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

-- The type arguments of operations whose constraints changed, applied in
-- the order 0.1.8.0 quantified them, so that this module compiles only while
-- that order holds: an operation that loses a constraint keeps the order of
-- its type variables by an explicit forall.
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE TypeApplications #-}
module TypeAppTest(test) where

import qualified Data.Array.Ranked as R
import qualified Data.Array.RankedS as RS
import qualified Data.Array.RankedU as RU
import qualified Data.Array.Shaped as S
import qualified Data.Array.ShapedG as SG
import qualified Data.Array.ShapedS as SS
import qualified Data.Array.ShapedU as SU
import qualified Data.Vector as V
import Test.Framework (Test, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.HUnit (assertEqual)

test :: Test
test = testGroup "TypeApp"
  [ testCase "order" $ do
      assertEqual "S" [0, 0, 0, 0, 0] (S.toList (S.stretchOuter @5 (S.constant 0 :: S.Array '[1, 1] Int)))
      assertEqual "SS" [0, 0, 0, 0, 0] (SS.toList (SS.stretchOuter @5 (SS.constant 0 :: SS.Array '[1, 1] Int)))
      assertEqual "SU" [0, 0, 0, 0, 0] (SU.toList (SU.stretchOuter @5 (SU.constant 0 :: SU.Array '[1, 1] Int)))
  , testCase "index" $ do
      assertEqual "SS" [3, 4] (SS.toList (SS.index @Int @3 (SS.fromList [1 .. 6] :: SS.Array '[3, 2] Int) 1))
      assertEqual "SU" [3, 4] (SU.toList (SU.index @Int @3 (SU.fromList [1 .. 6] :: SU.Array '[3, 2] Int) 1))
      assertEqual "RS" [3, 4] (RS.toList (RS.index @Int @1 (RS.fromList [3, 2] [1 .. 6] :: RS.Array 2 Int) 1))
      assertEqual "RU" [3, 4] (RU.toList (RU.index @Int @1 (RU.fromList [3, 2] [1 .. 6] :: RU.Array 2 Int) 1))
  , testCase "reshape" $ do
      assertEqual "RS" [3, 1, 2] (RS.shapeL (RS.reshape @Int @2 @3 [3, 1, 2] (RS.fromList [3, 2] [1 .. 6])))
      assertEqual "RU" [3, 1, 2] (RU.shapeL (RU.reshape @Int @2 @3 [3, 1, 2] (RU.fromList [3, 2] [1 .. 6])))
  , testCase "pad" $
      assertEqual "R" [0, 1, 2, 0] (R.toList (R.pad @1 @Int [(1, 1)] 0 (R.fromList [2] [1, 2])))
  , testCase "ravel" $
      assertEqual "SG" [1, 2, 3, 4, 5, 6]
        (SG.toList (SG.ravel @V.Vector @V.Vector @Int @'[2] @3
                      (SG.fromList [SG.fromList [1, 2], SG.fromList [3, 4], SG.fromList [5, 6]])))
  ]
