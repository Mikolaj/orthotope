{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE RankNTypes #-}
-- | Self-contained benchmark isolating orthotope's toVectorListT regime 3
-- (the per-element fallback for an innermost-strided array), so the
-- candidate fallbacks can be A/B'd without an ox-arrays + horde-ad rebuild.
-- It compares 20 strategies; 'mkStrided' builds a regime-3 input,
-- 'regimeOf' checks it really is one, and the @check@ main mode asserts all
-- strategies agree.
--
-- @README.md@ next to this file is the standalone account -- the full
-- strategy list, shape rationale, the numbers and the verdicts (kept there,
-- not in source, so they don't go stale).
module Main (main) where

import Control.DeepSeq (NFData(..), force)
import Control.Exception (evaluate)
import Control.Monad (foldM_)
import Control.Monad.ST (ST)
import Data.List (foldl')
import Criterion.Main
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Storable.Mutable as VSM
import GHC.Exts (build)
import GHC.Stats (getRTSStats, RTSStats(allocated_bytes))
import System.Environment (getArgs)
import System.Mem (performGC)

type ShapeL = [Int]

-- A faithful copy of orthotope's internal array representation and the
-- pieces of Data.Array.Internal that regime 3 uses, specialised to
-- Storable Double (horde-ad's element storage).
data T = T ![Int] !Int !(VS.Vector Double)  -- strides, offset, values

-- So criterion's 'env' can force the input to normal form before timing.
instance NFData T where
  rnf (T s o v) = rnf s `seq` rnf o `seq` rnf v

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

-- The eleven strategies compared (README.md#what-it-does).

-- Strategy A: the original fallback.
{-# NOINLINE fbList #-}
fbList :: ShapeL -> T -> VS.Vector Double
fbList sh a = VS.fromListN l (toListT sh a) where l = product sh

-- Strategy B: the first attempt -- vGenerate + linear-index-to-offset by
-- quotRem (the PR's point 1), one division per rank. Why it is a mixed
-- picture rather than a fix: README.md#reading-the-results.
{-# NOINLINE fbGenQuotRem #-}
fbGenQuotRem :: ShapeL -> T -> VS.Vector Double
fbGenQuotRem sh (T ats ao v) =
  VS.generate l (\i -> v VS.! (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (!q, !r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- Strategy C: as B but with unsafeIndex, to isolate the bounds-check cost.
{-# NOINLINE fbGenUnsafe #-}
fbGenUnsafe :: ShapeL -> T -> VS.Vector Double
fbGenUnsafe sh (T ats ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (!q, !r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- Strategy D: unfoldrExactN with an additive odometer state (point 2) --
-- no division, but an immutable list state rebuilt each step. It is an
-- allocating proxy for the truly fused, allocation-free form, which is
-- 'fbFused' below (README.md#reading-the-results).
{-# NOINLINE fbUnfoldAdd #-}
fbUnfoldAdd :: ShapeL -> T -> VS.Vector Double
fbUnfoldAdd sh (T ats ao v) =
  VS.unfoldrExactN l step (ao, replicate (length sh) 0)
  where l = product sh
        rsh = reverse sh
        rts = reverse ats
        step (!o, is) = (v VS.! o, adv o is rsh rts)
        adv !o []       _        _        = (o, [])
        adv !o (i : js) (n : ns) (s : ss)
          | i + 1 < n = (o + s, (i + 1) : js)
          | otherwise = let (!o', js') = adv (o - i * s) js ns ss
                        in  (o', 0 : js')
        adv !o _ _ _ = (o, [])

-- Base offset of each innermost run, row-major over the outer dims (all
-- dims but the innermost). Built by the same shared-offset odometer
-- recursion as 'toListT' -- one mul-add per node, outer offsets shared
-- across siblings, no division -- but stopping one dim short and
-- collecting offsets, not values. Length is @product (init sh)@ = the
-- number of runs @m@. The list is short (a factor @s@ smaller than @l@)
-- and consumed immediately by 'VS.fromListN'.
{-# INLINE runBaseOffsets #-}
runBaseOffsets :: Int -> [Int] -> [Int] -> [Int]
runBaseOffsets o0 osh oats = build $ \cons nil ->
  let go []       []         !o rest = cons o rest
      go (n : ns) (st : sts) !o rest =
        foldr (\i r -> go ns sts (o + i * st) r) rest [0 .. n - 1]
      go _        _          !o rest = cons o rest
  in  go osh oats o0 nil

-- The run base-offsets table (length @product osh@) as 'fbBaseOffsetsQuot'
-- builds it:
-- the 'runBaseOffsets' list fed to 'VS.fromListN'. Extracted so the allocation
-- diagnostic (see 'diag') measures the exact benchmarked build.
{-# INLINE baseOffsetsList #-}
baseOffsetsList :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsList o0 osh oats =
  VS.fromListN (product osh) (runBaseOffsets o0 osh oats)

-- The same table as 'fbBQmut' builds it: a mutable odometer fill of the
-- concrete Int scratch, no intermediate list.
{-# INLINE baseOffsetsMut #-}
baseOffsetsMut :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsMut o0 osh oats = VS.create $ do
  b <- VSM.unsafeNew (product osh)
  let go [] [] !q !baseOff = VSM.unsafeWrite b q baseOff >> return (q + 1)
      go (n : ns) (st : sts) !q !baseOff =
        let dim !i !qq
             | i >= n    = return qq
             | otherwise = go ns sts qq (baseOff + i * st) >>= dim (i + 1)
        in  dim 0 q
      go _ _ !q !baseOff = VSM.unsafeWrite b q baseOff >> return (q + 1)
  _ <- go osh oats 0 o0
  return b

-- The same table via a pure 'VS.generate' (no explicit mutation -- the fill
-- is vector's own, hidden like 'VS.fromListN'/'VS.generate' already are in
-- orthotope): each run's base-offset is computed independently by decomposing
-- the run index over the outer natural strides and re-dotting with the actual
-- outer strides. No list, so no transient garbage -- but @rank-1@ quotRems
-- per run instead of the odometer's shared adds.
{-# INLINE baseOffsetsGen #-}
baseOffsetsGen :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsGen o0 osh oats = VS.generate (product osh) baseOffset
  where nts = drop 1 (scanr (*) 1 osh)  -- outer natural (row-major) strides
        baseOffset q = o0 + go q nts oats
        go _  []         []         = 0
        go qq (nt : nts') (st : sts') = case qq `quotRem` nt of
                                          (!a, !b) -> a * st + go b nts' sts'
        go _  _          _          = 0

-- The same table by iterated expansion with 'VS.concatMap' (pure vector,
-- no 'VS.generate', no explicit mutation, no division): the base-offsets grid
-- is separable (@o0 + sum idx_d * stride_d@), so starting from @[o0]@ each
-- outer dimension expands every partial base-offset @a@ into @enumFromStepN a
-- stride_d n_d@ -- the odometer's shared adds, but expressed in vector's
-- stream framework rather than a hand-written loop.
{-# INLINE baseOffsetsExpand #-}
baseOffsetsExpand :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsExpand o0 osh oats = foldl' expand (VS.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VS.concatMap (\a -> VS.enumFromStepN a sd nd) acc

-- As 'baseOffsetsExpand' but with the zip and the strict left fold fused into
-- one hand-written recursion over the two lists (the base package
-- has no combined zip-fold), so the intermediate @zip osh oats@ list
-- of tuples is never built. The tuple list is only rank-1 long,
-- so this can matter at most marginally.
{-# INLINE baseOffsetsExpandZF #-}
baseOffsetsExpandZF :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsExpandZF o0 osh oats = go (VS.singleton o0) osh oats
  where go !acc (nd : nds) (sd : sds) =
          go (VS.concatMap (\a -> VS.enumFromStepN a sd nd) acc) nds sds
        go !acc _          _          = acc

-- Micro-optimised 'baseOffsetsExpand': seed the fold from the first dimension's
-- 'enumFromStepN' (one fewer concatMap layer everywhere, and pure
-- enumFromStepN with no concatMap at all when there is a single outer dim).
{-# INLINE baseOffsetsExpandB #-}
baseOffsetsExpandB :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsExpandB o0 osh oats =
  case zip osh oats of
    []                -> VS.singleton o0
    ((n0, s0) : rest) -> foldl' expand (VS.enumFromStepN o0 s0 n0) rest
  where expand !acc (!nd, !sd) =
          VS.concatMap (\a -> VS.enumFromStepN a sd nd) acc

-- Strict, unpackable state for the fused odometer: current source
-- @offset@, position @j@ within the current run, and run index @q@.
data S3 = S3 !Int !Int !Int

-- Strategy E: the truly-fused, allocation-free additive odometer that
-- 'fbUnfoldAdd' only approximated (its immutable-list state allocated per
-- step). Split off the innermost dim (size @s@, stride @t@):
-- precompute the @m@ run base-offsets once, then step with a strict
-- three-'Int' state that 'unfoldrExactN' + SpecConstr keep
-- in registers. The hot path (still inside a run) is a single add
-- @o + t@; only the @m@ run boundaries touch @baseOffsets@ -- no division, no
-- multiply, no per-step allocation.
{-# NOINLINE fbFused #-}
fbFused :: ShapeL -> T -> VS.Vector Double
fbFused sh (T ats ao v) = VS.unfoldrExactN l step (S3 ao 0 0)
  where l = product sh
        !s = last sh
        !t = last ats
        !m = l `div` s
        !baseOffsets = VS.fromListN m (runBaseOffsets ao (init sh) (init ats))
                         :: VS.Vector Int
        step (S3 o j q) =
          let !x = VS.unsafeIndex v o
              next
                | j + 1 < s = S3 (o + t) (j + 1) q
                | otherwise = let q1 = q + 1
                              in  if q1 < m
                                  then S3 (VS.unsafeIndex baseOffsets q1) 0 q1
                                  else S3 0 0 q1  -- last element; state unused
          in  (x, next)

-- Strategy F: precompute the run base-offsets as in E, but fill with a single
-- 'VS.generate' doing one 'quotRem' (by the innermost size @s@) per
-- element instead of one per rank -- to price the division-count
-- reduction on its own, without E's fully-fused loop.
{-# NOINLINE fbBaseOffsetsQuot #-}
fbBaseOffsetsQuot :: ShapeL -> T -> VS.Vector Double
fbBaseOffsetsQuot sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsList ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Offsets of every element, row-major over (sh, ats), starting at @o0@:
-- 'enumFromStepN' generates each innermost run directly (constant stride,
-- no division) and 'concatMap' nests the outer dims. Pure 'Vector' ops,
-- no intermediate list.
{-# INLINE strideOffsets #-}
strideOffsets :: Int -> [Int] -> [Int] -> VS.Vector Int
strideOffsets o0 sh0 ats0 = go o0 sh0 ats0
  where go o []       []         = VS.singleton o
        go o [n]      [st]       = VS.enumFromStepN o st n
        go o (n : ns) (st : sts) =
          VS.concatMap (\b -> go b ns sts) (VS.enumFromStepN o st n)
        go o _        _          = VS.singleton o

-- Strategy G: build the whole offset vector with the all-'Vector'
-- 'strideOffsets', then gather through 'unsafeBackpermute' (vector's
-- tight, fused indexing loop). Two passes over @l@ and an extra
-- 'Int'-vector, but every step is a plain memory read.
{-# NOINLINE fbBackperm #-}
fbBackperm :: ShapeL -> T -> VS.Vector Double
fbBackperm sh (T ats ao v) = VS.unsafeBackpermute v (strideOffsets ao sh ats)

-- Strategy H: the class-methods-only shape -- the only one expressible
-- in orthotope's abstract 'Data.Array.Internal' without a new 'Vector'
-- method or a concrete 'Int' scratch. It mirrors the existing regime-2
-- branch (recurse over the outer dims collecting a DList, then 'vConcat')
-- but, since the innermost dim is strided, emits each run as a strided
-- 'VS.generate' (constant-stride reads, no division) rather than an
-- @O(1)@ 'VS.slice'. Costs @m@ small allocations plus the concat copy;
-- whether that beats the single-vector strategies is what this measures.
{-# NOINLINE fbConcatRuns #-}
fbConcatRuns :: ShapeL -> T -> VS.Vector Double
fbConcatRuns sh (T ats ao v) = VS.concat (go (init sh) (init ats) ao [])
  where s = last sh
        !t = last ats
        run !baseOff = VS.generate s (\j -> VS.unsafeIndex v (baseOff + j * t))
        go []       []         !o rest = run o : rest
        go (n : ns) (st : sts) !o rest =
          foldr (\i r -> go ns sts (o + i * st) r) rest [0 .. n - 1]
        go _        _          !o rest = run o : rest

-- Strategy I: the mutable run-fill -- the tightest pure-'Vector' shape,
-- but needing an escape to a mutable buffer that orthotope's class does
-- not expose (this prototypes what a new class method would enable).
-- Allocate the result once ('VS.create'), walk the outer odometer, and
-- for each innermost run write @sInner@ elements with a tight inner loop
-- of pure additions -- no quotRem, no run base-offsets list, no per-run
-- allocation, no per-element state machine. @go@ returns the next output
-- position so siblings advance it without arithmetic.
{-# NOINLINE fbMutOdo #-}
fbMutOdo :: ShapeL -> T -> VS.Vector Double
fbMutOdo sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go []       []         !outPos !baseOff =
        writeRun outPos baseOff >> return (outPos + sInner)
      go (n : ns) (st : sts) !outPos !baseOff =
        let dim !i !op | i >= n    = return op
                       | otherwise = go ns sts op (baseOff + i * st)
                                     >>= dim (i + 1)
        in  dim 0 outPos
      go _        _          !outPos !baseOff =
        writeRun outPos baseOff >> return (outPos + sInner)
  _ <- go (init sh) (init ats) 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats

-- Strategy J: as I but iterating the precomputed run base-offsets list,
-- to price what the base-offsets list (a factor @sInner@ smaller than @l@)
-- costs the odometer-free variant against 'fbMutOdo'.
{-# NOINLINE fbMutBaseOffsets #-}
fbMutBaseOffsets :: ShapeL -> T -> VS.Vector Double
fbMutBaseOffsets sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
  foldM_ (\ !outPos !baseOff -> writeRun outPos baseOff
                                >> return (outPos + sInner))
         0 (runBaseOffsets ao (init sh) (init ats))
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats

-- Prototype of the one new 'Vector'-class method a mutable run-fill would
-- need: allocate a length-@n@ vector and let the caller populate every
-- index once through an unsafe writer, hidden behind @forall s@ so the
-- mutable buffer cannot leak. This mirrors exactly what the orthotope
-- instance would implement; 'fbBuild' below drives it with the same
-- odometer as 'fbMutOdo', so timing 'build' against 'mut-odo' prices
-- whether wrapping the fill in this general method costs the tight loop.
vBuildVS :: Int
         -> (forall s. (Int -> Double -> ST s ()) -> ST s ())
         -> VS.Vector Double
{-# INLINE vBuildVS #-}
vBuildVS n fill = VS.create $ do
  out <- VSM.unsafeNew n
  fill (VSM.unsafeWrite out)
  return out

-- Strategy K: 'fbMutOdo' expressed through the general 'vBuildVS' method,
-- to confirm the class-method abstraction is free (i.e. it inlines to the
-- same code as the hand-written mutable fill).
{-# NOINLINE fbBuild #-}
fbBuild :: ShapeL -> T -> VS.Vector Double
fbBuild sh (T ats ao v) = vBuildVS l $ \write ->
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = write (outPos + j) (VS.unsafeIndex v src)
                              >> inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go []       []         !outPos !baseOff =
        writeRun outPos baseOff >> return (outPos + sInner)
      go (n : ns) (st : sts) !outPos !baseOff =
        let dim !i !op | i >= n    = return op
                       | otherwise = go ns sts op (baseOff + i * st)
                                     >>= dim (i + 1)
        in  dim 0 outPos
      go _        _          !outPos !baseOff =
        writeRun outPos baseOff >> return (outPos + sInner)
  in  go (init sh) (init ats) 0 ao >> return ()
  where l = product sh
        !sInner = last sh
        !tInner = last ats

-- Strategy L: 'fbBaseOffsetsQuot' with the run base-offsets built by a mutable
-- odometer fill of a concrete 'Int' scratch ('VS.create'/'VSM') instead of
-- @VS.fromListN (runBaseOffsets ...)@ -- dropping the @l/sInner@-element
-- intermediate list. This is NOT a class extension: the abstract output is
-- still produced by the ordinary 'VS.generate', and only the concrete Int
-- scratch (which 'fbBaseOffsetsQuot' already uses) is built differently.
-- Tests how much of 'fbMutOdo's edge is just the base-offsets list.
{-# NOINLINE fbBQmut #-}
fbBQmut :: ShapeL -> T -> VS.Vector Double
fbBQmut sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsMut ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Strategy M: 'fbBQmut' but with the run base-offsets built by the pure
-- 'baseOffsetsGen' ('VS.generate', no explicit mutation) instead
-- of 'baseOffsetsMut'. Answers "can the base-offsets be built fast without
-- explicit vector mutation?".
{-# NOINLINE fbBQgen #-}
fbBQgen :: ShapeL -> T -> VS.Vector Double
fbBQgen sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsGen ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Strategy N: 'fbBQmut' but with the run base-offsets built by the pure
-- 'baseOffsetsExpand' ('VS.concatMap', no explicit mutation) instead of
-- 'baseOffsetsMut'. The concatMap route to answering the no-mutation question.
{-# NOINLINE fbBQexpand #-}
fbBQexpand :: ShapeL -> T -> VS.Vector Double
fbBQexpand sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Strategy O: fbBQexpand' with the fused zip-fold 'baseOffsetsExpandZF'
-- base-offsets build.
{-# NOINLINE fbBQexpandZF #-}
fbBQexpandZF :: ShapeL -> T -> VS.Vector Double
fbBQexpandZF sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpandZF ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Strategy P: 'fbBQexpand' with the micro-optimised 'baseOffsetsExpandB'.
{-# NOINLINE fbBQexpandB #-}
fbBQexpandB :: ShapeL -> T -> VS.Vector Double
fbBQexpandB sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpandB ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Strategy Q: also drop the output's per-element quotRem. The output is a
-- separable gather (offset[q*s+j] = baseOffsets[q] + j*t), so expand the outer
-- base-offsets as before, then gather with a FUSED 'map . concatMap': for each
-- base-offset, 'enumFromStepN' the inner run and read @v@. vector fuses
-- @map f (concatMap g x)@ into one stream, so there is no quotRem anywhere
-- and no full l-length offset table -- only the m-length base-offsets
-- materialise.
{-# NOINLINE fbCMGather #-}
fbCMGather :: ShapeL -> T -> VS.Vector Double
fbCMGather sh (T ats ao v) =
  VS.map (VS.unsafeIndex v)
         (VS.concatMap (\b -> VS.enumFromStepN b t s) baseOffsets)
  where s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (init ats)

-- Strategy R: the whole offset grid over ALL dims via 'baseOffsetsExpand', then
-- one gather. Materialises the full l-length offset table (foldl' forces
-- each level), so it prices what strategy Q's fused inner run avoids.
{-# NOINLINE fbAllExpand #-}
fbAllExpand :: ShapeL -> T -> VS.Vector Double
fbAllExpand sh (T ats ao v) =
  VS.map (VS.unsafeIndex v) (baseOffsetsExpand ao sh ats)

-- Strategy S: the full offset table (length @l@) built by the same mutable
-- odometer as 'fbMutOdo', then gathered with a single 'VS.generate' whose
-- callback is one contiguous Int read plus one strided value read -- no
-- quotRem, no multiply. Class-only (output via 'VS.generate'), but two
-- passes over @l@ and an @l@-sized Int scratch: prices whether dropping the
-- per-element arithmetic is worth the extra pass 'fbMutOdo' avoids.
{-# NOINLINE fbOffTab #-}
fbOffTab :: ShapeL -> T -> VS.Vector Double
fbOffTab sh (T ats ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (VS.unsafeIndex offs i))
  where l = product sh
        !s = last sh
        !t = last ats
        offs :: VS.Vector Int
        !offs = VS.create $ do
          o <- VSM.unsafeNew l
          let writeRun !outPos !baseOff =
                let inner !j !src
                      | j >= s    = return ()
                      | otherwise = VSM.unsafeWrite o (outPos + j) src
                                    >> inner (j + 1) (src + t)
                in  inner 0 baseOff
              go [] [] !outPos !baseOff =
                writeRun outPos baseOff >> return (outPos + s)
              go (n : ns) (st : sts) !outPos !baseOff =
                let dim !i !op | i >= n    = return op
                               | otherwise = go ns sts op (baseOff + i * st)
                                             >>= dim (i + 1)
                in  dim 0 outPos
              go _ _ !outPos !baseOff = writeRun outPos baseOff
                                        >> return (outPos + s)
          _ <- go (init sh) (init ats) 0 ao
          return o

-- Strategy T: 'fbBQmut' but building the base-offsets with 'VS.unfoldrExactN'
-- (a pure-typed builder whose mutation stays inside the vector library,
-- like 'VS.generate') instead of the explicit 'VS.create'/'VSM' fill of
-- 'fbBQmut'. No list, no explicit mutation in this module -- but the
-- odometer state is an immutable @[Int]@ rebuilt per run. Prices whether
-- the no-list base-offsets win survives without explicit mutation.
{-# NOINLINE fbBQunfold #-}
fbBQunfold :: ShapeL -> T -> VS.Vector Double
fbBQunfold sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        m = l `div` max 1 s
        rosh = reverse (init sh)
        roats = reverse (init ats)
        baseOffsets :: VS.Vector Int
        !baseOffsets = VS.unfoldrExactN m step (ao, replicate (length sh - 1) 0)
          where step (!o, is) = (o, adv o is rosh roats)
                adv !o []       _        _        = (o, [])
                adv !o (i : js) (n : ns) (st : sts)
                  | i + 1 < n = (o + st, (i + 1) : js)
                  | otherwise = let (!o', js') = adv (o - i * st) js ns sts
                                in  (o', 0 : js')
                adv !o _ _ _ = (o, [])
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

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
      swapLast2 xs = case reverse xs of
        (a:b:rest) -> reverse (b:a:rest); _ -> xs
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
  args <- getArgs
  if "diag" `elem` args
    then diag
    else if "check" `elem` args
      then check
      else defaultMain (map mkBench shapes)

-- Benchmark one shape. Criterion's 'env' builds the input once and forces it
-- to normal form before the clock starts, so input construction is excluded
-- from timing and the source vector is fully materialised. The
-- agreement/regime check is deliberately NOT here -- it lives in the separate
-- 'check' mode, so the timed program never even computes it and thus cannot
-- share (CSE) a strategy's result between the check and the benchmark.
mkBench :: (String, ShapeL) -> Benchmark
mkBench (name, normalSh) =
  env (evaluate (force (mkStrided normalSh))) $ \ ~(sh, a) ->
    bgroup name
      [ bench "list"        $ whnf (VS.sum . fbList sh) a
      , bench "gen-quotrem" $ whnf (VS.sum . fbGenQuotRem sh) a
      , bench "gen-unsafe"  $ whnf (VS.sum . fbGenUnsafe sh) a
      , bench "unfold-add"  $ whnf (VS.sum . fbUnfoldAdd sh) a
      , bench "fused"       $ whnf (VS.sum . fbFused sh) a
      , bench "offsets-quot" $ whnf (VS.sum . fbBaseOffsetsQuot sh) a
      , bench "backperm"    $ whnf (VS.sum . fbBackperm sh) a
      , bench "concat-runs" $ whnf (VS.sum . fbConcatRuns sh) a
      , bench "mut-odo"     $ whnf (VS.sum . fbMutOdo sh) a
      , bench "mut-offsets" $ whnf (VS.sum . fbMutBaseOffsets sh) a
      , bench "build"       $ whnf (VS.sum . fbBuild sh) a
      , bench "bq-mut"      $ whnf (VS.sum . fbBQmut sh) a
      , bench "offtab"      $ whnf (VS.sum . fbOffTab sh) a
      , bench "bq-unfold"   $ whnf (VS.sum . fbBQunfold sh) a
      , bench "bq-gen"      $ whnf (VS.sum . fbBQgen sh) a
      , bench "bq-expand"   $ whnf (VS.sum . fbBQexpand sh) a
      , bench "bq-expand-zf" $ whnf (VS.sum . fbBQexpandZF sh) a
      , bench "bq-expand-b" $ whnf (VS.sum . fbBQexpandB sh) a
      , bench "cm-gather"   $ whnf (VS.sum . fbCMGather sh) a
      , bench "all-expand"  $ whnf (VS.sum . fbAllExpand sh) a
      ]

-- Correctness / non-vacuity, in its own mode (@cabal run micro -- check@) so
-- it runs as a separate process from the timed benchmark: every shape must
-- take regime 3 and every strategy must produce the same vector as 'fbList'.
check :: IO ()
check = do
  mapM_ (\(n, s) -> putStrLn $ "FLAGGED too big, excluded: " ++ n ++ " "
                               ++ show s ++ ", l=" ++ show (product s))
        tooBig
  mapM_ one shapes
  where
    one (name, normalSh) = do
      let (sh, a) = mkStrided normalSh
          rList   = fbList sh a
          agree   = rList == fbGenQuotRem sh a
                 && rList == fbGenUnsafe sh a
                 && rList == fbUnfoldAdd sh a
                 && rList == fbFused sh a
                 && rList == fbBaseOffsetsQuot sh a
                 && rList == fbBackperm sh a
                 && rList == fbConcatRuns sh a
                 && rList == fbMutOdo sh a
                 && rList == fbMutBaseOffsets sh a
                 && rList == fbBuild sh a
                 && rList == fbBQmut sh a
                 && rList == fbOffTab sh a
                 && rList == fbBQunfold sh a
                 && rList == fbBQgen sh a
                 && rList == fbBQexpand sh a
                 && rList == fbBQexpandZF sh a
                 && rList == fbBQexpandB sh a
                 && rList == fbCMGather sh a
                 && rList == fbAllExpand sh a
          reg     = regimeOf sh a
      putStrLn $ name ++ ": normalSh " ++ show normalSh ++ " -> strided "
                 ++ show sh ++ ", l=" ++ show (product sh)
                 ++ ", regime=" ++ show reg ++ ", agree=" ++ show agree
      if agree && reg == 3
        then return ()
        else error ("CHECK FAILED: " ++ name)

-- Allocation diagnostic (run with @cabal run micro -- diag@): why is
-- 'fbBQmut' faster than 'fbBaseOffsetsQuot' when they share the same
-- 'VS.generate' output and the same @m@-element run base-offsets table?
-- Measure the heap a single base-offsets build allocates.
-- 'baseOffsetsList' feeds a lazy 'runBaseOffsets' list to 'VS.fromListN';
-- if that fused, no list would be materialized and its allocation
-- would match 'baseOffsetsMut' (a direct mutable fill of the same @m@ Ints).
-- The offset seed varies per build to defeat CSE; 'VS.sum' forces
-- the whole vector.
diag :: IO ()
diag = do
  putStrLn "=== heap allocated per run base-offsets build (bytes), lower is leaner ==="
  putStrLn "(both build the SAME m-element VS.Vector Int; only the method differs)"
  mapM_ one [ ("cnn-L1-24x24 [24,24,1,3,3]",  [24, 24, 1, 3, 3])
            , ("vgg-28-c256  [28,28,256,3,3]", [28, 28, 256, 3, 3]) ]
  where
    one (name, normalSh) = do
      let (sh, T ats _ _) = mkStrided normalSh
          osh  = init sh
          oats = init ats
          m    = product osh
      putStrLn $ "\n" ++ name ++ "  (m = " ++ show m ++ " base-offsets, "
                 ++ show (VS.length (baseOffsetsMut 0 osh oats)) ++ " built)"
      measure "  baseOffsetsList   fromListN . runBaseOffsets (lazy list) " (\k -> baseOffsetsList   k osh oats)
      measure "  baseOffsetsGen    VS.generate + per-run quotRem          " (\k -> baseOffsetsGen    k osh oats)
      measure "  baseOffsetsExpand VS.concatMap iterated expansion        " (\k -> baseOffsetsExpand k osh oats)
      measure "  baseOffsetsMut    VS.create mutable odometer             " (\k -> baseOffsetsMut    k osh oats)
    measure label build = do
      let n = 500 :: Int
      performGC
      s0 <- getRTSStats
      let loop !acc !k | k >= n    = acc
                      | otherwise = loop (acc + VS.sum (build k)) (k + 1)
      tot <- evaluate (loop (0 :: Int) 0)
      s1 <- getRTSStats
      let bytes =
            (fromIntegral (allocated_bytes s1 - allocated_bytes s0) :: Int)
            `div` n
      putStrLn $ label ++ ": "
                 ++ show bytes ++ " bytes  (checksum "
                 ++ show tot ++ ")"
