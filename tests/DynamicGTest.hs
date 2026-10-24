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
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
-- The properties of Dynamic arrays, through DynamicG at the boxed, Storable,
-- Unboxed and list instances of Vector: over random views, but for
-- prop_fromVector, prop_rotate and prop_vZipWith, which zips the instances'
-- vectors, and with Int and Word8 elements, but for prop_allSameA, whose
-- elements are Doubles.  The list instance runs the generic code with the
-- lists' own methods.
module DynamicGTest(test) where

import Control.DeepSeq (deepseq)
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
  ( Arbitrary (..), Gen, Property, checkCoverage, choose, conjoin
  , counterexample, cover, elements, forAll, listOf
  , property, shrinkList, vectorOf, (.&&.), (===), (==>) )
import Views
  ( Elem, Owns (..), View (..), adjustAt, applyOpG, failsIn, failsWith
  , forAllView
  , genBadOp, genElems, genOps, genShape, mkViewG, mkViewUpTo, opName, opShape
  , opSource, testPropertyN, upTo, valuesG )

test :: Test
test = testGroup "DynamicG" $
  backends @Int True ++ [testGroup "Word8" (backends @Word8 False)]

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
  , testPropertyN "prop_share" (prop_share @v @a)
  , testPropertyN "prop_zipWith" (prop_zipWith @v @a)
  , testPropertyN "prop_inView" (prop_inView @v @a)
  , testPropertyN "prop_update" (prop_update @v @a)
  , testPropertyN "prop_fromVector" (prop_fromVector @v @a)
  , testPropertyN "prop_show" (prop_show @v @a)
  , testPropertyN "prop_rerank" (prop_rerank @v @a)
  , testPropertyN "prop_ravel" (prop_ravel @v @a)
  , testPropertyN "prop_rotate" (prop_rotate @v @a)
  , testPropertyN "prop_vZipWith" (prop_vZipWith @v @a)
  , testPropertyN "prop_arbitrary" (prop_arbitrary @v @a)
  ]

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: forall v . (I.Vector v, I.VecElem v Double) => View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1],
                    [1, 1, 1, 2 :: Double]]) $ \ pool ->
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
prop_toList :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_toList v =
  let x = mkViewUpTo v :: Array v a
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
      let l' = adjustAt i (+ fromIntegral d) l
          y = fromList (shapeL x) l'
          -- y laid out in the reverse order of its dimensions, which no slice
          -- reads where two of them exceed one
          yt = reversedLayout y
          z = mkViewG v [ fromIntegral (if k == j then k + d else k)
                        | k <- [0 .. n - 1] ]
          -- z with its strides, at an offset m further into a longer vector
          w = case z of
            DG.A zsh (I.T zss o zv) | I.vLength zv > 0 ->
              DG.A zsh (I.T zss (o + m) (I.vAppend (I.vReplicate m 0) zv))
            _ -> z
          lz = toList z
          lw = toList w
      in  (x == y) === (l == l') .&&. compare x y === compare l l'
          .&&. compare y x === compare l' l
          .&&. (x == yt) === (l == l') .&&. compare x yt === compare l l'
          .&&. compare yt x === compare l' l
          .&&. (x == z) === (l == lz) .&&. compare x z === compare l lz
          .&&. (x == w) === (l == lw) .&&. compare x w === compare l lw

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
prop_pad v =
  let x = mkViewUpTo v :: Array v a
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
          p = pad ps (-1) x
      in  product psh <= 10000 ==>
          shapeL p === psh
          .&&. toList p === map elemAt (indices psh)
          .&&. (I.offset t', I.strides t') === (I.offset t, I.strides t)
          .&&. sameStorage (I.values t') w
               === sameStorage (I.vSlice 0 (I.vLength w) w) w

-- Each operation of a view has the shape opShape gives, and reads at every
-- index of its result the element of the array it applies to at the index
-- opSource gives.  For an Index op the two reads are one expression, so that
-- step checks the shape alone; prop_toList checks index against toList.
prop_viewOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
                View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOpG) (fromList sh (upTo (product sh))) ops
        :: [Array v a]
      step (x, op, y) =
        let xsh = shapeL x
            iss = indices (shapeL y)
        in  counterexample (show op)
              (shapeL y === opShape xsh op
               .&&. map (at y) iss === map (at x . opSource xsh op) iss)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

-- mapA id of a view that reads every element of one part of its vector keeps
-- its strides over a copy of that part, a layout no random view starts from;
-- and mapA id of any view, under further operations, gives what the view gives:
-- its elements, its vector, its sum and normalize.
prop_mapAViews :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
                  View -> Property
prop_mapAViews v =
  let x@(DG.A xsh tx) = mkViewUpTo v :: Array v a
      (_, ssx, _) = layoutOf x
      (_, ssm, _) = layoutOf (mapA id x)
      kept = case I.readRangeT xsh tx of
        I.Range _ _ -> ssm === ssx
        _ -> property True
  in  kept .&&. forAll (choose (0, 3) >>= \ n -> genOps n (shapeL x)) (\ ops ->
      let y = foldl (flip applyOpG) x ops
          z = foldl (flip applyOpG) (mapA id x) ops
          l = toList y
      in  toList z === l .&&. I.vToList (toVector z) === l
          .&&. sumA z === sum l .&&. toList (normalize z) === l)

-- An operation invalid on a view fails as soon as its result is evaluated,
-- with an error of the function opName names.
prop_badOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_badOps v =
  let x = mkViewUpTo v :: Array v a
      xsh = shapeL x
  in  forAll (genBadOp xsh) $ \ op ->
      failsIn (opName op) (applyOpG op x)

-- The offset, the strides and the length of the vector of an array.
layoutOf :: (I.Vector v, I.VecElem v a) => Array v a -> (Int, [Int], Int)
layoutOf (DG.A _ t) = (I.offset t, I.strides t, I.vLength (I.values t))

-- normalize gives the view as a normal array, its elements in a vector of just
-- their number, at offset 0 and with natural strides, and force the same in
-- storage of its own; reshape to one dimension, append and concatOuter of the
-- view and a normal array of its shape and of the view and itself, zipWithA of
-- the two either way round, and traverseA in the applicative of pairs agree
-- with the lists; concatOuter of the view alone, a concatenation of one part,
-- is the view; and append and concatOuter fail on scalars.
prop_copy :: forall v a . (Owns (v a), I.Vector v, I.VecElem v a, Elem a) =>
             View -> Property
prop_copy v =
  let x = mkViewUpTo v :: Array v a
      xsh = shapeL x
      l = toList x
      n = length l
  in  forAll (genElems (-9, 9) n) $ \ ys ->
      let y = fromList xsh ys
          z = normalize x
          fx = force x
      in  toList z === l .&&. layoutOf z === (0, drop 1 (scanr (*) 1 xsh), n)
          .&&. toList fx === l
          .&&. counterexample "force keeps a larger vector"
                              (ownsStorage (valuesG fx))
          .&&. toList (reshape [n] x) === l
          .&&. toList (zipWithA (-) x y) === zipWith (-) l ys
          .&&. toList (zipWithA (-) y x) === zipWith (-) ys l
          .&&. (if null xsh
                then failsWith ("append: bad shape " ++ show (xsh, shapeL y))
                               (append x y)
                     .&&. failsWith ("concatOuter: rank 0 array "
                                     ++ show [xsh, shapeL y, shapeL y])
                                    (concatOuter [x, y, y])
                else toList (append x y) === l ++ ys
                     .&&. toList (concatOuter [x, y, y]) === l ++ ys ++ ys
                     .&&. toList (append x x) === l ++ l
                     .&&. toList (concatOuter [x, x]) === l ++ l
                     .&&. concatOuter [x] === x)
          .&&. traverseA (\ e -> ([e], e - 1)) x
               === (l, fromList xsh (map (subtract 1) l))

-- toVector and normalize of a non-empty view share its vector exactly where its
-- elements lie one after another in order in it, whatever the strides of its
-- dimensions of extent 1, and a slice of the vector shares it, as one of a list
-- does not; force never shares it.
prop_share :: forall v a . (Owns (v a), I.Vector v, I.VecElem v a, Elem a) =>
              View -> Property
prop_share v =
  let x = mkViewUpTo v :: Array v a
      (o, _, len) = layoutOf x
      w = valuesG x
      l = toList x
      n = length l
      part = I.vSlice o n w
      shared = o + n <= len && I.vToList part == l && sameStorage part w
  in  n > 0 ==>
      sameStorage (toVector x) w === shared
      .&&. sameStorage (valuesG (normalize x)) w === shared
      .&&. counterexample "force shares its vector"
             (not (sameStorage (valuesG (force x)) w))

-- zipWith3A, zipWith4A and zipWith5A over the view and normal arrays of
-- its shape, the view first or last, agree with the lists.
prop_zipWith :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
                View -> Property
prop_zipWith v =
  let x = mkViewUpTo v :: Array v a
      xsh = shapeL x
      l = toList x
      ys = genElems (-9, 9) (length l)
  in  forAll ((,,,) <$> ys <*> ys <*> ys <*> ys) $ \ (ys1, ys2, ys3, ys4) ->
      let (y1, y2, y3, y4) = (fromList xsh ys1, fromList xsh ys2,
                              fromList xsh ys3, fromList xsh ys4)
          f3 a b c = a + 10 * b + 100 * c
          f4 a b c d = f3 a b c + 1000 * d
          f5 a b c d e = f4 a b c d + 10000 * e
      in  toList (zipWith3A f3 x y1 y2) === zipWith3 f3 l ys1 ys2
          .&&. toList (zipWith3A f3 y1 y2 x) === zipWith3 f3 ys1 ys2 l
          .&&. toList (zipWith4A f4 x y1 y2 y3) === zipWith4 f4 l ys1 ys2 ys3
          .&&. toList (zipWith4A f4 y1 y2 y3 x) === zipWith4 f4 ys1 ys2 ys3 l
          .&&. toList (zipWith5A f5 x y1 y2 y3 y4)
               === zipWith5 f5 l ys1 ys2 ys3 ys4
          .&&. toList (zipWith5A f5 y1 y2 y3 y4 x)
               === zipWith5 f5 ys1 ys2 ys3 ys4 l

-- mapA, zipWithA and zipWith3A apply their function to the elements the view
-- reads and to no other element of its vector, the whole vector of each
-- result forced.
prop_inView :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_inView v =
  let x = mkViewUpTo v :: Array v a
      l = toList x
      y = fromList (shapeL x) l
      g e | e `elem` l = e
          | otherwise = error ("applied outside the view to " ++ show e)
      forced r = I.vToList (valuesG r) `deepseq` toList r
  in  forced (mapA g x) === l
      .&&. forced (zipWithA (\ e _ -> g e) x y) === l
      .&&. forced (zipWithA (\ _ e -> g e) y x) === l
      .&&. forced (zipWith3A (\ e _ _ -> g e) x y y) === l

-- update agrees with replacing elements of the list, the last update at an
-- index being the one that stays, leaves the array it updates as it was, and
-- fails on an index outside the view: every component out of bounds, the first
-- below 0, the last at its extent, or a component too many.
prop_update :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_update v =
  let x = mkViewUpTo v :: Array v a
      xsh = shapeL x
      l = toList x
      ixs = zip [0 :: Int ..] (indices xsh)
      bad = if null xsh then [0] else xsh
      zeros = map (const 0) xsh
      bads = bad : (zeros ++ [0])
             : [ (-1) : drop 1 zeros | not (null xsh) ]
             ++ [ [ if k == length xsh - 1 then s else 0
                  | (k, s) <- zip [0 ..] xsh ]
                | not (null xsh) ]
  in  forAll (if null l then return []
              else listOf ((,) <$> elements ixs
                               <*> (fromIntegral <$> choose (-9, -1 :: Int))))
      $ \ us ->
      let set ys ((k, _), e) = adjustAt k (const e) ys
      in  l `deepseq` update x [ (is, e) | ((_, is), e) <- us ]
            === fromList xsh (foldl set l us)
          -- x read again, by index, once the update is evaluated
          .&&. map (at x) (indices xsh) === l
          .&&. conjoin [ failsWith ("update: index out of bounds: "
                                    ++ show ([b], xsh))
                                   (update x [(b, 0)])
                       | b <- bads ]

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
      .&&. failsWith ("fromVector: size mismatch " ++ show (sh, n' + 1))
                     (fromVector sh (I.vFromList (0 : xs)) :: Array v a)
      .&&. iterateN n (* 3) 1
           === (fromList [n] (take n (iterate (* 3) 1)) :: Array v a)

-- An array reads back from its show.
prop_show :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
             View -> Property
prop_show v = forAllView v $ \ (x :: Array v a) -> read (show x) === x

-- rerank applies its function to each subarray below the first n dimensions,
-- rerank2 to each pair of them, of the array with itself and with three times
-- it laid out in the reverse order of its dimensions, unravel lists the
-- subarrays below the first dimension and ravel puts them back.  Where one
-- of those dimensions is empty, unravel gives an empty array, and rerank and
-- rerank2 fail, having no result of the function to take a shape from.
prop_rerank :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
               View -> Property
prop_rerank v =
  let x = mkViewUpTo v :: Array v a
      xsh = shapeL x
      u = unravel x :: Array V.Vector (Array v a)
      unravelled = case xsh of
        [] -> property True
        0 : _ -> shapeL u === [0]
        s : _ -> map (\ a -> toList a) (toList u)
                 === [ toList (index x i) | i <- [0 .. s - 1] ]
                 .&&. ravel u === x
  in  unravelled .&&. forAll (choose (0, length xsh)) (\ n ->
      let (osh, ish) = splitAt n xsh
          double a = reshape [product (shapeL a)] (mapA (* 2) a)
          -- three times x, laid out in the reverse order of its dimensions
          y = reversedLayout (mapA (* 3) x)
      in  if product osh == 0
          then failsWith ("rerank: empty outer dimension " ++ show osh)
                         (rerank n double x)
               .&&. failsWith ("rerank2: empty outer dimension " ++ show osh)
                              (rerank2 n (\ a b -> zipWithA (+) a b) x x)
          else shapeL (rerank n double x) === osh ++ [product ish]
               .&&. toList (rerank n double x) === map (* 2) (toList x)
               .&&. toList (rerank2 n (\ a b -> zipWithA (+) a b) x x)
                    === map (* 2) (toList x)
               .&&. toList (rerank2 n (\ a b -> zipWithA (-) a b) x y)
                    === map (* (-2)) (toList x)
               .&&. toList (rerank2 n (\ a b -> zipWithA (-) a b) y x)
                    === map (* 2) (toList x))

-- ravel fails on an outer array of none, and on arrays of differing shapes,
-- naming the first one's shape and the first that differs.
prop_ravel :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
              View -> Property
prop_ravel v =
  let x = mkViewUpTo v :: Array v a
      y = reshape [product (shapeL x), 1] x
      msg = "ravel: non-conforming inner dimensions: "
        ++ show [shapeL x, shapeL y]
  in  failsWith "ravel: empty array"
                (ravel (fromList [0] [] :: Array V.Vector (Array v a)))
      .&&. (if shapeL x == shapeL y then property True
            else failsWith msg (ravel (fromList [3] [x, x, y]
                                         :: Array V.Vector (Array v a))))

-- A call of rotate on an array of shape osh ++ h : t, rotating it k times
-- along dimension length osh.
data RotateCase = RotateCase [Int] Int [Int] Int
  deriving Show

instance Arbitrary RotateCase where
  arbitrary = RotateCase <$> genShape 2 <*> choose (0, 4) <*> genShape 2
                         <*> choose (0, 12)
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
      rot ys = concat [ concat (rotL (k - 1 - i) (rows ys))
                      | i <- [0 .. k - 1] ]
      subs = [ take (h * m) (drop (j * h * m) xs)
             | j <- [0 .. product osh - 1] ]
  in  map toInteger xs == [1 .. toInteger n] ==>
      rotate (length osh) k (fromList (osh ++ h : t) xs :: Array v a)
      === fromList (osh ++ k : h : t) (concatMap rot subs)

-- The zips of the instance's vectors take as many elements as the shortest
-- vector has, as the list's zips do.
prop_vZipWith :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => Property
prop_vZipWith =
  forAll gen $ \ l1 -> forAll gen $ \ l2 -> forAll gen $ \ l3 ->
  forAll gen $ \ l4 -> forAll gen $ \ l5 ->
  let vec = I.vFromList :: [a] -> v a
      f3 a b c = a + 10 * b + 100 * c
      f4 a b c d = f3 a b c + 1000 * d
      f5 a b c d e = f4 a b c d + 10000 * e
  in  I.vToList (I.vZipWith (-) (vec l1) (vec l2)) === zipWith (-) l1 l2
      .&&. I.vToList (I.vZipWith3 f3 (vec l1) (vec l2) (vec l3))
           === zipWith3 f3 l1 l2 l3
      .&&. I.vToList (I.vZipWith4 f4 (vec l1) (vec l2) (vec l3) (vec l4))
           === zipWith4 f4 l1 l2 l3 l4
      .&&. I.vToList (I.vZipWith5 f5 (vec l1) (vec l2) (vec l3) (vec l4)
                                     (vec l5))
           === zipWith5 f5 l1 l2 l3 l4 l5
  where gen = choose (0, 4) >>= genElems (-9, 9) :: Gen [a]

-- The Arbitrary instance's arrays hold as many elements as their shapes say,
-- and some of them are empty.
prop_arbitrary :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => Property
prop_arbitrary = checkCoverage $
  forAll (arbitrary :: Gen (Array v a)) $ \ x ->
  cover 5 (null (toList x)) "empty" $
    length (toList x) === product (shapeL x)
