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

-- An operation applied to its input, on the one view all the calls share,
-- for the specialisation benchmark and test alike.
{-# LANGUAGE ExistentialQuantification #-}
module Call (Call (..), n, elems) where

import Control.DeepSeq (NFData)

-- | An operation, its name and its input.
data Call = forall a b. (NFData a, NFData b) => Call String (a -> b) a

-- | The element count of the one shape, [400, 500].
n :: Int
n = 200000

-- | The elements, spread over [0, 1).
elems :: [Double]
elems = [ fromIntegral ((i * 2654435761) `mod` 1000003) / 1000003
        | i <- [0 .. n - 1] ]
