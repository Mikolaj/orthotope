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
module DynamicUTest(test) where

import Control.Exception
import Data.Array.Convert (convert)
import qualified Data.Array.Dynamic as D
import Data.Array.DynamicU
import qualified Data.Array.Internal.DynamicU as DU
import Data.IORef (IORef, mkWeakIORef, newIORef)
import Data.Maybe (isJust)
import qualified Data.Vector.Unboxed as V
import Data.Word (Word8)
import System.Mem (performMajorGC)
import System.Mem.Weak (Weak, deRefWeak)
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.HUnit (assertEqual, assertFailure)
import Test.QuickCheck (Property, forAll, (.&&.), (===))
import Views (View (..), assertThrowsIn, genElems, mkViewG, testPropertyN)

test :: Test
test = testGroup "DynamicU" $
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
      index_4 = assertThrowsIn "<0" "index" (index a1 (-1))
      index_5 = assertThrowsIn ">" "index" (index a1 2)
      -- index need not know that the elements are Unboxed.
      constraints_1 = assertEqual "1" (index a1 1) (indexN a1 1)
        where indexN :: Array a -> Int -> Array a
              indexN a i = index a i
      toList_1 = assertEqual "1" [1,2,3,4,5,6] (toList a1)
      toList_2 = assertEqual "2" [1,4,2,5,3,6] (toList a2)
      toVector_1 = assertEqual "1" (V.fromList [1,2,3,4,5,6]) (toVector a1)
      toVector_2 = assertEqual "2" (V.fromList [1,4,2,5,3,6]) (toVector a2)
      fromList_1 = assertThrowsIn "sh" "fromList" (fromList [] [1,2::Int])
      fromList_2 = assertThrowsIn "sh" "fromList" (fromList [4,5] [1,2::Int])
      fromVector_1 = assertEqual "1" a1 (fromVector [2,3] $ V.fromList [1..6])
      fromVector_2 = assertThrowsIn "2" "fromVector" (fromVector [2,3] $ V.fromList [1..5::Int])
      normalize_1 = assertEqual "1" a1 (normalize a1)
      reshape_1 = assertEqual "1" (fromList [6] [1..6]) (reshape [6] a1)
      reshape_2 = assertEqual "2" (fromList [1,2,3,1] [1,4,2,5,3,6]) (reshape [1,2,3,1] a2)
      a3, a4 :: Array Int
      a3 = fromList [1] [5]
      a4 = fromList [] [5]
      stretch_1 = assertEqual "1" (fromList [3] [5,5,5]) (stretch [3] a3)
      stretch_2 = assertEqual "2" (fromList [2,2,3,2] [1,1,2,2,3,3,4,4,5,5,6,6,1,1,2,2,3,3,4,4,5,5,6,6])
                                  (stretch [2,2,3,2] $ reshape [1,2,3,1] a1)
      stretch_3 = assertThrowsIn "3" "stretch" (stretch [1,2] a3)
      stretch_4 = assertThrowsIn "4" "stretch" (stretch [4,3] a1)
      scalar_1 = assertEqual "1" a4 (scalar 5)
      unScalar_1 = assertEqual "1" 5 (unScalar a4)
      unScalar_2 = assertThrowsIn "2" "unScalar" (unScalar a3)
      constant_1 = assertEqual "1" (fromList [2,3] [1,1,1,1,1,1]) (constant [2,3] (1::Int))
      iota_1 = assertEqual "1" (map fromIntegral [0..299::Int]) (toList (iota 300 :: Array Word8))
      mapA_1 = assertEqual "1" (fromList [2,3] [2..7]) (mapA succ a1)
      mapA_2 = assertEqual "2" (fromList [3,2] [2,5,3,6,4,7]) (mapA succ a2)
      zipWithA_1 = assertEqual "1" (fromList [2,3] [2,4..12]) (zipWithA (+) a1 a1)
      zipWithA_2 = assertThrowsIn "2" "zipWithA" (zipWithA (+) a1 a2)
      zipWith3A_1 = assertEqual "1" (fromList [2,3] [2,6,12,20,30,42]) (zipWith3A (\ x y z -> x*y+z) a1 a1 a1)
      pad_1 = assertEqual "1" (fromList [5,10] [9,9,9,9,9,9,9,9,9,9,
                                                9,9,9,1,2,3,9,9,9,9,
                                                9,9,9,4,5,6,9,9,9,9,
                                                9,9,9,9,9,9,9,9,9,9,
                                                9,9,9,9,9,9,9,9,9,9])
                              (pad [(1,2),(3,4)] 9 a1)
      pad_2 = assertThrowsIn "2" "pad" (pad [(1,1),(1,1),(1,1)] 0 a1)
      -- pad writes a padding of -0.0 by primitive-0.9.1.0's setByteArray,
      -- which writes it as +0.0.
      -- TODO: turn pad_3 back on, and drop the sentence on -0.0 from the pad
      -- haddocks of DynamicU, RankedU and ShapedU, once a primitive release has
      -- https://github.com/haskell/primitive/pull/433.
      -- pad_3 = assertEqual "3" [True, True, False, True]
      --           (map isNegativeZero (toList (pad [(2, 1)] (-0.0) (fromList [1] [1.5 :: Double]))))
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
      transpose_7 = assertThrowsIn "7" "transpose" (transpose [0,1,2,3] a5)
      transpose_8 = assertThrowsIn "8" "transpose" (transpose [0,1,3] a5)
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
      concatOuter_2 = assertThrowsIn "2" "concatOuter" (concatOuter [a1, a2])
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
      window_2 = assertThrowsIn "2" "window" (window [3,6] a6)
      window_3 = assertThrowsIn "3" "window" (window [3,3,3] a6)
      stride_1 = assertEqual "1" (fromList [2,2,2] [1,3,
                                                    9,11,

                                                    13,15,
                                                    21,23])
                                 (stride [1,2,2] a5)
      stride_2 = assertThrowsIn "2" "stride" (stride [1,2,2] a1)
      stride_3 = assertThrowsIn "3" "stride" (stride [0] a1)
      stride_4 = assertThrowsIn "4" "stride" (stride [-1] a1)
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
      slice_1 = assertEqual "1" (fromList [2,2,1] [8,12,20,24])
                                (slice [(0,2),(1,2),(3,1)] a5)
      slice_2 = assertThrowsIn "2" "slice" (slice [(0,0)] a4)
      slice_3 = assertThrowsIn "3" "slice" (slice [(-1,1)] a5)
      slice_4 = assertThrowsIn "4" "slice" (slice [(10,0)] a5)
      slice_5 = assertThrowsIn "5" "slice" (slice [(0,3)] a5)
      a7 = mapA succ a5
      dot x y = reduce (+) 0 $ zipWithA (*) x y
      rerank2_1 = assertEqual "1" (fromList [2,3] [40,200,488,904,1448,2120])
                                  (rerank2 2 dot a5 a7)
      rev_1 = assertEqual "1" (fromList [2,3] [3,2,1,6,5,4])
                              (rev [1] a1)
      rev_2 = assertEqual "2" (fromList [2,3] [6,5,4,3,2,1])
                              (rev [0,1] a1)
      rev_3 = assertThrowsIn "3" "rev" (rev [2] a1)
      reduce_1 = assertEqual "1" (scalar 720) (reduce (*) 1 a1)
      reduce_2 = assertEqual "2" (fromList [2] [6,120]) (rerank 1 (\ r -> reduce (*) 1 r) a1)
      reduce_3 = assertEqual "3" (fromList [3] [4,10,18]) (rerank 1 (\ r -> reduce (*) 1 r) a2)
      -- An empty view at the end of a longer vector, so that reading the
      -- element at the offset fails under the bounds checks.
      allSameA_1 = assertEqual "1" True (allSameA (slice [(2,0)] a1))
      -- As allSame . toList, comparing the first element with the others only.
      allSameA_2 = assertEqual "2" [True, False, False, False, True]
                                   (map (\ a -> allSameA a) [ fromList [1] [nan], fromList [2] [nan, nan]
                                                 , constant [3] nan, normalize (constant [3] nan)
                                                 , slice [(0,1)] (fromList [2] [nan, 1]) ])
        where nan = 0 / 0 :: Double
      -- vector's DoNotUnboxLazy stores its elements unevaluated, and an
      -- operation that does not use one leaves it so, on a dense view and on
      -- a transposed one alike.
      lazyElems_1 = do
        assertEqual "mapA" [0, 0] (toList (mapA (\ _ -> 0 :: Int) lz))
        assertEqual "zipWithA" [5, 6] (toList (zipWithA (\ _ b -> b) lz five))
        assertEqual "zipWith3A" [5, 6] (toList (zipWith3A (\ _ _ c -> c) lz lz five))
        assertEqual "toList" 4 (length (toList lzT))
        assertEqual "foldrA" 4 (foldrA (\ _ n -> n + 1 :: Int) 0 lzT)
        assertEqual "anyA" True (anyA (const True) lzT)
        where lz = fromList [2] (map V.DoNotUnboxLazy [undefined, 1 :: Int])
              lzT = transpose [1, 0] (fromList [2, 2] (map V.DoNotUnboxLazy [undefined, 1, 2, 3 :: Int]))
              five = fromList [2] [5, 6 :: Int]
      -- An unforced element of a DoNotUnboxLazy result holds the elements its
      -- function reads, not the vectors they are read from, as vector's own
      -- map and zipWith store it: with the second element of the result
      -- forced, nothing holds the second element of the source.
      lazyElems_2 = do
        m <- retains (\ a -> mapA (\ (V.DoNotUnboxLazy r) -> V.DoNotUnboxLazy (r `seq` 0)) a)
        z <- retains (\ a -> zipWithA (\ (V.DoNotUnboxLazy r) _ -> V.DoNotUnboxLazy (r `seq` 0)) a a)
        assertEqual "the second source element held, after mapA and zipWithA" (False, False) (m, z)
        where
          retains :: (Array (V.DoNotUnboxLazy (IORef Int)) -> Array (V.DoNotUnboxLazy Int)) -> IO Bool
          retains op = heldAfterGC (make op)
          -- NOINLINE, so that what make allocates stays reachable only
          -- through what it returns.
          {-# NOINLINE make #-}
          make op = do
            r0 <- newIORef 0
            r1 <- newIORef 1
            w <- mkWeakIORef r1 (return ())
            b <- evaluate (op (fromList [2] [V.DoNotUnboxLazy r0, V.DoNotUnboxLazy r1]))
            case toList b of
              [_, V.DoNotUnboxLazy y] -> () <$ evaluate y
              _ -> assertFailure "two elements"
            return (b, w)

      -- So does a zip of views whose vectors hold one element each, here a row
      -- of a longer vector: with the result unforced, nothing holds the
      -- source's first element, outside the row.
      lazyElems_3 = do
        held <- heldAfterGC make
        assertEqual "the first source element held, after zipWithA" False held
        where
          -- NOINLINE, so that what make allocates stays reachable only
          -- through what it returns.
          {-# NOINLINE make #-}
          make :: IO (Array (V.DoNotUnboxLazy (IORef Int)), Weak (IORef Int))
          make = do
            r0 <- newIORef 0
            r1 <- newIORef 1
            w <- mkWeakIORef r0 (return ())
            let a = normalize (index (fromList [2, 1] [V.DoNotUnboxLazy r0, V.DoNotUnboxLazy r1]) 1)
            b <- evaluate (zipWithA const a a)
            return (b, w)
      -- A copy of a view broadcast along its innermost dimension forces its
      -- element, as README's Evaluation section says: here a copy by force,
      -- append, concatOuter, ravel and rerank.
      lazyElems_4 = do
        assertThrowsIn "force" "U" (force b)
        assertThrowsIn "append" "U" (append b dense)
        assertThrowsIn "concatOuter" "U" (concatOuter [b, dense])
        assertThrowsIn "ravel" "U" (ravel (D.fromList [2] [b, b]))
        assertThrowsIn "rerank" "U" (rerank 1 id b)
        where b = stretch [2, 4] (reshape [1, 1] (fromList [1] [V.DoNotUnboxLazy (error "U" :: Int)]))
              dense = fromList [1, 4] (map V.DoNotUnboxLazy [1, 2, 3, 4 :: Int])

      -- Calls of every wrapper the module under test exports, in the order of
      -- its export list, each against its value.
      wrappers_1 = do
        assertEqual "size" 6 (size a1)
        assertEqual "shapeL" [2, 3] (shapeL a1)
        assertEqual "rank" 2 (rank a1)
        assertEqual "toList" [1 .. 6] (toList a1)
        assertEqual "fromList" [7, 8, 9]
                    (toList (fromList [3] [7, 8, 9] :: Array Int))
        assertEqual "toVector" (V.fromList [1 .. 6]) (toVector a1)
        assertEqual "fromVector" a1 (fromVector [2, 3] (V.fromList [1 .. 6]))
        assertEqual "normalize" (fromList [3, 2] [1, 4, 2, 5, 3, 6])
                    (normalize (transpose [1, 0] a1))
        assertEqual "force" (fromList [3, 2] [1, 4, 2, 5, 3, 6])
                    (force (transpose [1, 0] a1))
        assertEqual "scalar" (fromList [] [5]) (scalar (5 :: Int))
        assertEqual "unScalar" 5 (unScalar (index (index a1 1) 1))
        assertEqual "constant" (fromList [2, 2] [7, 7, 7, 7])
                    (constant [2, 2] (7 :: Int))
        assertEqual "reshape" (fromList [3, 2] [1 .. 6])
                    (reshape [3, 2] a1)
        assertEqual "stretch" (fromList [2, 3] [1, 2, 3, 1, 2, 3])
                    (stretch [2, 3] (slice [(0, 1)] a1))
        assertEqual "stretchOuter" (fromList [2, 3] [1, 2, 3, 1, 2, 3])
                    (stretchOuter 2 (slice [(0, 1)] a1))
        assertEqual "transpose" (fromList [3, 2] [1, 4, 2, 5, 3, 6])
                    (transpose [1, 0] a1)
        assertEqual "index" (fromList [3] [4, 5, 6]) (index a1 1)
        assertEqual "pad" (fromList [2, 5] [0, 1, 2, 3, 0, 0, 4, 5, 6, 0])
                    (pad [(0, 0), (1, 1)] 0 a1)
        assertEqual "mapA" (fromList [2, 3] [2 .. 7]) (mapA (+ 1) a1)
        assertEqual "zipWithA" (fromList [2, 3] [2, 4 .. 12])
                    (zipWithA (+) a1 a1)
        assertEqual "zipWith3A" (fromList [2, 3] [3, 6 .. 18])
                    (zipWith3A (\ a b c -> a + b + c) a1 a1 a1)
        assertEqual "zipWith4A" (fromList [2, 3] [4, 8 .. 24])
                    (zipWith4A (\ a b c d -> a + b + c + d) a1 a1 a1 a1)
        assertEqual "zipWith5A" (fromList [2, 3] [5, 10 .. 30])
                    (zipWith5A (\ a b c d e -> a + b + c + d + e)
                               a1 a1 a1 a1 a1)
        assertEqual "append" (fromList [4, 3] [1, 2, 3, 4, 5, 6,
                                               1, 2, 3, 4, 5, 6])
                    (append a1 a1)
        assertEqual "concatOuter" (fromList [6] [4, 5, 6, 1, 2, 3])
                    (concatOuter [index a1 1, index a1 0])
        assertEqual "ravel" (fromList [2, 3] [4, 5, 6, 1, 2, 3])
                    (ravel (D.fromList [2] [index a1 1, index a1 0]))
        assertEqual "unravel" (D.fromList [2] [fromList [3] [1, 2, 3],
                                               fromList [3] [4, 5, 6]])
                    (unravel a1)
        assertEqual "ravel . unravel" a1 (ravel (unravel a1))
        assertEqual "window" (fromList [2, 2] [1, 2, 2, 3])
                    (window [2] (index a1 0))
        assertEqual "stride" (fromList [2, 2] [1, 3, 4, 6]) (stride [1, 2] a1)
        assertEqual "rotate" (fromList [2, 3] [2, 3, 1, 1, 2, 3])
                    (rotate 0 2 (index a1 0))
        assertEqual "slice" (fromList [2, 2] [2, 3, 5, 6])
                    (slice [(0, 2), (1, 2)] a1)
        assertEqual "rerank" (fromList [2] [6, 15])
                    (rerank 1 (\ r -> reduce (+) 0 r) a1)
        assertEqual "rerank2" (fromList [2] [14, 77]) (rerank2 1 dot a1 a1)
        assertEqual "rev" (fromList [2, 3] [4, 5, 6, 1, 2, 3]) (rev [0] a1)
        assertEqual "reduce" (fromList [] [21]) (reduce (+) 0 a1)
        assertEqual "foldrA" [1 .. 6] (foldrA (:) [] a1)
        assertEqual "traverseA" (Just (fromList [2, 3] [2 .. 7]))
                    (traverseA (Just . (+ 1)) a1)
        assertEqual "allSameA" False (allSameA a1)
        assertEqual "sumA" 21 (sumA a1)
        assertEqual "productA" 720 (productA a1)
        assertEqual "maximumA" 6 (maximumA a1)
        assertEqual "minimumA" 1 (minimumA a1)
        assertEqual "anyA" True (anyA (> 5) a1)
        assertEqual "allA" False (allA (> 1) a1)
        assertEqual "broadcast" (fromList [2, 3] [1, 2, 3, 1, 2, 3])
                    (broadcast [1] [2, 3] (index a1 0))
        assertEqual "update" (fromList [2, 3] [9, 2, 3, 4, 5, 6])
                    (update a1 [([0, 0], 9)])
        assertEqual "generate" (fromList [2, 3] [0 .. 5])
                    (generate [2, 3] (sum . zipWith (*) [3, 1]))
        assertEqual "iterateN" (fromList [3] [1, 2, 4])
                    (iterateN 3 (* 2) (1 :: Int))
        assertEqual "iota" (fromList [3] [0, 1, 2]) (iota 3 :: Array Int)

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
        , testCase "zipWithA_1" zipWithA_1
        , testCase "zipWithA_2" zipWithA_2
        , testCase "zipWith3A_1" zipWith3A_1
        , testCase "pad_1" pad_1
        , testCase "pad_2" pad_2
        -- , testCase "pad_3" pad_3  -- TODO: back on with pad_3
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
        , testCase "rotate_1" rotate_1
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
        , testCase "lazyElems_1" lazyElems_1
        , testCase "lazyElems_2" lazyElems_2
        , testCase "lazyElems_3" lazyElems_3
        , testCase "lazyElems_4" lazyElems_4
        , testCase "wrappers_1" wrappers_1
        ]
  in  tests ++ [testPropertyN "prop_convert" prop_convert]

-- Whether the weak pointer the action returns still finds its key after a
-- major collection, the array the action returns kept past the collection.
heldAfterGC :: Unbox a => IO (Array a, Weak k) -> IO Bool
heldAfterGC make = do
  (b, w) <- make
  performMajorGC
  held <- isJust <$> deRefWeak w
  _ <- evaluate (length (toList b))  -- the result kept past the collection
  return held

mkView :: Unbox a => View -> [a] -> Array a
mkView v = DU.A . mkViewG v

-- convert of a view to the boxed module and back keeps its shape and its
-- elements in order.
prop_convert :: View -> Property
prop_convert v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  let x = mkView v xs :: Array Int
      d = convert x :: D.Array Int
  in  D.shapeL d === shapeL x .&&. D.toList d === toList x
      .&&. convert d === x
