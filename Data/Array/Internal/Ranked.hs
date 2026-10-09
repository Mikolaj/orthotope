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
{-# LANGUAGE AllowAmbiguousTypes #-}
{-# LANGUAGE CPP #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE ExplicitNamespaces #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE UndecidableInstances #-}
-- See the comment on this flag in Dynamic.
#if MIN_VERSION_GLASGOW_HASKELL(9,6,3,0)
{-# OPTIONS_GHC -fpolymorphic-specialisation #-}
#endif
module Data.Array.Internal.Ranked(
  Array(..), Vector, ShapeL,
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
import Data.Data(Data)
import Data.Coerce(coerce)
import qualified Data.Vector as V
import GHC.Stack
import GHC.TypeLits(KnownNat, type (+), type (<=))
import Test.QuickCheck hiding (generate)

import GHC.Generics(Generic)
import Data.Array.Internal.Dynamic()  -- Vector instance
import qualified Data.Array.Internal.RankedG as G
import Data.Array.Internal(ShapeL, Vector(..), rnfViewT)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

type role Array nominal nominal
newtype Array n a = A { unA :: G.Array n V.Vector a }
  deriving (Pretty, Generic, Data)

instance NFData a => NFData (Array n a) where
  rnf (A (G.A sh t)) = rnf sh `seq` rnfViewT sh t
  {-# INLINE rnf #-}

instance (Show a) => Show (Array n a) where
  showsPrec p = showsPrec p . unA

instance (KnownNat n, Read a) => Read (Array n a) where
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array n V.Vector a) => Eq (Array n a) where
  x == y = unA x == unA y
  {-# INLINE (==) #-}

instance Ord (G.Array n V.Vector a) => Ord (Array n a) where
  compare x y = compare (unA x) (unA y)
  {-# INLINE compare #-}

-- | The number of elements in the array.
{-# INLINE size #-}
size :: Array n a -> Int
size = product . shapeL

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
shapeL :: Array n a -> ShapeL
shapeL = G.shapeL . unA

-- | The rank of an array, i.e., the number of dimensions it has,
-- which is the @n@ in @Array n a@.
-- O(1) time.
rank :: (KnownNat n) => Array n a -> Int
rank = G.rank . unA

-- | Index into an array.  Fails if the index is out of bounds.
-- O(1) time.
{-# INLINE index #-}
index :: (HasCallStack) => Array (1+n) a -> Int -> Array n a
index a = A . G.index (unA a)

-- | Convert to a list with the elements in the linearization order.
-- O(n) time.
{-# INLINE toList #-}
toList :: Array n a -> [a]
toList = G.toList . unA

-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: forall n a . (HasCallStack, KnownNat n) => ShapeL -> [a] -> Array n a
fromList ss = A . G.fromList ss

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: Array n a -> V.Vector a
toVector = G.toVector . unA

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: forall n a . (HasCallStack, KnownNat n) => ShapeL -> V.Vector a -> Array n a
fromVector ss = A . G.fromVector ss

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINABLE normalize #-}
normalize :: Array n a -> Array n a
normalize = A . G.normalize . unA

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  This is
-- especially useful for a view of a large array, such as @'index' a 0@,
-- which keeps the whole vector of @a@ alive, the elements it does not show
-- included: forcing it copies just its own elements and allows the large
-- vector to be garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINABLE force #-}
force :: Array n a -> Array n a
force = A . G.force . unA

-- | Change the shape of an array.  Fails if the arrays have different number of elements.
-- O(n) or O(1) time.
reshape :: forall n' n a . (HasCallStack, KnownNat n') => ShapeL -> Array n a -> Array n' a
reshape s = A . G.reshape s . unA

-- | Change the size of dimensions with size 1.  These dimension can be changed to any size.
-- All other dimensions must remain the same.
-- O(1) time.
stretch :: (HasCallStack) => ShapeL -> Array n a -> Array n a
stretch s = A . G.stretch s . unA

-- | Change the size of the outermost dimension by replication.
-- Fails if the outermost dimension is not 1 or the size is negative.
stretchOuter :: (HasCallStack, 1 <= n) => Int -> Array n a -> Array n a
stretchOuter s = A . G.stretchOuter s . unA

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
{-# INLINE scalar #-}
scalar :: a -> Array 0 a
scalar = A . G.scalar

-- | Convert a scalar (rank 0) array to a value.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: Array 0 a -> a
unScalar = G.unScalar . unA

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: forall n a . (HasCallStack, KnownNat n) => ShapeL -> a -> Array n a
constant sh = A . G.constant sh

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: forall n a b . (a -> b) -> Array n a -> Array n b
mapA f = A . G.mapA f . unA

instance Functor (Array n) where
  fmap = mapA

instance Foldable (Array n) where
  foldr = foldrA

instance Traversable (Array n) where
  traverse = traverseA

-- | Combine the elements of two arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: forall n a b c . (HasCallStack) => (a -> b -> c) -> Array n a -> Array n b -> Array n c
zipWithA f a b = A $ G.zipWithA f (unA a) (unA b)

-- | Combine the elements of three arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: forall n a b c d . (HasCallStack) => (a -> b -> c -> d) -> Array n a -> Array n b -> Array n c -> Array n d
zipWith3A f a b c = A $ G.zipWith3A f (unA a) (unA b) (unA c)

-- | Combine the elements of four arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: forall n a b c d e . (HasCallStack) => (a -> b -> c -> d -> e) -> Array n a -> Array n b -> Array n c -> Array n d -> Array n e
zipWith4A f a b c d = A $ G.zipWith4A f (unA a) (unA b) (unA c) (unA d)

-- | Combine the elements of five arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: forall n a b c d e f . (HasCallStack) => (a -> b -> c -> d -> e -> f) -> Array n a -> Array n b -> Array n c -> Array n d -> Array n e -> Array n f
zipWith5A f a b c d e = A $ G.zipWith5A f (unA a) (unA b) (unA c) (unA d) (unA e)

-- | Pad each dimension on the low and high side with the given value.
-- Fails if the padding list is longer than the rank or a padding is negative.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE pad #-}
pad :: forall n a . (HasCallStack) => [(Int, Int)] -> a -> Array n a -> Array n a
pad ps v = A . G.pad ps v . unA

-- | Do an arbitrary array transposition.
-- Fails if the transposition argument is not a permutation of the numbers
-- [0..l-1] for an l no greater than the rank of the array, whose l outermost
-- dimensions it permutes.
-- O(1) time.
transpose :: (HasCallStack, KnownNat n) => [Int] -> Array n a -> Array n a
transpose is = A . G.transpose is . unA

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- Fails if either array has rank 0.
-- O(n) time.
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINABLE append #-}
append :: (HasCallStack, KnownNat n) => Array n a -> Array n a -> Array n a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE concatOuter #-}
concatOuter :: (HasCallStack, KnownNat n) => [Array n a] -> Array n a
concatOuter = A . G.concatOuter . coerce

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINABLE ravel #-}
ravel :: (HasCallStack, KnownNat (1+n)) =>
         Array 1 (Array n a) -> Array (1+n) a
ravel = A . G.ravel . G.mapA unA . unA

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@ where the outermost dimension is not empty.
{-# INLINABLE unravel #-}
unravel :: Array (1+n) a -> Array 1 (Array n a)
unravel = A . G.mapA A . G.unravel . unA

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
window :: (HasCallStack, KnownNat n, KnownNat n') => [Int] -> Array n a -> Array n' a
window ws = A . G.window ws . unA

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- Fails if the stride list is longer than the rank or a stride is not
-- positive.
-- O(1) time.
stride :: (HasCallStack) => [Int] -> Array n a -> Array n a
stride ws = A . G.stride ws . unA

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- Fails if k is negative, and may fail if the result has more than half of
-- 'maxBound' elements.
-- With k = 1, the result is a view of the array, sharing its vector; 'force'
-- copies it out.
rotate :: forall d p a.
          (HasCallStack, KnownNat d,
          1 <= p  -- d is a dimension of the array
          ) =>
          Int -> Array (p + d) a -> Array (p + d + 1) a
rotate k = A . G.rotate @d @p k . unA

-- | Extract a slice of an array.
-- The first argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice [(1,2)] (fromList [4] [1,2,3,4]) == fromList [2] [2,3]@.
-- O(1) time.
slice :: (HasCallStack) => [(Int, Int)] -> Array n a -> Array n a
slice ss = A . G.slice ss . unA

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array, none of those /n/ dimensions
-- may be empty unless the function returns scalars, and the function's results
-- must all have one shape.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: forall n i o a b . (KnownNat n, KnownNat o, KnownNat (n+o)) =>
          (Array i a -> Array o b) -> Array (n+i) a -> Array (n+o) b
rerank f = A . G.rerank (unA . f . A) . unA

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array, none of those /n/ dimensions
-- may be empty unless the function returns scalars, and the function's results
-- must all have one shape.
-- Fails if the arrays differ in those /n/ outermost dimensions.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: forall n i o a b c .
           (HasCallStack, KnownNat n, KnownNat o, KnownNat (n+o)) =>
           (Array i a -> Array i b -> Array o c) -> Array (n+i) a -> Array (n+i) b -> Array (n+o) c
rerank2 f = \ ta tb -> A $ G.rerank2 @n (\ a b -> unA $ f (A a) (A b)) (unA ta) (unA tb)

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- Fails if a given dimension is not one of the array's.
-- O(1) time.
rev :: (HasCallStack) => [Int] -> Array n a -> Array n a
rev rs = A . G.rev rs . unA

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINE reduce #-}
reduce :: forall n a . (a -> a -> a) -> a -> Array n a -> Array 0 a
reduce f z = A . G.reduce f z . unA

-- | Constrained version of 'foldr' for Arrays.
--
-- Note that this 'Array' actually has 'Traversable' anyway.
{-# INLINE foldrA #-}
foldrA :: forall n a b . (a -> b -> b) -> b -> Array n a -> b
foldrA f z = G.foldrA f z . unA

-- | Constrained version of 'traverse' for Arrays.
--
-- Note that this 'Array' actually has 'Traversable' anyway.
{-# INLINE traverseA #-}
traverseA :: forall n f a b . Applicative f => (a -> f b) -> Array n a -> f (Array n b)
traverseA f = fmap A . G.traverseA f . unA

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: forall r a . (Eq a) => Array r a -> Bool
allSameA = G.allSameA . unA

instance (KnownNat r, Arbitrary a) => Arbitrary (Array r a) where arbitrary = A <$> arbitrary

-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: forall r a . (Num a) => Array r a -> a
sumA = G.sumA . unA

-- | Product of all elements.
{-# INLINE productA #-}
productA :: forall r a . (Num a) => Array r a -> a
productA = G.productA . unA

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE maximumA #-}
maximumA :: forall r a . (HasCallStack, Ord a) => Array r a -> a
maximumA = G.maximumA . unA

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE minimumA #-}
minimumA :: forall r a . (HasCallStack, Ord a) => Array r a -> a
minimumA = G.minimumA . unA

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: forall r a . (a -> Bool) -> Array r a -> Bool
anyA p = G.anyA p . unA

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: forall r a . (a -> Bool) -> Array r a -> Bool
allA p = G.allA p . unA

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimensions indices must have the same rank as the argument array
-- and it must be strictly ascending.
-- Fails if an index is not a dimension of the result or the argument's
-- dimensions differ from the result's at those indices.
{-# INLINABLE broadcast #-}
broadcast :: forall r' r a .
             (HasCallStack, KnownNat r') =>
             [Int] -> ShapeL -> Array r a -> Array r' a
broadcast ds sh = A . G.broadcast ds sh . unA

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE update #-}
update :: (HasCallStack) =>
          Array n a -> [([Int], a)] -> Array n a
update a = A . G.update (unA a)

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: forall n a . (HasCallStack, KnownNat n) =>
            ShapeL -> ([Int] -> a) -> Array n a
generate sh = A . G.generate sh

-- | Iterate a function n times.
-- Fails if n is negative.
{-# INLINE iterateN #-}
iterateN :: forall a .
            (HasCallStack) => Int -> (a -> a) -> a -> Array 1 a
iterateN n f = A . G.iterateN n f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: (HasCallStack, Num a) => Int -> Array 1 a
iota = A . G.iota
