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

-- Storable pad and fillStrided on the view of the specialisation benchmark,
-- from a module the specialiser does not run in: the controls of
-- BenchViewsTest's bounds on what Storable and Unboxed calls allocate over
-- boxed ones and on what fillStrided allocates.  pad's call passes its element
-- dictionary at run time.  fillStrided's goes through a copy compiled for any
-- vector and element type, as a client's call reached the library's own before
-- fillStrided had a pragma, and passes both dictionaries; inlined here at
-- the Storable vector, with the element's dictionary alone at run time, it
-- allocated only its result.
{-# OPTIONS_GHC -fno-specialise #-}
module Unspecialised(unspecialisedPad, unspecialisedFill) where

import qualified Data.Array.DynamicS as DS
import qualified Data.Array.Internal as I
import qualified Data.Vector.Storable as VS

import Call (Call (..), elems)
import qualified Call

unspecialisedPad :: Call
unspecialisedPad =
  Call "pad" (DS.pad [(1, 1), (1, 1)] 0)
       (DS.transpose [1, 0] (DS.fromList [500, 400] elems))

unspecialisedFill :: Call
unspecialisedFill = Call "fillStrided" polymorphicFill (VS.fromList elems)

{-# NOINLINE polymorphicFill #-}
polymorphicFill :: (I.Vector v, I.VecElem v a) => v a -> v a
polymorphicFill = I.fillStrided Call.axes 0 Call.n
