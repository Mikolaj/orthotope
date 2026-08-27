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

{-# OPTIONS_GHC -Wno-incomplete-uni-patterns #-}
{-# LANGUAGE AllowAmbiguousTypes #-}
{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE QuantifiedConstraints #-}
{-# LANGUAGE RecordWildCards #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}
{-# LANGUAGE UndecidableSuperClasses #-}
module Data.Array.Internal(module Data.Array.Internal) where
import Control.DeepSeq
import Control.Monad.ST(ST)
import Data.Data(Data)
import Data.Kind (Type)
import Data.List(foldl', zipWith4, zipWith5, sortBy, sortOn, foldl1')
import Data.Proxy
import qualified Data.Vector.Generic as VG
import qualified Data.Vector.Generic.Mutable as VGM
import qualified Data.Vector.Unboxed as VU
import GHC.Exts(Constraint, build)
import GHC.Generics(Generic)
import GHC.TypeLits(KnownNat, natVal)
import Text.PrettyPrint
import Text.PrettyPrint.HughesPJClass

{- HLINT ignore "Reduce duplication" -}

-- The underlying storage of values must be an instance of Vector.
-- For some types, like unboxed vectors, we require an extra
-- constraint on the elements, which VecElem allows you to express.
-- For vector types that don't need the constraint it can be set
-- to some dummy class.
-- | The 'Vector' class is the interface to the underlying storage for the arrays.
-- The operations map straight to operations for 'Vector'.
class Vector v where
  type VecElem v :: Type -> Constraint
  vIndex    :: (VecElem v a) => v a -> Int -> a
  vLength   :: (VecElem v a) => v a -> Int
  vToList   :: (VecElem v a) => v a -> [a]
  vFromList :: (VecElem v a) => [a] -> v a
  vFromListN:: (VecElem v a) => Int -> [a] -> v a
  vSingleton:: (VecElem v a) => a -> v a
  vReplicate:: (VecElem v a) => Int -> a -> v a
  vMap      :: (VecElem v a, VecElem v b) => (a -> b) -> v a -> v b
  vZipWith  :: (VecElem v a, VecElem v b, VecElem v c) => (a -> b -> c) -> v a -> v b -> v c
  vZipWith3 :: (VecElem v a, VecElem v b, VecElem v c, VecElem v d) => (a -> b -> c -> d) -> v a -> v b -> v c -> v d
  vZipWith4 :: (VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e) => (a -> b -> c -> d -> e) -> v a -> v b -> v c -> v d -> v e
  vZipWith5 :: (VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e, VecElem v f) => (a -> b -> c -> d -> e -> f) -> v a -> v b -> v c -> v d -> v e -> v f
  vAppend   :: (VecElem v a) => v a -> v a -> v a
  vConcat   :: (VecElem v a) => [v a] -> v a
  vFold     :: (VecElem v a) => (a -> a -> a) -> a -> v a -> a
  vSlice    :: (VecElem v a) => Int -> Int -> v a -> v a
  vSum      :: (VecElem v a, Num a) => v a -> a
  vProduct  :: (VecElem v a, Num a) => v a -> a
  vMaximum  :: (VecElem v a, Ord a) => v a -> a
  vMinimum  :: (VecElem v a, Ord a) => v a -> a
  vUpdate   :: (VecElem v a) => v a -> [(Int, a)] -> v a
  vGenerate :: (VecElem v a) => Int -> (Int -> a) -> v a
  vAll      :: (VecElem v a) => (a -> Bool) -> v a -> Bool
  vAny      :: (VecElem v a) => (a -> Bool) -> v a -> Bool

  -- | Materialize a strided view in row-major order.  The arguments are
  -- the shape, the strides, the offset, the total element count
  -- (@product sh@, passed in because every caller already has it) and
  -- the source vector; the shape must be non-empty.  This method is
  -- what makes a fast 'toVectorListT' possible, and that function's
  -- strided fallback goes through it: when
  -- the innermost dimension is strided no slice can be taken, and the
  -- fast fills for that case write a mutable result buffer across runs,
  -- which no existing method can express ('vGenerate' is stateless).
  -- The default is a terse but fast pure form, where the base-offsets
  -- table is built by expansion ('runBaseOffsetsT'), one division
  -- per element. The vector-backed instances override it with
  -- the faster mutable fill 'genericFillStrided'.  If the default's
  -- speed mattered, which it does not, -fspec-constr would improve it.
  vFillStrided :: (VecElem v a) => ShapeL -> [Int] -> Int -> Int -> v a -> v a
  vFillStrided sh ats ao l v =
    let !sInner = last sh
        !tInner = last ats
        !baseOffsets = runBaseOffsetsT ao (init sh) (init ats)
        gen i = case i `quotRem` sInner of
          (!q, !r) -> vIndex v (VU.unsafeIndex baseOffsets q + r * tInner)
    in  vGenerate l gen

class None a
instance None a

-- This instance is not used anywheer.  It serves more as a reference semantics.
instance Vector [] where
  type VecElem [] = None
  vIndex = (!!)
  vLength = length
  vToList = id
  vFromList = id
  vFromListN _ = id
  vSingleton = pure
  vReplicate = replicate
  vMap = map
  vZipWith = zipWith
  vZipWith3 = zipWith3
  vZipWith4 = zipWith4
  vZipWith5 = zipWith5
  vAppend = (++)
  vConcat = concat
  vFold = foldl'
  vSlice o n = take n . drop o
  vSum = sum
  vProduct = product
  vMaximum = maximum
  vMinimum = minimum
  vUpdate xs us = loop xs (sortOn fst us) 0
    where
      loop [] [] _ = []
      loop [] (_:_) _ = error "vUpdate: out of bounds"
      loop as [] _ = as
      loop (a:as) ias@((i,a'):ias') n =
        case compare i n of
          LT -> error "vUpdate: bad index"
          EQ -> a' : loop as ias' (n+1)
          GT -> a  : loop as ias  (n+1)
  vGenerate n f = map f [0 .. n-1]
  vAll = all
  vAny = any

prettyShowL :: (Pretty a) => PrettyLevel -> a -> String
prettyShowL l = render . pPrintPrec l 0

-- | The type /T/ is the internal type of arrays.  In general,
-- operations on /T/ do no sanity checking as that should be done
-- at the point of call.
--
-- To avoid manipulating the data the indexing into the vector containing
-- the data is somewhat complex.  To find where item /i/ of the outermost
-- dimension starts you calculate vector index @offset + i*strides[0]@.
-- To find where item /i,j/ of the two outermost dimensions is you
-- calculate vector index @offset + i*strides[0] + j*strides[1]@, etc.
type role T representational nominal
data T v a = T
    { strides :: ![Int]   -- length is tensor rank
    , offset  :: !Int     -- offset into vector of values
    , values  :: !(v a)   -- actual values
    }
    deriving (Show, Generic, Data)

instance NFData (v a) => NFData (T v a)

-- | The shape of an array is a list of its dimensions.
type ShapeL = [Int]

badShape :: ShapeL -> Bool
badShape = any (< 0)

-- When shapes match, we can be efficient and use loop-fused comparisons instead
-- of materializing a vector.
-- Note this assumes the shape is the same for both Vectors.
-- TODO(augustss): if the array is a small fraction of the vector this can be inefficient.
{-# INLINABLE equalT #-}
equalT :: (Vector v, VecElem v a, Eq a, Eq (v a))
                  => ShapeL -> T v a -> T v a -> Bool
equalT s x y | strides x == strides y
               && offset x == offset y
               && values x == values y = True
             | otherwise = toVectorT s x == toVectorT s y

-- Note this assumes the shape is the same for both Vectors.
{-# INLINABLE compareT #-}
compareT :: (Vector v, VecElem v a, Ord a, Ord (v a))
            => ShapeL -> T v a -> T v a -> Ordering
compareT s x y = compare (toVectorT s x) (toVectorT s y)

-- Given the dimensions, return the stride in the underlying vector
-- for each dimension.  The first element of the list is the total length.
{-# INLINE getStridesT #-}
getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

-- Convert an array to a list by indexing through all the elements.
-- The first argument is the array shape.
-- XXX Copy special cases from Tensor.
{-# INLINE toListT #-}
toListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [a]
toListT sh a@(T ss0 o0 v)
  | isCanonicalT (getStridesT sh) a = vToList v
  | otherwise = build $ \cons nil ->
      -- TODO: because unScalarT uses vIndex, this has unnecessary bounds
      -- checks.  We should expose an unchecked indexing function in the Vector
      -- class, add top-level bounds checks to cover the full range we'll
      -- access, and then do all accesses with the unchecked version.
      let go []     ss o rest = cons (unScalarT (T ss o v)) rest
          go (n:ns) ss o rest = foldr
            (\i -> case indexT (T ss o v) i of T ss' o' _ -> go ns ss' o')
            rest
            [0..n-1]
      in  go sh ss0 o0 nil

-- | Check if the strides are canonical, i.e., if the vector have the natural layout.
-- XXX Copy special cases from Tensor.
{-# INLINE isCanonicalT #-}
isCanonicalT :: (Vector v, VecElem v a) => [Int] -> T v a -> Bool
isCanonicalT (n:ss') (T ss o v) =
    o == 0 &&         -- Vector offset is 0
    ss == ss' &&      -- All strides are normal
    vLength v == n    -- The vector is the right size
isCanonicalT _ _ = error "impossible"

-- Convert a value to a scalar array.
{-# INLINE scalarT #-}
scalarT :: (Vector v, VecElem v a) => a -> T v a
scalarT = T [] 0 . vSingleton

-- Convert a scalar array to the actual value.
{-# INLINE unScalarT #-}
unScalarT :: (Vector v, VecElem v a) => T v a -> a
unScalarT (T _ o v) = vIndex v o

-- Make a constant array.
{-# INLINE constantT #-}
constantT :: (Vector v, VecElem v a) => ShapeL -> a -> T v a
constantT sh x = T (map (const 0) sh) 0 (vSingleton x)

-- Canonicalize a view for dispatch.  The invariant, holding before and
-- after: for an array of shape @sh@ and strides @ats@ over a vector at
-- some offset, the pair returned describes, over the same vector and
-- offset, an array with the same row-major element sequence --- the
-- array's elements listed with the last index varying fastest, the
-- order 'toVectorT' materializes.  Two rewrites keep it: drop the
-- dimensions of extent 1, which contribute @0 * stride@ to every index
-- whatever their stride; then merge each adjacent pair of dimensions
-- where @st_outer == n_inner * st_inner@, the index sum's own
-- distributivity, so it holds for negative strides too.  After it the
-- shape has no extent 1 and the strides no adjacent pair satisfying
-- that equation.
-- So a maximal run of the array's elements that are consecutive in the
-- vector is one canonical dimension of stride 1; a dense array (its
-- elements filling a contiguous piece of the vector in row-major order)
-- has the natural strides at whatever rank it was given; and a
-- broadcast axis (a dimension of stride 0, all its indices reading one
-- element) adjacent to another has become one with it.  O(rank) list
-- work.
{-# INLINE canonicalizeT #-}
canonicalizeT :: ShapeL -> [Int] -> (ShapeL, [Int])
canonicalizeT sh ats = canon sh ats
  where canon [] [] = ([], [])
        canon (1 : ns) (_ : ts) = canon ns ts
        canon (n : ns) (t : ts) = case canon ns ts of
          (n' : ns', t' : ts') | t == n' * t' -> (n * n' : ns', t' : ts')
          (ns', ts') -> (n : ns', t : ts')
        canon _ _ = error $ "canonicalizeT: rank mismatch " ++ show (sh, ats)

-- Base offset (into the values vector) of each innermost run of an array,
-- in row-major order over the outer dimensions (all dimensions but the
-- innermost).  The outer offset grid is separable (@o0 + sum idx_d *
-- stride_d@), so it is built by iterated expansion: from the singleton
-- @[o0]@, each outer dimension expands every partial base-offset @a@ into
-- @enumFromStepN a stride_d n_d@ (a constant-stride run, no division), all
-- inside vector's stream framework rather than a hand-written loop.  The
-- result is the unboxed Int scratch 'vFillStrided''s default indexes; it
-- has @product osh@ elements.
{-# INLINE runBaseOffsetsT #-}
runBaseOffsetsT :: Int    -- ^ the array offset to start from
                -> [Int]  -- ^ outer dimensions, i.e. @init sh@
                -> [Int]  -- ^ outer strides, i.e. @init (strides a)@
                -> VU.Vector Int
runBaseOffsetsT o0 osh oats = foldl' expand (VU.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- The measured-fastest fill for 'vFillStrided': an allocate-once mutable
-- result, an odometer recursion over the outer dimensions with the input
-- offset stepped additively, the innermost outer level fused into a
-- dedicated run loop, and the run fill unrolled by two with its bound on
-- the output cursor, so it is sound for zero and negative strides.
-- Written once against 'Data.Vector.Generic', which supplies the mutable
-- machinery orthotope's own 'Vector' class deliberately does not; each
-- vector-backed instance reuses it verbatim.  Ported bang-for-bang from
-- the benchmarked arm (mut-odo-vecdims-add-in-leaf-u2): the bang
-- patterns are part of what was measured. The benchmarks are preserved
-- at https://github.com/Mikolaj/orthotope/blob/speedup-strided-tovector/micro-regime3/
-- and the implementation is similar to what once was in orthotope file
-- FastReshape.hs, but independently discovered and improved on by Opus Fable.
{-# INLINE genericFillStrided #-}
genericFillStrided :: forall w a. (VG.Vector w a)
                   => ShapeL -> [Int] -> Int -> Int -> w a -> w a
genericFillStrided sh ats ao l v = VG.create fill
  where
    fill :: forall s. ST s (VG.Mutable w s a)
    fill = do
      out <- VGM.unsafeNew l
      let writeRun :: Int -> Int -> ST s ()
          writeRun !outPos !baseOff =
            let !oEnd = outPos + sInner
                inner :: Int -> Int -> ST s ()
                inner !o !src
                  | o + 1 >= oEnd =
                      if o >= oEnd then return ()
                      else VGM.unsafeWrite out o (VG.unsafeIndex v src)
                  | otherwise = do
                      VGM.unsafeWrite out o (VG.unsafeIndex v src)
                      VGM.unsafeWrite
                        out (o + 1) (VG.unsafeIndex v (src + tInner))
                      inner (o + 2) (src + t2)
            in  inner outPos baseOff
          go :: Int -> Int -> Int -> ST s Int
          go !lev !outPos !baseOff
            | lev >= rOuter = writeRun outPos baseOff
                              >> return (outPos + sInner)
            | lev == rOuter - 1 =
                let !n  = VU.unsafeIndex oshV lev
                    !st = VU.unsafeIndex oatsV lev
                    run :: Int -> Int -> Int -> ST s Int
                    run !k !op !boff
                      | k <= 0    = return op
                      | otherwise = writeRun op boff
                                    >> run (k - 1) (op + sInner) (boff + st)
                in  run n outPos baseOff
            | otherwise =
                let !n  = VU.unsafeIndex oshV lev
                    !st = VU.unsafeIndex oatsV lev
                    dim :: Int -> Int -> Int -> ST s Int
                    dim !k !op !boff
                      | k <= 0    = return op
                      | otherwise = go (lev + 1) op boff
                                    >>= \op' -> dim (k - 1) op' (boff + st)
                in  dim n outPos baseOff
      _ <- go 0 0 ao
      return out
    !sInner = last sh
    !tInner = last ats
    !t2 = tInner + tInner
    !rOuter = length sh - 1
    oshV, oatsV :: VU.Vector Int
    !oshV  = VU.fromList (init sh)
    !oatsV = VU.fromList (init ats)

-- The regime a view falls in once canonicalized, which is what
-- 'toVectorListT' and 'toVectorT' dispatch on.  Classified on the
-- canonical dimensions, so a unit dimension's arbitrary stride and a
-- reshape's appended dimensions no longer decide it.  The element count
-- (@product sh@) is passed in because every caller already has it, as
-- 'vFillStrided' takes it.
data Regime
  = Whole                  -- the canonical strides are the natural ones,
                           -- the offset 0 and the vector's length the
                           -- array's: the vector itself, as is
  | Slice                  -- the natural strides at an offset or over a
                           -- longer vector: a contiguous slice of it.
                           -- Rank 0 lands here or above: no dimensions,
                           -- no strides, the one element at the offset
  | Runs ShapeL [Int]      -- canonical innermost stride 1 under other
                           -- dimensions: contiguous runs, one per
                           -- canonical outer index
  | Strided ShapeL [Int]   -- any other canonical view: no run longer than
                           -- one element

{-# INLINE regimeT #-}
regimeT :: (Vector v, VecElem v a) => ShapeL -> Int -> T v a -> Regime
regimeT sh l (T ats ao v) = case canonicalizeT sh ats of
  (csh, cats)
    | cats /= ts -> if last cats == 1 then Runs csh cats else Strided csh cats
    | ao == 0 && vLength v == l -> Whole
    | otherwise -> Slice
    where _ : ts = getStridesT csh

-- Convert an array to a list of vectors, which together contain
-- all the elements in the natural order.
-- An invariant: if the input array is non-empty the returned list
-- will have no empty vectors.
-- The minimum/maximum operations rely on this invariant.
{-# INLINE toVectorListT #-}
toVectorListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [v a]
toVectorListT sh a@(T _ ao v)
  | l == 0 = []
  | otherwise = case regimeT sh l a of
      Whole -> [v]
      Slice -> [vSlice ao l v]
      Runs csh cats ->
        -- One slice per canonical run, the runs' base offsets built by
        -- expansion as the pure fill builds them.
        let !n = last csh
        in  map (\o -> vSlice o n v)
                (VU.toList (runBaseOffsetsT ao (init csh) (init cats)))
      Strided csh cats ->
        -- No slice can be taken.  Fill the result through
        -- 'vFillStrided', whose vector-backed instances write a mutable
        -- buffer directly.
        [vFillStrided csh cats ao l v]
  where !l = product sh

-- Convert an array to one vector holding all the elements in the
-- natural order.  Dispatches as 'toVectorListT' does, except that a
-- view of contiguous runs is filled through 'vFillStrided' rather than
-- sliced and concatenated: in the micro-benchmark 'genericFillStrided'
-- links, on runs of nine elements, the slice list ties the fill on time
-- and allocates several times the result in slice headers and list
-- cells.  The fill's stepping loop at stride 1 is the run copy: a
-- per-run memcpy measured slower than it on every run length tried.
{-# INLINE toVectorT #-}
toVectorT :: (Vector v, VecElem v a) => ShapeL -> T v a -> v a
toVectorT sh a@(T _ ao v)
  | l == 0 = vConcat []
  | otherwise = case regimeT sh l a of
      Whole -> v
      Slice -> vSlice ao l v
      Runs csh cats -> vFillStrided csh cats ao l v
      Strided csh cats -> vFillStrided csh cats ao l v
  where !l = product sh

-- Convert to a list of vectors containing altogether the right elements,
-- but not necessarily in the right order.
-- This is used for reduction with commutative&associative operations.
-- The one-block test is explained right below.
{-# INLINE toUnorderedVectorListT #-}
toUnorderedVectorListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [v a]
toUnorderedVectorListT sh a@(T ats ao v)
  | l == 0 = []
  | otherwise =
      let (csh, cats) = canonicalizeT sh ats
          oneBlock =
            let (acats, csh') =
                  unzip $ sortBy (flip compare) $ zip (map abs cats) csh
                _ : ts = getStridesT csh'
            in  acats == ts
      in  if oneBlock
          then let !start =
                     ao + sum [ (n - 1) * st | (n, st) <- zip csh cats, st < 0 ]
               in  [vSlice start l v]
          else toVectorListT sh a
  where !l = product sh

-- The one-block test of 'toUnorderedVectorListT', piece by piece.
--
-- Overview.  A consumer that folds with a commutative and associative
-- operation needs the array's elements as a multiset, not in order.  So
-- the question is whether the view reads each element of one contiguous
-- block of the vector exactly once, in whatever order; if it does, that
-- block is the answer as a single slice, and only otherwise are the
-- elements materialized in row-major order through 'toVectorListT'.
--
-- Why canonicalizeT.  Unit dimensions carry arbitrary strides and would
-- fail any stride test while touching nothing; merging adjacent
-- dimensions makes the test below exact rather than sufficient (two
-- dimensions that are one contiguous run read as one natural stride,
-- not as two that happen to compose).  Canonicalization preserves the
-- element sequence, so it preserves the multiset the consumer wants.
--
-- Why abs.  A negative stride walks an axis backwards over the same
-- cells a positive one walks forwards.  Order is not asked for here, so
-- only the magnitude says which cells are touched; the sign is used once
-- more, below, to find where the block begins.
--
-- Why sort.  A transposition reorders the dimensions and their strides
-- together without changing which cells are touched (an index sum does
-- not care about the order of its terms).  Sorting by stride magnitude,
-- descending, picks the one ordering in which a block-covering view has
-- its dimensions from outermost to innermost, so the test need not try
-- the permutations.
--
-- Why acats == ts.  Take a plain array with shape csh' built by
-- 'fromVectorT': its strides are 'getStridesT' csh' without the head,
-- the innermost 1 and each outer one the product of the extents inside
-- it, and its elements are exactly the vector's first product csh'
-- cells, each once.  The sorted view has the same extents; if its stride
-- magnitudes equal those natural strides, then index for index it
-- addresses the same cells as that plain array would, shifted by start
-- --- so it is such an array up to transposition and reversals, and
-- covers one block of product csh' cells exactly once.  Any other
-- magnitudes fail: 0 reads one cell many times (a broadcast), a larger
-- stride leaves gaps (a strided or interior slice), a smaller one
-- overlaps (a window).  The plain array is never built; only the
-- strides it would have are computed and compared.
--
-- Why start.  The slice has to begin at the block's lowest address, and
-- the offset ao is not it: ao is where index (0, ..., 0) sits, which is
-- the lowest address only when every stride is positive.  The address
-- of index (i_0, ..., i_k) is ao + sum i_d * st_d, and the sum is
-- smallest when each term is: at i_d = 0 for a positive stride, at
-- i_d = n_d - 1, the last index, for a negative one, where the term is
-- (n_d - 1) * st_d and negative.  So start is ao plus those negative
-- terms, one per reversed axis.
--
-- Why st < 0.  Only the reversed axes move the block's start; a positive
-- stride's smallest term is 0 and would add nothing to the sum, so the
-- filter leaves it out rather than adding it as 0.  A stride of 0 cannot
-- reach this branch, oneBlock having rejected it.  The strides here are
-- the canonical ones, not the sorted magnitudes: the sign is what the
-- sort threw away and this sum needs, and the extents must pair with
-- their own strides, which zip csh cats does and the sorted lists,
-- being reordered, would not.

{-# INLINE toUnorderedVectorT #-}
toUnorderedVectorT :: (Vector v, VecElem v a) => ShapeL -> T v a -> v a
toUnorderedVectorT sh a = case toUnorderedVectorListT sh a of
  [v] -> v
  l -> vConcat l

-- Convert from a vector.
{-# INLINE fromVectorT #-}
fromVectorT :: ShapeL -> v a -> T v a
fromVectorT sh = T (tail $ getStridesT sh) 0

-- Convert from a list
{-# INLINE fromListT #-}
fromListT :: (Vector v, VecElem v a) => [Int] -> [a] -> T v a
fromListT sh = fromVectorT sh . vFromListN (product sh)

-- Index into the outermost dimension of an array.
{-# INLINE indexT #-}
indexT :: T v a -> Int -> T v a
indexT (T (s : ss) o v) i = T ss (o + i * s) v
indexT _ _ = error "impossible"

-- Stretch the given dimensions to have arbitrary size.
-- The stretched dimensions must have size 1, and stretching is
-- done by setting the stride to 0.
{-# INLINE stretchT #-}
stretchT :: [Bool] -> T v a -> T v a
stretchT bs (T ss o v) = T (zipWith (\ b s -> if b then 0 else s) bs ss) o v

-- Map over the array elements.
{-# INLINE mapT #-}
mapT :: (Vector v, VecElem v a, VecElem v b) => ShapeL -> (a -> b) -> T v a -> T v b
mapT sh f (T ss o v) | product sh >= vLength v = T ss o (vMap f v)
mapT sh f t = fromVectorT sh $ vMap f $ toVectorT sh t

-- Zip two arrays with a function.
{-# INLINE zipWithT #-}
zipWithT :: (Vector v, VecElem v a, VecElem v b, VecElem v c) =>
            ShapeL -> (a -> b -> c) -> T v a -> T v b -> T v c
zipWithT sh f t@(T ss _ v) t'@(T _ _ v') =
  case (vLength v, vLength v') of
    (1, 1) ->
      -- If both vectors have length 1, then it's a degenerate case and it's better
      -- to operate on the single element directly.
      T ss 0 $ vSingleton $ f (vIndex v 0) (vIndex v' 0)
    (1, _) ->
      -- First vector has length 1, so use a map instead.
      mapT sh (vIndex v 0 `f` ) t'
    (_, 1) ->
      -- Second vector has length 1, so use a map instead.
      mapT sh (`f` vIndex v' 0) t
    (_, _) ->
      let cv  = toVectorT sh t
          cv' = toVectorT sh t'
      in  fromVectorT sh $ vZipWith f cv cv'

-- Zip three arrays with a function.
{-# INLINE zipWith3T #-}
zipWith3T :: (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d) =>
             ShapeL -> (a -> b -> c -> d) -> T v a -> T v b -> T v c -> T v d
zipWith3T _ f (T ss _ v) (T _ _ v') (T _ _ v'') |
  -- If all vectors have length 1, then it's a degenerate case and it's better
  -- to operate on the single element directly.
  vLength v == 1, vLength v' == 1, vLength v'' == 1 =
    T ss 0 $ vSingleton $ f (vIndex v 0) (vIndex v' 0) (vIndex v'' 0)
zipWith3T sh f t t' t'' = fromVectorT sh $ vZipWith3 f v v' v''
  where v   = toVectorT sh t
        v'  = toVectorT sh t'
        v'' = toVectorT sh t''

-- Zip four arrays with a function.
{-# INLINE zipWith4T #-}
zipWith4T :: (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e) => ShapeL -> (a -> b -> c -> d -> e) -> T v a -> T v b -> T v c -> T v d -> T v e
zipWith4T sh f t t' t'' t''' = fromVectorT sh $ vZipWith4 f v v' v'' v'''
  where v   = toVectorT sh t
        v'  = toVectorT sh t'
        v'' = toVectorT sh t''
        v'''= toVectorT sh t'''

-- Zip five arrays with a function.
{-# INLINE zipWith5T #-}
zipWith5T :: (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e, VecElem v f) => ShapeL -> (a -> b -> c -> d -> e -> f) -> T v a -> T v b -> T v c -> T v d -> T v e -> T v f
zipWith5T sh f t t' t'' t''' t'''' = fromVectorT sh $ vZipWith5 f v v' v'' v''' v''''
  where v   = toVectorT sh t
        v'  = toVectorT sh t'
        v'' = toVectorT sh t''
        v'''= toVectorT sh t'''
        v''''= toVectorT sh t''''

-- Do an arbitrary transposition.  The first argument should be
-- a permutation of the dimension, i.e., the numbers [0..r-1] in some order
-- (where r is the rank of the array).
{-# INLINE transposeT #-}
transposeT :: [Int] -> T v a -> T v a
transposeT is (T ss o v) = T (permute is ss) o v

-- Return all subarrays n dimensions down.
-- The shape argument should be a prefix of the array shape.
{-# INLINE subArraysT #-}
subArraysT :: ShapeL -> T v a -> [T v a]
subArraysT sh ten = sub sh ten []
  where sub [] t = (t :)
        sub (n:ns) t = foldr (.) id [sub ns (indexT t i) | i <- [0..n-1]]

-- Reverse the given dimensions.
{-# INLINE reverseT #-}
reverseT :: [Int] -> ShapeL -> T v a -> T v a
reverseT rs sh (T ats ao v) = T rts ro v
  where (ro, rts) = rev 0 sh ats
        rev !_ [] [] = (ao, [])
        rev r (m:ms) (t:ts) | r `elem` rs = (o + (m-1)*t, -t : ts')
                            | otherwise   = (o,            t : ts')
          where (o, ts') = rev (r+1) ms ts
        rev _ _ _ = error "reverseT: impossible"

-- Reduction of all array elements.
{-# INLINE reduceT #-}
reduceT :: (Vector v, VecElem v a) =>
           ShapeL -> (a -> a -> a) -> a -> T v a -> T v a
reduceT sh f z = scalarT . foldl' (vFold f) z . toVectorListT sh

-- Right fold via toListT.
{-# INLINE foldrT #-}
foldrT
  :: (Vector v, VecElem v a) => ShapeL -> (a -> b -> b) -> b -> T v a -> b
foldrT sh f z a = foldr f z (toListT sh a)

-- Traversal via toListT/fromListT.
{-# INLINE traverseT #-}
traverseT
  :: (Vector v, VecElem v a, VecElem v b, Applicative f)
  => ShapeL -> (a -> f b) -> T v a -> f (T v b)
traverseT sh f a = fmap (fromListT sh) (traverse f (toListT sh a))

-- Fast check if all elements are equal.
{-# INLINABLE allSameT #-}
allSameT :: (Vector v, VecElem v a, Eq a) => ShapeL -> T v a -> Bool
allSameT sh t@(T _ _ v)
  | vLength v <= 1 = True
  | otherwise =
    let !l = toVectorListT sh t
        !x = vIndex (l !! 0) 0
    in  all (vAll (x ==)) l

newtype Rect = Rect { unRect :: [String] }  -- A rectangle of text

toRect :: String -> Rect
toRect = Rect . lines

fromRect :: Rect -> String
fromRect (Rect ls) = unlines ls

-- Make each Rect be of size h * w
rectPad :: Int -> Int -> Rect -> Rect
rectPad h w (Rect ls) = Rect $ map padL ls ++ replicate (h - length ls) mt
  where mt = replicate w ' '
        padL s = replicate (w - length s) ' ' ++ s

-- Horizontal catenation.  Assumes input rectangle are padded.
-- Adds empty space between Rects.
hcatRect :: Rect -> Rect -> Rect
hcatRect (Rect xs) (Rect ys) = Rect $ zipWith (\ x y -> x ++ " " ++ y) xs ys

-- Vertical catenation.  Assumes input rectangle are padded.
-- Adds no space between Rects.
vcatRect :: Rect -> Rect -> Rect
vcatRect (Rect xs) (Rect ys) = Rect $ xs ++ ys

rectHeight :: Rect -> Int
rectHeight = length . unRect

-- Widest line
rectWidth :: Rect -> Int
rectWidth = maximum . (0:) . map length . unRect

ppT
  :: (Vector v, VecElem v a, Pretty a)
  => PrettyLevel -> Rational -> ShapeL -> T v a -> Doc
ppT l p sh = maybeParens (p > 10) . vcat' . map text . unRect . box boxMode . ppT_ (prettyShowL l) sh
  where boxMode | l >= prettyNormal = BoxMode True True True
                | otherwise = BoxMode False False False
        vcat' = foldl' ($+$) empty

ppT_
  :: (Vector v, VecElem v a)
  => (a -> String) -> ShapeL -> T v a -> Rect
ppT_ show_ sh t = showsT sh t'
  where ss = map (toRect . show_) $ toListT sh t
        maxH = maximum $ map rectHeight ss
        maxW = maximum $ map rectWidth ss
        ss' = map (rectPad maxH maxW) ss
        t' :: T [] Rect
        t' = T (tail (getStridesT sh)) 0 ss'

showsT :: [Int] -> T [] Rect -> Rect
showsT []     t = unScalarT t
showsT s@[_]  t = foldl1' hcatRect $ toListT s t
showsT (n:ns) t = foldl1' vcat' rs
  where vcat' x y = vcatRect x (vcatRect spc y)
        spc = Rect $ replicate (length ns - 1) (replicate (rectWidth (head rs)) ' ')
        rs = [ showsT ns (indexT t i) | i <- [0..n-1] ]

data BoxMode = BoxMode { _bmBars, _bmUnicode, _bmHeader :: Bool }

prettyBoxMode :: BoxMode
prettyBoxMode = BoxMode False False False

-- Possibly draw a box around a (padded) rectangle.
box :: BoxMode -> Rect -> Rect
box BoxMode{..} (Rect ls) =
  let bar | _bmUnicode = '\x2502'
          | otherwise = '|'
      dash | _bmUnicode = '\x2500'
           | otherwise = '-'
      ls' | _bmBars = map (\ l -> if null l then l else [bar] ++ l ++ [bar]) ls
          | otherwise = ls
      h = replicate (length (head ls)) dash
      t | _bmUnicode = "\x250c" ++ h ++ "\x2510"
        | otherwise = "+" ++ h ++ "+"
      b | _bmUnicode = "\x2514" ++ h ++ "\x2518"
        | otherwise = t
      ls'' | _bmHeader = [t] ++ ls' ++ [b]
           | otherwise = ls'
  in  Rect ls''

zipWithLong2 :: (a -> b -> b) -> [a] -> [b] -> [b]
zipWithLong2 f (a:as) (b:bs) = f a b : zipWithLong2 f as bs
zipWithLong2 _     _     bs  = bs

{-# INLINABLE padT #-}
padT :: forall v a . (Vector v, VecElem v a) => a -> [(Int, Int)] -> ShapeL -> T v a -> ([Int], T v a)
padT v aps ash at = (ss, fromVectorT ss $ vConcat $ pad' aps ash st at)
  where pad' :: [(Int, Int)] -> ShapeL -> [Int] -> T v a -> [v a]
        pad' [] sh _ t = toVectorListT sh t
        pad' ((l,h):ps) (s:sh) (n:ns) t =
          [vReplicate (n*l) v] ++ concatMap (pad' ps sh ns . indexT t) [0..s-1] ++ [vReplicate (n*h) v]
        pad' _ _ _ _ = error $ "pad: rank mismatch " ++ show (length aps, length ash)
        _ : st = getStridesT ss
        ss = zipWithLong2 (\ (l,h) s -> l+s+h) aps ash

-- Check if a reshape is just adding/removing some dimensions of
-- size 1, in which case it can be done by just manipulating
-- the strides.  Given the old strides, the old shapes, and the
-- new shape it will return the possible new strides.
simpleReshape :: [Int] -> ShapeL -> ShapeL -> Maybe [Int]
simpleReshape osts os ns
  | filter (1 /=) os == filter (1 /=) ns = Just $ loop ns sts'
    -- Old and new dimensions agree where they are not 1.
    where
      -- Get old strides for non-1 dimensions
      sts' = [ st | (st, s) <- zip osts os, s /= 1 ]
      -- Insert stride 0 for all 1 dimensions in new shape.
      loop [] [] = []
      loop (1:ss)     sts  = 0  : loop ss sts
      loop (_:ss) (st:sts) = st : loop ss sts
      loop _ _ = error $ "simpleReshape: shouldn't happen " ++ show (osts, os, ns)
simpleReshape _ _ _ = Nothing

-- Note: assumes + is commutative&associative.
{-# INLINE sumT #-}
sumT :: (Vector v, VecElem v a, Num a) => ShapeL -> T v a -> a
sumT sh = sum . map vSum . toUnorderedVectorListT sh

-- Note: assumes * is commutative&associative.
{-# INLINE productT #-}
productT :: (Vector v, VecElem v a, Num a) => ShapeL -> T v a -> a
productT sh = product . map vProduct . toUnorderedVectorListT sh

-- Note: assumes max is commutative&associative.
{-# INLINE maximumT #-}
maximumT :: (Vector v, VecElem v a, Ord a) => ShapeL -> T v a -> a
maximumT sh = maximum . map vMaximum . toUnorderedVectorListT sh

-- Note: assumes min is commutative&associative.
{-# INLINE minimumT #-}
minimumT :: (Vector v, VecElem v a, Ord a) => ShapeL -> T v a -> a
minimumT sh = minimum . map vMinimum . toUnorderedVectorListT sh

{-# INLINE anyT #-}
anyT :: (Vector v, VecElem v a) => ShapeL -> (a -> Bool) -> T v a -> Bool
anyT sh p = or . map (vAny p) . toUnorderedVectorListT sh

{-# INLINE allT #-}
allT :: (Vector v, VecElem v a) => ShapeL -> (a -> Bool) -> T v a -> Bool
allT sh p = and . map (vAll p) . toUnorderedVectorListT sh

{-# INLINE updateT #-}
updateT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [([Int], a)] -> T v a
updateT sh t us = T ss 0 $ vUpdate (toVectorT sh t) $ map ix us
  where _ : ss = getStridesT sh
        ix (is, a) = (sum $ zipWith (*) is ss, a)

{-# INLINE generateT #-}
generateT :: (Vector v, VecElem v a) => ShapeL -> ([Int] -> a) -> T v a
generateT sh f = T ss 0 $ vGenerate s g
  where s : ss = getStridesT sh
        g i = f (toIx ss i)
        toIx [] _ = []
        toIx (n:ns) i = q : toIx ns r where (q, r) = quotRem i n

{-# INLINE iterateNT #-}
iterateNT :: (Vector v, VecElem v a) => Int -> (a -> a) -> a -> T v a
iterateNT n f x = fromListT [n] $ take n $ iterate f x

{-# INLINE iotaT #-}
iotaT :: (Vector v, VecElem v a, Enum a, Num a) => Int -> T v a
iotaT n = fromListT [n] [0 .. fromIntegral n - 1]    -- TODO: should use V.enumFromTo instead

-------

-- | Permute the elements of a list, the first argument is indices into the original list.
{-# INLINE permute #-}
permute :: [Int] -> [a] -> [a]
permute is xs = map (xs!!) is

-- | Like 'dropWhile' but at the end of the list.
revDropWhile :: (a -> Bool) -> [a] -> [a]
revDropWhile p = reverse . dropWhile p . reverse

{-# INLINABLE allSame #-}
allSame :: (Eq a) => [a] -> Bool
allSame [] = True
allSame (x : xs) = all (x ==) xs

-- | Get the value of a type level Nat.
-- Use with explicit type application, i.e., @valueOf \@42@
{-# INLINE valueOf #-}
valueOf :: forall n i . (KnownNat n, Num i) => i
valueOf = fromInteger $ natVal (Proxy :: Proxy n)
