# regime-3 micro-benchmark (the PR change is a mixed picture)

This branch (`speedup-strided-tovector`) changes `toVectorListT`'s
regime-3 fallback in `Data/Array/Internal.hs` — the per-element path
taken when the innermost dimension is strided, so no contiguous run
longer than one element can be sliced out. The commit before this one
replaces the fallback

    [vFromListN l $ toListT sh a]                       -- build/foldr list

with a `vGenerate` over a linear-index-to-offset computation (per-element
`quotRem`). It was meant to speed that path up everywhere. This
benchmark shows it does not: it is a **mixed picture** — a win on some
shapes, a loss on others — so the change is not a general improvement and
this branch is kept as evidence rather than for merging.

## What it does

`Main.hs` replicates orthotope's `T` representation and its `toListT`
faithfully (specialised to `Storable Double`, horde-ad's element
storage), then compares four regime-3 strategies in one binary — the
real orthotope compiles only one at a time, so a replica is the only way
to A/B them:

    list         current fallback: vFromListN l . toListT
    gen-quotrem  this branch's change: vGenerate + per-element quotRem
    gen-unsafe   gen-quotrem with unsafeIndex, to price the bounds check
    unfold-add   unfoldrExactN with an additive odometer state (no division)

Each shape is checked to actually take regime 3 (`regimeOf`) and all four
strategies are asserted to produce identical vectors before timing.

## Running it

Self-contained (base + vector + criterion):

    cd micro-regime3 && cabal run micro          # ~10 min, 5s per bench
    cd micro-regime3 && cabal run micro -- -L1   # ~2 min, rougher
    cd micro-regime3 && cabal run micro -- vgg   # one group by name prefix

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

24 conv-derived shapes: the patch tensor, per image, laid out
`[outH, outW, Cin, KH, KW]` — the per-image `[nAh, nAw, nCinp, nKh, nKw]`
of the patch tensor above, renamed to the conventional axes (output
spatial, input channels, kernel) — and its per-position `[Cin, KH, KW]`
slices, with dims from real nets — kernels 3×3 (VGG/ResNet, horde-ad's own CNN),
5×5 (LeNet), 7×7 (ResNet stem), 11×11 (AlexNet); channels 1/3 up to 512;
spatial from horde-ad's 6/12/24 to ImageNet's 224/112/56/28/14/7. Six
further shapes (`stretch-*`) are not conv-derived — extreme rank, extreme
aspect ratio, non-power-of-two dims, a cache-hostile innermost stride —
to probe the space beyond convolution. See `convShapes`/`stretchShapes`
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
memory-hungry — the startup correctness check alone builds all four
strategies' vectors at once. `Cin` and the spatial dims scale `l` linearly too (in the
full run, doubling `Cin` ~doubles the cost, quadrupling the spatial area
~quadruples it), but reducing them reproduces a shape already here — a
per-position slice, or a smaller conv — so `nImgs` is the only dimension
genuinely free to drop.

## Results

criterion, GHC 9.12.4, -O1, means; representative rows. `q/l` is
`gen-quotrem / list`: below 1 the change wins, above 1 it loses.

| shape                          | list     | gen-quotrem | unfold  | q/l  |
|--------------------------------|----------|-------------|---------|------|
| cnn-L1-24x24-c1  [24,24,1,3,3] | 117 µs   | 178 µs      | 154 µs  | 1.51 |
| lenet-L1-28-c1-k5              | 380 µs   | 637 µs      | 447 µs  | 1.67 |
| cifar-L1-32-c3-k3              | 620 µs   | 915 µs      | 731 µs  | 1.48 |
| gather48-src-50  [50,3,3,50]   | 438 µs   | 616 µs      | 523 µs  | 1.41 |
| resnet-stem-112-c3-k7          | 34.1 ms  | 43.3 ms     | 35.3 ms | 1.27 |
| alexnet-L1-55-c3-k11           | 19.3 ms  | 25.7 ms     | 20.5 ms | 1.33 |
| stretch-rank10  [3×10]         | 1.38 ms  | 3.06 ms     | 1.58 ms | 2.21 |
| vgg-28-c256-k3                 | 67.7 ms  | **42.2 ms** | 44.5 ms | 0.62 |
| vgg-14-c512-k3                 | 33.0 ms  | **21.4 ms** | 22.5 ms | 0.65 |
| deep-7-c512-k3                 | 7.79 ms  | **5.56 ms** | 5.55 ms | 0.71 |
| alexnet-L2-27-c48-k5           | 30.0 ms  | 20.7 ms     | **18.0 ms** | 0.69 |
| stretch-wide-2xM  [2,1000000]  | 42.6 ms  | **21.3 ms** | 48.8 ms | 0.50 |
| stretch-square-1400            | 33.1 ms  | **21.7 ms** | 32.3 ms | 0.65 |

Over all 30: `list` fastest on 17, the change (`gen-quotrem`/`gen-unsafe`)
on 11, `unfold-add` on 2.

## Reading the results

- The change **loses** on the small, shallow, high-rank shapes — where
  the per-element `quotRem` count (one per dimension) dominates and `l`
  is modest. That is horde-ad's own CNN, LeNet, CIFAR, and the gather48
  layout, and most steeply the rank-10 stretch (2.2×). End to end in
  horde-ad's `bench/ConvVjpBench.hs` (this branch's orthotope wired in),
  the gather chains — 48-spatial, 3-channel, exactly this region —
  regress ~1.5–2.1× while the pure-scatter control is unchanged.
- The change **wins**, by up to ~2×, on the large mid-network layers with
  many channels (VGG/ResNet 256–512-channel 3×3) and on low-rank bulk
  transposes, where `l` is large and the list's per-element allocation
  dominates the few divisions.
- `gen-unsafe == gen-quotrem`: the bounds check is free (predicted /
  hidden under ILP); the division is the whole cost difference from
  `list`.
- `unfold-add` is division-free but its immutable odometer state
  allocates per step, so it rarely beats either of the others outright.

## Why the change is not the fix

Whichever pure-Haskell strategy wins a given shape, none closes the gap
to the stride-aware C kernels — roughly an order of magnitude on
comparable traffic: horde-ad's concrete *scatter*, which routes through
those kernels, runs the analogous chain in ~0.5 ms in `ConvVjpBench`
where the fastest gather strategy is several ms. Regime 3 has no
contiguous runs to hand a bulk kernel, so the transfer stays per-element
in Haskell no matter how the fallback is written. The win must move the transfer into C — the
client-side add-zero gather, or an upstream normalize-in-C /
strided-copy kernel — which is why this pure-Haskell change is kept as
evidence, not merged.

## Further untested ideas

Two pure-Haskell variants this benchmark does not settle, recorded here
so the branch is self-contained:

- A fusion-friendly `Vector` class method (in the spirit of vector's
  `unfoldrExactN`) that steps a multi-index by stride additions — no
  `quotRem` — so stream fusion collapses the strict state to a register
  loop, still behind a pure API. This is *not* the `unfold-add` strategy
  above: that uses an allocating immutable-list odometer (a proxy that
  loses), so the truly fused, allocation-free form is unmeasured.
- Tightening *regime 2* (innermost-normal, not exercised here) with a
  `toVectorT` that folds the contiguous runs directly instead of
  building the intermediate run list.

Both are pure Haskell, so the [C-gap](#why-the-change-is-not-the-fix)
above bounds them: they could shift the mixed picture but cannot bring
regime 2/3 within reach of the stride-aware C kernels.
