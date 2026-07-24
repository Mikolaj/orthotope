{-# LANGUAGE BangPatterns #-}
-- | Self-contained benchmark isolating orthotope's toVectorListT regime 3
-- (the per-element fallback for an innermost-strided array), so the
-- current fallback and the candidate on this branch can be A/B'd without
-- an ox-arrays + horde-ad rebuild. The four strategies are 'fbList' (the
-- current fallback), 'fbGenQuotRem' (this branch's change), 'fbGenUnsafe'
-- and 'fbUnfoldAdd'; 'mkStrided' builds a regime-3 input and 'regimeOf'
-- checks it really is one before timing.
--
-- The change was meant to speed regime 3 up everywhere; it is a mixed
-- picture instead. @README.md@ next to this file is the standalone
-- account -- shape rationale, the numbers and the verdict (kept there,
-- not in source, so they don't go stale); the comments below link into
-- its individual sections.
module Main (main) where

import Control.Exception (assert)
import Criterion.Main
import qualified Data.Vector.Storable as VS
import GHC.Exts (build)

type ShapeL = [Int]

-- A faithful copy of orthotope's internal array representation and the
-- pieces of Data.Array.Internal that regime 3 uses, specialised to
-- Storable Double (horde-ad's element storage).
data T = T ![Int] !Int !(VS.Vector Double)  -- strides, offset, values

getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

indexT :: T -> Int -> T
indexT (T (s : ss) o v) i = T ss (o + i * s) v
indexT _ _ = error "indexT"

unScalarT :: T -> Double
unScalarT (T _ o v) = v VS.! o

-- Exactly orthotope's toListT (the otherwise branch; our inputs are
-- never canonical).
toListT :: ShapeL -> T -> [Double]
toListT sh (T ss0 o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarT (T ss o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexT (T ss o v) i of T ss' o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

-- The four strategies compared (README.md#what-it-does).
-- Strategy A: the current fallback.
fbList :: ShapeL -> T -> VS.Vector Double
fbList sh a = VS.fromListN l (toListT sh a) where l = product sh

-- Strategy B: vGenerate + linear-index-to-offset by quotRem (the PR's
-- point 1, as implemented on the orthotope branch). Why this change is
-- not the fix: README.md#why-the-change-is-not-the-fix.
fbGenQuotRem :: ShapeL -> T -> VS.Vector Double
fbGenQuotRem sh (T ats ao v) = VS.generate l (\i -> v VS.! (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (q, r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- Strategy C: as B but with unsafeIndex, to isolate the bounds-check cost.
fbGenUnsafe :: ShapeL -> T -> VS.Vector Double
fbGenUnsafe sh (T ats ao v) = VS.generate l (\i -> VS.unsafeIndex v (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (q, r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- Strategy D: unfoldrExactN with an additive odometer state (point 2) --
-- no division, but an immutable list state rebuilt each step. A truly
-- fused, allocation-free class-method form is untested:
-- README.md#further-untested-ideas.
fbUnfoldAdd :: ShapeL -> T -> VS.Vector Double
fbUnfoldAdd sh (T ats ao v) = VS.unfoldrExactN l step (ao, replicate (length sh) 0)
  where l = product sh
        rsh = reverse sh
        rts = reverse ats
        step (!o, is) = (v VS.! o, adv o is rsh rts)
        adv o []       _        _        = (o, [])
        adv o (i : js) (n : ns) (s : ss)
          | i + 1 < n = (o + s, (i + 1) : js)
          | otherwise = let (o', js') = adv (o - i * s) js ns ss
                        in  (o', 0 : js')
        adv o _ _ _ = (o, [])

-- Build a strided regime-3 T: a normal array of shape `normalSh` viewed
-- with its two innermost dims transposed, so the innermost stride becomes
-- the original innermost dim size -- strided (regime 3) unless that dim
-- is 1. The logical shape returned is the transposed one. Why this models
-- the transpose a conv gather merges in: README.md#where-the-shapes-come-from.
mkStrided :: ShapeL -> (ShapeL, T)
mkStrided normalSh =
  let l = product normalSh
      v = VS.enumFromN (0 :: Double) l
      normalStrides = drop 1 (getStridesT normalSh)
      swapLast2 xs = case reverse xs of (a:b:rest) -> reverse (b:a:rest); _ -> xs
      sh' = swapLast2 normalSh
      st' = swapLast2 normalStrides
  in  (sh', T st' 0 v)

-- Which of toVectorListT's regimes a (shape, T) pair takes: 1 whole-vector
-- memcpy, 2 innermost-normal per-run loop, 3 innermost-strided
-- per-element fallback (the one this benchmark is about). Mirrors the
-- branch logic in Data.Array.Internal.toVectorListT.
regimeOf :: ShapeL -> T -> Int
regimeOf sh (T ats _ v)
  | ats == ts' && VS.length v == l = 1
  | null sh                        = 1
  | oks !! (length sh - 1)         = 2
  | otherwise                      = 3
  where l : ts' = getStridesT sh
        oks = scanr (&&) True (zipWith (==) ats ts')

-- The 24 conv-derived shapes (grouped inline below; see
-- README.md#the-shape-set for where they come from): a full patch tensor
-- is [outH, outW, Cin, KH, KW] -- output spatial, input channels, kernel
-- -- and a per-position slice is [Cin, KH, KW].
convShapes :: [(String, ShapeL)]
convShapes =
  [ -- horde-ad shaped CNN (MnistCnnShaped2; kernel kh+1 = 3)
    ("cnn-L1-6x6-c1",       [6, 6, 1, 3, 3])          -- 324
  , ("cnn-L1-12x12-c1",     [12, 12, 1, 3, 3])        -- 1296
  , ("cnn-L1-24x24-c1",     [24, 24, 1, 3, 3])        -- 5184
  , ("cnn-L2-12x12-c16",    [12, 12, 16, 3, 3])       -- 20736
  , ("cnn-L2-24x24-c32",    [24, 24, 32, 3, 3])       -- 165888
  , ("cnn-slice-c32",       [32, 3, 3])               -- 288  (one position)
  , ("cnn-slice-c64",       [64, 3, 3])               -- 576  (one position)
    -- MNIST LeNet-5
  , ("lenet-L1-28-c1-k5",   [28, 28, 1, 5, 5])        -- 19600
  , ("lenet-L2-14-c6-k5",   [14, 14, 6, 5, 5])        -- 29400
  , ("mnist-28-c1-k3",      [28, 28, 1, 3, 3])        -- 7056
    -- CIFAR-10 scale
  , ("cifar-L1-32-c3-k3",   [32, 32, 3, 3, 3])        -- 27648
  , ("cifar-L2-16-c64-k3",  [16, 16, 64, 3, 3])       -- 147456
  , ("cifar-L3-8-c128-k3",  [8, 8, 128, 3, 3])        -- 73728
  , ("cifar-32-c3-k5",      [32, 32, 3, 5, 5])        -- 76800
    -- ImageNet scale (only the layers whose patch tensor stays tractable)
  , ("resnet-stem-112-c3-k7", [112, 112, 3, 7, 7])    -- 1843968
  , ("vgg-28-c256-k3",      [28, 28, 256, 3, 3])      -- 1806336
  , ("vgg-14-c512-k3",      [14, 14, 512, 3, 3])      -- 903168
  , ("vgg-14-c256-k3",      [14, 14, 256, 3, 3])      -- 451584
  , ("deep-7-c512-k3",      [7, 7, 512, 3, 3])        -- 225792
  , ("alexnet-L1-55-c3-k11",[55, 55, 3, 11, 11])      -- 1098075
  , ("alexnet-L2-27-c48-k5",[27, 27, 48, 5, 5])       -- 874800
    -- horde-ad gather48 benchmark layout [S, K, K, S]
  , ("gather48-src-50",     [50, 3, 3, 50])           -- 22500
  , ("conv1d-24",           [24, 3, 3, 24])           -- 5184
  , ("slice-c512",          [512, 3, 3])              -- 4608  (one position)
  ]

-- Six non-conv shapes stretching the space beyond convolution
-- (README.md#the-shape-set); each is annotated inline with what it probes.
stretchShapes :: [(String, ShapeL)]
stretchShapes =
  [ ("stretch-rank10",      [3,3,3,3,3,3,3,3,3,3])    -- 59049, quotRem x10/elem
  , ("stretch-wide-2xM",    [2, 1000000])             -- 2000000, extreme aspect
  , ("stretch-primes",      [97, 89, 29])             -- 250357, non-2^k arithmetic
  , ("stretch-bigstride",   [3, 3, 200000])           -- 1800000, huge innermost stride
  , ("stretch-square-1400", [1400, 1400])             -- 1960000, rank-2 near-square
  , ("stretch-r5-8x512",    [8, 8, 8, 8, 512])        -- 2097152, big rank-5
  ]

shapes :: [(String, ShapeL)]
shapes = convShapes ++ stretchShapes  -- 24 + 6 = 30

-- Realistic conv layers excluded because their patch tensor (7M-29M
-- elements) is too large to benchmark even for one image; printed at
-- startup as a flag, not run. Which dimensions scale the work, and why
-- only the minibatch dim is free to drop:
-- README.md#dropping-the-minibatch-dimension.
tooBig :: [(String, ShapeL)]
tooBig =
  [ ("vgg-112-c64-k3",      [112, 112, 64, 3, 3])     -- 7225344  (~7M)
  , ("resnet-56-c128-k3",   [56, 56, 128, 3, 3])      -- 3612672  (~3.6M)
  , ("resnet-56-c256-k3",   [56, 56, 256, 3, 3])      -- 7225344  (~7.2M)
  , ("imagenet-224-c64-k3", [224, 224, 64, 3, 3])     -- 28901376 (~29M)
  ]

-- Print the flagged (too-big) shapes, then benchmark every shape in
-- 'shapes'. How to run: README.md#running-it. The numbers and how to
-- read them: README.md#results, README.md#reading-the-results.
main :: IO ()
main = do
  mapM_ (\(n, s) -> putStrLn $ "FLAGGED too big, excluded: " ++ n ++ " "
                               ++ show s ++ ", l=" ++ show (product s))
        tooBig
  benches <- mapM mkBench shapes
  defaultMain benches
  where
    mkBench (name, normalSh) = do
      let (sh, a) = mkStrided normalSh
          rList   = fbList sh a
          agree   = rList == fbGenQuotRem sh a
                 && rList == fbGenUnsafe sh a
                 && rList == fbUnfoldAdd sh a
          reg     = regimeOf sh a
      -- Non-vacuity: every benchmarked shape must actually take regime 3,
      -- and all four strategies must produce the same vector.
      assert (agree && reg == 3) (return ())
      putStrLn $ name ++ ": normalSh " ++ show normalSh ++ " -> strided "
                 ++ show sh ++ ", l=" ++ show (product sh)
                 ++ ", regime=" ++ show reg ++ ", agree=" ++ show agree
      return $ bgroup name
        [ bench "list"        $ whnf (VS.sum . fbList sh) a
        , bench "gen-quotrem" $ whnf (VS.sum . fbGenQuotRem sh) a
        , bench "gen-unsafe"  $ whnf (VS.sum . fbGenUnsafe sh) a
        , bench "unfold-add"  $ whnf (VS.sum . fbUnfoldAdd sh) a
        ]
