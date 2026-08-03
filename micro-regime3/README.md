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

A direct mutable result buffer is faster still, and Failed Run 6 widened the gap:
`mut-odo` is 1.2× over `bq-expand`, and `mut-odo-vecdims` — the same fill
with its dimension lists replaced by unboxed vectors — is **2.4×**, the
fastest strategy measured here. Both need a new `Vector`-class method, which
was measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal ([below](#the-mutable-ceiling-not-taken)).

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure one is **`bq-scan-packed-mulback`**, 0.124
against `bq-expand`'s 0.179; the fastest carrying **no size precondition at
all** is `bq-scan-rem-gm-mulback` at 0.160. None is what
`Data/Array/Internal.hs` does today, and the trade-offs — preconditions,
allocation, and a noise floor of about 2% — are in [Results](#results) and in
[the Lemire section](#lemire-multiplicative-inverses-at-the-two-division-sites).

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
then compares the regime-3 strategies in one binary — the real orthotope
compiles only one at a time, so a replica is the only way to A/B them.

The originals, the first attempt, and the two odometer fills:

    list         original fallback: vFromListN l . toListT (lazy cons-list)
    gen-quotrem  first attempt: vGenerate + per-element quotRem (one per rank)
    gen-unsafe   gen-quotrem with unsafeIndex, to price the bounds check
    unfold-add   unfoldrExactN with an allocating immutable-list odometer
    fused        unfold-add's allocation-free completion: run base-offsets
                 precomputed, then a strict three-Int unfoldrExactN state
                 whose hot path is a single add

The **run base-offsets family** — same output (one `vGenerate` with one
`quotRem` per element, reading a precomputed `m`-element run base-offsets
table); these differ *only* in how that table is built:

    offsets-quot base-offsets via fromListN . runBaseOffsets (a lazy build/foldr list)
    bq-mut       base-offsets via a VS.create mutable odometer (concrete Int scratch)
    bq-mut-runs  bq-mut with the innermost outer dim written by an additive loop
    bq-unfold    base-offsets via VS.unfoldrExactN (pure-typed, immutable-list state)
    bq-gen       base-offsets via VS.generate + one quotRem per run
    bq-gen-lemire
                 bq-gen with its per-run, per-dimension build quotRems replaced
                 by Lemire multiply-highs (1.30x SLOWER; the losing measurement
                 is kept in the suite so the idea is not proposed again)
    bq-expand    base-offsets via iterated VS.concatMap expansion   <-- SHIPPED
    bq-expand-zf bq-expand with the zip and fold fused into one recursion
    bq-expand-b  bq-expand seeded from the first dim's enumFromStepN

and these hold the build at one of the above and vary the per-element output
instead — the line every member of the family ends in, so pricing it once
prices it for all of them:

    bq-expand-qr-prim
                 bq-expand with the output quotRem replaced by the primop it
                 wraps, which prices GHC's two guards on it apart from
                 deleting the division
    bq-expand-lemire-out
                 bq-expand with the shared per-element OUTPUT quotRem replaced
                 by a Lemire multiply-high (see Results; faster pure
                 strategies have been measured since)
    bq-expand-lemire-mulback
                 lemire-out in the leaner form orthotope would ship: the
                 quotient from the multiply-high, the remainder as i - q*s
    bq-expand32-lemire-mulback
                 that, with the table and every concatMap intermediate at Int32
    bq-mut-lemire-out
                 the same output substitution against bq-mut's unrelated build
    bq-mut-lemire-mulback
                 and the mul-back form of it
    bq-mut-runs-mulback
                 the fastest build and the fastest output put together
    bq-mut-runs-gm-mulback
                 that, with a Granlund-Montgomery quotient instead: one extra
                 shift per element and no l < 2^32 bound
    bq-scan-mulback
                 the mul-back output over a table built as a prefix sum of a
                 generated delta stream -- pure, no mutable scratch
    bq-scan-rem-mulback
                 bq-scan-mulback with the build's divisibility test by quotRem
                 rather than multiply-high, shedding the builder's own bound
    bq-scan-gm-mulback
                 bq-scan-mulback with the Granlund-Montgomery quotient
    bq-scan-rem-gm-mulback
                 both of those at once: the one composition here carrying no
                 size precondition anywhere
    bq-odo-mulback
                 the scan's table by an adds-only unfoldrExactN odometer, no
                 per-entry division or multiplication at all
    bq-scan-packed-mulback
                 the scan's stream state packed into one Int, the constructive
                 test of the bare-Int-state law

Whole-offset / alternative-gather variants:

    backperm     build the full l-length offset vector, then unsafeBackpermute
    cm-gather    fused map . concatMap gather (no output quotRem at all)
    all-expand   full offset grid via concatMap expansion, then map gather
    offtab       full offset table via a mutable odometer, then vGenerate gather
    offtab32     offtab with that table narrowed to Int32
    offtab-scan  offtab with that table built by the scan, so nothing of it is
                 mutable -- the bet did not survive measurement

Direct mutable result-buffer fills (need a class extension / mutation):

    mut-odo      walk the outer odometer, write each run with a tight
                 additive inner loop straight into the result buffer
    mut-odo-vecdims
                 mut-odo with the odometer's dimension lists replaced by
                 unboxed vectors -- the fastest strategy measured
    mut-offsets  as mut-odo but iterating the precomputed run base-offsets list
    build        mut-odo through vBuildVS, a prototype of the one new Vector
                 method such a fill would need (prices the abstraction)
    mut-flat     bq-mut-runs-mulback's table and per-element arithmetic in a
                 flat ST loop rather than a vGenerate, so the pair prices the
                 output mechanism alone

    concat-runs  class-methods-only: per-run vGenerate + vConcat (mirrors
                 the regime-2 branch, but with strided runs) -- checked but
                 no longer timed, see below

That is the order `Main.hs` defines them in, and the order to read them in.
The order they are *run* in is deliberately a different one, fixed by
`roster` in that file so the controls straddle what they price; the Results
table below is sorted by time, a third. Sharing that roster with the
strategies, and not strategies themselves, are three A/A controls and the
`sum-only` pair — [the noise floor](#the-noise-floor-is-2-not-the-ci) and
[sum-only](#sum-only-and-why-no-corrected-column-is-published) say what each
is for.

The `check` mode (below) asserts every strategy produces byte-identical
vectors on every shape, and that each shape actually takes regime 3. It is
built from that same `roster`, so a strategy cannot be timed without being
checked; what that leaves to go stale, `read-run.py --lint` holds — every arm
named here, every strategy defined in `Main.hs` rostered, each A/A control
running the arm its name duplicates, and every control named as the reader's
own control test reads it.

`concat-runs` is the one strategy `check` covers and the benchmark does not.
It was by a clear margin the noisiest bench of the set — Failed Run 6's single
worst cell, the worst cell on five of its shapes, and a median cell some 2.5×
the shape's typical CI — and it sits in the heavy tail of both time and
allocation, though `list`, `unfold-add` and `cm-gather` all allocate more.
Since every `time` figure is a ratio to `list`, which runs first in the group,
an aftermath that outlived one bench would tilt the whole group one way rather
than cancelling out. Nothing was caught doing that: its successor times the
same after it as after a benign predecessor, and of the three A/A pairs the
one that straddles it agrees best. The unprobed risk is the [roster
effect](#the-noise-floor-is-2-not-the-ci) — a property of what shares a
process, worth 20% in horde-ad's `ConvVjpBench`, and one that persists for a
whole run rather than for one bench. What would trigger it is a bench extreme
enough to change the process it runs in, and this one is extreme where it
counts least defensibly: in how little its own figures can be trusted. They
refute it anyway, so timing it bought nothing to weigh against that.

## Running it

Self-contained (base + vector + criterion + deepseq):

    cd micro-regime3 && cabal run micro              # 5s per bench: hours
    cd micro-regime3 && cabal run micro -- -L1       # 1s per bench, rougher
    cd micro-regime3 && cabal run micro -- check     # correctness only, fast
    cd micro-regime3 && cabal run micro -- diag      # per-build allocations
    cd micro-regime3 && cabal run micro -- vgg       # one group by name prefix
    cd micro-regime3 && cabal run micro --ghc-options=-fspec-constr
    cd micro-regime3 && cabal run micro --ghc-options=-O2 -- diag

`micro.cabal` builds at -O1, the regime a default `cabal build` of orthotope
compiles under. The other two regimes are command-line only, the flag landing
after the cabal file's so the later `-O` wins: `-fspec-constr` for Run 7
(SpecConstr), `-O2` for the half of the scan-fusion refutation
that inverts there (a `diag` at -O2 is what measures it).

Those are all probes. A run whose numbers are meant to be kept and written
into this file is a different undertaking, and has a procedure of its own:
[Making a major benchmark run](#making-a-major-benchmark-run).

## Making a major benchmark run

A *major run* is the whole roster over the whole shape set at criterion's
default budget, analysed and written into this file; everything above is a
probe beside it. What follows is the procedure, and it is written to outlive
any one run.

**Where.** A session starts in `~/r/horde-ad`, which leaves *that*
repository's `CLAUDE.md` resident while this one is not governed by it; read
this file and `read-run.py`'s docstring instead, orthotope carrying no
`CLAUDE.md` of its own. Then:

    cd ~/r/orthotope/micro-regime3

**Before spending the hours**, three cheap checks:

    cabal build micro
    cabal run micro -- check     # every strategy agrees, every shape regime 3
    ./read-run.py --lint         # the roster, against this file and itself

**The run** is one command, the build flag going before the `--` when the
name asks for one:

    cabal run micro -- --json RUN.json > run.log 2>&1
    cabal run micro --ghc-options=-fspec-constr -- --json RUN.json > run.log 2>&1

Everything else is already a default. The allocation fit
`--regress allocated:iters` is on (it is well-conditioned at 5s), so `alloc`
comes out of the same process as the times rather than a side run; passing
`--regress` explicitly would replace it. The run prints its own provenance to
stderr as it finishes — roster size, shape count, wall clock and the two heap
peaks — so a document quoting its scale copies a measured number rather than
counting benches by hand, and so `micro.cabal`'s `-M2G` headroom claim has a
current source; the stderr redirect above is what keeps it.

**The time budget is always criterion's default.** Raising `-L` would buy
samples for the slowest shapes -- they bottom out around 6 where the fastest
get 130 -- but at a proportional cost in wall clock, and the runs are already
hours. Every recorded run therefore uses the default, so figures stay
comparable between runs and the sample counts in the tables mean the same
thing throughout. Where that leaves a shape thinly measured, the `smp` and
`CI%` columns say so rather than the budget hiding it.

Expect a couple of hours, so run it in the background — and **run nothing
else on this machine while it does**. Every strategy shares one process
precisely so that the figures are commensurable, and the [noise
floor](#the-noise-floor-is-2-not-the-ci) section is the measured evidence that
they move with what shares that process. What the rest of the machine does on
top of that is unmeasured, and a recorded run is the wrong place to find out.

**After it lands:**

- analyse with `./read-run.py`, which is where every table in this file comes
  from — read [Reading the results](#reading-the-results) first, and do not
  write another reader;
- walk the list under [Provenance](#provenance) of what the new numbers
  replace, and do not trust it to be complete: re-run the two sweeps it names,
  since it has been wrong before;
- record beside the numbers the run's name and regime, its stderr provenance
  line, and which machine (this page's figures are one desktop's and are not
  portable — see [Provenance](#provenance));
- keep no JSON here afterwards. The normal state of this directory is no run
  artifact at all, which is decided rather than an oversight; the numbers live
  in this file and the artifact does not.

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
image's patch tensor exceeds `sizeCap`, the element count that partitions
benchmarked shapes from flagged ones: past it a call is slow enough to
starve the sample count, and the run is long and memory-hungry with it.
`Cin` and the spatial dims scale `l` linearly too (in the full run, doubling
`Cin` ~doubles the cost, quadrupling the spatial area ~quadruples it), but
reducing them reproduces a shape already here — a per-position slice, or a
smaller conv — so `nImgs` is the only dimension genuinely free to drop.

## Results

Failed Run 6: criterion, GHC 9.12.4, **-O1**, hardened harness (`env`, `NOINLINE` on
the benchmark-facing functions, separate `check` mode); every strategy in one
process, so the figures are commensurable. 44 benchmarks over 35 shapes,
2h13m.

**Run 6 (-O1), the redo, keeps that regime**, so it replaces this table row
for row rather than measuring a different one; Run 7 (SpecConstr) comes after
it, and changes the answer for a whole class of strategies rather than
nudging it (below).
-O1 is the regime a default `cabal build` of orthotope compiles under today,
which is why the record is taken there first.

How to read the columns:

- **time** is the geomean over shapes of the per-shape OLS *slope* / `list`'s
  slope, with each strategy's single highest-CI shape dropped first. The trim
  matters: a 35-shape geomean divides ordinary noise by sqrt 35 but a lone
  wild cell by only 35, so one cell measured to +-70% moves the average more
  than all the well-measured cells together. Dropping one cell of 35 costs
  little and removes the larger error.

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
  move with what it was fitted on. **That is wrong.** Over the whole shape set
  41 of 42 strategies vary by more than 5% from shape to shape, the median
  strategy by 3.93× and the worst by 22×, and three shapes of identical
  `l` = 1800000 give `bq-expand` 2.778×, 3.000× and 3.642×. Every allocated
  fit sits at R² 1.000, so the spread is the quantity and not the measurement,
  and allocation being deterministic per call the budget does not bear on it —
  the run behind this was a rough one and that costs the figures nothing.
  What does survive is the column: a median over a *pinned* shape set
  reproduces, this run landing `list` at 27.67× and `unfold-add` at 29.89×
  where Failed Run 6's 35 shapes gave 27.67× and 29.90×. So read `alloc` as a
  statistic of a strategy **and** a shape set, and pin the shape set before
  comparing it across runs, exactly as the `time` column already asks.

| strategy | time | CI% | smp | alloc | needs | precondition |
|---|---:|---:|---:|---:|---|---|
| *sum-only* | *0.026* | *0.11* | *133* | *0.00x* | *shared term, not a strategy* | |
| **mut-odo-vecdims** | **0.074** | 0.15 | 111 | 1.00x | new `Vector` method | |
| mut-flat | 0.092 | 0.36 | 107 | 1.33x | new `Vector` method | `l < 2^32` |
| **bq-mut-runs-mulback** | **0.099** | 0.42 | 105 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| *bq-mut-runs-mulback-aa* | *0.101* | *0.42* | *105* | *1.33x* | *A/A control* | |
| bq-mut-runs-gm-mulback | 0.109 | 0.46 | 104 | 1.33x | mutable `Int` scratch | none |
| bq-mut-runs | 0.114 | 0.44 | 103 | 1.33x | mutable `Int` scratch | |
| **bq-scan-packed-mulback** | **0.124** | 0.19 | 101 | 2.00x | nothing (pure) | `l`, offsets < 2^32; m <= 2^31 |
| bq-odo-mulback | 0.133 | 0.24 | 99 | 3.44x | nothing (pure) | `l < 2^32` |
| offtab32 | 0.145 | 0.96 | 95 | 1.50x | mutable `Int` scratch | src < 2^31 |
| offtab | 0.148 | 1.15 | 94 | 2.00x | mutable `Int` scratch | |
| build | 0.148 | 1.17 | 96 | 1.00x | new `Vector` method | |
| mut-odo | 0.148 | 0.97 | 95 | 1.00x | new `Vector` method | |
| bq-scan-rem-mulback | 0.152 | 0.34 | 97 | 4.33x | nothing (pure) | `l < 2^32` |
| bq-scan-mulback | 0.160 | 0.19 | 96 | 4.33x | nothing (pure) | `l < 2^32` |
| **bq-scan-rem-gm-mulback** | **0.160** | 0.31 | 96 | 4.33x | nothing (pure) | **none** |
| bq-expand32-lemire-mulback | 0.162 | 0.26 | 94 | 3.42x | nothing (pure) | `l < 2^32`; src < 2^31 |
| bq-mut-lemire-mulback | 0.164 | 0.76 | 93 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-expand-lemire-out | 0.165 | 0.25 | 93 | 4.17x | nothing (pure) | `l < 2^32` |
| bq-mut-lemire-out | 0.166 | 0.63 | 93 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-mut | 0.166 | 0.60 | 92 | 1.33x | mutable `Int` scratch | |
| bq-expand-lemire-mulback | 0.166 | 0.26 | 93 | 4.17x | nothing (pure) | `l < 2^32` |
| bq-scan-gm-mulback | 0.171 | 0.29 | 95 | 4.33x | nothing (pure) | `l < 2^32` (builder) |
| *bq-expand-aa-adjacent* | *0.177* | *0.20* | *92* | *4.17x* | *A/A control* | |
| **bq-expand** | **0.179** | 0.19 | 92 | 4.17x | **nothing -- SHIPPED** | |
| bq-expand-qr-prim | 0.179 | 0.27 | 92 | 4.17x | nothing (pure) | shape well-formed |
| *bq-expand-aa-distant* | *0.179* | *0.25* | *92* | *4.17x* | *A/A control* | |
| bq-expand-b | 0.180 | 0.24 | 92 | 4.17x | nothing (pure) | |
| bq-expand-zf | 0.182 | 0.20 | 92 | 4.17x | nothing (pure) | |
| offsets-quot | 0.257 | 0.72 | 86 | 6.67x | nothing (pure) | |
| mut-offsets | 0.296 | 0.79 | 82 | 7.56x | new `Vector` method | |
| fused | 0.310 | 0.63 | 78 | 10.67x | new `Vector` method | |
| bq-unfold | 0.333 | 0.45 | 80 | 10.23x | nothing (pure) | |
| offtab-scan | 0.344 | 0.29 | 77 | 11.00x | nothing (pure) | `l < 2^32` (builder) |
| bq-gen | 0.391 | 0.90 | 72 | 4.67x | nothing (pure) | |
| all-expand | 0.460 | 0.34 | 76 | 12.65x | nothing (pure) | |
| bq-gen-lemire | 0.506 | 0.89 | 65 | 4.00x | nothing (pure) -- refuted | `l < 2^32` |
| backperm | 0.563 | 0.53 | 69 | 18.40x | nothing (pure) | |
| *concat-runs* | *0.583* | *0.82* | *70* | *11.23x* | *nothing (class-only) -- no longer timed, see above* | |
| cm-gather | 0.686 | 0.51 | 64 | 23.15x | nothing (pure) | |
| list (baseline) | 1.000 | 0.38 | 58 | 27.67x | -- | |
| unfold-add | 1.005 | 0.68 | 57 | 29.90x | nothing (pure) | |
| gen-unsafe | 1.067 | 0.57 | 49 | 13.00x | -- | |
| gen-quotrem | 1.096 | 0.93 | 49 | 13.00x | 1st attempt | |

Two caveats on the columns. The `needs` tier for `backperm`, `cm-gather` and
`all-expand` is **doubtful**: each produces its result by mapping a concrete
`Int` vector into the abstract element type, and the class has no method for
that (`vMap` is `v a -> v b`), so on the reasoning that re-tiered `fused` they
may need a class method too. An equivalent `vGenerate` form exists -- that is
`offtab`'s shape -- so the strategies are not ruled out, only the labels
suspect. And the geomean weights all 35 shapes **equally**, so a figure here
is a ranking statistic, not a claim about total work saved: the small shapes
count as much as the 4M-element ones.

### The noise floor is 2%, not the CI

Three A/A controls run an existing strategy twice under a second name. They
are the only rows whose true ratio is known to be exactly 1:

| pair | measured | where |
|---|---:|---|
| `bq-mut-runs-mulback` vs its twin | **1.0200** | fast end |
| `bq-expand` vs adjacent twin | 0.9882 | mid |
| `bq-expand` vs distant twin, 34 slots | 1.0014 | mid |

Two of those three are ratios of *trimmed* columns whose arms dropped
different shapes, so they compare different shape sets: paired shape by shape
they read 0.9991 and 0.9964 rather than 1.0200 and 0.9882, while the distant
pair, whose arms dropped the same shape, is 1.0014 either way. The published
figures are the right yardstick for comparing two rows of this table, a reader
of it computing exactly that; a margin measured per shape belongs against the
paired ones. `read-run.py --aa` prints both and says which pairs differ.

**Nothing under about 2% is a result.** The CI% for those same rows reads
0.19-0.42%, so the interval understates run-to-run variability roughly
fivefold: it measures sampling error *within* one benchmark, while two
separately placed benchmarks also differ in code layout, cache occupancy and
inherited GC state. The A/A is the only column that sees that, and it is what
a margin should be compared against.

Position is not the cause: the distant pair, 34 slots apart, agrees better
than the adjacent one.

Two things follow, and the controls have been re-aimed for Run 6 (-O1)
accordingly. The floor tracks **1/time, not GC pressure** -- the noisier arm
was the one allocating 1.33x, the quieter one 4.17x -- so the fast-end control
moves to `mut-odo-vecdims`, the fastest strategy measured and a third faster
than the arm that produced the 2.0%. And the close comparisons are **not** at
the top of the table, where 0.074/0.092/0.099 stand 20-35% apart, but in two
bands lower down: the five `bq-expand` variants within 3%, which the adjacent
control already covers, and the scan family, which holds an exact tie between
`bq-scan-mulback` and `bq-scan-rem-gm-mulback` that no control priced. The
distant slot therefore moves to `bq-scan-mulback`, where it prices that band
and still spans the group, so position stays monitored rather than assumed
once SpecConstr changes code layout. In a run those two print as
`mut-odo-vecdims-aa` and `bq-scan-mulback-aa-distant`, beside the surviving
`bq-expand-aa-adjacent`; the pairs in the table above are Failed Run 6's,
which had the twins elsewhere.

Three A/A points remain a poor estimate of a noise floor. Their own spread --
0.988, 1.001, 1.020 -- is the evidence that it is variable and roughly 1-2%,
so "~2%" is a soft threshold to compare margins against, not a computed
bound.

The floor above is also measured within one roster, and the roster is a
variable of its own: RTS pool state a predecessor leaves in the process
moved a horde-ad benchmark 20% ([the full account][pos-effect] -- which
includes this suite's own floor measured isolated against in-process, on
both harness generations). Every strategy sharing one process is what
protects the tables above, ratios cancelling the shared process draw; a
comparison that crosses runs should pin the benchmark selection along
with the binary, and between recorded runs here the roster has rarely
held still.

### R2 is the ramp detector, not the noise detector

The two columns catch disjoint failures. **CI%** finds sampling noise, which
the trim then removes. **R2** finds *curvature* -- early, low-iteration
samples running slower than late ones, because criterion forces only a minor
GC between samples and a full one just once per benchmark, so promoted data
accumulates as the sample count climbs.

A ramp is systematic, so it yields a *narrow* CI around a *biased* slope: the
trim cannot see it and will not remove it. The bias tilts the fit shallow, so
a ramped strategy reads slightly **faster** than it is -- and not uniformly,
since strategies allocating a large scratch ramp harder than in-place fills,
making the flattery differential exactly where the comparison is decided.
Read any row with R2 below 0.99 as possibly a couple of percent optimistic
rather than merely noisy. In Failed Run 6 that is 13 cells of 1540.

### sum-only, and why no corrected column is published

Every strategy is timed as `VS.sum . fb`, so every measurement carries the
same forcing pass; `sum-only` times that pass alone. It is 11-15% of
`bq-expand` across shapes, so every ratio here is compressed toward 1 by
about that much and the margins are *understatements*.

Subtracting it would restore them -- `bq-expand` 0.179 becomes 0.155,
`bq-scan-packed-mulback` 0.124 becomes 0.099 -- but it is not published, for
two reasons. It changes no ordering, since `(B+S)/(A+S) < 1` exactly when
`B < A`; and its own accuracy is unproven, because `sum-only` re-reads one
fixed vector while the strategies sum a vector their own fill has just
written, a warmer and less contended read. A second `sum-only` at the other
end of the group now tests whether the term is even position-independent; the
two print as `sum-only-early` and `sum-only-late`.
**That test is supplied by Run 6 (-O1), not this one**, which carried a
single `sum-only`; until it reports, no margin here is corrected. If the
halves agree the correction becomes sound and will be applied to every row;
if they diverge the term is not a constant and the correction is dropped
rather than applied.

A one-shape smoke run of the current roster is encouraging but not the test:
on `cnn-slice-c32` at `-L1` the halves read 169.9 ns and 170.1 ns, 0.12%
apart. One shape at a rough budget; Run 6 (-O1) gives all of them.

### Provenance

Failed Run 6 measured the shape set as it then stood. Every shape over
`sizeCap` has since been cut to it or moved to `tooBig`: `stretch-tab16MB` is
now `stretch-tab7MB`, `stretch-square-1400` is `stretch-square-1341`,
`stretch-r5-8x512` is `stretch-r5-8x432`, `stretch-wide-2xM` and
`stretch-tall-Mx2` keep their names on smaller dimensions, and
`vgg-28-c256-k3` and `resnet-stem-112-c3-k7` are flagged rather than run. The
single `sum-only` bench has become the pair described above, and `concat-runs`
is no longer timed, for the reason given with the strategy list. All of that
postdates these numbers — and the roster changes among them are the kind this
page's own noise-floor section says to pin before comparing across runs, so
Run 6 (-O1) is a fresh baseline rather than a continuation of this one.

Every figure here was measured on one desktop — Zen 3, a Ryzen 7 5800X, the
same machine whose `idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
None of it is portable, so a run elsewhere is a different measurement rather
than a repetition, and should say which machine here.

**What Run 6 (-O1) replaces.** Failed Run 6's numbers reach well past the
Results table, so this is the list to walk when the new ones land. It is only
as good as its own completeness, and it has not been: six of the sections
below were on no earlier version of it, and the previous update leaked past
it in a way still visible in the `gen-lemire` entry. Both sweeps that found
them are cheap to repeat — grep this file for figure-shaped numerals outside
the tables, and grep it for `Failed Run 6` — so repeat them rather than
trusting this list to have stayed complete.

- the Results table, all four columns, from `./read-run.py RUN.json`;
- the noise-floor table, from `--aa` — and mind which pairs' arms dropped the
  same shape, since only those two ratios mean the same thing — with the
  prose around it, which carries 0.074/0.092/0.099 and the 1.33x-against-4.17x
  argument that the floor tracks 1/time rather than GC pressure;
- the opening section's headline claims: `mut-odo` 1.2× and `mut-odo-vecdims`
  2.4× over `bq-expand`, `bq-scan-packed-mulback` 0.124 against 0.179,
  `bq-scan-rem-gm-mulback` 0.160;
- **What the table says**, where every bullet is a Failed Run 6 figure: the
  build ordering 0.179/0.166/0.257/0.333/0.391, `gen-quotrem` at 1.060, and
  the allocation multiples 4.2×/6.7×/1.0×/28×;
- **The mutable ceiling (not taken)**: 0.148 for `mut-odo`, `build` and
  `offtab`, 0.074, 0.124, and the "1.7×, not 2.4×" that closes it. This one
  and the next are rulings resting on figures, so stale numbers there re-open
  a decision rather than merely misreport one;
- **Why there is no gen-lemire**: 1.096 against 0.179, the 13.0× allocation,
  4.2×. Two of its figures are already stale and disagree with each other —
  it calls `gen-quotrem` and `gen-unsafe` "both 1.060" and the gap 5.9× where
  the Results table says 1.096 and 1.067 and the same section says 6.1×, the
  last update having moved the headline and left the argument. Settle which,
  and note that a tie is what made the bounds-check control "buy nothing":
  1.096 against 1.067 is 2.7%, just outside this page's own ~2% floor;
- **sum-only**: the 0.179→0.155 and 0.124→0.099 corrections and the 11-15%.
  This is also the run that decides whether the correction is published at
  all, its two halves being the test;
- `concat-runs`' "2.5× the shape's typical CI", in **What the benchmark does**
  and again in `Main.hs`'s `roster`;
- **R2 is the ramp detector**: "13 cells of 1540", a count over a roster and
  shape set that no longer exist;
- the Lemire section's `gen-quotrem`-against-`bq-expand` gap, and
  `bq-expand-lemire-out`'s 0.936×, its 0.934× slope, its 0.875-to-0.987 range
  and its 0.165-against-0.179 pair;
- `bq-gen-lemire`'s 1.30× loss, in the strategy list as well as in Results;
- the `alloc` column's shape-independence, which is refuted rather than open:
  the multiples vary across shapes by a median 3.93× where this page and
  `read-run.py` said half a percent, so the median over shapes is a smoothing
  and not the formality they call it. Both now say so; what is left for a run
  is to confirm it at full budget and to carry the consequence through — every
  multiple quoted in a `Main.hs` comment is a property of a strategy *and* a
  shape set, and the column wants the shape set pinned before it is compared
  across runs, as the `time` column already does;
- the per-shape `stretch-*` table, which says it predates Failed Run 6: Run 6
  can replace it or leave it saying so, but not silently inherit it;
- this section, which becomes Run 6 (-O1)'s own provenance;
- `read-run.py`'s docstring, whose validation paragraph names Failed Run 6 and
  whose `alloc` definition carries the shape-independence claim above;
- `micro.cabal`'s `-M2G` note, if the heap peaks the run prints have moved;
- `Main.hs`, wherever a comment cites a figure: the A/A spread and the
  `concat-runs` case, both in `roster`; the allocation multiples at
  `baseOffsetsScan` and `fbBQscanPackedMulback`; the tie at
  `fbBQscanRemGmMulback`; `fbMutOdoVecdims`' "half its control's time" and
  "fastest of everything measured"; `fbBQmutRunsGmMulback`'s "~10% behind";
  and `fbBQscanMulback`'s 1.33x "at the fastest pure time in the table".

How a run is made, and what to record beside its numbers, is [Making a major
benchmark run](#making-a-major-benchmark-run) — which is also where the walk
of the list above is one of the steps.

Four rows are not comparable to earlier runs, all from strictness fixes that
moved code toward what its comment already claimed: `bq-scan-packed-mulback`
and the two Granlund-Montgomery arms (a lazy tuple in `gmMagic`), and
`fused`, whose per-step state thunk had been inflating its allocation --
20.7x before the fix, 10.67x here.

## Reading the results

### The reader: read-run.py

Every figure below, and every column of the table above, comes out of
`read-run.py` in this directory. **Use it; do not write another reader.** The
definitions it encodes — which cell the trim drops, that `CI%` is a mean
half-width rather than a bound, that `alloc` needs an `l` the JSON does not
carry (it parses `Main.hs` for it), that the `*-aa-*` and `sum-only*` rows are
controls — each cost a session to settle, and an ad-hoc script gets them
subtly wrong. Its docstring is the reference for all of them; extend the
script rather than starting over.

    ./read-run.py RUN.json                  # roster, then the strategy table
    ./read-run.py RUN.json --shapes         # per shape: CI% max / median / mean
    ./read-run.py RUN.json --drops          # what the trim removes, by shape
    ./read-run.py RUN.json --aa             # the control pairs and their spans
    ./read-run.py RUN.json --cells          # every cell as TSV, for the rest
    ./read-run.py RUN.json --selftest       # check the reader's own invariants
    ./read-run.py RUN.json --exclude concat-runs --exclude-shape deep-7-c512-k3
    ./read-run.py --lint                    # Main.hs's roster, against README
                                            # and against itself

**No run artifacts are kept here.** The normal state of this directory is no
JSON at all, and one is made when a question needs it — which is the same
moment the reader is wanted, so it is built to be useful on a partial run as
well as a full one:

    micro --json RUN.json                                    # the whole thing
    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

The second takes seconds and still exercises the reader; a one-shape run says
so and skips the trim rather than dividing by an empty set. Failed Run 6's
JSON is gone with the rest, so the tables in this document cannot be
re-derived — Run 6 (-O1) replaces them.

`--lint` needs no run at all, which is this directory's usual state. It reads
`roster` out of `Main.hs` — the one list both the benchmark and `check` are
built from — and asks the four things about it that go stale silently: is
every arm named somewhere in this file; is every strategy defined in
`Main.hs` rostered, so that none is left neither timed nor checked; does each
A/A control run the same function as the arm its name duplicates; and is
every control named as the reader's own control test reads it, since a
renamed one would enter the aggregates as a strategy. An arm rostered and
deliberately not timed is a note rather than a failure, that being the case
of `concat-runs`.

The question it used to ask second — is every benchmarked strategy also held
to the reference by `check`? — is gone, and deliberately. The roster and the
agreement chain were two hand-written lists of the same strategies, and that
check compared them; one list now builds both, so the drift cannot happen
rather than being merely detectable. A check that cannot fail is a silent
search, so it was replaced rather than kept.

`--selftest` checks invariants of whatever run it is given: that the dims it
parses out of `Main.hs` match that file's own `l` annotations, that every cell
has a positive slope and a sane R², that the trim drops exactly one shape per
strategy and lands inside its own per-shape range, that `list` against itself
is 1, and that an A/A pair dropping the same shape from both arms has its
published ratio equal to its paired one. It names what it could not exercise
rather than passing silently, and exits 2 when the run file is absent. That
last invariant is a finding: the A/A ratios in the noise-floor table are
ratios of two *trimmed* columns, and each arm drops its own worst-CI shape —
so unless that is the same shape, the two columns are geomeans over different
shape sets. `--aa` prints both that published ratio and the paired per-shape
one, and flags the pairs whose dropped shapes differ.

### What the table says

- **The output method: a single in-order `vGenerate` wins.** Every
  run base-offsets-family strategy (`bq-*`, `offsets-quot`) uses it —
  `bq-expand-lemire-out` changes what the division is, not the `vGenerate` —
  and lands ahead of the fancier gathers: `fused`'s `unfoldrExactN`,
  `backperm`, `cm-gather` and `all-expand`, whose figures are in the table
  above rather than repeated here, four of them having drifted while they
  were.
  A single in-order `vGenerate` fuses tighter than a stepped `unfoldrExactN`
  state or a two-pass build-then-gather.
- **The base-offsets build decides within that family, and `concatMap` wins the
  pure builds.** Same output, only the `m`-element table build differs:
  `concatMap` (`bq-expand`, 0.179) is beaten by the explicit mutable fill
  (`bq-mut`, 0.166) and beats the lazy list (`offsets-quot`, 0.257),
  `unfoldrExactN` (`bq-unfold`, 0.333) and `generate`+per-run-quotRem
  (`bq-gen`, 0.391).
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
- **Lemire's multiplicative inverses win at one division site and lose badly
  at the other** — the section below tells that story in full.
- **`gen-quotrem` (the first attempt) is still slower than `list`** (1.060)
  — the mixed picture, reproduced: one `quotRem` per *dimension* per
  element costs more than the list's allocation on the shapes that matter.
- **Allocation:** `bq-expand` allocates ~4.2× the result vector (`concatMap`
  intermediates over the `m`-element base-offsets); `offsets-quot` ~6.7×
  (the cons list); the direct mutable fills ~1.0× (just the result); `list` ~28×
  (thunks). Lower allocation tracks lower time across the table.

## Lemire multiplicative inverses, at the two division sites

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

**At the per-element output site it wins.** (It was the fastest pure strategy
when written; Failed Run 6 has since put four ahead of it.) `bq-expand-lemire-out` is `bq-expand` with the shared
`i quotRem sInner` replaced, the table build held at `baseOffsetsExpand`. It
is **faster on all 35 shapes, geomean 0.936× `bq-expand`** (Failed Run 6: 0.165
against 0.179) — range 0.875 to
0.987, and the OLS `time` slope gives the same figure (0.934×), so no part of
it rests on the warm-up ramp. That takes it clear of the four-way tie: it
beats `bq-expand-b` on 33 of 35 shapes and even `bq-mut`, which needs
mutation, on 28. Two controls back it. Its allocation is identical to
`bq-expand`'s to within 5e-7 on every shape, which is what a build-identical
arm must show; and it runs *before* `bq-expand` in the group where
`bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot bias would
flatter one and penalise the other and cannot produce this pair of results.

**At the per-dimension build site it loses by 30%.** `bq-gen-lemire` is
`bq-gen` with the per-run, per-rank `quotRem`s replaced, and it is **1.302×
slower**, faster on 1 shape of 35. The shape of the loss says why: it tracks
*rank*, not element count — 0.997 at rank 2, 1.223 at rank 3, 1.370 at rank 5,
1.377 at rank 7, 1.427 at rank 10, 1.439 at rank 12. The cost is paid per
dimension, so the division was never what dominated there. Two reasons.
(i) The paper's win assumes you want a quotient *or* a remainder; an odometer
decomposition wants both, so the trick pays twice and collects once — where
`quotRemInt#` is one `idiv` yielding both. (ii) The magic table is a third
list to walk in step with `nts` and `sts`, adding a dereference and a pattern
match per dimension to the very loop whose per-dimension work was the target.
Rank 2 costs nothing because there is only one dimension to walk.

What separates the two sites is exactly what (i) and (ii) describe. At the
output the divisor is a single loop invariant, so `M` is computed once for the
whole fill and there is no list beside it; the per-element work really is one
division against two multiplies, and the multiplies win. The win is 6.4%
rather than several-fold because the hardware has moved since the paper:
64-bit `idiv` on this machine's Zen 3 (Ryzen 7 5800X) is ~14–19 cycles
against the 40–90 that made the trick famous, so there is far less to reclaim
than the method promises.

Two things a Core dump settled that source reading had got wrong. Both are
recorded because both were argued the other way first. **`quotRem` on `Int` is
not one instruction**: GHC wraps `quotRemInt#` in two guard branches, for a
zero divisor and for the `minBound quot (-1)` overflow, both on a
loop-invariant divisor — so the `d == 1` guard `fastQR` needs is not the
asymmetry it looked like, the baseline carries two of its own. And **the first
`fastQR` spent three multiplies where the algorithm needs two**, taking the
quotient from `timesWord2# m n` and then recomputing the low half as a
separate `timesWord# m n` when the one `timesWord2#` already yields both.
Fixing that is what turned the output site from a 2% curiosity into a 6.4%
win, and it recovered part of the build site's loss too — enough to see,
nowhere near enough to reverse it. Why the low half must not be recomputed is
recorded as a comment on `fastQR`, so the loose form is not written again.

**On shipping it.** `bq-expand-lemire-out` is pure, so the argument that kept
`mut-odo` out does not apply; what it costs is `MagicHash` and `UnboxedTuples`
in `Data/Array/Internal.hs`, about a dozen lines of helper, and a
precondition. The precondition is the substantive part: Lemire's identity
holds for `d, n < 2^32`, and `n` here is the linear output index, so a shipped
version needs an `l < 2^32` test choosing between the two fills —
loop-invariant and chosen once per call, but it must be there, since orthotope
does not otherwise cap array length. Weigh 6.4% against that; this
benchmark's job is to price it, not to decide it.

## Why there is no gen-lemire

A third such benchmark is easy to specify and is deliberately not written.
**`gen-lemire`** would be `gen-quotrem` — the first attempt's `vGenerate` over
a per-element, per-*dimension* `quotRem` — with those divisions replaced by
`fastQR`, standing to `gen-quotrem` exactly as `gen-unsafe` does: the same
base, one line changed. It is the form the idea is most naturally proposed in
— inverses of the array sizes, plural, one per dimension.

It looked the most promising of the three, on two independent grounds.

**Time.** `gen-quotrem` measures 1.096 against `bq-expand`'s 0.179, a 6.1×
gap, and the two differ chiefly in dividing once per rank per element rather
than once per element. Read that gap as division count and Lemire should
recover most of it — reaching the shipped strategy from a design needing no
base-offsets table at all. The bounds-check control seemed to corroborate:
`gen-unsafe` is `gen-quotrem` minus the bounds checks and buys nothing here
(both 1.060), so the cost is arithmetic rather than indexing.

**Allocation.** `bq-expand` allocates 4.2× the result, all of it the
base-offsets table and the `concatMap` intermediates building it. A
per-dimension decomposition needs no table — O(rank) magic numbers instead of
O(l/sInner) offsets — so it promised the mutable fills' ~1× allocation while
staying pure, which would be worth taking even on a time tie, since
allocation tracks time across this whole table.

Four numbers already in the tables above rule it out.

1. **The same substitution, measured at a sibling site, loses.**
   `bq-gen-lemire` is a per-dimension odometer decomposition with its
   `quotRem`s replaced by `fastQR` — structurally what `gen-lemire` would be,
   per run rather than per element. It is 1.302× slower with a loss that
   grows monotonically with rank. A per-dimension cost that *rises* when the
   division is replaced by a multiply says the division was not the
   per-dimension cost, and `gen-lemire` differs only in doing more of that
   same per-dimension work, once per element instead of once per run.
2. **The 5.9× gap is not mostly division.** `gen-quotrem` does not only
   divide per dimension; it walks two `[Int]` lists per element, a
   dereference and a pattern match per rank. The bounds-check control
   separates *indexing* from *arithmetic*, and that list-walking falls on the
   arithmetic side of the split — so the control never distinguished the
   division from the bookkeeping around it. Lemire adds to that bookkeeping:
   the magic table is a third list to walk, which is reason (ii) above.
3. **The allocation ground is contradicted by the strategies that already
   drop the table.** `gen-quotrem` and `gen-unsafe` allocate **13.0×** the
   result — three times `bq-expand`'s 4.2×, not a quarter of it. The
   per-element list recursion is itself what allocates, so dropping the
   base-offsets table costs allocation rather than buying it. No pure
   per-dimension strategy here allocates anything like the mutable fills.
4. **The output site caps what deleting a division can be worth.**
   `bq-expand-lemire-out` runs Lemire at the friendliest division in the
   benchmark — one divisor, magic computed once per fill, no list beside it,
   two multiplies — and it is worth 6.4%. A 6.4% ceiling does not close a
   5.9× gap.

And a `gen-lemire` that somehow survived all four would still not win, because
its ceiling is a design already beaten. The run base-offsets family's advantage
is structural — one division plus one table read per element, against rank-many
divisions *plus* rank-many list steps — so a free division still leaves the
walking. The division-free answer is already here and already faster:
`mut-odo` and `fused` remove the per-element index arithmetic instead of
accelerating it, which is the argument the whole table makes.

## Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes added
last — chosen to push past the ranges the rest cover, and named here without
their prefix — against the strategies nearest the decision, each as a
multiple of `list` on the same shape. These figures predate Failed Run 6 and
the shape-set changes under Provenance above, so read them for the ordering
they illustrate, not as current numbers:

| shape      | bq-expand | bq-expand-b | bq-expand-zf | lemire-out | build | offsets-quot |
|------------|----------:|------------:|-------------:|-----------:|------:|-------------:|
| inner1     |     0.206 |       0.226 |        0.191 |      0.185 | 0.260 |        0.425 |
| tall-Mx2   |     0.105 |       0.105 |        0.105 |      0.092 | 0.057 |        0.105 |
| coprime-r7 |     0.136 |       0.136 |        0.139 |      0.124 | 0.090 |        0.157 |
| rank12     |     0.378 |       0.378 |        0.403 |      0.369 | 0.314 |        0.463 |
| tab16MB    |     0.200 |       0.186 |        0.186 |      0.184 | 0.185 |        0.287 |

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is the only shape where the pure expansion
  strategies beat every mutable one: `bq-expand-lemire-out`, `bq-expand-zf`,
  `bq-expand` and `bq-expand-b` take the top four of the twenty-two, ahead of
  `mut-odo` (0.231) and `build` (0.260). Its innermost extent is 1, so each
  base offset covers a single element: the odometer that `mut-odo`/`build`
  step has nothing to amortize over, while the expansion build has no
  per-element odometer to begin with. At the other end `stretch-tall-Mx2` has
  an innermost extent of half its length and the ordering inverts completely —
  `mut-odo` 0.052 against `bq-expand` 0.105, with every mutable strategy
  ahead of every pure one. The geomean reports that second case and averages
  the first away, which is why this table is here.
- **Per-shape figures are far noisier than the geomean: trust the first
  digit only.** Independent runs of these shapes agree within 1–5% on most
  cells but differ by up to 27% on `stretch-inner1/bq-expand-b` — runs
  whose rosters also differed, making the
  [roster effect above](#the-noise-floor-is-2-not-the-ci) a candidate
  cause — and the order of `bq-expand{,-b,-zf}` within their sweep of
  `stretch-inner1` flips between runs. The sweep itself reproduces; which of the three leads does
  not. `bq-expand-lemire-out`'s margin is the exception that survives this
  caveat, being 35 shapes wide rather than one cell.
- **But check for a structural reason before discounting a cell as scatter,
  and check `stretch-inner1` in particular.** It is the shape whose innermost
  extent is 1, so a strategy that special-cases or elides a unit dimension
  behaves differently there *by construction*, and a striking figure is then
  the design showing through rather than noise. Two in `Main.hs` already do:
  the mul-back output hoists `s == 1` out of its loop entirely, and
  `baseOffsetsScan` elides unit dims, which on this shape leaves one real
  radix so no carry ever fires and the scan degenerates to a sequential fill.
  The scan-built strategies are not in the tables above yet; when they arrive,
  this is the cell to read first and the last one to average away.

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
- This benchmark: every strategy agrees with `list` on every shape.

End-to-end confirmation in horde-ad's `bench/ConvVjpBench.hs` (wiring this
branch's orthotope in and rebuilding ox-arrays + horde-ad) is not yet run;
the numbers above are from the replica.

## The mutable ceiling (not taken)

The `bq-*` strategies still fill the result one element at a time. The
tightest possible shape drops to a **mutable result buffer**: allocate it
once, walk the outer odometer, and write each innermost run with a tight
additive inner loop — no `quotRem`, no base-offsets table, no per-element step.
That is `mut-odo` (0.148) and `build` (0.148) — ~1.2× over `bq-expand` —
and `mut-odo-vecdims` (0.074), which is 2.4× over it and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.148) is nearly as fast without going that far: its output
is an ordinary `vGenerate` and only its `l`-sized `Int` offset table is filled
mutably, so it needs no class method, just a mutable scratch.

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
and minimal, and the gain over `bq-expand` (pure-Haskell either way, so
[the C-gap](#the-c-gap-still-a-deeper-ceiling) bounds both) did not justify
a new class method across all four instances. The strategies stay here as
the measured evidence for that ruling, so it is not re-proposed.
Failed Run 6 raises the stake rather than settling it: `mut-odo-vecdims` shows the
fill's real cost was the odometer's cons-list traffic, not the fill itself,
taking the class-method tier to 2.4× over `bq-expand` where it had been ~1.4×.
Against that, the best pure strategy now reaches 0.124, so the gap the class
method would buy is 1.7×, not 2.4×.

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
not taken). Two pure-Haskell items remain open:

- Deciding whether to ship `bq-expand-lemire-out`, the one measured strategy
  that beats what shipped without needing a class method
  ([above](#lemire-multiplicative-inverses-at-the-two-division-sites)).
- Tightening *regime 2* (innermost-normal, not exercised here) with a
  `toVectorT` that folds the contiguous runs directly instead of building
  the intermediate run list.

Being pure Haskell, it is bounded by the
[C-gap](#the-c-gap-still-a-deeper-ceiling)
above: it could sharpen regime 2 but cannot bring it within reach of the
stride-aware C kernels.

Two ideas died on paper, recorded so they are not re-proposed:

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
  class extension exists to provide. The table exists because `vGenerate`
  is stateless.
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

## TODO

- **No build-vs-output time decomposition.** `diag` measures per-builder
  *allocation* only, so a claim like "the table build is a third of the cost"
  -- the natural reading of `bq-mut-runs` beating `bq-mut` by 35% -- cannot be
  checked here. It needs a timing mode alongside `diag`'s allocation one,
  using the fixed-iteration differencing the horde-ad performance model
  prescribes (`-n 200` minus `-n 100`, fresh processes) rather than criterion,
  since the builders are not benchmarks.

[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
