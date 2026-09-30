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
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
-- The properties the Storable and Unboxed test modules share, at the
-- list instance of Vector, which runs the generic code with the lists' own
-- methods.
module DynamicGTest(test) where

import Data.Array.DynamicG
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.List (zipWith4, zipWith5)
import Test.Framework (Test, testGroup)
import Data.Word (Word8)
import Test.QuickCheck
  ( Property, choose, conjoin, counterexample, elements, forAll, property, shuffle
  , sublistOf, vectorOf, (.&&.), (===), (==>) )
import Views
  ( Elem, Op (..), View (..), applyOpG, failsIn, failsWith, genBadOp, genElems, genShape, opNames
  , opShape, opSource, silentBadOp, testPropertyN, upTo )

test :: Test
test = testGroup "DynamicG" $
  testPropertyN "prop_allSameA" prop_allSameA
  : elemProps @Int ++ [testGroup "Word8" (elemProps @Word8)]

-- applyOp and mkView of Views, over arrays of lists.
applyOp :: Op -> Array [] a -> Array [] a
applyOp (Transpose is) = transpose is
applyOp (Rev rs) = rev rs
applyOp (Slice sl) = slice sl
applyOp (Stride ts) = stride ts
applyOp (Window ws) = window ws
applyOp (Index i) = (`index` i)
applyOp (Broadcast ds sh) = broadcast ds sh
applyOp op@Raw{} = applyOpG op

mkView :: View -> [a] -> Array [] a
mkView (View sh ops) xs = foldl (flip applyOp) (fromList sh xs) ops

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1], [1, 1, 1, 2 :: Double]]) $ \ pool ->
  forAll (vectorOf (product sh) (elements pool)) $ \ xs ->
  let x = mkView v xs
  in  allSameA x === I.allSame (toList x)

-- The properties run at each Elem type, all but that of NaN.
elemProps :: forall a . Elem a => [Test]
elemProps =
  [ testPropertyN "prop_toList" (prop_toList @a)
  , testPropertyN "prop_compare" (prop_compare @a)
  , testPropertyN "prop_reduce" (prop_reduce @a)
  , testPropertyN "prop_pad" (prop_pad @a)
  , testPropertyN "prop_viewOps" (prop_viewOps @a)
  , testPropertyN "prop_badOps" (prop_badOps @a)
  , testPropertyN "prop_copy" (prop_copy @a)
  , testPropertyN "prop_zipWith" (prop_zipWith @a)
  , testPropertyN "prop_update" (prop_update @a)
  , testPropertyN "prop_fromVector" (prop_fromVector @a)
  , testPropertyN "prop_show" (prop_show @a)
  , testPropertyN "prop_rerank" (prop_rerank @a)
  ]

-- toList and toVector agree with indexing the view element by element.
prop_toList :: forall a . Elem a => View -> Property
prop_toList v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      l = [ unScalar (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) (shapeL x) ]
  in  toList x === l .&&. toVector x === l

-- == and compare agree with comparing the lists, between a view and an
-- array of its elements with at most one of them changed, and between two
-- views of one layout over vectors that differ in at most one element,
-- inside the views or outside them.
prop_compare :: forall a . Elem a => View -> Property
prop_compare v@(View sh _) =
  let n = product sh
      x = mkView v (upTo n) :: Array [] a
      l = toList x
  in  forAll (choose (0, length l)) $ \ i ->
      forAll (choose (0, n)) $ \ j ->
      forAll (choose (-1, 1)) $ \ d ->
      let l' = [ if k == i then e + fromIntegral d else e | (k, e) <- zip [0 ..] l ]
          y = fromList (shapeL x) l'
          z = mkView v [ fromIntegral (if k == j then k + d else k) | k <- [0 .. n - 1] ]
      in  (x == y) === (l == l') .&&. compare x y === compare l l'
          .&&. compare y x === compare l' l
          .&&. (x == z) === (l == toList z) .&&. compare x z === compare l (toList z)

-- The reductions agree with the list's: reduce, sumA, productA, maximumA,
-- minimumA, anyA and allA.
prop_reduce :: forall a . Elem a => View -> Property
prop_reduce v@(View sh _) =
  forAll (genElems (1, 9) (product sh)) $ \ xs ->
  forAll (fromIntegral <$> choose (0, 9 :: Int)) $ \ t ->
  let x = mkView v xs :: Array [] a
      l = toList x
  in  reduce (+) 0 x === scalar (sum l)
      .&&. sumA x === sum l .&&. productA x === product l
      .&&. anyA (> t) x === any (> t) l .&&. allA (> t) x === all (> t) l
      .&&. (if null l then property True
            else maximumA x === maximum l .&&. minimumA x === minimum l)

-- pad agrees with indexing the view where an index falls inside it, and
-- gives the padding value elsewhere, for a pad list of any length up to
-- the rank that leaves at most 10000 elements.
prop_pad :: forall a . Elem a => View -> Property
prop_pad v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
  in  forAll (choose (0, length xsh)) $ \ k ->
      forAll (vectorOf k ((,) <$> choose (0, 2) <*> choose (0, 2))) $ \ ps ->
      let psh = zipWith (\ (lo, hi) s -> lo + s + hi) ps xsh ++ drop k xsh
          at is = let (os, js) = splitAt k is
                      os' = zipWith (\ i (lo, _) -> i - lo) os ps
                  in  if and (zipWith (\ i s -> i >= 0 && i < s) os' xsh)
                      then unScalar (foldl index x (os' ++ js)) else -1
      in  product psh <= 10000 ==>
          shapeL (pad ps (-1) x) === psh
          .&&. toList (pad ps (-1) x) === [ at is | is <- mapM (\ s -> [0 .. s - 1]) psh ]

-- Each operation of a view has the shape opShape gives, and reads at every
-- index of its result the element of the array it applies to at the index
-- opSource gives.
prop_viewOps :: forall a . Elem a => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOp) (fromList sh (upTo (product sh))) ops :: [Array [] a]
      at x is = unScalar (foldl index x is)
      step (x, op, y) =
        let xsh = shapeL x
            iss = mapM (\ s -> [0 .. s - 1]) (shapeL y)
        in  counterexample (show op)
              (shapeL y === opShape xsh op
               .&&. map (at y) iss === map (at x . opSource xsh op) iss)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- An operation invalid on a view fails once the shape and the elements of
-- its result are forced, with an error of a function opNames names; but
-- broadcast to other extents of the same product gives an array of those,
-- which it should not.
prop_badOps :: forall a . Elem a => View -> Property
prop_badOps v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
  in  forAll (genBadOp xsh) $ \ op ->
      let y = applyOp op x
      in  if silentBadOp xsh op then shapeL y === opShape xsh op
          else failsIn (opNames op) (sum (shapeL y) + fromIntegral (sum (toList y)))

-- The offset, the strides and the length of the vector of an array.
layoutOf :: Array [] a -> (Int, [Int], Int)
layoutOf (DG.A _ t) = (I.offset t, I.strides t, length (I.values t))

-- normalize gives the view as a normal array, its elements in a vector
-- of just their number, at offset 0 and with natural strides; reshape to
-- one dimension, append and concatOuter of the view and a normal array of
-- its shape, zipWithA of the two either way round, and traverseA in the
-- applicative of pairs agree with the lists.
prop_copy :: forall a . Elem a => View -> Property
prop_copy v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
      l = toList x
      n = length l
  in  forAll (genElems (-9, 9) n) $ \ ys ->
      let y = fromList xsh ys
          z = normalize x
      in  toList z === l .&&. layoutOf z === (0, drop 1 (scanr (*) 1 xsh), n)
          .&&. toList (reshape [n] x) === l
          .&&. toList (zipWithA (-) x y) === zipWith (-) l ys
          .&&. toList (zipWithA (-) y x) === zipWith (-) ys l
          .&&. (if null xsh then property True
                else toList (append x y) === l ++ ys
                     .&&. toList (concatOuter [x, y, y]) === l ++ ys ++ ys)
          .&&. traverseA (\ e -> ([e], e - 1)) x === (l, fromList xsh (map (subtract 1) l))

-- zipWith3A, zipWith4A and zipWith5A over the view and normal arrays of
-- its shape, the view first or last, agree with the lists.
prop_zipWith :: forall a . Elem a => View -> Property
prop_zipWith v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
      l = toList x
      ys = genElems (-9, 9) (length l)
  in  forAll ((,,,) <$> ys <*> ys <*> ys <*> ys) $ \ (ys1, ys2, ys3, ys4) ->
      let (y1, y2, y3, y4) = (fromList xsh ys1, fromList xsh ys2, fromList xsh ys3, fromList xsh ys4)
          f3 a b c = a + 10 * b + 100 * c
          f4 a b c d = f3 a b c + 1000 * d
          f5 a b c d e = f4 a b c d + 10000 * e
      in  toList (zipWith3A f3 x y1 y2) === zipWith3 f3 l ys1 ys2
          .&&. toList (zipWith3A f3 y1 y2 x) === zipWith3 f3 ys1 ys2 l
          .&&. toList (zipWith4A f4 x y1 y2 y3) === zipWith4 f4 l ys1 ys2 ys3
          .&&. toList (zipWith4A f4 y1 y2 y3 x) === zipWith4 f4 ys1 ys2 ys3 l
          .&&. toList (zipWith5A f5 x y1 y2 y3 y4) === zipWith5 f5 l ys1 ys2 ys3 ys4
          .&&. toList (zipWith5A f5 y1 y2 y3 y4 x) === zipWith5 f5 ys1 ys2 ys3 ys4 l

-- update agrees with replacing elements of the list, and fails on an
-- index outside the view.  The updates are at distinct indices, the list
-- instance's vUpdate failing on a repeated one where the vector instances
-- keep the last update.
prop_update :: forall a . Elem a => View -> Property
prop_update v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
      l = toList x
      ixs = zip [0 :: Int ..] (mapM (\ s -> [0 .. s - 1]) xsh)
      bad = if null xsh then [0] else xsh
  in  forAll (sublistOf ixs >>= shuffle >>= mapM (\ i -> (,) i . fromIntegral <$> choose (-9, -1 :: Int))) $ \ us ->
      let set ys ((k, _), e) = [ if k' == k then e else y | (k', y) <- zip [0 ..] ys ]
      in  update x [ (is, e) | ((_, is), e) <- us ] === fromList xsh (foldl set l us)
          .&&. failsWith ("update: index out of bounds: " ++ show [bad]) (update x [(bad, 0)])

-- fromVector makes an array of the elements of a list, and fails on a
-- list of another length; iterateN makes one of the first iterates of a
-- function.
prop_fromVector :: forall a . Elem a => Property
prop_fromVector =
  forAll (genShape 3) $ \ sh ->
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  forAll (choose (0, 9)) $ \ n ->
  let n' = length xs
  in  fromVector sh xs === (fromList sh xs :: Array [] a)
      .&&. failsWith ("fromVector: size mismatch " ++ show (n', n' + 1))
                     (fromVector sh (0 : xs) :: Array [] a)
      .&&. iterateN n (* 3) 1 === (fromList [n] (take n (iterate (* 3) 1)) :: Array [] a)

-- An array reads back from its show.
prop_show :: forall a . Elem a => View -> Property
prop_show v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkView v xs :: Array [] a
  in  read (show x) === x

-- rerank applies its function to each subarray below the first n
-- dimensions, rerank2 to each pair of them, unravel lists the subarrays
-- below the first dimension and ravel puts them back.  Where one of those
-- dimensions is empty, each fails with "ravelOuter: empty list", which is
-- to become the model's answer once they find the shape of the result
-- without applying the function.
prop_rerank :: forall a . Elem a => View -> Property
prop_rerank v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array [] a
      xsh = shapeL x
      empty = "ravelOuter: empty list"
      unravelled = case xsh of
        [] -> property True
        0 : _ -> failsWith empty (unravel x :: Array [] (Array [] a))
        s : _ -> map toList (toList (unravel x :: Array [] (Array [] a)))
                 === [ toList (index x i) | i <- [0 .. s - 1] ]
                 .&&. ravel (unravel x :: Array [] (Array [] a)) === x
  in  unravelled .&&. forAll (choose (0, length xsh)) (\ n ->
      let (osh, ish) = splitAt n xsh
          subs = [ toList (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) osh ]
          double a = reshape [product (shapeL a)] (mapA (* 2) a)
      in  if product osh == 0
          then failsWith empty (rerank n double x)
               .&&. failsWith empty (rerank2 n (zipWithA (+)) x x)
          else shapeL (rerank n double x) === osh ++ [product ish]
               .&&. toList (rerank n double x) === concatMap (map (* 2)) subs
               .&&. toList (rerank2 n (zipWithA (+)) x x) === map (* 2) (toList x))
