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
{-# LANGUAGE DeriveDataTypeable #-}
{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RoleAnnotations #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE UndecidableInstances #-}
-- | Arrays of dynamic size.  The arrays are polymorphic in the underlying
-- linear data structure used to store the actual values.
module Data.Array.Internal.DynamicG(
  Array(..), Vector, ShapeL, VecElem,
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
import Control.Monad(replicateM)
import Data.Data(Data)
import Data.Maybe(fromMaybe)
import GHC.Generics(Generic)
import GHC.Stack
import Test.QuickCheck hiding (generate)
import Text.PrettyPrint.HughesPJClass hiding ((<>))

import Data.Array.Internal

-- | Arrays stored in a /v/ with values of type /a/.
type role Array representational nominal
data Array v a = A !ShapeL !(T v a)
  deriving (Generic, Data)

instance (Vector v, Show a, VecElem v a) => Show (Array v a) where
  showsPrec p a@(A s _) = showParen (p > 10) $
    showString "fromList " . showsPrec 11 s . showString " " . showsPrec 11 (toList a)

instance (Vector v, Read a, VecElem v a) => Read (Array v a) where
  readsPrec p = readParen (p > 10) $ \ r1 ->
    [(fromList s xs, r4) | ("fromList", r2) <- lex r1, (s, r3) <- readsPrec 11 r2,
                    (xs, r4) <- readsPrec 11 r3, not (badShape s), product s == length xs]

instance (Vector v, Eq a, VecElem v a) => Eq (Array v a) where
  (A s v) == (A s' v') = equalT s s' v v'
  {-# INLINE (==) #-}

instance (Vector v, Ord a, VecElem v a) => Ord (Array v a) where
  (A s v) `compare` (A s' v') = compare s s' <> compareT s v v'
  {-# INLINE compare #-}

instance (Vector v, Pretty a, VecElem v a) => Pretty (Array v a) where
  pPrintPrec l p (A sh t) = ppT l p sh t

instance (NFData (v a)) => NFData (Array v a)

-- | The number of elements in the array.
{-# INLINE size #-}
size :: Array v a -> Int
size = product . shapeL

-- | The shape of an array, i.e., a list of the sizes of its dimensions.
-- In the linearization of the array the outermost (i.e. first list element)
-- varies most slowly.
-- O(1) time.
{-# INLINE shapeL #-}
shapeL :: Array v a -> ShapeL
shapeL (A s _) = s

-- | The rank of an array, i.e., the number of dimensions it has.
-- O(1) time.
{-# INLINE rank #-}
rank :: Array v a -> Int
rank (A s _) = length s

-- | Index into an array.  Fails if the array has rank 0 or if the index is out of bounds.
-- O(1) time.
{-# INLINE index #-}
index :: HasCallStack => Array v a -> Int -> Array v a
index (A (s:ss) t) i | i < 0 || i >= s = error $ "index: out of bounds " ++ show (i, s)
                     | otherwise = A ss $ indexT t i
index (A [] _) _ = error "index: scalar"

-- | Convert to a list with the elements in the linearization order.
-- O(n) time.
{-# INLINE toList #-}
toList :: (Vector v, VecElem v a) => Array v a -> [a]
toList (A sh t) = toListT sh t

-- | Convert to a vector with the elements in the linearization order.
-- O(n) or O(1) time (the latter if the vector is already in the linearization order).
-- The O(1) result can be a slice of a larger vector, which it keeps alive;
-- 'force' the array first to get a vector of just its elements.
{-# INLINE toVector #-}
toVector :: (Vector v, VecElem v a) => Array v a -> v a
toVector (A sh t) = toVectorT sh t

-- HasCallStack, here and in the other array modules, goes on exactly the
-- functions that check an argument, calling error when it is bad, as
-- fromList does, and on the functions of the same name that pass their
-- arguments on to one, as the wrappers in the other modules do, so that the
-- error shows the line the operation was called from.  A contract check,
-- whose error says "violated contract", adds none, nor does an assert, both
-- guarding against a bug in the library, and class methods take none, as a
-- stack on one would bind every instance.
-- | Convert from a list with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the list.
-- O(n) time.
{-# INLINE fromList #-}
fromList :: (HasCallStack, Vector v, VecElem v a) => ShapeL -> [a] -> Array v a
fromList ss vs | badShape ss = error $ "fromList: bad shape " ++ show ss
               | n /= l = error $ "fromList: size mismatch " ++ show (n, l)
               | otherwise = A ss $ T st 0 $ vFromListN l vs
  where n : st = getStridesT ss
        l = length vs

-- | Convert from a vector with the elements given in the linearization order.
-- Fails if the given shape does not have the same number of elements as the vector.
-- O(1) time.
{-# INLINE fromVector #-}
fromVector :: (HasCallStack, Vector v, VecElem v a) => ShapeL -> v a -> Array v a
fromVector ss v | badShape ss = error $ "fromVector: bad shape " ++ show ss
                | n /= l = error $ "fromVector: size mismatch " ++ show (n, l)
                | otherwise = A ss $ T st 0 v
  where n : st = getStridesT ss
        l = vLength v

-- | Make sure the underlying vector is in the linearization order.
-- Where the elements already lie in that order in one part of the vector,
-- the result keeps that part without copying it, and so keeps the whole
-- vector alive; 'force' copies them out.
-- This is semantically an identity function, but can have big performance
-- implications.
-- O(n) or O(1) time.
{-# INLINE normalize #-}
normalize :: (Vector v, VecElem v a) => Array v a -> Array v a
normalize (A sh t) = A sh $ normalizeT sh t

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
force :: (Vector v, VecElem v a) => Array v a -> Array v a
force (A sh t) = A sh $ forceT sh t

-- | Change the shape of an array.  Fails if the arrays have different number of elements.
-- O(n) or O(1) time.
{-# INLINE reshape #-}
reshape :: (HasCallStack, Vector v, VecElem v a) => ShapeL -> Array v a -> Array v a
reshape sh (A sh' t@(T ost oo v))
  | badShape sh = error $ "reshape: bad shape " ++ show sh
  | n /= n' = error $ "reshape: size mismatch " ++ show (sh, sh')
  | vLength v == 1 = A sh $ T (map (const 0) sh) 0 v  -- Fast special case for singleton vector
  | Just nst <- simpleReshape ost sh' sh = A sh $ T nst oo v
  | otherwise = A sh $ T st 0 $ toVectorT sh' t
  where n : st = getStridesT sh
        n' = product sh'

-- | Change the size of dimensions with size 1.  These dimension can be changed to any size.
-- All other dimensions must remain the same.
-- O(1) time.
{-# INLINE stretch #-}
stretch :: (HasCallStack) => ShapeL -> Array v a -> Array v a
stretch sh _ | badShape sh = error $ "stretch: bad shape " ++ show sh
stretch sh (A sh' vs) | Just bs <- str sh sh' = A sh $ stretchT bs vs
                      | otherwise = error $ "stretch: incompatible " ++ show (sh, sh')
  where str [] [] = Just []
        str (x:xs) (y:ys) | x == y = (False :) <$> str xs ys
                          | y == 1 = (True  :) <$> str xs ys
        str _ _ = Nothing

-- | Change the size of the outermost dimension by replication.
-- Fails if the outermost dimension is not 1 or the size is negative.
{-# INLINE stretchOuter #-}
stretchOuter :: (HasCallStack) => Int -> Array v a -> Array v a
stretchOuter s (A (1:sh) vs)
  | badShape (s:sh) = error $ "stretchOuter: bad shape " ++ show (s:sh)
  | otherwise = A (s:sh) $ stretchT (True : map (const False) (strides vs)) vs
stretchOuter _ _ = error "stretchOuter: needs outermost dimension of size 1"

-- | Convert a value to a scalar (rank 0) array.
-- O(1) time.
{-# INLINE scalar #-}
scalar :: (Vector v, VecElem v a) => a -> Array v a
scalar = A [] . scalarT

-- | Convert a scalar (rank 0) array to a value.
-- Fails if the array is not a scalar.
-- O(1) time.
{-# INLINE unScalar #-}
unScalar :: (HasCallStack, Vector v, VecElem v a) => Array v a -> a
unScalar (A [] t) = unScalarT t
unScalar _ = error "unScalar: not a scalar"

-- | Make an array with all elements having the same value.
-- O(1) time.
{-# INLINE constant #-}
constant :: (HasCallStack, Vector v, VecElem v a) => ShapeL -> a -> Array v a
constant sh | badShape sh = error $ "constant: bad shape " ++ show sh
            | otherwise   = A sh . constantT sh

-- | Map over the array elements.
-- O(n) time.
{-# INLINE mapA #-}
mapA :: (Vector v, VecElem v a, VecElem v b) => (a -> b) -> Array v a -> Array v b
mapA f (A s t) = A s (mapT s f t)

-- | Combine the elements of two arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWithA #-}
zipWithA :: (HasCallStack, Vector v, VecElem v a, VecElem v b, VecElem v c) =>
            (a -> b -> c) -> Array v a -> Array v b -> Array v c
zipWithA f (A s t) (A s' t') | s == s' = A s (zipWithT s f t t')
                             | otherwise = error $ "zipWithA: shape mismatch " ++ show (s, s')

-- | Combine the elements of three arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith3A #-}
zipWith3A :: (HasCallStack, Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d) =>
             (a -> b -> c -> d) -> Array v a -> Array v b -> Array v c -> Array v d
zipWith3A f (A s t) (A s' t') (A s'' t'') | s == s' && s == s'' = A s (zipWith3T s f t t' t'')
                                          | otherwise = error $ "zipWith3A: shape mismatch " ++ show (s, s', s'')

-- | Combine the elements of four arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith4A #-}
zipWith4A :: (HasCallStack, Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e) =>
             (a -> b -> c -> d -> e) -> Array v a -> Array v b -> Array v c -> Array v d -> Array v e
zipWith4A f (A s t) (A s' t') (A s'' t'') (A s''' t''') | s == s' && s == s'' && s == s''' = A s (zipWith4T s f t t' t'' t''')
                                                        | otherwise = error $ "zipWith4A: shape mismatch " ++ show (s, s', s'', s''')

-- | Combine the elements of five arrays.
-- Fails if the shapes differ.
-- O(n) time.
{-# INLINE zipWith5A #-}
zipWith5A :: (HasCallStack, Vector v, VecElem v a, VecElem v b, VecElem v c, VecElem v d, VecElem v e, VecElem v f) =>
             (a -> b -> c -> d -> e -> f) -> Array v a -> Array v b -> Array v c -> Array v d -> Array v e -> Array v f
zipWith5A f (A s t) (A s' t') (A s'' t'') (A s''' t''') (A s'''' t'''') | s == s' && s == s'' && s == s''' && s == s'''' = A s (zipWith5T s f t t' t'' t''' t'''')
                                                                        | otherwise = error $ "zipWith5A: shape mismatch " ++ show (s, s', s'', s''', s'''')

-- | Pad each dimension on the low and high side with the given value.
-- Fails if the padding list is longer than the rank or a padding is negative.
-- O(n) time.
-- With no padding, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE pad #-}
pad :: forall a v . (HasCallStack, Vector v, VecElem v a) =>
       [(Int, Int)] -> a -> Array v a -> Array v a
pad aps v (A ash at) | length aps > length ash = error $ "pad: rank mismatch " ++ show (length aps, length ash)
                     | any (\ (l, h) -> l < 0 || h < 0) aps = error $ "pad: negative padding " ++ show aps
                     | or (zipWith (\ (l, h) s -> sumOverflows [l, s, h]) aps ash) =
                         error $ "pad: padding past maxBound " ++ show (aps, ash)
                     | badShape sh = error $ "pad: bad shape " ++ show sh
                     | all (== (0, 0)) aps = A ash at  -- no padding: the array itself
                     | otherwise = A sh t
  where sh = zipWithLong2 (\ (l, h) s -> l + s + h) aps ash
        (_, t) = padT v aps ash at

-- | Do an arbitrary array transposition.
-- Fails if the transposition argument is not a permutation of the numbers
-- [0..l-1] for an l no greater than the rank of the array, whose l outermost
-- dimensions it permutes.
-- O(1) time.
{-# INLINE transpose #-}
transpose :: (HasCallStack) => [Int] -> Array v a -> Array v a
transpose is (A sh t) | l > n = error $ "transpose: rank exceeded " ++ show (is, sh)
                      | not (all (`elem` is) [0 .. l-1]) =
                          error $ "transpose: not a permutation: " ++ show is
                      | otherwise = A (permute is' sh) (transposeT is' t)
  where l = length is
        n = length sh
        is' = is ++ [l .. n-1]

-- | Append two arrays along the outermost dimension.
-- All dimensions, except the outermost, must be the same.
-- Fails if either array has rank 0.
-- O(n) time.
-- Where one array's outer extent is 0, the result is the other itself, sharing
-- its vector; 'force' copies it out.
{-# INLINE append #-}
append :: (HasCallStack, Vector v, VecElem v a) => Array v a -> Array v a -> Array v a
append a@(A (sa:sh) _) b@(A (sb:sh') _)
  | sh == sh', sa == 0 = b  -- nothing to append to: the other array itself
  | sh == sh', sb == 0 = a
  | sh == sh' && not (sumOverflows [sa, sb]) =
    fromVector (sa+sb : sh) (vAppend (toVector a) (toVector b))
append _ _ = error "append: bad shape"

-- | Concatenate a number of arrays into a single array.
-- Fails if the list is empty, an array has rank 0 or any but the outer
-- dimensions differ.
-- O(n) time.
-- Of one array, the result is that array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE concatOuter #-}
concatOuter :: (HasCallStack, Vector v, VecElem v a) => [Array v a] -> Array v a
concatOuter [] = error "concatOuter: empty list"
concatOuter as | any null shs = error "concatOuter: rank 0 array"
               | [a] <- as = a  -- one array: the array itself
               | not $ allSame $ map tail shs =
                 error $ "concatOuter: non-conforming inner dimensions: " ++ show shs
               | n < 0 = error $ "concatOuter: outer extents summing past maxBound: " ++ show (map head shs)
               | otherwise = fromVector sh' $ vUnsafeConcatN (product sh') $ map toVector as
  where shs@(sh:_) = map shapeL as
        n = sumExtents (map head shs)
        sh' = n : tail sh

-- | Turn a rank-1 array of arrays into a single array by making the outer array into the outermost
-- dimension of the result array.  All the arrays must have the same shape,
-- and there must be at least one.
-- Fails if the outer array does not have rank 1.
-- O(n) time.
-- Of one array, the result is a view of it, sharing its vector; 'force' copies
-- it out.
{-# INLINE ravel #-}
ravel :: (HasCallStack, Vector v, Vector v', VecElem v a, VecElem v' (Array v a)) =>
         Array v' (Array v a) -> Array v a
ravel aa | rank aa /= 1 = error "ravel: outermost array does not have rank 1"
         | otherwise = case shapeL aa of
  [1] -> case unScalar (index aa 0) of  -- one array: a view of it
    A sh t -> A (1 : sh) (insertUnitsT 0 1 t)
  [k] | k > 0 -> ravelOuterOf [k] (shapeL (unScalar (index aa 0))) (toList aa)
  _ -> error "ravel: empty array"

-- | Turn an array into a nested array, this is the inverse of 'ravel'.
-- I.e., @ravel . unravel == id@ where the outermost dimension is not empty.
-- Fails if the array has rank 0.
{-# INLINE unravel #-}
unravel :: forall v v' a . (HasCallStack, Vector v', VecElem v' (Array v a)) =>
           Array v a -> Array v' (Array v a)
unravel (A [] _) = error "unravel: rank 0 array"
unravel (A (0 : _) _) = A [0] $ fromVectorT [0] (vConcat [])  -- no subarrays
unravel a = rerank 1 scalar a

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
window :: HasCallStack => [Int] -> Array v a -> Array v a
-- The window list is checked before the shape is built, so that the shape
-- a message shows holds no error of its own, and the extents are computed
-- as Integers, a window of 0 over an extent of maxBound making one past it.
window aws (A ash (T ss o v))
  | length aws > length ash = error $ "window: rank mismatch " ++ show (aws, ash)
  | (w, s) : _ <- filter (\ (w, s) -> w < 0 || w > s) (zip aws ash) =
      error $ "window: bad window size " ++ show (w, s)
  | any (> toInteger (maxBound :: Int)) rshI || badShape rsh =
      error $ "window: bad shape " ++ show rshI
  | otherwise = A rsh (T (ss' ++ ss) o v)
  where rshI = zipWith (\ w s -> toInteger s - toInteger w + 1) aws ash
               ++ map toInteger (aws ++ drop (length aws) ash)
        rsh = map fromInteger rshI
        ss' = zipWith const ss aws

-- | Stride the outermost dimensions.
-- E.g., if the array shape is @[10,12,8]@ and the strides are
-- @[2,2]@ then the resulting shape will be @[5,6,8]@.
-- Fails if the stride list is longer than the rank or a stride is not
-- positive.
-- O(1) time.
{-# INLINE stride #-}
-- The shape is forced here, not checked with 'badShape' as window's is:
-- its extents, each s / t rounded up, never pass the array's.
stride :: HasCallStack => [Int] -> Array v a -> Array v a
stride ats (A ash (T ss o v)) = length rsh `seq` A rsh (T (zipWith (*) (ats ++ repeat 1) ss) o v)  -- check now
  where rsh = str ats ash
        str (t:ts) (s:sh) | t <= 0 = error $ "stride: non-positive stride " ++ show ats
                          | otherwise = negate (negate s `div` t) : str ts sh  -- s / t rounded up, without overflow
        str [] sh = sh
        str _ _ = error $ "stride: rank mismatch " ++ show (ats, ash)

-- | Rotate the array k times along the d'th dimension.
-- E.g., if the array shape is @[2, 3, 2]@, d is 1, and k is 4,
-- the resulting shape will be @[2, 4, 3, 2]@.
-- Fails if d is not a dimension of the array or k is negative, and may fail
-- if the result has more than half of 'maxBound' elements.
-- With k = 1, the result is a view of the array, sharing its vector; 'force'
-- copies it out.
{-# INLINABLE rotate #-}  -- a complex operation, too much code for INLINE
rotate :: (HasCallStack, Vector v, VecElem v a) => Int -> Int -> Array v a -> Array v a
rotate d k a@(A sh _)
  | d < 0 || d >= rank a = error $ "rotate: dimension out of range " ++ show (d, rank a)
  | badShape sh' = error $ "rotate: bad shape " ++ show sh'
  | 0 `elem` sh' = A sh' $ fromVectorT sh' (vConcat [])  -- no elements
  | k == 1, A _ t <- a = A sh' (insertUnitsT d 1 t)  -- one rotation: a view of the array
  | copies > toInteger (maxBound :: Int) = error $ "rotate: count too large " ++ show (d, k, sh)
  | otherwise = rerank d f a
 where
  (osh, ish) = splitAt d sh
  sh' = osh ++ k : ish
  -- How many elements f's copies of a subarray hold: fewer than twice the
  -- k * n of its rotations, so past maxBound only where those pass half of it.
  copies = let h = toInteger (sh !! d)
               k' = toInteger k
           in (k' + (k' + h - 2) `quot` h) * toInteger (product ish)
  f arr = let h:t = shapeL arr
              m = product t
              n = h * m
              c = k + (k + h - 2) `quot` h  -- copies to fit k windows n + m apart
              A _ (T [s] o v) = reshape [c * n]
                                . stretchOuter c
                                . reshape (1:h:t) $ arr
          -- The k windows as one view: window [n] would view all
          -- c * n - n + 1 of them first, a view whose size can overflow Int.
          in rev [0]
             . reshape (k:h:t) $ A [k, n] (T [(n + m) * s, s] o v)

-- | Extract a slice of an array.
-- The first argument is a list of (offset, length) pairs.
-- The length of the slicing argument must not exceed the rank of the array.
-- The extracted slice must fall within the array dimensions.
-- E.g. @slice [(1,2)] (fromList [4] [1,2,3,4]) == fromList [2] [2,3]@.
-- O(1) time.
{-# INLINE slice #-}
slice :: (HasCallStack) => [(Int, Int)] -> Array v a -> Array v a
slice asl (A ash (T ats ao v)) = A rsh (T ats o v)
  where (o, rsh) = slc asl ash ats
        slc ((k,n):sl) (s:sh) (t:ts) | k < 0 || n < 0 || n > s - k = error $ "slice: out of bounds: slice=" ++ show (k, n) ++ " size=" ++ show s
                                     | otherwise = (i + k*t, n:ns) where (i, ns) = slc sl sh ts
        slc (_:_) [] _ = error "slice: slice list too long"
        slc [] sh _ = (ao, sh)
        slc _ _ _ = error "slice: violated contract: not one stride per dimension"

-- | Apply a function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must be from 0 to the rank of the array, none of those /n/ dimensions
-- may be empty, and the function's results must all have one shape.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank #-}
rerank :: forall v v' a b . (HasCallStack, Vector v', VecElem v' b) =>
          Int -> (Array v a -> Array v' b) -> Array v a -> Array v' b
rerank n f (A sh t) | n < 0 || n > length sh = error "rerank: rank exceeded"
                    | product osh == 1, [s] <- subArraysT osh t =
                      case f (A ish s) of  -- one subarray: a view of f's result
                        A rsh rt -> A (osh ++ rsh) (insertUnitsT 0 (length osh) rt)
                    | otherwise =
  ravelOuter osh $
  map (f . A ish) $
  subArraysT osh t
  where (osh, ish) = splitAt n sh

-- The caller computes the arrays, one for each index of @osh@, and each one's
-- shape is checked against the first's as it is copied, not all before
-- the copy, which, the fields of an array being strict, would compute every
-- array and hold them all.  Over an empty outer dimension there is none
-- to take the inner shape from.
{-# INLINE ravelOuter #-}
ravelOuter :: (HasCallStack, Vector v, VecElem v a) => ShapeL -> [Array v a] -> Array v a
ravelOuter _ [] = error "ravelOuter: empty outer dimension"
ravelOuter osh as@(a : _) = ravelOuterOf osh (shapeL a) as

-- 'ravelOuter' given the shape every array must have, which 'ravel' reads off
-- its first array without taking the list's head, so that the list fuses with
-- the copy.
{-# INLINE ravelOuterOf #-}
ravelOuterOf :: (HasCallStack, Vector v, VecElem v a) =>
                ShapeL -> ShapeL -> [Array v a] -> Array v a
ravelOuterOf osh sh as = fromVector sh' $ vUnsafeConcatN (product sh') $ map vec as
  where sh' = osh ++ sh
        vec x | shapeL x == sh = toVector x
              | otherwise = error $ "ravelOuterOf: non-conforming inner dimensions: " ++ show [sh, shapeL x]

-- | Apply a two-argument function to the subarrays /n/ levels down and make
-- the results into an array with the same /n/ outermost dimensions.
-- The /n/ must be from 0 to the rank of each array, none of those /n/
-- dimensions may be empty, and the function's results must all have one shape.
-- Fails if the arrays differ in those /n/ outermost dimensions.
-- O(n) time.
-- Over one outer index, the result is a view of the function's result,
-- sharing its vector; 'force' copies it out.
{-# INLINE rerank2 #-}
rerank2 :: forall v a b c . (HasCallStack, Vector v, VecElem v c) =>
           Int -> (Array v a -> Array v b -> Array v c) -> Array v a -> Array v b -> Array v c
rerank2 n f (A sha ta) (A shb tb) | n < 0 || n > length sha || n > length shb = error "rerank2: rank exceeded"
                                  | take n sha /= take n shb = error "rerank2: shape mismatch"
                                  | product osh == 1, [sa] <- subArraysT osh ta, [sb] <- subArraysT osh tb =
                                    case f (A isha sa) (A ishb sb) of  -- one subarray each: a view of f's result
                                      A rsh rt -> A (osh ++ rsh) (insertUnitsT 0 (length osh) rt)
                                  | otherwise =
  ravelOuter osh $
  zipWith (\ a b -> f (A isha a) (A ishb b))
          (subArraysT osh ta)
          (subArraysT osh tb)
  where (osh, isha) = splitAt n sha
        ishb = drop n shb

-- | Reverse the given dimensions, with the outermost being dimension 0.
-- Fails if a given dimension is not one of the array's.
-- O(1) time.
{-# INLINE rev #-}
rev :: (HasCallStack) => [Int] -> Array v a -> Array v a
rev rs (A sh t) | all (\ r -> r >= 0 && r < n) rs = A sh (reverseT rs sh t)
                | otherwise = error $ "rev: bad reverse dimension " ++ show (rs, n)
  where n = length sh

-- | Reduce all elements of an array into a rank 0 array.
-- To reduce parts use 'rerank' and 'transpose' together with 'reduce'.
-- Forcing the result forces the initial value.
-- O(n) time.
{-# INLINE reduce #-}
reduce :: (Vector v, VecElem v a) =>
          (a -> a -> a) -> a -> Array v a -> Array v a
reduce f z (A sh t) = A [] $ reduceT sh f z t

-- | Right fold across all elements of an array.
{-# INLINE foldrA #-}
foldrA :: (Vector v, VecElem v a) => (a -> b -> b) -> b -> Array v a -> b
foldrA f z (A sh t) = foldrT sh f z t

-- | Constrained version of 'traverse' for 'Array's.
{-# INLINE traverseA #-}
traverseA
  :: (Vector v, VecElem v a, VecElem v b, Applicative f)
  => (a -> f b) -> Array v a -> f (Array v b)
traverseA f (A sh t) = A sh <$> traverseT sh f t

-- | Check if all elements of the array are equal.
{-# INLINE allSameA #-}
allSameA :: (Vector v, VecElem v a, Eq a) => Array v a -> Bool
allSameA (A sh t) = allSameT sh t

instance (Vector v, VecElem v a, Arbitrary a) => Arbitrary (Array v a) where
  arbitrary = do
    r <- choose (0, 5)  -- Don't generate huge ranks
    -- Don't generate huge number of elements
    ss <- replicateM r (getSmall . getPositive <$> arbitrary) `suchThat` ((< 10000) . product)
    fromList ss <$> vector (product ss)

-- | Sum of all elements.
{-# INLINE sumA #-}
sumA :: (Vector v, VecElem v a, Num a) => Array v a -> a
sumA (A sh t) = sumT sh t

-- | Product of all elements.
{-# INLINE productA #-}
productA :: (Vector v, VecElem v a, Num a) => Array v a -> a
productA (A sh t) = productT sh t

-- | Maximum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE maximumA #-}
maximumA :: (HasCallStack, Vector v, VecElem v a, Ord a) => Array v a -> a
maximumA a@(A sh t) | size a > 0 = maximumT sh t
                    | otherwise  = error "maximumA: empty array"

-- | Minimum of all elements.
-- Of elements that compare equal, as @0.0@ and @-0.0@ do, the one returned
-- depends on the array's layout, and so does which pairs of elements it
-- compares, an element with itself among them.
-- Fails if the array is empty.
{-# INLINE minimumA #-}
minimumA :: (HasCallStack, Vector v, VecElem v a, Ord a) => Array v a -> a
minimumA a@(A sh t) | size a > 0 = minimumT sh t
                    | otherwise  = error "minimumA: empty array"

-- | Test if the predicate holds for any element.
{-# INLINE anyA #-}
anyA :: (Vector v, VecElem v a) => (a -> Bool) -> Array v a -> Bool
anyA p (A sh t) = anyT sh p t

-- | Test if the predicate holds for all elements.
{-# INLINE allA #-}
allA :: (Vector v, VecElem v a) => (a -> Bool) -> Array v a -> Bool
allA p (A sh t) = allT sh p t

-- | Put the dimensions of the argument into the specified dimensions,
-- and just replicate the data along all other dimensions.
-- The list of dimension indices must have the same rank as the argument array
-- and it must be strictly ascending.
-- Fails if an index is not a dimension of the result or the argument's
-- dimensions differ from the result's at those indices.
{-# INLINE broadcast #-}
broadcast :: HasCallStack =>
             [Int] -> ShapeL -> Array v a -> Array v a
broadcast ds sh a | any (\ d -> d < 0 || d >= r) ds = error "broadcast: bad dimension index"
                  | not (ascending ds) = error "broadcast: unordered dimensions"
                  | badShape sh = error $ "broadcast: bad shape " ++ show sh
                  | permute ds sh /= shapeL a =
                      error $ "broadcast: shape mismatch " ++ show (shapeL a, ds, sh)
                  | otherwise = A sh $ T sts o v
  where r = length sh
        -- The array's strides at ds, and 0 at the dimensions broadcast.
        A _ (T ats o v) = a
        sts = [ fromMaybe 0 (lookup i (zip ds ats)) | i <- [0 .. r - 1] ]
        ascending (x:y:ys) = x < y && ascending (y:ys)
        ascending _ = True

-- | Update the array at the specified indices to the associated value.
-- Fails if an index is out of bounds.
-- With no updates, the result is the array itself, sharing its vector; 'force'
-- copies it out.
{-# INLINE update #-}
update :: (HasCallStack, Vector v, VecElem v a) =>
          Array v a -> [([Int], a)] -> Array v a
update (A sh t) us | null us = A sh t  -- no update: the array itself
                   | all (ok . fst) us = A sh $ updateT sh t us
                   | otherwise = error $ "update: index out of bounds: " ++ show (filter (not . ok) $ map fst us)
  where ok is = length is == r && and (zipWith (\ i s -> 0 <= i && i < s) is sh)
        r = length sh

-- | Generate an array with a function that computes the value for each index.
{-# INLINE generate #-}
generate :: (HasCallStack, Vector v, VecElem v a) =>
            ShapeL -> ([Int] -> a) -> Array v a
generate sh | badShape sh = error $ "generate: bad shape " ++ show sh
            | otherwise = A sh . generateT sh

-- | Iterate a function n times.
-- Fails if n is negative.
{-# INLINE iterateN #-}
iterateN :: forall v a .
            (HasCallStack, Vector v, VecElem v a) =>
            Int -> (a -> a) -> a -> Array v a
iterateN n f | n < 0 = error $ "iterateN: negative size " ++ show n
             | otherwise = A [n] . iterateNT n f

-- | Generate a vector from 0 to n-1.
-- Each element is evaluated to weak head normal form as it is stored.
-- Fails if n is negative.
{-# INLINE iota #-}
iota :: forall v a .
        (HasCallStack, Vector v, VecElem v a, Num a) =>
        Int -> Array v a
iota n | n < 0 = error $ "iota: negative size " ++ show n
       | otherwise = A [n] $ iotaT n
