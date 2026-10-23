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

{-# LANGUAGE BangPatterns #-}
module Harness (Mode (..), measure) where

import Control.DeepSeq (rnf)
import Control.Exception (evaluate)
import Control.Monad (replicateM)
import Data.Int (Int64)
import GHC.Clock (getMonotonicTimeNSec)

import Call (Call (..), allocatedSecond)

-- The argument handed on through a call the compiler cannot see through,
-- varying with the call, so that full laziness cannot float the call out of
-- the timing loop, computing the result once and sharing it between calls.
{-# NOINLINE perturb #-}
perturb :: Int -> a -> a
perturb i x = if i == minBound then error "perturb" else x

-- | Whether a call's result is forced to normal form, as a client keeping
-- it would, or summed, every component taken apart, as one consuming it
-- would.
data Mode = Forced | Summing

-- | Nanoseconds a call of the result forced or summed, the fastest of three
-- batches, each of as many calls as take 5 ms, or given a count, of one batch
-- of that many calls, and the bytes the second of two calls allocates.
measure :: Mode -> Maybe Int -> Call -> IO (Double, Int64)
measure mode iters (Call _ f x g) = do
  a <- allocatedSecond h x
  t <- case iters of
    Just k -> batch k
    Nothing -> do
      (k, t1) <- calibrate 1
      ts <- replicateM 2 (batch k)
      return $! minimum (t1 : ts)
  return (t, a)
 where
  h = case mode of
    Forced -> rnf . f
    Summing -> \ y -> g y `seq` ()
  calls :: Int -> IO ()
  calls 0 = return ()
  calls !i = evaluate (h (perturb i x)) >> calls (i - 1)
  batch :: Int -> IO Double
  batch !k = do
    t0 <- getMonotonicTimeNSec
    calls k
    t1 <- getMonotonicTimeNSec
    return $! fromIntegral (t1 - t0) / fromIntegral k
  calibrate :: Int -> IO (Int, Double)
  calibrate !k = do
    t <- batch k
    if t * fromIntegral k >= 5e6 then return (k, t) else calibrate (2 * k)
