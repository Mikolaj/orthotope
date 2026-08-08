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

A direct mutable result buffer is faster still: `mut-odo` walks the outer
odometer and writes each innermost run, and `mut-odo-vecdims` — the same fill
with its dimension lists replaced by unboxed vectors — is on Run 8
(SpecConstr) **1.93×** over `bq-expand` and the fastest strategy measured
here. Both need a new `Vector`-class method, which was
measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal — a bar an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-not-taken), amended). Plain `mut-odo` no longer
argues for it at all: it no longer beats the shipped arm (1.08× the other
way, on an interval covering 1), where Run 7 (Harness), at -O1, had it 1.51×
ahead.

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure one is **`bq-odo-mulback`**, 0.089
against `bq-expand`'s 0.102; the fastest pure one carrying **no size
precondition at all** is `bq-scan-rem-gm-mulback` at 0.090. None is what
`Data/Array/Internal.hs` does today, and the trade-offs — preconditions,
allocation, and a noise floor this run measures at under 2% — are in
[Results](#results) and in
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

And **one regime's**, which Run 8 is the first run to make load-bearing. It
compiled the suite with `-fspec-constr`, where every run before it took the
plain -O1 a default `cabal build` of orthotope takes, and the flag reorders
the table rather than nudging it — it speeds `list` itself by 8%, `bq-expand`
by 27% and the plain scan family by 31%, leaves `bq-mut-runs-mulback` where
it was, and *slows* `mut-odo` by 19% ([the head of the run
chapter](#about-the-last-run-run-8)). So what to ship is decided on Run 7's
regime and what SpecConstr would buy on this one, and a figure quoted from
either says which.

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
  - [The noise floor is the A/A controls, not the CI](#the-noise-floor-is-the-aa-controls-not-the-ci)
  - [R2 is the ramp detector, not the noise detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now applied](#sum-only-and-the-correction-now-applied)
  - [Non-urgent TODO list](#non-urgent-todo-list)
- [About the last run (Run 8)](#about-the-last-run-run-8)
  - [Results](#results)
  - [What Run 9 compares against](#what-run-9-compares-against)
  - [The claims Run 9 should test](#the-claims-run-9-should-test)
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

| element type, at -O1 | `bq-expand` | worst | `alloc` | `mut-odo-vecdims` | worst |
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

**Re-probed under `-fspec-constr`, 2026-08-08, and the ordering holds
there too.** Run 8 moved the ordering at `Storable Double`, which is this
section's own trigger for re-probing, so the four types were re-run in that
regime, same six shapes, same three arms, one process per type:

| element type, at `-fspec-constr` | `bq-expand` | worst | `alloc` | `mut-odo-vecdims` | worst |
|---|---:|---:|---:|---:|---:|
| `Storable Double` | 0.148 | 0.245 | 2.61x | 0.092 | 0.123 |
| `Storable Float` | 0.156 | 0.248 | 2.11x | 0.098 | 0.140 |
| unboxed `Int` | 0.159 | 0.267 | 2.60x | 0.093 | 0.133 |
| `Storable Word8` | 0.153 | 0.247 | 1.73x | 0.093 | 0.123 |

Everything the -O1 table is read for survives. The ranking is the same at
every type, `bq-expand` spans 7% across the four where -O1 gave 3%, and its
`worst` sits between 0.245 and 0.267 — so on no shape of any type does the
shipped arm come within three times of the fallback it replaced, in either
regime. The `alloc` column's consistency check reproduces to the digit:
dividing by `8*l` whatever the element predicts `Float` 0.50x below `Double`
and `Word8` 0.875x below, and the observed gaps are 0.50x and 0.88x. So does
the width oddity — `Float` is again *worse* than `Double` for
`mut-odo-vecdims` despite half the width, which is now a two-regime
observation and still unexplained. The one thing that does not carry is the
comparison itself: these figures are the probe's, uncorrected, and belong
beside the -O1 table above rather than beside any run.

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

**At the per-element output site it wins at -O1, by 6.0%, and buys nothing
under `-fspec-constr`.**
`bq-expand-lemire-out` is `bq-expand` with the shared `i quotRem sInner`
replaced, the table build held at `baseOffsetsExpand`. At -O1 (Run 7) it is
faster than its control on 22 shapes of 24, with the published columns
agreeing with the per-shape geomean, so no part of that rests on the warm-up
ramp. Run 8 puts the same pair at 1.0015 over 24 shapes, 12 wins and sign p
1: a dead tie. The regime is the whole difference — same arms, same shapes,
same machine, one flag — so what the trick buys is however much of the
division GHC has not already dealt with, and the answer is regime-specific in
a way nothing else on this page is.
The two extremes survive the flip. `stretch-inner256` is still the arm's best
cell (0.74 of its control) and `stretch-square-1341` still its worst (1.25),
the run's worst-measured shape — read that one as the shape, not the
strategy; what the flag moved is the twenty-odd shapes between them. Two
controls back both readings. Its allocation is identical to `bq-expand`'s on
every shape, which is
what a build-identical arm must show; and it runs *before* `bq-expand` in the
group where `bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot bias
would flatter one and penalise the other and cannot produce both.

**At the per-dimension build site it loses in both regimes, by 35% and by
42%.** `bq-gen-lemire` is
`bq-gen` with the per-run, per-rank `quotRem`s replaced, and it is 1.352×
slower at -O1 and 1.421× under `-fspec-constr`, faster on no shape of the set
in either. The shape of the loss says why: it
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
does not otherwise cap array length. Weigh 6.0% against that at the -O1 a
default `cabal build` of orthotope takes, and nothing at all against it if
that build ever gains `-fspec-constr`; this
benchmark's job is to price it, not to decide it.


### Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes — chosen
to push past the ranges the rest cover, and named here without their prefix —
against the strategies nearest the decision, each as a multiple of `list` on
the same shape. These are Run 8 (SpecConstr)'s own figures, all of them net
of the forcing pass like the rest of the page:

| shape      | bq-expand | bq-expand-b | lemire-out | mut-odo | vecdims |
|------------|----------:|------------:|-----------:|--------:|--------:|
| inner1     |     0.072 |       0.066 |      0.068 |   0.275 |   0.093 |
| rank12     |     0.227 |       0.230 |      0.232 |   0.340 |   0.106 |
| wide-2xM   |     0.087 |       0.081 |      0.089 |   0.195 |   0.074 |
| coprime-r7 |     0.097 |       0.097 |      0.094 |   0.071 |   0.034 |
| pow2stride |     0.064 |       0.064 |      0.079 |   0.066 |   0.066 |
| primes     |     0.093 |       0.093 |      0.091 |   0.035 |   0.031 |
| inner256   |     0.074 |       0.075 |      0.055 |   0.019 |   0.019 |
| tall-Mx2   |     0.085 |       0.085 |      0.080 |   0.027 |   0.027 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which is
the axis the orderings turn on; the fuller per-shape record is in
[What Run 9 compares against](#what-run-9-compares-against).

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is where the expansion family does best against
  the odometer fills: `bq-expand` (0.072) and `bq-expand-b` (0.066) beat
  `mut-odo` (0.275) and `build` (0.265) three- to fourfold, which they do on
  no other shape here
  — `stretch-pow2stride` excepted, where the two families converge outright
  (0.064–0.066 across expansion and odometer alike).
  Its innermost extent is 1, so each
  base offset covers a single element: the odometer that `mut-odo`/`build`
  step has nothing to amortize over, while the expansion build has no
  per-element odometer to begin with. At the other end `stretch-tall-Mx2` has
  an innermost extent of half its length and the ordering inverts completely —
  `mut-odo` 0.027 against `bq-expand` 0.085, with every mutable strategy
  ahead of every pure one. The geomean reports that second case and averages
  the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry: that
  `stretch-inner1` is *the only shape where the pure expansion strategies beat
  every mutable one*, with the four `bq-expand` variants taking the top four
  slots. They no longer do. `bq-mut-runs-gm-mulback` takes that shape at 0.026,
  `mut-flat` and `bq-mut-runs-mulback` at 0.030, with
  `mut-odo-vecdims` at 0.093 — all ahead of every expansion variant —
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
  the worst-measured shape of the set by median and mean CI% (0.98 and 1.13,
  both the highest here, though its worst single cell is only the ninth
  worst), and where `bq-expand-lemire-out` loses hardest of the twelve shapes
  it now loses on. It stays in the column, its influence capped. That
  margin survives this caveat, being the whole shape set wide rather than
  one cell.
- **But check for a structural reason before discounting a cell as scatter,
  and check `stretch-inner1` in particular.** It is the shape whose innermost
  extent is 1, so a strategy that special-cases or elides a unit dimension
  behaves differently there *by construction*, and a striking figure is then
  the design showing through rather than noise. Two in `Main.hs` already do:
  the mul-back output hoists `s == 1` out of its loop entirely, and
  `baseOffsetsScan` elides unit dims, which on this shape leaves one real
  radix so no carry ever fires and the scan degenerates to a sequential fill.
  Both are now in the tables, and on that shape both sit far from their own
  averages: `bq-scan-packed-mulback` reads 0.129 there against a 0.108
  geomean, while `bq-mut-runs-mulback`
  reads 0.030
  against 0.078 — its best cell of all 24, as it was at -O1. Read that cell
  first and average it away last.

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
  only the positive ones the main set carries — and in both regimes, `check`
  having been re-run under `-fspec-constr` as well as at -O1.

End-to-end confirmation in horde-ad's `bench/ConvVjpBench.hs` — wiring this
branch's orthotope in and rebuilding ox-arrays + horde-ad — has been done and
is reported in that repo, not here.


### The mutable ceiling (not taken)

The `bq-*` strategies still fill the result one element at a time. The
tightest possible shape drops to a **mutable result buffer**: allocate it
once, walk the outer odometer, and write each innermost run with a tight
additive inner loop — no `quotRem`, no base-offsets table, no per-element step.
That is `mut-odo` and `mut-odo-vecdims` (0.053), the latter 1.93× over
`bq-expand` on Run 8 (SpecConstr) and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.146) does not go that far — its output is an ordinary
`vGenerate` and only its `l`-sized `Int` offset table is filled mutably, so it
needs no class method, just a mutable scratch — and Run 8 puts it 34% behind
`mut-odo` for it, on no shape of 24 ahead. On these numbers it is
no longer the cheap way to most of the gain, as it was when Failed Run 6 had
the two tied.

**Plain `mut-odo` has stopped making the case, and that is the regime's
doing.** It is the arm `-fspec-constr` sets back hardest but one — 1.19× its
own -O1 time per call, on 22 shapes of 24, with only `offtab` worse — so
Run 7's 1.51×
over `bq-expand` is gone, the pair now reading 1.08× the other way at seven
wins of 24 and an interval covering 1, which is a tie and not a defeat. The
tier's argument rests on
`mut-odo-vecdims` alone in this regime, which is a narrower base than the
ruling below was written against: two arms agreeing became one arm
carrying it.

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

**The Core says the identity holds and the gap is the measurement — in both
regimes now.** Dumped
from Run 6's source and Run 7's against one pinned dependency set,
`$wfbBuild` and `$wfbMutOdo` are the same worker in both binaries —
byte-identical once GHC's numbering is normalised, with `vBuildVS` surviving
as no top-level binding in either — and the two sources differ only by the
`Strides` newtype's zero-cost cast, which falls in both arms alike, so
neither binary is the odd one out. Nor is a dependency: `vector` and
`criterion` have been the same versions across those runs. A probe then
failed to reproduce the gap at all — in a binary relaid out by two inserted
arms the pair reads 1.004 paired (0.976..1.032, 11 shapes of 22), 1.24×
falling outside its whole per-shape range. Dumped again from Run 8's own
commit under `-fspec-constr` (2026-08-08) the two workers are still the same
worker, identical once the numbering is normalised down to the four floated
`init`/`last` error thunks each carries a private copy of, and `vBuildVS` is
still no top-level binding. So **the signature is free**, and
no `vBuild` is to be held back on either run's figure.

**What the pair has become is a second instrument, and it reads worse than
the first.** Two top-level names with identical Core are a true ratio of
exactly 1, which is what the A/A controls are built to supply — and this pair
disagrees by far more than they do, 1.24× at -O1 and 0.86× under
`-fspec-constr`, on 22 and 23 shapes of 24, where that run's six A/A twins
span 1.7%. The sign reverses with the regime, so nothing about either arm
explains it; what differs between the two names is where their code lands,
and the flag moves 12 KiB of `.text` under them all.
Read it as the A/A floor understating what code placement can do to two
*separately compiled* arms, the twins measuring only what it does to two
calls of one — and as a reason not to price any margin between distant rows
at the twins' floor. A pure-typed
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
8 (SpecConstr) prices the class-method tier at 1.93× over `bq-expand`.
Against that, the best pure strategy reaches 0.089, so the gap the class
method would buy is 1.68×, not 1.93× — which is the figure the ruling turns
on, and which -O1 put at 1.80×. Two regimes an ordering apart agree on it to
within a tenth, so the number the decision rests on is the steadiest thing on
this page.

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
[The noise floor](#the-noise-floor-is-the-aa-controls-not-the-ci) and
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

**Two rulings taken 2026-08-08 cut the timed roster from 38 strategies to 15,
and they are the roster Run 9 measures.** Both are about what is worth
spending a bench on, not about what is worth keeping: every dropped strategy
stays in `Main.hs` and stays in the roster as `concat-runs` is — checked
against the reference on every shape of every class, and not timed — so the
agreement net does not shrink and nothing has to be rewritten if a ruling is
later reopened.

- **A strategy with a precondition is not measured.** The column allowed
  `none`, an empty cell, and `shape well-formed`, which is a condition on
  being a valid view at all rather than on size; everything else is a size
  bound the caller would have to discharge. What that costs is real — it
  takes `bq-odo-mulback` (0.089), the fastest pure arm of Run 8, and the
  whole `mulback` output family with it — and the ruling is that the speed
  does not make up for the restriction: a fallback that needs `l < 2^32`
  tested and a second fill kept for when it fails is a different proposition
  from one that does not, and this suite exists to find the second kind. The
  column goes with them, having nothing left to say: after the cut every
  surviving row's cell is empty.
- **A strategy allocating 2.4x the result or more is not measured**, at
  `-fspec-constr`, which is the regime the cut was taken in and Run 9's.
  Allocation is the one column here that is deterministic per call,
  independent of what shares the process, and reproducible across rebuilds
  when time is not; it is also, across this table, no worse a predictor of
  rank than most single facts about a strategy. The threshold keeps
  `bq-expand` (2.35x) and drops the tier above it, which is the whole of the
  `new pure Vector method` group — `fused`, `all-expand`, `cm-gather`,
  `backperm`, `unfold-add` — plus `offsets-quot`, `bq-unfold` and
  `mut-offsets`.

`list` is exempt: it is the reference every ratio divides by, not a candidate,
and its 23.5x is the thing being beaten. `gen-quotrem` and `gen-unsafe`
survive both cuts at 1.00x, which the page needs — the first attempt is what
the fix is measured against.

**What the cut breaks, and has to be repaired when the roster is built.**
Several control relationships name an arm that is now untimed, and a control
whose base is not measured is not a control:

- the `bq-scan-mulback` A/A twins duplicate an arm the precondition rule
  drops, so they must be re-pointed at a surviving arm —
  `bq-scan-rem-gm-mulback` is the natural one, being the fastest pure arm
  left and carrying no precondition;
- `bq-mut-runs-gm-mulback` survives while its stated control
  `bq-mut-runs-mulback` does not, so the pair that prices dropping the size
  bound no longer exists — which is the ruling doing its work, since that
  pair's whole subject is the bound this rule now refuses;
- claim 4's controlled pair, `bq-scan-mulback` against
  `bq-expand-lemire-mulback`, loses both halves, and the Lemire output
  substitution loses its arm. Those readings stand as Run 8's and cannot be
  re-measured under this roster, which is the price of the rule and is
  recorded rather than worked around.

`--lint` and `--markdown` both need the change: the first asserts every
defined `fb` function is rostered, which the not-timed mechanism satisfies,
and the second carries `needs` and `precondition` forward from the table
above, so the column has to leave the reader and the table together.

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

The `-O2` one is a probe. `-fspec-constr` is no longer: Run 8 is a full
recorded run in that regime, and the flag therefore goes before the `--` of
every command of the sequence rather than being reached for once. A run whose
numbers are meant to be kept and written
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
floor][floor] section is the measured evidence that
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

**Quote every glob**, as those are: unquoted, the shell expands them first,
and in this directory `*/build` becomes `dist-newstyle/build` while
`*/mut-odo` finds no match and survives — so one arm silently leaves the run
and criterion reports nothing wrong. That cost a placement probe its whole
point once, the arm dropped being the only one the probe was about.

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


### The noise floor is the A/A controls, not the CI

Six A/A controls run an existing strategy twice under a second name — three
strategies, each duplicated once beside its base and once at a distance, so
position varies within a strategy and strategy within a position. They
are the only rows whose true ratio is known to be exactly 1 — or were, until
[the mutable ceiling](#the-mutable-ceiling-not-taken) turned up another by
accident:

| pair | span | published | mean per cell |
|---|---:|---:|---:|
| `bq-expand` vs adjacent twin | 1 | 1.0028 | 0.42% |
| `bq-scan-mulback` vs adjacent twin | 0 | 1.0030 | 0.46% |
| `mut-odo-vecdims` vs distant twin | 8 | 1.0036 | 1.59% |
| `mut-odo-vecdims` vs adjacent twin | 1 | 1.0037 | 2.16% |
| `bq-scan-mulback` vs distant twin | 31 | 1.0040 | 0.56% |
| `bq-expand` vs distant twin | 38 | **1.0168** | 2.56% |

No pair had a cell capped, so every published figure above equals its paired
one — the identity the winsorized estimator bought and `--selftest` asserts —
and the published column is the yardstick for comparing two rows of the
Results table, while a margin measured per shape still belongs against the
paired figures `read-run.py --aa` prints.

**On Run 8 the floor is 1.7%, and 1.7% is one cell.** Five of the six pairs
sit within 0.4% of 1. The sixth, `bq-expand` against its distant twin, owes
its whole deviation to a single shape — the twin runs 44% slower on
`vgg-14-c512-k3`, on identical allocation to the byte — and dropping that one
shape takes the pair to 1.0016 over a 0.982–1.028 per-shape range. So the
soft threshold this run supports is *under 0.5% between any two rows, with a
wild cell somewhere in the set at any time*, which is tighter than the 3.95%
Run 7's widest pair gave and than the ~3% this section carried before it.
Two runs
disagreeing twofold on the floor is itself the caution: read the floor as the
run's, re-measured every time, not as a constant of the harness.

The CI% for those six rows reads 0.05-0.12%, so the interval understates
run-to-run variability by more than an order of magnitude: it
measures sampling error *within* one benchmark, while two separately placed
benchmarks also differ in code layout, cache occupancy and inherited GC
state. The A/A is the only column that sees that, and `--aa` prints the
calibration outright — on Run 8, a median interval half-width of 0.77%
against an observed spread of 1.68% — so multiply any interval this reader
prints by about two before believing it, where Run 7 wanted three.

**Position did not reproduce.** Run 7 found the distant twin reading above
the adjacent one within every strategy and growing with span — +4.0pp, +1.7pp
and +1.3pp over 37, 31 and 7 slots — and read the group as warming up. Run 8
gives +1.4pp, +0.1pp and −0.01pp over the same spans, and the first of those
is the wild cell above rather than a trend. So the effect is either much
smaller in this regime or was never as large as three points estimated; what
survives is its sign, never negative beyond noise, and the standing advice
that `list` runs in the coldest slot so arms far down the roster are
flattered rather than penalised.

**What did turn up is a bigger placement effect, from an accident.** `build`
and `mut-odo` compile to the same worker — checked in Core at -O1 and again
under `-fspec-constr` — so they are a seventh known-true-ratio-1 pair, and
they disagree by 1.24× on Run 7 and 0.86× on Run 8, on 22 and 23 shapes of
24. The twins share one worker called from two slots; those two are separate
copies of one worker at two addresses, and the gap between what the two
instruments read is the part of layout the twins cannot see. Do not price a
margin between distant rows at the twins' floor.

**And a probe has since priced the rebuild itself, which is what neither the
twins nor that pair measure.** Four binaries built from sources differing
only in inert pad arms, the run filtered so the pads never execute, leave
`list` inside 0.5% and move `mut-odo` and `offtab` by up to 18% ([the open
list](#what-the-next-runs-have-to-decide) carries the figures). So this page
has three uncertainties of quite different size and only the smallest is on
the table above. An arm against **itself in one binary** is the A/A twins,
0.4%. Two **different arms in one binary** carry placement, which
`build`/`mut-odo` puts at 14-24% for a pair whose code is identical. One arm
across **two binaries** carries the rebuild, up to 18% on a susceptible arm
and almost nothing on an insusceptible one. Susceptibility is a property of
the arm and has been measured for three of them, so for the rest it is
unknown; what that protects is orderings and tiers, which several arms
witness at once, and what it does not protect is any single arm's figure read
across a rebuild.

**And the third of those is a bias, not a floor, which is the distinction to
keep.** A floor is a threshold below which a margin might be noise, and it
shrinks as samples accumulate; this does not. Each binary's figure is
*correct for that binary* — the pad probe's cells are geomeans over 24 shapes
with per-cell intervals of a fraction of a percent — so collecting more
samples inside one build cannot reduce it, and only averaging over several
builds would. The per-shape picture says the same: across rebuilds `list`
scatters 2.2-2.5% per shape while its geomean holds to 0.5%, where the two
susceptible arms scatter 5-10% per shape *and* move their geomeans. So do not
read 18% as a new floor for this page's tables. Every comparison inside the
Results table is two rows of one binary and is governed by the A/A twins as
before; what the 18% governs is the sentences that cross a build, which on
this page means the cross-regime absolute figures and nothing else.

**A filtered run cannot answer the position question**, and the trap is quiet
enough to be worth stating: criterion's selection removes the intervening
benches, so a pair placed 28 slots apart in the roster ends up adjacent, and
the crossed design collapses to six near-identical adjacent pairs. Measured on
a twelve-arm probe, spans of 28 and 0 both came out under 6. `--aa` says so
when the run is filtered. Position is the one question here that needs the
whole roster in the process.

The floor grew with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a
real difference. On raw slopes Run 8's six pairs read 1.0022 and 1.0141,
1.0023 and 1.0030, 1.0017 and 1.0023 — adjacent and distant per strategy —
so the largest deviation was 1.41% before the correction and is 1.68%
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
a second effect riding along with it — and Run 8's pairs move the same way,
every deviation larger net than raw.

**Failed Run 6's two conclusions here are settled.** *1/time* is refuted as
an account of the floor: per-cell *scatter* does track it -- the adjacent
pairs in the table rank by their arms' speed -- but scatter cancels, and
the bias that survives cancelling ranks by span, not by any arm's speed.
*Position* was confirmed by the crossed design built for it and is now
weakened by that same design's second run, above: what the crossing settled
for good is that the question is answerable at all, the re-aiming for Run 6
having changed strategy and position together.

Six A/A points are a modest estimate of a noise floor whichever run supplies
them. On Run 8 they are structured the other way from Run 7's: adjacent and
distant alike sit within ~0.4%, with one cell out at 44%. So the threshold to
quote is the running one, and a margin under half a percent is not a result
in any regime.

The floor above is also measured within one roster, and the roster is a
variable of its own: RTS pool state a predecessor leaves in the process
moved a horde-ad benchmark ~18% ([the full account][pos-effect] -- which
includes this suite's own floor measured isolated against in-process, on
both harness generations). Every strategy sharing one process is what
protects the tables above, ratios cancelling the shared process draw; a
comparison that crosses runs should pin the benchmark selection along
with the binary, and Run 8 is the first run here to have pinned everything
but the compiler flag.

**Each population measures its own floor.** The same six controls ride every
process, so a stride-class run prices the noise of the process its own
figures came out of — which is the only process they can be judged in — but
it prices it over two or three cells where the main set has two dozen. Read a
class's controls as this floor confirmed there or not, rather than as a
threshold of that class's own, and never carry the main set's figure into a
class comparison or the other way about. Run 8's class processes are that
ruling observed: floors from 0.8% (`slice`) up to 7.8% (`window`), and this
run puts **seven of the eight** at the `mut-odo-vecdims` slot, `reshape1`
alone excepted — one arm carrying the noise in nearly every population is a
pattern the controls were not designed to detect, and the next run's first
thing to look at.


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
rather than merely noisy. In Run 8 (SpecConstr) that is 1 cell of 1176 in the
main set — `bq-expand-zf` on `stretch-inner256` at 0.9867 — and the class
processes add one more, `build` on `bcast-tall-Mx2` at 0.9844. Run 7 had two
and six, five of its six on `bcast-inner900` where the scan family ramped
re-reading a 2000-element backing with 1.8M elements; those are gone, in the
regime that takes the same family's allocation to the table.

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
exists to remove. The ramp did not recur at Run 7's full budget, where the
same cost surfaced as scatter instead, `mut-odo` carrying that run's highest
`noise` figure by far; and the scatter did not recur under Run 8's flag,
where that arm reads an ordinary 1.00 and the noisiest benches are
`bq-mut-lemire-mulback` (4.98) and `bq-gen-lemire` (4.68). So whatever the
flag does to `mut-odo` — 19% slower per call than at -O1 — it does not do it
by making the bench noisy. **Positional or strategy-intrinsic is the
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
   **Run 8 (SpecConstr)**: 0.9999 paired, 0.21% mean per cell, worst cell
   0.57%, the halves 43 benches apart; and every class process within 0.3%.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape -- one sum over `l` elements -- and a term that were not
   could be wrong in both halves alike, leaving their agreement to notice
   nothing. It is: 0.591 to 0.607 ns per element across the whole shape set, a
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
   minus arm* is that sum in situ. Measured against `sum-only` on Run 8 they
   read
   **0.9852** and **0.9812** as medians -- within 2%, on the two arms where
   the term is the
   smallest and largest share of the bench (a quarter of `bq-expand`, a third
   of `mut-odo-vecdims`), so the test spans the range over which a bias would
   matter. Per-cell scatter is 8.0% and 4.0%, the worst cells on
   `stretch-rank12` and `stretch-inner256`. Failing
   is both medians leaving 1 on the same side by more than a few percent —
   the biased-read signature; one arm scattering while the other reads clean
   is a local disturbance for that population's write-up, not a failed gate,
   `rev`'s vecdims arm (0.9139, against `bq-expand`'s 0.9769) being Run 8's
   example.

   **This gate passed but stopped bracketing, which is new and is the next
   run's to watch.** Run 7's two medians sat either side of 1; Run 8's are
   both below it, and so is every `bq-expand` in-situ median in every one of
   the nine populations, over a 0.969–0.985 range. Both arms below 1 means
   the in-situ sum costs *less* than `sum-only`'s re-read, so the term is
   slightly over-subtracted and every ratio slightly flattered — by about
   0.5% of `bq-expand`'s own slope at a 2% error in a term that is a quarter
   of it, which is inside this run's floor. What makes it a thing to watch
   rather than a thing to fix is the consistency: nine populations on one
   side is the biased-read signature in miniature, at a size the failure test
   was not written to catch.

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
  (`mkWindow`) builds exactly those overlapping patch views, and both
  recorded runs agree: the overlap *lifts* every ratio rather than
  lowering it, so the main
  set's pessimism about this case was about absolute cost, never about the
  fallback's standing against `list`. The window block in [The stride
  classes, run by run](#the-stride-classes-run-by-run) carries the figures.
- **The roster order biases the table, and nothing corrects for it.** The
  warm-up drift above means a strategy's figure depends on its slot, `list`
  being in the coldest one. The fixes are all real changes rather than
  write-ups — a warm-up bench before `list`, interleaving or randomising the
  order, or correcting each row by its slot — and each breaks comparability
  with every run so far, which is why none is taken yet. Run 7 confirmed the
  drift and Run 8 mostly did not ([the floor section][floor]), which changes
  what is due: measure the effect again before correcting for it, since a
  correction fitted to Run 7's +0.05–0.18% a slot would be fitted to
  something Run 8 puts near zero. The placement gap the `build`/`mut-odo`
  pair shows is the larger target and no reordering addresses it.
- **No build-vs-output time decomposition**, which Run 8 wanted and did
  without. `diag` measures per-builder
  *allocation* only, so a claim like "the table build is a third of the cost"
  -- the natural reading of `bq-mut-runs` beating `bq-mut` by 39% -- cannot be
  checked here. Claim 4 no longer needs it — a Core diff identified what the
  flag deletes from the scan builder and the ~4% it is worth accounts for
  where the pair lands, the two arms sharing their output code exactly — but
  the residue does: how much of each arm's own ~25% absolute gain is build
  and how much output is still unmeasured, and the same question stands for
  every other arm in the table. It needs a timing mode alongside `diag`'s
  allocation one,
  using the fixed-iteration differencing the horde-ad performance model
  prescribes (`-n 200` minus `-n 100`, fresh processes) rather than criterion,
  since the builders are not benchmarks.

## About the last run (Run 8)

**Run 8 (SpecConstr).** Criterion, GHC 9.12.4,
**`--ghc-options=-fspec-constr`**; the first run in any regime but plain -O1,
and it changes the regime and nothing else — Run 7's shapes, Run 7's roster,
Run 7's class lists. One process per
population — the main set, then each class in `classViews`' order, back to
back on an otherwise idle machine, 3h1m28s in all — built from commit
`dc2b119` with a clean tree, on the same
desktop — Zen 3, a Ryzen 7 5800X. The main process's stderr provenance line
reads *roster 49
benchmarks over 24 shapes; elapsed 1h41m19s; peak 365 MiB in use, 137 MiB max
residency*, comfortably inside `micro.cabal`'s `-M2G`, which is why that note
stands unchanged. This run's nine JSONs are, unusually, kept for now — the
normal state of the directory is none, and Run 6's went as soon as its
write-up was drafted, which cost the ability to re-check anything needing the
raw samples when that write-up was later questioned. When they go, the commit
is what remains of them.

**The flag was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts
`baseOffsetsScan` at 2408938 bytes against `baseOffsetsMut`'s 2408530 on
`vgg-14-c512`, where plain -O1 separates the two tenfold. A run made in the
wrong regime passes every gate this page has and reads as a refutation of the
design it was built to test, so [the
procedure](#making-a-major-benchmark-run) puts that check before the run and
this line records that it was made.

**What the regime does, in absolute time**, since every column below is a
ratio and the baseline moved with everything else. Against Run 7, per call
and paired over the 24 shapes both ran: `list` itself 0.918, `bq-expand`
0.735, `bq-scan-rem-gm-mulback` 0.693, `build` 0.827, `mut-odo-vecdims`
0.904, `bq-mut-runs-mulback` 0.994, `bq-scan-packed-mulback` 1.022 and
`mut-odo` **1.192**, that last on 22 shapes of 24. So the flag speeds the
baseline by 8% and most of the table by more — which is why so many ratios
fall — while, of these eight, two arms sit still and one gets materially
worse. Every ratio in
this chapter understates its arm's absolute gain by the baseline's own 8%,
and cross-run ratio comparisons are read with that in hand — and with the
rebuild caveat [the floor section][floor] carries, since a susceptible arm
moves up to 18% between two builds of the same source, which is the size of
the smaller figures above and unmeasured for most arms. Ten of the 38
strategies besides `list` do come out slower under the flag, `offtab` (1.22)
and `mut-odo` worst of them, so "the flag helps" is a majority and not a
rule. The eight
figures above come
from the two runs' fingerprint tables, `list`'s net per call being kept there
for exactly this; the ten are each published column's own change times the
baseline's, a cheaper route that agrees with the paired figure to within
0.4% on all eight arms where both exist.

**Run 8 records every population**: the main set and the eight stride
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
and this run's re-pass of its gates), the scratch vectors are the unboxed
ones the shipped code uses, as they have been since Run 7
([the scratch vector flavour](#the-scratch-vector-flavour) says what that
severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under, and a row's distance from Run 7's is
the flag's doing and not a strategy's.

**Comparing runs?** The table below is Run 8's own; what to hold a new run
against is [What Run 9 compares against](#what-run-9-compares-against), the
claims to test are [the ones after it](#the-claims-run-9-should-test), the
population and the absolute anchor are in [Provenance](#provenance), and this
run's own floor — under 2%, and under 0.5% but for one cell — is [in the
floor section][floor].

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
| *bq-expand-nosum* | *--* | *--* | *0.13* | *80* | *2.35x* | *its base arm, forced with one element* |  |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *90* | *1.00x* | *the same, on the fastest arm* |  |
| *sum-only-early* | *--* | *--* | *0.02* | *102* | *0.00x* | *the term every row has subtracted* |  |
| *sum-only-late* | *--* | *--* | *0.01* | *102* | *0.00x* | *the same, at the other end* |  |
| **mut-odo-vecdims** | **0.053** | 0.106 | 0.04 | 80 | 1.00x | new mutating `Vector` method |  |
| *mut-odo-vecdims-aa-distant* | *0.053* | *0.105* | *0.07* | *80* | *1.00x* | *A/A control* |  |
| *mut-odo-vecdims-aa* | *0.053* | *0.105* | *0.07* | *81* | *1.00x* | *A/A control* |  |
| mut-flat | 0.074 | 0.182 | 0.14 | 84 | 1.33x | new mutating `Vector` method | `l < 2^32` |
| **bq-mut-runs-mulback** | **0.078** | 0.196 | 0.11 | 83 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-mut-runs-gm-mulback | 0.086 | 0.199 | 0.12 | 82 | 1.33x | mutable `Int` scratch | none |
| bq-odo-mulback | 0.089 | 0.179 | 0.14 | 80 | 1.50x | nothing (pure) | `l < 2^32` |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.160 | 0.08 | 76 | 1.33x | nothing (pure) | **none** |
| bq-mut-runs | 0.092 | 0.197 | 0.07 | 76 | 1.33x | mutable `Int` scratch |  |
| bq-scan-rem-mulback | 0.093 | 0.162 | 0.07 | 76 | 1.33x | nothing (pure) | `l < 2^32` |
| bq-expand32-lemire-mulback | 0.093 | 0.223 | 0.06 | 82 | 1.74x | nothing (pure) | `l < 2^32`; src < 2^31 |
| bq-scan-gm-mulback | 0.095 | 0.159 | 0.09 | 74 | 1.33x | nothing (pure) | `l < 2^32` (builder) |
| build | 0.095 | 0.273 | 0.34 | 72 | 1.00x | new mutating `Vector` method |  |
| bq-scan-mulback | 0.097 | 0.155 | 0.06 | 74 | 1.33x | nothing (pure) | `l < 2^32` |
| *bq-scan-mulback-aa-adjacent* | *0.097* | *0.159* | *0.11* | *74* | *1.33x* | *A/A control* |  |
| *bq-scan-mulback-aa-distant* | *0.097* | *0.158* | *0.05* | *74* | *1.33x* | *A/A control* |  |
| bq-expand-lemire-mulback | 0.098 | 0.226 | 0.06 | 81 | 2.35x | nothing (pure) | `l < 2^32` |
| bq-expand-b | 0.101 | 0.230 | 0.22 | 76 | 2.18x | nothing (pure) |  |
| **bq-expand** | **0.102** | 0.227 | 0.11 | 76 | 2.35x | **nothing -- SHIPPED** |  |
| bq-expand-lemire-out | 0.102 | 0.232 | 0.08 | 76 | 2.35x | nothing (pure) | `l < 2^32` |
| *bq-expand-aa-adjacent* | *0.102* | *0.227* | *0.12* | *76* | *2.35x* | *A/A control* |  |
| *bq-expand-aa-distant* | *0.103* | *0.227* | *0.08* | *76* | *2.35x* | *A/A control* |  |
| bq-expand-qr-prim | 0.104 | 0.230 | 0.17 | 75 | 2.35x | nothing (pure) | shape well-formed |
| bq-expand-zf | 0.105 | 0.249 | 0.12 | 75 | 2.35x | nothing (pure) |  |
| **bq-scan-packed-mulback** | **0.108** | 0.164 | 0.15 | 72 | 1.33x | nothing (pure) | `l`, offsets < 2^32; m <= 2^31 |
| mut-odo | 0.109 | 0.340 | 0.12 | 70 | 1.00x | new mutating `Vector` method |  |
| offtab32 | 0.128 | 0.320 | 0.60 | 68 | 1.50x | mutable `Int` scratch | src < 2^31 |
| bq-mut-lemire-out | 0.132 | 0.346 | 0.41 | 66 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-mut-lemire-mulback | 0.143 | 0.376 | 0.88 | 66 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| offtab-scan | 0.145 | 0.259 | 0.18 | 72 | 2.00x | nothing (pure) | `l < 2^32` (builder) |
| bq-mut | 0.146 | 0.338 | 0.26 | 64 | 1.33x | mutable `Int` scratch |  |
| offtab | 0.146 | 0.396 | 0.75 | 65 | 2.00x | mutable `Int` scratch |  |
| fused | 0.155 | 0.459 | 0.26 | 64 | 5.19x | new pure `Vector` method |  |
| offsets-quot | 0.202 | 0.517 | 0.20 | 58 | 5.19x | nothing (pure) |  |
| all-expand | 0.246 | 0.516 | 0.14 | 57 | 8.21x | new pure `Vector` method |  |
| bq-unfold | 0.259 | 0.813 | 0.42 | 54 | 8.27x | nothing (pure) |  |
| mut-offsets | 0.266 | 0.789 | 0.37 | 60 | 6.20x | new mutating `Vector` method |  |
| cm-gather | 0.287 | 0.553 | 0.70 | 52 | 10.73x | new pure `Vector` method |  |
| bq-gen | 0.339 | 2.123 | 0.42 | 51 | 1.33x | nothing (pure) |  |
| backperm | 0.358 | 1.141 | 0.55 | 51 | 11.89x | new pure `Vector` method |  |
| bq-gen-lemire | 0.479 | 3.503 | 0.73 | 48 | 1.33x | nothing (pure) -- refuted | `l < 2^32` |
| gen-unsafe | 0.912 | 3.743 | 0.47 | 42 | 1.00x | -- |  |
| gen-quotrem | 0.929 | 3.712 | 0.47 | 41 | 1.00x | 1st attempt |  |
| list (baseline) | 1.000 | 1.000 | 0.37 | 36 | 23.51x | -- |  |
| unfold-add | 1.004 | 1.485 | 0.50 | 34 | 27.94x | new pure `Vector` method |  |

`concat-runs` has no row: it is rostered and checked but no longer timed, for
the reason given with the strategy list above.

**Three things in the table are the run's findings rather than its numbers.**
The pure tier reordered under the flag: `bq-odo-mulback` (0.089) and
`bq-scan-rem-gm-mulback` (0.090) lead it, tying each other (0.989 paired, 10
wins of 24), where Run 7's leader `bq-scan-packed-mulback` has fallen to
0.108, with eleven pure arms now ahead of it and none at -O1. The scan
family's allocation collapsed to **1.33x** from
4.33x, exactly the tier the `diag` predicted, and `bq-expand`'s own dropped
to 2.35x from 3.11x. And the class-method tier's lead over the best pure arm
is now 1.68× (`mut-odo-vecdims` against `bq-odo-mulback`, 23 wins of
24), against 1.80× at -O1 — the figure [the
ruling](#the-mutable-ceiling-not-taken) turns on, moved by less than the
reordering underneath it would suggest.


### What Run 9 compares against

**Run 9 is decided: `-fspec-constr`, with a different roster** — the 15
strategies the two rulings under [what the benchmark
does](#what-the-benchmark-does) leave timed. So its
yardstick is the Run 8 column below, and the -O1 column beside it is kept for
a later run rather than for this one. The two together are what a third
regime, or a return to -O1, would read against. The five rows nearest the
decisions, in both regimes, so neither comparison needs the other section:

| strategy | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.053** | 0.054 |
| `mut-flat` | **0.074** | 0.063 |
| `bq-mut-runs-mulback` | **0.078** | 0.072 |
| `bq-odo-mulback` | **0.089** | 0.101 |
| `bq-scan-rem-gm-mulback` | **0.090** | 0.119 |
| `bq-expand` | **0.102** | 0.127 |
| `bq-scan-packed-mulback` | **0.108** | 0.097 |

Both columns are published geomeans over the same 24 shapes, so they may be
read against each other directly — but they are ratios to a `list` that the
flag itself moved by 8%, which is what the absolute figures at the head of
this chapter are for. Read this table for *orderings*: the leader of the pure
tier changed hands, and the two rows that rise are the two arms SpecConstr
does not help.

**Each stride class's yardstick is its own table below.** Run 7 recorded
every class first and Run 8 re-ran every one of them with the populations
pinned, so each class's paragraph carries what its regime flip moved and the
table above it is what Run 9 reads against.

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
| `cnn-slice-c32` | 3 | 288 | 5.27 µs | 0.150 | 0.155 |
| `cnn-L1-6x6-c1` | 3 | 324 | 6.48 µs | 0.203 | 0.150 |
| `stretch-rank12` | 2 | 4096 | 99.1 µs | 0.227 | 0.164 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 102 µs | 0.170 | 0.121 |
| `conv1d-24` | 3 | 5184 | 89.1 µs | 0.105 | 0.137 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 322 µs | 0.129 | 0.119 |
| `gather48-src-50` | 3 | 22500 | 385 µs | 0.099 | 0.134 |
| `stretch-rank10` | 3 | 59049 | 1.23 ms | 0.134 | 0.121 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.097 | 0.087 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.24 ms | 0.108 | 0.109 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.69 ms | 0.109 | 0.108 |
| `stretch-primes` | 89 | 250357 | 3.82 ms | 0.093 | 0.094 |
| `stretch-inner1` | 1 | 500000 | 12.2 ms | 0.072 | 0.129 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 25.5 ms | 0.062 | 0.067 |
| `vgg-14-c512-k3` | 3 | 903168 | 29 ms | 0.091 | 0.077 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 16.3 ms | 0.104 | 0.108 |
| `stretch-inner256` | 256 | 1750784 | 44 ms | 0.074 | 0.056 |
| `stretch-pow2stride` | 64 | 1769472 | 52.7 ms | 0.064 | 0.084 |
| `stretch-r5-8x432` | 8 | 1769472 | 49.9 ms | 0.054 | 0.061 |
| `stretch-square-1341` | 1341 | 1798281 | 25.5 ms | 0.125 | 0.161 |
| `stretch-bigstride` | 3 | 1800000 | 43.8 ms | 0.067 | 0.092 |
| `stretch-tab7MB` | 2 | 1800000 | 33.8 ms | 0.096 | 0.146 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 30.2 ms | 0.085 | 0.081 |
| `stretch-wide-2xM` | 2 | 1800000 | 33.7 ms | 0.087 | 0.144 |

| shape | scan-rem-gm | mut-runs-mulback | vecdims | mut-odo | build |
|---|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 0.149 | 0.121 | 0.090 | 0.208 | 0.178 |
| `cnn-L1-6x6-c1` | 0.136 | 0.168 | 0.104 | 0.231 | 0.205 |
| `stretch-rank12` | 0.135 | 0.196 | 0.106 | 0.340 | 0.273 |
| `cnn-L1-24x24-c1` | 0.103 | 0.133 | 0.075 | 0.222 | 0.193 |
| `conv1d-24` | 0.106 | 0.077 | 0.065 | 0.164 | 0.135 |
| `lenet-L1-28-c1-k5` | 0.099 | 0.099 | 0.056 | 0.135 | 0.129 |
| `gather48-src-50` | 0.105 | 0.075 | 0.064 | 0.158 | 0.137 |
| `stretch-rank10` | 0.099 | 0.100 | 0.067 | 0.180 | 0.172 |
| `stretch-coprime-r7` | 0.079 | 0.077 | 0.034 | 0.071 | 0.055 |
| `cifar-L2-16-c64-k3` | 0.088 | 0.083 | 0.059 | 0.154 | 0.147 |
| `cnn-L2-24x24-c32` | 0.088 | 0.080 | 0.060 | 0.138 | 0.119 |
| `stretch-primes` | 0.087 | 0.077 | 0.031 | 0.035 | 0.028 |
| `stretch-inner1` | 0.074 | 0.030 | 0.093 | 0.275 | 0.265 |
| `alexnet-L2-27-c48-k5` | 0.055 | 0.047 | 0.027 | 0.068 | 0.062 |
| `vgg-14-c512-k3` | 0.060 | 0.056 | 0.037 | 0.107 | 0.092 |
| `alexnet-L1-55-c3-k11` | 0.093 | 0.080 | 0.041 | 0.072 | 0.055 |
| `stretch-inner256` | 0.056 | 0.047 | 0.019 | 0.019 | 0.017 |
| `stretch-pow2stride` | 0.073 | 0.074 | 0.066 | 0.066 | 0.066 |
| `stretch-r5-8x432` | 0.051 | 0.043 | 0.021 | 0.043 | 0.034 |
| `stretch-square-1341` | 0.160 | 0.143 | 0.089 | 0.089 | 0.088 |
| `stretch-bigstride` | 0.070 | 0.050 | 0.040 | 0.107 | 0.084 |
| `stretch-tab7MB` | 0.106 | 0.071 | 0.072 | 0.189 | 0.143 |
| `stretch-tall-Mx2` | 0.075 | 0.067 | 0.027 | 0.027 | 0.021 |
| `stretch-wide-2xM` | 0.104 | 0.069 | 0.074 | 0.195 | 0.164 |

Two rows to read first. `stretch-square-1341` is one of the two shapes where
the fastest pure strategy *loses* to `bq-expand` — treat a disagreement
there as the shape; the other, `stretch-pow2stride`, is where the leading
arms of both families converge ([the per-shape section][pershape]).
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.


### The claims Run 9 should test

**Run 8's verdicts on Run 7's nine claims first**, since a run reports
breaks rather than re-deriving the table. Claims 1, 5, 6's first half and 8
held whole, and 2's first half held with its margin widened from 1.089 to
1.438; claim 7 held as an ordering of tiers while three of its levels moved,
which is the flag working. What broke: 2's second half inverted outright,
`offtab` / `bq-expand` reading **1.4402** at four wins of 24 where it had
been 0.869 — the `l`-length offset table stops paying once SpecConstr makes
the `m`-length builds allocation-free. 3 collapsed to an exact tie,
`bq-expand-lemire-out` / `bq-expand` **1.0015** at 12 of 24 and sign p 1,
where -O1 gives the Lemire output substitution a 6.0% win on 22 shapes of 24
([the Lemire section][lemire] now carries both regimes). And 9's first half
half-broke: `bq-expand-b` still ties (0.9963, 8 of 24) but `bq-expand-zf` is
now 3.6% behind on 23 shapes of 24, sign p 3e-06 — a consistent loss where it
was an inside-the-floor 1.6%.

**Claim 4 is the one Run 8 was made for, and it answers in full.** Against
`bq-expand` the scan reads 0.9548, past this run's floor — but at 15 wins of
24, sign p 0.31, and an interval covering 1. Against its own control, which
is the comparison the claim is really about, it lands exactly level:
`bq-scan-mulback` differs from `bq-expand-lemire-mulback` in the table
builder and nothing else, and reads **1.0004** at 15 of 24. So the flag did
*not* make the scan build beat the expansion build.

**Why it lands there is now measured rather than inferred**, by the Core
diff [the packed arm's entry](#what-the-next-runs-have-to-decide) describes:
the flag deletes from the scan builder exactly the boxed `Either` of a boxed
pair, and its per-step allocation, that the law at `baseOffsetsScanPacked`
names. What that is worth is about 4% of the whole arm — the pair reads
0.9946 published here against 1.034 at -O1, that second figure a division of
published cells and so good to about a percent — and it started some 3%
apart the other way, so it closes to level and stops. Nothing about the pair
is
left over: the builder's gain is identified, the arithmetic accounts for
where it lands, and the reason it does not pass the expansion build is that
the flag cheapens that build too. What it did do besides is
everything around that: the family's allocation collapsed to the predicted
1.33x, its absolute per-call time fell 31% — more than any arm ahead of it
in the table — and `bq-scan-rem-gm-mulback`, the arm with no size precondition
anywhere, went from 0.119 to 0.090 and joined the front of the pure tier. The
prediction recorded at `fbBQscanMulback` in `Main.hs` asked for three things
and got the first: 1.33x allocation, yes; the fastest pure time, no —
`bq-odo-mulback` (0.089) and `bq-scan-rem-gm-mulback` (0.090) share that
lead, with `bq-scan-mulback` itself at 0.097; ahead of the class-extension
tier, no — though it now passes two of that tier's four arms, `build` and
`mut-odo`.

**And claim 6's second half fired its own alarm, correctly.** `gen-quotrem` /
`list` reads 0.9294 where Run 7 had 1.0006, and the claim's instruction on a
break there is to check the anchor before anything else. The anchor moved:
`list` is 8% faster per call in this regime, and `gen-quotrem`'s allocation
fell from 12.01x to 1.00x, SpecConstr having fused away the per-dimension
list its arithmetic walks. So the break is the regime's, on both sides, and
not a strategy's — and at 12 wins of 24 with sign p 1 it is still a tie by
the only test immune to the baseline.

Restated on this run's own published basis, for Run 9 to check; margins are
paired geomeans, past the floor unless marked, each claim carrying the
reading it rests on. **All of them are `-fspec-constr` claims**: a Run 9 at
-O1 tests Run 7's set instead, and the two sets differ in more than their
numbers.

1. `mut-odo-vecdims` < `mut-flat` < `bq-mut-runs-mulback` < everything pure
   (0.713, 0.947, then 0.882 against `bq-odo-mulback`), each at 21 wins of
   24. The ceiling's own ordering is the one thing the regime leaves
   untouched.
2. `bq-expand` < `bq-mut` (0.695, 20 of 24) while `offtab` is now 1.440
   *behind* `bq-expand` (four of 24): the `m`-length table beats both the
   mutable scratch that builds it and the `l`-length table that replaces it.
3. `bq-expand-lemire-out` ties `bq-expand` (1.0015, 12 of 24): under this
   flag the Lemire output substitution buys nothing, where at -O1 it buys
   6.0%. A regime-conditional result, and the sharpest one here.
4. `bq-scan-mulback` ties its own build control `bq-expand-lemire-mulback`
   (1.0004, 15 of 24) while beating `bq-expand` by 4.5% (15 of 24, interval
   covering 1). Both readings are the claim; quoting only the second is how
   the tie gets reported as a win.
5. `bq-expand` < `offsets-quot` < `bq-gen` < `bq-gen-lemire` (0.502, 0.600,
   0.704): the build ordering, unbroken and every gap wider than at -O1,
   still ending in Lemire losing at the build site — by 42% now, against 35%.
   Among the builds only the mutable odometer still beats it, `bq-mut-runs`
   at 0.902 against `bq-expand` on 24 shapes of 24, the scan build having
   come level rather than ahead (claim 4). So `bq-expand` is still the
   fastest build that needs neither a class extension nor explicit
   mutation.
6. `cm-gather` < `list` (0.287, 24 of 24), and `gen-quotrem` ties `list`
   (0.929 on the geomean, 12 of 24) — the first attempt's arithmetic stops
   being dearer than the list's allocation once the flag takes its own
   allocation from 12.0x to 1.00x and leaves the list's at 23.5x, which is
   the mixed picture this suite exists to have
   refuted, arriving by a route nobody proposed.
7. Allocation, median multiples of the result on this basis: the mutable
   fills 1.00x, `gen-quotrem` also 1.00x, the whole scan family and `bq-mut`
   1.33x, `bq-odo-mulback` 1.50x, `offtab` 2.00x, `bq-expand` 2.35x, `list`
   23.5x. The tiers keep their order and three levels moved: the scan rows
   from 4.33x, `bq-expand` from 3.11x, `gen-quotrem` from 12.0x. The `diag`
   in this regime predicted the first of those exactly.
8. Every pure strategy ahead of `fused` (0.155) runs its output through the
   single in-order `vGenerate`, and the `bq-*` arms behind it lose on their
   table build, not their output — now three of them, `bq-unfold` having
   joined `bq-gen` and `bq-gen-lemire`, its stepped `unfoldrExactN` being
   exactly the build the claim names.
9. `bq-expand-b` ties `bq-expand` (0.996, 8 of 24) while `bq-expand-zf` runs
   3.6% behind it on 23 shapes of 24. `bq-expand-b`'s design still shows
   through where it should — its two best cells are `stretch-inner1` (0.920)
   and `stretch-wide-2xM` (0.930), the rank-2 views with one huge outer
   dimension where seeding from `enumFromStepN` replaces the whole
   `concatMap` build — but at a third of the margin -O1 gave it.

Each ordering is one `./read-run.py RUN.json --pair A B` line — paired
geomean,
an interval and a sign test — so a run reports which claims held
rather than re-deriving them from the table. A break in 6 would mean
something changed in
`list` or in GHC, not in a strategy — check the anchor before anything
else, as Run 8 had to.

**And for each stride class, the same three properties, now carrying Run 8's
verdicts**, the details beside each class's table:

1. **`bq-expand`'s `worst` stays under 1.** Held in every class — 0.179 at
   its highest, under `rev` — so the shipped fallback
   was never slower than the `list` it replaced, on any shape of any class the
   library can produce, in either regime now. This is the property the classes
   exist to test, no geomean can state it, and a break would have been the one
   result here to bear on `Data/Array/Internal.hs` directly.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-scan-packed-mulback` the fastest pure arm, `bq-expand` behind both.
   Its second clause is now false in **every** population, main set included:
   the packed scan leads nothing anywhere, the slot going to
   `bq-scan-rem-gm-mulback` in five classes, `bq-odo-mulback` in `revsome`
   and in the main set, and `bq-expand32-lemire-mulback` in `bcast` and
   `reshape1`. The first
   clause held in six of eight, breaking where it broke at -O1 — `reshape1`,
   whose top the flat fills own outright, and `scaled`, which now puts
   `build` ahead. The third held everywhere. Each break is read in its
   class's paragraph, and [the `sInner`
   ruling](#per-shape-where-the-geomean-hides-the-ordering) is what they bear
   on.
3. **The allocation tiers survive**: the mutable fills at the result vector,
   `bq-expand` at one to four times it, `list` at an order of magnitude more.
   Where a level moves it is the class's own `m` showing through, exactly as
   this property warned — `bq-expand` at 1.07x on `scaled` (`m` of 1 and
   2,000) and 4.22x on `reshape1` (`m = l`) — the ordering of tiers unbroken
   everywhere.

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

**Run 8 (SpecConstr) records every class**, one process per
class, in [the sequence](#making-a-major-benchmark-run); every table below
is that run's, and every paragraph reads it against Run 7's -O1 measurement of
the same population. This section
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

That header line is written out twice in this file, once here as the spec and
once as the table's own, and the two are the same text — so a session pasting
a run's rows must anchor at the line start and check that it landed on the
unindented one. Getting that wrong put Run 8's rows under this paragraph and
left Run 7's standing in the table, both checks passing, because the check
looked the table up the same wrong way the paste did.

`bq-expand` and `worst` are the shipped row's two columns in that class's
table; *fastest pure* and *ceiling* are the leading pure and mutable arms,
each with its name, since which arm leads is half of what the column says;
*floor* is the largest deviation from 1 among that process's six A/A
controls. A cell that breaks one of [the three
properties](#the-claims-run-9-should-test) is bolded, and the class's own
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
| `rev` | 3 | 0.104 | 0.179 | **`bq-scan-rem-gm-mulback`** 0.102 | `mut-odo-vecdims` 0.056 | 5.4% |
| `revsome` | 3 | 0.108 | 0.120 | **`bq-odo-mulback`** 0.103 | `mut-odo-vecdims` 0.057 | 5.3% |
| `bcast` | 3 | 0.077 | 0.100 | **`bq-expand32-lemire-mulback`** 0.070 | `mut-odo-vecdims` 0.036 | 2.9% |
| `bcastmid` | 2 | 0.115 | 0.138 | **`bq-scan-rem-gm-mulback`** 0.097 | `mut-odo-vecdims` 0.048 | 3.1% |
| `reshape1` | 2 | 0.087 | 0.094 | **`bq-expand32-lemire-mulback`** 0.036 | **`mut-flat`** 0.034 | 1.4% |
| `slice` | 2 | 0.119 | 0.140 | **`bq-scan-rem-gm-mulback`** 0.105 | `mut-odo-vecdims` 0.049 | 0.8% |
| `window` | 2 | 0.123 | 0.127 | **`bq-scan-rem-gm-mulback`** 0.104 | `mut-odo-vecdims` 0.057 | 7.8% |
| `scaled` | 2 | 0.106 | 0.108 | **`bq-scan-rem-gm-mulback`** 0.095 | **`build`** 0.032 | 3.6% |

**`rev` — every stride negated, offset at the top: the view `rev` on every
axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.03* | *137* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *145* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| **mut-odo-vecdims** | **0.056** | 0.083 | 0.76 | 137 | 1.00x |
| *mut-odo-vecdims-aa* | *0.058* | *0.091* | *0.07* | *137* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.059* | *0.088* | *0.30* | *136* | *1.00x* |
| mut-flat | 0.088 | 0.151 | 0.07 | 136 | 1.34x |
| **bq-mut-runs-mulback** | **0.095** | 0.139 | 0.04 | 135 | 1.34x |
| **bq-scan-rem-gm-mulback** | **0.102** | 0.107 | 0.02 | 130 | 1.34x |
| bq-expand-qr-prim | 0.102 | 0.183 | 0.04 | 130 | 2.52x |
| bq-odo-mulback | 0.103 | 0.120 | 0.06 | 132 | 1.41x |
| bq-expand-lemire-out | 0.104 | 0.181 | 0.02 | 131 | 2.52x |
| **bq-expand** | **0.104** | 0.179 | 0.04 | 131 | 2.52x |
| bq-expand-b | 0.104 | 0.182 | 0.02 | 131 | 2.52x |
| *bq-expand-aa-adjacent* | *0.105* | *0.179* | *0.02* | *131* | *2.52x* |
| bq-mut-runs-gm-mulback | 0.105 | 0.149 | 0.06 | 133 | 1.34x |
| *bq-expand-aa-distant* | *0.106* | *0.179* | *0.05* | *130* | *2.52x* |
| bq-expand-zf | 0.106 | 0.193 | 0.03 | 130 | 2.52x |
| bq-scan-gm-mulback | 0.106 | 0.117 | 0.04 | 129 | 1.34x |
| build | 0.107 | 0.196 | 0.04 | 124 | 1.00x |
| bq-scan-rem-mulback | 0.107 | 0.111 | 0.03 | 129 | 1.34x |
| mut-odo | 0.107 | 0.233 | 0.05 | 125 | 1.00x |
| bq-expand-lemire-mulback | 0.109 | 0.175 | 0.02 | 131 | 2.52x |
| bq-scan-mulback | 0.111 | 0.120 | 0.03 | 128 | 1.34x |
| *bq-scan-mulback-aa-adjacent* | *0.111* | *0.120* | *0.03* | *128* | *1.34x* |
| *bq-scan-mulback-aa-distant* | *0.111* | *0.120* | *0.03* | *128* | *1.34x* |
| bq-mut-runs | 0.112 | 0.161 | 0.05 | 132 | 1.34x |
| bq-expand32-lemire-mulback | 0.113 | 0.170 | 0.03 | 132 | 1.77x |
| **bq-scan-packed-mulback** | **0.120** | 0.133 | 0.04 | 126 | 1.34x |
| offtab32 | 0.130 | 0.231 | 0.34 | 123 | 1.50x |
| bq-mut-lemire-out | 0.153 | 0.256 | 0.08 | 121 | 1.34x |
| offtab | 0.157 | 0.291 | 0.07 | 120 | 2.00x |
| fused | 0.158 | 0.328 | 0.19 | 116 | 5.12x |
| bq-mut-lemire-mulback | 0.166 | 0.274 | 0.41 | 120 | 1.34x |
| offtab-scan | 0.173 | 0.177 | 0.02 | 121 | 2.00x |
| bq-mut | 0.177 | 0.277 | 0.04 | 120 | 1.34x |
| all-expand | 0.207 | 0.390 | 0.05 | 113 | 7.74x |
| offsets-quot | 0.230 | 0.381 | 0.03 | 112 | 5.12x |
| bq-unfold | 0.288 | 0.565 | 0.33 | 107 | 8.18x |
| cm-gather | 0.289 | 0.438 | 0.05 | 111 | 10.81x |
| backperm | 0.317 | 0.764 | 0.07 | 106 | 11.68x |
| mut-offsets | 0.344 | 0.531 | 0.38 | 105 | 6.13x |
| bq-gen | 0.511 | 0.671 | 0.25 | 99 | 1.34x |
| bq-gen-lemire | 0.778 | 1.070 | 0.30 | 91 | 1.34x |
| list (baseline) | 1.000 | 1.000 | 0.03 | 89 | 23.45x |
| unfold-add | 1.189 | 1.398 | 0.27 | 86 | 27.84x |
| gen-unsafe | 1.346 | 1.618 | 0.25 | 83 | 1.00x |
| gen-quotrem | 1.394 | 1.762 | 0.23 | 83 | 1.00x |


Controls: the `mut-odo-vecdims` pairs carry this process, deviating 5.4% and
4.9% (distant and adjacent, worst cells ~9.5%), so read that arm's lead from
its twins at 0.058 and 0.059; both `bq-expand` pairs and both
`bq-scan-mulback` pairs stay within 0.4%. The `sum-only` halves agree at
0.9984; the in-situ term reads 0.9139 and 0.9769 of `sum-only` as medians
(`mut-odo-vecdims` and `bq-expand` arms), the first the run's largest
departure and on the arm the A/A pairs already name.

Provenance: elapsed 0h12m39s, peak 63 MiB in use, 21 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 3.69 ms per call raw, 3.54 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.083/0.061/0.034,
`bq-mut-runs-mulback` 0.139/0.073/0.084, `bq-scan-rem-gm-mulback`
0.107/0.104/0.094, `bq-scan-packed-mulback` 0.127/0.133/0.103, `bq-expand`
0.179/0.098/0.101

What the class says: the shipped row is safe (`worst` 0.179, from 0.234) and
the fastest-pure slot inverts again, but not to the arm -O1 chose, and not
to one arm: the top of the pure tier is a cluster, `bq-scan-rem-gm-mulback`
and `bq-expand-qr-prim` tied at 0.102, `bq-odo-mulback` at 0.103 and
`bq-expand` itself at 0.104, where Run 7 gave the slot to `bq-odo-mulback`
alone. The summary table's cell is the first of those in table order, and
reads as a cluster rather than a winner. The scan family no longer sinks whole
under negated strides: `bq-scan-rem-gm-mulback` has crossed ahead of
`bq-expand` (0.102 against 0.104) where it trailed at -O1, while plain
`bq-scan-mulback` (0.111) is still behind. Run 7's one-population finding
here goes with it -- the GM quotient no longer overtakes the Lemire one in
the mutable-scratch pair (0.105 against 0.095) -- so that inversion was the
regime's and not the mechanism's. What survives both regimes is the
collapse of the first attempt: `gen-quotrem` and `gen-unsafe` run 1.35-1.39x
*slower than `list`*, worst cells at 1.76, with `unfold-add` at 1.189 and
`bq-gen-lemire`'s worst cell crossing 1. Reversal is this class's stress and
the per-dimension-arithmetic arms bear it worst whatever the flag.

**`revsome` — a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89),
`revsome-outer-g48` (`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l`
165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *91* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *117* | *0.00x* |
| *mut-odo-vecdims-aa* | *0.054* | *0.065* | *0.04* | *97* | *1.00x* |
| **mut-odo-vecdims** | **0.057** | 0.061 | 0.02 | 97 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.058* | *0.065* | *0.03* | *97* | *1.00x* |
| mut-flat | 0.087 | 0.088 | 0.07 | 89 | 1.33x |
| **bq-mut-runs-mulback** | **0.093** | 0.095 | 0.08 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.096 | 0.108 | 0.05 | 88 | 1.33x |
| bq-mut-runs | 0.099 | 0.106 | 0.05 | 87 | 1.33x |
| bq-odo-mulback | 0.103 | 0.110 | 0.03 | 86 | 1.41x |
| bq-expand32-lemire-mulback | 0.104 | 0.114 | 0.04 | 85 | 1.77x |
| **bq-scan-rem-gm-mulback** | **0.106** | 0.108 | 0.05 | 88 | 1.33x |
| bq-expand-lemire-mulback | 0.107 | 0.117 | 0.04 | 85 | 2.52x |
| bq-scan-gm-mulback | 0.108 | 0.112 | 0.03 | 87 | 1.33x |
| **bq-expand** | **0.108** | 0.120 | 0.04 | 84 | 2.52x |
| *bq-expand-aa-distant* | *0.108* | *0.120* | *0.04* | *84* | *2.52x* |
| bq-expand-b | 0.109 | 0.120 | 0.04 | 84 | 2.52x |
| *bq-expand-aa-adjacent* | *0.109* | *0.120* | *0.05* | *84* | *2.52x* |
| bq-expand-lemire-out | 0.109 | 0.121 | 0.03 | 84 | 2.52x |
| bq-scan-mulback | 0.110 | 0.114 | 0.03 | 86 | 1.33x |
| *bq-scan-mulback-aa-adjacent* | *0.110* | *0.114* | *0.03* | *86* | *1.33x* |
| *bq-scan-mulback-aa-distant* | *0.110* | *0.114* | *0.06* | *86* | *1.33x* |
| bq-scan-rem-mulback | 0.110 | 0.111 | 0.08 | 87 | 1.33x |
| bq-expand-qr-prim | 0.110 | 0.123 | 0.05 | 84 | 2.52x |
| bq-expand-zf | 0.112 | 0.127 | 0.03 | 84 | 2.52x |
| **bq-scan-packed-mulback** | **0.119** | 0.135 | 0.10 | 85 | 1.33x |
| build | 0.155 | 0.162 | 0.10 | 97 | 1.00x |
| mut-odo | 0.163 | 0.178 | 0.18 | 96 | 1.00x |
| offtab32 | 0.163 | 0.182 | 0.35 | 91 | 1.50x |
| offtab-scan | 0.168 | 0.180 | 0.07 | 80 | 2.00x |
| bq-mut-lemire-out | 0.171 | 0.193 | 0.08 | 87 | 1.33x |
| bq-mut-lemire-mulback | 0.173 | 0.197 | 0.17 | 85 | 1.33x |
| bq-mut | 0.181 | 0.194 | 0.05 | 84 | 1.33x |
| offtab | 0.200 | 0.208 | 0.11 | 89 | 2.00x |
| fused | 0.217 | 0.235 | 0.12 | 93 | 5.12x |
| offsets-quot | 0.245 | 0.297 | 0.05 | 83 | 5.12x |
| all-expand | 0.262 | 0.284 | 0.07 | 86 | 7.74x |
| cm-gather | 0.285 | 0.367 | 0.57 | 75 | 10.81x |
| backperm | 0.295 | 0.561 | 0.55 | 84 | 11.68x |
| mut-offsets | 0.346 | 0.445 | 0.28 | 94 | 6.13x |
| bq-unfold | 0.375 | 0.383 | 0.07 | 83 | 8.18x |
| bq-gen | 0.573 | 0.586 | 0.64 | 83 | 1.33x |
| bq-gen-lemire | 0.915 | 0.917 | 0.93 | 81 | 1.33x |
| list (baseline) | 1.000 | 1.000 | 0.15 | 47 | 23.45x |
| unfold-add | 1.124 | 1.190 | 0.09 | 46 | 27.84x |
| gen-unsafe | 1.327 | 1.485 | 0.46 | 45 | 1.00x |
| gen-quotrem | 1.331 | 1.501 | 0.35 | 45 | 1.00x |


Controls: the largest A/A deviation is 5.3% published on the
`mut-odo-vecdims` adjacent pair (1.0232 paired -- the gap is one capped cell,
as it was at -O1), with its distant pair at 2.3% published and 4.2% paired;
the other four sit within 0.4%. The `sum-only` halves agree at 1.0003, the
tightest of the run; the in-situ term reads 0.9738 and 0.9837 as medians
(`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h12m40s, peak 63 MiB in use, 22 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 3.46 ms per call raw, 3.31 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.037/0.061/0.059,
`bq-mut-runs-mulback` 0.094/0.075/0.095, `bq-scan-rem-gm-mulback`
0.108/0.107/0.095, `bq-scan-packed-mulback` 0.112/0.135/0.115, `bq-expand`
0.108/0.099/0.120

What the class says: mixed signs keep the top of the table in the main set's
order, and the pattern under `rev` has softened rather than repeated -- the
scan consumers no longer sink, `bq-scan-mulback` (0.110) now sitting level
with `bq-expand` (0.108) where at -O1 it was 13% behind. The pure lead is
`bq-odo-mulback` (0.103). The first attempt runs 1.33x behind `list`, worst
cells at 1.5, as it did at -O1.

**`bcast` — an innermost stride of 0, every run re-reading one element: a
broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.28* | *53* | *1.38x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.02* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *mut-odo-vecdims-aa* | *0.035* | *0.071* | *0.04* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.036** | 0.071 | 0.03 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.036* | *0.072* | *0.33* | *59* | *1.00x* |
| build | 0.047 | 0.167 | 0.30 | 62 | 1.00x |
| mut-flat | 0.056 | 0.072 | 0.08 | 50 | 1.13x |
| **bq-mut-runs-mulback** | **0.060** | 0.077 | 0.10 | 50 | 1.13x |
| bq-mut-runs-gm-mulback | 0.067 | 0.088 | 0.37 | 48 | 1.13x |
| mut-odo | 0.067 | 0.208 | 0.86 | 59 | 1.00x |
| bq-expand32-lemire-mulback | 0.070 | 0.092 | 0.11 | 47 | 1.19x |
| bq-expand-lemire-mulback | 0.072 | 0.094 | 0.33 | 47 | 1.38x |
| bq-odo-mulback | 0.074 | 0.093 | 0.33 | 48 | 1.14x |
| bq-expand-b | 0.075 | 0.100 | 0.36 | 46 | 1.38x |
| bq-mut-runs | 0.075 | 0.098 | 0.33 | 47 | 1.13x |
| fused | 0.076 | 0.236 | 0.45 | 58 | 2.52x |
| **bq-expand** | **0.077** | 0.100 | 0.35 | 46 | 1.38x |
| *bq-expand-aa-adjacent* | *0.077* | *0.100* | *0.35* | *46* | *1.38x* |
| *bq-expand-aa-distant* | *0.077* | *0.101* | *0.32* | *47* | *1.38x* |
| bq-expand-zf | 0.077 | 0.101 | 0.37 | 46 | 1.38x |
| offtab32 | 0.078 | 0.187 | 0.44 | 54 | 1.50x |
| bq-expand-lemire-out | 0.079 | 0.095 | 0.08 | 47 | 1.38x |
| bq-expand-qr-prim | 0.081 | 0.101 | 0.35 | 47 | 1.38x |
| bq-scan-gm-mulback | 0.086 | 0.112 | 0.49 | 48 | 1.13x |
| bq-mut-lemire-out | 0.088 | 0.178 | 0.32 | 52 | 1.13x |
| bq-scan-mulback | 0.089 | 0.117 | 0.34 | 47 | 1.13x |
| *bq-scan-mulback-aa-adjacent* | *0.090* | *0.117* | *0.34* | *47* | *1.13x* |
| *bq-scan-mulback-aa-distant* | *0.090* | *0.118* | *0.35* | *48* | *1.13x* |
| **bq-scan-rem-gm-mulback** | **0.091** | 0.104 | 0.36 | 48 | 1.13x |
| offtab | 0.093 | 0.236 | 0.64 | 52 | 2.00x |
| **bq-scan-packed-mulback** | **0.093** | 0.143 | 0.45 | 47 | 1.13x |
| bq-scan-rem-mulback | 0.095 | 0.109 | 0.43 | 47 | 1.13x |
| bq-mut-lemire-mulback | 0.098 | 0.178 | 0.63 | 49 | 1.13x |
| mut-offsets | 0.103 | 0.508 | 0.54 | 61 | 2.89x |
| bq-mut | 0.109 | 0.177 | 0.31 | 47 | 1.13x |
| offsets-quot | 0.139 | 0.279 | 0.06 | 47 | 2.52x |
| offtab-scan | 0.153 | 0.179 | 0.86 | 42 | 2.00x |
| bq-unfold | 0.168 | 0.416 | 0.33 | 47 | 3.65x |
| bq-gen | 0.186 | 0.292 | 0.95 | 46 | 1.13x |
| cm-gather | 0.199 | 0.386 | 0.95 | 38 | 8.45x |
| backperm | 0.211 | 0.437 | 0.74 | 29 | 7.33x |
| all-expand | 0.220 | 0.373 | 1.19 | 30 | 5.70x |
| bq-gen-lemire | 0.231 | 0.481 | 1.33 | 46 | 1.13x |
| gen-unsafe | 0.410 | 1.241 | 0.57 | 25 | 1.00x |
| gen-quotrem | 0.460 | 1.270 | 0.29 | 24 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 1.01 | 16 | 20.64x |
| unfold-add | 1.034 | 1.185 | 0.90 | 19 | 23.52x |


Controls: the largest A/A deviation is 2.9%, the `mut-odo-vecdims` adjacent
pair at 0.9705 on one 9.8% cell; the other five stay within 1.6%. The
`sum-only` halves agree at 1.0002; the in-situ term reads 0.9839 and 0.9840
as medians. One cell ramps, `build` on `bcast-tall-Mx2` at R2 0.9844 -- where
Run 7 had five, all on `bcast-inner900` and all in the scan family and
`backperm`, the arms whose allocation this regime collapses.

Provenance: elapsed 0h12m42s, peak 143 MiB in use, 49 MiB max residency; the
reader reads 49 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 49.7 ms per call raw, 48.6 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.045/0.015/0.071,
`bq-mut-runs-mulback` 0.077/0.040/0.068, `bq-scan-rem-gm-mulback`
0.097/0.046/0.104, `bq-scan-packed-mulback` 0.112/0.050/0.143, `bq-expand`
0.100/0.052/0.086

What the class says: every ratio sits far below the main set's, `list` paying
its cons-list walk on data the strategies read from cache, and the shipped
row is safe (`worst` 0.100). The fastest-pure slot goes to
`bq-expand32-lemire-mulback` (0.070), the third arm to hold it in three
populations. `build` climbs to second overall (0.047) with `mut-odo` sixth
(0.067), the pair having changed places since -O1. `bq-expand`'s allocation
tier sits at 1.38x on the class's small `m` (2,000-6,400 against `l` in the
hundreds of thousands), the `m`-tier effect the third property predicts; and
both first-attempt arms *beat* `list` (`gen-unsafe` 0.410, `gen-quotrem`
0.460), the stride-0 read being the one place their arithmetic is cheaper
than the list's allocation.

**`bcastmid` — the stretched axis in the middle instead: stride 0 on an
outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *90* | *2.10x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *108* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *113* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *113* | *0.00x* |
| *mut-odo-vecdims-aa* | *0.046* | *0.068* | *0.04* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.046* | *0.068* | *0.03* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.048** | 0.073 | 0.21 | 96 | 1.00x |
| build | 0.058 | 0.160 | 0.13 | 91 | 1.00x |
| mut-odo | 0.075 | 0.173 | 0.12 | 89 | 1.00x |
| mut-flat | 0.082 | 0.096 | 0.12 | 89 | 1.17x |
| **bq-mut-runs-mulback** | **0.088** | 0.104 | 0.04 | 88 | 1.17x |
| offtab32 | 0.096 | 0.176 | 0.18 | 86 | 1.50x |
| fused | 0.097 | 0.259 | 0.16 | 85 | 3.82x |
| **bq-scan-rem-gm-mulback** | **0.097** | 0.110 | 0.04 | 87 | 1.17x |
| bq-mut-runs-gm-mulback | 0.100 | 0.117 | 0.06 | 86 | 1.17x |
| bq-scan-gm-mulback | 0.101 | 0.119 | 0.04 | 86 | 1.17x |
| bq-scan-rem-mulback | 0.102 | 0.114 | 0.04 | 86 | 1.17x |
| bq-mut-runs | 0.105 | 0.116 | 0.14 | 86 | 1.17x |
| bq-odo-mulback | 0.105 | 0.122 | 0.04 | 86 | 1.78x |
| bq-scan-mulback | 0.105 | 0.123 | 0.05 | 86 | 1.17x |
| *bq-scan-mulback-aa-distant* | *0.106* | *0.124* | *0.02* | *86* | *1.17x* |
| *bq-scan-mulback-aa-adjacent* | *0.106* | *0.124* | *0.05* | *86* | *1.17x* |
| bq-expand32-lemire-mulback | 0.108 | 0.130 | 0.15 | 85 | 1.64x |
| bq-expand-lemire-mulback | 0.110 | 0.133 | 0.05 | 85 | 2.10x |
| **bq-scan-packed-mulback** | **0.110** | 0.131 | 0.06 | 85 | 1.17x |
| bq-expand-lemire-out | 0.111 | 0.138 | 0.04 | 84 | 2.10x |
| offtab | 0.113 | 0.210 | 0.07 | 84 | 2.00x |
| **bq-expand** | **0.115** | 0.138 | 0.06 | 84 | 2.10x |
| *bq-expand-aa-distant* | *0.116* | *0.138* | *0.03* | *84* | *2.10x* |
| *bq-expand-aa-adjacent* | *0.116* | *0.138* | *0.07* | *84* | *2.10x* |
| bq-expand-b | 0.116 | 0.138 | 0.06 | 84 | 2.10x |
| bq-expand-qr-prim | 0.117 | 0.141 | 0.06 | 84 | 2.10x |
| bq-expand-zf | 0.119 | 0.145 | 0.04 | 84 | 2.10x |
| bq-mut-lemire-out | 0.121 | 0.222 | 0.17 | 82 | 1.17x |
| mut-offsets | 0.124 | 0.457 | 0.25 | 80 | 4.39x |
| bq-mut-lemire-mulback | 0.133 | 0.225 | 0.63 | 82 | 1.17x |
| bq-mut | 0.147 | 0.218 | 0.06 | 80 | 1.17x |
| all-expand | 0.160 | 0.333 | 0.26 | 78 | 7.14x |
| offtab-scan | 0.162 | 0.182 | 0.08 | 79 | 2.00x |
| offsets-quot | 0.178 | 0.311 | 0.14 | 76 | 3.82x |
| bq-unfold | 0.217 | 0.446 | 0.22 | 74 | 5.77x |
| backperm | 0.239 | 0.637 | 0.24 | 72 | 11.40x |
| cm-gather | 0.266 | 0.439 | 0.45 | 70 | 9.65x |
| bq-gen | 0.284 | 0.750 | 0.35 | 69 | 1.17x |
| bq-gen-lemire | 0.340 | 1.020 | 1.19 | 66 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.17 | 48 | 21.99x |
| unfold-add | 1.111 | 1.260 | 0.41 | 46 | 25.60x |
| gen-unsafe | 1.208 | 1.468 | 1.32 | 44 | 1.00x |
| gen-quotrem | 1.339 | 1.720 | 0.92 | 43 | 1.00x |


Controls: both `mut-odo-vecdims` pairs read ~0.969 -- the base arm slower than
either twin, worst cells 7.1% on `bcastmid-c32-cnn` -- so this class's floor
is 3.1% and sits at that arm's slot, exactly as it did at -O1, the one
disturbance this page has now seen twice in the same class. Its in-situ term
says the same (1.0607 median against `bq-expand`'s 0.9744). The other four
pairs stay within 0.8% and the `sum-only` halves agree at 1.0001.

Provenance: elapsed 0h8m25s, peak 39 MiB in use, 13 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the bcastmid class. Anchor:
`bcastmid-primes`, `list` at 3.81 ms per call raw, 3.66 ms net.

What the class says: the main ordering holds at the top -- read
`mut-odo-vecdims`'s lead from its twins (0.046), per the controls above --
with `build` (0.058) second and `mut-odo` (0.075) third. The mover is
`fused`, from 0.256 at -O1 to 0.097, into the top eight and level with the
fastest pure arm: a `new pure Vector method` arm that the flag brings within
reach of the tier that needs no method at all.

**`reshape1` — the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *81* | *4.22x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.09* | *104* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| bq-mut-runs-gm-mulback | 0.030 | 0.030 | 0.09 | 90 | 2.00x |
| **bq-mut-runs-mulback** | **0.034** | 0.035 | 0.03 | 88 | 2.00x |
| mut-flat | 0.034 | 0.035 | 0.05 | 88 | 2.00x |
| bq-expand32-lemire-mulback | 0.036 | 0.043 | 0.06 | 87 | 2.62x |
| bq-odo-mulback | 0.041 | 0.044 | 0.09 | 86 | 2.15x |
| bq-expand-lemire-mulback | 0.042 | 0.051 | 0.06 | 86 | 4.22x |
| bq-mut-runs | 0.078 | 0.078 | 0.02 | 78 | 2.00x |
| bq-scan-rem-mulback | 0.079 | 0.080 | 0.05 | 77 | 2.00x |
| **bq-scan-rem-gm-mulback** | **0.081** | 0.082 | 0.08 | 77 | 2.00x |
| bq-expand-lemire-out | 0.082 | 0.090 | 0.08 | 76 | 4.22x |
| bq-expand-b | 0.083 | 0.094 | 0.11 | 76 | 3.72x |
| **bq-expand** | **0.087** | 0.094 | 0.12 | 76 | 4.22x |
| *bq-expand-aa-distant* | *0.087* | *0.094* | *0.11* | *76* | *4.22x* |
| *bq-expand-aa-adjacent* | *0.087* | *0.095* | *0.15* | *76* | *4.22x* |
| bq-expand-zf | 0.088 | 0.095 | 0.12 | 76 | 4.22x |
| bq-expand-qr-prim | 0.095 | 0.101 | 0.16 | 74 | 4.22x |
| bq-scan-gm-mulback | 0.095 | 0.098 | 0.07 | 74 | 2.00x |
| *bq-scan-mulback-aa-distant* | *0.095* | *0.098* | *0.33* | *74* | *2.00x* |
| bq-scan-mulback | 0.096 | 0.098 | 0.23 | 74 | 2.00x |
| *bq-scan-mulback-aa-adjacent* | *0.097* | *0.099* | *0.41* | *74* | *2.00x* |
| offtab-scan | 0.100 | 0.102 | 0.09 | 74 | 2.00x |
| *mut-odo-vecdims-aa* | *0.101* | *0.103* | *0.02* | *74* | *1.00x* |
| **mut-odo-vecdims** | **0.101** | 0.104 | 0.02 | 74 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.102* | *0.103* | *0.03* | *74* | *1.00x* |
| **bq-scan-packed-mulback** | **0.139** | 0.142 | 0.10 | 68 | 2.00x |
| bq-mut-lemire-mulback | 0.258 | 0.296 | 1.59 | 58 | 2.00x |
| build | 0.260 | 0.269 | 2.06 | 58 | 1.00x |
| bq-mut | 0.264 | 0.290 | 0.17 | 58 | 2.00x |
| bq-mut-lemire-out | 0.276 | 0.276 | 0.73 | 58 | 2.00x |
| offtab32 | 0.290 | 0.304 | 0.77 | 56 | 1.50x |
| mut-odo | 0.295 | 0.312 | 1.25 | 56 | 1.00x |
| offtab | 0.329 | 0.347 | 0.12 | 54 | 2.00x |
| fused | 0.385 | 0.385 | 0.18 | 52 | 13.18x |
| offsets-quot | 0.423 | 0.424 | 0.23 | 50 | 13.18x |
| cm-gather | 0.551 | 0.562 | 0.45 | 46 | 14.78x |
| all-expand | 0.562 | 0.570 | 0.33 | 46 | 13.78x |
| bq-unfold | 0.652 | 0.655 | 0.33 | 43 | 22.28x |
| gen-unsafe | 0.656 | 0.927 | 0.70 | 42 | 1.00x |
| gen-quotrem | 0.665 | 0.882 | 0.79 | 42 | 1.00x |
| bq-gen | 0.701 | 1.190 | 1.15 | 42 | 2.00x |
| backperm | 0.733 | 0.794 | 1.48 | 40 | 13.84x |
| mut-offsets | 0.852 | 0.864 | 0.55 | 38 | 16.20x |
| list (baseline) | 1.000 | 1.000 | 0.23 | 36 | 32.18x |
| bq-gen-lemire | 1.090 | 1.728 | 0.79 | 34 | 2.00x |
| unfold-add | 1.319 | 1.341 | 0.50 | 32 | 41.28x |


Controls: every A/A pair sits within 1.4%, the largest being
`bq-scan-mulback` distant at 0.9862; the `sum-only` halves agree at 0.9984;
the in-situ term reads 0.9815 and 0.9691 as medians. Run 7's disturbance at
this class's `mut-odo-vecdims` slot, which cost it a 3.5% floor and a 33%
in-situ scatter, is absent.

Provenance: elapsed 0h8m25s, peak 64 MiB in use, 23 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 11.3 ms per call raw, 11 ms net.

What the class says: the top still inverts completely and still by
construction -- with `sInner` 1 every run is one element, so the flat fills
win outright (`bq-mut-runs-gm-mulback` 0.030, `bq-mut-runs-mulback` and
`mut-flat` 0.034) while the odometer fills pay a full odometer step per
element (`mut-odo` 0.295, `build` 0.260) and `mut-odo-vecdims` lands
mid-table (0.101). This is [the `sInner` ruling][pershape]'s extreme case,
mechanism rather than scatter, and the regime does not touch it. What the
regime does touch is the scan builders, which hit `m = l` here: their
allocation falls from 11.00x to **2.00x** and their rows from 0.20-0.24 to
0.08-0.10, the flag's clearest single effect anywhere in this run.
`bq-expand` more than halves, to 0.087 from 0.188, posting its best class
`worst` (0.094) rather than its weakest; and `cm-gather`'s worst cell no
longer crosses 1 (0.562, from 1.019), leaving `unfold-add` and
`bq-gen-lemire` as the only arms above `list` here.

**`slice` — a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes`
(`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *90* | *2.16x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *107* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *112* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.09* | *113* | *0.00x* |
| **mut-odo-vecdims** | **0.049** | 0.069 | 0.04 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.049* | *0.069* | *0.06* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.049* | *0.069* | *0.05* | *95* | *1.00x* |
| build | 0.072 | 0.165 | 0.07 | 89 | 1.00x |
| mut-odo | 0.084 | 0.183 | 0.05 | 88 | 1.00x |
| mut-flat | 0.090 | 0.099 | 0.39 | 88 | 1.17x |
| **bq-mut-runs-mulback** | **0.095** | 0.103 | 0.52 | 88 | 1.17x |
| **bq-scan-rem-gm-mulback** | **0.105** | 0.109 | 0.04 | 86 | 1.17x |
| bq-mut-runs-gm-mulback | 0.107 | 0.113 | 0.11 | 86 | 1.17x |
| bq-mut-runs | 0.108 | 0.117 | 0.08 | 86 | 1.17x |
| offtab32 | 0.108 | 0.193 | 0.52 | 84 | 1.50x |
| bq-scan-rem-mulback | 0.109 | 0.116 | 0.06 | 86 | 1.17x |
| bq-scan-gm-mulback | 0.111 | 0.120 | 0.18 | 85 | 1.17x |
| *bq-scan-mulback-aa-distant* | *0.113* | *0.124* | *0.04* | *85* | *1.17x* |
| bq-odo-mulback | 0.113 | 0.124 | 0.10 | 85 | 1.79x |
| bq-scan-mulback | 0.113 | 0.125 | 0.06 | 85 | 1.17x |
| *bq-scan-mulback-aa-adjacent* | *0.113* | *0.125* | *0.05* | *85* | *1.17x* |
| fused | 0.114 | 0.257 | 0.29 | 84 | 3.82x |
| bq-expand32-lemire-mulback | 0.116 | 0.131 | 0.06 | 84 | 1.66x |
| bq-expand-lemire-out | 0.118 | 0.137 | 0.05 | 84 | 2.16x |
| **bq-scan-packed-mulback** | **0.118** | 0.133 | 0.08 | 84 | 1.17x |
| bq-expand-lemire-mulback | 0.118 | 0.137 | 0.09 | 84 | 2.16x |
| bq-expand-b | 0.119 | 0.140 | 0.07 | 84 | 2.16x |
| **bq-expand** | **0.119** | 0.140 | 0.05 | 84 | 2.16x |
| *bq-expand-aa-distant* | *0.119* | *0.138* | *0.03* | *84* | *2.16x* |
| *bq-expand-aa-adjacent* | *0.119* | *0.140* | *0.05* | *84* | *2.16x* |
| bq-expand-qr-prim | 0.120 | 0.143 | 0.05 | 84 | 2.16x |
| bq-expand-zf | 0.123 | 0.147 | 0.04 | 84 | 2.16x |
| offtab | 0.130 | 0.237 | 0.16 | 82 | 2.00x |
| bq-mut-lemire-out | 0.130 | 0.203 | 0.36 | 82 | 1.17x |
| mut-offsets | 0.143 | 0.457 | 0.44 | 78 | 4.39x |
| bq-mut-lemire-mulback | 0.143 | 0.223 | 0.83 | 80 | 1.17x |
| bq-mut | 0.150 | 0.217 | 0.24 | 80 | 1.17x |
| all-expand | 0.168 | 0.337 | 0.07 | 78 | 7.06x |
| offtab-scan | 0.176 | 0.183 | 0.07 | 78 | 2.00x |
| offsets-quot | 0.183 | 0.309 | 0.08 | 76 | 3.82x |
| bq-unfold | 0.223 | 0.444 | 0.10 | 74 | 5.77x |
| cm-gather | 0.260 | 0.388 | 0.63 | 71 | 9.70x |
| backperm | 0.263 | 0.660 | 0.19 | 70 | 11.27x |
| bq-gen | 0.285 | 0.727 | 0.09 | 69 | 1.17x |
| bq-gen-lemire | 0.377 | 1.158 | 0.64 | 64 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.17 | 48 | 21.99x |
| unfold-add | 1.155 | 1.305 | 0.21 | 46 | 25.60x |
| gen-quotrem | 1.356 | 1.588 | 0.90 | 43 | 1.00x |
| gen-unsafe | 1.367 | 1.566 | 0.37 | 42 | 1.00x |


Controls: the quietest process of the run, as at -O1 -- every A/A pair within
0.8%, the `sum-only` halves at 0.9980; the in-situ term reads 0.9589 and
0.9826 as medians (`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h8m26s, peak 66 MiB in use, 26 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the slice class. Anchor:
`slice-primes`, `list` at 3.67 ms per call raw, 3.52 ms net.

What the class says: a non-zero offset changes nothing, in either regime --
the main ordering reproduces whole, which is itself the result. `build`
(0.072) ahead of `mut-odo` (0.084) is the one change, and it is the main
set's change, not this class's.

**`window` — overlapping im2col patches: the workload this page opens by
naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *107* | *2.48x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *122* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.05* | *132* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *132* | *0.00x* |
| **mut-odo-vecdims** | **0.057** | 0.062 | 0.04 | 112 | 1.00x |
| *mut-odo-vecdims-aa* | *0.057* | *0.063* | *0.05* | *112* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.064* | *1.37* | *112* | *1.00x* |
| mut-flat | 0.087 | 0.088 | 0.07 | 107 | 1.27x |
| **bq-mut-runs-mulback** | **0.093** | 0.094 | 0.76 | 106 | 1.27x |
| bq-mut-runs-gm-mulback | 0.102 | 0.103 | 0.15 | 104 | 1.27x |
| **bq-scan-rem-gm-mulback** | **0.104** | 0.106 | 0.08 | 104 | 1.27x |
| bq-scan-rem-mulback | 0.108 | 0.110 | 0.06 | 104 | 1.27x |
| bq-mut-runs | 0.110 | 0.111 | 0.54 | 104 | 1.27x |
| bq-odo-mulback | 0.111 | 0.114 | 0.11 | 104 | 2.10x |
| bq-scan-gm-mulback | 0.111 | 0.111 | 0.05 | 103 | 1.27x |
| bq-scan-mulback | 0.114 | 0.115 | 0.09 | 103 | 1.27x |
| *bq-scan-mulback-aa-adjacent* | *0.115* | *0.115* | *0.06* | *103* | *1.27x* |
| *bq-scan-mulback-aa-distant* | *0.115* | *0.115* | *0.14* | *103* | *1.27x* |
| bq-expand32-lemire-mulback | 0.115 | 0.120 | 0.09 | 102 | 1.86x |
| bq-expand-lemire-mulback | 0.118 | 0.123 | 0.07 | 102 | 2.48x |
| bq-expand-lemire-out | 0.122 | 0.129 | 0.12 | 102 | 2.48x |
| **bq-expand** | **0.123** | 0.127 | 0.05 | 102 | 2.48x |
| *bq-expand-aa-distant* | *0.124* | *0.127* | *0.10* | *102* | *2.48x* |
| bq-expand-b | 0.124 | 0.127 | 0.05 | 102 | 2.48x |
| *bq-expand-aa-adjacent* | *0.124* | *0.127* | *0.08* | *102* | *2.48x* |
| bq-expand-qr-prim | 0.126 | 0.131 | 0.15 | 102 | 2.48x |
| **bq-scan-packed-mulback** | **0.128** | 0.130 | 0.08 | 102 | 1.27x |
| bq-expand-zf | 0.129 | 0.134 | 0.12 | 101 | 2.48x |
| build | 0.130 | 0.156 | 2.42 | 101 | 1.00x |
| mut-odo | 0.157 | 0.182 | 0.52 | 98 | 1.00x |
| offtab32 | 0.166 | 0.171 | 1.68 | 96 | 1.50x |
| bq-mut-lemire-out | 0.168 | 0.173 | 0.83 | 97 | 1.27x |
| offtab-scan | 0.172 | 0.176 | 0.20 | 96 | 2.00x |
| bq-mut-lemire-mulback | 0.177 | 0.180 | 1.19 | 96 | 1.27x |
| bq-mut | 0.180 | 0.183 | 0.26 | 96 | 1.27x |
| offtab | 0.194 | 0.218 | 0.47 | 94 | 2.00x |
| fused | 0.210 | 0.234 | 0.17 | 93 | 5.20x |
| offsets-quot | 0.270 | 0.282 | 0.17 | 89 | 5.20x |
| all-expand | 0.279 | 0.332 | 0.67 | 88 | 8.58x |
| cm-gather | 0.323 | 0.362 | 0.60 | 86 | 10.18x |
| mut-offsets | 0.363 | 0.402 | 0.72 | 84 | 6.08x |
| bq-unfold | 0.374 | 0.412 | 0.62 | 84 | 8.13x |
| bq-gen | 0.478 | 0.516 | 1.61 | 80 | 1.27x |
| backperm | 0.512 | 0.608 | 0.71 | 78 | 12.67x |
| bq-gen-lemire | 0.700 | 0.798 | 1.16 | 74 | 1.27x |
| list (baseline) | 1.000 | 1.000 | 0.32 | 66 | 23.46x |
| unfold-add | 1.219 | 1.243 | 0.33 | 63 | 27.87x |
| gen-unsafe | 1.276 | 1.682 | 1.37 | 62 | 1.00x |
| gen-quotrem | 1.304 | 1.629 | 1.02 | 62 | 1.00x |


Controls: the `mut-odo-vecdims` distant pair reads 1.0777 -- one 14.0% cell on
`window-28x28-k5`, on the noisiest bench of the process (CI% 1.37) -- while
every other pair sits within 0.7%, so the 7.8% floor is one cell as this
class's floor was at -O1, at a different arm's slot. The `sum-only` halves
agree at 1.0023; the in-situ term reads 0.9720 and 0.9847 as medians.

Provenance: elapsed 0h8m26s, peak 58 MiB in use, 15 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 8.54 ms per call raw, 8.27 ms net.

What the class says: the ordering holds whole, and the figure this class
exists for is the shipped row against the main set's -- 0.123 here, 0.102
there. The overlap the main set drops still *lifts* every ratio rather than
lowering it, by about the same margin as at -O1, so the main set flatters the
fallback's standing against `list` in both regimes and the pessimism this
page once recorded was about absolute cost only.

**`scaled` — superincreasing strides, none of them 1: a hand-built
dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30),
`scaled-rank1-m1` (`l` 300000, `sInner` 300000 — rank 1, so `m` is 1 and
the whole view is one strided run).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.17* | *104* | *1.07x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.36* | *126* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| build | 0.032 | 0.034 | 0.05 | 110 | 1.00x |
| *mut-odo-vecdims-aa* | *0.034* | *0.037* | *0.10* | *110* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.034* | *0.037* | *0.13* | *110* | *1.00x* |
| **mut-odo-vecdims** | **0.035** | 0.040 | 0.06 | 110 | 1.00x |
| mut-odo | 0.041 | 0.052 | 0.48 | 108 | 1.00x |
| mut-offsets | 0.047 | 0.076 | 0.40 | 106 | 1.26x |
| fused | 0.048 | 0.060 | 0.07 | 106 | 1.20x |
| offtab32 | 0.061 | 0.064 | 0.20 | 104 | 1.50x |
| offtab | 0.072 | 0.082 | 0.09 | 102 | 2.00x |
| all-expand | 0.075 | 0.095 | 0.06 | 102 | 3.70x |
| mut-flat | 0.077 | 0.078 | 0.03 | 101 | 1.02x |
| bq-mut-lemire-out | 0.077 | 0.086 | 0.22 | 101 | 1.02x |
| backperm | 0.082 | 0.138 | 0.56 | 100 | 4.97x |
| **bq-mut-runs-mulback** | **0.083** | 0.084 | 0.05 | 100 | 1.02x |
| bq-mut-lemire-mulback | 0.090 | 0.099 | 0.11 | 99 | 1.02x |
| bq-mut-runs-gm-mulback | 0.093 | 0.095 | 0.09 | 98 | 1.02x |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.098 | 0.05 | 98 | 1.02x |
| bq-scan-gm-mulback | 0.095 | 0.099 | 0.04 | 98 | 1.02x |
| bq-expand-lemire-out | 0.100 | 0.102 | 0.09 | 98 | 1.07x |
| bq-odo-mulback | 0.100 | 0.102 | 0.06 | 98 | 1.02x |
| bq-expand32-lemire-mulback | 0.101 | 0.102 | 0.04 | 98 | 1.04x |
| bq-scan-mulback | 0.102 | 0.105 | 0.07 | 97 | 1.02x |
| bq-expand-lemire-mulback | 0.102 | 0.103 | 0.06 | 97 | 1.07x |
| *bq-scan-mulback-aa-adjacent* | *0.102* | *0.105* | *0.05* | *97* | *1.02x* |
| *bq-scan-mulback-aa-distant* | *0.102* | *0.105* | *0.03* | *97* | *1.02x* |
| bq-scan-rem-mulback | 0.103 | 0.105 | 0.07 | 97 | 1.02x |
| bq-mut-runs | 0.105 | 0.106 | 0.03 | 97 | 1.02x |
| **bq-scan-packed-mulback** | **0.105** | 0.109 | 0.34 | 97 | 1.02x |
| bq-expand-b | 0.106 | 0.108 | 0.04 | 97 | 1.07x |
| **bq-expand** | **0.106** | 0.108 | 0.10 | 96 | 1.07x |
| bq-expand-qr-prim | 0.106 | 0.108 | 0.05 | 96 | 1.07x |
| *bq-expand-aa-adjacent* | *0.106* | *0.108* | *0.10* | *96* | *1.07x* |
| bq-expand-zf | 0.107 | 0.109 | 0.05 | 96 | 1.07x |
| *bq-expand-aa-distant* | *0.107* | *0.109* | *0.40* | *96* | *1.07x* |
| bq-mut | 0.111 | 0.119 | 0.07 | 96 | 1.02x |
| offsets-quot | 0.115 | 0.129 | 0.15 | 96 | 1.20x |
| bq-unfold | 0.122 | 0.144 | 0.13 | 95 | 1.36x |
| bq-gen | 0.123 | 0.148 | 0.13 | 94 | 1.02x |
| bq-gen-lemire | 0.134 | 0.171 | 0.40 | 93 | 1.02x |
| offtab-scan | 0.170 | 0.172 | 0.08 | 90 | 2.00x |
| cm-gather | 0.193 | 0.209 | 0.41 | 88 | 7.98x |
| gen-unsafe | 0.688 | 1.261 | 1.39 | 65 | 1.00x |
| gen-quotrem | 0.692 | 1.289 | 0.32 | 64 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.19 | 59 | 19.22x |
| unfold-add | 1.063 | 1.119 | 0.27 | 58 | 21.34x |


Controls: both `mut-odo-vecdims` pairs read below 1 (0.9645 adjacent, 0.9708
distant, worst cells 7.6% on `scaled-super-r3`), so the floor is 3.6% and
again at that arm; the other four pairs stay within 1.0%. The `sum-only`
halves agree at 0.9973; the in-situ term reads 0.9396 and 0.9834 as medians,
the vecdims arm's worst cell 11.4% on `scaled-rank1-m1` as at -O1.

Provenance: elapsed 0h8m25s, peak 80 MiB in use, 27 MiB max residency; the
reader reads 49 benchmarks over 2 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.27 ms per call raw, 4.09 ms net.

What the class says: this is the one population where `bq-expand` comes out
*worse* than at -O1 (0.106 from 0.097), and the one whose ceiling inverts
within itself again -- but differently: `build` (0.032) now leads outright
and `mut-odo-vecdims` (0.035) is back ahead of `mut-odo` (0.041), so Run 7's
vecdims/mut-odo inversion here was the regime's. The pure lead passes to
`bq-scan-rem-gm-mulback` (0.095) from `bq-odo-mulback`. The allocation tiers
still collapse toward 1 (`bq-expand` 1.07x, the scan rows 1.02x), the
`m`-tier effect at its floor -- `m` of 1 and 2,000 makes every table free --
which again lets the `l`-table arms shine (`mut-offsets` 0.047, `offtab32`
0.061). `gen-quotrem` beats `list` at 0.692 while its `worst` still crosses 1
(1.289), and `unfold-add` loses the only sub-1 geomean it had anywhere
(1.063, from 0.977).

### Provenance

The run's name, regime, scale and source commit are at the head of this
chapter; what follows is what they have to be read against. The commit is
recorded there because a run whose artifact is deleted and whose source is
unrecorded cannot be repeated even in principle.

Run 8 is the cleanest comparison this page has ever been able to draw and
also the one that gives most up. Everything but the compiler flag is pinned:
the same shapes, the same roster, the same class lists, the same machine, the
same GHC, the same `cabal.project.freeze`, and a tree clean at `dc2b119` —
where Run 7 against Run 6 had a roster, a shape set and the scratch
conversion all moving at once. What it gives up is the ratio column's
comparability: `-fspec-constr` moved `list` itself by 8%, so a Run 8 ratio
and a Run 7 ratio are answers to the same question in two different
denominators, and the absolute figures at the head of this chapter are what
that costs to undo. A Run 9 in either regime therefore has a like-for-like
predecessor, which is new.

The desktop named at the head of this chapter is the same machine whose
`idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and
should say which machine here.

**And the ground has not moved**, for the second run running: Run 8 measured
exactly the shapes and roster `Main.hs` holds today, in every population, so
Run 9 inherits a pinned set everywhere.

**The delta, so the population is recoverable.** What follows is the *only*
form in which a shape set or roster is recorded here: its difference from
whatever `Main.hs` holds now. A snapshot would need rewriting at every change
and would be a second copy of a list that already exists; a delta costs what
actually moved and shrinks to nothing when the two agree.

- Run 8's delta is empty: today's shapes, today's roster, today's class
  lists, winsorized per the estimator under `time`. Its regime is the only
  thing separating it from Run 7, whose delta is empty too — which is what
  makes the two columns in [What Run 9 compares
  against](#what-run-9-compares-against) a controlled pair.
- Run 6, still quoted here for the estimator ruling under `time`, for the
  `alloc` column's shape-dependence and for the correction's amplification
  arithmetic under [the floor][floor], measured today's
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

**The anchor, so a moved baseline is visible** — and this is the run where it
earned its keep. Every published figure is a
ratio to `list`, so a change in `list` itself — a new compiler, a new machine,
a changed `toListT`, or a compiler flag — rescales the whole table while
leaving every ratio intact and undetectable. These three absolute per-call
figures are the guard, and against Run 7's all three fell, by about 8%, which
is the regime and is what cleared `list` when `gen-quotrem` closed on it a
second time:

| shape | `l` | `list`, per call | net of the forcing pass |
|---|---:|---:|---:|
| `cnn-slice-c32` | 288 | 5.44 µs | 5.27 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.33 ms | 3.24 ms |
| `stretch-wide-2xM` | 1800000 | 34.8 ms | 33.7 ms |

Each stride class carries an anchor of its own, beside its table, and every
one of them moved the same way, by 4–11%: these three would not move at all
if `list` changed for one mechanism only — under
negative strides, say, or a stride-0 read — which is exactly the change a
population of ratios cannot show.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.591–0.607 ns per element across the whole set, median
0.605, so a raw slope is the published one plus about `0.60e-9 * l`, with `l`
from `Main.hs`. That recovers any uncorrected figure to within the term's own
3% spread — enough to hold a corrected run against any number
measured before the correction existed. The term itself is within 1% of Run
7's, so the flag does not touch the forcing pass, which is the control saying
the two runs' corrections are the same correction.

**What the next run replaces.** Run 8's numbers reach past the Results table,
so this is the list to walk when Run 9's land. It names *sections*, not
figures: a list of figures is a second copy of them, and enumerating it was
how the previous two versions of this list went stale — one missing six
sections, its predecessor leaking past it. What now guarantees completeness is
mechanical instead. Every section below is reached by an anchor, and the
coverage check is: no section carrying a figure outside a table may be absent
from these links. Run that check, and repeat the two sweeps it cannot replace
— grep this file for figure-shaped numerals outside the tables, and grep it
for `Run 8` — before trusting the list.

- [the head of this chapter](#about-the-last-run-run-8), which carries the run's
  name, regime, scale and source commit, and now the absolute per-call moves
  the regime is responsible for;
- [the Results table](#results), which `--markdown` emits whole, and the
  three findings under it;
- [What Run 9 compares against](#what-run-9-compares-against) — the yardstick
  geomeans in both regimes and the two-column per-shape fingerprint, all of
  which a run replaces wholesale, and which are the only per-shape record
  kept once the JSON is deleted;
- [The claims Run 9 should test](#the-claims-run-9-should-test), where a run
  reports which held rather than re-deriving them, and whose readings are
  run figures throughout;
- [the noise-floor table][floor] and its prose, from `--aa` — including the
  raw-slope six it compares against, the position verdict the crossed
  controls now disagree about between runs, and the `build`/`mut-odo` pair
  read as a second control;
- [the opening section][opening]'s headline ratios and its regime paragraph;
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
  verdict does not. Both now carry two regimes, and the Lemire one turns on
  which regime orthotope compiles under, so a run in a third would have to
  say what it does to that decision rather than only to the figure. Requote
  from the run; do not carry forward;
- [The C-gap](#the-c-gap-still-a-deeper-ceiling), whose figures are
  horde-ad's, not a run's: no run here replaces them, and they move when
  that repo re-measures — so the walk checks their currency instead;
- [The scratch vector flavour](#the-scratch-vector-flavour), whose figures
  are a probe's too, and whose conversion is why no `bq-*` figure predating
  it is comparable with one after it;
- [One element type](#one-element-type-and-what-the-probe-found), whose
  figures are a probe's and which no run replaces either. What would call for
  re-probing is a run that moves the ordering at `Storable Double`, since the
  claim is that the other types follow it — which Run 8 does, in a regime the
  probe was not run in, so the trigger is live and is [on the open
  list](#what-the-next-runs-have-to-decide) rather than discharged here;
- [sum-only](#sum-only-and-the-correction-now-applied), where what a run
  decides is no longer *whether* to correct but whether the term still passes
  its three gates, any failure invalidating the column rather than informing
  it;
- [R2 is the ramp detector][ramp], [the Lemire section][lemire], and
  [the per-shape `stretch-*` table][pershape];
- [what the benchmark does](#what-the-benchmark-does), whose two roster
  rulings quote the run they were cut on — the arms they drop and the
  allocation tier the threshold sits above — and whose membership a later
  ruling can reopen;
- [the non-urgent TODO list](#non-urgent-todo-list), whose roster-order entry
  cites the position figures a run measures and whose decomposition entry
  cites the question a run leaves open — the one part of the harness chapter
  a run touches at all;
- the `alloc` column's shape-dependence, refuted and confirmed refuted at full
  budget: every multiple quoted anywhere is a property of a strategy *and* a
  shape set, so pin the shape set before comparing across runs, as `time`
  already asks — and now a property of the regime too, three of the column's
  levels having moved with the flag alone;
- [What the next runs have to decide](#what-the-next-runs-have-to-decide),
  whose whole content is questions a run answers and figures a run moves;
- this section, which becomes the next run's own provenance;
- `read-run.py`'s docstring, whose `time`, `corr` and `net` definitions and
  A/A paragraph quote the run;
- `micro.cabal`'s `-M2G` note, if the printed heap peaks have moved;
- `Main.hs`, wherever a comment cites a figure — now `fbBQmutRunsGmMulback`'s
  margin over its control and `fbBQscanMulback`'s settled prediction, every
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

**Run 8 answered its one, and the answer is half a yes.** *Does SpecConstr
invert the scan family?* Its allocation half was already settled by a `diag`
in the run's own regime; the time half is now measured, and the family rose
without inverting anything. `bq-scan-rem-gm-mulback` went 0.119 to 0.090 and
joined the front of the pure tier, the family's absolute per-call time fell
31%, more than any arm ahead of it in the table, and its allocation landed
on the predicted 1.33x. But against its own build control the scan reads
1.0004 over
24 shapes, so the *builder* is exactly level with the expansion it was
supposed to beat, and the pure tier's lead went to `bq-odo-mulback` instead.
The flag lifted the family; it did not invert the comparison the question was
about.

The probe's three side predictions came out one right and two not. `bq-gen`
and `bq-gen-lemire` did collapse to the table in allocation, 3.58x and 2.95x
to 1.33x each — and got *slower*, 0.279 to 0.339 and 0.377 to 0.479, 11%
worse in absolute time for the first, which no reading of the `diag` had
suggested and which the Core does not account for either, `bq-gen` having
joined the placement question below. The expansion builders dropped without
vanishing as predicted, `bq-expand`'s tier going 3.11x to 2.35x. And
`bq-odo-mulback` was predicted not to follow the family up, on the ground
that its three-`Int` constructor state survives where a bare `Int` does not;
the builder's own allocation does survive, at 4.67x an entry in this regime,
but the arm rose anyway — 19% faster per call, and it now leads the pure
tier outright.

**Run 7's leftover is what Run 9 is now designed around.** *What moved
`mut-odo-vecdims` by the remaining ~13%?* Run 8 could not touch it, exactly
as its entry said — the arm is the steadiest thing in the table across the
regime flip (0.054 to 0.053, 0.904 in absolute time) and the roster was
pinned. Run 9 unpins it at the same regime, which is the two-runs-differing-
only-in-membership the question has been waiting for. Two things to hold on
to while designing it. The arm and its two twins have to survive the roster
change, or the run answers about an arm it no longer measures; and a roster
change moves membership and code layout **together**, so it still cannot
separate them — what it can do is bound the pair, because the layout half is
now measured on its own at up to 18% (the placement entry below).
A ~13% move would therefore be consistent with layout alone and would need no
roster effect at all, which is the prediction to record before the run rather
than after. What Run 8 adds is a reason to want the answer: this arm's A/A
pairs carry the largest deviation in seven of the eight class processes,
`reshape1` alone excepted.

**Three of these were answered the same day**, each by the probe its own
entry specified — the rule about a discriminating measurement deserving one
now rather than a slot in the next run, observed again:

- **`bq-scan-packed-mulback` gets worse because SpecConstr gives its control,
  for free, exactly what the packing was hand-rolled to buy — and the packing
  keeps charging for it.** Dumped in both regimes from Run 8's commit
  (2026-08-08, `-dsuppress-all -dsuppress-uniques`), the two arms' table
  builds differ like this. At -O1 the control's loop carries its state as a
  boxed `Either` of a boxed pair of a boxed `Int`, allocating a `Right` per
  step — the 72-bytes-an-entry the law at `baseOffsetsScanPacked` records —
  while the packed arm unwraps one `I#` and is otherwise unboxed, which is
  the 21% lead it held there. Under `-fspec-constr` both loops specialise to
  four raw arguments and *neither* boxes: the control's `Either`, pair, `I#`
  and its per-step allocation all vanish, and the packed arm loses only its
  one `I#` unwrap. What survives on one side and not the other is the
  packing's own arithmetic — `uncheckedIShiftRA# … 32#` and `andI# …
  4294967295#` on every element, against the control's two plain `+#` — so
  the flag pays off the debt the packing existed to avoid and leaves the
  packing's interest still due. Hence cheaper (1.33x on both) and slower
  (1.11× on 24 shapes of 24).

  Two consequences. The law at `baseOffsetsScanPacked` is confirmed in its
  constructive half and its corollary refuted: every state shape does unbox
  under the flag, but "indistinguishable from its control" does not follow,
  because unboxing removes the control's cost and not the packed arm's. The
  `diag` behind all of this was re-measured in Run 8's own regime and every
  figure quoted above reproduces, including the controls that say the
  instrument did not move; what it adds is that `baseOffsetsScanPacked` goes
  3.00x to 1.00x, so under the flag even the boxed `Int` in
  `unfoldrExactN`'s emit pair — which the -O1 reading called out of reach of
  any state shape — is gone. And
  the packed representation is now known to be a **-O1-only** optimisation:
  wherever SpecConstr runs it is strictly dominated by the plainer arm it was
  built to beat, which is a thing to have settled before the flag question
  below is answered rather than after.

- **It does not generalise to the other hand-packed arms, and why not is the
  useful half.** Three benchmarked pairs differ from their control in a
  hand-managed compact representation and in nothing else, and the flag moves
  all three differently. The -O1 column is a ratio of published columns, that
  run's artifact being gone; Run 8's is paired, and the last two columns are
  each arm's own absolute per-call move:

  | arm / its control | hand-packed how | -O1 | Run 8 | arm | control |
  |---|---|---:|---:|---:|---:|
  | `bq-scan-packed-mulback` / `bq-scan-mulback` | loop state, two fields in one `Int` | 0.789 | **1.113** | 1.022 | 0.724 |
  | `bq-expand32-lemire-mulback` / `bq-expand-lemire-mulback` | the `m`-length table at `Int32` | 0.983 | **0.949** | 0.729 | 0.756 |
  | `offtab32` / `offtab` | the `l`-length table at `Int32` | 1.136 | **0.877** | 0.940 | 1.218 |

  **Hand-packing survives the flag exactly when what it buys is something the
  specialiser cannot buy.** The packed state buys unboxed loop state, which
  is SpecConstr's own job, so the flag hands the control the same thing for
  nothing and leaves the packing holding its shift and mask. The two `Int32`
  tables buy heap footprint, which SpecConstr has no opinion about, and the
  Core says so: their distinguishing operations — two `intToInt32#`, a
  `writeInt32Array#`, no boxing — are identical in the two regimes, as are
  their controls', so the `expand32` pair barely moves. The `offtab32` pair
  moves furthest of the three and not for its packing at all: its arm
  improves 6% while its *control* regresses 22%.

- **The element-type ordering still follows `Storable Double`.** [That
  section's](#one-element-type-and-what-the-probe-found) own re-probe trigger
  is a run that moves the ordering at `Storable Double`, which Run 8 does, so
  all four types were re-run under the flag: the ranking is unchanged at every
  one of them, `bq-expand`'s `worst` stays between 0.245 and 0.267, and the
  column's arithmetic check reproduces to the digit. The figures are in that
  section beside the -O1 ones. What the re-probe does not settle is the
  question behind the trigger — whether the flag's reordering is an
  `Int`-arithmetic effect or an element-width one — since the ordering it
  moved is among the roster's arms and not among the types.

**What Run 8 leaves open**, each with what would settle it:

- **Should orthotope itself compile with `-fspec-constr`?** The flag is worth
  27% per call to `bq-expand` — the shipped fallback — on this replica, and
  8% to `list` beside it, so the question is no longer academic. What it is
  *not* is evidence about
  orthotope: this suite is a replica, its regime-3 fallback is one function
  among fifty in one module, and a library-wide flag is a library-wide
  decision with compile-time and code-size costs nothing here measures. The
  discriminating measurement is one level up and cheap — build this
  repository itself with and without the flag and run horde-ad's
  `convVjpBench` A/B over
  the pair, which is the same harness that priced the fallback fix — and it
  belongs in that repo's issue, not in a run here.
- **What does code placement cost?** **A rebuild is worth up to 18% on a
  susceptible arm and 0.5% on the baseline** — which is the size of every
  unexplained regression in Run 8, and the largest effect this page has
  measured that is not a strategy. Four binaries were built from sources
  differing only in inert pad arms, the run filtered so the pads never
  execute; against the first of them the other three read `list` 0.9949,
  1.0019 and 1.0031, `mut-odo` 1.0389, 0.8808 and 1.0401, and `offtab`
  0.8241, 0.9524 and 0.9126 (2026-08-08, `-fspec-constr`, 24 shapes,
  per-shape geomeans of absolute net time). So susceptibility is a property
  of the arm: the baseline has almost none and two arms have a great deal,
  and they are the same two the flag sets back hardest.

  Around that sit the readings it explains. `offtab`'s own regression is
  **not** roster or noise: filtered into a five-bench process it reads 1.2236
  across the regimes over 24 shapes, slower on 24 of 24, against the full
  run's 1.218 — but that used one binary for both regimes, so it rules out
  everything except placement. `build` and `mut-odo` compile to the same
  worker and moved in *opposite* directions under the flag, 17% faster and
  19% slower, which identical code cannot do. `bq-gen` regressed 12% with its
  build loop specialised like every other and its build allocation-free. And
  the flag moves 12 KiB of `.text` (20,349,125 bytes to 20,336,837), so every
  arm's address and alignment shift whether its code changed or not.

  What is left is narrower than the question was. The pad probe should have
  timed `build` across the four layouts and did not — a shell glob ate the
  arm ([the reader's section](#the-reader-read-runpy)) — so the pair's own
  swing is still unmeasured, and no probe has yet varied a *susceptible*
  arm's address deliberately rather than incidentally. Both want a quiet
  machine. What no longer needs asking is whether placement can be this
  large: it is.
- **Is the term still unbiased?** Gate 3 passed but stopped bracketing 1:
  every `bq-expand` in-situ median in every one of the nine populations sits
  below it, 0.969 to 0.985
  ([sum-only](#sum-only-and-the-correction-now-applied)).
  One run is not a trend and the size is inside the floor, so the measurement
  is simply the next run's own gate, read for the sign rather than only for
  the threshold; if it is one-sided again, the `-nosum` arms are pricing
  something `sum-only` does not.
Run 9's regime and roster are decided — `-fspec-constr`, membership changed —
so its yardstick is Run 8's column and its delta is the first non-empty one
this page has recorded since Run 6. What that buys is the membership
experiment; what it gives up is the exact repetition the same regime with the
same roster would have been, and with it the only clean measurement of
run-to-run drift this page could have taken. That measurement is now owed by
some later run.

[floor]: #the-noise-floor-is-the-aa-controls-not-the-ci
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[opening]: #regime-3-micro-benchmark-the-fix-bq-expand
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
