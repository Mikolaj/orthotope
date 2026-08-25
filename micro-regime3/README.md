# regime-3 micro-benchmark (the regime 3 fix)

This branch (`speedup-strided-tovector`) changes `toVectorListT`'s regime-3
fallback in `Data/Array/Internal.hs` --- the per-element path taken when
the innermost dimension is strided, so no contiguous run longer than one element
can be sliced out. What the branch carries in code is the stage-one fix, landed
2026-08-24: `vFillStrided`, the class method, its shared driver a bang-for-bang
port of `mut-odo-vecdims-add-in-leaf-u2`; **the regime 3 fix is decided:
on 2026-08-22 `mut-odo-vecdims` was decided as the implementation to go
upstream, on 2026-08-24 the stride-conditioned redirect that had kept
the decision open was dropped, and the same day the arm was refined
to the family's `add-in-leaf-u2` form on the two paired probes recorded
in the ceiling** --- [the ceiling](#the-mutable-ceiling-taken) carries
the decision and what it rests on, and [the two-stage
plan](#the-two-stage-plan-and-the-rework-proposal) below carries the drop
and the rework proposal the redirect's evidence now feeds.

The previous attempt, benchmarked as `gen-quotrem` resulted in a **mixed
picture**: it had replaced the original `list` fallback

    [vFromListN l $ toListT sh a]                       -- build/foldr list

with a `vGenerate` over a per-element `quotRem` (one division *per dimension*),
which sped up the large, many-channel shapes but *slowed* the small, shallow,
high-rank shapes that dominate horde-ad's convolutions (up to ~2x).

The fix now in `Data/Array/Internal.hs` is **`bq-expand`**: precompute
the base-offset of each innermost run once --- the outer-base grid is separable
(`o0 + sum idx_d * stride_d`), so it is built by iterated `concatMap` /
`enumFromStepN` expansion, no division and no thunk-list --- then fill
the result with a single `vGenerate` doing **one** `quotRem` per element.
It beats the original `list` fallback on every benchmarked shape
with no regression and needs no extension to orthotope classes.

**A direct mutable result buffer is faster still**: `mut-odo` walks the outer
odometer and writes each innermost run, and `mut-odo-vecdims` --- the same fill
with its dimension lists replaced by unboxed vectors --- is on Run 18
(SpecConstr, -A32m) **2.09x** over `bq-expand` paired. Its family holds the top
of the table, and which member leads is not settled: `mut-odo-vecdims-add-in`
reads **0.9813** against it on Run 18's 9.12 half --- add-in the faster, at 19
wins of 24 and sign p 0.0066, the two printing 0.054 and 0.055 --- **and 1.0016
at 14 of 24 and p 0.54 on the 9.14 half of the same pair**, a coin flip
on the wrong side of 1, which is the first reading to make the lead a property
of the compiler rather than of the arm. So it is not a tie the sort settles:
it is a lead on one compiler and absent on the other. It has [its own
entry][open], a mechanism in the machine code and no settled magnitude. Both
need a new `Vector`-class method, which was measured and deliberately
**not** taken, to keep orthotope's `Vector` API pure and minimal --- a bar
an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-taken), amended). Plain `mut-odo` no longer argues
for it at all: it and `bq-expand`, the arm `Data/Array/Internal.hs` carries
today, are a tie at 0.9059 paired, 12 shapes of 24 and sign p 1 on an interval
covering 1, where Run 7 (Harness), at -O1, had it 1.51x ahead.

**Several strategies measured since are faster than the last candidate,
`bq-expand`, and need no class method --- a distinction the decision
of 2026-08-22 retires, shipping the mutable family's arm instead.** The fastest
pure ones on Run 19 are **`bq-scan-rem-gm-mulback`** (0.098)
and **`bq-odo-gm-mulback`** (0.100) against `bq-expand`'s 0.115 --- a margin
of **1.16** and **1.15** paired, exactly Run 18's, where Run 17 read 1.17
and 1.16, Run 16 1.18 and 1.14, Run 13 1.14 and 1.15, Run 12 1.13 and 1.14, Run
11 1.15 on each and both halves of Run 10's pair 1.13 to 1.14. So it
is no longer a margin sitting inside the 1.22 that placement alone is worth
in an unaligned build, to be read as a candidate rather than a verdict:
alignment removed that term, and a run repeating Run 10 exactly --- same binary,
same roster, same order --- reproduces the margin to a hundredth ([the yardstick
table](runs/run19.md#what-the-next-run-compares-against)). They also carry
**no size precondition at all**, which is the point of them, a ruling since
having stopped this suite timing any arm that needs one ([what the benchmark
does](#what-the-benchmark-does)). Neither is what `Data/Array/Internal.hs` does
today. Of the trade-offs, allocation and a noise floor this run measures
at 2.32% across the eighteen A/A pairs of the half the table comes from,
and 1.71% across the eighteen of the other half of its pair,
are in [Results](runs/run19.md#results), each arm's precondition is at its entry
in `Main.hs`'s roster, and the division sites are in [the Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites).

Every figure in this README is **net of the shared forcing pass** every strategy
is timed through, which Run 6 (-O1) is the first run licensed to subtract
([sum-only](#sum-only-and-the-correction-now-applied)). That makes none of them
comparable to a figure from an earlier run, or to one from a later run that does
not subtract it.

Every figure is also **one population's**. The measured ones above are the main
set's --- the positive-stride views a merged transpose builds --- while
the regime-3 views the library's other operations produce (reversed, broadcast,
sliced, windowed, scaled) are the [stride
classes](#the-stride-classes-and-what-they-cover), each its own population, run
in its own process and tabled beside the main set rather than folded into it.

And **one regime's**, **one roster's** and now **one layout's** as well. Runs 8
through 11 all compiled the suite with `-fspec-constr`, where every run before
them took the plain -O1 a default `cabal build` of orthotope takes, and the flag
reorders the table rather than nudging it --- it speeds `list` itself by 8%,
`bq-expand` by 27% and the plain scan family by 31%. The 19% it was also said
to *cost* `mut-odo` is not the flag's: `build` compiles to the same worker
and moved 17% the other way, which identical code cannot do, and the pad probe
has since priced that disagreement as placement ([the floor section][floor]).
Every figure in this sentence crosses a rebuild and so carries some of the same
term; the three that survive it do so by being larger than it. Run 9
then changed the roster and nothing else, and moved arms from 9% faster to 19%
slower with the baseline standing still; Run 10 changed only the roster's
*order* and moved them 3% faster to 14% slower, and then measured the layout
term directly by running the same source from two binaries that differ in where
its loops sit --- 12 to 14% on the two arms whose loop straddled a cache line,
and a percent or two the other way on everything else. **Run 11 then changed
nothing at all**, re-running Run 10's aligned binary, and moved every arm
but one by under 1.5% and `list`'s worst cell by 4.3% ([the floor
section][floor]) --- which is what the three figures above have to be read
against, and is a quarter of the band that was available before the layout could
be held still. So a figure here belongs to a flag, to a membership, to an order
*and* to a layout, and the last is the one this README can now remove rather
than only price. **Whether orthotope should carry the flag library-wide
is not this README's question** and is deliberately not on its open list:
that decision is about compile time and code size across the library,
and the measurement that would settle it is horde-ad's `convVjpBench`
over a real build. The 27% is what this README contributes to it. **At module
scope it is settled (2026-08-24): the shipped file does not set
`-fspec-constr`**, the aligned HEAD probe having read the flag irrelevant
to the shipped family ([the ceiling](#the-mutable-ceiling-taken)),
and `-fspec-constr` stays the regime every claim below is read in rather
than a probe of one.


### The two-stage plan and the rework proposal

**Decided 2026-08-24: the fix ships in two stages, and the stride-conditioned
redirect is dropped rather than deferred.** Stage one is what goes upstream now,
landed on this branch 2026-08-24: `vFillStrided` with its driver, the vecdims
family's `add-in-leaf-u2` arm --- refined from plain `mut-odo-vecdims`
by the two paired probes the ceiling records --- for regime 3 alone,
with no condition on the strides --- the prototype this replaces, a compound
strategy with `mut-odo-vecdims` as the main element and one to three per-shape
or per-stride redirects around it, is dead. Stage two is a proposal, recorded
here and committing nobody: a later rework of `toVectorListT`'s whole dispatch,
all regimes, whose own evidence is what killed the redirect --- it shows
the redirect's constituency dissolving at the dispatch, and what remains
of regime 3 after it is stage one's arm, so the fix taken now may prove
to be the whole of regime 3 in the rework too.

**The redirect's measured constituency is unit dimensions and zero strides,
not stride classes.** [The ceiling](#the-mutable-ceiling-taken) names every
place an outside-family arm leads `mut-odo-vecdims`: the `reshape1` class,
`stretch-inner1`, `window-64x64-k1x9`, `bcast-tall-Mx2`
and `stretch-pow2stride`. All but the last are views with a unit innermost
extent or a zero stride --- and both properties mark work the fallback need
not do at all, where a redirect to a flat table arm still does all of it,
and at `sInner` 1 pays twice the result vector in allocation for a table as long
as the result.

**The proposal's first half: canonicalize the view before the regime dispatch
--- drop unit dimensions, then merge adjacent dimensions where
`st_outer == n_inner * st_inner`.** Both rewrites preserve the row-major element
sequence exactly --- a unit dimension contributes `0 * stride` to every index
whatever its stride, and the merge condition is the index sum's own
distributivity, sign-agnostic, so it fires on `rev` views too --- and both
are O(rank) integer work on the two lists the dispatch already holds.
The regimes are then classified on the canonical dims: `reshape1-*`
and `stretch-inner1` become regime 1 outright, since `simpleReshape` gives
an appended unit dim stride 0 over data that was dense and in order all along,
which `mkReshape1`'s comment has said since the class was built;
`window-64x64-k1x9` becomes canonical regime 2, contiguous runs of 9;
and the conv patch tensors stay regime 3 at lower rank, `cnn-L2-24x24-c32`
falling from rank 5 to 3. After unit-drop no regime-3 view has `sInner` 1 ---
only the scalar case, already special-cased --- so the flat table arms lose
their constituency structurally, not behind a predicate.

**The second half: specialize the zero strides inside the one remaining fill,
as conditions on the odometer rather than strategies beside it.** A zero
innermost stride (the `bcast` class) hoists the run's one read and stores
a register; a zero outer stride (`bcastmid`, any broadcast axis) fills the block
below that level once and block-copies it `n - 1` times, zero levels composing
since the topmost fires and the ones below fall inside its one filled block;
a canonical innermost stride of 1 (`window`) makes the run body a contiguous
copy. All three share the vecdims odometer, chosen once per call outside
the loops.

**A scratch probe priced the proposal, and its timings are anecdotal
by this README's standards --- magnitudes only, nothing finer.** The instrument:
in-process fixed-iteration differencing at -O1 `-fspec-constr` and -A32m, each
arm correctness-gated against a naive per-element reference, on a box carrying
about one core of foreign load; only reads past 1.5x were kept,
and those reproduced across two processes within about 20%. Against a verbatim
`mut-odo-vecdims` port: the `reshape1-500k` analog falls from about 2 ms to tens
of nanoseconds, the regime-1 return being O(1) --- the work is removed,
not shrunk --- where the redirect's own leader on that shape reads about 1.6x;
`window-64x64-k1x9` reads 6.6x with the contiguous-run copy where `mut-flat-gm`,
the redirect's candidate there, reads 1.3x; the hoisted read pays 1.7x at run
length 2 and about 5x at 1800; the block copy about 8x on a `bcastmid` analog.
The two controls canonicalization cannot touch --- `stretch-primes` exactly,
`cnn-L2-24x24-c32` up to its merge --- read ties, so the pass costs nothing
where it does nothing.

**One reclassification is not free, and it bounds what canonicalization may do
alone.** Promoting the window view into today's regime 2 --- the slice-per-run
list `toVectorT` then concatenates --- read a tie with `mut-odo-vecdims` on time
and 4.59x the result vector on allocation, some 260 bytes of slice header
and list per nine-element run. So the rework takes promotion to regime 2 only
together with a direct run-copy fill, or leaves short-run canonical-regime-2
views on the regime-3 arm; promotion to regime 1 is the one reclassification
free by itself. And that bound shapes the master plan for extending the rework
to regimes 1 and 2, ruled 2026-08-25: dispatch work and one consumer route,
never per-regime strategies. Canonicalization moves in front of the WHOLE
classification, in `toVectorListT` itself: regime 1 then admits every view whose
canonical strides are natural --- and is untouched past that, being already
the optimum, the backing handed over --- and regime 2's normal-suffix test reads
canonical dims, so a unit dim's arbitrary stride no longer truncates the maximal
slice and a view that hands back six slices today can hand back one.
`toVectorListT`'s slice list itself stays, for the consumers that use it
as a list, iterating without concatenating; what changes is `toVectorT`,
the one-vector consumer, which routes canonical unit-stride views through
the driver's contiguous-run copy instead of slices-plus-concat --- one branch
of `vFillStrided`, not a strategy, the branch `canon-memcpy-r2` times
and the tie above is the case for. All of it lands in `Data/Array/Internal.hs`'s
dispatch and `toVectorT`; the class method and its instances do not move again.
What stays open is only whether a NATIVE regime-1/2 input differs
from a regime-3 view that canonicalizes into those shapes; nothing here can
exercise one, and the question earns work only if `toVectorT` over native
regime-2 views shows up hot in horde-ad.

**On allocation the proposal never leaves the 1.00x tier and twice goes
under it** --- and these figures are exact, allocation being deterministic per
call. The hoisted read and the block copy allocate the result and single-digit
bytes more; canonicalization's own transients stay under two unpinned kilobytes
per call, 1.01x on the smallest probed view and vanishing on the megabyte ones;
and the regime-1 hits allocate about 470 bytes against `mut-odo-vecdims`'s 4.0
MB on the `reshape1-500k` analog --- minting no pinned buffer at all where every
materializing arm mints one, the small-pinned currency
of `small-pinned-churn-investigation/`, whose tax lands on later code and which
no per-call fit prices. The flat table redirect this replaces pays 2.00x
on the same shapes.

**The class method is decided, 2026-08-24: the whole-kernel pure-typed form, one
method for both stages --- and no `Mutable` associated type in orthotope's
`Vector` class, which would change orthotope too much.**
`vFillStrided :: VecElem v a => ShapeL -> [Int] -> Int -> Int -> v a -> v a` ---
shape, strides, offset, length, source --- is shaped as `vGenerate` is,
the mutation hidden inside each instance. Its class default is the pure
`bq-expand` form in existing methods, so the `[]` reference instance and any
instance outside the tree compile unchanged; the three vector-backed instances
override with one shared driver written against `Data.Vector.Generic`, whose
`Mutable` already exists where it belongs and whose copy primitives hand
Storable the memcpy for free. Stage one implements that driver as the family's
`add-in-leaf-u2` arm; stage two upgrades the driver's internals ---
canonicalization, the zero-stride conditions, the run copies --- with no further
change to the class. Rejected the same day, so they are not re-proposed:
a `vCreate` handing the callback the mutable buffer, which is what would need
the `Mutable` associated type; the per-element `vBuild` alone, which cannot
express a block copy or a contiguous-run copy and so buys a second method later;
a CPS extension handing the callback write-and-copy functions, which avoids
`Mutable` but is more surface than the whole-kernel form for the same wins;
and the FastReshape `unsafeCast` escape, an instance-side trick
with no `Storable` evidence at the generic call site. One debt travels
with the choice: the `build`/`mut-odo` identity was dumped
for the single-callback `vBuild` form, so the driver's workers are
to be re-dumped in this form before any figure of theirs is trusted. Nothing
else couples the stages: post-canonicalization every population this README
measures keeps the vecdims family at its head, the one residue being
`stretch-pow2stride`'s 10%, which is cache aliasing and [the
C-gap](#the-c-gap-still-a-deeper-ceiling)'s to close.

**The rework's arms enter the roster for Run 20, and Run 19 was stage one's
as planned** --- it rostered nothing new, which is what let its pair price
a compiler and nothing else. **TAKEN 2026-08-25, and the alternative
it was weighed against is gone**: a roster change and a placement pair cannot
ride together, and the placement pair was owed for the `add-in` question alone,
which is now [parked][open]. So the arms are in, and Run 20 has no purpose-built
pair left to owe. They are five --- `canon-vecdims` and its memcpy-run form
`canon-memcpy-r2`, the zero-stride conditions `bcast-set` and `mid-copy`,
and the endpoint `canon-full`, with `canon-full-nosum` beside them as the fourth
in-situ forcing control --- against the four pieces the proposal describes:
the composite canonicalizing arm, the hoisted-read fill, the block copy
and the contiguous-run copy. **The parking paid for them nearly exactly.**
The three placement-family arms whose only live question it was ---
`mut-odo-vecdims-add-out`, `-add-both` and `-add-both-down` --- drop to `Only`
the same day, so they stay checked against the reference on every shape and stop
costing benches, and the timed roster goes up by three rather than by six. They
are new functions, so Run 20 is the stronger pinning test the rider
under [Recommended tasks](#recommended-tasks-after-run-19) waits for;
and its write-up should expect `reshape1` to go degenerate for the composite
arm, whose cells there would measure dispatch rather than filling, so the class
wants a non-collapsing sibling --- a `[n, 1]` view over a strided source ---
to stay discriminating.

**Weighed and dropped within the proposal, so they are not re-proposed
with it:** tiling for the page-aliased stride (10% on one probe shape whose own
comment bounds damage rather than ranking); size thresholds in the dispatch
(nothing measured needs one after canonicalization, and the no-precondition
ruling stays whole); normalizing strides at view construction (observable
through the API, so the pass stays local to `toVectorListT`); and algebraic
shortcuts in reductions over broadcasts (the consumer's business,
not this fallback's).


## Contents

History is not here. `MARGINALIA` beside this file is a write-only journal
and not something to read: it exists because the models working here keep
putting history inside instructions, and it is where that goes instead
of into this README. It is not a `CHANGELOG`, which would face users. What
this README keeps is the rule and, where an editor might plausibly undo it, one
clause saying what undoing it cost.

Thirty-odd sections, so the map is here rather than left to a grep.
It is anchors and paths, not line numbers, on purpose: `--check-doc` verifies
that every anchor in both documents resolves and that every path into `runs/`
names the current run, so this list cannot rot silently, where line numbers
would be wrong by the next edit and say nothing. The last entry but one leaves
this file: **a run's own numbers are in `runs/run<N>.md`**, one file per run,
superseded by the next run's file beside it rather than edited into it.
That directory is not the history this section opens by refusing --- it holds
measurements, which are what a run makes, where `MARGINALIA` holds
the chronology of how the instructions got here.

- [The two-stage plan and the rework
  proposal](#the-two-stage-plan-and-the-rework-proposal)
- [What is settled, and where](#what-is-settled-and-where)
- [What is open](#what-is-open)
  - [Recommended tasks after Run 19](#recommended-tasks-after-run-19)
  - [Non-urgent TODO list](#non-urgent-todo-list)
- [The goal of these benchmarks](#the-goal-of-these-benchmarks)
  - [How the strictly positive picture
    was achieved](#how-the-strictly-positive-picture-was-achieved)
  - [Where the shapes come from](#where-the-shapes-come-from)
  - [The shape set](#the-shape-set)
  - [Dropping the minibatch dimension](#dropping-the-minibatch-dimension)
  - [The stride classes and what they
    cover](#the-stride-classes-and-what-they-cover)
  - [The scratch vector flavour](#the-scratch-vector-flavour)
  - [One element type, and what the probe
    found](#one-element-type-and-what-the-probe-found)
  - [Lemire multiplicative inverses, at the two division
    sites](#lemire-multiplicative-inverses-at-the-two-division-sites)
  - [Per shape, where the geomean hides
    the ordering](#per-shape-where-the-geomean-hides-the-ordering)
  - [The fix in Data/Array/Internal.hs](#the-fix-in-dataarrayinternalhs)
  - [The mutable ceiling (taken)](#the-mutable-ceiling-taken)
  - [The C-gap: still a deeper ceiling](#the-c-gap-still-a-deeper-ceiling)
  - [Dead ideas](#dead-ideas)
- [About the current harness](#about-the-current-harness)
  - [What the benchmark does](#what-the-benchmark-does)
  - [Running it](#running-it)
  - [Making a major benchmark run](#making-a-major-benchmark-run)
  - [Other toolchains, probed and not run](#other-toolchains-probed-and-not-run)
  - [The reader: read-run.py](#the-reader-read-runpy)
  - [What moves a figure when no strategy
    changed](#what-moves-a-figure-when-no-strategy-changed)
  - [R2 is the ramp detector, not the noise
    detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now
    applied](#sum-only-and-the-correction-now-applied)
- [Run 19](runs/run19.md)
  - [Results](runs/run19.md#results)
  - [What the next run compares
    against](runs/run19.md#what-the-next-run-compares-against)
  - [The claims the next run should
    test](runs/run19.md#the-claims-the-next-run-should-test)
  - [The stride classes, run
    by run](runs/run19.md#the-stride-classes-run-by-run)
  - [Provenance](runs/run19.md#provenance)
- [Provenance](#provenance), README's own


## What is settled, and where

**One line per thing this README has established, and the section that holds
it.** It exists because the file is long enough to re-derive itself:
the `build`/`mut-odo` Core identity was dumped, diffed and drafted as a new
finding, and found afterwards to have been recorded at [the mutable
ceiling][ceiling] since Run 8, a thousand lines from where the session
was working. Read this before deriving anything and grep it before writing
anything up.

**It carries no figures, and that is the design.** A figure here would
be a second copy of one kept elsewhere, which is how two versions
of [Provenance][prov]'s replace list went stale before it was rewritten to name
sections rather than numbers. Each entry names a subject and a home and stops;
the numbers live at the home and move with the run. An entry earns its place
by being a thing a later session might otherwise redo.

- **The `bq-expand` fix** and why the base-offsets table is built by expansion
  rather than by division: [the fix][fix], with the four findings behind
  it in [how the picture was achieved][achieved]. That form is now the last
  candidate: the decision of 2026-08-22 is [in the ceiling][ceiling].
- **The mutable ceiling**, why a direct mutable fill was not taken for eleven
  runs, the amendment that turned that bar into a weight, and the decision
  of 2026-08-22 that takes it --- `mut-odo-vecdims` as the upstream
  implementation, refined on 2026-08-24 to its `add-in-leaf-u2` form and landed
  in code the same day, alone since the drop that sent the stride-conditioned
  redirect to [the two-stage plan](#the-two-stage-plan-and-the-rework-proposal)
  as a rework proposal: [the ceiling][ceiling].
- **The class-method signature is free** --- `build` and `mut-odo` compile
  to the same worker, dumped in both regimes --- so no `vBuild` is held back
  on a figure: [the ceiling][ceiling].
- **Code placement moves figures**, and by more than the A/A controls can see:
  the identical-code pair, the rebuild bias, the per-loop reading
  and the cache-line table are all [in the floor section][floor]. **Straddling
  a cache line is a cost and not a correlation** --- the pad probe stepped two
  arms through every offset --- **and the penalty is graded** by where the split
  falls: same section. **But it is not the account of every gap it once seemed
  to explain**: Run 10 read three arms at four placements each and two of them
  kept their 16% with no copy straddling anywhere, which is what withdrew
  a suspension [the ceiling][ceiling] had placed on its own figures. The probe's
  own design, including the two kinds of pad that relocate nothing, is [on
  the open list][open] with what is still open about placement.
- **GHC's native backend aligns no loop**, where GCC, clang and GHC's own LLVM
  backend all do; `-fproc-alignment=64` pins the offsets rather than choosing
  them, and an assembler shim on `-pgma` aligns the loops outright, which
  is the instrument fix. What it costs and buys in time is [on the open
  list][open]; the rest is [in the floor section][floor], including why the shim
  must pad only between instructions. Two tools beside this file:
  `loop-offsets.py` reads a binary's copies, which makes the question a minute's
  work rather than a run's, and `align-as.py` is the shim; a paired run's two
  binaries are built from the recipes its own note carries, one per half. Both
  this and the recompilation trap beside it are written up and filed as GHC
  issues from horde-ad's `docs/`, which is where a reader outside this README
  should go; what stays here is what they cost this benchmark.
- **Which arm owns a loop copy is a property of the binary**, absent
  from a plain build and carried by a `-g3` one, which `loop-offsets.py` now
  reads for itself --- and **a `-g3` build is a twin to read and not a binary
  to time**, that having been gated and lost. The map of the vecdims group,
  the reading of Run 11's split it corrected, and what `-g3` costs in emitted
  code and in time are [on the open list][open].
- **The allocation area moves figures too** --- the default nursery against
  an arm's allocation in excess of its result --- with the predictor
  and the populations it reaches [in the floor section][floor]; and since
  2026-08-21 it is fixed at `-A32m`, here and in every horde-ad suite, never
  to vary again ([Running it](#running-it)).
- **The A/A controls are the noise floor**, not the printed CI, and what they do
  and do not bound is [in the floor section][floor]; R^2 is the ramp detector
  rather than the noise detector, [here][ramp].
- **Run-to-run drift, with shapes, roster, order, regime and layout all
  pinned**, measured for the first time by re-running one binary: a few percent
  per cell, a quarter of a percent on a geomean, and two arms that exceed it,
  [in the floor section][floor].
- **The forcing pass is subtracted from every figure**, on three gates
  that every run and every population re-passes, and gate 3's standing bias:
  [sum-only][correction].
- **`alloc` is deterministic per call** and is a statistic of a strategy
  *and* a shape set, so pin the shape set before comparing it: the column
  definitions under [Results][results].
- **Which strategy wins is decided by the innermost extent**, not by the rank
  and not by the element count, which is what the geomean hides: the `sInner`
  ruling, [per shape][pershape].
- **Division is priced at two sites**, and which multiplicative-inverse form
  survives which regime: [Lemire][lemire].
- **The element-type restriction is evidenced**, the ranking holding at four
  types: [the probe][probe]. **The scratch vector's flavour** severed
  comparability at a known point: [there][scratch].
- **The roster is cut by two rulings** --- a size precondition disqualifies
  an arm, and so does allocating past a bar --- and a majority of the roster
  is checked without being timed: [what the benchmark does][bench].
- **The shape set was halved and is not to grow back one shape at a time**: [the
  shape set][shapeset], the ruling itself beside `convShapes` in `Main.hs`.
- **The stride classes are separate populations**, tabled beside the main set
  and never merged into it: [the classes][classes].
- **Ideas that died on paper** are recorded so they are not re-proposed: [dead
  ideas][dead].
- **Pure Haskell cannot close the gap to the C kernels**, which bounds every
  strategy here: [the C-gap][cgap].
- **How a run is made and analysed**, including what a run does *not* touch:
  [the procedure][procedure], [the reader][reader] and [Provenance][prov].
- **What is open** is the chapter directly below, this index's complement, each
  question carrying the measurement that would settle it and what needs a quiet
  machine: [the open list][open], with the harness's own backlog folded
  in under [the TODO list][todo]. Nothing open is recorded anywhere else.


## What is open

**The complement of the index above, and read with it.** That one says what
is settled and where; this says what is not, each question with the measurement
that would settle it and the run that can supply it. Between them a session
knows what it must not re-derive and what is worth deriving, which is the pair
the file opens with rather than the two lists it used to end its chapters with.

**Every entry opens with its status, so that finding the live ones is a grep
and not a reading, and `--check-doc` fails the file for an entry that does
not** --- which it would have until 2026-08-22, seven of the non-urgent list's
thirteen entries having carried no token at all and four of those being closed,
saying so in prose where nothing could find it. `OPEN` wants a measurement
that is available; `PARKED` is open but its route is retired, and the entry says
why; `ANSWERED` records an outcome and is kept so the question
is not re-proposed; `STANDING` is a ruling or a convention with nothing to run.
`grep -E '^(- |[0-9]+\. ).OPEN.' README.md` is the list of live questions,
and the one that answers a session's first question about this section ---
the alternation being there because *Recommended tasks after Run N* numbers
its items where both lists bullet theirs, so a bullet-only pattern reads
that subsection as empty rather than as clean. The status is a pointer and never
the authority: the entry's own text is.

**An `ANSWERED` entry owes three things and not a fourth: the question as
it was asked, the outcome, and the section that holds the account.** This
is a question register, and what it keeps an answered question for
is that nothing else records a refutation --- [What is settled,
and where](#what-is-settled-and-where) names what is true and the topical
chapters carry the figures, so a question deleted here is one the next session
re-proposes. What it must not become is a second copy of the chapter: that index
says of itself that it carries no figures by design, for the same reason,
and an answer that runs to a chapter puts the account in the one
of this README's three places that does not move when a run does. The shape
to copy is the `window` overlap entry below, which states its outcome
in a sentence and ends by naming the block that carries its figures.
`--check-doc` FAILS the file for any `ANSWERED` entry past five hundred words
--- it listed until 2026-08-23 and gates now that nothing is left to judge,
with three truthful ways out that the failure itself names: move the account
to the section that owns it, give a run registration the family's lead, or say
in a bolded clause carrying `only copy` that there is nowhere to move it.
That last is what makes a gate honest rather than coercive,
`bq-scan-packed-mulback` being the live case of an answer nothing else records;
the entries already past it are the backlog that rule was written over, and they
are to be shortened as each is next touched rather than in one pass. **Length
is the whole test, and it was not**: the rule also asked that the entry point
nowhere, which sounds like the same thing and is an off switch, this README
cross-referencing constantly enough that every long entry names a link or a file
--- so the sweep listed none of the fourteen entries past three hundred words,
and exempted an eighteen-hundred-word summary for naming the files
its measurements are in. **The one exemption is the registration family**,
matched on the lead its members share --- *What Run N was built to answer* ---
and counted rather than dropped, the sweep's own line saying how many it passed
over. They earn it by the ruling below and not by their length: a registration
is the only copy there is. A member that drifts out of that phrasing loses
the exemption and gets listed, which is a failure a reader can see; Run 10's had
drifted, its lead saying *predictions* where its own text calls them
registrations, and was normalised back.

**The run registrations are the standing exception to it, and reducing the old
ones is REFUSED --- 2026-08-22, on reading two of them.**
`What Run N was built to answer` arrives once a run and none has ever left,
which makes the family the one part of this section that grows on a schedule;
cutting the older ones to a verdict and a pointer was the obvious answer
and the pointer has nowhere to aim. The run's file is replaced every run,
and the yardstick keeps one geomean per strategy per half --- where
a registration's answers are half-against-half and control readings
that no table here carries: Run 11's `list` scatter of 0.958 to 1.043
and its two-and-two max-skip split, Run 16's 35 arms of 42 inside 1.5%. So they
are not long entries that failed to point but the only copy there is. The length
rule happens to pass them by, every one of them pointing somewhere as well;
where one does not, this ruling is the authority and not the rule.

**The spent run registrations are not here, and where they went is the half
a removal owes.** Runs 10 to 16's went to `MARGINALIA` on 2026-08-23, verbatim
and whole --- Run 12's last, and only once its status was corrected, having
been held back by a stale `OPEN` that its own third item had contradicted since
2026-08-13. They were answered, every finding of theirs already lives
in the topical section its entry points at, and what they still cost
was this list: a run registration is exempt from the 500-word ceiling, so five
of them had grown to chapter length and every grep of this section paged through
all five. **The last two runs' stay.** A stale marker does not merely mislead,
it exempts --- which is why `--check-doc` now holds a registration's marker
to its own items. The rule going forward is that a registration leaves when
it is answered and two further runs have reported --- and that `MARGINALIA`
is write-only, so what leaves is gone from working use rather than merely moved.

**This is the only home for an open question.** They are collected here because
otherwise they sit one per section and get reconstructed every time ---
and worse, get missed: the question of why the count-down FastReshape form pays
was raised inside [the mutable ceiling][ceiling]'s own write-up and never
migrated, so a session that mined this list and its queue walked past it ---
migrated into the FastReshape-axes entry below on 2026-08-14, the example
standing because it is the reason for the rule. A question recorded anywhere
else is a bug to be moved here, not a note to be left where it was written.
The harness's own backlog is folded in below, for the same reason: two backlogs
a thousand lines apart is how one belongs to neither.

**Run 9's question closed as unanswerable by this design, and the ruling is what
this entry keeps: roster and layout move together, so no run that changes
the roster can separate them.** The membership change moved one arm 9% faster
and its own code-twin 19% slower, which identical code cannot do; the separation
had to come from the pad probe, which holds membership fixed and has since
priced layout alone at 1.16 to 1.19 on a shared loop ([the floor
section][floor]). One residue outlives the rest: the regime probe left `bq-gen`
11% slower in absolute time with its allocation collapsed to the table's ---
which neither the `diag` nor the Core accounts for, and the placement question
below inherits.

**And it raised a larger one in the same breath, which was then answered
the same day.** *What warms the expansion family?* On `vgg-14-c512-k3`,
`bq-expand` and three arms beside it run 35--40% slower in a small process
than at their published roster slots, reproducibly, while the scan and mutable
families do not move at all --- the largest effect this README has measured
that is not a strategy, and it lands on the **`bq-expand`** arm. A dozen probes
settled it: not GC time (5.8% of the cold process), but the **default 4 MB
nursery** against an arm allocating 13.2 MB per call beyond its result, warmed
by exactly one predecessor --- `sum-only-early`, whose one-off `l`-sized setup
allocation grows the block pool and leaves it grown. A nine-point `-A` sweep
shows a larger nursery rescuing the *cold* arm, and shows `-A1G`'s cliff to
be a collision with the `-M2G` cap rather than the nursery. The account is [in
the floor section][floor], and it carried **a roster fix, since applied twice**:
`sum-only-early` moved first from slot 5 to slot 2, ahead of the three distant
A/A twins, which were being calibrated against a colder heap than everything
they calibrate --- on that roster the 41% cell reads 0.24% --- and then, for Run
10, above `list` as well, which is the warm-up bench [the TODO list][todo] had
been asking for and leaves nothing measured on an ungrown pool.

  **It was answered the same day, and the decision it forced is kept
  with the account** --- **and SUPERSEDED on 2026-08-20, Run 16 having moved
  the published basis to `-A32m`**, so what follows is the reasoning that
  held while the default area was the basis and not a live instruction:
  keep the default area, and carry the caveat that
  the headline ratios are partly a statement about it ([the floor
  section][floor], which also holds the predictor for which cells the
  setting reaches, and the nine populations it has been applied to).
  What stays open is the size of it --- how much of a published geomean
  moves is a run and not a probe.

**Three of Run 8's were answered the same day**, each by the probe its own entry
specified --- the rule about a discriminating measurement deserving one now
rather than a slot in the next run, observed again:

- `ANSWERED` **`bq-scan-packed-mulback` gets worse because SpecConstr gives
  its control, for free, exactly what the packing was hand-rolled to buy ---
  and the packing keeps charging for it.** Dumped in both regimes from Run 8's
  commit (2026-08-08, `-dsuppress-all -dsuppress-uniques`), the two arms' table
  builds differ like this. At -O1 the control's loop carries its state
  as a boxed `Either` of a boxed pair of a boxed `Int`, allocating a `Right` per
  step --- the 72-bytes-an-entry the law at `baseOffsetsScanPacked` records ---
  while the packed arm unwraps one `I#` and is otherwise unboxed, which
  is the 21% lead it held there. Under `-fspec-constr` both loops specialise
  to four raw arguments and *neither* boxes: the control's `Either`, pair, `I#`
  and its per-step allocation all vanish, and the packed arm loses only its one
  `I#` unwrap. What survives on one side and not the other is the packing's own
  arithmetic --- `uncheckedIShiftRA# ... 32#` and `andI# ... 4294967295#`
  on every element, against the control's two plain `+#` --- so the flag pays
  off the debt the packing existed to avoid and leaves the packing's interest
  still due. Hence cheaper (1.33x on both) and slower (1.11x on 24 shapes
  of 24).

  **Two consequences. The law at `baseOffsetsScanPacked` is confirmed
  in its constructive half and its corollary refuted**: every state shape does
  unbox under the flag, but "indistinguishable from its control" does
  not follow, because unboxing removes the control's cost and not the packed
  arm's. The `diag` behind all of this was re-measured in Run 8's own regime
  and every figure quoted above reproduces, including the controls that say
  the instrument did not move; what it adds is that `baseOffsetsScanPacked` goes
  3.00x to 1.00x, so under the flag even the boxed `Int` in `unfoldrExactN`'s
  emit pair --- which the -O1 reading called out of reach of any state shape ---
  is gone. And the packed representation is now known to be a **-O1-only**
  optimisation: wherever SpecConstr runs it is strictly dominated by the plainer
  arm it was built to beat. That was written as a thing to settle before
  the flag question, and the flag question has since been answered against
  it --- every claim here is read under `-fspec-constr`, so the packed form
  is not a candidate here at all. **The Core account above is the only copy,
  and there is nowhere to move it:** the dead-ideas list takes ideas that died
  on paper and this one was built, rostered and measured, and the roster entry
  in `Main.hs` records the arm's size precondition rather than this ruling.
  Recorded so the move is not proposed a second time.

- `ANSWERED` **It does not generalise to the other hand-packed arms, and why
  not is the useful half.** Three benchmarked pairs differ from their control
  in a hand-managed compact representation and in nothing else, and the flag
  moves all three differently. The -O1 column is a ratio of published columns,
  that run's artifact being gone; Run 8's is paired, and the last two columns
  are each arm's own absolute per-call move:

  | arm / its control | hand-packed how | -O1 | Run 8 | arm | control |
  |---|---|---:|---:|---:|---:|
  | `bq-scan-packed-mulback` / `bq-scan-mulback` | loop state, two fields in one `Int` | 0.789 | **1.113** | 1.022 | 0.724 |
  | `bq-expand32-lemire-mulback` / `bq-expand-lemire-mulback` | the `m`-length table at `Int32` | 0.983 | **0.949** | 0.729 | 0.756 |
  | `offtab32` / `offtab` | the `l`-length table at `Int32` | 1.136 | **0.877** | 0.940 | 1.218 |

  **Hand-packing survives the flag exactly when what it buys is something
  the specialiser cannot buy.** The packed state buys unboxed loop state, which
  is SpecConstr's own job, so the flag hands the control the same thing
  for nothing and leaves the packing holding its shift and mask. The two `Int32`
  tables buy heap footprint, which SpecConstr has no opinion about, and the Core
  says so: their distinguishing operations --- two `intToInt32#`,
  a `writeInt32Array#`, no boxing --- are identical in the two regimes,
  as are their controls', so the `expand32` pair barely moves. The `offtab32`
  pair moves furthest of the three and not for its packing at all: its arm
  improves 6% while its *control* regresses 22%.

- `ANSWERED` **The element-type ordering still follows `Storable Double`.**
  [That section's](#one-element-type-and-what-the-probe-found) own re-probe
  trigger is a run that moves the ordering at `Storable Double`, which Run 8
  does, so all four types were re-run under the flag: the ranking is unchanged
  at every one of them, `bq-expand`'s `worst` stays between 0.245 and 0.267,
  and the column's arithmetic check reproduces to the digit. The figures
  are in that section beside the -O1 ones. What the re-probe does not settle
  is the question behind the trigger --- whether the flag's reordering
  is an `Int`-arithmetic effect or an element-width one --- since the ordering
  it moved is among the roster's arms and not among the types.

**What Run 10 leaves open**, each with what would settle it:

- `ANSWERED` **What does code placement cost?** **A rebuild is worth up to 18%
  on a susceptible arm and 0.5% on the baseline** --- the largest effect
  this README has measured that is not a strategy --- **and for a loop this size
  placement costs 1.16 to 1.19** (2026-08-10, the pad probe). Susceptibility
  is a property of the arm: the baseline has almost none and two arms have
  a great deal, and they are the same two the flag sets back hardest. What
  the probe does not reach is the rest of it --- a rebuild moves more than one
  loop's offset, and the regressions with no shared-loop counterpart have
  no mechanism. The four binaries, the readings they explain and the graded
  penalty are in [the floor section][floor].
- `STANDING` **The queue of experiments that want a quiet machine**, ranked,
  so that the next quiet window is not spent deciding what to spend it on.
  Written down 2026-08-09 with Run 9's artifacts still alive, and the ranking
  turns on one thing worth stating: *the binary must not be rebuilt between
  the arms of a comparison*, since a rebuild is worth up to 18% on a susceptible
  arm and swamps most of what is being asked.

  **Ordered against Run 10 rather than by value, 2026-08-10, now that its regime
  and roster are fixed.** One entry goes before it and the rest after,
  and the reasons are the schedule rather than the ranking: an experiment whose
  answer changes how Run 10 is *read* is worth its window first, while one Run
  10 supplies half of for nothing is worth waiting for. Durations below
  are quiet-machine costs, derived from the elapsed time and bench count a run's
  own provenance line reports --- about five seconds a bench-shape cell,
  criterion spending its budget whether the call is fast or slow --- and nothing
  here measures what contention does to them. **The gate entry below has since
  been folded into Run 10 rather than queued behind it**, alignment having
  turned out to be the thing that decides whether the rest of the queue
  is measuring anything; what stays there is the cheap gate that runs before
  the run does. Entries are referred to by name and not by number, two having
  been removed from under a reference already. **Nothing below is outstanding**:
  each has been run or closed, and what the list holds now is what each bought
  and the ordering rule above, which is what a later queue would be built on.
  1. **The pad probe done properly --- run 2026-08-10, and the hypothesis
     survives.** Eight binaries differing only in inert pad arms, two
     interleaved passes over all eight, 2h12m, with `build` and `mut-odo` both
     timed this time (the first attempt lost them to a shell glob) and each
     stepped through all eight 8-byte offsets --- the step being all GHC aligns
     the loop to --- with membership fixed throughout. A straddled copy costs
     1.19, or 1.10 where only three bytes precede the boundary, and the two
     discriminating binaries invert as predicted: [the floor section][floor]
     carries the verdict, the graded penalty and the controls. Placement
     and the allocator are separate effects, which is why this wanted a window
     of its own rather than being shrunk by 1: the `build`/`mut-odo` gap
     was measured across the nursery change and did not move.

     **Two pad designs relocate nothing, so they are not retried** --- measured
     on 2026-08-10 rather than reasoned about, and recorded here because
     the directory that first held them is to be deleted. Module-level inert
     pads that nothing rosters left both arms exactly where they were, across
     six variants. So did permuting two untimed roster entries deep in the list,
     which relocates only each other. What works is a pad rostered *before*
     the arm it must displace, emission order tracking first reference
     from `roster`; a pad kept inert by rostering it `Only` is checked on every
     shape and timed on none, so the selection stays what it was. Nothing else
     in that file was load-bearing, which was checked before deleting it:
     its shell-glob trap, its rule about counting what a filtered run selected
     and its correction caveat were already in [the reader][reader] and [the
     procedure](#making-a-major-benchmark-run), and what went with it
     was a per-binary offset map for binaries that are themselves gone.

     **It went before Run 10, which makes Run 10 a replication rather
     than the evidence** --- the point of that ordering, two of Run 10's
     registered predictions being the straddle hypothesis, and Run 10 testing
     it while moving roster order, heap warmth and code layout together where
     these binaries moved one thing and held the rest. It did more
     than replicate, in the end: answering the hypothesis is what turned Run 10
     from one binary into two, since an effect this size is worth removing once
     it is no longer in doubt. The asymmetric risk it was run against did
     not materialise: [the floor section][floor]'s loop table and [the
     suspension of two FastReshape axis figures][ceiling] both rested
     on a correlation inside one binary, and both stand, the suspension now
     with an out-of-sample check of its own. The binaries and the sixteen run
     files were untracked in `pad-probe/`, ~280 MB, and are deleted: this README
     carries what they showed, and the effect has a self-contained public
     reproducer in the filed issue.
  2. **A third `-nosum` arm, on a flat fill** --- the one probe that separates
     *the read is biased* from *those two arms are*. Landed
     as `mut-flat-gm-nosum` (2026-08-13) after waiting out two runs, membership
     having had to stay pinned through Run 11's repetition and unconfounded
     with Run 12's change of shim; its readings are with gate 3 and the roster
     entry. Two things from its scheduling outlive it. **The run's question goes
     in the second half**: Run 10 paired against an unaligned build and priced
     layout, Run 11 against max-skip and priced the padding, Run 12 against
     `-fproc-alignment=64` and priced the flag --- the new variable rides
     the control half and the basis stays comparable. And **`micro-both`
     was the obvious candidate for Run 12's pair and the wrong one**: it carries
     the *unconditional* shim with the flag because it was built hours before
     the max-skip form existed --- a composition that is chronology
     and not design, and a name that invites being read as design. Nor can such
     a pair separate the flag from the offsets it produces, pinning procedures
     being *how* it works; the resident offset's own price stays a probe
     on the pad-probe model.
  3. **The five-bench gate before Run 10's aligned half --- run 2026-08-10
     and it passes**, its verdicts and two corrections being
     with the predictions above. Kept because a later paired run wants the same
     gate before its own evening:

         ./run-gate.sh $R     # the two-process form this entry used to spell
                              # out is superseded: the script runs four, in a
                              # palindrome, and names its files
                              # $R-gate-<half>-<pass>.json -- the unprefixed
                              # form it used once silently overwrote Run 10's
                              # two aligned gate files

     run against `micro-unaligned` too, and expect 120 `benchmarking` lines
     each, then `--compare` one against the other, which is the reader's mode
     for an arm across two runs of one population and what prediction 4 is read
     with. `*/list` is in it for two reasons: it gives prediction 5 an early
     reading, and without a baseline `--selftest` has no ratios to check.
     With both executed copies resident at 0, `build`/`mut-odo` must read
     **1.00** and both arms must run at the resident level, which against Run
     9's placement is 10 to 19% faster rather than merely equal. A pair
     that reads 1.00 while neither arm moves would refute the penalty while
     confirming the symmetry, and that is a distinction no run so far can draw.
     Minutes, and it is the cheapest place to find out that the aligned binary
     is wrong before an hour of main set is spent on it. The dear half
     of this entry --- a main set aligned against one unaligned --- is no longer
     a queue item at all: it *is* Run 10, whose fourth prediction
     is that comparison read arm by arm.
  And three things **not** worth a quiet window, recorded so they
  are not reached for. The *how many preceding benches warm it* sweep, which
  the nursery finding supersedes --- the bench count is the symptom
  and the allocation area is the cause. The element-type re-probe, whose trigger
  is a run that moves the ordering at `Storable Double`, which Run 9 does only
  through layout and membership rather than anything an element type would feel.
  And **an A/B of the pre-swap binary against the post-swap one, to price
  the roster swap on its own** --- proposed and refuted the same day: that swap
  moved heap warmth *and* relocated every worker by ~40 KB, so binary against
  binary conflates exactly the two things Run 10's unaligned half conflates,
  and buys a number Run 10 supplies anyway at the price of a quiet hour
  and a false sense that one variable had been pinned. **Half of that refutation
  has since expired and the other half has not.** In an aligned build a roster
  swap relocates no loop, so such a pairing would no longer conflate the two ---
  but it would still buy a number Run 10's third prediction supplies
  for nothing, which was always the stronger of the two reasons. Recorded
  because the expiry of a premise is exactly what makes a dead idea look alive
  again.
- `ANSWERED` **Is the term still unbiased?** Gate 3 passes and still does
  not bracket 1: every in-situ median of both arms in all ten of Run 10's
  processes sits below it, **0.9641 to 0.9903**, for the **third** run running
  ([sum-only](#sum-only-and-the-correction-now-applied)) --- **a one-sidedness
  that has since gone**: Run 16's basis reads 1.0023, 1.0001 and 1.0184
  on the same three arms, two of them above 1, so the term is no longer biased
  in one direction and the standing caution is about its scatter rather
  than its sign --- and the two halves of the pair agree about it, so it
  is not a layout term either. Three runs on one side is no longer the coin-flip
  the failure test assumes, so the next measurement is not another gate reading:
  it is a third `-nosum` arm on a strategy whose write pattern differs from both
  --- a flat fill rather than an odometer or an expansion --- which is the one
  thing that would say whether the bias is the *read* or those two arms. Run 9's
  cells have since been read under those medians and narrow everything except
  that ([sum-only](#sum-only-and-the-correction-now-applied)): the shortfall
  is systematic per cell rather than differencing noise, the two arms order
  the shapes alike, it runs about a tenth of the term at the smallest shapes
  and vanishes at the largest, and re-pricing both arms by it moves no published
  geomean by a point. So the flat fill is the only thing left to ask,
  and the bias it would characterise is small enough that the column stands
  either way.

  **Asked and answered, 2026-08-13: it is the read.** `mut-flat-gm-nosum`
  was written into the roster and run filtered over the shape set on the Run 12
  basis build --- four benches, 96 cells, 8m17s --- and its in-situ term reads
  a median of **0.9701**, below 1 like the other two and inside
  the 0.9641--0.9903 band every process has landed in. A third arm whose write
  pattern shares neither an odometer step nor an expansion stream, agreeing
  in direction and sitting lower than both, is what distinguishes *the read
  is biased* from *those two arms are*, and it says the read. **What
  this filtered reading cannot carry is the magnitude**: with four arms
  in the process no span is what the roster places it at and every arm sits
  at the cold end, so its `mean|d|` is 7.15% against the full run's 2.98%
  and 3.39%, and its worst cell is 41% on `stretch-square-1341`, the set's
  worst-measured shape. The number to quote comes from Run 13's full main set,
  where the arm now rides; the direction does not need it. The `sum-only` pair
  covered 1 at 1.0000 in the same process, so the correction's own control
  passed alongside.
- `STANDING` **Before crediting a margin to a strategy, check whether the two
  arms' hot loops are the same code and where each landed.** Two families now
  read that way ([the floor section][floor]), and in one of them it suspended
  an axis figure the run had just published. What it does **not** extend to
  is a sweep of the roster, which was tried: the reading needs two arms whose
  hot loop is identical *and* which differ nowhere else. **That sweep has since
  been done properly, naming being available** (2026-08-13, a `-g3` twin
  over loop lengths 20 to 48). Main's own code holds a third same-code group
  and no more: `fbMutFlat` and `fbMutFlatGm` share a 24-byte loop, at offsets 5
  and 0. `mut-flat` is rostered `Only`, so the *timed* roster does hold exactly
  the two groups already read and the sentence stands as written ---
  but it stands as a checked fact rather than an assumption, and it does
  **not** become a placement pair if that arm is ever timed: the two differ
  in the Granlund-Montgomery quotient, so a line span between them competes
  with real arithmetic and says nothing, which is exactly the disqualification
  this bullet already states. A shared loop is necessary for the reading
  and not sufficient. The same sweep confirms the other half of this bullet:
  **no group at any swept length holds `bq-gen`**, so its 11% having
  no same-loop counterpart is now checked too. Everywhere else the shared loop
  is a table build while the arms differ in the output loop that distinguishes
  them, so a line span there competes with real arithmetic and says nothing.
  Recorded so the sweep is not attempted a second time.
- `STANDING` **Look at the distribution before quoting the summary --- per shape
  for a row, per sample for a cell.** Four questions settled on 2026-08-14 each
  came back the same way: an aggregate was carrying a mixture. `bq-expand-b`'s
  pooled 1% is two stable shapes and twenty-two scattering around 1;
  the `scaled` slot's slope is the average of two states a step apart;
  the alignment gain's 12% is a geomean over a distribution with no ordering
  in any dimension; and the four widest arms on the spread instrument span 2.4
  to 17.0 ns an element, so they are not a tier. The two readings cost nothing
  over kept artifacts --- `--pair` already prints a row's range and its extreme
  shapes, and a cell's samples split into quartiles by iteration count in four
  lines of arithmetic, which is what found the step. A margin whose distribution
  has not been looked at is a summary of something unknown, and the instrument
  that would have caught each of these existed before the question was asked.
  **For the per-sample half it now exists as a mode**: `--steps` reads every
  cell for a change of level mid-bench and reports it against the scatter inside
  the two segments it splits. **Its threshold is the whole test** --- some split
  is always the best one, so the naive reading flags a quarter of all cells
  and says nothing, where `t` above 40 with a step past 2% flags about 3%
  of them; quoting the first without the second would be the same error one
  level down.

- `STANDING` **The registrations those verdicts are read against.** Its order
  was chosen for heap state --- `sum-only-early` above `list`, so nothing
  is measured on an ungrown pool --- and the layout it happens to give
  was then read off the binary rather than shopped for, which is the distinction
  that keeps the run from being confirmatory. **Run 10 is now two binaries
  rather than one**, differing only in the assembler shim, so each prediction
  below says which half it is read on and the last two exist only because there
  are two ([the run's plan](#making-a-major-benchmark-run) has why,
  and the build and check sequence). Against Run 9's offsets, both
  of the straddle hypothesis's arms move, in opposite directions:
  1. **The FastReshape three go straddling to resident** (mod 40, 44, 44 to mod
     0, 36, 36) while their control stays resident (24 to 16). The hypothesis
     predicts 1.1552, 1.1795 and 1.1645 collapse toward 1.00. If they hold near
     1.16, the hypothesis is dead and [the suspension of those axis
     figures](#the-mutable-ceiling-taken) is withdrawn --- which is the outcome
     this README has the most reason to want detectable, the suspension being
     its own. **Sharpened by the pad probe**, which prices each offset instead
     of each side of the boundary: their present values are what a deep straddle
     over a resident control predicts, 1.18, and after the move all four copies
     sit resident, where the probe's own resident offsets span 0.904 to 0.956.
     So the collapse should be to between 1.00 and 1.05, and anything near 1.16
     still kills it. Do not interpolate the 36 across the boundary ---
     the penalty steps between 36 and 37 rather than ramping. **Read
     on the unaligned half**, which is the half these offsets belong to;
     on the aligned half all four copies sit at 0, so the same three ratios must
     read 1.00 outright, and that is the stronger form of the same test ---
     a 1.16 surviving alignment would kill the hypothesis where a 1.05 could
     still be argued.
  2. **`mut-odo` goes resident to straddling** (29 to 53) while `build` stays
     straddling (53 to 45). The hypothesis predicts their 1.13 closes toward
     1.0, and **the pad probe makes that a point prediction, 0.998**: two deep
     straddles, whose penalties cancel, so the pair should land on 1.0 rather
     than merely approach it. The same penalties reproduce Run 9's own 1.13,
     at 1.144. If it holds or widens, the hypothesis is dead by the other route.
     **Read on both halves, and it is the weaker of the two arms precisely
     because they agree**: the unaligned half predicts 1.00 because 45 and 53
     happen to carry near-equal penalties, and the aligned half predicts 1.00
     by construction, so the two halves cannot disagree here and the pair's own
     value is not what makes this run worth two binaries. Prediction 1
     and prediction 4 are.
  3. **The anchors move, and one of them is a control.** Warming `list`
     is the object of the swap, so the absolute anchors should fall and every
     ratio rise with them --- but not uniformly, and the excess-allocation rule
     says which. Ten of the eleven anchor cells carry 27 to 336 MB of excess
     and should move; `cnn-slice-c32`, at 0.05 MB, sits under the nursery
     and should hold, which makes it a control inside the anchor table.
     If it moves too, what warming does is not the nursery; if the other ten do
     not, warming does not reach the baseline and the swap bought nothing.
     And a fall shared by all nine populations is one effect rather than nine
     findings, so read the anchors together before reading any class paragraph.
     **Read on the aligned half alone.** Warming is heap state and not layout,
     `list` carries no layout term worth the name, so the anchors read the same
     on both halves and reading them twice would enter one effect as two
     findings. That last step is prediction 5's to establish, not this one's
     to assume: read 5 first, and if `list` does move between the halves
     then this prediction has no fixed anchor to be read against and waits.
     The nine populations' anchors are commensurable as printed, the fingerprint
     this run publishes being the aligned one and the eight class blocks aligned
     with it, so the reading-together above can be done off the run's file.
     That is a ruling and not a coincidence: had the unaligned fingerprint
     been the published one, exactly one of the nine would have crossed a basis,
     and the run's plan says why it is not.
  4. **The two halves differ, and for six arms by how much is registered here.**
     This is what the second binary is for. It was to have been a per-arm
     prediction over the whole roster, and **that is not available**:
     attributing a loop to an arm needs source information, every build
     that carries it relocates the code, and no bridge survives. `-g3` moves
     the fills from `[3, 53, 59, 45]` to `[8, 56, 4, 4]`; `-finfo-table-map`
     dissolves the groups altogether; matching the two builds by loop order
     fails at the first loop, and only 30 of 957 release loops have a body
     unique enough in both to match by bytes. The release binary keeps four
     `zdwgo7` symbols where the debug build has 47 and carries 98 `Main` symbols
     in all, none named for an arm, so its own symbol table cannot do it either
     --- and `NOINLINE`, the obvious fix, is already on these arms: adding
     it a second time is a compile error and the symbols are absent regardless,
     GHC emitting the module's code under a handful of workers. Measured
     2026-08-10, and recorded so the routes are not retried.

     What *did* work is the case-by-case form, and it is why six arms can
     be registered at all: take a loop's bytes from a `-g3` build, where
     `addr2line` names the `Main.hs` line and so the arm, then find the same
     bytes in the release binary. It succeeds when a loop is distinctive
     and fails when it is not --- the 30-of-957 figure is the wholesale version
     of this, and a loop shared by two arms is ambiguous by construction, which
     for `build` and `mut-odo` is the very fact being measured. So attribution
     is available one arm at a time, at the price of a second build and a hand
     check, and is not available as a sweep.

     **What is registrable is the six arms whose loops this README has already
     identified, read off `micro-unaligned` with `loop-offsets.py`**: the fills
     sit at `[3, 53, 59, 45]` and `[16, 0, 36, 36]`, and all eight copies go
     to offset 0 in `micro-aligned`. So **`build` and `mut-odo` should each run
     about 0.85 of their unaligned selves** --- from 45 and 53, both deep
     straddles at about 1.10, to the resident level near 0.93 --- while their
     *ratio* stays at 1.00, which is what makes this a different measurement
     from prediction 2 rather than a restatement of it. The four
     `mut-odo-vecdims` arms are resident already, at 16, 0, 36 and 36, so they
     should move by a few percent at most, and the three ratios by less. An arm
     here that moves the wrong way, or the pair moving apart, is a finding.

     **For the rest of the roster the prediction is aggregate and weaker,
     and says so**: the moves falling in two groups rather than smeared,
     and the count that can move bounded by the short loops the shim rescues ---
     50 of `micro-unaligned`'s 115 straddle where none of `micro-aligned`'s do,
     so 50 loop heads' worth of penalty is removed and how many arms
     that touches is exactly what the run finds out. An arm reading *slower*
     aligned is not by itself a refutation: the padding is NOPs, and an arm
     that falls through into an aligned head executes them every time it does,
     so a small loss where no loop was straddling is the shim's own cost
     and not evidence against the penalty.
  5. **`list` does not move between the halves**, which is the pairing's control
     and the one result that would invalidate the rest. It is the insusceptible
     arm, 0.5% across four rebuilds, so alignment should leave it alone;
     if it moves, the baseline may have been carrying layout too, every
     published ratio in this README divided by a moving denominator, and
     that is a larger finding than anything the run was built to get. *May*,
     because `list`'s hot loop is **library code and not Main's**: `fbList`
     is one line over `VS.fromListN` and `toListT`, and no loop in a `-g3` build
     resolves to its source lines, so the shim cannot align it and only
     the phase-matching keeps it still. Its expected stillness therefore rests
     on measurement and not on mechanism --- 0.5% across four rebuilds, which
     rerolled the libraries too --- which is weaker ground than the six arms
     stand on and worth saying before the number is read.

     **Three things rest on this one, and no other prediction here carries more
     than itself** --- which is why it is read first and why a failure
     is not one prediction lost but the run's arrangement to reconsider.
     Prediction 3 has no fixed anchor without it and says so. Run 10's mixed
     basis, its main table unaligned and its eight class blocks aligned,
     is tolerable only while the two halves' baselines agree. And the transition
     to Run 11 turns on Run 11's second column succeeding Run 10's unaligned
     table, which a moving denominator would put in doubt as well. The gate
     below already reads it on every shape and at the ordinary budget, so what
     the run adds is not coverage but company: `list` there shares a process
     with 33 other arms instead of four, and heap state and code position
     are exactly what this README has measured moving a figure when no strategy
     changed. That is the reading all three wait on.

  **The gate has been run and the three testable predictions hold** (2026-08-10,
  five benches over the 24 shapes, two passes per half in the order unaligned,
  aligned, aligned, unaligned, so both binaries carry the same mean position).
  Prediction 4: `build` reads **0.8836** of its unaligned self and `mut-odo`
  **0.8778**, so alignment is worth **12%** to each and the two agree to 0.7%,
  which is what one worker in two places should do. Prediction 5: `list` moves
  **0.3%**, so the baseline is still, the denominator holds, and the library
  reroll does not reach the one arm whose loop is library code ---
  the phase-matching earning its keep. Prediction 2: the pair reads 0.9754
  and 0.9805 unaligned, 0.9610 and 1.0082 aligned, nowhere near the 1.13 or 0.86
  earlier runs saw. Run 10 is worth its evening on this; what a gate of five
  benches and two passes cannot say is anything about the rest of the roster.

  **Two corrections come with it.** The registered 1.00 for prediction 2 was too
  strong: the pair sits at ~0.98 on both halves, where the pad probe's own
  both-resident binaries sat, so the arms' intrinsic ratio is **0.98 rather
  than the 0.9973** [the floor section][floor] carries --- an estimate
  that assumed the two arms share one penalty curve, which their 5.9%
  disagreement at offset 13 already contradicted. It costs the arms nothing,
  since they share a worker but not a call path, `build` being `mut-odo` driven
  through `vBuildVS`. And **offset 0 is measured for the first time**:
  the probe's eight offsets were all congruent to 5 mod 8, so the 0.85 predicted
  here was an extrapolation from the resident mean, and the gain at 0 is 12%
  rather than the 15.6% that implied.

  **The gain is not a constant, which prediction 4's aggregate form should
  say.** Read shape by shape it runs 0.719 to 1.031 for `build` and 0.763
  to 1.033 for `mut-odo` --- 28% at the best shape and a slight loss
  at the worst --- against a per-shape noise floor this gate puts at 6.3%,
  that being the median disagreement between the two arms' own gains where
  identical code says they should agree. So the extremes are real and the middle
  is not resolvable on two passes: the 12% is a geomean over a structured
  distribution and not a factor every arm pays. **Asked over 24 shapes
  and answered, so it retires** (2026-08-14, arithmetic over Run 10's two kept
  main sets, no machine time). The gain spans 0.773 to 1.025 on `build`
  and 0.697 to 1.018 on `mut-odo`, at geomeans 0.877 and 0.863, while the arms
  whose loops did not straddle sit flat --- `list` 1.006, `mut-odo-vecdims`
  1.007, `bq-expand` 1.002 --- which is the instrument saying it works. Against
  the four variables this entry named, the Spearman of log gain reaches |0.38|
  at most, and the two largest, `mut-odo` against `l` at -0.36 and against `m`
  at -0.38, fall to -0.04 and -0.02 on `build`, which no size law could do.
  The two shapes showing no gain at all, `stretch-pow2stride` at 1.007
  and `stretch-square-1341` at 1.025, are mid-range in every dimension.
  So the 12% is a geomean over an unordered distribution: there is no shape
  ordering to find, and the question is closed rather than parked.

  **The correction term moves too, by 0.6%.** Both `sum-only` halves read 0.9939
  and 0.9938 aligned over unaligned, agreeing to a digit over a range of 0.990
  to 0.998, so the forcing pass is itself slightly faster in the aligned build
  --- its own loop presumably being among the fifty the shim rescues.
  It is subtracted from every figure, so it is not a term that cancels between
  the halves; at 0.6% of a fraction of each cell it cannot reach the 12%,
  but a later reading that needs the halves to share a correction should know
  they do not quite. Allocation, by contrast, is identical to 2.5e-6.

  **The gate read the aligned half as the noisier one and the full budget says
  it is not.** Over the gate's five benches its median CI% was 0.532 against
  the unaligned half's 0.218, and its two passes disagreed more (`mut-odo`
  at 1.0224 against 0.9859), which left open whether alignment widens
  the per-cell interval structurally. Over Run 10's 816 cells a side the two
  halves are indistinguishable: median CI% **0.138 against 0.134**, median R^2
  0.99997 on both, and the aligned cell is the wider one 389 times of 816.
  So the widening was the gate's own sample size, and alignment removes
  a systematic term at no cost in precision. That closes the question the gate
  raised, which is what the full budget was wanted for.

  The first two were arms of one prediction, either of which could kill it,
  on arms already rostered and at no extra machine time; the third priced what
  the order change was for and carried its own control; the fourth is why
  the run was two binaries and the fifth is what made the fourth readable.
  The pad probe having answered the hypothesis first, the first two
  were replications carrying point predictions rather than the evidence ---
  which is what that probe's window was spent to buy, and why the run's own
  weight sat on 4.
- `ANSWERED` **What costs `mut-odo-vecdims-add-out` its 16%, now that layout
  cannot? Asked and answered the same day: it is a per-run cost, and the Core
  reading had it right all along.** Run 10 read the arm 1.1266 with its loop
  resident and 1.1612 with every copy at offset 0, so the suspension [the
  ceiling][ceiling] carried is withdrawn and the cost is the arithmetic's.
  Regressing the per-shape penalty on the aligned half --- arithmetic
  over the run's own cells, no machine time --- puts it at r **-0.64** against
  log `sInner` and **-0.01** against log `m`, 1.423 where `sInner` is 3
  and 0.997 where it is 64. That is the signature of work done once per run
  and amortized over the run's elements, which is what the `scanr (*)` stride
  table is; the account is [in the ceiling section][ceiling]. What made
  this unanswerable before is that Run 9's copy of the shared loop straddled
  a cache line, adding a *per-element* term that flattened the very correlation
  the question turns on --- so the pairing bought a mechanism here and not only
  a number. `add-both` tracks it at the same r and the corner's sub-additivity
  says the two axes largely pay for one thing. **And the third axis is migrated
  here, 2026-08-14, from where it was answered and left**: why the count-down
  form pays was raised inside [the mutable ceiling][ceiling]'s own write-up,
  which is where the answer sits too --- of the three axes FastReshape's loop
  arithmetic ports, one is free, one costs 16%, and the count-down form
  is the third, recovering most of the corner's loss at 0.9408 against it on 22
  shapes of 24, and reproducing Run 10's reading. Recorded here because the list
  is meant to be the only home, and a session mining it walked past this one.
- `OPEN` **What is the 3% that survives alignment on `build`/`mut-odo`?**
  With both copies of one worker at offset 0 the pair still reads 0.9685
  on the main set, tying by the sign test (16 of 24) while the interval misses
  1, and it runs 0.9148 to 1.0335 across the nine populations. The gate's
  correction already put these arms' intrinsic ratio at 0.98 rather than 1,
  on the pad probe's both-resident binaries, so Run 10 reproduces that at full
  budget rather than contradicting it.

  **Run 16 widens the question past that pair and excludes every mechanism
  the runtime can report** (2026-08-20, the wildlog probe on the `reshape1`
  class). The residue is not special to `build`/`mut-odo`: on `reshape1-500k`
  an arm and its own A/A duplicate --- the same function under a second name ---
  differ by **8.2% of mutator time** while allocating identically to 0.01%
  (4007172 bytes against 4007513 and 4007412), sitting at a flat 92 MiB in-use
  heap across every sample of all three benches, spending **0.03%** of their
  time collecting, and taking no major collection inside any of their timed
  windows. Allocation volume, heap occupancy and collector work are therefore
  all out, which is the whole of what the RTS reports.

  **And it is not a monotone effect of position in the process either, which
  is the sharper half.** The two duplicates run at roster slots 9 and 15
  and the base at 14, so they *bracket* it in execution order --- and they agree
  with each other to **0.09%** while both sit 8.2% from it. A warm-up or drift
  term would order with the slot and does not. Run 10 saw the same shape
  at the `scaled` slot, where it was the base arm that was slow and
  not the twins, so this is the second class in which the base is the odd one
  out among three readings of one function.

  **What would settle it, and it is one measurement.** The timed binary carries
  four copies of that body, at cache-line offsets `[0, 24, 0, 4]` on Run 17's
  basis where Run 16 held `[11, 0, 4, 0]`, and Run 13's ruling is that the `-g3`
  twin cannot say which arm runs which. Attribute the copies directly instead:
  `perf record` over those three benches on the run's own basis binary maps
  samples to addresses without needing DWARF names, and if the base executes
  a copy at a different offset from the twins' then the straddle model already
  in this README predicts both the sign and roughly the size. If the three turn
  out to share one copy, placement is excluded too and this README has
  no candidate left --- which is the more valuable outcome of the two.
  **The instrument is usable when the machine lets it be, and that is a state
  to assert and not a fact to record**: `perf` is installed,
  and `kernel.perf_event_paranoid` has to read 1 or lower before it counts
  anything --- **it is not persistent**, and on 2026-08-22 alone it read 1,
  then 4, then 1 again, so an entry quoting a value is stale by construction
  and this one no longer does. Lowering it is a `sudo sysctl -w` in a plain
  terminal, not something a session can do. Check it at the moment of use:
  `run-counts.sh` now refuses up front rather than spending its full sweep
  writing NaN, which is what a blocked `perf` used to buy. This is one filtered
  process rather than a run. The offsets move with every relink, so take them
  from the binary being sampled rather than from this entry.

  **Run 11 says the residual is not stable within itself, which is new.**
  Re-running that binary puts the pair at **0.9467** on the main set at 21 wins
  of 24, sign p 0.00028, where Run 10 read 0.9685 at 16 of 24 and called
  it a tie --- the point estimate moving two points and the sign test from tie
  to decisive with nothing changed. Across the nine populations it runs 0.9215
  (`revsome`) to 1.0209 (`slice`), reproducing Run 10's 0.9148 to 1.0335
  as a span while the individual classes swap sides: `bcastmid` and `slice` put
  `build` behind, `reshape1` puts it ahead by 5% where Run 10 had it behind
  by 3%. And these two arms are the ones the repetition finds least stable
  anywhere --- `mut-odo` the only arm whose geomean leaves 1.5%, `build` holding
  the two widest cells after the wild one ([the floor section][floor]).
  So the 3% is not one quantity waiting to be attributed: whatever
  it is fluctuates run to run on arms whose code, layout and slot are all
  pinned, and an experiment that prices it once has priced one draw. **And three
  draws now exist without one being run**: the between-process spread instrument
  below reads this pair on Run 11, Run 12 and Run 13 alike, and puts `build`
  in the widest three every time --- so what this entry wanted a run to supply,
  the kept artifacts already carry, and the open question is the account rather
  than another draw.

  **The Core route is closed and is not to be re-proposed.** The obvious
  candidate is the call path --- `build` being `mut-odo` driven through
  `vBuildVS` --- and it has been dumped three times, from Run 6's source, Run
  7's, and Run 8's commit under this regime: there is no call path to find,
  `vBuildVS` surviving as no top-level binding in any of them, the two workers
  byte-identical once numbering is normalised, and the sources differing only
  by the `Strides` newtype's zero-cost cast ([the mutable ceiling][ceiling]
  keeps the dumps' verdict). A fourth dump would reproduce that and nothing
  else.

  **Narrowed the same day, to about a percent, and not attributed.** The next
  candidate after the call path is that the shim aligns loop heads
  and not procedures, so putting both inner loops at offset 0 leaves everything
  about where the two procedures sit --- their cache sets, their neighbours,
  the outer odometer recursion's own alignment --- different. [The floor
  section][floor] had the build that tests it, a `-fproc-alignment=64` one
  in which the two procedures are 64-aligned and internally identical so both
  copies land on the *same* offset, built and read and left untimed; timing
  it is a filtered A/B and it now reads 0.9893 against 0.9782 for the shim's
  build and 0.9585 for neither. **Sharing an offset is now refuted as what makes
  the pair tie**, and from data already in hand: the named map puts `mut-odo`
  and `build` both at offset **0 in both Run 12 halves**, and the pair reads
  0.9822 in one and 0.9431 in the other --- sharing an offset in both, tying
  in neither, 3.9 points apart. The reading below is what that replaces.
  **Sharing an offset was what appeared to make the pair tie** --- both
  same-offset builds do, the different-offset one does not --- but the two ties
  cannot be ranked against each other on one pass, their intervals overlapping
  and their sign tests disagreeing about which is flatter. So procedure
  placement is still a candidate and not the answer, and the honest bound
  is that these two names differ by about a percent once their copies share
  an offset, part of which is roster context rather than either arm. The shim
  *and* the flag together would have ranked them; that build was made and timed
  on 2026-08-11 and **does not**, landing about a percent nearer level inside
  a 1.8 to 2.3% repeat spread, so procedure placement stays a candidate. A small
  filtered test beside it prices a shared straddling offset at 8 to 13% on both
  arms and the flag at 2 to 4% over the shim alone --- indicative only,
  and a reason to pad any pair that adopts the flag ([the floor
  section][floor]).

  **Run 12 gives the candidate its first full-budget term, and the term
  is large.** Its two halves differ in `-fproc-alignment=64` and in nothing
  else, which is the flag whose whole action is moving procedure starts ---
  and the pair reads **0.9822** on the basis, tying at 16 wins of 24 with sign p
  0.15 on an interval covering 1, against **0.9431** on the flag half at 17
  of 24, sign p 0.064, on an interval that misses it. **That is 3.9 points
  between two binaries with code, roster, order, shapes and shim all pinned**,
  and it is the widest a within-run pairing has moved this pair: Run 11's two
  halves parted by 3.1 points and Run 10's by 1.5. So procedure placement
  is no longer only a candidate that a filtered probe could not rank ---
  it is worth four points at full budget on the one comparison built to isolate
  it.

  **What it does not do is confirm the shared-offset reading**, and the two
  should not be run together. The expectation above was that 64-aligning both
  procedures makes the two copies share an offset and the pair therefore tie;
  Run 12's flag half is instead the *least* tie-like of the six full-budget
  readings this pair now has, which run 0.9431, 0.9467, 0.9532, 0.9685, 0.9778
  and 0.9822 across Runs 10 to 12. The two flattest are the two max-skip halves
  and both tie; the two steepest are the two builds carrying more alignment.
  The 2026-08-11 filtered reading that put shim-and-flag "about a percent nearer
  level" was taken on the *unconditional* shim with the flag, a combination
  this pair does not contain, so it is not a contradiction --- but it
  is a reason not to carry that reading forward as though it described this one.
  And the flag moves procedure starts and the offsets they produce together,
  exactly as [Run 12's second registered prediction](#what-is-open) records,
  so this four-point term prices the package and does not attribute it.

  **Across the nine populations Run 12 runs 0.9013 (`reshape1`) to 1.1644
  (`window`)**, against Run 11's 0.9215 to 1.0209 and Run 10's 0.9148 to 1.0335,
  and the classes swap sides again --- `bcastmid` (1.0365) and `window` put
  `build` behind where `reshape1` puts it ahead by 10%. Read the top
  of that span as the two-shape populations it comes from rather than
  as a finding: `window`'s is two cells at sign p 1. What the span says is what
  the entry already said, one run more strongly --- whatever the residual is,
  it is not one quantity waiting to be attributed.
- `ANSWERED` **Which arm owns a loop copy: answered, and the answer is
  that a binary can carry its own names.** A `-g3` build emits a per-block
  symbol with DWARF line info, so `loop-offsets.py` prints a copy
  as `fbMutOdoVecdims` with its source line instead of as one worker's mangled
  name, and a binary with no line info prints what it printed before.
  **The ruling is that the twin's names are a per-GROUP property and
  not a per-binary one**: count a body's copies in twin and timed binary before
  trusting them, which the vecdims group passes four against four
  and the `build`/`mut-odo` group fails at four against two. The named readings,
  the refuted padding prediction and the window-matching method are in [the
  floor section][floor].
- `ANSWERED` **The shim was blind under `-g`, which is why this wanted a fix
  and not merely a build.** Under `-g` every head follows the previous block's
  `_end` and `_proc_end` labels rather than an instruction, so not one head
  of a `-g3` assembly was given a directive and the build came out unaligned
  in silence. **The ruling is the condition on the fix and not the fix**:
  the look-through fires only where the assembly carries `.loc`, so a `-g` build
  gets the corrected guard and every other keeps the literal one byte for byte
  --- applied to every build it would find 27 heads more in the plain assembly
  and re-base every figure this README has published, for a reason no strategy
  changed. The counts, the end-to-end control and what those 27 heads cost
  in pads are in [the floor section][floor].
- `ANSWERED` **`-g3` is a different program, and what differs is register
  allocation.** Measured on the assembly GHC hands the assembler rather
  than inferred from the binary, both sides stripped of every `.loc`, every
  debug label and every `.debug_*` section and their label uniques renamed
  in order of appearance: 60056 instructions against the plain build's 59991,
  of which +63 are `movq`, with register assignments and block order differing
  throughout. What does not differ is what this README times --- all three
  28-byte groups have the same body in both builds --- and the two copies
  the `-g3` build lacks are the dead ones, its `build`/`mut-odo` group holding
  two where the plain build's holds four and `addr2line` putting those two
  in `fbMutOdo` and `fbBuild`. That confirms by a second route
  the `[dead, mut-odo, dead, build]` reading `loop-offsets.py`'s docstring had
  asserted, and it is the naming's non-vacuity control: a scheme that names them
  must put those two in that order. `-add-both-down` is in neither group,
  its loop being the count-down form's 24 bytes as [the floor section][floor]'s
  table records, and `--len 24` finds it.
- `ANSWERED` **So building everything with `-g3` is refuted, and a `-g3` build
  is a twin to read rather than a binary to time.** The proposal was that timed
  binaries carrying their own names would make a per-arm offset claim
  an ordinary reading, and its own criterion was that the arms agree within
  the run's floor. They do not: a pair differing in `-g3` alone gates at `build`
  0.9391 to 0.9517 plain over `-g3`, four to six times the floor and one
  direction. **And no weaker level is a way round it** --- `-g1` is the weakest
  GHC has and changes the emitted code exactly as `-g3` does, which is what
  horde-ad's `docs/ghc-issue-debug-changes-codegen.md` reports as [GHC work item
  27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687). The gate's
  figures and the copy census that bounds the naming are in [the floor
  section][floor].
- `OPEN` **A recurring transient that lands on the `bq-expand` family, worth 35
  to 74%, and which no published column would show.** Not one cell: **five
  sightings in twelve runs**, moving each time, the largest of them Run 17's
  74.48%, with Run 18 clean at a worst cell of 23.03% and Run 19 clean again
  at 19.75%. Run 8 read `bq-expand`'s distant twin 44% slow on `vgg-14-c512-k3`
  and Run 9 41.4% on the same arm and shape; Run 10 was clean; Run 11's aligned
  half reads `lenet-L1-28-c1-k5/bq-expand` at **1.355** of what that same binary
  read in Run 10 --- a different shape and, this time, the arm's **own** slot
  rather than a twin's; Runs 12 to 15 came up clean. Run 10's roster fix
  (`sum-only-early` above `list`, so nothing is measured on an ungrown pool)
  removed the Run 8 and Run 9 instance and was confirmed at full budget; it did
  not remove the effect. **Decomposed on a kept instance, 2026-08-14, and
  it is mutator time with the work identical.** Run 11's aligned half carries
  one: `lenet-L1-28-c1-k5/bq-expand` reads 56.56 us net there against 41.4
  to 41.9 across the seven other processes on disk, with `list` normal
  in that same process, so it is the arm and not the process. Per iteration,
  wild against normal --- time x1.279, **mutator x1.281**, gcWall x0.980, GC
  count x0.997, allocation **x1.000002**, peak heap equal --- which is the same
  instructions on the same bytes running 28% slower, and excludes GC, the pool's
  cost and any extra work *inside the anomalous process* rather than
  in a filtered one that never had the state. It is also flat from first sample
  to last, so the state was entered before the bench began. **The cache-miss row
  is now the only unexcluded candidate rather than one of several**,
  and the published 35 to 44% is the net figure against a raw slope ratio
  of 1.279, the correction amplifying it. **And it is the tail of something
  common, swept over every kept main set the same day**: of 4029 cells
  in the eight processes, 121 carry a step past 2% at `t` above 40 --- 3% ---
  the largest reaching 12 to 15%, and the arms carrying them are the ones
  this README already suspects, `build` at 20% of its cells, `offtab` 19%,
  `mut-odo` 16%, `gen-quotrem` 11%. **The axis is size, and it is not the spread
  instrument's axis**: step size against log `l` reads -0.70, where
  the between-process spread tracks `sInner` and rank instead, so the two
  instruments are measuring different things and neither subsumes the other.
  Incidence tracks `l` too (-0.64 raw), but sample count itself tracks log `l`
  at -0.93, so power is confounded with the effect there and only the size
  figure is clean; within an equal-power band the incidence correlation survives
  at -0.43. The four big shapes carry none at all. What this changes about
  the wild cell is that it is not a lottery among cells but the extreme
  of a distribution, which is why the `scaled` slot can stand in for it. **What
  that largest cell IS, measured on its per-sample record and recorded here
  because the registration carrying it retires**: a LEVEL and not an event.
  No step appears in the cell at all and `--steps` reports none; across
  the three copies of that function on that shape the heap sits at 81.0 MiB,
  no major collection runs, allocation an iteration agrees to a thousandth
  and the collector takes under 0.02% of mutator time, while mutator time
  an iteration reads 4,708,902 ns, 4,682,268 ns and **7,884,026 ns**. Every
  quantity the runtime reports is flat across a cell that is 68% slower, which
  is what makes this a transient rather than work.

  **Three things make this a threat to a published claim rather
  than a curiosity.** It is *the expansion family* that is susceptible,
  established rather than guessed: Run 9's filtered probes put
  `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback` each
  35--40% above their published cells on that shape while
  `bq-scan-rem-gm-mulback` and `mut-odo-vecdims` did not move at all.
  That family contains **`bq-expand`, which is what `Data/Array/Internal.hs`
  carries today** --- though not what this README recommends since the decision
  of 2026-08-22, which is `mut-odo-vecdims`. And **the table cannot show it**:
  the winsorized estimator caps the cell, so the row read 0.103 against 0.102
  and nothing looked wrong --- the only reason it was seen is that `bq-expand`
  carries two A/A twins, which disagreed with it by 25%. An arm without twins
  would show nothing at all, which is most of the roster.

  **The evidence against an intrusion is [in the floor section][floor]**: clean
  twins, time-neighbours within 1.2%, CI% 0.06 over 125 samples, `list`
  on that shape unmoved.

  **The samples have since been read, and they say the cell is a shift and
  not a defect** (2026-08-12, arithmetic over the run artifacts, no machine
  time; a refit of `reportMeasured` reproducing criterion's own slope to 2e-16
  first, which is what says the sample layout was read right). Its per-iteration
  residual dispersion is **2.57 us against its own twins' 2.76 and 0.70**
  in the same process, and against 2.20 to 2.79 for the same three arms
  in the maxskip half --- so it is not the noisy one. Every arm there shows
  the same small warm-up in its first third, gone by its last, and the residual
  correlates with allocation and GC count at +0.5 to +0.8 on twins and arm
  alike, so neither is the cell's. Allocation per iteration is the same
  340193--340195 for all six. What is left is a clean 14.4 us on the slope
  of one arm at one slot, with everything a sample can report looking ordinary
  --- which is what Run 8 and Run 9 found at their cell too.

  **Read the rest of what a sample carries and the mechanism narrows sharply**
  (same day, same artifacts). Against its two twins in the same process the cell
  runs 68342 ns an iteration against 53896 and 53364 --- and **259697 cycles
  against 204804 and 202781**, the same 1.28 as the time, so the clock
  is not moving: all three read 3.8000 GHz to four digits. Allocation
  is **340197 bytes an iteration against 340196**, one byte apart. GC time
  is **312 ns against 323 and 328**, so the arm collects no more than its twins
  and could not pay for 14.4 us if it did. The whole excess is mutator cycles:
  the same instructions over the same bytes, stalling 28% more.

  **That refutes, for this instance, the account inherited from Runs 8 and 9.**
  Theirs was a cold block pool at a roster slot --- an allocator warmth story,
  which predicts more or dearer collection --- and here GC is flat
  and allocation identical to the byte. So either the pool was one trigger
  of something more general, or the two sightings are different effects wearing
  the same shape. What is left, code placement being identical (one binary,
  the same offsets), the data volume identical and the clock fixed, is **where
  the data sits**: the input, the offsets table and the output buffer
  are allocated per bench and their addresses are the one thing that differs
  between an arm and its own twin. This README has spent four runs on code
  placement and has never measured the data side.

  **Three instruments were tried the same day and all three came back negative,
  which is worth as much here as a positive would have been: they say what
  the cause is not, and two of them are not to be reached for again.**

  1. **Cycles add nothing on this machine, so a cycles-based detector is
     not the answer.** Over **all 4556 cells of Runs 10 and 11** the effective
     clock is 3.8000 GHz to within 0.0012, so `measCycles` is a rigid multiple
     of `measTime` and carries no independent signal. What that does buy, once
     and for all, is that no timing anomaly on this desktop is ever the clock:
     not thermal, not frequency scaling. Do not add a cycles column to `--aa`.
  2. **The detector already exists and it fired.** `--aa` prints each pair's
     worst cell, and it printed 26.44% and 25.51% for the two `bq-expand` pairs.
     Nothing was missing but the reading --- which [the
     procedure](#making-a-major-benchmark-run) already demands in as many words,
     a pair inside the floor whose worst cell is an order of magnitude outside
     it being a finding the aggregate is hiding. A sweep of every A/A cell
     of both runs puts the rate at **2 of 804 past 10%**, both of them this one
     incident, and 4 past 5%: rare, not a lottery over every cell,
     and concentrated where the twins are.
  3. **The data-placement hypothesis is refuted, and with it `setarch -R`.**
     A standalone probe allocating the same three buffers a bench does reports
     the same three payload addresses in every one of eight processes ---
     `0x0042005fe010`, `0x0042005f6010`, `0x0042005cf010` --- because the GHC
     RTS reserves its heap at a fixed base, so ASLR never moves it however
     randomised the C heap and libraries are (`randomize_va_space` is 2 here,
     and `setarch -R` changes none of the three). So two processes of one binary
     lay their benchmark data out identically, there is no per-process address
     lottery to disable, and instrument 3 would have measured nothing.

  **What survives is narrower and sharper.** Buffers land where the *allocation
  history before them* puts them, and that history is not identical between two
  runs of one binary: criterion spends a time budget, so the iteration counts,
  and hence the bytes allocated before a given bench, differ run to run.
  That is a lottery driven by criterion's own scheduling rather than
  by the operating system, it is invisible to every instrument above,
  and it predicts exactly what is seen --- same binary, same slot, different
  run, one arm of a susceptible family 28% slower in mutator cycles
  with allocation identical to the byte.

  **What follows for reading a table, before any of it is measured further.**
  Four things, and the second is the one this README has been quiet about:
  1. **The A/A worst cell is a gate and not a note.** It is the only thing
     that caught a 35% error, and it caught it while every aggregate stayed
     green. A pair whose worst cell passes about 10% disqualifies that cell
     from the per-shape record and flags its row; listing it for adjudication
     is what let this one be read past.
  2. **Nine of the twenty-four timed strategies carry twins**, so that gate
     covers three eighths of the table: `bq-expand`, `bq-scan-rem-gm-mulback`,
     `mut-odo-vecdims`, and --- added 2026-08-14, first read in Run 14 ---
     `bq-odo-gm-mulback`, the susceptible family's own pure-tier head, `offtab`
     for [the spread question][open], and then `build`, `mut-odo`, `list`
     and `gen-unsafe` once the same day's readings said what the coverage
     was hiding: both anomalies on record landed on a twinned arm, so their
     apparent distribution is a fact about the controls before it is one about
     the machine. A wild cell on `bq-mut` or any other untwinned arm would still
     be capped by the estimator, would move its row by a thousandth, and nothing
     here would ever say so; that is the honest extent of the defence --- now
     with `build` and `mut-odo`, whose 1.13x gap is Run 14's own registered
     control, inside it rather than outside.
  3. **Winsorizing is a defence and not only an estimator choice.** It is what
     held `bq-expand`'s row to 0.103 with a 35% cell inside it. [The `time`
     column](runs/run19.md#results) argues for it on estimator grounds ---
     bounded influence rather than deleted evidence --- and this is the second
     and larger reason to keep it.
  4. **It gives the per-shape caution its mechanism.** [The per-shape
     table][pershape] says to trust the first digit only; a scheduling lottery
     moving one cell by a third is why, where a geomean over 24 shapes cannot
     move like that.

  **And a fourth instrument died on contact, which is worth a sentence because
  it is the obvious one.** If the mechanism is allocation history, pinning
  criterion's iteration count should pin the history and make cells reproduce;
  but `-n/--iters` is *Run benchmarks, don't analyse*, and a run under it writes
  no JSON at all --- measured, not read off the help text. There is no other way
  to fix the schedule from the command line, so the mechanism cannot be tested
  by pinning it, and it is recorded here dead rather than left
  to be re-proposed. What `-n` *is* for is the next paragraph.

  **The block-pool issue this project filed is the nearest precedent,
  and its methods are the ones to reach for next** ---
  `docs/ghc-issue-block-pool-fragmentation.md` in horde-ad, filed as [GHC work
  item 27601](https://gitlab.haskell.org/ghc/ghc/-/work_items/27601),
  with the full analysis in `docs/position-effect.md`. **The bug itself
  is probably not this**: its symptom is a pool that doubles and stays doubled,
  and `max_mem_in_use` across the four main-set processes of Runs 10 and 11 sits
  at 218 to 220 MiB with the *wild* process the smallest of them; nor does any
  of the 24 main-set shapes allocate in the worst-case band just above
  the 3276-byte large-object limit. **But its description of the statistical
  signature is this situation verbatim**, and having it filed upstream is worth
  more than re-deriving it: a bias rather than noise, regression fits staying
  tight around a value wrong by a fifth, more samples in the same process
  shrinking the interval *around the wrong value*, and --- the part that matches
  the lottery --- an effect that in rare runs does not reproduce and whose
  magnitude differs randomly from run to run.

  **So the instrument that report used is the one this question wants**:
  `perf stat` over runs with a fixed iteration count, read per iteration.
  Its table is the model --- task-clock, instructions, dTLB-load-misses,
  cache-misses, page faults, clock --- and it identified last-level cache misses
  by finding instructions equal to 0.9994, clock equal, GC and allocation equal,
  and cache-misses 2.86 times. Three of those rows are already known here
  and agree: the clock is fixed, allocation is identical to the byte, GC
  is flat. **The missing row is the cache misses, and only `perf` can supply
  it** --- paired with `-n`, whose fixed iteration count and absence of analysis
  is exactly what that method wants, which is what `-n` is for and why
  its retraction above is about JSON alone. `+RTS -H2G` is the control the same
  report validates: a pool taken in one contiguous piece removed the cost there,
  so a wild cell surviving `-H2G` is not pool structure.

  **`perf` needs `kernel.perf_event_paranoid` at 1 or lower before it counts
  anything** --- above that it reports `cpu-cycles:u <not supported>`, Ubuntu's
  level 4 being its own and above the upstream maximum of 3 --- and lowering
  it is a `sudo sysctl -w` in a plain terminal, not something a session can do.
  **The setting does not persist**, so it is asserted at the moment of use
  and never quoted as a property of this machine: [the position-term
  entry][open] carries the day it moved twice.

  **Run 2026-08-12, and the cell does not reproduce filtered, as expected.**
  Differencing `-n 40000` against `-n 20000` on `run12-maxskip`, which removes
  the process's fixed cost exactly rather than diluting it --- at `-n 200`
  startup was 45% of task-clock and the counters said nothing ---
  `lenet-L1-28-c1-k5/bq-expand` and its adjacent twin come out at **54.10
  against 53.95 us an iteration, 866206 against 866252 instructions, 1102.6
  against 1106.4 cache misses, 19.9 against 21.0 dTLB misses**. Everything
  inside a third of a percent but the dTLB, which is 5% on a base of twenty.
  A filtered process has no allocation history and a clean pool, so there
  was nothing for the effect to arise from; the null is consistent
  with the surviving account rather than against it. Three things it does buy:
  the **instructions agree to 5e-5**, which is the first instruction-level proof
  that an A/A pair is the same work and the control row that must stay flat when
  the effect does reproduce; a per-call counter baseline for that bench
  to compare a wild cell against; and **criterion's slope confirmed
  by an instrument sharing no code with it**, 54.10 us against the 53.46
  that half published, 1.2% apart. Seconds, and no quiet machine: counter ratios
  between two arms do not move because something else is running, where
  a wall-clock figure would.

  **The mechanism itself is tested by logging what it names**, per bench:
  the RTS's allocated-bytes total and the payload addresses. That is a `Main.hs`
  edit and belongs **after the current pair is spent**, since it changes
  the module's code, so its `.text`, so every loop offset, and would invalidate
  the md5s that pair's note records for binaries already built. **What
  it no longer waits on is a wild cell, 2026-08-14.** The `scaled` A/A slot
  shares this signature --- one arm, one process, identical work, the difference
  in mutator time and the state kept once entered --- and turns up in six runs
  of seven, where a wild cell is a lottery; so the mechanism can be instrumented
  there on demand, and a wild cell only decides whether the large instance
  is caught too. The two differ in where the state is entered, mid-bench there
  and before the bench here, which is why **the logging is per sample
  and not per bench**. And addresses are the right thing to log for a reason
  the decomposition supplies: allocation is identical to the byte in both
  instances, so the cost is per access rather than per allocation.
- `PARKED` **`mut-odo`'s wide interval on `micro-aligned` is, at sample level,
  the `build`/`mut-odo` pair scattering together --- a measurement without
  a mechanism.** The interval reproduces and belongs to that binary: CI% 1.06,
  1.09 and 1.15 in three independent processes on it --- Run 10's main set
  and both gate passes --- against 0.72 and 0.19 on `micro-maxskip` (2026-08-11,
  arithmetic over the run and gate artifacts, no machine time). The CI% column
  reads it as one arm's, `build`'s interval moving only 0.30 to 0.39 ---
  an artefact of the interval, which is sampling error about a fitted line
  and not stability: taking each cell's residual about its own line, per
  iteration, as a fraction of that cell's slope and medianing over shapes,
  `mut-odo` scatters **21.9%** on the aligned half and `build` **32.7%**,
  against `mut-odo-vecdims`'s 3.1% and `list`'s 3.2% --- an order of magnitude,
  `build` the worse of the two where its *interval* is much the narrower (CI%
  0.44 against 0.82) --- and both roughly halve on the max-skip half, 11.1%
  and 22.8%, where `list` and the vecdims arms barely move (2026-08-12,
  arithmetic over Run 11's two main sets). The same pair, behaving together,
  on the same two binaries as [the 3% that survives alignment][open]; kept
  because the two instruments will disagree again, and the scatter is the one
  to believe.

  **Three accounts are closed at sample level, the refit reproducing criterion's
  slope to 1e-15 first**: the residual correlates with `measNumGcs`
  and `measGcWallSeconds` at +-0.00 in every process, so it is not the block
  pool; with sample index at +-0.03, so it is not drift the slope missed;
  and allocation per iteration is constant. Nor is it shape-localised, two
  passes of one binary sharing no widest shape. What is left is dispersion about
  the line that no recorded covariate explains, on one arm, on one binary ---
  and thinner than the three readings suggest, per-cell dispersion swinging
  several-fold between passes and the comparison binary's own median moving 3.7x
  between its two.

  **Run 11 reproduced it a fourth time and turned it into a different
  question.** The same arm at the same slot in the same binary reads CI%
  **0.82**, against 0.31 on `micro-maxskip` --- so the split between
  the binaries survives, at three quarters of Run 10's separation. What is new
  is that `mut-odo` is also **the arm that drifts most across the repetition**,
  1.0327 where every other arm bar its own code twin is inside 1.5%, with cells
  at 1.1577 and 1.1467; `build` is second at 1.0095 with a 1.2471 cell. Two arms
  sharing one worker, at offset 0 in both runs, moving together and moving more
  than the roster: the wide interval and the wide drift are one arm's,
  and placement can no longer be either's account. What would separate
  a dispersion belonging to the *worker* from one belonging to the *slot*
  is a run with the two arms' roster positions exchanged --- which asks
  for an aligned build, a form this README has moved past ([the tasks' closing
  ruling](#recommended-tasks-after-run-19)).
- `OPEN` **A second instrument says different arms are unstable, and the two
  disagree --- which is the finding rather than something to average.**
  The entry above prices instability by the `CI%` column, which is sampling
  error *within* one benchmark. A pair's two halves supply another: each arm's
  spread of per-shape ratios between them, as the standard deviation of their
  logs, which prices disagreement *between* processes. Run 13 raised it
  and it is not that run's alone. **Measured on the three pairs whose two main
  sets are both on disk** --- Run 11 aligned against max-skip, Run 12 max-skip
  against `+procalign`, Run 13 max-skip against `lookrts` --- `offtab` ranks
  3rd, 2nd and 1st, `build` 2nd, 3rd and 3rd, and `offtab`, `build`,
  `gen-unsafe` and `bq-gen` sit in the widest six of all three. So it
  is a stable property of the arms and not an accident of one pair. **It
  is not sampling error**: against `CI%` it correlates at r +0.69, and `list`
  refutes the account outright, having the fewest samples of any arm
  and a *higher* `CI%` than `offtab`, `mut-odo` or `build` while its spread
  is a third of theirs. These arms are measured precisely inside a process
  and disagree wildly between them. **And the two instruments name different
  arms**, which is why this is an entry: `offtab`'s interval is an unremarkable
  0.74 in both halves, so the interval reads it as an arm that does not follow
  the phenomenon --- true of the interval, and false of the spread, where
  it is the worst arm in the roster in all three pairs. That account is built
  on the `build`/`mut-odo` code twin; the phenomenon is wider than the twin
  and its most consistent member is not a code twin at all. **Two things would
  settle it, and only the second wants a machine.** Correlating the per-shape
  spread against `sInner`, `l`, `m` and rank, and asking what those four arms
  share --- they are not a tier, `offtab` carrying mutable `Int` scratch,
  `build` a class-method fill and the other two pure, so a negative answer
  is informative --- is arithmetic over kept artifacts. Separating position
  from code for them wants a *twin* on one of them, which no run has had:
  through Run 13 the A/A gate covered three of the twenty-four timed strategies
  and none of these --- the same coverage gap the wild-cell entry above names
  from the other side. **The roster change is made, 2026-08-14**: `offtab`,
  the ranking's most consistent member, carries twins in both positions, so Run
  14 reads its position against its code directly. The three-pair reading
  is possible only while those runs' main sets are kept. **What it is measuring,
  asked over all three pairs and answered in part** (2026-08-14, arithmetic
  over the six kept main sets). Ranking arms by the stdev of their per-shape
  cross-half log ratios reproduces this entry's order at the top --- `offtab`
  7.6%, `mut-odo` 6.9%, `build` 6.9%, `gen-unsafe` 6.5% --- with `gen-quotrem`
  at 5.8% taking the fifth place recorded for `bq-gen`, which reads 4.7%
  and sixth. **They are not a speed tier**: the wide arms span 2.4 to 17.0 ns
  an element, and the two narrowest arms in the README are its fastest
  and its slowest, `mut-odo-vecdims` at 1.2% and `list` at 2.0%. What three
  of the four share is a shape law the `CI%` instrument has no counterpart
  for --- disagreement grows as the runs shorten and the rank rises,
  the Spearman of |log ratio| against `sInner` reading -0.64 on `build`, -0.58
  on `offtab` and -0.55 on `bq-gen`, against rank +0.51, +0.11 and +0.34 ---
  so what is being priced is the placement of the per-run work rather
  than of the per-element work. `gen-unsafe` is flat against every dimension
  and is therefore wide for some other reason, which is the negative answer
  this entry asked to have either way. **One arm is left over from Run 17
  and is still unread, kept here because the registration that raised
  it retires**: `bq-scan-rem-gm-mulback` moved **1.0419** across that run's flag
  change, slower on **all 24 shapes** at per-shape ratios of 1.0203 to 1.0704
  with both twins slower on 23 of 24 --- a consistent 4% and not a scatter,
  on an arm the layout account does not cover. That run named it the one thing
  a later run should re-read, and none has.

  **Run 15 adds a fifth pair, and its two readings disagree --- which is itself
  this entry's point.** Its two HALVES do *not* reproduce the finding: across
  them the widest timed arms are `gen-unsafe` at 0.2395 and `list` at 0.2381,
  then `list`'s two twins at 0.2366 and 0.2302, `gen-unsafe`'s adjacent twin
  at 0.2251 and `gen-quotrem` at 0.2242 --- and `offtab` falls to 13th of the 42
  the reader compares. That is the pair's own variable showing through rather
  than the arms' instability --- a 32 MB nursery moves `list` and the `gen-*`
  arms per shape, so this pair prices the nursery and not the instrument.
  Its REPETITION against Run 14 does reproduce it, and with no shim *setting*
  and no compiler flag between the sides: `mut-odo-aa-adjacent` 0.1088,
  `build-aa-adjacent` 0.1003 and `offtab-aa-distant` 0.0933 take the widest
  three timed slots, `build` 0.0899 and `mut-odo` 0.0812 next --- three
  of the four arms this entry names, each with a twin beside it. The fourth
  and fifth do not follow: `gen-unsafe` reaches only 8th, through its adjacent
  twin at 0.0741, and `bq-gen` 14th at 0.0478. **So the instrument wants a pair
  whose variable does not act per shape**, which the three earlier pairs
  were and neither nursery pair is. Two further readings from the repetition:
  `offtab` moved +3.62% and `offtab-aa-adjacent` +4.63% while
  `offtab-aa-distant` moved +0.03%, two A/A twins of one arm 4.6 points apart
  between runs; and `mut-odo-aa-distant` carries this run's basis floor
  at 2.32%. **And the build's share of that is now bounded rather
  than guessed**: timing the two runs' binaries against each other in one window
  puts them at most one or two percent apart on `offtab`, with `list` and both
  twins moving together by under 1.3%, and an A/B/A/B that does not converge ---
  0.9976 then 1.0209. So the arms' own width carries most of the 3.62%, which
  is what this entry prices. A three-rep repeat then measured that width
  directly: `offtab`'s alone leg alone spreads 21% across three processes of one
  binary at `-A32m` (2026-08-18,
  `small-pinned-churn-investigation/nursery-position-findings2.txt`),
  so no single-process reading of the arm means anything.
- `ANSWERED` **What the eight stride classes are worth as instruments --- read
  against each other for the first time on 2026-08-14, over Runs 10 to 13.**
  The ruling is that what they differ in is not a class property: in every one
  of the eight the *distant* twin is the slower half, and that is a confound
  in the crossed design rather than an instrument reading, every distant twin
  having sat in its group's first dozen slots with its base later, so *distant*
  has always also meant *earlier*. The per-class figures, the four changes
  that followed the same day and the check that each class's shapes satisfy
  its defining property are in [the stride classes and what they
  cover](#the-stride-classes-and-what-they-cover).
- `OPEN` **`scaled`'s A/A slot is real and its size is not: six runs of seven
  find a disturbance at the `mut-odo-vecdims` slot on `scaled-super-r3`,
  its magnitude never repeats, and the ruling is to quote the slot as a hazard
  of the class and never as a figure.** What stays open is the raw disagreement
  under it, which had no account until the sample-level reading at the end
  of this entry. The account below is Run 10's, where the arithmetic half
  was derived; the runs since are at its foot. On Run 10 both `mut-odo-vecdims`
  pairs read below 1, 0.9464 and 0.9574, both worst on `scaled-super-r3`, while
  the other four pairs in that process sat within 0.25% --- and it was the base
  arm that was slow, not the twins. **Two thirds of it is arithmetic
  and was mine to divide out before calling it a disturbance.** The raw slopes
  disagree by 2.13%; the forcing term is 59.8% of this bench, the largest share
  in the run; and 1/(1-f) turns the first into a predicted 5.29% against
  the 5.36% read. So the arm's cells are 2% apart, not the 11% the published
  pair suggests. The raw sample lists say nothing further is wrong: R2
  is 0.99995 or better on all four arms and there is no ramp the slope has
  not already handled. What survives is a 2.13% raw disagreement at one slot
  on one shape, against 0.17% raw or less for the four other pairs in the same
  process --- smaller than it looked and still this slot's. It also inverts Run
  9's wild cell, where the *twin* was slow and roster warmth was the account:
  the distant twin here is the earliest of the three and is the clean one,
  so that story does not transfer. **Do not reach for a filtered re-run
  of the six controls**: filtering collapses the spans the crossed design needs,
  which [the floor section][floor] records as making a span unmeasurable. What
  can be asked is Run 11 reading this population with layout pinned. **Read
  at sample level on Run 13, and it is neither a ramp nor an outlier
  but a step** (2026-08-14, `run13-maxskip-scaled.json`, the refit reproducing
  criterion's slope to 2e-16 first). The disturbed arm runs at its base's speed
  --- 58.106 against 58.06 us an iteration --- for 69 of its 89 post-ramp
  samples, then steps once to 60.700 and stays there, **+4.46%**, 1.69 s
  into a 4.72 s bench. Across that step allocation per iteration is identical
  to the byte at 480561, GC count per iteration is identical at 0.111,
  and the peak heap does not move from 28 MB; what carries the cost is mutator
  time, 60.4 against 57.8 us. The other five A/A pairs in that same process read
  within 0.25%. The signature repeats where the artifacts survive: the twin's
  last quartile jumps on Run 11 (58.27, 58.41, 57.23, **61.44**) and on Run 13
  (58.03, 58.17, 58.11, **62.03**), Run 12 is a mild 1.7%, and **Run 10 carries
  it on the base arm instead** --- 57.38 rising to 60.37 with the twin flat ---
  which is why the ratio moves in either direction and why the magnitude never
  repeats. A state the process enters once and keeps is the block-pool report's
  signature rather than a scheduling lottery's, so **the mechanism entry's
  logging wants to be per sample and not per bench**: a per-bench figure
  averages the two states it exists to separate.

  **It has, and the answer is that the slot is real and its size is not.** Run
  11 reads this class's floor at **3.27%** --- still the run's worst, still
  the `mut-odo-vecdims` slot, still worst on `scaled-super-r3`, so four runs
  of five have found a disturbance at one slot on one shape and a pinned layout
  does not remove it. What did not survive is everything about its magnitude:
  the pair that carries it swapped, the *distant* one reading 1.0327 where
  the adjacent one is clean at 1.0020, and the sign inverted, both having read
  *below* 1 in Run 10. The arithmetic half reproduced exactly --- raw 1.25%
  at `f` 0.609, so 1/(1-f) predicts 1.0320 against the 1.0327 published ---
  which is the account above holding while the quantity it explains moves by two
  points between two runs of one binary. So quote this slot as a hazard
  of the class and never as a figure, and treat a margin under about 3% here
  as unmeasured. **Two more runs have since found it, and the ruling
  is unchanged.** Run 12 read the same distant pair at 1.0151 on a worst cell
  of 3.74%, and Run 13 at **1.0547** on a worst cell of **11.59%** ---
  the largest recorded there and the worst A/A cell anywhere in that run. So six
  runs of seven have found a disturbance at this one slot on this one shape, Run
  9 the only exception, and the arithmetic half reproduces a third time: raw
  1.0212 at `f` 0.608, so `1 + raw/(1-f)` predicts 1.0540 against the 1.0547
  read. What goes on moving is the magnitude alone --- 5.36%, 3.27%, 1.51%,
  5.47% across Runs 10 to 13, each the class's floor and not its worst cell ---
  which is exactly what this entry already says and is why the ruling needs
  no revision: the slot is real, its size is not, and the amplification
  is arithmetic rather than a second effect.

  **Run 15 found the slot clean and the shape disturbed, which is the sharpest
  form this ruling has taken.** On its basis half the `mut-odo-vecdims` pairs
  read 0.9940 and 0.9968, worst cells 1.53% and 0.60%, both worst
  on `scaled-rank1-m1` and neither on `scaled-super-r3`; only Run 9 had done
  that, so six runs of eight found the slot disturbed --- and Run 16 finds
  it again, at 1.0219 on a worst cell of 7.27%, which makes it seven of nine.
  The shape gets no reprieve from it --- `scaled-super-r3` carries the worst
  cell of ten of that process's eighteen A/A pairs and all four of the largest,
  `gen-unsafe-aa-distant` 11.76%, `mut-odo-aa-adjacent` 9.71%,
  `gen-unsafe-aa-adjacent` 9.60% and `build-aa-distant` 8.05%. **So on Run 15
  the shape repeated and the arm did not** --- and **Run 16 retires
  that sharpening** (2026-08-20): there the arm's slot is disturbed again while
  `scaled-super-r3` carries the worst cell of only three of the eighteen pairs
  against ten here, and neither of the two largest. Neither the arm
  nor the shape repeats reliably, so the ruling reverts to its older and weaker
  form, which is that this is a hazard of the class to be quoted as one
  and never as a figure. The per-sample reading stays the instrument
  for its mechanism.
- `OPEN` **The basis half carries the wider class floor, run after run,
  and no variable the pairs differ in explains it. It carries the faster level
  too, and on the one class tested both survive having the halves' order
  swapped.** Over Runs 15, 16 and 17 the published half's class floor
  is the wider one in **18 of 24** comparisons --- 5, 7 and 6 of eight classes
  --- at sign p 0.023, and those three pairs differ in three unrelated things:
  an RTS setting (`run15-lookrts` against `run15-a32m`), an allocation area
  (`run16-a32m` against `run16-a64m`) and the per-sample instrument
  (`run17-wildlog` against `run17-det`). So it is none of the three, and what
  the wider halves share is being the half whose column got published. **Run 18
  goes the same way and strengthens it**, counted 2026-08-23 over its own eight
  classes: **6 of 8**, taking the running count to **24 of 32** and the sign
  test from p 0.023 to **p 0.007**. The one figure to take from a class here
  is its FLOOR, the max over its eighteen A/A pairs, which is what `--block`
  prints and what the class table's floor column carries --- not `read-all.sh`'s
  A/A worst-cell column, a max over cells, which for `run18-g912-slice` reads
  13.22% where the floor reads 6.01%. Counting this with the worst cell instead
  gave 4 of 8 and a weakening p, twice, before the two figures were told apart.
  Run 17 is where it is loudest: `revsome` reads **18.05%** on the basis against
  4.87% on the control, three times its own Run 16 figure, and that movement
  is what raised the question --- the paragraph that used to state such
  movements under the class table was cut on 2026-08-22 for quoting the previous
  run's, and its subject is here instead. **The measurement it registered
  was taken 2026-08-23, wanting no quiet machine and no new run, and the first
  branch fired.** The floor is a MAX over eighteen pairs, so a half with one
  wild cell carries a wider one at the same dispersion; read the median A/A
  deviation per half beside it, over the same JSONs, and the two halves
  are alike --- the basis is wider on the median in **9 of the 24** comparisons
  at sign p 0.31, against **18 of 24** at p 0.023 on the max. **So the ruling
  is that a floor is an order statistic and not a spread**, and what
  is asymmetric between the halves is the tail rather than the dispersion:
  the basis half carries the wilder cell, not the noisier roster. **Run 18
  then found the same asymmetry in the LEVEL, once the intrusion was rerun out
  of its way**: all eight class geomeans put the basis half faster, **0.9866
  to 0.9949**, on 198 of the 336 arms, where the pre-rerun figures straddled 1
  and showed nothing. That retires the dispersion candidate and leaves
  the evening's process order, which the artifacts can still answer, every
  process being timestamped --- the control half having run first in every pair
  of Run 18 and in both of its windows, so *which half it is* and *when it ran*
  name the same nine processes throughout. **The measurement that separates them
  was taken 2026-08-23 on `slice`, and it SPLITS this item.** The pair was run
  again with the halves' order reversed --- `g912` first, `g914` second ---
  on the same binaries, the same switches and the same evening, both halves
  clean of foreign CPU and both baselines inside the 0.7%. **The LEVEL follows
  the half.** `g912` is faster in both orders, at 0.9937 running second
  and **0.9878** running first, so reversing the order neither reversed the sign
  nor narrowed the margin --- it widened it, which is the opposite of what
  a second-is-faster position effect predicts. Position is refuted for the level
  ON THIS CLASS, and what is left there is the compiler and its boot libraries;
  the other seven were not reversed, and that every one of the eight leans
  the same way is what makes the reading worth carrying to them rather than what
  establishes it. **THE FLOOR FOLLOWS THE HALF TOO.** `g912` carries the wider
  floor in both orders --- **6.01% against 3.30%** running second, **3.41%
  against 1.79%** running first --- so position is refuted for the floor
  on this class as it is for the level, and the two halves of this item point
  the same way rather than apart. That WEAKENS the position candidate; it does
  not retire it, being one class of eight on one run of four, where
  the dispersion candidate was retired over all 24 comparisons at once. A second
  class reversed is what would, and it is the same measurement the level half
  wants --- one run of two processes answering both. If it holds, the item
  is left where it started with less in it: over Runs 15 to 17 the halves
  differed in an RTS setting, an allocation area and an instrument, all three
  already excluded, and the slot would join them, leaving the wider halves
  sharing nothing but having been the published one. **Read a class margin
  against its own run's column and never the previous one** --- the standing
  rule the cut paragraph carried.
- `OPEN` **What does the roster owe the next run?** The exact repetition
  is **taken** and is not owed again for its own sake: Run 11 inherited shapes,
  roster, order, regime and binary, and what it bought is [in the floor
  section][floor] --- a drift band a quarter of the one this README had
  been quoting, and every claim reproducing on it. What the roster owed
  is the third `-nosum` arm the queue holds, deferred out of Run 11 so
  that its membership stayed pinned and out of Run 12 so that it did not arrive
  in the same run as a change of shim. **It is now written**,
  as `mut-flat-gm-nosum`: a `Force` pair on the flat fill, the third shape
  of fill after the odometer and the expansion, which is what lets gate 3 tell
  a biased read from two biased arms. It sits beside its base, as both other
  `Force` pairs do, so its difference is taken between neighbours. **Both debts
  are now paid, on 2026-08-13.** The membership-invariance check Run 12's basis
  choice made due --- max-skip pads only the heads that need it, so an arm's
  arrival is not guaranteed to leave every loop where it was --- comes back
  clean: rebuilding the basis recipe with the arm leaves **every tracked loop
  at the same address**, fills `[11, 0, 4, 0]` and `[24, 8, 0, 0]` either side,
  32 self-loops in 25 distinct byte-sequences both times, and the roster grows
  by exactly the 24 cells the arm adds, 816 to 840. **Read that as the weak form
  it is**, though: a `Force` arm reuses a function the roster already
  references, so it emits no new code and emission order has nothing to reorder
  --- an addition that brought a *new function* would be the stronger test,
  and is what a later membership change should be read against. **Both fell due
  again for Run 14 and are PAID: the roster gained twelve A/A twins
  on 2026-08-14** --- `offtab` and `bq-odo-gm-mulback` first, then `build`,
  `mut-odo`, `list` and `gen-unsafe`, each in both positions, 840 benches
  to 1128 --- so that run owes the `-L1` pass and the invariance read, still
  the weak form, a twin reusing a rostered function and emitting no code. **Both
  were taken before the evening and both came back clean**, the `-L1` pass twice
  --- the first on a roster that five class shapes and a moved twin
  then replaced, which is the trap that line exists to catch ---
  and the invariance read holding every tracked loop at its address across both.
  What the twelve twins then did to the run is not a debt but a finding: they
  took the A/A population from six pairs to eighteen and the floor
  from a fraction of a percent to 2.19%, because the new ones sit
  on the widest-spread arms. A floor is a property of the arms it is measured
  over, and this is the run that made that visible. **The invariance read
  was taken on the 936-bench tree, 2026-08-14, and came back clean**: rebuilt
  from it, both recipes held every tracked loop where Run 13's binaries have
  it --- fills `[11, 0, 4, 0]` and `[24, 8, 0, 0]`, at the same addresses,
  on the `lookrts` recipe Run 14 makes its basis and on the max-skip one beside
  it, whose `.text` also came out at 20377797, the size that pair note records.
  **Taken again on the final roster, 2026-08-14, and clean there too**: the same
  build holds those loops at those addresses with `.text` to the byte, five
  class shapes and a moved twin later, which is what a shape being data
  and a twin reusing a rostered function predict. **The `-L1` pass was taken
  twice for the same reason** --- the first covered a roster that five class
  shapes and a moved twin then replaced, which is the trap that line exists
  to catch, a pass recorded for a roster that no longer exists. The second
  covers the main set and the `scaled` class, chosen because it is one
  of the five that crossed from two shapes to three, so `--block`'s three-shape
  branch is exercised for the first time; every reader mode exits 0 on both
  files, which is what that pass is for. It also settled the one slot claim
  this roster change made on an argument rather than a measurement:
  `list-aa-adjacent`, the single entry inserted above the distant twins,
  allocates 134261336 bytes a call against `list`'s 134261403, agreeing
  to 1.1e-4 over all 24 shapes, where `sum-only-early` --- the bench the slot
  rule is about --- allocates 204 bytes a call, its allocation being a one-off
  setup vector. So the twin fills as its base does and grows no pool the way
  that bench does. Its readings are with the pair note, and its timings go
  nowhere, `-L1` being a rougher budget than any recorded run's. The arm's own
  reading is [with gate 3](#what-is-open), taken filtered; Run 13 took
  it at full budget, and its Results row's `needs` cell reads *the same,
  on a third write pattern* --- the control convention, not the shippability
  phrase this entry first proposed. **A return to -O1 stood behind it
  as the second debt and is retired, its premise being false** (2026-08-14): -O1
  is not the regime the claims are read in, `-fspec-constr` being the basis
  every run since Run 8 has used, so Run 7's claim set is history rather
  than a debt. The build specification that entry had accumulated goes with it,
  a retired run having no use for one. An -O1 reading of a single ordering stays
  available as a filtered probe, as the 2026-08-08 twin probes were; what
  is retired is the evening. `--check-doc` enforces the yardstick's shape
  in the one direction it safely can: a run named aligned must also be named
  unaligned, so dropping Run 10's unaligned column fails the check. Dropping
  an *aligned* one cannot be checked, an unpaired run being what every column
  before Run 10 is, and stays the reading's job.

  **Run 11 had no unaligned half, and the check was left alone rather
  than widened --- the reading is that this was right.** Its two columns
  are `Run 11 (SpecConstr, aligned)` and `Run 11 (SpecConstr, max-skip)`,
  and `--check-doc` passes on them, the rule asking that a paired run publish
  a column per half and not one. Widening it was the alternative and is refused:
  the check would then have to know which half names count as a counterpart,
  which is a list that grows with every pair and is wrong the first time one
  is invented. Keep a basis column named `aligned`; name the other half
  for its shim.
- `ANSWERED` **At a large nursery an earlier bench in the same process
  permanently slows a later one --- the condition is named SMALL-PINNED CHURN
  and its cost the churn tax.** Churn of sub-3276-byte pinned allocations,
  the shared-accumulator size class: Run 14's probes found it (2026-08-15/16),
  the ladder is flat at `-A4m`, and the victim's added cost is mutator LLC
  misses at flat instructions and dTLB, the counter signature that has held
  through everything since. **It is not the pinned-spray pool condition of GHC
  work item 27601**, by controls and by a conceptual objection that stands,
  and everything reproduces on GHC HEAD where that issue is itself unfixed.
  The account is in [the floor section][floor]; the measurements, their tables
  and the recipes to re-take them
  are `small-pinned-churn-investigation/nursery-position-findings2.txt`'s.

- `OPEN` **One residue of the small-pinned churn, one answered, neither blocking
  its filing.** Open, and since 2026-08-21 no caller's, every horde-ad suite
  running at `-A32m`, so the residue belongs to the filing rather than
  to this README: the `-A1G` alone transient's micro-mechanism --- early
  and late iterations carry EQUAL cache-miss and dTLB counts per iteration while
  cycles differ ~17%, so the fresh-heap advantage is in miss cost or overlap,
  not count --- and the instrument that would name it, load/store-split
  or `perf mem` sampling, is unavailable on this machine (no IBS exposure;
  findings item 58). Answered: the added misses at `-A4m` are mutator-side,
  the collector's own symbols carrying ~1% of samples in every cell,
  so the conceptual objection above stands measured (item 56).

- `PARKED` **`mut-odo-vecdims-add-in` leads `mut-odo-vecdims` on most
  populations, and Run 18 read the margin outside a floor on one compiler
  and absent on the other.** Registered here 2026-08-22, out of Run 17; parked
  2026-08-25, the ruling being the last paragraph of this entry. The series
  is [under Results](runs/run19.md#results): `add-in` against the arm it varies
  read 1.0009, 0.9934, 0.9967, 1.0023 and 1.0043 across Runs 10 to 16, four
  of those five a coin flip, and Run 17 reads **0.9889 at 19 of 24, sign p
  0.0066** on its basis and **0.9709 at 21 of 24, p 0.00028** on its control.
  **What is new is not the margin but the agreement**: the two halves differ
  in `.text` and in every loop offset, `add-in` is itself moved 1% across them,
  and both put it ahead --- so the direction is not the slot, which is what
  the four coin-flip runs could not rule out. Per population it leads the main
  set, `rev`, `revsome`, `bcastmid`, `slice`, `window` and `scaled`,
  `mut-odo-vecdims` keeping only `bcast` and keeping it by 0.9989. **What
  it is not is decided, and the two halves disagree about that too.**
  The threshold for a margin between two arms of one run is that run's own
  restricted six, which on Run 17 read 1.31% on the basis, where the margin
  is 1.11% and so does not clear it, and 0.56% on the control, where 2.91%
  clears it more than fivefold. Against the eighteen-pair floor --- the wrong
  quantity here, and the one this entry first used --- neither would clear.
  **TAKEN 2026-08-22, the same evening, and it confirms the direction.** Both
  arms in ONE process --- so the pair shares its placement --- at a fixed
  iteration count, three fresh processes a cell over `cnn-slice-c32`,
  `cifar-L2-16-c64-k3` and `stretch-wide-2xM`, per-call mutator time read off
  the run's own per-sample instrument because criterion's fixed-iteration mode
  prints no per-bench figure and writes no JSON. `mut-odo-vecdims`
  over `mut-odo-vecdims-add-in` reads **1.0227, 1.0186 and 1.0039** by shape
  and **1.0151 over the nine processes, 8 of them above 1** --- the same
  direction as the roster's 1.0112 and slightly wider, on a route that owes
  criterion's estimator nothing and shares a process, so no *per-process*
  placement term survives it --- but the two arms sit at different cache-line
  offsets, 0 and 24, and that difference is static and survives every route
  here. At 1.51% it clears the basis's 1.31% six-pair threshold. GC is 0.015%
  of mutator on these arms, so reading mutator rather than wall changes nothing
  here. **What it does not cover is the control half**: the probe reads
  its timing off the instrument, which `run17-det` does not carry, so the nine
  `det` processes ran and said nothing --- a route that works only
  on an instrumented binary, which is worth knowing before the next one
  is designed. **The gap that left was closed the same evening**, by the same
  paired design in criterion's own mode rather than at a fixed count, which
  needs no instrument to read and so runs on both halves: three fresh processes
  a cell over the same three shapes. On the uninstrumented `run17-det` it reads
  **1.0171 over nine processes, 9 of 9 above 1** --- `cifar-L2-16-c64-k3` alone
  giving 1.0374, 1.0395 and 1.0386, a figure past every floor in this README ---
  and on `run17-wildlog` 1.0059 at 8 of 9. **So five readings on two binaries
  by three routes all put `add-in` ahead**: the basis roster at 1.0112 (19
  of 24, sign p 0.0066), the control roster at 1.0300 (21 of 24, p 0.00028),
  the fixed-n paired probe at 1.0151, and these two at 1.0171 and 1.0059.
  The magnitude is context-dependent and spans 1.0059 to 1.0300; the direction
  is not, and 1.71% on the uninstrumented half clears that half's 0.56% six-pair
  threshold threefold. **But placement is NOT excluded, and the offsets
  are the reason to suspect it.** The two arms share one 28-byte body and sit
  at different cache-line offsets: on Run 17, `fbMutOdoVecdims` at **0**
  and `fbMutOdoVecdimsAddIn` at **24**, named off the `-g3` twins and identical
  in both halves, since the patch shifts `.text` by 4096 bytes and these two
  loops by 6912, both whole multiples of 64. So every reading above is one draw
  on their placement rather than five. **Run 17 is the first run to move
  these two arms off the offsets they had held**, and the history is recorded
  rather than inferred: Runs 12 and 13 each named the vecdims four off a `-g3`
  twin and matched them by byte identity, both putting **`mut-odo-vecdims` at 24
  and `-add-in` at 8**, and `run16-a32m` carries the same arrangement
  `[24, 8, 0, 0]`. Run 17 carries `[0, 24, 0, 4]`, so the pair now sits at **0
  and 24** --- measured on this run's own twins, on both halves. All four copies
  *fit* their line in every one of those runs, so any effect here
  is the resident-offset kind rather than the straddle Run 10 priced at 12
  to 14%, the kind [this list already calls narrowed and not settled][open].
  **But the offsets do not sort the readings, and one run says so outright**:
  at the old 24-and-8, Run 13 read the pair at 0.9934 on **21 of 24** ---
  as strong a lead as Run 17's --- while Runs 14, 15 and 16 read coin flips
  at those same offsets. So three of the seven readings put `add-in` decisively
  ahead and four do not, across *two* offset arrangements, with the split
  falling inside one arrangement as well as across the change. Placement
  is therefore not excluded and not established either; what the offsets do
  is make it un-excludable by anything measured so far. **And the two arms
  are NOT the same code, which the machine code settles and a Core reading
  of 2026-08-09 had already predicted.** Their innermost loops
  are byte-identical --- the same eight instructions in 28 bytes, which is why
  `loop-offsets.py` groups all four family arms as copies of one body ---
  but the worker containing that loop is not: `$wgo7` is **328 bytes
  in `mut-odo-vecdims` against 296 in `-add-in`**, and the control carries
  an `imul` in its outer path that the sibling does not. Over each arm's whole
  code the two run 3472 bytes against 3424, 929 instructions against 927, two
  `imul` against one --- so that single multiply is very nearly the entire
  difference between them, and [the ceiling section][ceiling] carries the same
  measurement for all five family arms, no two of which share their whole code.
  That is exactly what [the ceiling section's Core
  reading](#the-mutable-ceiling-taken) recorded in 2026-08-09 --- *one multiply
  becomes an accumulated add threaded as a further argument*, a per-run change
  and not a per-element one --- now confirmed at the instruction level
  in the shipped `-fspec-constr` regime, and **in the timed binary and not only
  the `-g3` twin**: one `imul` in a window around `mut-odo-vecdims`'s loop
  and none around `-add-in`'s, in `run17-det` exactly as in its twin.
  So the direction has a mechanism, and it is the mechanism the family was built
  to expose: `add-in` does strictly less arithmetic per run. **What
  the mechanism does not explain is the size.** A per-run cost should track
  `sInner`, and it does not: over the shapes carrying one, the correlation
  of the log ratio against log `sInner` is **+0.04** on the basis and **-0.41**
  on the control, weak and not agreed even in sign --- the same flatness Run 9's
  readings showed and Run 10 could not account for either. **So the ordering
  is code and the magnitude may still be part placement**, and the two questions
  want separating. **What would settle the placement half** is Run 10's method
  aimed at these two arms: one source, two builds a shim setting apart, chosen
  so the pair's offsets swap or converge, read on nothing but `mut-odo-vecdims`
  against `mut-odo-vecdims-add-in`. If the ordering follows the offsets
  it is placement; if it survives them the arm is really faster. That is two
  twenty-second builds and a filtered probe, and it needs no run. Artifacts
  `probe-addin-*` and `probe-addin2-*`. **DEFERRED TO A FUTURE RUN by decision
  of 2026-08-22, and the decision is about what could change the shipping choice
  rather than about the probe's cost.** A margin of one to three percent does
  not move it: the regime 3 fix is not chosen on differences that size,
  and no reading here or in a probe of this kind will be larger. Nor
  is it chosen before the compilers the library's consumers build with have
  been measured --- GHC 9.14, which is Run 18's own subject, and HEAD after
  it --- since an ordering that holds on 9.12 alone is not the ordering
  the shipped code will meet. So the placement half waits for those, and until
  then the decision of 2026-08-22 stands and ships `mut-odo-vecdims`. What
  the entry is for is that the next run should not rediscover the lead
  as a surprise, nor spend an evening on it.

  **PARKED 2026-08-25: the condition that deferral named has been MET
  and the question is retired anyway, so no run and no probe will be built
  to answer it.** GHC 9.14 was Run 18's subject and HEAD was Run 19's, which
  is what the deferral waited for, and both put the orderings where 9.12 does
  --- so the placement half came due and was declined rather than deferred
  a second time. The reason is the deferral's own and has only got stronger:
  the margin is one to three percent, the regime 3 fix is not chosen
  on differences that size, and no instrument of this kind will read larger,
  so the answer cannot move the shipping choice whichever way it comes out. What
  is given up is knowing WHY `add-in` leads -- code or slot -- and
  that is knowingly given up. **Do not re-propose the two-shim pair, and do
  not let a run carry it as a rider**: what the entry keeps is the reading,
  so a later run meeting the lead again finds it recorded rather
  than surprising, and so that a run wanting a pair for something else
  is not told this one is owed.

  **RUN 18 ANSWERED THE HALF THIS ENTRY DEFERRED, and the answer is
  that the lead is the compiler's.** On one source, one shim and one roster,
  `add-in` against the arm it varies reads **0.9813 at 19 of 24, sign p 0.0066**
  on the 9.12 half --- the third run-reading in a row to put it ahead,
  and the fifth of the nine overall --- and **1.0016 at 14 of 24, p 0.54**
  on the 9.14 half, which is a coin flip and the wrong side of 1. The margin
  does not shrink on 9.14; it is absent. Against each half's own restricted six
  --- 0.54% and 0.31%, less than half Run 17's --- the 9.12 reading clears
  its threshold more than threefold where every earlier run had it inside
  a floor or barely past one, and the 9.14 reading has nothing to clear.
  **That is the condition this entry itself named**: *an ordering that holds
  on 9.12 alone is not the ordering the shipped code will meet*, and it holds
  on 9.12 alone. Per population the split shows too --- `add-in` heads the main
  set, `rev`, `bcastmid`, `slice`, `window` and `scaled` on the basis, six
  of nine, with `mut-odo-vecdims` itself taking `revsome` and `add-both-down`
  taking `bcast` --- but every one of the eight class margins is inside
  its population's floor, as they have been since Run 16, so the main set
  is again the only population that says anything --- and its own 1.87%
  is outside both of its floors, which is the point of the paragraph above.
  **AND THE `-g3` TWINS SETTLED THE PLACEMENT HALF THE SAME DAY, which
  no earlier run could do, because this pair swapped the offsets for free.**
  Named off a twin per compiler and matched to the timed binaries by byte
  identity and by the count check --- four copies in each twin against four
  in each timed binary, at the same offsets mod 64 --- the two arms **swap
  cache-line offsets between the compilers**: 9.12 puts `fbMutOdoVecdims`
  at **0** and `fbMutOdoVecdimsAddIn` at **24**, and 9.14 puts `add-in` at **0**
  and `mut-odo-vecdims` at **24**. **The margin followed the offset and
  not the arm.** In both builds the copy sitting at 24 is the faster of the two
  --- `add-in` by 1.87% on 9.12, `mut-odo-vecdims` by 0.16% on 9.14 --- which
  is the outcome this entry registered as *placement* when it asked for two
  builds whose offsets swap. **What it is not is that experiment**: a compiler
  changes the whole binary and not one loop's address, so the swap arrives
  with everything else, and the two magnitudes differ twelvefold, which
  no single placement term explains. The code mechanism does not go away either
  --- one `imul` fewer per run is real and predicts a fixed sign ---
  so the honest reading is that a slot term of about this size sits on top
  of it and can outweigh it, which is why the sign is not stable.
  **AND THE CONTROL REFUSES TO LET THAT STAND AS PLACEMENT.** `build` against
  `mut-odo` --- the other pair one worker serves at two slots --- splits
  by compiler in the same way and by as much, 0.9751 at 19 of 24 on 9.12 against
  1.0006 at 13 of 24 on 9.14, **and its two copies sit at cache-line offset 0
  in BOTH compilers**, the `-g3` twins putting that group at `[0, 0]` on each
  and differing only in address order. So a change of compiler moved
  a sub-percent margin by two and a half points with no slot change at all,
  which is the thing a slot account of the add-in swap has to explain
  and cannot. What the twins establish is therefore weaker than it first reads:
  the offsets did swap and the sign did follow them, but a control with no swap
  moved as far, so the swap is **consistent with** placement rather
  than evidence for it. **What is established is that the lead is not a property
  of the arm; what is not established is what it is a property of,
  and the magnitude is missing either way.** So the clean two-shim probe
  this entry describes is worth less than it was, having been twice indicated
  now, and **the shipping decision is untouched**: a margin of one to two
  percent on one compiler and none on the other is not a reason to ship
  the sibling, and it is a reason to stop treating the lead as a property
  of the arm.

  **RUN 19 REPEATED THE SPLIT ON A THIRD COMPILER AND TOOK THE SLOT ACCOUNT
  AWAY.** The margin came back in the same shape --- **0.9755 at 19 of 24, sign
  p 0.0066** on 9.12, and **0.9991 at 14 of 24, p 0.54** on GHC HEAD, which
  is Run 18's 9.14 win count and p to two figures --- so *the lead
  is the compiler's* now rests on two independent second compilers and not one.
  **What went is the reading that made it the slot.** The instrument does
  not carry to HEAD: its `-g3` twin reads `[0, 31, 31, 21]` where the timed
  binary reads `[23, 0, 1, 2]`, at address deltas of `0x45A9`, `0x49DF`,
  `0xF65E` and `0xFC13` rather than the flat `0x40` that licensed Run 18's
  naming, and byte identity cannot stand in, the four copies being one 28 B
  sequence by construction. Under the ascending-address correspondence ---
  an assumption on the HEAD half, satisfied on the 9.12 one --- HEAD puts
  `mut-odo-vecdims` at **0** and `add-in` at **23**, which is 9.12's arrangement
  and not 9.14's. **A slot account therefore predicts 9.12's margin on HEAD,
  and there is none.** Either the correspondence fails there or the margin does
  not follow the slot; this pair cannot separate those, and the control says
  the same thing from the other side, `build` against `mut-odo` reading 0.9633
  on 9.12 and **0.9325** on HEAD --- both below 1, a three-point move between
  compilers, where on Run 18 that pair split 0.9751 against 1.0006. **So after
  three compilers the position is: the lead is the compiler's, the mechanism
  is unidentified, and the placement hypothesis has now failed its one real test
  rather than merely lacking support.** What would still settle it
  is the two-shim pair this entry has always described --- one compiler, one
  source, two placements --- which is now the only instrument left that could,
  the free-by-product route having been shown not to carry.

- `OPEN` **Gate 3's sign reversed three runs ago and no run has adjudicated it;
  Run 18 is the first to say so.** The gate fails when the in-situ forcing
  term's medians leave 1 *on the same side by more than a few percent*, which
  was written when Runs 8, 9 and 10 were reading every median BELOW 1. From Run
  16 they read above it: 1.0023/1.0001/1.0184 on Run 16, 1.0154/1.0383/1.0769
  and 1.0002/1.0215/1.0598 on Run 17's halves, and 1.0297/1.0354/1.0600 against
  1.0275/1.0344/1.0558 on Run 18's. **So Run 18 has all three arms on the same
  side of 1 in both halves, by 2.8% to 6.0%** --- the letter of the failure
  condition on the largest arm and not on the two smaller ones, which is why
  its chapter records the gate as *at its threshold* rather than passed
  or failed. What makes the reading ambiguous rather than simply a failure
  is that a read bias which REVERSES direction between runs is not the stable
  biased-read signature the condition was written to catch, and Run 9's own
  re-pricing put the effect on published geomeans under a point. **What would
  settle it** is the measurement the sum-only section already names and no run
  has taken since the reversal: the `-nosum` arms read against `sum-only`
  on a build where the two can be compared at fixed iteration counts rather
  than through criterion, which separates a biased read from two biased arms ---
  now with four `-nosum` arms rather than two, `mut-flat-gm-nosum`
  and `canon-full-nosum` having been added for exactly this. Until
  then the correction stands, and a run that finds all three medians past a few
  percent on one side should say so in its chapter rather than passing the gate
  silently, as Runs 16 and 17 did.
- `ANSWERED` **What Run 18 was built to answer, registered before it ran ---
  and what it answered.** Its pair was `run18-g912`, the basis, against
  `run18-g914`, settled 2026-08-21 and run 2026-08-23: GHC 9.14.1 against
  9.12.4, on one source carrying `-fobject-determinism`, the per-sample
  instrument and a saturating preamble. Five registrations. **Three held, one
  broke narrowly and one failed to the machine rather than to the pair.**
  The basis is Run 17's basis recipe over `saturate-preamble.patch` (applied
  after `wildlog-instrument.patch`, whose `lookupEnv` it uses); the other half
  is the same source and shim on 9.14.1 through `cabal.project.ghc914`, whose
  freeze resolves the same `vector`, `criterion` and `criterion-measurement`
  versions at the one index-state, so the halves differ in the compiler
  and its boot libraries and in nothing a freeze can see --- which prices
  the consumer's 9.14 build, library code recompiled included, and is to be read
  as such. The preamble is the state made an input: `SATURATE=<dose>` sprays
  dose x 1.15M short-lived pinned buffers of 2304 B before criterion sees
  the roster, collects, and prints one `@@saturate` line carrying
  a fixed-iteration reading of `vgg-14-c512-k3/list` and the heap peak;
  on for every recorded process and every probe read against a recorded cell,
  off for the clean alone legs, skipped by `check`, `diag` and `--list`.
  **Its non-vacuity and its dose are measured, on a quiet machine** (2026-08-22,
  `sat-probe`, the basis recipe's binary, loadavg under 1; a first evening's
  figures at loadavg 1.5 to 2.0 had read +31% and scattered, and were the load).
  `vgg-14-c512-k3/list` alone reads 16.6 to 16.8 ms clean; after
  the reproducer's pure pinned burst 18.2 to 18.7 at dose 1 and 18.0 to 18.3
  at dose 2, +9 to +11%; after the roster's own sprayer ---
  `cnn-slice-c32/list`'s fill for a fixed million iterations, each a 288-cell
  cons list and a 2304 B pinned result, both formation routes at once --- 19.1
  to 19.3 at dose 1 and 19.2 at dose 2, +14 to +15%; and with that sprayer run
  as a criterion bench ahead of the victim in one process, no preamble, 18.6
  to 19.0, where Run 16's roster cell read 18.45 against its alone leg's 16.38.
  So the plateau holds for both doses, dose zero is the clean level, and
  on that shape the roster's own sprayer reproduces the roster's state where
  the pure burst falls some three points short --- which is why `SATURATE_BY`
  defaults to `list` and keeps `spray` as the control. The 9.14 binary reads
  the same, 19.04 against 16.96. **Over five more shapes the picture
  is flatter** (`probe-decomp-dryrun.log`, the same binary and evening):
  the `list` dose lifts `list` by 12 to 16% and the `spray` dose by 10 to 14.5%,
  against Run 16's roster-over-alone-leg deflations of 9 to 13.5% on the same
  shapes, so both doses land in the roster's band within a few points,
  the `list` dose erring about two points high on average and the `spray` dose
  about half a point low, with the sign varying by shape ---
  `stretch-inner256`'s roster cell sits five points under both. The default
  stands, both routes being in it, and what changes is how registration 3 reads:
  the rest is a few points of either sign and not a constant. Registrations,
  each with what kills it: (1) *the bridge*, the 9.12 basis against
  `run17-wildlog` across the preamble's source change, every arm inside
  the drift band and the fills where Run 17 held them, killed by an arm outside
  it --- **but the placement-exposed arms are outside that condition
  and were put there 2026-08-22, on Run 17's own measurement**: this
  is a `.text`-changing comparison and by a long way, the two source changes
  between the halves adding **24576 bytes** to `run17-wildlog`'s 20381893 ---
  12288 for the preamble and 12288 again for the load fields, three pages each,
  measured at 20394181 and 20406469 --- where the instrument patch Run 17 priced
  added 4096, and 4096 was worth up to 8% on `gen-unsafe`, `gen-quotrem`,
  `build`, `mut-odo`, `offtab` and `bq-mut` with no strategy changed. Six times
  that shift is what the bridge is read across. So a movement on those six
  families is layout and kills nothing; the other arms are what the registration
  is over --- **less one more, `bq-expand-zf`, exempted 2026-08-22
  on a measurement taken because it could not be taken afterwards.** Two builds
  of the basis recipe either side of the load fields, differing in nothing else,
  put the tracked fills at `[0, 24, 0, 4]` and `[0, 0]` on both, every copy
  fitting --- so the fields do not move the fills, which is the question Run 18
  had to ask --- but the second carries **one straddling loop where the first
  carries none**, 38 bytes at offset 32, and a `-g3` twin names
  it `fbBQexpandZF`, which is `bq-expand-zf` and a timed arm rather
  than the instrument's own code. Run 17's basis straddled nowhere, so Run 18's
  basis carries a straddle its predecessor had not, on an arm [Run 10 priced
  a straddle at 12 to 14%](#what-moves-a-figure-when-no-strategy-changed).
  It is in BOTH halves, one source building them, so the compiler registration
  is untouched and only the bridge sees it. **Not chased, and the ruling
  is this README's own**: layout is not hand-tuned here, which is what the shim
  is for --- moving the new functions about the module until the straddle lands
  elsewhere is a lottery the next source change re-rolls, no claim rests
  on `bq-expand-zf`, whose series closed at Run 13, and raising the shim's skip
  budget would be a regime change that confounds the compiler. **And it
  is a weak answer to the pinning claim rather than the strong one [the rider
  asks for][open]**: all six tracked copies moved by 3200 bytes, a whole
  multiple of 64, so nothing forced the shim to re-pin anything. **And the fills
  half of it is already answered and answers nothing**: `sat-probe` read
  `[0, 24, 0, 4]` and `[0, 0]`, Run 17's exactly, so that clause is measured
  rather than predicted --- and Run 17's twelve arms moved while its own two
  halves' fills were identical, which is why a fill match is not evidence
  the arms held still; (2) *the compiler*, the registered orderings holding
  on 9.14.1, killed by a BROKE that clears that half's floor --- a margin moving
  is the finding and not a break, as claim 4's history says --- with claim 7's
  allocation levels read per compiler, a compiler being able to change
  allocation where a slot cannot. **Which orderings, read off `--claims`
  and not off this sentence, which was written before Run 17 ran and said
  thirteen**: Run 17 broke two of that thirteen --- claim 4's second half, now
  twice running, and claim 9's first --- and *restated* claim 4, so what Run 18
  inherits is an ordering where the manifest had a tie. Re-read the count
  and the content out of the manifest before the evening; (3)
  *the decomposition*, every shape's `list` alone leg twice on the basis, `SAT=`
  off and on through `run-alonelegs.sh`, against its roster cell: the state
  is saturated minus clean and the rest is roster minus saturated. The dry run
  over six shapes puts the rest between -1.4 and +5 points with no constant
  sign, so the registration is the distribution over the 24 shapes and
  not a cell: its median inside the floor, its tails named and read per shape,
  a median past the floor naming what the state is not, criterion's own
  interleaving between samples the first suspect. The `spray` dose's legs,
  a third column if the budget allows, price the burst route's share, some ten
  of the thirteen points on `vgg-14-c512-k3` and within two points of the `list`
  dose elsewhere. The alone legs themselves are sound: ten processes
  of `cifar-L2-16-c64-k3/list` land within 0.9%, so `list` is immune
  to the per-process placement term that unreads `offtab` and `build`; (4)
  *counted work*, `run-counts.sh` on both halves, instructions an iteration
  for every arm and shape from two fixed-`-n` processes a cell --- not
  for the orderings, which the pilot on Run 16 refused it (the TODO list's
  ruling), but per arm the count ratio 9.14/9.12 beside the time ratio: time
  moving with counts is codegen, time moving without counts is the runtime
  or memory, layout being pinned --- a compiler's codegen term and runtime term
  separated for the first time; (5) *the plateau*, every recorded process's
  `@@saturate` victim reading inside a band of the run's own, a process outside
  it read before its figures are. **What is built**: `saturate-preamble.patch`,
  with its two doses, proved to build and to fire on both compilers; `sat-probe`
  and `sat-probe-914`, its binaries for the between-run probes, deleted after
  their read-backs and rebuilt from `run18-pair.txt`'s recipes when wanted;
  `cabal.project.ghc914` and its freeze; `run-counts.sh`, proved on one cell
  (`vgg-14-c512-k3/list` 260.6M instructions an iteration, `mut-odo` 54.4M,
  `sum-only-early` 8.1M, `N` = 5); the `SAT=` mode of `run-alonelegs.sh`, which
  refuses a binary without the preamble. **Both patches landed in `Main.hs`
  by commit on 2026-08-22**, Run 17's pair being spent, so every recipe lost
  its apply step and each patch file stays as the record of what it was as one
  diff, refusing a second application in its own header. **The one pre-run risk
  is retired**: the shim reads back on 9.14's assembly --- `sat-probe-914`,
  the other half's recipe, has 113 self-loops in `Main`-compiled code, 61
  at offset 0 and none straddling, the 9.12 probe 110, 56 and none, the tracked
  28 B groups reading `[0, 24, 0, 0]` and `[0, 0]` against `[0, 24, 0, 4]`
  and `[0, 0]`; its `--list` and its `check` output are byte-identical
  to the 9.12 probe's, and the preamble fires there alike. One trap
  for the read-back: on 9.14 the baked RTS line is stored with a byte before it,
  so `strings | grep -x` misses it while `+RTS --info` reports it and the heap
  peak shows it in effect --- the notes and `run-alonelegs.sh` read
  it by `--info` now. **What was owed before the evening was taken 2026-08-22,
  before any build, and only the `-g3` twins per compiler are left, which belong
  at the write-up.** The stamp carries its load fields: the `@@wild` line gains
  `load=` (the 1-minute average from `/proc/loadavg`), `run=` (that line's
  instantaneous count of runnable tasks) and `cpu=` (the machine-wide busy
  jiffies from `/proc/stat`'s first line, in USER_HZ, which the kernel fixes
  at 100 whatever it ticks at), read in the same hooks outside the timed block;
  `./read-run.py --wild LOG` differences a bench's `pre` and `post` stamps
  and prints the CPU something else consumed during its samples, the `cpu` delta
  less the process's own mutator-plus-collector delta the line already carries.
  The reason is the wild cell: from inside a process its signature ---
  a non-reproducing mutator step at flat RTS totals --- is exactly an external
  intrusion's, and Run 16's updater cell was told apart only by a wall-clock
  window; these fields tell the two apart, foreign CPU during a bench's samples
  being the updater class and none the machine's own. The 1-minute average alone
  dates a multi-minute intruder and barely marks a ten-second one (it is damped
  over 60 s and updated every 5 s), which is why the other two ride with it.
  Stamped per sample with the rest of the line and *reported* per bench,
  /proc/stat's 10 ms jiffy saying nothing inside one short sample. The plateau
  is counted per process in `run-major.sh`, exactly as bench counts are,
  and banded across them in `read-all.sh`, at 5% --- loose against the 0.9% ten
  alone-leg processes span, tight against the 14% an unsaturated process reads
  below a saturated one --- with `check-scripts.py` cases behind all of it,
  controls among them; and `run-alonelegs.sh` and `run-counts.sh` have cases
  now, each written against a defect it turned out to have. **Not in Run 18**:
  a roster change, which would confound the compiler. The 24m/48m probe, which
  could have reopened the area, was taken ahead of Run 17 and killed.
  And the `add-in` placement question, deferred by [its own entry][open]
  to a run that has the compilers measured.

  **THE VERDICTS, 2026-08-23.** (1) *The bridge*: **BROKEN, and narrowly.** Read
  as it has to be on this run --- per shape as a ratio to `list`, because
  the box moved 4.8% between the two runs and `--compare` across runs reads
  absolutes, so its own output puts `list` at +5.52% and every arm with it ---
  the 26 arms the registration covers give a geomean of 0.9867 with **two
  outside the 3.3% drift band**: `bq-gen` at 0.9545 and `bq-mut-runs-gm-mulback`
  at 0.9639. The kill condition was an arm outside the band, and two are.
  `mut-odo-vecdims` reads 1.0062, `mut-flat-gm` 1.0022, `bq-scan-rem-gm-mulback`
  0.9825 and `bq-expand` 0.9803, so the arms the claims rest on are inside
  it and the break is at the edges of the roster. The exempted placement-exposed
  families run 0.9333 to 1.0216, which is why they are exempted. (2)
  *The compiler*: **HELD, and it is the run's headline.** All thirteen
  registered orderings hold on 9.14.1 and all thirteen on 9.12.4, no BROKE
  on either half, and claim 7's allocation reads per compiler at 1072 of 1080
  cells agreeing to 1e-4. (3) *The decomposition*: **HELD.** The total
  in-process deflation is +12.76% on the basis and +12.53% on the control,
  and the preamble splits it: the **state** is +11.43% and the **rest**
  the roster adds on top is **+1.20%**, whose median sits inside this run's
  1.36% floor, which is what the registration asked. Twenty of the 24 shapes put
  the rest above 1 and the tails are named --- 0.9905 on `stretch-bigstride`
  and **1.1004** on `stretch-tall-Mx2`, the one shape where the roster adds ten
  points beyond the saturated state. So the preamble reproduces the roster's
  state to within the floor and the dose is right. (4) *Counted work*:
  **DELIVERED, and it separates the two terms for the first time.** Instructions
  an iteration on both halves, over 42 arms, split the roster cleanly in two.
  The `bq-expand` family moves in counts and time **together** --- counts 0.9889
  and time 0.9884 on `bq-expand` itself, with its twins, `-b`, `-qr-prim`, `-zf`
  and `-gm-mulback` all at counts 0.988 to 0.991 ---
  and `mut-odo-vecdims-add-both-down` likewise at counts 1.0278 against time
  1.0361. That is codegen, and it is the whole of the codegen this pair found.
  The arms with the **largest** time differences move at count ratios
  of **1.0000**: `bq-gen` +9.26% in time, `offtab` -5.76%, `gen-unsafe` -6.29%
  and `gen-quotrem` -3.14%, every one of them emitting the same number
  of instructions on both compilers to four decimal places. Time without counts
  is the runtime or memory rather than the code, and the correlation of the log
  ratios over all 42 arms is 0.213, weak as the Run 16 pilot found.
  **So the placement-exposed family's seven percent is not 9.14 emitting
  different code for it**, which is the sharpest thing this instrument has said
  and is a second, independent line on the same conclusion the `-g3` twins
  reach. (5) *The plateau*: **FAILED, and the failure is the machine rather
  than the pair.** The eighteen processes read the preamble's victim
  from 20.0411 to 21.7604 ms an iteration, an 8.58% spread against the 5% band
  `read-all.sh` gates at. The nine that ran before 10:52 span 20.04 to 20.38 ---
  **1.7%**, well inside the band --- and every reading above 21 belongs
  to a process that started after it, `g912-reshape1` at 21.76 and `g914-slice`
  at 21.73 leading them. So the gate is reading the intrusion it was built
  to notice, the band is the right band, and what a future run should
  not conclude from this is that the preamble is unstable.

- `ANSWERED` **Which of the `bq-expand`-centric claims retire, now that the fix
  decided is `mut-odo-vecdims`.** **Settled 2026-08-24**: claims 3, 4, 5 and 9
  retire, claim 1 gains `bq-scan-rem-gm-mulback` and the tie at its foot,
  and claim 2 changes its question to where `offtab` and `bq-expand` sit ---
  thirteen registered orderings becoming eight. Each retirement's reason,
  and the readings the two new links were measured at on both of Run 18's
  halves, are in the settlement paragraph at the foot of [the
  claims](runs/run19.md#the-claims-the-next-run-should-test), which owns
  the account; the `CLAIMS` manifest in `read-run.py` took it at Run 19's
  write-up on 2026-08-25, the retiring orderings having had one last
  cross-compiler reading first, in which all four held on both halves.
  **The second half of the ask was already spent**, the eight *What the class
  says* paragraphs having been written to the re-aimed properties at Run 18's
  write-up with only the sentence asking for it surviving. The decision
  was whoever asks for a run's, which is why it sat unmade through three runs;
  what kept it live was that it had no entry here until 2026-08-24, the index
  above saying nothing open is recorded anywhere else and the ask being a bolded
  TODO outside this list.

- `ANSWERED` **What Run 19 was built to answer, registered before it ran ---
  and what it answered.** **Four registrations held, one held while its own
  claim moved underneath it, and the sixth came back a negative that
  is this run's sharpest result.** Its pair is `run19-g912`, the basis, against
  `run19-ghead`, settled and built 2026-08-24: GHC HEAD 10.1.20260803,
  the in-tree stage1 of the checkout under `~/r/horde-ad/ghc`, against
  ghc-9.12.4, on one source, one shim, one roster and one regime, both halves
  under `WILDLOG=1 SATURATE=1`. It is Run 18's pair with HEAD in 9.14's place,
  asked for as that, and the basis recipe is Run 18's basis recipe with nothing
  changed at all: `Main.hs` at `e9fab1e` and `align-as.py` at `40f7a37` have
  not moved since that pair was built, and the rebuild reproduces `run18-g912`
  byte for byte --- md5 `9768189b5c6947beca4ba89cad5800c8`, `.text` 20406469 B,
  the same tracked fills and the same one 38 B straddler --- so the md5's
  one-sided instrument answers, and every input is proved unmoved
  with the dependency store among them. HEAD wants a project file of its own,
  `cabal.project.ghead`, `cabal.project.freeze` pinning `base ==4.21.2.0`
  and so refusing this compiler outright: it takes `base installed`
  and `allow-newer` for the boot packages, pins `criterion ==1.6.5.0`
  and `vector ==0.13.2.0` with `+boundschecks -unsafechecks` by hand, and names
  `hashable ==1.5.0.0` outright, 1.5.1.0's cabal file not declaring
  the `ghc-bignum` its source imports. `cabal.project.ghead.freeze` beside
  it pins the rest at the index-state the other two plans hold, so the three
  differ in the boot libraries and in nothing else a freeze can see. **The one
  pre-run risk is retired before the pair exists**: the shim was written against
  9.12's NCG output, and on HEAD's it reads back 109 self-loops
  in `Main`-compiled code, 51 at offset 0 and none straddling, against
  the basis's 113, 56 and one; the halves' `check` output is byte-identical
  on every shape it walks, their `--list` identical at 1128, and `diag` reads
  SpecConstr on both. **And HEAD groups the tracked loops differently before
  anything is timed**: its 28 B census is a four-copy group at `[23, 0, 1, 2]`,
  a three-copy group at `[0, 0, 13]` and a two-copy group at `[0, 0]`, where
  the basis holds `[0, 24, 0, 4]` and `[0, 0]` --- the three-copy group being
  `bq-mut-runs-gm-mulback`, `bq-mut-lemire-mulback` and `bq-mut-runs-mulback`
  compiled to one seven-instruction body that 9.12 does not share between them.
  Six registrations, each with what kills it: (1) *the repetition*, `run19-g912`
  against `run18-g912` --- one binary, two runs a day apart on one box,
  so `--compare` reads absolutes fairly and every arm belongs inside the drift
  band, killed by an arm outside it; what it prices is the box and the harness
  rather than any code; (2) *the compiler*, the registered orderings holding
  on HEAD, killed by a BROKE that clears that half's floor, with claim 7's
  allocation read per compiler, a compiler being able to change allocation where
  a slot cannot --- the count and the content off `--claims` and not off
  this sentence, which was written when thirteen of thirteen read HELD on Run
  18's basis; (3) *the decomposition*, every shape's `list` alone leg twice
  on each half, `SAT=` off and on through `run-alonelegs.sh`, against its roster
  cell: the state is saturated minus clean, the rest is roster minus saturated,
  and the registration is the distribution over the 24 shapes with its median
  inside the floor, where Run 18 read +11.43% and +1.20%; (4) *counted work*,
  `run-counts.sh` on both halves --- over the MAIN SET, which is all the script
  could then sweep --- the count ratio HEAD over 9.12 beside the time ratio per
  arm; time moving with counts is codegen and time moving without them
  is the runtime or the memory, which is how Run 18 put the placement-exposed
  family's seven percent on count ratios of 1.0000; taken 2026-08-24 ahead
  of the evening, counts wanting no quiet machine; (5) *the plateau*, every
  recorded process's `@@saturate` victim inside a band of the run's own, banded
  at 5% across them by `read-all.sh`; (6) *the offset swap*, whose instrument's
  limit is now measured rather than assumed. Run 18 read the swap off a `-g3`
  twin per compiler, each twin reproducing its timed binary's tracked offsets
  with its addresses a flat `0x40` below. Both twins were built here before
  the run: the 9.12 one repeats that exactly, being the same binary,
  and **the HEAD twin does not locate anything**. It reads `[0, 31, 31, 21]`
  where the timed `run19-ghead` reads `[23, 0, 1, 2]`, at address deltas
  of `0x45A9`, `0x49DF`, `0xF65E` and `0xFC13` rather than one constant. Byte
  identity cannot stand in, the four copies being one 28 B sequence
  by construction, and no weaker `-g` level is a way round, `-g1` changing
  the emitted code exactly as `-g3` does. So a twin names HEAD's four functions
  and does not say which copy is which, except under the ascending-address
  correspondence, which the 9.12 half satisfies and nothing on the HEAD half
  checks. What the registration may report is the timed offsets, measured
  on both halves, and the margin; an attribution of a HEAD margin to a slot
  is an assumption and is to be written as one. The question stands --- Run 18
  put `mut-odo-vecdims` and `-add-in` at 0 and 24 on 9.12 and at 24 and 0
  on 9.14, the margin following the offset both times, while the control pair
  sat at 0 on both and split by compiler as far --- and it is the reading
  that is weaker here, not the question. **Not in Run 19**: a roster change,
  which would confound the compiler; the floor question, whose preamble half
  wants one binary over the roster twice rather than a pair; and the `add-in`
  placement probe, which [its own entry][open] defers to a run that has
  the compilers measured. **THE VERDICTS, 2026-08-25.** (1) *The repetition*:
  **HELD**, and it did more than pass. Every one of the 42 arms landed between
  0.9836 and 1.0133 with `list` at 0.9918 and the machine check at -0.84%,
  so the box and the harness reproduce to under a percent --- but the same
  binary's FLOOR went 1.36% to 2.32%, which answers the standing floor question
  in this list by killing both of its candidates at once. (2) *The compiler*:
  **HELD**, all thirteen orderings on both halves, no BROKE, which is what let
  the four retiring claims retire on a reading rather than on a decision.
  **Its allocation half did not**: 1016 of 1080 cells agree across the halves
  where the 9.14 pair had 1072, so HEAD reallocates within the tiers while every
  tier returns --- the registration named exactly this as the thing a compiler
  can do that a slot cannot, and it is the first time claim 7 has caught
  anything. (3) *The decomposition*: **HELD** on both halves, the state
  at +11.73% and +12.57% against Run 18's +11.43%, the rest at +0.31%
  and +0.72%, both geomeans inside their floors. (4) *Counted work*:
  **DELIVERED, and it is now the reader's.** The reading was hand-rolled for two
  runs, so `--counts` was built here with three cases behind it, and it splits
  the pair cleanly: the fast pure tier's six-to-seven-percent loss is
  on its instruction counts, and `gen-unsafe`, `mut-odo`, `offtab` and `bq-gen`
  move at count ratios of 1.0000 to 1.0019. `bq-gen` is the finding ---
  the largest movement to HEAD's credit, +7.5%, at the same instructions;
  the largest against it, `bq-odo-gm-mulback` at 0.9270, is the one the counts
  explain. **And the registration was narrower than it read**: the sweep covered
  the main set alone, which no sentence in this file said, so eight of the nine
  populations had no counted work at all. Extended and swept the same day,
  sixteen further files: seven classes agree with the main set and `reshape1`'s
  geomean inverts, by 0.3% and with 78 of its 139 cells still HEAD-heavier,
  on a unit-innermost rule the chapter states. (5) *The plateau*: **HELD**,
  eighteen processes at 19.6244 to 20.2847 ms/iter, a 3.37% spread inside the 5%
  band. (6) *The offset swap*: **SPLIT --- the margin half DELIVERED
  and the instrument half KILLED.** The margin repeated a third time --- 0.9755
  at 19 of 24 and p 0.0066 on 9.12, 0.9991 at 14 of 24 and p 0.54 on HEAD,
  the same win count and p as Run 18's 9.14 half --- but under the address-order
  assumption HEAD arranges the two arms as 9.12 does, where 9.14 had them
  swapped, so the slot account predicts a margin that is absent. Either
  the correspondence fails on HEAD or the margin does not follow the slot,
  and this pair separates neither; the control moved three points between
  compilers in the direction the add-in pair did not. What is measured stands:
  both halves' timed offsets, and both margins.


### Recommended tasks after Run 19

**What Run 19 made cheaper for the next run, which is not a figure and no other
step gathers.** **One reader gap closed, and it is the one this list named two
runs running.** `--counts THIS.txt OTHER.txt`, taken with `--compare`, prints
each arm's instruction-count ratio beside its time ratio and the residue between
them, which is registration 4's whole reading and had been hand-rolled
at the write-up for two runs. Two cases went in first, and both were watched
to FAIL against the tree that lacked the mode --- a new flag has no earlier
revision for `--audit` to replay it against, so the failure was taken
in the working tree, which is the same proof at the only moment
it was available. They guard what the mode can silently get wrong: a `!!` cell
perf refused, which must be dropped and named rather than read as a count
of zero that destroys an arm's geomean, and an arm the counts hold that the run
does not time, which must be named and skipped rather than folded in. **A second
mode came out of the verification rather than the run**, and its defect
is a reader's: `--movers PCT` lists the arms whose geomean moved past
a threshold, counted and grouped by the same comparison that lists them. Run
19's independent checker reported twelve arms past 3% where eleven move ---
the eleventh sits at 3.99% and the twelfth at 2.51%, so no convention explains
it; what does is that the count had to be taken by eye off `--chapter`, whose
per-arm block lists arms outside ONE percent. Both the checker and this session
hand-rolled it in `awk`. The mode prints its threshold with its count
so a figure taken off it carries the threshold it was measured at, and it groups
by stripping the A/A suffix, three copies of one strategy moving together being
one finding rather than three. **What stays open is the bridge**, unchanged
from Run 18's entry: `--compare` across two runs reads absolutes, and no mode
reads them per shape as a ratio to `list`. This run did not need it, its box
not having moved --- which is exactly why it will be missing again the next time
one does. **And a second gap was found and left**: the alone legs' cross-half
level, Run 18's 1.0031, has no mode either, `--deflation` reading each half
against its own roster and nothing reading the halves against each other.
That line is absent from the run's file rather than hand-rolled into it.
**The load fields paid again, and this time on an intrusion small enough
that nothing else could have found it**: one bench of 1128 at 0.35 foreign CPU,
in a run whose other seventeen processes are clean. The A/A twins then priced
it without a rerun --- the exposed copy 2.0 to 2.2% above two twins agreeing
to 0.19% --- which is a use of the eighteen A/A pairs this README had not made
before: **they are not only a floor, they localise a contaminated cell to an arm
and a shape and bound what it moved.** Reach for them whenever `--wild` names
a bench, before deciding what a rerun would buy. **One capability RETIRED,
and it is the sharper half of this entry.** Run 18 recorded that a compiler pair
swaps loop offsets for free, so a placement experiment need never be built
again. Run 19 tried to spend that and could not: the `-g3` twin does not carry
to GHC HEAD, its four addresses sitting at four different deltas from the timed
binary's where 9.12 and 9.14 both gave a flat `0x40`, and byte identity cannot
stand in, the four copies being one 28 B sequence by construction. **So the free
route works on some compilers and not on others, and nothing announces which**
--- a twin looks exactly as usable either way until its deltas are checked.
Check them before believing a naming, and treat the purpose-built two-shim pair
as the only instrument that always works. **One trap met and worth writing
down**, from before the run-file split left one rename where there were four:
a literal rename of the four run-numbered headings missed a link text whose case
differed from the heading's --- `the recommended tasks after Run 18` against
`Recommended tasks after Run 18` --- so the anchor moved and the text did not,
which is Run 18's own trap arriving through a different door. `--check-doc`
reads anchors and not texts, so grep the old run number back afterwards rather
than trusting a replace count.

**Both of Run 17's items are spent, and this heading no longer carries them.**
Its first --- which shapes poison --- was answered 2026-08-18 and its account
is [the position-term entry][open] and `small-pinned-churn-investigation`.
Its second was Run 18's pair itself, whose last owed piece, the `-g3` twins per
compiler, was taken at Run 18's write-up and is recorded in `run18-pair.txt`
and in [the add-in entry][open]. Nothing spent stays under a heading naming
a run that is over.

**The replace list's second sweep has a blind spot, and Run 19 measured both
it and the obvious fix.** The preamble prescribes *grep them for the name
of the run being superseded*; that grep cannot see a paragraph naming only runs
OLDER than the superseded one, and this run met six such sites, four of them
named here --- three closing Results, naming Runs 10 and 13 to 17 and never Run
18 while every figure in them was Run 18's (one contradicting this run's
headline allocation finding in three other places), and a `1.84x` in the ceiling
ruling carried forward from **Run 11** through eight write-ups. An independent
checker found those four by hand; every mechanical gate here passed over them.
**The obvious repair was built and then refuted, which is why this is a note
and not a mode.** A `--check-doc` sweep flagging paragraphs whose newest named
run is behind the run in hand while carrying a figure returns **165** entries;
excluding the run file and prose saying *this run* leaves 104; scoping it
to the sections the replace list names leaves **100** --- for four that matter.
The reason is structural rather than a tuning failure: naming an old run beside
a figure is the NORMAL state of this document, which is full of answered entries
and dated mechanism accounts, and *reads as current* is the discriminating
property, which no cheap predicate has. A checker at that ratio is one nobody
reads, which this file already knows about hint lists. **What is left
for the next run is the honest form of the same instruction**: after
the run-name grep, walk the replace-listed sections and ask of each
figure-bearing paragraph *which run measured this*, which is a reading and
not a grep --- and the sites above are what it costs to skip it.

**A whole axis of the counted-work evidence was missing and no document said
so.** `run-counts.sh` was born at Run 18 to serve registration 4, whose question
--- separate codegen from placement in the arm-by-arm cross-half table ---
is the main set's, so the script took its shapes from `--list`, which
is the main roster, and covered the main set and nothing else. **The limit
was recorded in exactly one place: a comment in the script's own header.**
This file names the instrument **22 times and not one of those mentions
is within 250 characters of the words *main set***; the registration reads
*on both halves ... per arm*, which is population-blind and therefore reads
as covering the run. So a session writing up a run would have had to open
the driver to find that its class populations had no counted work at all,
and nobody did until the question was asked from outside. **It was never
a question of cost**: the eight classes hold 1128 cells, exactly the main set's
number, and sweep FASTER --- about seven minutes a half against twelve ---
because the cost is elements touched and not cells. The script now takes
an optional class, names its artifact for it and refuses a class matching
no bench, and step 20 of the run list sweeps every population. **The general
shape, and this file already has the rule in mirror image**: *write a capability
as a capability*, because a fact recorded as a tool's limitation goes inert.
Here the limitation was recorded accurately and went inert anyway, because
it was recorded where the tool lives and not where the run is planned. A scope
limit belongs in the sentence that asks for the measurement.

1. `ANSWERED` **What tightened the floor on Run 18 --- answered by Run 19,
   and the answer is that nothing did.** Run 18's halves came in at 1.36%
   and 1.42% against Run 17's 3.70% and 3.89%, and it could not attribute
   the move: two candidates were left, the box's BIOS idle settings
   and the saturating preamble, and its own pair separated neither. **Run 19
   separated them by holding everything still.** Its basis half is Run 18's
   basis BINARY, byte for byte --- same md5, same `.text`, same fills ---
   on the same box, the same roster, the same layout, the same regime
   and the same preamble, and it read **2.32%** where that binary read 1.36%,
   a factor of 1.7 with every named candidate fixed. So neither candidate
   is the mechanism, and the quantity is not one an evening's conditions set:
   **the floor is re-drawn per run, and a run inherits nothing
   of its predecessor's.** Where it lives is narrowed too --- the restricted six
   barely moved across the same two runs, 0.54% to 0.49%, so the variation
   is in the twelve pairs outside them, which are the widest-spread arms
   the twins were added to expose. What is left open, and it is a smaller
   question: whether the twelve's spread is criterion's sampling alone
   or something per-process on top of it, which one binary over the roster
   several times would answer and which no pair is needed for.
2. `ANSWERED` **The bridge wanted a reader mode and has one ---
   `--compare OTHER --bridge`, taken 2026-08-23, the same day this asked
   for it.** Every run until this one could read its bridge with `--compare`,
   because the box held still and an absolute comparison was a fair one. Run 18
   could not, and the figure its registration was written on had to be computed
   by hand: per shape, each arm's ratio to `list` in this run over the same
   in the last, which cancels a box term exactly and a `--compare` cannot.
   That is the computation a write-up must not improvise, so it was a defect
   report against the reader, and the mode answers it in those words: it reads
   each arm as a ratio to `list` in its own run, per shape, over the shapes
   the two runs share, and its own header says that is what cancels a box term
   where `--compare` does not.

**One rider rather than a task of its own, since it fires on an event and
not on a session.** The pinning claim --- that a shim'd build holds every
tracked loop at one address across a roster change --- is measured only
in its weak form: adding `mut-flat-gm-nosum` left every tracked loop where
it was, but a `Force` arm reuses a rostered function and emits no code
of its own, so emission order had nothing to move. **The next roster addition
that brings a new function is the stronger test, and is to be taken as one** ---
read the fills on one build either side of it, before anything else changes ---
which costs nothing at the moment the arm lands and cannot be taken afterwards.
Until then the claim covers additions that cost nothing to place, and should
be quoted that way.

**And one class not to repropose: work that needs an aligned build.**
`mut-odo`'s wide interval is the live case. The dispersion is documented
as belonging to `micro-aligned` --- 1.06, 1.09 and 1.15 there against 0.72
and 0.19 on `micro-maxskip`, and 0.82 against 0.31 on Run 11 --- and the swap
that would separate a dispersion belonging to the *worker* from one belonging
to the *slot* is enabled by an aligned build making it a membership-free edit.
No run since Run 11 has had one: the basis has been max-skip since Run 12, which
priced `-fproc-alignment=64` and saw the flag lose; the script that built
unaligned/aligned pairs was deleted on 2026-08-14; and Run 13 showed a two-shim
pair can hold every tracked loop at one offset in **both** halves, which
is the property alignment was wanted for. So the swap asks for a build form
this README has moved past. **Amended 2026-08-23**: Run 18 got the swap
for nothing, a change of compiler having reordered the vecdims group so that two
of its arms exchanged cache-line offsets, which is what the aligned build
was wanted to arrange deliberately. So the class stays not-to-repropose,
and the reason is now that the experiment arrives free whenever a pair changes
codegen rather than that it cannot be built.


### Non-urgent TODO list

- `STANDING` **A class process's provenance line counts every class view,
  not the population that ran.** The count is fixed before criterion does
  the selecting, so each class process reports the whole class set's size beside
  its own elapsed time and heap peaks, both of which are its own. The README
  takes the population from the reader instead, and that costs nothing at all
  now: `--block` emits the clause and `install-tables.sh` installs the paragraph
  it sits in. The fix in `Main.hs` stays refused --- `provenance` would have
  to parse a criterion argument it passes through untouched, a second source
  of truth for criterion's matching rules, wrong the moment a run reaches
  for `-m glob` --- and refusing it is what states the rule the installers go
  by: **install from the tool that already knows the value, never from one
  that would have to re-derive another's logic.**
- `ANSWERED` **Runs never overlap in the benchmarked set.** `mkStrided`'s index
  map is a bijection onto `[0, l)`, where im2col patches --- the workload
  this README opens by naming --- overlap heavily and so reuse cache. The window
  class (`mkWindow`) builds exactly those overlapping patch views, and both
  recorded runs agree: the overlap *lifts* every ratio rather than lowering it,
  so the main set's pessimism about this case was about absolute cost, never
  about the fallback's standing against `list`. The window block in [The stride
  classes, run by run](runs/run19.md#the-stride-classes-run-by-run) carries
  the figures.
- `ANSWERED` **The roster order biases the table, and nothing corrects for it.**
  The warm-up drift above means a strategy's figure depends on its slot, `list`
  being in the coldest one. The fixes are all real changes rather than write-ups
  --- a warm-up bench before `list`, interleaving or randomising the order,
  or correcting each row by its slot --- and each breaks comparability
  with every run so far, which is why none was taken for eight runs. Run 7
  confirmed the drift, Run 8 mostly did not, and Run 9 shows why both readings
  were of the wrong quantity ([the floor section][floor]): the effect is
  not a per-slot gradient to fit but a step, worth nothing on most arms
  and 35--40% on one family at one shape. **So a slot correction is now refuted
  rather than merely unmeasured** --- a linear fit in slot number cannot express
  a step that depends on the arm, and fitting one would smear a real 40% across
  thirty rows that do not have it. What the drift needed instead was the warm-up
  bench, the only one of the three fixes Run 9 left standing, and **Run 10 takes
  it**: `sum-only-early` above `list`, so the baseline is measured on a grown
  pool like everything else, at the cost of re-basing every published ratio ---
  which is what the entry above says none of these fixes could avoid. What
  it does not address is the placement gap the `build`/`mut-odo` pair shows,
  a separate and larger target that no reordering reaches.
- `OPEN` **No build-vs-output time decomposition**, which Run 8 wanted and did
  without. `diag` measures per-builder *allocation* only, so a claim like
  "the table build is a third of the cost" --- the natural reading
  of `bq-mut-runs` beating `bq-mut` by 39% --- cannot be checked here. Claim 4
  no longer needs it --- a Core diff identified what the flag deletes
  from the scan builder and the ~4% it is worth accounts for where the pair
  lands, the two arms sharing their output code exactly --- but the residue
  does: how much of each arm's own ~25% absolute gain is build and how much
  output is still unmeasured, and the same question stands for every other arm
  in the table. It needs a timing mode alongside `diag`'s allocation one, using
  the fixed-iteration differencing the horde-ad performance model prescribes
  (`-n 200` minus `-n 100`, fresh processes) rather than criterion, since
  the builders are not benchmarks.
- `PARKED` **Change the method and a family of prose is deleted rather
  than maintained --- the lever the two speculative regimes here share,
  and the one no tooling reaches. Both routes to it were piloted on 2026-08-22
  and both are refused, which is what parks the entry rather than answering
  it**: the lever is still worth having and this README knows no way to reach
  it. The controls, the pairing, the shim and the floor exist because wall-clock
  on this machine is layout- and history-dependent, and the write-up pays
  for that defence every run: the floor, the drift band, the pinning caveats,
  the restatement on the basis half, the basis matching owed before any figure
  is quoted. Numbers needing no such defence delete those paragraphs;
  an installer only makes one cheaper to write. Both candidates were written
  2026-08-14 from a review of the apparatus rather than from any run, and each
  names the pilot that would settle it. **Counted work instead of sampled time,
  wherever the question is an ordering.** Counted work is layout-independent ---
  the wild-cell probe read an A/A pair's instructions agreeing to 5e-5 ---
  so a cachegrind or fixed-`-n` counter table would want no quiet machine
  and no floor and would reproduce on any box, the clock staying
  for the boundaries where a memory-system effect can invert an ordering. Pilot:
  counts for every timed arm over the shape set, read against a published time
  column --- orderings that agree license the switch, and the cells
  that disagree are the memory-bound residue the clock is still for. **Taken
  2026-08-22 on `run16-a32m` against Run 16's column, and the switch
  is REFUSED**: over the 44 timed arms the count ordering agrees with the time
  ordering at Spearman 0.725, 201 of 946 pairs inverting, and the disagreement
  is not a residue but the fast tier --- `mut-flat-gm-nosum` executes 1.9 times
  `list`'s instructions per unit time and `bq-gen` 0.83, so what an instruction
  costs spans more than twofold across arms, and where arms differ in
  it the clock decides. What the pilot confirmed is the other half of the claim:
  counts are layout-free, every A/A pair agreeing to three digits across
  the table. So counts ride as the check of what a time change is made of, never
  as the ordering instrument; `run-counts.sh` is the driver, and Run 18's
  `run18-counts-g912.txt` and `run18-counts-g914.txt` are the artifacts it left
  --- the Run 16 pilot's went with that run's artifacts on 2026-08-23.
  **Randomised slots in per-trial processes instead of pinned ones.** Many short
  fixed-`-n` trials per cell, each in its own process with the order drawn
  fresh, so that position becomes noise that averages rather than bias
  that persists, and a table stops needing comparability carried between runs,
  being self-contained evidence. Not the reordering the roster-order entry above
  rejected --- that varied slots inside the one shared process --- but a regime
  that gives the shared process up. Pilot: a few arms and shapes read against
  the published column, with the A/A pairs' spread under randomisation
  as the method's own floor. Its precondition was the per-process floor
  registered with Run 17's pair, read 2026-08-22: `offtab` and `build` spread 12
  to 14% across ten single processes of one binary on a quiet machine, a mutator
  term that clock, TLB, last-level misses, ASLR and huge pages were each
  measured not to be, leaving physical page placement --- a term no in-process
  control sees and one this regime would draw afresh per trial, so the pilot
  is refused.
- `OPEN` **Render the run-scoped prose from a ledger --- speculative likewise.**
  The end state is verdicts, statuses, floors and tallies kept in one small
  machine-readable file beside the roster, `read-run.py` rendering them
  into the run's file as `--in-place` renders the tables, so that everything
  rendered cannot go stale and the checker fleet stops growing a check per
  defect class. The mechanism is not in doubt; the cost is a rewrite
  of the write-up procedure. **Its pilot was the claims verdicts and
  it is taken** (2026-08-16), which leaves the question the pilot cannot answer:
  whether one ledger file beats an installer per section. Do not design
  it before the installers say what it would hold --- three of them now do,
  and the fourth thing a run still writes by hand, the cross-class summary's
  emphasis, is exactly what a ledger would have to carry and no reader can
  derive.

- `OPEN` **The repoint, done rather than checked.** Post-run step 5 used to bump
  four run-numbered headings and repoint every link's text and anchor to them,
  `Main.hs`'s `README.md#` references included; the run-file split left it one
  heading --- *Recommended tasks after Run N* --- and one path rename, README's
  links from the last run's file onto this one. `--check-doc` fails any
  the rename missed, `runs/` keeping every run so a stale link resolves
  and renders rather than dying. A mode that performed the rename would leave
  nothing to catch; it writes the README, so it wants `--in-place`'s refusals,
  which is why it is registered rather than written.
- `OPEN` **More checks of the floor-consistency shape: one figure, several
  sites, must agree.** The floor pair, the roster size and every population size
  quoted as `over N shapes` are checked (the last two against Main.hs,
  2026-08-16, since agreement alone cannot see a count that is stale
  everywhere), and since 2026-08-22 the floor-movement sentence beside the class
  table --- alone among them in having a truth on the page rather than only
  agreement, its second figure being a claim about the column printed right
  above it. **It fired on the document it was written into**: Run 17 installed
  that column and left Run 16's paragraph standing under it, all eight movements
  landing on the previous run's figures with `--lint`, `--check-doc` and both
  installers green over them. The paragraph was cut rather than repaired, what
  moved the floors having no account --- the entry for that is in [What
  is open](#what-is-open). What is left of the four subjects Run 14 got wrong
  is the run window and the process count, neither of which has a phrasing crisp
  enough to match yet: the pattern has to distinguish a population's size
  from a win count, which is what `on N shapes` taught.
- `ANSWERED` **`run-counts.sh` priced a half at forty minutes where it is twelve
  --- TAKEN 2026-08-23, by cutting the duration rather than correcting it.**
  Measured that day on the g914 half at `N=50` over the full roster, off
  the stamps the sweep writes into its artifact's own header and footer ---
  which is what a session should read, so the numeral was the wrong thing
  to keep: the sentence it sat in claims that a blocked perf costs *the same
  time a real sweep takes*, and the figure was incidental to that. Cut at all
  four prose sites, twice in the script and twice in `check-scripts.py` ---
  a comment and `counts-refuses-an-unwritable-tmp`'s description --- none
  of them a matcher, so no case moved. The gate's own forty minutes elsewhere
  in this README is a different duration and is right.
- `ANSWERED` **Does `offtab-scan-rem` belong in the fingerprint? It does,
  and membership stopped dropping arms at all --- taken 2026-08-24.**
  `--fingerprint --classes` had been printing, as hand-work every run,
  that it *is best outside the family on one shape and is not a fingerprint arm*
  --- a membership question the install can raise and cannot settle, since what
  the fingerprint is for is keeping the previous run's absolutes readable
  and which arms earn that is a judgement. Registered 2026-08-23 because
  an unregistered notice printed every run is one nobody reads. Both steps
  it asked for were taken: the shape is `reshape1-rank10`, where the arm reads
  0.090 against `bq-scan-rem-gm-mulback`'s 0.091, and the notice names
  its shapes now instead of counting them. That thousandth is why the rule above
  drops nobody. It passes the one-per-family clause by crossing
  `bq-scan-rem-gm-mulback` rather than tracking it --- ahead by a thousandth
  here, 0.171 against 0.131 on `stretch-rank12` --- so the two are not one
  strategy spelled twice.
- `ANSWERED` **`--claims --compare PREV.json`, if the movement sentence turns
  out to be the last transcription.** The kept JSONs make *held, and moved
  from 0.9909 to 0.9940* mechanical --- `pair_stats` over both files ---
  and it is the one thing a claim's paragraph still copies by hand. Not taken,
  because it renders the reading rather than the arithmetic, and the division
  the installed readings keep is that the author owns whether a movement means
  anything.
- `ANSWERED` **Check that the basis half named in prose is the run's own ---
  taken 2026-08-19.** `--check-doc` holds every `run<N>-<half>` token
  in the Results section to the run its file is named for, which is where Run
  14's write-up left `run13-maxskip` standing while installing `run14-lookrts`'s
  tables under it, with `--lint`, `--check-doc`, `--selftest` and `--aa` all
  green because no check read that name. **The scope is that section and
  not the whole file**, which is the ruling worth keeping: the forward-looking
  sections name the previous run's halves on purpose --- Run 16's basis
  registration is a repetition against `run15-a32m` --- so a file-wide rule
  would fail the document for saying what it means. Non-vacuity sits beside
  the check and again as a control in `check-scripts.py`, which builds the Run
  14 defect out of the current run file rather than spelling it out, so it keeps
  working when the run number moves.
- `ANSWERED` **Check each class lead's shape list against its run --- taken
  2026-08-22.** The five class views that gained a third shape on 2026-08-14
  still had two-shape leads after Run 14's write-up, while
  the `--block`-installed per-shape line and anchor beneath them named three;
  the leads are the author's and nothing compared them with the population.
  `--block` knew both and now says so on stderr, the way it reports
  a summary-row disagreement. **Three readings and not one, and the second
  is the ruling worth keeping**: which shapes the lead names, in what order,
  and each `l` and `sInner` against `Main.hs`. The order is load-bearing because
  the per-shape paragraph is installed in run order and labelled *in the lead's
  order*, so a lead listing them otherwise does not go stale --- it mislabels
  three live ratios, which is the one of the three that no reading of the block
  can catch. Silent over every one of Run 17's leads, and the same defect family
  as the summary row's own check and the floor-movement sentence above:
  a hand-written line over installed content going stale under it.
- `ANSWERED` **Have `--block` price a class-property break against the floor,
  not only sort it --- taken 2026-08-22, and re-aimed the same day off the pure
  slot the shipping decision retired.** A property is stated on the published
  `time` column, so the sort settles ties in it and `--block` reports a break;
  Run 15 found that five of its seven breaks were ties inside their population's
  floor and one, `revsome`, was *inverted* against the paired reading,
  `bq-scan-rem-gm-mulback` leading at 1.0469 where the column had it behind.
  Each break now carries its paired margin, win count and sign p, that margin
  against the population's own A/A floor, and a line where the pair reads
  the other way round from the column. **What it makes of Run 17 is why
  it was worth writing**: seven of the eight classes break the top-of-the-table
  property, six of them inside their own floor and only `reshape1` outside it,
  at 50.98% --- which is the class the cross-class table already bolds,
  so the check reproduces the reading a careful run makes by hand and would have
  kept a falling count of breaks from being quoted as a trend. The inversion
  fires on class runs already on disk.
- `ANSWERED` **Print the eight-way extremes, because a class superlative has
  no derived source --- taken 2026-08-22 as `--extremes`.** *Widest
  of the eight*, *best of the eight*, *tightest floor of the eight* are claims
  about every class at once, and nothing printed them: `--block` sees one class,
  the cross-class table is hand-assembled, and the sort was left to the eye. Run
  15 got three of them wrong in one draft --- `scaled`'s spread called narrowest
  where `rev`'s is, `window`'s pure-slot gap called widest of the eight
  on the column where `reshape1`'s is wider on the pair, and `offtab`'s best
  class named before it was sorted --- every one caught by an independent reader
  rather than by a check. The mode ranks the populations it is given
  and `install-tables.sh` calls it once, after the installs and installing
  nothing: the cross-class summary stays hand-assembled, its emphasis being
  a per-run judgement, and what a rank owes the author is the sort
  under the sentence rather than the sentence. **The gap from the regime 3 fix
  to the best arm outside its family is printed both ways and the mode says
  where the two disagree**, which is Run 15's second error exactly: on Run 17
  the widest is `bcastmid`'s on the published column and `rev`'s paired. **What
  it does not rank is the main set**, which it refuses, that population having
  no row in the table these claims are made about --- so a superlative meant
  over all nine has no source here either.


## The goal of these benchmarks

**Nothing in this chapter changes from run to run.** It changes when the harness
changes radically, or when a ruling here is refuted --- and a ruling refuted
is a paragraph rewritten, not a figure updated. What it holds is why
these shapes and not others, why these strategies and not others, which designs
were tried and died, and what all of it was for: [the fix
in `Data/Array/Internal.hs`](#the-fix-in-dataarrayinternalhs), which is the goal
the rest of this file exists to have reached. Figures do appear here, inside
rulings that rest on them, and those are re-quoted when a run moves them;
the *rulings* are not re-verified each run.

Those rulings are architecture decision records in all but format --- context,
decision, consequence, and an evidence trail that makes them re-openable rather
than merely re-readable. The prose form is kept deliberately, since the evidence
is the point and a template tends to shed it. What the resemblance is worth
is a warning about growth: if the rulings outgrow the chapter, the ADR answer
is one record per file with an explicit *status* --- and the thing to carry
over would be that field, since what this README keeps getting wrong
is not stating a ruling but noticing when a later measurement has superseded
one.


### How the strictly positive picture was achieved

Four findings turned the mixed picture into `bq-expand`. **Price the outer
multi-index once per run, not once per element**: an `m`-element base-offsets
table (`m = product (init sh)`) drops the output to one `quotRem` per element,
where the first attempt paid one per *dimension* per element, which
was the whole cost on the small high-rank shapes. **Then the table build is what
remains, and it is a separable grid**, so `concatMap`/`enumFromStepN` builds
it with no division and no lazy cons-list --- a `foldl'`-over-a-`build`-list
does not fuse away, and that is `bq-expand`'s edge over `offsets-quot`.
**Strictness bangs on the hot loop are performance-essential**, worth ~2x
on their own, and are carried into `Data/Array/Internal.hs` with the logic.

**While this was achieved, the harness had to be hardened** --- criterion `env`
employed to move input construction outside the clock, `NOINLINE` so no result
is hoisted out of the timed loop, and the agreement check in a separate `check`
mode so it cannot share a computation with the benchmark via CSE. Under
it the ranking is stable and every time scales with `l`, so nothing is being
optimised away.


### Where the shapes come from

The benchmarked shapes are regime-3 arrays as horde-ad's shaped `conv2d`
and other programs produce them: it compiles to an im2col patch gather
(`CommonShapedOps.slicezS` builds a `[1, nCinp, nKh, nKw]` patch per output
position of `[nImgs, nCout, nAh, nAw]`), whose strided view is normalized
through `toVectorListT`. The patch depends on the image and the two spatial
positions but not on the output channel (it is shared across output channels,
which enter only the later dot), so the patch tensor is `[nImgs, nAh, nAw]` x
`[nCinp, nKh, nKw]`.

In general the source's transposes merge into that view, so its innermost
dimension is strided and normalizing it takes regime 3 --- which is the input
`mkStrided` builds (see its comment in `Main.hs` for how). Other operations
reach regime 3 by other routes, and those are the [stride
classes](#the-stride-classes-and-what-they-cover), populations of their own
beside this one.


### The shape set

The conv-derived shapes: the patch tensor, per image, laid out
`[outH, outW, Cin, KH, KW]` --- the per-image `[nAh, nAw, nCinp, nKh, nKw]`
of the patch tensor above, renamed to the conventional axes (output spatial,
input channels, kernel) --- and its per-position `[Cin, KH, KW]` slices,
with dims from real nets --- kernels 3x3 (VGG/ResNet, horde-ad's own CNN), 5x5
(LeNet), 11x11 (AlexNet); channels 1 up to 512; spatial from horde-ad's 6/24
to AlexNet's 55.

The `stretch-*` shapes are not conv-derived --- extreme rank, extreme aspect
ratio, non-power-of-two dims, a cache-hostile innermost stride, a run length
of one element, a base-offset table as long as the result, a page-aliasing
power-of-two stride, and a mid-range innermost extent --- to probe the space
beyond convolution. See `convShapes`/`stretchShapes` in `Main.hs` for the full
list.

**The conv set was halved after Run 6, and the shapes that went are not to come
back one at a time.** A strategy sees a shape as its innermost extent `sInner`,
its rank and its `l`, and nothing else --- not which paper the dims came
from --- and each dropped shape duplicated a kept one on all three while costing
a proportional share of every run. The freed wall clock went to A/A controls,
which calibrate every other figure and were the roster's scarce resource.
The halving moved the published geomean and the ratios between strategies past
the noise floor --- a change of population and not of any strategy, which is why
Run 7 was read against Run 6 restricted to the surviving shapes. The ruling,
and the two shapes that must survive any later cut for a reason unrelated
to their workload, sit at `convShapes` in `Main.hs`, beside the list.


### Dropping the minibatch dimension

The minibatch dimension `nImgs` is dropped --- every shape is for one image.
It never appears in a regime-3 array anyway: when the whole patch tensor
is normalized at once (`stoVector`) `nImgs` is a leading dimension,
so a minibatch scales that call's `l` linearly (the rank-5 shapes); when each
position's `[Cin, KH, KW]` slice is normalized separately
(`mvecsWritePartialLinear`) `nImgs`, with `nAh, nAw`, is an outer position,
so a minibatch scales the number of calls, not each `l` (the `*-slice` shapes).
Either way total regime-3 work is linear in the minibatch size (`nImgs` = 7
in horde-ad's own CNN; tens to a few hundred in general training).

`tooBig` (in `Main.hs`) lists realistic layers excluded because even one image's
patch tensor exceeds `sizeCap`, the element count that partitions benchmarked
shapes from flagged ones: past it a call is slow enough to starve the sample
count, and the run is long and memory-hungry with it. Those shapes are excluded
from runs, not unmeasurable: after Run 9 they were promoted into the shape set
behind a temporary edit, to settle what the allocation area should be
for a caller whose arrays are this size ([the floor section][floor]). `Cin`
and the spatial dims scale `l` linearly too (in the full run, doubling `Cin`
~doubles the cost, quadrupling the spatial area ~quadruples it), but reducing
them reproduces a shape already here --- a per-position slice, or a smaller conv
--- so `nImgs` is the only dimension genuinely free to drop.


### The stride classes and what they cover

`mkStrided` transposes the two innermost dims of a dense array, so every stride
the main set carries is positive and its offset is zero. The library reaches
regime 3 through other operations too --- its two commonest inputs of that kind
among them, a broadcast being stride 0 and `rev` negative --- and the **stride
classes** are one population per producing operation, named by the prefix
that selects them: `rev` (every stride negated, offset at the top), `revsome`
(a strict subset reversed, so the signs are mixed), `bcast` (an innermost stride
of 0, every run re-reading one element), `bcastmid` (the stretched axis
in the middle instead), `reshape1` (the `[n] -> [n, 1]` trap, innermost extent
1), `slice` (a view of a larger source, so a non-zero offset with positive
strides), `window` (overlapping im2col patches --- the workload this README
opens by naming, carrying the overlap that the main set's bijective index map
drops) and `scaled` (superincreasing strides, none of them 1). Each is a short
list in `Main.hs`, reusing a main-set shape where one fits so that a class
figure has a positive-stride counterpart to stand next to; each generator's
comment there says what it models, and the comment heading them all, above
`mkRev`, carries the coverage argument --- a hypothesis about what a valid
hand-built view can recombine, not a theorem --- which is not repeated here.
*Class* unqualified means one of these; the other sense in this README always
keeps its noun, *method* --- a `class method`, the class-method tier, or in full
a `Vector`-class method.

Two rulings govern how they are measured and published, both taken 2026-08-07,
ahead of the implementation:

- **Each class is its own pinned population**, published beside the main geomean
  and never folded into it. The geomean is a ranking statistic over a pinned set
  and a change of population moves it, as the conv-set halving measured; there
  is no combined figure to compute, so a sentence comparing populations compares
  their tables. One process per class follows from the same ruling,
  and `read-run.py` enforces it --- it names the population it read, fails
  a file spanning two, and refuses to emit a table for one.
- **No strategy is excluded from any class.** Every one is to be fixed to work
  on all of them, seen failing first wherever the failure can be fired.
  The see-it-fail run found nothing to fix: the Int32 strategies' partial sums
  are each the offset of a real element, in-bounds for any valid view whatever
  the stride signs, so the feared failure cannot fire below a 2^31-element
  source --- `int32Fits`'s own unfireable case. What mixed signs did break
  was the packed scan's assert --- a corner formula, maximal only for positive
  strides, with no lower bound, its claimed maximum observed sitting below
  a real entry of `revsome-mid-cnn-L2`'s own base-offsets table --- fixed
  at the builder, the numbers and the argument recorded at the assert and both
  Int32 comment sites.

**A class population is three shapes**, against the main set's two dozen, which
is deliberate --- the classes are there to vary the *mechanism*, and varying
size and rank within one is the main set's job --- but it decides how their
results read. A class geomean rests on three cells, so it is a summary
of a handful of numbers rather than a statistic over a spread; the per-shape
figures are nearly the whole population and are worth quoting where the main
set's would be flattened away; winsorizing has almost nothing to cap
and `--pair`'s bootstrap interval almost nothing to resample. What a class run
can decide is whether an *ordering* inverts under its mechanism and whether any
strategy's `worst` crosses 1 there. What it cannot do is be compared
with a main-set number, in either direction.

**What the eight are worth as instruments, read against each other for the first
time on 2026-08-14, over Runs 10 to 13.** Per class: the median A/A deviation
runs 0.08% (`slice`, `window`) to 0.34% (`scaled`); the worst cell 3.80%
(`revsome`) to **11.59%** (`scaled`, its standing slot); the median `CI%` 0.05
to **0.33**, `bcast` alone five times the field and its shapes the ones
the excess-allocation predictor says cross the nursery; and the correction's
amplification 1.30x (`reshape1`) to 1.81x (`scaled`), so one class makes
the same raw wobble read half again worse than another does. **The finding
is not a class property at all**: in every one of the eight the *distant* twin
is the slower half, +0.09% to +0.65%, where adjacent twins sit within +-0.2%
of zero. One-directional across eight classes and four runs is not scatter.
**And its cause is a confound in the crossed design** --- every distant twin sat
in the group's first dozen slots with its base later, so *distant* has always
also meant *earlier*, and a residual cold start is exactly what produces
that sign. Four changes followed, all the same day. `gen-unsafe`'s distant twin
moved to the group's tail, where it had landed two slots from its base
and spanned nothing; with `list`'s distant half late by construction, the next
run reads early-distant against late-distant and can say which of the two
the bias was. **Every class took a third shape**, two being too few
for the winsorizing that protects the main set, so a single disturbed cell owned
a class geomean --- and each new shape is that class's own extreme rather
than another size: `bcastmid-b200k` takes the stretch factor to the size cap,
`reshape1-rank10` the odometer to rank 11 at one run per element,
`slice-coprime-r7` the rank to 7 under a slice, `window-64x64-k1x9` the kernel
to 1 by 9 for an innermost extent of 1, and `scaled-r5` scatters 15015 outputs
over 42735 source elements. `--block` now prints the largest pair's **raw**
ratio and its amplification beside the net, which `--aa` always had
and the eight blocks a run never did; and it prints a **steps** line, `rev`
and `slice` carrying the most mid-bench steps of any class. What stays open
is `bcast`'s `CI%`, which Run 14's `-A1G` half now reads directly, every class
running on both halves.

**Each new shape was checked to belong to its class and not merely to compile**,
which `check` cannot say --- it holds an arm to the reference on whatever view
it is given, so a shape in the wrong list would pass it. Read off `check`'s own
printed view, strides and offset, all 24 class shapes satisfy their class's
defining property: every stride negative under `rev`, mixed signs
under `revsome`, a zero stride innermost under `bcast` and in the middle
under `bcastmid`, an appended size-1 dim under `reshape1`, a positive offset
under `slice`, the repeated window strides under `window`, and superincreasing
strides none of them 1 under `scaled` --- with all 50 checked shapes at regime 3
and none disagreeing. The predicates discriminate rather than passing
everything, which is what makes that worth quoting: the only foreign match
is the three `reshape1` shapes satisfying `bcast`'s test, and that is the code
saying so, `mkReshape1` being `mkBroadcast` of the shape with a 1 appended.


### The scratch vector flavour

Every table this suite builds --- the `m`-element base-offsets of the `bq-*`
family, the `l`-element offset tables, the odometer's dimension vectors --- used
to live in a **Storable** `Int` vector, because the payload is Storable
and nothing said the scratch had to follow. The fallback
in `Data/Array/Internal.hs` builds an **unboxed** one, deliberately: index
scratch is independent of the abstract element storage `v`, and the section
above says so in as many words. Nobody had noticed that the arm labelled
*shipped* in the results table therefore measured a vector flavour the shipped
code does not use, and no figure in this README had ever priced the difference.

The probe that settled it, 2026-08-08 at -O1: a twin differing from `bq-expand`
in the table's flavour and in nothing else, in the roster slot beside it, five
arms over the whole shape set so the correction rode along. Paired, which
is what a margin measured per shape wants:

| | unboxed vs Storable |
|---|---:|
| paired geomean | **0.9433** |
| 95% interval | 0.9103..0.9817 |
| shapes won | 19 of 24, sign p 0.0066 |
| `worst` cell | 0.302 against 0.369 |
| `alloc` | 3.11x against 3.15x |

**The unboxed table is 5.7% faster, roughly twice the floor**, its interval
clears 1, and it wins on the worst shape by more than it wins on the geomean.
Allocation is unmoved, so this is speed and not volume --- the same bytes, held
differently, by a mechanism nothing here measured and the probe does not need.
The one shape it loses is `stretch-square-1341`, which was the worst-measured
shape of both runs and is this README's standing warning about reading a single
cell.

**It was measured twice, with the arms' roles exchanged**, which is why
the figure is quoted flatly rather than hedged. The first run put an unboxed
twin beside a Storable roster, on a machine with other work on it, and read
0.9377 (interval 0.9081..0.9690); the second put a Storable twin beside
an unboxed roster --- after the conversion below, so the roster was by
then the other flavour --- on a quiet machine, and read 0.9433. They agree
to 0.6%, inside the floor, winning on the same 19 shapes of 24, and their tables
agree to three digits on `alloc` and to two on `worst`. A margin that survives
exchanging which arm is the twin, the machine's load and the direction
of the change is the code's and not the harness's.

**So every scratch vector here is now unboxed, matching what ships.** Three arms
keep a Storable table and must: `backperm` hands it to `unsafeBackpermute`,
`cm-gather` and `all-expand` to `map`, and each of those takes one vector
family, so for them the table's flavour *is* the payload's and unboxing it would
change the strategy rather than its scratch. They
are the new-pure-`Vector`-method tier, and that is the same fact seen
from the other side. `strideOffsets` and `baseOffsetsExpandVS` exist for exactly
those three and say so.

**Run 7 (Harness) is the first run to measure the converted suite, so the tables
now say what the library actually does.** On the shapes the two runs share,
`bq-expand` moved by -6.3% against the probe's -5.7% --- the prediction met
at full budget --- while the family did not move as one:
`bq-scan-packed-mulback` came out 4% *slower*, spread evenly over the shapes,
and `mut-odo-vecdims`, whose dimension vectors were Storable when its 0.051
was taken, read 0.056 on those same shapes --- neither priced by a probe
that had measured the `m`-table's flavour and not theirs.

**Both were put to a twin probe, 2026-08-08 at -O1**, each twin differing
from its base in that flavour alone and sitting in the slot beside it, ten arms
over the whole shape set with `list` and both `sum-only` halves
so the correction rode along. Paired, and restricted to the 22 shapes the two
runs share, which is the basis the two moves above were stated on:

| | the flavour's own effect |
|---|---:|
| `mut-odo-vecdims` / its Storable-dims twin | **0.9658** (0.9528..0.9793), 17 of 22 |
| `bq-scan-packed-mulback` / its Storable-table twin | **1.0369** (1.0243..1.0520), 0 of 22 |

**The packed scan's 4% is the flavour; the vecdims arm's is not.** Unboxing
that table costs `bq-scan-packed-mulback` 3.7%, on every shape of the set
and by a margin matching what the conversion was seen to cost it --- the one arm
the conversion hurt, and unexplained. The dimension vectors go the other way:
unboxed is 3.4% *faster*, so the conversion was worth -3.4% to `mut-odo-vecdims`
and removing the suspect deepens its move to about +13%. What is left
is position and code layout, which only a full roster can separate. Allocation
is identical within each pair, as two build-identical arms must be. The probe's
own gates: the `sum-only` halves agreed at 0.9991 and the term scaled 1.03x
across the set, while its one in-situ arm read 0.982; with no A/A pair
in the process its floor is Run 7's, which both margins clear.


### One element type, and what the probe found

Everything timed here is `Storable Double`, horde-ad's element storage, while
the fallback all of it justifies is polymorphic over the `Vector` class
*and* the element type. What the element changes is the copy --- its width sets
how many elements a cache line holds, and the instance sets what a write costs
--- and what it does not change is the index arithmetic, which is the only thing
the strategies differ in. So the question was never whether the magnitudes move
but whether the **ordering** does, and whether `bq-expand` stays under `list`
at every instance the library serves.

The probe, run 2026-08-08 at -O1 on the desktop this README's other figures come
from: three arms --- `list`, `bq-expand` and `mut-odo-vecdims`, spanning
the list, the per-element generate and the run copy --- over six shapes chosen
to span `sInner` and `l`, one process per type, by `cabal run probe -- f32`
and its siblings. Three further points, each varying one thing against
`Storable Double`: `Storable Float` is the same instance at half the width,
unboxed `Int` the same width in another instance, `Storable Word8` the same
instance at the narrowest width there is. Each figure is that type's own geomean
against that type's own `list`:

| element type, at -O1 | `bq-expand` | worst | `alloc` | `mut-odo-vecdims` | worst |
|---|---:|---:|---:|---:|---:|
| `Storable Double` | 0.189 | 0.317 | 3.73x | 0.084 | 0.112 |
| `Storable Float` | 0.189 | 0.321 | 3.23x | 0.095 | 0.137 |
| unboxed `Int` | 0.187 | 0.321 | 3.72x | 0.080 | 0.116 |
| `Storable Word8` | 0.193 | 0.322 | 2.85x | 0.073 | 0.106 |

**The ordering holds at every type, and `bq-expand` is never close to `list`.**
It spans 3.2% across the four, about the floor, and its `worst` --- the column
that answers what a geomean cannot --- sits between 0.317 and 0.322, so
on no shape of any type did it come within three times of the fallback
it replaced. That is the property that had to hold for every instance,
and it holds with room to spare and almost no variation, across an eightfold
range of element width and two `Vector` instances.

**What does not hold is the tidy width story.** `mut-odo-vecdims`
is not monotone in width: `Float` (0.095) is *worse* than `Double` (0.084)
though its elements are half the size, while `Word8` (0.073) is the best
of the four. That is a property of the measurement and not a stray cell ---
it reproduced on two independent runs, before and after the probe became
a program of its own --- and it is unexplained. It is also nowhere near
an inversion, so it bears on the width intuition rather than on any ruling here.

**Three cautions on the table.** It is **uncorrected** --- a probe carries
no `sum-only` bench --- so every column is compressed toward 1 by the forcing
pass; that cannot flip an under-1 verdict, the correction only moving a ratio
further from 1, and it falls on all three arms of a type alike. The `alloc`
column divides by `8*l` whatever the element, so a narrower type reads low
by exactly the result vector's own share: predicted 0.50x below `Double`
at `Float` and 0.875x below at `Word8`, observed 3.23x and 2.85x against 3.73x
--- both to the digit, which makes that column a consistency check as much
as a caveat. And three arms over six shapes is a probe, not a run.

**Re-probed under `-fspec-constr`, 2026-08-08, and the ordering holds there
too.** Run 8 moved the ordering at `Storable Double`, which is this section's
own trigger for re-probing, so the four types were re-run in that regime, same
six shapes, same three arms, one process per type:

| element type, at `-fspec-constr` | `bq-expand` | worst | `alloc` | `mut-odo-vecdims` | worst |
|---|---:|---:|---:|---:|---:|
| `Storable Double` | 0.148 | 0.245 | 2.61x | 0.092 | 0.123 |
| `Storable Float` | 0.156 | 0.248 | 2.11x | 0.098 | 0.140 |
| unboxed `Int` | 0.159 | 0.267 | 2.60x | 0.093 | 0.133 |
| `Storable Word8` | 0.153 | 0.247 | 1.73x | 0.093 | 0.123 |

**Everything the -O1 table is read for survives.** The ranking is the same
at every type, `bq-expand` spans 7% across the four where -O1 gave 3%,
and its `worst` sits between 0.245 and 0.267 --- so on no shape of any type does
`bq-expand` come within three times of the fallback it replaced, in either
regime. The `alloc` column's consistency check reproduces to the digit: dividing
by `8*l` whatever the element predicts `Float` 0.50x below `Double` and `Word8`
0.875x below, and the observed gaps are 0.50x and 0.88x. So does the width
oddity --- `Float` is again *worse* than `Double` for `mut-odo-vecdims` despite
half the width, which is now a two-regime observation and still unexplained.
The one thing that does not carry is the comparison itself: these figures
are the probe's, uncorrected, and belong beside the -O1 table above rather
than beside any run.

**These figures are the probe's own.** `Probe.hs` is a separate program
with its own transcribed arms --- all four types, `Double` included,
so that none of them is served by the roster's originals while the others run
copies and a difference could be an artifact of the copying. The price
is that its `bq-expand` is bq-expand-*shaped* rather than the roster's,
so a figure here never belongs beside one from a run. Its six shapes are copies
too, and those *are* held to `Main.hs`'s own dims by `--lint`, which is
not a hypothetical guard: three of the six were transposed when first written
and the check named all three.

**So one element type stays, and generalising the suite stays refused** --- now
on evidence rather than on cost alone. The cost argument is unchanged
and is under [what the benchmark does](#what-the-benchmark-does); what has
changed is that the coverage it buys is measured. Boxed elements
are deliberately absent, and not for cost --- their elements are thunks, so each
arm would defer a different share of its copy into the forcing sum
and the fill/forcing split every figure in this README rests on would not hold.
Probing boxed needs a design of its own, not another duplicate.


### Lemire multiplicative inverses, at the two division sites

**The idea (arXiv 2012.12369)**: precompute `M = floor(2^64/d) + 1` once per
divisor, then `n div d` is the high word of `M*n` and `n mod d` the high word
of `(M*n)*d` --- two 64x64->128 multiplies instead of a division.
It is implementable purely, through GHC's `timesWord2#`, so unlike the mutable
fills it needs no new `Vector` method. That is what made it worth trying: a pure
strategy that could move the family without touching orthotope's classes.

A run base-offsets strategy divides in two places, and the answer is opposite
at each. Both benchmarks below are one-line substitutions of `fastQR`
for a `quotRem` against a control already in the table, so each measures
its site and nothing else.

**At the per-element output site it wins at -O1, by 6.0%, and buys nothing
under `-fspec-constr`.** `bq-expand-lemire-out` is `bq-expand` with the shared
`i quotRem sInner` replaced, the table build held at `baseOffsetsExpand`. At -O1
(Run 7) it is faster than its control on 22 shapes of 24, with the published
columns agreeing with the per-shape geomean, so no part of that rests
on the warm-up ramp. Run 8 puts the same pair at 1.0015 over 24 shapes, 12 wins
and sign p 1: a dead tie. The regime is the whole difference --- same arms, same
shapes, same machine, one flag --- so what the trick buys is however much
of the division GHC has not already dealt with, and the answer
is regime-specific in a way nothing else in this README is. The two extremes
survive the flip. `stretch-inner256` is still the arm's best cell (0.74
of its control) and `stretch-square-1341` still its worst (1.25), the run's
worst-measured shape --- read that one as the shape, not the strategy; what
the flag moved is the twenty-odd shapes between them. Two controls back both
readings. Its allocation is identical to `bq-expand`'s on every shape, which
is what a build-identical arm must show; and it runs *before* `bq-expand`
in the group where `bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot
bias would flatter one and penalise the other and cannot produce both.

**At the per-dimension build site it loses in both regimes, by 35% and by 42%.**
`bq-gen-lemire` is `bq-gen` with the per-run, per-rank `quotRem`s replaced,
and it is 1.352x slower at -O1 and 1.421x under `-fspec-constr`, faster
on no shape of the set in either. The shape of the loss says why: it tracks
*rank*, not element count, rising from a few percent on the rank-2 shapes
to over half at ranks 7 through 12. The cost is paid per dimension,
so the division was never what dominated there. Two reasons. (i) The paper's win
assumes you want a quotient *or* a remainder; an odometer decomposition wants
both, so the trick pays twice and collects once --- where `quotRemInt#` is one
`idiv` yielding both. (ii) The magic table is a third list to walk in step
with `nts` and `sts`, adding a dereference and a pattern match per dimension
to the very loop whose per-dimension work was the target. Rank 2 costs least
because there is only one dimension to walk, though not nothing.

**What separates the two sites is (i) and (ii)**: at the output the divisor
is a loop invariant, so `M` is computed once for the whole fill with no list
beside it, and the per-element work really is one division against two
multiplies. The win is 6.0% rather than several-fold because the hardware has
moved since the paper --- 64-bit `idiv` on this Zen 3 is ~14--19 cycles against
the 40--90 that made the trick famous.

Two things a Core dump settled that source reading had got wrong. Both
are recorded because both were argued the other way first. **`quotRem` on `Int`
is not one instruction**: GHC wraps `quotRemInt#` in two guard branches,
for a zero divisor and for the `minBound quot (-1)` overflow, both
on a loop-invariant divisor --- so the `d == 1` guard `fastQR` needs is
not the asymmetry it looked like, the baseline carries two of its own.
And **the first `fastQR` spent three multiplies where the algorithm needs two**,
taking the quotient from `timesWord2# m n` and then recomputing the low half
as a separate `timesWord# m n` when the one `timesWord2#` already yields both.
Fixing that is what turned the output site into the win it now measures,
and it recovered part of the build site's loss too --- enough to see, nowhere
near enough to reverse it. Why the low half must not be recomputed is recorded
as a comment on `fastQR`, so the loose form is not written again.

**On shipping it.** `bq-expand-lemire-out` is pure, so the argument that kept
`mut-odo` out (a bar then, a weight since the mutable ceiling's amendment) does
not apply; what it costs is `MagicHash` and `UnboxedTuples`
in `Data/Array/Internal.hs`, about a dozen lines of helper, and a precondition.
The precondition is the substantive part: Lemire's identity holds
for `d, n < 2^32`, and `n` here is the linear output index, so a shipped version
needs an `l < 2^32` test choosing between the two fills --- loop-invariant
and chosen once per call, but it must be there, since orthotope does
not otherwise cap array length. **The conditional this paragraph used to end
on has resolved against it**, and against shipping: the 6.0% is an -O1 figure,
the deciding regime is `-fspec-constr`, and under the flag the same pair
is a dead tie --- so what there is to weigh against `MagicHash`, the helper
and the precondition is nothing. This README still only prices the arm; at zero,
the pricing is the answer.


### Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes --- chosen
to push past the ranges the rest cover, and named here without their prefix ---
against the strategies nearest the decision, each as a multiple of `list`
on the same shape. These are Run 13 (SpecConstr)'s own figures,
from its **basis** half as the fingerprint is, all of them net of the forcing
pass like the rest of the README. A `lemire-out` column stood between
`bq-expand-b` and `mut-odo` until the precondition ruling took
`bq-expand-lemire-out` out of the timed roster, a column a later run could only
have left standing under its own name. What that arm's per-shape behaviour
showed is in [the Lemire section][lemire], which is where its decision lives
anyway:

| shape      | bq-expand | bq-expand-b | mut-odo | vecdims |
|---|---:|---:|---:|---:|
| `inner1`     | 0.076 | 0.069 | 0.277 | 0.097 |
| `rank12`     | 0.228 | 0.225 | 0.296 | 0.100 |
| `wide-2xM`   | 0.088 | 0.082 | 0.181 | 0.067 |
| `coprime-r7` | 0.107 | 0.107 | 0.060 | 0.032 |
| `pow2stride` | 0.068 | 0.068 | 0.070 | 0.070 |
| `primes`     | 0.102 | 0.102 | 0.031 | 0.029 |
| `inner256`   | 0.069 | 0.069 | 0.016 | 0.016 |
| `tall-Mx2`   | 0.072 | 0.072 | 0.018 | 0.018 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which
is the axis the orderings turn on; the fuller per-shape record is in [What
the next run compares
against](runs/run19.md#what-the-next-run-compares-against).

- **Which strategy wins is decided by the innermost extent (the size
  of the innermost dimension, `sInner` below) --- not by the rank, not
  by the element count.** `stretch-inner1` is where the expansion family does
  best against the odometer fills: `bq-expand` (0.076) and `bq-expand-b` (0.069)
  beat `mut-odo` (0.277) and `build` (0.271) three- to fourfold, which they do
  on no other shape here --- `stretch-pow2stride` excepted, where the two
  families converge outright (0.068--0.070 across expansion and odometer alike).
  Its innermost extent is 1, so each base offset covers a single element:
  the odometer that `mut-odo`/`build` step has nothing to amortize over, while
  the expansion build has no per-element odometer to begin with. At the other
  end `stretch-tall-Mx2` has an innermost extent of half its length
  and the ordering inverts completely --- `mut-odo` 0.018 against `bq-expand`
  0.072, with every mutable fill ahead of every pure arm (the slowest fill
  0.058, the fastest pure arm 0.064). The geomean reports that second case
  and averages the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry:
  that `stretch-inner1` is *the only shape where the pure expansion strategies
  beat every mutable one*, with the four `bq-expand` variants taking the top
  four slots. They no longer do, and this roster says so more plainly than Run
  6's: `mut-flat-gm` and `bq-mut-runs-gm-mulback` take that shape tied at 0.027,
  both ahead of every expansion variant, while `mut-odo-vecdims` sits at 0.097
  --- strategies that did not exist, or were not rostered, when the claim
  was written. The unit innermost extent still explains why `mut-odo`
  and `build` do badly there; it never implied that no mutable fill could.
- **Per-shape figures are far noisier than the geomean: trust the first digit
  only.** Independent runs of these shapes agree within 1--5% on most cells
  but differ by up to 27% on `stretch-inner1/bq-expand-b` --- runs whose rosters
  also differed, making the [roster effect][floor] a candidate cause ---
  and the order of `bq-expand{,-b,-zf}` within their sweep of `stretch-inner1`
  flips between runs. The sweep itself reproduces; which of the three leads does
  not. `stretch-square-1341` is this run's standing warning on the point: again
  the worst-measured shape of the set by median and mean CI% (1.278 and 1.251
  on Run 13, both the highest here, as they were on Runs 9 to 12). It stays
  in the column, its influence capped. Run 8 added that it is also where
  `bq-expand-lemire-out` lost hardest of the twelve shapes it lost on; that arm
  is untimed since the precondition ruling, so the observation is Run 8's
  and no later run re-establishes it.
- **But check for a structural reason before discounting a cell as scatter,
  and check `stretch-inner1` in particular.** It is the shape whose innermost
  extent is 1, so a strategy that special-cases or elides a unit dimension
  behaves differently there *by construction*, and a striking figure is
  then the design showing through rather than noise. Two in `Main.hs` already
  do: the mul-back output hoists `s == 1` out of its loop entirely,
  and `baseOffsetsScan` elides unit dims, which on this shape leaves one real
  radix so no carry ever fires and the scan degenerates to a sequential fill.
  On that shape both sit far from their own averages: `bq-scan-packed-mulback`
  reads 0.129 there against a 0.108 geomean, while `bq-mut-runs-mulback` reads
  0.030 against 0.078 --- its best cell of all 24, as it was at -O1. Those four
  figures are quoted rather than looked up because both arms have since left
  the timed roster and their per-shape columns left the fingerprint with them;
  the reading is Run 8's and is what a later run would have to re-establish
  before using it. Read such a cell first and average it away last.

All three bullets are measured on positive-stride views. The [stride
classes](#the-stride-classes-and-what-they-cover) put the same axis under other
mechanisms --- `bcast`'s innermost stride of 0 has every run re-read one element
whatever its extent, `reshape1`'s extent is 1 by construction, `scaled-rank1-m1`
is a single run --- so each class run is a test of whether `sInner` still
decides, and a class table that contradicts this ruling is a finding to write up
rather than a cell to average away.


### The fix in Data/Array/Internal.hs

**Decided 2026-08-22, completed 2026-08-24, and landed the same day: the regime
3 fix is `vFillStrided`, the whole-kernel class method, its shared driver
`genericFillStrided` a bang-for-bang port of `mut-odo-vecdims-add-in-leaf-u2`**
--- the decision and what it rests on are [in the ceiling
section](#the-mutable-ceiling-taken), the signature ruling and the rejected
forms [in the two-stage plan](#the-two-stage-plan-and-the-rework-proposal),
and the arm's refinement from plain `mut-odo-vecdims` rests on the two paired
probes the ceiling records. `bq-expand`, the last candidate, is what every claim
below was measured against; the branch no longer carries it.

Regime 3 now goes through the class: `toVectorListT`'s innermost-strided branch
is `[vFillStrided sh ats ao l v]`. The method's default is the pure `bq-expand`
form --- `runBaseOffsetsT`'s expansion table, one `quotRem` per element ---
so the `[]` reference instance and any instance outside the tree compile
unchanged on a fast pure path, and the three vector-backed instances override
it with `genericFillStrided`, written once against `Data.Vector.Generic`, which
supplies the mutable machinery orthotope's own `Vector` class deliberately does
not: an allocate-once output, the odometer with the input offset stepped
additively, the innermost outer level fused into a dedicated run loop,
and the run fill unrolled by two with its bound on the output cursor, so
it is sound for zero and negative strides. The bang patterns
are performance-essential, ported with the loop structure from the benchmarked
arm; the shipped file does not set `-fspec-constr` --- the aligned HEAD probe
read the flag irrelevant to the shipped family, the two builds agreeing to three
decimals ([the ceiling](#the-mutable-ceiling-taken)) --- while it stays
the regime every figure behind the decision was measured in.

Validation on this branch:

- orthotope's own test suite: **407/407 pass** (Dynamic/Ranked/Shaped x
  boxed/storable/unboxed), with the fallback live through the method.
- Non-vacuity: deliberately dropping the `+ tInner` from the driver's unrolled
  second read fails 63 of the 407, `rev_2` among them --- so the pass
  is not vacuous.
- This benchmark: `check` agrees with `list` on every shape of every class
  for the ported arm (re-run 2026-08-24 with the Run 20 arms added),
  so the algorithm the driver ports covers negative, mixed-sign, zero
  and overlapping strides; the library port itself is validated by the suite
  and the break above.

End-to-end re-measurement in horde-ad's `bench/ConvVjpBench.hs` --- wiring
this branch's orthotope in and rebuilding ox-arrays + horde-ad --- is owed
and not yet done for this form: the run recorded in that repo is the `bq-expand`
form's.


### The mutable ceiling (taken)

**Decided 2026-08-22: the ceiling is to be taken; the code landed 2026-08-24
and the heading's *not taken* went with it.** `mut-odo-vecdims`, refined
the same day to its `add-in-leaf-u2` form, becomes the upstream implementation
of the regime-3 fallback, with the new `Vector` method it needs ---
the signature the Core below shows is free in its callback form, and decided
2026-08-24 as the pure-typed whole-kernel form --- and, since 2026-08-24,
no condition on the strides: the redirect is dropped for [the two-stage
plan](#the-two-stage-plan-and-the-rework-proposal), whose rework proposal serves
its constituency at the dispatch instead, so the fix is fully decided. What
the decision rests on, requoted from Run 19 rather than carried forward:
`mut-odo-vecdims` heads the main set at 0.055 of `list` with a worst shape
of 0.126, its family heads eight of the nine populations, and its worst in any
class is 0.110 (`reshape1-rank10`), so it was never slower than `list` anywhere
this README has measured. The one population its family does not head
is the redirect's case: in `reshape1` the flat fills own the top, `mut-flat-gm`
at a geomean of 0.033 against `mut-odo-vecdims`'s 0.094 --- though not on every
shape of it, `mut-flat-gm`'s worst there (0.135) lying above `mut-odo-vecdims`'s
0.110 on the same shape, so a redirect wants a predicate on the strides finer
than the class. On the main set, per shape, the best arm outside the family
beats `mut-odo-vecdims` on **3 of the 24 shapes**, and two of the three by more
than a thousandth: `stretch-inner1` (`sInner` 1, `bq-mut-runs-gm-mulback`
and `mut-flat-gm` both 0.032 against 0.090) and `stretch-pow2stride` (`sInner`
64, `bq-mut-runs` 0.115 against 0.126), with `stretch-wide-2xM` tied to within
one thousandth and `stretch-tall-Mx2` and `stretch-square-1341` now tied
the other way. Across the class shapes it is **5 of 24**, three of them
`reshape1`'s, with `window-64x64-k1x9` and `bcast-tall-Mx2` the others.
So the unit and huge-`sInner` ends of the set are where a redirect
on the strides would pay, and the summary table's *best outside family* column
says where else: `mut-flat-gm` in `rev`, `revsome` and `window`,
`bq-mut-runs-gm-mulback` in `reshape1`, `build` in `bcast`, `bcastmid`
and `slice`, and `mut-odo` in `scaled`, only `reshape1`'s ahead
of `mut-odo-vecdims`. **And one thing the decision now has to weigh that it did
not**: `mut-odo-vecdims-add-in` leads the arm chosen on both halves of Run 17
with significant sign tests, at margins still inside the floor --- [its own
entry][open] has what would settle it. Of what the decision owed, the class
method and its instances, the suite pass and the non-vacuity break landed
2026-08-24 ([the fix section](#the-fix-in-dataarrayinternalhs) has them);
the claims re-read is settled, applied at Run 19's write-up; what stays owed
is horde-ad's end-to-end re-measurement, its recorded gather figures being
the `bq-expand` form's.

**The `bq-*` strategies still fill the result one element at a time.**
The tightest possible shape drops to a **mutable result buffer**: allocate
it once, walk the outer odometer, and write each innermost run with a tight
additive inner loop --- no `quotRem`, no base-offsets table, no per-element
step. That is `mut-odo` and `mut-odo-vecdims` (0.049), the latter 2.11x
over `bq-expand` on Run 13 (SpecConstr); its family holds the top of the table,
`mut-odo-vecdims-add-in` leading it on a tied sign test with both printing
0.049. All allocate essentially just the result vector. `offtab` (0.136 on
Run 16) does not go that far --- its output is an ordinary `vGenerate` and only
its `l`-sized `Int` offset table is filled mutably, so it needs no class method,
just a mutable scratch --- and it sits **21% behind `mut-odo`** for it on Run
16, at four wins of 24 with sign p 0.0015, where Run 10's aligned half read 26%
and its unaligned half tied them: alignment decided this comparison and three
runs since have held it. On these numbers it is no longer the cheap way to most
of the gain, as it was when Failed Run 6 had the two tied, and the gap it must
close to become one again is 2.6x against `mut-odo-vecdims` (0.3901 paired, 24
shapes of 24).

**Plain `mut-odo` has stopped making the case, and it is not the regime's
doing.** Run 8 read the pair 1.08x *against* `mut-odo` and blamed the flag,
which sets that arm back hardest but one; Run 9, same flag, has the geomean back
on `mut-odo`'s side at 0.947, Run 10 at 0.9671 aligned, Run 11 at 0.9842 and Run
12 at **0.9719** --- and it is still not a win, at nine shapes of 24 with sign p
0.31 and an interval covering 1. The geomean and the win count point opposite
ways because the pair's per-shape range is enormous, 0.236 on `stretch-inner256`
to 3.699 on `stretch-inner1`, so a handful of large shapes carry the geomean
while most shapes go the other way; read the sign test, and the answer is a tie
in all five runs. What removed `mut-odo` from the argument was therefore
not `-fspec-constr` alone: the arm moved 9% *faster* between Run 8 and Run 9
on a roster change, `bq-expand` moved 3% slower, and the tie survived both.
The tier's argument rests on `mut-odo-vecdims` alone in both regimes, which
is a narrower base than the ruling below was written against: two arms agreeing
became one arm carrying it.

The catch is the API: a buffer filled across runs cannot be expressed
by the per-element `vGenerate`; it needs a new `Vector`-class method exposing
a fill (or the `Storable`-only `unsafeCast` escape the amendment below records).
`build` prices exactly that --- `mut-odo` driven through `vBuildVS`, a prototype
of

    vBuild :: Int -> (forall s. (Int -> a -> ST s ()) -> ST s ()) -> v a

--- and Run 6 had it matching `mut-odo` on every shape, so **the class method
was free there** (it inlines to the identical loop). Run 7 (Harness) broke
that identity, `build` reading 1.24x behind `mut-odo` paired and slower on 22
shapes of 24, on cells whose own CIs are hundredths of a percent, with neither
arm's source changed between the two binaries.

**The Core says the identity holds and the gap is the measurement --- in both
regimes now.** Dumped from Run 6's source and Run 7's against one pinned
dependency set, `$wfbBuild` and `$wfbMutOdo` are the same worker in both
binaries --- byte-identical once GHC's numbering is normalised, with `vBuildVS`
surviving as no top-level binding in either --- and the two sources differ only
by the `Strides` newtype's zero-cost cast, which falls in both arms alike,
so neither binary is the odd one out. Nor is a dependency: `vector`
and `criterion` have been the same versions across those runs. A probe
then failed to reproduce the gap at all --- in a binary relaid out by two
inserted arms the pair reads 1.004 paired (0.976..1.032, 11 shapes of 22), 1.24x
falling outside its whole per-shape range. Dumped again from Run 8's own commit
under `-fspec-constr` (2026-08-08) the two workers are still the same worker,
identical once the numbering is normalised down to the four floated
`init`/`last` error thunks each carries a private copy of, and `vBuildVS`
is still no top-level binding. **Run 17 checked the emitted code rather
than the Core and found what that predicts** (2026-08-22, off the `-g3` twin):
`$wfbMutOdo` and `$wfbBuild` are **1224 bytes each**, and of those 1224 only
**80 differ, in 34 runs of one to four bytes**, with a longest identical stretch
of 131 --- which is one function emitted twice at two addresses, the differing
bytes being address-relative operands and nothing else. So the identity now
rests on the Core in two regimes *and* on the machine code, and the pair stays
this README's cleanest known-true-ratio-1 control. **It is also the contrast
that makes the vecdims family's readings legible**: there no two arms share
their whole code at all, only an innermost run-fill and only four of the five,
which the family measurement below in this section has arm by arm.
So **the signature is free**, and no `vBuild` is to be held back on either run's
figure.

**What the pair has become is a second instrument, and it is read where
the other instruments are.** Two top-level names with identical Core are a true
ratio of exactly 1, which is what the A/A controls are built to supply,
and this pair disagrees by far more than they do --- so it prices what placement
does to two *separately compiled* arms, where the twins price only what it does
to two calls of one. That reading, its figures in every run and population,
and the per-loop account underneath it are [in the floor section][floor]
and are deliberately not repeated here: what this section needs from the pair
is only that its disagreement is placement rather than the abstraction, which
is what leaves the identity above licensing `vBuild`. A pure-typed alternative
(a strided-gather method taking the shape/stride/source and hiding the mutation
inside each instance, as `vGenerate` already does) would keep the speed without
`ST` in the signature --- and on 2026-08-24 this form was decided,
over a `Mutable`-exposing signature and over `vBuild` itself; [the two-stage
plan](#the-two-stage-plan-and-the-rework-proposal) carries the ruling
and the rejected forms.

This was **deliberately not taken.** Orthotope's `Vector` API was to stay pure
and minimal, and the gain over `bq-expand` (pure-Haskell either way, so [the
C-gap](#the-c-gap-still-a-deeper-ceiling) bounds both) did not justify a new
class method across all four instances. The strategies stay here as the measured
evidence for that ruling --- since amended below: the evidence now prices
the option instead of closing it. `mut-odo-vecdims` keeps the stake high rather
than settling it: the fill's real cost was the odometer's cons-list traffic,
not the fill itself, and Run 10 (SpecConstr) prices the class-method tier
at 2.11x over `bq-expand` (0.4745 paired). The best pure arm is now
`bq-scan-rem-gm-mulback` at 0.098 on Run 19, so what the class method would buy
is `mut-odo-vecdims` over that: **1.79x**, not 2.11x --- which is the figure
the ruling turns on, and which reads **0.5572 paired at 23 wins of 24**. It has
now read 1.80x at -O1, 1.68x on Run 8, 1.87x on Run 9, 1.85x on Run 10
with its aligned half giving 1.84x, and **1.79x** here, against 1.79x on Run 18
--- the same 23 wins of 24 as Run 10's aligned half, and a paired figure
that has moved five ten-thousandths across a REPETITION of one binary --- Run
18's basis and Run 19's are both ghc-9.12.4 and byte-identical. Across an actual
change of compiler it moves much further, to 0.5208 on HEAD, which is 1.92x.
So the spread is a tenth either side of 1.8 and neither the pairing
nor a repetition moves it. Read it as *approaching 2x and volatile at the tenth*
between runs that differ, and do not reopen or close the ruling on a movement
of that size --- Run 10 showed the volatility is not the layout's, and Run 11
shows it is not the run's either, which leaves the roster and the regime as what
moved it.

**Amended 2026-08-07: the bar is now a weight.** The tree itself carries
a precedent this section did not weigh: `Data/Array/Internal/FastReshape.hs`,
a `runST` flattener over this same fallback territory --- structurally
`mut-odo`, an allocate-once mutable result filled through an outer odometer
recursion with a per-element strided inner copy loop, its outer offsets stepped
additively where `mut-odo` multiplies --- which sidesteps the `Vector` class
altogether by `unsafeCast` to `Double`/`Float` on element size. So neither
mutability nor needing a new class method *disqualifies* a strategy any longer.
What keeps both as weights against one is that FastReshape.hs is not in use ---
absent from the cabal file, and still declaring its source project's module name
and imports (`CoreCompiler.ArrayReshape`; `Utils.Misc`, `CoreCompiler.Error`),
so it does not even compile in place: precedent for writing such a module,
not for shipping one. A mutable or class-method strategy is now priced against
that weight rather than refused at the door.

**And now weighed in code, 2026-08-08: the four FastReshape arms.** They port
the precedent's loop arithmetic onto `mut-odo-vecdims` one axis at a time, a 2x2
plus one over that shared control: `mut-odo-vecdims-add-in`, the input offset
stepped additively in place of the loop's one multiply;
`mut-odo-vecdims-add-out`, the output position through a precomputed stride
table in place of the threaded return --- the axis that can lose;
`mut-odo-vecdims-add-both`, the corner, doubling as the endpoint contrast
that still reads if the solo margins sit inside the floor;
and `mut-odo-vecdims-add-both-down`, both loops in the count-down-to-zero form,
over the corner as its control. Any close pair among them is to be read
workers-first, per the `build` lesson above.

**Run 10 priced them on a build where the loop's placement cannot
be the answer** (the paragraph after next is what makes that true) **and Run 11
reproduced every one of them**: against `mut-odo-vecdims`, `add-out` **1.1588**
where Run 10 read 1.1612, `add-both` **1.1173** against 1.1184, `add-both-down`
**1.0512** against 1.0527 at the same 7 wins of 24, and `add-in` **0.9934** (21
of 24, sign p 0.00028) against 1.0009 at 13 of 24 --- three of the four inside
a quarter of a percent, and the fourth the sign-test flip [the Results
findings](runs/run19.md#results) read as the instrument rather than the arm.
The corner stays sharply sub-additive --- 11.7% where the two solo losses sum
to 15.2% --- and the count-down form still recovers most of the corner's loss,
0.9408 against it on 22 shapes of 24 where Run 10 had 0.9412 on 24 of 24.

**Run 9 had priced them differently, and the pre-run reading was right about
the sign and wrong about the size.** That reading --- one shape, Run 8's regime
--- put all four behind their control by +4% to +12%, the corner sub-additive
and the count-down form recovering two thirds of its loss. Over 24 shapes Run 9
read `add-in` **1.1552** (0 wins of 24), `add-out` **1.1795** (1 of 24),
`add-both` **1.1645** (1 of 24), each against `mut-odo-vecdims` and each
with sign p at or below 3e-06. So all three solo-or-corner arms sat behind their
control by more than the one-shape probe suggested, and near-unanimously across
shapes --- which the write-up first read as the precedent's arithmetic losing
on both axes, and which the Core reading two paragraphs down withdraws:
near-unanimity across shapes is what the identical-code pair shows too,
so it separates nothing. The corner is sharply sub-additive, 16.5% where the two
solo losses sum to 33.5%, so the two axes are largely paying for the same thing.
The count-down form is the one that pays: `add-both-down` reads **0.8745**
against the corner on 23 shapes of 24, recovering nearly the whole loss rather
than two thirds, and it ties the shared control outright (1.0183, 13 of 24, sign
p 0.84). Allocation was not in doubt and is not --- all four read 1.00x,
the stride table costing about 1.3 KB against a megabyte-scale result.

**Why the count-down form pays is now in the Core, and why the other three lose
is not what this section took it to be** (2026-08-09, `-fspec-constr`).
`add-both-down`'s innermost run-fill is seven instructions where every sibling's
is eight: it carries the output position in a register and steps it, where
the others rebuild `outPos + j` with a move and an add on every element.
That is a per-element change, and Run 9 agrees it behaves like one ---
its advantage grows with `sInner`, r -0.29 against log `sInner`, 1.052 where
`sInner` is 3 or less against 0.972 where it is 8 or more. The other three do
not. `add-in`'s counted loops are identical to its control's instruction
for instruction, its whole code difference sitting in the odometer recursion,
where one multiply becomes an accumulated add threaded as a further argument ---
a per-*run* change. **Run 17 confirmed that in the machine code, and measured
the whole of the family rather than its loops** (2026-08-22, `-fspec-constr`,
spans off the `-g3` twins). **No two arms share their whole code**,
and the sizes sort them into exactly the two kinds this paragraph names.
`mut-odo-vecdims` is **3472 bytes over 929 instructions with two `imul`**;
`-add-in` is **3424 over 927 with one** --- 48 bytes and two instructions apart
in total, the missing multiply being the whole of it, which is this paragraph's
per-run substitution seen in the emitted code. The other three are a different
thing: `-add-out` 4440 bytes over 1170 instructions, `-add-both` 4416 over 1179
and `-add-both-down` 4424 over 1167, each carrying some 950 bytes and 240
instructions the control does not --- the `scanr (*)` table built once per call,
which is why they are per-run costs and not per-element ones. `-add-out` keeps
both multiplies at two `imul` where `-add-both` and `-add-both-down` drop
to one, as the corner and the down form should. **What is byte-identical is only
the innermost run-fill, and only across four of the five**: `-add-both-down`'s
is 24 bytes and seven instructions where the other four share one 28-byte,
eight-instruction body, which is the per-element change above and why
`loop-offsets.py` groups those four as copies of one loop. The discriminating
`imul` was checked in the **timed** binary as well, in a window around each loop
--- one for `mut-odo-vecdims` and none for `-add-in` --- so it is
not a debug-build artifact. What none of this reproduces is a per-run
*signature* in the timings: the `-add-in` advantage is flat in `sInner`, as Run
9's readings were. `add-out` and `add-both` carry real extra code of the same
kind --- a `scanr (*)` over the shape, built into a byte array once per call
and read once per run --- which adds nothing to the per-element loop.

**Run 9 could not see those as per-run changes and Run 10 can, which
is the second thing the pairing bought.** On Run 9 the three penalties were flat
in `sInner` (`add-in` r +0.21) and largest on `stretch-tall-Mx2`, shape [2,
900000], where the odometer descends twice per call --- 1.3152, 1.2930
and 1.2901 there, which two multiplies and a two-element table cannot cost.
That was the argument for suspending them, and it was right to suspect
the figures: they were layout. Read on Run 10's aligned half, where every copy
of the shared loop sits at offset 0, the same regression comes out the shape
a per-run cost has to have. **`add-out`'s penalty scales as 1/`sInner`**, r
**-0.64** against log `sInner` and **-0.01** against log `m`: 1.423
on `cnn-L1-6x6-c1` and 1.340 on `cnn-slice-c32`, both `sInner` 3, against 1.009
at `sInner` 256 and 0.997 at `sInner` 64. A cost paid once per run and amortized
over the run's elements is exactly a penalty that falls with the run's length
and ignores the number of runs, and `stretch-tall-Mx2` --- the shape whose 1.29
was the objection --- now reads level. `add-both` tracks it at r -0.64,
and `add-in`, which is free, is flat at -0.16 over a 0.955--1.078 range.
So the code identified in 2026-08-09's Core reading is the code that pays,
the arithmetic is per-run as that reading said, and what stood between the two
was the address of a loop neither arm's difference lives in.

**The two solo axis figures were suspended on that reading, and Run 10 resolves
the suspension in opposite directions.** The suspension said: what costs 16%
on them is not the arithmetic they port, the loop doing the per-element work
being the same code in all four arms, but the layout span, their executed copy
of that loop straddling a cache line where their control's does not ([the floor
section][floor]). Run 10 put every copy of that loop inside a line in one binary
and at offset 0 in another, and read the three arms in both:

- **`add-in` is acquitted and the suspension becomes a withdrawal.** It reads
  0.9937 and 1.0009 against its control, where Run 9 read 1.1552. Stepping
  the input offset additively in place of the loop's one multiply costs
  **nothing**, and the +15.5% recorded for it was the address of a loop the two
  arms share. **Run 17 takes this one step further**: the same substitution
  is now read as a small *gain* rather than as free, on five readings
  and with the missing `imul` visible in the machine code ([its entry][open]).
- **`add-out` is convicted, and the corner with it.** It reads 1.1266 resident
  and **1.1612** aligned, `add-both` 1.0906 and 1.1184, on four placements
  between them and no straddle among any of them. So the +18.0%
  is the arithmetic's after all: carrying the output position through
  a precomputed stride table, in place of the threaded return, costs about 16%,
  and the corner's sub-additivity is a property of the two axes and not of where
  they landed.

**That is the outcome the registration named as killing the straddle hypothesis
for the arm that shows it, and it kills it for two of three.** What survives
is sharper than what it replaces: of the three axes FastReshape's loop
arithmetic ports, one is free, one costs 16%, and the count-down form that ties
its control is the third.

**The pad probe had upheld the suspension**, and this is where the two
instruments part. Stepping a shared loop through all eight offsets prices a deep
straddle at 1.19 against a resident copy, and these three sat at mod 40, 44
and 44 against a control at 24 --- a predicted 1.18 against the 1.155 to 1.180
they read, on a family and a binary the probe never touched ([the floor
section][floor]). The agreement was real and was a coincidence for two
of the three arms: the correction the probe supplies is a *screen*, licensed
only where the loop is the same code, and here it is the same code while
the arms differ elsewhere as well. Read that as the screen's stated limit
meeting a case it could not see rather than as the probe being wrong --- its own
binaries, which differ in placement and in nothing else, still reproduce
to a median 1.0%.

**What that does to the precedent's weight.** FastReshape's arithmetic, ported
one axis at a time onto this README's fastest arm, buys nothing here and one
axis of it now demonstrably *costs*: the count-down form ties the control,
the additive input offset is free, and the precomputed output stride table
is 16% behind on a layout that cannot be blamed. So the in-tree precedent argues
for the *shape* of a mutable fill and not for its arithmetic, and the ruling
above is unmoved: what a new class method would buy is still `mut-odo-vecdims`,
at the **1.79x** the ruling above prices, and none of these four adds to it.

**Four arms extend the decomposition for Run 20**, added 2026-08-24: the two
mechanisms the verdict leaves unpriced solo, each over the arm it varies.
`mut-odo-vecdims-down` is the count-down run fill over the shared control ---
the one per-element mechanism above, freed of the table that buries
it in `add-both-down`'s reading --- and `mut-odo-vecdims-add-in-down` the same
form at both loops over `add-in`. `mut-odo-vecdims-add-in-leaf` fuses the leaf
call into the innermost outer level over `add-in`, removing the per-run non-tail
call, level check and threaded return that no arm above varies --- the additive
output axis at the one level that pays it, with no table.
`mut-odo-vecdims-add-in-leaf-down` is the corner: one change from the leaf arm,
the fill form at the fused site, and the endpoint against `add-in`. Run 19
predates all four and runs the roster without them.

**A same-day paired probe pruned the four to two** (`probe-run20arms-*`,
the `probe-addin2` design: the seven family arms of interest in one process
so the group shares its placement, three processes each
over `cifar-L2-16-c64-k3`, `stretch-wide-2xM`, `stretch-inner256`
and `stretch-square-1341`, criterion's own mode, one build at `-fspec-constr`).
The leaf arm is the finding: **0.83** of `add-in` on `cifar-L2-16-c64-k3`
and **0.68** on `stretch-wide-2xM`, flat at 0.98 to 1.01 on the two long-run
shapes, 10 of 12 process readings below 1 --- the per-run mechanism's own
signature, growing as runs shorten, and on the short-run shapes past the 1.22
an unaligned build's placement can span. The corner ties it, 0.999 over its 12.
The down solo arms are refuted, by codegen rather than by the stopwatch:
under the leaf continuation `>> return (outPos + sInner)` the live `outPos`
pushes the down fill's loop invariants out of registers --- **40 bytes over 11
instructions**, in the timed binary and its `-g3` twin alike, against
the canonical 24 over 7 that `add-both-down` keeps in the same build, the extra
four read off the disassembly as per-element reloads of `tInner` and both base
pointers off the closure, one of them dead --- and they probe 1.06 to 1.22
behind their controls at 0 of 24 readings below 1, worst where runs are longest,
which is a per-element signature. So the down fill wants a unit-return context
--- the output-stride table bought `add-both-down` one at a price, the fused
leaf buys the corner one for free, and the solo cell has none --- and both solo
arms are rostered `Only`, the reason at their definitions. Two bounds on reading
the probe: in this build's draw the live up-form fills of `mut-odo-vecdims`,
`add-out` and `add-both` straddle a cache line while `add-in`'s sits resident,
enough to explain `add-in` probing an out-of-band 0.90 of its control
on the short-run shapes; and the probe is one build, so the leaf margin's size,
not its direction, waits on Run 20.

**A second probe the same day priced two further fill forms and added one arm**
(`probe-x-*`, the same paired design on a scratch build, three processes each
over `cifar-L2-16-c64-k3`, `stretch-wide-2xM` and `stretch-square-1341`,
its `check-x.log` beside it; the leaf pair replicated at 0.8376 and 0.6809
in that different binary, which is the design's own control). The fill
**unrolled by two**, epilogue for an odd or empty run, is the arm it added,
`mut-odo-vecdims-add-in-leaf-u2`, and the trio left timed, with the rework's
block beside it, takes the roster to 1272 benches: a 48-byte, twelve-instruction
main body --- six per element, one branch per two --- probing **0.9696
of the corner at 9 of 9 readings below 1**, 0.9559 on `cifar-L2-16-c64-k3` and,
the interesting cell, **0.9655 on the DRAM-bound `stretch-square-1341`**, more
than its instruction count explains; the reading offered, as a reading,
is memory-level parallelism, shorter iterations fitting more strided misses
in the out-of-order window. It carries no counter at all, the bound living
on the output cursor, so it is stride-sign-agnostic and supersedes the up/down
question inside the run. The dead-ideas ruling below kills unrolling
by the runtime `sInner` only; a fixed factor was untested until this probe.
**The intermediate fused-bound form is refuted as a wash and is not rostered,
recorded here so it is not re-derived**: the falling counter merged
into the output cursor it duplicates compiles to the promised six-instruction
body --- the seventh, a `test` the native backend emits redundantly after `dec`,
was never the bottleneck --- and probes 0.9967 at 5 of 9 below 1, inside any
floor. Unrolling by four is the one cell of this axis left unprobed.

**A third probe, 2026-08-24 late, put the whole family on GHC HEAD with every
hot loop aligned, on a quiet machine** --- two binaries from this branch through
`cabal.project.ghead` and the `align-as.py` shim, one at `-fspec-constr` and one
without, the seven family arms in one process per shape, three processes per
cell over eight shapes (the five conv shapes `cifar-L2-16-c64-k3`,
`cnn-slice-c32`, `cnn-L2-24x24-c32`, `lenet-L1-28-c1-k5` and `vgg-14-c512-k3`,
plus `stretch-wide-2xM`, `stretch-inner256` and `stretch-square-1341`), the two
`Only` arms flipped timed in a throwaway clone, artifacts under `/tmp` only
and not kept. Five findings. **`mut-odo-vecdims-add-in-leaf-u2` heads the family
at 0.820 of `mut-odo-vecdims` overall** --- 0.76 on the three biggest conv
shapes, `vgg-14-c512-k3` among them, 0.63 on `stretch-wide-2xM`, and one loss,
`stretch-inner256` at 1.058 with rep spread near 0.003, so real and small;
`cifar-L2-16-c64-k3` reads 267.4 us against 203.8 us absolute. **`-fspec-constr`
is irrelevant to this family**: the two builds agree to three decimals in every
column. **The `add-in` lead dissolves under alignment**, 0.998 against
its control on both builds and both placement draws --- the reading its open
entry has been circling, that the lead was the offset and not the missing
multiply, now read directly. **The corner still ties
`mut-odo-vecdims-add-in-leaf`**, 0.872 against 0.872 with both fills resident,
so the seven-against-nine-instruction difference is below this band's floor
rather than eaten by a straddle, and the earlier placement reading of that tie
retires. **The down solo arms lose 14 to 16% uniformly across every shape** ---
1.158 and 1.137 overall, the reload penalty undiluted once placement is gone,
against the 6 to 22% the unaligned probe read with placement mixed in. Two
instrument checks carry the numbers: the five-arm binaries probed before
the `Only` flip and the seven-arm binaries after it are different layouts,
and every shared column reproduces across them to about 0.002; and rep-to-rep
spread on the quiet machine is about 0.3%, far under every margin quoted here.

### The C-gap: still a deeper ceiling

**Everything in this document lives under this ceiling.** Every strategy
in the table, every ruling resting on one, and every margin the floor
adjudicates are rearrangements *within* pure Haskell --- and no pure-Haskell
strategy closes the gap to the stride-aware C kernels. Measured on the analogous
chain (horde-ad's interleaved A/B of 2026-07-31, recorded in that repo):
concrete *scatter*, which routes through them, runs it in ~0.5 ms,
and the gather over this branch's fix takes 2.55x that in its natural
orientation, 1.32x in its fastest --- a 1.3--2.6x gap, down from the order
of magnitude the released fallback showed. What a C strided copy would leave
of it is unmeasured.

Regime 3 has no contiguous runs to hand a bulk kernel, so the transfer stays
per-element in Haskell however the fallback is written. Closing it needs C.
`bq-expand` is the pure win to take meanwhile, not a replacement for it.
This is discussed further in the horde-ad repo.


### Dead ideas

Ideas that **died on paper**, recorded so they are not re-proposed:

- **Delta-compressing an offset table** (storing Int8/Int16 steps, mostly
  the constant `tInner`, instead of absolute offsets) fails `vGenerate`'s
  contract: the callback is random-access, and recovering an absolute offset
  from deltas is a prefix sum --- a scan the callback would redo per element.
- **Reordering the expansion so the largest outer dimension expands last**
  (to shrink the `concatMap` intermediates, whose sizes are the prefix products
  of the expansion order) has no freedom to spend: the table must be indexed
  by the row-major run index, so the expansion order is fixed by the output
  order.
- **Fusing the base-offsets build into the output fill** --- the output reads
  the table at `q = i div sInner`, which ascends monotonically, so the two
  passes could stream in lockstep; but the callback would then carry odometer
  state, and a stateful fill is exactly what the mutable ceiling's class
  extension exists to provide --- so since that ceiling's amendment this idea
  is priced with it, not dead outright. The table exists because `vGenerate`
  is stateless.
- **Caching the table across calls** (horde-ad normalizes the same shapes
  over and over) --- `toVectorListT` is a pure per-array function with nowhere
  to keep a cache.
- **Padding the innermost extent to a power of two**, so the output division
  becomes shift-and-mask --- padding changes the enumeration the contract fixes,
  and conv's inner extents are 3/5/7/11.
- **A separate `q`-table** (`qtab[i] = i div sInner`, in Int32) --- strictly
  dominated by `offtab32`, which stores the finished offset for the same
  traffic.
- **Software-prefetching `v` from inside the callback** (which may legally read
  the offset table ahead of `i`) --- GHC's prefetch primops all thread `State#`,
  so a pure callback cannot issue them without an unsafe escape.
- **`constructN` instead of `scanl'` for the prefix-sum build** (its callback
  legally reads the already-built prefix) --- the scan fuses, so the fallback
  is moot, and it loses regardless: the recurrence reads `table[q-1]` back
  through a store-to-load forward where the scan carries the sum in a register,
  each step passes a freshly wrapped prefix slice, and the one power `scanl'`
  lacks --- deltas depending on earlier *values* --- is power a position-only
  delta never uses. Prefix access cannot even cheapen the carries:
  `table[q] = table[q - suffixProduct c] + st_c` still needs the same
  divisibility cascade to find `c`.
- **A branchless delta select in the scan build** (folding the carry correction
  in arithmetically instead of branching) --- the branch's outcome is periodic
  with period `sInner`, which a modern predictor learns, so the branch
  is already ~free.
- **Unrolling the scan by `sInner`** so the carry test runs once per run ---
  `sInner` is not a compile-time constant, and GHC will not unroll a loop
  by a runtime value.
- **Alternatives to the Granlund--Montgomery form for an unbounded output
  quotient.** For a stateless output loop with a runtime divisor that wants
  quotient and remainder both, the GM round-up magic is the end of the road.
  Barrett reduction's correction step is a *data-dependent* branch ---
  a misprediction generator where GM's dispatch is loop-invariant;
  floating-point reciprocals cap the dividend at 2^53 and need an exactness
  proof plus FMA to be safe; a full-width 128-bit Lemire magic spends three
  multiply-highs, worse than the division it replaces. And the general GM form's
  65-bit add-fixup never arises here: `Int` dividends spend only 63 bits,
  so a magic of width `63 + ceil(log2 d)` always fits one `Word` --- one
  multiply-high and one shift per element, no bound on `l` (`gmMagic`
  in `Main.hs`).


## About the current harness

**This chapter normally does not change from run to run either**, but
for a different reason: it describes the instrument rather than any result.
Every generic instruction for making, reading and checking a run is here,
and a session told to make one can work from this chapter alone --- but
for the two layouts a write-up pastes into, which sit beside the figures they
explain: the [Results](runs/run19.md#results) columns and the [per-class
blocks](runs/run19.md#the-stride-classes-run-by-run). What is *not* here
is anything a particular future run has to settle --- that is [What
is open](#what-is-open), the chapter at the front, which is where everything
that goes stale as soon as a run reports is now collected.


### What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT` faithfully
(specialised to `Storable Double`, horde-ad's element storage), then compares
the regime-3 strategies in one binary --- the real orthotope compiles only one
at a time, so a replica is the only way to A/B them.

**One element type, where the fix serves them all.** Everything here
is `Storable Double`; the fallback is polymorphic over the `Vector` class
and the element type. Element width sets how many elements a cache line holds
and boxed elements change the copy entirely, so the *ranking* and not only
the magnitudes may differ for the instances the shipped code actually serves.
Nothing in the roster probes that; `Probe.hs`, a program of its own, does
at three further types and found the ordering unmoved --- [the
probe](#one-element-type-and-what-the-probe-found) is the evidence
this restriction now rests on, boxed excepted.

**Don't generalise the suite to run every arm at every element type.**
The typing is the cheap part --- the payload is only ever loaded and stored, all
the arithmetic being `Int`, so `T a` and a `Storable a` context would cost about
sixty lines of signature. What it would really cost is a run per type,
and the roster shared by both is what makes figures commensurable, so the choice
is between interleaving them --- doubling the roster and re-collapsing the A/A
spans the crossed controls need --- and two processes, whose comparison
then crosses processes and inherits the roster effect. The code cost is worse
than it looks too: `NOINLINE` on a polymorphic function blocks specialisation,
so every arm would time a dictionary rather than a fill unless roughly forty
`SPECIALISE` pragmas are added, **and each of those has to be confirmed
in Core** --- an unverified one leaves the dictionary in place and the suite
then measures dispatch while reporting it as a strategy, which is the failure
mode that looks most like a result. Probe instead: a handful of shapes at one
other type, asking only whether the ranking inverts. The property that has
to hold for every instance is not the ranking but `worst` staying under 1 ---
never slower than the fallback being replaced --- and six shapes will show that.

The strategies are named here and *described* in `Main.hs`, each at its own
definition, where a reader meets the code the description is about. This list
is the index, in that file's definition order --- base before variant, which
is also the order to read them in:

- **The originals and the first attempt.** `list` (the fallback being replaced:
  `vFromListN l . toListT`, a lazy cons-list), `gen-quotrem` (a `vGenerate`
  over one `quotRem` per *dimension* per element), `gen-unsafe` (that minus
  the bounds checks, to price them), `unfold-add` and `fused`
  (an `unfoldrExactN` odometer, allocating and then allocation-free).
- **The run base-offsets family**, all with the same output --- one `vGenerate`
  doing one `quotRem` per element against a precomputed `m`-element table ---
  and differing only in how that table is built: `offsets-quot` (lazy list),
  `bq-mut` and `bq-mut-runs` (mutable odometer), `bq-unfold`, `bq-gen`,
  `bq-gen-lemire` (Lemire at the build site; kept because it *lost*, so the idea
  is not re-proposed), `bq-expand` (**the arm the file carries today**),
  `bq-expand-zf` and `bq-expand-b`.
- **The same family varying the per-element output instead**, which is the line
  every member ends in, so pricing it once prices it for all:
  `bq-expand-qr-prim`, `bq-expand-lemire-out`, `bq-expand-lemire-mulback`,
  `bq-expand32-lemire-mulback`, `bq-mut-lemire-out`, `bq-mut-lemire-mulback`,
  `bq-mut-runs-mulback`, `bq-mut-runs-gm-mulback`, `bq-scan-mulback`,
  `bq-scan-rem-mulback`, `bq-scan-gm-mulback`, `bq-scan-rem-gm-mulback`,
  `bq-odo-mulback`, `bq-scan-packed-mulback`, and the two added when
  the precondition ruling left their builds with no unconditional output form,
  `bq-expand-gm-mulback` and `bq-odo-gm-mulback`. Three of those carry no size
  precondition anywhere: the two new ones and `bq-scan-rem-gm-mulback`, whose
  builder drops the bound as well as its output.
- **Whole-offset and alternative gathers**, which build an `l`-length offset
  vector rather than an `m`-length one: `backperm`, `cm-gather`, `all-expand`,
  `offtab`, `offtab32`, `offtab-scan` and `offtab-scan-rem`, the last being
  the unconditional twin of the one before it --- its bound is the builder's,
  which no output substitution reaches.
- **Direct mutable result-buffer fills**, which need a class extension
  or explicit mutation and are the [ceiling](#the-mutable-ceiling-taken):
  `mut-odo`, `mut-odo-vecdims`, `mut-offsets`, `build`, `mut-flat`
  and `mut-flat-gm`, the unconditional twin of the last. And `concat-runs`,
  class-methods-only and the first arm to be checked without being timed
  (below).

The order they are *run* in is deliberately a different one, fixed by `roster`
in `Main.hs`, where a majority of them now take no slot at all, being checked
and not timed; the Results table below is sorted by time, a third. Sharing
that roster with the strategies, and not strategies themselves, are twenty-four
controls: eighteen A/A arms --- `bq-expand-aa-adjacent`
and `bq-expand-aa-distant`, `bq-scan-rem-gm-mulback-aa-adjacent`
and `bq-scan-rem-gm-mulback-aa-distant`, `mut-odo-vecdims-aa`
and `mut-odo-vecdims-aa-distant`, `offtab-aa-adjacent` and `offtab-aa-distant`,
`bq-odo-gm-mulback-aa-adjacent` and `bq-odo-gm-mulback-aa-distant`, and, added
2026-08-14, `build-aa-adjacent` and `build-aa-distant`, `mut-odo-aa-adjacent`
and `mut-odo-aa-distant`, `list-aa-adjacent` and `list-aa-distant`,
`gen-unsafe-aa-adjacent` and `gen-unsafe-aa-distant`, nine strategies each
duplicated in both positions --- the `sum-only-early`/`sum-only-late` pair,
and `bq-expand-nosum`, `mut-odo-vecdims-nosum`, `mut-flat-gm-nosum` and, added
2026-08-25, `canon-full-nosum`, each its base arm forced with one element
instead of the sum. [The noise
floor](#what-moves-a-figure-when-no-strategy-changed)
and [sum-only](#sum-only-and-the-correction-now-applied) say what each is for.

The `check` mode (below) asserts every strategy produces byte-identical vectors
on every shape, that each shape actually takes regime 3, and that the view's
innermost extent is the second-to-last dim as listed --- which is the one thing
`read-run.py` has to assume, since no JSON carries the strided shape, and which
`m` and every `alloc` multiple rest on. The [stride
classes](#the-stride-classes-and-what-they-cover) go through the same mode, each
held to its own structural conditions --- negative strides, mixed signs,
a stride-0 axis --- with a deliberate-breakage proof per conjunct, and each
class list has its own reading of the innermost extent in the reader, which
`check` is again the only place to confirm. It is built from that same `roster`,
so a strategy cannot be timed without being checked; what that leaves to go
stale, `read-run.py --lint` holds --- every arm named here, every strategy
defined in `Main.hs` rostered, each A/A control running the arm its name
duplicates, every control named as the reader's own control test reads it,
and every shape's `l` annotation agreeing with what its list's rule computes.

`concat-runs` was the first strategy `check` covers and the benchmark does not,
and is the only one excluded on its own noise rather than by a ruling below.
It was by a clear margin the noisiest bench of the set --- Failed Run 6's single
worst cell, and a median cell some 2.5x the shape's typical CI --- so excluding
it costs no information the run needs, and it is one of the changes preceding
the current, quieter run, though nothing separates its contribution
from the others'.

**The worry was never its own figures but its neighbours'**: every `time`
is a ratio to `list`, which runs before every strategy, so an aftermath
outliving one bench would tilt the group rather than cancel. The probes found
nothing --- its successor timed the same after it as after a benign predecessor,
and of the three A/A pairs the one straddling it agreed best. What stays
unprobed is the [roster effect][floor], worth ~18% in horde-ad's `ConvVjpBench`
and persisting for a whole run rather than one bench: unretired rather
than absent, since that case ran benchmarks of a different scale.

**Two rulings taken 2026-08-08 cut the timed roster from 38 strategies to 15,
and the arms written since bring it back to 26** --- the four unconditional
forms the precondition ruling itself called for (below), the four FastReshape
arms and, of the five Run 20 arms beside them, the three the probes left timed
([the mutable ceiling](#the-mutable-ceiling-taken)). Both rulings are about what
is worth spending a bench on, not about what is worth keeping: every dropped
strategy stays in `Main.hs` and stays in the roster as `concat-runs` is ---
checked against the reference on every shape of every class, and not timed ---
so the agreement net does not shrink and nothing has to be rewritten if a ruling
is later reopened. The 23 arms the rulings dropped carry `Only` in that roster,
each naming the bound or the multiple that disqualified it; with the controls
the run is 53 benches, and the Run 20 trio with the rework's block takes
the roster to 1272 benches, three placement-family arms having dropped to `Only`
beside them.

- **A strategy with a precondition is not measured.** The column allowed `none`,
  an empty cell, and `shape well-formed`, which is a condition on being a valid
  view at all rather than on size; everything else is a size bound the caller
  would have to discharge. What that costs is real --- it takes `bq-odo-mulback`
  (0.089), the fastest pure arm of Run 8, and the whole `mulback` output family
  with it --- and the ruling is that the speed does not make up
  for the restriction: a fallback that needs `l < 2^32` tested and a second fill
  kept for when it fails is a different proposition from one that does not,
  and this suite exists to find the second kind. **Four runs now say the cost
  was near zero**, which the ruling did not need but is worth recording:
  its unconditional counterpart `bq-odo-gm-mulback` has come in at 0.090 on each
  of Runs 9 to 13, within a thousandth of the arm it replaces, and on Run 13
  it took the head of the pure tier outright again (0.9949 paired against
  `bq-scan-rem-gm-mulback`, 7 of 24, sign p 0.064 --- a tie by the sign test
  and a lead in the published column). Dropping the bound bought back
  the restriction and cost about a point. The column went with them, having
  nothing left to say once every surviving row's cell was empty; each dropped
  arm's bound is now at its roster entry, spelled as that arm's own assert
  spells it.
- **A strategy allocating 2.4x the result or more is not measured**,
  at `-fspec-constr`, which is the regime the cut was taken in and Run 10's.
  Allocation is the one column here that is deterministic per call, independent
  of what shares the process, and reproducible across rebuilds when time is not;
  it is also, across this table, no worse a predictor of rank than most single
  facts about a strategy. The threshold keeps `bq-expand` (2.35x) and drops
  the tier above it, which is the whole of the `new pure Vector method` group
  --- `fused`, `all-expand`, `cm-gather`, `backperm`, `unfold-add` --- plus
  `offsets-quot`, `bq-unfold` and `mut-offsets`.

`list` is exempt: it is the reference every ratio divides by, not a candidate,
and its 23.5x is the thing being beaten. `gen-quotrem` and `gen-unsafe` survive
both cuts at 1.00x, which the README needs --- the first attempt is what the fix
is measured against.

**What the cut breaks, and has to be repaired when the roster is built.**
Several control relationships name an arm that is now untimed, and a control
whose base is not measured is not a control:

- the `bq-scan-mulback` A/A twins duplicated an arm the precondition rule drops,
  and **have been re-pointed** at `bq-scan-rem-gm-mulback`, the fastest pure arm
  left and the one carrying no precondition: the pair is now
  `bq-scan-rem-gm-mulback-aa-adjacent`, moved to sit beside its new base,
  and `bq-scan-rem-gm-mulback-aa-distant`, kept early so the span stays. Run 8's
  tables name the old pair because that is what ran in them;
- `bq-mut-runs-gm-mulback` survives while its stated control
  `bq-mut-runs-mulback` does not, so the pair that prices dropping the size
  bound no longer exists --- which is the ruling doing its work, since
  that pair's whole subject is the bound this rule now refuses;
- claim 4's controlled pair, `bq-scan-mulback` against
  `bq-expand-lemire-mulback`, loses both halves, and the Lemire output
  substitution loses its arm. Those *readings* stand as Run 8's and cannot
  be re-measured under this roster, which is the price of the rule
  and is recorded rather than worked around. Both *questions* survive
  on the counterparts written below, and [the claims
  list](runs/run19.md#the-claims-the-next-run-should-test) has been re-aimed
  onto them.

**The crossed A/A design survives the cut, at half to two thirds the span.**
Its three distant twins are placed early and their bases late, and 23
of the benches between them have gone: the spans fell to 25, 22 and 4
intervening benches, from 38, 31 and 8, and Run 10's roster order takes one more
off each (24, 21 and 3). That is still nothing like the twelve-arm probe where
[spans of 28 and 0 read alike][floor], so the design keeps doing what
it was built for; what it does not keep is comparability with an older span
column, a pair being a different distance apart under the same name in each
of the last three runs.

**Every dropped arm was then checked for a surviving counterpart that differs
only in not using the trick that costs the bound**, and the check turns
on splitting the bound by where it arises, since a substitution at one site does
nothing for the other. `baseOffsetsScan`, `baseOffsetsScanPacked`
and `baseOffsetsGenLemire` carry a bound of their own --- on `m` rather
than on `l`, which is what their consumers' roster entries mark
as *its builder's*; `baseOffsetsExpand`, `baseOffsetsOdo`, `baseOffsetsScanRem`
and `baseOffsetsMutRuns` carry none. Eleven of the fifteen dropped arms had
a counterpart already timed --- the mutable-scratch family through `bq-mut`,
`bq-mut-runs` and `bq-mut-runs-gm-mulback`, the scan family through
`bq-scan-rem-gm-mulback`, whose builder drops the bound the Granlund-Montgomery
output cannot reach, and `bq-gen-lemire` through `bq-gen`, its Lemire being
at the build site. Four had none and were written: `bq-expand-gm-mulback`,
`bq-odo-gm-mulback`, `mut-flat-gm` and `offtab-scan-rem`, the last
not a Granlund-Montgomery twin because its bound is its builder's. All four
clear the allocation bar already, at 1.33x, 1.51x, 2.00x and 2.35x --- measured
twice, on a quiet machine and a busy one, to the same digits, which
is the property the bar was chosen for. Three runs have now said whether they
are fast: on Run 11 `mut-flat-gm` reads 0.081, `bq-odo-gm-mulback` 0.090,
`bq-expand-gm-mulback` 0.094 and `offtab-scan-rem` 0.119, so three of the four
land ahead of `bq-expand` and the fourth behind it, as in each run before.

**Two of the eleven are covered at the level of the idea rather
than line-for-line, and say so here rather than being counted quietly.**
`bq-expand-lemire-out`'s counterpart is the mul-back output, Granlund-Montgomery
having no `out` analogue that yields quotient and remainder together.
And **the `Int32` narrowing cannot be rescued at all**: its bound is `int32Fits`
on the source, which is what narrowing *means*, so `offtab32`
and `bq-expand32-lemire-mulback` leave with no unconditional form possible.
That is the ruling's sharpest cost, because the narrowing is the one
hand-packing that survives the flag --- 0.877 of its control for `offtab32`
and 0.949 for the expansion pair, where the packed state is dominated.
The ruling stands as taken; what it gives up is measured and recorded rather
than assumed small.

`--lint` and `--markdown` both took the change with the roster: the first
asserts every defined `fb` function is rostered, which the not-timed mechanism
satisfies, and reports the not-timed set as a note rather than a failure;
the second carried `needs` and `precondition` forward from the table above,
so the column left the reader and the table in the same commit --- a column
dropped from one alone would be reinstated by the next install.


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
    cd micro-regime3 && cabal run micro \
      --ghc-options="-fspec-constr -fllvm -optlc-align-loops=64"  # LLVM, 64 B
    cd micro-regime3 && cabal run probe -- check     # the element-type probe
    cd micro-regime3 && cabal run probe -- f32       # one element type
    ./run15-lookrts -m glob 'SHAPE/list' +RTS -A32m -I0 -T -M8G  # the baked line
    #  A `+RTS` line does not inherit the baked one, so repeat the baked
    #  options in full beside whatever is being varied -- all four here --
    #  or the probe runs in a regime nobody chose and its figures are not
    #  the run's. The three lines below want the same treatment
    ./run15-lookrts -m glob 'SHAPE/list' +RTS -s     # allocation, copying, GCs
    ./run15-lookrts -m glob 'SHAPE/list' +RTS -hT    # live heap by closure type
    ./run15-lookrts -m glob 'SHAPE/list' +RTS -S     # one line per collection

`probe` is a second executable and not part of the roster: [the element-type
probe](#one-element-type-and-what-the-probe-found), whose own header
in `Probe.hs` says why it is a separate program and what its separateness costs.
Both are executables rather than benchmark stanzas, which is what lets every
mode above take its arguments directly --- and what keeps a bare `cabal bench`
from launching a multi-hour run.

The `classes` mode replaces the main set
with the [stride-class](#the-stride-classes-and-what-they-cover) populations,
one selected per process by its name prefix; without a prefix it runs all
of them into one process, which is a probe and never a recorded run, the reader
declining to publish a table over two populations.

`cabal.project.freeze` pins the resolved plan --- `vector`, `criterion`, `base`
and the rest, with an index-state --- so that a recorded run's source commit
and its dependency *versions* are both known. **What it does not pin is their
ABI hashes, and a store rebuilt at unchanged versions is therefore invisible
to it**: Run 14's and Run 15's binaries share not one package hash of 48,
at identical versions and one compiler, which relinks every call target
and leaves half of `.text` different at the same size (measured 2026-08-17,
after that difference had been misattributed to the assembler shim). So two
runs' binaries can differ for a reason nothing recorded here names,
and the pre-run list's md5 step says what to read to find out. It postdates
the earliest runs recorded here and so cannot pin theirs; what covers those
is a hand check that `vector` and `criterion` have been the same versions since
Failed Run 6 inclusive, which is what lets a question about generated code
be asked across those runs at all. One pin is load-bearing rather
than housekeeping: `vector` is built `+boundschecks -unsafechecks`, which
is what makes the `gen-quotrem`/`gen-unsafe` pair price a bounds check at all,
since one uses `VS.!` and the other `VS.unsafeIndex`. **And the module itself
is not what varies, which Run 17 settled and no run re-asks**: two builds of one
recipe back to back gave one `Main.o` by md5 WITHOUT `-fobject-determinism`,
and the control --- the previous run's recipe, twice --- gave one as well, where
two had been registered. So the flag is priced at nothing on this module, having
reproduced without it, and the run-to-run binary differences this README has met
are the store's and not this module's.

`micro.cabal` builds at -O1, which is what a default `cabal build` of orthotope
takes --- **and that is not the regime the claims decide in**, a correction made
2026-08-14 after several entries had been written on the other reading
and amended 2026-08-24: the deciding regime is `-fspec-constr`, every run since
Run 8 already in it, and the shipped file does not set the flag ([the
ceiling](#the-mutable-ceiling-taken) has the probe that settled it). Other
regimes are command-line only, the flag landing after the cabal file's
so the later `-O` wins: `-fspec-constr` when testing the `SpecConstr`
optimization effect, `-O2` for the half of the scan-fusion refutation
that inverts there (a `diag` at `-O2` is what measures it). **The RTS line
is the second thing the shipped setting fixes, and since 2026-08-21 this suite
shares it by decision: every horde-ad test and benchmark and every process here
runs at `-A32m`, and the area is not to vary again.** `micro.cabal` bakes
the whole line, `-A32m -I0 -T -M8G`, the one every recorded recipe since Run 13
carried, so no recipe passes `-with-rtsopts` any more, and a `+RTS` line
that varies anything else repeats it in full. The caller ran at `-A1G` until
then, a gap [the floor section][floor] priced on one shape and Runs 14 to 16
over the table, and what closed it is the churn findings: the tax grows
with the area and `-A32m` is their recommendation for this workload class.

**Those last four need no build and no pair**: `micro.cabal` compiles
with `-rtsopts`, so an already-built binary takes any RTS setting, and `-s`,
`-hT` and `-S` are available in a non-profiling build --- which is how Run 15
answered a registered question, found the collector mechanism behind its own
table, and named what a major collection copies, all on binaries it had already
timed. What `-s` cannot see is the churn state: on the 27719 reproducer
it prints `0 MiB lost due to fragmentation` poisoned and clean alike and reads
productivity HIGHER poisoned, and `max_mem_in_use_bytes`, the heap peak every
run prints, is flat under the tax --- so a clean `-s` or an equal peak across
two processes says nothing about which state either is in, and a fixed-n victim
reading is what dates a state. The `-O2` one is a probe. `-fspec-constr`
is no longer: Run 8 is a full recorded run in that regime, and the flag
therefore goes before the `--` of every command of the sequence rather
than being reached for once. A run whose numbers are meant to be kept
and written into this file is a different undertaking, and has a procedure
of its own: [Making a major benchmark run](#making-a-major-benchmark-run).


### Making a major benchmark run

**FIRST, THE FORK, because it decides how much of this chapter you owe and
it is four commands.** A run is either already prepared or it is not,
and the half of this procedure that builds a pair is the half most sessions do
not need. Answer these before reading anything else here:

    cd ~/r/orthotope/micro-regime3
    cat $R-pair.txt                    # NO SUCH FILE = the BUILD path
    md5sum $R-<basis> $R-<other>       # do they match the note's?
    git log -1 --format=%h -- :/micro-regime3/Main.hs
    git log -1 --format=%h -- :/micro-regime3/align-as.py

A pair whose note matches, whose md5s match and whose `Main.hs` and shim have
either not moved or moved by comments only is the **CONFIRM path**: you owe
`./preflight.sh $R`, step 9b, and then the run list from step 13, and you owe
NOTHING of the building half --- not 3b, not the two `--survey` legs,
not the note. Anything else is the **BUILD path**, which is 3b and those two
lines besides. Expect `Main.hs` to have moved: this file's prose lives
in its comments, so a write-up moves it, and only the diff tells that
from a real change. **And the run number is one past the newest file
in `runs/`**: that file is the run behind you, and the disk is where
it is written. Two headings carry it and step 5 renames both --- the run file's
own title, and *Recommended tasks after Run N* in the open list --- where
the four the old chapter needed were four because none of them was a file name.

The rest of this chapter is three checklists and the reasons behind them.
The reasons restate nothing the lists carry, so reading them front to back
before starting is the single largest waste available here --- Run 16 read
the whole of it first and needed almost none of it, and Run 18 read the whole
of it and then took the CONFIRM path the four lines above would have given it.

**What a run must read, so that nothing else is read to find out.**
This chapter's three checklists --- a fifth of its lines --- and of the rest
only the *part* each section keeps, since most of what these sections hold
is the previous run's data that the write-up is about to replace. The last run's
own file, whole, that being the one thing worth reading entire. Of [What
the next run compares
against](runs/run19.md#what-the-next-run-compares-against), the paragraphs
settling the regime, the roster and the basis, and the column rules
under the yardstick --- not its figures. Of [the
claims](runs/run19.md#the-claims-the-next-run-should-test), BOTH numbered sets
at the end --- the five live claims and the three class properties, a run
returning verdicts on each --- and not the previous run's readings above them,
which `--claims` reprints. Of [the class
blocks](runs/run19.md#the-stride-classes-run-by-run), the six numbered items
of the form and one example block --- not the other seven.
Of [Provenance](#provenance), the replace list and the delta bullets. The open
list is read by its status markers rather than end to end. Everything else
in this file is reference, and reading it is how a write-up's budget goes
without a figure to show for it.

A *major run* is the whole roster over the whole shape set at criterion's
default budget --- the main set and, by default, **every stride-class population
with it**: one process for the main set and one per class, or two of each where
the run is paired, in the order of the sequence below. Asking for a major run
asks for all of them; leaving a population out is an explicit exception
to be stated, not a choice this README leaves open. The whole is analysed
and written into the run's own file. What follows is the procedure, and
it is written to outlive any one run.

**What asking for a run asks for, since the request is one sentence and the work
is this chapter.** The whole of it, without coming back for permission between
the steps: the pre-run checks, the sequence, the write-up, and the probes
the results turn out to justify. The procedure is the permission --- each step
names what it needs and what it must not do --- so a question this chapter
answers is not a reason to stop. **Two parties appear below and this README
keeps them apart.** *A session* is whoever executes the run, here as
in the twenty-odd other places this README says it. *Whoever asked for the run*
holds the decisions a procedure cannot make, and is never called *the author*:
that word means the session writing a block --- the one whose prose
an independent checker is set against --- and it is the executor,
not the requester.

**A probe budget rides with it, and it is spent AFTER the write-up rather
than before.** It is separate from the pre-registered questions, which
are appended after the classes and were designed before the evening. What
this ordering is for: the write-up is where a run's errors are made, it is done
last, and a probe spent first is spent out of its attention --- Run 14 probed
heavily and well, and shipped twenty-one prose errors past four green checkers
because the writing came at the end of it. Take whatever measurement the run's
own *results* make worthwhile, with no ceiling on it: a discriminating reading
of a cell that came out strange, a derivation over the artifacts while they
still exist. What bounds it is the artifacts and not a clock --- spend it while
they live, most of it being unspendable afterwards. **And do not read the budget
as a concession --- it is where this README's mechanisms have come from, where
the run is where its figures come from.** Run 15's six and a half hours produced
figures, held 13 of 13 claims and confirmed a repetition, and no mechanism
at all; some two hours of probes afterwards settled five standing questions,
refuted three of that run's own published claims and found a caveat touching
every ratio here. So a question with a discriminating measurement deserves
a filtered run now rather than a slot in the next full one, which is a rule
this chapter states twice and had buried both times.

**Stop for two things.** No further progress --- a build that will not build,
a gate that fails, evidence that is not on this machine --- and a decision
that belongs to whoever asked for the run rather than to the procedure: whether
the artifacts go, whether anything is pushed, which pair the next run takes,
anything that publishes. Report those and wait; decide the rest. **THE TEST
IS WHAT THE ANSWER CHANGES, NOT WHOSE THE DECISION IS: stop only where
the answer changes what the machine does next.** Where it changes only what
the write-up says, proceed under a stated assumption and report it where
it bites --- the run collects the same artifacts whatever is decided. Apply
the test and not the category: *belongs to whoever asked* cannot be applied
from inside, since anything can be argued into it, where *changes what
the machine does next* is answerable in a sentence and would have answered every
stop this chapter has recorded. A preparation that leaves such a decision says
so outright --- Run 19's put the claims-retirement decision at the head
of the pair note in this paragraph's own vocabulary, with *before the gate
is paid* beside it, and its first operator read it as a stop and lost the night
(2026-08-24), where the test says plainly that a manifest edit due
at the write-up changes nothing the evening does.

**Confirm each long process on the screen as it finishes**, rather than folding
it into a later summary. The gate, the sequence, a rebuild, any probe that takes
a window: say that it finished, what it exited with, and whether its counts
were what the roster asked for. They run for tens of minutes to hours, and while
the rest is in progress their completion is the only thing a reader can act on.

**The pre-run half as a list, because its actions are spread over eight hundred
lines and every one of them earns its place separately.** **The three lists
below carry every operative fact in this chapter, and the prose carries
the reasons and does not restate them.** That is a contract and was audited
into being: a pass over the prose in 2026-08-14 found seventy-nine facts
that changed what an executor DOES and were in no list, which is why sessions
kept reading all thousand lines. So execute from the lists; read the prose where
a step surprises you, and where you want to know why it is there. A fact
that changes what you do belongs in a list --- if you find one that is not,
that is the defect, not your reading. And a rule's evidence goes at the end
of its paragraph, as a date and an outcome --- never inside an instruction,
and never as a chronology.

    # READ THIS LIST AND THE LAST RUN'S FILE, AND START. The prose
    # around these three lists is reference: it holds the reasons and
    # restates no fact you need, so reading it front to back before
    # beginning is the single largest waste available here -- Run 16 read
    # the whole of it first and needed almost none of it for this half.
    # Come back to a paragraph when a step surprises you.
    cd ~/r/orthotope/micro-regime3        # and re-set R and REGIME per call
    #      NN is one past the newest file in runs/, which is the run
    #      behind you, and the disk is where the number is written. DO
    #      NOT MAKE `runs/$R.md` YET: every
    #      mode defaults to the newest file, and everything before
    #      post-run step 5 -- the gate's machine check, the claims read
    #      back -- wants the run BEHIND you and would read this run's
    #      empty file instead. Step 5 makes it
    #      R=runNN; REGIME=-fspec-constr -- an EMPTY regime is a plain -O1
    #      build and nothing downstream notices. That hazard is 3b's
    #      alone: REGIME reaches the build and nothing else, so on the
    #      CONFIRM path nothing reads it and setting it buys nothing.
    #      Governing docs are this
    #      file and read-run.py's docstring; horde-ad's CLAUDE.md is not
    cat $R-pair.txt                       # 0. the note: six steps quote it,
    #      four here and two in the run list -- the halves' roles, the
    #      md5s, the commit, the gate line, and any environment its LAUNCH
    #      line puts in FRONT of a command. NO SUCH FILE is the answer to
    #      the fork rather than an error: you are on the BUILD path, and
    #      the note is written at 3b, before either binary exists. Come
    #      back to this line after it, since the steps below quote it
    #      BASIS/OTHER come from it, never from a half's name; setting
    #      them in the scripts is step 3c, and reading an older pair whose
    #      basis differs is what the environment override is for.
    #      The basis runs second, and both halves run the classes
    ls $R-*                               # 1. is there a pair? A note-only
    #      listing is the answer NO, and so is nothing at all: the note is
    #      written at 3b, so an empty listing is a run that has not reached
    #      3b rather than an impossible state
    md5sum $R-<basis> $R-<other>          # 2. is it the note's pair? On the
    #      BUILD path there is nothing to sum yet: 3b transcribes the md5s
    #      as it builds, and this line is that transcription's check
    git log -1 --format=%h -- :/micro-regime3/Main.hs   # 3. has it moved?
    git diff <note's commit> HEAD -- :/micro-regime3/Main.hs  # comment-only?
    #      MOVED IS NOT REBUILT, and this line is what tells the two
    #      apart: a comment-only diff leaves the binary the note's, so it
    #      is the CONFIRM path. EXPECT a move -- this file's own prose
    #      lives in Main.hs's comments, so a documentation commit touches
    #      it -- and read a diff that reaches CODE as the BUILD path
    git log -1 --format=%h -- :/micro-regime3/align-as.py  # 3a. and the SHIM,
    git diff <note's shim commit> HEAD -- :/micro-regime3/align-as.py
    #      which is on the recipe's -pgma and is as much an input to the
    #      binary as the source is, so it takes step 3's two lines and
    #      step 3's verdict: a docstring-only diff leaves the shim
    #      emission-identical and the pair sound, and a change to what it
    #      EMITS is the BUILD path. The run file's Provenance records
    #      its commit beside the compiler's; the fork looked at neither
    #      until 2026-08-16,
    #      when a walk found it three commits past what that section names
    #      and had to read the diff to be sure the pair was still sound
    #  the :/ pathspec resolves from the repo root, so these answer the same
    #  from anywhere; a bare `-- Main.hs` run from the root prints nothing
    #  and exits 0, which reads exactly like an unmoved source. Where the
    #  note records two commits, the other is the tree it was built in
    #  BEFORE THE FORK: if the run's own JSONs are already here, this list
    #      and the run list are both spent and the entry point is post-run
    #      step 1. Do NOT read a moved Main.hs as a licence to rebuild --
    #      the landed JSONs are provenanced to the binaries that made
    #      them, and the fork answers a question about a run that has not
    #      happened
    #  AND IF THE PREPARATION IS SPENT BUT THE GATE IS NOT: a note whose
    #      fill-in block is complete and whose GATE line reads NOT RUN has
    #      spent this list already. Yours, from this session, enters at 13.
    #      Somebody else's, or older than today, takes CONFIRM and re-runs
    #      the cheap read-only steps -- 4 to 10 cost seconds each and 9 is
    #      the whole regime guard -- inheriting only the three the note
    #      records: the gate, the smoke sweep and the roster pass
    #  1-3 ARE THE FORK, and the two branches have names this file uses
    #  elsewhere. Missing, or moved with CODE changed, sends you down the
    #  BUILD path: 3b and the two --survey lines, and nothing else. Moved
    #  comment-only is CONFIRM, the binary still being the note's.
    #  Matching sends you down
    #  the CONFIRM path, where those are skipped and step 9 carries the
    #  whole guard instead, there being no build to have carried the
    #  regime (About the current harness has that, at `--survey`). Every
    #  other step is the same on both, in the same order, which is why
    #  this is one list and not two: the fork is one step wide
    #  3b. BUILD BOTH HALVES -- the BUILD path's own step, only if 1-3 say
    #      so and from the note's own
    #      recipe. It is a STEP and a session's to run like every other line
    #      here, not a remark and not somebody else's job; what is not
    #      is the note, whose prose and verdicts are written by hand.
    #      There is no builder, every pair being two shims typed out, so
    #      write the note FIRST, from pair-note-template.txt -- it is the
    #      only copy of both recipes, and the template is what says what a note owes.
    #      WHAT THE PAIR VARIES is not in this list and not in the
    #      template: it is settled in *What Run N compares against*, and
    #      the recipe to vary is the previous run's note. Read both before
    #      writing this one -- a session executing the list top to bottom
    #      arrives here with neither, which is where a walk arrived
    #      Every build wants -fforce-recomp and a fresh --builddir, cabal
    #      answering "Up to date" for a -pgma or an environment change;
    #      the recipe SPELLS THE REGIME OUT rather than interpolating
    #      $REGIME, as every recorded note does, so that what the note
    #      says is what was built and the empty-variable hazard cannot
    #      reach a pair; $REGIME is for the ad-hoc call, and where one
    #      is written --ghc-options="$REGIME" stays quoted. Build the halves
    #      back to back with nothing touched between -- about twenty
    #      seconds each here, the dependencies being in the store and only
    #      the local package recompiled -- keep both executables, delete
    #      each --builddir once its binary is copied out, and read the
    #      pair's variable straight out of each
    #      with the note's own `strings` line before trusting either.
    #      Then transcribe into the note what only the build can say: the
    #      Main.hs and align-as.py commits it was built from, the GHC, the
    #      two md5s, .text and the fills -- the fill-in block is that
    #      transcription, and steps 2, 3, 9b and 10 are all reading it back.
    #      BUILD BOTH, ALWAYS. Reusing the previous run's basis binary is
    #      REFUTED (2026-08-16) and not to be re-proposed, whatever the
    #      source and the md5 say: the other half is built today, so the
    #      pair's two halves went through whatever the shim was on two
    #      different days. That is the effect the back-to-back rule exists
    #      to keep out, reached by a route that rule does not name --
    #      nothing is rebuilt BETWEEN the halves, the drift is between the
    #      runs -- and no step downstream can see it. Run 11's basis was
    #      Run 10's binary, which is the precedent this retires
    #      ON A REPETITION THE MD5 IS A ONE-SIDED INSTRUMENT: a rebuild
    #      that reproduces the previous basis byte for byte proves every
    #      input unmoved in twenty seconds, but one that does NOT
    #      reproduce DOES NOT NAME ITS CAUSE, and the note's recorded
    #      inputs do not cover them all. What is missing is the
    #      dependency store: cabal.project.freeze pins 97 versions and an
    #      index-state, NOT the ABI hashes, so a store rebuilt at
    #      unchanged versions relinks every call target and changes half
    #      of .text while every check here still passes, the tracked
    #      loops not having moved. So a non-reproducing md5 is a finding
    #      and not a stop, and locating it takes THREE reads, not one:
    #      diff the source, rebuild once with the previous shim commit to
    #      price the shim, and compare the two binaries' package ABI
    #      hashes (`strings B | grep -oE '[A-Za-z][A-Za-z0-9-]*zm[0-9zi.]+zm[0-9a-f]{32,}'` --- the narrower `[a-z-]` class silently drops `QuickCheck`, `Glob` and `text-iso8601`)
    #      to price the store. Run 15 did all three after its write-up
    #      had blamed the shim: the shim was emission-neutral and all 48
    #      dependencies had been relinked (2026-08-17)
    #  3c. SET THE HALVES' NAMES in the three scripts that take an OTHER --
    #      run-major.sh, run-gate.sh, smoke-sweep.sh -- and check that
    #      install-tables.sh's BASIS agrees; read-all.sh is the fifth
    #      script a run passes and needs nothing set, deriving the halves
    #      from the filenames. Here, because the names exist
    #      from 3b and everything below reads them. A wrong OTHER stops
    #      run-major.sh and run-gate.sh at a missing binary; in
    #      smoke-sweep.sh it sweeps the wrong half and looks clean
    ./preflight.sh $R                     # 4-10 IN ONE CALL, and the way
    #      to run them: each step prints PASS or FAIL with what it read and
    #      the exit status is the verdict, so none can be skipped by being
    #      forgotten -- step 8 being the one this chapter says is skipped
    #      most often. It does NOT do 9b (the pair's own variable, which
    #      only the note can name), 10a/10b (the BUILD path's, and the
    #      note's), or 11 and 12 (machine time, and the pair's to inherit).
    #      Its own non-vacuity is in its header, proved on stub halves. The
    #      steps below are what it runs, and what to reach for when one FAILs
    ./$R-<basis> check > <your tmp>/a.log 2>&1   # 4. every shape agrees
    ./$R-<other> check > <your tmp>/b.log 2>&1   # 5. and the other half
    cmp <your tmp>/a.log <your tmp>/b.log        #  byte-identical, or STOP
    #      NOT /tmp/a.log, which no seat here permits sandboxed: send both
    #      to the temp directory this session actually has, since a
    #      blocked redirect runs nothing at all. Scratch names, spelled in
    #      full: a $R-*.log here makes run-major.sh refuse hours later,
    #      and $TMPDIR is unset unsandboxed
    ./$R-<basis> --list 2>/dev/null | wc -l    # 6. roster size, then the
    diff <(./$R-<basis> --list 2>/dev/null) <(./$R-<other> --list 2>/dev/null)
    #      two halves' listings: identical is what one source built twice
    #      looks like, and the pair note asks for that half of it. THE
    #      EXCEPTION IS A PAIR WHOSE VARIABLE IS THE ROSTER, where the
    #      diff IS the variable and the note records what it should be --
    #      Run 20 is the first, 1272 benches against 1128, so read the
    #      note before reading a difference here as a defect
    ./read-run.py --lint                  # 7. roster and shape annotations
    ./read-run.py --check-doc --quiet     # 8. anchors, paths, widths, sweeps
    #      7+8 are the WHOLE document check here; no other repo's checkers,
    #      now or at post-run step 7. Exit code is the verdict: the
    #      `note:` worklists are write-up material, only FAIL: stops you, and
    #      a wrap FAIL means a HAND-wrapped paragraph, not a long one
    #      --quiet keeps the FAILs and withholds the worklists by count.
    #      Every call but one takes it; the one that does not is post-run
    #      step 7, where the worklists are read and adjudicated
    #      A `FAIL: BLOCKED:` here is a root the wrapper did not mount,
    #      usually ../../horde-ad, and it means the path check did not
    #      happen rather than that it failed: a name that is simply wrong
    #      cannot be told from one nothing searched. Get the checkout
    #      mounted and rerun, or run with it blocked and say so in the
    #      write-up -- the one thing not available is reading it as a pass
    ./check-scripts.py --families         # 8b. and the defect families, over
    #      the source of every Python program here -- the shell drivers are
    #      outside an AST family's reach -- which is the one of the three
    #      that can name a site nobody has met
    ./check-scripts.py --properties       # 8c. and its properties, which
    #      are quantified over every run JSON here rather than over a
    #      fixture, so they answer for inputs no case anticipated. It
    #      WITHHOLDS the reader's own stderr and counts it BY KIND -- the
    #      reader warns once per run per table about rows a later roster
    #      dropped, which is correct and was 198 KB against six lines of
    #      verdict. A kind with a count of one is a warning this corpus
    #      has not shown before and is the thing to read; `--warnings`
    #      restores them verbatim
    ./check-scripts.py                    # 8d. and if any script here has
    #      changed since the last run: every defect these scripts have had,
    #      planted again and refused again. Seconds, and it writes nothing
    #      OF RECORD -- no run file, no README, not even the index -- but
    #      it and 8c both write `zz-` fixtures here and remove them, so
    #      both want an unsandboxed seat. `--audit` replays each
    #      case against the code before its own fix, where it MUST fail,
    #      which is the suite's own non-vacuity and worth a look after
    #      adding one
    ./$R-<basis> diag                     # 9. the regime, in the binary
    #      read one row: allocated bytes of baseOffsetsScan against
    #      baseOffsetsMut on vgg-14-c512 -- equal to three figures under
    #      SpecConstr, 2.4 MB against 2.4 MB where plain -O1 is ten times
    #      apart, and no eye misreads that
    #  9b. and the pair's own variable, by whatever the note says reads it:
    #      diag answers for the regime and for nothing else, so what the
    #      halves differ in is checked by the note's own command -- or by
    #      the note saying which variable leaves no trace to read, and what
    #      stands in for it
    ./loop-offsets.py $R-<other> $R-<basis>    # 10. fills, kept with the run
    ./loop-offsets.py --library $R-<basis> $R-<other>   #     and the library
    #      near-total same-offset agreement is what a pair built from ONE
    #      SOURCE looks like; where the halves differ in source the figure
    #      moves wholesale, and that movement is a registered variable to
    #      be read against what the note registered rather than against
    #      this line -- Run 17's halves read 25.3% where Runs 14 to 16 all
    #      read 100%. Only `--library` PRINTS an agreement figure. The
    #      plain form lists each binary's own fills and leaves the
    #      comparison to the eye, which is a reading and not a verdict:
    #      what a sound pair shows there is the same fills at the same
    #      addresses in both sections. A note's nm-based figure is a
    #      different number again, so compare like with like.
    ./loop-offsets.py --survey $R-<basis>       # 10a. on the BUILD path,
    ./loop-offsets.py --survey $R-<other>       # 10b. never the confirm one,
    #      and the answer goes in the note: it is the binary's, not the
    #      reading session's. What it means is below, at the pad
    ./smoke-sweep.sh $R                   # 11. the smoke sweep, and read
    #      its counting: it holds each process to the arm count `--list`
    #      gives for that shape
    ./$R-<basis> -L1 --json smoke-l1-main.json         # 12. the roster
    ./$R-<basis> classes scaled- -L1 --json smoke-l1-scaled.json  # pass,
    #      ONLY if `--list` changed membership AND the pair note records
    #      none -- it belongs to the pair as the gate does, so grep the
    #      note before paying the twenty minutes; on the BUILD path that
    #      grep reads your own hour-old note, and the question is whether
    #      membership moved. Where the PREVIOUS run's basis is still on
    #      disk the membership question is answered directly and in a
    #      second -- diff the two --list outputs -- rather than through
    #      the roster delta under Provenance. Any class serves: six are
    #      three shapes and `reshape1` and `bcastmid` are four since
    #      2026-08-25 -- prefer one of the five that crossed from two,
    #      which drives `--block`'s three-shape branch. Name the artifacts probe-* or smoke-*, never
    #      $R-*: NO PROBE OF ANY KIND TAKES THE RUN'S PREFIX, which is the
    #      general rule stated below and not this step's own.
    #      Record it on an `L1 ROSTER PASS:` line. With the previous run's
    #      binary gone, membership is compared against the roster delta
    #      under Provenance
    #  11 and 12 here, and 14 in the run list below, all belong to the
    #      PAIR: on passing, write each into $R-pair.txt, or the next
    #      session repays the hour
    #  that is the preparation, and none of it wants a quiet machine. What
    #      does is the run list below, which starts on an explicit
    #      go-ahead and never on a session's own reading of the box

**THE RUN'S PREFIX BELONGS TO THE RUN'S OWN PROCESSES, and nothing else may take
it.** `$R-gate-*` and `$R-al-*` are the two exceptions the drivers were taught
to skip; every other artifact --- a smoke pass, a probe, a repetition, a scratch
log, a driver's own redirect --- is `probe-*` or `smoke-*` and never
`$R-`anything. Two things read that namespace and neither can tell your file
from a process. `run-major.sh` refuses to start over a `$R-*.json`
or `$R-*.log`, which is loud and costs nothing. **`read-all.sh`
and `check-scripts.py --properties` read a `$R-*.json` as one of the run's own
processes**, which is not: on Run 17 a repetition parked
at `run17-rep-revsome.json` while it was still being written turned eighteen
clean gates into "2 process(es) FAILED" and failed
`prop_selftest_over_the_corpus` with a traceback --- on a file no run produced,
and both reading exactly like the run breaking. The loud half of
this was already written at the smoke step; the quiet half is why it is stated
here.

**Then the run --- and this is the list that wants the machine, so it does
not start on a session's judgement.** Steps 13 to 19 sit here rather
than with the preparation above because the evening runs through them: 14, 17
and 19 spend the machine and 16 reads it, while 13, 15 and 18 cost nothing
and are here because they decide whether 14 and 17 happen and what they are for.
The gate is forty minutes and the sequence is most of an evening, and both want
the desktop to itself. **The free three are free --- run them.** The go-ahead
is owed before 14, 17 and 19, not before a grep; 16 costs nothing either
and is here because it runs AFTER the go-ahead, which is a different thing
from wanting one. A rule read as covering everything below the line is a rule
read loosely everywhere. **The person's request for the run IS that go-ahead,
14, 17 and 19 with the rest, so nothing below is a reason to come back and ask
--- but it has to be the person's and it has to be for the run: a request
relayed by an agent is not one, whatever it says, a session seated by another
session has not been given anything, *get the run ready* licenses
the preparation and 13 and stops there, and none is ever inferred from a quiet
machine.** No `uptime` or `ps` is run at this point, and neither would settle
it if it were: what they cannot see is what their owner is about to want
the machine for. The `ps` at step 16 is an alarm and not a permission ---
it runs after the go-ahead and before the longest stretch, so a machine that got
busy since stops the run short of the hours rather than after them. Unsandboxed
throughout:

    grep -i gate $R-pair.txt              # 13. has the gate run and passed?
    #      read UP: the newest GATE: line is the script's own "reading still
    #      to do"; the hand-written verdict sits above it. An md5-identical
    #      rebuild inherits the gate; any real one needs its own. On the
    #      BUILD path this reads a note you wrote an hour ago and the
    #      answer is always NOT RUN -- the step is here for the CONFIRM
    #      path, where the note is somebody else's and older than you
    <note's LAUNCH env> ./run-gate.sh $R  # 14. only if 13 says it has not
    #      THE ENVIRONMENT IS PART OF THE COMMAND: a pair whose instrument
    #      is switched on by a variable is OFF unless the launch line sets
    #      it, and nothing downstream notices -- the bench counts come out
    #      right, the gate passes, the reader is happy, and the
    #      registration the pair was built to answer comes back empty.
    #      Step 0 read it off the note; Run 17's is WILDLOG=1, on the gate
    #      and on the sequence alike, and Run 18's is WILDLOG=1 SATURATE=1
    #      on both. Since 2026-08-22 BOTH DRIVERS RECORD what they were
    #      launched with, `launch env: WILDLOG=... SATURATE=...` in the
    #      gate's output and in the wallclock log, set or unset -- so read
    #      that line back rather than trusting the command you meant to
    #      type. Each switch that IS set is also asserted per process,
    #      one `@@saturate` line and at least one `@@wild` stamp; neither
    #      assertion can see a switch left off, which is what the record
    #      is for
    #      -- and it is owed because THIS pair is two builds. A pair whose
    #      halves differ in an RTS option alone can be one binary run
    #      twice, and then none of this is owed, the gate included; the
    #      decision paragraph under what the pair compares against records
    #      why two was taken anyway. Read that before paying the forty
    #      minutes, not after
    ./read-run.py $R-gate-<basis>-a.json --compare $R-gate-<other>-a.json
    ./read-run.py $R-gate-<basis>-b.json --compare $R-gate-<other>-b.json
    #      BOTH passes, the -a pair and the -b pair: the verdict
    #      is the two agreeing. Write it by hand ABOVE the script's block,
    #      clearing `GATE: not yet run` in the same edit. A gate answers
    #      sound or not sound; never quote a magnitude from one
    ./read-run.py --para 'What Run'       # 15. the run's registered
    #      predictions. SEVERAL LEADS MATCH `What Run`, so it prints an
    #      index of leads and locations and you ask again for the one you
    #      want; `--all` prints them whole where the set is the point.
    #      READ `What Run N compares against` besides,
    #      because --para matches bolded open-list leads and a run whose
    #      registrations live under that heading returns only its
    #      predecessors', which reads as an empty registration. An empty
    #      one really is not a blocker, so this step's own licence to
    #      record it and go is what hides the miss. The pair note names
    #      where its registrations are; believe the note over the mode
    uptime; ps -eo pid,etime,comm | grep $R-      # 16. the ALARM, never
    #      the permission -- unsandboxed, or ps sees only this session's
    #      own processes. It runs here, after the go-ahead and before the
    #      longest stretch, so a machine that got busy since stops the run
    #      short of the hours rather than after them
    <note's LAUNCH env> ./run-major.sh $R &    # 17. THE SEQUENCE: many
    #      processes, several hours -- under the same environment the gate
    #      took at 14, and for the same reason
    ps -eo pid,etime,comm | grep $R-      # confirm from an UNSANDBOXED ps:
    #      comm, not args, and comm truncates at 15 characters. A blocked
    #      write leaves a launch that never happened looking like one in
    #      progress, which is how two copies once ran at once
    #      do NOT wait with pgrep -f, which self-matches and never
    #      returns. THE GENERAL FORM IS: WAIT ON A FILE'S CONTENTS, NEVER
    #      ON A PROCESS LIST -- and where the harness wakes you when a job
    #      ends, the waiter is redundant besides. Run 18 hung a shell for
    #      two hours on `until ! pgrep -f 'check-scripts'` waiting for a
    #      job whose completion it was already being told about;
    #      the sequence ENDS WITHOUT ANNOUNCING ITSELF, so arrange to be
    #      woken by `major run complete` in $R-wallclock.log rather than
    #      deciding to look: six hours of idle machine followed a session
    #      that read this line as where to look and set nothing watching.
    #      Something must be set watching, and the form is a background
    #      waiter on the file rather than on a process --
    #      `until grep -q 'major run complete' $R-wallclock.log; do sleep
    #      300; done` -- since the pid cannot be polled from inside the
    #      sandbox and the file is what the sequence actually writes
    #      nothing else on the machine, and no edit to the tree, until it
    #      ends: the driver's git lines are the binary's provenance
    #      never raise -L on a recorded run -- the figures stop being
    #      comparable with every run before it
    #      a process far slower than its neighbours is worth looking at:
    #      the previous run's -wallclock.log says what each should take,
    #      SCALED BY THE BENCH COUNT -- criterion spends its budget per
    #      bench, so a roster that grew since makes every process slower
    #      than its counterpart there for no reason worth chasing
    #      no resume. If it dies mid-sequence, hand-run the class loop over
    #      both halves with `[ -e "$out.json" ] && continue`, check each
    #      benchmarking count against `classes --list`, append to the same
    #      $R-wallclock.log, and say in the write-up that the populations
    #      ran in more than one window
    #      pre-registered probes are appended after the classes, same
    #      evening; a filtered probe takes ONE -m MODE then its patterns,
    #      and its benchmarking lines are counted before any number is read
    #      report each long process as it finishes: exit code and bench
    #      count, not folded into a later summary
    #  18. read ahead while the sequence runs, which costs no machine
    #      time: the last run's own file, which shapes the whole write-up
    #      and is worth little read after it has begun, and the open list
    #      by its status markers. NOT the replace list -- it is walked and
    #      mapped at post-run step 6, gains nothing from being read six
    #      hours early, and the read is paid twice if the session does not
    #      survive the sequence, nothing recording that it happened
    <note's LAUNCH env> ./run-alonelegs.sh $R <other>  # 19. THE RIDERS,
    <note's LAUNCH env> ./run-alonelegs.sh $R <basis>  #     control first
    #      owed with the pair since Run 16, and out of the EVENING rather
    #      than out of the probe budget: the 24 main-set `list` alone legs
    #      on each half's own binary, one bench per process, after that
    #      half's major processes. They are what turn the in-process
    #      deflation from an estimate into a per-shape measurement, so a
    #      run without them cannot check a span prediction. The script
    #      refuses a previous attempt's artifacts and reads the baked line
    #      back before anything runs
    for c in '' rev revsome bcast bcastmid reshape1 slice window scaled
    do ./run-counts.sh $R <other> $c; ./run-counts.sh $R <basis> $c; done
    #  20. THE COUNTED WORK, over EVERY population and not the main set
    #      alone -- the empty first element is the main set, and the eight
    #      that follow are the classes, `run19-counts-<half>[-<class>].txt`
    #      apiece. Instructions an iteration from two fixed-`-n` processes
    #      a cell, differenced, which owes criterion nothing: an arm whose
    #      time moved between the halves either moved its counts with it,
    #      which is codegen, or did not, which is the runtime or the
    #      memory. `--counts` reads a pair of these files beside
    #      `--compare`.
    #      IT WANTS NO QUIET MACHINE, an instruction count being
    #      insensitive to load, so this is the one owed measurement that
    #      may be taken on a working desktop and either side of the
    #      evening. That is why it is last here rather than in the
    #      preparation: it belongs to the pair, not to the hour.
    #      ABOUT TWELVE MINUTES A HALF FOR THE MAIN SET AND SEVEN FOR THE
    #      EIGHT CLASSES, measured 2026-08-25, and the classes are cheaper
    #      DESPITE holding the same 1128 cells because the cost is elements
    #      touched and not cells: each cell runs 150 whole iterations, so a
    #      class of small shapes is half a minute and `bcast`, whose three
    #      shapes include two at l = 1.8M, is two.
    #      perf must be able to count: kernel.perf_event_paranoid at 1 or
    #      less, which does NOT survive a reboot here. The script probes it
    #      on /bin/true and refuses in a millisecond rather than spending
    #      the sweep writing `!!`
    #      COVERED THE MAIN SET ALONE UNTIL 2026-08-25 and said so in its
    #      own header and nowhere else -- 22 mentions of it in this file,
    #      not one naming a population, so every one read as covering the
    #      run. A class question asked of it had no answer at all

**One rule for the sandbox in this directory, since half of what a run does must
write here.** Run everything unsandboxed except the read-only checks.
Those are worth having cheap and are all of them safe: both `check`s, `diag`,
`--lint`, `--check-doc`, `loop-offsets.py`, `--list`, a `grep` of the note,
and pre-run steps 6 to 10 --- except 8c and 8d, which write `zz-` fixtures here
and remove them. Everything that builds, benchmarks or leaves a file
is the other kind: 3b, 11, 12, 14, 17 and 19, and steps 4 and 5 too, which write
only through their redirect and that is enough. A session starts
in `~/r/horde-ad`, so its sandbox permits writes there and to its own temp
directory and nowhere else; THIS directory is outside it, and `run-major.sh`
moves here before doing anything. **And never write `$TMPDIR` here; spell
the scratch path in full.** That variable is set only under the sandbox,
so the idiom that works in a read-only check writes to `/` the moment the flag
that makes a command able to write at all is added --- silently, the write
succeeding. The rule is about the PLACE and not the variable, because
the conditional it would otherwise be turns on a property of the call, which
changes call to call here, where `$TMPDIR/x` is a habit that does not.
`/tmp/a.log` is in neither permitted directory and `/tmp/claude` is not the temp
directory in every seat; a walk's first redirect there died
`No such file or directory`. **The two refusals do not look alike, which
is the part that has cost hours.** A redirection on a simple command is checked
before exec, so the benchmark never starts at all; `log`'s `tee` is a pipeline
whose `echo` still prints, so you get the sequence's start lines on the console,
no wall-clock file, no JSON and no run. That reads as a run in progress, which
is how two copies once ended up on this machine at once. Confirm a launch
by an unsandboxed process list, never by the launching shell --- and note
that `ps` in a session lists only that session's own processes, so it catches
a launch made from here and not one made from anywhere else, `uptime` being
the half of it that reaches the machine.

**Three pre-run steps are the pair's and not the session's, and the note
is where they survive.** The one that is skipped most often is 8, and the one
that is run when it should not be is 14 --- the gate belongs to the pair,
so a note recording a pass means it is done. **And what is true of 14 is true
of 11 and 12: write each into the pair note when it passes.** All three cost
machine time, all three are properties of the pair and its roster rather
than of the session that ran them, and a session that cannot see they were run
pays for them again --- twenty minutes for the roster pass, about forty
for the gate. The note is the only thing that outlives a session, so an outcome
recorded nowhere is an outcome nobody after you can use; the gate's own line has
said so all along, and the other two now say it too.

**Steps 7 and 8 are the whole of this README's document check, and no other
repository's checkers belong on it.** Theirs carry a per-repo configuration ---
search roots, an owned module namespace, an allowlist --- so pointed here they
resolve this directory's names in their own tree and report correct names
as missing, which is the noise-for-signal failure that stops a checker being
read at all. Said here rather than beside the verification pass it governs
because a session starts in another repository and arrives
with that repository's standing checks already resident, so the moment to know
this is the moment the checklist reaches these two steps. If a future document
here does grow `file:line` citations, that is the moment to port one,
and not before.

**Where the effort actually goes, because it is not where it looks.** The run
is several hours and *unattended* --- a process sitting far longer
than its neighbours is worth looking at rather than waiting on, and what says
how long each should take is the previous run's `-wallclock.log`, which stamps
every start and finish; it costs patience and a quiet machine, nothing else.
Everything expensive happens after it, in the write-up, and that is where
a session's token budget is spent and where its mistakes are made. **The eight
class blocks are NO LONGER the bulk of the typing, and this paragraph said they
were for four runs after they stopped being.** `install-tables.sh` writes 32
computed paragraphs across them now --- table, controls, provenance, per-shape
line, cross-half line --- so what is left per class is the one paragraph of what
it says, written from the verdicts `--block` emits rather than from the table
above it. Eight paragraphs of judgement, and nothing else. **The run file's head
is the bulk**: every paragraph of it rewritten, and nothing installs any
of them. **The bulk of the *cost* is adjudication rather than typing** ---
deciding which run, which basis and which population a figure belongs to ---
and it scales with how many comparisons the run invites rather than with how
many tables it fills, so a run that is both a repetition and a pairing
is the dearest to write up for that reason alone. **The shape to expect,
in the units a session actually spends**, which are not hours but tool calls
and how much must be read before the first one. The fixed cost is the reading
--- this chapter and the last run's own file --- and it is larger than executing
either checklist, which is what both checklists are for. After it the work
divides three ways and only one part is large. *Batchable*: anything with one
invocation per process or per claim --- a `--selftest` and an `--aa` apiece,
the dozen-odd `--pair` lines, a `--block` per class --- goes in one call per
kind, so steps 1 and 3 together are a handful. *One per site*: the eleven
`--in-place` installs, three calls. *Unbatchable*: the prose, one edit per
paragraph, and this is the bulk --- the eight class blocks alone are some thirty
items, and no tool reduces the count, `--block`'s skeletons only removing
the extraction that used to precede each. Then verification costs about what
the prose cost, because every finding is a fix and every fix is a claim ---
and on Run 19 it cost rather more, two checker passes returning 22 defects whose
fixes then wanted their own re-derivation. **Budget the run file's head,
the verification and the eight class paragraphs as the work**, in that order;
the readings are noise beside them, and the run itself is unattended. Two
further consequences worth having in mind before starting. Prefer analysis
that localises --- per shape, per control --- over re-quoting figures that moved
a few percent and changed nothing; the first is where the surprises have come
from and the second is what has gone stale twice.

**A probe is not a lesser instrument than a major run, and the write-up is where
the instruments get built.**, which is the sharper form of the same point. Run
13's registered question came back a null, and its durable output was four
instruments: two checks in the reader and two rules in this chapter, every one
of them from a mistake made while writing up rather than from anything the run
measured. So the write-up is an instrument-building phase and not only
a reporting one, and the four things worth watching for are the computation you
improvised, the check that would have caught the error, the step you skipped,
and the capability you found --- that set is the run's other product,
and it outlives the figures, which the next run replaces.

**Write a capability as a capability.** A fact recorded as a tool's limitation
goes inert: this README said `run-major.sh` cannot give one binary two RTS
configurations, which is true, and two runs each built a second binary and paid
a forty-minute gate to price a nursery that `+RTS -A` sets on the binary already
built. The same fact written as *any nursery question is answerable
on an already-built binary; only a recorded run needs the driver* would have
retired both pairs. So when a limitation is found, write down what it still
leaves possible, in the place a session looks before spending. On the original
point: the measurements that closed the `sum-only` objection, established
that the forcing term scales, and settled the floor's mechanism cost twenty
minutes and, for the latter two, no extra machine time at all, while the major
run they hang off changed no decision. A question with a discriminating
measurement usually deserves a filtered run now rather than a slot in the next
full one.

**Where.** A session starts in `~/r/horde-ad`, which leaves *that* repository's
`CLAUDE.md` resident while this repo is not governed by it, even though all
generalizable preferences apply; read this file and `read-run.py`'s docstring
instead, orthotope carrying no `CLAUDE.md` of its own. Then:

    cd ~/r/orthotope/micro-regime3

**The run's two variables come first**, because everything below uses them
and a shell that has not set them will silently do the wrong thing: an empty
`$REGIME` is a -O1 build that every gate here passes. It reaches the *build*
and nothing else --- no check mode takes a regime, and
on the confirm-don't-rebuild path nothing consumes it at all.

    R=run10                              # names every artifact; no default
    REGIME=-fspec-constr                 # every run since Run 8; empty for -O1
    #  and the pair's halves are $R-<basis> and $R-<other> throughout, here
    #  as in the checklist: which is which is what the pair note records and
    #  what no half's name tells you, so no command below spells one out

**And in a session they will not survive to the next command.** Each tool call
gets a fresh shell, so a `cd` and an assignment made in one are gone
by the next, and the commands below are spread over a dozen of them --- which
is to say the shell this warning is about is the ordinary one here,
not a careless one. Inline the two literals into every command, or re-set them
at the head of each:
`cd ~/r/orthotope/micro-regime3 && R=run10 REGIME=-fspec-constr && ...`. The two
do not fail alike: `./run-major.sh $R` with `$R` empty is loud, the driver
refusing without a name, where an empty `$REGIME` is the silent case
the paragraph above describes.

`$REGIME` is the bare GHC flag and not a `--ghc-options=` spelling of it,
because a recipe composes it with a `-pgma` of its own and each wants
an `--ghc-options=` of its own. Its value begins with a dash, so it goes inside
the quotes --- `--ghc-options="$REGIME"` --- and never as a bare word after
a space, which the option's parser reads as the next flag.

**Then build what will actually be timed --- but first, is there a pair here
already?** That is the fork, and it comes before the build rather than after it,
because a rebuild replaces both halves: the offsets the predictions
are registered against are the present pair's, and one coming out even slightly
different would retire them in silence. Where the binaries and the note
recording what they were built from are already there, confirm them instead
of rebuilding.

The fork's five questions and their commands are in the list; what the list
cannot carry is why the third one usually answers *yes*. **Expect `Main.hs`
to have moved, and read the diff before believing it**: step 8 below sends
the write-up into that file's comments and forbids rebuilding for it,
so a comment-only move is the expected state after any run whose write-up went
there, and only `git diff` tells that from a real one. The regime is the fourth
question and is not answerable from git at all, the JSON recording no compiler
flag --- the `diag` step is what answers it. The shim is the fifth, and
is the one the fork used to miss.

**The preparation may be any age, and the fork is where a later session
re-enters.** Nothing in it wants a quiet machine, so it is legitimately
an afternoon days before the evening --- and a session picking one up runs steps
1 to 3, finds a pair and a note, and takes the CONFIRM path, which is what
that path is for. What a stale preparation never owes again is the three
that cost machine time: the gate, the smoke sweep and the roster pass belong
to the pair and survive, which is why they are recorded in the note rather
than in a session. What it does owe is `--lint` and `--check-doc`, the README
having moved under it, and the cheap read-only steps with them --- 4 to 10
are seconds each, and 9 is the whole regime guard on a path with no build
to have carried it, so re-running them costs less than deciding not to.
The exception is the roster pass, whose own note line records it being re-taken
the same day for exactly this reason --- a pass belongs to the roster
it was taken on, and a roster that moved since voids it.

**And before any of that, the previous run has to be finished.** Nothing
in this list asks, and starting on top of a half-written write-up is a wrong
start no later step catches: the artifacts of a run whose step 12 was never
reached look exactly like those of one whose deletion offer was declined.
The evidence is on the disk and in the open list --- `runs/` already carries
a file for your run, and the open list carries its registration.

Only where there is no pair, or where `Main.hs` or the regime has moved since
the note was written, is a build the thing to do --- and there is nothing here
that does it. Every pair since Run 11 is two shims, and each half is one
`cabal build` from the recipe its note carries: the regime, a `-pgma` shim
of its own, whatever variable the pair exists to price, and `-fforce-recomp`
with a fresh `--builddir` --- without which a shim change comes to be measured
against itself, which is what step 3b's *Up to date* warning is about. Write
the note first, since it is the only copy of both recipes, and read the pair
afterwards:

    ./loop-offsets.py $R-<other> $R-<basis>
    ./loop-offsets.py --library $R-<basis> $R-<other>

The second is the one a two-shim pair cannot take on trust. No `-pgma` shim
reaches a library, so a library loop that moved was displaced by a change
in `.text`'s size, and a pair that moves them prices that displacement along
with whatever it meant to price.

So the confirm path is the three fork questions above and the note's own
recorded verification, and nothing else.

There is no single-binary form of a major run any more, the pairing being
permanent: `run-major.sh` and `run-gate.sh` both refuse to start without both
halves, so a lone binary has no driver. What
`cabal build micro ${REGIME:+--ghc-options=$REGIME}` is still for is a probe ---
a filtered handful of benches answering one question --- and those are run
with `cabal run micro ${REGIME:+--ghc-options=$REGIME} --`, never through
the sequence below.

**Before spending the hours**, the cheap checks --- the first three against
the binaries that will be timed, not a third built beside them, and the last two
against `Main.hs` and this file, which open no binary at all:

    ./$R-<basis> check > /tmp/a.log 2>&1   # every strategy agrees, every
    ./$R-<other> check > /tmp/b.log 2>&1   #   shape regime 3, both halves
    cmp /tmp/a.log /tmp/b.log              # and the two logs are identical
    #  scratch names, not $R-*.log: run-major.sh refuses to start where one
    #  of those exists, so a log named for the run blocks the run
    ./$R-<basis> --list 2>/dev/null | wc -l    # 2>/dev/null is NOT
                                 #   optional:
                                 #   the provenance line goes to stderr and
                                 #   interleaves inside a bench name without it
    ./read-run.py --lint         # the roster and the shape annotations
    ./read-run.py --check-doc    # anchors, coverage, widths, stale figures

**What the `note:` lines ARE, the list having said only that they do not stop
you.** They are the write-up's adjudication material and nothing a preparation
owes: every superseded figure, every superlative, every absolute time the two
documents quote, and every link from standing prose into the run's file
as a whole. `--quiet` withholds them by count, which is why every call carries
it but post-run step 7's; **`--worklists` is what promotes them** there,
and not the absence of `--quiet`, which withholds too. `--lint` reads the same
way, noting the rostered arms it knows are deliberately untimed. **One
of those `ok:` lines is the wrap check, and it reads differently mid-edit.**
It asks its question per paragraph rather than of the whole file, so a paragraph
an edit left on one line is reported as mid-edit and not failed, and a `FAIL:`
there means a paragraph wrapped by *hand* --- neither the formatter's form
nor one line. The gate therefore stays green on a document being worked on,
which is what stops it demanding a `wrap80 -i` between edits: wrapping is owed
before committing, not before checking.

Both halves. On the unaligned/aligned pairs this README used to build, only one
half had its own code rewritten --- the other's shim appended dead bytes, where
`align-as.py` moves labels about --- but on a pair of two shims, which every
pair since Run 11 has been, both can be mispadded and both need it, so checking
both is the rule and the one-sided case is the exception that no longer arises.
The halves are held to each other besides --- a sound pair makes the two logs
byte-identical, agreement on every shape being a property of the strategies
and not of where their loops landed. A difference stops the run, and the rebuild
goes through the recipe in that pair's note. The two lines above cost seconds.

**Then confirm the regime is the one intended**, which nothing later can:

    ./$R-<basis> diag

and read one row of it --- the allocated bytes of `baseOffsetsScan` against
`baseOffsetsMut` on `vgg-14-c512`, which is a `diag` label rather than a shape
and so will not be found in the shape set. They are equal to three figures
under SpecConstr and ten times apart at plain -O1, a separation no eye misreads,
and both ends of it are measured (2026-08-08), the flag being the only thing
that moves them. Seconds either way --- on the build path, the seconds after
a rebuild the flag forces anyway; on the confirm path, its own, and the only
ones spent there that matter, since with no build to carry the regime
this is the only check standing between a mistyped regime and a run that refutes
the design it was built to test.

**A paired run adds a second binary, and both are built and checked before
either is timed.** Alignment is not a regime flag: it arrives on `-pgma`, GHC
notices neither that nor `-fproc-alignment`, and a rebuild between the two
halves would put back the very effect the pairing measures. That is why the two
halves are built one after the other from the note's recipes, with nothing
touched in between, and why both executables are kept.

`check` is the gate and the offsets are not, a wrongly padded binary having
correct-looking offsets and wrong answers. Read both listings anyway: what each
half's fills are, since a prediction made per arm is made from them and no later
binary has them. **Whether any short loop of a half's own code straddles
is the build path's to read and the note's to keep**, `--survey` being one
binary at a time and the answer a property of the pair rather than
of the session confirming it --- offsets at 0 are what a fully padded half shows
and not a thing to require of a max-skip one, which leaves a resident loop where
it fell; `--survey` is the length-agnostic form and takes one binary at a time
(`./loop-offsets.py --survey $R-<basis>`), and what "every timed arm's loop"
means is bounded by what can be attributed at all. The sequence below runs each
half in turn, and `run-major.sh` does it for you; what neither can do
is interleave two processes of this size within a population, so the order they
ran in is written down and is one of the two things left uncontrolled.

**The other was that the halves differed by more than Main's alignment,
and that one is fixed.** Aligning grows `.text` by 12 KB, so everything linked
after it moves: in the first pair built here, of 867 library symbols carrying
a short loop, 856 sat at a different address and `vector`'s straddling short
loops went from 36 to 40. The shim reaches only what GHC compiles here,
so those loops were rerolled rather than aligned, and an arm whose innermost
work is in library code would have carried a term the pairing scrambled instead
of removing --- which is not hypothetical, `list`'s own loop being library code
(prediction 5). Padding the unaligned half to the same size *and phase* closed
it: 95% of the library loops at the same cache-line offset and 98% in the same
straddle state, the rest of the delta being 384 bytes, six whole lines. Matching
the size alone does not do it --- that left the delta at 416, which is 32 mod 64
and so the worst shift available --- and the two-step that does
is in `align-as.py`'s docstring, beside the `PAD_BYTES` it feeds. **A pair
of two shims has no such step and no such guarantee**, only whatever its two
recipes give it, which is why `./loop-offsets.py --library` exists: it reports
what share of the library self-loops the two halves put at the same offset
in their line, and near-total agreement is what a pair built from ONE SOURCE
looks like; halves that differ in source move it wholesale, which
is a registered variable rather than a verdict. A note may record the same
property the other way round, off `nm` symbol by symbol, which is the stronger
reading and not this tool's output --- so compare like with like, or read
the note's own figure as the note's. So the pair now differs in Main's loop
alignment and in nothing else an offset can see, and `micro-unaligned` keeps
every offset the unpadded build had: the same fills at [3, 53, 59, 45] and [16,
0, 36, 36], the same 115 short loops with 50 straddling.

**Which two halves a pair has is a property of the pair, not of this README ---
but how they are named is not.** A half is `$R-<tag>`, the tag naming what
that half *is* rather than which role it holds: `run13-maxskip`
and `run13-lookrts`, `run14-lookrts` and `run14-a1g`. So a new pair derives
its own names before it has a note to read them from, and step 0's rule stands
untouched, the tag saying what a half is and the note saying which of them
is the basis. The names are recorded in the pair note and set in one place
in each of the four scripts that take a run --- `run-major.sh`, `run-gate.sh`,
`smoke-sweep.sh` and `install-tables.sh`, the last carrying `BASIS` alone ---
as `OTHER` and `BASIS`, and each is a `${BASIS:-...}` default an environment
variable overrides for an older pair; the basis is the half the expected bench
counts are read from and every table is installed from, and it runs second; both
halves run every class. **The two roles are BASIS and CONTROL**, which is what
this README calls them where it names a role at all; the scripts' variable
is `OTHER` and the prose often says *the other half*, and all three are one
thing. The halves are named for what they vary --- Run 10's
`unaligned`/`aligned`, Run 11's `maxskip`/`aligned`, Run 12's
`maxskip`/`maxskippa` --- and which of them is the basis is a decision the pair
note records, not something a half's name tells you. Run 12 is where the two
would collide if this README still called the basis *the aligned half*:
its control is `maxskippa`, the half that carries `-fproc-alignment=64`
and so is the more aligned build of the two. Where a sentence below says
*aligned* it is about alignment, not about a role; where it is plainly about one
past pair --- as the paragraph on the 12 KB of `.text` is, every figure
in it being Run 10's --- it keeps that pair's half names.

**Name the artifacts by half, and drive every `--in-place` from the basis
half.** The sequence below builds every filename off `$R`, which a paired run
has to split: one `$R-<half>-main.json` per half, and the class files
`$R-<basis>-$c.json`, there being no others --- the infix being the binary's own
name, so an artifact cannot be traced to the wrong half. **One scheme covers
everything a run leaves**, the binaries and the pair note with the JSONs:
`$R-<rest>`, the run first and nothing before it, which is what stops two runs
writing one filename. Binaries from Run 11 and earlier were named for the half
alone (`micro-aligned`, `micro-unaligned`), which is what this README's history
calls them. The README carries one basis and not one per half, and what
the other half contributes is the `--compare` and a yardstick column. Run 10
is the one run that answered otherwise, its Results table coming
from the unaligned half while its fingerprint and its class blocks came
from the aligned one --- a split it needed because its aligned half
was the first here and had no predecessor to succeed. That ended with Run 11:
**the basis half is the table and the other half is the control**, whatever
the control is built to price.

**What the other half is for**, since a run that publishes no table from it will
otherwise be asked why it spends an hour building and timing it. That depends
on which half it is, and the pair is chosen for it. An *unaligned* control
is the layout one, the per-arm term being measured afresh each run rather
than inherited, and it is the yardstick for GHC itself: the native backend
aligns no loop today ([the floor section][floor]), and when that is fixed
the same pairing is what prices how well GHC does it against the assembler shim
here --- a comparison no single build can make. Run 11's *max-skip* counterpart
prices the shim's own padding instead, its two halves differing in which loop
heads get a directive and in nothing else, so its arms separate what alignment
buys from what the NOPs cost.

**The pairing doubles the classes too.** Both halves run the main set, since
that is where the per-arm comparison lives, and both now run every class
as well. The rule it replaces ran the eight class populations on the basis
alone, on the argument that a class block is read for the ordering inside
its own population and the basis is where that ordering is legible --- true,
and beside the point the moment a pair's variable can act on a class and
not on the main set. Run 14 is that moment: it varies the allocation area,
and the classes hold the shapes whose excess allocation crosses the nursery,
so a class read on one half only cannot say whether the variable touched it.
The old rule was standing rather than a concession, which is exactly why
it would not have been noticed in time; what replaces it is standing too, paid
every run so that no run has to see its own need coming. The cost is one more
process per class, which was never the reason for the exception and is
not the reason against it.

**And one more, nearly free**, because everything above exercises
the *benchmark* while nothing exercises the *reader* until hours later ---
at `-L1`, since the smoke tests the reader's code paths, not its statistics:

    ./smoke-sweep.sh $R

It runs three `-L1` processes --- one main-set shape from each half and one
shape of a class from the basis, that being what holds every process to one
shape's arm count --- then every reader mode over what they wrote,
then the `--in-place` installers into a copy of this file, and deletes all
of it. Minutes, on a machine doing nothing else. It uses binaries already built
rather than `cabal run`, which would build a third in whatever regime the shell
happens to carry; it exercises the reader rather than the regime either way.
**It is a driver, for the reason `run-major.sh` is one:** it counts, holding
each process to the arm count `--list` gives for that shape. The reason
it is not *also* still printed here is the one this README learned the hard way
the same day --- a pasted copy of a driver's sequence drifts from the driver
and nothing checks it, which is what the class loop above had done.

**What this proves and what it does not**, since it reads like a verification
of the installs and is not one: it proves each *table* installer found its table
and wrote something, and `cmp` fails loudly if the copy came out identical,
which is the case where one silently found nothing. The claims installer
is the exception and is checked the other way round: the claims are registered
over the whole main set and a smoke run is one shape of it, so the install must
REFUSE, and a zero exit there is the failure. It does not prove the right rows
went to the right place --- that guarantee lives in `install`, which matches
by whole line, an indented copy of a header being unable to satisfy it,
and asserts the row count rather than assuming it. That is where the Run 8
mis-paste is made impossible rather than merely detectable, and it is born
checked four ways; the smoke exercises the path, it does not re-derive
the guarantee.

`--in-place` earns its own block because it is the one mode that writes: pointed
at `README.md` it would install a one-shape smoke table over the published one,
so the copy is the point, and `cmp` afterwards is what keeps the check
from passing on an installer that found nothing and said nothing. Run the copy's
own diff by eye if a table looks wrong; the copy is deleted with the rest.
**Each install is smoked from the half it will really come from** --- every one
from the basis half, `--markdown`, `--fingerprint` and `--claims` off
the main-set JSON and `--block` off the class one --- which is why
these are spelled out and not looped. The write-up is hours too late to find
a broken installer.

The first runs every timed arm on one shape and puts the whole analysis path ---
the correction, the controls, the table generator --- through its paces;
the third does the same for the `classes` plumbing, the reader's per-list shape
rules and the six-column class table, on the class whose rule is least trivial.
Those two go through every single-file mode a class JSON can take,
and the main-set one takes `--claims` besides, the claims being the main set's;
the lines after them add the modifiers a write-up reaches for --- `--brief`
on `--aa` and `--block`, and the filters `--no-controls`, `--exclude`
and `--exclude-shape` --- because a mode that passes bare can still die
under the flag it is really given. A reader broken by a roster or shape-list
change fails here in minutes instead of after the run.

The second file exists for `--compare`, which no single file can reach:
it is the reader's only two-run mode and the one a paired run is read with,
so leaving it out of the sweep would leave the pairing's own instrument untested
until the write-up. It is also the only point before the evening at which
the *other* half writes a JSON at all --- the basis half writes the first file
--- and a pair whose halves turn out not to be comparable has cost the hours
twice.

**Run every mode, not the interesting ones.** The loop above is written
as a loop because a partial sweep has already missed a real break: after
the trim came out, `--pair` and `--aa` both died on a name that a removal had
taken with it, while `check`, `--lint`, `--check-doc` and `--selftest` all
passed --- the failure lived in the two modes nobody had thought to run. Modes
are cheap to run and expensive to be missing, and the run artifact is the only
thing that can reproduce one, so sweep before deleting it rather than after.

**After a roster change, add a `-L1` pass over the main set and one three-shape
class**, which is about twenty minutes and reaches three things a one-shape
smoke cannot. `--selftest` skips a whole block on one shape and says so ---
winsorizing, the A/A identities and the baseline identity, none of which
is an identity of anything until there are shapes to be one over. Every claim's
`--pair` line goes unrun, and a claim re-aimed at an arm the run does not carry
fails only when someone runs it. And `--block`'s per-shape line is guarded
by `len(shapes) > 2`, so it is dead on a one-shape file --- a guard that hid
an edited line of this reader through a whole smoke sweep. Every class
is three-shape since 2026-08-14, so any of them serves; the list above prefers
one of the five that crossed from two, which drives `--block`'s three-shape
branch, and `scaled` is the one it names. The pass is two processes:

    ./$R-<basis> -L1 --json smoke-l1-main.json
    ./$R-<basis> classes scaled- -L1 --json smoke-l1-scaled.json

Its numbers go nowhere: `-L1` is a rougher budget than any recorded run's,
and this pass is a test of the reader, not a measurement. It is recorded
on an `L1 ROSTER PASS:` line, and a second session owes the twenty minutes only
if none is there. **Name its artifacts `smoke*` and not `$R-*`**, which
is not tidiness but the relaunch guard step 12 names: a `$R-l1-main.json` left
beside the pair refuses the very run this pass was run to clear. `smoke*.json`
is outside that glob and inside `.gitignore` already. The relaunch guard
is the smaller half of the reason and this step's own; the general rule, wider
than any step and quieter when broken, is [above](#making-a-major-benchmark-run)
--- no probe of any kind takes the run's prefix.

**"Roster change" here means membership, and the test is `--list`**:
the binary's listing differs from what the previous run's did, in its set
of names rather than their order. Criterion emits it sorted, so an arm moving
slot cannot produce a false positive --- which is the only thing making the test
sound and is worth knowing, since order *is* a change, of the kind
[Provenance](#provenance) deals with rather than this pass. An edit
to the reader or to a claim is not a roster change either, though the three
reasons above are worded in their terms because a roster change is the only
thing that has ever broken them. What the test cannot usually do is run itself:
the previous run's binary is deleted and its listing recorded nowhere,
so the comparison is against the roster delta under [Provenance](#provenance)
--- look before taking that route, since a pair whose artifacts have
not been offered for deletion yet is still on disk and answers directly, which
is kept for exactly this. A run whose basis half *is* the previous run's binary,
as Run 11's is, answers it outright instead, and the pair note records the count
on both sides. Spelled out because two readings of this paragraph have split
on it: with membership unmoved the pass is not owed however much else changed,
and Run 10 is such a run.

**A paired run has one gate more, and the first thing to do about it is read
rather than run it. The gate belongs to the pair, not to the session**, which
is what stops it being paid for twice. A pair's note, `$R-pair.txt`, is written
by hand beside the binaries --- every name in this directory carries the run,
so that two runs cannot write one filename however alike their half names
are --- and it carries both recipes, what was verified, and a `GATE:` line
saying it has not been run; `run-gate.sh` appends to that file. So read what
the note says about the gate first --- `grep -i gate $R-pair.txt`, this pair's
note and not every note in the directory, case-insensitive and not anchored
on the `GATE:` token, because a note written by hand says it in prose
and grepping for the token finds nothing in one, which reads as *no gate*
and costs the hour it was meant to save. **Read the whole output and
not its last line, and the newest `GATE:` line is not the verdict**:
`run-gate.sh` appends its mechanical block last and closes by asking
for a reading, so on every gated pair the newest `GATE:` line is the script's
and says the reading is still to do, while the verdict --- written by hand,
above it --- is the older one. Read up the output until a `GATE:` line states
an outcome; that is the verdict, whatever sits below it. Following *newest wins*
here costs the forty minutes the step exists to save, which is how it was found.
If a verdict records a pass, this step is already done and the next action
is the run itself. A rebuild that comes out md5-identical inherits the gate,
and one that does not --- a changed `Main.hs`, a changed regime --- needs
its own. Re-running it on a pair that has already passed costs a quiet forty
minutes and can only reproduce what the note says.

**If that line says the gate has not run**, it is the last thing before
the evening --- but it is not part of the preparation, and *get the run ready*
does not license it. The gate spends forty minutes of quiet machine, so it lives
in the run list behind the go-ahead with the sequence itself. `run-gate.sh`
takes five benches over the shape set from each half, twice each,
in a palindrome --- control, basis, basis, control --- so that drift
over the hour cannot read as a difference between the binaries, which
is the part a person retyping the command would drop:

    ./run-gate.sh $R
    ./read-run.py $R-gate-<basis>-a.json \
      --compare $R-gate-<other>-a.json
    ./read-run.py $R-gate-<basis>-b.json \
      --compare $R-gate-<other>-b.json

**Both passes are read, which is what the palindrome is for**: the `a` pair puts
the two halves next to each other early and the `b` pair does it late,
so a verdict is the two readings agreeing rather than one of them taken
at a moment. It wants the same quiet the run does and costs about forty minutes,
so it is not one of the cheap checks above; what it buys is finding out
that the basis binary is wrong before an hour of main set is spent on it. **What
it does not buy is a first reading of the arms the pairing is predicted on**,
which this README claimed until a run measured it. Its selection carries `build`
and `mut-odo`, which are two of the three widest-spread arms in the roster ---
the placement-sensitive pair [the floor section][floor] is written about ---
so the term between its two passes runs past the drift band a movement is asked
to clear, and a magnitude read off a gate is not evidence. Whether a five-bench
process is *also* noisier than a full one is not separable from this with one
process per binary, so the reason to distrust the figure is the selection, which
is known. And the two passes disagreeing is not a second opinion about
the binaries: their ratio is algebraically the ratio of the two same-binary
readings, so a palindrome that fails to converge is reporting its own noise.
Read the gate for soundness, and take every magnitude off the run. What
the script writes back into the note is the mechanical half alone --- four exit
codes and four bench counts --- because that is what it knows; whether the pair
is sound is the reading's verdict and is written there by hand --- **above**
the script's block, where reading up from the end meets it first,
and the `GATE: not yet run` line goes in the same edit, since a reader reading
up would otherwise meet that one and stop. What the predictions are is in [the
open list](#what-is-open) with the rest of the run's registrations; what
the gate read is in the note, written by hand above the script's mechanical
block. **The gate also answers one question that is not a reading at all: has
the machine changed?** `run-gate.sh` runs
`./read-run.py $R-gate-<basis>-a.json --machine` after its four processes
and puts the answer in the note. It holds `list`'s net per call, shape by shape,
to the fingerprint the last run's file keeps, so its absolutes are in `runs/`
long after its JSONs are offered for deletion and nothing has to be kept for it;
the gate's own selection carries `*/list` and both `sum-only` halves on every
shape, which is what makes the comparison net against net. It reads the geomean
rather than a cell, at a threshold the mode's own docstring derives from every
kept process this README has, and beside it the per-shape residual about
that geomean, which says whether the shapes moved together: inside the band
a single shape ordinarily wanders it is a LEVEL SHIFT, one number describing
the box, and every cross-run ordering survives it; outside, the orderings
are in question along with the level. **Neither stops the run, at any size,
in either direction.** A box that moved between runs cannot reach a within-run
comparison, and every claim here is one; what it reaches is the cross-run
absolute column, which re-baselines by itself, each write-up replacing
the fingerprint it reads. So a move is recorded and the evening proceeds,
the write-up owing a paragraph naming it and the box question going to a person
once the machine is free: **ask whether the box changed** --- a kernel,
a microcode update, a BIOS setting, a thermal state, a different machine ---
none of which a run can see from inside itself, and none worth a night of idle
machine to ask. **Run 18 is why that is written down**: its gate stopped on what
the reading above calls a level shift, and the evening was spent waiting
for the answer *run anyway and re-baseline*, which was never in doubt. What
still fails the gate is a comparison the mode cannot make at all --- no shape
of this run in the fingerprint, every `list` net non-positive.

**The run** is one sequence --- the main set from each binary the run has,
then each stride-class population in its own process, in `classViews`' order.
Each `$c-` argument selects a class by name prefix, the prefixes being disjoint
by construction (`bcast-` does not match `bcastmid-*`); one process per
population is the recorded protocol at `classBenches`, so no population's
figures owe anything to another's leftover heap state and each JSON
is single-population by construction. **The regime is a variable
of the procedure, not a flag to remember**: it is set once at the top beside
the run's name and goes to each half's build, so that leaving it empty
is a deliberate act rather than an omission. On a path that skipped the build
the whole guard is the `diag` reading above, which is why that step
is not optional there. A run made in the wrong regime is not detectably wrong
--- the roster, the shapes, the gates and the reader all pass, the JSON records
no compiler flag, and the only symptom is the regime's own effect failing
to appear, which reads as a refutation of the design rather than as a missing
flag:

    # $R and $REGIME are already set, at the top of this procedure. Anything
    # added to REGIME that carries a VALUE -- -fllvm, -pgma and the alignment
    # shim, an inliner threshold -- wants -fforce-recomp or a fresh
    # --builddir beside it, or the run measures the previous binary and says
    # nothing. Toggling -fspec-constr itself is safe: GHC notices that one,
    # and it is the control that proved the rest are missed. The floor
    # section, under what moves a figure when no strategy changed, has why.
    # These two are what the run records about its own provenance, and the
    # driver below already runs both -- they are here to say what belongs in
    # the log, not to be typed when run-major.sh is what launches the run.
    git log -1 --format=%h && git status --porcelain  # the write-up's commit
    uptime                                # quiet, or note what was not

**`run-major.sh` is that sequence as a driver**, and `$R` is its argument rather
than a variable it inherits:

    ./run-major.sh $R          # many processes, unattended, several hours

It refuses without one, the prefix being the run's identity: artifacts called
`run-*` would not say which run made them and the next run would overwrite them.
**It also refuses to start where that name already has artifacts, which makes
an interrupted sequence a hand job --- expect that, since the machine gets
wanted back.** The guard is right (relaunching overwrites hours in place),
but it has no resume, so finishing a sequence whose main sets landed and whose
classes did not means running the class loop yourself: the `for c in ...` half
of the sequence above, both halves inside it,
an `[ -e "$out.json" ] && continue` before each so a population that already ran
is skipped rather than redone, and its `benchmarking` count checked against
`classes --list` as the driver does. Stamp each into the same
`$R-wallclock.log`, so the run's own record stays one file, and say
in the write-up that the populations ran in more than one window --- one process
per population is what makes that harmless, each carrying its own controls
and gates, but it is a fact about the run and the run file states it.

What it adds over pasting the sequence is the counting: every process's bench
count is checked against what the roster holds, so a selection that silently
caught the wrong set is loud in the log at once instead of at the write-up ---
loud rather than fatal: the sequence carries on to the next process, there being
no reading in which eight sound populations are worth discarding for one
that is not, so the wall-clock log is what has to be read before any figure is,
and the exit status carries out the count of them, a sequence launched with `&`
being read by whatever collected it. The expected count is read
from the binary's own `--list` rather than written down, because a literal would
be wrong for the next roster and would turn a correct run into an alarm on every
process; `run-gate.sh` derives its own the same way, and a class process's
is its prefix's share of `classes --list`, a prefix matching nothing being
reported rather than run as a process of no benches. The class list itself
is the literal that remains, so the drift the other way --- a class the binary
has that `CLASSES` does not name --- is refused before the run rather
than reported during it: it would otherwise run nowhere, print nothing and leave
no artifact, which is measured and not feared. Neither builds anything, and both
refuse to start without the pair. The sequence:

    {
      date -Is
      # A paired run: both halves take the main set and both take every
      # class, and each half is its own binary -- never rebuild between
      # them. $OTHER and $BASIS are the pair's, set in run-major.sh.
      for h in $OTHER $BASIS; do
        ./$R-$h --json $R-$h-main.json > $R-$h-main.log 2>&1
        echo "$h main exit=$? $(date -Is)"
      done
      for c in rev revsome bcast bcastmid reshape1 slice window scaled; do
        for h in $OTHER $BASIS; do    # adjacent, control then basis
          ./$R-$h classes $c- --json $R-$h-$c.json > $R-$h-$c.log 2>&1
          echo "$h $c exit=$? $(date -Is)"
        done
      done
    } >> $R-wallclock.log 2>&1

**The files that leaves**, spelled out because deriving them from the loop
is a step every reader has had to take in the script instead:

    $R-<other>-main.json        $R-<basis>-main.json
    $R-<other>-rev.json         $R-<basis>-rev.json
    $R-<other>-revsome.json     $R-<basis>-revsome.json
    $R-<other>-bcast.json       $R-<basis>-bcast.json
    $R-<other>-bcastmid.json    $R-<basis>-bcastmid.json
    $R-<other>-reshape1.json    $R-<basis>-reshape1.json
    $R-<other>-slice.json       $R-<basis>-slice.json
    $R-<other>-window.json      $R-<basis>-window.json
    $R-<other>-scaled.json      $R-<basis>-scaled.json

each with a `.log` beside it, and `$R-wallclock.log` over them all. The gate's
own `$R-gate-*` files are not among them and are excluded from the relaunch
guard for that reason.

Everything else is already a default. The allocation fit
`--regress allocated:iters` is on (it is well-conditioned at 5s), so `alloc`
comes out of the same process as the times rather than a side run; passing
`--regress` explicitly would replace it. Each process prints its own provenance
to stderr as it finishes --- roster size, shape count, wall clock and the two
heap peaks --- so a document quoting its scale copies a measured number rather
than counting benches by hand, and so `micro.cabal`'s `-M8G` headroom claim has
a current source; the stderr redirect above is what keeps it. In a class process
every part of that line is its own but the shape count, which is fixed before
criterion selects and so names the whole class set.

**Check what a filtered selection actually selected.** Criterion takes one
`-m MODE` and then its patterns positionally, so `-m glob A -m glob B` matches
*nothing* and the process exits at once --- which looks exactly like a fast run
and cost one probe here before the zero timings gave it away. Count
the `benchmarking` lines against what was asked for before reading any number
out of a filtered run; it is the prove-a-search-non-vacuous rule applied
to bench selection, and the same count catches a pattern that silently caught
more arms than intended. The sequence's own processes have this done for them
by `run-major.sh`, class ones included; what is left to the runner is every
filtered probe made by hand, which is where the rule was learned and where
nothing counts on its behalf.

**Probes whose designs predate the run ride the same script.** The machine
is quiet for the whole sequence either way, so a question already on [the open
list](#what-is-open) with its measurement written --- a twin in a named slot,
a filtered A/B --- is appended after the classes and answered the same day,
pre-registered rather than improvised. What this does not cover is the run's own
surprises, which need the run read first; those become that list's next entries,
each with the probe that would settle it.

**The time budget is always criterion's default.** Raising `-L` would buy
samples for the slowest shapes --- they bottom out around 6 where the fastest
get 130 --- but at a proportional cost in wall clock, and the runs are already
hours. Every recorded run therefore uses the default, so figures stay comparable
between runs and the sample counts in the tables mean the same thing throughout.
Where that leaves a shape thinly measured, the `smp` and `CI%` columns say
so rather than the budget hiding it.

Expect several hours for the sequence, so run it in the background --- and **run
nothing else on this machine while it does**. Unsandboxed, and confirmed
from a process list rather than from the launching shell, which a blocked write
leaves lying:

    ./run-major.sh $R &               # its own wall-clock log is the record
    ps -eo pid,etime,comm | grep $R-  # comm, NOT args, as at step 16

Every strategy of a population shares that population's process precisely
so its figures are commensurable, and the [noise floor][floor] section
is the measured evidence that they move with what shares that process. What
the rest of the machine does on top of that is unmeasured, and a recorded run
is the wrong place to find out. The session's own hands stay off the machine
and the tree alike until the sequence ends --- the script's git lines
are the binary's provenance, and an edit under a running sequence falsifies them
--- while reading ahead costs nothing: the last run's own file and the open list
are what the write-up is about to need.

The wall-clock file is why the script stamps each process: a criterion log
is timestamped only at the end, so without the window there is no way to say
which shapes an intrusion exposed, and a suspicious cell can then be neither
blamed on it nor cleared of it. The exit codes ride along because a class
process that dies mid-sequence otherwise leaves a truncated JSON behind a green
scroll-back. Run 6 (-O1) had three short greps in its first minutes
and the exposure was settled from the cell data instead --- the anomalies
were strategy-intrinsic, not a time window
([R2](#r2-is-the-ramp-detector-not-the-noise-detector)) --- but that worked only
because the suspects sat at one roster slot on two shapes, which is luck
and not a method.

**The run's registered predictions** ([the open list][open]) say what this run
was for and what would kill each one, and are read while the sequence is still
ahead of you --- checklist step 15, which is where their reading is placed.
Record their verdicts there rather than in the run's own chapter, which the next
run replaces. **An empty registration does not hold the run.** Where a run has
none, note the absence and read the outcome against its queue entry instead.
What is not open is registering afterwards: the point of the list is
that it predates the hours, so the choice here is to register before the evening
or to do without. **Each registration is written with an empty `verdict:` slot
beneath it**, so the write-up fills a form rather than composing one and a count
of what held is read off the list rather than tallied from memory --- which
is how Run 18 came to summarise five registrations in its lead before it had
adjudicated the fifth. **And a verdict is written in a fixed vocabulary, because
a checker reads it**: `--check-doc` holds a registration's marker to its items
--- numbered `1.` at the start of a line, Run 17's form, or `(N)` inline before
an italic label, Run 18's, a number's spans grouped so that stating a question
and later adjudicating it under one number reads as one item --- so an `OPEN`
entry whose every item is adjudicated is reported as a stale marker
and an `ANSWERED` one with an item that is not is reported as an incomplete
adjudication. What it recognises is a **bolded span whose first sixty characters
carry one of** ANSWERED, REFUTED, HELD, BROKE, BROKEN, FAILED, SPLIT, KILLED,
TAKEN, DELIVERED, PAID, CLEAN, SETTLED, RETIRED, SPENT, UNUSED, NULL
or WITHDRAWN --- both house styles pass, the label-then-verdict
`*The flag's cost.* **KILLED, ...**` and the paragraph-opening
`**The condition was met and the debt is PAID**`. **A verdict written outside
that vocabulary is invisible to the check**, so a new word is added
to `VERDICT_WORDS` in `read-run.py` in the same edit that first uses it,
or the item reads as unadjudicated for ever. Run 12's entry sat `OPEN` for six
runs on an item that said PAID, and the check's own first draft missed
it by keying on capitalisation instead of the word. **And say what a partial
outcome is**: a prediction registered over several arms can come apart,
and neither "held" nor "refuted" is then true --- Run 10's first was stated
over three arms and one confirmed it while two met its own kill condition.
Report that as a split, name which arms went which way, and carry
the consequence for each separately; the temptation is to round it to whichever
answer the majority of arms gives, which loses the finding.

**After it lands**, in this order:

**The post-run half as a list, for the same reason the pre-run half has one.**
Its twelve steps below are the prose's own numbers, so a reference to step 7.7
still lands; the prose is where the reasons live and is not replaced by this.
What it replaces is reading the twelve paragraphs three times to be sure nothing
was missed, which is what they have cost.

    #  DO STEP 11 AS SOON AS THESE GATES PASS, out of order and before
    #      any prose. It is the only step whose window closes -- it spends
    #      the artifacts -- and it is numbered last but one, so it is what
    #      a session that runs out of will loses. On Run 18 it produced
    #      the sharpest finding of the evening, the two add-in arms
    #      swapping cache-line offsets between the compilers, which no
    #      later session could have recovered once the binaries went. The
    #      numbers here are the prose's own and do not move, so this is an
    #      instruction about ORDER and not a renumbering
    ./read-all.sh $R                                  # 1. gate EVERY
    #      process -- both halves of every population, which is eighteen
    #      --selftest and eighteen --aa, and nine is what counting by hand
    #      leaves when it counts populations. A run from before
    #      2026-08-14 has ten, its classes being the basis's alone; the
    #      driver counts what is there, so read it and not this line for
    #      an older run. The driver prints a line
    #      apiece and the A/A WORST CELL beside it. READ that column: it
    #      is not the pair's geomean and the gate is not it either, and it
    #      is the NET ratio, the same quantity as the published floor.
    #      A failed gate invalidates that
    #      population's whole time column and only that one. The published
    #      floor is the NET ratio; the raw one is an arm against itself, and
    #      quoting it as the floor overstates by 1/(1-f). Write this run's
    #      floor into the head of the chapter now: every margin is judged
    #      against it. Read $R-wallclock.log FIRST -- a wrong bench count is
    #      logged loudly and is not fatal, so nothing else stops on it.
    #      On a run carrying the preamble it also gates THE PLATEAU, off
    #      the logs rather than the JSONs: every recorded process's own
    #      @@saturate reading inside 5% of the run's. A process outside
    #      that band measured in a state the others did not, and every
    #      other gate here is WITHIN one process and cannot see it
    ./read-run.py $R-<half>-<pop>.log --wild          # 1b. and, on an
    #      instrumented run, the per-sample stamps that log carries:
    #      allocation, mutator, collector and in-use per bench, and the
    #      foreign CPU during its samples. That last is what tells a WILD
    #      CELL from an external intrusion -- both being a moved mutator
    #      clock at flat RTS totals, and the difference being whether
    #      anything else was running. Reach for it when a cell in step 1's
    #      worst-cell column wants explaining, not on every process
    #  1c. if 1b names an intrusion, RERUN the populations it touched,
    #      BOTH halves of each -- a pair read across two windows is not a
    #      pair, so a clean half is rerun with its exposed twin. About
    #      12m15s a process, which is what one process per population
    #      buys. Two rules, both bought the hard way on Run 18: the rerun
    #      window is quiet FOR THE DRIVER TOO, reading this run's own
    #      logs during it having been enough to void a process; and drive
    #      it through run-major.sh rather than by hand, whose launch line
    #      carries WILDLOG and SATURATE and whose guards catch a process
    #      that lost them -- 141 benches at rc=0 with no stamps in the
    #      log looks perfect and certifies nothing. Park what it
    #      supersedes as probe-*: read-all.sh globs $R-*.log for the
    #      plateau and lists by name any log it finds no reading in,
    #      so a superseded copy left in that namespace fails the gate
    #      -- which is what a driver's own stdout redirected to
    #      $R-install.log did on 2026-08-23
    #   2. match bases before reading any ratio -- same population, same
    #      restriction, the basis the claim was stated on
    ./read-run.py $R-<basis>-main.json --claims       # 3. every claim's
    #      ordering and registered verdict in one call, in the claims
    #      section's own order -- and, after them, the README's own verdict
    #      figures read back against these readings. Give it the BASIS:
    #      the control half lists two dozen figures as unaccounted, which
    #      is what a stale section looks like too
    ./read-run.py $R-<basis>-$c.json --block          #    one per class
    ./read-run.py $R-<basis>-$c.json --compare $R-<other>-$c.json
    #      and one per class ACROSS the halves -- from Run 14 on, a run
    #      before that having no control-half class JSON to compare
    #      against, so these eight are skipped and the chapter says they
    #      were. Which is what running every
    #      class on both is for and what nothing else in this list reads: a
    #      pair's variable can act on a class and not on the main set.
    #      --alloc takes the same pair where allocation is the question
    ./read-run.py $R-<basis>-main.json --compare $R-<other>-main.json --chapter
    ./read-run.py $R-<basis>-main.json --compare $R-<other>-main.json --alloc
    #      --compare takes the BASIS first and the control as its argument,
    #      so below 1 means the basis is faster; reversed, every figure
    #      inverts and nothing in the output says so. Write each class
    #      paragraph from --block's VERDICTS, never from its table, one
    #      paragraph each. Use --brief on --aa and --block: no computed
    #      figure is lost. Do not write a second reader
    #   4. one JSON at a time, never merged; there is no combined figure, so
    #      a sentence comparing populations compares their tables
    #   5. MAKE THE RUN'S OWN FILE, `runs/$R.md`, by copying the last
    #      run's over it: it is the whole of what a run replaces -- head,
    #      Results, what the next run compares against, the claims it
    #      should test, the eight class blocks and its own Provenance --
    #      and every install below writes it and no other document. The
    #      number is in the NAME and in none of that file's SECTIONS, so
    #      the four this step used to rename are TWO: the file's title,
    #      renamed by the copy, and `Recommended tasks after Run N`, which
    #      is the open list's and takes THIS run. Then repoint README's links
    #      from the run before to this file: --check-doc fails any that
    #      still name it, runs/ keeping every run, so a missed one
    #      resolves and renders and promises the previous run's figures.
    #      No source file is repointed: Main.hs and read-run.py name
    #      README anchors, which no run moves, and neither may name a run
    #      file. REPOINT ON THE UNWRAPPED FORM: a literal rename over the
    #      wrapped document misses any link text a line break falls inside
    #      while replacing its path. Run 18 lost three that way.
    #      Repointing is not re-verifying: --check-doc lists the links
    #      naming the run file AS A WHOLE; walk those and the section
    #      links both, against what the file now says. It lists the second
    #      kind nowhere, there being two dozen of them
    ./install-tables.sh $R                            # (7.4) install, never
    #      paste: --markdown, --fingerprint, a --block per class and
    #      --claims, eleven tables and a reading per claim, all from the
    #      BASIS half and all into `runs/$R.md`, which is the one
    #      document any of them writes. Take the movement reading BEFORE this: the claims
    #      install overwrites the figures a "moved from" sentence compares
    #      against, and after it they are in git or in the kept JSON only.
    #      Commit or park this file first, since every one of them writes
    #      it. Read
    #      what the driver collects at the end: a row new to the roster
    #      installs as `?` and is filled by hand, a departed row is
    #      dropped with a warning. The cross-class summary
    #      is assembled LAST, transcribed from the class tables
    #   6. walk the replace list under Provenance, re-run the two sweeps it
    #      names, and map every hit to the bullet covering it -- running
    #      them is not reading them. REPLACE, do not annotate: a figure that
    #      moved inside the floor is requoted without comment
    #  6a. REPLACE BY ANCHOR: `--replace ANCHOR --with FILE` swaps a
    #      paragraph without its old text passing through a transcript,
    #      which is what quoting it into a script costs and what Run 18
    #      paid sixty times over. Quote only what you are EDITING. It
    #      searches BOTH documents and refuses an anchor found in each,
    #      so which file holds a paragraph is not yours to know first;
    #      `--para` prints the file it found one in
    #   7. verify. Every count and ratio comes from --cells or --pair, never
    #      from a printed table, which is rounded to three figures; before
    #      re-deriving a figure a previous run published, reproduce THAT
    #      run's value with your method first. A new column needs a route
    #      sharing no code with the reader -- difference wall, or user AND
    #      system, at two iteration counts. Two instruments disagreeing is
    #      the finding: locate it, and until then neither is evidence. If
    #      any edit was scripted, assert its extent and read a
    #      `wrap80 --unwrap` diff of both sides: nothing else sees a lost
    #      paragraph. A correction is a claim -- derive it, then re-run the
    #      gates. Then --lint, --check-doc, adjudicate the worklists,
    #      read end to end, and walk the diff against the writing rules.
    #  7a. THE INDEPENDENT CHECKER, and it is a STEP because it is the
    #      highest-yield thing in this list: on Run 19 it returned 22
    #      defects, six of them whole paragraphs of the PREVIOUS run's
    #      left standing under this run's tables, which every mechanical
    #      gate here had passed and a truth-focused read had not caught.
    #      TWO passes on ONE agent -- tables when they go in, then the
    #      prose WITH the fixes the first pass caused. The second pass is
    #      not a formality: Run 19's found SEVEN errors introduced by the
    #      first pass's own fixes, two of them substantive, and a session
    #      that stops at one pass ships them.
    #      BRIEF IT WITH ALL OF THIS, since an under-briefed checker
    #      wastes its pass: it works in THIS directory; its evidence is
    #      this run's JSONs and read-run.py and nothing else; NO other
    #      repository's checkers come near this README; it re-runs no
    #      benchmark; it REPORTS ONLY and edits nothing; it quotes a
    #      distinctive PHRASE and never a line number, the file being
    #      rewrapped between turns; and it separates confirmed defects
    #      from what it could not check. Give it the diff and name the
    #      sections a run replaces.
    #      AND CHECK ITS WORK. Run 19's said twelve arms moved past 3%
    #      where sorting gives eleven. Its report is evidence, not verdict
    #      Once the write-up settles, one comprehension probe: a fresh
    #      session answers a few of the README's own questions from the
    #      document alone, with citations
    ./read-run.py --lint          # 8. again after ANY Main.hs edit, and
    #      never rebuild the pair to satisfy it: say in the write-up that
    #      the comment-only move happened
    #   9. record the run's name and regime, each process's stderr line,
    #      the machine, and THE COMMIT, transcribed from $R-pair.txt; also
    #      which half ran first. A class line's shape count is the whole
    #      class-view set, so the population size comes from the reader
    #   9a. collect what this run made CHEAPER for the next, which no
    #      other step gathers and which is not a figure: the checks that
    #      would have caught each error, the computations improvised, the
    #      steps skipped, and any capability found. Run 15's durable output
    #      was four checker gaps, two corrected rules here, and the finding
    #      that a probe needs no pair; none of it is in a table. It feeds
    #      10 and so comes before it -- a suffix here follows its number,
    #      as 10a and 10b do in the pre-run list, and never precedes it
    #  10. walk the open list: grep the settled index before adding an
    #      entry, move answered ones with their measurement, and add each
    #      surprise with what would settle it. Prediction verdicts go THERE,
    #      not in the chapter the next run replaces; report a split as a
    #      split, arm by arm    ./read-run.py $R-<basis>-main.json --deflation   # 10a. and the same
    #      on the control: the roster cell over its own alone leg, per
    #      shape, which is what the riders were run for. RAW over RAW,
    #      which the mode does because a leg carries no `sum-only` to
    #      correct with -- the one figure here a session had to hand-roll
    #      before the mode existed, and the one place it would reach for
    #      the wrong numerator    #  11. NAME THE FILL GROUPS off a -g3 twin, and spend the other
    #      load-independent measurements while the artifacts live --
    #      allocation, Core, a `size` invocation, minutes each. The naming
    #      is what this step is for and reads like housekeeping: it turns
    #      `[0, 24, 0, 4]` into four arms, and on Run 17 it collapsed two
    #      of this README's open questions into one object by showing the
    #      `[0, 0]` group IS the build/mut-odo residue. Owed by every
    #      paired run: rebuild each recipe with -g3, export the NAMED
    #      fills into the note, match groups by byte identity of the loop
    #      body and never by proximity, and read the count check -- a
    #      group whose twin carries fewer copies than the timed binary is
    #      not named from the twin at all
    #  12. offer the artifacts for deletion -- the JSONs, the logs, the
    #      wall-clock file, and for a pair both binaries and $R-pair.txt --
    #      once, after step 7 is done AND presented, saying what keeping
    #      them buys. Offering is the step; deleting is not

Steps 1 to 4 are readings and cost only tool calls; 5, 6 and the installs write;
7 is the one that finds things. The same contract holds here: the operative
facts are in the list, the reasons are below it, and step 11's window closes
when the artifacts go. The step most often skipped is 11, because by
then the run reads finished, and it is the only one whose window closes:
the artifacts are what it spends.



1. **Gate every population on the correction, before reading any figure ---
   and read the A/A *worst cell*, not only the pair's geomean.** A control
   that passes its gate can still be the run's most informative measurement:
   `bq-expand`'s distant twin passed on Run 8 and again on Run 9 while carrying
   a 41% cell, published both times as a noise floor, and chasing that one cell
   is what produced the roster fix and the nursery account [in the floor
   section][floor]. A pair inside the floor whose worst cell is an order
   of magnitude outside it is not noise; it is a finding the aggregate
   is hiding. The gates themselves: `--selftest` checks that the forcing term
   scales with `l` --- one pass over the elements, not something whose size
   varies with the shape --- and `--aa` prints both whether the two `sum-only`
   halves agree and how the term compares with the same pass measured in situ,
   off the `-nosum` arms. The three are independent and the correction needs all
   of them: position, size, and the read itself, each blind to what the others
   catch ([sum-only](#sum-only-and-the-correction-now-applied)). Any of them
   failing invalidates the whole time column rather than merely leaving
   it uncorrected, and all have to be re-passed by every run rather
   than inherited --- by every *population* too, each process carrying its own
   `sum-only` pair, its own eighteen A/A controls and its own four `-nosum`
   arms, so a class run passes or fails the gates on its own evidence
   and a failure there invalidates that class's column and no other.
   **Then write this run's own floor at the head of the chapter as you draft it,
   and keep it there.** That is where every margin judged against it is written
   too, so it is published with them rather than kept where only this session
   can see it. Every margin below is judged against it, it is re-measured each
   run, and the runs have disagreed several-fold, so the previous run's figure
   is the one you will reach for by habit and it is the wrong one. `--aa` prints
   each pair's raw ratio and `f` beside the net one for a related reason:
   the net figure is the floor between two published rows, the raw one is how
   much an arm disagrees with itself, and quoting the first as the second
   overstates it by 1/(1-f).
2. **Match bases before reading any ratio.** The first act of a comparison
   is making its two sides one basis --- the same population, the same
   restriction, the basis a claim was stated on --- and only then reading
   figures. Run 7's first claim check ran on its 24 shapes against claims stated
   on 22, and every pair had to be re-run.
3. Analyse with `./read-run.py`, which is where every table in this file comes
   from --- read [the reader's own section](#the-reader-read-runpy) first,
   and do not write another reader. **The claims are part of this and
   are the thing these steps are likeliest to leave out**: the run's file names
   three things a run reads, and the claims section is the third, each
   of its orderings carried in `--claims` with its registered expectation,
   so that a run transcribes printed verdicts rather than re-deriving the table.
   The class properties are the same job three times a population, off
   the verdicts `--block` emits, and the set is restated for the next run
   on this run's basis while the readings are still in front of you. **A paired
   run's own mode is `--compare`, and its direction is a convention worth
   stating**: the run given first is the one the ratios are *of*,
   the `--compare` argument being what they are divided by,
   so `basis --compare control` puts a figure below 1 where the basis is faster
   --- for Run 10, whose control was unaligned, that was where alignment
   was faster. Prediction 4's per-arm term and the aligned half's published
   column both read that way round; reversed, every one of them inverts
   and nothing in the output says so.
4. **One JSON at a time, never merged.** The reader takes one file,
   and its geomean is that file's population --- the main set's or one class's.
   Every mode names that population in its first line, `--selftest` fails a file
   spanning two and `--markdown` declines to emit a table for one, so a merged
   run is caught rather than published. The class tables stand beside the main
   geomean, per [the ruling](#the-stride-classes-and-what-they-cover), and there
   is no combined figure to compute, so a sentence comparing populations
   compares their tables.
5. **Make the run's own file and repoint README at it, and not before
   this step.** `runs/run<N>.md` is one run's write-up entire, so a run copies
   the last one's over its own name and rewrites it --- HERE, because every mode
   defaults to the newest file in `runs/` and everything above wants the run
   BEHIND this one: the gate's machine check reads the previous run's
   fingerprint and `--claims` reads back the claims it registered. Making
   the file early aims both at an empty copy of itself. What used to be four
   heading renames is one: *Recommended tasks after Run N*, in the open list,
   which is about the run just read. Its SECTIONS carry no number --- *Results*,
   *What the next run compares against*, *The claims the next run should test*,
   *The stride classes, run by run*, *Provenance* --- because the name does;
   the title is the second heading a run renames, and the copy renames it.
   So Run 9's eleven dead anchors and Run 18's three half-renamed links
   are failures this step no longer has. **What it has instead is one link
   check, and `runs/` accumulating is what makes it necessary**: the previous
   run's file stays on disk, so a link left pointing at it resolves, renders
   and quietly promises figures this run replaced. `--check-doc` fails every
   such link and names it. **Expect it to fail five ways the moment the file
   exists and before you have touched README** --- dead anchors, links naming
   the run before, the run file's sections uncovered by the replace list,
   the Results section naming the previous basis, and the head unchanged
   from the run before --- and every one of those is this step. Driven end
   to end 2026-08-25 on a copy: all five, and the eleven tables installing
   into the new file regardless. No source file is repointed: `Main.hs`
   and `read-run.py` name README anchors, which no run moves, and neither names
   a run file --- one that did would go stale at the next run, and `--check-doc`
   could not see it, `runs/` keeping every run so the path resolves. Repoint
   on the UNWRAPPED form, a path rename over the wrapped document missing any
   link text a wrap falls inside. Repointing is not re-verifying:
   a standing-prose link into the run file promises content the replacement may
   have moved out, and the ones that decayed this way kept resolving through two
   renames. `--check-doc` lists the links naming the file AS A WHOLE, which
   are the ones promising something unspecified; a link naming a SECTION
   of it is not listed, there being two dozen and a wall being what nobody reads
   --- so those are walked by hand, and by the same test: does the text still
   describe what is there. A link whose TEXT quotes a ratio, pointing
   at a section that no longer carries it, is what that walk is for:
   this refactor found one that had survived two runs with its anchor resolving
   throughout.
6. Walk the list under [Provenance](#provenance) of what the new numbers
   replace, and do not trust it to be complete: re-run the two sweeps it names
   and map each hit to the bullet covering it, since running the sweeps
   is not the same as reading them, and the list has been wrong before. **What
   skipping this costs is measured**: Run 16 walked it shallowly
   and an independent checker then found **fourteen of its twenty-one findings**
   were stale prose in sections this list names --- an anchor table, a launch
   window, four per-claim verdicts, a class calibration paragraph --- every one
   of them contradicted by a table the same write-up had just installed.
   **Replace; do not annotate.** Walking a list of what to replace makes "now X,
   where it was Y" the natural sentence, and a superseded number has to earn
   its place by the test in the user-scope `CLAUDE.md` --- would someone redo
   the work without it --- which most do not meet; `--check-doc` lists the ones
   already here for adjudication. And a figure that moved *inside* the floor
   is requoted without comment --- only a movement past the floor earns
   a sentence.
7. **Verify the write-up before deleting anything.** These are the checks
   the procedure used to leave to judgement, each of which has caught something.

   **This step is the whole of the document verification a run owes, and nothing
   else is to be reached for. Four passes, in this order:** run
   `./read-run.py --lint` and `--check-doc` --- **without `--quiet`, this being
   the one call that reads the worklists rather than the verdict** --- whose
   exit codes are the verdict; read the worklists they print and adjudicate each
   entry; read the write-up end to end against the run's own artifacts; and hand
   the diff to an independent checker, which the paragraph after next briefs.
   None of them is optional, the third is the one that keeps finding real
   errors, and the fourth is what catches what the third cannot see in its own
   writing.

   **REPLACE A PARAGRAPH BY ITS ANCHOR, NOT BY QUOTING IT.**
   `./read-run.py --replace ANCHOR --with FILE` swaps the paragraph carrying
   ANCHOR for the text in FILE and asserts the anchor is unique, so the old text
   never passes through a transcript and no `assert s.count(old) == 1` has
   to quote it back. That is the difference between naming a paragraph
   and reprinting it, and it is the largest single cost in a write-up: Run 18
   replaced some sixty paragraphs by locate-print-quote-assert and spent several
   times the whole document's reading budget doing it, with this mode sitting
   unused in the reader's own list. **Quoting is for a paragraph you
   are EDITING; replacing wants only the anchor** --- and a paragraph rewritten
   wholesale from this run's figures, which is most of them, needs no sight
   of what it replaces. The `Edit` tool is the same trade one level down:
   it demands the whole of `old_string`, so use it where the change is a clause
   and `--replace` where it is a paragraph.

   **And where the write-up is made by scripted replacement rather
   than by `Edit`, WRITE AFTER EVERY REPLACEMENT.** A batch that applies a list
   of edits and writes at the end loses all of them the moment one anchor
   misses: the assertion fires, the script exits, and the successes before
   it are discarded with the failure. Nothing announces that --- the run reports
   an error about one edit while silently dropping the rest --- and it cost Run
   16 six fixes that were then described in a commit message as done. Write
   the file inside the loop and report per edit, so a later miss cannot discard
   an earlier success. That is separate from what a scripted rewrite gets
   *wrong*, which is the next paragraph, and it is the failure to expect first
   because it is the quiet one.

   **Then one mechanical read comes before those four.** Unwrap both sides
   and diff them --- `wrap80 --unwrap` over the committed version and
   over the working one --- and read that diff for text that left without
   a replacement arriving. **And run the figure sweep BEFORE unwrapping,
   or re-wrap to read it**: `--check-doc` marks its worklist hits as added
   by this diff by comparing against the committed README, so while the document
   is unwrapped every line reads as changed and the classification is worthless.
   Run 16 unwrapped to edit --- which the wrapping rules ask for --- and thereby
   disabled the one sweep that would have found the stale prose the replace-list
   walk missed, being told 54 figures were new when most were untouched.
   A scripted rewrite fails in two shapes and neither is a wrong figure.
   Anchored on a *prefix*, it replaces the whole paragraph and drops whatever
   followed the part its author had read; `--check-doc` catches that one, every
   prose paragraph being required to end a sentence. Anchored on two *markers*,
   it deletes every paragraph between them, however many that turns out
   to be --- and nothing catches it: the survivors still end sentences,
   the anchors still resolve, the figures still match, and every check here
   is a predicate over what is **present**, so none can see what is gone.
   Measured on 2026-08-14, when a paragraph recording that the regime had
   been confirmed in the binary was removed from this file and `--lint`,
   `--check-doc` and the truncation check all exited 0. So assert the extent
   in the script, echo what it is about to overwrite, and read the unwrapped
   diff afterwards, which is the only place a lost paragraph shows.

   **A correction is a claim, and is written under exactly the conditions
   that produce bad ones.** Whatever the verification turns up gets fixed
   at the end of a long write-up, at speed, and the fix is a new assertion
   with no derivation behind it unless one is made: Run 13 corrected
   its allocation reading twice and the second correction was wrong, having
   been computed from a rounded print. Derive a fix the way the sentence
   it replaces should have been derived, re-run the gates after it, and give
   the checker's second pass the fixes and not the prose alone: on Run 15 four
   of that pass's seven findings existed only because the first round of fixes
   had been written.

   **DO NOT RE-DERIVE AN INSTALLED FIGURE AT ALL; spend the whole of that budget
   on the prose and on the sentences elsewhere your tables have just
   falsified.** Run 16's checker recomputed 487 table rows against the reader
   and found not one wrong, against 34 prose errors in the same diff; Run 18's
   recomputed 491 and found not one wrong either, against 52 prose findings
   over two checker passes and a comprehension probe --- so re-deriving
   an installed figure buys nothing that `--in-place` did not already guarantee,
   while every hour spent there is an hour not spent on the two places errors
   actually live. **Expect every error to be in the prose and none
   in the numbers, and expect the green checkers to be why.** Run 11 shipped
   six, and not one was a wrong figure out of the reader: four superlatives
   asserted without sorting the population they quantify over, one sentence
   contradicting its own paragraph three lines later, and one percentage
   computed from a published table instead of from the cells. `--lint`,
   `--check-doc`, `--selftest` and `--aa` were green throughout and right
   to be --- they check the measurements, and the measurements were sound.
   The hazard is that green instruments make the remaining gap feel small when
   the remaining gap is where all of it lives.

   A write-up is a document edit, so the three-pass discipline applies ---
   but its passes live here, in this repo's own instruments,
   and the general-purpose form of it does not fit a README whose claims
   are *measurements* rather than statements about code. Pass 1, which resolves
   `file:line` citations and pinned permalinks, has no subject: this README
   cites no line and no permalink, deliberately, and what it does cite --- arm
   names, strategy names, shape names, `Main.hs` functions --- is what `--lint`
   checks, which a line number could not, a citation surviving the refactor
   that moves it. Pass 2 is `--check-doc`'s path check. Pass 3 is the reading,
   below. The heading-scope and cross-reference passes are `--check-doc`'s
   anchor and replace-list coverage checks. No other repository's checkers
   belong in this README, for the reason given with the pre-run checklist, where
   a session meets these two tools first.

   **What the instruments cannot supply is the reading, and the reading
   is the pass.** What the tools print is its output and not its method:
   `--check-doc`'s three sweeps hand you a worklist of superseded figures,
   superlatives and absolute times, and adjudicating that list is not reading
   the document. Nor is inheriting one --- a worklist you did not derive
   verifies somebody else's findings while telling you nothing about what else
   is wrong, which is the completeness question the reading exists to answer.
   Run 11 is the case above: every checker green and the worklist adjudicated
   while six errors stood. **The checker and the comprehension probe are not two
   goes at one job, and the split is what makes the second worth its cost.**
   A checker is scoped to the diff: it reads what changed, recomputes it,
   and is the only instrument that returns completeness over a table. It cannot
   see a sentence in a section nobody touched that this run's tables have just
   falsified --- and on a run that changes its basis those are everywhere.
   The probe reads the README as a stranger meets it, and on Run 16
   that is exactly what it returned: three different thresholds quoted for one
   quantity, two of them in one paragraph; `six pairs` and `eighteen pairs` both
   given as the A/A population; a `keep the default area` ruling standing
   unmarked in the run that abandoned it; and two comparison rules that read
   as one and contradict. Not one of those is in any diff. **So run both,
   and read the probe's findings as being about the README rather than about
   the run.**

   **So put an independent checker on the diff against the artifacts, launched
   when the tables go in rather than at the end --- and the cost of launching
   late is measured** (Run 15, which launched once the whole write-up
   was drafted): its first pass returned seventeen findings, several of them
   prose built on a table figure a table-time pass would have caught first,
   and its second pass returned seven more of which four existed *only* because
   the first round of fixes had been written. Late launching does not merely
   delay the findings, it multiplies them --- and it is **two passes on one
   agent**, since at that moment only the tables exist: the tables as they go
   in, then the prose together with the fixes the first pass caused, the second
   continuing the first rather than paying a fresh bootstrap. Run 13's first
   pass verified 341 table lines and found the cross-class summary untouched;
   its second found six prose errors, including a previous run's figure
   presented as this one's. One agent, briefed to recompute every added figure
   from the reader and to re-derive every *only*, *largest* and *N of the nine*
   by sorting, and to report discrepancies rather than opinions. It is dear per
   finding --- Run 11's cost some thirty times what the same session's own
   targeted re-checks did --- and it is worth it anyway, because its findings
   are the ones a session has already proved it cannot see in its own prose,
   and because it returns a completeness the author cannot: 306 of 306 table
   rows verified rather than the ones somebody thought to check. Leave
   the placement, contradiction and writing-rule reading to yourself.
   **The brief is checked in as `checker-brief.txt` and is not to be retyped**
   --- it carries both agents' briefs and only its first block changes from run
   to run, which is the run name, the two half names and the previous run's two.
   Run 16 wrote it out twice, once because a rate limit killed the agent
   mid-pass. Four things it cannot derive are why it exists: which half
   is the basis, and so which of the eighteen JSONs every published table comes
   from; that it works in this directory, that its evidence is this run's own
   JSONs and `read-run.py`, and that no other repository's checkers come near
   this README --- it starts where your session started, so the artifacts
   are not where it is and the checkers it arrives with are not this README's.
   And once the write-up has settled, aim the same instrument at the finished
   README rather than the diff: a comprehension probe --- a fresh session
   answering a handful of the README's own questions from the document alone,
   with citations --- reads as a stranger what every diff-scoped check reads
   as a change, and on every run it has been given it has surfaced
   a contradiction between standing passages that nothing above could have seen.
   (The rule that a check must be proven able to fail governs the instruments
   themselves and is stated with them, [in the reader's
   section](#the-reader-read-runpy).)

   The checks themselves:
   1. **derive every count and ratio in the prose from `--cells`, never by eye,
      and never from a published table** --- the second half is the one
      that looks safe: a table prints three significant figures because
      that is what a reader needs, so arithmetic on its cells is arithmetic
      on the rounding. Run 11 computed its eleven anchor movements
      from the printed anchors and put the largest at +4.1% where the cells say
      +4.3%, which is a tenth of the figure and was invisible until
      an independent reader rebuilt it. A percentage, a ratio and a count all
      come from `--cells` or from `--pair`, whatever is printed three lines
      above --- and for a class paragraph, from the verdicts `--block` now emits
      under its per-shape line, which state the three properties' outcomes
      and name the arms that actually lead. That block exists because this rule
      kept losing to the table being right there while the paragraph
      was written: three of Run 9's class sentences were wrong that way
      and no mechanical check saw any of them. "32 of 33", "30th of its 33
      shapes", "the only two past 7%" are all claims a glance at a sorted table
      gets wrong; two of Run 6's were wrong until recomputed. Two shapes
      of claim need naming because counting is not what they look like. **Every
      *only*, *largest*, *fastest* or *never* is a claim about the whole table**
      and is derived by sorting it, not by looking at the arms the sentence
      is about: Run 8's write-up carried four such --- "the only arm the flag
      demotes", "the largest gain of any arm" among them --- each false,
      and each caught late or by a reader. And **a ratio between two published
      cells comes from `--pair`, never from dividing the printed figures**,
      which are rounded to three digits: the same write-up quoted 0.9898
      for a pair the reader puts at 0.9946. **And `--cells` is a print too**,
      its `alloc_mult` carrying four decimals, so a question finer than what
      it prints wants the mode that answers it rather than a script
      over the dump: allocation agreement is `--compare --alloc`, which exists
      because a script over the printed multiple found every cell agreeing where
      the underlying fit does not. **Before reading any figure whose predecessor
      is on record, reproduce the predecessor first.** Stated narrowly
      this is about re-deriving a published figure, and it generalises to every
      probe: Run 15's ladder probe reproduced Run 14's 14.1 and 22.3 ms before
      it read anything at a new nursery, which is the only reason the new figure
      was trustworthy the moment it appeared. This
      is the prove-a-search-non-vacuous rule applied to a derivation rather
      than a grep --- run the computation against a case whose answer is known
      before trusting it on one whose answer is not --- and it is cheap: one
      extra invocation. Run 13's write-up skipped it, read the wrong column, got
      a count that disagreed with what Run 12 had published, located
      that disagreement in the *data* rather than in its own *method*,
      and explained the residue with a mechanism the previous pair refutes.
      The one invocation would have stopped all three;
   2. **reproduce any newly-derived column by a route that shares no code
      with the reader.** A four-bench filtered run carrying both `sum-only`
      halves takes seconds, and criterion's own printed `time` lines then give
      the ratio by hand: on `cnn-slice-c32`,
      `(1.506 - 0.1739) / (6.339 - 0.1739)` = 0.2161 against the reader's 0.216.
      Recomputing from `--cells` is worth doing too, but it shares the reader's
      arithmetic and cannot catch a wrong definition, only a wrong
      transcription. Two rules the independent route needs, both learned
      by getting them wrong after Run 9. **Difference wall time, or user
      *and* system --- never user alone**: the inherited "wall and user time
      agree on it" is a property of the workload it was written for, and where
      the RTS does kernel work they part completely, which is how 0.36 ms per
      call of system time went unseen and a real 10% effect was reported
      as zero. And **difference at two scales**: if the per-call figure moves
      with `n`, part of what is being divided is a fixed cost, which is how
      a one-time 0.9 s of page-faulting read as half a millisecond a call;
   3. **take the cheap decomposition before proposing a mechanism.** Where
      a cost can be split by an instrument already to hand --- mutator against
      collector, one arm against another, alone against after --- split
      it first: Run 15 built a copying account of the position term, found
      its arithmetic off by two orders, and settled the question with a single
      `-s` reading of GC against mutator time that should have come before
      the account rather than after it. **And when two instruments disagree,
      that is the finding.** Do not average them, pick the one the README
      prefers, or quietly drop the awkward one. Locate the disagreement first:
      the criterion slope and the `-n` differencing above parted by 8 points
      on one arm, both reproducible to a fraction of a percent, and the cause
      was neither sampling nor sample size but which clock was being read. Until
      it is located, neither number is evidence, and a retraction made
      on the strength of the wrong one is worse than the claim it withdrew;
   4. **install the tables with `--in-place` rather than pasting them.**
      `--markdown`, `--fingerprint`, `--block` and `--claims` each take it ---
      the last installing a `Readings:` paragraph under each claim's lead rather
      than a table --- and each refuses rather than guessing: the match
      is by whole line, the count is asserted, and a class table is narrowed
      by its block's bolded lead. **A claim's reading is placed
      by its `**Claim N` lead the same way, which is prose the write-up
      is editing while it works**: rename a lead and the install that fills
      the paragraph beneath it refuses, naming the claim. Hand-pasting is what
      this replaces, and the reason is on the record --- the cross-class
      summary's header is written out twice, once indented as the spec
      that fixes the columns, and a session locating the table by searching
      for that text put Run 8's rows under the spec and left Run 7's table
      standing, with every check green because the check looked it up the same
      way. If you paste by hand anyway, do not edit the table: it renders
      the same rows the terminal does, and carries `needs` and the emphasis
      forward from the table already there. `--aa` and `--block` both take
      `--brief`, which drops the standing explanation and the table `--in-place`
      installs anyway, costing no computed figure; across a run's processes
      that is several hundred lines you have already read. Its stderr
      is the whole of what is left by hand: a row new to the roster comes out
      with `?`, a departed row is dropped with a warning. Run 9 had ten such
      rows and filled them from a note written here before the run, which
      is the practice to repeat whenever a roster change is known in advance ---
      the cell then gets transcribed rather than invented at the end of a long
      day. Each class JSON emits its own table the same way and is pasted
      the same way, into its block in [The stride classes, run
      by run](runs/run19.md#the-stride-classes-run-by-run); those come out six
      columns wide, `needs` being a property of a strategy rather than
      of a population and so stated in the main table alone. The per-shape
      fingerprint is pasted the same way, whole, from `--fingerprint`;
   5. **assemble the cross-class summary last, from the tables and not
      from the JSONs.** Every cell of it appears in one of the class tables
      above it, so it is a transcription and is checked as one --- cell against
      table, each in turn --- where recomputing it from the runs would
      be a second derivation able to disagree with the tables it summarises.
      **Each class's `--block` now checks its own row** and names the cell
      on stderr, so `install-tables.sh` reports a wrong transcription among what
      it leaves you; the table stays hand-assembled because its emphasis
      is a judgement no reader can derive, and the marks have already drifted
      between runs;
   6. **check that every `](#...)` resolves**, here and in `Main.hs`'s
      `README.md#...` references, and that every figure-bearing section
      is linked from the Provenance list. Findings rename headings,
      and a renamed heading breaks a link silently;
   7. **walk the diff against the writing rules as a check of its own, not only
      while writing.** The replace-list walk manufactures "now X, where
      it was Y", requoting a count in place preserves a sentence that should
      have lost its numeral, and a class paragraph's close invites a mechanism
      the run never measured. `--check-doc`'s figure sweep lists candidates,
      `Main.hs` comments included, and `--para` prints the ones it names without
      reading the file around them, but the redo test itself is the reader's.
      Run 7's write-up carried fifteen-odd such sentences past every green check
      here, found only when a reader asked;
   8. **read the document end to end**, and aim the reading at what
      the instruments cannot see. The mechanical passes above do not catch
      a bullet contradicting the table three lines below it, which is how
      "`bq-mut` ties `bq-expand`" survived two runs beside a build ordering
      that refuted it. Nor do they see the three things Run 8's write-up got
      wrong: a table installed in the wrong place, an exclusivity claim about
      arms nobody sorted, and a figure quoted on a basis it was not measured on.
      That the checkers here are good is itself the hazard --- green instruments
      make the remaining gap feel small, and the gap is exactly where they do
      not look, so read for placement, for *only* and *largest*, and for which
      run and basis each figure belongs to. This is the pass that keeps finding
      real errors;

   **Four conventions this README holds to, each of which exists because
   breaking it has cost something here.** **A ratio is quoted in the direction
   `--pair` prints it, or the sentence says in words which arm is faster.** Both
   directions appear in this file, a margin and its reciprocal, and a WIN COUNT
   belongs to only one of them --- so a reciprocal quoted beside its own arm's
   win count inverts the finding while every check here stays green. Run 18's
   opening did exactly that to the run's headline reading, on both halves
   at once, and a comprehension probe caught it where two checker passes had
   not. **A figure in prose names its run, its basis and its population,
   or it belongs in a table with the prose pointing at it** --- a bare numeral
   carries no provenance, and that is how one sentence came to put a Failed Run
   6 figure beside a Run 6 one, and another to compare a *published* ratio
   with a *paired* one. The population is the newest way to make that mistake
   and the easiest, a class figure and a main-set one being the same kind
   of number over different shapes. **An anchor longer than about thirty
   characters goes reference-style**, defined at the foot of the file: inline
   it overflows the width and the rewrapping that follows is pure churn.
   And **a link's text names its subject, never its position** --- five links
   reading *the head of the run chapter* kept resolving through two renames
   while the content they promised left it, a decay no anchor check sees, which
   is why `--check-doc` lists standing-prose links into the run's file and step
   5 re-verifies them;
8. Re-run `--lint` after editing `Main.hs`, even when only comments changed:
   the reader parses that file for the roster and the shape dims, so a comment
   edit can break a check that passed before it. `--lint` reads the source
   and needs no build, which is the whole of what that reason asks for. **Do
   not rebuild the pair to satisfy this step.** Steps 6 and 7.7 send you
   into `Main.hs`'s comments on purpose, and a rebuild would replace both halves
   and want a fresh note stamped with today's date and commit --- which
   is the file the next step transcribes the binary's provenance out of.
   A comment edit after the run leaves the timed binaries correct and the source
   they were built from moved by a comment; say so in the write-up rather
   than rebuilding to hide it;
9. Record beside the numbers the run's name and regime, each process's stderr
   provenance line, which machine, **and the commit the binary was built
   from** --- for a paired run, transcribed from `<prefix>-pair.txt`, which
   carries the commit, the regime, the GHC and both md5s because this step asks
   for them --- the GHC only since 2026-08-16, the template having had no slot
   for it and Run 14's note therefore having none, where
   `strings $R-<basis> | grep -oE 'ghc-[0-9.]+'` reads it back out of a binary
   still on disk --- and the note outlives the session that built the pair
   (the JSONs do not survive, so the source is the only thing that makes a run
   reproducible even in principle --- this README's figures are one desktop's
   and are not portable, see [Provenance](#provenance)). A class process's line
   is measured for its elapsed time and its two heap peaks but not for its shape
   count: that count is fixed before criterion does the selecting, so it reads
   every class view rather than the population that ran, and the population's
   own size comes from the reader's first line;
10. **Walk the open list against what this session actually did**, which nothing
    checks. **Grep [the settled index][settled] before adding an entry ---
    and before ASSERTING anything this README may already have ruled on**,
    not only before deriving: a question is easy to open against something
    already answered in a section you are not writing in, which is how Run 10's
    write-up proposed a Core dump that had been taken three times and whose
    answer --- `vBuildVS` surviving as no top-level binding, so there is no call
    path to dump --- was recorded at the ceiling, a thousand lines from where
    the entry was being written. A run answers some of its own questions
    and a write-up raises others, and both go stale in place: Run 8 answered
    the element-type entry with the probe that entry specified and left
    it standing open, and answered the packed-arm entry the same day. Move what
    was answered into the answered block with its measurement, leave what
    a probe narrowed as narrowed, and add the run's surprises
    with the measurement that would settle each.
11. **Spend the load-independent measurements before the artifacts go.**
    Allocation is deterministic per call, Core is a compile, and a binary's size
    is a `size` invocation --- none of them wants a quiet machine or a run slot,
    and each is minutes. Run 8 stopped at the write-up and left a Core diff,
    a two-regime `diag` and a code-size figure undone; all three were done
    later, two of them changed rulings, and one answered an open question
    outright. So before step 12, take every question on the open list whose
    measurement is a compile, an allocation or an arithmetic re-derivation,
    and take it now. **One of them is owed by every paired run and is named here
    so it is not rediscovered: export the pair's NAMED fills into its note.**
    `loop-offsets.py` names a copy only in a `-g3` build, so each half's recipe
    is rebuilt with `-g3` added and the twin's groups matched to the timed ones
    by byte identity of the loop body --- never by proximity or by which group
    sorts first. Bare offsets are what the note records otherwise, and the map
    is a property of the binary: once the binaries go, no offset this README
    quotes can ever be tied to an arm again. Run 12's were derived this way
    on the last day they existed and refuted two accounts of its own split; Run
    10's and Run 11's are gone unnamed. What is left over is the timing work,
    which is what a quiet machine is for.
12. **Only then, offer the artifacts for deletion --- once --- and abide
    by the answer.** The JSONs, the logs and the wall-clock file, and
    for a paired run the two binaries and their `$R-pair.txt` with them,
    that note being about a pair and worth little once the pair is gone.
    **Offering is the step; deleting is not**, and the offer is made after
    the verification above is done and presented, not after the writing --- Run
    6's artifact went as soon as its write-up was drafted, which cost
    the ability to re-check anything needing the raw samples when that write-up
    was later questioned.

    **They are not required to go, and this README no longer says they are.**
    The rule used to be that the normal state of this directory is no run
    artifact at all; what justified it was that the numbers live in this file
    and the fingerprint exists precisely so a per-shape record outlives its run.
    Both remain true, and neither makes deletion *owed*: what they actually
    argue is that nothing is *lost* by deleting, which is a licence and
    not an obligation. What is lost by deleting early is concrete and has
    been paid twice --- every `--pair` a later question wants, every per-shape
    spread that separates a bias from noise, every count re-derived
    from `--cells`, and every sample-level reading needs the JSON and nothing
    else does. Run 8's were kept and drawn on a dozen times in the days after,
    for questions its write-up had not thought to ask; Run 11's were kept
    and became the disturbed control and the wild cell's sample-level account,
    neither of which its write-up foresaw.

    So: ask once, say what they buy, and take no for an answer without raising
    it again. A previous run's artifacts still being here is not a defect
    to be tidied and is not a blocker for the next run, whose relaunch guard
    is scoped to its own name.


### Other toolchains, probed and not run

**Two of these three paragraphs are probe records and not run instructions**,
which is why they sit here rather than in [Running it](#running-it), where they
stood between a session reading the run modes and the chapter it was reading
them for. Their figures are a probe's on another compiler or another backend;
no run here replaces them, and what would call for re-probing is a move
in either toolchain rather than a run. Read them when a toolchain question
arises, and not on the way to an evening. **The HEAD paragraph is the exception
since 2026-08-24**: Run 19's control half is built through the project file
it names, so what was a probe's recipe is a pair's, and the file rather
than the paragraph is the copy of record.

**Running the suite through GHC's LLVM backend takes two flags and a different
correction.** `--ghc-options=-fllvm` sends Main.hs through the `opt` and `llc`
that `ghc --info` names --- `opt-18` and `llc-18` here ---
and `--ghc-options=-optlc-align-loops=64` puts its loop heads on a cache line,
LLVM's own default for them being 16 bytes; that option is in bytes where
its `--align-all-nofallthru-blocks` neighbour is in log2, and the latter pads
every branch target rather than the loops. The assembler shim on `-pgma`
is the native backend's instrument and has no business in such a build. What
does not carry over at all is the forcing-pass correction: `sum-only` runs
a median 1.49x and a worst 2.29x of the bench it would be subtracted from,
so the default sinks most cells and the column reads `--`. Read such a run
with `./read-run.py RUN --corr=insitu`, which subtracts the term the `-nosum`
pairs measure instead, says on stderr that it did, and is comparable
to no figure in this README --- [the correction
section](#sum-only-and-the-correction-now-applied) has what that trades away.

**Compiling with a GHC HEAD build wants a project file of its own,
and `cabal.project.ghead` is it** --- `cabal.project.freeze` pins `base`
and so refuses every other compiler. It names the checkout's stage1 `ghc`
in `with-compiler`, carries `allow-newer` for the boot packages
and `constraints: base installed`, and pins by hand what a freeze would
otherwise have held: `criterion ==1.6.5.0` and `vector ==0.13.2.0`
with `vector`'s `+boundschecks -unsafechecks`, those being what every run here
was taken on, and `hashable ==1.5.0.0`, whose cabal file declares
the `ghc-bignum` its source imports where 1.5.1.0's does not, so the newer one
does not compile here at all. `cabal.project.ghead.freeze` beside it pins
the rest at the index-state the other two plans hold. head.hackage is neither
needed nor helpful --- its index here is stale enough that the tarball hashes
no longer verify. Why each pin is there is in the file's own comments,
so a session building on HEAD reads that and not this.

**And what the vecdims family reads under each, from probe legs and not
from a recorded run** (2026-08-21, one bench per process so that every arm sits
at the same slot, on a machine that was not idle). On the native backend
`mut-odo-vecdims` and `-add-in` tied, inside the A/A floor and with the sign
test flat --- a reading Run 17 has since gone past, its roster and three paired
probes all putting `-add-in` ahead ([its entry][open]), so read these legs
for the *other three* arms and not for that pair --- and `-add-both-down`,
`-add-both` and `-add-out` follow 6 to 11% behind. Under LLVM with 64-byte loop
heads those two tie again, the in-process and one-per-process legs straddling 1,
and the other three sit 8 to 11% back in an order the two legs do not agree
on --- so the tie is the durable reading and the losers' own ranking is not.
In absolute terms the winner's fill, read off its `-nosum` leg so
that no forcing pass is in it, runs about 0.90 of its native-backend self
and is ahead on all but three shapes; that figure crosses compiler, backend
and dependency set at once, and its two windows are an hour apart on that same
busy machine, so read it as a direction with a magnitude and not
as a measurement of the backend.


### The reader: read-run.py

Every figure below comes out of `read-run.py` in this directory, and the table
above is *emitted* by it rather than copied from it. **Use it; do not write
another reader.** It reads two documents --- this file and the run's own,
`runs/run<N>.md` --- and knows which of them a mode's subject is in, so a caller
names a paragraph and not a file. The definitions it encodes --- which cells
the column caps, that `CI%` is a mean half-width rather than a bound,
that `alloc` needs an `l` the JSON does not carry (it parses `Main.hs` for it),
that the `*-aa-*`, `sum-only*` and `*-nosum` rows are controls, that every ratio
is net of the forcing pass while every other column is raw --- each cost
a session to settle, and an ad-hoc script gets them subtly wrong. Its docstring
is the reference for all of them; extend the script rather than starting over.

**`check-scripts.py` is the one exception to that, and it is where a defect
of the reader goes.** `--selftest` asserts a run's numbers; the two reviews
of 2026-08-17 found thirty defects that were not numbers at all --- a class
table installed over the next class's, four checks whose silence read as a pass,
a mode the dispatch dropped without a word, a subprocess status ignored ---
and it caught none of them, calling no checker, no installer and no flag guard.
The corpus drives every script here from outside, exit code and stderr included,
planting each fault again into a copy of this README or of a run JSON;
and `--audit` replays each case against the commit BEFORE its own fix, where
it must fail. That is what makes a fix's proof outlive the commit: every proof
made that day compared the new file against `git show HEAD:...`, which stops
meaning anything the moment the fix is HEAD. **The case comes before the fix**
--- a claim that turns out wrong costs one case rather than one implementation,
and a fix without one has come back twice here already. What it does NOT yet do
--- a source lint for the families these defects fall into, which is the only
thing that would find an instance nobody has observed --- is recorded in its own
docstring rather than re-derived.

    ./check-scripts.py                      # the scripts' own defect corpus
    ./check-scripts.py --families           # and the shapes these defects
                                            # keep returning in, over the
                                            # Python source: the only one
                                            # of the three that names a
                                            # site nobody has looked at
    ./check-scripts.py --properties         # and its properties, over every
                                            # run on disk rather than any
                                            # fixture: the half that can
                                            # find a defect nobody has met
    ./read-run.py RUN.json                  # roster, then the strategy table
    ./read-run.py RUN.json --markdown       # that table as README markdown
    ./read-run.py RUN.json --shapes         # per shape: CI% max / median / mean
    ./read-run.py RUN.json --aa             # controls, spans, in-situ term
    ./read-run.py RUN.json --pair A B       # two arms, paired, with an interval
    ./read-run.py A.json --compare B.json   # one arm across two runs
    ./read-run.py A.json --compare B.json --alloc  # what each arm allocates
    ./read-run.py A.json --compare B.json --chapter  # the chapter's figures
    ./read-run.py A.json --compare B.json --bridge # ratios to `list`, so a
                                            # moved box cancels; the plain
                                            # form reads absolutes, and a
                                            # box that moved then puts every
                                            # arm at the box's own figure
    ./read-run.py A.json --compare B.json --ci  # the CI% column's MEDIAN,
                                            # which is the statistic it
                                            # publishes and not the mean
    ./read-run.py RUN.json --claims         # every claim's verdict, one call
    #      then the README's verdict figures read back: what reproduces these
    #      readings, and what is neither theirs nor attributed to a run
    ./read-run.py RUN.json --cells          # every cell as TSV, for the rest
    ./read-run.py RUN.json --fingerprint    # the kept per-shape record
    ./read-run.py RUN.json --block          # a class block's parts, + verdicts
    ./read-run.py --extremes --classes A.json B.json ...  # which class holds
                                            # each extreme -- tightest floor,
                                            # widest gap, best class for an
                                            # arm -- since a superlative about
                                            # the classes has no other source
    ./read-run.py RUN.json --markdown --in-place   # install it, do not paste
    ./read-run.py RUN.json --selftest       # check the reader's own invariants
    ./read-run.py RUN.json --exclude concat-runs --exclude-shape deep-7-c512-k3
    ./read-run.py RUN.json --deflation      # the roster cell over this run's
                                            # own alone legs, per shape
    ./read-run.py RUN-half-pop.log --wild   # the per-sample instrument's LOG,
                                            # not a JSON: each bench's
                                            # pre/post pair differenced, and
                                            # the foreign CPU during its
                                            # samples where the stamp carries
                                            # the load fields. --verbose adds
                                            # the per-sample dump
    ./read-run.py --lint                    # Main.hs's roster and shape
                                            # annotations, against both
                                            # documents and against itself
    ./read-run.py --run-doc runs/run20.md ANY-OF-THE-ABOVE
                                            # which run's file to read or
                                            # write; the newest in runs/
                                            # by default, and the only
                                            # document --in-place writes
    ./read-run.py --para 'the floor is'     # the paragraphs whose bolded
                                            # lead matches, in EITHER
                                            # document, and their lines
    ./read-run.py --replace ANCHOR --with F # swap the paragraph carrying
                                            # ANCHOR for the text in F,
                                            # without the old text passing
                                            # through a transcript. The unit
                                            # is a BLANK-LINE PARAGRAPH, and
                                            # a list with no blank lines
                                            # between its items is one of
                                            # them -- so an anchor in any
                                            # item but the first is refused,
                                            # and so is a replacement that is
                                            # one item where the paragraph
                                            # is nine

**Anything this reader can emit, a session should not read.** It is why
no write-up has ever read a table row out of either document: `--markdown`,
`--fingerprint` and `--block` emit those rows and `--in-place` installs them,
so three hundred-odd cells are never carried through a context that does
not need them. `--claims --in-place` extended that from rows to prose,
the readings under each claim being the reader's sentence and not the author's.
`--para` is the same trick for prose --- the alternative is a `grep -n` paired
with a `sed -n` for every passage wanted, both of which go stale the moment
an edit above moves the lines, which every install and every fix does. The rule
generalises: when a session finds itself reading this README to get at something
the reader could compute or locate, that is a mode missing rather than a README
to read harder.

Every mode's first line names the run's **population** --- the main set or one
[stride class](#the-stride-classes-and-what-they-cover) --- which the reader
works out from the shape lists in `Main.hs`. It is the one property of a run
that no column shows and every figure depends on, so `--selftest` fails a file
spanning two populations and `--markdown` emits no table for one: a geomean
over two of them is a statistic of neither.

`--pair` compares two arms **shape by shape**, and it is the right way
to compare any two: a strategy's ratio to `list` spans six-fold across the shape
set, so an unpaired comparison of two table columns fights that spread, while
`A_s/B_s` does not --- both arms move together with the shape. `list` cancels
out of it too, so a paired figure owes nothing to the baseline. It prints
the paired geomean, a bootstrap interval, the win count and its sign test,
and the published-column ratio beside them, those last two answering different
questions. **Reach for it instead of writing a script.** Every paired figure
this README quotes was once recomputed by hand and thrown away, which is how one
came to be printed beside a figure from a different run.

The interval wants multiplying before it is believed, and `--aa` says by how
much: the A/A pairs are the only comparisons whose true answer is known
to be exactly 1, so they are the only place an interval can be held
to an answer. `--aa` reports whether each covers 1 and how its half-width
compares with the spread the pairs actually show, which turns the floor
from a threshold someone chose into a factor a run measured. Read that factor
as an order of magnitude: it rests on eighteen pairs.

`--markdown` renders the same rows the plain table does, from one shared call,
so the published figures cannot drift from the terminal's. It reads the Results
table already in the run's file for the one column a run cannot know --- `needs`
--- and for which rows the prose emphasises, carries those forward, and says
on stderr what it could not: a strategy new to the roster comes out with `?`
to be written by hand, and one that has left it is dropped with a warning.
The arms added after Run 6 sat in exactly that state until Run 7 timed them,
which is what the mechanism is for.

**A run artifact is made when a question needs it**, which is the same moment
the reader is wanted, so it is built to be useful on a partial run as well
as a full one:

    micro --json RUN.json                                    # the whole thing
    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

**Quote every glob**, as those are: unquoted, the shell expands them first,
and in this directory `*/build` becomes `dist-newstyle/build` while `*/mut-odo`
finds no match and survives --- so one arm silently leaves the run and criterion
reports nothing wrong. That cost a placement probe its whole point once, the arm
dropped being the only one the probe was about. The general guard is to count
what a filtered run selected before reading it ([the
procedure](#making-a-major-benchmark-run)), which catches this
and the repeated-`-m` mistake alike.

The second takes seconds and still exercises the reader; a one-shape run says
so. A filtered run like it carries no `sum-only` bench, so its figures
are uncorrected and not comparable to the tables here --- the reader warns
on stderr when that is what it is reading. A run's JSONs go when its questions
are answered and the offer to delete them is accepted, so whether a table here
can be re-derived depends on what is still in the directory; the next run
replaces it either way.

`--lint` needs no run JSON at all, which is this directory's usual state.
It reads `roster` out of `Main.hs` --- the one list both the benchmark
and `check` are built from --- and asks the four things about it that go stale
silently: is every arm named somewhere in this file; is every strategy defined
in `Main.hs` rostered, so that none is left neither timed nor checked; does each
A/A control run the same function as the arm its name duplicates; and is every
control named as the reader's own control test reads it, since a renamed one
would enter the aggregates as a strategy. An arm rostered and deliberately
not timed is a note rather than a failure, and since the two rulings that note
is the larger half of the strategies: it prints the split and wraps the names,
being the one place the checked-but-untimed set is listed at all.

It asks a fifth about the shape lists rather than the roster: does every entry's
`l` annotation agree with what its list's rule computes, so that a mistyped
dimension or annotation is caught at edit time. `--selftest` had that oracle
first and still carries it, but only for the shapes a run's JSON happens to hold
--- which for a class list is after that population's process has finished,
hours past the point where the check is worth anything.

And a sixth about a second file: do `Probe.hs`'s six copied shapes still match
the dims `Main.hs` gives those names. The probe is a separate program
and its shapes are copies (its header says why), so this is the one thing
standing between a transposed dim there and a probe measuring a shape it still
names after --- which is not hypothetical, three of the six being wrong when
they were first written and named by this check.

The question it used to ask second --- is every benchmarked strategy also held
to the reference by `check`? --- is gone, and deliberately. The roster
and the agreement chain were two hand-written lists of the same strategies,
and that check compared them; one list now builds both, so the drift cannot
happen rather than being merely detectable. A check that cannot fail is a silent
search, so it was replaced rather than kept.

That is the standing rule for everything under `--lint`, `--selftest`,
`--check-doc` and the `health` warnings, and it is why each carries a recorded
proof in its docstring: **a new check is not finished until it has been made
to fail on purpose**, with what was broken and what it then said written down
beside it --- **written down AFTER it has been run and quoting what it printed,
never as the plan for running it**. That distinction is not pedantry: a proof
composed in advance reads exactly like one performed, nothing downstream can
tell them apart, and Run 18 wrote one into a case comment and reported
it as done before running it. It happened to agree when run; the next one will
not. Several here can only fail on data no real run produces --- a forcing term
larger than the cell it is subtracted from, a term that does not scale with `l`
--- so provoking them is the only way to know they are wired to anything.
It reaches a pass run *by hand* too, which has the same failure and no exit
status to hint at it: before calling one clean, break something it ought
to catch and confirm it says so. And it reaches a check's every *branch*:
the path check's absent-sibling arm is exercised by pointing its roots
at a directory that does not exist, since a branch no control reaches
is a silent search whatever the checks around it do.

`--selftest` checks invariants of whatever run it is given: that the dims
it parses out of `Main.hs` match that file's own `l` annotations, that every
cell has a positive slope and a sane R^2, that the forcing term is positive
on every shape and leaves every cell's net positive, that the same term scales
with `l` as one pass over the elements must, that every row's winsorized geomean
covers all shapes and lands inside its own per-shape range, that `list` against
itself is 1, and that an A/A pair with no capped cell has its published ratio
equal to its paired one. The one thing it still cannot reach --- that `sInner`
is the second-to-last listed dim --- it now names as `check`'s rather
than as nobody's. It names what it could not exercise rather than passing
silently, and exits 2 when the run file is absent. That last invariant
is a finding: the A/A ratios in the noise-floor table are geomeans over every
shape, so a published ratio is the paired one whenever neither arm had a cell
capped. `--aa` prints both and `--selftest` asserts the identity where it holds.


### What moves a figure when no strategy changed

Eighteen A/A controls run an existing strategy twice under a second name ---
nine strategies, each duplicated once beside its base and once at a distance,
so position varies within a strategy and strategy within a position.
The `offtab` and `bq-odo-gm-mulback` pairs, added 2026-08-14 for the coverage
gap the wild-cell entry names and for the spread instrument's widest arm,
and the `build`, `mut-odo`, `list` and `gen-unsafe` pairs added the same day ---
the placement-sensitive pair that carries Run 14's own control, the denominator
every ratio divides by, and the one wide arm flat against every shape dimension
--- are first read in Run 14, so the table below is Run 13's six. They
are the only rows whose true ratio is known to be exactly 1 --- or were, until
[the mutable ceiling](#the-mutable-ceiling-taken) turned up another by accident:

| pair | span | max-skip | +lookrts | mean per cell |
|---|---:|---:|---:|---:|
| `mut-odo-vecdims` vs adjacent twin | 1 | **0.9972** | 0.9984 | 0.40 / 0.27% |
| `mut-odo-vecdims` vs distant twin | 3 | 0.9974 | 0.9997 | 0.42 / 0.25% |
| `bq-scan-rem-gm-mulback` vs adjacent twin | 0 | 1.0014 | 1.0003 | 0.24 / 0.07% |
| `bq-expand` vs distant twin | 25 | 1.0007 | 1.0008 | 0.40 / 0.44% |
| `bq-expand` vs adjacent twin | 1 | 0.9998 | 0.9994 | 0.22 / 0.12% |
| `bq-scan-rem-gm-mulback` vs distant twin | 22 | **1.0033** | **1.0062** | 0.52 / 0.68% |

Run 13 is paired, so each pair reads twice; the two columns are the two binaries
and nothing else. No pair had a cell capped in either half, so every published
figure above equals its paired one --- the identity the winsorized estimator
bought and `--selftest` asserts --- and the published column is the yardstick
for comparing two rows of the Results table, while a margin measured per shape
still belongs against the paired figures `read-run.py --aa` prints. Two spans
moved by one against Run 12's, the roster having gained an arm between
the distant twins and their bases.

**On Run 19 the floor is 2.32% on the basis half and 1.71% on the control,
and both ends loosened on the run before.** Both are over the eighteen A/A
pairs, on the roster, that Run 18's 1.36% and 1.42%, Run 17's 3.70% and 3.89%
and Run 16's 2.32% and 1.22% were measured on, so the last five runs compare
directly. `offtab-aa-distant` carries the basis figure and `build-aa-distant`
the control one, both among the widest-spread arms the twelve twins were added
to expose. Read on the six pairs that carry back to Run 10 the same run gives
0.49% and 0.29%, against Run 18's 0.54% and 0.31%. **And this run settles what
Run 18 could only list candidates for.** Run 18 saw both ends tighten together
and could not attribute it, naming the box and the preamble as the two
candidates its pair could not separate. Run 19's basis half is Run 18's basis
BINARY, byte for byte, on the same box, the same roster, the same layout,
the same regime and the same preamble --- and it reads **2.32% where that binary
read 1.36%**, a factor of 1.7 with every one of those candidates held still.
So the floor is a property of the RUN, re-drawn each evening, and neither
the box nor the preamble nor the pair's variable is what sets it; what remains
is the eighteen pairs' own sampling, which the six-pair figure's steadiness
across the same two runs (0.54% then 0.49%) locates in the twelve outside them.
The threshold this run supports is therefore two figures --- *0.49% between any
two rows of the table* on the six-pair basis, which is what carries across runs,
and 2.32% on the eighteen --- where Run 18 supported 0.54% and 1.36%, Run 17
1.31% and 3.70%, Run 16 0.39% and 2.32%, Run 14 0.29% and 2.19%, Run 12 0.35%
and 0.24%, Run 11 a quarter of a percent on its max-skip half and 1.21%
on the other, Run 10 1.00% unaligned and 0.54% aligned, Run 9 under 0.1%
with a wild cell, Run 8 0.5% and Run 7 nearly 4%. Runs disagreeing several-fold
on the floor is itself the caution, and one binary disagreeing by 1.7x
with itself a day later is that caution sharpened as far as it goes: read
the floor as the run's *and the half's*, re-measured every time, never
as a constant of the harness and never inherited.

**The twins have now taken every side available, which is what a sign this weak
is worth.** Run 10 read all six pairs above 1 on its unaligned half and five
of six above on its aligned one, the twin slower than its base, and called
it worth a sentence and not a mechanism. Run 11 read all six *below* 1
on that same aligned binary and five of six above on the max-skip one. Run 12
split both halves, three of six above on the basis and four on the flag half.
Run 13 splits both halves evenly --- three of six above 1 in each --- which
is again the arrangement a fair coin gives. Three strategies at two positions
each are not six independent draws, and the direction is evidently
not a property of the code, the layout or the roster order, all of which
were held fixed across the flips.

Those six pairs' bootstrap intervals are half-widths of 0.06-0.65% and their
`CI%` column reads 0.05-0.13%, so the interval still understates run-to-run
variability: it measures sampling error *within* one benchmark, while two
separately placed benchmarks also differ in code layout, cache occupancy
and inherited GC state. The A/A is the only column that sees that, and `--aa`
prints the calibration outright --- on Run 19, a median interval half-width
of 0.49% against an observed spread of 2.32% on the basis half, a factor
of **5**, and 0.52% against 1.71% on the control, a factor of **3** ---
so multiply any interval this reader prints by about that before believing it,
where Run 18 wanted three and three, Run 17 five and five, Run 16 five and two,
Run 14 three and twelve, Run 12 one either way, Run 11 one on its max-skip half
and three on its aligned one, Run 10 four and one, Run 9 nine, Run 8 two and Run
7 three. **That the two halves DISAGREE on the factor this run** --- five
against three, where Run 18's agreed at three and three and Run 17's at five
and five --- is the same fact as the basis half carrying both the wider floor
and the wider cells, and it is a gap of two, where Run 16 read five against two
and Run 14 three against twelve --- so the halves parting is not itself unusual,
and what is new is only that this pair's did. Neither main set carries a wild
cell, at 18.50% and 17.66%; the loosest cell of the run is a class's,
and the run file's head reads it. What the basis half carries is two
of its eighteen intervals missing 1 against the control's one, every one of them
an arm whose two processes differ by less than its interval admits. It rests
on eighteen pairs, so one loose pair moves it less than it did on six.

**The class populations are where the factor still bites**, and the reason
is arithmetic rather than noise: a two- or three-shape bootstrap gives
an interval far narrower than the spread those shapes actually show. The run's
largest factor is `window` at **8**, with `reshape1` at 7 and `scaled` at 6
behind it, where Run 18's largest was `rev` at fifteen, Run 17's `revsome`
at nine and Run 16's `scaled` at twenty-three; the rest sit between three
and five, `rev` at four where it read fifteen the run before. So the factor
is reporting which slot happened to be disturbed rather than the reader's
arithmetic, and it does not stay with a class from run to run --- `rev` falling
from fifteen to four on a roster, a box and a basis binary that did not change
is this run's own demonstration of that. The class whose intervals cover 1 least
often is `bcastmid` at **10 of 18**, with `revsome`, `window` and `scaled`
at 13; `bcast` reaches 16 and `reshape1` 17. Read a class interval that misses 1
as the reader's arithmetic and the pair's own deviation as the finding;
the per-class factors are with each block below.

**And what is left when every other cause is pinned has now been measured:
run-to-run drift is a few percent per cell and a quarter of a percent
on a geomean.** Run 11 re-ran Run 10's aligned binary with shapes, roster, order
and regime unchanged --- the repetition this README had wanted since Run 9 ---
so its every movement is drift and nothing else. `list`'s per-shape scatter
is **0.958 to 1.043**; of 762 cells, 495 are within 1%, 693 within 5% and 743
within 10%; every arm's geomean is within 1.5% but `mut-odo`'s 1.0327.
That is the figure to hold a *later* margin against, and it is a quarter
of the 0.902-to-1.181 band Run 10 had to quote when the roster order moved
the layout underneath it. Two consequences worth keeping when the run file
carrying them is replaced: a margin of a few percent between two runs is still
not evidence, and a margin between two *arms* of one run has to clear
the six-pair figure of the half it is read on --- 0.49% on this run's basis ---
which is the A/A floor above restricted to the pairs that carry, and a different
quantity from the eighteen-pair floor. **Three figures are in play and they
answer three questions**: 2.32% and 1.71% are the widest an arm differs
from its own duplicate by on each half, net and over all eighteen pairs, 0.49%
and 0.29% are the same over the six pairs that carry back to Run 10 and so what
two rows of one table must clear, and 3.3% is the across-run drift band an arm
must clear to have moved between runs. **All three are the word *floor*,
over different populations, and two things that are not it wear it easily.**
A class's `floor` column is the same statistic again over that population's
eighteen pairs, so it is a fourth member of the family and not a fourth sense.
**The worst single A/A cell is not a floor at all** --- 19.75% on this run ---
and the procedure says so where it is read; it is one cell where
these are geomeans over a population, and quoting it as one overstates
the instrument by an order of magnitude. Nor is the residue [the alignment
question][open] asks about, which is an effect size that survived a control
rather than a spread the run measured. The exceptions are `build` and `mut-odo`,
one worker at two slots, whose cells reach 1.25 and 1.16 with their loops
at offset 0 in both runs --- the residue the pairing cannot reach, and [the open
list][open]'s.

**And a busy machine has now been measured rather than only avoided, which
is what says the wild cell is not one.** Run 11's sequence was launched twice;
the first attempt's max-skip main set completed before it was stopped,
on a machine that turned out not to be quiet, and its artifact was read against
the recorded one --- the same binary, the same roster, an hour apart --- before
being deleted with the rest. The disturbance is **diffuse**: the floor rises
from 0.22% to **1.11%**, **50 of 762 cells** run more than 5% slow,
and the worst of them are scattered over four shapes and eight arms (`build`
on `cnn-L2-24x24-c32` 1.161, `bq-odo-gm-mulback` on `stretch-square-1341` 1.147,
`mut-odo-vecdims` on `cifar-L2-16-c64-k3` 1.138), while every arm's geomean
stays inside 2% and the per-shape ranges widen to 0.758..1.161. **The wild cell
is the opposite signature in every respect**: one bench, its interval
a twentieth of a microsecond, its neighbours in run order and its own two twins
clean --- and in this disturbed run `lenet-L1-28-c1-k5/bq-expand` reads 1.0070,
so the shape and slot are not what carries it either. An intrusion smears;
this does not, which is why it is a finding and not noise.

**The wild cell went where the fix predicted, and came back somewhere the fix
does not reach.** Run 8 recorded `bq-expand`'s distant twin 44% slow
on `vgg-14-c512-k3`, Run 9 41.4% on the same arm and shape, and five filtered
probes ran it down to a cold block pool at that twin's roster slot. Run 10 moved
`sum-only-early` above `list`, so nothing is measured on an ungrown pool,
and that pair read 1.0043 with its worst cell 1.67% on a different shape ---
the three-bench probe that priced the fix at 0.24% reproduced over the whole
roster and shape set at full budget. **Run 11, on that same binary, carries
a 35% cell at `lenet-L1-28-c1-k5/bq-expand`**, with both of that arm's twins
clean, both time-neighbours clean, CI% 0.06 and `list` on the shape unmoved.
So what the roster fix removed was the *slot* --- a twin measured on an ungrown
pool --- and not whatever makes this family susceptible: the same arm, the third
run in four to carry a cell of this size, and this time at its own slot rather
than a twin's. Nothing here has been probed, the machine having been wanted
elsewhere; [the open list][open] carries what would settle it. The account
of the Run 8 and Run 9 cell, from those probes (2026-08-09, Run 9's own binary
and regime), stays because the mechanism is what the predictor below rests
on and because a recurrence is the reason to keep it:

**The wild cell's mechanism --- SPENT 2026-08-20, and it is a negative result
that excludes three mechanisms.** The trigger this entry names fired: Run 16's
worst A/A cell anywhere is 43.43% on `reshape1-500k` at `mut-odo-aa-distant`,
with its adjacent twin at 31.19% on the same shape, so `wildlog-a32m` went
to the `reshape1` class process rather than to `scaled`. One process, 141
benches, 12m08s, 21334 sample records. **Run 17 has since reproduced the finding
at scale and out of a recorded run**, at 74.48% on `revsome-inner-primes`
with allocation, heap and collector flat across a 67% mutator difference,
so what this probe established on one hand-run process the roster now
establishes on its own; the run file's head carries it. **The 43.43% cell did
not come back** --- `mut-odo-aa-distant`'s worst is 15.35% here and
on a different shape, its adjacent twin's 12.59% --- which is itself
the standing ruling holding: the magnitude does not repeat. What the per-sample
record settles is what the spread is NOT made of. Between an arm and its own
byte-identical duplicate on `reshape1-500k`: allocation per iteration
is identical to 0.01% (4007172 against 4007513 and 4007412 bytes), in-use heap
is flat at 92 MiB across all three benches and every sample of them, GC
is **0.03% of mut+gc** and no major collection falls inside any of the three
benches' timed windows, though the process runs 517 in all, 516 of them after
the logging began --- and mutator time still differs by **8.2%**, the two twins
agreeing with each other to 0.09% while sitting that far from the base.
The twins run at slots 9 and 15 and the base at 14, so they bracket
it in execution order and still agree with each other rather than with it.
**So the reshape1 A/A spread is not allocation volume, not heap occupancy
and not collector work**, which is every quantity the runtime can report; what
is left is where the code sits, and step 11's named fills bear on it ---
`mut-odo` and `build` share one loop body at two call sites. The caveat
is the instrument's own: this is the wildlog binary, whose patch moves `.text`,
so it characterises the class's hazard and not that one cell. What would settle
the residue is an address-level read, which this entry has always said costs
a fill per sample. The instrument, kept for the next time it is wanted:
the instrument is `wildlog-a32m` (2026-08-19): the basis recipe over a `Main.hs`
edit logging the RTS's allocated-bytes total with the GC and mutator clocks
beside it, one line per criterion **sample** --- a step inside one bench being
averaged away by a per-bench figure --- off unless `WILDLOG` is set
in the environment, proved firing and silent before the tree was restored,
and kept as `wildlog-instrument.patch` while Run 17's pair was live --- landed
in `Main.hs` by commit on 2026-08-22 once that pair was spent, so the patch file
is now the record of what Run 17's basis carried over its control and not a step
anyone applies. It hangs off criterion's `allocEnv` and `cleanEnv`, which
bracket the timed block from outside, and runs criterion's own `whnf'` loop,
so a logged arm executes the instructions every published bench does. Addresses
are not logged though the entry names them, and the code says why: the RTS
reserves its heap at a fixed base, so what moves is where within that arena
a buffer lands, which is what the allocation total says, and taking an output
buffer's address would cost an extra fill per sample --- perturbing the history
under test. **Riding both halves of the pair, which this heading asked for until
2026-08-19, is refused**: Run 16's basis registration is a repetition against
run15-a32m, the edit moves `.text` and every loop offset, so the bridge would
cross a layout change, and per-sample logging allocates. Run 17 puts it on ONE
half by decision of 2026-08-21 --- `run17-wildlog`, the basis, against
`run17-det` without it --- so the pair prices the instrument rather
than inheriting it ([What the next run compares
against](runs/run19.md#what-the-next-run-compares-against)). It was pointed
at the `scaled` class process, whose disturbance turns up in six runs of eight
where a wild cell is three of eight and none in the last four --- but **a wild
cell in Run 16's own A/A worst cell was the trigger** to spend the budget
on that process instead, and it fired, so `reshape1` took it. Neither instance
reproduces filtered --- measured both times --- so either probe is a whole
process and never a five-bench run. Its `perf` half still wants
`kernel.perf_event_paranoid` lowered by hand. **And Run 15 moves where to point
it**: the `scaled` slot's disturbance sat on `mut-odo-vecdims` for six runs
and this run finds it on `mut-odo`, `gen-unsafe` and `build` instead, all three
worst on `scaled-super-r3` --- so the instrument follows the shape and
not the arm. Both readings are with the wild-cell entry.

- It **reproduces deterministically**. The twin reads 4.46 ms in the run
  and 4.50 ms alone; the two adjacent copies read 3.315 and 3.314 ms in the run.
  Same code, same allocation, tight intervals on all of them.
- **The slow figure is the arm's real isolated cost, and the published one
  is the anomaly.** Run `bq-expand` in a two-bench process and it reads 4.52 ms
  --- the *distant twin's* figure, not its own published 3.32. So the twin
  at roster slot 3 is measuring the arm correctly and the arm at slot 29
  is being flattered by 26%.
- **It is the whole expansion family, not one arm.** Filtered into a small
  process, `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback`
  each read 35--40% above their published cells on this shape, while
  `bq-scan-rem-gm-mulback` (2.275 ms against 2.279) and `mut-odo-vecdims` (1.566
  against 1.570) do not move at all. Susceptibility is a property of the arm,
  and these are five more arms with it settled.
- **One single predecessor does all of it, and it is `sum-only-early`.** Six
  bisection probes looked for a cumulative cause and found none --- `list`
  first, `bq-gen` between, slots 4--16, 17--22 and 24--28 each left the arm slow
  --- because every one of them omitted the bench that matters. Put
  `sum-only-early` between the twin and the arm and `bq-expand` reads 3.347 ms;
  put `mut-odo-vecdims` there instead and it reads 4.583. Nothing else is needed
  and nothing else substitutes. `sum-only` times a sum over a *fixed* vector,
  so its setup allocates one `l`-sized buffer and then allocates essentially
  nothing per call --- a single large allocation that grows the block pool
  and leaves it grown, which is exactly [the position effect][pos-effect]'s
  mechanism and not code placement, the binary being identical throughout.

  **That made it a roster-order defect rather than a curiosity, and it is now
  fixed.** `sum-only-early` sat at slot 5 with the three distant A/A twins
  at slots 2, 3 and 4 --- *before* it --- so those three controls were measured
  against a colder heap than every strategy they exist to calibrate,
  and the only reason two of them looked fine is that they twin arms with too
  little excess allocation to care. A "distant" twin was therefore varying heap
  state as well as position, which is not what the crossed design says
  it varies. `sum-only-early` now runs at slot 2, directly after `list`
  and ahead of the twins; the reasoning, and why it stays *after* `list` rather
  than before, is at its roster entry in `Main.hs`.

  **Proven non-vacuous, as a fix to a measurement has to be.** The same
  three-bench probe that isolated the cause, re-run on the moved roster
  at the default nursery, puts the twin at 3.367 ms and its base at 3.375 ---
  **0.24% apart**, where the identical selection before the move read 4.53
  and 3.35. The 41% cell is gone, and gone for the stated reason rather
  than by any change to what the arms compute.
- **It is not GC time.** Under `+RTS -s` the cold two-bench process spends
  **5.8%** of its total time collecting (productivity 94.2%, 41 MiB in use)
  and the warm 34-bench one **2.3%** (97.7%, 60 MiB). Even abolishing collection
  outright in the cold process buys 5.8% against a 36% gap, so the cost
  is inside MUT.
- **The allocation area is what it turns on, and `-A32m` removes it outright.**
  This is the cold twin's cell and not the position ladder [the open list][open]
  registers for Run 15 --- same shape, `vgg-14-c512-k3`, other arm,
  and the nursery works the opposite way on each: a larger one cures
  this and creates that. `-H512m` does nothing (4.74 and 5.16 ms raw), so
  it is the nursery specifically and not the heap size. An eight-point sweep,
  all on this shape and all **net** of the forcing pass, with `mut-odo-vecdims`
  carried through as a control the predictor says must not move:

  The two left columns are criterion slopes on the **pre-fix** roster, where
  the twin was still cold, and are here to show it converging; being alone-leg
  slopes, the large-area rows carry the transient hazard [the position-term
  entry][open] records, which the differenced caller table below does not.
  The two GC columns are exact rather than normalised: taken at a fixed `-n`,
  every setting allocates the identical 41.066 GB, so the counts are directly
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

  **The gen-0 column is the method checking itself**: it falls as `1/nursery`
  at a constant 0.74 of the predicted count, that fraction being the large
  objects that bypass the nursery altogether. `-A1G` under the cap is the one
  row where it collapses to **zero** --- a 1 GB nursery the 2 GB cap will
  not let it fill, so the RTS does 31 major collections instead of minor ones.

  **What the sweep settles is the cold arm, not the warm one.** The twin
  converges on its arm from 32m onward --- 41% apart at the default, within 2%
  everywhere after --- so a large nursery is a second route to the state
  the roster fix now reaches: it spares the *cold* arm the pool growth rather
  than paying for it. Major collections confirm it deterministically. Re-run
  at a fixed iteration count, where every setting does identical work (41.066 GB
  allocated at all nine, which is the method checking itself), gen-1 collections
  read **255** at the default and **2** at every larger nursery
  but `-A1G`-under-cap, and gen-0 falls as `1/nursery` at a constant 0.74
  of the predicted count, the large-object fraction that bypasses the nursery.

  **It buys on a warm arm too, and the cost it removes is KERNEL time.**
  This took resolving, because two instruments disagreed and the losing one
  was mine. Criterion's slope put `bq-expand` at 2.795 ms net at the default
  against 2.501 at `-A32m` (quiet machine, three interleaved reps, spread
  under 0.4%), while differencing the process CPU at two iteration counts put
  the two level. Neither sample size nor GC interleaving explained it ---
  at `-L60`, where criterion's samples reach 839 iterations, its ratio
  is unchanged at 0.903. **What explained it is that `/usr/bin/time -f %U`
  reports user CPU only.** Split the clocks and the default's missing cost
  is in *system* time, 0.29 s at `-n 800` and 0.58 s at `-n 1600` --- perfectly
  linear, so **0.36 ms of kernel time per call** --- where `-A32m` pays 0.03
  and 0.04 s, which is fixed startup and nothing per call. Differenced on wall
  time the two instruments agree: 3.300 ms against 3.075. So the small nursery's
  price is memory-management work in the kernel, an arm allocating 13.2 MB per
  call beyond its result against a 4 MB area, and a user-CPU measurement cannot
  see it. The general lesson is worth more than the figure: **difference wall
  time, or user *and* system** --- a README rule inherited from horde-ad says
  "wall and user time agree on it", which was true of the workload
  it was written for and is false here.

  **The predictor called it, on a control shape** --- the excess-allocation rule
  stated in full below. `cifar-L2-16-c64-k3` has 1.59 MB of excess per call,
  below the 4 MB area, so it should show neither kernel time nor benefit.
  It shows neither: system time is 0.00-0.01 s at both settings and does
  not scale with `n`, and `-A32m` is if anything 6% *slower* there. Two shapes,
  opposite predictions, both confirmed.

  **`-A1G` is a cliff, and the cliff is the `-M2G` cap and not the nursery.**
  The arm reads worse than the *default* --- +20.3% by differencing ---
  and gen-1 collections go from 2 to 31 at identical work. Re-run at `-M8G`
  and it rejoins the others exactly (gen-1 back to 2). The high-water mark, 2318
  MiB, is the first in the sweep to cross `micro.cabal`'s 2048 MiB cap,
  and crossing it is the whole of the effect. So a large nursery
  is not intrinsically bad here; a large nursery *under this cabal file's heap
  cap* is pathological, and would also destroy the guard the cap exists for.

  **What a caller should run with is a different question, and it answers
  cleanly.** The suite's question is which setting measures best; a user
  of `Data/Array/Internal.hs` wants the cheapest real cost, which is wall time
  --- kernel work is cost to them --- with no `-M` cap in the way. Differencing
  wall time at `-n 400`/`-n 800`, `-M8G` throughout, on the shape where
  the effect is largest:

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

  **Everything from 32m to 1G is one price at this size, and 32m is the cheapest
  way to buy it.** The whole 6.1% is captured at 32m; above it the per-call time
  is flat and only the costs grow --- memory linearly, and a one-time kernel
  charge of roughly **1.2 s per GB** as the area is faulted in. That fixed
  charge is what makes a small-`n` measurement of a large nursery look
  catastrophic: divided over 100 calls it reads as half a millisecond each,
  and it is not per call at all. The gain also exists only where an arm's
  per-call excess outruns the default 4 MB, so on `cifar-L2-16-c64-k3` (1.59 MB)
  every enlarged nursery is *worse* --- 0.465 ms at the default against 0.480
  to 0.500 across the band. And `-A1G` is safe here only because `-M8G` removes
  the cap.

  **But "at this size" is load-bearing, and the advice inverts above the shape
  cap.** Real callers use arrays past `sizeCap`, so the `tooBig` shapes
  were promoted into the shape set behind a temporary edit and measured
  (2026-08-09, `-M20G`, busy machine, min of 5; the edit is reverted).
  Allocation first, which is exact and load-independent, and which confirms
  the one thing that does scale: **excess allocation is linear in `l` to three
  digits** over a 32x range --- `bq-expand` 14.6 to 14.7 B/element, `list` 190.2
  to 190.4 --- so at `imagenet-224-c64-k3` (`l` = 28.9M) a single call churns
  **425 MB** past its result, and `list` churns **5.50 GB**.

  | `-A`, at `imagenet-224-c64-k3` | `bq-expand` | its kernel time | `list` |
  |---|---:|---:|---:|
  | default | 113.5 ms | 13.5 ms | 1040 ms |
  | 32m | **134.0** | **31.0** | 637 |
  | 64m | 94.5 | ~0 | 603 |
  | 128m | 99.0 | 1.0 | 657 |
  | 256m | 99.0 | 1.0 | -- |
  | 512m | 100.0 | 0.5 | 603 |

  **`-A32m` goes from the best setting to the worst one** --- worse
  than the default, by 18%, on 31 ms per call of kernel time, and it reproduced
  in two passes. Whatever the 4 MB default does badly at this scale, 32 MB does
  twice as badly, and 64 MB stops doing it at all. The threshold therefore moves
  with `l` but **nowhere near linearly**: 32m suffices at `l` = 0.9M and fails
  at 28.9M, while 64m covers both --- a 2x nursery across a 32x size,
  not the 425 MB a "nursery must exceed the excess" rule would demand. That rule
  is refuted; what sets the threshold is not measured here.

  **Two more things the big shapes change.** The prize **grows** rather
  than shrinking with size --- 6% at `l` = 0.9M against 12-17% here, and ~40%
  for `list` --- so the guess that DRAM-bound behaviour would swamp
  the allocator at scale is wrong. And `bq-expand`'s margin over what
  it replaced narrows under a bigger nursery at *every* size measured, 9.2x
  to 6.4x here against 10.2x to 6.4x at `l` = 0.9M, which is the same effect
  at a 32x remove.

  **So, for a caller, this section said `-A64m` to `-A256m` --- and the decision
  of 2026-08-21 overrules it: every horde-ad test and benchmark runs at `-A32m`,
  as does every process here, and the area is not to vary again.** What the band
  had for it stands as measured: the default leaves 6-17% on the table above `l`
  ~= 1M, `-A32m` is actively harmful at the top of the range, and above 256m
  nothing improves while memory and startup keep growing --- busy-machine wall
  figures whose +-5% between neighbouring settings should not be read,
  the kernel-time column carrying the finding; and `-A1G`'s cliff in the sweep
  was `micro.cabal`'s `-M2G` cap and not the nursery, at `-M8G` it rejoining
  the others. What overrules it is the churn findings: the tax grows
  with the area, +44% at `-A1G` against +33% inside the band and about +13%
  at `-A32m`; `-A32m` is their recommendation for this workload class;
  and the alone-slope transient that makes criterion baselines untrustworthy
  without fixed-iteration differencing belongs to areas past the 32 MB L3 ---
  the last two are [the position-term entry][open]'s. So the caller takes
  the imagenet-scale kernel cost above in exchange for the tax it declines,
  and the regime Runs 14 and 15 were built to price --- the then prevailing
  `-with-rtsopts=-A1G -I0 -T -M8G`, Run 14 at `-A1G` and Run 15 at `-A32m` ---
  is nobody's here any more.

**So the mechanism is settled: an arm allocating more per call beyond its result
than the nursery holds pays for it in kernel memory management, and the default
area is 4 MB.** The first consequence is the one already acted on --- the roster
move, which warms every timed bench and takes the cell from 41% to 0.24%.

**The second is much larger and is not acted on: `list` is the most
nursery-sensitive arm in this README, so the published ratios are themselves
a statement about the default allocation area.** Its excess is predicted at up
to 353 MB per call, two orders above `bq-expand`'s, because a cons list of `l`
elements is nothing but small-object allocation. Measured on `vgg-14-c512-k3`,
quiet: `list` goes **28.659 ms to 16.019 ms**, a 1.79x speedup, where
`bq-expand` gains 10%. The ratios therefore do not cancel, they move hard ---

| on `vgg-14-c512-k3` | default | `-A32m` |
|---|---:|---:|
| `bq-expand` / `list` | 0.098 | **0.157** |
| `mut-odo-vecdims` / `list` | 0.036 | **0.065** |

**At a large nursery an earlier bench in the same process permanently slows
a later one --- and the condition is now named SMALL-PINNED CHURN, its cost
the churn tax: churn of sub-3276-byte pinned allocations, the shared-accumulator
size class.** Run 14's probes found it (2026-08-15/16): `vgg-14-c512-k3/list`
read 14.1 ms with nothing before it and 22.3 ms after certain shapes, the same
ladder was flat at `-A4m`, and the victim's added cost was mutator LLC misses
at flat instructions and dTLB --- the counter signature that has held through
everything since. **It is not the pinned-spray pool condition of GHC work item
27601**, by controls and by a conceptual objection that stands: on one machine
and one compiler `+RTS -H2G` removes that reproducer's penalty and leaves
this one whole, `max_mem_in_use_bytes` moves 2.7% here against a doubling there,
and that issue's mechanism needs rare collections to let block groups accumulate
where this condition's disturbance is full size at 4 MB and merely unpaid.
Everything reproduces on GHC HEAD, where that issue is itself unfixed. Run 15
was built to read the term at a caller's nursery, and the probe sessions
of 2026-08-17/18/19 resolved it; the account below is the summary,
and the measurements, their tables and the recipes to re-take them
are `small-pinned-churn-investigation/nursery-position-findings2.txt`'s.

**The resolution in one paragraph, the route split of 2026-08-19 folded in.**
One damaged state, two formation routes. An UPFRONT burst is class-selective:
churning pinned allocations of at most 3276 bytes --- the shared-accumulator
path, up to 406 doubles (the limit is compared in words), every Storable vector
being pinned at any size --- degrades every later `list`-like phase, while
the same burst of own-group objects (3600 B and larger) costs nothing; padding
the small results above the limit erases this route completely, +12% to +0.2%
at `-A32m` and +44% to +0.6% at `-A1G` on the fixed-n victim. The INTERLEAVED
route is class-free: any sub-threshold allocation, pinned or movable,
punctuating a victim builds the same state, dosed by cumulative bytes ---
and this route, not the class, is what a criterion process does to its later
benches: the corrected scans put all 23 candidates on one count-ordered curve,
log-linear until it saturates around a million calls, and a fully padded binary
reproduces the same curve. So there is no poison set, every shape is a victim
on its `list` --- around +14% at `-A32m` after one saturating in-process poison,
padded or not --- while among arms stable enough to read no other arm pays
(`offtab` and `build` cannot be read by single processes at all, their alone
legs spreading 10 to 21%). **What it costs this README**: `list` is every
published figure's denominator and runs in-process in every main run,
so the published absolutes sit above the shapes' clean alone rates --- roughly
uniformly ~14% at `-A32m` and a shape-dependent 0 to 10% at the default, now
measured directly against clean single-bench alone legs for every `list`
denominator, main set and classes (findings items 64/68) --- while within-run
ratios carry little of it, the crossed A/A twins bounding position bias
under a percent. No allocation policy reaches the in-process deflation; its outs
are single-bench processes or a GHC fix. A ~130-line base-only reproducer,
`small-pinned-churn-investigation/ReproSmall.hs`, shows both routes on 9.12.4,
9.14.1 and HEAD, the own-group upfront control at zero inside the same binary.

**Two standing rules and one boundary come out of it.** The instrument rule:
a big-churn bench's ALONE reading at an area past the 32 MB L3 is a fresh-heap
transient, not its steady state --- vgg's true alone rate at `-A1G` is 16.5
ms/iter where criterion's slope said 14.12 and its `mean` 20.99 --- so steady
state is read by fixed-iteration differencing, never an alone slope,
and the term's real `-A1G` size is +29 to +44% by victim, not the +56.5% once
quoted here. The tuning rule: the tax cannot be `-A`-tuned away --- +33%
at `-A64m` and at `-A256m`, +44% at `-A1G`, and only 4 MB-scale areas decline
to pay, at their own collector cost --- and the remedy is route-specific:
padding cures upfront bursts outright, no source-level policy reaches
the in-process route, so its outs are process isolation or a GHC fix; the issue
and its follow-up comment are staged in horde-ad's docs, nothing posted.
The former boundary is resolved: cifar's +10.2% at the DEFAULT nursery
was roster context over a ~+5.5% clean-pair tax inside the small-area band
(findings items 40b/51) --- small-area immunity was never strict anyway, a few
percent rather than zero (items 27/30).

**And the five shapes a bigger nursery helps are NOT this term --- that
is the correction the same probes force.** The victim runs 1.74x faster at 32 MB
with nothing before it at all, so its main-set gain is steady state
and the ladder runs the other way. What selects the five is generational
promotion, and the chain is span, promotion, copying, time. Each shape has
a **live span** --- the size of the intermediate structure that is still
reachable when a collection fires --- read off as the nursery at which
its promotion collapses: 4 to 8 MB for `stretch-pow2stride`, 32 to 64 MB
for `stretch-r5-8x432` and `stretch-inner256`, past 64 MB
for `stretch-bigstride`, nothing for `stretch-wide-2xM`. Below the span
the structure is promoted at every minor collection --- 979 KB per minor at 4 MB
against 357 bytes at 32 MB on `stretch-pow2stride`, a 2700-fold collapse, where
`stretch-wide-2xM` reads about 225 bytes at both. **Promotion is the copying**:
6.15 GB against 4.6 MB done by majors, and `-hT` names it ARR_WORDS with nothing
else above kilobytes. A major fires per **20.9 MB promoted**, the generation-1
growth budget, which is why total-copied-over-majors reads as a constant. Time
follows copying at **0.42 ms per MB**, agreeing to 0.4% across
`stretch-pow2stride`, `vgg-14-c512-k3` and `alexnet-L2-27-c48-k5`, whose
promotion goes to nothing by 32 MB; `stretch-tall-Mx2`'s loss runs the same way
at 0.4663, 11% off.

**So the nursery has two opposing effects and this README had them entangled**:
collector copying falls with the area, worth up to 1.96x, while the churn tax
rises with it, worth +29% to +44% of the true steady state. A shape's net
is whichever dominates, which is why no single property selected the five.

**Swept over all 24 shapes, and the answer is one positive and one negative**
(2026-08-17, `+RTS -A` at six areas from 4m to 128m, one binary, no build).
**Only eight shapes promote heavily at all**, and they are exactly the eight
with a finite span: `stretch-bigstride` and `stretch-tall-Mx2` at 128 MB,
`stretch-r5-8x432` and `stretch-inner256` at 64, `vgg-14-c512-k3` at 16,
and `stretch-pow2stride`, `alexnet-L2-27-c48-k5` and `stretch-coprime-r7` at 8.
The other sixteen never exceed a few kilobytes per minor at any area, so they
have nothing to win from any nursery and only ever pay its mutator cost ---
which is the whole of why the main set's gainers are so few. **And the span
predicts the gain**: the five that gained at 32 MB are all drawn from the six
with a span at or under 64, the gain scaling as the area approaches it, while
the two at 128 gain nothing there.

**What no structural property predicts is the span itself.** Size correlates
at Spearman +0.893 and does not determine it: `stretch-pow2stride`,
`stretch-r5-8x432` and `stretch-bigstride` all have `l` near 1769472 and spans
of **8, 64 and 128 MB**, a sixteenfold spread at one size. Over ten candidates,
rank reads -0.607, the innermost footprint +0.750, the largest dimension +0.786,
and both `m` and the base-offsets size about zero --- `stretch-tall-Mx2` has `m`
= 2 and the largest span, `stretch-pow2stride` `m` = 27648 and the smallest.
The span-over-result ratio runs 0.57 to 8.89. So the span is the quantity
that matters, it costs two `-S` runs and no build to measure for any shape ---
the sweep behind this paragraph, 144 processes no run artifact holds,
and its analysis are tracked
as `small-pinned-churn-investigation/span-sweep-run15.txt`
and `small-pinned-churn-investigation/span-correlate.py` --- and it is
**not a function of the view's shape parameters** --- which is where
this question now rests, and it is a measurement to take per shape rather
than a formula to look for.

**RETRACTED, and with it this entry's oldest claim: there is no measured poison
SET, in this run or in Run 14.** A scan run on 2026-08-17 read six shapes
as poisoning `vgg-14-c512-k3/list` at `-A32m` --- `cnn-slice-c32` 18.70,
`cnn-L1-6x6-c1` 18.69, `lenet-L1-28-c1-k5` 18.32, `cnn-L1-24x24-c1` 18.28,
`cifar-L2-16-c64-k3` 17.57, `cnn-L2-24x24-c32` 17.52 --- against seventeen
"innocents" inside 16.42 to 16.64. **Criterion runs benches in ROSTER order
and not in the order the `-m glob` patterns are given**, and the roster puts
those six at positions 1 to 6 with the victim at 7. So the six are exactly
the shapes that *can* precede the victim, and in each of the other seventeen
processes the victim ran FIRST --- those readings are victim-alone baselines,
which is why they cluster just under the 16.67 alone-figure instead
of scattering around it. **Seventeen of the twenty-three candidates have never
been tested as poisons at all.** What survives is that the six which do precede
the victim all poison it; what does not survive is any statement about which
shapes do not, and with it the identity-permutation clue,
the `conv1d-24`-against-`cnn-L1-24x24-c1` pairing this entry has named for two
runs, and a three-condition rule that was perfectly confounded with roster
position. **Run 14 has the same defect**: its probe notes --- superseded
by `small-pinned-churn-investigation/nursery-position-findings2.txt` and removed
--- recorded the victim as "24th and last" where the roster puts it 7th,
and that run's innocent readings show the same clustering just under its own
alone-figure. **The corrected experiment** --- the victim taken from the END
of the roster so that every candidate precedes it --- **is the scan above.**

**What the term is NOT is collector work, and the account that says
so was tested and failed.** The account tried was that a poison leaves
a retained heap the victim's collections then copy, and every part of it failed.
The ~22 MB live during the victim's phase is the victim's OWN live set, present
at the same 21.8 MB with nothing before it. The poison does not add major
collections but *removes* them, 97 in the poisoned process against 103 and 112
in unpoisoned ones. And majors copy 72.9 KB apiece here, the retained bytes
being large objects a copying collector does not move, so the extra copying
over the whole process is 6.9 MB. At the measured 0.42 ms per MB that predicts 3
ms where the observed cost is some 650 ms, off by two orders. Split directly, GC
time is 0.043 s alone against 0.059 s after and the whole difference
is **mutator** time, which is where Run 14 left it with its LLC-miss and IPC
readings. So the two nursery effects are independent as well as opposed: one
is copying, the other is what a resident footprint does to the mutator.

--- so on this shape `bq-expand` beats the fallback it replaced by 10.2x
at the default area and 6.4x at 32 MB. **Both are true; they answer different
questions.** The default is what a GHC program gets unless it says otherwise,
so the published column is the right one for "what does a caller see today",
and this README has only ever measured that. What it is *not*
is a nursery-independent property of the two algorithms, and the headline ratios
should not be read as one. Quantifying it over the whole table is a run,
not a probe: one shape is not the geomean, and the small shapes --- where every
arm's excess is under 4 MB, as the `cifar` control shows --- will move nothing.
**Those runs are Run 14 and Run 15**, whose control halves carry `-A1G`
and `-A32m` against bases identical to them but for the allocation area. Run 15
answers the quantification: over the whole table the baseline moves **5.13%**
and every ratio with it, so the two halves' `time` columns are not subtractable
and the arm-by-arm reading is the one to use --- which is now the standing rule
for every pair that varies the area, [stated
under the yardstick](runs/run19.md#what-the-next-run-compares-against),
those runs' own files having since been replaced.

**The predictor, recorded before the run that would test it.** What decides
whether an arm feels the nursery is not its total allocation but its allocation
**in excess of the result buffer**, `(alloc - 1) x 8l`: the result is one large
object and goes straight to the large-object list, bypassing the nursery, while
the excess is the part that churns through it. On the six arms whose
`vgg-14-c512-k3` behaviour is already measured the rule separates them outright,
and the line falls on the nursery itself --- affected at 11.2 to 13.2 MB
of excess (`bq-expand` and its two output variants, `bq-odo-gm-mulback`),
unaffected at 2.4 MB (`bq-scan-rem-gm-mulback`) and 0 (`mut-odo-vecdims`). Total
allocation does *not* separate them, putting an unaffected arm at 9.6 MB
and an affected one at 18.5 MB with no line between that means anything. Applied
to the kept Run 9 cells the rule predicts **131 of 782** cells move,
concentrated on the large shapes, and names **14 arms that should not move
on any shape** --- the whole `mut-odo-vecdims` family, `build`, `mut-odo`,
`gen-quotrem`, `gen-unsafe` and both `sum-only` halves. Two consequences worth
having in writing before the measurement. `list` itself is predicted affected
on 17 shapes, by up to 353 MB of excess, so **the baseline is expected to move
and every ratio with it** --- which is most of the case against adopting
the flag casually. And `build` and `mut-odo` are both predicted *unaffected*,
so their 1.13x gap should survive `-A32m` untouched; if it collapses instead,
this predictor is wrong and what this README calls placement is really
the allocator. **Run 14 and Run 15 are the runs that test all of this**, over 24
shapes rather than the one it was built on --- Run 14 at `-A1G` and Run 15
at exactly the `-A32m` named above. **Both refute the same half of it, and both
confirm the other.** The rule named nine arms on this roster that should move
on no shape --- the five `mut-odo-vecdims` variants, `build`, `mut-odo`,
`gen-quotrem` and `gen-unsafe` --- and every one of the nine moved at `-A1G`
and moved again at `-A32m`, from `build` at 0.9775 to `gen-quotrem` at 0.7760.
What it got right is `list`: predicted affected, and expected to carry every
ratio with it, which is what 32 MB does. And `build` against `mut-odo`, the pair
whose 1.13x gap the rule said would survive untouched, had already gone before
either variable was applied --- 1.0171 on Run 14's basis and 1.0181 on Run 15's
--- so that control was ill-posed rather than a refutation of the predictor.
**The two settings are not interchangeable tests of it**: they agree at `l` ~=
0.9M and part company at the top of the range, where 32m turns actively harmful
and 1G does not, so `-A1G` is the stronger test of the same predictions rather
than a substitution for `-A32m`, and the two runs together cover the range
the single-shape sweep found.

**And the eight class populations, which that count left out** (2026-08-09,
the same arithmetic over the kept JSONs; it reproduces the main set's 131 of 782
exactly, which is what makes the rest worth quoting). `list` crosses the nursery
in **every** population, so no class table divides by an unaffected baseline ---
336 MB of excess on `bcast-tall-Mx2`, 118 on `reshape1-500k`, 34 to 81
elsewhere. The strategies cross in three classes only, `bcast` (24 cells of 96),
`reshape1` (17 of 64) and `window` (10 of 66); in `bcastmid`, `rev`, `revsome`,
`scaled` and `slice` nothing but the baseline does. So those five are penalised
in one direction throughout, which leaves their orderings alone and their levels
flattered, while the three are penalised unevenly and are where a nursery A/B
would move a table.

**That second half was tested the same day and the prediction holds.** Both arms
plus a `sum-only` half, filtered over all 24 shapes, run twice from one binary
with the nursery as the only difference (2026-08-09): the pair reads **1.1604**
at the default and **1.1433** at `-A32m`, each at three wins of 24 and sign p
0.00028. The gap does not move. Nor do the arms themselves, 1.028 and 1.043
in absolute time across the change, against the 35--40% the excess-allocating
arms show. Two things follow. The predictor survives a test it could have
failed, on the side where failure was cheapest to detect. And **the placement
question is now confirmed independent of the allocator**, so the pad probe
was unavoidable rather than possibly-subsumed: this pair's 1.16x
is not filtering either, the full run reading 1.13x over the same shapes with 31
benches between the two arms.

**So position reproduced after all, and much larger than the twins price it.**
Run 7 read the distant twin above the adjacent one within every strategy
and growing with span; Run 8 read that as not reproducing. Run 9 says both
were looking at a summary of the wrong thing. Aggregated over shapes the effect
is nothing --- three of Run 9's six pairs sit *below* 1 --- while on one shape
and one family it is 35--40%, which no geomean over 24 shapes can show.
The standing advice survives and sharpens: `list` runs in the coldest slot, arms
far down the roster are **flattered** rather than penalised, and now there
is a measured case of by how much.

**What did turn up is a bigger placement effect, from an accident.** `build`
and `mut-odo` compile to the same worker --- checked in Core at -O1 and again
under `-fspec-constr`, the dumps being [the mutable ceiling][ceiling]'s, which
is where that identity is kept --- so they are a seventh known-true-ratio-1
pair, and they disagree by 1.24x on Run 7, 0.86x on Run 8, **1.13x** on Run 9 (3
wins of 24, sign p 0.00028) and 0.95x on Run 10's unaligned half. Four runs, two
of them differing from their predecessor in the roster alone, and the pair spans
0.86 to 1.24: that range is the instrument, and it is 44% wide for code
that is identical. The twins share one worker called from two slots; those two
are separate copies of one worker at two addresses, and the gap between what
the two instruments read is the part of layout the twins cannot see. Do
not price a margin between distant rows at the twins' floor. **Aligning both
copies shrinks the instrument rather than zeroing it**: on Run 10's aligned half
the pair reads 0.9685 with both copies at offset 0, so about 3% survives the one
intervention that removes the whole difference the table above attributes
it to --- and the sign test ties there, 16 of 24, where every unaligned reading
of this pair has been lopsided.

**And those two addresses now have a candidate consequence, read out
of the binary** (2026-08-09, `-fspec-constr`). The innermost run-fill is 28
bytes --- seven instructions and a backward branch --- and the binary carries
four byte-identical copies of it, two per arm, the only alignment directive
anywhere in either procedure being `.align 8`. One copy per arm
is the mismatched-length `fail` join and cannot run on a well-formed shape;
the copies that do run are `mut-odo`'s at byte 29 of its cache line, which fits,
and `build`'s at 53, which straddles two. The dead copies fall the other way
round, which is why the pair looks like a wash until the executed one
is identified. That is one bit against one gap, so it was a candidate and
not an account --- but one the pad probe could test, nothing pinning these loops
to a line: pad in eight-byte steps until `build`'s executed copy lands whole
and see whether the gap goes with it. It did --- the confirmation is below
the loop table. The instrument is steady meanwhile, the flag's 12 KiB of `.text`
reproducing to the byte on a base the arms written since have grown.

**And a second family reads the same way, which is what takes it past one
point.** The four `mut-odo-vecdims` arms carry one copy each of that same
28-byte fill, the FastReshape three differing from their control nowhere inside
it ([the mutable ceiling](#the-mutable-ceiling-taken)), so their copies stand
beside `build`/`mut-odo`'s. **Every ratio is the row's arm against its family's
control** --- `mut-odo-vecdims` for the four arms under it, `mut-odo`
for `build` --- which is why the two control rows have no ratio of their own
and read `--` in all three: a control against itself is 1 by construction
and says nothing. The offsets are the executed copy's, read
with `loop-offsets.py`:

| arm | loop | mod 64, Run 9 | Run 9 ratio | mod 64, Run 10 | Run 10 ratio | aligned ratio |
|---|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | 28 B | 24 | -- | 16 | -- | -- |
| `mut-odo-vecdims-add-in` | 28 B | 40 | 1.1552 | 0 | 0.9937 | 1.0009 |
| `mut-odo-vecdims-add-out` | 28 B | 44 | 1.1795 | 36 | 1.1266 | **1.1612** |
| `mut-odo-vecdims-add-both` | 28 B | 44 | 1.1645 | 36 | 1.0906 | **1.1184** |
| `mut-odo-vecdims-add-both-down` | 24 B | 33 | 1.0183 | 29, 5 | 1.0149 | 1.0527 |
| `mut-odo` | 28 B | 29 | -- | 53 | -- | -- |
| `build` | 28 B | 53 | 1.13 | 45 | 0.9532 | 0.9685 |

The count-down row is the one whose loop is not the 28-byte fill,
so `loop-offsets.py --len 24` is what finds it, and its group has two copies
with neither attributed to a call path: 29 and 5 in `micro-unaligned`, both at 0
in `micro-aligned`. Which of the two executes does not matter to the question
this table asks, since a 24-byte loop fits inside a line at both 29 and 5,
so that row is resident in every binary here.

**On Run 9's binary every copy that fits inside one line read level or ahead
and every copy that straddles read 13--18% behind, with no arm of either family
dissenting. Run 10 splits that.** Its offsets come from `loop-offsets.py`
over the two binaries, so the mod-64 column is read and not inferred,
and the aligned column is a build in which all ten copies the table covers sit
at 0. `build`/`mut-odo` behaves as the hypothesis says throughout --- both
copies straddle in `micro-unaligned` at 45 and 53, both are resident
in `micro-aligned`, and the pair goes from Run 9's 1.13 to 0.9532 and 0.9685.
`add-in` behaves as it says too, and twice over: its copy is resident in *both*
Run 10 binaries and the ratio is 1.00 in both, where Run 9 had it straddling
at 40 and reading 1.1552. But `add-out` and `add-both` are resident at 36
in the unaligned half and at 0 in the aligned one, and they read 1.1266
and 1.0906, then **1.1612 and 1.1184**. Four placements each, none of them
straddling, and the penalty does not go. So the correlation inside Run 9's
binary was real for one arm of the family and coincidental for two, and what
those two cost is not layout --- it is read in [the mutable ceiling][ceiling],
whose suspension of those figures this withdraws. The count-down form sits
in the table for completeness, resident throughout and so with nothing to say
about straddling either way, and is read in its own section.

**A third placement of the pair, taken the same day, says what the residual
is** (2026-08-11, `-fspec-constr`, one filtered pass, `*/build` and `*/mut-odo`
over the shape set, 48 benches in each process, the two arms adjacent so each
ratio is formed inside one process). The `-fproc-alignment=64` build below puts
*both* executed copies at 53 --- the same offset, both straddling --- where
`micro-unaligned` has them at 45 and 53 and `micro-aligned` at 0 and 0:

| binary | the two copies | `build`/`mut-odo` | 95% CI | sign test |
|---|---|---:|---|---|
| `micro-unaligned` | 45 and 53 | 0.9585 | 0.9347..0.9813 | 18/24, p 0.023 |
| `micro-aligned` | 0 and 0 | 0.9782 | 0.9498..1.0054 | 12/24, **p 1** |
| `micro-procalign` | 53 and 53 | 0.9893 | 0.9703..1.0091 | 16/24, p 0.15 |

**Whenever the two copies share an offset the pair ties, and when they do
not it does not** --- and that holds at a resident shared offset
and a straddling one alike, which is what layout-neutral-by-construction
predicts and what no earlier reading could separate. **What this cannot do
is rank the two same-offset builds.** Their intervals overlap heavily
and the two tests disagree about which is nearer level --- the shim's build has
the flatter sign test and the flag's the point estimate nearer 1 --- so 0.9782
against 0.9893 is not a difference one filtered pass resolves, the same binary
moving by about as much between a filtered reading and a full-roster one (0.9782
against 0.9685). Procedure placement, which aligning loop *heads* does
not control, therefore stays a candidate for the residual rather than a finding.
What the probe does settle is that no placement of these two copies leaves them
more than about a percent apart once they share an offset.

**Which arm owns a loop copy: answered, and the answer is that a binary can
carry its own names.** Run 12's second prediction had to record that tying
a named arm to a named offset was not licensed, every `Main` copy printing
under one mangled symbol because these arms compile to one worker. A `-g3` build
carries what is missing --- GHC emits a per-block symbol with DWARF line info
--- and `loop-offsets.py` now reads it without help: `addr2line` for the source
line, the source file for the top-level binding that line falls in, so a copy
prints as `fbMutOdoVecdims` with the source line beside it instead of as one
worker's mangled name. A binary with no line info prints exactly what it printed
before. Read that way on 2026-08-13, at `-fspec-constr` with `LOOP_MAXSKIP=1`,
the four-copy vecdims group is, in address order, `mut-odo-vecdims`, `-add-in`,
`-add-out` and `-add-both`, and the pair beside it is `mut-odo` then `build`.
That is the order the loop table below assigns its per-arm offsets in,
so that table's ordering is now a measurement; and a second route agrees,
emission order tracking first reference from `roster`, which lists those four
in exactly that order. What it bought is at Run 12's second prediction above:
Run 11's split crosses the resident copies rather than following them.
**The recommended next step is taken and its prediction is refuted**
(2026-08-14, an unconditional build and a max-skip build from one source read
with `loop-offsets.py`, against Run 11's two kept main sets). The unconditional
form puts 100 of 100 Main self-loops at offset 0 where max-skip puts 58 of 113,
and **neither leaves a straddler**, so what padding every head buys is padding
that nothing needed. Per arm it buys `build` alone, at 0.9896, and costs
the tail up to 5.9% --- `bq-mut` 1.0588, `mut-odo-vecdims-add-out` 1.0513,
`bq-gen` 1.0504, `-add-both` 1.0333, `gen-unsafe` 1.0327, `gen-quotrem` 1.0275,
`offtab` 1.0259, `mut-odo` 1.0221. The arms that do carry a head max-skip
skipped land on both sides of 1, `build` against `mut-odo`, and the three
largest losers carry no tracked 28-byte loop at all, the tracked set being
`fbBuild`, `fbMutOdo`, `fbMutBaseOffsets` and the four vecdims fills. **What
the two forms differ in beyond offsets is a census**: the unconditional pads sit
inside enclosing loops and push thirteen of them past the 64-byte window, 113
self-loops falling to 100 and the 28-byte set 36 to 32. That is a cost
of padding every head which the offsets alone do not show, and it is the better
candidate the refuted prediction leaves behind. **And the step's own phrasing
named a difference that is not there**: the two forms emit *the same 395
directives at the same heads*, on the same assembly lines, differing only
in the max-skip budget written as each directive's third operand --- a median 33
bytes of slack, four heads with none --- so there are no per-form head lists
to compare, and the 27 extra heads on record are look-through's rather
than the unconditional form's. What the unconditional form spends is 8192 bytes
of `.text`, 20385989 against 20377797. **And the step's other half could
not have been taken at all**, which is a dependency neither entry declared:
attributing heads to arms wants `addr2line`, `addr2line` wants DWARF,
and the naming entry above measures DWARF changing the code --- a plain build
holding two copies of a loop per function where the twin holds one,
so the offsets-to-arms map is one-to-many in exactly the binary being timed.
A plan resting on an instrument should say what the instrument is known
to change. **And the instrument the residue wants now exists**:
`loop-offsets.py --len 0` widens the grouped, named report from the 28-byte
run-fill to every loop a cache line can hold, which in Main's own code is 112
loops over twenty lengths against the nine of one length the tracked set saw ---
so the arms that lose most under the unconditional form, and carry no 28-byte
loop at all, are visible to whatever asks next.

**And the map does reach the timed binary, which is the question a twin
raises.** The two builds are one source, each of the plain build's four vecdims
copies sits within 192 bytes of exactly one of the `-g3` build's, and matching
them by the normalised instruction window around each head --- mnemonics
with every displacement and immediate masked, the loop bodies themselves being
identical --- is a bijection that agrees with both: 74 and 75 of 80
for `-add-out` and `-add-both` against a runner-up of 38, and 73
for `mut-odo-vecdims` and `-add-in` against 70, those two arms differing
in almost nothing but the add. `-add-both-down`'s 24-byte loop matches the same
way at 75 against 3, and sits at offset 0 in the timed half, so today's basis
recipe has the five at 24, 8, 0, 0 and 0. **The same matching says nothing about
the `build`/`mut-odo` group**, every score there falling to 10 to 13 of 80
because `-g3` restructured that region when it dropped the two dead copies; what
names those two is `addr2line` on the twin's survivors and the entry order
already in the docstring. So the window method proposed as the fallback works
where the code is stable and is silent where it is not, which is worth knowing
before it is leaned on.

**Run 13 exported its own and found the twin's fidelity is a per-GROUP property,
not a per-binary one.** The same method names the vecdims four again --- offsets
24, 8, 0 and 0 going to `mut-odo-vecdims`, `-add-in`, `-add-out`
and `-add-both`, in that order, on both halves --- and the bijection is cleaner
than Run 12's, every timed head matching its own named counterpart at exactly
1.000 on the basis half against a runner-up of 0.921 or less. The other tracked
group, `[11, 0, 4, 0]`, it cannot name at all: all four copies share one
byte-identical body, that body is the `fbMutOdo`/`fbBuild` worker the two arms
compile to, and **the `-g3` twin carries only two copies of it where each timed
binary carries four** --- counted over `.text` in all four binaries.
With no third or fourth name to give, the window match degenerates to near-ties
an order below the vecdims group's. So the standing ruling that `-g3`
is a different program bites group by group: count a body's copies in twin
and timed binary before trusting the twin's names, which the vecdims group
passes four against four and this one fails. Run 13's figures are in its pair
note, which goes with its binaries.

**A build with both, and an instrument that does not cancel** (2026-08-11,
`-fspec-constr`, `*/build` and `*/mut-odo` over the shape set, 48 benches
a process). `micro-both` carries the shim *and* `-fproc-alignment=64`, so all
eight fills sit at 0 inside procedures pinned to 64 --- the build [the open
list][open] asked for. Its pair ratio ranks nothing: 1.0001 and 0.9820 over two
passes against the shim alone's 0.9921 and 0.9695, where each build's own passes
differ by 1.8 to 2.3%. That is the pair ratio's nature, dividing two arms
that share a penalty. The absolute per-arm reading does not cancel:

| against `micro-aligned` | its two copies | `mut-odo` | `build` |
|---|---|---:|---:|
| `micro-procalign`, the flag alone | 53 and 53 | 1.1167 (1/24) | 1.1294 (2/24) |
| `micro-unaligned`, phase-matched | 45 and 53 | 1.1061 (2/24) | 1.0839 (3/24) |
| `micro-both`, the shim and the flag | 0 and 0 | 1.0163, 1.0319 (6, 4/24) | 1.0246, 1.0451 (9, 7/24) |
| `micro-aligned`, its own second pass | 0 and 0 | 1.0025 (13/24) | 0.9797 (14/24) |

**The count is shapes of 24 where the row's build is faster.** So a shared
straddling offset costs both arms 8 to 13% while leaving their ratio level ---
the flag removes the variance, not the cost --- and shim plus flag costs 2 to 4%
over the shim alone. **Indicative only**: one pass a row against that same
repeat spread, times uncorrected, and only `micro-unaligned` phase-matched
to the basis. That row is what says the instrument works, reading 1.11 and 1.08
where Run 10's full budget read 1.16 and 1.14. Keep these out of the table
above, which is one pass per binary of a different quantity.

**The probe has since confirmed it, and found the penalty graded** (2026-08-10,
`-fspec-constr`, eight binaries differing only in inert pad arms, two
interleaved passes over the shape set, no rebuild anywhere in it; the tables
are here, the scratch directory being gone). Each arm was stepped through all
eight 8-byte offsets with code, membership and bench order fixed, so each
is a reading of one penalty in its own right: `build` runs **1.169x** slower
where its executed copy straddles and `mut-odo` **1.162x**, every straddling
placement of an arm slower than every resident one. The discriminating pair
inverts as predicted --- 0.874 where only `mut-odo` straddles, 1.102 where only
`build` does. And the penalty turns on *where* the split falls, which no reading
inside one binary could have shown: offsets 37, 45 and 53 cost 1.19 where offset
61, three bytes short of the boundary, costs 1.10 --- which is why the one
control with both arms straddling reads 1.069 instead of level, `build` at 53
paying full where `mut-odo` at 61 pays half. Evaluated at Run 9's own offsets
those penalties give 1.144 against the 1.13 it read, on a binary not among
the eight. The binaries differ in placement and in nothing else: fitted
allocation agrees to 1.000008 across the sixteen runs, and the subtracted
forcing term spreads 1.0046 where the arms spread 1.20. So the table above
stands, and the 13--18% it spans is the distance between a deep straddle
and a resident copy rather than a range still to be explained.

**What that span bounds is every margin under about a fifth --- in an unaligned
build.** The per-offset figures run 0.9040 at offset 13 to 1.1051 at 37, so one
loop's placement is worth **1.22x** best to worst, and that is the number
a margin has to clear rather than the 1.169. Two rows of the Results table
differing by less can be layout entire *in such a build*, and the A/A twins
cannot see it: they call one worker from two slots, executing one copy at one
address, where `build` and `mut-odo` are two copies at two. **An aligned build
removes that variance rather than bounding it**, every short loop of Main's code
sitting at offset 0, so a margin read there does not have to clear 1.22 ---
which is what makes the aligned half the place to adjudicate, and why a margin
agreeing across the two halves is evidence where either alone is not. Two limits
on that. It reaches only the loops the shim reaches, Main's and
not the libraries', so `list`'s own hot loop is outside it. And attribution
is per arm and exists for six of them, so for any other pair this is a statement
about the population of loops rather than about that pair's own. Reading
the offsets is minutes of `objdump` against a quiet-machine window, so it
is the cheap first question about a gap this size. `loop-offsets.py` beside
this file finds the copies structurally --- a backward branch whose target
is one loop length back, grouped by raw bytes, so "byte-identical copies"
is read rather than assumed --- and it was proved non-vacuous by reproducing
three of the probe binaries' documented offsets before it was pointed
at anything new.

**But the table corrects only where the loop is the same code; elsewhere
it screens.** As 0.98 x pen(A's offset) / pen(B's offset) --- the intrinsic
ratio being 0.98 and not the 0.9973 the probe's balanced design gave, which Run
10's gate settled against it (see the open list) --- it reproduces the eight
binaries to a median 1.0% and a worst 3.8%, Run 9's pair to 1.144 against
the 1.13 read, and the FastReshape three to 1.18 against 1.155--1.180.
Its resolution floor is the 5.9% by which the two arms disagree at offset 13,
so it settles a 17% gap and cannot touch a 5% one. And it reaches the six arms
carrying this fill and no others: dividing layout out of two *different*
algorithms needs each one's own penalty curve, which only stepping that arm's
address supplies. Everywhere else this is a quantified caveat, not a correction.

**GHC's native backend aligns no loop, and every other compiler to hand does**
(verified 2026-08-10 on this machine). GCC 13.3 at -O2 emits `.p2align 4,,10`
at each loop head, on by default as `-falign-loops=16:11:8`; clang 18 emits
`.p2align 4` above every block LLVM marks an inner loop header, with nothing
asked for. GHC's NCG emits `.align 8` at procedure starts and nothing inside
them --- on 9.10.3, 9.12.4, 9.14.1 and HEAD (10.1.20260803) alike,
and `-fproc-alignment=64` adds none of it either --- which is what leaves
this loop wherever it falls. The exposure follows: at 8-byte alignment three
or four of the eight reachable offsets straddle, four of eight for this one;
at 16 bytes one of four; at 32 or more none at all, a 28-byte loop starting at 0
or 32 ending inside its line either way.

**An isolated reproducer prices the same effect at 1.58x, and names what
it needs to appear** --- horde-ad's `docs/ghc-issue-no-loop-alignment.md`, filed
as [GHC work item 27668](https://gitlab.haskell.org/ghc/ghc/-/work_items/27668),
which is where this belongs written up and which cites this benchmark for what
`-fproc-alignment=64` does in a larger program and what the correction costs
there. A 23-byte loop stepped through all eight 8-byte positions of a line runs
0.256 to 0.261 ns an iteration at the six that keep it whole and 0.410
at the two that divide it, alike on the four compilers. Two things that adds
here. It is outside this harness entirely --- no criterion, no shape set,
no forcing term --- so the pad probe's verdict no longer rests on one
instrument. And it names the condition: that loop carries four independent
accumulators and is fetch-bound, where the first attempt at the reproducer used
one accumulator with each iteration waiting on the last and measured
**no** difference at any position. So a straddle costs where the processor
is fetching ahead and is free where it is waiting --- a sharper statement
of scope than two arms here could reach, and a candidate for why 1.19 here
is smaller than 1.58 there, the run-fill copying memory rather than only adding,
though nothing here measures that.

**Its LLVM backend does align them, which makes this a backend choice rather
than a property of the compiler.** `-fllvm` emits that same `.p2align 4` above
the inner loop header, on all four of those compilers,
and `-optlc -align-loops=64` (bytes)
or `-optlc -x86-experimental-pref-innermost-loop-alignment=6` (log2) raises
it to 64, each checked by reading the directive that came out. Read it rather
than trusting it: these feed a heuristic,
and `-x86-experimental-pref-loop-alignment` at 5 and at 6 gave 64 and 4 bytes.
What it would cost is a whole regime, `-fllvm` being a different code generator
that no figure here would survive; what it would buy is the first regime
in which layout is controlled rather than measured around, and in which
the identical-code pair must read 1.00.

**`-fproc-alignment=64` pins the offsets, which is the instrument fix**
(2026-08-10; the pad0, pad1 and pad2 sources rebuilt with and without it
and the offsets read out of the binaries --- a claim about layout, so no quiet
machine is involved). Without it the four copies walk 24 bytes a pad:
`[3, 53, 59, 45]`, `[27, 13, 19, 5]`, `[51, 37, 43, 29]`. With it all three
builds read `[3, 53, 3, 53]`, and the `mut-odo-vecdims` family `[8, 8, 4, 4]`.
A membership change no longer rerolls layout, which is the confound that made
Run 9's question unanswerable and this probe necessary. It does more than pin
them: the two procedures holding the copies are then 64-aligned and internally
identical, so the paired arms land on the *same* offset and the pair
is layout-neutral by construction. Two things it does not do. It freezes
this pair at 53, which straddles --- the variance goes, the penalty stays,
and the offset frozen at is set by the procedure's own internals rather
than chosen. That the option stops at functions is deliberate and known: GHC
[#14701](https://gitlab.haskell.org/ghc/ghc/-/work_items/14701) has the person
who added it saying loops could be done too and were not looked at closely.
**It is now timed, and it is free on the baseline** (2026-08-11, a filtered
`*/list` pass over the shape set on each of three binaries, 24 benches each,
quiet machine). `.text` grows 0.14% and `list` does not notice: per-shape
geomeans of **0.9993** for the flag's build against `micro-unaligned` and 0.9997
for `micro-aligned` against the same, both scattering +-2 to 3.5% per shape.
So the insusceptible arm stays insusceptible under either intervention, which
is what licenses reading a ratio out of any of these builds ---
and it reproduces Run 10's fifth prediction in a second setting, a one-bench
process rather than a full roster. The rebuilt binary's offsets
are the `[3, 53, 3, 53]` and `[8, 8, 4, 4]` recorded above, read out again,
and its `check` log is byte-identical to `micro-unaligned`'s:
`cabal build micro --ghc-options='-fspec-constr -fproc-alignment=64' --builddir=dist-procalign`,
the fresh builddir being what forces the rebuild a value-carrying flag does not.

**The loops can be aligned outright, though, by standing in for the assembler**
(2026-08-10). `-pgma` replaces the program GHC assembles with, so `align-as.py`
beside this file rewrites the `.s` on the way past: every local label
that a later instruction jumps backwards to --- which is what a loop head
is in the NCG's output --- gets a `.p2align 6`. On this suite that aligns 395
heads and puts **every copy of both fills at offset 0**, grows `.text` by 0.13%,
and leaves `micro check` green, 45 shapes agreeing and none dissenting.
So the straddle can be removed rather than merely frozen, and with
it the penalty --- which turns the whole finding into a two-bench question ([the
open list][open]).

**How far it gets is a thing to measure and not to infer**, the shim's own count
of 395 being labels in the assembly it was handed rather than loops
in the binary that came out. `loop-offsets.py --survey` counts the population
that matters --- self-loops no longer than a line, in this suite's own compiled
code, since only those can be rescued by an offset and everything longer spans
several lines in any build. It reads 115 such loops in `micro-unaligned`, **50
of them straddling and one at offset 0**, against 101 in `micro-aligned`
with **100 at offset 0 and none straddling at all**.

**The shim was blind under `-g`, which is why this wanted a fix and not merely
a build.** `align-as.py` aligns a head only where the line before it
is an instruction, that being how it refuses to put padding between an info
table and the code the table belongs to; under `-g` every head follows
the previous block's `_end` and `_proc_end` labels instead, so **not one head
of a `-g3` assembly was given a directive** --- 0 against the same day's plain
assembly at 395, read off the two captures --- and the build came out unaligned
in silence: none of its 101 short self-loops at offset 0, 41 straddling, and two
of those the timed fills of `-add-in` at 56 and `build` at 52. The guard now
reads past the lines that emit no bytes, another label or a `.loc`, and the same
build gets 421 heads a budget, 46 loops at 0 and one straddler left ---
a 44-byte loop in `mkBroadcastMid`, which is view construction rather
than a fill and one of the heads the info-table guard is there to leave alone.
**The look-through fires only where the assembly carries `.loc`,
and that condition is the point rather than a nicety**: applied to every build
it finds 27 heads more in the plain assembly, 422 against 395, which would
re-base every figure this README has published for a reason no strategy changed.
So a `-g` assembly gets the corrected guard and every other keeps the literal
one, byte for byte --- which is the control, and it is an end-to-end one because
a shim change reaches nothing otherwise: built from one source into **two fresh
builddirs**, `-fforce-recomp` and all, the max-skip half comes out md5-identical
under the fixed shim and under the shim as committed, each printing 395.
**Those 27 are one shape of loop and not a scattering**: each is a pre-tested
loop whose head carries a block label as well as its own, two labels at one
address, so the literal guard read a label where an instruction had
been the whole test. **And what they do to the binary is one pad**, which
is the figure to have before spending a run on them: a directive is a budget
and not a padding, and the assembler declines it wherever the loop already spans
the least its length allows. Of the 395 the literal guard emits, **156 actually
pad** --- 3941 bytes in Main's code, a median of three multi-byte NOP
instructions each and 60 bytes at the longest --- and adding the 27 makes
that **157 pads and 3988 bytes**. Twenty-six of the twenty-seven are declined;
one fires, and everything after it moves 47 bytes. The short-loop populations
agree that nothing else happened: 112 loops either way, none straddling
in either, and the count at offset 0 going 58 to 57. So the question those 27
raise is not what NOPs cost. It is whether one more aligned loop is worth
re-rolling the placement of everything downstream of it, which is the term
this README prices at a few percent and cannot predict --- a paired run's
to answer if anyone wants it answered.

**So building everything with `-g3` is refuted, and a `-g3` build is a twin
to read rather than a binary to time.** The proposal was that if the timed
binaries carried their own names there would be no correspondence to establish
and a per-arm offset claim would become an ordinary reading; its own criterion
was that the arms agree within the run's floor. They do not. A pair differing
in `-g3` alone --- one source, one regime, and needing no pad, the two `.text`
coming out the same size with all 29449 shared library symbols at a whole-line
delta --- gates at `build` **0.9391, 0.9488, 0.9363 and 0.9517**, plain
over `-g3`, across the four pairings of two passes each, and `mut-odo` at 0.9626
to 0.9743, against each binary's own repeat of 0.9868 and 0.9970 on `build`
and 0.9958 and 1.0079 on `mut-odo`. Five percent and three percent, one
direction, four to six times the floor, with `list` still to under 1.4%
and no wider between the halves than inside one. What that prices
is the package, the halves differing in emitted code *and* in where the executed
copies land, 0 and 0 against 4 and 28 --- and the package is what a basis
decision wants. The `build`/`mut-odo` ratio moves with them, 0.9862 and 0.9952
in the plain passes against 1.0109 and 1.0219 in the `-g3` ones, but all four
are ties by sign test on intervals covering 1, so that is a point estimate
shifting and not the pair separating; the shared-offset reading above is neither
confirmed nor contradicted at this budget. **The machine was not fully quiet**,
its owner having said so while the gate ran, which is why the floor here is each
binary's own repeat rather than Run 11's drift band; the palindrome cancels
drift across the hour and all four pairings agree in sign and size. **Both
halves were built with the look-through applied unconditionally**, which
is the form that predates the `.loc` condition above and the reason it can
be said the shim is held constant across them rather than treating one half
differently: what the pair varies is `-g3`. That half is not the basis recipe
byte for byte, carrying the 27 extra heads, but it places every tracked loop
where the basis recipe does --- the same `[11, 0, 4, 0]` and `[24, 8, 0, 0]`,
checked on both forms --- so what the gate compares is two builds whose timed
loops sit identically and whose debug information does not. Rebuilding the pair
from this tree therefore reproduces the `-g3` half exactly and the other
with those 27 heads unaligned, which is the same experiment and not the same
bytes. So the naming above is read off a twin and carried to the timed binary
by the correspondence --- the arrangement the recommended path meant to remove,
and does not. **And the twin is short of copies as well as of registers, which
is what bounds the naming** (2026-08-14, four binaries --- the two timed halves,
a fresh plain build and a fresh `-g3` twin --- matched by body bytes rather
than by proximity). One body reads four copies in every plain binary and **two**
in the twin, and the twin's two carry distinct worker symbols that `addr2line`
puts in `fbMutOdo` and `fbBuild`; the vecdims body reads four in all four
binaries, which is exactly why that family names as a bijection and this group
cannot be named at all. A plain build therefore holds **two copies of that loop
per function** and `-g3` emits one --- a duplication the debug build suppresses,
the same class of divergence as the register allocation above, and the reason
the recommended path's `addr2line` step can reach a function but never a copy
--- and the reason the NOPs entry's own next step was undecidable before
it was attempted, which is recorded there.

**And a weaker level is no way round it, which is the move to expect
from a README that says `-g3` throughout.** `-g1` is the weakest GHC has ---
the users guide gives it as producing stack unwinding records for top-level
functions, which is data about a program rather than a part of one ---
and it changes the emitted code exactly as `-g3` does: one instruction fewer
and a different register assignment on an eight-line module, the same on GHC
9.10.3, 9.12.4, 9.14.1 and HEAD, with `-g2` between them behaving alike.
The reproducer and that table are horde-ad's
`docs/ghc-issue-debug-changes-codegen.md`, filed as [GHC work item
27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687), which
this README's finding produced; what they settle here is that no debug level
is a cheap way to put names in a binary that will be timed.

**Those two populations are not the same size, and the difference
is the disassembler rather than the binary** (2026-08-11, and it corrects how
the two counts above may be read). Lifting the survey's own 64-byte cap, Main's
resolved self-loops go 144 to 125 across *every* span bucket, not just the short
one --- which rules out the obvious account, that padding inflated loops past
a line, since the 65-to-128 bucket falls too, 20 to 16. Counting one level
further back says what happened: Main's code carries **1580** backward jumps
in the unaligned binary and **1583** in the aligned one, so the loop structure
is untouched, as it must be for a shim that only inserts alignment directives.
What moves is resolvability --- targets not decoded as an instruction start go
**613 to 777** --- because `objdump -d` sweeps linearly and tables-next-to-code
interleaves info tables with instructions, so shifting code by arbitrary NOP
runs changes where the sweep mis-decodes and re-syncs. So the fourteen missing
short loops did not grow and did not vanish; they stopped being visible
to the instrument. Read *none straddling* as a statement about a sample
that alignment makes smaller, not about the binary, and take the completeness
question to the assembly instead, where the shim works and there is no decoding
ambiguity: it knows which 395 heads it aligned, and the heads it skipped
are exactly those whose preceding line was not an instruction. That is the form
in which the claim below is sound, and the survey is corroboration rather
than the evidence.

The heads the padding rule skips, the ones a table sits in front of,
are not loop heads that would have straddled here: for short loops in the code
this README compiles, the alignment is complete rather than partial. What
it still does not reach is the libraries, `vector`'s loops among them, which
no `-pgma` on this build touches.

**Pad only between two instructions, which is what the first attempt did not.**
Aligning every backward-jump target, 928 of them, produced a binary that failed
`check` on the first shape with `index out of bounds (-1378,324)`.
Tables-next-to-code puts an info table immediately before a return point, which
is a local label too, and a `.p2align` inserted there separates the table
from the code it belongs to. Requiring the preceding line to be an instruction
fixes it, at the cost of the loops whose head follows a table --- none of which
this README measures. It is also why `check` is the gate to run on such a build
and the offsets are not: the offsets looked right in the broken one.

**And a trap that would have ruined that experiment silently**, on all four
of those compilers. GHC does not count `-fproc-alignment` as a flag change,
so an incremental build that only adds or drops it keeps the old object code
and says nothing: `ghc -O1` then `ghc -O1 -fproc-alignment=64` leaves
a byte-identical binary, where adding `-fforce-recomp` gives a different one.
Cabal is not at fault --- it reports `(configuration changed)` and re-invokes
GHC every time, and the same toggle on `-fspec-constr` recompiles
with `[Optimisation flags changed]`.

**And the trap is far wider than the flag that found it**, which is what makes
it a standing rule here rather than a note about one probe. Recompilation
checking hashes boolean `GeneralFlag`s and a fixed list of fields, so every
setting that carries a *value* is outside it --- `-pgma` and `-optlo`/`-optlc`,
the inliner's `-funfolding-use-threshold` and `-funfolding-fun-discount`,
`-fmax-worker-args`, `-fdmd-unbox-width`, and **`-fllvm`**, so that switching
the whole code generator reuses the native backend's objects in silence. All
of them confirmed missed on all four compilers, and that list is a floor:
it is what one test module could exercise. So **any A/B in this README
that toggles a flag must force the rebuild** --- `-fforce-recomp` or a fresh
`--builddir` --- and the regime comparisons already run that way only because
they were built in separate trees. The first round of the alignment experiment
had neither and read its flag as inert. Written up
as `docs/ghc-issue-recompilation-ignores-codegen-flags.md` in horde-ad, beside
the block-pool issue and in the same form, and filed from there as [GHC work
item 27667](https://gitlab.haskell.org/ghc/ghc/-/work_items/27667) --- that file
carries the cause in GHC's own source and the list of settings, and is the copy
to read.

**What is comparable across an alignment change, and what is not.** `list`
is the one arm measured insusceptible to placement --- 0.9949, 1.0019 and 1.0031
across the rebuild probe's four binaries --- so the denominator of every ratio
this README publishes, and the absolute anchor cells beside them, stay
comparable across the change. A susceptible arm's absolute figure does not,
which is why an aligned build wants a column of its own beside the regimes
rather than a splice into one: folding aligned figures into `-fspec-constr`'s
column would reintroduce in silence the term that alignment exists to remove.
And once an aligned build is the standing regime, the per-shape record a later
run compares against is taken from *it*, a fingerprint kept from an unaligned
run passing the layout term forward into every run that reads it.

**An aligned figure read against an unaligned one is a diagnosis,
not a continuation.** An arm that moves between the two has had its old figure's
layout term subtracted, which is neither a regression to explain nor the roster
doing something, and it wants writing up in those words. Such a pairing also
carries its own control, and the control is `list`: it is predicted not to move,
and if it does then the baseline was carrying layout too, every published ratio
has been divided by a moving denominator, and that is a larger finding
than whatever the pairing was run for.

**And the identical-code pair collapsed across all nine populations at once when
the loops were aligned**, which is the strongest single result the pairing gave.
On Run 9, one unaligned binary throughout, `build`/`mut-odo` ran 1.078
(`window`) to 1.375 (`bcastmid`), above 1 in every population, with `build`
slower on 39 of the 43 shapes between them. On Run 10's aligned half it runs
**0.9148 (`revsome`) to 1.0335 (`reshape1`)**, below 1 in eight of the nine.
So a 30-point spread that was above 1 everywhere became a 12-point band around
it, in nine populations measured in nine separate processes, and the only thing
changed was where the loop sits in its cache line. Two things it does not do.
It does not close the pair --- 3% survives on the main set --- and the one
population that inverts is `reshape1`, where both arms are twenty-seven times
slower than the class's leaders and whatever separates them is not the loop
the shim aligned.

**And a probe has since priced the rebuild itself, which is what neither
the twins nor that pair measure.** Four binaries built from sources differing
only in inert pad arms, the run filtered so the pads never execute, leave `list`
inside 0.5% and move `mut-odo` and `offtab` by up to 18% ([the open
list](#what-is-open) carries the figures). So this README has three
uncertainties of quite different size and only the smallest is on the table
above. An arm against **itself in one binary** is the A/A twins, 1.00% on Run
10's unaligned half and 0.54% on its aligned one. Two **different arms in one
binary** carry placement, which `build`/`mut-odo` put at 14-24% for a pair whose
code is identical --- **until the loops were aligned, which takes it to about
3%**, and to a tie by the sign test whenever the two copies share an offset. One
arm across **two binaries** carries the rebuild, up to 18% on a susceptible arm
and almost nothing on an insusceptible one. Susceptibility is a property
of the arm and has been measured for three of them, so for the rest
it is unknown; what that protects is orderings and tiers, which several arms
witness at once, and what it does not protect is any single arm's figure read
across a rebuild.

**What does code placement cost?** **A rebuild is worth up to 18%
on a susceptible arm and 0.5% on the baseline** --- which is the size of every
unexplained regression in Run 8, and the largest effect this README has measured
that is not a strategy. Four binaries were built from sources differing only
in inert pad arms, the run filtered so the pads never execute; against the first
of them the other three read `list` 0.9949, 1.0019 and 1.0031, `mut-odo` 1.0389,
0.8808 and 1.0401, and `offtab` 0.8241, 0.9524 and 0.9126 (2026-08-08,
`-fspec-constr`, 24 shapes, per-shape geomeans of absolute net time).
So susceptibility is a property of the arm: the baseline has almost none and two
arms have a great deal, and they are the same two the flag sets back hardest.

**Around that sit the readings it explains.** `offtab`'s own regression
is **not** roster or noise: filtered into a five-bench process it reads 1.2236
across the regimes over 24 shapes, slower on 24 of 24, against the full run's
1.218 --- but that used one binary for both regimes, so it rules out everything
except placement. `build` and `mut-odo` compile to the same worker and moved
in *opposite* directions under the flag, 17% faster and 19% slower, which
identical code cannot do. `bq-gen` regressed 12% with its build loop specialised
like every other and its build allocation-free. And the flag moves 12 KiB
of `.text` (20,349,125 bytes to 20,336,837), so every arm's address
and alignment shift whether its code changed or not.

**Answered, 2026-08-10: for a loop this size, placement costs 1.16 to 1.19.**
The first attempt at this left the question narrower than it found it ---
it should have timed `build` across the four layouts and did not, a shell glob
having eaten the arm ([the reader's section](#the-reader-read-runpy)) ---
and what settled it instead was the pad probe done properly, eight binaries
stepping each arm through all eight 8-byte offsets with membership fixed
(the figures, the graded penalty and the tables are below). So the *how* is now
measured and not merely read off a binary: a straddled copy of the 28-byte fill
costs 1.19, or 1.10 where only three bytes precede the boundary, and
that is what the pair's 0.86-to-1.24 span across runs was made of.

What the probe does **not** reach is the rest of this entry. The 18% a rebuild
is worth stands as measured, since a rebuild moves more than one loop's offset;
`offtab`'s and `bq-gen`'s regressions have no shared-loop counterpart to be read
this way, which is the entry below on crediting a margin to a strategy;
and susceptibility remains a property of the arm, now with a mechanism
for the two arms that share a loop and none for the others.

**Run 9 had made this the README's central question rather than a caveat
on it**, and that is the framing the answer inherits. A membership change alone
moved five fingerprint arms from 0.910 to 1.192 in absolute time against
a baseline that held to 0.998, and moved `build`/`mut-odo` --- one worker, two
slots --- to 1.13 where Run 8 read 0.86 and Run 7 1.24. Every route through
the roster was blocked, the roster being one of the things that sets the layout,
which is why the answer had to come from a probe that holds membership still.

**And the third of those is a bias, not a floor, which is the distinction
to keep.** A floor is a threshold below which a margin might be noise,
and it shrinks as samples accumulate; this does not. Each binary's figure
is *correct for that binary* --- the four-binary rebuild probe's cells
are geomeans over 24 shapes with per-cell intervals of a fraction of a percent
--- so collecting more samples inside one build cannot reduce it, and only
averaging over several builds would. The per-shape picture says the same: across
rebuilds `list` scatters 2.2-2.5% per shape while its geomean holds to 0.5%,
where the two susceptible arms scatter 5-10% per shape *and* move their
geomeans. So do not read 18% as a new floor for this README's tables. Every
comparison inside the Results table is two rows of one binary and is governed
by the A/A twins as before; what the 18% governs is the sentences that cross
a build, which in this README means the cross-regime absolute figures
and nothing else.

**Bisect a position effect by REMOVING from the full group, never by adding
to a pair.** Six probes here searched for what warmed `bq-expand` by building
selections up from a hypothesis, and every one of them omitted the single bench
that did it, because a hypothesis-shaped selection can only contain what has
already been thought of. Removal cannot make that mistake: start from the whole
group, which is known to show the effect, and take benches away until it stops.

**A filtered run cannot answer the position question by measuring spans**,
and the trap is quiet enough to be worth stating: criterion's selection removes
the intervening benches, so a pair placed 28 slots apart in the roster ends up
adjacent, and the crossed design collapses to six near-identical adjacent pairs.
Measured on a twelve-arm probe, spans of 28 and 0 both came out under 6. `--aa`
says so when the run is filtered. A span this way is unmeasurable, and the whole
roster in the process is what the crossed design needs.

**What a filtered run can do is put every arm at the cold end**, which is how
Run 9's five probes worked and why they answered. Collapsing the spans is
not a defect there: it removes the warming, so every arm reads its isolated
cost, and the published cell is then held against *that* rather than against
another slot. Read the two uses apart --- a filtered run cannot price
the distance between two slots, and it can price the difference between a warmed
process and a cold one, which is the larger of the two effects here by an order
of magnitude.

**The floor grows with the margins, and for the same reason**: subtracting
a term common to both arms magnifies their disagreement exactly as it magnifies
a real difference. On raw slopes Run 10's unaligned six read 1.0008 and 1.0038,
1.0027 and 1.0033, 1.0066 and 1.0035 --- adjacent and distant per strategy ---
so the largest deviation is 0.66% before the correction and 1.00% after it,
and every one of the six grows. Correcting the table without correcting
the floor would have been the whole error.

**And it was re-checked at full budget on Run 10, over four populations
at once** (2026-08-11). Predicting each A/A pair's net deviation from its raw
one as `1 + raw/(1-f)`, with `f` the forcing term's share of that arm's own
slope, reproduces all **24** pairs of the main set, `window`, `bcastmid`
and `scaled` to a few hundredths of a percentage point --- 5.36% predicted
5.29%, 0.54% predicted 0.67%, and the rest closer. Two things that buys.
The amplification is arithmetic and not a second effect, confirmed on a run
rather than inherited. And it says **why the `mut-odo-vecdims` slot keeps
carrying the worst pair**: `f` is largest for the fastest fill, 0.598 against
0.296 for `bq-expand` in the same `scaled` process, so that arm amplifies
whatever raw disagreement it has by 2.49x where its neighbours amplify by 1.42x.
The raw disagreement is still the larger factor there --- 2.13% against 0.17%
--- so this explains part of a pattern rather than dissolving it.

**That is a mechanism rather than an observation, so it was checked --- on Run
6's three pairs, when the correction landed.** Subtracting a shared term scales
a pair's deviation from 1 by `1/(1-f)`, `f` being the term as a share of the arm
--- an identity *per shape*, and therefore worth nothing until it has survived
the geomean over shapes. It did, to within 0.01 percentage points on all three:
predicted 1.0010, 0.9943 and 1.0293 against observed 1.0011, 0.9942 and 1.0292,
with the amplification tracking `1/(1-f)` arm by arm too. So the floor's growth
is the correction's own arithmetic, not a second effect riding along with it ---
and Run 9's pairs move the same way, every deviation larger net than raw.

**Failed Run 6's two conclusions here are settled.** *1/time* is refuted
as an account of the floor: per-cell *scatter* does track it --- the adjacent
pairs in the table rank by their arms' speed --- but scatter cancels,
and the bias that survives cancelling ranks by span, not by any arm's speed.
*Position* was confirmed by the crossed design built for it, read
as not reproducing on Run 8, and is confirmed again by Run 9 in a form
the crossing cannot summarise: it is per shape and per family, not a trend
in span. What the crossed design settled for good is that the question
is answerable at all; what Run 9 adds is that the answer is not a single number.

**Six A/A points are a modest estimate of a noise floor whichever run supplies
them, and the four runs disagree several-fold**: Run 9 was the tightest
and the wildest at once, five pairs inside 0.07% and one cell at 41%, where Run
10 is uniform instead --- every pair inside 1.00% unaligned and 0.54% aligned,
worst cells 11.2% and 7.7%. Expect either shape rather than a constant.
So the threshold to quote is the running one, and it is the run's own number
and not a tenth of a percent that a margin has to clear.

**The floor above is also measured within one roster, and the roster
is a variable of its own**: RTS pool state a predecessor leaves in the process
moved a horde-ad benchmark ~18% ([the full account][pos-effect] --- which
includes this suite's own floor measured isolated against in-process, on both
harness generations). Run 9 is that account reproduced here and larger,
its expansion family reading 35-40% above its published cells once the process
is emptied of predecessors. Every strategy sharing one process is what protects
the tables above, ratios cancelling the shared process draw --- and the vgg cell
is what that protection costs when the draw is *not* shared, one family warming
and another not. A comparison that crosses runs should pin the benchmark
selection along with the binary.

**Every kind of comparison this README makes wants an instrument, and only some
have one.** Worth asking outright of any new claim, because the four answers
known so far differ by two orders of magnitude and none was found on purpose:
an arm against itself in one binary is the A/A twins, 0.54% to 1.00% on Run 10
and 0.07% on Run 9; two different arms in one binary carry placement, which
`build`/`mut-odo` put at 13-24% for a pair whose code is identical and put
at about 3% once both copies are aligned; one arm across two binaries carries
the rebuild, up to 18% on a susceptible arm; and one arm across two *process
populations* carries the warming, 35-40% on the expansion family
at `vgg-14-c512-k3`. The last is the largest, and the second is the one
this README has learned to remove rather than only price. So when a sentence
compares something new --- two populations, two machines, two GHC versions,
an arm against a prediction --- ask which of these bounds it, and if none does,
say so in the sentence rather than borrowing the nearest number.

**Each population measures its own floor.** The same eighteen controls ride
every process, so a stride-class run prices the noise of the process its own
figures came out of --- which is the only process they can be judged in ---
but it prices it over three cells where the main set has two dozen. Read
a class's controls as this floor confirmed there or not, rather than
as a threshold of that class's own, and never carry the main set's figure
into a class comparison or the other way about. Run 10's class processes
are that ruling observed: floors from 0.16% (`rev`) up to 5.36% (`scaled`),
a **thirty-fourfold** spread across populations of one run, where Run 9 spread
fifteenfold and Run 8 differently again. The `mut-odo-vecdims` slot carries
the worst pair in **five** of the eight --- `revsome`, `bcastmid`, `reshape1`,
`window` and `scaled` --- where Run 9 put it in four and Run 8 in seven;
`bq-expand`'s pairs take the other three and `bq-scan-rem-gm-mulback`'s take
none. Four runs at four counts is not a pattern settling, but the amplification
above says the slot is not neutral either: `f` is largest for the fastest fill,
so that arm converts a given raw disagreement into a larger published one
than any other pair in the same process. Read the recurrence as partly
arithmetic and partly unexplained, and read a class's floor as the run's own.


### R2 is the ramp detector, not the noise detector

The two columns catch disjoint failures. **CI%** finds sampling noise, which
the capping then bounds. **R2** finds *curvature* --- early, low-iteration
samples running slower than late ones, because criterion forces only a minor GC
between samples and a full one just once per benchmark, so promoted data
accumulates as the sample count climbs.

**A ramp is systematic, so it yields a *narrow* CI around a *biased* slope:
the capping cannot see it and will not bound it.** The bias tilts the fit
shallow, so a ramped strategy reads slightly **faster** than it is ---
and not uniformly, since strategies allocating a large scratch ramp harder
than in-place fills, making the flattery differential exactly where
the comparison is decided. Read any row with R2 below 0.99 as possibly a couple
of percent optimistic rather than merely noisy. In Run 10 (SpecConstr)
the unaligned half has 1 cell of 816 in the main set --- `bq-expand-zf`
on `stretch-inner256` at 0.9877, **the same arm and shape for the third run
running**, which makes it a property of that pair rather than of a run --- while
the aligned half has 3, worst `bq-expand-gm-mulback` on `stretch-square-1341`
at 0.9800, and two class processes add one each (`build` on `reshape1-r3`
at 0.9886, `gen-quotrem` on `slice-cnn-L2-24x24-c32` at 0.9751). Run 9 had one
and no class cell, Run 8 one plus `build` on `bcast-tall-Mx2`, Run 7 two
and six, five of its six on `bcast-inner900` where the scan family ramped
re-reading a 2000-element backing with 1.8M elements; those are gone,
in the regime that takes the same family's allocation to the table. Alignment
therefore does not reduce curvature and may add a little, which is a different
axis from the noise it leaves alone (its median CI% is 0.138 against
the unaligned half's 0.134 over the same 816 cells).

**Run 6's two worst cells had a cause worth the space, because it is a method
as much as a finding.** `mut-odo` carried that run's highest CI cell on both
of its two smallest `cnn-L1` shapes, while `build` --- the identical fill
through `vBuildVS`, from a different roster slot --- and `mut-odo-vecdims` ---
the same fill with the odometer's cons-lists replaced by unboxed vectors ---
were clean on the same two. Same shape, same process, so it was neither
the shape nor a disturbance in that stretch of the run: it is the odometer's
list traffic as a GC ramp where `l` is small enough for it to dominate, which
is the cost `mut-odo-vecdims` exists to remove. The ramp did not recur at Run
7's full budget, where the same cost surfaced as scatter instead, `mut-odo`
carrying that run's highest `noise` figure by far; it did not recur on Run 8
or Run 9, that arm reading an ordinary 1.01 on the latter --- **and it is back
on Run 10, larger, and largest of all on the half where the arm is fastest**.
`mut-odo` reads 2.40 unaligned and **4.51 aligned**, the noisiest bench
of that process, ahead of `list` (3.59), `gen-unsafe` (3.43) and `gen-quotrem`
(3.36); on the unaligned half the first-attempt arms still lead it, `gen-unsafe`
at 5.57 and `gen-quotrem` at 3.48. For scale, `concat-runs` was dropped
from the timed roster at 2.45. So the earlier reading --- that whatever the flag
does to this arm, it does not do it by making the bench noisy --- no longer
holds: removing 12% of its time by aligning its loop left it noisier
than anything else in the process, and nothing here explains why. **Positional
or strategy-intrinsic is the question to ask first of any suspicious cell**,
and `--cells` answers it cheaply: a disturbance shows as a contiguous window
of roster slots, a property of the code shows as one slot across several shapes.

That second reading needs several shapes to see the slot across, which a [stride
class](#the-stride-classes-and-what-they-cover) does not have: with two
or three, a ramped cell is a large share of its column and only the first
reading is available. Whether it is the shape or the strategy is then a question
for the main set, where the same strategy has two dozen cells.


### sum-only, and the correction now applied

**Every strategy is timed as `VS.sum . fb`, so every measurement carries
the same forcing pass; `sum-only` times that pass alone.** It is a median 17.7%
of `bq-expand` and 2.7% of `list`, so an uncorrected ratio is compressed toward
1 by about that much and every margin read off one is an *understatement*.

**Run 6 (-O1) licensed subtracting it, and every figure a run publishes is net
of it**: its two halves agreed to 0.01% paired, flat in shape size as well
as position, and `read-run.py` has since taken the term per shape as the mean
of the halves and divided net of it. Nothing is comparable across that line ---
every figure predating Run 6 here and in `Main.hs` was uncorrected --- though
the uncorrected column stays one
`--exclude sum-only-early --exclude sum-only-late` away, and `read-run.py` says
on stderr when it is reading one. And the correction can change an ordering,
although `(B+S)/(A+S) < 1` exactly when `B < A`: that identity holds *per
shape*, and the geomean over shapes does not preserve it --- Run 6 saw three
adjacent pairs swap, all inside the floor.

**The term passes three gates, re-passed by every run rather than inherited**,
each blind to what the others catch:

1. *Position.* The two halves sit far apart in the roster and must agree;
   failing is the halves parting past the floor. **Run 9 (SpecConstr)**: 1.0000
   paired, 0.10% mean per cell, worst cell 0.53%, the halves 28 benches apart;
   and every class process within 0.3%, the loosest being `scaled` at 1.0026.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape --- one sum over `l` elements --- and a term that
   were not could be wrong in both halves alike, leaving their agreement
   to notice nothing. It is: 0.592 to 0.607 ns per element across the whole
   shape set, a 1.02x spread over that 6250x range of `l`, with the largest
   shapes a couple of percent dearer per element than the smallest and no trend
   beyond that. `--selftest` checks it on every run and fails the run past
   a 1.5x spread; all nine of Run 9's populations passed, none spreading past
   1.02x.
3. *The read itself.* `sum-only` re-reads one **fixed** vector, where a strategy
   sums one its own fill has just written --- a different cache state,
   and the one thing neither gate above can see, since a term biased by it would
   be biased alike on every shape and in both halves. This is what
   `bq-expand-nosum` and `mut-odo-vecdims-nosum` are for: each is its base arm
   run again and forced with a single element instead of the sum, so *base minus
   arm* is that sum in situ. Measured against `sum-only` on Run 9 they read
   **0.9854** and **0.9764** as medians --- within 3%, on the two arms where
   the term is the smallest and largest share of the bench (a quarter
   of `bq-expand`, a third of `mut-odo-vecdims`), so the test spans the range
   over which a bias would matter. Per-cell scatter is 4.3% and 3.5%, the worst
   cells on `stretch-inner256` and `stretch-square-1341`. Failing is both
   medians leaving 1 on the same side by more than a few percent ---
   the biased-read signature; one arm scattering while the other reads clean
   is a local disturbance for that population's write-up, not a failed gate.

   **It has now not bracketed for two runs, which promotes it from a thing
   to watch to a thing to price.** Run 7's two medians sat either side of 1; Run
   8's were both below, and Run 9's are both below again --- as is **every**
   in-situ median of both arms in all nine populations, eighteen readings
   between 0.960 and 0.999. Two runs and eighteen readings on one side
   is no longer a coincidence at any reasonable reading. The in-situ sum costs
   *less* than `sum-only`'s re-read, so the term is slightly over-subtracted
   and every ratio slightly flattered --- by about 0.5% of `bq-expand`'s own
   slope at a 2% error in a term that is a quarter of it, which is inside
   this run's floor everywhere but `bcastmid`, where the reading is 0.9597
   and the flattery about 1%. The gate still passes on its own test, which asks
   for *more than a few percent*; what it has stopped doing is passing
   for the reason the test assumes. [The open list](#what-is-open) carries what
   would settle it.

   **The cells under those medians say the same, and add a gradient the medians
   hide** (2026-08-09, off Run 9's artifacts). Taken per shape instead of
   as a median, over both arms and all nine populations, the in-situ readings
   sit below 1 on 73 cells of 86, sign p 2.7e-11 --- and not because
   differencing two nearly equal numbers is noisy: calibrated on each arm's own
   A/A cells and amplified by the differencing, the scatter to expect
   is a fraction of a percent to a couple of percent, and three `bq-expand`
   cells of 24 and no `mut-odo-vecdims` cell fall inside it. The two arms also
   order the main set's shapes alike --- Spearman 0.82, and 0.85 with the three
   cells above 1.03 set aside --- and two fills an octave apart in speed,
   at roster slots 13 and 50, agreeing shape by shape is what a property
   of the read looks like rather than one of either arm. The gradient is in `l`:
   the shortfall runs about a tenth of the term at the smallest shapes
   and vanishes at the largest (smallest twelve shapes 0.955 and 0.960
   by geomean, largest twelve 1.027 and 1.002; r against log `l` 0.60 and 0.58),
   which is neither a per-call constant nor a per-element rate. Where
   it concentrates is the shapes whose result is L1-resident: the three at 32
   KiB of result or under read 0.898 and 0.925 by geomean against 0.98 to 0.99
   for everything larger, and between the L2 and L3 buckets it barely moves
   at all. Whether that is a step at the L1 boundary or a smooth trend three
   shapes cannot settle --- with the cells above 1.03 kept a line in log `l`
   fits better and with them dropped a three-level step does, decisively
   for `bq-expand` and marginally for `mut-odo-vecdims` --- so read
   it as concentrated in the L1-resident shapes rather than as a boundary
   effect. None of this replaced the third `-nosum` arm: a third write pattern
   was the only thing that could separate the read from these two arms,
   and the above is evidence pointing that way rather than a substitute.
   **The arm has since been added, and it agrees.** `mut-flat-gm-nosum`
   is a flat fill sharing neither an odometer step nor an expansion stream,
   and its in-situ term reads below 1 like the other two, which is the reading
   gate 3's entry carries and the answer this paragraph was waiting for.

   **Priced, it is under a point.** Re-pricing each arm's own numerator
   with its in-situ term, the `list` denominator left alone at 2.7% of itself,
   moves Run 9's published main-set geomean to 0.9993 for `bq-expand` and 1.0088
   for `mut-odo-vecdims`, and each class's to between 1.0015 and 1.0288,
   the largest under `bcastmid`, `scaled` and `bcast`. Per shape it reaches +3%
   and -8%, and the cells that move a published figure most are the three
   reading *above* 1 rather than the systematic shortfall. So the flattery
   is real, sits inside the layout span everywhere, and is worth a sentence
   about a particular cell rather than a second correction to the column.

**And the correction is invertible, which is what keeps a pre-correction figure
comparable at all.** A raw slope is the published one plus the forcing term
times `l`, with `l` from `Main.hs`, so any uncorrected figure recovers to within
the term's own spread --- and the term has been within about 2% of every run's
since Run 7, through a flag, a roster, a layout, the shim's padding,
`-fproc-alignment=64`, an RTS line, a source patch that moves every loop offset
and a change of compiler. That is the control saying every run's correction
is one correction. Each run's own span is in its file, under Provenance.

**The three gates are a population's, not a run's.** Every process carries
the `sum-only` pair and the four `-nosum` arms, so a [stride
class](#the-stride-classes-and-what-they-cover) measures its own term
and re-passes all three on its own cells; the main set's term licenses nothing
about a class's, in either direction. What a small population weakens is gate 2
alone: it reads the term's cost per element across the shape set, and a class
spans a fraction of the main set's range of `l` --- three shapes of nearly equal
`l` leave it almost nothing to see. Gates 1 and 3 are as strong there as here,
being about position and about the read.

**What remains open is narrower than the original objection, and narrower again
since 2026-08-25**: the `-nosum` pairs price four arms, not the whole roster,
so a fill whose write pattern leaves the cache in some quite different state
could still be summed at a cost `sum-only` misses. The three that priced
it until then are all element-wise fills, which is the shape of the hole;
`canon-full-nosum` was added with the rework's block because that endpoint
dispatches per shape between hoisted stores, `VS.unsafeCopy` and the stepping
loop, so it is the first control here whose write pattern is not one pattern.
Two arms an octave apart in speed agreeing to 1% makes that unlikely rather
than impossible, and the arms are in the roster so every run reprices them.


## Provenance

**The half of a run's provenance that outlives the run.** A run's own --- what
its pair was, how the sequence ran, what moved and what did not, its anchors
and its correction --- is under [Provenance in the run's
file](runs/run19.md#provenance) and is replaced with the rest of it. What
is here is what a run does not replace: the delta chain below, which gains
a bullet per run and is the only record of which shape set and roster each
measured, and the list of what a run replaces OUTSIDE its own file, which
is a recipe. Between them they say what a run's figures have to be read against.

The desktop named at the head of the run's file is the same machine whose `idiv`
cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and should
name its machine at the head of its own file, where this one does.

**The delta, so the population is recoverable.** What follows is the *only* form
in which a shape set or roster is recorded here: its difference from whatever
`Main.hs` holds now. A snapshot would need rewriting at every change and would
be a second copy of a list that already exists; a delta costs what actually
moved and shrinks to nothing when the two agree. A roster delta has two halves
now that membership no longer settles what ran: which arms the roster held,
and which of them it timed. **And a third: the ORDER they ran in.** Order
is not membership, it *can* move code layout, and Run 10 measured layout at 12
to 14% on the two arms whose loop the shim rescues --- so a delta stated
in membership alone can read empty while the run is not repeatable. Whether
a given reorder moves anything is a thing to measure rather than assume, both
answers having turned up in one afternoon: `sum-only-early`'s slot-5-to-2 move
left all eight loops this README tracks byte-identical, while lifting it one
further place, above `list`, shifts every worker by ~40 KB and rerolls every
alignment. So record the order, and read the binary before deciding what
the record costs. **A fourth half arrives with the pairing and is not a delta
at all**: which half of the pair a figure came from, which is why the run file's
tables and its fingerprint say so.

- Run 19 measured today's shapes, class lists, roster membership and order,
  so its delta is empty --- it is today. What a reader has to carry is which
  half a figure came from: everything published in the run's file
  is `run19-g912`, the 9.12 half, and `run19-ghead` contributes the yardstick's
  second column, the arm-by-arm comparison at that file's head, the counted-work
  column, and a class comparison on five of the eight populations, three of them
  being disqualified by a baseline past 0.7%. **And two things that
  are not deltas.** The halves differ in the compiler, so a figure crossing them
  carries codegen and layout, as Run 18's did --- but this pair's `list` moved
  0.78% between them, so unlike Run 18's its two columns may be ordered
  and not subtracted. And the basis half is Run 18's basis BINARY, byte
  for byte, so absolutes cross those two runs freely and the boundary that stops
  them is still the BIOS change before Run 18.
- Run 18 measured the same shapes, class lists, membership and order,
  so its delta is empty too. Everything it published was `run18-g912`
  and `run18-g914` contributed its second yardstick column. **And one thing
  that is not a delta**: the BOX moved under it, its BIOS idle settings having
  changed before it, so no absolute of Run 18's or Run 19's is comparable
  with Run 17's or earlier --- ratios are, absolutes are not, and Run 18's
  fingerprint re-baselined them.
- Run 17 measured the same shapes, class lists, membership and order,
  so its delta is empty too. What a reader has to carry there is which half
  a figure came from: everything it published was `run17-wildlog`,
  the instrumented half, and `run17-det` contributed the yardstick's second
  column and a class comparison on all eight populations. **And one thing
  that is not a delta**: its two halves differed in `.text` size, so a figure
  crossing them carries a layout term where Runs 14 to 16 carried a runtime
  setting.
- Run 16 measured the same shapes, class lists, membership and order,
  so its delta is empty too. What a reader has to carry there is which half
  a figure came from: everything it published was `run16-a32m` and `run16-a64m`
  contributed its second yardstick column, and **its basis moved off the default
  nursery**, so a row's distance from any column before Run 16 carries
  the allocation area with it.
- Run 15 measured the same shapes, class lists, membership and order,
  so its delta is empty too. What a reader has to carry there is which half
  a figure came from: everything it published was `run15-lookrts`,
  the default-nursery half, and `run15-a32m` --- the half at this run's own
  area, and so the one Run 16's basis is checked against --- contributed
  its yardstick column. **And one input that is not a delta and not a half**:
  the dependency store, whose 48 packages were rebuilt between the two runs
  at unchanged versions, so Run 14's binary and this one share no package ABI
  hash. The assembler shim also moved, `9a70576` against `89c7ae8`,
  and is emission-neutral.
- Run 14 measured the same shapes, class lists, membership and order,
  so its delta is empty too --- what a reader has to carry there is
  that its control was `run14-a1g`, at two hundred and fifty-six times
  the default nursery where this run's is at eight times it, and
  that its halves' absolutes were not subtractable.
- Run 13 measured today's class lists and today's roster **order**, on **five
  class views short of a third shape** and on today's roster **minus the twelve
  A/A twins added after it** (`offtab`, `bq-odo-gm-mulback`, `build`, `mut-odo`,
  `list` and `gen-unsafe`, each in both positions) --- 840 benches against
  today's 1128 --- timing 35 of its own and leaving 24 untimed, winsorized per
  the estimator under `time`. What a reader has to carry besides is which half
  a figure came from: everything it published was `run13-maxskip`,
  and `run13-lookrts` contributed the yardstick's second column
  and the arm-by-arm comparison at the head of Run 13's own write-up.
- Run 12 measured the same shapes, class lists and order, on Run 13's roster
  **minus `mut-flat-gm-nosum`** --- 816 benches against Run 13's 840 --- timing
  34 of its own, winsorized likewise. Everything it published
  was `run12-maxskip`, `run12-maxskippa` contributing its yardstick column,
  and its class tables are a max-skip half's as this run's are, which is the one
  thing that makes the two runs' class figures a same-kind-of-build comparison.
- Run 11 measured the same shapes, class lists and order, on the roster Run 12
  had, so its delta is Run 12's --- what a reader has to carry there is
  that its published tables were the *aligned* half's, where Run 12's and Run
  13's are a max-skip half's.
- Run 10 measured the same shapes, class lists, membership and order,
  so its delta is empty too --- what a reader has to carry there is which binary
  each of its figures came from, its Results table being `micro-unaligned`'s
  while its fingerprint and class blocks were `micro-aligned`'s. That mixed
  basis was the transition to this one and lasted the one run.
- Run 9 measured the same shapes, class lists and membership **in a different
  roster ORDER**: `sum-only-early` sat at slot 5, moved to slot 2 ahead
  of the three distant A/A twins after that run, and to slot 1 above `list`
  for Run 10 ([the floor section][floor]). The first move relocated nothing ---
  a binary rebuilt from Run 9's own commit `96378d2` puts all eight tracked
  loops at the same offsets as the moved roster does, to the byte ---
  and the second relocated everything, which is what Run 10 spent to buy
  the pool fix and its predictions. **Run 11 did not spend it again**, which
  is the second thing alignment bought the schedule: in an aligned build
  a roster change relocates no loop, so the repetition this README had never had
  was available for the first time and is what Run 11 took.
- Run 8 measured today's shapes and today's class lists, on Run 12's roster
  **minus the eight arms written between them** (`bq-expand-gm-mulback`,
  `bq-odo-gm-mulback`, `mut-flat-gm`, `offtab-scan-rem` and the four
  `mut-odo-vecdims-add-*`), **timing all of it but `concat-runs`** where today
  leaves 24 untimed, winsorized likewise. Run 7's delta is Run 8's plus
  the regime, which is what keeps the last two columns in [What the next run
  compares against](runs/run19.md#what-the-next-run-compares-against)
  a controlled pair and the first two a different controlled pair.
- Run 6, still quoted here for the estimator ruling under `time`,
  for the `alloc` column's shape-dependence and for the correction's
  amplification arithmetic under [the floor][floor], measured today's main-set
  shapes **minus `stretch-pow2stride` and `stretch-inner256`, plus eleven since
  dropped** (`cnn-L1-12x12-c1`, `cnn-L2-12x12-c16`, `cnn-slice-c64`,
  `lenet-L2-14-c6-k5`, `mnist-28-c1-k3`, `cifar-L1-32-c3-k3`,
  `cifar-L3-8-c128-k3`, `cifar-32-c3-k5`, `vgg-14-c256-k3`, `deep-7-c512-k3`,
  `slice-c512`), on today's roster **minus thirteen arms** (the three crossed
  A/A twins, the two `-nosum` controls and the eight Run 8 also lacked),
  **timing all of it**, trimmed rather than winsorized, on the Storable scratch
  the conversion since replaced, and with no stride class in existence.
  That is the whole chain between its figures and this run's.

**What the next run replaces.** Run 19's numbers reach past the Results table,
so this is the list to walk when Run 20's land. Run 10 walked it twice
over and not symmetrically, one half per pass; every run since has walked
it once, one basis publishing everything, which is how it is walked from here.
It names *sections*, not figures: a list of figures is a second copy of them,
and enumerating it was how the previous two versions of this list went stale ---
one missing six sections, its predecessor leaking past it. What now guarantees
completeness is mechanical instead. Every section below is reached by a link,
and the coverage check is: no section carrying a figure outside a table may
be absent from them. The run's own file is reached whole rather than section
by section, that being what a run replaces and why it is a file. Run that check,
and repeat the two sweeps it cannot replace --- grep both documents
for figure-shaped numerals outside the tables, and grep them for the name
of the run being superseded, which is the one the previous run's file still
carries --- before trusting the list. The second sweep is written without
its numeral on purpose: spelled out, it is a run number nothing in step 5
reaches, so it would go on naming a run two runs back. It earns its place every
time: this run's pass found a superseded basis half named in the Results
section's own lead, `run13-maxskip` where Run 14's write-up should have put
its own, which every anchor and figure check passed over.

**Inside a section, find the paragraphs rather than reading it.** The list names
sections and a section here runs to hundreds of lines, of which a run rewrites
three or four paragraphs; Run 10's write-up read most of the floor section
to change four of its leads. **Not every paragraph opens with a bolded lead**:
well over a third carry none, and a few dozen of those carry a figure.
So a `grep -n '^\*\*'` between a section's heading and the next, in either
document, gives a section's **claims** and not its contents, and a walk
that stops there misses figure-bearing prose --- the opening section's
continuous argument, and continuation paragraphs inside list entries. The ones
a run touches are those whose lead or body carries a figure, which is why
`--para` falls back to the body when no lead matches.
`./read-run.py --para 'lead'` then prints any one of them with the line
it starts at, which is what keeps a jump off the `grep -n`/`sed -n` pair
that the install above it has already invalidated. `--check-doc`'s two sweeps
print line numbers for the comparative and superlative candidates already,
so between the three the walk is a list of jumps rather than a read.
This is deliberately a recipe and not a stored list of paragraph names: a stored
one would be a second copy of the structure and would rot the first time a lead
was reworded, which is the failure this list was rewritten to escape.

- [the run's own file](runs/run19.md) ENTIRE, which is what makes it a file:
  its head, carrying the run's name, regime, scale and source commit, the layout
  span a roster order change alone is worth and which half published what;
  the Results table and the findings under it; the yardstick and the two-column
  per-shape fingerprint, which are the only per-shape record kept once the JSON
  is deleted; the claims, where a run reports which held rather than re-deriving
  them; each class's own table, controls, provenance, anchor and paragraph;
  and its own Provenance, carrying what the pair was, how the sequence ran,
  the three main-set anchors with the eight class ones, and the correction's
  span. The bullets that used to name those sections one by one are this one,
  and the coverage check below reads it as covering every heading in that file;
- [the recommended tasks after Run 19](#recommended-tasks-after-run-19), which
  is run-scoped by its own title: a task taken or superseded leaves it, what
  survives is renamed to the run that inherits it, and a run's own surprises
  are added to it before the run file is replaced. **Leaving is not deleting,
  and where it goes is the half this used to omit**: a spent task's outcome
  and a pointer to whatever holds its account --- an entry of the open list,
  a topical section, an investigation directory --- go to that home,
  and the item itself goes. Item 1 of Run 17's subsection shows the migration
  done and the removal not: its evening is consolidated into the position-term
  entry and its raw material into `small-pinned-churn-investigation`,
  and a hundred words of it stand here anyway. **Nothing spent stays
  under a heading naming a run that is over**, which Run 17's items did until
  Run 18's write-up removed them and named where each had gone --- a departure
  rule with no destination named is one nobody applies;
- [the noise-floor table][floor] and its prose, from `--aa` --- including
  the raw-slope six it compares against, the position verdict the crossed
  controls now disagree about between runs, and the `build`/`mut-odo` pair read
  as a second control;
- [the opening section][opening]'s headline ratios and its regime paragraph;
- [The stride classes and what they
  cover](#the-stride-classes-and-what-they-cover), whose figures a run does
  NOT replace: they are one reading of the eight as instruments, taken over Runs
  10 to 13 and dated in its own lead, and it is on this list because
  the coverage check is over figure-bearing sections rather than over replaced
  ones. What the walk owes it is currency --- that the classes it describes
  are still the classes that ran, and that its membership check still names
  every class shape; the layout above them is not, in the way the column
  definitions are not. A run that leaves a population out says so there, rather
  than leaving the previous run's table standing under a new run's name;
- [The mutable ceiling (taken)](#the-mutable-ceiling-taken) and the shipping
  paragraph closing [the Lemire section][lemire]. These are *rulings resting
  on figures*, so a stale number re-opens a decision rather than merely
  misreporting one --- and a ruling's number moves for reasons its verdict does
  not. Both now carry two regimes, and the Lemire one turns on which regime
  orthotope compiles under, so a run in a third would have to say what it does
  to that decision rather than only to the figure. Requote from the run; do
  not carry forward;
- [The C-gap](#the-c-gap-still-a-deeper-ceiling), whose figures are horde-ad's,
  not a run's: no run here replaces them, and they move when that repo
  re-measures --- so the walk checks their currency instead;
- [The scratch vector flavour](#the-scratch-vector-flavour), whose figures
  are a probe's too, and whose conversion is why no `bq-*` figure predating
  it is comparable with one after it;
- [One element type](#one-element-type-and-what-the-probe-found), whose figures
  are a probe's and which no run replaces either. What would call for re-probing
  is a run that moves the ordering at `Storable Double`, since the claim
  is that the other types follow it --- which Run 8 does, in a regime the probe
  was not run in, so the trigger is live and is [on the open
  list](#what-is-open) rather than discharged here;
- [The two-stage plan and the rework
  proposal](#the-two-stage-plan-and-the-rework-proposal), whose figures
  are a scratch probe's and which no run replaces until Run 20 rosters
  the rework's arms --- whose tables then supersede the probe magnitudes,
  and the section is re-read against them;
- [Other toolchains, probed and not run](#other-toolchains-probed-and-not-run),
  whose figures are a probe's on another compiler and another backend and which
  no run here replaces: what would call for re-probing is a move in either
  toolchain, so the walk checks their currency instead;
- [sum-only](#sum-only-and-the-correction-now-applied), where what a run decides
  is no longer *whether* to correct but whether the term still passes its three
  gates, any failure invalidating the column rather than informing it;
- [R2 is the ramp detector][ramp], [the Lemire section][lemire], and [the
  per-shape `stretch-*` table][pershape];
- [what the benchmark does](#what-the-benchmark-does), whose two roster rulings
  quote the run they were cut on --- the arms they drop and the allocation tier
  the threshold sits above --- and whose membership a later ruling can reopen;
- [the non-urgent TODO list](#non-urgent-todo-list), whose roster-order entry
  cites the position figures a run measures and whose decomposition entry cites
  the question a run leaves open --- the one part of the harness chapter a run
  touches at all;
- the `alloc` column's shape-dependence, refuted and confirmed refuted at full
  budget: every multiple quoted anywhere is a property of a strategy
  *and* a shape set, so pin the shape set before comparing across runs,
  as `time` already asks --- and now a property of the regime too, three
  of the column's levels having moved with the flag alone;
- [What is open](#what-is-open), whose whole content is questions a run answers
  and figures a run moves;
- this section, whose delta chain gains a bullet for the run just read;
- `read-run.py`'s docstring, whose `time`, `corr` and `net` definitions and A/A
  paragraph quote the run;
- `micro.cabal`'s `-M8G` note, if the printed heap peaks have moved;
- `Main.hs`, wherever a comment cites a figure --- now `fbBQmutRunsGmMulback`'s
  margin over its control and `fbBQscanMulback`'s settled prediction, every
  other comment having been rewritten to name an ordering and point here
  for the number. The `diag` allocations at `baseOffsetsScan`
  and `baseOffsetsScanPacked` move with the regime rather than with a run.

**And what a run does not touch.** The converse of that list is worth stating,
because a session told to make a run will reach for everything: a new
measurement bears on figures and on rulings whose figures moved, and on nothing
else. It does not bear on the *reasoning* behind a decision, on the ideas
recorded as having died on paper, on the shape-set, roster and stride-class
rulings, or on the account of how the fix was found. Those change when
an argument changes, which a run is not. If a run seems to call for rewriting
one of them, that is a finding worth its own paragraph, not an edit to be folded
in quietly.

How a run is made, and what to record beside its numbers, is [Making a major
benchmark run](#making-a-major-benchmark-run) --- which is also where the walk
of the list above is one of the steps.



[achieved]: #how-the-strictly-positive-picture-was-achieved
[bench]: #what-the-benchmark-does
[ceiling]: #the-mutable-ceiling-taken
[cgap]: #the-c-gap-still-a-deeper-ceiling
[classes]: #the-stride-classes-and-what-they-cover
[correction]: #sum-only-and-the-correction-now-applied
[dead]: #dead-ideas
[fix]: #the-fix-in-dataarrayinternalhs
[floor]: #what-moves-a-figure-when-no-strategy-changed
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[open]: #what-is-open
[opening]: #regime-3-micro-benchmark-the-regime-3-fix
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
[probe]: #one-element-type-and-what-the-probe-found
[procedure]: #making-a-major-benchmark-run
[prov]: #provenance
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[reader]: #the-reader-read-runpy
[results]: runs/run19.md#results
[settled]: #what-is-settled-and-where
[scratch]: #the-scratch-vector-flavour
[shapeset]: #the-shape-set
[todo]: #non-urgent-todo-list
