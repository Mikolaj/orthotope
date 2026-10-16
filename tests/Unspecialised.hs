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

-- pad and fillStrided on the specialisation benchmark's large strided view,
-- from a module the specialiser does not run in, at Storable and at Unboxed.
-- pad's call passes its element dictionary at run time.  fillStrided's goes
-- through a copy compiled for any vector and element type, as a client's call
-- reached the library's own before fillStrided had a pragma, and passes both
-- dictionaries.  At Unboxed they are the controls of BenchViewsTest's bounds
-- on what Storable and Unboxed calls allocate over boxed ones and on what
-- fillStrided allocates; at Storable, whose fill copies elements by their size,
-- they meet those bounds.
{-# OPTIONS_GHC -fno-specialise #-}
module Unspecialised
  ( unspecialisedPad, unspecialisedPadU, unspecialisedFill, unspecialisedFillU
  ) where

import qualified Data.Array.DynamicS as DS
import qualified Data.Array.DynamicU as DU
import qualified Data.Array.Internal as I
import qualified Data.Vector.Storable as VS
import qualified Data.Vector.Unboxed as VU

import Call (Call (..), elems)
import qualified Call

unspecialisedPad :: Call
unspecialisedPad =
  Call.call "pad" (\ a -> DS.pad [(0, 1), (1, 1)] 0 a)
            (DS.transpose [1, 0] (DS.fromList [500, 400] elems))

unspecialisedPadU :: Call
unspecialisedPadU =
  Call.call "pad" (\ a -> DU.pad [(0, 1), (1, 1)] 0 a)
            (DU.transpose [1, 0] (DU.fromList [500, 400] elems))

unspecialisedFill :: Call
unspecialisedFill = Call.call "fillStrided" polymorphicFill (VS.fromList elems)

unspecialisedFillU :: Call
unspecialisedFillU = Call.call "fillStrided" polymorphicFill (VU.fromList elems)

{-# NOINLINE polymorphicFill #-}
polymorphicFill :: (I.Vector v, I.VecElem v a) => v a -> v a
polymorphicFill v = I.fillStrided Call.axes 0 Call.n v
