-- Reproducer for SMALL-PINNED CHURN, the condition behind ../README.md's
-- position-term entry, its cost the churn tax -- NOT for GHC work item
-- 27601, whose reproducer this file's shape deliberately mirrors so the
-- two stay comparable.  Staged 2026-08-17, run 2026-08-18: the matrices
-- are in repro-matrix-2026-08-18.txt and repro-matrix2-2026-08-18.txt
-- beside this file, the registered predictions in
-- nursery-position-plan.txt, the verdicts in
-- nursery-position-findings2.txt items 16 and 29.  Base only.
--
-- Build:  ghc -O1 -rtsopts ReproSmall.hs
-- Run:    ./ReproSmall victim           +RTS -A1G -I0 -T -RTS
--         ./ReproSmall poison victim    +RTS -A1G -I0 -T -RTS
--         ./ReproSmall poisonbig victim +RTS -A1G -I0 -T -RTS
--   and the same three at -A32m, -A4m, and -A1G -H2G.
--
-- The hypothesis this discriminates: micro's two full-strength poisons are
-- the only two shapes whose per-iteration result vector is SMALL-pinned
-- (2304 and 2592 bytes, below the 3276-byte large-object threshold), so the
-- poison phase here sprays short-lived pinned buffers of 288 doubles = 2304
-- bytes -- each lands in a shared pinned block instead of its own block
-- group, which is the opposite size class from work item 27601's 3600-byte
-- spray (`poisonbig` below, kept for the A/B).  The victim mimics micro's
-- `list` arm on a large shape: heavy short-lived BOXED churn (a lazily
-- consumed cons list) read off a long-lived pinned source buffer, plus one
-- pinned result per iteration.  If the small spray slows this victim at
-- -A1G, less at -A32m, ~not at -A4m, with -H2G NOT curing it and mem in use
-- nearly unmoved, small-pinned churn has a base-only reproducer and can
-- be filed; if not, the difference against micro (criterion's per-bench
-- performGC, per-sample minor GCs, the env lifetime) is what to add next.
{-# LANGUAGE BangPatterns #-}
module Main (main) where

import Control.Monad (forM_, when)
import Foreign.ForeignPtr (mallocForeignPtrBytes, withForeignPtr)
import Foreign.Ptr (Ptr)
import Foreign.Storable (peekElemOff, pokeElemOff)
import GHC.Clock (getMonotonicTime)
import GHC.Stats (getRTSStats, max_mem_in_use_bytes)
import System.Environment (getArgs)
import System.Mem (performGC)

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

-- The small-pinned spray: 288 doubles = 2304 bytes < 3276, so each buffer
-- shares a pinned block rather than getting its own group.  4000 * 288
-- ~ 1.15M allocations, the order criterion gives cnn-slice-c32's arms in
-- one 5 s budget.  Counted, not timed, like work item 27601's dose.
{-# NOINLINE poisonIter #-}
poisonIter :: Int -> IO Double
poisonIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 288 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

-- Two sprays below the block's HALF: 225 doubles = 1800 B (two objects
-- share a 4 KB accumulator block) and 100 doubles = 800 B (five share).
-- They discriminate whether the damage needs the one-object-per-block
-- corner (sizes in 2048..3276 B) or any accumulator churn: a threshold
-- lowered to BLOCK_SIZE/2 would move today's poisons to own-group and
-- leave only these packings behind.
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

-- Work item 27601's spray, verbatim: 450 doubles = 3600 bytes > 3276, own
-- block group each.  Kept so one binary can A/B the two size classes.
{-# NOINLINE poisonBigIter #-}
poisonBigIter :: Int -> IO Double
poisonBigIter seed = do
  let go !acc !i | i >= 288 = pure acc
                 | otherwise = do v <- fillSum 450 (fromIntegral (seed + i))
                                  go (acc + v) (i + 1)
  go 0 0

-- The victim mimics micro's `list` arm on a vgg-sized shape: read a
-- long-lived pinned source through a boxed list (~600k conses and boxed
-- Doubles per iteration, ~24 MB of nursery churn), then one pinned result
-- per iteration.  The mapM materializes the whole list before sum consumes
-- it -- deliberate, mirroring the multi-MB live spans the span sweep
-- measured on micro's victims, not an accident to optimize away.  The
-- source stays live across iterations, as criterion's env keeps a shape's
-- setup vector live.
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
    performGC
    -- Two halves timed separately: an unpoisoned run's first pass through
    -- a fresh large nursery hits kernel-zeroed, cache-warm pages and runs
    -- FASTER than steady state (measured 2026-08-18, micro's fixed-n
    -- ladders), so the second half is the honeymoon-free reading and the
    -- one to compare across modes.
    t0 <- getMonotonicTime
    forM_ [1 .. 150 :: Int] $ \i -> do
      _ <- victimIter src i
      pure ()
    t1 <- getMonotonicTime
    forM_ [151 .. 300 :: Int] $ \i -> do
      _ <- victimIter src i
      pure ()
    t2 <- getMonotonicTime
    m <- memGiB
    putStrLn ("victim: first half " ++ show ((t1 - t0) / 150 * 1000)
              ++ " ms/iter, second half " ++ show ((t2 - t1) / 150 * 1000)
              ++ " ms/iter; mem in use: " ++ show m ++ " GiB")
