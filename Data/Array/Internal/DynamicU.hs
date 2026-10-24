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

{-# OPTIONS_GHC -Wno-orphans #-}
{-# LANGUAGE BangPatterns #-}
{-# LANGUAGE CPP #-}
{-# LANGUAGE ConstraintKinds #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE ExplicitForAll #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}
-- A workaround for https://gitlab.haskell.org/ghc/ghc/-/work_items/23050, to go
-- once the GHCs supported carry its fix; DynamicS says more.
#if MIN_VERSION_GLASGOW_HASKELL(9,6,3,0)
{-# OPTIONS_GHC -fno-polymorphic-specialisation #-}
#endif
module Data.Array.Internal.DynamicU(
  Array(..), Vector, ShapeL, Unbox,
  size, shapeL, rank,
  toList, fromList, toVector, fromVector,
  normalize, force,
  scalar, unScalar, constant,
  reshape, stretch, stretchOuter, transpose,
  index, pad,
  mapA, zipWithA, zipWith3A, zipWith4A, zipWith5A,
  append, concatOuter,
  ravel, unravel,
  window, stride, rotate,
  slice, rerank, rerank2, rev,
  reduce, foldrA, traverseA,
  allSameA,
  sumA, productA, maximumA, minimumA,
  anyA, allA,
  broadcast,
  update,
  generate, iterateN, iota,
  ) where
import Control.DeepSeq hiding (force)
import Data.Coerce(coerce)
import Data.Data(Data)
import qualified Data.Vector.Unboxed as V
import qualified Data.Vector.Unboxed.Mutable as MV
import GHC.Stack(HasCallStack)
import Test.QuickCheck hiding (generate)
import GHC.Generics(Generic)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import qualified Data.Array.Internal.Dynamic as D
import qualified Data.Array.Internal.DynamicG as G
import Data.Array.Internal(genericUnsafeUpdateOwned, genericUnsafeConcatViewsN,
                           genericMapStrided, genericConcatPadN,
                           genericZipWithStrided, genericZipWith3Strided,
                           genericZipWith4Strided, genericZipWith5Strided,
                           ShapeL, Vector(..), genericUnsafeConcatN,
                           genericForce, genericFromListExactN,
                           genericMaximum, genericMinimum,
                           genericUnsafeFillStrided, genericFillInto,
                           genericMap, genericZipWith, genericZipWith3,
                           genericZipWith4, genericZipWith5,
                           genericUnsafeWithElem, genericGenerate',
                           genericAll, genericAny, genericZipLoop,
                           genericFoldlStored, genericFromListN)

type Unbox = V.Unbox

instance Vector V.Vector where
  type VecElem V.Vector = Unbox
  -- Point-free, as are the point-free methods below, for the reason at the
  -- boxed instance in Data.Array.Internal.Dynamic.
  {-# INLINE vIndex #-}
  vIndex = (V.!)
  {-# INLINE vUnsafeIndex #-}
  vUnsafeIndex = V.unsafeIndex
  {-# INLINE vLength #-}
  vLength = V.length
  -- Named, for the bang, as at the boxed instance in
  -- Data.Array.Internal.Dynamic.
  {-# INLINE vToList #-}
  vToList !a = V.toList a
  {-# INLINE vFromList #-}
  vFromList = V.fromList
  -- By one foldr, for the reason at 'genericFromListN'.
  {-# INLINE vFromListN #-}
  vFromListN = genericFromListN
  {-# INLINE vFromListExactN #-}
  vFromListExactN = genericFromListExactN
  -- By a write into a vector of one element rather than by vector's singleton,
  -- which fills through its stream loop: on GHC HEAD 10.1.20260918 (2026-10-16)
  -- Unboxed scalar, constant, reduce at [3, 3], rerank2.one and single-row
  -- zips ran 12 to 27 instructions a call fewer, and Unboxed rerank 31
  -- to 33 fewer at [3, 3].  The write stands in for the SpecConstr that -O1
  -- leaves off: on GHC HEAD 10.1.20261019 (2026-10-24) with vector patched as
  -- issues 570, 571 and 575 propose and -fspec-constr, scalar and constant ran
  -- up to 5 instructions a call more than through vector's singleton, and
  -- reduce up to 23 more.  Unlike singleton, whose elemseq forces it
  -- (https://github.com/haskell/vector/issues/575), the write leaves an element
  -- at vector's DoNotUnboxLazy unevaluated.
  --
  -- INLINE: on GHC HEAD 10.1.20260918 (2026-10-16), under INLINABLE the
  -- specialisation benchmark's summed Shaped reduce at [3, 3] and of an empty
  -- array ran 5 instructions a call more, 1 to 3%, and Dynamic and Ranked
  -- rerank at [3, 3] 6 to 8 fewer, 0.2%.
  {-# INLINE vSingleton #-}
  vSingleton a = V.create $ do
    v <- MV.unsafeNew 1
    MV.unsafeWrite v 0 a
    return v
  -- vector's replicate, whose elemseq forces an element at vector's
  -- DoNotUnboxLazy (https://github.com/haskell/vector/issues/575).
  {-# INLINE vReplicate #-}
  vReplicate = V.replicate
  -- The map and the zips build their result over the indices, which
  -- stands in for the SpecConstr that -O1 leaves off: without it vector's
  -- own stream-fused loops allocate per element, a zipWith on Doubles
  -- 72 bytes an element against 8, taking through zipWithA 13 to 15
  -- times as long; and vector's zipWith5, whose stream SpecConstr leaves
  -- boxed (https://github.com/haskell/vector/issues/579), allocates so
  -- with -fspec-constr too, 496 bytes an element against 8, on GHC HEAD
  -- 10.1.20261019 (2026-10-24).  They write it by 'genericMap' and its zips, as
  -- the boxed instance does, each element read in ST before the function takes
  -- it, strictly for the primitive representations and as stored for vector's
  -- DoNotUnboxLazy, so that such a result holds, until forced, the elements its
  -- function reads and not the vectors they come from: written as 'g i', by a
  -- loop of their own or by generate, it held those (the test lazyElems_2).
  -- Against that, on GHC HEAD 10.1.20261019 (2026-10-21), the specialisation
  -- benchmark's forced zipWithA ran 24 instructions a call fewer at [3, 3]
  -- and 2 an element fewer at [400, 500], 1.5 to 17%, and zipWith5A 8 a call
  -- fewer, mapA, zipWith3A and zipWith4A as many.  No fusion is given up, and
  -- reading each element before the function takes it saves allocation, as at
  -- DynamicS's map and zips, whose figures were measured at both kinds.
  {-# INLINE vMap #-}
  vMap = genericMap
  {-# INLINE vZipWith #-}
  vZipWith = genericZipWith
  {-# INLINE vZipWith3 #-}
  vZipWith3 = genericZipWith3
  {-# INLINE vZipWith4 #-}
  vZipWith4 = genericZipWith4
  {-# INLINE vZipWith5 #-}
  vZipWith5 = genericZipWith5
  {-# INLINE vAppend #-}
  vAppend = (V.++)
  -- INLINE: not for fusion; F1 reads no fusion here: V.concat hands its list to
  -- vector's fromVectors, which refers to it three times, so it fuses with no
  -- producer.
  {-# INLINE vConcat #-}
  vConcat = V.concat
  -- vFold, vSum and vProduct fold over the indices, each element read as
  -- stored, as vAll and vAny read it, which stands in for the SpecConstr
  -- that -O1 leaves off: against vector's own, on GHC HEAD 10.1.20261019
  -- (2026-10-24) the specialisation benchmark's reduce, sumA and productA ran
  -- 8 to 10 instructions a call fewer at [3, 3], 1.4 to 1.5%, and 1 an element
  -- fewer at [400, 500], 14%, and with -fspec-constr as many, reduce at [3, 3]
  -- 2 more.
  {-# INLINE vFold #-}
  vFold = genericFoldlStored
  {-# INLINE vSlice #-}
  vSlice = V.slice
  {-# INLINE vUnsafeSlice #-}
  vUnsafeSlice = V.unsafeSlice
  {-# INLINABLE vSum #-}
  vSum = genericFoldlStored (+) 0
  {-# INLINABLE vProduct #-}
  vProduct = genericFoldlStored (*) 1
  -- INLINE: see the header of Data.Array.Internal, where these two are measured
  -- with productT, maximumT and minimumT.
  --
  -- The maximum and the minimum fold over the indices, in the order of vector's
  -- foldl1': on GHC HEAD with vector patched as issue 570 proposes, minimumA
  -- took 0.67 to 0.72 of its time at -O1 and maximumA as long as with vector's
  -- own, and with -fspec-constr, on a view of runs, 0.71 and 0.85 of it,
  -- elsewhere as long: but on views of runs, they stand in for the SpecConstr
  -- that -O1 leaves off.
  {-# INLINE vMaximum #-}
  vMaximum v = genericMaximum v
  -- INLINE and folded as vMaximum is.
  {-# INLINE vMinimum #-}
  vMinimum v = genericMinimum v
  {-# INLINE vUpdate #-}
  vUpdate = (V.//)
  -- vGenerate writes over the indices ('genericZipLoop') each element as
  -- its function gives it, by one counter, where vector's generate fills
  -- through unstream's loop, which keeps the position it writes beside
  -- the stream's index, two counters always equal that GHC does not merge
  -- (https://gitlab.haskell.org/ghc/ghc/-/work_items/4470): against vector's
  -- generate, on GHC HEAD 10.1.20261019 (2026-10-24) the specialisation
  -- benchmark's generate ran 38 instructions a call fewer at [3, 3] and 4 an
  -- element fewer at [400, 500], 2.6 and 3.4%, and with -fspec-constr 28 and 3
  -- fewer.
  {-# INLINE vGenerate #-}
  vGenerate n g = genericZipLoop (max 0 n) (\ i -> return (g i))
  -- vAll and vAny read as the boxed instance's do, which stands in for the
  -- SpecConstr that -O1 leaves off: on GHC HEAD 10.1.20261019 (2026-10-24) with
  -- vector patched as issues 570, 571 and 575 propose, the specialisation
  -- benchmark's allA and anyA ran up to 12 instructions a call fewer at [3, 3]
  -- and up to 1 an element fewer at [400, 500], up to 11%, than through
  -- vector's own, and with -fspec-constr up to 2 a call more at [3, 3].
  {-# INLINE vAll #-}
  vAll = genericAll
  {-# INLINE vAny #-}
  vAny = genericAny
  -- The element at an index in bounds, handed on as unsafeIndexM reads
  -- it, as the boxed instance reads its own: evaluated for the primitive
  -- representations, whose reads are strict, and as stored for vector's
  -- DoNotUnboxLazy, whose elements can be undefined.  Forcing the read, as
  -- 'V.unsafeIndex' with a bang did, would fail on such an element.
  {-# INLINE vUnsafeWithElem #-}
  vUnsafeWithElem = genericUnsafeWithElem
  -- Each element forced before it is written: vector's write stores
  -- a DoNotUnboxLazy element as it is given.
  {-# INLINE vGenerate' #-}
  vGenerate' = genericGenerate'
  {-# INLINE vUnsafeFillStrided #-}
  vUnsafeFillStrided = genericUnsafeFillStrided 64
  {-# INLINE vForce #-}
  vForce = genericForce
  {-# INLINE vUnsafeUpdateOwned #-}
  vUnsafeUpdateOwned = genericUnsafeUpdateOwned
  {-# INLINE vUnsafeConcatViewsN #-}
  vUnsafeConcatViewsN = genericUnsafeConcatViewsN (genericFillInto 64)
  {-# INLINE vMapStrided #-}
  vMapStrided = genericMapStrided False
  {-# INLINE vConcatPadN #-}
  vConcatPadN = genericConcatPadN (genericFillInto 64)
  {-# INLINE vZipWithStrided #-}
  vZipWithStrided = genericZipWithStrided False
  {-# INLINE vZipWith3Strided #-}
  vZipWith3Strided = genericZipWith3Strided False
  {-# INLINE vZipWith4Strided #-}
  vZipWith4Strided = genericZipWith4Strided False
  {-# INLINE vZipWith5Strided #-}
  vZipWith5Strided = genericZipWith5Strided False
  {-# INLINE vUnsafeConcatN #-}
  vUnsafeConcatN = genericUnsafeConcatN

type role Array nominal
newtype Array a = A { unA :: G.Array V.Vector a }
  deriving (Pretty, Generic, Data)

-- Through Generic, so that rnf evaluates the shape, the strides and the offset
-- fully and the vector to weak head normal form, as vector's own rnf does,
-- and no element: a DoNotUnboxLazy element stays as stored, where the boxed
-- modules' rnf evaluates the elements of the view.
instance NFData (Array a)

-- Point-free, as are the point-free wrappers and instance methods below, for
-- the reason at the Show instance of Data.Array.Internal.Dynamic.
instance (Show a, Unbox a) => Show (Array a) where
  {-# INLINE showsPrec #-}
  showsPrec p = showsPrec p . unA

instance (Read a, Unbox a) => Read (Array a) where
  {-# INLINABLE readsPrec #-}
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array V.Vector a) => Eq (Array a) where
  {-# INLINE (==) #-}
  x == y = unA x == unA y

instance Ord (G.Array V.Vector a) => Ord (Array a) where
  {-# INLINE compare #-}
  compare x y = compare (unA x) (unA y)

-- Not G.size . unA: see Data.Array.Internal.Dynamic's size.
--
-- | The number of elements in the array.
size :: Array a -> Int
size = product . shapeL

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
{-# INLINE shapeL #-}
shapeL :: Array a -> ShapeL
shapeL = G.shapeL . unA

-- | The rank of an array, i.e., the number of dimensions it has.
-- O(1) time.
{-# INLINE rank #-}
rank :: Array a -> Int
rank = G.rank . unA

-- | Index into an array.  Fails if the array has rank 0 or if the index is out of bounds.
-- O(1) time.
{-# INLINE index #-}
index :: (HasCallStack) => Array a -> Int -> Array a
index a = A . G.index (unA a)

-- | Convert to a list with the elements in the linearization order.
-- O(n) time.
{-# INLINE toList #-}
toList :: (Unbox a) => Array a -> [a]
toList = G.toList . unA

-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: (HasCallStack, Unbox a) => ShapeL -> [a] -> Array a
fromList ss = A . G.fromList ss

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: (Unbox a) => Array a -> V.Vector a
toVector = G.toVector . unA

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the
-- vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: (HasCallStack, Unbox a) => ShapeL -> V.Vector a -> Array a
fromVector ss = A . G.fromVector ss

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINE normalize #-}
normalize :: (Unbox a) => Array a -> Array a
normalize = A . G.normalize . unA

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  This is
-- especially useful for a view of a large array, such as @'index' a 0@,
-- which keeps the whole vector of @a@ alive, the elements it does not show
-- included: forcing it copies just its own elements and allows the large
-- vector to be garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINE force #-}
force :: (Unbox a) => Array a -> Array a
force = A . G.force . unA

-- | Change the shape of an array.  Fails if the arrays have different number of elements.
-- O(n) or O(1) time.
{-# INLINE reshape #-}
reshape :: (HasCallStack, Unbox a) => ShapeL -> Array a -> Array a
reshape s = A . G.reshape s . unA

-- | Change the size of dimensions with size 1.  These dimensions can be changed
-- to any size.
-- All other dimensions must remain the same.
-- O(1) time.
{-# INLINE stretch #-}
stretch :: (HasCallStack) => ShapeL -> Array a -> Array a
stretch s = A . G.stretch s . unA

-- | Change the size of the outermost dimension by replication.
-- Fails if the outermost dimension is not 1 or the size is negative.
{-# INLINE stretchOuter #-}
stretchOuter :: (HasCallStack) => Int -> Array a -> Array a
stretchOuter s = A . G.stretchOuter s . unA

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
{-# INLINE scalar #-}
scalar :: (Unbox a) => a -> Array a
scalar = A . G.scalar

-- | Convert a scalar (rank 0) array to a value.
-- Fails if the array is not a scalar.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: (HasCallStack, Unbox a) => Array a -> a
unScalar = G.unScalar . unA

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: (HasCallStack, Unbox a) => ShapeL -> a -> Array a
constant sh = A . G.constant sh

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: (Unbox a, Unbox b) => (a -> b) -> Array a -> Array b
mapA f = A . G.mapA f . unA

-- | Combine the elements of two arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: (HasCallStack, Unbox a, Unbox b, Unbox c) =>
            (a -> b -> c) -> Array a -> Array b -> Array c
zipWithA f a b = A $ G.zipWithA f (unA a) (unA b)

-- | Combine the elements of three arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: (HasCallStack, Unbox a, Unbox b, Unbox c, Unbox d) =>
             (a -> b -> c -> d) -> Array a -> Array b -> Array c -> Array d
zipWith3A f a b c = A $ G.zipWith3A f (unA a) (unA b) (unA c)

-- | Combine the elements of four arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: (HasCallStack, Unbox a, Unbox b, Unbox c, Unbox d, Unbox e) =>
             (a -> b -> c -> d -> e) -> Array a -> Array b -> Array c -> Array d -> Array e
zipWith4A f a b c d = A $ G.zipWith4A f (unA a) (unA b) (unA c) (unA d)

-- | Combine the elements of five arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: (HasCallStack, Unbox a, Unbox b, Unbox c, Unbox d, Unbox e, Unbox f) =>
             (a -> b -> c -> d -> e -> f) -> Array a -> Array b -> Array c -> Array d -> Array e -> Array f
zipWith5A f a b c d e = A $ G.zipWith5A f (unA a) (unA b) (unA c) (unA d) (unA e)

-- | Pad each dimension on the low and high side with the given value.
-- Fails if the padding list is longer than the rank or a padding is negative.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
-- A padding of -0.0 at Float or Double is written as +0.0, by
-- primitive-0.9.1.0's setByteArray, until a primitive release has
-- https://github.com/haskell/primitive/pull/433.
{-# INLINE pad #-}
pad :: (HasCallStack, Unbox a) => [(Int, Int)] -> a -> Array a -> Array a
pad ps v = A . G.pad ps v . unA

-- | Do an arbitrary array transposition.
-- Fails if the transposition argument is not a permutation of the numbers
-- [0..l-1] for an l no greater than the rank of the array, whose l outermost
-- dimensions it permutes.
-- O(1) time.
{-# INLINE transpose #-}
transpose :: (HasCallStack) => [Int] -> Array a -> Array a
transpose is = A . G.transpose is . unA

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- Fails if either array has rank 0.
-- O(n) time.
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINE append #-}
append :: (HasCallStack, Unbox a) => Array a -> Array a -> Array a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE concatOuter #-}
concatOuter :: (HasCallStack, Unbox a) => [Array a] -> Array a
concatOuter = A . G.concatOuter . coerce

-- INLINE: see Data.Array.Internal.Dynamic's ravel.
-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- Fails if the outer array does not have rank 1.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINE ravel #-}
ravel :: (HasCallStack, Unbox a) => D.Array (Array a) -> Array a
ravel = A . G.ravelWith unA . D.unA

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@ where the outermost dimension is not empty.
-- Fails if the array has rank 0.
{-# INLINE unravel #-}
unravel :: (HasCallStack) => Array a -> D.Array (Array a)
unravel = D.A . G.unravelWith A . unA

-- | Make a window of the outermost dimensions.
-- The rank increases with the length of the window list.
-- E.g., if the shape of the array is @[10,12,8]@ and
-- the window size is @[3,3]@ then the resulting array will have shape
-- @[8,10,3,3,8]@.
--
-- E.g., @window [2] (fromList [4] [1,2,3,4]) == fromList [3,2] [1,2, 2,3, 3,4]@
-- Fails if the window list is longer than the rank or a window is negative or
-- larger than its dimension.
-- O(1) time.
--
-- If the window parameter @ws = [w1,...,wk]@ and @wa = window ws a@ then
-- @wa `index` i1 ... `index` ik == slice [(i1,w1),...,(ik,wk)] a@.
{-# INLINE window #-}
window :: (HasCallStack) => [Int] -> Array a -> Array a
window ws = A . G.window ws . unA

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- Fails if the stride list is longer than the rank or a stride is not
-- positive.
-- O(1) time.
{-# INLINE stride #-}
stride :: (HasCallStack) => [Int] -> Array a -> Array a
stride ws = A . G.stride ws . unA

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- Fails if d is not a dimension of the array or k is negative, and may fail
-- if the result has more than half of 'maxBound' elements.
-- With k = 1, or along a dimension the array broadcasts, the result is a view
-- of the array, sharing its vector; 'force' copies it out.
{-# INLINE rotate #-}
rotate :: (HasCallStack, Unbox a) => Int -> Int -> Array a -> Array a
rotate d k = A . G.rotate d k . unA

-- | Extract a slice of an array.
-- The first argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice [(1,2)] (fromList [4] [1,2,3,4]) == fromList [2] [2,3]@.
-- O(1) time.
{-# INLINE slice #-}
slice :: (HasCallStack) => [(Int, Int)] -> Array a -> Array a
slice ss = A . G.slice ss . unA

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must be from 0 to the rank of the array, none of those /n/ dimensions
-- may be empty, and the function's results must all have one shape.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: forall a b . (HasCallStack, Unbox b)
       => Int -> (Array a -> Array b) -> Array a -> Array b
rerank n f = A . G.rerank n (unA . f . A) . unA

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must be from 0 to the rank of each array, none of those /n/
-- dimensions may be empty, and the function's results must all have one shape.
-- Fails if the arrays differ in those /n/ outermost dimensions.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: forall a b c . (HasCallStack, Unbox c) =>
           Int -> (Array a -> Array b -> Array c) -> Array a -> Array b -> Array c
rerank2 n f ta tb = A $ G.rerank2 n (\ a b -> unA $ f (A a) (A b)) (unA ta) (unA tb)

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- Fails if a given dimension is not one of the array's, or is given twice.
-- O(1) time.
{-# INLINE rev #-}
rev :: (HasCallStack) => [Int] -> Array a -> Array a
rev rs = A . G.rev rs . unA

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINE reduce #-}
reduce :: (Unbox a) => (a -> a -> a) -> a -> Array a -> Array a
reduce f z = A . G.reduce f z . unA

-- | Constrained version of 'foldr' for Arrays.
{-# INLINE foldrA #-}
foldrA :: (Unbox a) => (a -> b -> b) -> b -> Array a -> b
foldrA f z = G.foldrA f z . unA

-- | Constrained version of 'traverse' for Arrays.
{-# INLINE traverseA #-}
traverseA
  :: (Unbox a, Unbox b, Applicative f) => (a -> f b) -> Array a -> f (Array b)
traverseA f = fmap A . G.traverseA f . unA

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Unbox a, Eq a) => Array a -> Bool
allSameA = G.allSameA . unA

instance (Arbitrary a, Unbox a) => Arbitrary (Array a) where
  {-# INLINABLE arbitrary #-}
  arbitrary = A <$> arbitrary

-- INLINABLE: see Data.Array.Internal.Dynamic's sumA.
-- | Sum of all elements.
{-# INLINABLE sumA #-}
sumA :: (Unbox a, Num a) => Array a -> a
sumA = G.sumA . unA

-- | Product of all elements.
{-# INLINE productA #-}
productA :: (Unbox a, Num a) => Array a -> a
productA = G.productA . unA

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE maximumA #-}
maximumA :: (HasCallStack, Unbox a, Ord a) => Array a -> a
maximumA = G.maximumA . unA

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE minimumA #-}
minimumA :: (HasCallStack, Unbox a, Ord a) => Array a -> a
minimumA = G.minimumA . unA

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: Unbox a => (a -> Bool) -> Array a -> Bool
anyA p = G.anyA p . unA

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: Unbox a => (a -> Bool) -> Array a -> Bool
allA p = G.allA p . unA

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimension indices must have the same rank as the argument array
-- and it must be strictly ascending.
-- Fails if an index is not a dimension of the result or the argument's
-- dimensions differ from the result's at those indices.
{-# INLINE broadcast #-}
broadcast :: (HasCallStack) =>
             [Int] -> ShapeL -> Array a -> Array a
broadcast ds sh = A . G.broadcast ds sh . unA

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds or not of the array's rank.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE update #-}
update :: (HasCallStack, Unbox a) =>
          Array a -> [([Int], a)] -> Array a
update a = A . G.update (unA a)

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: (HasCallStack, Unbox a) => ShapeL -> ([Int] -> a) -> Array a
generate sh = A . G.generate sh

-- | Iterate a function n times.
-- Fails if n is negative.
{-# INLINE iterateN #-}
iterateN :: (HasCallStack, Unbox a) => Int -> (a -> a) -> a -> Array a
iterateN n f = A . G.iterateN n f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: (HasCallStack, Unbox a, Num a) => Int -> Array a
iota = A . G.iota
