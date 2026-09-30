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

-- The properties over random views of the dynamic test modules, at the
-- list instance of Vector, which runs the generic code with the lists' own
-- methods.
module DynamicGTest(test) where

import Data.Array.DynamicG
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  ( Property, choose, conjoin, counterexample, elements, forAll, property
  , vectorOf, (.&&.), (===), (==>) )
import Views (Op (..), View (..), opShape, opSource, testPropertyN)

test :: Test
test = testGroup "DynamicG"
  [ testPropertyN "prop_allSameA" prop_allSameA
  , testPropertyN "prop_toList" prop_toList
  , testPropertyN "prop_compare" prop_compare
  , testPropertyN "prop_reduce" prop_reduce
  , testPropertyN "prop_pad" prop_pad
  , testPropertyN "prop_viewOps" prop_viewOps
  , testPropertyN "prop_copy" prop_copy
  , testPropertyN "prop_show" prop_show
  ]

-- applyOp and mkView of Views, over arrays of lists.
applyOp :: Op -> Array [] a -> Array [] a
applyOp (Transpose is) = transpose is
applyOp (Rev rs) = rev rs
applyOp (Slice sl) = slice sl
applyOp (Stride ts) = stride ts
applyOp (Window ws) = window ws
applyOp (Index i) = (`index` i)
applyOp (Broadcast ds sh) = broadcast ds sh

mkView :: View -> [a] -> Array [] a
mkView (View sh ops) xs = foldl (flip applyOp) (fromList sh xs) ops

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1], [1, 1, 1, 2 :: Double]]) $ \ pool ->
  forAll (vectorOf (product sh) (elements pool)) $ \ xs ->
  let x = mkView v xs
  in  allSameA x === I.allSame (toList x)

-- toList and toVector agree with indexing the view element by element.
prop_toList :: View -> Property
prop_toList v@(View sh _) =
  let x = mkView v [0 .. product sh - 1] :: Array [] Int
      l = [ unScalar (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) (shapeL x) ]
  in  toList x === l .&&. toVector x === l

-- == and compare agree with comparing the lists, between a view and an
-- array of its elements with at most one of them changed, and between two
-- views of one layout over vectors that differ in at most one element,
-- inside the views or outside them.
prop_compare :: View -> Property
prop_compare v@(View sh _) =
  let n = product sh
      x = mkView v [0 .. n - 1] :: Array [] Int
      l = toList x
  in  forAll (choose (0, length l)) $ \ i ->
      forAll (choose (0, n)) $ \ j ->
      forAll (choose (-1, 1)) $ \ d ->
      let l' = [ if k == i then e + d else e | (k, e) <- zip [0 ..] l ]
          y = fromList (shapeL x) l'
          z = mkView v [ if k == j then k + d else k | k <- [0 .. n - 1] ]
      in  (x == y) === (l == l') .&&. compare x y === compare l l'
          .&&. compare y x === compare l' l
          .&&. (x == z) === (l == toList z) .&&. compare x z === compare l (toList z)

-- The reductions agree with the list's: reduce, sumA, productA, maximumA,
-- minimumA, anyA and allA.
prop_reduce :: View -> Property
prop_reduce v@(View sh _) =
  forAll (vectorOf (product sh) (choose (1, 9))) $ \ xs ->
  forAll (choose (0, 9)) $ \ t ->
  let x = mkView v xs :: Array [] Int
      l = toList x
  in  reduce (+) 0 x === scalar (sum l)
      .&&. sumA x === sum l .&&. productA x === product l
      .&&. anyA (> t) x === any (> t) l .&&. allA (> t) x === all (> t) l
      .&&. (if null l then property True
            else maximumA x === maximum l .&&. minimumA x === minimum l)

-- pad agrees with indexing the view where an index falls inside it, and
-- gives the padding value elsewhere, for a pad list of any length up to
-- the rank that leaves at most 10000 elements.
prop_pad :: View -> Property
prop_pad v@(View sh _) =
  let x = mkView v [0 .. product sh - 1] :: Array [] Int
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
prop_viewOps :: View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOp) (fromList sh [0 .. product sh - 1]) ops :: [Array [] Int]
      at x is = unScalar (foldl index x is)
      step (x, op, y) =
        let xsh = shapeL x
            iss = mapM (\ s -> [0 .. s - 1]) (shapeL y)
        in  counterexample (show op)
              (shapeL y === opShape xsh op
               .&&. map (at y) iss === map (at x . opSource xsh op) iss)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- The offset, the strides and the length of the vector of an array.
layoutOf :: Array [] a -> (Int, [Int], Int)
layoutOf (DG.A _ t) = (I.offset t, I.strides t, length (I.values t))

-- normalize gives the view as a normal array, its elements in a vector
-- of just their number, at offset 0 and with natural strides; reshape to
-- one dimension, append of the view and a normal array of its shape, and
-- zipWithA of the two either way round agree with the lists.
prop_copy :: View -> Property
prop_copy v@(View sh _) =
  let x = mkView v [0 .. product sh - 1] :: Array [] Int
      xsh = shapeL x
      l = toList x
      n = length l
  in  forAll (vectorOf n (choose (-9, 9))) $ \ ys ->
      let y = fromList xsh ys
          z = normalize x
      in  toList z === l .&&. layoutOf z === (0, drop 1 (scanr (*) 1 xsh), n)
          .&&. toList (reshape [n] x) === l
          .&&. toList (zipWithA (-) x y) === zipWith (-) l ys
          .&&. toList (zipWithA (-) y x) === zipWith (-) ys l
          .&&. (if null xsh then property True else toList (append x y) === l ++ ys)

-- An array reads back from its show.
prop_show :: View -> Property
prop_show v@(View sh _) =
  forAll (vectorOf (product sh) (choose (-9, 9))) $ \ xs ->
  let x = mkView v xs :: Array [] Int
  in  read (show x) === x
