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
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
-- The properties of Dynamic arrays, through DynamicG at the boxed,
-- Storable, Unboxed and list instances of Vector: over random views, but
-- for prop_fromVector and prop_rotate, and with Int and Word8 elements,
-- but for prop_allSameA, whose elements are Doubles.  The list instance
-- runs the generic code with the lists' own methods.
module DynamicGTest(test) where

import Data.Array.DynamicG
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.Array.Internal.DynamicS ()
import Data.Array.Internal.DynamicU ()
import Data.List (sort, zipWith4, zipWith5)
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import Data.Word (Word8)
import Foreign.Storable (Storable)
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  ( Arbitrary (..), Property, choose, conjoin, counterexample, elements, forAll, listOf, property
  , shrinkList, vectorOf, (.&&.), (===), (==>) )
import Views
  ( Elem, Owns (..), View (..), applyOpG, failsIn, failsWith, genBadOp, genElems, genOps
  , genShape, mkViewG, opName, opShape, opSource, testPropertyN, upTo )

test :: Test
test = testGroup "DynamicG" $ backends @Int True ++ [testGroup "Word8" (backends @Word8 False)]

-- The properties at each instance of Vector, with elements of an Elem type,
-- and allSameA's, whose elements are Doubles, where asked.
backends :: forall a . (Elem a, Storable a, VU.Unbox a, Owns (VU.Vector a)) =>
            Bool -> [Test]
backends nan =
  [ backend @V.Vector @a nan "boxed"
  , backend @VS.Vector @a nan "Storable"
  , backend @VU.Vector @a nan "Unboxed"
  , backend @[] @a nan "list"
  ]

backend :: forall v a . ( I.Vector v, I.VecElem v a, I.VecElem v Double, Elem a
                        , Owns (v a) ) =>
           Bool -> String -> Test
backend nan n = testGroup n $
  [ testPropertyN "prop_allSameA" (prop_allSameA @v) | nan ] ++
  [ testPropertyN "prop_toList" (prop_toList @v @a)
  , testPropertyN "prop_compare" (prop_compare @v @a)
  , testPropertyN "prop_reduce" (prop_reduce @v @a)
  , testPropertyN "prop_pad" (prop_pad @v @a)
  , testPropertyN "prop_viewOps" (prop_viewOps @v @a)
  , testPropertyN "prop_mapAViews" (prop_mapAViews @v @a)
  , testPropertyN "prop_badOps" (prop_badOps @v @a)
  , testPropertyN "prop_copy" (prop_copy @v @a)
  , testPropertyN "prop_zipWith" (prop_zipWith @v @a)
  , testPropertyN "prop_update" (prop_update @v @a)
  , testPropertyN "prop_fromVector" (prop_fromVector @v @a)
  , testPropertyN "prop_show" (prop_show @v @a)
  , testPropertyN "prop_rerank" (prop_rerank @v @a)
  , testPropertyN "prop_ravel" (prop_ravel @v @a)
  , testPropertyN "prop_rotate" (prop_rotate @v @a)
  ]

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: forall v . (I.Vector v, I.VecElem v Double) => View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1], [1, 1, 1, 2 :: Double]]) $ \ pool ->
  forAll (vectorOf (product sh) (elements pool)) $ \ xs ->
  let x = mkViewG v xs :: Array v Double
  in  allSameA x === I.allSame (toList x)

-- Every index of the shape, in order.
indices :: [Int] -> [[Int]]
indices sh = mapM (\ s -> [0 .. s - 1]) sh

-- The element of the array at the index.
at :: (I.Vector v, I.VecElem v a) => Array v a -> [Int] -> a
at x is = unScalar (foldl (\ a i -> index a i) x is)

-- The array laid out in the reverse order of its dimensions.
reversedLayout :: (I.Vector v, I.VecElem v a) => Array v a -> Array v a
reversedLayout x =
  transpose rv (fromList (reverse (shapeL x)) (toList (transpose rv x)))
  where rv = reverse [0 .. length (shapeL x) - 1]

-- toList and toVector agree with indexing the view element by element.
prop_toList :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_toList v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      l = map (at x) (indices (shapeL x))
  in  toList x === l .&&. I.vToList (toVector x) === l

-- == and compare agree with comparing the lists, between a view and an array of
-- its elements with at most one of them changed, laid out in order or in the
-- reverse order of its dimensions, and between two views of one layout over
-- vectors that differ in at most one element, inside the views or outside them.
prop_compare :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
                View -> Property
prop_compare v@(View sh _) =
  let n = product sh
      x = mkViewG v (upTo n) :: Array v a
      l = toList x
  in  forAll (choose (0, length l)) $ \ i ->
      forAll (choose (0, n)) $ \ j ->
      forAll (choose (-1, 1)) $ \ d ->
      forAll (choose (1, 3)) $ \ m ->
      let l' = [ if k == i then e + fromIntegral d else e | (k, e) <- zip [0 ..] l ]
          y = fromList (shapeL x) l'
          -- y laid out in the reverse order of its dimensions, which no slice
          -- reads where two of them exceed one
          yt = reversedLayout y
          z = mkViewG v [ fromIntegral (if k == j then k + d else k) | k <- [0 .. n - 1] ]
          -- z with its strides, at an offset m further into a longer vector
          w = case z of
            DG.A zsh (I.T zss o zv) | I.vLength zv > 0 ->
              DG.A zsh (I.T zss (o + m) (I.vAppend (I.vReplicate m 0) zv))
            _ -> z
      in  (x == y) === (l == l') .&&. compare x y === compare l l'
          .&&. compare y x === compare l' l
          .&&. (x == yt) === (l == l') .&&. compare x yt === compare l l'
          .&&. compare yt x === compare l' l
          .&&. (x == z) === (l == toList z) .&&. compare x z === compare l (toList z)
          .&&. (x == w) === (l == toList w) .&&. compare x w === compare l (toList w)

-- The reductions agree with the list's: reduce, sumA, productA, maximumA,
-- minimumA, anyA and allA; and the vector toUnorderedVectorT gives holds
-- the list's elements in some order.
prop_reduce :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_reduce v@(View sh _) =
  forAll (genElems (1, 9) (product sh)) $ \ xs ->
  forAll (fromIntegral <$> choose (0, 9 :: Int)) $ \ t ->
  let x = mkViewG v xs :: Array v a
      l = toList x
      DG.A xsh tx = x
  in  reduce (+) 0 x === scalar (sum l)
      .&&. sumA x === sum l .&&. productA x === product l
      .&&. anyA (> t) x === any (> t) l .&&. allA (> t) x === all (> t) l
      .&&. (if null l then property True
            else maximumA x === maximum l .&&. minimumA x === minimum l)
      .&&. sort (I.vToList (I.toUnorderedVectorT xsh tx)) === sort l

-- pad agrees with indexing the view where an index falls inside it, and gives
-- the padding value elsewhere, for a pad list of any length up to the rank that
-- leaves at most 10000 elements; and padT, given a pad list of zeros of that
-- length, returns the view's own layout and shares its vector where a slice of
-- the vector does.
prop_pad :: forall v a . (Owns (v a), I.Vector v, I.VecElem v a, Elem a) =>
            View -> Property
prop_pad v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      DG.A _ t = x
      w = I.values t
  in  forAll (choose (0, length xsh)) $ \ k ->
      forAll (vectorOf k ((,) <$> choose (0, 2) <*> choose (0, 2))) $ \ ps ->
      let psh = zipWith (\ (lo, hi) s -> lo + s + hi) ps xsh ++ drop k xsh
          elemAt is = let (os, js) = splitAt k is
                          os' = zipWith (\ i (lo, _) -> i - lo) os ps
                      in  if and (zipWith (\ i s -> i >= 0 && i < s) os' xsh)
                          then at x (os' ++ js) else -1
          t' = I.padT (-1) (map (const (0, 0)) ps) xsh t
      in  product psh <= 10000 ==>
          shapeL (pad ps (-1) x) === psh
          .&&. toList (pad ps (-1) x) === map elemAt (indices psh)
          .&&. (I.offset t', I.strides t') === (I.offset t, I.strides t)
          .&&. sameStorage (I.values t') w
               === sameStorage (I.vSlice 0 (I.vLength w) w) w

-- Each operation of a view has the shape opShape gives, and reads at every
-- index of its result the element of the array it applies to at the index
-- opSource gives.  For an Index op the two reads are one expression, so that
-- step checks the shape alone; prop_toList checks index against toList.
prop_viewOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOpG) (fromList sh (upTo (product sh))) ops :: [Array v a]
      step (x, op, y) =
        let xsh = shapeL x
            iss = indices (shapeL y)
        in  counterexample (show op)
              (shapeL y === opShape xsh op
               .&&. map (at y) iss === map (at x . opSource xsh op) iss)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- mapA id of a view keeps its strides over a copy of the part of the vector
-- it reads, a layout no random view starts from; under further operations it
-- gives what the view gives: its elements, its vector, its sum and normalize.
prop_mapAViews :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_mapAViews v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
  in  forAll (choose (0, 3) >>= \ n -> genOps n (shapeL x)) $ \ ops ->
      let y = foldl (flip applyOpG) x ops
          z = foldl (flip applyOpG) (mapA id x) ops
          l = toList y
      in  toList z === l .&&. I.vToList (toVector z) === l
          .&&. sumA z === sum l .&&. toList (normalize z) === l

-- An operation invalid on a view fails as soon as its result is evaluated,
-- with an error of the function opName names.
prop_badOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_badOps v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
  in  forAll (genBadOp xsh) $ \ op ->
      failsIn (opName op) (applyOpG op x)

-- The offset, the strides and the length of the vector of an array.
layoutOf :: (I.Vector v, I.VecElem v a) => Array v a -> (Int, [Int], Int)
layoutOf (DG.A _ t) = (I.offset t, I.strides t, I.vLength (I.values t))

valuesOf :: Array v a -> v a
valuesOf (DG.A _ t) = I.values t

-- normalize gives the view as a normal array, its elements in a vector of just
-- their number, at offset 0 and with natural strides, and force the same in
-- storage of its own; normalize of a row of a normal array shares its vector
-- where a slice of the vector does, and force of the row does not; reshape to
-- one dimension, append and concatOuter of the view and a normal array of its
-- shape, zipWithA of the two either way round, and traverseA in the applicative
-- of pairs agree with the lists; concatOuter of the view alone, a concatenation
-- of one part, is the view; and append and concatOuter fail on scalars.
prop_copy :: forall v a . (Owns (v a), I.Vector v, I.VecElem v a, Elem a) =>
             View -> Property
prop_copy v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      l = toList x
      n = length l
  in  forAll (genElems (-9, 9) n) $ \ ys ->
      let y = fromList xsh ys
          z = normalize x
      in  toList z === l .&&. layoutOf z === (0, drop 1 (scanr (*) 1 xsh), n)
          .&&. toList (force x) === l
          .&&. counterexample "force keeps a larger vector" (ownsStorage (valuesOf (force x)))
          .&&. (case xsh of
                  s : _ | n > 0 ->
                    let r = index y 0
                        w = valuesOf y
                    in  sameStorage (valuesOf (normalize r)) w
                          === sameStorage (I.vSlice 0 (n `quot` s) w) w
                        .&&. counterexample "force of a row shares its vector"
                               (not (sameStorage (valuesOf (force r)) w))
                  _ -> property True)
          .&&. toList (reshape [n] x) === l
          .&&. toList (zipWithA (-) x y) === zipWith (-) l ys
          .&&. toList (zipWithA (-) y x) === zipWith (-) ys l
          .&&. (if null xsh
                then failsWith "append: bad shape" (append x y)
                     .&&. failsWith "concatOuter: rank 0 array" (concatOuter [x, y, y])
                else toList (append x y) === l ++ ys
                     .&&. toList (concatOuter [x, y, y]) === l ++ ys ++ ys
                     .&&. concatOuter [x] === x)
          .&&. traverseA (\ e -> ([e], e - 1)) x === (l, fromList xsh (map (subtract 1) l))

-- zipWith3A, zipWith4A and zipWith5A over the view and normal arrays of
-- its shape, the view first or last, agree with the lists.
prop_zipWith :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_zipWith v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
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

-- update agrees with replacing elements of the list, the last update at
-- an index being the one that stays, and fails on an index outside the
-- view.
prop_update :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_update v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      l = toList x
      ixs = zip [0 :: Int ..] (indices xsh)
      bad = if null xsh then [0] else xsh
  in  forAll (if null l then return [] else listOf ((,) <$> elements ixs <*> (fromIntegral <$> choose (-9, -1 :: Int)))) $ \ us ->
      let set ys ((k, _), e) = [ if k' == k then e else y | (k', y) <- zip [0 ..] ys ]
      in  update x [ (is, e) | ((_, is), e) <- us ] === fromList xsh (foldl set l us)
          .&&. failsWith ("update: index out of bounds: " ++ show [bad]) (update x [(bad, 0)])

-- fromVector makes an array of the elements of a vector, here a slice of
-- a longer one, and fails on a vector of another length; iterateN makes
-- one of the first iterates of a function.
prop_fromVector :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
                   Property
prop_fromVector =
  forAll (genShape 3) $ \ sh ->
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  forAll (choose (0, 3)) $ \ k ->
  forAll (choose (0, 3)) $ \ m ->
  forAll (choose (0, 9)) $ \ n ->
  let n' = length xs
      vec = I.vSlice k n' (I.vFromList (replicate k 99 ++ xs ++ replicate m 99))
  in  fromVector sh vec === (fromList sh xs :: Array v a)
      .&&. failsWith ("fromVector: size mismatch " ++ show (n', n' + 1))
                     (fromVector sh (I.vFromList (0 : xs)) :: Array v a)
      .&&. iterateN n (* 3) 1 === (fromList [n] (take n (iterate (* 3) 1)) :: Array v a)

-- An array reads back from its show.
prop_show :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
             View -> Property
prop_show v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkViewG v xs :: Array v a
  in  read (show x) === x

-- rerank applies its function to each subarray below the first n dimensions,
-- rerank2 to each pair of them, of the array with itself and with three times
-- it laid out in the reverse order of its dimensions, unravel lists the
-- subarrays below the first dimension and ravel puts them back.  Where one
-- of those dimensions is empty, unravel gives an empty array, and rerank and
-- rerank2 fail, having no result of the function to take a shape from.
prop_rerank :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_rerank v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      unravelled = case xsh of
        [] -> property True
        0 : _ -> shapeL (unravel x :: Array V.Vector (Array v a)) === [0]
        s : _ -> map (\ a -> toList a) (toList (unravel x :: Array V.Vector (Array v a)))
                 === [ toList (index x i) | i <- [0 .. s - 1] ]
                 .&&. ravel (unravel x :: Array V.Vector (Array v a)) === x
  in  unravelled .&&. forAll (choose (0, length xsh)) (\ n ->
      let (osh, ish) = splitAt n xsh
          subs = [ toList (foldl (\ a i -> index a i) x is) | is <- indices osh ]
          double a = reshape [product (shapeL a)] (mapA (* 2) a)
          -- three times x, laid out in the reverse order of its dimensions
          y = reversedLayout (mapA (* 3) x)
      in  if product osh == 0
          then failsWith "ravelOuter: empty outer dimension" (rerank n double x)
               .&&. failsWith "ravelOuter: empty outer dimension" (rerank2 n (\ a b -> zipWithA (+) a b) x x)
          else shapeL (rerank n double x) === osh ++ [product ish]
               .&&. toList (rerank n double x) === concatMap (map (* 2)) subs
               .&&. toList (rerank2 n (\ a b -> zipWithA (+) a b) x x) === map (* 2) (toList x)
               .&&. toList (rerank2 n (\ a b -> zipWithA (-) a b) x y) === map (* (-2)) (toList x)
               .&&. toList (rerank2 n (\ a b -> zipWithA (-) a b) y x) === map (* 2) (toList x))

-- ravel fails on an outer array of none, and on arrays of differing shapes,
-- naming the first one's shape and the first that differs.
prop_ravel :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_ravel v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      y = reshape [product (shapeL x), 1] x
      msg = "ravelOuterOf: non-conforming inner dimensions: " ++ show [shapeL x, shapeL y]
  in  failsWith "ravel: empty array" (ravel (fromList [0] [] :: Array V.Vector (Array v a)))
      .&&. (if shapeL x == shapeL y then property True
            else failsWith msg (ravel (fromList [3] [x, x, y] :: Array V.Vector (Array v a))))

-- A call of rotate on an array of shape osh ++ h : t, rotating it k times
-- along dimension length osh.
data RotateCase = RotateCase [Int] Int [Int] Int
  deriving Show

instance Arbitrary RotateCase where
  arbitrary = RotateCase <$> genShape 2 <*> choose (0, 4) <*> genShape 2 <*> choose (0, 12)
  shrink (RotateCase osh h t k) =
    [ RotateCase osh' h t k | osh' <- shrinkList shrinkExtent osh ] ++
    [ RotateCase osh h' t k | h' <- shrinkExtent h ] ++
    [ RotateCase osh h t' k | t' <- shrinkList shrinkExtent t ] ++
    [ RotateCase osh h t k' | k' <- shrinkExtent k ]

shrinkExtent :: Int -> [Int]
shrinkExtent = filter (>= 0) . shrink

-- rotate against a list model: the i'th of the k rotations of a subarray
-- is the subarray rotated left by k-1-i rows.  An array whose elements,
-- 1 to n, the type cannot hold, past 255 in Word8, is discarded, as
-- repeated elements could hide a misplaced one.
prop_rotate :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               RotateCase -> Property
prop_rotate (RotateCase osh h t k) =
  let m = product t
      n = product (osh ++ h : t)
      xs = map fromIntegral [1 .. n] :: [a]
      rows ys = [ take m (drop (i * m) ys) | i <- [0 .. h - 1] ]
      rotL j rs = let j' = j `mod` max 1 h in drop j' rs ++ take j' rs
      rot ys = concat [ concat (rotL (k - 1 - i) (rows ys)) | i <- [0 .. k - 1] ]
      subs = [ take (h * m) (drop (j * h * m) xs) | j <- [0 .. product osh - 1] ]
  in  map toInteger xs == [1 .. toInteger n] ==>
      rotate (length osh) k (fromList (osh ++ h : t) xs :: Array v a)
      === fromList (osh ++ k : h : t) (concatMap rot subs)
