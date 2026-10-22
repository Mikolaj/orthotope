-- Every operation of a Dynamic module, included by OpsDynamic once a vector
-- kind and a size with ARR the module of the kind, OPS its list on a view
-- in a form, ROWS the shape's rows, SIZE the size's other values, IARR the
-- kind's internal module, CONV the module of the kind convert converts to,
-- BOXED or STORABLE defined at those kinds, CR and CS the kind's Ranked and
-- Shaped modules, and SHD and FLATD the Shaped shapes of the view and of its
-- elements in a row.  After an operation's call come those of the arms it
-- leaves untaken, each named for its operation and its arm; at ROWS 0 only the
-- calls an empty array takes.
OPS :: Form -> View -> [Call]
OPS form view =
  [ call "size" (\ a -> ARR.size a) t
  , call "shapeL" (\ a -> ARR.shapeL a) t
  , call "rank" (\ a -> ARR.rank a) t
  , call "toList" (\ a -> sum (ARR.toList a)) t
  , call "fromList" (\ xs -> ARR.fromList [ROWS, cols] xs)
                    (take (ROWS * cols) elemsFrom)
  , call "fromList.map" (\ xs -> ARR.fromList [ROWS, cols] (map (+ 1) xs))
                        (take (ROWS * cols) elemsFrom)
  , call "toVector" (\ a -> ARR.toVector a) t
  , call "toUnorderedVectorT"
         (\ (IARR.A (DG.A sh u)) -> I.toUnorderedVectorT sh u) t
  , call "toUnorderedVectorListT"
         (\ (IARR.A (DG.A sh u)) -> I.toUnorderedVectorListT sh u) t
  , call "fromVector" (\ v -> ARR.fromVector [ROWS, cols] v) (ARR.toVector d)
  , call "normalize" (\ a -> ARR.normalize a) t
  , call "force" (\ a -> ARR.force a) t
  , call "force.rank5" (\ a -> ARR.force a) tx
  , call "force.narrow" (\ a -> ARR.force a) tnr
#if ROWS > 0
  , call "force.window" (\ a -> ARR.force (ARR.window [2, 2] a)) t
#endif
  , call "scalar" (\ x -> ARR.scalar x) x0
  , call "unScalar" (\ a -> ARR.unScalar a) (ARR.scalar x0)
  , call "constant" (\ x -> ARR.constant [ROWS, cols] x) x0
  , call "reshape" (\ a -> ARR.reshape [ROWS * cols] a) t
#if ROWS > 0
  , call "reshape.scalar" (\ a -> ARR.reshape [] a) t11
#endif
#if ROWS > 0
  , call "stretch" (\ a -> ARR.stretch [ROWS, cols] a) r1
  , call "stretchOuter" (\ a -> ARR.stretchOuter ROWS a) r1
#endif
  , call "transpose" (\ a -> ARR.transpose [1, 0] a) t
#if ROWS > 0
  , call "index" (\ a -> ARR.index a irow) t
#endif
  -- Every element read through two indexes, the row index i varying
  -- fastest so that each element takes its own row: with j fastest, one
  -- row served a whole row of elements.
  , call "indexIndex"
         (\ a -> sum [ ARR.unScalar (ARR.index (ARR.index a i) j)
                     | j <- [0 .. cols - 1], i <- [0 .. ROWS - 1] ]) t
  , call "pad" (\ a -> ARR.pad [(0, 1), (1, 1)] 0 a) t
  , call "pad.none" (\ a -> ARR.pad [(0, 0), (0, 0)] 0 a) t
  , call "pad.outer" (\ a -> ARR.pad [(1, 1)] 0 a) t
  , call "mapA" (\ a -> ARR.mapA (+ 1) a) t
  , call "zipWithA" (\ (a, b) -> ARR.zipWithA (+) a b) (t, tn)
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
  , call "append" (\ (a, b) -> ARR.append a b) (t, tn)
#if ROWS > 0
  , call "append.emptyL" (\ a -> ARR.append e a) t
  , call "append.emptyR" (\ a -> ARR.append a e) t
#endif
  , call "concatOuter" (\ (a, b) -> ARR.concatOuter [a, b]) (t, tn)
  , call "concatOuter.one" (\ a -> ARR.concatOuter [a]) t
#if ROWS > 0
  , call "concatOuter.map"
         (\ a -> ARR.concatOuter
                   (map (\ i -> ARR.slice [(i, 1)] a) [0 .. ROWS - 1]))
         t
#endif
#if ROWS > 0
  , call "ravel" (\ a -> ARR.ravel a) (ARR.unravel t)
  , call "ravel.one" (\ a -> ARR.ravel a) (ARR.unravel t1)
#endif
  , call "unravel" (\ a -> ARR.unravel a) t
#if ROWS > 0
  , call "window" (\ a -> ARR.window [2, 2] a) t
#endif
  , call "stride" (\ a -> ARR.stride [2, 2] a) t
  , call "stride.outer" (\ a -> ARR.stride [2] a) t
  , call "rotate" (\ a -> ARR.rotate 0 2 a) t
  , call "rotate.one" (\ a -> ARR.rotate 1 1 a) t
  , call "rotate.inner" (\ a -> ARR.rotate 1 2 a) t
#if ROWS > 0
  , call "slice" (\ a -> ARR.slice [(1, sliceRows), (1, cols - 1)] a) t
  , call "rerank" (\ a -> ARR.rerank 1 (\ r -> ARR.scalar (ARR.sumA r)) a) t
  , call "rerank2"
         (\ (a, b) -> ARR.rerank2 1 (\ x y -> ARR.zipWithA (+) x y) a b) (t, tn)
  , call "rerank2.one"
         (\ a -> ARR.rerank2 1 (\ x y -> ARR.zipWithA (+) x y) a a) t1
#endif
  , call "rev" (\ a -> ARR.rev [0, 1] a) t
  , call "reduce" (\ a -> ARR.reduce (+) 0 a) t
  , call "foldrA" (\ a -> ARR.foldrA (+) 0 a) t
  , call "traverseA"
         (\ a -> runIdentity (ARR.traverseA (\ x -> Identity (x + 1)) a)) t
  , call "allSameA" (\ a -> ARR.allSameA a) same
#if ROWS > 0
  , call "allSameA.tiers" (\ a -> ARR.allSameA a) tw
#endif
  , call "sumA" (\ a -> ARR.sumA a) t
  , call "productA" (\ a -> ARR.productA a) t
#if ROWS > 0
  , call "maximumA" (\ a -> ARR.maximumA a) t
  , call "maximumA.one" (\ a -> ARR.maximumA a) t11
  , call "maximumA.rank5" (\ a -> ARR.maximumA a) tx
  , call "minimumA" (\ a -> ARR.minimumA a) t
#endif
  , call "anyA" (\ a -> ARR.anyA (> 2) a) t
  , call "allA" (\ a -> ARR.allA (< 2) a) t
  , call "broadcast" (\ a -> ARR.broadcast [1, 2, 3] [2, 2, ROWS, cols, 2] a) t3
#if ROWS > 0
  , call "update" (\ a -> ARR.update a [(ielem, 9)]) t
#endif
  , call "update.none" (\ a -> ARR.update a []) t
  -- A pair per perPair elements built in each call, the list depending on its
  -- array so that it is not floated out of the loop.
  , call "update2000"
         (\ a -> ARR.update a [ ([i `quot` cols, i `rem` cols], fromIntegral i)
                              | i <- [0 .. ARR.size a `quot` perPair - 1] ]) t
  , call "generate" (\ k -> ARR.generate [ROWS, cols]
                                (\ ix -> fromIntegral (sum ix + k) :: Double))
                  0
  , call "iterateN" (\ x -> ARR.iterateN (ROWS * cols) (+ 1) x) x0
  , call "iota" (\ k -> ARR.iota k :: ARR.Array Double) (ROWS * cols)
#ifdef STORABLE
  , call "bitcast" (\ a -> ARR.bitcast a :: ARR.Array Int64) t
#endif
  , call "convert" (\ a -> convert a :: CONV.Array Double) t
  , call "convertE" (\ a -> convertE a :: Either String (CONV.Array Double)) t
  , call "convert.rank5" (\ a -> convert a :: CONV.Array Double) tx
#if defined(BOXED) || defined(STORABLE)
  , call "convert.ranked" (\ a -> convert a :: CR.Array 2 Double) t
  , call "convertE.ranked"
         (\ a -> convertE a :: Either String (CR.Array 3 Double)) t
  , call "convert.shaped" (\ a -> convert a :: CS.Array SHD Double) t
  , call "convertE.shaped"
         (\ a -> convertE a :: Either String (CS.Array FLATD Double)) t
#endif
#ifdef BOXED
  , call "convert.unboxed" (\ a -> convert a :: U.Array Double) t
  , call "convertE.unboxed"
         (\ a -> convertE a :: Either String (U.Array Double)) t
#endif
  , call "convert.g" (\ a -> convert a `asTypeOf` IARR.unA a) t
  , call "convertE.g" (\ a -> convertE a `asTypeOf` Right (IARR.unA a)) t
  , call "==" (\ (a, b) -> (a == b, b == a)) (t, tn)
#if ROWS > 0
  , call "==.shapes" (\ (a, b) -> a == b) (t, t1)
  , call "==.rank1" (\ (a, b) -> a == b) (row, rown)
#endif
  , call "==.rank3" (\ (a, b) -> a == b) (t3, t3n)
  , call "==.rank5" (\ (a, b) -> a == b) (tx, txn)
#if ROWS > 0
  , call "==.units" (\ (a, b) -> a == b) (t1, r1)
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
  , call "fmap" (\ a -> fmap (+ 1) a) t
  , call "<$" (\ a -> x0 <$ a) t
  , call "fold" (\ a -> fold a) (fmap Sum t)
  , call "foldr" (\ a -> foldr (+) 0 a) t
  , call "traverse" (\ a -> runIdentity (traverse (\ x -> Identity (x + 1)) a))
                    t
  , call "sequenceA" (\ a -> runIdentity (sequenceA a)) (fmap Identity t)
#endif
  ]
 where
  Size {..} = SIZE
  x0 = 1.5 :: Double
  d = ARR.fromList [cols, ROWS] (take (ROWS * cols) elemsFrom)
  t = formed (viewOf elemsFrom)
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
  same = formed (viewOf (repeat x0))
  formed a = case form of
    Viewed -> a
    Normalized -> ARR.normalize a
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
