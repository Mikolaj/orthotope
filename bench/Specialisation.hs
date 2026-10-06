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

-- The time of every operation of the nine array modules at Double: each
-- operation of Dynamic, Ranked and Shaped runs at the three vector kinds on one
-- view, a transposed [400, 500] array, and a cell is the time per element of
-- the view of forcing the result to normal form, the fastest of three batches
-- of calls.  Arguments, if any, select the rows whose names contain one of
-- them.
--
-- BenchViewsTest checks on the same calls that a client specialises the
-- operations, by what they allocate, which tells a call passing its element
-- dictionary at run time apart where time does not: such an Unboxed rotate took
-- less time than the boxed one on GHC HEAD.
--
-- The table measures no change between two builds, loop placement alone moving
-- a reading by more than many a change does.  To compare two builds, build each
-- on GHC HEAD in a fresh build directory, its loop heads aligned to cache lines
-- by horde-ad's assembler shim tools/align-as.py, given to GHC as -pgma with
-- LOOP_MAXSKIP, LOOP_LOOKTHROUGH, LOOP_DEADSPOT, LOOP_EXITSPAN and LOOP_SETTLED
-- set to 1, and run the two binaries interleaved, one row a process, pinned to
-- one core.
module Main (main) where

import Control.Monad (forM_)
import Data.List (isInfixOf, nub)
import System.Environment (getArgs)
import Text.Printf (printf)

import Call (Call (..), n)
import Harness (measure)
import qualified OpsDynamic as D
import qualified OpsRanked as R
import qualified OpsShaped as S

main :: IO ()
main = do
  args <- getArgs
  let families = [ ("Dynamic", [D.opsB, D.opsS, D.opsU])
                 , ("Ranked", [R.opsB, R.opsS, R.opsU])
                 , ("Shaped", [S.opsB, S.opsS, S.opsU]) ]
      rows = [ (row, map (callNamed name) kinds)
             | (family, kinds) <- families
             , name <- nub [ nm | calls <- kinds, Call nm _ _ <- calls ]
             , let row = family ++ "/" ++ name
             , null args || any (`isInfixOf` row) args ]
  printf "%-20s %27s\n" "" "ns an element"
  printf "%-20s %9s%9s%9s\n" "" "boxed" "Storable" "Unboxed"
  forM_ rows $ \ (row, cells) -> do
    ts <- mapM (traverse measure) cells
    let cell = maybe "-" (\ t -> printf "%.2f" (t / fromIntegral n))
    printf "%-20s %9s%9s%9s\n" row (cell (ts !! 0)) (cell (ts !! 1))
                                   (cell (ts !! 2))

-- The call of the operation of the name, if the kind has it.
callNamed :: String -> [Call] -> Maybe Call
callNamed name calls = case [ c | c@(Call m _ _) <- calls, m == name ] of
  c : _ -> Just c
  [] -> Nothing
