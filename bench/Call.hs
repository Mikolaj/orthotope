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

-- An operation applied to its input, on the views the calls share, and the
-- count of the bytes a call allocates, for the specialisation benchmark and
-- test alike.
{-# LANGUAGE ExistentialQuantification #-}
module Call ( Call (..), call, Form (..), View (..), views, viewName
            , n, elems, elemsFrom, axes
            , Size (..), sizeLarge, sizeSmall, sizeEmpty, allocated ) where

import Control.DeepSeq (NFData)
import Control.Exception (evaluate)
import Data.Typeable (Typeable)
import Data.Array.Internal (Axes (..), Axis (..), InnerFirst (..))
import Data.Char (toLower)
import Data.Int (Int64)
import GHC.Conc (getAllocationCounter, setAllocationCounter)
import GHC.Exts (inline)

import Summed (Summed (..))

-- | An operation, its name and its input, its result comparable to
-- another call's, and the operation with its result summed.
data Call = forall a b. (NFData a, NFData b, Eq b, Show b, Typeable b)
                     => Call String (a -> b) a (a -> Double)

-- | A call and its result summed at its site, compiled as a client's own
-- @summed (f x)@ is: 'inline' unfolds the row's expression @f@ into the sum,
-- and GHC inlines the operation there as it would for a client.  The expression
-- written out twice compiles the same; 'inline' on the operation's own name, at
-- the row, inlines more, but for a class method such as @convert@.
{-# INLINE call #-}
call :: (NFData a, NFData b, Eq b, Show b, Typeable b, Summed b)
     => String -> (a -> b) -> a -> Call
call nm f x = Call nm f x (\ y -> summed (inline f y))

-- | Whether a call's input is the view or the view normalized, every other
-- input derived from either alike.
data Form = Viewed | Normalized
  deriving Show

-- | How the view of a shape lies in its vector, each reaching a route of its
-- own: 'Dense', the natural strides, one slice of the vector, accessed in order
-- or not; 'Strided', the inner dimension at the stride of the outer's extent,
-- filled element by element in order and one slice out of order; 'Runs', rows
-- cut out of wider ones, runs in order or not, no one slice; 'Scaled', every
-- other element of each row, filled in order or not; 'Bcastmid', one row
-- repeated at stride 0, runs in order, one slice to a consumer that visits
-- a repeated element once; 'Flip', each row reversed, at stride -1, filled
-- element by element in order and one slice out of order; 'Window', each
-- row one element on from the one before, overlapping runs in order or not;
-- 'Bcast', one column repeated at stride 0, filled by setting runs in order,
-- one slice to a consumer that visits a repeated element once; 'Scalar', one
-- element at stride 0 throughout, filled by setting one run in order, one slice
-- of one element to such a consumer.
data View = Dense | Strided | Runs | Scaled | Bcastmid
          | Flip | Window | Bcast | Scalar
  deriving (Eq, Show, Enum, Bounded)

-- | Every view, the one 'opsB' and its kin share second.
views :: [View]
views = [minBound .. maxBound]

-- | The view's name, in lower case.
viewName :: View -> String
viewName v = case show v of
  c : cs -> toLower c : cs
  [] -> []

-- | The element count of the large shape, [400, 500].
n :: Int
n = 200000

-- | The elements of the large shape.
elems :: [Double]
elems = take n elemsFrom

-- | Elements without end, spread over [0, 1).
elemsFrom :: [Double]
elemsFrom = [ fromIntegral ((i * 2654435761) `mod` 1000003) / 1000003
            | i <- [0 :: Int ..] ]

-- | The axes of the large shape's 'Strided' view, [500, 400] transposed:
-- the inner dimension at stride 400, the outer at stride 1.
axes :: Axes
axes = Axes 400 500 (InnerFirst [Axis 1 400])

-- | A size's values but its rows, which the preprocessor's conditions read
-- and so stay a macro: the columns, a row, an element's index, the rows a slice
-- keeps, the elements per pair update2000 builds, and the elements of six
-- windows' input and the windows' lengths.
data Size = Size { cols, irow :: Int, ielem :: [Int], sliceRows, perPair, twn
                 , tw1, tw2, tw3, tw4, tw5, tw6 :: Int }

-- | The large size, [400, 500], the small, [3, 3], and the empty, [0, 3],
-- whose calls take none of the six windows, so that it keeps the small size's.
sizeLarge, sizeSmall, sizeEmpty :: Size
sizeLarge = Size { cols = 500, irow = 7, ielem = [3, 4], sliceRows = 398
                 , perPair = 100, twn = 628, tw1 = 2, tw2 = 3, tw3 = 4
                 , tw4 = 32, tw5 = 96, tw6 = 97 }
sizeSmall = Size { cols = 3, irow = 1, ielem = [1, 1], sliceRows = 1
                 , perPair = 2, twn = 172, tw1 = 2, tw2 = 3, tw3 = 4
                 , tw4 = 5, tw5 = 33, tw6 = 34 }
sizeEmpty = sizeSmall { irow = 0, ielem = [0, 0], sliceRows = 0 }

-- | The bytes the thread allocates evaluating @f x@ to WHNF.
{-# NOINLINE allocated #-}
allocated :: (a -> b) -> a -> IO Int64
allocated f x = do
  setAllocationCounter maxBound
  _ <- evaluate (f x)
  c <- getAllocationCounter
  return (maxBound - c)
