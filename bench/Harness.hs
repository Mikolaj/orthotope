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
module Harness (measure) where

import Control.DeepSeq (rnf)
import Control.Exception (evaluate)
import GHC.Clock (getMonotonicTimeNSec)

import Call (Call (..))

-- The argument handed on through a call the compiler cannot see through,
-- varying with the call, so that full laziness cannot float the call out of
-- the timing loop, computing the result once and sharing it between calls.
{-# NOINLINE perturb #-}
perturb :: Int -> a -> a
perturb i x = if i == minBound then error "perturb" else x

-- | Nanoseconds a call of the result forced to normal form: the fastest of
-- three batches, each of as many calls as take 5 ms.
measure :: Call -> IO Double
measure (Call _ f x) = do
  _ <- evaluate (rnf x)
  k <- calibrate 1
  minimum <$> mapM (const (batch k)) [1 .. 3 :: Int]
 where
  calls :: Int -> IO ()
  calls 0 = return ()
  calls !i = evaluate (rnf (f (perturb i x))) >> calls (i - 1)
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
