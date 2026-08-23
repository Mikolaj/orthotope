{-# LANGUAGE BangPatterns #-}

-- | The element-type probe: does the regime-3 strategy ordering survive a
-- change of element type?
--
-- @Main.hs@ is all @Storable Double@, horde-ad's element storage, while the
-- fallback all of it justifies is polymorphic over the @Vector@ class AND the
-- element type. What the element changes is the COPY -- its width sets how
-- many elements a cache line holds, the instance sets what a write costs --
-- and what it leaves alone is the index arithmetic, which is the only thing
-- the strategies differ in. So the question is not whether the magnitudes
-- move (they must) but whether the ORDERING does, and whether bq-expand
-- stays under @list@ at every instance the library serves.
--
-- Four points, each varying one thing against @Storable Double@:
-- @Storable Float@ is the same instance at half the width, unboxed @Int@ the
-- same width in another instance, @Storable Word8@ the same instance at the
-- narrowest width there is. Boxed is deliberately absent, and not for cost:
-- its elements are thunks, so each arm would defer a different share of its
-- copy into the forcing sum, and the fill/forcing split every figure in
-- README.md rests on would not hold. Probing boxed needs a design of its own.
--
-- WHY THIS IS A SEPARATE PROGRAM, and what that costs.
--
-- It cannot live in @Main.hs@: these arms are in no roster, and a roster arm
-- is what @Main.hs@'s @check@ and @--lint@ are built around. It cannot import
-- @Main.hs@ either -- that module would have to import this one back for the
-- benchmark mode, which is a cycle, and a @main-is@ module is not importable
-- anyway. So this file is self-contained, and its shape helpers, its
-- base-offsets build and its six shapes are COPIES of @Main.hs@'s.
--
-- What the copying buys is that all four element types sit on equal footing:
-- were @Double@ served by @Main.hs@'s own @fb*@ arms and the other three by
-- copies, a difference between them could be an artifact of the copying
-- rather than an effect of the element. Here every type runs the same
-- transcribed code.
--
-- What it costs is drift, and the two halves of that are guarded differently.
-- The six shapes are checked: @read-run.py --lint@ compares the dims below
-- against @Main.hs@'s own lists and fails on a disagreement, so a shape
-- cannot quietly stop being the shape it names. The base-offsets build is
-- NOT checked, and deliberately: this file's @bq-expand@ is bq-expand-SHAPED
-- rather than @Main.hs@'s @bq-expand@, so its absolute figures are its own
-- and only the ordering across the four types is read off them. A figure
-- from here therefore never belongs beside one from a roster run.
--
-- MONOMORPHIC DUPLICATES, four times over, rather than one polymorphic set.
-- @NOINLINE@ on a polymorphic function times a dictionary rather than a fill,
-- so a polymorphic version would need a @SPECIALISE@ per type per arm, each
-- confirmed in Core -- an unverified one leaves the dictionary in place and
-- the program then measures dispatch while reporting it as a strategy, the
-- failure that looks most like a result. The four blocks below are one
-- template instantiated at four types and are to be kept character-identical
-- modulo the type, the vector module and the element: an edit to one is an
-- edit to all four.
--
-- Modes:
--
-- > cabal run probe -- check                 -- every arm against its own list
-- > cabal run probe -- f64  --json et-f64.json
-- > cabal run probe -- f32  --json et-f32.json
-- > cabal run probe -- intu --json et-intu.json
-- > cabal run probe -- w8   --json et-w8.json
--
-- One process per type, the bench names the same in each, so every JSON is an
-- ordinary run for @read-run.py@: the groups are main-set shape names, @list@
-- is there to divide by, and the four tables are then read against each
-- other. No @sum-only@ bench rides along, so the figures are uncorrected and
-- compressed toward 1 by the forcing pass; that costs the ordering question
-- nothing, and it cannot flip the under-1 property either, the correction
-- only moving a ratio further from 1.
module Main (main) where

import           Control.DeepSeq              (NFData (..), force)
import           Control.Exception            (evaluate)
import           Criterion.Main
import           Criterion.Types              (Config (regressions))
import           Data.List                    (foldl')
import qualified Data.Vector.Storable         as VS
import qualified Data.Vector.Storable.Mutable as VSM
import qualified Data.Vector.Unboxed          as VU
import qualified Data.Vector.Unboxed.Mutable  as VUM
import           Data.Word                    (Word8)
import           GHC.Exts                     (build)
import           System.Environment           (getArgs, withArgs)

type ShapeL = [Int]

-- The strides of a view, one per dimension; the wrapper is 'Main.hs''s and
-- is kept so a call cannot swap a shape for its strides.
newtype Strides = Strides [Int]

-- The six shapes, by the names they carry in 'Main.hs''s @convShapes@ and
-- @stretchShapes@, spanning what decides the orderings there -- @sInner@ from
-- 1 to half the length, @l@ from hundreds to the cap. Both shapes README
-- singles out are here: @stretch-inner1@ for its unit innermost extent, and
-- @stretch-tall-Mx2@ for inverting the ordering the rest of the set shows.
--
-- These dims are a COPY of that file's; @read-run.py --lint@ compares them
-- and fails on a disagreement, which is what keeps the copy honest.
probeShapes :: [(String, ShapeL)]
probeShapes =
  [ ("cnn-slice-c32",      [32, 3, 3])          -- 288
  , ("stretch-rank12",     [2,2,2,2,2,2,2,2,2,2,2,2])  -- 4096
  , ("lenet-L1-28-c1-k5",  [28, 28, 1, 5, 5])   -- 19600
  , ("cifar-L2-16-c64-k3", [16, 16, 64, 3, 3])  -- 147456
  , ("stretch-inner1",     [1, 500000])         -- 500000
  , ("stretch-tall-Mx2",   [900000, 2])         -- 1800000
  ]

-- The natural strides of a dense shape, total size first; every caller
-- splits it.
getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

swapLast2 :: [a] -> [a]
swapLast2 xs = case reverse xs of
  (a:b:rest) -> reverse (b:a:rest); _ -> xs

-- 'Main.hs''s @mkStrided@ view without its payload -- the two innermost dims
-- transposed, so the innermost stride is the original innermost dim size --
-- so that each element type can lay its own vector under the same shape,
-- strides and length.
stridedViewOf :: ShapeL -> (ShapeL, Strides, Int)
stridedViewOf normalSh =
  ( swapLast2 normalSh
  , Strides (swapLast2 (drop 1 (getStridesT normalSh)))
  , product normalSh )

-- The run base-offsets by iterated expansion, in an unboxed Int vector: the
-- flavour @Data/Array/Internal.hs@ ships and, since that was measured, the
-- flavour every table in @Main.hs@ uses too. Transcribed from
-- @baseOffsetsExpand@ there, and bq-expand-shaped rather than that build
-- itself -- see the header on what that means for these figures.
{-# INLINE baseOffsets #-}
baseOffsets :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsets o0 osh (Strides oats) =
  foldl' expand (VU.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- Storable Double: horde-ad's element storage, and the baseline the other
-- three are read against.

data TDbl = TDbl !Strides !Int !(VS.Vector Double)

instance NFData TDbl where
  rnf (TDbl (Strides s) o v) = rnf s `seq` rnf o `seq` rnf v

mkStridedDbl :: ShapeL -> (ShapeL, TDbl)
mkStridedDbl normalSh = (sh, TDbl sts 0 (VS.enumFromN 0 l))
  where (sh, sts, l) = stridedViewOf normalSh

indexTDbl :: TDbl -> Int -> TDbl
indexTDbl (TDbl (Strides (s : ss)) o v) i = TDbl (Strides ss) (o + i * s) v
indexTDbl _ _                             = error "indexTDbl"

unScalarTDbl :: TDbl -> Double
unScalarTDbl (TDbl _ o v) = v VS.! o

toListTDbl :: ShapeL -> TDbl -> [Double]
toListTDbl sh (TDbl (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarTDbl (TDbl (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexTDbl (TDbl (Strides ss) o v) i of
                 TDbl (Strides ss') o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

{-# NOINLINE listDbl #-}
listDbl :: ShapeL -> TDbl -> VS.Vector Double
listDbl sh a = VS.fromListN l (toListTDbl sh a) where l = product sh

{-# NOINLINE expandDbl #-}
expandDbl :: ShapeL -> TDbl -> VS.Vector Double
expandDbl sh (TDbl (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !bo = baseOffsets ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex bo q + j * t)

{-# NOINLINE odoDbl #-}
odoDbl :: ShapeL -> TDbl -> VS.Vector Double
odoDbl sh (TDbl (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- Storable Float: the same instance at half the width.

data TF32 = TF32 !Strides !Int !(VS.Vector Float)

instance NFData TF32 where
  rnf (TF32 (Strides s) o v) = rnf s `seq` rnf o `seq` rnf v

mkStridedF32 :: ShapeL -> (ShapeL, TF32)
mkStridedF32 normalSh = (sh, TF32 sts 0 (VS.enumFromN 0 l))
  where (sh, sts, l) = stridedViewOf normalSh

indexTF32 :: TF32 -> Int -> TF32
indexTF32 (TF32 (Strides (s : ss)) o v) i = TF32 (Strides ss) (o + i * s) v
indexTF32 _ _                             = error "indexTF32"

unScalarTF32 :: TF32 -> Float
unScalarTF32 (TF32 _ o v) = v VS.! o

toListTF32 :: ShapeL -> TF32 -> [Float]
toListTF32 sh (TF32 (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarTF32 (TF32 (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexTF32 (TF32 (Strides ss) o v) i of
                 TF32 (Strides ss') o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

{-# NOINLINE listF32 #-}
listF32 :: ShapeL -> TF32 -> VS.Vector Float
listF32 sh a = VS.fromListN l (toListTF32 sh a) where l = product sh

{-# NOINLINE expandF32 #-}
expandF32 :: ShapeL -> TF32 -> VS.Vector Float
expandF32 sh (TF32 (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !bo = baseOffsets ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex bo q + j * t)

{-# NOINLINE odoF32 #-}
odoF32 :: ShapeL -> TF32 -> VS.Vector Float
odoF32 sh (TF32 (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- Unboxed Int: the same width in a different instance.

data TIntU = TIntU !Strides !Int !(VU.Vector Int)

instance NFData TIntU where
  rnf (TIntU (Strides s) o v) = rnf s `seq` rnf o `seq` rnf v

mkStridedIntU :: ShapeL -> (ShapeL, TIntU)
mkStridedIntU normalSh = (sh, TIntU sts 0 (VU.enumFromN 0 l))
  where (sh, sts, l) = stridedViewOf normalSh

indexTIntU :: TIntU -> Int -> TIntU
indexTIntU (TIntU (Strides (s : ss)) o v) i = TIntU (Strides ss) (o + i * s) v
indexTIntU _ _                              = error "indexTIntU"

unScalarTIntU :: TIntU -> Int
unScalarTIntU (TIntU _ o v) = v VU.! o

toListTIntU :: ShapeL -> TIntU -> [Int]
toListTIntU sh (TIntU (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarTIntU (TIntU (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexTIntU (TIntU (Strides ss) o v) i of
                 TIntU (Strides ss') o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

{-# NOINLINE listIntU #-}
listIntU :: ShapeL -> TIntU -> VU.Vector Int
listIntU sh a = VU.fromListN l (toListTIntU sh a) where l = product sh

{-# NOINLINE expandIntU #-}
expandIntU :: ShapeL -> TIntU -> VU.Vector Int
expandIntU sh (TIntU (Strides ats) ao v) = VU.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !bo = baseOffsets ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VU.unsafeIndex v (VU.unsafeIndex bo q + j * t)

{-# NOINLINE odoIntU #-}
odoIntU :: ShapeL -> TIntU -> VU.Vector Int
odoIntU sh (TIntU (Strides ats) ao v) = VU.create $ do
  out <- VUM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VUM.unsafeWrite out (outPos + j) (VU.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- Storable Word8: the same instance at the narrowest width there is, so a
-- cache line holds eight times what it holds of Double. If element width can
-- move the ordering at all, this is where it shows. The payload wraps mod 256
-- as 'enumFromN' fills it and again as the arms sum it, which costs the probe
-- nothing: every arm wraps identically, and @check@ holds each to its own
-- type's @list@ on the same wrapped values.

data TW8 = TW8 !Strides !Int !(VS.Vector Word8)

instance NFData TW8 where
  rnf (TW8 (Strides s) o v) = rnf s `seq` rnf o `seq` rnf v

mkStridedW8 :: ShapeL -> (ShapeL, TW8)
mkStridedW8 normalSh = (sh, TW8 sts 0 (VS.enumFromN 0 l))
  where (sh, sts, l) = stridedViewOf normalSh

indexTW8 :: TW8 -> Int -> TW8
indexTW8 (TW8 (Strides (s : ss)) o v) i = TW8 (Strides ss) (o + i * s) v
indexTW8 _ _                            = error "indexTW8"

unScalarTW8 :: TW8 -> Word8
unScalarTW8 (TW8 _ o v) = v VS.! o

toListTW8 :: ShapeL -> TW8 -> [Word8]
toListTW8 sh (TW8 (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarTW8 (TW8 (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexTW8 (TW8 (Strides ss) o v) i of
                 TW8 (Strides ss') o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

{-# NOINLINE listW8 #-}
listW8 :: ShapeL -> TW8 -> VS.Vector Word8
listW8 sh a = VS.fromListN l (toListTW8 sh a) where l = product sh

{-# NOINLINE expandW8 #-}
expandW8 :: ShapeL -> TW8 -> VS.Vector Word8
expandW8 sh (TW8 (Strides ats) ao v) = VS.generate l get
  where l = product sh
        !s = last sh
        !t = last ats
        !bo = baseOffsets ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex bo q + j * t)

{-# NOINLINE odoW8 #-}
odoW8 :: ShapeL -> TW8 -> VS.Vector Word8
odoW8 sh (TW8 (Strides ats) ao v) = VS.create $ do
  out <- VSM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VSM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
                  inner (j + 1) (src + tInner)
        in  inner 0 baseOff
      go !lev !outPos !baseOff
        | lev >= rOuter = writeRun outPos baseOff >> return (outPos + sInner)
        | otherwise =
            let !n  = VU.unsafeIndex oshV lev
                !st = VU.unsafeIndex oatsV lev
                dim !i !op
                  | i >= n    = return op
                  | otherwise = go (lev + 1) op (baseOff + i * st)
                                >>= dim (i + 1)
            in  dim 0 outPos
  _ <- go 0 0 ao
  return out
  where l = product sh
        !sInner = last sh
        !tInner = last ats
        !rOuter = length sh - 1
        oshV, oatsV :: VU.Vector Int
        !oshV  = VU.fromList (init sh)
        !oatsV = VU.fromList (init ats)

-- One group per shape, three benches in it, named the same at every type.
benchesFor :: String -> [Benchmark]
benchesFor ty = map one probeShapes
  where
    one (name, normalSh) = case ty of
      "f64"  -> env (evaluate (force (mkStridedDbl normalSh))) $ \ ~(sh, a) ->
        bgroup name
          [ bench "list"            $ whnf (VS.sum . listDbl sh) a
          , bench "bq-expand"       $ whnf (VS.sum . expandDbl sh) a
          , bench "mut-odo-vecdims" $ whnf (VS.sum . odoDbl sh) a ]
      "f32"  -> env (evaluate (force (mkStridedF32 normalSh))) $ \ ~(sh, a) ->
        bgroup name
          [ bench "list"            $ whnf (VS.sum . listF32 sh) a
          , bench "bq-expand"       $ whnf (VS.sum . expandF32 sh) a
          , bench "mut-odo-vecdims" $ whnf (VS.sum . odoF32 sh) a ]
      "intu" -> env (evaluate (force (mkStridedIntU normalSh))) $ \ ~(sh, a) ->
        bgroup name
          [ bench "list"            $ whnf (VU.sum . listIntU sh) a
          , bench "bq-expand"       $ whnf (VU.sum . expandIntU sh) a
          , bench "mut-odo-vecdims" $ whnf (VU.sum . odoIntU sh) a ]
      "w8"   -> env (evaluate (force (mkStridedW8 normalSh))) $ \ ~(sh, a) ->
        bgroup name
          [ bench "list"            $ whnf (VS.sum . listW8 sh) a
          , bench "bq-expand"       $ whnf (VS.sum . expandW8 sh) a
          , bench "mut-odo-vecdims" $ whnf (VS.sum . odoW8 sh) a ]
      _      -> error ("probe: want f64, f32, intu or w8, not " ++ ty)

-- Every arm against its own type's @list@, on every probe shape. Separate
-- from the benchmark mode so the timed program never computes it and thus
-- cannot share a result between the two through CSE -- the same separation
-- @Main.hs@ keeps between its @check@ and its run.
--
-- Non-vacuity: dropping the @+ j * t@ term from 'expandW8' turns the w8
-- verdict False on every shape while the other three stay True, which is
-- also what tells the four duplicates apart.
check :: IO ()
check = mapM_ one probeShapes
  where
    one (name, normalSh) = do
      let (shD, aD) = mkStridedDbl normalSh
          (shF, aF) = mkStridedF32 normalSh
          (shI, aI) = mkStridedIntU normalSh
          (shW, aW) = mkStridedW8 normalSh
          okD = expandDbl shD aD == rD && odoDbl shD aD == rD
          okF = expandF32 shF aF == rF && odoF32 shF aF == rF
          okI = expandIntU shI aI == rI && odoIntU shI aI == rI
          okW = expandW8 shW aW == rW && odoW8 shW aW == rW
          rD = listDbl shD aD
          rF = listF32 shF aF
          rI = listIntU shI aI
          rW = listW8 shW aW
      putStrLn $ name ++ ": f64 agree=" ++ show okD
                 ++ ", f32 agree=" ++ show okF
                 ++ ", intu agree=" ++ show okI
                 ++ ", w8 agree=" ++ show okW

-- The type to run is the first argument, the rest go to criterion, so a JSON
-- comes out of the same invocation. The allocation fit is on by default, as
-- in @Main.hs@, so @alloc@ comes from the same process as the times.
main :: IO ()
main = do
  args <- getArgs
  case args of
    "check" : _ -> check
    ty : rest   -> withArgs rest $ defaultMainWith cfg (benchesFor ty)
    []          -> error "probe: name a type -- check, f64, f32, intu or w8"
  where cfg = defaultConfig { regressions = [(["iters"], "allocated")] }
