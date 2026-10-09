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
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE ExplicitNamespaces #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE KindSignatures #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE UndecidableInstances #-}
-- | Arrays of static size.  The arrays are polymorphic in the underlying
-- linear data structure used to store the actual values.
module Data.Array.Internal.ShapedG(
  Array(..), Shape(..), Size, Rank, Vector, ShapeL, VecElem,
  Window, Stride, Permute, Permutation, ValidDims,
  Broadcast,
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
  anyA, allA,
  broadcast,
  update,
  generate, iterateN, iota,
  ) where
import Control.DeepSeq hiding (force)
import Data.Data(Data)
import Data.Proxy(Proxy(..))
import GHC.Generics(Generic)
import GHC.Stack(HasCallStack)
import GHC.TypeLits(Nat, type (<=), KnownNat, type (+))
import Test.QuickCheck hiding (generate)
import Text.PrettyPrint.HughesPJClass

import Data.Array.Internal
import qualified Data.Array.Internal.DynamicG as DG
import Data.Array.Internal.Shape

-- | Arrays stored in a /v/ with values of type /a/.
type role Array nominal representational nominal
newtype Array (sh :: [Nat]) v a = A (T v a)
  deriving (Generic, Data)

instance (Vector v, Show a, VecElem v a, Shape sh) => Show (Array sh v a) where
  {-# INLINABLE showsPrec #-}
  showsPrec p a@(A _) = showParen (p > 10) $
    showString "fromList @" . showsPrec 11 (shapeL a) . showString" " . showsPrec 11 (toList a)

instance (Shape sh, Vector v, Read a, VecElem v a) => Read (Array sh v a) where
  readsPrec p = readParen (p > 10) $ \ r1 ->
    [(fromList xs, r4)
    | ("fromList", r2) <- lex r1, ("@", r2') <- lex r2
    , (s, r3) <- readsPrec 11 r2', (xs, r4) <- readsPrec 11 r3
    , s == shapeP (Proxy :: Proxy sh), product s == length xs]

instance (Vector v, Eq a, VecElem v a, Shape sh)
         => Eq (Array sh v a) where
  a@(A v) == (A v') = equalT (shapeL a) (shapeL a) v v'
  {-# INLINE (==) #-}

instance (Vector v, Ord a, VecElem v a, Shape sh)
         => Ord (Array sh v a) where
  a@(A v) `compare` (A v') = compareT (shapeL a) v v'
  {-# INLINE compare #-}

instance (Vector v, Pretty a, VecElem v a, Shape sh) => Pretty (Array sh v a) where
  pPrintPrec l p a@(A t) = ppT l p (shapeL a) t

instance (NFData (v a)) => NFData (Array sh v a) where
  rnf (A t) = rnf t

-- | The number of elements in the array.
{-# INLINE size #-}
size :: forall sh v a . (Shape sh) => Array sh v a -> Int
size _ = sizeP (Proxy :: Proxy sh)

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
{-# INLINE shapeL #-}
shapeL :: forall sh v a . (Shape sh) => Array sh v a -> ShapeL
shapeL _ = shapeP (Proxy :: Proxy sh)

-- | The rank of an array, i.e., the number of dimensions it has.
-- O(1) time.
{-# INLINE rank #-}
rank :: forall sh v a . KnownNat (Rank sh) => Array sh v a -> Int
rank _ = valueOf @(Rank sh)

-- | Index into an array.  Fails if the index is out of bounds.
-- O(1) time.
{-# INLINE index #-}
index :: forall s sh v a . (HasCallStack, KnownNat s) =>
         Array (s:sh) v a -> Int -> Array sh v a
index (A t) i | i < 0 || i >= s = error $ "index: out of bounds " ++ show (i, s)
              | otherwise = A $ indexT t i
  where s = natT @s

-- | Convert to a list with the elements in the linearization order.
-- O(n) time.
{-# INLINE toList #-}
toList :: forall sh v a . (Vector v, VecElem v a, Shape sh) => Array sh v a -> [a]
toList a@(A t) = toListT (shapeL a) t

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: forall sh v a . (Vector v, VecElem v a, Shape sh) => Array sh v a -> v a
toVector a@(A t) = toVectorT (shapeL a) t

-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: forall sh v a . (HasCallStack, Vector v, VecElem v a, Shape sh) =>
            [a] -> Array sh v a
fromList vs | n /= l = error $ "fromList: size mismatch " ++ show (n, l)
            | otherwise = A $ T st 0 $ vFromListN l vs
  where n : st = getStridesT ss
        l = length vs
        ss = shapeP (Proxy :: Proxy sh)

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: forall sh v a . (HasCallStack, Vector v, VecElem v a, Shape sh) =>
              v a -> Array sh v a
fromVector v | n /= l = error $ "fromVector: size mismatch " ++ show (n, l)
             | otherwise = A $ T st 0 v
  where n : st = getStridesT ss
        l = vLength v
        ss = shapeP (Proxy :: Proxy sh)

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINE normalize #-}
normalize :: forall sh v a . (Vector v, VecElem v a, Shape sh) => Array sh v a -> Array sh v a
normalize a@(A t) = A $ normalizeT (shapeL a) t

-- | Copy the elements of the array into a vector of their own, in the
-- linearization order, sharing no storage with another array.  At the list
-- instance, whose 'vForce' is the identity, a whole list is not copied, and
-- a lazy result keeps alive what its unevaluated parts refer to.  This is
-- especially useful for a view of a large array, such as @'index' a 0@, which
-- keeps the whole vector of @a@ alive, the elements it does not show included:
-- forcing it copies just its own elements and allows the large vector to be
-- garbage collected, if nothing else refers to it.
-- O(n) time.
{-# INLINE force #-}
force :: forall sh v a . (Vector v, VecElem v a, Shape sh) => Array sh v a -> Array sh v a
force a@(A t) = A $ forceT (shapeL a) t

-- | Change the shape of an array.  Type error if the arrays have different number of elements.
-- O(n) or O(1) time.
{-# INLINE reshape #-}
reshape :: forall sh' sh v a .
           (Vector v, VecElem v a, Shape sh, Shape sh', Size sh ~ Size sh') =>
           Array sh v a -> Array sh' v a
reshape a = reshape' (shapeP (Proxy :: Proxy sh')) (shapeL a) a

{-# INLINABLE reshape' #-}
reshape' :: (Vector v, VecElem v a) =>
            ShapeL -> ShapeL -> Array sh v a -> Array sh' v a
reshape' sh sh' (A t@(T ost oo v))
  | vLength v == 1 = A $ T (map (const 0) sh) 0 v  -- Fast special case for singleton vector
  | Just nst <- simpleReshape ost sh' sh = A $ T nst oo v
  | otherwise = A $ fromVectorT sh $ toVectorT sh' t

-- | Change the size of dimensions with size 1.  These dimension can be changed to any size.
-- All other dimensions must remain the same.
-- O(1) time.
{-# INLINE stretch #-}
stretch :: forall sh' sh v a . (Shape sh', ValidStretch sh sh') =>
           Array sh v a -> Array sh' v a
stretch a = sizeP (Proxy :: Proxy sh') `seq`  -- the result's size checked now
            stretch' (stretching (Proxy :: Proxy sh) (Proxy :: Proxy sh')) a

stretch' :: [Bool] -> Array sh v a -> Array sh' v a
stretch' str (A vs) = A $ stretchT str vs

-- | Change the size of the outermost dimension by replication.
{-# INLINE stretchOuter #-}
stretchOuter :: forall s sh v a . (KnownNat s, Shape sh) =>
                Array (1 : sh) v a -> Array (s : sh) v a
stretchOuter (A vs) = sizeP (Proxy :: Proxy (s : sh)) `seq`  -- the result's size checked now
                      A $ stretchT (True : map (const False) (strides vs)) vs

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
{-# INLINE scalar #-}
scalar :: (Vector v, VecElem v a) => a -> Array '[] v a
scalar = A . scalarT

-- | Convert a scalar (rank 0) array to a value.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: (Vector v, VecElem v a) => Array '[] v a -> a
unScalar (A t) = unScalarT t

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: forall sh v a . (Vector v, VecElem v a, Shape sh) =>
            a -> Array sh v a
constant = A . constantT (shapeP (Proxy :: Proxy sh))

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: forall sh v a b . (Vector v, VecElem v a, VecElem v b, Shape sh) =>
        (a -> b) -> Array sh v a -> Array sh v b
mapA f a@(A t) = A $ mapT (shapeL a) f t

-- | Combine the elements of two arrays.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: forall sh v a b c . (Vector v, VecElem v a, VecElem v b, VecElem v c, Shape sh) =>
            (a -> b -> c) -> Array sh v a -> Array sh v b -> Array sh v c
zipWithA f a@(A t) (A t') = A $ zipWithT (shapeL a) f t t'

-- | Combine the elements of three arrays.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: forall sh v a b c d . (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, Shape sh) =>
             (a -> b -> c -> d) -> Array sh v a -> Array sh v b -> Array sh v c -> Array sh v d
zipWith3A f a@(A t) (A t') (A t'') = A $ zipWith3T (shapeL a) f t t' t''

-- | Combine the elements of four arrays.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: forall sh v a b c d e . (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e, Shape sh) =>
             (a -> b -> c -> d -> e) -> Array sh v a -> Array sh v b -> Array sh v c -> Array sh v d -> Array sh v e
zipWith4A f a@(A t) (A t') (A t'') (A t''') = A $ zipWith4T (shapeL a) f t t' t'' t'''

-- | Combine the elements of five arrays.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: forall sh v a b c d e f . (Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e, VecElem v f, Shape sh) =>
             (a -> b -> c -> d -> e -> f) -> Array sh v a -> Array sh v b -> Array sh v c -> Array sh v d -> Array sh v e -> Array sh v f
zipWith5A f a@(A t) (A t') (A t'') (A t''') (A t'''') = A $ zipWith5T (shapeL a) f t t' t'' t''' t''''

-- | Pad each dimension on the low and high side with the given value.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE pad #-}
pad :: forall ps sh' sh a v . (HasCallStack, Vector v, VecElem v a, Padded ps sh sh', Shape sh) =>
       a -> Array sh v a -> Array sh' v a
pad v a@(A at) | or (zipWith (\ (l, h) s -> sumOverflows [l, s, h]) aps ash) =
                   error $ "pad: padding past maxBound " ++ show (aps, ash)
               | not (validShape sh) = error $ "pad: bad shape " ++ show sh
               | all (== (0, 0)) aps = A at  -- no padding: the array itself
               | otherwise = A t
  where ash = shapeL a
        aps = padded (Proxy :: Proxy ps) (Proxy :: Proxy sh)
        -- Computed, not taken from padT's result: forcing that pair
        -- for the shape built the padded array too, before the checks.
        sh = zipWithLong2 (\ (l, h) s -> l + s + h) aps ash
        (_, t) = padT v aps ash at

-- | Do an arbitrary array transposition.
-- The transposition argument, which its type checks, is a permutation of the
-- numbers [0..l-1] for an l no greater than the rank of the array, whose l
-- outermost dimensions it permutes.
-- O(1) time.
{-# INLINE transpose #-}
transpose :: forall is sh v a .
             (HasCallStack, Permutation is, Rank is <= Rank sh, Shape sh, Shape is, KnownNat (Rank sh)) =>
             Array sh v a -> Array (Permute is sh) v a
transpose a@(A t) | not (validShape sh') = error $ "transpose: bad shape " ++ show sh'
                  | otherwise = A (transposeT is' t)
  where sh' = permute is' (shapeL a)
        l = length is
        n = valueOf @(Rank sh)
        is' = is ++ [l .. n-1]
        is = listP (Proxy :: Proxy is)

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- O(n) time.
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINE append #-}
append :: forall sh m n v a .
          (Vector v, VecElem v a, Shape sh, KnownNat m, KnownNat n, KnownNat (m+n)) =>
          Array (m ': sh) v a -> Array (n ': sh) v a -> Array (m+n ': sh) v a
append a@(A ta) b@(A tb)
  | natT @m == 0 = A tb  -- nothing to append to: the other array itself
  | natT @n == 0 = A ta
  | otherwise = fromVector (vAppend (toVector a) (toVector b))

-- | Concatenate a number of arrays into a single array.
-- Fails if the outer extents of the arrays do not sum to that of the result.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE concatOuter #-}
concatOuter :: forall m n sh v a . (HasCallStack, Vector v, VecElem v a, KnownNat m, KnownNat n, Shape sh) =>
               [Array (n ': sh) v a] -> Array (m ': sh) v a
concatOuter as | sumExtents ns /= s = error $ "concatOuter: outer extent mismatch " ++ show (ns, s)
               | [A t] <- as = A t  -- one array: the array itself
               | otherwise = fromVector $ vUnsafeConcatN (sizeT @(m ': sh)) $ map toVector as
  where ns = map (const (natT @n)) as
        s = natT @m

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINE ravel #-}
ravel :: forall sh s v v' a .
         (Vector v, Vector v', VecElem v a, VecElem v' (Array sh v a)
         , Shape sh, KnownNat s) =>
         Array '[s] v' (Array sh v a) -> Array (s:sh) v a
ravel aa | natT @s == 1, [A t] <- toList aa = A (insertUnitsT 0 1 t)  -- one array: a view of it
         | otherwise = fromVector $ vUnsafeConcatN (sizeT @(s:sh)) $ map toVector $ toList aa

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@.
{-# INLINE unravel #-}
unravel :: forall sh s v v' a . (Vector v', VecElem v' (Array sh v a)
           , Shape sh, KnownNat s) =>
           Array (s:sh) v a -> Array '[s] v' (Array sh v a)
unravel = rerank @1 scalar

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
{-# INLINE window #-}
window :: forall ws sh' sh v a .
          (Window ws sh sh', KnownNat (Rank ws), Shape sh') =>
          Array sh v a -> Array sh' v a
window (A (T ss o v)) = sizeP (Proxy :: Proxy sh') `seq`  -- the result's size checked now
                        A (T (ss' ++ ss) o v)
  where ss' = take (valueOf @(Rank ws)) ss

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- O(1) time.
{-# INLINE stride #-}
stride :: forall ts sh' sh v a .
          (Stride ts sh sh', Shape ts) =>
          Array sh v a -> Array sh' v a
stride (A (T ss o v)) = A (T (zipWith (*) (ats ++ repeat 1) ss) o v)
  where ats = listP (Proxy :: Proxy ts)

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- May fail if the result has more than half of 'maxBound' elements.
-- With k = 1, the result is a view of the array, sharing its vector; 'force'
-- copies it out.
{-# INLINE rotate #-}
rotate :: forall d k sh v a .
          (HasCallStack, KnownNat d, KnownNat k, Vector v, VecElem v a, Shape sh,
           d + 1 <= Rank sh, Shape (Take d sh ++ (k ': Drop d sh))) =>
          Array sh v a -> Array (Take d sh ++ (k ': Drop d sh)) v a
-- Through DynamicG's rotate, as RankedG's is.
rotate a@(A t) =
  sizeP (Proxy :: Proxy (Take d sh ++ (k ': Drop d sh))) `seq`  -- the result's size checked now
  case DG.rotate (natT @d) (natT @k) (DG.A (shapeL a) t) of
    DG.A _ t' -> A t'

-- | Extract a slice of an array.
-- The first type argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice \@'[ '(1,2)] (fromList \@'[4] [1,2,3,4]) == fromList \@'[2] [2,3]@.
-- O(1) time.
{-# INLINE slice #-}
slice :: forall sl sh' sh v a .
         (Slice sl sh sh') =>
         Array sh v a -> Array sh' v a
slice (A (T ts o v)) = A (T ts (o+i) v)
  where i = sum $ zipWith (*) ts $ sliceOffsets (Proxy :: Proxy sl) (Proxy :: Proxy sh)

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: forall n i o sh v v' a b .
          (Vector v', VecElem v' b,
           Drop n sh ~ i, Shape sh, KnownNat n, Shape o, Shape (Take n sh ++ o)) =>
          (Array i v a -> Array o v' b) -> Array sh v a -> Array (Take n sh ++ o) v' b
rerank f a@(A t)
  | product osh == 1, [s] <- subArraysT osh t =
    case f (A s) of  -- one subarray: a view of f's result
      A rt -> A (insertUnitsT 0 (length osh) rt)
  | otherwise =
  fromVector $
  vUnsafeConcatN (sizeT @(Take n sh ++ o)) $
  map (toVector . f . A) $
  subArraysT osh t
  where osh = take (valueOf @n) (shapeL a)

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must not exceed the rank of the array.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: forall n i1 i2 o sh1 sh2 r v a b c .
           (Vector v, VecElem v c,
            Drop n sh1 ~ i1, Drop n sh2 ~ i2, Shape sh1,
            Take n sh1 ~ r, Take n sh2 ~ r,
            KnownNat n, Shape o, Shape (r ++ o)) =>
           (Array i1 v a -> Array i2 v b -> Array o v c) -> Array sh1 v a -> Array sh2 v b -> Array (r ++ o) v c
rerank2 f aa@(A ta) (A tb)
  | product osh == 1, [sa] <- subArraysT osh ta, [sb] <- subArraysT osh tb =
    case f (A sa) (A sb) of  -- one subarray each: a view of f's result
      A rt -> A (insertUnitsT 0 (length osh) rt)
  | otherwise =
  fromVector $
  vUnsafeConcatN (sizeT @(r ++ o)) $
  zipWith (\ a b -> toVector $ f (A a) (A b))
          (subArraysT osh ta)
          (subArraysT osh tb)
  where osh = take (valueOf @n) (shapeL aa)


-- | Reverse the given dimensions, with the outermost being dimension 0.
-- O(1) time.
{-# INLINE rev #-}
rev :: forall rs sh v a . (ValidDims rs sh, Shape rs, Shape sh) => Array sh v a -> Array sh v a
rev a@(A t) = A (reverseT rs sh t)
  where rs = listP (Proxy :: Proxy rs)
        sh = shapeL a

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINE reduce #-}
reduce :: forall sh v a . (Vector v, VecElem v a, Shape sh) =>
          (a -> a -> a) -> a -> Array sh v a -> Array '[] v a
reduce f z a@(A t) = A $ reduceT (shapeL a) f z t

-- | Right fold across all elements of an array.
{-# INLINE foldrA #-}
foldrA
  :: forall sh v a b . (Vector v, VecElem v a, Shape sh)
  => (a -> b -> b) -> b -> Array sh v a -> b
foldrA f z a@(A t) = foldrT (shapeL a) f z t

-- | Constrained version of 'traverse' for 'Array's.
{-# INLINE traverseA #-}
traverseA
  :: forall sh v a b f . (Vector v, VecElem v a, VecElem v b, Applicative f, Shape sh)
  => (a -> f b) -> Array sh v a -> f (Array sh v b)
traverseA f a@(A t) = A <$> traverseT (shapeL a) f t

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Shape sh, Vector v, VecElem v a, Eq a) => Array sh v a -> Bool
allSameA a@(A t) = allSameT (shapeL a) t

instance (Shape sh, Vector v, VecElem v a, Arbitrary a) => Arbitrary (Array sh v a) where
  arbitrary = fromList <$> vector (sizeP (Proxy :: Proxy sh))

-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: forall sh v a . (Vector v, VecElem v a, Num a, Shape sh) => Array sh v a -> a
sumA a@(A t) = sumT (shapeL a) t

-- | Product of all elements.
{-# INLINE productA #-}
productA :: forall sh v a . (Vector v, VecElem v a, Num a, Shape sh) => Array sh v a -> a
productA a@(A t) = productT (shapeL a) t

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
{-# INLINE maximumA #-}
maximumA :: forall sh v a . (Vector v, VecElem v a, Ord a, Shape sh, 1 <= Size sh) => Array sh v a -> a
maximumA a@(A t) = maximumT (shapeL a) t

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
{-# INLINE minimumA #-}
minimumA :: forall sh v a . (Vector v, VecElem v a, Ord a, Shape sh, 1 <= Size sh) => Array sh v a -> a
minimumA a@(A t) = minimumT (shapeL a) t

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: forall sh v a . (Vector v, VecElem v a, Shape sh) => (a -> Bool) -> Array sh v a -> Bool
anyA p a@(A t) = anyT (shapeL a) p t

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: forall sh v a . (Vector v, VecElem v a, Shape sh) => (a -> Bool) -> Array sh v a -> Bool
allA p a@(A t) = allT (shapeL a) p t

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimensions indices must have the same rank as the argument array
-- and it must be strictly ascending.
{-# INLINE broadcast #-}
broadcast :: forall ds sh' sh v a .
             (Shape sh, Shape sh',
              Broadcast ds sh sh',
              Vector v, VecElem v a) =>
             Array sh v a -> Array sh' v a
broadcast a = sizeP (Proxy :: Proxy sh') `seq`  -- the result's size checked now
              stretch' bc $
              reshape' rsh sh a
  where sh' = shapeP (Proxy :: Proxy sh')
        sh = shapeP (Proxy :: Proxy sh)
        rsh = [ if b then 1 else s | (s, b) <- zip sh' bc ]
        bc = broadcasting @ds @sh @sh'

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE update #-}
update :: forall sh v a . (HasCallStack, Vector v, VecElem v a, Shape sh) =>
          Array sh v a -> [([Int], a)] -> Array sh v a
-- Through DynamicG's update, as 'rotate' goes through DynamicG's rotate.
update a@(A t) us = case DG.update (DG.A (shapeL a) t) us of
  DG.A _ t' -> A t'

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: forall sh v a .
            (Vector v, VecElem v a, Shape sh) =>
            ([Int] -> a) -> Array sh v a
generate = A . generateT (shapeP (Proxy :: Proxy sh))

-- | Iterate a function n times.
{-# INLINE iterateN #-}
iterateN :: forall n v a .
            (Vector v, VecElem v a, KnownNat n) =>
            (a -> a) -> a -> Array '[n] v a
iterateN f = A . iterateNT (natT @n) f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
{-# INLINE iota #-}
iota :: forall n v a .
        (Vector v, VecElem v a, KnownNat n, Num a) =>
        Array '[n] v a
iota = A $ iotaT (natT @n)
