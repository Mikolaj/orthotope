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

-- The operations of the three Dynamic modules, one list a vector kind and
-- a size, on a view: the large size, the shape [400, 500]; the small, [3, 3],
-- the least at which window keeps every dimension of more than one element;
-- and the empty, [0, 3].  'opsB', 'opsS' and 'opsU' are the large size's lists
-- on the strided view.
{-# LANGUAGE CPP #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE RecordWildCards #-}
module OpsDynamic ( opsB, opsS, opsU
                  , opsBLarge, opsSLarge, opsULarge
                  , opsBSmall, opsSSmall, opsUSmall
                  , opsBEmpty, opsSEmpty, opsUEmpty ) where

import Data.Foldable (fold)
import Data.Functor.Identity (Identity (..))
import Data.Int (Int64)
import Data.Monoid (Sum (..))

import qualified Data.Array.Dynamic as B
import qualified Data.Array.DynamicS as S
import qualified Data.Array.DynamicU as U

import Data.Array.Convert (convert, convertE)
import qualified Data.Array.Internal as I
import qualified Data.Array.Ranked as RB
import qualified Data.Array.RankedS as RS
import qualified Data.Array.Shaped as SB
import qualified Data.Array.ShapedS as SS
import qualified Data.Array.Internal.Dynamic as IB
import qualified Data.Array.Internal.DynamicG as DG
import qualified Data.Array.Internal.DynamicS as IS
import qualified Data.Array.Internal.DynamicU as IU

import Call ( Call (..), Form (..), Size (..), View (..), call, elemsFrom
            , sizeEmpty, sizeLarge, sizeSmall )

opsB, opsS, opsU :: [Call]
opsB = opsBLarge Viewed Strided
opsS = opsSLarge Viewed Strided
opsU = opsULarge Viewed Strided

-- The Shaped arrays' shapes the lists convert to, which the C preprocessor
-- must not see after an apostrophe: the view's, and one of a single row.
type ShD = '[400, 500]
type FlatD = '[200000]
type ShDSmall = '[3, 3]
type FlatDSmall = '[9]
type ShDEmpty = '[0, 3]
type FlatDEmpty = '[0]

#define SHD ShD
#define FLATD FlatD
#define ROWS 400
#define SIZE sizeLarge

#define OPSB opsBLarge
#define OPSS opsSLarge
#define OPSU opsULarge
#include "dynamic-kinds.inc"
#undef OPSU
#undef OPSS
#undef OPSB

#undef ROWS
#undef SIZE
#undef FLATD
#undef SHD
#define SHD ShDSmall
#define FLATD FlatDSmall
#define ROWS 3
#define SIZE sizeSmall

#define OPSB opsBSmall
#define OPSS opsSSmall
#define OPSU opsUSmall
#include "dynamic-kinds.inc"
#undef OPSU
#undef OPSS
#undef OPSB

#undef ROWS
#undef SIZE
#undef FLATD
#undef SHD
#define SHD ShDEmpty
#define FLATD FlatDEmpty
#define ROWS 0
#define SIZE sizeEmpty

#define OPSB opsBEmpty
#define OPSS opsSEmpty
#define OPSU opsUEmpty
#include "dynamic-kinds.inc"
#undef OPSU
#undef OPSS
#undef OPSB
