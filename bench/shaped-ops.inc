-- Every operation of a Shaped module, included by OpsShaped once a vector kind
-- and a size with ARR the module of the kind, OPS its list on a view, SH the
-- shape, ROWS its rows, SIZE the size's other values, IARR the kind's internal
-- module, CONV the module of the kind convert converts to, BOXED or STORABLE
-- defined at those kinds, CD and CR the kind's Dynamic and Ranked modules,
-- and SHT, FLAT, ROW1, SL, CAT, NN, SHR, SLR, SHW, SH3, SH5, SHB, SHO, WINO,
-- COL1, EMP, SLNR, TW1 to TW6 and TWN the type arguments of the size. After an
-- operation's call come those of the arms it leaves untaken, each named for
-- its operation and its arm; at ROWS 0 only the calls an empty array takes, on
-- every view but the window, whose type has no array of no rows.
OPS :: View -> [Call]
OPS view =
  [ call "size" ARR.size t
  , call "shapeL" ARR.shapeL t
  , call "rank" ARR.rank t
  , call "toList" (sum . ARR.toList) t
  , call "fromList" (ARR.fromList @SH) (take (ROWS * cols) elemsFrom)
  , call "toVector" ARR.toVector t
  , call "toUnorderedVectorT"
         (\ (IARR.A a@(SG.A u)) -> I.toUnorderedVectorT (SG.shapeL a) u) t
  , call "toUnorderedVectorListT"
         (\ (IARR.A a@(SG.A u)) -> I.toUnorderedVectorListT (SG.shapeL a) u) t
  , call "fromVector" (ARR.fromVector @SH) (ARR.toVector d)
  , call "normalize" ARR.normalize t
  , call "force" ARR.force t
  , call "force.rank5" ARR.force tx
  , call "force.narrow" ARR.force tnr
#if ROWS > 0
  , call "force.window" (ARR.force . ARR.window @Win) t
#endif
  , call "scalar" ARR.scalar x0
  , call "unScalar" ARR.unScalar (ARR.scalar x0)
  , call "constant" (ARR.constant @SH) x0
  , call "reshape" (ARR.reshape @FLAT) t
#if ROWS > 0
  , call "reshape.scalar" (ARR.reshape @Sh0) t11
#endif
#if ROWS > 0
  , call "stretch" (ARR.stretch @SH) r1
  , call "stretchOuter" (\ a -> ARR.stretchOuter a `asTypeOf` t) r1
#endif
  , call "transpose" (ARR.transpose @Perm) t
#if ROWS > 0
  , call "index" (`ARR.index` irow) t
#endif
  -- Every element read through two indexes, the row index i varying
  -- fastest so that each element takes its own row: with j fastest, one
  -- row served a whole row of elements.
  -- GHC.Exts.lazy on the array in ShapedG's index, putting index's check
  -- before the array is forced, stops GHC simplifying through it: tried
  -- 2026-10-11 on GHC HEAD 10.1.20260918, this row then allocated 32 bytes
  -- an element and took 1.2 to 1.5 times as long with index INLINE, and 64
  -- bytes and 2.2 to 3.3 times as long with index INLINABLE, Dynamic's row
  -- unmoved.
  , call "indexIndex"
         (\ a -> sum [ ARR.unScalar (ARR.index (ARR.index a i) j)
                     | j <- [0 .. cols - 1], i <- [0 .. ROWS - 1] ]) t
  , call "pad" (ARR.pad @Pads 0) t
  , call "pad.none" (\ a -> ARR.pad @Pads0 0 a `asTypeOf` t) t
  , call "pad.outer" (ARR.pad @Pads1 0) t
  , call "mapA" (ARR.mapA (+ 1)) t
  , call "zipWithA" (uncurry (ARR.zipWithA (+))) (t, tn)
  , call "zipWithA.singleR" (\ a -> ARR.zipWithA (+) a c) t
  , call "zipWith3A" (\ (a, b) -> ARR.zipWith3A (\ x y z -> x + y + z) a b a)
                     (t, tn)
  , call "zipWith3A.singleR"
         (\ a -> ARR.zipWith3A (\ x y z -> x + y + z) a c c) t
  , call "zipWith4A" (\ (a, b) -> ARR.zipWith4A (\ x y z u -> x + y + z + u)
                                               a b a b) (t, tn)
  , call "zipWith5A" (\ (a, b) -> ARR.zipWith5A
                                   (\ x y z u w -> x + y + z + u + w)
                                   a b a b a) (t, tn)
  , call "append" (uncurry ARR.append) (t, tn)
#if ROWS > 0
  , call "append.emptyL" (ARR.append e) t
  , call "append.emptyR" (\ a -> ARR.append a e) t
#endif
  , call "concatOuter" (\ (a, b) -> ARR.concatOuter @CAT [a, b]) (t, tn)
  , call "concatOuter.one" (\ a -> ARR.concatOuter @ROWS [a]) t
  , call "ravel" ARR.ravel (ARR.unravel t)
#if ROWS > 0
  , call "ravel.one" ARR.ravel (ARR.unravel t1)
#endif
  , call "unravel" ARR.unravel t
#if ROWS > 0
  , call "window" (ARR.window @Win) t
#endif
  , call "stride" (ARR.stride @Str22) t
  , call "stride.outer" (ARR.stride @Str1) t
  , call "rotate" (ARR.rotate @0 @2) t
  , call "rotate.one" (ARR.rotate @1 @1) t
#if ROWS > 0
  , call "slice" (ARR.slice @SL) t
#endif
  , call "rerank" (ARR.rerank @1
                     (\ r -> ARR.scalar (ARR.sumA (r `asTypeOf` row))))
                t
  , call "rerank2" (\ (a, b) -> ARR.rerank2 @1
                           (\ x y -> ARR.zipWithA (+) (x `asTypeOf` row) y) a b)
                 (t, tn)
#if ROWS > 0
  , call "rerank2.one" (\ a -> ARR.rerank2 @1
                               (\ x y -> ARR.zipWithA (+) (x `asTypeOf` row) y)
                               a a)
                     t1
#endif
  , call "rev" (ARR.rev @Rev01) t
  , call "reduce" (ARR.reduce (+) 0) t
  , call "foldrA" (ARR.foldrA (+) 0) t
  , call "traverseA" (runIdentity . ARR.traverseA (Identity . (+ 1))) t
  , call "allSameA" ARR.allSameA same
#if ROWS > 0
  , call "allSameA.tiers" ARR.allSameA tw
#endif
  , call "sumA" ARR.sumA t
  , call "productA" ARR.productA t
#if ROWS > 0
  , call "maximumA" ARR.maximumA t
  , call "maximumA.one" ARR.maximumA t11
  , call "maximumA.rank5" ARR.maximumA tx
  , call "minimumA" ARR.minimumA t
#endif
  , call "anyA" (ARR.anyA (> 2)) t
  , call "allA" (ARR.allA (< 2)) t
  , call "broadcast" (ARR.broadcast @Bc123 @SHB) t3
#if ROWS > 0
  , call "update" (`ARR.update` [(ielem, 9)]) t
#endif
  , call "update.none" (`ARR.update` []) t
  -- A pair per perPair elements built in each call, the list depending on its
  -- array so that it is not floated out of the loop.
  , call "update2000"
         (\ a -> ARR.update a [ ([i `quot` cols, i `rem` cols], fromIntegral i)
                              | i <- [0 .. ARR.size a `quot` perPair - 1] ]) t
  , call "generate" (\ k -> ARR.generate (\ ix -> fromIntegral (sum ix + k))
                          `asTypeOf` t)
                  0
  , call "iterateN" (ARR.iterateN @NN (+ 1)) x0
  , call "iota" iota (ROWS * cols :: Int)
#ifdef WITH_BITCAST
  , call "bitcast" (ARR.bitcast :: ARR.Array SH Double -> ARR.Array SH Int64) t
#endif
  , call "convert" (convert :: ARR.Array SH Double -> CONV.Array SH Double) t
  , call "convertE"
         (convertE :: ARR.Array SH Double
                   -> Either String (CONV.Array SH Double)) t
  , call "convert.rank5"
         (convert :: ARR.Array SH5 Double -> CONV.Array SH5 Double) tx
#if defined(BOXED) || defined(STORABLE)
  , call "convert.dynamic" (convert :: ARR.Array SH Double -> CD.Array Double) t
#endif
#ifdef BOXED
  , call "convert.ranked"
         (convert :: ARR.Array SH Double -> CR.Array 2 Double) t
#endif
#ifdef BOXED
  , call "convert.unboxed"
         (convert :: ARR.Array SH Double -> U.Array SH Double) t
  , call "convertE.unboxed"
         (convertE :: ARR.Array SH Double
                   -> Either String (U.Array SH Double)) t
#endif
#if defined(BOXED) || defined(STORABLE)
  , call "convertE.dynamic"
         (convertE :: ARR.Array SH Double -> Either String (CD.Array Double)) t
#endif
#ifdef BOXED
  , call "convertE.ranked"
         (convertE :: ARR.Array SH Double
                   -> Either String (CR.Array 2 Double)) t
#endif
  , call "convert.g" (\ a -> convert a `asTypeOf` IARR.unA a) t
  , call "convertE.g" (\ a -> convertE a `asTypeOf` Right (IARR.unA a)) t
  , call "==" (\ (a, b) -> (a == b, b == a)) (t, tn)
#if ROWS > 0
  , call "==.rank1" (uncurry (==)) (row, rown)
#endif
  , call "==.rank3" (uncurry (==)) (t3, t3n)
  , call "==.rank5" (uncurry (==)) (tx, txn)
#if ROWS > 0
  , call "==.units" (uncurry (==)) (t1, r1)
#endif
  , call "/=" (\ (a, b) -> (a /= b, b /= a)) (t, tn)
  , call "/=.g" (\ (a, b) -> (a /= b, b /= a)) (IARR.unA t, IARR.unA tn)
  , call "compare" (\ (a, b) -> (compare a b, compare b a)) (t, tn)
#if ROWS > 0
  , call "<" (\ (a, b) -> (a < b, b < a)) (t, tu)
  , call "<.g" (\ (a, b) -> (a < b, b < a)) (IARR.unA t, IARR.unA tu)
  , call "<=" (\ (a, b) -> (a <= b, b <= a)) (t, tu)
  , call "<=.g" (\ (a, b) -> (a <= b, b <= a)) (IARR.unA t, IARR.unA tu)
  , call ">" (\ (a, b) -> (a > b, b > a)) (t, tu)
  , call ">.g" (\ (a, b) -> (a > b, b > a)) (IARR.unA t, IARR.unA tu)
  , call ">=" (\ (a, b) -> (a >= b, b >= a)) (t, tu)
  , call ">=.g" (\ (a, b) -> (a >= b, b >= a)) (IARR.unA t, IARR.unA tu)
  , call "max" (\ (a, b) -> (max a b, max b a)) (t, tu)
  , call "max.g" (\ (a, b) -> (max a b, max b a)) (IARR.unA t, IARR.unA tu)
  , call "min" (\ (a, b) -> (min a b, min b a)) (t, tu)
  , call "min.g" (\ (a, b) -> (min a b, min b a)) (IARR.unA t, IARR.unA tu)
#endif
  , call "rnf" id t
#ifdef BOXED
  , call "fmap" (fmap (+ 1)) t
  , call "<$" (x0 <$) t
  , call "fold" fold (fmap Sum t)
  , call "foldr" (foldr (+) 0) t
  , call "traverse" (runIdentity . traverse (Identity . (+ 1))) t
  , call "sequenceA" (runIdentity . sequenceA) (fmap Identity t)
  , call "pure" (\ x -> pure x `asTypeOf` t) x0
  , call "<*>" (pure (+ 1) <*>) t
  , call "liftA2" (uncurry (A.liftA2 (+))) (t, t)
#endif
  ]
 where
  Size {..} = SIZE
  x0 = 1.5 :: Double
  d = ARR.fromList @SHT (take (ROWS * cols) elemsFrom)
  t = viewOf elemsFrom
  -- The view in the vector's order; an array of one element at stride 0
  -- throughout; the view under a dimension of two elements at stride 0,
  -- and among five dimensions, the outermost of one element and two between
  -- its own two, of two elements at stride 0 and of one, each beside its
  -- order's so; and the view less its last column, its rows of the other
  -- parity.
  tn = ARR.normalize t
  c = ARR.constant @SH x0
  t3 = ARR.broadcast @Bc12 @SH3 t
  t3n = ARR.broadcast @Bc12 @SH3 tn
  tx = ARR.broadcast @Bc14 @SH5 t
  txn = ARR.broadcast @Bc14 @SH5 tn
  tnr = ARR.slice @SLNR t
  row = ARR.index t 0
#if ROWS > 0
  -- The view's first row alone, its first element alone, the view with an
  -- element changed, an array of no rows to append the view to, its first row
  -- reshaped to the view's rank, and the first row of the view's order.
  t1 = ARR.slice @Sl1 t
  t11 = ARR.slice @Sl11 t
  tu = ARR.update t [(ielem, 9)]
  e = ARR.fromList @EMP []
  r1 = ARR.reshape @ROW1 row
  rown = ARR.index tn 0
  -- Seven dimensions at stride 1, whose lengths fall in every tier the sort
  -- of an unordered route ranks runs by, two pairs of them in one tier each.
  tw = ARR.window @TW1 (ARR.window @TW2 (ARR.window @TW3
         (ARR.window @TW4 (ARR.window @TW5 (ARR.window @TW6
           (ARR.fromList @TWN (take twn elemsFrom)))))))
#endif
  same = viewOf (repeat x0)
  viewOf :: [Double] -> ARR.Array SH Double
  viewOf xs = case view of
    Dense -> ARR.fromList @SH (take (ROWS * cols) xs)
    Strided -> ARR.transpose @Perm (ARR.fromList @SHT (take (ROWS * cols) xs))
    Runs -> ARR.slice @SLR (ARR.fromList @SHR (take (ROWS * (cols + 2)) xs))
    Scaled -> ARR.stride @Str2 (ARR.fromList @SHW (take (ROWS * 2 * cols) xs))
    Bcastmid -> ARR.stretch @SH (ARR.fromList @ROW1 (take cols xs))
    Flip -> ARR.rev @Rev1 (ARR.fromList @SH (take (ROWS * cols) xs))
#if ROWS > 0
    Window -> ARR.window @WINO
                     (ARR.fromList @SHO (take (ROWS + cols - 1) xs))
#else
    Window -> error "viewOf: a window of no rows has no type"
#endif
    Bcast -> ARR.stretch @SH (ARR.fromList @COL1 (take ROWS xs))
    Scalar -> ARR.constant @SH (sum (take 1 xs))
  -- The size comes at run time: of a size known statically, full laziness
  -- would make the array a constant computed once.
  iota k = case someNatVal (toInteger k) of
    Just (SomeNat p) -> ARR.toVector (ARR.iota `sizedBy` p)
    Nothing -> error "iota: negative size"
  sizedBy :: ARR.Array (Vec m) Double -> Proxy m -> ARR.Array (Vec m) Double
  sizedBy a _ = a
