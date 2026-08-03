{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE MagicHash #-}
{-# LANGUAGE UnboxedTuples #-}
{-# LANGUAGE RankNTypes #-}
-- | Self-contained benchmark isolating orthotope's toVectorListT regime 3
-- (the per-element fallback for an innermost-strided array), so the
-- candidate fallbacks can be A/B'd without an ox-arrays + horde-ad rebuild.
-- It compares the candidate strategies; 'mkStrided' builds a regime-3 input,
-- 'regimeOf' checks it really is one, and the @check@ main mode asserts all
-- strategies agree.
--
-- The strategies are defined below in the four families README.md groups them
-- into, base before variant; 'roster' holds the different order they are RUN
-- in, and is the one list both the benchmark and @check@ are built from.
--
-- @README.md@ next to this file is the standalone account -- the full
-- strategy list, shape rationale, the numbers and the verdicts (kept there,
-- not in source, so they don't go stale).
module Main (main) where

import Control.DeepSeq (NFData(..), force)
import Control.Exception (assert, evaluate)
import Control.Monad (foldM_)
import Control.Monad.ST (ST)
import Data.Bits ((.&.), countLeadingZeros, shiftR)
import Data.Int (Int32)
import Data.List (foldl')
import Criterion.Main
import Criterion.Types (Config(regressions))
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Storable.Mutable as VSM
import GHC.Exts (build, int2Word#, quotRemInt#, timesWord2#, word2Int#,
                 Int(..), Word(..))
import GHC.Stats (getRTSStats,
                  RTSStats(allocated_bytes, elapsed_ns, max_live_bytes,
                           max_mem_in_use_bytes))
import System.Environment (getArgs)
import System.IO (hPutStrLn, stderr)
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

-- The size preconditions the fast paths rest on, stated as assertions at the
-- construct each one guards: 'lemireFits' beside the magic that needs it,
-- 'int32Fits' beside the narrowed table that needs it.
--
-- Both are VACUOUS here and are meant to stay so. The largest shape in the
-- set is 'sizeCap' elements, some thousandfold under the smaller of the two
-- bounds, and the -M2G heap cap in micro.cabal keeps any future shape in the
-- same range. So neither assertion can fire on any input this harness
-- produces. The usual non-vacuity proof splits in two here: breaking the
-- PREDICATE is possible -- make 'lemireFits' constantly False and @check@
-- fails at the first shape, which is how to confirm that -fno-ignore-asserts
-- is in effect and these are compiled in rather than dropped -- while
-- breaking the PRECONDITION is not, needing a 17GB source or a 34GB result.
-- So what they establish is that they fire when false, not that they can be
-- made false.
-- They are written anyway, because this benchmark
-- is the design record for a change to Data/Array/Internal.hs, and the thing
-- a reader must not conclude from a green shape set is that the fast paths are
-- unconditionally valid. A shipped version turns each assertion into a real
-- dispatch that falls back to the quotRem/Int fill; asserting is right here
-- because timing a branch that is never taken would only ever time the branch.
--
-- The two bounds are on DIFFERENT quantities and neither implies the other --
-- which is exactly what this harness cannot show, since 'mkStrided' gives
-- every view a source of its own length, so here the two differ only by a
-- factor of two. In orthotope a strided view is a window onto someone else's
-- buffer, so a two-element view of a three-billion-element array clears
-- 'lemireFits' by nine orders of magnitude and fails 'int32Fits'. A shipped
-- dispatch therefore needs both tests, not one standing in for the other.

-- Lemire's identity holds for @d, n < 2^32@. Here @n@ is the linear output
-- index, bounded by @l@, and @d@ is the innermost extent, which divides @l@ --
-- so bounding @l@ bounds both.
{-# INLINE lemireFits #-}
lemireFits :: Int -> Bool
lemireFits l = l <= 4294967296  -- 2^32

-- An Int32 offset table needs every offset it stores to fit. Offsets are
-- indices into the source vector, so its length bounds them; Int32 is signed,
-- hence 2^31 and not 2^32. Sufficient without inspecting the strides, and so
-- correct for the negative ones @rev@ produces.
{-# INLINE int32Fits #-}
int32Fits :: VS.Vector Double -> Bool
int32Fits v = VS.length v <= 2147483648  -- 2^31

-- The division tricks the builders and the strategies below both reach for.

-- Lemire's multiplicative-inverse division (arXiv 2012.12369): with
-- @M = floor(2^64/d) + 1@ precomputed once per divisor, @n div d@ is the high
-- word of @M*n@ and @n mod d@ the high word of @(M*n)*d@ -- two 64x64->128
-- multiplies instead of a division.  Valid for @d, n < 2^32@, which every
-- outer natural stride and run index here is.  @d == 1@ is the one case the
-- formula overflows (M would be 2^64), so it is taken separately and flagged
-- by a 0 magic, which no legal divisor can produce.  @d == 0@ takes the same
-- exit for a different reason: the formula would divide by zero, and a zero
-- extent means @l == 0@, so whatever magic it yields is never read.  Keeping
-- 'magicOf' total on non-negative divisors is what lets the degenerate shapes
-- in 'degenerateShapes' reach 'check' at all.
{-# INLINE mulhi #-}
mulhi :: Word -> Word -> Word
mulhi (W# a) (W# b) = case timesWord2# a b of (# hi, _ #) -> W# hi

{-# INLINE magicOf #-}
magicOf :: Int -> Word
magicOf d | d <= 1 = 0
          | otherwise = (maxBound `quot` fromIntegral d) + 1

-- One 'timesWord2#' yields both halves of @M*n@: the quotient is its high
-- word, and its low word is exactly the product the remainder step needs. An
-- earlier version took the quotient from 'mulhi' and then recomputed the low
-- half as a separate @m * nw@, which is a third multiply the algorithm does
-- not call for; a Core dump is what showed it, and fixing it is what turned
-- the output site into a win
-- (README.md#lemire-multiplicative-inverses-at-the-two-division-sites).
-- Both result components are forced here rather than left to the caller's
-- @(!q, !j)@ pattern: inlined into a strict case GHC fuses the tuple away
-- either way, but the bangs are what keep a context where it does not inline
-- -- another GHC, a bigger enclosing loop -- from building a remainder thunk
-- per element.
{-# INLINE fastQR #-}
fastQR :: Word -> Int -> Int -> (Int, Int)
fastQR 0 _ n = (n, 0)
fastQR (W# m) d (I# n) = case timesWord2# m (int2Word# n) of
  (# hi, lo #) -> let !q = I# (word2Int# hi)
                      !r = fromIntegral (mulhi (W# lo) (fromIntegral d))
                  in  (q, r)

-- Granlund-Montgomery round-up magic for dividends below 2^63 -- which is
-- every nonnegative Int, so every vector index -- against the Lemire form's
-- @n < 2^32@. With @L = ceil(log2 d)@ and @M = 2^(63+L) `div` d + 1@, the
-- quotient of any such n by d is @mulhi M n >> (L-1)@: one multiply-high
-- and one shift, no fixup branch, no bound on the array. The magic-width
-- theorem behind it: a round-up magic of width dividend-bits + L is exact,
-- and Int dividends spend only 63 bits, so M always fits one Word for
-- d >= 2 and the general form's 65-bit add-fixup never arises. Powers of
-- two need no special case (d = 2^L gives M = 2^63 + 1, whose
-- multiply-and-shift is exactly @n >> L@); @d <= 1@ returns the (0, 0)
-- sentinel, total for the same reason 'magicOf' is -- the callers' banged
-- bindings force it on paths their @s == 1@ guard never uses. The setup
-- division runs through Integer, once per call. Correctness is gated by
-- the agreement check like everything else, but its hard cases (l at and
-- past 2^32) are unreachable by any buildable shape -- a shipped form owes
-- the helper a standalone property test against 'quotRem' over adversarial
-- (n, d).
{-# INLINE gmMagic #-}
gmMagic :: Int -> (Word, Int)
gmMagic d
  | d <= 1 = (0, 0)
    -- Both components forced here rather than left to the callers' banged
    -- bindings, for the reason 'fastQR' gives: it costs nothing where the
    -- caller does force them, and keeps a context that does not from
    -- carrying two thunks into a per-element loop.
  | otherwise = let !mg = fromInteger (2 ^ (63 + lg) `div` toInteger d + 1)
                    !sh = lg - 1
                in  (mg, sh)
  where !lg = 64 - countLeadingZeros (fromIntegral d - 1 :: Word)

-- The run base-offsets table: the same @product (init sh)@ offsets, built
-- every way the strategies below want them. 'baseOffsetsList' is the
-- reference @check@'s @builds@ arm holds the rest to.

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

-- Int32 twin of 'baseOffsetsMut'. NO STRATEGY BUILDS WITH IT -- it is kept as
-- the specimen the narrowing question is argued against, and two comments
-- define themselves by the contrast with it: 'baseOffsetsExpand32''s, and the
-- NB on 'fbBQexpand32LemireMulback''s table. Here the odometer arithmetic
-- stays in Int and ONLY the store narrows, so every value written is a final
-- base offset and the single new failure mode is a write at or above 2^31,
-- which 'int32Fits' bounds exactly. That is what makes
-- 'baseOffsetsExpand32''s soundness TODO mean something: there the arithmetic
-- runs in Int32 as well, so the intermediates must fit too and 'int32Fits'
-- stops being the whole precondition. Delete this and that distinction has
-- nothing to point at.
--
-- 'int32Fits' is a bound on the SOURCE and independent of the 'lemireFits'
-- bound on the result: neither implies the other, and a shipped dispatch
-- needs both. Kept a monomorphic copy like the rest of the 'baseOffsets*'
-- family, so the fill's inner loop stays concrete.
{-# INLINE baseOffsetsMut32 #-}
baseOffsetsMut32 :: Int -> [Int] -> [Int] -> VS.Vector Int32
baseOffsetsMut32 o0 osh oats = VS.create $ do
  b <- VSM.unsafeNew (product osh)
  let go [] [] !q !baseOff = VSM.unsafeWrite b q (fromIntegral baseOff)
                             >> return (q + 1)
      go (n : ns) (st : sts) !q !baseOff =
        let dim !i !qq
             | i >= n    = return qq
             | otherwise = go ns sts qq (baseOff + i * st) >>= dim (i + 1)
        in  dim 0 q
      go _ _ !q !baseOff = VSM.unsafeWrite b q (fromIntegral baseOff)
                           >> return (q + 1)
  _ <- go osh oats 0 o0
  return b

-- 'baseOffsetsMut' with the split-innermost treatment the rest of this file
-- lives by, applied one level up: along the innermost OUTER dimension the
-- offsets are an arithmetic progression (stride @st_last@), so they are
-- written by a dedicated additive loop -- store, add, compare -- and the
-- generic odometer recursion runs once per @n_last@ writes instead of once
-- per write. At -O1 the difference is real: SpecConstr, which would
-- specialise the empty-spine call pattern of 'baseOffsetsMut''s leaf away,
-- runs only at -O2, so there every write pays a call, two list-constructor
-- matches and a multiply that this loop does not.
--
-- The check gate is proven non-vacuous on exactly this code path: the
-- first draft of this function had the guards of @dim@ inverted, wrote
-- nothing, and the agreement check failed at the first shape.
{-# INLINE baseOffsetsMutRuns #-}
baseOffsetsMutRuns :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsMutRuns o0 osh oats = VS.create $ do
  b <- VSM.unsafeNew (product osh)
  if null osh
    then VSM.unsafeWrite b 0 o0
    else do
      let !nLast  = last osh
          !stLast = last oats
          writeRun !q0 !off0 =
            let inner !j !off
                  | j >= nLast = return ()
                  | otherwise  = VSM.unsafeWrite b (q0 + j) off
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

-- 'baseOffsetsGen' with its per-run quotRems replaced by 'fastQR', and
-- nothing else changed. This is the per-dimension division site -- one per
-- rank per run, with a magic list walked in step with the strides; the other
-- site Lemire is measured at is the per-element output, in
-- 'fbBQexpandLemireOut' below.
{-# INLINE baseOffsetsGenLemire #-}
baseOffsetsGenLemire :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsGenLemire o0 osh oats =
    -- In the builder for the same reason as in 'baseOffsetsScan': run
    -- indices and outer natural strides are both bounded by the run count.
    assert (lemireFits (product osh))
  $ VS.generate (product osh) baseOffset
  where nts = drop 1 (scanr (*) 1 osh)
        ms  = map magicOf nts
        baseOffset q = o0 + go q ms nts oats
        go _  []        _           _          = 0
        go qq (m : ms') (nt : nts') (st : sts') = case fastQR m nt qq of
                                          (!a, !b) -> a * st + go b ms' nts' sts'
        go _  _         _           _          = 0

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

-- Int32 twin of 'baseOffsetsExpand'. Unlike 'baseOffsetsMut32' the
-- arithmetic itself runs in Int32 -- 'enumFromStepN' generates in the
-- element type -- so every 'concatMap' intermediate halves too, not only
-- the final table. Sound whenever every offset fits in Int32: the partial
-- base-offsets are sums of non-negative index*stride terms, each bounded
-- by a full offset, so no intermediate exceeds what the final table holds.
--
-- TODO: that soundness argument is harness-scoped -- every 'mkStrided'
-- stride is positive, but orthotope's rev'd views carry negative strides,
-- under which the partial sums are mixed-sign and need their own bound; a
-- shipped Int32 variant must restate it for those.
{-# INLINE baseOffsetsExpand32 #-}
baseOffsetsExpand32 :: Int -> [Int] -> [Int] -> VS.Vector Int32
baseOffsetsExpand32 o0 osh oats =
  foldl' expand (VS.singleton (fromIntegral o0)) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VS.concatMap (\a -> VS.enumFromStepN a (fromIntegral sd) nd) acc

-- The run base-offsets as a prefix sum. Consecutive table entries differ by
-- only rank-many distinct values: @st_last@ within a stretch of the
-- innermost outer dimension, and at each odometer carry a per-level
-- constant -- the increment at the carrying level minus the rewind of every
-- level below it, @st_c - sum_{j>c} (n_j - 1) * st_j@. So the table is
-- @scanl' (+) o0@ over a delta stream, and 'VS.scanl'' is the one
-- pure-typed builder whose contract IS stateful-in-order -- the loophole in
-- "'VS.generate' is stateless" that no other strategy here uses.
--
-- The allocation half of that hope is REFUTED, by @diag@ and not by
-- argument: its figures are this comment's.
-- Stream fusion does collapse generate-then-scan into one loop with one
-- vector allocation -- but at -O1 the loop's state is a heap-allocated
-- @Either _ (Int, Int)@ rebuilt every entry: Right + pair + two I# boxes
-- = 9 words = 72 bytes per entry, measured exactly by @diag@ (10x the
-- table's own bytes on vgg-14-c512, against 1.00x for the mutable fills)
-- and visible in Core as boxed joinrec state. Dissolving compound stream
-- state is SpecConstr's job, and SpecConstr runs only at -O2; 'VS.generate'
-- escapes at -O1 only because its state is a bare Int index, which
-- worker/wrapper alone unboxes. The same tax is what the fused (20.7x),
-- bq-unfold (10.2x) and unfold-add (29.9x) rows were already paying: at
-- -O1, every stateful pure-typed builder boxes its state per step, and
-- only index-only 'VS.generate' and explicit mutable fills do not. So the
-- scan build allocates like 'baseOffsetsExpand' (a few percent apart on
-- the diag), not like 'baseOffsetsMut', and its strategies inherit
-- bq-expand-class allocation.
--
-- At -O2 the refutation inverts: SpecConstr dissolves the state and the
-- diag measures this build allocation-free (table + ~500 bytes on
-- vgg-14-c512, matching 'baseOffsetsMut'; 'baseOffsetsGen' and
-- 'baseOffsetsGenLemire' collapse to table-only too, while the expands
-- keep their intermediates, which are data, not state). So the failure
-- belongs to the compilation regime, not the design; -O1 is what this
-- harness measures because it is what a default cabal build of orthotope
-- ships, and promoting the design means shipping the flag -- e.g.
-- OPTIONS_GHC -O2 on Data/Array/Internal.hs -- which is a maintainer
-- decision with its own measurement (time at -O2 is unmeasured here, for
-- every strategy).
--
-- Two setup normalizations keep the per-entry work honest. Unit dims are
-- elided: a radix-1 digit always wraps and adds @(n - 1) * st = 0@ to the
-- rewind, so dropping those pairs changes nothing -- and it removes
-- 'magicOf''s 0-sentinel case from the hot loop (the hoisted level is
-- always a real radix) and picks the first non-1 radix as that level,
-- which is what makes an innermost extent of 1 cost nothing instead of a
-- carry per entry. And the divisibility test is mul-back: the remainder
-- is needed only against zero, and @r == 0@ iff @p == c * nLast@, so the
-- hot path is one multiply-high, one multiply and a compare -- no second
-- 'timesWord2#', no 'quotRem'. Only real carries, a @1/nLast@ fraction of
-- entries, walk the (paired) dims list -- so the per-entry list walk that
-- sank 'baseOffsetsGenLemire' never happens.
--
-- What this builder buys is a TIER, not a percentage, and that is the reason
-- to care about it. Both consumers -- 'fbBQscanMulback' and 'fbOffTabScan' --
-- produce their result through 'VS.generate' and build their table with this
-- scan, so neither needs the mutable concrete-Int scratch that their controls
-- 'fbBQmut' and 'fbOffTab' rest on, and neither needs a new 'Vector' class
-- method: the table is concrete index scratch, as the shipped
-- 'baseOffsetsExpand' one already is. Orthotope's library carries no mutable
-- code, so that is the difference between a shipping candidate and a mere
-- bound on what purity costs. 'fbOffTab' is the fastest strategy needing no
-- new class method, and the fastest pure strategy is well behind it, so if
-- 'fbOffTabScan' holds its control then the pure frontier moves further than
-- every Lemire substitution here moved it -- and two rows of the README's
-- @needs@ column become "nothing (pure)". Figures stay in README.md, as
-- everywhere else in this file.
--
-- The @m == 0@ guard keeps the LENGTH CONTRACT, and that alone. A zero
-- dimension passes the unit-dim filter (@n /= 1@ keeps 0); without the guard
-- the scan returns a one-element table where 'baseOffsetsExpand' and
-- 'baseOffsetsMut' return none, since 'VS.generate' of a negative length is
-- empty and 'scanl'' still prepends the seed (both measured, not reasoned) --
-- which is what the @builds@ arm of @check@ reports and end-to-end agreement
-- does not. What the guard does NOT protect against is a division: 'magicOf'
-- is total at 0, so a zero hoisted radix is harmless by itself. The two
-- guards are independent and both live, and 'degenerateShapes' is the
-- regression test for each. Unreachable in this harness, which has no zero
-- dimension -- but orthotope has zero-size arrays, and this builder is
-- proposed for it.
{-# INLINE baseOffsetsScan #-}
baseOffsetsScan :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsScan o0 osh oats
  | m == 0 = VS.empty
  | otherwise =
      -- Asserted in the builder, not at the call sites: the multiply-high is
      -- internal to this function, so a caller with no Lemire of its own still
      -- inherits the bound -- which 'fbOffTabScan' does, and would otherwise
      -- have carried the precondition with nothing stating it.
      assert (lemireFits m)
      $ scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    scanned []   = VS.singleton o0
    scanned dims = VS.scanl' (+) o0 (VS.generate (m - 1) delta)
      where !lastDim    = last dims
            !nLast      = fst lastDim
            !stLast     = snd lastDim
            !mgLast     = magicOf nLast
            !rewindLast = stLast * (nLast - 1)
            !rdims      = drop 1 (reverse dims)
            delta !q =
              let !p = q + 1
                  !c = fromIntegral (mulhi mgLast (fromIntegral p))
              in  if p /= c * nLast then stLast
                  else carry c rdims rewindLast
            carry !c ((n, st) : ds) !acc = case c `quotRem` n of
              (!c', !r') -> if r' /= 0 then st - acc
                            else carry c' ds (acc + st * (n - 1))
            carry !_ _ !acc = negate acc  -- unreachable: q + 1 < m

-- 'baseOffsetsScan' with the hot-path divisibility test done by 'quotRem'
-- instead of the multiply-high -- one change, so that builder is its
-- control. What it prices is simplification, not speed: the rem form
-- carries no magic number and no 'mulhi', so this builder sheds the
-- @lemireFits@ bound entirely (a consumer with a mul-back output still
-- carries its own), and 'qr-prim' already measured the division's guards
-- as free on a loop-invariant divisor. The quotient the carry cascade
-- needs comes out of the same 'quotRem', so nothing is computed twice.
{-# INLINE baseOffsetsScanRem #-}
baseOffsetsScanRem :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsScanRem o0 osh oats
  | m == 0 = VS.empty
  | otherwise = scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    scanned []   = VS.singleton o0
    scanned dims = VS.scanl' (+) o0 (VS.generate (m - 1) delta)
      where !lastDim    = last dims
            !nLast      = fst lastDim
            !stLast     = snd lastDim
            !rewindLast = stLast * (nLast - 1)
            !rdims      = drop 1 (reverse dims)
            delta !q = case (q + 1) `quotRem` nLast of
              (!c, !r) -> if r /= 0 then stLast
                          else carry c rdims rewindLast
            carry !c ((n, st) : ds) !acc = case c `quotRem` n of
              (!c', !r') -> if r' /= 0 then st - acc
                            else carry c' ds (acc + st * (n - 1))
            carry !_ _ !acc = negate acc  -- unreachable: q + 1 < m

-- Strict state for 'baseOffsetsOdo': the offset to emit next, the countdown
-- within the innermost non-unit outer dimension, and the count of completed
-- stretches of it (the carry cascade's dividend).
data SOdo = SOdo !Int !Int !Int

-- The scan's table built with no per-entry division or multiplication at
-- all: an 'unfoldrExactN' odometer whose common step is emit, add, count
-- down -- 'baseOffsetsMutRuns'-shaped arithmetic from a pure-typed builder,
-- and hence no size bound of its own. The state is a strict three-Int
-- constructor, which is exactly what plain -O1 boxed per step (the old
-- refutations of 'fused' and 'bq-unfold') and what the standing SpecConstr
-- regime is expected to keep in registers: this builder is the bet that
-- the un-refutation carries from consuming streams to producing them.
-- Carries recompute the higher digits from the stretch counter by
-- 'quotRem', a 1/nLast fraction of entries, exactly as in
-- 'baseOffsetsScan', whose unit-dim elision this shares. Unlike the scan's,
-- the carry catch-all here is reachable -- once, computing the final
-- step's successor state, which 'VS.unfoldrExactN' discards -- so it must
-- not crash and does not.
{-# INLINE baseOffsetsOdo #-}
baseOffsetsOdo :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsOdo o0 osh oats
  | m == 0 = VS.empty
  | otherwise = built [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    built []   = VS.singleton o0
    built dims = VS.unfoldrExactN m step (SOdo o0 nLast 0)
      where !lastDim    = last dims
            !nLast      = fst lastDim
            !stLast     = snd lastDim
            !rewindLast = stLast * (nLast - 1)
            !rdims      = drop 1 (reverse dims)
            step (SOdo o cnt c)
              | cnt > 1   = (o, SOdo (o + stLast) (cnt - 1) c)
              | otherwise =
                  let !c' = c + 1
                  in  (o, SOdo (o + carry c' rdims rewindLast) nLast c')
            carry !c ((n, st) : ds) !acc = case c `quotRem` n of
              (!c', !r') -> if r' /= 0 then st - acc
                            else carry c' ds (acc + st * (n - 1))
            carry !_ _ !acc = negate acc  -- reachable once; see above

-- 'baseOffsetsScan' with the stream state packed into ONE Int: the run
-- index in the bits above 32, the running offset in the low 32, so
-- advancing both is a single add of @2^32 + delta@ (the offset stays in
-- its field because it is a real offset, bounded by the assert). This is
-- the constructive test of the bare-Int-state law, and it is only
-- meaningful WITHOUT SpecConstr: the law says a fused loop's state
-- unboxes at plain -O1 iff it is a bare Int -- measured in one direction
-- ('scanl''s Either-of-pair boxes 72 bytes per entry; index-only
-- 'VS.generate' does not) but never in the constructive one, and under
-- -fspec-constr every state shape unboxes, so this arm is
-- indistinguishable from its control there. Failed Run 6 bore the prediction out
-- exactly: 2.00x allocation, against the scan's 4.33x and the 1.33x a fully
-- unboxed emit would give. The diag verdict at -O1 is
-- already in: 16 bytes per entry against the scan's 72 -- the state
-- boxing is gone, confirming the law's constructive half for the state,
-- but one boxed Int per step survives in 'VS.unfoldrExactN''s emit pair,
-- which no state shape can reach. So the strategy is expected near 2.0x
-- allocation at -O1, between the scan's 4.33x and the 1.33x that a fully
-- unboxed emit would have given. Preconditions of the
-- packing, asserted: offsets below 2^32 (their field), m at most 2^31
-- (the index field), on top of the mulhi test's own bound -- and the
-- offset-bound arithmetic assumes non-negative strides, true of every
-- 'mkStrided' input.
{-# INLINE baseOffsetsScanPacked #-}
baseOffsetsScanPacked :: Int -> [Int] -> [Int] -> VS.Vector Int
baseOffsetsScanPacked o0 osh oats
  | m == 0 = VS.empty
      -- Strict bounds, unlike 'lemireFits': an offset of exactly 2^32 would
      -- mask to 0 in the low field, and m <= 2^31 keeps every EMITTED index
      -- out of the sign bit (the discarded final successor may set it;
      -- nothing reads it). lemireFits m for the mulhi test is implied.
  | otherwise =
      assert (m <= 2147483648 && maxOff < 4294967296)
      $ scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    maxOff = o0 + sum [(n - 1) * st | (n, st) <- zip osh oats]
    scanned []   = VS.singleton o0
    scanned dims = VS.unfoldrExactN m step o0
      where !lastDim    = last dims
            !nLast      = fst lastDim
            !stLast     = snd lastDim
            !mgLast     = magicOf nLast
            !rewindLast = stLast * (nLast - 1)
            !rdims      = drop 1 (reverse dims)
            step !st0 =
              let !acc = st0 .&. 4294967295
                  !p   = (st0 `shiftR` 32) + 1
                  !c   = fromIntegral (mulhi mgLast (fromIntegral p))
                  !d   = if p /= c * nLast then stLast
                         else carry c rdims rewindLast
                  -- Forced, not left to 'unfoldrExactN' to force on the next
                  -- step: this arm exists to ask whether a bare-Int state
                  -- unboxes at plain -O1, and handing the stream a thunk
                  -- instead of an evaluated Int would answer no for a reason
                  -- that has nothing to do with the state's shape.
                  !st1 = st0 + 4294967296 + d
              in  (acc, st1)
            carry !c ((n, st) : ds) !acc = case c `quotRem` n of
              (!c', !r') -> if r' /= 0 then st - acc
                            else carry c' ds (acc + st * (n - 1))
            carry !_ _ !acc = negate acc  -- reachable once, for the final
              -- step's discarded successor, as in 'baseOffsetsOdo'

-- The strategies compared, in the four families README.md's strategy list
-- uses and in its order (README.md#what-the-benchmark-does), base before
-- variant. That is the reading order. The RUN order is a different one,
-- stated at 'roster' below, and the Results table is sorted by time, a third.
--
-- Family 1: the originals, the first attempt, and the two odometer fills.

-- The original fallback.
{-# NOINLINE fbList #-}
fbList :: ShapeL -> T -> VS.Vector Double
fbList sh a = VS.fromListN l (toListT sh a) where l = product sh

-- The first attempt -- vGenerate + linear-index-to-offset by
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

-- 'fbGenQuotRem' with unsafeIndex, to isolate the bounds-check cost.
--
-- The third one-line variant of it -- those per-dimension divisions
-- replaced by 'fastQR' -- is deliberately not written; the numbers that
-- rule it out are in README.md#why-there-is-no-gen-lemire.
{-# NOINLINE fbGenUnsafe #-}
fbGenUnsafe :: ShapeL -> T -> VS.Vector Double
fbGenUnsafe sh (T ats ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (!q, !r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- unfoldrExactN with an additive odometer state (point 2) --
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

-- Strict, unpackable state for the fused odometer: current source
-- @offset@, position @j@ within the current run, and run index @q@.
data S3 = S3 !Int !Int !Int

-- The truly-fused, allocation-free additive odometer that
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
        -- @max 1 s@ as in 'fbBQunfold': a zero innermost extent would divide
        -- by zero here, and the bang forces it even though @l == 0@ makes the
        -- run count irrelevant. 'degenerateShapes' is what reaches this.
        !m = l `div` max 1 s
        !baseOffsets = VS.fromListN m (runBaseOffsets ao (init sh) (init ats))
                         :: VS.Vector Int
        step (S3 o j q) =
          -- @next@ is forced: unbanged it is a thunk per step, which is
          -- precisely the "no per-step allocation" this strategy claims. The
          -- 'S3' boxes and 'unfoldrExactN''s emit pair remain, and at plain
          -- -O1 those are what the 20x allocation is; the thunk was on top.
          let !x = VS.unsafeIndex v o
              !next
                | j + 1 < s = S3 (o + t) (j + 1) q
                | otherwise = let !q1 = q + 1
                              in  if q1 < m
                                  then S3 (VS.unsafeIndex baseOffsets q1) 0 q1
                                  else S3 0 0 q1  -- last element; state unused
          in  (x, next)

-- Family 2: the run base-offsets family. One 'VS.generate' over the result
-- doing one quotRem per element, reading a precomputed @m@-element table of
-- run base-offsets. These vary the TABLE BUILD, the output held fixed.

-- Precompute the run base-offsets as 'fbFused' does, but fill with a single
-- 'VS.generate' doing one 'quotRem' (by the innermost size @s@) per
-- element instead of one per rank -- to price the division-count
-- reduction on its own, without that strategy's fully-fused loop.
{-# NOINLINE fbBaseOffsetsQuot #-}
fbBaseOffsetsQuot :: ShapeL -> T -> VS.Vector Double
fbBaseOffsetsQuot sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsList ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- 'fbBaseOffsetsQuot' with the run base-offsets built by a mutable
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

-- 'fbBQmut' with the run base-offsets built by 'baseOffsetsMutRuns' instead
-- of 'baseOffsetsMut' -- one change, so 'bq-mut' is its control and the pair
-- prices the leaf specialisation of the build alone. Expect the gain to
-- track the table's share of the work: largest at small @sInner@
-- ('stretch-inner1' at the extreme, where the table is as long as the
-- output) and nil at 'stretch-tall-Mx2' (two base offsets). Unit-dim
-- elision (see 'baseOffsetsScan') would help this odometer too and is
-- deliberately absent: a second change would confound the control.
{-# NOINLINE fbBQmutRuns #-}
fbBQmutRuns :: ShapeL -> T -> VS.Vector Double
fbBQmutRuns sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmut' but building the base-offsets with 'VS.unfoldrExactN'
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

-- 'fbBQmut' but with the run base-offsets built by the pure
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

-- The per-dimension site: 'fbBQgen' with the run base-offsets built by
-- 'baseOffsetsGenLemire' instead of 'baseOffsetsGen', so 'bq-gen' is its
-- control.
{-# NOINLINE fbBQgenLemire #-}
fbBQgenLemire :: ShapeL -> T -> VS.Vector Double
fbBQgenLemire sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        -- Lemire is in the build here, so the bound is asserted there.
        !baseOffsets = baseOffsetsGenLemire ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmut' but with the run base-offsets built by the pure
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

-- 'fbBQexpand' with the fused zip-fold 'baseOffsetsExpandZF'
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

-- 'fbBQexpand' with the micro-optimised 'baseOffsetsExpandB'.
{-# NOINLINE fbBQexpandB #-}
fbBQexpandB :: ShapeL -> T -> VS.Vector Double
fbBQexpandB sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpandB ao (init sh) (init ats)
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- Family 2 continued: the OUTPUT varied instead, each against a build already
-- above.

-- 'fbBQexpand' with the output 'quotRem' replaced by the primop it wraps.
-- GHC guards 'quotRemInt#' against a zero divisor and against the
-- @minBound quot (-1)@ overflow, both tests on a loop-invariant divisor and
-- neither reachable here: @s@ is positive whenever the fill runs at all,
-- since a zero dimension makes @l@ zero and 'VS.generate' then never calls
-- the callback. This is the control that splits what
-- 'fbBQexpandLemireOut' owes to deleting the division from what it owes to
-- deleting those two guards -- a distinction that decides whether the Lemire
-- machinery is worth shipping at all, since this variant needs no magic
-- number and no bound on @l@.
{-# NOINLINE fbBQexpandQRprim #-}
fbBQexpandQRprim :: ShapeL -> T -> VS.Vector Double
fbBQexpandQRprim sh (T ats ao v) =
  -- Stands in for the two tests 'quotRem' makes and 'quotRemInt#' does not.
  -- It holds because @s@ is a shape dimension, hence never negative, so the
  -- @minBound quot (-1)@ overflow needs a divisor this can never have; and a
  -- zero dimension makes @l@ zero, whereupon 'VS.generate' never runs the
  -- callback, so the divisor cannot be zero at any division actually
  -- performed. Unlike the size preconditions above, this one is checkable
  -- from the shape alone and would fire on a malformed one.
  assert (l == 0 || s > 0) $ VS.generate l get
  where l = product sh
        !s = last sh
        !(I# s#) = s
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (init ats)
        get (I# i) = case quotRemInt# i s# of
          (# q, j #) -> VS.unsafeIndex v
                          (VS.unsafeIndex baseOffsets (I# q) + I# j * t)

-- The per-element output site: 'fbBQexpand' with the shared @i quotRem s@
-- replaced, the table build held at the shipped 'baseOffsetsExpand', so
-- 'bq-expand' is its control. Every run base-offsets strategy ends in that
-- same line, so this prices the output method for all of them at once. Unlike
-- the site above, the divisor is a single loop invariant, so the magic is
-- computed once per fill and no per-dimension list is walked beside it; the
-- @d == 1@ test inside 'fastQR' does stay in the loop, on a value that never
-- changes ('stretch-inner1' is the shape that takes it).
{-# NOINLINE fbBQexpandLemireOut #-}
fbBQexpandLemireOut :: ShapeL -> T -> VS.Vector Double
fbBQexpandLemireOut sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !mg = assert (lemireFits l) $ magicOf s
        !baseOffsets = baseOffsetsExpand ao (init sh) (init ats)
        get i = case fastQR mg s i of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- 'fbBQexpandLemireOut' in the leaner form orthotope would actually ship:
-- take only the quotient from the multiply-high and recover the remainder as
-- @i - q * s@, one multiply and a subtract in place of the second
-- 'timesWord2#'. The @s == 1@ case has to leave the loop for this to work at
-- all -- mul-back cannot use the 0-magic sentinel, since @mulhi 0 i@ is 0 and
-- would give @(0, i)@ where @(i, 0)@ is wanted -- so the two changes are one
-- change, not two confounded ones. Dropping the sentinel also drops the
-- per-element test on it, and 'magicOf' and 'fastQR' stop being needed:
-- what a caller has to carry is 'mulhi' and this loop.
--
-- @magic@ is 0 at @s == 1@ by its own guard rather than by @maxBound `quot` 1
-- + 1@ wrapping. The bang forces it at body entry even in the branch that
-- never reads it, so the guard costs one comparison per call and buys a
-- defined value in place of reliance on Word overflow staying benign -- and
-- saves the division there too. The three siblings that share this shape
-- ('fbBQexpand32LemireMulback', 'fbBQmutLemireMulback', 'fbBQscanMulback')
-- carry the same guard.
{-# NOINLINE fbBQexpandLemireMulback #-}
fbBQexpandLemireMulback :: ShapeL -> T -> VS.Vector Double
fbBQexpandLemireMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsExpand ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQexpandLemireMulback' with the base-offsets table narrowed to Int32
-- ('baseOffsetsExpand32'); the reconversion on read is a sign-extending
-- register move, free on x86-64. The pure candidate at reduced allocation:
-- the table and every expansion intermediate halve, as does the table's
-- read traffic under the fill. Carries both preconditions: 'int32Fits' on
-- the source for the narrowed table and 'lemireFits' on @l@ for the mul-back
-- output. They are separate tests on separate quantities, so a shipped
-- version needs both branches, not one covering the other.
{-# NOINLINE fbBQexpand32LemireMulback #-}
fbBQexpand32LemireMulback :: ShapeL -> T -> VS.Vector Double
fbBQexpand32LemireMulback sh (T ats ao v)
  | s == 1 = VS.generate l
               (VS.unsafeIndex v . fromIntegral . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        baseOffsets :: VS.Vector Int32
        -- NB 'int32Fits' is NOT the whole precondition here, unlike for
        -- 'baseOffsetsMut32': this builder does its arithmetic in Int32, so
        -- the partial base-offsets must fit too, and a source-length bound
        -- implies that only while every stride is non-negative. See the TODO
        -- on 'baseOffsetsExpand32'.
        !baseOffsets = assert (int32Fits v)
                       $ baseOffsetsExpand32 ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (fromIntegral (VS.unsafeIndex baseOffsets q)
                       + (i - q * s) * t)

-- The same output substitution against a second, unrelated table build:
-- 'fbBQmut', whose base-offsets come from a mutable odometer rather than
-- 'concatMap'. Every run base-offsets strategy shares the output line, so the
-- claim is that pricing it once prices it for all of them -- but that is an
-- inference from the shared source line, and this is the measurement of it.
-- It is also the interesting combination in its own right: 'bq-mut' ties
-- 'bq-expand' on time at a third of its allocation, so if the win carries,
-- this is the cheapest form of the fastest output.
{-# NOINLINE fbBQmutLemireOut #-}
fbBQmutLemireOut :: ShapeL -> T -> VS.Vector Double
fbBQmutLemireOut sh (T ats ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !mg = assert (lemireFits l) $ magicOf s
        !baseOffsets = baseOffsetsMut ao (init sh) (init ats)
        get i = case fastQR mg s i of
          (!q, !j) -> VS.unsafeIndex v (VS.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmutLemireOut' with the output changed to the single-multiply mul-back
-- form, sharing 'fbBQexpandLemireMulback''s hoisted @s == 1@ branch. One line
-- differs from 'bq-mut-lemire-out' and one build differs from
-- 'bq-expand-lemire-mulback', so it has a control on each axis and reads as
-- a one-change variant of either. What it prices that nothing else does is
-- the output form on a mutable build; 'fbBQexpand32LemireMulback' and
-- 'fbOffTab32' price the Int32 narrowing separately.
{-# NOINLINE fbBQmutLemireMulback #-}
fbBQmutLemireMulback :: ShapeL -> T -> VS.Vector Double
fbBQmutLemireMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMut ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- The fastest build and the fastest output measured so far, put together:
-- 'baseOffsetsMutRuns' for the table, the single-multiply mul-back for the
-- fill. One line differs from 'bq-mut-runs' and one build differs from
-- 'bq-mut-lemire-mulback', so it is a one-change variant of either and both
-- controls are in the table.
--
-- Worth stating what it does not settle, since combining two winners invites
-- the assumption that it must win. Each half is priced against a control, but
-- their sum is not: the output substitution is already measured to carry
-- differently across builds -- strongly on the expansion build, weakly on the
-- mutable one -- so this arm's margin over 'bq-mut-runs' is its own
-- measurement, not the transfer of anyone else's.
{-# NOINLINE fbBQmutRunsMulback #-}
fbBQmutRunsMulback :: ShapeL -> T -> VS.Vector Double
fbBQmutRunsMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQmutRunsMulback' with the quotient by the Granlund-Montgomery magic
-- ('gmMagic') instead of the Lemire multiply-high -- one change, so that
-- strategy is its control, and the pair prices dropping the l < 2^32
-- restriction: same table, same mul-back remainder, one extra shift per
-- element, and no 'lemireFits' anywhere in the arm. Predicted within noise
-- of the control and is NOT: Failed Run 6 has it ~10% behind, against a measured
-- A/A floor of ~2%. Dropping the size bound costs real time on this build,
-- so the bound is worth keeping where it holds.
{-# NOINLINE fbBQmutRunsGmMulback #-}
fbBQmutRunsGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQmutRunsGmMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (init ats)
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQexpandLemireMulback' with the table built by 'baseOffsetsScan'
-- instead of 'baseOffsetsExpand' -- one change, so that strategy is its
-- control. The pure sweet spot it was built to be, conditional on
-- SpecConstr, which is the standing assumption: under -fspec-constr the
-- build is allocation-free (diag, table + ~500 bytes) and the strategy
-- measures 1.33x allocation at the fastest pure time in the table, ahead
-- of the class-extension tier. At plain -O1 the builder's stream state
-- boxes per entry and this inherits bq-expand-class allocation instead
-- (the record of that regime is the comment at 'baseOffsetsScan').
-- Tunings to 'baseOffsetsScan' move this strategy and 'fbOffTabScan'
-- together -- deliberate coupling, the price of reusing the builder
-- verbatim; the difference against the control stays the build alone.
{-# NOINLINE fbBQscanMulback #-}
fbBQscanMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScan ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsScanRem' -- one
-- change, so that strategy is its control, and the pair prices the
-- builder's divisibility test alone: multiply-high against plain
-- 'quotRem', predicted ~neutral. If it measures neutral, the rem form is
-- what a shipped scan should use -- one less magic number in
-- Data/Array/Internal.hs, and the builder's own size bound gone.
{-# NOINLINE fbBQscanRemMulback #-}
fbBQscanRemMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanRemMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScanRem ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the quotient by the Granlund-Montgomery magic
-- ('gmMagic') instead of the Lemire multiply-high -- one change, so that
-- strategy is its control; the twin of 'fbBQmutRunsGmMulback' on the pure
-- side. The build is 'baseOffsetsScan' unchanged, so this arm's own
-- 'lemireFits' exposure is only the builder's internal one; the fully
-- restriction-free pure composition (scan-rem build + GM output) is one
-- further swap, deliberately not taken until each half is priced alone.
{-# NOINLINE fbBQscanGmMulback #-}
fbBQscanGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanGmMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsScan ao (init sh) (init ats)
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- The swap the two arms above each leave open, taken: 'baseOffsetsScanRem'
-- for the table and the Granlund-Montgomery quotient for the output. One
-- change from 'bq-scan-rem-mulback' (its output) and one from
-- 'bq-scan-gm-mulback' (its build), so it has a control on each axis and each
-- half is priced alone in this same run.
--
-- What makes it worth a row of its own rather than an inference from those
-- two: it is the only composition here with NO size precondition anywhere.
-- The scan-rem build tests divisibility with plain 'quotRem', so it carries
-- no magic and no bound; GM's quotient is exact for every non-negative Int,
-- so it carries none either. Grep this arm for 'lemireFits' and there is
-- nothing to find. Failed Run 6: it ties 'bq-scan-mulback' exactly (0.160 each) and
-- trails 'bq-scan-rem-mulback' by ~5%. So a shipped form CAN drop the size
-- dispatch entirely, at a price of about 5% against the best scan variant --
-- which is the trade to weigh on a machine whose arrays pass 2^32, where the
-- dispatch stops being a formality.
{-# NOINLINE fbBQscanRemGmMulback #-}
fbBQscanRemGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanRemGmMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsScanRem ao (init sh) (init ats)
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsOdo' -- one
-- change, so that strategy is its control, and the pair prices the last
-- lever the pure tier has: replacing the scan's per-entry divisibility
-- test with adds-only odometer state. If the standing regime keeps the
-- three-Int state in registers, the pure build matches
-- 'baseOffsetsMutRuns' arithmetic and most of the purity gap to
-- 'bq-mut-runs-mulback' should close; if the 'fused' row says SpecConstr
-- does not deliver that for produced streams, this arm is where the idea
-- dies with a number attached.
{-# NOINLINE fbBQodoMulback #-}
fbBQodoMulback :: ShapeL -> T -> VS.Vector Double
fbBQodoMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsOdo ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsScanPacked' -- one
-- change, so that strategy is its control. The pair is only informative
-- at plain -O1 (see the builder's comment); under -fspec-constr the two
-- should be indistinguishable, and measuring that indistinguishability is
-- itself the control.
{-# NOINLINE fbBQscanPackedMulback #-}
fbBQscanPackedMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanPackedMulback sh (T ats ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VS.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScanPacked ao (init sh) (init ats)
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VS.unsafeIndex baseOffsets q + (i - q * s) * t)

-- Family 3: whole-offset and alternative-gather variants -- offsets for every
-- element rather than for every run, or a gather with no output division.

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

-- Build the whole offset vector with the all-'Vector'
-- 'strideOffsets', then gather through 'unsafeBackpermute' (vector's
-- tight, fused indexing loop). Two passes over @l@ and an extra
-- 'Int'-vector, but every step is a plain memory read.
{-# NOINLINE fbBackperm #-}
fbBackperm :: ShapeL -> T -> VS.Vector Double
fbBackperm sh (T ats ao v) = VS.unsafeBackpermute v (strideOffsets ao sh ats)

-- Drop the per-element output quotRem as well. The output is a
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

-- The whole offset grid over ALL dims via 'baseOffsetsExpand', then
-- one gather. Materialises the full l-length offset table (foldl' forces
-- each level), so it prices what 'fbCMGather''s fused inner run avoids.
{-# NOINLINE fbAllExpand #-}
fbAllExpand :: ShapeL -> T -> VS.Vector Double
fbAllExpand sh (T ats ao v) =
  VS.map (VS.unsafeIndex v) (baseOffsetsExpand ao sh ats)

-- The full offset table (length @l@) built by the same mutable
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

-- 'fbOffTab' with the l-length offset table narrowed to Int32. The table
-- is that strategy's whole extra cost -- one sequential write plus one
-- sequential read of the full 8*l bytes on top of what 'fbMutOdo' does --
-- and this halves both, and the 2.0x allocation with them. 'fbOffTab' is
-- the fastest strategy needing no class extension, so this asks whether
-- narrowing moves it toward 'fbMutOdo', whose lead over it is exactly that
-- extra pass. Odometer arithmetic stays in Int; only the store narrows, so
-- 'int32Fits' is the whole of its precondition -- it uses no multiply-high,
-- and so needs nothing from 'lemireFits'.
{-# NOINLINE fbOffTab32 #-}
fbOffTab32 :: ShapeL -> T -> VS.Vector Double
fbOffTab32 sh (T ats ao v) =
  VS.generate l
    (\i -> VS.unsafeIndex v (fromIntegral (VS.unsafeIndex offs i)))
  where l = product sh
        !s = last sh
        !t = last ats
        offs :: VS.Vector Int32
        !offs = assert (int32Fits v) $ VS.create $ do
          o <- VSM.unsafeNew l
          let writeRun !outPos !baseOff =
                let inner !j !src
                      | j >= s    = return ()
                      | otherwise = VSM.unsafeWrite o (outPos + j)
                                      (fromIntegral src)
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

-- 'fbOffTab' with the offset table built by 'baseOffsetsScan' over ALL the
-- dims instead of by the mutable odometer: the full offset grid is the run
-- base-offsets grid of a shape whose "outer" dims are all of them, so the
-- builder is reused verbatim and no 'VS.create' remains -- the first pure
-- strategy with offtab's shape, an arithmetic-free gather off a
-- sequentially-read table. What it prices: whether offtab's pass-split
-- advantage (it beats 'bq-mut' despite strictly more traffic, because no
-- arithmetic delays the gather's loads) survives paying the delta
-- arithmetic l times rather than m and an l-length table. Unlike the
-- mulback strategies it needs no @s == 1@ branch: there is no output
-- division to guard.
--
-- The bet did not survive measurement: at ~0.35x list against 'fbOffTab''s
-- ~0.17x (a rough pass, its write-up no longer kept), the builder's
-- per-entry state boxing (see 'baseOffsetsScan') runs l times here and
-- costs more than the arithmetic-free gather saves, and the allocation
-- lands at 11x the result against the 2.0x the fused form promised. Two
-- tunings once listed as pending -- hoisting the second cascade level, an
-- Int32 table twin -- were premised on the fused form and are moot until
-- the state boxing itself is fixed, which at -O1 no pure-typed builder
-- escapes ( -O2 does fix it, at the builder level: see 'baseOffsetsScan').
--
-- The builder's unit-dim elision is what makes 'stretch-inner1' optimal
-- here rather than pathological: its [500000, 1] filters to one real
-- radix, so carries never fire, the delta is constantly 1 and the scan
-- degenerates to a sequential fill.
{-# NOINLINE fbOffTabScan #-}
fbOffTabScan :: ShapeL -> T -> VS.Vector Double
fbOffTabScan sh (T ats ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (VS.unsafeIndex offs i))
  where l = product sh
        !offs = baseOffsetsScan ao sh ats

-- Family 4: direct mutable result-buffer fills, which need a class extension
-- or explicit mutation, and the class-methods-only 'fbConcatRuns' that closes
-- the family needing neither.

-- The mutable run-fill -- the tightest pure-'Vector' shape,
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

-- 'fbMutOdo' with the odometer's dimension lists replaced by unboxed
-- vectors walked with a bare-Int level index -- one change, so 'mut-odo'
-- is its control. It was written as a diagnostic and answered decisively:
-- the direct fill's per-run cost WAS the cons-list traffic of the odometer
-- recursion, not the nested structure. Failed Run 6 puts it at half its control's
-- time and fastest of everything measured, which reopens the class-method
-- tier the README had closed at ~1.4x. 'writeRun' is kept character-identical to 'fbMutOdo''s so the build
-- of each run cannot differ.
{-# NOINLINE fbMutOdoVecdims #-}
fbMutOdoVecdims :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdims sh (T ats ao v) = VS.create $ do
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
            let !n  = VS.unsafeIndex oshV lev
                !st = VS.unsafeIndex oatsV lev
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
        oshV, oatsV :: VS.Vector Int
        !oshV  = VS.fromList (init sh)
        !oatsV = VS.fromList (init ats)

-- 'fbMutOdo' but iterating the precomputed run base-offsets list, to
-- price what that list (a factor @sInner@ smaller than @l@) costs the
-- odometer-free variant against its control.
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

-- 'fbMutOdo' expressed through the general 'vBuildVS' method,
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

-- 'fbBQmutRunsMulback' with the output written by an explicit flat ST loop
-- instead of 'VS.generate' -- same table, same per-element arithmetic, so
-- the pair prices the output MECHANISM alone. It is also the missing
-- corner of a factorial whose other diagonal is 'fbMutOdo': generate/flat
-- ('fbBQmutRunsMulback'), ST/nested ('fbMutOdo'), ST/flat (this); a
-- generate/nested corner cannot exist, 'VS.generate' being inherently
-- flat. The factorial is what tests the hypothesis that the direct fill
-- loses to the table strategies because it answers "which run am I in"
-- with per-run control flow where they answer it with per-element
-- arithmetic in one counted loop: if this arm matches 'fbBQmutRunsMulback'
-- the loop structure is the story and generate is not special; if it
-- lands near 'fbMutOdo', the structure hypothesis dies.
{-# NOINLINE fbMutFlat #-}
fbMutFlat :: ShapeL -> T -> VS.Vector Double
fbMutFlat sh (T ats ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let goCopy !i
        | i >= l = return ()
        | otherwise = do
            VSM.unsafeWrite out i
              (VS.unsafeIndex v (VS.unsafeIndex baseOffsets i))
            goCopy (i + 1)
      go !i
        | i >= l = return ()
        | otherwise = do
            let !q = fromIntegral (mulhi magic (fromIntegral i))
            VSM.unsafeWrite out i
              (VS.unsafeIndex v
                 (VS.unsafeIndex baseOffsets q + (i - q * s) * t))
            go (i + 1)
  if s == 1 then goCopy 0 else go 0
  return out
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (init ats)

-- The class-methods-only shape -- the only one expressible
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

-- The conv-derived shapes (grouped inline below; see
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
    -- ImageNet scale (only the layers whose per-call cost still buys, at
    -- criterion's default budget, the samples a tight fit needs)
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

-- Non-conv shapes stretching the space beyond convolution
-- (README.md#the-shape-set); each is annotated inline with what it probes.
-- The later entries push past the ranges the earlier ones cover, in the
-- terms the strategies are sensitive to: the view's innermost extent
-- @sInner@, which sets how many base offsets a table costs (@l \/ sInner@
-- of them); its innermost stride @tInner@; the rank; and @l@.
stretchShapes :: [(String, ShapeL)]
stretchShapes =
  [ ("stretch-rank10",      [3,3,3,3,3,3,3,3,3,3])    -- 59049, quotRem x10/elem
  , ("stretch-wide-2xM",    [2, 900000])              -- 1800000, extreme aspect
  , ("stretch-primes",      [97, 89, 29])             -- 250357, non-2^k arithmetic
  , ("stretch-bigstride",   [3, 3, 200000])           -- 1800000, huge innermost stride
  , ("stretch-square-1341", [1341, 1341])             -- 1798281, rank-2 near-square
  , ("stretch-r5-8x432",    [8, 8, 8, 8, 432])        -- 1769472, big rank-5
  , ("stretch-inner1",      [1, 500000])              -- 500000, sInner 1
  , ("stretch-tall-Mx2",    [900000, 2])              -- 1800000, 2 base offsets
  , ("stretch-coprime-r7",  [2, 3, 5, 7, 11, 13, 2])  -- 60060, rank 7, coprime
  , ("stretch-rank12",      [2,2,2,2,2,2,2,2,2,2,2,2])  -- 4096, deepest rank
    -- Sized to the 1800000 cap, which is what keeps it out of 'tooBig'. It
    -- keeps what it is for -- a base-offsets table as large as that cap
    -- allows (@m == l \/ 2@, tied with 'stretch-wide-2xM'), over a rank-3
    -- outer odometer, which is what separates it from that shape's rank-2
    -- grid of the same size.
  , ("stretch-tab7MB",      [900, 2, 1000])           -- 1800000, 900k-entry table
  ]

shapes :: [(String, ShapeL)]
shapes = convShapes ++ stretchShapes

-- Degenerate regime-3 shapes, checked but deliberately NOT benchmarked, and
-- so kept out of 'shapes'. Both have @l == 0@: timing one would divide
-- call overhead by call overhead, and that meaningless ratio would then carry
-- a full shape's weight in the geomean, which is over the shape set. What
-- they are for is the two corners no ordinary shape reaches, one each. Both
-- are regression tests for a GUARD rather than for the code it sits in: each
-- passes as things stand and fails the moment its guard is taken out.
--
--   * @[100000, 0]@ transposes to @[0, 100000]@, whose outer product is 0, so
--     the run count @m@ is 0. Remove 'baseOffsetsScan''s @m == 0@ guard and
--     the scan returns a one-element table where its siblings return none --
--     which the @builds@ arm of @check@ reports while @agree@ stays True,
--     since no strategy reads the entry.
--   * @[0, 100000]@ transposes to @[100000, 0]@, so the INNERMOST extent is 0.
--     Narrow 'magicOf' back to @d == 1@ and this shape dies with a divide by
--     zero: every magic-precomputing strategy binds its magic strictly, so
--     @l == 0@ spares none of them. 'fbFused''s @max 1 s@ run count is the
--     same story with a different guard.
--
-- Rank 1 and below cannot serve: @[]@, @[100000]@ and @[0]@ are all regime 1,
-- there being no second dimension to transpose against.
degenerateShapes :: [(String, ShapeL)]
degenerateShapes =
  [ ("degenerate-m0",      [100000, 0])  -- -> [0, 100000], l=0, m=0
  , ("degenerate-sinner0", [0, 100000])  -- -> [100000, 0], l=0, sInner=0
  ]

-- The cap that partitions the shape set: benchmarked iff @l <= sizeCap@,
-- flagged and excluded otherwise. 'stretchShapes' is written to it exactly.
sizeCap :: Int
sizeCap = 1800000

-- Conv layers excluded from 'shapes', printed at startup as a flag rather
-- than run. The rule is @l > sizeCap@, which 'partitioned' asserts, so the
-- two sets cannot overlap.
--
-- @l@ is the rule but not the run cost: criterion spends a time budget per
-- benchmark, so a shape's share of a run is set by how many strategies run
-- on it, not by how slow one call is. What @l@ drives is the per-call time,
-- and through that the sample count the budget buys -- which is the accuracy
-- the floor is really protecting. Which dimensions scale the work, and why
-- only the minibatch dim is free to drop:
-- README.md#dropping-the-minibatch-dimension.
tooBig :: [(String, ShapeL)]
tooBig =
  [ ("vgg-28-c256-k3",      [28, 28, 256, 3, 3])      -- 1806336  (~1.8M)
  , ("vgg-112-c64-k3",      [112, 112, 64, 3, 3])     -- 7225344  (~7M)
  , ("resnet-stem-112-c3-k7", [112, 112, 3, 7, 7])    -- 1843968  (~1.8M)
  , ("resnet-56-c128-k3",   [56, 56, 128, 3, 3])      -- 3612672  (~3.6M)
  , ("resnet-56-c256-k3",   [56, 56, 256, 3, 3])      -- 7225344  (~7.2M)
  , ("imagenet-224-c64-k3", [224, 224, 64, 3, 3])     -- 28901376 (~29M)
  ]

-- The rule of the two lists above as a check rather than a comment, and the
-- only thing standing between a mistyped dimension and a shape that quietly
-- takes a whole run's budget. Asserted in 'main', so it holds in every mode
-- and not only in the one that happens to read the list it guards.
-- Non-vacuity: lower 'sizeCap', or move one 'tooBig' entry into
-- 'convShapes', and every mode dies at startup -- run with the cap at
-- 1000000, where @check@, @diag@ and a benchmark run each exited 1 on
-- AssertionFailed rather than one of them passing.
partitioned :: Bool
partitioned = all ((<= sizeCap) . product . snd) shapes
           && all ((> sizeCap) . product . snd) tooBig

-- One roster entry: what 'mkBench' declares and what 'check' holds to the
-- reference. Both read the same list, so the two cannot come apart; they used
-- to be two hand-written lists of the same strategies, with @--lint@
-- comparing them. The constructor is where every deliberate asymmetry is
-- stated:
--
--   Base  'fbList': timed like the rest, and the vector every other arm is
--         held to, so it has nothing of its own left to check.
--   Fill  an ordinary strategy: timed as @VS.sum . f sh@, and checked.
--   Twin  an A/A control -- a 'Fill' arm run again under a second name, so
--         its own entry does the checking and this one only takes a slot.
--   Term  the @sum-only@ pair: the shared forcing term every other arm
--         carries, timed on a pre-built vector, with no fill of its own.
--   Only  checked but deliberately not timed; the reason is at the entry.
--
-- @read-run.py --lint@ reads the list below and holds it to what a reader of
-- either file assumes: every name documented in README.md, every @fb@
-- function defined here rostered, each 'Twin' naming the arm it duplicates,
-- and the controls named as that script's own control test recognises them.
data Arm = Base (ShapeL -> T -> VS.Vector Double)
         | Fill (ShapeL -> T -> VS.Vector Double)
         | Twin (ShapeL -> T -> VS.Vector Double)
         | Term
         | Only (ShapeL -> T -> VS.Vector Double)

-- Every arm, in RUN order -- which is neither the reading order of the
-- definitions above nor the Results table's, that one being sorted by time.
-- This order is placed for measurement: the A/A controls straddle what they
-- price, the Lemire arms straddle their controls, and the @sum-only@ pair
-- sits at both ends. Moving an entry takes a control off what it was aimed at
-- and breaks comparability with earlier runs, so it stays put; the families
-- are expressed in the definition order above instead.
roster :: [(String, Arm)]
roster =
  [ ("list",                       Base fbList)
    -- A/A controls, three of them, none a strategy: each runs an
    -- existing function twice so its true ratio is known to be exactly 1,
    -- and what it measures instead is what two identical things differ by.
    -- A margin narrower than they are is not a result.
    --
    -- They are aimed where comparisons are close, which Failed Run 6 showed is
    -- NOT the top of the table (0.074/0.092/0.099 are 20-35% apart) but
    -- two bands lower down. This one duplicates 'bq-scan-mulback' from
    -- ~28 slots away, so it prices the scan band -- which holds an exact
    -- tie, 'bq-scan-mulback' against 'bq-scan-rem-gm-mulback', and that
    -- tie is the shipping question -- and simultaneously spans the group,
    -- keeping position monitored rather than assumed now that SpecConstr
    -- changes code layout. Failed Run 6 found no position effect at -O1:
    -- the distant pair agreed to 0.14% against the adjacent one's 1.2% --
    -- published ratios, i.e. of the two trimmed columns, where the arms
    -- may drop different shapes; paired shape by shape the two read 0.34%
    -- and 0.36%, the same verdict by a cleaner route
    -- (README.md#the-noise-floor-is-2-not-the-ci).
  , ("bq-scan-mulback-aa-distant", Twin fbBQscanMulback)
    -- The early half of the 'sum-only' pair; the late half is the last
    -- bench in the group. Subtracting the shared forcing term from every
    -- other row is only sound if that term is a CONSTANT, and this bench
    -- is the one place in the suite where that is in doubt: every other
    -- bench allocates its own result each iteration and so is indifferent
    -- to what ran before it, while this one re-reads a FIXED vector and
    -- therefore depends on whether that vector survived in cache. The A/A
    -- pair's agreement does not license the assumption -- it duplicates a
    -- self-allocating bench, the insensitive kind. If the two halves
    -- agree the correction is sound; if they diverge, the term is not a
    -- constant and the correction must be dropped rather than applied.
  , ("sum-only-early",             Term)
  , ("gen-quotrem",                Fill fbGenQuotRem)
  , ("gen-unsafe",                 Fill fbGenUnsafe)
  , ("unfold-add",                 Fill fbUnfoldAdd)
  , ("fused",                      Fill fbFused)
  , ("offsets-quot",               Fill fbBaseOffsetsQuot)
  , ("backperm",                   Fill fbBackperm)
    -- 'fbConcatRuns' is deliberately NOT benchmarked, though @check@
    -- still holds it to the reference. It is by a clear margin the
    -- noisiest bench of the set -- Failed Run 6's single worst cell, the
    -- worst cell on five of its shapes, and a median cell some 2.5x the
    -- shape's typical CI -- and it sits in the heavy tail of both time
    -- and allocation, though 'list', 'unfold-add' and 'cm-gather' all
    -- allocate more. Every time figure is a ratio to 'list', which runs
    -- first in the group, so an aftermath outliving one bench would tilt
    -- the whole group one way instead of cancelling. The direct probes
    -- find nothing: its successor times the same after it as after a
    -- benign predecessor, and the A/A pair that straddles it agrees
    -- better than the two that do not. What is not probed is the roster
    -- effect (README.md#the-noise-floor-is-2-not-the-ci): 20% in
    -- horde-ad's ConvVjpBench, a property of what shares the process
    -- rather than of any one bench, and persisting for a whole run. The
    -- bench likeliest to trigger it is the one with the most extreme
    -- footprint, which is this one, and it is refuted on its own numbers
    -- anyway -- so timing it buys nothing to set against that risk. It
    -- keeps a roster entry, and with it an agreement check, but takes no
    -- slot in the run; the entry sits where the slot used to be.
  , ("concat-runs",                Only fbConcatRuns)
  , ("mut-odo",                    Fill fbMutOdo)
  , ("mut-odo-vecdims",            Fill fbMutOdoVecdims)
    -- The fast-end control, on the fastest strategy measured. Failed Run 6 put
    -- the floor at 2.0% duplicating a 0.099 arm against 0.14-1.2% on a
    -- 0.179 one -- and the noisier arm was the one allocating LESS, so
    -- the floor tracks 1/time rather than GC pressure. That predicts a
    -- larger floor still here, at 0.074, which nothing has measured.
  , ("mut-odo-vecdims-aa",         Twin fbMutOdoVecdims)
  , ("mut-offsets",                Fill fbMutBaseOffsets)
  , ("build",                      Fill fbBuild)
  , ("bq-mut",                     Fill fbBQmut)
  , ("bq-mut-runs",                Fill fbBQmutRuns)
  , ("bq-mut-runs-mulback",        Fill fbBQmutRunsMulback)
  , ("mut-flat",                   Fill fbMutFlat)
  , ("bq-mut-runs-gm-mulback",     Fill fbBQmutRunsGmMulback)
  , ("bq-mut-lemire-out",          Fill fbBQmutLemireOut)
  , ("bq-mut-lemire-mulback",      Fill fbBQmutLemireMulback)
  , ("offtab",                     Fill fbOffTab)
  , ("offtab32",                   Fill fbOffTab32)
  , ("offtab-scan",                Fill fbOffTabScan)
  , ("bq-unfold",                  Fill fbBQunfold)
  , ("bq-gen",                     Fill fbBQgen)
    -- The Lemire arms are placed to straddle their controls: this one
    -- runs just after 'bq-gen', and the output-substitution arms run
    -- ahead of 'bq-expand'. A group's later slots are the warmer ones,
    -- so any position bias flatters one side and penalises the other,
    -- and cannot manufacture a verdict that agrees across both.
  , ("bq-gen-lemire",              Fill fbBQgenLemire)
  , ("bq-expand-lemire-out",       Fill fbBQexpandLemireOut)
  , ("bq-expand-lemire-mulback",   Fill fbBQexpandLemireMulback)
  , ("bq-expand32-lemire-mulback", Fill fbBQexpand32LemireMulback)
  , ("bq-scan-mulback",            Fill fbBQscanMulback)
  , ("bq-scan-rem-mulback",        Fill fbBQscanRemMulback)
  , ("bq-scan-gm-mulback",         Fill fbBQscanGmMulback)
  , ("bq-scan-rem-gm-mulback",     Fill fbBQscanRemGmMulback)
  , ("bq-odo-mulback",             Fill fbBQodoMulback)
  , ("bq-scan-packed-mulback",     Fill fbBQscanPackedMulback)
  , ("bq-expand-qr-prim",          Fill fbBQexpandQRprim)
  , ("bq-expand",                  Fill fbBQexpand)
  , ("bq-expand-aa-adjacent",      Twin fbBQexpand)
  , ("bq-expand-zf",               Fill fbBQexpandZF)
  , ("bq-expand-b",                Fill fbBQexpandB)
  , ("cm-gather",                  Fill fbCMGather)
  , ("all-expand",                 Fill fbAllExpand)
    -- Not a strategy: the shared forcing term every other bench carries.
    -- Each of them is @whnf (VS.sum . fb sh) a@, so each timing is fill
    -- PLUS this sum, and every ratio reported anywhere is @(B+S)/(A+S)@ --
    -- compressed toward 1 by an amount nothing measured until now, and
    -- compressed most for the fastest arms, which is where the table is
    -- closest. With @S@ in hand every margin in the record becomes
    -- correctable after the fact, which is why it is worth a row in the
    -- last run at this optimisation level.
    --
    -- The late half of the pair; the early half sits third in the group
    -- and the two together test whether the term is position-independent
    -- (see there). Last in the group deliberately: its 'env' materialises
    -- a second l-element vector, and nothing after it can be perturbed by
    -- that -- nothing follows.
  , ("sum-only-late",              Term)
  ]

-- The reference every other arm is held to, and the bench named @list@: read
-- off the roster rather than named a second time here, so the arm that gets
-- timed and the vector 'check' compares against cannot come apart.
reference :: ShapeL -> T -> VS.Vector Double
reference sh a = case [f | (_, Base f) <- roster] of
  f : _ -> f sh a
  []    -> error "roster: no Base entry to serve as the reference"

-- The arms 'check' holds to that reference. The reference has nothing to
-- compare itself against, a 'Twin' duplicates an arm already checked, and a
-- 'Term' has no fill of its own -- so those three are absent by construction
-- rather than by omission, which is what a hand-written chain could not say.
--
-- Proved non-vacuous by shortening 'fbBQexpandB''s result by one element:
-- @check@ then failed at the first shape, naming @bq-expand-b@.
checkedArms :: [(String, ShapeL -> T -> VS.Vector Double)]
checkedArms = [(n, f) | (n, arm) <- roster, f <- fills arm]
  where fills (Fill f) = [f]
        fills (Only f) = [f]
        fills _        = []

-- Print the flagged (too-big) shapes, then benchmark every shape in
-- 'shapes'. How to run: README.md#running-it. The numbers and how to
-- read them: README.md#results, README.md#reading-the-results.
main :: IO ()
main = assert partitioned $ do
  args <- getArgs
  if "diag" `elem` args
    then diag
    else if "check" `elem` args
      then check
      -- The allocation fit is on by default rather than left to the command
      -- line, so the alloc figures come out of the same process as the times
      -- instead of a side run, and cannot be forgotten. Criterion's
      -- 'manyDefault' means an explicit @--regress@ still replaces this.
      else do
        let bs = map mkBench shapes
        defaultMainWith
          defaultConfig { regressions = [(["iters"], "allocated")] } bs
        provenance

-- What a run records about itself, so that a document quoting its scale
-- copies a measured number instead of counting benches by hand -- which is
-- how README came to claim one bench more than the run it describes
-- actually held. The heap pair is the one micro.cabal's -M2G comment
-- rests on, and all of it comes from the -T stats that flag already asks
-- for, so nothing here needs a flag from the invoker. It goes to stderr,
-- leaving @--list@ and criterion's own stdout machine-readable, and it
-- reports the roster rather than what a filtered run selected.
--
-- The count is the roster's timed arms, not the 'Benchmark' nodes 'mkBench'
-- built. Those are one per timed arm per SHAPE, so counting them reported
-- their product -- 1452 where 44 was meant, in a line whose whole purpose is
-- to be quoted. Reading the roster is not the weaker check it looks like:
-- 'mkBench' emits exactly one bench per timed arm, so the two cannot differ.
provenance :: IO ()
provenance = do
  s <- getRTSStats
  let secs = fromIntegral (elapsed_ns s) / 1e9 :: Double
      (h, r) = (round secs :: Int) `divMod` 3600
      (m, sec) = r `divMod` 60
      mib b = show (round (fromIntegral b / 1048576 :: Double) :: Int)
      timed = [n | (n, arm) <- roster, notOnly arm]
      notOnly (Only _) = False
      notOnly _        = True
  hPutStrLn stderr $
    "=== roster " ++ show (length timed) ++ " benchmarks over "
    ++ show (length shapes)
    ++ " shapes; elapsed " ++ show h ++ "h" ++ show m ++ "m" ++ show sec
    ++ "s; peak " ++ mib (max_mem_in_use_bytes s) ++ " MiB in use, "
    ++ mib (max_live_bytes s) ++ " MiB max residency"

-- Benchmark one shape: every 'roster' arm, in that list's order, which is
-- where each arm's slot and the reason for it are recorded. Criterion's 'env'
-- builds the input once and forces it to normal form before the clock starts,
-- so input construction is excluded from timing and the source vector is
-- fully materialised. The agreement/regime check is deliberately NOT here --
-- it lives in the separate 'check' mode, so the timed program never even
-- computes it and thus cannot share (CSE) a strategy's result between the
-- check and the benchmark.
--
-- Each fill reaches the timed loop as a closure out of 'roster' rather than
-- as a literal composition, which is what deriving both consumers from one
-- list costs, and it costs it in every arm alike.
mkBench :: (String, ShapeL) -> Benchmark
mkBench (name, normalSh) =
  env (evaluate (force (mkStrided normalSh))) $ \ ~(sh, a) ->
    bgroup name (concatMap (arm sh a) roster)
  where
    arm sh a (n, Base f) = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Fill f) = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Twin f) = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Term)   = [env (evaluate (force (reference sh a))) $ \r ->
                              bench n $ whnf VS.sum r]
    arm _  _ (_, Only _) = []

-- Correctness / non-vacuity, in its own mode (@cabal run micro -- check@) so
-- it runs as a separate process from the timed benchmark: every shape must
-- take regime 3 and every strategy must produce the same vector as the
-- reference. Which arms those are is 'checkedArms', read off the same
-- 'roster' the benchmark is built from, so a strategy cannot be timed
-- without being checked; a disagreeing arm is named rather than merely
-- counted, which a chain of @&&@ could not do.
check :: IO ()
check = do
  mapM_ (\(n, s) -> putStrLn $ "FLAGGED too big, excluded: " ++ n ++ " "
                               ++ show s ++ ", l=" ++ show (product s))
        tooBig
  mapM_ one (shapes ++ degenerateShapes)
  where
    one (name, normalSh) = do
      let (sh, a@(T ats ao _)) = mkStrided normalSh
          rList   = reference sh a
          -- The builders compared directly, not only through the strategies
          -- that consume them. End-to-end agreement hides a table that is
          -- wrong past the entries a fill happens to read, or right in its
          -- entries and wrong in its length -- which is exactly how
          -- 'baseOffsetsScan' came to return a one-element table at @m == 0@
          -- while every strategy built on it still produced the right vector.
          -- 'baseOffsetsList' is the reference because it is the one nothing
          -- else is derived from. Every builder 'diag' measures is here: a
          -- builder reached only through a consumer has its entries checked
          -- where that consumer reads them and its length checked nowhere,
          -- which is the gap this arm exists to close, so add to both lists
          -- together. Non-vacuity, per conjunct and not merely for the arm:
          -- lengthening 'baseOffsetsScanRem', 'baseOffsetsOdo' or
          -- 'baseOffsetsScanPacked' by one entry fails at the first shape
          -- with @agree=True, builds=False@ -- the very split this arm is
          -- here for.
          osh     = init sh
          oats    = init ats
          rBuild  = baseOffsetsList ao osh oats
          w32     = VS.map fromIntegral  -- Int32 table read back as the rest
          builds  = rBuild == baseOffsetsGen        ao osh oats
                 && rBuild == baseOffsetsGenLemire  ao osh oats
                 && rBuild == baseOffsetsExpand     ao osh oats
                 && rBuild == baseOffsetsExpandZF   ao osh oats
                 && rBuild == baseOffsetsExpandB    ao osh oats
                 && rBuild == baseOffsetsScan       ao osh oats
                 && rBuild == baseOffsetsScanRem    ao osh oats
                 && rBuild == baseOffsetsOdo        ao osh oats
                 && rBuild == baseOffsetsScanPacked ao osh oats
                 && rBuild == baseOffsetsMut        ao osh oats
                 && rBuild == baseOffsetsMutRuns    ao osh oats
                 && rBuild == w32 (baseOffsetsExpand32 ao osh oats)
                 && rBuild == w32 (baseOffsetsMut32    ao osh oats)
          bad     = [n | (n, f) <- checkedArms, f sh a /= rList]
          agree   = null bad
          reg     = regimeOf sh a
      putStrLn $ name ++ ": normalSh " ++ show normalSh ++ " -> strided "
                 ++ show sh ++ ", l=" ++ show (product sh)
                 ++ ", regime=" ++ show reg ++ ", agree=" ++ show agree
                 ++ ", builds=" ++ show builds
      if agree && builds && reg == 3
        then return ()
        else error ("CHECK FAILED: " ++ name
                    ++ (if null bad then ""
                        else ", disagreeing: " ++ unwords bad))

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
  putStrLn "(each builds the SAME m-element table; only method and element width differ)"
  mapM_ one [ ("cnn-L1-24x24 [24,24,1,3,3]",  [24, 24, 1, 3, 3])
            , ("vgg-14-c512  [14,14,512,3,3]", [14, 14, 512, 3, 3]) ]
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
      measure "  baseOffsetsGenLemire  Gen with 'fastQR'                  " (\k -> baseOffsetsGenLemire k osh oats)
      measure "  baseOffsetsExpand VS.concatMap iterated expansion        " (\k -> baseOffsetsExpand k osh oats)
      measure "  baseOffsetsExpandZF  Expand, zip and fold fused          " (\k -> baseOffsetsExpandZF k osh oats)
      measure "  baseOffsetsExpandB   Expand seeded from the first dim    " (\k -> baseOffsetsExpandB  k osh oats)
      measure "  baseOffsetsScan   scanl' over a generated delta stream   " (\k -> baseOffsetsScan   k osh oats)
      measure "  baseOffsetsScanRem  Scan with quotRem divisibility       " (\k -> baseOffsetsScanRem k osh oats)
      measure "  baseOffsetsOdo    unfoldrExactN 3-Int odometer state     " (\k -> baseOffsetsOdo    k osh oats)
      measure "  baseOffsetsScanPacked  Scan with one-Int packed state    " (\k -> baseOffsetsScanPacked k osh oats)
      measure "  baseOffsetsMut    VS.create mutable odometer             " (\k -> baseOffsetsMut    k osh oats)
      measure "  baseOffsetsMutRuns  Mut with leaf run-writes             " (\k -> baseOffsetsMutRuns k osh oats)
      measure32 "  baseOffsetsExpand32  Expand at Int32                   " (\k -> baseOffsetsExpand32 k osh oats)
      measure32 "  baseOffsetsMut32  Mut at Int32                         " (\k -> baseOffsetsMut32  k osh oats)
    -- Int32 twin of 'measure': the checksum folds to Int so it neither
    -- overflows nor allocates a converted copy.
    measure32 label build = do
      let n = 500 :: Int
      performGC
      s0 <- getRTSStats
      let loop !acc !k
            | k >= n    = acc
            | otherwise =
                loop (acc + VS.foldl' (\a x -> a + fromIntegral x) 0 (build k))
                     (k + 1)
      tot <- evaluate (loop (0 :: Int) 0)
      -- Both readings are GC'd, not just the first: 'allocated_bytes' only
      -- advances at a GC, so without this the tail since the last one goes
      -- uncounted -- and a build small enough that no GC fires at all over
      -- the whole loop reads as 0 bytes rather than as its true size.
      performGC
      s1 <- getRTSStats
      let bytes =
            (fromIntegral (allocated_bytes s1 - allocated_bytes s0) :: Int)
            `div` n
      putStrLn $ label ++ ": "
                 ++ show bytes ++ " bytes  (checksum "
                 ++ show tot ++ ")"
    measure label build = do
      let n = 500 :: Int
      performGC
      s0 <- getRTSStats
      let loop !acc !k | k >= n    = acc
                      | otherwise = loop (acc + VS.sum (build k)) (k + 1)
      tot <- evaluate (loop (0 :: Int) 0)
      -- Both readings are GC'd, not just the first: 'allocated_bytes' only
      -- advances at a GC, so without this the tail since the last one goes
      -- uncounted -- and a build small enough that no GC fires at all over
      -- the whole loop reads as 0 bytes rather than as its true size.
      performGC
      s1 <- getRTSStats
      let bytes =
            (fromIntegral (allocated_bytes s1 - allocated_bytes s0) :: Int)
            `div` n
      putStrLn $ label ++ ": "
                 ++ show bytes ++ " bytes  (checksum "
                 ++ show tot ++ ")"
