-- Copyright 2020 Google LLC
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE TypeOperators #-}
module Data.Array.Convert(Convert(..)) where
import Data.Proxy
import qualified Data.Vector as V
import qualified Data.Vector.Generic as VG
import qualified Data.Vector.Unboxed as VU
import qualified Data.Vector.Storable as VS
import GHC.TypeLits(KnownNat, natVal)

import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.Dynamic as D
import qualified Data.Array.Internal.DynamicG as DG
import qualified Data.Array.Internal.DynamicS as DS
import qualified Data.Array.Internal.DynamicU as DU
import qualified Data.Array.Internal.Ranked as R
import qualified Data.Array.Internal.RankedG as RG
import qualified Data.Array.Internal.RankedS as RS
import qualified Data.Array.Internal.RankedU as RU
import qualified Data.Array.Internal.Shaped as S
import qualified Data.Array.Internal.ShapedG as SG
import qualified Data.Array.Internal.ShapedS as SS
import qualified Data.Array.Internal.ShapedU as SU
import Data.Array.Internal.Shape(Shape(..))

-- INLINE: on GHC HEAD (2026-10-10), under INLINABLE a client's specialised
-- convert still called its worker with the Storable dictionary, running 3.5
-- times the instructions, since the instance's a ~ b casts that dictionary
-- (https://gitlab.haskell.org/ghc/ghc/-/work_items/27920).
-- A Storable vector copied into a boxed one, each element read before it
-- is stored, where vector's convert stores the read as a thunk holding the
-- Storable vector (https://github.com/haskell/vector/issues/570).  On GHC
-- HEAD, converting a view of 200000 Doubles took 0.28 of the time at -O1
-- and allocated 72 bytes an element where 120; with vector patched as the issue
-- proposes and -fspec-constr, it took 0.93 to 0.95 of it.
{-# INLINE fromStorable #-}
fromStorable :: VS.Storable a => VS.Vector a -> V.Vector a
fromStorable v =
  I.genericZipLoop (VS.length v) (\ i -> return $! VS.unsafeIndex v i)

-- A view converted between the vector package's boxings, the source's
-- elements read as stored: a range by vector's convert, any other view walked.
{-# INLINE boxingT #-}
boxingT :: (VG.Vector v a, VG.Vector w a, I.Vector v, I.VecElem v a,
            I.Vector w, I.VecElem w a)
        => [Int] -> I.T v a -> I.T w a
boxingT sh = I.convertT sh V.convert (I.genericMapStrided False id)

-- A Storable view converted to a boxed one, each element read before it is
-- stored, as 'fromStorable' reads it.
{-# INLINE fromStorableT #-}
fromStorableT :: VS.Storable a => [Int] -> I.T VS.Vector a -> I.T V.Vector a
fromStorableT sh = I.convertT sh fromStorable (I.genericMapStrided True id)

class Convert a b where
  -- | Convert between two array types.
  -- If both arrays have the same flavor of boxing this is a O(1)
  -- operation. Conversion between different boxing is a O(n) operation.
  convert  :: a -> b
  -- | Convert between two array types if possible, or return error message.
  convertE :: a -> Either String b
  {-# INLINABLE convert #-}
  convert = either error id . convertE
  -- Lazy in convert's result.  The instances below in which building
  -- no thunk under Right saved bytes define convertE strictly; strict
  -- here, on GHC HEAD 10.1.20260918 (2026-10-15), a boxed array
  -- converted to a Storable one allocated 8 to 16 bytes a call more
  -- where forced, and a boxed Dynamic or Ranked one converted to an
  -- Unboxed one 40 more where summed, against 24 less where forced.
  -- The forced cost, where read, was a thunk of GHC's tag inference
  -- (https://gitlab.haskell.org/ghc/ghc/-/work_items/27841),
  -- and the summed one a call of a method of the benchmark's
  -- summing dictionary, used once and left out of line by design
  -- (https://gitlab.haskell.org/ghc/ghc/-/work_items/26571).
  {-# INLINE convertE #-}
  convertE = Right . convert
  {-# MINIMAL convert | convertE #-}

-- Whether a shape is the one the type gives. Monomorphic, so that no client
-- calls base's list equality with Integer's dictionary.
sameShape :: [Int] -> [Integer] -> Bool
sameShape (x : xs) (y : ys) = toInteger x == y && sameShape xs ys
sameShape [] [] = True
sameShape _ _ = False

-- INLINE: on GHC HEAD 10.1.20261019 (2026-10-22), under INLINABLE it stayed
-- out of line, returning the Either its caller takes apart built, and the
-- specialisation benchmark's convert to a Shaped array of a small or empty
-- array allocated 16 bytes a call more, 48 summed, and convertE to one of
-- another shape 32 more, and 72 summed from a Ranked array.
-- The checks of a conversion to a Shaped array: the shape against the type's,
-- then the type's against the check of 'shapeP', made once a dictionary.
{-# INLINE shapedE #-}
shapedE :: Shape sh => Proxy sh -> [Int] -> r -> Either String r
shapedE p sh r | not (sameShape sh ns) = Left $ "convert: shape mismatch "
                 ++ show (sh, ns)
               | not (validP p) = Left $ "convert: bad shape " ++ show ns
               | otherwise = Right r
  where ns = natsP p

-- INLINE: see shapedE.
-- The check of a conversion to a Ranked array: the shape's rank against the
-- type's.
{-# INLINE rankedE #-}
rankedE :: KnownNat n => Proxy n -> [Int] -> r -> Either String r
rankedE p sh r
  | toInteger (length sh) /= n =
      Left $ "convert: rank mismatch " ++ show (sh, n)
  | otherwise = Right r
  where n = natVal p

-- We write these instances like "instance (a ~ b) => Convert (X a) (Y b)" so
-- that instance resolution will commit to them as soon as it knows the array
-- types, and then introduce an equality constraint on the element types.  This
-- way, if you call 'convert' on an array, type inference can propagate the
-- element type across the conversion.  If we wrote them like  "instance
-- Convert (X a) (Y a)" instead, they'd not be selected until the element types
-- of both arrays are determined to be the same by other means, which would
-- lead to unnecessary ambiguity errors.
--
-- The conversions between boxings are INLINABLE, so that a client specialises
-- them at its element type: their worker, with 'I.convertT' inlined into it,
-- is too big for an unfolding of its own, and called with the element's
-- dictionary, converting a dense array of 200000 Doubles ran 2.3 to 7.0 times
-- the instructions and allocated up to 12 times as much.

-----

instance (a ~ b, DU.Unbox a) => Convert (D.Array a) (DU.Array b) where
  {-# INLINABLE convert #-}
  convert (D.A (DG.A sh t)) = DU.A (DG.A sh (boxingT sh t))

instance (a ~ b, DU.Unbox a) => Convert (DU.Array a) (D.Array b) where
  {-# INLINABLE convert #-}
  convert (DU.A (DG.A sh t)) = D.A (DG.A sh (boxingT sh t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

instance (a ~ b, DS.Unbox a) => Convert (D.Array a) (DS.Array b) where
  {-# INLINABLE convert #-}
  convert (D.A (DG.A sh t)) = DS.A (DG.A sh (boxingT sh t))

instance (a ~ b, DS.Unbox a) => Convert (DS.Array a) (D.Array b) where
  {-# INLINABLE convert #-}
  convert (DS.A (DG.A sh t)) = D.A (DG.A sh (fromStorableT sh t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

-- As above with the element types, we arrange to select the Convert instance
-- before the ranks are known to be equal, then constrain them to be equal.

instance (a ~ b, n ~ m, RU.Unbox a) => Convert (R.Array n a) (RU.Array m b) where
  {-# INLINABLE convert #-}
  convert (R.A (RG.A sh t)) = RU.A (RG.A sh (boxingT sh t))

instance (a ~ b, n ~ m, RU.Unbox a) => Convert (RU.Array n a) (R.Array m b) where
  {-# INLINABLE convert #-}
  convert (RU.A (RG.A sh t)) = R.A (RG.A sh (boxingT sh t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

instance (a ~ b, n ~ m, RS.Unbox a) => Convert (R.Array n a) (RS.Array m b) where
  {-# INLINABLE convert #-}
  convert (R.A (RG.A sh t)) = RS.A (RG.A sh (boxingT sh t))

instance (a ~ b, n ~ m, RS.Unbox a) => Convert (RS.Array n a) (R.Array m b) where
  {-# INLINABLE convert #-}
  convert (RS.A (RG.A sh t)) = R.A (RG.A sh (fromStorableT sh t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

instance (a ~ b, n ~ m, SU.Unbox a, S.Shape n)
         => Convert (S.Array n a) (SU.Array m b) where
  {-# INLINABLE convert #-}
  convert (S.A g@(SG.A t)) = SU.A (SG.A (boxingT (SG.shapeL g) t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

instance (a ~ b, n ~ m, SU.Unbox a, S.Shape n)
         => Convert (SU.Array n a) (S.Array m b) where
  {-# INLINABLE convert #-}
  convert (SU.A g@(SG.A t)) = S.A (SG.A (boxingT (SG.shapeL g) t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

instance (a ~ b, n ~ m, SS.Unbox a, S.Shape n)
         => Convert (S.Array n a) (SS.Array m b) where
  {-# INLINABLE convert #-}
  convert (S.A g@(SG.A t)) = SS.A (SG.A (boxingT (SG.shapeL g) t))

instance (a ~ b, n ~ m, SS.Unbox a, S.Shape n)
         => Convert (SS.Array n a) (S.Array m b) where
  {-# INLINABLE convert #-}
  convert (SS.A g@(SG.A t)) = S.A (SG.A (fromStorableT (SG.shapeL g) t))
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

-----

instance (a ~ b) => Convert (R.Array n a) (D.Array b) where
  {-# INLINE convert #-}
  convert (R.A (RG.A sh t)) = D.A (DG.A sh t)
  convertE x = Right $! convert x

instance (a ~ b, KnownNat n) => Convert (D.Array a) (R.Array n b) where
  -- INLINE: on GHC HEAD 10.1.20260918 (2026-10-15), the convertE methods that
  -- check a rank or a shape INLINABLE, as their contexts give them, cost the
  -- specialisation benchmark's summed conversions to Shaped arrays 16 to 40
  -- bytes a call, against 16 saved where forced.
  {-# INLINE convertE #-}
  convertE (D.A (DG.A sh t)) = rankedE (Proxy :: Proxy n) sh $ R.A (RG.A sh t)

instance (a ~ b, S.Shape sh) => Convert (S.Array sh a) (D.Array b) where
  {-# INLINE convert #-}
  convert (S.A a@(SG.A t)) = D.A (DG.A (SG.shapeL a) t)
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

instance (a ~ b, S.Rank sh ~ n, S.Shape sh) => Convert (S.Array sh a) (R.Array n b) where
  {-# INLINE convert #-}
  convert (S.A a@(SG.A t)) = R.A (RG.A (SG.shapeL a) t)
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

instance (a ~ b, S.Shape sh) => Convert (D.Array a) (S.Array sh b) where
  -- INLINE: see convertE from D.Array to R.Array above.
  {-# INLINE convertE #-}
  convertE (D.A (DG.A sh t)) = shapedE (Proxy :: Proxy sh) sh $ S.A (SG.A t)

instance (a ~ b, S.Rank sh ~ n, S.Shape sh) => Convert (R.Array n a) (S.Array sh b) where
  -- INLINE: see convertE from D.Array to R.Array above.
  {-# INLINE convertE #-}
  convertE (R.A (RG.A sh t)) = shapedE (Proxy :: Proxy sh) sh $ S.A (SG.A t)

------

instance (a ~ b) => Convert (RS.Array n a) (DS.Array b) where
  {-# INLINE convert #-}
  convert (RS.A (RG.A sh t)) = DS.A (DG.A sh t)
  convertE x = Right $! convert x

instance (a ~ b, KnownNat n) => Convert (DS.Array a) (RS.Array n b) where
  -- INLINE: see convertE from D.Array to R.Array above.
  {-# INLINE convertE #-}
  convertE (DS.A (DG.A sh t)) = rankedE (Proxy :: Proxy n) sh $ RS.A (RG.A sh t)

instance (a ~ b, SS.Shape sh) => Convert (SS.Array sh a) (DS.Array b) where
  {-# INLINE convert #-}
  convert (SS.A a@(SG.A t)) = DS.A (DG.A (SG.shapeL a) t)
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

instance (a ~ b, SS.Rank sh ~ n, SS.Shape sh)
         => Convert (SS.Array sh a) (RS.Array n b) where
  {-# INLINE convert #-}
  convert (SS.A a@(SG.A t)) = RS.A (RG.A (SG.shapeL a) t)
  {-# INLINABLE convertE #-}
  convertE x = Right $! convert x

instance (a ~ b, SS.Shape sh) => Convert (DS.Array a) (SS.Array sh b) where
  -- INLINE: see convertE from D.Array to R.Array above.
  {-# INLINE convertE #-}
  convertE (DS.A (DG.A sh t)) = shapedE (Proxy :: Proxy sh) sh $ SS.A (SG.A t)

instance (a ~ b, SS.Rank sh ~ n, SS.Shape sh)
         => Convert (RS.Array n a) (SS.Array sh b) where
  -- INLINE: see convertE from D.Array to R.Array above.
  {-# INLINE convertE #-}
  convertE (RS.A (RG.A sh t)) = shapedE (Proxy :: Proxy sh) sh $ SS.A (SG.A t)

------

instance (a ~ b) => Convert (D.Array a) (DG.Array V.Vector b) where
  {-# INLINE convert #-}
  convert (D.A a) = a

instance (a ~ b) => Convert (DU.Array a) (DG.Array VU.Vector b) where
  {-# INLINE convert #-}
  convert (DU.A a) = a

instance (a ~ b) => Convert (DS.Array a) (DG.Array VS.Vector b) where
  {-# INLINE convert #-}
  convert (DS.A a) = a

------

instance (a ~ b, n ~ m) => Convert (R.Array n a) (RG.Array m V.Vector b) where
  {-# INLINE convert #-}
  convert (R.A a) = a

instance (a ~ b, n ~ m) => Convert (RU.Array n a) (RG.Array m VU.Vector b) where
  {-# INLINE convert #-}
  convert (RU.A a) = a

instance (a ~ b, n ~ m) => Convert (RS.Array n a) (RG.Array m VS.Vector b) where
  {-# INLINE convert #-}
  convert (RS.A a) = a

------

instance (a ~ b, s ~ t) => Convert (S.Array s a) (SG.Array t V.Vector b) where
  {-# INLINE convert #-}
  convert (S.A a) = a

instance (a ~ b, s ~ t) => Convert (SU.Array s a) (SG.Array t VU.Vector b) where
  {-# INLINE convert #-}
  convert (SU.A a) = a

instance (a ~ b, s ~ t) => Convert (SS.Array s a) (SG.Array t VS.Vector b) where
  {-# INLINE convert #-}
  convert (SS.A a) = a

------

-- XXX need more conversions.
