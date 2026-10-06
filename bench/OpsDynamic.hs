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

-- The operations of the three Dynamic modules, one list a vector kind.
{-# LANGUAGE CPP #-}
module OpsDynamic (opsB, opsS, opsU) where

import Data.Functor.Identity (Identity (..))
import Data.Int (Int64)

import qualified Data.Array.Dynamic as B
import qualified Data.Array.DynamicS as S
import qualified Data.Array.DynamicU as U

import Call (Call (..), elems, n)

#define ARR B
#define OPS opsB
#define WITH_ROTATE
#include "dynamic-ops.inc"
#undef WITH_ROTATE
#undef OPS
#undef ARR

#define ARR S
#define OPS opsS
#define WITH_BITCAST
#define WITH_ROTATE
#include "dynamic-ops.inc"
#undef WITH_ROTATE
#undef WITH_BITCAST
#undef OPS
#undef ARR

#define ARR U
#define OPS opsU
#include "dynamic-ops.inc"
