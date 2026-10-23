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

-- Whether a client's call builds a value of a type the library marks as never
-- to be built, Route, Range and Axes: each binding that returns or takes one,
-- called as a client calls it on each view of the small size, the value taken
-- apart at once, with the bytes the call allocates as compiled and with the
-- value handed to 'built', a function out of line, which builds it.  Where the
-- two agree, the call as compiled built it too; where it did not, they part by
-- the value's size: 24 bytes a Range or an RSlice, 32 an Axes, 64 an RRuns or
-- an RFill with its Axes, and none a NoRange, which is static.
module Materialize (Probe (..), probes) where

import qualified Data.Array.DynamicS as S
import qualified Data.Array.Internal as I
import qualified Data.Array.Internal.DynamicG as DG
import qualified Data.Array.Internal.DynamicS as DS

import Call (View (..), elemsFrom, viewName, views)

-- | A probe: its row, the call as compiled, the call building the value, and
-- the view it is called on.
data Probe = Probe String (S.Array Double -> Int) (S.Array Double -> Int)
                   (S.Array Double)

-- | Each probe on each view of the small size.
probes :: [Probe]
probes =
  [ Probe (ty ++ "/" ++ name ++ "/" ++ viewName view) f g (viewOf view)
  | (ty, name, f, g) <- calls, view <- views ]

-- The bindings that take or return one, each as compiled and with the value
-- built.
calls :: [(String, String, S.Array Double -> Int, S.Array Double -> Int)]
calls = [ (ty, name, f . DS.unA, g . DS.unA) | (ty, name, f, g) <- calls' ]
 where
  calls' =
    [ ("Route", "routeT", route I.routeT fields id, route I.routeT fields built)
    , ("Route", "unorderedRouteT", route I.unorderedRouteT fields id
                                 , route I.unorderedRouteT fields built)
    , ("Route", "cellsRouteT", route I.cellsRouteT fields id
                             , route I.cellsRouteT fields built)
    , ("Route", "routeOfT", routeOf id, routeOf built)
    , ("Route", "routeVectorT", route I.routeT vector id
                              , route I.routeT vector built)
    , ("Route", "routeSlicesT", route I.routeT slices id
                              , route I.routeT slices built)
    , ("Route", "routeFoldT", route I.routeT fold id, route I.routeT fold built)
    , ("Route", "routePartsT", route I.routeT parts id
                             , route I.routeT parts built)
    , ("Range", "readRangeT", readRange id, readRange built)
    , ("Range", "sameRangeT", sameRange id, sameRange built)
    , ("Range", "range3T", range3 id, range3 built)
    , ("Axes", "canonicalizeT", canonicalize id, canonicalize built)
    , ("Axes", "sortAxesT", sortAxes id, sortAxes built)
    , ("Axes", "canonicalizeSortedT", canonicalizeSorted id
                                    , canonicalizeSorted built)
    , ("Axes", "routeOfT", axesRouteOf id, axesRouteOf built)
    , ("Axes", "runSlicesT", runSlices id, runSlices built)
    , ("Axes", "elemsT", elems id, elems built)
    , ("Axes", "fillStrided", fill I.fillStrided id
                            , fill I.fillStrided built)
    , ("Axes", "vUnsafeFillStrided", fill I.vUnsafeFillStrided id
                                   , fill I.vUnsafeFillStrided built)
    , ("Axes", "genericUnsafeFillStrided"
              , fill (I.genericUnsafeFillStrided 64) id
              , fill (I.genericUnsafeFillStrided 64) built) ]

-- INLINE: Route, A3: each call, its value handed to the function given, the
-- identity or 'built', so that each call site knows which, and then to the
-- consumer given.
{-# INLINE route #-}
route :: (I.ShapeL -> Int -> I.T v Double -> I.Route)
      -> (v Double -> I.Route -> Int)
      -> (I.Route -> I.Route) -> DG.Array v Double -> Int
route f k b (DG.A sh t@(I.T _ _ v)) = k v (b $! f sh (product sh) t)

-- INLINE: Route, A3: see route.
{-# INLINE routeOf #-}
routeOf :: (I.Route -> I.Route) -> DG.Array v Double -> Int
routeOf b (DG.A sh t@(I.T _ o _)) =
  routeSum (b $! I.routeOfT o (product sh) (axesOf sh t))

-- INLINE: Route, A3: see route.
--
-- The consumers of a route that 'route' takes: its fields, and each binding
-- that takes one.
{-# INLINE fields #-}
fields :: v Double -> I.Route -> Int
fields _ = routeSum

-- INLINE: Route, A3: see route.
{-# INLINE vector #-}
vector :: (I.Vector v, I.VecElem v Double) => v Double -> I.Route -> Int
vector v r = I.vLength (I.routeVectorT v r)

-- INLINE: Route, A3: see route.
{-# INLINE slices #-}
slices :: (I.Vector v, I.VecElem v Double) => v Double -> I.Route -> Int
slices v r = I.routeSlicesT v r (\ s k -> I.vLength s + k) 0

-- INLINE: Route, A3: see route.
{-# INLINE fold #-}
fold :: (I.Vector v, I.VecElem v Double) => v Double -> I.Route -> Int
fold v r = I.routeFoldT v r (\ s k -> I.vLength s + k) (\ _ k -> k + 1) 0

-- INLINE: Route, A3: see route.
{-# INLINE parts #-}
parts :: v Double -> I.Route -> Int
parts _ r = I.routePartsT r (\ o l k -> o + l + k) 0

-- INLINE: Range, A3: see route.
{-# INLINE readRange #-}
readRange :: (I.Range -> I.Range) -> DG.Array v Double -> Int
readRange b (DG.A sh t) = rangeSum (b $! I.readRangeT sh t)

-- INLINE: Range, A3: see route.
{-# INLINE sameRange #-}
sameRange :: (I.Range -> I.Range) -> DG.Array v Double -> Int
sameRange b (DG.A sh t) = rangeSum (b $! I.sameRangeT sh sh t t)

-- INLINE: Range, A3: see route.
{-# INLINE range3 #-}
range3 :: (I.Range -> I.Range) -> DG.Array v Double -> Int
range3 b (DG.A [n1, n2] (I.T [s1, s2] o _)) =
  rangeSum (b $! I.range3T n1 s1 n2 s2 1 1 o)
range3 _ _ = 0

-- INLINE: Axes, A3: see route.
--
-- The canonical axes of the view, as 'I.routeT' takes them, its first axis
-- an 'I.Axes' and the rest left to the merge loop.
{-# INLINE canonicalize #-}
canonicalize :: (I.Axes -> I.Axes) -> DG.Array v Double -> Int
canonicalize b (DG.A sh t) = axesSum (b $! axesOf sh t)

-- INLINE: Axes, A3: see route.
--
-- The axes sorted, as 'I.unorderedRouteT' takes them.
{-# INLINE sortAxes #-}
sortAxes :: (I.Axes -> I.Axes) -> DG.Array v Double -> Int
sortAxes b (DG.A sh (I.T ats ao _)) = case I.absAxesAndStartT [] ao ats sh of
  (a : axs, _) -> axesSum (b $! I.sortAxesT a [] axs)
  ([], _) -> 0

-- INLINE: Axes, A3: see route.
--
-- The view's axes, unsorted, merged as if sorted, the first an 'I.Axes'.
{-# INLINE canonicalizeSorted #-}
canonicalizeSorted :: (I.Axes -> I.Axes) -> DG.Array v Double -> Int
canonicalizeSorted b (DG.A sh (I.T ats ao _)) =
  case I.absAxesAndStartT [] ao ats sh of
    (I.Axis st n : rest, _) ->
      axesSum (b $! I.canonicalizeSortedT rest (I.Axes st n (I.InnerFirst [])))
    ([], _) -> 0

-- INLINE: Axes, A3: it builds the Axes its callers hand on.
--
-- The canonical axes handed to each binding that takes them.
{-# INLINE axesOf #-}
axesOf :: I.ShapeL -> I.T v Double -> I.Axes
axesOf (n : ns) (I.T (st : sts) _ _) =
  I.canonicalizeT sts ns (I.Axes st n (I.InnerFirst []))
axesOf _ _ = I.Axes 1 1 (I.InnerFirst [])

-- INLINE: Axes, A3: see route.
{-# INLINE axesRouteOf #-}
axesRouteOf :: (I.Axes -> I.Axes) -> DG.Array v Double -> Int
axesRouteOf b (DG.A sh t@(I.T _ o _)) =
  routeSum (I.routeOfT o (product sh) (b $! axesOf sh t))

-- INLINE: Axes, A3: see route.
{-# INLINE runSlices #-}
runSlices :: (I.Vector v, I.VecElem v Double)
          => (I.Axes -> I.Axes) -> DG.Array v Double -> Int
runSlices b (DG.A sh t@(I.T _ o v)) =
  I.runSlicesT (b $! axesOf sh t) o v (\ s k -> I.vLength s + k) 0

-- INLINE: Axes, A3: see route.
{-# INLINE elems #-}
elems :: (I.Vector v, I.VecElem v Double)
      => (I.Axes -> I.Axes) -> DG.Array v Double -> Int
elems b (DG.A sh t@(I.T _ o v)) =
  I.elemsT (b $! axesOf sh t) o v (\ _ k -> k + 1) 0

-- INLINE: Axes, A3: see route.
{-# INLINE fill #-}
fill :: (I.Vector v, I.VecElem v Double)
     => (I.Axes -> Int -> Int -> v Double -> v Double)
     -> (I.Axes -> I.Axes) -> DG.Array v Double -> Int
fill f b (DG.A sh t@(I.T _ o v)) =
  I.vLength (f (b $! axesOf sh t) o (product sh) v)

-- NOINLINE: A3: the value handed to a function out of line, which builds it.
{-# NOINLINE built #-}
built :: a -> a
built x = x

-- INLINE: Route, A3: it takes apart the Route its callers build.
--
-- Every field of a route, taken apart.
{-# INLINE routeSum #-}
routeSum :: I.Route -> Int
routeSum r = case r of
  I.RSlice o l -> o + l
  I.RRuns axes o l -> axesSum axes + o + l
  I.RFill axes o l -> axesSum axes + o + l

-- INLINE: Range, A3: it takes apart the Range its callers build.
--
-- Every field of a range, taken apart.
{-# INLINE rangeSum #-}
rangeSum :: I.Range -> Int
rangeSum r = case r of
  I.Range o l -> o + l
  I.NoRange -> 0

-- INLINE: Axes, A3: it takes apart the Axes its callers build.
--
-- The fields of axes, the outer ones counted.
{-# INLINE axesSum #-}
axesSum :: I.Axes -> Int
axesSum (I.Axes s n (I.InnerFirst outer)) = s + n + length outer

-- The small size's views, as the Dynamic lists build them.
viewOf :: View -> S.Array Double
viewOf view = case view of
  Dense -> S.fromList [3, 3] (take 9 elemsFrom)
  Strided -> S.transpose [1, 0] (S.fromList [3, 3] (take 9 elemsFrom))
  Runs -> S.slice [(0, 3), (1, 3)] (S.fromList [3, 5] (take 15 elemsFrom))
  Scaled -> S.stride [1, 2] (S.fromList [3, 6] (take 18 elemsFrom))
  Bcastmid -> S.stretch [3, 3] (S.fromList [1, 3] (take 3 elemsFrom))
  Flip -> S.rev [1] (S.fromList [3, 3] (take 9 elemsFrom))
  Window -> S.window [3] (S.fromList [5] (take 5 elemsFrom))
  Bcast -> S.stretch [3, 3] (S.fromList [3, 1] (take 3 elemsFrom))
  Scalar -> S.constant [3, 3] (sum (take 1 elemsFrom))
