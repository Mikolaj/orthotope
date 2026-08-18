-- Goal-3 driver for pinned-churn-plan.txt section 3: the mixed workload --
-- single iterations of list, bq-expand and mut-odo-vecdims in equal
-- proportion, uniformly random order (seeded), across all 24 main shapes
-- -- and the user-code workaround toggles measured against it.  Untracked,
-- beside the plan.  Built by goal3/build.sh (a tiny cabal package;
-- base + vector only, like micro).
--
-- PROVENANCE: mkStrided, the shape list, toListT, baseOffsetsExpand and
-- the three arm bodies are copied from ../Main.hs (micro, run15 state);
-- mut-odo-vecdims is a CANDIDATE arm there, not library code; list and
-- bq-expand replicate the released and the shipped orthotope
-- toVectorListT paths.  One deliberate deviation, uniform across arms:
-- each result is filled through VSM.unsafeNew + a hand loop and returned
-- through VS.unsafeTake, instead of VS.fromListN / VS.generate, so that
-- the pad variant differs from base by the ALLOCATION LENGTH alone.
-- The toy run checks per-arm rates against micro's known figures.
--
-- Usage: MixedLoad SEED NROUNDS VARIANT [prepoison] [rep:K | nosmall]
--   VARIANT   = base | pad | unpin | strong | strongpad
--   prepoison = spray 1.15M pinned 2304 B buffers first (ReproSmall's
--               dose), so the run starts in the saturated state.
--   prepoisonbig = the same count of 3600 B buffers (own block group
--               each, ReproSmall's poisonbig / work item 27601's class)
--               -- the upfront-dose class control for plan section 6.3.
--   rep:K     = the REPETITIVE training-loop schedule (plan section 6.1)
--               in place of the shuffle: each round is K calls of
--               cnn-slice-c32/mut-odo-vecdims (the cheapest sub-threshold
--               sprayer, ~1.8 us and one 2304 B pinned result per call)
--               followed by one vgg-14-c512-k3/list and one
--               stretch-inner256/list -- a spray phase then a list phase,
--               identical every round.  Dose rate = K sprays per round.
--   rep1:K    = rep:K with the single victim vgg-14-c512-k3/list -- the
--               victim-alternation-free control (one homogeneous heavy
--               phase, the ReproSmall shape).
--   switch:R  = with rep1:K -- rounds before R run the schedule as
--               given, rounds from R on drop the sprayer calls (rep1:0):
--               the persistence cell -- does the interleaving-built
--               state outlive the interleaving?
--   noalloc   = with rep:K/rep1:K -- replace the sprayer call by a
--               non-allocating read of an equal-sized source (sum of
--               288 doubles, no result vector): does the foreign call
--               need to allocate to build the state?
--   nosmall   = the shuffle over the 66 calls of the 22 shapes whose
--               results are own-group, i.e. the two sub-threshold shapes
--               excluded (plan section 6.3's discriminator).
-- One round is the reporting window; in shuffle mode it is the 72
-- (shape, arm) pairs freshly shuffled (~100 calls).  Steady state =
-- the last 20% of rounds.
{-# LANGUAGE BangPatterns #-}
-- Criterion's own defense, for the same reason its Benchmarkable
-- internals carry it: without it, full laziness may float `f sh t` out of
-- apVS's state lambda and every call after the first reuses the forced
-- result instead of recomputing.  The toy run's per-round table is the
-- check: sharing would make every round after the first ~1000x faster.
{-# OPTIONS_GHC -fno-full-laziness #-}
module Main (main) where

import           Control.Monad                (when)
import           Control.Monad.ST             (runST)
import           Data.Bits                    (shiftL, shiftR, xor)
import           Data.List                    (foldl')
import qualified Data.Vector                  as V
import qualified Data.Vector.Storable         as VS
import qualified Data.Vector.Storable.Mutable as VSM
import qualified Data.Vector.Unboxed          as VU
import qualified Data.Vector.Unboxed.Mutable  as VUM
import           Data.Word                    (Word64)
import           Foreign.ForeignPtr           (mallocForeignPtrBytes,
                                               withForeignPtr)
import           Foreign.Storable             (peekElemOff, pokeElemOff)
import           GHC.Clock                    (getMonotonicTime)
import           GHC.Exts                     (build)
import           GHC.RTS.Flags                (GCFlags (largeAllocLim, minAllocAreaSize),
                                               getGCFlags)
import           GHC.Stats                    (GCDetails (..), RTSStats (..),
                                               getRTSStats)
import           System.Environment           (getArgs)
import           System.Exit                  (die)
import           System.Mem                   (performGC)

type ShapeL = [Int]
newtype Strides = Strides [Int]
data T = T !Strides !Int !(VS.Vector Double)  -- strides, offset, values

getStridesT :: ShapeL -> [Int]
getStridesT = scanr (*) 1

indexT :: T -> Int -> T
indexT (T (Strides (s : ss)) o v) i = T (Strides ss) (o + i * s) v
indexT _ _                          = error "indexT"

unScalarT :: T -> Double
unScalarT (T _ o v) = v VS.! o

-- Copied from ../Main.hs: exactly orthotope's toListT (the otherwise
-- branch; these inputs are never canonical).
toListT :: ShapeL -> T -> [Double]
toListT sh (T (Strides ss0) o0 v) = build $ \cons nil ->
  let go []     ss o rest = cons (unScalarT (T (Strides ss) o v)) rest
      go (n:ns) ss o rest = foldr
        (\i -> case indexT (T (Strides ss) o v) i of
                 T (Strides ss') o' _ -> go ns ss' o')
        rest
        [0..n-1]
  in  go sh ss0 o0 nil

-- Copied from ../Main.hs: the shipped fix's base-offsets table build.
{-# INLINE baseOffsetsExpand #-}
baseOffsetsExpand :: Int -> ShapeL -> Strides -> VU.Vector Int
baseOffsetsExpand o0 osh (Strides oats) =
  foldl' expand (VU.singleton o0) (zip osh oats)
  where expand !acc (!nd, !sd) =
          VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

-- Copied from ../Main.hs.
swapLast2 :: [a] -> [a]
swapLast2 xs = case reverse xs of
  (a:b:rest) -> reverse (b:a:rest); _ -> xs

mkStrided :: ShapeL -> (ShapeL, T)
mkStrided normalSh =
  let l = product normalSh
      v = VS.enumFromN (0 :: Double) l
      normalStrides = drop 1 (getStridesT normalSh)
      sh' = swapLast2 normalSh
      strides' = swapLast2 normalStrides
  in  (sh', T (Strides strides') 0 v)

-- Copied from ../Main.hs: the 24 main shapes, roster order.
shapes :: [(String, ShapeL)]
shapes =
  [ ("cnn-L1-6x6-c1",       [6, 6, 1, 3, 3])
  , ("cnn-L1-24x24-c1",     [24, 24, 1, 3, 3])
  , ("cnn-L2-24x24-c32",    [24, 24, 32, 3, 3])
  , ("cnn-slice-c32",       [32, 3, 3])
  , ("lenet-L1-28-c1-k5",   [28, 28, 1, 5, 5])
  , ("cifar-L2-16-c64-k3",  [16, 16, 64, 3, 3])
  , ("vgg-14-c512-k3",      [14, 14, 512, 3, 3])
  , ("alexnet-L1-55-c3-k11",[55, 55, 3, 11, 11])
  , ("alexnet-L2-27-c48-k5",[27, 27, 48, 5, 5])
  , ("gather48-src-50",     [50, 3, 3, 50])
  , ("conv1d-24",           [24, 3, 3, 24])
  , ("stretch-rank10",      [3,3,3,3,3,3,3,3,3,3])
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

-- 407 doubles = 3256 B payload is the last sub-threshold size; padding to
-- 410 clears the 3276 B limit with the 16 B header included.
padTo :: Int -> Int
padTo l = max l 410

-- The three arms, each parameterized by the result ALLOCATION length lp
-- (>= l; base passes l, pad passes padTo l) and returned as the first l
-- elements of that allocation.

-- list: the released fallback -- materialize the view through a boxed
-- cons list (../Main.hs fbList; fill loop in place of VS.fromListN).
{-# NOINLINE armList #-}
armList :: Int -> ShapeL -> T -> VS.Vector Double
armList !lp sh a = VS.unsafeTake l $ VS.create $ do
  out <- VSM.unsafeNew lp
  let fill !i (x:xs) | i < l = VSM.unsafeWrite out i x >> fill (i + 1) xs
      fill _ _ = pure ()
  fill 0 (toListT sh a)
  return out
  where l = product sh

-- bq-expand: the shipped fix -- base-offsets table + per-element quotRem
-- (../Main.hs fbBQexpand; fill loop in place of VS.generate).
{-# NOINLINE armBQ #-}
armBQ :: Int -> ShapeL -> T -> VS.Vector Double
armBQ !lp sh (T (Strides ats) ao v) = VS.unsafeTake l $ VS.create $ do
  out <- VSM.unsafeNew lp
  let fill !i | i >= l = pure ()
              | otherwise = do VSM.unsafeWrite out i (get i); fill (i + 1)
  fill 0
  return out
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

-- mut-odo-vecdims: the fastest candidate arm (../Main.hs fbMutOdoVecdims,
-- body verbatim but for VSM.unsafeNew lp / unsafeTake l).
{-# NOINLINE armMut #-}
armMut :: Int -> ShapeL -> T -> VS.Vector Double
armMut !lp sh (T (Strides ats) ao v) = VS.unsafeTake l $ VS.create $ do
  out <- VSM.unsafeNew lp
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

-- Unpinned (unboxed) result forms of the three arms, for the unpin
-- variant's sub-threshold shapes: same bodies, VUM in place of VSM.
{-# NOINLINE armListU #-}
armListU :: ShapeL -> T -> VU.Vector Double
armListU sh a = VU.create $ do
  out <- VUM.unsafeNew l
  let fill !i (x:xs) | i < l = VUM.unsafeWrite out i x >> fill (i + 1) xs
      fill _ _ = pure ()
  fill 0 (toListT sh a)
  return out
  where l = product sh

{-# NOINLINE armBQU #-}
armBQU :: ShapeL -> T -> VU.Vector Double
armBQU sh (T (Strides ats) ao v) = VU.create $ do
  out <- VUM.unsafeNew l
  let fill !i | i >= l = pure ()
              | otherwise = do VUM.unsafeWrite out i (get i); fill (i + 1)
  fill 0
  return out
  where l = product sh
        !s = last sh
        !t = last ats
        !baseOffsets = baseOffsetsExpand ao (init sh) (Strides (init ats))
        get i = case i `quotRem` s of
          (!q, !j) -> VS.unsafeIndex v (VU.unsafeIndex baseOffsets q + j * t)

{-# NOINLINE armMutU #-}
armMutU :: ShapeL -> T -> VU.Vector Double
armMutU sh (T (Strides ats) ao v) = VU.create $ do
  out <- VUM.unsafeNew l
  let writeRun !outPos !baseOff =
        let inner !j !src
              | j >= sInner = return ()
              | otherwise   = do
                  VUM.unsafeWrite out (outPos + j) (VS.unsafeIndex v src)
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

-- Strong form for list (Mikolaj, 2026-08-18): rebuild the WORKING
-- representation -- the bq-expand walk into an unboxed vector, then one
-- copy into Storable at the end.  bq-expand's times bound it from above;
-- the final copy is the one pinned allocation, padded in strongpad.
{-# NOINLINE armListStrong #-}
armListStrong :: Int -> ShapeL -> T -> VS.Vector Double
armListStrong !lp sh a = VS.unsafeTake l $ VS.create $ do
  out <- VSM.unsafeNew lp
  let !u = armBQU sh a
      fill !i | i >= l = pure ()
              | otherwise = do VSM.unsafeWrite out i (VU.unsafeIndex u i)
                               fill (i + 1)
  fill 0
  return out
  where l = product sh

-- The non-allocating stand-in for the sprayer (the noalloc mode): read
-- an equal-sized source end to end, allocate nothing, return the sum.
{-# NOINLINE noallocProbe #-}
noallocProbe :: VS.Vector Double -> IO Double
noallocProbe v = do
  let go !acc !i | i >= VS.length v = pure acc
                 | otherwise = go (acc + VS.unsafeIndex v i) (i + 1)
  go 0 0

-- The pre-poison spray, copied from ReproSmall.hs: 4000 * 288 ~ 1.15M
-- pinned 2304 B buffers, the saturating dose.
{-# NOINLINE fillSum #-}
fillSum :: Int -> Double -> IO Double
fillSum n x = do
  fp <- mallocForeignPtrBytes (n * 8)
  withForeignPtr fp $ \p -> do
    let fill !i | i >= n = pure ()
                | otherwise = pokeElemOff p i x >> fill (i + 1)
    fill 0
    let summ !acc !i | i >= n = pure acc
                     | otherwise = do v <- peekElemOff p i
                                      summ (acc + v) (i + 1)
    summ 0 0

prepoison :: Int -> IO ()  -- buffer length in doubles: 288 or 450
prepoison n = do
  t0 <- getMonotonicTime
  let go !acc !k
        | k >= (4000 :: Int) = pure acc
        | otherwise = do
            let inner !a !i | i >= (288 :: Int) = pure a
                            | otherwise = do
                                v <- fillSum n (fromIntegral (k + i))
                                inner (a + v) (i + 1)
            acc' <- inner acc 0
            go acc' (k + 1)
  s <- go 0 0
  t1 <- getMonotonicTime
  putStrLn ("prepoisoned (" ++ show n ++ " doubles) in " ++ show (t1 - t0)
            ++ " s (sink " ++ show (s > 0) ++ ")")

-- A small xorshift PRNG and a Fisher-Yates shuffle, so the driver needs
-- no extra dependency and the seed pins the whole order.
xorshift :: Word64 -> Word64
xorshift x0 =
  let x1 = x0 `xor` (x0 `shiftL` 13)
      x2 = x1 `xor` (x1 `shiftR` 7)
  in  x2 `xor` (x2 `shiftL` 17)

-- Shuffle [0 .. n-1]; returns the permutation and the advanced PRNG state.
shuffled :: Int -> Word64 -> (VU.Vector Int, Word64)
shuffled n g0 = runST $ do
  mv <- VU.thaw (VU.enumFromN 0 n)
  let go !i !g | i <= 0 = pure g
               | otherwise = do
                   let !g' = xorshift g
                       !j = fromIntegral (g' `mod` fromIntegral (i + 1))
                   VUM.swap mv i j
                   go (i - 1) g'
  g1 <- go (n - 1) g0
  v <- VU.unsafeFreeze mv
  pure (v, g1)

-- The per-call applicators, criterion's whnf pattern: NOINLINE, and the
-- arm application is built from the applicator's own arguments, so every
-- call constructs and forces a fresh result instead of sharing the first
-- one.  The sink reads two elements of the result, so the result is
-- forced and then dead -- short-lived, as in the benchmark.
{-# NOINLINE apVS #-}
apVS :: (ShapeL -> T -> VS.Vector Double) -> ShapeL -> T -> IO Double
apVS f sh t = do
  let v = f sh t
  pure $! VS.unsafeIndex v 0 + VS.unsafeIndex v (VS.length v - 1)

{-# NOINLINE apVU #-}
apVU :: (ShapeL -> T -> VU.Vector Double) -> ShapeL -> T -> IO Double
apVU f sh t = do
  let v = f sh t
  pure $! VU.unsafeIndex v 0 + VU.unsafeIndex v (VU.length v - 1)

-- One closure per (shape, arm) pair, input Ts built once and live for the
-- whole run (as criterion's env keeps a shape's setup vector live).
mkCalls :: String -> V.Vector (String, IO Double)
mkCalls variant = V.fromList
  [ (nm ++ "/" ++ anm, call)
  | (nm, normalSh) <- shapes
  , let (sh, t) = mkStrided normalSh
        l = product sh
        small = l <= 407
  , (anm, call) <- case variant of
      "base" ->
        [ ("list", apVS (armList l) sh t)
        , ("bq-expand", apVS (armBQ l) sh t)
        , ("mut-odo-vecdims", apVS (armMut l) sh t) ]
      "pad" ->
        [ ("list", apVS (armList (padTo l)) sh t)
        , ("bq-expand", apVS (armBQ (padTo l)) sh t)
        , ("mut-odo-vecdims", apVS (armMut (padTo l)) sh t) ]
      "unpin" | small ->
        [ ("list", apVU armListU sh t)
        , ("bq-expand", apVU armBQU sh t)
        , ("mut-odo-vecdims", apVU armMutU sh t) ]
      "unpin" ->
        [ ("list", apVS (armList l) sh t)
        , ("bq-expand", apVS (armBQ l) sh t)
        , ("mut-odo-vecdims", apVS (armMut l) sh t) ]
      "strong" ->
        [ ("list", apVS (armListStrong l) sh t)
        , ("bq-expand", apVS (armBQ l) sh t)
        , ("mut-odo-vecdims", apVS (armMut l) sh t) ]
      "strongpad" ->
        [ ("list", apVS (armListStrong (padTo l)) sh t)
        , ("bq-expand", apVS (armBQ (padTo l)) sh t)
        , ("mut-odo-vecdims", apVS (armMut (padTo l)) sh t) ]
      _ -> error ("unknown variant: " ++ variant)
  ]

main :: IO ()
main = do
  args <- getArgs
  (seed, nrounds, variant, opts) <- case args of
    (s : n : v : rest)
      | v `elem` ["base", "pad", "unpin", "strong", "strongpad"]
      , all (\o -> o == "prepoison" || o == "prepoisonbig" || o == "nosmall"
                   || o == "noalloc" || take 7 o == "switch:"
                   || take 4 o == "rep:" || take 5 o == "rep1:") rest
      -> pure (read s :: Word64, read n :: Int, v, rest)
    _ -> die "usage: MixedLoad SEED NROUNDS VARIANT [prepoison] [rep:K | rep1:K | nosmall]\n\
             \  VARIANT = base | pad | unpin | strong | strongpad"
  let doPre = "prepoison" `elem` opts
      doPreBig = "prepoisonbig" `elem` opts
      noSmall = "nosmall" `elem` opts
      repK = case [(read (drop 5 o) :: Int, True) | o <- opts, take 5 o == "rep1:"]
                  ++ [(read (drop 4 o), False) | o <- opts, take 4 o == "rep:"] of
               [kv] -> Just kv
               []   -> Nothing
               _    -> error "at most one rep:K / rep1:K"
      noAlloc = "noalloc" `elem` opts
      switchAt = case [read (drop 7 o) :: Int | o <- opts, take 7 o == "switch:"] of
                   [r] -> Just r
                   []  -> Nothing
                   _   -> error "at most one switch:R"
  gcf <- getGCFlags
  putStrLn ("MixedLoad seed=" ++ show seed ++ " rounds=" ++ show nrounds
            ++ " variant=" ++ variant ++ " prepoison=" ++ show doPre
            ++ (if doPreBig then " prepoisonbig" else "")
            ++ concat [" rep" ++ (if one then "1" else "") ++ ":" ++ show k
                      | Just (k, one) <- [repK]]
            ++ concat [" switch:" ++ show r | Just r <- [switchAt]]
            ++ (if noAlloc then " noalloc" else "")
            ++ (if noSmall then " nosmall" else "")
            ++ " minAllocAreaSize(blocks)=" ++ show (minAllocAreaSize gcf)
            ++ " largeAllocLim(blocks)=" ++ show (largeAllocLim gcf))
  let calls = mkCalls variant
      n = V.length calls
  when (n /= 72) $ die ("expected 72 calls, got " ++ show n)
  let idxOf nm = case V.findIndex ((== nm) . fst) calls of
        Just i  -> i
        Nothing -> error ("no call " ++ nm)
      -- The per-round index sequence: shuffle (default), the 66-call
      -- shuffle without the sub-threshold shapes, or the fixed
      -- repetitive schedule.  Each returns the advanced PRNG state.
      smallIdxs = [idxOf (nm ++ "/" ++ a)
                  | nm <- ["cnn-slice-c32", "cnn-L1-6x6-c1"]
                  , a <- ["list", "bq-expand", "mut-odo-vecdims"]]
      bigIdxs = VU.fromList [i | i <- [0 .. n - 1], i `notElem` smallIdxs]
      sprayIdx = if noAlloc then -1 else idxOf "cnn-slice-c32/mut-odo-vecdims"
      repSeq k one =
        VU.fromList (replicate k sprayIdx
                     ++ idxOf "vgg-14-c512-k3/list"
                        : [idxOf "stretch-inner256/list" | not one])
      mkPerm :: Int -> Word64 -> (VU.Vector Int, Word64)
      mkPerm r g = case repK of
        Just (k, one) ->
          let k' = case switchAt of Just sr | r >= sr -> 0; _ -> k
          in  (repSeq k' one, g)
        Nothing
          | noSmall -> let (p, g') = shuffled (VU.length bigIdxs) g
                       in  (VU.map (VU.unsafeIndex bigIdxs) p, g')
          | otherwise -> shuffled n g
      nasrc = VS.enumFromN (0 :: Double) 288
  -- Force every setup vector now, before any timing.
  setupSink <- V.foldM' (\ !acc (_, c) -> (acc +) <$> c) 0 calls
  when doPre (prepoison 288)
  when doPreBig (prepoison 450)
  performGC
  -- Per-call wall accumulator, reset at the steady tail's start so the
  -- printed per-call means are tail-only (the diagnosis of whether the
  -- mix itself runs its arms at their poisoned or their alone rates).
  perCall <- VUM.replicate n (0 :: Double)
  let tailStart = nrounds - max 1 (nrounds `div` 5)
  putStrLn "round  ms      allocGB  memInUseMB  blockFragMB"
  let runRound :: Word64 -> Int -> Double -> IO Double
      runRound !g !r !acc
        | r >= nrounds = pure acc
        | otherwise = do
            when (r == tailStart) $ VUM.set perCall 0
            let (perm, g') = mkPerm r g
                !m = VU.length perm
            t0 <- getMonotonicTime
            let go !i !a | i >= m = pure a
                         | otherwise = do
                             let !k = VU.unsafeIndex perm i
                             c0 <- getMonotonicTime
                             x <- if k < 0 then noallocProbe nasrc
                                  else snd (calls V.! k)
                             c1 <- getMonotonicTime
                             when (k >= 0) $
                               VUM.unsafeModify perCall (+ (c1 - c0)) k
                             go (i + 1) (a + x)
            acc' <- go 0 acc
            t1 <- getMonotonicTime
            st <- getRTSStats
            let d = gc st
            putStrLn (pad5 (show r) ++ "  "
                      ++ fmt ((t1 - t0) * 1000) ++ "  "
                      ++ fmt (fromIntegral (allocated_bytes st) / 1e9) ++ "  "
                      ++ fmt (fromIntegral (gcdetails_mem_in_use_bytes d)
                              / 1048576) ++ "  "
                      ++ fmt (fromIntegral
                                (gcdetails_block_fragmentation_bytes d)
                              / 1048576))
            runRound g' (r + 1) acc'
      pad5 s = s ++ replicate (5 - length s) ' '
      fmt :: Double -> String
      fmt x = let r = fromIntegral (round (x * 100) :: Integer) / 100
              in show (r :: Double)
  sink <- runRound seed 0 0
  -- Steady state: the last 20% of rounds is what the caller compares; the
  -- per-round table above is the evidence.  Recomputed by the reader, not
  -- here, so the table stays the single source.
  pc <- VU.unsafeFreeze perCall
  let tailN = nrounds - tailStart
  putStrLn ("per-call mean ms over the last " ++ show tailN ++ " rounds:")
  V.iforM_ calls $ \i (name, _) ->
    putStrLn ("  " ++ name ++ " " ++ show (VU.unsafeIndex pc i
                                           / fromIntegral tailN * 1000))
  putStrLn ("done; sink=" ++ show (setupSink + sink))

