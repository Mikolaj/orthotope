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
-- a call whose input is no view, whose arm accesses none of it, or whose arms
-- another row takes on every view runs once a size.  Between them the calls at
-- the two smaller sizes take every arm of the library's code but those that
-- fail, the Left of a conversion to a shape the Shaped modules reject, those
-- no operation reaches, the list instance of Vector, the Data and Generic
-- instances and those that print, parse or generate arrays, genericFillInto's
-- copy of a run longer than their rows, and those that need an element other
-- than Double or a shape whose extents overflow Int before one of 0.  A row is
-- the family, the operation, the size and the view, and a cell the time of a
-- call with its result forced to normal form or, given --summed, summed, every
-- component taken apart as a client consuming it would, the fastest of three
-- batches of calls, and the bytes a call allocates, both per element of the
-- view at the large size and per call at the others, where what a call costs
-- once shows.  Other arguments, if any, select the rows whose names contain one
-- of them.  Given --iters N and -m glob PATTERN, as criterion takes them, it
-- makes instead one batch of N calls of the one cell whose name, the row's and
-- the vector kind's joined by a slash, PATTERN matches, and prints the cell's
-- nanoseconds and bytes a call: two runs' instruction counts, at N calls and at
-- 2N, differ by N calls', the process's setup cancelling, where a batch of 5 ms
-- holds a number of calls that varies between builds.
--
-- Without --summed the probes follow, in a table of their own printed as the
-- other is, where it has rows: for each type the library marks as never to be
-- built, whether a client's call builds it (Materialize), its bytes comparing
-- exactly too.
--
-- Given --cells full, groups or thin, it takes the cells one at a time instead,
-- a cell named as $S/tools/NCG-battery/a2tcells.py cells names it, $S a
-- checkout of https://github.com/Mikolaj/slop: the row's name and the kind's
-- joined by a slash, summed: before a summed one's.  The selection full is
-- every cell to which the tables give a time, the forced table's then the
-- summed one's, in the tables' order, groups one cell of each group of them
-- and thin the battery's sample of 1000 forced cells, both lists as CellLists
-- says.  Of these --forced or --summed keeps the forced or the summed cells
-- alone, other arguments those whose names contain one of them, and --shard
-- I/K those whose index among the cells kept is I modulo K; a listed name the
-- benchmark does not have goes to the standard error, and the exit is 2.  With
-- --list it prints the names, given --tables each followed by a tab and its N,
-- and measures nothing.  Otherwise it prints a line a cell as the cell ends,
-- tab-separated: its name, its nanoseconds and its bytes, as its table entry
-- has them, or given --count, in the form of the battery's a2t-LABEL.tsv, its
-- name, its user-space instructions a call of the process's own thread, by
-- Linux's perf_event_open, a status, 0 for a cell counted, 1 for one whose
-- repetitions' differences spread over 1% of its figure and 2 for one not
-- counted, and its bytes a call, by the thread's allocation counter.  Each
-- is the lowest count at 2N calls less the lowest at N, over N, of --reps R
-- repetitions, 1 by default, as $S/tools/perf-per-call.py takes them: N is
-- --iters N where given, else, given --tables FORCED SUMMED, two tables the
-- benchmark printed, without and with --summed, sized from the cell's time
-- in the table of its mode, a cell kept that has no time there going to the
-- standard error and the exit being 2, else for thin 200000, the battery's,
-- and for the others sized from the cell's time taken first as above; sized, N
-- calls take about 20 ms, a call taken at 100 ns at least, from 10 to 300000.
-- The counter takes a batch's calls alone, after the major collection that the
-- bytes' count makes, all in the one process, whose heap earlier batches have
-- used: perf-per-call.py's fresh processes, whose batches run on nursery blocks
-- used for the first time, counted 0.16% more instructions a call over the full
-- selection.  A large cell's figure can move with N and with the cells counted
-- before it: Shaped/mapA/large/flip/boxed's falls by a sixth from N 10 to N
-- 20, in fresh processes too, and by 4% at N 10 after the forced large cells
-- of mapA and fmap before it, so that two counts of such a cell compare only
-- at one N, as --iters or --tables fixes it, and with the same cells before
-- it.  Off Linux, or where the kernel refuses the counter, it says so and gives
-- the bytes alone, and the exit is 2.  Given --out FILE it appends the lines
-- to FILE and passes over the cells FILE has, but for those of status 2, whose
-- lines it removes and which it counts again, so that a run stopped resumes,
-- and given --cpu C it pins the process to CPU C.  Given --compare A B [N], it
-- prints what $S/tools/NCG-battery/a2tcmp.py prints of two such files, the N
-- worst, 20 by default.
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
-- Every call applies each operation of the library to all its arguments, a
-- composition, a section or a partial application written as a lambda naming
-- them: GHC inlines an INLINE function only at a call giving it every argument
-- its definition names.
--
-- A property no construction keeps, so check it once a year or every 100
-- commits, whichever comes first: the large size's rows and the small
-- size's take the same arms of the library's code but genericFillInto's
-- copy named above, which the large size's alone take.  It last held on
-- 2026-10-24, on GHC HEAD 10.1.20261019.  Where it fails, widen a call until
-- it holds again, rather than adding a narrow one.  From the package's
-- directory, with the hpc of the GHC that builds it and $S a checkout of
-- https://github.com/Mikolaj/slop:
--
--   cabal build bench:specialisation --ghc-options=-fhpc --builddir=dist-hpc
--   B=$(find dist-hpc -type f -name specialisation -perm -u+x)
--   rm -f specialisation.tix
--   $B /large/ > /dev/null; mv specialisation.tix large.tix
--   $B /small/ > /dev/null; mv specialisation.tix small.tix
--   P=$(cd .hpc && ls -d orthotope-*-inplace)
--   for t in large small; do
--     hpc draft --hpcdir=.hpc/$P --include=$P: $t.tix > $t.draft
--     python3 $S/tools/hpc-untaken.py $t.draft --src . > $t.untaken; done
--   diff large.untaken small.untaken
--
-- A run adds to the specialisation.tix it finds, hence the rm.  The diff prints
-- each arm one size never entered and the other did, and that copy alone where
-- the property holds.
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

import Control.Monad (forM_, unless)
import Data.List (isInfixOf, tails)
import System.Environment (getArgs)
import System.Exit (exitWith)
import Text.Printf (printf)

import Call (Form (..), allocatedSecond)
import Cells (cellFlags, cellsMain)
import Compare (compareFiles)
import Harness (Mode (..), measure)
import Materialize (Probe (..), probes)
import qualified Rows

main :: IO ()
main = do
  allArgs <- getArgs
  let summing = "--summed" `elem` allArgs
      mode = if summing then Summing else Forced
  case allArgs of
    ["--compare", a, b] -> compareFiles a b 20 >>= exitWith
    ["--compare", a, b, k] | [(k', "")] <- reads k ->
      compareFiles a b k' >>= exitWith
    _ | "--compare" `elem` allArgs -> error "--compare A B [N]"
      | any (`elem` cellFlags) allArgs -> cellsMain allArgs >>= exitWith
    _ -> case options (filter (/= "--summed") allArgs) of
      (Just k, Just pattern, _) -> counted mode k pattern
      (Nothing, Nothing, args) -> table mode args
      _ -> error "--iters and -m glob go together"

-- The table of the rows the arguments select.
table :: Mode -> [String] -> IO ()
table mode args = do
  let rows = [ r | r@(row, _, _) <- Rows.rows, selected row ]
  unless (null rows) $ do
    printf "%-48s %s, the result %s\n" ""
           "ns, then bytes, an element at the large size, a call at the others"
           (case mode of Forced -> "forced"; Summing -> "summed")
    let cols = concatMap (printf "%9s") Rows.kinds :: String
    printf "%-48s %s %s\n" "" cols cols
  forM_ rows $ \ (row, per, cells) -> do
    ms <- mapM (traverse (measure mode Nothing)) (cells Viewed)
    let time = maybe "-" (\ (t, _) -> printf "%.2f" (t / fromIntegral per))
        bytes = maybe "-" (\ (_, a) -> printf "%.2f"
                             (fromIntegral a / fromIntegral per :: Double))
        figures f = concatMap (printf "%9s" . f) ms :: String
    printf "%-48s %s %s\n" row (figures time) (figures bytes)
  let probed = case mode of
        Summing -> []
        Forced -> [ p | p@(Probe row _ _ _) <- probes, selected row ]
  unless (null probed) $
    printf "\n%-48s %s\n" ""
      "bytes a call at Storable: as compiled, the value built, the difference"
  forM_ probed $ \ (Probe row f g a) -> do
    af <- allocatedSecond f a
    ag <- allocatedSecond g a
    printf "%-48s %9d%9d%9d\n" row af ag (ag - af)
 where
  selected row = null args || any (`isInfixOf` row) args

-- One batch of the given number of calls of the one cell the pattern matches,
-- and the cell's nanoseconds and bytes a call.
counted :: Mode -> Int -> String -> IO ()
counted mode k pattern =
  case [ (cell, c) | (row, _, cells) <- Rows.rows
                   , (kind, Just c) <- zip Rows.kinds (cells Viewed)
                   , let cell = row ++ "/" ++ kind
                   , glob pattern cell ] of
    [(cell, c)] -> do
      (t, a) <- measure mode (Just k) c
      printf "%s %.2f %d\n" cell t a
    cs -> error $ "-m glob matches " ++ show (length cs) ++ " cells, not one"

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
