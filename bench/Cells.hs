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

-- The specialisation benchmark's cells one at a time, a line a cell, each
-- timed as its table entry is or counted in instructions and bytes a call,
-- in one of three selections: every cell, one cell of each group, or the thin
-- sample.  Specialisation's header gives the options.
{-# LANGUAGE BangPatterns #-}
{-# OPTIONS_GHC -fno-full-laziness #-}
module Cells (cellFlags, cellsMain) where

import Control.Exception (IOException, evaluate, try)
import Control.Monad (foldM, forM, forM_, unless, void, when)
import Data.IORef (newIORef, readIORef, writeIORef)
import Data.List (isInfixOf, isPrefixOf)
import qualified Data.Map.Strict as M
import Data.Maybe (isJust, isNothing)
import qualified Data.Set as S
import qualified Data.Vector as V
import qualified Data.Vector.Unboxed as VU
import GHC.Conc (getAllocationCounter)
import System.Directory (renameFile)
import System.Exit (ExitCode (..))
import System.IO ( BufferMode (..), IOMode (..), hPutStrLn
                 , hSetBuffering, readFile', stderr, stdout, withFile )
import Text.Printf (printf)
import Text.Read (readMaybe)

import Call (Call, Form (..))
import qualified CellLists
import Compare (fixed)
import qualified Counter
import Harness (Mode (..), measure, measureAround)
import qualified Rows

-- | The options that only a run of cells takes, any of which makes a run one
-- of cells.
cellFlags :: [String]
cellFlags = [ "--cells", "--forced", "--list", "--count", "--reps", "--tables"
            , "--out", "--shard", "--cpu" ]

data Selection = Full | Groups | Thin

data Options = Options
  { optCells :: Maybe Selection
  , optForced, optSummed, optList, optCount :: Bool
  , optIters :: Maybe Int
  , optReps :: Int
  , optTables :: Maybe (FilePath, FilePath)
  , optOut :: Maybe FilePath
  , optShard :: Maybe (Int, Int)
  , optCpu :: Maybe Int
  , optPatterns :: [String] }

-- One repetition, as the battery counts its cells.
defaults :: Options
defaults = Options Nothing False False False False Nothing 1 Nothing Nothing
                   Nothing Nothing []

options :: Options -> [String] -> Either String Options
options o args = case args of
  [] -> Right o {optPatterns = reverse (optPatterns o)}
  "--cells" : s : as -> case s of
    "full" -> options o {optCells = Just Full} as
    "groups" -> options o {optCells = Just Groups} as
    "thin" -> options o {optCells = Just Thin} as
    _ -> Left $ "--cells " ++ s ++ ": not full, groups or thin"
  "--forced" : as -> options o {optForced = True} as
  "--summed" : as -> options o {optSummed = True} as
  "--list" : as -> options o {optList = True} as
  "--count" : as -> options o {optCount = True} as
  "--reps" : r : as -> positive "--reps" r >>= \ k ->
    options o {optReps = k} as
  "--iters" : k : as -> positive "--iters" k >>= \ i ->
    options o {optIters = Just i} as
  "--tables" : f : g : as -> options o {optTables = Just (f, g)} as
  ["--tables", _] -> Left "--tables needs two files, FORCED and SUMMED"
  "--out" : f : as -> options o {optOut = Just f} as
  "--shard" : s : as -> case break (== '/') s of
    (i, _ : k) | Just i' <- readMaybe i, Just k' <- readMaybe k
               , 0 <= i' && i' < k' -> options o {optShard = Just (i', k')} as
    _ -> Left $ "--shard " ++ s ++ ": not I/K, 0 <= I < K"
  "--cpu" : c : as -> case readMaybe c of
    Just c' -> options o {optCpu = Just c'} as
    Nothing -> Left $ "--cpu " ++ c ++ ": not a CPU's number"
  "-m" : _ -> Left "-m glob selects a cell of the tables, not of --cells"
  [a] | a `elem` [ "--cells", "--reps", "--iters", "--tables", "--out", "--shard"
                 , "--cpu" ]
      -> Left $ a ++ " needs a value"
  a : as | "--" `isPrefixOf` a -> Left $ "unknown option " ++ a
         | otherwise -> options o {optPatterns = a : optPatterns o} as
 where
  positive flag s = case readMaybe s of
    Just k | k >= 1 -> Right k
    _ -> Left $ flag ++ " " ++ s ++ ": not a positive number"

-- A cell: its name, as $S/tools/NCG-battery/a2tcells.py cells names it, its
-- mode, the count its table's figures are per, and its row's calls and its
-- kind's index among them, the call made anew where it is measured, so that
-- the list of the cells holds no call's input.
data Cell = Cell String Mode Int (Form -> [Maybe Call]) Int

cellName :: Cell -> String
cellName (Cell nm _ _ _ _) = nm

-- The cells of the selection that the options keep but those the output
-- file has, each with its N where tables are given, the names the selection
-- lists that no cell has, and the names of the cells kept to which the tables
-- give no time.  Every list of cells is local and built anew at each call, full
-- laziness being off in this module, so that none of them, nor the tables,
-- stays live while the cells are measured: as a list of strings the names
-- of every cell took some 30 MB, which each major collection inside a batch
-- copied.
{-# NOINLINE select #-}
select :: Options -> Selection -> S.Set String -> Maybe (Table, Table)
       -> IO (Packed, [String], [String])
select o sel have tables = do
  todo <- packed [ (c, n) | (c, Just n) <- withN ]
  _ <- evaluate (length missing + length untimed)
  return (todo, missing, untimed)
 where
  remaining = [ c | c <- sharded, not (S.member (cellName c) have) ]
  withN = case tables of
    Nothing -> [ (c, Just 0) | c <- remaining ]
    Just ts -> [ (c, tableCalls ts c) | c <- remaining ]
  untimed = [ cellName c | (c, n) <- withN, isNothing n ]
  -- Every cell to which the tables give a time, the forced table's, then the
  -- summed one's, in the tables' order.
  catalogue =
    [ Cell (prefix ++ row ++ "/" ++ kind) mode per cells k
    | (prefix, mode) <- [("", Forced), ("summed:", Summing)]
    , (row, per, cells) <- Rows.rows
    , (k, kind, Just _) <- zip3 [0 ..] Rows.kinds (cells Viewed) ]
  byName = M.fromList [ (cellName c, c) | c <- catalogue ]
  named nms = ( [ c | nm <- nms, Just c <- [M.lookup nm byName] ]
              , [ nm | nm <- nms, not (M.member nm byName) ] )
  (listed, missing) = case sel of
    Full -> (catalogue, [])
    Groups -> named CellLists.groups
    Thin -> named CellLists.thin
  kept = [ c | c@(Cell nm mode _ _ _) <- listed
             , case mode of
                 Forced -> optForced o || not (optSummed o)
                 Summing -> optSummed o || not (optForced o)
             , null (optPatterns o) || any (`isInfixOf` nm) (optPatterns o) ]
  sharded = case optShard o of
    Nothing -> kept
    Just (i, k) -> [ c | (j, c) <- zip [0 :: Int ..] kept, j `mod` k == i ]

-- | A run of cells, given every argument, and its exit: 2 where an option,
-- a table or a listed name is wrong, the CPU could not be taken, a cell kept
-- has no time in the tables or a cell was not counted.
cellsMain :: [String] -> IO ExitCode
cellsMain args = case options defaults args of
  Left e -> failed e
  Right o -> case optCells o of
    Nothing -> failed "--cells full, groups or thin selects the cells"
    Just _ | isJust (optIters o) && not (optCount o) ->
             failed "--iters, given --cells, is the count of --count"
           | isJust (optIters o) && isJust (optTables o) ->
             failed "--iters and --tables each give N: one of them"
           | isJust (optTables o) && not (optCount o || optList o) ->
             failed "--tables sizes the counts of --count"
    Just sel -> do
      got <- traverse readTables (optTables o)
      pinned <- maybe (return (Right ())) Counter.pin (optCpu o)
      case (sequence got, pinned) of
        (Left e, _) -> failed $ "--tables: " ++ e
        (_, Left e) -> failed $ "--cpu: " ++ e
        (Right tables, Right ()) -> do
          have <- case optOut o of
            Just f | not (optList o) -> written f
            _ -> return S.empty
          (cells, missing, untimed) <- select o sel have tables
          forM_ missing $ \ nm -> hPutStrLn stderr $ "no cell " ++ nm
          forM_ untimed $ \ nm ->
            hPutStrLn stderr $ "no time of " ++ nm ++ " in the tables"
          ok <- if optList o
                then do
                  forM_ (unpacked cells) $ \ (c, n) ->
                    putStrLn $ cellName c
                               ++ if isJust tables then '\t' : show n else ""
                  return True
                else run o sel cells
          return $ if ok && null missing && null untimed then ExitSuccess
                   else ExitFailure 2
 where
  failed e = hPutStrLn stderr e >> return (ExitFailure 2)

-- The cells measured or counted, each line written as its cell ends; whether
-- every cell was counted.
run :: Options -> Selection -> Packed -> IO Bool
run o sel cells =
  withOutput (optOut o) $ \ out ->
    if optCount o then countCells o sel out cells
    else timeCells out cells >> return True

-- The cells to measure, their names packed into one unboxed string with each
-- one's end, and each one's N from the tables, 0 where none are given, so that
-- what is live while they are measured is little more than their calls'
-- closures.
data Packed = Packed (VU.Vector Char) (VU.Vector Int) (V.Vector Cell)
                     (VU.Vector Int)

packed :: [(Cell, Int)] -> IO Packed
packed cells = do
  let names = VU.fromList (concatMap (cellName . fst) cells)
      ends = VU.fromList (scanl1 (+) (map (length . cellName . fst) cells))
      nameless = V.fromList [ Cell "" mode per cs k
                            | (Cell _ mode per cs k, _) <- cells ]
      ns = VU.fromList (map snd cells)
  _ <- evaluate (VU.length names + VU.length ends + V.length nameless
                 + VU.length ns)
  return $! Packed names ends nameless ns

-- The cells, each with its name, and each one's N from the tables.
unpacked :: Packed -> [(Cell, Int)]
unpacked (Packed names ends nameless ns) =
  [ (Cell (VU.toList (VU.slice start (end - start) names)) mode per cs k, n)
  | (i, Cell _ mode per cs k) <- zip [0 ..] (V.toList nameless)
  , let end = ends VU.! i
        start = if i == 0 then 0 else ends VU.! (i - 1)
        n = ns VU.! i ]

-- The names of the cells of the file's complete lines, a line of a time three
-- fields and one of a count four, but those of a count of status 2, cells
-- not counted, whose lines the file loses, so that they are counted again;
-- none where there is no file.
written :: FilePath -> IO (S.Set String)
written f = do
  got <- try (readFile f)
  case got :: Either IOException String of
    Left _ -> return S.empty
    Right s -> do
      let ls = complete s
          kept = [ l | l <- ls, case fields l of
                                  [_, _, "2", _] -> False
                                  _ -> True ]
      when (length kept < length ls) $ do
        writeFile (f ++ ".tmp") (unlines kept)
        renameFile (f ++ ".tmp") f
      return $! S.fromList
        [ nm | l <- kept, let fs = fields l, length fs `elem` [3, 4]
             , nm : _ <- [fs] ]
 where
  complete s = case lines s of
    ls | not (null s) && last s /= '\n' -> init ls
       | otherwise -> ls
  fields l = case break (== '\t') l of
    (x, _ : rest) -> x : fields rest
    (x, []) -> [x]

-- Lines to the file, appended after a line a stopped run left unfinished, or
-- to the standard output, each as it ends.
withOutput :: Maybe FilePath -> ((String -> IO ()) -> IO a) -> IO a
withOutput Nothing act = do
  hSetBuffering stdout LineBuffering
  act putStrLn
withOutput (Just f) act = do
  got <- try (readFile f)
  let unfinished = case got :: Either IOException String of
        Right s -> not (null s) && last s /= '\n'
        Left _ -> False
  unfinished `seq` withFile f AppendMode $ \ h -> do
    hSetBuffering h LineBuffering
    when unfinished $ hPutStrLn h ""
    act (hPutStrLn h)

-- The call of the cell, made anew.
callOf :: Cell -> Call
callOf (Cell nm _ _ cells k) = case drop k (cells Viewed) of
  Just c : _ -> c
  _ -> error $ "no call of " ++ nm

-- Each cell timed as its table entry is, its nanoseconds and bytes in its
-- table's units.
timeCells :: (String -> IO ()) -> Packed -> IO ()
timeCells out cells = forM_ (map fst (unpacked cells)) $
                      \ c@(Cell nm mode per _ _) -> do
  (t, a) <- measure mode Nothing (callOf c)
  out $ printf "%s\t%.2f\t%.2f" nm (t / fromIntegral per)
                (fromIntegral a / fromIntegral per :: Double)

-- The calls a cell of the thin sample is counted at, the battery's.
thinCalls :: Int
thinCalls = 200000

-- $S/tools/NCG-battery/a2tcells.py's N of a cell whose call takes
-- the nanoseconds given: about 20 ms of calls, a call taken at 100 ns at least,
-- from 10 to 300000 calls.
callsFor :: Double -> Int
callsFor ns = max 10 (min 300000 (truncate (2e7 / max ns 100)))

-- The N of a cell timed at the nanoseconds given, a call's, the time read
-- as its table prints it.
sized :: Int -> Double -> Int
sized per t =
  callsFor (read (printf "%.2f" (t / fromIntegral per)) * fromIntegral per)

-- A table the benchmark printed, each row's six figures by the row's name,
-- read as $S/tools/census.py reads one: a line of seven fields whose first
-- holds a slash.
type Table = M.Map String [String]

-- The two tables of --tables, the forced one's and the summed one's.
readTables :: (FilePath, FilePath) -> IO (Either String (Table, Table))
readTables (f, g) = do
  got <- try ((,) <$> readFile' f <*> readFile' g)
  return $ case got of
    Left e -> Left $ show (e :: IOException)
    Right (tf, tg) -> (,) <$> table f tf <*> table g tg
 where
  table path text =
    let t = M.fromList [ (row, fs) | l <- lines text, row : fs <- [words l]
                                   , length fs == 6, '/' `elem` row ]
    in if M.null t then Left (path ++ " has no table row") else Right t

-- The N of a cell by its time in the table of its mode, none where the table
-- has no number there.
tableCalls :: (Table, Table) -> Cell -> Maybe Int
tableCalls (forced, summed) (Cell nm mode per _ k) = do
  figures <- M.lookup row (case mode of Forced -> forced; Summing -> summed)
  t <- readMaybe =<< case drop k figures of
         f : _ -> Just f
         [] -> Nothing
  return $! callsFor (t * fromIntegral per)
 where
  bare = case mode of
    Forced -> nm
    Summing -> drop (length "summed:") nm
  row = reverse (drop 1 (dropWhile (/= '/') (reverse bare)))

-- Each cell counted at N and 2N calls, R times, by
-- $S/tools/perf-per-call.py's method, in the battery's a2t-LABEL.tsv form:
-- the name, the instructions a call, the status, 0 where counted, 1 where
-- the repetitions' differences spread over 1% of the figure and 2 where none
-- was counted, and the bytes a call; whether every cell was counted.
countCells :: Options -> Selection -> (String -> IO ()) -> Packed -> IO Bool
countCells o sel out cells = do
  counter <- Counter.open
  case counter of
    Left e -> hPutStrLn stderr $ "--count: " ++ e ++ ", so bytes alone"
    Right _ -> return ()
  foldM (\ !ok (c@(Cell nm mode per _ _), given) -> do
    let x = callOf c
        -- A batch counted at k calls, k forced before the counter starts,
        -- as N's sizing would otherwise be counted with the first batch, and
        -- the counter around the calls alone, after the major collection
        -- that measure makes for the bytes' count: that collection copies
        -- whatever earlier cells left live, and counted, its cost moved
        -- by hundreds of thousands of instructions from batch to batch.
        once !k = do
          i <- case counter of
            Right ctr -> do
              got <- newIORef 0
              let around b = Counter.counted ctr (void b) >>= writeIORef got
                             >> return 0
              _ <- measureAround around mode (Just k) x
              Just <$> readIORef got
            Left _ -> void (measure mode (Just k) x) >> return Nothing
          a <- getAllocationCounter
          return (i, maxBound - a)
    !n <- case (optIters o, sel) of
      (Just k, _) -> return k
      _ | given > 0 -> return given
      (Nothing, Thin) -> return thinCalls
      (Nothing, _) -> sized per . fst <$> measure mode Nothing x
    runs <- forM [0 .. optReps o - 1] $ \ r ->
      if even r then (,) <$> once n <*> once (2 * n)
      else flip (,) <$> once (2 * n) <*> once n
    let perCall :: Integer -> Integer -> Double
        perCall c1 c2 = fromIntegral (c2 - c1) / fromIntegral n
        lowest f = toInteger (minimum (map f runs))
        bytes = perCall (lowest (snd . fst)) (lowest (snd . snd))
        counts = mapM (\ ((i1, _), (i2, _)) -> (,) <$> i1 <*> i2) runs
        ins = case counts of
          Just is ->
            let lo f = toInteger (minimum (map f is))
                diffs = [ perCall (toInteger c1) (toInteger c2)
                        | (c1, c2) <- is ]
                v = perCall (lo fst) (lo snd)
            in Just (v, maximum diffs - minimum diffs > 0.01 * abs v)
          Nothing -> Nothing
        figure v = if v < 0 then "-" else fixed 1 v
        status = case ins of
          Just (v, wide) | v >= 0 -> if wide then "1" else "0"
          _ -> "2"
    out $ nm ++ "\t" ++ maybe "-" (figure . fst) ins ++ "\t" ++ status ++ "\t"
          ++ figure bytes
    unless (status == "0") $ hPutStrLn stderr $ nm ++ ": status " ++ status
    return $! ok && status /= "2") True (unpacked cells)
