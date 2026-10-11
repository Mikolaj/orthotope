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

-- The time and allocation of every operation of the nine array modules at
-- Double, of the conversions between them and to their generic arrays,
-- of the generic arrays' comparisons, and of the unordered vectors of
-- Data.Array.Internal: each runs at the vector kinds having it, at three
-- sizes, [400, 500], [3, 3] and [0, 3], on the nine views of Call's View at
-- the first two and on all but the window at the empty, the window having no
-- array of no rows, and beside an operation's call are calls of the arms of
-- its code that call leaves untaken, each named for the operation and the arm;
-- a call whose input is no view, or whose arm accesses none of it, runs once
-- a size.  Between them the calls at the two smaller sizes take every arm of
-- the library's code but those that fail, those no operation reaches, the list
-- instance of Vector and the instances that print, parse or generate arrays,
-- and those at the large size every such arm but those of an empty array.  A
-- row is the family, the operation, the size and the view, and a cell the
-- time of forcing the result to normal form, the fastest of three batches of
-- calls, and the bytes a call allocates, both per element of the view at the
-- large size and per call at the others, where what a call costs once shows.
-- Arguments, if any, select the rows whose names contain one of them.
--
-- Each family's calls are written once, in an include file that the C
-- preprocessor instantiates once a vector kind and a size, with the module, the
-- shape and the indices fixed: every call is monomorphic code as a client
-- writes it, literal shapes being a common usage pattern, and none is code
-- polymorphic in the vector kind or in anything else, an unlikely use case the
-- benchmark does not cover.
--
-- A property no construction keeps, so check it once a year or every 100
-- commits, whichever comes first: the large size's rows and the small size's
-- take the same arms of the library's code.  It last held on 2026-10-12, on
-- GHC HEAD 10.1.20260918.  Where it fails, widen a call until it holds again,
-- rather than adding a narrow one.  From the package's directory, with the hpc
-- of the GHC that builds it:
--
--   cabal build bench:specialisation --ghc-options=-fhpc --builddir=dist-hpc
--   B=$(find dist-hpc -type f -name specialisation -perm -u+x)
--   rm -f specialisation.tix
--   $B /large/ > /dev/null; mv specialisation.tix large.tix
--   $B /small/ > /dev/null; mv specialisation.tix small.tix
--   hpc combine large.tix small.tix --output=both.tix
--   P=$(cd .hpc && ls -d orthotope-*-inplace)
--   for t in large small both; do
--     hpc report $t.tix --hpcdir=.hpc/$P --include=$P:; done
--
-- The three reports must agree: a box that one size alone takes
-- puts both.tix's count above the other size's.  A run adds to the
-- specialisation.tix it finds, hence the rm.  Where they disagree, list what
-- each size never entered with horde-ad's tools/hpc-untaken.py, $H being a
-- checkout of horde-ad; an arm one list holds and the other does not is one
-- the other size alone takes:
--
--   for t in large small; do
--     hpc draft --hpcdir=.hpc/$P --include=$P: $t.tix > $t.draft
--     python3 $H/tools/hpc-untaken.py $t.draft --src . > $t.untaken; done
--   diff large.untaken small.untaken
--
-- BenchViewsTest checks on the large size's calls on the strided view that
-- a client specialises the operations, by what they allocate, which tells a
-- call passing its element dictionary at run time apart where time does not:
-- such an Unboxed rotate took less time than the boxed one on GHC HEAD.
--
-- The table's times measure no change between two builds, loop placement alone
-- moving a reading by more than many a change does, while its bytes and the
-- probes' compare exactly.  To compare two builds' times, build each on GHC
-- HEAD in a fresh build directory, its loop heads aligned to cache lines by
-- horde-ad's assembler shim tools/align-as.py, given to GHC as -pgma with
-- LOOP_MAXSKIP, LOOP_LOOKTHROUGH, LOOP_DEADSPOT, LOOP_EXITSPAN and LOOP_SETTLED
-- set to 1, and run the two binaries interleaved, one row a process, pinned to
-- one core; their bytes need no shim.
module Main (main) where

import Control.Monad (forM_)
import Data.Int (Int64)
import Data.List (isInfixOf)
import Data.Maybe (isJust)
import System.Environment (getArgs)
import Text.Printf (printf)

import Call (Call (..), View (..), n, viewName, views)
import Harness (measure)
import qualified OpsDynamic as D
import qualified OpsRanked as R
import qualified OpsShaped as S

main :: IO ()
main = do
  args <- getArgs
  let families =
        [ ("Dynamic", [ ("large", n, [D.opsBLarge, D.opsSLarge, D.opsULarge])
                      , ("small", 1, [D.opsBSmall, D.opsSSmall, D.opsUSmall])
                      , ("empty", 1, [D.opsBEmpty, D.opsSEmpty, D.opsUEmpty]) ])
        , ("Ranked", [ ("large", n, [R.opsBLarge, R.opsSLarge, R.opsULarge])
                     , ("small", 1, [R.opsBSmall, R.opsSSmall, R.opsUSmall])
                     , ("empty", 1, [R.opsBEmpty, R.opsSEmpty, R.opsUEmpty]) ])
        , ("Shaped", [ ("large", n, [S.opsBLarge, S.opsSLarge, S.opsULarge])
                     , ("small", 1, [S.opsBSmall, S.opsSSmall, S.opsUSmall])
                     , ("empty", 1, [S.opsBEmpty, S.opsSEmpty, S.opsUEmpty]) ])
        ]
      rows = [ (row, per, cells)
             | (family, sizes) <- families
             , name <- merged [ [ nm | Call nm _ _ <- ops Strided ]
                              | (_, _, kinds) <- sizes, ops <- kinds ]
             , (size, per, kinds) <- sizes
             , view <- if name `elem` viewless then [Strided]
                       else if size == "empty" then filter (/= Window) views
                       else views
             , let row = family ++ "/" ++ name ++ "/" ++ size ++ "/"
                         ++ viewName view
             , null args || any (`isInfixOf` row) args
             , let cells = map (\ ops -> callNamed name (ops view)) kinds
             , any isJust cells ]
  printf "%-36s %s\n" ""
         "ns, then bytes, an element at the large size, a call at the others"
  printf "%-36s %9s%9s%9s %9s%9s%9s\n" "" "boxed" "Storable" "Unboxed"
                                         "boxed" "Storable" "Unboxed"
  forM_ rows $ \ (row, per, cells) -> do
    ms <- mapM (traverse measure) cells
    let time = maybe "-" (\ (t, _) -> printf "%.2f" (t / fromIntegral per))
        bytes = maybe "-" (\ (_, a) -> printf "%.2f" (perOf per a))
    printf "%-36s %9s%9s%9s %9s%9s%9s\n" row
           (time (ms !! 0)) (time (ms !! 1)) (time (ms !! 2))
           (bytes (ms !! 0)) (bytes (ms !! 1)) (bytes (ms !! 2))

-- Bytes over the count given.
perOf :: Int -> Int64 -> Double
perOf per a = fromIntegral a / fromIntegral per

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
viewless = [ "fromList", "fromVector", "scalar", "unScalar", "constant"
           , "generate", "iterateN", "iota", "pure"
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
callNamed name calls = case [ c | c@(Call m _ _) <- calls, m == name ] of
  c : _ -> Just c
  [] -> Nothing
