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

{-# LANGUAGE DataKinds #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeOperators #-}
module ShapedTest(test) where

import Control.DeepSeq
import Control.Exception
import Data.Array.Convert (convertE)
import qualified Data.Array.Dynamic as D
import Data.Array.Shape (withShape, withShapeP)
import Data.Array.Shaped
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.ShapedG as SG
import qualified Data.Vector as V
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.HUnit (assertEqual, assertFailure, Assertion)

assertThrows :: (NFData a) => String -> a -> Assertion
assertThrows s a = catch (deepseq a $ assertFailure s) (\ (_ :: ErrorCall) -> return ())

assertThrowsIn :: (NFData a) => String -> String -> a -> Assertion
assertThrowsIn s f a = catch (deepseq a $ assertFailure s)
                             (\ (ErrorCall e) -> assertEqual s f (takeWhile (/= ':') e))

test :: Test
test = testGroup "Shaped" $
  let a1, a1' :: Array [2,3] Int
      a1 = fromList [1..6]
      a1' = fromList [2..7]
      a2 :: Array [3,2] Int
      a2 = fromList [1,4,2,5,3,6]
      show_1 = assertEqual "1" "fromList @[2,3] [1,2,3,4,5,6]" (show a1)
      show_2 = assertEqual "2" "fromList @[3,2] [1,4,2,5,3,6]" (show a2)
      eq_1 = assertEqual "1" True (a1 == a1)
      eq_2 = assertEqual "2" False (a1 == a1')
      ord_1 = assertEqual "1" EQ (a1 `compare` a1)
      ord_2 = assertEqual "2" LT (a1 `compare` a1')
      shapeL_1 = assertEqual "1" [2,3] (shapeL a1)
      shapeL_2 = assertEqual "2" [3,2] (shapeL a2)
      rank_1 = assertEqual "1" 2 (rank a1)
      rank_2 = assertEqual "2" 2 (rank a2)
      index_1 = assertEqual "1" (fromList [1,2,3]) (index a1 0)
      index_2 = assertEqual "2" (fromList [1,4]) (index a2 0)
      index_3 = assertEqual "3" (fromList [4]) (a2 `index` 0 `index` 1)
      index_4 = assertThrows "<0" (index a1 (-1))
      index_5 = assertThrows ">" (index a1 2)
      index_6 = catch (deepseq (index a1 (-1)) $ assertFailure "6")
                      (\ (ErrorCall e) -> assertEqual "6" "index: out of bounds (-1,2)" e)
      -- stretchOuter need not know the extent it stretches to nor the shape
      -- below it, and ShapedG's show need not know how to show a vector.
      constraints_1 = assertEqual "1" (stretchOuter b :: Array [2,3] Int, show a1)
                                      (stretchOuterN b, showG (SG.fromList [1..6] :: SG.Array [2,3] [] Int))
        where b = fromList [1,2,3] :: Array [1,3] Int
              stretchOuterN :: Array (1 : sh) Int -> Array (s : sh) Int
              stretchOuterN = stretchOuter
              showG :: (Show a, I.Vector v, I.VecElem v a, Shape sh) => SG.Array sh v a -> String
              showG = show
      toList_1 = assertEqual "1" [1,2,3,4,5,6] (toList a1)
      toList_2 = assertEqual "2" [1,4,2,5,3,6] (toList a2)
      toVector_1 = assertEqual "1" (V.fromList [1,2,3,4,5,6]) (toVector a1)
      toVector_2 = assertEqual "2" (V.fromList [1,4,2,5,3,6]) (toVector a2)
      fromList_1 = assertThrows "sh" (fromList [1,2] :: Array '[] Int)
      fromList_2 = assertThrows "sh" (fromList [1,2] :: Array [4,5] Int)
      -- Shapes with an extent or a size past maxBound, the extent below
      -- 2^64: fromList at '[2^64+3] made GHC 9.14.1 panic, not 10.1.20260918.
      -- TODO: try '[2^64+3] on GHC 9.14.2 once it is out, and if it still
      -- panics, report it to GHC.
      fromList_3 = assertThrowsIn "3" "Shape" (fromList [] :: Array [4294967296, 4294967296] Int)
      fromList_4 = assertThrowsIn "4" "Shape" (fromList [1,2,3] :: Array '[9223372036854775811] Int)
      fromVector_1 = assertEqual "1" a1 (fromVector $ V.fromList [1..6])
      normalize_1 = assertEqual "1" a1 (normalize a1)
      reshape_1 = assertEqual "1" (fromList [1..6] :: Array '[6] Int) (reshape a1)
      reshape_2 = assertEqual "1" (fromList [1,4,2,5,3,6]) (reshape a2 :: Array [1,2,3,1] Int)
      a3 :: Array '[1] Int
      a3 = fromList [5]
      a4 :: Array '[] Int
      a4 = fromList [5]
      stretch_1 = assertEqual "1" (fromList @'[3] [5,5,5]) (stretch @'[3] a3)
      stretch_2 = assertEqual "2" (fromList @[2,2,3,2] [1,1,2,2,3,3,4,4,5,5,6,6,1,1,2,2,3,3,4,4,5,5,6,6])
                                  (stretch @[2,2,3,2] (reshape @[1,2,3,1] a1))
      stretch_3 = assertThrowsIn "3" "Shape" (stretch @[4294967296, 4294967296] (fromList [7] :: Array [1,1] Int))

      scalar_1 = assertEqual "1" a4 (scalar 5)
      unScalar_1 = assertEqual "1" 5 (unScalar a4)
      constant_1 = assertEqual "1" (fromList [1,1,1,1,1,1]) (constant 1 :: Array [2,3] Int)
      constant_2 = assertThrowsIn "2" "Shape" (constant 0 :: Array [4294967296, 4294967296] Int)
      generate_1 = assertThrowsIn "1" "Shape" (generate (const 0) :: Array [4294967296, 4294967296] Int)
      broadcast_1 = assertEqual "1" [1,1,2,2,3,3] (toList (broadcast @'[0] @'[3,2] (index a1 0)))
      broadcast_2 = assertEqual "2" [7,7,7,7,7,7]
                                    (toList (broadcast @'[1] @'[2,3] (constant 7 :: Array '[3] Int)))
      broadcast_3 = assertEqual "3" [1,2,3,1,2,3]
                                    (toList (broadcast @'[1] @'[2,3] (fromList [1,2,3] :: Array '[3] Int)))
      mapA_1 = assertEqual "1" (fromList [2..7]) (mapA succ a1)
      mapA_2 = assertEqual "1" (fromList [2,5,3,6,4,7]) (mapA succ a2)
      zipWithA_1 = assertEqual "1" (fromList [2,4..12]) (zipWithA (+) a1 a1)
      zipWith3A_1 = assertEqual "1" (fromList [2,6,12,20,30,42]) (zipWith3A (\ x y z -> x*y+z) a1 a1 a1)
      pad_1 = assertEqual "1" (fromList [9,9,9,9,9,9,9,9,9,9,
                                         9,9,9,1,2,3,9,9,9,9,
                                         9,9,9,4,5,6,9,9,9,9,
                                         9,9,9,9,9,9,9,9,9,9,
                                         9,9,9,9,9,9,9,9,9,9])
                              (pad @['(1,2), '(3,4)] 9 a1)
      -- A padded size past maxBound.
      pad_2 = assertThrowsIn "2" "pad" (pad @['(0,0), '(0,4294967294)] 0 (constant 7 :: Array [4294967296, 2] Int) :: Array [4294967296, 4294967296] Int)
      a5 :: Array '[2,3,4] Int
      a5 = fromList [1..24]
      transpose_1 = assertEqual "1" (fromList [1,2,3,4,
                                               5,6,7,8,
                                               9,10,11,12,

                                               13,14,15,16,
                                               17,18,19,20,
                                               21,22,23,24])
                                    (transpose @'[0,1,2] a5)
      transpose_2 = assertEqual "2" (fromList [1,5,9,
                                               2,6,10,
                                               3,7,11,
                                               4,8,12,

                                               13,17,21,
                                               14,18,22,
                                               15,19,23,
                                               16,20,24])
                                    (transpose @'[0,2,1] a5)
      transpose_3 = assertEqual "3" (fromList [1,2,3,4,
                                               13,14,15,16,

                                               5,6,7,8,
                                               17,18,19,20,

                                               9,10,11,12,
                                               21,22,23,24])
                                    (transpose @'[1,0,2] a5)
      transpose_4 = assertEqual "4" (fromList [1,13,
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
                                    (transpose @'[1,2,0] a5)
      transpose_5 = assertEqual "5" (fromList [1,5,9,
                                               13,17,21,

                                               2,6,10,

                                               14,18,22,

                                               3,7,11,
                                               15,19,23,

                                               4,8,12,
                                               16,20,24])
                                    (transpose @'[2,0,1] a5)
      transpose_6 = assertEqual "6" (fromList [1,13,
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
                                    (transpose @'[2,1,0] a5)
      transpose_9 = assertEqual "9" (fromList [1,2,3,4,
                                               13,14,15,16,

                                               5,6,7,8,
                                               17,18,19,20,

                                               9,10,11,12,
                                               21,22,23,24])
                                    (transpose @'[1,0] a5)
      append_1 = assertEqual "1" (fromList [1..9])
                                 (append a1 (fromList @[1,3] [7,8,9]))
      ravel_1 = assertEqual "1" (fromList @[3,2,3] [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6])
                                (ravel $ fromList @'[3] [a1,a1,a1])
      unravel_1 = assertEqual "1" [a1,a1,a1]
                                  (toList $ unravel $ ravel $ fromList @'[3] [a1,a1,a1])
      a6 :: Array [4,5] Int
      a6 = fromList [1..20]
      window_1 = assertEqual "1" (fromList @[2,3,3,3] [1,2,3,
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
                                 (window @[3,3] a6)
      stride_1 = assertEqual "1" (fromList @[2,2,2] [1,3,
                                                    9,11,

                                                    13,15,
                                                    21,23])
                                 (stride @[1,2,2] a5)
      slice_1 = assertEqual "1" (fromList @[2,2,1] [8,12,20,24])
                                (slice @['(0,2), '(1,2), '(3,1)] a5)
      box = scalar . Just
      rerank_1 = assertEqual "1" (box a5)
                                 (rerank @0 box a5)
      rerank_2 = assertEqual "2" (fromList [Just $ fromList @[3,4] [1,2,3,4,5,6,7,8,9,10,11,12],
                                            Just $ fromList @[3,4] [13,14,15,16,17,18,19,20,21,22,23,24]])
                                 (rerank @1 box a5)
      rerank_3 = assertEqual "3" (fromList @[2,3] [Just $ fromList [1,2,3,4],
                                                   Just $ fromList [5,6,7,8],
                                                   Just $ fromList [9,10,11,12],
                                                   Just $ fromList [13,14,15,16],
                                                   Just $ fromList [17,18,19,20],
                                                   Just $ fromList [21,22,23,24]])
                                 (rerank @2 box a5)
      rerank_4 = assertEqual "4" (mapA (Just . scalar) a5)
                                 (rerank @3 box a5)
      a7 = mapA succ a5
      dot x y = reduce (+) 0 $ zipWithA (*) x y
      rerank2_1 = assertEqual "1" (fromList [40,200,488,904,1448,2120])
                                  (rerank2 @2 dot a5 a7)
      rev_1 = assertEqual "1" (fromList [3,2,1,6,5,4])
                              (rev @'[1] a1)
      rev_2 = assertEqual "2" (fromList [6,5,4,3,2,1])
                              (rev @[0,1] a1)
      withShapeP_1 = assertThrowsIn "1" "withShapeP" (withShapeP [-1] (\ _ -> ()))
      withShape_1 = assertThrowsIn "1" "withShape" (withShape [-1] ())
      convertE_1 = assertEqual "1" (Left "convert: shape mismatch") (convertE (D.fromList [2] [1,2 :: Int]) :: Either String (Array '[3] Int))
      reduce_1 = assertEqual "1" (scalar 720) (reduce (*) 1 a1)
      reduce_2 = assertEqual "2" (fromList @'[2] [6,120]) (rerank @1 (reduce (*) 1) a1)
      reduce_3 = assertEqual "3" (fromList @'[3] [4,10,18]) (rerank @1 (reduce (*) 1) a2)

      -- One call of each reduction wrapper that the other tests of
      -- ShapedTest, ShapedSTest or ShapedUTest leave uncalled.
      wrappers_1 = do
        assertEqual "sumA" 21 (sumA a1)
        assertEqual "productA" 720 (productA a1)
        assertEqual "maximumA" 6 (maximumA a1)
        assertEqual "minimumA" 1 (minimumA a1)
        assertEqual "anyA" True (anyA (> 5) a1)
        assertEqual "allA" False (allA (> 1) a1)
        assertEqual "allSameA" False (allSameA a1)

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
        , testCase "index_6" index_6
        , testCase "constraints_1" constraints_1
        , testCase "toList_1" toList_1
        , testCase "toList_2" toList_2
        , testCase "toVector_1" toVector_1
        , testCase "toVector_2" toVector_2
        , testCase "fromList_1" fromList_1
        , testCase "fromList_2" fromList_2
        , testCase "fromList_3" fromList_3
        , testCase "fromList_4" fromList_4
        , testCase "fromVector_1" fromVector_1
        , testCase "normalize_1" normalize_1
        , testCase "reshape_1" reshape_1
        , testCase "reshape_2" reshape_2
        , testCase "stretch_1" stretch_1
        , testCase "stretch_2" stretch_2
        , testCase "stretch_3" stretch_3
        , testCase "scalar_1" scalar_1
        , testCase "unScalar_1" unScalar_1
        , testCase "constant_1" constant_1
        , testCase "constant_2" constant_2
        , testCase "generate_1" generate_1
        , testCase "broadcast_1" broadcast_1
        , testCase "broadcast_2" broadcast_2
        , testCase "broadcast_3" broadcast_3
        , testCase "mapA_1" mapA_1
        , testCase "mapA_2" mapA_2
        , testCase "zipWithA_1" zipWithA_1
        , testCase "zipWith3A_1" zipWith3A_1
        , testCase "pad_1" pad_1
        , testCase "pad_2" pad_2
        , testCase "transpose_1" transpose_1
        , testCase "transpose_2" transpose_2
        , testCase "transpose_3" transpose_3
        , testCase "transpose_4" transpose_4
        , testCase "transpose_5" transpose_5
        , testCase "transpose_6" transpose_6
        , testCase "transpose_9" transpose_9
        , testCase "append_1" append_1
        , testCase "ravel_1" ravel_1
        , testCase "unravel_1" unravel_1
        , testCase "window_1" window_1
        , testCase "stride_1" stride_1
        , testCase "slice_1" slice_1
        , testCase "rerank_1" rerank_1
        , testCase "rerank_2" rerank_2
        , testCase "rerank_3" rerank_3
        , testCase "rerank_4" rerank_4
        , testCase "rerank2_1" rerank2_1
        , testCase "rev_1" rev_1
        , testCase "rev_2" rev_2
        , testCase "withShapeP_1" withShapeP_1
        , testCase "withShape_1" withShape_1
        , testCase "convertE_1" convertE_1
        , testCase "reduce_1" reduce_1
        , testCase "reduce_2" reduce_2
        , testCase "reduce_3" reduce_3
        , testCase "wrappers_1" wrappers_1
        ]
  in  tests
