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

A direct mutable result buffer is faster still, and Run 6 (-O1) widens the gap
further: `mut-odo` is 1.46× over `bq-expand`, and `mut-odo-vecdims` — the same
fill with its dimension lists replaced by unboxed vectors — is **3.03×**, the
fastest strategy measured here. Both need a new `Vector`-class method, which
was measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal ([below](#the-mutable-ceiling-not-taken)).

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure one is **`bq-scan-packed-mulback`**, 0.097
against `bq-expand`'s 0.155; the fastest carrying **no size precondition at
all** is `bq-scan-rem-gm-mulback` at 0.132. None is what
`Data/Array/Internal.hs` does today, and the trade-offs — preconditions,
allocation, and a noise floor of about 3% — are in [Results](#results) and in
[the Lemire section](#lemire-multiplicative-inverses-at-the-two-division-sites).

Every figure on this page is **net of the shared forcing pass** every strategy
is timed through, which Run 6 (-O1) is the first run licensed to subtract
([sum-only](#sum-only-and-the-correction-now-applied)). That makes none of
them comparable to a figure from an earlier run, or to one from a later run
that does not subtract it.

## How the strictly positive picture was achieved

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
**And the harness has to be hardened before any of that is believable** —
criterion `env` so input construction is outside the clock, `NOINLINE` so no
result is hoisted out of the timed loop, and the agreement check in a separate
`check` mode so it cannot share a computation with the benchmark via CSE.
Under it the ranking is stable and every time scales with `l`, so nothing is
being optimised away.

## What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT`
faithfully (specialised to `Storable Double`, horde-ad's element storage),
then compares the regime-3 strategies in one binary — the real orthotope
compiles only one at a time, so a replica is the only way to A/B them.

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
  (the one composition with no size precondition anywhere), `bq-odo-mulback`
  and `bq-scan-packed-mulback`.
- **Whole-offset and alternative gathers**, which build an `l`-length offset
  vector rather than an `m`-length one: `backperm`, `cm-gather`, `all-expand`,
  `offtab`, `offtab32`, `offtab-scan`.
- **Direct mutable result-buffer fills**, which need a class extension or
  explicit mutation and are the [ceiling](#the-mutable-ceiling-not-taken):
  `mut-odo`, `mut-odo-vecdims`, `mut-offsets`, `build`, `mut-flat`. And
  `concat-runs`, class-methods-only, checked but no longer timed (below).

The order they are *run* in is deliberately a different one, fixed by `roster`
in `Main.hs`; the Results table below is sorted by time, a third. Sharing that
roster with the strategies, and not strategies themselves, are nine controls:
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
and which `m` and every `alloc` multiple rest on. It is
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
effect](#the-noise-floor-is-3-not-the-ci) — a property of what shares a
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
default budget, analysed and written into this file. What follows is the
procedure, and it is written to outlive any one run.

**Where the effort actually goes, because it is not where it looks.** The run
is about two hours and *unattended* — it costs patience and a quiet machine,
nothing else. Everything expensive happens after it, in the write-up, and that
is where a session's budget is spent and where its mistakes are made. Two
consequences worth having in mind before starting. Prefer analysis that
localises — per shape, per control — over re-quoting figures that moved a few
percent and changed nothing; the first is where every surprise has come from
and the second is what has gone stale twice. And **a probe is not a lesser
instrument than a major run**: the measurements that closed the `sum-only`
objection, established that the forcing term scales, and settled the floor's
mechanism cost twenty minutes, zero extra machine time, and zero extra machine
time respectively, while the major run they hang off changed no decision at
all. A question with a discriminating measurement usually deserves a filtered
run now rather than a slot in the next full one.

**Where.** A session starts in `~/r/horde-ad`, which leaves *that*
repository's `CLAUDE.md` resident while this one is not governed by it; read
this file and `read-run.py`'s docstring instead, orthotope carrying no
`CLAUDE.md` of its own. Then:

    cd ~/r/orthotope/micro-regime3

**Before spending the hours**, three cheap checks:

    cabal build micro
    cabal run micro -- check     # every strategy agrees, every shape regime 3
    ./read-run.py --lint         # the roster, against this file and itself
    ./read-run.py --check-doc    # anchors, coverage, widths, stale figures

and one more that costs five minutes and is worth them, because the three
above exercise the *benchmark* while nothing exercises the *reader* until two
hours later:

    cabal run micro -- cnn-slice-c32 --json smoke.json   # every arm, one shape
    ./read-run.py smoke.json --selftest
    ./read-run.py smoke.json --aa
    ./read-run.py smoke.json --markdown >/dev/null
    rm smoke.json

That runs every roster arm on one shape and puts the whole analysis path —
the correction, the controls, the table generator — through its paces. A
reader broken by a roster change fails here in five minutes instead of after
the run.

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
floor](#the-noise-floor-is-3-not-the-ci) section is the measured evidence that
they move with what shares that process. What the rest of the machine does on
top of that is unmeasured, and a recorded run is the wrong place to find out.

If something did run anyway, **record the wall-clock window** rather than
hoping: the run's own log is timestamped only at the end, so without the
window there is no way to say which shapes were exposed, and a suspicious cell
can then be neither blamed on it nor cleared of it. Run 6 (-O1) had three
short greps in its first minutes and the exposure was settled from the cell
data instead — the anomalies were strategy-intrinsic, not a time window
([R2](#r2-is-the-ramp-detector-not-the-noise-detector)) — but that worked only
because the suspects sat at one roster slot on two shapes, which is luck and
not a method.

**After it lands:**

- analyse with `./read-run.py`, which is where every table in this file comes
  from — read [Reading the results](#reading-the-results) first, and do not
  write another reader;
- **gate on the correction, before reading anything else.** `--selftest`
  checks that the forcing term scales with `l` — one pass over the elements,
  not something whose size varies with the shape — and `--aa` prints both
  whether the two `sum-only` halves agree and how the term compares with the
  same pass measured in situ, off the `-nosum` arms. The three are independent
  and the correction needs all of them: position, size, and the read itself,
  each blind to what the others catch
  ([sum-only](#sum-only-and-the-correction-now-applied)). Any of them failing
  invalidates the whole time column rather than merely leaving it uncorrected,
  and all have to be re-passed by every run rather than inherited;
- walk the list under [Provenance](#provenance) of what the new numbers
  replace, and do not trust it to be complete: re-run the two sweeps it names
  and map each hit to the bullet covering it, since running the sweeps is not
  the same as reading them, and the list has been wrong before. **Replace;
  do not annotate.** Walking a list of what to replace makes "now X, where it
  was Y" the natural sentence, and a superseded number has to earn its place
  by the test in the user-scope `CLAUDE.md` — would someone redo the work
  without it — which most do not meet. `--check-doc` lists the ones already
  here for adjudication;
- **verify the write-up before deleting anything.** These are the checks the
  procedure used to leave to judgement, each of which has caught something:
  - **derive every count and ratio in the prose from `--cells`, never by
    eye.** "32 of 33", "30th of its 33 shapes", "the only two past 7%" are all
    claims a glance at a sorted table gets wrong; two of Run 6's were wrong
    until recomputed;
  - **reproduce any newly-derived column by a route that shares no code with
    the reader.** A four-bench filtered run carrying both `sum-only` halves
    takes seconds, and criterion's own printed `time` lines then give the
    ratio by hand: on `cnn-slice-c32`, `(1.506 - 0.1739) / (6.339 - 0.1739)`
    = 0.2161 against the reader's 0.216. Recomputing from `--cells` is worth
    doing too, but it shares the reader's arithmetic and cannot catch a wrong
    definition, only a wrong transcription;
  - **paste `--markdown`'s output over the Results table**; do not edit the
    table. It renders the same rows the terminal does, and carries `needs`,
    `precondition` and the emphasis forward from the table already there.
    Its stderr is the whole of what is left by hand: a row new to the roster
    comes out with `?`, a departed row is dropped with a warning;
  - **check that every `](#...)` resolves**, here and in `Main.hs`'s
    `README.md#...` references, and that every figure-bearing section is
    linked from the Provenance list. Findings rename headings, and a renamed
    heading breaks a link silently;
  - **read the document end to end.** The mechanical passes above do not catch
    a bullet contradicting the table three lines below it, which is how
    "`bq-mut` ties `bq-expand`" survived two runs beside a build ordering that
    refuted it. This is the pass that keeps finding real errors;

  Two conventions this page holds to, both of which exist because breaking
  them has cost something here. **A figure in prose names its run and its
  basis, or it belongs in a table with the prose pointing at it** — a bare
  numeral carries no provenance, and that is how one sentence came to put a
  Failed Run 6 figure beside a Run 6 one, and another to compare a *published*
  ratio with a *paired* one. **An anchor longer than about thirty characters
  goes reference-style**, defined at the foot of the file: inline it overflows
  the width and the rewrapping that follows is pure churn;
- rebuild and re-run `--lint` and `check` after editing `Main.hs`, even when
  only comments changed: the reader parses that file for the roster and the
  shape dims, so a comment edit can break a check that passed before it;
- record beside the numbers the run's name and regime, its stderr provenance
  line, which machine, **and the commit the binary was built from** (the JSON
  does not survive, so the source is the only thing that makes a run
  reproducible even in principle — this page's figures are one desktop's and
  are not portable, see [Provenance](#provenance));
- **only then** delete the JSON. The normal state of this directory is no run
  artifact at all, which is decided rather than an oversight; the numbers live
  in this file and the artifact does not. But "afterwards" means after the
  verification above, not after the writing: Run 6's artifact was deleted as
  soon as its write-up was drafted, which cost the ability to re-check
  anything needing the raw samples when the write-up was later questioned.

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
5×5 (LeNet), 11×11 (AlexNet); channels 1 up to 512; spatial from horde-ad's
6/24 to AlexNet's 55. The
`stretch-*` shapes are not conv-derived — extreme rank, extreme aspect
ratio, non-power-of-two dims, a cache-hostile innermost stride, a run
length of one element, a base-offset table as long as the result — to
probe the space beyond convolution. See `convShapes`/`stretchShapes`
in `Main.hs` for the full list.

**The conv set was halved after Run 6, and the eleven that went are not to
come back one at a time.** A strategy sees a shape as its innermost extent
`sInner`, its rank and its `l`, and nothing else — not which paper the dims
came from — and each dropped shape duplicated a kept one on all three while
costing a proportional share of every run. The freed wall clock went to A/A
controls, which calibrate every other figure and were the roster's scarce
resource. The ruling and the full reasoning sit at `convShapes` in `Main.hs`,
beside the list, along with the two shapes that must survive any later trim
for a reason unrelated to their workload: `gather48-src-50` and `conv1d-24`
are the only ones whose two innermost listed dims differ, which is what keeps
`check`'s `sInner` assertion from passing vacuously.

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

Run 6 (-O1): criterion, GHC 9.12.4, **-O1**, hardened harness (`env`,
`NOINLINE` on
the benchmark-facing functions, separate `check` mode); every strategy in one
process, so the figures are commensurable. 44 benchmarks over 33 shapes,
2h5m2s, peak 397 MiB in use and 134 MiB max residency, on the desktop named
under [Provenance](#provenance). -O1 is the regime a default `cabal build` of
orthotope compiles under today, which is why the record is taken there first;
Run 7 (SpecConstr) comes after it, and changes the answer for a whole class of
strategies rather than nudging it (below).

This is the first run whose figures have the shared forcing pass subtracted,
so **no figure here is comparable to one from any earlier run**, and Run 7's
will not be either unless it subtracts the same term
([sum-only](#sum-only-and-the-correction-now-applied) carries that decision).

**Comparing runs?** The table below is Run 6's own; what to hold a new run
against is [What Run 7 compares against](#what-run-7-compares-against), the
claims to test are [the ones after it](#the-claims-run-7-should-test), the
population and the absolute anchor are in [Provenance](#provenance), and
nothing under ~3% is a result.

How to read the columns:

- **time** is the geomean over shapes of the per-shape OLS *slope*, less that
  shape's forcing term, over `list`'s slope less the same term, with each
  strategy's single highest-CI shape dropped first. The trim
  matters: a 33-shape geomean divides ordinary noise by sqrt 33 but a lone
  wild cell by only 33, so one cell measured to +-70% moves the average more
  than all the well-measured cells together. Dropping one cell of 33 costs
  little and removes the larger error. The trim reads the *raw* CI%, as do the
  `CI%`, `smp` and `alloc` columns: subtracting a shared term moves a point
  estimate, it does not make a cell better measured.

  That choice was tested rather than assumed, and it is **not** free, so it is
  recorded here instead of being re-litigated. Reading the trim off the
  correction-relative CI% instead -- the half-width as a share of the *net*,
  which is larger, and most so for the fastest cells -- changes which shape is
  dropped for 4 strategies of 42 and moves their columns by +1.3% to +5.0%
  (`bq-gen-lemire` 0.498 to 0.523, the one past the floor); three of the four
  then drop `stretch-square-1341`, the run's worst-measured shape. Every other
  row is unmoved and no ruling on this page turns on any of the four. The raw
  rule is kept because measurement quality is a property of the measurement,
  and letting the correction pick the dropped cell would make the trim depend
  on the thing it is supposed to be independent of; the cost of keeping it is
  those four rows.

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
  rough pass and this run, where Failed Run 6's 35 shapes gave 27.67× and
  29.90×. So read `alloc` as a
  statistic of a strategy **and** a shape set, and pin the shape set before
  comparing it across runs, exactly as the `time` column already asks. It is
  the one column the correction does not touch.

| strategy | time | CI% | smp | alloc | needs | precondition |
|---|---:|---:|---:|---:|---|---|
| *sum-only-early* | *--* | *0.09* | *134* | *0.00x* | *the term every row has subtracted* | |
| *sum-only-late* | *--* | *0.07* | *134* | *0.00x* | *the same, at the other end* | |
| **mut-odo-vecdims** | **0.051** | 0.25 | 112 | 1.00x | new `Vector` method | |
| *mut-odo-vecdims-aa* | *0.052* | *0.19* | *113* | *1.00x* | *A/A control* | |
| mut-flat | 0.071 | 0.33 | 106 | 1.33x | new `Vector` method | `l < 2^32` |
| **bq-mut-runs-mulback** | **0.075** | 0.26 | 106 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-mut-runs-gm-mulback | 0.087 | 0.45 | 105 | 1.34x | mutable `Int` scratch | none |
| bq-mut-runs | 0.088 | 0.34 | 104 | 1.33x | mutable `Int` scratch | |
| **bq-scan-packed-mulback** | **0.097** | 0.15 | 104 | 2.00x | nothing (pure) | `l`, offsets < 2^32; m <= 2^31 |
| bq-odo-mulback | 0.104 | 0.13 | 103 | 3.45x | nothing (pure) | `l < 2^32` |
| mut-odo | 0.107 | 0.49 | 98 | 1.00x | new `Vector` method | |
| build | 0.108 | 0.51 | 99 | 1.00x | new `Vector` method | |
| bq-scan-rem-mulback | 0.121 | 0.13 | 100 | 4.34x | nothing (pure) | `l < 2^32` |
| bq-scan-mulback | 0.129 | 0.15 | 99 | 4.34x | nothing (pure) | `l < 2^32` |
| bq-mut-lemire-mulback | 0.130 | 0.49 | 98 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| **bq-scan-rem-gm-mulback** | **0.132** | 0.12 | 99 | 4.34x | nothing (pure) | **none** |
| *bq-scan-mulback-aa-distant* | *0.133* | *0.15* | *99* | *4.34x* | *A/A control* | |
| bq-mut-lemire-out | 0.134 | 0.38 | 96 | 1.33x | mutable `Int` scratch | `l < 2^32` |
| bq-expand32-lemire-mulback | 0.139 | 0.15 | 95 | 3.29x | nothing (pure) | `l < 2^32`; src < 2^31 |
| offtab32 | 0.139 | 0.82 | 96 | 1.50x | mutable `Int` scratch | src < 2^31 |
| bq-expand-lemire-mulback | 0.140 | 0.14 | 95 | 3.90x | nothing (pure) | `l < 2^32` |
| offtab | 0.141 | 0.95 | 96 | 2.00x | mutable `Int` scratch | |
| bq-scan-gm-mulback | 0.142 | 0.15 | 98 | 4.34x | nothing (pure) | `l < 2^32` (builder) |
| bq-expand-lemire-out | 0.142 | 0.15 | 95 | 3.90x | nothing (pure) | `l < 2^32` |
| bq-mut | 0.143 | 0.54 | 96 | 1.33x | mutable `Int` scratch | |
| bq-expand-b | 0.151 | 0.13 | 94 | 3.84x | nothing (pure) | |
| **bq-expand** | **0.155** | 0.14 | 94 | 3.90x | **nothing -- SHIPPED** | |
| *bq-expand-aa-adjacent* | *0.155* | *0.20* | *94* | *3.90x* | *A/A control* | |
| bq-expand-zf | 0.157 | 0.20 | 93 | 3.90x | nothing (pure) | |
| bq-expand-qr-prim | 0.158 | 0.15 | 94 | 3.90x | nothing (pure) | shape well-formed |
| offsets-quot | 0.223 | 0.51 | 87 | 6.68x | nothing (pure) | |
| mut-offsets | 0.266 | 0.51 | 87 | 7.57x | new `Vector` method | |
| fused | 0.300 | 0.68 | 84 | 10.68x | new `Vector` method | |
| bq-unfold | 0.310 | 0.34 | 82 | 10.23x | nothing (pure) | |
| offtab-scan | 0.319 | 0.30 | 79 | 11.00x | nothing (pure) | `l < 2^32` (builder) |
| bq-gen | 0.360 | 0.66 | 79 | 4.03x | nothing (pure) | |
| all-expand | 0.409 | 0.18 | 79 | 11.58x | nothing (pure) | |
| bq-gen-lemire | 0.498 | 0.72 | 71 | 3.37x | nothing (pure) -- refuted | `l < 2^32` |
| backperm | 0.522 | 0.51 | 70 | 17.06x | nothing (pure) | |
| cm-gather | 0.663 | 0.55 | 67 | 23.58x | nothing (pure) | |
| list (baseline) | 1.000 | 0.38 | 60 | 27.67x | -- | |
| unfold-add | 1.000 | 0.39 | 59 | 29.89x | nothing (pure) | |
| gen-quotrem | 1.087 | 0.75 | 54 | 13.00x | 1st attempt | |
| gen-unsafe | 1.087 | 0.65 | 55 | 13.00x | -- | |

`concat-runs` has no row: it is rostered and checked but no longer timed, for
the reason given with the strategy list above.

### What Run 7 compares against

The table above is a geomean over Run 6's 33 shapes, eleven of which are gone
([Provenance](#provenance)). **Do not compare a Run 7 figure with it.**
Restricted to the 22 that survive, untrimmed, Run 6 reads:

| strategy | published (33) | restricted (22) |
|---|---:|---:|
| `mut-odo-vecdims` | 0.051 | **0.051** |
| `bq-mut-runs-mulback` | 0.075 | **0.073** |
| `bq-scan-packed-mulback` | 0.097 | **0.097** |
| `bq-scan-rem-gm-mulback` | 0.132 | **0.128** |
| `bq-expand` | 0.155 | **0.144** |

The right column is the one to hold Run 7 against. The gap between the two is
population, not any strategy: the eleven dropped shapes skew small, and the
base-offsets build is a larger share of a small shape, so `bq-expand` loses
6.5% of its published figure and ratios between strategies move by up to ~6% —
both past the floor. A run that ignored this would read a shape-set change as
a code change.

And because a geomean cannot say *where* it moved, these two columns per
shape — the shipped strategy and the fastest pure one, net, against `list` —
are kept so a future disagreement can be localised rather than only noticed:

| shape | `sInner` | `l` | `bq-expand` | `bq-scan-packed-mulback` |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 0.219 | 0.137 |
| `cnn-L1-6x6-c1` | 3 | 324 | 0.300 | 0.133 |
| `stretch-rank12` | 2 | 4096 | 0.370 | 0.153 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 0.263 | 0.114 |
| `conv1d-24` | 3 | 5184 | 0.152 | 0.118 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 0.169 | 0.098 |
| `gather48-src-50` | 3 | 22500 | 0.143 | 0.114 |
| `stretch-rank10` | 3 | 59049 | 0.190 | 0.103 |
| `stretch-coprime-r7` | 13 | 60060 | 0.111 | 0.074 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 0.162 | 0.096 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 0.165 | 0.097 |
| `stretch-primes` | 89 | 250357 | 0.084 | 0.071 |
| `stretch-inner1` | 1 | 500000 | 0.188 | 0.134 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 0.080 | 0.055 |
| `vgg-14-c512-k3` | 3 | 903168 | 0.118 | 0.067 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 0.110 | 0.084 |
| `stretch-r5-8x432` | 8 | 1769472 | 0.059 | 0.049 |
| `stretch-square-1341` | 1341 | 1798281 | 0.108 | 0.135 |
| `stretch-bigstride` | 3 | 1800000 | 0.101 | 0.081 |
| `stretch-tab7MB` | 2 | 1800000 | 0.168 | 0.132 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 0.076 | 0.061 |
| `stretch-wide-2xM` | 2 | 1800000 | 0.159 | 0.129 |

Two rows to read first. `stretch-square-1341` is the only shape where the
fastest pure strategy *loses* to `bq-expand`, and it is the one the trim
drops for over half the arms — treat a disagreement there as the shape.
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.

### The claims Run 7 should test

Stated so a run can check each and report only the breaks. All hold on the
restricted basis above with a margin past the floor, the one tie marked:

1. `mut-odo-vecdims` < `mut-flat` < `bq-mut-runs-mulback` < everything pure.
2. `bq-scan-packed-mulback` ties `mut-odo` (1.4%, inside the floor) — the
   fastest pure strategy meets the class-method tier here, and this is the
   comparison the mutable-ceiling ruling turns on.
3. `bq-scan-mulback` < `bq-expand`, and `bq-expand-lemire-out` < `bq-expand`:
   both the scan build and the Lemire output beat the shipped strategy.
4. `bq-mut` < `bq-expand` and `offtab` < `bq-expand`: mutable scratch wins on
   time, which is the cost of `bq-expand` being pure.
5. `bq-expand` < `offsets-quot` < `bq-gen` < `bq-gen-lemire`: the build
   ordering, ending in Lemire losing at the build site.
6. `cm-gather` < `list` < `gen-quotrem`: the first attempt is still slower
   than the fallback it replaced, which is the whole reason this suite exists.
7. Allocation, median multiples of the result: mutable fills 1.00x, `bq-mut`
   1.33x, `offtab` and `bq-scan-packed-mulback` 2.00x, `bq-expand` 3.33x,
   `gen-quotrem` 13.0x, `list` 27.0x.

A break in 2 is expected under SpecConstr and is Run 7's point. A break in 6
would mean something changed in `list` or in GHC, not in a strategy — check
the anchor before anything else.

Two caveats on the columns. The `needs` tier for `backperm`, `cm-gather` and
`all-expand` is **doubtful**: each produces its result by mapping a concrete
`Int` vector into the abstract element type, and the class has no method for
that (`vMap` is `v a -> v b`), so on the reasoning that re-tiered `fused` they
may need a class method too. An equivalent `vGenerate` form exists -- that is
`offtab`'s shape -- so the strategies are not ruled out, only the labels
suspect. And the geomean weights every benchmarked shape **equally**, so a
figure here is a ranking statistic, not a claim about total work saved: the
small shapes count as much as the 4M-element ones.

### The noise floor is 3%, not the CI

Three A/A controls run an existing strategy twice under a second name. They
are the only rows whose true ratio is known to be exactly 1:

| pair | published | paired | mean per cell | span |
|---|---:|---:|---:|---:|
| `bq-expand` vs adjacent twin | 1.0012 | 1.0011 | 0.24% | 0 |
| `mut-odo-vecdims` vs its twin | 1.0066 | 0.9942 | 2.87% | 0 |
| `bq-scan-mulback` vs distant twin | **1.0309** | 1.0292 | 3.70% | 28 |

The middle pair's arms dropped *different* shapes, so its two columns are
geomeans over different shape sets and part company; the other two dropped the
same shape and differ only by the one extra shape the paired figure keeps. The
published figures are the right yardstick for comparing two rows of this
table, a reader of it computing exactly that; a margin measured per shape
belongs against the paired ones. `read-run.py --aa` prints both and says which
pairs differ.

**Nothing under about 3% is a result.** The CI% for those six rows reads
0.14-0.25%, so the interval understates run-to-run variability by roughly an
order of magnitude: it measures sampling error *within* one benchmark, while
two separately placed benchmarks also differ in code layout, cache occupancy
and inherited GC state. The A/A is the only column that sees that, and it is
what a margin should be compared against.

The floor grew with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a
real difference. On raw slopes these three pairs read 1.0010, 1.0031 and
1.0260, so the largest deviation was 2.60% before the correction and is 3.09%
after it. Correcting the table without correcting the floor would have been
the whole error.

That is a mechanism rather than an observation, so it was checked. Subtracting
a shared term scales a pair's deviation from 1 by `1/(1-f)`, `f` being the
term as a share of the arm — an identity *per shape*, and therefore worth
nothing until it has survived the geomean over shapes. It does, to within 0.01
percentage points on all three pairs: predicted 1.0010, 0.9943 and 1.0293
against observed 1.0011, 0.9942 and 1.0292. The amplification tracks `1/(1-f)`
arm by arm too — 1.497 against a predicted 1.487 on `mut-odo-vecdims`, 1.186
against 1.189 on `bq-scan-mulback`, and a looser 1.230 against 1.153 on
`bq-expand`, whose deviation is small enough that the ratio of two of them is
mostly noise. So the floor's growth is the correction's own arithmetic, not a
second effect riding along with it.

**One of Failed Run 6's two conclusions here is refuted; the other has merely
lost its evidence**, and the difference between those is the point. It held
that the floor tracks *1/time, not GC pressure*, and that *position is not the
cause* -- the
first because its noisier arm allocated 1.33x against the quieter one's 4.17x,
the second because its distant pair agreed better than its adjacent one.

*1/time* is **refuted**, with evidence rather than for want of it. Run 6 splits
the claim in two: per-cell *scatter* does track 1/time -- `mut-odo-vecdims`,
the fastest strategy and a 1.00x allocator, scatters 2.87% per cell where
`bq-expand` scatters 0.24% -- but scatter cancels, that pair's geomean landing
at 0.9942, and the floor is what survives cancelling. Ranked by published
deviation the three pairs read 0.12%, 0.66% and 3.09%, with the fastest arm
second and a mid-table one worst, which is not 1/time in any order.

*Position* is **not refuted, and not supported either**. What does not cancel
is a bias, and only the distant pair carries it: +2.9%, on a bench quieter by
CI% than either of the others. That is equally consistent with a position
effect and with a property of that one arm, because the re-aiming for Run 6
changed strategy and position together where Failed Run 6 had varied position
alone. The earlier exoneration has lost the run behind it, which is weaker
than being wrong: nothing licenses either verdict. The roster now crosses
three strategies against both slots, which decides it directly -- a bias
following the slot is position, one following the name is not.

Three A/A points remain a poor estimate of a noise floor. Their own published
spread -- 1.001, 1.007, 1.031 -- is the evidence that it is variable and
roughly 1-3%, so "~3%" is a soft threshold to compare margins against, not a
computed bound.

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
rather than merely noisy. In Run 6 (-O1) that is 4 cells of 1452, the worst
0.9857: `mut-odo` on the two smallest `cnn-L1` shapes, `build` on
`alexnet-L2-27-c48-k5`, and `bq-expand-lemire-out` on `stretch-square-1341`.

The two worst have a cause worth the space, because it is a method as much as
a finding. `mut-odo` carried the run's highest CI cell on both of those
shapes, while `build` -- the identical fill through `vBuildVS`, from a
different roster slot -- and `mut-odo-vecdims` -- the same fill with the
odometer's cons-lists replaced by unboxed vectors -- were clean on the same
two. Same shape, same process, so it is neither the shape nor a disturbance in
that stretch of the run: it is the odometer's list traffic as a GC ramp where
`l` is small enough for it to dominate, which is the cost `mut-odo-vecdims`
exists to remove. **Positional or strategy-intrinsic is the question to ask
first of any suspicious cell**, and `--cells` answers it cheaply: a
disturbance shows as a contiguous window of roster slots, a property of the
code shows as one slot across several shapes.

### sum-only, and the correction now applied

Every strategy is timed as `VS.sum . fb`, so every measurement carries the
same forcing pass; `sum-only` times that pass alone. It is a median 13.2% of
`bq-expand` and 2.7% of `list`, so an uncorrected ratio is compressed toward 1
by about that much and every margin read off one is an *understatement*.

**Run 6 (-O1) subtracts it, and every figure on this page is net of it.** The
run carried the pair the decision waited on -- `sum-only-early` and
`sum-only-late`, 40 benches apart -- and they agree: 1.0001 paired, 0.21% mean
per cell, worst cell 1.18%, against a floor of ~3%. The term is therefore
position-independent, which is the test the previous version of this section
set, and `read-run.py` now takes it per shape as the mean of the two halves
and divides net of it. `bq-expand` 0.179 becomes 0.155 and
`bq-scan-packed-mulback` 0.121 becomes 0.097, the first exactly the figure
that version predicted from Failed Run 6's numbers. That agreement is flat in
shape size as well as position -- regressed against `ln l` the halves' ratio
rises 0.1% across the whole 6250x range, which is a twentieth of its own
scatter -- so it is not a large-shape bias cancelling a small-shape one.

**The term now passes three gates, and it needed all three**, each blind to
what the others catch:

1. *Position*, the halves above.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape -- one sum over `l` elements -- and a term that were not
   could be wrong in both halves alike, leaving their agreement to notice
   nothing. It is: 0.588 to 0.608 ns per element across the whole shape set, a
   1.04x spread over that 6250x range of `l`, with the largest shapes 0.7%
   dearer per element than the smallest and no trend beyond that. `--selftest`
   checks it on every run and fails the run past a 1.5x spread.
3. *The read itself.* `sum-only` re-reads one **fixed** vector, where a
   strategy sums one its own fill has just written -- a different cache state,
   and the one thing neither gate above can see, since a term biased by it
   would be biased alike on every shape and in both halves. This is what
   `bq-expand-nosum` and `mut-odo-vecdims-nosum` are for: each is its base arm
   run again and forced with a single element instead of the sum, so *base
   minus arm* is that sum in situ. Measured against `sum-only` they read
   **0.990** and **1.008** -- within 1%, on the two arms where the term is the
   smallest and largest share of the bench (an eighth of `bq-expand`, a third
   of `mut-odo-vecdims`), so the test spans the range over which a bias would
   matter. They also *bracket* 1, where a systematically warmer fixed-vector
   read would have put both on one side of it. Per-cell scatter is 4.2% and
   4.3%, worst on `stretch-square-1341` as usual.

So the second of the two reasons the previous version gave for withholding the
correction -- that the term's own accuracy was unproven -- is answered rather
than outstanding. What backs it is a 20-minute probe of seven arms over the
whole shape set, not a full run: the `-nosum` arms sit adjacent to their bases
precisely so the difference survives a different process around it.

Two things follow, and both contradict the reasons that version gave for *not*
publishing it.

- **It is not comparable to anything.** Every earlier figure on this page and
  in `Main.hs` was uncorrected, and Run 7's will be unless it subtracts the
  same term. This is the cost the decision was taken with open eyes; the
  uncorrected column is still one `--exclude sum-only-early --exclude
  sum-only-late` away, and `read-run.py` says on stderr when it is reading
  one.
- **It does change ordering**, where that version argued it could not.
  `(B+S)/(A+S) < 1` exactly when `B < A` holds *per shape*, but the column is
  a geomean over shapes after a trim that drops a different shape for
  different strategies, and neither step preserves the argument. Three
  adjacent pairs swap: `bq-mut-runs-gm-mulback` with `bq-mut-runs`, and
  `offtab` past `bq-scan-gm-mulback` and `bq-expand-lemire-out`. All three
  swaps are inside the floor, so no ordering the page treats as real moves --
  but the reason as stated was wrong, not merely unnecessary.

What remains open is narrower than the objection was: the `-nosum` pairs price
two arms, not forty-four, so a fill whose write pattern leaves the cache in
some quite different state could still be summed at a cost `sum-only` misses.
Two arms an octave apart in speed agreeing to 1% makes that unlikely rather
than impossible, and the arms are in the roster so every run reprices them.

A one-shape smoke run had said as much before the run did: on `cnn-slice-c32`
at `-L1` the halves read 169.9 ns and 170.1 ns, 0.12% apart.

### Provenance

Run 6 (-O1) is the run every figure above and below comes from: the whole
roster over the whole shape set at criterion's default budget, one process,
2h5m2s, built from commit `db1b20b` with a clean tree. Its stderr provenance
line reads *roster 44 benchmarks over 33 shapes;
elapsed 2h5m2s; peak 397 MiB in use, 134 MiB max residency* -- comfortably
inside `micro.cabal`'s `-M2G`, which is why that note still stands unchanged.
Its JSON is not kept, by the rule above; the commit is what remains of it, and
is here because a run whose artifact is deleted and whose source is unrecorded
cannot be repeated even in principle.

It is a fresh baseline rather than a continuation of Failed Run 6, on two
counts that compound. The shape set moved first: every shape over `sizeCap`
was cut to it or moved to `tooBig` (`stretch-tab16MB` became
`stretch-tab7MB`, `stretch-square-1400` became `stretch-square-1341`,
`stretch-r5-8x512` became `stretch-r5-8x432`, `stretch-wide-2xM` and
`stretch-tall-Mx2` kept their names on smaller dimensions, and
`vgg-28-c256-k3` and `resnet-stem-112-c3-k7` are flagged rather than run), the
single `sum-only` bench became a pair, the A/A controls were re-aimed, and
`concat-runs` stopped being timed -- exactly the roster changes this page's
own noise-floor section says to pin before comparing across runs. Then the
correction landed on top, which alone would have severed the comparison.

Every figure here was measured on one desktop — Zen 3, a Ryzen 7 5800X, the
same machine whose `idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
None of it is portable, so a run elsewhere is a different measurement rather
than a repetition, and should say which machine here.

**And the ground has moved again since.** The conv set was halved and the
roster gained five arms — three A/A controls completing the crossed design,
and the two `-nosum` arms. So Run 7 stands to Run 6 exactly as Run 6 stood to
Failed Run 6, for the same two compounding reasons: a different shape set
makes `alloc` and `time` statistics of a different population, and a different
roster makes every bench share a different process. Neither change is a
defect — each bought something this page names — but a figure here and a
figure from Run 7 are not two measurements of one quantity, and the ratio
between them is not a result.

**The delta, so the population is recoverable.** What follows is the *only*
form in which a shape set or roster is recorded here: its difference from
whatever `Main.hs` holds now. A snapshot would need rewriting at every change
and would be a second copy of a list that already exists; a delta costs what
actually moved and shrinks to nothing when the two agree.

- Run 6 measured today's shapes **plus eleven since dropped**:
  `cnn-L1-12x12-c1`, `cnn-L2-12x12-c16`, `cnn-slice-c64`, `lenet-L2-14-c6-k5`,
  `mnist-28-c1-k3`, `cifar-L1-32-c3-k3`, `cifar-L3-8-c128-k3`,
  `cifar-32-c3-k5`, `vgg-14-c256-k3`, `deep-7-c512-k3`, `slice-c512`.
- Run 6's roster was today's **minus five arms**: `bq-expand-aa-distant`,
  `mut-odo-vecdims-aa-distant`, `bq-scan-mulback-aa-adjacent`,
  `bq-expand-nosum`, `mut-odo-vecdims-nosum`.
- Its trim dropped `stretch-square-1341` for 24 of the 44 arms; the remaining
  20 drops fell on 16 other shapes. That asymmetry is why two published
  columns can differ from their paired ratio, and it is the shape to expect
  the same of next time.

**The anchor, so a moved baseline is visible.** Every published figure is a
ratio to `list`, so a change in `list` itself — a new compiler, a new machine,
a changed `toListT` — rescales the whole table while leaving every ratio
intact and undetectable. These three absolute per-call figures are the guard,
all on shapes that survive:

| shape | `l` | `list`, per call | net of the forcing pass |
|---|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.06 µs | 5.89 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.68 ms | 3.59 ms |
| `stretch-wide-2xM` | 1800000 | 37.6 ms | 36.5 ms |

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.587–0.608 ns per element across the whole set, median
0.604, so a raw slope is the published one plus about `0.60e-9 * l`, with `l`
from `Main.hs`. That recovers any uncorrected figure to within the term's own
3% spread — enough to hold Run 6 against Failed Run 6, or against any number
measured before the correction existed.

**What the next run replaces.** Run 6's numbers reach past the Results table,
so this is the list to walk when Run 7's land. It names *sections*, not
figures: a list of figures is a second copy of them, and enumerating it was
how the previous two versions of this list went stale — one missing six
sections, its predecessor leaking past it. What now guarantees completeness is
mechanical instead. Every section below is reached by an anchor, and the
coverage check is: no section carrying a figure outside a table may be absent
from these links. Run that check, and repeat the two sweeps it cannot replace
— grep this file for figure-shaped numerals outside the tables, and grep it
for `Run 6` — before trusting the list.

- [the Results table](#results), which `--markdown` emits whole;
- [What Run 7 compares against](#what-run-7-compares-against) — the restricted
  geomeans and the two-column per-shape fingerprint, both of which a run
  replaces wholesale, and which are the only per-shape record kept once the
  JSON is deleted;
- [The claims Run 7 should test](#the-claims-run-7-should-test), where a run
  reports which held rather than re-deriving them;
- [the noise-floor table][floor] and its prose, from `--aa` — including the
  raw-slope triple it compares against, and the crossed-control design that
  Run 6 could not supply;
- [the opening section][opening]'s headline ratios;
- [What the table says](#what-the-table-says), where every bullet is a run
  figure;
- [The mutable ceiling (not taken)](#the-mutable-ceiling-not-taken) and
  [Why there is no gen-lemire](#why-there-is-no-gen-lemire). These two are
  *rulings resting on figures*, so a stale number re-opens a decision rather
  than merely misreporting one — and a ruling's number moves for reasons its
  verdict does not. Every decision-bearing ratio was checked in both columns
  when the correction landed: none changed direction, but magnitudes moved by
  up to +31%, because subtracting a shared term inflates a ratio the more the
  arms it compares are fast. Requote from the run; do not carry forward;
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
- [What the next run has to decide](#what-the-next-run-has-to-decide), whose
  whole content is questions a run answers and figures a run moves;
- this section, which becomes the next run's own provenance;
- `read-run.py`'s docstring, whose `time`, `corr` and `net` definitions and
  A/A paragraph quote the run;
- `micro.cabal`'s `-M2G` note, if the printed heap peaks have moved;
- `Main.hs`, wherever a comment cites a figure — `roster`, `expandCost`,
  `baseOffsetsScan`, `fbFused`, `fbOffTab32`, `fbOffTabScan`,
  `fbBQscanMulback`, `fbBQscanRemGmMulback`, `fbBQmutRunsGmMulback`,
  `fbMutOdoVecdims`. `concat-runs`' figure there is Failed Run 6's and stays,
  the bench being untimed since, so no run replaces it.

**And what a run does not touch.** The converse of that list is worth stating,
because a session told to make a run will reach for everything: a new
measurement bears on figures and on rulings whose figures moved, and on
nothing else. It does not bear on the *reasoning* behind a decision, on the
ideas recorded as having died on paper, on the shape-set and roster rulings,
or on the account of how the fix was found. Those change when an argument
changes, which a run is not. If a run seems to call for rewriting one of them,
that is a finding worth its own paragraph, not an edit to be folded in
quietly.

How a run is made, and what to record beside its numbers, is [Making a major
benchmark run](#making-a-major-benchmark-run) — which is also where the walk
of the list above is one of the steps.

Four rows are not comparable to runs before Failed Run 6, all from strictness
fixes that moved code toward what its comment already claimed:
`bq-scan-packed-mulback` and the two Granlund-Montgomery arms (a lazy tuple in
`gmMagic`), and `fused`, whose per-step state thunk had been inflating its
allocation -- 20.7x before the fix, 10.68x here.

## Reading the results

### The reader: read-run.py

Every figure below comes out of `read-run.py` in this directory, and the
table above is *emitted* by it rather than copied from it. **Use it; do not
write another reader.** The
definitions it encodes — which cell the trim drops, that `CI%` is a mean
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
    ./read-run.py RUN.json --drops          # what the trim removes, by shape
    ./read-run.py RUN.json --aa             # controls, spans, in-situ term
    ./read-run.py RUN.json --cells          # every cell as TSV, for the rest
    ./read-run.py RUN.json --selftest       # check the reader's own invariants
    ./read-run.py RUN.json --exclude concat-runs --exclude-shape deep-7-c512-k3
    ./read-run.py --lint                    # Main.hs's roster, against README
                                            # and against itself

`--markdown` renders the same rows the plain table does, from one shared
call, so the published figures cannot drift from the terminal's. It reads the
Results table already in this file for the two columns a run cannot know —
`needs` and `precondition` — and for which rows the prose emphasises, carries
those forward, and says on stderr what it could not: a strategy new to the
roster comes out with `?` to be written by hand, and one that has left it is
dropped with a warning. The `bq-expand-nosum` and `mut-odo-vecdims-nosum` arms
are in exactly that state until a run at this optimisation level times them.

**No run artifacts are kept here.** The normal state of this directory is no
JSON at all, and one is made when a question needs it — which is the same
moment the reader is wanted, so it is built to be useful on a partial run as
well as a full one:

    micro --json RUN.json                                    # the whole thing
    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

The second takes seconds and still exercises the reader; a one-shape run says
so and skips the trim rather than dividing by an empty set. A filtered run
like it carries no `sum-only` bench, so its figures are uncorrected and not
comparable to the tables here — the reader warns on stderr when that is what
it is reading. Run 6 (-O1)'s JSON is gone with Failed Run 6's, so the tables
in this document cannot be re-derived; the next run replaces them.

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
as one pass over the elements must, that the trim drops exactly one
shape per strategy and lands inside its own per-shape range, that `list`
against itself is 1, and that an A/A pair dropping the same shape from both
arms has its published ratio equal to its paired one. The one thing it still
cannot reach — that `sInner` is the second-to-last listed dim — it now names
as `check`'s rather than as nobody's. It names what it could
not exercise
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
  `concatMap` (`bq-expand`, 0.155) is beaten by the explicit mutable fill
  (`bq-mut`, 0.143) and beats the lazy list (`offsets-quot`, 0.223),
  `unfoldrExactN` (`bq-unfold`, 0.310) and `generate`+per-run-quotRem
  (`bq-gen`, 0.360).
  The list route pays for a non-fusing cons-list of thunks; `concatMap`
  builds the separable grid inside vector's stream framework instead. So
  `bq-expand` is the fastest build that needs neither a class extension nor
  explicit mutation.
- **`bq-mut` beats `bq-expand` on time and allocates far less** (1.3× vs
  3.9× the result) — a mutable `Int` scratch vs `concatMap` intermediates
  — at the cost of explicit mutation; `bq-expand` is the pure choice. The
  margin is 7.9%, outside the floor: this bullet used to say *ties*, which
  contradicted the build ordering above it in the same section and was wrong
  against Failed Run 6's own table too, not only against Run 6's.
- **The `bq-expand` variants add nothing in the geomean, and `bq-expand-b`
  adds a lot on two shapes.** `bq-expand-zf` (zip and fold fused into one
  recursion) and `bq-expand-b` (first-dim special-case) tie `bq-expand` over
  the shape set — 1.0% behind and 2.9% ahead, both inside the floor — and for
  `bq-expand-zf` that is the whole story: the zip list is only rank-1 long and
  `foldl'` is already well-tuned, so there is nothing to gain.
  `bq-expand-b` is different, and Run 6 refutes the claim that it ties *on the
  shapes chosen to separate them*: it is 24% ahead on `stretch-inner1` and 22%
  on `stretch-wide-2xM`, its two best cells by a wide margin and the only two
  past 7%. Both are rank-2 views with one huge outer dimension, which is
  exactly where seeding from `enumFromStepN` replaces the entire `concatMap`
  build rather than saving one step of it — a structural reason, so read those
  cells as the design showing through and not as scatter. `bq-expand` is still
  what shipped, on the geomean and on being the plainest form, but the
  special-case is not the no-op this bullet used to call it.
- **Lemire's multiplicative inverses win at one division site and lose badly
  at the other** — the section below tells that story in full.
- **`gen-quotrem` (the first attempt) is still slower than `list`** (1.087)
  — the mixed picture, reproduced: one `quotRem` per *dimension* per
  element costs more than the list's allocation on the shapes that matter.
- **Allocation:** `bq-expand` allocates ~3.9× the result vector (`concatMap`
  intermediates over the `m`-element base-offsets); `offsets-quot` ~6.7×
  (the cons list); the direct mutable fills ~1.0× (just the result); `list` ~28×
  (thunks). Lower allocation tracks lower time across the table. Read each as
  a median over *this* shape set, per the `alloc` column's own caveat.

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

**At the per-element output site it wins**, by 7.4%.
`bq-expand-lemire-out` is `bq-expand` with the shared `i quotRem sInner`
replaced, the table build held at `baseOffsetsExpand`. It was the fastest pure
strategy when written and Run 6 has since put eight pure ones ahead of it, but
the substitution itself still pays: faster than its control on all but one
shape, and the published columns agree with the per-shape geomean, so no part
of it rests on the warm-up ramp. The exception is `stretch-square-1341`, the
run's worst-measured shape and the one the trim drops for over half the
benches — read it as the shape, not the strategy. Two controls back the
result. Its allocation is identical to `bq-expand`'s on every shape, which is
what a build-identical arm must show; and it runs *before* `bq-expand` in the
group where `bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot bias
would flatter one and penalise the other and cannot produce both.

**At the per-dimension build site it loses by 40%.** `bq-gen-lemire` is
`bq-gen` with the per-run, per-rank `quotRem`s replaced, and it is 1.401×
slower, faster on one shape of the set. The shape of the loss says why: it
tracks *rank*, not element count, rising from about a tenth at rank 2 to about
a half at rank 12. The cost is paid per
dimension, so the division was never what dominated there. Two reasons.
(i) The paper's win assumes you want a quotient *or* a remainder; an odometer
decomposition wants both, so the trick pays twice and collects once — where
`quotRemInt#` is one `idiv` yielding both. (ii) The magic table is a third
list to walk in step with `nts` and `sts`, adding a dereference and a pattern
match per dimension to the very loop whose per-dimension work was the target.
Rank 2 costs least because there is only one dimension to walk, though not
nothing, as an earlier run had it.

What separates the two sites is (i) and (ii): at the output the divisor is a
loop invariant, so `M` is computed once for the whole fill with no list beside
it, and the per-element work really is one division against two multiplies.
The win is 7.4% rather than several-fold because the hardware has moved since
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
Fixing that is what turned the output site from a 2% curiosity into the win it
now measures, and it recovered part of the build site's loss too — enough to
see,
nowhere near enough to reverse it. Why the low half must not be recomputed is
recorded as a comment on `fastQR`, so the loose form is not written again.

**On shipping it.** `bq-expand-lemire-out` is pure, so the argument that kept
`mut-odo` out does not apply; what it costs is `MagicHash` and `UnboxedTuples`
in `Data/Array/Internal.hs`, about a dozen lines of helper, and a
precondition. The precondition is the substantive part: Lemire's identity
holds for `d, n < 2^32`, and `n` here is the linear output index, so a shipped
version needs an `l < 2^32` test choosing between the two fills —
loop-invariant and chosen once per call, but it must be there, since orthotope
does not otherwise cap array length. Weigh 7.4% against that; this
benchmark's job is to price it, not to decide it.

### Why there is no gen-lemire

**Don't write it.** A third such benchmark is easy to specify and is
deliberately absent: `gen-lemire` would be `gen-quotrem` with its
per-dimension divisions replaced by `fastQR`, standing to it exactly as
`gen-unsafe` does. That is the form the idea is most naturally proposed in —
inverses of the array sizes, plural, one per dimension — and it is the form
the two measurements above already refute, which is why it stays unwritten
rather than being tried again.

It looks promising because `gen-quotrem` trails `bq-expand` by 7.0× while
differing chiefly in dividing once per *rank* per element, and because a
per-dimension decomposition needs no base-offsets table and so promised the
mutable fills' ~1× allocation while staying pure. Both grounds fail against
figures already in the table.

1. **The same substitution loses at the sibling site.** `bq-gen-lemire` is
   structurally what `gen-lemire` would be, per run rather than per element,
   and it is 1.401× *slower* with a loss that grows with rank. A per-dimension
   cost that rises when a division becomes a multiply says the division was
   never the per-dimension cost; `gen-lemire` differs only in paying that same
   cost once per element instead of once per run.
2. **The output site caps the prize at 7.4%**, measured at the friendliest
   division in the suite, which does not close a 7.0× gap. Most of that gap is
   not division at all: `gen-quotrem` walks two `[Int]` lists per element, and
   Lemire adds a third to walk.
3. **The allocation ground is inverted**, not merely unproven: `gen-quotrem`
   and `gen-unsafe` allocate 13.0× the result against `bq-expand`'s 3.9×, so
   dropping the table costs allocation rather than buying it.

The bounds-check control is what makes point 2 safe to assert: `gen-unsafe` is
`gen-quotrem` minus the bounds checks and buys nothing (0.06% apart), so the
gap is arithmetic and bookkeeping, not indexing. That tie is Run 6's and
settles a disagreement this page carried for two runs, Failed Run 6 having put
the pair 2.7% apart — just outside its own floor, which would have left the
control saying something rather than nothing.

A `gen-lemire` surviving all three would still lose, because its ceiling is a
design already beaten: the base-offsets family pays one division and one table
read per element against rank-many divisions *plus* rank-many list steps, so
even a free division leaves the walking.

## Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes — chosen
to push past the ranges the rest cover, and named here without their prefix —
against the strategies nearest the decision, each as a multiple of `list` on
the same shape. These are Run 6 (-O1)'s own figures, all of them net of the
forcing pass like the rest of the page:

| shape      | bq-expand | bq-expand-b | lemire-out | mut-odo | vecdims |
|------------|----------:|------------:|-----------:|--------:|--------:|
| inner1     |     0.188 |       0.143 |      0.166 |   0.237 |   0.097 |
| rank12     |     0.370 |       0.370 |      0.363 |   0.293 |   0.096 |
| wide-2xM   |     0.159 |       0.124 |      0.144 |   0.152 |   0.067 |
| coprime-r7 |     0.111 |       0.111 |      0.096 |   0.051 |   0.034 |
| primes     |     0.084 |       0.084 |      0.071 |   0.025 |   0.028 |
| tall-Mx2   |     0.076 |       0.076 |      0.061 |   0.020 |   0.025 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which is
the axis the orderings turn on; the fuller per-shape record is
[above](#what-run-7-compares-against).

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is where the expansion family does best against
  the odometer fills: `bq-expand` (0.188) and `bq-expand-b` (0.143) beat
  `mut-odo` (0.237) and `build` (0.235), which they do on no other shape here.
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
  slots. They no longer do. `bq-mut-runs-gm-mulback` and `bq-mut-runs-mulback`
  take that shape at 0.030, `mut-flat` at 0.032 and `mut-odo-vecdims` at
  0.097, all ahead of every expansion variant — strategies that did not exist,
  or were not rostered, when the claim was written. The unit innermost extent
  still explains why `mut-odo` and `build` do badly there; it never implied
  that no mutable fill could.
- **Per-shape figures are far noisier than the geomean: trust the first
  digit only.** Independent runs of these shapes agree within 1–5% on most
  cells but differ by up to 27% on `stretch-inner1/bq-expand-b` — runs
  whose rosters also differed, making the
  [roster effect above][floor] a candidate cause — and the order of
  `bq-expand{,-b,-zf}` within their sweep of `stretch-inner1` flips between
  runs. The sweep itself reproduces; which of the three leads does not.
  `stretch-square-1341` is this run's standing warning on the point: it is
  the one shape where `bq-expand-lemire-out` loses, and the trim drops it for
  over half the arms. That strategy's own margin is the exception surviving
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
  averages: `bq-scan-packed-mulback` reads 0.134 there against a 0.097
  geomean, 30th of its 33 shapes, while `bq-mut-runs-mulback` reads 0.030
  against 0.075 — its best cell of all 33. Read that cell first and average it
  away last.

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
That is `mut-odo` (0.107) and `build` (0.108) — ~1.45× over `bq-expand` —
and `mut-odo-vecdims` (0.051), which is 3.03× over it and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.141) does not go that far — its output is an ordinary
`vGenerate` and only its `l`-sized `Int` offset table is filled mutably, so it
needs no class method, just a mutable scratch — and Run 6 puts it 33% behind
`mut-odo` for it, where Failed Run 6 had the two tied at 0.148. On these
numbers it is no longer the cheap way to most of the gain.

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
Run 6 raises the stake again rather than settling it: `mut-odo-vecdims` shows
the fill's real cost was the odometer's cons-list traffic, not the fill
itself, taking the class-method tier to 3.03× over `bq-expand`, where Failed
Run 6 read 2.4× and the run before it ~1.4×. Against that, the best pure
strategy now reaches 0.097, so the gap the class method would buy is 1.89×,
not 3.03× — the figure the ruling turns on, and the one that has grown each
run.

## The C-gap: still a deeper ceiling

**Everything in this document lives under this ceiling.** Every strategy in
the table, every ruling resting on one, and every margin the ~3% floor
adjudicates are rearrangements *within* pure Haskell — and no pure-Haskell
strategy closes the gap to the stride-aware C kernels, roughly an order of
magnitude on comparable traffic: horde-ad's concrete *scatter* routes through
them and runs the analogous chain in ~0.5 ms where the fastest gather strategy
here is several ms. The table spans a range narrower than the step it does not
take, so read this section before the Results one.

Regime 3 has no contiguous runs to hand a bulk kernel, so the transfer stays
per-element in Haskell however the fallback is written. Closing it needs C, by
one of two routes this benchmark cannot price:

- an **upstream strided-copy kernel** in ox-arrays' cbits, serving every
  client of the fallback;
- the **client-side add-zero gather**, rebuilding gather on the scatter model
  so the C arith kernels do the densifying — priced against a `scatter48`
  bound a later orthotope fix largely measured away, so its arithmetic needs
  redoing before it is proposed again.

`bq-expand` is the pure win to take meanwhile, not a replacement for it.

## What the next run has to decide

The open questions, each with the measurement that would settle it, collected
here because they otherwise sit one per section and get reconstructed every
time.

- **Does position move a bench, or was that one arm?** Run 6 found a +2.9%
  bias on its distant control and could not attribute it, its distant slot
  holding a strategy its adjacent slot did not. The roster now crosses three
  strategies against both positions, so `--aa` decides it directly: a bias
  that follows the slot is position, one that follows the name is not.
- **Ship `bq-expand-lemire-out`?** It is worth 7.4% and costs an `l < 2^32`
  dispatch plus `MagicHash`/`UnboxedTuples` upstream. Nothing further needs
  measuring; this is a judgement someone has to make.
- **Does SpecConstr invert the scan family?** `baseOffsetsScan` boxes its
  stream state at -O1 and is predicted allocation-free at -O2, which would put
  `bq-scan-mulback` at 1.33x allocation and the fastest pure time. That is
  Run 7's whole point and nothing here has tested it.
- **Is the ~3% floor real or an artifact of three points?** Six controls now
  replace three; if the spread stays, the floor is a property of the machine
  rather than of the sample.
- **Does the halved shape set move the geomean?** It should not — the eleven
  dropped shapes each duplicated a kept one on `sInner`, rank and `l` — but no
  run has confirmed that, and the first run on the new set is the one that
  can, by comparing the strategies whose ordering the trim never touched.

## Further ideas

One pure-Haskell item is open and not listed under
[what the next run decides](#what-the-next-run-has-to-decide), because no run
bears on it: tightening *regime 2* (innermost-normal, not exercised here) with
a `toVectorT` folding the contiguous runs directly rather than building the
intermediate run list. Being pure Haskell it sits under the
[C-gap](#the-c-gap-still-a-deeper-ceiling) like everything else here.

The rest of this section is ideas that **died on paper**, recorded so they are
not re-proposed:

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
  -- the natural reading of `bq-mut-runs` beating `bq-mut` by 39% -- cannot be
  checked here. It needs a timing mode alongside `diag`'s allocation one,
  using the fixed-iteration differencing the horde-ad performance model
  prescribes (`-n 200` minus `-n 100`, fresh processes) rather than criterion,
  since the builders are not benchmarks.

[floor]: #the-noise-floor-is-3-not-the-ci
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[opening]: #regime-3-micro-benchmark-the-fix-bq-expand
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
