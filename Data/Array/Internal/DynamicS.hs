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
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE InstanceSigs #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}
-- On GHC HEAD, where -fpolymorphic-specialisation is on by default,
-- the specialiser copies the INLINABLE functions this module calls
-- for the vector type alone and rewrites the unfoldings this
-- module exports to call the copies.  A copy has no unfolding
-- (https://gitlab.haskell.org/ghc/ghc/-/work_items/23050), so a client cannot
-- specialise it on the element type: on a transposed [400, 500] view of
-- Doubles, pad and rotate took 19 and 8 times as long as with the flag off.
-- The flag is off in all six Storable and Unboxed modules: off in the Dynamic
-- ones alone, it left the Ranked and Shaped ones, which import DynamicS and
-- DynamicU for their instances, making the copies instead.  It can go once
-- the GHCs supported carry the fix of that issue: with the copies' unfoldings
-- exposed, as -fexpose-overloaded-unfoldings does, clients specialised pad and
-- rotate again.  9.6.3 is the first GHC to know the flag.
#if MIN_VERSION_GLASGOW_HASKELL(9,6,3,0)
{-# OPTIONS_GHC -fno-polymorphic-specialisation #-}
#endif
module Data.Array.Internal.DynamicS(
  Array(..), Vector, ShapeL, V.Storable, Unbox,
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
  bitcast,
  ) where
import Control.DeepSeq hiding (force)
import Data.Coerce(coerce)
import Data.Data(Data)
import qualified Data.Vector.Storable as V
import Foreign.Storable(sizeOf)
import GHC.Generics(Generic)
import GHC.Exts(build)
import GHC.Stack(HasCallStack)
import Test.QuickCheck hiding (generate)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import qualified Data.Array.Internal.Dynamic as D
import qualified Data.Array.Internal.DynamicG as G
import Data.Array.Internal(Axes, T(..), ShapeL, Vector(..), genericUnsafeConcatN,
                           genericUnsafeFillStrided)

type Unbox = V.Storable

instance Vector V.Vector where
  type VecElem V.Vector = Unbox
  {-# INLINE vIndex #-}
  vIndex = (V.!)
  {-# INLINE vUnsafeIndex #-}
  vUnsafeIndex = V.unsafeIndex
  {-# INLINE vLength #-}
  vLength = V.length
  -- vToList, vFold, vAll and vAny hand each element to a function of the
  -- client's, so they read it by index and force it, where vector's own hand on
  -- Storable's read as a thunk (https://github.com/haskell/vector/issues/570)
  -- that a function GHC cannot see into, or a consumer keeping the elements,
  -- as traverseA does, takes as it is, 40 bytes an element holding the vector.
  -- On GHC HEAD with the issue fixed and -fspec-constr, the operations reading
  -- through them took 0.95 to 1.02 of their time; at -O1, anyA and allA took
  -- 0.61 and 0.91 of it, fixed or not.  vSum, vProduct, vMaximum and vMinimum
  -- keep vector's own: their functions are the element's class methods, which a
  -- call the client specialises knows, so the read is no thunk there.
  {-# INLINE vToList #-}
  vToList v = build $ \ cons nil ->
    let !n = V.length v
        go !i | i >= n = nil
              | otherwise = let !x = V.unsafeIndex v i in cons x (go (i + 1))
    in  go 0
  {-# INLINE vFromList #-}
  vFromList = V.fromList
  {-# INLINE vFromListN #-}
  vFromListN = V.fromListN
  {-# INLINE vSingleton #-}
  vSingleton = V.singleton
  {-# INLINE vReplicate #-}
  vReplicate = V.replicate
  -- The map and the zips generate their result over the indices, working
  -- around vector's own, whose stream-fused loops allocate per element:
  -- a zipWith on Doubles 112 bytes an element at -O1, against 8, taking
  -- through zipWithA and zipWith3A 7 to 49 times as long, and still 64
  -- with the SpecConstr of -O2, 56 of them the lazy element read of
  -- https://github.com/haskell/vector/issues/570.  No fusion is given up:
  -- vector's fuse with a vector they read, but each array operation stores its
  -- result, so the array operations never fused their inputs; a map of a map
  -- allocates one vector per map, with vector's map as with this one.
  -- Each read is forced before the function takes it: given a function GHC
  -- cannot see into, on GHC HEAD with vector's issue 570 fixed, on views of
  -- 200000 Doubles, mapA allocated 40 bytes an element where 80 and zipWithA
  -- 72 where 152, and given known functions every operation ran as many
  -- instructions as before.
  {-# INLINE vMap #-}
  vMap f v = V.generate (V.length v) (\ i -> let !x = V.unsafeIndex v i in f x)
  {-# INLINE vZipWith #-}
  vZipWith f a b =
    V.generate (V.length a `min` V.length b) $ \ i ->
      let !x = V.unsafeIndex a i
          !y = V.unsafeIndex b i
      in  f x y
  {-# INLINE vZipWith3 #-}
  vZipWith3 f a b c =
    V.generate (V.length a `min` V.length b `min` V.length c) $ \ i ->
      let !x = V.unsafeIndex a i
          !y = V.unsafeIndex b i
          !z = V.unsafeIndex c i
      in  f x y z
  {-# INLINE vZipWith4 #-}
  vZipWith4 f a b c d =
    V.generate (V.length a `min` V.length b `min` V.length c
                `min` V.length d) $ \ i ->
      let !x = V.unsafeIndex a i
          !y = V.unsafeIndex b i
          !z = V.unsafeIndex c i
          !u = V.unsafeIndex d i
      in  f x y z u
  {-# INLINE vZipWith5 #-}
  vZipWith5 f a b c d e =
    V.generate (V.length a `min` V.length b `min` V.length c
                `min` V.length d `min` V.length e) $ \ i ->
      let !x = V.unsafeIndex a i
          !y = V.unsafeIndex b i
          !z = V.unsafeIndex c i
          !u = V.unsafeIndex d i
          !w = V.unsafeIndex e i
      in  f x y z u w
  {-# INLINE vAppend #-}
  vAppend = (V.++)
  {-# INLINE vConcat #-}
  -- The empty list by hand: without -fspec-constr, off at -O, GHC keeps
  -- V.concat []'s copy loop wherever it is inlined, and CSE keeps the
  -- copies apart (https://gitlab.haskell.org/ghc/ghc/-/work_items/27892).
  vConcat [] = V.empty
  vConcat vs = V.concat vs
  -- Each element read forced, as at vToList.
  {-# INLINE vFold #-}
  vFold f z v = go z 0
    where !n = V.length v
          go !acc !i | i >= n = acc
                     | otherwise =
                         let !x = V.unsafeIndex v i in go (f acc x) (i + 1)
  {-# INLINE vSlice #-}
  vSlice = V.slice
  {-# INLINE vUnsafeSlice #-}
  vUnsafeSlice = V.unsafeSlice
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
  -- Each element read forced, as at vToList.
  {-# INLINE vAll #-}
  vAll q v = go 0
    where !n = V.length v
          go !i | i >= n = True
                | otherwise = let !x = V.unsafeIndex v i in q x && go (i + 1)
  -- Each element read forced, as at vToList.
  {-# INLINE vAny #-}
  vAny q v = go 0
    where !n = V.length v
          go !i | i >= n = False
                | otherwise = let !x = V.unsafeIndex v i in q x || go (i + 1)
  -- Forced, as at vToList, so a peek that fails fails here.
  {-# INLINE vUnsafeWithElem #-}
  vUnsafeWithElem v i k = let !x = V.unsafeIndex v i in k x
  {-# INLINE vGenerate' #-}
  vGenerate' = V.generate
  {-# INLINE vUnsafeFillStrided #-}
  vUnsafeFillStrided :: forall a. Unbox a
               => Axes -> Int -> Int -> V.Vector a -> V.Vector a
  vUnsafeFillStrided = genericUnsafeFillStrided (512 `quot` max 1 (sizeOf (undefined :: a)))
  {-# INLINE vUnsafeConcatN #-}
  vUnsafeConcatN = genericUnsafeConcatN

type role Array nominal
newtype Array a = A { unA :: G.Array V.Vector a }
  deriving (Pretty, Generic, Data)

instance NFData (Array a)

instance (Show a, Unbox a) => Show (Array a) where
  showsPrec p = showsPrec p . unA

instance (Read a, Unbox a) => Read (Array a) where
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array V.Vector a) => Eq (Array a) where
  x == y = unA x == unA y
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
-- Fails if the given shape does not have the same number of elements as the vector.
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
{-# INLINABLE normalize #-}
normalize :: (Unbox a) => Array a -> Array a
normalize = A . G.normalize . unA

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  This is
-- especially useful for a view of a large array, such as @'index' a 0@,
-- which keeps the whole vector of @a@ alive, the elements it does not show
-- included: forcing it copies just its own elements and allows the large
-- vector to be garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINABLE force #-}
force :: (Unbox a) => Array a -> Array a
force = A . G.force . unA

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
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
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
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINABLE append #-}
append :: (HasCallStack, Unbox a) => Array a -> Array a -> Array a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE concatOuter #-}
concatOuter :: (HasCallStack, Unbox a) => [Array a] -> Array a
concatOuter = A . G.concatOuter . coerce

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- Fails if the outer array does not have rank 1.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
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

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- Fails if d is not a dimension of the array or k is negative, and may fail
-- if the result has more than half of 'maxBound' elements.
-- With k = 1, the result is a view of the array, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE rotate #-}
rotate :: (HasCallStack, Unbox a) => Int -> Int -> Array a -> Array a
rotate d k = A . G.rotate d k . unA

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
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: (HasCallStack, Unbox a, Unbox b) => Int -> (Array a -> Array b) -> Array a -> Array b
rerank n f = A . G.rerank n (unA . f . A) . unA

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array, and none of those /n/
-- dimensions may be empty.
-- Fails if the arrays differ in those /n/ outermost dimensions.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: (HasCallStack, Unbox a, Unbox b, Unbox c) =>
           Int -> (Array a -> Array b -> Array c) -> Array a -> Array b -> Array c
rerank2 n f = \ ta tb -> A $ G.rerank2 n (\ a b -> unA $ f (A a) (A b)) (unA ta) (unA tb)

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- Fails if a given dimension is not one of the array's.
-- O(1) time.
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
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
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
-- Each element is evaluated to weak head normal form as it is stored.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: (HasCallStack, Unbox a, Num a) => Int -> Array a
iota = A . G.iota

-- | Convert between types by just reinterpreting the bits as another type.
-- For instance the floating point number @(1.5 :: Float)@ will convert to
-- @(0x3fc00000 :: Word32)@ since they have the same bit representation.
-- Fails if the two types differ in size.
{-# INLINE bitcast #-}
bitcast :: forall a b . (HasCallStack, Unbox a, Unbox b) => Array a -> Array b
bitcast (A (G.A sh (T ss o v)))
  | sza /= szb
  = error $ "bitcast: the types must have the same size. " ++ show (sza, szb)
  | otherwise
  = A (G.A sh (T ss o (V.unsafeCast v)))
  where sza = sizeOf (undefined :: a)
        szb = sizeOf (undefined :: b)
