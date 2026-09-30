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

{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeFamilies #-}
module DynamicTest(test) where

import Control.DeepSeq
import Control.Exception
import Data.Array.Dynamic
import qualified Data.Array.DynamicG as G
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.Dynamic as D
import qualified Data.Array.Internal.DynamicG as DG
import Data.List (nub, sort)
import qualified Data.Vector as V
import Data.Word (Word8)
import Test.Framework (Test, TestOptions' (..), plusTestOptions, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.HUnit (assertEqual, assertFailure, Assertion)
import Test.QuickCheck
  ( Arbitrary (..), Gen, Property, Testable, choose, oneof, shrinkList
  , shuffle, sublistOf, vectorOf, (.&&.), (===) )

assertThrows :: (NFData a) => String -> a -> Assertion
assertThrows s a = catch (deepseq a $ assertFailure s) (\ (_ :: ErrorCall) -> return ())

assertThrowsIn :: (NFData a) => String -> String -> a -> Assertion
assertThrowsIn s f a = catch (deepseq a $ assertFailure s)
                             (\ (ErrorCall e) -> assertEqual s f (takeWhile (/= ':') e))

-- A Vector instance with the methods the class had before vFromListN.
newtype OldVector a = OldVector [a]

instance I.Vector OldVector where
  type VecElem OldVector = I.None
  vIndex (OldVector xs) = I.vIndex xs
  vLength (OldVector xs) = I.vLength xs
  vToList (OldVector xs) = xs
  vFromList = OldVector
  vSingleton = OldVector . I.vSingleton
  vReplicate n = OldVector . I.vReplicate n
  vMap f (OldVector xs) = OldVector (I.vMap f xs)
  vZipWith f (OldVector xs) (OldVector ys) = OldVector (I.vZipWith f xs ys)
  vZipWith3 f (OldVector xs) (OldVector ys) (OldVector zs) = OldVector (I.vZipWith3 f xs ys zs)
  vZipWith4 f (OldVector xs) (OldVector ys) (OldVector zs) (OldVector us) = OldVector (I.vZipWith4 f xs ys zs us)
  vZipWith5 f (OldVector xs) (OldVector ys) (OldVector zs) (OldVector us) (OldVector ws) = OldVector (I.vZipWith5 f xs ys zs us ws)
  vAppend (OldVector xs) (OldVector ys) = OldVector (I.vAppend xs ys)
  vConcat xss = OldVector (I.vConcat [ xs | OldVector xs <- xss ])
  vFold f z (OldVector xs) = I.vFold f z xs
  vSlice o n (OldVector xs) = OldVector (I.vSlice o n xs)
  vSum (OldVector xs) = I.vSum xs
  vProduct (OldVector xs) = I.vProduct xs
  vMaximum (OldVector xs) = I.vMaximum xs
  vMinimum (OldVector xs) = I.vMinimum xs
  vUpdate (OldVector xs) us = OldVector (I.vUpdate xs us)
  vGenerate n = OldVector . I.vGenerate n
  vAll p (OldVector xs) = I.vAll p xs
  vAny p (OldVector xs) = I.vAny p xs

test :: Test
test = testGroup "Dynamic" $
  let a1, a2 :: Array Int
      a1 = fromList [2,3] [1..6]
      a2 = transpose [1,0] a1
      show_1 = assertEqual "1" "fromList [2,3] [1,2,3,4,5,6]" (show a1)
      show_2 = assertEqual "2" "fromList [3,2] [1,4,2,5,3,6]" (show a2)
      eq_1 = assertEqual "1" True (a1 == a1)
      eq_2 = assertEqual "2" False (a1 == a2)
      -- Views over vectors with elements outside them, which == must not compare.
      eq_3 = assertEqual "3" True (x == x)
        where x = stretch [4] (slice [(0,1)] (fromList [2] [1, undefined] :: Array Int))
      eq_4 = assertEqual "4" True (x == x)
        where x = stretch [3,2] $ reshape [1,2] $ index a 0
              a = fromList [2,2] [1,2,undefined,undefined] :: Array Int
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
      toList_1 = assertEqual "1" [1,2,3,4,5,6] (toList a1)
      toList_2 = assertEqual "2" [1,4,2,5,3,6] (toList a2)
      toVector_1 = assertEqual "1" (V.fromList [1,2,3,4,5,6]) (toVector a1)
      toVector_2 = assertEqual "2" (V.fromList [1,4,2,5,3,6]) (toVector a2)
      fromList_1 = assertThrows "sh" (fromList [] [1,2::Int])
      fromList_2 = assertThrows "sh" (fromList [4,5] [1,2::Int])
      fromVector_1 = assertEqual "1" a1 (fromVector [2,3] $ V.fromList [1..6])
      fromVector_2 = assertThrowsIn "2" "fromVector" (fromVector [2,3] $ V.fromList [1..5::Int])
      vFromListN_1 = assertEqual "1" (V.toList $ V.fromListN 2 [1,2,3::Int])
                                     (I.vFromListN 2 [1,2,3])
      vFromListN_2 = assertEqual "2" [1,2]
                                     (G.toList (G.fromList [2] [1,2] :: G.Array OldVector Int))
      normalize_1 = assertEqual "1" a1 (normalize a1)
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
      mapA_3 = assertEqual "3" True  -- 1 `div` 0 outside the view, the vector forced as if strict
                               (case mapA (1 `div`) (stretch [4] (slice [(2,1)] (fromList [3] [0,0,1 :: Int]))) of
                                  D.A (DG.A _ t) -> V.all (== 1) (I.values t))
      -- mapA maps only the part of the vector a view reads, and a broadcast
      -- of a view that skips elements without its broadcast dimensions.
      mapA_4 = assertEqual "4" [100, 100, 2]
                 [ vlen (mapA (+ 1) (stretch [1000,100] (reshape [1,100] (index m 3))))
                 , vlen (mapA (+ 1) (window [50] (iota 100 :: Array Int)))
                 , vlen (mapA (+ 1) (broadcast [1] [1000,2] (stride [2] (fromList [3] [1,2,3 :: Int])))) ]
        where m = fromList [10,100] [1..1000] :: Array Int
              vlen x = case x of D.A (DG.A _ t) -> V.length (I.values t)
      zipWithA_1 = assertEqual "1" (fromList [2,3] [2,4..12]) (zipWithA (+) a1 a1)
      zipWithA_2 = assertThrows "2" (zipWithA (+) a1 a2)
      zipWith3A_1 = assertEqual "1" (fromList [2,3] [2,6,12,20,30,42]) (zipWith3A (\ x y z -> x*y+z) a1 a1 a1)
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
      ravel_1 = assertEqual "1" (fromList [3,2,3] [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6])
                                (ravel $ fromList [3] [a1,a1,a1])
      ravel_2 = assertThrows "2" (ravel $ fromList [2] [a1, concatOuter [a1,a1]])
      unravel_1 = assertEqual "1" [a1,a1,a1]
                                  (toList $ unravel $ ravel $ fromList [3] [a1,a1,a1])
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
      stride_5 = assertEqual "5" (fromList [1] [1]) (stride [maxBound] (fromList [3] [1,2,3::Int]))
      rotate_1 = assertEqual "1" (fromList [2, 4, 3, 2]
                                           [1, 2, 3, 4, 5, 6,
                                            5, 6, 1, 2, 3, 4,
                                            3, 4, 5, 6, 1, 2,
                                            1, 2, 3, 4, 5, 6,
                                            7, 8, 9, 10, 11, 12,
                                            11, 12, 7, 8, 9, 10,
                                            9, 10, 11, 12, 7, 8,
                                            7, 8, 9, 10, 11, 12])
                                 (rotate 1 4 $ fromList [2, 3, 2] [1 .. 12::Int])
      rotate_2 = assertEqual "2" (fromList [2, 5, 3, 2]
                                           [3, 4, 5, 6, 1, 2,
                                            1, 2, 3, 4, 5, 6,
                                            5, 6, 1, 2, 3, 4,
                                            3, 4, 5, 6, 1, 2,
                                            1, 2, 3, 4, 5, 6,
                                            9, 10, 11, 12, 7, 8,
                                            7, 8, 9, 10, 11, 12,
                                            11, 12, 7, 8, 9, 10,
                                            9, 10, 11, 12, 7, 8,
                                            7, 8, 9, 10, 11, 12])
                                 (rotate 1 5 $ fromList [2, 3, 2] [1 .. 12::Int])
      rotate_3 = assertEqual "3" (fromList [3,1] [5,5,5]) (rotate 0 3 $ fromList [1] [5::Int])
      rotate_4 = assertThrowsIn "4" "rotate" (rotate 0 (-2) $ fromList [3] [1,2,3::Int])
      rotate_5 = assertEqual "5" (fromList [0,2,3] []) (rotate 1 2 $ fromList [0,3] ([] :: [Int]))
      rotate_6 = assertEqual "6" 0  -- the empty rotation keeps no vector alive
                                 (case rotate 1 2 (slice [(0,0)] a1) of D.A (DG.A _ t) -> V.length (I.values t))
      rotate_7 = assertThrowsIn "7" "rotate" (rotate (-1) 2 $ fromList [3] [1,2,3::Int])
      slice_1 = assertEqual "1" (fromList [2,2,1] [8,12,20,24])
                                (slice [(0,2),(1,2),(3,1)] a5)
      slice_2 = assertThrows "2" (slice [(0,0)] a4)
      slice_3 = assertThrows "3" (slice [(-1,1)] a5)
      slice_4 = assertThrows "4" (slice [(10,0)] a5)
      slice_5 = assertThrows "5" (slice [(0,3)] a5)
      box = scalar . Just
      rerank_1 = assertEqual "1" (box a5)
                                 (rerank 0 box a5)
      rerank_2 = assertEqual "2" (fromList [2] [Just $ fromList [3,4] [1,2,3,4,5,6,7,8,9,10,11,12],
                                                Just $ fromList [3,4] [13,14,15,16,17,18,19,20,21,22,23,24]])
                                 (rerank 1 box a5)
      rerank_3 = assertEqual "3" (fromList [2,3] [Just $ fromList [4] [1,2,3,4],
                                                  Just $ fromList [4] [5,6,7,8],
                                                  Just $ fromList [4] [9,10,11,12],
                                                  Just $ fromList [4] [13,14,15,16],
                                                  Just $ fromList [4] [17,18,19,20],
                                                  Just $ fromList [4] [21,22,23,24]])
                                 (rerank 2 box a5)
      rerank_4 = assertEqual "4" (mapA (Just . scalar) a5)
                                 (rerank 3 box a5)
      rerank_5 = assertThrows "4" (rerank 4 box a5)
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

      -- Test fast toVector
      toVector_10 =
        assertEqual "10" (V.fromList [1..24]) (toVector a5)                  -- full vector
      toVector_11 =
        assertEqual "11" (V.fromList [1..12]) (toVector $ slice [(0,1)] a5)  -- reduced length
      toVector_12 =
        assertEqual "12" (V.fromList [13..24]) (toVector $ slice [(1,1)] a5)  -- offset
      toVector_13 =
        assertEqual "13" (V.fromList $ [13..24] ++ [1..12])
                    (toVector $ rev [0] a5)                             -- non-normal dim 0
      toVector_14 =
        assertEqual "14" (V.fromList [9,10,11,12,5,6,7,8,1,2,3,4,21,22,23,24,17,18,19,20,13,14,15,16])
                    (toVector $ rev [1] a5)                             -- non-normal dim 1
      toVector_15 =
        assertEqual "15" (V.fromList [4,3,2,1,8,7,6,5,12,11,10,9,16,15,14,13,20,19,18,17,24,23,22,21])
                    (toVector $ rev [2] a5)                             -- non-normal dim 2

      tests =
        [ testCase "show_1" show_1
        , testCase "show_2" show_2
        , testCase "eq_1" eq_1
        , testCase "eq_2" eq_2
        , testCase "eq_3" eq_3
        , testCase "eq_4" eq_4
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
        , testCase "toList_1" toList_1
        , testCase "toList_2" toList_2
        , testCase "toVector_1" toVector_1
        , testCase "toVector_2" toVector_2
        , testCase "fromList_1" fromList_1
        , testCase "fromList_2" fromList_2
        , testCase "fromVector_1" fromVector_1
        , testCase "fromVector_2" fromVector_2
        , testCase "vFromListN_1" vFromListN_1
        , testCase "vFromListN_2" vFromListN_2
        , testCase "normalize_1" normalize_1
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
        , testCase "mapA_4" mapA_4
        , testCase "zipWithA_1" zipWithA_1
        , testCase "zipWithA_2" zipWithA_2
        , testCase "zipWith3A_1" zipWith3A_1
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
        , testCase "ravel_1" ravel_1
        , testCase "ravel_2" ravel_2
        , testCase "unravel_1" unravel_1
        , testCase "window_1" window_1
        , testCase "window_2" window_2
        , testCase "window_3" window_3
        , testCase "stride_1" stride_1
        , testCase "stride_2" stride_2
        , testCase "stride_3" stride_3
        , testCase "stride_4" stride_4
        , testCase "stride_5" stride_5
        , testCase "rotate_1" rotate_1
        , testCase "rotate_2" rotate_2
        , testCase "rotate_3" rotate_3
        , testCase "rotate_4" rotate_4
        , testCase "rotate_5" rotate_5
        , testCase "rotate_6" rotate_6
        , testCase "rotate_7" rotate_7
        , testCase "slice_1" slice_1
        , testCase "slice_2" slice_2
        , testCase "slice_3" slice_3
        , testCase "slice_4" slice_4
        , testCase "slice_5" slice_5
        , testCase "rerank_1" rerank_1
        , testCase "rerank_2" rerank_2
        , testCase "rerank_3" rerank_3
        , testCase "rerank_4" rerank_4
        , testCase "rerank_5" rerank_5
        , testCase "rerank2_1" rerank2_1
        , testCase "rev_1" rev_1
        , testCase "rev_2" rev_2
        , testCase "rev_3" rev_3
        , testCase "reduce_1" reduce_1
        , testCase "reduce_2" reduce_2
        , testCase "reduce_3" reduce_3
        , testCase "toVector_10" toVector_10
        , testCase "toVector_11" toVector_11
        , testCase "toVector_12" toVector_12
        , testCase "toVector_13" toVector_13
        , testCase "toVector_14" toVector_14
        , testCase "toVector_15" toVector_15
        , testPropertyN "prop_rotate" prop_rotate
        , testPropertyN "prop_readRangeT" prop_readRangeT
        , testPropertyN "prop_eq" prop_eq
        , testPropertyN "prop_mapA" prop_mapA
        ]
  in  tests

-- A property checked on a thousand cases rather than the default hundred.
testPropertyN :: Testable p => String -> p -> Test
testPropertyN name =
  plusTestOptions mempty { topt_maximum_generated_tests = Just 1000 } . testProperty name

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

genShape :: Int -> Gen [Int]
genShape r = do
  r' <- choose (0, r)
  vectorOf r' (choose (0, 4))

shrinkExtent :: Int -> [Int]
shrinkExtent = filter (>= 0) . shrink

-- rotate against a list model: the i'th of the k rotations of a subarray
-- is the subarray rotated left by k-1-i rows.
prop_rotate :: RotateCase -> Property
prop_rotate (RotateCase osh h t k) =
  let m = product t
      xs = [1 .. product (osh ++ h : t)] :: [Int]
      rows ys = [ take m (drop (i * m) ys) | i <- [0 .. h - 1] ]
      rotL j rs = let j' = j `mod` max 1 h in drop j' rs ++ take j' rs
      rot ys = concat [ concat (rotL (k - 1 - i) (rows ys)) | i <- [0 .. k - 1] ]
      subs = [ take (h * m) (drop (j * h * m) xs) | j <- [0 .. product osh - 1] ]
  in  rotate (length osh) k (fromList (osh ++ h : t) xs)
      === fromList (osh ++ k : h : t) (concatMap rot subs)

-- The operations that make views, for building random views.
data Op = Transpose [Int] | Rev [Int] | Slice [(Int, Int)] | Stride [Int]
        | Window [Int] | Index Int | Broadcast [Int] [Int]
  deriving Show

applyOp :: Op -> Array a -> Array a
applyOp (Transpose is) = transpose is
applyOp (Rev rs) = rev rs
applyOp (Slice sl) = slice sl
applyOp (Stride ts) = stride ts
applyOp (Window ws) = window ws
applyOp (Index i) = (`index` i)
applyOp (Broadcast ds sh) = broadcast ds sh

-- An operation valid on an array of the given shape.
genOp :: [Int] -> Gen Op
genOp sh = oneof $
  [ Transpose <$> shuffle [0 .. r - 1]
  , Rev <$> sublistOf [0 .. r - 1]
  , Slice <$> mapM (\ s -> do k <- choose (0, s); n <- choose (0, s - k); return (k, n)) sh
  , Stride <$> mapM (const (choose (1, 3))) sh
  , do e <- choose (0, 2)
       ds <- sort . take r <$> shuffle [0 .. r + e - 1]
       extra <- vectorOf e (choose (0, 3))
       let fill i ss xs | i `elem` ds, s : ss' <- ss = s : fill (i + 1) ss' xs
                        | x : xs' <- xs = x : fill (i + 1) ss xs'
                        | otherwise = []
       return (Broadcast ds (fill (0 :: Int) sh extra))
  ] ++
  [ Window . (: []) <$> choose (1, s) | s : _ <- [sh], s > 0 ] ++
  [ Index <$> choose (0, s - 1) | s : _ <- [sh], s > 0 ]
  where r = length sh

-- n operations, each valid on the shape the ones before it leave.
genOps :: Int -> [Int] -> Gen [Op]
genOps 0 _ = return []
genOps n sh = do
  op <- genOp sh
  (op :) <$> genOps (n - 1) (shapeL (applyOp op (constant sh ())))

-- A view: the shape of an array made by fromList and the operations to
-- apply to it.  A prefix of the operations is a view too.
data View = View [Int] [Op]
  deriving Show

instance Arbitrary View where
  arbitrary = do
    sh <- genShape 3
    n <- choose (0, 4)
    View sh <$> genOps n sh
  shrink (View sh ops) = [ View sh (take i ops) | i <- [0 .. length ops - 1] ]

mkView :: View -> [a] -> Array a
mkView (View sh ops) xs = foldl (flip applyOp) (fromList sh xs) ops

-- The view over the vector of its indices, with the elements outside
-- the view failing when forced.
mkViewOnly :: View -> Array Int
mkViewOnly v@(View sh _) =
  let n = product sh
      is = toList (mkView v [0 .. n - 1])
  in  mkView v [ if i `elem` is then i else error "outside the view" | i <- [0 .. n - 1] ]

-- A view built directly: a shape, strides and an offset whose indices fit
-- in a vector of the given length, often exactly as long as the view.
data RawView = RawView [Int] [Int] Int Int
  deriving Show

instance Arbitrary RawView where
  arbitrary = do
    sh <- genShape 3
    ts <- vectorOf (length sh) (choose (-4, 4))
    let lo = sum [ (s - 1) * t | (s, t) <- zip sh ts, s > 0, t < 0 ]
        hi = sum [ (s - 1) * t | (s, t) <- zip sh ts, s > 0, t > 0 ]
    exact <- arbitrary
    slack <- choose (0, 2)
    let n = if exact then max (hi - lo + 1) (product sh) else hi - lo + 1 + slack
    pre <- choose (0, n - (hi - lo + 1))
    return (RawView sh ts (pre - lo) n)

-- readRangeT finds the part of the vector a view reads where it reads every
-- element of one part, and nothing where it reads none or skips one.
prop_readRangeT :: RawView -> View -> Property
prop_readRangeT (RawView rsh ts o n) v@(View sh _) =
  let rt = I.T ts o (V.fromList [0 .. n - 1])
      x = mkView v [0 .. product sh - 1] :: Array Int
      range is = case sort (nub is) of
        js@(j : _) | js == [j .. j + length js - 1] -> Just (j, length js)
        _ -> Nothing
  in  I.readRangeT rsh rt === range (I.toListT rsh rt)
      .&&. (case x of D.A (DG.A sh' t) -> I.readRangeT sh' t) === range (toList x)

-- == agrees with comparing the lists, on the view against itself, the view
-- mapped and the view normalized, and compares no element outside the views.
prop_eq :: View -> Property
prop_eq v =
  let x = mkViewOnly v
      y = mapA (`div` 2) x
  in  (x == x) === True .&&. (x == y) === (toList x == toList y)
      .&&. (x == normalize x) === True

-- mapA agrees with map on the list, and does not apply its function to
-- the elements outside the view, which a strict vector would force.
prop_mapA :: View -> Property
prop_mapA v =
  let x = mkViewOnly v
      y = mapA (* 2) x
  in  toList y === map (* 2) (toList x)
      .&&. (case y of D.A (DG.A _ t) -> V.sum (I.values t) >= 0)

