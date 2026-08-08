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

A direct mutable result buffer is faster still: on Run 7 (Harness) `mut-odo`
is 1.51× over `bq-expand`, and `mut-odo-vecdims` — the same fill with its
dimension lists replaced by unboxed vectors — is **2.35×**, the fastest
strategy measured here. Both need a new `Vector`-class method, which was
measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal — a bar an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-not-taken), amended).

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure one is **`bq-scan-packed-mulback`**, 0.097
against `bq-expand`'s 0.127; the fastest pure one carrying **no size
precondition at all** is `bq-scan-rem-gm-mulback` at 0.119. None is what
`Data/Array/Internal.hs` does today, and the trade-offs — preconditions,
allocation, and a noise floor of about 3% — are in [Results](#results) and in
[the Lemire section](#lemire-multiplicative-inverses-at-the-two-division-sites).

Every figure on this page is **net of the shared forcing pass** every strategy
is timed through, which Run 6 (-O1) is the first run licensed to subtract
([sum-only](#sum-only-and-the-correction-now-applied)). That makes none of
them comparable to a figure from an earlier run, or to one from a later run
that does not subtract it.

Every figure is also **one population's**. The measured ones above are the
main set's — the positive-stride views a merged transpose builds — while the
regime-3 views the library's other operations produce (reversed, broadcast,
sliced, windowed, scaled) are the [stride
classes](#the-stride-classes-and-what-they-cover), each its own population,
run in its own process and tabled beside the main set rather than folded into
it.

## Contents

- [The goal of these benchmarks](#the-goal-of-these-benchmarks)
  - [How the strictly positive picture was achieved](#how-the-strictly-positive-picture-was-achieved)
  - [Where the shapes come from](#where-the-shapes-come-from)
  - [The shape set](#the-shape-set)
  - [Dropping the minibatch dimension](#dropping-the-minibatch-dimension)
  - [The stride classes and what they cover](#the-stride-classes-and-what-they-cover)
  - [The scratch vector flavour](#the-scratch-vector-flavour)
  - [One element type, and what the probe found](#one-element-type-and-what-the-probe-found)
  - [Lemire multiplicative inverses, at the two division sites](#lemire-multiplicative-inverses-at-the-two-division-sites)
  - [Per shape, where the geomean hides the ordering](#per-shape-where-the-geomean-hides-the-ordering)
  - [The fix in Data/Array/Internal.hs](#the-fix-in-dataarrayinternalhs)
  - [The mutable ceiling (not taken)](#the-mutable-ceiling-not-taken)
  - [The C-gap: still a deeper ceiling](#the-c-gap-still-a-deeper-ceiling)
  - [Dead ideas](#dead-ideas)
- [About the current harness](#about-the-current-harness)
  - [What the benchmark does](#what-the-benchmark-does)
  - [Running it](#running-it)
  - [Making a major benchmark run](#making-a-major-benchmark-run)
  - [The reader: read-run.py](#the-reader-read-runpy)
  - [The noise floor is 3%, not the CI](#the-noise-floor-is-3-not-the-ci)
  - [R2 is the ramp detector, not the noise detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now applied](#sum-only-and-the-correction-now-applied)
  - [Non-urgent TODO list](#non-urgent-todo-list)
- [About the last run (Run 7)](#about-the-last-run-run-7)
  - [Results](#results)
  - [What Run 8 compares against](#what-run-8-compares-against)
  - [The claims Run 8 should test](#the-claims-run-8-should-test)
  - [The stride classes, run by run](#the-stride-classes-run-by-run)
  - [Provenance](#provenance)
  - [What the next runs have to decide](#what-the-next-runs-have-to-decide)

## The goal of these benchmarks

**Nothing in this chapter changes from run to run.** It changes when the
harness changes radically, or when a ruling here is refuted — and a ruling
refuted is a paragraph rewritten, not a figure updated. What it holds is why
these shapes and not others, why these strategies and not others, which
designs were tried and died, and what all of it was for: [the fix in
`Data/Array/Internal.hs`](#the-fix-in-dataarrayinternalhs), which is the goal
the rest of this file exists to have reached. Figures do appear here, inside
rulings that rest on them, and those are re-quoted when a run moves them; the
*rulings* are not re-verified each run.

Those rulings are architecture decision records in all but format — context,
decision, consequence, and an evidence trail that makes them re-openable
rather than merely re-readable. The prose form is kept deliberately, since the
evidence is the point and a template tends to shed it. What the resemblance is
worth is a warning about growth: if the rulings outgrow the chapter, the ADR
answer is one record per file with an explicit *status* — and the thing to
carry over would be that field, since what this page keeps getting wrong is
not stating a ruling but noticing when a later measurement has superseded
one.

### How the strictly positive picture was achieved

Four findings turned the mixed picture into `bq-expand`. **Price the outer
multi-index once per run, not once per element**: an `m`-element base-offsets
table (`m = product (init sh)`) drops the output to one `quotRem` per element,
where the first attempt paid one per *dimension* per element, which was the
whole cost on the small high-rank shapes. **Then the table build is what
remains, and it is a separable grid**, so `concatMap`/`enumFromStepN` builds
it with no division and no lazy cons-list — a `foldl'`-over-a-`build`-list
does not fuse away, and that is `bq-expand`'s edge over `offsets-quot`.
**Strictness bangs on the hot loop are performance-essential**, worth ~2× on
their own, and are carried into `Data/Array/Internal.hs` with the logic.

**While this was achieved, the harness had to be hardened** — criterion `env`
employed to move input construction outside the clock, `NOINLINE` so no
result is hoisted out of the timed loop, and the agreement check in a separate
`check` mode so it cannot share a computation with the benchmark via CSE.
Under it the ranking is stable and every time scales with `l`, so nothing is
being optimised away.


### Where the shapes come from

The benchmarked shapes are regime-3 arrays as horde-ad's shaped `conv2d`
and other programs produce them: it compiles to an im2col patch gather
(`CommonShapedOps.slicezS` builds a `[1, nCinp, nKh, nKw]` patch per
output position of `[nImgs, nCout, nAh, nAw]`), whose strided view is
normalized through `toVectorListT`. The patch depends on the image and
the two spatial positions but not on the output channel (it is shared
across output channels, which enter only the later dot), so the patch
tensor is `[nImgs, nAh, nAw]` × `[nCinp, nKh, nKw]`.

In general the source's transposes merge into that view, so its innermost
dimension is strided and normalizing it takes regime 3 — which is the
input `mkStrided` builds (see its comment in `Main.hs` for how). Other
operations reach regime 3 by other routes, and those are the
[stride classes](#the-stride-classes-and-what-they-cover), populations of
their own beside this one.


### The shape set

The conv-derived shapes: the patch tensor, per image, laid out
`[outH, outW, Cin, KH, KW]` — the per-image `[nAh, nAw, nCinp, nKh, nKw]`
of the patch tensor above, renamed to the conventional axes (output
spatial, input channels, kernel) — and its per-position `[Cin, KH, KW]`
slices, with dims from real nets — kernels 3×3 (VGG/ResNet, horde-ad's own CNN),
5×5 (LeNet), 11×11 (AlexNet); channels 1 up to 512; spatial from horde-ad's
6/24 to AlexNet's 55.

The `stretch-*` shapes are not conv-derived — extreme rank, extreme aspect
ratio, non-power-of-two dims, a cache-hostile innermost stride, a run
length of one element, a base-offset table as long as the result, a
page-aliasing power-of-two stride, and a mid-range innermost extent — to
probe the space beyond convolution. See `convShapes`/`stretchShapes`
in `Main.hs` for the full list.

**The conv set was halved after Run 6, and the shapes that went are not to
come back one at a time.** A strategy sees a shape as its innermost extent
`sInner`, its rank and its `l`, and nothing else — not which paper the dims
came from — and each dropped shape duplicated a kept one on all three while
costing a proportional share of every run. The freed wall clock went to A/A
controls, which calibrate every other figure and were the roster's scarce
resource. The halving moved the published geomean and the ratios between
strategies past the noise floor — a change of population and not of any
strategy, which is why Run 7 was read against Run 6 restricted to the
surviving shapes. The
ruling, and the two shapes that must survive any later cut for a reason
unrelated to their workload, sit at `convShapes` in `Main.hs`, beside the
list.


### Dropping the minibatch dimension

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
image's patch tensor exceeds `sizeCap`, the element count that partitions
benchmarked shapes from flagged ones: past it a call is slow enough to
starve the sample count, and the run is long and memory-hungry with it.
`Cin` and the spatial dims scale `l` linearly too (in the full run, doubling
`Cin` ~doubles the cost, quadrupling the spatial area ~quadruples it), but
reducing them reproduces a shape already here — a per-position slice, or a
smaller conv — so `nImgs` is the only dimension genuinely free to drop.


### The stride classes and what they cover

`mkStrided` transposes the two innermost dims of a dense array, so every
stride the main set carries is positive and its offset is zero. The library
reaches regime 3 through other operations too — its two commonest inputs of
that kind among them, a broadcast being stride 0 and `rev` negative — and the
**stride classes** are one population per producing operation, named by the
prefix that selects them: `rev` (every stride negated, offset at the top),
`revsome` (a strict subset reversed, so the signs are mixed), `bcast` (an
innermost stride of 0, every run re-reading one element), `bcastmid` (the
stretched axis in the middle instead), `reshape1` (the `[n] -> [n, 1]` trap,
innermost extent 1), `slice` (a view of a larger source, so a non-zero offset
with positive strides), `window` (overlapping im2col patches — the workload
this page opens by naming, carrying the overlap that the main set's bijective
index map drops) and `scaled` (superincreasing strides, none of them 1). Each
is a short list in `Main.hs`, reusing a main-set shape where one fits so that
a class figure has a positive-stride counterpart to stand next to; each
generator's comment there says what it models, and the comment heading them
all, above `mkRev`, carries the coverage argument — a hypothesis about what a
valid hand-built view can recombine, not a theorem — which is not repeated
here. *Class* unqualified means one of these; the other sense on this page
always keeps its noun, *method* — a `class method`, the class-method tier,
or in full a `Vector`-class method.

Two rulings govern how they are measured and published, both taken
2026-08-07, ahead of the implementation:

- **Each class is its own pinned population**, published beside the main
  geomean and never folded into it. The geomean is a ranking statistic over a
  pinned set and a change of population moves it, as the conv-set halving
  measured; there is no combined figure to compute, so a sentence comparing
  populations compares their tables. One process per class follows from the
  same ruling, and `read-run.py` enforces it — it names the population it
  read, fails a file spanning two, and refuses to emit a table for one.
- **No strategy is excluded from any class.** Every one is to be fixed to
  work on all of them, seen failing first wherever the failure can be fired.
  The see-it-fail run found nothing to fix: the Int32 strategies' partial sums
  are each the offset of a real element, in-bounds for any valid view whatever
  the stride signs, so the feared failure cannot fire below a 2^31-element
  source — `int32Fits`'s own unfireable case. What mixed signs did break was
  the packed scan's assert — a corner formula, maximal only for positive
  strides, with no lower bound, its claimed maximum observed sitting below a
  real entry of `revsome-mid-cnn-L2`'s own base-offsets table — fixed at the
  builder, the numbers and the argument recorded at the assert and both Int32
  comment sites.

**A class population is two or three shapes**, against the main set's
two dozen, which is deliberate — the classes are there to vary the
*mechanism*, and varying size and rank within one is the main set's job —
but it decides how their results read. A class geomean rests on two or three
cells, so it is a summary of a handful of numbers rather than a statistic
over a spread; the per-shape figures are nearly the whole population and are
worth quoting where the main set's would be flattened away; winsorizing has
almost nothing to cap and `--pair`'s bootstrap interval almost nothing to
resample. What a class run can decide is whether an *ordering* inverts under
its mechanism and whether any strategy's `worst` crosses 1 there. What it
cannot do is be compared with a main-set number, in either direction.


### The scratch vector flavour

Every table this suite builds — the `m`-element base-offsets of the `bq-*`
family, the `l`-element offset tables, the odometer's dimension vectors —
used to live in a **Storable** `Int` vector, because the payload is Storable
and nothing said the scratch had to follow. The fallback in
`Data/Array/Internal.hs` builds an **unboxed** one, deliberately: index
scratch is independent of the abstract element storage `v`, and the section
above says so in as many words. Nobody had noticed that the arm labelled
*shipped* in the results table therefore measured a vector flavour the shipped
code does not use, and no figure on this page had ever priced the difference.

The probe that settled it, 2026-08-08 at -O1: a twin differing from
`bq-expand` in the table's flavour and in nothing else, in the roster slot
beside it, five arms over the whole shape set so the correction rode along.
Paired, which is what a margin measured per shape wants:

| | unboxed vs Storable |
|---|---:|
| paired geomean | **0.9433** |
| 95% interval | 0.9103..0.9817 |
| shapes won | 19 of 24, sign p 0.0066 |
| `worst` cell | 0.302 against 0.369 |
| `alloc` | 3.11x against 3.15x |

**The unboxed table is 5.7% faster, roughly twice the floor**, its interval
clears 1, and it wins on the worst shape by more than it wins on the geomean.
Allocation is unmoved, so this is speed and not volume — the same bytes, held
differently, by a mechanism nothing here measured and the probe does not
need. The one shape it loses is `stretch-square-1341`, which
was the worst-measured shape of both runs and is this page's standing warning
about reading a single cell.

**It was measured twice, with the arms' roles exchanged**, which is why the
figure is quoted flatly rather than hedged. The first run put an unboxed twin
beside a Storable roster, on a machine with other work on it, and read 0.9377
(interval 0.9081..0.9690); the second put a Storable twin beside an unboxed
roster — after the conversion below, so the roster was by then the other
flavour — on a quiet machine, and read 0.9433. They agree to 0.6%, inside the
floor, winning on the same 19 shapes of 24, and their tables agree to three
digits on `alloc` and to two on `worst`. A margin that survives exchanging
which arm is the twin, the machine's load and the direction of the change is
the code's and not the harness's.

**So every scratch vector here is now unboxed, matching what ships.** Three
arms keep a Storable table and must: `backperm` hands it to
`unsafeBackpermute`, `cm-gather` and `all-expand` to `map`, and each of those
takes one vector family, so for them the table's flavour *is* the payload's
and unboxing it would change the strategy rather than its scratch. They are
the new-pure-`Vector`-method tier, and that is the same fact seen from the
other side. `strideOffsets` and `baseOffsetsExpandVS` exist for exactly those
three and say so.

Run 7 (Harness) is the first run to measure the converted suite, so the
tables now say what the library actually does. On the shapes the two runs
share, `bq-expand` moved by −6.3% against the probe's −5.7% — the prediction
met at full budget — while the family did not move as one:
`bq-scan-packed-mulback` came out 4% *slower*, spread evenly over the shapes,
and `mut-odo-vecdims`, whose dimension vectors were Storable when its 0.051
was taken, read 0.056 on those same shapes — neither priced by a probe that
had measured the `m`-table's flavour and not theirs.

**Both were put to a twin probe, 2026-08-08 at -O1**, each twin differing
from its base in that flavour alone and sitting in the slot beside it, ten
arms over the whole shape set with `list` and both `sum-only` halves so the
correction rode along. Paired, and restricted to the 22 shapes the two runs
share, which is the basis the two moves above were stated on:

| | the flavour's own effect |
|---|---:|
| `mut-odo-vecdims` / its Storable-dims twin | **0.9658** (0.9528..0.9793), 17 of 22 |
| `bq-scan-packed-mulback` / its Storable-table twin | **1.0369** (1.0243..1.0520), 0 of 22 |

**The packed scan's 4% is the flavour; the vecdims arm's is not.** Unboxing
that table costs `bq-scan-packed-mulback` 3.7%, on every shape of the set and
by a margin matching what the conversion was seen to cost it — the one arm
the conversion hurt, and unexplained. The dimension vectors go the other way:
unboxed is 3.4% *faster*, so the conversion was worth −3.4% to
`mut-odo-vecdims` and removing the suspect deepens its move to about +13%.
What is left is position and code layout, which only a full roster can
separate. Allocation is identical within each pair, as two build-identical
arms must be. The probe's own gates: the `sum-only` halves agreed at 0.9991
and the term scaled 1.03× across the set, while its one in-situ arm read
0.982; with no A/A pair in the process its floor is Run 7's, which both
margins clear.


### One element type, and what the probe found

Everything timed here is `Storable Double`, horde-ad's element storage, while
the fallback all of it justifies is polymorphic over the `Vector` class *and*
the element type. What the element changes is the copy — its width sets how
many elements a cache line holds, and the instance sets what a write costs —
and what it does not change is the index arithmetic, which is the only thing
the strategies differ in. So the question was never whether the magnitudes
move but whether the **ordering** does, and whether the shipped arm stays
under `list` at every instance the library serves.

The probe, run 2026-08-08 at -O1 on the desktop this page's other figures come
from: three arms — `list`, `bq-expand` and `mut-odo-vecdims`, spanning the
list, the per-element generate and the run copy — over six shapes chosen to
span `sInner` and `l`, one process per type, by `cabal run probe -- f32` and
its siblings. Three further points, each varying one thing against `Storable
Double`: `Storable Float` is the same instance at half the width, unboxed
`Int` the same width in another instance, `Storable Word8` the same instance
at the narrowest width there is. Each figure is that type's own geomean
against that type's own `list`:

| element type | `bq-expand` | worst | `alloc` | `mut-odo-vecdims` | worst |
|---|---:|---:|---:|---:|---:|
| `Storable Double` | 0.189 | 0.317 | 3.73x | 0.084 | 0.112 |
| `Storable Float` | 0.189 | 0.321 | 3.23x | 0.095 | 0.137 |
| unboxed `Int` | 0.187 | 0.321 | 3.72x | 0.080 | 0.116 |
| `Storable Word8` | 0.193 | 0.322 | 2.85x | 0.073 | 0.106 |

**The ordering holds at every type, and the shipped arm is never close to
`list`.** `bq-expand` spans 3.2% across the four, about the floor, and its
`worst` — the column that answers what a geomean cannot — sits between 0.317
and 0.322, so on no shape of any type did it come within three times of the
fallback it replaced. That is the property that had to hold for every
instance, and it holds with room to spare and almost no variation, across an
eightfold range of element width and two `Vector` instances.

**What does not hold is the tidy width story.** `mut-odo-vecdims` is not
monotone in width: `Float` (0.095) is *worse* than `Double` (0.084) though its
elements are half the size, while `Word8` (0.073) is the best of the four.
That is a property of the measurement and not a stray cell — it reproduced on
two independent runs, before and after the probe became a program of its own —
and it is unexplained. It is also nowhere near an inversion, so it bears on
the width intuition rather than on any ruling here.

Three cautions on the table. It is **uncorrected** — a probe carries no
`sum-only` bench — so every column is compressed toward 1 by the forcing pass;
that cannot flip an under-1 verdict, the correction only moving a ratio
further from 1, and it falls on all three arms of a type alike. The `alloc`
column divides by `8*l` whatever the element, so a narrower type reads low by
exactly the result vector's own share: predicted 0.50x below `Double` at
`Float` and 0.875x below at `Word8`, observed 3.23x and 2.85x against 3.73x —
both to the digit, which makes that column a consistency check as much as a
caveat. And three arms over six shapes is a probe, not a run.

**These figures are the probe's own.** `Probe.hs` is a separate program with
its own transcribed arms — all four types, `Double` included, so that none of
them is served by the roster's originals while the others run copies and a
difference could be an artifact of the copying. The price is that its
`bq-expand` is bq-expand-*shaped* rather than the roster's, so a figure here
never belongs beside one from a run. Its six shapes are copies too, and those
*are* held to `Main.hs`'s own dims by `--lint`, which is not a hypothetical
guard: three of the six were transposed when first written and the check named
all three.

**So one element type stays, and generalising the suite stays refused** — now
on evidence rather than on cost alone. The cost argument is unchanged and is
under [what the benchmark does](#what-the-benchmark-does); what has changed is
that the coverage it buys is measured. Boxed elements are deliberately absent,
and not for cost — their elements are thunks, so each arm would defer a
different share of its copy into the forcing sum and the fill/forcing split
every figure on this page rests on would not hold. Probing boxed needs a
design of its own, not another duplicate.


### Lemire multiplicative inverses, at the two division sites

The idea (arXiv 2012.12369): precompute `M = floor(2^64/d) + 1` once per
divisor, then `n div d` is the high word of `M*n` and `n mod d` the high word
of `(M*n)*d` — two 64×64→128 multiplies instead of a division. It is
implementable purely, through GHC's `timesWord2#`, so unlike the mutable fills
it needs no new `Vector` method. That is what made it worth trying: a pure
strategy that could move the family without touching orthotope's classes.

A run base-offsets strategy divides in two places, and the answer is opposite
at each. Both benchmarks below are one-line substitutions of `fastQR` for a
`quotRem` against a control already in the table, so each measures its site
and nothing else.

**At the per-element output site it wins**, by 6.0%.
`bq-expand-lemire-out` is `bq-expand` with the shared `i quotRem sInner`
replaced, the table build held at `baseOffsetsExpand`. Other pure strategies
have passed it since, and the substitution itself still pays: faster than its
control on 22 shapes of 24, and the published columns agree with the
per-shape geomean, so no part of it rests on the warm-up ramp. One exception
is `stretch-square-1341`, the
run's worst-measured shape — read it as the shape, not the strategy. The
other is `stretch-pow2stride`, new to the set — and not the power-of-two
`sInner`, which `stretch-inner256` shares while being this arm's best cell.
Two controls back the
result. Its allocation is identical to `bq-expand`'s on every shape, which is
what a build-identical arm must show; and it runs *before* `bq-expand` in the
group where `bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot bias
would flatter one and penalise the other and cannot produce both.

**At the per-dimension build site it loses by 35%.** `bq-gen-lemire` is
`bq-gen` with the per-run, per-rank `quotRem`s replaced, and it is 1.352×
slower, faster on no shape of the set. The shape of the loss says why: it
tracks *rank*, not element count, rising from a few percent on the rank-2
shapes to over half at ranks 7 through 12. The cost is paid per
dimension, so the division was never what dominated there. Two reasons.
(i) The paper's win assumes you want a quotient *or* a remainder; an odometer
decomposition wants both, so the trick pays twice and collects once — where
`quotRemInt#` is one `idiv` yielding both. (ii) The magic table is a third
list to walk in step with `nts` and `sts`, adding a dereference and a pattern
match per dimension to the very loop whose per-dimension work was the target.
Rank 2 costs least because there is only one dimension to walk, though not
nothing.

What separates the two sites is (i) and (ii): at the output the divisor is a
loop invariant, so `M` is computed once for the whole fill with no list beside
it, and the per-element work really is one division against two multiplies.
The win is 6.0% rather than several-fold because the hardware has moved since
the paper — 64-bit `idiv` on this Zen 3 is ~14–19 cycles against the 40–90
that made the trick famous.

Two things a Core dump settled that source reading had got wrong. Both are
recorded because both were argued the other way first. **`quotRem` on `Int` is
not one instruction**: GHC wraps `quotRemInt#` in two guard branches, for a
zero divisor and for the `minBound quot (-1)` overflow, both on a
loop-invariant divisor — so the `d == 1` guard `fastQR` needs is not the
asymmetry it looked like, the baseline carries two of its own. And **the first
`fastQR` spent three multiplies where the algorithm needs two**, taking the
quotient from `timesWord2# m n` and then recomputing the low half as a
separate `timesWord# m n` when the one `timesWord2#` already yields both.
Fixing that is what turned the output site into the win it now measures, and
it recovered part of the build site's loss too — enough to see, nowhere near
enough to reverse it. Why the low half must not be recomputed is
recorded as a comment on `fastQR`, so the loose form is not written again.

**On shipping it.** `bq-expand-lemire-out` is pure, so the argument that kept
`mut-odo` out (a bar then, a weight since the mutable ceiling's amendment)
does not apply; what it costs is `MagicHash` and `UnboxedTuples`
in `Data/Array/Internal.hs`, about a dozen lines of helper, and a
precondition. The precondition is the substantive part: Lemire's identity
holds for `d, n < 2^32`, and `n` here is the linear output index, so a shipped
version needs an `l < 2^32` test choosing between the two fills —
loop-invariant and chosen once per call, but it must be there, since orthotope
does not otherwise cap array length. Weigh 6.0% against that; this
benchmark's job is to price it, not to decide it.


### Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes — chosen
to push past the ranges the rest cover, and named here without their prefix —
against the strategies nearest the decision, each as a multiple of `list` on
the same shape. These are Run 7 (Harness)'s own figures, all of them net of
the forcing pass like the rest of the page:

| shape      | bq-expand | bq-expand-b | lemire-out | mut-odo | vecdims |
|------------|----------:|------------:|-----------:|--------:|--------:|
| inner1     |     0.178 |       0.135 |      0.158 |   0.204 |   0.098 |
| rank12     |     0.305 |       0.301 |      0.297 |   0.250 |   0.121 |
| wide-2xM   |     0.154 |       0.121 |      0.144 |   0.137 |   0.072 |
| coprime-r7 |     0.101 |       0.101 |      0.091 |   0.042 |   0.033 |
| pow2stride |     0.062 |       0.062 |      0.076 |   0.063 |   0.063 |
| primes     |     0.085 |       0.085 |      0.078 |   0.025 |   0.029 |
| inner256   |     0.066 |       0.066 |      0.047 |   0.016 |   0.017 |
| tall-Mx2   |     0.076 |       0.076 |      0.066 |   0.020 |   0.025 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which is
the axis the orderings turn on; the fuller per-shape record is in
[What Run 8 compares against](#what-run-8-compares-against).

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is where the expansion family does best against
  the odometer fills: `bq-expand` (0.178) and `bq-expand-b` (0.135) beat
  `mut-odo` (0.204) and `build` (0.289), which they do on no other shape here
  — `stretch-pow2stride` excepted, where the two families converge outright
  (0.062–0.063 across expansion and odometer alike).
  Its innermost extent is 1, so each
  base offset covers a single element: the odometer that `mut-odo`/`build`
  step has nothing to amortize over, while the expansion build has no
  per-element odometer to begin with. At the other end `stretch-tall-Mx2` has
  an innermost extent of half its length and the ordering inverts completely —
  `mut-odo` 0.020 against `bq-expand` 0.076, with every mutable strategy
  ahead of every pure one. The geomean reports that second case and averages
  the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry: that
  `stretch-inner1` is *the only shape where the pure expansion strategies beat
  every mutable one*, with the four `bq-expand` variants taking the top four
  slots. They no longer do. `mut-flat` takes that shape at 0.025,
  `bq-mut-runs-mulback` at 0.026 and `bq-mut-runs-gm-mulback` at 0.029, with
  `mut-odo-vecdims` at 0.098 — all ahead of every expansion variant —
  strategies that did not exist,
  or were not rostered, when the claim was written. The unit innermost extent
  still explains why `mut-odo` and `build` do badly there; it never implied
  that no mutable fill could.
- **Per-shape figures are far noisier than the geomean: trust the first
  digit only.** Independent runs of these shapes agree within 1–5% on most
  cells but differ by up to 27% on `stretch-inner1/bq-expand-b` — runs
  whose rosters also differed, making the
  [roster effect][floor] a candidate cause — and the order of
  `bq-expand{,-b,-zf}` within their sweep of `stretch-inner1` flips between
  runs. The sweep itself reproduces; which of the three leads does not.
  `stretch-square-1341` is this run's standing warning on the point: again
  the worst-measured shape of the set, one of the two where
  `bq-expand-lemire-out` loses (the Lemire section names the other), and it
  stays in the column, its influence capped. That margin survives
  this caveat, being the whole shape set wide rather than one cell.
- **But check for a structural reason before discounting a cell as scatter,
  and check `stretch-inner1` in particular.** It is the shape whose innermost
  extent is 1, so a strategy that special-cases or elides a unit dimension
  behaves differently there *by construction*, and a striking figure is then
  the design showing through rather than noise. Two in `Main.hs` already do:
  the mul-back output hoists `s == 1` out of its loop entirely, and
  `baseOffsetsScan` elides unit dims, which on this shape leaves one real
  radix so no carry ever fires and the scan degenerates to a sequential fill.
  Both are now in the tables, and on that shape both sit far from their own
  averages: `bq-scan-packed-mulback` reads 0.136 there against a 0.097
  geomean, among its half-dozen worst cells of 24, while `bq-mut-runs-mulback`
  reads 0.026
  against 0.072 — its best cell of all 24. Read that cell first and average it
  away last.

All three bullets are measured on positive-stride views. The
[stride classes](#the-stride-classes-and-what-they-cover) put the same axis
under other mechanisms — `bcast`'s innermost stride of 0 has every run
re-read one element whatever its extent, `reshape1`'s extent is 1 by
construction, `scaled-rank1-m1` is a single run — so each class run is a test
of whether `sInner` still decides, and a class table that contradicts this
ruling is a finding to write up rather than a cell to average away.


### The fix in Data/Array/Internal.hs

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
- Non-vacuity: deliberately dropping the `r * tInner` term fails the suite at
  `transpose_2/4/5/6`, `stride_1` and `rev_1/2` among others — so the pass is
  not vacuous.
- This benchmark: every strategy agrees with `list` on every shape, the
  [stride classes](#the-stride-classes-and-what-they-cover) included, so the
  agreement covers negative, mixed-sign, zero and overlapping strides and not
  only the positive ones the main set carries.

End-to-end confirmation in horde-ad's `bench/ConvVjpBench.hs` — wiring this
branch's orthotope in and rebuilding ox-arrays + horde-ad — has been done and
is reported in that repo, not here.


### The mutable ceiling (not taken)

The `bq-*` strategies still fill the result one element at a time. The
tightest possible shape drops to a **mutable result buffer**: allocate it
once, walk the outer odometer, and write each innermost run with a tight
additive inner loop — no `quotRem`, no base-offsets table, no per-element step.
That is `mut-odo` (0.084) — 1.51× over `bq-expand` —
and `mut-odo-vecdims` (0.054), which is 2.35× over it and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.110) does not go that far — its output is an ordinary
`vGenerate` and only its `l`-sized `Int` offset table is filled mutably, so it
needs no class method, just a mutable scratch — and Run 7 puts it 31% behind
`mut-odo` for it, where Failed Run 6 had the two tied. On these numbers it is
no longer the cheap way to most of the gain.

The catch is the API: a buffer filled across runs cannot be expressed by
the per-element `vGenerate`; it needs a new `Vector`-class method exposing
a fill (or the `Storable`-only `unsafeCast` escape the amendment below
records). `build` prices exactly that — `mut-odo` driven through `vBuildVS`, a
prototype of

    vBuild :: Int -> (forall s. (Int -> a -> ST s ()) -> ST s ()) -> v a

— and Run 6 had it matching `mut-odo` on every shape, so **the class method
was free there** (it inlines to the identical loop). Run 7 (Harness) broke
that identity, `build` reading 1.24× behind `mut-odo` paired and slower on 22
shapes of 24, on cells whose own CIs are hundredths of a percent, with
neither arm's source changed between the two binaries.

**The Core says the identity holds and the gap was the measurement.** Dumped
from Run 6's source and Run 7's against one pinned dependency set,
`$wfbBuild` and `$wfbMutOdo` are the same worker in both binaries —
byte-identical once GHC's numbering is normalised, with `vBuildVS` surviving
as no top-level binding in either — and the two sources differ only by the
`Strides` newtype's zero-cost cast, which falls in both arms alike, so
neither binary is the odd one out. Nor is a dependency: `vector` and
`criterion` have been the same versions across those runs. A probe then
failed to reproduce the gap at all — in a binary relaid out by two inserted
arms the pair reads 1.004 paired (0.976..1.032, 11 shapes of 22), 1.24×
falling outside its whole per-shape range. So **the signature is free**, and
no `vBuild` is to be held back on Run 7's figure; what produced that figure
is unsettled, position and code placement both being live and `mut-odo` being
the noisiest bench of the set. A pure-typed
alternative (a
strided-gather method taking the shape/stride/source and hiding the
mutation inside each instance, as `vGenerate` already does) would keep the
speed without `ST` in the signature.

This was **deliberately not taken.** Orthotope's `Vector` API was to stay
pure and minimal, and the gain over `bq-expand` (pure-Haskell either way, so
[the C-gap](#the-c-gap-still-a-deeper-ceiling) bounds both) did not justify
a new class method across all four instances. The strategies stay here as
the measured evidence for that ruling — since amended below: the evidence
now prices the option instead of closing it.
`mut-odo-vecdims` keeps the stake high rather than settling it: the fill's
real cost was the odometer's cons-list traffic, not the fill itself, and Run
7 (Harness) prices the class-method tier at 2.35× over `bq-expand`. Against
that, the best pure strategy reaches 0.097, so the gap the class method would
buy is 1.80×, not 2.35× — which is the figure the ruling turns on.

**Amended 2026-08-07: the bar is now a weight.** The tree itself carries a
precedent this section did not weigh: `Data/Array/Internal/FastReshape.hs`,
a `runST` flattener over this same fallback territory — structurally
`mut-odo`, an allocate-once mutable result filled through an outer odometer
recursion with a per-element strided inner copy loop, its outer offsets
stepped additively where `mut-odo` multiplies — which sidesteps the `Vector`
class altogether by `unsafeCast` to `Double`/`Float` on element size. So
neither mutability nor needing a new class method *disqualifies* a strategy
any longer. What keeps both as weights against one is that FastReshape.hs is
not in use — absent from the cabal file, and still declaring its source
project's module name and imports (`CoreCompiler.ArrayReshape`;
`Utils.Misc`, `CoreCompiler.Error`), so it does not even compile in place:
precedent for writing such a module, not for shipping one. A mutable or
class-method strategy is now priced against that weight rather than refused
at the door.


### The C-gap: still a deeper ceiling

**Everything in this document lives under this ceiling.** Every strategy in
the table, every ruling resting on one, and every margin the ~3% floor
adjudicates are rearrangements *within* pure Haskell — and no pure-Haskell
strategy closes the gap to the stride-aware C kernels. Measured on the
analogous chain (horde-ad's interleaved A/B of 2026-07-31, recorded in that
repo): concrete *scatter*, which routes through them, runs it in ~0.5 ms,
and the gather over this branch's fix takes 2.55× that in its natural
orientation, 1.32× in its fastest — a 1.3–2.6× gap, down from the order of
magnitude the released fallback showed. What a C strided copy would leave
of it is unmeasured.

Regime 3 has no contiguous runs to hand a bulk kernel, so the transfer stays
per-element in Haskell however the fallback is written. Closing it needs C.
`bq-expand` is the pure win to take meanwhile, not a replacement for it.
This is discussed further in the horde-ad repo.


### Dead ideas

Ideas that **died on paper**, recorded so they are not re-proposed:

- **Delta-compressing an offset table** (storing Int8/Int16 steps, mostly
  the constant `tInner`, instead of absolute offsets) fails `vGenerate`'s
  contract: the callback is random-access, and recovering an absolute
  offset from deltas is a prefix sum — a scan the callback would redo per
  element.
- **Reordering the expansion so the largest outer dimension expands last**
  (to shrink the `concatMap` intermediates, whose sizes are the prefix
  products of the expansion order) has no freedom to spend: the table must
  be indexed by the row-major run index, so the expansion order is fixed by
  the output order.
- **Fusing the base-offsets build into the output fill** — the output reads
  the table at `q = i div sInner`, which ascends monotonically, so the two
  passes could stream in lockstep; but the callback would then carry
  odometer state, and a stateful fill is exactly what the mutable ceiling's
  class extension exists to provide — so since that ceiling's amendment
  this idea is priced with it, not dead outright. The table exists because
  `vGenerate` is stateless.
- **Caching the table across calls** (horde-ad normalizes the same shapes
  over and over) — `toVectorListT` is a pure per-array function with
  nowhere to keep a cache.
- **Padding the innermost extent to a power of two**, so the output
  division becomes shift-and-mask — padding changes the enumeration the
  contract fixes, and conv's inner extents are 3/5/7/11.
- **A separate `q`-table** (`qtab[i] = i div sInner`, in Int32) — strictly
  dominated by `offtab32`, which stores the finished offset for the same
  traffic.
- **Software-prefetching `v` from inside the callback** (which may legally
  read the offset table ahead of `i`) — GHC's prefetch primops all thread
  `State#`, so a pure callback cannot issue them without an unsafe escape.
- **`constructN` instead of `scanl'` for the prefix-sum build** (its
  callback legally reads the already-built prefix) — the scan fuses, so
  the fallback is moot, and it loses regardless: the recurrence reads
  `table[q-1]` back through a store-to-load forward where the scan carries
  the sum in a register, each step passes a freshly wrapped prefix slice,
  and the one power `scanl'` lacks — deltas depending on earlier *values*
  — is power a position-only delta never uses. Prefix access cannot even
  cheapen the carries: `table[q] = table[q - suffixProduct c] + st_c`
  still needs the same divisibility cascade to find `c`.
- **A branchless delta select in the scan build** (folding the carry
  correction in arithmetically instead of branching) — the branch's
  outcome is periodic with period `sInner`, which a modern predictor
  learns, so the branch is already ~free.
- **Unrolling the scan by `sInner`** so the carry test runs once per run —
  `sInner` is not a compile-time constant, and GHC will not unroll a loop
  by a runtime value.
- **Alternatives to the Granlund–Montgomery form for an unbounded output
  quotient.** For a stateless output loop with a runtime divisor that wants
  quotient and remainder both, the GM round-up magic is the end of the
  road. Barrett reduction's correction step is a *data-dependent* branch —
  a misprediction generator where GM's dispatch is loop-invariant;
  floating-point reciprocals cap the dividend at 2^53 and need an
  exactness proof plus FMA to be safe; a full-width 128-bit Lemire magic
  spends three multiply-highs, worse than the division it replaces. And
  the general GM form's 65-bit add-fixup never arises here: `Int`
  dividends spend only 63 bits, so a magic of width `63 + ceil(log2 d)`
  always fits one `Word` — one multiply-high and one shift per element,
  no bound on `l` (`gmMagic` in `Main.hs`).

## About the current harness

**This chapter normally does not change from run to run either**, but for a
different reason: it describes the instrument rather than any result. Every
generic instruction for making, reading and checking a run is here, and a
session told to make one can work from this chapter alone — but for the two
layouts a write-up pastes into, which sit beside the figures they explain:
the [Results](#results) columns and the
[per-class blocks](#the-stride-classes-run-by-run). What is *not* here
is anything a particular future run has to settle — that is
[What the next runs have to decide](#what-the-next-runs-have-to-decide), at
the end of the last chapter, because it goes stale as soon as that run
reports.

### What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT`
faithfully (specialised to `Storable Double`, horde-ad's element storage),
then compares the regime-3 strategies in one binary — the real orthotope
compiles only one at a time, so a replica is the only way to A/B them.

**One element type, where the fix serves them all.** Everything here is
`Storable Double`; the fallback is polymorphic over the `Vector` class and the
element type. Element width sets how many elements a cache line holds and
boxed elements change the copy entirely, so the *ranking* and not only the
magnitudes may differ for the instances the shipped code actually serves.
Nothing in the roster probes that; `Probe.hs`, a program of its own, does at
three further types and found the ordering unmoved —
[the probe](#one-element-type-and-what-the-probe-found) is the evidence this
restriction now rests on, boxed excepted.

**Don't generalise the suite to run every arm at every element type.** The
typing is the cheap part — the payload is only ever loaded and stored, all the
arithmetic being `Int`, so `T a` and a `Storable a` context would cost about
sixty lines of signature. What it would really cost is a run per type, and the
roster shared by both is what makes figures commensurable, so the choice is
between interleaving them — doubling the roster and re-collapsing the A/A
spans the crossed controls need — and two processes, whose comparison then
crosses processes and inherits the roster effect. The code cost is worse than
it looks too: `NOINLINE` on a polymorphic function blocks specialisation, so
every arm would time a dictionary rather than a fill unless roughly forty
`SPECIALISE` pragmas are added, **and each of those has to be confirmed in
Core** — an unverified one leaves the dictionary in place and the suite then
measures dispatch while reporting it as a strategy, which is the failure mode
that looks most like a result. Probe instead: a handful of shapes at one other
type, asking only whether the ranking inverts. The property that has to hold
for every instance is not the ranking but `worst` staying under 1 — never
slower than the fallback being replaced — and six shapes will show that.

The strategies are named here and *described* in `Main.hs`, each at its own
definition, where a reader meets the code the description is about. This list
is the index, in that file's definition order — base before variant, which is
also the order to read them in:

- **The originals and the first attempt.** `list` (the fallback being
  replaced: `vFromListN l . toListT`, a lazy cons-list), `gen-quotrem` (a
  `vGenerate` over one `quotRem` per *dimension* per element), `gen-unsafe`
  (that minus the bounds checks, to price them), `unfold-add` and `fused` (an
  `unfoldrExactN` odometer, allocating and then allocation-free).
- **The run base-offsets family**, all with the same output — one `vGenerate`
  doing one `quotRem` per element against a precomputed `m`-element table —
  and differing only in how that table is built: `offsets-quot` (lazy list),
  `bq-mut` and `bq-mut-runs` (mutable odometer), `bq-unfold`, `bq-gen`,
  `bq-gen-lemire` (Lemire at the build site; kept because it *lost*, so the
  idea is not re-proposed), `bq-expand` (**shipped**), `bq-expand-zf` and
  `bq-expand-b`.
- **The same family varying the per-element output instead**, which is the
  line every member ends in, so pricing it once prices it for all:
  `bq-expand-qr-prim`, `bq-expand-lemire-out`, `bq-expand-lemire-mulback`,
  `bq-expand32-lemire-mulback`, `bq-mut-lemire-out`, `bq-mut-lemire-mulback`,
  `bq-mut-runs-mulback`, `bq-mut-runs-gm-mulback`, `bq-scan-mulback`,
  `bq-scan-rem-mulback`, `bq-scan-gm-mulback`, `bq-scan-rem-gm-mulback`
  (the one pure composition with no size precondition anywhere),
  `bq-odo-mulback` and `bq-scan-packed-mulback`.
- **Whole-offset and alternative gathers**, which build an `l`-length offset
  vector rather than an `m`-length one: `backperm`, `cm-gather`, `all-expand`,
  `offtab`, `offtab32`, `offtab-scan`.
- **Direct mutable result-buffer fills**, which need a class extension or
  explicit mutation and are the [ceiling](#the-mutable-ceiling-not-taken):
  `mut-odo`, `mut-odo-vecdims`, `mut-offsets`, `build`, `mut-flat`. And
  `concat-runs`, class-methods-only, checked but no longer timed (below).

The order they are *run* in is deliberately a different one, fixed by `roster`
in `Main.hs`; the Results table below is sorted by time, a third. Sharing that
roster with the strategies, and not strategies themselves, are ten controls:
six A/A arms — `bq-expand-aa-adjacent` and `bq-expand-aa-distant`,
`bq-scan-mulback-aa-adjacent` and `bq-scan-mulback-aa-distant`,
`mut-odo-vecdims-aa` and `mut-odo-vecdims-aa-distant`, three strategies each
duplicated in both positions — the `sum-only-early`/`sum-only-late` pair, and
`bq-expand-nosum` and `mut-odo-vecdims-nosum`, each its base arm forced with
one element instead of the sum.
[The noise floor](#the-noise-floor-is-3-not-the-ci) and
[sum-only](#sum-only-and-the-correction-now-applied) say what each is for.

The `check` mode (below) asserts every strategy produces byte-identical
vectors on every shape, that each shape actually takes regime 3, and that the
view's innermost extent is the second-to-last dim as listed — which is the one
thing `read-run.py` has to assume, since no JSON carries the strided shape,
and which `m` and every `alloc` multiple rest on. The
[stride classes](#the-stride-classes-and-what-they-cover) go through the same
mode, each held to its own structural conditions — negative strides, mixed
signs, a stride-0 axis — with a deliberate-breakage proof per conjunct, and
each class list has its own reading of the innermost extent in the reader,
which `check` is again the only place to confirm. It is
built from that same `roster`, so a strategy cannot be timed without being
checked; what that leaves to go stale, `read-run.py --lint` holds — every arm
named here, every strategy defined in `Main.hs` rostered, each A/A control
running the arm its name duplicates, every control named as the reader's
own control test reads it, and every shape's `l` annotation agreeing with
what its list's rule computes.

`concat-runs` is the one strategy `check` covers and the benchmark does not.
It was by a clear margin the noisiest bench of the set — Failed Run 6's single
worst cell, and a median cell some 2.5× the shape's typical CI — so excluding
it costs no information the run needs, and it is one of the changes preceding
the current, quieter run, though nothing separates its contribution from the
others'.

The worry was never its own figures but its neighbours': every `time` is a
ratio to `list`, which runs first, so an aftermath outliving one bench would
tilt the group rather than cancel. The probes found nothing — its successor
timed the same after it as after a benign predecessor, and of the three A/A
pairs the one straddling it agreed best. What stays unprobed is the [roster
effect][floor], worth ~18% in horde-ad's `ConvVjpBench` and persisting for a
whole run rather than one bench: unretired rather than absent, since that
case ran benchmarks of a different scale.


### Running it

Self-contained (base + vector + criterion + deepseq):

    cd micro-regime3 && cabal run micro              # 5s per bench: hours
    cd micro-regime3 && cabal run micro -- -L1       # 1s per bench, rougher
    cd micro-regime3 && cabal run micro -- check     # correctness only, fast
    cd micro-regime3 && cabal run micro -- diag      # per-build allocations
    cd micro-regime3 && cabal run micro -- vgg       # one group by name prefix
    cd micro-regime3 && cabal run micro -- classes rev-   # one stride class
    cd micro-regime3 && cabal run micro --ghc-options=-fspec-constr
    cd micro-regime3 && cabal run micro --ghc-options=-O2 -- diag
    cd micro-regime3 && cabal run probe -- check     # the element-type probe
    cd micro-regime3 && cabal run probe -- f32       # one element type

`probe` is a second executable and not part of the roster:
[the element-type probe](#one-element-type-and-what-the-probe-found), whose
own header in `Probe.hs` says why it is a separate program and what its
separateness costs. Both are executables rather than benchmark stanzas, which
is what lets every mode above take its arguments directly — and what keeps a
bare `cabal bench` from launching a multi-hour run.

The `classes` mode replaces the main set with the
[stride-class](#the-stride-classes-and-what-they-cover) populations, one
selected per process by its name prefix; without a prefix it runs all of
them into one process, which is a probe and never a recorded run, the reader
declining to publish a table over two populations.

`cabal.project.freeze` pins the resolved plan — `vector`, `criterion`, `base`
and the rest, with an index-state — so that a recorded run's source commit and
its dependencies are both known. It postdates the earliest runs recorded here
and so cannot pin theirs; what covers those is a hand check that `vector` and
`criterion` have been the same versions since Failed Run 6 inclusive, which is
what lets a question about generated code be asked across those runs at all.
One pin is load-bearing rather than
housekeeping: `vector` is built `+boundschecks -unsafechecks`, which is what
makes the `gen-quotrem`/`gen-unsafe` pair price a bounds check at all, since
one uses `VS.!` and the other `VS.unsafeIndex`.

`micro.cabal` builds at -O1, the regime a default `cabal build` of orthotope
compiles under. Other regimes are command-line only, the flag landing
after the cabal file's so the later `-O` wins: `-fspec-constr`
when testing the `SpecConstr` optimization effect, `-O2` for the half
of the scan-fusion refutation that inverts there (a `diag` at `-O2`
is what measures it).

Those are all probes. A run whose numbers are meant to be kept and written
into this file is a different undertaking, and has a procedure of its own:
[Making a major benchmark run](#making-a-major-benchmark-run).


### Making a major benchmark run

A *major run* is the whole roster over the whole shape set at criterion's
default budget — the main set and, by default, **every stride-class
population with it**: one process for the main set, one per class, in the
order of the sequence below. Asking for a major run asks for all of them;
leaving a population out is an explicit exception to be stated, not a
choice this page leaves open. The whole is analysed and written into this
file. What follows is the procedure, and it is written to outlive any one
run.

**Where the effort actually goes, because it is not where it looks.** The
run is several hours and *unattended*; it costs patience and a quiet
machine, nothing else. Everything expensive happens after it, in the
write-up, and that is where a session's token budget is spent and where its
mistakes are made.
Two consequences worth having in mind before starting. Prefer analysis that
localises — per shape, per control — over re-quoting figures that moved a few
percent and changed nothing; the first is where the surprises have come from
and the second is what has gone stale twice.
And **a probe is not a lesser instrument than a major run**:
the measurements that closed the `sum-only` objection,
established that the forcing term scales, and settled the floor's mechanism
cost twenty minutes and, for the latter two, no extra machine time at all,
while the major run they hang off changed no decision.
A question with a discriminating measurement usually deserves a filtered
run now rather than a slot in the next full one.

**Where.** A session starts in `~/r/horde-ad`, which leaves *that*
repository's `CLAUDE.md` resident while this repo is not governed by it,
even though all generalizable preferences apply; read this file
and `read-run.py`'s docstring instead, orthotope carrying no
`CLAUDE.md` of its own. Then:

    cd ~/r/orthotope/micro-regime3

**Before spending the hours**, three cheap checks — in the run's own
`$REGIME`, since a regime change is a codegen change and agreement is what
would notice one going wrong:

    cabal build micro $REGIME
    cabal run micro $REGIME -- check   # every strategy agrees, every shape regime 3
    ./read-run.py --lint         # the roster and the shape annotations
    ./read-run.py --check-doc    # anchors, coverage, widths, stale figures

**Then confirm the regime is the one intended**, which nothing later can:

    cabal run micro $REGIME -- diag

and read one row of it — `baseOffsetsScan` against `baseOffsetsMut` on
`vgg-14-c512`. They are equal under SpecConstr and ten times apart at plain
-O1, a separation no eye misreads, and both ends of it are measured
(2026-08-08), the flag being the only thing that moves them. This costs the
seconds after a rebuild the flag forces anyway, and it is the only check
standing between a mistyped regime and a run that refutes the design it was
built to test.

**And one more, nearly free**, because everything above exercises the
*benchmark* while nothing exercises the *reader* until
hours later — at `-L1`, since the smoke tests the reader's code paths, not
its statistics:

    cabal run micro -- -L1 cnn-slice-c32 --json smoke.json   # every arm, one shape
    cabal run micro -- classes window-28x28-k5 -L1 --json smoke-class.json
    for f in smoke.json smoke-class.json; do
      for m in --selftest --aa --shapes --markdown --cells --fingerprint \
               "--pair bq-expand list" ""; do
        ./read-run.py $f $m >/dev/null || echo "BROKEN: $f $m"
      done
    done
    ./read-run.py smoke-class.json --block >/dev/null || echo "BROKEN: --block"
    rm smoke.json smoke-class.json

The first runs every roster arm on one shape and puts the whole analysis
path — the correction, the controls, the table generator — through its
paces; the second does the same for the `classes` plumbing, the reader's
per-list shape rules and the six-column class table, on the class whose
rule is least trivial. Both go through every mode, because the two files
take different paths through the reader from the population line onwards. A
reader broken by a roster or shape-list change fails here in minutes
instead of after the run.

**Run every mode, not the interesting ones.** The loop above is written as a
loop because a partial sweep has already missed a real break: after the trim
came out, `--pair` and `--aa` both died on a name that a removal had taken
with it, while `check`, `--lint`, `--check-doc` and `--selftest` all passed —
the failure lived in the two modes nobody had thought to run. Modes are cheap
to run and expensive to be missing, and the run artifact is the only thing
that can reproduce one, so sweep before deleting it rather than after.

**The run** is one sequence — the main set, then each stride-class
population in its own process, in `classViews`' order. Each `$c-` argument
selects a class by name prefix, the prefixes being disjoint by
construction (`bcast-` does not match `bcastmid-*`); one process per
population is the recorded protocol at `classBenches`, so no population's
figures owe anything to another's leftover heap state and each JSON is
single-population by construction. **The regime is a variable of the script,
not a flag to remember**: it goes before the `--` of every command alike, and
it is set once at the top beside the run's name, so that copying the script
carries the choice and leaving it empty is a deliberate act. A run made in
the wrong regime is not detectably wrong — the roster, the shapes, the gates
and the reader all pass, the JSON records no compiler flag, and the only
symptom is the regime's own effect failing to appear, which reads as a
refutation of the design rather than as a missing flag:

    R=RUN   # one name for the run's artifacts, e.g. run7
    REGIME=--ghc-options=-fspec-constr   # Run 8's; empty for plain -O1
    git log -1 --format=%h && git status --porcelain  # the write-up's commit
    uptime                                # quiet, or note what was not
    {
      date -Is
      cabal run micro $REGIME -- --json $R-main.json > $R-main.log 2>&1
      echo "main exit=$? $(date -Is)"
      for c in rev revsome bcast bcastmid reshape1 slice window scaled; do
        cabal run micro $REGIME -- classes $c- --json $R-$c.json > $R-$c.log 2>&1
        echo "$c exit=$? $(date -Is)"
      done
    } >> $R-wallclock.log 2>&1

Everything else is already a default. The allocation fit
`--regress allocated:iters` is on (it is well-conditioned at 5s), so `alloc`
comes out of the same process as the times rather than a side run; passing
`--regress` explicitly would replace it. Each process prints its own
provenance to stderr as it finishes — roster size, shape count, wall clock and
the two heap peaks — so a document quoting its scale copies a measured number
rather than counting benches by hand, and so `micro.cabal`'s `-M2G` headroom
claim has a current source; the stderr redirect above is what keeps it. In a
class process every part of that line is its own but the shape count, which
is fixed before criterion selects and so names the whole class set.

**Probes whose designs predate the run ride the same script.** The machine
is quiet for the whole sequence either way, so a question already on [the
open list](#what-the-next-runs-have-to-decide) with its measurement written
— a twin in a named slot, a filtered A/B — is appended after the classes
and answered the same day, pre-registered rather than improvised. What this
does not cover is the run's own surprises, which need the run read first;
those become that list's next entries, each with the probe that would
settle it.

**The time budget is always criterion's default.** Raising `-L` would buy
samples for the slowest shapes -- they bottom out around 6 where the fastest
get 130 -- but at a proportional cost in wall clock, and the runs are already
hours. Every recorded run therefore uses the default, so figures stay
comparable between runs and the sample counts in the tables mean the same
thing throughout. Where that leaves a shape thinly measured, the `smp` and
`CI%` columns say so rather than the budget hiding it.

Expect several hours for the sequence, so run it in the background — and
**run nothing else on this machine while it does**. Every strategy of a
population shares that population's process precisely so its figures are
commensurable, and the [noise
floor](#the-noise-floor-is-3-not-the-ci) section is the measured evidence that
they move with what shares that process. What the rest of the machine does on
top of that is unmeasured, and a recorded run is the wrong place to find out.
The session's own hands stay off the machine and the tree alike until the
sequence ends — the script's git lines are the binary's provenance, and an
edit under a running sequence falsifies them — while reading ahead costs
nothing: the last run's chapter and the open list are what the write-up is
about to need.

The wall-clock file is why the script stamps each process: a criterion log
is timestamped only at the end, so without the window there is no way to
say which shapes an intrusion exposed, and a suspicious cell
can then be neither blamed on it nor cleared of it. The exit codes ride
along because a class process that dies mid-sequence otherwise leaves a
truncated JSON behind a green scroll-back. Run 6 (-O1) had three
short greps in its first minutes and the exposure was settled from the cell
data instead — the anomalies were strategy-intrinsic, not a time window
([R2](#r2-is-the-ramp-detector-not-the-noise-detector)) — but that worked only
because the suspects sat at one roster slot on two shapes, which is luck and
not a method.

**After it lands**, in this order:

1. **Gate every population on the correction, before reading any figure.**
   `--selftest`
   checks that the forcing term scales with `l` — one pass over the elements,
   not something whose size varies with the shape — and `--aa` prints both
   whether the two `sum-only` halves agree and how the term compares with the
   same pass measured in situ, off the `-nosum` arms. The three are
   independent
   and the correction needs all of them: position, size, and the read itself,
   each blind to what the others catch
   ([sum-only](#sum-only-and-the-correction-now-applied)). Any of them failing
   invalidates the whole time column rather than merely leaving it
   uncorrected,
   and all have to be re-passed by every run rather than inherited — by every
   *population* too, each process carrying its own `sum-only` pair, its own
   six
   A/A controls and its own two `-nosum` arms, so a class run passes or fails
   the gates on its own evidence and a failure there invalidates that class's
   column and no other.
2. **Match bases before reading any ratio.** The first act of a comparison
   is making its two sides one basis — the same population, the same
   restriction, the basis a claim was stated on — and only then reading
   figures. Run 7's first claim check ran on its 24 shapes against claims
   stated on 22, and every pair had to be re-run.
3. Analyse with `./read-run.py`, which is where every table in this file
   comes
   from — read [the reader's own section](#the-reader-read-runpy) first, and
   do not write another reader.
4. **One JSON at a time, never merged.** The reader takes one file, and its
   geomean is that file's population — the main set's or one class's. Every
   mode names that population in its first line, `--selftest` fails a file
   spanning two and `--markdown` declines to emit a table for one, so a
   merged
   run is caught rather than published. The class tables stand beside the
   main
   geomean, per [the ruling](#the-stride-classes-and-what-they-cover), and
   there is no combined figure to compute, so a sentence comparing
   populations
   compares their tables.
5. Walk the list under [Provenance](#provenance) of what the new numbers
   replace, and do not trust it to be complete: re-run the two sweeps it
   names
   and map each hit to the bullet covering it, since running the sweeps is
   not
   the same as reading them, and the list has been wrong before. **Replace;
   do not annotate.** Walking a list of what to replace makes "now X, where
   it
   was Y" the natural sentence, and a superseded number has to earn its place
   by the test in the user-scope `CLAUDE.md` — would someone redo the work
   without it — which most do not meet; `--check-doc` lists the ones already
   here for adjudication. And a figure that moved *inside* the floor is
   requoted without comment — only a movement past the floor earns a
   sentence.
6. **Verify the write-up before deleting anything.** These are the checks the
   procedure used to leave to judgement, each of which has caught something:
   1. **derive every count and ratio in the prose from `--cells`, never by
      eye.** "32 of 33", "30th of its 33 shapes", "the only two past 7%" are all
      claims a glance at a sorted table gets wrong; two of Run 6's were wrong
      until recomputed;
   2. **reproduce any newly-derived column by a route that shares no code with
      the reader.** A four-bench filtered run carrying both `sum-only` halves
      takes seconds, and criterion's own printed `time` lines then give the
      ratio by hand: on `cnn-slice-c32`, `(1.506 - 0.1739) / (6.339 - 0.1739)`
      = 0.2161 against the reader's 0.216. Recomputing from `--cells` is worth
      doing too, but it shares the reader's arithmetic and cannot catch a wrong
      definition, only a wrong transcription;
   3. **paste `--markdown`'s output over the Results table**; do not edit the
      table. It renders the same rows the terminal does, and carries `needs`,
      `precondition` and the emphasis forward from the table already there.
      Its stderr is the whole of what is left by hand: a row new to the roster
      comes out with `?`, a departed row is dropped with a warning. Each class
      JSON emits its own table the same way and is pasted the same way, into
      its block in [The stride classes, run by
      run](#the-stride-classes-run-by-run); those come out six columns wide,
      `needs` and `precondition` being properties of a strategy rather than of
      a population and so stated in the main table alone. The per-shape
      fingerprint is pasted the same way, whole, from `--fingerprint`;
   4. **assemble the cross-class summary last, from the tables and not from
      the JSONs.** Every cell of it appears in one of the class tables above
      it, so it is a transcription and is checked as one — cell against table,
      each in turn — where recomputing it from the runs would be a second
      derivation able to disagree with the tables it summarises;
   5. **check that every `](#...)` resolves**, here and in `Main.hs`'s
      `README.md#...` references, and that every figure-bearing section is
      linked from the Provenance list. Findings rename headings, and a renamed
      heading breaks a link silently;
   6. **walk the diff against the writing rules as a check of its own, not
      only while writing.** The replace-list walk manufactures "now X, where
      it was Y", requoting a count in place preserves a sentence that should
      have lost its numeral, and a class paragraph's close invites a
      mechanism the run never measured. `--check-doc`'s figure sweep lists
      candidates, `Main.hs` comments included, but the redo test itself is
      the reader's. Run 7's write-up carried fifteen-odd such sentences past
      every green check here, found only when a reader asked;
   7. **read the document end to end.** The mechanical passes above do not catch
      a bullet contradicting the table three lines below it, which is how
      "`bq-mut` ties `bq-expand`" survived two runs beside a build ordering that
      refuted it. This is the pass that keeps finding real errors;

   Two conventions this page holds to, both of which exist because breaking
   them has cost something here. **A figure in prose names its run, its basis
   and its population, or it belongs in a table with the prose pointing at
   it** — a bare numeral carries no provenance, and that is how one sentence
   came to put a Failed Run 6 figure beside a Run 6 one, and another to compare
   a *published* ratio with a *paired* one. The population is the newest way to
   make that mistake and the easiest, a class figure and a main-set one being
   the same kind of number over different shapes. **An anchor longer than about
   thirty characters
   goes reference-style**, defined at the foot of the file: inline it overflows
   the width and the rewrapping that follows is pure churn;
7. Rebuild and re-run `--lint` and `check` after editing `Main.hs`, even when
   only comments changed: the reader parses that file for the roster and the
   shape dims, so a comment edit can break a check that passed before it;
8. Record beside the numbers the run's name and regime, each process's stderr
   provenance line, which machine, **and the commit the binary was built
   from** (the JSONs do not survive, so the source is the only thing that
   makes a run reproducible even in principle — this page's figures are one
   desktop's and are not portable, see [Provenance](#provenance)). A class
   process's line is measured for its elapsed time and its two heap peaks but
   not for its shape count: that count is fixed before criterion does the
   selecting, so it reads every class view rather than the population that
   ran, and the population's own size comes from the reader's first line;
9. **Only then**, and after asking the user, delete the artifacts —
   the JSONs, the logs and the wall-clock file alike.
   The normal state of this directory is no run
   artifact at all, which is decided rather than an oversight; the numbers live
   in this file and the artifacts do not. But "afterwards" means after the
   verification above is done, presented to the user and accepted,
   not after the writing: Run 6's artifact was deleted as
   soon as its write-up was drafted, which cost the ability to re-check
   anything needing the raw samples when the write-up was later questioned.


### The reader: read-run.py

Every figure below comes out of `read-run.py` in this directory, and the
table above is *emitted* by it rather than copied from it. **Use it; do not
write another reader.** The
definitions it encodes — which cells the column caps, that `CI%` is a mean
half-width rather than a bound, that `alloc` needs an `l` the JSON does not
carry (it parses `Main.hs` for it), that the `*-aa-*`, `sum-only*` and
`*-nosum` rows are
controls, that every ratio is net of the forcing pass while every other column
is raw — each cost a session to settle, and an ad-hoc script gets them
subtly wrong. Its docstring is the reference for all of them; extend the
script rather than starting over.

    ./read-run.py RUN.json                  # roster, then the strategy table
    ./read-run.py RUN.json --markdown       # that table as README markdown
    ./read-run.py RUN.json --shapes         # per shape: CI% max / median / mean
    ./read-run.py RUN.json --aa             # controls, spans, in-situ term
    ./read-run.py RUN.json --pair A B       # two arms, paired, with an interval
    ./read-run.py RUN.json --cells          # every cell as TSV, for the rest
    ./read-run.py RUN.json --fingerprint    # the kept per-shape record
    ./read-run.py RUN.json --block          # a class block's mechanical parts
    ./read-run.py RUN.json --selftest       # check the reader's own invariants
    ./read-run.py RUN.json --exclude concat-runs --exclude-shape deep-7-c512-k3
    ./read-run.py --lint                    # Main.hs's roster and shape
                                            # annotations, against README
                                            # and against itself

Every mode's first line names the run's **population** — the main set or one
[stride class](#the-stride-classes-and-what-they-cover) — which the reader
works out from the shape lists in `Main.hs`. It is the one property of a run
that no column shows and every figure depends on, so `--selftest` fails a
file spanning two populations and `--markdown` emits no table for one: a
geomean over two of them is a statistic of neither.

`--pair` compares two arms **shape by shape**, and it is the right way to
compare any two: a strategy's ratio to `list` spans six-fold across the shape
set, so an unpaired comparison of two table columns fights that spread, while
`A_s/B_s` does not — both arms move together with the shape. `list` cancels
out of it too, so a paired figure owes nothing to the baseline. It prints the
paired geomean, a bootstrap interval, the win count and its sign test, and the
published-column ratio beside them, those last two answering different
questions. **Reach for it instead of writing a script.** Every paired figure
this page quotes was once recomputed by hand and thrown away, which is how one
came to be printed beside a figure from a different run.

The interval wants multiplying before it is believed, and `--aa` says by how
much: the A/A pairs are the only comparisons whose true answer is known to be
exactly 1, so they are the only place an interval can be held to an answer.
`--aa` reports whether each covers 1 and how its half-width compares with the
spread the pairs actually show, which turns the floor from a threshold someone
chose into a factor a run measured. Read that factor as an order of magnitude:
it rests on six pairs.

`--markdown` renders the same rows the plain table does, from one shared
call, so the published figures cannot drift from the terminal's. It reads the
Results table already in this file for the two columns a run cannot know —
`needs` and `precondition` — and for which rows the prose emphasises, carries
those forward, and says on stderr what it could not: a strategy new to the
roster comes out with `?` to be written by hand, and one that has left it is
dropped with a warning. The arms added after Run 6 sat in exactly that
state until Run 7 timed them, which is what the mechanism is for.

**No run artifacts are kept here.** The normal state of this directory is no
JSON at all, and one is made when a question needs it — which is the same
moment the reader is wanted, so it is built to be useful on a partial run as
well as a full one:

    micro --json RUN.json                                    # the whole thing
    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

The second takes seconds and still exercises the reader; a one-shape run says
so. A filtered run
like it carries no `sum-only` bench, so its figures are uncorrected and not
comparable to the tables here — the reader warns on stderr when that is what
it is reading. Each run's JSON is gone when fully processed and the deletion
accepted by the user, so the tables in this document cannot be re-derived;
the next run replaces them.

`--lint` needs no run JSON at all, which is this directory's usual state. It
reads `roster` out of `Main.hs` — the one list both the benchmark and `check`
are built from — and asks the four things about it that go stale silently: is
every arm named somewhere in this file; is every strategy defined in
`Main.hs` rostered, so that none is left neither timed nor checked; does each
A/A control run the same function as the arm its name duplicates; and is
every control named as the reader's own control test reads it, since a
renamed one would enter the aggregates as a strategy. An arm rostered and
deliberately not timed is a note rather than a failure, that being the case
of `concat-runs`.

It asks a fifth about the shape lists rather than the roster: does every
entry's `l` annotation agree with what its list's rule computes, so that a
mistyped dimension or annotation is caught at edit time. `--selftest` had
that oracle first and still carries it, but only for the shapes a run's JSON
happens to hold — which for a class list is after that population's process
has finished, hours past the point where the check is worth anything.

And a sixth about a second file: do `Probe.hs`'s six copied shapes still
match the dims `Main.hs` gives those names. The probe is a separate program
and its shapes are copies (its header says why), so this is the one thing
standing between a transposed dim there and a probe measuring a shape it
still names after — which is not hypothetical, three of the six being wrong
when they were first written and named by this check.

The question it used to ask second — is every benchmarked strategy also held
to the reference by `check`? — is gone, and deliberately. The roster and the
agreement chain were two hand-written lists of the same strategies, and that
check compared them; one list now builds both, so the drift cannot happen
rather than being merely detectable. A check that cannot fail is a silent
search, so it was replaced rather than kept.

That is the standing rule for everything under `--lint`, `--selftest` and the
`health` warnings, and it is why each carries a recorded proof in its
docstring: **a new check is not finished until it has been made to fail on
purpose**, with what was broken and what it then said written down beside it.
Several here can only fail on data no real run produces — a forcing term
larger than the cell it is subtracted from, a term that does not scale with
`l` — so provoking them is the only way to know they are wired to anything.

`--selftest` checks invariants of whatever run it is given: that the dims it
parses out of `Main.hs` match that file's own `l` annotations, that every cell
has a positive slope and a sane R², that the forcing term is positive on every
shape and leaves every cell's net positive, that the same term scales with `l`
as one pass over the elements must, that every row's winsorized geomean
covers all shapes and lands inside its own per-shape range, that `list`
against itself is 1, and that an A/A pair with no capped cell has its
published ratio equal to its paired one. The one thing it still
cannot reach — that `sInner` is the second-to-last listed dim — it now names
as `check`'s rather than as nobody's. It names what it could
not exercise
rather than passing silently, and exits 2 when the run file is absent. That
last invariant is a finding: the A/A ratios in the noise-floor table are
geomeans over every shape, so a published ratio is the paired one whenever
neither arm had a cell capped. `--aa` prints both and `--selftest` asserts
the identity where it holds.


### The noise floor is 3%, not the CI

Six A/A controls run an existing strategy twice under a second name — three
strategies, each duplicated once beside its base and once at a distance, so
position varies within a strategy and strategy within a position. They
are the only rows whose true ratio is known to be exactly 1:

| pair | span | published | mean per cell |
|---|---:|---:|---:|
| `bq-expand` vs adjacent twin | 1 | 0.9996 | 0.29% |
| `bq-scan-mulback` vs adjacent twin | 0 | 0.9970 | 0.46% |
| `mut-odo-vecdims` vs adjacent twin | 1 | 0.9890 | 1.13% |
| `mut-odo-vecdims` vs distant twin | 8 | 1.0017 | 1.80% |
| `bq-scan-mulback` vs distant twin | 31 | **1.0144** | 2.39% |
| `bq-expand` vs distant twin | 38 | **1.0395** | 5.90% |

No pair had a cell capped, so every published figure above equals its paired
one — the identity the winsorized estimator bought and `--selftest` asserts —
and the published column is the yardstick for comparing two rows of the
Results table, while a margin measured per shape still belongs against the
paired figures `read-run.py --aa` prints.

**Nothing under about 3% is a result across the roster; about 1% between
neighbours.** The CI% for those six rows reads 0.06-0.14%, so the interval
understates run-to-run variability by more than an order of magnitude: it
measures sampling error *within* one benchmark, while two separately placed
benchmarks also differ in code layout, cache occupancy and inherited GC
state. The A/A is the only column that sees that, and `--aa` prints the
calibration outright — on Run 7, a median interval half-width of 1.36%
against an
observed spread of 3.95% — so multiply any interval this reader prints by
about three before believing it.

**Position moves a bench, the bias follows the slot, and Run 7 (Harness)
records it on a full-budget run.** Within each strategy the distant twin
reads above the adjacent one — +4.0pp on `bq-expand` over 37 slots of
separation, +1.7pp on `bq-scan-mulback` over 31, +1.3pp on `mut-odo-vecdims`
over 7 — so the bias appears *inside* every strategy and grows with span:
position, not a property of any arm, at roughly +0.05% to +0.18% per bench
slot. The distant twins sit early and their bases late, so the sign says the
earlier slot is slower:
**the group warms up**, which is the same effect the R2 section sees within a
bench. `list` runs first, in the coldest slot, so every ratio divides by an
inflated baseline and arms far down the roster are flattered — by up to ~4%,
which is larger than the adjacent-pair floor and systematic rather than
noise. Comparisons
between roster-adjacent arms are nearly unbiased; cross-roster ones are not.

**A filtered run cannot answer the position question**, and the trap is quiet
enough to be worth stating: criterion's selection removes the intervening
benches, so a pair placed 28 slots apart in the roster ends up adjacent, and
the crossed design collapses to six near-identical adjacent pairs. Measured on
a twelve-arm probe, spans of 28 and 0 both came out under 6. `--aa` says so
when the run is filtered. Position is the one question here that needs the
whole roster in the process.

The floor grew with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a
real difference. On raw slopes Run 7's six pairs read 0.9996 and 1.0346,
0.9975 and 1.0121, 0.9923 and 1.0016 — adjacent and distant per strategy —
so the largest deviation was 3.46% before the correction and is 3.95%
after it. Correcting the table without correcting the floor would have been
the whole error.

That is a mechanism rather than an observation, so it was checked — on Run
6's three pairs, when the correction landed. Subtracting
a shared term scales a pair's deviation from 1 by `1/(1-f)`, `f` being the
term as a share of the arm — an identity *per shape*, and therefore worth
nothing until it has survived the geomean over shapes. It did, to within 0.01
percentage points on all three: predicted 1.0010, 0.9943 and 1.0293
against observed 1.0011, 0.9942 and 1.0292, with the amplification tracking
`1/(1-f)`
arm by arm too. So the floor's growth is the correction's own arithmetic, not
a second effect riding along with it — and Run 7's pairs move the same way,
every distant deviation larger net than raw.

**Failed Run 6's two conclusions here are settled.** *1/time* is refuted as
an account of the floor: per-cell *scatter* does track it -- the adjacent
pairs in the table rank by their arms' speed -- but scatter cancels, and
the bias that survives cancelling ranks by span, not by any arm's speed.
*Position* is confirmed, by the crossed design built for it: the re-aiming
for Run 6 had changed strategy and position together, which is why that run
could license neither verdict, and crossing them is what settled it.

Six A/A points are still a modest estimate of a noise floor, but a
structured one: adjacent pairs sit within ~1% of 1, distant ones reach ~4%.
So "~3%" survives as the
soft threshold for a margin between two arbitrary rows, a margin between
roster-adjacent arms can be read from about 1%, and neither is a computed
bound.

The floor above is also measured within one roster, and the roster is a
variable of its own: RTS pool state a predecessor leaves in the process
moved a horde-ad benchmark ~18% ([the full account][pos-effect] -- which
includes this suite's own floor measured isolated against in-process, on
both harness generations). Every strategy sharing one process is what
protects the tables above, ratios cancelling the shared process draw; a
comparison that crosses runs should pin the benchmark selection along
with the binary, and between recorded runs here the roster has rarely
held still.

**Each population measures its own floor.** The same six controls ride every
process, so a stride-class run prices the noise of the process its own
figures came out of — which is the only process they can be judged in — but
it prices it over two or three cells where the main set has two dozen. Read a
class's controls as this floor confirmed there or not, rather than as a
threshold of that class's own, and never carry the main set's ~3% into a
class comparison or the other way about. Run 7's class processes are that
ruling observed: floors from 0.5% (`slice`) up to 10.0% (`window`) and 12.2%
(`bcast`), each of the two large ones one wild control cell in a
two-or-three-shape population — `bcast`'s is a 41% cell on
`bcast-tall-Mx2` — with every other control in those processes quiet.


### R2 is the ramp detector, not the noise detector

The two columns catch disjoint failures. **CI%** finds sampling noise, which
the capping then bounds. **R2** finds *curvature* -- early, low-iteration
samples running slower than late ones, because criterion forces only a minor
GC between samples and a full one just once per benchmark, so promoted data
accumulates as the sample count climbs.

A ramp is systematic, so it yields a *narrow* CI around a *biased* slope: the
capping cannot see it and will not bound it. The bias tilts the fit shallow, so
a ramped strategy reads slightly **faster** than it is -- and not uniformly,
since strategies allocating a large scratch ramp harder than in-place fills,
making the flattery differential exactly where the comparison is decided.
Read any row with R2 below 0.99 as possibly a couple of percent optimistic
rather than merely noisy. In Run 7 (Harness) that is 2 cells of 1176 in the
main set — `all-expand` on `stretch-square-1341` at 0.9697, the worst, and
one A/A control's cell on `stretch-inner1` — and the class processes add six
more, five of them on `bcast-inner900`, the scan family ramping where 1.8M
elements re-read a 2000-element backing.

Run 6's two worst cells had a cause worth the space, because it is a method
as much as
a finding. `mut-odo` carried that run's highest CI cell on both of its two
smallest `cnn-L1` shapes, while `build` -- the identical fill through
`vBuildVS`, from a
different roster slot -- and `mut-odo-vecdims` -- the same fill with the
odometer's cons-lists replaced by unboxed vectors -- were clean on the same
two. Same shape, same process, so it was neither the shape nor a disturbance
in
that stretch of the run: it is the odometer's list traffic as a GC ramp where
`l` is small enough for it to dominate, which is the cost `mut-odo-vecdims`
exists to remove. The ramp did not recur at Run 7's full budget; the same
cost surfaces there as scatter instead, `mut-odo` carrying the main set's
highest `noise` figure by far. **Positional or strategy-intrinsic is the
question to ask
first of any suspicious cell**, and `--cells` answers it cheaply: a
disturbance shows as a contiguous window of roster slots, a property of the
code shows as one slot across several shapes.

That second reading needs several shapes to see the slot across, which a
[stride class](#the-stride-classes-and-what-they-cover) does not have: with
two or three, a ramped cell is a large share of its column and only the first
reading is available. Whether it is the shape or the strategy is then a
question for the main set, where the same strategy has two dozen cells.


### sum-only, and the correction now applied

Every strategy is timed as `VS.sum . fb`, so every measurement carries the
same forcing pass; `sum-only` times that pass alone. It is a median 17.7% of
`bq-expand` and 2.7% of `list`, so an uncorrected ratio is compressed toward 1
by about that much and every margin read off one is an *understatement*.

**Run 6 (-O1) licensed subtracting it, and every figure on this page is net
of it**: its two halves agreed to 0.01% paired, flat in shape size as well
as position, and `read-run.py` has since taken the term per shape as the
mean of the halves and divided net of it. Nothing is comparable across that
line — every figure predating Run 6 here and in `Main.hs` was uncorrected —
though the uncorrected column stays one `--exclude sum-only-early --exclude
sum-only-late` away, and `read-run.py` says on stderr when it is reading
one. And the correction can change an ordering, although `(B+S)/(A+S) < 1`
exactly when `B < A`: that identity holds *per shape*, and the geomean over
shapes does not preserve it — Run 6 saw three adjacent pairs swap, all
inside the floor.

**The term passes three gates, re-passed by every run rather than
inherited**, each blind to
what the others catch:

1. *Position.* The two halves sit far apart in the roster and must agree;
   failing is the halves parting past the floor.
   **Run 7 (Harness)**: 0.9989 paired, 0.23% mean per cell, worst cell
   0.74%, the halves 43 benches apart.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape -- one sum over `l` elements -- and a term that were not
   could be wrong in both halves alike, leaving their agreement to notice
   nothing. It is: 0.588 to 0.604 ns per element across the whole shape set, a
   1.03x spread over that 6250x range of `l`, with the largest shapes a
   couple of percent
   dearer per element than the smallest and no trend beyond that. `--selftest`
   checks it on every run and fails the run past a 1.5x spread.
3. *The read itself.* `sum-only` re-reads one **fixed** vector, where a
   strategy sums one its own fill has just written -- a different cache state,
   and the one thing neither gate above can see, since a term biased by it
   would be biased alike on every shape and in both halves. This is what
   `bq-expand-nosum` and `mut-odo-vecdims-nosum` are for: each is its base arm
   run again and forced with a single element instead of the sum, so *base
   minus arm* is that sum in situ. Measured against `sum-only` on Run 7 they
   read
   **1.0034** and **0.9966** as medians -- within 1%, on the two arms where
   the term is the
   smallest and largest share of the bench (a sixth of `bq-expand`, a third
   of `mut-odo-vecdims`), so the test spans the range over which a bias would
   matter. They also *bracket* 1, where a systematically warmer fixed-vector
   read would have put both on one side of it. Per-cell scatter is 3.1% and
   6.5%, the worst cells on `stretch-inner256` and `stretch-rank10`. Failing
   is both medians leaving 1 on the same side by more than a few percent —
   the biased-read signature; one arm scattering while the other reads clean
   is a local disturbance for that population's write-up, not a failed gate,
   `reshape1`'s vecdims arm being Run 7's example.

**The three gates are a population's, not a run's.** Every process carries the
`sum-only` pair and the two `-nosum` arms, so a
[stride class](#the-stride-classes-and-what-they-cover) measures its own term
and re-passes all three on its own cells; the main set's term licenses
nothing about a class's, in either direction. What a small population weakens
is gate 2 alone: it reads the term's cost per element across the shape set,
and a class spans a fraction of the main set's range of `l` — two shapes of
nearly equal `l` leave it almost nothing to see. Gates 1 and 3 are as strong
there as here, being about position and about the read.

What remains open is narrower than the original objection: the `-nosum`
pairs price
two arms, not the whole roster, so a fill whose write pattern leaves the cache
in
some quite different state could still be summed at a cost `sum-only` misses.
Two arms an octave apart in speed agreeing to 1% makes that unlikely rather
than impossible, and the arms are in the roster so every run reprices them.


### Non-urgent TODO list

- **A class process's provenance line counts every class view, not the
  population that ran.** The count is fixed before criterion does the
  selecting, so each class process reports the whole class set's size beside
  its own elapsed time and heap peaks, both of which are its own; the
  write-up takes the population's size from the reader instead, which costs a
  sentence every run. The fix would have `provenance` told what was selected,
  and that means `Main.hs` parsing a criterion argument it currently passes
  through untouched — a second source of truth for criterion's own matching
  rules, wrong the moment a run reaches for `-m glob`, which is why the
  sentence is preferred to the code.
- **Runs never overlap in the benchmarked set.** `mkStrided`'s index map is
  a bijection onto `[0, l)`, where im2col patches — the workload this page
  opens by naming — overlap heavily and so reuse cache. The window class
  (`mkWindow`) builds exactly those overlapping patch views, and Run 7
  (Harness) records them: the overlap *lifts* every ratio rather than
  lowering it, so the main
  set's pessimism about this case was about absolute cost, never about the
  fallback's standing against `list`. The window block in [The stride
  classes, run by run](#the-stride-classes-run-by-run) carries the figures.
- **The roster order biases the table, and nothing corrects for it.** The
  warm-up drift above means a strategy's figure depends on its slot, `list`
  being in the coldest one. The fixes are all real changes rather than
  write-ups — a warm-up bench before `list`, interleaving or randomising the
  order, or correcting each row by its slot — and each breaks comparability
  with every run so far, which is why none is taken yet. Run 7 has now
  confirmed the drift on a recorded run, with its size in [the floor
  section][floor], so the choice is due — and its natural moment is
  after Run 8, whose regime flip wants everything else held still.
- **No build-vs-output time decomposition.** `diag` measures per-builder
  *allocation* only, so a claim like "the table build is a third of the cost"
  -- the natural reading of `bq-mut-runs` beating `bq-mut` by 39% -- cannot be
  checked here. It needs a timing mode alongside `diag`'s allocation one,
  using the fixed-iteration differencing the horde-ad performance model
  prescribes (`-n 200` minus `-n 100`, fresh processes) rather than criterion,
  since the builders are not benchmarks.

## About the last run (Run 7)

**Run 7 (Harness).** Criterion, GHC 9.12.4, **-O1**; the first run on the
converted scratch vectors, the first with the crossed A/A controls and the
`-nosum` arms, and the first to record any stride class. One process per
population — the main set, then each class in `classViews`' order, back to
back on an otherwise idle machine, 3h1m26s in all — built from commit
`3437f37` with a clean tree, on one
desktop — Zen 3, a Ryzen 7 5800X. The main process's stderr provenance line
reads *roster 49
benchmarks over 24 shapes; elapsed 1h41m20s; peak 364 MiB in use, 138 MiB max
residency*, comfortably inside `micro.cabal`'s `-M2G`, which is why that note
stands unchanged. The JSONs are not kept; the commit is what remains of them.

-O1 is the regime a default `cabal build` of orthotope compiles under today,
which is why the record is taken there first. Run 8 (SpecConstr) follows,
changing the answer for a whole family
of strategies rather than nudging it, and keeps the populations this run
pins, so that regime is never confounded with membership.

**Run 7 records every population**: the main set and the eight stride
classes, one process each,
so its provenance lines are one per process: the main set's at this head, each
class's beside its own table in [The stride classes, run by
run](#the-stride-classes-run-by-run). The regime, the machine and the commit
are the whole run's and stay here, stated once.

**Everything in this chapter is replaced by the next run.** What exactly, and
in which other files, is [Provenance](#provenance). None of it is portable: a
run on another machine is a different measurement rather than a repetition.

### Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](#sum-only-and-the-correction-now-applied) carries that decision
and this run's re-pass of its gates), and this is the first table measured
on the unboxed scratch the shipped code uses, so **no figure here is
comparable to one from a run before the conversion**
([the scratch vector flavour](#the-scratch-vector-flavour) says what that
severed).

**Comparing runs?** The table below is Run 7's own; what to hold a new run
against is [What Run 8 compares against](#what-run-8-compares-against), the
claims to test are [the ones after it](#the-claims-run-8-should-test), the
population and the absolute anchor are in [Provenance](#provenance), and
nothing under ~3% is a result.

**It is the main set's table**, and every column below is a statistic of that
population: each stride class has a table of its own, on the same rows and in
the same columns but its own basis, in [The stride classes, run by
run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*,
  less that shape's forcing term, over `list`'s slope less the same term,
  with the per-shape log-ratios *winsorized* first — capped at the row's own
  median plus or minus three MADs. Nothing is dropped, so all rows cover one
  population and any two columns are comparable; a cell far enough out to
  distort the mean has its influence bounded instead of its evidence deleted.
  The `CI%`, `worst`, `smp` and `alloc` columns stay raw: subtracting a shared
  term moves a point estimate, it does not make a cell better measured.

  **This replaced a trim** — drop each strategy's single highest-CI shape —
  and the ruling is worth keeping because the trim looks obviously right and
  is not. It selected on CI, and criterion spends a *time* budget, so a slow
  cell buys fewer samples and a wider CI: measured on Run 6, the cell it
  removed was above its own row's geomean in **30 of 41** rows, p about 0.003.
  It therefore deleted each strategy's worst evidence, differentially, and a
  catastrophic shape is exactly the shape it would remove:
  `bq-expand-lemire-out` loses on one shape of 33, and that shape was the one
  trimmed from its column.
  Because the cell removed differed by row, two published columns were also
  geomeans over different shape sets, which is why a published A/A ratio used
  to disagree with its paired one. Swapping estimators costs a median 2% and
  moves one row (`mut-offsets`) by 14%, that row having been flattered all
  along; it buys back exact comparability, and `--selftest` now asserts
  published == paired for every uncapped pair.

  **Don't reach for inverse-variance weighting**, which is the
  standard-looking repair and is worse than what it repairs. It assumes every
  shape estimates one ratio and differs only in precision, where here the
  between-shape variance runs a median 5,000x the within-shape kind — the
  heterogeneity is this page's finding, not its error — so weighting by
  precision collapses the effective shape count from 33 to about nine and
  hands a quarter of the weight to the smallest shape in the set. Worse for
  the purpose: a catastrophically slow cell buys fewer samples, so it has a
  wider CI, so IVW discounts precisely the cells the trim used to delete —
  the same failure made continuous, not a repair of it.

  The *slope* rather than criterion's mean, because criterion never times one
  call: it times batches — one call, then four, then twenty — and every batch
  also pays for starting the timer and for the first pass through cold code
  and cold data. A mean divides each batch's time by its calls, so that fixed
  cost is smeared across them and weighs most in the small batches. The slope
  is the line through those points: how much more time one *additional* call
  adds, leaving the fixed part behind as the line's height at zero. On the
  microsecond shapes, hundreds of samples and no warm-up worth speaking of,
  the two agree. They part on the slow shapes, where the early batches run
  cold: there the mean reads high, and by different amounts for different
  strategies — which is exactly the part that dividing by `list` cannot
  cancel. It also keeps `CI%` and R² describing the number the table shows,
  both being properties of that same fitted line.
- **CI%** is the median across shapes of the slope's confidence interval as a
  percentage of the slope -- "how many digits are real". 0.5% is three; 5% is
  one.
- **smp** is the median sample count. Criterion spends a time budget, so a
  slow call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`), the
  median over shapes of the `allocated` fit the harness now runs on every
  bench of every shape. The multiples were held to be shape-independent —
  refitted on a different shape, every one reproduced to within 0.4% — so that
  the median was a formality rather than a smoothing and the column did not
  move with what it was fitted on. **That is wrong**, and Run 6 (-O1)
  reproduced the refutation at full budget where a rough pass had found it:
  41 of 42 strategies vary by more than 5% from shape to shape, the median
  strategy by 3.93× and the worst by 22× (`bq-unfold`, 1.00× to 22.00×), and
  the four shapes of identical `l` = 1800000 give `bq-expand` 1.000×, 2.778×,
  3.000× and 3.642×. Every allocated
  fit sits at R² 1.000, so the spread is the quantity and not the measurement,
  and allocation being deterministic per call the budget does not bear on it.
  What does survive is the column: a median over a *pinned* shape set
  reproduces, `list` landing at 27.67× and `unfold-add` at 29.89× on both the
  rough pass and Run 6. So read `alloc` as a
  statistic of a strategy **and** a shape set, and pin the shape set before
  comparing it across runs, exactly as the `time` column already asks. It is
  the one column the correction does not touch.

| strategy | time | worst | CI% | smp | alloc | needs | precondition |
|---|---:|---:|---:|---:|---:|---|---|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *69* | *3.11x* | *its base arm, forced with one element* |  |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *88* | *1.00x* | *the same, on the fastest arm* |  |
| *sum-only-early* | *--* | *--* | *0.02* | *102* | *0.00x* | *the term every row has subtracted* |  |
| *sum-only-late* | *--* | *--* | *0.02* | *102* | *0.00x* | *the same, at the other end* |  |
| *mut-odo-vecdims-aa* | *0.053* | *0.121* | *0.06* | *79* | *1.00x* | *A/A control* |  |
| **mut-odo-vecdims** | **0.054** | 0.121 | 0.04 | 78 | 1.00x | new mutating `Vector` method |  |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.122* | *0.06* | *78* | *1.00x* | *A/A control* |  |
| mut-flat | 0.063 | 0.165 | 0.08 | 84 | 1.33x | new mutating `Vector` method | `l < 2^32` |
| **bq-mut-runs-mulback** | **0.072** | 0.188 | 0.11 | 83 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-mut-runs-gm-mulback | 0.078 | 0.201 | 0.05 | 82 | 1.33x | mutable `Int` scratch | none |
| mut-odo | 0.084 | 0.250 | 0.71 | 72 | 1.00x | new mutating `Vector` method |  |
| bq-mut-runs | 0.089 | 0.221 | 0.06 | 76 | 1.33x | mutable `Int` scratch |  |
| **bq-scan-packed-mulback** | **0.097** | 0.151 | 0.07 | 71 | 2.00x | nothing (pure) | `l`, offsets < 2^32; m <= 2^31 |
| bq-odo-mulback | 0.101 | 0.182 | 0.10 | 69 | 2.75x | nothing (pure) | `l < 2^32` |
| build | 0.105 | 0.327 | 0.30 | 68 | 1.00x | new mutating `Vector` method |  |
| offtab | 0.110 | 0.244 | 0.34 | 67 | 2.00x | mutable `Int` scratch |  |
| bq-mut-lemire-out | 0.111 | 0.296 | 0.24 | 68 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-scan-rem-mulback | 0.115 | 0.198 | 0.11 | 67 | 4.33x | nothing (pure) | `l < 2^32` |
| bq-expand32-lemire-mulback | 0.117 | 0.293 | 0.08 | 68 | 2.49x | nothing (pure) | `l < 2^32`; src < 2^31 |
| **bq-scan-rem-gm-mulback** | **0.119** | 0.229 | 0.09 | 67 | 4.33x | nothing (pure) | **none** |
| bq-expand-lemire-out | 0.119 | 0.297 | 0.07 | 67 | 3.11x | nothing (pure) | `l < 2^32` |
| bq-expand-lemire-mulback | 0.119 | 0.298 | 0.08 | 68 | 3.11x | nothing (pure) | `l < 2^32` |
| *bq-scan-mulback-aa-adjacent* | *0.123* | *0.235* | *0.14* | *66* | *4.33x* | *A/A control* |  |
| bq-mut-lemire-mulback | 0.123 | 0.300 | 0.22 | 66 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-scan-mulback | 0.123 | 0.235 | 0.16 | 66 | 4.33x | nothing (pure) | `l < 2^32` |
| bq-expand-b | 0.124 | 0.301 | 0.23 | 68 | 3.06x | nothing (pure) |  |
| offtab32 | 0.125 | 0.315 | 0.27 | 66 | 1.50x | mutable `Int` scratch | src < 2^31 |
| *bq-scan-mulback-aa-distant* | *0.125* | *0.246* | *0.09* | *66* | *4.33x* | *A/A control* |  |
| bq-expand-qr-prim | 0.127 | 0.297 | 0.09 | 66 | 3.11x | nothing (pure) | shape well-formed |
| *bq-expand-aa-adjacent* | *0.127* | *0.305* | *0.14* | *66* | *3.11x* | *A/A control* |  |
| **bq-expand** | **0.127** | 0.305 | 0.12 | 66 | 3.11x | **nothing -- SHIPPED** |  |
| bq-scan-gm-mulback | 0.128 | 0.271 | 0.08 | 66 | 4.33x | nothing (pure) | `l < 2^32` (builder) |
| bq-expand-zf | 0.129 | 0.329 | 0.14 | 66 | 3.11x | nothing (pure) |  |
| *bq-expand-aa-distant* | *0.132* | *0.338* | *0.08* | *66* | *3.11x* | *A/A control* |  |
| bq-mut | 0.138 | 0.336 | 0.12 | 64 | 1.33x | mutable `Int` scratch |  |
| offsets-quot | 0.188 | 0.468 | 0.37 | 58 | 5.21x | nothing (pure) |  |
| mut-offsets | 0.236 | 0.712 | 0.43 | 58 | 6.20x | new mutating `Vector` method |  |
| bq-unfold | 0.239 | 0.750 | 0.24 | 54 | 8.28x | nothing (pure) |  |
| fused | 0.256 | 0.505 | 0.51 | 54 | 9.21x | new pure `Vector` method |  |
| bq-gen | 0.279 | 1.837 | 0.53 | 52 | 3.58x | nothing (pure) |  |
| offtab-scan | 0.319 | 0.454 | 0.31 | 54 | 11.00x | nothing (pure) | `l < 2^32` (builder) |
| bq-gen-lemire | 0.377 | 2.885 | 0.52 | 49 | 2.95x | nothing (pure) -- refuted | `l < 2^32` |
| all-expand | 0.388 | 0.691 | 0.76 | 46 | 11.03x | new pure `Vector` method |  |
| backperm | 0.455 | 1.118 | 0.62 | 43 | 15.25x | new pure `Vector` method |  |
| cm-gather | 0.620 | 0.993 | 0.57 | 39 | 22.99x | new pure `Vector` method |  |
| unfold-add | 0.932 | 1.401 | 0.67 | 34 | 27.94x | new pure `Vector` method |  |
| gen-unsafe | 0.997 | 3.396 | 0.49 | 41 | 12.01x | -- |  |
| gen-quotrem | 0.999 | 3.604 | 0.51 | 41 | 12.01x | 1st attempt |  |
| list (baseline) | 1.000 | 1.000 | 0.31 | 35 | 26.21x | -- |  |

`concat-runs` has no row: it is rostered and checked but no longer timed, for
the reason given with the strategy list above. This is the first table
estimated as the column definitions above describe — winsorized, with the
`worst` column — where Run 6's was trimmed, one more reason no figure crosses
between them.


### What Run 8 compares against

Run 8 keeps this run's shape set and roster and changes only the regime, so
there is no restricting to do: the published column above is the yardstick.
What a regime flip is read for is orderings and allocation tiers rather than
margins — a binary compiled under another regime is a different measurement,
not a repetition. The five rows nearest the decisions:

| strategy | Run 7 (Harness) |
|---|---:|
| `mut-odo-vecdims` | **0.054** |
| `bq-mut-runs-mulback` | **0.072** |
| `bq-scan-packed-mulback` | **0.097** |
| `bq-scan-rem-gm-mulback` | **0.119** |
| `bq-expand` | **0.127** |

How Run 7 itself read against Run 6's yardstick: on the 22 shared shapes
`bq-expand` came in at 0.135 against the yardstick's 0.144 — the −6.3% the
scratch conversion's probe predicted — and `mut-odo-vecdims` at 0.056
against 0.051, +9.8%, past the floor and unattributed ([the scratch vector
flavour](#the-scratch-vector-flavour)); the other three rows moved at or
inside the floor. The
published columns differ further by the two shapes new since
([Provenance](#provenance)), which flatter the whole `bq-*` family — a run
that ignored this would read a shape-set change as a code change.

**Each stride class's yardstick is its own table below**, this run being the
first measurement of every class; Run 8 reads them class by class, the
populations pinned across the regime flip on purpose.

And because a geomean cannot say *where* it moved, the **fingerprint**
below is kept so a future disagreement can be localised rather than only
noticed. Its membership is a rule, not a habit: the shipped arm, the rows
the Results table bolds, and any arm an open question names — `mut-odo`
and `build` sit here on [the broken-identity
question](#what-the-next-runs-have-to-decide) — and an arm leaves when its
question closes. `list`'s own net per call rides along, guarding the
baseline at every shape where the anchors guard three, and converting any
ratio beside it back to absolute time. Allocation stays medians-only on
purpose: deterministic per call, so a run that raises an allocation
question re-derives it within itself. `./read-run.py RUN.json
--fingerprint` emits both tables — paste them whole, transcribing nothing
by hand, since hand-carrying this table once left two of Run 6's cells
standing under Run 7's name, and the first emitted paste is what caught
them. The column heads shorten the arm names as the stretch table's do:
scan-packed is `bq-scan-packed-mulback`, scan-rem-gm
`bq-scan-rem-gm-mulback`, mut-runs-mulback `bq-mut-runs-mulback`, vecdims
`mut-odo-vecdims`. And the [stretch table][pershape] is the same kind of
record for `bq-expand-b` and `bq-expand-lemire-out`, on the shapes chosen
to stress orderings — compare it the same way.

| shape | `sInner` | `l` | `list`, net | bq-expand | scan-packed |
|---|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.83 µs | 0.191 | 0.142 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.03 µs | 0.253 | 0.139 |
| `stretch-rank12` | 2 | 4096 | 108 µs | 0.305 | 0.151 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 109 µs | 0.227 | 0.115 |
| `conv1d-24` | 3 | 5184 | 96.4 µs | 0.147 | 0.122 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 358 µs | 0.155 | 0.102 |
| `gather48-src-50` | 3 | 22500 | 418 µs | 0.140 | 0.119 |
| `stretch-rank10` | 3 | 59049 | 1.37 ms | 0.175 | 0.114 |
| `stretch-coprime-r7` | 13 | 60060 | 1.24 ms | 0.101 | 0.074 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.55 ms | 0.146 | 0.098 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.97 ms | 0.150 | 0.098 |
| `stretch-primes` | 89 | 250357 | 4.31 ms | 0.085 | 0.078 |
| `stretch-inner1` | 1 | 500000 | 12.6 ms | 0.178 | 0.136 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 27.6 ms | 0.078 | 0.059 |
| `vgg-14-c512-k3` | 3 | 903168 | 30.5 ms | 0.107 | 0.069 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.1 ms | 0.110 | 0.090 |
| `stretch-inner256` | 256 | 1750784 | 49 ms | 0.066 | 0.047 |
| `stretch-pow2stride` | 64 | 1769472 | 55.4 ms | 0.062 | 0.077 |
| `stretch-r5-8x432` | 8 | 1769472 | 54.9 ms | 0.060 | 0.053 |
| `stretch-square-1341` | 1341 | 1798281 | 29 ms | 0.112 | 0.141 |
| `stretch-bigstride` | 3 | 1800000 | 46.6 ms | 0.099 | 0.087 |
| `stretch-tab7MB` | 2 | 1800000 | 35.9 ms | 0.164 | 0.138 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 33.7 ms | 0.076 | 0.065 |
| `stretch-wide-2xM` | 2 | 1800000 | 36.2 ms | 0.154 | 0.136 |

| shape | scan-rem-gm | mut-runs-mulback | vecdims | mut-odo | build |
|---|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 0.189 | 0.108 | 0.091 | 0.169 | 0.211 |
| `cnn-L1-6x6-c1` | 0.182 | 0.151 | 0.108 | 0.208 | 0.232 |
| `stretch-rank12` | 0.201 | 0.188 | 0.121 | 0.250 | 0.327 |
| `cnn-L1-24x24-c1` | 0.147 | 0.125 | 0.087 | 0.183 | 0.232 |
| `conv1d-24` | 0.159 | 0.072 | 0.067 | 0.144 | 0.188 |
| `lenet-L1-28-c1-k5` | 0.124 | 0.089 | 0.062 | 0.115 | 0.123 |
| `gather48-src-50` | 0.152 | 0.069 | 0.063 | 0.144 | 0.167 |
| `stretch-rank10` | 0.146 | 0.095 | 0.076 | 0.137 | 0.170 |
| `stretch-coprime-r7` | 0.084 | 0.068 | 0.033 | 0.042 | 0.061 |
| `cifar-L2-16-c64-k3` | 0.126 | 0.073 | 0.055 | 0.123 | 0.145 |
| `cnn-L2-24x24-c32` | 0.128 | 0.078 | 0.062 | 0.112 | 0.151 |
| `stretch-primes` | 0.078 | 0.071 | 0.029 | 0.025 | 0.032 |
| `stretch-inner1` | 0.229 | 0.026 | 0.098 | 0.204 | 0.289 |
| `alexnet-L2-27-c48-k5` | 0.074 | 0.043 | 0.029 | 0.049 | 0.067 |
| `vgg-14-c512-k3` | 0.091 | 0.052 | 0.039 | 0.070 | 0.109 |
| `alexnet-L1-55-c3-k11` | 0.105 | 0.073 | 0.041 | 0.055 | 0.067 |
| `stretch-inner256` | 0.067 | 0.043 | 0.017 | 0.016 | 0.017 |
| `stretch-pow2stride` | 0.064 | 0.072 | 0.063 | 0.063 | 0.063 |
| `stretch-r5-8x432` | 0.060 | 0.039 | 0.022 | 0.028 | 0.035 |
| `stretch-square-1341` | 0.134 | 0.133 | 0.080 | 0.082 | 0.082 |
| `stretch-bigstride` | 0.107 | 0.048 | 0.042 | 0.066 | 0.084 |
| `stretch-tab7MB` | 0.177 | 0.068 | 0.073 | 0.135 | 0.178 |
| `stretch-tall-Mx2` | 0.069 | 0.061 | 0.025 | 0.020 | 0.025 |
| `stretch-wide-2xM` | 0.176 | 0.065 | 0.072 | 0.137 | 0.175 |

Two rows to read first. `stretch-square-1341` is one of the two shapes where
the fastest pure strategy *loses* to `bq-expand` — treat a disagreement
there as the shape; the other, `stretch-pow2stride`, is where the leading
arms of both families converge ([the per-shape section][pershape]).
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.


### The claims Run 8 should test

**Run 7's verdicts on Run 6's seven claims first**, since a run reports
breaks rather than re-deriving the table. Claims 1 and 5 held whole, as did
the second halves of 3 and 4 and the first half of 6, and claim 7 but for
`bq-expand`'s allocation, which the scratch conversion shifted. What moved:
the tie in 2 broke without SpecConstr's help,
`bq-scan-packed-mulback`/`mut-odo` reading 1.096 on the shared shapes — but
at 13 wins of 22 and a 0.61–3.26 per-shape spread that is a geomean shift
with no per-shape ordering behind it. 3's first half collapsed into the
floor (`bq-scan-mulback`/`bq-expand` 0.975 at 13 wins of 22): the scan
build's edge over `concatMap` was mostly the Storable table's cost, which
the conversion removed. 4's first half inverted outright: `bq-mut` /
`bq-expand` 1.102, two wins of 22, sign p 0.00012. And 6's second half,
`list` <
`gen-quotrem`, held on the shared shapes (0.939 for `list`) while tying on
the published set, the two shapes new since Run 6 flattering `gen-quotrem` —
the anchors moved only ~1%, so it is population, not `list`.

Restated on this run's own published basis, for Run 8 to check; margins are
paired geomeans, past the floor unless marked, each claim carrying the
reading it rests on:

1. `mut-odo-vecdims` < `mut-flat` < `bq-mut-runs-mulback` < everything pure
   (0.848, 0.877, then 0.745 against the fastest pure arm).
2. `bq-expand` < `bq-mut` (1.089 the other way, 20 wins of 24) and `offtab`
   < `bq-expand` (0.869): after the conversion the pure `concatMap` build
   beats the mutable scratch table, while the `l`-table gather still beats
   both. Run 6 had `bq-mut` ahead, outside the floor; the inversion is the
   conversion's doing rather than a ranking wobble, at two wins of 22 on the
   shapes the runs share.
3. `bq-expand-lemire-out` < `bq-expand` (0.940, 22 of 24): the Lemire output
   substitution keeps paying ([the Lemire section][lemire] carries both
   division sites' story).
4. `bq-scan-mulback` ties `bq-expand` (0.973, inside the floor) — the tie
   SpecConstr is predicted to break, which is Run 8's whole point.
5. `bq-expand` < `offsets-quot` < `bq-gen` < `bq-gen-lemire` (0.676, 0.672,
   0.740): the build ordering — `concatMap` builds the separable grid
   inside vector's stream framework where the lazy list pays for a
   non-fusing cons-list of thunks — ending in Lemire losing at the build
   site. So `bq-expand` is the fastest build that needs neither a class
   extension nor explicit mutation, and among the builds only the mutable
   odometer pair (`bq-mut-runs`, 0.089) still beats it.
6. `cm-gather` < `list` (0.619, 24 of 24), and `gen-quotrem` ties `list` on
   this population (1.0006) while staying 6.5% behind with the two new
   shapes excluded and up to 3.6x behind on its worst — the mixed picture
   this suite exists to have refuted: one `quotRem` per *dimension* per
   element still costs more than the list's allocation on the shapes that
   matter.
7. Allocation, median multiples of the result on this basis: the mutable
   fills 1.00x (just the result), `bq-mut` 1.33x, `offtab` and
   `bq-scan-packed-mulback` 2.00x, `bq-expand` 3.11x (the `concatMap`
   intermediates over the `m`-element table), `gen-quotrem` 12.0x, `list`
   26.2x (thunks). Lower allocation tracks lower time across the table's
   span, though no longer pair by pair — `bq-expand` beats `bq-mut` at
   2.3× its allocation. SpecConstr is predicted to take the plain scan rows
   from 4.33x to 1.33x, and, on the `diag` in its own regime, to move the
   `bq-gen` pair and `bq-expand` with them ([the Run 8
   question](#what-the-next-runs-have-to-decide)).
8. Every pure strategy ahead of `fused` (0.256) runs its output through the
   single in-order `vGenerate`, and the `bq-*` arms behind `fused` —
   `bq-gen` and `bq-gen-lemire` — lose on their table build, not their
   output: one in-order `vGenerate` fuses tighter than a stepped
   `unfoldrExactN` state or a two-pass build-then-gather.
9. `bq-expand-zf` and `bq-expand-b` tie `bq-expand` in the geomean (1.6%
   behind and 2.4% ahead, inside the floor), while `bq-expand-b` runs 24%
   and 22% ahead on `stretch-inner1` and `stretch-wide-2xM`, its only two
   cells past 7% — rank-2 views with one huge outer dimension, exactly
   where seeding from `enumFromStepN` replaces the entire `concatMap`
   build rather than saving one step of it: the design showing through,
   not the no-op an earlier version of this page called it. `bq-expand` is
   still what shipped, on the geomean and on being the plainest form.

Each ordering is one `./read-run.py RUN.json --pair A B` line — paired
geomean,
an interval and a sign test — so a run reports which claims held
rather than re-deriving them from the table. Breaks in 4 and in 7's scan
rows are expected under SpecConstr and are Run 8's point. A break in 6 would
mean something changed in
`list` or in GHC, not in a strategy — check the anchor before anything
else.

**And for each stride class, the same three properties, now carrying Run 7's
verdicts**, the details beside each class's table:

1. **`bq-expand`'s `worst` stays under 1.** Held in every class — 0.234 at
   its highest, under `rev` — so the shipped fallback was never
   slower than the `list` it replaced, on any shape of any class the library
   can produce. This is the property the classes exist to test, no geomean can
   state it, and a break would have been the one
   result here to bear on `Data/Array/Internal.hs` directly.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-scan-packed-mulback` the fastest pure arm, `bq-expand` behind both.
   Held in `revsome`, `bcastmid`, `slice` and `window`; broke where a
   mechanism removes what an arm amortizes over — `rev`, `bcast`, `reshape1`
   and, by a hair, `scaled` hand the
   fastest-pure slot to `bq-odo-mulback`, `reshape1` inverts the whole top
   (`mut-flat` at 0.027 with the `bq-mut-runs-*` arms beside it), and
   `scaled` puts `mut-odo` ahead of `mut-odo-vecdims`. Each break is read in
   its class's paragraph, and [the `sInner`
   ruling](#per-shape-where-the-geomean-hides-the-ordering) is what they
   bear on.
3. **The allocation tiers survive**: the mutable fills at about the result
   vector, `bq-expand` at several times it, `list` at an order of magnitude
   more. Where a level moves it is the class's own `m` showing through,
   exactly as this property warned — `bq-expand` at 1.11x on `scaled` (`m`
   of 1 and 2,000), the plain scan rows at 11.00x on `reshape1` (`m = l`) —
   the ordering of tiers unbroken everywhere.

`--pair` works within a class JSON exactly as within the main one, and is
still the way to compare two arms; its bootstrap interval, over two or three
shapes, is worth less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier in
two. A **new pure `Vector` method** delegates to a pure function the vector
package already ships for every carrier -- `unfoldrExactN`, `backpermute`,
the `concatMap`/`enumFromStepN` pipeline -- so it fights only *minimal* in
orthotope's pure-and-minimal API rule; the **new mutating `Vector` method**
the direct fills need is the [mutable
ceiling](#the-mutable-ceiling-not-taken)'s ask, which *pure* barred outright
until the amendment there turned the bar into a weight.
`offtab` is the `Vector`-class-expressible shape of these gathers -- output by
plain `vGenerate` over a concrete offset table -- so its own cell names only
its mutable `Int` scratch. And the geomean weights every benchmarked shape
**equally**, so a
figure here is a ranking statistic, not a claim about total work saved: the
small shapes count as much as the largest.


### The stride classes, run by run

**Run 7 (Harness) is the first run to record every class**, one process per
class, in [the sequence](#making-a-major-benchmark-run); every table below
is that run's. This section
fixes the form, so that a class is written up the way
the main set is rather than however the session that ran it chose. The form is
this section's own prose and is not a run's to rewrite, exactly as the column
definitions under [Results](#results) outlive the table they explain; what a
run replaces is everything below the form. What a class *is*, and the two
rulings
that keep it a population of its own, are
[in the goal chapter](#the-stride-classes-and-what-they-cover).

First, one table over all of them, so that an inversion is visible without
reading every class's table. Every figure in it is transcribed from a class's
own table below — none is computed here, and none is an average across
classes, there being no such population to average over. Its header, fixed
here so a run fills rows and never reshapes columns:

    | class | shapes | bq-expand | worst | fastest pure | ceiling | floor |

`bq-expand` and `worst` are the shipped row's two columns in that class's
table; *fastest pure* and *ceiling* are the leading pure and mutable arms,
each with its name, since which arm leads is half of what the column says;
*floor* is the largest deviation from 1 among that process's six A/A
controls. A cell that breaks one of [the three
properties](#the-claims-run-8-should-test) is bolded, and the class's own
paragraph says what broke.

Then one block per class, in `classViews`' order — `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled` — each carrying the same
five things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause, and
   its shapes with their `l` and `sInner`, which is what makes the table under
   it readable without `Main.hs` open;
2. the table `./read-run.py $R-$c.json --markdown` emits, pasted whole and
   never edited — six columns, with the emphasis carried over from the main
   table so the shipped row is found at a glance, and `needs` and
   `precondition` left to that table as properties of a strategy rather than
   of a population;
3. its own controls, off `--aa`: the A/A deviations with their spans, the two
   `sum-only` halves, and the in-situ term from the `-nosum` arms — this
   process's own floor and its own three gates, neither inherited nor lent;
4. its provenance and its anchor: elapsed time and the two heap peaks from
   that process's stderr line, its population's size from the reader's first
   line ([why not both from one place](#making-a-major-benchmark-run)), and
   `list`'s absolute per-call time on one of its shapes, raw and net. The main
   set's three anchors guard a baseline that moves for every population at
   once; this one guards a baseline that could move for this mechanism alone,
   which is the case a table of ratios hides completely. A three-shape class
   adds one line here — the bolded rows' per-shape net ratios, in the lead's
   shape order — because its table under-determines its cells, where a
   two-shape table carries them already, `time` and `worst` jointly fixing
   both;
5. one paragraph of what the class says, and none where it says nothing: an
   ordering that inverted, a `worst` above 1, an allocation tier that moved, a
   mechanism showing through a single cell. A class that reproduces the main
   ordering gets one sentence saying so, that being a result and reading as
   one.

`./read-run.py RUN.json --block` assembles items 2 through 4's mechanical
parts in one call — table, controls, the provenance and anchor skeleton,
and a three-shape population's per-shape line; the lead and the paragraph
stay the author's, a skeleton writing no findings.

The blocks carry no headings of their own. One per class would crowd the
contents and the replace list alike, where a bolded lead reads the same and
lets one link cover the section — which is what `--check-doc`'s coverage
check counts.

| class | shapes | bq-expand | worst | fastest pure | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.145 | 0.234 | **`bq-odo-mulback`** 0.109 | `mut-odo-vecdims` 0.056 | 1.0% |
| `revsome` | 3 | 0.134 | 0.176 | `bq-scan-packed-mulback` 0.113 | `mut-odo-vecdims` 0.059 | 2.7% |
| `bcast` | 3 | 0.095 | 0.153 | **`bq-odo-mulback`** 0.080 | `mut-odo-vecdims` 0.036 | 12.2% |
| `bcastmid` | 2 | 0.130 | 0.182 | `bq-scan-packed-mulback` 0.097 | `mut-odo-vecdims` 0.045 | 3.7% |
| `reshape1` | 2 | 0.188 | 0.192 | **`bq-odo-mulback`** 0.130 | **`mut-flat`** 0.027 | 3.5% |
| `slice` | 2 | 0.130 | 0.183 | `bq-scan-packed-mulback` 0.105 | `mut-odo-vecdims` 0.047 | 0.5% |
| `window` | 2 | 0.159 | 0.174 | `bq-scan-packed-mulback` 0.113 | `mut-odo-vecdims` 0.060 | 10.0% |
| `scaled` | 2 | 0.097 | 0.102 | **`bq-odo-mulback`** 0.083 | **`mut-odo`** 0.028 | 0.8% |

**`rev` — every stride negated, offset at the top: the view `rev` on every
axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *128* | *3.22x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.04* | *158* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.056* | *0.089* | *0.02* | *136* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.056* | *0.089* | *0.07* | *136* | *1.00x* |
| **mut-odo-vecdims** | **0.056** | 0.089 | 0.05 | 136 | 1.00x |
| mut-flat | 0.077 | 0.122 | 0.16 | 137 | 1.34x |
| bq-mut-runs-gm-mulback | 0.082 | 0.151 | 0.03 | 134 | 1.34x |
| mut-odo | 0.085 | 0.179 | 0.04 | 125 | 1.00x |
| **bq-mut-runs-mulback** | **0.086** | 0.130 | 0.06 | 135 | 1.34x |
| bq-mut-runs | 0.093 | 0.166 | 0.05 | 131 | 1.34x |
| bq-odo-mulback | 0.109 | 0.131 | 0.04 | 127 | 2.72x |
| build | 0.110 | 0.239 | 0.69 | 122 | 1.00x |
| offtab | 0.112 | 0.189 | 0.07 | 124 | 2.00x |
| **bq-scan-packed-mulback** | **0.118** | 0.119 | 0.05 | 126 | 2.00x |
| offtab32 | 0.130 | 0.224 | 0.05 | 122 | 1.50x |
| bq-mut-lemire-out | 0.133 | 0.228 | 0.11 | 123 | 1.34x |
| bq-expand32-lemire-mulback | 0.134 | 0.220 | 0.03 | 125 | 2.47x |
| bq-expand-lemire-out | 0.135 | 0.222 | 0.04 | 125 | 3.22x |
| bq-expand-lemire-mulback | 0.136 | 0.223 | 0.02 | 125 | 3.22x |
| bq-expand-qr-prim | 0.144 | 0.231 | 0.04 | 124 | 3.22x |
| bq-expand-b | 0.144 | 0.233 | 0.04 | 124 | 3.22x |
| bq-mut-lemire-mulback | 0.144 | 0.235 | 0.38 | 121 | 1.34x |
| **bq-expand** | **0.145** | 0.234 | 0.05 | 124 | 3.22x |
| *bq-expand-aa-distant* | *0.145* | *0.234* | *0.05* | *124* | *3.22x* |
| *bq-expand-aa-adjacent* | *0.145* | *0.234* | *0.03* | *124* | *3.22x* |
| bq-expand-zf | 0.147 | 0.247 | 0.03 | 124 | 3.22x |
| bq-scan-rem-mulback | 0.147 | 0.149 | 0.02 | 123 | 4.34x |
| **bq-scan-rem-gm-mulback** | **0.151** | 0.151 | 0.05 | 122 | 4.34x |
| bq-scan-mulback | 0.158 | 0.164 | 0.03 | 121 | 4.34x |
| *bq-scan-mulback-aa-adjacent* | *0.159* | *0.164* | *0.06* | *121* | *4.34x* |
| *bq-scan-mulback-aa-distant* | *0.159* | *0.165* | *0.05* | *121* | *4.34x* |
| bq-scan-gm-mulback | 0.167 | 0.169 | 0.03 | 120 | 4.34x |
| bq-mut | 0.172 | 0.266 | 0.10 | 117 | 1.34x |
| offsets-quot | 0.208 | 0.351 | 0.25 | 113 | 5.14x |
| bq-unfold | 0.265 | 0.516 | 0.07 | 107 | 8.18x |
| fused | 0.296 | 0.402 | 0.16 | 108 | 9.14x |
| mut-offsets | 0.337 | 0.464 | 0.38 | 105 | 6.13x |
| offtab-scan | 0.356 | 0.388 | 0.03 | 107 | 11.00x |
| all-expand | 0.393 | 0.544 | 0.05 | 103 | 10.43x |
| bq-gen | 0.427 | 0.644 | 0.09 | 99 | 4.01x |
| backperm | 0.447 | 0.805 | 0.21 | 100 | 15.03x |
| bq-gen-lemire | 0.604 | 1.022 | 0.13 | 91 | 3.34x |
| cm-gather | 0.699 | 0.822 | 0.30 | 93 | 22.82x |
| list (baseline) | 1.000 | 1.000 | 0.21 | 87 | 26.13x |
| unfold-add | 1.109 | 1.303 | 0.07 | 85 | 27.84x |
| gen-quotrem | 1.336 | 1.747 | 0.25 | 80 | 11.00x |
| gen-unsafe | 1.351 | 1.752 | 0.18 | 80 | 11.00x |

Controls: the six A/A pairs deviate by at most 1.0% (`mut-odo-vecdims`
distant, span 8, at 0.9901; both `bq-expand` pairs within 0.03%); the
`sum-only` halves agree at 1.0019 paired; the in-situ term reads 0.9894 and
0.9921 of `sum-only` as medians (`mut-odo-vecdims` and `bq-expand` arms).
One cell ramps (`mut-odo` on
`rev-gather48-src-50`, R2 0.9893).

Provenance: elapsed 0h12m39s, peak 63 MiB in use, 22 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.09 ms per call raw, 3.94 ms net. Per shape, in
the lead's order: `bq-expand` 0.234/0.139/0.093, `bq-scan-packed-mulback`
0.118/0.119/0.085, `bq-scan-rem-gm-mulback` 0.151/0.151/0.086,
`bq-mut-runs-mulback` 0.130/0.068/0.076, `mut-odo-vecdims`
0.089/0.062/0.032.

What the class says: the shipped row is safe (`worst` 0.234) and the ceiling
order holds, but the fastest-pure slot inverts — the whole scan family sinks
under negated strides, `bq-scan-mulback` (0.158) falling behind `bq-expand`
(0.145) where the main set orders them the other way, and `bq-odo-mulback`
(0.109) inherits the lead; within the mutable-scratch pair the GM quotient
overtakes the Lemire one (0.082 against 0.086), the only population where it
does. And the first attempt collapses outright: `gen-quotrem` and
`gen-unsafe` run 1.34–1.35× *slower than `list`*, worst cells at 1.75, with
`unfold-add` at 1.109 and `bq-gen-lemire`'s worst cell crossing 1 (1.022) —
reversal is this class's stress and the per-dimension-arithmetic arms bear
it worst.

**`revsome` — a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89),
`revsome-outer-g48` (`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l`
165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *91* | *3.22x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *117* | *0.00x* |
| **mut-odo-vecdims** | **0.059** | 0.066 | 0.04 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.059* | *0.066* | *0.03* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.060* | *0.066* | *0.07* | *96* | *1.00x* |
| mut-flat | 0.071 | 0.081 | 0.06 | 90 | 1.33x |
| **bq-mut-runs-mulback** | **0.082** | 0.091 | 0.06 | 89 | 1.33x |
| bq-mut-runs-gm-mulback | 0.087 | 0.100 | 0.05 | 87 | 1.33x |
| bq-mut-runs | 0.097 | 0.112 | 0.05 | 86 | 1.33x |
| offtab | 0.109 | 0.163 | 0.24 | 91 | 2.00x |
| **bq-scan-packed-mulback** | **0.113** | 0.121 | 0.07 | 85 | 2.00x |
| bq-odo-mulback | 0.116 | 0.129 | 0.09 | 84 | 2.72x |
| mut-odo | 0.119 | 0.176 | 0.64 | 97 | 1.00x |
| bq-expand32-lemire-mulback | 0.127 | 0.162 | 0.06 | 84 | 2.47x |
| bq-expand-lemire-out | 0.128 | 0.165 | 0.05 | 84 | 3.22x |
| bq-expand-lemire-mulback | 0.129 | 0.166 | 0.03 | 84 | 3.22x |
| bq-expand-qr-prim | 0.134 | 0.175 | 0.08 | 84 | 3.22x |
| bq-expand-b | 0.134 | 0.176 | 0.05 | 84 | 3.22x |
| *bq-expand-aa-distant* | *0.134* | *0.176* | *0.03* | *84* | *3.22x* |
| *bq-expand-aa-adjacent* | *0.134* | *0.176* | *0.06* | *84* | *3.22x* |
| **bq-expand** | **0.134** | 0.176 | 0.06 | 84 | 3.22x |
| bq-expand-zf | 0.137 | 0.184 | 0.06 | 84 | 3.22x |
| bq-scan-rem-mulback | 0.143 | 0.153 | 0.04 | 83 | 4.33x |
| **bq-scan-rem-gm-mulback** | **0.146** | 0.154 | 0.04 | 85 | 4.33x |
| bq-mut-lemire-out | 0.147 | 0.150 | 0.09 | 86 | 1.33x |
| bq-mut-lemire-mulback | 0.148 | 0.177 | 0.28 | 85 | 1.33x |
| bq-scan-mulback | 0.152 | 0.170 | 0.04 | 83 | 4.33x |
| build | 0.153 | 0.176 | 0.03 | 96 | 1.00x |
| *bq-scan-mulback-aa-adjacent* | *0.154* | *0.168* | *0.03* | *83* | *4.33x* |
| *bq-scan-mulback-aa-distant* | *0.155* | *0.168* | *0.03* | *84* | *4.33x* |
| offtab32 | 0.160 | 0.167 | 0.11 | 89 | 1.50x |
| bq-scan-gm-mulback | 0.161 | 0.172 | 0.04 | 84 | 4.33x |
| bq-mut | 0.163 | 0.199 | 0.06 | 84 | 1.33x |
| offsets-quot | 0.249 | 0.274 | 0.07 | 83 | 5.14x |
| bq-unfold | 0.323 | 0.384 | 0.07 | 83 | 8.18x |
| fused | 0.329 | 0.341 | 0.23 | 73 | 9.14x |
| offtab-scan | 0.377 | 0.406 | 0.16 | 65 | 11.00x |
| mut-offsets | 0.379 | 0.399 | 0.10 | 93 | 6.13x |
| all-expand | 0.390 | 0.499 | 0.06 | 68 | 10.43x |
| backperm | 0.431 | 0.694 | 0.12 | 70 | 15.03x |
| bq-gen | 0.466 | 0.529 | 0.03 | 82 | 4.01x |
| bq-gen-lemire | 0.686 | 0.810 | 0.25 | 81 | 3.34x |
| cm-gather | 0.707 | 0.788 | 0.44 | 54 | 22.82x |
| list (baseline) | 1.000 | 1.000 | 0.16 | 47 | 26.13x |
| unfold-add | 1.132 | 1.137 | 0.28 | 46 | 27.84x |
| gen-unsafe | 1.207 | 1.383 | 0.19 | 45 | 11.00x |
| gen-quotrem | 1.221 | 1.426 | 0.33 | 45 | 11.00x |

Controls: the largest A/A deviation is 2.7% published on the
`mut-odo-vecdims` distant pair (0.36% paired — the gap is one capped cell,
on `revsome-outer-g48` as every pair's worst cell here is); the `sum-only`
halves agree at 1.0000; the in-situ term reads 0.9952 and 0.9940 as medians
(`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h12m38s, peak 61 MiB in use, 22 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 3.86 ms per call raw, 3.71 ms net. Per
shape, in the lead's order: `bq-expand` 0.099/0.139/0.176,
`bq-scan-packed-mulback` 0.100/0.121/0.117, `bq-scan-rem-gm-mulback`
0.093/0.154/0.150, `bq-mut-runs-mulback` 0.086/0.070/0.091,
`mut-odo-vecdims` 0.034/0.062/0.066.

What the class says: mixed signs keep the top of the table in the main
set's order; below it the same pattern as under `rev`, milder — the scan
consumers sink, `bq-scan-mulback` (0.152) falling behind `bq-expand`
(0.134), and the first attempt runs 1.21–1.22× behind `list`, worst cells
at 1.4.

**`bcast` — an innermost stride of 0, every run re-reading one element: a
broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.29* | *53* | *1.63x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.036* | *0.071* | *0.07* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.036* | *0.071* | *0.03* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.036** | 0.072 | 0.03 | 59 | 1.00x |
| mut-odo | 0.045 | 0.134 | 0.39 | 62 | 1.00x |
| mut-flat | 0.048 | 0.058 | 0.08 | 52 | 1.13x |
| build | 0.055 | 0.147 | 0.82 | 59 | 1.00x |
| **bq-mut-runs-mulback** | **0.057** | 0.070 | 0.08 | 50 | 1.13x |
| bq-mut-runs-gm-mulback | 0.059 | 0.074 | 0.33 | 49 | 1.13x |
| offtab | 0.066 | 0.138 | 0.65 | 53 | 2.00x |
| bq-mut-runs | 0.071 | 0.090 | 0.05 | 47 | 1.13x |
| offtab32 | 0.076 | 0.166 | 0.46 | 53 | 1.50x |
| bq-mut-lemire-out | 0.077 | 0.137 | 0.34 | 51 | 1.13x |
| bq-odo-mulback | 0.080 | 0.130 | 0.33 | 49 | 1.64x |
| bq-expand32-lemire-mulback | 0.083 | 0.138 | 0.40 | 48 | 1.45x |
| bq-expand-lemire-out | 0.084 | 0.142 | 0.06 | 49 | 1.63x |
| bq-expand-lemire-mulback | 0.085 | 0.144 | 0.08 | 49 | 1.63x |
| bq-mut-lemire-mulback | 0.089 | 0.172 | 0.36 | 49 | 1.13x |
| **bq-scan-packed-mulback** | **0.090** | 0.134 | 0.46 | 46 | 1.38x |
| bq-scan-rem-mulback | 0.093 | 0.171 | 0.45 | 48 | 2.25x |
| bq-expand-zf | 0.094 | 0.146 | 0.35 | 46 | 1.63x |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.172 | 0.49 | 48 | 2.25x |
| bq-expand-qr-prim | 0.095 | 0.152 | 0.34 | 47 | 1.63x |
| **bq-expand** | **0.095** | 0.153 | 0.33 | 47 | 1.63x |
| *bq-expand-aa-adjacent* | *0.095* | *0.153* | *0.37* | *46* | *1.63x* |
| *bq-scan-mulback-aa-adjacent* | *0.098* | *0.196* | *0.47* | *48* | *2.25x* |
| bq-scan-mulback | 0.098 | 0.196 | 0.33 | 49 | 2.25x |
| *bq-scan-mulback-aa-distant* | *0.099* | *0.198* | *0.41* | *49* | *2.25x* |
| bq-mut | 0.102 | 0.166 | 0.33 | 47 | 1.13x |
| bq-expand-b | 0.104 | 0.120 | 0.38 | 46 | 1.63x |
| *bq-expand-aa-distant* | *0.106* | *0.215* | *0.38* | *46* | *1.63x* |
| bq-scan-gm-mulback | 0.107 | 0.200 | 0.47 | 47 | 2.25x |
| mut-offsets | 0.108 | 0.458 | 0.03 | 59 | 2.89x |
| offsets-quot | 0.129 | 0.264 | 0.14 | 47 | 2.52x |
| bq-unfold | 0.157 | 0.390 | 0.07 | 47 | 3.65x |
| fused | 0.204 | 0.358 | 0.90 | 38 | 6.52x |
| bq-gen | 0.221 | 0.246 | 0.40 | 47 | 1.88x |
| bq-gen-lemire | 0.291 | 0.296 | 1.36 | 46 | 1.63x |
| all-expand | 0.303 | 0.545 | 1.02 | 31 | 7.95x |
| offtab-scan | 0.308 | 0.375 | 1.13 | 28 | 11.00x |
| backperm | 0.331 | 0.536 | 0.84 | 26 | 9.84x |
| gen-unsafe | 0.520 | 1.143 | 1.07 | 21 | 9.00x |
| gen-quotrem | 0.524 | 1.164 | 1.10 | 22 | 9.00x |
| cm-gather | 0.622 | 0.838 | 0.54 | 22 | 16.70x |
| list (baseline) | 1.000 | 1.000 | 1.11 | 15 | 22.89x |
| unfold-add | 1.090 | 1.094 | 1.05 | 18 | 23.53x |

Controls: the `bq-expand` distant pair reads 1.1222 — one 41% cell on
`bcast-tall-Mx2`, the largest control deviation anywhere in the run — while
the other five pairs stay within 0.8%; the `sum-only` halves agree at
0.9995; the in-situ term reads 0.9958 and 0.9904 as medians
(`mut-odo-vecdims` and `bq-expand` arms). Five cells
ramp, all on `bcast-inner900` — the scan family and `backperm`, worst
`bq-scan-packed-mulback` at R2 0.9467 — where 1.8M elements re-read a
2000-element backing.

Provenance: elapsed 0h12m43s, peak 129 MiB in use, 47 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 51.8 ms per call raw, 50.7 ms net. Per shape,
in the lead's order: `bq-expand` 0.113/0.050/0.153,
`bq-scan-packed-mulback` 0.096/0.057/0.134, `bq-scan-rem-gm-mulback`
0.112/0.044/0.172, `bq-mut-runs-mulback` 0.070/0.039/0.064,
`mut-odo-vecdims` 0.044/0.015/0.072.

What the class says — at arm's length, its floor being 12% by the letter:
the shipped row is safe (`worst` 0.153, its own CI ordinary) and every ratio
sits far below the main set's, `list` paying its cons-list walk on data the
strategies read from cache. The fastest-pure slot goes to `bq-odo-mulback`
(0.080) as under `rev`; `mut-odo` climbs to second overall (0.045);
`bq-expand`'s allocation tier drops to 1.63x on the class's small `m`
(2,000–6,400 against `l` in the hundreds of thousands), the `m`-tier effect
the third property predicts; and `gen-quotrem` *beats* `list` at 0.524 here,
the stride-0 read being the one place the first attempt's arithmetic is
cheaper than the list's allocation.

**`bcastmid` — the stretched axis in the middle instead: stride 0 on an
outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *86* | *2.68x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *106* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *113* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *113* | *0.00x* |
| **mut-odo-vecdims** | **0.045** | 0.068 | 0.03 | 95 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.069* | *0.04* | *95* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.047* | *0.068* | *0.03* | *94* | *1.00x* |
| mut-odo | 0.054 | 0.140 | 0.27 | 92 | 1.00x |
| mut-flat | 0.069 | 0.081 | 0.04 | 90 | 1.17x |
| build | 0.078 | 0.192 | 0.07 | 87 | 1.00x |
| **bq-mut-runs-mulback** | **0.081** | 0.093 | 0.53 | 88 | 1.17x |
| bq-mut-runs-gm-mulback | 0.087 | 0.104 | 0.04 | 87 | 1.17x |
| offtab | 0.092 | 0.170 | 1.12 | 86 | 2.00x |
| **bq-scan-packed-mulback** | **0.097** | 0.120 | 0.04 | 86 | 1.52x |
| bq-mut-lemire-out | 0.099 | 0.151 | 0.05 | 85 | 1.17x |
| offtab32 | 0.100 | 0.173 | 0.10 | 84 | 1.50x |
| bq-odo-mulback | 0.103 | 0.134 | 0.05 | 84 | 2.25x |
| bq-mut-runs | 0.103 | 0.117 | 0.05 | 84 | 1.17x |
| bq-scan-rem-mulback | 0.113 | 0.153 | 0.05 | 83 | 2.72x |
| bq-mut-lemire-mulback | 0.114 | 0.176 | 0.07 | 83 | 1.17x |
| **bq-scan-rem-gm-mulback** | **0.114** | 0.154 | 0.04 | 83 | 2.72x |
| bq-expand32-lemire-mulback | 0.116 | 0.168 | 0.05 | 82 | 2.21x |
| bq-scan-mulback | 0.116 | 0.166 | 0.15 | 83 | 2.72x |
| bq-expand-lemire-out | 0.116 | 0.170 | 0.04 | 82 | 2.68x |
| *bq-scan-mulback-aa-adjacent* | *0.116* | *0.166* | *0.05* | *83* | *2.72x* |
| *bq-scan-mulback-aa-distant* | *0.116* | *0.167* | *0.04* | *82* | *2.72x* |
| bq-expand-lemire-mulback | 0.117 | 0.171 | 0.06 | 82 | 2.68x |
| bq-scan-gm-mulback | 0.122 | 0.172 | 0.04 | 82 | 2.72x |
| mut-offsets | 0.127 | 0.406 | 0.30 | 79 | 4.39x |
| bq-expand-b | 0.130 | 0.181 | 0.04 | 81 | 2.68x |
| *bq-expand-aa-adjacent* | *0.130* | *0.182* | *0.05* | *81* | *2.68x* |
| **bq-expand** | **0.130** | 0.182 | 0.05 | 81 | 2.68x |
| bq-expand-qr-prim | 0.130 | 0.182 | 0.13 | 81 | 2.68x |
| *bq-expand-aa-distant* | *0.131* | *0.184* | *0.03* | *81* | *2.68x* |
| bq-expand-zf | 0.133 | 0.189 | 0.05 | 80 | 2.68x |
| bq-mut | 0.140 | 0.208 | 0.23 | 80 | 1.17x |
| offsets-quot | 0.166 | 0.285 | 0.14 | 76 | 3.93x |
| bq-unfold | 0.209 | 0.439 | 0.24 | 73 | 5.77x |
| bq-gen | 0.231 | 0.522 | 0.41 | 71 | 2.87x |
| fused | 0.256 | 0.349 | 0.17 | 70 | 7.93x |
| bq-gen-lemire | 0.291 | 0.783 | 0.16 | 67 | 2.53x |
| all-expand | 0.362 | 0.516 | 0.34 | 64 | 9.60x |
| offtab-scan | 0.367 | 0.378 | 0.22 | 64 | 11.00x |
| backperm | 0.399 | 0.754 | 0.46 | 62 | 14.20x |
| cm-gather | 0.681 | 0.811 | 0.52 | 53 | 18.86x |
| list (baseline) | 1.000 | 1.000 | 0.17 | 46 | 24.45x |
| unfold-add | 1.054 | 1.187 | 0.30 | 46 | 25.60x |
| gen-unsafe | 1.121 | 1.281 | 0.24 | 44 | 11.00x |
| gen-quotrem | 1.122 | 1.293 | 0.23 | 44 | 11.00x |

Controls: the largest A/A deviation is 3.7% — and it is the *adjacent*
`mut-odo-vecdims` pair, a 7.6% cell on `bcastmid-primes`, so this class's
`mut-odo-vecdims` cells carry a local disturbance; its in-situ term says the
same (0.9602 median against `bq-expand`'s 0.9934). The other five pairs stay
within 0.4% and the `sum-only` halves agree at 0.9972.

Provenance: elapsed 0h8m25s, peak 39 MiB in use, 12 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the bcastmid class. Anchor:
`bcastmid-primes`, `list` at 4.05 ms per call raw, 3.90 ms net.

What the class says: the main ordering holds whole — read `mut-odo-vecdims`'s
lead from its twins (0.045–0.047), per the controls above.

**`reshape1` — the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *64* | *6.27x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.04* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| mut-flat | 0.027 | 0.027 | 0.03 | 90 | 2.00x |
| **bq-mut-runs-mulback** | **0.028** | 0.028 | 0.04 | 90 | 2.00x |
| bq-mut-runs-gm-mulback | 0.033 | 0.037 | 0.05 | 87 | 2.00x |
| bq-mut-runs | 0.076 | 0.077 | 0.05 | 76 | 2.00x |
| *mut-odo-vecdims-aa-distant* | *0.101* | *0.102* | *0.04* | *72* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.101* | *0.102* | *0.10* | *72* | *1.00x* |
| **mut-odo-vecdims** | **0.105** | 0.108 | 0.05 | 71 | 1.00x |
| bq-odo-mulback | 0.130 | 0.132 | 0.15 | 68 | 6.10x |
| **bq-scan-packed-mulback** | **0.135** | 0.141 | 0.17 | 67 | 4.00x |
| bq-expand32-lemire-mulback | 0.143 | 0.146 | 0.05 | 66 | 4.68x |
| bq-expand-lemire-mulback | 0.149 | 0.153 | 0.04 | 66 | 6.27x |
| bq-expand-b | 0.164 | 0.191 | 0.19 | 64 | 5.77x |
| bq-expand-lemire-out | 0.168 | 0.173 | 0.03 | 64 | 6.27x |
| bq-expand-zf | 0.179 | 0.186 | 0.07 | 62 | 6.27x |
| bq-mut-lemire-out | 0.186 | 0.195 | 0.15 | 62 | 2.00x |
| *bq-expand-aa-adjacent* | *0.188* | *0.191* | *0.11* | *62* | *6.27x* |
| bq-expand-qr-prim | 0.188 | 0.192 | 0.04 | 62 | 6.27x |
| **bq-expand** | **0.188** | 0.192 | 0.06 | 62 | 6.27x |
| *bq-expand-aa-distant* | *0.188* | *0.192* | *0.13* | *62* | *6.27x* |
| bq-mut-lemire-mulback | 0.190 | 0.203 | 0.10 | 62 | 2.00x |
| bq-scan-rem-mulback | 0.199 | 0.199 | 0.16 | 61 | 11.00x |
| **bq-scan-rem-gm-mulback** | **0.200** | 0.201 | 0.14 | 61 | 11.00x |
| mut-odo | 0.220 | 0.259 | 1.12 | 60 | 1.00x |
| offtab | 0.229 | 0.258 | 0.19 | 58 | 2.00x |
| offtab-scan | 0.236 | 0.242 | 0.31 | 58 | 11.00x |
| bq-scan-gm-mulback | 0.239 | 0.243 | 0.21 | 58 | 11.00x |
| bq-scan-mulback | 0.239 | 0.244 | 0.24 | 58 | 11.00x |
| *bq-scan-mulback-aa-distant* | *0.239* | *0.244* | *0.17* | *58* | *11.00x* |
| *bq-scan-mulback-aa-adjacent* | *0.240* | *0.245* | *0.16* | *58* | *11.00x* |
| bq-mut | 0.244 | 0.269 | 0.98 | 57 | 2.00x |
| offtab32 | 0.256 | 0.269 | 1.22 | 57 | 1.50x |
| build | 0.278 | 0.288 | 0.04 | 55 | 1.00x |
| offsets-quot | 0.394 | 0.411 | 0.22 | 49 | 13.21x |
| fused | 0.440 | 0.441 | 0.35 | 48 | 17.21x |
| bq-gen | 0.482 | 0.661 | 0.39 | 46 | 8.00x |
| gen-quotrem | 0.572 | 0.743 | 0.37 | 42 | 9.00x |
| gen-unsafe | 0.592 | 0.795 | 0.26 | 42 | 9.00x |
| bq-unfold | 0.592 | 0.596 | 0.47 | 42 | 22.28x |
| bq-gen-lemire | 0.643 | 0.960 | 1.03 | 41 | 6.00x |
| all-expand | 0.700 | 0.725 | 0.55 | 40 | 17.81x |
| mut-offsets | 0.732 | 0.748 | 0.28 | 39 | 16.20x |
| backperm | 0.852 | 0.947 | 1.55 | 36 | 19.87x |
| cm-gather | 0.994 | 1.019 | 0.35 | 34 | 38.81x |
| list (baseline) | 1.000 | 1.000 | 0.23 | 34 | 36.21x |
| unfold-add | 1.276 | 1.299 | 0.50 | 31 | 41.28x |

Controls: both `mut-odo-vecdims` pairs read ~0.966 — the *base* arm slower
than both its twins, worst cells ~7% on `reshape1-r3`, the adjacent
interval missing 1 — so the disturbance sits at the base's slot and the
class's floor is 3.5%; the same arm's in-situ term scatters 33% per cell
while `bq-expand`'s reads 1.0003. The `sum-only` halves agree at 1.0024.

Provenance: elapsed 0h8m25s, peak 68 MiB in use, 23 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 12.4 ms per call raw, 12.1 ms net.

What the class says: the top inverts completely, and by construction — with
`sInner` 1 every run is one element, so the flat fills win outright
(`mut-flat` 0.027, `bq-mut-runs-mulback` 0.028, a mutable-`Int`-scratch arm
effectively tying the class-method tier), the odometer fills pay a full
odometer step per element (`mut-odo` 0.220, `build` 0.278) and
`mut-odo-vecdims` lands mid-table (0.105). The scan builders hit `m = l`:
11.00x allocation and rows at 0.24, the third property's `m`-tier effect at
its other extreme. `bq-expand` posts its weakest class geomean (0.188,
`worst` 0.192) and is still five times under `list`; `cm-gather`'s worst
cell crosses 1 (1.019). This is [the `sInner`
ruling][pershape]'s extreme case, mechanism rather than scatter.

**`slice` — a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes`
(`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *86* | *2.73x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *1.58* | *106* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *113* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *113* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.047* | *0.069* | *0.02* | *94* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.047* | *0.069* | *0.02* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.047** | 0.069 | 0.04 | 94 | 1.00x |
| mut-odo | 0.060 | 0.127 | 0.05 | 90 | 1.00x |
| mut-flat | 0.077 | 0.085 | 0.04 | 89 | 1.17x |
| build | 0.077 | 0.174 | 0.09 | 88 | 1.00x |
| **bq-mut-runs-mulback** | **0.088** | 0.096 | 0.44 | 88 | 1.17x |
| bq-mut-runs-gm-mulback | 0.093 | 0.105 | 0.48 | 86 | 1.17x |
| offtab | 0.093 | 0.158 | 0.06 | 86 | 2.00x |
| bq-mut-runs | 0.103 | 0.117 | 0.05 | 84 | 1.17x |
| **bq-scan-packed-mulback** | **0.105** | 0.121 | 0.11 | 84 | 1.52x |
| offtab32 | 0.106 | 0.179 | 0.09 | 84 | 1.50x |
| bq-mut-lemire-out | 0.111 | 0.160 | 0.55 | 83 | 1.17x |
| bq-odo-mulback | 0.112 | 0.136 | 0.11 | 84 | 2.25x |
| **bq-scan-rem-gm-mulback** | **0.116** | 0.155 | 0.04 | 83 | 2.72x |
| bq-mut-lemire-mulback | 0.122 | 0.176 | 0.97 | 82 | 1.17x |
| bq-scan-rem-mulback | 0.122 | 0.154 | 0.03 | 82 | 2.72x |
| bq-scan-gm-mulback | 0.124 | 0.173 | 0.06 | 82 | 2.72x |
| bq-expand32-lemire-mulback | 0.125 | 0.169 | 0.05 | 82 | 2.24x |
| bq-expand-lemire-out | 0.125 | 0.172 | 0.06 | 82 | 2.73x |
| *bq-scan-mulback-aa-adjacent* | *0.125* | *0.168* | *0.11* | *82* | *2.72x* |
| *bq-scan-mulback-aa-distant* | *0.126* | *0.169* | *0.11* | *82* | *2.72x* |
| bq-expand-lemire-mulback | 0.126 | 0.173 | 0.04 | 82 | 2.73x |
| bq-scan-mulback | 0.126 | 0.168 | 0.10 | 82 | 2.72x |
| bq-expand-qr-prim | 0.130 | 0.182 | 0.05 | 81 | 2.73x |
| bq-expand-b | 0.130 | 0.183 | 0.04 | 81 | 2.73x |
| *bq-expand-aa-adjacent* | *0.130* | *0.182* | *0.05* | *81* | *2.73x* |
| **bq-expand** | **0.130** | 0.183 | 0.05 | 81 | 2.73x |
| *bq-expand-aa-distant* | *0.130* | *0.183* | *0.03* | *81* | *2.73x* |
| bq-expand-zf | 0.134 | 0.190 | 0.08 | 80 | 2.73x |
| mut-offsets | 0.137 | 0.408 | 0.14 | 78 | 4.39x |
| bq-mut | 0.141 | 0.212 | 0.63 | 80 | 1.17x |
| offsets-quot | 0.166 | 0.285 | 0.14 | 76 | 3.93x |
| bq-unfold | 0.203 | 0.409 | 0.14 | 74 | 5.77x |
| bq-gen | 0.230 | 0.519 | 0.23 | 70 | 2.87x |
| fused | 0.256 | 0.349 | 0.13 | 70 | 7.93x |
| bq-gen-lemire | 0.293 | 0.772 | 0.20 | 66 | 2.53x |
| all-expand | 0.362 | 0.507 | 0.23 | 64 | 9.52x |
| offtab-scan | 0.369 | 0.380 | 0.20 | 64 | 11.00x |
| backperm | 0.394 | 0.698 | 0.14 | 62 | 14.07x |
| cm-gather | 0.645 | 0.790 | 0.50 | 54 | 18.92x |
| list (baseline) | 1.000 | 1.000 | 0.21 | 46 | 24.45x |
| unfold-add | 1.049 | 1.183 | 0.52 | 46 | 25.60x |
| gen-quotrem | 1.119 | 1.294 | 0.54 | 44 | 11.00x |
| gen-unsafe | 1.126 | 1.280 | 1.41 | 44 | 11.00x |

Controls: the quietest process of the run — every A/A pair within 0.5%, the
`sum-only` halves at 0.9994; the `mut-odo-vecdims` in-situ median reads
0.9343 (its `-nosum` arm the process's one noisy bench, CI% 1.58) against
`bq-expand`'s 0.9893.

Provenance: elapsed 0h8m25s, peak 66 MiB in use, 26 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.08 ms per call raw, 3.93 ms net.

What the class says: a non-zero offset changes nothing — the main ordering
reproduces whole, which is itself the result.

**`window` — overlapping im2col patches: the workload this page opens by
naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *100* | *3.32x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.06* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *132* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *132* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.060* | *0.065* | *0.05* | *111* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.060* | *0.065* | *0.04* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.060** | 0.065 | 0.03 | 111 | 1.00x |
| mut-flat | 0.075 | 0.080 | 0.04 | 108 | 1.27x |
| **bq-mut-runs-mulback** | **0.085** | 0.086 | 0.12 | 106 | 1.27x |
| bq-mut-runs-gm-mulback | 0.094 | 0.098 | 0.09 | 104 | 1.27x |
| bq-mut-runs | 0.109 | 0.111 | 0.44 | 102 | 1.27x |
| **bq-scan-packed-mulback** | **0.113** | 0.116 | 0.02 | 102 | 1.80x |
| mut-odo | 0.116 | 0.131 | 0.17 | 102 | 1.00x |
| bq-odo-mulback | 0.123 | 0.131 | 0.14 | 101 | 2.87x |
| bq-mut-lemire-out | 0.140 | 0.143 | 0.06 | 98 | 1.27x |
| bq-scan-rem-mulback | 0.141 | 0.151 | 0.10 | 98 | 3.67x |
| **bq-scan-rem-gm-mulback** | **0.144** | 0.152 | 0.11 | 98 | 3.67x |
| bq-expand32-lemire-mulback | 0.145 | 0.160 | 0.02 | 98 | 2.70x |
| offtab | 0.145 | 0.166 | 1.23 | 99 | 2.00x |
| bq-expand-lemire-out | 0.147 | 0.162 | 0.02 | 98 | 3.32x |
| bq-expand-lemire-mulback | 0.148 | 0.163 | 0.02 | 98 | 3.32x |
| *bq-scan-mulback-aa-adjacent* | *0.152* | *0.164* | *0.09* | *97* | *3.67x* |
| bq-scan-mulback | 0.153 | 0.164 | 0.11 | 97 | 3.67x |
| bq-mut-lemire-mulback | 0.158 | 0.160 | 0.17 | 97 | 1.27x |
| bq-scan-gm-mulback | 0.159 | 0.169 | 0.09 | 96 | 3.67x |
| build | 0.159 | 0.182 | 1.78 | 97 | 1.00x |
| bq-expand-b | 0.159 | 0.173 | 0.05 | 96 | 3.32x |
| *bq-expand-aa-distant* | *0.159* | *0.174* | *0.06* | *96* | *3.32x* |
| *bq-expand-aa-adjacent* | *0.159* | *0.174* | *0.06* | *96* | *3.32x* |
| **bq-expand** | **0.159** | 0.174 | 0.04 | 96 | 3.32x |
| bq-expand-qr-prim | 0.160 | 0.172 | 0.03 | 96 | 3.32x |
| bq-expand-zf | 0.164 | 0.181 | 0.04 | 96 | 3.32x |
| *bq-scan-mulback-aa-distant* | *0.168* | *0.199* | *0.21* | *96* | *3.67x* |
| offtab32 | 0.173 | 0.184 | 0.21 | 95 | 1.50x |
| bq-mut | 0.175 | 0.187 | 0.22 | 95 | 1.27x |
| offsets-quot | 0.254 | 0.266 | 0.12 | 88 | 5.35x |
| fused | 0.325 | 0.335 | 0.16 | 84 | 9.35x |
| mut-offsets | 0.331 | 0.373 | 0.34 | 84 | 6.08x |
| bq-unfold | 0.346 | 0.384 | 0.08 | 83 | 8.13x |
| offtab-scan | 0.362 | 0.388 | 0.19 | 82 | 11.00x |
| bq-gen | 0.364 | 0.391 | 0.16 | 82 | 3.40x |
| all-expand | 0.475 | 0.576 | 0.84 | 78 | 11.27x |
| bq-gen-lemire | 0.539 | 0.589 | 0.61 | 75 | 2.87x |
| backperm | 0.584 | 0.667 | 0.22 | 74 | 15.89x |
| cm-gather | 0.752 | 0.796 | 0.30 | 70 | 21.13x |
| list (baseline) | 1.000 | 1.000 | 0.16 | 64 | 26.15x |
| unfold-add | 1.160 | 1.193 | 0.75 | 62 | 27.87x |
| gen-unsafe | 1.236 | 1.566 | 0.13 | 61 | 11.00x |
| gen-quotrem | 1.245 | 1.584 | 0.22 | 60 | 11.00x |

Controls: the `bq-scan-mulback` distant pair reads 1.1003 — one 21.5% cell
on `window-224x224-k3` — while every other pair sits within 0.25%, the
sharpest one-wild-cell floor of the run; the `sum-only` halves agree at
0.9999; the in-situ term reads 0.9965 and 0.9953 as medians
(`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h8m24s, peak 57 MiB in use, 17 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.17 ms per call raw, 8.90 ms net.

What the class says: the ordering holds whole, and the figure this class
exists for is the shipped row against the main set's — 0.159 here, 0.127
there. The overlap the main set drops *lifts* every ratio rather than
lowering it, so the main set was flattering the fallback's standing against
`list`, not selling it short, and the pessimism this page once recorded was
about absolute cost only.

**`scaled` — superincreasing strides, none of them 1: a hand-built
dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30),
`scaled-rank1-m1` (`l` 300000, `sInner` 300000 — rank 1, so `m` is 1 and
the whole view is one strided run).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *103* | *1.11x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.27* | *126* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| mut-odo | 0.028 | 0.029 | 0.05 | 110 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.030* | *0.034* | *0.05* | *110* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.031* | *0.034* | *0.04* | *110* | *1.00x* |
| **mut-odo-vecdims** | **0.031** | 0.034 | 0.06 | 110 | 1.00x |
| build | 0.035 | 0.043 | 0.15 | 108 | 1.00x |
| mut-offsets | 0.047 | 0.078 | 0.06 | 105 | 1.26x |
| offtab | 0.054 | 0.056 | 0.06 | 104 | 2.00x |
| mut-flat | 0.061 | 0.062 | 0.07 | 102 | 1.02x |
| offtab32 | 0.062 | 0.069 | 0.07 | 102 | 1.50x |
| bq-mut-lemire-out | 0.070 | 0.076 | 0.21 | 100 | 1.02x |
| **bq-mut-runs-mulback** | **0.075** | 0.076 | 0.04 | 100 | 1.02x |
| bq-mut-runs-gm-mulback | 0.077 | 0.078 | 0.06 | 100 | 1.02x |
| bq-mut-lemire-mulback | 0.080 | 0.087 | 0.08 | 99 | 1.02x |
| bq-odo-mulback | 0.083 | 0.087 | 0.05 | 98 | 1.09x |
| **bq-scan-packed-mulback** | **0.084** | 0.088 | 0.05 | 98 | 1.05x |
| bq-expand-lemire-out | 0.084 | 0.088 | 0.03 | 98 | 1.11x |
| bq-expand-lemire-mulback | 0.085 | 0.090 | 0.05 | 98 | 1.11x |
| bq-expand32-lemire-mulback | 0.085 | 0.090 | 0.05 | 98 | 1.07x |
| *bq-scan-mulback-aa-distant* | *0.086* | *0.093* | *0.04* | *98* | *1.17x* |
| *bq-scan-mulback-aa-adjacent* | *0.086* | *0.093* | *0.02* | *98* | *1.17x* |
| bq-scan-mulback | 0.086 | 0.094 | 0.05 | 98 | 1.17x |
| bq-scan-rem-mulback | 0.088 | 0.094 | 0.06 | 98 | 1.17x |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.095 | 0.03 | 98 | 1.17x |
| bq-scan-gm-mulback | 0.092 | 0.099 | 0.04 | 97 | 1.17x |
| bq-mut-runs | 0.094 | 0.096 | 0.03 | 97 | 1.02x |
| *bq-expand-aa-distant* | *0.097* | *0.102* | *0.04* | *96* | *1.11x* |
| bq-expand-b | 0.097 | 0.102 | 0.04 | 96 | 1.11x |
| bq-expand-qr-prim | 0.097 | 0.102 | 0.04 | 96 | 1.11x |
| *bq-expand-aa-adjacent* | *0.097* | *0.102* | *0.04* | *96* | *1.11x* |
| **bq-expand** | **0.097** | 0.102 | 0.05 | 96 | 1.11x |
| bq-expand-zf | 0.098 | 0.103 | 0.07 | 96 | 1.11x |
| bq-mut | 0.099 | 0.106 | 0.06 | 96 | 1.02x |
| offsets-quot | 0.103 | 0.115 | 0.13 | 96 | 1.21x |
| bq-unfold | 0.109 | 0.129 | 0.16 | 94 | 1.36x |
| bq-gen | 0.112 | 0.137 | 0.05 | 94 | 1.12x |
| bq-gen-lemire | 0.121 | 0.157 | 0.11 | 93 | 1.08x |
| fused | 0.195 | 0.202 | 0.15 | 86 | 5.21x |
| backperm | 0.209 | 0.250 | 0.09 | 84 | 7.04x |
| all-expand | 0.264 | 0.277 | 0.06 | 80 | 5.73x |
| offtab-scan | 0.397 | 0.401 | 0.19 | 73 | 11.00x |
| cm-gather | 0.582 | 0.637 | 1.94 | 66 | 14.28x |
| gen-quotrem | 0.716 | 1.169 | 0.19 | 62 | 7.00x |
| gen-unsafe | 0.720 | 1.171 | 0.16 | 62 | 7.00x |
| unfold-add | 0.977 | 1.029 | 0.21 | 57 | 21.34x |
| list (baseline) | 1.000 | 1.000 | 0.23 | 57 | 21.26x |

Controls: every A/A pair within 0.8%; the `sum-only` halves agree at
1.0013; the `mut-odo-vecdims` in-situ median reads 0.9387 (worst cell 11.7%
on `scaled-rank1-m1`) against `bq-expand`'s 0.9923.

Provenance: elapsed 0h8m26s, peak 252 MiB in use, 26 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.80 ms per call raw, 4.62 ms net.

What the class says: the ceiling inverts within itself — `mut-odo` (0.028)
ahead of `mut-odo-vecdims` (0.031), past this process's 0.8% floor — and
the pure lead passes to `bq-odo-mulback` by a hair too
(0.083 against `bq-scan-packed-mulback`'s 0.084, a margin no floor
licenses). The allocation tiers collapse toward 1 (`bq-expand` 1.11x, the
scan rows 1.17x), the `m`-tier effect at its floor — `m` of 1 and 2,000
makes every table free — which also lets the `l`-table arms shine
(`mut-offsets` 0.047, `offtab` 0.054). `gen-quotrem` beats `list` at 0.716
on the geomean while its `worst` still crosses 1 (1.169), and `unfold-add`
reaches its only sub-1 geomean (0.977).


### Provenance

The run's name, regime, scale and source commit are at the head of this
chapter; what follows is what they have to be read against. The commit is
recorded there because a run whose artifact is deleted and whose source is
unrecorded cannot be repeated even in principle.

Run 7 is the closest thing to a repeat measurement this page has had, as the
previous version of this section predicted: it kept Run 6's regime and
measured its surviving shapes, so the shared-shape comparison in [What Run 8
compares against](#what-run-8-compares-against) is like-for-like but for the
roster — whose own effect the six crossed controls price — and for the
scratch conversion, a code change whose probe predicted the `bq-expand` move
the run then showed. Against Run 6's *published* column the discontinuity
stands as ever, a different shape set making `alloc` and `time` statistics
of a different population. Run 8 gives the closeness up again, changing the
regime with everything else held still.

The desktop named at the head of this chapter is the same machine whose
`idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and
should say which machine here.

**And the ground has not moved since**, for the first time in this page's
history: Run 7 measured exactly the shapes and roster `Main.hs` holds today,
in every population, so Run 8 inherits a pinned set everywhere.

**The delta, so the population is recoverable.** What follows is the *only*
form in which a shape set or roster is recorded here: its difference from
whatever `Main.hs` holds now. A snapshot would need rewriting at every change
and would be a second copy of a list that already exists; a delta costs what
actually moved and shrinks to nothing when the two agree.

- Run 7's delta is empty: today's shapes, today's roster, today's class
  lists, winsorized per the estimator under `time`.
- Run 6, whose yardstick figures [What Run 8 compares
  against](#what-run-8-compares-against) still quotes, measured today's
  main-set shapes **minus `stretch-pow2stride` and `stretch-inner256`, plus
  eleven since dropped**
  (`cnn-L1-12x12-c1`, `cnn-L2-12x12-c16`, `cnn-slice-c64`,
  `lenet-L2-14-c6-k5`,
  `mnist-28-c1-k3`, `cifar-L1-32-c3-k3`, `cifar-L3-8-c128-k3`,
  `cifar-32-c3-k5`, `vgg-14-c256-k3`, `deep-7-c512-k3`, `slice-c512`), on
  today's roster **minus five arms** (the three crossed A/A twins and the
  two `-nosum` controls), trimmed rather than winsorized, on the Storable
  scratch the conversion since replaced, and with no stride class in
  existence. That is the whole chain between its figures and this run's.

**The anchor, so a moved baseline is visible.** Every published figure is a
ratio to `list`, so a change in `list` itself — a new compiler, a new machine,
a changed `toListT` — rescales the whole table while leaving every ratio
intact and undetectable. These three absolute per-call figures are the
guard — against Run 6's they moved ~1%, which is what cleared `list` when
`gen-quotrem` closed on it:

| shape | `l` | `list`, per call | net of the forcing pass |
|---|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.00 µs | 5.83 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.64 ms | 3.55 ms |
| `stretch-wide-2xM` | 1800000 | 37.3 ms | 36.2 ms |

Each stride class carries an anchor of its own, beside its table: these three
would not move at all if `list` changed for one mechanism only — under
negative strides, say, or a stride-0 read — which is exactly the change a
population of ratios cannot show.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.588–0.604 ns per element across the whole set, median
0.601, so a raw slope is the published one plus about `0.60e-9 * l`, with `l`
from `Main.hs`. That recovers any uncorrected figure to within the term's own
3% spread — enough to hold a corrected run against any number
measured before the correction existed.

**What the next run replaces.** Run 7's numbers reach past the Results table,
so this is the list to walk when Run 8's land. It names *sections*, not
figures: a list of figures is a second copy of them, and enumerating it was
how the previous two versions of this list went stale — one missing six
sections, its predecessor leaking past it. What now guarantees completeness is
mechanical instead. Every section below is reached by an anchor, and the
coverage check is: no section carrying a figure outside a table may be absent
from these links. Run that check, and repeat the two sweeps it cannot replace
— grep this file for figure-shaped numerals outside the tables, and grep it
for `Run 7` — before trusting the list.

- [the head of this chapter](#about-the-last-run-run-7), which carries the run's
  name, regime, scale and source commit;
- [the Results table](#results), which `--markdown` emits whole;
- [What Run 8 compares against](#what-run-8-compares-against) — the yardstick
  geomeans and the two-column per-shape fingerprint, both of which a run
  replaces wholesale, and which are the only per-shape record kept once the
  JSON is deleted;
- [The claims Run 8 should test](#the-claims-run-8-should-test), where a run
  reports which held rather than re-deriving them, and whose readings are
  run figures throughout;
- [the noise-floor table][floor] and its prose, from `--aa` — including the
  raw-slope six it compares against, and the position verdict the crossed
  controls decided;
- [the opening section][opening]'s headline ratios;
- [The stride classes, run by run](#the-stride-classes-run-by-run) — the
  summary table, and each class's own table, controls, provenance, anchor and
  paragraph. All of that is a run's, in the way the Results table is; the
  layout above them is not, in the way the column definitions are not. A run
  that leaves a population out says so there, rather than leaving the previous
  run's table standing under a new run's name;
- [The mutable ceiling (not taken)](#the-mutable-ceiling-not-taken) and the
  shipping paragraph closing [the Lemire section][lemire]. These are
  *rulings resting on figures*, so a stale number re-opens a decision rather
  than merely misreporting one — and a ruling's number moves for reasons its
  verdict does not. Every decision-bearing ratio was checked in both columns
  when the correction landed: none changed direction, but magnitudes moved by
  up to +31%, because subtracting a shared term inflates a ratio the more the
  arms it compares are fast. Requote from the run; do not carry forward;
- [The C-gap](#the-c-gap-still-a-deeper-ceiling), whose figures are
  horde-ad's, not a run's: no run here replaces them, and they move when
  that repo re-measures — so the walk checks their currency instead;
- [The scratch vector flavour](#the-scratch-vector-flavour), whose figures
  are a probe's too, and whose conversion is why no `bq-*` figure predating
  it is comparable with one after it;
- [One element type](#one-element-type-and-what-the-probe-found), whose
  figures are a probe's and which no run replaces either. What would call for
  re-probing is a run that moves the ordering at `Storable Double`, since the
  claim is that the other types follow it;
- [sum-only](#sum-only-and-the-correction-now-applied), where what a run
  decides is no longer *whether* to correct but whether the term still passes
  its three gates, any failure invalidating the column rather than informing
  it;
- [R2 is the ramp detector][ramp], [the Lemire section][lemire], and
  [the per-shape `stretch-*` table][pershape];
- the `alloc` column's shape-dependence, refuted and confirmed refuted at full
  budget: every multiple quoted anywhere is a property of a strategy *and* a
  shape set, so pin the shape set before comparing across runs, as `time`
  already asks;
- [What the next runs have to decide](#what-the-next-runs-have-to-decide),
  whose whole content is questions a run answers and figures a run moves;
- this section, which becomes the next run's own provenance;
- `read-run.py`'s docstring, whose `time`, `corr` and `net` definitions and
  A/A paragraph quote the run;
- `micro.cabal`'s `-M2G` note, if the printed heap peaks have moved;
- `Main.hs`, wherever a comment cites a figure — now `fbBQmutRunsGmMulback`'s
  margin over its control and `fbBQscanMulback`'s prediction for Run 8, every
  other comment having been rewritten to name an ordering and point here for
  the number. The `diag` allocations at `baseOffsetsScan` and
  `baseOffsetsScanPacked` move with the regime rather than with a run.

**And what a run does not touch.** The converse of that list is worth stating,
because a session told to make a run will reach for everything: a new
measurement bears on figures and on rulings whose figures moved, and on
nothing else. It does not bear on the *reasoning* behind a decision, on the
ideas recorded as having died on paper, on the shape-set, roster and
stride-class rulings, or on the account of how the fix was found. Those
change when an argument changes, which a run is not. If a run seems to call
for rewriting one of them, that is a finding worth its own paragraph, not an
edit to be folded in quietly.

How a run is made, and what to record beside its numbers, is [Making a major
benchmark run](#making-a-major-benchmark-run) — which is also where the walk
of the list above is one of the steps.


### What the next runs have to decide

The open questions, each with the measurement that would settle it and the
run that can supply it, collected here because they otherwise sit one per
section and get reconstructed every time.

**Run 7 answered its six** — position is the floor's mechanism, following
the slot across all three crossed strategies ([the floor][floor]); the floor
is real and structured, ~1% between roster neighbours and ~4% across it; the
halved shape set moved geomeans but no ordering the page treats as real, the
one casualty (`gen-quotrem` closing on `list`) being the two new shapes'
doing and visible within Run 7 alone; the shipped fallback is never slower
than `list` in any class; four classes invert an ordering, `rev` and `bcast`
on the pure side, `reshape1` and `scaled` at the ceiling, each with a
structural reading in [its block](#the-stride-classes-run-by-run); and the
window class prices the main set's overlap pessimism — absolute cost only,
the ratios lifting instead.

**Run 8 answers one**, and gives up cross-run margins to do it:

- **Does SpecConstr invert the scan family?** `baseOffsetsScan` boxes its
  stream state at -O1, and its allocation half is now measured **in Run 8's
  own regime rather than at -O2**: a `diag` at `--ghc-options=-fspec-constr`,
  2026-08-08, puts that builder and `baseOffsetsScanRem` at the table and
  nothing else, 10.00x to 1.00x on `vgg-14-c512`. So the flag alone
  dissolves the state and the premise holds; what Run 8 still has to settle
  is the *time*, which no `diag` measures.

  That probe carries three predictions past the one this question was
  written for, so Run 8 is read against them too. `baseOffsetsGen` and
  `baseOffsetsGenLemire` also collapse to the table (11.00x and 9.00x to
  1.00x), so `bq-gen` and `bq-gen-lemire` should fall with the scan rows and
  not only behind them. The expansion builders drop without vanishing
  (8.82x to 5.49x, 36 spare bytes an entry), so `bq-expand`'s own tier
  improves by about a third — a shipped-arm move nothing had predicted.
  And `baseOffsetsOdo` keeps 29 bytes an entry (7.33x to 4.67x) where
  `baseOffsetsScanPacked`, an `unfoldrExactN` like it, goes to 1.00x: the
  un-refutation carries to a produced stream whose state is a bare `Int` and
  not to one whose state is a three-`Int` constructor, so `bq-odo-mulback`
  is predicted *not* to follow the family up. `baseOffsetsMut` and
  `baseOffsetsMutRuns` sit at 1.00x in both regimes, which is the control
  saying the diag itself did not move.

Run 8 keeps the populations Run 7 pins, main set and classes alike, so each
table is readable against its Run 7 counterpart, and the regime is
never confounded with membership.

**The three questions Run 7 raised are answered**, each by the probe its own
entry specified and none by a scheduled run — which is the rule about a
discriminating measurement deserving a filtered run now, observed:

- `bq-scan-packed-mulback`'s +4% is **real, and is the packed table's
  flavour**: unboxing it costs 3.7%, on every shape of the set
  ([the scratch vector flavour](#the-scratch-vector-flavour)).
- `mut-odo-vecdims`'s +9.8% is **not** its dimension vectors' flavour, which
  runs the other way at −3.4% and so deepens the move to about +13% with the
  suspect removed (same section).
- `build` **is free**: its Core is `mut-odo`'s in Run 6's binary and Run 7's
  alike, and the gap does not reproduce in a third
  ([the mutable ceiling](#the-mutable-ceiling-not-taken)).

**What the first two leave is one question, and it needs a full roster**, so
it is the next run's rather than a probe's:

- **What moved `mut-odo-vecdims` by the remaining ~13%?** Not its slot: Run
  7's crossed controls price position at +0.05% to +0.18% a slot
  ([the floor][floor]) and this arm moved three of them. The right size is
  the roster *effect* and code placement — what shares the process and where
  the code lands, rather than where in the order — which the flavour probe
  moved together and by more than enough: its ten-bench process read 0.044
  on this arm where the full roster published 0.054. Two full-roster runs
  differing only in membership would separate them; no probe can, and Run 8
  pins the roster, so nothing scheduled will.

[floor]: #the-noise-floor-is-3-not-the-ci
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[opening]: #regime-3-micro-benchmark-the-fix-bq-expand
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
