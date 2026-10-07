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
{-# LANGUAGE CPP #-}
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
#if !MIN_VERSION_base(4,20,0)
import Data.List(foldl')
#endif
import Data.List(zipWith4, zipWith5, sortBy, sortOn, foldl1')
import Data.Ord(comparing)
import Data.Proxy
import qualified Data.Vector.Generic as VG
import qualified Data.Vector.Generic.Mutable as VGM
import GHC.Exts(Constraint, SpecConstrAnnotation(..), build)
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
  -- | The vectors' elements, in order, in a new vector, which shares no
  -- buffer with them even when there is one: 'normalize' relies on it to
  -- copy an array out of a larger vector.
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

  vFromListN n = vFromList . take n

  -- | Materialize a strided view in row-major order.  The arguments are
  -- the view's canonical axes (as t'Axes'), the offset, the total element
  -- count and the source vector.  The contract: every extent in the axes
  -- is positive, the count is their product (@product sh@, passed in
  -- because every caller already has it), and every element the axes
  -- address from the offset lies in the source vector.  The vector-backed
  -- instances check none of it, but for an assertion of a positive count
  -- that an optimised build drops unless asserts are kept, and read and
  -- write unchecked, so a call that breaks it reads outside the source or
  -- writes outside the result, which can corrupt memory.  This method is
  -- what makes a fast 'toVectorListT' and
  -- 'toVectorT' possible: what the conversions to vectors do not hand
  -- out as slices of the source they fill through it, over the
  -- view's canonical axes ('routeT'), and the fast fills
  -- write a mutable result buffer across runs, which no existing
  -- method can express ('vGenerate' is stateless).
  --
  -- The default lists the view's elements as 'toListT' does ('elemsT') and
  -- builds its result from that list.  The vector-backed instances override it
  -- with the faster mutable fill 'genericFillStrided', each passing the run
  -- length from which it copies runs whole.  An instance that keeps the
  -- default fills element by element every view that is not one slice,
  -- runs of a contiguous view included, which 'toVectorT' and the
  -- operations built on it then pay: override it, with
  -- 'genericFillStrided' where the vector type is an instance of
  -- 'Data.Vector.Generic.Vector', or risk their slowness on such views.
  vFillStrided :: (VecElem v a) => Axes -> Int -> Int -> v a -> v a
  vFillStrided axes !ao l !v = vFromListN l (elemsT axes ao v (:) [])

  -- | Concatenate parts whose lengths sum to the count given first, which every
  -- caller already has.  The default returns a lone part of that length as it
  -- is and otherwise is 'vConcat', reading the count for nothing else.  The
  -- Storable and Unboxed instances override it with 'genericConcatN', which
  -- copies each part as the list yields it; the boxed one keeps the default and
  -- says why.
  vConcatN :: (VecElem v a) => Int -> [v a] -> v a
  vConcatN n [v] | vLength v == n = v
  vConcatN _ vs = vConcat vs

  -- | Hand the element at an index to a continuation, read as the instance
  -- chooses.  The list of a view's elements that 'elemsT' builds holds what it
  -- is handed.  The default hands on 'vIndex' unevaluated, a thunk holding the
  -- vector; the boxed vector instance hands on the element stored, unforced,
  -- and the Storable and Unboxed ones the element read and forced, as none of
  -- theirs is undefined.
  vWithElem :: (VecElem v a) => v a -> Int -> (a -> r) -> r
  vWithElem v i k = k (vIndex v i)

class None a
instance None a

-- This instance serves as a reference semantics.  Pretty-printing also uses it,
-- for the array of rendered elements.
instance Vector [] where
  type VecElem [] = None
  vIndex = (!!)
  vLength = length
  vToList = id
  vFromList = id
  vFromListN = take
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
  -- Fails on a slice out of range, as the vector instances do; on one the
  -- list runs out in, only where its end is forced.
  vSlice o n xs
    | o < 0 || n < 0 = bad
    | otherwise = let ys = dropN o xs in ys `seq` takeN n ys
    where bad = error $ "vSlice: violated contract: invalid slice " ++ show (o, n, length xs)
          dropN 0 ys = ys
          dropN k (_ : ys) = dropN (k - 1) ys
          dropN _ [] = bad
          takeN 0 _ = []
          takeN k (y : ys) = y : takeN (k - 1) ys
          takeN _ [] = bad
  vSum = sum
  vProduct = product
  vMaximum = maximum
  vMinimum = minimum
  vUpdate xs us = loop xs (sortOn fst us) 0
    where
      loop [] [] _ = []
      loop [] (_:_) _ = error "vUpdate: violated contract: index out of bounds"
      loop as [] _ = as
      loop (a:as) ias@((i,a'):ias') n =
        case compare i n of
          LT -> error "vUpdate: violated contract: bad index"
          EQ -> loop (a':as) ias' n  -- the last update at n stays, as in (//)
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
--
-- The functions here have contracts, which the operations of the array
-- modules establish before calling them. A call that breaks one is a bug:
-- where a contract is checked, the error says "violated contract", or an
-- assert fails. An argument a caller keeping every contract can pass, and
-- that has no result, is checked in the operation that takes it, before any
-- contract check and before any call that relies on it, and the error names
-- that operation.
type role T representational nominal
data T v a = T
    { strides :: ![Int]   -- length is tensor rank
    , offset  :: !Int     -- offset into vector of values
    , values  :: !(v a)   -- actual values
    }
    deriving (Show, Generic, Data)

-- TODO: rnf forces the whole vector, elements outside the view included,
-- and so do the generic arrays' instances, whose contexts lack the
-- Vector v and VecElem v a that 'rnfViewT' needs, and the Shaped one's
-- also the Shape sh its shape needs.  The boxed arrays' force only the
-- view, by 'rnfViewT'.
instance NFData (v a) => NFData (T v a)

-- The elements of the view, of the shape given, reduced to normal form,
-- and no element outside it: the part of the vector it reads where it
-- reads every element of one part, and otherwise its elements without
-- its broadcast dimensions, which repeat what the rest holds.
{-# INLINE rnfViewT #-}
rnfViewT :: (Vector v, VecElem v a, NFData a, NFData (v a)) => ShapeL -> T v a -> ()
rnfViewT sh t@(T _ _ v) = case readRangeT sh t of
  Just (lo, n) -> rnf (vSlice lo n v)
  Nothing -> let (_, rsh, r) = dropBroadcastT sh t
             in  foldr (\ x z -> rnf x `seq` z) () (toListT rsh r)

-- | The shape of an array is a list of its dimensions.
type ShapeL = [Int]

-- A shape with a negative extent, or with more elements than an Int counts.
-- After an extent of 0 only a negative one makes the shape bad,
-- and after the size passes maxBound so does the lack of a 0 to follow.
badShape :: ShapeL -> Bool
badShape = go 1
  where go !_ [] = False
        go !n (s : ss) | s < 0 = True
                       | s == 0 = any (< 0) ss
                       | n > maxBound `quot` s = any (< 0) ss || 0 `notElem` ss
                       | otherwise = go (n * s) ss

-- The sum of non-negative extents, or -1 where it is past 'maxBound', where
-- an extent made by adding them would wrap.  A foldr, so that a list built
-- to be summed, a literal or a map, fuses with it and is never allocated.
{-# INLINE sumExtents #-}
sumExtents :: [Int] -> Int
sumExtents ss = foldr (\ s k !n -> if n > maxBound - s then -1 else k (n + s)) id ss 0

-- Whether non-negative extents sum past 'maxBound'.
{-# INLINE sumOverflows #-}
sumOverflows :: [Int] -> Bool
sumOverflows ss = sumExtents ss < 0

-- Compare two arrays of the same shape, the first argument, element by element,
-- stopping at the first element that differs.  Two views of the same strides
-- read their vectors alike, from offsets that may differ: where they read every
-- element of one part of their vectors ('readRangeT') they compare the two
-- parts, and where they do not they compare their views without the broadcast
-- dimensions, which repeat what the rest holds, part by part along the route
-- ('routePartsT'), a part being a run or, where the uniform run length is one
-- element, an element.  Otherwise two views that are one slice each compare as
-- the slices, a view and a slice as the view's parts against the slice from its
-- start on, and any other pair as the first view's parts against the second
-- normalized, a slice of its own.  The index loops allocate nothing, a walk
-- against a slice 16 bytes a part, and no case reads an element outside the
-- views or materializes one but the last, which copies the second.
--
-- The parts that two views of the same strides read whole are compared
-- in the order of the vectors, not of the views, so where they hold an
-- undefined element, x == y can fail on it where compare x y, which
-- follows the views, returns.
--
-- The loops are written out rather than taken from the vectors'
-- own '==', which on two Storable vectors of 60000 Doubles, on GHC
-- 9.12.4, took ten times the index loop's time at -O2 and allocated 56
-- bytes an element, 72 at -O1.  That '==' is vector-stream's 'eqBy'
-- (vector-stream-0.1.0.1 under vector-0.13.2.0), and Storable's
-- 'basicUnsafeIndexM' leaves the element read unevaluated, so the inner
-- step of 'eqBy' receives every element of the first vector as a thunk
-- and then boxes it (https://github.com/haskell/vector/issues/570); a
-- copy of 'eqBy' with that argument banged took twice the index loop's
-- time at -O2 and allocated nothing.  The 16 bytes an element it kept
-- at -O1 are the first vector's index, passed boxed between the two
-- steps, which 'eqBy''s SPEC arguments leave to SpecConstr to unbox, a
-- pass -O1 does not run; and 'eqBy', an unfolding, is compiled where
-- it is used, at this package's -O1, whatever vector itself is built
-- with.  So -fspec-constr would take only a quarter off the vectors'
-- '==', the thunk remaining.  'compare' is vector-stream's 'cmpBy', of
-- the same shape and, from GHC 9.12 on, the same cost, hence the loop
-- in 'compareT'.
{-# INLINE equalT #-}
equalT :: (Vector v, VecElem v a, Eq a) => ShapeL -> T v a -> T v a -> Bool
equalT s x@(T _ _ vx) y@(T _ _ vy)
  | l == 0 = True
  | strides x == strides y = case readRangeT s x of
      Just (lo, n) -> go lo (lo + d) n
      Nothing -> let (_, rs, x') = dropBroadcastT s x
                 in  routePartsT (routeT rs (product rs) x')
                                 (\p n rest -> go p (p + d) n && rest) True
  | otherwise = case (routeT s l x, routeT s l y) of
      (RSlice ox _, RSlice oy _) -> go ox oy l
      (rx, RSlice oy _) ->
        routePartsT rx (\p n rest !q -> go p q n && rest (q + n))
                    (const True) oy
      (RSlice ox _, ry) ->
        routePartsT ry (\p n rest !q -> go q p n && rest (q + n))
                    (const True) ox
      (rx, _) -> let !(T _ oz vz) = normalizeT s y
                 in  routePartsT rx (\p n rest !q -> goWith vz p q n && rest (q + n))
                                 (const True) oz
  where
    !l = product s
    !d = offset y - offset x
    go :: Int -> Int -> Int -> Bool
    go = goWith vy
    goWith !w !ox !oy !k = loop 0
      where loop !i = i >= k || (vIndex vx (ox + i) == vIndex w (oy + i)
                                 && loop (i + 1))

-- Compare two arrays of the same shape lexicographically in row-major order:
-- two views of the same strides part by part along the route of their views
-- without the broadcast dimensions, as 'equalT' does where they read no part
-- whole, two views that are one slice each by index, a view and a slice as
-- 'equalT' compares them, and any other pair as 'equalT' does.  Without the
-- broadcast dimensions the order is kept: the first element that differs in the
-- views is the first one that differs in what remains.
{-# INLINE compareT #-}
compareT :: (Vector v, VecElem v a, Ord a)
            => ShapeL -> T v a -> T v a -> Ordering
compareT s x@(T _ _ vx) y@(T _ _ vy)
  | l == 0 = EQ
  | strides x == strides y =
      let (_, rs, x') = dropBroadcastT s x
      in  routePartsT (routeT rs (product rs) x')
                      (\p n rest -> case go p (p + d) n of
                                      EQ -> rest
                                      o -> o)
                      EQ
  | otherwise = case (routeT s l x, routeT s l y) of
      (RSlice ox _, RSlice oy _) -> go ox oy l
      (rx, RSlice oy _) ->
        routePartsT rx (\p n rest !q -> case go p q n of
                                          EQ -> rest (q + n)
                                          o -> o)
                    (const EQ) oy
      (RSlice ox _, ry) ->
        routePartsT ry (\p n rest !q -> case go q p n of
                                          EQ -> rest (q + n)
                                          o -> o)
                    (const EQ) ox
      (rx, _) -> let !(T _ oz vz) = normalizeT s y
                 in  routePartsT rx (\p n rest !q -> case goWith vz p q n of
                                                      EQ -> rest (q + n)
                                                      o -> o)
                                 (const EQ) oz
  where
    !l = product s
    !d = offset y - offset x
    go :: Int -> Int -> Int -> Ordering
    go = goWith vy
    goWith !w !ox !oy !k = loop 0
      where loop !i
              | i >= k = EQ
              | otherwise =
                  case compare (vIndex vx (ox + i)) (vIndex w (oy + i)) of
                    EQ -> loop (i + 1)
                    o -> o

-- Given the dimensions, return the stride in the underlying vector
-- for each dimension.  The first element of the list is the total length.
{-# INLINE getStridesT #-}
getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

-- Convert an array to a list of its elements in row-major order.
-- The first argument is the array shape.
--
-- Dispatches on 'routeT' as 'toVectorListT' does: an 'RSlice' lists its
-- slice, an 'RRuns' each run's slice as 'runSlicesT' reaches it, and an
-- 'RFill' its elements one by one over the canonical axes ('elemsT'),
-- where a fill followed by 'vToList' would materialize the whole array
-- before the first element.  So the list is lazy on every route: a
-- consumer that stops early walks only a prefix, and the 'build' form
-- fuses with a consumer that sees it inlined.  The run slices stay
-- because the element walk steps the odometer once a run, which on
-- short runs costs more than a slice header: 2.7 times the time of a
-- fused 'sum' at runs of two.
{-# INLINE toListT #-}
toListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [a]
toListT sh a@(T _ _ v)
  | l == 0 = []
  | otherwise = case routeT sh l a of
      RSlice ao _ -> vToList (wholeOrSliceT ao l v)
      RRuns axes ao _ -> build $ \cons nil ->
        runSlicesT axes ao v (\s rest -> foldr cons rest (vToList s)) nil
      RFill axes ao _ -> build $ \cons nil -> elemsT axes ao v cons nil
  where !l = product sh

-- The start and length of the part of the vector the array reads, if it reads
-- every element of one part, broadcasts and overlapping windows included, and
-- Nothing if it reads no element or skips one.  Leaving out the dimensions of
-- stride 0 or size 1 and taking the others by increasing absolute stride, the
-- array reads one part if each absolute stride is at most one more than the
-- reach of those before it.
{-# INLINE readRangeT #-}
readRangeT :: ShapeL -> T v a -> Maybe (Int, Int)
readRangeT sh (T ats ao _)
  | product sh == 0 = Nothing
  | otherwise = go 0 (sortBy (comparing fst) [ (abs t, s) | (t, s) <- tss ])
  where tss = [ (t, s) | (t, s) <- zip ats sh, t /= 0, s /= 1 ]
        lo = ao + sum [ (s - 1) * t | (t, s) <- tss, t < 0 ]  -- lowest index read
        go !hi [] = Just (lo, hi + 1)
        go !hi ((t, s) : sts) | t <= hi + 1 = go (hi + (s - 1) * t) sts
                              | otherwise = Nothing

-- The array without its broadcast dimensions, of stride 0 and positive
-- extent, which repeat one subarray: which dimensions those are, and the
-- shape and the view of the rest.
{-# INLINE dropBroadcastT #-}
dropBroadcastT :: ShapeL -> T v a -> ([Bool], ShapeL, T v a)
dropBroadcastT sh (T ats ao v) =
  (bs, [ s | (b, s) <- zip bs sh, not b ], T [ t | (b, t) <- zip bs ats, not b ] ao v)
  where bs = zipWith (\ s t -> t == 0 && s > 0) sh ats

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

-- The measured-fastest fill for 'vFillStrided': an allocate-once mutable
-- result, an odometer recursion over the outer dimensions with the input offset
-- stepped additively, the innermost outer level fused into a dedicated loop
-- over the innermost runs, and the innermost-run fill unrolled by two with its
-- bound on the output cursor, so it is sound for zero and negative strides, or,
-- from a run length the instance picks, each run at stride 1 copied whole.  The
-- recursion walks the outer levels as a 'Nest' built over them innermost first,
-- each level holding its 'Axis'.
--
-- Two zero-stride conditions sit inside it, neither decided per element:
-- an innermost run at stride 0, decided once a fill, reads its one element
-- once and stores it, and an outer level of stride 0, decided per level of
-- the odometer, fills the block below it once and copies it onto the level's
-- remaining positions by doubling.  Given canonical dimensions ('routeT') the
-- conditions fire wherever they can; given any other dimensions the fill is
-- still correct.
--
-- A run at stride 1 of @copyRun@ elements or more is copied whole, by one
-- 'VG.unsafeCopy' a run.  The copy rides on the stride-1 branch below, which
-- already re-derives 'RRuns' from the axes; that hack is what lets each
-- instance pick @copyRun@ and tune the copy per kind of vector.  A boxed
-- element's store pays GHC's write barrier, a store to the array's header, a
-- card marked and a test for the nonmoving collector, which the copy pays once
-- a run.  Boxed vectors copy runs of 5 elements or more: on 200000 elements
-- the copy is 1.2 times faster than the stepping loop on runs of 6 and 3.4
-- times on runs of 1000 or more, and level with it on runs of 4.  Storable and
-- Unboxed stores pay no barrier.  Storable vectors copy runs of 512 bytes or
-- more and Unboxed ones, whose element size the class does not give, runs of 64
-- elements: well past where a copy's cost a run is paid off, rather than where
-- this machine's figures would put the cut.  On views of 20000 to 100000000
-- Doubles a copy of every run took 0.6 to 1.6 of the stepping loop's time at
-- both kinds: faster on runs of 64 to 4096 in views of 20000 and 200000 and on
-- runs past glibc's non-temporal threshold of 24 MiB, slower on runs of 5 and
-- up to 10% slower on runs of 4096 to 1048576 in views of 10000000 to 100000000
-- Doubles.  Measured on Zen 3.
--
-- The count must be positive, asserted at entry: a zero-stride
-- innermost run reads its one element, and a zero-stride level writes
-- its innermost run or block, before reading the extent, so a zero
-- extent would read past the source or write into an empty result.
-- Every entry point of this module returns the empty vector or list
-- before routing an empty view here, and a caller of 'vFillStrided'
-- from outside owes the same.
--
-- Written once against 'Data.Vector.Generic', which supplies
-- the mutable machinery orthotope's own 'Vector' class deliberately does
-- not; each vector-backed instance reuses it verbatim.  Ported
-- bang-for-bang from the fastest fill of the micro-benchmark preserved
-- at https://github.com/Mikolaj/orthotope/tree/speedup-strided-tovector/micro-regime3/
-- as of the commit "Read the runs' elements as genericFillStrided does" (the
-- bang patterns are part of what was measured), but for the count's bang, whose
-- removal shrinks the -O1 Core, and for the copied run; one choice made for the
-- NCG, marked at the line it is on, costs -fllvm a little.
--
-- The implementation is similar to what once was in orthotope file
-- FastReshape.hs (a Storable-only odometer flatten behind an unsafeCast to
-- Double or Float, never in the cabal file, removed once subsumed by this).
--
-- INLINABLE, so that a client specialises the fill at most once per
-- instance of 'Vector' and element type instead of inlining it at
-- every call.  Exposing it instead by -fexpose-overloaded-unfoldings,
-- with no pragma, waits until clients routinely build with
-- -fspecialise-aggressively, without which they specialise only what is
-- marked INLINABLE, and until GHC's exitification in this module stops
-- leaving the exposed loop's exit holding the boxed cursors, which a
-- client's specialisation then keeps boxed: a box an element, as seen with
-- GHC HEAD 10.1 (https://gitlab.haskell.org/ghc/ghc/-/work_items/27893).
{-# INLINABLE genericFillStrided #-}
genericFillStrided :: forall w a. (VG.Vector w a)
                   => Int -> Axes -> Int -> Int -> w a -> w a
genericFillStrided !copyRun (Axes stInner nInner outerAxes) !ao l !v =
  assert (l > 0) $ VG.create fill
 where
  fill :: forall s. ST s (VG.Mutable w s a)
  fill = do
    out <- VGM.unsafeNew l
    let -- The stepping run, an innermost run at nonzero stride: the
        -- source cursor advances by the stride, the fill unrolled
        -- by two.  The run bodies are INLINE so that inlining at their
        -- sites in 'walk' is the source's property and not a size
        -- threshold's.  Each element is read by 'VG.unsafeIndexM' and
        -- then stored: 'VG.unsafeIndex' as the store's argument would
        -- leave in a boxed result a thunk holding the source vector.
        {-# INLINE writeRunStep #-}
        writeRunStep :: Int -> Int -> Int -> ST s ()
        writeRunStep !st !outPos !baseOff =
          let !oEnd = outPos + nInner
              inner :: Int -> Int -> ST s ()
              inner !o !src
                | o + 1 >= oEnd =
                    if o >= oEnd then return ()
                    else VG.unsafeIndexM v src >>= VGM.unsafeWrite out o
                -- FOR THE NCG, AND A REGRESSION UNDER -fllvm.  The cursor steps
                -- twice by st instead of once by a doubled stride: one live
                -- value fewer, which is what lets the NCG's allocator keep
                -- the output base in a register instead of reloading it twice
                -- a pair.  Worth 5 to 25% of the fill's instructions there,
                -- most at long innermost runs; -fllvm needs neither, keeps two
                -- induction variables and loses 1 to 8%.  A workaround for an
                -- unidentified issue of the NCG's register allocation.
                | otherwise = do
                    VG.unsafeIndexM v src >>= VGM.unsafeWrite out o
                    let !srcNext = src + st
                    VG.unsafeIndexM v srcNext >>= VGM.unsafeWrite out (o + 1)
                    inner (o + 2) (srcNext + st)
          in  inner outPos baseOff
        -- The copied run, a run at stride 1 copied whole.
        {-# INLINE writeRunCopy #-}
        writeRunCopy :: Int -> Int -> ST s ()
        writeRunCopy !outPos !baseOff =
          VG.unsafeCopy (VGM.unsafeSlice outPos nInner out)
                        (VG.unsafeSlice baseOff nInner v)
        -- The broadcast run, the innermost run at stride 0: its one
        -- element read once, then the stores, unrolled by two as
        -- the stepping run is.  Without the unroll, a store and a
        -- compare per element read 1.20 of the stepping run serving
        -- the broadcast, a read and a store per element unrolled by
        -- two, at an innermost run of two elements; unrolled, the
        -- hoisted read wins.  The read is by 'VG.unsafeIndexM', which
        -- also keeps such a thunk out of a boxed result.
        {-# INLINE writeRunSet #-}
        writeRunSet :: Int -> Int -> ST s ()
        writeRunSet !outPos !baseOff = do
          x <- VG.unsafeIndexM v baseOff
          let !oEnd = outPos + nInner
              inner :: Int -> ST s ()
              inner !o
                | o + 1 >= oEnd =
                    if o >= oEnd then return ()
                    else VGM.unsafeWrite out o x
                | otherwise = do
                    VGM.unsafeWrite out o x
                    VGM.unsafeWrite out (o + 1) x
                    inner (o + 2)
          -- 'VG.elemseq' forces x for unboxed elements and leaves a boxed
          -- one unforced.  Specialization should simplify it to 'seq' or to
          -- nothing; where it does not, as in an instance polymorphic in
          -- 'Unbox a', it stays a call through the dictionary, which only the
          -- Core of a caller's own call at its concrete arrays shows.
          VG.elemseq v x (inner outPos)
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
        copies :: Int -> Int -> Int -> ST s ()
        copies !n !blk !src
          | n <= 1 = return ()
          | otherwise = grow blk
          where
            !end = src + n * blk
            grow :: Int -> ST s ()
            grow !have
              | src + have >= end = return ()
              | otherwise = do
                  let !len = min have (end - src - have)
                  VGM.unsafeCopy (VGM.unsafeSlice (src + have) len out)
                                 (VGM.unsafeSlice src len out)
                  grow (have + len)
        -- @n@ blocks of @blk@ elements, each written by @body@ at a
        -- base offset @st@ on from the last, or at stride 0 the first
        -- copied: the fused level's innermost runs and every level
        -- above them.
        {-# INLINE level #-}
        level :: (Int -> Int -> ST s ())
              -> Axis -> Int -> Int -> Int -> ST s ()
        level body (Axis st n) !blk !outPos !baseOff
          | st == 0 = body outPos baseOff >> copies n blk outPos
          | otherwise =
              let go :: Int -> Int -> Int -> ST s ()
                  go !k !op !boff
                    | k <= 0    = return ()
                    | otherwise = body op boff
                                  >> go (k - 1) (op + blk) (boff + st)
              in  go n outPos baseOff
              -- Where a client specialises the fill rather than
              -- inlining it, the specialised copy meets full laziness
              -- before any simplification, and a loop that mentions
              -- nothing run binds is floated out of run and becomes a
              -- heap closure, 56 to 80 bytes a call
              -- (https://gitlab.haskell.org/ghc/ghc/-/work_items/27894).
              -- This one mentions st, of the Axis that run takes out of
              -- its Nest, which is why Fused holds the innermost
              -- level's, so it stays in run and becomes a join point.
              -- Bounding it by an end computed from outPos does the
              -- same with a loop one instruction shorter, which on Zen 3
              -- ran slower where the innermost runs are two elements
              -- long.
        -- The nest built over the outer axes, innermost first: the fused
        -- level's innermost runs at its core and each level above a loop of @n@
        -- blocks of @blk@ elements around the nest below it, as data so that
        -- each level is a known call of 'run', where closures lose.  A loop
        -- of its own with the block size banged, where at -O1, which leaves
        -- SpecConstr off, a 'foldl'' over a pair carried it boxed, an 'I#' a
        -- level: 16 bytes a level and up to 58 instructions a call less.
        buildNest :: Nest -> Int -> InnerFirst -> Nest
        buildNest inner !blk axes = case innerFirst axes of
          [] -> inner
          axis@(Axis _ n) : rest ->
            buildNest (Level axis blk inner) (n * blk) (InnerFirst rest)
        -- The run body a static argument, so that each use below
        -- inlines it with the body known, and the choice between the
        -- bodies is made once per fill, never per innermost run.
        {-# INLINE walk #-}
        walk :: (Int -> Int -> ST s ()) -> ST s ()
        walk writeRun = case innerFirst outerAxes of
          [] -> writeRun 0 ao
          axis0@(Axis _ n0) : outer ->
            let run :: Nest -> Int -> Int -> ST s ()
                -- The innermost runs' loop has no register to spare, and two
                -- things nothing enforces keep it from spilling one every two
                -- elements: it advances by 'nInner' itself, where a field
                -- equal to it is one value more, and it sits in 'run', a
                -- function the fill calls, where inlined into the fill's
                -- body the result's buffer and length stay live across it
                -- (https://gitlab.haskell.org/ghc/ghc/-/work_items/27737).
                -- Each broke in a variant, 6.5 to 22% more instructions on
                -- views that take 'RFill'.
                run (Fused axis) !outPos !baseOff =
                  level writeRun axis nInner outPos baseOff
                run (Level axis blk inner) !outPos !baseOff =
                  level (run inner) axis blk outPos baseOff
            in  run (buildNest (Fused axis0) (n0 * nInner) (InnerFirst outer))
                    0 ao
    -- Contiguous runs, at stride 1, get a walk of their own: copied whole
    -- from the instance's @copyRun@ on, and below it stepped with the stride
    -- known to be 1 there and not a value 'run' holds, which, where a client
    -- specialises the fill rather than inlining it, measured a word a call less
    -- and, at boxed and Unboxed elements, an instruction or more an element,
    -- on large views 6 to 10%, before the copy took the longer runs.  The test
    -- @stInner == 1@ makes it known, not the literal: with 'stInner' in its
    -- place, a client compiled the same code on GHC HEAD.
    if stInner == 0 then walk writeRunSet
    else if stInner == 1 then
      if nInner >= copyRun then walk writeRunCopy else walk (writeRunStep 1)
    else walk (writeRunStep stInner)
    return out

-- The concatenation for 'vConcatN': one buffer of the length given, each part
-- copied into it as the list yields it, by one 'foldr', so that a part dies
-- young and a list a 'build' produces is never built.  The vector package's
-- concat walks its list twice, for the length and then to copy, so it holds
-- the list and every part before it copies any and fuses with no producer.
-- Every caller of vConcatN can hand it a lone part of the length given, as
-- concatOuter of one array and rotate along the outermost dimension do, and
-- that is returned as it is; like a view's, it can be a slice of a longer
-- vector and keep that alive.  On GHC HEAD with loop heads aligned, on 200000
-- Doubles at Storable and Unboxed elements, at allocation areas of 32 MB and
-- then of 4 MB, pad and rerank both took 0.38 to 0.68 and 0.40 to 0.49 of
-- their time on rows of 2 to 8 elements, rerank allocating 99 to 356 bytes an
-- element where it had allocated 110 to 400; on rows of 500 pad and rerank, and
-- pad on a transposed view, took 0.79 to 1.00 and 0.81 to 0.94; concatOuter
-- took 0.87 to 1.10 and 0.90 to 0.93 on four transposed views, running as many
-- instructions; and rotate along the outermost dimension took 0.54 to 0.73 at
-- 32 MB, while at 4 MB it ran 0.92 to 0.93 of the cycles alone in its process
-- but took 2.5 times as long or more in a process holding a large live heap.
-- Neither concatenation fuses with a consumer that streams the result: none of
-- vector's fusion rules fired in clients streaming what pad, concatOuter or
-- rerank return, compiled by GHC HEAD at -O1 or -O2.
{-# INLINE genericConcatN #-}
genericConcatN :: (VG.Vector w a) => Int -> [w a] -> w a
genericConcatN n [v] | VG.length v == n = v
genericConcatN n vs = VG.create $ do
  out <- VGM.unsafeNew n
  let step x k = \ !i -> do
        let !m = VG.length x
        assert (i + m <= n) $ VG.unsafeCopy (VGM.unsafeSlice i m out) x
        k (i + m)
  foldr step (\ !i -> assert (i == n) $ return ()) vs 0
  return out

-- The outer levels of a view as 'genericFillStrided' walks them: the
-- fused level's innermost runs, or a level of @n@ blocks of @blk@
-- elements at stride @st@, stride 0 copying the first, @st@ and @n@
-- the outer axes list's own 'Axis'.  A hand-rolled strict list, the
-- loop nest as data, holding the 'Axis' for readability and a word less
-- a level: up to 16 bytes a call, and nothing else measurably.  The
-- fragility 'Axes' records does not bite here: the box is the list's
-- own, built before the loop, and 'run' and 'level' only take it apart;
-- a consumer that had to build one would bring the allocation back into
-- the loop.  'Fused' holds the innermost outer level's 'Axis' too, so
-- that the loop over it mentions what 'run' takes apart (GHC #27894).
data Nest = Fused !Axis | Level !Axis !Int !Nest

-- | The route a non-empty view takes once canonicalized: what its
-- consumer does with it, which is what 'toVectorListT', 'toVectorT',
-- 'toListT', 'equalT', 'compareT' and, on the view with its axes
-- reordered, the two unordered entry points dispatch on.  A view of no
-- elements (@product sh == 0@) has no route: each of these entry points
-- answers it before computing one.
--
-- Three constructors: slice the view, walk its runs as slices, or fill a vector
-- from it.  Every route carries the offset it starts at and the element count
-- (@product sh@), which every caller has in hand, so that a consumer takes the
-- route and the vector and nothing beside them; each constructor carries what
-- its way takes and no more, and 'RRuns' serves the lists and the comparisons,
-- 'routeVectorT' filling it as it fills 'RFill'.
--
-- The system is mixed: some patterns of shape and strides are told apart
-- here, as routes, and others, or the same ones again, further down, where
-- 'genericFillStrided' tells runs from strided views by the innermost stride,
-- as 'routeOfT' does, and finds broadcasts, which no route names, in the
-- innermost axis and at each outer level.  The split was made case by case,
-- mostly for speed; no system expressing every pattern as a route was ever
-- built and optimized to compare with it, so nothing shows this one cannot
-- be bettered.  The constructors are limited throughout by what the vector
-- API underneath can express, and their set changes when that API does (e.g.,
-- a reverse copy would give a reversed contiguous view a route of its own).
-- The set does not need to change when a new pattern of shape and strides
-- arrives (e.g., windows whose runs overlap), typically one a newly added
-- array operation produces.  The performance for such new patterns may not be
-- ideal, but the routes are correct, because the uniform run length is uniquely
-- determined for every non-empty canonical view and 'routeOfT' reads the route
-- off it alone; the note at 'runSlicesT' says what the length is and is not.
data Route
  = RSlice !Int !Int
      -- ^ the canonical strides are the natural ones: one contiguous
      -- slice of the vector, at the start and of the count.  Rank 0
      -- lands here: no dimensions, no strides, one element
  | RRuns !Axes !Int !Int
      -- ^ canonical innermost stride 1 under other dimensions:
      -- contiguous runs of the innermost extent, one per canonical
      -- outer index, from the start; the count is not needed to walk
      -- them, and is what they are filled by where one vector is asked
  | RFill Axes !Int !Int
      -- ^ any other canonical view, its uniform run length one: the
      -- conversions to vectors fill it as one vector of the count, from
      -- the start, and 'toListT' and the comparisons walk it an element
      -- at a time

-- The axes are a strict field in 'RRuns' and a lazy one in 'RFill' by
-- measurement: each bang of this module was flipped alone and the -O1
-- Core compared, and the one on the axes of 'RRuns' improved it, where
-- one on those of 'RFill' did not.

-- | An axis as its stride and extent.  Each level of the odometer of
-- 'offsetsT' holds the canonical list's own axis, shared by every state
-- of the level, so that a step allocates the level and nothing else:
-- copied into the level, the two cost a word a step and a fifth more
-- allocation on windows over an array.
data Axis = Axis { axisStride :: !Int, axisExtent :: !Int }

-- SpecConstr leaves 'Axis' alone: under -fspec-constr, which -O2
-- turns on, it would unbox the axis 'sortAxesT' and 'insertAxis'
-- also cons whole, and rebuild a box at each step of the sort.  GHC
-- https://gitlab.haskell.org/ghc/ghc/-/work_items/27628 is that reboxing and
-- https://gitlab.haskell.org/ghc/ghc/-/work_items/21562 the boxity analysis
-- that would prevent it; the annotation is one GHC documents as deprecated.
{-# ANN type Axis NoSpecConstr #-}

-- | Axes innermost first: the orientation 'routeT' and
-- 'unorderedRouteT' write and every consumer of a canonical view reads.
newtype InnerFirst = InnerFirst { innerFirst :: [Axis] }

-- | The canonical axes of a non-empty view: the innermost stride
-- and extent, then the axes outside it, innermost first.  What
-- 'canonicalizeT' takes and returns and 'routeOfT', 'vFillStrided' and
-- the runs walker take, so that none of them has to find the innermost
-- axis in a list.
--
-- In effect a non-empty t'InnerFirst' with a strict head, and the head
-- is two 'Int' fields, unboxed by the type, where an '!Axis' is unboxed
-- only while no consumer keeps its box: as one it measured the same,
-- every consumer taking it apart, and as the head of the list itself,
-- t'InnerFirst' in place of this type, it cost a built t'Axis' and cons a
-- call, 35 to 48 bytes, and more instructions in all but one case.
data Axes = Axes !Int !Int InnerFirst

-- @routeT sh l a@, the route of the view of @a@ at shape @sh@ as it is,
-- requires one stride in @a@ per dimension of @sh@, @l == product sh@
-- and @l > 0@; on other arguments it fails or returns a wrong route.
--
-- It canonicalizes the view on the way.  The invariant, holding
-- before and after: for an array of shape @sh@ and strides @ats@ over
-- a vector at some offset, the canonical axes describe, over the same
-- vector and offset, an array with the same row-major element sequence
-- --- the array's elements listed with the last index varying fastest,
-- the order 'toVectorT' materializes.  Two rewrites keep it: drop the
-- dimensions of extent 1, which contribute @0 * stride@ to every index
-- whatever their stride; then merge each adjacent pair of dimensions
-- where @st_outer == n_inner * st_inner@, the index sum's own
-- distributivity, so it holds for negative strides too.  After it no
-- extent is 1 and no adjacent pair satisfies that equation.
--
-- So a dense array (its elements filling a contiguous piece of the
-- vector in row-major order) has the natural strides at whatever rank
-- it was given, and a broadcast axis (a dimension of stride 0, all its
-- indices reading one element) adjacent to another has become one with
-- it; what the walks of the innermost dimension are, and are not, is
-- said at 'runSlicesT'.  One pass of O(rank) list work.
--
-- 'routeT' answers a view of one element, rank 0 or every extent 1, as
-- one slice from that count, so no view reaches its last equation and
-- 'canonicalizeT' always meets an axis of extent other than 1.  From
-- the outermost axis on, it merges each kept axis into the one just
-- outside it, carried as its stride and extent, where that one's stride
-- is this one's stride times its extent, drops that one where the merge
-- fails and it is of extent 1, and otherwise puts the kept axis inside
-- it.  The axes are kept innermost first, as 'InnerFirst', so that the
-- innermost axis and the axes outside it are a pattern match wherever a
-- consumer takes them apart.  The loop is out of line, so that its code
-- is not copied wherever 'routeT' is inlined, and takes and returns
-- 'Axes', which worker/wrapper passes and returns unboxed; returning
-- the merged list instead cost a built innermost axis and cons a call,
-- 48 bytes, and a 'Maybe' of the merged axes, 63 to 240 bytes.
{-# INLINE routeT #-}
routeT :: ShapeL -> Int -> T v a -> Route
routeT _ 1 (T _ ao _) = RSlice ao 1
routeT (n : ns) l (T (st : sts) ao _) =
  routeOfT ao l (canonicalizeT sts ns (Axes st n (InnerFirst [])))
routeT _ _ _ =
  error "routeT: violated contract: l /= product sh, or too few strides"

-- The merge loop of 'routeT', in the view's order, which the ordered
-- result must keep, its 'Axes' last: first, GHC took each axis of
-- extent other than 1 apart twice.
canonicalizeT :: [Int] -> ShapeL -> Axes -> Axes
canonicalizeT (_ : sts) (1 : ns) !axes = canonicalizeT sts ns axes
canonicalizeT (st : sts) (n : ns) (Axes stHead nHead irest@(InnerFirst rest))
  | stHead == n * st = canonicalizeT sts ns (Axes st (nHead * n) irest)
  | nHead == 1 = canonicalizeT sts ns (Axes st n irest)
  | otherwise =
      canonicalizeT sts ns (Axes st n (InnerFirst (Axis stHead nHead : rest)))
canonicalizeT _ _ axes = axes

-- The route of a view given as its canonical axes, at a start offset
-- and of an element count, the innermost axis as its stride and
-- extent and the axes outside it innermost first: 'routeT' reads it
-- for the view as it is and 'unorderedRouteT' for the view with its
-- axes reordered, each where its merge loop ends, and each answers a
-- view with no canonical axis, one element, as one slice itself.
--
-- Decided on the canonical axes alone ('routeT'), so a unit
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
-- 'routeT' holding at every adjacent pair, and after it no pair
-- satisfies that equation, so a canonical view is natural only at rank
-- 0, or at rank 1 with stride 1.
{-# INLINE routeOfT #-}
routeOfT :: Int -> Int -> Axes -> Route
routeOfT start !l (Axes 1 _ (InnerFirst [])) = RSlice start l
routeOfT start l axes@(Axes 1 _ _) = RRuns axes start l
routeOfT start l axes = RFill axes start l

-- The slices of a view of contiguous runs, one per canonical outer
-- index in row-major order, produced on demand.  The arguments are the
-- canonical axes, the innermost at stride 1 and its extent the run
-- length, the offset of the first run and the vector, then the cons
-- and nil of the 'build' the list entry points are written under, so
-- that a consumer folding the list fuses with the walk, holds no more
-- of the list than it has reached and, stopping early, does no more of
-- the walk.  The walk is 'offsetsT' with the innermost outer axis as
-- its counter, a slice a position.
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
-- address, most of the instructions a run of two elements costs.
{-# INLINE runSlicesT #-}
runSlicesT :: forall v a b. (Vector v, VecElem v a)
           => Axes -> Int -> v a -> (v a -> b -> b) -> b -> b
runSlicesT (Axes _ n (InnerFirst outerAxes)) !start !v cons nil =
  case outerAxes of
    [] -> cons (vSlice start n v) nil
      -- Currently impossible: 'routeOfT' sends a view of one run to
      -- 'RSlice', where it is the vector or one slice of it.
    axis : above ->
      -- TODO: 'vSlice' bounds-checks every run, tests that cannot fail
      -- on a view the odometer walks, @n >= 0@ among them not even
      -- varying with the run; removing them wants an unchecked slice in
      -- the 'Vector' class.
      offsetsT axis above start (\p rest -> cons (vSlice p n v) rest) nil

-- The elements of a non-empty canonical view in row-major order, as the
-- cons and nil of a 'build': 'offsetsT' with the innermost axis as its
-- counter, an element a position.  Each element is read by 'vWithElem', which
-- leaves forcing it to the consumer at a boxed vector and forces it where
-- the instance's elements cannot be undefined.  The vector is banged as in
-- 'runSlicesT'.
{-# INLINE elemsT #-}
elemsT :: forall v a b. (Vector v, VecElem v a)
       => Axes -> Int -> v a -> (a -> b -> b) -> b -> b
elemsT (Axes t n (InnerFirst outerAxes)) !start !v cons nil =
  -- TODO: 'vWithElem' bounds-checks every element; see 'runSlicesT'.
  offsetsT (Axis t n) outerAxes start
           (\p rest -> vWithElem v p (`cons` rest)) nil

-- The offsets of a counter axis's positions under the axes outside it,
-- in row-major order, each handed to the step as the walk reaches it:
-- the loop 'runSlicesT' and 'elemsT' share.  The arguments are the
-- counter axis, the axes outside it innermost first, the start offset,
-- and the step and nil of the 'build' fold the walk is written under.
--
-- 'go' walks the counter axis with a counter and a cursor, and 'block'
-- holds the levels above it, an 'Odometer' stepped only when the
-- counter runs out.  One flat loop, and not a fold per level with
-- the rest of the list passed down as a continuation: fused with a
-- consumer's fold, the level form met at every level's exit a
-- continuation it could not see and passed the accumulator to it lazily
-- and boxed, a thunk and a box per run; here every continuation is
-- 'go', 'block' or nil, all known to the compiler, so base's own left
-- folds, 'sum' among them, see a strict known call and allocate nothing
-- per run.
--
-- The odometer is a value, each level holding its own offset and its
-- axis, the canonical list's own 'Axis'.  A carry loop before it
-- collected the levels it reset, reversed them back on and undid the
-- counter's stride arithmetic; against it the value form allocates
-- 26 to 35% less on windows over an array, retires up to 3.3% fewer
-- instructions, and on one compiler executes two fewer taken branches
-- a run on views of short runs, 'go' no longer carrying the odometer.
-- Not kept: the odometer an argument of 'go', which keeps the carry's
-- run loop on that compiler; the axes as a second list beside the
-- levels, one more value live across the run loop and 4.5% more
-- instructions than the carry on a 3x3 window over 64 channels; and the
-- initial state by 'foldl'' over the reversed axes, up to 0.5% fewer
-- instructions, not attributed, for a reverse a walk.
{-# INLINE offsetsT #-}
offsetsT :: forall b. Axis -> [Axis] -> Int -> (Int -> b -> b) -> b -> b
offsetsT (Axis sk dk) above !start step nil =
  let block :: Int -> Odometer -> b
      block o outer =
        let go :: Int -> Int -> b
            go !i !p
              | i < dk = step p (go (i + 1) (p + sk))
              | otherwise = case stepOdometer outer of
                  OdoDone -> nil
                  next@(OdoLevel oNext _ _ _) -> block oNext next
        in  go 0 o
  in  block start
            (foldr (\axis@(Axis _ d) outer -> OdoLevel start d axis outer)
                   OdoDone above)

-- The outer levels of the odometer of 'offsetsT', innermost first, each at
-- an offset, with indices left, of an 'Axis'.  A strict list,
-- hand-rolled so that a level and its cell are one object: a list cell
-- cannot unpack a strict record, so a list of level records took two
-- objects and a pointer hop a level, and two fifths more allocation on
-- windows over an array.  The tail's bang makes the initial 'foldr'
-- build the odometer whole; without it that leaves a thunk a level, 64
-- to 121 bytes an iteration on windows and under a tenth of a percent
-- in instructions.
data Odometer = OdoLevel !Int !Int !Axis !Odometer | OdoDone

-- The odometer one step on, 'OdoDone' once it has gone round.
stepOdometer :: Odometer -> Odometer
stepOdometer OdoDone = OdoDone
stepOdometer (OdoLevel o c axis@(Axis s d) outer)
  | c > 1 = OdoLevel (o + s) (c - 1) axis outer
  | otherwise = case stepOdometer outer of
      OdoDone -> OdoDone
      next@(OdoLevel oNext _ _ _) -> OdoLevel oNext d axis next

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
-- vector where the uniform run length is one element.
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

-- The parts of the vector a route reads, in the route's order, as the
-- offset and the length of each, by the step and nil of a right fold:
-- the one slice, a run at a time, or an element at a time where the
-- uniform run length is one element.
{-# INLINE routePartsT #-}
routePartsT :: Route -> (Int -> Int -> b -> b) -> b -> b
routePartsT route step nil = case route of
  RSlice ao l -> step ao l nil
  RRuns (Axes _ n (InnerFirst outerAxes)) ao _ -> case outerAxes of
    [] -> step ao n nil
    axis : above -> offsetsT axis above ao (\p rest -> step p n rest) nil
  RFill (Axes t n (InnerFirst outerAxes)) ao _ ->
    offsetsT (Axis t n) outerAxes ao (\p rest -> step p 1 rest) nil

-- Convert an array to one vector holding all the elements in the
-- natural order.  Dispatches as 'toVectorListT' does, except that a
-- view of contiguous runs is filled through 'vFillStrided' rather than
-- sliced and concatenated: in the micro-benchmark preserved at
-- https://github.com/Mikolaj/orthotope/tree/speedup-strided-tovector/micro-regime3/,
-- on runs of nine elements, the slice list ties the fill on time
-- and allocates several times the result in slice headers and list
-- cells.  Where its instance asks, the fill copies each run whole into its one
-- buffer ('genericFillStrided'): on 200000 boxed Doubles in runs of 5 to 16
-- that took 0.36 to 0.46 of the slice list's time, and the same from runs of
-- 1000.
{-# INLINE toVectorT #-}
toVectorT :: (Vector v, VecElem v a) => ShapeL -> T v a -> v a
toVectorT sh a@(T _ _ v)
  | l == 0 = vConcat []
  | otherwise = routeVectorT v (routeT sh l a)
  where !l = product sh

-- Put the array into a vector of just its elements, in the linearization
-- order.  An array whose elements lie one after another in that order in
-- its vector, whatever the strides of its dimensions of extent 1, keeps
-- the vector where they are all of it, and otherwise has them copied,
-- by vConcat of the one slice, which builds a new vector, as the class
-- requires.
{-# INLINE normalizeT #-}
normalizeT :: (Vector v, VecElem v a) => ShapeL -> T v a -> T v a
normalizeT sh t@(T ats ao v)
  | map fst dense == ts' =
    fromVectorT sh $ if vLength v == l then v else vConcat [vSlice ao l v]
  | otherwise = fromVectorT sh $ toVectorT sh t
  where dense = [ (st, s) | (st, s) <- zip ats sh, s /= 1 ]
        l : ts' = getStridesT (map snd dense)

-- The vector a route stands for: one slice of the vector, or the view
-- filled as one vector, runs included.  'toVectorT' and
-- 'toUnorderedVectorT' both take it.
{-# INLINE routeVectorT #-}
routeVectorT :: (Vector v, VecElem v a) => v a -> Route -> v a
routeVectorT v route = case route of
  RSlice ao l -> wholeOrSliceT ao l v
  RRuns axes ao l -> vFillStrided axes ao l v
  RFill axes ao l -> vFillStrided axes ao l v

-- The axes of extent above 1, their strides made absolute, onto the
-- list given in reverse of the order given, and the offset given moved
-- to the view's lowest address, in one walk over the strides and the
-- shape; the view is non-empty, which the caller has checked, so no
-- extent is 0.  The reversal is what makes 'sortAxesT' cheap: a view
-- whose axes come outermost first reaches it innermost first, and
-- each axis goes in at the head.  Which of two axes of one absolute
-- stride and one extent comes first, the only order 'byStrideRank'
-- leaves open, 'canonicalizeSortedT' treats alike.  A function
-- returning the pair, which GHC returns in registers: as a loop
-- inside 'unorderedRouteT', going on into the sort, it cost 10 to 58
-- instructions a call.  The account after 'unorderedRouteT' says why
-- one walk and why each of the three.
absAxesAndStartT :: [Axis] -> Int -> [Int] -> ShapeL -> ([Axis], Int)
absAxesAndStartT axes !off (_ : sts) (1 : ns) =
  absAxesAndStartT axes off sts ns
absAxesAndStartT axes !off (st : sts) (n : ns)
  | st < 0 =
      absAxesAndStartT (Axis (negate st) n : axes) (off + (n - 1) * st) sts ns
  | otherwise = absAxesAndStartT (Axis st n : axes) off sts ns
absAxesAndStartT axes off _ _ = (axes, off)

-- Absolute stride descending; on a tie at stride 1 the length 'runRank'
-- prefers last, so that it is the run, and on any other tie the extent
-- ascending.
--
-- In case form rather than over '<>', as measured: the '<>' form retired from
-- 42 to 128 instructions a call more than this, the tie branch being the one
-- most comparisons never reach.  A workaround for an unidentified GHC issue.
byStrideRank :: Axis -> Axis -> Ordering
byStrideRank (Axis s1 n1) (Axis s2 n2) = case compare s2 s1 of
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
{-# INLINE runRank #-}
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

-- The route of a non-empty view with its axes reordered for a consumer
-- that owes no order, from the offset the reordered view starts at:
-- what the two unordered entry points dispatch on.  The account below
-- says why each piece.
{-# INLINE unorderedRouteT #-}
unorderedRouteT :: ShapeL -> Int -> T v a -> Route
unorderedRouteT sh !l (T ats ao _) = case axes of
  a : axs -> routeOfT off l (sortAxesT a [] axs)
  [] -> RSlice off l
  where
    (axes, !off) = absAxesAndStartT [] ao ats sh

-- The sort of 'unorderedRouteT', into 'byStrideRank''s order: an
-- insertion over the walk's list, the outermost axis so far held apart
-- from the rest, each axis after every axis it ranks after, so one
-- comparison an axis where the walk's list is already in reverse order;
-- at the end it enters the merge loop with the held axis as the merge's
-- first, so the sorted axes are never one list.  Both loops are out of
-- line, as 'canonicalizeT' is, and return 'Axes', which worker/wrapper
-- returns unboxed.  As measured against 'sortBy', which compiles to a
-- merge sort calling the comparator through a closure, into a merge loop
-- local to the route: 22 to 1250 instructions a call fewer on every view
-- measured, and up to 856 bytes fewer, none more.  Returning the sorted
-- list for the route to take apart cost 40 to 249 instructions and 22 to
-- 97 bytes more on every view, and inserting during the walk, which meets
-- the axes outermost first and so put each at the end, 111 to 697
-- instructions more than 'sortBy' on views of rank 5 to 7.
sortAxesT :: Axis -> [Axis] -> [Axis] -> Axes
sortAxesT h !rest (x : xs)
  | GT <- byStrideRank x h = sortAxesT h (insertAxis x rest) xs
  | otherwise = sortAxesT x (h : rest) xs
sortAxesT (Axis st n) rest [] =
  canonicalizeSortedT rest (Axes st n (InnerFirst []))

insertAxis :: Axis -> [Axis] -> [Axis]
insertAxis x (y : ys)
  | GT <- byStrideRank x y = let !r = insertAxis x ys in y : r
insertAxis x ys = x : ys

-- The merge loop of 'unorderedRouteT', entered from the end of
-- 'sortAxesT', in the sorted order, its 'Axes' last as 'canonicalizeT'
-- has it, and free to reorder at its exit, the result need keep only the
-- multiset: a zero-stride head moves there just outside the unit-stride
-- axis next to it.  Moved after the loop, into the route, the move read
-- 6 to 10 instructions a call fewer on views with a zero stride and 3 to
-- 9 more on views without one, wherever the count resolves.
canonicalizeSortedT :: [Axis] -> Axes -> Axes
canonicalizeSortedT (Axis st n : ps)
                    (Axes stHead nHead irest@(InnerFirst rest))
  | stHead == n * st = canonicalizeSortedT ps (Axes st (nHead * n) irest)
  | otherwise =
      canonicalizeSortedT ps (Axes st n (InnerFirst (Axis stHead nHead : rest)))
canonicalizeSortedT [] (Axes 0 nHead (InnerFirst (Axis 1 n1 : outer))) =
  Axes 1 n1 (InnerFirst (Axis 0 nHead : outer))
canonicalizeSortedT [] axes = axes

-- The dispatch of 'unorderedRouteT', piece by piece.
--
-- Overview.  A consumer that folds with a commutative and associative
-- operation needs the view's elements as a multiset, not in order.
-- So the axes may be reordered freely, a reversed axis may be walked
-- forwards, and the question is only which slices of the vector, taken
-- together, hold each element as often as the view holds it.  The
-- answer: sort the axes by stride, merge the axes that are walked as
-- one, move a broadcast axis outside the run, and read the route off
-- what is left, one slice, runs, or a fill.  The passes over the axes
-- are ordered so that each sees as few axes as it can, and the account
-- below takes them in the order they run.
--
-- Why one walk first.  Three things are read off the shape and the
-- strides as given: which axes have extent 1, the absolute value of
-- each stride, and the start offset (below).  Each is a pass over the
-- two lists, and 'absAxesAndStartT' takes all three in one, returning
-- the axes that matter, their strides made absolute, with the start
-- offset beside them.
--
-- Why drop the axes of extent 1 before the sort.  An axis of extent 1
-- selects one index and is walked no distance, so its stride says
-- nothing about which cells are touched, and canonicalization drops it
-- whatever its stride.  Dropped before the sort, it leaves the sort
-- fewer axes to order, and on a view where such an axis shares a stride
-- with another --- the channel axis of a one-channel convolution patch,
-- extent 1 at the output axis's stride --- the sort meets no tie and
-- has no order to undo, where 'sortBy', the sort before 'sortAxesT',
-- paid several hundred instructions to reorder five axes on meeting
-- one.  A zero stride on such an axis goes with it, so no later test
-- has to see past it.
--
-- Why abs.  A negative stride walks an axis backwards over the same
-- cells a positive one walks forwards.  Order is not asked for here, so
-- only the magnitude says which cells are touched; the sign is used
-- once, in the same walk, to find where the lowest address is.
--
-- Why start.  The slices, or the fill, must begin at the block's
-- lowest address, and the offset ao is not it: ao is where index
-- (0, ..., 0) sits, which is the lowest address only when no stride
-- is negative.  An axis with a negative stride has its lowest address
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
-- one axis of the combined extent would.  The merge loop merges every
-- such pair.  Done after the sort, the merge finds every pair the sorted
-- order stands next to each other, which in a view without a stride
-- tie is every pair any order of the axes would have put together; a
-- view that is one block of the vector has no tie, so it merges to a
-- single axis of stride 1 and reads as one slice, whatever order its
-- axes came in, and 'routeOfT' decides that off the merged form with
-- no stride list built.
--
-- Why the zero-stride axis moves just outside the run, and why after
-- the merge.  A broadcast axis, stride 0, reads the same cells at every
-- index.  Sorted by stride it lands innermost, and there it makes the
-- route a fill, each element copied as many times as the broadcast
-- repeats it.  Moved over a unit-stride axis it makes the route runs:
-- the runs walk repeats one slice as many times, the same multiset
-- with nothing copied, and the fill writes the run once and copies it
-- by doubling.  Decided after the merge, the move is one look at the
-- first two merged axes, innermost first: a zero stride merges with
-- nothing but another zero stride, so there is at most one such axis,
-- and it sorts after every other stride, so it is innermost, the head;
-- and a unit-stride axis worth moving it over is the one after it.
-- The merge loop does the look and the move at its exit.
--
-- Just outside the run rather than outermost is a choice neither
-- placement wins.  A cons there saves the append, 26 to 36
-- instructions a call where the move passes no axis, and makes the
-- broadcast's extent the one the odometer turns over on, which read
-- 1.58 times the instructions and 30 KB a call more at a broadcast of
-- 2, and 0.46 times and 62 KB a call less at a broadcast of 52, both on
-- views of 4992 elements.  Placing it just outside the run only where
-- its extent exceeds that of the axis it would displace would take the
-- better of both; untried.

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
-- array yielding the empty list.  The list is produced lazily, as
-- 'toVectorListT''s is, so 'anyT' and 'allT' stop at the first slice that
-- decides.
{-# INLINE toUnorderedVectorListT #-}
toUnorderedVectorListT :: (Vector v, VecElem v a) => ShapeL -> T v a -> [v a]
toUnorderedVectorListT sh a@(T _ _ v) = build $ \cons nil ->
  -- Under one 'build' with the dispatch inside it, as 'toVectorListT'
  -- is and for the same reason.
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
indexT _ _ = error "indexT: violated contract: rank 0"

-- Stretch the given dimensions to have arbitrary size.
-- The stretched dimensions must have size 1, and stretching is
-- done by setting the stride to 0.
{-# INLINE stretchT #-}
stretchT :: [Bool] -> T v a -> T v a
stretchT bs (T ss o v) = T (zipWith (\ b s -> if b then 0 else s) bs ss) o v

-- Map over the array elements.  A view that skips elements is mapped
-- without its broadcast dimensions, which then repeat the result.
-- Future TODO: a view that skips elements and reads others more than
-- once, as a window over a stride does, is built whole, so f runs once
-- per element of the view, not once per element it reads.  The plan: in
-- the view without its broadcast dimensions, merge every two axes of one
-- stride, of extents n and k, into one of extent n + k - 1, which leaves
-- the footprint, the elements the view reads; where the footprint reads
-- each of them once, build it with toVectorT, map f over that, and give the
-- result the view's axes at offset 0, each with the stride its footprint
-- axis has in the new vector; otherwise build the view whole, as now.
{-# INLINE mapT #-}
mapT :: (Vector v, VecElem v a, VecElem v b) => ShapeL -> (a -> b) -> T v a -> T v b
mapT sh f t = convertT sh (vMap f) t

-- Convert the vector of an array by the function given, which takes only
-- the part of the vector the view reads: 'mapT' is this at 'vMap', and
-- the conversions between the boxings of the vector package take it too.
-- The future TODO at 'mapT' holds of every use: a view that skips
-- elements and reads others more than once is built whole here.
{-# INLINE convertT #-}
convertT :: (Vector v, VecElem v a, Vector w, VecElem w b)
         => ShapeL -> (v a -> w b) -> T v a -> T w b
convertT sh _ _ | 0 `elem` sh = fromVectorT sh (vConcat [])
convertT sh g t@(T ss o v) | Just (lo, n) <- readRangeT sh t = T ss (o - lo) (g (vSlice lo n v))
convertT sh g t = stretchT bs $ fromVectorT [ if b then 1 else s | (b, s) <- zip bs sh ] $
                  g $ toVectorT rsh r
  where (bs, rsh, r) = dropBroadcastT sh t

-- Zip two arrays with a function.
-- TODO: two views of the same strides that each read every element of one
-- part could zip those parts and keep the strides, as 'convertT' maps a view.
-- Measured on 60000 Doubles, that pays only where they broadcast, from 550
-- us to 1.9, gains nothing on transpositions and costs 14% on dense arrays;
-- a guard confining it to parts smaller than the view would complicate this
-- function and slow down every call.
{-# INLINE zipWithT #-}
zipWithT :: (Vector v, VecElem v a, VecElem v b, VecElem v c) =>
            ShapeL -> (a -> b -> c) -> T v a -> T v b -> T v c
zipWithT sh f t@(T ss _ v) t'@(T _ _ v') =
  case (vLength v, vLength v') of
    (1, 1) | 0 `notElem` sh ->
      -- If both vectors have length 1, then it's a degenerate case and it's better
      -- to operate on the single element directly, unless the view is empty and
      -- the element lies outside it.
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
zipWith3T sh f (T ss _ v) (T _ _ v') (T _ _ v'') |
  -- If all vectors have length 1, then it's a degenerate case and it's better
  -- to operate on the single element directly, unless the view is empty and
  -- the element lies outside it.
  0 `notElem` sh, vLength v == 1, vLength v' == 1, vLength v'' == 1 =
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

-- Return all subarrays n dimensions down.  The shape argument should be a
-- prefix of the array shape.  In row-major order, under one 'build' walked by
-- 'offsetsT', so that a consumer folding the list fuses with the walk; an empty
-- outer dimension leaves none.
{-# INLINE subArraysT #-}
subArraysT :: ShapeL -> T v a -> [T v a]
subArraysT sh (T ts o v) = build $ \ cons nil ->
  if product sh == 0 then nil else case reverse (zipWith Axis ots sh) of
    [] -> cons (T its o v) nil
    axis : above -> offsetsT axis above o (\ p rest -> cons (T its p v) rest) nil
  where (ots, its) = splitAt (length sh) ts

-- Reverse the given dimensions.
{-# INLINE reverseT #-}
reverseT :: [Int] -> ShapeL -> T v a -> T v a
reverseT rs sh (T ats ao v) = T rts ro v
  where (ro, rts) = rev 0 sh ats
        rev !_ [] [] = (ao, [])
        rev !r (m:ms) (t:ts) | r `elem` rs = (o + (m-1)*t, -t : ts')
                             | otherwise   = (o,            t : ts')
          where (o, ts') = rev (r+1) ms ts
        rev _ _ _ = error "reverseT: violated contract: not one stride per dimension"

-- Reduction of all array elements, in row-major order, which the function may
-- need.  A view that no slice serves, which 'toVectorListT' would fill into
-- one vector, is folded over its element walk ('elemsT') instead, as 'toListT'
-- lists it.
{-# INLINE reduceT #-}
reduceT :: (Vector v, VecElem v a) =>
           ShapeL -> (a -> a -> a) -> a -> T v a -> T v a
reduceT sh f !z a@(T _ _ v)
  | l == 0 = scalarT z
  | otherwise = scalarT $ case routeT sh l a of
      RFill axes ao _ ->
        foldl' f z (build $ \cons nil -> elemsT axes ao v cons nil)
      route ->
        foldl' (vFold f) z (build $ \cons nil -> routeSlicesT v route cons nil)
  where !l = product sh

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

-- Fast check if all elements are equal, agreeing with allSame.  Of two or
-- more elements, the first is compared with all, itself included, which
-- gives allSame's answer as long as an element unequal to itself, as NaN
-- is, is unequal to all others.
{-# INLINABLE allSameT #-}
allSameT :: (Vector v, VecElem v a, Eq a) => ShapeL -> T v a -> Bool
allSameT sh t@(T _ ao v)
  | product sh <= 1 = True
  | vLength v == 1 = let !x = vIndex v 0 in x == x
  | otherwise =
    -- Order does not matter, so the unordered list, which is one slice
    -- for a dense view under any transposition.  The element at index
    -- zero sits at the offset, so no slice is held for it.  The fold sits
    -- on the list expression, where it fuses with the walk and stops at
    -- the first element that differs.
    let !x = vIndex v ao
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

-- Pretty-print an array as its elements laid out in rows by its shape,
-- which is not shown otherwise: arrays of shapes [3] and [1,3] print alike,
-- and every array with no elements has no rows, so prints as the same empty
-- box, or as nothing below prettyNormal, "()" at a precedence above 10.
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
showsT s      _ | 0 `elem` s = Rect []  -- no elements, no rows
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
      h = replicate (rectWidth (Rect ls)) dash
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
padT v aps ash at =
  (ss, fromVectorT ss $ vConcatN (product ss) $ pad' aps ash st at)
  where pad' :: [(Int, Int)] -> ShapeL -> [Int] -> T v a -> [v a]
        -- The last padded dimension's block is taken whole as toVectorListT's
        -- list and not recursed into: recursing made each core a subarray of
        -- that dimension, a scalar where the innermost dimension is padded,
        -- and so a slice and an indexT per element; on views of about 200000
        -- Doubles with the innermost dimension padded, the block taken whole
        -- took 0.01 to 0.32 of the time.  As a list and not one vector by
        -- toVectorT: here vConcatN copies every part once, so a block lying in
        -- runs of the source is copied once from the list's slices and would
        -- be copied twice from a vector toVectorT filled; a strided block,
        -- which no slice can take, is filled and copied either way.  The
        -- vector was tried and refuted: about twice the list's
        -- time on a block of runs of 500, and faster only on boxed runs of
        -- 8, in about half the list's time, which a choice per block by run
        -- length would buy for a dispatch here.  The parts produced under one
        -- 'build', each level handing the rest on so that genericConcatN's
        -- 'foldr' fuses with them, were tried and refuted: on
        -- GHC HEAD at Storable and Unboxed elements, at allocation areas
        -- of 32 MB and then of 4 MB, 0.99 to 1.34 and 1.03 to 1.30 times
        -- the list's time, allocating at most 3.3% less, and at boxed ones
        -- 0.88 to 0.96 and 0.94 to 1.08 times it.
        pad' [] sh _ t = toVectorListT sh t
        pad' [(l,h)] (s:sh) (!n:_) t =
          [vReplicate (n*l) v] ++ toVectorListT (s:sh) t ++ [vReplicate (n*h) v]
        pad' ((l,h):ps) (s:sh) (!n:ns) t =
          [vReplicate (n*l) v] ++ concatMap (pad' ps sh ns . indexT t) [0..s-1] ++ [vReplicate (n*h) v]
        pad' _ _ _ _ = error $ "padT: violated contract: padding list longer than the rank " ++ show (length aps, length ash)
        _ : st = getStridesT ss
        -- The padded shape, which fails on more pairs than dimensions even
        -- where an empty dimension stops pad' before the surplus pair.
        ss = padded aps ash
        padded ((l,h):ps) (s:sh) = l+s+h : padded ps sh
        padded [] sh = sh
        padded _ [] = error $ "padT: violated contract: padding list longer than the rank " ++ show (length aps, length ash)

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
      loop _ _ = error $ "simpleReshape: violated contract: not one stride per dimension " ++ show (osts, os, ns)
simpleReshape _ _ _ = Nothing

-- Note: assumes + is commutative&associative.
{-# INLINE sumT #-}
sumT :: (Vector v, VecElem v a, Num a) => ShapeL -> T v a -> a
sumT sh = sum . map vSum . toUnorderedVectorListT sh

-- Note: assumes * is commutative&associative.
{-# INLINE productT #-}
productT :: (Vector v, VecElem v a, Num a) => ShapeL -> T v a -> a
productT sh = product . map vProduct . toUnorderedVectorListT sh

-- Note: assumes max is commutative&associative.  A view of runs folds the
-- runs' maxima in the order 'maximum' folds their list, the walk's own cons
-- carrying whether one has been taken, so that no list is built; the element
-- at the offset only starts the accumulator, which the first maximum replaces
-- unread.  A view that is one vector, a slice or a fill, takes its maximum as
-- it is: folded as runs are, on a dense array of boxed Doubles it ran 12% more
-- instructions.
{-# INLINE maximumT #-}
maximumT :: (Vector v, VecElem v a, Ord a) => ShapeL -> T v a -> a
maximumT sh t@(T _ ao v)
  | l == 0 = maximum (map vMaximum (toUnorderedVectorListT sh t))
  | otherwise = case unorderedRouteT sh l t of
      RRuns axes o _ -> runSlicesT axes o v step (\ _ acc -> acc) False (vIndex v ao)
      route -> routeSlicesT v route (\ s _ -> vMaximum s) (vIndex v ao)
  where !l = product sh
        step s k = \ started !acc -> let !m = vMaximum s
                                     in  k True (if started then max acc m else m)

-- Note: assumes min is commutative&associative.  Folded as 'maximumT' folds.
{-# INLINE minimumT #-}
minimumT :: (Vector v, VecElem v a, Ord a) => ShapeL -> T v a -> a
minimumT sh t@(T _ ao v)
  | l == 0 = minimum (map vMinimum (toUnorderedVectorListT sh t))
  | otherwise = case unorderedRouteT sh l t of
      RRuns axes o _ -> runSlicesT axes o v step (\ _ acc -> acc) False (vIndex v ao)
      route -> routeSlicesT v route (\ s _ -> vMinimum s) (vIndex v ao)
  where !l = product sh
        step s k = \ started !acc -> let !m = vMinimum s
                                     in  k True (if started then min acc m else m)

{-# INLINE anyT #-}
anyT :: (Vector v, VecElem v a) => ShapeL -> (a -> Bool) -> T v a -> Bool
anyT sh p = or . map (vAny p) . toUnorderedVectorListT sh

{-# INLINE allT #-}
allT :: (Vector v, VecElem v a) => ShapeL -> (a -> Bool) -> T v a -> Bool
allT sh p = and . map (vAll p) . toUnorderedVectorListT sh

-- vUpdate copies the vector toVectorT returns, a second copy wherever the view
-- is not one slice and that vector was just filled.  Not skipped: that wants
-- a class method updating a vector the caller owns, updateT reaching the fill
-- only through vFillStrided and so unable to force it inline for vector's
-- clone/new rule to drop the copy.
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
        toIx (n:ns) !i = q : toIx ns r where (q, r) = quotRem i n

{-# INLINE iterateNT #-}
iterateNT :: (Vector v, VecElem v a) => Int -> (a -> a) -> a -> T v a
iterateNT n f x = fromListT [n] $ take n $ iterate f x

{-# INLINE iotaT #-}
iotaT :: (Vector v, VecElem v a, Num a) => Int -> T v a
iotaT n = fromVectorT [n] $ vFromListN n [ x | i <- [0 .. n - 1], let !x = fromIntegral i ]  -- evaluated, as a boxed vGenerate would not

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
