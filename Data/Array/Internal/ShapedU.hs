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

{-# LANGUAGE AllowAmbiguousTypes #-}
{-# LANGUAGE CPP #-}
{-# LANGUAGE ConstraintKinds #-}
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
-- A workaround for https://gitlab.haskell.org/ghc/ghc/-/work_items/23050, to go
-- once the GHCs supported carry its fix; DynamicS says more.
#if MIN_VERSION_GLASGOW_HASKELL(9,6,3,0)
{-# OPTIONS_GHC -fno-polymorphic-specialisation #-}
#endif
module Data.Array.Internal.ShapedU(
  Array(..), Shape(..), Size, Rank, Vector, ShapeL, Unbox,
  Window, Stride, Permute, Permutation, ValidDims,
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
  sumA, productA, minimumA, maximumA,
  allA, anyA,
  broadcast,
  update,
  generate, iterateN, iota,
  ) where
import Control.DeepSeq hiding (force)
import Data.Coerce(coerce)
import Data.Data(Data)
import qualified Data.Vector.Unboxed as V
import GHC.Generics(Generic)
import GHC.Stack(HasCallStack)
import GHC.TypeLits(KnownNat, type (+), type (<=))
import Test.QuickCheck hiding (generate)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import Data.Array.Internal.DynamicU()  -- Vector instance
import qualified Data.Array.Internal.Shaped as S
import qualified Data.Array.Internal.ShapedG as G
import Data.Array.Internal(ShapeL, Vector)
import Data.Array.Internal.Shape

type Unbox = V.Unbox

type role Array nominal nominal
newtype Array sh a = A { unA :: G.Array sh V.Vector a }
  deriving (Pretty, Generic, Data)

instance NFData (Array sh a)

instance (Unbox a, Show a, Shape sh) => Show (Array sh a) where
  showsPrec p = showsPrec p . unA

instance (Read a, Unbox a, Shape sh) => Read (Array sh a) where
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array sh V.Vector a) => Eq (Array sh a) where
  x == y = unA x == unA y
  {-# INLINE (==) #-}

instance Ord (G.Array sh V.Vector a) => Ord (Array sh a) where
  compare x y = compare (unA x) (unA y)
  {-# INLINE compare #-}

-- | The number of elements in the array.
{-# INLINE size #-}
size :: forall sh a . (Shape sh) => Array sh a -> Int
size = G.size . unA

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
shapeL :: (Shape sh) => Array sh a -> ShapeL
shapeL = G.shapeL . unA

-- | The rank of an array, i.e., the number of dimensions it has,
-- which is the length of @sh@ in @Array sh a@.
-- O(1) time.
rank :: KnownNat (Rank sh) => Array sh a -> Int
rank = G.rank . unA

-- | Index into an array.  Fails if the index is out of bounds.
-- O(1) time.
{-# INLINE index #-}
index :: forall s sh a . (HasCallStack, KnownNat s) => Array (s:sh) a -> Int -> Array sh a
index a = A . G.index (unA a)

-- | Convert to a list with the elements in the linearization order.
-- O(n) time.
{-# INLINE toList #-}
toList :: forall sh a . (Unbox a, Shape sh) => Array sh a -> [a]
toList = G.toList . unA

-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: forall sh a . (HasCallStack, Unbox a, Shape sh) => [a] -> Array sh a
fromList = A . G.fromList

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: forall sh a . (Unbox a, Shape sh) => Array sh a -> V.Vector a
toVector = G.toVector . unA

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: forall sh a . (HasCallStack, Unbox a, Shape sh) => V.Vector a -> Array sh a
fromVector = A . G.fromVector

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINABLE normalize #-}
normalize :: forall sh a . (Unbox a, Shape sh) => Array sh a -> Array sh a
normalize = A . G.normalize . unA

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  This is
-- especially useful for a view of a large array, such as @'index' a 0@,
-- which keeps the whole vector of @a@ alive, the elements it does not show
-- included: forcing it copies just its own elements and allows the large
-- vector to be garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINABLE force #-}
force :: forall sh a . (Unbox a, Shape sh) => Array sh a -> Array sh a
force = A . G.force . unA

-- | Change the shape of an array.  Type error if the arrays have different number of elements.
-- O(n) or O(1) time.
{-# INLINABLE reshape #-}
reshape :: forall sh' sh a . (Unbox a, Shape sh, Shape sh', Size sh ~ Size sh') =>
           Array sh a -> Array sh' a
reshape = A . G.reshape . unA

-- | Change the size of dimensions with size 1.  These dimension can be changed to any size.
-- All other dimensions must remain the same.
-- O(1) time.
stretch :: forall sh' sh a . (Shape sh', ValidStretch sh sh') => Array sh a -> Array sh' a
stretch = A . G.stretch . unA

-- | Change the size of the outermost dimension by replication.
stretchOuter :: (KnownNat s, Shape sh) => Array (1 : sh) a -> Array (s : sh) a
stretchOuter = A . G.stretchOuter . unA

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
{-# INLINE scalar #-}
scalar :: (Unbox a) => a -> Array '[] a
scalar = A . G.scalar

-- | Convert a scalar (rank 0) array to a value.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: (Unbox a) => Array '[] a -> a
unScalar = G.unScalar . unA

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: forall sh a . (Unbox a, Shape sh) =>
            a -> Array sh a
constant = A . G.constant

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: forall sh a b . (Unbox a, Unbox b, Shape sh) => (a -> b) -> Array sh a -> Array sh b
mapA f = A . G.mapA f . unA

-- | Combine the elements of two arrays.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: forall sh a b c . (Unbox a, Unbox b, Unbox c, Shape sh) => (a -> b -> c) -> Array sh a -> Array sh b -> Array sh c
zipWithA f a b = A $ G.zipWithA f (unA a) (unA b)

-- | Combine the elements of three arrays.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: forall sh a b c d . (Unbox a, Unbox b, Unbox c, Unbox d, Shape sh) => (a -> b -> c -> d) -> Array sh a -> Array sh b -> Array sh c -> Array sh d
zipWith3A f a b c = A $ G.zipWith3A f (unA a) (unA b) (unA c)

-- | Combine the elements of four arrays.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: forall sh a b c d e . (Unbox a, Unbox b, Unbox c, Unbox d, Unbox e, Shape sh) =>
             (a -> b -> c -> d -> e) -> Array sh a -> Array sh b -> Array sh c -> Array sh d -> Array sh e
zipWith4A f a b c d = A $ G.zipWith4A f (unA a) (unA b) (unA c) (unA d)

-- | Combine the elements of five arrays.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: forall sh a b c d e f . (Unbox a, Unbox b, Unbox c, Unbox d, Unbox e, Unbox f, Shape sh) =>
             (a -> b -> c -> d -> e -> f) -> Array sh a -> Array sh b -> Array sh c -> Array sh d -> Array sh e -> Array sh f
zipWith5A f a b c d e = A $ G.zipWith5A f (unA a) (unA b) (unA c) (unA d) (unA e)

-- | Pad each dimension on the low and high side with the given value.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE pad #-}
pad :: forall ps sh' sh a . (HasCallStack, Unbox a, Padded ps sh sh', Shape sh) =>
       a -> Array sh a -> Array sh' a
pad v = A . G.pad @ps v . unA

-- | Do an arbitrary array transposition.
-- The transposition argument, which its type checks, is a permutation of the
-- numbers [0..l-1] for an l no greater than the rank of the array, whose l
-- outermost dimensions it permutes.
-- O(1) time.
transpose :: forall is sh a .
             (HasCallStack, Permutation is, Rank is <= Rank sh, Shape sh, Shape is, KnownNat (Rank sh)) =>
             Array sh a -> Array (Permute is sh) a
transpose = A . G.transpose @is . unA

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- O(n) time.
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINABLE append #-}
append :: forall sh m n a . (Unbox a, Shape sh, KnownNat m, KnownNat n, KnownNat (m+n)) =>
          Array (m ': sh) a -> Array (n ': sh) a -> Array (m+n ': sh) a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the outer extents of the arrays do not sum to that of the result.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE concatOuter #-}
concatOuter :: forall m n sh a . (HasCallStack, Unbox a, KnownNat m, KnownNat n, Shape sh) =>
               [Array (n ': sh) a] -> Array (m ': sh) a
concatOuter = A . G.concatOuter @m @n . coerce

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINABLE ravel #-}
ravel :: forall sh s a . (Unbox a, Shape sh, KnownNat s) =>
         S.Array '[s] (Array sh a) -> Array (s:sh) a
ravel = A . G.ravel . G.mapA unA . S.unA

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@.
{-# INLINABLE unravel #-}
unravel :: forall sh s a . (Shape sh, KnownNat s) =>
           Array (s:sh) a -> S.Array '[s] (Array sh a)
unravel = S.A . G.mapA A . G.unravel . unA

-- | Make a window of the outermost dimensions.
-- The rank increases with the length of the window list.
-- E.g., if the shape of the array is @[10,12,8]@ and
-- the window size is @[3,3]@ then the resulting array will have shape
-- @[8,10,3,3,8]@.
--
-- E.g., @window \@'[2] (fromList \@'[4] [1,2,3,4]) == fromList \@'[3,2] [1,2, 2,3, 3,4]@
-- O(1) time.
--
-- If the window type parameter @ws = '[w1,...,wk]@ and @wa = window \@ws a@ then
-- @wa `index` i1 ... `index` ik == slice \@'[ '(i1,w1),...,'(ik,wk)] a@.
{-# INLINABLE window #-}
window :: forall ws sh' sh a .
          (Window ws sh sh', KnownNat (Rank ws), Shape sh') =>
          Array sh a -> Array sh' a
window = A . G.window @ws . unA

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- O(1) time.
stride :: forall ts sh' sh a .
          (Stride ts sh sh', Shape ts) =>
          Array sh a -> Array sh' a
stride = A . G.stride @ts . unA

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- May fail if the result has more than half of 'maxBound' elements.
-- With k = 1, the result is a view of the array, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE rotate #-}
rotate :: forall d k sh a .
          (HasCallStack, KnownNat d, KnownNat k, Unbox a, Shape sh,
           d + 1 <= Rank sh, Shape (Take d sh ++ (k ': Drop d sh))) =>
          Array sh a -> Array (Take d sh ++ (k ': Drop d sh)) a
rotate = A . G.rotate @d @k . unA

-- | Extract a slice of an array.
-- The first type argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice \@'[ '(1,2)] (fromList \@'[4] [1,2,3,4]) == fromList \@'[2] [2,3]@.
-- O(1) time.
slice :: forall sl sh' sh a .
         (Slice sl sh sh') =>
         Array sh a -> Array sh' a
slice = A . G.slice @sl . unA

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: forall n i o sh a b .
          (Unbox b,
           Drop n sh ~ i, Shape sh, KnownNat n, Shape o, Shape (Take n sh ++ o)) =>
          (Array i a -> Array o b) -> Array sh a -> Array (Take n sh ++ o) b
rerank f = A . G.rerank @n (unA . f . A) . unA

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: forall n i o sh a b c .
           (Unbox c,
            Drop n sh ~ i, Shape sh, KnownNat n, Shape o, Shape (Take n sh ++ o)) =>
           (Array i a -> Array i b -> Array o c) -> Array sh a -> Array sh b -> Array (Take n sh ++ o) c
rerank2 f = \ ta tb -> A $ G.rerank2 @n (\ a b -> unA $ f (A a) (A b)) (unA ta) (unA tb)

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- O(1) time.
rev :: forall rs sh a . (ValidDims rs sh, Shape rs, Shape sh) =>
       Array sh a -> Array sh a
rev = A . G.rev @rs . unA

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINE reduce #-}
reduce :: forall sh a . (Unbox a, Shape sh) => (a -> a -> a) -> a -> Array sh a -> Array '[] a
reduce f z = A . G.reduce f z . unA

-- | Constrained version of 'foldr' for Arrays.
{-# INLINE foldrA #-}
foldrA :: forall sh a b . (Unbox a, Shape sh) => (a -> b -> b) -> b -> Array sh a -> b
foldrA f z = G.foldrA f z . unA

-- | Constrained version of 'traverse' for Arrays.
{-# INLINE traverseA #-}
traverseA
  :: forall sh a b f . (Unbox a, Unbox b, Applicative f, Shape sh)
  => (a -> f b) -> Array sh a -> f (Array sh b)
traverseA f = fmap A . G.traverseA f . unA

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Shape sh, Unbox a, Eq a) => Array sh a -> Bool
allSameA = G.allSameA . unA

instance (Shape sh, Arbitrary a, Unbox a) => Arbitrary (Array sh a) where arbitrary = A <$> arbitrary
-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: forall sh a . (Unbox a, Num a, Shape sh) => Array sh a -> a
sumA = G.sumA . unA

-- | Product of all elements.
{-# INLINE productA #-}
productA :: forall sh a . (Unbox a, Num a, Shape sh) => Array sh a -> a
productA = G.productA . unA

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
{-# INLINE maximumA #-}
maximumA :: forall sh a . (Unbox a, Ord a, Shape sh, 1 <= Size sh) => Array sh a -> a
maximumA = G.maximumA . unA

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
{-# INLINE minimumA #-}
minimumA :: forall sh a . (Unbox a, Ord a, Shape sh, 1 <= Size sh) => Array sh a -> a
minimumA = G.minimumA . unA

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: (Shape sh, Unbox a) => (a -> Bool) -> Array sh a -> Bool
anyA p = G.anyA p . unA

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: (Shape sh, Unbox a) => (a -> Bool) -> Array sh a -> Bool
allA p = G.allA p . unA

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimensions indices must have the same rank as the argument array
-- and it must be strictly ascending.
{-# INLINABLE broadcast #-}
broadcast :: forall ds sh' sh a .
             (Unbox a, Shape sh, Shape sh',
              G.Broadcast ds sh sh') =>
             Array sh a -> Array sh' a
broadcast = A . G.broadcast @ds @sh' @sh . unA

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE update #-}
update :: forall sh a . (HasCallStack, Unbox a, Shape sh) =>
          Array sh a -> [([Int], a)] -> Array sh a
update a = A . G.update (unA a)

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: forall sh a . (Unbox a, Shape sh) => ([Int] -> a) -> Array sh a
generate = A . G.generate

-- | Iterate a function n times.
{-# INLINE iterateN #-}
iterateN :: forall n a .
            (Unbox a, KnownNat n) => (a -> a) -> a -> Array '[n] a
iterateN f = A . G.iterateN f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
{-# INLINE iota #-}
iota :: (KnownNat n, Unbox a, Num a) => Array '[n] a
iota = A G.iota
