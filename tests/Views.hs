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

-- Random views, for the properties of the dynamic test modules.
module Views(testPropertyN, genShape, Op(..), applyOp, View(..), mkView) where

import Data.Array.Dynamic
import Data.List (sort)
import Test.Framework (Test, TestOptions' (..), plusTestOptions)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.QuickCheck
  ( Arbitrary (..), Gen, Testable, choose, oneof, shuffle, sublistOf, vectorOf )

-- A property checked on a thousand cases rather than the default hundred.
testPropertyN :: Testable p => String -> p -> Test
testPropertyN name =
  plusTestOptions mempty { topt_maximum_generated_tests = Just 1000 } . testProperty name

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
