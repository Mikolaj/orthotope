{-# LANGUAGE BangPatterns  #-}
{-# LANGUAGE MagicHash     #-}
{-# LANGUAGE RankNTypes    #-}
{-# LANGUAGE UnboxedTuples #-}
-- | Self-contained benchmark isolating orthotope's toVectorListT regime 3
-- (the per-element fallback for an innermost-strided array), so the
-- candidate fallbacks can be A/B'd without an ox-arrays + horde-ad rebuild.
-- It compares the candidate strategies; 'mkStrided' builds a regime-3 input
-- (the stride-class generators beside it, 'mkRev' through 'mkScaled', build
-- the regime-3 inputs other library operations produce -- always checked,
-- timed only by the @classes@ mode as their own populations), 'regimeOf'
-- checks each really is one, and the @check@ main mode asserts all
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

import           Control.DeepSeq              (NFData (..), force)
import           Control.Exception            (assert, evaluate)
import           Control.Monad                (foldM_, unless, void)
import           Control.Monad.ST             (ST)
import           Criterion.Main
import           Criterion.Types              (Config (regressions))
import           Data.Bits                    (countLeadingZeros, shiftR, (.&.))
import           Data.Int                     (Int32)
import           Data.List                    (foldl')
import qualified Data.Vector.Storable         as VS
import qualified Data.Vector.Storable.Mutable as VSM
import qualified Data.Vector.Unboxed          as VU
import qualified Data.Vector.Unboxed.Mutable  as VUM
import           GHC.Exts                     (Int (..), Word (..), build,
                                               int2Word#, quotRemInt#,
                                               timesWord2#, word2Int#)
import           GHC.Stats                    (RTSStats (allocated_bytes, elapsed_ns, max_live_bytes, max_mem_in_use_bytes),
                                               getRTSStats)
import           System.Environment           (getArgs, withArgs)
import           System.IO                    (hPutStrLn, stderr)
import           System.Mem                   (performGC)

type ShapeL = [Int]

-- The strides of a view, one stride (a vector-index step) per dimension --
-- a list like a shape, which is what the wrapper is for: a builder takes a
-- shape and strides side by side, and bare [Int]s would let a call swap
-- them silently. Where a shape is CONVERTED into strides ('getStridesT'
-- and the natural-stride locals derived from it), the raw list stays.
newtype Strides = Strides [Int]

-- A faithful copy of orthotope's internal array representation and the
-- pieces of Data.Array.Internal that regime 3 uses, specialised to
-- Storable Double (horde-ad's element storage).
data T = T !Strides !Int !(VS.Vector Double)  -- strides, offset, values

-- So criterion's 'env' can force the input to normal form before timing.
instance NFData T where
  rnf (T (Strides s) o v) = rnf s `seq` rnf o `seq` rnf v

-- The result is the total size prefixed to the shape's natural strides --
-- one element longer than the rank, so not a 'Strides'; every caller
-- splits it.
getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

indexT :: T -> Int -> T
indexT (T (Strides (s : ss)) o v) i = T (Strides ss) (o + i * s) v
indexT _ _                          = error "indexT"

unScalarT :: T -> Double
unScalarT (T _ o v) = v VS.! o

-- Exactly orthotope's toListT (the otherwise branch; our inputs are
-- never canonical).
toListT :: ShapeL -> T -> [Double]
toListT sh (T (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarT (T (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexT (T (Strides ss) o v) i of
                 T (Strides ss') o' _ -> go ns ss' o')
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
-- which the main set cannot show, since 'mkStrided' gives every view a
-- source of its own length, so there the two differ only by a factor of
-- two. The sliced and scaled classes ('mkSliced', 'mkScaled') separate them
-- structurally -- the backing strictly exceeds what the view reads -- though
-- at magnitudes where both bounds still hold. In orthotope a strided view is
-- a window onto someone else's buffer, so a two-element view of a
-- three-billion-element array clears 'lemireFits' by nine orders of
-- magnitude and fails 'int32Fits'. A shipped dispatch therefore needs both
-- tests, not one standing in for the other.

-- Lemire's identity holds for @d, n < 2^32@. Here @n@ is the linear output
-- index, bounded by @l@, and @d@ is the innermost extent, which divides @l@ --
-- so bounding @l@ bounds both.
{-# INLINE lemireFits #-}
lemireFits :: Int -> Bool
lemireFits l = l < 4294967296  -- 2^32

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
-- TODO, owed before any shipped form: a standalone property test against
-- 'quotRem' over adversarial (n, d). Correctness here rests on @check@
-- agreeing on benchmarked shapes, which exercise neither the @d == 1@ path
-- nor anything near the @n < 2^32@ bound the identity needs -- so the
-- helper is tested only where it is easiest to be right.
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
-- past 2^32) are unreachable under 'sizeCap', which bounds this harness and
-- not the library.
--
-- TODO, owed before any shipped form and the same debt 'fastQR' carries: a
-- standalone property test against 'quotRem' over adversarial (n, d).
-- orthotope's own test suite is where it goes; QuickCheck over the whole
-- Int range costs nothing and covers what no benchmarked shape reaches.
--
-- This helper's lazy result tuple was a bug: forcing it moved the
-- Granlund-Montgomery arms rostered at the time, as the analogous
-- strictness fixes moved 'fbBQscanPackedMulback' and 'fbFused'. Those rows
-- are therefore not comparable to any run before Failed Run 6 -- a CODE
-- change, where the shape set and roster deltas README records are
-- population changes, and the two want telling apart when an old figure
-- looks wrong.
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
-- and consumed immediately by 'VU.fromListN'.
{-# INLINE runBaseOffsets #-}
runBaseOffsets :: Int -> ShapeL -> Strides -> [Int]
runBaseOffsets o0 osh (Strides oats) = build $ \cons nil ->
  let go []       []         !o rest = cons o rest
      go (n : ns) (st : sts) !o rest =
        foldr (\i r -> go ns sts (o + i * st) r) rest [0 .. n - 1]
      go _        _          !o rest = cons o rest
  in  go osh oats o0 nil

-- The run base-offsets table (length @product osh@) as 'fbBaseOffsetsQuot'
-- builds it:
-- the 'runBaseOffsets' list fed to 'VU.fromListN'. Extracted so the allocation
-- diagnostic (see 'diag') measures the exact benchmarked build.
{-# INLINE baseOffsetsList #-}
baseOffsetsList :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsList o0 osh (Strides oats) =
  VU.fromListN (product osh) (runBaseOffsets o0 osh (Strides oats))

-- The same table as 'fbBQmut' builds it: a mutable odometer fill of the
-- concrete Int scratch, no intermediate list.
{-# INLINE baseOffsetsMut #-}
baseOffsetsMut :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsMut o0 osh (Strides oats) = VU.create $ do
  b <- VUM.unsafeNew (product osh)
  let go [] [] !q !baseOff = VUM.unsafeWrite b q baseOff >> return (q + 1)
      go (n : ns) (st : sts) !q !baseOff =
        let dim !i !qq
             | i >= n    = return qq
             | otherwise = go ns sts qq (baseOff + i * st) >>= dim (i + 1)
        in  dim 0 q
      go _ _ !q !baseOff = VUM.unsafeWrite b q baseOff >> return (q + 1)
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
baseOffsetsMut32 :: Int -> ShapeL -> Strides -> VU.Vector Int32
baseOffsetsMut32 o0 osh (Strides oats) = VU.create $ do
  b <- VUM.unsafeNew (product osh)
  let go [] [] !q !baseOff = VUM.unsafeWrite b q (fromIntegral baseOff)
                             >> return (q + 1)
      go (n : ns) (st : sts) !q !baseOff =
        let dim !i !qq
             | i >= n    = return qq
             | otherwise = go ns sts qq (baseOff + i * st) >>= dim (i + 1)
        in  dim 0 q
      go _ _ !q !baseOff = VUM.unsafeWrite b q (fromIntegral baseOff)
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
baseOffsetsMutRuns :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsMutRuns o0 osh (Strides oats) = VU.create $ do
  b <- VUM.unsafeNew (product osh)
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

-- The same table via a pure 'VU.generate' (no explicit mutation -- the fill
-- is vector's own, hidden like 'VU.fromListN'/'VU.generate' already are in
-- orthotope): each run's base-offset is computed independently by decomposing
-- the run index over the outer natural strides and re-dotting with the actual
-- outer strides. No list, so no transient garbage -- but @rank-1@ quotRems
-- per run instead of the odometer's shared adds.
{-# INLINE baseOffsetsGen #-}
baseOffsetsGen :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsGen o0 osh (Strides oats) = VU.generate (product osh) baseOffset
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
baseOffsetsGenLemire :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsGenLemire o0 osh (Strides oats) =
    -- In the builder for the same reason as in 'baseOffsetsScan': run
    -- indices and outer natural strides are both bounded by the run count.
    assert (lemireFits (product osh))
  $ VU.generate (product osh) baseOffset
  where nts = drop 1 (scanr (*) 1 osh)
        ms  = map magicOf nts
        baseOffset q = o0 + go q ms nts oats
        go _  []        _           _          = 0
        go qq (m : ms') (nt : nts') (st : sts') = case fastQR m nt qq of
                                          (!a, !b) -> a * st + go b ms' nts' sts'
        go _  _         _           _          = 0

-- The same table by iterated expansion with 'VU.concatMap' (pure vector,
-- no 'VU.generate', no explicit mutation, no division): the base-offsets grid
-- is separable (@o0 + sum idx_d * stride_d@), so starting from @[o0]@ each
-- outer dimension expands every partial base-offset @a@ into @enumFromStepN a
-- stride_d n_d@ -- the odometer's shared adds, but expressed in vector's
-- stream framework rather than a hand-written loop.
{-# INLINE baseOffsetsExpand #-}
baseOffsetsExpand :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsExpand o0 osh (Strides oats) = foldl' expand (VU.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- 'baseOffsetsExpand''s table in a STORABLE vector, which is what every table
-- here used to be. It survives for the three arms that hand a table to a
-- payload-flavour 'Vector' combinator -- 'fbBackperm''s 'unsafeBackpermute'
-- and 'fbCMGather''s and 'fbAllExpand''s 'map' all take one vector family, so
-- for those the table's flavour IS the payload's and unboxing it would change
-- the strategy rather than its scratch. Every other table here is unboxed,
-- the flavour 'Data/Array/Internal.hs' ships; the probe that settled it, and
-- what it cost, are at README.md#the-scratch-vector-flavour.
{-# INLINE baseOffsetsExpandVS #-}
baseOffsetsExpandVS :: Int -> ShapeL -> Strides -> VS.Vector Int
baseOffsetsExpandVS o0 osh (Strides oats) =
  foldl' expand (VS.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VS.concatMap (\a -> VS.enumFromStepN a sd nd) acc

-- As 'baseOffsetsExpand' but with the zip and the strict left fold fused into
-- one hand-written recursion over the two lists (the base package
-- has no combined zip-fold), so the intermediate @zip osh oats@ list
-- of tuples is never built. The tuple list is only rank-1 long,
-- so this can matter at most marginally.
{-# INLINE baseOffsetsExpandZF #-}
baseOffsetsExpandZF :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsExpandZF o0 osh (Strides oats) = go (VU.singleton o0) osh oats
  where go !acc (nd : nds) (sd : sds) =
          go (VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc) nds sds
        go !acc _          _          = acc

-- Micro-optimised 'baseOffsetsExpand': seed the fold from the first dim's
-- 'enumFromStepN' (one fewer concatMap layer everywhere, and pure
-- enumFromStepN with no concatMap at all when there is a single outer dim).
{-# INLINE baseOffsetsExpandB #-}
baseOffsetsExpandB :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsExpandB o0 osh (Strides oats) =
  case zip osh oats of
    []                -> VU.singleton o0
    ((n0, s0) : rest) -> foldl' expand (VU.enumFromStepN o0 s0 n0) rest
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- Int32 twin of 'baseOffsetsExpand'. Unlike 'baseOffsetsMut32' the
-- arithmetic itself runs in Int32 -- 'enumFromStepN' generates in the
-- element type -- so every 'concatMap' intermediate halves too, not only
-- the final table. Sound whenever every offset fits in Int32, whatever
-- the strides' signs: a partial base-offset after the first k dims is
-- @o0 + sum of the first k index*stride terms@, which is the offset of
-- the element whose remaining indices are all 0 -- a real element of the
-- view -- so for a valid view every intermediate lies within the source
-- and 'int32Fits' is the whole precondition. An earlier version argued
-- this from the terms being non-negative and flagged rev'd views as
-- needing their own bound; 'revShapes' now runs mixed-sign terms through
-- this builder, and the element-offset argument is the restatement that
-- flag asked for.
{-# INLINE baseOffsetsExpand32 #-}
baseOffsetsExpand32 :: Int -> ShapeL -> Strides -> VU.Vector Int32
baseOffsetsExpand32 o0 osh (Strides oats) =
  foldl' expand (VU.singleton (fromIntegral o0)) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a (fromIntegral sd) nd) acc

-- The run base-offsets as a prefix sum. Consecutive table entries differ by
-- only rank-many distinct values: @st_last@ within a stretch of the
-- innermost outer dimension, and at each odometer carry a per-level
-- constant -- the increment at the carrying level minus the rewind of every
-- level below it, @st_c - sum_{j>c} (n_j - 1) * st_j@. So the table is
-- @scanl' (+) o0@ over a delta stream, and 'VU.scanl'' is the one
-- pure-typed builder whose contract IS stateful-in-order -- the loophole in
-- "'VU.generate' is stateless" that no other strategy here uses.
--
-- The allocation half of that hope is REFUTED, by @diag@ and not by
-- argument: its figures are this comment's.
-- Stream fusion does collapse generate-then-scan into one loop with one
-- vector allocation -- but at -O1 the loop's state is a heap-allocated
-- @Either _ (Int, Int)@ rebuilt every entry: Right + pair + two I# boxes
-- = 9 words = 72 bytes per entry, measured exactly by @diag@ (10x the
-- table's own bytes on vgg-14-c512, against 1.00x for the mutable fills)
-- and visible in Core as boxed joinrec state. Dissolving compound stream
-- state is SpecConstr's job, and SpecConstr runs only at -O2; 'VU.generate'
-- escapes at -O1 only because its state is a bare Int index, which
-- worker/wrapper alone unboxes. The same tax is what the fused (9.2x on
-- Run 7's shapes), bq-unfold (8.3x) and unfold-add (27.9x) rows were
-- already paying: at
-- -O1, every stateful pure-typed builder boxes its state per step, and
-- only index-only 'VU.generate' and explicit mutable fills do not. So the
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
-- produce their result through 'VU.generate' and build their table with this
-- scan, so neither needs the mutable concrete-Int scratch that their controls
-- 'fbBQmut' and 'fbOffTab' rest on, and neither needs a new 'Vector' class
-- method: the table is concrete index scratch, as the shipped
-- 'baseOffsetsExpand' one already is. Orthotope's library carries no mutable
-- code, so that is the difference between a shipping candidate and a mere
-- bound on what purity costs. When this was written 'fbOffTab' was the
-- fastest strategy needing no new class method and the fastest pure strategy
-- was well behind it; Run 6 (-O1) reordered both ends and Run 7 (Harness)
-- swung one back -- the scan consumers'
-- rows now carry "nothing (pure)" in README's @needs@ column,
-- 'fbOffTab' runs ahead of 'fbBQscanMulback' again, and 'fbOffTabScan' lost
-- its control, with the figures at its own comment -- so what this paragraph
-- still carries is the tier argument, not any ordering.
-- Figures stay in README.md, as everywhere else in this file.
--
-- The @m == 0@ guard keeps the LENGTH CONTRACT, and that alone. A zero
-- dimension passes the unit-dim filter (@n /= 1@ keeps 0); without the guard
-- the scan returns a one-element table where 'baseOffsetsExpand' and
-- 'baseOffsetsMut' return none, since 'VU.generate' of a negative length is
-- empty and 'scanl'' still prepends the seed (both measured, not reasoned) --
-- which is what the @builds@ arm of @check@ reports and end-to-end agreement
-- does not. What the guard does NOT protect against is a division: 'magicOf'
-- is total at 0, so a zero hoisted radix is harmless by itself. The two
-- guards are independent and both live, and 'degenerateShapes' is the
-- regression test for each. Unreachable in this harness, which has no zero
-- dimension -- but orthotope has zero-size arrays, and this builder is
-- proposed for it.
{-# INLINE baseOffsetsScan #-}
baseOffsetsScan :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsScan o0 osh (Strides oats)
  | m == 0 = VU.empty
  | otherwise =
      -- Asserted in the builder, not at the call sites: the multiply-high is
      -- internal to this function, so a caller with no Lemire of its own still
      -- inherits the bound -- which 'fbOffTabScan' does, and would otherwise
      -- have carried the precondition with nothing stating it.
      assert (lemireFits m)
      $ scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    scanned []   = VU.singleton o0
    scanned dims = VU.scanl' (+) o0 (VU.generate (m - 1) delta)
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
baseOffsetsScanRem :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsScanRem o0 osh (Strides oats)
  | m == 0 = VU.empty
  | otherwise = scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    scanned []   = VU.singleton o0
    scanned dims = VU.scanl' (+) o0 (VU.generate (m - 1) delta)
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
-- step's successor state, which 'VU.unfoldrExactN' discards -- so it must
-- not crash and does not.
{-# INLINE baseOffsetsOdo #-}
baseOffsetsOdo :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsOdo o0 osh (Strides oats)
  | m == 0 = VU.empty
  | otherwise = built [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    built []   = VU.singleton o0
    built dims = VU.unfoldrExactN m step (SOdo o0 nLast 0)
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
-- 'VU.generate' does not) but never in the constructive one, and under
-- -fspec-constr every state shape unboxes, so this arm is
-- indistinguishable from its control there. Failed Run 6 bore the prediction
-- out exactly and Run 6 (-O1) and Run 7 (Harness) repeated it:
-- 2.00x allocation, against the scan's 4.33x and the 1.33x a fully
-- unboxed emit would give. The diag verdict at -O1 is
-- already in: 16 bytes per entry against the scan's 72 -- the state
-- boxing is gone, confirming the law's constructive half for the state,
-- but one boxed Int per step survives in 'VU.unfoldrExactN''s emit pair,
-- which no state shape can reach. Preconditions of the
-- packing, asserted: every offset within its field, non-negative and
-- below 2^32, m at most 2^31 (the index field), on top of the mulhi
-- test's own bound. The offset bounds take each dimension at its
-- extremizing end, so they are exact for the mixed-sign strides
-- 'revShapes' feeds this builder, which an earlier corner formula was
-- not -- the restatement at the assert says how it was wrong. The
-- ARITHMETIC needed no change: the running offset is always the offset
-- of a real element of a valid view, so the low field never leaves
-- [0, source length) however the strides are signed.
{-# INLINE baseOffsetsScanPacked #-}
baseOffsetsScanPacked :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsScanPacked o0 osh (Strides oats)
  | m == 0 = VU.empty
      -- Strict bounds of their own: an offset of exactly 2^32 would mask to
      -- 0 in the low field, a negative one would borrow into the index
      -- field, and m <= 2^31 keeps every EMITTED index out of the sign bit
      -- (the discarded final successor may set it; nothing reads it).
      -- lemireFits m for the mulhi test is implied. The extreme offsets are
      -- per-dimension separable, so each bound takes every dimension at
      -- whichever end of its range extremizes it: 'maxOff' tops up the
      -- positive-stride dims, 'minOff' the negative ones. The first draft
      -- summed every dim's top into 'maxOff' -- the maximum only for
      -- non-negative strides; on a rev'd view it lands mid-range -- and
      -- carried no lower bound at all, which 'revShapes' is what exposed
      -- and 'revsome-mid-cnn-L2' is what observes: there the retired
      -- formula reads 158978 while the table's own maximum entry is
      -- 165881 (this bound reads exactly that), so the claimed maximum
      -- sat below a real offset. Only the CONSEQUENCE -- a 2^32 crossing
      -- admitted -- stays unfireable at harness scale, like the size
      -- preconditions near 'lemireFits'. Flipping the new conjunct to
      -- @minOff > 0@ fails the first shape's assert, so it is compiled
      -- in, by that comment's own proof route.
  | otherwise =
      assert (m <= 2147483648 && maxOff < 4294967296 && minOff >= 0)
      $ scanned [(n, st) | (n, st) <- zip osh oats, n /= 1]
  where
    m = product osh
    maxOff = o0 + sum [max 0 ((n - 1) * st) | (n, st) <- zip osh oats]
    minOff = o0 + sum [min 0 ((n - 1) * st) | (n, st) <- zip osh oats]
    scanned []   = VU.singleton o0
    scanned dims = VU.unfoldrExactN m step o0
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
-- picture rather than a fix: README.md#the-reader-read-runpy.
{-# NOINLINE fbGenQuotRem #-}
fbGenQuotRem :: ShapeL -> T -> VS.Vector Double
fbGenQuotRem sh (T (Strides ats) ao v) =
  VS.generate l (\i -> v VS.! (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (!q, !r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- 'fbGenQuotRem' with unsafeIndex, to isolate the bounds-check cost.
--
-- The third one-line variant of it -- those per-dimension divisions
-- replaced by 'fastQR' -- is deliberately not written, and the numbers that
-- rule it out are, on Run 7 (Harness), 'fbBQgenLemire' losing 1.35x at the
-- sibling site with the
-- loss growing in rank (so the division was never the per-dimension cost),
-- the output site capping the prize at 6.0% against a 7.9x gap to close, and
-- this arm and 'fbGenQuotRem' allocating 12x the result against
-- 'fbBQexpand''s 3.1x (so dropping the table costs allocation rather than
-- buying it). Recorded here rather than in README because that is where the
-- variant would be written.
{-# NOINLINE fbGenUnsafe #-}
fbGenUnsafe :: ShapeL -> T -> VS.Vector Double
fbGenUnsafe sh (T (Strides ats) ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (ao + offsetOf i ts' ats))
  where l : ts' = getStridesT sh
        offsetOf i (t:ts) (s:ss) = case i `quotRem` t of
                                     (!q, !r) -> q * s + offsetOf r ts ss
        offsetOf _ _      _      = 0

-- unfoldrExactN with an additive odometer state (point 2) --
-- no division, but an immutable list state rebuilt each step. It is an
-- allocating proxy for the truly fused, allocation-free form, which is
-- 'fbFused' below (README.md#the-reader-read-runpy).
-- 'VS.unfoldrExactN' is no method of orthotope's class, so this strategy
-- and 'fbFused' sit in the needs column's new-PURE-method tier: the method
-- is one delegation per instance to a pure builder vector already ships.
{-# NOINLINE fbUnfoldAdd #-}
fbUnfoldAdd :: ShapeL -> T -> VS.Vector Double
fbUnfoldAdd sh (T (Strides ats) ao v) =
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
fbFused sh (T (Strides ats) ao v) = VS.unfoldrExactN l step (S3 ao 0 0)
  where l = product sh
        !s = last sh
        !t = last ats
        -- @max 1 s@ as in 'fbBQunfold': a zero innermost extent would divide
        -- by zero here, and the bang forces it even though @l == 0@ makes the
        -- run count irrelevant. 'degenerateShapes' is what reaches this.
        !m = l `div` max 1 s
        !baseOffsets = VU.fromListN m (runBaseOffsets ao (init sh) (Strides (init ats)))
                         :: VU.Vector Int
        step (S3 o j q) =
          -- @next@ is forced: unbanged it is a thunk per step, which is
          -- precisely the "no per-step allocation" this strategy claims. The
          -- 'S3' boxes and 'unfoldrExactN''s emit pair remain, and at plain
          -- -O1 those are what the row's allocation multiple is (9.2x on
          -- Run 7's shapes); the thunk had been another 10x on top, which
          -- is why the pre-fix row read 20.7x beside a then-10.7x fixed
          -- one.
          let !x = VS.unsafeIndex v o
              !next
                | j + 1 < s = S3 (o + t) (j + 1) q
                | otherwise = let !q1 = q + 1
                              in  if q1 < m
                                  then S3 (VU.unsafeIndex baseOffsets q1) 0 q1
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
fbBaseOffsetsQuot sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsList ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBaseOffsetsQuot' with the run base-offsets built by a mutable
-- odometer fill of a concrete 'Int' scratch ('VU.create'/'VUM') instead of
-- @VU.fromListN (runBaseOffsets ...)@ -- dropping the @l/sInner@-element
-- intermediate list. This is NOT a class extension: the abstract output is
-- still produced by the ordinary 'VS.generate', and only the concrete Int
-- scratch (which 'fbBaseOffsetsQuot' already uses) is built differently.
-- Tests how much of 'fbMutOdo's edge is just the base-offsets list.
{-# NOINLINE fbBQmut #-}
fbBQmut :: ShapeL -> T -> VS.Vector Double
fbBQmut sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsMut ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

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
fbBQmutRuns sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmut' but building the base-offsets with 'VU.unfoldrExactN'
-- (a pure-typed builder whose mutation stays inside the vector library,
-- like 'VU.generate') instead of the explicit 'VU.create'/'VUM' fill of
-- 'fbBQmut'. No list, no explicit mutation in this module -- but the
-- odometer state is an immutable @[Int]@ rebuilt per run. Prices whether
-- the no-list base-offsets win survives without explicit mutation.
{-# NOINLINE fbBQunfold #-}
fbBQunfold :: ShapeL -> T -> VS.Vector Double
fbBQunfold sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        m = l `div` max 1 s
        rosh = tail (reverse sh)
        roats = tail (reverse ats)
        baseOffsets :: VU.Vector Int
        !baseOffsets = VU.unfoldrExactN m step (ao, replicate (length sh - 1) 0)
          where step (!o, is) = (o, adv o is rosh roats)
                adv !o []       _        _        = (o, [])
                adv !o (i : js) (n : ns) (st : sts)
                  | i + 1 < n = (o + st, (i + 1) : js)
                  | otherwise = let (!o', js') = adv (o - i * st) js ns sts
                                in  (o', 0 : js')
                adv !o _ _ _ = (o, [])
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmut' but with the run base-offsets built by the pure
-- 'baseOffsetsGen' ('VU.generate', no explicit mutation) instead
-- of 'baseOffsetsMut'. Answers "can the base-offsets be built fast without
-- explicit vector mutation?".
{-# NOINLINE fbBQgen #-}
fbBQgen :: ShapeL -> T -> VS.Vector Double
fbBQgen sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsGen ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- The per-dimension site: 'fbBQgen' with the run base-offsets built by
-- 'baseOffsetsGenLemire' instead of 'baseOffsetsGen', so 'bq-gen' is its
-- control.
{-# NOINLINE fbBQgenLemire #-}
fbBQgenLemire :: ShapeL -> T -> VS.Vector Double
fbBQgenLemire sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        -- Lemire is in the build here, so the bound is asserted there.
        !baseOffsets = baseOffsetsGenLemire ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmut' but with the run base-offsets built by the pure
-- 'baseOffsetsExpand' ('VU.concatMap', no explicit mutation) instead of
-- 'baseOffsetsMut'. The concatMap route to answering the no-mutation question.
{-# NOINLINE fbBQexpand #-}
fbBQexpand :: ShapeL -> T -> VS.Vector Double
fbBQexpand sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQexpand' with the fused zip-fold 'baseOffsetsExpandZF'
-- base-offsets build.
{-# NOINLINE fbBQexpandZF #-}
fbBQexpandZF :: ShapeL -> T -> VS.Vector Double
fbBQexpandZF sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpandZF ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQexpand' with the micro-optimised 'baseOffsetsExpandB'.
{-# NOINLINE fbBQexpandB #-}
fbBQexpandB :: ShapeL -> T -> VS.Vector Double
fbBQexpandB sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpandB ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

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
fbBQexpandQRprim sh (T (Strides ats) ao v) =
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
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get (I# i) = case quotRemInt# i s# of
          (# q, j #) -> VS.unsafeIndex v
                          (VU.unsafeIndex baseOffsets (I# q) + I# j * t)

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
fbBQexpandLemireOut sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !mg = assert (lemireFits l) $ magicOf s
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = case fastQR mg s i of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

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
fbBQexpandLemireMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

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
fbBQexpand32LemireMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l
               (VS.unsafeIndex v . fromIntegral . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        baseOffsets :: VU.Vector Int32
        -- NB 'int32Fits' is NOT the whole precondition here, unlike for
        -- 'baseOffsetsMut32': this builder does its arithmetic in Int32, so
        -- the partial base-offsets must fit too, and a source-length bound
        -- implies that only while every stride is non-negative. See the TODO
        -- on 'baseOffsetsExpand32'.
        !baseOffsets = assert (int32Fits v)
                       $ baseOffsetsExpand32 ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (fromIntegral (VU.unsafeIndex baseOffsets q)
                       + (i - q * s) * t)

-- The same output substitution against a second, unrelated table build:
-- 'fbBQmut', whose base-offsets come from a mutable odometer rather than
-- 'concatMap'. Every run base-offsets strategy shares the output line, so the
-- claim is that pricing it once prices it for all of them -- but that is an
-- inference from the shared source line, and this is the measurement of it.
-- It is also the interesting combination in its own right: 'bq-mut' beats
-- 'bq-expand' on time at a third of its allocation, so if the win carries,
-- this is the cheapest form of the fastest output.
{-# NOINLINE fbBQmutLemireOut #-}
fbBQmutLemireOut :: ShapeL -> T -> VS.Vector Double
fbBQmutLemireOut sh (T (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !mg = assert (lemireFits l) $ magicOf s
        !baseOffsets = baseOffsetsMut ao (init sh) (Strides (init ats))
        get i = case fastQR mg s i of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- 'fbBQmutLemireOut' with the output changed to the single-multiply mul-back
-- form, sharing 'fbBQexpandLemireMulback''s hoisted @s == 1@ branch. One line
-- differs from 'bq-mut-lemire-out' and one build differs from
-- 'bq-expand-lemire-mulback', so it has a control on each axis and reads as
-- a one-change variant of either. What it prices that nothing else does is
-- the output form on a mutable build; 'fbBQexpand32LemireMulback' and
-- 'fbOffTab32' price the Int32 narrowing separately.
{-# NOINLINE fbBQmutLemireMulback #-}
fbBQmutLemireMulback :: ShapeL -> T -> VS.Vector Double
fbBQmutLemireMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMut ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

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
fbBQmutRunsMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQmutRunsMulback' with the quotient by the Granlund-Montgomery magic
-- ('gmMagic') instead of the Lemire multiply-high -- one change, so that
-- strategy is its control, and the pair prices dropping the l < 2^32
-- restriction: same table, same mul-back remainder, one extra shift per
-- element, and no 'lemireFits' anywhere in the arm. Predicted within noise
-- of the control and is NOT: Run 7 (Harness) has it ~8% behind (1.077
-- paired, 3 wins of 24), the third run on which the verdict has held past
-- the floor.
-- Dropping the size bound costs real time on this build,
-- so the bound is worth keeping where it holds.
{-# NOINLINE fbBQmutRunsGmMulback #-}
fbBQmutRunsGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQmutRunsGmMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQexpandLemireMulback' with the table built by 'baseOffsetsScan'
-- instead of 'baseOffsetsExpand' -- one change, so that strategy is its
-- control. The pure sweet spot it was built to be, conditional on
-- SpecConstr, which is the standing assumption: under -fspec-constr the
-- build is allocation-free (diag, table + ~500 bytes) and the strategy is
-- predicted at 1.33x allocation and the fastest pure time in the table,
-- ahead of the class-extension tier. That prediction is Run 8's to settle
-- and nothing here has tested it: at plain -O1 the builder's stream state
-- boxes per entry, this inherits bq-expand-class allocation instead
-- (the record of that regime is the comment at 'baseOffsetsScan'), and
-- Run 7 (Harness) puts it at 4.33x and 0.123, mid-pack among the pure
-- arms -- 'fbBQscanPackedMulback' the fastest of them at 0.097.
-- Tunings to 'baseOffsetsScan' move this strategy and 'fbOffTabScan'
-- together -- deliberate coupling, the price of reusing the builder
-- verbatim; the difference against the control stays the build alone.
{-# NOINLINE fbBQscanMulback #-}
fbBQscanMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScan ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsScanRem' -- one
-- change, so that strategy is its control, and the pair prices the
-- builder's divisibility test alone: multiply-high against plain
-- 'quotRem', predicted ~neutral. If it measures neutral, the rem form is
-- what a shipped scan should use -- one less magic number in
-- Data/Array/Internal.hs, and the builder's own size bound gone.
{-# NOINLINE fbBQscanRemMulback #-}
fbBQscanRemMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanRemMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScanRem ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the quotient by the Granlund-Montgomery magic
-- ('gmMagic') instead of the Lemire multiply-high -- one change, so that
-- strategy is its control; the twin of 'fbBQmutRunsGmMulback' on the pure
-- side. The build is 'baseOffsetsScan' unchanged, so this arm's own
-- 'lemireFits' exposure is only the builder's internal one; the fully
-- restriction-free pure composition (scan-rem build + GM output) is one
-- further swap, deliberately not taken until each half is priced alone.
{-# NOINLINE fbBQscanGmMulback #-}
fbBQscanGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanGmMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsScan ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

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
-- nothing to find. Run 7 (Harness): it edges 'bq-scan-mulback', 0.119
-- against 0.123 (0.961 paired, 19 wins of 24), and trails
-- 'bq-scan-rem-mulback'
-- by 2.8%. So a shipped form CAN drop the
-- size
-- dispatch entirely, at a price of a few percent against the best scan
-- variant -- which is the trade to weigh on a machine whose arrays pass 2^32,
-- where the dispatch stops being a formality.
{-# NOINLINE fbBQscanRemGmMulback #-}
fbBQscanRemGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanRemGmMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsScanRem ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

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
fbBQodoMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsOdo ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsScanPacked' -- one
-- change, so that strategy is its control. The pair is only informative
-- at plain -O1 (see the builder's comment); under -fspec-constr the two
-- should be indistinguishable, and measuring that indistinguishability is
-- itself the control.
{-# NOINLINE fbBQscanPackedMulback #-}
fbBQscanPackedMulback :: ShapeL -> T -> VS.Vector Double
fbBQscanPackedMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsScanPacked ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral (mulhi magic (fromIntegral i))
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- Family 3: whole-offset and alternative-gather variants -- offsets for every
-- element rather than for every run, or a gather with no output division.

-- Offsets of every element, row-major over (sh, ats), starting at @o0@:
-- 'enumFromStepN' generates each innermost run directly (constant stride,
-- no division) and 'concatMap' nests the outer dims. Pure 'Vector' ops,
-- no intermediate list.
--
-- Storable, where every table but this one and 'baseOffsetsExpandVS' is
-- unboxed: its one consumer hands it to 'unsafeBackpermute', which takes a
-- single vector family, so here the table's flavour IS the payload's
-- (README.md#the-scratch-vector-flavour).
{-# INLINE strideOffsets #-}
strideOffsets :: Int -> ShapeL -> Strides -> VS.Vector Int
strideOffsets o0 sh0 (Strides ats0) = go o0 sh0 ats0
  where go o []       []         = VS.singleton o
        go o [n]      [st]       = VS.enumFromStepN o st n
        go o (n : ns) (st : sts) =
          VS.concatMap (\b -> go b ns sts) (VS.enumFromStepN o st n)
        go o _        _          = VS.singleton o

-- Build the whole offset vector with the all-'Vector'
-- 'strideOffsets', then gather through 'unsafeBackpermute' (vector's
-- tight, fused indexing loop). Two passes over @l@ and an extra
-- 'Int'-vector, but every step is a plain memory read. Orthotope's class
-- has no backpermute, so the README's needs column puts this in the
-- new-pure-method tier: 'vBackpermute', one delegation per instance.
{-# NOINLINE fbBackperm #-}
fbBackperm :: ShapeL -> T -> VS.Vector Double
fbBackperm sh (T strides ao v) = VS.unsafeBackpermute v (strideOffsets ao sh strides)

-- Drop the per-element output quotRem as well. The output is a
-- separable gather (offset[q*s+j] = baseOffsets[q] + j*t), so expand the outer
-- base-offsets as before, then gather with a FUSED 'map . concatMap': for each
-- base-offset, 'enumFromStepN' the inner run and read @v@. vector fuses
-- @map f (concatMap g x)@ into one stream, so there is no quotRem anywhere
-- and no full l-length offset table -- only the m-length base-offsets
-- materialise.
-- That fused pipeline is what the class cannot express: not for 'vMap''s
-- shape -- @v Int -> v Double@ is fine on every instance -- but because
-- 'concatMap' and 'enumFromStepN' are no methods of it, and the concrete
-- scratch they build here cannot feed a @v@-typed map. Hence the
-- new-pure-method tier: each is a one-line delegation, several of them.
{-# NOINLINE fbCMGather #-}
fbCMGather :: ShapeL -> T -> VS.Vector Double
fbCMGather sh (T (Strides ats) ao v) =
  VS.map (VS.unsafeIndex v)
         (VS.concatMap (\b -> VS.enumFromStepN b t s) baseOffsets)
  where s = last sh
        !t = last ats
        -- Storable, where every other table here is unboxed: the map below
        -- takes one vector family, so for this arm the table's flavour IS
        -- the payload's ('baseOffsetsExpandVS').
        !baseOffsets = baseOffsetsExpandVS ao (init sh) (Strides (init ats))

-- The whole offset grid over ALL dims via 'baseOffsetsExpandVS', then
-- one gather. Materialises the full l-length offset table (foldl' forces
-- each level), so it prices what 'fbCMGather''s fused inner run avoids.
-- Same new-pure-method tier as 'fbCMGather', for the same reason, and
-- Storable for the same reason too -- the map takes one vector family.
{-# NOINLINE fbAllExpand #-}
fbAllExpand :: ShapeL -> T -> VS.Vector Double
fbAllExpand sh (T strides ao v) =
  VS.map (VS.unsafeIndex v) (baseOffsetsExpandVS ao sh strides)

-- The full offset table (length @l@) built by the same mutable
-- odometer as 'fbMutOdo', then gathered with a single 'VS.generate' whose
-- callback is one contiguous Int read plus one strided value read -- no
-- quotRem, no multiply. Class-only (output via 'VS.generate'), but two
-- passes over @l@ and an @l@-sized Int scratch: prices whether dropping the
-- per-element arithmetic is worth the extra pass 'fbMutOdo' avoids.
{-# NOINLINE fbOffTab #-}
fbOffTab :: ShapeL -> T -> VS.Vector Double
fbOffTab sh (T (Strides ats) ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (VU.unsafeIndex offs i))
  where l = product sh
        !s = last sh
        !t = last ats
        offs :: VU.Vector Int
        !offs = VU.create $ do
          o <- VUM.unsafeNew l
          let writeRun !outPos !baseOff =
                let inner !j !src
                      | j >= s    = return ()
                      | otherwise = VUM.unsafeWrite o (outPos + j) src
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
-- and this halves both, taking the table's share of the 2.0x allocation
-- with them: 1.50x measured against 'fbOffTab''s 2.00x. 'fbOffTab' was the
-- fastest strategy needing no class extension when this was written, so this
-- asks whether narrowing moves it toward 'fbMutOdo', whose lead over it is
-- exactly that extra pass. Run 6 (-O1) said barely, inside the floor;
-- Run 7 (Harness) says the narrowing costs: 0.125
-- against 0.110 (1.133 paired, 5 wins of 24), while 'fbMutOdo' sits at
-- 0.084.
-- Odometer arithmetic stays in Int; only the store narrows, so
-- 'int32Fits' is the whole of its precondition -- it uses no multiply-high,
-- and so needs nothing from 'lemireFits'.
{-# NOINLINE fbOffTab32 #-}
fbOffTab32 :: ShapeL -> T -> VS.Vector Double
fbOffTab32 sh (T (Strides ats) ao v) =
  VS.generate l
    (\i -> VS.unsafeIndex v (fromIntegral (VU.unsafeIndex offs i)))
  where l = product sh
        !s = last sh
        !t = last ats
        offs :: VU.Vector Int32
        !offs = assert (int32Fits v) $ VU.create $ do
          o <- VUM.unsafeNew l
          let writeRun !outPos !baseOff =
                let inner !j !src
                      | j >= s    = return ()
                      | otherwise = VUM.unsafeWrite o (outPos + j)
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
-- builder is reused verbatim and no 'VU.create' remains -- the first pure
-- strategy with offtab's shape, an arithmetic-free gather off a
-- sequentially-read table. What it prices: whether offtab's pass-split
-- advantage (it beats 'bq-mut' despite strictly more traffic, because no
-- arithmetic delays the gather's loads) survives paying the delta
-- arithmetic l times rather than m and an l-length table. Unlike the
-- mulback strategies it needs no @s == 1@ branch: there is no output
-- division to guard.
--
-- The bet did not survive measurement: at 0.319 list against 'fbOffTab''s
-- 0.110 (Run 7 (Harness); Run 6 and a rough pass before it gave the same
-- verdict, so it is thrice measured), the builder's
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
fbOffTabScan sh (T strides ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (VU.unsafeIndex offs i))
  where l = product sh
        !offs = baseOffsetsScan ao sh strides

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
fbMutOdo sh (T (Strides ats) ao v) = VS.create $ do
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
-- recursion, not the nested structure. Run 7 (Harness) puts it at 64% of its
-- control's time (0.054 against 0.084, 0.635 paired) and fastest of
-- everything measured,
-- which reopens the class-method tier the README had closed at ~1.4x and
-- now prices at 2.35x over 'bq-expand'.
-- 'writeRun' is kept character-identical to 'fbMutOdo''s so the build
-- of each run cannot differ.
{-# NOINLINE fbMutOdoVecdims #-}
fbMutOdoVecdims :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdims sh (T (Strides ats) ao v) = VS.create $ do
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

-- 'fbMutOdo' but iterating the precomputed run base-offsets list, to
-- price what that list (a factor @sInner@ smaller than @l@) costs the
-- odometer-free variant against its control.
{-# NOINLINE fbMutBaseOffsets #-}
fbMutBaseOffsets :: ShapeL -> T -> VS.Vector Double
fbMutBaseOffsets sh (T (Strides ats) ao v) = VS.create $ do
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
         0 (runBaseOffsets ao (init sh) (Strides (init ats)))
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
fbBuild sh (T (Strides ats) ao v) = vBuildVS l $ \write ->
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
  in  void (go (init sh) (init ats) 0 ao)
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
fbMutFlat sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let goCopy !i
        | i >= l = return ()
        | otherwise = do
            VSM.unsafeWrite out i
              (VS.unsafeIndex v (VU.unsafeIndex baseOffsets i))
            goCopy (i + 1)
      go !i
        | i >= l = return ()
        | otherwise = do
            let !q = fromIntegral (mulhi magic (fromIntegral i))
            VSM.unsafeWrite out i
              (VS.unsafeIndex v
                 (VU.unsafeIndex baseOffsets q + (i - q * s) * t))
            go (i + 1)
  if s == 1 then goCopy 0 else go 0
  return out
  where l = product sh
        !s = last sh
        !t = last ats
        !magic = assert (lemireFits l)
                 $ if s <= 1 then 0
                   else (maxBound `quot` fromIntegral s) + 1 :: Word
        !baseOffsets = baseOffsetsMutRuns ao (init sh) (Strides (init ats))

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
fbConcatRuns sh (T (Strides ats) ao v) = VS.concat (go (init sh) (init ats) ao [])
  where s = last sh
        !t = last ats
        run !baseOff = VS.generate s (\j -> VS.unsafeIndex v (baseOff + j * t))
        go []       []         !o rest = run o : rest
        go (n : ns) (st : sts) !o rest =
          foldr (\i r -> go ns sts (o + i * st) r) rest [0 .. n - 1]
        go _        _          !o rest = run o : rest

-- The innermost-two transpose shared by the generators that model the
-- transpose a conv gather merges in ('mkStrided', 'mkSliced').
swapLast2 :: [a] -> [a]
swapLast2 xs = case reverse xs of
  (a:b:rest) -> reverse (b:a:rest); _ -> xs

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
      sh' = swapLast2 normalSh
      strides' = swapLast2 normalStrides
  in  (sh', T (Strides strides') 0 v)

-- Which of toVectorListT's regimes a (shape, T) pair takes: 1 whole-vector
-- memcpy, 2 innermost-normal per-run loop, 3 innermost-strided
-- per-element fallback (the one this benchmark is about). Mirrors the
-- branch logic in Data.Array.Internal.toVectorListT.
regimeOf :: ShapeL -> T -> Int
regimeOf sh (T (Strides ats) _ v)
  | ats == ts' && VS.length v == l = 1
  | null sh                        = 1
  | oks !! (length sh - 1)         = 2
  | otherwise                      = 3
  where l : ts' = getStridesT sh
        oks = scanr (&&) True (zipWith (==) ats ts')

-- The stride classes beyond 'mkStrided''s: regime-3 views the library
-- reaches through operations other than the merged transpose -- each
-- generator below models one producing operation, named at its comment.
-- Each class is its own pinned population, published beside the existing
-- geomean and never folded into it
-- (README.md#the-stride-classes-and-what-they-cover):
-- 'check' holds every strategy and builder to the reference on all of
-- them, the @classes@ benchmark mode times them -- one population per
-- process, per the protocol at 'classBenches' -- while the default run
-- stays the main set alone, and 'partitioned' holds every entry to
-- 'sizeCap'. @rotate@
-- deliberately has no generator: it is a composite of stretch, reshape,
-- window, stride and rev whose own output keeps innermost stride 1
-- (regime 2), and the strides a further transpose exposes -- negated sums
-- of dim products -- add no mechanism the rev and scaled classes do not
-- already cover. A general transpose likewise has no generator: no class
-- permutes the outer dims among themselves, the innermost-two swap aside.
-- Non-monotonic stride orders do occur incidentally ('gather48-src-50',
-- 'stretch-wide-2xM', 'bcastmid-primes'), the kernel walks the dims in
-- whatever order it is given with no order-sensitive branch, and
-- outer-dim order is the one axis with a measured null result behind it:
-- horde-ad's shm-reorder experiment moved nothing, in time or in
-- allocation. Add a permuting generator only if that measurement is ever
-- contradicted.
--
-- Why this coverage survives hand-built views: the constructors are
-- exported, so a program can write any strides and offset directly, yet a
-- VALID hand-built view (every box index in bounds; invalid views are
-- outside every contract here) can only recombine mechanisms these
-- classes exercise, because the fallback reads a view at three sites
-- only -- the regime test, the base-offsets build over the outer strides,
-- and the @base + j * tInner@ addressing. The claim is a HYPOTHESIS about
-- BENCHMARKING coverage, not a theorem: that strides and offset influence
-- the kernel's TIME only through regime membership, read locality within
-- and across runs, aliasing (cache warmth), and the magnitudes @sInner@,
-- @m@ and @l@ -- so one class per mechanism spans the performance space
-- although the value space is infinite. A separate and weaker claim: if
-- that hypothesis holds, the same classes are likely an EFFICIENT
-- coverage for correctness too, plausibly driving every conditional
-- branch a plausible strategy contains -- the @s == 1@ and @m == 0@
-- exits, the carry cascades, the sign-sensitive bounds -- though not
-- every branch on every input, which no finite set can.

-- Regime-3 view as @rev@ produces it: 'mkStrided''s view with EVERY
-- dimension reversed -- each stride negated, the offset moved to where the
-- reversed index map now starts. The un-reversed view is a permutation of
-- its dense source, so that offset is exactly @l - 1@ (the top), which the
-- class condition in 'check' pins. Negative strides and a non-zero offset
-- are the class's whole point: no 'mkStrided' input has either.
mkRev :: ShapeL -> (ShapeL, T)
mkRev normalSh =
  let (sh, T (Strides ats) _ v) = mkStrided normalSh
      ao = sum [(n - 1) * t | (n, t) <- zip sh ats]
  in  (sh, T (Strides (map negate ats)) ao v)

-- Regime-3 view as @rev@ of a SUBSET of the dims produces it:
-- 'mkStrided''s view with the dims named by the entry reversed, so the
-- strides are MIXED-sign -- the case 'mkRev''s all-negative form cannot
-- reach, and the one 'baseOffsetsScanPacked''s offset bounds extremize
-- per dimension for. The entries keep the subset strict and non-empty,
-- which the mixed-signs condition pins.
mkRevSome :: [Int] -> ShapeL -> (ShapeL, T)
mkRevSome rs normalSh =
  let (sh, T (Strides ats) _ v) = mkStrided normalSh
      ao = sum [(n - 1) * t | (r, (n, t)) <- zip [0 ..] (zip sh ats)
                            , r `elem` rs]
      ats' = [if r `elem` rs then negate t else t
             | (r, t) <- zip [0 ..] ats]
  in  (sh, T (Strides ats') ao v)

-- Regime-3 view as a broadcast produces it: the given shape read as the
-- VIEW shape, its innermost dimension stride-0 over a dense source of the
-- outer dimensions alone -- orthotope's @stretch@ (ox-arrays'
-- @X.replicate@) applied to a trailing size-1 array. Every run re-reads
-- one element @sInner@ times: the all-hits extreme no positive stride can
-- produce.
mkBroadcast :: ShapeL -> (ShapeL, T)
mkBroadcast sh =
  let osh = init sh
      v = VS.enumFromN (0 :: Double) (product osh)
      strides = Strides (drop 1 (getStridesT osh) ++ [0])
  in  (sh, T strides 0 v)

-- Regime-3 view as a broadcast of a MIDDLE axis produces it -- @reshape@
-- inserting a size-1 dim after the outermost, @stretch@ to @b@, then the
-- usual innermost-two transpose: a zero stride among the OUTER strides
-- with the innermost still strided, so the base-offsets TABLE carries
-- duplicated entries, where 'mkBroadcast''s innermost zero multiplies
-- runs and never table entries.
mkBroadcastMid :: Int -> ShapeL -> (ShapeL, T)
mkBroadcastMid b normalSh =
  case mkStrided normalSh of
    (s0 : srest, T (Strides (t0 : trest)) _ v) ->
      (s0 : b : srest, T (Strides (t0 : 0 : trest)) 0 v)
    _ -> error ("mkBroadcastMid: non-scalar shape expected: " ++ show normalSh)

-- Regime-3 view of a CONTIGUOUS array: @reshape@ appending a size-1
-- innermost dimension goes through orthotope's @simpleReshape@, which
-- gives every new size-1 dimension stride 0 -- so the data is dense and in
-- order, yet @last strides /= 1@ sends toVectorListT to regime 3, with
-- @sInner == 1@ and a base-offsets table as long as the result. The listed
-- shape is the dense one; the view appends the 1.
mkReshape1 :: ShapeL -> (ShapeL, T)
mkReshape1 normalSh = mkBroadcast (normalSh ++ [1])

-- Regime-3 view as @slice@ of a transposed enclosure produces it: the
-- dense source is the ENCLOSING shape, every dimension 2 larger, the view
-- cut at offset 1 in each and then innermost-two transposed as usual. So
-- the offset is non-zero, the backing is strictly larger than the view
-- spans, and the stride values are suffix products of a shape the view
-- does not show -- three things no 'mkStrided' input exhibits, and the
-- first structural separation of the source-bound ('int32Fits') from the
-- result-bound ('lemireFits') quantities (see the comment above those
-- predicates).
mkSliced :: ShapeL -> (ShapeL, T)
mkSliced normalSh =
  let esh = map (+ 2) normalSh
      v = VS.enumFromN (0 :: Double) (product esh)
      enclosingStrides = drop 1 (getStridesT esh)
      ao = sum enclosingStrides  -- slice offset 1 in every dimension
      sh' = swapLast2 normalSh
      strides' = swapLast2 enclosingStrides
  in  (sh', T (Strides strides') ao v)

-- Regime-3 view as @window@ produces it: the im2col patch tensor itself --
-- dense @[h, w]@ windowed to @[h-kh+1, w-kw+1, kh, kw]@ with strides
-- @[w, 1, w, 1]@, then the same innermost-two transpose the conv gather
-- merges in. The windowed strides DUPLICATE the source's, so distinct
-- output positions read the same element through distinct non-zero
-- strides: @l@ exceeds the backing and runs overlap, which is the overlap
-- README.md#non-urgent-todo-list records the main set as pessimistic
-- about.
mkWindow :: ShapeL -> (ShapeL, T)
mkWindow [h, w, kh, kw] =
  let v = VS.enumFromN (0 :: Double) (h * w)
      sh = [h - kh + 1, w - kw + 1, kw, kh]
      strides = Strides [w, 1, 1, w]
  in  (sh, T strides 0 v)
mkWindow sh = error ("mkWindow: [h, w, kh, kw] expected: " ++ show sh)

-- Regime-3 view with NO unit stride anywhere, as @stride@ composed over
-- @window@ and @slice@ reaches -- or as a hand-built T, the constructors
-- being exported: explicit strides over the tightest backing they span.
-- The entries keep the strides superincreasing (each exceeds the span of
-- the dims within it), so the map stays injective and the class stays
-- distinct from 'mkWindow''s overlap. Where every 'mkStrided' view keeps a
-- stride-1 second-innermost slot, this one has no stride-1 slot at all;
-- and its rank-1 entry reaches @m == 1@, the floor 'stretch-tall-Mx2''s
-- comment records as out of 'mkStrided''s reach.
mkScaled :: ShapeL -> Strides -> (ShapeL, T)
mkScaled sh strides@(Strides ats) =
  let n = 1 + sum (zipWith (\s t -> (s - 1) * t) sh ats)
      v = VS.enumFromN (0 :: Double) n
  in  (sh, T strides 0 v)

-- The conv-derived shapes (grouped inline below; see
-- README.md#the-shape-set for where they come from): a full patch tensor
-- is [outH, outW, Cin, KH, KW] -- output spatial, input channels, kernel
-- -- and a per-position slice is [Cin, KH, KW].
--
-- HALVED, and the eleven that went are not to come back one at a time.
-- What a shape exercises here is the view's innermost extent @sInner@ (the
-- second-to-last dim listed, so for a patch tensor the kernel height), the
-- rank, and @l@; a strategy has no way to see that two shapes came from
-- different papers. The dropped eleven each duplicated a kept one on all
-- three -- 'mnist-28-c1-k3' against 'cnn-L1-24x24-c1', 'vgg-14-c256-k3' and
-- 'deep-7-c512-k3' against 'vgg-14-c512-k3', 'cnn-slice-c64' against
-- 'cnn-slice-c32', and so on -- so they cost a proportional share of every
-- run's wall clock for coverage already held. The freed time went to A/A
-- controls, which calibrate every other figure and were the roster's scarce
-- resource (README.md#the-noise-floor-is-3-not-the-ci).
--
-- It DOES move the published geomean, which an earlier version of this
-- comment denied: the eleven skew small, and the base-offsets build is a
-- larger share of a small shape, so 'bq-expand' reads 6.5% lower over the
-- surviving set and ratios between strategies shift by up to ~6% -- both
-- past the noise floor. That is a change of population, not of any
-- strategy, and it is why Run 7 was read against Run 6 restricted to these
-- shapes rather than against its published column
-- (README.md#what-run-8-compares-against).
--
-- Two of the kept eleven are load-bearing beyond their workload and must
-- not be dropped in a later cut. 'gather48-src-50' and 'conv1d-24' are the
-- only CONV shapes whose two innermost listed dims DIFFER -- every other
-- conv shape ends in a square kernel, where @check@'s @sInner@ assertion's
-- two readings coincide and it would pass however it was written -- and the
-- first in run order to exercise it. Several stretch shapes differ too, so
-- the assertion does not go vacuous without these two; what would is the
-- conv set's own coverage of it.
convShapes :: [(String, ShapeL)]
convShapes =
  [ -- horde-ad shaped CNN (MnistCnnShaped2; kernel kh+1 = 3)
    ("cnn-L1-6x6-c1",       [6, 6, 1, 3, 3])          -- 324
  , ("cnn-L1-24x24-c1",     [24, 24, 1, 3, 3])        -- 5184
  , ("cnn-L2-24x24-c32",    [24, 24, 32, 3, 3])       -- 165888
  , ("cnn-slice-c32",       [32, 3, 3])               -- 288  (one position)
    -- MNIST LeNet-5
  , ("lenet-L1-28-c1-k5",   [28, 28, 1, 5, 5])        -- 19600
    -- CIFAR-10 scale
  , ("cifar-L2-16-c64-k3",  [16, 16, 64, 3, 3])       -- 147456
    -- ImageNet scale (only the layers whose per-call cost still buys, at
    -- criterion's default budget, the samples a tight fit needs)
  , ("vgg-14-c512-k3",      [14, 14, 512, 3, 3])      -- 903168
  , ("alexnet-L1-55-c3-k11",[55, 55, 3, 11, 11])      -- 1098075
  , ("alexnet-L2-27-c48-k5",[27, 27, 48, 5, 5])       -- 874800
    -- horde-ad gather48 benchmark layout [S, K, K, S]; both keep the
    -- @sInner@ assertion honest, see above
  , ("gather48-src-50",     [50, 3, 3, 50])           -- 22500
  , ("conv1d-24",           [24, 3, 3, 24])           -- 5184
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
    -- Two base offsets, and that is the floor THIS GENERATOR reaches.
    -- 'mkStrided' transposes the two innermost listed dims, so for @[.., b,
    -- c]@ the view has @m == product (init sh) * c@; forcing that to 1 forces
    -- @c == 1@, which makes the innermost stride 1 and the array regime 2.
    -- The only other route to one run is rank 1, and 'mkStrided' needs two
    -- innermost dims to transpose. So no shape here can reach @m == 1@.
    -- The orthotope library can produce such strides, though (stride or slice
    -- operation on a rank-1 array) -- now exercised, check-only, by
    -- 'scaled-rank1-m1' in 'scaledViews'.
  , ("stretch-tall-Mx2",    [900000, 2])              -- 1800000, 2 base offsets
  , ("stretch-coprime-r7",  [2, 3, 5, 7, 11, 13, 2])  -- 60060, rank 7, coprime
  , ("stretch-rank12",      [2,2,2,2,2,2,2,2,2,2,2,2])  -- 4096, deepest rank
    -- Sized to the 1800000 cap, which is what keeps it out of 'tooBig'. It
    -- keeps what it is for -- a base-offsets table as large as that cap
    -- allows (@m == l \/ 2@, tied with 'stretch-wide-2xM'), over a rank-3
    -- outer odometer, which is what separates it from that shape's rank-2
    -- grid of the same size.
  , ("stretch-tab7MB",      [900, 2, 1000])           -- 1800000, 900k-entry table
    -- The one shape here aimed at the CACHE rather than at the arithmetic.
    -- Every other stride in the set is odd, prime or huge; this one is 512
    -- elements, which for Double is 4096 bytes, which is one page and an
    -- exact multiple of the L1 way stride. So all 64 elements of a run land
    -- in one cache set on an 8-way L1 and 56 of them must miss, where a run
    -- of the same length at a stride of 3 costs a handful of lines. A
    -- power-of-two stride is the classic pathological gather, it is what an
    -- unforeseen caller is most likely to hand this code, and nothing else
    -- in the set produced one. It bounds the DAMAGE rather than the ranking:
    -- 'fbList' walks the same elements in the same order, so a cache
    -- catastrophe here is one the fallback being replaced shares.
  , ("stretch-pow2stride",  [54, 64, 512])            -- 1769472, page-aliased
    -- Fills the gap in the axis that decides which strategy wins. The set
    -- jumped 13 -> 1341 in @sInner@ with nothing between, which is most of
    -- the range where the base-offsets table stops dominating and the run
    -- copy starts to; 256 sits in it. Being a power of two it also prices
    -- what the output division would cost if it could be a shift, which is
    -- the measurement the padding idea died without (README.md#dead-ideas).
    -- Its stride is prime so the cache shape above is not confounded into
    -- it.
  , ("stretch-inner256",    [7, 256, 977])            -- 1750784, mid sInner
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

-- The stride-class input lists, one per generator above, checked in this
-- order after the main set and timed by the @classes@ mode through
-- 'classViews' (which also carries their 'sizeCap' conformity into
-- 'partitioned'). Each class reuses a listed shape of the main set where
-- one fits, so a figure, once recorded, has a positive-stride counterpart
-- to stand next to.
revShapes :: [(String, ShapeL)]
revShapes =
  [ ("rev-cnn-L1-24x24-c1", [24, 24, 1, 3, 3])  -- 5184, rev'd main workhorse
    -- innermost-two dims differ, keeping the swap under the rev honest
  , ("rev-gather48-src-50", [50, 3, 3, 50])     -- 22500
  , ("rev-primes",          [97, 89, 29])       -- 250357, rev'd stretch-primes
  ]

-- Dims to reverse (of the VIEW) beside the listed shape; strict non-empty
-- subsets -- innermost, outermost, and a middle pair.
revSomeShapes :: [(String, [Int], ShapeL)]
revSomeShapes =
  [ ("revsome-inner-primes", [2],    [97, 89, 29])    -- 250357
  , ("revsome-outer-g48",    [0],    [50, 3, 3, 50])  -- 22500
    -- mixed signs among the OUTER strides alone: the partial sums the
    -- packed scan's bounds extremize per dimension for
  , ("revsome-mid-cnn-L2",   [1, 2], [24, 24, 32, 3, 3])  -- 165888
  ]

-- Listed shape IS the view shape; the backing is its outer dims alone.
broadcastShapes :: [(String, ShapeL)]
broadcastShapes =
  [ ("bcast-inner8",   [64, 100, 8])    -- 51200, over a 6400-elem source
  , ("bcast-inner900", [50, 40, 900])   -- 1800000, long runs, tiny source
  , ("bcast-tall-Mx2", [900000, 2])     -- 1800000, 900k-run table, all hits
  ]

-- The stretch factor beside the dense shape whose middle axis broadcasts.
broadcastMidShapes :: [(String, Int, ShapeL)]
broadcastMidShapes =
  [ ("bcastmid-c32-cnn", 32, [24, 24, 3, 3])  -- 165888, mirrors cnn-L2-c32
  , ("bcastmid-primes",  89, [97, 29])        -- 250357
  ]

-- Listed shape is the dense array; the view appends the size-1 dim.
reshape1Shapes :: [(String, ShapeL)]
reshape1Shapes =
  [ ("reshape1-500k", [500000])         -- 500000, the [n] -> [n, 1] trap
  , ("reshape1-r3",   [100, 50, 36])    -- 180000, differing trailing dims
  ]

slicedShapes :: [(String, ShapeL)]
slicedShapes =
  [ ("slice-cnn-L2-24x24-c32", [24, 24, 32, 3, 3])  -- 165888, sliced c32
  , ("slice-primes",           [97, 89, 29])        -- 250357, sliced primes
  ]

-- Listed as [h, w, kh, kw]: image and kernel, not the view shape.
windowShapes :: [(String, ShapeL)]
windowShapes =
  [ ("window-28x28-k5",   [28, 28, 5, 5])    -- 14400, over 784 elements
  , ("window-224x224-k3", [224, 224, 3, 3])  -- 443556, over 50176
  ]

-- Views, not shapes like its siblings: explicit strides beside the shape,
-- superincreasing, none 1.
scaledViews :: [(String, ShapeL, Strides)]
scaledViews =
  [ ("scaled-super-r3", [40, 50, 30], Strides [4547, 91, 3])  -- 60000
  , ("scaled-rank1-m1", [300000], Strides [5])  -- 300000, the m == 1 floor
  ]

-- Every stride-class entry beside its built view, in the lists' order --
-- the one list the @classes@ benchmark mode and 'partitioned' both read,
-- so an entry cannot be timed at a size the cap never saw. The views are
-- thunks: nothing here forces a source vector until criterion's @env@
-- builds that group's input, and 'partitioned' forces shapes alone.
classViews :: [(String, (ShapeL, T))]
classViews =
  [(n, mkRev s) | (n, s) <- revShapes]
  ++ [(n, mkRevSome rs s) | (n, rs, s) <- revSomeShapes]
  ++ [(n, mkBroadcast s) | (n, s) <- broadcastShapes]
  ++ [(n, mkBroadcastMid b s) | (n, b, s) <- broadcastMidShapes]
  ++ [(n, mkReshape1 s) | (n, s) <- reshape1Shapes]
  ++ [(n, mkSliced s) | (n, s) <- slicedShapes]
  ++ [(n, mkWindow s) | (n, s) <- windowShapes]
  ++ [(n, mkScaled s sts) | (n, s, sts) <- scaledViews]

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
           -- the class populations obey the same cap, on their VIEW
           -- shapes, whose product is each entry's @l@
           && all ((<= sizeCap) . product . fst . snd) classViews

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
--   Force a 'Fill' arm run again under a second name and forced with ONE
--         element instead of the sum, so that subtracting it from its base
--         gives that sum as it actually occurs -- over a vector the fill has
--         just written, which is the one thing 'Term' cannot measure about
--         itself. Like 'Twin' it runs an already-checked function, so its own
--         entry checks nothing.
--   Only  checked but deliberately not timed; the reason is at the entry.
--
-- @read-run.py --lint@ reads the list below and holds it to what a reader of
-- either file assumes: every name documented in README.md, every @fb@
-- function defined here rostered, each 'Twin' naming the arm it duplicates,
-- and the controls named as that script's own control test recognises them.
--
-- ADDING AN ARM touches five places, listed because the last time they were
-- found one failing check at a time, after the arm had already been measured:
--
--   1. this 'roster', with the reason for the SLOT at the entry -- an arm's
--      position is part of what it measures;
--   2. README.md, or @--lint@ fails: the strategy list there is the index
--      every name has to appear in;
--   3. @read-run.py@'s 'is_control', if the arm is not a strategy, or it
--      enters the aggregates as one;
--   4. 'time_of', if a corrected time would be meaningless for it, as it is
--      for anything that never ran the forcing pass;
--   5. the 'health' sunk-cell warning and @--selftest@'s winsorizing check,
--      which assume every timed arm carries that pass.
--
-- 3 to 5 are one question asked three times -- is this arm a strategy? -- and
-- the 'Force' arms needed all three answered NO. An ordinary strategy needs
-- only 1 and 2.
data Arm = Base (ShapeL -> T -> VS.Vector Double)
         | Fill (ShapeL -> T -> VS.Vector Double)
         | Twin (ShapeL -> T -> VS.Vector Double)
         | Term
         | Force (ShapeL -> T -> VS.Vector Double)
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
    -- NOT the top of the table (0.074/0.092/0.099 are 8-34% apart) but
    -- two bands lower down. This one duplicates 'bq-scan-mulback' from
    -- ~28 slots away, so it prices the scan band -- which holds the
    -- shipping question, 'bq-scan-mulback' against 'bq-scan-rem-gm-mulback'
    -- -- and simultaneously spans the group,
    -- keeping position monitored rather than assumed now that SpecConstr
    -- changes code layout.
    --
    -- Aiming it at a SECOND strategy was a mistake, and Run 6 (-O1) is
    -- where it cost something. Failed Run 6 had found no position effect
    -- at -O1 -- its distant pair agreed to 0.14% against the adjacent
    -- one's 1.2%, and 0.34% against 0.36% paired -- because both slots
    -- ran 'bq-expand', so position was the only variable. This roster
    -- changed strategy and position together, and the distant pair now
    -- reads a +2.9% bias that the adjacent one does not. That is either
    -- a position effect or a property of this arm, and nothing here can
    -- say which. The crossed twins below now supply exactly that -- three
    -- strategies each in both slots, the scan band priced by its own
    -- adjacent twin -- and Run 7 ran them: the bias follows the slot,
    -- monotone in span (README.md#the-noise-floor-is-3-not-the-ci).
  , ("bq-scan-mulback-aa-distant", Twin fbBQscanMulback)
    -- The other two distant twins, added with the time the halved shape set
    -- freed. With these the controls are CROSSED: three strategies
    -- ('bq-expand', 'bq-scan-mulback', 'fbMutOdoVecdims') each duplicated
    -- once here and once beside its base, so position varies within a
    -- strategy and strategy varies within a position. Run 6 (-O1) could do
    -- neither -- its distant slot held a strategy its adjacent slot did not,
    -- so the +2.9% bias it found was a position effect or a property of that
    -- one arm and nothing could say which. That was the question these two
    -- arms existed to answer, and Run 7 answered it: the bias follows the
    -- slot across all three strategies, at +0.05% to +0.18% per slot of
    -- separation (README.md#the-noise-floor-is-3-not-the-ci).
  , ("bq-expand-aa-distant",       Twin fbBQexpand)
  , ("mut-odo-vecdims-aa-distant", Twin fbMutOdoVecdims)
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
    --
    -- Run 6 (-O1) licensed it -- 1.0001 paired, 0.21% per cell, no trend
    -- against shape size -- and Run 7 (Harness) re-passed it at 0.9989 and
    -- 0.23%; the correction is applied to every published figure
    -- (README.md#sum-only-and-the-correction-now-applied). Both halves
    -- stay in the roster, because this is a test every run must repeat:
    -- a run whose halves diverged would invalidate its whole time column,
    -- not merely decline to correct it. What this pair CANNOT test about
    -- itself -- that a fixed vector is read at the same cost as one the fill
    -- has just written -- is what the two 'Force' arms measure.
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
    -- effect (README.md#the-noise-floor-is-3-not-the-ci): ~18% in
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
    -- The second of the two 'Force' pairs, on the fastest strategy measured
    -- and so the one where the forcing term is the largest share of the
    -- bench (a median third of it, against an eighth of 'bq-expand'). If the
    -- term is biased at all, this is the arm the bias distorts most, and one
    -- pair on its own could not tell a biased term from a size-dependent
    -- one -- two pairs an octave apart in speed can.
  , ("mut-odo-vecdims-nosum",      Force fbMutOdoVecdims)
    -- The fast-end control, on the fastest strategy measured. Failed Run 6 put
    -- the floor at 2.0% duplicating a 0.099 arm against 0.14-1.2% on a
    -- 0.179 one -- and the noisier arm was the one allocating LESS, so
    -- the floor tracks 1/time rather than GC pressure. That predicted a
    -- larger floor still here, and the runs since split the prediction:
    -- per-cell scatter does track 1/time (1.13% here against 0.29% on the
    -- 'bq-expand' pair, Run 7), but it CANCELS, this pair's geomean landing
    -- at 0.9890 while the distant pairs carry span-ordered biases that do
    -- not. So keep
    -- this arm for the scatter it measures, and read the floor off the
    -- pairs that are biased, not the one that is merely noisy.
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
    -- The adjacent half of 'bq-scan-mulback''s pair, so this strategy has a
    -- twin in both positions exactly as 'bq-expand' does; the two together
    -- are what separate position from strategy.
  , ("bq-scan-mulback-aa-adjacent", Twin fbBQscanMulback)
  , ("bq-scan-rem-mulback",        Fill fbBQscanRemMulback)
  , ("bq-scan-gm-mulback",         Fill fbBQscanGmMulback)
  , ("bq-scan-rem-gm-mulback",     Fill fbBQscanRemGmMulback)
  , ("bq-odo-mulback",             Fill fbBQodoMulback)
  , ("bq-scan-packed-mulback",     Fill fbBQscanPackedMulback)
  , ("bq-expand-qr-prim",          Fill fbBQexpandQRprim)
  , ("bq-expand",                  Fill fbBQexpand)
    -- The same fill, forced with one element instead of the sum, so that
    -- 'bq-expand' minus this one is the forcing pass AS IT OCCURS: over a
    -- vector this fill has just written. That is the half of the
    -- @sum-only@ objection its own pair cannot reach -- both halves re-read
    -- one FIXED vector, a warmer and less contended read than summing what
    -- you have just produced, and a term biased by that would be biased
    -- alike on every shape and in both halves, so position-independence and
    -- scaling both pass and neither notices.
    --
    -- Adjacent to its base on purpose, against the roster's usual rule that
    -- controls straddle what they price: this pair is subtracted rather than
    -- divided, so what matters is that the two see the same cache and GC
    -- state, not that they span the group.
    --
    -- First measured on a seven-arm probe over the whole shape set: the
    -- in-situ term reads 0.990 of @sum-only@ here and 1.008 at
    -- 'fbMutOdoVecdims', so the objection is answered and the two bracket 1
    -- rather than sitting on one side of it, which a warmer fixed-vector read
    -- would have produced.
  , ("bq-expand-nosum",            Force fbBQexpand)
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
        -- 'Force' joins 'Twin' among the absent: it runs a function its base
        -- entry already checks, and checking it again would only assert that
        -- the same call gives the same answer.

-- Print the flagged (too-big) shapes, then benchmark every shape in
-- 'shapes' -- or, given the @classes@ argument, the stride-class
-- populations of 'classBenches' instead, any remaining arguments going to
-- criterion as usual, which is how one population is selected per process
-- (@classes rev-@). How to run: README.md#running-it. The numbers and how
-- to read them: README.md#results, README.md#the-reader-read-runpy.
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
        let cfg = defaultConfig { regressions = [(["iters"], "allocated")] }
        if "classes" `elem` args
          then withArgs (filter (/= "classes") args) $ do
            defaultMainWith cfg classBenches
            provenance (length classBenches)
          else do
            defaultMainWith cfg (map mkBench shapes)
            provenance (length shapes)

-- What a run records about itself, so that a document quoting its scale
-- copies a measured number instead of counting benches by hand -- which is
-- how README came to claim one bench more than the run it describes
-- actually held. The heap pair is the one micro.cabal's -M2G comment
-- rests on, and all of it comes from the -T stats that flag already asks
-- for, so nothing here needs a flag from the invoker. It goes to stderr,
-- leaving @--list@ and criterion's own stdout machine-readable, and it
-- reports the roster rather than what a filtered run selected.
--
-- The count is the roster's timed arms, not the 'Benchmark' nodes
-- 'benchView' built. Those are one per timed arm per GROUP, so counting
-- them reported their product -- 1452 where 44 was meant, in a line whose
-- whole purpose is to be quoted. Reading the roster is not the weaker
-- check it looks like: 'benchView' emits exactly one bench per timed arm,
-- so the two cannot differ. The group count is the caller's, naming the
-- benchmark list of the mode that ran.
provenance :: Int -> IO ()
provenance nGroups = do
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
    ++ show nGroups
    ++ " shapes; elapsed " ++ show h ++ "h" ++ show m ++ "m" ++ show sec
    ++ "s; peak " ++ mib (max_mem_in_use_bytes s) ++ " MiB in use, "
    ++ mib (max_live_bytes s) ++ " MiB max residency"

-- Benchmark one view ('benchView'; 'mkBench' builds the main set's view
-- with 'mkStrided'): every 'roster' arm, in that list's order, which is
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
-- What a 'Force' arm forces with: the fill runs in full -- every strategy
-- here writes its whole buffer before returning a vector at all -- and then
-- ONE element is read, in place of the O(l) sum every other arm carries.
--
-- Reading an element rather than taking 'VS.length' is deliberate: a length
-- does not depend on the buffer's contents, so it is the one thing an
-- optimiser could serve without the fill having happened, and the point of
-- this arm is that the fill DID happen and the sum did not. 'NOINLINE' here
-- and on every @fb@ is what stops the pair being fused into a single
-- indexing expression, which is the same protection the sum arms rely on.
-- The 'VS.null' guard costs one test per call and keeps the arm defined on a
-- degenerate shape, which nothing benchmarks today but @check@ carries.
touchLast :: VS.Vector Double -> Double
touchLast v = if VS.null v then 0 else VS.unsafeLast v
{-# NOINLINE touchLast #-}

benchView :: String -> (ShapeL, T) -> Benchmark
benchView name view =
  env (evaluate (force view)) $ \ ~(sh, a) ->
    bgroup name (concatMap (arm sh a) roster)
  where
    arm sh a (n, Base f)  = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Fill f)  = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Twin f)  = [bench n $ whnf (VS.sum . f sh) a]
    arm sh a (n, Term)    = [env (evaluate (force (reference sh a))) $
                               bench n . whnf VS.sum]
    arm sh a (n, Force f) = [bench n $ whnf (touchLast . f sh) a]
    arm _  _ (_, Only _)  = []

mkBench :: (String, ShapeL) -> Benchmark
mkBench (name, normalSh) = benchView name (mkStrided normalSh)

-- The stride-class populations as benchmarks, one 'bgroup' per
-- 'classViews' entry in that list's order -- reachable only through the
-- @classes@ mode, so the default run's composition and slot order stay
-- those of every recorded run. The recorded-run protocol for these is one
-- population per process, selected by prefix (@classes rev-@,
-- @classes bcast-@, ...): each JSON is then single-population, so the
-- reader never has to partition a geomean, and no class's figures owe
-- anything to another class's leftover heap state -- the position effect
-- the main set accepts WITHIN a pinned order, not across populations.
-- The full sequence, which a major run includes by default:
-- README.md#making-a-major-benchmark-run.
classBenches :: [Benchmark]
classBenches = [benchView n view | (n, view) <- classViews]

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
-- which is the gap this check exists to close, so add to both lists
-- together. Non-vacuity, per conjunct and not merely for the whole:
-- lengthening 'baseOffsetsScanRem', 'baseOffsetsOdo' or
-- 'baseOffsetsScanPacked' by one entry fails at the first shape
-- with @agree=True, builds=False@ -- the very split this check is
-- here for.
buildersMatch :: Int -> ShapeL -> Strides -> Bool
buildersMatch ao osh oats =
     rBuild == baseOffsetsGen        ao osh oats
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
  where rBuild = baseOffsetsList ao osh oats
        w32    = VU.map fromIntegral  -- Int32 table read back as the rest

-- The shared core of the stride-class checks: what the legacy 'one' asserts
-- of a 'mkStrided' view -- regime 3, every strategy agreeing with the
-- reference, every builder agreeing with 'baseOffsetsList' -- asserted of a
-- view from any generator, plus the CLASS CONDITIONS the caller computes
-- from the view in hand: the named structural properties that make the
-- class what it claims to be, so that a generator drifting out of its class
-- fails by name rather than passing as a different, weaker input. A failed
-- condition is named in the error like a disagreeing arm is.
oneView :: String -> ShapeL -> T -> [(String, Bool)] -> IO ()
oneView name sh a@(T (Strides ats) ao v) conds = do
  let rList  = reference sh a
      builds = buildersMatch ao (init sh) (Strides (init ats))
      bad    = [n | (n, f) <- checkedArms, f sh a /= rList]
      agree  = null bad
      reg    = regimeOf sh a
      failedConds = [c | (c, ok) <- conds, not ok]
  putStrLn $ name ++ ": view " ++ show sh ++ ", strides " ++ show ats
             ++ ", offset " ++ show ao
             ++ ", l=" ++ show (product sh)
             ++ ", backing=" ++ show (VS.length v)
             ++ ", regime=" ++ show reg
             ++ ", agree=" ++ show agree ++ ", builds=" ++ show builds
             ++ (if null failedConds then ""
                 else " FAILED " ++ unwords failedConds)
  unless (agree && builds && reg == 3 && null failedConds) $
    error ("CHECK FAILED: " ++ name
           ++ (if null failedConds then ""
               else ", class conditions failed: "
                    ++ unwords failedConds)
           ++ (if null bad then "" else ", disagreeing: " ++ unwords bad))

-- Correctness / non-vacuity, in its own mode (@cabal run micro -- check@) so
-- it runs as a separate process from the timed benchmark: every shape must
-- take regime 3 and every strategy must produce the same vector as the
-- reference. Which arms those are is 'checkedArms', read off the same
-- 'roster' the benchmark is built from, so a strategy cannot be timed
-- without being checked; a disagreeing arm is named rather than merely
-- counted, which a chain of @&&@ could not do. After the main set and the
-- degenerates, the stride-class lists run through 'oneView' with their
-- class conditions, in the order the lists are defined.
check :: IO ()
check = do
  mapM_ (\(n, s) -> putStrLn $ "FLAGGED too big, excluded: " ++ n ++ " "
                               ++ show s ++ ", l=" ++ show (product s))
        tooBig
  mapM_ one (shapes ++ degenerateShapes)
  mapM_ oneRev revShapes
  mapM_ oneRevSome revSomeShapes
  mapM_ oneBroadcast broadcastShapes
  mapM_ oneBroadcastMid broadcastMidShapes
  mapM_ oneReshape1 reshape1Shapes
  mapM_ oneSliced slicedShapes
  mapM_ oneWindow windowShapes
  mapM_ oneScaled scaledViews
  where
    one (name, normalSh) = do
      let (sh, a@(T (Strides ats) ao _)) = mkStrided normalSh
          rList   = reference sh a
          -- The builders' direct comparison lives in 'buildersMatch', whose
          -- comment carries the reason and the per-conjunct non-vacuity.
          builds  = buildersMatch ao (init sh) (Strides (init ats))
          bad     = [n | (n, f) <- checkedArms, f sh a /= rList]
          agree   = null bad
          reg     = regimeOf sh a
          -- What @read-run.py@ can only assume, asserted where the view is
          -- actually in hand. That reader has no strided shape in its JSON,
          -- so it takes the innermost extent to be the second-to-last dim as
          -- LISTED here, on a reading of 'mkStrided' -- and every @m@ and
          -- every @alloc@ multiple it prints inherits that reading unchecked.
          -- Wrong, it would scale a whole column by a constant with nothing
          -- to notice, which is the one way that column could be silently
          -- wrong for every strategy at once. Here the transposed view exists,
          -- so the reading is a fact about it and is tested rather than
          -- trusted: its innermost extent against that listed dim, and the
          -- run count the reader derives from it against the view's own.
          -- Non-vacuity: taking the LAST listed dim instead of the
          -- second-to-last fails at @gather48-src-50@, [50,3,3,50] viewed as
          -- [50,3,50,3] -- the first shape in run order whose two innermost
          -- dims differ, every conv shape before it ending in a square kernel
          -- where the two readings coincide. That coincidence is the reason
          -- the check has to run over the whole shape set and not a
          -- representative handful of it.
          sInnerView   = if null sh then 1 else last sh
          sInnerListed = case reverse normalSh of
                           _ : d : _ -> d
                           _         -> 1
          mView        = product (init sh)
          sInnerOK     = sInnerView == sInnerListed
                      && (sInnerView == 0 || mView == product sh `div`
                                             sInnerView)
      putStrLn $ name ++ ": normalSh " ++ show normalSh ++ " -> strided "
                 ++ show sh ++ ", l=" ++ show (product sh)
                 ++ ", regime=" ++ show reg ++ ", agree=" ++ show agree
                 ++ ", builds=" ++ show builds
                 ++ ", sInner=" ++ show sInnerView
                 ++ (if sInnerOK then "" else " MISMATCHED")
      unless (agree && builds && reg == 3 && sInnerOK) $
        error ("CHECK FAILED: " ++ name
               ++ (if sInnerOK then "" else ", sInner from the view is "
                   ++ show sInnerView ++ " where the listing's"
                   ++ " second-to-last dim is " ++ show sInnerListed)
               ++ (if null bad then ""
                   else ", disagreeing: " ++ unwords bad))
    -- The class conditions, one runner per stride class. Each names the
    -- structural properties its generator owes the class, computed from the
    -- view in hand and asserted by 'oneView' beside the shared regime,
    -- agreement and builder checks. Every conjunct is proven non-vacuous by
    -- a deliberate breakage that keeps the view VALID -- regime 3, agree and
    -- builds all still green, so the named condition is the only thing
    -- standing -- except where a record below says the conjunct's space is
    -- guarded elsewhere. Each record names its breakage and what fired.
    --
    -- Non-vacuity: leaving the outermost dim un-reversed (a valid partial
    -- rev) fails all-negative and offset-top together at the first rev
    -- shape; growing the backing by 7 with the offset at its top fails
    -- offset-top alone.
    oneRev (name, normalSh) =
      let (sh, a@(T (Strides ats) ao _)) = mkRev normalSh
      in  oneView name sh a
            [ ("all-negative", all (< 0) ats)
            , ("offset-top",   ao == product sh - 1) ]
    -- Non-vacuity: reversing every dim regardless of the entry's subset (a
    -- valid full rev) fails mixed-signs alone -- offset-rev-sum passes,
    -- deriving from the view; growing the backing by 7 with the offset
    -- shifted by 6 fails offset-rev-sum alone.
    oneRevSome (name, rs, normalSh) =
      let (sh, a@(T (Strides ats) ao _)) = mkRevSome rs normalSh
      in  oneView name sh a
            [ ("mixed-signs",    any (< 0) ats && any (> 0) ats)
            , ("offset-rev-sum", ao == sum [(n - 1) * negate t
                                           | (n, t) <- zip sh ats, t < 0]) ]
    -- Non-vacuity: doubling the backing fails one-elem-per-run alone.
    -- stride0-inner has no valid same-backing falsification: an innermost
    -- stride of 1 over the tight backing reads past the source and died on
    -- the reference's bounds check when tried, and a backing that admits it
    -- makes the view regime 2 -- so that conjunct's space is guarded by the
    -- bounds and regime checks, and it stands here as the class's
    -- definition rather than as a live tripwire.
    oneBroadcast (name, sh) =
      let (sh', a@(T (Strides ats) _ v)) = mkBroadcast sh
      in  oneView name sh' a
            [ ("stride0-inner",    last ats == 0)
            , ("one-elem-per-run", VS.length v == product (init sh')) ]
    -- Non-vacuity: appending the broadcast axis innermost instead of
    -- inserting it (a valid 'mkBroadcast'-shaped view) fails stride0-outer
    -- alone, stretch-factor staying true; doubling the backing fails
    -- stretch-factor alone.
    oneBroadcastMid (name, b, normalSh) =
      let (sh, a@(T (Strides ats) _ v)) = mkBroadcastMid b normalSh
      in  oneView name sh a
            [ ("stride0-outer",  0 `elem` init ats && last ats /= 0)
            , ("stretch-factor", VS.length v * b == product sh) ]
    -- Non-vacuity: building the dense strides innermost-two-swapped (a
    -- valid transposed view) fails contiguous alone -- at reshape1-r3, the
    -- rank-1 entry passing because the swap is the identity there, which is
    -- why the class keeps an entry with differing trailing dims.
    oneReshape1 (name, normalSh) =
      let (sh, a@(T (Strides ats) _ v)) = mkReshape1 normalSh
      in  oneView name sh a
            [ ("stride0-inner", last ats == 0)
            , ("contiguous",    VS.length v == product sh
                                && init ats
                                   == drop 1 (getStridesT (init sh))) ]
    -- Non-vacuity: slicing at the origin fails offset-positive alone;
    -- zeroing the margins as well fails both conditions, the view then
    -- being 'mkStrided''s own.
    oneSliced (name, normalSh) =
      let (sh, a@(T _ ao v)) = mkSliced normalSh
      in  oneView name sh a
            [ ("offset-positive",   ao > 0)
            , ("backing-enclosing", VS.length v
                                    == product (map (+ 2) normalSh)) ]
    -- Non-vacuity: an innermost stride of 2 in place of the duplicated one
    -- (still in-bounds) fails dup-stride alone; shrinking the view to a
    -- single patch fails aliasing alone.
    oneWindow (name, hwkk) =
      let (sh, a@(T (Strides ats) _ v)) = mkWindow hwkk
          dup = case ats of t : _ -> t == last ats
                            []    -> False
      in  oneView name sh a
            [ ("aliasing",   VS.length v < product sh)
            , ("dup-stride", dup) ]
    -- Non-vacuity: a 1 in an entry's stride list fails no-unit-stride
    -- alone -- the mistyped entry being exactly what it guards -- and five
    -- elements of backing slack fail tight-backing alone.
    oneScaled (name, sh, strides) =
      let (sh', a@(T (Strides ats) _ v)) = mkScaled sh strides
      in  oneView name sh' a
            [ ("no-unit-stride", all (>= 2) ats)
            , ("tight-backing",  VS.length v
                                 == 1 + sum (zipWith (\s t -> (s - 1) * t)
                                             sh' ats)) ]

-- Allocation diagnostic (run with @cabal run micro -- diag@): why is
-- 'fbBQmut' faster than 'fbBaseOffsetsQuot' when they share the same
-- 'VS.generate' output and the same @m@-element run base-offsets table?
-- Measure the heap a single base-offsets build allocates.
-- 'baseOffsetsList' feeds a lazy 'runBaseOffsets' list to 'VU.fromListN';
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
      let (sh, T (Strides ats) _ _) = mkStrided normalSh
          osh  = init sh
          oats = Strides (init ats)
          m    = product osh
      putStrLn $ "\n" ++ name ++ "  (m = " ++ show m ++ " base-offsets, "
                 ++ show (VU.length (baseOffsetsMut 0 osh oats)) ++ " built)"
      measure "  baseOffsetsList   fromListN . runBaseOffsets (lazy list) " (\k -> baseOffsetsList   k osh oats)
      measure "  baseOffsetsGen    VU.generate + per-run quotRem          " (\k -> baseOffsetsGen    k osh oats)
      measure "  baseOffsetsGenLemire  Gen with 'fastQR'                  " (\k -> baseOffsetsGenLemire k osh oats)
      measure "  baseOffsetsExpand VU.concatMap iterated expansion        " (\k -> baseOffsetsExpand k osh oats)
      measure "  baseOffsetsExpandZF  Expand, zip and fold fused          " (\k -> baseOffsetsExpandZF k osh oats)
      measure "  baseOffsetsExpandB   Expand seeded from the first dim    " (\k -> baseOffsetsExpandB  k osh oats)
      measure "  baseOffsetsScan   scanl' over a generated delta stream   " (\k -> baseOffsetsScan   k osh oats)
      measure "  baseOffsetsScanRem  Scan with quotRem divisibility       " (\k -> baseOffsetsScanRem k osh oats)
      measure "  baseOffsetsOdo    unfoldrExactN 3-Int odometer state     " (\k -> baseOffsetsOdo    k osh oats)
      measure "  baseOffsetsScanPacked  Scan with one-Int packed state    " (\k -> baseOffsetsScanPacked k osh oats)
      measure "  baseOffsetsMut    VU.create mutable odometer             " (\k -> baseOffsetsMut    k osh oats)
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
                loop (acc + VU.foldl' (\a x -> a + fromIntegral x) 0 (build k))
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
                      | otherwise = loop (acc + VU.sum (build k)) (k + 1)
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
