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

-- Random views and other helpers for the properties of the test modules.
module Views(testPropertyN, failsWith, failsIn, Elem, genElems, upTo, genShape, Op(..), opShape
            , opSource, genBadOp, opNames, silentBadOp, View(..), mkView, applyOpG
            , mkViewG, genRawView) where

import Control.DeepSeq (NFData)
import Control.Exception (ErrorCall (..), evaluate, try)
import Data.Array.Dynamic
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.Dynamic as DI
import qualified Data.Array.Internal.DynamicG as DG
import Data.List (sort)
import Data.Word (Word8)
import Test.Framework (Test, TestOptions' (..), plusTestOptions)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.QuickCheck
  ( Arbitrary (..), Gen, Property, Testable, choose, counterexample, elements, frequency
  , ioProperty, oneof, shuffle, sublistOf, suchThat, vectorOf, (===) )

-- A property checked on a thousand cases rather than the default hundred.
testPropertyN :: Testable p => String -> p -> Test
testPropertyN name =
  plusTestOptions mempty { topt_maximum_generated_tests = Just 1000 } . testProperty name

-- Evaluating the value to WHNF fails with the message.
failsWith :: String -> a -> Property
failsWith msg a = ioProperty $ do
  r <- try (evaluate a)
  return $ case r of
    Left (ErrorCall e) -> e === msg
    Right _ -> counterexample ("no error, where " ++ msg ++ " was due") False

-- Evaluating the value to WHNF fails with a message whose part before its
-- first colon is one of the names.
failsIn :: [String] -> a -> Property
failsIn names a = ioProperty $ do
  r <- try (evaluate a)
  return $ case r of
    Left (ErrorCall e) -> counterexample e (takeWhile (/= ':') e `elem` names)
    Right _ -> counterexample ("no error, where one of " ++ show names ++ " was due") False

-- The element types of the properties that take one: Int, and Word8,
-- whose arithmetic wraps at 256.
class (Integral a, Show a, Read a, NFData a) => Elem a
instance Elem Int
instance Elem Word8

-- n elements drawn from the range, which wraps in Word8.
genElems :: Elem a => (Int, Int) -> Int -> Gen [a]
genElems r n = vectorOf n (fromIntegral <$> choose r)

-- The numbers from 0 to n - 1, as elements, which must tell them apart.
upTo :: Elem a => Int -> [a]
upTo n | map toInteger xs == map toInteger [0 .. n - 1] = xs
       | otherwise = error ("upTo: " ++ show n ++ " elements are not distinct")
  where xs = map fromIntegral [0 .. n - 1]

genShape :: Int -> Gen [Int]
genShape r = do
  r' <- choose (0, r)
  vectorOf r' (choose (0, 4))

-- The operations that make views, for building random views, and Raw sh ss
-- o k m, which reads the vector of a fresh array of rank 1, less k elements
-- at its start and m at its end, as an array of shape sh with strides ss
-- from offset o.
data Op = Transpose [Int] | Rev [Int] | Slice [(Int, Int)] | Stride [Int]
        | Window [Int] | Index Int | Broadcast [Int] [Int] | Raw [Int] [Int] Int Int Int
  deriving Show

-- The shape of the result of an operation on an array of the given shape.
opShape :: [Int] -> Op -> [Int]
opShape sh (Transpose is) = map (sh !!) is ++ drop (length is) sh
opShape sh (Rev _) = sh
opShape sh (Slice sl) = map snd sl ++ drop (length sl) sh
opShape sh (Stride ts) = zipWith (\ s t -> (s + t - 1) `div` t) sh ts ++ drop (length ts) sh
opShape sh (Window ws) =
  zipWith (\ s w -> s - w + 1) sh ws ++ ws ++ drop (length ws) sh
opShape sh (Index _) = drop 1 sh
opShape _ (Broadcast _ sh') = sh'
opShape _ (Raw sh' _ _ _ _) = sh'

-- The index in an array of the given shape that an index of the result of
-- the operation reads.
opSource :: [Int] -> Op -> [Int] -> [Int]
opSource _ (Transpose is) js =
  [ js !! i | d <- [0 .. length is - 1], (i, d') <- zip [0 ..] is, d' == d ] ++ drop (length is) js
opSource sh (Rev rs) js = [ if d `elem` rs then s - 1 - j else j | (d, s, j) <- zip3 [0 ..] sh js ]
opSource _ (Slice sl) js = zipWith (+) (map fst sl) js ++ drop (length sl) js
opSource _ (Stride ts) js = zipWith (*) ts js ++ drop (length ts) js
opSource _ (Window ws) js =
  let k = length ws
  in  zipWith (+) (take k js) (take k (drop k js)) ++ drop (2 * k) js
opSource _ (Index i) js = i : js
opSource _ (Broadcast ds _) js = map (js !!) ds
opSource _ (Raw _ ss o k _) js = [k + o + sum (zipWith (*) ss js)]

-- A slice of an extent: an offset and a length.
okSlice :: Int -> Gen (Int, Int)
okSlice s = do k <- choose (0, s); n <- choose (0, s - k); return (k, n)

-- Strides of 1 to 3, one for each dimension of the shape.
okStrides :: [Int] -> Gen [Int]
okStrides = mapM (const (choose (1, 3)))

-- An operation valid on an array of the given shape.
genOp :: [Int] -> Gen Op
genOp sh = oneof $
  [ do k <- choose (min r 2, r); Transpose <$> shuffle [0 .. k - 1]
  , Rev <$> sublistOf [0 .. r - 1]
  , Slice <$> mapM okSlice sh
  , Stride <$> okStrides sh
  , uncurry Broadcast <$> genBroadcast sh
  ] ++
  [ do k <- choose (1, min 2 (length ps)); Window <$> mapM (\ s -> choose (0, s)) (take k ps)
  | let ps = takeWhile (> 0) sh, not (null ps) ] ++
  [ Index <$> choose (0, s - 1) | s : _ <- [sh], s > 0 ]
  where r = length sh

-- The arguments of a broadcast valid on an array of the given shape.
genBroadcast :: [Int] -> Gen ([Int], [Int])
genBroadcast sh = do
  e <- choose (0, 2)
  ds <- sort . take r <$> shuffle [0 .. r + e - 1]
  extra <- vectorOf e (choose (0, 3))
  let fill i ss xs | i `elem` ds, s : ss' <- ss = s : fill (i + 1) ss' xs
                   | x : xs' <- xs = x : fill (i + 1) ss xs'
                   | otherwise = []
  return (ds, fill (0 :: Int) sh extra)
  where r = length sh

-- A shape, strides and an offset, and the length of a vector their indices
-- fit in, often exactly as long as the array.
genLayout :: Gen ([Int], [Int], Int, Int)
genLayout = do
  sh <- genShape 3
  ts <- vectorOf (length sh) (choose (-4, 4))
  let lo = sum [ (s - 1) * t | (s, t) <- zip sh ts, s > 0, t < 0 ]
      hi = sum [ (s - 1) * t | (s, t) <- zip sh ts, s > 0, t > 0 ]
  exact <- arbitrary
  slack <- choose (0, 2)
  let n = if exact then max (hi - lo + 1) (product sh) else hi - lo + 1 + slack
  pre <- choose (0, n - (hi - lo + 1))
  return (sh, ts, pre - lo, n)

-- An operation invalid on an array of the given shape: its list too long
-- for the rank, or one bad argument.
genBadOp :: [Int] -> Gen Op
genBadOp sh = oneof $
  [ Transpose <$> shuffle [0 .. r]
  , do ds <- sublistOf [0 .. r - 1]; d <- elements [-1, r]; Rev <$> shuffle (d : ds)
  , Slice . (++ [(0, 0)]) <$> mapM okSlice sh
  , Stride . (++ [1]) <$> okStrides sh
  , Window . (++ [0]) <$> okWindows
  , do (ds, sh') <- genBroadcast sh
       let r' = length sh'
       oneof $
         [ return (Broadcast (ds ++ [0]) sh') ] ++
         [ return (Broadcast (drop 1 ds) sh') | r > 0 ] ++
         [ do j <- choose (0, r - 1); d <- elements [-1, r']; return (Broadcast (setAt j d ds) sh')
         | r > 0 ] ++
         [ Broadcast <$> elements [setAt 1 (ds !! 0) ds, setAt 0 (ds !! 1) (setAt 1 (ds !! 0) ds)]
                     <*> pure sh'
         | r > 1 ] ++
         [ do j <- choose (0, r' - 1); return (Broadcast ds (setAt j (-1) sh')) | r' > 0 ] ++
         [ do j <- choose (0, r - 1)
              s' <- elements (filter (/= sh !! j) [0 .. 5])
              return (Broadcast ds (setAt (ds !! j) s' sh'))
         | r > 0 ]
  , if r == 0 then Index <$> choose (-1, 1) else Index <$> elements [-1, sh !! 0, sh !! 0 + 1]
  ] ++
  [ do k <- choose (1, r)
       is <- shuffle [0 .. k - 1]
       i <- choose (0, k - 1)
       e <- elements (-1 : k : [ j | j <- is, j /= is !! i ])
       return (Transpose (setAt i e is))
  | r > 0 ] ++
  [ do i <- choose (0, r - 1)
       let s = sh !! i
       oneof [ do sl <- mapM okSlice sh
                  b <- elements [(-1, 0), (0, -1), (s + 1, 0), (0, s + 1)]
                  return (Slice (setAt i b sl))
             , do ts <- okStrides sh
                  t <- elements [0, -1]
                  return (Stride (setAt i t ts))
             , do ws <- okWindows
                  w <- elements [-1, s + 1]
                  return (Window (setAt i w ws)) ]
  | r > 0 ]
  where r = length sh
        okWindows = mapM (\ s -> choose (0, s)) sh
        setAt i e xs = take i xs ++ e : drop (i + 1) xs

-- The functions whose errors may report an invalid operation: its own,
-- and for broadcast also reshape and stretch, which check its extents.
opNames :: Op -> [String]
opNames (Transpose _) = ["transpose"]
opNames (Rev _) = ["reverse"]
opNames (Slice _) = ["slice"]
opNames (Stride _) = ["stride"]
opNames (Window _) = ["window"]
opNames (Index _) = ["index"]
opNames (Broadcast _ _) = ["broadcast", "reshape", "stretch"]
opNames Raw{} = []  -- genBadOp draws no Raw

-- The invalid operations on an array of the given shape that give an
-- array: a broadcast to extents other than the array's but of the same
-- product, which reshape does not tell apart.
silentBadOp :: [Int] -> Op -> Bool
silentBadOp sh (Broadcast ds sh') =
  length ds == length sh && all (\ d -> d >= 0 && d < length sh') ds
  && and (zipWith (<) ds (drop 1 ds)) && all (>= 0) sh'
  && product [ sh' !! d | d <- ds ] == product sh
silentBadOp _ _ = False

-- n operations, each valid on the shape the ones before it leave.
genOps :: Int -> [Int] -> Gen [Op]
genOps 0 _ = return []
genOps n sh = do
  op <- genOp sh
  (op :) <$> genOps (n - 1) (opShape sh op)

-- A view: the shape of an array made by fromList and the operations to
-- apply to it.  A prefix of the operations is a view too.
data View = View [Int] [Op]
  deriving Show

-- At least three random views in four have a dimension and no empty one.
-- One in three starts with Raw.
instance Arbitrary View where
  arbitrary = frequency [(1, anyView), (3, anyView `suchThat` nontrivial)]
    where anyView = frequency [(2, fresh), (1, genRawView)]
          fresh = do
            sh <- genShape 3
            n <- choose (0, 4)
            View sh <$> genOps n sh
          nontrivial (View sh ops) =
            let vsh = foldl opShape sh ops
            in  not (null vsh) && product vsh > 0
  shrink (View sh ops) = [ View sh (take i ops) | i <- [0 .. length ops - 1] ]

-- A view that starts with Raw.
genRawView :: Gen View
genRawView = do
  (sh, ss, o, l) <- genLayout
  k <- choose (0, 3)
  m <- choose (0, 3)
  n <- choose (0, 3)
  View [k + l + m] . (Raw sh ss o k m :) <$> genOps n sh

-- The operation, and the view over the elements given, through DynamicG at
-- any instance of Vector.
applyOpG :: (I.Vector v, I.VecElem v a) => Op -> DG.Array v a -> DG.Array v a
applyOpG (Transpose is) = DG.transpose is
applyOpG (Rev rs) = DG.rev rs
applyOpG (Slice sl) = DG.slice sl
applyOpG (Stride ts) = DG.stride ts
applyOpG (Window ws) = DG.window ws
applyOpG (Index i) = (`DG.index` i)
applyOpG (Broadcast ds sh) = DG.broadcast ds sh
applyOpG (Raw sh ss o k m) = \ x ->
  let v = DG.toVector x in DG.A sh (I.T ss o (I.vSlice k (I.vLength v - k - m) v))

mkViewG :: (I.Vector v, I.VecElem v a) => View -> [a] -> DG.Array v a
mkViewG (View sh ops) xs = foldl (flip applyOpG) (DG.fromList sh xs) ops

-- The view over the elements given, as a boxed Dynamic array.
mkView :: View -> [a] -> Array a
mkView v = DI.A . mkViewG v
