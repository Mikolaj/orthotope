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

-- Two output files of the specialisation benchmark's cells compared,
-- figure for figure as $S/tools/NCG-battery/a2tcmp.py compares the battery's,
-- $S a checkout of https://github.com/Mikolaj/slop: the cells both count,
-- how many are worse by 0.2% and by 1% and the worst, how many are better
-- by 0.2% with their median ratio and the best, and the cells either has no
-- figure of, then the same of the bytes a call where both files carry them.
-- Its numbers are printed as Python prints them, so that the two tools' output
-- compares by diff.
module Compare (compareFiles, fixed) where

import Control.Exception (IOException, try)
import Data.List (sort, sortBy)
import qualified Data.Map.Strict as M
import Data.Maybe (fromMaybe)
import Data.Ord (Down (..), comparing)
import Numeric (floatToDigits)
import System.Exit (ExitCode (..))
import System.IO (hPutStrLn, stderr)
import Text.Read (readMaybe)

-- | The comparison of file B with file A, the worst of the cells worse by
-- 0.2% shown to the count given, as a2tcmp.py A B N prints it, the files
-- named for the labels; exit 2 where a file cannot be read or a figure is
-- no number.
compareFiles :: FilePath -> FilePath -> Int -> IO ExitCode
compareFiles a b k = do
  got <- try ((,) <$> readFile' a <*> readFile' b)
  case got of
    Left e -> do
      hPutStrLn stderr $ show (e :: IOException)
      return $ ExitFailure 2
    Right (ta, tb) ->
      case (,,,) <$> load 1 ta <*> load 1 tb <*> load 3 ta <*> load 3 tb of
        Left bad -> do
          hPutStrLn stderr $
            "could not convert string to float: '" ++ bad ++ "'"
          return $ ExitFailure 2
        Right (ca, cb, aa, ab) -> do
          putStr $ unlines $ compareCounts a b ca cb k "cells counted"
          let allocating = any (maybe False (/= 0)) . M.elems
          if allocating aa && allocating ab
            then putStr $ unlines $
                   compareCounts a b aa ab k "cells allocating, bytes a call,"
            else return ()
          return ExitSuccess
 where
  readFile' f = do
    s <- readFile f
    length s `seq` return s

-- The figure of each cell in the column, of a line of three fields or four,
-- the last line of a cell counting, Nothing where it is - or absent, or
-- the field that is no number.
load :: Int -> String -> Either String (M.Map String (Maybe Double))
load column text = M.fromList <$> mapM figure
  [ fs | l <- lines text, let fs = splitTabs l, length fs `elem` [3, 4] ]
 where
  figure [] = Left ""
  figure (c : fs) = case drop (column - 1) fs of
    "-" : _ -> Right (c, Nothing)
    [] -> Right (c, Nothing)
    v : _ -> case readMaybe v of
      Just x -> Right (c, Just x)
      Nothing -> Left v

splitTabs :: String -> [String]
splitTabs s = case break (== '\t') s of
  (f, _ : rest) -> f : splitTabs rest
  (f, []) -> [f]

-- a2tcmp.py's compare: a cell whose figure is absent or 0 in either file is
-- not compared.
compareCounts :: String -> String -> M.Map String (Maybe Double)
              -> M.Map String (Maybe Double) -> Int -> String -> [String]
compareCounts a b ca cb k what =
  [ a ++ " to " ++ b ++ ": " ++ what ++ " in both " ++ show (M.size both)
    ++ " of " ++ show (M.size (M.union ca cb))
  , "  worse by 0.2%: " ++ show (length worse) ++ ", by 1%: "
    ++ show (length [ () | (r, _) <- worse, r - 1 >= bar - 1e-12 ]) ]
  ++ [ "    " ++ fixed 4 r ++ "  " ++ c ++ "  " ++ repr (value ca c) ++ " "
       ++ repr (value cb c)
     | (r, c) <- take k worse ]
  ++ (case better of
        (r0, c0) : _ ->
          [ "  better by 0.2%: " ++ show (length better) ++ ", median ratio "
            ++ fixed 4 (median (map fst better)) ++ ", best " ++ fixed 4 r0
            ++ " (" ++ c0 ++ ")" ]
        [] -> ["  better by 0.2%: 0"])
  ++ [ "  no count under " ++ lab ++ ": " ++ show (length miss)
       ++ ", the first " ++ m
     | (lab, mine) <- [(a, ca), (b, cb)]
     , let miss = [ c | c <- M.keys (M.union ca cb)
                      , maybe True (== 0) (M.findWithDefault Nothing c mine) ]
     , m : _ <- [miss] ]
 where
  move = 0.002
  bar = 0.01
  nonzero m = M.mapMaybe (\ v -> case v of
                             Just x | x /= 0 -> Just x
                             _ -> Nothing) m
  both = M.intersectionWith (\ x y -> y / x) (nonzero ca) (nonzero cb)
  worse = sortBy (comparing Down)
            [ (r, c) | (c, r) <- M.toList both, r - 1 >= move - 1e-12 ]
  better = sort [ (r, c) | (c, r) <- M.toList both, 1 - r >= move - 1e-12 ]
  value m c = fromMaybe 0 (M.findWithDefault Nothing c m)

-- Python's statistics.median.
median :: [Double] -> Double
median xs =
  let ys = sort xs
      l = length ys
  in if odd l then ys !! (l `div` 2)
     else (ys !! (l `div` 2 - 1) + ys !! (l `div` 2)) / 2

-- | The number at the decimals given, as Python's format rounds it: from its
-- exact binary value, a tie to even, a negative number's sign kept where
-- the rounding makes it 0.
fixed :: Int -> Double -> String
fixed d x =
  (if x < 0 || isNegativeZero x then "-" else "")
  ++ show q ++ (if d > 0 then '.' : pad (show r) else "")
 where
  m = round (abs (toRational x) * 10 ^ d) :: Integer
  (q, r) = m `quotRem` (10 ^ d)
  pad s = replicate (d - length s) '0' ++ s

-- Python's repr of a float: its shortest digits, in positional notation where
-- its exponent is from -4 to 15, else in scientific notation.
repr :: Double -> String
repr x
  | isNaN x = "nan"
  | isInfinite x = if x > 0 then "inf" else "-inf"
  | x < 0 || isNegativeZero x = '-' : repr (negate x)
  | x == 0 = "0.0"
  | e - 1 >= -4 && e - 1 < 16 = positional
  | otherwise = scientific
 where
  (ds, e) = floatToDigits 10 x
  digits = concatMap show ds
  positional
    | e <= 0 = "0." ++ replicate (negate e) '0' ++ digits
    | length digits <= e = digits ++ replicate (e - length digits) '0' ++ ".0"
    | otherwise = take e digits ++ "." ++ drop e digits
  scientific =
    take 1 digits ++ (if length digits > 1 then '.' : drop 1 digits else "")
    ++ "e" ++ (if e - 1 < 0 then "-" else "+")
    ++ pad2 (show (abs (e - 1)))
  pad2 s = replicate (2 - length s) '0' ++ s
