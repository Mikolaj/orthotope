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

{-# LANGUAGE AllowAmbiguousTypes #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE RankNTypes #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE TypeOperators #-}
-- Ranked arrays against Dynamic ones, at the boxed, Storable, Unboxed
-- and list instances of Vector, with Int and Word8 elements: the random
-- views of the dynamic test modules as Ranked arrays of their ranks,
-- every operation of those views and invalid ones done by Ranked, and
-- the operations whose ranks their types fix on the random views of rank
-- 3, rotate also on those of ranks 1 and 2, and the arrays built from
-- nothing.
module RankedGTest(test) where

import Control.DeepSeq (NFData, force)
import Control.Exception (ErrorCall (..), evaluate, try)
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.Array.Internal.DynamicS ()
import Data.Array.Internal.DynamicU ()
import qualified Data.Array.Internal.RankedG as RG
import Data.Proxy (Proxy (..))
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import Data.Word (Word8)
import Foreign.Storable (Storable)
import GHC.TypeLits (KnownNat, SomeNat (..), someNatVal, type (+))
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  ( Arbitrary (..), Property, choose, conjoin, counterexample, forAll, ioProperty
  , property, suchThat, (.&&.), (===) )
import Views
  ( Elem, Op (..), View (..), applyOpG, genBadOp, genElems, mkViewG, opShape
  , testPropertyN, upTo )

test :: Test
test = testGroup "RankedG" $ backends @Int ++ [testGroup "Word8" (backends @Word8)]

-- The properties at each instance of Vector, with elements of an Elem type.
backends :: forall a . (Elem a, Storable a, VU.Unbox a) => [Test]
backends =
  [ backend @V.Vector @a "boxed"
  , backend @VS.Vector @a "Storable"
  , backend @VU.Vector @a "Unboxed"
  , backend @[] @a "list"
  ]

backend :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
           String -> Test
backend n = testGroup n
  [ testPropertyN "prop_views" (prop_views @v @a)
  , testPropertyN "prop_viewOps" (prop_viewOps @v @a)
  , testPropertyN "prop_badOps" (prop_badOps @v @a)
  , testPropertyN "prop_rank3" (prop_rank3 @v @a)
  , testPropertyN "prop_rotate" (prop_rotate @v @a)
  ]

-- Run the continuation at the rank given, as a type.
withRank :: Int -> (forall n . KnownNat n => Proxy n -> r) -> r
withRank n f = case someNatVal (toInteger n) of
  Just (SomeNat p) -> f p
  Nothing -> error ("withRank: " ++ show n)

-- The Ranked array a Dynamic one is, and the same array at another rank,
-- the rank being only in its type.
toR :: DG.Array v a -> RG.Array n v a
toR (DG.A sh t) = RG.A sh t

retype :: RG.Array n v a -> RG.Array m v a
retype (RG.A sh t) = RG.A sh t

-- The shape and the elements of an array.
obs :: (I.Vector v, I.VecElem v a) => RG.Array n v a -> ([Int], [a])
obs a = (RG.shapeL a, RG.toList a)

obsD :: (I.Vector v, I.VecElem v a) => DG.Array v a -> ([Int], [a])
obsD x = (DG.shapeL x, DG.toList x)

-- The two are equal, or fail with messages that agree up to their first
-- colon.
sameAs :: (NFData b, Eq b, Show b) => b -> b -> Property
sameAs a b = ioProperty $ do
  ra <- try (evaluate (force a))
  rb <- try (evaluate (force b))
  return $ case (ra, rb) of
    (Right a', Right b') -> a' === b'
    (Left (ErrorCall e), Left (ErrorCall e')) -> takeWhile (/= ':') e === takeWhile (/= ':') e'
    _ -> counterexample (see ra ++ " /= " ++ see rb) False
  where see = either (\ (ErrorCall e) -> "error " ++ e) show

-- A random view, as a Ranked array of its rank, gives what it does as a
-- Dynamic array or a list: its elements, their reductions and right fold,
-- its order against an array of its elements with at most one of them
-- changed, the results of normalize, mapA, zipWithA, reduce, pad, append
-- and reshape to one dimension; and it reads back from its show.
prop_views :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
              View -> Property
prop_views v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkViewG v xs :: DG.Array v a
      xsh = DG.shapeL x
      l = DG.toList x
      ps = [ (1, 2) | not (null xsh) ]
  in  withRank (length xsh) $ \ (_ :: Proxy n) ->
      let r = toR x :: RG.Array n v a
      in  forAll (choose (0, length l)) $ \ i ->
          let l' = [ if k == i then e + 1 else e | (k, e) <- zip [0 ..] l ]
              r' = RG.fromList xsh l' :: RG.Array n v a
          in  RG.toList r === l .&&. RG.toVector r === DG.toVector x
              .&&. RG.toList (RG.normalize r) === l
              .&&. RG.sumA r === sum l .&&. RG.productA r === product l
              .&&. RG.anyA (> 0) r === any (> 0) l .&&. RG.allA (> 0) r === all (> 0) l
              .&&. (if null l then property True
                    else RG.maximumA r === maximum l .&&. RG.minimumA r === minimum l)
              .&&. RG.allSameA r === DG.allSameA x .&&. RG.foldrA (:) [] r === l
              .&&. (r == r') === (l == l') .&&. compare r r' === compare l l'
              .&&. RG.toList (RG.mapA (* 2) r) === map (* 2) l
              .&&. RG.toList (RG.zipWithA (-) r r') === zipWith (-) l l'
              .&&. RG.unScalar (RG.reduce (+) 0 r) === sum l
              .&&. obs (RG.pad ps 0 r) === obsD (DG.pad ps 0 x)
              .&&. (if null xsh then property True else obs (RG.append r r) === obsD (DG.append x x))
              .&&. obs (RG.reshape @n @1 [length l] r) === obsD (DG.reshape [length l] x)
              .&&. read (show r) === r

-- The Ranked operation of an Op, from an array of rank n to one of rank n'.
applyOpR :: forall n n' v a . (KnownNat n, KnownNat n', I.Vector v, I.VecElem v a) =>
            Op -> RG.Array n v a -> RG.Array n' v a
applyOpR (Transpose is) = retype . RG.transpose is
applyOpR (Rev rs) = retype . RG.rev rs
applyOpR (Slice sl) = retype . RG.slice sl
applyOpR (Stride ts) = retype . RG.stride ts
applyOpR (Window ws) = RG.window ws
applyOpR (Index i) = \ a -> RG.index (retype a :: RG.Array (1 + n') v a) i
applyOpR (Broadcast ds sh) = RG.broadcast ds sh
applyOpR (Raw sh ss o k m) = \ a ->
  let v = RG.toVector a in RG.A sh (I.T ss o (I.vSlice k (I.vLength v - k - m) v))

-- Each operation of a random view, done by Ranked at the ranks of its
-- argument and of its result, gives what Dynamic's does.
prop_viewOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOpG) (DG.fromList sh (upTo (product sh))) ops :: [DG.Array v a]
      step (x, op, y) =
        withRank (DG.rank x) $ \ (_ :: Proxy n) ->
        withRank (DG.rank y) $ \ (_ :: Proxy n') ->
        counterexample (show op) (obs (applyOpR @n @n' op (toR x)) === obsD y)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- The rank of the result of an operation on an array of rank n, as the
-- type of the Ranked operation fixes it, but for index of a scalar, which
-- no type allows.
opRank :: Int -> Op -> Maybe Int
opRank n (Window ws) = Just (n + length ws)
opRank n (Index _) = if n > 0 then Just (n - 1) else Nothing
opRank _ (Broadcast _ sh) = Just (length sh)
opRank _ (Raw sh _ _ _ _) = Just (length sh)
opRank n _ = Just n

-- An operation invalid on a random view, done by Ranked at the rank of the
-- view and the rank opRank gives, fails as Dynamic's does.
prop_badOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_badOps v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: DG.Array v a
  in  forAll (genBadOp (DG.shapeL x)) $ \ op ->
      case opRank (DG.rank x) op of
        Nothing -> property True
        Just r ->
          withRank (DG.rank x) $ \ (_ :: Proxy n) ->
          withRank r $ \ (_ :: Proxy n') ->
          sameAs (obs (applyOpR @n @n' op (toR x))) (obsD (applyOpG op x))

-- The rank of a view.
rankOf :: View -> Int
rankOf (View sh ops) = length (foldl opShape sh ops)

-- rotate, rerank, rerank2, unravel, ravel, stretch and stretchOuter,
-- whose types fix the ranks they take, give what Dynamic's do on the
-- random views of rank 3, or fail as they do: rotate for any dimension
-- and a number of rotations from -2 up, stretch and stretchOuter to an
-- outer extent from 0 up.  constant, generate, iota and iterateN, at
-- that extent, give what Dynamic's do too.
prop_rank3 :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => Property
prop_rank3 =
  forAll (arbitrary `suchThat` ((== 3) . rankOf)) $ \ v@(View sh _) ->
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  forAll (choose (-2, 9)) $ \ k ->
  let x = mkViewG v xs :: DG.Array v a
      r = toR x :: RG.Array 3 v a
      xsh = DG.shapeL x
      e = max 0 k  -- an extent
      rot :: Int -> RG.Array 4 v a -> Property
      rot d a = counterexample ("rotate " ++ show d) (sameAs (obs a) (obsD (DG.rotate d k x)))
      nested ps = (concatMap fst ps, concatMap snd ps)
  in  rot 0 (RG.rotate @0 @3 k r) .&&. rot 1 (RG.rotate @1 @2 k r) .&&. rot 2 (RG.rotate @2 @1 k r)
      .&&. counterexample "rerank 1"
             (sameAs (obs (RG.rerank @1 (RG.transpose [1,0]) r))
                     (obsD (DG.rerank 1 (DG.transpose [1,0]) x)))
      .&&. counterexample "rerank 2"
             (sameAs (obs (RG.rerank @2 (RG.reduce (+) 0) r)) (obsD (DG.rerank 2 (DG.reduce (+) 0) x)))
      .&&. counterexample "rerank2 2"
             (sameAs (obs (RG.rerank2 @2 (RG.zipWithA (+)) r r))
                     (obsD (DG.rerank2 2 (DG.zipWithA (+)) x x)))
      .&&. counterexample "unravel"
             (sameAs (nested (map obs (RG.toList (RG.unravel r :: RG.Array 1 V.Vector (RG.Array 2 v a)))))
                     (nested (map obsD (DG.toList (DG.unravel x :: DG.Array V.Vector (DG.Array v a))))))
      .&&. counterexample "ravel"
             (sameAs (obs (RG.ravel (RG.unravel r :: RG.Array 1 V.Vector (RG.Array 2 v a))))
                     (obsD (DG.ravel (DG.unravel x :: DG.Array V.Vector (DG.Array v a)))))
      .&&. counterexample "stretch"
             (sameAs (obs (RG.stretch (e : xsh) (RG.reshape @3 @4 (1 : xsh) r)))
                     (obsD (DG.stretch (e : xsh) (DG.reshape (1 : xsh) x))))
      .&&. counterexample "stretchOuter"
             (sameAs (obs (RG.stretchOuter e (RG.reshape @3 @4 (1 : xsh) r)))
                     (obsD (DG.stretchOuter e (DG.reshape (1 : xsh) x))))
      .&&. counterexample "constant"
             (sameAs (obs (RG.constant [e, 3] 7 :: RG.Array 2 v a))
                     (obsD (DG.constant [e, 3] 7 :: DG.Array v a)))
      .&&. counterexample "generate"
             (sameAs (obs (RG.generate [2, e] (fromIntegral . sum) :: RG.Array 2 v a))
                     (obsD (DG.generate [2, e] (fromIntegral . sum) :: DG.Array v a)))
      .&&. counterexample "iota"
             (sameAs (obs (RG.iota e :: RG.Array 1 v a)) (obsD (DG.iota e :: DG.Array v a)))
      .&&. counterexample "iterateN"
             (sameAs (obs (RG.iterateN e (+ 1) 0 :: RG.Array 1 v a))
                     (obsD (DG.iterateN e (+ 1) 0 :: DG.Array v a)))

-- rotate gives what Dynamic's does, or fails as it does, on the random
-- views of ranks 1 and 2, for any dimension and a number of rotations from
-- -2 up.
prop_rotate :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => Property
prop_rotate =
  forAll (arbitrary `suchThat` ((`elem` [1, 2]) . rankOf)) $ \ v@(View sh _) ->
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  forAll (choose (-2, 9)) $ \ k ->
  let x = mkViewG v xs :: DG.Array v a
      rot :: Int -> RG.Array m v a -> Property
      rot d a = counterexample ("rotate " ++ show d) (sameAs (obs a) (obsD (DG.rotate d k x)))
  in  if DG.rank x == 1 then rot 0 (RG.rotate @0 @1 k (toR x :: RG.Array 1 v a))
      else rot 0 (RG.rotate @0 @2 k (toR x :: RG.Array 2 v a))
           .&&. rot 1 (RG.rotate @1 @1 k (toR x :: RG.Array 2 v a))
