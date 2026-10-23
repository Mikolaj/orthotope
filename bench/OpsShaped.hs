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

-- The operations of the three Shaped modules, one list a vector kind and a
-- size, on a view: the large size, the shape [400, 500]; the small, [3, 3], the
-- least at which window keeps every dimension of more than one element; and the
-- empty, [0, 3].
{-# LANGUAGE CPP #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE RecordWildCards #-}
{-# LANGUAGE KindSignatures #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE TypeOperators #-}
module OpsShaped ( opsBLarge, opsSLarge, opsULarge
                 , opsBSmall, opsSSmall, opsUSmall
                 , opsBEmpty, opsSEmpty, opsUEmpty ) where

import qualified Control.Applicative as A
import Data.Foldable (fold)
import Data.Functor.Identity (Identity (..))
import Data.Int (Int64)
import Data.Monoid (Sum (..))
import Data.Proxy (Proxy)
import GHC.TypeLits (Nat, SomeNat (..), someNatVal, type (+), type (-))

import qualified Data.Array.Shaped as B
import qualified Data.Array.ShapedS as S
import qualified Data.Array.ShapedU as U

import Data.Array.Convert (convert, convertE)
import qualified Data.Array.Internal as I
import qualified Data.Array.Dynamic as DB
import qualified Data.Array.DynamicS as DS
import qualified Data.Array.Ranked as RB
import qualified Data.Array.RankedS as RS
import qualified Data.Array.Internal.Shaped as IB
import qualified Data.Array.Internal.ShapedG as SG
import qualified Data.Array.Internal.ShapedS as IS
import qualified Data.Array.Internal.ShapedU as IU

import Call ( Call (..), Form (..), Size (..), View (..), call, callOnce
            , elemsFrom, sizeEmpty, sizeLarge, sizeSmall )

-- The type arguments, named here because the C preprocessor that includes
-- the lists replaces no macro on a line after an apostrophe: those of every
-- size, then those over a size's rows and columns, which the macros below
-- apply to each size's.
type Perm = '[1, 0]
type Pads = '[ '(0, 1), '(1, 1)]
type Win = '[2, 2]
type Rev01 = '[0, 1]
type Str12 = '[1, 2]
type Pads0 = '[ '(0, 0), '(0, 0)]
type Pads1 = '[ '(1, 1)]
type Str22 = '[2, 2]
type Str2 = '[2]
type Bc14 = '[1, 4]
type Bc12 = '[1, 2]
type Bc123 = '[1, 2, 3]
type Rev1 = '[1]
type Sl1 = '[ '(0, 1)]
type Sl11 = '[ '(0, 1), '(0, 1)]
type Sh0 = ('[] :: [Nat])
type Vec (m :: Nat) = '[m]

type Sh (r :: Nat) (c :: Nat) = '[r, c]
type ShT (r :: Nat) (c :: Nat) = '[c, r]
type Row1 (c :: Nat) = '[1, c]
type Sl (r :: Nat) (c :: Nat) = '[ '(1, r - 2), '(1, c - 1)]
type ShR (r :: Nat) (c :: Nat) = '[r, c + 2]
type SlR (r :: Nat) (c :: Nat) = '[ '(0, r), '(1, c)]
type ShW (r :: Nat) (c :: Nat) = '[r, c + c]
type Sh3 (r :: Nat) (c :: Nat) = '[2, r, c]
type Sh5 (r :: Nat) (c :: Nat) = '[1, r, 2, 1, c]
type ShB (r :: Nat) (c :: Nat) = '[2, 2, r, c, 2]
type ShO (r :: Nat) (c :: Nat) = '[r + c - 1]
type Col1 (r :: Nat) = '[r, 1]
type Emp (c :: Nat) = '[0, c]
type SlNR (r :: Nat) (c :: Nat) = '[ '(0, r), '(0, c - 1)]

#define FAMILY_OPS "shaped-ops.inc"

#define SH (Sh ROWS COLS)
#define SHT (ShT ROWS COLS)
#define ROW1 (Row1 COLS)
#define SL (Sl ROWS COLS)
#define SHR (ShR ROWS COLS)
#define SLR (SlR ROWS COLS)
#define SHW (ShW ROWS COLS)
#define SH3 (Sh3 ROWS COLS)
#define SH5 (Sh5 ROWS COLS)
#define SHB (ShB ROWS COLS)
#define SHO (ShO ROWS COLS)
#define WINO (Vec COLS)
#define COL1 (Col1 ROWS)
#define EMP (Emp COLS)
#define SLNR (SlNR ROWS COLS)

#define ROWS 400
#define COLS 500
#define SIZE sizeLarge
#define FLAT (Vec 200000)
#define CAT 800
#define NN 200000
#define TW4 (Vec 32)
#define TW5 (Vec 96)
#define TW6 (Vec 97)
#define TWN (Vec 628)

#define OPSB opsBLarge
#define OPSS opsSLarge
#define OPSU opsULarge
#include "kinds.inc"

#undef TWN
#undef TW6
#undef TW5
#undef TW4
#undef NN
#undef CAT
#undef FLAT
#undef SIZE
#undef COLS
#undef ROWS
#define ROWS 3
#define COLS 3
#define SIZE sizeSmall
#define FLAT (Vec 9)
#define CAT 6
#define NN 9
#define TW4 (Vec 5)
#define TW5 (Vec 33)
#define TW6 (Vec 34)
#define TWN (Vec 172)

#define OPSB opsBSmall
#define OPSS opsSSmall
#define OPSU opsUSmall
#include "kinds.inc"

#undef TWN
#undef TW6
#undef TW5
#undef TW4
#undef NN
#undef CAT
#undef FLAT
#undef SIZE
#undef COLS
#undef ROWS
#define ROWS 0
#define COLS 3
#define SIZE sizeEmpty
#define FLAT (Vec 0)
#define CAT 0
#define NN 0

#define OPSB opsBEmpty
#define OPSS opsSEmpty
#define OPSU opsUEmpty
#include "kinds.inc"
