-- Reproducer for the small-pinned churn tax, with the interleave modes
-- of the follow-up comment added.  Base only.  The upfront modes and
-- the victim are the program of the issue description, unchanged.
--
-- Build:  ghc -O1 -rtsopts Repro.hs
-- Run:    ./Repro victim              +RTS -A32m -I0 -T -RTS
--         ./Repro poison victim       +RTS -A32m -I0 -T -RTS
--           (and poisonmid, poisontiny, poisonbig, as in the description)
--         ./Repro inter victim        +RTS -A32m -I0 -T -RTS
--         ./Repro interbig victim     +RTS -A32m -I0 -T -RTS
--         ./Repro interunboxed victim +RTS -A32m -I0 -T -RTS
--         ./Repro interunboxedbig victim +RTS -A32m -I0 -T -RTS
--         ./Repro internoalloc victim +RTS -A32m -I0 -T -RTS
--         ./Repro internoallocr victim +RTS -A32m -I0 -T -RTS
--   and the same at -A1G.
--
-- The inter modes make 1000 small calls between every pair of victim
-- iterations, so the cumulative call count crosses the dose curve's
-- saturation region inside the victim's second half (150000 calls by
-- its start).  The calls' own wall time is measured and subtracted, so
-- the printed halves stay the victim's rate.  Per call, inter allocates
-- a 2304 B pinned buffer (the description's poison class), interbig a
-- 3600 B pinned buffer (own block group each), interunboxed a 2304 B
-- movable ByteArray# (no pinned allocation at all), and
-- interunboxedbig a 3600 B movable ByteArray# -- above the large-object
-- limit, so it gets its own block group and does not pass through the
-- nursery.  Two modes allocate
-- nothing and are the controls: internoalloc WRITES a preallocated
-- pinned 2304 B buffer end to end at the same cadence, and
-- internoallocr READS an equal-sized window of the long-lived source.
{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE MagicHash #-}
{-# LANGUAGE UnboxedTuples #-}
module Main (main) where

import Control.Monad (forM_, when)
import Data.IORef (modifyIORef', newIORef, readIORef)
import Foreign.ForeignPtr (ForeignPtr, mallocForeignPtrBytes, withForeignPtr)
import Foreign.Ptr (Ptr)
import Foreign.Storable (peekElemOff, pokeElemOff)
import GHC.Clock (getMonotonicTime)
import GHC.Exts
import GHC.IO (IO (..))
import GHC.Stats (getRTSStats, max_mem_in_use_bytes)
import System.Environment (getArgs)
import System.Mem (performMajorGC)

-- Allocate a pinned n-Double buffer on the RTS heap, fill it, sum it.
{-# NOINLINE fillSum #-}
fillSum :: Int -> Double -> IO Double
fillSum n x = do
  fp <- mallocForeignPtrBytes (n * 8)
  withForeignPtr fp $ \p -> do
    let fill !i | i >= n = pure ()
                | otherwise = pokeElemOff p i x >> fill (i + 1)
    fill 0
    let summ !acc !i | i >= n = pure acc
                     | otherwise = do v <- peekElemOff p i
                                      summ (acc + v) (i + 1)
    summ 0 0

-- The sprays: 4000 * 288 ~ 1.15M pinned allocations each, counted rather
-- than timed so the dose does not depend on compiler or library speed.
{-# NOINLINE poisonIter #-}
poisonIter :: Int -> IO Double
poisonIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 288 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

{-# NOINLINE poisonMidIter #-}
poisonMidIter :: Int -> IO Double
poisonMidIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 225 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

{-# NOINLINE poisonTinyIter #-}
poisonTinyIter :: Int -> IO Double
poisonTinyIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 100 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

{-# NOINLINE poisonBigIter #-}
poisonBigIter :: Int -> IO Double
poisonBigIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 450 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

-- The unpinned counterpart of fillSum: the same fill-and-sum over an
-- ordinary movable ByteArray# from newByteArray# -- no pinned
-- allocation at all.  Base only, via primops.
{-# NOINLINE fillSumUnpinned #-}
fillSumUnpinned :: Int -> Double -> IO Double
fillSumUnpinned (I# n) (D# x) = IO $ \s0 ->
  case newByteArray# (n *# 8#) s0 of
    (# s1, mba #) ->
      let fill i s | isTrue# (i >=# n) = s
                   | otherwise = fill (i +# 1#) (writeDoubleArray# mba i x s)
          summ acc i s
            | isTrue# (i >=# n) = (# s, D# acc #)
            | otherwise = case readDoubleArray# mba i s of
                (# s', v #) -> summ (acc +## v) (i +# 1#) s'
      in  summ 0.0## 0# (fill 0# s1)

-- The non-allocating write control: write a preallocated pinned 2304 B
-- buffer end to end, read two elements back, allocate nothing.
{-# NOINLINE noallocWrite #-}
noallocWrite :: ForeignPtr Double -> Int -> IO Double
noallocWrite fp seed = withForeignPtr fp $ \p -> do
  let x = fromIntegral seed
      fill !i | i >= (288 :: Int) = pure ()
              | otherwise = pokeElemOff p i x >> fill (i + 1)
  fill 0
  a <- peekElemOff p 0
  b <- peekElemOff p 287
  pure $! a + b

-- The non-allocating read control: sum an equal-sized window of the
-- long-lived source, allocate and dirty nothing.
{-# NOINLINE noallocRead #-}
noallocRead :: Ptr Double -> Int -> IO Double
noallocRead p seed = do
  let go !acc !i | i >= (288 :: Int) = pure acc
                 | otherwise = do v <- peekElemOff p i
                                  go (acc + v) (i + 1)
  go (fromIntegral seed) 0

-- 1000 calls of the selected small operation, between two victim
-- iterations.
{-# NOINLINE interIter #-}
interIter :: (Int -> IO Double) -> Int -> IO Double
interIter one seed = do
  let go !acc !i | i >= 1000 = pure acc
                 | otherwise = do v <- one (seed + i)
                                  go (acc + v) (i + 1)
  go 0 0

-- The victim: read a long-lived pinned source through a temporary
-- cons list of boxed Doubles (~600k (:) cells and boxed Doubles per
-- iteration, ~24 MB of nursery churn), then one pinned result per
-- iteration.  The mapM materializes the whole list before sum consumes
-- it -- deliberate, a multi-megabyte live span, not an accident to
-- optimize away.
{-# NOINLINE victimIter #-}
victimIter :: Ptr Double -> Int -> IO Double
victimIter src seed = do
  let l = 600000 :: Int
  vs <- mapM (peekElemOff src) [0 .. l - 1]
  let !s = sum [v + fromIntegral seed | v <- vs]
  r <- fillSum 200000 s
  pure $! s + r

memGiB :: IO Double
memGiB = do s <- getRTSStats
            pure (fromIntegral (max_mem_in_use_bytes s) / 2 ^ (30 :: Int))

main :: IO ()
main = do
  args <- getArgs
  srcFp <- mallocForeignPtrBytes (600000 * 8)
  naFp <- mallocForeignPtrBytes (288 * 8)
  withForeignPtr srcFp $ \src -> do
    forM_ [0 .. 600000 - 1] $ \i ->
      pokeElemOff src i (fromIntegral i :: Double)
    forM_ [("poison", poisonIter), ("poisonmid", poisonMidIter),
           ("poisontiny", poisonTinyIter), ("poisonbig", poisonBigIter)] $
      \(name, iter) ->
        when (name `elem` args) $ do
          t0 <- getMonotonicTime
          forM_ [1 .. 4000 :: Int] $ \i -> do
            _ <- iter i
            pure ()
          t1 <- getMonotonicTime
          m <- memGiB
          putStrLn (name ++ "ed in " ++ show (t1 - t0)
                    ++ " s; mem in use: " ++ show m ++ " GiB")
    performMajorGC
    -- Two halves timed separately: an unpoisoned run's first pass through
    -- a fresh large nursery runs FASTER than steady state, so the second
    -- half is the reading to compare across modes.
    let interOne
          | "inter" `elem` args =
              Just (\k -> fillSum 288 (fromIntegral k))
          | "interbig" `elem` args =
              Just (\k -> fillSum 450 (fromIntegral k))
          | "interunboxed" `elem` args =
              Just (\k -> fillSumUnpinned 288 (fromIntegral k))
          | "interunboxedbig" `elem` args =
              Just (\k -> fillSumUnpinned 450 (fromIntegral k))
          | "internoalloc" `elem` args = Just (noallocWrite naFp)
          | "internoallocr" `elem` args = Just (noallocRead src)
          | otherwise = Nothing
    sprayT <- newIORef (0 :: Double)
    let victimLoop lo hi = forM_ [lo .. hi :: Int] $ \i -> do
          case interOne of
            Nothing -> pure ()
            Just one -> do
              c0 <- getMonotonicTime
              _ <- interIter one (i * 1000)
              c1 <- getMonotonicTime
              modifyIORef' sprayT (+ (c1 - c0))
          _ <- victimIter src i
          pure ()
    t0 <- getMonotonicTime
    victimLoop 1 150
    t1 <- getMonotonicTime
    s1 <- readIORef sprayT
    victimLoop 151 300
    t2 <- getMonotonicTime
    s2 <- readIORef sprayT
    m <- memGiB
    putStrLn ("victim: first half " ++ show ((t1 - t0 - s1) / 150 * 1000)
              ++ " ms/iter, second half "
              ++ show ((t2 - t1 - (s2 - s1)) / 150 * 1000)
              ++ " ms/iter; mem in use: " ++ show m ++ " GiB")
