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
module DynamicSTest(test) where

import Control.DeepSeq
import Control.Exception
import qualified Data.Array.Dynamic as D
import Data.Array.DynamicS
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.List (zipWith4, zipWith5)
import qualified Data.Array.Internal.DynamicS as DS
import qualified Data.Vector.Storable as V
import Data.Int (Int8)
import Data.Word (Word16, Word8)
import Foreign.ForeignPtr.Unsafe (unsafeForeignPtrToPtr)
import Foreign.Ptr (minusPtr)
import Foreign.Storable (sizeOf)
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.HUnit (assertEqual, assertFailure, Assertion)
import Test.QuickCheck
  ( Property, choose, conjoin, counterexample, elements, forAll, listOf, property
  , vectorOf, (.&&.), (===), (==>) )
import Views
  ( Elem, Op (..), View (..), failsIn, failsWith, genBadOp, genElems, genShape, opNames, opShape
  , opSource, silentBadOp, testPropertyN, upTo )

assertThrows :: (NFData a) => String -> a -> Assertion
assertThrows s a = catch (deepseq a $ assertFailure s) (\ (_ :: ErrorCall) -> return ())

assertThrowsIn :: (NFData a) => String -> String -> a -> Assertion
assertThrowsIn s f a = catch (deepseq a $ assertFailure s)
                             (\ (ErrorCall e) -> assertEqual s f (takeWhile (/= ':') e))

test :: Test
test = testGroup "DynamicS" $
  let a1, a2 :: Array Int
      a1 = fromList [2,3] [1..6]
      a2 = transpose [1,0] a1
      show_1 = assertEqual "1" "fromList [2,3] [1,2,3,4,5,6]" (show a1)
      show_2 = assertEqual "2" "fromList [3,2] [1,4,2,5,3,6]" (show a2)
      eq_1 = assertEqual "1" True (a1 == a1)
      eq_2 = assertEqual "2" False (a1 == a2)
      ord_1 = assertEqual "1" EQ (a1 `compare` a1)
      ord_2 = assertEqual "2" LT (a1 `compare` a2)
      shapeL_1 = assertEqual "1" [2,3] (shapeL a1)
      shapeL_2 = assertEqual "2" [3,2] (shapeL a2)
      rank_1 = assertEqual "1" 2 (rank a1)
      rank_2 = assertEqual "2" 2 (rank a2)
      index_1 = assertEqual "1" (fromList [3] [1,2,3]) (index a1 0)
      index_2 = assertEqual "2" (fromList [2] [1,4]) (index a2 0)
      index_3 = assertEqual "3" (fromList [] [4]) (a2 `index` 0 `index` 1)
      index_4 = assertThrows "<0" (index a1 (-1))
      index_5 = assertThrows ">" (index a1 2)
      -- index need not know that the elements are Storable.
      constraints_1 = assertEqual "1" (index a1 1) (indexN a1 1)
        where indexN :: Array a -> Int -> Array a
              indexN = index
      toList_1 = assertEqual "1" [1,2,3,4,5,6] (toList a1)
      toList_2 = assertEqual "2" [1,4,2,5,3,6] (toList a2)
      toVector_1 = assertEqual "1" (V.fromList [1,2,3,4,5,6]) (toVector a1)
      toVector_2 = assertEqual "2" (V.fromList [1,4,2,5,3,6]) (toVector a2)
      fromList_1 = assertThrows "sh" (fromList [] [1,2::Int])
      fromList_2 = assertThrows "sh" (fromList [4,5] [1,2::Int])
      fromVector_1 = assertEqual "1" a1 (fromVector [2,3] $ V.fromList [1..6])
      fromVector_2 = assertThrowsIn "2" "fromVector" (fromVector [2,3] $ V.fromList [1..5::Int])
      normalize_1 = assertEqual "1" a1 (normalize a1)
      -- toVector of a row is a slice of the whole vector, which normalize copies
      -- the row out of, and a normal array normalize leaves alone, as it does
      -- one whose dimension of extent 1 has stride 0.
      normalize_2 = assertEqual "2" (True, False, True, False, True, True)
                      ( inBig (toVector (index big 1)), inBig (toVector (normalize (index big 1)))
                      , inBig (toVector (reshape [1,1000] (index big 1)))
                      , inBig (toVector (normalize (reshape [1,1000] (index big 1))))
                      , ptrOf (toVector (normalize big)) == ptrOf (toVector big)
                      , ptrOf (toVector (normalize (reshape [4000,1] (reshape [4000] big))))
                        == ptrOf (toVector big) )
        where big = fromList [4,1000] [1..4000] :: Array Double
              ptrOf = unsafeForeignPtrToPtr . fst . V.unsafeToForeignPtr0
              inBig w = let d = ptrOf w `minusPtr` ptrOf (toVector big) in d >= 0 && d < 32000
      reshape_1 = assertEqual "1" (fromList [6] [1..6]) (reshape [6] a1)
      reshape_2 = assertEqual "1" (fromList [1,2,3,1] [1,4,2,5,3,6]) (reshape [1,2,3,1] a2)
      a3, a4 :: Array Int
      a3 = fromList [1] [5]
      a4 = fromList [] [5]
      stretch_1 = assertEqual "1" (fromList [3] [5,5,5]) (stretch [3] a3)
      stretch_2 = assertEqual "2" (fromList [2,2,3,2] [1,1,2,2,3,3,4,4,5,5,6,6,1,1,2,2,3,3,4,4,5,5,6,6])
                                  (stretch [2,2,3,2] $ reshape [1,2,3,1] a1)
      stretch_3 = assertThrows "3" (stretch [1,2] a3)
      stretch_4 = assertThrows "4" (stretch [4,3] a1)
      scalar_1 = assertEqual "1" a4 (scalar 5)
      unScalar_1 = assertEqual "1" 5 (unScalar a4)
      unScalar_2 = assertThrows "2" (unScalar a3)
      constant_1 = assertEqual "1" (fromList [2,3] [1,1,1,1,1,1]) (constant [2,3] (1::Int))
      iota_1 = assertEqual "1" (map fromIntegral [0..299::Int]) (toList (iota 300 :: Array Word8))
      mapA_1 = assertEqual "1" (fromList [2,3] [2..7]) (mapA succ a1)
      mapA_2 = assertEqual "1" (fromList [3,2] [2,5,3,6,4,7]) (mapA succ a2)
      mapA_3 = assertEqual "3" (fromList [4] [1,1,1,1])  -- 1 `div` 0 outside the view
                               (mapA (1 `div`) (stretch [4] (slice [(2,1)] (fromList [3] [0,0,1 :: Int]))))
      zipWithA_1 = assertEqual "1" (fromList [2,3] [2,4..12]) (zipWithA (+) a1 a1)
      zipWithA_2 = assertThrows "2" (zipWithA (+) a1 a2)
      zipWithA_3 = assertEqual "3" [] (toList (zipWithA quot (constant [0] 1) (constant [0] (0 :: Int))))  -- 1 `quot` 0 outside the view
      zipWith3A_1 = assertEqual "1" (fromList [2,3] [2,6,12,20,30,42]) (zipWith3A (\ x y z -> x*y+z) a1 a1 a1)
      zipWith3A_2 = assertEqual "2" [] (toList (zipWith3A (\ x y z -> x `quot` (y + z)) (constant [0] 1) (constant [0] 0) (constant [0] (0 :: Int))))
      pad_1 = assertEqual "1" (fromList [5,10] [9,9,9,9,9,9,9,9,9,9,
                                                9,9,9,1,2,3,9,9,9,9,
                                                9,9,9,4,5,6,9,9,9,9,
                                                9,9,9,9,9,9,9,9,9,9,
                                                9,9,9,9,9,9,9,9,9,9])
                              (pad [(1,2),(3,4)] 9 a1)
      pad_2 = assertThrows "2" (pad [(1,1),(1,1),(1,1)] 0 a1)
      a5 :: Array Int
      a5 = fromList [2,3,4] [1..24]
      transpose_1 = assertEqual "1" (fromList [2,3,4] [1,2,3,4,
                                                       5,6,7,8,
                                                       9,10,11,12,

                                                       13,14,15,16,
                                                       17,18,19,20,
                                                       21,22,23,24])
                                    (transpose [0,1,2] a5)
      transpose_2 = assertEqual "2" (fromList [2,4,3] [1,5,9,
                                                       2,6,10,
                                                       3,7,11,
                                                       4,8,12,

                                                       13,17,21,
                                                       14,18,22,
                                                       15,19,23,
                                                       16,20,24])
                                    (transpose [0,2,1] a5)
      transpose_3 = assertEqual "3" (fromList [3,2,4] [1,2,3,4,
                                                       13,14,15,16,

                                                       5,6,7,8,
                                                       17,18,19,20,

                                                       9,10,11,12,
                                                       21,22,23,24])
                                    (transpose [1,0,2] a5)
      transpose_4 = assertEqual "4" (fromList [3,4,2] [1,13,
                                                       2,14,
                                                       3,15,
                                                       4,16,

                                                       5,17,
                                                       6,18,
                                                       7,19,
                                                       8,20,

                                                       9,21,
                                                       10,22,
                                                       11,23,
                                                       12,24])
                                    (transpose [1,2,0] a5)
      transpose_5 = assertEqual "5" (fromList [4,2,3] [1,5,9,
                                                       13,17,21,

                                                       2,6,10,

                                                       14,18,22,

                                                       3,7,11,
                                                       15,19,23,

                                                       4,8,12,
                                                       16,20,24])
                                    (transpose [2,0,1] a5)
      transpose_6 = assertEqual "6" (fromList [4,3,2] [1,13,
                                                       5,17,
                                                       9,21,

                                                       2,14,
                                                       6,18,
                                                       10,22,

                                                       3,15,
                                                       7,19,
                                                       11,23,

                                                       4,16,
                                                       8,20,
                                                       12,24])
                                    (transpose [2,1,0] a5)
      transpose_7 = assertThrows "7" (transpose [0,1,2,3] a5)
      transpose_8 = assertThrows "7" (transpose [0,1,3] a5)
      transpose_9 = assertEqual "9" (fromList [3,2,4] [1,2,3,4,
                                                       13,14,15,16,

                                                       5,6,7,8,
                                                       17,18,19,20,

                                                       9,10,11,12,
                                                       21,22,23,24])
                                    (transpose [1,0] a5)
      append_1 = assertEqual "1" (fromList [3,3] [1..9])
                                 (append a1 (fromList [1,3] [7,8,9]))
      concatOuter_1 = assertEqual "1" (fromList [6,3] [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6])
                                      (concatOuter [a1, concatOuter [a1,a1]])
      concatOuter_2 = assertThrows "2" (concatOuter [a1, a2])
      a6 :: Array Int
      a6 = fromList [4,5] [1..20]
      window_1 = assertEqual "1" (fromList [2,3,3,3] [1,2,3,
                                                      6,7,8,
                                                      11,12,13,

                                                      2,3,4,
                                                      7,8,9,
                                                      12,13,14,

                                                      3,4,5,
                                                      8,9,10,
                                                      13,14,15,


                                                      6,7,8,
                                                      11,12,13,
                                                      16,17,18,

                                                      7,8,9,
                                                      12,13,14,
                                                      17,18,19,

                                                      8,9,10,
                                                      13,14,15,
                                                      18,19,20])
                                 (window [3,3] a6)
      window_2 = assertThrows "2" (window [3,6] a6)
      window_3 = assertThrows "3" (window [3,3,3] a6)
      stride_1 = assertEqual "1" (fromList [2,2,2] [1,3,
                                                    9,11,

                                                    13,15,
                                                    21,23])
                                 (stride [1,2,2] a5)
      stride_2 = assertThrows "2" (stride [1,2,2] a1)
      stride_3 = assertThrows "3" (stride [0] a1)
      stride_4 = assertThrows "4" (stride [-1] a1)
      slice_1 = assertEqual "1" (fromList [2,2,1] [8,12,20,24])
                                (slice [(0,2),(1,2),(3,1)] a5)
      slice_2 = assertThrows "2" (slice [(0,0)] a4)
      slice_3 = assertThrows "3" (slice [(-1,1)] a5)
      slice_4 = assertThrows "4" (slice [(10,0)] a5)
      slice_5 = assertThrows "5" (slice [(0,3)] a5)
      a7 = mapA succ a5
      dot x y = reduce (+) 0 $ zipWithA (*) x y
      rerank2_1 = assertEqual "1" (fromList [2,3] [40,200,488,904,1448,2120])
                                  (rerank2 2 dot a5 a7)
      rev_1 = assertEqual "1" (fromList [2,3] [3,2,1,6,5,4])
                              (rev [1] a1)
      rev_2 = assertEqual "2" (fromList [2,3] [6,5,4,3,2,1])
                              (rev [0,1] a1)
      rev_3 = assertThrows "3" (rev [2] a1)
      reduce_1 = assertEqual "1" (scalar 720) (reduce (*) 1 a1)
      reduce_2 = assertEqual "2" (fromList [2] [6,120]) (rerank 1 (reduce (*) 1) a1)
      reduce_3 = assertEqual "3" (fromList [3] [4,10,18]) (rerank 1 (reduce (*) 1) a2)
      -- An empty view at the end of a longer vector, so that reading the
      -- element at the offset fails under the bounds checks.
      allSameA_1 = assertEqual "1" True (allSameA (slice [(2,0)] a1))
      -- As allSame . toList, comparing the first element with the others only.
      allSameA_2 = assertEqual "2" [True, False, False, False, True]
                                   (map allSameA [ fromList [1] [nan], fromList [2] [nan, nan]
                                                 , constant [3] nan, normalize (constant [3] nan)
                                                 , slice [(0,1)] (fromList [2] [nan, 1]) ])
        where nan = 0 / 0 :: Double

      tests =
        [ testCase "show_1" show_1
        , testCase "show_2" show_2
        , testCase "eq_1" eq_1
        , testCase "eq_2" eq_2
        , testCase "ord_1" ord_1
        , testCase "ord_2" ord_2
        , testCase "shapeL_1" shapeL_1
        , testCase "shapeL_2" shapeL_2
        , testCase "rank_1" rank_1
        , testCase "rank_2" rank_2
        , testCase "index_1" index_1
        , testCase "index_2" index_2
        , testCase "index_3" index_3
        , testCase "index_4" index_4
        , testCase "index_5" index_5
        , testCase "constraints_1" constraints_1
        , testCase "toList_1" toList_1
        , testCase "toList_2" toList_2
        , testCase "toVector_1" toVector_1
        , testCase "toVector_2" toVector_2
        , testCase "fromList_1" fromList_1
        , testCase "fromList_2" fromList_2
        , testCase "fromVector_1" fromVector_1
        , testCase "fromVector_2" fromVector_2
        , testCase "normalize_1" normalize_1
        , testCase "normalize_2" normalize_2
        , testCase "reshape_1" reshape_1
        , testCase "reshape_2" reshape_2
        , testCase "stretch_1" stretch_1
        , testCase "stretch_2" stretch_2
        , testCase "stretch_3" stretch_3
        , testCase "stretch_4" stretch_4
        , testCase "scalar_1" scalar_1
        , testCase "unScalar_1" unScalar_1
        , testCase "unScalar_2" unScalar_2
        , testCase "constant_1" constant_1
        , testCase "iota_1" iota_1
        , testCase "mapA_1" mapA_1
        , testCase "mapA_2" mapA_2
        , testCase "mapA_3" mapA_3
        , testCase "zipWithA_1" zipWithA_1
        , testCase "zipWithA_2" zipWithA_2
        , testCase "zipWithA_3" zipWithA_3
        , testCase "zipWith3A_1" zipWith3A_1
        , testCase "zipWith3A_2" zipWith3A_2
        , testCase "pad_1" pad_1
        , testCase "pad_2" pad_2
        , testCase "transpose_1" transpose_1
        , testCase "transpose_2" transpose_2
        , testCase "transpose_3" transpose_3
        , testCase "transpose_4" transpose_4
        , testCase "transpose_5" transpose_5
        , testCase "transpose_6" transpose_6
        , testCase "transpose_7" transpose_7
        , testCase "transpose_8" transpose_8
        , testCase "transpose_9" transpose_9
        , testCase "append_1" append_1
        , testCase "concatOuter_1" concatOuter_1
        , testCase "concatOuter_2" concatOuter_2
        , testCase "window_1" window_1
        , testCase "window_2" window_2
        , testCase "window_3" window_3
        , testCase "stride_1" stride_1
        , testCase "stride_2" stride_2
        , testCase "stride_3" stride_3
        , testCase "stride_4" stride_4
        , testCase "slice_1" slice_1
        , testCase "slice_2" slice_2
        , testCase "slice_3" slice_3
        , testCase "slice_4" slice_4
        , testCase "slice_5" slice_5
        , testCase "rerank2_1" rerank2_1
        , testCase "rev_1" rev_1
        , testCase "rev_2" rev_2
        , testCase "rev_3" rev_3
        , testCase "reduce_1" reduce_1
        , testCase "reduce_2" reduce_2
        , testCase "reduce_3" reduce_3
        , testCase "allSameA_1" allSameA_1
        , testCase "allSameA_2" allSameA_2
        , testPropertyN "prop_allSameA" prop_allSameA
        ]
  in  tests ++ elemProps @Int @Word ++ [testGroup "Word8" (elemProps @Word8 @Int8)]

-- applyOp and mkView of Views, over Storable arrays.
applyOp :: Unbox a => Op -> Array a -> Array a
applyOp (Transpose is) = transpose is
applyOp (Rev rs) = rev rs
applyOp (Slice sl) = slice sl
applyOp (Stride ts) = stride ts
applyOp (Window ws) = window ws
applyOp (Index i) = (`index` i)
applyOp (Broadcast ds sh) = broadcast ds sh

mkView :: Unbox a => View -> [a] -> Array a
mkView (View sh ops) xs = foldl (flip applyOp) (fromList sh xs) ops

-- allSameA agrees with allSame on the list, NaN included.
prop_allSameA :: View -> Property
prop_allSameA v@(View sh _) =
  forAll (elements [[1], [0 / 0], [1, 2], [0 / 0, 1], [1, 1, 1, 2 :: Double]]) $ \ pool ->
  forAll (vectorOf (product sh) (elements pool)) $ \ xs ->
  let x = mkView v xs
  in  allSameA x === I.allSame (toList x)

-- The properties run at each Elem type a, all but that of NaN, and bitcast
-- between a and b, of its size.
elemProps :: forall a b . (Elem a, Unbox a, Integral b, Show b, Unbox b) => [Test]
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
  , testPropertyN "prop_bitcast" (prop_bitcast @a @b)
  , testPropertyN "prop_show" (prop_show @a)
  , testPropertyN "prop_rerank" (prop_rerank @a)
  ]

-- toList and toVector agree with indexing the view element by element.
prop_toList :: forall a . (Elem a, Unbox a) => View -> Property
prop_toList v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
      l = [ unScalar (foldl index x is) | is <- mapM (\ s -> [0 .. s - 1]) (shapeL x) ]
  in  toList x === l .&&. V.toList (toVector x) === l

-- == and compare agree with comparing the lists, between a view and an
-- array of its elements with at most one of them changed, and between two
-- views of one layout over vectors that differ in at most one element,
-- inside the views or outside them.
prop_compare :: forall a . (Elem a, Unbox a) => View -> Property
prop_compare v@(View sh _) =
  let n = product sh
      x = mkView v (upTo n) :: Array a
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
prop_reduce :: forall a . (Elem a, Unbox a) => View -> Property
prop_reduce v@(View sh _) =
  forAll (genElems (1, 9) (product sh)) $ \ xs ->
  forAll (fromIntegral <$> choose (0, 9 :: Int)) $ \ t ->
  let x = mkView v xs :: Array a
      l = toList x
  in  reduce (+) 0 x === scalar (sum l)
      .&&. sumA x === sum l .&&. productA x === product l
      .&&. anyA (> t) x === any (> t) l .&&. allA (> t) x === all (> t) l
      .&&. (if null l then property True
            else maximumA x === maximum l .&&. minimumA x === minimum l)

-- pad agrees with indexing the view where an index falls inside it, and
-- gives the padding value elsewhere, for a pad list of any length up to
-- the rank that leaves at most 10000 elements.
prop_pad :: forall a . (Elem a, Unbox a) => View -> Property
prop_pad v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
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
prop_viewOps :: forall a . (Elem a, Unbox a) => View -> Property
prop_viewOps (View sh ops) =
  let steps = scanl (flip applyOp) (fromList sh (upTo (product sh))) ops :: [Array a]
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
prop_badOps :: forall a . (Elem a, Unbox a) => View -> Property
prop_badOps v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
      xsh = shapeL x
  in  forAll (genBadOp xsh) $ \ op ->
      let y = applyOp op x
      in  if silentBadOp xsh op then shapeL y === opShape xsh op
          else failsIn (opNames op) (sum (shapeL y) + fromIntegral (sum (toList y)))

-- The offset, the strides and the length of the vector of an array.
layoutOf :: Unbox a => Array a -> (Int, [Int], Int)
layoutOf (DS.A (DG.A _ t)) = (I.offset t, I.strides t, V.length (I.values t))

-- normalize gives the view as a normal array, its elements in a vector
-- of just their number, at offset 0 and with natural strides; reshape to
-- one dimension, append and concatOuter of the view and a normal array of
-- its shape, zipWithA of the two either way round, and traverseA in the
-- applicative of pairs agree with the lists.
prop_copy :: forall a . (Elem a, Unbox a) => View -> Property
prop_copy v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
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
prop_zipWith :: forall a . (Elem a, Unbox a) => View -> Property
prop_zipWith v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
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
prop_update :: forall a . (Elem a, Unbox a) => View -> Property
prop_update v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
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
prop_fromVector :: forall a . (Elem a, Unbox a) => Property
prop_fromVector =
  forAll (genShape 3) $ \ sh ->
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  forAll (choose (0, 3)) $ \ k ->
  forAll (choose (0, 3)) $ \ m ->
  forAll (choose (0, 9)) $ \ n ->
  let n' = length xs
      vec = V.slice k n' (V.fromList (replicate k 99 ++ xs ++ replicate m 99))
  in  fromVector sh vec === fromList sh (xs :: [a])
      .&&. failsWith ("fromVector: size mismatch " ++ show (n', n' + 1))
                     (fromVector sh (V.fromList (0 : xs)))
      .&&. iterateN n (* 3) (1 :: a) === fromList [n] (take n (iterate (* 3) 1))

-- bitcast of a view to an integral type b of the same size reinterprets
-- each element as fromIntegral does, and bitcast to a type of another size
-- fails.
prop_bitcast :: forall a b . (Elem a, Unbox a, Integral b, Show b, Unbox b) => View -> Property
prop_bitcast v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkView v xs :: Array a
      w = bitcast x :: Array b
  in  toList w === map fromIntegral (toList x) .&&. bitcast w === x
      .&&. failsWith ("bitcast: the types must have the same size. "
                      ++ show (sizeOf (0 :: a), sizeOf (0 :: Word16)))
                     (bitcast x :: Array Word16)

-- An array reads back from its show.
prop_show :: forall a . (Elem a, Unbox a) => View -> Property
prop_show v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkView v xs :: Array a
  in  read (show x) === x

-- rerank applies its function to each subarray below the first n
-- dimensions, rerank2 to each pair of them, unravel lists the subarrays
-- below the first dimension and ravel puts them back.  Where one of those
-- dimensions is empty, each fails with "ravelOuter: empty list", which is
-- to become the model's answer once they find the shape of the result
-- without applying the function.
prop_rerank :: forall a . (Elem a, Unbox a) => View -> Property
prop_rerank v@(View sh _) =
  let x = mkView v (upTo (product sh)) :: Array a
      xsh = shapeL x
      empty = "ravelOuter: empty list"
      unravelled = case xsh of
        [] -> property True
        0 : _ -> failsWith empty (unravel x :: D.Array (Array a))
        s : _ -> map toList (D.toList (unravel x :: D.Array (Array a)))
                 === [ toList (index x i) | i <- [0 .. s - 1] ]
                 .&&. ravel (unravel x :: D.Array (Array a)) === x
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
