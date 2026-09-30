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
module Views(testPropertyN, failsWith, genShape, Op(..), applyOp, opShape, opSource, View(..)
            , mkView, applyOpG, mkViewG) where

import Control.Exception (ErrorCall (..), evaluate, try)
import Data.Array.Dynamic
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.List (sort)
import Test.Framework (Test, TestOptions' (..), plusTestOptions)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.QuickCheck
  ( Arbitrary (..), Gen, Property, Testable, choose, counterexample, frequency, ioProperty
  , oneof, shuffle, sublistOf, suchThat, vectorOf, (===) )

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

genShape :: Int -> Gen [Int]
genShape r = do
  r' <- choose (0, r)
  vectorOf r' (choose (0, 4))

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

-- An operation valid on an array of the given shape.
genOp :: [Int] -> Gen Op
genOp sh = oneof $
  [ do k <- choose (min r 2, r); Transpose <$> shuffle [0 .. k - 1]
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
  [ do k <- choose (1, min 2 (length ps)); Window <$> mapM (\ s -> choose (0, s)) (take k ps)
  | let ps = takeWhile (> 0) sh, not (null ps) ] ++
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

-- At least three random views in four have a dimension and no empty one.
instance Arbitrary View where
  arbitrary = frequency [(1, anyView), (3, anyView `suchThat` nontrivial)]
    where anyView = do
            sh <- genShape 3
            n <- choose (0, 4)
            View sh <$> genOps n sh
          nontrivial v@(View sh _) =
            let vsh = shapeL (mkView v (replicate (product sh) ()))
            in  not (null vsh) && product vsh > 0
  shrink (View sh ops) = [ View sh (take i ops) | i <- [0 .. length ops - 1] ]

mkView :: View -> [a] -> Array a
mkView (View sh ops) xs = foldl (flip applyOp) (fromList sh xs) ops

-- applyOp and mkView through DynamicG, at any instance of Vector.
applyOpG :: (I.Vector v, I.VecElem v a) => Op -> DG.Array v a -> DG.Array v a
applyOpG (Transpose is) = DG.transpose is
applyOpG (Rev rs) = DG.rev rs
applyOpG (Slice sl) = DG.slice sl
applyOpG (Stride ts) = DG.stride ts
applyOpG (Window ws) = DG.window ws
applyOpG (Index i) = (`DG.index` i)
applyOpG (Broadcast ds sh) = DG.broadcast ds sh

mkViewG :: (I.Vector v, I.VecElem v a) => View -> [a] -> DG.Array v a
mkViewG (View sh ops) xs = foldl (flip applyOpG) (DG.fromList sh xs) ops
