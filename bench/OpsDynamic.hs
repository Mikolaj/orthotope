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

#define ARR B
#define IARR IB
#define CONV S
#define CR RB
#define CS SB
#define BOXED
#define OPS opsBLarge
#include "dynamic-ops.inc"
#undef OPS
#undef BOXED
#undef CS
#undef CR
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CR RS
#define CS SS
#define OPS opsSLarge
#define WITH_BITCAST
#include "dynamic-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CS
#undef CR
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsULarge
#include "dynamic-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR

#undef ROWS
#undef SIZE
#undef FLATD
#undef SHD
#define SHD ShDSmall
#define FLATD FlatDSmall
#define ROWS 3
#define SIZE sizeSmall

#define ARR B
#define IARR IB
#define CONV S
#define CR RB
#define CS SB
#define BOXED
#define OPS opsBSmall
#include "dynamic-ops.inc"
#undef OPS
#undef BOXED
#undef CS
#undef CR
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CR RS
#define CS SS
#define OPS opsSSmall
#define WITH_BITCAST
#include "dynamic-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CS
#undef CR
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsUSmall
#include "dynamic-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR

#undef ROWS
#undef SIZE
#undef FLATD
#undef SHD
#define SHD ShDEmpty
#define FLATD FlatDEmpty
#define ROWS 0
#define SIZE sizeEmpty

#define ARR B
#define IARR IB
#define CONV S
#define CR RB
#define CS SB
#define BOXED
#define OPS opsBEmpty
#include "dynamic-ops.inc"
#undef OPS
#undef BOXED
#undef CS
#undef CR
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CR RS
#define CS SS
#define OPS opsSEmpty
#define WITH_BITCAST
#include "dynamic-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CS
#undef CR
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsUEmpty
#include "dynamic-ops.inc"
