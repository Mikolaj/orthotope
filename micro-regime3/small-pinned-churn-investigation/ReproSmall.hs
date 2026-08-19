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
-- long-lived pinned source through a temporary cons list of boxed
-- Doubles (~600k (:) cells and boxed Doubles per iteration, ~24 MB
-- of nursery churn), then one pinned result per iteration.  The mapM
-- materializes the whole list before sum consumes it -- deliberate,
-- mirroring the multi-MB live spans the span sweep measured on micro's
-- victims, not an accident to optimize away.  The source stays live
-- across iterations, as criterion's env keeps a shape's setup vector
-- live.
{-# NOINLINE victimIter #-}
victimIter :: Ptr Double -> Int -> IO Double
victimIter src seed = do
  let l = 600000 :: Int
  vs <- mapM (peekElemOff src) [0 .. l - 1]
  let !s = sum [v + fromIntegral seed | v <- vs]
  r <- fillSum 200000 s
  pure $! s + r

-- The unpinned counterpart of 'fillSum': the same fill-and-sum over an
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

-- The non-allocating control for the interleaved route (internoalloc,
-- padding-plan A3's verdict carried base-only): WRITE a preallocated
-- pinned 2304 B buffer end to end at the sprayer's cadence, allocating
-- nothing -- the same bytes a spray would dirty, with allocation the
-- one ingredient absent.  Registered lean, judged not remembered: the
-- victim stays clean at both areas (the driver's read and write probes
-- both did, findings item 55).
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

-- The read twin of 'noallocWrite' (internoallocr): sum an equal-sized
-- window of the long-lived source at the same cadence, allocating and
-- dirtying nothing.  Added 2026-08-19 when the write probe's -A32m
-- cells came back elevated (+16-19%) against a clean -A1G -- this
-- discriminates dirtying from mere punctuation there.  Registered
-- lean: clean at both areas, the driver's read probe having been clean
-- at -A64m (item 41b).
{-# NOINLINE noallocRead #-}
noallocRead :: Ptr Double -> Int -> IO Double
noallocRead p seed = do
  let go !acc !i | i >= (288 :: Int) = pure acc
                 | otherwise = do v <- peekElemOff p i
                                  go (acc + v) (i + 1)
  go (fromIntegral seed) 0

-- The INTERLEAVED route's dose (the follow-up comment's condition, not
-- the upfront issue's): 1000 small allocating calls between every pair
-- of victim iterations, so the cumulative count crosses the 10^5
-- saturation region inside the victim's second half (150 iterations in,
-- 150k calls).  Registered predictions, judged not remembered: inter
-- (2304 B pinned), interbig (3600 B pinned) and interunboxed (2304 B
-- movable) all lift the second half toward the upfront-poison level --
-- class-independent -- while the upfront modes above keep their class
-- split inside the same binary.  The spray calls' own wall is timed and
-- subtracted, so the printed halves stay the victim's rate.
-- The call count per victim iteration is K: 1000 by default, overridden
-- by a k:N argument (padding-plan.txt A2's dose sweep); iters:N likewise
-- overrides the 300-iteration victim horizon, split into halves. The
-- defaults reproduce every cell recorded before the arguments existed.
{-# NOINLINE interIter #-}
interIter :: Int -> (Int -> IO Double) -> Int -> IO Double
interIter k one seed = do
  let go !acc !i | i >= k = pure acc
                 | otherwise = do v <- one (seed + i)
                                  go (acc + v) (i + 1)
  go 0 0

memGiB :: IO Double
memGiB = do s <- getRTSStats
            pure (fromIntegral (max_mem_in_use_bytes s) / 2 ^ (30 :: Int))

main :: IO ()
main = do
  args <- getArgs
  -- dose:N sets the upfront modes' outer count (N * 288 objects; the
  -- default 4000 is the recorded 1.15M dose), for the upfront
  -- count-vs-bytes cells; sub-saturation doses are its point.
  let numArg0 pfx dflt = case [read (drop (length pfx) a) :: Int
                              | a <- args, take (length pfx) a == pfx] of
        [n] -> n
        []  -> dflt
        _   -> error ("at most one " ++ pfx)
      dose = numArg0 "dose:" 4000
  when (dose /= 4000) $ putStrLn ("dose=" ++ show dose)
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
          forM_ [1 .. dose] $ \i -> do
            _ <- iter i
            pure ()
          t1 <- getMonotonicTime
          m <- memGiB
          putStrLn (name ++ "ed in " ++ show (t1 - t0)
                    ++ " s; mem in use: " ++ show m ++ " GiB")
    performMajorGC
    -- Two halves timed separately: an unpoisoned run's first pass through
    -- a fresh large nursery hits kernel-zeroed, cache-warm pages and runs
    -- FASTER than steady state (measured 2026-08-18, micro's fixed-n
    -- ladders), so the second half is the honeymoon-free reading and the
    -- one to compare across modes.
    let k = numArg0 "k:" 1000
        half = numArg0 "iters:" 300 `div` 2
        -- intersize:N sets the inter/interunboxed spray's element count
        -- (default 288 = 2304 B; sub-threshold only up to 407), for the
        -- padding-plan follow-up's count-vs-bytes cells.  interbig and
        -- interunboxedbig stay fixed at 450 = 3600 B, own block group.
        sz = numArg0 "intersize:" 288
    when (k /= 1000 || half /= 150 || sz /= 288) $
      putStrLn ("k=" ++ show k ++ " iters=" ++ show (2 * half)
                ++ " intersize=" ++ show sz)
    let interOne
          | "inter" `elem` args =
              Just (\k' -> fillSum sz (fromIntegral k'))
          | "interbig" `elem` args =
              Just (\k' -> fillSum 450 (fromIntegral k'))
          | "interunboxed" `elem` args =
              Just (\k' -> fillSumUnpinned sz (fromIntegral k'))
          | "interunboxedbig" `elem` args =
              Just (\k' -> fillSumUnpinned 450 (fromIntegral k'))
          | "internoalloc" `elem` args = Just (noallocWrite naFp)
          | "internoallocr" `elem` args = Just (noallocRead src)
          | otherwise = Nothing
    sprayT <- newIORef (0 :: Double)
    let victimLoop lo hi = forM_ [lo .. hi :: Int] $ \i -> do
          case interOne of
            Nothing -> pure ()
            Just one -> do
              c0 <- getMonotonicTime
              _ <- interIter k one (i * 1000)
              c1 <- getMonotonicTime
              modifyIORef' sprayT (+ (c1 - c0))
          _ <- victimIter src i
          pure ()
    t0 <- getMonotonicTime
    victimLoop 1 half
    t1 <- getMonotonicTime
    s1 <- readIORef sprayT
    victimLoop (half + 1) (2 * half)
    t2 <- getMonotonicTime
    s2 <- readIORef sprayT
    m <- memGiB
    let perIter d = d / fromIntegral half * 1000
    putStrLn ("victim: first half " ++ show (perIter (t1 - t0 - s1))
              ++ " ms/iter, second half "
              ++ show (perIter (t2 - t1 - (s2 - s1)))
              ++ " ms/iter; mem in use: " ++ show m ++ " GiB")
