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

-- The views a micro-benchmark of toVector measured, with the shapes,
-- strides and offsets it gave them, over random Storable elements, and
-- what it checked of them: the values that toVector, toList, the two lists
-- of vectors and sumA give, what toVector and sumA allocate, how much
-- building the head of a list of vectors allocates, and what the lists
-- hold for an empty view; and what == allocates on a broadcast of a view
-- that skips elements, and == and mapA on an empty view.
-- Its bounds on toVector, sumA and the list heads run in an optimised
-- build alone.
module BenchViewsTest(test) where

import Control.Exception (evaluate)
import Data.Array.DynamicS (mapA, sumA, toList, toVector)
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import qualified Data.Array.Internal.DynamicS as DS
import Data.Bits (shiftR, xor)
import Data.Int (Int64)
import Data.List (mapAccumR)
import qualified Data.Vector.Storable as VS
import GHC.Conc (getAllocationCounter, setAllocationCounter)
import Test.Framework (Test, TestOptions' (..), plusTestOptions, testGroup)
import Test.Framework.Providers.HUnit (testCase)
import Test.Framework.Providers.QuickCheck2 (testProperty)
import Test.HUnit (Assertion, assertBool)
import Test.QuickCheck (Property, choose, counterexample, forAll, (.&&.), (===))

-- A view's shape, strides and offset, and the length of the vector
-- under it.
type Layout = ([Int], [Int], Int, Int)

test :: Test
test = testGroup "BenchViews"
  [ testGroup "values"
      [ testOnce n (prop_values l) | (n, l) <- mainViews ++ otherViews ]
  , optimisedGroup "toVector allocation"
      $  [ testCase n (allocUnder (scaled toVectorFactor l) toVector l)
         | (n, l) <- mainViews ++ otherViews ]
      ++ [ testCase "transposed runs, element by element"
             (allocOver (scaled toVectorFactor transposedBlock)
                        (headOf elementwise) transposedBlock) ]
  , optimisedGroup "sumA allocation"
      $  [ testCase n (allocUnder 16384 sumA l) | (n, l) <- mainViews ]
      ++ [ testCase n (allocUnder (scaled sumAFactor l) sumA l) | (n, l) <- otherViews ]
    -- The head of a list of vectors of a view of runs is one run, built
    -- in under 32768 bytes, the lists being lazy.
  , optimisedGroup "list heads"
      [ testCase "ordered, runs"
          (allocUnder 32768 (headOf I.toVectorListT) runsBlock)
      , testCase "unordered, runs"
          (allocUnder 32768 (headOf I.toUnorderedVectorListT) runsBlock)
      , testCase "ordered, transposed runs"
          (allocUnder (scaled orderedHeadFactor transposedBlock)
                      (headOf I.toVectorListT) transposedBlock)
      , testCase "ordered, transposed runs, element by element"
          (allocOver (scaled orderedHeadFactor transposedBlock)
                     (headOf elementwise) transposedBlock)
      , testCase "unordered, transposed runs"
          (allocUnder (scaled unorderedHeadFactor transposedBlock)
                      (headOf I.toUnorderedVectorListT) transposedBlock) ]
    -- == compares a broadcast of a view that skips elements without its
    -- broadcast dimensions, and == and mapA take an empty view at once, in
    -- under 32768 bytes.
  , testGroup "== allocation"
      [ testCase "broadcast of a strided row" (allocUnder 32768 (\ x -> x == x) stridedBroadcast)
      , testCase "empty view" (allocUnder 32768 (\ x -> x == x) emptyView) ]
  , testGroup "mapA allocation"
      [ testCase "empty view" (allocUnder 32768 (mapA (+ 1)) emptyView) ]
    -- The lists of vectors of an empty view hold no vector.
  , testGroup "empty lists"
      [ testCase (vn ++ ", " ++ n) (assertBool "a vector" (null (f sh t)))
      | (vn, l@(sh, _, _, _)) <- [ (n, mkStrided s) | (n, s) <- degenerateShapes ]
      , let t = fst (mkArray 1 l)
      , (n, f) <- [ ("ordered", I.toVectorListT)
                  , ("unordered", I.toUnorderedVectorListT) ] ]
  ]

-- The bounds on toVector, sumA and the list heads hold for an optimised
-- build alone, an unoptimised one allocating more for each element, so
-- their groups run empty there.
optimisedGroup :: String -> [Test] -> Test
optimisedGroup n ts = testGroup n (if optimised then ts else [])

-- Whether this module was optimised: the rule fires only when optimising.
optimised :: Bool
optimised = False
{-# NOINLINE optimised #-}
{-# RULES "optimised" optimised = True #-}

-- What toVector allocates, over the view's size: the result alone, 1.0 on
-- these views, under a bound that listing the transposed runs element by
-- element, 21, exceeds.
toVectorFactor :: Double
toVectorFactor = 2

-- What sumA allocates, over the view's size, where the unordered list does
-- not take the view as one block: up to 2 on these views, under a bound
-- that listing a view element by element, over 40, exceeds.  On the
-- transposed dense arrays of mainViews, which it takes as one block, sumA
-- allocates under 16384 bytes.
sumAFactor :: Double
sumAFactor = 4

-- What building the head of the ordered list of a transposed view of runs
-- allocates, over the view's size: the whole view filled, 1.0, under a
-- bound that listing it element by element, 21, exceeds.
orderedHeadFactor :: Double
orderedHeadFactor = 4

-- The same for the unordered list, which could instead walk the runs in
-- the order of the vector and build its head in under 32768 bytes, as it
-- does for the runs untransposed.
unorderedHeadFactor :: Double
unorderedHeadFactor = 64

-- A factor times the size of a view of Doubles, plus 32768 bytes for the
-- costs of a call, which a small view's size does not cover.
scaled :: Double -> Layout -> Int64
scaled factor (sh, _, _, _) = round (factor * 8 * fromIntegral (product sh)) + 32768

-- The mkStrided views of the shapes of convolutions, of the extremes and
-- of the empty views.
mainViews :: [(String, Layout)]
mainViews =
  [ (n, mkStrided s) | (n, s) <- convShapes ++ stretchShapes ++ degenerateShapes ]

-- The views of the stride classes, and a unit dimension of stride 0 beside
-- one of stride 1 at a non-zero offset.
otherViews :: [(String, Layout)]
otherViews = classViews ++ [ ("reshape1-slice-off7", ([50, 1], [1, 0], 7, 100)) ]

-- 200000 runs of 20 with a gap of 12 between them, and the same
-- transposed.
runsBlock, transposedBlock :: Layout
runsBlock = mkBlock [200000, 20] [200000, 32] 0
transposedBlock = mkCompose [20, 200000] [1, 32] 0

-- A row of 2 elements 2 apart, broadcast to 100000 rows.
stridedBroadcast :: Layout
stridedBroadcast = ([100000, 2], [0, 2], 0, 3)

-- An empty view whose outer dimension has 10^7 indices.
emptyView :: Layout
emptyView = ([10000000, 0, 1], [1, 10000000, 1], 0, 0)

-- A property checked on one case, each case a view of up to about two
-- million elements, with a random seed.
testOnce :: String -> (Int -> Property) -> Test
testOnce n =
  plusTestOptions mempty { topt_maximum_generated_tests = Just 1 } . testProperty n
  . forAll (choose (0, maxBound))

-- The view over random elements drawn from the seed.
mkArray :: Int -> Layout -> (I.T VS.Vector Double, DS.Array Double)
mkArray seed (sh, ts, o, n) =
  let t = I.T ts o (randomVector seed n)
  in  (t, DS.A (DG.A sh t))

-- n pseudo-random integers below a million, as Doubles, so that any sum
-- of two million of them is exact whatever the order of summation.
randomVector :: Int -> Int -> VS.Vector Double
randomVector seed n =
  VS.generate n (\ i -> fromIntegral (mix (fromIntegral (seed + i)) `mod` 1000000))
  where mix :: Word -> Word
        mix z0 = let z1 = (z0 `xor` (z0 `shiftR` 30)) * 0xbf58476d1ce4e5b9
                     z2 = (z1 `xor` (z1 `shiftR` 27)) * 0x94d049bb133111eb
                 in  z2 `xor` (z2 `shiftR` 31)

-- The view's elements in row-major order, each read off the strides and
-- offset alone.
reference :: Layout -> VS.Vector Double -> VS.Vector Double
reference (sh, ts, o, _) v = VS.generate (product sh) (\ i -> v VS.! (o + at i))
  where at i = sum (zipWith (*) ts (snd (mapAccumR (\ q s -> q `quotRem` s) i sh)))

-- toVector, toList and the ordered list of vectors give the view's
-- elements in order, the unordered list gives as many as the view has
-- and their sum, and so does sumA; neither list holds an empty vector
-- when the view is not empty.
prop_values :: Layout -> Int -> Property
prop_values l@(sh, _, _, _) seed =
  let (t, x) = mkArray seed l
      r = reference l (I.values t)
      ordered = I.toVectorListT sh t
      unordered = I.toUnorderedVectorListT sh t
      nonEmpty vs = product sh == 0 || not (any VS.null vs)
  in  agree "toVector" (toVector x) r .&&. agree "toList" (VS.fromList (toList x)) r
      .&&. agree "ordered" (VS.concat ordered) r .&&. nonEmpty ordered
      .&&. sum (map VS.length unordered) === VS.length r
      .&&. sum (map VS.sum unordered) === VS.sum r .&&. nonEmpty unordered
      .&&. sumA x === VS.sum r

-- The vectors are equal, or where they first differ is reported, the
-- vectors themselves being too long to show.
agree :: String -> VS.Vector Double -> VS.Vector Double -> Property
agree what u r = counterexample (what ++ ": " ++ firstDiff) (u == r)
  where firstDiff
          | VS.length u /= VS.length r =
            "length " ++ show (VS.length u) ++ ", not " ++ show (VS.length r)
          | otherwise = case [ i | i <- [0 .. VS.length u - 1], u VS.! i /= r VS.! i ] of
              i : _ -> "at " ++ show i ++ ", " ++ show (u VS.! i) ++ ", not " ++ show (r VS.! i)
              [] -> "equal"

-- Evaluating f of the view, built and forced beforehand, to WHNF a second
-- time allocates at most the bound, in bytes; the first time can also
-- allocate a new chunk of the thread's stack.
allocUnder :: Int64 -> (DS.Array Double -> b) -> Layout -> Assertion
allocUnder bound f l = do
  bytes <- secondAlloc f l
  assertBool (show bytes ++ " bytes allocated, over " ++ show bound) (bytes <= bound)

-- The same allocates more than the bound: the control that shows a bound
-- tells what it holds apart.
allocOver :: Int64 -> (DS.Array Double -> b) -> Layout -> Assertion
allocOver bound f l = do
  bytes <- secondAlloc f l
  assertBool (show bytes ++ " bytes allocated, not over " ++ show bound) (bytes > bound)

-- What evaluating f of the view to WHNF allocates the second time.
secondAlloc :: (DS.Array Double -> b) -> Layout -> IO Int64
secondAlloc f l@(sh, ts, _, _) = do
  let (t, x) = mkArray 1 l
  _ <- evaluate (sum sh + sum ts + VS.length (I.values t))
  _ <- evaluate x
  _ <- allocated f x
  allocated f x

-- The bytes the thread allocates evaluating f x to WHNF.
{-# NOINLINE allocated #-}
allocated :: (a -> b) -> a -> IO Int64
allocated f x = do
  setAllocationCounter maxBound
  _ <- evaluate (f x)
  c <- getAllocationCounter
  return (maxBound - c)

-- The listing a fill replaced: the elements one by one into a vector, the
-- list forced whole first.
elementwise :: [Int] -> I.T VS.Vector Double -> [VS.Vector Double]
elementwise sh t = let xs = I.toListT sh t in length xs `seq` [I.vFromListN (length xs) xs]

-- The head of a list of vectors of the array.
headOf :: ([Int] -> I.T VS.Vector Double -> [VS.Vector Double])
       -> DS.Array Double -> VS.Vector Double
headOf f (DS.A (DG.A sh t)) = case f sh t of
  v : _ -> v
  [] -> error "headOf: an empty list"

-- The natural strides of a dense array of the given shape.
natural :: [Int] -> [Int]
natural = drop 1 . I.getStridesT

swapLast2 :: [a] -> [a]
swapLast2 xs = case reverse xs of
  a : b : r -> reverse (b : a : r)
  _ -> xs

-- A dense array with its two innermost dimensions transposed, as the
-- gather of a convolution merges them in; the shape listed is the dense
-- one.
mkStrided :: [Int] -> Layout
mkStrided sh = (swapLast2 sh, swapLast2 (natural sh), 0, product sh)

-- The dims rs of a view at offset 0 with non-negative strides ts
-- reversed: those strides negated, and the offset where the reversed
-- index map starts.
reverseDims :: [Int] -> [Int] -> [Int] -> ([Int], Int)
reverseDims rs sh ts =
  ( [ if r `elem` rs then negate t else t | (r, t) <- zip [0 ..] ts ]
  , sum [ (n - 1) * t | (r, (n, t)) <- zip [0 :: Int ..] (zip sh ts), r `elem` rs ] )

-- mkStrided's view with the dims rs reversed, so the strides are of
-- mixed signs, or all negative when rs are all the dims.
mkRevSome :: [Int] -> [Int] -> Layout
mkRevSome rs dsh = let (sh, ts, _, n) = mkStrided dsh
                       (ts', o) = reverseDims rs sh ts
                   in  (sh, ts', o, n)

mkRev :: [Int] -> Layout
mkRev dsh = mkRevSome [0 .. length dsh - 1] dsh

-- The given shape with its innermost dimension broadcast, at stride 0,
-- over a dense source of the outer dimensions.
mkBroadcast :: [Int] -> Layout
mkBroadcast sh = (sh, natural (init sh) ++ [0], 0, product (init sh))

-- mkStrided's view with a dimension of extent b at stride 0 inserted
-- after the outermost.
mkBroadcastMid :: Int -> [Int] -> Layout
mkBroadcastMid b dsh = case mkStrided dsh of
  (s0 : srest, t0 : trest, _, n) -> (s0 : b : srest, t0 : 0 : trest, 0, n)
  _ -> error "mkBroadcastMid: a scalar"

-- A dense array reshaped with a unit innermost dimension appended, which
-- gets stride 0.
mkReshape1 :: [Int] -> Layout
mkReshape1 dsh = mkBroadcast (dsh ++ [1])

-- The same over mkStrided's view.
mkReshape1Strided :: [Int] -> Layout
mkReshape1Strided dsh = let (sh, ts, o, n) = mkStrided dsh in (sh ++ [1], ts ++ [0], o, n)

-- mkStrided's view cut out of an enclosing dense array two larger in
-- every dimension, at offset 1 in each.
mkSliced :: [Int] -> Layout
mkSliced dsh = let es = natural (map (+ 2) dsh)
               in  (swapLast2 dsh, swapLast2 es, sum es, product (map (+ 2) dsh))

-- The patches of a dense [h, w] image, [oh, ow, kw, kh], for a window
-- stride s and a kernel dilation d, 1 unless listed: the strides repeat
-- the image's, so the view reads elements more than once.
mkWindow :: [Int] -> Layout
mkWindow [h, w, kh, kw] = mkWindow [h, w, kh, kw, 1, 1]
mkWindow [h, w, kh, kw, s, d] =
  let spanOf k = (k - 1) * d + 1
  in  ( [(h - spanOf kh) `div` s + 1, (w - spanOf kw) `div` s + 1, kw, kh]
      , [s * w, s, d, d * w], 0, h * w )
mkWindow sh = error ("mkWindow: " ++ show sh)

-- mkWindow over an image of c channels, the channel axis after the output
-- positions.
mkWindowChannels :: [Int] -> Layout
mkWindowChannels [h, w, c, kh, kw] =
  ([h - kh + 1, w - kw + 1, c, kw, kh], [w, 1, h * w, 1, w], 0, c * h * w)
mkWindowChannels sh = error ("mkWindowChannels: " ++ show sh)

-- Rows of contiguous runs, the rest of the dimensions, with a gap of one
-- element between them.
mkRuns :: [Int] -> Layout
mkRuns sh@(rows : inner) = let run = product inner
                           in  (sh, (run + 1) : natural inner, 0, rows * (run + 1))
mkRuns sh = error ("mkRuns: " ++ show sh)

-- A dense array of shape esh cut to shape sh at offset o.
mkBlock :: [Int] -> [Int] -> Int -> Layout
mkBlock sh esh o = (sh, natural esh, o, product esh)

-- mkBlock at offset 0 with the dims rs reversed.
mkFlipIn :: [Int] -> [Int] -> [Int] -> Layout
mkFlipIn rs sh esh = let (ts, o) = reverseDims rs sh (natural esh) in (sh, ts, o, product esh)

mkFlip :: [Int] -> [Int] -> Layout
mkFlip rs sh = mkFlipIn rs sh sh

-- The given strides at offset o over the shortest vector they fit.
mkCompose :: [Int] -> [Int] -> Int -> Layout
mkCompose sh ts o = (sh, ts, o, o + sum [ (s - 1) * t | (s, t) <- zip sh ts, t > 0 ] + 1)

-- The patch tensors of convolutions, [outH, outW, Cin, KH, KW], the patches
-- of one position, [Cin, KH, KW], and two shapes of rank 4, through
-- mkStrided.
convShapes :: [(String, [Int])]
convShapes =
  [ ("cnn-L1-6x6-c1",       [6, 6, 1, 3, 3])
  , ("cnn-L1-12x12-c1",     [12, 12, 1, 3, 3])
  , ("cnn-L1-24x24-c1",     [24, 24, 1, 3, 3])
  , ("cnn-L2-24x24-c32",    [24, 24, 32, 3, 3])
  , ("cnn-slice-c32",       [32, 3, 3])
  , ("lenet-L1-28-c1-k5",   [28, 28, 1, 5, 5])
  , ("lenet-slice-c6-k5",   [6, 5, 5])
  , ("cifar-L2-16-c64-k3",  [16, 16, 64, 3, 3])
  , ("vgg-14-c512-k3",      [14, 14, 512, 3, 3])
  , ("alexnet-L1-55-c3-k11",[55, 55, 3, 11, 11])
  , ("alexnet-L2-27-c48-k5",[27, 27, 48, 5, 5])
  , ("gather48-src-50",     [50, 3, 3, 50])
  , ("conv1d-24",           [24, 3, 3, 24])
  ]

-- Shapes at the extremes of rank, aspect and extent, through mkStrided.
stretchShapes :: [(String, [Int])]
stretchShapes =
  [ ("stretch-rank10",      [3,3,3,3,3,3,3,3,3,3])
  , ("stretch-wide-2xM",    [2, 900000])
  , ("stretch-primes",      [97, 89, 29])
  , ("stretch-bigstride",   [3, 3, 200000])
  , ("stretch-square-1341", [1341, 1341])
  , ("stretch-r5-8x432",    [8, 8, 8, 8, 432])
  , ("stretch-inner1",      [1, 500000])
  , ("stretch-tall-Mx2",    [900000, 2])
  , ("stretch-coprime-r7",  [2, 3, 5, 7, 11, 13, 2])
  , ("stretch-rank12",      [2,2,2,2,2,2,2,2,2,2,2,2])
  , ("stretch-tab7MB",      [900, 2, 1000])
  , ("stretch-pow2stride",  [54, 64, 512])
  , ("stretch-inner256",    [7, 256, 977])
  ]

-- Empty views through mkStrided: the view [0, 100000] and the view
-- [100000, 0].
degenerateShapes :: [(String, [Int])]
degenerateShapes =
  [ ("degenerate-m0",      [100000, 0])
  , ("degenerate-sinner0", [0, 100000])
  ]

-- The views of the stride classes, by the generators above.
classViews :: [(String, Layout)]
classViews =
  [ (n, mkRev s)
  | (n, s) <- [ ("rev-cnn-L1-24x24-c1", [24, 24, 1, 3, 3])
              , ("rev-gather48-src-50", [50, 3, 3, 50])
              , ("rev-primes",          [97, 89, 29]) ] ]
  ++ [ (n, mkRevSome rs s)
     | (n, rs, s) <- [ ("revsome-inner-primes", [2],    [97, 89, 29])
                     , ("revsome-outer-g48",    [0],    [50, 3, 3, 50])
                     , ("revsome-mid-cnn-L2",   [1, 2], [24, 24, 32, 3, 3]) ] ]
  ++ [ (n, mkBroadcast s)
     | (n, s) <- [ ("bcast-inner8",   [64, 100, 8])
                 , ("bcast-inner900", [50, 40, 900])
                 , ("bcast-tall-Mx2", [900000, 2])
                 , ("bcast-src8",     [8, 225000])
                 , ("bcast-src64",    [64, 28125])
                 , ("bcast-src512",   [512, 3515]) ] ]
  ++ [ (n, mkBroadcastMid b s)
     | (n, b, s) <- [ ("bcastmid-c32-cnn", 32, [24, 24, 3, 3])
                    , ("bcastmid-primes",  89, [97, 29])
                    , ("bcastmid-b200k",   200000, [3, 3])
                    , ("bcastmid-block150k", 4, [3, 300, 500])
                    , ("edge-bcastmid-b0", 0, [3, 3])
                    , ("edge-bcastmid-b0-deep", 0, [2, 3, 3])
                    , ("edge-bcastmid-b2", 2, [3, 3])
                    , ("edge-bcastmid-b3", 3, [3, 3])
                    , ("edge-bcastmid-b5", 5, [3, 3]) ] ]
  ++ [ (n, mkReshape1 s)
     | (n, s) <- [ ("reshape1-500k", [500000])
                 , ("reshape1-r3",   [100, 50, 36])
                 , ("reshape1-rank10", [3,3,3,3,3,3,3,3,3,3]) ] ]
  ++ [ ("reshape1-strided-r3", mkReshape1Strided [100, 50, 36]) ]
  ++ [ (n, mkSliced s)
     | (n, s) <- [ ("slice-cnn-L2-24x24-c32", [24, 24, 32, 3, 3])
                 , ("slice-primes",           [97, 89, 29])
                 , ("slice-coprime-r7",       [2, 3, 5, 7, 11, 13, 2]) ] ]
  ++ [ (n, mkWindow s)
     | (n, s) <- [ ("window-28x28-k5",      [28, 28, 5, 5])
                 , ("window-224x224-k3",    [224, 224, 3, 3])
                 , ("window-64x64-k1x9",    [64, 64, 1, 9])
                 , ("window-128x128-k7",    [128, 128, 7, 7])
                 , ("window-224x224-k3-s2", [224, 224, 3, 3, 2, 1])
                 , ("window-224x224-k3-d2", [224, 224, 3, 3, 1, 2]) ] ]
  ++ [ (n, mkWindowChannels s)
     | (n, s) <- [ ("window-64x64-c16-k3", [64, 64, 16, 3, 3])
                 , ("window-32x32-c64-k3", [32, 32, 64, 3, 3]) ] ]
  ++ [ (n, mkCompose s ts 0)
     | (n, s, ts) <- [ ("scaled-super-r3", [40, 50, 30], [4547, 91, 3])
                     , ("scaled-rank1-m1", [300000], [5])
                     , ("scaled-r5", [3,5,7,11,13], [14245,2849,407,37,3]) ] ]
  ++ [ (n, mkRuns s)
     | (n, s) <- [ ("runs-2",        [900000, 2])
                 , ("runs-3",        [600000, 3])
                 , ("runs-4",        [450000, 4])
                 , ("runs-5",        [360000, 5])
                 , ("runs-7",        [257142, 7])
                 , ("runs-9",        [200000, 9])
                 , ("runs-32",       [56250, 32])
                 , ("runs-48",       [37500, 48])
                 , ("runs-64",       [28125, 64])
                 , ("runs-96",       [18750, 96])
                 , ("runs-256",      [7031, 256])
                 , ("runs-512",      [3515, 512])
                 , ("runs-1024",     [1757, 1024])
                 , ("runs-4096",     [439, 4096])
                 , ("runs-16384",    [109, 16384])
                 , ("runs-65536",    [27, 65536])
                 , ("runs-r3-48x30", [1250, 48, 30]) ] ]
  ++ [ (n, mkFlip rs s)
     | (n, rs, s) <- [ ("flip-whole-square", [0, 1], [1341, 1341])
                     , ("flip-last-c32",     [4],    [24, 24, 32, 3, 3])
                     , ("flip-last-rows",    [1],    [18750, 96]) ] ]
  ++ [ (n, mkFlipIn rs s e)
     | (n, rs, s, e) <- [ ("flip-inner-gap64", [1], [2048, 64], [2048, 128])
                        , ("flip-outer-gap64", [0], [2048, 64], [2048, 128]) ] ]
  ++ [ (n, mkBlock s e o)
     | (n, s, e, o) <- [ ("block-run64-gap1",  [2048, 64],   [2048, 65],   0)
                       , ("block-run64-gap64", [2048, 64],   [2048, 128],  0)
                       , ("block-run64-page",  [2048, 64],   [2048, 512],  0)
                       , ("block-run64-off7",  [2048, 64],   [2048, 128],  7)
                       , ("block-r3-vol64",    [64, 64, 64], [72, 72, 72], 0) ] ]
  ++ [ (n, mkCompose s ts 0)
     | (n, s, ts) <- [ ("small-row96",    [4, 96],    [97, 1])
                     , ("small-patch-k5", [6, 5, 5],  [25, 1, 5])
                     , ("small-bcast32",  [8, 32],    [1, 0])
                     , ("small-flat64",   [4, 1, 64], [64, 0, 1])
                     , ("small-patch-r5", [2, 2, 4, 4, 4], [20, 4, 1, 20, 4]) ] ]
  ++ [ (n, mkCompose s ts o)
     | (n, s, ts, o) <- [ ("compose-rev-bcast",   [64, 100, 8],   [-100, -1, 0], 6399)
                        , ("compose-slice-bcast", [64, 100, 8],   [100, 1, 0],   7)
                        , ("compose-zero-mid",    [200, 90, 100], [0, 1, 0],     0)
                        , ("compose-scalar",      [1200, 1500],   [0, 0],        0)
                        , ("compose-bcast-nest",  [25, 25, 48, 10, 6], [39233, -1268, 17, 1, 0], 30432)
                        , ("compose-bcast-wide",  [4, 5, 5, 5, 5, 6, 120], [7564, -1466, 287, 55, 10, 1, 0], 5864) ] ]
