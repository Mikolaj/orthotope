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

-- A client that sums every component of a call's result, an array's shape,
-- strides, offset and vector included, rather than forcing it to normal
-- form: one that a call inlined into it may pass its fields unbuilt.
{-# LANGUAGE BangPatterns, FlexibleContexts, FlexibleInstances #-}
module Summed (Summed (..), sumVec) where

import Data.Char (ord)
import Data.Int (Int64)
import Data.Monoid (Sum (..))
import qualified Data.Vector as V
import qualified Data.Vector.Generic as VG
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU

import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.Dynamic as DB
import qualified Data.Array.Internal.DynamicG as DG
import qualified Data.Array.Internal.DynamicS as DS
import qualified Data.Array.Internal.DynamicU as DU
import qualified Data.Array.Internal.Ranked as RB
import qualified Data.Array.Internal.RankedG as RG
import qualified Data.Array.Internal.RankedS as RS
import qualified Data.Array.Internal.RankedU as RU
import qualified Data.Array.Internal.Shape as Sh
import qualified Data.Array.Internal.Shaped as SB
import qualified Data.Array.Internal.ShapedG as SG
import qualified Data.Array.Internal.ShapedS as SS
import qualified Data.Array.Internal.ShapedU as SU

class Summed b where
  summed :: b -> Double

-- | The sum of a vector's elements, each summed: a loop of its own and not
-- V.sum, to keep noise from the vector package's machinery, which churns
-- between its releases, out of the readings.
{-# INLINE sumVec #-}
sumVec :: (VG.Vector v e, Summed e) => v e -> Double
sumVec v = go 0 0
  where
    !len = VG.length v
    go !i !acc | i >= len = acc
               | otherwise = go (i + 1) (acc + summed (VG.unsafeIndex v i))

{-# INLINE sumT #-}
sumT :: (VG.Vector v e, Summed e) => [Int] -> I.T v e -> Double
sumT sh (I.T st o v) = fromIntegral (sum sh + sum st + o) + sumVec v

instance Summed Double where
  {-# INLINE summed #-}
  summed = id
instance Summed Int where
  {-# INLINE summed #-}
  summed = fromIntegral
instance Summed Int64 where
  {-# INLINE summed #-}
  summed = fromIntegral
instance Summed Bool where
  {-# INLINE summed #-}
  summed = fromIntegral . fromEnum
instance Summed Char where
  {-# INLINE summed #-}
  summed = fromIntegral . ord
instance Summed Ordering where
  {-# INLINE summed #-}
  summed = fromIntegral . fromEnum
instance Summed a => Summed [a] where
  {-# INLINE summed #-}
  summed = sum . map summed
instance (Summed a, Summed b) => Summed (a, b) where
  {-# INLINE summed #-}
  summed (a, b) = summed a + summed b
instance (Summed a, Summed b) => Summed (Either a b) where
  {-# INLINE summed #-}
  summed = either summed summed
instance Summed a => Summed (V.Vector a) where
  {-# INLINE summed #-}
  summed = sumVec
instance (VS.Storable a, Summed a) => Summed (VS.Vector a) where
  {-# INLINE summed #-}
  summed = sumVec
instance (VU.Unbox a, Summed a) => Summed (VU.Vector a) where
  {-# INLINE summed #-}
  summed = sumVec

instance Summed a => Summed (DB.Array a) where
  {-# INLINE summed #-}
  summed (DB.A (DG.A sh t)) = sumT sh t
instance (VS.Storable a, Summed a) => Summed (DS.Array a) where
  {-# INLINE summed #-}
  summed (DS.A (DG.A sh t)) = sumT sh t
instance (VU.Unbox a, Summed a) => Summed (DU.Array a) where
  {-# INLINE summed #-}
  summed (DU.A (DG.A sh t)) = sumT sh t
instance Summed a => Summed (RB.Array n a) where
  {-# INLINE summed #-}
  summed (RB.A (RG.A sh t)) = sumT sh t
instance (VS.Storable a, Summed a) => Summed (RS.Array n a) where
  {-# INLINE summed #-}
  summed (RS.A (RG.A sh t)) = sumT sh t
instance (VU.Unbox a, Summed a) => Summed (RU.Array n a) where
  {-# INLINE summed #-}
  summed (RU.A (RG.A sh t)) = sumT sh t
instance (Sh.Shape sh, Summed a) => Summed (SB.Array sh a) where
  {-# INLINE summed #-}
  summed (SB.A a@(SG.A t)) = sumT (SG.shapeL a) t
instance (Sh.Shape sh, VS.Storable a, Summed a) => Summed (SS.Array sh a) where
  {-# INLINE summed #-}
  summed (SS.A a@(SG.A t)) = sumT (SG.shapeL a) t
instance (Sh.Shape sh, VU.Unbox a, Summed a) => Summed (SU.Array sh a) where
  {-# INLINE summed #-}
  summed (SU.A a@(SG.A t)) = sumT (SG.shapeL a) t
instance (VG.Vector v a, Summed a)
         => Summed (DG.Array v a) where
  {-# INLINE summed #-}
  summed (DG.A sh t) = sumT sh t
instance (VG.Vector v a, Summed a)
         => Summed (RG.Array n v a) where
  {-# INLINE summed #-}
  summed (RG.A sh t) = sumT sh t
instance (Sh.Shape sh, VG.Vector v a, Summed a)
         => Summed (SG.Array sh v a) where
  {-# INLINE summed #-}
  summed a@(SG.A t) = sumT (SG.shapeL a) t
instance Summed a => Summed (Sum a) where
  {-# INLINE summed #-}
  summed = summed . getSum
