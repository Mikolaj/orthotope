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
import           Criterion.Measurement.Types.Internal (whnf')
import           Criterion.Types              (Benchmarkable (..),
                                               Config (regressions))
import           Data.Bits                    (countLeadingZeros, shiftR, (.&.))
import           Data.Int                     (Int32, Int64)
import           Data.List                    (foldl', isPrefixOf, sort,
                                               sortBy)
import qualified Data.Vector.Storable         as VS
import qualified Data.Vector.Storable.Mutable as VSM
import qualified Data.Vector.Unboxed          as VU
import qualified Data.Vector.Unboxed.Mutable  as VUM
import           GHC.Clock                    (getMonotonicTime)
import           GHC.Exts                     (Int (..), Word (..), build,
                                               int2Word#, quotRemInt#,
                                               timesWord2#, word2Int#)
import           GHC.Stats                    (RTSStats (allocated_bytes, elapsed_ns, gc_elapsed_ns, gcs, major_gcs, max_live_bytes, max_mem_in_use_bytes, mutator_elapsed_ns),
                                               getRTSStats)
import           System.Environment           (getArgs, lookupEnv, withArgs)
import           System.IO                    (IOMode (ReadMode), hGetLine,
                                               hPutStrLn, stderr, withFile)
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
-- bounds, and the -M8G heap cap in micro.cabal keeps any future shape in the
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
-- state is SpecConstr's job, and SpecConstr is off at plain -O1 -- its own
-- flag turns it on there, as -O2 does; 'VU.generate'
-- escapes at -O1 only because its state is a bare Int index, which
-- worker/wrapper alone unboxes. The same tax is what the fused, bq-unfold
-- and unfold-add rows were already paying: at
-- -O1, every stateful pure-typed builder boxes its state per step, and
-- only index-only 'VU.generate' and explicit mutable fills do not. So the
-- scan build allocates like 'baseOffsetsExpand' (a few percent apart on
-- the diag), not like 'baseOffsetsMut', and its strategies inherit
-- bq-expand-class allocation.
--
-- Under SpecConstr the refutation inverts: it dissolves the state and the
-- diag measures this build allocation-free (table + ~500 bytes on
-- vgg-14-c512, matching 'baseOffsetsMut'; 'baseOffsetsGen' and
-- 'baseOffsetsGenLemire' collapse to table-only too). Measured at -O2
-- first and re-measured under the flag alone, which suffices. What did NOT
-- survive re-measuring is the reading that the expands keep their
-- intermediates because those are data and not state: under the flag they
-- drop by about a third, keeping some. The figures are in README, at the
-- Run 8 question. So the failure
-- belongs to the compilation regime, not the design; -O1 is what this
-- harness measures because it is what a default cabal build of orthotope
-- ships, and promoting the design means shipping a flag on
-- Data/Array/Internal.hs -- OPTIONS_GHC -fspec-constr rather than -O2,
-- since the diag says the narrower one buys the whole builder-level
-- effect, which makes it a smaller thing to ask of a maintainer. Either
-- way it is that maintainer's decision and wants its own measurement: time
-- under either flag is unmeasured here, for every strategy.
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
-- bound on what purity costs. The tier is all this paragraph carries: which
-- arm leads within it has changed run over run, and orderings, like every
-- figure, stay in README.md.
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
-- -fspec-constr every state shape unboxes, so this arm was predicted
-- indistinguishable from its control there. Run 8 refuted the corollary and
-- a Core diff in both regimes said why. The premise holds: under the flag
-- both loops specialise to four raw arguments and neither boxes. What does
-- not follow is indistinguishability, because the unboxing removes the
-- CONTROL's cost and not this arm's -- at -O1 the control's loop carries a
-- boxed Either of a boxed pair of a boxed Int and allocates a Right per
-- step, all of which the flag deletes, while this arm loses only one 'I#'
-- unwrap and goes on paying its shift and mask ('uncheckedIShiftRA#' 32,
-- 'andI#' 0xffffffff) per element against the control's two plain adds. So
-- the flag pays off the debt the packing exists to avoid and leaves the
-- packing's interest due: identical 1.33x allocation, 1.11x the time on 24
-- shapes of 24. THE PACKING IS A -O1-ONLY OPTIMIZATION -- wherever
-- SpecConstr runs this arm is dominated by the plainer 'fbBQscanMulback' it
-- was built to beat, and it should not be proposed for a build carrying the
-- flag. At -O1 the prediction still stands, at the allocation multiple
-- README's table carries: below the scan's and above what a fully unboxed
-- emit would give. The diag
-- verdict at -O1 is already in: 16 bytes per entry against the scan's 72 --
-- the state boxing is gone, confirming the law's constructive half for the
-- state, but one boxed Int per step survives in 'VU.unfoldrExactN''s emit
-- pair, which no state shape can reach. The flag reaches it: the same diag
-- under -fspec-constr puts this builder at 1.00x, so there the emit pair
-- unboxes too and the packing has nothing left to buy. Preconditions of the
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
-- replaced by 'fastQR' -- is deliberately not written. Three measurements
-- rule it out, each in README: 'fbBQgenLemire' loses at the sibling site
-- with the loss growing in rank, so the division was never the
-- per-dimension cost; the output site caps the prize at a few percent
-- against the gap this arm would have to close; and this arm and
-- 'fbGenQuotRem' allocate several times what 'fbBQexpand' does, so dropping
-- the table costs allocation rather than buying it. Recorded here rather
-- than in README because that is where the variant would be written.
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
          -- -O1 those are what the row's allocation multiple is; the thunk
          -- had been another tenfold on top of them, which is why the bang
          -- stays.
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

-- 'fbBQexpandLemireMulback' with the quotient by the Granlund-Montgomery
-- magic ('gmMagic') instead of the Lemire multiply-high -- one change, so
-- that strategy is its control, and the pair prices dropping the l < 2^32
-- bound on the SHIPPED build where 'fbBQmutRunsGmMulback' prices it on a
-- mutable one. Added when the precondition ruling
-- (README.md#what-the-benchmark-does) stopped timing every Lemire arm: the
-- mul-back output was worth ~4% over plain 'quotRem' on this build at Run 8,
-- and without this arm that idea would have left the timed set with no
-- unconditional form to be measured in.
{-# NOINLINE fbBQexpandGmMulback #-}
fbBQexpandGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQexpandGmMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
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
-- of the control and is NOT: Run 8 (SpecConstr) has it ~9% behind at two
-- wins of 24, past the floor as on every run since the pair was written and
-- in both regimes. Dropping the size bound
-- costs real time on this build, so the bound is worth keeping where it
-- holds. That reading is now frozen: the precondition ruling stopped timing
-- the control, so Run 9 could not re-read the pair and no later run can
-- either while the ruling stands. What the ruling leaves measurable is this
-- arm against the other unconditional builds, which is claim 1.
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
-- SpecConstr, which is the standing assumption. Run 8 settled that
-- prediction and it came out a third right: under -fspec-constr the
-- allocation is the predicted 1.33x exactly and the arm's absolute per-call
-- time falls 31% -- but it lands
-- level with its own build control rather than ahead of it (1.0004 over 24
-- shapes), so the builder does not beat the expansion it replaces, and the
-- fastest pure time went to 'fbBQodoMulback' instead. Both halves of that
-- pair are untimed since the precondition ruling, so the reading is frozen
-- where Run 8 left it; the same builder comparison on unconditional arms is
-- claim 4's FIRST half, which every run since has read as a tie by the sign
-- test -- its second half, against 'fbBQexpand' rather than against the
-- build control, is an ordering from Run 16 on and README says so.
-- At plain -O1 the
-- builder's stream state boxes per entry and this inherits
-- bq-expand-class allocation
-- (the record of that regime is the comment at 'baseOffsetsScan'), leaving
-- it mid-pack among the pure arms. Orderings, as ever, are README.md's.
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
-- nothing to find. Run 7 (Harness) has it edging 'bq-scan-mulback' and
-- trailing 'bq-scan-rem-mulback' by a few percent. So a shipped form CAN
-- drop the size dispatch entirely, at that price against the best scan
-- variant -- which is the trade to weigh on a machine whose arrays pass
-- 2^32, where the dispatch stops being a formality.
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

-- 'fbBQodoMulback' with the Granlund-Montgomery quotient -- one change, so
-- that strategy is its control. This is the only unconditional arm built on
-- 'baseOffsetsOdo', and without it the odometer BUILD leaves the timed set
-- altogether under the precondition ruling, taking Run 8's fastest pure arm
-- (0.089) with it. Whether the build is worth its 4.67x-an-entry allocation
-- once the output costs a shift more is what Run 9 measures.
{-# NOINLINE fbBQodoGmMulback #-}
fbBQodoGmMulback :: ShapeL -> T -> VS.Vector Double
fbBQodoGmMulback sh (T (Strides ats) ao v)
  | s == 1 = VS.generate l (VS.unsafeIndex v . VU.unsafeIndex baseOffsets)
  | otherwise = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
        !baseOffsets = baseOffsetsOdo ao (init sh) (Strides (init ats))
        get i = let !q = fromIntegral
                           (mulhi magic (fromIntegral i) `shiftR` gsh)
                in  VS.unsafeIndex v
                      (VU.unsafeIndex baseOffsets q + (i - q * s) * t)

-- 'fbBQscanMulback' with the table built by 'baseOffsetsScanPacked' -- one
-- change, so that strategy is its control. The pair was held to be
-- informative only at plain -O1, its -fspec-constr reading expected to be a
-- null and to serve as a control on the harness rather than as a result.
-- Run 8 refuted that: 1.11x apart there on 24 shapes of 24 at identical
-- allocation. A Core diff placed the fault in the inference and not in the
-- harness -- the premise holds, both loops specialising and neither boxing,
-- but unboxing deletes the CONTROL's Either-of-pair and leaves this arm's
-- shift and mask standing. The builder's comment carries the mechanism and
-- the -O1-only ruling that follows from it.
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
-- Storable, where the index scratch here is otherwise unboxed: its consumer
-- takes one vector family, so for this arm the table's flavour IS the
-- payload's ('baseOffsetsExpandVS').
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
        -- Storable, where the index scratch here is otherwise unboxed: its
        -- consumer takes one vector family, so for this arm the table's
        -- flavour IS the payload's ('baseOffsetsExpandVS').
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
-- and this halves both, taking the table's share of the allocation with
-- them. 'fbOffTab' was the fastest strategy needing no class extension when
-- this was written, so this asks whether narrowing moves it toward
-- 'fbMutOdo', whose lead over it is exactly that extra pass. The answer is
-- the regime's, not the narrowing's: at -O1 (Run 7) the narrowing costs time
-- rather than buying it, and under -fspec-constr (Run 8) it buys 12% on 24
-- shapes of 24 -- but the pair inverts because the CONTROL regresses 22% in
-- absolute time there, the largest setback of that run and unexplained,
-- while this arm improves 6%. The narrowing's own Core is regime-invariant,
-- two 'intToInt32#' and a 'writeInt32Array#' in both, which is why it moves
-- with what it is measured against rather than with the flag.
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
-- The bet did not survive measurement, and has not on any run since: it
-- lands well behind 'fbOffTab', because the builder's per-entry state
-- boxing (see 'baseOffsetsScan') runs l times here and costs more than the
-- arithmetic-free gather saves, and its allocation lands several times
-- above the 2.0x the fused form promised. Two
-- tunings once listed as pending -- hoisting the second cascade level, an
-- Int32 table twin -- were premised on the fused form and are moot until
-- the state boxing itself is fixed, which at plain -O1 no pure-typed
-- builder escapes (the SpecConstr flag fixes it, as -O2 does: see
-- 'baseOffsetsScan').
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

-- 'fbOffTabScan' with the table built by 'baseOffsetsScanRem' -- one change,
-- so that strategy is its control, and the pair prices the divisibility
-- cascade against the multiply-high at the BUILD site rather than the
-- output one. Added with the precondition ruling
-- (README.md#what-the-benchmark-does), which drops the control: its bound
-- is the builder's 'lemireFits' and not an output division, so the
-- Granlund-Montgomery substitution that rescues the other Lemire arms does
-- nothing here and only the other builder does. Without this arm the pure
-- l-length-table gather leaves the timed set, 'fbOffTab' being the same
-- shape over a mutable Int scratch and so a tier away.
{-# NOINLINE fbOffTabScanRem #-}
fbOffTabScanRem :: ShapeL -> T -> VS.Vector Double
fbOffTabScanRem sh (T strides ao v) =
  VS.generate l (\i -> VS.unsafeIndex v (VU.unsafeIndex offs i))
  where l = product sh
        !offs = baseOffsetsScanRem ao sh strides

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
-- recursion, not the nested structure. It has been the fastest arm measured
-- ever since, which is what reopened the class-method tier the README had
-- closed (README.md#the-mutable-ceiling-taken).
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

-- The four FastReshape arms. The tree's own precedent for this family,
-- Data/Array/Internal/FastReshape.hs
-- (README.md#the-mutable-ceiling-taken, the amendment), differs from
-- 'fbMutOdoVecdims' -- once its cons-list odometer is put aside as the
-- representation 'mut-odo' already prices -- in loop arithmetic alone:
-- offsets stepped additively where this family multiplies or threads,
-- and loops counted down to zero. These arms port that difference one
-- axis at a time over the shared control: input axis, output axis, both
-- (the corner, doubling as the endpoint contrast -- read directly
-- against 'mut-odo-vecdims', not summed from marginals, which is the
-- reading that still stands if the solo margins sit inside the floor),
-- and the loop form on top of the corner. Margins in this band are
-- close, so before pricing any pair here, ask the question 'build'
-- taught (same README section): whether the two workers differ in Core
-- at all -- a pair with identical workers is a placement instrument, not
-- a measurement.
--
-- The bangs follow FastReshape's discipline -- every loop-carried
-- variable banged, per-level reads rebound through banged locals, bangs
-- kept where they look unneeded -- except its one structural habit: its
-- loops take the base case as a separate equation wildcarding the
-- accumulators (@recLoop 0 _ _ = return ()@), which leaves the loop
-- formally lazy in them, the bangs binding only the taken branch. All
-- four arms keep the family's single-equation guard form instead, banged
-- on every path.

-- 'fbMutOdoVecdims' with the input offset stepped additively -- @boff@
-- carried down and advanced by @st@ where the control computes
-- @baseOff + i * st@, the counter staying for the bound alone -- one
-- change, so that arm is its control. The axis FastReshape's @recLoop@
-- takes (@ioffs + is@); what it drops is the loop's one multiply.
{-# NOINLINE fbMutOdoVecdimsAddIn #-}
fbMutOdoVecdimsAddIn :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddIn sh (T (Strides ats) ao v) = VS.create $ do
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
                dim !i !op !boff
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (i + 1) op' (boff + st)
            in  dim 0 outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbMutOdoVecdims' with the output position stepped additively through
-- a precomputed outer output-strides table, the recursion returning unit
-- where the control returns the next position through the bind -- one
-- change, so that arm is its control. The axis FastReshape carries with
-- its precomputed @ost@ (@ooffs + os@). It can lose: the table costs one
-- more 'VU.unsafeIndex' per level entry, priced against a returned Int.
{-# NOINLINE fbMutOdoVecdimsAddOut #-}
fbMutOdoVecdimsAddOut :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddOut sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                !os = VU.unsafeIndex oostV lev
                dim !i !op
                  | i >= n    = return ()
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >> dim (i + 1) (op + os)
            in  dim 0 outPos
  go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV, oostV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)
        !oostV = VU.fromList (init (drop 1 (getStridesT sh)))

-- Both axes at once, so the 2x2 over the shared control closes: this arm
-- moving by more than the two solo arms combined is the interaction,
-- measured. Against 'mut-odo-vecdims' it is also the endpoint contrast
-- -- the whole of FastReshape's offset arithmetic in one reading.
{-# NOINLINE fbMutOdoVecdimsAddBoth #-}
fbMutOdoVecdimsAddBoth :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddBoth sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                !os = VU.unsafeIndex oostV lev
                dim !i !op !boff
                  | i >= n    = return ()
                  | otherwise = go (lev + 1) op boff
                                >> dim (i + 1) (op + os) (boff + st)
            in  dim 0 outPos baseOff
  go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV, oostV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)
        !oostV = VU.fromList (init (drop 1 (getStridesT sh)))

-- 'fbMutOdoVecdimsAddBoth' with FastReshape's count-down-to-zero loop
-- form -- one change, the form, applied at both loops, so that arm is
-- its control. The counters compare against 0 rather than a
-- register-held bound, which 'add-both' freed them for, its counters
-- being bounds and nothing else. The run loop cannot compute
-- @outPos + j@ from a falling counter, so the write position becomes a
-- carried cursor, and this is the one arm of the four whose run loop is
-- deliberately NOT character-identical to the family's 'writeRun': the
-- form under test lives in that loop, and the shared build would keep it
-- untested. The interface is unchanged, so the calls to it stay
-- identical.
{-# NOINLINE fbMutOdoVecdimsAddBothDown #-}
fbMutOdoVecdimsAddBothDown :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddBothDown sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !d !src !o
              | d <= 0    = return ()
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  inner (d - 1) (src + tInner) (o + 1)
        in  inner sInner baseOff outPos
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                !os = VU.unsafeIndex oostV lev
                dim !k !op !boff
                  | k <= 0    = return ()
                  | otherwise = go (lev + 1) op boff
                                >> dim (k - 1) (op + os) (boff + st)
            in  dim n outPos baseOff
  go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV, oostV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)
        !oostV = VU.fromList (init (drop 1 (getStridesT sh)))

-- The four arms below extend the FastReshape decomposition, added
-- 2026-08-24 for Run 20. The family's verdict
-- (README.md#the-mutable-ceiling-taken) refuted FastReshape's offset
-- arithmetic but left two mechanisms unpriced solo: the count-down run
-- fill -- the family's one recorded per-element mechanism, seven
-- instructions against the shared eight, measured only on top of the
-- output-stride table whose per-call cost buries it -- and the per-run
-- control flow, a non-tail call, a level check and a threaded return per
-- run, which no arm above varies. A same-day paired probe (the README
-- section above) pruned the four to two timed arms: the down fill's solo
-- arms are refuted by codegen and rostered 'Only', reasons at their
-- comments, and the leaf arms are the Run 20 additions.

-- 'fbMutOdoVecdims' with the run fill alone in the count-down form,
-- 'writeRun' kept character-identical to 'fbMutOdoVecdimsAddBothDown''s
-- -- one change, so 'mut-odo-vecdims' is its control. Refuted as a timed
-- arm the day it was written, so it is rostered 'Only': under the leaf
-- continuation @>> return (outPos + sInner)@ the live @outPos@ pushes
-- the down fill's loop invariants out of registers, 40 bytes over 11
-- instructions against the canonical 24 over 7 -- the extra four being
-- per-element reloads of @tInner@ and both base pointers, one of them
-- dead -- in the timed binary and its -g3 twin alike, and the probe
-- agrees (README.md#the-mutable-ceiling-taken). The down fill wants a
-- unit-return context: the output-stride table buys
-- 'fbMutOdoVecdimsAddBothDown' one at a price, the fused leaf buys
-- 'fbMutOdoVecdimsAddInLeafDown' one for free; this arm has none. The
-- outer loop keeps counting up, deliberately: there the counter is the
-- multiplier in @baseOff + i * st@, so the falling form is free only on
-- the additive arms.
{-# NOINLINE fbMutOdoVecdimsDown #-}
fbMutOdoVecdimsDown :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsDown sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !d !src !o
              | d <= 0    = return ()
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  inner (d - 1) (src + tInner) (o + 1)
        in  inner sInner baseOff outPos
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

-- 'fbMutOdoVecdimsAddIn' with FastReshape's count-down-to-zero form at
-- both loops -- one change, the form, so that arm is its control,
-- standing to it as 'fbMutOdoVecdimsAddBothDown' stands to
-- 'fbMutOdoVecdimsAddBoth'. Rostered 'Only', by the same reload
-- refutation as 'fbMutOdoVecdimsDown' above -- the same 40-byte fill in
-- both binaries, and the worse probe reading of the two, its fill copy
-- straddling a cache line on top of the reloads
-- (README.md#the-mutable-ceiling-taken). 'writeRun' is
-- character-identical to 'fbMutOdoVecdimsAddBothDown''s.
{-# NOINLINE fbMutOdoVecdimsAddInDown #-}
fbMutOdoVecdimsAddInDown :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInDown sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !d !src !o
              | d <= 0    = return ()
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  inner (d - 1) (src + tInner) (o + 1)
        in  inner sInner baseOff outPos
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !k !op !boff
                  | k <= 0    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (k - 1) op' (boff + st)
            in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbMutOdoVecdimsAddIn' with the leaf call fused into the innermost
-- outer level -- one change, so that arm is its control. The recursion
-- answers "which run am I in" with per-run control flow: enter 'go',
-- fail the level check, fill, and thread the next output position back
-- through an unboxed tuple. At @lev == rOuter - 1@ that pattern is
-- constant -- every run advances the output position by @sInner@ -- so
-- 'run' calls 'writeRun' directly and steps both cursors additively,
-- which is the output axis 'add-out' bought with a table, here at the
-- one level that pays it, for free. The top guard still fires, for
-- rank-1 views alone. 'writeRun' is kept character-identical to the
-- family's.
{-# NOINLINE fbMutOdoVecdimsAddInLeaf #-}
fbMutOdoVecdimsAddInLeaf :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInLeaf sh (T (Strides ats) ao v) = VS.create $ do
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
        | lev == rOuter - 1 =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                run !i !op !boff
                  | i >= n    = return op
                  | otherwise = writeRun op boff
                                >> run (i + 1) (op + sInner) (boff + st)
            in  run 0 outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op !boff
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (i + 1) op' (boff + st)
            in  dim 0 outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- Both new axes at once, so the Run 20 2x2 over 'fbMutOdoVecdimsAddIn'
-- closes: one change from 'fbMutOdoVecdimsAddInLeaf' (the form, at every
-- loop) and one from 'fbMutOdoVecdimsAddInDown' (the fused leaf).
-- Against 'add-in' it is the endpoint contrast, read directly, not
-- summed from marginals. 'writeRun' is character-identical to
-- 'fbMutOdoVecdimsAddBothDown''s.
{-# NOINLINE fbMutOdoVecdimsAddInLeafDown #-}
fbMutOdoVecdimsAddInLeafDown :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInLeafDown sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !d !src !o
              | d <= 0    = return ()
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  inner (d - 1) (src + tInner) (o + 1)
        in  inner sInner baseOff outPos
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | lev == rOuter - 1 =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !k !op !boff
                  | k <= 0    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (k - 1) op' (boff + st)
            in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbMutOdoVecdimsAddInLeafDown' with the fill unrolled by two, an
-- epilogue taking the odd or empty run -- one change, the fill body, so
-- that arm is its control; against 'fbMutOdoVecdimsAddInLeaf' it is the
-- form axis's third value. The unrolled fill has no counter at all, the
-- bound living on the output cursor, which always steps by one -- so it
-- is sound for zero and negative strides, and it supersedes the up/down
-- question inside the run rather than crossing it. The dead-ideas
-- ruling (README.md#dead-ideas) kills unrolling by the runtime @sInner@
-- only; a fixed factor was untested until the probe of 2026-08-24
-- (README.md#the-mutable-ceiling-taken), which also read the
-- intermediate fused-bound form -- counter merged into the cursor,
-- six instructions -- as a wash; that form is 'fbMutOdoVecdimsAddInLeafU1'
-- below, rostered for Run 25 to re-read the wash under the shim.
-- This is the arm the library ships: 'genericFillStrided' in
-- Data/Array/Internal.hs is its bang-for-bang port, landed 2026-08-24.
{-# NOINLINE fbMutOdoVecdimsAddInLeafU2 #-}
fbMutOdoVecdimsAddInLeafU2 :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInLeafU2 sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let !oEnd = outPos + sInner
            inner !o !src
              | o + 1 >= oEnd =
                  if o >= oEnd then return ()
                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src' = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src')
                  inner (o + 2) (src' + tInner)
        in  inner outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | lev == rOuter - 1 =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !k !op !boff
                  | k <= 0    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (k - 1) op' (boff + st)
            in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        -- No doubled stride here any more; see the fill's own note.
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbMutOdoVecdimsAddInLeafU2' with the fill not unrolled: the same
-- @oEnd@ cursor bound, one element per iteration, the epilogue as the
-- whole loop -- one change, so that arm is its control on the unroll
-- axis, and 'fbMutOdoVecdimsAddInLeaf', which differs from this in
-- carrying a counter beside the cursor, @j@ against @sInner@ with each
-- write at @outPos + j@, its control on the bound. This is the
-- intermediate fused-bound form the probe of 2026-08-24 read as a wash
-- against the counted leaf, 0.9967 at 5 of 9,
-- on a scratch build with no shim and so with its loop heads wherever
-- the native backend left them; rostered 2026-09-04 for Run 25 so the
-- two changes the shipped fill bundles are priced apart under
-- controlled placement (README.md#the-mutable-ceiling-taken). Read on
-- the dead-spot -g3 twin the same day: the rank-1 copy is the probe's
-- six instructions, the run-level copy seven, reloading the source base
-- from the stack once per element (README.md#what-is-open, the Run 25
-- entry).
-- Non-vacuity, 2026-09-04: dropping the @+ tInner@ from the recursive
-- call fails @check@ at @cnn-L1-6x6-c1@, naming this arm.
{-# NOINLINE fbMutOdoVecdimsAddInLeafU1 #-}
fbMutOdoVecdimsAddInLeafU1 :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInLeafU1 sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let !oEnd = outPos + sInner
            inner !o !src
              | o >= oEnd = return ()
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  inner (o + 1) (src + tInner)
        in  inner outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | lev == rOuter - 1 =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !k !op !boff
                  | k <= 0    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (k - 1) op' (boff + st)
            in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbMutOdoVecdimsAddInLeafU2' with the fill's bound a falling count
-- instead of the @oEnd@ cursor bound -- one change, so that arm is its
-- control. It exists for the allocator and not for the algorithm: in
-- Run 20's HEAD binary the run-level copy of the U2 fill keeps seven
-- values live and spills both base pointers, four stack reloads per
-- two elements, where its rank-1 copy keeps them in registers
-- (README.md#the-mutable-ceiling-taken). The count replaces @oEnd@
-- one for one, so the loop is a value lighter, and the same epilogue
-- takes the odd or empty run. Rostered 'Only' on 2026-08-27 and timed
-- from 2026-08-28. The bound is on the count and not the cursor, so it is
-- as sign-agnostic as its control. Non-vacuity, 2026-08-27: dropping
-- the @+ tInner@ from the second read fails @check@ at @cnn-L1-6x6-c1@,
-- naming this arm.
{-# NOINLINE fbMutOdoVecdimsAddInLeafU2Down #-}
fbMutOdoVecdimsAddInLeafU2Down :: ShapeL -> T -> VS.Vector Double
fbMutOdoVecdimsAddInLeafU2Down sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !d !o !src
              | d < 2 =
                  if d <= 0 then return ()
                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src' = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src')
                  inner (d - 2) (o + 2) (src' + tInner)
        in  inner sInner outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | lev == rOuter - 1 =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !k !op !boff
                  | k <= 0    = return op
                  | otherwise = go (lev + 1) op boff
                                >>= \op' -> dim (k - 1) op' (boff + st)
            in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        -- No doubled stride here any more; see the fill's own note.
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- The rework-proposal family
-- (README.md#the-two-stage-plan-and-the-rework-proposal): the
-- canonicalization pass and the arms that price it and the two
-- zero-stride conditions, each against 'fbMutOdoVecdims', the arm the
-- fix ships and the body every one of them varies. Their figures decide
-- nothing about regime 1, which no generator here builds natively, and
-- were read before 'mkRuns' built native regime-2 views; what the
-- composites price on the regime-3 populations is views that CANONICALIZE
-- into those regimes.

-- Canonicalize a view for dispatch: drop unit dimensions -- a size-1
-- dim contributes @0 * stride@ to every index whatever its stride --
-- then merge adjacent dimensions where @st_outer == n_inner *
-- st_inner@, the index sum's own distributivity, sign-agnostic, so it
-- fires on 'rev' views too. Both rewrites preserve the row-major
-- element sequence exactly; O(rank) list work per call.
canonView :: ShapeL -> [Int] -> (ShapeL, [Int])
canonView sh ats =
  let merge (!n, !st) ((n', st') : rest)
        | st == n' * st' = (n * n', st') : rest
      merge p rest = p : rest
      merged = foldr merge [] [p | p@(n, _) <- zip sh ats, n /= 1]
  in  (map fst merged, map snd merged)

-- 'fbMutOdoVecdims' behind 'canonView', the canonical natural-stride
-- case returned as an O(1) slice of the source -- the regime-1 hit the
-- pass exists for, which every 'reshape1' shape and 'stretch-inner1'
-- take -- and everything else filled by the control's own body over the
-- canonical dims, a unit innermost stride landing in the same
-- 'writeRun' at step 1. One change over 'fbMutOdoVecdims', so that arm
-- is its control and the pair prices the pass plus the rank it sheds
-- (the conv patch tensors merge, 'cnn-L2-24x24-c32' from rank 5 to 3).
-- Non-vacuity, 2026-08-25: reversing the natural-stride slice fails
-- @check@ at @stretch-inner1@, the first shape to take that branch.
{-# NOINLINE fbCanonVecdims #-}
fbCanonVecdims :: ShapeL -> T -> VS.Vector Double
fbCanonVecdims sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> VS.replicate l (VS.unsafeIndex v ao)
      (csh, cats)
        | cats == [1] -> VS.slice ao l v  -- lean, see 'fbLibStage2Lean'
        | otherwise -> VS.create $ do
            out <- VSM.unsafeNew l
            let !sInner = last csh
                !tInner = last cats
                !rOuter = length csh - 1
                oshV, oatsV :: VU.Vector Int
                !oshV  = VU.fromList (init csh)
                !oatsV = VU.fromList (init cats)
                writeRun !outPos !baseOff =
                  let inner !j !src
                        | j >= sInner = return ()
                        | otherwise   = do
                            VSM.unsafeWrite out (outPos + j)
                                            (VS.unsafeIndex v src)
                            inner (j + 1) (src + tInner)
                  in  inner 0 baseOff
                go !lev !outPos !baseOff
                  | lev >= rOuter = writeRun outPos baseOff
                                    >> return (outPos + sInner)
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

-- 'fbCanonVecdims' with the canonical unit-stride runs copied by
-- 'VS.unsafeCopy' -- memcpy for Storable -- instead of the per-element
-- loop, the run body chosen once per call; one change, so that arm is
-- its control. The case is the window class, whose canonical form has
-- innermost stride 1 (contiguous runs of the kernel row); on views
-- whose canonical innermost stride is neither natural nor 1 the two
-- arms share their whole body.
-- Non-vacuity, 2026-08-25: negating the copied run fails @check@
-- at @window-64x64-k1x9@, the class the copy branch exists for.
{-# NOINLINE fbCanonMemcpyR2 #-}
fbCanonMemcpyR2 :: ShapeL -> T -> VS.Vector Double
fbCanonMemcpyR2 sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> VS.replicate l (VS.unsafeIndex v ao)
      (csh, cats)
        | cats == [1] -> VS.slice ao l v  -- lean, see 'fbLibStage2Lean'
        | otherwise -> VS.create $ do
            out <- VSM.unsafeNew l
            let !sInner = last csh
                !tInner = last cats
                !rOuter = length csh - 1
                oshV, oatsV :: VU.Vector Int
                !oshV  = VU.fromList (init csh)
                !oatsV = VU.fromList (init cats)
                writeRunStep !outPos !baseOff =
                  let inner !j !src
                        | j >= sInner = return ()
                        | otherwise   = do
                            VSM.unsafeWrite out (outPos + j)
                                            (VS.unsafeIndex v src)
                            inner (j + 1) (src + tInner)
                  in  inner 0 baseOff
                writeRunCpy !outPos !baseOff =
                  VS.unsafeCopy (VSM.unsafeSlice outPos sInner out)
                                (VS.unsafeSlice baseOff sInner v)
                writeRun = if tInner == 1 then writeRunCpy else writeRunStep
                go !lev !outPos !baseOff
                  | lev >= rOuter = writeRun outPos baseOff
                                    >> return (outPos + sInner)
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

-- 'fbMutOdoVecdims' with the run's read hoisted when the innermost
-- stride is 0 -- one read into a register, then stores, breaking the
-- per-element load -- the body chosen once per call; every other view
-- takes the control's own stepping run, so that arm is its control and
-- only the bcast class can separate the pair. No canonicalization: a
-- zero stride is not a unit dim and survives 'canonView' unchanged.
-- Non-vacuity, 2026-08-25: adding 1 to the hoisted read fails @check@
-- at @bcast-inner8@.
{-# NOINLINE fbBcastSet #-}
fbBcastSet :: ShapeL -> T -> VS.Vector Double
fbBcastSet sh (T (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRunStep !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      writeRunSet !outPos !baseOff =
        let !x = VS.unsafeIndex v baseOff
            inner !j
              | j >= sInner = return ()
              | otherwise   = VSM.unsafeWrite out (outPos + j) x
                              >> inner (j + 1)
        in  inner 0
      writeRun = if tInner == 0 then writeRunSet else writeRunStep
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

-- 'fbMutOdoVecdims' with a zero-stride OUTER level filled once and its
-- block copied to the level's remaining positions ('VSM.unsafeCopy',
-- disjoint output slices) -- the bcastmid case, where everything below
-- the zero stride repeats verbatim; zero levels compose, the topmost
-- firing and the ones below falling inside its one filled block. On
-- views with no zero outer stride the recursion is the control's own,
-- so 'fbMutOdoVecdims' is its control and only the bcastmid class can
-- separate the pair.
-- Non-vacuity, 2026-08-25: copying the block from one element over
-- fails @check@ at @bcastmid-c32-cnn@.
{-# NOINLINE fbMidCopy #-}
fbMidCopy :: ShapeL -> T -> VS.Vector Double
fbMidCopy sh (T (Strides ats) ao v) = VS.create $ do
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
                              VSM.unsafeCopy
                                (VSM.unsafeSlice dst blk out)
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

-- The stage-two endpoint, the arms above composed: 'canonView' first,
-- the natural-stride case an O(1) slice, then the odometer over the
-- canonical dims with zero-stride outer levels block-copied and the run
-- body chosen once per call -- hoisted stores at innermost stride 0,
-- 'VS.unsafeCopy' at 1, the stepping loop otherwise. Against
-- 'fbMutOdoVecdims' it prices the whole rework's regime-3 behaviour;
-- against the solo arms above, whether their conditions compose without
-- paying for each other. Its branches are textual copies of theirs, so
-- the non-vacuity breaks recorded at those definitions stand for these.
{-# NOINLINE fbCanonFull #-}
fbCanonFull :: ShapeL -> T -> VS.Vector Double
fbCanonFull sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> VS.replicate l (VS.unsafeIndex v ao)
      (csh, cats)
        | cats == [1] -> VS.slice ao l v  -- lean, see 'fbLibStage2Lean'
        | otherwise -> VS.create $ do
            out <- VSM.unsafeNew l
            let !sInner = last csh
                !tInner = last cats
                !rOuter = length csh - 1
                oshV, oatsV :: VU.Vector Int
                !oshV  = VU.fromList (init csh)
                !oatsV = VU.fromList (init cats)
                writeRunStep !outPos !baseOff =
                  let inner !j !src
                        | j >= sInner = return ()
                        | otherwise   = do
                            VSM.unsafeWrite out (outPos + j)
                                            (VS.unsafeIndex v src)
                            inner (j + 1) (src + tInner)
                  in  inner 0 baseOff
                writeRunSet !outPos !baseOff =
                  let !x = VS.unsafeIndex v baseOff
                      inner !j
                        | j >= sInner = return ()
                        | otherwise   = VSM.unsafeWrite out (outPos + j) x
                                        >> inner (j + 1)
                  in  inner 0
                writeRunCpy !outPos !baseOff =
                  VS.unsafeCopy (VSM.unsafeSlice outPos sInner out)
                                (VS.unsafeSlice baseOff sInner v)
                writeRun | tInner == 0 = writeRunSet
                         | tInner == 1 = writeRunCpy
                         | otherwise   = writeRunStep
                go !lev !outPos !baseOff
                  | lev >= rOuter = writeRun outPos baseOff
                                    >> return (outPos + sInner)
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
                                        VSM.unsafeCopy
                                          (VSM.unsafeSlice dst blk out)
                                          (VSM.unsafeSlice outPos blk out)
                                        copies (i + 1) (dst + blk)
                              copies 1 op'
                            else
                              let dim !i !op
                                    | i >= n    = return op
                                    | otherwise = go (lev + 1) op
                                                     (baseOff + i * st)
                                                  >>= dim (i + 1)
                              in  dim 0 outPos
            _ <- go 0 0 ao
            return out
  where l = product sh

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


-- 'fbMutFlat' with the Granlund-Montgomery quotient -- one change, so that
-- strategy is its control. It is the only unconditional FLAT fill: every
-- other direct-buffer arm ('fbMutOdo', 'fbMutOdoVecdims', 'fbBuild') walks
-- an odometer, so without this one the flat shape leaves the timed set under
-- the precondition ruling, and it left Run 8 second overall at 0.074.
{-# NOINLINE fbMutFlatGm #-}
fbMutFlatGm :: ShapeL -> T -> VS.Vector Double
fbMutFlatGm sh (T (Strides ats) ao v) = VS.create $ do
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
            let !q = fromIntegral (mulhi magic (fromIntegral i) `shiftR` gsh)
            VSM.unsafeWrite out i
              (VS.unsafeIndex v
                 (VU.unsafeIndex baseOffsets q + (i - q * s) * t))
            go (i + 1)
  if s == 1 then goCopy 0 else go 0
  return out
  where l = product sh
        !s = last sh
        !t = last ats
        !gm = gmMagic s
        !magic = fst gm
        !gsh = snd gm
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

-- The library-shaped arms: the whole of what a user's 'toVectorT' costs,
-- dispatch included, on every population -- so that a run reads a
-- library change class by class, not only the regime-3 fill the rest
-- of the roster isolates. Three, one per library form, each a port of
-- the library code and not a strategy of its own; their pairs are what
-- an orthotope user would measure.
--
-- Stage one as it shipped (Data/Array/Internal.hs at 0386073): regime 1
-- the vector itself or a slice, regime 2 one slice per maximal normal
-- suffix and a concatenation, regime 3 the fill 'genericFillStrided'
-- ports from 'fbMutOdoVecdimsAddInLeafU2'.
-- Non-vacuity, 2026-08-28: dropping the regime-2 branch (so those views
-- take the fill) leaves @check@ green, the fill being correct there --
-- which is why the runs class prices it rather than a check; slicing
-- from @o + 1@ fails @check@ at @runs-2@.
{-# NOINLINE fbLibStage1 #-}
fbLibStage1 :: ShapeL -> T -> VS.Vector Double
fbLibStage1 sh a@(T (Strides ats) ao v)
  | ats == ts' && VS.length v == l = v
  | null sh = VS.slice ao 1 v
  | oks !! (length sh - 1) = VS.concat (loop oks sh ats ao)
  | otherwise = fbMutOdoVecdimsAddInLeafU2 sh a
  where l : ts' = getStridesT sh
        oks = scanr (&&) True (zipWith (==) ats ts')
        loop (b : bs) (n : ns) (t : ts) !o
          | b = [VS.slice o (n * t) v]
          | otherwise = concat [loop bs ns ts (i * t + o) | i <- [0 .. n - 1]]
        loop _ _ _ _ = error "fbLibStage1: impossible"

-- Stage two as the branch pr-mikolaj-toVectorListT has it: the view
-- canonicalized ('canonView'), natural canonical strides the vector or a
-- slice, and everything else -- contiguous runs included -- filled by
-- 'fillStage2', the branch's driver. One change over 'fbLibStage1' per
-- population: on the main set none (both fill, the same loop), on the
-- runs class the route, on the broadcast classes the conditions.
-- The one dispatch that keeps the strides comparison after the ruling of
-- 2026-09-05 at 'fbLibStage2Lean', as that arm's control; every other
-- dispatch over 'canonView' here, and the branch's 'regimeT', took the
-- lean form.
{-# NOINLINE fbLibStage2 #-}
fbLibStage2 :: ShapeL -> T -> VS.Vector Double
fbLibStage2 sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      (csh, cats)
        | cats /= ts -> fillStage2 csh cats ao l v
        | ao == 0 && VS.length v == l -> v
        | otherwise -> VS.slice ao l v
        where _ : ts = getStridesT csh
  where l = product sh

-- 'fbLibStage2' with canonical contiguous runs sent back to one slice
-- per run and a concatenation, stage one's route for them over stage
-- two's dispatch -- the repair candidate if the runs class reads the
-- fill behind the memcpy at long runs. One change over 'fbLibStage2Lean',
-- so that arm is its control, and the pair is the runs class's question.
{-# NOINLINE fbLibStage2Concat #-}
fbLibStage2Concat :: ShapeL -> T -> VS.Vector Double
fbLibStage2Concat sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats)
        | last cats == 1 ->
            let !n = last csh
            in  VS.concat
                  [ VS.slice o n v
                  | o <- VU.toList (baseOffsetsList ao (init csh)
                                                    (Strides (init cats))) ]
        | otherwise -> fillStage2 csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

-- The run length at or above which 'fbLibStage2Disp' sends a contiguous
-- canonical run back to one slice, and the only thing it varies over
-- 'fbLibStage2Concat'. Read off the runs class rather than chosen: the
-- class sweeps the run from 2 to 65536, so what it can settle is which
-- pair of its lengths the crossover falls between, and any value inside
-- that pair selects the same route on every view this suite holds. The
-- number is therefore a bracket's representative and not a measurement of
-- its own, and a library taking this dispatch would want its own sweep.
-- Cut to 256 on 2026-08-30 inside a bracket of 96 to 1024; re-cut to
-- 2048 on 2026-09-02 by the one-binary probe README's task 9 records,
-- which put the crossover between `runs-1024` and `runs-4096` on the
-- dead-spot binary and read the 2048 arm nowhere behind the better route
-- past the class's floor, where 8192 and 32768 were behind it at 4096.
dispRun :: Int
dispRun = 2048

-- 'fbLibStage2Concat' with the slice route taken only where the canonical
-- run reaches 'dispRun' -- the dispatch on run length the runs class
-- measured a crossover for, and ONE change over that arm, so 'lib-stage2-
-- concat' is this one's control and 'lib-stage2-lean' the other side of
-- what it dispatches between. Below the threshold stage two's fill wins
-- and this arm is 'fbLibStage2Lean'; at or above it one memcpy per run
-- wins and this arm is 'fbLibStage2Concat'. Nothing that stays strided after
-- canonicalization is touched, so on every regime-3 population all three
-- are the same code and only the runs class separates them.
--
-- Non-vacuity is not something 'check' can give: every threshold is
-- correct, so the route has to be read off ALLOCATION, where the two
-- branches differ by construction -- the slice route builds a base-offset
-- table per call and the fill builds none. At 'dispRun' between the two
-- bracketing lengths this arm reads stage two's flat multiple below the
-- bracket and stage one's above it, which is what
-- probe-runlen-vacuity.log records.
{-# NOINLINE fbLibStage2Disp #-}
fbLibStage2Disp :: ShapeL -> T -> VS.Vector Double
fbLibStage2Disp sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats)
        | last cats == 1 && last csh >= dispRun ->
            let !n = last csh
            in  VS.concat
                  [ VS.slice o n v
                  | o <- VU.toList (baseOffsetsList ao (init csh)
                                                    (Strides (init cats))) ]
        | otherwise -> fillStage2 csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

-- 'fbLibStage2Disp' with the threshold an argument instead of 'dispRun',
-- added 2026-09-02 for the one-binary runs-class probe README's task 9
-- registers: one roster arm per candidate threshold over one copy of this
-- code, the fill and the slice route being the same NOINLINE functions
-- every other arm calls, so the arms differ in the number compared
-- against and in nothing else. The body above is kept as it is rather
-- than defined through this one, so that 'lib-stage2-disp' stays the code
-- Run 23 timed and reads as the probe's control. Not an @fb@ name, being
-- no arm: the three arms are the named applications below, which is the
-- form the roster parser in read-run.py reads -- rostered as partial
-- applications they were checked and timed and seen by no lint.
{-# NOINLINE libStage2DispAt #-}
libStage2DispAt :: Int -> ShapeL -> T -> VS.Vector Double
libStage2DispAt !thr sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats)
        | last cats == 1 && last csh >= thr ->
            let !n = last csh
            in  VS.concat
                  [ VS.slice o n v
                  | o <- VU.toList (baseOffsetsList ao (init csh)
                                                    (Strides (init cats))) ]
        | otherwise -> fillStage2 csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

fbLibStage2Disp2048, fbLibStage2Disp8192, fbLibStage2Disp32768
  :: ShapeL -> T -> VS.Vector Double
fbLibStage2Disp2048 = libStage2DispAt 2048
fbLibStage2Disp8192 = libStage2DispAt 8192
fbLibStage2Disp32768 = libStage2DispAt 32768

-- The branch's 'genericFillStrided' at Storable Double, ported
-- bang-for-bang: 'fbMutOdoVecdimsAddInLeafU2''s odometer and unrolled
-- run, the run body a static argument of the INLINE fused level, the
-- broadcast run hoisted at innermost stride 0, zero-stride outer levels
-- filled once and block-copied. Kept in step with the library by hand;
-- 'check' holds it to the reference on every view.
{-# NOINLINE fillStage2 #-}
fillStage2 :: ShapeL -> [Int] -> Int -> Int -> VS.Vector Double
           -> VS.Vector Double
fillStage2 sh ats !ao !l !v = VS.create $ do
  out <- VSM.unsafeNew l
  let {-# INLINE writeRunStep #-}
      writeRunStep !outPos !baseOff =
        let !oEnd = outPos + sInner
            inner !o !src
              | o + 1 >= oEnd =
                  if o >= oEnd then return ()
                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src' = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src')
                  inner (o + 2) (src' + tInner)
        in  inner outPos baseOff
      {-# INLINE writeRunSet #-}
      writeRunSet !outPos !baseOff =
        let !x = VS.unsafeIndex v baseOff
            !oEnd = outPos + sInner
            inner !o
              | o >= oEnd = return ()
              | otherwise = VSM.unsafeWrite out o x >> inner (o + 1)
        in  inner outPos
      copies !n !blk !src !dst
        | n <= 1 = return dst
        | otherwise = do
            VSM.unsafeCopy (VSM.unsafeSlice dst blk out)
                           (VSM.unsafeSlice src blk out)
            copies (n - 1) blk src (dst + blk)
      {-# INLINE runsWith #-}
      runsWith writeRun !n !st !outPos !baseOff
        | st == 0 = writeRun outPos baseOff
                    >> copies n sInner outPos (outPos + sInner)
        | otherwise =
            let run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter =
            (if tInner == 0 then writeRunSet else writeRunStep)
              outPos baseOff
            >> return (outPos + sInner)
        | otherwise =
            level (VU.unsafeIndex oshV lev) (VU.unsafeIndex oatsV lev)
        where
          level !n !st
            | lev == rOuter - 1 =
                if tInner == 0
                then runsWith writeRunSet n st outPos baseOff
                else runsWith writeRunStep n st outPos baseOff
            | st == 0 = do
                op' <- go (lev + 1) outPos baseOff
                copies n (op' - outPos) outPos op'
            | otherwise =
                let dim !k !op !boff
                      | k <= 0    = return op
                      | otherwise = go (lev + 1) op boff
                                    >>= \op' -> dim (k - 1) op' (boff + st)
                in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where !sInner = last sh
        !tInner = last ats
        -- No doubled stride here any more; see the fill's own note.
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fillStage2' with the stepping run unrolled by FOUR instead of two,
-- the odd remainder taken by the by-two loop and then the by-one tail
-- -- one change over that fill, so 'lib-stage2' is this arm's control.
-- What it buys is the loop's own overhead per element on long runs, the
-- cursor arithmetic and the bound test being paid once a quad rather
-- than once a pair; what it risks is the tail on short runs, where a
-- run of 3 or 5 never enters the quad loop and pays its test for
-- nothing. No live value is added: the quad steps the same cursor by
-- the same stride, which is the condition the NCG's allocator was
-- measured to want (README.md#what-moves-a-figure-when-no-strategy-changed).
-- RULED OUT FOR THE LIBRARY, 2026-08-30, by Mikolaj: a run unrolled by
-- four is too complex for orthotope, the shipped by-two loop being
-- itself close to that bar, and a simpler loop preferred over it where
-- the performance is close. The bar is taken per orthogonal feature, so
-- it rules out this loop wherever it appears and says nothing about
-- the features beside it. So this arm prices
-- what the loop would buy and is not a candidate to ship; the ruling is
-- in README beside the arm's entry.
{-# NOINLINE fillStage2U4 #-}
fillStage2U4 :: ShapeL -> [Int] -> Int -> Int -> VS.Vector Double
             -> VS.Vector Double
fillStage2U4 sh ats !ao !l !v = VS.create $ do
  out <- VSM.unsafeNew l
  let {-# INLINE writeRunStep #-}
      writeRunStep !outPos !baseOff =
        let !oEnd = outPos + sInner
            inner !o !src
              | o + 3 >= oEnd = pairs o src
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src1 = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src1)
                  let !src2 = src1 + tInner
                  VSM.unsafeWrite out (o + 2) (VS.unsafeIndex v src2)
                  let !src3 = src2 + tInner
                  VSM.unsafeWrite out (o + 3) (VS.unsafeIndex v src3)
                  inner (o + 4) (src3 + tInner)
            pairs !o !src
              | o + 1 >= oEnd =
                  if o >= oEnd then return ()
                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src' = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src')
                  pairs (o + 2) (src' + tInner)
        in  inner outPos baseOff
      {-# INLINE writeRunSet #-}
      writeRunSet !outPos !baseOff =
        let !x = VS.unsafeIndex v baseOff
            !oEnd = outPos + sInner
            inner !o
              | o >= oEnd = return ()
              | otherwise = VSM.unsafeWrite out o x >> inner (o + 1)
        in  inner outPos
      copies !n !blk !src !dst
        | n <= 1 = return dst
        | otherwise = do
            VSM.unsafeCopy (VSM.unsafeSlice dst blk out)
                           (VSM.unsafeSlice src blk out)
            copies (n - 1) blk src (dst + blk)
      {-# INLINE runsWith #-}
      runsWith writeRun !n !st !outPos !baseOff
        | st == 0 = writeRun outPos baseOff
                    >> copies n sInner outPos (outPos + sInner)
        | otherwise =
            let run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter =
            (if tInner == 0 then writeRunSet else writeRunStep)
              outPos baseOff
            >> return (outPos + sInner)
        | otherwise =
            level (VU.unsafeIndex oshV lev) (VU.unsafeIndex oatsV lev)
        where
          level !n !st
            | lev == rOuter - 1 =
                if tInner == 0
                then runsWith writeRunSet n st outPos baseOff
                else runsWith writeRunStep n st outPos baseOff
            | st == 0 = do
                op' <- go (lev + 1) outPos baseOff
                copies n (op' - outPos) outPos op'
            | otherwise =
                let dim !k !op !boff
                      | k <= 0    = return op
                      | otherwise = go (lev + 1) op boff
                                    >>= \op' -> dim (k - 1) op' (boff + st)
                in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fillStage2' with a run of 2, 3, 4 or 5 elements written by a body
-- unrolled to exactly that length -- no inner loop, no bound test, no
-- tail -- the body chosen once per row of runs as the broadcast body
-- already is, and every other run length taking the stepping loop
-- unchanged. One change over that fill, so 'lib-stage2' is this arm's
-- control. What it aims at is the per-run cost the counts put at about
-- thirteen instructions a run against about six an element, which on
-- the k3 and k5 convolution shapes and on the runs class's short end is
-- half the work or more; 'canonView' has already merged every run that
-- could be longer, so a short run here is short for good. One
-- deliberate asymmetry: the rank-1 leaf keeps the stepping loop at
-- every length, no rostered view reaching it with a short extent. The
-- complexity bar recorded at 'fillStage2U4' is taken per orthogonal
-- feature, so the short bodies are judged on their own and not with
-- the loop beside them; nothing rules them out, and Run 22 prices them.
-- RULED OUT FOR THE LIBRARY, 2026-09-04, by Mikolaj: a body per run
-- length of 2 to 5 is too repetitive and so too complex for orthotope,
-- by the bar the quad loop failed on 2026-08-30 -- taken per orthogonal
-- feature, so it rules out the short bodies wherever they appear -- in
-- 'fbLibStage2Short', and in the composite `lib-stage2-short-lean` that
-- stood beside it under the lean dispatch until 2026-09-05, when this
-- arm took that dispatch too and the composite, now the same code, was
-- removed -- and says nothing about the lean dispatch. The arm prices
-- what the bodies would buy and is not a candidate to ship; the ruling
-- is in README beside the arm's entry.
{-# NOINLINE fillStage2Short #-}
fillStage2Short :: ShapeL -> [Int] -> Int -> Int -> VS.Vector Double
                -> VS.Vector Double
fillStage2Short sh ats !ao !l !v = VS.create $ do
  out <- VSM.unsafeNew l
  let {-# INLINE writeRunStep #-}
      writeRunStep !outPos !baseOff =
        let !oEnd = outPos + sInner
            inner !o !src
              | o + 1 >= oEnd =
                  if o >= oEnd then return ()
                  else VSM.unsafeWrite out o (VS.unsafeIndex v src)
              | otherwise = do
                  VSM.unsafeWrite out o (VS.unsafeIndex v src)
                  let !src' = src + tInner
                  VSM.unsafeWrite out (o + 1) (VS.unsafeIndex v src')
                  inner (o + 2) (src' + tInner)
        in  inner outPos baseOff
      -- The four unrolled bodies, one per short run length.
      {-# INLINE writeRun2 #-}
      writeRun2 !outPos !baseOff = do
        VSM.unsafeWrite out outPos (VS.unsafeIndex v baseOff)
        VSM.unsafeWrite out (outPos + 1) (VS.unsafeIndex v (baseOff + tInner))
      {-# INLINE writeRun3 #-}
      writeRun3 !outPos !baseOff = do
        VSM.unsafeWrite out outPos (VS.unsafeIndex v baseOff)
        let !src1 = baseOff + tInner
        VSM.unsafeWrite out (outPos + 1) (VS.unsafeIndex v src1)
        VSM.unsafeWrite out (outPos + 2) (VS.unsafeIndex v (src1 + tInner))
      {-# INLINE writeRun4 #-}
      writeRun4 !outPos !baseOff = do
        VSM.unsafeWrite out outPos (VS.unsafeIndex v baseOff)
        let !src1 = baseOff + tInner
        VSM.unsafeWrite out (outPos + 1) (VS.unsafeIndex v src1)
        let !src2 = src1 + tInner
        VSM.unsafeWrite out (outPos + 2) (VS.unsafeIndex v src2)
        VSM.unsafeWrite out (outPos + 3) (VS.unsafeIndex v (src2 + tInner))
      {-# INLINE writeRun5 #-}
      writeRun5 !outPos !baseOff = do
        VSM.unsafeWrite out outPos (VS.unsafeIndex v baseOff)
        let !src1 = baseOff + tInner
        VSM.unsafeWrite out (outPos + 1) (VS.unsafeIndex v src1)
        let !src2 = src1 + tInner
        VSM.unsafeWrite out (outPos + 2) (VS.unsafeIndex v src2)
        let !src3 = src2 + tInner
        VSM.unsafeWrite out (outPos + 3) (VS.unsafeIndex v src3)
        VSM.unsafeWrite out (outPos + 4) (VS.unsafeIndex v (src3 + tInner))
      {-# INLINE writeRunSet #-}
      writeRunSet !outPos !baseOff =
        let !x = VS.unsafeIndex v baseOff
            !oEnd = outPos + sInner
            inner !o
              | o >= oEnd = return ()
              | otherwise = VSM.unsafeWrite out o x >> inner (o + 1)
        in  inner outPos
      copies !n !blk !src !dst
        | n <= 1 = return dst
        | otherwise = do
            VSM.unsafeCopy (VSM.unsafeSlice dst blk out)
                           (VSM.unsafeSlice src blk out)
            copies (n - 1) blk src (dst + blk)
      {-# INLINE runsWith #-}
      runsWith writeRun !n !st !outPos !baseOff
        | st == 0 = writeRun outPos baseOff
                    >> copies n sInner outPos (outPos + sInner)
        | otherwise =
            let run !k !op !boff
                  | k <= 0    = return op
                  | otherwise = writeRun op boff
                                >> run (k - 1) (op + sInner) (boff + st)
            in  run n outPos baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter =
            (if tInner == 0 then writeRunSet else writeRunStep)
              outPos baseOff
            >> return (outPos + sInner)
        | otherwise =
            level (VU.unsafeIndex oshV lev) (VU.unsafeIndex oatsV lev)
        where
          level !n !st
            | lev == rOuter - 1 =
                -- The choice, once per row: the broadcast body first,
                -- as in the control, then the short bodies by length.
                if tInner == 0
                then runsWith writeRunSet n st outPos baseOff
                else case sInner of
                  2 -> runsWith writeRun2 n st outPos baseOff
                  3 -> runsWith writeRun3 n st outPos baseOff
                  4 -> runsWith writeRun4 n st outPos baseOff
                  5 -> runsWith writeRun5 n st outPos baseOff
                  _ -> runsWith writeRunStep n st outPos baseOff
            | st == 0 = do
                op' <- go (lev + 1) outPos baseOff
                copies n (op' - outPos) outPos op'
            | otherwise =
                let dim !k !op !boff
                      | k <= 0    = return op
                      | otherwise = go (lev + 1) op boff
                                    >>= \op' -> dim (k - 1) op' (boff + st)
                in  dim n outPos baseOff
  _ <- go 0 0 ao
  return out
  where !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- 'fbLibStage2Lean' over 'fillStage2U4' -- the same dispatch, the fill
-- the one change, so 'lib-stage2-lean' is the control (since 2026-09-05;
-- its readings were taken against 'lib-stage2') and every population
-- where the fill runs reads the unrolling.
{-# NOINLINE fbLibStage2U4 #-}
fbLibStage2U4 :: ShapeL -> T -> VS.Vector Double
fbLibStage2U4 sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats) -> fillStage2U4 csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

-- 'fbLibStage2Lean' over 'fillStage2Short' -- the same dispatch, the
-- fill the one change, so 'lib-stage2-lean' is the control (since
-- 2026-09-05; its readings were taken against 'lib-stage2'); it can move
-- only where the canonical run is 2 to 5 elements long, and every other
-- view is the control's code.
{-# NOINLINE fbLibStage2Short #-}
fbLibStage2Short :: ShapeL -> T -> VS.Vector Double
fbLibStage2Short sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats) -> fillStage2Short csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

-- 'fbLibStage2' with the dispatch read off the merged form alone --
-- the same 'fillStage2', so the pair prices the dispatch and nothing
-- else. What licenses it: a canonical view of rank 2 or more can never
-- carry the natural strides, because 'canonView' merges exactly the
-- adjacent pairs the natural strides consist of -- 'getStridesT' sets
-- each outer stride to the inner dim times the inner stride, which is
-- the merge condition -- so the `cats /= ts` the control asks is
-- decided by the merged rank and the innermost stride, and the strides
-- list the control's dispatch builds and compares is not built. One
-- change over 'fbLibStage2', so that arm is the control, and 'check'
-- holds the equivalence on every view. It is also the simpler form,
-- which the complexity ruling at 'fillStage2U4' prefers where the
-- performance is close.
-- TAKEN 2026-09-05 for every dispatch that admits it, here and in the
-- branch's 'regimeT' (README.md#the-stride-classes-and-what-they-cover):
-- mainly for the simplification, no stride list built at the dispatch,
-- and for Run 24 reading this arm at or below 'fbLibStage2' on every
-- population of both halves. 'fbLibStage2' alone keeps the comparison,
-- as this arm's control. What does not admit it: the stage-one ports
-- and 'regimeOf', which compare RAW strides, where the invariant does
-- not hold; the unordered one-block tests, whose sort by absolute stride
-- can make a rank-2 canonical view one block; and 'check''s own regime
-- conditions, kept explicit so the equivalence is checked, not assumed.
{-# NOINLINE fbLibStage2Lean #-}
fbLibStage2Lean :: ShapeL -> T -> VS.Vector Double
fbLibStage2Lean sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise = case canonView sh ats of
      ([], _) -> whole
      ([_], [1]) -> whole
      (csh, cats) -> fillStage2 csh cats ao l v
  where
    l = product sh
    whole | ao == 0 && VS.length v == l = v
          | otherwise = VS.slice ao l v

-- The list consumer under each stage: 'toVectorListT' as the library has
-- it, then one concatenation of what it returns. The concatenation is the
-- same term in both arms, so the pair prices what building the list costs
-- -- stage one's slice recursion against stage two's base-offset table and
-- its 'VU.toList' -- in time and, exactly, in allocation. What a library
-- consumer that iterates the list pays, 'reduceT' and 'padT' among them.
--
-- Stage one's list (Data/Array/Internal.hs at 0386073): regime 1 the
-- vector, regime 2 the slice recursion over the normal suffix, regime 3
-- the fill as one element. 'fbLibStage1' is the same dispatch feeding
-- 'VS.concat' the same lists, so the two agree by construction.
{-# NOINLINE fbLibListStage1 #-}
fbLibListStage1 :: ShapeL -> T -> VS.Vector Double
fbLibListStage1 sh a@(T (Strides ats) ao v) = VS.concat parts
  where parts
          | ats == ts' && VS.length v == l = [v]
          | null sh = [VS.slice ao 1 v]
          | oks !! (length sh - 1) = loop oks sh ats ao
          | otherwise = [fbMutOdoVecdimsAddInLeafU2 sh a]
        l : ts' = getStridesT sh
        oks = scanr (&&) True (zipWith (==) ats ts')
        loop (b : bs) (n : ns) (t : ts) !o
          | b = [VS.slice o (n * t) v]
          | otherwise = concat [loop bs ns ts (i * t + o) | i <- [0 .. n - 1]]
        loop _ _ _ _ = error "fbLibListStage1: impossible"

-- Stage two's list, the branch's 'toVectorListT': the canonical
-- dispatch, contiguous runs as one slice each off a base-offset table
-- built by expansion ('runBaseOffsetsT' in the library, 'baseOffsetsExpand'
-- here, the same expansion) and listed, everything strided as one filled
-- element. One change over 'fbLibListStage1' per population: the list's
-- construction.
{-# NOINLINE fbLibListStage2 #-}
fbLibListStage2 :: ShapeL -> T -> VS.Vector Double
fbLibListStage2 sh (T (Strides ats) ao v) = VS.concat parts
  where parts
          | l == 0 = []
          | otherwise = case canonView sh ats of
              ([], _) -> whole
              ([_], [1]) -> whole
              (csh, cats)
                | last cats == 1 ->
                    let !n = last csh
                    in  [ VS.slice o n v
                        | o <- VU.toList (baseOffsetsExpand ao (init csh)
                                            (Strides (init cats))) ]
                | otherwise -> [fillStage2 csh cats ao l v]
        whole | ao == 0 && VS.length v == l = [v]
              | otherwise = [VS.slice ao l v]
        l = product sh

-- The unordered-list consumer under each stage: 'toUnorderedVectorListT'
-- and one concatenation, the third entry point the branch changes and
-- the one commutative reductions take. The two stage arms are each
-- their stage's one-block test in front of that stage's list body, so
-- the liblist arms are the fall-back halves and the pair prices the
-- entry point end to end; the third arm, below, is a candidate. Added
-- 2026-08-30 so that a shim-switch reading on the fills (Run 23's
-- LOOP_DEADSPOT) has these routes' sanity readings beside it, which no
-- test of the branch can show until GHC itself grows such a capability.
--
-- Stage one's test (Data/Array/Internal.hs at 0386073): sort the raw
-- (stride, dim) pairs descending and ask whether the sorted strides
-- are the sorted shape's natural strides; one slice if so, the released
-- 'toVectorListT' otherwise. Unit dims, mergeable dims and negative
-- strides all defeat it.
{-# NOINLINE fbLibUnordStage1 #-}
fbLibUnordStage1 :: ShapeL -> T -> VS.Vector Double
fbLibUnordStage1 sh a@(T (Strides ats) ao v)
  | ats' == ts' = VS.slice ao l v
  | otherwise = fbLibListStage1 sh a
  where (ats', sh') = unzip (sortBy (flip compare) (zip ats sh))
        l : ts' = getStridesT sh'

-- Stage two's test, the branch's: the same question asked of the
-- CANONICAL dims and sorted by absolute stride, so unit and mergeable
-- dims no longer defeat it and a reversed view is one block, read from
-- its lowest offset. One change over 'fbLibUnordStage1' per population:
-- the test and the fall-back move together, as this family's stage
-- pairs do throughout.
{-# NOINLINE fbLibUnordStage2 #-}
fbLibUnordStage2 :: ShapeL -> T -> VS.Vector Double
fbLibUnordStage2 sh a@(T (Strides ats) ao v)
  | l == 0 = VS.empty
  | oneBlock =
      let !start = ao + sum [ (n - 1) * st | (n, st) <- zip csh cats, st < 0 ]
      in  VS.slice start l v
  | otherwise = fbLibListStage2 sh a
  where !l = product sh
        (csh, cats) = canonView sh ats
        oneBlock =
          let (acats, csh') =
                unzip $ sortBy (flip compare) $ zip (map abs cats) csh
              _ : ts = getStridesT csh'
          in  acats == ts

-- Stage three, a candidate and not a port of anything: the one-block
-- test generalized into the dispatch. An unordered consumer owes no
-- order, so the view is walked in ADDRESS order whatever its logical
-- one: the canonical dims sorted by absolute stride, descending, from
-- the lowest offset -- a reversed axis covering the same addresses from
-- the other end -- and the sorted pairs canonicalized AGAIN, so that
-- every adjacent pair the sort brought together merges and the lean
-- rank test decides one block (rank 0, or rank 1 at stride 1: one
-- slice); everything else is ONE 'fillStage2' over the sorted positive
-- strides, every axis walked forward and the smallest stride innermost.
-- What it prices: Run 25's flip class read a reversed run at about twice
-- its forward cost on identical instructions, which this fill never
-- pays, and a transposed view fills with its smallest stride innermost.
-- Against 'fbLibUnordStage2' the margin also carries that arm's list
-- and concatenation, which a reducing consumer does not pay, so the
-- reading is the direction where stage two falls back to the list and
-- the tie where both slice. 'check' holds it to the reference as a
-- multiset, as it holds the other unordered arms.
-- In the library this is 'toUnorderedVectorListT' with its one-block
-- test and its fall-back to 'toVectorListT' replaced by this dispatch:
-- 'canonicalizeT' for 'canonView', and the two branches returned as
-- singleton lists, @[vSlice start l v]@ and @[vFillStrided ssh sats
-- start l v]@; the commit adding this arm carries the body. The dispatch
-- half stands on its own: the rank test over the re-canonicalized sorted
-- pairs equals the sorted natural-strides test the library asks today,
-- checked over 300000 random views and every view to rank 3 with extents
-- to 3 and strides to 4, a mutant skipping the re-canonicalization
-- failing it, so it can land as a simplification if the fill is refuted.
{-# NOINLINE fbLibUnordStage3 #-}
fbLibUnordStage3 :: ShapeL -> T -> VS.Vector Double
fbLibUnordStage3 sh (T (Strides ats) ao v)
  | l == 0 = VS.empty
  | otherwise =
      let (csh, cats) = canonView sh ats
          !start = ao + sum [ (n - 1) * st | (n, st) <- zip csh cats, st < 0 ]
          (acats, csh') =
            unzip $ sortBy (flip compare) $ zip (map abs cats) csh
      in  case canonView csh' acats of
            ([], _) -> VS.slice start l v
            ([_], [1]) -> VS.slice start l v
            (ssh, sats) -> fillStage2 ssh sats start l v
  where !l = product sh

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
-- 'sizeCap'. Regime-2 views have their own class since 2026-08-28,
-- 'runsShapes', for the route the library takes on them. @rotate@
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
--
-- Under the branch's fill the mechanism a view exercises is its CANONICAL
-- form: 'canonView' drops the unit dimensions and merges what merges before
-- 'fillStage2' dispatches, so two classes whose views canonicalize alike
-- time one mechanism twice, and a hand-built view is covered by the
-- canonical form it reaches and not by the operation that built it.
-- 'retiredClasses' below is that test applied to the classes here,
-- 2026-09-04, and the coverage claim reads per canonical mechanism since:
-- regime 1; contiguous runs by length, gap, offset and direction; the
-- broadcast body; the block copy; the strided fill with and without a
-- stride-1 level and with overlap; and per-call size.

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

-- The same trap over a STRIDED source, added 2026-08-25 so the class
-- stays discriminating for the canonicalizing arms. 'mkReshape1' appends
-- the size-1 dim to a DENSE array, so dropping that dim leaves a
-- contiguous run and the composite arm short-circuits to an O(1) slice --
-- which measures dispatch and not filling. Here the dim is appended to
-- 'mkStrided''s innermost-two-transposed view, so the canonical form is
-- still strided and neither a slice nor a run memcpy can serve it. Same
-- @l@, @sInner@ and @m@ as 'reshape1-r3', whose dense shape it takes, so
-- the pair differs in the source's stridedness and in the order of the
-- two trailing view dims the transpose swaps.
mkReshape1Strided :: ShapeL -> (ShapeL, T)
mkReshape1Strided normalSh =
  case mkStrided normalSh of
    (sh, T (Strides ts) o v) -> (sh ++ [1], T (Strides (ts ++ [0])) o v)

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
-- about. A six-entry listing adds a window stride @s@ and a kernel
-- dilation @d@ (2026-09-03): the outer strides become @s * w@ and @s@, the
-- kernel's @d@ and @d * w@, and the output shrinks to what the strided
-- and dilated kernel fits, as a strided or dilated convolution's patch
-- view has them. Four entries are @s = d = 1@.
mkWindow :: ShapeL -> (ShapeL, T)
mkWindow [h, w, kh, kw] = mkWindow [h, w, kh, kw, 1, 1]
mkWindow [h, w, kh, kw, s, d] =
  let v = VS.enumFromN (0 :: Double) (h * w)
      spanOf k = (k - 1) * d + 1
      sh = [(h - spanOf kh) `div` s + 1, (w - spanOf kw) `div` s + 1, kw, kh]
      strides = Strides [s * w, s, d, d * w]
  in  (sh, T strides 0 v)
mkWindow sh = error ("mkWindow: [h, w, kh, kw] or [h, w, kh, kw, s, d]"
                     ++ " expected: " ++ show sh)

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

-- Regime-3 view as @rev@ of a DENSE array produces it, whole or along
-- its last axis: natural strides with the reversed dims negated, the
-- offset where the reversed index map starts. The innermost stride is
-- -1 -- regime 2 mirrored, which no other class reaches, 'mkRev' negating
-- 'mkStrided' views whose innermost stride is never 1 -- and 'canonView'
-- merges sign-agnostically, so the whole reversal is one run at stride
-- -1 and a last-axis reversal is rows of them. Added 2026-09-03.
mkFlip :: [Int] -> ShapeL -> (ShapeL, T)
mkFlip rs sh =
  let v = VS.enumFromN (0 :: Double) (product sh)
      ts = drop 1 (getStridesT sh)
      ats = [if r `elem` rs then negate t else t | (r, t) <- zip [0 ..] ts]
      ao = sum [(n - 1) * t | (r, (n, t)) <- zip [0 ..] (zip sh ts)
                            , r `elem` rs]
  in  (sh, T (Strides ats) ao v)

-- Regime-2 view as @slice@ of a wider array produces it: a sub-block of
-- an enclosing dense array, every extent short of the enclosure's so
-- 'canonView' merges nothing, listed as view shape, enclosing shape and
-- offset. The axes 'runsShapes' fixes, swept: the gap between one run's
-- end and the next's start, from one element to a page, which decides
-- what each run's first read costs; a rank-3 block, so the fill's
-- odometer runs a level deeper per run where the slice route's per-run
-- cost is flat; and an offset off an 8-element boundary, which a memcpy
-- per run meets and a stepping loop does not. Added 2026-09-03.
mkBlock :: ShapeL -> ShapeL -> Int -> (ShapeL, T)
mkBlock sh esh ao =
  let v = VS.enumFromN (0 :: Double) (product esh)
  in  (sh, T (Strides (drop 1 (getStridesT esh))) ao v)

-- Views a few hundred elements or less, one per canonical regime, over
-- the tightest backing their strides span: every other population is
-- thousands of elements and up, so a per-call cost -- the dispatch,
-- 'canonView''s O(rank) list work, the base-offsets table's allocation --
-- is noise there and a share of the call here. Listed with the regime
-- the view takes, the class spanning them by design. Added 2026-09-03.
mkSmall :: ShapeL -> Strides -> (ShapeL, T)
mkSmall = mkScaled

-- Views combining mechanisms the classes above hold one at a time, as the
-- library composes its operations and no one operation's class builds:
-- a broadcast reversed; a broadcast sliced to a non-zero offset; a zero
-- stride on each side of a non-zero one, which 'canonView' cannot merge,
-- adjacent zeros being the case it does, so the hoisted read and the
-- block copy compose in one fill; and a scalar broadcast to a whole
-- array, every stride 0. Listed with explicit strides and offset, over
-- the tightest backing the view spans from that offset. Added 2026-09-03.
mkCompose :: ShapeL -> Strides -> Int -> (ShapeL, T)
mkCompose sh strides@(Strides ats) ao =
  let top = ao + sum [(s - 1) * t | (s, t) <- zip sh ats, t > 0]
      v = VS.enumFromN (0 :: Double) (top + 1)
  in  (sh, T strides ao v)

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
-- resource (README.md#what-moves-a-figure-when-no-strategy-changed).
--
-- It DOES move the published geomean, which an earlier version of this
-- comment denied: the eleven skew small, and the base-offsets build is a
-- larger share of a small shape, so both the geomean and the ratios between
-- strategies shift past the noise floor -- a change of population, not of
-- any strategy (README.md#the-shape-set).
--
-- Two of the kept eleven are load-bearing beyond their workload and must
-- not be dropped in a later cut. 'gather48-src-50' and 'conv1d-24' are the
-- only CONV shapes whose two innermost listed dims DIFFER -- every other
-- conv shape ends in a square kernel, where @check@'s @sInner@ assertion's
-- two readings coincide and it would pass however it was written -- and the
-- first in run order to exercise it. Several stretch shapes differ too, so
-- the assertion does not go vacuous without these two; what would is the
-- conv set's own coverage of it.
-- Retiring a shape from TIMING keeps this, @check@ reading 'allShapes' --
-- which is how 'conv1d-24' went on 2026-09-04 ('retiredShapes').
convShapes :: [(String, ShapeL)]
convShapes =
  [ -- horde-ad shaped CNN (MnistCnnShaped2; kernel kh+1 = 3)
    ("cnn-L1-6x6-c1",       [6, 6, 1, 3, 3])          -- 324
    -- Two small shapes added 2026-09-02 for Run 24, in the gap between
    -- 324 and 4096 elements and below 288, where the set had nothing: a
    -- per-call dispatch cost is a share of a small call and of nothing
    -- else, and the leaner dispatch's whole constituency is here.
  , ("cnn-L1-12x12-c1",     [12, 12, 1, 3, 3])        -- 1296
  , ("cnn-L1-24x24-c1",     [24, 24, 1, 3, 3])        -- 5184
  , ("cnn-L2-24x24-c32",    [24, 24, 32, 3, 3])       -- 165888
  , ("cnn-slice-c32",       [32, 3, 3])               -- 288  (one position)
    -- MNIST LeNet-5
  , ("lenet-L1-28-c1-k5",   [28, 28, 1, 5, 5])        -- 19600
  , ("lenet-slice-c6-k5",   [6, 5, 5])                -- 150  (one position, k5)
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
shapes = [s | s@(n, _) <- allShapes, n `notElem` retiredShapes]

-- Every main-set shape, timed or retired: what 'check', 'partitioned' and
-- the saturating preamble read.
allShapes :: [(String, ShapeL)]
allShapes = convShapes ++ stretchShapes

-- Main-set shapes retired from TIMING and kept in 'check', ruled 2026-09-04
-- on their canonical forms as the stride classes were ('retiredClasses'
-- below): every main-set view canonicalizes to a rank-3 positive fill with a
-- stride-1 level, or to a regime-1 slice, so what is left to differ in is
-- the two inner extents, their strides and the run count. 'stretch-inner1'
-- is the regime-1 slice, O(1) at any size, which 'small-flat64' times;
-- 'lenet-slice-c6-k5' is 'small-patch-k5' to the stride; 'cnn-L1-6x6-c1',
-- 'stretch-rank10', 'cifar-L2-16-c64-k3' and 'cnn-L1-12x12-c1' are rungs of
-- the [A, 3, 3] ladder at strides [9, 1, 3] beside 'cnn-slice-c32',
-- 'cnn-L1-24x24-c1', 'cnn-L2-24x24-c32' and 'vgg-14-c512-k3', the first two
-- within a tenth in A of a kept rung and the rank-10 odometer merged away;
-- 'conv1d-24' is runs of 3 at stride 24 beside 'gather48-src-50' at 50; and
-- 'stretch-rank12' is runs of 2 at stride 2, its rank merged away, the third
-- of three runs-of-2 shapes and the only small one, which the small class
-- covers. The anchor 'cifar-L2-16-c64-k3' held moved to 'cnn-L2-24x24-c32'
-- with it (read-run.py's ANCHORS, run-alonelegs.sh). The population moved,
-- so a Run 25 geomean re-baselines against Run 24; the fingerprint's per-
-- shape rows and the anchors cross. The entries stay listed so that @check@
-- still holds every arm to the reference on them and older readers parse the
-- lists; a shape is re-timed by deleting its name here
-- (README.md#the-shape-set).
retiredShapes :: [String]
retiredShapes =
  [ "stretch-inner1"
  , "lenet-slice-c6-k5"
  , "cnn-L1-6x6-c1"
  , "cifar-L2-16-c64-k3"
  , "stretch-rank10"
  , "conv1d-24"
  , "stretch-rank12"
  , "cnn-L1-12x12-c1"
  ]

-- Every retired name is a listed shape, asserted in 'main' beside
-- 'partitioned': a misspelt one would retire nothing and say nothing.
retiredShapesKnown :: Bool
retiredShapesKnown = all (`elem` map fst allShapes) retiredShapes

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
    -- The third shape every class took on 2026-08-14, two shapes not
    -- being enough to winsorize, so one disturbed cell owned the class
    -- geomean (README.md#what-is-open). Each is the class's OWN extreme
    -- rather than another size: here the stretch factor taken to the size
    -- cap, a nine-element table read 200000 times, where the two above
    -- stretch by 32 and 89. It is the case where the broadcast IS the
    -- cost and the table build vanishes beside it.
  , ("bcastmid-b200k",   200000, [3, 3])      -- 1800000, stretch at the cap
    -- The fourth shape, added 2026-08-25 with the 'mid-copy' arm: the
    -- BLOCK taken to the cap's scale -- 150000 elements filled once and
    -- copied three times per outer index -- where the three above run
    -- blocks of 216, 97 and 3, so this is the block-copy arm's best case
    -- exactly as 'b200k' above is its worst.
  , ("bcastmid-block150k", 4, [3, 300, 500])  -- 1800000, 150000-elem block
  ]

-- Listed shape is the dense array; the view appends the size-1 dim.
reshape1Shapes :: [(String, ShapeL)]
reshape1Shapes =
  [ ("reshape1-500k", [500000])         -- 500000, the [n] -> [n, 1] trap
  , ("reshape1-r3",   [100, 50, 36])    -- 180000, differing trailing dims
    -- The class's extreme, added 2026-08-14: appending the size-1 dim
    -- makes sInner 1 and so m = l for every shape here, which is one run
    -- per element; this takes that to a rank-11 view over the deepest
    -- odometer the main set carries, where the two above are rank 2
    -- and 4. Per-run overhead against nothing else.
  , ("reshape1-rank10", [3,3,3,3,3,3,3,3,3,3])  -- 59049, deepest odometer
  ]

-- Listed shape is the dense array; the view is its innermost-two
-- transpose with the size-1 dim appended. See 'mkReshape1Strided'.
reshape1StridedShapes :: [(String, ShapeL)]
reshape1StridedShapes =
  [ ("reshape1-strided-r3", [100, 50, 36])  -- 180000, r3's shape, strided
  ]

slicedShapes :: [(String, ShapeL)]
slicedShapes =
  [ ("slice-cnn-L2-24x24-c32", [24, 24, 32, 3, 3])  -- 165888, sliced c32
  , ("slice-primes",           [97, 89, 29])        -- 250357, sliced primes
    -- The class's extreme, added 2026-08-14: this class offsets by 1 in
    -- every dimension of an enclosing array, so what stresses it is
    -- dimensions -- rank 7 with coprime extents, where the two above are
    -- rank 5 and 3 and every extent is small.
  , ("slice-coprime-r7",     [2, 3, 5, 7, 11, 13, 2])  -- 60060, rank 7
  ]

-- Listed as [h, w, kh, kw]: image and kernel, not the view shape.
windowShapes :: [(String, ShapeL)]
windowShapes =
  [ ("window-28x28-k5",   [28, 28, 5, 5])    -- 14400, over 784 elements
  , ("window-224x224-k3", [224, 224, 3, 3])  -- 443556, over 50176
    -- The class's extreme, added 2026-08-14: the kernel sets the two
    -- innermost extents of the view, and both shapes above are square, so
    -- neither can say what a degenerate one costs. This one is 1 by 9 --
    -- innermost extent 1 under the repeated strides an overlapping window
    -- has, which is the run-of-one-element case this class never saw.
    -- Under 'canonView' that kernel row of 1 is dropped and the view is
    -- runs of 9, 'runs-9''s own run, over a backing those runs overlap on;
    -- kept for that overlap, which 'runsShapes' has none of (2026-09-04).
  , ("window-64x64-k1x9", [64, 64, 1, 9])    -- 32256, over 4096
    -- A kernel one past the short bodies of 'fillStage2Short', which
    -- write runs of 2 to 5, added 2026-09-02 for Run 24: both square
    -- shapes above are inside that range, so the class that gave the
    -- short-body arm its widest lead could not say where the lead ends.
    -- The image is sized to keep the view under 'sizeCap'.
  , ("window-128x128-k7", [128, 128, 7, 7])  -- 729316, over 16384
  ]

-- A strided and a dilated window over the k3 image, added 2026-09-03:
-- the four above are stride-1 and undilated, as 'mkWindow' built every
-- window until then, so a strided convolution's patch view -- outer
-- strides twice the row and 2 -- and a dilated kernel's -- taps a row
-- and two elements apart -- had no view. The kernel stays k3 so the
-- short body still fires. Listed as image and kernel beside (stride,
-- dilation), IN A LIST OF THEIR OWN rather than as six-entry rows of
-- 'windowShapes': read-run.py's older revisions, which `defect-run.py
-- --audit` replays against today's Main.hs, unpack that list's rows
-- four ways and die on a longer one, and a day of six-entry rows there
-- turned 25 audits into tracebacks (2026-09-03). A list an old reader
-- does not name it does not read.
windowStridedShapes :: [(String, ShapeL, (Int, Int))]
windowStridedShapes =
  [ ("window-224x224-k3-s2", [224, 224, 3, 3], (2, 1))  -- 110889, stride 2
  , ("window-224x224-k3-d2", [224, 224, 3, 3], (1, 2))  -- 435600, dilated by 2
  ]

-- Views, not shapes like its siblings: explicit strides beside the shape,
-- superincreasing, none 1.
scaledViews :: [(String, ShapeL, Strides)]
scaledViews =
  [ ("scaled-super-r3", [40, 50, 30], Strides [4547, 91, 3])  -- 60000
  , ("scaled-rank1-m1", [300000], Strides [5])  -- 300000, the m == 1 floor
    -- The class's extreme, added 2026-08-14, and the shape this README's
    -- own findings ask for: rank 5 with coprime extents against the rank
    -- 3 and rank 1 above, its superincreasing strides scattering 15015
    -- outputs across 42735 source elements -- read nearly three times its
    -- own size, deepest odometer here, per-run work dominant. That is the
    -- memory-placement corner the wild cell and the mid-bench step both
    -- live in (README.md#what-is-open), and this class had no cell in it.
    -- Strides superincreasing as this list's are and none 1: each exceeds
    -- the span of everything under it (36, 406, 2848, 14244), so no two
    -- runs overlap. Rank stops at 5 because the entry must fit one line
    -- for the reader's parser, and rank 7 needs six-digit strides.
  , ("scaled-r5", [3,5,7,11,13], Strides [14245,2849,407,37,3])  -- 15015
  ]

-- Every stride-class entry beside its built view, in the lists' order --
-- the one list the @classes@ benchmark mode and 'partitioned' both read,
-- so an entry cannot be timed at a size the cap never saw. The views are
-- thunks: nothing here forces a source vector until criterion's @env@
-- builds that group's input, and 'partitioned' forces shapes alone.
--
-- A CLASS NAME CARRIES NO HYPHEN, though a shape name may and most do.
-- The drivers derive a bench's population by cutting its name at the first
-- hyphen, so `bcast-inner8` yields `bcast`, and a class called `bcast-mid`
-- would yield `bcast` too and be run as one population with it -- one
-- process for two, its bench count agreeing, and the second leaving no
-- artifact. The names below already read as though this were known; it was
-- not written down until 2026-08-17, and run-major.sh now refuses a
-- hyphenated name in CLASSES rather than leaving it to be noticed.
-- Regime-2 views: an innermost run of contiguous elements under a padded
-- outer stride, as @slice@ of a wider array, @window@ with a unit kernel
-- row, or any dense array's sub-block produces them -- the one population
-- the library dispatches to a slice-and-concatenate path and not to the
-- regime-3 fill, and the one the stage-two branch moved to the fill. The
-- listed shape is the view shape; the run is everything under the outer
-- dim, the outer stride the run plus one, so the view is regime 2 and
-- never regime 1. Unlike its siblings this class is a sweep and not a
-- triple: its question is a crossover in run length -- one memcpy per
-- run against the fill's stepping loop -- so it walks the run from 2 to
-- 65536 at a fixed size, with one rank-3 entry whose two inner dims are
-- contiguous and merge under 'canonView', so the library's merge and not
-- the listing decides its run.
runsShapes :: [(String, ShapeL)]
runsShapes =
  [ ("runs-2",        [900000, 2])      -- 1800000, runs of 2
  , ("runs-3",        [600000, 3])      -- 1800000, a k3 conv row
  , ("runs-4",        [450000, 4])      -- 1800000, a 2x2 pooling window
  , ("runs-5",        [360000, 5])      -- 1800000, a k5 conv row
    -- One past the short bodies of 'fillStage2Short', which write runs
    -- of 2 to 5, added 2026-09-02 for Run 24: the first length where the
    -- stepping loop with its odd tail takes over from them, and a k7
    -- conv row.
  , ("runs-7",        [257142, 7])      -- 1799994, a k7 conv row
  , ("runs-9",        [200000, 9])      -- 1800000, the window probe's run
  , ("runs-96",       [18750, 96])      -- 1800000, an image row
    -- Two lengths that bracket 'dispRun' within a factor of two, added
    -- 2026-08-30: the class jumped 96 -> 1024 with the crossover inside,
    -- so the threshold was cut to a bracket an order of magnitude wide.
  , ("runs-256",      [7031, 256])      -- 1799936
  , ("runs-512",      [3515, 512])      -- 1799680
  , ("runs-1024",     [1757, 1024])     -- 1799168
    -- Two lengths inside the 64x gap the crossover moved into, added
    -- 2026-09-02 for Run 24: Runs 22 and 23 read stage two ahead of stage
    -- one at 1024 and behind at 65536 on both compilers and both layouts,
    -- so the bracket a threshold is cut to was again an order of
    -- magnitude wide, twice over.
  , ("runs-4096",     [439, 4096])      -- 1798144
  , ("runs-16384",    [109, 16384])     -- 1785856
  , ("runs-65536",    [27, 65536])      -- 1769472, a few long runs
  , ("runs-r3-48x30", [1250, 48, 30])   -- 1800000, merges to runs of 1440
  ]

mkRuns :: ShapeL -> (ShapeL, T)
mkRuns sh@(rows : inner) =
  let run = product inner
      rowStride = run + 1
      v = VS.enumFromN (0 :: Double) (rows * rowStride)
      strides = rowStride : drop 1 (getStridesT inner)
  in  (sh, T (Strides strides) 0 v)
mkRuns sh = error ("mkRuns: rank 2 or more expected: " ++ show sh)

-- Dims to reverse (of the dense array) beside its shape; the last dim is
-- always among them, which the innermost-minus-one condition pins.
flipShapes :: [(String, [Int], ShapeL)]
flipShapes =
  [ ("flip-whole-square", [0, 1], [1341, 1341])       -- 1798281, one run at stride -1
  , ("flip-last-c32",     [4],    [24, 24, 32, 3, 3]) -- 165888, runs of 3, reversed
  , ("flip-last-rows",    [1],    [18750, 96])        -- 1800000, rows of 96, reversed
  ]

-- View shape, enclosing shape and offset; every view extent stays short
-- of the enclosure's, which the canon-rank condition pins.
blockViews :: [(String, ShapeL, ShapeL, Int)]
blockViews =
  [ ("block-run64-gap1",  [2048, 64],   [2048, 65],   0)  -- 131072, one element between rows
  , ("block-run64-gap64", [2048, 64],   [2048, 128],  0)  -- 131072, a row between rows
  , ("block-run64-page",  [2048, 64],   [2048, 512],  0)  -- 131072, rows a page apart
  , ("block-run64-off7",  [2048, 64],   [2048, 128],  7)  -- 131072, at offset 7
  , ("block-r3-vol64",    [64, 64, 64], [72, 72, 72], 0)  -- 262144, rank 3 under canonView
  ]

-- The regime the view takes, its shape and its strides.
smallViews :: [(String, Int, ShapeL, Strides)]
smallViews =
  [ ("small-row96",    2, [4, 96],    Strides [97, 1])     -- 384, rows of 96
  , ("small-patch-k5", 3, [6, 5, 5],  Strides [25, 1, 5])  -- 150, lenet-slice-c6-k5's own view
  , ("small-bcast32",  3, [8, 32],    Strides [1, 0])      -- 256, a broadcast
  , ("small-flat64",   2, [4, 1, 64], Strides [64, 0, 1])  -- 256, collapses to regime 1
  ]

-- Shape, strides and offset; each combines a zero stride with a second
-- mechanism, which the second-mechanism condition pins.
composeViews :: [(String, ShapeL, Strides, Int)]
composeViews =
  [ ("compose-rev-bcast",   [64, 100, 8],   Strides [-100, -1, 0], 6399)  -- 51200, bcast-inner8 reversed
  , ("compose-slice-bcast", [64, 100, 8],   Strides [100, 1, 0],   7)     -- 51200, bcast-inner8 at offset 7: the hoisted read off a base
  , ("compose-zero-mid",    [200, 90, 100], Strides [0, 1, 0],     0)     -- 1800000, zero, one, zero
  , ("compose-scalar",      [1200, 1500],   Strides [0, 0],        0)     -- 1800000, every stride 0
  ]

classViews :: [(String, (ShapeL, T))]
classViews =
  [(n, mkRev s) | (n, s) <- revShapes]
  ++ [(n, mkRevSome rs s) | (n, rs, s) <- revSomeShapes]
  ++ [(n, mkBroadcast s) | (n, s) <- broadcastShapes]
  ++ [(n, mkBroadcastMid b s) | (n, b, s) <- broadcastMidShapes]
  ++ [(n, mkReshape1 s) | (n, s) <- reshape1Shapes]
  ++ [(n, mkReshape1Strided s) | (n, s) <- reshape1StridedShapes]
  ++ [(n, mkSliced s) | (n, s) <- slicedShapes]
  ++ [(n, mkWindow s) | (n, s) <- windowShapes]
  ++ [(n, mkWindow (s ++ [st, d])) | (n, s, (st, d)) <- windowStridedShapes]
  ++ [(n, mkScaled s sts) | (n, s, sts) <- scaledViews]
  ++ [(n, mkRuns s) | (n, s) <- runsShapes]
  ++ [(n, mkFlip rs s) | (n, rs, s) <- flipShapes]
  ++ [(n, mkBlock s e o) | (n, s, e, o) <- blockViews]
  ++ [(n, mkSmall s sts) | (n, _, s, sts) <- smallViews]
  ++ [(n, mkCompose s sts o) | (n, s, sts, o) <- composeViews]

-- Classes retired from TIMING and kept in 'check', by prefix -- ruled
-- 2026-09-04 on the canonical forms the branch's fill sees ('canonView',
-- then 'fillStage2''s dispatch), which is what a timed class has to be
-- distinct in. 'reshape1': three of its four views canonicalize to the
-- regime-1 slice 'stretch-inner1' and 'small-flat64' already time, and the
-- fourth to a main-set view -- which is why it is the class the correction
-- degenerates on. 'revsome': reproduced 'rev' on every run it ran; its
-- inner-reversed view is 'rev''s mechanism and its two outer-reversed ones
-- are main-set views walked in another order, the fill's addressing being
-- sign-agnostic and the sign-sensitive bounds it was built for belonging to
-- the packed Int32 scan, settled. 'slice': a main-set view plus a base
-- offset the fill reads once, the offset timed by 'block-run64-off7' and
-- 'compose-slice-bcast' since. The lists and generators stay: 'check' holds
-- every arm to the reference on these views still, read-run.py's older
-- revisions parse the lists, and a class is re-timed by deleting its name
-- here. run-major.sh's CLASSES omits them, held to `classes --list` by its
-- own cross-check, and read-run.py reads this list for the class counts it
-- holds a run file to (README.md#the-stride-classes-and-what-they-cover).
retiredClasses :: [String]
retiredClasses = ["reshape1", "revsome", "slice"]

-- The class a shape name belongs to: its prefix up to the first hyphen,
-- the derivation every driver uses (run-major.sh says why).
classOf :: String -> String
classOf = takeWhile (/= '-')

-- Every retired name is a class, asserted in 'main' beside 'partitioned':
-- a misspelt one would retire nothing and say nothing.
retiredKnown :: Bool
retiredKnown = all (`elem` map (classOf . fst) classViews) retiredClasses

-- 'classViews' less the retired classes: what the @classes@ mode times.
timedClassViews :: [(String, (ShapeL, T))]
timedClassViews =
  [cv | cv@(n, _) <- classViews, classOf n `notElem` retiredClasses]

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
partitioned = all ((<= sizeCap) . product . snd) allShapes
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
--         For all but 'concat-runs', which predates them, that reason is one
--         of the two rulings of 2026-08-08
--         (README.md#what-the-benchmark-does) -- a size precondition, or 2.4x
--         the result in allocation -- and the entry names the disqualifying
--         fact alone. With the column those preconditions used to occupy gone
--         from README's table, these entries are where they are recorded.
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
--
-- An 'Only' entry takes no slot, so what is actually run is the sublist of
-- the rest, and every such entry still sits where its slot used to be: the
-- placements below are stated for the roster they were chosen in, and a
-- placement reasoned about an arm that is now 'Only' says why the slot is
-- there rather than what it currently measures.
roster :: [(String, Arm)]
roster =
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
    -- Every run since has licensed it, and the correction is applied to
    -- every published figure
    -- (README.md#sum-only-and-the-correction-now-applied). Both halves
    -- stay in the roster, because this is a test every run must repeat:
    -- a run whose halves diverged would invalidate its whole time column,
    -- not merely decline to correct it. What this pair CANNOT test about
    -- itself -- that a fixed vector is read at the same cost as one the fill
    -- has just written -- is what the two 'Force' arms measure.
    --
    -- THIS SLOT IS LOAD-BEARING and was moved here after Run 9, from
    -- below the three distant twins. Timing a sum over a FIXED vector
    -- means allocating that vector once in setup and almost nothing per
    -- call, and that one large allocation grows the block pool and leaves
    -- it grown -- so this bench silently divides the group into a cold
    -- prefix and a warm remainder. With it below the twins, all three were
    -- measured cold against bases measured warm, which is a heap-state
    -- difference where the crossed design intends a POSITION difference,
    -- and on 'vgg-14-c512-k3' it put 'bq-expand-aa-distant' 41% above its
    -- own base for two runs running. Measured, not reasoned: inserting
    -- this bench between the twin and the base is alone enough to move the
    -- base from 4.58 ms to 3.35 ms, where 'mut-odo-vecdims' in the same
    -- slot changes nothing
    -- (README.md#what-moves-a-figure-when-no-strategy-changed).
    --
    -- MOVED AGAIN BEFORE RUN 10, this time above 'list', which leaves
    -- nothing in the group measured on an ungrown pool. Through Run 9 it
    -- sat below the baseline deliberately, the argument being that warming
    -- 'list' moves the denominator of every published ratio and so is a
    -- larger change than the one being made -- true, and the reason it
    -- waited for a run willing to pay it. What made this that run is that
    -- the pool asymmetry had been narrowed to exactly one bench: after the
    -- move above, every timed arm is measured warm EXCEPT the one every
    -- figure divides by, which is also the arm the nursery punishes hardest
    -- (README.md#what-moves-a-figure-when-no-strategy-changed). This is
    -- the warm-up bench the TODO list asks for, spent from the roster
    -- rather than added to it, so the delta stays order-only.
    --
    -- Two consequences to expect rather than to discover. The three
    -- absolute 'list' anchors are built to detect a moved baseline and this
    -- moves it on purpose, so they fire by construction. And unlike the
    -- previous move, this one relocates code: swapping these two entries
    -- shifts every worker by ~40 KB and rerolls every hot loop's alignment,
    -- measured on the two binaries, where the slot-5-to-2 move left all
    -- eight measured loops byte-identical
    -- (README.md#what-is-open). Anything added above
    -- the twins from now on has to be checked for the pool property, and
    -- any reorder at all for this one.
  [ ("sum-only-early",             Term)
  , ("list",                       Base fbList)
    -- The adjacent half of the baseline's own pair, and the one insertion
    -- above the distant twins the slot rule allows -- measured rather than
    -- argued, on the -L1 pass of the day it landed: it allocates 134261336
    -- B a call against 'list''s 134261403, agreeing to 1.1e-4 over all 24
    -- shapes, where 'sum-only-early', the bench that rule is about,
    -- allocates 204 B a call because its allocation is a one-off setup
    -- vector. So it fills as its base does and grows no pool the way that
    -- bench does. It moves every later slot by one, which the roster delta
    -- records. Added 2026-08-14, first read in Run 14.
  , ("list-aa-adjacent",           Twin fbList)
    -- The distant halves of the crossed A/A pairs, none a strategy: each
    -- runs an existing function twice, so its true ratio is known to be
    -- exactly 1 and what it measures is what two identical things differ
    -- by -- a margin narrower than they are is not a result. Each twinned
    -- strategy is duplicated once here and once beside its base, so
    -- position varies within a strategy and strategy within a position,
    -- which is the design that settled the position question
    -- (README.md#what-moves-a-figure-when-no-strategy-changed). Nine
    -- strategies were twinned at Run 14, the scan band's pair the oldest,
    -- its distant half once in the slot above these; 'offtab''s twins
    -- went with its parking
    -- on 2026-08-28 and five more pairs with the prune of 2026-09-04
    -- (README.md#what-the-benchmark-does), a twin of an untimed arm
    -- pricing nothing, and the slots below stayed where they were.
  , ("bq-expand-aa-distant",       Twin fbBQexpand)
  , ("mut-odo-vecdims-aa-distant", Twin fbMutOdoVecdims)
  , ("list-aa-distant",            Twin fbList)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("gen-quotrem",                Only fbGenQuotRem)
    -- Parked 'Only' 2026-09-04 by the prune, with fifteen more below
    -- marked the same way: the roster is cut to the one question left,
    -- how the mut-odo-vecdims family is used in the library
    -- (README.md#what-the-benchmark-does). An arm parked so stays
    -- checked; its A/A twins and its 'Force' arm are deleted, a control
    -- of an untimed arm pricing nothing; and its column in a run's own
    -- geomean table stays blank from Run 25 on.
  , ("gen-unsafe",                 Only fbGenUnsafe)
    -- not timed: 27.94x the result
  , ("unfold-add",                 Only fbUnfoldAdd)
    -- not timed: 5.19x the result
  , ("fused",                      Only fbFused)
    -- not timed: 5.19x the result
  , ("offsets-quot",               Only fbBaseOffsetsQuot)
    -- not timed: 11.89x the result
  , ("backperm",                   Only fbBackperm)
    -- 'fbConcatRuns' is deliberately NOT benchmarked, though @check@ still
    -- holds it to the reference. It is by a clear margin the noisiest
    -- bench of the set and the one with the most extreme footprint, so it
    -- is the likeliest to leave an aftermath in the slots after it -- and
    -- it is refuted on its own numbers anyway, so timing it buys nothing
    -- to set against that risk. What was probed about the aftermath, and
    -- what stays unprobed, is at README.md#what-the-benchmark-does. It
    -- keeps a roster entry, and with it an agreement check, but takes no
    -- slot in the run; the entry sits where the slot used to be.
  , ("concat-runs",                Only fbConcatRuns)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("mut-odo",                    Only fbMutOdo)
  , ("mut-odo-vecdims",            Fill fbMutOdoVecdims)
    -- The second of the two 'Force' pairs, on the fastest strategy measured
    -- and so the one where the forcing term is the largest share of the
    -- bench. If the term is biased at all, this is the arm the bias
    -- distorts most, and one pair on its own could not tell a biased term
    -- from a size-dependent one -- two pairs an octave apart in speed can.
  , ("mut-odo-vecdims-nosum",      Force fbMutOdoVecdims)
    -- The fast-end control, on the fastest strategy measured, where a
    -- Failed Run 6 prediction had the noise floor tracking 1/time rather
    -- than GC pressure -- the noisier of its two pairs being the one
    -- allocating LESS. The runs since split that prediction: per-cell
    -- scatter does track 1/time, but it CANCELS, where the distant pairs
    -- carry span-ordered biases that do not
    -- (README.md#what-moves-a-figure-when-no-strategy-changed).
    -- So keep this arm for the
    -- scatter it measures, and read the floor off the pairs that are
    -- biased, not the one that is merely noisy.
  , ("mut-odo-vecdims-aa",         Twin fbMutOdoVecdims)
    -- The FastReshape decomposition, four arms after their shared control
    -- above (README.md#the-mutable-ceiling-taken): solo input axis,
    -- solo output axis, the corner, the loop form on the corner. A block
    -- after the control's own pair, so no existing control moves.
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("mut-odo-vecdims-add-in",     Only fbMutOdoVecdimsAddIn)
    -- not timed since 2026-08-25: the decomposition is priced and
    -- spent -- the solo output axis convicted at ~16%, the corner
    -- sub-additive over it, the down form recovering the corner's loss
    -- to a tie with the shared control -- and the decision ships
    -- vecdims alone, the redirect dropped
    -- (README.md#the-two-stage-plan-and-the-rework-proposal).
  , ("mut-odo-vecdims-add-out",    Only fbMutOdoVecdimsAddOut)
  , ("mut-odo-vecdims-add-both",   Only fbMutOdoVecdimsAddBoth)
  , ("mut-odo-vecdims-add-both-down", Only fbMutOdoVecdimsAddBothDown)
    -- The Run 20 extension of the FastReshape block, added 2026-08-24,
    -- first read in Run 20: the leaf call fused into the innermost outer
    -- level, solo, crossed with the count-down fill, and crowned with
    -- the unrolled fill, over the controls each varies
    -- (README.md#the-mutable-ceiling-taken).
    -- The count-down fill's own solo arms sit here as 'Only', refuted by
    -- codegen the day they were written, reasons at their definitions.
    -- Appended to the family block for the block's own reason -- after
    -- the control's pair, so no existing control moves -- at the price
    -- that every slot below moves by three against Runs 9 to 19, which
    -- any cross-run read of those slots has to carry.
    -- not timed: the down fill reloads per element at the go leaf, see
    -- its definition
  , ("mut-odo-vecdims-down",       Only fbMutOdoVecdimsDown)
    -- not timed: the same reloads, see its definition
  , ("mut-odo-vecdims-add-in-down", Only fbMutOdoVecdimsAddInDown)
    -- Parked 'Only' 2026-09-02, after Run 23 read the ordering on both
    -- halves: the shipped `-u2` leaf leads this one on every population
    -- and its count-down twin in all twenty, so neither is an alternative
    -- any more, and their slots went to Run 24's additions. Timed again
    -- 2026-09-04 for Run 25 alone, as the bound control of the `-u1` arm
    -- below (README.md#what-is-open, the Run 25 entry); parked again
    -- after it.
  , ("mut-odo-vecdims-add-in-leaf", Fill fbMutOdoVecdimsAddInLeaf)
  , ("mut-odo-vecdims-add-in-leaf-down", Only fbMutOdoVecdimsAddInLeafDown)
  , ("mut-odo-vecdims-add-in-leaf-u2", Fill fbMutOdoVecdimsAddInLeafU2)
    -- Timed since 2026-08-28, parked 'Only' the day before: the
    -- lighter-loop form of the shipped arm, see its definition.
  , ("mut-odo-vecdims-add-in-leaf-u2-down", Fill fbMutOdoVecdimsAddInLeafU2Down)
    -- The un-unrolled form of the shipped fill, added 2026-09-04 for Run
    -- 25 and placed beside its parents, every slot below moving by one;
    -- reasons at its definition.
  , ("mut-odo-vecdims-add-in-leaf-u1", Fill fbMutOdoVecdimsAddInLeafU1)
    -- The rework-proposal block, added 2026-08-25, first read in Run 20
    -- (README.md#the-two-stage-plan-and-the-rework-proposal): the
    -- canonicalizing composite, its memcpy-run form, the two
    -- zero-stride conditions solo, and the full endpoint, each one
    -- change over 'mut-odo-vecdims' or over the previous member,
    -- reasons at the definitions. Appended after the family for the
    -- family block's own reason -- no existing control moves -- taking
    -- six slots where the three demotions above return three, so
    -- every slot below moves by three more than the block above already
    -- carries.
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("canon-vecdims",              Only fbCanonVecdims)
    -- Parked 'Only' 2026-09-02: refused at Run 20, behind the arm it
    -- varies on `window`
    -- (README.md#the-two-stage-plan-and-the-rework-proposal), and timed
    -- for three runs since without a question left.
  , ("canon-memcpy-r2",            Only fbCanonMemcpyR2)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("bcast-set",                  Only fbBcastSet)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("mid-copy",                   Only fbMidCopy)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does);
    -- its 'Force' arm, the fourth in-situ forcing control and the one
    -- whose write pattern varied across the main set, went with it
    -- (README.md#sum-only-and-the-correction-now-applied)
  , ("canon-full",                 Only fbCanonFull)
    -- The library-shaped block, added 2026-08-28: what a user's
    -- toVectorT costs under stage one, under stage two, and under stage
    -- two with contiguous runs routed to slices -- each a port of the
    -- library code, reasons at the definitions. Appended for the
    -- family block's own reason -- no existing control moves -- at
    -- three slots.
  , ("lib-stage1",                 Fill fbLibStage1)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does):
    -- the two halves that bracketed 'dispRun', spent once the arm below
    -- carried its cut
  , ("lib-stage2",                 Only fbLibStage2)
  , ("lib-stage2-concat",          Only fbLibStage2Concat)
    -- The dispatch arm the runs class's crossover asks for, added
    -- 2026-08-30: one change over the entry above, and placed beside it
    -- so the two are read as neighbours -- at the price that every slot
    -- below moves by one against Run 21, which any cross-run read of those
    -- slots has to carry.
    -- Re-cut to 2048 on 2026-09-02 by the probe below, the cut at 256
    -- having been killed by Run 22 on both compilers and by Run 23 on
    -- both layouts; timed by Run 24 at the new cut, reasons at 'dispRun'.
  , ("lib-stage2-disp",            Fill fbLibStage2Disp)
    -- One arm per candidate threshold, added 2026-09-02 for the
    -- one-binary runs-class probe README's task 9 registers: the same
    -- dispatch with its threshold an argument ('libStage2DispAt', named
    -- per threshold beside it), cut at the three lengths between
    -- `runs-1024`, where Runs 22 and 23 read stage two ahead, and
    -- `runs-65536`, where they read it behind, and timed beside the
    -- entry above at 256 as their control. The probe ran the same day
    -- (probe-disp2-runs.json) and picked 2048, which the entry above now
    -- carries; the three are parked 'Only', spent, and stay checked.
  , ("lib-stage2-disp-2048",       Only fbLibStage2Disp2048)
  , ("lib-stage2-disp-8192",       Only fbLibStage2Disp8192)
  , ("lib-stage2-disp-32768",      Only fbLibStage2Disp32768)
    -- Three candidates for the branch, added 2026-08-30 for Run 22: the
    -- run unrolled by four, a run of 2 to 5 elements written by a body
    -- of exactly that length, and the same fill under a leaner dispatch,
    -- each one change over 'lib-stage2'. Placed beside their control as
    -- the entry above is, and moving every slot below by three more;
    -- reasons at the definitions.
    -- Parked 'Only' 2026-09-02: ruled out for the library at its
    -- definition, and Run 23's dead-spot half read it behind its control
    -- on `runs`, the one class it had a lead in.
  , ("lib-stage2-u4",              Only fbLibStage2U4)
    -- Parked 'Only' 2026-09-04: ruled out for the library at
    -- 'fillStage2Short''s definition, the short bodies too repetitive and
    -- so too complex, as the quad loop was; its Run 24 readings stand.
  , ("lib-stage2-short",           Only fbLibStage2Short)
  , ("lib-stage2-lean",            Fill fbLibStage2Lean)
    -- The list consumer under each stage, added the same day: the
    -- library's toVectorListT and one concatenation, so the pair prices
    -- the list's construction alone, reasons at the definitions.
  , ("liblist-stage1",             Fill fbLibListStage1)
  , ("liblist-stage2",             Fill fbLibListStage2)
    -- The unordered entry point under each stage, added 2026-08-30 with
    -- the fill candidates and for the same run: one-block test in front
    -- of the liblist body, reasons at the definitions. Every slot below
    -- moves by two more, six in all against Run 21.
  , ("libunord-stage1",            Fill fbLibUnordStage1)
  , ("libunord-stage2",            Fill fbLibUnordStage2)
    -- The entry point's candidate, added 2026-09-05 for Run 26: the
    -- one-block test generalized into a fill in address order, reasons
    -- at the definition. Every slot below moves by one.
  , ("libunord-stage3",            Fill fbLibUnordStage3)
    -- not timed: 6.20x the result
  , ("mut-offsets",                Only fbMutBaseOffsets)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("build",                      Only fbBuild)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-mut",                     Only fbBQmut)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-mut-runs",                Only fbBQmutRuns)
    -- not timed: l < 2^32
  , ("bq-mut-runs-mulback",        Only fbBQmutRunsMulback)
    -- not timed: l < 2^32
  , ("mut-flat",                   Only fbMutFlat)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does);
    -- its 'Force' arm, gate 3's third shape of fill, went with it, so the
    -- gate reads two shapes from Run 25 on
    -- (README.md#sum-only-and-the-correction-now-applied)
  , ("mut-flat-gm",                Only fbMutFlatGm)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("bq-mut-runs-gm-mulback",     Only fbBQmutRunsGmMulback)
    -- not timed: l < 2^32
  , ("bq-mut-lemire-out",          Only fbBQmutLemireOut)
    -- not timed: l < 2^32
  , ("bq-mut-lemire-mulback",      Only fbBQmutLemireMulback)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on,
    -- and its two A/A twins, added 2026-08-14 and read from Run 14 to Run
    -- 20, are gone
    -- with it -- a twin of an untimed arm prices nothing.
  , ("offtab",                     Only fbOffTab)
    -- not timed: 'int32Fits' on the source, i.e. at most 2^31 elements
  , ("offtab32",                   Only fbOffTab32)
    -- not timed: m < 2^32, its builder's
  , ("offtab-scan",                Only fbOffTabScan)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("offtab-scan-rem",            Only fbOffTabScanRem)
    -- not timed: 8.27x the result
  , ("bq-unfold",                  Only fbBQunfold)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-gen",                     Only fbBQgen)
    -- The Lemire arms are placed to straddle their controls: this one
    -- runs just after 'bq-gen', and the output-substitution arms run
    -- ahead of 'bq-expand'. A group's later slots are the warmer ones,
    -- so any position bias flatters one side and penalises the other,
    -- and cannot manufacture a verdict that agrees across both. All three
    -- are 'Only' since the precondition ruling, so the straddle is inert
    -- and this is the record of where they go if it is ever reopened.
    -- not timed: m < 2^32, its builder's
  , ("bq-gen-lemire",              Only fbBQgenLemire)
    -- not timed: l < 2^32
  , ("bq-expand-lemire-out",       Only fbBQexpandLemireOut)
    -- not timed: l < 2^32
  , ("bq-expand-lemire-mulback",   Only fbBQexpandLemireMulback)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("bq-expand-gm-mulback",       Only fbBQexpandGmMulback)
    -- not timed: l < 2^32, and 'int32Fits' on the source
  , ("bq-expand32-lemire-mulback", Only fbBQexpand32LemireMulback)
    -- not timed: l < 2^32
  , ("bq-scan-mulback",            Only fbBQscanMulback)
    -- not timed: l < 2^32
  , ("bq-scan-rem-mulback",        Only fbBQscanRemMulback)
    -- not timed: m < 2^32, its builder's
  , ("bq-scan-gm-mulback",         Only fbBQscanGmMulback)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("bq-scan-rem-gm-mulback",     Only fbBQscanRemGmMulback)
    -- not timed: l < 2^32
  , ("bq-odo-mulback",             Only fbBQodoMulback)
    -- parked 2026-09-04 by the prune (README.md#what-the-benchmark-does)
  , ("bq-odo-gm-mulback",          Only fbBQodoGmMulback)
    -- not timed: l < 2^32, plus its builder's m <= 2^31 and every offset
    -- in [0, 2^32)
  , ("bq-scan-packed-mulback",     Only fbBQscanPackedMulback)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-expand-qr-prim",          Only fbBQexpandQRprim)
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
    -- The pair's own verdict -- that the two arms bracket 1 rather than
    -- sitting on one side of it, which a warmer fixed-vector read would
    -- have produced -- is at
    -- README.md#sum-only-and-the-correction-now-applied.
  , ("bq-expand-nosum",            Force fbBQexpand)
  , ("bq-expand-aa-adjacent",      Twin fbBQexpand)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-expand-zf",               Only fbBQexpandZF)
    -- parked 2026-08-28, permanently, by decision (README.md#what-is-open,
    -- the Run 21 entry): superseded, answering no registered question;
    -- its column in a run's own geomean table stays blank from Run 21 on
  , ("bq-expand-b",                Only fbBQexpandB)
    -- not timed: 10.73x the result
  , ("cm-gather",                  Only fbCMGather)
    -- not timed: 8.21x the result
  , ("all-expand",                 Only fbAllExpand)
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
    -- 'gen-unsafe-aa-distant' sat here from Run 14 to Run 24, the one
    -- distant twin placed late so that early-distant could be read
    -- against late-distant; deleted 2026-09-04 with its arm's parking.
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
-- @check@ then failed at the first shape, naming @bq-expand-b@. Proved again
-- for the 'Only' half, which is the half a passing run cannot show and which
-- the roster now leans on for a majority of its strategies: the same
-- shortening of 'fbBQodoMulback' fails at the first shape naming
-- @bq-odo-mulback@, an arm nothing times.
-- The one deliberate weakening of the agreement: the 'libunord' arms
-- port 'toUnorderedVectorListT', whose contract is the right elements in
-- ANY order -- on a one-block view they return the source block in
-- memory order -- so holding them to the reference elementwise fails
-- the arm for keeping its own contract. They are held to it as a
-- MULTISET instead, by sorted equality, which still fails on a wrong
-- result: shortening stage two's one-block slice by one element fails
-- @check@ at the first shape naming @libunord-stage2@ (non-vacuity,
-- 2026-08-30, the same breakage the elementwise chain was proven by).
-- Every other arm stays elementwise, and an unordered arm that agrees
-- elementwise skips the sorts.
agreesWithRef :: VS.Vector Double -> String -> VS.Vector Double -> Bool
agreesWithRef rList n u
  | u == rList = True
  | "libunord-" `isPrefixOf` n =
      sort (VS.toList u) == sort (VS.toList rList)
  | otherwise = False

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
-- to read them: the Results table in the run's own file under runs/,
-- and README.md#the-reader-read-runpy.
-- The saturating preamble, off unless SATURATE is set in the environment
-- to a dose multiplier -- 1 is the saturating dose, 2 the plateau control,
-- 0 and unset are off -- and what it is for is Run 18's entry in README's
-- open list: the block-level state a process benchmarks in is made an
-- input every process asserts, instead of a by-product of its slot, its
-- selection and its time budget. Before criterion sees the roster it
-- installs the state, performs a major collection, and then reads a
-- list-shaped victim at a fixed iteration count beside the heap peak, as
-- ONE LINE on stderr, `@@saturate ...`, which is what a run script asserts
-- the plateau on. Two doses, SATURATE_BY selecting: `list`, the default,
-- is dose x 1M iterations of cnn-slice-c32/list's own fill -- the roster's
-- first sprayer, each iteration a 288-cell cons list and a 2304 B pinned
-- result, both formation routes at once, about six seconds a dose -- and
-- it reproduces the roster's state on the victim (measured 2026-08-22,
-- quiet machine: the roster cell's +12-13%, where the pure burst installs
-- +9-10%); `spray` is the reproducer's pure pinned burst, dose x 4000 x
-- 288 short-lived buffers of 2304 B, a quarter of a second a dose, kept as
-- the control that separates the burst route from the rest. Counted
-- rather than timed, so a dose does not depend on the machine. The
-- environment is read here, in main's own call, never at import time. The
-- check, diag and --list modes skip it: they time nothing.
saturate :: IO ()
saturate = do
  set <- lookupEnv "SATURATE"
  by <- lookupEnv "SATURATE_BY"
  let dose = maybe 0 read set :: Int
      bySpray = by == Just "spray"
  unless (dose <= 0) $ do
    let view name = maybe (error ("saturate: no shape " ++ name)) mkStrided
                      (lookup name allShapes)
        (svsh, sa) = view sprayerShape
        (vsh, a) = view victimShape
    _ <- evaluate (force ((svsh, sa), (vsh, a)))
    t0 <- getMonotonicTime
    (sprayed, keep) <- if bySpray then spray (dose * 4000) 0 0
                       else viaList svsh sa (dose * 1000000) 0 0
    t1 <- getMonotonicTime
    performGC
    t2 <- getMonotonicTime
    s <- victim vsh a victimIters 0
    t3 <- getMonotonicTime
    st <- getRTSStats
    hPutStrLn stderr $
      "@@saturate dose=" ++ show dose ++ "x by="
      ++ (if bySpray then "spray" else "list")
      ++ " sprayed=" ++ show sprayed ++ " in " ++ show (t1 - t0)
      ++ " s; victim " ++ victimShape ++ "/list "
      ++ show ((t3 - t2) / fromIntegral victimIters * 1000)
      ++ " ms/iter over " ++ show victimIters ++ "; inuse="
      ++ show (max_mem_in_use_bytes st) ++ " keep=" ++ show (keep + s)
  where
    sprayerShape = "cnn-slice-c32"
    victimShape = "vgg-14-c512-k3"
    victimIters = 20 :: Int
    -- The roster's sprayer: the fill every list arm runs, on the smallest
    -- shape's view, the sum read back keeping each result from being
    -- dropped unbuilt.
    viaList :: ShapeL -> T -> Int -> Int -> Double -> IO (Int, Double)
    viaList _ _ 0 !n !acc = return (n, acc)
    viaList vsh a k !n !acc = do
      x <- evaluate (VS.sum (fbList vsh a))
      viaList vsh a (k - 1) (n + 1) (acc + x)
    -- The pure burst: one step is 288 buffers, as in the reproducer; the
    -- element read back from each keeps the allocation from being elided.
    spray :: Int -> Int -> Double -> IO (Int, Double)
    spray 0 !n !acc = return (n, acc)
    spray k !n !acc = do
      acc' <- burst (288 :: Int) acc
      spray (k - 1) (n + 288) acc'
    burst :: Int -> Double -> IO Double
    burst 0 !acc = return acc
    burst i !acc = do
      v <- VSM.replicate 288 (fromIntegral i :: Double)
      x <- VSM.unsafeRead v 287
      burst (i - 1) (acc + x)
    victim :: ShapeL -> T -> Int -> Double -> IO Double
    victim _ _ 0 !acc = return acc
    victim vsh a i !acc = do
      x <- evaluate (VS.sum (fbList vsh a))
      victim vsh a (i - 1) (acc + x)
{-# NOINLINE saturate #-}

main :: IO ()
main = assert (partitioned && retiredKnown && retiredShapesKnown) $ do
  args <- getArgs
  unless (any (`elem` ["check", "diag", "--list", "-l"]) args) saturate
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
-- actually held. The heap pair is the one micro.cabal's -M8G comment
-- rests on, and all of it comes from the -T stats that flag already asks
-- for, so nothing here needs a flag from the invoker. It goes to stderr,
-- leaving @--list@ and criterion's own stdout machine-readable, and it
-- reports the roster rather than what a filtered run selected.
--
-- The count is the roster's timed arms, not the 'Benchmark' nodes
-- 'benchView' built. Those are one per timed arm per GROUP, so counting
-- them reported their product, in a line whose whole purpose is to be
-- quoted. Reading the roster is not the weaker
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

-- The wild-cell instrument, off unless WILDLOG is set in the environment,
-- and what it is for is [the mechanism entry] in README's open list: the RTS
-- cumulative allocated-bytes total, with the GC and mutator clocks beside
-- it, ONE LINE PER CRITERION SAMPLE. The granularity is the entry's own ask
-- and not a choice here -- both instances this hunts are a state a process
-- ENTERS and then keeps, so a per-bench figure averages the two states it
-- exists to separate.
--
-- It costs the measurement nothing, which is why it hangs here rather than
-- inside the loop. 'Criterion.Measurement.runBenchmarkable' calls 'allocEnv'
-- before it hands the loop to the timing block and 'cleanEnv' after that
-- block returns, so both lines are written outside the clock; and
-- 'runRepeatedly' below is criterion's own 'whnf'', the NOINLINE loop that
-- 'whnf' itself installs -- @whnf f x = toBenchmarkable (whnf' f x)@ -- so a
-- logged arm runs the instructions every published bench runs, and
-- everything this Benchmarkable adds is outside the timing.
--
-- The environment is read per sample rather than once at load: a top-level
-- read would be an import-time environment parse, which defect-lint.py
-- refuses as a defect family, and 'lookupEnv' walks the environment block
-- without a syscall, outside the clock, once per sample.
--
-- ADDRESSES ARE DELIBERATELY NOT LOGGED, though the mechanism entry names
-- them beside the allocation total. The RTS reserves its heap at a fixed
-- base, so the payload addresses repeat across processes -- the same three
-- in eight of eight, which is what refuted the data-placement hypothesis --
-- and what moves WITHIN that arena is a function of how much has been
-- allocated before a buffer, which is the total logged here. Taking an
-- output buffer's address would cost an extra fill per sample, perturbing
-- the very history under test.
wildLog :: String -> String -> Int64 -> IO ()
wildLog nm phase n = do
  on <- lookupEnv "WILDLOG"
  case on of
    Nothing -> return ()
    Just _  -> do
      s <- getRTSStats
      (load1, runq, busy) <- machineLoad
      hPutStrLn stderr $
        "@@wild " ++ nm ++ " " ++ phase ++ " iters=" ++ show n
        ++ " alloc=" ++ show (allocated_bytes s)
        ++ " mut=" ++ show (mutator_elapsed_ns s)
        ++ " gc=" ++ show (gc_elapsed_ns s)
        ++ " gcs=" ++ show (gcs s) ++ "/" ++ show (major_gcs s)
        ++ " inuse=" ++ show (max_mem_in_use_bytes s)
        ++ " load=" ++ load1
        ++ " run=" ++ runq
        ++ " cpu=" ++ show busy

-- The three load fields the line above ends with, decided 2026-08-22 for Run
-- 18 and read in the same hooks, outside the timed block. THE REASON IS THE
-- WILD CELL: from inside a process its signature -- a non-reproducing mutator
-- step at flat RTS totals -- is exactly an external intrusion's, and Run 16's
-- updater cell was told apart only by a wall-clock window. `cpu` is what
-- separates them, being machine-wide rather than this process's: differenced
-- between consecutive stamps and less the process's own mutator-plus-collector
-- delta, what is left is the CPU something ELSE consumed during that sample,
-- which is the updater class, and none of it is the machine's own. That
-- subtraction is `./read-run.py --wild`'s, and `load` and `run` are printed
-- beside it rather than subtracted.
--
-- `load` ALONE WOULD NOT DO IT, which is why the other two ride with it: the
-- 1-minute average is damped over 60 s and updated every 5 s, so it dates a
-- multi-minute intruder and barely marks a ten-second one. `run` is the
-- instantaneous runnable-task count off the same line, and is the field that
-- marks a short one.
--
-- Not defended against a missing /proc: this harness is Linux-only, both
-- files are virtual and neither can short-read, so a failure here is a
-- machine that could not have run the benchmark either.
machineLoad :: IO (String, String, Integer)
machineLoad = do
  la <- words <$> procLine "/proc/loadavg"
  st <- words <$> procLine "/proc/stat"
  let -- `1min 5min 15min runnable/total lastpid`
      load1 = case la of
        (x : _) -> x
        _       -> "?"
      runq = case la of
        (_ : _ : _ : r : _) -> takeWhile (/= '/') r
        _                   -> "?"
      -- `cpu user nice system idle iowait irq softirq steal guest ...`, in
      -- USER_HZ and not in CONFIG_HZ -- the kernel fixes the unit of this
      -- file at 100 Hz whatever it ticks at, which is what lets the reader
      -- turn a jiffy into 10 ms without asking the machine. Busy is every
      -- field but idle and iowait, the two a benchmark does not compete with.
      busy = sum [ j | (i, j) <- zip [0 :: Int ..] (map read (drop 1 st))
                     , i /= 3, i /= 4 ]
  return (load1, runq, busy)

-- One line, and the handle closed with it: a per-sample 'readFile' would
-- leave a lazy handle open per sample, thousands of them per process.
procLine :: FilePath -> IO String
procLine p = withFile p ReadMode hGetLine

-- 'whnf' with 'wildLog' on either side of the timed block, and differing
-- from it in nothing else: criterion's own is
-- @Benchmarkable noop (const noop) (const (whnf' f x)) False@.
whnfLogged :: String -> (a -> b) -> a -> Benchmarkable
whnfLogged nm f x =
  Benchmarkable (wildLog nm "pre") (\n () -> wildLog nm "post" n)
                (\() n -> whnf' f x n) False

benchView :: String -> (ShapeL, T) -> Benchmark
benchView name view =
  env (evaluate (force view)) $ \ ~(sh, a) ->
    bgroup name (concatMap (arm sh a) roster)
  where
    arm sh a (n, Base f)  = [bench n $ lg n (VS.sum . f sh) a]
    arm sh a (n, Fill f)  = [bench n $ lg n (VS.sum . f sh) a]
    arm sh a (n, Twin f)  = [bench n $ lg n (VS.sum . f sh) a]
    arm sh a (n, Term)    = [env (evaluate (force (reference sh a))) $
                               bench n . lg n VS.sum]
    arm sh a (n, Force f) = [bench n $ lg n (touchLast . f sh) a]
    arm _  _ (_, Only _)  = []
    -- The log line carries GROUP/ARM, the group being the shape, since a
    -- bench name alone leaves a reader counting benches to place a step.
    lg n = whnfLogged (name ++ "/" ++ n)

mkBench :: (String, ShapeL) -> Benchmark
mkBench (name, normalSh) = benchView name (mkStrided normalSh)

-- The stride-class populations as benchmarks, one 'bgroup' per
-- 'timedClassViews' entry in that list's order -- reachable only through the
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
classBenches = [benchView n view | (n, view) <- timedClassViews]

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
oneView = oneViewReg 3

-- 'oneView' with the regime the class owes made explicit: 3 for every
-- class but @runs@, whose views are regime 2 by definition.
oneViewReg :: Int -> String -> ShapeL -> T -> [(String, Bool)] -> IO ()
oneViewReg expReg name sh a@(T (Strides ats) ao v) conds = do
  let rList  = reference sh a
      builds = buildersMatch ao (init sh) (Strides (init ats))
      bad    = [n | (n, f) <- checkedArms,
                    not (agreesWithRef rList n (f sh a))]
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
  unless (agree && builds && reg == expReg && null failedConds) $
    error ("CHECK FAILED: " ++ name
           ++ (if reg == expReg then "" else ", regime " ++ show reg
               ++ " where the class owes " ++ show expReg)
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
  mapM_ one (allShapes ++ degenerateShapes)
  mapM_ oneRev revShapes
  mapM_ oneRevSome revSomeShapes
  mapM_ oneBroadcast broadcastShapes
  mapM_ oneBroadcastMid broadcastMidShapes
  mapM_ oneReshape1 reshape1Shapes
  mapM_ oneReshape1Strided reshape1StridedShapes
  -- One hand-built view, checked and never benched: the regime-1 return
  -- with a NONZERO offset, which no generator reaches -- 'mkReshape1'
  -- and 'stretch-inner1' both canonicalize to natural strides at offset
  -- 0, so the canonicalizing arms' O(1)-slice branch had never met the
  -- offset a slice-then-reshape view hands it.
  -- Non-vacuity, 2026-08-25: dropping the offset from 'fbCanonVecdims''s
  -- slice return fails this view alone, every generator's offset being 0
  -- on that branch.
  -- The view is a standing gate rather than a one-off -- 'checkedArms'
  -- derives from the roster, so every future arm meets it for free --
  -- and when the rework lands upstream the same case belongs in
  -- orthotope's own test suite, the shipped slice branch carrying the
  -- identical hazard. Never to be benched: timing it would measure
  -- dispatch, the degeneracy 'reshape1-strided-r3' exists to keep out
  -- of the class's timings.
  oneView "reshape1-slice-off7" [50, 1]
          (T (Strides [1, 0]) 7 (VS.enumFromN 0 100))
          [ ("canon-natural-at-offset",
             case canonView [50, 1] [1, 0] of
               (csh, cats) -> cats == drop 1 (getStridesT csh)) ]
  mapM_ oneSliced slicedShapes
  mapM_ oneWindow windowShapes
  mapM_ (\(n, s, (st, d)) -> oneWindow (n, s ++ [st, d])) windowStridedShapes
  mapM_ oneScaled scaledViews
  mapM_ oneRuns runsShapes
  mapM_ oneFlip flipShapes
  mapM_ oneBlock blockViews
  mapM_ oneSmall smallViews
  mapM_ oneCompose composeViews
  where
    one (name, normalSh) = do
      let (sh, a@(T (Strides ats) ao _)) = mkStrided normalSh
          rList   = reference sh a
          -- The builders' direct comparison lives in 'buildersMatch', whose
          -- comment carries the reason and the per-conjunct non-vacuity.
          builds  = buildersMatch ao (init sh) (Strides (init ats))
          bad     = [n | (n, f) <- checkedArms,
                         not (agreesWithRef rList n (f sh a))]
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
    -- The sibling's negation, and that is the point of it: same stride-0
    -- innermost dim, and strided once canonicalized, so neither a slice
    -- nor a run memcpy can serve it and the canon arms measure filling
    -- here rather than dispatch. The condition asks 'canonView' itself
    -- for that property -- the property the shape exists for -- rather
    -- than a proxy over the raw strides.
    --
    -- Non-vacuity: swapping 'mkStrided' for 'mkReshape1''s dense source
    -- fails canon-strided alone -- which is exactly the degeneracy this
    -- shape was added against, so the check fires on the thing it exists
    -- to exclude. Proven over the 'canonView' form, 2026-08-25.
    oneReshape1Strided (name, normalSh) =
      let (sh, a@(T (Strides ats) _ _)) = mkReshape1Strided normalSh
      in  oneView name sh a
            [ ("stride0-inner", last ats == 0)
            , ("canon-strided",
               case canonView sh ats of
                 (csh, cats) -> cats /= drop 1 (getStridesT csh)
                                && last cats `notElem` [0, 1]) ]
    -- Non-vacuity: slicing at the origin fails offset-positive alone;
    -- zeroing the margins as well fails both conditions, the view then
    -- being 'mkStrided''s own.
    oneSliced (name, normalSh) =
      let (sh, a@(T _ ao v)) = mkSliced normalSh
      in  oneView name sh a
            [ ("offset-positive",   ao > 0)
            , ("backing-enclosing", VS.length v
                                    == product (map (+ 2) normalSh)) ]
    -- Non-vacuity: an innermost stride of 2 in place of the row multiple
    -- (still in-bounds) fails row-multiples alone; shrinking the view to a
    -- single patch fails aliasing alone. The condition was dup-stride,
    -- outer equal to innermost, until the strided and dilated windows of
    -- 2026-09-03, whose two are @s * w@ and @d * w@.
    oneWindow (name, hwkk) =
      let (sh, a@(T (Strides ats) _ v)) = mkWindow hwkk
          w = hwkk !! 1
          rowMultiples = case ats of
            t : _ -> t `mod` w == 0 && last ats `mod` w == 0
            []    -> False
      in  oneView name sh a
            [ ("aliasing",      VS.length v < product sh)
            , ("row-multiples", rowMultiples) ]
    -- Non-vacuity: a 1 in an entry's stride list fails no-unit-stride
    -- alone -- the mistyped entry being exactly what it guards -- and five
    -- elements of backing slack fail tight-backing alone.
    -- Non-vacuity, 2026-08-28: padding the outer stride by 0 instead of 1
    -- (a valid dense view) fails the regime, 1 where the class owes 2;
    -- listing a rank-1 shape is refused by 'mkRuns' itself.
    oneRuns (name, sh) =
      let (sh', a@(T (Strides ats) _ _)) = mkRuns sh
          (_, cats) = canonView sh' ats
      in  oneViewReg 2 name sh' a
            [ ("innermost-unit", last ats == 1)
            , ("canon-rank2",    length cats == 2 && last cats == 1) ]
    oneScaled (name, sh, strides) =
      let (sh', a@(T (Strides ats) _ v)) = mkScaled sh strides
      in  oneView name sh' a
            [ ("no-unit-stride", all (>= 2) ats)
            , ("tight-backing",  VS.length v
                                 == 1 + sum (zipWith (\s t -> (s - 1) * t)
                                             sh' ats)) ]
    -- Non-vacuity of the four below, proven at the interpreter on
    -- 2026-09-03 over small views of each generator's own kind. flip:
    -- leaving the last dim un-reversed (a valid partial rev) fails
    -- innermost-minus-one and canon-minus-one together and the regime
    -- with them, 2 where the class owes 3 -- so those two stand as the
    -- class's definition, their space guarded by the regime check, as
    -- bcast's stride0-inner does -- while shifting the offset by 7 over a
    -- backing grown by 7 fails offset-rev-sum alone. block: an enclosure
    -- equal to the view fails canon-rank and the regime together, 1 where
    -- the class owes 2, and a backing grown by 7 fails backing-enclosing
    -- alone; innermost-unit and offset-listed derive from the generator
    -- and stand as its definition. small: a backing grown by 1 fails
    -- tight-backing alone, and a view of 1152 elements fails few-hundred
    -- alone. compose: a lone innermost zero stride at offset 0 fails
    -- second-mechanism alone.
    oneFlip (name, rs, sh) =
      let (sh', a@(T (Strides ats) ao _)) = mkFlip rs sh
          (_, cats) = canonView sh' ats
      in  oneView name sh' a
            [ ("innermost-minus-one", last ats == -1)
            , ("canon-minus-one",     last cats == -1)
            , ("offset-rev-sum", ao == sum [(n - 1) * negate t
                                           | (n, t) <- zip sh' ats, t < 0]) ]
    oneBlock (name, sh, esh, ao) =
      let (sh', a@(T (Strides ats) ao' v)) = mkBlock sh esh ao
          (csh, _) = canonView sh' ats
      in  oneViewReg 2 name sh' a
            [ ("innermost-unit",    last ats == 1)
            , ("canon-rank",        length csh == length sh')
            , ("offset-listed",     ao' == ao)
            , ("backing-enclosing", VS.length v == product esh) ]
    oneSmall (name, reg, sh, strides) =
      let (sh', a@(T (Strides ats) _ v)) = mkSmall sh strides
      in  oneViewReg reg name sh' a
            [ ("few-hundred",   product sh' < 1000)
            , ("tight-backing", VS.length v
                                == 1 + sum (zipWith (\s t -> (s - 1) * t)
                                            sh' ats)) ]
    oneCompose (name, sh, strides, ao) =
      let (sh', a@(T (Strides ats) ao' v)) = mkCompose sh strides ao
          zeros = [i | (i, t) <- zip [0 :: Int ..] ats, t == 0]
          apart = or [b - c > 1 | (c, b) <- zip zeros (drop 1 zeros)]
          second = any (< 0) ats || ao' > 0 || length zeros == length ats
                   || apart
      in  oneView name sh' a
            [ ("zero-stride",      not (null zeros))
            , ("second-mechanism", second)
            , ("tight-backing",    VS.length v
                                   == 1 + ao' + sum [(s - 1) * t
                                                    | (s, t) <- zip sh' ats
                                                    , t > 0]) ]

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
