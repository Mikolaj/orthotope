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
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE RankNTypes #-}
{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE TypeApplications #-}
-- Shaped arrays against Dynamic ones, at the boxed, Storable, Unboxed and
-- list instances of Vector, with Int and Word8 elements: the random views
-- of the dynamic test modules as Shaped arrays of their shapes, and Shaped
-- operations, with their arguments fixed in the types, on arrays of one
-- shape in several layouts.
module ShapedGTest(test) where

import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import Data.Array.Internal.DynamicS ()
import Data.Array.Internal.DynamicU ()
import Data.Array.Internal.Shape (withShapeP)
import qualified Data.Array.Internal.ShapedG as SG
import Data.Proxy (Proxy (..))
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import Data.Word (Word8)
import Foreign.Storable (Storable)
import Test.Framework (Test, testGroup)
import Test.QuickCheck
  (Property, choose, conjoin, counterexample, forAll, (.&&.), (===))
import Views (Elem, View (..), genElems, mkViewG, testPropertyN)

test :: Test
test = testGroup "ShapedG" $ backends @Int ++ [testGroup "Word8" (backends @Word8)]

-- The properties at each instance of Vector, with elements of an Elem type.
backends :: forall a . (Elem a, Storable a, VU.Unbox a) => [Test]
backends =
  [ backend @V.Vector @a "boxed"
  , backend @VS.Vector @a "Storable"
  , backend @VU.Vector @a "Unboxed"
  , backend @[] @a "list"
  ]

backend :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
           String -> Test
backend n = testGroup n $
  testPropertyN "prop_views" (prop_views @v @a)
  : [ testPropertyN on (prop_op f g) | (on, f, g) <- ops @v @a ]

-- A random view, as a Shaped array of its shape, gives what it does as a
-- Dynamic array or a list: its elements, their reductions but maximumA and
-- minimumA, which want a shape known not to be empty, their right fold, its
-- order against an array of its elements with at most one of them changed,
-- and the results of normalize, mapA, zipWithA and reduce; and it reads
-- back from its show.
prop_views :: forall v a . (I.Vector v, I.VecElem v a, Ord (v a), Show (v a), Elem a) =>
              View -> Property
prop_views v@(View sh _) =
  forAll (genElems (-9, 9) (product sh)) $ \ xs ->
  case mkViewG v xs :: DG.Array v a of
    x@(DG.A xsh t) -> withShapeP xsh $ \ (_ :: Proxy sh) ->
      let s = SG.A t :: SG.Array sh v a
          l = DG.toList x
      in  forAll (choose (0, length l)) $ \ i ->
          let l' = [ if k == i then e + 1 else e | (k, e) <- zip [0 ..] l ]
              s' = SG.fromList l' :: SG.Array sh v a
          in  SG.toList s === l .&&. SG.toVector s === DG.toVector x
              .&&. SG.toList (SG.normalize s) === l
              .&&. SG.sumA s === sum l .&&. SG.productA s === product l
              .&&. SG.anyA (> 0) s === any (> 0) l .&&. SG.allA (> 0) s === all (> 0) l
              .&&. SG.allSameA s === DG.allSameA x .&&. SG.foldrA (:) [] s === l
              .&&. (s == s') === (l == l') .&&. compare s s' === compare l l'
              .&&. SG.toList (SG.mapA (* 2) s) === map (* 2) l
              .&&. SG.toList (SG.zipWithA (-) s s') === zipWith (-) l l'
              .&&. SG.unScalar (SG.reduce (+) 0 s) === sum l
              .&&. read (show s) === s

-- The Shaped operation gives what the Dynamic one does on each source.
prop_op :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
           (SG.Array '[2,3,4] v a -> ([Int], [a])) -> (DG.Array v a -> ([Int], [a]))
        -> Property
prop_op f g = forAll (genElems (-9, 9) 60) $ \ xs ->
  conjoin [ counterexample n (f s === g (toD s)) | (n, s) <- sources xs ]

-- The Dynamic array a Shaped one is.
toD :: forall sh v a . SG.Shape sh => SG.Array sh v a -> DG.Array v a
toD a@(SG.A t) = DG.A (SG.shapeL a) t

-- The shape and the elements of an array.
obs :: (I.Vector v, I.VecElem v a, SG.Shape sh) => SG.Array sh v a -> ([Int], [a])
obs a = (SG.shapeL a, SG.toList a)

obsD :: (I.Vector v, I.VecElem v a) => DG.Array v a -> ([Int], [a])
obsD x = (DG.shapeL x, DG.toList x)

-- Arrays of shape [2,3,4] over the elements, fresh and as views of other
-- arrays: transposed, reversed, sliced, strided and broadcast.
sources :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
           [a] -> [(String, SG.Array '[2,3,4] v a)]
sources xs =
  [ ("fresh", SG.fromList (take 24 xs))
  , ("transposed", SG.transpose @'[1,0,2] (SG.fromList @'[3,2,4] (take 24 xs)))
  , ("reversed", SG.rev @'[0,2] (SG.fromList (take 24 xs)))
  , ("sliced", SG.slice @'[ '(1,2), '(1,3), '(0,4) ] (SG.fromList @'[3,4,5] (take 60 xs)))
  , ("strided", SG.stride @'[1,2] (SG.fromList @'[2,5,4] (take 40 xs)))
  , ("broadcast", SG.broadcast @'[0,2] @'[2,3,4] (SG.fromList @'[2,4] (take 8 xs)))
  ]

-- The Shaped operations on an array of shape [2,3,4] and their Dynamic
-- counterparts, alone and composed, and the Shaped arrays built from
-- nothing, which ignore the source.
ops :: forall v a . (I.Vector v, I.VecElem v a, Elem a) =>
       [(String, SG.Array '[2,3,4] v a -> ([Int], [a]), DG.Array v a -> ([Int], [a]))]
ops =
  [ ("transpose [2,0,1]", obs . SG.transpose @'[2,0,1], obsD . DG.transpose [2,0,1])
  , ("transpose [1,0]", obs . SG.transpose @'[1,0], obsD . DG.transpose [1,0])
  , ("rev [1]", obs . SG.rev @'[1], obsD . DG.rev [1])
  , ("rev [0,2]", obs . SG.rev @'[0,2], obsD . DG.rev [0,2])
  , ("slice [(1,1),(0,2)]", obs . SG.slice @'[ '(1,1), '(0,2) ], obsD . DG.slice [(1,1),(0,2)])
  , ("stride [2,2,3]", obs . SG.stride @'[2,2,3], obsD . DG.stride [2,2,3])
  , ("window [2,2]", obs . SG.window @'[2,2], obsD . DG.window [2,2])
  , ("rotate 0 3", obs . SG.rotate @0 @3, obsD . DG.rotate 0 3)
  , ("rotate 1 0", obs . SG.rotate @1 @0, obsD . DG.rotate 1 0)
  , ("rotate 2 5", obs . SG.rotate @2 @5, obsD . DG.rotate 2 5)
  , ("index 1", obs . (`SG.index` 1), obsD . (`DG.index` 1))
  , ( "broadcast [0,2,3] [2,5,3,4]", obs . SG.broadcast @'[0,2,3] @'[2,5,3,4]
    , obsD . DG.broadcast [0,2,3] [2,5,3,4] )
  , ("reshape [6,4]", obs . SG.reshape @'[6,4], obsD . DG.reshape [6,4])
  , ("reshape [4,3,2]", obs . SG.reshape @'[4,3,2], obsD . DG.reshape [4,3,2])
  , ("reshape [24]", obs . SG.reshape @'[24], obsD . DG.reshape [24])
  , ( "stretch [2,5,3,4] of reshape [2,1,3,4]"
    , obs . SG.stretch @'[2,5,3,4] . SG.reshape @'[2,1,3,4]
    , obsD . DG.stretch [2,5,3,4] . DG.reshape [2,1,3,4] )
  , ( "stretchOuter 3 of reshape [1,2,3,4]"
    , obs . SG.stretchOuter @3 . SG.reshape @'[1,2,3,4]
    , obsD . DG.stretchOuter 3 . DG.reshape [1,2,3,4] )
  , ("pad [(1,2),(0,1)]", obs . SG.pad @'[ '(1,2), '(0,1) ] 0, obsD . DG.pad [(1,2),(0,1)] 0)
  , ( "zipWith4A with rev [0], rev [1] and rev [2]"
    , \ a -> obs (SG.zipWith4A f4 a (SG.rev @'[0] a) (SG.rev @'[1] a) (SG.rev @'[2] a))
    , \ x -> obsD (DG.zipWith4A f4 x (DG.rev [0] x) (DG.rev [1] x) (DG.rev [2] x)) )
  , ( "zipWith5A with rev [0], rev [1], rev [2] and itself"
    , \ a -> obs (SG.zipWith5A f5 a (SG.rev @'[0] a) (SG.rev @'[1] a) (SG.rev @'[2] a) a)
    , \ x -> obsD (DG.zipWith5A f5 x (DG.rev [0] x) (DG.rev [1] x) (DG.rev [2] x) x) )
  , ( "update [([1,2,3],7),([0,1,0],5),([1,2,3],6)]", \ a -> obs (SG.update a us)
    , \ x -> obsD (DG.update x us) )
  , ("append", \ a -> obs (SG.append a a), \ x -> obsD (DG.append x x))
  , ( "concatOuter of itself, rev [1] and itself", \ a -> obs (SG.concatOuter @6 [a, SG.rev @'[1] a, a])
    , \ x -> obsD (DG.concatOuter [x, DG.rev [1] x, x]) )
  , ( "unravel"
    , \ a -> nested (map obs (SG.toList (SG.unravel a :: SG.Array '[2] V.Vector (SG.Array '[3,4] v a))))
    , \ x -> nested (map obsD (DG.toList (DG.unravel x :: DG.Array V.Vector (DG.Array v a)))) )
  , ( "ravel of unravel"
    , \ a -> obs (SG.ravel (SG.unravel a :: SG.Array '[2] V.Vector (SG.Array '[3,4] v a)))
    , \ x -> obsD (DG.ravel (DG.unravel x :: DG.Array V.Vector (DG.Array v a))) )
  , ( "rerank 1 (transpose [1,0])", obs . SG.rerank @1 (SG.transpose @'[1,0])
    , obsD . DG.rerank 1 (DG.transpose [1,0]) )
  , ( "rerank2 2 (zipWithA (+))", \ a -> obs (SG.rerank2 @2 (SG.zipWithA (+)) a a)
    , \ x -> obsD (DG.rerank2 2 (DG.zipWithA (+)) x x) )
  , ( "rev [1] of transpose [2,0,1] of broadcast [0,2,3] [2,5,3,4]"
    , obs . SG.rev @'[1] . SG.transpose @'[2,0,1] . SG.broadcast @'[0,2,3] @'[2,5,3,4]
    , obsD . DG.rev [1] . DG.transpose [2,0,1] . DG.broadcast [0,2,3] [2,5,3,4] )
  , ( "window [2] of stride [1,2,3] of rev [2]"
    , obs . SG.window @'[2] . SG.stride @'[1,2,3] . SG.rev @'[2]
    , obsD . DG.window [2] . DG.stride [1,2,3] . DG.rev [2] )
  , ( "slice [(0,2),(1,2)] of transpose [1,2,0] of index 1 of reshape [2,1,3,4]"
    , obs . SG.slice @'[ '(0,2), '(1,2) ] . SG.transpose @'[1,2,0] . (`SG.index` 1)
      . SG.reshape @'[2,1,3,4]
    , obsD . DG.slice [(0,2),(1,2)] . DG.transpose [1,2,0] . (`DG.index` 1)
      . DG.reshape [2,1,3,4] )
  , ( "constant [2,3] 7", const (obs (SG.constant @'[2,3] 7 :: SG.Array '[2,3] v a))
    , const (obsD (DG.constant [2,3] 7 :: DG.Array v a)) )
  , ( "generate [2,3] sum", const (obs (SG.generate @'[2,3] (fromIntegral . sum) :: SG.Array '[2,3] v a))
    , const (obsD (DG.generate [2,3] (fromIntegral . sum) :: DG.Array v a)) )
  , ( "iota 5", const (obs (SG.iota @5 :: SG.Array '[5] v a))
    , const (obsD (DG.iota 5 :: DG.Array v a)) )
  , ( "iterateN 5 (+ 1) 0", const (obs (SG.iterateN @5 (+ 1) 0 :: SG.Array '[5] v a))
    , const (obsD (DG.iterateN 5 (+ 1) 0 :: DG.Array v a)) )
  ]
  where nested ps = (concatMap fst ps, concatMap snd ps)
        f4 w0 w1 w2 w3 = w0 - 2 * w1 + 3 * w2 - 4 * w3
        f5 w0 w1 w2 w3 w4 = f4 w0 w1 w2 w3 + 5 * w4
        us = [([1,2,3], 7), ([0,1,0], 5), ([1,2,3], 6)]
