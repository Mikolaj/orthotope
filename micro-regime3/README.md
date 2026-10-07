# regime-3 micro-benchmark (the regime 3 fix)

This branch (`speedup-strided-tovector`) changes `toVectorListT`'s regime-3
fallback in `Data/Array/Internal.hs` --- the per-element path taken when
the innermost dimension is strided, so no contiguous run longer than one element
can be sliced out. What the branch carries in code is the stage-one fix, landed
2026-08-24: `vFillStrided`, the class method, and its shared driver (stage two
is on
[`pr-mikolaj-toVectorListT`](https://github.com/Mikolaj/orthotope/tree/pr-mikolaj-toVectorListT),
at parity with stage one since the unboxing fix of 2026-08-29, [the
ceiling](#the-mutable-ceiling-taken)'s tenth reading). **The regime 3 fix
is decided: the `mut-odo-vecdims` family in its `add-in-leaf-u2` form,
with no stride-conditioned redirect** --- [the
ceiling](#the-mutable-ceiling-taken) carries the decision and what it rests on,
and [the two-stage plan](#the-two-stage-plan-and-the-rework-proposal) below
carries the drop and the rework proposal the redirect's evidence now feeds.

The previous attempt, benchmarked as `gen-quotrem` resulted in a **mixed
picture**: it had replaced the original `list` fallback

    [vFromListN l $ toListT sh a]                       -- build/foldr list

with a `vGenerate` over a per-element `quotRem` (one division *per dimension*),
which sped up the large, many-channel shapes but *slowed* the small, shallow,
high-rank shapes that dominate horde-ad's convolutions (up to ~2x).

The fix before stage one, and `vFillStrided`'s class default since,
is **`bq-expand`**: precompute the base-offset of each innermost run once ---
the outer-base grid is separable (`o0 + sum idx_d * stride_d`), so it is built
by iterated `concatMap` / `enumFromStepN` expansion, no division
and no thunk-list --- then fill the result with a single `vGenerate` doing
**one** `quotRem` per element. It beats the original `list` fallback on every
benchmarked shape with no regression and needs no extension to orthotope classes
--- **that is the FILL**, and `lib-stage1`, the stage-one route as it shipped
--- its fill `fillStage3` behind a `walkAx` conversion, and so no longer
the library's own --- is slower than `list` on the shortest run of the `runs`
class this roster times, `runs-2`, which [the run file's property
1](runs/run45.md#the-properties-the-next-run-should-test) records.

The words for a view's pieces are the library's, defined at the `T` haddock
of `Data/Array/Internal.hs` on `pr-mikolaj-toVectorListT`: a *walk* is one
traversal of the innermost dimension; an *innermost run* is what one walk
yields, consecutive in the result whatever its stride; a *contiguous run*
is a stretch consecutive in the source and in the view's order, which
an innermost run is at stride 1. Unqualified, *run* means the innermost run
in fill prose and the contiguous run in route prose, and a benchmark run
is written Run 27, or capitalised where a sentence would otherwise read two
ways.

**A direct mutable result buffer is faster still**: `mut-odo` walks the outer
odometer and writes each innermost run, and `mut-odo-vecdims` --- the same fill
with its dimension lists replaced by unboxed vectors --- is on Run 45 (plain
-O1, -A32m, exit span, settled cost, GHC HEAD `10.1.20260918` patched
under its unchanged version, launched from disk) **2.86x** over `bq-expand`
paired, ahead on all nineteen shapes. **That headline moves with the published
REGIME and with where a build places `bq-expand`, and not with the COMPILER**:
on plain -O1 it has read 2.83x to 2.87x on every build from Run 29 to Run 45
but Run 41's, whose basis placed `bq-expand` 4% slower and read 2.97x, and Run
43's, whose published 2.89x is its main set's second process, which ran
`bq-expand` 1.5% slower than the first process of the same binary, reading 2.85x
([Run 43's file](runs/run43.md)), and 2.84x to 2.86x on the GHC HEAD halves Runs
32 to 35 carried. **TWO of `-O2`'s passes cost this headline what the whole
level cost it**: with `-fspec-constr -fliberate-case` on plain -O1 it reads
2.18x to 2.20x on every build from Run 36 on, Run 45's 2.18x the lowest, against
the whole level's 2.19x on Run 31, across two compilers --- so raising the level
costs the headline better than six tenths of a multiple and those two passes
are where the cost lives, `-O2` speeding `bq-expand` by 29% and leaving the fill
where it is; the gap this ratio reports is the one the library actually compiles
in. **One main-set shape sits on the line**: on `stretch-pow2stride` the fill
and `bq-expand` tie, class property 1 breaking on whichever half reads the fill
behind, and whether any run reads it behind by more than its floor is [an open
question][open], which carries every draw. **The mutable fills hold the top
of the table** --- `lib-stage3-lean` and `lib-stage2-lean` at 0.023,
`lib-stage2-disp` at 0.024 and `lib-stage2-lean-u1` and `lib-stage1` at 0.025
([the run file](runs/run45.md#results)), and the shipped leaf at 0.026, against
`mut-odo-vecdims`'s 0.045 --- and every one of them needs a new `Vector`-class
method, which the decision of 2026-08-22 **took** ([the
ceiling](#the-mutable-ceiling-taken)). Plain `mut-odo` does not argue for
it at all: it and `bq-expand` are a tie at 0.8906 paired, 14 shapes of 26
and sign p 0.85 on an interval covering 1 --- and at 0.8918 on Run 24's HEAD
half, a thousandth away, so the tie is not one compiler's.

**Several strategies measured since are faster than the last candidate,
`bq-expand`, and need no class method --- a distinction the decision
of 2026-08-22 retires, shipping the mutable family's arm instead.** The fastest
pure ones are **`bq-scan-rem-gm-mulback`** and **`bq-odo-gm-mulback`**, and what
survives of that ordering is the pure yardstick [the mutable
ceiling](#the-mutable-ceiling-taken) prices the shipped arm against, which
is where its figure is kept and requoted. **The per-run margin over `bq-expand`
is retired with the candidacy and is not to be re-quoted**: no decision turns
on it now that the class method has landed. They also carry **no size
precondition at all**, which is the point of them, a ruling since having stopped
this suite timing any arm that needs one ([what the benchmark
does](#what-the-benchmark-does)). Of the trade-offs, allocation and the noise
floor --- measured per run over the A/A pairs of each half, and quoted
with its carrying pair in [the floor section][floor], which owns it ---
are in [Results](runs/run45.md#results), each arm's precondition is at its entry
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

And **one regime's**, **one roster's** and **one layout's** as well. Runs 8
to 29 compiled the suite with `-fspec-constr`, the runs before them at the plain
-O1 a default `cabal build` of orthotope takes, and every run from Run 30
publishes its basis on plain -O1, as ruled on 2026-09-13 ([the open
list][open]), its control half free to carry flags; the flag reorders the table
rather than nudging it, **Run 29's pair** reading `list` 13.79% and `bq-expand`
28.04% apart between its halves, which is the figure to quote between runs
on either side of that ruling. **The whole level the flag is one pass
of reorders it too**: on Run 31 `-O2` was worth 29.74% to `list` and 29.43%
to `bq-expand` and nothing measurable to the shipped fill, so a table published
at -O1 and one published at -O2 are two orderings of the same arms rather
than one table with a scale factor. **The COMPILER is not such a factor**: asked
at one level by Runs 32 to 34, it moved `list` by under half a point each time,
and the one large reading, a class arm's 29.5 points on Run 33, is since read
as the basis file's page frame and did not reproduce on Run 34 ([the open
list][open]). The roster and its order move figures as much --- Run 9 changed
the roster alone and moved arms from 9% faster to 19% slower with the baseline
standing still, Run 10 the order alone and moved them 3% faster to 14% slower
--- and so does where a build places the loops ([the floor section][floor]).
So a figure here belongs to a flag, to a membership, to an order *and*
to a layout, and the last is the one this README can now remove rather than only
price. **Whether orthotope should carry the flag library-wide is
not this README's question** and is deliberately not on its open list:
that decision is about compile time and code size across the library,
and the measurement that would settle it is horde-ad's `convVjpBench`
over a real build, to which this README contributes Run 29's pair. **At module
scope it is settled (2026-08-24): the shipped file does not set
`-fspec-constr`**, the aligned HEAD probe having read the flag irrelevant
to the shipped family ([the ceiling](#the-mutable-ceiling-taken)).


### The two-stage plan and the rework proposal

**Decided 2026-08-24: the fix ships in two stages, and the stride-conditioned
redirect is dropped rather than deferred.** Stage one is what goes upstream now,
landed on this branch 2026-08-24: `vFillStrided` with its driver, the vecdims
family's `add-in-leaf-u2` arm --- refined from plain `mut-odo-vecdims`
by the two paired probes the ceiling records --- for regime 3 alone,
with no condition on the strides --- the prototype this replaces, a compound
strategy with `mut-odo-vecdims` as the main element and one to three per-shape
or per-stride redirects around it, is dead. Stage two is a rework
of `toVectorListT`'s whole dispatch, all regimes, whose own evidence is what
killed the redirect --- it shows the redirect's constituency dissolving
at the dispatch, and what remains of regime 3 after it is stage one's arm.
**It is implemented, 2026-08-27, on the permanent branch
[`pr-mikolaj-toVectorListT`](https://github.com/Mikolaj/orthotope/tree/pr-mikolaj-toVectorListT):
the canonicalization, the dispatch on it, `toUnorderedVectorListT`'s one-block
test on it, `toVectorT`'s route through the fill, the two zero-stride conditions
in the driver, the Storable test modules wired into the suite,
and `Data/Array/Internal/FastReshape.hs` removed as subsumed.** It was written
as if Run 20's readings were complete and binding and as if the compiler's
codegen were fixed ([the ceiling](#the-mutable-ceiling-taken)'s fourth reading
says what is not), so every figure below is the benchmark's and none
is the branch's: what the branch owes is horde-ad's end-to-end run
and `stretch-tall-Mx2`. This section keeps what the design rests on; the design
itself is the branch's code and its commit messages.

**The redirect's measured constituency is unit dimensions and zero strides,
not stride classes.** [The ceiling](#the-mutable-ceiling-taken) names every
place an outside-family arm leads `mut-odo-vecdims`: the `reshape1` class,
`stretch-inner1`, `window-64x64-k1x9`, `bcast-tall-Mx2`
and `stretch-pow2stride`. All but the last are views with a unit innermost
extent or a zero stride --- and both properties mark work the fallback need
not do at all, where a redirect to a flat table arm still does all of it,
and at `sInner` 1 pays twice the result vector in allocation for a table as long
as the result.

**The first half is canonicalization before the dispatch --- drop unit
dimensions, merge adjacent dimensions where `st_outer == n_inner * st_inner` ---
with the regimes classified on the canonical dims.** What that reclassifies,
in this README's populations: `reshape1-*` and `stretch-inner1` become regime 1
outright; `window-64x64-k1x9` becomes canonical regime 2, contiguous runs of 9;
the conv patch tensors stay regime 3 at lower rank, `cnn-L2-24x24-c32` falling
from rank 5 to 3. After unit-drop no regime-3 view has `sInner` 1, so the flat
table arms lose their constituency structurally, not behind a predicate.

**The second half is the zero strides specialized inside the one remaining fill,
as conditions on the odometer rather than strategies beside it:** a zero
innermost stride (the `bcast` class) hoists the run's one read; a zero outer
stride (`bcastmid`, any broadcast axis) fills the block below it once
and block-copies it. A third condition, a contiguous copy at canonical innermost
stride 1 (`window`), Run 20 refused: `canon-memcpy-r2` is BEHIND the arm
it varies on `window`, 1.0636 at 0 of 3, because after the unit drop
the stepping loop at stride 1 already is the run copy and a `memcpy` per run
of 3, 5 or 9 loses to it --- so that branch is dropped for every run length
the roster has a shape for, and earns a place only on one it has not. Both
conditions are decided per level of the odometer and never per element.
**The run body must not be a closure chosen once per call** --- `bcast-set`'s
form, `writeRun = if tInner == 0 then set else step`, and the branch's first
port of it: an unknown function at every run site, so the fill no longer inlines
into the run loop and every run pays a call, which is the per-run cost the leaf
fusion was measured to remove. The branch's driver instead takes the run body
as a static argument of an `INLINE` fused level, chosen once per row of runs,
so each choice inlines its body; `bcast-set`'s 0.057 against 0.054 on the main
set, inside the floor, is what that closure form is expected to have cost.

**A scratch probe priced the proposal, and its timings are anecdotal
by this README's standards --- magnitudes only, nothing finer.** The instrument:
in-process fixed-iteration differencing at -O1 `-fspec-constr` and -A32m, each
arm correctness-gated against a naive per-element reference, on a box carrying
about one core of foreign load; only reads past 1.5x were kept,
and those reproduced across two processes within about 20%. **Run 20 rostered
all five pieces --- `canon-vecdims`, `canon-memcpy-r2`, `canon-full`,
`bcast-set` and `mid-copy`, across the main set and all eight classes ([Run 20's
file](runs/run20.md)) --- and its tables replace the probe's magnitudes wherever
the roster has a shape.** What held: the regime-1 return is O(1), three
`reshape1` shapes and `stretch-inner1` reading work removed rather than shrunk;
`window-64x64-k1x9` reads 0.020 against `mut-odo-vecdims`'s 0.095,
and that factor is canonicalization's alone; the block copy takes `bcastmid`
outright, `mid-copy` 0.5490 at 4 of 4; the two controls canonicalization cannot
touch --- `stretch-primes` exactly, `cnn-L2-24x24-c32` up to its merge --- read
ties to the thousandth, so the pass costs nothing where it does nothing;
and every new arm allocates at the mutable fills' own 1.00x. What shrank:
the hoisted read, `bcast-set` 0.9230 at 3 of 3 on `bcast` and a tie
on `bcast-tall-Mx2`, where the probe had read a factor. What fell
is the run-copy branch, above. The probe's own figures stay only for the analogs
the roster has no shape for.

**One reclassification is not free, and it bounds what canonicalization may do
alone.** Promoting the window view into today's regime 2 --- the slice-per-run
list `toVectorT` then concatenates --- read a tie with `mut-odo-vecdims` on time
and 4.59x the result vector on allocation, some 260 bytes of slice header
and list per nine-element run. So promotion to regime 2 comes only with a direct
fill --- `toVectorT` fills a canonical-regime-2 view through the driver's
stepping loop, which at stride 1 is the run copy, and `toVectorListT` keeps
the slices for the consumers that iterate them --- while promotion to regime 1
is the one reclassification free by itself. The ruling of 2026-08-25 behind
the whole of regimes 1 and 2: dispatch work and one consumer route, never
per-regime strategies, and the class method and its instances do not move again.
What stays open is only whether a NATIVE regime-1/2 input differs
from a regime-3 view that canonicalizes into those shapes; nothing here can
exercise one, and the question earns work only if `toVectorT` over native
regime-2 views shows up hot in horde-ad.

**On allocation the proposal never leaves the 1.00x tier and twice goes
under it** --- and these figures are exact, allocation being deterministic per
call. The hoisted read and the block copy allocate the result and single-digit
bytes more; canonicalization's own transients stay under two unpinned kilobytes
per call, 1.01x on the smallest probed view and vanishing on the megabyte ones;
and the regime-1 hits allocate about 470 bytes against `mut-odo-vecdims`'s
4.0 MB on the `reshape1-500k` analog --- minting no pinned buffer at all where
every materializing arm mints one, the small-pinned currency
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
`add-in-leaf-u2` arm; stage two changed the driver's internals and the dispatch
around it and the class not at all. Rejected the same day, so they
are not re-proposed: a `vCreate` handing the callback the mutable buffer, which
is what would need the `Mutable` associated type; the per-element `vBuild`
alone, which cannot express a block copy or a contiguous-run copy and so buys
a second method later; a CPS extension handing the callback write-and-copy
functions, which avoids `Mutable` but is more surface than the whole-kernel form
for the same wins; and the FastReshape `unsafeCast` escape, an instance-side
trick with no `Storable` evidence at the generic call site. One debt travels
with the choice: the `build`/`mut-odo` identity was dumped
for the single-callback `vBuild` form, so the driver's workers are
to be re-dumped in this form before any figure of theirs is trusted. Nothing
else couples the stages: post-canonicalization every population this README
measures keeps the vecdims family at its head, the one residue being
`stretch-pow2stride`'s 10%, which is cache aliasing and [the
C-gap](#the-c-gap-still-a-deeper-ceiling)'s to close.

**The rework's arms are five, checked and not timed** --- `canon-vecdims`
and its memcpy-run form `canon-memcpy-r2`, the zero-stride conditions
`bcast-set` and `mid-copy`, and the endpoint `canon-full` --- against the four
pieces the proposal describes: the composite canonicalizing arm,
the hoisted-read fill, the block copy and the contiguous-run copy. **Every one
of the five varies plain `mut-odo-vecdims`, not the leaf body the branch ships**
(`Main.hs`, the rework-proposal family's header), so Run 20 priced
canonicalization and the leaf block separately and composed them nowhere:
`canon-vecdims` reads 0.049 against its control's 0.054 on the main set while
`-add-in-leaf-u2` reads 0.038, and on `window` the shipped arm at 0.032 beats
`canon-vecdims` at 0.037 doing none of the rework. Stage two's driver
is therefore written on the leaf body, and the composite over
it is `lib-stage2`, the branch's `toVectorT` ported whole, at parity
with `lib-stage1` since the unboxing fix of 2026-08-29 ([the ceiling][ceiling]'s
tenth reading). `reshape1` goes degenerate for the canonicalizing arms, whose
cells there price dispatch rather than filling, so the class carries
the non-collapsing `reshape1-strided-r3`, `reshape1-r3`'s shape made strided,
the only cell in the class that prices the fill.

**Weighed and dropped within the proposal, so they are not re-proposed
with it:** tiling for the page-aliased stride (10% on one probe shape whose own
comment bounds damage rather than ranking); size thresholds in the dispatch
(nothing measured needs one after canonicalization, and the no-precondition
ruling stays whole); normalizing strides at view construction (observable
through the API, so the pass stays local to `toVectorListT`); and algebraic
shortcuts in reductions over broadcasts (the consumer's business,
not this fallback's).


## Contents

History is not here. `../MARGINALIA`, at the repository root, is a write-only
journal and not something to read: it exists because the models working here
keep putting history inside instructions, and it is where that goes instead
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
  - [Standing rulings from past runs](#standing-rulings-from-past-runs)
  - [Non-urgent TODO list](#non-urgent-todo-list)
- [The goal of these benchmarks](#the-goal-of-these-benchmarks)
  - [How the strictly positive picture
    was achieved](#how-the-strictly-positive-picture-was-achieved)
  - [Where the shapes come from](#where-the-shapes-come-from)
  - [The shape set](#the-shape-set)
  - [Dropping the minibatch dimension](#dropping-the-minibatch-dimension)
  - [The stride classes and what they
    cover](#the-stride-classes-and-what-they-cover)
  - [Which population answers a question, and how to ask all
    of them](#which-population-answers-a-question-and-how-to-ask-all-of-them)
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
  - [Making a major benchmark Run](#making-a-major-benchmark-run)
  - [Other toolchains, probed and not run](#other-toolchains-probed-and-not-run)
  - [The reader: read-run.py](#the-reader-read-runpy)
  - [Reading a run file](#reading-a-run-file)
  - [What moves a figure when no strategy
    changed](#what-moves-a-figure-when-no-strategy-changed)
  - [R2 is the ramp detector, not the noise
    detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now
    applied](#sum-only-and-the-correction-now-applied)
- [Run 45](runs/run45.md)
  - [Results](runs/run45.md#results)
  - [What the next run compares
    against](runs/run45.md#what-the-next-run-compares-against)
  - [The properties the next run should
    test](runs/run45.md#the-properties-the-next-run-should-test)
  - [The stride classes, run
    by run](runs/run45.md#the-stride-classes-run-by-run)
  - [Provenance](runs/run45.md#provenance)
  - [What this run was built to answer, and what it
    answered](runs/run45.md#what-this-run-was-built-to-answer-and-what-it-answered)
- [Provenance](#provenance), README's own


## What is settled, and where

**One line per thing this README has established, and the section that holds
it.** It exists because the file is long enough to re-derive itself. Read
this before deriving anything and grep it before writing anything up.

**It carries no figures, and that is the design.** A figure here would
be a second copy of one kept elsewhere, and go stale. Each entry names a subject
and a home and stops; the numbers live at the home and move with the run.
An entry earns its place by being a thing a later session might otherwise redo.

- **The `bq-expand` fix** and why the base-offsets table is built by expansion
  rather than by division: [the fix][fix], with the four findings behind
  it in [how the picture was achieved][achieved]. That form is now the last
  candidate: the decision of 2026-08-22 is [in the ceiling][ceiling].
- **The mutable ceiling**, the decision of 2026-08-22 that takes it ---
  the `mut-odo-vecdims` family as the upstream implementation, narrowed
  on 2026-08-24 to its `add-in-leaf-u2` member and landed in code the same day,
  alone since the drop that sent the stride-conditioned redirect to [the
  two-stage plan](#the-two-stage-plan-and-the-rework-proposal) as a rework
  proposal --- and the readings behind the shipped form: [the ceiling][ceiling].
- **The class-method signature is free** --- `build` and `mut-odo` compile
  to the same worker, dumped in both regimes --- so no `vBuild` is held back
  on a figure: [the ceiling][ceiling].
- **The lean dispatch is taken**, 2026-09-05, for every dispatch that admits it,
  `lib-stage2` alone keeping the strides comparison as its control; the ruling,
  its grounds and what does not admit it: [the stride
  classes](#the-stride-classes-and-what-they-cover).
- **The list `toVectorListT` and `toUnorderedVectorListT` return stays lazy**,
  2026-09-07, up to one exception, a view moved between laziness patterns
  by canonicalization alone; the ruling, the exception, what it forecloses
  and what it leaves outside, `toVectorT` being strict whichever way
  it is built: [dead ideas][dead].
- **The run-length dispatch is taken inside the fill**, 2026-10-06, overriding
  the ruling of 2026-09-07 that kept it out of `toVectorT`: each run at stride 1
  at least as long as a length each `Vector` instance picks copied whole,
  and `lib-stage2-disp`, the slice-list form, retired: [dead ideas][dead].
- **Code placement moves figures**, and by more than the A/A controls can see:
  the identical-code pair, the rebuild bias, the per-loop reading
  and the cache-line table are all [in the floor section][floor]. **Straddling
  a cache line is a cost and not a correlation** --- the pad probe stepped two
  arms through every offset --- **and the penalty is graded** by where the split
  falls: same section. **But it is not the account of every gap**: Run 10 read
  three arms at four placements each and two of them kept their 16% with no copy
  straddling anywhere ([the ceiling][ceiling]'s FastReshape arms). The probe's
  own design, including the two kinds of pad that relocate nothing, is [on
  the open list][open] with what is still open about placement.
- **GHC's native backend aligns no loop**, where GCC, clang and GHC's own LLVM
  backend all do; `-fproc-alignment=64` pins the offsets rather than choosing
  them, and an assembler shim on `-pgma` aligns the loops outright, which
  is the instrument fix. What it costs and buys in time is [on the open
  list][open]; the rest is [in the floor section][floor], including why the shim
  must pad only between instructions. Two tools in horde-ad:
  `tools/loop-offsets.py` reads a binary's copies, which makes the question
  a minute's work rather than a run's, and `tools/align-as.py` is the shim;
  a paired Run's two binaries are built from the recipes its own note carries,
  one per half. Both this and the recompilation trap beside it are written up
  and filed as GHC issues from horde-ad's `docs/`, which is where a reader
  outside this README should go; what stays here is what they cost
  this benchmark.
- **Which arm owns a loop copy is a property of the binary**, absent
  from a plain build and carried by a `-g3` one, which `tools/loop-offsets.py`
  now reads for itself --- and **a `-g3` build is a twin to read and
  not a binary to time**, that having been gated and lost. The map
  of the vecdims group, the reading of Run 11's split it corrected, and what
  `-g3` costs in emitted code and in time are [on the open list][open].
- **The allocation area moves figures too** --- the default nursery against
  an arm's allocation in excess of its result --- with the predictor [in
  the floor section][floor]; and since 2026-08-21 it is fixed at `-A32m`, here
  and in every horde-ad suite, never to vary again ([Running it](#running-it)).
- **The A/A controls are the noise floor**, not the printed CI, and what they do
  and do not bound is [in the floor section][floor]; R^2 is the ramp detector
  rather than the noise detector, [here][ramp].
- **Run-to-run drift, with shapes, roster, order, regime and layout all
  pinned**, measured by re-running one binary: a few percent per cell, a quarter
  of a percent on a geomean, and two arms that exceed it, [in the floor
  section][floor].
- **The forcing pass is subtracted from every figure**, on three gates
  that every run and every population re-passes: [sum-only][correction].
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
  is checked without being timed: [what the benchmark does][bench]; and
  by a third cut on 2026-09-04, the prune to the family's shipping question,
  in the same section.
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
not**. `OPEN` wants a measurement that is available; `PARKED` is open
but its route is retired, and the entry says why; `ANSWERED` records an outcome
and is kept so the question is not re-proposed; `STANDING` is a ruling
or a convention with nothing to run. `grep -E '^(- |[0-9]+\. ).OPEN.' README.md`
is the list of live questions, and the one that answers a session's first
question about this section --- the alternation being there because a numbered
item is an entry too, so a bullet-only pattern would read a numbered subsection
as empty rather than as clean. The status is a pointer and never the authority:
the entry's own text is.

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
`--check-doc` FAILS the file for any `ANSWERED` entry past five hundred words,
with three truthful ways out that the failure itself names: move the account
to the section that owns it, give a run registration the family's lead, or say
in a bolded clause carrying `only copy` that there is nowhere to move it.
That last is what makes a gate honest rather than coercive,
`bq-scan-packed-mulback` being the live case of an answer nothing else records.
**Length is the whole test**: a condition that the entry also point nowhere
would be an off switch, this README cross-referencing constantly enough
that every long entry names a link or a file. **The one exemption
is the registration family**, matched on the lead its members share --- *What
Run N was built to answer* --- and counted rather than dropped, the sweep's own
line saying how many it passed over. A member that drifts out of that phrasing
loses the exemption and gets listed, which is a failure a reader can see.

**A run's registrations live in the file of the run that made it, and what stays
here per run is a stub**: the lead, a verdict in a clause and a link
to that file, `runs/` accumulating a file for every run from 7 on. A stale
marker does not merely mislead, it exempts --- which is why `--check-doc` holds
a registration's marker to its own items.

**This is the only home for an open question.** They are collected here because
otherwise they sit one per section and get reconstructed every time ---
and worse, get missed: the question of why the count-down FastReshape form pays
was raised inside [the mutable ceiling][ceiling]'s own write-up and left there,
so a session that mined this list and its queue walked past it. A question
recorded anywhere else is a bug to be moved here, not a note to be left where
it was written. The harness's own backlog is folded in below, for the same
reason: two backlogs a thousand lines apart is how one belongs to neither.

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

**And it raised a larger one, answered the same day: what warms the expansion
family?** On `vgg-14-c512-k3`, `bq-expand` and three arms beside it ran 35--40%
slower in a small process than at their published roster slots: the **default
4 MB nursery** against an arm allocating 13.2 MB per call beyond its result,
warmed by one predecessor, `sum-only-early`, whose setup allocation grows
the block pool and leaves it grown. The account is [in the floor
section][floor], and the roster fix it carried puts `sum-only-early` above
`list`, so nothing is measured on an ungrown pool.

- `ANSWERED` **What the next run's two binaries are is declared in TWO places,
  and that is a source of contradictions rather than a redundancy worth
  checking.** **Ruled 2026-09-19 by the owner: the REGISTRATION
  is the declaration site.** The pair, its half names and its recipes
  are written once, in the open list's `What Run N is built to answer` entry,
  which is what the run is judged against; the previous run's *What the next run
  compares against* names it as `[registered <date>][open]` and restates
  nothing, and the pair note is filled in from it.
- `ANSWERED` **An arm parts 3.70 points across the halves and it is one half's
  BINARY OR ITS FILE INSTANCE, which only the half-local reading can say ---
  and it is the INSTANCE, taken 2026-09-20 in two passes, the first of which
  answered wrong.** **It is the INSTANCE.** Fresh disk copies of the two
  controls read level within 2.5 points on every cell
  but `alexnet-L1-55-c3-k11`, where Run 37's is the faster at 0.935, their hot
  loops byte-identical, while Run 37's launch instance reads **1.139** against
  its own fresh copies on that cell --- a slow 4 KiB draw; a first pass had read
  level only because its one copy was itself a slow draw, which is why
  a one-copy gate is blind one launch in ten. Run 38, built again from the same
  recipes, reads the arm at **1.0205** with counts level. The readings are [in
  Run 37's file](runs/run37.md) and [Run 38's](runs/run38.md).
- `ANSWERED` **What Run 45 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 45's own
  file](runs/run45.md#what-this-run-was-built-to-answer-and-what-it-answered),
  where a run's registrations have lived since 2026-08-29; in a clause each: (1)
  the count-down level loop gave `lib-stage2-lean` back what Run 44's bounded
  loop cost it, `lib-stage3-lean` over it reading 1.0053 on `stretch-wide-2xM`
  against 1.02 within 4% and 1.0013 over the main set against 1.00 within 1.5%,
  on the basis; (2) `lib-stage0`, master's route, runs 35.0472 times
  `lib-stage1` against a band of 27.8 drawn from cycles, KILLED; (3)
  `lib-stage2-disp` reads with `lib-stage2-lean` on the main set, 1.0021
  and 1.0017, and on `small`'s control, 0.9992, and is KILLED on `small`'s basis
  at 0.9873 on instructions level to 1e-3, a placement; (4) `sortAxes` saves
  stage thirteen at least 115 instructions a call against stage fifteen on every
  main-set shape and 126, 173 and 272 on `bcast`, `compose` and `bcastmid`,
  and reads 0.9879 of its time against 0.991 within 0.8%; and (5) the source
  reached nothing the passes compile on `list` and `bq-expand`, their counted
  work at 1.2929 and 1.5063 to the fourth decimal and their crosses at 1.2929
  and 1.3048 inside 1% of 1.2965 and 1.3% of 1.3096 --- eight of the ten spans
  HELD on every reading, item (2)'s KILLED and item (3)'s KILLED on one
  of its four, 14 of the 16 readings held.
- `OPEN` **`lib-stage0`, master's route, ran 35 times `lib-stage1` in Run 45's
  timed processes, where the four prior cycle sweeps at `N=50` read it 26.4
  to 29.2 times, and the counter that would say why does not read
  under the preamble.** Run 45's registration (2) drew its band from four cycle
  sweeps, 26.4 to 29.2, and time read **35.0472** on the basis's main set,
  KILLED ([Run 45's
  file](runs/run45.md#what-this-run-was-built-to-answer-and-what-it-answered)).
  A fifth sweep taken clean after the run reads 28.79 on user cycles
  over the nineteen shapes and 19.64 with kernel cycles added over eighteen,
  the second by a scratch computation, no reader taking `cycles:k`, so kernel
  time runs the other way, `lib-stage1` carrying the larger share of it; a sixth
  under `SATURATE=1`, the state every process the tables read benchmarks in,
  broke the differenced method, 69 of 76 cells NONLINEAR and `sum-only`'s own
  cycles, summed over both arms, 1.19 times the clean sweep's and negative
  on three shapes (`probe-r45-item2k.txt`, `probe-r45-item2sat.txt`).
  The candidate is that state, which this run's riders put at 1.1183 on `list`
  on the basis and 1.1655 on the control, against an arm that allocates
  as `list` does, 25.21x the result vector against `lib-stage1`'s 1.00x. **What
  would settle it** is the two arms timed by criterion in fresh processes, clean
  and under `SATURATE=1`, over the main set: near 29 clean and near 35 saturated
  says the state is the term, and a registration on a `list`-shaped arm
  then draws its band from time rather than from cycles. Since 2026-10-06
  `lib-stage0` is retired by the owner, checked and not timed, so that reading
  wants it timed again.
- `ANSWERED` **The two `-O2` passes made `libunord-stage13-sum` allocate 18%
  more because SpecConstr reboxes the axis `sortAxes` and `insertAxis` cons
  whole, and since 2026-10-05 `Main.hs` keeps SpecConstr off `Axis`.** Run 45's
  flagged half allocated **1.1845** of the basis on that arm over the main set
  ([Run 45's file](runs/run45.md#the-properties-the-next-run-should-test)).
  The STG of the two recipes, read 2026-10-05, puts the allocation in the merge
  loop's caller and not in the loop: SpecConstr specialises `sortAxes`
  and `insertAxis` on their `Axis`, and each step of the sort then rebuilds
  the box the source conses whole, the excess a multiple of 24 bytes a call
  on every main-set shape but `stretch-inner256`, where stage fifteen's bytes
  move too, one box for each axis sorted after the first. The merge loop's own
  specialisation allocates what the basis's does, a step later. GHC
  [#27628](https://gitlab.haskell.org/ghc/ghc/-/work_items/27628)
  is that reboxing and GHC
  [#21562](https://gitlab.haskell.org/ghc/ghc/-/work_items/21562) the boxity
  analysis that would prevent it. `{-# ANN type Axis NoSpecConstr #-}` leaves
  the plain -O1 Core unchanged binding for binding and brings the flagged half's
  bytes to the basis's, within a byte summed over the main set; under the passes
  it moves no other timed arm's Core, only a join point in `check`'s list
  producers besides the sort. `pr-mikolaj-toVectorListT` carries the same
  annotation since 2026-10-05.
- `ANSWERED` **What Run 44 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 44's own file](runs/run44.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the branch's
  conversion code bought no time, `lib-stage3-lean` over `lib-stage2-lean`
  reading 0.9709 on the basis and 0.9840 on the control against 1.017 within
  1.5%, KILLED on both, and `liblist-stage4-sum` over `-stage5-sum` 1.0118
  and 1.0003 against 0.990 within 1.2%, KILLED on the basis and HELD
  on the control; (2) `libunord-stage13-sum` reads with stage fifteen on the two
  grown `compose` views, 0.9985 and 1.0005 on the basis and 0.9999 and 0.9991
  on the control against 1.00 within 3%, and at 0.65 and 0.67 of stage fourteen
  on `compose-bcast-wide` against 0.67 within 6%; (3) the fills `fdcd7a8`
  rewrote and the arms no commit reached keep Run 43's distances,
  `lib-stage2-lean-u1` over `lib-stage3-lean` 1.0767 and 1.0611, `lib-stage1`
  over the leaf 1.0029 and 1.0074 paired, its published columns parting in sign,
  the leaf over `mut-odo-vecdims` 0.6366 and 0.6358, `bq-expand` over it 2.8567
  on the basis and 2.1917 on the control; and (4) the patch left the control's
  counted work level, `list` at 1.2929 and `bq-expand` at 1.5063 to the fourth
  decimal, and the regime's worth reads `list` at 1.3040 against 1.294 within 1%
  and `bq-expand` at 1.3070 against 1.31 within 2.5% --- twelve of the fourteen
  spans HELD on every reading and item (1)'s two KILLED on three of their four
  readings, 19 of the 22 readings held.
- `ANSWERED` **What Run 43 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 43's own file](runs/run43.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the six
  commits move no timed arm's instructions and the lean fills and `lib-stage1`
  keep Run 42's distances, 1.0662, 1.0066 and 0.9928 on the basis and 1.0628,
  1.0044 and 1.0021 on the control against 1.067, 0.998 and 1.003; (2)
  the shipped leaf keeps its lead and `bq-expand` its distance, 0.6416
  and 0.6380 against 0.637, `bq-expand` 2.8893 on the basis and 2.1860
  on the control against 2.86 and 2.19; (3) grown to `sizeCap`, stage fifteen
  pays on `compose-bcast-wide` and costs little on `compose-bcast-nest`, 0.67
  and 1.04 on the basis and 0.66 and 1.06 on the control, and is level where
  it passes no axis; and (4) the regime's worth reads `list` at 1.2950 against
  1.294 within 1% and `bq-expand` at 1.3212 against 1.305 within 2%, on the main
  set's quiet rerun --- all eleven spans HELD.
- `ANSWERED` **Why did the instructions `b7d0ee1` saves in `lib-stage2-lean`
  cost time? The level loop's form and not its placement: bounded by an end,
  it runs slower on this Zen 3 than counting its blocks down, where
  the innermost runs are two elements long --- taken 2026-10-04.** Run 44's
  registration (1) read those instructions as time and was KILLED on both halves
  ([Run 44's file](runs/run44.md)), `lib-stage2-lean` 2.81 points slower
  than on Run 43's basis and widest on `stretch-wide-2xM`. `perf record`
  on that cell names the loop on both basis binaries: the same 46-byte body
  writing two elements, at offset 0 of its line on both, the level loop's exit
  `dec; test; jle` on Run 43 and `mov; cmp; jge` on Run 44, one instruction
  a run fewer, and the fill at 1.13 to 1.15 of Run 43's cycles with the forcing
  pass level. A build of `c100112` with the two fills' level loops exchanged
  (`probe-r44-swap/`), read beside the two runs' binaries, moves the cost
  with the form: in cycles a run of two elements, the whole cell, the medians
  read 10.59 to 10.68 for the counted loop at four placements and 11.39 to 11.40
  for the bounded one at three, the control half's among them. Op-cache windows
  and misses, the op queue, branches and their mispredicts, fills, prefetches
  and TLB misses read the same on both forms, while stalls on a full retire
  queue go from about 0.04 to about 0.22 a run; IBS op samples taken
  from a plain terminal (probe-r44-ibs.sh, `probe-r44-ibs/report-fixed.txt`)
  time each op from dispatch to completion about the same on both forms, within
  a cycle, and find fewer ops in flight on the bounded one, so the loss
  is in how fast ops are dispatched, which no counter read here names.
  On patched copies of the Run 44 basis the exit's `cmp` reading another
  register moves nothing, one op added to the level loop recovers about two
  fifths of the cost, and two or three meet an op-cache limit. **What
  it changed**: `pr-mikolaj-toVectorListT` now counts the loop down, keeping
  it out of GHC
  [#27894](https://gitlab.haskell.org/ghc/ghc/-/work_items/27894)'s float
  with `Fused` holding the innermost outer level's `Axis`, a workaround
  that issue's filed text lists, folded on 2026-10-04 into the branch's commit
  that ported the Axis path; `b5cd52e` ported it to `fillStage2Axes`, so Run 45
  times it. Built from the branch on GHC HEAD with `tools/align-as.py` aligning
  both loops, a client converting a transposed Storable view through `DynamicS`
  reads the counted loop at 0.81 to 0.89 of the bounded one's cycles
  at `[2, 900000]` and 0.92 to 1.04 at three smaller views, on the same bytes
  a call. Counting the remaining elements down from the bound instead spilled
  the source vector's base in the inner loop and ran slower than both forms
  (`probe-r44-c1/`).
- `ANSWERED` **What moved the control's `lib-stage1` on `small`, Run 43's one
  unexplained half-local mover? That evening's PROCESS --- taken 2026-10-04.**
  By the copy test, on the owner's quiet box after Run 44's counts:
  on `small-bcast32/lib-stage1` a fresh copy of `run43-gheadtwopass` reads 0.992
  of the timed file and Run 42's control 1.018, which `--copy-test` reads
  as PROCESS, Run 42's binary reading with Run 43's in fresh processes. The same
  test's other cell, `flip-last-rows/mut-odo-vecdims-aa-distant`, reads
  INSTANCE, the copy at 1.098 and Run 42's control at 1.100
  of `run43-gheadtwopass`'s own file (`probe-copy-test-run43.log`, [Run 44's
  Results](runs/run44.md)).
- `OPEN` **A cross-half figure is read two ways and held to two bars, and Run
  43's comprehension probe could not tell which applies.** The run file's
  Results says `--compare`'s paired ratio per arm "says which half runs that arm
  faster and by how much", and every class block's `Across the halves` line says
  it is "NOT read for the pair's variable" before its own paragraph counts
  strategies past an A/A bar in points; and the head judges an arm's cross
  figure against the cross-half A/A bar `--compare` prints, 0.28 points on Run
  43's main set, where [Reading a run file](#reading-a-run-file) holds a margin
  on that line to the WIDER of the two halves' floors, 0.79% on the same set ---
  a bar three of the five arms the head says clear it do not ([Run 43's
  file](runs/run43.md)). Neither is this run's to rule: both rules
  are the chapter's and older than the run. **What would settle it** is a ruling
  naming which bar a cross-half arm figure faces and what the class line's
  `NOT read` withholds --- the geomean over arms, or every per-arm figure
  under it --- written where the two rules stand, and the head and class
  paragraphs read against it.
- `ANSWERED` **What Run 42 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 42's own file](runs/run42.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) on one path
  `lib-stage2-lean-u1` keeps its distance from `lib-stage3-lean`, 1.0690
  on the basis and 1.0654 on the control against 1.07 within 3%; (2) the two
  lean fills stay level, 1.0005 and 0.9961 against 0.99 within 2%; (3)
  `lib-stage1` over the shipped leaf stays inside the band around where Run 41
  read it, 1.0009 and 1.0058 against 0.993 within 2%, the conversion moving
  it a point where its instructions moved a third of one; (4) stage fifteen's
  placement costs on `compose-bcast-nest` and pays on `compose-bcast-wide`, 2.02
  and 0.37 on the basis and 2.01 and 0.38 on the control, and is level where
  it passes no axis; and (5) the regime's worth reads `list` at 1.2905 against
  1.295 within 1% and `bq-expand` at 1.3097 against 1.33 within 3.5% --- all
  nine spans HELD.
- `ANSWERED` **What moved Run 42's four half-local movers with their counts
  level? The control's file instance moved its `lib-stage2-lean`,
  `mut-odo-vecdims` and `mut-odo-vecdims-aa` on `flip`, and the build moved
  the basis's `lib-stage1` on `rev` --- taken 2026-09-27.** By the copy test,
  on the owner's quiet box after the write-up:
  on `flip-last-rows/lib-stage2-lean` a fresh copy of `run42-gheadtwopass`
  and Run 41's control both read about 1.16 of the timed file,
  and on `rev-cnn-L1-24x24-c1/lib-stage1` the copy reads with the timed file
  and Run 41's basis 0.962 of it ([Run 42's Results](runs/run42.md)).
  The page-frame reading an INSTANCE verdict calls for next wants root
  and was not taken.
- `ANSWERED` **What Run 41 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 41's own file](runs/run41.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) with one fill
  algorithm under both, `lib-stage3-lean`'s lead over `lib-stage2-lean` closed,
  at 0.9904 on the basis and 0.9948 on the control against a prior of 1.00
  within 2%; (2) `lib-stage2-lean-u1`, the fill without the unrolled stepping
  run, costs against the frozen copy what it cost against the nest, 1.0601
  and 1.0638 against 1.06 within 3%; (3) the copy took over the lead
  on the shipped leaf, 0.8911 and 0.8938 against 0.90 within 3%; and (4) split,
  `list`'s cross figure holding at 1.2926 against 1.295 within 1%
  and `bq-expand`'s KILLED at 1.3620 against 1.303, the basis half's family
  having slowed on level instructions --- four spans HELD and one KILLED.
- `ANSWERED` **What Run 40 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 40's own file](runs/run40.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the nest's
  instruction saving reached the clock, `lib-stage3-lean` over `lib-stage2-lean`
  at 0.9656 on the basis and 0.9564 on the control against a prior of 0.97
  within 2%; (2) the rewritten `lib-stage2-lean-u1` gave back most of its gap,
  at 1.0575 and 1.0617 of `lib-stage3-lean` against 1.05 within 4%, where Run 39
  read 1.1203 and 1.1249; and (3) the regime's worth on the untouched families
  held, `list` at 1.2983 and `bq-expand` at 1.3058 against 1.294 and 1.302
  within 1% --- all four spans HELD.
- `ANSWERED` **What Run 39 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 39's own file](runs/run39.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the fill cell
  on `stretch-wide-2xM` is back on both halves, `lib-stage2-lean`
  and `lib-stage3-lean` at 1.0259 and 1.0305 of the `-u1` loop on the basis
  and 1.0301 and 1.0393 on the control, while its pair span died at 0.9790
  on `c0a8aaa`'s rewrite of the inward fill, which the registration predates;
  and (2) `probe-r39-rules.py` names no arm slower past 3% on both halves in any
  population, so no back-edge rule is named for retirement.
- `ANSWERED` **What Run 38 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 38's own file](runs/run38.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the two
  passes are worth 1.2907 on `list` over the eighteen shapes, which names Run
  36's draw the outlier and Run 37's the pair's; (2) `bq-expand` repeats a third
  time at 1.3032; (3) no arm outside the two families joins them, all nine null
  spans inside 2.5%; (4) `mut-odo-vecdims-add-in-leaf-u1` reads 1.0205
  and is back among its siblings, so its move belonged to Run 37's BUILD; (5)
  the four counted-work spans hold at 0.00 to 0.09 of a point across a source
  fourteen commits on; and (6) the fill numbering the pairing added is worth
  nothing outside the floor, its three pairs at 1.0061, 1.0027 and 0.9996.
- `ANSWERED` **A fill-in row whose label is sixteen characters long
  was invisible to every reader of the block, and the draft emitter wrote one
  --- FIXED 2026-09-21 by moving the block's value column to 20.** **THE FIX
  IS THE EMITTER'S AND NOT THE READER'S**, ruled by the owner 2026-09-21:
  `read-run.py`'s `FILL_LABEL` and `preflight.sh`'s same rule still parse a row
  only where TWO spaces follow the label, and `_fill_skeleton`, preflight's
  every `--fill-in` line and `pair-note-template.txt`'s block now write
  a 16-wide label field and then TWO literal spaces, so a label longer
  than sixteen still gets its two where a wider field would only move
  the failure. `md5 gheadtwopass`, sixteen long, had been emitted with one space
  and dropped silently by `--draft`. **What it does not reach** is a note
  already written at column 19: Run 37's row stays unreadable. Case
  `draft-writes-a-fill-row-no-reader-can-read`.
- `ANSWERED` **What Run 37 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 37's own file](runs/run37.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the WIDE
  `list` span KILLED at 1.2960 against 1.3360 and the NARROW one HELD at 1.2950
  against 1.3129, which is Run 36's wild cell not recurring rather
  than the passes moving, and is the outcome the item's own text called
  decisive; (2) HELD on `bq-expand` at 1.3101 against 1.2980, so neither
  the moved source, the launch from disk nor the reboot shows on that arm; (3)
  the sentence HOLDS, no arm outside the two families joining them, while ONE
  of its ten null spans is killed by `mut-odo-vecdims-add-in-leaf-u1` at 0.9630
  moving the BASIS's way, which step 4a puts on the control half at counts level
  and which is now an open entry of its own; (4) HELD on all four counts spans,
  three of them at 0.00 points, which makes the counted work the one thing
  this pair repeats exactly.
- `ANSWERED` **What Run 36 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 36's own file](runs/run36.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) KILLED
  on `list`, the two passes reading 1.3360 where the whole `-O2` level read
  1.2974 and the two single-pass runs compose to 1.3325, so the level's other
  passes hand `list` back; (2) HELD on `bq-expand` at 1.2980, where both
  accounts agree, which is what makes (1) the composition question and
  not the compiler's; (3) the sentence HOLDS, no arm outside the two families
  joining them and the widest at 1.0119, while its two `list`-family spans die
  with (1)'s and for its reason; (4) the sentence HOLDS, the counted work
  parting at 1.2926 and 1.5063 against 1.0383 and 1.0522, while its two family
  spans die on size.
- `ANSWERED` **What Run 35 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 35's own file](runs/run35.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) HELD on all
  twenty-two readings, stage thirteen under stage twelve where a call is short
  and level where it is long, deepest on `small` at 0.8410 and 0.8518; (2)
  KILLED on `scaled` alone, its thinnest view saving only 138 and 136
  instructions where the item asked for more than two hundred on every view,
  and holding on the other ten populations; (3) KILLED by its spans while
  its own sentence holds --- a `counts` span under `--compare` reads one half
  against the other rather than against Run 34, and the two earlier runs
  of this pair read 1.0062 and 1.0063 where the item allowed 0.1%, so the span
  was unholdable when written, where the claim it states reads 1.0000 across
  the runs.
- `ANSWERED` **What Run 34 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 34's own file](runs/run34.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) HELD, stage
  twelve taking stage six's run on `window` on the basis, where an item naming
  no half is read; (2) KILLED by its count clause, stage twelve level with stage
  eleven on every span but retiring more instructions than it on 20 of 154
  tie-view readings; (3) HELD, stage twelve across the halves at 0.9304
  on `window`; (4) KILLED, `runs-48` 4.0 to 5.4% under `runs-96` an element; (5)
  KILLED within the control half, `small-flat64` 5.06% over stage seven against
  4%.
- `ANSWERED` **What Run 32 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 32's own file](runs/run32.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the shipped
  fill HELD on the main set and missed the class band on `window` alone; (2)
  the reference HELD at 1.0043, inside the differencing bar, where Run 31's
  `-O2` moved it 29.74 points; (3) the fused list KILLED, the consumer 3.09
  points off on `runs` against a 3% bar and this run's only kill; (4)
  the odometer over the table HELD on both halves; (5) stage ten HELD and Run
  31's `window` cancellation reproduced on two of its three views; (6) the pass
  where neither change fires HELD, `rev` reading 1.0111; (7) the dispatch HELD
  for a fifth run; (8) the floor pair HELD in all forty-four readings, the two
  halves naming different pairs at 0.66% and 0.68%; (9) the leaf fusion HELD
  at 0.6459 and 0.6358; (10) the allocation levels HELD EXACTLY, every tier
  identical between the halves, where Run 31's was killed; (11) the unrolling
  HELD; (12) the odometer over master's HELD on all four spans; (13)
  the zero-stride move HELD, its `window` span missed on the basis half alone;
  (14) the composed route HELD everywhere; (15) and (16) the two `-list-sum`
  arms HELD and agree to 0.23 of a point where the counts say the routes walk
  one loop.
- `ANSWERED` **What Run 31 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 31's own file](runs/run31.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the shipped
  fill HELD where Run 30's kill fell on it, the three arms reading 0.9956,
  0.9972 and 0.9997; (2) KILLED, `list` moving 1.2974 against a registered 1.17;
  (3) neither kill fired and the `runs` span missed by 15.57 points, the bangs
  of 2026-09-13 having removed what it predicted; (4) HELD, the odometer ahead
  of the table on both halves; (5) KILLED, three `window` views putting stage
  ten behind stage nine on both halves where Runs 29 and 30 found them parting
  in sign; (6) HELD, `rev` reading 1.0244 as Run 30 read it; (7) HELD on all
  four spans; (8) HELD in all forty-four readings, and the whole-set floor
  is the `bq-expand` pair's on the basis and the fill pair's on the control; (9)
  HELD at 0.6417 and 0.6436; (10) KILLED, `-O2` taking `bq-expand` from 2.78x
  to 2.11x and `list` from 25.20x to 23.45x; (11) HELD on both spans; (12) HELD
  on all four; (13) HELD on both kills with the `window` span missed on both
  halves; (14) HELD in every reading; (15) HELD, the user's fold no longer ahead
  of the shared loop on `runs` and `window`, which is what the walker's bangs
  were written to do.

- `ANSWERED` **What Run 30 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 30's own file](runs/run30.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the flag
  on the shipped fill, KILLED on the main set at 0.9891, 1.09 points off 1
  and so 0.09 past its 1% bar --- a margin resting on one capped cell
  and on which statistic is read, which that item's verdict sets out and which
  would reverse on the column the table publishes and the first -O2 pass here
  to make the shipped fill slower rather than leave it alone; (2) the flag
  on the reference, KILLED at 1.1710 on the main set and past the bar on all
  eleven populations, so the two columns are an ordering; (3) the flag
  on the fused list, NEITHER KILL FIRING, its three magnitude spans missing
  because they are Run 29's and read in that run's orientation, the flag worth
  18.27 points on `runs` where `-fspec-constr` was worth 2.21; (4) the odometer
  over the table, HELD at 0.4678 and 0.3947 on `runs`; (5) the list
  over the fill, HELD at 0.5808 and 0.4900 on `runs` and tying inside the floor
  on all five fill classes; (6) stage ten where both changes fire, HELD on both
  kills, its `window` span missing on the control at 0.8863 where the two views
  Run 29 found parting in sign part by twenty-eight and nineteen points; (7)
  stage ten where neither fires, HELD at 1.0244 and 1.0245 on `rev` --- outside
  both floors, as when it was killed on Run 29, and inside the 3% it was amended
  to; (8) `lib-stage1` against the lean fill, HELD and reproducing Run 28's 0.23
  and 0.42 for a third run; (9) the floor with the fill family's pair, HELD
  in all forty-four readings --- and its hand-read half REVERSES Run 29's,
  `bq-expand-aa-distant` carrying the whole-set floor at 0.57% where two runs
  had said the gap was the fill pair's own. Both kills fell on an item
  predicting a no-op, which is the third run running.
- `ANSWERED` **What Run 29 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 29's own file](runs/run29.md), where a run's
  registrations have lived since 2026-08-29; in a clause: (1) the flag
  on the shipped fill, HELD on the main set at 1.0001, 0.9945 and 1.0044,
  with ten of its thirty-three class readings outside 1% on `bcast`, `bcastmid`,
  `block` and `small`; (2) the flag on the reference, KILLED, `list` reading
  0.8788 on the main set and past the 0.7% differencing bar on all eleven
  populations; (3) the flag on the fused list, HELD at 0.9779 on `runs`, 0.9839
  on `block` and 0.9771 on `window`, read raw after a reader defect found
  and fixed in this write-up; (4) the odometer over the table without the flag,
  HELD at 0.4915 and 0.4664 on `runs` and 0.7826 and 0.7220 on `block`; (5)
  the list over the fill without the flag, HELD at 0.5675 and 0.5795 on `runs`
  and 0.4453 and 0.4493 on `block`, with all five fill classes tying inside
  their floors; (6) stage ten where both changes fire, HELD at 0.5850
  on `bcast`, 0.6128 on `bcastmid` and 0.7433 over stage nine on `window`, both
  per-view kills failing; (7) stage ten where neither fires, KILLED on `rev`
  at 1.0229 and 1.0240 past floors of 0.40% and 0.21%; (8) `lib-stage1` against
  the lean fill with one fill under both, HELD at 0.9975 and 0.9967 on `bcast`,
  1.0075 and 0.9710 on `bcastmid`, 0.2320 and 0.2328 on `runs` and 0.4225
  and 0.4259 on `block`; (9) the floor with the fill family's pair, HELD in all
  forty-four readings, the whole-set floor being that pair's for a second run
  at 0.51% against the carry-back figure's 0.26%. **Every kill fell on an item
  predicting a no-op** --- Run 28's own finding read again on a different
  variable, and the write-up does not claim the converse, five other no-op
  arguments having held.
- `ANSWERED` **Why does `bq-scan-packed-mulback` get worse
  under `-fspec-constr`, when the packing was hand-rolled to buy exactly what
  the flag hands its control for free?** Dumped in both regimes from Run 8's
  commit and answered there; the account, and the three-pair table showing
  it does not generalise to the other hand-packed arms, are [in Run 8's own
  file](runs/run8.md).
- `ANSWERED` **The element-type ordering still follows `Storable Double`.** All
  four element types re-run under the flag keep the ranking, the figures beside
  the -O1 ones in [that section](#one-element-type-and-what-the-probe-found).
  What the re-probe does not settle is whether the flag's reordering
  is an `Int`-arithmetic effect or an element-width one, the ordering it moved
  being among the roster's arms and not among the types.

- `ANSWERED` **What does code placement cost?** **A rebuild is worth up to 18%
  on a susceptible arm and 0.5% on the baseline** --- the largest effect
  this README has measured that is not a strategy --- **and for a loop this size
  placement costs 1.16 to 1.19** (2026-08-10, the pad probe). Susceptibility
  is a property of the arm, and what a rebuild moves beyond one loop's offset
  has no mechanism; the four binaries, the readings they explain and the graded
  penalty are in [the floor section][floor].
- `ANSWERED` **Is the term still unbiased?** **Answered 2026-08-13: it
  is the read**, not the two arms: a third `-nosum` arm with a flat fill,
  `mut-flat-gm-nosum`, read its in-situ term at a median of **0.9701**, below 1
  like the other two. The account is in [the sum-only section][correction];
  the sign has since reversed, which the gate 3 entry below puts on the arms.
- `STANDING` **Before crediting a margin to a strategy, check whether the two
  arms' hot loops are the same code and where each landed** ([the floor
  section][floor]). The reading needs two arms whose hot loop is identical
  *and* which differ nowhere else, so a shared loop is necessary
  and not sufficient. **The roster sweep for such pairs is done** (2026-08-13,
  a `-g3` twin over loop lengths 20 to 48): beyond the two groups the floor
  section reads, Main's code holds one more, `fbMutFlat` and `fbMutFlatGm`
  sharing a 24-byte loop, which is no placement pair even if `mut-flat` is ever
  timed, the two differing in the Granlund-Montgomery quotient; **no group
  at any swept length holds `bq-gen`**; and everywhere else the shared loop
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

- `ANSWERED` **Did aligning the loops do what the pad probe said it would,
  and at what cost in precision?** Run 10 registered five predictions before
  its aligned half ran; the gate of 2026-08-10 held the three testable ones, two
  corrections came with the full budget, and the account is [in Run 10's own
  file](runs/run10.md). Two of its findings outlive it and are the reason
  to open that file rather than take the outcome on trust: **a pair's two halves
  do not quite share a `sum-only` correction**, which matters to any later
  reading that assumes they do, and **a gate's five benches cannot price
  precision** --- Run 10's gate read its aligned half as the noisier
  and the full budget found the two indistinguishable, the widening having
  been the gate's own sample size.
- `ANSWERED` **What costs `mut-odo-vecdims-add-out` its 16%, now that layout
  cannot? Asked and answered the same day: it is a per-run cost, and the Core
  reading had it right all along.** It is a per-run cost, the `scanr (*)` stride
  table amortized over the run's elements: Run 10's aligned half puts
  the per-shape penalty at r **-0.64** against log `sInner` and **-0.01**
  against log `m`, which Run 9's straddling loop copy had hidden.
  The regression, `add-both`'s share of it and why the count-down form pays
  are in [the ceiling section][ceiling].
- `ANSWERED` **GHC HEAD compiles a `Ptr`-walking fill into an allocating one,
  and 9.12.4 does not --- GHC
  [#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778), worked around
  2026-09-06.** **What settled it** is the Core diff of the two builds:
  a bang-bound `plusPtr` result let-generalises to `forall b. Ptr b`, both
  compilers desugar it to a case on a type lambda, and 9.12.4 collapses
  that case where 9.14.1 and HEAD keep it, so STG allocates a `Ptr` per run
  in `-u1-ptr` and one more per two elements in `-u2-ptr`; a strict or unlifted
  field does it and a lazy lifted one does not, and HEAD's own default language
  hides it, MonoLocalBinds being in it. The record is horde-ad's
  `docs/ghc-issue-strict-polymorphic-ptr-boxed.md`. **The workaround
  is applied**, `:: Ptr Double` on every such binding in the three pointer arms,
  leaving 9.12.4's STG byte-identical and HEAD's free of `Ptr` allocation,
  and Run 27 read it holding on every axis it was registered on, as [the ceiling
  section][ceiling]'s twenty-third reading.

- `ANSWERED` **A loop's latch keeps its fall-through only where the block
  it exits to has no second predecessor --- GHC
  [#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799), filed
  2026-09-11.** A strided copy loop can end in `cmp`, `jge` and `jmp`
  or in `cmp` and `jl`, one instruction an element, and both compilers emit both
  shapes, `-fobject-determinism` selecting which: the exit is a join whose arms
  disagree about registers, the linear allocator splices a fixup block
  onto the arm it reaches second in `sccBlocks`' input order, the proc's blocks
  in ascending unique, and block layout then weights the latch's edge by 0.96875
  for leaving a conditional branch (`relevantWeight`, GHC
  [#18053](https://gitlab.haskell.org/ghc/ghc/-/work_items/18053)), so the latch
  loses a contest it led; GHC
  [#27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687) is the same
  mechanism with the fixup on the other arm. **So an edit that touches no fill
  can move the shape**, the uniques deciding it, and a run meeting
  a one-instruction step on an arm should read this entry before it reaches
  for a strategy.

- `ANSWERED` **The published `time` column moves a row across runs by far more
  than the arm moves, because its winsorizing BAND collapses under it ---
  measured 2026-09-15, and two modes now say so.** The column is a winsorized
  geomean, outliers capped at 3 MADs of the log, and the cap moves
  with the row's own spread: `lib-stage2-lean-u1` prints **0.029**
  on `run31-nospec` and **0.025** on `run32-nospec` where `--compare` reads
  the arm at **0.9839**, because the scaled MAD of its log-ratios fell
  from 0.34402 to 0.17956 and dragged the same four capped cells down with it;
  re-implementing the winsorization reproduces the published figure to three
  decimals on eight rows. **TAKEN 2026-09-15 in two modes**: `--winsor` prints
  each timed row's plain per-shape geomean beside the published one with how
  many cells the cap touched, and `--compare` flags a row whose two published
  figures divide to something its paired ratio does not. **A document check
  on cross-run sentences was REFUSED**, a matcher keyed on prose being unable
  to tell this run's figure from earlier runs' in the same paragraph ---
  the reason recorded beside `--check-doc`'s own agreement table. Cases
  `compare-does-not-flag-column-drift`
  and `winsor-does-not-say-what-the-cap-moved`, with a mutant apiece.
- `ANSWERED` **The `--library` within-pair agreement was quoted as a series
  across runs and did not reproduce under one tool; the series is now one
  tool's.** **TAKEN 2026-09-15, in one call** over every surviving pair: **14.0%
  and 66.2%** on Runs 24, 25 and 26 alike, **12.5% and 64.7%** on Run 27,
  **11.8% and 74.3%** on Run 28, all of 136 loops in common; **4.4% and 58.7%**
  of 916 on Run 31, whose halves share a compiler; and **11.0% and 65.4%**
  of 136 on Run 32. THAT is the series; the figures runs recorded for themselves
  were taken under more than one version of `tools/loop-offsets.py`,
  the denominator having moved from 141 to 136 at a time nothing here names,
  and Runs 29's and 30's binaries are not on disk.
- `ANSWERED` **A compiler is worth up to 29.5% on one arm of one class while
  the two compilers execute the same instructions to four decimals ---
  and it was not the compiler but the physical frame the page cache held one
  page of the basis's FILE in, read 2026-09-16.** A byte-identical copy
  of the basis file ran the cell at 2800M cycles against the original's 3260M,
  every extra cycle in the fill loop's own line, and evicting the original's
  cached pages brought it to 2785M: the term is the frame one 4 KiB page
  was drawn into, which no within-pair reading can see. [The placement
  section][floor] carries the readings and HEAD's instance of its own; post-run
  step 4a's `--half-movers` is the reading that separates the term. Run 34,
  launched from `hugebin/`, reads the arm at 1.0027 across the halves on `runs`
  with its counts level.
- `PARKED` **A rebuild of one recipe moved `bq-expand` 3 to 10% on ONE half
  with its instructions level, and killed a cross-figure registration
  that argued no commit reached it.** **PARKED 2026-09-26 by the owner.** Run
  41's basis ran the whole `bq-expand` family slower than Run 40's basis
  on the main set, `rev`, `bcastmid` and `window`, on level instructions,
  the widest cell in each population a shape of `sInner` 3, while no commit
  touched `bq-expand`'s code and the shim's change sat under both halves ([Run
  41's file](runs/run41.md)). **The copy test says it is the BUILD, and
  it is not an offset in line**: `perf record` on `cnn-L2-24x24-c32/bq-expand`
  puts 15% more cycles in the binary's own code on that build, libc's `memmove`
  level, and the three hottest blocks at the same offset in their cache line
  on both builds, moved by whole lines so that their distances from one another
  changed. Run 42's rebuild took the move back, so the term belonged to one
  build; and Run 43 found a PROCESS term on the same family, 1.5 to 1.7 points
  between two processes of one binary where the build moved it 3.4 to 9.5,
  so a copy test that reads BUILD against the previous run's half is reading
  across both terms at once ([Run 43's file](runs/run43.md)). **What would
  settle it**: a basis rebuilt with the shim at `fe6d133` on Run 41's source
  separates the shim's replanning from the source's, and a counter reading
  of that cell on the two builds --- front-end and branch events,
  `probe-stalls.sh` --- says what the cycles are spent on.
- `PARKED` **Four arms moved past 3% against Run 32 on ONE half each, with their
  counts level; the copy test, taken after the run, gives one of them
  to the evening's mounted file instance and cannot reach the other three.**
  **PARKED 2026-09-26 by the owner.** Run 34's `--half-movers run34 run32` named
  `mut-odo-vecdims-add-in-leaf-u1` on `scaled` on the basis half, both
  of the shipped leaf's A/A copies on `small` on the control
  and `lib-stage2-lean` on `rev` on the control, every count within 0.20
  of a point. The copy test, each mover's worst cell timed as raw cycles
  an iteration on four instances (`probe-r34-instance.sh`,
  `probe-r34-instance2.sh`): **on `scaled` it is the file instance**,
  the evening's copy at a median 1.075 of a second copy of the same bytes, all
  eight readings above all eight, with the frames of the pair in [the placement
  section][floor]; **on `rev` and `small` it reaches nothing**, those three
  movers being a few percent each where repeats of one instance part by up
  to eight, below what a differenced fixed-`-n` process resolves. **What would
  settle them** is the cell timed with criterion's own sampling on the evening's
  copy and a second one, interleaved.
- `OPEN` **The frame a copy draws is a durable property of the instance,
  and which physical bits it collides in is untested; the gate written to catch
  the slow draw ran at every launch until the mount was suspended
  and is suspended with it, and three routes past it are recorded here
  so that none is re-proposed blind.** Run 34's mounted basis,
  `hugebin/run34-exit`, untouched since its evening, read a median **1.10**
  of a fresh copy on `scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1` a day
  and a half after its copy test, instructions equal to within fourteen in 4.8
  million (`probe-r34-instance2-0918b.log`) --- so a slow draw stays slow
  for as long as the file stays cached, and one reading per launch gates it:
  `instance-gate.sh`, run list step 16a, times each half's launch instance
  against a fresh copy and swaps the copy in when the launch is the slow one,
  parking the slow copy as `.slow` rather than deleting it, because page
  shuffling is off on this box (`page_alloc.shuffle` reads N) and a freed block
  is the likeliest thing the next copy gets, a mechanism read
  from the allocator's design and not yet from a pagemap. A swap made on noise
  costs one copy and nothing else, which is the asymmetry the bar is set by.
  **Three routes past the gate, none taken.** (1) *The bit-range experiment*,
  half an hour on a quiet box with root for the pagemap reads: eight copies
  of one binary on the mount, a few hundred megabytes of unrelated allocation
  between copies so that the frames spread, each timed on the scaled cell
  and its 2 MiB frame read by `tools/probe-pageflags.py` while it runs. Slowness
  tracking bits 21 to 29 means placement can be controlled; only bits 30 and up
  separating the copies means DRAM channel or L3 slice selection, out of user
  space's reach, and the gate is the ceiling. Eight frames adjacent despite
  the spacers leave the high bits untested, and the run must say so rather
  than answer. (2) *1 GiB pages*, only if (1) names bits 21 to 29: not a mount,
  since nothing executes from hugetlbfs, ELF segments sitting at 4 KiB file
  offsets, so it needs a loader that remaps the text at startup, which
  libhugetlbfs's `hugectl --text` did and nothing maintained does now. (3)
  *A fresh copy per process* instead of per half, which turns a half-wide bias
  into per-process noise the A/A floors absorb, at the price of wider floors ---
  the fallback where the gate's minutes per launch are not to be had. **The draw
  was counted on both media over every binary on disk on 2026-09-20, Runs 31
  to 37, both halves of each** (probe-frames-0920.sh, `probe-instances-0920.sh`
  and `probe-draws-0920.sh`, their logs beside them): **the rate is about one
  draw in ten on both media, and the binary's era does not enter**, every slow
  draw 6 to 10 percent over its siblings, on both compilers, both regimes
  and every build alike. **Instances keep their frames**, all 56 hot pages of 28
  instances at the same physical address morning and evening, the mounted ones
  each in one 2 MiB folio at physical equal to virtual modulo 2 MiB ---
  so the mount held the L2 sets fixed and the rate stayed the disk's: the term
  lives in bits 21 and up. **Route (1)'s one candidate rule is REFUTED, recorded
  so it is not re-proposed**: the two slow mounted copies of that day
  were the only two of 28 whose physical bits 25 to 28 read 0 or 1,
  and a prediction registered on it (`probe-reuse-0920.sh`'s header) failed,
  the one fresh copy landing in that region reading level at 1.021 and the one
  copy past the bar sitting outside it --- so those were two draws
  of the one-in-ten kind handed out back to back. The counter sweep on a slow
  instance is in [the placement section][floor]: the store-to-load count did
  not move. While the mount stands, `half-bin.sh` hands the next run its mounted
  copy: a run that wants the disk launch the suspension ruled unmounts first.
- `ANSWERED` **A `predict:` span can ask a different question from the sentence
  that registers it, and since 2026-09-18 `--lint` prints, under an OPEN
  registration, every span as `--predictions` will compare it --- the mode,
  the two operands and their orientation, the key and the half ---
  for the author to read back against their own sentence at pre-run 12b.**
  A span reading `counts` under `--compare` reads one half over the other,
  not against the previous run, which is how Run 35's item (3) was unholdable
  the day it was written; `--lint` holds a registration's arms to the roster
  and its populations to the class list, and nothing else holds a span's
  vocabulary to the quantity its prose names. Case
  `registration-span-reads-are-printed`.
- `ANSWERED` **Nine consumers part by a quarter on ONE shape across a compiler
  pair with their instruction counts identical, and the term is the one [the
  placement section][floor]'s *The two stage arms' mechanism* paragraph already
  prices: HEAD's code order on `sumLazyRuns`'s per-run loop, one taken branch
  and two fetch blocks a run more.** On Run 35's `runs-3` nine `-sum` arms read
  **0.7563 to 0.7581** basis over control with counts at **1.0000** while
  `runs`'s class geomean is 1.0027, so a class table can hide a quarter on one
  shape. `perf stat` over `runs-3/libunord-stage13-sum` on the two Run 35
  binaries, differenced as `run-counts.sh` counts, reads per three-element run
  **6.23 to 6.28** cycles against **8.10 to 8.24**, the same 38.0 instructions,
  no branch miss on either, and **5.00 taken branches and 5.00 op-cache fetches
  against 6.00 and 7.00** --- the paragraph's counts exactly, so it is neither
  a placement the shim can move nor prediction.
- `ANSWERED` **Seven consumers on that loop part by a third on Run 40's `runs-3`
  INSIDE one process, where Runs 36 to 39 read none of it, and the term
  is placement: `943fecd`'s run loop, its head at residue 7, draws one of three
  op-cache modes on runs of three.** The seven arms that reach `sumLazyRuns` ---
  `liblist-stage4-sum` and `-5-sum`, `libunord-stage6-sum`, `-7-sum`, `-9-sum`,
  `-13-sum` and `-14-sum` --- retire the same 22.2M instructions an iteration
  there on both halves, the five `libunord` ones four taken branches and five
  op-cache fetches a run, and read 6.8, 7.8 or 10.2 cycles a run as a process
  or a stretch of its samples draws a mode, at 0.06, 0.25 or 0.6 op-cache misses
  a run with every data-side count level. So their order on that cell,
  and the cross-half figures step 4b quotes there, are draws and not the arms
  or the passes. Built on Run 40's basis recipe, `e2f68a7` reads one mode
  and `943fecd` all three; address randomisation and the core are ruled out,
  `setarch -R` and `taskset` leaving the spread as it was. `runs-3` is retired
  from timing since 2026-09-25 for it, `check` still covering it. The hazard's
  map by residue, run length and re-entry is [the placement section][floor]'s
  paragraph on `943fecd`'s loop.
- `PARKED` **On `flip-last-rows` the shipped leaf's own cell parted from BOTH
  its A/A copies by 22% in one process, and the copies agreed with each other.**
  **PARKED 2026-09-26 by the owner.** Run 34's `run34-exit-flip` read both
  copies 21 to 22% slower than `mut-odo-vecdims-add-in-leaf-u2` on that one
  shape, `--wild` finding no foreign CPU and the parting in the mutator time
  with the three arms' allocation alike, and Run 35 on the same recipe, shape
  and half read its worst A/A cell at 2.43%. So the 22% is a term of one process
  rather than of the leaf's code or its offset, and **what would settle
  it** is the cell timed on the original and one copy in one filtered process,
  interleaved, across several processes of one binary.
- `PARKED` **What a session's command costs the timed process it lands on,
  against a control.** **PARKED 2026-09-26 by the owner.** **The exposure is per
  command and not per minute**: a document read costs tenths of a second of CPU
  and a bench's samples are milliseconds, so anything concurrent trips
  the 0.25-of-a-core bar, and there is no quiet window inside the evening
  to move a reading to. Measured where they landed: document reads at 0.26
  to 0.35 of a core on the benches they overlapped (Run 33), a sub-second
  `./run-status.sh` at 0.81 and 0.65 on the two it overlapped (Run 35),
  and a gate reading at 0.82 (Run 32). **So every reading is taken at run list
  step 13a, before `run-evening.sh` is launched, `./run-status.sh $R` included**
  (ruled 2026-09-16), the done-condition reading the same before the evening
  as after it; and the residue an evening still meets, as Run 38's two foreign
  benches with no session command on the box, is the BOX's. **What would settle
  it** is the same command run beside a process rather than on it, which nobody
  has priced.
- `ANSWERED` **The readings carrier is retired, 2026-09-16: the reading it saved
  is a reading the write-up cannot avoid.** **IT RETIRED A CARRIER
  FOR THE PREVIOUS RUN'S SECTIONS AND NOT CARRIERS IN GENERAL.** Post-run step 5
  copies the previous run's file and the write-up edits the copy paragraph
  by paragraph, so the session reads those sections as the text it is replacing
  and a carrier read them a second time --- 111,877 tokens on Run 33
  for an 11.6 KB file --- and its file went unopened on two of the three runs
  that used one. The QUESTION each reading-list item carried now sits
  at the step that rewrites its section. **What would reopen it**: a write-up
  that does NOT edit the previous run's file in place, or a session dying
  between the launch and the write-up --- and that case wants the four
  `--section` calls written to a file by the session, not an agent.
- `PARKED` **Class property 1's `bq-expand` clause breaks on ONE main-set cell,
  `stretch-pow2stride`, where the two arms tie.** **PARKED 2026-09-26
  by the owner.** The clause is a sanity check, `mut-odo-vecdims` ahead
  of `bq-expand` on every shape. It holds on every shape of all ten classes
  on both halves, and on this one cell the runs from Run 36 on have read
  `mut-odo-vecdims` on both sides of 1, every reading behind `bq-expand` inside
  the floor of the half it was read on.
  `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints
  every run's reading on disk beside its half's floor. The entry stays OPEN
  on one question: whether any run reads `mut-odo-vecdims` BEHIND `bq-expand`
  on that cell by more than its own half's floor. Until one does, a break there
  is a tie and not a failure of the clause. **On the flagged-plain pair
  the plain half's readings sit within a point of the line on either side,
  and the flagged half's ahead of it every time.**
- `PARKED` **Which of the two `-O2` passes carries the regime's points,
  on a compiler this series still builds with.** **PARKED 2026-09-26
  by the owner.** Both together, `-fspec-constr` and `-fliberate-case` on one
  half and neither on the other, have been read from Run 36 on,
  and `./read-run.py --record regime` prints the readings; a run that builds
  that pair again appends its row. **They settle how many points the two passes
  are worth**: every reading from Run 37's build on puts `list` within a point
  of Run 31's whole-level 1.2974 over the main set, where Run 36's 1.3360 stood
  3.9 above it, so Run 36's was the outlier and its reading that the level's
  other passes hand `list` back is refuted across a rebuild and not only across
  a second draw of one build. The composition of the two single-pass runs,
  1.3325, overshoots. The only readings of either pass ALONE are Runs 29's
  and 30's, taken on ghc-9.12.4, on an older roster, and
  with the `-fspec-constr` half as that run's basis so that its published
  figures are the reciprocals of this orientation. So the SPLIT is not accounted
  for at all: nothing says whether SpecConstr carries it, as its allocation
  signature suggests, or whether LiberateCase carries part of it on this HEAD.
  **What settles it is one pair and one variable**: either flag alone against
  the unflagged half, built by the newest published basis's own recipe --- now
  `run45-gheadnospec`, `Main.hs` at `f5bf411` and the shim at `1a359bd`
  under the settled cost, on the stage1 patched on 2026-10-03, with the project
  file and the launch unmoved --- which reads with the box as the only term.
  Registered here rather than in a run's registration because it is a pair
  to ask for and not a prediction to hold.
- `PARKED` **A single wild cell can move a run's headline by points while every
  mechanical gate passes it.** **PARKED 2026-09-26 by the owner.** On Run 36's
  basis half `list` on `stretch-coprime-r7` read a net slope with a criterion CI
  of 10.07% and an R2 of 0.9395 where its own two A/A copies, in the same
  process, agreed with each other to 0.22 of a point and stood 28.4% below
  it --- the ORIGINAL the wild one --- and `read-all.sh`, `--check-doc`,
  `--lint` and the intrusion verdict all passed it, while it moved that run's
  registration item (1) from 1.3129 to 1.3360. **What would settle it is a gate
  rather than a reading**: a cell whose A/A copies agree far better
  than the cell does is a defect the reader can name mechanically --- the copies
  are the same code in the same process --- where the R2 and CI columns only say
  a cell measured loosely and say it of cells that are fine. Until
  then the worst-cell column is read by hand at post-run step 1, and a run whose
  headline rests on a cell that column flags quotes both figures.
- `ANSWERED` **The write-up's vocabulary and its Contents map had gaps a fresh
  reader fell into, found by the comprehension probes from Run 36 on --- closed
  2026-09-26.** The words and every bar with its unit are one glossary
  at the head of [Reading a run file](#reading-a-run-file), which each run
  file's opening paragraph links, and `family` keeps the sense of an arm
  with its A/A copies, the group being **the vecdims arms**, the column
  `best outside vecdims`, dated accounts keeping the old word. **What stays
  is the open list's own size**: a run file's pointers into this section land
  on a long list, and a probe that reads a tenth of this file can still meet
  a gap no probe has reached.
- `PARKED` **`-O2` changes what the preamble's spray leaves RESIDENT,
  and the two of its passes this series builds with do not.** **PARKED
  2026-09-26 by the owner.** Run 31's twenty-two processes carry one `keep`
  value and TWO `inuse` values --- 95420416 on every plain -O1 process
  and 74448896 on every `-O2` one, split exactly by half. The preamble sprays
  a fixed number of elements, so what differs is what survives the spray. Run
  36, its halves differing in `-fspec-constr -fliberate-case` alone, carries ONE
  `inuse` value, 95420416, while its allocation multiples move exactly as Run
  31's did, so **the resident level and the allocation multiples are NOT one
  fact**: those two passes take the whole of the second and none of the first,
  whatever in `-O2` moves the resident level being some other pass of it,
  and a compiler change at one level (Run 32) moves neither. Which pass, nothing
  here has asked.
- `PARKED` **Each -O2 pass changes what an arm ALLOCATES and not only how fast
  it runs, they disagree on WHICH arms and move `list`'s multiple in OPPOSITE
  directions, and nothing here says why an optimisation pass should move
  an allocation multiple at all.** **PARKED 2026-09-26 by the owner.**
  Over the main set's tiers, medians of the per-shape multiple and not
  to be divided: `-fspec-constr` alone takes `bq-expand` from 2.76x to 2.06x
  and `list` from 24.90x to 22.38x (Run 29); `-fliberate-case` alone leaves
  `bq-expand` at 2.76x and takes `list` UPWARD to 25.26x (Run 30); and the whole
  `-O2` level (Run 31) and the two passes together (Run 36) both take
  `bq-expand` from 2.78x to 2.11x and `list` from 25.20x to 23.45x,
  so the level's allocation signature is carried by those two passes,
  SpecConstr's fall beating LiberateCase's rise. A compiler change at one level
  (Run 32) moves no multiple. The allocation change and the time change arrive
  together on the same arms and on no others, the two families a pass speeds up,
  and the two passes break [the run file's property 3 LEVEL
  clause](runs/run45.md#the-properties-the-next-run-should-test) in every
  population. **Until it is answered, nothing here should describe an allocation
  multiple as a property of a strategy alone**: the levels are the regime's
  as much as the strategy's. **What would settle it** is Core for `bq-expand`
  or `list` under each regime, read for what SpecConstr's specialisation does
  to a boxed intermediate the unspecialised loop allocates per call; `list`
  is the reference every table here divides by, so the answer decides how much
  of the published column is a property of the regime rather than
  of the strategies.

- `PARKED` **Adding a pass grows `.text` by an exact multiple of a page and has
  mostly left FEWER self-loops, the loops measured gone and not grown
  (2026-09-13); a compiler change does neither.** **PARKED 2026-09-26
  by the owner.** `./read-run.py --record selfloops` prints each pair surveyed,
  and a run that surveys its pair appends its row. **The page multiple holds
  on every flag pair and on no compiler pair**, and nothing here explains why
  the difference should be a round page multiple. **The loop count parts
  from it**: on a flag pair the flagged half, the larger, carries fewer
  self-loops on some runs and more on others, the sign changing between runs
  whose compiler did not move, so what changes it is not the compiler; Run 32,
  the one compiler pair surveyed, carries more on its larger half. **Where there
  were fewer, they were removed and not grown past the survey's 64 B cutoff**:
  counting every self-loop of any length in `_Main_`-compiled code, the cutoff
  lifted to 96, 128, 192 and 256 B and then past any loop, `run29-nospec` holds
  327 against `run29-spec`'s 268 and `run30-nospec` 327 against
  `run30-libcase`'s 318, so neither gap closes at any cutoff. `--library`
  separates one pass from a level: `-fliberate-case` displaced no tracked
  library loop and the whole `-O2` level nearly all of them, the table's
  same-offset column reading 100.0% and 4.4%. What would close the entry
  is that raised-cutoff count on the pairs not yet asked, Run 31's
  and those from Run 36 on; until then a run that read placement off the survey
  count would be reading two events as one.

- `PARKED` **A saving in instructions reaches the clock at anything from NONE
  of it to MORE than all of it WITHIN ONE BINARY.** **PARKED 2026-09-26
  by the owner.** [The ceiling](#the-mutable-ceiling-taken)'s nineteenth reading
  put the conversion at about three quarters, measured across two builds of one
  recipe; within one binary the rate is a property of the arm and the pass
  together and of neither alone. One `-fspec-constr -fliberate-case` pair
  (Run 36) carries in one table the `bq-expand` trio converting three fifths
  of its saving, ten fill arms converting almost none of four to five percent,
  and the `list` trio, where the clock moves FURTHER than the counts; a real
  saving can even cost time, `mut-odo-vecdims-add-in-leaf-u2-last` over `-u2`
  turning 3.1% fewer instructions into a 1.4% LOSS on two runs. **Read per run
  length (2026-09-06, Run 26's artifacts), the rate is not one number either,
  and its profile is the pair's**: over `runs`, `-u1-ptr` over `-u1` turns
  a tenth to a quarter of its saving into time at run lengths 2 to 9 and about
  three quarters of it from 256 up, while `-u2-ptr` over `-u1-ptr` turns
  a quarter of the loop's instructions into no time at all from 256 up, either
  pointer fill moving some 42 GB/s there --- so a main-set geomean of the rate
  is the shape set's weighting of a profile, and carries between shape sets
  no better than between comparisons. **So a span derived from a count ratio
  should carry the rate it used and be read as a floor on the arm's direction
  rather than as a prediction of its size** --- Run 26's registration (8)
  derived three time spans through the three-quarters rate, its instruction
  ratios came back to a ten-thousandth, and all three time spans were killed
  for missing low. **What would settle the rest** is whether a cross-build A/B
  and a within-binary arm pair agree on one pair of arms of identical code,
  no run here having taken both.

- `ANSWERED` **Does list fusion pay in this harness, and what does the list
  interface cost a reduction against a fold? Probed 2026-09-09, before Run 28,
  and the harness rebuilt on the answer.** Only once the fold sits on the list
  expression itself, where it fuses: about a fifth of the time and a quarter
  of the allocation on every class where the list route fires. **DECIDED
  2026-09-09**: `lazyRuns` is in `build` form, each lazy stage's dispatch
  is a `Route` value read by shared readers, and the loop fold is one timed arm,
  `libunord-stage6-loop-sum`, for what the list interface costs a reduction.
  The account is the fusion premise of Run 28's registration, [in Run 28's
  file](runs/run28.md).
- `PARKED` **An argument that a change cannot reach a population, or that two
  changes compose, is the cheapest clause a registration can carry and the least
  reliable.** **PARKED 2026-09-26 by the owner.** Where the pair's variable
  reaches the population, such clauses fail often and past the population's own
  floor on both halves: four of Run 28's eight no-op predictions, among them two
  routes argued to be one code past a dispatch and parting on `window`,
  `small-patch-r5` and `rev`; three of Run 29's; Run 31's (5), stage nine's move
  and stage seven's tie-break argued to compose and refuted on three `window`
  views; and Run 41's (4), no commit reaching `bq-expand`, killed on level
  instructions. Where it does not reach --- Run 32's compiler pair at one level
  --- seven of its eight held and the eighth missed by nine hundredths
  of a point, so the failure rate tracks whether the variable reaches
  the population at all. **The converse does not follow**: on the same rosters
  every item predicting a real effect landed and several no-op arguments held.
  **`rev` is the population to note**: a dispatch's extra pass over the axes
  is visible there at a call of tens of microseconds, twice measured, on views
  with no zero stride whose route the argument called untouched. **What would
  settle it** is a next registration that states, for each no-op clause, which
  line of `Main.hs` makes the two routes identical --- the failures were argued
  from the shape of the code and not from the dispatch it compiles to ---
  and that reads, for every pair it registers, the probe JSONs already on disk:
  the fusion probe of 2026-09-09 had a killed pair behind on both populations
  that killed it, and nobody read those cells for the item.
- `ANSWERED` **The A/A floor and the carry-back figure part on some runs
  and close on others, so which of them a margin between two rows must clear
  is a ruling and not a measurement. RULED 2026-09-13: the whole-set floor
  is the bar and the carry-back figure the series.** A margin between two rows
  clears the whole-set floor, the widest an arm disagrees with its own duplicate
  by on that half over every pair the roster carries; the carry-back figure,
  over the pairs that carry back to Run 10, is the series and never the bar.
  The runs' figures are in [the floor section][floor].
- `ANSWERED` **What Run 28 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 28's own file](runs/run28.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the dispatch
  cost of the first canonicalization, HELD on `small` at 0.9073 and 0.9363; (2)
  the tie everywhere else, HELD on all eight populations and both halves; (3)
  allocation, KILLED, 16 of 77 views differing at the column's own precision
  and each on both halves; (4) the tie-break where it cannot fire, HELD, `rev`
  outside the floor on one half alone; (5) the tie-break where it fires, HELD
  on `window` at 0.7425 and 0.7237; (6) the longest chain, KILLED on both
  its conditions, `window` and `small-patch-r5`; (7) zero-stride axes outermost,
  KILLED on `rev` while every zero-stride prediction it made held; (8) the fold
  entry point, HELD, the hand-written loop behind the fused list at 1.7249
  and 1.7422; (9) the ports without the copy, WITHDRAWN with its arms before
  the run; (10) the ceiling's consumer, HELD on all five named populations; (11)
  the ordered list's consumers, KILLED by its second kill on `main`, `rev`
  and `small` while both its primary spans held; (12) base's `sum`
  over the list, HELD at 0.7176 and 0.7314 on `window`; (13) the two unrollings,
  HELD, `bcast-tall-Mx2` reading 1.2061 and 1.2058; (14) the lean fill ahead
  of the shipped leaf, HELD on its kills with both spans wrong in the arm's
  favour; (15) the shipped fill's own A/A pair, HELD in all forty-four readings;
  (16) the reversal read inside one process, HELD at 2.1892 and 2.1252.
- `ANSWERED` **What Run 27 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 27's own file](runs/run27.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the pointer
  fills on GHC HEAD, HELD in every clause on both halves, the three spans
  0.9713, 0.9357 and 0.9419 against 0.9751, 0.9239 and 0.9386 and both fills
  at 1.00x, where Run 26 read 2.6731 and 2.61x; (2) the same two arms in counts,
  HELD at 1.0054 and 1.0051; (3) the basis half against Run 26's, KILLED,
  and killed by a box that moved 3.66% under the run; (4) the rate
  an instruction saving reaches the clock, HELD, 27% to 46% on the three spans;
  (5) the class-floor asymmetry, HELD, the basis wider in 6 of the eleven; (6)
  the lazy unordered candidates, KILLED on `runs` and `block` though their
  crossover against the fill landed inside the predicted window; (7) the lean
  trick on the unordered list, KILLED on `small` and `compose`; (8) the lazy
  ordered candidates, KILLED on all three of its kill conditions; (9)
  the reducing consumers, HELD, `libunord-stage1-sum` leading its own fill
  in all ten classes on both halves; (10) the baseline between the halves,
  KILLED at 0.33% where 1.1% was registered, which reopens the subtraction; (11)
  the dispatch pair, WITHDRAWN with the arm before the run; (12) the class-level
  margin on the four reversed classes, HELD, all four inside 0.95 to 1.01; (13)
  the hoisted bound, KILLED at 1.0138 and 1.0157 against a 1.005 kill, its 3.1%
  instruction saving costing 1.4% of the time; (14) the unroll
  under the library's dispatch, HELD at 1.0516 and 1.0414.

- `ANSWERED` **What Run 26 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 26's own file](runs/run26.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: the dispatch pair
  KILLED on `small` alone, the roster change SPLIT with its arm-level clause
  held and its per-shape kill fired, `libunord-stage3` HELD, Run 24's unread
  clause HELD in all eleven populations, Run 25's orderings clause HELD,
  the class clauses `flip` and `block` KILLED again and `small` HELD
  at its first reading, the two window views HELD, and the pointer fills' three
  spans KILLED with two of their three directions established and the third
  parting between the two statistics the run file publishes --- and not one
  clause of the eight was unreadable, where Runs 24 and 25 lost five between
  them.
- `ANSWERED` **What Run 25 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 25's own file](runs/run25.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the box, HELD
  --- -0.08% at the gate and +0.32% and -0.77% on the two main-set processes
  against Run 24's kept fingerprint, all inside 3%; (2) the anchors, HELD,
  `cnn-L2-24x24-c32` -1.59% of Run 24's own net for it; (3) the pair, KILLED ---
  `list` moved 1.10% between the halves where 0.7% was allowed, so the two
  columns are ordered and not differenced, and its second clause was unreadable,
  all three orderings it names turning on an arm parked that day --- two against
  `lib-stage2` and one stated of `lib-stage2-short-lean`; (4) the additions
  of 2026-09-03, task 10's four: `flip` KILLED by every fill on both halves,
  a reversed run costing the regime-3 fill about twice its forward twin
  at the same length, `block` and `compose` SPLIT and `small` unreadable; (5)
  the retirement, HELD, nothing published moving for it and Run 24's basis
  column giving this one's figure back on fourteen of the eighteen shared arms
  once the shape set is pinned, a printed digit away on the other four; (6)
  the prune, HELD, the three crossed pairs inside Run 24's floor on both halves
  with their spans shortened; and (7) the unroll, HELD on both halves ---
  `mut-odo-vecdims-add-in-leaf-u1` between `-add-in-leaf` and `-u2`,
  so the shipped fill's margin is the unrolling's and the merged bound is worth
  six and a half percent rather than the wash a shimless probe read. **Two
  of the seven lost five clauses between them to arms parked the day after they
  were registered**, which is the entry above this one, fired again.
- `ANSWERED` **The baseline moved 1.10% between two halves that differ only
  in the compiler, and the counted work says it is not instructions.** **TAKEN
  2026-09-05: the term is `list`'s own**, cycles per instruction in its code
  under each compiler. It does not scale with the roster, `list` reading 1.0104
  cross-half as a roster of one against 1.0107 at twenty-four; it is
  not a process term, every other arm's time-over-counts residual running 0.978
  to 1.008 where `list`'s is 1.0145, so the plain `--compare` stands
  for this pair and `--compare --bridge` would move it onto arms that do
  not carry it; and `perf stat` on `list` alone, differenced, reads instructions
  at 0.9966 and cycles at 1.0057 with GC at 0.0% and neither cache nor branch
  misses moving with it. Run 26 reproduced it at a residual of 1.0149; a third
  compiler is what would say whose the term is.
- `ANSWERED` **What Run 24 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 24's own file](runs/run24.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the short
  bodies, SPLIT --- ahead past both floors on every k3 and k5 shape and killed
  by its own count clause on `stretch-coprime-r7`; (2) the lean dispatch, HELD,
  and taken 2026-09-05 ([the stride
  classes](#the-stride-classes-and-what-they-cover)); (3) the composite, HELD
  on every population of both halves; (4) the straddlers, HELD, and named rather
  than counted for the first time; (5) HEAD, HELD on its orderings and
  not on one of its figures, with one clause unreadable because the arm
  it turned on had been parked; and (6) the threshold, HELD, the re-cut dispatch
  now leading the `runs` class.
- `PARKED` **A registration can name an arm the roster has parked, and lose
  the clause unread.** `--lint` holds an OPEN registration's backticked arm
  names to the timed roster, and reads a deferral's TARGET paragraph as it reads
  the registration's own, refusing by name ---
  `registration defers to task N, which names arms the roster does not time`.
  **A clause naming another registration instead of an arm has no cheap
  predicate**, and stays pre-run step 12b's, a reading: a registration
  that names another registration inherits its arms. **PARKED 2026-09-06,
  and the prevention is in the pre-run list rather than in a tool**: step 12b
  says do not defer, write the clause out with its arms named, which Run 26 did
  for seven inherited clauses and lost none where Runs 24 and 25 lost six
  between them. A `--lint` that followed a clause's named registration
  to the roster would buy the same protection for a tool change where
  a paragraph buys it for free, so it is not worth doing and is not
  to be re-proposed. **What would reopen it** is a run that loses a clause
  DESPITE restating, which would mean the failure is not the deferral after all.
- `ANSWERED` **`--replace` took a following heading with the paragraph
  it replaced, where no blank line separated them --- fixed 2026-09-03.** **What
  settled it**: `--replace` now refuses when the paragraph it matched carries
  a heading no blank line separates from it, naming that heading; case
  `replace-takes-an-abutting-heading`. Run 24's write-up had lost `## Results`
  that way, and the rule the run chapter already states stands beside the fix:
  read the `out` lines and not only the `in` ones.
- `ANSWERED` **`--machine` run after `install-tables.sh` compares a run
  with its own freshly installed fingerprint and reads +0.00%.** From post-run
  step 5b the box check is the run against itself. **DONE 2026-09-05**:
  `--machine` refuses when the JSON's run is the one the run file's fingerprint
  came from and tells the caller to give the PREVIOUS run's file (`--run-doc`).
  **Taking the reading before 5b instead was REFUSED**: it puts the guard
  in an ordering the post-run list has to hold, and nothing would report a later
  reordering.
- `ANSWERED` **What Run 23 was built to answer, registered before it ran ---
  and what it answered.** The six registrations, their kill conditions and their
  verdicts are [in Run 23's own file](runs/run23.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) the nine
  padded arms' win reproduced within 0.7 of a point, HELD, and the counted work
  says it is the pads, 4.0% of their instructions over the 23 readable shapes;
  (2) the flatness control flat at count ratios of 1, HELD; (3) the classes
  SPLIT and the `runs` monotone prediction KILLED, the margin ordering
  with nothing; (4) `build`/`mut-odo` a tie on the basis and 0.9449
  on the dead-spot half at counts of 1, HELD; (5) the placement-exposed workers'
  counts equal, HELD on that and not on the size, `gen-unsafe` 4.9 points
  from the probe's figure; (6) no Run 22 verdict re-decided by the switch,
  and KILLED by its own terms nonetheless, the repetition of Run 22's binary
  unseating `lib-stage2-u4`'s kill.
- `ANSWERED` **What Run 22 was built to answer, registered before it ran ---
  and what it answered.** The five registrations, their kill conditions
  and their verdicts are [in Run 22's own file](runs/run22.md), where a run's
  registrations have lived since 2026-08-29; a registration is that run's record
  and reads against that run's tables. **Two held, one split and two
  were killed**, and unlike Run 21's one-sided set they share a subject rather
  than a mistake: `fillStage2` got fast enough between the two runs
  that a threshold, an unrolling and a family ordering all cut around its old
  cost are each mis-cut. The headline is that Run 21's 2.43-to-4.54 regime-3
  regression is gone --- 0.74 to 1.03 on the same six populations.

- `ANSWERED` **`dispRun` was demonstrably mis-cut, and its right value
  is a measurement rather than a guess --- taken 2026-09-02 and re-cut to 2048,
  to 32768 on 2026-10-04 and to 8192 on 2026-10-05.** Run 22 put the crossover
  between `runs-1024` and `runs-65536` on both compilers, `lib-stage2-disp`
  6.65% behind stage two at `runs-1024` on the basis and 4.22% on the control,
  and Run 23 read 5.75% and 6.24% on both halves of one compiler, so the failure
  is neither a compiler's nor a pad's. **The in-cache probe**, one process
  over `runs` on the dead-spot binary with an arm per candidate threshold, put
  the crossover between `runs-1024` and `runs-4096` and the 2048 arm nowhere
  behind the better route. **The past-cache probe**, probe-cache-build.sh
  and probe-cache-run.sh, removed 2026-10-06, timing two regime-2 views of 8
  million elements at runs of 96 and 4096, KILLED its registration by a small
  inversion: `list` at 14.7 ns an element, memory-bound at every size; at 96
  `lib-stage2` reads 0.5548 of `lib-stage1`, and at 4096 0.9802, the fill two
  points ahead where in cache the slice route leads by five, `lib-stage2-disp`
  reading 1.0227 of the fill --- past the cells' fit widths, 0.14 to 0.54%,
  and inside the `runs` class's floors, 2.79% to 3.15% on Runs 25 to 27.
  So `dispRun` is a function of the working set by the letter and not in a way
  that costs, and the cut stood; the dispatch and its probe arms were retired
  for their own reasons on 2026-09-07 ([dead ideas][dead]). **The third probe,
  2026-10-04, re-cut it to 32768 over the branch's fill of 2026-10-04**: one
  process over `runs` on Run 44's basis recipe, `lib-stage2-disp` rebuilt
  over `lib-stage2-lean` and run at a threshold of 1 so that it sliced every run
  (`probe-p45disp1-runs.json`), read the slice route over the fill, net,
  at 1.1374 at `runs-1024`, 1.1095 on `runs-r3-48x30`'s runs of 1440, 1.0078
  at `runs-4096`, 1.0026 at `runs-16384` and 0.9838 at `runs-65536`, the sign
  turning between the last two. Every figure from `runs-4096` up is inside
  that process's A/A spread, the shipped leaf's twin parting by 1.24% a shape
  and 3.47% at worst, so past the floor the slice route now leads on no view
  of the class, where the in-cache probe had it five points ahead, and
  at that cut it took `runs-65536` alone. **The fourth probe, 2026-10-05, priced
  glibc's `rep movsb` inside the slice route**, which `x86_rep_movsb_threshold`
  puts at 2112 bytes on glibc 2.39 here: the third probe's binary
  at its threshold of 1, over the seven `runs` views from `runs-256` up
  and the arms `lib-stage1`, `lib-stage2-disp`, `lib-stage2-lean` and both
  `sum-only` halves, in four processes ordered ABBA, both B processes launched
  under `GLIBC_TUNABLES=glibc.cpu.x86_rep_movsb_threshold=0x10000000` so
  that no run copied with it, and no bench at 0.25 of a foreign core
  (`probe-movsb-A1-runs.json` and its three siblings). **It is some of the slice
  route's deficit and not most of it.** A over B, net, both slice routes read
  1.073 to 1.075 at `runs-512`'s runs of 4 KB and 1.031 to 1.064
  at `runs-1024`'s 8 KB in both pairs, where the fill, which calls no `memcpy`
  on these views, reads 0.977 to 1.010 on those two, and on `runs-256`, whose
  2 KB runs sit under the threshold, every arm reads 0.992 to 1.020; yet in both
  B processes the slice route still trails the fill by 17 to 26% at `runs-512`
  and 10 to 13% at `runs-1024`. From `runs-4096` up the first pair reads every
  arm at 0.979 to 1.009, and the second reads A2's own process, A2 parting
  from A1 there by 5.7 to 6.4 points at worst on each arm, the fill included,
  so neither cut rests on glibc's choice of copy. **The re-reading of 2026-10-05
  re-cut it to 8192.** The fourth probe's processes, read slice route over fill
  rather than A over B, put `lib-stage2-disp` at its threshold of 1 at 0.9983
  to 1.0338 of `lib-stage2-lean`, net, at `runs-4096`, and at `runs-16384`
  at 0.9693, 0.9719 and 0.9835 in A1, B1 and B2 and at 0.9291 in A2, whose lean
  cell reads a CI of 1.84%; and `lib-stage1`, which slices every run, reads
  1.0115 to 1.0302 of `lib-stage2-lean` at `runs-4096` and 0.9709 to 0.9876
  at `runs-16384` on both halves of every run from Run 40 to Run 45. The third
  probe's 1.0026 at `runs-16384` sat inside the spread of its own fill copies
  on that cell, 0.9394 to 1.0068. So the slice route is level with the fill
  or behind it at `runs-4096` and ahead of it from `runs-16384` up, 8192
  represents that bracket, and at it the slice route takes `runs-16384`
  and `runs-65536`. **This entry is the only copy of the four probes' accounts
  and is never trimmed to a question.** What the 2048 cut's probes did
  NOT measure is in [the non-urgent TODO list][todo].

- `PARKED` **The 0.7% bar that decides whether a pair's two columns may
  be subtracted is used everywhere, and where 0.7 came from is written
  nowhere.** **PARKED 2026-09-26 by the owner.** It decides the readability
  of a pair's whole second column, in the form *past the 0.7% that lets two
  columns be differenced*. What it bounds is in the glossary at the head
  of [Reading a run file](#reading-a-run-file): how far `list`, the denominator,
  may move between two files before their columns stop sharing one. The evidence
  is in the paragraph beside the floor's, which measures the bar against
  the pairs it is applied to and finds it near the MEDIAN of the thing it bounds
  rather than above it. **What stays open is the half a measurement cannot
  reach**: where 0.7 came from, and why the main set and the classes share one
  figure, which wants whoever set it.
- `ANSWERED` **A hand-edited table goes stale unchecked --- ANSWERED 2026-09-26:
  the rows are installed, and a paragraph that begins mid-sentence fails
  `--check-doc`.** `read-run.py --hand-tables`, run by `install-tables.sh`
  at post-run step 5b, recomputes the run file's two hand tables ---
  the two-column geomeans and the Provenance anchors --- from the two main JSONs
  and, without `--in-place`, names every row that disagrees; a stale row had
  corrupted a published figure, `--machine` resolving its fingerprint off it.
  A paragraph that lost its opening words passes a check that asks only
  that it end a sentence, so `--check-doc` holds a prose paragraph to beginning
  on anything but a lower-case letter, with its case and a mutant.

- `ANSWERED` **A run's sequence can be split across two windows and still be one
  run.** Run 22's was stopped by hand at the `scaled`/`runs` boundary when
  the machine was wanted back, and the two `runs` processes ran eight hours
  later. What certifies it is the plateau gate rather than the clock: all twenty
  processes assert their preamble victim inside a 2.60% spread against a 5%
  band, the two late ones among them. A hand-stop three seconds into a process
  leaves no JSON at all, so nothing had to be discarded. The account is in [Run
  22's Provenance](runs/run22.md).

- `PARKED` **Routing the one-level fill through the odometer reached plain -O1's
  emission and not the two passes'.** **PARKED 2026-09-25 by the owner,
  with the arm retired to `Only`: the fill is not worth keeping even
  at that speedup, so the `-g3` reading that would settle it prices nothing.**
  `3c02e36` took `fillStage2OneLevel`'s runs loop through the recursive
  odometer, to remove the stack-slot spill [the dead-ideas entry on skipping
  the level table](#dead-ideas) describes, and on Run 40 that sped the plain -O1
  half by up to 18% on `runs` while the flagged half's counts did not move.
- `PARKED` **The unordered entry point buys a level BELOW the result vector,
  which no arm here had.** **PARKED 2026-09-26 by the owner.** libunord-stage1
  and libunord-stage2, checked and not timed since 2026-09-09 with every arm
  that concatenates a list, their consumers carrying the reading, read 0.00x
  allocation where every mutable fill reads 1.00x: where the one-block test
  fires they return a slice of the source and allocate nothing. The allocation
  ladder has a floor under its floor. What is not known is what that is worth
  to a consumer who cannot accept a view, and whether the test's cost is visible
  where it does NOT fire --- Run 22 reads both arms inside the floor on the six
  classes where it does not, which bounds it but does not price it. **Run 27
  answers the consumer half and the answer is large.** Its four `-sum` arms
  are `sumT` over each stage's list, one slice at a time and no concatenation,
  which is the entry point as a consumer actually uses it; `libunord-stage1-sum`
  leads `libunord-stage1` past the floor in **all ten classes on both halves**,
  from **0.0854** on HEAD's `runs` to 0.7871 on HEAD's `small`, so the copy
  a Fill arm over a list pays is between a fifth and nine tenths of the call.
  That is registration (9), which held --- read against Fill arms
  that concatenated a singleton, so on the classes where the list is one fill
  part of that lead was the harness's own copy, which Run 28's item (9) takes
  out. **What stays open is the other half**: a consumer that cannot accept
  a view still has to materialise, and no arm here times that path against
  the fill it would replace.

- `ANSWERED` **What Run 21 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 21's own file](runs/run21.md), where they were moved
  on 2026-08-29; a registration is that run's record and reads against
  that run's tables.
- `PARKED` **What is the 3% that survives alignment on `build`/`mut-odo`?**
  **PARKED 2026-09-04 with the prune: both arms are `Only`, so the residue
  is read on no run until they are re-timed.** With both copies of one worker
  at offset 0 the pair read 0.9431 to 0.9822 over the six full-budget halves
  of Runs 10 to 12, tying on some and not on others, the classes swapping sides
  between runs --- so it fluctuates run to run on arms whose code, layout
  and slot are all pinned, and an experiment that prices it once has priced one
  draw. **What is excluded**: everything the runtime reports, an arm and its own
  A/A duplicate on `reshape1-500k` differing by 8.2% of mutator time
  with allocation equal to 0.01%, a flat heap and no major collection (Run 16);
  a monotone effect of position in the process, the two duplicates bracketing
  the base in execution order and agreeing with each other to 0.09%; sharing
  an offset as what makes the pair tie, the named map putting both copies
  at offset 0 in both halves of Run 12, which read 0.9822 and 0.9431;
  and the Core route, below. **What is left is procedure placement and what
  the pads reach**: Run 12's halves differ in `-fproc-alignment=64` alone,
  the four points between them pricing the package of procedure starts
  and the offsets they produce together; and on Run 23 the pair reads 0.9998
  on the max-skip basis and 0.9449 on the same code with every pad placed after
  an unconditional `jmp`, both tracked loops still at offset 0 ([Run 23's
  file](runs/run23.md)). **What would settle it**: `perf record` over the arm
  and its duplicates on the run's own basis binary, which maps samples
  to addresses without DWARF names --- if the base executes a copy
  at a different offset from the twins', the straddle model predicts the sign
  and roughly the size, and if all three share one copy, placement is excluded
  too. The offsets move with every relink, so take them from the binary being
  sampled.

  **The Core route is closed and is not to be re-proposed.** The obvious
  candidate is the call path --- `build` being `mut-odo` driven through
  `vBuildVS` --- and it has been dumped three times, from Run 6's source, Run
  7's, and Run 8's commit under this regime: there is no call path to find,
  `vBuildVS` surviving as no top-level binding in any of them, the two workers
  byte-identical once numbering is normalised, and the sources differing only
  by the `Strides` newtype's zero-cost cast ([the mutable ceiling][ceiling]
  keeps the dumps' verdict). A fourth dump would reproduce that and nothing
  else.

- `ANSWERED` **Which arm owns a loop copy: answered, and the answer is
  that a binary can carry its own names**, a `-g3` build's per-block symbols
  letting `tools/loop-offsets.py` name a copy by its binding and source line.
  **The twin's names are a per-GROUP property and not a per-binary one**: count
  a body's copies in twin and timed binary before trusting them, which
  the vecdims group passes and the `build`/`mut-odo` group fails. The named
  readings, the refuted padding prediction and the method are in [the floor
  section][floor].
- `ANSWERED` **The shim was blind under `-g`, which is why this wanted a fix
  and not merely a build**: not one head of a `-g3` assembly was given
  a directive. **The ruling is the condition on the fix and not the fix** ---
  the look-through fires only where the assembly carries `.loc`, every other
  build keeping the literal guard byte for byte, since applied everywhere
  it would re-base every figure this README has published for a reason
  no strategy changed. The mechanism, the counts, the end-to-end control
  and what the 27 extra heads cost in pads are in [the floor section][floor].
- `ANSWERED` **`-g3` is a different program, and what differs is register
  allocation.** Measured on the assembly GHC hands the assembler, every debug
  artifact stripped: 60056 instructions against the plain build's 59991,
  register assignments and block order differing throughout. What this README
  times does not differ --- all three 28-byte groups have the same body in both
  builds --- and the two copies the `-g3` build lacks are the dead ones,
  confirming by a second route `tools/loop-offsets.py`'s
  `[dead, mut-odo, dead, build]` reading, the naming's non-vacuity control;
  the groups are in [the floor section][floor].
- `ANSWERED` **So building everything with `-g3` is refuted, and a `-g3` build
  is a twin to read rather than a binary to time**: its own criterion
  was that the arms agree within the run's floor, and a pair differing in `-g3`
  alone gates at `build` 0.9391 to 0.9517 plain over `-g3`, four to six times
  the floor and one direction. **And no weaker level is a way round it**, `-g1`
  changing the emitted code exactly as `-g3` does (GHC
  [#27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687)) ---
  nor is one a way to a name, which is the other thing a twin is for: `-g1`
  and `-g2` twins of Run 28's HEAD half, built beside its `-g3` one
  on 2026-09-11, read the same census, name the same single straddler of seven
  and refuse the same two. The gate's figures and the copy census that bounds
  the naming are in [the floor section][floor].
- `PARKED` **A recurring transient that lands on the `bq-expand` family, worth
  35 to 74%, and which no published column would show.** **PARKED 2026-09-26
  by the owner.** Not one cell: five sightings by Run 19, moving each time,
  the largest Run 17's 74.48%; the earliest, and the roster fix that removed
  the slot and not the susceptibility, are in [the floor section][floor].
  **It is mutator time with the work identical**: on a kept instance, Run 11's
  `lenet-L1-28-c1-k5/bq-expand`, the wild cell runs time x1.279 and mutator
  x1.281 against the arm's other processes, with GC count, allocation
  (x1.000002) and peak heap equal and `list` normal in that same process, flat
  from first sample to last, so the state is entered before the bench begins;
  the published 35 to 44% is the net figure, the correction amplifying a raw
  ratio of 1.279. Its largest cell is a LEVEL and not an event, every quantity
  the runtime reports flat across a cell 68% slower, `--steps` reporting
  no step. **And it is the tail of something common**: of 4029 cells over eight
  kept main sets, 3% carry a step past 2% at `t` above 40, the largest 12
  to 15%, on the arms this README already suspects --- `build`, `offtab`,
  `mut-odo`, `gen-quotrem` --- the step size tracking log `l` at -0.70 where
  the between-process spread tracks `sInner` and rank, so the two instruments
  measure different things and neither subsumes the other; so the wild cell
  is the extreme of a distribution and not a lottery among cells, which is why
  the `scaled` slot can stand in for it. Smaller cells of the same signature
  recur in the family, the parting in the mutator time with allocation equal
  and no foreign CPU, as on Runs 43 to 45.

  **Three things make this a threat to a published claim rather
  than a curiosity.** It is *the expansion family* that is susceptible,
  established rather than guessed: Run 9's filtered probes put
  `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback` each
  35--40% above their published cells on that shape while
  `bq-scan-rem-gm-mulback` and `mut-odo-vecdims` did not move at all.
  That family contains **`bq-expand`**, `vFillStrided`'s class default.
  And **the table cannot show it**: the winsorized estimator caps the cell,
  so the row read 0.103 against 0.102 and nothing looked wrong --- the only
  reason it was seen is that `bq-expand` carries two A/A twins, which disagreed
  with it by 25%. An arm without twins would show nothing at all, which is most
  of the roster.

  **The evidence against an intrusion is [in the floor section][floor]**: clean
  twins, time-neighbours within 1.2%, CI% 0.06 over 125 samples, `list`
  on that shape unmoved.

  **The samples say the cell is a shift and not a defect, and refute
  the cold-pool account inherited from Runs 8 and 9** (2026-08-12, over the run
  artifacts, a refit of `reportMeasured` reproducing criterion's own slope
  to 2e-16 first). Its residual dispersion matches its own twins' in the same
  process, so it is not the noisy one; against them it runs 1.28 times
  the cycles at a clock reading 3.8000 GHz to four digits, allocation one byte
  apart and GC time no greater --- the same instructions over the same bytes,
  stalling 28% more, where a cold block pool predicts more or dearer collection.

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
  2. **That gate covers only the arms that carry twins**: a wild cell
     on an untwinned arm would still be capped by the estimator, would move
     its row by a thousandth, and nothing here would ever say so, which
     is the honest extent of the defence --- and the anomalies on record all
     landed on twinned arms, so their apparent distribution is a fact about
     the controls before it is one about the machine.
  3. **Winsorizing is a defence and not only an estimator choice.** It is what
     held `bq-expand`'s row to 0.103 with a 35% cell inside it. [The `time`
     column](runs/run45.md#results) argues for it on estimator grounds ---
     bounded influence rather than deleted evidence --- and this is the second
     and larger reason to keep it.
  4. **It gives the per-shape caution its mechanism.** [The per-shape
     table][pershape] says to trust the first digit only; a scheduling lottery
     moving one cell by a third is why, where a geomean over a whole main set
     cannot move like that.

  **And a fourth instrument died on contact, which is worth a sentence because
  it is the obvious one.** If the mechanism is allocation history, pinning
  criterion's iteration count should pin the history and make cells reproduce;
  but `-n/--iters` is *Run benchmarks, don't analyse*, and a run under it writes
  no JSON at all --- measured, not read off the help text. There is no other way
  to fix the schedule from the command line, so the mechanism cannot be tested
  by pinning it, and it is recorded here dead rather than left
  to be re-proposed. What `-n` *is* for is the `perf` method below.

  **The block-pool issue this project filed, GHC
  [#27601](https://gitlab.haskell.org/ghc/ghc/-/work_items/27601),
  is the nearest precedent, and its method is the one to reach for next.**
  **The bug itself is probably not this**: its symptom is a pool that doubles
  and stays doubled, and `max_mem_in_use` across the main-set processes of Runs
  10 and 11 sits level, the *wild* process the smallest of them; nor does any
  main-set shape allocate in the worst-case band just above the 3276-byte
  large-object limit. **But its statistical signature is this situation's
  verbatim**: a bias rather than noise, regression fits staying tight around
  a value wrong by a fifth, more samples shrinking the interval *around
  the wrong value*, and an effect that in rare runs does not reproduce and whose
  magnitude differs randomly from run to run.

  **So the instrument that report used is the one this question wants**:
  `perf stat` over runs with a fixed iteration count, `-n`, read per iteration
  --- task-clock, instructions, dTLB-load-misses, cache-misses, page faults,
  clock --- which identified last-level cache misses there by finding everything
  else equal. Here the clock is fixed, allocation is identical to the byte
  and GC is flat, so **the missing row is the cache misses, and only `perf` can
  supply it**. `+RTS -H2G` is the control the same report validates: a pool
  taken in one contiguous piece removed the cost there, so a wild cell surviving
  `-H2G` is not pool structure.

  **`perf` needs `kernel.perf_event_paranoid` at 1 or lower before it counts
  anything** --- above that it reports `cpu-cycles:u <not supported>`, Ubuntu's
  level 4 being its own and above the upstream maximum of 3 --- and lowering
  it is a `sysctl -w` in a plain terminal, not something a session can do.
  **It is set persistently here since 2026-08-26**, so a sweep meets it ready
  and no checklist asks anyone to read it first; what `run-counts.sh` still
  probes is whether perf COUNTS, a capability a container or a missing binary
  can take away as readily as a setting.

  **Filtered, the cell does not reproduce, as expected** (2026-08-12, `-n 40000`
  differenced against `-n 20000` on `run12-maxskip`, which removes the process's
  fixed cost exactly): `lenet-L1-28-c1-k5/bq-expand` and its adjacent twin agree
  inside a third of a percent on time, instructions and cache misses, a filtered
  process having no allocation history for the effect to arise from. It buys
  **the instructions agreeing to 5e-5**, the first instruction-level proof
  that an A/A pair is the same work; a per-call counter baseline for a wild
  cell; and **criterion's slope confirmed by an instrument sharing no code
  with it**, 1.2% apart --- in seconds and on no quiet machine, counter ratios
  between two arms not moving because something else is running.

  **What would settle the mechanism is logging what it names, per sample**:
  the RTS's allocated-bytes total and the payload addresses. That is a `Main.hs`
  edit and belongs **between pairs**, since it moves every loop offset and would
  invalidate the md5s a pair's note records. The `scaled` A/A slot shares
  this signature and turns up on demand, so the mechanism can be instrumented
  there, the state entered mid-bench there and before the bench here, which
  is why **the logging is per sample and not per bench**; allocation being
  identical to the byte in both instances, the cost is per access rather
  than per allocation.
- `PARKED` **`mut-odo`'s wide interval on `micro-aligned` is, at sample level,
  the `build`/`mut-odo` pair scattering together --- a measurement without
  a mechanism.** The `CI%` column reads it as one arm's, which is an artefact
  of the interval, sampling error about a fitted line and not stability: taking
  each cell's residual about its own line, per iteration, as a fraction
  of that cell's slope, `mut-odo` scatters **21.9%** on the aligned half
  and `build` **32.7%**, against `mut-odo-vecdims`'s 3.1% and `list`'s 3.2%,
  `build` the worse where its *interval* is the narrower, and both roughly halve
  on the max-skip half (2026-08-12, Run 11's two main sets) --- the same pair,
  on the same two binaries, as [the 3% that survives alignment][open], and kept
  because the two instruments will disagree again and the scatter is the one
  to believe. **Three accounts are closed at sample level**, the refit
  reproducing criterion's slope to 1e-15 first: the residual correlates with GC
  count and GC wall time at +-0.00, so it is not the block pool; with sample
  index at +-0.03, so it is not drift the slope missed; and allocation per
  iteration is constant. The two arms share one worker at offset 0 and drift
  most across a repetition too, so placement is neither's account; **what would
  separate a dispersion belonging to the worker from one belonging to the slot**
  is a run with the two arms' roster positions exchanged, which asks
  for an aligned build, a form this README has moved past ([the standing
  rulings' closing one](#standing-rulings-from-past-runs)).

- `PARKED` **A second instrument says different arms are unstable, and the two
  disagree --- which is the finding rather than something to average.** **PARKED
  2026-09-26 by the owner.** Besides `CI%`, sampling error *within* one
  benchmark, a pair's two halves price disagreement *between* processes,
  as the standard deviation of each arm's per-shape log ratios. Over the three
  pairs whose main sets were both on disk, Runs 11 to 13, `offtab`, `build`,
  `gen-unsafe` and `bq-gen` sat in the widest six of all three, so it
  is a stable property of the arms; **it is not sampling error**, `list` having
  the fewest samples of any arm and a *higher* `CI%` than `offtab`, `mut-odo`
  or `build` while its spread is a third of theirs; and **the two instruments
  name different arms**, `offtab`'s interval unremarkable where its spread
  is the roster's worst. **They are not a speed tier** --- the two narrowest
  arms are the README's fastest and slowest --- and three of the four share
  a shape law `CI%` has no counterpart for, disagreement growing as runs shorten
  and rank rises (Spearman against `sInner` -0.55 to -0.64), so what is priced
  is the placement of the per-run work rather than of the per-element work;
  `gen-unsafe` is flat against every dimension and wide for some other reason.
  **The instrument wants a pair whose variable does not act per shape**:
  a nursery pair's halves price the nursery instead (Run 15), while
  its repetition against Run 14 reproduced the ranking. `offtab`'s alone leg
  spreads 21% across three processes of one binary at `-A32m` (2026-08-18,
  `small-pinned-churn-investigation/nursery-position-findings2.txt`),
  so no single-process reading of that arm means anything. **The fill family's
  placement control exists since 2026-09-09**: `mut-odo-vecdims-add-in-leaf-u2`
  carries copies beside its base and at the roster's far end, and eighteen legs
  of `flip-last-rows` on Run 27's binaries say the split is per arm and not per
  run, `-u1-ptr` spreading 30% within one binary at one setting; that the view's
  floor is a distribution and not a figure, its A/A triple running 0.46%
  to 11.31%, so a clause on it is read against the max; and that the variable
  is the allocator, `-A64m` moving nine of ten arms to 0.83 to 0.87 of their
  `-A32m` cells with the bytes and offsets unchanged. **One reading is unread**:
  `bq-scan-rem-gm-mulback` moved 1.0419 across Run 17's flag change, slower
  on all 24 shapes with both twins slower on 23, a consistent 4% on an arm
  the layout account does not cover. **What would settle the rest**: correlating
  the per-shape spread against `sInner`, `l`, `m` and rank for what the four
  arms share, arithmetic over kept artifacts, and a twin on one of them
  to separate position from code.

- `ANSWERED` **What the eight stride classes are worth as instruments --- read
  against each other for the first time on 2026-08-14, over Runs 10 to 13.**
  What they differ in is not a class property but a confound in the crossed
  design, *distant* having always also meant *earlier*; the account is in [the
  stride classes and what they cover](#the-stride-classes-and-what-they-cover).
- `PARKED` **`scaled`'s A/A slot is real and its size is not: a disturbance
  at the `mut-odo-vecdims` slot recurs, its magnitude never repeats,
  and the ruling is to quote the slot as a hazard of the class and never
  as a figure, a margin under about 3% there being unmeasured.** **PARKED
  2026-09-26 by the owner.** **Two thirds of it is arithmetic**: the forcing
  term is some 60% of the bench, so `1 + raw/(1-f)` turns a raw 2.13%
  disagreement into the 5.36% published, and that arithmetic reproduced on three
  runs while the quantity it explains moved 5.36%, 3.27%, 1.51% and 5.47% across
  Runs 10 to 13, the pair carrying it swapping and the sign inverting.
  **At sample level it is a step and not a ramp or an outlier** (2026-08-14,
  `run13-maxskip-scaled.json`): the disturbed arm runs at its base's speed
  for 69 of its 89 post-ramp samples, then steps once by +4.46% and stays,
  allocation identical to the byte, GC count and peak heap level, the cost
  in mutator time; the signature repeats on the twin or on the base wherever
  the artifacts survive, which is why the ratio moves in either direction ---
  a state the process enters once and keeps, the block-pool report's signature
  rather than a scheduling lottery's, and why the mechanism's logging is per
  sample. **It is intermittent between processes and not only between runs**:
  eight processes of the class in one sitting (2026-09-07,
  `probe-order-reversal.sh`) fired it in one, on `scaled-rank1-m1`, and neither
  the arm nor the shape repeats reliably. **Do not reach for a filtered re-run
  of the six controls**: filtering collapses the spans the crossed design needs,
  which [the floor section][floor] records as making a span unmeasurable.

- `PARKED` **The basis half carried the wider class floor over Runs 15 to 18,
  and nothing since Run 23 reproduces it.** **PARKED 2026-09-26 by the owner.**
  Over Runs 15 to 18 the published half's class floor was the wider in 24 of 32
  comparisons, sign p 0.007, across pairs differing in an RTS setting,
  an allocation area and an instrument. **A floor is an order statistic
  and not a spread** (2026-08-23): read the median A/A deviation per half beside
  it and the halves are alike, so what was asymmetric was the tail. Neither
  the half nor the evening position explains it since: four classes run in both
  orders on two recipes (2026-09-06 and -07, `probe-order-reversal.sh`) put
  the basis wider in 5 of 16 and the first process in 11 of 16, and Runs 24
  to 29 put the basis wider in 29 of 65. **The LEVEL follows the half
  and not the position**: the basis was the faster half in 15 of the 16 reversed
  readings, most of the margin the compiler's, shrinking once the GHC
  [#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778) workaround
  was in --- read per class, `--cross-classes`'s *all below 1* line answering
  whether every class agrees rather than whether the margin moved. **The one
  figure to take from a class is its FLOOR**, the max over its A/A pairs, which
  `--block` prints and the class table carries, and not `read-all.sh`'s
  worst-cell column, a max over cells; and **a class margin is read against
  its own run's column and never the previous one**. What would close the entry
  is a ruling that it is retired on that evidence; what would reopen it
  is a mechanism, which nobody has proposed.
- `ANSWERED` **What Run 33 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 33's own file](runs/run33.md), where a run's
  registrations have lived since 2026-08-29; in a clause each: (1) KILLED,
  the lean fill 3.54 points apart on the main set where the exit span was meant
  to level it; (2) HELD, `list` inside 2% on the main set and 3% on all ten
  classes; (3) KILLED, the shared per-run loop level on `runs` where 0.81
  was predicted; (4) HELD, the shipped leaf inside 2% and its fusion at 0.6428;
  (5) HELD in all forty-four floor-pair readings; (6) HELD, the exit span worth
  under 2% to either fill arm across the two builds; (7) NOT ADJUDICABLE,
  the shipped shim reporting no exit span astride at all.
- `ANSWERED` **Price the exit span against the entry count, `LOOP_EXITSPAN=1`
  against `LOOP_ENTRIES=1`, each under the dead-spot form --- registered
  2026-09-15, before either has been built into a half, and answered the same
  day by the probes rather than by a run: LEVEL, so the exit span stands
  and the entry count is parked.** B, `LOOP_ENTRIES=1`, crosses more windows
  than A almost everywhere, reads level with A on thirteen cells on both
  compilers and loses 7 percent on `window-224x224-k3`'s stage 9, so A,
  `LOOP_EXITSPAN=1` under the dead-spot form, is the simpler rule and the basis,
  and B stays in the shim, off, with the sweep beside it; the readings
  are in [the placement section][floor]. Run 33's registration (6) then held
  on the switch on all three of its spans, [in Run 33's file](runs/run33.md).
- `ANSWERED` **Why `libunord-stage10-sum` trailed `libunord-stage9-sum`
  on the `window` views while retiring fewer instructions, and why HEAD moved
  stage 9 and not stage 10 --- answered 2026-09-15.** Stage 10's tie-break makes
  each run the longest unit-stride axis, a chain of dependent adds at the FADD
  latency, so the arm is latency-bound, placement-blind and the same on both
  compilers, while stage 9's short runs overlap and run at instruction
  throughput, placement-sensitive, HEAD's difference on it being the compiler's
  code order; the account is in [the placement section][floor]: no placement
  defeats the rules, and none mends HEAD. **On the tiny views the arm also paid
  the zero-stride move on every call**, whether or not a zero stride is there;
  stage eleven, `libunord-stage11-sum`, guards the move ([Run 33's
  file](runs/run33.md)).
- `ANSWERED` **At a large nursery an earlier bench in the same process
  permanently slows a later one --- the condition is named SMALL-PINNED CHURN
  and its cost the churn tax.** Run 14's probes found it (2026-08-15/16),
  its counter signature has held through everything since, **and it is
  not the pinned-spray pool condition of GHC
  [#27601](https://gitlab.haskell.org/ghc/ghc/-/work_items/27601)**. The account
  is in [the floor section][floor]; the measurements, their tables
  and the recipes to re-take them
  are `small-pinned-churn-investigation/nursery-position-findings2.txt`'s.

- `PARKED` **One residue of the small-pinned churn, one answered, neither
  blocking its filing.** **PARKED 2026-09-26 by the owner.** Open, and since
  2026-08-21 no caller's, every horde-ad suite running at `-A32m`,
  so the residue belongs to the filing rather than to this README: the `-A1G`
  alone transient's micro-mechanism --- early and late iterations carry EQUAL
  cache-miss and dTLB counts per iteration while cycles differ ~17%,
  so the fresh-heap advantage is in miss cost or overlap, not count ---
  and the instrument that would name it, load/store-split or `perf mem`
  sampling, is unavailable on this machine (no IBS exposure; findings item 58).
  Answered: the added misses at `-A4m` are mutator-side, the collector's own
  symbols carrying ~1% of samples in every cell, so the conceptual objection
  in [the floor section][floor] stands measured (item 56).

- `PARKED` **`mut-odo-vecdims-add-in` leads `mut-odo-vecdims` on one compiler
  and not on others, and why is knowingly given up.** **PARKED 2026-08-25,
  and the two-shim pair that would separate code from slot is not
  to be re-proposed nor carried as a rider**: the margin is one to three
  percent, the regime 3 fix is not chosen on differences that size, and since
  the prune of 2026-09-04 the arm is `Only`, the shipped fill carrying the axis
  it added. What is kept is the reading, so a later run meeting the lead finds
  it recorded. On 9.12 `add-in` leads by one to three percent at 19 or more
  of 24 on Runs 17 to 19, and on 9.14 and GHC HEAD the margin is absent (Runs 18
  and 19). **The two arms are not the same code**: their innermost loops
  are byte-identical, but `mut-odo-vecdims`'s worker carries an `imul` per run
  that `-add-in` threads as an accumulated add, [the ceiling section's Core
  reading](#the-mutable-ceiling-taken) confirmed in the timed binary --- yet
  the margin does not track `sInner` as a per-run cost should.
  **Nor is placement the account**: the `-g3` twins swapped the two arms'
  offsets between 9.12 and 9.14 and the sign followed, but the `build`/`mut-odo`
  control, its copies at offset 0 on both, moved as far with no slot change,
  and on HEAD the slot account predicted 9.12's margin and there was none.
  So the lead is not a property of the arm, and what it is a property
  of is unidentified.
- `ANSWERED` **Gate 3's sign reversed, and the reversal is the arms' and
  not the read's.** **ADJUDICATED 2026-09-05, AND IT IS THE ARMS.**
  In instructions, off Run 25's counts sweeps, the in-situ term over `sum-only`
  is a median of **1.0000** on both arms and both halves; in time at fixed
  iteration counts, `(t(2N) - t(N)) / N` off `probe-gate3.py`, it reads
  **1.065** and **1.074** on the basis and 1.025 and 1.130 on the control.
  So forcing a vector the fill has just written takes a few percent longer
  than `sum-only` takes for the same instructions, the correction subtracts
  that much too little, under a point on published geomeans, and the correction
  stands; the gate's wording, written for a read bias and now describing an arm
  cost, is a decision and not a measurement. The probe counts criterion's
  `benchmarking` lines and refuses any count but one, `-n`'s bare bench name
  being a prefix.
- `ANSWERED` **What Run 18 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 18's own file](runs/run18.md), where they were moved
  on 2026-08-29; a registration is that run's record and reads against
  that run's tables.
- `ANSWERED` **What Run 19 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 19's own file](runs/run19.md), where they were moved
  on 2026-08-29; a registration is that run's record and reads against
  that run's tables.
- `ANSWERED` **What Run 20 was built to answer, registered before it ran ---
  and what it answered.** The registrations, their kill conditions and their
  verdicts are [in Run 20's own file](runs/run20.md), where they were moved
  on 2026-08-29; a registration is that run's record and reads against
  that run's tables.


### Standing rulings from past runs

**What this heading holds is rulings taken in past runs' write-ups, and no task:
what the next run should do is the open list's `OPEN` entries above.** **Every
run's `What Run N made cheaper` block is in `MARGINALIA`, appended there
at post-run step 5d --- Runs 33 to 44's in the archived `MARGINALIA.old.1`
beside this file --- and this heading keeps none**: what a block asks
of the procedure is made in the chapter or a tool in the same write-up, which
is where the next run meets it.

**A scope limit belongs in the sentence that asks for the measurement.** A fact
recorded as a tool's limitation goes inert where it is recorded beside the tool
and not where the run is planned: `run-counts.sh` covered the main set alone
for its first runs, the limit stated only in its own header, so the class
populations had no counted work and nobody saw it until the question was asked
from outside. It was never a question of cost, the classes sweeping faster
than the main set; the script takes an optional class, and step 20 of the run
list sweeps every population.

**And one class not to repropose: work that needs an aligned build.** The basis
has been max-skip since Run 12, the builder of aligned pairs is deleted,
and a two-shim pair can hold every tracked loop at one offset in **both**
halves, which is the property alignment was wanted for; the experiment
an aligned build would arrange, two arms' offsets swapped, arrives free whenever
a pair changes codegen, as on Run 18. `mut-odo`'s wide interval is the live case
([the open list][open]).


### Non-urgent TODO list

- `OPEN` **When the lazy list ships, its PR description owes one sentence
  on the consumer's shape, or the library loses the fusion the harness
  measured.** The fusion probe of 2026-09-09 (Run 28's registration, the fusion
  premise) found that a `build`-form producer and a `foldr`-shaped consumer fuse
  only when the fold is applied to the list expression itself, from an inlined
  producer: a consumer that pattern-matches the producer's result and folds
  a case-bound variable, or one whose fold is a closed partial application
  that full laziness floats to the top level, materializes the list, at 145
  bytes a run against 88 fused under the level-form walker and none
  under the flat one. Master's `sumT` is the right shape,
  `sum . map vSum . toUnorderedVectorListT sh` applied directly, and both list
  entry points are `INLINE`; the port of `lazyRuns` has to keep both properties
  and the flat walker's shape, every continuation known, which is what lets
  a fold the library did not write allocate nothing (Run 28's item (12)),
  and any new consumer written as a `case` over the list loses it silently,
  since every value stays correct. And the route the odometer list replaces
  was never fusible: the branch's table list, a comprehension over `VU.toList`
  of the base-offset table, read 1.000 in allocation under the same fold
  in the same probe, as master's recursion did, so a consumer of today's
  `toVectorListT` builds the whole list before it folds, on either side
  of the branch. Say both where the reviewer will read them.
- `PARKED` **Two measurements the `dispRun` cut was settled without, kept
  because the cut rests on them.** **PARKED 2026-09-26 by the owner.** Run 25's
  probe placed the crossover between the slice route and the fill at 2048
  and found the cut wrong by at most a few points either side of the cache,
  which is why it stood until the re-cut of 2026-10-04, over a different fill
  ([the `dispRun` entry][open]). What it did not measure is a length between 96
  and 4096 PAST the cache, where the in-cache crossover then sat and which one
  more view would place; and the allocation multiple of the two routes, which
  the reader cannot compute for a view `Main.hs` does not list, so they
  were read in bytes. Neither blocks the ruling and both would sharpen it.
- `OPEN` **Boxed broadcast runs still store element by element: fill
  an innermost broadcast by doubling copies from the instance's `copyRun` on ---
  registered 2026-10-06, unmeasured.** Since the commit "Copy whole runs inside
  the fill from a length each instance picks" on `pr-mikolaj-toVectorListT`,
  the library's `genericFillStrided` copies each run at stride 1 whole
  from a run length each `Vector` instance passes, because a boxed `writeArray#`
  pays GHC's write barrier on every store --- the array's header written again,
  a card marked, the nonmoving collector's test --- and one `copyArray#` a run
  pays it once. The innermost broadcast, `writeRunSet`, still stores one pointer
  `sInner` times. The remedy is already in the fill: `copies` doubles a block
  onto a zero-stride level's positions, so storing the element once
  and then `copies sInner 1 outPos` would pay the barrier about log2 `sInner`
  times --- one branch at the head of `writeRunSet` on `sInner >= copyRun`,
  no new walk, and nothing evaluated, the copy moving pointers. Expected near
  the runs' 3.4x on long boxed broadcasts and less, or a loss, on short ones,
  so the cut wants measuring rather than borrowing from the runs' 5. **The real
  question is the shared cut**: Storable and Unboxed stores pay no barrier
  and their broadcast loop is one store an element, unrolled by two, so doubling
  `memcpy`s may win only on long broadcasts in cache; if one `copyRun` does
  not fit runs and broadcasts at every kind of vector, broadcasts want a number
  of their own per instance, a cost in the hook not to pay for a small gain.
  Not worth special-casing: a whole constant view as `VGM.replicate`, which
  saves even the doubling pass but is one more pattern recognized inside
  the fill. In `Main.hs` the views with an innermost broadcast under the ordered
  route are `bcast-inner8`, `bcast-inner900`, `bcast-tall-Mx2`, `bcast-src8`,
  `bcast-src64`, `bcast-src512`, `small-bcast32` and every `compose` view;
  `bcast-tall-Mx2`'s broadcast of 2 sits below both cuts, and `bcast-inner8`,
  `small-bcast32`, `compose-rev-bcast`, `compose-slice-bcast`
  and `compose-bcast-nest` below the Storable one, 64; the unordered route moves
  the zero stride outside an adjacent unit-stride axis, which of these only
  `compose-scalar` lacks. This harness times Storable Doubles only, so it can
  price the Storable half; the boxed half wants a boxed bench, `[r, 1]`
  stretched to `[r, k]` for `k` from 2 to 4096 and one constant view, under GHC
  HEAD and the shim.
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
  classes, run by run](runs/run45.md#the-stride-classes-run-by-run) carries
  the figures.
- `ANSWERED` **The roster order biases the table, and nothing corrects for it.**
  **A slot correction is refuted**: Run 9 showed the effect is not a per-slot
  gradient but a step, worth nothing on most arms and 35--40% on one family
  at one shape ([the floor section][floor]), and a linear fit in slot number
  would smear a real 40% across thirty rows that do not have it. **Run 10 took
  the warm-up bench** instead, `sum-only-early` above `list`, at the cost
  of re-basing every published ratio; interleaving or randomising the order,
  the other fix, breaks comparability with every run so far and was not taken.
  The placement gap the `build`/`mut-odo` pair shows is a separate target
  no reordering reaches.
- `ANSWERED` **The published basis has left the regime this chapter's figures
  are ruled to be read in --- RULED 2026-09-13: the deciding regime follows
  the basis to plain -O1.** Plain -O1 is what the shipped
  `Data/Array/Internal.hs` compiles under, so Runs 8 to 29's `-fspec-constr`
  readings are history the series does not continue, and a run publishing at -O1
  owes no flagged column.
- `ANSWERED` **`--para` compiled its argument as a regex, so a bolded lead
  pasted verbatim failed SILENTLY and an unbalanced bracket tracebacked ---
  TAKEN 2026-09-13.** **The fix retries the pattern as a literal, at the lead
  search AND at the body search**, a registration item having no bolded lead
  at all; cases `para-traceback-on-a-bracketed-lead`
  and `para-refuses-an-uncompilable-pattern`, both of which failed before it.
- `ANSWERED` **A driver line that says what is yours to do next must say WHEN
  --- TAKEN 2026-09-13.** `run-evening.sh`'s *the verdict is yours to write
  into $R-pair.txt* line, printed two seconds before the sequence begins,
  was acted on inside the sequence and voided two benches, so it names run-list
  step 19a and step 17 outright. It carries a record and no case: the line
  is reachable only where the gate runs and passes, which no stand-in here makes
  it do.
- `OPEN` **No build-vs-output time decomposition.** `diag` measures per-builder
  *allocation* only, so a claim like "the table build is a third of the cost"
  --- the natural reading of `bq-mut-runs` beating `bq-mut` by 39% --- cannot
  be checked here. The question no longer needs it --- a Core diff identified
  what the flag deletes from the scan builder and the ~4% it is worth accounts
  for where the pair lands, the two arms sharing their output code exactly ---
  but the residue does: how much of each arm's own ~25% absolute gain is build
  and how much output is still unmeasured, and the same question stands
  for every other arm in the table. It needs a timing mode alongside `diag`'s
  allocation one, using the fixed-iteration differencing the horde-ad
  performance model prescribes (`-n 200` minus `-n 100`, fresh processes) rather
  than criterion, since the builders are not benchmarks.
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
  an installer only makes one cheaper to write. **Counted work instead
  of sampled time, wherever the question is an ordering, is REFUSED**
  (2026-08-22, `run16-a32m` against Run 16's column): over the timed arms
  the count ordering agrees with the time ordering at Spearman 0.725,
  and the disagreement is not a residue but the fast tier, what an instruction
  costs spanning more than twofold across arms, so where arms differ in
  it the clock decides. Counts are layout-free for an A/A pair, though
  not between two different arms under the assembler shim, whose padding retires
  ([what moves a figure](#what-moves-a-figure-when-no-strategy-changed)),
  so counts ride as the check of what a time change is made of, never
  as the ordering instrument, `run-counts.sh` being the driver. **Randomised
  slots in per-trial processes instead of pinned ones is REFUSED too**: many
  short fixed-`-n` trials per cell, each in its own process with the order drawn
  fresh, would turn position into noise that averages, but `offtab` and `build`
  spread 12 to 14% across ten single processes of one binary on a quiet machine
  (2026-08-22), a mutator term that clock, TLB, last-level misses, ASLR and huge
  pages were each measured not to be, leaving physical page placement --- a term
  no in-process control sees and one this regime would draw afresh per trial.
- `STANDING` **Render the run-scoped prose from what the reader already
  computes, section by section, and never from a ledger file.** The end state
  this entry first proposed was verdicts, statuses, floors and tallies kept
  in one small machine-readable file beside the roster, `read-run.py` rendering
  them into the run's file as `--in-place` renders the tables. **REFUSED
  2026-08-26 as a single file, and the installers answered it by arriving**:
  they write the Results table, the fingerprint and a block per class
  into the run file, so a ledger would be a second home for what already has
  one, bought with a rewrite of the write-up procedure, and the cross-class
  summary's emphasis is a per-run judgement no ledger can render either.
  **The direction since 2026-09-17 is the installers', extended one section
  at a time**, each installment taking out of a write-up's hands prose it used
  to type: the class paragraph's figures with `___` for its finding
  (`--block --compare`, installed by `install-tables.sh`), each registration
  item's span readings (`--predictions --in-place`), the apparatus every run
  file carried, kept once in [Reading a run file](#reading-a-run-file), and one
  cell's readings over every run as a generated table (`--series`). Kept
  as a ruling because the single-file mechanism is attractive and was proposed
  twice.

- `OPEN` **More checks of the floor-consistency shape: one figure, several
  sites, must agree.** **The first thing such a check needs is the sites**:
  a check that knows too few phrasings passes while a wrong figure sits
  in a site it cannot see, so the floor-pair check knows seven and reads all ten
  sites, which is why that duplication is left standing rather than cut:
  a figure repeated where a checker reads every copy is cheaper than a figure
  stated once and pointed at from five sections. Widen the patterns when a run
  rewords a lead. The floor pair, the roster size and every population size
  quoted as `over N shapes` are checked, the last two against Main.hs since
  agreement alone cannot see a count that is stale everywhere, and so
  is the floor-movement sentence beside the class table, its second figure being
  a claim about the column printed right above it. **The class-process count
  is checked SOMEWHERE and not everywhere**: a run spends one process per class
  per half, so `N class processes` must be quoted somewhere as the block count
  or twice it, where requiring every quoted figure to be the structural one
  fails a run that names a subset, as of class processes rerun; a stale count
  is a run where no site quotes the figure. **The bare process total and the run
  window are refused**, `N processes` carrying several correct figures in one
  run file --- the sequence, one half, the reruns and what survived them ---
  so a sweep over it would flag right prose or admit anything. Non-vacuity
  is `rundoc-miscounts-its-class-processes`, and the check reads the RUN file
  and not the pair.
- `ANSWERED` **Does `offtab-scan-rem` belong in the fingerprint? It does,
  and membership stopped dropping arms at all --- taken 2026-08-24.**
  `offtab-scan-rem` is best outside the family on `reshape1-rank10`, 0.090
  against `bq-scan-rem-gm-mulback`'s 0.091, and passes the one-per-family clause
  by crossing that arm rather than tracking it, 0.171 against 0.131
  on `stretch-rank12`, so the two are not one strategy spelled twice; the notice
  names its shapes now instead of counting them.
- `ANSWERED` **Check that the basis half named in prose is the run's own ---
  taken 2026-08-19.** `--check-doc` holds every `run<N>-<half>` token
  in the Results section to the run its file is named for. **The scope
  is that section and not the whole file**, which is the ruling worth keeping:
  the forward-looking sections name the previous run's halves on purpose,
  so a file-wide rule would fail the document for saying what it means.
  The control in `defects.py` builds Run 14's defect out of the current run
  file, so it keeps working when the run number moves.
- `ANSWERED` **Check each class lead's shape list against its run --- taken
  2026-08-22.** `--block` now reports on stderr a lead that disagrees
  with the installed population, reading three things: which shapes the lead
  names, in what order, and each `l` and `sInner` against `Main.hs`. **The order
  is the ruling worth keeping**: the per-shape paragraph is installed in run
  order and labelled *in the lead's order*, so a lead listing them otherwise
  mislabels three live ratios, which no reading of the block can catch.
- `ANSWERED` **Have `--block` price a class-property break against the floor,
  not only sort it --- taken 2026-08-22.** Each break `--block` reports carries
  its paired margin, win count and sign p, that margin against the population's
  own A/A floor, and a line where the pair reads the other way round
  from the column, the reading a careful run makes by hand.
- `ANSWERED` **Print the eight-way extremes, because a class superlative has
  no derived source --- taken 2026-08-22 as `--extremes`.** The mode ranks
  the populations it is given, `install-tables.sh` calling it once after
  the installs and installing nothing, and prints the gap from the vecdims arms'
  plain one to the best arm outside them both ways, saying where the published
  column and the pair disagree. **What it does not rank is the main set**, which
  it refuses, that population having no row in the table these claims are made
  about --- so a superlative meant over all nine has no source here either.
- `PARKED` **Price a rotated pair as one cycle where the outer cycle is short.**
  **PARKED 2026-09-26 by the owner.** Registered 2026-09-15 off
  the `sumLazyRuns` reading in [the open list][open]: the tiers hand a group's
  residue to the inner head, and for a per-run loop whose inner body is a few
  instructions with a trip count of three, the outer cycle is the hot path
  and the inner's residue is the wrong thing to optimise. The trip count
  is not in the code, but the outer cycle's length is: when the inner body
  is under about sixteen bytes and the outer cycle fits two lines, sum the two
  heads' block-rule costs instead of ordering them, the inner's counted two
  or three times for an assumed short run. Exposure bounded: an inner loop
  with a long trip count under such an outer loses at most one crossing per
  iteration where the sum prefers the outer, the same size of error the present
  order makes the other way for every short-run loop, and the fill's rotated
  pairs, with inner bodies of 34 to 51 bytes, fall outside the rule. No cell
  measures what it would buy: on this loop the inner head's free residues read
  level inside one tree on HEAD, and on 9.12.4 the plain form found the optimum;
  the case for it is the rotated pair whose outer cycle is hot and whose inner
  head's free band leaves the outer's crossing somewhere that costs, which
  the sweeps say exists and no arm here has shown. Not built: the flag pair
  it would face is the block rules with and without it, on the stage arms'
  `runs` and `window` cells.
- `ANSWERED` **`MergeAccAx`, the `Ax` merge's accumulator, was a non-empty list
  with a strict head used as a possibly empty one, a head of extent 1 standing
  for *no axis yet* --- answered 2026-09-26 by deleting it.** Each of the two
  dispatches merges in loops of its own, local to the reader: `routeList5`'s
  `start` skips the axes of extent 1 up to the first kept one
  and `routeUnord14`'s takes the first sorted axis, and each hands it
  to a `canonicalizeAx` carrying the head as two `Int`s, which gives `routeOfAx`
  the head and the `InnerFirstAx` outside it, so no state stands for *no axis
  yet*. On Run 41's basis recipe against the fake-head merge, over the small,
  window, `stretch-coprime-r7` and `stretch-primes` views, `lib-stage3-lean`
  and `liblist-stage5-sum` retire 40 to 99 instructions a call fewer
  and `libunord-stage14-sum` 24 to 78, allocation unchanged but for 56 bytes
  less on `small-bcast32`'s unordered cell; a timing probe of 28 pairs a cell
  put no cell slower than its A/A floor and most small cells 1 to 2 percent
  faster. The loops pay only while they read the view's offset and length, which
  keeps GHC from floating them out: floated, a loop returning the merged list
  built the head and a cons a call, 48 bytes, one returning a `Maybe` 63 to 240
  bytes, and one returning an unboxed `Maybe` kept the head in registers
  but needed `MagicHash` and fell short of the local loops. `absAxes`,
  the unordered route's pass over the raw axes, is the opposite case, a function
  of its own whose pair GHC returns in registers, where continuing into the sort
  inside the reader cost 10 to 58 instructions a call; it carries no `INLINE`,
  which on a recursive function stops its worker/wrapper split: the pair came
  back boxed, 30 to 46 bytes and 61 to 148 instructions a call. What else lost,
  each against the form it varied: the merge step shared by the routes
  as a `foldr` handing the head to a continuation, 0 to 8 instructions
  on the small views; the list route's extent-1 skip factored into one helper,
  30 to 35 bytes; the head carried as an `Axis`, 53 to 299 instructions and 22
  to 120 bytes on the list twins; the list route fed `zipWith Axis`
  over the strides and the shape, which GHC materialises, 233 to 826
  instructions and 222 to 784 bytes; and the extent-1 skip moved from `absAxes`
  into `routeUnord14`, 168 to 784 instructions and 63 to 391 bytes. The honest
  types that lost to the fake head on 2026-09-25, on Run 40's basis recipe, cost
  a second constructor 16 to 34 instructions and 63 to 161 bytes a call
  on the list twins, the list as the accumulator 25 to 94 and 47 to 216 on all
  but one arm and view, and a fold started from a `case` on the zipped list 145
  to 500 and 224 to 560 on the list twins.


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

Four findings turned the mixed picture into `bq-expand`, which
is `vFillStrided`'s class default and not what the three vector-backed instances
run --- so this is the account of the pure default, and the shipped fill's
is [the mutable ceiling](#the-mutable-ceiling-taken). **Price the outer
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
employed to move input construction outside the clock, `NOINLINE` so
that the arms and the `check` mode run one compiled body of each strategy,
and the agreement check in a separate `check` mode so it cannot share
a computation with the benchmark via CSE. Each call stays inside the timed loop
because criterion's own loop, `whnf'`, is compiled without full laziness.
Under it the ranking is stable and every time scales with `l`, so nothing
is being optimised away.


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
back one at a time.** The halving moved the published geomean and the ratios
between strategies past the noise floor --- a change of population and
not of any strategy. The ruling and its reasons, and the two shapes that must
survive any later cut for a reason unrelated to their workload, sit
at `convShapes` in `Main.hs`, beside the list.

**Eight main-set shapes were retired from timing on 2026-09-04, ruled
on the same test as the three stride classes below: `stretch-inner1`,
`lenet-slice-c6-k5`, `cnn-L1-6x6-c1`, `cifar-L2-16-c64-k3`, `stretch-rank10`,
`conv1d-24`, `stretch-rank12` and `cnn-L1-12x12-c1`; seven of them stay retired,
kept in `check`.** Under the branch's fill every main-set view canonicalizes
to a rank-3 positive fill with a stride-1 level, or to a regime-1 slice, so what
a timed shape can differ in is its two inner extents, their strides and its run
count, and by that reading the eight duplicate what stays. `stretch-inner1`
is the regime-1 slice, O(1) at any size, which `small-flat64` times,
and the main-set shape the canonicalizing arms return an O(1) slice on.
`lenet-slice-c6-k5` is `small-patch-k5` to the stride. Four are rungs of one
ladder, `[A, 3, 3]` at strides `[9, 1, 3]`, whose kept rungs
are `cnn-slice-c32`, `cnn-L1-24x24-c1`, `cnn-L2-24x24-c32` and `vgg-14-c512-k3`:
`cnn-L1-6x6-c1` and `cifar-L2-16-c64-k3` each within a tenth in run count
of a kept rung, `stretch-rank10` a rung once its odometer is merged away,
`cnn-L1-12x12-c1` the fifth of five. `conv1d-24` is runs of 3 at stride 24
beside `gather48-src-50` at stride 50, which the `rev` class mirrors.
`stretch-rank12` is runs of 2 at stride 2, its rank merged away, the third
of three runs-of-2 shapes and the only small one, which the `small` class covers
now. The population moved, so a main-set geomean from Run 25 on re-baselines
against Run 24, as the halving's did, only the fingerprint's per-shape rows
and the anchors crossing. And `check` still holds every arm to the reference
on the eight, the entries staying listed in `Main.hs` under `retiredShapes`,
which is what the binary's roster and `read-run.py`'s counts read; the run file
that timed them is held to its own population by the provenance bullet's
*were retired DATE, after the run*, as a class is. A shape comes back
by deleting its name from that list, as `cnn-L1-6x6-c1` did on 2026-09-05:
as a rung it duplicated a kept one, but at 324 elements it is the second small
main-set shape beside `cnn-slice-c32`, and a per-call reading wants a population
and not a cell. The size rung `stretch-rank10` held, the only one between 5184
and 147456 elements, is a size argument and not a stride one, and is the first
thing to re-add if a size ladder is wanted.


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

The `big` class (`bigShapes` and `bigRunsShapes` in `Main.hs`) holds realistic
layers whose patch tensor exceeds `sizeCap` even for one image, and `runs` views
past the L3 cache. `sizeCap` is the element count that partitions the class
from the main set and every other class: past it a call is slow enough to starve
the sample count, so the class times only the arms `classArms` names,
at the multiple of criterion's default time limit `classBudget` gives. `Cin`
and the spatial dims scale `l` linearly too (in the full run, doubling `Cin`
~doubles the cost, quadrupling the spatial area ~quadruples it), but reducing
them reproduces a shape already here --- a per-position slice, or a smaller conv
--- so `nImgs` is the only dimension genuinely free to drop.


### The stride classes and what they cover

`mkStrided` transposes the two innermost dims of a dense array, so every stride
the main set carries is positive and its offset is zero. The library reaches
regime 3 through other operations too --- its two commonest inputs of that kind
among them, a broadcast being stride 0 and `rev` negative --- and the **stride
classes** are one population per producing operation --- three of them retired
from timing on 2026-09-04 and kept in `check`, the ruling being the paragraph
below --- named by the prefix that selects them, two excepted and named last:
`rev` (every stride negated, offset at the top), `revsome` (a strict subset
reversed, so the signs are mixed), `bcast` (an innermost stride of 0, every run
re-reading one element), `bcastmid` (the stretched axis in the middle instead),
`reshape1` (the `[n] -> [n, 1]` trap, innermost extent 1), `slice` (a view
of a larger source, so a non-zero offset with positive strides), `window`
(overlapping im2col patches --- the workload this README opens by naming,
carrying the overlap that the main set's bijective index map drops --- a strided
and a dilated k3 window among them), `scaled` (superincreasing strides, none
of them 1), `runs` (regime 2, not 3: an innermost run of contiguous elements
under a padded outer stride, the one population the library sends to slices
rather than to the fill), `flip` (a dense array reversed whole or along its last
axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1
once canonicalized; a gapped sub-block with each row reversed,
`flip-inner-gap64`, beside the same block with its rows in reverse order,
`flip-outer-gap64`, regime 2 --- the pair that separates the direction
of the innermost walk from the reversal as such, which the unordered candidate
is priced on; and one member that is not reversed at all, `flip-fwd-rows96`,
`runs-96`'s construction under a `flip` name, so that the class's own reversal
reading is two views of one process), `block` (regime 2 as a sub-block
of a wider array: the gap between runs swept from one element to a page,
a rank-3 block that does not merge, and an offset off an 8-element boundary),
`small` (one view per canonical regime at a few hundred elements, and a rank-5
im2col patch beside the rank-3 one, where a per-call cost is a share of the call
and its O(rank) part shows --- the one class defined by a size and not
by an operation) and `compose` (a zero stride combined with a second mechanism
--- reversed, sliced to an offset, a second zero stride it cannot merge with,
every stride zero, or beside runs under a reversed nest, where the placement
of the zero-stride axis decides which extent the odometer turns over on ---
as the library composes its operations and no one operation's class builds:
the other exception). Each is a short list in `Main.hs`, reusing a main-set
shape where one fits so that a class figure has a positive-stride counterpart
to stand next to; each generator's comment there says what it models,
and the comment heading them all, above `mkRev`, carries the coverage argument
--- a hypothesis about what a valid hand-built view can recombine, not a theorem
--- which is not repeated here. *Class* unqualified means one of these;
the other sense in this README always keeps its noun, *method* ---
a `class method`, the class-method tier, or in full a `Vector`-class method.

**Three classes are retired from timing and kept in `check`, ruled 2026-09-04:
`reshape1`, `revsome` and `slice`.** What a timed class has to be distinct
in is the form the branch's fill sees, `canonView` having dropped the unit
dimensions and merged what merges before it dispatches --- so the coverage
comment above `mkRev` reads per canonical mechanism --- and by that test
the three time mechanisms other populations already hold. Three of `reshape1`'s
four views canonicalize to the regime-1 slice `stretch-inner1`
and `small-flat64` time and its fourth to a main-set view, which is why
it is the class the correction degenerates on, nine arms sunk on Run 24.
`revsome` reproduced `rev` on every run it ran: its inner-reversed view
is `rev`'s mechanism and its two outer-reversed ones are main-set views walked
in another order, the fill's addressing being sign-agnostic,
and the sign-sensitive bounds it was built for belong to the packed Int32 scan
and are settled. `slice`'s views are main-set views plus a base offset the fill
reads once, and `block-run64-off7` and `compose-slice-bcast` time the offset.
Two overlaps stay, named where they sit in `Main.hs`: `window-64x64-k1x9`
canonicalizes to `runs-9`'s runs of 9 and is kept for the overlap
of its backing, and `compose-slice-bcast` is `bcast-inner8` at offset 7. Nothing
is deleted: `check` holds every arm to the reference on the retired views still,
`retiredClasses` in `Main.hs` is what the `classes` mode and `read-run.py`'s
class counts read, and `run-major.sh`'s `CLASSES` omits them, held to the binary
by its own cross-check. A retired class comes back by deleting its name
from that list. A run file that timed a class since retired is held to the count
that keeps it, which the provenance bullet declares as *were retired DATE, after
the run*, exactly as it declares views added after a run.

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
  on all of them, seen failing first wherever the failure can be fired; why
  the Int32 strategies cannot fail below a 2^31-element source whatever
  the stride signs, and the packed scan's assert that mixed signs did break,
  are at that assert and both Int32 comment sites in `Main.hs`.

**A class population is a handful of shapes** --- a scale, re-read off a run's
own cross-class table rather than maintained --- against a main set several
times the size, which is deliberate --- the classes are there to vary
the *mechanism*, and varying size and rank within one is the main set's job ---
but it decides how their results read. A class geomean rests on three cells,
so it is a summary of a handful of numbers rather than a statistic
over a spread; the per-shape figures are nearly the whole population
and are worth quoting where the main set's would be flattened away; winsorizing
has almost nothing to cap and `--pair`'s bootstrap interval almost nothing
to resample. What a class run can decide is whether an *ordering* inverts
under its mechanism and whether any strategy's `worst` crosses 1 there. What
it cannot do is be compared with a main-set number, in either direction.
**`runs` is one exception, a sweep rather than a triple**, because its question
is a crossover and not a mechanism: its views walk the run from 2 to 65536
at a fixed size, with one rank-3 entry whose inner dims merge
under canonicalization so the library's merge and not the listing sets its run,
and one at 4096 small enough that its source and result fit in L2 together.
**`big` is the other, its axis being size and not a mechanism**: its views
are those past `sizeCap`.

**The `runs` class and the library-shaped arms exist for regressions
this benchmark could not see, added 2026-08-28 after horde-ad caught one.**
Every population above is regime 3, and every arm isolates the regime-3 fill;
the stage-two branch changed the dispatch of every regime, and its `toVectorT`
route for contiguous runs --- the fill's stepping loop in place of one memcpy
per run --- was decided on a nine-element probe and then read 45% slower
and 15.7% more allocation on horde-ad's `inp-96x96/H-exec`, whose views are rows
of 96. So the roster carries arms that are ports of library code
and not strategies, which copy of the library each matches being
at its definition in `Main.hs`: `lib-stage1`, the shipped `toVectorT` whole;
`lib-stage2`, the branch's, its driver with both zero-stride conditions;
`lib-stage2-concat`, the branch with contiguous runs sent back to slices
and a concatenation, the repair candidate; and the list consumer under each
stage, `liblist-stage1` and `liblist-stage2`, the library's `toVectorListT`
followed by one concatenation, the same term in both, so that pair prices
the list's construction alone --- stage one's slice recursion against stage
two's base-offset table and its `VU.toList` --- in time and, exactly,
in allocation, which is what a consumer iterating the list pays.

**`lib-stage0` is master's `toVectorT` whole**: stage one's dispatch,
with regime 3 a vector built from the element list behind `toListT`'s test
for the natural layout, so it parts from `lib-stage1` in regime 3 alone
and is what the two stages replace; retired 2026-10-06 by the owner, checked
and not timed. **The ports fill through `fillStage3`, its `Axis` form, which
the library does not carry. A port hands a one-element list's element back
as `toVectorT` does and concatenates only runs**, so on a view the library fills
once a port and its fill are the same vector, the pair prices the list where
there is one, and the allocation column reads what the library allocates ---
the reason the lazy stages' dispatch is a value read by four shared readers.

**`lib-stage2-disp`, the slice route taken only where the canonical run reaches
`dispRun`, is retired**, 2026-10-06 by the owner, checked and not timed:
the library's fill copies each run at stride 1 whole from a length each instance
picks, which is that dispatch done inside the fill ([dead ideas][dead]).

**Three fill candidates sit beside `lib-stage2`**, each a fill change
under the same dispatch: `lib-stage2-u4`, the stepping run unrolled by four;
`lib-stage2-short`, a canonical run of 2 to 5 elements written by a body
of exactly that length, chosen once per row as the broadcast body is;
and `lib-stage2-lean`, the same fill under a leaner dispatch: a canonical view
of rank 2 or more can never carry the natural strides, the merge that made
it canonical having consumed every natural pair, so the regimes are read off
the merged form alone and the strides comparison the control's dispatch pays
is not paid --- the fill under it the branch's route, outside the laziness
ruling of 2026-09-07 as `lib-stage2`'s is ([dead ideas][dead]), and the dispatch
what shipped.

**`liblist-stage3` and `liblist-stage4` are the list entry point's candidates
under the ruling**: `toVectorListT` kept lazy up to the exception ---
canonicalized, so a unit or mergeable dimension moves a view to a lazier
pattern, its slices produced on demand by the odometer list and no table built
--- then the one concatenation the two ports carry, stage three
under the natural-strides dispatch and stage four under the lean one,
so `liblist-stage4` against `liblist-stage2`, under one lean dispatch,
is the lazy odometer list against the strict base-offset table wherever a run
exists and the same fill wherever none does.

**And beside those, the unordered entry point joins the family**:
`libunord-stage1` and `libunord-stage2`, each stage's `toUnorderedVectorListT`
one-block test in front of its liblist body and one concatenation -- the third
route the branch changes, rostered so that a shim-switch reading (Run 23's
LOOP_DEADSPOT among them) has its sanity readings, which no test of the branch
alone can show until GHC itself grows such a capability.

**`libunord-stage3` is the family's one candidate rather than a port**:
the one-block test generalized into the dispatch, the canonical dims sorted
by absolute stride from the lowest offset and canonicalized again, so the lean
rank test reads one block and everything else is one fill in address order,
every axis forward and the smallest stride innermost --- what Run 25's `flip`
finding, a reversed run at twice its forward cost on identical instructions,
says an unordered consumer pays today for nothing. **That finding's evidence
(2026-09-05, Run 25)**: `flip-last-rows` and `runs-96` are the same `l`
at the same `sInner`, one reversed and one not, and per call `mut-odo-vecdims`
reads about 2.1 of its forward cell, the stage-two routes about 1.9, against
a `list` paying about 1.08. **The counts say it is the memory system and
not the code**: `mut-odo-vecdims` executes 89 instructions in 31.5 million
an iteration more on `flip-last-rows` than on `runs-96`, the other fills inside
150 and `list` inside 4272 in 412 million, on both halves --- so the same code
does the same work and the doubling is what walking backwards costs, which
no fill can address; and both compilers emit the same loops there, every arm's
instructions reading 1.0000 between them but `list`'s, which is base's code.
**So a clause pricing `lib-stage2-lean` against `lib-stage1` on `flip-last-rows`
prices that floor and not the two routes, and is not to be registered
on that view again**: their corrected instructions there part by less
than a hundredth of a percent, `fbLibStage1`'s dispatch falling through
to the same fill, so the pair is an A/A control under two names, while
on the two other views such a clause has covered the same counts part by 8.5%
and 40.8%. **The arms whose counts DO move are the ones that choose a route**:
`lib-stage1` +6.4%, `libunord-stage1` +17.7%, `liblist-stage1` +20.3%,
`liblist-stage2` +106%, and `libunord-stage2` collapsing to a slice at 0.0004
of its forward cell, the canonicalization taking the library's route for those.
**Its fill half is ruled out for the library since 2026-09-07** ([dead
ideas][dead]), the list having to stay lazy, so the arm stays timed
as the ceiling of what an address-order fill would buy and what can land
is its dispatch. Against `libunord-stage2` its margin also carries that arm's
list and concatenation, which a reducing consumer does not pay, so the reading
is the direction where stage two falls back to the list and the tie where both
slice.

**`libunord-stage4` and `libunord-stage5` are the candidates the ruling
leaves**: the same sorted address order over the unordered list kept lazy up
to the exception --- one slice where the sorted view is one block, a lazy list
of forward runs where its innermost stride is 1, one fill only where no run
is longer than an element --- stage four under the natural-strides test
and stage five under the lean rank test with the sorted pairs canonicalized
again, so no `getStridesT` is built; each hands a single slice or a single fill
back as the ports do and concatenates only its runs, under the ports' own
`VS.concat`, so the pair with `libunord-stage3` is the same code where both
slice or both fill and a lazy list against the fill where runs exist,
and the pair with `libunord-stage2` prices the list's construction alone where
both list.

**Beside them the four reducing consumers**, `libunord-stage1-sum`,
`libunord-stage2-sum` (parked 2026-09-13, no registration having named it),
`libunord-stage4-sum` (parked 2026-09-11, the sorted dispatch having priced it)
and `libunord-stage5-sum` (parked 2026-09-13 with `libunord-stage3-sum`, their
pair read on three runs): `sumT` as the library composes it over each stage's
list, one slice at a time and no concatenation, returned as one element
that `check` holds to the reference's sum --- the first reading of the entry
point as it is used, the copy every Fill arm over a list carries being one
the consumer never pays. **And `check` carries a laziness gate since the same
day**: forcing the head of each list producer on 200000 runs of 20 must allocate
under 32 KB for the lazy ones and must not for the two ports of the branch,
whose strict base-offset table is the planted breakage that proves the gate
bites, the unordered candidates asked again on the same array transposed,
the exception's own move.

**A ruling stands over the quad loop, 2026-08-30, and it is Mikolaj's rather
than a measurement's: a stepping run unrolled by four is too complex
for orthotope, so `lib-stage2-u4` prices what that feature would buy and
is not a candidate to ship.** The measure is an intuitive estimate of complexity
taken PER ORTHOGONAL FEATURE, not a count of lines or loops and not a total
over a function that composes several: the shipped by-two loop is fine but close
to the bar, so a simpler loop is preferred over it where the performance
is close, while a function that joins that loop with further orthogonal features
--- the short bodies of `lib-stage2-short` among them --- is judged feature
by feature, and the short bodies stand or fall on their own. **They fell,
2026-09-04, on the same ruling and by the same hand: a body per run length of 2
to 5 is too repetitive and so too complex for orthotope, so `lib-stage2-short`
and `lib-stage2-short-lean` price what the bodies would buy, are not candidates
to ship, and are parked `Only` as `lib-stage2-u4` is; their Run 24 readings
stand in that run's file.**

**The lean dispatch is taken, 2026-09-05, for every dispatch that admits it,
in the branch's `regimeT` and in every natural-strides dispatch over `canonView`
here but `lib-stage2`'s, which keeps the strides comparison as the lean arm's
control**: mainly because the merged form decides the regime with no stride list
built, which is the simpler code, and because Run 24 read `lib-stage2-lean`
at or below `lib-stage2`, within the floor, on every readable population of both
halves and ahead past both floors on the four smallest main-set shapes (Run 24's
registration 2, whose verdict [the open list][open] keeps); the two shapes
it read behind past one half's floor, `stretch-primes` on the basis
and `stretch-inner256` on HEAD, execute the same corrected instructions to five
parts in ten thousand on both halves, so neither loss is the dispatch. What does
not admit it: the stage-one ports and `regimeOf`, which compare raw strides,
where the invariant does not hold; the two unordered ports' one-block test,
whose sort by absolute stride can make a rank-2 canonical view one block, which
the candidate `libunord-stage3` answers by canonicalizing the sorted pairs
again; and `check`'s own regime conditions, kept explicit so
that the equivalence is checked and not assumed. The licence --- after
canonicalization no adjacent pair satisfies the merge equation, and natural
strides at rank 2 or more are that equation at every pair --- was checked
against the branch's `canonicalizeT` the same day over 300000 random views
and every view up to rank 3 with extents to 3 and strides to 4, the control's
decision equal to the lean one on all of them, and two deliberate breaks
of it fail the check. The library-shaped arms each run on every population,
so a library change is read where a user would meet it, class by class,
whichever of the two entry points the user takes, and the `runs` class is where
the routes part; the reason each was landed or parked is at its roster entry,
and a run's own bench count is its bullet in [Provenance](#provenance); the last
change, the retirement of `lib-stage0` and `lib-stage2-disp` on 2026-10-06,
takes the roster to 551 benches --- the figure's second site, which
`--check-doc` holds to `Main.hs` beside the first, under [What the benchmark
does](#what-the-benchmark-does).

**What the classes are worth as instruments** (2026-08-14, over Runs 10 to 13):
the correction's amplification runs from 1.30x to 1.81x by class, so one class
makes the same raw wobble read half again worse than another, which is why
`--block` prints the largest pair's **raw** ratio and its amplification beside
the net. And the *distant* twin read slower in every class, which is a confound
of the crossed design and not a class property: every distant twin sat
in the group's first dozen slots with its base later, so *distant* also meant
*earlier*, and a residual cold start produces that sign. **Every class carries
at least three shapes**, two being too few for the winsorizing that protects
the main set, so that a single disturbed cell cannot own a class geomean, each
added shape being its class's own extreme rather than another size.

**A new class shape is checked to belong to its class and not merely
to compile**: `check` holds an arm to the reference on whatever view
it is given, so a shape in the wrong list would pass it; read the view, strides
and offset `check` prints against the class's defining property.


### Which population answers a question, and how to ask all of them

**This is the one statement of the rule; everything else points here.** A run's
populations are the main set and the stride classes above, and it leaves one
JSON per population per half, `$R-<half>-<pop>.json`. A mode takes any of them
and reads THAT file's shapes, and where it uses a floor it uses THAT file's own
A/A floor, so one question can hold on one population and be killed on another,
and the tolerance line names the floor it used.

**A question that names no population, or that says only `population` or any
word that could mean either, is answered on the main set AND every class.**
That is the reading that cannot under-report, and a question meaning less
than that says so in as many words. Inside a class block the block names
the population and `here` is enough --- and `--check-doc` holds it to that,
refusing a block that quotes a floor which is not its own. What must name
the population in words is a figure quoted OUTSIDE its block: in a head,
a registration, a claim, a checker's brief, or any sentence setting two
populations side by side.

To ask all of them: `./read-all.sh $R` gates every process a run left, both
halves; `./run-counts-all.sh` walks the main set and every class the basis
binary lists, which is where the roster comes from rather than a list written
here; and any reader mode loops the files, `$CLASSES` coming from the basis
binary as `run-counts-all.sh` derives it (`classes --list`), which
for the registration spans is post-run step 5c:

    for p in main $CLASSES; do
      ./read-run.py $R-$BASIS-$p.json --compare $R-$OTHER-$p.json --predictions
    done

The case on record is Run 26's registration (1) (`runs/run26.md`), whose one
span reads HELD on the main set and KILLED on `small` against that class's own
floors --- both correct, and a session reading only the main set would have
written HELD.


### The scratch vector flavour

Every table this suite builds --- the `m`-element base-offsets of the `bq-*`
family, the `l`-element offset tables, the odometer's dimension vectors ---
is an **unboxed** `Int` vector, as the fallback in `Data/Array/Internal.hs`
builds: index scratch is independent of the abstract element storage `v`,
so a payload being Storable says nothing about its scratch.

The probe that priced the flavour, 2026-08-08 at -O1: a twin differing
from `bq-expand` in the table's flavour and in nothing else, in the roster slot
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
Allocation is unmoved, so this is speed and not volume --- the same bytes, held
differently, by a mechanism nothing here measured and the probe does not need.
The one shape it loses is `stretch-square-1341`, which was the worst-measured
shape of both runs and is this README's standing warning about reading a single
cell.

**It was measured twice, with the arms' roles exchanged**, an unboxed twin
beside a Storable roster on a loaded machine and a Storable twin beside
an unboxed roster on a quiet one, 0.9377 and 0.9433, winning on the same 19
shapes of 24: a margin that survives exchanging which arm is the twin,
the machine's load and the direction of the change is the code's and
not the harness's.

**So every scratch vector here is unboxed, matching what ships.** Three arms
keep a Storable table and must: `backperm` hands it to `unsafeBackpermute`,
`cm-gather` and `all-expand` to `map`, and each of those takes one vector
family, so for them the table's flavour *is* the payload's and unboxing it would
change the strategy rather than its scratch. They
are the new-pure-`Vector`-method tier, and that is the same fact seen
from the other side. `strideOffsets` and `baseOffsetsExpandVS` exist for exactly
those three and say so. One arm pays for the unboxing, `bq-scan-packed-mulback`,
3.7% on every shape by a twin probe of the same day, unexplained, where
`mut-odo-vecdims`'s dimension vectors run 3.4% faster unboxed.

**The shipped fill's own dimension tables were priced the same way
on 2026-09-19, and there the flavour is worth nothing.** They hold one entry per
outer axis and are read once per odometer level, where `bq-expand`'s table has
an entry per run and is read per element; Storable twins of the three library
arms, `lib-stage2-lean-vsdims`, `liblist-stage4-vsdims-sum`
and `libunord-stage13-vsdims-sum` (`probe-vsdims.sh`, Run 36's basis recipe),
read 0.9971, 1.0052 and 1.0002 of their originals paired, all three inside
that half's floor. So the 5.7% does not carry to tables of two to four entries
read per level, the shipped fill keeps its unboxed tables, and the twins
are parked `Only`.


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
on the warm-up ramp. Run 8 puts the same pair at 1.0015 over its own 24 shapes,
12 wins and sign p 1: a dead tie. The regime is the whole difference --- same
arms, same shapes, same machine, one flag --- so what the trick buys is however
much of the division GHC has not already dealt with, and the answer
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

**On shipping it: not shipped.** What `bq-expand-lemire-out` would cost
is `MagicHash` and `UnboxedTuples` in `Data/Array/Internal.hs`, about a dozen
lines of helper, and a precondition. The precondition is the substantive part:
Lemire's identity holds for `d, n < 2^32`, and `n` here is the linear output
index, so a shipped version needs an `l < 2^32` test choosing between the two
fills --- loop-invariant and chosen once per call, but it must be there, since
orthotope does not otherwise cap array length. The 6.0% is a plain -O1 figure,
the deciding regime, and is what there is to weigh against `MagicHash`,
the helper and the precondition, on an arm the roster checks and no longer
times; under `-fspec-constr` the same pair is a dead tie. This README only
prices the arm.


### Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes --- chosen
to push past the ranges the rest cover, and named here without their prefix ---
against the strategies nearest the decision, each as a multiple of `list`
on the same shape. These are Run 20 (SpecConstr)'s own figures,
from its **basis** half as the fingerprint is, all of them net of the forcing
pass like the rest of the README:

| shape      | bq-expand | bq-expand-b | mut-odo | vecdims |
|---|---:|---:|---:|---:|
| `inner1`     | 0.078 | 0.067 | 0.224 | 0.090 |
| `rank12`     | 0.233 | 0.233 | 0.248 | 0.092 |
| `wide-2xM`   | 0.085 | 0.076 | 0.132 | 0.061 |
| `coprime-r7` | 0.111 | 0.110 | 0.058 | 0.035 |
| `pow2stride` | 0.126 | 0.123 | 0.123 | 0.122 |
| `primes`     | 0.094 | 0.094 | 0.031 | 0.029 |
| `inner256`   | 0.115 | 0.114 | 0.033 | 0.032 |
| `tall-Mx2`   | 0.067 | 0.067 | 0.023 | 0.022 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which
is the axis the orderings turn on; the fuller per-shape record is in [What
the next run compares
against](runs/run45.md#what-the-next-run-compares-against).

**The fingerprint is a per-shape summary computed from the run alone.** Two
tables under the run file's *What the next run compares against*, the main set's
and the classes' with a class column: per shape its `sInner` and `l`, `list`'s
net per call as an absolute --- the column `--machine` reads, guarding
the baseline at every shape and converting any ratio beside it back to time ---
then `mut-odo-vecdims`'s ratio, the best arm outside the vecdims arms
with its ratio, and the ceiling, the vecdims arms' leading arm with its ratio,
the three read as the cross-class summary's columns of those names are, per
shape rather than per population. A sunk cell reads `--`. Allocation has
no column on purpose, being deterministic per call, so a run that raises
an allocation question re-derives it within itself. **A column per arm,
under a membership rule carried across runs, is retired (2026-09-04) and
not to be re-proposed:** it made the table depend on every earlier run and
on a judgement at each write-up, for cells the run's own JSON derives. Run files
before Run 24 keep that form.

- **Which strategy wins is decided by the innermost extent (the size
  of the innermost dimension, `sInner` below) --- not by the rank, not
  by the element count.** `stretch-inner1` is where the expansion family does
  best against the odometer fills: `bq-expand` (0.078) and `bq-expand-b` (0.067)
  beat `mut-odo` (0.224) and `build` (0.214) by close to threefold, which they
  do on no other shape here --- `stretch-pow2stride` excepted, where the two
  families converge outright (0.122--0.126 across expansion and odometer alike).
  Its innermost extent is 1, so each base offset covers a single element:
  the odometer that `mut-odo`/`build` step has nothing to amortize over, while
  the expansion build has no per-element odometer to begin with. At the other
  end `stretch-tall-Mx2` has an innermost extent of half its length
  and the ordering inverts completely --- `mut-odo` 0.023 against `bq-expand`
  0.067, with every mutable fill ahead of every pure arm (the slowest fill
  0.051, the fastest pure arm 0.058). The geomean reports that second case
  and averages the first away, which is why this table is here.

  **It is not the only shape where the pure expansion strategies beat every
  mutable one** (refuted on Run 6): among the arms that fill it, `mut-flat-gm`
  and `bq-mut-runs-gm-mulback` tie ahead of every expansion variant,
  and the canonicalizing arms return it in O(1). The unit innermost extent
  explains why `mut-odo` and `build` do badly there; it never implied
  that no mutable fill could.
- **Per-shape figures are far noisier than the geomean: trust the first digit
  only.** Independent runs of these shapes agree within 1--5% on most cells
  but differ by up to 27% on `stretch-inner1/bq-expand-b` --- runs whose rosters
  also differed, making the [roster effect][floor] a candidate cause ---
  and the order of `bq-expand{,-b,-zf}` within their sweep of `stretch-inner1`
  flips between runs. The sweep itself reproduces; which of the three leads does
  not. `stretch-square-1341` is the standing warning on the point: on Run 20
  it is again the worst-measured shape of the set by median CI%, at 0.966,
  as it was on Runs 9 to 13 --- though no longer by the mean, where
  `stretch-tab7MB`, `stretch-wide-2xM` and `stretch-bigstride` are above
  its 1.065. It stays in the column, its influence capped.
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
- **The rows where both leaders of the pure tier lose to `bq-expand`
  are not derived again**: `vFillStrided` ships the mutable fill,
  so that ordering flags nothing.

The measured bullets above are on positive-stride views. The [stride
classes](#the-stride-classes-and-what-they-cover) put the same axis under other
mechanisms --- `bcast`'s innermost stride of 0 has every run re-read one element
whatever its extent, `reshape1`'s extent is 1 by construction, `scaled-rank1-m1`
is a single run --- so each class run is a test of whether `sInner` still
decides, and a class table that contradicts this ruling is a finding to write up
rather than a cell to average away.


### The fix in Data/Array/Internal.hs

**Decided 2026-08-22 and landed 2026-08-24: the regime 3 fix is `vFillStrided`,
the whole-kernel class method, with one shared driver, `genericFillStrided`**
--- the decision and what it rests on are [in the ceiling
section](#the-mutable-ceiling-taken), the signature ruling and the rejected
forms [in the two-stage plan](#the-two-stage-plan-and-the-rework-proposal),
and the arm's refinement from plain `mut-odo-vecdims` rests on the two paired
probes the ceiling records. `bq-expand`, the last candidate, is what every
figure below was measured against. This branch's library stays at stage one;
stage two is
[`pr-mikolaj-toVectorListT`](https://github.com/Mikolaj/orthotope/tree/pr-mikolaj-toVectorListT),
at parity with stage one or ahead of it since the unboxing fix ([the
ceiling][ceiling]'s tenth reading).

Regime 3 now goes through the class: `toVectorListT`'s innermost-strided branch
is `[vFillStrided sh ats ao l v]`. The method's default is the pure `bq-expand`
form --- `runBaseOffsetsT`'s expansion table, one `quotRem` per element ---
so the `[]` reference instance and any instance outside the tree compile
unchanged on a fast pure path, and the three vector-backed instances override
it with `genericFillStrided`, written once against `Data.Vector.Generic`, which
supplies the mutable machinery orthotope's own `Vector` class deliberately does
not: an allocate-once output, the odometer with the input offset stepped
additively, the innermost outer level fused into a dedicated loop
over the innermost runs, and the innermost-run fill unrolled by two
with its bound on the output cursor, so it is sound for zero and negative
strides; an innermost run at stride 0 reads its element once, and a zero-stride
outer level is filled once and copied onto its remaining positions by doubling.
The bang patterns are performance-essential, ported with the loop structure
from the benchmarked arm; the shipped file does not set `-fspec-constr` ---
the aligned HEAD probe read the flag irrelevant to the shipped family, the two
builds agreeing to three decimals ([the ceiling](#the-mutable-ceiling-taken))
--- while it stays the regime every figure behind the decision was measured in.

Validation on this branch:

- orthotope's own test suite: **596/596 pass** (Dynamic/Ranked/Shaped x
  boxed/storable/unboxed), with the fallback live through the method.
- Non-vacuity: deliberately dropping the `+ tInner` from the driver's unrolled
  second read fails 94 of the 596, `rev_2` among them --- so the pass
  is not vacuous.
- This benchmark: `check` agrees with `list` on every shape of every class
  for the ported arm, so the algorithm the driver ports covers negative,
  mixed-sign, zero and overlapping strides; the library port itself is validated
  by the suite and the break above.

**The latest reading of stage two against stage one is Run 26's, on both
compilers**: 0.24 to 1.02 over all eleven populations --- `runs` 0.2352, `block`
0.4392, `flip` 0.7600, `small` 0.7206, `bcastmid` 0.7846, `rev` 0.8949, `window`
0.8957, `compose` 0.9065, the main set 0.9714, `scaled` 0.9756 and `bcast`
1.0105 on the basis, and 0.2368, 0.4385, 0.7660, 0.7295, 0.7850, 0.8779, 0.8553,
0.9050, 0.9510, 0.9757 and 1.0177 on GHC HEAD --- ahead on ten and behind
on `bcast` alone, by most on the regime-2 populations where stage one takes
the slice-and-concatenate route, the two compilers within a point on eight
of the eleven.

End-to-end re-measurement in horde-ad's `bench/ConvVjpBench.hs` --- wiring
this branch's orthotope in and rebuilding ox-arrays + horde-ad --- was taken
on 2026-08-27, as horde-ad's `CLAUDE.md` records.


### The mutable ceiling (taken)

**Decided 2026-08-22: the ceiling is taken, and the code landed 2026-08-24.**
The `mut-odo-vecdims` family, narrowed to its `add-in-leaf-u2` member,
is the upstream implementation of the regime-3 fallback, with the new `Vector`
method it needs --- the signature the Core below shows is free in its callback
form, decided as the pure-typed whole-kernel form --- and no condition
on the strides, the redirect dropped for [the two-stage
plan](#the-two-stage-plan-and-the-rework-proposal), whose rework proposal serves
its constituency at the dispatch instead. What the decision rests on: the family
is nowhere slower than `list` on anything this README has measured, and every
arm that reads below `mut-odo-vecdims` --- the leaf block, the rework's
canonicalizing arms --- needs a mutating `Vector` method and nothing more, which
is exactly what the fix needs, so none of them reopens the decision. What
the decision owed is in [the fix section](#the-fix-in-dataarrayinternalhs).

**The `bq-*` strategies still fill the result one element at a time.**
The tightest possible shape drops to a **mutable result buffer**: allocate
it once, walk the outer odometer, and write each innermost run with a tight
additive inner loop --- no `quotRem`, no base-offsets table, no per-element
step. That is `mut-odo` and `mut-odo-vecdims`, whose family holds the top
of the table, all of them allocating essentially just the result vector.
`offtab` does not go that far --- its output is an ordinary `vGenerate` and only
its `l`-sized `Int` offset table is filled mutably, so it needs no class method,
just a mutable scratch --- and it sits well behind `mut-odo` once the loops
are aligned, so it is not the cheap way to most of the gain.

**Plain `mut-odo` does not make the case**: against `bq-expand` it ties
by the sign test on every run that has read it, the geomean carried by a handful
of large shapes over a per-shape range from 0.24 to 3.7, so the tier's argument
rests on `mut-odo-vecdims` alone.

The catch is the API: a buffer filled across runs cannot be expressed
by the per-element `vGenerate`; it needs a new `Vector`-class method exposing
a fill (or the `Storable`-only `unsafeCast` escape the amendment below records).
`build` prices exactly that --- `mut-odo` driven through `vBuildVS`, a prototype
of

    vBuild :: Int -> (forall s. (Int -> a -> ST s ()) -> ST s ()) -> v a

--- and **the class method is free**, `build` inlining to `mut-odo`'s identical
loop, so a gap between the two, as the 1.24x of Run 7 with neither source
changed, is the measurement and not the abstraction.

**The Core says the identity holds, in both regimes.** Dumped at -O1
and under `-fspec-constr` against one pinned dependency set, `$wfbBuild`
and `$wfbMutOdo` are the same worker --- identical once GHC's numbering
is normalised, with `vBuildVS` surviving as no top-level binding --- and the two
sources differ only by the `Strides` newtype's zero-cost cast. **The emitted
code agrees** (Run 17's `-g3` twin): the two workers are 1224 bytes each,
of which only 80 differ, all of them address-relative operands, which is one
function emitted twice at two addresses. So the identity now rests on the Core
in two regimes *and* on the machine code, and the pair stays this README's
cleanest known-true-ratio-1 control. **It is also the contrast that makes
the vecdims family's readings legible**: there no two arms share their whole
code at all, only an innermost run-fill and only four of the five, which
the family measurement below in this section has arm by arm. So **the signature
is free**, and no `vBuild` is to be held back on either run's figure.

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

**What the class method buys over the best pure arm is about 1.8x** ---
`mut-odo-vecdims` over `bq-scan-rem-gm-mulback`, the figure the decision turned
on, read paired from -O1 through Run 24 at 1.68x to 1.95x, the fill's real cost
having been the odometer's cons-list traffic and not the fill itself ---
and **it is approaching 2x and volatile at the tenth** between runs that differ
in roster or regime, so no ruling turns on a movement of that size. **Pin
the shape set before comparing it**: over Run 24's own 26 shapes the pair read
0.5493 and over the 25 that exclude `stretch-inner1` 0.5312, a movement
of a point and a half that is the population's. **The series ends at Run 24**:
the prune of 2026-09-04 parked the denominator, and until a run re-times
that arm the roster prices the family's own leaf ratio,
`mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims`, which is a different
question and not a continuation of this one.

**The in-tree precedent is `Data/Array/Internal/FastReshape.hs`** (removed
on the stage-two branch once the fill subsumed it), a `runST` flattener
over this same fallback territory --- structurally `mut-odo`, an allocate-once
mutable result filled through an outer odometer recursion with a per-element
strided inner copy loop, its outer offsets stepped additively where `mut-odo`
multiplies --- which sidesteps the `Vector` class altogether by `unsafeCast`
to `Double`/`Float` on element size. It is in no cabal file and still declares
its source project's module name and imports, so it does not compile in place:
precedent for writing such a module, not for shipping one.

**Its arithmetic weighed in code, 2026-08-08: the four FastReshape arms.** They
port the precedent's loop arithmetic onto `mut-odo-vecdims` one axis at a time,
a 2x2 plus one over that shared control: `mut-odo-vecdims-add-in`, the input
offset stepped additively in place of the loop's one multiply;
`mut-odo-vecdims-add-out`, the output position through a precomputed stride
table in place of the threaded return --- the axis that can lose;
`mut-odo-vecdims-add-both`, the corner, doubling as the endpoint contrast
that still reads if the solo margins sit inside the floor;
and `mut-odo-vecdims-add-both-down`, both loops in the count-down-to-zero form,
over the corner as its control. Any close pair among them is to be read
workers-first, per the `build` lesson above.

**Run 10 priced them on a build where the loop's placement cannot be the answer,
and Run 11 reproduced every one**: against `mut-odo-vecdims`, `add-out` 1.16,
`add-both` 1.12 and `add-both-down` 1.05, and `add-in` a tie or a small gain
([its entry][open]) --- so of the three axes FastReshape's arithmetic ports,
**the additive input offset is free, the precomputed output stride table costs
about 16%, and the count-down form recovers most of the corner's loss**,
the corner being sub-additive, the two axes largely paying for the same thing.
**The Core and the machine code say why** (2026-08-09, and Run 17's `-g3` twin):
`add-in` differs from its control by one `imul` per run, a multiply become
an accumulated add threaded as a further argument, 3424 bytes over 927
instructions against 3472 over 929; `add-out`, `add-both` and `add-both-down`
carry some 950 bytes and 240 instructions more, a `scanr (*)` table built once
per call and read once per run, so their cost is per run, and `add-out`'s
penalty scales as 1/`sInner` on Run 10's aligned half (r -0.64 against log
`sInner`, -0.01 against log `m`); and `add-both-down`'s innermost run-fill
is seven instructions where the others' is eight, the output position carried
in a register, a per-element change whose advantage grows with `sInner`. No two
arms share their whole code, only the innermost run-fill being byte-identical
across four of the five. **Run 9 had read the three 15 to 18% behind on nearly
every shape, and that was the address of a loop all four share**, its copies
straddling a cache line: a penalty near-unanimous across shapes separates
nothing, the identical-code pair showing the same, and the pad probe's straddle
price matched by coincidence for two of the three, its correction being a screen
licensed only where the arms differ nowhere but the loop. **So the in-tree
precedent argues for the *shape* of a mutable fill and not for its arithmetic.**

**The leaf fusion and the unrolling are what the shipped arm adds, each priced
by a paired probe of 2026-08-24** (the family arms in one process so the group
shares its placement, criterion's own mode, `probe-run20arms-*`
and `probe-x-*`). `mut-odo-vecdims-add-in-leaf` fuses the leaf call
into the innermost outer level over `add-in`, removing the per-run non-tail
call, level check and threaded return --- the additive output axis at the one
level that pays it, with no table --- and reads 0.83 and 0.68 of `add-in`
on the short-run shapes and level on the long ones, the per-run mechanism's own
signature. The fill **unrolled by two**, `mut-odo-vecdims-add-in-leaf-u2`,
a 48-byte twelve-instruction body with its bound on the output cursor
and so stride-sign-agnostic, reads 0.97 of the fused corner,
`mut-odo-vecdims-add-in-leaf-down`, more on a DRAM-bound shape
than its instruction count explains. **The count-down fill solo is refuted
by codegen**: under the leaf continuation the live `outPos` pushes its loop
invariants out of registers, so the down fill wants a unit-return context
and its solo arms, `mut-odo-vecdims-down` and `mut-odo-vecdims-add-in-down`,
are `Only`, the reason at their definitions. **Unrolling by four is ruled out**
(2026-08-27), for diminishing returns and the Haskell it would take, so the axis
ends at two.

**A third probe, 2026-08-24, put the whole family on GHC HEAD with every hot
loop aligned, on a quiet machine**, at `-fspec-constr` and without:
`mut-odo-vecdims-add-in-leaf-u2` heads the family at 0.820 of `mut-odo-vecdims`
overall, its one loss `stretch-inner256` at 1.058; **`-fspec-constr`
is irrelevant to this family**, the two builds agreeing to three decimals
in every column; the `add-in` lead dissolves under alignment, 0.998 against
its control on both builds; the corner ties `-add-in-leaf` with both fills
resident; and the down solo arms lose 14 to 16% uniformly, the reload penalty
undiluted once placement is gone.

**A fourth reading, 2026-08-27, is a disassembly: the `-g3` twin
of `run20-ghead`.** Every leaf arm carries two copies of its fill --- a rank-1
copy behind the top guard and the fused `run`-level copy every rank-2+ shape
executes --- so which copy a reading names decides what it says,
`scaled-rank1-m1` running the rank-1 copy for every fill arm.
`-add-in-leaf-u2`'s rank-1 copy is the twelve-instruction body with no load
beyond the work; **its `run`-level copy is seventeen, with the source base
and the output base reloaded from the stack before every load and every store**,
the fused level keeping `k`, `boff`, `st`, `sInner` and `op` live across
the fill. So the corner's Run 20 lead was the spill and nothing else,
and with the bases in registers the order is the probe's. The trigger
is the live-value class of GHC
[#27737](https://gitlab.haskell.org/ghc/ghc/-/work_items/27737), a stack spill
of the allocator's choosing. A `Ptr`-walking fill, with nothing to spill,
is refused as below the level this library is written at ([dead ideas][dead]),
and **a per-call cross-over on `sInner` is not to be written**: it would
dispatch around a codegen accident and be dead code once the allocator is fixed.

**A fifth reading, 2026-08-29, kills `mut-odo-vecdims-add-in-leaf-u2-down`
at its premise: the count-down form is a value HEAVIER across the loop
that runs.** `-u2`'s bound `oEnd = op + sInner` serves twice, bounding the fill
and becoming the next run's `op`, so `op` dies at run entry; a falling count
bounds the fill and nothing else, so `-u2-down` holds `op` and `sInner` live
across the fill, six free variables in the run loop's continuation against four,
and on the fused copy spills both bases where `-u2` spills one, on both
compilers. **So no change to `Data/Array/Internal.hs`**: the shipped `-u2` fill
is the better of the two wherever the fused level runs.

**A sixth reading, 2026-08-29, shows the fused loop CAN be allocated without
spilling**, under `-fllvm` (`probe-llvm-g912`, a codegen reading and
not a regime this README adopts): both loops want more than the eleven registers
there are, and LLVM spills run-level values reloaded once per RUN where the NCG
spills `base_in`, read twice per ELEMENT. **GHC's linear allocator lacks
the weighting** (`GHC.CmmToAsm.Reg.Linear`, read at `d415f38a75`):
`allocRegsAndSpill_spill` takes the head of `nonDetUFMToList`
over the assignment map as its victim --- no next-use distance, no use count,
no loop depth, the module's own note carrying *not used for a while* as a ToDo
--- and the graph allocator's spill cost sets every loop frequency to 1
and is disabled regardless (GHC
[#7679](https://gitlab.haskell.org/ghc/ghc/-/work_items/7679)); the victim
following introduction order is what GHC
[#27742](https://gitlab.haskell.org/ghc/ghc/-/work_items/27742) reads
from outside. The restore an iteration is a block boundary's, `JoinToTargets`
reconciling assignments at a label another edge also targets. Even spill-free,
`-u2-down` stays one instruction heavier per two elements.

**A seventh reading, 2026-08-29, found the branch's fill's term a BOXING failure
and not an inlining one**: `fillStage2` re-scrutinised the boxed source vector
inside the loop, pushing an eighty-eight-byte frame and writing ten live values
into it per two elements --- fifty instructions and twenty-three stack accesses
against the shipped fill's eighteen and four, the counted work's 2.776 matching
50 over 18. **No pragma can lift that**: the `INLINE`s on its helpers had fired
all along, a rebuild with them emitting the fill byte-identical.

**An eighth reading, 2026-08-29, takes the fix: one bang an argument**,
`sh ats !ao !l !v` on `genericFillStrided`, the `vFillStrided` default beside
it and the port alike --- mirrored, because a bang the port carried
and the library did not would make `lib-stage2` stop measuring what the branch
ships. The worker then takes `Addr#` and `ForeignPtrContents` where it took
a boxed `Vector`, and the fill is a real loop. In the library the strictness
arrives through the `INLINE` template, `case ao`, `case l` and `case v`
at the head of the body it hands each call site, its demand signature unmoved,
so the monomorphic port and not the library's own Core is where to read it.

**A ninth reading, 2026-08-29, is the counted work after the fix**: `lib-stage2`
against `lib-stage1` reads parity or better on every regime-3 population
that carried the term, where Run 21 read 1.7 to 3.5 times, and the broadcast
paths moved in stage two's favour too, for a reason this reading does not name.

**A tenth reading, 2026-08-30, is the TIME after the fix, and it retires
the regression this benchmark was built to catch**: `lib-stage2` against
`lib-stage1` reads 0.78 to 1.08 over the regime-3 populations where Run 21 read
2.43 to 4.54, every one inside its floor or ahead but `slice`, behind
by an eighth where it was behind by four times --- most of that since read
as the benchmark's own shim and the thirteenth reading's epilogue term.
**The second term dies with it on regime 3 and survives on broadcast**: time
over counted work reads about 1 on regime 3 where Run 21 read 1.16 to 1.67,
and 1.49 on `bcast` and 2.50 on `bcastmid`, unmoved --- the term was the frame
and its store-to-load chains, and the broadcast loops never had a frame.

**An eleventh reading, 2026-08-30, names the broadcast term by counters**
(`probe-stalls.sh`): cycles per instruction agree with the clock's,
and on `bcastmid` front-end stalls, cache misses and branch misses all run
several times stage one's rate, on `bcast` cache misses alone ---
so the branch's broadcast paths are bandwidth-bound, executing a quarter
to seven tenths of stage one's instructions in more time, and instructions
retired is the wrong currency for them.

**A twelfth reading, 2026-08-30, timed `-u2` against `-down` in a spill-free
`-fllvm` binary** and found the ordering unmoved, against the sixth's prediction
from its counts, whose half-instruction difference changed sign between two LLVM
builds of one source. **So an ordering differenced off a dump predicts only
where the counts hold across the builds compared.** The eighteenth reading reads
the ordering in time on the fill that now exists.

**A thirteenth reading, 2026-08-30: once the shim's padding came out
of the counted work, the branch's remaining cost was ONE INSTRUCTION A RUN,
at odd run lengths only** --- the epilogue reloading the output base where
the shipped fill held it in a register, every even-run shape reading 1.0000
to 1.0002. The fourteenth reading removed it; **what stays is the method**,
a per-run term being visible as an even/odd split where a per-element one
is not.

**A fourteenth reading, 2026-08-30, fixes it from the other end, and its ruling
is the refuted candidate**: hoisting the odd tail out of the loop added two live
values and made every odd shape WORSE, by up to 18%, so **in a fill whose
binding constraint is register pressure, under an allocator with no next-use
information (GHC
[#27742](https://gitlab.haskell.org/ghc/ghc/-/work_items/27742)), a source
change that ADDS a live value cannot be argued sound however much arithmetic
it saves.** What works is one line: step the source cursor twice by `tInner`
instead of once by a doubled stride, dropping that stride from the live set,
sixteen instructions and four stack accesses per two elements becoming twelve
and one.

**A fifteenth reading, 2026-08-30, gives the SHIPPED fill the same line**,
and `-u2-down`, which has to stay `-u2` with one change: on the native backend
the shipped fill drops 14.76% of its instructions over the main set, up to 25%
on long runs, while under `-fllvm`, where nothing spills, the same change costs
4.5%; the un-unrolled leaf, with no doubled stride to lose, reads +0.00%
on every shape, the control. With both fills changed `lib-stage2` against
`lib-stage1` reads 0.9414: nothing about the branch's fill was ever ahead
of the shipped one.

**A sixteenth reading, 2026-08-30, screens every other arm for the same tweak
and finds none to make**: the change pays by freeing a register in a loop
that spills, and `tools/probe-nospill-fills.py` over a shim-free dump build
finds no stack access in any timed arm's element loop but `list`'s, which
is its recursion's closure traffic and the denominator besides,
and `bq-expand`'s, whose three live values none derives from another. **What
the screen cannot see**: it reads Main-compiled code only, so an arm whose loop
is inside a library function, as `gen-unsafe`'s is in `vector`'s `generate`, has
no entry.

**A seventeenth reading, 2026-08-30: the change frees a register in the two
UNROLLED fills alone**, inverting both of the family's comparisons in counted
work with both directions right and both magnitudes too large, as the eighteenth
read in time; and in a shimmed build `-down` RISES 15% with no source change,
the shim padding a loop the change displaced, so a count delta does not carry
between a shimmed and a shim-free build.

**An eighteenth reading, 2026-08-30, reads it in TIME in one process,
and the shipped fill now leads**: `-u2` over `-down` goes from 1.1070 to 0.8348
at 7 wins of 7, and `-u2` over `-u2-down` becomes a tie, 0.9981 ---
so the twelfth's ordering is refuted for the current fill, and the fifth's
account of why `-u2-down` loses is spent. **Read it in-process only**:
the untouched `-down` moved +15% in time between the halves, so a cross-half
comparison of an arm the pair did not change is not a reading of that arm.

**A nineteenth reading, 2026-08-30, prices the change in time on the main set
and `slice`**: the shipped fill reads 0.9031 on the main set, 0.8541 on `slice`
and 0.8682 on `runs`, and `lib-stage1` 0.9087, 0.8560 and 1.0026 on `runs`,
where stage one never reaches the fill, which is the reading's consistency
check. **Against the counted work of the same binaries that is about three
quarters**, 13.1% of the instructions buying 9.7% of the time and 18.6% buying
13.2%. And `-down`'s move between the halves is INSTRUCTIONS and not placement,
its counted work rising 15 to 22% in the shimmed pair where the shim-free pair
reads +0.00% --- **so a control is a property of the pair it was taken on**:
the eighteenth's 0.8348 is about thirteen points of the change and fifteen
of `-down` moving under it, and the change is worth a tenth to a seventh,
not a quarter.

**A twentieth reading, 2026-09-05, reads the three leaf loops that RUN,
by profile, under three allocators**: under the linear one each reloads
the source base from the C stack once an iteration, `mov 0x40(%rsp)` --- `-u1`
at seven instructions an element, `-u2` at twelve for two, the leaf at nine ---
so the unrolling's instruction gain is amortising that one reload;
`-fregs-graph` spills more, and `-fllvm` orders the two the other way,
so neither is a stand-in for a fixed allocator. **Registered for the first pair
on a patched compiler**: `-u2` over `-u1` at about 0.92 in corrected
instructions on the long-run shapes, from 0.86 on the stock compiler,
and the `0x40(%rsp)` line gone from all three loops.

**A twenty-first reading, 2026-09-05, dodges the spill at the source and prices
the unrolling alone at a quarter.** `mut-odo-vecdims-add-in-leaf-u1-ptr`
and `mut-odo-vecdims-add-in-leaf-u2-ptr`, the leaf fills with their cursors
as running pointers, are the `Ptr`-walking fill refused for the library ([dead
ideas][dead]), rostered as the ceiling each parent would reach
under an allocator that spilled nothing and parked `Only` since 2026-09-13:
with no stack access, `-u2-ptr` executes 0.8356 of `-u2`'s corrected
instructions and 0.8604 of `-u1-ptr`'s, 4.50 an element on long runs against
6.00, so **once the spill is gone the unrolling is worth a quarter of the loop
in instructions**. Pointers in the leaf alone,
`mut-odo-vecdims-add-in-leaf-u1-ptr-leaf`, cost an index-to-pointer conversion
per run, 1.0581 of `-u1` over the set --- the shape not to propose again.

**A twenty-second reading, Run 26, times the pointer fills**: `-u1-ptr` reads
0.9693 of `-u1`, so that parent's spill is worth about a thirtieth of the fill,
and with the reload out of both arms the unrolled one is further ahead,
not nearer, `-u2-ptr` over `-u1-ptr` at 0.8605 in instructions and 0.9431
in time --- the opposite of what the twentieth registered for a compiler fix,
which a source rewrite is not. **The rate at which an instruction saving reaches
the clock is a third to a half here**, against the nineteenth's three quarters
across two builds, so a span DERIVED from that rate misses low, as Run 26's
registration (8) did three times ([the open list][open]). On GHC HEAD the two
pointer fills lost the saving and allocated 1.41x and 2.61x, which is GHC
[#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778).

**A twenty-third reading, Run 27, holds with GHC
[#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778) worked around**:
the `:: Ptr Double` annotation on each bang-bound `plusPtr` result gives HEAD
the basis's code, both pointer fills at 1.00x on both halves and their ratios
within a point of the basis's, so the ceiling is a ceiling on two codegens.
The rate reads a third to a half again, and a real 3.1% instruction saving can
cost 1.4% of the clock (`-u2-last`), so a span derived from a count ratio can
miss in either direction.

**The reload is priced on shipped code without either.** `lib-stage2-lean`
over `lib-stage1` at `flip-whole-square` is the rank-1 copy against
the `run`-level one, in one process on one input, and its margin
is that `0x40(%rsp)` line and not the rank it sheds --- 11 instructions a pair
against 12, where the `Ptr` form reaches nine --- at 0.9154 in corrected
instructions on both halves of Runs 25 to 28. It is not GHC
[#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799)'s latch, which
is in the un-unrolled loop. The two pointer arms being parked, a further reading
of this kind needs one un-parked.


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
per-element in Haskell however the fallback is written. Closing it needs C;
the mutable fill `vFillStrided` shipped on 2026-08-24 is a win
under this ceiling and not a step toward closing it. This is discussed further
in the horde-ad repo.


### Dead ideas

**Taking the source base once through a `Ptr` and reading it with `peekElemOff`,
instead of indexing through the vector --- refuted 2026-09-05.**
`mut-odo-vecdims-add-in-leaf-u1-base` is the un-unrolled leaf written that way,
and it executes **0.9985** of `-u1`'s corrected instructions over nineteen
shapes, on a counts probe whose own header calls it a smoke run and
not a recorded column: a tenth of a percent, where losing one of the run copy's
seven per element would be some fourteen. So the `0x40(%rsp)` reload is still
there and this shape does not price it. The same sweep reproduced the two ratios
already on record, `-u1` over `-u2` at 1.0859 against Run 25's 1.0892
and over the counted leaf at 0.8497 against 0.8456, so the null is the arm's
and not the instrument's. It stays rostered `Only`, checked and not timed,
so the refuted shape is on the record rather than in anyone's head; what did
dodge the spill is the `Ptr`-walking form of [the
ceiling](#the-mutable-ceiling-taken)'s twenty-second and twenty-third readings,
which is refused for the library for its own reasons.

**Choosing the run as the longest contiguous chain over every order of absorbing
axes, `libunord-stage8`, in place of the tie-break's longest unit-stride axis
--- refuted 2026-09-11, on Run 28's registration (6).** The chain can beat
the sort only where an axis whose stride equals the run's length is
not the sort's neighbour of the run: a blocker of intermediate stride between
them, dims [4,3,4] on strides [1,2,4], runs of 16 where the sort stops at 4;
or two axes tied at the run's stride of which the smaller leads on to a third,
dims [4,2,4,3] on strides [1,4,4,8], runs of 24 where the tie-break takes 16.
Both are self-overlapping views with an exact tiling at the same scale, which
a parity reshape of a hop axis produces and no image view does: im2col at any
hop or dilation, pooling, patchify, channels-last and transposed windows carry
strides at two scales, 1 and the row width, and the chain needs one at a third.
On the roster the chain's run never differs from stage seven's ---
`small-patch-r5`, the one view the registration named, reads sixteen runs of 16
under both --- so what Run 28 priced was the dispatch, an exhaustive search
over lists, and the order of two tied levels the chain leaves in stage six's
form where stage seven reverses it: 1.05 behind stage seven on `window` and 1.22
to 1.26 on `small-patch-r5`, on both halves. `libunord-stage8-sum` is checked
and not timed since; the route stays for `check`.

Ideas that **died on paper**, recorded so they are not re-proposed --- and,
first, those that did not die on paper at all:

- **A run-length dispatch inside `toVectorT`, one memcpy per run above
  a threshold and the fill below it**, `lib-stage2-disp` with `dispRun` at 2048
  --- **it works, it is 8 to 12% faster on the `runs` class at runs of 4096
  to 65536 on a 14 MB array, and it was ruled out until the owner overrode
  the ruling on 2026-10-06.** **Over the branch's fill of 2026-10-04 it is some
  1.5 to 3.5% faster, net, at runs of 16384 and 65536**, level with the fill
  or up to 3.5% behind it at 4096 and 10.9% and more behind it at runs of 1440
  and below, and `dispRun` stands at 8192 ([the `dispRun` entry][open]). RULED
  OUT 2026-09-07 on code complexity, which sat right at the threshold,
  with the dependence on a hard-coded constant tipping it: the threshold
  is a run of 16 KB sized to the L1 and cut on this box, a library would carry
  it blind, and the past-cache probe read the crossover moving with the working
  set. **OVERRIDDEN 2026-10-06 by the owner**: since
  `pr-mikolaj-toVectorListT`'s commit "Copy whole runs inside the fill
  from a length each instance picks", `genericFillStrided` copies each run
  at stride 1 whole, one `VG.unsafeCopy` a run, from a run length each `Vector`
  instance passes, and steps the shorter ones --- the dispatch on run length,
  done inside the fill, and well enough to be worth the longer source code;
  its Storable cut, 512 bytes, is set past where a copy's cost a run is paid off
  and not to this box's L1. The fills here kept in step with the library carry
  the copy (`copyRun` in `Main.hs`). What the gain is worth and where --- a tie
  past the L3 at 64 MB, the per-call comparison priced on `small`,
  the real-world views that reach it --- is at the arm's definition
  in `Main.hs`, and its figures stand in Run 26's `runs` table and the `dispRun`
  entry; the arm itself is retired, checked and not timed.
- **A `Ptr`-walking fill under `unsafeWith`**, bases folded into the cursors
  so there is nothing to spill --- **it would work, and it will not be done.**
  What it would buy is measured rather than argued: LLVM performs exactly
  this transformation on the same source, and [the ceiling][ceiling]'s sixth
  reading reads every fill out of that build with no stack access at all,
  thirteen instructions per two elements where the native backend spends sixteen
  and two NOPs over four. **RULED OUT 2026-08-29 all the same, and not
  on a measurement**: raw pointer arithmetic under `unsafeWith` is below
  the level orthotope's fallback is written at, and buying a code generator's
  defect back with a Storable-only instance override is not a trade this library
  makes. So the spill stands until GHC's linear allocator weighs an eviction
  by anything at all, which is a report's lever and not this file's,
  and no future reading of what the fill would buy reopens it --- the refusal
  is about where the code belongs, so a larger figure argues for the report
  and not for the fill. **Measuring it does not reopen it**:
  `mut-odo-vecdims-add-in-leaf-u1-ptr` and `-u2-ptr` are rostered, `Only` since
  the ceiling was read, as the CEILING each parent would reach under a register
  allocator that spilled nothing ([the ceiling][ceiling]'s twenty-first
  to twenty-third readings), the refusal being of shipping the fill and
  not of measuring it --- and the form's codegen differing between compilers
  until a workaround is a further reason not to ship it.
- **Starting `sumNoSpec`'s per-run sum from the run's first element, its loop
  tested at the bottom** --- **it works, it makes `libunord-stage14-sum` about
  a third faster on `runs-2` under GHC HEAD and 9.12.4 alike and up to 27%
  on `window`, and it will not be done.** NOT TAKEN 2026-09-23: the harness's
  consumer stays close to the library's, whose `sumT` sums each run
  with vector's `sum`.
- **Unrolling `runSlices`'s per-run loop by two** --- **it works, it makes
  `libunord-stage14-sum` a quarter faster on `runs-2` under GHC HEAD and a sixth
  under 9.12.4, slower on no measured shape, and it will not be done.**
  NOT TAKEN 2026-09-23 on code complexity: `runSlices` is already too complex
  for a second copy of its run step.
- **Skipping the fill's level table where the view has at most one outer level,
  `fillStage2OneLevel` under `lib-stage3-lean-onelevel`** --- **it works,
  it makes the roster's two single-level views of tens of elements 6 to 11%
  faster, and it will not be done.** NOT TAKEN 2026-09-24 as fragile
  for a constant: the saving is a few hundred instructions a call ---
  `small-bcast32` at 0.895 of `lib-stage3-lean`, `small-row96` at 0.942, level
  at large `l` --- and, as the special case is naturally written, its runs loop
  is inlined into the fill with the result's length and buffer live across it,
  and GHC's allocator reloads and stores a stack slot every two elements, 4
  to 13% slower than `lib-stage3-lean` on Run 39's large single-level shapes.
  Routing the case through the recursive odometer removes the spill at a 72-byte
  closure a call, which is a trick against the allocator, and the special case
  is complication that `genericFillStrided` does without and `fillStage2`, which
  since 2026-09-24 builds no table at any level count, has no use for. Its arm
  went to `Only` on 2026-09-25, Run 40's 7 to 18% on plain -O1 not changing
  the verdict ([the one-level entry][open]).
- **Building `fillStage2`'s level nest out of closures, a loop per level around
  the one below** --- **refuted 2026-09-23 at 1.3 to 2.5 times the instructions
  of the fill it replaced, and repaired it still loses, so the nest is data
  walked by one known function.** As first written, `runsWith` met a partial
  application and stayed out of line, calling each run through an unknown
  function with boxed arguments; each level returned a boxed position; each
  closure sat in a lazy field, entered through an indirection; and the fused
  level's stride and extent came from a lazy pattern. With all four repaired
  it reads 6 to 17% over the table on the conv shapes: an unknown call every
  iteration of the level above the fused one, whose callee saves its free
  variables to a frame for the boxed arguments an unknown caller passes. Two
  ways round that lose as well: closures taking `Int#`, for which the RTS has
  no apply pattern beside a state token, so each call goes through `stg_ap_n`
  and two stack frames; and, in the data form, a recursive runs function
  in place of `fused`'s `NOINLINE`, whose self-call is a call and not a jump,
  1.24 of the table on runs of 2. Inlined into `run`, the stepping loop spills
  a register every two elements where it advances by a value other than `sInner`
  itself, a field equal to it included, or is inlined further into the fill's
  body, where the result's buffer and length stay live across it, 6 to 22%
  over on the stretch shapes; with neither it has sat in `run` since 2026-09-24,
  where the older `Rep` and `Dim` pair spilled it too, for a reason not found.
  `handoff-fill-prologue.md` holds the readings.
- **Speeding up `toVectorListT` or `toUnorderedVectorListT` by returning a less
  lazy list** --- the whole array filled as a singleton list, or a table built
  before the first slice --- **it may well be faster, and it will not be done.**
  RULED OUT 2026-09-07 on the interface rather than on a measurement: the list
  is produced lazily always, so a consumer folds it slice by slice in memory
  bounded by the rank, and `anyT` and `allT` stop at the first slice
  that decides, where a fill does the whole array's work and allocation before
  the consumer sees an element. Regime 2 on master is that lazy list,
  a difference-list recursion consumed on demand; regime 3 never was, one vector
  built through `toListT`, so the branch's `vFillStrided` there is not this.
  **One exception, taken the same day**: where canonicalizing the shape
  and strides moves a view from one of these patterns to another and nothing
  else changes --- as master's own dispatch already sends one view to the long
  lazy list and another to a one-element list --- the laziness lost
  with the move is permitted; what is not is a pattern itself made less lazy.
  What the ruling forecloses is the fill half of `libunord-stage3`'s library
  form, whose dispatch half stands on its own, its consumer
  `libunord-stage3-sum` staying. What it does not reach is `toVectorT`, strict
  whichever way it is built: the branch's fill of contiguous runs there ---
  `lib-stage2`'s route and `lib-stage2-lean`'s under the lean dispatch ---
  stands or falls on the runs class and not on this ruling. The branch's `Runs`
  regime builds its base-offset table whole, by `runBaseOffsetsT`, before
  the first slice --- the same kind of step, on the run count rather
  than the size, and outside the exception, the pattern itself changing.
  No timed arm can see either, every arm being forced whole through a sum; what
  sees it, since the same day, is `check`'s laziness gate, which forces the head
  of each list producer on 200000 runs and requires the two ports of the branch
  to fail it, and what prices it for the consumer is the `-sum` arms ([the
  stride classes](#the-stride-classes-and-what-they-cover)).
- **Cutting a run longer than a constant C into runs of C in the unordered list,
  so that the one-accumulator consumer's chain of adds never exceeds C** ---
  died on paper 2026-09-16, on size and on the constant. The size: the cut has
  to come after `canonViewOfPairs`, which merges a chunk level whose stride
  equals the inner extent straight back into one run, and it needs a second walk
  over the same outer levels for the remainder where C does not divide the run,
  so the route becomes two walks and a `-list-sum` arm is owed beside the `-sum`
  one to price the longer list to an unfused consumer: some forty lines beside
  stage eleven's seventeen, for what is a guard of one line there. The constant:
  Run 33's `runs` class on the basis half has stage eleven at 0.70 ns an element
  on runs of 2, 0.289 on runs of 9, 0.38 on runs of 96 and 0.60 from 4096 up,
  the asymptote being the dependent-add rate [the open list][open] names
  in its answer of 2026-09-15; a probe the same day over `runs-32`, `runs-48`
  and `runs-64` read 0.31 at 32 and 0.38 at 48 and 64 beside 0.31 at 9 and 0.39
  at 96 in the same process, a plateau to 32 and a step by 48 --- so C
  is a figure read off one Zen 3, about 32 here, and the win it buys
  is that machine's. The simpler forms meet the same two walls. Stage six's
  tie-break in place of stage seven's takes three of the unstrided `window`
  views back, by 17 to 37 percent on Run 33's basis, and gives up the two
  with channels and `window-28x28-k5`, by 19, 48 and 32, the lever being the run
  length and not the tie; a cut at the square root of the run leaves
  `runs-65536` in chunks of 256, on the asymptote; and any partition
  of the multiset into contiguous runs sums each run serially, so no run choice
  under the unordered contract escapes the latency without a length. What
  escapes it is a fold the library drives with two accumulators, a different
  entry point and not this list.
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
  state, and a stateful fill is exactly what the mutable ceiling's class method
  provides, which is what shipped. The table exists because `vGenerate`
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
explain: the [Results](runs/run45.md#results) columns and the [per-class
blocks](runs/run45.md#the-stride-classes-run-by-run). What is *not* here
is anything a particular future run has to settle --- that is [What
is open](#what-is-open), the chapter at the front, which is where everything
that goes stale as soon as a run reports is now collected.


### What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT` faithfully
(specialised to `Storable Double`, horde-ad's element storage), then compares
the regime-3 strategies in one binary --- the real orthotope compiles only one
at a time, so a replica is the only way to A/B them.

**One element type, where the fix serves them all.** Everything here
is `Storable Double`, where the fallback is polymorphic over the `Vector` class
and the element type; [the probe](#one-element-type-and-what-the-probe-found),
a program of its own, is the evidence that restriction rests on, boxed excepted.

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
  is not re-proposed), `bq-expand` (**`vFillStrided`'s class default**),
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
that roster with the strategies, and not strategies themselves, are twelve
controls: eight A/A arms --- `bq-expand-aa-adjacent` and `bq-expand-aa-distant`,
`mut-odo-vecdims-aa` and `mut-odo-vecdims-aa-distant`, `list-aa-adjacent`
and `list-aa-distant`, and `mut-odo-vecdims-add-in-leaf-u2-aa`
and `mut-odo-vecdims-add-in-leaf-u2-aa-distant`, four strategies each duplicated
in both positions, the last pricing a slot for the arm the library runs where
the others price the family root and the references ---
the `sum-only-early`/`sum-only-late` pair, and `bq-expand-nosum`
and `mut-odo-vecdims-nosum`, each its base arm forced with one element instead
of the sum. [The noise floor](#what-moves-a-figure-when-no-strategy-changed)
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
it costs no information the run needs. Its neighbours were probed
for an aftermath and showed none.

**The timed roster is cut by three rulings, and every arm a ruling drops stays
rostered as `concat-runs` is, `Only`, checked against the reference on every
shape of every class and not timed**, so the agreement net does not shrink
and nothing has to be rewritten if a ruling is later reopened; the reason
for each is at its roster entry, spelled as the arm's own assert spells a bound.
Two rulings of 2026-08-08 are the bullets below. **The third, the prune
of 2026-09-04, cuts the timed roster to the one question the benchmark still
serves: how exactly the `mut-odo-vecdims` family is used in the library.** What
stays timed is `list`, the reference; `bq-expand`, the class default;
`mut-odo-vecdims` and the shipped fill `-add-in-leaf-u2`; and the library-shaped
arms with a question left, with their consumers. The pure arms the decision
of 2026-08-22 retired from candidacy, `build` and `mut-odo`, whose identity
is settled, and the fragments that have delivered their reading and vary a body
nothing ships are `Only`. **A parked arm's A/A twins and `Force` arm are deleted
rather than parked**, a control of an untimed arm pricing nothing, and the slots
that stay keep their order, so `sum-only-early` still precedes `list`
and the distant twins still sit early. **A run's own bench count is its bullet
in [Provenance](#provenance)**; the last change to the roster, the retirement
of 2026-10-06 by the owner --- `lib-stage0` and `lib-stage2-disp`, reasons
at their entries --- takes the roster to 551 benches, so with the controls
the run is 29 arms. **An arm parked with a registration standing on it leaves
that registration unreadable**, so a run that wants such a clause read times
the arm for that run alone, as Run 26 did four, which reopens no parking's
grounds.

- **A strategy with a precondition is not measured.** The column allowed `none`,
  an empty cell, and `shape well-formed`, which is a condition on being a valid
  view at all rather than on size; everything else is a size bound the caller
  would have to discharge. What that costs is real --- it takes `bq-odo-mulback`
  (0.089), the fastest pure arm of Run 8, and the whole `mulback` output family
  with it --- and the ruling is that the speed does not make up
  for the restriction: a fallback that needs `l < 2^32` tested and a second fill
  kept for when it fails is a different proposition from one that does not,
  and this suite exists to find the second kind. Its unconditional counterpart
  `bq-odo-gm-mulback`, written for the ruling as each dropped arm without one
  got one, came in within a thousandth of the arm it replaced on Runs 9 to 13,
  so dropping the bound cost about a point. **The `Int32` narrowing alone cannot
  be rescued**: its bound is `int32Fits` on the source, which is what narrowing
  *means*, so `offtab32` and `bq-expand32-lemire-mulback` have no unconditional
  form --- the ruling's sharpest cost, the narrowing being the one hand-packing
  that survives the flag, at 0.877 of its control for `offtab32` and 0.949
  for the expansion pair.
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
and its 23.5x is the thing being beaten.


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
and leaves half of `.text` different at the same size. So two runs' binaries can
differ for a reason nothing recorded here names, and the pre-run list's md5 step
says what to read to find out. It postdates the earliest runs recorded here
and so cannot pin theirs; what covers those is a hand check that `vector`
and `criterion` have been the same versions since Failed Run 6 inclusive, which
is what lets a question about generated code be asked across those runs at all.
One pin is load-bearing rather than housekeeping: `vector` is built
`+boundschecks -unsafechecks`, which is what MADE the `gen-quotrem`/`gen-unsafe`
pair price a bounds check at all, since one uses `VS.!` and the other
`VS.unsafeIndex` --- **that pair ended with the parking of `gen-quotrem`
on 2026-08-28**, leaving the pin load-bearing for comparability alone, every
figure in this README having been taken at it. **And the module itself
is not what varies, which Run 17 settled and no run re-asks**: two builds of one
recipe back to back gave one `Main.o` by md5 WITHOUT `-fobject-determinism`,
and the control --- the previous run's recipe, twice --- gave one as well, where
two had been registered. So the flag is priced at nothing on this module
for REPRODUCIBILITY, having reproduced without it, and the run-to-run binary
differences this README has met are the store's and not this module's.
**It is not inert in the code it emits, which is the other question
and was answered the other way on 2026-09-11**: toggling it moves which loop
latches fuse, on this module and on both compilers --- seven of seven against
six of seven one way and the reverse the other --- which is [the open
list][open]'s GHC
[#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799) entry,
and is why a build compared across that flag is not comparing the same code.

`micro.cabal` builds at -O1, which is what a default `cabal build` of orthotope
takes and what the shipped file compiles under --- **the regime the figures
are read in** (ruled 2026-09-13, [the open list][open]); Runs 8 to 29 were read
under `-fspec-constr`, and the two series do not join. Other regimes
are command-line only, the flag landing after the cabal file's so the later `-O`
wins: `-fspec-constr` when testing the `SpecConstr` optimization effect, `-O2`
for the half of the scan-fusion refutation that inverts there (a `diag` at `-O2`
is what measures it). **The RTS line is the second thing the shipped setting
fixes, and since 2026-08-21 this suite shares it by decision: every horde-ad
test and benchmark and every process here runs at `-A32m`, and the area
is not to vary again.** `micro.cabal` bakes the whole line, `-A32m -I0 -T -M8G`,
the one every recorded recipe since Run 13 carried, so no recipe passes
`-with-rtsopts` any more, and a `+RTS` line that varies anything else repeats
it in full. The churn findings are why: the tax grows with the area, and `-A32m`
is their recommendation for this workload class.

**Those last four need no build and no pair**: `micro.cabal` compiles
with `-rtsopts`, so an already-built binary takes any RTS setting, and `-s`,
`-hT` and `-S` are available in a non-profiling build, so a question about
the collector is answered on binaries already timed. What `-s` cannot see
is the churn state: on the 27719 reproducer it prints
`0 MiB lost due to fragmentation` poisoned and clean alike and reads
productivity HIGHER poisoned, and `max_mem_in_use_bytes`, the heap peak every
run prints, is flat under the tax --- so a clean `-s` or an equal peak across
two processes says nothing about which state either is in, and a fixed-n victim
reading is what dates a state. The `-O2` and `-fspec-constr` lines are probes.
A run whose numbers are meant to be kept and written into this file
is a different undertaking, and has a procedure of its own: [Making a major
benchmark Run](#making-a-major-benchmark-run).


### Making a major benchmark Run

**FIRST, THE TWO COMMANDS THAT SPARE YOU MOST OF THIS CHAPTER.** The list you
owe prints alone, and the disk says what is already done, so neither is a thing
to reconstruct by reading:

    ./read-run.py --checklist pre|run|post   # a PREPARATION owes `pre` ALONE
    ./read-run.py --checklist readings       # the items steps name by number
    ./run-status.sh $R                       # what is done, off the artifacts

**Stop reading here and run them.** What follows is the three lists and,
at the chapter's end under *The reasons behind the three lists*, why each step
is what it is; a step that surprises you names its paragraph on a `why:` line.

    # READ THIS LIST AND START. The prose around these three lists is
    # reasons and restates no fact you need; a step that surprises you
    # names its paragraph on a `why:` line, which --check-doc holds to a
    # paragraph that is still there.
    # You are the preparation, and this list plus its `READ NOW` lines
    # is the whole of what you owe. Of the chapter's readings you owe 1
    # (this list alone), 3, 7 as 12a scopes it, 9 by the part a step
    # needs and 10 as step 2's draft prints it, and each is named at the
    # step whose work needs it. Reading 5 is owed only where
    # this preparation parks or drops an arm: step 7's --lint tells you,
    # refusing a property that names an untimed arm, and 12a says when to
    # read it. Nothing else in the chapter is owed,
    # and reading the executing session's half is the largest avoidable
    # spend here. The default form prints each step through its `why:`
    # line; `--full` adds the reasons under it.
    cd ~/r/orthotope/micro-regime3        # and re-set R, PREV and REGIME
    #      per call
    #      NN is one past the highest-numbered file in runs/, the run
    #      behind you. DO NOT MAKE `runs/$R.md` YET: post-run step 5
    #      makes it. Governing docs are this file and read-run.py's
    #      docstring, and CLAUDE.md beside this file says how far
    #      horde-ad's binds here
    #      why: every mode defaults to the newest run file.
    #      Every mode defaults to the newest file, and everything
    #      before post-run step 5 -- the evening's machine check, the tables
    #      read back -- wants the run behind you and would read this run's
    #      empty file instead. The disk is where the run number is written.
    R=runNN; PREV=runMM; REGIME=-fspec-constr   # an empty regime is a
    #      plain -O1 build and nothing downstream notices; that hazard is
    #      step 2's alone, REGIME reaching the build and nothing else.
    #      PREV is the run behind you, which the steps below read from --
    #      its note, its basis binary, its fills
    ./run-status.sh $R                    # 0. what is already done, off the
    #      artifacts and the repository rather than off this list, and it
    #      is not always nothing: a preparation can arrive to find 12a and
    #      12c taken, the registration having landed with the roster
    #      commits days before the pair.
    #      RUN IT AGAIN after the last edit to the note, which 12c repeats
    #      why: it reads the note as the drivers will.
    #      It is the only check that reads the note as the drivers
    #      will -- the machine lines through pair-halves.sh, the GATE
    #      block, the `<yours>` slots. On a copy whose `HALVES:` and
    #      `COMPARE:` lines were folded into the prose (measured
    #      2026-09-19) the readings part three ways: --note-check,
    #      --check-doc and --lint all PASS it, being predicates over
    #      prose; preflight refuses, exit 2 with no step line at all,
    #      which reads like a tooling fault rather than a note defect; and
    #      this names the cause, `2b NOT DONE ... has no 'HALVES:
    #      basis=<b> other=<o>' line`
    #   1. NOTHING NAMED FOR THIS RUN MAY EXIST YET, and step 0 above
    #      has already said so, as the first line of its pre-run block:
    #      `nothing named $R-* here` for a run about to be prepared, and
    #      a count of what it found otherwise, which is a run already
    #      under way or a leftover to clear and never a pair to adopt
    #  If anything for this run is already here, step 1 has caught a
    #      preparation that is not yours to redo, and what landed says
    #      which entry point it is: the run's own JSONs mean post-run
    #      step 0; a complete note whose GATE line reads NOT RUN
    #      means 13, which is the executing session's normal entry, with
    #      `./preflight.sh $R` re-running 4 to 10 in one call. Nothing
    #      older than this run's own preparation is ever inherited
    #      why: --para 'A preparation already spent'
    #      Rebuilding now would orphan the binaries the run's JSONs are
    #      provenanced to
    #   2. BUILD BOTH HALVES -- unconditional, from the note's own
    #      recipe. READ NOW, before any of this step: item 3, the
    #      registration the compares-against prose points at; item 10,
    #      the previous run's note, is read as the draft below prints it.
    #      Item 9, read-run.py's docstring, is read by part when a step
    #      needs it: `--doc modes` for a mode, `--doc definitions` for
    #      what a figure means.
    #      Go back to these the moment a figure surprises you, a gate
    #      refuses a leg, or the roster brings an arm whose relation to
    #      the forcing pass is new. Reading 3 is one call and it wants its
    #      table: `./read-run.py --section 'What the next run compares
    #      against' --with-tables 1`, the first table being the two-column
    #      one the reading list asks for. For a `--repeat` pair it is
    #      less: the registration by `./read-run.py --para 'What Run <N>
    #      is built to answer'` and the pair's earlier readings by
    #      `./read-run.py --record NAME`, the series it is read in, which
    #      `--record` alone lists. `--section` and `--para` search
    #      README and the newest run file both, so neither wants a
    #      `--run-doc`. It is a step and a session's to run, and the note
    #      is the part written by hand.
    #      The halves launch from disk, `./$R-<half>`, hugebin/ being
    #      suspended -- ruled 2026-09-19 -- so a row reading `./` is the
    #      expected reading. Preflight's 10f, a step of preflight.sh run at
    #      4-10 below, refuses a mount nobody asked for: it FAILs where the
    #      path half-bin.sh returns for a half is under `hugebin/` and
    #      PLACEMENT is unset.
    #      The mount is an emergency measure: a run whose question is the
    #      placement term raises it by hand (`mkdir -p hugebin &&
    #      mount hugebin`, root's, the fstab line in half-bin.sh's
    #      header), runs preflight with PLACEMENT=1, says in its note that
    #      it did and on whose word, and takes run-list step 16a with it,
    #      the mount writable or 16a leaves the instance untested. Every
    #      other run leaves it unmounted.
    #      Write the note first, from pair-note-template.txt. What `first`
    #      means is the recipe block, which is the part the build reads:
    #      write that, build the halves on it, and write the rest of the
    #      prose under the build and the preflight, which are minutes each.
    #      And the note is never reflowed, by any tool. Break a long line
    #      by hand where one bothers you, or leave it long.
    #      One command does the reading and the copying, redirected to
    #      $R-pair.txt in an unsandboxed call:
    #          ./read-run.py --note $PREV-pair.txt --draft $R \
    #                        --halves <basis>,<other> [--repeat]
    #      `--repeat` is for the previous pair's own recipes built again:
    #      its [PAIR'S] blocks come whole rather than as models, and a
    #      slot at the head names each input that moved since that build.
    #      It is the whole note: each `[SAME]` block from the template with
    #      this pair's names and the previous LAUNCH and RIDERS values put
    #      in, each `[PAIR'S]` block the previous note's under a `<yours>`
    #      line as a model to rewrite, the handover and the fill-in rows
    #      empty. Its header names the blocks it took from the template,
    #      any paragraph dropped with one, and every carried block that
    #      needs re-reading with the reason each is suspect. So the note is
    #      that file filled in, not three files assembled, and the
    #      previous note needs no reading of its own.
    #      What the pair varies is settled in the registration, `What Run
    #      N is built to answer` in the open list, which *What the next
    #      run compares against* points at and which carries the recipes;
    #      the draft's models are what the previous run built.
    #      Where the request differs from that section, the request wins,
    #      and the section and the open list's task recording the
    #      decision are amended first, in a commit of their own.
    #      Every build wants -fforce-recomp and a fresh --builddir; the
    #      recipe spells the regime out rather than interpolating $REGIME.
    #      $REGIME is for the ad-hoc call, and where one is written
    #      --ghc-options="$REGIME" stays quoted. Build the halves back to
    #      back with nothing touched between, which is one call: build,
    #      copy, build, copy. Keep both executables and delete each
    #      --builddir once its binary is copied out; the pair's variable is
    #      read back out of each by the note's VARIABLE-CHECK line (2b),
    #      which preflight runs as 9b.
    #      Then the note's fill-in block: the Main.hs and align-as.py
    #      commits, the two compilers, the md5s, .text, the fills. Do not
    #      transcribe it -- `--fill-in`, which the preflight line at steps
    #      4 to 10 carries, derives every one of those rows from what
    #      those steps just read and prints the block to paste, marking
    #      `<yours>` the rows this call cannot give -- the sweeps, the
    #      roster pass, repetition, and 8c and 8d, which `--corpus
    #      --fill-in` prints when it has run them. Step 10 reads the block
    #      back.
    #      And the fills are read before anything else changes, at 2d
    #      below; 2a and 2b sit between and change neither binary.
    #      Build both, always -- the both-halves-are-built-anew ruling,
    #      whatever the source and the md5 say. On a repetition the md5 is
    #      one-sided, and an md5 that does not reproduce is not a stop:
    #      the note records the observation, the write-up carries what
    #      moved. What the recorded inputs do not cover is the dependency
    #      store relinked at unchanged versions, which the two binaries'
    #      ABI hashes show --
    #      the `strings` line is in the paragraph this why names
    #      why: --para 'three rules are what they are'
    #      Item 9 is here and not at step 7 because its definitions --
    #      corr, net, time, worst, and which rows have no corrected time
    #      and read `--`, which is stated there and in no list -- are what
    #      this note's prose and every `predict:` span at 12a are written
    #      against. Without `--with-tables` the section mode prints the
    #      prose and says only afterwards that a table was withheld, which
    #      is the section paid for twice.
    #      The mount failed to come up at the reboot of 2026-09-19. WHY it
    #      cannot come up, and the fstab line that would, are
    #      half-bin.sh's header and are not repeated here.
    #      What it costs, stated here so no run re-derives it: a code
    #      page sits at the page cache's 4 KiB draw and not at its
    #      layout's offset in a 2 MiB frame, which the placement section
    #      prices at 15 percent on one arm of Run 33's basis. That term
    #      is back in both halves, so it bears on cross-run absolutes and
    #      not on a pair's own two columns. 10f exists so that a
    #      mount raised between runs cannot take the placement term back in
    #      silence.
    #      There is no builder, every pair being two shims typed out, so
    #      the note comes first: its recipes come from the registration,
    #      the one place that declares them, and the template is what
    #      says what a note owes. A preparation that writes the whole note
    #      before building holds the machine idle while it writes.
    #      `wrap80` is for Markdown and `par` for comment blocks, and this
    #      file is plain text carrying machine-read lines -- `HALVES:`,
    #      `COMPARE:`, `LAUNCH:`, `RIDERS:`, `RERUN:`, `VARIABLE-CHECK:`.
    #      `par` over its
    #      long paragraphs once folded `HALVES:` and `COMPARE:` into the
    #      prose: the note still READ correctly, and pair-halves.sh could
    #      not find the halves at all.
    #      A blocked redirect runs nothing at all, so the name carries $R:
    #      a file the previous preparation left cannot then read back as
    #      this one's output. The first command withholds the handover and
    #      the gate, spent with that run, and the `[SAME]` blocks, which
    #      the second carries over, saying how much; on a repetition what
    #      those blocks change is run numbers, and the second's header is
    #      what a preparation actually uses. Hand-copying the `[SAME]`
    #      blocks is what the second removes.
    #      The registration is the one declaration site (ruled
    #      2026-09-19); a session executing the list top to bottom arrives
    #      here with neither it nor the previous note read.
    #      Cabal answers "Up to date" for a -pgma or an environment
    #      change; every recorded note spells the regime out. A call
    #      apiece is an invitation to put something between the builds,
    #      and the rule is that nothing goes there. About twenty seconds
    #      each here, the dependencies being in the store and only the
    #      local package recompiled. A hand reads the wrong column, `size
    #      -A`'s SECOND field being the load address and not .text.
    cat $R-pair.txt                       # 2a. the note, quoted by steps
    #      here and in the run list alike -- the halves' roles, the
    #      md5s, the commit, the gate line, and any environment its LAUNCH
    #      line puts in front of a command. It is written at step 2,
    #      from pair-note-template.txt and before either binary exists;
    #      here it is read, and the steps below quote it
    #      BASIS/OTHER come from its HALVES: line, never from a half's
    #      name, and every script reads them there (2b).
    #      The basis runs second, and both halves run the classes
    #      why: --para 'Which two halves a pair has'
    #      At run-list step 13 the executing session reads the [EXEC]
    #      blocks and skims the rest, those being the ones it acts on
    #      rather than the ones the preparation wrote
    #  2b. the note's machine lines, written with it and read by
    #      the scripts that take a run: `HALVES: basis=<b> other=<o>`,
    #      which pair-halves.sh reads for all of them and holds the
    #      environment to; `COMPARE: run<N>`, the earlier run
    #      the evening's machine check, `--movement`, `--bridge` and
    #      `--half-movers` read against unless told otherwise, which
    #      `--draft` sets to $PREV and a ruling may change; `LAUNCH:
    #      <NAME=value ...>` or `LAUNCH: none`; and `RIDERS: clean [sat]`
    #      or `RIDERS: none`, the two run-evening.sh reads; `RERUN:`,
    #      which post-run step 3 reads; and `VARIABLE-CHECK:`, which
    #      preflight runs as 9b -- `regime basis|other`, `run CMD => ERE`
    #      or `none REASON`, --note-check refusing a note without it. An
    #      older note's `scripts set` row is not copied forward
    #      A HALF'S TAG IS ONE TOKEN, `[A-Za-z0-9_]`. Where a declared tag
    #      falls outside that set, the declaration and the registration
    #      are renamed first, in a commit of their own
    #      why: --para 'Which two halves a pair has'
    #      So nothing is set in any script. pair-halves.sh refuses any
    #      other tag, as `--draft` does at step 2
    ../../horde-ad/tools/loop-offsets.py --delta $PREV-<PREV's basis> $R-<basis>   # 2d. the
    #      fills against the previous build of this recipe, taken the
    #      moment both binaries exist and before anything else changes.
    #      There is no 2c: that is run-status.sh's label for a finished
    #      note.
    #      TAKE IT EVERY TIME: it is owed wherever a timed arm brings a new
    #      function, which only 6c shows, later, and it costs nothing where
    #      it is not. Read the previous run's basis off its own note's
    #      HALVES line, which is where preflight's fill-in block reads it.
    #      why: a rebuild retires the comparison.
    #      A rebuild retires it, and the fills read here are the
    #      pinning claim's only reading.
    #      The two tags are not always one: a tag names what a half is, so
    #      a run that changes the variable renames the basis while the
    #      recipe stands.
    #      It is against the previous build of this recipe and not against
    #      a note's transcription of it -- offsets preserved or not,
    #      addresses surviving to the byte, and the displacement set, which
    #      is what the README's readings turn on. preflight's own step 10
    #      reads the fills AGAIN and does not make this comparison -- it
    #      says so on the line -- so taking it here is not a duplicate.
    #      What the claim covers, and how Runs 20 and 21 killed its strong
    #      form, are in the prose.
    #  2e. the priors 12a writes against, taken NOW, while the box is quiet
    #      and before preflight and the sweeps load it: `probe-stalls.sh`
    #      on $R-<basis>, `EVENTS=instructions:u,cycles:u`, at the counts
    #      N the previous run's sweeps name, TWICE, each over every timed
    #      arm on the main set and over the classes holding an arm
    #      `./registration-drift.py $R --since $PREV` names as reached,
    #      and once with `ALLOC=1` over those arms -- the items are 12a's
    #      and not written yet, so the sweep names none of them.
    #      Quiet means reads and text edits beside it and nothing else: no
    #      build and no checker.
    #      And once 11 and 12 have printed their verdicts, before
    #      `--corpus`, on the quiet box again: TWO MORE SWEEPS of the arms
    #      whose cycles an item quotes. A cycle figure is a prior only
    #      where all four agree; the rest are quoted as the reader's
    #      spread. Read them with `./read-run.py $PREV-<basis>-main.json
    #      --counts SWEEP --pair A B`, adding `--event cycles:u` for a
    #      cycle prior and `--event bytes` on the ALLOC sweep, a countdiff
    #      span's figure with `--counts SWEEP --countdiff A B`, and a sweep
    #      against the previous run's counts with `--counts-over NEW OLD`
    #      why: a load the box carries is counted in its cycles.
    #      Run 42 took them under the roster pass, and its two sweeps'
    #      cycles parted by up to four times on one cell. Run 45's two,
    #      and two more on the idle box, parted alike: by up to eleven
    #      points on a main-set net-cycle geomean near 1 between two fill
    #      arms. Quiet alone does not make two sweeps agree at N=50.
    #   3. retired 2026-09-25: the two md5s and the Main.hs and shim
    #      commits are rows preflight's `--fill-in` derives at 4-10, so
    #      they owe no call of their own. The number stays unused, so that
    #      no pointer to it lands on another step
    #  a `git log -- :/micro-regime3/FILE` pathspec resolves from the repo
    #  root, so it answers the same from anywhere; a bare `-- Main.hs` run
    #  from the root prints nothing and exits 0, which reads exactly like
    #  an unmoved source
    #  and `git show HEAD:FILE` resolves from the root too, which is the
    #  same rule read the other way and is the one that answers WRONG
    #  rather than empty: from here `git show HEAD:README.md` hands back
    #  orthotope's top-level README, a different document of a few hundred
    #  lines, and says nothing. `git show HEAD:./README.md` is the form
    #  that means this directory's
    ./preflight.sh $R --no-corpus --fill-in   # 4-10 LESS 8c AND 8d, which
    #      `--corpus` takes at their own line below, once 11 and 12 have
    #      landed. A session RE-ENTERING a spent preparation wants the
    #      plain `./preflight.sh $R`, which is all of it and nothing to
    #      sequence
    #      AND 10c, 10d AND 10e ARE EXPECTED TO FAIL HERE, the note being
    #      half written when this runs. Read them, do not chase them;
    #      `./preflight.sh $R --note` re-runs those three and 8 in seconds
    #      once the note is finished, and that is the reading that counts
    #      4-10 in one call: PASS or FAIL per step with what it read, the
    #      exit status the verdict. It runs 10a and 10b too, straight
    #      after 4,5 and on their astride count alone, the figures staying
    #      the note's, and 9b by the note's VARIABLE-CHECK line -- so what
    #      it does not run is 6c, 11 and 12, whose own lines follow, nor 8c
    #      and 8d under --no-corpus; its fill-in block quotes 2d's and 6c's
    #      readings without judging them. The other steps below are what
    #      it runs and what to reach for when one FAILs
    #      why: 8c and 8d must not overlap 11 and 12.
    #      8c and 8d read every run JSON on disk and so must not run
    #      while 11 or 12 is writing one.
    #      Deferring them is what lets the roster pass -- the longest step
    #      of this half -- start minutes sooner. One call, so none is
    #      skipped by being forgotten.
    #      10c, 10d and 10e read the note's paths, its recipes against the
    #      HALVES line and its carried prose, and a draft's carried blocks
    #      still name the run before last. Its own 10c, the note's paths,
    #      runs third, a fresh note being the likeliest thing to fail, and
    #      its 10d holds the note's recipes to its HALVES line.
    ./$R-<basis> check > /tmp/claude-1000/a.log 2>&1   # 4. every shape agrees
    ./$R-<other> check > /tmp/claude-1000/b.log 2>&1   # 5. and the other half
    cmp /tmp/claude-1000/a.log /tmp/claude-1000/b.log #  byte-identical, or STOP
    #  What is not a stop, and it is the one reading this cmp needs: a
    #      difference confined to an instrument's own measured output,
    #      with every verdict word agreeing and both halves exiting 0, is
    #      a finding about the instrument and not about the pair. Say what
    #      it was, fix the instrument, rebuild both halves and re-run
    #      this -- do not carry it. Any other difference is the stop
    #      this line says it is
    #      Scratch goes under /tmp/claude-1000, the one directory both
    #      seats write, and never to a $R-*.log here.
    #      And `check` is spent here: nothing later wants it again
    #      why: halves that compute differently leave nothing to compare.
    #      A blocked redirect runs nothing at all; a $R-*.log here makes
    #      run-major.sh refuse hours later, and $TMPDIR is /tmp
    #      unsandboxed and /tmp/claude-1000 sandboxed.
    #      `check` runs over every shape and class view, the retired ones
    #      included. What holds the retired NAMES to the lists is Main.hs's
    #      `retiredKnown` and `retiredShapesKnown`, asserted in `main`
    #      and so exercised by every mode rather than by this one --
    #      which is that file's own note beside them, and not a thing
    #      `check` is needed for
    ./$R-<basis> --list 2>/dev/null | wc -l    # 6. roster size, then the
    diff <(./$R-<basis> --list 2>/dev/null) <(./$R-<other> --list 2>/dev/null)
    #      two halves' listings: identical is what one source built twice
    #      looks like, and the pair note asks for that half of it. No pair
    #      here varies the roster
    #      why: a roster difference breaks four steps.
    #      A pair whose halves differ in the ROSTER would break this
    #      and three more of these steps -- preflight 4,5 cmps the two
    #      `check` outputs, and run-major.sh and smoke-sweep.sh hold every
    #      half to the BASIS's bench count
    #  6b. and the gate's own selection, which preflight reads by asking
    #      the script that will run it: `./run-gate.sh $R --show` prints
    #      SEL's globs and the count it derives, spends nothing, and
    #      refuses where a glob names an arm the roster has parked. That
    #      is the note's `gate arms` line derived, never read off the
    #      previous note
    ./roster-delta.py $PREV-<PREV's basis> $R-<basis>   # 6c. what the
    #      roster change was -- and the first tag is the previous run's,
    #      as at 2d. Off the two binaries: benches, arms in and out,
    #      whether the survivors kept their order, main-set shapes in and
    #      out, the class views per class, and every shape or view whose
    #      geometry moved under an unchanged name, off `check`, a minute a
    #      binary. ITS ARMS IN AND ITS PER-CLASS
    #      TALLY ARE WHAT STEP 12 NAMES ITS CLASSES FROM -- every class where
    #      an arm came in, else each class whose count moved -- so read it
    #      here and carry the answer down
    #      why: this run's basis tag may name no binary $PREV built.
    #      It is what the note's roster block and Provenance's delta
    #      bullet both state in prose.
    ./read-run.py --lint                  # 7. roster and shape annotations,
    #      the properties, and the open registration: every arm it
    #      names must be timed and every `task N` it defers to must
    #      resolve. What that does NOT ask is whether the task still
    #      carries a prediction, a pointer resolving while the sentence
    #      around it is false. That half is 12b's, a reading, and this is
    #      why 12b is not optional
    #      why: --para 'Steps 7 and 8 are the whole'
    ./read-run.py --check-doc --quiet     # 8. anchors, paths, widths, sweeps
    #      7+8 are the whole document check here; no other repo's checkers,
    #      now or at post-run step 7. THEY ARE OWED TWICE: here, and again
    #      after 12a, which is where the registration they check is
    #      written. The second is the verdict. Exit code is the verdict:
    #      `note:` lines are write-up material (6e's --worklists prints
    #      them), and a wrap FAIL is a hand-wrapped paragraph, never a
    #      long one
    #      A `FAIL: BLOCKED:` here is a root the wrapper did not mount,
    #      usually ../../horde-ad, and it means the path check did not
    #      happen rather than that it failed. Get the checkout
    #      mounted and rerun, or run with it blocked and say so in the
    #      write-up -- the one thing not available is reading it as a pass
    #      why: --para 'What the `note:` lines ARE'
    #      A clean pass here says nothing about text that does not exist
    #      yet. A name that is simply wrong cannot be told from one
    #      nothing searched
    check-all .
    #      8b. the static checks, checks.py's steps whole: the records
    #      validated, the defect families over the Python source here,
    #      pyflakes over it and shellcheck over the shell drivers, the
    #      executable bits and the bang shapes, a linter off PATH failing
    #      its step by name; ten seconds on 2026-10-04.
    #      The rest of the tree's check, the properties over every run,
    #      the cases both ways and the mutants, is `check-all
    #      checks-deep.py`, which is 8c to 8e, run once a preparation
    ./properties.py                       # 8c. its properties, over every
    #      run JSON here -- and THIS BARE INVOCATION IS THE ONLY SWEEP THAT
    #      READS THEM ALL. The reader's stderr is withheld and counted by
    #      kind, a kind with a count of one being the thing to read, and
    #      `--warnings` restores it. It is checks-deep.py's first step
    #      why: a property that fails only on an older run is caught here.
    #      Nothing else catches such a property, which is also why what an
    #      old run's artifacts still buy the checks is this step.
    #  8d. every defect these scripts have had, planted again and refused
    #      again, in both directions -- `defect-run.py .` and its
    #      `--audit`, which replays each case against the code before its
    #      own fix -- whatever changed since the last run, a data change
    #      owing the audit as much as a code change. Not a call of your
    #      own: checks-deep.py's two case steps, which `--corpus` below
    #      runs. 8c to 8e want an unsandboxed seat, and they run alone
    #  8e. every mutant, `selftest-mutants.py .`, checks-deep.py's last
    #      step: an edit can move a mutant's anchor, and 94a3cfd lost one
    #      unseen until a write-up
    #  8c TO 8e COME AFTER 11 AND 12, at the `--corpus` line under 12,
    #      which says when
    #      why: --para 'What the script-check steps'
    #      Until 2026-10-04 8d ran only the cases of the scripts changed
    #      since the last run, `check-all .` running every case after an
    #      edit.
    #      8c and 8d write `zz-` fixtures here and remove them, and a file
    #      created anywhere in the tree while they run -- a log, a scratch
    #      redirect, an edit committed or not -- makes the cases report
    #      PARTIAL and settle nothing.
    #      The conflict runs both ways: these two read every run JSON on
    #      disk, and 11 and 12 write them, so either order of overlap
    #      fails. A leg caught half written fails
    #      prop_selftest_over_the_corpus with a traceback, on a file no
    #      run produced and reading exactly like a defect. 12c is what
    #      must not overlap -- a commit while these two run reads as a
    #      case that changed the tree
    ./$R-<basis> diag                     # 9. the regime, in the binary:
    #      one row, baseOffsetsScan against baseOffsetsMut on vgg-14-c512,
    #      equal to three figures under SpecConstr and ten times apart at
    #      plain -O1. MATCH THE TWO ROW LABELS, never the position
    #      why: --para 'Then confirm the regime'
    #      diag prints the whole baseOffsets* family per shape, and the
    #      rows above these two are another question's
    #  9b. and the pair's own variable, by the note's VARIABLE-CHECK
    #      line, which preflight runs at 4-10 and --note-check holds to one
    #      of its three forms (2b)
    #      why: diag answers for the regime and for nothing else
    ../../horde-ad/tools/loop-offsets.py $R-<other> $R-<basis>    # 10. fills, kept with the run:
    ../../horde-ad/tools/loop-offsets.py --library $R-<basis> $R-<other>   #     the eye's reading
    #      is the same fills at the same addresses in both, and only
    #      `--library` prints a figure -- read it against the band for
    #      this pair's recipes: near-total for one source padded to one
    #      size and phase, a tenth to a quarter where a shim or a compiler
    #      varies, lower still where the pads are placed differently. Never
    #      against a fixed line, and not against a note's nm-based figure,
    #      which is another number
    #      why: --para 'can differ by more than Main'
    ../../horde-ad/tools/loop-offsets.py --survey $R-<basis>       # 10a. one leg per half,
    ../../horde-ad/tools/loop-offsets.py --survey $R-<other>       # 10b. both owed, both new,
    #      and the answer goes in the note.
    #      Each leg prints three counts, the third being exit
    #      spans astride, the span as align-as.py costs it under
    #      LOOP_EXITSPAN. On a half built with that switch it is 0, or
    #      the recipe lacks the switch, the shim regressed, or the survey
    #      read a table as a loop: dump the
    #      head's bytes first, and stop before 11 for the other two; on a
    #      half built without it, a figure for the note
    #      why: the answer is the binary's.
    #      It is the binary's, not the reading session's. What it
    #      means is below, at the pad.
    ./smoke-sweep.sh $R                   # 11. the smoke sweep, STARTED NOW
    ./smoke-l1.sh $R [CLASS ...]          #     in the background with 12 where
    #      6c says it is owed, and 12a and 12b taken under
    #      them.
    #      A repair to read-run.py or preflight.sh lands before step 11 or
    #      waits for it. What the pass does not hold -- pair-halves.sh,
    #      read once at its start, and README -- is editable under it.
    #      A repair to the reader itself need not wait idle: `cp
    #      read-run.py log-work-read-run.py`, edit the copy, test it
    #      against real JSONs, and apply it when the pass prints its
    #      verdict. Delete the copy once it is applied: `check-all .`,
    #      which is 8b, lints every *.py here
    #      And not before preflight's 4,5, nor before 10a and 10b.
    #      The wait is on the log lines and not on the call: launch these
    #      two the moment preflight's log shows `4,5  PASS` with `10a` and
    #      `10b` PASS under it, three adjacent lines and minutes before
    #      that call returns.
    #      Read those lines by appending `command grep -cE '(4,5|10a|10b)
    #      +PASS'` of the log to the calls you are making anyway, and
    #      expect 3 -- never a `tail` window. The log writes every verdict
    #      indented by two spaces, so a pattern anchored at the start of a
    #      line never fires
    #      IN THE BACKGROUND, THROUGH THE HARNESS'S OWN MODE, NEVER A
    #      TYPED `&`, AND WITH NO WAITER SET.
    #      A backgrounded call's status is its last command's: never end
    #      one with `; echo "exit $?"`. End the call with the command
    #      itself, or read the status in the task output rather than in
    #      the redirected log alone
    #      why: --para 'And one more, nearly free'
    #      They are the only machine time in this half, neither wants a
    #      quiet box, and the registration is the long hand step, so the
    #      half is the length of its longest step and not the sum.
    #      These two lock the reader for an hour, which decides the order
    #      of everything else this half does: smoke-l1.sh invokes
    #      read-run.py once per leg, so an edit to the reader between legs
    #      is read by the rest of the pass, and preflight.sh cannot be
    #      edited while it runs at all, bash re-reading a running script by
    #      byte offset. The pass hands each leg a JSON, so it never opens
    #      README. 8c and 8d's own line below carries the other half of
    #      the sequencing. The sweep holds each process to the arm count
    #      `--list` gives for that shape.
    #      Since 2026-09-19 10a and 10b are the two verdicts printed
    #      straight after 4,5, so the ordering costs nothing and reads as
    #      none: a nonzero astride count stops before this pass by 10a's
    #      own line, so a pass launched in front of it spends its hour on
    #      binaries a stop may retire. Those two `check` runs are
    #      nearly all of a preflight and sit in front of this pass, so
    #      overlapping them buys minutes -- and 4,5 is the step whose
    #      failure retires the binaries, so a pass started early spends
    #      its hour on binaries that no longer exist. What is taken is
    #      the parallelism inside 4,5: the two halves check concurrently,
    #      which costs nothing and risks nothing, the assertion being
    #      that their logs agree. The two surveys were hoisted to sit
    #      beside 4,5 for exactly this, the astride stop above being
    #      unreadable until they had run.
    #      A `tail` window misses the lines where several land between two
    #      polls; the note's own writing is a dozen calls and each carries
    #      the poll for nothing.
    #      The background mechanism is horde-ad's portable notes, under
    #      the session facts, and is not restated here; the command lines
    #      above carry no `&` for it. With `; echo "exit $?"` last, what
    #      the harness announces is the echo's 0 for a step that exited 2,
    #      an aborted preflight reading as a clean one
    #  12. the roster pass, owed only
    #      if `--list` changed membership AND the pair note records none
    #      -- it belongs to the pair as the gate does, so grep the note
    #      first, and read the membership off 6c above rather than off
    #      the roster delta under Provenance. The main set plus a leg per
    #      class named,
    #      AND NAME EVERY CLASS where the roster gained an arm, with
    #      `ARMS=` naming the arms 6c counts in and a control beside them:
    #      each class leg then takes those, `list` and the two `sum-only`
    #      arms, and the main leg the whole roster, which is then most
    #      of the pass's cost, about a quarter of the hour the whole roster
    #      over every class takes (ruled 2026-09-26).
    #      Where the roster gained no arm, name `scaled` plus each class
    #      whose count 6c's tally moved, over the whole roster, the
    #      script's bare default being `scaled` alone.
    #      Artifacts are
    #      `smoke-l1-$R-*`, never `$R-*` (smoke-l1.sh's header, the
    #      namespace), and a previous attempt's are refused. A pass you
    #      stopped is a previous attempt, so clear its artifacts before
    #      relaunching, by `smoke-l1-$R*` and not `smoke-l1-$R-*`.
    #      And a stopped leg leaves a half-written JSON: clear it before
    #      any check runs, not before the next pass. Record the outcome on
    #      an `L1 ROSTER PASS:` line
    #  11 and 12 here, and run-list step 14, all belong to the
    #      pair: on passing, write each into $R-pair.txt
    #  12 is the long one: what is read when each ends is its last `===`
    #      line, the contention in the elapsed times it records being a sanity
    #      reading and not a measurement.
    #      The turn-end hold is set at the first wait and not here, which
    #      is step 2's build (~/.claude/rules/turn-end-hold.md), on each
    #      repository the run edits, named: `wrap-restore --hold
    #      ~/r/orthotope`, a bare --hold holding the working directory's,
    #      which for a session rooted in horde-ad is not this one. Clear it
    #      at 12c. And wait on nothing: launched as step 11 says you are
    #      woken. A `tail` between legs shows nothing
    #      why: --para 'After a roster change'
    #      A timed arm lands on every class but `big`, whose arms
    #      `classArms` names, so the classes whose VIEWS moved are not
    #      the ones at risk. The pass is the longest thing this half
    #      spends and it fills one row.
    #      The driver's own log is `smoke-l1-$R.log`, with no hyphen, so
    #      the obvious glob leaves exactly the one file the refusal reads
    #      and the relaunch dies again on it. Both halves of that were met
    #      on 2026-09-20.
    #      A half-written JSON is not merely clutter: 8c reads every run
    #      JSON here, so a truncated one fails
    #      prop_selftest_over_the_corpus with a traceback and takes the
    #      cases and the mutants down with it, three steps red for one
    #      file and no message naming it.
    #      Unwritten into the note, the next session repays the hour. 12
    #      is about three quarters of an hour on the BASIS half alone,
    #      where 11 is minutes.
    #      Every wait ends a turn and the Stop hook rewraps the documents
    #      at each, and another session's turn end rewraps them too, wait
    #      or not, so the hold pays from the first backgrounded thing
    #      rather than from the first edit under these sweeps. Set that
    #      early it costs nothing and covers the whole half; set here it
    #      covers the registration and leaves the build's own waits
    #      uncovered. A waiter that greps a process list matches ITS OWN
    #      command line and never returns -- `pgrep -f`, `pkill -f` and
    #      `ps -eo args | grep` alike. Each driver prints a leg when that
    #      leg ENDS, so its output file is unchanged for the whole of a
    #      leg while the leg's JSON grows under it, which reads like
    #      progress and is not
    ./preflight.sh $R --corpus --fill-in  # 8c to 8e, deferred to here,
    #      `check-all checks-deep.py` run alone, printing their fill-in
    #      row: once 11 has printed `sweep
    #      clean` and 12, where owed, `pass clean`, nothing is writing a
    #      JSON, and BEFORE 12c, the commit -- 12a and 12b under the
    #      sweeps, then 2e's two more cycle sweeps, then this, then 12c.
    #      And AFTER THE PREPARATION'S LAST SCRIPT EDIT: repairs met on
    #      the way land before it, an edit after it owing it again. Their
    #      verdicts are the only ones this half owes that were not read
    #      above
    #  12a. write the registration, which is this half's largest product
    #      -- as ONE paragraph, which post-run step 5 moves whole into the
    #      run file with `--move-registration`: what this run is built to
    #      answer, as an `OPEN` entry of the open list led `What Run N is
    #      built to answer, registered before it runs`, numbered
    #      questions with a prediction and a kill condition each, and a
    #      `predict:` span where the quantity is one the reader computes,
    #      its grammar being `./read-run.py --doc spans`, written in
    #      --compare's orientation, the basis over the control
    #      (`predict: cross list 1.0 within 0.5% on main both` predicts
    #      `list` level between the halves to half a point on the main
    #      set) -- and every span carries its scope, `on POP,...`
    #      and one of `basis`, `control` or `both`, which `--predictions`
    #      reads it on and nowhere else; a clause no kind states is read
    #      by a script committed with the registration and named in it as
    #      `` `script: NAME` ``, and `--lint` refuses an item carrying no
    #      span, no script and no deferral to a task, or a span without
    #      its scope. A band set from a probe quotes that probe's own
    #      spread beside it -- and the probe JSONs already on disk are read
    #      for every pair registered.
    #      Each item names the mode or the file its prior came off, in the
    #      item and not once at the head for all of them: `--lint` refuses
    #      an item quoting a figure and naming neither, a null span at 1.0
    #      quoting nothing and being exempt.
    #      And a figure off a probe build names a file that holds it, in the
    #      prose as in a span: the build's log, the shim's report, the perf
    #      output, kept on disk beside the probe. A commit message or a
    #      docstring is prose and not an artifact, and a figure only prose
    #      holds is one 12b cannot re-derive.
    #      What an item that names none means, and how to ask every
    #      population at once, is one section and not repeated here --
    #      its title, whole, for a grep or a --section:
    #      Which population answers a question, and how to ask all of them
    #      No verdict word in the entry -- HELD, KILLED, SPLIT and their
    #      kin.
    #      READ NOW: item 7, scoped to the open entries naming an arm the
    #      line below reaches -- its arm-by-arm list of what each commit
    #      since $PREV's build touched is the reading of the source -- and
    #      item 5 where this preparation parks or drops an arm. That
    #      reading is a carrier agent's, as 12b's re-derivation is: brief
    #      one carrier with the list, for the entries this run could
    #      answer, one line each with the file each figure came off and
    #      nothing on the rest; the previous registration's pre-run form
    #      out of git, verbatim; and the probe files newer than $PREV's
    #      run file, one line each.
    #      It goes in the open list and not in the note, which names it:
    #      immediately above the previous run's `ANSWERED` registration
    #      entry. And the previous run file's `What the next run compares
    #      against` gains a sentence pointing at it as `[registered
    #      <date>][open]`, which --lint refuses the registration without.
    #      The form is the previous run's, in that run's own file. EVERY
    #      FIGURE IT QUOTES IS DERIVED FROM THE ARTIFACT, which 12b reads
    #      back
    #      why: the verdicts are then read mechanically.
    #      Post-run step 5 reads its verdict off `--predictions` and
    #      not off a session's reading of the tables.
    #      A collective claim of provenance is checked against no item, as
    #      Run 38's registration showed, calling a figure an A/A floor
    #      that another mode had produced.
    #      What `--lint` enforces is a floor and not the tie: it asks that
    #      the item name SOME mode or file, not that the figure came off
    #      the one named, so an item misattributing its figure would
    #      satisfy it. Tying a figure to its mode is 12b's reading, and
    #      nothing mechanical here does it.
    #      --check-doc reads a verdict word as an item already
    #      adjudicated.
    #      Every live entry is a paragraph, so a session reading them
    #      itself carries tens of
    #      thousands of tokens of prose for a handful of claims.
    #      Two copies of a registration is one copy that goes stale.
    ./registration-drift.py $R --since $PREV   # 12a's scope for item 7
    ./read-run.py --para '<a lead you just wrote>'   # 12b. READ BACK
    #      WHAT THIS HALF WROTE: re-derive every figure the note and the
    #      registration quote FROM THE FILE IT CAME FROM, never from the
    #      sentence beside it, and then read both back end to end. It is
    #      not a substitute for post-run step 6b's independent reader
    #      and read what the source did after the registration:
    #      `./registration-drift.py $R` lists each commit to Main.hs
    #      between the registration's and the build's, with the
    #      definitions it touched, exiting 1 where there is any. Read each
    #      against the arms the spans name
    #      and `--lint` prints every span as `--predictions` will compare
    #      it, under the registration it reads -- the mode, the two
    #      operands and their orientation, the key, the half: read each
    #      line against the sentence beside its span.
    #      Three of those errors are a machine's, and preflight runs
    #      them as 10e: `./read-run.py --note-check $R-pair.txt`. It does
    #      not read a figure, so the re-derivation below is owed whole
    #      and a `cross` prior on a `-sum` arm is read by `--compare`, in
    #      a block of its own under the table, on raw `slope` and never
    #      in the table's own column
    #      and the stronger reading of a quoted prior is `--predictions`
    #      over the JSONs of the run that quoted it.
    #      Locate by phrase, not by coordinate: this is what `--para`
    #      is, never a `grep -n` for a line number.
    #      And the re-derivation is a carrier agent's -- and the artifacts
    #      it will read are confirmed on disk before it is briefed.
    #      And when it is done, `./run-status.sh $R` reads `2c done: no
    #      <yours> slot left`, which is the one check that says the note
    #      is finished rather than merely written
    ./read-run.py $R --carried --others <RUN>-*-main.json <RUN>-*-runs.json
    #      And this is the mechanical half of the registration's figures,
    #      as --figures is of the note's. It
    #      derives each `pair A B` span on the runs given and names the
    #      item where nothing it quotes matches anything its own span
    #      produces.
    #      $R is named and not read.
    #      One JSON per population the items are read on, both halves. It
    #      is a warning and never a verdict, so what it hands back is a
    #      shortlist to read, and the reading is still 12b's
    #      And <RUN> is the run the item names, which is not always $PREV
    #  and `./read-run.py $R --carry-over` is that comparison, item by
    #      item against the previous registration's pre-run form, which
    #      is in git and not in the run file. It names the words that
    #      moved and judges none: which changes were meant is the
    #      reading's
    #  `./preflight.sh $R --figures` is the mechanical half of the note and
    #      runs in
    #      seconds, taking no step: it re-derives the fill-in rows from the
    #      artifacts -- the two binaries and git -- and reports every
    #      figure missing from the note's row of that label.
    #      It reads each in its role and not merely as present, and in
    #      its own half's place.
    #      What it does not reach is half the block and all the prose: the
    #      rows a session writes from its own reading -- repetition, fills,
    #      straddle, regime, check, the sweep, the roster pass, the two
    #      check rows and `scripts set` -- and every figure outside the
    #      block, the roster counts and the previous run's totals among
    #      them. Those are yours, in one pass and not one call per figure
    #      And name that file where you write the figure, or the next
    #      reader copies you rather than re-deriving it. `./preflight.sh $R
    #      --note` re-checks 10c, 10d, 10e and 8 after these edits, in
    #      seconds
    #      And walk the arms of every task the registration defers to,
    #      not only its own -- so do not defer: write the clause out, with
    #      its arms named. A parked arm's live twin stands in for it
    #      where it is the same code for that clause's purpose. Where a
    #      pointer is kept anyway, follow it and read what it lands on
    #      why: nothing above reads what this half wrote.
    #      Nothing above reads what this half wrote: 4 to 10 are
    #      predicates over structure and not one of them reads a
    #      sentence, so a note and a registration full of quoted figures
    #      pass eleven PASS untouched. This is post-run step 7 scoped to
    #      the preparation and it is owed for the same reason. It costs
    #      minutes.
    #      A registration can predate a Main.hs commit that changes an arm
    #      it spans: Run 39's predated `c0a8aaa`, which rebuilt the fill
    #      behind one arm of a registered pair, and the span died on the
    #      second variable.
    #      The span printout exists because a span can compare
    #      the wrong operands, a claim about the PREVIOUS run spanned as
    #      `counts`, which compares the two HALVES, being unholdable the
    #      day it is written.
    #      10e reads the note's CARRIED blocks for a continuity claim that
    #      stops short of $PREV (`as Runs 20 to 31` in a note whose
    #      previous run is 32), an item number above what this run's
    #      registration carries ((10) against a registration of seven),
    #      and a half tag missing from the roll under NAMING THE HALVES;
    #      most of what a carried block states is of no kind a check can
    #      have.
    #      The `-sum` block and the table's column are different
    #      quantities.
    #      `--predictions` adjudicates THAT run's own items, so it prints
    #      the figure with its band and its verdict rather than a bare
    #      ratio -- `./read-run.py run32-nospec-runs.json --compare
    #      run32-ghead-runs.json --predictions` reads `libunord-stage7-sum`
    #      0.9691 and the 3.09 points that killed Run 32's item (3). Only
    #      an arm some span of that registration NAMES comes back, which is
    #      what `--compare`'s block above is for
    #      A `grep -n` for a line number is what sends a session to `sed`
    #      and from there into the chapter; a line number into prose does
    #      not survive a turn boundary either, the wrapping hook moving it.
    #      The re-derivation is a dozen reader calls whose tables nothing
    #      will quote, so only the verdicts need come back; a registration
    #      quoting a probe's counts otherwise sends the agent at a sweep
    #      nobody kept, which comes back unanswerable rather than wrong.
    #      A probe's figure wearing a run's name is the shape --carried was
    #      built for and reads exactly like a right one. At this step the
    #      run has not gone, so there is no $R JSON to hand it and none is
    #      wanted; the name is how it finds the OPEN entry in README.
    #      Handed only the main set it reports every item read on `runs`
    #      or `block` as matching nothing, which is the mode being asked
    #      the wrong question and not a finding; an item may quote a
    #      level, a count, a third arm. A registration carried over quotes
    #      the figures of the run before it, so $PREV's JSONs derive none
    #      of them and every such item comes back flagged, which is the
    #      wrong question again and costs a call the size of the roster.
    #      Post-run step 5 moved the registration into the run file and
    #      the write-up appended a verdict to every item, so a diff
    #      against that copy reports all of them changed. A carry-over is
    #      meant to change where the halves are renamed and where an
    #      amendment was decided.
    #      --figures catches a citation that has slid onto another row,
    #      and a swap between halves.
    #      `--lint` holds the registration's backticked arms to the timed
    #      roster and the arms of the task it defers to as well, but a
    #      clause naming another registration rather than an arm inherits
    #      that registration's arms and reaches no check at all. A
    #      restated clause is one `--lint` can hold to the roster; a
    #      deferral is one nothing can. That is the whole of the fix and
    #      it costs a paragraph
    #  12c. TAG THE NOTE'S ENTRY POINT `[EXEC]` FIRST: one block, saying
    #      what is spent, what is still owed and what the executing
    #      session acts on. `--note-check` refuses a note without one.
    #      THEN COMMIT, AND REVIEW BEFORE YOU DO, not after: walk what this
    #      half wrote for errors -- 12b is the figures, this is the shape
    #      of the changes -- and commit once at the end. Run
    #      `./run-status.sh $R` as the last thing before the commit, and
    #      clear the turn-end hold once the commit has landed.
    #      What the commit itself is: the registration on its own, tooling
    #      changes partitioned from it, and nothing pushed without a
    #      go-ahead. Roster debt that 7 or 8 finds at preflight -- a
    #      roster change whose commit left the counts stale -- is repaired
    #      in a commit of its own, before the registration's. Leave
    #      nothing uncommitted. The note is gitignored and
    #      goes with the pair, so it is never in a commit.
    #  That is the preparation. What wants a quiet machine is the run
    #      list below, which starts on an explicit
    #      go-ahead and never on a session's own reading of the box
    #      why: a review after the commit costs a rewrite.
    #      A review after 12c pays a history rewrite per error found,
    #      and the whole-tree checks again with it, since a document edit
    #      is content those checks read. This is the user-scope rule about
    #      committing at the end of an iteration rather than in the
    #      middle, at the one step here that can disobey it.
    #      run-status.sh is the only check that reads the note as the
    #      drivers will, so it is what catches an edit that left the note
    #      readable and unusable, which step 0's line records.
    #      Run list step 17 forbids an edit to the tree while the sequence
    #      runs, so what this half leaves uncommitted the other half
    #      cannot commit

**The shape of a registration, which pre-run step 12a writes and post-run step 5
moves whole.** ONE paragraph, one `OPEN` entry of the open list, led
`What Run N is built to answer, registered before it runs` and carrying numbered
items; the previous run's own file holds a worked example, and this is what
a session needs BEFORE reading one, a finished registration running to twenty
kilobytes with its verdicts. **Four facts a draft gets wrong, each of which has
cost a run.** A span's `within P%` is P POINTS of the ratio and not P percent
of the target, so `within 1.3%` on 1.2974 admits 1.2844 to 1.3104. A `cross`
or `counts` span is CROSS-HALF, so a scope of `both` reads it once in each
half's own orientation and the two readings are reciprocals --- `--lint` refuses
`both` on a target away from 1; a band set to a quantity nobody has measured,
on a target of 1, is the span readback's to catch, below, and
not this refusal's. `pair`, `cell` and `countdiff` are within-half and take
`both` at any target. And every span carries `on POP,...` and one of `basis`,
`control` or `both`; one carrying no scope is refused. The skeleton, two items
of the two kinds --- the open list's own `- ` bullet goes in front of the lead
and is left off here, `wrap80` reflowing an indented block whose first line
begins with one:

      `OPEN` **What Run N is built to answer, registered before it runs.**
        The pair is <the variable>: <what the halves share, and the one thing
        they do not>, so every span below reads <what a cross reads here> in
        `--compare`'s orientation of the unflagged basis over the control.
        <Each prior, with the artifact it was derived from named -- a JSON, a
        sweep, a run file -- and never quoted from a third document.>
        <Any limit the run cannot remove, named before it runs.>
        (1) *<The claim, one line, italic.>* `predict: cross list 1.2974
        within 1.3% on main basis`. <What a reading outside the band says,
        and which item tells the variable from a term it carries.>
        (2) *<The counted claim.>* `predict: counts list 1.3120 within 1.5%
        on main basis`, read with `--counts` over each population's own
        sweep, which run-list step 20 takes.

`--lint` prints every span as `--predictions` will compare it, which
is the check that the prose and the vocabulary ask ONE question; read each
printed line against the sentence beside its span. NO VERDICT WORD in the entry
--- `--check-doc` reads HELD, KILLED and their kin as an item already
adjudicated.

**THE RUN'S PREFIX BELONGS TO THE RUN'S OWN PROCESSES, and nothing else may take
it.** `$R-gate-*` and `$R-al-*` are the two exceptions the drivers were taught
to skip; every other artifact --- a smoke pass, a probe, a repetition, a scratch
log, a driver's own redirect --- is `probe-*` or `smoke-*` and never
`$R-`anything. Two things read that namespace and neither can tell your file
from a process. `run-major.sh` refuses to start over a `$R-*.json`
or `$R-*.log`, which is loud and costs nothing. **`read-all.sh`
and `properties.py` read a `$R-*.json` as one of the run's own processes**,
so a stray file under the prefix turns clean gates into failed processes
and fails the properties, reading exactly like the run breaking. **This
is the one statement of the rule and the other sites point at it**: the smoke
step and post-run step 3 each name it in a clause and link back.

**Then the run --- and this is the list that wants the machine, so it does
not start on a session's judgement.** Steps 13 to 20 sit here rather
than with the preparation above because the evening runs through them: 14, 17
and 19 want the machine quiet and 20 merely spends it, 16 reads it, 13 decides
whether the gate is owed, and 15 and 18 are what the session reads while
the driver runs. The gate is five minutes and the sequence is most
of an evening, and both want the desktop to itself. **The person's request
for the run IS the go-ahead, this whole list with it --- though what it buys
is the QUIET machine only as far as 19a, where the list hands it back ---
so nothing below is a reason to come back and ask --- but it has to
be the person's and it has to be for the run: a request relayed by an agent
is not one, whatever it says, a session seated by another session has
not been given anything, and none of it is ever inferred from a quiet machine.**
A run being two sessions, **that is the normal path and not a guard**:
the preparing session's go-ahead stopped at 12 and cannot be passed on,
so an executing session always arrives needing its own, and a spent preparation
with an unrun gate is what it should expect to find. A session that finds itself
here without that request stops and reports what it verified --- it does
not wait for one and does not hand the run on, the preparation it confirmed
surviving in the note, which is what the note is for. No `uptime` or `ps` is run
at this point, and neither would settle it if it were: what they cannot see
is what their owner is about to want the machine for. Step 16's alarm is
not a permission either --- it runs after the go-ahead and before the longest
stretch, so a machine that got busy since stops the run short of the hours
rather than after them. Execute the list, its `why:` pointers being the prose;
its machine steps are two commands, so what a session does here is read.
Unsandboxed throughout:

    #  TERMS, here and in the post-run list: $R is this run, $PREV the
    #      one before; the note is $R-pair.txt, whose HALVES: line names
    #      <basis> and <other>, the control; the run file is runs/$R.md;
    #      the open list is README's `What is open`; `item N` is the
    #      readings list, `./read-run.py --checklist readings`.
    grep -i gate $R-pair.txt              # 13. has the gate run?
    #      read UP: the newest GATE: line is the script's own block, clean
    #      or FAILED, and no verdict is written by hand.
    #      The note is always somebody else's; NOT RUN is its ordinary
    #      answer and means the evening's first stage takes the gate, so
    #      read its [EXEC] blocks and not the note -- those are the ones
    #      this session ACTS on, where [SAME] and [PAIR'S] say who WROTE
    #      the block; the rest is the preparation's record and is skimmed.
    #      DONE WHEN the newest GATE: block reads mechanically clean, or
    #      GATE: reads NOT RUN.
    #      why: --para 'A paired Run has one gate more'
    #      THERE IS NO `or the whole note` BRANCH: a note without an
    #      [EXEC] block is a note `--note-check` refuses at pre-run 12c,
    #      so by the time this step reads one the block is there
    ./read-run.py --section 'What this run was built to answer' \
      --run-doc runs/$PREV.md             # 13a, AND EVERY OTHER READING
    #      THIS LIST OWES, HERE AND NOT INSIDE THE EVENING BELOW. Read
    #      now: the PREVIOUS run's registered predictions and their
    #      verdicts, in its own file -- `--para 'What Run'` reads the
    #      pointer and not the registration, and an empty-looking answer
    #      is not a blocker; the open list by its status markers (READ
    #      NOW: item 7); and the post-run list's first half, `--checklist
    #      post-a`. NOT the replace list, walked at post-run step 6. NOT
    #      ITEMS 2, 4, 5 AND 6, read at post-run 4, 5 and 6a with the text
    #      open. Spawn no agent for them.
    #      why: --para 'registered predictions'
    #      The replace list gains nothing from being read six hours early;
    #      items 2, 4, 5 and 6 are the sections post-run 4, 5 and 6a
    #      rewrite; and the open list's ruling on the readings carrier is
    #      why no agent is spawned.
    #      THIS SITS BEFORE THE LAUNCH BECAUSE THE EXPOSURE IS PER
    #      COMMAND AND NOT PER MINUTE: a read here costs 0.08 s to 0.37 s
    #      of CPU, a bench's samples are milliseconds, and half a second
    #      of anything concurrent trips the 0.25-of-a-core bar the reader
    #      calls an intrusion. So there is no quiet window inside the
    #      evening to move the reading to; there is one before it, and a
    #      reading this cheap has no claim on the hours anyway.
    ./run-status.sh $R                    # AND THE DONE-CONDITION, run HERE
    #      and whenever the run seems finished, and NEVER between the launch
    #      below and the riders' last line. It checks every step of the
    #      three lists an artifact or the repository can answer for,
    #      `STATUS: all done` being the one state in which a session is
    #      finished with a run, whatever it has to report. A NOT DONE line
    #      is the next step.
    #      why: in that window it lands inside a timed process
    #      (the open list's reading-windows entry)
    ./run-evening.sh $R                   # 14 TO 19 IN ONE COMMAND, in
    #      the harness's background mode and NOT a typed `&`, AND WITH NO
    #      REDIRECT. CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 must be
    #      in the harness's environment -- the user settings carry it,
    #      and this script refuses to start under the harness without it,
    #      so a session without the setting stops here and not hours in.
    #      It runs the gate (14), the alarm (16), the instance gate (16a:
    #      SUSPENDED WITH hugebin/ -- instance-gate.sh
    #      says so PER HALF, naming each, and exits 0), the sequence (17),
    #      the machine check (17a) and the riders (19), in that order,
    #      under the environment the
    #      note's LAUNCH: line names, each stage's verdict appended to
    #      $R-evening.txt as it lands and the machine handed back on its
    #      last line. It refuses a note without HALVES:, LAUNCH: and
    #      RIDERS: lines; it skips a gate the note records mechanically
    #      clean; the gate refusing or a busy box stops it, and nothing
    #      after that does. CONFIRM THE LAUNCH by `evening begins` in
    #      $R-evening.txt and never by the launching shell's output.
    #      A DEAD ATTEMPT IS PARKED, NOT DELETED. Where the box goes busy
    #      mid-gate, or a stage is killed, stop the driver, check no child
    #      survived, and move what it left aside as
    #      `probe-killed-$R-<half>-<pop>.json.truncated`. Then EITHER move
    #      the dead attempt's $R-evening.txt aside and launch again, OR
    #      resume it at the stage that died, `./run-evening.sh $R --from
    #      STAGE` (gate, alarm, instance, sequence, machine or riders),
    #      which
    #      appends to that file under a `resumed` line -- a sequence only
    #      where no process of it started, its stray check refusing any
    #      $R-*.json or $R-*.log; one that started is finished by step
    #      17's class loop.
    #      ARM NOTHING BESIDE IT: its exit is the session's wake-up. ASKED
    #      MID-EVENING, answer with `./evening-status.sh $R`, one line off
    #      two tails, and nothing heavier.
    #      why: --para 'The harness reaps a backgrounded job'
    #      and why: --para 'run-major.sh is that sequence'
    #      and why: --para 'Nothing is armed beside the evening'
    #      NO REDIRECT: the harness keeps the output, and a file named for
    #      the run is one the sequence's relaunch guard refuses over,
    #      which the driver refuses before its gate. The harness kills a task it tracks on a kernel
    #      memory-pressure event unless that variable is in its
    #      environment.
    #      16a has no instance to gate when the halves launch from disk,
    #      so the stage still runs and costs nothing. Where a run raises
    #      the mount as the emergency step 2 describes, 16a is each half's
    #      launch instance against a fresh copy on one cell, the copy
    #      swapped in when the launch is the slow draw and the slow one
    #      parked as hugebin/$R-<half>.slow, which post-run step 9's
    #      deletion offer covers with the rest
    #      (why: --para 'the gate written to catch the slow draw').
    #      A blocked write leaves a launch that never happened looking
    #      like one in progress, hence `evening begins`.
    #      The parking name is the one step 17 already fixes for a killed
    #      process: criterion writes that file as it goes, so a killed
    #      process leaves a truncated one, and properties.py reads every
    #      `.json` here that does not begin `zz`.
    #      Eight hours of ticks cost more than the one cold read they
    #      forestall, and a status call costs 0.81 of a core on a box
    #      being timed.
    #  14. THE GATE, its first stage: run-gate.sh on both halves twice in a
    #      palindrome, `list`, `bq-expand` and both `sum-only` halves over
    #      the `rev` class, about five minutes, and FOUR --compare readings
    #      put in $R-evening-out.txt: the two cross-half passes, the -a
    #      pair and the -b pair, and then EACH HALF over its own two legs.
    #      No verdict is written on it -- the readings
    #      are the write-up's -- and never quote a magnitude from one. A
    #      spread between the passes IS the two halves' own drift, the
    #      passes' ratio being the control's legs over the basis's by
    #      construction: read which half moved. `./read-run.py
    #      --gate-draft $R` puts the four side by side, and the driver
    #      appends it to $R-evening-out.txt, with the registration's
    #      `cross` spans ON THE GATE'S CLASS held to the two passes under
    #      it, the rest named as 5c's: a span outside its band there is a
    #      question, not a forecast.
    #      why: the second pair of readings says what a spread is.
    #      THE SECOND PAIR OF READINGS IS WHAT A SPREAD BETWEEN THE
    #      PASSES IS, before it is the pair's: the control's legs over the
    #      basis's ARE the second pass over the first, term by term, so
    #      they attribute a spread and cannot fail to match it.
    #      It is owed on every pair, both halves being
    #      two builds by the BOTH HALVES ARE BUILT ANEW ruling, and again
    #      after either half is rebuilt: run-evening.sh inherits a recorded
    #      gate only for the binaries its block names by md5
    #  16. THE ALARM, its second stage: two reads of /proc/stat two seconds
    #      apart, refused above 5% non-idle, MAXBUSY overriding -- the
    #      reading the riders take. The request for the run is the
    #      go-ahead: ask nothing here.
    #      why: an alarm and never a permission.
    #      It only stops a box that got busy since short of the hours
    #      rather than after them
    #  17. THE SEQUENCE, its third stage: run-major.sh, many processes,
    #      several hours, its complaints recorded and not fatal. Read back
    #      each process's `start` line in the wallclock log for the
    #      instance it launched, `from ./$R-<half>` while hugebin/ is
    #      suspended and `from hugebin/$R-<half>` on a run that raised it,
    #      rather than assuming either. NOTHING ELSE ON THE MACHINE, AND
    #      NO EDIT TO THE TREE, until the evening ends. Never raise -L on
    #      a recorded run. Look at a process far slower than its
    #      neighbours against the previous run's -wallclock.log, SCALED BY
    #      THE BENCH COUNT. No resume once a process has started: if it dies mid-sequence, hand-run
    #      the class loop over both halves, skipping a population on
    #      whether its JSON PARSES and never on whether it exists;
    #      `python3 -c 'import json,sys; json.load(open(sys.argv[1]))'
    #      "$out.json" 2>/dev/null && continue` is the test. PARK THE
    #      TRUNCATED ONE UNDER A NAME THAT DOES NOT END IN `.json`,
    #      `probe-killed-$R-<half>-<pop>.json.truncated`. Check each
    #      benchmarking count against `classes --list`, append to the same
    #      $R-wallclock.log, and say in the write-up that the populations
    #      ran in more than one window. Pre-registered probes are appended
    #      after the classes, INSIDE THIS STAGE, and need no asking, 19a's
    #      ask being for a probe the sequence did not carry;
    #      a filtered probe takes ONE -m MODE then its patterns, and its
    #      benchmarking lines are counted before any number is read
    #      why: an edit moves the driver's git lines, the binary's
    #      provenance; criterion spends its budget per bench.
    #      Criterion writes the JSON as it goes, so a killed process
    #      leaves a truncated one. `probe-` alone keeps it out of
    #      read-all.sh's plateau glob and NOT out of properties.py's
    #      corpus, which globs every `.json` here and fails its properties
    #      on a truncated one.
    #  17a. THE MACHINE CHECK, its fourth stage: `list`'s net
    #      on the basis half's main-set JSON against the fingerprint of the
    #      note's COMPARE run, or of the newest run file, its reading in
    #      $R-evening-out.txt and one line in $R-evening.txt. It stops
    #      nothing, a moved box being read and named; a COMPARE line
    #      naming a run with no file stops the evening before the gate.
    #      why: --para 'A paired Run has one gate more'
    #  19. THE RIDERS, its fifth stage: run-alonelegs.sh on each half,
    #      control first, clean (SATURATE stripped from the launch
    #      environment) and then `SAT=1` where the note's RIDERS: line
    #      says `sat` -- the main-set `list` alone legs, one bench
    #      per process. Each refuses a previous attempt's artifacts, reads
    #      the baked RTS line back, and refuses a busy machine as 16 does
    #      why: without them a run cannot check a span prediction.
    #      They turn the in-process deflation from an estimate into a
    #      per-shape measurement
    #  19a. THEN, WOKEN, AND THE MACHINE IS FREE: read $R-evening.txt top
    #      to bottom -- each stage's rc and any COMPLAINT -- then
    #      $R-wallclock.log's `!!` lines, and report each stage's exit,
    #      the machine check's line among them, rather than folding them
    #      into a later summary. HOLD ANY TOOLING FIX a stage's complaint calls for
    #      until the write-up's 7a, save one a 6a gate cannot pass
    #      without, made at 6a in a commit of its own, as the open list's
    #      owed changes are. READ THE CONTAINING ARTIFACT ONLY,
    #      NEVER BOTH: $R-evening-out.txt holds $R-wallclock.log byte for
    #      byte, and the write-up reads the first. A file the harness
    #      persisted out of a command's own output is read, never the
    #      copy opened too.
    #      AND SAY THAT THE BOX NEED NOT BE QUIET ANY MORE, BESIDE the
    #      launch below, in the message carrying its tool call.
    #      AND THE CLAIM ON A QUIET BOX ENDS WITH THE SAYING: anything
    #      wanting the box quiet AGAIN -- a probe the sequence did not
    #      carry, post-run 3's rerun unless the note's RERUN: line says
    #      `allowed`, a filtered A/B this run's results
    #      suggest -- is ASKED FOR and waited on, one ask to a sitting,
    #      unless the note's QUIET-AFTER: line says `allowed`, which
    #      covers every timed reading this run's results call for, the
    #      copy test above all, post-run 3's rerun being RERUN:'s.
    #      AN `ask` WITH NOBODY AT THE MACHINE WAITS FOR THE OWNER'S
    #      RETURN: the session goes on with what wants no quiet box and
    #      asks when they are back, an absent owner being no `allowed`
    #      and no `no` (ruled 2026-09-26).
    #      THAT WAIT COSTS THE RUN NOTHING and is not a shortfall to
    #      work around (the owner, 2026-09-27): the write-up finishes
    #      without the reading, the open list records it as owed, and
    #      the owner asks for the quiet box at a later sitting, the
    #      run file amended when it lands. What the wait owes is that
    #      nothing evict the timed binaries meanwhile -- no reboot, no
    #      copy over them -- or a copy test reads an
    #      INSTANCE term as gone.
    #      why: a fix landed mid-write-up costs every stretch after it an
    #      unwrap, each commit rewrapping README.
    #      The log read here is a second copy of what the out file had, and
    #      opening a persisted copy reads it twice.
    #      Nothing below wants a quiet box (20's own line says why), so
    #      the desktop goes back to its owner here; a message with no tool
    #      call is a turn end and not a note. It is why the evening is two
    #      commands at all: chained, the counts hold the box past the last
    #      stage that needs it with the session asleep, so nobody can be
    #      told.
    #      The saying is THE ONE STATEMENT OF THAT RULE and what the sites
    #      below point at. The request that bought the evening bought the
    #      hours up to here; and the chapter's own test agrees, a probe
    #      being exactly a thing that changes what the machine does next
    ./run-counts-all.sh $R                # 20, IN THE SAME TURN, in the
    #      harness's background mode again, as at 14. ITS EXIT IS ITS
    #      ANNOUNCEMENT: poll nothing of it before then.
    #      Quote how long it
    #      takes from the previous run's `./read-run.py --counts-cost
    #      $PREV`, never a guess
    #      why: a typed `&` would detach and wake nobody
    #  20. THE COUNTS, THE SECOND COMMAND: run-counts-all.sh, which is
    #      run-counts.sh over EVERY population, the main set and each
    #      class, control then basis apiece, a
    #      `$R-counts-<half>[-<class>].txt` each: instructions an iteration
    #      from two fixed-`-n` processes a cell, differenced; `--counts`
    #      reads a pair of these files beside `--compare`. An arm whose
    #      time moved between the halves either moved its counts with it,
    #      which is codegen, or did not, which is the runtime or the
    #      memory. perf must be able to count, kernel.perf_event_paranoid
    #      at 1 or less; the script probes it on /bin/true and refuses in
    #      a millisecond, and run-counts-all.sh refuses a stage still
    #      running besides.
    #      THEN, WOKEN AGAIN: read the counts stages in $R-evening.txt,
    #      whose last line is EVENING COMPLETE and whose tally is the
    #      complaints of both commands; report each rather than folding
    #      them into a later summary, and go on with the post-run list in
    #      its order, whose 1, 2 and 3a's twin builds may
    #      already have run beside the counts.
    #      why: an instruction count wants no quiet machine.
    #      It owes criterion nothing and is insensitive to load; counted
    #      beside a timed process, both readings are spoilt

**One rule for the sandbox in this directory, since half of what a run does must
write here.** Run everything unsandboxed except the read-only checks.
Those are worth having cheap and are all of them safe: both `check`s, `diag`,
`--lint`, `--check-doc`, `tools/loop-offsets.py`, `--list`, a `grep`
of the note, and pre-run steps 6 to 10 --- except 8c and 8d, which write `zz-`
fixtures here and remove them. Everything that builds, benchmarks or leaves
a file is the other kind: 2, 11, 12, 14, 17, 19 and 20, and steps 4 and 5 too,
which write only through their redirect and that is enough. A session starts
in `~/r/horde-ad`, so its sandbox permits writes there and to its own temp
directory and nowhere else; THIS directory is outside it, and `run-major.sh`
moves here before doing anything. **And never write `$TMPDIR` here; spell
the scratch path in full.** That variable is `/tmp/claude-1000`
under the sandbox and `/tmp` outside it, so the idiom that works in a read-only
check writes somewhere else the moment the flag that makes a command able
to write at all is added --- silently, the write succeeding and the file missing
from the next sandboxed read. The rule is about the PLACE and not the variable,
because the conditional it would otherwise be turns on a property of the call,
which changes call to call here, where `$TMPDIR/x` is a habit that does not.
`/tmp/a.log` is in neither permitted directory and `/tmp/claude` is not the temp
directory in every seat. **The two refusals do not look alike, which is the part
that has cost hours.** A redirection on a simple command is checked before exec,
so the benchmark never starts at all; `log`'s `tee` is a pipeline whose `echo`
still prints, so you get the sequence's start lines on the console,
no wall-clock file, no JSON and no run. That reads as a run in progress, which
is how two copies once ended up on this machine at once. Confirm a launch
by an unsandboxed process list, never by the launching shell --- and note
that `ps` in a session lists only that session's own processes, so it catches
a launch made from here and not one made from anywhere else, `uptime` being
the half of it that reaches the machine.

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
a session's token budget is spent and where its mistakes are made. **The class
blocks are not the bulk of the typing**: `install-tables.sh` writes their
computed paragraphs --- table, controls, provenance, per-shape line, cross-half
line --- so what is left per class is the one paragraph of what it says, written
from the verdicts `--block` emits rather than from the table above it. One
paragraph of judgement per class, and nothing else. **The run file's head
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
invocation per process or per registration --- a `--selftest` and an `--aa`
apiece, the dozen-odd `--pair` lines, a `--block` per class --- goes in one call
per kind, so steps 1 and 3 together are a handful. *One per site*: the eleven
`--in-place` installs, three calls. *Unbatchable*: the prose, one edit per
paragraph, and this is the bulk --- the class blocks alone are one paragraph
apiece, plus a lead wherever the roster moved one, and no tool reduces
the count, `--block`'s skeletons only removing the extraction that used
to precede each. Then verification costs about what the prose cost, and can cost
more, because every finding is a fix and every fix is a claim. **Budget the run
file's head, the verification and the class paragraphs as the work**,
in that order; the readings are noise beside them, and the run itself
is unattended. Two further consequences worth having in mind before starting.
Prefer analysis that localises --- per shape, per control --- over re-quoting
figures that moved a few percent and changed nothing; the first is where
the surprises have come from and the second is what has gone stale twice.

**A probe is not a lesser instrument than a major run, and the write-up is where
the instruments get built.** A registered question can come back a null while
the write-up's own mistakes yield checks and rules, so the write-up
is an instrument-building phase and not only a reporting one, and what is worth
watching for is the computation you improvised, the check that would have caught
the error, the step you skipped, the capability you found, and the reading you
delegated and what it cost --- that set is the run's other product,
and it outlives the figures, which the next run replaces.

**Write a capability as a capability.** A fact recorded as a tool's limitation
goes inert: *`run-major.sh` cannot give one binary two RTS configurations*
is true, and mounted two nursery questions as recorded runs, where *any nursery
question is answerable on an already-built binary; only a recorded run needs
the driver* would have kept both out of a run altogether. So when a limitation
is found, write down what it still leaves possible, in the place a session looks
before spending.

**A preparation already spent on THIS run may be any age, and a later session
re-enters at 13.** Nothing in the preparation wants a quiet machine, so
it is legitimately an afternoon days before the evening. What such a session
never owes again is the three that cost machine time: the gate, the smoke sweep
and the roster pass are properties of the pair and its roster, and the note
is the only thing that outlives a session, so each is recorded there or is paid
again --- minutes of quiet machine in the gate's case, the step most often
re-run when it should not be. What it does owe is `--lint` and `--check-doc`,
the README having moved under it, and the cheap read-only steps with them --- 4
to 10 are seconds each, so re-running them costs less than deciding not to.
The exception is the roster pass, whose own note line records it being re-taken
the same day for exactly this reason --- a pass belongs to the roster
it was taken on, and a roster that moved since voids it. None of this reaches
a *previous* run's preparation, whose binaries the BOTH HALVES ARE BUILT ANEW
ruling refuses whatever their age.

**And before any of that, the previous run has to be finished.** Nothing
in this list asks, and starting on top of a half-written write-up is a wrong
start no later step catches: the artifacts of a run whose post-run step 9
was never reached look exactly like those of one whose deletion offer
was declined. The evidence is on the disk and in the open list --- `runs/`
already carries a file for your run, and the open list carries its registration.

**Why the build's three rules are what they are.** *The fills read
at the build*: the pinning claim --- that an addition costing nothing to place
leaves the tracked loops where they were --- is read at every build that brings
a new function, by `loop-offsets.py --delta` against the previous build
of the same recipe, because the reading costs nothing at that moment and cannot
be taken afterwards. Its record, form by form, is [the floor section][floor]'s
--- killed under the max-skip form, holding for the tracked heads' offsets
under the dead-spot form --- and the numbers are each run's own file's,
this chapter carrying only the pointer. What the reading does not reach
is the rest of the placement term: `build` has read five points from `mut-odo`
with both heads at offset 0, so a cross-run column still owes the counted work
before a movement on a fill is called code. And the eight are the sample;
the population reading is `--library` between the two builds. *Build both,
always*: reusing the previous run's basis binary was refused on 2026-08-16
because the other half is built today, so the pair's two halves went through
whatever the shim was on two different days --- the very effect the back-to-back
rule exists to keep out, reached by a route that rule does not name, since
nothing is rebuilt BETWEEN the halves and the drift is between the RUNS. No step
downstream can see it, and the argument reaches every way of not building two
halves today: a probe's binary carries the same gap, a copy makes one recipe
stand for two, and one binary run twice under two sets of flags is a pair whose
halves cannot differ in anything the compiler decided. The BOTH HALVES ARE BUILT
ANEW ruling refuses all four. *The md5 on a repetition*: what the note's
recorded inputs do not cover is the dependency store. `cabal.project.freeze`
pins the versions and an index-state and NOT the ABI hashes, so a store rebuilt
at unchanged versions relinks every call target and changes half of `.text`
while every check in the list still passes, the tracked loops not having moved.
The ABI hashes are read
with `strings B | grep -oE '[A-Za-z][A-Za-z0-9-]*zm[0-9zi.]+zm[0-9a-f]{32,}'`,
whose leading character class is the whole of the care it takes: the narrower
`[a-z-]` silently drops `QuickCheck`, `Glob` and `text-iso8601`.

Of step 10's two readings, the library one is what a two-shim pair cannot take
on trust. No `-pgma` shim reaches a library, so a library loop that moved
was displaced by a change in `.text`'s size, and a pair that moves them prices
that displacement along with whatever it meant to price.

There is no single-binary form of a major run any more, the pairing being
permanent: `run-major.sh` and `run-gate.sh` both refuse to start without both
halves, so a lone binary has no driver. What
`cabal build micro ${REGIME:+--ghc-options=$REGIME}` is still for is a probe ---
a filtered handful of benches answering one question --- and those are run
with `cabal run micro ${REGIME:+--ghc-options=$REGIME} --`, never through
the sequence below.

**The cheap checks run against the binaries that will be timed**, not a third
built beside them, and the two document checks against `Main.hs` and this file,
which open no binary at all. The `2>/dev/null` on `--list` is not optional,
the provenance line going to stderr and interleaving inside a bench name without
it.

**What the script-check steps are each for.** `defect-lint.py .` reads
the source of every Python program here --- the shell drivers are outside an AST
family's reach, and shellcheck's --- and is the one of them that can name a site
nobody has met. `properties.py` withholds the reader's own stderr and counts
it by kind because the reader warns once per run per table about rows a later
roster dropped, which is correct and was 198 KB against six lines of verdict.
`defect-run.py .` runs every case, which is 8d's, and `--changed .` only
the cases whose own script moved, which is what an edit owes between
preparations, saying so and claiming nothing where none did.
And `defect-run.py --audit .` replays each case against the code before its own
fix, where it MUST fail --- the suite's own non-vacuity, and worth a look after
adding one. `selftest-mutants.py .`, 8e, replays the deliberate breaks
in `mutants.py`, each of which some check must catch. The tools
but `properties.py` are the shared ones on PATH from `~/.claude/bin`; what
is this directory's is the corpus `defects.py`, the properties, and two lists
of the lot: `checks.py`'s static steps, which `check-all .` runs after an edit,
and `checks-deep.py`'s properties over every run, cases both ways and mutants,
which `check-all checks-deep.py` runs once a preparation as 8c to 8e, and daily
or so when the owner asks.

**What the `note:` lines ARE, the list having said only that they do not stop
you.** They are the write-up's adjudication material and nothing a preparation
owes: every superseded figure, every superlative, every absolute time the two
documents quote, every four-decimal figure a new paragraph quotes without naming
the reader mode that printed it, and every link from standing prose
into the run's file as a whole. They are withheld by count and **`--worklists`
is what prints them**, at post-run step 6e and at no other call ---
not the absence of `--quiet`, which is the default now and withholds just
the same. `--lint` reads the same way, noting the rostered arms it knows
are deliberately untimed. **One of those `ok:` lines is the wrap check,
and it reads differently mid-edit.** It asks its question per paragraph rather
than of the whole file, so a paragraph an edit left on one line is reported
as mid-edit and not failed, and a `FAIL:` there means a paragraph wrapped
by *hand* --- neither the formatter's form nor one line. The gate therefore
stays green on a document being worked on and asks for no wrapping at all:
the commit hook wraps a tracked document back, and a check is run on whichever
form is in front of you.

Both halves: on a pair of two shims both can be mispadded, so both are checked.
The halves are held to each other besides --- a sound pair makes the two logs
byte-identical, agreement on every shape being a property of the strategies
and not of where their loops landed. A difference stops the run, and the rebuild
goes through the recipe in that pair's note. Steps 4 and 5 cost about a minute
and a half.

**Then confirm the regime is the one intended**, which nothing later can: step
9's `diag`, and read one row of it --- the allocated bytes of `baseOffsetsScan`
against `baseOffsetsMut` on `vgg-14-c512`, which is a `diag` label rather
than a shape and so will not be found in the shape set. They are equal to three
figures under SpecConstr and ten times apart at plain -O1, a separation no eye
misreads, and both ends of it are measured (2026-08-08), the flag being the only
thing that moves them. Seconds, and the seconds after a rebuild the flag forces
anyway. It is the only check standing between a mistyped regime and a run
that refutes the design it was built to test.

**A paired Run adds a second binary, and both are built and checked before
either is timed.** Alignment is not a regime flag: it arrives on `-pgma`, GHC
notices neither that nor `-fproc-alignment`, and a rebuild between the two
halves would put back the very effect the pairing measures. That is why the two
halves are built one after the other from the note's recipes, with nothing
touched in between, and why both executables are kept --- and why the note
is written first and the predictions are registered against the offsets step 10
reads out of the binaries this run built, an inherited half leaving them
registered against a binary the run does not carry.

`check` is the gate and the offsets are not, a wrongly padded binary having
correct-looking offsets and wrong answers. Read both listings anyway: what each
half's fills are, since a prediction made per arm is made from them and no later
binary has them. **Whether any short loop of a half's own code straddles
is the build path's to read and the note's to keep**, `--survey` being
the length-agnostic form, one binary at a time, and the answer a property
of the pair --- offsets at 0 are what a fully padded half shows and not a thing
to require of a max-skip one, which leaves a resident loop where it fell; what
"every timed arm's loop" means is bounded by what can be attributed at all.
The exit-span count the survey prints beside the straddlers (2026-09-16) is read
the same way and is sharper: under `LOOP_EXITSPAN=1` it is 0 on both halves
by the shim's own claim, so a nonzero there is a recipe or shim defect,
or the reader's, and never a placement, while a half built without the switch
records it, in the tens. The sequence below runs each half in turn,
and `run-major.sh` does it for you; what neither can do is interleave two
processes of this size within a population, so the order they ran in is written
down and is left uncontrolled.

**The halves can differ by more than Main's alignment, the shim reaching only
what GHC compiles here**: aligning grows `.text`, so everything linked after
it moves, library loops among them, and an arm whose innermost work is library
code, as `list`'s is, carries a term the pairing scrambles instead of removing.
Padding one half to the other's size *and phase* closes it, size alone leaving
the worst shift available; the two-step is in `tools/align-as.py`'s docstring,
beside the `PAD_BYTES` it feeds. **A pair of two shims has no such step
and no such guarantee**, only whatever its two recipes give it, which is why
`loop-offsets.py --library` exists: it reports what share of the library
self-loops the two halves put at the same offset in their line. **What a given
reading means is banded here rather than carried forward note by note**:
near-total where the two halves are one source padded to one size and PHASE;
between a tenth and a quarter across the pairs that vary a shim or a compiler;
and lower still where the halves differ in where every pad is PLACED. Read
a pair's own figure against the band its recipes put it in, and record
in its note that figure and no other. A note may record the same property
the other way round, off `nm` symbol by symbol, which is the stronger reading
and not this tool's output --- so compare like with like, or read the note's own
figure as the note's.

**Which two halves a pair has is a property of the pair, not of this README ---
but how they are named is not.** A half is `$R-<tag>`, the tag naming what
that half *is* rather than which role it holds: `run13-maxskip`
and `run13-lookrts`, `run14-lookrts` and `run14-a1g`. So a new pair derives
its own names before it has a note to read them from, and step 2a's rule stands
untouched, the tag saying what a half is and the note saying which of them
is the basis. The names are recorded on the pair note's `HALVES:` line, which
every script that takes a run reads through `pair-halves.sh` --- an environment
naming them differently is refused, one repeating them allowed, and with no note
at all the environment stands in and says so --- as `OTHER` and `BASIS`;
the basis is the half the expected bench counts are read from and every table
is installed from, and it runs second; both halves run every class. **The two
roles are BASIS and CONTROL**, which is what this README calls them where
it names a role at all; the scripts' variable is `OTHER` and the prose often
says *the other half*, and all three are one thing. The halves are named
for what they vary --- `unaligned`/`aligned`, `maxskip`/`aligned`,
`maxskip`/`maxskippa` --- and which of them is the basis is a decision the pair
note records, not something a half's name tells you. Calling the basis
*the aligned half* would collide on the last of those, whose control `maxskippa`
carries `-fproc-alignment=64` and so is the more aligned build of the two. Where
a sentence says *aligned* it is about alignment, not about a role; where
it is plainly about one past pair it keeps that pair's half names.

**Every half tag on record is hyphen-free, and two tools require it.**
`install-tables.sh` finds the basis's class JSONs by globbing
`$R-<basis>-*.json`, so a control called `<basis>-pa` is caught by that glob
and `ls` sorts it after the basis's own --- leaving the CONTROL half's table
in every class block under a driver that says every table comes from the basis,
with nothing downstream able to see it; it is refused there rather than left
to the naming. `pair-halves.sh` refuses a tag outside `[A-Za-z0-9_]`. The roll
of tags this chapter has used is `aligned`, `maxskip`, `maxskippa`, `lookrts`,
`a1g`, `a32m`, `g912`, `g914`, `ghead`, `spot`, `spec`, `nospec`, `libcase`,
`o2`, `exit`, `gheadexit`, `gheadnospec` and `gheadtwopass`, `maxskip` before
`maxskippa`, and `ghead` before `gheadexit`, `gheadnospec` and `gheadtwopass`,
being bare prefixes and safe, the hyphen alone colliding. **The roll lives here
and not in a pair note**, copies of it having drifted: a note names its own two
halves and points here for the rest.

**Name the artifacts by half, and drive every `--in-place` from the basis
half.** The sequence below builds every filename off `$R`, which a paired Run
has to split: one `$R-<half>-main.json` per half, and the class files
`$R-<basis>-$c.json`, there being no others --- the infix being the binary's own
name, so an artifact cannot be traced to the wrong half. **One scheme covers
everything a run leaves**, the binaries and the pair note with the JSONs:
`$R-<rest>`, the run first and nothing before it, which is what stops two runs
writing one filename. Binaries from Run 11 and earlier were named for the half
alone (`micro-aligned`, `micro-unaligned`), which is what this README's history
calls them. So **the basis half is the table and the other half
is the control**, whatever the control is built to price.

**What the other half is for**, since a run that publishes no table from it will
otherwise be asked why it spends an hour building and timing it. That depends
on which half it is, and the pair is chosen for it. A *compiler* control
is the reading a form about to be published is owed on a second codegen: it says
whether the basis half's orderings are one compiler's accident, and its counted
work is what separates the instructions a compiler emits from the slot it put
them in. An *unaligned* control is the layout one, the per-arm term being
measured afresh each run rather than inherited, and it is the yardstick for GHC
itself: the native backend aligns no loop today ([the floor section][floor]),
and when that is fixed the same pairing is what prices how well GHC does
it against the assembler shim here --- a comparison no single build can make.
A *max-skip* counterpart prices the shim's own padding instead, its two halves
differing in which loop heads get a directive and in nothing else, so its arms
separate what alignment buys from what the NOPs cost.

**The pairing doubles the classes too.** Both halves run the main set, since
that is where the per-arm comparison lives, and both run every class as well:
a pair's variable can act on a class and not on the main set, as an allocation
area does on the shapes whose excess allocation crosses the nursery, and a class
read on one half only cannot say whether the variable touched it. The rule
is standing, paid every run, so that no run has to see its own need coming;
the cost is one more process per class.

**And one more, nearly free**, because everything above exercises
the *benchmark* while nothing exercises the *reader* until hours later.
`smoke-sweep.sh`, step 11, runs three `-L1` processes --- one main-set shape
from each half and one class shape from the basis --- then every reader mode
over what they wrote, the `--in-place` installers into a copy of the run file,
and deletes all of it; its header says what it holds each process to and what
it proves. Minutes, no quiet machine, and the reader's code paths rather
than its statistics, `-L1` being a rougher budget than any recorded run's.
**It is a driver for the reason `run-major.sh` is one:** it counts, and a pasted
copy of a driver's sequence drifts from the driver with nothing checking it.
**What it proves and what it does not**: each *table* installer found its table
and wrote something, `cmp` failing loudly where the copy came out identical,
which is the case where one silently found nothing; an installer must REFUSE,
a table being written over the whole main set and a smoke run being one shape
of it, so a zero exit there is the failure. It does not prove the right rows
went to the right place --- that guarantee is `install`'s, which matches
by whole line and asserts the row count, so a mis-paste is impossible rather
than merely detectable --- and it is hours too late to find a broken installer
at the write-up.

**Run every mode, not the interesting ones**, which is why the script sweeps
them as a loop: a removal can kill a mode nobody thought to run while `check`,
`--lint`, `--check-doc` and `--selftest` all pass. The second file exists
for `--compare`, the reader's only two-run mode and the one a paired Run is read
with, and it is the only point before the evening at which the *other* half
writes a JSON at all; a pair whose halves turn out not to be comparable has cost
the hours twice. Modes are cheap to run and expensive to be missing, and the run
artifact is the only thing that can reproduce one, so sweep before deleting
it rather than after.

**After a roster change, add a `-L1` pass over the main set and one three-shape
class**, which reaches three things a one-shape smoke cannot. `--selftest` skips
a whole block on one shape and says so --- winsorizing, the A/A identities
and the baseline identity, none of which is an identity of anything until there
are shapes to be one over. Every registered `--pair` line goes unrun, and one
re-aimed at an arm the run does not carry fails only when someone runs it.
And `--block`'s per-shape line is guarded by `len(shapes) > 2`, so it is dead
on a one-shape file --- a guard that hid an edited line of this reader through
a whole smoke sweep. Which class serves, and why `scaled` is the default,
is in `smoke-l1.sh`'s header, step 12 being that script.

Its numbers go nowhere, this pass being a test of the reader and
not a measurement; it is recorded on an `L1 ROSTER PASS:` line, and a second
session owes the pass only if none is there. Its artifacts are `smoke*`
for the rule [above](#making-a-major-benchmark-run) --- no probe takes the run's
prefix --- and for the smaller reason that a `$R-l1-main.json` left beside
the pair would refuse the very run the pass was run to clear.

**"Roster change" here means membership, and the test is `--list`**:
the binary's listing differs from what the previous run's did, in its set
of names rather than their order. Criterion emits it sorted, so an arm moving
slot cannot produce a false positive --- which is the only thing making the test
sound and is worth knowing, since order *is* a change, of the kind
[Provenance](#provenance) deals with rather than this pass. An edit
to the reader or to a property is not a roster change either, though the three
reasons above are worded in their terms because a roster change is the only
thing that has ever broken them. What the test cannot usually do is run itself:
the previous run's binary is deleted and its listing recorded nowhere,
so the comparison is against the roster delta under [Provenance](#provenance)
--- look before taking that route, since a pair whose artifacts have
not been offered for deletion yet is still on disk and answers directly, which
is kept for exactly this. A run whose basis half *is* the previous run's binary
answers it outright instead, and the pair note records the count on both sides.
With membership unmoved the pass is not owed however much else changed.

**What 12b catches and what it does not.** A session re-reading its own
registration catches most of what slips past every gate --- a wrong kill margin,
a figure on the wrong arm, a population asserted where it was not evaluated,
a prediction off by a factor, a wrong cause, an interpretation in a block
of observations --- and reads past a figure taken from the wrong position
of a length-ordered series, a compressed clause false as written, and a count
a diff of definitions cannot see through a call. Those three are why it is
not a substitute for post-run step 6b's independent reader.

**A paired Run has one gate more, and the first thing to do about it is read
rather than run it. The gate belongs to the pair, not to the session**, which
is what stops it being paid for twice: re-running it on a pair that has passed
costs quiet minutes and can only reproduce what the note says, and a rebuild
that comes out md5-identical inherits it where one that does not --- a changed
`Main.hs`, a changed regime --- needs its own. The grep is case-insensitive
and not anchored on the `GATE:` token because a note written by hand says
it in prose, and grepping for the token finds nothing in one, which reads
as *no gate* and costs the quiet minutes it was meant to save. **The newest
`GATE:` line is the answer**: `run-gate.sh` appends its mechanical block last,
clean or FAILED, and no verdict is written above it by hand.

**If that line says the gate has not run**, it is the last thing before
the evening --- but it is not part of the preparation, and a session preparing
the run does not reach it: it spends minutes of quiet machine, so it lives
in the run list behind the go-ahead with the sequence itself, as the driver's
first stage. `run-gate.sh` checks that both binaries list every arm
its selection names over the `rev` class, then takes `list`, `bq-expand`
and the two `sum-only` halves over that class's three views from each half,
twice each, in a palindrome --- control, basis, basis, control --- so that drift
over the run cannot read as a difference between the binaries, and **both passes
are read, which is what the palindrome is for**: the `a` pair puts the two
halves next to each other early and the `b` pair late. What it buys is finding
out that a binary is wrong before the hours are spent on it, and **the one
repetition of a process on either half inside the run**: the four readings say
how far each half moved between its own two legs, which is how Run 41's
`bq-expand` outlier was read as that build's and not that process's, both passes
agreeing. **It refuses on the apparatus and never on the world**: a missing
binary, a selection that is not the arms it names, a nonzero exit, a half
that asserted no heap state or an instrument switched on and absent from the log
makes the night's data unusable whatever the machine does, while a box
that measures differently is the machine check's, below, which stops nothing
(ruled 2026-08-23, a machine check having stopped a run and cost the hours
it was meant to save). **Why `rev` and four arms, ruled 2026-10-05
by the owner**: `rev`'s three views carried Run 41's `bq-expand` outlier
in about five minutes where the main set took thirty-three, while `scaled` reads
`bq-expand` level on every run and would have missed it; `list` is the baseline
and the two `sum-only` halves the forcing pass every net is corrected by. **What
it does not buy is a magnitude**: a gate is a rehearsal over three views,
and the pair's figures come off the run; nor is the two passes disagreeing
a second opinion about the binaries, their ratio being algebraically the ratio
of the two same-binary readings, so a palindrome that fails to converge
is reporting its own noise. **And no verdict is written on it** (retired
2026-10-05 by the owner, the hand-written verdict having read SOUND on every run
from Run 24 to Run 45): the four readings are the write-up's, quoted
in its Provenance. **The machine check is not the gate's, and asks one question
that is not a reading at all: has the machine changed?** `run-evening.sh` runs
`./read-run.py $R-<basis>-main.json --machine` after the sequence, as stage 17a,
and puts the answer in `$R-evening-out.txt` and a line of
it in `$R-evening.txt`. It holds `list`'s net per call, shape by shape,
to the fingerprint the last run's file keeps, so its absolutes are in `runs/`
long after its JSONs are offered for deletion and nothing has to be kept for it;
the main set carries `*/list` and both `sum-only` halves on every shape, which
is what makes the comparison net against net, and the gate's one class does
not hold the fingerprint's shapes, which is why the check is not the gate's.
It reads the geomean rather than a cell, at a threshold the mode's own docstring
derives from every kept process this README has, and beside it the per-shape
residual about that geomean, which says whether the shapes moved together:
inside the band a single shape ordinarily wanders it is a LEVEL SHIFT, one
number describing the box, and every cross-run ordering survives it; outside,
the orderings are in question along with the level. **Neither stops the run,
at any size, in either direction.** A box that moved between runs cannot reach
a within-run comparison, and every claim here is one; what it reaches
is the cross-run absolute column, which re-baselines by itself, each write-up
replacing the fingerprint it reads. So a move is recorded and the evening
proceeds, the write-up owing a paragraph naming it and the box question going
to a person once the machine is free: **ask whether the box changed** ---
a kernel, a microcode update, a BIOS setting, a thermal state, a different
machine --- none of which a run can see from inside itself, and none worth
a night of idle machine to ask. What the stage still records as a complaint
is a comparison the mode cannot make at all --- no shape of this run
in the fingerprint, every `list` net non-positive.

**The run** is one sequence --- the main set from each half, then each
stride-class population on each half, control then basis, adjacent,
in `classViews`' order. Each `$c-` argument selects a class by name prefix,
the prefixes being disjoint by construction (`bcast-` does not match
`bcastmid-*`); one process per population is the recorded protocol
at `classBenches`, so no population's figures owe anything to another's leftover
heap state and each JSON is single-population by construction. It leaves
`$R-<half>-main.json` and `$R-<half>-<class>.json` for every class on both
halves, each with a `.log` beside it, and `$R-wallclock.log` over them all;
the gate's `$R-gate-*` and the riders' `$R-al-*` are not among them
and the relaunch guard excludes both. **The regime is a variable
of the procedure, not a flag to remember**: `REGIME` is set beside the run's
name and goes to each half's build, so that leaving it empty is a deliberate act
rather than an omission --- an empty `$REGIME` is a plain -O1 build that every
gate here passes, since no check mode takes a regime, where an empty `$R`
is loud, the drivers refusing without a name. It is the bare GHC flag and
not a `--ghc-options=` spelling of it, because a recipe composes it
with a `-pgma` of its own; its value begins with a dash, so it goes inside
the quotes --- `--ghc-options="$REGIME"` --- and never as a bare word after
a space, which the option's parser reads as the next flag. Each tool call gets
a fresh shell, so both are re-set at the head of every command. A run made
in the wrong regime is not detectably wrong --- the roster, the shapes,
the gates and the reader all pass, the JSON records no compiler flag,
and the only symptom is the regime's own effect failing to appear, which reads
as a refutation of the design rather than as a missing flag; the `diag` reading
at step 9 is the whole guard, which is why that step is not optional. A session
starts in `~/r/horde-ad`, which leaves *that* repository's `CLAUDE.md` resident;
this directory's own `CLAUDE.md` says how far it binds here, and where the two
differ this file and `read-run.py`'s docstring govern.

**`run-major.sh` is that sequence as a driver**, `$R` its argument rather
than a variable it inherits, and the evening's third stage. It refuses without
one, the prefix being the run's identity, and refuses to start where that name
already has artifacts, since relaunching would overwrite hours in place ---
**which makes an interrupted sequence a hand job; expect that, since the machine
gets wanted back.** It has no resume once a process has started,
`run-evening.sh --from sequence` refusing any log or JSON of the run,
so a sequence whose main sets landed and whose classes did not is finished
by running the class loop yourself, with the skip-and-count discipline step 17
spells out; one process per population is what makes a run in two windows
harmless, each carrying its own controls and gates, but it is a fact about
the run and the run file states it. What the driver adds over the pasted
sequence it replaced is the counting, and its header says how: every process's
bench count against the binary's own listing, loud in the log and not fatal,
the exit status carrying the count of complaints out to whatever collected it.

**Nothing is armed beside the evening, ruled 2026-09-23, and `run-heartbeat.sh`
stays for a probe watching itself.** The evening is a backgrounded job whose
exit wakes the session, and that is enough: an evening has run seven hours
with no monitor and no pending wake-up, untouched. What a monitor bought
was a prompt cache kept warm, and over eight hours it costs more than it saves:
a monitor lives at most THIRTY minutes whatever its `timeout_ms` asks, and each
tick and each re-arm is a wake-up costing about a tenth of the one cold read
at the evening's exit, so the wall-clock log's per-process stamps and two
re-arms an hour come to several times that read. For a probe of an hour or two
the arithmetic turns, and `HEARTBEAT_ONCE=1 ./run-heartbeat.sh` is the line
a timed waiter prints at its wake-up.

**The harness reaps a backgrounded job on memory STALL and not on free memory,
which is why the evening launches
with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1`.** Read out of the harness
binary on 2026-09-18: its reaper listens for the kernel's stall counter
`/proc/pressure/memory`, fires at 150 ms of stall inside a 2 s window, and kills
a tracked task once the session has been idle for thirty minutes, reading
no free-memory figure. A stall here comes from pages evicted under earlier
pressure and touched again, so it can fire with most of the memory free,
as it has mid-sequence with 43 GB of 64 free. `run-evening.sh` refuses to start
under the harness without the switch. A launch detached under `setsid` survives
the reaper and loses the harness's wake-up at exit, so it is not the workaround.

Everything else is already a default. The allocation fit
`--regress allocated:iters` is on (it is well-conditioned at 5s), so `alloc`
comes out of the same process as the times rather than a side run; passing
`--regress` explicitly would replace it. Each process prints its own provenance
to stderr as it finishes --- roster size, shape count, wall clock and the two
heap peaks --- so a document quoting its scale copies a measured number rather
than counting benches by hand, and so `micro.cabal`'s `-M8G` headroom claim has
a current source; the stderr redirect above is what keeps it.

**Check what a filtered selection actually selected.** Criterion takes one
`-m MODE` and then its patterns positionally, so `-m glob A -m glob B` matches
*nothing* and the process exits at once --- which looks exactly like a fast run
and cost one probe here before the zero timings gave it away. Counting
the `benchmarking` lines against what was asked for
is the prove-a-search-non-vacuous rule applied to bench selection, and the same
count catches a pattern that silently caught more arms than intended;
the drivers do it for every process of theirs, and every filtered probe made
by hand is where nothing counts on the runner's behalf.

**And the sharper form of the same rule, for the checks themselves: A STAGE
THAT CANNOT FAIL IS A STAGE NOBODY READS.** *Prove a check non-vacuous* asks
whether a check that CAN fail does; this asks the prior question, whether
it can. A stage that only reports looks exactly like coverage and is not,
and the two are told apart by one question --- what input would make this print
a finding? If none, it is a reading dressed as a gate --- as a sweep that prints
which modes refused, and reads a leg whose *every* mode refused as clean, is;
so `smoke-l1.sh` splits the modes into the ones that gate and the ones
that are named, by leg, a class file and a main-set file owing different modes.
The same shape is worth suspecting wherever a script's output is a list rather
than a count: the counted-work sweep's `!!` lines, a driver's per-process
summary, and any step of this chapter whose only product is a paragraph
in the write-up.

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

**Run nothing else on this machine while the sequence runs.** Every strategy
of a population shares that population's process precisely so its figures
are commensurable, and the [noise floor][floor] section is the measured evidence
that they move with what shares that process; what the rest of the machine does
on top of that is unmeasured, and a recorded run is the wrong place to find out.
The session's own hands stay off the tree too, the driver's git lines being
the binary's provenance, which an edit under a running sequence falsifies.

The wall-clock file is why the script stamps each process: a criterion log
is timestamped only at the end, so without the window there is no way to say
which shapes an intrusion exposed, and a suspicious cell can then be neither
blamed on it nor cleared of it. The exit codes ride along because a class
process that dies mid-sequence otherwise leaves a truncated JSON behind a green
scroll-back.

**The run's registered predictions** ([the open list][open]) say what this run
was for and what would kill each one, and are read while the whole evening
is still ahead of you, at step 13a and before it is launched; their verdicts
are written beside them once post-run step 5 has moved them into the run's own
file. **An empty registration does not hold the run.** Where a run has none,
note the absence and read the outcome against its queue entry instead. What
is not open is registering afterwards: the point of the list is that it predates
the hours, so the choice here is to register before the evening or to do
without. **A count of what held is read off the items rather than tallied
from memory**, or a lead summarises registrations not yet adjudicated.
**And a verdict is written in a fixed vocabulary, because a checker reads it**:
`--check-doc` holds a registration's marker to its items --- numbered `1.`
at the start of a line, or `(N)` inline before an italic label, a number's spans
grouped so that stating a question and later adjudicating it under one number
reads as one item --- so an `OPEN` entry whose every item is adjudicated
is reported as a stale marker and an `ANSWERED` one with an item that is
not is reported as an incomplete adjudication. What it recognises is a **bolded
span whose first sixty characters carry one of** ANSWERED, REFUTED, HELD, BROKE,
BROKEN, FAILED, SPLIT, KILLED, TAKEN, DELIVERED, PAID, CLEAN, SETTLED, RETIRED,
SPENT, UNUSED, NULL or WITHDRAWN --- both house styles pass,
the label-then-verdict `*The flag's cost.* **KILLED, ...**`
and the paragraph-opening `**The condition was met and the debt is PAID**`.
**A verdict written outside that vocabulary is invisible to the check**,
so a new word is added to `VERDICT_WORDS` in `read-run.py` in the same edit
that first uses it, or the item reads as unadjudicated for ever; the check keys
on the word, not on its capitalisation. **And say what a partial outcome is**:
a prediction registered over several arms can come apart, and neither "held"
nor "refuted" is then true. Report that as a split, name which arms went which
way, and carry the consequence for each separately; the temptation is to round
it to whichever answer the majority of arms gives, which loses the finding.

**After it lands**, in this order:

**The post-run half as a list, for the same reason the pre-run half has one.**
Its steps below are the prose's own numbers, so a reference to one of them still
lands in both places --- which is a thing to KEEP true: renumber the list
and the prose's items move with it, or a reader following a pointer arrives
at the wrong reason; the prose is where the reasons live and is not replaced
by this. What it replaces is reading those paragraphs three times to be sure
nothing was missed, which is what they have cost. Execute this list, and open
a step's prose by its `why: --para` pointer when the step's rule is unclear,
not otherwise.

    ./read-all.sh $R --brief-facts                    # 1. GATE EVERY
    #      PROCESS -- and EVERY gate on this list is run BARE, as
    #      post-b's `A GATE IS NEVER FILTERED`, after 8b, says.
    #      PROCESS AND DERIVE THE HEAD'S FACTS IN ONE CALL -- no bare
    #      `./read-all.sh $R` beside it: the window and its timestamps,
    #      the plateau band, BOTH floors per population, `list` against
    #      the 0.7% bar per population, the A/A processes past 5% and the
    #      sunk cells -- the rows Provenance's gate and window paragraphs
    #      and Results' floor and differencing paragraphs are written
    #      from.
    #      EVERY PROCESS IS BOTH HALVES of every population, a line apiece
    #      with the A/A WORST CELL beside it. READ that column: it is the NET
    #      ratio, the quantity the published floor is taken on, and neither
    #      the pair's geomean nor the gate. A failed gate invalidates that
    #      population's whole time column and only that one. Note this
    #      run's floor for the run file's Results, which step 5 makes. Read
    #      $R-wallclock.log FIRST.
    #      On a run carrying the preamble it also gates THE PLATEAU, off
    #      the logs rather than the JSONs: every recorded process's own
    #      @@saturate reading inside 5% of the run's own readings.
    #      why: --para 'Gate every population on the correction'
    #      The bare-gate rule is named at the first step that runs one, the
    #      foot being four hundred lines away: a gate read through a pipe
    #      or a refused redirect reads `RC=0` on a failure. The flag rides
    #      the same invocation and the facts come off the readings just
    #      taken, so a bare `./read-all.sh $R` would gate every process a
    #      second time for nothing; a session that skips the facts
    #      re-derives them by hand at 6a. Every margin is judged against
    #      the floor. A wrong bench count is logged loudly and is not
    #      fatal, so nothing else stops on it. A process outside the
    #      plateau band measured in a state the others did not, and every
    #      other gate here is WITHIN one process and cannot see it
    ./read-run.py $R-<half>-<pop>.log --wild          # 2. and, on an
    #      instrumented run, the per-sample stamps that log carries:
    #      allocation, mutator, collector and in-use per bench, and the
    #      foreign CPU during its samples. Step 4's post-run-readings.sh
    #      takes it over every log, as wild-LOG.txt; read a log's own
    #      table when a cell in step 1's worst-cell column wants
    #      explaining.
    #      THE `fgn/core` COLUMN IS A RATIO OF ONE CORE, NOT A PERCENT,
    #      and at or above 0.25 the reader calls it an INTRUSION and
    #      says so in one line at the foot of the table. READ THAT LINE
    #      BEFORE STEP 5
    #      why: a rerun is cheaper than a second write-up.
    #      A rerun costs one population's evening; a write-up derived
    #      twice costs the session.
    #      The foreign CPU is what tells a WILD CELL from an external
    #      intrusion -- both being a moved mutator clock at flat RTS
    #      totals, and the difference being whether anything else was
    #      running.
    #   3. if 2 names an intrusion, RERUN the populations it touched,
    #      BOTH halves of each, a clean half with its exposed twin. ASK
    #      FIRST -- UNLESS the note's `RERUN:` line answered already:
    #      `allowed` reruns at once, `no` puts the sensitivity reading in
    #      its place.
    #      SIZE EACH EXPOSED CELL ON BOTH CLOCKS whichever way it goes:
    #      `./read-run.py $R-<other>-<pop>.json --compare
    #      $R-<basis>-<pop>.json --cell SHAPE/ARM` prints the corrected
    #      net the tables use and the mutator clock `--wild` reads
    #      A process costs what ITS OWN population costs, not what a main
    #      set does -- 42 minutes a process on `runs` at 490 benches. Two
    #      rules: the rerun window is quiet FOR THE DRIVER TOO, reading
    #      this run's own logs during it being enough to void a process;
    #      and drive it through `./run-major.sh $R POP...` rather than
    #      by hand. Park what it supersedes as probe-*
    #      why: a pair read across two windows is not a pair.
    #      A rerun wants the box quiet again, which 19a gave back.
    #      run-major.sh takes the populations to rerun and narrows its
    #      relaunch guard to what they would overwrite, its launch line
    #      carries WILDLOG and SATURATE, and its guards catch a process
    #      that lost them: a process at rc=0 with no stamps in the log
    #      looks perfect and certifies nothing. read-all.sh globs
    #      $R-*.log for the plateau and lists by name any log it finds no
    #      reading in, so a superseded copy left in that namespace fails
    #      the gate
    #  3a. NAME THE FILL GROUPS off a -g3 twin, and spend the other
    #      load-independent measurements while the artifacts live --
    #      allocation, Core, a `size` invocation, minutes each, and all
    #      of it before 9 spends the binaries. THE TWIN'S BUILD RUNS
    #      BESIDE step 20's counts where no rerun is owed.
    #      Owed by every paired Run: rebuild each recipe with -g3,
    #      `./g3-twins.sh $R` reading both off the note, export
    #      the NAMED fills into the note, match groups by byte identity
    #      of the loop body and never by proximity, and read the count
    #      check -- a group whose twin carries fewer copies than the
    #      timed binary is not named from the twin at all.
    #      `../../horde-ad/tools/loop-offsets.py $R-<half> --match probe-g3-<half>-$R` does
    #      the straddlers' half of that by the same rule, naming each by
    #      its bytes and saying NOT NAMED where no twin holds a copy.
    #      GIVE IT BOTH TWINS, the half's own first, and add --loose.
    #      --loose then offers a register-masked signature for what the
    #      bytes refuse, and it prints a FAMILY rather than a name:
    #      read it only where the family has one member or the rest are
    #      already anchored.
    #      NOT NAMED can also mean no loop, and `reaches` in
    #      loop-offsets.py has the tell of all three shapes. THAT REFUSAL
    #      is not a shortfall to work around.
    #      WHERE THE PREPARATION SPENT THIS HALF EARLY, RE-RUN THE
    #      `--match` OFF THE BINARIES YOU TIMED, which is two minutes
    #      why: --para 'Name the fill groups'
    #      EARLY because it is the only step whose window CLOSES: it
    #      spends the binaries, and every step below it can be taken
    #      afterwards from the JSONs and the two documents. It does not
    #      wait on the gates either, reading the binaries rather than the
    #      measurements, which is what lets it go here. Its compiles are
    #      the one thing on this list that loads the box a rerun would
    #      want quiet; beside the counts they cost nothing, an instruction
    #      count being insensitive to load.
    #      The naming is what the step is FOR and reads like housekeeping:
    #      it turns `[0, 24, 0, 4]` into four arms, which is the only form
    #      in which an offset this README quotes can be tied to one.
    #      Both twins: the compilers emit many of these bodies alike, so
    #      the other half's twin names what -g3 destroyed in this one, at
    #      no build. THE REFUSAL IS WHAT MAKES A NEGATIVE HONEST.
    #      The re-run turns the note's block from a transcription into
    #      evidence: the twins are kept beside the binaries for it, the
    #      preparation's own reading was taken on an idle box a day
    #      before, and a note's fill-in block is where transcribed
    #      figures live
    #   4. match bases before reading any ratio -- same population, same
    #      restriction, the basis the claim was stated on;
    #      one JSON at a time, never merged; a sentence comparing
    #      populations compares their tables
    #      READ NOW: item 9's execution half of read-run.py's docstring
    #      -- the statistic definitions, the A/A identity and the modes
    #      that read a run's figures -- and reading items 5 and 6 HERE,
    #      off the previous run's own file, whose properties section and
    #      class blocks this step's readings are about to replace: which
    #      properties are live and how many, and the six-part form of a
    #      class block. `--section 'The properties the next run should
    #      test' --run-doc runs/$PREV.md` and `--section 'The stride
    #      classes, run by run' --run-doc runs/$PREV.md` are the reads
    #      why: --para 'Match bases before reading any ratio'
    ./post-run-readings.sh $R        #    EVERY READING OF 4, 4a, 4b AND 4c,
    #      in parallel, a file each in log-read-$R/, the script's header
    #      naming which file holds which; the count-dependent ones only
    #      once $R-evening.txt reads EVENING COMPLETE, so it is run again
    #      then
    #      AND `--compare` PRINTS THE REDUCING CONSUMERS UNDER ITS TABLE,
    #      on raw `slope`. NEVER QUOTE THE TWO IN ONE COLUMN, ROW OR
    #      TABLE. `--predictions` reads a `cross` prior on those arms
    #      the same way, and a `-sum` figure wants no hand-written geomean
    #      EVERY CLASS IS READ ACROSS THE HALVES, and on each half
    #      against the other, which is how a `pair` span is read within
    #      the control half.
    #      --alloc --per-shape takes the same pair where allocation is the
    #      question, and the `--per-shape` half is the one to read; the
    #      `alloc` column cannot give it -- a median over shapes, not to
    #      be divided across halves. post-run-readings.sh takes this form
    #      into main-alloc.txt.
    #      and `--exclude ARM` composes with `--compare` as it does with
    #      the default table, which is how a cross-half geomean is taken
    #      with an arm dropped.
    #      IT DROPS AN ARM AND NOT A FAMILY, repeatable being the whole of
    #      how a family goes, so a family wants its twins named too
    #      READ THE BLOCKS BY THEIR LINES AND NOT WHOLE: pipe them
    #      through `grep -E 'Verdicts|property|Across the halves|floor'`
    #      -- AND THE SAME FOR `--wild` AND `--aa`, whose answer is one
    #      line: `--wild`'s `reaches 0.25 foreign` line, which is the
    #      intrusion verdict, and `--aa`'s `observed spread` line, which
    #      is the FLOOR and is not read-all.sh's worst-cell column
    #      -- and its `sum-only` row prints LATE over EARLY
    #      THE SAME FOR THE PREDICTIONS AND COUNTS FILES, the first by
    #      `grep -E '^ {2}\(|span\(s\)'`
    #      floor-pairs.txt IS THE STANDING floor-pair registration in one
    #      call: every A/A copy against its original, per population and
    #      half, with each population's floor and the pair that carries
    #      it
    #      main-<half>-deflation.txt, on both halves: THE DECOMPOSITION
    #      IS PROVENANCE'S and is taken here with the rest, 4c reading
    #      it
    #      AND THE BAR THE CROSS-HALF FIGURES ARE READ AGAINST comes off
    #      the plain `--compare` file, which prints how far an arm and
    #      its own A/A duplicate part IN THAT COMPARISON and names the
    #      arms that move further. READ IT BEFORE WRITING THE HEAD.
    #      `--winsor` is the same caution per row, the published column
    #      against its own uncapped geomean, and the same `--compare`
    #      flags a row whose two published figures divide to something no
    #      arm did
    #      AND `--winsor`'s CLOSING LINES CENSUS THE SIGN PARTINGS over
    #      every pair of timed rows and NAME the pair that parts with both
    #      its figures, so that count is read and never scripted
    #      POP-<basis>-compare.txt takes the BASIS first and the control
    #      as its argument, so below 1 means the basis is faster;
    #      POP-<other>-compare.txt is the same reversed, every figure
    #      inverted. Write each class paragraph from --block's VERDICTS,
    #      never from its table, one paragraph each. Do not write a second
    #      reader
    #      why: --para 'The properties are part of this'
    #      The reducing consumers run no forcing pass, so their net is
    #      that term subtracted from itself and the table above skips
    #      them; a corrected net over a corrected net and a raw slope over
    #      a raw slope are different quantities, and a table holding both
    #      says neither. A prior and the block agree by construction.
    #      A pair's variable can act on a class and not on the main set.
    #      The plain --alloc form counts cells inside 1e-4 and names the
    #      worst, which says whether the halves AGREE, where a pair whose
    #      variable moves allocation wants the size PER ARM; a hand
    #      computation of it once took an absolute deviation, so
    #      `2 - ratio` reached the page on one arm.
    #      --exclude is what says WHOSE a movement is when one family
    #      carries it: `--exclude list --exclude bq-expand` takes 18 arms
    #      to 16 and not to 12, the four A/A copies staying.
    #      The --wild and --aa tables run to hundreds of lines; every
    #      block in one call is a hundred KB, the write-up uses some forty
    #      lines of them. LATE over EARLY is the orientation a hand
    #      computation reverses, putting reciprocals on the page.
    #      The --compare bar is the counterpart of the floor `--aa` gives
    #      WITHIN one half, and the thing a pair's headline is read
    #      against. A census scripted from the mode's two columns, the
    #      table read and not the closing lines, gets the count wrong.
    #      Nothing in the reversed compare file's output says it is
    #      inverted
    #  4a. THE HALF-LOCAL MOVERS, each half against the COMPARE run's
    #      same half over every population, BEFORE any cross-half
    #      figure is attributed to the pair's variable, AND AFTER
    #      $R-evening.txt reads EVENING COMPLETE, its counts columns
    #      reading `--` until the counts have landed:
    #      half-movers.txt, at a 3% bar; `./read-run.py --half-movers $R
    #      --movers PCT`
    #      sets another.
    #      An arm it flags with its counts level is that half's binary or
    #      its FILE INSTANCE and not the pair's. For each flagged arm, the
    #      COPY TEST first, on a box asked quiet (19a) or taken at once
    #      where the note says QUIET-AFTER: allowed: `./copy-test.sh $R`,
    #      which takes one cell per population and half off
    #      `--copy-cells` and times it on the timed file, a fresh copy and
    #      the previous run's half, read with `./read-run.py --copy-test
    #      probe-copy-test-$R.log` -- INSTANCE, PROCESS or BUILD per cell;
    #      then, where it says INSTANCE and BEFORE anything evicts
    #      the file -- a reboot, a copy over it, the fadvise -- the frames
    #      off the slow instance while it runs:
    python3 ../../horde-ad/tools/probe-pageflags.py <pid> <addr of the hot line> --heap   # as root
    #      which prints the code frame beside the heap's; its header says
    #      what PID and VADDR are
    #      why: --para 'The physical frame of a code page is a placement term too'
    #      Nothing else in this list sees the term, the A/A pairs sharing
    #      the binary and the counts the code. The frames printed side by
    #      side mean the bits they share are read and not guessed
    #  4b. EVERY CELL ACROSS THE HALVES, time beside counts over every
    #      population, ranked by what the counts do not explain:
    #      cell-movers.txt, step 4's, 20 rows; `./read-run.py --cell-movers
    #      $R 80` takes
    #      more. Read the rows in three kinds. COUNT-LED: the codegen's,
    #      and on `lib-stage2-lean-u1` the known offender, the latch of
    #      GHC https://gitlab.haskell.org/ghc/ghc/-/work_items/27799 on a
    #      rank-1 view, which the mode names under the table.
    #      TIME-LED with counts level and the arm's twins agreeing: one
    #      half's binary, file instance or process -- the copy test of
    #      4a and the cell timed in a fresh process tell those apart.
    #      TIME-LED with the twins parting: bench position.
    #      why: --para 'latch keeps its fall-through only where the block'
    #      4a and every table above read ARMS, and an arm is a geomean
    #      over its population's shapes: a cell at 1.25 among seventeen
    #      is an arm at 1.01, under every bar in this list, which is how
    #      Run 34's record missed cells at 1.23 with counts level and
    #      the latch's count differences, the run's largest.
    #      WHAT THE READING FOUND ON RUN 34 ACROSS ITS HALVES, kind by
    #      kind with the instrument that settled each, basis over HEAD,
    #      read at 80 rows; the reducers' `-sum` cells on two- and
    #      three-element runs head the table, the three-element ones the
    #      known term the mode names, and are left out here:
    #        count-led: `lib-stage2-lean-u1` on compose-scalar 1.0714
    #          and on flip-whole-square and scaled-rank1-m1 0.9412,
    #          time level -- the latch above; `lib-stage1` on
    #          cnn-L1-24x24-c1 and its `rev` view, 1.12 in time on
    #          1.03 in counts, three instructions of a hundred a run on
    #          a per-run-bound cell and the same in Run 32 -- codegen
    #          in stage 1's own per-run path
    #        time-led, counts level, twins agreeing: `mut-odo-vecdims`
    #          on compose-zero-mid 1.11 -- one mispredict a run, 18000
    #          an iteration on the basis and none on HEAD, read with
    #          `perf stat -e branch-misses:u` over -n 2N less -n N;
    #          the same family on runs-16384 1.23 -- the evening's
    #          process, all four instances level under criterion in
    #          fresh processes; the leaf `u1` on scaled-rank1-m1 1.24
    #          -- the basis file instance, 4a's copy test
    #        time-led, twins parting: the leaf `u2` on flip-last-rows,
    #          the original 0.91 against its twins at 1.11 and 1.13 --
    #          bench position, the open list's entry
    #        unread: the lean fill and `u1` on cnn-slice-c32 and
    #          cnn-L1-6x6-c1 near 0.89 and 1.13, and `u1` on
    #          cnn-L1-24x24-c1 at 0.87, on the last of which instructions,
    #          taken branches, mispredicts, both branch-target buffers,
    #          decoder redirects, resyncs, op-cache hits and misses, icache
    #          and TLB misses all read level between each half's Run 34
    #          binary and its Run 32 and 33 ones, and what moves, a
    #          quarter, is perf's `r28F`, event 0x8F with umask 2 under the
    #          raw encoding and not the 0x28F the chapter reads as
    #          `r20000078f`; every fill loop of the three
    #          sits at its residue. On cnn-slice-c32 criterion reads it in
    #          fresh processes on a fresh copy of each Run 34 binary and
    #          on neither Run 33's nor Run 32's: a term of that build on
    #          both compilers, some 250 cycles a call, the lean fill and
    #          `u1` moving in opposite directions on each half
    #  4c. main-<half>-deflation.txt, on both halves: the roster cell
    #      over its own alone leg, per shape. RAW over RAW. TAKEN WITH
    #      STEP 4's READINGS, post-run-readings.sh writing it
    #      why: a leg has no `sum-only` to correct with.
    #      A leg carries no `sum-only` to correct with -- the one
    #      place a session would reach for the wrong numerator. It is
    #      what the riders were run for
    #   5. MAKE THE RUN'S OWN FILE, `runs/$R.md`, with
    #      `./copy-run-file.py runs/$PREV.md runs/$R.md`, which masks every
    #      decimal, percentage and run number of the last run's prose as
    #      `{{was ...}}`, AND COMMIT THAT COPY BEFORE EDITING IT
    #      (reading item 2 HERE, off the copy you have just made, which
    #      IS the last run's head and Results prose until you replace it:
    #      one sentence on what this run's own head has to answer).
    #      Every install below writes that file and no other document.
    #      ONE heading takes the number: the file's title, renamed by the
    #      copy.
    #      Then repoint README's links from the run before to this file
    #      with `./read-run.py --repoint $PREV`, which moves every link
    #      into that file but the older run's OWN -- a link whose text
    #      names it, the delta chain's bullet and its `ANSWERED` entry
    #      among them -- and prints each it kept, which is the one list
    #      to read. Repointing is not re-verifying: walk the links
    #      --check-doc lists, and the section links it does not, against
    #      what the file now says
    #      NAME THE PATHS ON EVERY `git add`, here and at 6b, 6d and 7a,
    #      never `git add -A .`, and read the diffstat of the commit just
    #      made, expecting exactly the paths you named
    #      NAME THE STEP IN THE COMMIT SUBJECT, here and at 6b, 6d and 7a
    #      why: --para 'COMMIT THE COPY'
    #      Three reasons for committing the copy first, all of them there
    #      and only one about wrapping.
    #      Both the older run's links and this run's read correctly after
    #      a wrong repoint because `runs/` keeps every run. --check-doc
    #      fails any link that still names the file; no source file names
    #      a run file.
    #      This directory holds scores of untracked scratch files and
    #      `git add -A .` takes every one of them, after which `git
    #      status` reads CLEAN, the files having been absorbed; only
    #      a diffstat of the commit just made shows it. Each of these four
    #      steps commits a different set, so no fixed count is the check.
    #      Those four commits are the only record of which post-run
    #      steps have run, so a session returning to an interrupted
    #      write-up reads `git log` rather than its own memory
    ./read-run.py --move-registration     #  5, second act: this run's
    #      OPEN registration leaves the open list for the run file's last
    #      section, whole and under a one-line preface, and the entry
    #      becomes the ANSWERED stub with `___` for the verdict clause;
    #      the verdicts are then written beside each prediction where it
    #      already stands. It deletes the preparation's pointer to this
    #      registration, which the copy brought across, and names it; two
    #      or more such paragraphs it leaves, each for you to read.
    #      It refuses unless exactly one OPEN entry names
    #      this run, so it is run once, after the copy is committed
    ./read-run.py $R-<basis>-main.json --movement    # 5a. THE MOVEMENT
    #      READING, whose window 5b closes: a "moved from X to Y"
    #      sentence compares against the COMPARE run's file, or,
    #      where the note names none, against the figures the install
    #      overwrites. `--compare` against the COMPARE run's own JSON is
    #      what says how far the ARM moved, and the same with
    #      `--per-shape` which cells carry it
    #      why: 5b overwrites the figures it compares against.
    #      After 5b those figures are in git or in the kept JSON
    #      only.
    #      The mode reads the same two sources the install does, says
    #      which figures are three decimals and which are full, and says
    #      of every row what the chapter says once: a row's movement
    #      between runs is the winsorized column moving -- a reading Run
    #      39 scripted by hand
    ./install-tables.sh $R                            # 5b. install, never
    #      paste: every table, from the BASIS half
    #      into `runs/$R.md`, the one document any of them writes -- so
    #      commit or park it first. Read what the driver collects at the
    #      end, the rows left to hand-fill; the cross-class summary is
    #      installed too, off each class's own block,
    #      in the row order the document already has
    #      why: --para 'Install the tables with'
    ./read-run.py --prose-draft $R --in-place   # 5b too: the rest of
    #      the run file's mechanical prose -- the census, the bar, the
    #      roster, the step, the standings, the properties, the class
    #      lead, the bold and ties, the offsets and the straddlers --
    #      drafted over the step-5 copy with `___` where a reading is
    #      yours, every paragraph written since being kept
    ./read-run.py $R-<basis>-main.json --compare $R-<other>-main.json --predictions --counts $R-counts-<basis>.txt $R-counts-<other>.txt
    ./read-run.py $R-<basis>-main.json --compare $R-<other>-main.json \
      --predictions --in-place       # 5c. THE REGISTRATION'S SPANS, taken
    #      here, after the counts, AND `./install-tables.sh $R` AGAIN,
    #      which places each class block's counts sentence over the `___`
    #      5b's install left and keeps every paragraph written since, as
    #      a second `--prose-draft $R --in-place` does for its own.
    #      WHILE THEY ARE TAKEN, read `--checklist
    #      post-b` once, `--full` only for a step whose reason you need,
    #      then take steps 5d and 5e, which want no counts, and
    #      6a's three readers. Every `predict:` span read on each
    #      population and half its scope names, HELD or KILLED with the
    #      figure read, and written under its item in the run file as
    #      `**Read by --predictions, item (N):**`, a rerun replacing it;
    #      an item carrying a `script:` is that script's to read, and one
    #      carrying neither is yours.
    #      Those readings are not the item's verdict: the verdict is its
    #      KILL CONDITION applied across them, written beside the item
    #      with the population each figure came from. The verdicts and
    #      the tally sentence are the whole of the adjudication left to
    #      judgement
    #      why: it reads the counts, which land last.
    #      It READS THE COUNTS, which the run list launches at step
    #      20 -- after the box is handed back, so on any run whose
    #      write-up starts promptly they are still being taken while 5a
    #      and 5b are done. This is the list's one long wait and the work
    #      that fits it is named rather than left to be found, a session
    #      that fills it unbriefed writing a third of 6a before it meets
    #      step 6.
    #  5d. TAKEN BEFORE 6d AND COMMITTED WITH IT. Collect what
    #      this run made CHEAPER for the next: the checks that
    #      would have caught each error, the computations improvised, the
    #      steps skipped, any capability found, and the readings the
    #      carrier took with what they cost. HALF OF IT IS THE
    #      PREPARING SESSION'S: read the note's WHAT THE PREPARATION
    #      LEARNED block before writing yours and carry both halves.
    #      THE BLOCK GOES TO MARGINALIA, appended there as `What Run N
    #      made cheaper`, and README keeps none: what it asks of the
    #      procedure is made in the chapter or a tool in the same write-up,
    #      which is where the next run meets it (--check-doc refuses a
    #      block left in README). ITS FORM, MARGINALIA BEING WRITE-ONLY:
    #      a bold `What Run N made cheaper` lead, then THE PREPARATION'S
    #      HALF and THE WRITE-UP SESSION'S HALF, each a run of bold-led
    #      items -- written from this, never copied out of the file
    #      why: it feeds 5e and so comes before it.
    #      No other step gathers this, and it is not a figure. The
    #      preparing session met the same list a day earlier and is gone,
    #      so its half reaches you only through the note
    #  5e. TAKEN BEFORE 6d AND COMMITTED WITH IT, as 5d is. Walk the open
    #      list: grep the settled index before adding an
    #      entry, move answered ones with their measurement, and add each
    #      surprise with what would settle it. PREDICTION VERDICTS DO NOT
    #      GO HERE: a run's registrations and their
    #      verdicts live in `What this run was built to answer, and what
    #      it answered` in the run's OWN file, written at step 5 with the
    #      rest of it, and the open list keeps one `ANSWERED` entry per
    #      run -- the lead, a verdict in a clause, and a link to that
    #      file. Report a split as a split, arm by arm
    #      why: --para 'Walk the open list against what this session'
    #   6. walk the replace list under Provenance (READ NOW: item 8, the
    #      list itself and its delta bullets), take the two sweeps it
    #      names over README with `./read-run.py --sweep $PREV` -- the
    #      paragraphs quoting a figure only the previous run's file
    #      carries, and those naming that run -- and map every hit to the
    #      bullet covering it -- running them is not reading them. The
    #      run file's half is --inherited's and --stale's. REPLACE, do not
    #      annotate: a figure that moved inside the floor is requoted
    #      without comment. The
    #      bullets below GOVERN the walk rather than following it, which
    #      is why they are bullets and not sub-steps; 6a and 6c ARE it
    #      * SET THE TURN-END HOLD HERE and clear it at 9, setting it
    #        again for any editing past 9 (~/.claude/rules/
    #        turn-end-hold.md), on ~/r/orthotope by name, `wrap-restore
    #        --hold ~/r/orthotope`, and on any other repository the
    #        write-up edits: a bare --hold holds the working directory's.
    #        read-run.py's --replace, --delete and
    #        --para match the flattened form and want no unwrap; an
    #        EXACT-MATCH edit wants `wrap80 --unwrap -i README.md` first
    #        and again after each of 6b, 6d and 7a, whose commits rewrap.
    #        Never wrap by hand (~/.claude/rules/markdown-wrapping.md)
    #      * REPLACE BY ANCHOR, `./read-run.py --replace ANCHOR --with
    #        FILE`, for every
    #        paragraph edit at 5d, 5e, here and at 6a, 6b, 6c and 7 --- AND ITS
    #        UNIT IS THE BLANK-LINE BLOCK, not the sentence and not the
    #        prose. Read the `out, last` line every time --- AND for a
    #        sentence-level edit too, which is a --replace of the
    #        paragraph the sentence sits in.
    #        WHERE A SCRIPT IS USED ANYWAY, ONE SUBSTITUTION PER FILE
    #        WRITE, matching the wrapping in force, AND THE SCRIPT IN A
    #        QUOTED HEREDOC, `python3 - <<'EOF'`, never `python3 -c "..."`:
    #        a backtick in the prose is a command substitution there,
    #        which loses a span of text without an error.
    #        Quote only what you are EDITING. READ THE `out` LINES AND NOT
    #        ONLY THE `in` ONES
    #      * TWO HALVES IN TWO FILES, 6a and 6c below: the replace list's
    #        FIRST bullet is the run's own file ENTIRE and every other
    #        bullet is a README section
    #      why: --para 'What skipping this costs is measured'
    #      A class block's lead has its installed TABLE on the next line
    #      with no blank between; --replace replaces the prose above a
    #      table that ends the block and keeps the table, and refuses a
    #      table with prose after it, an abutting heading and an
    #      abutting list, but a loss it misses exits 0
    #      with `--check-doc` passing straight after, a gate being a
    #      predicate over what is present. A script that edits inside a
    #      paragraph and misses the wrapping replaces one line of a
    #      wrapped paragraph and leaves the rest; a batch that asserts
    #      between substitutions prints a success line for each and
    #      writes NOTHING when a late one fails. --replace searches BOTH
    #      documents and refuses an anchor found in each; the FIRST of two
    #      replacements can remove the second anchor's other occurrence,
    #      leaving it unique somewhere you did not mean.
    #      The replace list does not look like two halves, so a session
    #      reading 6 as one walk writes a whole document with no step
    #      naming that it did
    #  6a. THE RUN'S OWN FILE (reading item 4 HERE, off the copy: does the
    #      two-column table this half hand-edits carry the last run's
    #      columns?), which is that first bullet and is the bulk of the
    #      run: its head, Results and the findings under it, what the
    #      next run compares against with its two-column table, the
    #      properties, the class leads and paragraphs, its
    #      Provenance and its registrations. Do this half FIRST.
    #      THE TEN CLASS BLOCKS ARE PLACED AND NOT RE-TYPED:
    #      install-tables.sh at 5b writes the table and the five
    #      paragraphs one line each, the two cross-half ones where the
    #      second JSON is on disk, and its rerun at 5c places each
    #      `What the class says:` counts sentence over its `___`.
    #      The `___` left after that are yours and run-status.sh
    #      refuses a run file still carrying one, each saying what it
    #      wants. A sentence of the class's own is optional since
    #      2026-09-25, written only where the class has a finding.
    ./read-run.py --opening $R            # 6a's THREE READERS IN ONE
    #      CALL, --inherited, --stale and --prose-facts in the order the
    #      body gives them, and BEFORE the first paragraph
    #      FIRST, BEFORE A WORD OF IT: `./read-run.py --inherited`,
    #      which names the paragraphs this file carried WHOLE from
    #      the last run's and which claim something about the run in
    #      front of them. Read each: it is the apparatus every
    #      run re-carries, or it is last run's claim under this run's
    #      name. RUN IT HERE AND NOT AT 6d.
    #      AND READ EACH HIT AGAINST THE TABLE BESIDE IT, not only for
    #      whether it names a run.
    #      AND ITS SIBLING, `./read-run.py --stale`: the paragraph this
    #      run DID edit around a count or a number word it did not, the
    #      copy having masked every other figure. Run it TWICE, here and
    #      again after the prose. It prints the twenty most-edited
    #      paragraphs first, which is the ordering that matters.
    #      AND `./read-run.py --prose-facts $R` BEFORE THE FIRST
    #      PARAGRAPH: the figures this half quotes, gathered out of
    #      log-read-$R/ and computed nowhere -- per population and half
    #      the A/A bar, how many arms clear it and the counted work, and
    #      every in-scope span with its verdict.
    #      ONE SITE PER FIGURE: a figure is written where it is derived
    #      -- an intrusion's sizes in Provenance, a class's in its block --
    #      and the head, Results and README point there rather than
    #      requote it.
    #      **THE HEAD IS WRITTEN LAST**, after 5c, in at most THREE
    #      PARAGRAPHS -- the pair and its headline, what the registration
    #      was built to show with its tally, and anomalies -- which
    #      `--check-doc` holds it to: what the next run takes is the
    #      compares-against section's, the counts and allocation are
    #      Provenance's and the properties', and so are the gate, window,
    #      intrusion, repetition, `.text`, regime, straddlers and
    #      decomposition. THE TWO TABLES
    #      ONCE TYPED, the two-column geomeans and the PROVENANCE
    #      ANCHORS, are installed at 5b, their rows by
    #      `--hand-tables`, and their leads and headers are yours; the
    #      same mode without --in-place checks them after an edit.
    #      THE MECHANICAL PROVENANCE PARAGRAPHS ARE PLACED AND READ, NOT
    #      WRITTEN: 5b installs `--provenance-draft $R` over the previous
    #      run's -- the evening, gate, plateau, identity, both anchors
    #      paragraphs, correction, counts, in-situ term, decomposition --
    #      each with a `___` where a lead or a reading is yours; the
    #      delta, straddler and regime paragraphs stay yours whole.
    #      AND PROVENANCE OWES A FIXED LIST besides its anchors:
    #      the run's name and regime, each process's stderr line, the
    #      machine, which half ran first, and THE COMMIT transcribed from
    #      `$R-pair.txt` now. A class line's shape count is the whole
    #      class-view set, so the population size comes from the reader.
    #      The INSTALLED tables went in at 5b and are not touched here; what is
    #      written is the prose around them, one edit per paragraph.
    #      Budget the head and the class paragraphs as the work.
    #      AND STATE THE DIRECTION ONCE, THEN CHECK EVERY CLAIM
    #      AGAINST IT: a `cross` figure ABOVE 1 means the CONTROL half
    #      is the FASTER, `--compare` taking the basis first. Say it once
    #      in the head, and take one cell with `--cells` on one arm on one
    #      shape before writing a sentence that says which half won
    #      WRITE EACH PARAGRAPH FROM THE READER'S OUTPUT AND NOT BY
    #      EDITING THE PREVIOUS RUN'S. A PARAGRAPH DEFERRED until a
    #      measurement lands carries `[[TODO]]` in its place, which
    #      --check-doc refuses until it is written
    #      why: --para 'commit the binary was built from'; 6b requotes it.
    #      FIRST, and not for tidiness: 6b's figures are requoted FROM
    #      this half.
    #      A script joining the wrapped form can split an arm name at a
    #      break, `lib- stage2-lean-u1` reaching the page -- an arm name
    #      that renders wrong, matches no row of the table above it and
    #      answers no search for the arm. The counts-against-clock clause
    #      is written by --block where both count sweeps are given.
    #      --inherited finds the one class of defect neither checker
    #      pass can see -- their diff base is step 5's copy, so an
    #      untouched paragraph produces no diff line at all -- and it is
    #      cheap and easy to skip. After the prose is written every hit
    #      is a rewrite. A paragraph describing an INSTALLED table's shape
    #      is apparatus by its wording and this run's claim by its
    #      content, and 5b has already replaced the table under it: such
    #      hits read as apparatus, go in, and only the independent checker
    #      finds them.
    #      --stale reads the other half of the same defect. Neither
    #      checker pass sees that either -- an edited paragraph is in the
    #      diff and the numeral that survived inside it reads as context.
    #      Here it says which figures the copy will hand you, and after,
    #      which ones you let through. A paragraph 99% identical to the
    #      copy has barely been touched.
    #      Finding the --prose-facts figures by grep costs a third of this
    #      half's tokens and makes transcription errors.
    #      A figure quoted in several places has every correction find
    #      all of them, and readers still find them disagreeing;
    #      `--check-doc`'s agreement checks are for the figures that
    #      genuinely live in both documents, not a licence to copy.
    #      The head is the only section that generalises over the others,
    #      so written first it generalises over figures not yet
    #      adjudicated. The class blocks, the registration verdicts and
    #      Provenance are mechanical and settle their own figures; the
    #      head then summarises settled ones. A stale anchor row passes
    #      every gate and a whole checker pass while --machine resolves
    #      its fingerprint off it. The note goes with the pair at 12, so
    #      the transcription cannot wait. No tool reduces the paragraph
    #      count.
    #      The reader prints the direction's key in every table header and
    #      in no verdict. Prose is where it goes wrong, past an end-to-end
    #      read, and `--cells` settles a direction in one line where a
    #      legend re-read does not.
    #      Writing from the reader's output is the prose counterpart of
    #      `install, never paste` and bites harder: a table is replaced
    #      whole and a paragraph is edited in place, so a clause whose
    #      numbers you did not touch survives inside a sentence whose
    #      other numbers you replaced. A deferral with no marker is
    #      forgotten.
    #  6b. COMMIT 6a'S WORK IN ONE COMMIT, subject naming THE RUN AND THE
    #      STEP and not the work it commits -- `Run $R step 6b: ...`.
    #      START the checker's first pass on it, an agent in the
    #      background; THEN do 6c beside it. THAT COMMIT'S DIFF IS WHAT
    #      THE AGENT WORKS ON -- not the working tree, not a range.
    #      README's step-5 repoint and whatever of 6c is already written
    #      GO IN THE SAME COMMIT. PRE-AUTHORIZED by the user-scope
    #      CLAUDE.md and not a thing to ask about.
    #      ONE AGENT, TWO PASSES: this is the first and 6d the second, on
    #      the SAME agent; the checker REPORTS ONLY and edits nothing.
    #      FIXING IS THIS STEP'S OTHER HALF and not 6d's.
    #      IF THE PASS HAS NOT RETURNED BY THE TIME 6c IS DONE, COMMIT
    #      6d ANYWAY and fix both reports at 7
    #      AND SEND PASS 2 THE MOMENT PASS 1 LANDS, wherever that falls
    #      -- beside 6e if it lands there -- rather than carrying it to
    #      7a. Pass 2's condition is on pass 1 RETURNING and not on 6c being
    #      done; two agents at once, never three.
    #      KEEP CHAPTER EDITS OUT OF THE WRITE-UP'S COMMITS; where they
    #      have already happened, bound README's diff at the run's own
    #      last commit, the brief's RUNTIP, given in the launch message
    #      and advanced in the brief afterwards as a record.
    #      THE BRIEF IS `checker-brief.txt`, and its two THIS RUN ONLY
    #      items are PASTED FROM `log-read-$R/for-brief.txt`, which step
    #      4's post-run-readings.sh writes last, rather than retyped --
    #      and `./read-run.py --brief-update $R` DOES THAT PASTE. It
    #      writes the two items and the substitution block's RUN, BASIS,
    #      OTHER, PREV, PREVBASIS and PREVSAME, counts every `<yours>`
    #      slot it left, and does NOT write PRETIP or RUNTIP, which are
    #      commits and yours. The two items arrive with every figure an
    #      artifact can settle already in place, the class views landed
    #      since PREV among them, and the two `<yours>` slots filled where
    #      the note's recipes and the run file's head lead say them: a
    #      slot it leaves is a pair its recipe diff cannot state, or a
    #      head not yet written.
    #      EDITED EVERY RUN BEFORE EITHER PASS IS LAUNCHED. Its head says
    #      which three things change; WALK THE FILE, NOT ITS HEAD. It is
    #      not retyped and not summarised here.
    #      DERIVE WHAT CAN BE DERIVED: read the THIS RUN ONLY items
    #      against the rows step 1's `--brief-facts` printed, and change
    #      what disagrees, HERE and not at 7a.
    #      IT IS ONE LINE PER PARAGRAPH, and no tool or hook wraps it, so
    #      an edit REPLACES A WHOLE PARAGRAPH and never re-fills lines.
    #      AND CHECK ITS WORK: its report is evidence, not verdict
    #      why: --para 'The four ways its inputs have been got wrong'
    #      BOTH halves of the subject are load-bearing: run-status.sh
    #      filters `git log` to the subjects naming the run and only then
    #      looks for the step, so `step 6b` alone is invisible to it
    #      however plainly it names the step. `step 6a` names what the
    #      commit carries instead of the step it is, and reads as not done
    #      too. The pass is scoped by PATH, `-- micro-regime3/runs`, so it
    #      reads the run file alone whatever else the commit carries. The
    #      commit is the first action and not housekeeping: given one
    #      commit's diff the pass has a fixed object, so 6c's edits cannot
    #      move under it and you need not stop writing.
    #      The same agent keeps its reading of this run's artifacts and
    #      pays no second bootstrap; what fixes its object is the COMMIT
    #      rather than the tree, so neither 6c nor a gate-clearing edit to
    #      the run file can collide with it -- the freeze is 6d's and
    #      starts there. 6d exists to read what the fixing broke.
    #      The passes are minutes to tens of minutes and 6c is often
    #      shorter, so waiting idles the session for nothing and the one
    #      barrier this list has is 7's. A session that reads 6d's
    #      condition the other way runs THREE agents at once where this
    #      list intends two, and a report that lands after its object has
    #      moved is what the ordering is for.
    #      Keeping chapter edits out is what makes `that commit's diff`
    #      mean anything; the commit that carries RUNTIP's edit is unable
    #      to name itself.
    #      The paste is the one step of this half nothing checked: a stale
    #      brief looks exactly like a used one, and both passes read it as
    #      given. The two THIS RUN ONLY items are the half of the walk that
    #      gets skipped. The brief carries all three briefs and every fact
    #      an agent starting where your session started cannot derive.
    #      Step 1's --brief-facts rows are what the THIS RUN ONLY items
    #      state in prose, both passes reading what the brief states.
    #      wrap-restore reads only `.md`, and nothing checks a hand fill.
    #  6c. THE README SECTIONS, every other bullet: the floor section,
    #      the run's row in each series/*.tsv it reads (`./read-run.py
    #      --record` lists them), the opening, the mutable ceiling, the
    #      Lemire shipping paragraph, the stride-class chapter, the delta
    #      chain -- which gains a bullet for the run just read -- What is
    #      open, read-run.py's docstring, micro.cabal's -M8G note, and
    #      Main.hs wherever a comment cites a figure. THE TWO SWEEPS ARE
    #      THIS HALF'S.
    #      why: --para 'What skipping this costs is measured'
    #      A cross-document figure -- the floor pair, the carry-back one --
    #      is quoted in BOTH files and --check-doc holds them to
    #      agreement, so a half-done 6b FAILS that gate rather than
    #      passing quietly, which is the one place this half announces
    #      itself
    #  6d. COMMIT 6b'S AND 6c'S WORK AS A SINGLE COMMIT, subject naming
    #      the step -- AND STEPS 5d AND 5e GO IN IT TOO, taken before this
    #      commit and not after 7. SEND the second pass WITH NOTHING BUT
    #      THE STEP AND THE TWO DIFF COMMANDS -- checker-brief.txt's `THE
    #      DIFF`, `git -C .. diff PRETIP..HEAD -- micro-regime3/runs` and
    #      `git -C .. diff PRETIP..RUNTIP -- micro-regime3/README.md` --
    #      and no covering message telling it the file has moved. Name
    #      the fixes, not the prose. Send it to the same agent once its
    #      first has returned, send the BLIND READER beside it on the same
    #      diff (7a's paragraph has its brief) -- a separate agent, its
    #      being blind to the figures being what found Run 41's sixteen
    #      page defects past pass 2, which leaves page questions to it --
    #      run 6e meanwhile, and
    #      FREEZE WRITES to both documents until 7. THAT ONE COMMIT, both
    #      files in it and not two commits, IS WHAT THE AGENT ADJUDICATES;
    #      what it READS is those two commands, both files since the run's
    #      base commit, never README whole.
    #      `--inherited` WAS RUN AT 6a's HEAD, not here
    #      why: --para 'Verify the write-up before deleting'
    #      Neither 5d nor 5e depends on anything pass 2 produces, and 8b's
    #      own line says everything committed after RUNTIP is unreviewed
    #      BY CONSTRUCTION -- step 5d's record and step 5e's open list
    #      being the bulk of it. The brief already scopes pass 2 to this
    #      commit's diff and to nothing pass 1 verified, and a covering
    #      message that says `the file has moved under you, re-read it`
    #      undoes that scoping in one sentence, the pass then re-deriving
    #      the whole run file. A finding may quote a phrase you would
    #      otherwise have changed. The pass reads BOTH files, the one pass
    #      that can and the first moment all of a run's prose exists, and
    #      two commits would let it read one and call the run covered. It
    #      is not a formality: the first round of fixes makes findings of
    #      its own, and a session that stops at one pass ships them.
    #  6e. VERIFY, THE READ-ONLY HALF, run in parallel with 6d and
    #      producing a worklist rather than an edit: `./read-run.py
    #      --lost --run-doc runs/$R.md`, `./read-run.py --lint`,
    #      `./read-run.py --check-doc --worklists`, adjudicating the
    #      items it marks ADDED BY THIS DIFF and no others, and
    #      `./check-commands.py runs/$R.md`, every quoted reader command
    #      run and each figure of its sentence that no output printed
    #      listed, a figure the prose credits elsewhere included. The figure
    #      and superlative walks are the checker's, at 6b and 6d, and
    #      the end-to-end read is 7a's probe's. A timing column no
    #      earlier run published still wants a route sharing no code
    #      with the reader -- wall, or user AND system, differenced at
    #      two iteration counts. WHAT IS VERIFIED IS EVERY FILE THIS RUN
    #      WROTE: `runs/$R.md` and `README.md` always, and -- where 6c
    #      reached them -- `read-run.py`'s docstring, `micro.cabal`'s
    #      `-M8G` note and `Main.hs` wherever a comment cites a figure
    #      why: --para 'Verify the write-up before deleting'
    #      A read-only worklist is what lets it share the window.
    #      `--lost` reads both documents' paragraph lists against step
    #      5's copy and is the one check that sees a lost paragraph.
    #      --lint and --check-doc read the two DOCUMENTS; the three
    #      source files are the reading's alone, nothing gating their
    #      comments, so a stale figure there survives every green run
    #      until someone opens the file.
    #   7. WAIT FOR 6d, THE BLIND READER AND 6e ALL -- the one barrier
    #      in this list. Then CONVERGE TO ONE WRITER and fix, which is
    #      all that is left here: merge the THREE reports into a SINGLE
    #      cycle and apply it -- 6d's over both files, the blind reader's
    #      and 6e's worklist. 6b's is NOT among them, save where it landed
    #      after 6d's commit and 6b sent it here; 7a's probe comes
    #      after and is its own small cycle. A correction is a claim --
    #      derive it, then RE-RUN THE GATES
    #      why: --para 'Verify the write-up before deleting'
    #      A session that starts on whichever report came back first fixes
    #      half a document twice. 6b's pass was fixed at 6b, which is why
    #      6b owns its fixing. Two sources of fixes for one defect is how
    #      the errors 6d exists to catch get made twice over. 6e ran the
    #      gates before these fixes existed and nothing else re-runs
    #      them: the fix cycle is the one stretch of the write-up no pass
    #      and no gate has seen.
    #  7a. COMMIT 7'S WORK, subject naming the step. Then the
    #      COMPREHENSION PROBE, the blind reader having gone out at 6d.
    #      THE BLIND READER, SENT AT 6d BESIDE PASS 2, on the same two diff
    #      commands: a fresh agent given the write-up's whole
    #      diff, no reasoning about it and SIX questions, all of which
    #      turn on the page and none on the artifacts -- a bolded lead
    #      against its own body; a quantifier against the cases the text
    #      lists; a date or a run number against the order of events; a
    #      claim against what else the two documents say; a sentence that
    #      cannot be parsed or that says what the writer plainly did not
    #      mean; and anything reading as left over from an earlier
    #      version. Bound it at THIRTY tool calls, spawning none, and have
    #      it report what it did not reach.
    #      THEN THE COMPREHENSION PROBE -- which reads the finished
    #      documents rather than a diff, AND READS THEM OUT OF 7a's COMMIT
    #      and not out of the working tree, `git show
    #      <7a>:micro-regime3/runs/$R.md`: a fresh agent, NEVER the 6b/6d
    #      one. ITS BRIEF IS THE THIRD BLOCK OF `checker-brief.txt`,
    #      edited there and not retyped. It asks whether the document can
    #      be READ, not whether it is right.
    #      APPLY WHAT IT FINDS and re-run the gates. A FIGURE defect here
    #      is read as a signal that 6d or 6e missed something, and not
    #      patched
    #      why: --para 'Verify the write-up before deleting'
    #      The commit comes first so the probe reads a settled document
    #      and its findings name text that still exists.
    #      The blind reader was added after Run 35, whose measurement it
    #      is, and sent at 6d since Run 39's, the first moment all of the
    #      run's prose exists: at 7a its findings cost a second fix cycle,
    #      which at 6d they join. It finds more than the session's own
    #      end-to-end read and the figure checker's second pass together,
    #      and it costs no artifact reading at all, which is why it is
    #      first: every finding is a property of the text, so it can run
    #      the moment the text settles.
    #      The tree is where the probe's own findings are applied, so a
    #      probe reading it reads text that moves under it, which is why
    #      every other pass here is scoped to a commit. It is HERE because
    #      its own condition is `once the write-up settles`, which happens
    #      at 7 and not before; the 6b/6d agent has read this run's JSONs
    #      and cannot be surprised by the document. What it finds is a
    #      navigation defect, which no gate here has ever caught and no
    #      figure check can.
    #      IT IS ALSO THE ONLY READING THE POST-FIX DOCUMENT GETS. 6e ran
    #      the gates before 7's fixes existed and 6d read the prose
    #      before them, so the fix cycle is otherwise seen by nothing --
    #      which 7 says of itself. It is a second fix cycle and a small
    #      one, few and structural, and naming its destination is what
    #      stops the findings being answered in a reply and never made.
    ./read-run.py --lint          # 8. again after ANY Main.hs edit, and
    #      never rebuild the pair to satisfy it: say in the write-up that
    #      the comment-only move happened
    #      why: --para 'Do not rebuild the pair'
    ./run-status.sh $R                    # 8a. THE DONE-CONDITION: every
    #      step of the three lists an artifact or the repository answers for.
    #      `STATUS: all done`, with its `yours` lines done by hand, is
    #      the one state in which this run is finished; a NOT DONE line
    #      is the next step, and a summary of what remains is not one
    #  8b. THE TAIL, which no pass has read, and the LAST READING this
    #      list does, step 9 being the deletion offer. Run 8a, do 8b,
    #      run 8a again. Re-resolve RUNTIP, read
    #        git -C .. diff RUNTIP..HEAD -- micro-regime3/README.md \
    #          micro-regime3/runs/$R.md
    #      yourself, and say in the commit what it covered. Read over the
    #      working tree BEFORE 7a's commit, the tail rides in that commit,
    #      its subject naming both, `Run $R steps 7a and 8b: ...`; a
    #      commit of its own is owed only where 7a's has already landed
    #  A GATE IS NEVER FILTERED AND A READING'S OUTPUT MAY BE, which is
    #      the line between the readings above and the checks below. A
    #      GATE -- `--lint`, `--check-doc`, `check-all`, `defect-run.py
    #      --changed=<REV> .`, `selftest-mutants.py .`, a build or a test suite
    #      -- is run bare and its status read from its own exit.
    #      `2>/dev/null` is legitimate on a reading whose warnings this
    #      session has already read once, and on no gate and no first
    #      call.
    #      AND EVERY GATE HERE STATES ITS VERDICT IN WORDS: READ THAT
    #      LINE. THREE print it labelled -- `VERDICT: PASS|FAIL (exit N)`
    #      from `--lint`, `--check-doc` and `properties.py` -- and the
    #      rest say it in their own last line: `N steps, M failed` from
    #      `check-all`, `N cases run in the ok direction, M failed` from
    #      `defect-run.py --changed=<REV> .`, `N mutants, M caught, K survived`
    #      from `selftest-mutants.py .`, and `every process gated clean`
    #      from `read-all.sh`. The exit status is a second copy of it.
    #      AND A HUMAN TABLE IS NOT PARSED BY FIELD INDEX. Use `--cells`,
    #      which is TSV for exactly this; where a mode has no TSV form,
    #      match the LABEL on the line rather than its offset, and assert
    #      the header you expect before reading a row under it.
    #      AND A PUBLISHED COLUMN IS NEVER INVERTED TO GET THE OTHER
    #      ORIENTATION. RE-RUN THE READER with the halves swapped, the one
    #      you want first: `./read-run.py $PREV-<other>-main.json --compare
    #      $PREV-<basis>-main.json`, the tags being $PREV's own, prints
    #      the orientation you want, off the JSONs.
    #      AND A FIGURE THIS FILE QUOTES IN EVERY RUN IS PRINTED BY A READER
    #      MODE, never got by hand arithmetic over other modes' output.
    #      Two modes use the exit status besides: `--predictions` exits 1
    #      where a span went unread and `--pair` 2 where it refused a sunk
    #      pair.
    #  WHICH CHECK AFTER WHICH EDIT, and no other -- a commit is not a
    #      change of what a check reads:
    #      a paragraph of runs/$R.md or README.md: nothing between
    #        edits, and `./read-run.py --check-doc --quiet` once the
    #        stretch ends; `defect-run.py --changed` selects no case for
    #        prose. THE CASES PROSE DOES OWE are `check-all
    #        checks-deep.py`'s, and they are not run here: the next
    #        preparation runs them as its 8c to 8e, by the owner's ruling
    #        of 2026-10-04, so a case this write-up's prose breaks is that
    #        preparation's finding. Prefer the digits the previous run
    #        used wherever
    #        a sentence is rewritten around a figure.
    #        An edit to the checker's brief alone owes nothing
    #      Main.hs, even a comment: `./read-run.py --lint`
    #      a script here, or read-run.py: `defect-run.py
    #        --changed=<REV> .` at the END of the stretch, <REV> the commit
    #        before it -- bare `--changed` is HEAD and sees only uncommitted
    #        edits -- in the
    #        background and ALONE -- no file created anywhere in the tree
    #        while it runs,
    #        which is not merely no edit and no commit -- with `-k NAME`
    #        for one case while iterating; read-run.py besides wants
    #        `--selftest` on one run JSON
    #      a table install: `--check-doc`, the install's check too
    #      a note or a registration: `./preflight.sh $R --note`
    #      and any script here besides: `check-all .`, the static checks
    #        whole, a linter off PATH failing its step by name
    #      why: RUNTIP..HEAD is unread, and a filtered gate misreports.
    #      Pass 2 reads README bounded at RUNTIP, so everything
    #      committed after it is unreviewed BY CONSTRUCTION -- 7a's own
    #      fixes, step 5d's record, step 5e's open list and its
    #      retirements, and any disclosure a person makes after the run.
    #      8b runs after the done-condition, its text covering the
    #      output of 5d, 5e and 8, and 8a is what reports it undone, so
    #      the two are a short loop rather than a sequence.
    #      The gate rule: the three ways a gate's status gets lost are the
    #      user-scope CLAUDE.md's, with the measurements: a pipe and an
    #      `&&` chain each report the LAST command's status, and in
    #      background mode the harness reports the TASK's, so `check-all
    #      . > log; echo "RC=$?"` ends in the echo. The stderr a run wants
    #      is there -- the sunk-cell count, the R2 and sample warnings,
    #      `--corr=insitu`'s notice that its column compares to nothing in
    #      README. The verdict line is the channel a pipe cannot take: a
    #      session that reads the line cannot be fooled by a status a pipe
    #      or background mode lost, and one that reads only `$?` can be.
    #      The labelled three are not the set a grep for `VERDICT` finds
    #      -- the other three carry the word in comments and print no
    #      such line.
    #      The field-index rule is this chapter's own and not portable:
    #      the tables these modes print are aligned for reading, so a
    #      column's position depends on the widest arm name in the run.
    #      A run file prints its `cross` figures to four places and a
    #      previous run's basis is often the half yours is not, so the
    #      reciprocal is wanted every time three runs are put in one
    #      orientation -- but `1/0.8788` is a rounded number's reciprocal
    #      and not the geomean `--compare` computes with the halves
    #      swapped, and the two need not agree past the places the first
    #      was printed to. No check here catches an inverted one. Hand
    #      arithmetic over other modes' output is got wrong.
    #      Which check: an expensive check's answer stands until what it
    #      reads changes. --check-doc takes seconds, and a paragraph left
    #      long is mid-edit and passes. Prose owes the cases and looks as
    #      though it does not: defects.py derives fixtures from BOTH
    #      documents, `RUNDOC` being the newest run file and read at many
    #      sites, so a paragraph either side can move a case. A case
    #      asserts on the run file's LITERAL text, so a rewrite that
    #      spells a figure differently breaks one and no document pass
    #      sees it; spelling a figure in words is what does it. The
    #      checker's brief is the one document it never reads.
    #      `--check-doc` recomputes the tables from the JSONs. One failed
    #      spelling of one route is not a tool's absence
    #   9. offer the artifacts for deletion -- the JSONs, the logs, the
    #      wall-clock file, and for a pair both binaries, $R-pair.txt, and
    #      on a run that raised the mount their copies on hugebin/ with any
    #      `.slow` the instance gate parked beside them, which a suspended
    #      run has none of, the tmpfs emptying itself at the next reboot --
    #      once, after step 7 is done AND presented, saying what keeping
    #      them buys, and CLEAR THE TURN-END HOLD before sending the offer.
    #      Offering is the step; deleting is not
    #      why: --para 'Only then, offer the artifacts'

Steps 1 to 4c but 3a are readings and cost only tool calls, 5a another; 5, 5b
and 6's two halves write; 6b, 6d and 6e are what find things, and 7 is where
what they find is applied. Naming the fill groups, 3a, was the step most often
skipped when it stood last, because by then the run read finished; putting
it before the readings is what retires that.

1. **Gate every population on the correction, before reading any figure ---
   and read the A/A *worst cell*, not only the pair's geomean.** A control
   that passes its gate can still be the run's most informative measurement,
   as a twin carrying a 41% cell under a floor published from it was ([the floor
   section][floor]'s nursery account). A pair inside the floor whose worst cell
   is an order of magnitude outside it is not noise; it is a finding
   the aggregate is hiding. The gates themselves: `--selftest` checks
   that the forcing term scales with `l` --- one pass over the elements,
   not something whose size varies with the shape --- and `--aa` prints both
   whether the two `sum-only` halves agree and how the term compares
   with the same pass measured in situ, off the `-nosum` arms. The three
   are independent and the correction needs all of them: position, size,
   and the read itself, each blind to what the others catch
   ([sum-only](#sum-only-and-the-correction-now-applied)). Any of them failing
   invalidates the whole time column rather than merely leaving it uncorrected,
   and all have to be re-passed by every run rather than inherited --- by every
   *population* too, each process carrying its own `sum-only` pair, its own A/A
   controls and its own `-nosum` arms --- a half built on another roster carries
   that roster's --- so a class run passes or fails the gates on its own
   evidence and a failure there invalidates that class's column and no other.
   **Then write this run's own floor into the run file's Results as you draft
   it, and keep it there.** It is published with the margins it judges rather
   than kept where only this session can see it, it is re-measured each run,
   and the runs have disagreed several-fold, so the previous run's figure
   is the one you will reach for by habit and it is the wrong one. `--aa` prints
   each pair's raw ratio and `f` beside the net one for a related reason:
   the net figure is the floor between two published rows, where the raw one
   is how much an arm disagrees with itself.
- 3a. **Name the fill groups, and spend the other load-independent measurements,
  before the artifacts go --- early, because this is the only step whose window
  closes.** Allocation is deterministic per call, Core is a compile,
  and a binary's size is a `size` invocation --- none of them wants a quiet
  machine or a run slot, and each is minutes. So before the offer at step 9,
  take every question the open list already carries whose measurement
  is a compile, an allocation or an arithmetic re-derivation, and take it now
  --- the questions this run raises are step 5e's and get their turn there.
  **The named fills are the one owed by every paired Run**:
  `tools/loop-offsets.py` names a copy only in a `-g3` build, bare offsets
  are what the note records otherwise, and the map is a property of the binary,
  so once the binaries go no offset this README quotes can ever be tied
  to an arm again. **What the step produces no later session can recover once
  the binaries go, which is why it is first.** The REFUSALS are what make
  a negative honest: a loop named off no byte-identical copy is refused rather
  than guessed, and a straddler the sweep reports may be an info table
  it misread rather than a loop. **A refusal wants the OTHER half's twin tried
  before it is recorded**, the basis twin naming the `-u2` leaf fills
  by the same byte identity, and what no `-g3` build holds byte-identical
  on either compiler, `fillStage2`'s runs, being named by `--loose` off their
  signature. The ORDER has been taken both ways without cost, so what the list
  fixes is the deadline and not the sequence. And a note's fill-in block
  is where TRANSCRIBED figures live, which is why the executing session re-runs
  the `--match` off the binaries it timed, and reads the block it ends with,
  the exit spans astride named the same way --- empty on a `LOOP_EXITSPAN=1`
  half, and on any other the loops that switch would move. **Where a preparation
  spent this half early, on an idle box before the pair ran, the executing
  session re-derives it off the binaries it timed** --- two minutes,
  and the difference between a block that was read and one that was carried,
  which is the distinction pre-run step 12b exists to make and which a note's
  fill-in block cannot make for itself. What is left over is the timing work,
  which is what a quiet machine is for.
4. **Match bases before reading any ratio.** The first act of a comparison
   is making its two sides one basis --- the same population, the same
   restriction, the basis a figure was stated on --- and only then reading
   figures. **AND WHERE THIS RUN'S SHAPE SET MOVED, PIN IT BACK BEFORE QUOTING
   ANY CROSS-RUN FIGURE**: `--exclude-shape` the shapes this run added, once per
   shape, so the figure is over the population its predecessor had. This
   is not the `alloc` column's rule, though that column is where it is written
   down; it is every cross-run figure's. A run that added two main-set shapes
   read its ceiling and eight `alloc` rows as moved out of their bands until
   each was re-read over its predecessor's own shapes and returned
   that predecessor's figure ([Run 24's file](runs/run24.md)). **One JSON
   at a time, never merged.** The reader takes one file, and its geomean
   is that file's population --- the main set's or one class's. Every mode names
   that population in its first line, `--selftest` fails a file spanning two
   and `--markdown` declines to emit a table for one, so a merged run is caught
   rather than published. The class tables stand beside the main geomean, per
   [the ruling](#the-stride-classes-and-what-they-cover), and there
   is no combined figure to compute, so a sentence comparing populations
   compares their tables.
Analyse with `./read-run.py`, which is where every table in this file comes
from --- read [the reader's own section](#the-reader-read-runpy) first, and do
not write another reader. **The properties are part of this and are the thing
these steps are likeliest to leave out**: they are the same job three times
a population, off the verdicts `--block` emits, and the set is restated
for the next run on this run's basis while the readings are still in front
of you. **A paired Run's own mode is `--compare`**, and its direction
is the list's convention: the run given first is the one the ratios are *of*,
so `basis --compare control` puts a figure below 1 where the basis is faster.
5. **Make the run's own file, COMMIT THE COPY, and repoint README at it,
   and not before this step.** `runs/run<N>.md` is one run's write-up entire ---
   *Results*, *What the next run compares against*, *The properties the next run
   should test*, *The stride classes, run by run*, *Provenance*, none of them
   numbered because the name is --- so a run copies the last one's over its own
   name with `copy-run-file.py`, commits that copy, and rewrites it, HERE
   and not earlier for the reason the pre-run list's head gives: every mode
   defaults to the newest file in `runs/`, and everything before this step wants
   the run behind. **What it has instead is one link check, and `runs/`
   accumulating is what makes it necessary**: the previous run's file stays
   on disk, so a link left pointing at it resolves, renders and quietly promises
   figures this run replaced. **Expect it to fail five ways the moment the file
   exists and before you have touched README** --- dead anchors, links naming
   the run before, the run file's sections uncovered by the replace list,
   the Results section naming the previous basis, and the head unchanged
   from the run before --- and every one of those is this step. A source file
   naming a run file would go stale at the next run and `--check-doc` could
   not see it, `runs/` keeping every run so the path resolves --- which is why
   none does. A standing-prose link into the run file promises content
   the replacement may have moved out, and such links keep resolving through
   renames, which is why repointing is not re-verifying. A link whose TEXT
   quotes a ratio, pointing at a section that no longer carries it, is what
   that walk is for. **Committing the copy before editing it is what makes
   the rest of this step cheap.** An untracked file has no committed form,
   so `wrap-restore` cannot classify it and leaves it alone --- one of the two
   cases the wrapping rules still leave to be done by hand, the other being
   a file whose last commit sits at neither fixed point, and this one need
   not arise. The copy also gives git a restore point for the whole write-up,
   which a range splice can make necessary. And it makes the write-up's own diff
   the artifact step 6b briefs the checker to read --- uncommitted, the file
   enters history as wholly new and its diff says nothing about what the run
   changed, so the checker has to snapshot it and diff against its own copy.
   The cost is one commit whose content is a copy, which reads as diary until
   the next diff makes it legible. **The copy masks every decimal, percentage
   and run number in prose and no other figure, and `--check-doc` refuses a mask
   left**, ruled 2026-10-05 by the owner: a figure the copy carries unedited
   is last run's number under this run's name, and a mask makes keeping one
   a retyping. Masking every measured figure would mask stable counts of shapes,
   arms and classes, retyped every run, which is how a gate gets switched off,
   and masking only the paragraphs `--inherited` calls run-specific would leave
   most decimals as copied. Counts and number words stay `--stale`'s, printed
   and never refused.
- 5b. **Install the tables with `--in-place` rather than pasting them.**
  `--markdown`, `--fingerprint` and `--block` each take it, and each refuses
  rather than guessing: the match is by whole line, the count is asserted,
  and a class table is narrowed by its block's bolded lead. **An install
  is placed by a bolded lead, which is prose the write-up is editing while
  it works**: rename a lead and the install that fills the paragraph beneath
  it refuses, naming it. Hand-pasting is what this replaces: a table located
  by searching for its header text can land rows under a quoted copy
  of that header and leave the old table standing, every check green because
  the check looks it up the same way. The table carries `needs` and the emphasis
  forward from the one already there, and its stderr is the whole of what
  is left by hand; new rows are filled from a note written here before the run
  whenever a roster change is known in advance --- the cell then gets
  transcribed rather than invented at the end of a long day. A class table comes
  out six columns wide, `needs` being a property of a strategy rather than
  of a population and so stated in the main table alone.

- 5e. **Walk the open list against what this session actually did**, which
  nothing checks. **Grep [the settled index][settled] before adding an entry ---
  and before ASSERTING anything this README may already have ruled on**,
  not only before deriving: a question is easy to open against something already
  answered in a section you are not writing in. A run answers some of its own
  questions and a write-up raises others, and both go stale in place: an entry
  answered by the very probe it specified stays open until this walk closes it.
  What a probe narrowed is left as narrowed.

**The cross-class summary is INSTALLED, from the class blocks and not
from the JSONs.** Every cell of it appears in one of the class tables above it,
so `install-tables.sh` reads the rows off each class's own `--block` ---
the same output those tables came from, never a second derivation able
to disagree with them --- and refills the table IN THE ORDER THE DOCUMENT
ALREADY HAS, a table inherited from run to run being no place for a reordering
nobody asked for. A row whose class this run has no block for is LEFT STANDING
and the driver says so and exits nonzero. What stays the author's is the prose
around it. **Each class's `--block` now checks its own row** and names the cell
on stderr, so `install-tables.sh` reports a wrong transcription among what
it leaves you. Its emphasis comes off the same block's `summary bolds`, decided
on the unrounded values, so the drift between runs that a judgement applied
by hand produced cannot recur.

6. Walk the list under [Provenance](#provenance) of what the new numbers
   replace, and do not trust it to be complete: re-run the two sweeps it names
   and map each hit to the bullet covering it; the list has been wrong before.
   **What skipping this costs is measured**: Run 16 walked it shallowly
   and an independent checker then found **fourteen of its twenty-one findings**
   were stale prose in sections this list names --- an anchor table, a launch
   window, four verdict paragraphs, a class calibration paragraph --- every one
   of them contradicted by a table the same write-up had just installed.
   **Replace; do not annotate.** Walking a list of what to replace makes "now X,
   where it was Y" the natural sentence, and a superseded number has to earn
   its place by the test in the user-scope `CLAUDE.md` --- would someone redo
   the work without it --- which most do not meet; `--check-doc` lists the ones
   already here for adjudication. Only a movement past the floor earns
   a sentence.
6a, whose reasons these are since the recording moved there. **The commit
the binary was built from** is transcribed for a paired Run
from `<prefix>-pair.txt`, which carries the commit, the regime, the GHC and both
md5s because this step asks for them --- and where a note has no GHC,
`strings $R-<basis> | grep -oE 'ghc-[0-9.]+'` reads it back out of a binary
still on disk --- and the note outlives the session that built the pair
(the JSONs do not survive, so the source is the only thing that makes a run
reproducible even in principle --- this README's figures are one desktop's
and are not portable, see [Provenance](#provenance)). A class process's line
is measured for its elapsed time and its two heap peaks but not for its shape
count: that count is fixed before criterion does the selecting, so it reads
every class view rather than the population that ran, and the population's own
size comes from the reader's first line;
7. **Verify the write-up before deleting anything --- and the reasons here cover
   6b, 6d, 6e, 7 and 7a, which is what one step's worth of verification
   was split into.** Each of these checks has caught something.

   **This step is the whole of the document verification a run owes, and nothing
   else is to be reached for. Four passes, in this order --- and a fifth, first,
   where any edit was scripted:** run `./read-run.py --lint`
   and `--check-doc --worklists` --- **the one call that reads the worklists
   rather than the verdict** --- whose exit codes are the verdict, anchors
   and the replace list's coverage of every figure-bearing section among what
   they settle; read the worklists they print and adjudicate each entry; read
   the write-up end to end against the run's own artifacts; and hand the diff
   to an independent checker, which the paragraph after next briefs. None
   of them is optional --- and the first is re-run after the fixing, findings
   renaming headings and a renamed heading breaking a link silently. The third
   is the one that keeps finding real errors, and the fourth is what catches
   what the third cannot see in its own writing.

   **REPLACE A PARAGRAPH BY ITS ANCHOR, NOT BY QUOTING IT.**
   `./read-run.py --replace ANCHOR --with FILE` swaps the paragraph carrying
   ANCHOR for the text in FILE and asserts the anchor is unique, so the old text
   never passes through a transcript and no `assert s.count(old) == 1` has
   to quote it back. That is the difference between naming a paragraph
   and reprinting it, and reprinting by locate-print-quote-assert is the largest
   single cost a write-up can run up. **Quoting is for a paragraph you
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
   an error about one edit while silently dropping the rest. Write the file
   inside the loop and report per edit, so a later miss cannot discard
   an earlier success. That is separate from what a scripted rewrite gets
   *wrong*, which is the next paragraph, and it is the failure to expect first
   because it is the quiet one.

   **That fifth pass is one command:**
   `./read-run.py --lost --run-doc runs/$R.md`, which reads both documents'
   paragraph lists against step 5's copy and names what left without
   a replacement arriving. **The figure sweep reads the same on either form,
   so nothing is wrapped to read it**: `--check-doc` keys a paragraph
   by its collapsed text when it asks whether this diff added it, and reads
   the committed copies from the commit that added the run file. A scripted
   rewrite fails in two shapes and neither is a wrong figure. Anchored
   on a *prefix*, it replaces the whole paragraph and drops whatever followed
   the part its author had read; `--check-doc` catches that one, every prose
   paragraph being required to end a sentence. Anchored on two *markers*,
   it deletes every paragraph between them, however many that turns out
   to be --- and nothing catches it: the survivors still end sentences,
   the anchors still resolve, the figures still match, and every check here
   is a predicate over what is **present**, so none can see what is gone ---
   measured 2026-08-14, `--lint`, `--check-doc` and the truncation check all
   exiting 0 over a removed paragraph. So assert the extent in the script, echo
   what it is about to overwrite, and run `--lost` afterwards, the one check
   here that sees a lost paragraph.

   **A correction is a claim, and is written under exactly the conditions
   that produce bad ones.** Whatever the verification turns up gets fixed
   at the end of a long write-up, at speed, and the fix is a new assertion
   with no derivation behind it unless one is made. Derive a fix the way
   the sentence it replaces should have been derived, re-run the gates after it,
   and give the checker's second pass the fixes and not the prose alone ---
   the paragraph after next measures what late fixing costs.

   **DO NOT RE-DERIVE AN INSTALLED FIGURE AT ALL; spend the whole of that budget
   on the prose and on the sentences elsewhere your tables have just
   falsified.** Two checkers recomputed some five hundred table rows each
   against the reader and found not one wrong, against 34 and 52 prose findings
   in the same diffs --- so re-deriving an installed figure buys nothing
   that `--in-place` did not already guarantee, while every hour spent there
   is an hour not spent on the two places errors actually live. **Expect every
   error to be in the prose and none in the numbers, and expect the green
   checkers to be why.** The shipped errors have been superlatives asserted
   without sorting the population they quantify over, a sentence contradicting
   its own paragraph three lines later, and a percentage computed
   from a published table instead of from the cells --- not one a wrong figure
   out of the reader. `--lint`, `--check-doc`, `--selftest` and `--aa`
   were green throughout and right to be --- they check the measurements,
   and the measurements were sound.

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
   `--check-doc`'s sweeps hand you worklists, and adjudicating them
   is not reading the document. Nor is inheriting one --- a worklist you did
   not derive verifies somebody else's findings while telling you nothing about
   what else is wrong, which is the completeness question the reading exists
   to answer. **The checker and the comprehension probe are not two goes at one
   job, and the split is what makes the second worth its cost.** A checker
   is scoped to the diff: it reads what changed, recomputes it, and is the only
   instrument that returns completeness over a table. It cannot see a sentence
   in a section nobody touched that this run's tables have just falsified ---
   and on a run that changes its basis those are everywhere. The probe reads
   the README as a stranger meets it, and that is what it returns: three
   thresholds quoted for one quantity, two sizes given for one population,
   a ruling standing unmarked in the run that abandoned it, two comparison rules
   that read as one and contradict --- not one of them in any diff. **So run
   both, and read the probe's findings as being about the README rather
   than about the run.**

   **An independent checker on the diff is the highest-yield instrument here,
   and the cost of launching it late is measured**: launched once a whole
   write-up was drafted, its first pass returned seventeen findings, several
   of them prose built on a table figure an earlier pass would have caught
   first, and its second returned seven more of which four existed *only*
   because the first round of fixes had been written. Late launching does
   not merely delay the findings, it multiplies them --- which is why
   the checklist gives each pass a commit to work from and a position rather
   than a condition, and why the fixing belongs to the pass that caused it.
   It is dear per finding --- some thirty times what a session's own targeted
   re-checks cost --- and it is worth it anyway, because its findings
   are the ones a session has already proved it cannot see in its own prose,
   and because it returns a completeness the author cannot: every table row
   verified rather than the ones somebody thought to check. (The rule
   that a check must be proven able to fail governs the instruments themselves
   and is stated with them, [in the reader's section](#the-reader-read-runpy).)

   **The four ways its inputs have been got wrong, each measured.** Its BRIEF:
   `checker-brief.txt` has been written out twice over a killed agent,
   and passed over for a typed brief that left *could not check* items checkable
   for want of paths the file names --- while a stale brief looks exactly like
   a used one, carrying the previous run's box reading, window, class counts
   and threshold list, which sends a probe after the wrong classes. Its OBJECT:
   pointed at the working tree, the pass idled seventeen minutes rather
   than writing. Its DIFF: twelve chapter commits between a write-up
   and its second pass made *that commit's diff* mean this chapter as much
   as the run. And its AUTHORITY: reports have miscounted the arms past 3%
   and put a crossover a length out by skipping a shape. Being asked about
   is a fifth: the pass is pre-authorized by the user-scope `CLAUDE.md`, whose
   standing request discharges Claude Code's own conditional.

   The checks themselves:
   1. **MEASURE, THEN WRITE THE CLAUSE --- and derive every count and ratio
      in the prose from `--cells`, never by eye, and never from a published
      table.** The order is the operative half and is stated first because
      the rest of this rule is a property of the finished sentence, checked
      at verification, while the failure is in composition. A sentence written
      before its measurement is a guess with a citation. The second half
      is the one that looks safe: a table prints three significant figures
      because that is what a reader needs, so arithmetic on its cells
      is arithmetic on the rounding, and a +4.3% comes out +4.1%. A percentage,
      a ratio and a count all come from `--cells` or from `--pair`, whatever
      is printed three lines above --- and for a class paragraph,
      from the verdicts `--block` now emits under its per-shape line, which
      state the three properties' outcomes and name the arms that actually lead.
      That block exists because this rule kept losing to the table being right
      there while the paragraph was written. "32 of 33", "30th of its 33
      shapes", "the only two past 7%" are all claims a glance at a sorted table
      gets wrong. Two shapes of claim need naming because counting is not what
      they look like. **Every *only*, *largest*, *fastest* or *never* is a claim
      about the whole table** --- or about this file's own HISTORY, *the first
      repetition*, *the widest floor on record*, which is derived by walking
      the run files and never remembered --- and is derived by sorting it,
      not by looking at the arms the sentence is about. And **a ratio between
      two published cells comes from `--pair`, never from dividing the printed
      figures**, which are rounded to three digits. **And `--cells` is a print
      too**, its `alloc_mult` carrying four decimals, so a question finer
      than what it prints wants the mode that answers it rather than a script
      over the dump: allocation agreement is `--compare --alloc`, which exists
      because a script over the printed multiple found every cell agreeing where
      the underlying fit does not. **Before reading any figure whose predecessor
      is on record, reproduce the predecessor first.** Stated narrowly
      this is about re-deriving a published figure, and it generalises to every
      probe: a probe that reproduces its predecessor's figures before it reads
      anything at a new setting has a new figure trustworthy the moment
      it appears. This is the prove-a-search-non-vacuous rule applied
      to a derivation rather than a grep --- run the computation against a case
      whose answer is known before trusting it on one whose answer is not ---
      and it is cheap: one extra invocation;
   2. **reproduce any newly-derived column by a route that shares no code
      with the reader.** A four-bench filtered run carrying both `sum-only`
      halves takes seconds, and criterion's own printed `time` lines then give
      the ratio by hand: on `cnn-slice-c32`,
      `(1.506 - 0.1739) / (6.339 - 0.1739)` = 0.2161 against the reader's 0.216.
      Recomputing from `--cells` is worth doing too, but it shares the reader's
      arithmetic and cannot catch a wrong definition, only a wrong
      transcription. Two rules the independent route needs. **Difference wall
      time, or user *and* system --- never user alone**: the inherited "wall
      and user time agree on it" is a property of the workload it was written
      for, and where the RTS does kernel work they part completely, which is how
      0.36 ms per call of system time went unseen and a real 10% effect
      was reported as zero. And **difference at two scales**: if the per-call
      figure moves with `n`, part of what is being divided is a fixed cost,
      which is how a one-time 0.9 s of page-faulting read as half a millisecond
      a call;
   3. **take the cheap decomposition before proposing a mechanism.** Where
      a cost can be split by an instrument already to hand --- mutator against
      collector, one arm against another, alone against after --- split
      it first, as one `-s` reading of GC against mutator time settles what
      an account built before it can get wrong by orders. **And when two
      instruments disagree, that is the finding.** Do not average them, pick
      the one the README prefers, or quietly drop the awkward one. Locate
      the disagreement first: the criterion slope and the `-n` differencing
      above parted by 8 points on one arm, both reproducible to a fraction
      of a percent, and the cause was neither sampling nor sample size but which
      clock was being read. Until it is located, neither number is evidence,
      and a retraction made on the strength of the wrong one is worse
      than the claim it withdrew;
   4. **walk the diff against the writing rules as a check of its own, not only
      while writing.** The replace-list walk manufactures "now X, where
      it was Y", requoting a count in place preserves a sentence that should
      have lost its numeral, and a class paragraph's close invites a mechanism
      the run never measured. `--check-doc`'s figure sweep lists candidates,
      `Main.hs` comments included, and `--para` prints the ones it names without
      reading the file around them, but the redo test itself is the reader's;
   5. **read the document end to end**, and aim the reading at what
      the instruments cannot see. The mechanical passes above do not catch
      a bullet contradicting the table three lines below it, a table installed
      in the wrong place, an exclusivity claim about arms nobody sorted,
      or a figure quoted on a basis it was not measured on. That the checkers
      here are good is itself the hazard --- green instruments make
      the remaining gap feel small, and the gap is exactly where they do
      not look, so read for placement, for *only* and *largest*, and for which
      run and basis each figure belongs to. This is the pass that keeps finding
      real errors;

   **Four conventions this README holds to, each of which exists because
   breaking it has cost something here.** **A ratio is quoted in the direction
   `--pair` prints it, or the sentence says in words which arm is faster.** Both
   directions appear in this file, a margin and its reciprocal, and a WIN COUNT
   belongs to only one of them --- so a reciprocal quoted beside its own arm's
   win count inverts the finding while every check here stays green. **A figure
   in prose names its run, its basis and its population, or it belongs
   in a table with the prose pointing at it** --- a bare numeral carries
   no provenance, and without it a failed run's figure lands beside a good one,
   or a *published* ratio is compared with a *paired* one. The population
   is the newest way to make that mistake and the easiest, a class figure
   and a main-set one being the same kind of number over different shapes.
   **An anchor longer than about thirty characters goes reference-style**,
   defined at the foot of the file: inline it overflows the width
   and the rewrapping that follows is pure churn. And **a link's text names
   its subject, never its position** --- a link reading *the head of the run
   chapter* keeps resolving through renames while the content it promised
   leaves, a decay no anchor check sees, which is why `--check-doc` lists
   standing-prose links into the run's file and step 5 re-verifies them;
8. Re-run `--lint` after editing `Main.hs`, even when only comments changed:
   the reader parses that file for the roster and the shape dims, so a comment
   edit can break a check that passed before it. `--lint` reads the source
   and needs no build, which is the whole of what that reason asks for. **Do
   not rebuild the pair to satisfy this step.** Steps 6 and 7.4 send you
   into `Main.hs`'s comments on purpose, and a rebuild would replace both halves
   and want a fresh note stamped with today's date and commit --- which
   is the file 6a transcribes the binary's provenance out of. A comment edit
   after the run leaves the timed binaries correct and the source they
   were built from moved by a comment; say so in the write-up rather
   than rebuilding to hide it;
9. **Only then, offer the artifacts for deletion --- once --- and abide
   by the answer.** The JSONs, the logs and the wall-clock file, and
   for a paired Run the two binaries and their `$R-pair.txt` with them,
   that note being about a pair and worth little once the pair is gone.
   The offer comes after the verification is presented and not after the writing
   --- an artifact deleted once its write-up is drafted takes with
   it the ability to re-check anything needing the raw samples when
   that write-up is later questioned. **AND IT IS NOT ONE RUN'S OFFER: a pair
   a LIVE registration derives its priors from outlives the run that used it.**
   A registration takes its figures off an earlier pair's own binaries, JSONs
   and counts files rather than quoting them, which it can do only while
   that pair is still on disk --- so the offer says which earlier pair this run
   leaned on, and the session making it checks the open list for a registration
   resting on one before naming it. **And it waits on a quiet tree**: another
   session may be timing probes against the two binaries hours after
   the write-up closed, which the directory's own mtimes show and nothing else
   does.

    **They are not required to go.** The numbers live in this file and the fingerprint keeps a per-shape record past its run, which makes deletion a licence and not an obligation. What is lost by deleting early is concrete --- every `--pair` a later question wants, every per-shape spread that separates a bias from noise, every count re-derived from `--cells`, and every sample-level reading needs the JSON and nothing else does --- and kept artifacts have answered questions their write-ups never foresaw.

    So: ask once, say what they buy, and take no for an answer without raising it again. A previous run's artifacts still being here is not a defect to be tidied and is not a blocker for the next run, whose relaunch guard is scoped to its own name.


#### The reasons behind the three lists

No STEP is here: every fact that changes what a session does is in one
of the three lists above, which is this chapter's own contract, and what follows
is why those steps are what they are. **One ruling is stated here rather
than in a list, and the lists lean on it**, so it is named at the top rather
than met by surprise: BOTH HALVES ARE BUILT ANEW, EVERY RUN, whose four refused
shortcuts are spelled out below and whose instruction is pre-run step 2's *BUILD
BOTH, ALWAYS*. Point at it by NAME. It sits below the lists, where a preparation
reading the list it owes does not pass it on the way in. Take a paragraph
from here when a step surprises you: every `why:` line in the lists names one
by its bolded lead, which `--para` resolves wherever the paragraph sits.

**The three lists carry every operative fact in this chapter, and the prose
carries the reasons and does not restate them.** That is a contract. A fact
that changes what you do belongs in a list --- if you find one that is not,
that is the defect, not your reading. And a rule's evidence goes at the end
of its paragraph, as a date and an outcome --- never inside an instruction,
and never as a chronology. **AND THE OVERLAP BETWEEN THEM WAS MEASURED
ON 2026-09-18 AND IS NOT WORTH CUTTING, so this is a don't-do ruling and
not an invitation.** Steps look as though they restate their own `why:`
paragraphs, and the sweep --- every `why:` pointer, its step's body against
the paragraph it names, longest shared run of words --- found ONE
of thirty-seven sharing eight words or more, step 9's regime figures, which
the list owes as operative and the paragraph needs to argue that no eye misreads
the separation. So the mechanism already does its job, the impression being
of length and not of repetition, and what a future session should re-run before
proposing this again is that sweep.

**A RUN IS ALWAYS TWO SESSIONS, and which one you are decides everything
in the three lists above.** One PREPARES the run, through step 12 of the pre-run
list, and hands over `$R-pair.txt`; another EXECUTES it from step 13 and writes
it up. Which half you were asked for decides which of the readings below you
owe, which list you start in, and what is already spent and not yours to redo
--- so settle it before reading anything else. **And a run is finished when
`./run-status.sh $R` says all done**, read off the artifacts and the repository
and never off a session's sense of it: a summary of what remains is not a step
toward it.

**What a run must read, so that nothing else is read to find out --- and
it is read BY THE PART, never whole.** *Whole* is the word a session acts on,
because it governs how the file gets opened, tables named skippable and all.
The enumeration is the instruction and the tables are what a run does not read
--- the reader emits them, `--in-place` installs them, and the checker
recomputes them from the JSONs. **`./read-run.py --section NAME` is what makes
that takeable**, printing one section's prose without its tables and naming
the size it withheld, since a line range cannot skip what sits between
the paragraphs it spans and a line number does not survive a rewrap.
**This README is never read whole**: it runs to well over a hundred thousand
words and this chapter alone to thirty-odd thousand, which is what `--section`
and `--checklist` exist for. **So, as ten items, each owing an artifact,
and each read AT THE STEP THAT NAMES IT and not before**: item 1 is read now,
and every other item stands in the lists above as a `READ NOW` line at the step
whose work needs it, because a reading taken at the head is forgotten
by the time its step arrives. A reading that owes nothing cannot be told
from a reading not done, which is the whole of why this is a list and
not a sentence. **Items 2, 4, 5 and 6 are read at the three post-run steps
that rewrite those very sections** --- 5 for item 2, 6a for item 4, 4 for items
5 and 6 --- and by nobody else, never by a carrier, the reading not being
avoidable to begin with. Post-run step 5 copies the previous run's file
and the write-up edits that copy paragraph by paragraph, so the session reads
that run's head, its two-column section, its properties and its class blocks
AS THE TEXT IT IS REPLACING --- and a carrier reads the same four a second time,
in another process, to summarise what the session is about to have open in front
of it, while runs handed the summary never opened the file. What the items keep
is their QUESTION --- does the two-column table carry the last run's columns,
which properties are live and how many --- which is the half a carrier
was really enforcing and which costs nothing asked at the step that rewrites
the section.

    1. this chapter's three checklists, each printed alone by
    `./read-run.py --checklist pre|run|post`, a fifth of the chapter's lines
         -- every step of them is owed, the build included
         AND BOTH LONG LISTS COME IN HALVES, `pre-a`/`pre-b` and
         `post-a`/`post-b`. The post list is cut at step 6, nothing below
         it being actionable until 5b's tables are in; the pre list at
         step 11, where the machine time starts and where nothing can be
         started until preflight's 4,5 has passed on binaries that exist.
         Take `pre-a` at step 0 and `post-a` at run list step 13a, before
         the evening is launched, the other half of each when its steps
         arrive.
    2. the last run's head and Results prose
         -- one sentence: what this run's own head has to answer
    3. What the next run compares against, its prose and not its figures
         -- the regime, the roster and the basis, each named
    4. the two-column table under it, the ONE table read, `--with-tables`
         -- does it carry the last run's columns? A write-up can
            forget to add its own, which is why this is named separately
    5. the properties and the prose after them, which is where retirements
         are recorded -- which are live, and how many
    6. the class blocks: the six numbered items of the form, and one example
       block, not the rest
         -- the form, in your own words
         ITEMS 2, 4, 5 AND 6 ARE READ AT THE STEPS THAT REWRITE THOSE
         SECTIONS -- post-run 5 for item 2, 6a for item 4, and 4 for
         items 5 and 6 -- and not before and not by anyone else, the
         session having those sections open then; no carrier reads them
         ITS FOUR READS, none of which opens a file whole (P=$PREV):
             item 2  --section Results --run-doc runs/$P.md
             item 4  --section 'What the next run compares against' --run-doc runs/$P.md --with-tables 1
             item 5  --section 'The properties the next run should test' --run-doc runs/$P.md
             item 6  --section 'The stride classes, run by run' --run-doc runs/$P.md
         The 1 is the two-column table and the other tables of that
         section are the per-shape fingerprint, which item 4 does not
         read; the withheld line names how many
         the section carries, so a run that adds one can still find it
    7. the open list, by its status markers rather than end to end,
         grepped over `wrap80 --unwrap README.md` -- a marker sits at
         the head of an item, which the wrapped form breaks
         -- the OPEN entries, named; a preparation reads only those
            naming an arm `./registration-drift.py $R --since $PREV`
            reaches, which is pre-run step 12a's scope
    8. Provenance's replace list and its delta bullets
         -- what this run has to replace
         -- THE WRITE-UP'S, read at post-run step 6, and not a
            preparation's
    9. `read-run.py`'s docstring, this chapter's other governing
         document -- BY HALF, like the list it sits in. A PREPARATION
         uses the Modes list, `--para`, `--section` and the two gates, `--lint` and `--check-doc`;
         the statistic definitions, the A/A identity, the validation
         history and every mode that reads a run's FIGURES are the
         EXECUTION's.
         THAT SPLIT IS A DEFAULT AND NOT A PROHIBITION: a roster can
         take arms past a bound the correction needs, so that rows go
         entirely non-positive and a required mode refuses legs, and
         which rows have no corrected time is stated in the `time`
         definition and in no list. So go back to corr, net, time and
         worst the moment a
         figure surprises you, a gate refuses a leg, or an arm's
         relation to that pass is in question -- which is the moment
         the EXECUTION's half becomes a preparation's
         -- NAME THE MODE YOU TOOK A FIGURE FROM, on the note's own
            `--fill-in` row or beside the figure: an item owing no
            artifact cannot be told from an item not done, which is the
            whole of why this is a list
    10. the PREVIOUS run's pair note, `$PREV-pair.txt`, and
         pair-note-template.txt beside it -- that note is the only copy
         of both recipes and is what this run's note is written FROM,
         and the template says what a note owes; where the pair wants a
         half of a kind that note never built -- a compiler it did not
         carry -- the last note that built one holds that recipe, and
         `grep -n 'HOW EACH HALF IS BUILT' -A 70 $OLD-pair.txt` is how
         you take one block out of a note you do not otherwise owe
         ONE COMMAND READS IT, and it is step 2's:
             ./read-run.py --note $PREV-pair.txt --draft $R \
                           --halves <basis>,<other>
         It prints each of that note's `[PAIR'S]` blocks -- the two
         recipes, what the pair measured and why its basis was that
         recipe, the roster, the compiler, the shim -- as a model under
         a `<yours>` line, takes the `[SAME]` blocks from the template,
         and withholds the handover and the gate, which are spent with
         that run
         -- the two recipes, and which of their lines the pair varies

**SO THIS IS TWO LISTS, and there is no case in which a session owes all ten.**
The numbers never move, so a reference to an item still lands. The pre-run
list's own head names the five its half owes, which is where a preparation meets
the split; the run and post lists have no such head, so an executing session
meets it here. What each is for: **The PREPARATION owes 1, 3, 7 as pre-run step
12a scopes it, 9 and 10** --- of item 1, THE PRE-RUN LIST ALONE, and of items 9
and 10 the halves their own entries name. The launch, rider and counts blocks
the note carries are in `pair-note-template.txt`, where the note is written
from anyway, so neither the run list nor the post-run one is owed. Those five
decide the pair, the roster, the note and what this run is for, and nothing else
does. **The EXECUTION owes 1 --- the run and post-run lists --- with 2, 4, 5, 6
and 8, the replace list and its delta bullets**, every one of which answers
a question the write-up asks: the replace list is walked at post-run step 6
and gains nothing from being read hours early, which run list step 13a already
says of it, and the class blocks' form is not used until a block is written.
**ONE OF THOSE CROSSES BACK, and it is 5.** A roster change that parks or drops
an arm can leave a live property naming an untimed one, which `--lint` refuses
at step 7 --- so the preparation that made the change is the one that must
retire or re-aim it, and it owes the properties section to do that.
A preparation that parks nothing does not owe 5, and step 7 is what tells
it which it is. **Reading the other session's half is the largest avoidable
spend in this chapter after the prose itself.** It is a spend the split makes
invisible: nothing in a handover shows what the session before it read
for nothing. Items 2 to 6 are [the last run's own file](runs/run45.md#results),
3 and 4 being [what the next run compares
against](runs/run45.md#what-the-next-run-compares-against), 5 [the
properties](runs/run45.md#the-properties-the-next-run-should-test) and 6 [the
class blocks](runs/run45.md#the-stride-classes-run-by-run) --- and `--section`
takes the heading's own words, never the anchor those links spell, which
it refuses by name:

    ./read-run.py --section 'What the next run compares against'
    ./read-run.py --section 'What the next run compares against' --with-tables 1

Everything else in this file is reference, and reading it is how a write-up's
budget goes without a figure to show for it. **The excuse to expect
is not laziness but *"I read what I judged useful and drifted"***, given
by a session told not to economise for skipping item 2, the largest single input
to its work; nothing it skipped owed anything, so it reported none of it.

**FIRST, THE RULING, because it decides what this chapter is: BOTH HALVES
ARE BUILT ANEW, EVERY RUN.** A recorded run's two binaries are built during
this preparation, back to back, from the two recipes its note carries. Four
shortcuts are refused by name, and none of them is a judgement call:
the previous run's binary, a binary built for a probe, one half copied to stand
as the other, and one binary run twice under two sets of flags. So there
is no fork and no path to be on --- the build step is unconditional and every
run owes the whole of this chapter, however recently the last one built what
looks like the same pair. Why a shortcut cannot be argued sound from its inputs
is under *Why the build's three rules are what they are*: the drift it admits
is between the RUNS, nothing is rebuilt between the halves to expose it,
and no step here can see it.

A *major run* is the whole roster over the whole shape set at criterion's
default budget --- the main set and, by default, **every stride-class population
with it**: one process for the main set and one per class, or two of each where
the run is paired, in the order of the sequence the run list gives. Asking
for a major run asks for all of them; leaving a population out is an explicit
exception to be stated, not a choice this README leaves open. The whole
is analysed and written into the run's own file. What follows is the procedure,
and it is written to outlive any one run.

**What asking for a run asks for, since the request is one sentence and the work
is this chapter, and it is asked once per half.** Each half is asked separately
and each is given whole without coming back for permission between the steps ---
the procedure is the permission, each step naming what it needs and what it must
not do, so a question this chapter answers is not a reason to stop. The go-ahead
does not carry across the boundary, which the run list's head says where
it bites. **THREE parties appear below and this README keeps them apart.**
*The preparing session* builds the pair and writes the note, and stops at 12.
*The executing session* spends the machine and writes the run up; where
this README says *a session* with no qualifier it means that one, here as
in the twenty-odd other places it says it. *Whoever asked for the run* holds
the decisions a procedure cannot make, and is never called *the author*:
that word means the session writing a block --- the one whose prose
an independent checker is set against --- and it is the executor,
not the requester and not the preparer.

**A probe budget rides with it, and it is spent AFTER the write-up rather
than before.** It is separate from the pre-registered questions, which
are appended after the classes and were designed before the evening. What
this ordering is for: the write-up is where a run's errors are made, it is done
last, and a probe spent first is spent out of its attention. Take whatever
measurement the run's own *results* make worthwhile, with no ceiling on it:
a discriminating reading of a cell that came out strange, a derivation
over the artifacts while they still exist. What bounds it is the artifacts
and not a clock --- spend it while they live, most of it being unspendable
afterwards. **What DOES bound it is the box**: this budget is spent past step
19a, where the machine was handed back, so a probe in it that TIMES anything
is asked for first (19a); one that only reads the artifacts is not. **And do
not read the budget as a concession --- it is where this README's mechanisms
have come from, where the run is where its figures come from.** An evening
produces figures and, often, no mechanism, where an hour or two of probes after
it can settle standing questions and refute the evening's own claims.
So a question with a discriminating measurement deserves a filtered run now
rather than a slot in the next full one.

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
so outright, and says what it changes: a retirement decision headed *before
the gate is paid* was once read as a stop and lost the night (2026-08-24), where
the test says plainly that a manifest edit due at the write-up changes nothing
the evening does.

**Confirm each long process on the screen as it finishes**, rather than folding
it into a later summary. The gate, the sequence, a rebuild, any probe that takes
a window: say that it finished, what it exited with, and whether its counts
were what the roster asked for. They run for tens of minutes to hours, and while
the rest is in progress their completion is the only thing a reader can act on.


### Other toolchains, probed and not run

**Two of these three paragraphs are probe records and not run instructions**,
which is why they sit here rather than in [Running it](#running-it). Their
figures are a probe's on another compiler or another backend; no run here
replaces them, and what would call for re-probing is a move in either toolchain
rather than a run. Read them when a toolchain question arises, and not
on the way to an evening. **The HEAD paragraph is the exception**: a pair's half
is built through the project file it names, so the file rather
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
and so refuses every other compiler. Two of its lines are the ones a session
would not arrive at by itself: `hashable ==1.5.0.0`, because 1.5.1.0's cabal
file does not declare the `ghc-bignum` its source imports and so does
not compile here at all, and `-frebindable-known-names` for data-default-class
alone, whose cabal file declares no `base` and which therefore cannot compile
with base hidden. head.hackage is neither needed nor helpful --- its index here
is stale enough that the tarball hashes no longer verify. Why each line is there
is in the file's own comments, so a session building on HEAD reads that
and not this.

**And what the vecdims family reads under each, from probe legs and not
from a recorded run** (2026-08-21, one bench per process so that every arm sits
at the same slot, on a machine that was not idle). On the native backend
`-add-both-down`, `-add-both` and `-add-out` follow `mut-odo-vecdims` 6 to 11%
behind (its pair with `-add-in` is [its entry][open]'s). Under LLVM with 64-byte
loop heads `mut-odo-vecdims` and `-add-in` tie, the in-process
and one-per-process legs straddling 1, and the other three sit 8 to 11% back
in an order the two legs do not agree on --- so their losing is the durable
reading and their own ranking is not. In absolute terms the winner's fill, read
off its `-nosum` leg so that no forcing pass is in it, runs about 0.90
of its native-backend self and is ahead on all but three shapes; that figure
crosses compiler, backend and dependency set at once, and its two windows
are an hour apart on that same busy machine, so read it as a direction
with a magnitude and not as a measurement of the backend.


### The reader: read-run.py

Every figure below comes out of `read-run.py` in this directory, and the run
file's tables are *emitted* by it rather than copied from them. **Use it; do
not write another reader.** It reads two documents --- this file and the run's
own, `runs/run<N>.md` --- and knows which of them a mode's subject is in,
so a caller names a paragraph and not a file. The definitions it encodes ---
which cells the column caps, that `CI%` is a mean half-width rather
than a bound, that `alloc` needs an `l` the JSON does not carry (it parses
`Main.hs` for it), that the `*-aa-*`, `sum-only*` and `*-nosum` rows
are controls, that every ratio is net of the forcing pass while every other
column is raw --- each cost a session to settle, and an ad-hoc script gets them
subtly wrong. Its docstring is the reference for all of them; extend the script
rather than starting over.

**`defects.py` is the one exception to that, and it is where a defect
of the reader goes.** `--selftest` asserts a run's numbers and calls no checker,
installer or flag guard, so the corpus drives every script here from outside,
exit code and stderr included, and `defect-run.py --audit .` replays each case
against the commit BEFORE its own fix, where it must fail --- which is what
makes a fix's proof outlive the commit. The corpus is a Python module
on the shared record form, so its fixtures stay callables that derive
from the live documents and the story of each case stays beside it; the runner,
the validator and the lint are the shared tools, and `check-all .` runs what
`checks.py` lists, `check-all checks-deep.py` what `checks-deep.py` does.
**The case comes before the fix**: a claim that turns out wrong costs one case
rather than one implementation, and a fix without one can come back.

    defect-run.py .                         # the scripts' own defect corpus,
                                            # every case, minutes -- which is
                                            # what the two below are for
    defect-run.py --changed[=REV] .         # only the cases whose own script
                                            # differs from REV, HEAD by
                                            # default: what an edit owes
    defect-run.py -k SUBSTRING .            # the cases whose id or name
                                            # matches, for iterating on one
                                            # checker; it refuses a pattern
                                            # matching none, but a pattern
                                            # matching FEWER than you meant
                                            # is yours to catch
    defect-lint.py .                        # and the shapes these defects
                                            # keep returning in, over the
                                            # Python source: the only one
                                            # of the three that names a
                                            # site nobody has looked at
    ./properties.py                         # and its properties, over every
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
    ./read-run.py --run-doc runs/run24.md ANY-OF-THE-ABOVE
                                            # which run's file to read or
                                            # write; the newest in runs/
                                            # by default, and the only
                                            # document --in-place writes
    ./read-run.py --para 'the floor is'     # the paragraphs whose bolded
                                            # lead matches, in EITHER
                                            # document, and their lines
    ./read-run.py --cross-classes --classes A.json... --others B.json...
                                            # the class section's intro
                                            # figures, aggregated from the
                                            # same per-class rows the
                                            # cross-half lines print, so the
                                            # two cannot part -- counts, the
                                            # geomean range with its classes,
                                            # both extremes with the
                                            # degenerate arms named and kept
                                            # out, and every class whose
                                            # `list` is past the 0.7% bar
    ./read-run.py --section 'Provenance'    # one section's PROSE, without
                                            # its tables, naming the size it
                                            # withheld -- the mode that makes
                                            # the reading a run owes takeable,
                                            # a line range being unable to
                                            # skip what sits between the
                                            # paragraphs it spans.
                                            # --with-tables adds them,
                                            # --with-tables N one of them
    ./read-run.py --delete ANCHOR           # delete the paragraph carrying
                                            # ANCHOR: --replace's counterpart,
                                            # refusing a list and anything
                                            # past --delete-limit, so removing
                                            # a paragraph is never a byte
                                            # range between two markers
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
not need them. An `--in-place` install extended that from rows to prose,
the reading under a lead being the reader's sentence and not the author's.
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
questions. **Reach for it instead of writing a script.**

The interval wants multiplying before it is believed, and `--aa` says by how
much: the A/A pairs are the only comparisons whose true answer is known
to be exactly 1, so they are the only place an interval can be held
to an answer. `--aa` reports whether each covers 1 and how its half-width
compares with the spread the pairs actually show, which turns the floor
from a threshold someone chose into a factor a run measured. Read that factor
as an order of magnitude: it rests on eight pairs.

`--markdown` renders the same rows the plain table does, from one shared call,
so the published figures cannot drift from the terminal's. It reads the Results
table already in the run's file for the one column a run cannot know --- `needs`
--- and for which rows the prose emphasises, carries those forward, and says
on stderr what it could not: a strategy new to the roster comes out with `?`
to be written by hand, and one that has left it is dropped with a warning.

**A run artifact is made when a question needs it**, and the reader is built
for a partial run as much as a full one:

    micro --json RUN.json                                    # the whole thing
    micro -m glob 'cnn-slice-c32/list' 'cnn-slice-c32/bq-expand' --json x.json

**Quote every glob**, as those are: unquoted, the shell expands them first,
and in this directory `*/build` becomes `dist-newstyle/build` while `*/mut-odo`
finds no match and survives --- so one arm silently leaves the run and criterion
reports nothing wrong. The general guard is to count what a filtered run
selected before reading it ([the procedure](#making-a-major-benchmark-run)),
which catches this and the repeated-`-m` mistake alike.

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
silently: is every arm named somewhere in the two documents; is every strategy
defined in `Main.hs` rostered, so that none is left neither timed nor checked;
does each A/A control run the same function as the arm its name duplicates;
and is every control named as the reader's own control test reads it, since
a renamed one would enter the aggregates as a strategy. An arm rostered
and deliberately not timed is a note rather than a failure, and since the two
rulings that note is the larger half of the strategies: it prints the split
and wraps the names, being the one place the checked-but-untimed set is listed
at all.

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
names after.

**`--lint` does not ask whether every benchmarked strategy is also held
to the reference by `check`**: one list, `roster`, builds both, so that drift
cannot happen, and a check that cannot fail is a silent search.

That is the standing rule for everything under `--lint`, `--selftest`,
`--check-doc` and the `health` warnings, and it is why each carries a recorded
proof in its docstring: **a new check is not finished until it has been made
to fail on purpose**, with what was broken and what it then said written down
beside it --- **written down AFTER it has been run and quoting what it printed,
never as the plan for running it**. That distinction is not pedantry: a proof
composed in advance reads exactly like one performed, and nothing downstream can
tell them apart. Several here can only fail on data no real run produces ---
a forcing term larger than the cell it is subtracted from, a term that does
not scale with `l` --- so provoking them is the only way to know they are wired
to anything. It reaches a pass run *by hand* too, which has the same failure
and no exit status to hint at it: before calling one clean, break something
it ought to catch and confirm it says so. And it reaches a check's every
*branch*: the path check's absent-sibling arm is exercised by pointing its roots
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


### Reading a run file

What a run's own file stands on and does not restate: how its tables are read,
the rulings its comparisons rest on, and the form its class section keeps.
It is here once because none of it changes with a run, and the run file links
it where it applies.

**The words a run file uses and the bars it reads against, once.** A **point**
is a hundredth of a ratio: a cross figure of 1.2926 is `list` 29.26 points apart
between the halves, and a gap between two ratios is their difference times
a hundred, so `moved 29.61%` and `29.61 of a point` in one block are one
quantity on one scale. **Every ratio is written A over B, below 1 meaning
A is the faster**: a cross figure is the basis over the control, so above 1
is the control, the flagged half, the faster; a cross-run figure is this run
over the earlier one; a `--pair` figure is its first-named arm over its second,
as property 1's `mut-odo-vecdims` over `bq-expand`. **A strategy** is any arm
that is not a control --- not an A/A copy, a `sum-only` half or a `-nosum` twin
--- and `N of 8 strategies` counts those carrying a corrected time, `list`
included; the Results table's rows are every timed arm, controls and reducing
consumers too. **A family** is an arm with its A/A copies,
as in `the bq-expand family`; **the vecdims arms** are `mut-odo-vecdims`
and the arms refined from it, whose best rival the `best outside vecdims` column
names --- dated accounts written before 2026-09-26 call them the family.
**The shipped leaf** is `mut-odo-vecdims-add-in-leaf-u2`, the vecdims arm fixed
on 2026-08-24 as the form of the fix to ship, and it keeps the name whatever
the library's driver has since been ported from. **The preamble**
is the saturating spray a process under `SATURATE=1` makes before its first
bench, **the victim** the one bench it then times, `vgg-14-c512-k3/list`,
reported on the process's `@@saturate` line, and **the plateau** the state
that leaves, which `read-all.sh` gates by every process's victim reading inside
5% of the run's; **the riders** are the alone legs after the sequence, each
shape's `list` alone in a process of its own, clean and saturated, off which
`--deflation` splits what the preamble and the roster each cost a process.

| bar | unit | what it bounds | where it is read |
|---|---|---|---|
| the A/A floor | % | whether two rows of ONE process's table differ; the widest an A/A pair parts over the eight pairs, per population and half | `--aa`, `--floor-pairs`, [the floor section][floor] |
| the carry-back figure | % | nothing: the same over the four pairs that carry back to Run 10, kept as a series across runs | `--record floor` |
| the A/A bar | points | whether an arm moved between TWO files further than its own A/A copy did in that same comparison; a class block's `A/A bar` is this, per class | `--compare`, under its table |
| the 0.7% bar | % | whether two files' columns may be subtracted: `list`, the denominator, sitting still between them | `read-all.sh --brief-facts`, each class block's `Across the halves` line |
| the drift band | % | whether an arm moved between two RUNS: 3.3%, Run 11's, what `--bridge` prints against; 2.1%, Run 23's reading on one binary; 3%, what `--half-movers` flags at | `--bridge`, `--half-movers` |
| the wider floor | % | a margin across a pair's two halves on a class, held to the wider of their two floors | [the floor section][floor] |
| a registration's band | % | whether a prediction held, one per `predict:` span | `--predictions` |
| the machine bars | % | whether the box moved: 5% a shape, 3% the geomean, `list` against the kept fingerprint | `--machine`, `run-gate.sh` |
| the plateau band | % | whether every process started from one state | `read-all.sh` |
| the worst-cell gate | % | whether an A/A cell, at about 10%, leaves the per-shape record | [the procedure][procedure] |

**The Results table.** How to read its columns, the `needs` column's own gloss
being under the run file's properties with the tier it splits:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*,
  less that shape's forcing term, over `list`'s slope less the same term,
  with the per-shape log-ratios *winsorized* first --- capped at the row's own
  median plus or minus three MADs, the MAD scaled by 1.4826 so the cap
  is in standard deviations. Nothing is dropped by the estimator, so winsorizing
  costs no row its population and a cell far enough out to distort the mean has
  its influence bounded instead of its evidence deleted. What can cost a row
  shapes is the correction and not the estimator: a cell the shared forcing pass
  is not smaller than is dropped from its row and named. The `CI%`, `smp`
  and `alloc` columns stay raw: subtracting a shared term moves a point
  estimate, it does not make a cell better measured. `worst` is a ratio of nets,
  as `time` is, just per shape and unwinsorized.

  **This replaced a trim** --- drop each strategy's single highest-CI shape ---
  and the ruling is worth keeping because the trim looks obviously right
  and is not. It selected on CI, and criterion spends a *time* budget, so a slow
  cell buys fewer samples and a wider CI: measured on Run 6, the cell it removed
  was above its own row's geomean in **30 of 41** rows, p about 0.003.
  It therefore deleted each strategy's worst evidence, differentially,
  and a catastrophic shape is exactly the shape it would remove:
  `bq-expand-lemire-out` loses on one shape of 33, and that shape was the one
  trimmed from its column. Because the cell removed differed by row, two
  published columns were also geomeans over different shape sets, which is why
  a published A/A ratio used to disagree with its paired one. Swapping
  estimators costs a median 2% and moves one row (`mut-offsets`) by 14%,
  that row having been flattered all along; it buys back exact comparability,
  and `--selftest` now asserts published == paired for every uncapped pair.

  **Don't reach for inverse-variance weighting**, which is the standard-looking
  repair and is worse than what it repairs. It assumes every shape estimates one
  ratio and differs only in precision, where here the between-shape variance
  runs a median 5,000x the within-shape kind --- the heterogeneity
  is the README's finding, not its error --- so weighting by precision collapses
  the effective shape count from 33 to about nine and hands a quarter
  of the weight to the smallest shape in the set. Worse for the purpose:
  a catastrophically slow cell buys fewer samples, so it has a wider CI, so IVW
  discounts precisely the cells the trim used to delete --- the same failure
  made continuous, not a repair of it.

  **The *slope* rather than criterion's mean, because criterion never times one
  call**: it times batches --- one call, then four, then twenty --- and every
  batch also pays for starting the timer and for the first pass through cold
  code and cold data. A mean divides each batch's time by its calls,
  so that fixed cost is smeared across them and weighs most in the small
  batches. The slope is the line through those points: how much more time one
  *additional* call adds, leaving the fixed part behind as the line's height
  at zero. On the microsecond shapes, hundreds of samples and no warm-up worth
  speaking of, the two agree. They part on the slow shapes, where the early
  batches run cold: there the mean reads high, and by different amounts
  for different strategies --- which is exactly the part that dividing by `list`
  cannot cancel. It also keeps `CI%` and R^2 describing the number the table
  shows, both being properties of that same fitted line.
- **worst** is the row's largest per-shape ratio to `list` --- the shape
  on which that strategy does least well against the baseline. It is what
  property 1 is about, and it is raw rather than winsorized.
- **CI%** is the median across shapes of the slope's confidence half-width
  as a percentage of the slope --- "how many digits are real". 0.5% is three; 5%
  is one.
- **smp** is the median sample count. Criterion spends a time budget, so a slow
  call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`),
  the median over shapes of the `allocated` fit the harness now runs on every
  bench of every shape. **So two of its entries are not to be divided either**,
  for the same reason the `time` column's are not: a median is not a geomean
  of ratios, and on Run 36 dividing the two halves' published `bq-expand` tiers,
  2.11x by 2.78x, gives 0.759 where the per-shape geomean of that arm's
  allocation across the halves is **0.8119**. What answers a cross-half
  allocation question is `--compare --alloc --per-shape`, which prints
  that geomean per arm; the tiers answer what an arm allocates WITHIN one half,
  and a run that wants both quotes them as two statistics. **The multiples
  are not shape-independent**: every row varies by more than 5% from shape
  to shape, the median row by 2.00x on Run 9's cells, and four shapes
  of identical `l` = 1800000 give `bq-expand` 2.000x, 2.111x, 1.000x and 2.639x,
  every allocated fit at R^2 1.000 --- so the spread is the quantity and
  not the measurement, and allocation being deterministic per call the budget
  does not bear on it either way. What does survive is the column: a median
  over a *pinned* shape set reproduces, every allocation tier returning
  on its own level across a roster change. So read `alloc` as a statistic
  of a strategy **and** a shape set, and pin the shape set before comparing
  it across runs, exactly as the `time` column already asks. It is the one
  column the correction does not touch.

**It is the main set's table**, and every column of a run file's Results table
is a statistic of that population: each stride class has a table of its own,
on the same rows and in the same columns but its own basis, under the run file's
*The stride classes, run by run*. No figure crosses between them.

**What the next run compares against.** Four rulings stand under that section's
comparisons, and two notes on its tables follow them.

**No roster-order pair is owed for the position term**: what Runs 14 and 15 saw
is small-pinned churn, priced per shape by filtered scans without a pair ([the
open list's small-pinned churn entry][open],
`small-pinned-churn-investigation/nursery-position-findings2.txt`).

**No further allocation-area pair is owed**: the area was priced by Runs 14
and 15, Run 15 finding it about 6% of the roster's time, and was fixed
at `-A32m` outright on 2026-08-21, here and in every horde-ad suite.

**Where a run changes basis, the new basis is checked against the previous half
at its OWN allocation area and against no other**: distance from a half
at another area is that area plus whatever else moved, Run 16's three anchors
reading within a percent of the half at their area and 8 to 10% from the half
at another; only distance from the half at a run's own area is drift.

**A pair's two halves are never folded into one.** Merging them puts back,
in the record built to outlive every artifact, exactly the term the pairing
exists to separate --- and what a given pair's two columns price is that run's
own file's to say, not this section's. `--check-doc` catches one half of it:
a run named aligned must also be named unaligned. Pruning an aligned column,
merging two, and naming a second half accurately are the reading's to catch ---
the check cannot demand an unaligned half of every pair, most having none.
**Widening it to other half names was refused on 2026-08-14**: it would have
to know which names count as a counterpart, a list that grows with every pair
and is wrong the first time one is invented, so a basis column keeps the name
`aligned` where it is aligned and the other half is named for its shim.

**Every table a run's file publishes is installed, and two of them only by their
rows.** `install-tables.sh` writes the Results table, the fingerprints,
the class tables and the cross-class summary whole, the summary off each class's
own block; the two-column table under *What the next run compares against*
and the Provenance anchors are installed by `read-run.py --hand-tables`, which
rewrites their rows off the two main JSONs and leaves their headers and leads
to the prose, and which checks them without `--in-place`. A table row edited
by hand anyway is edited with the whole line named, never with a prefix anchor,
which can match an earlier table and put cells into another table's header.

**The two-column table is two orderings and not two speeds.** Each entry
is that arm's net over `list`'s net in ITS OWN half, winsorized per row within
that half, so dividing an arm's two entries reproduces neither its `--compare`
figure nor anything else; which half runs an arm faster, and by how much,
is `--compare`'s paired ratio, where the reference is not divided out. The two
columns may be SUBTRACTED only where `list` moved under the 0.7% bar between
the halves, the two sharing a denominator then; a pair whose variable moves
`list` past it --- every regime pair here --- is read side by side,
and a control column printing higher is the denominator shrinking under
it and not an arm slowing.

**Each stride class has its own table in a run's file.** Every run re-runs every
class with the populations pinned, so each class's paragraph carries what
the last change moved and its table is what the next run reads against.
**A class figure compared across the Run 11/Run 12 boundary is not compared
on one build**: Run 11's class tables are its *aligned* half's and Run 12's
its *max-skip* basis half's, and the main set prices that difference at nothing
below 0.99 and up to 1.06, so a point or two of movement across that boundary
is the shim rather than the class. From Run 13 on, every run's class tables
are its own basis half's.

And because a geomean cannot say *where* it moved, the **fingerprint**
in that section is kept so a future disagreement can be localised rather
than only noticed; its membership rule, the column heads and the rulings
on dropping a column are [in the per-shape section][pershape]. Its two tables
are installed from the run's own JSONs in the per-shape form that section
describes.

**The properties.** `--pair` works within a class JSON exactly as within
the main one, and is still the way to compare two arms; its bootstrap interval,
over three shapes, is worth less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier
in two. A **new pure `Vector` method** delegates to a pure function the vector
package already ships for every carrier --- `unfoldrExactN`, `backpermute`,
the `concatMap`/`enumFromStepN` pipeline --- so it fights only *minimal*
in orthotope's pure-and-minimal API rule; the **new mutating `Vector` method**
the direct fills need is the [mutable ceiling](#the-mutable-ceiling-taken)'s
ask, which the decision of 2026-08-22 takes. `offtab`
is the `Vector`-class-expressible shape of these gathers --- output by plain
`vGenerate` over a concrete offset table --- so its own cell names only
its mutable `Int` scratch. And the geomean weights every benchmarked shape
**equally**, so a figure here is a ranking statistic, not a claim about total
work saved: the small shapes count as much as the largest.

**The stride classes, run by run.** The section opens with one table over all
the classes, so that an inversion is visible without reading every class's
table. Every figure in it is transcribed from a class's own table --- none
is computed there, and none is an average across classes, there being no such
population to average over. Its header, fixed here so a run fills rows and never
reshapes columns:

**The cross-class summary's columns.** `mut-odo-vecdims` and `worst`
are that arm's two columns in that class's table; *best outside vecdims*
is the leading arm outside the vecdims arms, what the dropped stride-conditioned
redirect would have taken, and *ceiling* the leading arm OF the vecdims arms,
each with its name --- and both are read over the POPULATION, so the arm named
may lead on no single shape and the per-shape fingerprint under *What the next
run compares against* may name another, which is [the per-shape
section][pershape]'s own point and not a disagreement; where an arm outside
the vecdims arms leads, the two name different arms and the gap between them
is what the lead is worth, and never one arm in both columns. *floor*
is the largest deviation from 1 among that process's A/A controls. The row's
fastest timed arm is bolded, ruled 2026-09-27: it is always one of the two named
cells, `best outside vecdims` or `ceiling`, and the install decides between them
on the unrounded values, which `--block`'s `summary bolds` line and the `bold`
column of `--extremes` print where the two tie at three decimals.

    | class | shapes | mut-odo-vecdims | worst | best outside vecdims | ceiling | floor |

**The aggregate figures in the paragraph above the blocks are the reader's,
emitted rather than assembled.** `./read-run.py RUN --cross-classes` prints
every one of them --- the comparison count, the faster/slower split, the range
of the geomeans with the class at each end, the arm holding each extreme and how
many populations share it, the degenerate arms it kept out, and the classes
whose `list` is past the 0.7% bar --- from the same per-class rows the blocks'
cross-half lines print, so the intro and the blocks cannot part;
and `install-tables.sh` installs the clause quoting the count, the split,
the range and the extremes, as `--cross-classes` prints it on its `lead:` line,
leaving whatever the author writes after it. The comparison count,
the faster/slower split, the range of the geomeans and the extreme arms are each
an aggregate over the blocks' `--block --compare` lines, one per class, so they
are read off those lines and never off a population assembled for the purpose.
Where a figure genuinely cannot come off those lines, because a class's own
maximum is a degenerate cell, the paragraph says so rather than quoting
it as though it could.

Then one block per class, in `classViews`' order --- which `Main.hs` fixes
and the run file follows, so a class landing or retiring moves the blocks
and not a list there --- each carrying the same six things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause,
   and its shapes with their `l` and `sInner`, which is what makes the table
   under it readable without `Main.hs` open;
2. the table `--block --in-place` installs from `$R-<basis>-$c.json`, whole
   and never edited --- six columns, with the emphasis carried over
   from the main table so the `mut-odo-vecdims` row is found at a glance,
   and `needs` left to that table as a property of a strategy rather than
   of a population;
3. its own controls, off `--aa`: the A/A deviations with their spans, the two
   `sum-only` halves, and the in-situ term from the `-nosum` arms ---
   this process's own floor and its own three gates, neither inherited nor lent
   --- and where the paragraph quotes the OTHER half's figure, it says so
   in the form `the other half's own eight pairs span N%` and never
   with the word *floor* beside the number, which `--check-doc` holds
   to this table's column;
4. its provenance and its anchor: elapsed time and the two heap peaks
   from that process's stderr line, its population's size from the reader's
   first line ([why not both from one place](#making-a-major-benchmark-run)),
   and `list`'s absolute per-call time on one of its shapes, raw and net.
   The main set's three anchors guard a baseline that moves for every population
   at once; this one guards a baseline that could move for this mechanism alone,
   which is the case a table of ratios hides completely. A three-shape class
   adds one line here --- the bolded rows' per-shape net ratios, in the lead's
   shape order --- because its table under-determines its cells, where
   a two-shape table carried them already, `time` and `worst` jointly fixing
   both; every class is three shapes or more now, so the line always prints;
5. the cross-half reading, one line, which `--block --compare` against the other
   half's JSON now emits and `install-tables.sh` writes in with the other three
   --- how many of the population's arms move, which way, and the spread;
   a margin on this line is judged against the WIDER of the two halves' floors
   ([the floor section][floor]). This is where a pair's variable acting
   on a class and not on the main set is read. A run whose halves differ
   in nothing a class can see says so in a clause;
6. one paragraph of what the class says, and none where it says nothing,
   the install's skeleton then being deleted: an ordering that inverted,
   a `worst` above 1, an allocation tier that moved, a mechanism showing through
   a single cell. A class that reproduces the main ordering gets one sentence
   saying so, that being a result and reading as one.

`./read-run.py RUN.json --block --compare OTHER.json` assembles items 3 through
5's mechanical parts and item 6's figures, its counts geomean where both sweeps
are given with `--counts`, and `install-tables.sh` writes them in in one call
--- table, controls, the provenance and anchor skeleton, a three-shape
population's per-shape line, the cross-half line, and item 6 with `___` where
the finding goes, over the carried paragraph or an unfilled one and never
over a written one; the lead and the finding stay the author's. Item 2's own
table is NOT among what that call prints, which is why the list above starts
where it does: it comes from the separate `--block --in-place` call item 2
itself names. **The cross-half line carries its own disqualification**: where
`list` moves more than 0.7% between the halves the line says so and says
it is not read for the pair's variable.

The blocks carry no headings of their own. One per class would crowd
the contents and the replace list alike, where a bolded lead reads the same
and lets one link cover the section --- which is what `--check-doc`'s coverage
check counts.

A floor's movement between runs is not a sentence under the table: what moves
the floors is [an open question][open], and `--check-doc` holds any such
movement a run writes to the class table's own column.


### What moves a figure when no strategy changed

**And one thing that moves a COUNTED figure when no strategy changed, found
2026-08-30 and not previously suspected: the assembler shim's own padding.**
`run-counts.sh` counts retired instructions, and a padding nop retires.
**And where it lands is the INNERMOST loop's own back-edge cycle, not some outer
one, which is the whole reason it is worth percent and not parts per million.**
These fills are test-first, so the block a loop is ENTERED at is its latch,
and the latch sits mid-cycle: the body falls through to it and it jumps back
to the body. Aligning an entry target therefore pads BETWEEN the body
and the latch rather than before the loop, and nothing branches over it --
on `slice-primes`'s fill the body's last instruction, `add $0x2,%rsi`, falls
straight into the nops. So the pad is paid once an ITERATION, which here is once
per two elements. Two arms whose bodies end at different offsets modulo
the boundary get different pads, and that difference is paid at the same rate.
**And the shim is not misidentifying the head, which is the first thing to check
and the answer changes what a fix would be.** Its rule is *a local label a later
instruction jumps backwards to*, and the padded block IS one: on `slice-primes`
the block at the fill's latch is the target of the RUN loop's own backward jump,
so it is that loop's head, correctly found. What the rule does not account
for is that GHC laid the two cycles OVERLAPPING rather than nested ---
the fill's latch is the run loop's head, so the run cycle begins inside the fill
cycle and ends after it --- and a pad before a head in that position is paid
on the OTHER loop's iterations, amplified by its trip count and not
by the padded loop's. Ordinary nesting is the opposite and is what the shim
is for: an inner head inside an outer cycle costs one pad per outer iteration,
which is the trade it was built to make. **The two are told apart
by a containment test on data the shim already has**, every (head, back-edge)
pair being how it finds heads at all: skip a head whose own cycle `(H, J)`
overlaps another `(a, b)` with `a < H < b < J`, and leave the nested case alone.
**The dead-spot form, `LOOP_DEADSPOT=1` ([the open list][open]), keeps that test
and turns the skip into an order: the inner head of a rotated pair is placed
and the outer yields, so on a dead-spot binary the fill's stepping loop sits
at offset 0 and the loop the survey then reports straddling is the outer,
per-run one** --- by design and on every dead-spot build, so a future run should
expect them and price them as a per-run term where the pad they replace was paid
per iteration. **Over this module's assembly that separates 840 nested heads
from 331 overlapping ones, 28.2% of 1172** --- an exposure count from a static
pass with instruction indices standing in for addresses, so a bound on how many
heads could be affected and not a measurement of what they cost. What it would
cost to find out is in [the open list][open]. **Read out of the timed binary
itself**, at the addresses sampling it put the instructions at rather than
in a twin: on `slice-primes` the branch's fill and the shipped fill are the SAME
CODE, sixteen real instructions and four stack accesses per two elements each,
and they differ by one nop, three against two, because one body ends a byte
earlier before the pad. That is **one retired instruction per two elements**,
and it closes the arithmetic with the epilogue term beside it: `slice-primes`
is 2813 runs of 89, so 44 body iterations a run, and 44 x 2813 = 123772 extra
nops plus one extra epilogue instruction a run, 2813, predicts **126585**
against a measured excess of **127331** --- **99.4%**, in two terms that
are the shim's and [the ceiling][ceiling]'s thirteenth reading's respectively,
one paid per iteration and one per run. **The control is a build without
the shim**, roster and `check` identical, where the excess falls to **+0.18%**
from +5.57% -- and the counted ratio of those two arms moves on every
population, all in the branch's favour: the main set 0.672 to 0.652, `rev` 0.940
to 0.908, `revsome` 1.047 to 1.015, `slice` 1.048 to 1.013, `scaled` 1.015
to 0.982, `window` 0.789 to 0.744, `runs` 1.137 to 0.985. **What this does
NOT say is that the shim is wrong or that a figure here is**: the shim
is this benchmark's deliberate instrument, Run 10 having priced layout at 12
to 14% on the arms whose loop it rescues, and every figure in this file is taken
at it, so the no-shim build is a control and never a regime. What it says
is narrower and sharper -- **an instruction-count difference between two
DIFFERENT arms can be padding rather than code, and the counter cannot tell you
which** -- and the practical form is that a counted ratio being used to argue
about CODE wants the no-shim control beside it, where one used to argue about
an ordering does not. **It also refines the layout-independence this file leans
on** [in the parked entry](#non-urgent-todo-list): an A/A pair's counts agree
to 5e-5 because both halves are the same code and carry the same pad, which
is exactly the case that cannot show this. **And what the no-shim build costs
is what the shim was bought for, which the same evening measured**: timed
over `slice` it puts the two arms at 1.0536 paired against the shimmed build's
1.0811 --- so about three of those eight points are the padding, as the counted
work says --- but its floor is **8.36%** against the shimmed build's **4.44%**,
so the five points left are inside it and the un-shimmed build cannot resolve
what the shimmed one can. The per-shape figures say the same thing louder:
`slice-coprime-r7` reads 1.1135 shimmed and 0.9990 not. **So neither build
is the honest one on its own** --- the shimmed one resolves a margin it partly
creates, the other creates less and resolves nothing --- and the pair of them
is the reading. That is the shim's standing rule restated from a new direction
and not a case against it.

Eight A/A controls run an existing strategy twice under a second name --- four
strategies, each duplicated once beside its base and once at a distance,
so position varies within a strategy and strategy within a position.
**The carry-back figure is the floor over the four pairs that carry back to Run
10**, the `bq-expand` and `mut-odo-vecdims` pairs, kept as a series:
a present-tense `carry back` means those four, and a carry-back figure read
across the prune of 2026-09-04, which deleted the twins of every arm it parked,
is over two populations. The table below is the six that carried back on Run 20.
A/A pairs are the only rows whose true ratio is known to be exactly 1 ---
or were, until [the mutable ceiling](#the-mutable-ceiling-taken) turned up
another by accident:

| pair | span | g912 | ghead | mean per cell |
|---|---:|---:|---:|---:|
| `mut-odo-vecdims` vs adjacent twin | 1 | 0.9996 | 1.0001 | 0.39 / 0.43% |
| `mut-odo-vecdims` vs distant twin | 10 | 1.0007 | 0.9990 | 0.60 / 0.84% |
| `bq-scan-rem-gm-mulback` vs adjacent twin | 0 | 0.9988 | 1.0005 | 0.24 / 0.25% |
| `bq-expand` vs distant twin | 41 | **1.0042** | 0.9989 | 0.76 / 0.64% |
| `bq-expand` vs adjacent twin | 1 | 0.9997 | 1.0005 | 0.24 / 0.18% |
| `bq-scan-rem-gm-mulback` vs distant twin | 37 | 1.0017 | 0.9994 | 0.86 / 0.65% |

**That table is RUN 20's**, its two columns that pair's two binaries, which
differ in the compiler and nothing else. Where a pair has a cell capped
its published figure parts from its paired one, and **the margin is the PAIRED
figure and never the published column** --- what a run file's own *DO NOT DIVIDE
TWO ROWS OF THIS TABLE FOR A MARGIN* paragraph says, and what the floor
requires, the floor being defined in that same statistic (ruled 2026-09-14).

**On Run 45 the floor is 0.85% on the basis half and 0.72% on the control,
carried by `bq-expand-aa-distant` on the basis and `mut-odo-vecdims-aa-distant`
on the control, over these EIGHT pairs.** The eight are `list`, `bq-expand`,
`mut-odo-vecdims` and `mut-odo-vecdims-add-in-leaf-u2`, each with an adjacent
and a distant twin, unmoved since the shipped fill's own copies landed
2026-09-09. Over the four pairs that carry back to Run 10 this run reads
the same **0.85%** and **0.72%**, so the whole-set and restricted thresholds
agree on both halves. `./read-run.py --record floor` prints both series, a row
per run from Run 16, and a write-up appends its run's row at post-run step 6c.
**A max over six pairs, one over eight, one over sixteen and one over eighteen
are four different statistics**, so the whole-set column is a series only across
rows of one `pairs` count. **The carry-back column is the series, and it says
where the movement lives**: it has read between 0.21% and 0.83% on the basis
from Run 18 to Run 44, Run 42's the lowest, while over Runs 18 to 24
the whole-set figure, a max over sixteen or eighteen pairs, ran 1.26% to 2.92%,
so the pairs outside the four were what moved. **This run's basis figure, 0.85%,
is the highest the carry-back column has read and it is an intrusion's**:
its pair, `bq-expand-aa-distant`, is one of the two benches foreign CPU met
on `cnn-slice-c32`, and read without that shape the basis's floor is 0.53%,
inside the series. The control's 0.72% is a wild cell's, `mut-odo-vecdims`
itself running 1.043 and 1.045 of its two copies on the mutator clock
on `vgg-14-c512-k3` with no foreign CPU. The worst A/A cells of this run's two
main sets are those two cells, **6.61%** on `cnn-slice-c32` on the basis
and **13.81%** on `vgg-14-c512-k3` on the control. `--floor-pairs` reads
the eight on every population on both halves, and SIX of the eight carry a floor
somewhere, which is the same instability the whole-set figure above reads. **One
cell passes the about 10% past which [the open list][open] takes a worst cell
out of the per-shape record, on the control**, the 13.81% above, so it leaves
that record. **A floor moves on a binary that has not changed at all** ---
by a factor of 1.7 on Run 19, 1.44 on Run 30 and 1.98 on Run 43, its basis
between two main-set processes of one binary --- so no run's floor
is inheritable by the run after it. The threshold this run supports
is the whole-set figure a half, the restricted four-pair reading having closed
on it on both halves --- and since 2026-09-13 a margin between two rows clears
the whole-set one, the carry-back figure being the series and not the bar ([the
open list][open]). Read the floor as the run's *and the half's*, re-measured
every time, never as a constant of the harness and never inherited. **Only
the rows from Run 40 on can still be re-derived**, earlier runs' artifacts
having been deleted at the owner's word, so `--series` starts at Run 40
and every earlier row of `series/floor.tsv` is a RECORD rather than something
a later session can check.

**The 0.7% differencing bar, measured against the pairs it is applied to ---
and it is near the MEDIAN of that population rather than a bound on it.**
The bar decides whether a pair's two columns may be subtracted or only ordered,
and no sentence anywhere said what it bounds ([the open list][open] carries
the question and it is not closed by this). What CAN be said is what
the artifacts say, and Run 29 took it: over the five pairs whose JSONs survive
--- Runs 24 to 28, every one of them varying the COMPILER and so a pair whose
variable is not the reference --- `list`'s cross-half move reads over **54
population readings**, one per population per pair, at a median of **0.64%** ---
the two middle readings being 0.62% and 0.66% --- a third quartile of **1.13%**,
a ninetieth centile of **1.75%** and a worst of **3.27%**, on `reshape1` in
Run 24. **Only 30 of the 54 are inside the bar.** So a pair whose variable ought
not to touch the reference fails this bar on nearly half of its populations,
and the per-run counts are 5 of 10, 8 of 11, 4 of 11, 6 of 11 and 7 of 11 ---
no run of the five clears it everywhere, and none is near doing so. **What
follows for a reader is the ordering and not the bar.** A figure past 0.7%
is not thereby suspect: it is in the company of half the readings this harness
has taken from pairs it trusts, and what the bar buys is a rule that does
not have to be argued per population. What a figure FAR past it means
is a different thing, and Run 29 is the case that separates them --- its 12.12
points on the main set is nearly four times the worst of those 54, and every one
of its eleven populations is past, which no compiler pair on record manages.
**This paragraph is a measurement and not a provenance.** Where the number 0.7
came from is still unrecorded and is still whoever set it to say; what
is settled here is only what it is worth against the evidence, which is
that it sits inside the spread of the thing it bounds.

**Four processes of ONE binary in ONE day put a number on that caution,
2026-09-06** (`probe-within-evening.sh`). Run 26's own basis process at 03:19
and three more at 15:23, 16:12 and 17:01 --- `run26-g912` throughout, 570
benches apiece, every one clean --- read floors of **0.31%, 0.47%, 0.41%
and 0.36%**, a factor of 1.5 with the binary, the roster, the switches
and the day all held still, between Run 19's 1.7 and Run 23's twentieth
and bought without a second recipe or a pair. **The floor stays within 1.2
to 1.7 of the sampling under it**: the median A/A half-width in those same four
processes reads 0.21%, 0.28%, 0.33% and 0.24% and the reader's own
understatement factor 2x, 2x, 1x and 1x, so the floor is the order statistic
over that sampling rather than a large term of its own --- [the class-floor
entry][open]'s *a floor is an order statistic and not a spread*, met a second
time and inside one binary instead of across a pair's halves. **What it
is NOT is a copy of that sampling step for step**, and the three afternoon
processes are where the two part: they fall 0.47%, 0.41% and 0.36% where their
own half-widths go 0.28%, 0.33% and 0.24%. That fall looked like a law for one
evening --- 8 of 8 consecutive steps down over three blocks --- and did
not survive being repeated over four classes on two recipes, which [the
class-floor entry][open] carries. **What that fall is NOT is a general drift
down an evening**, and the reading that says so cost nothing: over the 64
recorded processes of Runs 24, 25 and 26 the rank correlation of a process's
position with its floor is -0.04, and with the saturating preamble's victim
reading about as little, so the box does not drift and neither does the figure
([the class-floor entry][open] carries the counts). **The same 64 processes do
confirm what this paragraph is about**: floor against the median half-width
beneath it correlates +0.26, +0.49 and +0.52 by run, so the order-statistic
reading holds across runs and compilers and not only inside this one binary.
**What the process does not move is which pair carries it.**
`bq-expand-aa-distant` carries all four, as it carries both of Run 26's halves
above: 1.0031 with its interval covering 1, then 1.0047, 1.0041 and 1.0036
with theirs missing it --- so that slot is worth about +0.4% and repeats where
its size does not. **A per-process term is not resolved by four processes**,
and saying which pairs carry one depends on the test: no two of the four have
disjoint intervals for any of the six pairs, while the tightest interval
of a pair excludes another process's estimate for two of them. The widest
movement is `mut-odo-vecdims-aa-distant`'s, 0.9985, 0.9958, 1.0006 and 0.9970,
which the tightest of its own four intervals --- 0.9970 to 1.0000 --- excludes
at both ends; `bq-expand-aa-adjacent` is excluded at one end and the other four
at neither. So *read the floor as the run's and the half's* takes
*and the process's*. **What survives a process is which pair carries the floor
and not the order beneath it**: `bq-expand-aa-distant` leads all four, while
`mut-odo-vecdims-aa-distant` ranks 3rd, 2nd, 5th and 2nd of the six across them.

**The twins' direction is a coin**: across Runs 10 to 20 the pairs read above 1
and below it in every arrangement, the code, the layout and the roster order
held fixed across the flips, so the direction is a property of none of them.

The pairs' intervals understate run-to-run variability: an interval measures
sampling error *within* one benchmark, while two separately placed benchmarks
also differ in code layout, cache occupancy and inherited GC state. The A/A
is the only column that sees that, and `--aa` prints the calibration outright
--- the observed spread over the median interval half-width, a factor that has
run from one to twelve across runs and halves, four and six on Run 24's two ---
so multiply any interval this reader prints by about that before believing it.
**That the two halves DISAGREE on the factor is the ordinary case**,
and with only a handful of pairs one loose pair moves it far.

**The class populations are where the factor bites hardest**, for arithmetic
rather than noise: a two- or three-shape bootstrap gives an interval far
narrower than the spread those shapes actually show, so the factor --- five
to twenty-three across classes on Runs 16 to 21, never staying with one class
--- reports which slot happened to be disturbed rather than the reader's
arithmetic. Read a class interval that misses 1 as the reader's arithmetic
and the pair's own deviation as the finding. The blocks print a floor, a worst
cell and an interval count, and no factor.

**And what is left when every other cause is pinned has now been measured twice:
run-to-run drift is a few percent per cell and under a point on most geomeans.**
Run 11 re-ran Run 10's aligned binary with shapes, roster, order and regime
unchanged, so its every movement is drift and nothing else. `list`'s per-shape
scatter is **0.958 to 1.043**; of 762 cells, 495 are within 1%, 693 within 5%
and 743 within 10%; every arm's geomean is within 1.5% but `mut-odo`'s 1.0327.
Run 23 re-ran Run 22's basis binary the same way, two evenings apart, and reads
its `list` at 0.9962 with a per-shape scatter of 0.983 to 1.019, 44 of 49 arms
within 1% of their Run 22 geomean over the 23 shapes the correction leaves
readable, and the widest non-degenerate arm at 2.08%, `gen-unsafe-aa-adjacent`
--- the two `libunord` arms sitting apart at 0.58 and 0.68 because a cell
that is its own forcing term moves a hundredfold between evenings and is
not a measurement. That is the figure to hold a *later* margin against,
and it is a quarter of the 0.902-to-1.181 band Run 10 had to quote when
the roster order moved the layout underneath it. Two consequences worth keeping
when the run file carrying them is replaced: a margin of a few percent between
two runs is still not evidence, and a margin between two *arms* of one run has
to clear the whole-set floor of the half it is read on (ruled 2026-09-13),
the carry-back figure being the series across runs rather than the bar.
**The two are one on both halves of Run 45**: 0.85% and 0.72% are the widest
an arm differs from its own duplicate by on each half over the eight pairs
this roster carries, `bq-expand-aa-distant` on the basis
and `mut-odo-vecdims-aa-distant` on the control, and the four pairs that carry
back to Run 10 read the same, the same two pairs carrying them ---
so the restriction costs nothing on either half of it, where on other runs
it has parted on one half or both, the whole-set figure being the conservative
reading --- and 2.1% is the across-run drift band an arm must clear to have
moved between runs on this box, Run 23's one-binary reading, where Run 11's
was 3.3%. **All three are the word *floor*, over different populations, and two
things that are not it wear it easily.** A class's `floor` column is the same
statistic again over that population's A/A pairs, so it is a fourth member
of the family and not a fourth sense. **And a margin read ACROSS a pair's two
halves on a class is judged against the WIDER of the two halves' floors,
and a registration's kill condition on a class says so**: the narrower floor
is the one that makes a kill and the wider the one that makes a tie honest,
and a pair whose halves' floors differ threefold --- Run 23's `reshape1`, 3.09%
on the basis and 10.75% on the dead-spot half --- is exactly where a reader
should not get to choose (ruled 2026-09-02). **The worst single A/A cell
is not a floor at all** --- 16.66% on Run 24's basis main set and 19.72% on one
of its class processes, against 2.04% and 5.48% on Run 25's two main sets ---
and the procedure says so where it is read; it is one cell where
these are geomeans over a population, and quoting it as one overstates
the instrument by an order of magnitude. Nor is the residue [the alignment
question][open] asks about, which is an effect size that survived a control
rather than a spread the run measured. The exceptions are `build` and `mut-odo`,
one worker at two slots, whose cells reached 1.092 on Run 23's basis and 0.828
on that run's dead-spot half, though post-run step 3a names the tracked two-copy
group off a `-g3` twin as `fbBuild` and `fbMutOdo`, both at offset 0 in their
cache line on BOTH halves of Runs 21 to 23. So the residue the pairing cannot
reach is not a cache-line offset; what Run 23 adds is that placing every OTHER
pad off the execution path opens the pair from a tie to 0.9449 on the dead-spot
half, and what it is remains [the open list][open]'s.

**A busy machine smears and the wild cell does not.** A main set taken
on a machine that was not quiet, read against the same binary's recorded one
(Run 11), raised the floor from 0.22% to 1.11% with 50 of 762 cells more than 5%
slow, scattered over shapes and arms while every arm's geomean stayed inside 2%;
the wild cell is one bench, its interval a twentieth of a microsecond,
its neighbours and its own twins clean --- which is why it is a finding
and not noise.

**The cold block pool behind the Run 8 and Run 9 wild cell** (2026-08-09, Run
9's binary): `bq-expand`'s distant twin, at roster slot 3, read 41% above
its base on `vgg-14-c512-k3`, deterministically, and the slow figure
was the arm's real isolated cost, the base being the flattered one; the whole
expansion family is susceptible, `bq-expand-gm-mulback`, `bq-expand-qr-prim`
and `bq-odo-gm-mulback` reading 35--40% above their published cells where
`bq-scan-rem-gm-mulback` and `mut-odo-vecdims` do not move; and one predecessor
does all of it, `sum-only-early`, whose one `l`-sized setup allocation grows
the block pool and leaves it grown --- [the position effect][pos-effect]'s
mechanism, the binary identical throughout. **So `sum-only-early` runs directly
after `list` and ahead of the twins**, which took the cell from 41% to 0.24%
on the same three-bench probe; the reasoning is at its roster entry
in `Main.hs`. The fix removed the slot and not the family's susceptibility,
which [the open list][open]'s transient entry carries.

**An arm allocating more per call beyond its result than the nursery holds pays
for it in KERNEL memory management** --- not in GC time, 5.8% of the cold
process, and not in the heap size, `-H512m` doing nothing. On `vgg-14-c512-k3`
the default 4 MB area cost `bq-expand` 0.36 ms of system time per call against
an excess of 13.2 MB a call, where `-A32m` cost none, which only a wall-time
or user-and-system differencing sees. **The predictor is that excess against
the area**: `cifar-L2-16-c64-k3`, at 1.59 MB of excess, shows neither kernel
time nor benefit, and excess allocation is linear in `l` to three digits
over a 32x range. **`-A1G`'s cliff is `micro.cabal`'s `-M2G` cap and
not the nursery**: at identical work its gen-1 collections go from 2 to 31,
and at `-M8G` it rejoins the other areas. **At a caller's scale `-A32m`
is not the cheapest area**: on `imagenet-224-c64-k3`, `l` = 28.9M, it runs 18%
behind the default on 31 ms a call of kernel time where 64 MB pays none,
so the threshold moves with `l`, though far from linearly. The area is fixed
at `-A32m` all the same (2026-08-21), the churn tax below outweighing that cost.

**The published ratios are a statement about the allocation area, `list` being
the most nursery-sensitive arm here**: a cons list of `l` elements is nothing
but small-object allocation, and on `vgg-14-c512-k3` `list` runs 1.79x faster
at `-A32m` than at the default where `bq-expand` gains 10%, so `bq-expand`
over `list` reads 0.098 at the default and 0.157 at `-A32m` --- both true,
answering different questions. Over the whole table the baseline moves 5.13%
between those two areas (Run 15), so a pair varying the area is read arm by arm,
its two `time` columns not subtractable.

**At a large nursery an earlier bench in the same process permanently slows
a later one --- and the condition is named SMALL-PINNED CHURN, its cost
the churn tax: churn of sub-3276-byte pinned allocations, the shared-accumulator
size class.** Run 14's probes found it (2026-08-15/16): `vgg-14-c512-k3/list`
read 14.1 ms with nothing before it and 22.3 ms after certain shapes, the same
ladder was flat at `-A4m`, and the victim's added cost was mutator LLC misses
at flat instructions and dTLB --- the counter signature that has held through
everything since. **It is not the pinned-spray pool condition of GHC
[#27601](https://gitlab.haskell.org/ghc/ghc/-/work_items/27601)**, by controls
and by a conceptual objection that stands: on one machine and one compiler
`+RTS -H2G` removes that reproducer's penalty and leaves this one whole,
`max_mem_in_use_bytes` moves 2.7% here against a doubling there,
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

**Swept over the whole main set of the time, and the answer is one positive
and one negative** (2026-08-17, `+RTS -A` at six areas from 4m to 128m, one
binary, no build). **Only eight shapes promote heavily at all**, and they
are exactly the eight with a finite span: `stretch-bigstride`
and `stretch-tall-Mx2` at 128 MB, `stretch-r5-8x432` and `stretch-inner256`
at 64, `vgg-14-c512-k3` at 16, and `stretch-pow2stride`, `alexnet-L2-27-c48-k5`
and `stretch-coprime-r7` at 8. The other sixteen never exceed a few kilobytes
per minor at any area, so they have nothing to win from any nursery and only
ever pay its mutator cost --- which is the whole of why the main set's gainers
are so few. **And the span predicts the gain**: the five that gained at 32 MB
are all drawn from the six with a span at or under 64, the gain scaling
as the area approaches it, while the two at 128 gain nothing there.

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

**There is no measured poison SET, and the scan that seemed to find one shows
why** (retracted 2026-08-17): **criterion runs benches in ROSTER order
and not in the order the `-m glob` patterns are given**, so a scan whose victim
sits mid-roster tests only the shapes ahead of it, every other process timing
the victim alone. The corrected experiment takes the victim from the END
of the roster, so that every candidate precedes it, which is the scan above.

**What the term is NOT is collector work, and the account that says
so was tested and failed.** The account tried was that a poison leaves
a retained heap the victim's collections then copy, and every part of it failed.
The ~22 MB live during the victim's phase is the victim's OWN live set, present
at the same 21.8 MB with nothing before it. The poison does not add major
collections but *removes* them, 97 in the poisoned process against 103 and 112
in unpoisoned ones. And majors copy 72.9 KB apiece here, the retained bytes
being large objects a copying collector does not move, so the extra copying
over the whole process is 6.9 MB. At the measured 0.42 ms per MB that predicts
3 ms where the observed cost is some 650 ms, off by two orders. Split directly,
GC time is 0.043 s alone against 0.059 s after and the whole difference
is **mutator** time, which is where Run 14 left it with its LLC-miss and IPC
readings. So the two nursery effects are independent as well as opposed: one
is copying, the other is what a resident footprint does to the mutator.

**The predictor, allocation in EXCESS of the result buffer, got `list` right
and the strategies wrong.** The excess, `(alloc - 1) x 8l`, is what churns
through the nursery, the result being one large object that bypasses it,
and on `vgg-14-c512-k3` it separates the arms where total allocation does not.
But Runs 14 and 15, at `-A1G` and `-A32m`, moved every one of the nine arms
it named as unmoved, from `build` at 0.9775 to `gen-quotrem` at 0.7760, while
`list`, predicted affected by up to 353 MB of excess, carried every ratio
with it. `list` crosses the nursery in every population, so no class table
divides by an unaffected baseline.

**The placement question is independent of the allocator**: `build` against
`mut-odo` read 1.1604 at the default area and 1.1433 at `-A32m` from one binary
(2026-08-09), the gap unmoved. Position matters on one shape and one family
by 35--40% where a geomean over a population shows nothing, so `list` runs
in the coldest slot and arms far down the roster are **flattered** rather
than penalised.

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
is identified. The pad probe, stepping `build`'s executed copy in eight-byte
steps until it lands whole, confirmed that the gap goes with it, below the loop
table.

**And a second family reads the same way, which is what takes it past one
point.** The four `mut-odo-vecdims` arms carry one copy each of that same
28-byte fill, the FastReshape three differing from their control nowhere inside
it ([the mutable ceiling](#the-mutable-ceiling-taken)), so their copies stand
beside `build`/`mut-odo`'s. **Every ratio is the row's arm against its family's
control** --- `mut-odo-vecdims` for the four arms under it, `mut-odo`
for `build` --- which is why the two control rows have no ratio of their own
and read `--` in all three: a control against itself is 1 by construction
and says nothing. The offsets are the executed copy's, read
with `tools/loop-offsets.py`:

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
dissenting. Run 10 splits that.** Its offsets come from `tools/loop-offsets.py`
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
carry its own names.** A plain build prints every `Main` copy under one mangled
symbol, these arms compiling to one worker. A `-g3` build carries what
is missing --- GHC emits a per-block symbol with DWARF line info ---
and `tools/loop-offsets.py` now reads it without help: `addr2line`
for the source line, the source file for the top-level binding that line falls
in, so a copy prints as `fbMutOdoVecdims` with the source line beside it instead
of as one worker's mangled name. A binary with no line info prints exactly what
it printed before. Read that way on 2026-08-13, at `-fspec-constr`
with `LOOP_MAXSKIP=1`, the four-copy vecdims group is, in address order,
`mut-odo-vecdims`, `-add-in`, `-add-out` and `-add-both`, and the pair beside
it is `mut-odo` then `build`. That is the order the loop table above assigns
its per-arm offsets in, so that table's ordering is a measurement, and emission
order tracking first reference from `roster` agrees. **Padding EVERY head
is refuted** (2026-08-14, an unconditional build and a max-skip build from one
source): the unconditional form puts every Main self-loop at offset 0 where
max-skip puts about half, **neither leaving a straddler**, so what padding every
head buys is padding nothing needed --- `build` alone gains, and the tail loses
up to 5.9%, the three largest losers carrying no tracked loop at all; its pads
sit inside enclosing loops and push some past the 64-byte window, a cost
the offsets alone do not show. And attributing heads to arms wants DWARF, which
changes the code, a plain build holding two copies of a loop per function where
the twin holds one --- so a plan resting on an instrument says what
the instrument is known to change. **And the instrument the residue wants
exists**: `loop-offsets.py --len 0` widens the grouped, named report
from the 28-byte run-fill to every loop a cache line can hold, which in Main's
own code is 112 loops over twenty lengths against the nine of one length
the tracked set saw --- so the arms that lose most under the unconditional form,
and carry no 28-byte loop at all, are visible to whatever asks next.

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

**The twin's fidelity is a per-GROUP property, not a per-binary one** (Run 13).
The same method names the vecdims four on both halves, every timed head matching
its own named counterpart at exactly 1.000 against a runner-up of 0.921 or less.
The other tracked group, `[11, 0, 4, 0]`, it cannot name at all: all four copies
share one byte-identical body, that body is the `fbMutOdo`/`fbBuild` worker
the two arms compile to, and **the `-g3` twin carries only two copies
of it where each timed binary carries four** --- counted over `.text` in all
four binaries. With no third or fourth name to give, the window match
degenerates to near-ties an order below the vecdims group's. So the standing
ruling that `-g3` is a different program bites group by group: count a body's
copies in twin and timed binary before trusting the twin's names, which
the vecdims group passes four against four and this one fails.

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
is the cheap first question about a gap this size. `tools/loop-offsets.py`
in horde-ad finds the copies structurally --- a backward branch whose target
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
as GHC [#27668](https://gitlab.haskell.org/ghc/ghc/-/work_items/27668), which
is where this belongs written up and which cites this benchmark for what
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

**What a line boundary costs is an op-cache entry, and a split instruction
is not a second thing** (2026-09-15, on this Zen 3, a Ryzen 7 5800X). Run 32's
HEAD half lands `fillStage2`'s stepping loop at offset 9, its exit `cmp; jge`
astride the line end, and pays about a cycle a run on every two-
and four-element run where the 9.12.4 half at offset 0 pays none,
the instructions, taken branches and mispredictions of the two binaries being
identical: op-cache fetches read one more a run, 5.4M against 4.5M an iteration
on `stretch-wide-2xM`, with 900k runs an iteration. Swept over all 64 offsets
in a standalone copy of that loop, `tools/probe-entries-sweep.py`, the run costs
4 cycles at offsets 0 to 8 and 22 to 31 and 5 or 6 everywhere else, and offset
9, where the branch is split, reads the same as offset 10, where it starts
the next line. A straight loop of 14 instructions swept the same way costs
nothing at any cut that leaves five or more ops on both sides of the boundary
and up to a cycle where a side holds a lone branch. The vendor documents name
the unit: an entry of up to 8 sequential instructions ending in the same 64-byte
region, terminated at the region's end, on Zen 2; 8 macro ops on Zen 3, where
the sentence about the region is gone from the guide and the fetch counter reads
a block more per crossing, as a boundary that ends an entry would give; 9 macro
ops from up to two adjacent lines on Zen 4. Intel before Golden Cove builds
lines of 6 uops per 32-byte window, and Skylake through Comet Lake under the JCC
microcode cannot cache a jump that crosses or ends on a 32-byte boundary at all,
so there the split branch is the worse case and not the same one. An entry
count, each piece of a straight segment charged one entry per 8 instructions,
reproduces the sweep at 54 of the 64 offsets on the probe's own run and 51
on the first, the misses being 18, 22, 32 to 35 and 60 to 63 on both and 19
to 21 on the first alone; the middle band is where a fourth L1 BTB override
a run appears, on 32 to 42, unexplained, and counting fused ops instead
of instructions fits worse, at 48 on the first run. Two things follow
for the shim. Its criterion, lines spanned by the head-to-back-edge span
and not straddling, is the right unit and the wrong span: a loop that turns
over once a run exits every run, and the exit is what the boundary cut.
And the criterion is this machine's; the table is what a run on another core
would have to re-derive.

| core | entry limit | window that ends an entry | ops a cycle | source |
|---|---|---|---|---|
| Zen 2 | 8 instructions | 64 bytes: up to 8 sequential instructions ending in the same 64-byte aligned region; an entry terminates at the region's end | 8 | [Zen 2 SOG 56305][zen2-sog] |
| Zen 3 | 8 macro ops; CMP, TEST, SUB, ADD, INC, DEC, OR, AND and XOR fuse with a following Jcc | 64 bytes, a block more per crossing on the fetch counter and the sweep here; the guide no longer says so | 8 | [Zen 3 SOG 56665][zen3-sog] |
| Zen 4 | 9 macro ops, fewer with many immediates or EVEX prefixes | an entry may hold instructions from two adjacent 64-byte lines | 9 | [Zen 4 SOG 57647][zen4-sog], [Chips and Cheese][zen4-cc] |
| Zen 5 | 6K entries; two taken branches a cycle | not in a document opened here | 6 per branch | [Agner Fog][agner], [Hot Chips 2024][zen5-hc] |
| Intel Sandy Bridge to Skylake | 6 uops a line, at most 3 lines a window; an unconditional jump ends a line | 32 bytes; one line a clock | 4 | [Agner Fog][agner] |
| Skylake to Comet Lake with the JCC microcode | as above | as above, and a jump crossing or ending on a 32-byte boundary is not cached at all | | [Intel, JCC mitigation][jcc] |
| Golden Cove and later | 4096 entries; 12-wide on Lion Cove | the window is 64 bytes | 8 | [Chips and Cheese][golden-cove] |

**What the Zen 3 guide's own front-end chapter says about the bands, read
on the evening of 2026-09-15, and what the counters rule out.** Section 2.8
of [the Zen 3 guide][zen3-sog]: the next-address logic produces one naturally
aligned 64-byte fetch block a cycle, and "branching to the end of a 64-byte
fetch block can result in loss of prediction bandwidth as it will result
in a shortened fetch block", which is the 60 to 63 band, a head in the line's
last bytes; a BTB entry holds two branches only "if the last bytes
of the branches reside in the same 64-byte aligned cache line and the first
branch is a conditional branch", and a third predicted branch after a cache-line
entry point "will require an additional BTB entry and additional cycles
of prediction latency", which is what the 32 to 42 band's fourth L1 BTB override
a run looks like and what the 9 to 13 band's `jl` ending in one line and `jge`
in the next would pay; fetch windows are tracked in a 64-entry FIFO from fetch
to retirement, one entry a line visited or more, and fetch stalls when it fills;
and the guide's own loop advice, section 2.8.3, is to align the END of a loop
to the last byte of a line and keep predicted branches per entry point at two,
the exit span's rule stated the other way round for a cycle that fits a line
and a rule for the cut where it does not. The processor programming reference
for the same core, 55898, defines the counters: 0x28F counts op-cache micro-tag
lookups, one a fetch block, 0xA9 cycles with the op queue empty, 0x1D0 retired
fused instructions, and 0xAA, the op-source split, sits under erratum 1287
and reads zero here. Read on the fill kernel at six offsets, per run: 26
instructions, 22 ops, four fused pairs and three taken branches at every offset;
op-cache misses, op-cache to decoder switches, op-queue-empty cycles and every
dispatch token stall at zero at the costly offsets as at the free ones.
So the lost cycle is in the front end and never shows as a starved dispatcher,
and the predictor's block sequencing under the two rules above is the account
to test, not the op cache's capacity.

**Nine sweeps in a quiet half hour, 2026-09-15 evening,
`tools/probe-fetch-model.py`, each table saved with its assembled layout
so the rules are re-scored offline.** The fill's per-run cycle at runs of 2, 4,
8 and 64, and a straight loop of 12 ops in 3-byte and in 6-byte instructions,
of 20 ops, of 12 with the branch unfused from its flag writer, and of 12
with an unconditional back edge. What they settle, offset by offset. A plain
crossing inside a segment costs nothing: the fill's body cut 9 and 5 at offsets
22 to 31 reads the free 4 cycles, and the 20-op straight loop fits the block
count at all 64 offsets. A taken conditional branch, or the fused pair
it belongs to, cut by the line boundary costs a cycle: the fill's `jge` at 9
to 12 and its entry `jl` at 14 to 17, the straight loop's `jnz` at 25 to 28;
a not-taken one cut the same way, the tail's `jle` at 43 to 46, costs nothing.
A block whose predicted branches end in two lines costs a cycle, the guide's
two-branch rule: offset 13, `jl` ending in the first line and `jge`
in the second with neither cut. A head whose block holds fewer than two whole
instructions costs a cycle, offsets 56 to 63, while a tail or re-entry segment
entered the same way, 54 and 55, 20 and 21, does not, which the rules as fitted
carry by charging the loop head alone. A block holding only an unconditional
`jmp` costs its block and, on the fill, nothing more that shows, 33 to 42, while
the straight loop with an unconditional back edge read half a cycle for it,
which the rules carry as a half. The op cache's entry limit binds only where
instructions carry 32-bit immediates: the 6-byte loop, twelve `and $imm32`,
reads 3.26 cycles at every offset that fits its 84 bytes in two lines, three
entries by the eight-immediates limit where the 3-byte loop needs two.
An unfused taken conditional costs about a third of a cycle an iteration in one
block and half a cycle when the cut leaves it with three or fewer instructions,
against the fused pair's whole cycle. And the runs of 4, 8 and 64
are memory-bound, 6.5, 11.3 and 100 cycles a run flat across most offsets,
the front-end penalties hidden except the two that survive anything: the cut
taken pair at 14 to 17 and the head in the line's last bytes at 60 to 63, each
still 15 to 17 percent on the 64-element run. So what a placement must avoid
on this core, in every regime seen: a taken conditional or its fused pair
astride a boundary, a head within eight bytes of a line's end, and a block whose
two predicted branches end in different lines; what it may ignore: a crossing
anywhere else. Written as rules in the probe and re-scored offline against
the tables, they fit the fill at run length 2 and the four 3-byte straight loops
at 319 of 320 residues, the one miss a row that jitters between 2.4 and 2.9
on a 2.5-cycle floor: one cycle a fetch block, a straddling first instruction
leaving an empty block that is fetched like any other; a whole cycle for the cut
taken pair and for the head in the line's last eight bytes; half cycles
for a cut leaving a last block of three or fewer instructions, a block holding
only a `jmp`, and a quarter for an unfused taken conditional; the penalties
added to the larger of ops over six and blocks, whole where the fetch bounds
the loop and halved where the dispatcher does. The tables are the files
the probe writes beside itself, named for the kernel swept, untracked.

**The two costs priced against each other, 2026-09-15, without a run,
and the third read the same evening** --- the pair registered in the open list,
answered here. `probe-fetches.sh` over both binaries, every population, no cell
refused: B crosses more windows than A almost everywhere, over half again
as many on 450 of the 1969 cells above 100k fetches an iteration, 5 to 50
percent more on 739, within 5 percent on 768 and 5 to 8 percent fewer on 12,
the fewer being `list` and the reducers; the fill loop that started this crosses
two windows more a run under B on all four short-run shapes, where A reads
the five a run Run 32's basis half did. Then `probe-interleave.sh` on thirteen
cells in a ten-minute quiet window, nine pairs each: the medians of B over A run
0.9938 to 1.0055, `flip-whole-square`'s lean fill the lowest
and `scaled-rank1-m1`'s the highest, the four short-run cells at 0.9976
to 1.0038, the shipped leaf on `cnn-L2-24x24-c32` at 1.0019 and the two cells
where B crosses fewer at 0.9965 and 0.9994, with per-cell ranges of one to three
percent and one of eight on `compose-scalar`. So the crossings the entry count
permits cost nothing this instrument can see on fills and references --- on one
reducer's per-run loop they cost 7 percent, the next paragraph, which confirms
the verdict rather than moving it --- and the pads the exit span adds cost
nothing either; A is the simpler rule and is the candidate for the next basis,
the entry count staying in the shim, off, with the sweep beside it. The cell
that contradicts it came on 2026-09-22, and the other way round:
`probe-r38-sweep.py`, the sweep over Run 38's fill loop on `stretch-wide-2xM`,
reads residue 0 at four op-cache fetches a run and 3.8 to 4.7 cycles in every
page line and process read, against three fetches at residues 2 to 13, two
of which, 3 and 4, read 6 to 9 cycles in most page lines and 5.5 to 7.1 across
eight processes of one binary --- so the fewest fetches are not the cheapest
residue, the count would move the head off the one placement every reading
holds, and the exit span's free band, 0 to 13, holds both bad residues too.
**Run 39 timed the settled cost, `LOOP_SETTLED=1`, on both halves, and that cell
came back**: `lib-stage2-lean` and `lib-stage3-lean` read 1.026 and 1.031
of the `-u1` loop on `stretch-wide-2xM` on the basis where Run 38 read 1.54
and 1.81, every tracked fill copy at offset 0, while the straddle count doubled
to 27 and 24 ([Run 39's Provenance](runs/run39.md)). **The same on HEAD,
the same afternoon**: the two costs built through `cabal.project.ghead` read
level on the same thirteen cells, medians 0.9917 to 1.0071 with per-cell ranges
of one to three percent and `compose-scalar`'s of thirteen, while the exit span
moves 527 of HEAD's 1860 heads on the tree of that afternoon, 1901 heads once
stage 11 landed, and the entry count 1378 more, and B crosses over half again
as many windows on 557 of 1970 large cells. And the fix itself, the exit-span
half against Run 32's own HEAD binary in the same window --- two trees,
that binary being the day before's, with the fill's head read by shape at 9
in it and 0 in the exit-span half, and the entry count's and block rules' halves
reading the same 0.93 against it: that binary reads slower by **1.0894**
on `stretch-wide-2xM`, 1.0785 on `stretch-tab7MB`, 1.0480 on `runs-2` and 1.0385
on `runs-4`, gross cycles an iteration on the lean fill, nine pairs each
and every pair above 1.02, with the shipped leaf on `cnn-L2-24x24-c32`
at 0.9981, its loop not having moved. That is the cycle a run of 2026-09-15's
reading bought back, seen on the compiler that lost it. **The third cost,
`LOOP_BLOCKRULES=1`, the nine sweeps' rules carried into the shim the same
evening, was built and read on both compilers before the day ended**: it places
1145 of 1874 heads on 9.12.4 and 1159 of 1901 on HEAD at residues the exit span
would not, leaves 57 and 67 short loops straddling by the lines criterion,
and in interleaved pairs reads level with the exit span on the lean fill
and on both window cells, 1.018 and 1.001 on HEAD's stage 9 and 1.016
on 9.12.4's --- so it loses nothing where the entry count lost, and it does
not move stage 9 on HEAD either. That settles which part of the shim the stage 9
cell indicts: not the cost, all three of which price the residue the planner
hands the inner head, but the tier that hands it there. The inner loop
of that rotated pair is the three-element `sumNoSpec`, cold per element,
and the outer walker is the hot cycle, so the residue should be the outer's;
the planner has no way to know a trip count, and a profile is what would tell
it. The end-alignment the guide recommends is a tie-break the block rules do
not yet carry, and it too would be spent on the inner head.

**The two stage arms' mechanism, their loop built to order, and HEAD's code
order on it.** Not the placement cause of the paragraph above, for the two arms;
that cause, for the two compilers. Both arms are `sumRoute` over `sumLazyRuns`,
whose `sumNoSpec` folds each run through one accumulator, so a run of L elements
is a chain of L dependent adds at the FADD latency, three cycles on this Zen 3,
and the chains of successive runs overlap only at their ends. Stage 10's
tie-break makes the run the longest unit-stride axis, 224, 128 and 64 elements
on the three views, and the arm runs latency-bound: 2.67 and 2.27 cycles
an element on `window-224x224-k3` and `window-128x128-k7`, rising with the run
length toward the three, at an IPC of 2.0 where it retires 2.34M instructions
an iteration against stage 9's 5.72M. Stage 9 keeps stage six's order, runs
of 3, 7 and 9, short chains that overlap across runs, and runs instruction-bound
at an IPC of 5.7. So the tie-break saves the per-run instructions and serialises
the adds, and on these views the adds cost more than the instructions saved.
A latency-bound loop is placement-blind, which the reproducer's paragraph above
says in its own words, and stage 10 reads the same on both compilers
and under all four placements, 0.3236 to 0.3278 ms on `window-128x128-k7`. Stage
9 is placement-sensitive for the same reason, and that is the compiler
difference: HEAD retires the same instructions and 22 to 39 percent more
op-cache fetches on its per-run cycle, and reads 1.082 and 1.145 slower
than 9.12.4 on the two views in interleaved pairs, under the exit span as much
as under the plain form --- a crossing neither cost covers, the cycle
a three-element run executes spanning more than a line, so that lines beyond
least and entries beyond least both admit one crossing and neither says where
it may fall. **And the same cell is where the entry count loses on 9.12.4**: B
crosses 19 percent more windows on `window-224x224-k3`'s stage 9 than
A and reads 1.074 slower in seven interleaved pairs, against 1.000
on `window-128x128-k7` and 0.991 on the latency-bound stage 10. The thirteen
cells the paragraph above was answered on held fills and references
and no reducer, and a reducer's per-run loop with a three-element body
is exactly the population where a stub piece costs. **Asked whether any
placement of these arms defeats the rules, the loop was built to order the same
evening** with the shim's new `LOOP_PIN`, `sumLazyRuns`'s inner head pinned
at residues 0, 30 and 58 on 9.12.4 --- the same loop serving stages 7, 9 and 10,
and stage 11 since it landed, which is why Run 32's `runs-3` read 1.24 on all
three it had. Its per-run cycle is 78 bytes and five taken branches: the outer
head's test, three not-taken bounds checks and a `jmp` into the rotated
three-element inner loop, the inner's `jl` taken three times, the accumulate
and the jump back. At 0 the `jmp` ends on byte 63 and the inner loop starts
the next line, five fetch blocks a run and 6.15 cycles, which is where every
9.12.4 binary had it; at 30 the one crossing falls in the straight part
of the checks and reads level, 0.94 to 1.04; at 58 the inner body is astride
the line on every iteration and reads 1.34 to 1.42 on `runs-3`
and `window-224x224-k3` for stage 9, 1.39 to 1.48 on `runs-3` for stages 7, 10
and 11, 1.29 to 1.36 on the stride-2 window for the three, and 1.08 to 1.10
on the long-run window for stages 10 and 11, where the arm is latency-bound
and the crossing per element still shows. The rules charge 58 and not 30,
as the machine does, so on this loop no placement defeats them, for any
of the four arms that run it. **HEAD's penalty on it is two blocks
of the compiler's own making and one of placement**: HEAD emits the outer head's
test as `cmpq; jl` into the checks, a taken branch every run where 9.12.4's
`jge` falls through, GHC
[#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799)'s shape
at a loop head, and lays the loop's exit block inside the cycle, 100 bytes
that cannot fit two lines without a crossing --- six taken branches and seven
fetch blocks a run against five and five, 8.1 cycles against 6.15. Pinned at 0
on HEAD it reads 7.40 cycles and seven blocks against the plain half's 8.10 ---
but that plain half is Run 32's, built from the tree of the day before,
and a comparison inside one tree, the block rules' half at 0 against the same
tree pinned at 30, reads 0.9999 on `runs-3`, 0.995 on stage 7's and 1.028
on the window view, level: on HEAD the residue of this head is worth nothing,
the 0.93 first read here was the two trees parting, and the whole of HEAD's
penalty is code order. **Where HEAD's planners actually put it, read off
the binaries by the loop's five-instruction shape rather than by a pattern's
first match, which can name another copy**: the plain form at 30, the exit span
at 3, the block rules at 0, every one free by the rules and the planner's trace
confirming the block rules chose 0 with a budget of 29 at the head's own dead
spot. So no cost failed to act on HEAD, and the free band hides nothing there
either: 0, 3 and 30 read level inside one tree, and the differences first read
between them were the trees parting. The same holds for stages 7, 10 and 11,
which run this loop.

**`943fecd`'s run loop and where it can sit, read 2026-09-25: on runs of three
it is stable only in bands with a sixteen-byte period, and every build of
it so far sits outside them.** `943fecd` made `runSlices`'s odometer a value,
which cut two taken branches a run from `sumLazyRuns`'s cycle on HEAD and packed
it into two lines: the inner three-element loop and fourteen instructions
of the rest of the run in the first, entered at three points, and six
in the second, 37 instructions and four taken branches a run. Its own build
and both Run 40 halves put the head at residue 7. Its 76 bytes, reassembled byte
for byte and run from a C driver with no GHC runtime --- a reproducer not kept
in the tree --- read at every residue of the binary's own line, six processes
each: stable at 6.1 cycles a run with no op-cache miss at residues 0, 11 to 16,
27 to 32 and 43 to 46; one of several modes per process, 6.7 to 10.9 cycles
and 0.06 to 0.7 misses a run, at 1 to 10, 17 to 26 and 33 to 42, residue 7 among
them; stable at 9.1 at 47 to 50 and at 8.1 from 51 up. The page line moves
nothing, residue 13 reading 6.1 on lines 0, 5, 30 and 62 and residue 7 slow
or mixed on each. At residue 7 only run length 3 trips it, lengths 1 to 16, 32
and 64 reading stable there; at residue 13 length 8 does instead, stable at 16
cycles against 11.2. And it wants the loop uninterrupted: re-entered every 30
to 222 runs, as a window view's odometer steps re-enter it, it holds the stable
mode, misses begin near 1,000 runs and reach half the uninterrupted loop's rate
by 10,000 --- which is why the four `window` views that walk runs of three never
trip it and `runs-3`, 600,000 runs with no level end, did. Placed in a stable
band the loop reads 6.1 cycles a run against Run 39's three-line loop's about
7.3, so the commit's gain is real and its placement gave it back on the one
cell. Why the settled cost rates residue 7 free for this loop, and what
in the op cache the sixteen-byte period is, are unread.

**Two exact readings did the attribution, both cheap and neither a probe
script's yet.** A hardware breakpoint counts one instruction's executions
and nothing else, `perf stat -e mem:ADDR:x:u` against a plain binary's address:
the inner loop's back edge over its fall-through is a cell's run length plus
one, which is how the twenty cells that walk runs of three were found among
the 269 that run the loop. And instruction counts, being placement-free, find
every arm that reaches changed code when read across two binaries of one recipe:
an arm whose count moves runs the change, one level to the instruction runs none
of it, where a walk of the source's callers by pattern missed five
of the thirteen and named three that do not.

**The physical frame of a code page is a placement term too, priced at 15
percent on a 27-byte loop (2026-09-16), and it is the one term here that neither
the shim nor the survey can see.** A byte-identical copy of Run 33's basis file
ran `runs-16384/lib-stage2-lean-u1` at 2800M cycles where the original ran
3260M, every extra cycle in the fill loop's own line at the same residue,
instructions and L1 misses equal, and evicting the original's cached pages,
`posix_fadvise(DONTNEED)`, re-drew its frame and brought it to 2785M: the frame
is drawn when a file is first read and held by the page cache for as long
as the file stays cached, at 4 KiB or 2 MiB as the page cache chooses. **What
a frame collides in is unread**: the heap's pages share the code frame's low
physical bits at the random rate; the front end, the caches, the TLB, resyncs
and prefetch read level, IBS (`probe-ibs.sh`) attributing nothing; and the whole
cycle gap on a slow instance is an integer-scheduler token stall,
`de_dis_dispatch_token_stalls1.int_sched_misc_token_stall`, with every
memory-side count level (2026-09-20, `probe-counters-0920.sh`
and `probe-counters2-0920.sh`). Its size scaled with the nursery, 5 percent
at `-A8m` and 15 at `-A32m`. **Two readings reach the term and nothing else here
does**: `--half-movers RUN PREV`, each half against the previous run's same half
over every population, since the A/A pairs share the binary and the counts share
the code; and the copy test, the half copied to a probe name and the cell timed
on both, a minute. `tools/probe-pageflags.py` reads the frames of a running
instance, its `--heap` form beside the heap's, and is what to run on the next
slow instance BEFORE anything evicts it, which a reboot, a copy over the file
or the eviction itself all do. **A tmpfs mount, `hugebin/`, makes the frame
a function of the layout** --- the text in 2 MiB compound pages, physical equal
to virtual modulo 2 MiB and the L2 sets the virtual ones --- **and
not the term**: a mounted copy is still a draw at 2 MiB granularity, Run 34's
mounted instance reading 1.075 of a second mounted copy of the same bytes.
The mount does not survive a reboot, so it is SUSPENDED since 2026-09-19
as an emergency measure, `half-bin.sh` answering with the on-disk file
and the run chapter's pre-run step 2 carrying the ruling; the instance gate
and the routes past it are [in the open list][open].

**A copy of a loop can carry a cost that follows it wherever it was moved, found
2026-09-24 on `stretch-wide-2xM` and not explained.** `fillStage2`'s nest runs
that view's stepping loop from a copy of its own, the odometer's instructions
under other registers, one of them a store's index in `%r14` that costs a REX
byte, so the loop is a byte longer and its run tail starts on the next line.
That copy reads 1.07 to 1.08 of `lib-stage2-lean-u1` in cycles where
the odometer's reads 1.00 to 1.01, at equal instructions, and the cost follows
the copy: exchanging the two fills' call sites, which moved both loops, carries
it to `lib-stage2-lean`; `LOOP_PIN` at residues 8, 16 and 32 leaves it at 1.08
to 1.09, 24 costing 1.35 to 1.37 as a band of its own; and a fresh copy
of the file, five nursery sizes and gdb's reading that both fills write one
output buffer at one address leave it where it was. Its counts part in the front
end alone, `ic_fetch_stall.ic_stall_any` 5.7M to 5.9M an iteration against 4.0M
to 4.6M with op-cache misses level at about five thousand and level too
the integer-scheduler token stall that carried the slow instance above.
The op-cache fetch count, one HIGHER a run at the costly offset
of the line-boundary paragraph above, reads one LOWER here, 4.5M against 5.4M,
and at residues 16 and 32 comes back to 5.4M with the cycles unmoved, so
on this loop the fetch count and the cost come apart. Swapping the two fills'
definitions in the source moves neither loop by a byte, so source order
is no lever on placement here. Two levers remove it, both read 2026-09-24
in pairs of variants and neither explained: passing the fused level's extent
and stride to the out-of-line runs function as arguments, where `fused` took
them from its closure, and inlining that loop into `run`, `fillStage2`'s form
since then, which reads 0.996 to 1.004 of `lib-stage2-lean` in cycles.
The readings are in `handoff-fill-prologue.md`.

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
(2026-08-10). `-pgma` replaces the program GHC assembles with,
so `tools/align-as.py`, in horde-ad, rewrites the `.s` on the way past: every
local label that a later instruction jumps backwards to --- which is what a loop
head is in the NCG's output --- gets a `.p2align 6`. On this suite that aligns
395 heads and puts **every copy of both fills at offset 0**, grows `.text`
by 0.13%, and leaves `micro check` green, 45 shapes agreeing and none
dissenting. So the straddle can be removed rather than merely frozen,
and with it the penalty --- which turns the whole finding into a two-bench
question ([the open list][open]).

**How far it gets is a thing to measure and not to infer**, the shim's own count
of 395 being labels in the assembly it was handed rather than loops
in the binary that came out. `loop-offsets.py --survey` counts the population
that matters --- self-loops no longer than a line, in this suite's own compiled
code, since only those can be rescued by an offset and everything longer spans
several lines in any build. It reads 115 such loops in `micro-unaligned`, **50
of them straddling and one at offset 0**, against 101 in `micro-aligned`
with **100 at offset 0 and none straddling at all**.

**A straddler count is not a count of straddling HOT loops.** Run 32's pair
carries eight apiece, and `probe-attr.sh` over their `-g3` twins puts samples
in the same two on each half: the `run` loops of `fbMutOdoVecdimsAddInLeafU2`
and `fillStage2`, which turn over once a run. They take 14 to 16% of a fill
arm's instructions on `cnn-L2-24x24-c32` against 0.9 to 1.1%
on `stretch-square-1341` --- a run-loop signature and not an element one ---
and the loop each jumps into is the unrolled-by-two element body, 42 bytes
at mod-64 offset 0 on three of the four and 8 on the fourth. The other six
are cold in every cell measured, save `-u2-ptr` on the HEAD half, which no HEAD
twin places and which is parked in any case. So the per-element work crosses
no line on either half, which is what the alignment is for and what a count
alone cannot say.

**The shim was blind under `-g`, which is why this wanted a fix and not merely
a build.** `tools/align-as.py` aligns a head only where the line before it
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
this README prices at a few percent and cannot predict --- a paired Run's
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
confirmed nor contradicted at this budget. The floor here is each binary's own
repeat, the machine not having been fully quiet, and the palindrome cancels
drift across the hour, all four pairings agreeing in sign and size; both halves
carried the shim's look-through, so what the pair varies is `-g3`. So the naming
above is read off a twin and carried to the timed binary by the correspondence
--- the arrangement the recommended path meant to remove, and does not.
**And the twin is short of copies as well as of registers, which is what bounds
the naming** (2026-08-14, four binaries --- the two timed halves, a fresh plain
build and a fresh `-g3` twin --- matched by body bytes rather
than by proximity). One body reads four copies in every plain binary and **two**
in the twin, and the twin's two carry distinct worker symbols that `addr2line`
puts in `fbMutOdo` and `fbBuild`; the vecdims body reads four in all four
binaries, which is exactly why that family names as a bijection and this group
cannot be named at all. A plain build therefore holds **two copies of that loop
per function** and `-g3` emits one --- a duplication the debug build suppresses,
the same class of divergence as the register allocation above, and the reason
an `addr2line` step can reach a function but never a copy.

**And a weaker level is no way round it, which is the move to expect
from a README that says `-g3` throughout.** `-g1` is the weakest GHC has ---
the users guide gives it as producing stack unwinding records for top-level
functions, which is data about a program rather than a part of one ---
and it changes the emitted code exactly as `-g3` does: one instruction fewer
and a different register assignment on an eight-line module, the same on GHC
9.10.3, 9.12.4, 9.14.1 and HEAD, with `-g2` between them behaving alike.
The reproducer and that table are horde-ad's
`docs/ghc-issue-debug-changes-codegen.md`, filed as GHC
[#27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687), which
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
to the instrument. **The same sweep INVENTS loops, and the third shape
of that is refused**: a body carrying a run of four zero bytes, which is an info
table read as code --- both the flow test and the `(bad)` filter admit one,
`00 00` being a legal instruction --- so survey totals recorded before
2026-09-11 can be higher by one or two wherever it fires. Read *none straddling*
as a statement about a sample that alignment makes smaller, not about
the binary, and take the completeness question to the assembly instead, where
the shim works and there is no decoding ambiguity: it knows which 395 heads
it aligned, and the heads it skipped are exactly those whose preceding line
was not an instruction. That is the form in which the claim below is sound,
and the survey is corroboration rather than the evidence.

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
the block-pool issue and in the same form, and filed from there as GHC
[#27667](https://gitlab.haskell.org/ghc/ghc/-/work_items/27667) --- that file
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

**A shim'd build does not hold its tracked loops at one address across a roster
change, so a figure read across one carries the layout term as well as drift.**
Under the max-skip form no tracked loop kept its address across a roster change
(Runs 20 and 21), so there the claim covers only additions that cost nothing
to place, and the layout term rides on every figure read across a roster change.
**Under the dead-spot form, RULED 2026-09-15: a tracked head's offset survives
a roster ADDITION and is not shown to survive a source rewrite beside it** ---
Runs 24 and 25 kept every mod-64 offset of the tracked heads, the heads moving
by whole constants as the form promises, while Run 32, six commits to `Main.hs`
beside its one new arm, moved a head of the six-copy group by 24. So the layout
term a figure read across a source change carries is not bounded by this claim,
and what would narrow it again is a build whose roster gains an arm
with no other source change. The offsets, addresses and constants themselves
are each run's own file's and its pair note's, read at the build against
the previous build of the same recipe by `loop-offsets.py --delta`;
this paragraph carries the ruling per form and not the numbers. **Every roster
addition that brings a new function is another reading of it** --- the fills
on one build either side, before anything else changes --- which costs nothing
at the moment the arms land and cannot be taken afterwards; the build step
of the run list is where it is asked for, and this paragraph is where
its verdict lands.

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
the twins nor that pair measure** --- the next paragraph has its figures,
and the paragraph *Every kind of comparison this README makes wants
an instrument*, below, lists it beside the other uncertainties this README
carries, only the smallest of which is on the table above. Susceptibility
is a property of the arm and has been measured for three of them, so
for the rest it is unknown; what that protects is orderings and tiers, which
several arms witness at once, and what it does not protect is any single arm's
figure read across a rebuild.

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
across the regimes over that run's 24 shapes, slower on 24 of 24, against
the full run's 1.218 --- but that used one binary for both regimes, so it rules
out everything except placement. `build` and `mut-odo` compile to the same
worker and moved in *opposite* directions under the flag, 17% faster and 19%
slower, which identical code cannot do. `bq-gen` regressed 12% with its build
loop specialised like every other and its build allocation-free. And the flag
moves 12 KiB of `.text` (20,349,125 bytes to 20,336,837), so every arm's address
and alignment shift whether its code changed or not.

**Answered, 2026-08-10: for a loop this size, placement costs 1.16 to 1.19**,
by the pad probe, eight binaries stepping each arm through all eight 8-byte
offsets with membership fixed (the figures, the graded penalty and the tables
are above). So the *how* is now measured and not merely read off a binary:
a straddled copy of the 28-byte fill costs 1.19, or 1.10 where only three bytes
precede the boundary, and that is what the pair's 0.86-to-1.24 span across runs
was made of.

What the probe does **not** reach is the rest of this entry. The 18% a rebuild
is worth stands as measured, since a rebuild moves more than one loop's offset;
`offtab`'s and `bq-gen`'s regressions have no shared-loop counterpart to be read
this way, which is the standing entry in [the open list][open] on crediting
a margin to a strategy; and susceptibility remains a property of the arm, now
with a mechanism for the two arms that share a loop and none for the others.

**A membership change alone moves layout**: on Run 9 it moved five fingerprint
arms from 0.910 to 1.192 in absolute time against a baseline that held to 0.998,
the roster being one of the things that sets the layout, which is why the answer
had to come from a probe that holds membership still.

**And the rebuild's 18% is a bias, not a floor, which is the distinction
to keep.** A floor is a threshold below which a margin might be noise,
and it shrinks as samples accumulate; this does not. Each binary's figure
is *correct for that binary* --- the four-binary rebuild probe's cells
are geomeans over that probe's 24 shapes with per-cell intervals of a fraction
of a percent --- so collecting more samples inside one build cannot reduce it,
and only averaging over several builds would. The per-shape picture says
the same: across rebuilds `list` scatters 2.2-2.5% per shape while its geomean
holds to 0.5%, where the two susceptible arms scatter 5-10% per shape *and* move
their geomeans. So do not read 18% as a new floor for this README's tables.
Every comparison inside the Results table is two rows of one binary
and is governed by the A/A twins as before; what the 18% governs
is the sentences that cross a build, which in this README means the cross-regime
absolute figures and nothing else.

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

**The floor is not *1/time***: per-cell *scatter* tracks an arm's speed,
but scatter cancels, and the bias that survives cancelling ranks by span.
**And a handful of A/A points is a modest estimate whichever run supplies
them**: one run can be the tightest and the wildest at once, pairs inside 0.07%
and one cell at 41% (Run 9), another uniform (Run 10), so expect either shape
rather than a constant, and quote the run's own number.

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

**Each population measures its own floor, and a single view inside one can
measure a much wider one.** `./view-floor.py RUN` prints each view's own A/A
spread beside its class's, per A/A group so that `list` does not speak
for a clause about a fill, and stars a view whose own floor exceeds its class's
by more than a factor; `--legs DIR` reports it as the distribution repeated legs
of one view show it to be, which on `flip-last-rows` ran from a half a percent
to eleven. The same eight controls ride every process, so a stride-class run
prices the noise of the process its own figures came out of --- which
is the only process they can be judged in --- but it prices it over three cells
where the main set has two dozen. Read a class's floor as that class's own
threshold and never carry the main set's figure into a class comparison
or the other way about: floors spread up to thirty-fourfold across
the populations of one run (Run 10). The `mut-odo-vecdims` slot carries
a class's worst pair more often than its share, which the amplification above
partly explains, `f` being largest for the fastest fill, so that arm converts
a given raw disagreement into a larger published one than any other pair
in the same process; read the recurrence as partly arithmetic and partly
unexplained.


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
of percent optimistic rather than merely noisy. A ramped cell can be a property
of an arm and shape, `bq-expand-zf` on `stretch-inner256` sitting under 0.99
three runs running, and alignment does not reduce curvature, which
is a different axis from the noise it leaves alone.

**A cell can be noisy for a property of the code, as `mut-odo`'s odometer list
traffic made a GC ramp where `l` is small** --- the cost `mut-odo-vecdims`
exists to remove, `build`, the identical fill from another slot,
and `mut-odo-vecdims` reading clean on the same shapes. **Positional
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

   **What the in-situ term departs from `sum-only` by is the arms' cost
   and not the read, and it is under a point on published geomeans** ([the open
   list][open]'s gate 3 entry, adjudicated 2026-09-05): its sign has stood
   on both sides of 1 across runs, the gate passing on its own test, which asks
   for *more than a few percent*, and the departure concentrating on the shapes
   whose result is L1-resident.

**And the correction is invertible, which is what keeps a pre-correction figure
comparable at all.** A raw slope is the published one plus the forcing term
times `l`, with `l` from `Main.hs`, so any uncorrected figure recovers to within
the term's own spread --- and the term has been within about 2% of every run's
since Run 7, through a flag, a roster, a layout, the shim's padding,
`-fproc-alignment=64`, an RTS line, a source patch that moves every loop offset
and a change of compiler. That is the control saying every run's correction
is one correction. Each run's own span is in its file, under Provenance.

**The three gates are a population's, not a run's.** Every process carries
the `sum-only` pair and the `-nosum` arms, so a [stride
class](#the-stride-classes-and-what-they-cover) measures its own term
and re-passes all three on its own cells; the main set's term licenses nothing
about a class's, in either direction. What a small population weakens is gate 2
alone: it reads the term's cost per element across the shape set, and a class
spans a fraction of the main set's range of `l` --- three shapes of nearly equal
`l` leave it almost nothing to see. Gates 1 and 3 are as strong there as here,
being about position and about the read.

**What remains open**: the `-nosum` pairs price two arms, the odometer
and the expansion, so a fill whose write pattern leaves the cache in some quite
different state could still be summed at a cost `sum-only` misses. A flat fill
and an endpoint dispatching between stores, copies and the stepping loop priced
it too on Runs 13 to 24, which is a record rather than a control every run
reprices; two arms an octave apart in speed agreeing to 1% makes the hole
unlikely rather than impossible.

**And a cell the term cannot correct is a shape the row loses, not a row lost
--- ruled 2026-08-26.** Where the forcing term is not smaller than the cell,
the arm removed the fill's work and what is left in the bench is the forcing
pass, so there is nothing per-element for a per-element term to be subtracted
from. The canonicalizing arms hit that by construction on the views they turn
into regime 1: one cell of `canon-full` on the main set and five over three arms
in `reshape1`, read at `-L1` before the run was paid for. `read-run.py` drops
such a cell from that row's geomean and from its `worst`, says on stderr which
rows lost how many, and `--selftest` names them instead of failing the file.
The cost is that two rows of one table can then cover different shape sets,
so a comparison between them is the reading's to make rather than the column's
to assert, which is what the printed count is for. A sunk **baseline** cell
is untouched by the ruling: it takes every row of its shape with it and still
fails the run.


## Provenance

**The half of a run's provenance that outlives the run.** A run's own --- what
its pair was, how the sequence ran, what moved and what did not, its anchors
and its correction --- is under [Provenance in the run's
file](runs/run45.md#provenance) and is replaced with the rest of it. What
is here is what a run does not replace: the delta chain below, which gains
a bullet per run and, with Runs 30 down to 8's bullets in their own files,
is the only record of which shape set and roster each measured, and the list
of what a run replaces OUTSIDE its own file, which is a recipe. Between them
they say what a run's figures have to be read against.

The desktop named at the head of the run's file is the same machine whose `idiv`
cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and should
name its machine at the head of its own file, where this one does.

**A FIGURE QUOTED AS AN EARLIER RUN'S NAMES THAT RUN IN THE SAME CLAUSE**, which
is what lets `--check-doc`'s agreement checks tell a history from a live claim:
they match a phrasing, not an intent, so `this run's main set` in a bullet about
one run reads to them as the next run's and fails; naming the run
is the convention, not a repair.

**The delta, so the population is recoverable.** What follows is the *only* form
in which a shape set or roster is recorded here: each run's difference
from the run before it. The newest bullet's run measured the shapes, class views
and roster `Main.hs` defines today, but for what that bullet declares added
or retired after the run, so a reader reaches today's state from the top
of the chain and walks down the deltas, from Run 30 down in each run's own file.
A snapshot would be a second copy of a list that already exists; a delta costs
what actually moved and shrinks to nothing when the two agree. A roster delta
has two halves now that membership no longer settles what ran: which arms
the roster held, and which of them it timed. **And a third: the ORDER they ran
in.** Order is not membership, it *can* move code layout, and Run 10 measured
layout at 12 to 14% on the two arms whose loop the shim rescues --- so a delta
stated in membership alone can read empty while the run is not repeatable.
Whether a given reorder moves anything is a thing to measure rather than assume,
both answers having turned up in one afternoon: `sum-only-early`'s slot-5-to-2
move left all eight loops this README tracks byte-identical, while lifting
it one further place, above `list`, shifts every worker by ~40 KB and rerolls
every alignment. So record the order, and read the binary before deciding what
the record costs. **A fourth half arrives with the pairing and is not a delta
at all**: which half of the pair a figure came from, which is why the run file's
tables and its fingerprint say so.

- Run 45 measured 31 timed arms over 19 main-set shapes and 62 class views
  in TEN classes, 589 benches and 1922, EIGHT A/A pairs, the `runs` class
  at SIXTEEN, `window` at EIGHT, `bcast`, `compose` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 44 is TWO ARMS IN AND TWO OUT, NOTHING GROWN**: two
  of the owner's commits carried `Main.hs` from `c100112` to `f5bf411`,
  `b5cd52e` retiring `libunord-stage7-sum` and `libunord-stage9-sum`, adding
  `lib-stage0`, master's `toVectorT`, timing `lib-stage2-disp` again rebuilt
  over `lib-stage2-lean` with `dispRun` re-cut to 32768, and counting
  `fillStage2Axes`'s level loop down, and `f5bf411` sorting `routeUnord13`'s
  axes by insertion, while the compiler, the shim, the project file,
  `micro.cabal` and the boot are Run 44's --- so what moved under the recipe
  is the source alone, the twenty-nine surviving arms keeping Run 44's order.
  **It is a REGIME pair and Runs 36's to 44's repeated a tenth time**, both
  halves one stage1 at plain `-O1` under the exit span and the settled cost
  and the control's command line carrying `-fspec-constr -fliberate-case`
  besides, so it is read against Run 44's basis `run44-gheadnospec`, whose
  recipe its own BASIS repeats to the character, and there the three arms whose
  instructions the commits moved all moved FASTER, `lib-stage2-lean` 3.11 points
  on 0.81% more instructions, and every other arm with a corrected time within
  0.86 points ([Run 45's file](runs/run45.md)). Its sequence ran in ONE window,
  02:42:06 to 09:58:35, 20 class processes and two main-set ones, in the order
  the run list gives, and foreign CPU met two A/A benches of the basis's main
  set, whose rerun the owner declined. `list` having moved 29.29 points
  on this run's main set, none of its eleven populations may have its two
  columns differenced. **And its floor is a maximum over EIGHT A/A pairs**, both
  halves' figures in [Run 45's own file](runs/run45.md). `bcastmid-block150k`
  was retired 2026-10-05, after the run, its lean-family fills drawing a slow
  or a fast state per process (`retiredShapes`). `block-run63-gap1`,
  `runs-4096-l2`, `big-vgg-28-c256-k3`, `big-vgg-112-c64-k3`,
  `big-resnet-stem-112-c3-k7`, `big-resnet-56-c128-k3`, `big-resnet-56-c256-k3`,
  `big-imagenet-224-c64-k3`, `big-runs-64`, `big-runs-1048576`
  and `big-runs-4194304` were added 2026-10-06, after the run.
- Run 44 measured 31 timed arms over 19 main-set shapes and 62 class views
  in TEN classes, 589 benches and 1922, EIGHT A/A pairs, the `runs` class
  at SIXTEEN, `window` at EIGHT, `bcast`, `compose` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 43 is NONE IN, NONE OUT AND NOTHING GROWN**: three
  of the owner's commits carried `Main.hs` from `e29cdf2` to `c100112`, making
  `fillStage2Axes`, `fillStage3` and `fillStage3U1` read a broadcast run's
  element as `genericFillStrided` does (`fdcd7a8`) and giving `lib-stage2-lean`,
  `liblist-stage4-sum` and `libunord-stage13-sum` the conversion code
  of `pr-mikolaj-toVectorListT` (`b7d0ee1`), and the COMPILER at the recipe's
  path was patched under its unchanged version `10.1.20260918`, while the shim,
  the project file, `micro.cabal` and the boot are Run 43's --- so what moved
  under the recipe is the source and the compiler together. **It is a REGIME
  pair and Runs 36's to 43's repeated a ninth time**, both halves that one
  stage1 at plain `-O1` under the exit span and the settled cost
  and the control's command line carrying `-fspec-constr -fliberate-case`
  besides, so it is read against Run 43's basis `run43-gheadnospec`, whose
  recipe its own BASIS repeats to the character, and there two of the three arms
  the branch's code reached moved the WRONG way, `lib-stage2-lean` 2.81 points
  slower and the reducing consumer `liblist-stage4-sum` 1.28, and every other
  arm with a corrected time within 1.08 points ([Run 44's file](runs/run44.md)).
  Its sequence ran in ONE window, 02:49:51 to 10:06:18, 20 class processes
  and two main-set ones, in the order the run list gives, and no bench met
  foreign CPU. `list` having moved 30.40 points on Run 44's main set, none
  of its eleven populations may have its two columns differenced.
  **And its floor is a maximum over EIGHT A/A pairs**, both halves' figures
  in [Run 44's own file](runs/run44.md).
- Run 43 measured 31 timed arms over 19 main-set shapes and 62 class views
  in TEN classes, 589 benches and 1922, EIGHT A/A pairs, the `runs` class
  at SIXTEEN, `window` at EIGHT, `bcast`, `compose` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 42 is NONE IN, NONE OUT AND TWO CLASS VIEWS GROWN
  under their names**: `aa18c24` grew `compose-bcast-nest`
  and `compose-bcast-wide` from 4992 elements to `sizeCap`, 1800000, carrying
  `Main.hs` from `eb76398` to `e29cdf2` in six of the owner's commits, which
  besides moved bangs where the -O1 Core read better, returned `lib-stage1`'s
  lone slice without `VS.concat` and matched the `Axis` port's bangs and names
  to the library's, while `micro.cabal` took orthotope's warning flags;
  the shim, the project file, the COMPILER `10.1.20260918` and the boot are Run
  42's --- so what moved under the recipe is the source alone. **It is a REGIME
  pair and Runs 36's to 42's repeated an eighth time**, both halves that one
  stage1 at plain `-O1` under the exit span and the settled cost
  and the control's command line carrying `-fspec-constr -fliberate-case`
  besides, so it is read against Run 42's basis `run42-gheadnospec`, whose
  recipe its own BASIS repeats to the character, and every timed arm's
  instructions read level there and every arm's main-set clock within a point
  but the `bq-expand` family's, 1.1 to 1.6 points slower in the main set's
  second process where its first read it level ([Run 43's file](runs/run43.md)).
  Its sequence ran in ONE window, 02:19:04 to 09:35:18, 20 class processes
  and two main-set ones, in the order the run list gives; one bench
  of the basis's main-set process met foreign CPU, so both main-set processes
  were rerun in a SECOND window, 11:03:06 to 12:45:06, on a quiet box the owner
  granted. `list` having moved 29.50 points on Run 43's main set, none
  of its eleven populations may have its two columns differenced.
  **And its floor is a maximum over EIGHT A/A pairs**, both halves' figures
  in [Run 43's own file](runs/run43.md).
- Run 42 measured 31 timed arms over 19 main-set shapes and 62 class views
  in TEN classes, 589 benches and 1922, EIGHT A/A pairs, the `runs` class
  at SIXTEEN, `window` at EIGHT, `bcast`, `compose` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 41 is ONE IN, NONE OUT AND TWO CLASS VIEWS IN**:
  `eb76398` timed `libunord-stage15-sum`, stage fourteen's route
  with the zero-stride axis consed just outside the run, and `e1ab85c` added
  `compose-bcast-nest` and `compose-bcast-wide`, carrying `Main.hs`
  from `688e952` to `eb76398` in six of the owner's commits, which besides moved
  `lib-stage2-lean-u1` onto the `Axis` path, made both lean fills merge and nest
  in loops, deleted `fillStage2` so that `lib-stage1` fills through
  `fillStage3`, and moved the unordered stages onto the `Axis` path; the shim,
  the project file, the COMPILER `10.1.20260918` and the boot are Run 41's ---
  so what moved under the recipe is the source alone. **It is a REGIME pair
  and Runs 36's to 41's repeated a seventh time**, both halves that one stage1
  at plain `-O1` under the exit span and the settled cost and the control's
  command line carrying `-fspec-constr -fliberate-case` besides, so it is read
  against Run 41's basis `run41-gheadnospec`, whose recipe its own BASIS repeats
  to the character, and the `bq-expand` family, which no commit reached, reads
  4.1 points faster there, back where Run 40's build had it, while `lib-stage1`
  reads 1.1 points slower and the other twelve arms that carry a corrected time
  read within 0.7 of a point ([Run 42's file](runs/run42.md)). Its sequence ran
  in ONE window, 01:44:40 to 09:00:47, 20 class processes and two main-set ones,
  in the order the run list gives, and no bench was intruded on. `list` having
  moved 29.05 points on Run 42's main set, none of its eleven populations may
  have its two columns differenced. **And its floor is a maximum over EIGHT A/A
  pairs**, both halves' figures in [Run 42's own file](runs/run42.md).
- Run 41 measured 30 timed arms over 19 main-set shapes and 60 class views
  in TEN classes, 570 benches and 1800, EIGHT A/A pairs, the `runs` class
  at SIXTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block` and `small`
  at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 40 is NONE IN, ONE OUT AND ONE CLASS VIEW OUT**:
  `0cd790c` retired `lib-stage3-lean-onelevel` and `94aeee7` the view `runs-3`,
  both kept in `check`, carrying `Main.hs` from `bb6b12e` to `688e952`
  in fifteen of the owner's commits, which besides froze `lib-stage2-lean`'s
  fill as a copy of `fillStage2`'s nest, gave `lib-stage3-lean` an `Axis` path
  of its own and made the merge's accumulator a strict record; the shim moved
  from `fe6d133` to `1a359bd`, changing what the settled cost plans, while
  the project file, the COMPILER `10.1.20260918` and the boot are Run 40's ---
  so what moved under the recipe is the source and the shim. **It is a REGIME
  pair and Runs 36's to 40's repeated a sixth time**, both halves that one
  stage1 at plain `-O1` under the exit span and the settled cost
  and the control's command line carrying `-fspec-constr -fliberate-case`
  besides, so it is read against Run 40's basis `run40-gheadnospec`, whose
  recipe its own BASIS repeats to the character, and two rewritten fills read
  1.9 and 4.4 points faster there while the `bq-expand` family, which no commit
  reached, reads slower on level instructions ([Run 41's item
  (4)](runs/run41.md)), and the other eleven arms that carry a corrected time
  read within 1.1 points. Its sequence ran in ONE window, 02:10:07 to 09:01:49,
  20 class processes and two main-set ones, in the order the run list gives,
  and TWO benches were intruded on, both in the control half's main set,
  for which a sensitivity reading stands in place of a rerun. `list` having
  moved 29.26 points on Run 41's main set, none of its eleven populations may
  have its two columns differenced. **And its floor is a maximum over EIGHT A/A
  pairs**, both halves' figures in [Run 41's own file](runs/run41.md).
- Run 40 measured 31 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 589 benches and 1891, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 39 is NONE IN, NONE OUT AND NO CLASS VIEW
  MOVED**: `Main.hs` moved from `c870e1e` to `bb6b12e` in ten of the owner's
  commits, rewriting `fillStage2`, `fillStage2U1`, `fillStage2OneLevel`
  and `runSlices`'s odometer behind timed arms and moving no arm in or out,
  while the shim stands at `fe6d133` with Run 39's five switches, the project
  file is Run 39's and the COMPILER is `10.1.20260918`, all unmoved --- so what
  moved under the recipe is the source, with a reboot of the box besides.
  **It is a REGIME pair and Runs 36's to 39's repeated a fifth time**, both
  halves that one stage1 at plain `-O1` under the exit span and the settled cost
  and the control's command line carrying `-fspec-constr -fliberate-case`
  besides, so it is read against Run 39's basis `run39-gheadnospec`, whose
  recipe its own BASIS repeats to the character, and three of the rewritten
  fills read 1.1 to 7.0 points faster there while the other fourteen arms
  that carry a corrected time read within 0.65 of a point. Its sequence ran
  in ONE window, 01:29:30 to 08:40:06, 20 class processes and two main-set ones,
  in the order the run list gives, and no bench was intruded on. `list` having
  moved 29.83 points on Run 40's main set, none of its eleven populations may
  have its two columns differenced. **And its floor is a maximum over EIGHT A/A
  pairs**, both halves' figures in [Run 40's own file](runs/run40.md).
- Run 39 measured 31 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 589 benches and 1891, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 38 is ONE IN, FOUR OUT AND NO CLASS VIEW
  MOVED**: `fe430cf` timed `lib-stage3-lean-onelevel`, the lean route
  over a fill that skips its tables at one level, and `c870e1e` parked
  `mut-odo-vecdims-add-in-leaf-u1`, `liblist-stage2-sum`, `liblist-stage3-sum`
  and `libunord-stage12-sum`, carrying `Main.hs` from `bb6f0fc` to `c870e1e`
  in seven commits, while the shim moved from `f31bd1c` to `fe6d133` and gained
  `LOOP_SETTLED=1` on both halves, the project file is Run 38's unmoved
  and the COMPILER is that run's `10.1.20260918` unmoved --- so what moved
  under the recipe is the source and the shim cost. **It is a REGIME pair
  and Runs 36's to 38's repeated a fourth time**, under the settled cost: both
  halves are that one stage1 at plain `-O1` under the exit span
  and the control's command line carries `-fspec-constr -fliberate-case`
  besides, so it is read against Run 38's basis `run38-gheadnospec`, whose
  recipe its own BASIS repeats less the switch, and the four fills read 3.4
  to 7.5 points faster there while the other twelve arms that carry a corrected
  time and ran in both read within 0.8 of a point. Its sequence ran in ONE
  window, 03:10:30 to 10:21:18, 20 class processes and two main-set ones, AFTER
  its riders rather than before them, the driver's sequence stage having refused
  over a stray file named for the run; and THREE benches were intruded on, all
  the control half's, none rerun at the owner's word. `list` having moved 29.66
  points on Run 39's main set, none of its eleven populations may have its two
  columns differenced. **And its floor is a maximum over EIGHT A/A pairs**, both
  halves' figures in [Run 39's own file](runs/run39.md).
- Run 38 measured 34 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 646 benches and 2074, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 37 is THREE IN, ONE OUT AND NO CLASS VIEW
  MOVED**: the pairing of 2026-09-21 timed `lib-stage3-lean`,
  `liblist-stage5-sum` and `libunord-stage14-sum`, each its counterpart's route
  under the fill numbered innermost first, and parked `liblist-stage4-list-sum`
  as `Only`, carrying `Main.hs` from `05cfe93` to `bb6f0fc` in fourteen commits,
  while the shim stands at `f31bd1c` unmoved, the project file is Run 37's
  unmoved and the COMPILER is that run's `10.1.20260918` unmoved --- so what
  moved under the recipe is the source and the boot and nothing else. **It
  is a REGIME pair and Runs 36's and 37's repeated a third time**: both halves
  are that one stage1 at plain `-O1` under the exit span and the control's
  command line carries `-fspec-constr -fliberate-case` besides, so it is read
  against Run 37's basis `run37-gheadnospec`, whose recipe its own BASIS
  repeats, and every one of the sixteen arms that carry a corrected time and ran
  in both reads within 2.09 points of it, at a `--bridge` geomean of 0.9993
  over the fifteen of them left once `list` is divided out. Its sequence ran
  in ONE window, 02:14:55 to 10:07:04, 20 class processes and two main-set ones,
  and TWO benches were intruded on, both the control half's --- one of the main
  set's 646 and one of the gate's 95 --- for which a sensitivity reading stands
  in place of a rerun. `list` having moved 28.89 points on Run 38's main set,
  none of its eleven populations may have its two columns differenced.
  **And its floor is a maximum over EIGHT A/A pairs**, both halves' figures
  in [Run 38's own file](runs/run38.md).
- Run 37 measured 32 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 608 benches and 1952, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 36 is NONE IN, THREE OUT AND NO CLASS VIEW
  MOVED**: `libunord-stage10-list-sum`, `libunord-stage10-sum`
  and `libunord-stage11-sum` went to `Only` in the owner's commit `2973582`,
  carrying `Main.hs` from `0eda736` to `05cfe93`, while the shim stands
  at `f31bd1c` unmoved and the COMPILER is Run 36's `10.1.20260918` unmoved ---
  so what moved under the recipe is the source, the project file, rewritten
  to the minimum that compiles on a current index, and the launch, off
  the suspended `hugebin/` mount and onto disk. **It is a REGIME pair and Run
  36's repeated**: both halves are that one stage1 at plain `-O1` under the exit
  span and the control's command line carries `-fspec-constr -fliberate-case`
  besides, so it is read against Run 36's basis `run36-gheadnospec`, whose
  recipe its own BASIS repeats, and every one of the sixteen shared timed arms
  reads within 1.90 points of it. Its sequence ran in ONE window, 02:44:57
  to 10:09:25, 20 class processes and two main-set ones, and NO process
  of the run was intruded on, the gate's four and the riders' included. `list`
  having moved 29.60 points on Run 37's main set, none of its eleven populations
  may have its two columns differenced. **And its floor is a maximum over EIGHT
  A/A pairs**, both halves' figures in [Run 37's own file](runs/run37.md).
- Run 36 measured 35 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 665 benches and 2135, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 35 is NONE IN, NONE OUT AND NO CLASS VIEW
  MOVED**: `Main.hs` stands at `0eda736` and the shim at `f31bd1c`, both unmoved
  since Run 35's build, and both halves launched from the `hugebin/` mount
  as Run 35's did --- so the roster is Run 35's entire and what moved
  under the recipe is the COMPILER, to an in-tree stage1 of `10.1.20260918`
  where Run 35's HEAD half was `10.1.20260803`, with the whole dependency stack
  rebuilt behind it. **It is a REGIME pair and not a compiler one**: both halves
  are that one stage1 at plain `-O1` under the exit span and the control's
  command line carries `-fspec-constr -fliberate-case` besides, so it is read
  against Run 35's HEAD half `run35-gheadexit`, whose recipe its BASIS repeats,
  and every one of the sixteen shared timed arms reads within 1.02 points of it.
  Its sequence ran in ONE window, 02:06:14 to 10:11:57, 20 class processes
  and two main-set ones, and NO process of the run was intruded on, the gate's
  four and the riders' included. `list` having moved 33.60 points on Run 36's
  main set, none of its eleven populations may have its two columns differenced.
  **And its floor is a maximum over EIGHT A/A pairs**, both halves' figures
  in [Run 36's own file](runs/run36.md).
- Run 35 measured 35 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 665 benches and 2135, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 34 is ONE ARM IN, NONE OUT AND NO CLASS VIEW
  MOVED**: `Main.hs` moved from `2496c98` to `0eda736` in three commits
  of 2026-09-17 --- `90740d6` and `ff45149` touching comments alone,
  and `0eda736` landing `libunord-stage13-sum`, stage twelve's route found
  with fewer passes over the axes, with its untimed sibling, and lifting
  the merge step `mergeInto` and the route tail `routeOf` to top level --- while
  the shim stood at `f31bd1c` and both halves launched from the `hugebin/`
  mount, as Run 34's did. It is read against RUN 34, whose recipe it repeats
  to the commit, so the one term between its published basis and Run 34's
  is the source. Its sequence ran in THREE windows, 01:54:33 to 03:49:22,
  03:55:00 to 10:05:35 and 11:24:11 to 11:48:34 --- a harness kill between
  the first two and a rerun of `bcastmid` on both halves in the third, after
  `--wild` named an intrusion inside the first `bcastmid` process, which
  the journal attributes to a root cron session. No process of the SEQUENCE
  was intruded on; one gate process was, by this session's own status call.
  **And its floor is a maximum over EIGHT A/A pairs**, both halves' figures
  in [Run 35's own file](runs/run35.md).
- Run 34 measured 34 timed arms over 19 main-set shapes and 61 class views
  in TEN classes, 646 benches and 2074, EIGHT A/A pairs, the `runs` class
  at SEVENTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block`
  and `small` at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled`
  at THREE. **Its delta against RUN 33 is ONE ARM IN, NONE OUT AND THREE CLASS
  VIEWS IN**: `Main.hs` moved from `f31bd1c` to `2496c98` in three commits
  of 2026-09-16 --- `971ffb6` landing `runs-32`, `runs-48` and `runs-64`,
  `0d637b7` landing `libunord-stage12-sum`, stage eleven with the run chosen
  among tied unit-stride axes by its length, with its untimed sibling,
  and `2496c98` firing stage eleven's guard on a zero stride of extent above 1
  alone --- while the shim stood at `f31bd1c`, and every process launched
  from the `hugebin/` mount, which no earlier run's did. It is read against RUN
  32 and not Run 33, by the owner's ruling of 2026-09-16; against Run 32
  its delta is two arms in and the same three views, with the exit span,
  the shim and the launch besides. Its sequence ran in ONE window, 02:20:29
  to 10:12:17, and no process of the run, the gate's and the riders' included,
  was intruded on. **And its floor is a maximum over EIGHT A/A pairs**, both
  halves' figures in [Run 34's own file](runs/run34.md).
- Run 33 measured 33 timed arms over 19 main-set shapes and 58 class views
  in TEN classes, 627 benches and 1914, EIGHT A/A pairs, the `runs` class
  at FOURTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block` and `small`
  at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled` at THREE.
  Its timings were ruled skewed by filesystem issues on 2026-09-16,
  the file-page frame term. **Its delta against RUN 32 is ONE ARM IN AND NONE
  OUT**: `Main.hs` moved from `f95795a` to `f31bd1c` in two commits ---
  `f46867f` landing `libunord-stage11-sum`, stage ten with its zero-stride move
  guarded, with its untimed sibling beside it, and `f31bd1c` changing one
  comment line and no code --- and the SHIM moved too, from `b3a1aca`
  to `f31bd1c` in NINE commits, `3b49356` adding the `LOOP_EXITSPAN` cost
  this pair is the first to build under and `f1a5adb` fixing it. Its sequence
  ran in ONE window, 01:05:22 to 08:26:08, and ONE of its twenty-two processes
  was intruded on by the write-up session, `run33-gheadexit-main`, for 3
  of its 627 benches at a peak of 0.35 of a core; the rerun post-run step 3
  orders was launched and stopped at the owner's word, and the run's own file
  carries the sensitivity reading that stands in for it. Its four gate processes
  and all 88 alone-leg logs are clean. **And its floor is a maximum over EIGHT
  A/A pairs**, 0.47% and 0.62%, `bq-expand-aa-distant` carrying it on BOTH
  halves; its restricted four-pair reading is the same two figures, so the two
  thresholds are closed on both halves for a second run.
- Run 32 measured 32 timed arms over 19 main-set shapes and 58 class views
  in TEN classes, 608 benches and 1856, EIGHT A/A pairs, the `runs` class
  at FOURTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block` and `small`
  at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 31 is ONE ARM IN AND NONE OUT**: `Main.hs` moved
  from `13cbd0d` to `f95795a` in six commits --- `c2021a8` adding comments
  and no code, `396f01c` carrying Run 31's own step-6d fixes, `4488631` landing
  `liblist-stage4-list-sum`, base's `sum` over stage four's list, and making
  the shared loop `sumLazyRuns` sum each run through `sumNoSpec` without
  vector's `SPEC` argument, a code change under unmoved names that reaches every
  lazy consumer wherever a view routes to runs, and `08ee255`, `e12b000`
  and `f95795a` taking an unzip immediately undone by a zip out
  of the zero-stride orders and threading the canonicalization on pairs. The 19
  main-set shapes and all 58 class views are unmoved, so a cross-run figure
  against Run 31 is over all nineteen shapes and over the 16 arms both rosters
  time --- and it carries a SOURCE term that nothing inside this run separates
  from the box's. **No md5 reproduces anything here**, the source having moved:
  `run32-nospec` is `0fa8e3e39a1ec5d0bc080dd853473916` with `.text` 20766917
  and `run32-ghead` is `9e8074782182dd8128a01309041204a7` with 20920127,
  the HEAD half larger by 153210 bytes, which is no multiple of 4096 ---
  and `--delta` against `run31-nospec` reads the two-copy group's mod-64 offsets
  preserved and THE SIX-COPY GROUP'S NOT, its second head moving by 24, which
  REOPENS the pinning claim's strong form and is recorded at that claim's own
  paragraph. **And the box did NOT move**: the gate's machine check reads
  `list`'s net at +0.86% against the fingerprint Run 31 installed, 0 of 19
  shapes past 5%, and against `run31-nospec` --- this recipe's own previous
  build --- the sixteen shared timed arms span 0.9839 to 1.0149 with `list`
  at 1.0031. What a reader has to carry is which half a figure came from:
  everything published in its file is `run32-nospec`, ghc-9.12.4 at PLAIN -O1,
  and `run32-ghead` --- the same source, shim, shim environment, roster, shape
  set and bench order built by the GHC checkout's in-tree stage1,
  `10.1.20260803`, instead --- contributes the second column of `runs/run32.md`.
  **Its `list` moved 0.43 points between the halves, INSIDE the 0.7% bar,
  so its two columns MAY be subtracted**, as may six of its ten classes';
  the four past the bar are `scaled`, `rev`, `small` and `compose`, at 1.19
  to 2.27 points. Its sequence ran in ONE window, 00:35:17 to 07:42:54,
  with NO intrusion in any of its twenty-two processes or its eighty-eight
  alone-leg logs --- one of its four GATE processes was intruded on
  by the write-up session, and no figure it publishes comes from a gate.
  **And its floor is a maximum over EIGHT A/A pairs**, 0.66% and 0.68%,
  `bq-expand-aa-distant` carrying the basis figure for a third run
  and `mut-odo-vecdims-aa-distant` the control's; its restricted four-pair
  reading is the same two figures, so the two thresholds are closed on both
  halves for the first time.
- Run 31 measured 31 timed arms over 19 main-set shapes and 58 class views
  in TEN classes, 589 benches and 1798, EIGHT A/A pairs, the `runs` class
  at FOURTEEN, `window` at EIGHT, `bcast` and `flip` at SIX, `block` and `small`
  at FIVE, `bcastmid` and `compose` at FOUR and `rev` and `scaled` at THREE.
  **Its delta against RUN 30 is SIX ARMS OUT AND ONE IN**: `Main.hs` moved
  from `7685375` to `13cbd0d` in three commits on 2026-09-13 --- `c753fff`
  parking `libunord-stage2-sum`, `-stage3-sum`, `-stage5-sum`,
  `libunord-stage6-list-sum` and the two pointer leaves
  `mut-odo-vecdims-add-in-leaf-u1-ptr` and `-u2-ptr`, reasons at their entries;
  `a22677b` banging the stage-ten walker's vector and the offset its empty carry
  ignores, a code change under unmoved names that reaches the `Route` stages'
  lists and consumers wherever a view routes to runs; and `13cbd0d` landing
  `libunord-stage10-list-sum`, base's `sum` over stage ten's list. The 19
  main-set shapes and all 58 class views are unmoved, so a cross-run figure
  against Run 30 is over all nineteen shapes and over the 16 arms both rosters
  time --- and it carries a SOURCE term that nothing inside this run separates
  from the box's. **No md5 reproduces anything here**, the source having moved:
  `run31-nospec` is `bbce438866c7a20652b96a60f4e1748d` with `.text` 20775109
  and `run31-o2` is `0bb3b8cc28592fbe592195d71435d1ab` with 20787397, the -O2
  half larger by 12288 bytes, and `--delta` against `run30-nospec` reads every
  tracked fill's mod-64 offset preserved, no address surviving to the byte
  and one displacement per group, which is the pinning claim in the form
  this README states it. **And the box did NOT move**: the gate's machine check
  reads `list`'s net at -0.23% against the fingerprint Run 30 installed, 0 of 19
  shapes past 5%, and against `run30-nospec` --- this recipe's own previous
  build --- the sixteen shared timed arms span 0.9909 to 1.0179 with `list`
  at 0.9959. What a reader has to carry is which half a figure came from:
  everything published in its file is `run31-nospec`, ghc-9.12.4 at PLAIN -O1,
  and `run31-o2` --- the same source, shim, shim environment, compiler, store
  and plan built at `-O2` instead --- contributes the second column
  of `runs/run31.md`. **Its `list` moved 29.74 points between the halves,
  OUTSIDE the 0.7% bar, so its two columns may NOT be subtracted**, nor may any
  of its ten classes', which moved 23.72 to 38.35 points: every cross-half
  figure in its file is an ordering. Its sequence ran in ONE window, 01:20:50
  to 08:14:07, with NO intrusion found anywhere, in any of the 114 logs that run
  wrote. **And its floor is a maximum over EIGHT A/A pairs**, 0.61% and 1.58%,
  `bq-expand-aa-distant` carrying the basis figure for a second run
  and the shipped leaf's distant copy carrying the control's on two wild
  `cnn-slice-c32` cells; its restricted four-pair reading is 0.61% and 0.43%,
  equal to the whole-set figure on the basis for a second run running.

Runs 30 down to 8 are tabled by their counts, each row linking that run's own
file, whose last section, *Its delta against the run before*, holds the bullet
moved there on 2026-09-23; a `-` is a run whose bullet gave no counts.

| run | timed arms | main-set shapes | class views | classes | delta |
|---:|---:|---:|---:|---|---|
| 30 | 36 | 19 | 58 | ten | [Run 30's delta](runs/run30.md) |
| 29 | 36 | 19 | 58 | ten | [Run 29's delta](runs/run29.md) |
| 28 | 39 | 19 | 58 | ten | [Run 28's delta](runs/run28.md) |
| 27 | 35 | 19 | 52 | ten | [Run 27's delta](runs/run27.md) |
| 26 | 30 | 19 | 52 | ten | [Run 26's delta](runs/run26.md) |
| 25 | 24 | 18 | 49 | ten | [Run 25's delta](runs/run25.md) |
| 24 | 52 | 26 | 41 | nine | [Run 24's delta](runs/run24.md) |
| 23 | 55 | 24 | 37 | nine | [Run 23's delta](runs/run23.md) |
| 22 | 55 | 24 | 37 | nine | [Run 22's delta](runs/run22.md) |
| 21 | 49 | 24 | 33 | nine | [Run 21's delta](runs/run21.md) |
| 20 | 53 | 24 | 26 | eight | [Run 20's delta](runs/run20.md) |
| 19 | 47 | 24 | 24 | eight | [Run 19's delta](runs/run19.md) |
| 18 | = Run 17 | = Run 17 | = Run 17 | = Run 17 | [Run 18's delta](runs/run18.md) |
| 17 | = Run 16 | = Run 16 | = Run 16 | = Run 16 | [Run 17's delta](runs/run17.md) |
| 16 | = Run 15 | = Run 15 | = Run 15 | = Run 15 | [Run 16's delta](runs/run16.md) |
| 15 | = Run 14 | = Run 14 | = Run 14 | = Run 14 | [Run 15's delta](runs/run15.md) |
| 14 | 47 | 24 | 24 | eight | [Run 14's delta](runs/run14.md) |
| 13 | 35 | - | - | - | [Run 13's delta](runs/run13.md) |
| 12 | = Run 11 | = Run 11 | = Run 11 | = Run 11 | [Run 12's delta](runs/run12.md) |
| 11 | = Run 10 | = Run 10 | = Run 10 | = Run 10 | [Run 11's delta](runs/run11.md) |
| 10 | = Run 9 | = Run 9 | = Run 9 | = Run 9 | [Run 10's delta](runs/run10.md) |
| 9 | - | = Run 8 | = Run 8 | = Run 8 | [Run 9's delta](runs/run9.md) |
| 8 | - | - | - | - | [Run 8's delta](runs/run8.md) |

- Run 6, still quoted here for the estimator ruling under `time`,
  for the `alloc` column's shape-dependence and for the correction's
  amplification arithmetic under [the floor][floor], **timed all
  of its roster**, trimmed rather than winsorized, on the Storable scratch
  the conversion since replaced, and with no stride class in existence.

**What the next run replaces.** A run's numbers reach past the Results table,
so this is the list they are walked against, once, from the one basis
that publishes everything. It names *sections*, not figures, a list of figures
being a second copy of them that goes stale. What guarantees completeness
is mechanical instead. Every section below is reached by a link,
and the coverage check is: no section carrying a figure outside a table may
be absent from them. The run's own file is reached whole rather than section
by section, that being what a run replaces and why it is a file. Run that check,
and repeat the two sweeps it cannot replace --- `./read-run.py --sweep PREV`,
README's paragraphs quoting a figure only the superseded run's file carries
and those naming that run, the run file's own half being `--inherited`'s
and `--stale`'s --- before trusting the list. The second sweep is written
without its numeral on purpose: spelled out, it is a run number nothing in step
5 reaches, so it would go on naming a run two runs back. **And there is a THIRD
sweep, which is a reading and not a grep, owed every run beside those two**:
walk the replace-listed sections and ask of each figure-bearing paragraph *which
run measured this*. The run-name sweep is structurally blind to a paragraph
naming only runs OLDER than the superseded one, which is the normal state
of a document full of dated mechanism accounts, and *reads as current*
is the discriminating property --- so no cheap predicate has it, and the checker
built for it was refuted at 100 entries for the four that mattered. Walk
the rulings and the tables first: a ruling resting on a figure is where a stale
number costs a decision, a table is where nothing in the prose can go stale
visibly, and the walk of 2026-08-26 found all its sites in those two places
and none in the dated accounts. **And ask it of claims about the tree, not only
of figures**, which is a second blind spot beside that one: a paragraph saying
*nothing checks for it* goes stale the moment the check is written, moves
no numeral, and names the current run while doing it, so no question about
figure currency can reach it. So the sweep asks two questions of a paragraph
and not one: *which run measured this*, and *does the tree still work this way*.

**Inside a section, find the paragraphs rather than reading it.** The list names
sections and a section here runs to hundreds of lines, of which a run rewrites
three or four paragraphs. **Not every paragraph opens with a bolded lead**: well
over a third carry none, and a few dozen of those carry a figure.
So a `grep -n '^\*\*'` between a section's heading and the next, in either
document, gives a section's **claims** and not its contents, and a walk
that stops there misses figure-bearing prose --- the opening section's
continuous argument, and continuation paragraphs inside list entries. The ones
a run touches are those whose lead or body carries a figure, which is why
`--para` falls back to the body when no lead matches.
`./read-run.py --para 'lead'` then prints any one of them with the line
it starts at, which is what keeps a jump off the `grep -n`/`sed -n` pair
that the install above it has already invalidated. **AND WHERE YOU ALREADY HAVE
A LINE NUMBER, `--para-at FILE:LINE` CONVERTS IT**, printing the paragraph
that holds it and, above it, the `--para` handle to carry instead --- lengthened
until it names one lead and no other. What this chapter recommends is `--para`
and what a caller holds after grepping is a number, and the converter is where
the two meet. Convert the hit and discard the number; it outlives neither
a rewrap nor the next `--in-place` install. `--check-doc`'s two sweeps print
line numbers for the comparative and superlative candidates already, so between
the three the walk is a list of jumps rather than a read. This is deliberately
a recipe and not a stored list of paragraph names: a stored one would
be a second copy of the structure and would rot the first time a lead
was reworded, which is the failure this list was rewritten to escape.

- [the run's own file](runs/run45.md) ENTIRE, which is what makes it a file:
  its head of at most three paragraphs, the pair and its headline, what
  the registration was built to show with its tally, and anomalies; the Results
  table and the findings under it, with which half published what; its own
  two-column geomeans and the two-column per-shape fingerprint, which
  are the only record kept once the JSON is deleted; the properties, where a run
  reports which held rather than re-deriving them; each class's own table,
  controls, provenance, anchor and paragraph; and its own Provenance, carrying
  what the pair was, its regime, scale and source commit, how the sequence ran
  and was gated, the three main-set anchors with the class ones, the straddlers
  and the layout span a roster order change alone is worth, the decomposition,
  and the correction's span. The bullets that used to name those sections one
  by one are this one, and the coverage check below reads it as covering every
  heading in that file;
- [the standing rulings from past runs](#standing-rulings-from-past-runs), whose
  rulings a run does NOT replace: it holds no task and no run's block,
  and a ruling there changes when an argument does, which a run is not. What
  the walk owes it is currency, a run's own surprises going to the open list;
- [the noise-floor table][floor] and its prose, from `--aa`, and the run's row
  in `series/floor.tsv` --- including the raw-slope six it compares against,
  the position verdict the crossed controls now disagree about between runs,
  and the `build`/`mut-odo` pair read as a second control;
- [the opening section][opening]'s headline ratios and its regime paragraph;
- [Making a major benchmark Run](#making-a-major-benchmark-run), whose figures
  are worked examples inside its own steps, which a run does not requote, only
  reads to see that each still illustrates the step it sits in; the pinning
  claim's record is [the floor section][floor]'s and not the chapter's;
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
- [The mutable ceiling (taken)](#the-mutable-ceiling-taken), a *ruling resting
  on figures*, so a stale number re-opens a decision rather than merely
  misreporting one --- and a ruling's number moves for reasons its verdict does
  not. It now carries two regimes. Requote from the run; do not carry forward;
- [The fix in Data/Array/Internal.hs](#the-fix-in-dataarrayinternalhs), whose
  validation counts are the test suite's rather than a run's, but whose
  paragraph pricing the branch's stage two against stage one carries a run's
  figures, the latest reading of the two stages over the populations. Requote
  those from the run as the ceiling's are requoted; the validation counts move
  when the suite does and not when a run does;
- the shipping paragraph closing [the Lemire section][lemire], a ruling
  of the same kind and the one a run CANNOT requote: both arms it rests
  on are checked and not timed since the precondition ruling, so its figures
  are frozen at Runs 7 and 8 and what the walk owes them is currency,
  not a requote. What bears on the decision is a change of regime --- orthotope
  compiling under a third would have to say what that does to the verdict rather
  than to the figure;
- [Dead ideas][dead], whose figures are the measurements that killed each shape
  and which a run does NOT replace: they are dated where they stand and a run
  touches one only by refuting a shape of its own, in which case the ruling
  and its evidence land here together;
- [The C-gap](#the-c-gap-still-a-deeper-ceiling), whose figures are horde-ad's,
  not a run's: no run here replaces them, and they move when that repo
  re-measures --- so the walk checks their currency instead;
- [The scratch vector flavour](#the-scratch-vector-flavour), whose figures
  are a probe's too, and whose conversion is why no `bq-*` figure predating
  it is comparable with one after it;
- [One element type](#one-element-type-and-what-the-probe-found), whose figures
  are a probe's and which no run replaces either. What would call for re-probing
  is a run that moves the ordering at `Storable Double`, since the claim
  is that the other types follow it --- which Run 8 did, and the re-probe
  in its regime kept the ranking ([the open list](#what-is-open));
- [The two-stage plan and the rework
  proposal](#the-two-stage-plan-and-the-rework-proposal), whose figures
  are a scratch probe's and Run 20's, which no later run replaces, the rework's
  arms being untimed;
- [Other toolchains, probed and not run](#other-toolchains-probed-and-not-run),
  whose figures are a probe's on another compiler and another backend and which
  no run here replaces: what would call for re-probing is a move in either
  toolchain, so the walk checks their currency instead;
- [sum-only](#sum-only-and-the-correction-now-applied), where what a run decides
  is no longer *whether* to correct but whether the term still passes its three
  gates, any failure invalidating the column rather than informing it;
- [R2 is the ramp detector][ramp] and [the per-shape `stretch-*`
  table][pershape];
- [what the benchmark does](#what-the-benchmark-does), whose two roster rulings
  quote the run they were cut on --- the arms they drop and the allocation tier
  the threshold sits above --- and whose membership a later ruling can reopen;
- [the non-urgent TODO list](#non-urgent-todo-list), whose roster-order entry
  cites the position figures a run measures and whose decomposition entry cites
  the question a run leaves open --- the one part of the harness chapter a run
  touches at all;
- [Reading a run file](#reading-a-run-file), whose figures are the evidence
  its rulings were taken on and which a run does NOT replace --- among them
  the `alloc` column's shape-dependence, refuted and confirmed refuted at full
  budget, so that every multiple quoted anywhere is a property of a strategy
  *and* a shape set, and of the regime too, three of the column's levels having
  moved with the flag alone;
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
benchmark Run](#making-a-major-benchmark-run) --- which is also where the walk
of the list above is one of the steps.

[achieved]: #how-the-strictly-positive-picture-was-achieved
[agner]: https://www.agner.org/optimize/microarchitecture.pdf
[bench]: #what-the-benchmark-does
[ceiling]: #the-mutable-ceiling-taken
[cgap]: #the-c-gap-still-a-deeper-ceiling
[classes]: #the-stride-classes-and-what-they-cover
[correction]: #sum-only-and-the-correction-now-applied
[dead]: #dead-ideas
[fix]: #the-fix-in-dataarrayinternalhs
[floor]: #what-moves-a-figure-when-no-strategy-changed
[golden-cove]: https://chipsandcheese.com/p/popping-the-hood-on-golden-cove
[jcc]: https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/mitigation-strategies-jcc-microcode.html
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[open]: #what-is-open
[open-tasks]: #standing-rulings-from-past-runs
[opening]: #regime-3-micro-benchmark-the-regime-3-fix
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
[probe]: #one-element-type-and-what-the-probe-found
[procedure]: #making-a-major-benchmark-run
[prov]: #provenance
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[reader]: #the-reader-read-runpy
[results]: runs/run45.md#results
[scratch]: #the-scratch-vector-flavour
[settled]: #what-is-settled-and-where
[shapeset]: #the-shape-set
[todo]: #non-urgent-todo-list
[zen2-sog]: https://kib.kiev.ua/x86docs/AMD/Optimization/56305_3.00_Software%20Optimization%20Guide%20for%20AMD%20Family%2017h%20Models%2030h%20and%20Greater%20Processors.pdf
[zen3-sog]: https://www.lsferreira.net/public/knowledge-base/x86/upos/amd_zen3.pdf
[zen4-cc]: https://chipsandcheese.com/p/amds-zen-4-part-1-frontend-and-execution-engine
[zen4-sog]: https://www.numberworld.org/blogs/2024_8_7_zen5_avx512_teardown/57647_zen4_sog.pdf
[zen5-hc]: https://hc2024.hotchips.org/assets/program/conference/day2/24_HC2024.AMD.Cohen.Subramony.final.pdf
