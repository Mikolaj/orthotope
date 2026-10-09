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
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RankNTypes #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE UndecidableInstances #-}
-- The structural operations here constrain the element by nothing a client
-- could specialise them on, so the copies this module makes of the INLINABLE
-- functions it calls, for the vector type alone, are their specialisations, and
-- only -fpolymorphic-specialisation makes them, off by default before GHC HEAD:
-- without it, on 9.12.4, a boxed reshape, pad or append took 5 to 8 times as
-- long on a transposed [400, 500] view of Doubles.  9.6.3 is the first GHC to
-- know the flag, and DynamicS turns it off for the opposite reason.
#if MIN_VERSION_GLASGOW_HASKELL(9,6,3,0)
{-# OPTIONS_GHC -fpolymorphic-specialisation #-}
#endif
module Data.Array.Internal.Dynamic(
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
import Control.Monad.ST(ST)
import Data.Coerce(coerce)
import Data.Data(Data)
import Data.Vector.Fusion.Util(Box(..))
import GHC.Generics(Generic)
import qualified Data.Vector as V
import qualified Data.Vector.Mutable as MV
import GHC.Stack(HasCallStack)
import Test.QuickCheck hiding (generate)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import qualified Data.Array.DynamicG as G
import Data.Array.Internal(ShapeL, Vector(..), None, genericUnsafeFillStrided, rnfViewT)
import qualified Data.Array.Internal.DynamicG as DG

instance Vector V.Vector where
  type VecElem V.Vector = None
  {-# INLINE vIndex #-}
  vIndex = (V.!)
  {-# INLINE vUnsafeIndex #-}
  vUnsafeIndex = V.unsafeIndex
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
  {-# INLINE vMap #-}
  vMap = fmap
  -- The zips write each result unevaluated over the indices, reading the
  -- elements unforced, as vector's own do, whose stream state, an index for
  -- each vector and the element held between them, stays boxed without the
  -- SpecConstr of -O2.  On GHC HEAD with vector patched as issue 570 proposes,
  -- on views of 200000 Doubles, zipWithA to zipWith5A took 0.44 to 0.82 of
  -- their time at -O1 and rerank2 of zipWithA 0.62; with -fspec-constr, 0.94 to
  -- 1.03, but zipWith5A, whose stream SpecConstr leaves boxed, 0.50 to 0.62,
  -- allocating 120 bytes an element where 528.  The same loop gained nothing
  -- for vGenerate, which keeps vector's own.
  {-# INLINE vZipWith #-}
  vZipWith f a b = zipLoop (V.length a `min` V.length b) $ \ i ->
    f <$> V.unsafeIndexM a i <*> V.unsafeIndexM b i
  {-# INLINE vZipWith3 #-}
  vZipWith3 f a b c =
    zipLoop (V.length a `min` V.length b `min` V.length c) $ \ i ->
      f <$> V.unsafeIndexM a i <*> V.unsafeIndexM b i <*> V.unsafeIndexM c i
  {-# INLINE vZipWith4 #-}
  vZipWith4 f a b c d =
    zipLoop (V.length a `min` V.length b `min` V.length c
             `min` V.length d) $ \ i ->
      f <$> V.unsafeIndexM a i <*> V.unsafeIndexM b i <*> V.unsafeIndexM c i
        <*> V.unsafeIndexM d i
  {-# INLINE vZipWith5 #-}
  vZipWith5 f a b c d e =
    zipLoop (V.length a `min` V.length b `min` V.length c `min` V.length d
             `min` V.length e) $ \ i ->
      f <$> V.unsafeIndexM a i <*> V.unsafeIndexM b i <*> V.unsafeIndexM c i
        <*> V.unsafeIndexM d i <*> V.unsafeIndexM e i
  {-# INLINE vAppend #-}
  vAppend = (V.++)
  {-# INLINE vConcat #-}
  -- The empty list by hand: without -fspec-constr, off at -O, GHC keeps
  -- V.concat []'s copy loop wherever it is inlined, and CSE keeps the
  -- copies apart (https://gitlab.haskell.org/ghc/ghc/-/work_items/27892).
  vConcat [] = V.empty
  vConcat vs = V.concat vs
  {-# INLINE vFold #-}
  vFold = V.foldl'
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
  -- vAll and vAny read each element by index through unsafeIndexM, which hands
  -- the predicate the element stored, where unsafeIndex would hand it a thunk
  -- of the read.  On GHC HEAD with vector patched as issue 570 proposes, on
  -- views of 200000 Doubles, they ran 0.96 of the instructions of vector's own
  -- at -O1 and as many with -fspec-constr; their times, varying from run to run
  -- by up to 1.55 times, showed no difference.
  {-# INLINE vAll #-}
  vAll q v = go 0
    where !n = V.length v
          go !i | i >= n = True
                | otherwise = case V.unsafeIndexM v i of
                    Box x -> q x && go (i + 1)
  -- Read as vAll's are.
  {-# INLINE vAny #-}
  vAny q v = go 0
    where !n = V.length v
          go !i | i >= n = False
                | otherwise = case V.unsafeIndexM v i of
                    Box x -> q x || go (i + 1)
  -- The element stored, unforced, read through unsafeIndexM, which hands it on
  -- without the thunk of the read that vUnsafeIndex would leave in a list of a
  -- view's elements ('elemsT').
  {-# INLINE vUnsafeWithElem #-}
  vUnsafeWithElem v i k = case V.unsafeIndexM v i of Box x -> k x
  -- Each element forced as it is written.
  {-# INLINE vGenerate' #-}
  vGenerate' n g = zipLoop (max 0 n) (\ i -> return $! g i)
  {-# INLINE vUnsafeFillStrided #-}
  vUnsafeFillStrided = genericUnsafeFillStrided 5
  -- vUnsafeConcatN keeps the default, the vector package's concat but for a
  -- lone vector: on GHC HEAD, copying each vector as the list yields it, as
  -- genericUnsafeConcatN does, took 0.95 to 1.28 times as long on boxed
  -- vectors of 500 elements or more at a 32 MB allocation area and 1.22
  -- to 2.21 at 4 MB, running 1.02 to 1.41 and 1.35 to 2.88 times the
  -- instructions, though it took 0.41 to 0.79 and 0.50 to 0.76 of the time
  -- on rows of 2 to 8 elements.

-- A vector of n elements, the ith what the action at i returns, written
-- unevaluated.
{-# INLINE zipLoop #-}
zipLoop :: Int -> (forall s. Int -> ST s a) -> V.Vector a
zipLoop !n g = V.create $ do
  mv <- MV.unsafeNew n
  let go !i | i >= n = return mv
            | otherwise = do
                x <- g i
                MV.unsafeWrite mv i x
                go (i + 1)
  go 0

type role Array nominal
newtype Array a = A { unA :: G.Array V.Vector a }
  deriving (Pretty, Generic, Data)

instance NFData a => NFData (Array a) where
  rnf (A (DG.A sh t)) = rnf sh `seq` rnfViewT sh t
  {-# INLINE rnf #-}

instance (Show a) => Show (Array a) where
  showsPrec p = showsPrec p . unA

instance (Read a) => Read (Array a) where
  readsPrec p s = [(A a, r) | (a, r) <- readsPrec p s]

instance Eq (G.Array V.Vector a) => Eq (Array a) where
  x == y = unA x == unA y
  {-# INLINE (==) #-}

instance Ord (G.Array V.Vector a) => Ord (Array a) where
  compare x y = compare (unA x) (unA y)
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
toList :: Array a -> [a]
toList = G.toList . unA

-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: (HasCallStack) => ShapeL -> [a] -> Array a
fromList ss = A . G.fromList ss

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: Array a -> V.Vector a
toVector = G.toVector . unA

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: (HasCallStack) => ShapeL -> V.Vector a -> Array a
fromVector ss = A . G.fromVector ss

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINABLE normalize #-}
normalize :: Array a -> Array a
normalize = A . G.normalize . unA

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  This is
-- especially useful for a view of a large array, such as @'index' a 0@,
-- which keeps the whole vector of @a@ alive, the elements it does not show
-- included: forcing it copies just its own elements and allows the large
-- vector to be garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINABLE force #-}
force :: Array a -> Array a
force = A . G.force . unA

-- | Change the shape of an array.  Fails if the arrays have different number of elements.
-- O(n) or O(1) time.
reshape :: (HasCallStack) => ShapeL -> Array a -> Array a
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
scalar :: a -> Array a
scalar = A . G.scalar

-- | Convert a scalar (rank 0) array to a value.
-- Fails if the array is not a scalar.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: (HasCallStack) => Array a -> a
unScalar = G.unScalar . unA

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: (HasCallStack) => ShapeL -> a -> Array a
constant sh = A . G.constant sh

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: (a -> b) -> Array a -> Array b
mapA f = A . G.mapA f . unA

instance Functor Array where
  fmap = mapA

instance Foldable Array where
  foldr = foldrA

instance Traversable Array where
  traverse = traverseA

-- | Combine the elements of two arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: (HasCallStack) => (a -> b -> c) -> Array a -> Array b -> Array c
zipWithA f a b = A $ G.zipWithA f (unA a) (unA b)

-- | Combine the elements of three arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: (HasCallStack) => (a -> b -> c -> d) -> Array a -> Array b -> Array c -> Array d
zipWith3A f a b c = A $ G.zipWith3A f (unA a) (unA b) (unA c)

-- | Combine the elements of four arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: (HasCallStack) => (a -> b -> c -> d -> e) -> Array a -> Array b -> Array c -> Array d -> Array e
zipWith4A f a b c d = A $ G.zipWith4A f (unA a) (unA b) (unA c) (unA d)

-- | Combine the elements of five arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: (HasCallStack) => (a -> b -> c -> d -> e -> f) -> Array a -> Array b -> Array c -> Array d -> Array e -> Array f
zipWith5A f a b c d e = A $ G.zipWith5A f (unA a) (unA b) (unA c) (unA d) (unA e)

-- | Pad each dimension on the low and high side with the given value.
-- Fails if the padding list is longer than the rank or a padding is negative.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE pad #-}
pad :: (HasCallStack) => [(Int, Int)] -> a -> Array a -> Array a
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
append :: (HasCallStack) => Array a -> Array a -> Array a
append x y = A $ G.append (unA x) (unA y)

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE concatOuter #-}
concatOuter :: (HasCallStack) => [Array a] -> Array a
concatOuter = A . G.concatOuter . coerce

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- Fails if the outer array does not have rank 1.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINABLE ravel #-}
ravel :: (HasCallStack) => Array (Array a) -> Array a
ravel = A . G.ravel . G.mapA unA . unA

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@ where the outermost dimension is not empty.
-- Fails if the array has rank 0.
{-# INLINABLE unravel #-}
unravel :: (HasCallStack) => Array a -> Array (Array a)
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
rotate :: (HasCallStack) => Int -> Int -> Array a -> Array a
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
-- The /n/ must be from 0 to the rank of the array, none of those /n/ dimensions
-- may be empty, and the function's results must all have one shape.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: (HasCallStack) => Int -> (Array a -> Array b) -> Array a -> Array b
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
rerank2 :: (HasCallStack) => Int -> (Array a -> Array b -> Array c) -> Array a -> Array b -> Array c
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
reduce :: (a -> a -> a) -> a -> Array a -> Array a
reduce f z = A . G.reduce f z . unA

-- | Constrained version of 'foldr' for Arrays.
--
-- Note that this 'Array' actually has 'Traversable' anyway.
{-# INLINE foldrA #-}
foldrA :: (a -> b -> b) -> b -> Array a -> b
foldrA f z = G.foldrA f z . unA

-- | Constrained version of 'traverse' for Arrays.
--
-- Note that this 'Array' actually has 'Traversable' anyway.
{-# INLINE traverseA #-}
traverseA :: Applicative f => (a -> f b) -> Array a -> f (Array b)
traverseA f = fmap A . G.traverseA f . unA

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Eq a) => Array a -> Bool
allSameA = G.allSameA . unA

instance Arbitrary a => Arbitrary (Array a) where arbitrary = A <$> arbitrary

-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: (Num a) => Array a -> a
sumA = G.sumA . unA

-- | Product of all elements.
{-# INLINE productA #-}
productA :: (Num a) => Array a -> a
productA = G.productA . unA

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE maximumA #-}
maximumA :: (HasCallStack, Ord a) => Array a -> a
maximumA = G.maximumA . unA

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE minimumA #-}
minimumA :: (HasCallStack, Ord a) => Array a -> a
minimumA = G.minimumA . unA

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: (a -> Bool) -> Array a -> Bool
anyA p = G.anyA p . unA

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: (a -> Bool) -> Array a -> Bool
allA p = G.allA p . unA

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimensions indices must have the same rank as the argument array
-- and it must be strictly ascending.
-- Fails if an index is not a dimension of the result or the argument's
-- dimensions differ from the result's at those indices.
{-# INLINABLE broadcast #-}
broadcast :: (HasCallStack) =>
             [Int] -> ShapeL -> Array a -> Array a
broadcast ds sh = A . G.broadcast ds sh . unA

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE update #-}
update :: (HasCallStack) =>
          Array a -> [([Int], a)] -> Array a
update a = A . G.update (unA a)

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: (HasCallStack) => ShapeL -> ([Int] -> a) -> Array a
generate sh = A . G.generate sh

-- | Iterate a function n times.
-- Fails if n is negative.
{-# INLINE iterateN #-}
iterateN :: (HasCallStack) => Int -> (a -> a) -> a -> Array a
iterateN n f = A . G.iterateN n f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: (HasCallStack, Num a) => Int -> Array a
iota = A . G.iota
