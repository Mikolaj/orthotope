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
{-# LANGUAGE CPP #-}
{-# LANGUAGE ConstraintKinds #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
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
  normalize,
  scalar, unScalar, constant,
  reshape, stretch, stretchOuter, transpose,
  index, pad,
  mapA, zipWithA, zipWith3A, zipWith4A, zipWith5A,
  append, concatOuter,
  ravel, unravel,
  window, stride,
  slice, rerank, rerank2, rev,
  reduce, foldrA, traverseA,
  allSameA,
  sumA, productA, maximumA, minimumA,
  anyA, allA,
  broadcast,
  update,
  generate, iterateN, iota,
  ) where
import Control.DeepSeq
import Data.Coerce(coerce)
import Data.Data(Data)
import qualified Data.Vector.Unboxed as V
import GHC.Stack(HasCallStack)
import Test.QuickCheck hiding (generate)
import GHC.Generics(Generic)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import qualified Data.Array.Internal.Dynamic as D
import qualified Data.Array.DynamicG as G
import Data.Array.Internal(ShapeL, Vector(..), genericFillStrided)

type Unbox = V.Unbox

instance Vector V.Vector where
  type VecElem V.Vector = Unbox
  {-# INLINE vIndex #-}
  vIndex = (V.!)
  {-# INLINE vLength #-}
  vLength = V.length
  {-# INLINE vToList #-}
  vToList = V.toList
  {-# INLINE vFromList #-}
  vFromList = V.fromList
  {-# INLINE vFromListN #-}
  vFromListN = V.fromListN
  {-# INLINE vSingleton #-}
  vSingleton = V.singleton
  {-# INLINE vReplicate #-}
  vReplicate = V.replicate
  -- The map and the zips generate their result over the indices, working
  -- around vector's own, whose stream-fused loops at -O1 allocate per element:
  -- a zipWith on Doubles 112 bytes an element, and 64 with SpecConstr, against
  -- 8, taking through zipWithA and zipWith3A 7 to 49 times as long.  No
  -- fusion is given up: vector's fuse with a vector they read, but each array
  -- operation stores its result, so the array operations never fused their
  -- inputs; a map of a map allocates one vector per map, with vector's map
  -- as with this one.
  {-# INLINE vMap #-}
  vMap f v = V.generate (V.length v) (\ i -> f (V.unsafeIndex v i))
  {-# INLINE vZipWith #-}
  vZipWith f a b =
    V.generate (V.length a `min` V.length b) $ \ i ->
      f (V.unsafeIndex a i) (V.unsafeIndex b i)
  {-# INLINE vZipWith3 #-}
  vZipWith3 f a b c =
    V.generate (V.length a `min` V.length b `min` V.length c) $ \ i ->
      f (V.unsafeIndex a i) (V.unsafeIndex b i) (V.unsafeIndex c i)
  {-# INLINE vZipWith4 #-}
  vZipWith4 f a b c d =
    V.generate (V.length a `min` V.length b `min` V.length c
                `min` V.length d) $ \ i ->
      f (V.unsafeIndex a i) (V.unsafeIndex b i) (V.unsafeIndex c i)
        (V.unsafeIndex d i)
  {-# INLINE vZipWith5 #-}
  vZipWith5 f a b c d e =
    V.generate (V.length a `min` V.length b `min` V.length c
                `min` V.length d `min` V.length e) $ \ i ->
      f (V.unsafeIndex a i) (V.unsafeIndex b i) (V.unsafeIndex c i)
        (V.unsafeIndex d i) (V.unsafeIndex e i)
  {-# INLINE vAppend #-}
  vAppend = (V.++)
  {-# INLINE vConcat #-}
  -- The empty list by hand: without -fspec-constr, off at -O, GHC keeps
  -- V.concat []'s copy loop wherever it is inlined.
  vConcat [] = V.empty
  vConcat vs = V.concat vs
  {-# INLINE vFold #-}
  vFold = V.foldl'
  {-# INLINE vSlice #-}
  vSlice = V.slice
  {-# INLINE vSum #-}
  vSum = V.sum
  {-# INLINE vProduct #-}
  vProduct = V.product
  {-# INLINE vMaximum #-}
  vMaximum = V.maximum
  {-# INLINE vMinimum #-}
  vMinimum = V.minimum
  {-# INLINE vUpdate #-}
  vUpdate = (V.//)
  {-# INLINE vGenerate #-}
  vGenerate = V.generate
  {-# INLINE vAll #-}
  vAll = V.all
  {-# INLINE vAny #-}
  vAny = V.any
  {-# INLINE vFillStrided #-}
  vFillStrided = genericFillStrided 64

type role Array nominal
newtype Array a = A { unA :: G.Array V.Vector a }
  deriving (Pretty, Generic, Data)

instance NFData (Array a)

instance (Show a, Unbox a) => Show (Array a) where
  showsPrec p = showsPrec p . unA

instance (Read a, Unbox a) => Read (Array a) where
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array V.Vector a) => Eq (Array a) where
  x == y = shapeL x == shapeL y && unA x == unA y
  {-# INLINE (==) #-}

instance Ord (G.Array V.Vector a) => Ord (Array a) where
  compare x y = compare (shapeL x) (shapeL y) <> compare (unA x) (unA y)
  {-# INLINE compare #-}

-- | The number of elements in the array.
{-# INLINE size #-}
size :: Array a -> Int
size = product . shapeL

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
shapeL :: Array a -> ShapeL
shapeL = G.shapeL . unA

-- | The rank of an array, i.e., the number of dimensions it has.
-- O(1) time.
rank :: Array a -> Int
rank = G.rank . unA

-- | Index into an array.  Fails if the array has rank 0 or if the index is out of bounds.
-- O(1) time.
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
-- 'normalize' the array first to get a vector of just its elements, which
-- can itself be a slice, as 'normalize' says.
{-# INLINE toVector #-}
toVector :: (Unbox a) => Array a -> V.Vector a
toVector = G.toVector . unA

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: (HasCallStack, Unbox a) => ShapeL -> V.Vector a -> Array a
fromVector ss = A . G.fromVector ss

-- | Make sure the underlying vector is in the linearization order.
-- The vector then holds just the elements of the array, so no larger vector
-- the array is a view of is kept alive; an array whose vector holds just its
-- elements keeps that vector, even where it is a slice of a larger one, such
-- as one given to 'fromVector' or taken by 'reshape' from a view.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINABLE normalize #-}
normalize :: (Unbox a) => Array a -> Array a
normalize = A . G.normalize . unA

-- | Change the shape of an array.  Fails if the arrays have different number of elements.
-- O(n) or O(1) time.
{-# INLINABLE reshape #-}
reshape :: (HasCallStack, Unbox a) => ShapeL -> Array a -> Array a
reshape s = A . G.reshape s . unA

-- | Change the size of dimensions with size 1.  These dimension can be changed to any size.
-- All other dimensions must remain the same.
-- O(1) time.
stretch :: (HasCallStack) => ShapeL -> Array a -> Array a
stretch s = A . G.stretch s . unA

-- | Change the size of the outermost dimension by replication.
-- Fails if the outermost dimension is not 1 or the size is negative.
stretchOuter :: (HasCallStack) => Int -> Array a -> Array a
stretchOuter s = A . G.stretchOuter s . unA

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
scalar :: (Unbox a) => a -> Array a
scalar = A . G.scalar

-- | Convert a scalar (rank 0) array to a value.
-- Fails if the array is not a scalar.
-- O(1) time.
unScalar :: (HasCallStack, Unbox a) => Array a -> a
unScalar = G.unScalar . unA

-- | Make an array with all elements having the same value.
-- O(1) time
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
{-# INLINABLE pad #-}
pad :: (HasCallStack, Unbox a) => [(Int, Int)] -> a -> Array a -> Array a
pad ps v = A . G.pad ps v . unA

-- | Do an arbitrary array transposition.
-- Fails if the transposition argument is not a permutation of the numbers
-- [0..l-1] for an l no greater than the rank of the array, whose l outermost
-- dimensions it permutes.
-- O(1) time.
transpose :: (HasCallStack) => [Int] -> Array a -> Array a
transpose is = A . G.transpose is . unA

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- Fails if either array has rank 0.
-- O(n) time.
{-# INLINABLE append #-}
append :: (HasCallStack, Unbox a) => Array a -> Array a -> Array a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
{-# INLINABLE concatOuter #-}
concatOuter :: (HasCallStack, Unbox a) => [Array a] -> Array a
concatOuter = A . G.concatOuter . coerce

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- Fails if the outer array does not have rank 1.
-- O(n) time.
{-# INLINABLE ravel #-}
ravel :: (HasCallStack, Unbox a) => D.Array (Array a) -> Array a
ravel = A . G.ravel . G.mapA unA . D.unA

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@ where the outermost dimension is not empty.
-- Fails if the array has rank 0.
{-# INLINABLE unravel #-}
unravel :: (HasCallStack, Unbox a) => Array a -> D.Array (Array a)
unravel = D.A . G.mapA A . G.unravel . unA

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
{-# INLINABLE window #-}
window :: (HasCallStack) => [Int] -> Array a -> Array a
window ws = A . G.window ws . unA

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- Fails if the stride list is longer than the rank or a stride is not
-- positive.
-- O(1) time.
stride :: (HasCallStack) => [Int] -> Array a -> Array a
stride ws = A . G.stride ws . unA

-- | Extract a slice of an array.
-- The first argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice [(1,2)] (fromList [4] [1,2,3,4]) == fromList [2] [2,3]@.
-- O(1) time.
slice :: (HasCallStack) => [(Int, Int)] -> Array a -> Array a
slice ss = A . G.slice ss . unA

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array, and none of those /n/
-- dimensions may be empty.
-- O(n) time.
{-# INLINABLE rerank #-}
rerank :: (HasCallStack, Unbox a, Unbox b) => Int -> (Array a -> Array b) -> Array a -> Array b
rerank n f = A . G.rerank n (unA . f . A) . unA

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array, and none of those /n/
-- dimensions may be empty.
-- Fails if the arrays differ in those /n/ outermost dimensions.
-- O(n) time.
{-# INLINABLE rerank2 #-}
rerank2 :: (HasCallStack, Unbox a, Unbox b, Unbox c) =>
           Int -> (Array a -> Array b -> Array c) -> Array a -> Array b -> Array c
rerank2 n f ta tb = A $ G.rerank2 n (\ a b -> unA $ f (A a) (A b)) (unA ta) (unA tb)

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- Fails if a given dimension is not one of the array's.
-- O(1) time.
rev :: (HasCallStack) => [Int] -> Array a -> Array a
rev rs = A . G.rev rs . unA

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINABLE reduce #-}
reduce :: (Unbox a) => (a -> a -> a) -> a -> Array a -> Array a
reduce f z = A . G.reduce f z . unA

-- | Constrained version of 'foldr' for Arrays.
{-# INLINE foldrA #-}
foldrA :: (Unbox a) => (a -> b -> b) -> b -> Array a -> b
foldrA f z = G.foldrA f z . unA

-- | Constrained version of 'traverse' for Arrays.
{-# INLINABLE traverseA #-}
traverseA
  :: (Unbox a, Unbox b, Applicative f) => (a -> f b) -> Array a -> f (Array b)
traverseA f = fmap A . G.traverseA f . unA

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Unbox a, Eq a) => Array a -> Bool
allSameA = G.allSameA . unA

instance (Arbitrary a, Unbox a) => Arbitrary (Array a) where arbitrary = A <$> arbitrary

-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: (Unbox a, Num a) => Array a -> a
sumA = G.sumA . unA

-- | Product of all elements.
{-# INLINE productA #-}
productA :: (Unbox a, Num a) => Array a -> a
productA = G.productA . unA

-- | Maximum of all elements.
-- Fails if the array is empty.
{-# INLINE maximumA #-}
maximumA :: (HasCallStack, Unbox a, Ord a) => Array a -> a
maximumA = G.maximumA . unA

-- | Minimum of all elements.
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
-- The list of dimensions indicies must have the same rank as the argument array
-- and it must be strictly ascending.
-- Fails if an index is not a dimension of the result or the argument's
-- dimensions differ from the result's at those indices.
{-# INLINABLE broadcast #-}
broadcast :: (HasCallStack, Unbox a) =>
             [Int] -> ShapeL -> Array a -> Array a
broadcast ds sh = A. G.broadcast ds sh . unA

-- | Update the array at the specified indicies to the associated value.
-- Fails if an index is out of bounds.
{-# INLINABLE update #-}
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
iterateN :: (HasCallStack, Unbox a) =>
            Int -> (a -> a) -> a -> Array a
iterateN n f = A . G.iterateN n f

-- | Generate a vector from 0 to n-1.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: (HasCallStack, Unbox a, Num a) => Int -> Array a
iota = A . G.iota
