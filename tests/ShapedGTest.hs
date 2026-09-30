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
-- list instances of Vector: the random views of the dynamic test modules
-- as Shaped arrays of their shapes, and Shaped operations, with their
-- arguments fixed in the types, on arrays of one shape in several layouts.
module ShapedGTest(test) where

import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as D
import Data.Array.Internal.DynamicS ()
import Data.Array.Internal.DynamicU ()
import Data.Array.Internal.Shape (withShapeP)
import qualified Data.Array.Internal.ShapedG as S
import Data.Proxy (Proxy (..))
import qualified Data.Vector as V
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.QuickCheck
  (Property, choose, conjoin, counterexample, forAll, vectorOf, (.&&.), (===))
import Views (View (..), mkViewG, testPropertyN)

test :: Test
test = testGroup "ShapedG"
  [ backend @V.Vector "boxed"
  , backend @VS.Vector "Storable"
  , backend @VU.Vector "Unboxed"
  , backend @[] "list"
  ]

backend :: forall v . (I.Vector v, I.VecElem v Int, Ord (v Int), Show (v Int)) => String -> Test
backend n = testGroup n $
  testPropertyN "prop_views" (prop_views @v)
  : [ testProperty on (prop_op f g) | (on, f, g) <- ops @v ]

-- A random view, as a Shaped array of its shape, gives what it does as a
-- Dynamic array or a list: its elements, their reductions but maximumA and
-- minimumA, which want a shape known not to be empty, its order against an
-- array of its elements with at most one of them changed, and the results
-- of normalize, mapA, zipWithA and reduce; and it reads back from its show.
prop_views :: forall v . (I.Vector v, I.VecElem v Int, Ord (v Int), Show (v Int)) =>
              View -> Property
prop_views v@(View sh _) =
  forAll (vectorOf (product sh) (choose (-9, 9))) $ \ xs ->
  case mkViewG v xs :: D.Array v Int of
    x@(D.A xsh t) -> withShapeP xsh $ \ (_ :: Proxy sh) ->
      let s = S.A t :: S.Array sh v Int
          l = D.toList x
      in  forAll (choose (0, length l)) $ \ i ->
          let l' = [ if k == i then e + 1 else e | (k, e) <- zip [0 ..] l ]
              s' = S.fromList l' :: S.Array sh v Int
          in  S.toList s === l .&&. S.toVector s === D.toVector x
              .&&. S.toList (S.normalize s) === l
              .&&. S.sumA s === sum l .&&. S.productA s === product l
              .&&. S.anyA (> 0) s === any (> 0) l .&&. S.allA (> 0) s === all (> 0) l
              .&&. S.allSameA s === D.allSameA x
              .&&. (s == s') === (l == l') .&&. compare s s' === compare l l'
              .&&. S.toList (S.mapA (* 2) s) === map (* 2) l
              .&&. S.toList (S.zipWithA (-) s s') === zipWith (-) l l'
              .&&. S.unScalar (S.reduce (+) 0 s) === sum l
              .&&. read (show s) === s

-- The Shaped operation gives what the Dynamic one does on each source.
prop_op :: forall v . (I.Vector v, I.VecElem v Int) =>
           (S.Array '[2,3,4] v Int -> ([Int], [Int])) -> (D.Array v Int -> ([Int], [Int]))
        -> Property
prop_op f g = forAll (vectorOf 60 (choose (-9, 9))) $ \ xs ->
  conjoin [ counterexample n (f s === g (toD s)) | (n, s) <- sources xs ]

-- The Dynamic array a Shaped one is.
toD :: forall sh v a . S.Shape sh => S.Array sh v a -> D.Array v a
toD a@(S.A t) = D.A (S.shapeL a) t

-- The shape and the elements of an array.
obs :: (I.Vector v, I.VecElem v Int, S.Shape sh) => S.Array sh v Int -> ([Int], [Int])
obs a = (S.shapeL a, S.toList a)

obsD :: (I.Vector v, I.VecElem v Int) => D.Array v Int -> ([Int], [Int])
obsD x = (D.shapeL x, D.toList x)

-- Arrays of shape [2,3,4] over the elements, fresh and as views of other
-- arrays: transposed, reversed, sliced, strided and broadcast.
sources :: forall v . (I.Vector v, I.VecElem v Int) =>
           [Int] -> [(String, S.Array '[2,3,4] v Int)]
sources xs =
  [ ("fresh", S.fromList (take 24 xs))
  , ("transposed", S.transpose @'[1,0,2] (S.fromList @'[3,2,4] (take 24 xs)))
  , ("reversed", S.rev @'[0,2] (S.fromList (take 24 xs)))
  , ("sliced", S.slice @'[ '(1,2), '(1,3), '(0,4) ] (S.fromList @'[3,4,5] (take 60 xs)))
  , ("strided", S.stride @'[1,2] (S.fromList @'[2,5,4] (take 40 xs)))
  , ("broadcast", S.broadcast @'[0,2] @'[2,3,4] (S.fromList @'[2,4] (take 8 xs)))
  ]

-- The Shaped operations on an array of shape [2,3,4] and their Dynamic
-- counterparts, alone and composed, and the Shaped arrays built from
-- nothing, which ignore the source.
ops :: forall v . (I.Vector v, I.VecElem v Int) =>
       [(String, S.Array '[2,3,4] v Int -> ([Int], [Int]), D.Array v Int -> ([Int], [Int]))]
ops =
  [ ("transpose [2,0,1]", obs . S.transpose @'[2,0,1], obsD . D.transpose [2,0,1])
  , ("transpose [1,0]", obs . S.transpose @'[1,0], obsD . D.transpose [1,0])
  , ("rev [1]", obs . S.rev @'[1], obsD . D.rev [1])
  , ("rev [0,2]", obs . S.rev @'[0,2], obsD . D.rev [0,2])
  , ("slice [(1,1),(0,2)]", obs . S.slice @'[ '(1,1), '(0,2) ], obsD . D.slice [(1,1),(0,2)])
  , ("stride [2,2,3]", obs . S.stride @'[2,2,3], obsD . D.stride [2,2,3])
  , ("window [2,2]", obs . S.window @'[2,2], obsD . D.window [2,2])
  , ("index 1", obs . (`S.index` 1), obsD . (`D.index` 1))
  , ( "broadcast [0,2,3] [2,5,3,4]", obs . S.broadcast @'[0,2,3] @'[2,5,3,4]
    , obsD . D.broadcast [0,2,3] [2,5,3,4] )
  , ("reshape [6,4]", obs . S.reshape @'[6,4], obsD . D.reshape [6,4])
  , ("reshape [4,3,2]", obs . S.reshape @'[4,3,2], obsD . D.reshape [4,3,2])
  , ("reshape [24]", obs . S.reshape @'[24], obsD . D.reshape [24])
  , ( "stretch [2,5,3,4] of reshape [2,1,3,4]"
    , obs . S.stretch @'[2,5,3,4] . S.reshape @'[2,1,3,4]
    , obsD . D.stretch [2,5,3,4] . D.reshape [2,1,3,4] )
  , ( "stretchOuter 3 of reshape [1,2,3,4]"
    , obs . S.stretchOuter @3 . S.reshape @'[1,2,3,4]
    , obsD . D.stretchOuter 3 . D.reshape [1,2,3,4] )
  , ("pad [(1,2),(0,1)]", obs . S.pad @'[ '(1,2), '(0,1) ] 0, obsD . D.pad [(1,2),(0,1)] 0)
  , ("append", \ a -> obs (S.append a a), \ x -> obsD (D.append x x))
  , ( "unravel"
    , \ a -> nested (map obs (S.toList (S.unravel a :: S.Array '[2] V.Vector (S.Array '[3,4] v Int))))
    , \ x -> nested (map obsD (D.toList (D.unravel x :: D.Array V.Vector (D.Array v Int)))) )
  , ( "rerank 1 (transpose [1,0])", obs . S.rerank @1 (S.transpose @'[1,0])
    , obsD . D.rerank 1 (D.transpose [1,0]) )
  , ( "rerank2 2 (zipWithA (+))", \ a -> obs (S.rerank2 @2 (S.zipWithA (+)) a a)
    , \ x -> obsD (D.rerank2 2 (D.zipWithA (+)) x x) )
  , ( "rev [1] of transpose [2,0,1] of broadcast [0,2,3] [2,5,3,4]"
    , obs . S.rev @'[1] . S.transpose @'[2,0,1] . S.broadcast @'[0,2,3] @'[2,5,3,4]
    , obsD . D.rev [1] . D.transpose [2,0,1] . D.broadcast [0,2,3] [2,5,3,4] )
  , ( "window [2] of stride [1,2,3] of rev [2]"
    , obs . S.window @'[2] . S.stride @'[1,2,3] . S.rev @'[2]
    , obsD . D.window [2] . D.stride [1,2,3] . D.rev [2] )
  , ( "slice [(0,2),(1,2)] of transpose [1,2,0] of index 1 of reshape [2,1,3,4]"
    , obs . S.slice @'[ '(0,2), '(1,2) ] . S.transpose @'[1,2,0] . (`S.index` 1)
      . S.reshape @'[2,1,3,4]
    , obsD . D.slice [(0,2),(1,2)] . D.transpose [1,2,0] . (`D.index` 1)
      . D.reshape [2,1,3,4] )
  , ( "constant [2,3] 7", const (obs (S.constant @'[2,3] 7 :: S.Array '[2,3] v Int))
    , const (obsD (D.constant [2,3] 7 :: D.Array v Int)) )
  , ( "generate [2,3] sum", const (obs (S.generate @'[2,3] sum :: S.Array '[2,3] v Int))
    , const (obsD (D.generate [2,3] sum :: D.Array v Int)) )
  , ( "iota 5", const (obs (S.iota @5 :: S.Array '[5] v Int))
    , const (obsD (D.iota 5 :: D.Array v Int)) )
  ]
  where nested ps = (concatMap fst ps, concatMap snd ps)
