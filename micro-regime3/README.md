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
with its dimension lists replaced by unboxed vectors — is on Run 9
(SpecConstr) **2.18×** over `bq-expand` and the fastest strategy measured
here. Both need a new `Vector`-class method, which was
measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal — a bar an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-not-taken), amended). Plain `mut-odo` no longer
argues for it at all: it and the shipped arm are a tie, winning eight shapes
of 24 with sign p 0.15 and an interval covering 1, where Run 7 (Harness), at
-O1, had it 1.51× ahead.

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure ones on Run 9 are
**`bq-scan-rem-gm-mulback`** and **`bq-odo-gm-mulback`**, tied at 0.090
against `bq-expand`'s 0.105 and carrying **no size precondition at all** —
which is the point of them, a ruling since having stopped this suite timing
any arm that needs one ([what the benchmark
does](#what-the-benchmark-does)). Neither is what
`Data/Array/Internal.hs` does today. Of the trade-offs, allocation and a
noise floor this run measures at 0.07% between five of its six control
pairs are in [Results](#results), each
arm's precondition is at its entry in `Main.hs`'s roster, and the division
sites are in
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

And **one regime's**, and now **one roster's** as well. Runs 8 and 9 both
compiled the suite with `-fspec-constr`, where every run before them took the
plain -O1 a default `cabal build` of orthotope takes, and the flag reorders
the table rather than nudging it — it speeds `list` itself by 8%, `bq-expand`
by 27% and the plain scan family by 31%, and *slows* `mut-odo` by 19%. Run 9
then changed the roster and nothing else, and moved arms from 9% faster to
19% slower with the baseline standing still ([the head of the run
chapter](#about-the-last-run-run-9)). So a figure here belongs to a flag
*and* to a membership, and the second turns out to be worth as much as the
first. **Whether orthotope should carry the flag is not this
page's question** and is deliberately not on its open list: this is a replica
of one function, where that decision is a library-wide one about compile time
and code size, and the measurement that would settle it is horde-ad's
`convVjpBench` over a real build. The 27% is what this page contributes to
it.

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
Those shapes are excluded from runs, not unmeasurable: after Run 9 they were
promoted into the shape set behind a temporary edit, to settle what the
allocation area should be for a caller whose arrays are this size ([the floor
section][floor]). `Cin` and the spatial dims scale `l` linearly too (in the
full run, doubling
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
the same shape. These are Run 9 (SpecConstr)'s own figures, all of them net
of the forcing pass like the rest of the page. A `lemire-out` column stood
between `bq-expand-b` and `mut-odo` until the precondition ruling took
`bq-expand-lemire-out` out of the timed roster, a column a later run could
only have left standing under its own name. What that arm's per-shape
behaviour showed is in
[the Lemire section][lemire], which is where its decision lives anyway:

| shape      | bq-expand | bq-expand-b | mut-odo | vecdims |
|------------|----------:|------------:|--------:|--------:|
| inner1     |     0.086 |       0.071 |   0.287 |   0.098 |
| rank12     |     0.238 |       0.231 |   0.324 |   0.101 |
| wide-2xM   |     0.093 |       0.082 |   0.171 |   0.066 |
| coprime-r7 |     0.102 |       0.101 |   0.055 |   0.030 |
| pow2stride |     0.066 |       0.066 |   0.067 |   0.067 |
| primes     |     0.093 |       0.093 |   0.028 |   0.026 |
| inner256   |     0.072 |       0.071 |   0.017 |   0.016 |
| tall-Mx2   |     0.085 |       0.085 |   0.021 |   0.020 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which is
the axis the orderings turn on; the fuller per-shape record is in
[What Run 10 compares against](#what-run-10-compares-against).

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is where the expansion family does best against
  the odometer fills: `bq-expand` (0.086) and `bq-expand-b` (0.071) beat
  `mut-odo` (0.287) and `build` (0.316) three- to fourfold, which they do on
  no other shape here
  — `stretch-pow2stride` excepted, where the two families converge outright
  (0.066–0.067 across expansion and odometer alike).
  Its innermost extent is 1, so each
  base offset covers a single element: the odometer that `mut-odo`/`build`
  step has nothing to amortize over, while the expansion build has no
  per-element odometer to begin with. At the other end `stretch-tall-Mx2` has
  an innermost extent of half its length and the ordering inverts completely —
  `mut-odo` 0.021 against `bq-expand` 0.085, with every mutable strategy
  ahead of every pure one. The geomean reports that second case and averages
  the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry: that
  `stretch-inner1` is *the only shape where the pure expansion strategies beat
  every mutable one*, with the four `bq-expand` variants taking the top four
  slots. They no longer do, and Run 9's roster says so more plainly than
  Run 6's: `mut-flat-gm` takes that shape at 0.027 and
  `bq-mut-runs-gm-mulback` at 0.031, both ahead of every expansion variant,
  while `mut-odo-vecdims` sits at 0.098 —
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
  the worst-measured shape of the set by median and mean CI% (1.018 and
  1.058 on Run 9, both the highest here, though its worst single cell ranks
  only thirteenth of 24). It stays in the column, its influence capped.
  Run 8 added that it is also where `bq-expand-lemire-out` lost hardest of
  the twelve shapes it lost on; that arm is untimed since the precondition
  ruling, so the observation is Run 8's and no later run re-establishes it.
- **But check for a structural reason before discounting a cell as scatter,
  and check `stretch-inner1` in particular.** It is the shape whose innermost
  extent is 1, so a strategy that special-cases or elides a unit dimension
  behaves differently there *by construction*, and a striking figure is then
  the design showing through rather than noise. Two in `Main.hs` already do:
  the mul-back output hoists `s == 1` out of its loop entirely, and
  `baseOffsetsScan` elides unit dims, which on this shape leaves one real
  radix so no carry ever fires and the scan degenerates to a sequential fill.
  On that shape both sit far from their own
  averages: `bq-scan-packed-mulback` reads 0.129 there against a 0.108
  geomean, while `bq-mut-runs-mulback`
  reads 0.030
  against 0.078 — its best cell of all 24, as it was at -O1. Those four
  figures are quoted rather than looked up because both arms have since left
  the timed roster and their per-shape columns left the fingerprint with
  them; the reading is Run 8's and is what a later run would have to
  re-establish before using it. Read such a cell
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
That is `mut-odo` and `mut-odo-vecdims` (0.048), the latter 2.18× over
`bq-expand` on Run 9 (SpecConstr) and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.115) does not go that far — its output is an ordinary
`vGenerate` and only its `l`-sized `Int` offset table is filled mutably, so it
needs no class method, just a mutable scratch — and Run 9 puts it 16% behind
`mut-odo` for it, at eight wins of 24. On these numbers it is
no longer the cheap way to most of the gain, as it was when Failed Run 6 had
the two tied, and the gap it must close to become one again is 2.4× against
`mut-odo-vecdims` (0.4172 paired, 24 shapes of 24).

**Plain `mut-odo` has stopped making the case, and it is not the regime's
doing.** Run 8 read the pair 1.08× *against* `mut-odo` and blamed the flag,
which sets that arm back hardest but one; Run 9, same flag, has the geomean
back on `mut-odo`'s side at 0.947 — and it is still not a win, at eight
shapes of 24 with sign p 0.15 and an interval covering 1. The two halves
point opposite ways because the pair's per-shape range is enormous, 0.233 on
`stretch-inner256` to 3.342 on `stretch-inner1`, so a handful of large shapes
carry the geomean while most shapes go the other way; read the sign test, and
the answer is a tie in both runs. What removed `mut-odo` from the argument
was therefore not `-fspec-constr` alone: the arm moved 9% *faster* between
Run 8 and Run 9 on a roster change, `bq-expand` moved 3% slower, and the tie
survived both. The tier's argument rests on
`mut-odo-vecdims` alone in both regimes, which is a narrower base than the
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
9 (SpecConstr) prices the class-method tier at 2.18× over `bq-expand`.
Against that, the best pure strategy reaches 0.090, so the gap the class
method would buy is **1.87×**, not 2.18× — which is the figure the ruling
turns on. It has now read 1.80× at -O1, 1.68× on Run 8 and 1.87× here, so it
is *not* the steadiest thing on this page, as the previous two runs had it:
the spread is a tenth either side of 1.8, and Run 9's move came from a roster
change that touched neither arm's code. Read it as *approaching 2× and
volatile at the tenth*, and do not reopen or close the ruling on a movement
of that size — it is the same span the layout question prices.

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

**And now weighed in code, 2026-08-08: the four FastReshape arms.** They
port the precedent's loop arithmetic onto `mut-odo-vecdims` one axis at a
time, a 2×2 plus one over that shared control: `mut-odo-vecdims-add-in`,
the input offset stepped additively in place of the loop's one multiply;
`mut-odo-vecdims-add-out`, the output position through a precomputed
stride table in place of the threaded return — the axis that can lose;
`mut-odo-vecdims-add-both`, the corner, doubling as the endpoint contrast
that still reads if the solo margins sit inside the floor; and
`mut-odo-vecdims-add-both-down`, both loops in the count-down-to-zero
form, over the corner as its control. Any close pair among them is
to be read workers-first, per the `build` lesson above.

**Run 9 priced them, and the pre-run reading was right about the sign and
wrong about the size.** That reading — one shape, Run 8's regime — put all
four behind their control by +4% to +12%, the corner sub-additive and the
count-down form recovering two thirds of its loss. Over 24 shapes:
`add-in` **1.1552** (0 wins of 24), `add-out` **1.1795** (1 of 24),
`add-both` **1.1645** (1 of 24), each against `mut-odo-vecdims` and each with
sign p at or below 3e-06. So the precedent's loop arithmetic **loses on both
axes**, by more than the one-shape probe suggested, and near-unanimously
across shapes — the 2×2 therefore prices how much of the loss each axis owns,
as the pre-run reading warned it might, and not which axis wins. The corner
is sharply sub-additive, 16.5% where the two solo losses sum to 33.5%, so the
two axes are largely paying for the same thing. The count-down form is the
one that pays: `add-both-down` reads **0.8745** against the corner on 23
shapes of 24, recovering nearly the whole loss rather than two thirds, and it
ties the shared control outright (1.0183, 13 of 24, sign p 0.84). Allocation
was not in doubt and is not — all four read 1.00x, the stride table costing
about 1.3 KB against a megabyte-scale result.

**Why the count-down form pays is now in the Core, and why the other three
lose is not what this section took it to be** (2026-08-09, `-fspec-constr`).
`add-both-down`'s innermost run-fill is seven instructions where every
sibling's is eight: it carries the output position in a register and steps
it, where the others rebuild `outPos + j` with a move and an add on every
element. That is a per-element change, and Run 9 agrees it behaves like one
— its advantage grows with `sInner`, r −0.29 against log `sInner`, 1.052
where `sInner` is 3 or less against 0.972 where it is 8 or more. The other
three do not. `add-in`'s counted loops are identical to its control's
instruction for instruction, its whole code difference sitting in the
odometer recursion, where one multiply becomes an accumulated add threaded
as a further argument — a per-*run* change. And a per-run change is not what
the run measured: the penalty is flat in `sInner` (r +0.21), and its largest
cell is `stretch-tall-Mx2`, shape [2, 900000], where the odometer descends
twice per call and `add-in` still reads 1.3152. Two multiplies do not cost
31%. `add-out` and `add-both` do carry real extra code — a `scanr (*)` over
the shape, built into a byte array once per call and read once per run — but
it adds nothing to the per-element loop, and the same shape disposes of it:
at rank 2 and two runs their entire extra work is a two-element table and
two reads, and they read 1.2930 and 1.2901 there.

**So the two solo axis figures are suspended, not replaced.** What costs 16%
on them is not the arithmetic they port, the loop doing the per-element work
being the same code in all four arms; and it is the size the layout span is,
on arms whose executed copy of that loop straddles a cache line where their
control's does not ([the floor section][floor]). The ruling below keeps its
conclusion, since the axis that is genuinely per-element is the count-down
one and it ties. What it loses is the price: +15.5% and +18.0% are not what
FastReshape's arithmetic costs, and the honest reading of these four is that
the precedent's arithmetic is neutral here rather than harmful.

**What that does to the precedent's weight.** FastReshape's arithmetic, ported
one axis at a time onto this page's fastest arm, buys nothing here: the
count-down form ties the control, and the two solo axes' losses are not the
arithmetic's to pay (above). So the in-tree precedent argues for the *shape*
of a mutable fill and
not for its arithmetic, and the ruling above is unmoved: what a new class
method would buy is still `mut-odo-vecdims`, at [the 1.87×](#results) the
ceiling section prices, and none of these four adds to it.


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
  `bq-scan-rem-mulback`, `bq-scan-gm-mulback`, `bq-scan-rem-gm-mulback`,
  `bq-odo-mulback`, `bq-scan-packed-mulback`, and the two added when the
  precondition ruling left their builds with no unconditional output form,
  `bq-expand-gm-mulback` and `bq-odo-gm-mulback`. Three of those carry no
  size precondition anywhere: the two new ones and `bq-scan-rem-gm-mulback`,
  whose builder drops the bound as well as its output.
- **Whole-offset and alternative gathers**, which build an `l`-length offset
  vector rather than an `m`-length one: `backperm`, `cm-gather`, `all-expand`,
  `offtab`, `offtab32`, `offtab-scan` and `offtab-scan-rem`, the last being
  the unconditional twin of the one before it — its bound is the builder's,
  which no output substitution reaches.
- **Direct mutable result-buffer fills**, which need a class extension or
  explicit mutation and are the [ceiling](#the-mutable-ceiling-not-taken):
  `mut-odo`, `mut-odo-vecdims`, `mut-offsets`, `build`, `mut-flat` and
  `mut-flat-gm`, the unconditional twin of the last. And
  `concat-runs`, class-methods-only and the first arm to be checked without
  being timed (below).

The order they are *run* in is deliberately a different one, fixed by `roster`
in `Main.hs`, where a majority of them now take no slot at all, being checked
and not timed; the Results table below is sorted by time, a third. Sharing that
roster with the strategies, and not strategies themselves, are ten controls:
six A/A arms — `bq-expand-aa-adjacent` and `bq-expand-aa-distant`,
`bq-scan-rem-gm-mulback-aa-adjacent` and
`bq-scan-rem-gm-mulback-aa-distant`,
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

`concat-runs` was the first strategy `check` covers and the benchmark does
not, and is the only one excluded on its own noise rather than by a ruling
below. It was by a clear margin the noisiest bench of the set — Failed Run 6's
single worst cell, and a median cell some 2.5× the shape's typical CI — so
excluding it costs no information the run needs, and it is one of the changes
preceding the current, quieter run, though nothing separates its contribution
from the others'.

**Two rulings taken 2026-08-08 cut the timed roster from 38 strategies to 15,
and the arms written since bring Run 9's back to 23** — the four unconditional
forms the precondition ruling itself called for (below) and the four
FastReshape arms ([the mutable
ceiling](#the-mutable-ceiling-not-taken)). Both rulings are about what is worth
spending a bench on, not about what is worth keeping: every dropped strategy
stays in `Main.hs` and stays in the roster as `concat-runs` is — checked
against the reference on every shape of every class, and not timed — so the
agreement net does not shrink and nothing has to be rewritten if a ruling is
later reopened. The 23 arms the rulings dropped carry `Only` in that roster,
each naming the bound or the multiple that disqualified it; with the controls
the run is 34 benches.

- **A strategy with a precondition is not measured.** The column allowed
  `none`, an empty cell, and `shape well-formed`, which is a condition on
  being a valid view at all rather than on size; everything else is a size
  bound the caller would have to discharge. What that costs is real — it
  takes `bq-odo-mulback` (0.089), the fastest pure arm of Run 8, and the
  whole `mulback` output family with it — and the ruling is that the speed
  does not make up for the restriction: a fallback that needs `l < 2^32`
  tested and a second fill kept for when it fails is a different proposition
  from one that does not, and this suite exists to find the second kind.
  **Run 9 says the cost was near zero**, which the ruling did not need but is
  worth recording: its unconditional counterpart `bq-odo-gm-mulback` came in
  at 0.090, within a thousandth of the arm it replaces, and ties
  `bq-scan-rem-gm-mulback` at the head of the pure tier. Dropping the bound
  bought back the restriction and cost about a point. The
  column went with them, having nothing left to say once every surviving
  row's cell was empty; each dropped arm's bound is now at its roster entry,
  spelled as that arm's own assert spells it.
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

- the `bq-scan-mulback` A/A twins duplicated an arm the precondition rule
  drops, and **have been re-pointed** at `bq-scan-rem-gm-mulback`, the
  fastest pure arm left and the one carrying no precondition: the pair is now
  `bq-scan-rem-gm-mulback-aa-adjacent`, moved to sit beside its new base, and
  `bq-scan-rem-gm-mulback-aa-distant`, kept early so the span stays. Run 8's
  tables name the old pair because that is what ran in them;
- `bq-mut-runs-gm-mulback` survives while its stated control
  `bq-mut-runs-mulback` does not, so the pair that prices dropping the size
  bound no longer exists — which is the ruling doing its work, since that
  pair's whole subject is the bound this rule now refuses;
- claim 4's controlled pair, `bq-scan-mulback` against
  `bq-expand-lemire-mulback`, loses both halves, and the Lemire output
  substitution loses its arm. Those *readings* stand as Run 8's and cannot be
  re-measured under this roster, which is the price of the rule and is
  recorded rather than worked around. Both *questions* survive on the
  counterparts written below, and [the claims
  list](#the-claims-run-10-should-test) has been re-aimed onto them.

**The crossed A/A design survives the cut, at half to two thirds the span.**
Its three distant twins are placed early and their bases late, and 23 of the
benches between them have gone: the spans fall to 25, 22 and 4 intervening
benches, from 38, 31 and 8. That is still nothing like the
twelve-arm probe where [spans of 28 and 0 read alike][floor], so the design
keeps doing what it was built for; what it does not keep is comparability
with Run 8's span column, a Run 9 pair being a different distance apart under
the same name.

**Every dropped arm was then checked for a surviving counterpart that differs
only in not using the trick that costs the bound**, and the check turns on
splitting the bound by where it arises, since a substitution at one site does
nothing for the other. `baseOffsetsScan`, `baseOffsetsScanPacked` and
`baseOffsetsGenLemire` carry a bound of their own — on `m` rather than on `l`,
which is what their consumers' roster entries mark as *its builder's*;
`baseOffsetsExpand`, `baseOffsetsOdo`,
`baseOffsetsScanRem` and `baseOffsetsMutRuns` carry none. Eleven of the
fifteen dropped arms had a counterpart already timed — the mutable-scratch
family through `bq-mut`, `bq-mut-runs` and `bq-mut-runs-gm-mulback`, the scan
family through `bq-scan-rem-gm-mulback`, whose builder drops the bound the
Granlund-Montgomery output cannot reach, and `bq-gen-lemire` through `bq-gen`,
its Lemire being at the build site. Four had none and were written:
`bq-expand-gm-mulback`, `bq-odo-gm-mulback`, `mut-flat-gm` and
`offtab-scan-rem`, the last not a Granlund-Montgomery twin because its bound
is its builder's. All four clear the allocation bar already, at 1.33x, 1.51x,
2.00x and 2.35x — measured twice, on a quiet machine and a busy one, to the
same digits, which is the property the bar was chosen for. What Run 9 still
has to say about them is only whether they are fast.

Two of the eleven are covered at the level of the idea rather than
line-for-line, and say so here rather than being counted quietly.
`bq-expand-lemire-out`'s counterpart is the mul-back output, Granlund-
Montgomery having no `out` analogue that yields quotient and remainder
together. And **the `Int32` narrowing cannot be rescued at all**: its bound is
`int32Fits` on the source, which is what narrowing *means*, so `offtab32` and
`bq-expand32-lemire-mulback` leave with no unconditional form possible. That
is the ruling's sharpest cost, because the narrowing is the one hand-packing
that survives the flag — 0.877 of its control for `offtab32` and 0.949 for the
expansion pair, where the packed state is dominated. The ruling stands as
taken; what it gives up is measured and recorded rather than assumed small.

`--lint` and `--markdown` both took the change with the roster: the first
asserts every defined `fb` function is rostered, which the not-timed mechanism
satisfies, and reports the not-timed set as a note rather than a failure; the
second carried `needs` and `precondition` forward from the table above, so the
column left the reader and the table in the same commit — a column dropped
from one alone would be reinstated by the next install.

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
**The eight class blocks are the bulk of it**, and mostly mechanical: write
each from the verdicts `--block` emits rather than from the table above them,
keep each to one paragraph, and expect them to take longer than the main
set's write-up did. Two further consequences worth having in mind before
starting. Prefer analysis that localises — per shape, per control — over
re-quoting figures that moved a few percent and changed nothing; the first is
where the surprises have come from and the second is what has gone stale
twice.
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

    cabal run micro $REGIME -- -L1 cnn-slice-c32 --json smoke.json
    cabal run micro $REGIME -- classes window-28x28-k5 -L1 --json smoke-class.json
    for f in smoke.json smoke-class.json; do
      for m in --selftest --aa --shapes --markdown --cells --fingerprint \
               "--pair bq-expand list" ""; do
        ./read-run.py $f $m >/dev/null || echo "BROKEN: $f $m"
      done
    done
    ./read-run.py smoke-class.json --block >/dev/null || echo "BROKEN: --block"
    cp README.md README.smoke.md            # --in-place WRITES; never at README
    for m in --markdown --fingerprint; do
      ./read-run.py smoke.json $m --in-place --readme README.smoke.md \
        >/dev/null || echo "BROKEN: $m --in-place"
    done
    ./read-run.py smoke-class.json --block --in-place --readme README.smoke.md \
      >/dev/null || echo "BROKEN: --block --in-place"
    cmp -s README.smoke.md README.md \
      && echo "BROKEN: --in-place wrote nothing"
    rm smoke.json smoke-class.json README.smoke.md

These carry `$REGIME` like everything else, though they exercise the reader
rather than the regime: leaving it off costs two rebuilds and leaves the
binary in the wrong regime for whatever runs next.

`--in-place` earns its three lines because it is the one mode that writes:
pointed at `README.md` it would install a one-shape smoke table over the
published one, so the copy is the point, and `cmp` afterwards is what keeps
the check from passing on an installer that found nothing and said nothing.
Run the copy's own diff by eye if a table looks wrong; the copy is deleted
with the rest.

The first runs every timed arm on one shape and puts the whole analysis
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

**After a roster change, add a `-L1` pass over the main set and one
three-shape class**, which is about twenty minutes and reaches three things a
one-shape smoke cannot. `--selftest` skips a whole block on one shape and
says so — winsorizing, the six A/A identities and the baseline identity,
none of which is an identity of anything until there are shapes to be one
over. Every claim's `--pair` line goes unrun, and a claim re-aimed at an arm
the run does not carry fails only when someone runs it. And `--block`'s
per-shape line is guarded by `len(shapes) > 2`, so it is dead on a one-shape
file — a guard that hid an edited line of this reader through a whole smoke
sweep. `rev`, `revsome` and `bcast` are the three-shape classes.
Its numbers go nowhere: `-L1` is a rougher budget than any recorded run's,
and this pass is a test of the reader, not a measurement.

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
    REGIME=--ghc-options=-fspec-constr   # Runs 8 and 9's; empty for -O1
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

**Check what a filtered selection actually selected.** Criterion takes one
`-m MODE` and then its patterns positionally, so `-m glob A -m glob B`
matches *nothing* and the process exits at once -- which looks exactly like a
fast run and cost one probe here before the zero timings gave it away. Count
the `benchmarking` lines against what was asked for before reading any
number out of a filtered run; it is the prove-a-search-non-vacuous rule
applied to bench selection, and the same count catches a pattern that
silently caught more arms than intended.

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

1. **Gate every population on the correction, before reading any figure --
   and read the A/A *worst cell*, not only the pair's geomean.** A control
   that passes its gate can still be the run's most informative measurement:
   `bq-expand`'s distant twin passed on Run 8 and again on Run 9 while
   carrying a 41% cell, published both times as a noise floor, and chasing
   that one cell is what produced the roster fix and the nursery account
   [in the floor section][floor]. A pair inside the floor whose worst cell is
   an order of magnitude outside it is not noise; it is a finding the
   aggregate is hiding.
   The gates themselves:
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
5. **Rename the three run-numbered headings** -- the chapter head, *What Run
   N compares against* and *The claims Run N should test* -- and repoint every
   link to them. It is mechanical, it is easy to forget because nothing in
   the numbers asks for it, and `--check-doc` catches the fallout as dead
   anchors rather than as the rename it was: Run 9 left eleven.
6. Walk the list under [Provenance](#provenance) of what the new numbers
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
7. **Verify the write-up before deleting anything.** These are the checks the
   procedure used to leave to judgement, each of which has caught something:
   1. **derive every count and ratio in the prose from `--cells`, never by
      eye** -- and for a class paragraph, from the verdicts `--block` now
      emits under its per-shape line, which state the three properties'
      outcomes and name the arms that actually lead. That block exists
      because this rule kept losing to the table being right there while the
      paragraph was written: three of Run 9's class sentences were wrong that
      way and no mechanical check saw any of them. "32 of 33", "30th of its
      33 shapes", "the only two past 7%" are all
      claims a glance at a sorted table gets wrong; two of Run 6's were wrong
      until recomputed. Two shapes of claim need naming because counting is
      not what they look like. **Every *only*, *largest*, *fastest* or *never*
      is a claim about the whole table** and is derived by sorting it, not by
      looking at the arms the sentence is about: Run 8's write-up carried four
      such — "the only arm the flag demotes", "the largest gain of any arm"
      among them — each false, and each caught late or by a reader. And **a
      ratio between two published cells comes from `--pair`, never from
      dividing the printed figures**, which are rounded to three digits: the
      same write-up quoted 0.9898 for a pair the reader puts at 0.9946;
   2. **reproduce any newly-derived column by a route that shares no code with
      the reader.** A four-bench filtered run carrying both `sum-only` halves
      takes seconds, and criterion's own printed `time` lines then give the
      ratio by hand: on `cnn-slice-c32`, `(1.506 - 0.1739) / (6.339 - 0.1739)`
      = 0.2161 against the reader's 0.216. Recomputing from `--cells` is worth
      doing too, but it shares the reader's arithmetic and cannot catch a wrong
      definition, only a wrong transcription. Two rules the independent route
      needs, both learned by getting them wrong after Run 9. **Difference wall
      time, or user *and* system -- never user alone**: the inherited "wall
      and user time agree on it" is a property of the workload it was written
      for, and where the RTS does kernel work they part completely, which is
      how 0.36 ms per call of system time went unseen and a real 10% effect
      was reported as zero. And **difference at two scales**: if the per-call
      figure moves with `n`, part of what is being divided is a fixed cost,
      which is how a one-time 0.9 s of page-faulting read as half a
      millisecond a call;
   3. **when two instruments disagree, that is the finding.** Do not average
      them, pick the one the page prefers, or quietly drop the awkward one.
      Locate the disagreement first: the criterion slope and the `-n`
      differencing above parted by 8 points on one arm, both reproducible to
      a fraction of a percent, and the cause was neither sampling nor sample
      size but which clock was being read. Until it is located, neither
      number is evidence, and a retraction made on the strength of the wrong
      one is worse than the claim it withdrew;
   4. **install the tables with `--in-place` rather than pasting them.**
      `--markdown`, `--fingerprint` and `--block` each take it, and each
      refuses rather than guessing: the match is by whole line, the count is
      asserted, and a class table is narrowed by its block's bolded lead.
      Hand-pasting is what this replaces, and the reason is on the record —
      the cross-class summary's header is written out twice, once indented as
      the spec that fixes the columns, and a session locating the table by
      searching for that text put Run 8's rows under the spec and left Run 7's
      table standing, with every check green because the check looked it up
      the same way. If you paste by hand anyway, do not edit the table: it
      renders the same rows the terminal does, and carries `needs` and the
      emphasis forward from the table already there.
      Its stderr is the whole of what is left by hand: a row new to the roster
      comes out with `?`, a departed row is dropped with a warning. Run 9 had
      ten such rows and filled them from a note written here before the run,
      which is the practice to repeat whenever a roster change is known in
      advance — the cell then gets transcribed rather than invented at the end
      of a long day. Each class
      JSON emits its own table the same way and is pasted the same way, into
      its block in [The stride classes, run by
      run](#the-stride-classes-run-by-run); those come out six columns wide,
      `needs` being a property of a strategy rather than of
      a population and so stated in the main table alone. The per-shape
      fingerprint is pasted the same way, whole, from `--fingerprint`;
   5. **assemble the cross-class summary last, from the tables and not from
      the JSONs.** Every cell of it appears in one of the class tables above
      it, so it is a transcription and is checked as one — cell against table,
      each in turn — where recomputing it from the runs would be a second
      derivation able to disagree with the tables it summarises;
   6. **check that every `](#...)` resolves**, here and in `Main.hs`'s
      `README.md#...` references, and that every figure-bearing section is
      linked from the Provenance list. Findings rename headings, and a renamed
      heading breaks a link silently;
   7. **walk the diff against the writing rules as a check of its own, not
      only while writing.** The replace-list walk manufactures "now X, where
      it was Y", requoting a count in place preserves a sentence that should
      have lost its numeral, and a class paragraph's close invites a
      mechanism the run never measured. `--check-doc`'s figure sweep lists
      candidates, `Main.hs` comments included, but the redo test itself is
      the reader's. Run 7's write-up carried fifteen-odd such sentences past
      every green check here, found only when a reader asked;
   8. **read the document end to end**, and aim the reading at what the
      instruments cannot see. The mechanical passes above do not catch
      a bullet contradicting the table three lines below it, which is how
      "`bq-mut` ties `bq-expand`" survived two runs beside a build ordering that
      refuted it. Nor do they see the three things Run 8's write-up got wrong:
      a table installed in the wrong place, an exclusivity claim about arms
      nobody sorted, and a figure quoted on a basis it was not measured on.
      That the checkers here are good is itself the hazard — green instruments
      make the remaining gap feel small, and the gap is exactly where they do
      not look, so read for placement, for *only* and *largest*, and for which
      run and basis each figure belongs to. This is the pass that keeps
      finding real errors;

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
8. Rebuild and re-run `--lint` and `check` after editing `Main.hs`, even when
   only comments changed: the reader parses that file for the roster and the
   shape dims, so a comment edit can break a check that passed before it;
9. Record beside the numbers the run's name and regime, each process's stderr
   provenance line, which machine, **and the commit the binary was built
   from** (the JSONs do not survive, so the source is the only thing that
   makes a run reproducible even in principle — this page's figures are one
   desktop's and are not portable, see [Provenance](#provenance)). A class
   process's line is measured for its elapsed time and its two heap peaks but
   not for its shape count: that count is fixed before criterion does the
   selecting, so it reads every class view rather than the population that
   ran, and the population's own size comes from the reader's first line;
10. **Walk the open list against what this session actually did**, which
   nothing checks. A run answers some of its own questions and a write-up
   raises others, and both go stale in place: Run 8 answered the element-type
   entry with the probe that entry specified and left it standing open, and
   answered the packed-arm entry the same day. Move what was answered into
   the answered block with its measurement, leave what a probe narrowed as
   narrowed, and add the run's surprises with the measurement that would
   settle each.
11. **Spend the load-independent measurements before the artifacts go.**
   Allocation is deterministic per call, Core is a compile, and a binary's
   size is a `size` invocation — none of them wants a quiet machine or a run
   slot, and each is minutes. Run 8 stopped at the write-up and left a Core
   diff, a two-regime `diag` and a code-size figure undone; all three were
   done later, two of them changed rulings, and one answered an open question
   outright. So before step 12, take every question on the open list whose
   measurement is a compile, an allocation or an arithmetic re-derivation,
   and take it now. What is left over is the timing work, which is what a
   quiet machine is for.
12. **Only then**, and after asking the user, delete the artifacts —
   the JSONs, the logs and the wall-clock file alike.
   The normal state of this directory is no run
   artifact at all, which is decided rather than an oversight; the numbers live
   in this file and the artifacts do not. But "afterwards" means after the
   verification above is done, presented to the user and accepted,
   not after the writing: Run 6's artifact was deleted as
   soon as its write-up was drafted, which cost the ability to re-check
   anything needing the raw samples when the write-up was later questioned.
   What they buy while they live is worth knowing before answering: every
   `--pair` a later question wants, every per-shape spread that separates a
   bias from noise, and every count re-derived from `--cells` needs the JSON
   and nothing else does. Run 8's were kept and drawn on a dozen times in the
   days after, for questions its write-up had not thought to ask.


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
    ./read-run.py RUN.json --block          # a class block's parts, + verdicts
    ./read-run.py RUN.json --markdown --in-place   # install it, do not paste
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
Results table already in this file for the one column a run cannot know —
`needs` — and for which rows the prose emphasises, carries
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
point once, the arm dropped being the only one the probe was about. The
general guard is to count what a filtered run selected before reading it
([the procedure](#making-a-major-benchmark-run)), which catches this and the
repeated-`-m` mistake alike.

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
deliberately not timed is a note rather than a failure, and since the two
rulings that note is the larger half of the strategies: it prints the split
and wraps the names, being the one place the checked-but-untimed set is
listed at all.

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
| `bq-expand` vs adjacent twin | 1 | 0.9997 | 0.24% |
| `mut-odo-vecdims` vs distant twin | 4 | 0.9993 | 0.31% |
| `mut-odo-vecdims` vs adjacent twin | 1 | 0.9994 | 0.26% |
| `bq-scan-rem-gm-mulback` vs adjacent twin | 0 | 1.0007 | 0.19% |
| `bq-scan-rem-gm-mulback` vs distant twin | 22 | 1.0007 | 0.31% |
| `bq-expand` vs distant twin | 25 | **1.0152** | 2.16% |

No pair had a cell capped, so every published figure above equals its paired
one — the identity the winsorized estimator bought and `--selftest` asserts —
and the published column is the yardstick for comparing two rows of the
Results table, while a margin measured per shape still belongs against the
paired figures `read-run.py --aa` prints.

**On Run 9 the floor is 0.07%, and one cell is everything else.** Five of the
six pairs sit within 0.07% of 1 — the tightest this page has recorded, by a
factor of five. The sixth, `bq-expand` against its distant twin, reads 1.0152
and owes **all** of it to one shape: drop `vgg-14-c512-k3` and the pair is
1.0007 over a 0.987–1.014 per-shape range, level with the other five. So the
threshold this run supports is *under 0.1% between any two rows, with one
wild cell in the set*, where Run 8 supported 0.5% and Run 7 nearly 4%. Runs
disagreeing several-fold on the floor is itself the caution: read the floor as
the run's, re-measured every time, not as a constant of the harness.

The CI% for those six rows reads 0.04-0.25%, so the interval understates
run-to-run variability by nearly an order of magnitude: it
measures sampling error *within* one benchmark, while two separately placed
benchmarks also differ in code layout, cache occupancy and inherited GC
state. The A/A is the only column that sees that, and `--aa` prints the
calibration outright — on Run 9, a median interval half-width of 0.16%
against an observed spread of 1.52%, a factor of **9** — so multiply any
interval this reader prints by about that before believing it, where Run 8
wanted two and Run 7 three. The factor is this large because the spread is
one cell; on the other five pairs the intervals are honest.

**The wild cell is the same cell as Run 8's, and this run ran it down.** Run
8 recorded `bq-expand`'s distant twin 44% slow on `vgg-14-c512-k3`, on
identical allocation, and left it as an oddity. Run 9 reads 41.4% on the same
arm and the same shape, so it is not a fluke, and five filtered probes
(2026-08-09, the run's own binary and regime) say what it is:

- It **reproduces deterministically**. The twin reads 4.46 ms in the run and
  4.50 ms alone; the two adjacent copies read 3.315 and 3.314 ms in the run.
  Same code, same allocation, tight intervals on all of them.
- **The slow figure is the arm's real isolated cost, and the published one is
  the anomaly.** Run `bq-expand` in a two-bench process and it reads 4.52 ms
  — the *distant twin's* figure, not its own published 3.32. So the twin at
  roster slot 3 is measuring the arm correctly and the arm at slot 29 is
  being flattered by 26%.
- **It is the whole expansion family, not one arm.** Filtered into a small
  process, `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback`
  each read 35–40% above their published cells on this shape, while
  `bq-scan-rem-gm-mulback` (2.275 ms against 2.279) and `mut-odo-vecdims`
  (1.566 against 1.570) do not move at all. Susceptibility is a property of
  the arm, and these are five more arms with it settled.
- **One single predecessor does all of it, and it is `sum-only-early`.** Six
  bisection probes looked for a cumulative cause and found none — `list`
  first, `bq-gen` between, slots 4–16, 17–22 and 24–28 each left the arm slow
  — because every one of them omitted the bench that matters. Put
  `sum-only-early` between the twin and the arm and `bq-expand` reads 3.347
  ms; put `mut-odo-vecdims` there instead and it reads 4.583. Nothing else is
  needed and nothing else substitutes. `sum-only` times a sum over a *fixed*
  vector, so its setup allocates one `l`-sized buffer and then allocates
  essentially nothing per call — a single large allocation that grows the
  block pool and leaves it grown, which is exactly [the position
  effect][pos-effect]'s mechanism and not code placement, the binary being
  identical throughout.

  **That made it a roster-order defect rather than a curiosity, and it is
  now fixed.** `sum-only-early` sat at slot 5 with the three distant A/A
  twins at slots 2, 3 and 4 — *before* it — so those three controls were
  measured against a colder heap than every strategy they exist to
  calibrate, and the only reason two of them looked fine is that they twin
  arms with too little excess allocation to care. A "distant" twin was
  therefore varying heap state as well as position, which is not what the
  crossed design says it varies. `sum-only-early` now runs at slot 2,
  directly after `list` and ahead of the twins; the reasoning, and why it
  stays *after* `list` rather than before, is at its roster entry in
  `Main.hs`.

  **Proven non-vacuous, as a fix to a measurement has to be.** The same
  three-bench probe that isolated the cause, re-run on the moved roster at
  the default nursery, puts the twin at 3.367 ms and its base at 3.375 —
  **0.24% apart**, where the identical selection before the move read 4.53
  and 3.35. The 41% cell is gone, and gone for the stated reason rather than
  by any change to what the arms compute.
- **It is not GC time.** Under `+RTS -s` the cold two-bench
  process spends **5.8%** of its total time collecting (productivity 94.2%,
  41 MiB in use) and the warm 34-bench one **2.3%** (97.7%, 60 MiB). Even
  abolishing collection outright in the cold process buys 5.8% against a 36%
  gap, so the cost is inside MUT.
- **The allocation area is what it turns on, and `-A32m` removes it
  outright.** `-H512m` does nothing (4.74 and 5.16 ms raw), so it is the
  nursery specifically and not the heap size. An eight-point sweep, all on
  this shape and all **net** of the forcing pass, with `mut-odo-vecdims`
  carried through as a control the predictor says must not move:

  The two left columns are criterion slopes on the **pre-fix** roster, where
  the twin was still cold, and are here to show it converging. The two GC
  columns are exact rather than normalised: taken at a fixed `-n`, every
  setting allocates the identical 41.066 GB, so the counts are directly
  comparable and no per-GB rate is needed.

  | `-A` | twin (cold) | its base | gen-0 | gen-1 | in use |
  |---|---:|---:|---:|---:|---:|
  | default | 3.934 | 2.799 | 5789 | **255** | 56 MiB |
  | 32m | 2.508 | 2.497 | 945 | 2 | 103 MiB |
  | 64m | 2.502 | 2.537 | 481 | 2 | 174 MiB |
  | 128m | 2.477 | 2.506 | 242 | 2 | 316 MiB |
  | 256m | 2.420 | 2.450 | 120 | 2 | 603 MiB |
  | 512m | 2.368 | 2.420 | 59 | 2 | 1177 MiB |
  | 768m | 2.457 | 2.506 | 39 | 2 | 1752 MiB |
  | 1G | 4.854 | 5.644 | 0 | **31** | 2318 MiB |
  | 1G, `-M8G` | 2.661 | 2.647 | 29 | 2 | 2324 MiB |

  The gen-0 column is the method checking itself: it falls as `1/nursery` at
  a constant 0.74 of the predicted count, that fraction being the large
  objects that bypass the nursery altogether. `-A1G` under the cap is the one
  row where it collapses to **zero** — a 1 GB nursery the 2 GB cap will not
  let it fill, so the RTS does 31 major collections instead of minor ones.

  **What the sweep settles is the cold arm, not the warm one.** The twin
  converges on its arm from 32m onward — 41% apart at the default, within 2%
  everywhere after — so a large nursery is a second route to the state the
  roster fix now reaches: it spares the *cold* arm the pool growth rather
  than paying for it. Major collections confirm it deterministically. Re-run
  at a fixed iteration count, where every setting does identical work (41.066
  GB allocated at all nine, which is the method checking itself), gen-1
  collections read **255** at the default and **2** at every larger nursery
  but `-A1G`-under-cap, and gen-0 falls as `1/nursery` at a constant 0.74 of
  the predicted count, the large-object fraction that bypasses the nursery.

  **It buys on a warm arm too, and the cost it removes is KERNEL time.** This
  took resolving, because two instruments disagreed and the losing one was
  mine. Criterion's slope put `bq-expand` at 2.795 ms net at the default
  against 2.501 at `-A32m` (quiet machine, three interleaved reps, spread
  under 0.4%), while differencing the process CPU at two iteration counts put
  the two level. Neither sample size nor GC interleaving explained it — at
  `-L60`, where criterion's samples reach 839 iterations, its ratio is
  unchanged at 0.903. **What explained it is that `/usr/bin/time -f %U`
  reports user CPU only.** Split the clocks and the default's missing cost is
  in *system* time, 0.29 s at `-n 800` and 0.58 s at `-n 1600` — perfectly
  linear, so **0.36 ms of kernel time per call** — where `-A32m` pays 0.03 and
  0.04 s, which is fixed startup and nothing per call. Differenced on wall
  time the two instruments agree: 3.300 ms against 3.075. So the small
  nursery's price is memory-management work in the kernel, an arm allocating
  13.2 MB per call beyond its result against a 4 MB area, and a user-CPU
  measurement cannot see it. The general lesson is worth more than the
  figure: **difference wall time, or user *and* system** — a page rule
  inherited from horde-ad says "wall and user time agree on it", which was
  true of the workload it was written for and is false here.

  **The predictor called it, on a control shape.** `cifar-L2-16-c64-k3` has
  1.59 MB of excess per call, below the 4 MB area, so it should show neither
  kernel time nor benefit. It shows neither: system time is 0.00-0.01 s at
  both settings and does not scale with `n`, and `-A32m` is if anything 6%
  *slower* there. Two shapes, opposite predictions, both confirmed.

  **`-A1G` is a cliff, and the cliff is the `-M2G` cap and not the nursery.**
  The arm reads worse than the *default* — +20.3% by differencing — and gen-1
  collections go from 2 to 31 at identical work. Re-run at `-M8G` and it
  rejoins the others exactly (gen-1 back to 2). The high-water mark, 2318
  MiB, is the first in the sweep to cross `micro.cabal`'s 2048 MiB cap, and
  crossing it is the whole of the effect. So a large nursery is not
  intrinsically bad here; a large nursery *under this cabal file's heap cap*
  is pathological, and would also destroy the guard the cap exists for.

  **What a caller should run with is a different question, and it answers
  cleanly.** The suite's question is which setting measures best; a user of
  `Data/Array/Internal.hs` wants the cheapest real cost, which is wall time —
  kernel work is cost to them — with no `-M` cap in the way. Differencing
  wall time at `-n 400`/`-n 800`, `-M8G` throughout, on the shape where the
  effect is largest:

  | `-A` | `bq-expand` per call | per-call kernel | one-time kernel | peak RSS |
  |---|---:|---:|---:|---:|
  | default | 3.275 ms | **0.350 ms** | -- | 67 MiB |
  | 32m | 3.075 | ~0 | 0.04 s | 109 MiB |
  | 64m | 3.075 | ~0 | 0.06 s | 180 MiB |
  | 128m | 3.075 | ~0 | 0.17 s | 323 MiB |
  | 256m | 3.075 | ~0 | 0.33 s | 580 MiB |
  | 512m | 3.100 | ~0 | 0.64 s | 956 MiB |
  | 768m | 3.025 | ~0 | 0.92 s | 1374 MiB |
  | 1G | 3.025 | ~0 | 1.20 s | 1759 MiB |

  **Everything from 32m to 1G is one price at this size, and 32m is the
  cheapest way to buy it.** The whole 6.1% is captured at 32m; above it the
  per-call time is flat and only the costs grow — memory linearly, and a
  one-time kernel charge of roughly **1.2 s per GB** as the area is faulted
  in. That fixed charge is what makes a small-`n` measurement of a large
  nursery look catastrophic: divided over 100 calls it reads as half a
  millisecond each, and it is not per call at all. The gain also exists only
  where an arm's per-call excess outruns the default 4 MB, so on
  `cifar-L2-16-c64-k3` (1.59 MB) every enlarged nursery is *worse* — 0.465 ms
  at the default against 0.480 to 0.500 across the band. And `-A1G` is safe
  here only because `-M8G` removes the cap.

  **But "at this size" is load-bearing, and the advice inverts above the
  shape cap.** Real callers use arrays past `sizeCap`, so the `tooBig` shapes
  were promoted into the shape set behind a temporary edit and measured
  (2026-08-09, `-M20G`, busy machine, min of 5; the edit is reverted).
  Allocation first, which is exact and load-independent, and which confirms
  the one thing that does scale: **excess allocation is linear in `l` to
  three digits** over a 32× range — `bq-expand` 14.6 to 14.7 B/element,
  `list` 190.2 to 190.4 — so at `imagenet-224-c64-k3` (`l` = 28.9M) a single
  call churns **425 MB** past its result, and `list` churns **5.50 GB**.

  | `-A`, at `imagenet-224-c64-k3` | `bq-expand` | its kernel time | `list` |
  |---|---:|---:|---:|
  | default | 113.5 ms | 13.5 ms | 1040 ms |
  | 32m | **134.0** | **31.0** | 637 |
  | 64m | 94.5 | ~0 | 603 |
  | 128m | 99.0 | 1.0 | 657 |
  | 256m | 99.0 | 1.0 | -- |
  | 512m | 100.0 | 0.5 | 603 |

  **`-A32m` goes from the best setting to the worst one** — worse than the
  default, by 18%, on 31 ms per call of kernel time, and it reproduced in two
  passes. Whatever the 4 MB default does badly at this scale, 32 MB does
  twice as badly, and 64 MB stops doing it at all. The threshold therefore
  moves with `l` but **nowhere near linearly**: 32m suffices at `l` = 0.9M and
  fails at 28.9M, while 64m covers both — a 2× nursery across a 32× size, not
  the 425 MB a "nursery must exceed the excess" rule would demand. That rule
  is refuted; what sets the threshold is not measured here.

  Two more things the big shapes change. The prize **grows** rather than
  shrinking with size — 6% at `l` = 0.9M against 12-17% here, and ~40% for
  `list` — so the guess that DRAM-bound behaviour would swamp the allocator at
  scale is wrong. And the fix's margin over what it replaced narrows under a
  bigger nursery at *every* size measured, 9.2× to 6.4× here against 10.2× to
  6.4× at `l` = 0.9M, which is the same effect at a 32× remove.

  **So, for a caller: `-A64m` to `-A256m`.** It is the only band that is good
  at both ends — the default leaves 6-17% on the table above `l` ≈ 1M, `-A32m`
  is actively harmful at the top of the range, and above 256m nothing improves
  while memory and startup keep growing. Below `l` ≈ 1M, stay on the default.
  These are busy-machine wall figures and the ±5% between neighbouring
  settings should not be read; the kernel-time column is what carries the
  finding, being the mechanism marker and far less disturbed by load.

**So the mechanism is settled: an arm allocating more per call beyond its
result than the nursery holds pays for it in kernel memory management, and
the default area is 4 MB.** The first consequence is the one already acted
on — the roster move, which warms every timed bench and takes the cell from
41% to 0.24%.

**The second is much larger and is not acted on: `list` is the most
nursery-sensitive arm on this page, so the published ratios are themselves a
statement about the default allocation area.** Its excess is predicted at up
to 353 MB per call, two orders above `bq-expand`'s, because a cons list of
`l` elements is nothing but small-object allocation. Measured on
`vgg-14-c512-k3`, quiet: `list` goes **28.659 ms to 16.019 ms**, a 1.79×
speedup, where `bq-expand` gains 10%. The ratios therefore do not cancel,
they move hard —

| on `vgg-14-c512-k3` | default | `-A32m` |
|---|---:|---:|
| `bq-expand` / `list` | 0.098 | **0.157** |
| `mut-odo-vecdims` / `list` | 0.036 | **0.065** |

— so on this shape the shipped fix beats the fallback it replaced by 10.2×
at the default area and 6.4× at 32 MB. **Both are true; they answer different
questions.** The default is what a GHC program gets unless it says otherwise,
so the published column is the right one for "what does a caller see today",
and this page has only ever measured that. What it is *not* is a
nursery-independent property of the two algorithms, and the headline ratios
should not be read as one. Quantifying it over the whole table is a run, not
a probe: one shape is not the geomean, and the small shapes — where every
arm's excess is under 4 MB, as the `cifar` control shows — will move nothing.

**So position reproduced after all, and much larger than the twins price
it.** Run 7 read the distant twin above the adjacent one within every
strategy and growing with span; Run 8 read that as not reproducing. Run 9
says both were looking at a summary of the wrong thing. Aggregated over
shapes the effect is nothing — three of Run 9's six pairs sit *below* 1 —
while on one shape and one family it is 35–40%, which no geomean over 24
shapes can show. The standing advice survives and sharpens: `list` runs in
the coldest slot, arms far down the roster are **flattered** rather than
penalised, and now there is a measured case of by how much.

**What did turn up is a bigger placement effect, from an accident.** `build`
and `mut-odo` compile to the same worker — checked in Core at -O1 and again
under `-fspec-constr` — so they are a seventh known-true-ratio-1 pair, and
they disagree by 1.24× on Run 7, 0.86× on Run 8 and **1.13×** on Run 9 (3
wins of 24, sign p 0.00028). Three runs, one of them differing from its
predecessor in membership alone, and the pair spans 0.86 to 1.24: that range
is the instrument, and it is 44% wide for code that is identical. The twins
share one worker called from two slots; those two are separate
copies of one worker at two addresses, and the gap between what the two
instruments read is the part of layout the twins cannot see. Do not price a
margin between distant rows at the twins' floor.

**And those two addresses now have a candidate consequence, read out of the
binary** (2026-08-09, `-fspec-constr`). The innermost run-fill is 28 bytes —
seven instructions and a backward branch — and the binary carries four
byte-identical copies of it, two per arm, the only alignment directive
anywhere in either procedure being `.align 8`. One copy per arm is the
mismatched-length `fail` join and cannot run on a well-formed shape; the
copies that do run are `mut-odo`'s at byte 29 of its cache line, which fits,
and `build`'s at 53, which straddles two. The dead copies fall the other way
round, which is why the pair looks like a wash until the executed one is
identified. That is one bit against one gap, so it is a candidate and not an
account — but it is one the pad probe can test, nothing pinning these loops
to a line: pad in eight-byte steps until `build`'s executed copy lands whole
and see whether the gap goes with it. The instrument is steady meanwhile,
the flag's 12 KiB of `.text` reproducing to the byte on a base the arms
written since have grown.

**And a second family reads the same way, which is what takes it past one
point.** The four `mut-odo-vecdims` arms carry one copy each of that same
28-byte fill, the FastReshape three differing from their control nowhere
inside it ([the mutable ceiling](#the-mutable-ceiling-not-taken)), so their
copies stand beside `build`/`mut-odo`'s:

| arm | loop | mod 64 | lines | Run 9 against its control |
|---|---:|---:|---:|---:|
| `mut-odo-vecdims` | 28 B | 24 | 1 | — |
| `mut-odo-vecdims-add-in` | 28 B | 40 | 2 | 1.1552 |
| `mut-odo-vecdims-add-out` | 28 B | 44 | 2 | 1.1795 |
| `mut-odo-vecdims-add-both` | 28 B | 44 | 2 | 1.1645 |
| `mut-odo-vecdims-add-both-down` | 24 B | 33 | 1 | 1.0183 |
| `mut-odo` | 28 B | 29 | 1 | — |
| `build` | 28 B | 53 | 2 | 1.13 |

Every copy that fits inside one line reads level or ahead, every copy that
straddles reads 13–18% behind, and no arm of either family dissents. The
count-down form is the one row whose loop is not that code — it is the
shorter one, and line-resident as well — so it sits here for completeness
and is read in its own section. This is still a correlation inside one
binary, and 64 bytes is the granularity of more than the cache line, the op
cache included, so the pad probe stays the test rather than the
confirmation. What it stops being is a guess.

**And the identical-code pair reads the same way in all nine of Run 9's
populations**, one binary throughout, so the gap owes nothing to the main
set's choice of shapes: `build`/`mut-odo` runs 1.078 (`window`) to 1.375
(`bcastmid`), above 1 in every population, with `build` slower on 39 of the
43 shapes between them. That widens the range as much as it confirms it — 8
to 37% across populations against the 13 to 18% the main set alone shows —
and it is smallest in the class whose views overlap and reuse cache, which
is the direction a front-end cost would take, though nothing here measures
that.

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

**Bisect a position effect by REMOVING from the full group, never by adding
to a pair.** Six probes here searched for what warmed `bq-expand` by building
selections up from a hypothesis, and every one of them omitted the single
bench that did it, because a hypothesis-shaped selection can only contain
what has already been thought of. Removal cannot make that mistake: start
from the whole group, which is known to show the effect, and take benches
away until it stops.

**A filtered run cannot answer the position question by measuring spans**,
and the trap is quiet enough to be worth stating: criterion's selection
removes the intervening benches, so a pair placed 28 slots apart in the
roster ends up adjacent, and the crossed design collapses to six
near-identical adjacent pairs. Measured on a twelve-arm probe, spans of 28
and 0 both came out under 6. `--aa` says so when the run is filtered. A span
this way is unmeasurable, and the whole roster in the process is what the
crossed design needs.

**What a filtered run can do is put every arm at the cold end**, which is how
Run 9's five probes worked and why they answered. Collapsing the spans is not
a defect there: it removes the warming, so every arm reads its isolated cost,
and the published cell is then held against *that* rather than against
another slot. Read the two uses apart — a filtered run cannot price the
distance between two slots, and it can price the difference between a warmed
process and a cold one, which is the larger of the two effects here by an
order of magnitude.

The floor grew with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a
real difference. On raw slopes Run 9's six pairs read 0.9998 and 1.0130,
0.9998 and 0.9997, 1.0005 and 1.0005 — adjacent and distant per strategy —
so the largest deviation was 1.30% before the correction and is 1.52%
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
a second effect riding along with it — and Run 9's pairs move the same way,
every deviation larger net than raw.

**Failed Run 6's two conclusions here are settled.** *1/time* is refuted as
an account of the floor: per-cell *scatter* does track it -- the adjacent
pairs in the table rank by their arms' speed -- but scatter cancels, and
the bias that survives cancelling ranks by span, not by any arm's speed.
*Position* was confirmed by the crossed design built for it, read as not
reproducing on Run 8, and is confirmed again by Run 9 in a form the crossing
cannot summarise: it is per shape and per family, not a trend in span. What
the crossed design settled for good is that the question is answerable at
all; what Run 9 adds is that the answer is not a single number.

Six A/A points are a modest estimate of a noise floor whichever run supplies
them, and Run 9's are the tightest and the wildest at once: five pairs inside
0.07% and one cell at 41%. That is the shape to expect rather than an
accident of this run — a floor that is very low nearly everywhere and
occasionally not a floor at all. So the threshold to quote is the running
one, and a margin under a tenth of a percent is not a result in any regime.

The floor above is also measured within one roster, and the roster is a
variable of its own: RTS pool state a predecessor leaves in the process
moved a horde-ad benchmark ~18% ([the full account][pos-effect] -- which
includes this suite's own floor measured isolated against in-process, on
both harness generations). Run 9 is that account reproduced here and larger,
its expansion family reading 35-40% above its published cells once the
process is emptied of predecessors. Every strategy sharing one process is
what protects the tables above, ratios cancelling the shared process draw --
and the vgg cell is what that protection costs when the draw is *not* shared,
one family warming and another not. A comparison that crosses runs should pin
the benchmark selection along with the binary.

**Every kind of comparison this page makes wants an instrument, and only
some have one.** Worth asking outright of any new claim, because the four
answers known so far differ by two orders of magnitude and none was found on
purpose: an arm against itself in one binary is the A/A twins at 0.07%; two
different arms in one binary carry placement, which `build`/`mut-odo` puts at
13-24% for a pair whose code is identical; one arm across two binaries
carries the rebuild, up to 18% on a susceptible arm; and one arm across two
*process populations* carries the warming, 35-40% on the expansion family at
`vgg-14-c512-k3`. The last is the largest and the newest. So when a sentence
compares something new — two populations, two machines, two GHC versions, an
arm against a prediction — ask which of these bounds it, and if none does,
say so in the sentence rather than borrowing the nearest number.

**Each population measures its own floor.** The same six controls ride every
process, so a stride-class run prices the noise of the process its own
figures came out of — which is the only process they can be judged in — but
it prices it over two or three cells where the main set has two dozen. Read a
class's controls as this floor confirmed there or not, rather than as a
threshold of that class's own, and never carry the main set's figure into a
class comparison or the other way about. Run 9's class processes are that
ruling observed: floors from 0.15% (`slice`) up to 2.32% (`window`), a
fifteenfold spread across populations of one run. The `mut-odo-vecdims` slot
carries the worst pair in **four** of the eight, where Run 8 put it in seven,
so that pattern has weakened rather than settled and is not yet a property of
the arm. The other four split evenly, `bq-expand`'s distant twin taking
`bcast` and `reshape1` and `bq-scan-rem-gm-mulback`'s taking `slice` and
`scaled`, which is no pattern at all.


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
rather than merely noisy. In Run 9 (SpecConstr) that is 1 cell of 816 in the
main set — `bq-expand-zf` on `stretch-inner256` at 0.9813, the same arm and
shape Run 8 flagged — and **no class process adds one**, where Run 8's added
`build` on `bcast-tall-Mx2`. Run 7 had two
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
`noise` figure by far; and the scatter has not recurred in either
`-fspec-constr` run, that arm reading an ordinary 1.01 on Run 9 while the
noisiest benches are `gen-quotrem` (5.57) and `gen-unsafe` (3.96). So
whatever the flag does to `mut-odo` — 19% slower per call than at -O1 — it
does not do it
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
   **Run 9 (SpecConstr)**: 1.0000 paired, 0.10% mean per cell, worst cell
   0.53%, the halves 28 benches apart; and every class process within 0.3%,
   the loosest being `scaled` at 1.0026.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape -- one sum over `l` elements -- and a term that were not
   could be wrong in both halves alike, leaving their agreement to notice
   nothing. It is: 0.592 to 0.607 ns per element across the whole shape set, a
   1.02x spread over that 6250x range of `l`, with the largest shapes a
   couple of percent
   dearer per element than the smallest and no trend beyond that. `--selftest`
   checks it on every run and fails the run past a 1.5x spread; all nine of
   Run 9's populations passed, none spreading past 1.02x.
3. *The read itself.* `sum-only` re-reads one **fixed** vector, where a
   strategy sums one its own fill has just written -- a different cache state,
   and the one thing neither gate above can see, since a term biased by it
   would be biased alike on every shape and in both halves. This is what
   `bq-expand-nosum` and `mut-odo-vecdims-nosum` are for: each is its base arm
   run again and forced with a single element instead of the sum, so *base
   minus arm* is that sum in situ. Measured against `sum-only` on Run 9 they
   read
   **0.9854** and **0.9764** as medians -- within 3%, on the two arms where
   the term is the
   smallest and largest share of the bench (a quarter of `bq-expand`, a third
   of `mut-odo-vecdims`), so the test spans the range over which a bias would
   matter. Per-cell scatter is 4.3% and 3.5%, the worst cells on
   `stretch-inner256` and `stretch-square-1341`. Failing
   is both medians leaving 1 on the same side by more than a few percent —
   the biased-read signature; one arm scattering while the other reads clean
   is a local disturbance for that population's write-up, not a failed gate.

   **It has now not bracketed for two runs, which promotes it from a thing to
   watch to a thing to price.** Run 7's two medians sat either side of 1; Run
   8's were both below, and Run 9's are both below again — as is **every**
   in-situ median of both arms in all nine populations, eighteen readings
   between 0.960 and 0.999. Two runs and eighteen readings on one side is no
   longer a coincidence at any reasonable reading. The in-situ sum costs
   *less* than `sum-only`'s re-read, so the term is slightly over-subtracted
   and every ratio slightly flattered — by about 0.5% of `bq-expand`'s own
   slope at a 2% error in a term that is a quarter of it, which is inside this
   run's floor everywhere but `bcastmid`, where the reading is 0.9597 and the
   flattery about 1%. The gate still passes on its own test, which asks for
   *more than a few percent*; what it has stopped doing is passing for the
   reason the test assumes. [The open
   list](#what-the-next-runs-have-to-decide) carries what would settle it.

   **The cells under those medians say the same, and add a gradient the
   medians hide** (2026-08-09, off Run 9's artifacts). Taken per shape
   instead of as a median, over both arms and all nine populations, the
   in-situ readings sit below 1 on 73
   cells of 86, sign p 2.7e-11 — and not because differencing two nearly
   equal numbers is noisy: calibrated on each arm's own A/A cells and
   amplified by the differencing, the scatter to expect is a fraction of a
   percent to a couple of percent, and three `bq-expand` cells of 24 and no
   `mut-odo-vecdims` cell fall inside it. The two arms also order the main
   set's shapes alike — Spearman 0.82, and 0.85 with the three cells above
   1.03 set aside — and two fills an octave apart in speed, at roster slots
   13 and 50, agreeing shape by shape is what a property of the read looks
   like rather than one of either arm. The gradient is in `l`: the shortfall
   runs about a tenth of the term at the smallest shapes and vanishes at the
   largest (smallest twelve shapes 0.955 and 0.960 by geomean, largest twelve
   1.027 and 1.002; r against log `l` 0.60 and 0.58), which is neither a
   per-call constant nor a per-element rate. Where it concentrates is the
   shapes whose result is L1-resident: the three at 32 KiB of result or
   under read 0.898 and 0.925 by geomean against 0.98 to 0.99 for everything
   larger, and between the L2 and L3 buckets it barely moves at all.
   Whether that is a step at the L1 boundary or a smooth trend three shapes
   cannot settle — with the cells above 1.03 kept a line in log `l` fits
   better and with them dropped a three-level step does, decisively for
   `bq-expand` and marginally for `mut-odo-vecdims` — so read it as
   concentrated in the L1-resident shapes rather than as a boundary effect.
   None of this replaces the third `-nosum` arm: a third write
   pattern is still the only thing that separates the read from these two
   arms, and this is evidence pointing that way rather than a substitute.

   **Priced, it is under a point.** Re-pricing each arm's own numerator with
   its in-situ term, the `list` denominator left alone at 2.7% of itself,
   moves Run 9's published main-set geomean to 0.9993 for `bq-expand` and
   1.0088 for `mut-odo-vecdims`, and each class's to between 1.0015 and
   1.0288, the largest under `bcastmid`, `scaled` and `bcast`. Per shape it
   reaches +3% and −8%, and the cells that move a published figure most are
   the three reading *above* 1 rather than the systematic shortfall. So the
   flattery is real, sits inside the layout span everywhere, and is worth a
   sentence about a particular cell rather than a second correction to the
   column.

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
  drift, Run 8 mostly did not, and Run 9 shows why both readings were of the
  wrong quantity ([the floor section][floor]): the effect is not a per-slot
  gradient to fit but a step, worth nothing on most arms and 35–40% on one
  family at one shape. **So a slot correction is now refuted rather than
  merely unmeasured** — a linear fit in slot number cannot express a step
  that depends on the arm, and fitting one would smear a real 40% across
  thirty rows that do not have it. What the drift needs instead is the
  warm-up bench, which addresses the step directly and is the only one of the
  three fixes Run 9 leaves standing. The placement gap the `build`/`mut-odo`
  pair shows is a separate and larger target, and no reordering addresses it.
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

## About the last run (Run 9)

**Run 9 (SpecConstr).** Criterion, GHC 9.12.4,
**`--ghc-options=-fspec-constr`**; Run 8's regime kept deliberately, with the
**roster** as the one thing that moved — Run 8's shapes, Run 8's class lists,
and the membership the two rulings under [what the benchmark
does](#what-the-benchmark-does) called for: 23 strategies and `list` timed of
58 rostered, where Run 8 timed all but one of 50. One process per
population — the main set, then each class in `classViews`' order, back to
back on an otherwise idle machine, 2h5m46s in all — built from commit
`96378d2` with a clean tree, on the same
desktop — Zen 3, a Ryzen 7 5800X. The main process's stderr provenance line
reads *roster 34
benchmarks over 24 shapes; elapsed 1h10m16s; peak 219 MiB in use, 74 MiB max
residency*, comfortably inside `micro.cabal`'s `-M2G`, which is why that note
stands unchanged — the shorter roster is why every figure in it fell against
Run 8's.

**The flag was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts
`baseOffsetsScan` at 2408938 bytes against `baseOffsetsMut`'s 2408530 on
`vgg-14-c512`, where plain -O1 separates the two tenfold. A run made in the
wrong regime passes every gate this page has and reads as a refutation of the
design it was built to test, so [the
procedure](#making-a-major-benchmark-run) puts that check before the run and
this line records that it was made. Both figures are Run 8's to the byte,
which is the instrument saying it did not move.

**The baseline did not move, and that is what this run buys.** `list` per
call, paired over the 24 shapes, reads **0.9979** against Run 8 — so for the
first time on this page two runs share a denominator and a ratio may be held
against its predecessor directly, where Run 8 against Run 7 needed the whole
absolute detour a regime flip forces. What the two runs differ in is
membership, and against a still baseline the absolute moves are the roster's
own: `mut-odo-vecdims` **0.910**, `mut-odo` **0.910**, `bq-scan-rem-gm-mulback`
1.001, `bq-expand` 1.034 and `build` **1.192**. Read that as a **span, not a
verdict**: a change that touched no line of any arm's code moved five arms
from 9% faster to 19% slower, and the two ends of it are `mut-odo` and
`build`, which [the placement
entry](#what-the-next-runs-have-to-decide) records as compiling to the same
worker. Identical code cannot move in opposite directions for a reason of its
own, so what the span measures is layout and placement, which membership
drags along with it. These five come from the two runs' fingerprint tables,
`list`'s net per call being kept there for exactly this; the published
columns give the same five as 0.906, 0.936, 1.000, 1.029 and 1.200, a cheaper
route that agrees to within 0.5 points except on `mut-odo`, where the two
part by 2.6 and the winsorizing is the difference.

**`list`'s own scatter is the closest thing to a drift measurement this page
has.** Its code, its regime and its roster slot are all unchanged between the
two runs, and its geomean moved 0.2% while single shapes moved by up to 5%
(0.934 to 1.048). That is not the clean repetition [Provenance](#provenance)
says is still owed — the roster around it moved — but it bounds what a
figure may do between runs for no reason at all, and it is the number to hold
a suspicious 3% against.

**Run 9 records every population**: the main set and the eight stride
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
`Data/Array/Internal.hs` compiles under, and a row's distance from Run 8's is
the roster's doing and not a strategy's, the flag being the same one.

**Comparing runs?** The table below is Run 9's own; what to hold a new run
against is [What Run 10 compares against](#what-run-10-compares-against), the
claims to test are [the ones after it](#the-claims-run-10-should-test), the
population and the absolute anchor are in [Provenance](#provenance), and this
run's own floor — 0.31% on five of the six A/A pairs and 1.52% on the sixth,
all of that sixth being one cell — is [in the floor section][floor].

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

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.23* | *79* | *2.35x* | *its base arm, forced with one element* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *92* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *102* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *102* | *0.00x* | *the same, at the other end* |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.101* | *0.06* | *82* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.048* | *0.101* | *0.06* | *81* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.048** | 0.101 | 0.05 | 82 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both-down | 0.049 | 0.121 | 0.11 | 82 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.056 | 0.123 | 0.11 | 79 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both | 0.056 | 0.130 | 0.14 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-out | 0.057 | 0.131 | 0.12 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.080 | 0.196 | 0.37 | 83 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.088 | 0.216 | 0.19 | 82 | 1.33x | mutable `Int` scratch |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.161 | 0.09 | 76 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.090* | *0.162* | *0.12* | *76* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.090* | *0.162* | *0.04* | *76* | *1.33x* | *A/A control* |
| bq-odo-gm-mulback | 0.090 | 0.179 | 0.13 | 80 | 1.51x | nothing (pure) |
| bq-mut-runs | 0.094 | 0.212 | 0.22 | 76 | 1.33x | mutable `Int` scratch |
| bq-expand-gm-mulback | 0.097 | 0.231 | 0.21 | 80 | 2.35x | nothing (pure) |
| bq-expand-b | 0.102 | 0.231 | 0.32 | 76 | 2.18x | nothing (pure) |
| bq-expand-qr-prim | 0.102 | 0.228 | 0.12 | 76 | 2.35x | nothing (pure) |
| mut-odo | 0.102 | 0.324 | 0.20 | 70 | 1.00x | new mutating `Vector` method |
| *bq-expand-aa-adjacent* | *0.105* | *0.239* | *0.25* | *74* | *2.35x* | *A/A control* |
| **bq-expand** | **0.105** | 0.238 | 0.25 | 74 | 2.35x | **nothing -- SHIPPED** |
| bq-expand-zf | 0.106 | 0.250 | 0.16 | 75 | 2.35x | nothing (pure) |
| *bq-expand-aa-distant* | *0.107* | *0.239* | *0.12* | *74* | *2.35x* | *A/A control* |
| build | 0.114 | 0.361 | 0.41 | 68 | 1.00x | new mutating `Vector` method |
| offtab | 0.115 | 0.296 | 0.93 | 70 | 2.00x | mutable `Int` scratch |
| offtab-scan-rem | 0.120 | 0.242 | 0.12 | 73 | 2.00x | nothing (pure) |
| bq-mut | 0.156 | 0.365 | 0.20 | 63 | 1.33x | mutable `Int` scratch |
| bq-gen | 0.341 | 2.173 | 0.40 | 51 | 1.33x | nothing (pure) |
| gen-quotrem | 0.911 | 3.686 | 0.57 | 42 | 1.00x | 1st attempt |
| gen-unsafe | 0.918 | 3.447 | 0.54 | 41 | 1.00x | -- |
| list (baseline) | 1.000 | 1.000 | 0.29 | 36 | 23.51x | -- |

`concat-runs` has no row, and neither do the other 23 arms the roster holds
and checks without timing: the reason is at each entry and the count is
[`--lint`'s](#the-reader-read-runpy). Ten rows here are first readings — the
eight arms written since Run 8 and the two A/A controls re-pointed onto
`bq-scan-rem-gm-mulback` — so a break in one of them is a reading rather than
a break.

**Three things in the table are the run's findings rather than its numbers.**
The roster cut cost the front of the pure tier nothing: `bq-scan-rem-gm-mulback`
(0.090) and `bq-odo-gm-mulback` (0.090) tie at its head (0.9934 paired, 17
wins of 24, sign p 0.064), and the second of those is a first reading — the
unconditional counterpart landing on the figure the `bq-odo-mulback` it
replaces held, with the preconditioned arm gone from the roster and the
Granlund-Montgomery output in its place. **The mutable ceiling widened**:
`mut-odo-vecdims` against the fastest pure arm is now **1.87×** (0.5360
paired, 23 wins of 24, sign p 3e-06), where Run 8 read 1.68× and -O1 1.80× —
the figure [the ruling](#the-mutable-ceiling-not-taken) turns on, and the
first time the gap has widened rather than closed. And **allocation
reproduced exactly**: every tier claim 7 named came back on its own level,
the mutable fills and `gen-quotrem` at 1.00x, the scan family and `bq-mut` at
1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x and
`list` 23.51x — the one column a roster change was not expected to touch, and
it did not.

**A fourth is new rather than moved.** The four `mut-odo-vecdims-add-*`
variants get their first reading, and only one of them is free:
`add-both-down` ties the arm it varies (1.0183 paired, 13 wins of 24, sign p
0.84, and the published columns' 0.049 against 0.048 is inside the floor),
while `add-in`, `add-both` and `add-out` cost 15% to 19%. What separates them
is in the arms' own entries, not measured here.


### What Run 10 compares against

**Run 10's regime and roster are open**, and the table below is what either
choice reads against. At `-fspec-constr` its yardstick is the Run 9 column,
whose basis it would share outright; at -O1 it is the Run 7 column, and the
two sets of claims differ in more than their numbers.

**Neither of the older columns is to be pruned**, however much each looks
like a leftover. The -O1 one is the only place Run 7's basis survives, so
deleting it leaves any future return to -O1 — the regime
`Data/Array/Internal.hs` actually compiles under — with no yardstick at all
and nothing to recover one from once the artifacts are gone; it goes when a
-O1 run replaces it, not before, and `--check-doc` fails if the column
disappears meanwhile. The Run 8 one is now load-bearing for a second reason:
its four bottom rows name arms **nothing times any more**, so with Run 8's
Results table replaced above and its JSON deleted, this is the only record
they have left. The rows nearest the decisions, in every regime that has
measured them, so no comparison needs another section:

| strategy | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|
| `mut-odo-vecdims` | **0.048** | 0.053 | 0.054 |
| `mut-flat-gm` | **0.080** | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.088** | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.090** | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.090** | 0.090 | 0.119 |
| `bq-expand` | **0.105** | 0.102 | 0.127 |
| `build` | **0.114** | 0.095 | -- |
| `offtab` | **0.115** | 0.146 | -- |
| `mut-flat` | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | 0.108 | 0.097 |

All three columns are published geomeans over the same 24 shapes. The first
two share a denominator as well — the baseline moved 0.2% between them — so
they may be subtracted and not merely ordered, which is what the third cannot
do at an 8% baseline shift. Read the Run 9 column against the Run 8 one for
*size*, then: nothing there is a strategy changing, the two runs differing in
membership alone, so every row of it prices layout. Read the -O1 column for
orderings only.

**Each stride class's yardstick is its own table below.** Run 8 re-ran every
class with the populations pinned and Run 9 again, so each class's paragraph
carries what its roster change moved and the table above it is what Run 10
reads against.

And because a geomean cannot say *where* it moved, the **fingerprint**
below is kept so a future disagreement can be localised rather than only
noticed. Its membership is a rule, not a habit: the shipped arm, the rows
the Results table bolds, and any arm an open question names — `mut-odo`
and `build` sit here on [the placement
question](#what-the-next-runs-have-to-decide), which this run has just made
the sharpest one on the list — and an arm leaves when its question closes,
the roster cut having taken two out that way. An arm nothing measures cannot
be the subject of a future disagreement to localise, and what is given up
when one goes is the per-shape half alone, its geomean staying in the
yardstick table above. `list`'s own net per call rides along, guarding the
baseline at every shape where the anchors guard three, and converting any
ratio beside it back to absolute time. Allocation stays medians-only on
purpose: deterministic per call, so a run that raises an allocation
question re-derives it within itself. `./read-run.py RUN.json
--fingerprint` emits both tables — paste them whole, transcribing nothing
by hand, since hand-carrying this table once left two of Run 6's cells
standing under Run 7's name, and the first emitted paste is what caught
them. The column heads shorten the arm names as the stretch table's do:
scan-rem-gm is `bq-scan-rem-gm-mulback` and vecdims
`mut-odo-vecdims`. And the [stretch table][pershape] is the same kind of
record for `bq-expand-b`, on the shapes chosen
to stress orderings — compare it the same way. It lost a `lemire-out` column
to this same rule on the same day, and says so.

| shape | `sInner` | `l` | `list`, net | bq-expand |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.35 µs | 0.153 |
| `cnn-L1-6x6-c1` | 3 | 324 | 6.5 µs | 0.208 |
| `stretch-rank12` | 2 | 4096 | 98.4 µs | 0.238 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 103 µs | 0.178 |
| `conv1d-24` | 3 | 5184 | 88.4 µs | 0.109 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 326 µs | 0.132 |
| `gather48-src-50` | 3 | 22500 | 382 µs | 0.103 |
| `stretch-rank10` | 3 | 59049 | 1.24 ms | 0.140 |
| `stretch-coprime-r7` | 13 | 60060 | 1.06 ms | 0.102 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.24 ms | 0.113 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.72 ms | 0.114 |
| `stretch-primes` | 89 | 250357 | 3.83 ms | 0.093 |
| `stretch-inner1` | 1 | 500000 | 11.4 ms | 0.086 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 26 ms | 0.063 |
| `vgg-14-c512-k3` | 3 | 903168 | 28.8 ms | 0.096 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 16.4 ms | 0.105 |
| `stretch-inner256` | 256 | 1750784 | 46.1 ms | 0.072 |
| `stretch-pow2stride` | 64 | 1769472 | 51.5 ms | 0.066 |
| `stretch-r5-8x432` | 8 | 1769472 | 50.2 ms | 0.054 |
| `stretch-square-1341` | 1341 | 1798281 | 25.4 ms | 0.128 |
| `stretch-bigstride` | 3 | 1800000 | 43.7 ms | 0.069 |
| `stretch-tab7MB` | 2 | 1800000 | 33.4 ms | 0.102 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 30 ms | 0.085 |
| `stretch-wide-2xM` | 2 | 1800000 | 33.5 ms | 0.093 |

| shape | scan-rem-gm | vecdims | mut-odo | build |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 0.141 | 0.082 | 0.193 | 0.206 |
| `cnn-L1-6x6-c1` | 0.136 | 0.093 | 0.221 | 0.242 |
| `stretch-rank12` | 0.140 | 0.101 | 0.324 | 0.361 |
| `cnn-L1-24x24-c1` | 0.103 | 0.072 | 0.195 | 0.216 |
| `conv1d-24` | 0.107 | 0.062 | 0.156 | 0.181 |
| `lenet-L1-28-c1-k5` | 0.098 | 0.051 | 0.135 | 0.142 |
| `gather48-src-50` | 0.106 | 0.057 | 0.143 | 0.146 |
| `stretch-rank10` | 0.099 | 0.064 | 0.166 | 0.186 |
| `stretch-coprime-r7` | 0.082 | 0.030 | 0.055 | 0.068 |
| `cifar-L2-16-c64-k3` | 0.088 | 0.052 | 0.136 | 0.166 |
| `cnn-L2-24x24-c32` | 0.087 | 0.052 | 0.139 | 0.154 |
| `stretch-primes` | 0.087 | 0.026 | 0.028 | 0.035 |
| `stretch-inner1` | 0.077 | 0.098 | 0.287 | 0.316 |
| `alexnet-L2-27-c48-k5` | 0.054 | 0.025 | 0.067 | 0.065 |
| `vgg-14-c512-k3` | 0.060 | 0.035 | 0.094 | 0.114 |
| `alexnet-L1-55-c3-k11` | 0.094 | 0.035 | 0.058 | 0.078 |
| `stretch-inner256` | 0.054 | 0.016 | 0.017 | 0.018 |
| `stretch-pow2stride` | 0.074 | 0.067 | 0.067 | 0.067 |
| `stretch-r5-8x432` | 0.051 | 0.019 | 0.040 | 0.044 |
| `stretch-square-1341` | 0.161 | 0.090 | 0.092 | 0.092 |
| `stretch-bigstride` | 0.071 | 0.037 | 0.096 | 0.111 |
| `stretch-tab7MB` | 0.107 | 0.068 | 0.165 | 0.204 |
| `stretch-tall-Mx2` | 0.075 | 0.020 | 0.021 | 0.026 |
| `stretch-wide-2xM` | 0.105 | 0.066 | 0.171 | 0.200 |

Two rows to read first, and the pair is derived rather than remembered:
`stretch-square-1341` and `stretch-pow2stride` are the only two shapes where
**both** arms tying at the head of the pure tier *lose* to `bq-expand`, so
treat a disagreement on either as the shape. They fail differently, which is
why both are named. On `stretch-square-1341` the mutable fills win it back
outright (`mut-odo-vecdims` 0.090 against `bq-expand`'s 0.128) while the pure
arms trail; on `stretch-pow2stride` the two families converge instead, four
of the five fingerprint arms landing inside a point of each other ([the
per-shape section][pershape]). Taking the tier's leaders one at a time gives
six shapes and three, which is why the sentence says both.
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.


### The claims Run 10 should test

**Run 9's verdicts on Run 8's nine claims first**, since a run reports
breaks rather than re-deriving the table. Claims 1, 2's first half, 4, 5's
second half, 6, 7 and 8's structural half held; three of the nine carry a
first reading rather than a re-test, the arms they name having been written
after Run 8. **Claim 7 held to the digit** — every allocation tier came back
on its own level, which is what a roster change with the regime pinned should
do and the one column that did it.

**Claim 9 inverted, both halves.** `bq-expand-b` / `bq-expand` reads
**0.9678** at 22 wins of 24, sign p 3.6e-05, where it tied at 0.996 on 8 of
24; `bq-expand-zf` / `bq-expand` reads **1.0028** at 8 of 24, sign p 0.15,
where it was 3.6% behind on 23 of 24. Read the two together and the caution
is the same one: both flips are about 3%, in a run whose *only* change was
membership and whose own span for that change is 9% faster to 19% slower.
**Nothing here says a strategy changed.** These three arms differ in their
seeding and their fusion, they sit at adjacent roster slots, and 3% is what
this run measures a slot to be worth.

**Claim 2's second half held in direction and collapsed in size.** `offtab` /
`bq-expand` reads **1.0969** at 7 wins of 24, sign p 0.064, against 1.440 at
four of 24 — the `l`-length table is still behind the `m`-length one, but
barely. Neither side is innocent: `offtab` gained 21% in absolute time and
`bq-expand` lost 3%, and `offtab` is one of the two arms [the placement
entry](#what-the-next-runs-have-to-decide) names as susceptible. So this is
the placement finding showing up inside a claim, not a table build getting
better.

**Claim 3 is a first reading and it pays.** `bq-expand-gm-mulback` /
`bq-expand` reads **0.9214** at 20 of 24, sign p 0.0015: a mul-back output is
worth 7.9% on the shipped build under this flag, where the claim expected a
few percent from what the Lemire form had shown. The arm is new, so this
sets the figure rather than moving one.

**Claim 4's tie survives the test that decides it, and drifts.** Against its
own build control the scan reads **0.9268** — 7.3% ahead where Run 8's
corresponding pair read 1.0004 — but at 16 wins of 24, sign p 0.15, on an
interval covering 1. So by the sign test, which is the test the claim rests
on and the only one immune to the baseline, the builders are still level; the
point estimate has moved and the evidence has not. Against `bq-expand` the
scan reads 0.8539 at 18 of 24, sign p 0.023, so the second half holds
outright. Quoting only that second figure is how this tie gets reported as a
win, which is why the claim carries both.

**Claim 5 exposed a bad figure rather than a break.** `bq-expand` / `bq-gen`
reads **0.3088** at 21 of 24 against the 0.600 the claim recorded — but Run
8's own published columns put the pair at 0.102 / 0.339 = 0.301, so the
recorded 0.600 disagreed with the table it was drawn from before this run
touched it. Treat the recorded figure as the error and the ordering as
unmoved; Run 8's artifact is gone, so which of *paired* and *published* the
0.600 was meant to be can no longer be recovered, and that is the whole
lesson. The claim's other half held: `bq-mut-runs` / `bq-expand` 0.8974 on 24
shapes of 24.

**Claim 6 held without its alarm firing.** `gen-quotrem` / `list` reads
0.9107 at 12 wins of 24, sign p exactly 1 — a tie by the only test immune to
the baseline, and this time the anchor the claim tells you to check first has
nothing to answer for: `list` moved 0.2%.

**Claim 8's structural half stands and its threshold is gone.** Every pure
arm still runs its output through the single in-order `vGenerate` over an
`m`-length table, and the arms that fall behind still lose on their table
build. But the gap the claim was stated across is now populated —
`bq-expand-zf` at 0.106 and `offtab-scan-rem` at 0.120 sit between the 0.105
tier and `bq-gen`'s 0.341 — so the claim keeps its structure and loses its
numeral for good.

Restated on this run's own published basis, for Run 10 to check; margins are
paired geomeans, past the floor unless marked, each claim carrying the
reading it rests on. **All of them are `-fspec-constr` claims**: a Run 10 at
-O1 tests Run 7's set instead, and the two sets differ in more than their
numbers. **And all of them are now read against a measured layout span**: a
membership change alone moved arms by up to 19%, so a margin under that is
evidence of a slot and not of a strategy unless something pins the layout.

**The list needed no re-aiming this time**, the roster it was rewritten onto
before Run 8 being the roster Run 9 ran: every claim below names an arm this
run timed, and each carries its own reading rather than the previous one's.
That the rewrite survived a full run is the evidence that keeping the
*question* and changing the *arm* was the right repair — the unconditional
counterparts were written so that dropping a precondition would not drop a
question with it, and none of them dropped one.

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` <
   `bq-odo-gm-mulback`, the whole ordering now read on unconditional arms:
   0.6017 (22 of 24), 0.9046 (**24 of 24**, sign p 1.2e-07) and 0.9782 (19 of
   24). The middle link is the sturdiest thing on this list — no shape
   dissents — and the first is the widest the ceiling's own gap has been.
   The ceiling's ordering survived the substitution the cut forced on it,
   which is what restating it was for.
2. `bq-expand` < `bq-mut` (0.6756, 20 of 24) while `offtab` is 1.0969
   *behind* `bq-expand` (7 of 24, sign p 0.064, marked): the `m`-length table
   beats both the mutable scratch that builds it and the `l`-length table
   that replaces it — the second of those now by a margin inside the layout
   span, so a Run 10 that inverts it has said nothing until the layout is
   pinned.
3. `bq-expand-gm-mulback` < `bq-expand` (0.9214, 20 of 24): a mul-back output
   pays 7.9% on the shipped build under this flag. Set by Run 9 rather than
   carried, `bq-expand-lemire-out` — the arm the question used to be asked
   through — being untimed for its `l < 2^32` precondition and having no
   unconditional form, Granlund-Montgomery offering no `out` analogue that
   yields quotient and remainder together.
4. `bq-scan-rem-gm-mulback` ties its own build control
   `bq-expand-gm-mulback` (0.9268, 16 of 24, sign p 0.15, interval covering
   1) while beating `bq-expand` (0.8539, 18 of 24, sign p 0.023). The two
   differ in `baseOffsetsScanRem` against `baseOffsetsExpand` and in nothing
   else, their output code being identical, so the first reading is about
   builders and the second about the shipped arm. Both readings are the
   claim; quoting only the second is how the tie gets reported as a win, and
   the point estimate drifting to 7.3% while the sign test stays at a tie is
   exactly the shape that invites it.
5. `bq-expand` < `bq-gen` (0.3088, 21 of 24): the build ordering, trimmed to
   its timed arms — `offsets-quot` and `bq-gen-lemire` were its two ends and
   are both untimed, so the run cannot re-read the gap widening or the
   ending. That refutation stands on Run 7 and Run 8, which is enough for an
   idea kept only so that it is not re-proposed. Among the builds only the
   mutable odometer still beats `bq-expand`, `bq-mut-runs` at 0.8974 on 24
   shapes of 24, the scan build being level rather than ahead (claim 4). So
   `bq-expand` is still the fastest build that needs neither a class
   extension nor explicit mutation.
6. `gen-quotrem` ties `list` (0.9107 on the geomean, 12 of 24, **sign p
   exactly 1**) — the first attempt's arithmetic stops being dearer than the
   list's allocation once the flag takes its own allocation to 1.00x against
   the list's 23.5x, which is the mixed picture this suite exists to have
   refuted, arriving by a route nobody proposed. The `cm-gather` < `list`
   half is untimed and stands as Run 8's. A break here would mean something
   changed in `list` or in GHC, not in a strategy — check the anchor before
   anything else, as Run 8 had to and Run 9 did not.
7. Allocation, median multiples of the result on this basis: the mutable
   fills 1.00x, `gen-quotrem` also 1.00x, `bq-mut` and the scan family
   1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x,
   `list` 23.5x. Every level reproduced across the roster change, which is
   what makes this the claim to check first in a run that moved membership:
   allocation is deterministic per call, so a level that *does* move is a
   code change and never a slot.
8. Every pure arm in the fast tier runs its output through the single
   in-order `vGenerate` over an `m`-length table, and a `bq-*` arm that falls
   behind loses on its table build and not on its output. Read the structure
   and not a threshold: the gap the claim used to be stated across is
   populated now, `bq-expand-zf` (0.106) and `offtab-scan-rem` (0.120) lying
   between the leading tier and `bq-gen` (0.341).
9. `bq-expand-b` < `bq-expand` (0.9678, 22 of 24) while `bq-expand-zf` ties
   it (1.0028, 8 of 24, sign p 0.15). Both are inversions of Run 8 and both
   are inside the layout span, so the geomeans are the weak half of this
   claim. The strong half is per shape: `bq-expand-b`'s two best cells are
   `stretch-inner1` (0.826) and `stretch-wide-2xM` (0.882), the rank-2 views
   with one huge outer dimension where seeding from `enumFromStepN` replaces
   the whole `concatMap` build — the same two Run 8 named, at twice the
   margin. A layout effect has no reason to pick those two shapes, so what
   this claim should be checked on is whether they stay its best, not whether
   the geomean stays under 1.

Each ordering is one `./read-run.py RUN.json --pair A B` line — paired
geomean, an interval and a sign test — so a run reports which claims held
rather than re-deriving them from the table.

**And for each stride class, the same three properties, now carrying Run 9's
verdicts**, the details beside each class's table:

1. **`bq-expand`'s `worst` stays under 1.** Held in every class — 0.186 at
   its highest, under `rev` — so the shipped fallback
   was never slower than the `list` it replaced, on any shape of any class the
   library can produce, in any regime or roster this page has run. This is the
   property the classes
   exist to test, no geomean can state it, and a break would have been the one
   result here to bear on `Data/Array/Internal.hs` directly.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-scan-rem-gm-mulback` the fastest pure arm, `bq-expand` behind both.
   The first clause broke in `reshape1` alone, where the flat fills own the
   top outright and have since -O1; `scaled`, which put `build` ahead in Run
   8, is repaired. Everywhere else it holds or ties — and the tie is a new
   thing needing a ruling rather than a reading, `mut-odo-vecdims-add-both-down`
   heading six of the nine populations by a thousandth or two. It is a
   variant of the arm the clause names, so nothing about the ceiling has
   changed hands; **the clause is to be read as the vecdims family's, not one
   arm's**, until a run separates them. The second clause held in six of the
   nine, the slot going to `bq-expand-gm-mulback` in `rev` and `bcast` and to
   `bq-odo-gm-mulback` in `reshape1` — both of them arms written since Run 8,
   so this is the cut's unconditional forms arriving at the front, not a
   reordering among old ones. The third clause holds in all nine if read as
   *behind whichever arms lead*, and breaks in `reshape1` alone if read on the
   two arms it names, `bq-expand` (0.095) sitting ahead of `mut-odo-vecdims`
   (0.101) there. Each break is read in its
   class's paragraph, and [the `sInner`
   ruling](#per-shape-where-the-geomean-hides-the-ordering) is what they bear
   on.
3. **The allocation tiers survive**: the mutable fills at the result vector,
   `bq-expand` at one to four times it, `list` at an order of magnitude more.
   Where a level moves it is the class's own `m` showing through, exactly as
   this property warned — `bq-expand` at 1.07x on `scaled` (`m` of 1 and
   2,000) and 4.22x on `reshape1` (`m = l`) — the ordering of tiers unbroken
   everywhere, and both of those levels the same to the digit as Run 8's.

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

**Run 9 (SpecConstr) records every class**, one process per
class, in [the sequence](#making-a-major-benchmark-run); every table below
is that run's, and every paragraph reads it against Run 8's measurement of
the same population at the same regime — the roster being the only thing
between them, so a class's movement here prices membership exactly as the
main set's does. This section
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
properties](#the-claims-run-10-should-test) is bolded, and the class's own
paragraph says what broke.

Then one block per class, in `classViews`' order — `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled` — each carrying the same
five things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause, and
   its shapes with their `l` and `sInner`, which is what makes the table under
   it readable without `Main.hs` open;
2. the table `./read-run.py $R-$c.json --markdown` emits, pasted whole and
   never edited — six columns, with the emphasis carried over from the main
   table so the shipped row is found at a glance, and `needs` left to that
   table as a property of a strategy rather than of a population;
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
| `rev` | 3 | 0.104 | 0.186 | **`bq-expand-gm-mulback`** 0.097 | `mut-odo-vecdims-add-both-down` 0.050 | 1.96% |
| `revsome` | 3 | 0.113 | 0.138 | `bq-scan-rem-gm-mulback` 0.107 | `mut-odo-vecdims-add-both-down` 0.051 | 1.44% |
| `bcast` | 3 | 0.079 | 0.103 | **`bq-expand-gm-mulback`** 0.072 | `mut-odo-vecdims-add-both-down` 0.026 | 0.34% |
| `bcastmid` | 2 | 0.121 | 0.144 | `bq-scan-rem-gm-mulback` 0.100 | `mut-odo-vecdims-add-both-down` 0.036 | 0.50% |
| `reshape1` | 2 | 0.095 | 0.102 | **`bq-odo-gm-mulback`** 0.046 | **`mut-flat-gm`** 0.029 | 0.22% |
| `slice` | 2 | 0.122 | 0.146 | `bq-scan-rem-gm-mulback` 0.107 | `mut-odo-vecdims-add-both-down` 0.044 | 0.15% |
| `window` | 2 | 0.130 | 0.136 | `bq-scan-rem-gm-mulback` 0.105 | `mut-odo-vecdims` 0.055 | 2.32% |
| `scaled` | 2 | 0.106 | 0.109 | `bq-scan-rem-gm-mulback` 0.096 | `mut-odo-vecdims-add-both-down` 0.028 | 0.68% |

**`rev` — every stride negated, offset at the top: the view `rev` on every
axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.03* | *136* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.050* | *0.076* | *0.08* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.050* | *0.076* | *0.04* | *138* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.050 | 0.079 | 0.06 | 138 | 1.01x |
| **mut-odo-vecdims** | **0.051** | 0.076 | 0.02 | 138 | 1.00x |
| mut-odo-vecdims-add-in | 0.059 | 0.090 | 0.04 | 137 | 1.00x |
| mut-odo-vecdims-add-both | 0.059 | 0.090 | 0.04 | 136 | 1.01x |
| mut-odo-vecdims-add-out | 0.059 | 0.090 | 0.06 | 136 | 1.01x |
| mut-odo | 0.094 | 0.208 | 0.04 | 126 | 1.00x |
| bq-expand-gm-mulback | 0.097 | 0.176 | 0.02 | 131 | 2.52x |
| mut-flat-gm | 0.097 | 0.138 | 0.08 | 134 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.102* | *0.107* | *0.03* | *130* | *1.34x* |
| *bq-expand-aa-distant* | *0.102* | *0.186* | *0.04* | *130* | *2.52x* |
| bq-mut-runs-gm-mulback | 0.102 | 0.159 | 0.05 | 132 | 1.34x |
| bq-odo-gm-mulback | 0.104 | 0.120 | 0.03 | 131 | 1.41x |
| **bq-scan-rem-gm-mulback** | **0.104** | 0.107 | 0.04 | 130 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.104* | *0.107* | *0.01* | *130* | *1.34x* |
| *bq-expand-aa-adjacent* | *0.104* | *0.185* | *0.04* | *130* | *2.52x* |
| bq-expand-qr-prim | 0.104 | 0.178 | 0.02 | 130 | 2.52x |
| bq-expand-b | 0.104 | 0.179 | 0.04 | 130 | 2.52x |
| **bq-expand** | **0.104** | 0.186 | 0.03 | 130 | 2.52x |
| bq-expand-zf | 0.106 | 0.192 | 0.03 | 130 | 2.52x |
| bq-mut-runs | 0.111 | 0.161 | 0.18 | 132 | 1.34x |
| build | 0.113 | 0.233 | 0.05 | 122 | 1.00x |
| offtab-scan-rem | 0.139 | 0.140 | 0.04 | 125 | 2.00x |
| offtab | 0.145 | 0.211 | 0.17 | 122 | 2.00x |
| bq-mut | 0.181 | 0.274 | 0.05 | 119 | 1.34x |
| bq-gen | 0.535 | 0.672 | 0.04 | 99 | 1.34x |
| list (baseline) | 1.000 | 1.000 | 0.03 | 89 | 23.45x |
| gen-unsafe | 1.360 | 1.679 | 0.23 | 83 | 1.00x |
| gen-quotrem | 1.366 | 1.626 | 0.21 | 82 | 1.00x |


Controls: the `mut-odo-vecdims` pairs carry this process, deviating 1.96% and
1.78% (distant and adjacent, worst cells ~5.8% on `rev-primes`), so read that
arm's lead from its twins at 0.050; both `bq-expand` pairs and both
`bq-scan-rem-gm-mulback` pairs stay within 0.3%. The `sum-only` halves agree
at 0.9997; the in-situ term reads 0.9668 and 0.9790 of `sum-only` as medians
(`mut-odo-vecdims` and `bq-expand` arms), the first the run's largest
departure and on the arm the A/A pairs already name — the same coincidence
Run 8 recorded here, so it is this class and not that run.

Provenance: elapsed 0h8m46s, peak 60 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 3.69 ms per call raw, 3.54 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.076/0.057/0.030,
`bq-scan-rem-gm-mulback` 0.107/0.105/0.095, `bq-expand` 0.186/0.103/0.102

What the class says: the shipped row is safe (`worst` 0.186) and the
fastest-pure slot goes to an arm that did not exist for Run 8 —
`bq-expand-gm-mulback` at 0.097, clear of the cluster at 0.104 where
`bq-scan-rem-gm-mulback`, `bq-expand-qr-prim`, `bq-expand-b` and `bq-expand`
itself all sit. So under negated strides the mul-back output is worth
7% where the main set gives it 8%, and it is the *builder* comparison that
collapses: every expansion arm within a thousandth of the scan. The other
reading here is the ceiling's, and it is the widest in any population —
`mut-odo` at 0.094 beats **every** pure arm, which it does nowhere else, and
the vecdims family sits at 0.050. What survives every regime and roster is
the collapse of the first attempt: `gen-quotrem` and `gen-unsafe` run
1.37x and 1.36x *slower than `list`*, worst cells above 1.6. Reversal is this
class's stress and the per-dimension-arithmetic arms bear it worst whatever
the flag.

**`revsome` — a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89),
`revsome-outer-g48` (`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l`
165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *91* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.07* | *115* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *117* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.051 | 0.064 | 0.07 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.053* | *0.062* | *0.06* | *98* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.053* | *0.062* | *0.03* | *98* | *1.00x* |
| **mut-odo-vecdims** | **0.053** | 0.062 | 0.06 | 97 | 1.00x |
| mut-odo-vecdims-add-both | 0.058 | 0.072 | 0.05 | 96 | 1.00x |
| mut-odo-vecdims-add-out | 0.059 | 0.072 | 0.04 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.059 | 0.069 | 0.04 | 96 | 1.00x |
| mut-flat-gm | 0.091 | 0.102 | 0.09 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.105 | 0.111 | 0.06 | 87 | 1.33x |
| bq-mut-runs | 0.105 | 0.121 | 0.09 | 86 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.107* | *0.108* | *0.05* | *88* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.107* | *0.109* | *0.02* | *88* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.107** | 0.108 | 0.04 | 88 | 1.33x |
| bq-odo-gm-mulback | 0.111 | 0.118 | 0.06 | 86 | 1.41x |
| bq-expand-gm-mulback | 0.111 | 0.128 | 0.05 | 84 | 2.52x |
| bq-expand-qr-prim | 0.112 | 0.131 | 0.05 | 84 | 2.52x |
| bq-expand-b | 0.112 | 0.132 | 0.05 | 84 | 2.52x |
| *bq-expand-aa-adjacent* | *0.113* | *0.138* | *0.05* | *84* | *2.52x* |
| **bq-expand** | **0.113** | 0.138 | 0.05 | 84 | 2.52x |
| *bq-expand-aa-distant* | *0.115* | *0.138* | *0.02* | *84* | *2.52x* |
| bq-expand-zf | 0.116 | 0.139 | 0.05 | 84 | 2.52x |
| build | 0.119 | 0.198 | 0.27 | 96 | 1.00x |
| mut-odo | 0.122 | 0.163 | 0.14 | 97 | 1.00x |
| offtab | 0.130 | 0.165 | 1.33 | 92 | 2.00x |
| offtab-scan-rem | 0.141 | 0.149 | 0.05 | 84 | 2.00x |
| bq-mut | 0.212 | 0.222 | 0.04 | 84 | 1.33x |
| bq-gen | 0.482 | 0.699 | 0.12 | 83 | 1.33x |
| list (baseline) | 1.000 | 1.000 | 0.15 | 49 | 23.45x |
| gen-unsafe | 1.322 | 1.489 | 0.35 | 45 | 1.00x |
| gen-quotrem | 1.379 | 1.481 | 0.25 | 44 | 1.00x |


Controls: the largest A/A deviation is 1.44% on the `mut-odo-vecdims`
adjacent pair (0.9856 paired), its distant pair reading 0.9860, both with
their worst cells on `revsome-inner-primes`; the other four sit within 0.2%,
and this is the one process of the nine where every control pair had a cell
capped, so `--selftest` skips the published-equals-paired identity here and
says so. The `sum-only` halves agree at 0.9998; the in-situ term reads 0.9848
and 0.9790 as medians (`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h8m45s, peak 59 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 3.47 ms per call raw, 3.32 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.033/0.058/0.062,
`bq-scan-rem-gm-mulback` 0.108/0.108/0.104, `bq-expand` 0.108/0.103/0.138

What the class says: mixed signs keep the top of the table in the main set's
order, and this is the class that reproduces it most exactly — the pure lead
is `bq-scan-rem-gm-mulback` (0.107) as claimed, with `bq-odo-gm-mulback` and
`bq-expand-gm-mulback` tied a step behind at 0.111 and `bq-expand` at 0.113.
Where `rev` scrambles the pure tier, reversing only some axes does not. The
first attempt runs 1.38x behind `list`, worst cells at 1.5, as it did in both
previous regimes.

**`bcast` — an innermost stride of 0, every run re-reading one element: a
broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.31* | *53* | *1.38x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *84* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *69* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.026 | 0.065 | 0.28 | 63 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.065* | *0.09* | *62* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.065 | 0.24 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.066* | *0.03* | *62* | *1.00x* |
| mut-odo-vecdims-add-both | 0.036 | 0.071 | 0.28 | 59 | 1.00x |
| mut-odo-vecdims-add-in | 0.037 | 0.071 | 0.07 | 59 | 1.00x |
| mut-odo-vecdims-add-out | 0.038 | 0.076 | 0.25 | 59 | 1.00x |
| mut-odo | 0.051 | 0.196 | 0.02 | 62 | 1.00x |
| build | 0.064 | 0.194 | 0.34 | 59 | 1.00x |
| mut-flat-gm | 0.064 | 0.083 | 0.33 | 48 | 1.13x |
| bq-mut-runs-gm-mulback | 0.068 | 0.089 | 0.35 | 48 | 1.13x |
| offtab | 0.071 | 0.177 | 0.60 | 55 | 2.00x |
| bq-expand-gm-mulback | 0.072 | 0.095 | 0.32 | 48 | 1.38x |
| bq-odo-gm-mulback | 0.075 | 0.095 | 0.35 | 48 | 1.14x |
| bq-mut-runs | 0.075 | 0.099 | 0.33 | 47 | 1.13x |
| bq-expand-b | 0.075 | 0.101 | 0.36 | 46 | 1.38x |
| bq-expand-qr-prim | 0.077 | 0.101 | 0.33 | 46 | 1.38x |
| bq-expand-zf | 0.078 | 0.102 | 0.36 | 46 | 1.38x |
| **bq-expand** | **0.079** | 0.103 | 0.34 | 46 | 1.38x |
| *bq-expand-aa-adjacent* | *0.079* | *0.103* | *0.34* | *47* | *1.38x* |
| *bq-expand-aa-distant* | *0.081* | *0.103* | *0.34* | *46* | *1.38x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.104* | *0.42* | *48* | *1.13x* |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.103 | 0.34 | 48 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.103* | *0.33* | *48* | *1.13x* |
| bq-mut | 0.115 | 0.196 | 0.31 | 47 | 1.13x |
| offtab-scan-rem | 0.125 | 0.138 | 0.78 | 44 | 2.00x |
| bq-gen | 0.212 | 0.277 | 0.36 | 46 | 1.13x |
| gen-quotrem | 0.445 | 1.166 | 0.30 | 24 | 1.00x |
| gen-unsafe | 0.452 | 1.224 | 0.81 | 24 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 1.02 | 16 | 20.64x |


Controls: the tightest set of any class — the largest A/A deviation is
0.34%, `bq-expand`'s distant pair at 1.0034, and the other five stay within
0.2%. The `sum-only` halves agree at 0.9984; the in-situ term reads 0.9793
and 0.9987 as medians, the second the closest to 1 in the whole run and the
only in-situ reading anywhere that a gate-3 sign test would call unbiased.

Provenance: elapsed 0h8m47s, peak 75 MiB in use, 26 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 49.2 ms per call raw, 48.2 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.035/0.010/0.065,
`bq-scan-rem-gm-mulback` 0.098/0.047/0.103, `bq-expand` 0.103/0.053/0.091

What the class says: every ratio sits far below the main set's, `list` paying
its cons-list walk on data the strategies read from cache, and the shipped
row is safe (`worst` 0.103). The fastest-pure slot goes to
`bq-expand-gm-mulback` (0.072) and `bq-scan-rem-gm-mulback` falls to 0.093 —
the largest inversion of that clause anywhere, and the one class where
`bq-expand` itself (0.079) is ahead of the arm claimed to lead the pure tier.
A stride-0 innermost run re-reads one element, so the table build is nearly
the whole cost here and the scan's cheaper output buys nothing. `build`
climbs to second overall (0.064), tied with `mut-flat-gm`. `bq-expand`'s
allocation tier sits at 1.38x on the class's small `m` (2,000-6,400 against
`l` in the hundreds of thousands), the `m`-tier effect the third property
predicts; and both first-attempt arms *beat* `list` (`gen-quotrem` 0.445,
`gen-unsafe` 0.452), the stride-0 read being the one place their arithmetic
is cheaper than the list's allocation. `list` itself is measured on 16
samples here, the thinnest in the run, so read this class's absolute anchor
before its ratios.

**`bcastmid` — the stretched axis in the middle instead: stride 0 on an
outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *90* | *2.10x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *112* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *112* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.036 | 0.066 | 0.06 | 98 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.037* | *0.065* | *0.03* | *98* | *1.00x* |
| **mut-odo-vecdims** | **0.037** | 0.065 | 0.03 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.037* | *0.065* | *0.04* | *98* | *1.00x* |
| mut-odo-vecdims-add-in | 0.049 | 0.073 | 0.13 | 96 | 1.00x |
| mut-odo-vecdims-add-both | 0.050 | 0.075 | 0.05 | 95 | 1.00x |
| mut-odo-vecdims-add-out | 0.050 | 0.076 | 0.07 | 95 | 1.00x |
| mut-odo | 0.062 | 0.171 | 0.06 | 90 | 1.00x |
| build | 0.085 | 0.208 | 0.31 | 88 | 1.00x |
| offtab | 0.094 | 0.188 | 1.10 | 86 | 2.00x |
| mut-flat-gm | 0.096 | 0.107 | 0.23 | 87 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.109* | *0.02* | *87* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.109 | 0.05 | 87 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.110* | *0.05* | *87* | *1.17x* |
| bq-mut-runs-gm-mulback | 0.102 | 0.117 | 0.21 | 86 | 1.17x |
| bq-odo-gm-mulback | 0.108 | 0.123 | 0.12 | 86 | 1.78x |
| bq-mut-runs | 0.111 | 0.121 | 0.09 | 85 | 1.17x |
| bq-expand-gm-mulback | 0.111 | 0.135 | 0.05 | 85 | 2.10x |
| bq-expand-qr-prim | 0.118 | 0.138 | 0.06 | 84 | 2.10x |
| bq-expand-b | 0.119 | 0.139 | 0.22 | 84 | 2.10x |
| **bq-expand** | **0.121** | 0.144 | 0.05 | 84 | 2.10x |
| *bq-expand-aa-distant* | *0.121* | *0.144* | *0.04* | *84* | *2.10x* |
| *bq-expand-aa-adjacent* | *0.122* | *0.145* | *0.04* | *84* | *2.10x* |
| bq-expand-zf | 0.122 | 0.146 | 0.12 | 84 | 2.10x |
| offtab-scan-rem | 0.135 | 0.139 | 0.06 | 82 | 2.00x |
| bq-mut | 0.159 | 0.242 | 0.07 | 80 | 1.17x |
| bq-gen | 0.282 | 0.706 | 0.11 | 70 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.22 | 48 | 21.99x |
| gen-unsafe | 1.311 | 1.535 | 0.68 | 43 | 1.00x |
| gen-quotrem | 1.319 | 1.502 | 0.40 | 43 | 1.00x |


Controls: the `mut-odo-vecdims` pairs straddle their arm — 0.9950 distant and
1.0041 adjacent, worst cells ~1% on `bcastmid-primes` — so this class's floor
is 0.50% and still sits at that arm's slot, as it did at -O1 and in Run 8,
the one disturbance this page has now seen three times in the same class,
though at a sixth of its previous size. The other four pairs stay within 0.4%
and the `sum-only` halves agree at 1.0001, the tightest of the run. The
in-situ term is this class's one caution: 0.9767 and **0.9597** as medians,
the second the furthest from 1 anywhere in Run 9 and on `bq-expand` rather
than on the arm the A/A pairs name.

Provenance: elapsed 0h5m50s, peak 35 MiB in use, 12 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the bcastmid class. Anchor:
`bcastmid-primes`, `list` at 3.64 ms per call raw, 3.49 ms net.

What the class says: the main ordering holds at the top and in the pure tier
both — `mut-odo-vecdims` (0.037) leads, `bq-scan-rem-gm-mulback` (0.100) is
the fastest pure arm, `bq-expand` (0.121) sits behind both — which is all
three clauses of the second property in one population, and only `revsome`
does the same. Behind the vecdims family come `mut-odo` (0.062), `build`
(0.085) and `offtab` (0.094) in that order, the two placement-susceptible
arms adjacent and both ahead of every pure arm.

**`reshape1` — the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *79* | *4.22x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *104* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *104* | *0.00x* |
| mut-flat-gm | 0.029 | 0.030 | 0.11 | 90 | 2.00x |
| bq-mut-runs-gm-mulback | 0.035 | 0.038 | 0.07 | 88 | 2.00x |
| bq-odo-gm-mulback | 0.046 | 0.048 | 0.09 | 84 | 2.15x |
| bq-expand-gm-mulback | 0.047 | 0.055 | 0.11 | 84 | 4.22x |
| bq-mut-runs | 0.078 | 0.079 | 0.09 | 78 | 2.00x |
| offtab-scan-rem | 0.079 | 0.080 | 0.11 | 77 | 2.00x |
| **bq-scan-rem-gm-mulback** | **0.079** | 0.080 | 0.10 | 77 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.079* | *0.080* | *0.11* | *77* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.079* | *0.080* | *0.04* | *77* | *2.00x* |
| bq-expand-b | 0.083 | 0.094 | 0.12 | 76 | 3.72x |
| bq-expand-qr-prim | 0.087 | 0.094 | 0.14 | 76 | 4.22x |
| bq-expand-zf | 0.088 | 0.097 | 0.28 | 76 | 4.22x |
| **bq-expand** | **0.095** | 0.102 | 0.12 | 74 | 4.22x |
| *bq-expand-aa-adjacent* | *0.095* | *0.102* | *0.12* | *74* | *4.22x* |
| *bq-expand-aa-distant* | *0.096* | *0.102* | *0.05* | *74* | *4.22x* |
| *mut-odo-vecdims-aa* | *0.101* | *0.103* | *0.05* | *74* | *1.00x* |
| **mut-odo-vecdims** | **0.101** | 0.103 | 0.05 | 74 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.101* | *0.103* | *0.02* | *74* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.101 | 0.103 | 0.08 | 74 | 1.00x |
| mut-odo-vecdims-add-in | 0.109 | 0.114 | 0.15 | 72 | 1.00x |
| mut-odo-vecdims-add-both | 0.111 | 0.112 | 0.08 | 72 | 1.00x |
| mut-odo-vecdims-add-out | 0.111 | 0.113 | 0.07 | 72 | 1.00x |
| offtab | 0.267 | 0.276 | 1.42 | 58 | 2.00x |
| mut-odo | 0.271 | 0.272 | 1.05 | 57 | 1.00x |
| build | 0.305 | 0.323 | 0.28 | 56 | 1.00x |
| bq-mut | 0.312 | 0.319 | 0.48 | 54 | 2.00x |
| gen-quotrem | 0.640 | 0.912 | 0.90 | 42 | 1.00x |
| gen-unsafe | 0.644 | 0.941 | 1.05 | 42 | 1.00x |
| bq-gen | 0.689 | 1.143 | 0.17 | 41 | 2.00x |
| list (baseline) | 1.000 | 1.000 | 0.28 | 36 | 32.18x |


Controls: **the tightest process of the run** — every A/A pair within 0.22%,
the largest being `bq-expand` distant at 1.0022, and no cell capped anywhere.
The `sum-only` halves agree at 1.0002; the in-situ term reads 0.9761 and
0.9762 as medians, the two arms agreeing with each other to a ten-thousandth,
which no other population manages. Run 7's disturbance at this class's
`mut-odo-vecdims` slot, which cost it a 3.5% floor and a 33% in-situ scatter,
is absent for the second run running.

Provenance: elapsed 0h5m50s, peak 42 MiB in use, 15 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 11.3 ms per call raw, 11 ms net.

What the class says: the top still inverts completely and still by
construction — with `sInner` 1 every run is one element, so the flat fills
win outright (`mut-flat-gm` 0.029, `bq-mut-runs-gm-mulback` 0.035) while the
odometer fills pay a full odometer step per element (`mut-odo` 0.271, `build`
0.305) and `mut-odo-vecdims` lands mid-table (0.101). This is [the `sInner`
ruling][pershape]'s extreme case, mechanism rather than scatter, and neither
the regime nor the roster touches it. It is also the one class breaking two
clauses of the second property at once: the fastest pure arm is
`bq-odo-gm-mulback` (0.046) rather than the scan, and `bq-expand` (0.095) is
*ahead* of `mut-odo-vecdims` — the only population anywhere where the shipped
arm beats the ceiling's own arm. `m = l` here, which is what puts
`bq-expand`'s allocation at 4.22x, its highest in any class and the level the
third property names. That level carries a nursery consequence with it:
`bq-expand` holds 6–8 MB of excess allocation on both shapes and
`mut-odo-vecdims` none at all, against `list`'s 43 and 118 MB, so the default
4 MB area penalises the baseline hardest and the ceiling's arm not at all. A
larger nursery would raise `mut-odo-vecdims`'s ratio more than `bq-expand`'s,
so the inversion above is a floor rather than an artifact — it would widen
([the predictor](#what-the-next-runs-have-to-decide)).

**`slice` — a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes`
(`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *89* | *2.16x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *110* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *112* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *112* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.044 | 0.067 | 0.04 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.044** | 0.066 | 0.04 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.044* | *0.066* | *0.04* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.044* | *0.066* | *0.02* | *96* | *1.00x* |
| mut-odo-vecdims-add-out | 0.052 | 0.076 | 0.04 | 94 | 1.00x |
| mut-odo-vecdims-add-both | 0.052 | 0.076 | 0.05 | 94 | 1.00x |
| mut-odo-vecdims-add-in | 0.054 | 0.083 | 0.03 | 94 | 1.00x |
| mut-odo | 0.074 | 0.171 | 0.02 | 89 | 1.00x |
| build | 0.087 | 0.193 | 0.06 | 88 | 1.00x |
| mut-flat-gm | 0.098 | 0.105 | 0.08 | 87 | 1.17x |
| offtab | 0.099 | 0.187 | 0.15 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.107* | *0.110* | *0.04* | *86* | *1.17x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.107* | *0.110* | *0.02* | *86* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.107** | 0.110 | 0.09 | 86 | 1.17x |
| bq-mut-runs | 0.111 | 0.121 | 0.05 | 85 | 1.17x |
| bq-mut-runs-gm-mulback | 0.112 | 0.122 | 0.05 | 85 | 1.17x |
| bq-odo-gm-mulback | 0.118 | 0.127 | 0.10 | 84 | 1.79x |
| bq-expand-qr-prim | 0.119 | 0.139 | 0.05 | 84 | 2.16x |
| bq-expand-gm-mulback | 0.119 | 0.137 | 0.14 | 84 | 2.16x |
| bq-expand-b | 0.120 | 0.140 | 0.14 | 84 | 2.16x |
| **bq-expand** | **0.122** | 0.146 | 0.06 | 84 | 2.16x |
| *bq-expand-aa-adjacent* | *0.122* | *0.146* | *0.06* | *84* | *2.16x* |
| *bq-expand-aa-distant* | *0.122* | *0.146* | *0.03* | *84* | *2.16x* |
| bq-expand-zf | 0.124 | 0.147 | 0.05 | 84 | 2.16x |
| offtab-scan-rem | 0.143 | 0.144 | 0.06 | 81 | 2.00x |
| bq-mut | 0.156 | 0.230 | 0.09 | 80 | 1.17x |
| bq-gen | 0.294 | 0.754 | 0.74 | 68 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.23 | 48 | 21.99x |
| gen-quotrem | 1.299 | 1.534 | 0.62 | 44 | 1.00x |
| gen-unsafe | 1.321 | 1.560 | 0.51 | 43 | 1.00x |


Controls: every A/A pair within 0.15%, the smallest spread of any population
here and the run's lowest floor; the `sum-only` halves agree at 1.0001. The
in-situ term reads 0.9815 and 0.9756 as medians (`mut-odo-vecdims` and
`bq-expand` arms). This class has now been the quietest or near it in three
successive runs, which is a property of the population rather than of a run.

Provenance: elapsed 0h5m50s, peak 47 MiB in use, 17 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the slice class. Anchor:
`slice-primes`, `list` at 3.64 ms per call raw, 3.49 ms net.

What the class says: a non-zero offset changes nothing, in any regime or
roster — all three clauses of the second property hold, the main ordering
reproduces whole, and that is the result. `mut-odo` (0.074) ahead of `build`
(0.087) reverses Run 8's order here, and it is the main set's reversal rather
than this class's, the two arms being the identical-worker pair the floor
section prices.

**`window` — overlapping im2col patches: the workload this page opens by
naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.03* | *106* | *2.48x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *123* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *132* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *132* | *0.00x* |
| *mut-odo-vecdims-aa* | *0.055* | *0.061* | *0.05* | *113* | *1.00x* |
| **mut-odo-vecdims** | **0.055** | 0.061 | 0.05 | 113 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.055 | 0.062 | 0.12 | 113 | 1.01x |
| *mut-odo-vecdims-aa-distant* | *0.056* | *0.061* | *0.27* | *113* | *1.00x* |
| mut-odo-vecdims-add-both | 0.063 | 0.071 | 0.04 | 112 | 1.01x |
| mut-odo-vecdims-add-in | 0.063 | 0.068 | 0.05 | 111 | 1.00x |
| mut-odo-vecdims-add-out | 0.064 | 0.071 | 0.05 | 112 | 1.01x |
| mut-flat-gm | 0.095 | 0.097 | 0.14 | 106 | 1.27x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.105* | *0.107* | *0.03* | *104* | *1.27x* |
| **bq-scan-rem-gm-mulback** | **0.105** | 0.107 | 0.08 | 104 | 1.27x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.105* | *0.108* | *0.07* | *104* | *1.27x* |
| bq-mut-runs-gm-mulback | 0.107 | 0.110 | 0.07 | 104 | 1.27x |
| bq-odo-gm-mulback | 0.114 | 0.117 | 0.06 | 104 | 2.10x |
| bq-mut-runs | 0.115 | 0.115 | 0.12 | 103 | 1.27x |
| bq-expand-gm-mulback | 0.119 | 0.126 | 0.07 | 102 | 2.48x |
| bq-expand-qr-prim | 0.125 | 0.130 | 0.02 | 102 | 2.48x |
| bq-expand-b | 0.126 | 0.130 | 0.13 | 102 | 2.48x |
| *bq-expand-aa-distant* | *0.130* | *0.136* | *0.11* | *101* | *2.48x* |
| *bq-expand-aa-adjacent* | *0.130* | *0.135* | *0.10* | *102* | *2.48x* |
| **bq-expand** | **0.130** | 0.136 | 0.05 | 101 | 2.48x |
| bq-expand-zf | 0.131 | 0.137 | 0.11 | 101 | 2.48x |
| offtab | 0.132 | 0.148 | 0.26 | 101 | 2.00x |
| offtab-scan-rem | 0.135 | 0.139 | 0.07 | 100 | 2.00x |
| mut-odo | 0.143 | 0.162 | 0.96 | 100 | 1.00x |
| build | 0.154 | 0.182 | 1.34 | 98 | 1.00x |
| bq-mut | 0.201 | 0.208 | 0.05 | 94 | 1.27x |
| bq-gen | 0.487 | 0.542 | 0.21 | 79 | 1.27x |
| list (baseline) | 1.000 | 1.000 | 0.16 | 66 | 23.46x |
| gen-unsafe | 1.168 | 1.470 | 0.72 | 64 | 1.00x |
| gen-quotrem | 1.282 | 1.616 | 3.50 | 61 | 1.00x |


Controls: this class carries the run's widest class floor, 2.32%, at the
`mut-odo-vecdims` distant pair (1.0232, worst cell 3.81% on
`window-28x28-k5`) — the third successive run to put this class's floor on
one cell of that small shape, and the second to put it at that arm's slot.
Every other pair sits within 0.6%. The `sum-only` halves agree at 1.0002; the
in-situ term reads 0.9779 and 0.9673 as medians, the second the run's
furthest from 1 after `bcastmid`'s.

Provenance: elapsed 0h5m51s, peak 41 MiB in use, 15 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 8.41 ms per call raw, 8.15 ms net.

What the class says: the ordering holds whole — all three clauses — and the
figure this class exists for is the shipped row against the main set's, 0.130
here against 0.105 there. The overlap the main set drops still *lifts* every
ratio rather than lowering it, by about the same margin as in both previous
runs, so the main set flatters the fallback's standing against `list` in
every regime and roster tried, and the pessimism this page once recorded was
about absolute cost only. It is also where claim 2's collapsed second half is
narrowest: `offtab` (0.132) trails `bq-expand` (0.130) by less than the main
set's own floor, so on this population the two are indistinguishable.

**`scaled` — superincreasing strides, none of them 1: a hand-built
dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30),
`scaled-rank1-m1` (`l` 300000, `sInner` 300000 — rank 1, so `m` is 1 and
the whole view is one strided run).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *103* | *1.07x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *130* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.028 | 0.030 | 0.06 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.030* | *0.04* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.030 | 0.05 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.030* | *0.07* | *111* | *1.00x* |
| mut-odo | 0.031 | 0.033 | 0.29 | 110 | 1.00x |
| mut-odo-vecdims-add-in | 0.034 | 0.036 | 0.07 | 110 | 1.00x |
| mut-odo-vecdims-add-out | 0.034 | 0.037 | 0.06 | 110 | 1.00x |
| mut-odo-vecdims-add-both | 0.034 | 0.037 | 0.05 | 110 | 1.00x |
| build | 0.040 | 0.050 | 0.08 | 108 | 1.00x |
| offtab | 0.058 | 0.059 | 0.08 | 104 | 2.00x |
| mut-flat-gm | 0.086 | 0.087 | 0.09 | 100 | 1.02x |
| bq-mut-runs-gm-mulback | 0.094 | 0.096 | 0.12 | 98 | 1.02x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.097* | *0.03* | *98* | *1.02x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.096* | *0.098* | *0.06* | *98* | *1.02x* |
| **bq-scan-rem-gm-mulback** | **0.096** | 0.098 | 0.04 | 98 | 1.02x |
| bq-expand-gm-mulback | 0.096 | 0.098 | 0.04 | 98 | 1.07x |
| bq-odo-gm-mulback | 0.100 | 0.102 | 0.04 | 98 | 1.02x |
| bq-mut-runs | 0.104 | 0.106 | 0.04 | 97 | 1.02x |
| bq-expand-qr-prim | 0.105 | 0.108 | 0.05 | 97 | 1.07x |
| **bq-expand** | **0.106** | 0.109 | 0.05 | 96 | 1.07x |
| *bq-expand-aa-distant* | *0.106* | *0.108* | *0.07* | *96* | *1.07x* |
| bq-expand-b | 0.106 | 0.109 | 0.04 | 96 | 1.07x |
| *bq-expand-aa-adjacent* | *0.107* | *0.110* | *0.27* | *96* | *1.07x* |
| bq-expand-zf | 0.107 | 0.109 | 0.12 | 96 | 1.07x |
| bq-mut | 0.111 | 0.120 | 0.04 | 96 | 1.02x |
| bq-gen | 0.123 | 0.148 | 0.06 | 94 | 1.02x |
| offtab-scan-rem | 0.139 | 0.140 | 0.06 | 92 | 2.00x |
| gen-quotrem | 0.702 | 1.345 | 0.12 | 65 | 1.00x |
| gen-unsafe | 0.702 | 1.254 | 1.46 | 65 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.19 | 58 | 19.22x |


Controls: the floor is 0.68%, at `bq-scan-rem-gm-mulback`'s distant pair
(0.9932, worst cell 1.13% on `scaled-super-r3`) rather than at the
`mut-odo-vecdims` slot that carried it in both previous runs; that arm's own
pairs are now 0.9975 and 1.0044, so the disturbance this class showed twice
has gone. The `sum-only` halves agree at 1.0026, the loosest of the run and
still well inside any floor; the in-situ term reads 0.9824 and 0.9774 as
medians.

Provenance: elapsed 0h5m51s, peak 59 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.3 ms per call raw, 4.12 ms net.

What the class says: **Run 8's break here is repaired** — `build` (0.040) led
this class outright then and is now back behind the vecdims family (0.028)
and `mut-odo` (0.031), so the second property's first clause holds where it
did not. All three clauses do. The allocation tiers collapse toward 1
(`bq-expand` 1.07x, the scan rows 1.02x), the `m`-tier effect at its floor —
`m` of 1 and 2,000 makes every table free — which is why the spread from the
fastest arm to `bq-gen` is the narrowest of any population, 0.028 to 0.123.
`gen-quotrem` and `gen-unsafe` beat `list` at 0.702 while their `worst` cells
still cross 1 (1.345 and 1.254), the only class besides `bcast` where the
first attempt wins at all.

### Provenance

The run's name, regime, scale and source commit are at the head of this
chapter; what follows is what they have to be read against. The commit is
recorded there because a run whose artifact is deleted and whose source is
unrecorded cannot be repeated even in principle.

Run 9 is the cleanest comparison this page has drawn, Run 8 having been the
previous holder of that title on a different axis. Everything but the
**roster** is pinned: the same shapes, the same class lists, the same
machine, the same GHC, the same `cabal.project.freeze`, the same compiler
flag, and a tree clean at `96378d2`. Where Run 8 against Run 7 pinned
membership and moved the regime — and paid for it in the denominator, the
flag having moved `list` by 8% — Run 9 against Run 8 does the reverse and
pays nothing: `list` moved 0.2%, so the two runs' ratio columns may be
subtracted directly. That is what makes this run's every movement a
measurement of layout, and it is why the span at the head of this chapter is
the chapter's main result.

The desktop named at the head of this chapter is the same machine whose
`idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and
should say which machine here.

**The shapes have not moved**, for the third run running: Run 9 measured
exactly the shapes `Main.hs` holds today, in every population. The roster is
the part that moved, between Run 8 and this run and not since — so the delta
below is empty for the first time, and the next run inherits both pinned.

**The delta, so the population is recoverable.** What follows is the *only*
form in which a shape set or roster is recorded here: its difference from
whatever `Main.hs` holds now. A snapshot would need rewriting at every change
and would be a second copy of a list that already exists; a delta costs what
actually moved and shrinks to nothing when the two agree. A roster delta has
two halves now that membership no longer settles what ran: which arms the
roster held, and which of them it timed. **And a third: the ORDER they ran
in.** Order is not membership, it *can* move code layout, and Run 9 measured
layout at up to 19% on an arm -- so a delta stated in membership alone can
read empty while the run is not repeatable. Whether a given reorder moves
anything is now a thing to measure rather than assume, both answers having
turned up in one afternoon: `sum-only-early`'s slot-5-to-2 move left all
eight loops this page tracks byte-identical, while lifting it one further
place, above `list`, shifts every worker by ~40 KB and rerolls every
alignment. So record the order, and read the binary before deciding what the
record costs.

- Run 9 measured today's shapes, today's class lists and today's roster
  membership, timing today's 24 of it, winsorized per the estimator under
  `time` — but **in a different roster ORDER**: `sum-only-early` has since
  moved from slot 5 to slot 2, ahead of the three distant A/A twins ([the
  floor section][floor]). Membership is unchanged, so a delta stated in
  membership alone would read empty and be wrong, which is a gap in this
  form worth naming. What that move costs is now measured rather than
  feared: a binary rebuilt from Run 9's own commit `96378d2` puts all eight
  tracked loops at the same offsets as the moved roster does, to the byte,
  so the two orders differ in heap state and not in layout — which is what
  lets [the floor section][floor]'s loop table hold Run 9's ratios against
  offsets read off a later binary at all. Run 10 forfeits the repetition for
  a different reason and deliberately: it lifts `sum-only-early` one place
  further, above `list`, and that swap *does* relocate everything.
- Run 8 measured today's shapes and today's class lists, on today's roster
  **minus the eight arms written since** (`bq-expand-gm-mulback`,
  `bq-odo-gm-mulback`, `mut-flat-gm`, `offtab-scan-rem` and the four
  `mut-odo-vecdims-add-*`), **timing all of it but `concat-runs`** where today
  leaves 24 untimed, winsorized likewise. Run 7's delta is Run 8's plus the
  regime, which is what keeps the last two columns in [What Run 10 compares
  against](#what-run-10-compares-against) a controlled pair and the first two
  a different controlled pair.
- Run 6, still quoted here for the estimator ruling under `time`, for the
  `alloc` column's shape-dependence and for the correction's amplification
  arithmetic under [the floor][floor], measured today's
  main-set shapes **minus `stretch-pow2stride` and `stretch-inner256`, plus
  eleven since dropped**
  (`cnn-L1-12x12-c1`, `cnn-L2-12x12-c16`, `cnn-slice-c64`,
  `lenet-L2-14-c6-k5`,
  `mnist-28-c1-k3`, `cifar-L1-32-c3-k3`, `cifar-L3-8-c128-k3`,
  `cifar-32-c3-k5`, `vgg-14-c256-k3`, `deep-7-c512-k3`, `slice-c512`), on
  today's roster **minus thirteen arms** (the three crossed A/A twins, the
  two `-nosum` controls and the eight Run 8 also lacked), **timing all of it**,
  trimmed rather than winsorized, on the Storable
  scratch the conversion since replaced, and with no stride class in
  existence. That is the whole chain between its figures and this run's.

**The anchor, so a moved baseline is visible** — and this is the run where it
earned its keep by *not* moving. Every published figure is a
ratio to `list`, so a change in `list` itself — a new compiler, a new machine,
a changed `toListT`, or a compiler flag — rescales the whole table while
leaving every ratio intact and undetectable. These three absolute per-call
figures are the guard, and against Run 8's all three are within 1%, which is
what licenses reading this run's column against its predecessor's at all:

| shape | `l` | `list`, per call | net of the forcing pass |
|---|---:|---:|---:|
| `cnn-slice-c32` | 288 | 5.53 µs | 5.35 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.33 ms | 3.24 ms |
| `stretch-wide-2xM` | 1800000 | 34.6 ms | 33.5 ms |

Each stride class carries an anchor of its own, beside its table, and this
run they scatter rather than moving together: −4.5% (`bcastmid`) to +0.7%
(`scaled`), with `rev` and `reshape1` unmoved to three digits. A baseline
that changed for one mechanism only — under negative strides, say, or a
stride-0 read — is exactly the change a population of ratios cannot show, and
scatter of this size across eight independent baselines is what the guard
looks like when nothing has.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.592–0.607 ns per element across the whole set, so a raw
slope is the published one plus about `0.60e-9 * l`, with `l`
from `Main.hs`. That recovers any uncorrected figure to within the term's own
3% spread — enough to hold a corrected run against any number
measured before the correction existed. The term itself is within 1% of Run
8's and of Run 7's, so neither the flag nor the roster touches the forcing
pass, which is the control saying three runs' corrections are one correction.

**What the next run replaces.** Run 9's numbers reach past the Results table,
so this is the list to walk when Run 10's land. It names *sections*, not
figures: a list of figures is a second copy of them, and enumerating it was
how the previous two versions of this list went stale — one missing six
sections, its predecessor leaking past it. What now guarantees completeness is
mechanical instead. Every section below is reached by an anchor, and the
coverage check is: no section carrying a figure outside a table may be absent
from these links. Run that check, and repeat the two sweeps it cannot replace
— grep this file for figure-shaped numerals outside the tables, and grep it
for `Run 9` — before trusting the list.

- [the head of this chapter](#about-the-last-run-run-9), which carries the run's
  name, regime, scale and source commit, and now the layout span a membership
  change alone is worth;
- [the Results table](#results), which `--markdown` emits whole, and the
  findings under it;
- [What Run 10 compares against](#what-run-10-compares-against) — the yardstick
  geomeans in every regime measured and the two-column per-shape fingerprint,
  all of which a run replaces wholesale, and which are the only per-shape record
  kept once the JSON is deleted;
- [The claims Run 10 should test](#the-claims-run-10-should-test), where a run
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

**Run 9 answered its one, and the answer is the prediction.** *What moved
`mut-odo-vecdims` by the remaining ~13%?* The entry below asked for a run
differing from its predecessor in membership alone and predicted, before the
run, that a move of that size would be consistent with **layout alone**. Run
9 is that run and the prediction holds: the arm moved 9.0% in absolute time
against an unmoved baseline, which is inside the 18% a rebuild was already
known to be worth, and it did not move alone — `mut-odo` moved 9.0% the same
way and `build` moved 19.2% the other, the two of them compiling to one
worker. A membership change that improves one arm 9% and worsens its own
code-twin 19% has not told you anything about membership. So the question
closes as **unanswerable by this design**, not as answered: roster and layout
move together and no run that changes the roster can separate them. What
would separate them is the pad probe done properly — vary a *susceptible*
arm's address deliberately, with membership fixed — which is the entry below
and now the only route left to this question.

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

**And it raised a larger one in the same breath, which was then answered the
same day.** *What warms the expansion family?* On `vgg-14-c512-k3`,
`bq-expand` and three arms beside it run 35–40% slower in a small process
than at their published roster slots, reproducibly, while the scan and
mutable families do not move at all — the largest effect this page has
measured that is not a strategy, and it lands on the **shipped** arm. A dozen
probes settled it: not GC time (5.8% of the cold process), but the **default
4 MB nursery** against an arm allocating 13.2 MB per call beyond its result,
warmed by exactly one predecessor — `sum-only-early`, whose one-off
`l`-sized setup allocation grows the block pool and leaves it grown. A
nine-point `-A` sweep shows a larger nursery rescuing the *cold* arm, and
shows `-A1G`'s cliff to be a collision with the `-M2G` cap rather than the
nursery. The account is [in the floor
section][floor], and it carried **a roster fix, since applied**:
`sum-only-early` has moved from slot 5 to slot 2, ahead of the three distant
A/A twins, which were being calibrated against a colder heap than everything
they calibrate. On the moved roster the 41% cell reads 0.24%.

  **The acute symptom is gone**, by the roster move rather than by any flag.
  What the flag question became instead was settled on a quiet machine the
  same day, and the answer is bigger than the question: a larger nursery
  helps a warm arm by about 10%, the cost it removes is *kernel* time, and
  **`list` is the arm it helps most of all** — 1.79× on `vgg-14-c512-k3`,
  which takes `bq-expand`/`list` there from 0.098 to 0.157 ([the floor
  section][floor]).

  **So the decision is no, and for a better reason than "it buys nothing".**
  The default 4 MB area is what a GHC program gets unless it says otherwise,
  so the published column answers *what does a caller see today*; `-A32m`
  answers a question nobody asked, at the price of re-basing every figure the
  page has published and forfeiting the clean repetition Run 10 is positioned
  to give. Keep the default. What changes is not the setting but the
  **caveat**: the headline ratios are partly a statement about the allocation
  area, they are not a nursery-independent property of the algorithms, and
  the effect is confined to shapes where an arm's excess outruns 4 MB — which
  the `cifar` control shows the small shapes do not. What is *not* known is
  how much of the published geomean moves, since one shape is not the table;
  that is a run rather than a probe, and worth appending to whichever run
  comes next rather than commissioning on its own.

  **The predictor, recorded before the run that would test it.** What decides
  whether an arm feels the nursery is not its total allocation but its
  allocation **in excess of the result buffer**, `(alloc − 1) × 8l`: the
  result is one large object and goes straight to the large-object list,
  bypassing the nursery, while the excess is the part that churns through it.
  On the six arms whose `vgg-14-c512-k3` behaviour is already measured the
  rule separates them outright, and the line falls on the nursery itself —
  affected at 11.2 to 13.2 MB of excess (`bq-expand` and its two
  output variants, `bq-odo-gm-mulback`), unaffected at 2.4 MB
  (`bq-scan-rem-gm-mulback`) and 0 (`mut-odo-vecdims`). Total allocation does
  *not* separate them, putting an unaffected arm at 9.6 MB and an affected
  one at 18.5 MB with no line between that means anything. Applied to the
  kept Run 9 cells the rule predicts **131 of 782** cells move, concentrated
  on the large shapes, and names **14 arms that should not move on any
  shape** — the whole `mut-odo-vecdims` family, `build`, `mut-odo`,
  `gen-quotrem`, `gen-unsafe` and both `sum-only` halves. Two consequences
  worth having in writing before the measurement. `list` itself is predicted
  affected on 17 shapes, by up to 353 MB of excess, so **the baseline is
  expected to move and every ratio with it** — which is most of the case
  against adopting the flag casually. And `build` and `mut-odo` are both
  predicted *unaffected*, so their 1.13× gap should survive `-A32m`
  untouched; if it collapses instead, this predictor is wrong and what this
  page calls placement is really the allocator.

  **And the eight class populations, which that count left out**
  (2026-08-09, the same arithmetic over the kept JSONs; it reproduces the
  main set's 131 of 782 exactly, which is what makes the rest worth
  quoting). `list` crosses the nursery in **every** population, so no class
  table divides by an unaffected baseline — 336 MB of excess on
  `bcast-tall-Mx2`, 118 on `reshape1-500k`, 34 to 81 elsewhere. The
  strategies cross in three classes only, `bcast` (24 cells of 96),
  `reshape1` (17 of 64) and `window` (10 of 66); in `bcastmid`, `rev`,
  `revsome`, `scaled` and `slice` nothing but the baseline does. So those
  five are penalised in one direction throughout, which leaves their
  orderings alone and their levels flattered, while the three are penalised
  unevenly and are where a nursery A/B would move a table. Whichever run
  takes the `-A32m` pair should take the classes with it.

  **That second half was tested the same day and the prediction holds.** Both
  arms plus a `sum-only` half, filtered over all 24 shapes, run twice from
  one binary with the nursery as the only difference (2026-08-09): the pair
  reads **1.1604** at the default and **1.1433** at `-A32m`, each at three
  wins of 24 and sign p 0.00028. The gap does not move. Nor do the arms
  themselves, 1.028 and 1.043 in absolute time across the change, against the
  35–40% the excess-allocating arms show. Two things follow. The predictor
  survives a test it could have failed, on the side where failure was
  cheapest to detect. And **the placement question is now confirmed
  independent of the allocator**, so the pad probe is unavoidable rather than
  possibly-subsumed: this pair's 1.16× is not filtering either, the full run
  reading 1.13× over the same shapes with 31 benches between the two arms.

**Three of Run 8's were answered the same day**, each by the probe its own
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

**What Run 9 leaves open**, each with what would settle it:

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
  large: it is. And the *how* has come one step down since, in the binary
  rather than in a run: the pair's disagreement now has a 28-byte loop under
  it that GHC aligns to eight bytes, with the two arms' executed copies
  falling either side of a cache-line boundary ([the floor section][floor]).

  **Run 9 makes this the page's central question rather than a caveat on it.**
  A membership change alone moved five fingerprint arms from 0.910 to 1.192 in
  absolute time against a baseline that held to 0.998, and moved
  `build`/`mut-odo` — one worker, two slots — to 1.13 where Run 8 read 0.86
  and Run 7 1.24. So the closing question above is now answerable only here:
  every route through the roster is blocked, because the roster is one of the
  things that sets the layout. The probe to build is the pad probe with
  `build` and `mut-odo` both timed and a susceptible arm's address stepped
  deliberately across a handful of binaries, membership fixed throughout.
- **The queue of experiments that want a quiet machine**, ranked, so that the
  next quiet window is not spent deciding what to spend it on. Written down
  2026-08-09 with Run 9's artifacts still alive, and the ranking turns on one
  thing worth stating: *the binary must not be rebuilt between the arms of a
  comparison*, since a rebuild is worth up to 18% on a susceptible arm and
  swamps most of what is being asked.
  1. **The main set at `+RTS -A32m`, paired with a main set at the
     default** — about 2h15m for both, and the cleanest A/B this page can
     run, because an RTS flag needs **no rebuild**: the placement and rebuild
     confounds that qualify every other cross-run sentence here do not apply,
     and the only thing to pin besides is the benchmark selection. It tests
     the predictor above over 782 cells instead of six, and its
     default-nursery half doubles as the run-to-run drift measurement
     [Provenance](#provenance) says is owed. Do this one first.
  2. **The pad probe done properly** — four to six binaries differing only in
     inert pad arms, with `build` and `mut-odo` both timed this time (the
     first attempt lost them to a shell glob) and a *susceptible* arm's
     address stepped deliberately rather than incidentally. Half a day. It is
     the only route left to the placement question now that every route
     through the roster is blocked, and it is **not** shrunk by 1: the
     `build`/`mut-odo` gap was measured across the nursery change the same
     day and did not move, so placement and the allocator are separate
     effects and this probe has to be run for its own sake. **The step is
     eight bytes**, which is all GHC aligns the loop in question to, and the
     pair now carries a prediction to aim at: [the floor section][floor]
     reads the executed copy of `build`'s innermost loop across a cache-line
     boundary and `mut-odo`'s inside one, so pad until `build`'s lands whole
     and see whether the gap goes with it.
  3. **A third `-nosum` arm, on a flat fill** — a `Main.hs` addition and then
     a filtered run over the shape set. The two existing `-nosum` arms are an
     odometer and an expansion, so a flat fill is the one probe that
     separates *the read is biased* from *those two arms are*, which is what
     gate 3's entry below now needs.

  And two things **not** worth a quiet window, recorded so they are not
  reached for: the *how many preceding benches warm it* sweep, which the
  nursery finding supersedes — the bench count is the symptom and the
  allocation area is the cause; and the element-type re-probe, whose trigger
  is a run that moves the ordering at `Storable Double`, which Run 9 does
  only through layout and membership rather than anything an element type
  would feel.
- **Is the term still unbiased?** Gate 3 passed but stopped bracketing 1:
  every in-situ median of both arms in all nine populations sits below it,
  0.960 to 0.999, for the **second** run running
  ([sum-only](#sum-only-and-the-correction-now-applied)). Eighteen readings
  on one side across two runs is no longer the coin-flip the failure test
  assumes, so the next measurement is not another gate reading: it is a third
  `-nosum` arm on a strategy whose write pattern differs from both — a flat
  fill rather than an odometer or an expansion — which is the one thing that
  would say whether the bias is the *read* or those two arms. Run 9's cells
  have since been read under those medians and narrow everything except that
  ([sum-only](#sum-only-and-the-correction-now-applied)): the shortfall is
  systematic per cell rather than differencing noise, the two arms order the
  shapes alike, it runs about a tenth of the term at the smallest shapes and
  vanishes at the largest, and re-pricing both arms by it moves no published
  geomean by a point. So the flat fill is the only thing left to ask, and the
  bias it would characterise is small enough that the column stands either
  way.
- **Before crediting a margin to a strategy, check whether the two arms' hot
  loops are the same code and where each landed.** Two families now read
  that way ([the floor section][floor]), and in one of them it suspended an
  axis figure the run had just published. What it does **not** extend to is
  a sweep of the roster, which was tried: the reading needs two arms whose
  hot loop is identical *and* which differ nowhere else, and the timed
  roster holds exactly the two groups already read. Everywhere else the
  shared loop is a table build while the arms differ in the output loop that
  distinguishes them, so a line span there competes with real arithmetic and
  says nothing; and `bq-gen`, whose 11% is still unaccounted for, has no
  counterpart sharing its per-element loop at all, so this instrument cannot
  reach it. Recorded so the sweep is not attempted a second time.
- **Run 10's two predictions, registered before it runs.** Its order was
  chosen for heap state — `sum-only-early` above `list`, so nothing is
  measured on an ungrown pool — and the layout it happens to give was then
  read off the binary rather than shopped for, which is the distinction that
  keeps the run from being confirmatory. Against Run 9's offsets, both of
  the straddle hypothesis's arms move, in opposite directions:
  1. **The FastReshape three go straddling to resident** (mod 40, 44, 44 to
     mod 0, 36, 36) while their control stays resident (24 to 16). The
     hypothesis predicts 1.1552, 1.1795 and 1.1645 collapse toward 1.00. If
     they hold near 1.16, the hypothesis is dead and [the suspension of
     those axis figures](#the-mutable-ceiling-not-taken) is withdrawn —
     which is the outcome this page has the most reason to want detectable,
     the suspension being its own.
  2. **`mut-odo` goes resident to straddling** (29 to 53) while `build` stays
     straddling (53 to 45). The hypothesis predicts their 1.13 closes toward
     1.0. If it holds or widens, the hypothesis is dead by the other route.
  3. **The anchors move, and one of them is a control.** Warming `list` is
     the object of the swap, so the absolute anchors should fall and every
     ratio rise with them — but not uniformly, and the excess-allocation
     rule says which. Ten of the eleven anchor cells carry 27 to 336 MB of
     excess and should move; `cnn-slice-c32`, at 0.05 MB, sits under the
     nursery and should hold, which makes it a control inside the anchor
     table. If it moves too, what warming does is not the nursery; if the
     other ten do not, warming does not reach the baseline and the swap
     bought nothing. And a fall shared by all nine populations is one effect
     rather than nine findings, so read the anchors together before reading
     any class paragraph.

  Two arms of one prediction, either of which can kill it, on arms already
  rostered and at no extra machine time. Read them before reading anything
  else in Run 10, and record the verdict here rather than in the run's own
  chapter, which the run after replaces.
- **What does the roster owe the next run?** Run 9's delta is empty and Run
  10 inherits shapes, roster and regime all pinned, so a Run 10 at
  `-fspec-constr` would be the exact repetition this page has never had and
  the only clean measurement of run-to-run drift available. Run 9 supplies a
  partial one already — `list`'s own figures, whose code and slot did not
  move, held to 0.2% in geomean and scattered up to 5% per shape — but that
  is one arm. **Decided for Run 10: `-fspec-constr`, and the repetition
  spent** — the roster order buys the pool fix and the two predictions above
  instead, which is a trade of a measurement this page has never made for
  two it can act on. So the drift measurement stays owed and `list`'s 0.2%
  is still the only bound on it, and a return to -O1 — the regime
  `Data/Array/Internal.hs` actually compiles under, unvisited since Run 7 —
  stays open for the run after.

[floor]: #the-noise-floor-is-the-aa-controls-not-the-ci
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[opening]: #regime-3-micro-benchmark-the-fix-bq-expand
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
