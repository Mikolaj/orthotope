-- Every operation of a Dynamic module, included by OpsDynamic once
-- a vector kind with ARR the module of the kind and OPS its list.
OPS :: [Call]
OPS =
  [ Call "size" ARR.size t
  , Call "shapeL" ARR.shapeL t
  , Call "rank" ARR.rank t
  , Call "toList" (sum . ARR.toList) t
  , Call "fromList" (ARR.fromList [400, 500]) elems
  , Call "toVector" ARR.toVector t
  , Call "fromVector" (ARR.fromVector [400, 500]) (ARR.toVector d)
  , Call "normalize" ARR.normalize t
  , Call "scalar" ARR.scalar x0
  , Call "unScalar" ARR.unScalar (ARR.scalar x0)
  , Call "constant" (ARR.constant [400, 500]) x0
  , Call "reshape" (ARR.reshape [n]) t
  , Call "stretch" (ARR.stretch [400, 500]) r1
  , Call "stretchOuter" (ARR.stretchOuter 400) r1
  , Call "transpose" (ARR.transpose [1, 0]) t
  , Call "index" (`ARR.index` 7) t
  , Call "pad" (ARR.pad [(1, 1), (1, 1)] 0) t
  , Call "mapA" (ARR.mapA (+ 1)) t
  , Call "zipWithA" (\ a -> ARR.zipWithA (+) a a) t
  , Call "zipWith3A" (\ a -> ARR.zipWith3A (\ x y z -> x + y + z) a a a) t
  , Call "zipWith4A" (\ a -> ARR.zipWith4A (\ x y z u -> x + y + z + u)
                                         a a a a) t
  , Call "zipWith5A" (\ a -> ARR.zipWith5A (\ x y z u w -> x + y + z + u + w)
                                         a a a a a) t
  , Call "append" (\ a -> ARR.append a a) t
  , Call "concatOuter" (\ a -> ARR.concatOuter [a, a]) t
  , Call "ravel" ARR.ravel (ARR.unravel t)
  , Call "unravel" ARR.unravel t
  , Call "window" (ARR.window [2, 2]) t
  , Call "stride" (ARR.stride [2, 2]) t
  , Call "rotate" (ARR.rotate 0 2) t
  , Call "slice" (ARR.slice [(1, 398)]) t
  , Call "rerank" (ARR.rerank 1 (ARR.scalar . ARR.sumA)) t
  , Call "rerank2" (\ a -> ARR.rerank2 1 (ARR.zipWithA (+)) a a) t
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
  , Call "broadcast" (ARR.broadcast [1] [400, 500]) row
  , Call "update" (`ARR.update` [([3, 4], 9)]) t
  , Call "generate" (\ k -> ARR.generate [400, 500]
                                (\ ix -> fromIntegral (sum ix + k) :: Double))
                  0
  , Call "iterateN" (ARR.iterateN n (+ 1)) x0
  , Call "iota" (ARR.iota :: Int -> ARR.Array Double) n
#ifdef WITH_BITCAST
  , Call "bitcast" (ARR.bitcast :: ARR.Array Double -> ARR.Array Int64) t
#endif
  , Call "==" (\ a -> a == a) t
  , Call "compare" (\ a -> compare a a) t
  , Call "rnf" id t
  ]
 where
  x0 = 1.5 :: Double
  d = ARR.fromList [500, 400] elems
  t = ARR.transpose [1, 0] d
  row = ARR.index t 0
  r1 = ARR.reshape [1, 500] row
  same = ARR.transpose [1, 0] (ARR.fromList [500, 400] (replicate n x0))
