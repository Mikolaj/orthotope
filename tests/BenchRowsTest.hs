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

-- Every row of the specialisation benchmark as a test of its name: at
-- each vector kind, the row's call gives on the view what it gives on the
-- view's normalized copy, every other input of the call derived from either
-- alike.  Between them the rows take every arm of the library's code that the
-- benchmark's header names, and each arm that a call reaches through the view
-- is checked against what the dense path gives; a call whose input no form
-- changes is checked only to run.  The results are compared with ==, and where
-- that fails, the numbers in their shown forms each within a relative 1e-9, a
-- reduction adding in the order the layout gives; the unordered vectors are
-- compared as their elements sorted.
--
-- Every size's rows run, the large ones too, though the rows took 77.5 s of the
-- suite's 100 on GHC HEAD 10.1.20261019 (2026-10-21): kept to the large rows
-- that reach an arm no smaller row reaches, the test would go stale without a
-- coverage run before each test, which would cost more than the rows it drops.
-- A call whose input no form changes runs in both forms all the same, its
-- second run costing about 1% of the rows' time on the same GHC (2026-10-22).
module BenchRowsTest (test) where

import Control.Monad (unless, zipWithM_)
import Data.Char (isDigit)
import Data.Foldable (asum)
import Data.IORef (newIORef, readIORef)
import Data.List (sort)
import Data.Typeable (Typeable, cast)
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.HUnit (Assertion, assertFailure)

import Call (Call (..), Form (..))
import Rows (rows)

test :: Test
test = testGroup "BenchRows" [ testCase row (agreeRow row cells)
                             | (row, _, cells) <- rows ]

-- The row's calls at each kind on the view against those on its normalized
-- copy.  The forms are read at run time, so that the calls, and the arrays
-- they build, are made anew in the run and held by nothing in the test tree,
-- which holds every row.
agreeRow :: String -> (Form -> [Maybe Call]) -> Assertion
agreeRow row cells = do
  forms <- newIORef (Viewed, Normalized)
  (viewed, normalized) <- readIORef forms
  zipWithM_ (agree row) ["boxed", "Storable", "Unboxed"]
            (zip (cells viewed) (cells normalized))

-- The call at the kind on the view against the call on its normalized copy.
agree :: String -> String -> (Maybe Call, Maybe Call) -> Assertion
agree _ _ (Nothing, Nothing) = return ()
agree row kind (Just (Call name f a _), Just (Call _ g b _)) =
  case cast (g b) of
    Nothing -> assertFailure (row ++ " at " ++ kind ++ ": two result types")
    Just y -> do
      let x = f a
          same | x == y = True
               | name `elem` unordered = sortedElems x == sortedElems y
               | otherwise = close (show x) (show y)
      unless same $ assertFailure $
        row ++ " at " ++ kind ++ ": " ++ take 200 (show x) ++ " on the view, "
        ++ take 200 (show y) ++ " on its normalized copy"
agree row kind _ = assertFailure (row ++ " at " ++ kind ++ ": one call alone")

-- The calls whose results lie in the order of the layout.
unordered :: [String]
unordered = ["toUnorderedVectorT", "toUnorderedVectorListT"]

-- The elements of a vector or a list of vectors, sorted.
sortedElems :: Typeable b => b -> [Double]
sortedElems r = maybe (error "sortedElems: no vector of Double") sort $ asum
  [ V.toList <$> (cast r :: Maybe (V.Vector Double))
  , VS.toList <$> (cast r :: Maybe (VS.Vector Double))
  , VU.toList <$> (cast r :: Maybe (VU.Vector Double))
  , concatMap V.toList <$> (cast r :: Maybe [V.Vector Double])
  , concatMap VS.toList <$> (cast r :: Maybe [VS.Vector Double])
  , concatMap VU.toList <$> (cast r :: Maybe [VU.Vector Double]) ]

-- Two shown results alike but in their numbers, each within a relative
-- 1e-9 of its counterpart.
close :: String -> String -> Bool
close s s' = case (number s, number s') of
  (Just (x, r), Just (y, r')) ->
    (x == y || abs (x - y) <= 1e-9 * max (abs x) (abs y)) && close r r'
  (Nothing, Nothing) -> case (s, s') of
    (c : r, c' : r') -> c == c' && close r r'
    ([], []) -> True
    _ -> False
  _ -> False

-- The number a shown result starts with, and the rest.
number :: String -> Maybe (Double, String)
number s@(c : r)
  | isDigit c || c == '-' && any isDigit (take 1 r)
  , [(x, rest)] <- reads s = Just (x, rest)
number _ = Nothing
