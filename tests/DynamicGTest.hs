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
{-# LANGUAGE MagicHash #-}
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
import Data.List (zipWith4, zipWith5)
import Data.Primitive.ByteArray (sizeofByteArray)
import qualified Data.Vector as V
import qualified Data.Vector.Primitive as VP
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import qualified Data.Vector.Unboxed.Base as VUB
import Data.Word (Word8)
import Foreign.Storable (Storable, sizeOf)
import GHC.Exts (Int (I#), sizeofMutableByteArray#)
import GHC.ForeignPtr (ForeignPtr (..), ForeignPtrContents (..))
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  ( Arbitrary (..), Property, choose, conjoin, counterexample, elements, forAll, listOf, property
  , shrinkList, vectorOf, (.&&.), (===), (==>) )
import Views
  ( Elem, View (..), applyOpG, failsIn, failsWith, genBadOp, genElems, genShape, mkViewG
  , opName, opShape, opSource, testPropertyN, upTo )

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

backend :: forall v a . ( I.Vector v, I.VecElem v a, I.VecElem v Double, Ord (v a)
                        , Show (v a), Elem a, Owns (v a) ) =>
           Bool -> String -> Test
backend nan n = testGroup n $
  [ testPropertyN "prop_allSameA" (prop_allSameA @v) | nan ] ++
  [ testPropertyN "prop_toList" (prop_toList @v @a)
  , testPropertyN "prop_compare" (prop_compare @v @a)
  , testPropertyN "prop_reduce" (prop_reduce @v @a)
  , testPropertyN "prop_pad" (prop_pad @v @a)
  , testPropertyN "prop_viewOps" (prop_viewOps @v @a)
  , testPropertyN "prop_badOps" (prop_badOps @v @a)
  , testPropertyN "prop_copy" (prop_copy @v @a)
  , testPropertyN "prop_zipWith" (prop_zipWith @v @a)
  , testPropertyN "prop_update" (prop_update @v @a)
  , testPropertyN "prop_fromVector" (prop_fromVector @v @a)
  , testPropertyN "prop_show" (prop_show @v @a)
  , testPropertyN "prop_rerank" (prop_rerank @v @a)
  , testPropertyN "prop_rotate" (prop_rotate @v @a)
  ]

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: forall v . (I.Vector v, I.VecElem v Double) => View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1], [1, 1, 1, 2 :: Double]]) $ \ pool ->
  forAll (vectorOf (product sh) (elements pool)) $ \ xs ->
  let x = mkViewG v xs :: Array v Double
  in  allSameA x === I.allSame (toList x)

-- toList and toVector agree with indexing the view element by element.
prop_toList :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_toList v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      l = [ unScalar (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) (shapeL x) ]
  in  toList x === l .&&. I.vToList (toVector x) === l

-- == and compare agree with comparing the lists, between a view and an
-- array of its elements with at most one of them changed, and between two
-- views of one layout over vectors that differ in at most one element,
-- inside the views or outside them.
prop_compare :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Elem a) =>
                View -> Property
prop_compare v@(View sh _) =
  let n = product sh
      x = mkViewG v (upTo n) :: Array v a
      l = toList x
  in  forAll (choose (0, length l)) $ \ i ->
      forAll (choose (0, n)) $ \ j ->
      forAll (choose (-1, 1)) $ \ d ->
      let l' = [ if k == i then e + fromIntegral d else e | (k, e) <- zip [0 ..] l ]
          y = fromList (shapeL x) l'
          z = mkViewG v [ fromIntegral (if k == j then k + d else k) | k <- [0 .. n - 1] ]
      in  (x == y) === (l == l') .&&. compare x y === compare l l'
          .&&. compare y x === compare l' l
          .&&. (x == z) === (l == toList z) .&&. compare x z === compare l (toList z)

-- The reductions agree with the list's: reduce, sumA, productA, maximumA,
-- minimumA, anyA and allA.
prop_reduce :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
               View -> Property
prop_reduce v@(View sh _) =
  forAll (genElems (1, 9) (product sh)) $ \ xs ->
  forAll (fromIntegral <$> choose (0, 9 :: Int)) $ \ t ->
  let x = mkViewG v xs :: Array v a
      l = toList x
  in  reduce (+) 0 x === scalar (sum l)
      .&&. sumA x === sum l .&&. productA x === product l
      .&&. anyA (> t) x === any (> t) l .&&. allA (> t) x === all (> t) l
      .&&. (if null l then property True
            else maximumA x === maximum l .&&. minimumA x === minimum l)

-- pad agrees with indexing the view where an index falls inside it, and
-- gives the padding value elsewhere, for a pad list of any length up to
-- the rank that leaves at most 10000 elements.
prop_pad :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_pad v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
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
prop_viewOps :: forall v a . (I.Vector v, I.VecElem v a, Elem a) => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOpG) (fromList sh (upTo (product sh))) ops :: [Array v a]
      at x is = unScalar (foldl index x is)
      step (x, op, y) =
        let xsh = shapeL x
            iss = mapM (\ s -> [0 .. s - 1]) (shapeL y)
        in  counterexample (show op)
              (shapeL y === opShape xsh op
               .&&. map (at y) iss === map (at x . opSource xsh op) iss)
  in  conjoin (map step (zip3 steps ops (drop 1 steps)))

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

-- Whether a vector's storage holds its elements and nothing more, keeping no
-- larger vector alive, as normalize's copy out of a longer vector must.
class Owns w where
  ownsStorage :: w -> Bool

instance Owns [a] where
  ownsStorage _ = True

instance Owns (V.Vector a) where
  ownsStorage w = let (arr, _, n) = V.toArraySlice w
                  in  V.length (V.fromArray arr) == n

instance Storable a => Owns (VS.Vector a) where
  ownsStorage w = case VS.unsafeToForeignPtr0 w of
    (ForeignPtr _ (PlainPtr m), n) -> owns m n
    (ForeignPtr _ (MallocPtr m _), n) -> owns m n
    (_, n) -> n == 0
    where owns m n = I# (sizeofMutableByteArray# m) == n * sizeOf (undefined :: a)

instance Owns (VU.Vector Int) where
  ownsStorage (VUB.V_Int (VP.Vector _ n b)) = sizeofByteArray b == n * sizeOf (0 :: Int)

instance Owns (VU.Vector Word8) where
  ownsStorage (VUB.V_Word8 (VP.Vector _ n b)) = sizeofByteArray b == n

-- normalize gives the view as a normal array, its elements in a vector
-- of just their number, at offset 0 and with natural strides; reshape to
-- one dimension, append and concatOuter of the view and a normal array of
-- its shape, zipWithA of the two either way round, and traverseA in the
-- applicative of pairs agree with the lists; and append and concatOuter
-- fail on scalars.
prop_copy :: forall v a . (Owns (v a), I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
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
          .&&. counterexample "normalize keeps a larger vector"
                 (I.vLength (valuesOf x) == n || ownsStorage (valuesOf z))
          .&&. toList (reshape [n] x) === l
          .&&. toList (zipWithA (-) x y) === zipWith (-) l ys
          .&&. toList (zipWithA (-) y x) === zipWith (-) ys l
          .&&. (if null xsh
                then failsWith "append: bad shape" (append x y)
                     .&&. failsWith "concatOuter: rank 0 array" (concatOuter [x, y, y])
                else toList (append x y) === l ++ ys
                     .&&. toList (concatOuter [x, y, y]) === l ++ ys ++ ys)
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
prop_update :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
               View -> Property
prop_update v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      l = toList x
      ixs = zip [0 :: Int ..] (mapM (\ s -> [0 .. s - 1]) xsh)
      bad = if null xsh then [0] else xsh
  in  forAll (if null l then return [] else listOf ((,) <$> elements ixs <*> (fromIntegral <$> choose (-9, -1 :: Int)))) $ \ us ->
      let set ys ((k, _), e) = [ if k' == k then e else y | (k', y) <- zip [0 ..] ys ]
      in  update x [ (is, e) | ((_, is), e) <- us ] === fromList xsh (foldl set l us)
          .&&. failsWith ("update: index out of bounds: " ++ show [bad]) (update x [(bad, 0)])

-- fromVector makes an array of the elements of a vector, here a slice of
-- a longer one, and fails on a vector of another length; iterateN makes
-- one of the first iterates of a function.
prop_fromVector :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
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
prop_show :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
             View -> Property
prop_show v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkViewG v xs :: Array v a
  in  read (show x) === x

-- rerank applies its function to each subarray below the first n
-- dimensions, rerank2 to each pair of them, unravel lists the subarrays
-- below the first dimension and ravel puts them back.  Where one of those
-- dimensions is empty, unravel gives an empty array, and rerank and
-- rerank2 fail, having no result of the function to take a shape from.
prop_rerank :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
               View -> Property
prop_rerank v@(View sh _) =
  let x = mkViewG v (upTo (product sh)) :: Array v a
      xsh = shapeL x
      unravelled = case xsh of
        [] -> property True
        0 : _ -> shapeL (unravel x :: Array V.Vector (Array v a)) === [0]
        s : _ -> map toList (toList (unravel x :: Array V.Vector (Array v a)))
                 === [ toList (index x i) | i <- [0 .. s - 1] ]
                 .&&. ravel (unravel x :: Array V.Vector (Array v a)) === x
  in  unravelled .&&. forAll (choose (0, length xsh)) (\ n ->
      let (osh, ish) = splitAt n xsh
          subs = [ toList (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) osh ]
          double a = reshape [product (shapeL a)] (mapA (* 2) a)
      in  if product osh == 0
          then failsWith "rerank: empty outer dimension" (rerank n double x)
               .&&. failsWith "rerank2: empty outer dimension" (rerank2 n (zipWithA (+)) x x)
          else shapeL (rerank n double x) === osh ++ [product ish]
               .&&. toList (rerank n double x) === concatMap (map (* 2)) subs
               .&&. toList (rerank2 n (zipWithA (+)) x x) === map (* 2) (toList x))

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
prop_rotate :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
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
