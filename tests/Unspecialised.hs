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

-- Storable pad on the view of the specialisation benchmark, from a module the
-- specialiser does not run in, so that the call passes its element dictionary
-- at run time: the control of BenchViewsTest's bound on what Storable and
-- Unboxed calls allocate over boxed ones.
{-# OPTIONS_GHC -fno-specialise #-}
module Unspecialised(unspecialisedPad) where

import qualified Data.Array.DynamicS as DS

import Call (Call (..), elems)

unspecialisedPad :: Call
unspecialisedPad =
  Call "pad" (DS.pad [(1, 1), (1, 1)] 0)
       (DS.transpose [1, 0] (DS.fromList [500, 400] elems))
