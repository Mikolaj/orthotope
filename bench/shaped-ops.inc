-- Every operation of a Shaped module, included by OpsShaped once
-- a vector kind with ARR the module of the kind and OPS its list.
OPS :: [Call]
OPS =
  [ Call "size" ARR.size t
  , Call "shapeL" ARR.shapeL t
  , Call "rank" ARR.rank t
  , Call "toList" (sum . ARR.toList) t
  , Call "fromList" (ARR.fromList @Sh) elems
  , Call "toVector" ARR.toVector t
  , Call "fromVector" (ARR.fromVector @Sh) (ARR.toVector d)
  , Call "normalize" ARR.normalize t
  , Call "force" ARR.force t
  , Call "scalar" ARR.scalar x0
  , Call "unScalar" ARR.unScalar (ARR.scalar x0)
  , Call "constant" (ARR.constant @Sh) x0
  , Call "reshape" (ARR.reshape @Flat) t
  , Call "stretch" (ARR.stretch @Sh) r1
  , Call "stretchOuter" (\ a -> ARR.stretchOuter a `asTypeOf` t) r1
  , Call "transpose" (ARR.transpose @Perm) t
  , Call "index" (`ARR.index` 7) t
  , Call "pad" (ARR.pad @Pads 0) t
  , Call "mapA" (ARR.mapA (+ 1)) t
  , Call "zipWithA" (\ a -> ARR.zipWithA (+) a a) t
  , Call "zipWith3A" (\ a -> ARR.zipWith3A (\ x y z -> x + y + z) a a a) t
  , Call "zipWith4A" (\ a -> ARR.zipWith4A (\ x y z u -> x + y + z + u)
                                         a a a a) t
  , Call "zipWith5A" (\ a -> ARR.zipWith5A (\ x y z u w -> x + y + z + u + w)
                                         a a a a a) t
  , Call "append" (\ a -> ARR.append a a) t
  , Call "concatOuter" (\ a -> ARR.concatOuter @800 [a, a]) t
  , Call "ravel" ARR.ravel (ARR.unravel t)
  , Call "unravel" ARR.unravel t
  , Call "window" (ARR.window @Win) t
  , Call "stride" (ARR.stride @Win) t
  , Call "rotate" (ARR.rotate @0 @2) t
  , Call "slice" (ARR.slice @Sl) t
  , Call "rerank" (ARR.rerank @1
                     (\ r -> ARR.scalar (ARR.sumA (r `asTypeOf` row))))
                t
  , Call "rerank2" (\ a -> ARR.rerank2 @1
                           (\ x y -> ARR.zipWithA (+) (x `asTypeOf` row) y) a a)
                 t
  , Call "rev" (ARR.rev @Rev0) t
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
  , Call "broadcast" (ARR.broadcast @Bc @Sh) row
  , Call "update" (`ARR.update` [([3, 4], 9)]) t
  , Call "generate" (\ k -> ARR.generate (\ ix -> fromIntegral (sum ix + k))
                          `asTypeOf` t)
                  0
  , Call "iterateN" (ARR.iterateN @200000 (+ 1)) x0
  , Call "iota" iota n
#ifdef WITH_BITCAST
  , Call "bitcast" (ARR.bitcast :: ARR.Array Sh Double -> ARR.Array Sh Int64) t
#endif
  , Call "==" (\ a -> a == a) t
  , Call "compare" (\ a -> compare a a) t
  , Call "rnf" id t
  ]
 where
  x0 = 1.5 :: Double
  d = ARR.fromList @ShT elems
  t = ARR.transpose @Perm d
  row = ARR.index t 0
  r1 = ARR.reshape @Row1 row
  same = ARR.transpose @Perm (ARR.fromList @ShT (replicate n x0))
  -- The size comes at run time: of a size known statically, full laziness
  -- would make the array a constant computed once.
  iota k = case someNatVal (toInteger k) of
    Just (SomeNat p) -> ARR.toVector (ARR.iota `sizedBy` p)
    Nothing -> error "iota: negative size"
  sizedBy :: ARR.Array (Vec m) Double -> Proxy m -> ARR.Array (Vec m) Double
  sizedBy a _ = a
