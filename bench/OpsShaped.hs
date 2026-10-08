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

-- The operations of the three Shaped modules, one list a vector kind.
{-# LANGUAGE CPP #-}
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE KindSignatures #-}
{-# LANGUAGE TypeApplications #-}
module OpsShaped (opsB, opsS, opsU) where

import Data.Functor.Identity (Identity (..))
import Data.Int (Int64)
import Data.Proxy (Proxy)
import GHC.TypeLits (Nat, SomeNat (..), someNatVal)

import qualified Data.Array.Shaped as B
import qualified Data.Array.ShapedS as S
import qualified Data.Array.ShapedU as U

import Call (Call (..), elems, n)

-- The type arguments, named here because the C preprocessor that includes
-- the lists replaces no macro on a line after an apostrophe.
type ShT = '[500, 400]
type Perm = '[1, 0]
type Sh = '[400, 500]
type Flat = '[200000]
type Row1 = '[1, 500]
type Pads = '[ '(1, 1), '(1, 1)]
type Win = '[2, 2]
type Sl = '[ '(1, 398)]
type Rev0 = '[0]
type Bc = '[1]
type Vec (m :: Nat) = '[m]

#define ARR B
#define OPS opsB
#include "shaped-ops.inc"
#undef OPS
#undef ARR

#define ARR S
#define OPS opsS
#define WITH_BITCAST
#include "shaped-ops.inc"
#undef WITH_BITCAST
#undef OPS
#undef ARR

#define ARR U
#define OPS opsU
#include "shaped-ops.inc"
