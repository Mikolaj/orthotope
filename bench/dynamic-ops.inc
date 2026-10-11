-- Every operation of a Dynamic module, included by OpsDynamic once a vector
-- kind and a size with ARR the module of the kind, OPS its list on a view, ROWS
-- the shape's rows, SIZE the size's other values, IARR the kind's internal
-- module, CONV the module of the kind convert converts to, BOXED or STORABLE
-- defined at those kinds, CR and CS the kind's Ranked and Shaped modules, and
-- SHD and FLATD the Shaped shapes of the view and of its elements in a row.
-- After an operation's call come those of the arms it leaves untaken, each
-- named for its operation and its arm; at ROWS 0 only the calls an empty array
-- takes.
OPS :: View -> [Call]
OPS view =
  [ call "size" ARR.size t
  , call "shapeL" ARR.shapeL t
  , call "rank" ARR.rank t
  , call "toList" (sum . ARR.toList) t
  , call "fromList" (ARR.fromList [ROWS, cols]) (take (ROWS * cols) elemsFrom)
  , call "toVector" ARR.toVector t
  , call "toUnorderedVectorT"
         (\ (IARR.A (DG.A sh u)) -> I.toUnorderedVectorT sh u) t
  , call "toUnorderedVectorListT"
         (\ (IARR.A (DG.A sh u)) -> I.toUnorderedVectorListT sh u) t
  , call "fromVector" (ARR.fromVector [ROWS, cols]) (ARR.toVector d)
  , call "normalize" ARR.normalize t
  , call "force" ARR.force t
  , call "force.rank5" ARR.force tx
  , call "force.narrow" ARR.force tnr
#if ROWS > 0
  , call "force.window" (ARR.force . ARR.window [2, 2]) t
#endif
  , call "scalar" ARR.scalar x0
  , call "unScalar" ARR.unScalar (ARR.scalar x0)
  , call "constant" (ARR.constant [ROWS, cols]) x0
  , call "reshape" (ARR.reshape [ROWS * cols]) t
#if ROWS > 0
  , call "reshape.scalar" (ARR.reshape []) t11
#endif
#if ROWS > 0
  , call "stretch" (ARR.stretch [ROWS, cols]) r1
  , call "stretchOuter" (ARR.stretchOuter ROWS) r1
#endif
  , call "transpose" (ARR.transpose [1, 0]) t
#if ROWS > 0
  , call "index" (`ARR.index` irow) t
#endif
  -- Every element read through two indexes, the row index i varying
  -- fastest so that each element takes its own row: with j fastest, one
  -- row served a whole row of elements.
  , call "indexIndex"
         (\ a -> sum [ ARR.unScalar (ARR.index (ARR.index a i) j)
                     | j <- [0 .. cols - 1], i <- [0 .. ROWS - 1] ]) t
  , call "pad" (ARR.pad [(0, 1), (1, 1)] 0) t
  , call "pad.none" (ARR.pad [(0, 0), (0, 0)] 0) t
  , call "pad.outer" (ARR.pad [(1, 1)] 0) t
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
  , call "concatOuter" (\ (a, b) -> ARR.concatOuter [a, b]) (t, tn)
  , call "concatOuter.one" (\ a -> ARR.concatOuter [a]) t
#if ROWS > 0
  , call "ravel" ARR.ravel (ARR.unravel t)
  , call "ravel.one" ARR.ravel (ARR.unravel t1)
#endif
  , call "unravel" ARR.unravel t
#if ROWS > 0
  , call "window" (ARR.window [2, 2]) t
#endif
  , call "stride" (ARR.stride [2, 2]) t
  , call "stride.outer" (ARR.stride [2]) t
  , call "rotate" (ARR.rotate 0 2) t
  , call "rotate.one" (ARR.rotate 1 1) t
#if ROWS > 0
  , call "slice" (ARR.slice [(1, sliceRows), (1, cols - 1)]) t
  , call "rerank" (ARR.rerank 1 (ARR.scalar . ARR.sumA)) t
  , call "rerank2" (\ (a, b) -> ARR.rerank2 1 (ARR.zipWithA (+)) a b) (t, tn)
  , call "rerank2.one" (\ a -> ARR.rerank2 1 (ARR.zipWithA (+)) a a) t1
#endif
  , call "rev" (ARR.rev [0, 1]) t
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
  , call "broadcast" (ARR.broadcast [1, 2, 3] [2, 2, ROWS, cols, 2]) t3
#if ROWS > 0
  , call "update" (`ARR.update` [(ielem, 9)]) t
#endif
  , call "update.none" (`ARR.update` []) t
  -- A pair per perPair elements built in each call, the list depending on its
  -- array so that it is not floated out of the loop.
  , call "update2000"
         (\ a -> ARR.update a [ ([i `quot` cols, i `rem` cols], fromIntegral i)
                              | i <- [0 .. ARR.size a `quot` perPair - 1] ]) t
  , call "generate" (\ k -> ARR.generate [ROWS, cols]
                                (\ ix -> fromIntegral (sum ix + k) :: Double))
                  0
  , call "iterateN" (ARR.iterateN (ROWS * cols) (+ 1)) x0
  , call "iota" (ARR.iota :: Int -> ARR.Array Double) (ROWS * cols)
#ifdef WITH_BITCAST
  , call "bitcast" (ARR.bitcast :: ARR.Array Double -> ARR.Array Int64) t
#endif
  , call "convert" (convert :: ARR.Array Double -> CONV.Array Double) t
  , call "convertE"
         (convertE :: ARR.Array Double -> Either String (CONV.Array Double)) t
  , call "convert.rank5" (convert :: ARR.Array Double -> CONV.Array Double) tx
#if defined(BOXED) || defined(STORABLE)
  , call "convert.ranked" (convert :: ARR.Array Double -> CR.Array 2 Double) t
  , call "convertE.ranked"
         (convertE :: ARR.Array Double -> Either String (CR.Array 3 Double)) t
  , call "convert.shaped" (convert :: ARR.Array Double -> CS.Array SHD Double) t
  , call "convertE.shaped"
         (convertE :: ARR.Array Double
                   -> Either String (CS.Array FLATD Double)) t
#endif
#ifdef BOXED
  , call "convert.unboxed" (convert :: ARR.Array Double -> U.Array Double) t
  , call "convertE.unboxed"
         (convertE :: ARR.Array Double -> Either String (U.Array Double)) t
#endif
  , call "convert.g" (\ a -> convert a `asTypeOf` IARR.unA a) t
  , call "convertE.g" (\ a -> convertE a `asTypeOf` Right (IARR.unA a)) t
  , call "==" (\ (a, b) -> (a == b, b == a)) (t, tn)
#if ROWS > 0
  , call "==.shapes" (uncurry (==)) (t, t1)
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
#endif
  ]
 where
  Size {..} = SIZE
  x0 = 1.5 :: Double
  d = ARR.fromList [cols, ROWS] (take (ROWS * cols) elemsFrom)
  t = viewOf elemsFrom
  -- The view in the vector's order; an array of one element at stride 0
  -- throughout; the view under a dimension of two elements at stride 0,
  -- and among five dimensions, the outermost of one element and two between
  -- its own two, of two elements at stride 0 and of one, each beside its
  -- order's so; and the view less its last column, its rows of the other
  -- parity.
  tn = ARR.normalize t
  c = ARR.constant [ROWS, cols] x0
  t3 = ARR.broadcast [1, 2] [2, ROWS, cols] t
  t3n = ARR.broadcast [1, 2] [2, ROWS, cols] tn
  tx = ARR.broadcast [1, 4] [1, ROWS, 2, 1, cols] t
  txn = ARR.broadcast [1, 4] [1, ROWS, 2, 1, cols] tn
  tnr = ARR.slice [(0, ROWS), (0, cols - 1)] t
#if ROWS > 0
  -- The view's first row alone, its first element alone, the view with an
  -- element changed, an array of no rows to append the view to, the first rows
  -- of the view and of its order's, and the view's first row reshaped to the
  -- view's rank.
  t1 = ARR.slice [(0, 1)] t
  t11 = ARR.slice [(0, 1), (0, 1)] t
  tu = ARR.update t [(ielem, 9)]
  e = ARR.fromList [0, cols] []
  row = ARR.index t 0
  rown = ARR.index tn 0
  r1 = ARR.reshape [1, cols] row
  -- Seven dimensions at stride 1, whose lengths fall in every tier the sort
  -- of an unordered route ranks runs by, two pairs of them in one tier each.
  tw = ARR.window [tw1] (ARR.window [tw2] (ARR.window [tw3]
         (ARR.window [tw4] (ARR.window [tw5] (ARR.window [tw6]
           (ARR.fromList [twn] (take twn elemsFrom)))))))
#endif
  same = viewOf (repeat x0)
  viewOf xs = case view of
    Dense -> ARR.fromList [ROWS, cols] (take (ROWS * cols) xs)
    Strided -> ARR.transpose [1, 0]
                    (ARR.fromList [cols, ROWS] (take (ROWS * cols) xs))
    Runs -> ARR.slice [(0, ROWS), (1, cols)]
                (ARR.fromList [ROWS, cols + 2] (take (ROWS * (cols + 2)) xs))
    Scaled -> ARR.stride [1, 2]
                 (ARR.fromList [ROWS, 2 * cols] (take (ROWS * 2 * cols) xs))
    Bcastmid -> ARR.stretch [ROWS, cols]
                   (ARR.fromList [1, cols] (take cols xs))
    Flip -> ARR.rev [1] (ARR.fromList [ROWS, cols] (take (ROWS * cols) xs))
    Window -> ARR.window [cols]
                     (ARR.fromList [ROWS + cols - 1]
                                   (take (ROWS + cols - 1) xs))
    Bcast -> ARR.stretch [ROWS, cols]
                (ARR.fromList [ROWS, 1] (take ROWS xs))
    Scalar -> ARR.constant [ROWS, cols] (sum (take 1 xs))
