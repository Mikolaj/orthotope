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
import Control.Exception(assert)
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
  -- the view's canonical axes ('Axes', a non-empty view by type), the
  -- offset, the total element count (@product sh@, passed in because
  -- every caller already has it) and the source vector.  This method is
  -- what makes a fast 'toVectorListT' and 'toVectorT' possible: every
  -- view that is not a slice of the source goes through it, over the
  -- view's canonical axes ('canonicalizeT'), and the fast fills
  -- write a mutable result buffer across runs, which no existing
  -- method can express ('vGenerate' is stateless).
  --
  -- The default is a terse but fast pure form, where the base-offsets
  -- table is built by expansion ('runBaseOffsetsT'), one division
  -- per element.  The vector-backed instances override it with
  -- the faster mutable fill 'genericFillStrided'.  If the default's
  -- speed mattered, which it does not, -fspec-constr would improve it.
  vFillStrided :: (VecElem v a) => Axes -> Int -> Int -> v a -> v a
  vFillStrided (Axes tInner sInner outerAxes) !ao !l !v =
    let !baseOffsets = runBaseOffsetsT ao (outerFirst outerAxes)
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
-- A @T@ is a view of its vector: it reads the vector through the offset
-- and the strides and copies nothing, so a slice, a transposition or
-- a broadcast of an array is another @T@ view over the same vector.
-- The comments below say /view/ for a @T@ taken with its shape; /walk/
-- for one traversal of a view's innermost axis; /innermost run/ for
-- what one walk yields, consecutive in the result whatever its stride;
-- and /run/ for a stretch of a view's elements that lie in the vector
-- consecutively and in the view's order, which an innermost run is at
-- innermost stride 1.
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
-- some offset, the (stride, extent) pairs returned describe, over the
-- same vector and offset, an array with the same row-major element
-- sequence --- the array's elements listed with the last index varying
-- fastest, the order 'toVectorT' materializes.  Two rewrites keep it:
-- drop the dimensions of extent 1, which contribute @0 * stride@ to
-- every index whatever their stride; then merge each adjacent pair of
-- dimensions where @st_outer == n_inner * st_inner@, the index sum's
-- own distributivity, so it holds for negative strides too.  After it
-- no extent is 1 and no adjacent pair satisfies that equation.
--
-- So a dense array (its elements filling a contiguous piece of the
-- vector in row-major order) has the natural strides at whatever rank
-- it was given, and a broadcast axis (a dimension of stride 0, all its
-- indices reading one element) adjacent to another has become one with
-- it; what the walks of the innermost dimension are, and are not, is
-- said at 'runSlicesT'.  One pass of O(rank) list work.
--
-- Returned innermost first, as 'InnerFirst', so that the innermost axis
-- and the axes outside it are a pattern match wherever a consumer takes
-- them apart, and empty exactly for a view of one element, rank 0 or
-- every extent 1, since every axis kept has extent 2 or more.
{-# INLINE canonicalizeT #-}
canonicalizeT :: ShapeL -> [Int] -> InnerFirst
canonicalizeT sh ats = InnerFirst (foldl' mergeInner [] (zip ats sh))

-- The merge step, one axis added inside the axes so far, whose head is
-- the axis just outside it: dropped where its extent is 1, merged into
-- the head where that one's stride is this one's stride times its
-- extent, so that the two are walked as one, and put in front of it
-- otherwise.  'unorderedRouteT' folds it over the pairs it has sorted,
-- from which its own walk has dropped the axes of extent 1 already.
mergeInner :: [(Int, Int)] -> (Int, Int) -> [(Int, Int)]
mergeInner acc (_, 1) = acc
mergeInner ((st', n') : rest) (!st, n)
  | st' == n * st = (st, n' * n) : rest
mergeInner acc p = p : acc
{-# INLINE mergeInner #-}

-- Base offset (into the values vector) of each innermost run of an array,
-- in row-major order over the outer dimensions (all dimensions but the
-- innermost), given as (stride, extent) pairs outermost first.  The
-- outer offset grid is separable (@o0 + sum idx_d * stride_d@), so it
-- is built by iterated expansion: from the singleton @[o0]@, each outer
-- dimension expands every partial base-offset @a@ into
-- @enumFromStepN a stride_d n_d@ (constant stride, no division), all
-- inside vector's stream framework rather than a hand-written loop.  The
-- result is the unboxed Int scratch 'vFillStrided''s default indexes; it
-- has as many elements as the outer dimensions have indices.
{-# INLINE runBaseOffsetsT #-}
runBaseOffsetsT :: Int -> [(Int, Int)] -> VU.Vector Int
runBaseOffsetsT o0 outer = foldl' expand (VU.singleton o0) outer
  where expand !acc (!sd, !nd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- The measured-fastest fill for 'vFillStrided': an allocate-once
-- mutable result, an odometer recursion over the outer dimensions with
-- the input offset stepped additively, the innermost outer level fused
-- into a dedicated loop over the innermost runs, and the innermost-run
-- fill unrolled by two with its bound on the output cursor, so it is
-- sound for zero and negative strides.
--
-- Two zero-stride conditions sit inside it, each decided per level
-- of the odometer and never per element: an innermost run at stride
-- 0 reads its one element once and stores it, and an outer level
-- of stride 0 fills the block below it once and copies it onto the
-- level's remaining positions by doubling.  Given canonical dimensions
-- ('canonicalizeT') the conditions fire wherever they can; given any
-- other dimensions the fill is still correct.
--
-- The count must be positive, asserted at entry: a zero-stride
-- innermost run reads its one element, and a zero-stride level writes
-- its innermost run or block, before reading the extent, so a zero
-- extent would read past the source or write into an empty result.
-- Every entry point of this module returns the empty vector or list
-- before routing an empty view here, and a caller of 'vFillStrided'
-- from outside owes the same; the assert is live in an unoptimized
-- build only, GHC dropping asserts at -O, and is checked there by
-- disabling 'toVectorT''s guard, which fails the Dynamic modules'
-- 'toVector_3' on it (2026-09-21).
--
-- Written once against 'Data.Vector.Generic', which supplies
-- the mutable machinery orthotope's own 'Vector' class deliberately does
-- not; each vector-backed instance reuses it verbatim.  Ported
-- bang-for-bang from the fastest fill of the micro-benchmark preserved
-- at https://github.com/Mikolaj/orthotope/blob/speedup-strided-tovector/micro-regime3/
-- (the bang patterns are part of what was measured); one choice made
-- for the NCG, marked at the line it is on, costs -fllvm a little.
--
-- The implementation is similar to what once was in orthotope file
-- FastReshape.hs (a Storable-only odometer flatten behind an unsafeCast to
-- Double or Float, never in the cabal file, removed once subsumed by this),
-- but independently discovered and improved on by Opus Fable.
{-# INLINE genericFillStrided #-}
genericFillStrided :: forall w a. (VG.Vector w a)
                   => Axes -> Int -> Int -> w a -> w a
genericFillStrided (Axes tInner sInner outerAxes) !ao !l !v =
  assert (l > 0) $ VG.create fill
  where
    fill :: forall s. ST s (VG.Mutable w s a)
    fill = do
      out <- VGM.unsafeNew l
      let -- The stepping run, an innermost run at nonzero stride: the
          -- source cursor advances by the stride, the fill unrolled
          -- by two.  Both bodies are INLINE so that inlining at their
          -- two sites each is the source's property and not a size
          -- threshold's.
          {-# INLINE writeRunStep #-}
          writeRunStep :: Int -> Int -> ST s ()
          writeRunStep !outPos !baseOff =
            let !oEnd = outPos + sInner
                inner :: Int -> Int -> ST s ()
                inner !o !src
                  | o + 1 >= oEnd =
                      if o >= oEnd then return ()
                      else VGM.unsafeWrite out o (VG.unsafeIndex v src)
                  -- FOR THE NCG, AND A REGRESSION UNDER -fllvm.  The
                  -- cursor steps twice by tInner instead of once by a
                  -- doubled stride: one live value fewer, which is what
                  -- lets the NCG's allocator keep the output base in
                  -- a register instead of reloading it twice a pair.
                  -- Worth 5 to 25% of the fill's instructions there,
                  -- most at long innermost runs; -fllvm needs neither,
                  -- keeps two induction variables and loses 1 to 8%.
                  | otherwise = do
                      VGM.unsafeWrite out o (VG.unsafeIndex v src)
                      let !src' = src + tInner
                      VGM.unsafeWrite out (o + 1) (VG.unsafeIndex v src')
                      inner (o + 2) (src' + tInner)
            in  inner outPos baseOff
          -- The broadcast run, the innermost run at stride 0: its one
          -- element read once, then the stores, unrolled by two as
          -- the stepping run is.  Without the unroll, a store and a
          -- compare per element read 1.20 of the stepping run serving
          -- the broadcast, a read and a store per element unrolled by
          -- two, at an innermost run of two elements; unrolled, the
          -- hoisted read wins.
          {-# INLINE writeRunSet #-}
          writeRunSet :: Int -> Int -> ST s ()
          writeRunSet !outPos !baseOff =
            let !x = VG.unsafeIndex v baseOff
                !oEnd = outPos + sInner
                inner :: Int -> ST s ()
                inner !o
                  | o + 1 >= oEnd =
                      if o >= oEnd then return ()
                      else VGM.unsafeWrite out o x
                  | otherwise = do
                      VGM.unsafeWrite out o x
                      VGM.unsafeWrite out (o + 1) x
                      inner (o + 2)
            in  inner outPos
          -- A zero-stride outer level: everything below it repeats
          -- verbatim, so the block below is filled once and copied to
          -- the level's remaining n - 1 positions.  Zero levels compose,
          -- the topmost firing and the ones below it falling inside the
          -- one block it fills.  The block at src, already written, to n
          -- copies in all: each pass copies everything written so far
          -- onto what follows, so the length doubles and the last pass
          -- is clipped.  One copy per block read 2.3 of the stepping run
          -- refilling the level on 200000 copies of 24 bytes; by
          -- doubling, the copy wins.
          copies :: Int -> Int -> Int -> ST s Int
          copies !n !blk !src
            | n <= 1 = return (src + blk)
            | otherwise = grow blk
            where
              !end = src + n * blk
              grow :: Int -> ST s Int
              grow !have
                | src + have >= end = return end
                | otherwise = do
                    let !len = min have (end - src - have)
                    VGM.unsafeCopy (VGM.unsafeSlice (src + have) len out)
                                   (VGM.unsafeSlice src len out)
                    grow (have + len)
          -- The fused level: n innermost runs, the run body a static
          -- argument, so that each of the two uses below inlines it
          -- with the body known, and the choice between the bodies is
          -- made once per entry here, a row of innermost runs, never
          -- per innermost run.
          {-# INLINE runsWith #-}
          runsWith :: (Int -> Int -> ST s ())
                   -> Int -> Int -> Int -> Int -> ST s Int
          runsWith writeRun !n !st !outPos !baseOff
            | st == 0 = writeRun outPos baseOff >> copies n sInner outPos
            | otherwise =
                let run :: Int -> Int -> Int -> ST s Int
                    run !k !op !boff
                      | k <= 0    = return op
                      | otherwise = writeRun op boff
                                    >> run (k - 1) (op + sInner) (boff + st)
                in  run n outPos baseOff
          go :: Int -> Int -> Int -> ST s Int
          go !lev !outPos !baseOff
            | lev >= rOuter =
                (if tInner == 0 then writeRunSet else writeRunStep)
                  outPos baseOff
                >> return (outPos + sInner)
            | otherwise =
                level (VU.unsafeIndex oshV lev) (VU.unsafeIndex oatsV lev)
            where
              level :: Int -> Int -> ST s Int
              level !n !st
                | lev == rOuter - 1 =
                    if tInner == 0
                    then runsWith writeRunSet n st outPos baseOff
                    else runsWith writeRunStep n st outPos baseOff
                | st == 0 = do
                    op' <- go (lev + 1) outPos baseOff
                    copies n (op' - outPos) outPos
                | otherwise =
                    let dim :: Int -> Int -> Int -> ST s Int
                        dim !k !op !boff
                          | k <= 0    = return op
                          | otherwise = go (lev + 1) op boff
                                        >>= \op' -> dim (k - 1) op' (boff + st)
                    in  dim n outPos baseOff
      _ <- go 0 0 ao
      return out
    -- No doubled stride here any more; see the fill's own note.
    !rOuter = length levels
    -- The odometer's levels are numbered outermost first.
    levels :: [(Int, Int)]
    levels = outerFirst outerAxes
    oshV, oatsV :: VU.Vector Int
    !oshV  = VU.fromList (map snd levels)
    !oatsV = VU.fromList (map fst levels)

-- | The route a non-empty view takes once canonicalized: what its
-- consumer does with it, which is what 'toVectorListT', 'toVectorT'
-- and, on the view with its axes reordered, the two unordered entry
-- points dispatch on.  A view of no elements (@product sh == 0@) has no
-- route: each of the four entry points returns the empty vector or list
-- before computing one.
--
-- Three constructors, one per thing that can be done with a view: slice
-- it, walk its runs as slices, or only expensively fill a vector from
-- it element by element.  Every route carries the offset it starts at
-- and the element count (@product sh@), which every caller has in hand,
-- so that a consumer takes the route and the vector and nothing beside
-- them; each constructor carries what its way takes and no more, and
-- 'RRuns' is the list consumer's alone, 'routeVectorT' filling it as it
-- fills 'RFill'.
--
-- The choice of constructors is partly arbitrary, motivated by
-- performance, partly systematic, following the runs a view contains,
-- and limited throughout by what the vector API underneath can express.
-- The set changes only when the vector API under it changes (e.g., a
-- reverse copy would give a reversed contiguous view a route of its
-- own) or another way of copying a view into a vector through the API
-- as it stands is measured to pay (the per-run memcpy 'toVectorT'
-- names was tried and did not).  The set does not need to change when
-- a new pattern of shape and strides arrives (e.g., windows whose runs
-- overlap), typically one a newly added array operation produces.  The
-- performance for such new patterns may not be ideal, but the routes
-- are correct, because the uniform run length is uniquely determined
-- for every non-empty canonical view and 'routeOfT' reads the route off
-- it alone; the note at 'runSlicesT' says what the length is and is
-- not.
data Route
  = RSlice !Int !Int
      -- ^ the canonical strides are the natural ones: one contiguous
      -- slice of the vector, at the start and of the count.  Rank 0
      -- lands here: no dimensions, no strides, one element
  | RRuns Axes !Int !Int
      -- ^ canonical innermost stride 1 under other dimensions:
      -- contiguous runs of the innermost extent, one per canonical
      -- outer index, from the start; the count is not needed to walk
      -- them, and is what they are filled by where one vector is asked
  | RFill Axes !Int !Int
      -- ^ any other canonical view: no run longer than one element, so
      -- the view is filled as one vector of the count, from the start

-- | Axes as (stride, extent) pairs, innermost first: the orientation
-- 'canonicalizeT' writes and every consumer of a canonical view reads.
-- A newtype so that the one place the orientation flips, the fills'
-- odometer numbering its levels outermost first, is 'outerFirst' and
-- nowhere else.
newtype InnerFirst = InnerFirst { innerFirst :: [(Int, Int)] }

-- The same axes outermost first, the one flip of the orientation.
{-# INLINE outerFirst #-}
outerFirst :: InnerFirst -> [(Int, Int)]
outerFirst = reverse . innerFirst

-- | The canonical axes of a non-empty view: the innermost stride and
-- extent, then the axes outside it, innermost first.  What
-- 'vFillStrided' and the runs walker take, so that neither has to find
-- the innermost axis in a list.
data Axes = Axes !Int !Int InnerFirst

{-# INLINE routeT #-}
routeT :: ShapeL -> Int -> T v a -> Route
routeT sh l (T ats ao _) = routeOfT ao l (canonicalizeT sh ats)

-- The route of a view given as its canonical axes, innermost first, at
-- a start offset and of an element count: 'routeT' reads it for the
-- view as it is and 'unorderedRouteT' for the view with its axes
-- reordered.
--
-- Decided on the canonical axes alone ('canonicalizeT'), so a unit
-- dimension's arbitrary stride and a reshape's appended dimensions do
-- not decide it, and the underlying vector never does: whether a slice
-- is the whole vector is 'wholeOrSliceT''s to see, where the vector is
-- handed out.
--
-- The uniform run length of a canonical view is the innermost extent
-- where the innermost stride is 1, and one element otherwise, and the
-- route is that length against the count: all of it, 'RSlice'; less
-- than it, 'RRuns'; one element, 'RFill'.
--
-- Whether the canonical strides are the natural ones is decided by
-- the canonical rank alone, so no stride list is built and compared:
-- natural strides at rank 2 or more are the merge equation of
-- 'canonicalizeT' holding at every adjacent pair, and after it no pair
-- satisfies that equation, so a canonical view is natural only at rank
-- 0, or at rank 1 with stride 1.
{-# INLINE routeOfT #-}
routeOfT :: Int -> Int -> InnerFirst -> Route
routeOfT start l (InnerFirst axes) = case axes of
  [] -> RSlice start l
  [(1, _)] -> RSlice start l
  (1, n) : rest -> RRuns (Axes 1 n (InnerFirst rest)) start l
  (t, n) : rest -> RFill (Axes t n (InnerFirst rest)) start l

-- The slices of a view of contiguous runs, one per canonical outer
-- index in row-major order, produced on demand.  The arguments are the
-- canonical axes, the innermost at stride 1 and its extent the run
-- length, the offset of the first run and the vector, then the cons
-- and nil of the 'build' the list entry points are written under, so
-- that a consumer folding the list fuses with the walk, holds no more
-- of the list than it has reached and, stopping early, does no more of
-- the walk.
--
-- The innermost outer level is a counter and a cursor; the levels
-- above it are an odometer of (index, extent, stride) triples touched
-- only on a carry, the levels exhausted on the way out reset and put
-- back on the front in their order.  One flat loop, and not a fold per
-- level with the rest of the list passed down as a continuation: fused
-- with a consumer's fold, the level form met at every level's exit a
-- continuation it could not see and passed the accumulator to it lazily
-- and boxed, a thunk and a box per run; here every continuation is
-- 'go', 'carry' or nil, all known to the compiler, so base's own left
-- folds, 'sum' among them, see a strict known call and allocate nothing
-- per run.
--
-- Each run that this function gives has the view's uniform run length:
-- the run length of the coarsest partition of the view into equal runs.
-- Each run is an innermost run at stride 1, and a walk stops at each
-- carry.  Thus the canonical dimensions and the start offset give the
-- number of runs and the start of each run.  A longer block of equal
-- runs is not possible, because it contains the first carry.  That one
-- is adjacent only when the merge equation holds, which the canonical
-- form does not permit.
--
-- These runs are not the maximal runs.  A maximal run continues through
-- a carry across two or more axes when that carry is adjacent.  Shape
-- [2,2,2] has such a carry at strides [7,5,1], and at strides [2,0,1],
-- which a stretched unit axis gives.  Thus the maximal runs are a
-- property of the stride values, and the uniform runs are a property of
-- the canonical structure.
--
-- To join two adjacent runs, the walk must compare the start of each
-- run with the end of the run before it.  The walk must also hold one
-- slice until the next run does not extend it.  The flat loop gives
-- each slice to the consumer as soon as the walk reaches it and holds
-- no slice back.  A slice held back is live across iterations, so a
-- join can change the measured cost of the loop.  The join has a cost
-- for each view of runs and a gain only for such strides, so it is not
-- measured.
--
-- Entered on a view of canonical rank two or more, which is what
-- 'RRuns' means, so there is at least one outer level and one run.  The
-- arm for no outer level, which no route reaches, is the one run as
-- one slice: correct rather than an error, so the walker is total on
-- its own terms and the type asks nothing of the route that builds it.
--
-- The bang on the vector is measured, not style: every use of it sits
-- under the consumer's cons, so without the bang the walk is lazy in
-- it, takes it boxed and re-enters it on every run for its length and
-- address, most of the instructions a run of two elements costs.  The
-- bang on the offset 'carry' ignores is the same: without it 'carry'
-- is lazy in its offset, 'go' boxes it for the one call a level makes,
-- and the heap check for that box sits at the head of 'go' and is paid
-- every run.
{-# INLINE runSlicesT #-}
runSlicesT :: forall v a b. (Vector v, VecElem v a)
           => Axes -> Int -> v a -> (v a -> b -> b) -> b -> b
runSlicesT (Axes _ n (InnerFirst outerAxes)) !start !v cons nil =
  case outerAxes of
    [] -> cons (vSlice start n v) nil
      -- Currently impossible: 'routeOfT' sends a view of one run to
      -- 'RSlice', where it is the vector or one slice of it.
    (!sk, !dk) : above ->
      let go :: Int -> Int -> [(Int, Int, Int)] -> b
          go !i !o outer
            | i < dk = cons (vSlice o n v) (go (i + 1) (o + sk) outer)
            | otherwise = carry outer (o - dk * sk) []
          carry :: [(Int, Int, Int)] -> Int -> [(Int, Int, Int)] -> b
          carry [] !_ _ = nil
          carry ((j, d, s) : rest) !o reset
            | j + 1 < d =
                go 0 (o + s) (foldl' (flip (:)) ((j + 1, d, s) : rest) reset)
            | otherwise = carry rest (o + s - d * s) ((0, d, s) : reset)
      in  go 0 start [ (0, d, s) | (s, d) <- above ]

-- Convert an array to a list of vectors, which together contain
-- all the elements in the natural order.
--
-- An invariant: the returned list has no empty vectors, an empty
-- array yielding the empty list.
--
-- The list is produced lazily: a consumer folds it slice by slice,
-- holding no more of it than it has reached, where a table of the
-- runs' offsets would do all its work before the consumer sees an
-- element.  Written under one 'build' with the dispatch inside
-- it, so that a fold applied to this list fuses with it whichever case
-- the view takes.
{-# INLINE toVectorListT #-}
toVectorListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [v a]
toVectorListT sh a@(T _ _ v) = build $ \cons nil ->
  if l == 0 then nil else routeSlicesT v (routeT sh l a) cons nil
  where !l = product sh

-- The slice of the vector an 'RSlice' route stands for, at an offset
-- and of a length: the vector itself where the slice is all of it, so
-- that a dense array's conversion hands back no new header.
{-# INLINE wholeOrSliceT #-}
wholeOrSliceT :: (Vector v, VecElem v a) => Int -> Int -> v a -> v a
wholeOrSliceT ao l v
  | ao == 0 && vLength v == l = v
  | otherwise = vSlice ao l v

-- The slices a route stands for, as the cons and nil of a 'build': one
-- slice of the vector, one slice per run, or the view filled as one
-- vector where no run is longer than one element.
{-# INLINE routeSlicesT #-}
routeSlicesT :: (Vector v, VecElem v a)
             => v a -> Route -> (v a -> b -> b) -> b -> b
routeSlicesT v route cons nil = case route of
  RSlice ao l -> cons (wholeOrSliceT ao l v) nil
  RRuns axes ao _ -> runSlicesT axes ao v cons nil
  RFill axes ao l ->
    -- No slice can be taken.  Fill the result through 'vFillStrided',
    -- whose vector-backed instances write a mutable buffer directly.
    cons (vFillStrided axes ao l v) nil

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
toVectorT sh a@(T _ _ v)
  | l == 0 = vConcat []
  | otherwise = routeVectorT v (routeT sh l a)
  where !l = product sh

-- The vector a route stands for: one slice of the vector, or the view
-- filled as one vector, runs included.  'toVectorT' and
-- 'toUnorderedVectorT' both take it.
{-# INLINE routeVectorT #-}
routeVectorT :: (Vector v, VecElem v a) => v a -> Route -> v a
routeVectorT v route = case route of
  RSlice ao l -> wholeOrSliceT ao l v
  RRuns axes ao l -> vFillStrided axes ao l v
  RFill axes ao l -> vFillStrided axes ao l v

-- The (absolute stride, extent) pairs of the axes of extent above 1,
-- in the order given, and the offset of the view's lowest address, in
-- one walk over the strides and the shape; the view is non-empty,
-- which the caller has checked, so no extent is 0.  The account after
-- 'unorderedRouteT' says why one walk and why each of the three.
absAxesAndStartT :: Int -> [Int] -> ShapeL -> ([(Int, Int)], Int)
absAxesAndStartT ao = go
  where
    go :: [Int] -> ShapeL -> ([(Int, Int)], Int)
    go (s : ss) (n : ns)
      | n == 1 = go ss ns
      | s < 0 = case go ss ns of
          (axes, !start) -> ((negate s, n) : axes, start + (n - 1) * s)
      | otherwise = case go ss ns of
          (axes, !start) -> ((s, n) : axes, start)
    go _ _ = ([], ao)
{-# INLINE absAxesAndStartT #-}

-- Absolute stride descending; on a tie at stride 1 the length 'runRank'
-- prefers last, so that it is the run, and on any other tie the extent
-- ascending.
--
-- In case form rather than over '<>', and the strides banged and
-- the extents not, as measured: the '<>' form retired 42 to 128
-- instructions a call more than this, and a bang on the extents 69 to
-- 162 more, the tie branch being the one most comparisons never reach.
-- 'sortBy' calls the comparator unknown, so a banged field is an unbox
-- at every entry.
byStrideRank :: (Int, Int) -> (Int, Int) -> Ordering
byStrideRank (!s1, n1) (!s2, n2) = case compare s2 s1 of
  EQ | s1 == 1 -> runRank n2 n1
     | otherwise -> compare n1 n2
  o -> o

-- The corners of the curve of a reducing consumer's cost per element
-- against the run length, measured on one machine: where the plateau
-- begins, where it ends, and the shelf's end, past which a run loses
-- to a run of 3.
runLo, runHi, runFar :: Int
runLo = 5
runHi = 32
runFar = 96

-- Which of two run lengths a reducing consumer prefers, LT the faster:
-- by tier, the plateau, the shelf above it, runs of 3 and 4, the climb
-- past the shelf, then 2 and 1; and within a tier the longer on the
-- plateau and among the short runs, where the rate falls or is flat,
-- and the shorter on the shelf, which rises across its width, and on
-- the climb.
runRank :: Int -> Int -> Ordering
runRank !a !b = case compare ta tb of
  EQ | ta == 1 || ta == 3 -> compare a b
     | otherwise -> compare b a
  o -> o
  where
    !ta = tier a
    !tb = tier b
    tier :: Int -> Int
    tier n
      | n <= 2 = 4
      | n < runLo = 2
      | n <= runHi = 0
      | n <= runFar = 1
      | otherwise = 3
{-# INLINE runRank #-}

-- The merged axes, innermost first, with their zero-stride axis, if
-- they begin with one followed by a unit-stride axis, moved to the end.
zeroStrideOutermost :: InnerFirst -> InnerFirst
zeroStrideOutermost (InnerFirst ((0, z) : axes@((1, _) : _))) =
  InnerFirst (axes ++ [(0, z)])
zeroStrideOutermost axes = axes

-- The route of a non-empty view with its axes reordered for a consumer
-- that owes no order, from the offset the reordered view starts at:
-- what the two unordered entry points dispatch on.  The account below
-- says why each piece.
{-# INLINE unorderedRouteT #-}
unorderedRouteT :: ShapeL -> Int -> T v a -> Route
unorderedRouteT sh l (T ats ao _) =
  let (axes, !start) = absAxesAndStartT ao ats sh
      merged = InnerFirst (foldl' mergeInner [] (sortBy byStrideRank axes))
  in  routeOfT start l (zeroStrideOutermost merged)

-- The dispatch of 'unorderedRouteT', piece by piece.
--
-- Overview.  A consumer that folds with a commutative and associative
-- operation needs the view's elements as a multiset, not in order.  So
-- the axes may be reordered freely, a reversed axis may be walked
-- forwards, and the question is only which slices of the vector, taken
-- together, hold each element as often as the view holds it.  The
-- answer: sort the axes by stride, merge the axes that are walked as
-- one, move a broadcast axis outermost, and read the route off what
-- is left, one slice, runs, or a fill.  The passes over the axes are
-- ordered so that each sees as few axes as it can, and the account
-- below takes them in the order they run.
--
-- Why one walk first.  Three things are read off the shape and the
-- strides as given: which axes have extent 1, the absolute value of
-- each stride, and the start offset (below).  Each is a pass over the
-- two lists, and 'absAxesAndStartT' takes all three in one, returning
-- the (absolute stride, extent) pairs of the axes that matter with the
-- start offset beside them.
--
-- Why drop the axes of extent 1 before the sort.  An axis of extent 1
-- selects one index and is walked no distance, so its stride says
-- nothing about which cells are touched, and canonicalization drops it
-- whatever its stride.  Dropped before the sort, it leaves the sort
-- fewer axes to order, and on a view where such an axis shares a stride
-- with another --- the channel axis of a one-channel convolution patch,
-- extent 1 at the output axis's stride --- the sort meets no tie and
-- has no order to undo, where a sort that meets one pays several
-- hundred instructions to reorder five axes.  A zero stride on such an
-- axis goes with it, so no later test has to see past it.
--
-- Why abs.  A negative stride walks an axis backwards over the same
-- cells a positive one walks forwards.  Order is not asked for here, so
-- only the magnitude says which cells are touched; the sign is used
-- once, in the same walk, to find where the lowest address is.
--
-- Why start.  The slices, or the fill, must begin at the block's
-- lowest address, and the offset ao is not it: ao is where index
-- (0, ..., 0) sits, which is the lowest address only when every stride
-- is positive.  An axis with a negative stride has its lowest address
-- at its last index, and contributes (extent - 1) * stride, a negative
-- amount.  So start is ao plus those amounts, one per reversed axis,
-- and the walk adds each as it takes the stride's absolute value, the
-- sign being in hand there and nowhere later.
--
-- Why sort.  A transposition reorders the axes and their strides
-- together without changing which cells are touched (an index sum does
-- not care about the order of its terms).  Sorting by stride magnitude,
-- descending, puts the axes from outermost to innermost, which is the
-- order in which two axes walked as one stand next to each other, and
-- in which the innermost axis, the run, is last.  'byStrideRank' is
-- that order.  Equal strides alias, one step along either axis reading
-- the same element, so a tie exists only in a self-overlapping view, a
-- window over an array among them; on a tie at stride 1 the comparator
-- puts the axis whose extent makes the better run innermost, and on
-- any other tie the shorter axis outside.
--
-- Why the run's length is ranked.  A reducing consumer's chain of adds
-- runs at one add latency an element on a long run and overlaps the
-- next run's on a short one, so its cost per element falls from the
-- shortest runs to a plateau, stays flat across it, sits on a shelf
-- above it, and climbs past the shelf towards the long-run rate, with
-- runs of 3 and 4 a hair above the shelf.  'runRank' orders the tiers
-- and the lengths within them; its corners are one machine's, and a
-- tie at stride 1 is the only place they decide anything.
--
-- Why merge after the sort.  Two adjacent axes are one axis when the
-- outer stride is the inner stride times the inner extent: walking the
-- inner axis to its end and stepping the outer axis once lands where
-- one axis of the combined extent would.  'mergeInner' merges every
-- such pair.  Done after the sort, the merge finds every pair the sorted
-- order stands next to each other, which in a view without a stride
-- tie is every pair any order of the axes would have put together; a
-- view that is one block of the vector has no tie, so it merges to a
-- single axis of stride 1 and reads as one slice, whatever order its
-- axes came in, and 'routeOfT' decides that off the merged form with
-- no stride list built.
--
-- Why the zero-stride axis moves outermost, and why after the merge.
-- A broadcast axis, stride 0, reads the same cells at every index.
-- Sorted by stride it lands innermost, and there it makes the route a
-- fill, each element copied as many times as the broadcast repeats it.
-- Moved outermost over a unit-stride axis it makes the route runs:
-- the runs walk repeats one slice as many times, the same multiset
-- with nothing copied, and the fill writes the block once and copies it
-- by doubling.  Decided after the merge, the move is one look at the
-- first two merged axes, innermost first: a zero stride merges with
-- nothing but another zero stride, so there is at most one such axis,
-- and it sorts after every other stride, so it is innermost, the head;
-- and a unit-stride axis worth moving it over is the one after it.
-- 'zeroStrideOutermost' does the look and the move.

-- Convert to a list of vectors containing altogether the right elements,
-- but not necessarily in the right order.
-- This is used for reduction with commutative&associative operations.
--
-- This is over-optimized: the dispatch is long, its order of passes is
-- tuned, and it carries three magic constants read off one machine.
-- The two milder versions in the commit history --- a one-block test
-- with a fall-back, then the sorted axes with a guarded move --- were
-- already hard to follow and needed a battery of implementation notes
-- each, so this one is at least really sharp, and the account at
-- 'unorderedRouteT' says why each piece.
--
-- An invariant: the returned list has no empty vectors, an empty
-- array yielding the empty list; the minimum/maximum operations rely
-- on it.  The list is produced lazily, as 'toVectorListT''s is, so 'anyT'
-- and 'allT' stop at the first slice that decides.
{-# INLINE toUnorderedVectorListT #-}
toUnorderedVectorListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [v a]
toUnorderedVectorListT sh a@(T _ _ v) = build $ \cons nil ->
  -- Under one 'build' with the dispatch inside it, as 'toVectorListT'
  -- is and for the same reason: written as a case returning a list per
  -- branch, a fold over this list would meet the case and never fuse.
  if l == 0 then nil else routeSlicesT v (unorderedRouteT sh l a) cons nil
  where !l = product sh

-- Convert to one vector holding all the elements, not necessarily in
-- the right order.  Dispatches as 'toUnorderedVectorListT' does and
-- takes the vector as 'toVectorT' does: a view of runs is filled, a
-- repeated block once and then copied by doubling, where the list would
-- hand one slice per repeat to a concatenation.
{-# INLINE toUnorderedVectorT #-}
toUnorderedVectorT :: (Vector v, VecElem v a) => ShapeL -> T v a -> v a
toUnorderedVectorT sh a@(T _ _ v)
  | l == 0 = vConcat []
  | otherwise = routeVectorT v (unorderedRouteT sh l a)
  where !l = product sh

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
allSameT sh t@(T _ ao v)
  | vLength v <= 1 = True
  | otherwise =
    -- Order does not matter, so the unordered list, which is one slice
    -- for a dense view under any transposition.  The element at index
    -- zero sits at the offset, so no slice is held for it; it is not
    -- forced here because an empty view has no element there and never
    -- asks for it.  The fold sits on the list expression, where it
    -- fuses with the walk and stops at the first element that differs.
    let x = vIndex v ao
    in  all (vAll (x ==)) (toUnorderedVectorListT sh t)

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
