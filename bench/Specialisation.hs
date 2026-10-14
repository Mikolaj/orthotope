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
-- row is the family, the operation, the size and the view, and a cell the time
-- of a call with its result forced to normal form or, given --summed, summed,
-- every component taken apart as a client consuming it would, the fastest of
-- three batches of calls, and the bytes a call allocates, both per element of
-- the view at the large size and per call at the others, where what a call
-- costs once shows.  Other arguments, if any, select the rows whose names
-- contain one of them.  Given --iters N and -m glob PATTERN, as criterion
-- takes them, it makes instead one batch of N calls of the one cell whose
-- name, the row's and the vector kind's joined by a slash, PATTERN matches,
-- and prints the cell's nanoseconds and bytes a call: two runs' instruction
-- counts, at N calls and at 2N, differ by N calls', the process's setup
-- cancelling, where a batch of 5 ms holds a number of calls that varies
-- between builds.
--
-- The two tables, forced and summed, are compared and never combined: where
-- they lead to different conclusions about a change, the divergence is
-- investigated, and one that cannot be removed gets a note at the code
-- responsible saying why.
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
-- moving a reading by more than many a change does, while its bytes compare
-- exactly.  To compare two builds' times, build each on GHC HEAD in a fresh
-- build directory and run the two binaries interleaved, one row a process,
-- pinned to one core.
module Main (main) where

import Control.Monad (forM_)
import Data.Int (Int64)
import Data.List (isInfixOf, tails)
import System.Environment (getArgs)
import Text.Printf (printf)

import Call (Form (..))
import Harness (Mode (..), measure)
import qualified Rows

main :: IO ()
main = do
  allArgs <- getArgs
  let summing = "--summed" `elem` allArgs
      mode = if summing then Summing else Forced
  case options (filter (/= "--summed") allArgs) of
    (Just k, Just pattern, _) -> counted mode k pattern
    (Nothing, Nothing, args) -> table mode args
    _ -> error "--iters and -m glob go together"

-- The table of the rows the arguments select.
table :: Mode -> [String] -> IO ()
table mode args = do
  let rows = [ r | r@(row, _, _) <- Rows.rows
                 , null args || any (`isInfixOf` row) args ]
  printf "%-36s %s, the result %s\n" ""
         "ns, then bytes, an element at the large size, a call at the others"
         (case mode of Forced -> "forced"; Summing -> "summed")
  printf "%-36s %9s%9s%9s %9s%9s%9s\n" "" "boxed" "Storable" "Unboxed"
                                         "boxed" "Storable" "Unboxed"
  forM_ rows $ \ (row, per, cells) -> do
    ms <- mapM (traverse (measure mode Nothing)) (cells Viewed)
    let time = maybe "-" (\ (t, _) -> printf "%.2f" (t / fromIntegral per))
        bytes = maybe "-" (\ (_, a) -> printf "%.2f" (perOf per a))
    printf "%-36s %9s%9s%9s %9s%9s%9s\n" row
           (time (ms !! 0)) (time (ms !! 1)) (time (ms !! 2))
           (bytes (ms !! 0)) (bytes (ms !! 1)) (bytes (ms !! 2))

-- Bytes over the count given.
perOf :: Int -> Int64 -> Double
perOf per a = fromIntegral a / fromIntegral per

-- One batch of the given number of calls of the one cell the pattern matches,
-- and the cell's nanoseconds and bytes a call.
counted :: Mode -> Int -> String -> IO ()
counted mode k pattern =
  case [ (cell, c) | (row, _, cells) <- Rows.rows
                   , (kind, Just c) <- zip kinds (cells Viewed)
                   , let cell = row ++ "/" ++ kind
                   , glob pattern cell ] of
    [(cell, c)] -> do
      (t, a) <- measure mode (Just k) c
      printf "%s %.2f %d\n" cell t a
    cs -> error $ "-m glob matches " ++ show (length cs) ++ " cells, not one"

-- The vector kinds, in the order of a row's cells.
kinds :: [String]
kinds = ["boxed", "Storable", "Unboxed"]

-- The count of --iters, the pattern of -m glob and the other arguments.
options :: [String] -> (Maybe Int, Maybe String, [String])
options ("--iters" : k : as) = let (_, p, rest) = options as
                               in (Just (read k), p, rest)
options ("-m" : "glob" : p : as) = let (i, _, rest) = options as
                                   in (i, Just p, rest)
options (a : as) = let (i, p, rest) = options as in (i, p, a : rest)
options [] = (Nothing, Nothing, [])

-- Whether the pattern, its * matching any string and its ? any character,
-- matches the whole name.
glob :: String -> String -> Bool
glob ('*' : p) s = any (glob p) (tails s)
glob ('?' : p) (_ : s) = glob p s
glob (c : p) (d : s) = c == d && glob p s
glob p [] = all (== '*') p
glob [] (_ : _) = False
