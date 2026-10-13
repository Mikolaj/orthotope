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
module Harness (Mode (..), measure, allocated) where

import Control.DeepSeq (rnf)
import Control.Exception (evaluate)
import Data.Int (Int64)
import GHC.Clock (getMonotonicTimeNSec)
import GHC.Conc (getAllocationCounter, setAllocationCounter)
import System.Mem (performMajorGC)

import Call (Call (..))

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
-- batches, each of as many calls as take 5 ms, and the bytes the second of
-- two calls allocates.
measure :: Mode -> Call -> IO (Double, Int64)
measure mode (Call _ f x g) = do
  _ <- allocated h x
  -- A major collection between the first call, which evaluates the part of
  -- the input the calls use, and the calls measured: without one, the calls
  -- followed the indirections that evaluating the input left, and boxed ravel
  -- of a large dense view took twice its time.
  performMajorGC
  a <- allocated h x
  k <- calibrate 1
  t <- minimum <$> mapM (const (batch k)) [1 .. 3 :: Int]
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
  calibrate :: Int -> IO Int
  calibrate !k = do
    t0 <- getMonotonicTimeNSec
    calls k
    t1 <- getMonotonicTimeNSec
    if t1 - t0 >= 5000000 then return k else calibrate (2 * k)

-- | The bytes the thread allocates evaluating @f x@ to WHNF.
{-# NOINLINE allocated #-}
allocated :: (a -> b) -> a -> IO Int64
allocated f x = do
  setAllocationCounter maxBound
  _ <- evaluate (f x)
  c <- getAllocationCounter
  return (maxBound - c)
