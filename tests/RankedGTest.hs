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
-- Ranked arrays against Dynamic ones, at the boxed, Storable, Unboxed and
-- list instances of Vector: the random views of the dynamic test modules
-- as Ranked arrays of their ranks, every operation of those views done by
-- Ranked, and the operations whose ranks their types fix on the random
-- views of rank 3, rotate also on those of ranks 1 and 2.
module RankedGTest(test) where

import Control.DeepSeq (NFData, force)
import Control.Exception (ErrorCall (..), evaluate, try)
import qualified Data.Array.Dynamic as DD
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as D
import Data.Array.Internal.DynamicS ()
import Data.Array.Internal.DynamicU ()
import qualified Data.Array.Internal.RankedG as R
import Data.Proxy (Proxy (..))
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import GHC.TypeLits (KnownNat, SomeNat (..), someNatVal, type (+))
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  ( Arbitrary (..), Property, choose, conjoin, counterexample, forAll, ioProperty
  , property, suchThat, vectorOf, (.&&.), (===) )
import Views (Op (..), View (..), applyOpG, mkView, mkViewG, testPropertyN)

test :: Test
test = testGroup "RankedG"
  [ backend @V.Vector "boxed"
  , backend @VS.Vector "Storable"
  , backend @VU.Vector "Unboxed"
  , backend @[] "list"
  ]

backend :: forall v . (I.Vector v, I.VecElem v Int, Ord (v Int), Show (v Int)) => String -> Test
backend n = testGroup n
  [ testPropertyN "prop_views" (prop_views @v)
  , testPropertyN "prop_viewOps" (prop_viewOps @v)
  , testPropertyN "prop_rank3" (prop_rank3 @v)
  , testPropertyN "prop_rotate" (prop_rotate @v)
  ]

-- Run the continuation at the rank given, as a type.
withRank :: Int -> (forall n . KnownNat n => Proxy n -> r) -> r
withRank n f = case someNatVal (toInteger n) of
  Just (SomeNat p) -> f p
  Nothing -> error ("withRank: " ++ show n)

-- The Ranked array a Dynamic one is, and the same array at another rank,
-- the rank being only in its type.
toR :: D.Array v a -> R.Array n v a
toR (D.A sh t) = R.A sh t

retype :: R.Array n v a -> R.Array m v a
retype (R.A sh t) = R.A sh t

-- The shape and the elements of an array.
obs :: (I.Vector v, I.VecElem v Int) => R.Array n v Int -> ([Int], [Int])
obs a = (R.shapeL a, R.toList a)

obsD :: (I.Vector v, I.VecElem v Int) => D.Array v Int -> ([Int], [Int])
obsD x = (D.shapeL x, D.toList x)

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
prop_views :: forall v . (I.Vector v, I.VecElem v Int, Ord (v Int), Show (v Int)) =>
              View -> Property
prop_views v@(View sh _) =
  forAll (vectorOf (product sh) (choose (-9, 9))) $ \ xs ->
  let x = mkViewG v xs :: D.Array v Int
      xsh = D.shapeL x
      l = D.toList x
      ps = [ (1, 2) | not (null xsh) ]
  in  withRank (length xsh) $ \ (_ :: Proxy n) ->
      let r = toR x :: R.Array n v Int
      in  forAll (choose (0, length l)) $ \ i ->
          let l' = [ if k == i then e + 1 else e | (k, e) <- zip [0 ..] l ]
              r' = R.fromList xsh l' :: R.Array n v Int
          in  R.toList r === l .&&. R.toVector r === D.toVector x
              .&&. R.toList (R.normalize r) === l
              .&&. R.sumA r === sum l .&&. R.productA r === product l
              .&&. R.anyA (> 0) r === any (> 0) l .&&. R.allA (> 0) r === all (> 0) l
              .&&. (if null l then property True
                    else R.maximumA r === maximum l .&&. R.minimumA r === minimum l)
              .&&. R.allSameA r === D.allSameA x .&&. R.foldrA (:) [] r === l
              .&&. (r == r') === (l == l') .&&. compare r r' === compare l l'
              .&&. R.toList (R.mapA (* 2) r) === map (* 2) l
              .&&. R.toList (R.zipWithA (-) r r') === zipWith (-) l l'
              .&&. R.unScalar (R.reduce (+) 0 r) === sum l
              .&&. obs (R.pad ps 0 r) === obsD (D.pad ps 0 x)
              .&&. (if null xsh then property True else obs (R.append r r) === obsD (D.append x x))
              .&&. obs (R.reshape @n @1 [length l] r) === obsD (D.reshape [length l] x)
              .&&. read (show r) === r

-- The Ranked operation of an Op, from an array of rank n to one of rank n'.
applyOpR :: forall n n' v a . (KnownNat n, KnownNat n', I.Vector v, I.VecElem v a) =>
            Op -> R.Array n v a -> R.Array n' v a
applyOpR (Transpose is) = retype . R.transpose is
applyOpR (Rev rs) = retype . R.rev rs
applyOpR (Slice sl) = retype . R.slice sl
applyOpR (Stride ts) = retype . R.stride ts
applyOpR (Window ws) = R.window ws
applyOpR (Index i) = \ a -> R.index (retype a :: R.Array (1 + n') v a) i
applyOpR (Broadcast ds sh) = R.broadcast ds sh

-- Each operation of a random view, done by Ranked at the ranks of its
-- argument and of its result, gives what Dynamic's does.
prop_viewOps :: forall v . (I.Vector v, I.VecElem v Int) => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOpG) (D.fromList sh [0 .. product sh - 1]) ops :: [D.Array v Int]
      step (x, op, y) =
        withRank (D.rank x) $ \ (_ :: Proxy n) ->
        withRank (D.rank y) $ \ (_ :: Proxy n') ->
        counterexample (show op) (obs (applyOpR @n @n' op (toR x)) === obsD y)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- The rank of a view.
rankOf :: View -> Int
rankOf v@(View sh _) = length (DD.shapeL (mkView v (replicate (product sh) ())))

-- rotate, rerank, rerank2, unravel and ravel, whose types fix the ranks
-- they take, give what Dynamic's do on the random views of rank 3, or
-- fail as they do: rotate for any dimension and a number of rotations
-- from -2 up.
prop_rank3 :: forall v . (I.Vector v, I.VecElem v Int) => Property
prop_rank3 =
  forAll (arbitrary `suchThat` ((== 3) . rankOf)) $ \ v@(View sh _) ->
  forAll (vectorOf (product sh) (choose (-9, 9))) $ \ xs ->
  forAll (choose (-2, 9)) $ \ k ->
  let x = mkViewG v xs :: D.Array v Int
      r = toR x :: R.Array 3 v Int
      rot :: Int -> R.Array 4 v Int -> Property
      rot d a = counterexample ("rotate " ++ show d) (sameAs (obs a) (obsD (D.rotate d k x)))
      nested ps = (concatMap fst ps, concatMap snd ps)
  in  rot 0 (R.rotate @0 @3 k r) .&&. rot 1 (R.rotate @1 @2 k r) .&&. rot 2 (R.rotate @2 @1 k r)
      .&&. counterexample "rerank 1"
             (sameAs (obs (R.rerank @1 (R.transpose [1,0]) r))
                     (obsD (D.rerank 1 (D.transpose [1,0]) x)))
      .&&. counterexample "rerank 2"
             (sameAs (obs (R.rerank @2 (R.reduce (+) 0) r)) (obsD (D.rerank 2 (D.reduce (+) 0) x)))
      .&&. counterexample "rerank2 2"
             (sameAs (obs (R.rerank2 @2 (R.zipWithA (+)) r r))
                     (obsD (D.rerank2 2 (D.zipWithA (+)) x x)))
      .&&. counterexample "unravel"
             (sameAs (nested (map obs (R.toList (R.unravel r :: R.Array 1 V.Vector (R.Array 2 v Int)))))
                     (nested (map obsD (D.toList (D.unravel x :: D.Array V.Vector (D.Array v Int))))))
      .&&. counterexample "ravel"
             (sameAs (obs (R.ravel (R.unravel r :: R.Array 1 V.Vector (R.Array 2 v Int))))
                     (obsD (D.ravel (D.unravel x :: D.Array V.Vector (D.Array v Int)))))

-- rotate gives what Dynamic's does, or fails as it does, on the random
-- views of ranks 1 and 2, for any dimension and a number of rotations from
-- -2 up.
prop_rotate :: forall v . (I.Vector v, I.VecElem v Int) => Property
prop_rotate =
  forAll (arbitrary `suchThat` ((`elem` [1, 2]) . rankOf)) $ \ v@(View sh _) ->
  forAll (vectorOf (product sh) (choose (-9, 9))) $ \ xs ->
  forAll (choose (-2, 9)) $ \ k ->
  let x = mkViewG v xs :: D.Array v Int
      rot :: Int -> R.Array m v Int -> Property
      rot d a = counterexample ("rotate " ++ show d) (sameAs (obs a) (obsD (D.rotate d k x)))
  in  if D.rank x == 1 then rot 0 (R.rotate @0 @1 k (toR x :: R.Array 1 v Int))
      else rot 0 (R.rotate @0 @2 k (toR x :: R.Array 2 v Int))
           .&&. rot 1 (R.rotate @1 @1 k (toR x :: R.Array 2 v Int))
