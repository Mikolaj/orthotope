# regime-3 micro-benchmark (the fix: bq-expand)

This branch (`speedup-strided-tovector`) changes `toVectorListT`'s regime-3
fallback in `Data/Array/Internal.hs` — the per-element path taken when the
innermost dimension is strided, so no contiguous run longer than one
element can be sliced out.

The previous attempt, benchmarked as `gen-quotrem` resulted in
a **mixed picture**: it had replaced the original `list` fallback

    [vFromListN l $ toListT sh a]                       -- build/foldr list

with a `vGenerate` over a per-element `quotRem` (one division *per
dimension*), which sped up the large, many-channel shapes but *slowed* the
small, shallow, high-rank shapes that dominate horde-ad's convolutions (up
to ~2×).

The fix now in `Data/Array/Internal.hs` is **`bq-expand`**: precompute the
base-offset of each innermost run once — the outer-base grid is separable
(`o0 + sum idx_d * stride_d`), so it is built by iterated `concatMap` /
`enumFromStepN` expansion, no division and no thunk-list — then fill the
result with a single `vGenerate` doing **one** `quotRem` per element. It
beats the original `list` fallback on every benchmarked shape with no
regression and needs no extension to orthotope classes.

A direct mutable result buffer is faster still (`mut-odo`/`build`, ~1.5×
over `bq-expand`), but only by adding a new `Vector`-class method. This was
measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal ([below](#the-mutable-ceiling-not-taken)).

## How the strictly positive picture was achieved

Four findings turned the mixed picture into `bq-expand`:

1. **Split off the innermost dimension and price the outer multi-index
   once per run, not once per element.** The first attempt's per-element,
   per-*dimension* `quotRem` was the whole cost on the small high-rank shapes;
   precomputing an `m`-element base-offsets table drops the output to
   one `quotRem` per element (`m` = number of runs = `product (init sh)`).
2. **The build of run base-offsets is itself the remaining cost, and it is a
   separable grid** — so `concatMap`/`enumFromStepN` builds it with no
   division and no lazy cons-list, which a `foldl'`-over-a-`build`-list
   does not fuse away. That is `bq-expand`'s edge over `offsets-quot`.
3. **Strictness bangs on the hot loop are performance-essential, not
   cosmetic** — the `quotRem` result tuple and the loop invariants — worth
   ~2× on their own (unbanged, the odometer/output accretes thunks). They
   are copied into `Data/Array/Internal.hs`.
4. **A hardened harness makes the ranking trustworthy** — criterion `env`
   (input built once, forced to NF, excluded from timing), `NOINLINE` on
   the benchmark-facing functions (so no result is hoisted out of the
   timed loop), and the agreement check moved to a separate `check` mode
   (so it never shares a computation, via CSE, with the benchmark). Under
   this harness the ranking is stable and every time scales with `l`, so
   nothing is being optimised away.

## What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT`
faithfully (specialised to `Storable Double`, horde-ad's element storage),
then compares 20 regime-3 strategies in one binary — the real orthotope
compiles only one at a time, so a replica is the only way to A/B them.

The originals and the first attempt:

    list         original fallback: vFromListN l . toListT (lazy cons-list)
    gen-quotrem  first attempt: vGenerate + per-element quotRem (one per rank)
    gen-unsafe   gen-quotrem with unsafeIndex, to price the bounds check
    unfold-add   unfoldrExactN with an allocating immutable-list odometer

The **run base-offsets family** — identical output (one `vGenerate` with one
`quotRem` per element, reading a precomputed `m`-element run base-offsets
table); they differ *only* in how that table is built:

    offsets-quot base-offsets via fromListN . runBaseOffsets (a lazy build/foldr list)
    bq-unfold    base-offsets via VS.unfoldrExactN (pure-typed, immutable-list state)
    bq-gen       base-offsets via VS.generate + one quotRem per run
    bq-mut       base-offsets via a VS.create mutable odometer (concrete Int scratch)
    bq-expand    base-offsets via iterated VS.concatMap expansion   <-- SHIPPED
    bq-expand-zf bq-expand with the zip and fold fused into one recursion
    bq-expand-b  bq-expand seeded from the first dim's enumFromStepN

Whole-offset / alternative-gather variants:

    backperm     build the full l-length offset vector, then unsafeBackpermute
    cm-gather    fused map . concatMap gather (no output quotRem at all)
    all-expand   full offset grid via concatMap expansion, then map gather
    offtab       full offset table via a mutable odometer, then vGenerate gather

Direct mutable result-buffer fills (need a class extension / mutation):

    mut-odo      walk the outer odometer, write each run with a tight
                 additive inner loop straight into the result buffer
    mut-offsets  as mut-odo but iterating the precomputed run base-offsets list
    build        mut-odo through vBuildVS, a prototype of the one new Vector
                 method such a fill would need (prices the abstraction)

    concat-runs  class-methods-only: per-run vGenerate + vConcat (mirrors
                 the regime-2 branch, but with strided runs)

The `check` mode (below) asserts all 20 strategies produce byte-identical
vectors on all 30 shapes, and that each shape actually takes regime 3.

## Running it

Self-contained (base + vector + criterion + deepseq):

    cd micro-regime3 && cabal run micro              # ~50 min, 5s per bench
    cd micro-regime3 && cabal run micro -- -L1       # ~10 min, rougher
    cd micro-regime3 && cabal run micro -- check     # correctness only, fast
    cd micro-regime3 && cabal run micro -- diag      # per-build allocations
    cd micro-regime3 && cabal run micro -- vgg       # one group by name prefix

Add `--regress allocated:iters` to a benchmark run for reliable per-call
allocations (well-conditioned at 5s).

## Where the shapes come from

The benchmarked shapes are regime-3 arrays as horde-ad's shaped `conv2d`
produces them: it compiles to an im2col patch gather
(`CommonShapedOps.slicezS` builds a `[1, nCinp, nKh, nKw]` patch per
output position of `[nImgs, nCout, nAh, nAw]`), whose strided view is
normalized through `toVectorListT`. The patch depends on the image and
the two spatial positions but not on the output channel (it is shared
across output channels, which enter only the later dot), so the patch
tensor is `[nImgs, nAh, nAw]` × `[nCinp, nKh, nKw]`.

In general the source's transposes merge into that view, so its innermost
dimension is strided and normalizing it takes regime 3 — which is the
input `mkStrided` builds (see its comment in `Main.hs` for how).

## The shape set

The conv-derived shapes: the patch tensor, per image, laid out
`[outH, outW, Cin, KH, KW]` — the per-image `[nAh, nAw, nCinp, nKh, nKw]`
of the patch tensor above, renamed to the conventional axes (output
spatial, input channels, kernel) — and its per-position `[Cin, KH, KW]`
slices, with dims from real nets — kernels 3×3 (VGG/ResNet, horde-ad's own CNN),
5×5 (LeNet), 7×7 (ResNet stem), 11×11 (AlexNet); channels 1/3 up to 512;
spatial from horde-ad's 6/12/24 to ImageNet's 224/112/56/28/14/7. The
`stretch-*` shapes are not conv-derived — extreme rank, extreme aspect
ratio, non-power-of-two dims, a cache-hostile innermost stride, a run
length of one element, a base-offset table as long as the result — to
probe the space beyond convolution. See `convShapes`/`stretchShapes`
in `Main.hs` for the full list.

## Dropping the minibatch dimension

The minibatch dimension `nImgs` is dropped — every shape is for one
image. It never appears in a regime-3 array anyway: when the whole patch
tensor is normalized at once (`stoVector`) `nImgs` is a leading
dimension, so a minibatch scales that call's `l` linearly (the rank-5
shapes); when each position's `[Cin, KH, KW]` slice is normalized
separately (`mvecsWritePartialLinear`) `nImgs`, with `nAh, nAw`, is an
outer position, so a minibatch scales the number of calls, not each `l`
(the `*-slice` shapes). Either way total regime-3 work is linear in the
minibatch size (`nImgs` = 7 in horde-ad's own CNN; tens to a few hundred
in general training).

`tooBig` (in `Main.hs`) lists realistic layers excluded because even one
image's patch tensor (7M–29M elements) makes a run too long and
memory-hungry. `Cin` and the spatial dims scale `l` linearly too (in the
full run, doubling `Cin` ~doubles the cost, quadrupling the spatial area
~quadruples it), but reducing them reproduces a shape already here — a
per-position slice, or a smaller conv — so `nImgs` is the only dimension
genuinely free to drop.

## Results

Run 5: criterion, GHC 9.12.4, -O1, hardened harness (`env`, `NOINLINE` on
the benchmark-facing functions, separate `check` mode). **Time** is the
geomean over every shape of the per-shape mean ÷ `list`'s mean (below 1 =
faster than the original fallback). **Alloc** is bytes allocated per call as
a multiple of the result vector (`8·l`), from the `--regress allocated`
fit on `vgg-28-c256-k3`. Fastest first.

| strategy        | time ×list | alloc ×result | needs                      |
|-----------------|-----------:|--------------:|----------------------------|
| mut-odo         |      0.115 |          1.0× | class extension / mutation |
| build           |      0.125 |          1.0× | new `Vector` method        |
| offtab          |      0.133 |          2.0× | mutation                   |
| bq-expand-b     |      0.170 |          4.2× | nothing (pure)             |
| bq-mut          |      0.172 |          1.3× | mutation                   |
| **bq-expand**   |  **0.173** |      **4.2×** | **nothing — SHIPPED**      |
| bq-expand-zf    |      0.174 |          4.2× | nothing (pure)             |
| offsets-quot    |      0.241 |          6.7× | nothing (pure)             |
| mut-offsets     |      0.293 |          7.6× | mutation                   |
| bq-unfold       |      0.312 |         10.2× | nothing (pure)             |
| bq-gen          |      0.366 |          4.7× | nothing (pure)             |
| all-expand      |      0.446 |         12.6× | nothing (pure)             |
| fused           |      0.465 |         20.7× | concrete `Int` scratch     |
| backperm        |      0.550 |         18.4× | nothing (pure)             |
| concat-runs     |      0.576 |         11.2× | nothing (class-only)       |
| cm-gather       |      0.679 |         23.2× | nothing (pure)             |
| unfold-add      |      0.983 |         29.9× | nothing (pure)             |
| list (baseline) |      1.000 |         27.7× | —                          |
| gen-unsafe      |      1.082 |         13.0× | —                          |
| gen-quotrem     |      1.100 |         13.0× | 1st attempt                |

`bq-expand-b`, `bq-mut`, `bq-expand` and `bq-expand-zf` are a four-way tie:
they span 2% here, and their order differs between runs. The table is sorted
because a table has to be, not because it ranks them; what separates them is
the `needs` column, and that is what the choice rested on.

## Reading the results

- **The output method: `vGenerate` + one `quotRem` wins.** Every
  run base-offsets-family strategy (`bq-*`, `offsets-quot`) uses it
  and lands ahead of the fancier gathers — `fused`'s `unfoldrExactN` (0.467),
  `backperm` (0.559), `cm-gather` (0.680), `all-expand` (0.446).
  A single in-order `vGenerate` fuses tighter than a stepped `unfoldrExactN`
  state or a two-pass build-then-gather, and its per-element `quotRem`
  is hidden under the scattered read.
- **The base-offsets build decides within that family, and `concatMap` wins the
  pure builds.** Same output, only the `m`-element table build differs:
  `concatMap` (`bq-expand`, 0.173) ties the explicit mutable fill (`bq-mut`,
  0.172) and beats the lazy list (`offsets-quot`, 0.241), `unfoldrExactN`
  (`bq-unfold`, 0.312) and `generate`+per-run-quotRem (`bq-gen`, 0.366).
  The list route pays for a non-fusing cons-list of thunks; `concatMap`
  builds the separable grid inside vector's stream framework instead. So
  `bq-expand` is the fastest build that needs neither a class extension nor
  explicit mutation.
- **`bq-mut` ties `bq-expand` on time but allocates far less** (1.3× vs
  4.2× the result) — a mutable `Int` scratch vs `concatMap` intermediates
  — at the cost of explicit mutation; `bq-expand` is the pure choice.
- **The `bq-expand` variants add nothing.** `bq-expand-zf` (zip and fold
  fused into one recursion) and `bq-expand-b` (first-dim special-case) tie
  `bq-expand`, here and on the shapes chosen to separate them; the zip list
  is only rank-1 long and `foldl'` is already well-tuned, so there is
  nothing to gain. `bq-expand` is kept as the plainest form.
- **`gen-quotrem` (the first attempt) is still slower than `list`** (1.100)
  — the mixed picture, reproduced: one `quotRem` per *dimension* per
  element costs more than the list's allocation on the shapes that matter.
- **Allocation:** `bq-expand` allocates ~4.2× the result vector (`concatMap`
  intermediates over the `m`-element base-offsets); `offsets-quot` ~6.7×
  (the cons list); the direct mutable fills ~1.0× (just the result); `list` ~28×
  (thunks). Lower allocation tracks lower time across the table.

## Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes added
last — chosen to push past the ranges the rest cover, and named here without
their prefix — against the strategies nearest the decision, each as a
multiple of `list` on the same shape:

| shape      | bq-expand | bq-expand-b | bq-expand-zf | build | offsets-quot |
|------------|----------:|------------:|-------------:|------:|-------------:|
| inner1     |     0.196 |       0.165 |        0.182 | 0.227 |        0.457 |
| tall-Mx2   |     0.106 |       0.106 |        0.106 | 0.054 |        0.106 |
| coprime-r7 |     0.140 |       0.141 |        0.142 | 0.077 |        0.162 |
| rank12     |     0.376 |       0.384 |        0.394 | 0.316 |        0.472 |
| tab16MB    |     0.195 |       0.189 |        0.189 | 0.170 |        0.289 |

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is the only shape where
  `bq-expand` beats `build`, and the only one where `bq-expand{,-b,-zf}`
  take the top three of the twenty, ahead of every mutable strategy. Its
  innermost extent is 1, so each base offset covers a single element: the
  odometer that `mut-odo`/`build` step has nothing to amortize over, while
  the expansion build has no per-element odometer to begin with. At the
  other end `stretch-tall-Mx2` has an innermost extent of a million, and
  `build` wins by 2×. The geomean reports that second case and averages the
  first away, which is why this table is here.
- **Per-shape figures are far noisier than the geomean: trust the first
  digit only.** Two independent runs of these shapes agree within 1–5% on
  most cells, but differ by 15% on `stretch-rank12/build` and 27% on
  `stretch-inner1/bq-expand-b`, and the order of `bq-expand{,-b,-zf}` within
  their sweep of `stretch-inner1` flipped between them. The sweep itself
  reproduced in both runs; which of the three led did not.

## The fix in Data/Array/Internal.hs

Regime 3 now builds the run base-offsets by expansion and fills with one
`vGenerate`:

    runBaseOffsetsT o0 osh oats = foldl' expand (VU.singleton o0) (zip osh oats)
      where expand !acc (!nd, !sd) = VU.concatMap (\a -> VU.enumFromStepN a sd nd) acc

    -- in toVectorListT, innermost-strided branch:
    let !sInner = last sh
        !tInner = last ats
        !baseOffsets = runBaseOffsetsT ao (init sh) (init ats)     -- unboxed Int scratch
        gen i = case i `quotRem` sInner of
          (!q, !r) -> vIndex v (VU.unsafeIndex baseOffsets q + r * tInner)
    in  [vGenerate l gen]

The run base-offsets live in an unboxed `Int` vector — index scratch,
independent of the abstract element storage `v` — so the only new dependency
is a qualified `Data.Vector.Unboxed` import (already a library dependency).
The bang patterns are performance-essential, ported from the benchmarked
`bq-expand` (finding 3 above).

Validation on this branch:

- orthotope's own test suite: **407/407 pass** (Dynamic/Ranked/Shaped ×
  boxed/storable/unboxed).
- Non-vacuity: deliberately dropping the `r * tInner` term fails 63 cases,
  among them `transpose_2/4/5/6`, `stride_1`, `rev_1/2` — so the pass is not
  vacuous.
- This benchmark: all 20 strategies agree with `list` on all 30 shapes.

End-to-end confirmation in horde-ad's `bench/ConvVjpBench.hs` (wiring this
branch's orthotope in and rebuilding ox-arrays + horde-ad) is not yet run;
the numbers above are from the replica.

## The mutable ceiling (not taken)

The `bq-*` strategies still fill the result one element at a time. The
tightest possible shape drops to a **mutable result buffer**: allocate it
once, walk the outer odometer, and write each innermost run with a tight
additive inner loop — no `quotRem`, no base-offsets table, no per-element step.
That is `mut-odo` (0.118), `build` (0.127) and `offtab` (0.134) — ~1.5×
over `bq-expand`, allocating essentially just the result vector.

The catch is the API: a buffer filled across runs cannot be expressed by
the per-element `vGenerate`; it needs a new `Vector`-class method exposing
a fill. `build` prices exactly that — `mut-odo` driven through `vBuildVS`, a
prototype of

    vBuild :: Int -> (forall s. (Int -> a -> ST s ()) -> ST s ()) -> v a

— and matches `mut-odo` on every shape, so **the class method is free**
(it inlines to the identical loop). A pure-typed alternative (a
strided-gather method taking the shape/stride/source and hiding the
mutation inside each instance, as `vGenerate` already does) would keep the
speed without `ST` in the signature.

This was **deliberately not taken.** Orthotope keeps its `Vector` API pure
and minimal, and a ~1.5× gain over `bq-expand` (pure-Haskell either way, so
[the C-gap](#the-c-gap-still-a-deeper-ceiling) bounds both) did not justify
a new class method across all four instances. The strategies stay here as
the measured evidence for that ruling, so it is not re-proposed.

## The C-gap: still a deeper ceiling

`bq-expand` is a pure-Haskell win over the fallback, but no pure-Haskell
strategy closes the gap to the stride-aware C kernels — roughly an order of
magnitude on comparable traffic: horde-ad's concrete *scatter*, which
routes through those kernels, runs the analogous chain in ~0.5 ms in
`ConvVjpBench` where the fastest gather strategy here is several ms.
Regime 3 has no contiguous runs to hand a bulk kernel, so the transfer
stays per-element in Haskell no matter how the fallback is written.
Closing that gap needs the transfer moved into C — the client-side
add-zero gather, or an upstream normalize-in-C / strided-copy kernel.
`bq-expand` is the incremental pure win to take meanwhile, not a
replacement for that work.

## Further ideas

The truly-fused allocation-free odometer is the `fused` strategy (it
works, but loses to `bq-expand` here), and the faster-still mutable fill is
`mut-odo`/`build` ([above](#the-mutable-ceiling-not-taken), measured but
not taken). One pure-Haskell idea remains untested:

- Tightening *regime 2* (innermost-normal, not exercised here) with a
  `toVectorT` that folds the contiguous runs directly instead of building
  the intermediate run list.

Being pure Haskell, it is bounded by the
[C-gap](#the-c-gap-still-a-deeper-ceiling)
above: it could sharpen regime 2 but cannot bring it within reach of the
stride-aware C kernels.
