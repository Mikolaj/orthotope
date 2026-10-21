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

-- The rows of the specialisation benchmark, which it times and
-- BenchRowsTest checks, each a call of an operation at the vector kinds
-- having it.
module Rows (rows) where

import Data.List (find)
import Data.Maybe (isJust)

import Call (Call (..), Form (..), View (..), n, viewName, views)
import qualified OpsDynamic as D
import qualified OpsRanked as R
import qualified OpsShaped as S

-- | Each row's name, the family, the operation, the size and the view;
-- the count its figures are per, the view's elements at the large size and
-- one call at the others; and its call at each vector kind, boxed,
-- Storable and Unboxed, if the kind has the operation, on the view in the
-- form given, made anew at each application, so that what holds the rows
-- holds no call's input.
rows :: [(String, Int, Form -> [Maybe Call])]
rows =
  [ (row, per, cells)
  | (family, sizes) <- families
  , name <- merged [ [ nm | Call nm _ _ _ <- ops Viewed Strided ]
                   | (_, _, kinds) <- sizes, ops <- kinds ]
  , (size, per, kinds) <- sizes
  , view <- if name `elem` viewless then [Strided]
            else if size == "empty" then filter (/= Window) views
            else views
  , let row = family ++ "/" ++ name ++ "/" ++ size ++ "/" ++ viewName view
        cells form = map (\ ops -> callNamed name (ops form view)) kinds
  , any isJust (cells Viewed) ]
 where
  families =
    [ ("Dynamic", [ ("large", n, [D.opsBLarge, D.opsSLarge, D.opsULarge])
                  , ("small", 1, [D.opsBSmall, D.opsSSmall, D.opsUSmall])
                  , ("empty", 1, [D.opsBEmpty, D.opsSEmpty, D.opsUEmpty]) ])
    , ("Ranked", [ ("large", n, [R.opsBLarge, R.opsSLarge, R.opsULarge])
                 , ("small", 1, [R.opsBSmall, R.opsSSmall, R.opsUSmall])
                 , ("empty", 1, [R.opsBEmpty, R.opsSEmpty, R.opsUEmpty]) ])
    , ("Shaped", [ ("large", n, [S.opsBLarge, S.opsSLarge, S.opsULarge])
                 , ("small", 1, [S.opsBSmall, S.opsSSmall, S.opsUSmall])
                 , ("empty", 1, [S.opsBEmpty, S.opsSEmpty, S.opsUEmpty]) ]) ]

-- The names of the lists, each list's in its order, a name that no earlier list
-- holds placed before the name after it in its own, so that the call of an arm
-- that one size alone has stays beside its operation's.
merged :: [[String]] -> [String]
merged = foldl (\ acc names -> place acc Nothing (reverse names)) []
 where
  place acc _ [] = acc
  place acc next (nm : nms)
    | nm `elem` acc = place acc (Just nm) nms
    | otherwise = place (before next nm acc) (Just nm) nms
  before Nothing nm acc = acc ++ [nm]
  before (Just s) nm acc = let (xs, ys) = break (== s) acc in xs ++ nm : ys

-- The calls whose input is no view, or whose arm accesses none of it, which run
-- on one view.
viewless :: [String]
viewless = [ "fromList", "fromList.map", "fromVector", "scalar", "unScalar"
           , "constant", "generate", "iterateN", "iota", "pure"
           , "append.emptyL", "append.emptyR", "concatOuter.one", "rotate.one"
           , "update.none", "pad.none", "==.shapes", "maximumA.one"
           , "reshape.scalar", "allSameA.tiers"
           , "convert.ranked", "convertE.ranked"
           , "convert.shaped", "convertE.shaped"
           , "convert.dynamic", "convertE.dynamic"
           , "convert.g", "convertE.g"
           , "<=", "<=.g", ">", ">.g", ">=", ">=.g"
           , "max", "max.g", "min", "min.g" ]

-- The call of the operation of the name, if the kind has it.
callNamed :: String -> [Call] -> Maybe Call
callNamed name = find (\ (Call m _ _ _) -> m == name)
