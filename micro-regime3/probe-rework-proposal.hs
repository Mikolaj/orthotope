#!/usr/bin/env cabal
{- cabal:
build-depends: base, vector
ghc-options: -O1 -fspec-constr -with-rtsopts=-A32m
-}
-- The scratch probe behind README.md's "The two-stage plan and the
-- rework proposal" section (2026-08-24): prices canonicalization
-- (unit-dim drop plus adjacent-dim merge), the hoisted-read broadcast
-- fill, the outer-zero-stride block copy and the contiguous-run memcpy
-- fill against a verbatim mut-odo-vecdims port and mut-flat-gm's s == 1
-- branch, on analogs of the shapes named in the output below. Tracked
-- as that section's instrument, for Run 20 to absorb these arms into
-- Main.hs, after which this file is deleted.
--
-- Run it as a cabal script from a scratch directory OUTSIDE this
-- project, so the shebang's cabal sees no cabal.project:
--     cp probe-rework-proposal.hs /tmp/ && cd /tmp && cabal run -v0 ./probe-rework-proposal.hs
--
-- Timings are coarse in-process fixed-iteration differencing -- the
-- README section reads them as magnitudes only, past a 1.5x bar -- and
-- the allocation figures are exact, allocation being deterministic per
-- call. Not the suite's methodology. The transcript at the bottom is
-- this file's own run of 2026-08-24.
{-# LANGUAGE BangPatterns #-}
module Main (main) where

import Control.Monad (forM_, unless, when)
import Data.Bits (shiftR)
import Data.IORef
import Data.List (foldl')
import GHC.Clock (getMonotonicTimeNSec)
import GHC.Conc (getAllocationCounter)
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Storable.Mutable as VSM
import qualified Data.Vector.Unboxed as VU
import qualified Data.Vector.Unboxed.Mutable as VUM

data T = T [Int] Int (VS.Vector Double)  -- strides, offset, source

-- Reference: naive per-element multi-index decomposition.
refFill :: [Int] -> T -> VS.Vector Double
refFill sh (T ats ao v) = VS.generate l get
  where l = product sh
        nats = drop 1 (scanr (*) 1 sh)
        get i = VS.unsafeIndex v (ao + sum (zipWith (*) (dec i nats) ats))
        dec _ [] = []
        dec i (nt:nts) = let (q,r) = i `quotRem` nt in q : dec r nts

-- Verbatim port of fbMutOdoVecdims (the decided fix).
{-# NOINLINE vecdims #-}
vecdims :: [Int] -> T -> VS.Vector Double
vecdims sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- baseOffsetsMutRuns equivalent.
{-# INLINE mkTable #-}
mkTable :: Int -> [Int] -> [Int] -> VU.Vector Int
mkTable o0 osh oats = VU.create $ do
  b <- VUM.unsafeNew (max 1 (product osh))
  if null osh
    then VUM.unsafeWrite b 0 o0
    else do
      let !nLast  = last osh
          !stLast = last oats
          writeRun !q0 !off0 =
            let inner !j !off
                  | j >= nLast = return ()
                  | otherwise  = VUM.unsafeWrite b (q0 + j) off
                                 >> inner (j + 1) (off + stLast)
            in  inner 0 off0
          go [] [] !q !off = writeRun q off >> return (q + nLast)
          go (n : ns) (st : sts) !q !off =
            let dim !i !qq
                  | i >= n    = return qq
                  | otherwise = go ns sts qq (off + i * st) >>= dim (i + 1)
            in  dim 0 q
          go _ _ !q !off = writeRun q off >> return (q + nLast)
      _ <- go (init osh) (init oats) 0 o0
      return ()
  return b

-- mut-flat-gm's s==1 branch: gather through an l-long offsets table.
{-# NOINLINE flatS1 #-}
flatS1 :: [Int] -> T -> VS.Vector Double
flatS1 sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let goCopy !i
        | i >= l = return ()
        | otherwise = do
            VSM.unsafeWrite out i
              (VS.unsafeIndex v (VU.unsafeIndex baseOffsets i))
            goCopy (i + 1)
  goCopy 0
  return out
  where l = product sh
        !baseOffsets = mkTable ao (init sh) (init ats)

-- Canonicalize: drop unit dims, then merge adjacent where
-- st_outer == n_inner * st_inner.
canonShape :: [Int] -> [Int] -> ([Int], [Int])
canonShape sh ats =
  let noUnit = [(n, st) | (n, st) <- zip sh ats, n /= 1]
      merge (n, st) ((n', st') : rest)
        | st == n' * st' = (n * n', st') : rest
      merge p rest = p : rest
      merged = foldr merge [] noUnit
  in  (map fst merged, map snd merged)

-- Canonicalize, then: regime 1 -> O(1) slice; innermost stride 1 ->
-- direct mutable fill with per-element run copy; else vecdims.
{-# NOINLINE canonFill #-}
canonFill :: [Int] -> T -> VS.Vector Double
canonFill sh (T ats ao v) =
  let l = product sh
      (csh, cats) = canonShape sh ats
  in  case (csh, cats) of
        ([], []) -> VS.replicate (max 1 l) (VS.unsafeIndex v ao)
        _ | cats == drop 1 (scanr (*) 1 csh) -> VS.slice ao l v
          | last cats == 1 -> r2Fill l csh cats ao v
          | otherwise -> vecdims csh (T cats ao v)

-- Direct regime-2 fill: odometer, contiguous inner runs, element loop.
{-# NOINLINE r2Fill #-}
r2Fill :: Int -> [Int] -> [Int] -> Int -> VS.Vector Double
       -> VS.Vector Double
r2Fill l csh cats ao v = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j)
                    (VS.unsafeIndex v (baseOff + j))
                  inner (j + 1)
        in  inner 0
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where !sInner = last csh
        !rOuter = length csh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init csh)
        !oatsV = VU.fromList (init cats)

-- Same, runs copied via VS.copy (memcpy for Storable).
{-# NOINLINE canonFillCpy #-}
canonFillCpy :: [Int] -> T -> VS.Vector Double
canonFillCpy sh (T ats ao v) =
  let l = product sh
      (csh, cats) = canonShape sh ats
  in  case (csh, cats) of
        ([], []) -> VS.replicate (max 1 l) (VS.unsafeIndex v ao)
        _ | cats == drop 1 (scanr (*) 1 csh) -> VS.slice ao l v
          | last cats == 1 -> VS.create $ do
              out <- VSM.unsafeNew l
              let !sInner = last csh
                  !rOuter = length csh - 1
                  oshV = VU.fromList (init csh)
                  oatsV = VU.fromList (init cats)
                  go !lev !outPos !baseOff
                    | lev >= rOuter = do
                        VS.copy (VSM.unsafeSlice outPos sInner out)
                                (VS.unsafeSlice baseOff sInner v)
                        return (outPos + sInner)
                    | otherwise =
                        let !n  = VU.unsafeIndex oshV lev
                            !st = VU.unsafeIndex oatsV lev
                            dim !i !op
                              | i >= n    = return op
                              | otherwise = go (lev + 1) op (baseOff + i * st)
                                            >>= dim (i + 1)
                        in  dim 0 outPos
              _ <- go 0 0 ao
              return out
          | otherwise -> vecdims csh (T cats ao v)

-- Today's regime-2 path after canonicalization: maximal slices
-- collected into a list, then concatenated (toVectorT semantics).
{-# NOINLINE r2Slices #-}
r2Slices :: [Int] -> T -> VS.Vector Double
r2Slices sh (T ats ao v) =
  let l = product sh
      (csh, cats) = canonShape sh ats
      nats = drop 1 (scanr (*) 1 csh)
      oks = scanr (&&) True (zipWith (==) cats nats)
      loop (b:bs) (s:ss) (t:ts) !o =
        if b then [VS.slice o (s * t) v]
        else concat [loop bs ss ts (i * t + o) | i <- [0 .. s - 1]]
      loop _ _ _ !o = [VS.slice o 1 v]
  in  case (csh, cats) of
        ([], []) -> VS.replicate (max 1 l) (VS.unsafeIndex v ao)
        _ | cats == nats -> VS.slice ao l v
          | last cats == 1 -> VS.concat (loop oks csh cats ao)
          | otherwise -> vecdims csh (T cats ao v)

-- vecdims with the tInner == 0 run hoisted: read once, store sInner times.
{-# NOINLINE bcastFill #-}
bcastFill :: [Int] -> T -> VS.Vector Double
bcastFill sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let !x = VS.unsafeIndex v baseOff
            inner !j
              | j >= sInner = return ()
              | otherwise   = VSM.unsafeWrite out (outPos + j) x
                              >> inner (j + 1)
        in  inner 0
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- vecdims with an outer zero-stride level filled once and block-copied.
{-# NOINLINE midCopyFill #-}
midCopyFill :: [Int] -> T -> VS.Vector Double
midCopyFill sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
            in  if st == 0 && n > 1
                  then do
                    op' <- go (lev + 1) outPos baseOff
                    let !blk = op' - outPos
                        copies !i !dst
                          | i >= n = return dst
                          | otherwise = do
                              VSM.copy (VSM.unsafeSlice dst blk out)
                                       (VSM.unsafeSlice outPos blk out)
                              copies (i + 1) (dst + blk)
                    copies 1 op'
                  else
                    let dim !i !op
                          | i >= n    = return op
                          | otherwise = go (lev + 1) op (baseOff + i * st)
                                        >>= dim (i + 1)
                    in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- Timing: calibrate reps to ~0.25s, then difference t(2n) - t(n).
timeReps :: IORef Double -> ([Int] -> T -> VS.Vector Double)
         -> [Int] -> T -> Int -> IO Double
timeReps sink f sh t reps = do
  targ <- newIORef t  -- opaque: stops the call being floated out
  t0 <- getMonotonicTimeNSec
  let loop !i !acc
        | i >= reps = return acc
        | otherwise = do
            t' <- readIORef targ
            let r = f sh t'
            loop (i + 1) (acc + VS.unsafeIndex r 0
                              + VS.unsafeIndex r (VS.length r - 1))
  s <- loop 0 0
  modifyIORef' sink (+ s)
  t1 <- getMonotonicTimeNSec
  return (fromIntegral (t1 - t0) / 1e9)

-- Bytes allocated per call, by allocation-counter differencing over
-- 10 calls (deterministic per call, so 10 is plenty; the counter counts
-- down). One warm call first so any one-time allocation stays out.
allocPerCall :: IORef Double -> ([Int] -> T -> VS.Vector Double)
             -> [Int] -> T -> IO Double
allocPerCall sink f sh t = do
  targ <- newIORef t
  t0' <- readIORef targ
  let r0 = f sh t0'
  modifyIORef' sink (+ VS.unsafeIndex r0 0)
  c0 <- getAllocationCounter
  let n = 10 :: Int
      loop !i !acc
        | i >= n = return acc
        | otherwise = do
            t' <- readIORef targ
            let r = f sh t'
            loop (i + 1) (acc + VS.unsafeIndex r 0
                              + VS.unsafeIndex r (VS.length r - 1))
  sacc <- loop 0 0
  c1 <- getAllocationCounter
  modifyIORef' sink (+ sacc)
  return (fromIntegral (c0 - c1) / fromIntegral n)

perCall :: IORef Double -> ([Int] -> T -> VS.Vector Double)
        -> [Int] -> T -> IO Double
perCall sink f sh t = do
  let calibrate !n = do
        el <- timeReps sink f sh t n
        if el >= 0.25 then return n else calibrate (n * 2)
  n <- calibrate 1
  let pair = do
        e1 <- timeReps sink f sh t n
        e2 <- timeReps sink f sh t (2 * n)
        return ((e2 - e1) / fromIntegral n)
  xs <- mapM (const pair) [1 :: Int, 2, 3]
  let med [a, b, c] = max (min a b) (min c (max a b))
      med _ = error "med"
  return (med xs)

main :: IO ()
main = do
  sink <- newIORef 0
  let dense n = VS.enumFromN (0 :: Double) n
      views =
        [ ("reshape1-500k", [500000, 1], [1, 0], 0, dense 500000)
        , ("window-64x64-k1x9", [64, 56, 9, 1], [64, 1, 1, 64], 0, dense 4096)
        , ("bcast-1000x1800", [1000, 1800], [1, 0], 0, dense 1000)
        , ("bcast-tall-Mx2", [900000, 2], [1, 0], 0, dense 900000)
        , ("bcastmid-30x200x3x100", [30, 200, 3, 100], [300, 0, 1, 3], 0,
           dense 9000)
        , ("cnn-L2-24x24-c32", [24, 24, 32, 3, 3], [6912, 288, 9, 1, 3], 0,
           dense 165888)
        , ("stretch-primes", [97, 29, 89], [2581, 1, 29], 0, dense 250357)
        ]
      arms =
        [ ("vecdims", vecdims, const True)
        , ("flat-s1", flatS1, \(sh, _) -> last sh == 1)
        , ("canon", canonFill, const True)
        , ("canon-memcpy", canonFillCpy, const True)
        , ("r2-slices", r2Slices, \(sh, ats) ->
             let (csh, cats) = canonShape sh ats
             in  not (null cats) && last cats == 1)
        , ("bcast-set", bcastFill, \(_, ats) -> last ats == 0)
        , ("mid-copy", midCopyFill, \(_, ats) -> 0 `elem` init ats)
        ]
  forM_ views $ \(vname, sh, ats, ao, v) -> do
    let t = T ats ao v
        ref = refFill sh t
    putStrLn $ "== " ++ vname ++ " sh=" ++ show sh ++ " str=" ++ show ats
               ++ " l=" ++ show (product sh)
    forM_ arms $ \(aname, f, applies) ->
      when (applies (sh, ats)) $ do
        let r = f sh t
        unless (r == ref) $
          error (vname ++ "/" ++ aname ++ ": WRONG RESULT")
        ab <- allocPerCall sink f sh t
        pc <- perCall sink f sh t
        let mult = ab / (8 * fromIntegral (product sh))
        putStrLn $ "  " ++ aname ++ ": "
                   ++ show (pc * 1e6) ++ " us/call, alloc "
                   ++ show (round ab :: Int) ++ " B/call = "
                   ++ show (fromIntegral (round (mult * 100) :: Int)
                            / 100 :: Double) ++ "x of result"
  s <- readIORef sink
  putStrLn ("sink " ++ show s)

-- Transcript, 2026-08-24, loadavg about 1 at launch:
-- == reshape1-500k sh=[500000,1] str=[1,0] l=500000
--   vecdims: 2005.7400390624996 us/call, alloc 4000384 B/call = 1.0x of result
--   flat-s1: 1149.9237460937502 us/call, alloc 8000280 B/call = 2.0x of result
--   canon: 5.177618336677551e-2 us/call, alloc 472 B/call = 0.0x of result
--   canon-memcpy: 5.459330701828004e-2 us/call, alloc 472 B/call = 0.0x of result
--   r2-slices: 4.98166286945343e-2 us/call, alloc 472 B/call = 0.0x of result
--   bcast-set: 1798.40805078125 us/call, alloc 4000392 B/call = 1.0x of result
-- == window-64x64-k1x9 sh=[64,56,9,1] str=[64,1,1,64] l=32256
--   vecdims: 137.1274814453125 us/call, alloc 258816 B/call = 1.0x of result
--   flat-s1: 92.16777661132814 us/call, alloc 516824 B/call = 2.0x of result
--   canon: 80.08326513671877 us/call, alloc 259848 B/call = 1.01x of result
--   canon-memcpy: 21.15154113769531 us/call, alloc 259928 B/call = 1.01x of result
--   r2-slices: 155.15583593750003 us/call, alloc 1184152 B/call = 4.59x of result
-- == bcast-1000x1800 sh=[1000,1800] str=[1,0] l=1800000
--   vecdims: 3961.2019374999995 us/call, alloc 14400384 B/call = 1.0x of result
--   canon: 3957.9044843750003 us/call, alloc 14401216 B/call = 1.0x of result
--   canon-memcpy: 3962.656796874999 us/call, alloc 14401216 B/call = 1.0x of result
--   bcast-set: 824.2214296874998 us/call, alloc 14400392 B/call = 1.0x of result
-- == bcast-tall-Mx2 sh=[900000,2] str=[1,0] l=1800000
--   vecdims: 5590.782718750002 us/call, alloc 14400384 B/call = 1.0x of result
--   canon: 5578.900921875 us/call, alloc 14401216 B/call = 1.0x of result
--   canon-memcpy: 5640.784046875001 us/call, alloc 14401216 B/call = 1.0x of result
--   bcast-set: 3439.2302578125004 us/call, alloc 14400392 B/call = 1.0x of result
-- == bcastmid-30x200x3x100 sh=[30,200,3,100] str=[300,0,1,3] l=1800000
--   vecdims: 3929.7973749999996 us/call, alloc 14400768 B/call = 1.0x of result
--   canon: 3941.3973124999998 us/call, alloc 14402432 B/call = 1.0x of result
--   canon-memcpy: 3936.1589218750005 us/call, alloc 14402432 B/call = 1.0x of result
--   mid-copy: 486.4601835937499 us/call, alloc 14400784 B/call = 1.0x of result
-- == cnn-L2-24x24-c32 sh=[24,24,32,3,3] str=[6912,288,9,1,3] l=165888
--   vecdims: 497.487548828125 us/call, alloc 1327984 B/call = 1.0x of result
--   canon: 494.58944921875013 us/call, alloc 1329040 B/call = 1.0x of result
--   canon-memcpy: 494.25764257812494 us/call, alloc 1329040 B/call = 1.0x of result
-- == stretch-primes sh=[97,29,89] str=[2581,1,29] l=250357
--   vecdims: 553.0927929687499 us/call, alloc 2003416 B/call = 1.0x of result
--   canon: 554.3327382812499 us/call, alloc 2004664 B/call = 1.0x of result
--   canon-memcpy: 551.054958984375 us/call, alloc 2004664 B/call = 1.0x of result
-- sink 1.3842691614453e14
