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

-- The operations of the three Shaped modules, one list a vector kind and
-- a size, on a view: the large size, the shape [400, 500]; the small, [3, 3],
-- the least at which window keeps every dimension of more than one element;
-- and the empty, [0, 3].  'opsB', 'opsS' and 'opsU' are the large size's lists
-- on the strided view.
{-# LANGUAGE CPP #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE RecordWildCards #-}
{-# LANGUAGE KindSignatures #-}
{-# LANGUAGE TypeApplications #-}
module OpsShaped ( opsB, opsS, opsU
                 , opsBLarge, opsSLarge, opsULarge
                 , opsBSmall, opsSSmall, opsUSmall
                 , opsBEmpty, opsSEmpty, opsUEmpty ) where

import qualified Control.Applicative as A
import Data.Foldable (fold)
import Data.Functor.Identity (Identity (..))
import Data.Int (Int64)
import Data.Monoid (Sum (..))
import Data.Proxy (Proxy)
import GHC.TypeLits (Nat, SomeNat (..), someNatVal)

import qualified Data.Array.Shaped as B
import qualified Data.Array.ShapedS as S
import qualified Data.Array.ShapedU as U

import Data.Array.Convert (convert, convertE)
import qualified Data.Array.Internal as I
import qualified Data.Array.Dynamic as DB
import qualified Data.Array.DynamicS as DS
import qualified Data.Array.Ranked as RB
import qualified Data.Array.Internal.Shaped as IB
import qualified Data.Array.Internal.ShapedG as SG
import qualified Data.Array.Internal.ShapedS as IS
import qualified Data.Array.Internal.ShapedU as IU

import Call ( Call (..), Form (..), Size (..), View (..), call, elemsFrom
            , sizeEmpty, sizeLarge, sizeSmall )

opsB, opsS, opsU :: [Call]
opsB = opsBLarge Viewed Strided
opsS = opsSLarge Viewed Strided
opsU = opsULarge Viewed Strided

-- The type arguments, named here because the C preprocessor that includes
-- the lists replaces no macro on a line after an apostrophe: those of every
-- size, then the large size's, the small size's and the empty size's.
type Perm = '[1, 0]
type Pads = '[ '(0, 1), '(1, 1)]
type Win = '[2, 2]
type Rev01 = '[0, 1]
type Str2 = '[1, 2]
type Pads0 = '[ '(0, 0), '(0, 0)]
type Pads1 = '[ '(1, 1)]
type Str22 = '[2, 2]
type Str1 = '[2]
type Bc14 = '[1, 4]
type Bc12 = '[1, 2]
type Bc123 = '[1, 2, 3]
type Rev1 = '[1]
type Sl1 = '[ '(0, 1)]
type TwE1 = '[2]
type TwE2 = '[3]
type TwE3 = '[4]
type Sl11 = '[ '(0, 1), '(0, 1)]
type Sh0 = ('[] :: [Nat])
type Vec (m :: Nat) = '[m]

type Sh = '[400, 500]
type ShT = '[500, 400]
type Flat = '[200000]
type Row1 = '[1, 500]
type Sl = '[ '(1, 398), '(1, 499)]
type ShR = '[400, 502]
type SlR = '[ '(0, 400), '(1, 500)]
type ShW = '[400, 1000]
type Sh3 = '[2, 400, 500]
type Sh5 = '[1, 400, 2, 1, 500]
type ShB = '[2, 2, 400, 500, 2]
type ShO = '[899]
type WinO = '[500]
type Col1 = '[400, 1]
type Emp = '[0, 500]
type TwE4 = '[32]
type TwE5 = '[96]
type TwE6 = '[97]
type TwN = '[628]
type SlNR = '[ '(0, 400), '(0, 499)]

type ShSmall = '[3, 3]
type ShTSmall = '[3, 3]
type FlatSmall = '[9]
type Row1Small = '[1, 3]
type SlSmall = '[ '(1, 1), '(1, 2)]
type ShRSmall = '[3, 5]
type SlRSmall = '[ '(0, 3), '(1, 3)]
type ShWSmall = '[3, 6]
type Sh3Small = '[2, 3, 3]
type Sh5Small = '[1, 3, 2, 1, 3]
type ShBSmall = '[2, 2, 3, 3, 2]
type ShOSmall = '[5]
type WinOSmall = '[3]
type Col1Small = '[3, 1]
type EmpSmall = '[0, 3]
type TwE4Small = '[5]
type TwE5Small = '[33]
type TwE6Small = '[34]
type TwNSmall = '[172]
type SlNRSmall = '[ '(0, 3), '(0, 2)]

type ShEmpty = '[0, 3]
type ShTEmpty = '[3, 0]
type FlatEmpty = '[0]
type Row1Empty = '[1, 3]
type ShREmpty = '[0, 5]
type SlREmpty = '[ '(0, 0), '(1, 3)]
type ShWEmpty = '[0, 6]
type Sh3Empty = '[2, 0, 3]
type Sh5Empty = '[1, 0, 2, 1, 3]
type ShBEmpty = '[2, 2, 0, 3, 2]
type Col1Empty = '[0, 1]
type SlNREmpty = '[ '(0, 0), '(0, 2)]

#define TW1 TwE1
#define TW2 TwE2
#define TW3 TwE3
#define TW4 TwE4
#define TW5 TwE5
#define TW6 TwE6
#define TWN TwN
#define SLNR SlNR
#define ROWS 400
#define SIZE sizeLarge
#define SH Sh
#define SHT ShT
#define FLAT Flat
#define ROW1 Row1
#define SL Sl
#define CAT 800
#define NN 200000
#define SHR ShR
#define SLR SlR
#define SHW ShW
#define SH3 Sh3
#define SH5 Sh5
#define SHB ShB
#define SHO ShO
#define WINO WinO
#define COL1 Col1
#define EMP Emp

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CR RB
#define BOXED
#define OPS opsBLarge
#include "shaped-ops.inc"
#undef OPS
#undef BOXED
#undef CR
#undef CD
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CD DS
#define OPS opsSLarge
#define WITH_BITCAST
#include "shaped-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CD
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsULarge
#include "shaped-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR

#undef EMP
#undef COL1
#undef WINO
#undef SHO
#undef SHB
#undef SH5
#undef SH3
#undef SHW
#undef SLR
#undef SHR
#undef NN
#undef CAT
#undef SL
#undef ROW1
#undef FLAT
#undef SHT
#undef SH
#undef ROWS
#undef SIZE
#undef SLNR
#undef TWN
#undef TW6
#undef TW5
#undef TW4
#undef TW3
#undef TW2
#undef TW1
#define TW1 TwE1
#define TW2 TwE2
#define TW3 TwE3
#define TW4 TwE4Small
#define TW5 TwE5Small
#define TW6 TwE6Small
#define TWN TwNSmall
#define SLNR SlNRSmall
#define ROWS 3
#define SIZE sizeSmall
#define SH ShSmall
#define SHT ShTSmall
#define FLAT FlatSmall
#define ROW1 Row1Small
#define SL SlSmall
#define CAT 6
#define NN 9
#define SHR ShRSmall
#define SLR SlRSmall
#define SHW ShWSmall
#define SH3 Sh3Small
#define SH5 Sh5Small
#define SHB ShBSmall
#define SHO ShOSmall
#define WINO WinOSmall
#define COL1 Col1Small
#define EMP EmpSmall

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CR RB
#define BOXED
#define OPS opsBSmall
#include "shaped-ops.inc"
#undef OPS
#undef BOXED
#undef CR
#undef CD
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CD DS
#define OPS opsSSmall
#define WITH_BITCAST
#include "shaped-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CD
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsUSmall
#include "shaped-ops.inc"
#undef OPS
#undef CONV
#undef IARR
#undef ARR

#undef EMP
#undef COL1
#undef WINO
#undef SHO
#undef SHB
#undef SH5
#undef SH3
#undef SHW
#undef SLR
#undef SHR
#undef NN
#undef CAT
#undef SL
#undef ROW1
#undef FLAT
#undef SHT
#undef SH
#undef ROWS
#undef SIZE
#undef SLNR
#undef TWN
#undef TW6
#undef TW5
#undef TW4
#undef TW3
#undef TW2
#undef TW1
#define SLNR SlNREmpty
#define ROWS 0
#define SIZE sizeEmpty
#define SH ShEmpty
#define SHT ShTEmpty
#define FLAT FlatEmpty
#define ROW1 Row1Empty
#define CAT 0
#define NN 0
#define SHR ShREmpty
#define SLR SlREmpty
#define SHW ShWEmpty
#define SH3 Sh3Empty
#define SH5 Sh5Empty
#define SHB ShBEmpty
#define COL1 Col1Empty

#define ARR B
#define IARR IB
#define CONV S
#define CD DB
#define CR RB
#define BOXED
#define OPS opsBEmpty
#include "shaped-ops.inc"
#undef OPS
#undef BOXED
#undef CR
#undef CD
#undef CONV
#undef IARR
#undef ARR

#define ARR S
#define IARR IS
#define CONV B
#define STORABLE
#define CD DS
#define OPS opsSEmpty
#define WITH_BITCAST
#include "shaped-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef CD
#undef STORABLE
#undef CONV
#undef IARR
#undef ARR

#define ARR U
#define IARR IU
#define CONV B
#define OPS opsUEmpty
#include "shaped-ops.inc"
