-- Every operation of a Ranked module, included by OpsRanked once
-- a vector kind with ARR the module of the kind and OPS its list.
OPS :: [Call]
OPS =
  [ Call "size" ARR.size t
  , Call "shapeL" ARR.shapeL t
  , Call "rank" ARR.rank t
  , Call "toList" (sum . ARR.toList) t
  , Call "fromList" (\ xs -> ARR.fromList [400, 500] xs `asTypeOf` t) elems
  , Call "toVector" ARR.toVector t
  , Call "fromVector" (\ v -> ARR.fromVector [400, 500] v `asTypeOf` t)
                    (ARR.toVector d)
  , Call "normalize" ARR.normalize t
  , Call "scalar" ARR.scalar x0
  , Call "unScalar" ARR.unScalar (ARR.scalar x0)
  , Call "constant" (\ x -> ARR.constant [400, 500] x `asTypeOf` t) x0
  , Call "reshape" (\ a -> ARR.reshape [n] a `asTypeOf` row) t
  , Call "stretch" (ARR.stretch [400, 500]) r1
  , Call "stretchOuter" (ARR.stretchOuter 400) r1
  , Call "transpose" (ARR.transpose [1, 0]) t
  , Call "index" (\ a -> ARR.index a 7 `asTypeOf` row) t
  , Call "pad" (ARR.pad [(1, 1), (1, 1)] 0) t
  , Call "mapA" (ARR.mapA (+ 1)) t
  , Call "zipWithA" (\ a -> ARR.zipWithA (+) a a) t
  , Call "zipWith3A" (\ a -> ARR.zipWith3A (\ x y z -> x + y + z) a a a) t
  , Call "append" (\ a -> ARR.append a a) t
  , Call "concatOuter" (\ a -> ARR.concatOuter [a, a]) t
  , Call "ravel" (\ a -> ARR.ravel a `asTypeOf` t) rows
  , Call "unravel" (\ a -> ARR.unravel a `asTypeOf` rows) t
  , Call "window" (\ a -> ARR.window [2, 2] a :: ARR.Array 4 Double) t
  , Call "stride" (ARR.stride [2, 2]) t
  , Call "rotate" (\ a -> ARR.rotate @0 2 a :: ARR.Array 3 Double) t
  , Call "slice" (ARR.slice [(1, 398)]) t
  , Call "rerank" (ARR.rerank @1
                     (\ r -> ARR.scalar (ARR.sumA (r `asTypeOf` row))))
                t
  , Call "rerank2" (\ a -> ARR.rerank2 @1
                           (\ x y -> ARR.zipWithA (+) (x `asTypeOf` row) y) a a)
                 t
  , Call "rev" (ARR.rev [0]) t
  , Call "reduce" (ARR.reduce (+) 0) t
  , Call "foldrA" (ARR.foldrA (+) 0) t
  , Call "traverseA" (runIdentity . ARR.traverseA (Identity . (+ 1))) t
  , Call "allSameA" ARR.allSameA same
  , Call "sumA" ARR.sumA t
  , Call "productA" ARR.productA t
  , Call "maximumA" ARR.maximumA t
  , Call "minimumA" ARR.minimumA t
  , Call "anyA" (ARR.anyA (> 2)) t
  , Call "allA" (ARR.allA (< 2)) t
  , Call "broadcast" (\ a -> ARR.broadcast [1] [400, 500] a `asTypeOf` t) row
  , Call "generate" (\ k -> ARR.generate [400, 500]
                                      (\ ix -> fromIntegral (sum ix + k))
                          `asTypeOf` t)
                  0
  , Call "iterateN" (ARR.iterateN n (+ 1)) x0
  , Call "iota" (ARR.iota :: Int -> ARR.Array 1 Double) n
  , Call "==" (\ a -> a == a) t
  , Call "compare" (\ a -> compare a a) t
  , Call "rnf" id t
  ]
 where
  x0 = 1.5 :: Double
  d = ARR.fromList [500, 400] elems `asTypeOf` t
  t = ARR.transpose [1, 0] d :: ARR.Array 2 Double
  row = ARR.index t 0 :: ARR.Array 1 Double
  r1 = ARR.reshape [1, 500] row `asTypeOf` t
  rows = ARR.unravel t :: B.Array 1 (ARR.Array 1 Double)
  same = ARR.transpose [1, 0] (ARR.fromList [500, 400] (replicate n x0))
         `asTypeOf` t
