# regime-3 micro-benchmark (the fix: bq-expand)

This branch (`speedup-strided-tovector`) changes `toVectorListT`'s regime-3
fallback in `Data/Array/Internal.hs` — the per-element path taken when
the innermost dimension is strided, so no contiguous run longer than one element
can be sliced out.

The previous attempt, benchmarked as `gen-quotrem` resulted in a **mixed
picture**: it had replaced the original `list` fallback

    [vFromListN l $ toListT sh a]                       -- build/foldr list

with a `vGenerate` over a per-element `quotRem` (one division *per dimension*),
which sped up the large, many-channel shapes but *slowed* the small, shallow,
high-rank shapes that dominate horde-ad's convolutions (up to ~2×).

The fix now in `Data/Array/Internal.hs` is **`bq-expand`**: precompute
the base-offset of each innermost run once — the outer-base grid is separable
(`o0 + sum idx_d * stride_d`), so it is built by iterated `concatMap` /
`enumFromStepN` expansion, no division and no thunk-list — then fill the result
with a single `vGenerate` doing **one** `quotRem` per element. It beats
the original `list` fallback on every benchmarked shape with no regression
and needs no extension to orthotope classes.

A direct mutable result buffer is faster still: `mut-odo` walks the outer
odometer and writes each innermost run, and `mut-odo-vecdims` — the same fill
with its dimension lists replaced by unboxed vectors — is on Run 13 (SpecConstr)
**2.11×** over `bq-expand`. Its family holds the top of the table, and which
member leads is a tie the sort settles: `mut-odo-vecdims-add-in` reads 0.9940
against it, at 15 wins of 24 and sign p 0.31, the two printing the same 0.049.
Both need a new `Vector`-class method, which was measured and deliberately
**not** taken, to keep orthotope's `Vector` API pure and minimal — a bar
an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-not-taken), amended). Plain `mut-odo` no longer
argues for it at all: it and the shipped arm are a tie, winning nine shapes
of 24 with sign p 0.31 and an interval covering 1 for the second run running,
where Run 7 (Harness), at -O1, had it 1.51× ahead.

Several strategies measured since are faster than what shipped and need no class
method. The fastest pure ones on Run 13 are **`bq-odo-gm-mulback`** (0.090)
and **`bq-scan-rem-gm-mulback`** (0.091) against `bq-expand`'s 0.103 — a margin
of **1.15** and **1.14** paired, where Run 12 read 1.13 and 1.14, Run 11 1.15
on each and both halves of Run 10's pair 1.13 to 1.14. So it is no longer
a margin sitting inside the 1.22 that placement alone is worth in an unaligned
build, to be read as a candidate rather than a verdict: alignment removed
that term, and a run repeating Run 10 exactly — same binary, same roster, same
order — reproduces the margin to a hundredth ([the yardstick
table](#what-run-15-compares-against)). They also carry **no size precondition
at all**, which is the point of them, a ruling since having stopped this suite
timing any arm that needs one ([what the benchmark
does](#what-the-benchmark-does)). Neither is what `Data/Array/Internal.hs` does
today. Of the trade-offs, allocation and a noise floor this run measures
at 2.19% across the eighteen control pairs of the half the table comes from,
and 4.02% across the eighteen of its control half, are in [Results](#results),
each arm's precondition is at its entry in `Main.hs`'s roster, and the division
sites are in [the Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites).

Every figure on this page is **net of the shared forcing pass** every strategy
is timed through, which Run 6 (-O1) is the first run licensed to subtract
([sum-only](#sum-only-and-the-correction-now-applied)). That makes none of them
comparable to a figure from an earlier run, or to one from a later run that does
not subtract it.

Every figure is also **one population's**. The measured ones above are the main
set's — the positive-stride views a merged transpose builds — while the regime-3
views the library's other operations produce (reversed, broadcast, sliced,
windowed, scaled) are the [stride
classes](#the-stride-classes-and-what-they-cover), each its own population, run
in its own process and tabled beside the main set rather than folded into it.

And **one regime's**, **one roster's** and now **one layout's** as well. Runs 8
through 11 all compiled the suite with `-fspec-constr`, where every run before
them took the plain -O1 a default `cabal build` of orthotope takes, and the flag
reorders the table rather than nudging it — it speeds `list` itself by 8%,
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
its loops sit — 12 to 14% on the two arms whose loop straddled a cache line,
and a percent or two the other way on everything else. **Run 11 then changed
nothing at all**, re-running Run 10's aligned binary, and moved every arm
but one by under 1.5% and `list`'s worst cell by 4.3% ([the floor
section][floor]) — which is what the three figures above have to be read
against, and is a quarter of the band that was available before the layout could
be held still. So a figure here belongs to a flag, to a membership, to an order
*and* to a layout, and the last is the one this page can now remove rather
than only price. **Whether orthotope should carry the flag library-wide
is not this page's question** and is deliberately not on its open list:
that decision is about compile time and code size across the library,
and the measurement that would settle it is horde-ad's `convVjpBench`
over a real build. The 27% is what this page contributes to it. **At module
scope it is settled, and was mis-stated here until 2026-08-14**: the file
the fix lands in sets `-fspec-constr` itself, so this function ships
under the flag whatever the library does globally, and `-fspec-constr`
is the regime every claim below is read in rather than a probe of one.


## Contents

History is not here. `MARGINALIA` beside this file is a write-only journal
and not something to read: it exists because the models working here keep
putting history inside instructions, and it is where that goes instead
of into this page. It is not a `CHANGELOG`, which would face users. What
this page keeps is the rule and, where an editor might plausibly undo it, one
clause saying what undoing it cost.

Thirty-odd sections, so the map is here rather than left to a grep.
It is anchors and not line numbers on purpose: `--check-doc` verifies that every
anchor in this file resolves, so this list cannot rot silently, where line
numbers would be wrong by the next edit and say nothing.

- [What is settled, and where](#what-is-settled-and-where)
- [What is open](#what-is-open)
  - [Recommended tasks after Run 14](#recommended-tasks-after-run-14)
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
  - [The mutable ceiling (not taken)](#the-mutable-ceiling-not-taken)
  - [The C-gap: still a deeper ceiling](#the-c-gap-still-a-deeper-ceiling)
  - [Dead ideas](#dead-ideas)
- [About the current harness](#about-the-current-harness)
  - [What the benchmark does](#what-the-benchmark-does)
  - [Running it](#running-it)
  - [Making a major benchmark run](#making-a-major-benchmark-run)
  - [The reader: read-run.py](#the-reader-read-runpy)
  - [What moves a figure when no strategy
    changed](#what-moves-a-figure-when-no-strategy-changed)
  - [R2 is the ramp detector, not the noise
    detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now
    applied](#sum-only-and-the-correction-now-applied)
- [About the last run (Run 14)](#about-the-last-run-run-14)
  - [Results](#results)
  - [What Run 15 compares against](#what-run-15-compares-against)
  - [The claims Run 15 should test](#the-claims-run-15-should-test)
  - [The stride classes, run by run](#the-stride-classes-run-by-run)
  - [Provenance](#provenance)


## What is settled, and where

**One line per thing this page has established, and the section that holds it.**
It exists because the file is long enough to re-derive itself:
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

- **The fix that shipped** and why the base-offsets table is built by expansion
  rather than by division: [the fix][fix], with the four findings behind
  it in [how the picture was achieved][achieved].
- **The mutable ceiling**, why a direct mutable fill was not taken,
  and the amendment that turned that bar into a weight: [the ceiling][ceiling].
- **The class-method signature is free** — `build` and `mut-odo` compile
  to the same worker, dumped in both regimes — so no `vBuild` is held back
  on a figure: [the ceiling][ceiling].
- **Code placement moves figures**, and by more than the A/A controls can see:
  the identical-code pair, the rebuild bias, the per-loop reading
  and the cache-line table are all [in the floor section][floor]. **Straddling
  a cache line is a cost and not a correlation** — the pad probe stepped two
  arms through every offset — **and the penalty is graded** by where the split
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
  issues from horde-ad's `docs/`, which is where a reader outside this page
  should go; what stays here is what they cost this benchmark.
- **Which arm owns a loop copy is a property of the binary**, absent
  from a plain build and carried by a `-g3` one, which `loop-offsets.py` now
  reads for itself — and **a `-g3` build is a twin to read and not a binary
  to time**, that having been gated and lost. The map of the vecdims group,
  the reading of Run 11's split it corrected, and what `-g3` costs in emitted
  code and in time are [on the open list][open].
- **The allocation area moves figures too** — the default nursery against
  an arm's allocation in excess of its result — with the predictor
  and the populations it reaches [in the floor section][floor].
- **The A/A controls are the noise floor**, not the printed CI, and what they do
  and do not bound is [in the floor section][floor]; R² is the ramp detector
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
- **The roster is cut by two rulings** — a size precondition disqualifies
  an arm, and so does allocating past a bar — and a majority of the roster
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
and not a reading.** `OPEN` wants a measurement that is available; `PARKED`
is open but its route is retired, and the entry says why; `ANSWERED` records
an outcome and is kept so the question is not re-proposed; `STANDING`
is a ruling or a convention with nothing to run. `grep '^- .OPEN.' README.md`
is the list of live questions, and the one that answers a session's first
question about this section. The status is a pointer and never the authority:
the entry's own text is.

**This is the only home for an open question.** They are collected here because
otherwise they sit one per section and get reconstructed every time — and worse,
get missed: the question of why the count-down FastReshape form pays was raised
inside [the mutable ceiling][ceiling]'s own write-up and never migrated,
so a session that mined this list and its queue walked past it — migrated
into the FastReshape-axes entry below on 2026-08-14, the example standing
because it is the reason for the rule. A question recorded anywhere else
is a bug to be moved here, not a note to be left where it was written.
The harness's own backlog is folded in below, for the same reason: two backlogs
a thousand lines apart is how one belongs to neither.

**Run 9's question closed as unanswerable by this design, and the ruling is what
this entry keeps: roster and layout move together, so no run that changes
the roster can separate them.** The membership change moved one arm 9% faster
and its own code-twin 19% slower, which identical code cannot do; the separation
had to come from the pad probe, which holds membership fixed and has since
priced layout alone at 1.16 to 1.19 on a shared loop ([the floor
section][floor]). One residue outlives the rest: the regime probe left `bq-gen`
11% slower in absolute time with its allocation collapsed to the table's — which
neither the `diag` nor the Core accounts for, and the placement question below
inherits.

**And it raised a larger one in the same breath, which was then answered
the same day.** *What warms the expansion family?* On `vgg-14-c512-k3`,
`bq-expand` and three arms beside it run 35–40% slower in a small process
than at their published roster slots, reproducibly, while the scan and mutable
families do not move at all — the largest effect this page has measured
that is not a strategy, and it lands on the **shipped** arm. A dozen probes
settled it: not GC time (5.8% of the cold process), but the **default 4 MB
nursery** against an arm allocating 13.2 MB per call beyond its result, warmed
by exactly one predecessor — `sum-only-early`, whose one-off `l`-sized setup
allocation grows the block pool and leaves it grown. A nine-point `-A` sweep
shows a larger nursery rescuing the *cold* arm, and shows `-A1G`'s cliff to
be a collision with the `-M2G` cap rather than the nursery. The account is [in
the floor section][floor], and it carried **a roster fix, since applied twice**:
`sum-only-early` moved first from slot 5 to slot 2, ahead of the three distant
A/A twins, which were being calibrated against a colder heap than everything
they calibrate — on that roster the 41% cell reads 0.24% — and then, for Run 10,
above `list` as well, which is the warm-up bench [the TODO list][todo] had
been asking for and leaves nothing measured on an ungrown pool.

  **It was answered the same day, and the decision it forced is kept
  with the account**: keep the default area, and carry the caveat that
  the headline ratios are partly a statement about it ([the floor
  section][floor], which also holds the predictor for which cells the
  setting reaches, and the nine populations it has been applied to).
  What stays open is the size of it — how much of a published geomean
  moves is a run and not a probe.

**Three of Run 8's were answered the same day**, each by the probe its own entry
specified — the rule about a discriminating measurement deserving one now rather
than a slot in the next run, observed again:

- `ANSWERED` **`bq-scan-packed-mulback` gets worse because SpecConstr gives
  its control, for free, exactly what the packing was hand-rolled to buy —
  and the packing keeps charging for it.** Dumped in both regimes from Run 8's
  commit (2026-08-08, `-dsuppress-all -dsuppress-uniques`), the two arms' table
  builds differ like this. At -O1 the control's loop carries its state
  as a boxed `Either` of a boxed pair of a boxed `Int`, allocating a `Right` per
  step — the 72-bytes-an-entry the law at `baseOffsetsScanPacked` records —
  while the packed arm unwraps one `I#` and is otherwise unboxed, which
  is the 21% lead it held there. Under `-fspec-constr` both loops specialise
  to four raw arguments and *neither* boxes: the control's `Either`, pair, `I#`
  and its per-step allocation all vanish, and the packed arm loses only its one
  `I#` unwrap. What survives on one side and not the other is the packing's own
  arithmetic — `uncheckedIShiftRA# … 32#` and `andI# … 4294967295#` on every
  element, against the control's two plain `+#` — so the flag pays off the debt
  the packing existed to avoid and leaves the packing's interest still due.
  Hence cheaper (1.33x on both) and slower (1.11× on 24 shapes of 24).

  Two consequences. The law at `baseOffsetsScanPacked` is confirmed
  in its constructive half and its corollary refuted: every state shape does
  unbox under the flag, but "indistinguishable from its control" does
  not follow, because unboxing removes the control's cost and not the packed
  arm's. The `diag` behind all of this was re-measured in Run 8's own regime
  and every figure quoted above reproduces, including the controls that say
  the instrument did not move; what it adds is that `baseOffsetsScanPacked` goes
  3.00x to 1.00x, so under the flag even the boxed `Int` in `unfoldrExactN`'s
  emit pair — which the -O1 reading called out of reach of any state shape —
  is gone. And the packed representation is now known to be a **-O1-only**
  optimisation: wherever SpecConstr runs it is strictly dominated by the plainer
  arm it was built to beat. That was written as a thing to settle before
  the flag question, and the flag question has since been answered against it —
  the shipped file sets `-fspec-constr`, so the packed form is not a candidate
  here at all.

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
  says so: their distinguishing operations — two `intToInt32#`,
  a `writeInt32Array#`, no boxing — are identical in the two regimes,
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
  is the question behind the trigger — whether the flag's reordering
  is an `Int`-arithmetic effect or an element-width one — since the ordering
  it moved is among the roster's arms and not among the types.

**What Run 10 leaves open**, each with what would settle it:

- `ANSWERED` **What does code placement cost?** **A rebuild is worth up to 18%
  on a susceptible arm and 0.5% on the baseline** — which is the size of every
  unexplained regression in Run 8, and the largest effect this page has measured
  that is not a strategy. Four binaries were built from sources differing only
  in inert pad arms, the run filtered so the pads never execute; against
  the first of them the other three read `list` 0.9949, 1.0019 and 1.0031,
  `mut-odo` 1.0389, 0.8808 and 1.0401, and `offtab` 0.8241, 0.9524 and 0.9126
  (2026-08-08, `-fspec-constr`, 24 shapes, per-shape geomeans of absolute net
  time). So susceptibility is a property of the arm: the baseline has almost
  none and two arms have a great deal, and they are the same two the flag sets
  back hardest.

  Around that sit the readings it explains. `offtab`'s own regression
  is **not** roster or noise: filtered into a five-bench process it reads 1.2236
  across the regimes over 24 shapes, slower on 24 of 24, against the full run's
  1.218 — but that used one binary for both regimes, so it rules out everything
  except placement. `build` and `mut-odo` compile to the same worker and moved
  in *opposite* directions under the flag, 17% faster and 19% slower, which
  identical code cannot do. `bq-gen` regressed 12% with its build loop
  specialised like every other and its build allocation-free. And the flag moves
  12 KiB of `.text` (20,349,125 bytes to 20,336,837), so every arm's address
  and alignment shift whether its code changed or not.

  **Answered, 2026-08-10: for a loop this size, placement costs 1.16 to 1.19.**
  The first attempt at this left the question narrower than it found it —
  it should have timed `build` across the four layouts and did not, a shell glob
  having eaten the arm ([the reader's section](#the-reader-read-runpy)) —
  and what settled it instead was the pad probe done properly, eight binaries
  stepping each arm through all eight 8-byte offsets with membership fixed ([the
  floor section][floor] carries the figures, the graded penalty and the tables).
  So the *how* is now measured and not merely read off a binary: a straddled
  copy of the 28-byte fill costs 1.19, or 1.10 where only three bytes precede
  the boundary, and that is what the pair's 0.86-to-1.24 span across runs
  was made of.

  What the probe does **not** reach is the rest of this entry. The 18% a rebuild
  is worth stands as measured, since a rebuild moves more than one loop's
  offset; `offtab`'s and `bq-gen`'s regressions have no shared-loop counterpart
  to be read this way, which is the entry below on crediting a margin
  to a strategy; and susceptibility remains a property of the arm, now
  with a mechanism for the two arms that share a loop and none for the others.

  **Run 9 had made this the page's central question rather than a caveat
  on it**, and that is the framing the answer inherits. A membership change
  alone moved five fingerprint arms from 0.910 to 1.192 in absolute time against
  a baseline that held to 0.998, and moved `build`/`mut-odo` — one worker, two
  slots — to 1.13 where Run 8 read 0.86 and Run 7 1.24. Every route through
  the roster was blocked, the roster being one of the things that sets
  the layout, which is why the answer had to come from a probe that holds
  membership still.
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
  own provenance line reports — about five seconds a bench-shape cell, criterion
  spending its budget whether the call is fast or slow — and nothing here
  measures what contention does to them. **The gate entry below has since
  been folded into Run 10 rather than queued behind it**, alignment having
  turned out to be the thing that decides whether the rest of the queue
  is measuring anything; what stays there is the cheap gate that runs before
  the run does. Entries are referred to by name and not by number, two having
  been removed from under a reference already. **Nothing below is outstanding**:
  each has been run or closed, and what the list holds now is what each bought
  and the ordering rule above, which is what a later queue would be built on.
  1. **The pad probe done properly — run 2026-08-10, and the hypothesis
     survives.** Eight binaries differing only in inert pad arms, two
     interleaved passes over all eight, 2h12m, with `build` and `mut-odo` both
     timed this time (the first attempt lost them to a shell glob) and each
     stepped through all eight 8-byte offsets — the step being all GHC aligns
     the loop to — with membership fixed throughout. A straddled copy costs
     1.19, or 1.10 where only three bytes precede the boundary, and the two
     discriminating binaries invert as predicted: [the floor section][floor]
     carries the verdict, the graded penalty and the controls. Placement
     and the allocator are separate effects, which is why this wanted a window
     of its own rather than being shrunk by 1: the `build`/`mut-odo` gap
     was measured across the nursery change and did not move.

     **Two pad designs relocate nothing, so they are not retried** — measured
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
     than the evidence** — the point of that ordering, two of Run 10's
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
     files were untracked in `pad-probe/`, ~280 MB, and are deleted: this page
     carries what they showed, and the effect has a self-contained public
     reproducer in the filed issue.
  2. **A third `-nosum` arm, on a flat fill** — the one probe that separates
     *the read is biased* from *those two arms are*. Landed
     as `mut-flat-gm-nosum` (2026-08-13) after waiting out two runs, membership
     having had to stay pinned through Run 11's repetition and unconfounded
     with Run 12's change of shim; its readings are with gate 3 and the roster
     entry. Two things from its scheduling outlive it. **The run's question goes
     in the second half**: Run 10 paired against an unaligned build and priced
     layout, Run 11 against max-skip and priced the padding, Run 12 against
     `-fproc-alignment=64` and priced the flag — the new variable rides
     the control half and the basis stays comparable. And **`micro-both`
     was the obvious candidate for Run 12's pair and the wrong one**: it carries
     the *unconditional* shim with the flag because it was built hours before
     the max-skip form existed — a composition that is chronology
     and not design, and a name that invites being read as design. Nor can such
     a pair separate the flag from the offsets it produces, pinning procedures
     being *how* it works; the resident offset's own price stays a probe
     on the pad-probe model.
  3. **The five-bench gate before Run 10's aligned half — run 2026-08-10
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
     of this entry — a main set aligned against one unaligned — is no longer
     a queue item at all: it *is* Run 10, whose fourth prediction
     is that comparison read arm by arm.
  And three things **not** worth a quiet window, recorded so they
  are not reached for. The *how many preceding benches warm it* sweep, which
  the nursery finding supersedes — the bench count is the symptom
  and the allocation area is the cause. The element-type re-probe, whose trigger
  is a run that moves the ordering at `Storable Double`, which Run 9 does only
  through layout and membership rather than anything an element type would feel.
  And **an A/B of the pre-swap binary against the post-swap one, to price
  the roster swap on its own** — proposed and refuted the same day: that swap
  moved heap warmth *and* relocated every worker by ~40 KB, so binary against
  binary conflates exactly the two things Run 10's unaligned half conflates,
  and buys a number Run 10 supplies anyway at the price of a quiet hour
  and a false sense that one variable had been pinned. **Half of that refutation
  has since expired and the other half has not.** In an aligned build a roster
  swap relocates no loop, so such a pairing would no longer conflate the two —
  but it would still buy a number Run 10's third prediction supplies
  for nothing, which was always the stronger of the two reasons. Recorded
  because the expiry of a premise is exactly what makes a dead idea look alive
  again.
- `ANSWERED` **Is the term still unbiased?** Gate 3 passes and still does
  not bracket 1: every in-situ median of both arms in all ten of Run 10's
  processes sits below it, **0.9641 to 0.9903**, for the **third** run running
  ([sum-only](#sum-only-and-the-correction-now-applied)) — and the two halves
  of the pair agree about it, so it is not a layout term either. Three runs
  on one side is no longer the coin-flip the failure test assumes, so the next
  measurement is not another gate reading: it is a third `-nosum` arm
  on a strategy whose write pattern differs from both — a flat fill rather
  than an odometer or an expansion — which is the one thing that would say
  whether the bias is the *read* or those two arms. Run 9's cells have since
  been read under those medians and narrow everything except
  that ([sum-only](#sum-only-and-the-correction-now-applied)): the shortfall
  is systematic per cell rather than differencing noise, the two arms order
  the shapes alike, it runs about a tenth of the term at the smallest shapes
  and vanishes at the largest, and re-pricing both arms by it moves no published
  geomean by a point. So the flat fill is the only thing left to ask,
  and the bias it would characterise is small enough that the column stands
  either way.

  **Asked and answered, 2026-08-13: it is the read.** `mut-flat-gm-nosum`
  was written into the roster and run filtered over the shape set on the Run 12
  basis build — four benches, 96 cells, 8m17s — and its in-situ term reads
  a median of **0.9701**, below 1 like the other two and inside
  the 0.9641–0.9903 band every process has landed in. A third arm whose write
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
  the two groups already read and the sentence stands as written — but it stands
  as a checked fact rather than an assumption, and it does **not** become
  a placement pair if that arm is ever timed: the two differ
  in the Granlund-Montgomery quotient, so a line span between them competes
  with real arithmetic and says nothing, which is exactly the disqualification
  this bullet already states. A shared loop is necessary for the reading
  and not sufficient. The same sweep confirms the other half of this bullet:
  **no group at any swept length holds `bq-gen`**, so its 11% having
  no same-loop counterpart is now checked too. Everywhere else the shared loop
  is a table build while the arms differ in the output loop that distinguishes
  them, so a line span there competes with real arithmetic and says nothing.
  Recorded so the sweep is not attempted a second time.
- `STANDING` **Look at the distribution before quoting the summary — per shape
  for a row, per sample for a cell.** Four questions settled on 2026-08-14 each
  came back the same way: an aggregate was carrying a mixture. `bq-expand-b`'s
  pooled 1% is two stable shapes and twenty-two scattering around 1;
  the `scaled` slot's slope is the average of two states a step apart;
  the alignment gain's 12% is a geomean over a distribution with no ordering
  in any dimension; and the four widest arms on the spread instrument span 2.4
  to 17.0 ns an element, so they are not a tier. The two readings cost nothing
  over kept artifacts — `--pair` already prints a row's range and its extreme
  shapes, and a cell's samples split into quartiles by iteration count in four
  lines of arithmetic, which is what found the step. A margin whose distribution
  has not been looked at is a summary of something unknown, and the instrument
  that would have caught each of these existed before the question was asked.
  **For the per-sample half it now exists as a mode**: `--steps` reads every
  cell for a change of level mid-bench and reports it against the scatter inside
  the two segments it splits. **Its threshold is the whole test** — some split
  is always the best one, so the naive reading flags a quarter of all cells
  and says nothing, where `t` above 40 with a step past 2% flags about 3%
  of them; quoting the first without the second would be the same error one
  level down.
- `ANSWERED` **Run 10's predictions, and how they came out.** The run is made;
  the verdicts are here, with the registrations they are read against left
  standing underneath so that what was predicted before the hours were spent
  stays legible. **Two held, one held only in direction, one split and one
  is refuted.**
  1. **Split, and the split is the finding.** `mut-odo-vecdims-add-in` collapsed
     as predicted — 0.9937 on the unaligned half, where all four copies are now
     line-resident, and **1.0009** on the aligned half, where the prediction
     was 1.00 outright — so its Run 9 reading of 1.1552 was layout and is gone.
     `add-out` and `add-both` did not: they read 1.1266 and 1.0906 unaligned
     and **1.1612** and **1.1184** *aligned*, with every copy of the loop
     at offset 0. The registration says a reading near 1.16 surviving alignment
     kills the hypothesis for the arm that carries it, and `add-out`'s does.
     So the straddle account holds for one of the three and is refuted
     for the other two, and [the suspension of those axis figures][ceiling]
     resolves the same way — withdrawn for `add-in`, converted into a measured
     cost for `add-out` and the corner.
  2. **Held in direction, missed its point value.** `build`/`mut-odo` reads
     0.9532 paired unaligned and **0.9685** aligned, against a registered 0.998
     and Run 9's 1.13. So the pair closed past 1.0 rather than onto it,
     and on the aligned half — where both copies sit at offset 0
     and the prediction is 1.00 by construction — identical code still differs
     3.2% by geomean while tying by the sign test (16 of 24, p 0.15). The gate
     had already read 0.961 to 1.008 aligned, so this is the gate reproduced
     at full budget rather than a new disagreement.
  3. **Refuted.** The anchors did not fall. `list`'s net per call, aligned,
     against Run 9: `cnn-slice-c32` −0.6% (the control, predicted to hold,
     and it did), `cifar-L2-16-c64-k3` −2.5%, `stretch-wide-2xM` +0.2%,
     and across the eight class anchors −1.1% (`rev-primes`) to **+7.9%**
     (`bcast-inner900`), four of them rising by more than a percent. Ten
     of the eleven cells were predicted to move down and did not, which
     is the prediction's own second disjunct: **warming does not reach
     the baseline.** What the swap did buy is prediction 1's sibling finding
     below — the wild cell — so the roster move is vindicated by the controls
     and not by the anchors, and a predecessor's one large allocation
     is evidently not the same lever on `list` as the nursery size is ([the
     floor section][floor] measures the latter at 1.79× on one shape).
  4. **Held, and it is the run's main result.** `mut-odo` reads **0.8632**
     of its unaligned self and `build` **0.8771**, each on 22 shapes of 24,
     against a registered ~0.85 and the gate's 0.8836 and 0.8778; the two agree
     to 1.6% where the gate had them at 0.7%, against a per-shape floor the gate
     put at 6.3%. The four already-resident `mut-odo-vecdims` arms moved a few
     percent at most, as registered, and all four the *slower* way — 1.0069,
     1.0143, 1.0326 and 1.0378, the last on 0 shapes of 24 — which
     the registration allows for as the shim's own NOP cost and which is worth
     carrying as a measured price rather than a possibility. For the rest
     of the roster the moves do fall in two groups: two arms at 0.86 to 0.88
     and every other at 0.97 to 1.07. An independent route agrees: differencing
     whole-process wall time at a fixed `-n`, five interleaved pairs
     on `stretch-wide-2xM/build`, gives 0.887 where the reader's per-shape cell
     reads 0.8688 — two instruments sharing no code, 2% apart, on a cell whose
     own spread across passes is 8%. System time was 0.02 s throughout, so wall
     and user+system agree here and the two-clock caution finds nothing.
  5. **Held.** `list` reads **1.0058** aligned over unaligned, 8 shapes of 24 —
     0.6% where the gate read 0.3%, and inside the unaligned half's own 1.00%
     A/A floor. The baseline is still, so the denominator holds, the three
     things resting on this one stand, and the mixed-basis page is readable.

  **And the roster fix is confirmed at full budget, which no prediction
  claimed.** Run 9's `bq-expand` distant twin read 1.0152 with **41.4% on one
  cell** of `vgg-14-c512-k3`; the same pair now reads 1.0043 with its worst cell
  1.67%, and the six A/A pairs span 1.0011 to 1.0100 unaligned and 0.9987
  to 1.0054 aligned. The three-bench probe that priced the fix at 0.24%
  is thereby reproduced over the whole roster and the whole shape set. What
  the aligned half does *not* do is tighten the floor everywhere: it halves
  the main set's (1.00% to 0.54%) and leaves `scaled` with a 5.36% pair on one
  cell of `scaled-super-r3`, the run's one bad control.

- `STANDING` **The registrations those verdicts are read against.** Its order
  was chosen for heap state — `sum-only-early` above `list`, so nothing
  is measured on an ungrown pool — and the layout it happens to give
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
     figures](#the-mutable-ceiling-not-taken) is withdrawn — which
     is the outcome this page has the most reason to want detectable,
     the suspension being its own. **Sharpened by the pad probe**, which prices
     each offset instead of each side of the boundary: their present values
     are what a deep straddle over a resident control predicts, 1.18, and after
     the move all four copies sit resident, where the probe's own resident
     offsets span 0.904 to 0.956. So the collapse should be to between 1.00
     and 1.05, and anything near 1.16 still kills it. Do not interpolate the 36
     across the boundary — the penalty steps between 36 and 37 rather
     than ramping. **Read on the unaligned half**, which is the half
     these offsets belong to; on the aligned half all four copies sit at 0,
     so the same three ratios must read 1.00 outright, and that is the stronger
     form of the same test — a 1.16 surviving alignment would kill
     the hypothesis where a 1.05 could still be argued.
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
     ratio rise with them — but not uniformly, and the excess-allocation rule
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
     with it, so the reading-together above can be done off the page. That
     is a ruling and not a coincidence: had the unaligned fingerprint
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
     — and `NOINLINE`, the obvious fix, is already on these arms: adding
     it a second time is a compile error and the symbols are absent regardless,
     GHC emitting the module's code under a handful of workers. Measured
     2026-08-10, and recorded so the routes are not retried.

     What *did* work is the case-by-case form, and it is why six arms can
     be registered at all: take a loop's bytes from a `-g3` build, where
     `addr2line` names the `Main.hs` line and so the arm, then find the same
     bytes in the release binary. It succeeds when a loop is distinctive
     and fails when it is not — the 30-of-957 figure is the wholesale version
     of this, and a loop shared by two arms is ambiguous by construction, which
     for `build` and `mut-odo` is the very fact being measured. So attribution
     is available one arm at a time, at the price of a second build and a hand
     check, and is not available as a sweep.

     What is registrable is the six arms whose loops this page has already
     identified, read off `micro-unaligned` with `loop-offsets.py`: the fills
     sit at `[3, 53, 59, 45]` and `[16, 0, 36, 36]`, and all eight copies go
     to offset 0 in `micro-aligned`. So **`build` and `mut-odo` should each run
     about 0.85 of their unaligned selves** — from 45 and 53, both deep
     straddles at about 1.10, to the resident level near 0.93 — while their
     *ratio* stays at 1.00, which is what makes this a different measurement
     from prediction 2 rather than a restatement of it. The four
     `mut-odo-vecdims` arms are resident already, at 16, 0, 36 and 36, so they
     should move by a few percent at most, and the three ratios by less. An arm
     here that moves the wrong way, or the pair moving apart, is a finding.

     For the rest of the roster the prediction is aggregate and weaker, and says
     so: the moves falling in two groups rather than smeared, and the count
     that can move bounded by the short loops the shim rescues — 50
     of `micro-unaligned`'s 115 straddle where none of `micro-aligned`'s do,
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
     published ratio on this page divided by a moving denominator, and that
     is a larger finding than anything the run was built to get. *May*, because
     `list`'s hot loop is **library code and not Main's**: `fbList` is one line
     over `VS.fromListN` and `toListT`, and no loop in a `-g3` build resolves
     to its source lines, so the shim cannot align it and only
     the phase-matching keeps it still. Its expected stillness therefore rests
     on measurement and not on mechanism — 0.5% across four rebuilds, which
     rerolled the libraries too — which is weaker ground than the six arms stand
     on and worth saying before the number is read.

     **Three things rest on this one, and no other prediction here carries more
     than itself** — which is why it is read first and why a failure is not one
     prediction lost but the run's arrangement to reconsider. Prediction 3 has
     no fixed anchor without it and says so. Run 10's mixed basis, its main
     table unaligned and its eight class blocks aligned, is tolerable only while
     the two halves' baselines agree. And the transition to Run 11 turns on Run
     11's second column succeeding Run 10's unaligned table, which a moving
     denominator would put in doubt as well. The gate below already reads
     it on every shape and at the ordinary budget, so what the run adds
     is not coverage but company: `list` there shares a process with 33 other
     arms instead of four, and heap state and code position are exactly what
     this page has measured moving a figure when no strategy changed.
     That is the reading all three wait on.

  **The gate has been run and the three testable predictions hold** (2026-08-10,
  five benches over the 24 shapes, two passes per half in the order unaligned,
  aligned, aligned, unaligned, so both binaries carry the same mean position).
  Prediction 4: `build` reads **0.8836** of its unaligned self and `mut-odo`
  **0.8778**, so alignment is worth **12%** to each and the two agree to 0.7%,
  which is what one worker in two places should do. Prediction 5: `list` moves
  **0.3%**, so the baseline is still, the denominator holds, and the library
  reroll does not reach the one arm whose loop is library code —
  the phase-matching earning its keep. Prediction 2: the pair reads 0.9754
  and 0.9805 unaligned, 0.9610 and 1.0082 aligned, nowhere near the 1.13 or 0.86
  earlier runs saw. Run 10 is worth its evening on this; what a gate of five
  benches and two passes cannot say is anything about the rest of the roster.

  **Two corrections come with it.** The registered 1.00 for prediction 2 was too
  strong: the pair sits at ~0.98 on both halves, where the pad probe's own
  both-resident binaries sat, so the arms' intrinsic ratio is **0.98 rather
  than the 0.9973** [the floor section][floor] carries — an estimate
  that assumed the two arms share one penalty curve, which their 5.9%
  disagreement at offset 13 already contradicted. It costs the arms nothing,
  since they share a worker but not a call path, `build` being `mut-odo` driven
  through `vBuildVS`. And **offset 0 is measured for the first time**:
  the probe's eight offsets were all congruent to 5 mod 8, so the 0.85 predicted
  here was an extrapolation from the resident mean, and the gain at 0 is 12%
  rather than the 15.6% that implied.

  **The gain is not a constant, which prediction 4's aggregate form should
  say.** Read shape by shape it runs 0.719 to 1.031 for `build` and 0.763
  to 1.033 for `mut-odo` — 28% at the best shape and a slight loss at the worst
  — against a per-shape noise floor this gate puts at 6.3%, that being
  the median disagreement between the two arms' own gains where identical code
  says they should agree. So the extremes are real and the middle
  is not resolvable on two passes: the 12% is a geomean over a structured
  distribution and not a factor every arm pays. **Asked over 24 shapes
  and answered, so it retires** (2026-08-14, arithmetic over Run 10's two kept
  main sets, no machine time). The gain spans 0.773 to 1.025 on `build`
  and 0.697 to 1.018 on `mut-odo`, at geomeans 0.877 and 0.863, while the arms
  whose loops did not straddle sit flat — `list` 1.006, `mut-odo-vecdims` 1.007,
  `bq-expand` 1.002 — which is the instrument saying it works. Against the four
  variables this entry named, the Spearman of log gain reaches |0.38| at most,
  and the two largest, `mut-odo` against `l` at −0.36 and against `m` at −0.38,
  fall to −0.04 and −0.02 on `build`, which no size law could do. The two shapes
  showing no gain at all, `stretch-pow2stride` at 1.007
  and `stretch-square-1341` at 1.025, are mid-range in every dimension.
  So the 12% is a geomean over an unordered distribution: there is no shape
  ordering to find, and the question is closed rather than parked.

  **The correction term moves too, by 0.6%.** Both `sum-only` halves read 0.9939
  and 0.9938 aligned over unaligned, agreeing to a digit over a range of 0.990
  to 0.998, so the forcing pass is itself slightly faster in the aligned build —
  its own loop presumably being among the fifty the shim rescues.
  It is subtracted from every figure, so it is not a term that cancels between
  the halves; at 0.6% of a fraction of each cell it cannot reach the 12%,
  but a later reading that needs the halves to share a correction should know
  they do not quite. Allocation, by contrast, is identical to 2.5e-6.

  **The gate read the aligned half as the noisier one and the full budget says
  it is not.** Over the gate's five benches its median CI% was 0.532 against
  the unaligned half's 0.218, and its two passes disagreed more (`mut-odo`
  at 1.0224 against 0.9859), which left open whether alignment widens
  the per-cell interval structurally. Over Run 10's 816 cells a side the two
  halves are indistinguishable: median CI% **0.138 against 0.134**, median R²
  0.99997 on both, and the aligned cell is the wider one 389 times of 816.
  So the widening was the gate's own sample size, and alignment removes
  a systematic term at no cost in precision. That closes the question the gate
  raised, which is what the full budget was wanted for.

  The first two were arms of one prediction, either of which could kill it,
  on arms already rostered and at no extra machine time; the third priced what
  the order change was for and carried its own control; the fourth is why
  the run was two binaries and the fifth is what made the fourth readable.
  The pad probe having answered the hypothesis first, the first two
  were replications carrying point predictions rather than the evidence — which
  is what that probe's window was spent to buy, and why the run's own weight sat
  on 4.
- `ANSWERED` **What costs `mut-odo-vecdims-add-out` its 16%, now that layout
  cannot? Asked and answered the same day: it is a per-run cost, and the Core
  reading had it right all along.** Run 10 read the arm 1.1266 with its loop
  resident and 1.1612 with every copy at offset 0, so the suspension [the
  ceiling][ceiling] carried is withdrawn and the cost is the arithmetic's.
  Regressing the per-shape penalty on the aligned half — arithmetic
  over the run's own cells, no machine time — puts it at r **−0.64** against log
  `sInner` and **−0.01** against log `m`, 1.423 where `sInner` is 3 and 0.997
  where it is 64. That is the signature of work done once per run and amortized
  over the run's elements, which is what the `scanr (*)` stride table is;
  the account is [in the ceiling section][ceiling]. What made this unanswerable
  before is that Run 9's copy of the shared loop straddled a cache line, adding
  a *per-element* term that flattened the very correlation the question turns
  on — so the pairing bought a mechanism here and not only a number. `add-both`
  tracks it at the same r and the corner's sub-additivity says the two axes
  largely pay for one thing. **And the third axis is migrated here, 2026-08-14,
  from where it was answered and left**: why the count-down form pays was raised
  inside [the mutable ceiling][ceiling]'s own write-up, which is where
  the answer sits too — of the three axes FastReshape's loop arithmetic ports,
  one is free, one costs 16%, and the count-down form is the third, recovering
  most of the corner's loss at 0.9408 against it on 22 shapes of 24,
  and reproducing Run 10's reading. Recorded here because the list is meant
  to be the only home, and a session mining it walked past this one.
- `OPEN` **What is the 3% that survives alignment on `build`/`mut-odo`?**
  With both copies of one worker at offset 0 the pair still reads 0.9685
  on the main set, tying by the sign test (16 of 24) while the interval misses
  1, and it runs 0.9148 to 1.0335 across the nine populations. The gate's
  correction already put these arms' intrinsic ratio at 0.98 rather than 1,
  on the pad probe's both-resident binaries, so Run 10 reproduces that at full
  budget rather than contradicting it.

  **Run 11 says the residual is not stable within itself, which is new.**
  Re-running that binary puts the pair at **0.9467** on the main set at 21 wins
  of 24, sign p 0.00028, where Run 10 read 0.9685 at 16 of 24 and called
  it a tie — the point estimate moving two points and the sign test from tie
  to decisive with nothing changed. Across the nine populations it runs 0.9215
  (`revsome`) to 1.0209 (`slice`), reproducing Run 10's 0.9148 to 1.0335
  as a span while the individual classes swap sides: `bcastmid` and `slice` put
  `build` behind, `reshape1` puts it ahead by 5% where Run 10 had it behind
  by 3%. And these two arms are the ones the repetition finds least stable
  anywhere — `mut-odo` the only arm whose geomean leaves 1.5%, `build` holding
  the two widest cells after the wild one ([the floor section][floor]).
  So the 3% is not one quantity waiting to be attributed: whatever
  it is fluctuates run to run on arms whose code, layout and slot are all
  pinned, and an experiment that prices it once has priced one draw. **And three
  draws now exist without one being run**: the between-process spread instrument
  below reads this pair on Run 11, Run 12 and Run 13 alike, and puts `build`
  in the widest three every time — so what this entry wanted a run to supply,
  the kept artifacts already carry, and the open question is the account rather
  than another draw.

  **The Core route is closed and is not to be re-proposed.** The obvious
  candidate is the call path — `build` being `mut-odo` driven through `vBuildVS`
  — and it has been dumped three times, from Run 6's source, Run 7's, and Run
  8's commit under this regime: there is no call path to find, `vBuildVS`
  surviving as no top-level binding in any of them, the two workers
  byte-identical once numbering is normalised, and the sources differing only
  by the `Strides` newtype's zero-cost cast ([the mutable ceiling][ceiling]
  keeps the dumps' verdict). A fourth dump would reproduce that and nothing
  else.

  **Narrowed the same day, to about a percent, and not attributed.** The next
  candidate after the call path is that the shim aligns loop heads
  and not procedures, so putting both inner loops at offset 0 leaves everything
  about where the two procedures sit — their cache sets, their neighbours,
  the outer odometer recursion's own alignment — different. [The floor
  section][floor] had the build that tests it, a `-fproc-alignment=64` one
  in which the two procedures are 64-aligned and internally identical so both
  copies land on the *same* offset, built and read and left untimed; timing
  it is a filtered A/B and it now reads 0.9893 against 0.9782 for the shim's
  build and 0.9585 for neither. **Sharing an offset is now refuted as what makes
  the pair tie**, and from data already in hand: the named map puts `mut-odo`
  and `build` both at offset **0 in both Run 12 halves**, and the pair reads
  0.9822 in one and 0.9431 in the other — sharing an offset in both, tying
  in neither, 3.9 points apart. The reading below is what that replaces.
  **Sharing an offset was what appeared to make the pair tie** — both
  same-offset builds do, the different-offset one does not — but the two ties
  cannot be ranked against each other on one pass, their intervals overlapping
  and their sign tests disagreeing about which is flatter. So procedure
  placement is still a candidate and not the answer, and the honest bound
  is that these two names differ by about a percent once their copies share
  an offset, part of which is roster context rather than either arm. The shim
  *and* the flag together would have ranked them; that build was made and timed
  on 2026-08-11 and **does not**, landing about a percent nearer level inside
  a 1.8 to 2.3% repeat spread, so procedure placement stays a candidate. A small
  filtered test beside it prices a shared straddling offset at 8 to 13% on both
  arms and the flag at 2 to 4% over the shim alone — indicative only,
  and a reason to pad any pair that adopts the flag ([the floor
  section][floor]).

  **Run 12 gives the candidate its first full-budget term, and the term
  is large.** Its two halves differ in `-fproc-alignment=64` and in nothing
  else, which is the flag whose whole action is moving procedure starts —
  and the pair reads **0.9822** on the basis, tying at 16 wins of 24 with sign p
  0.15 on an interval covering 1, against **0.9431** on the flag half at 17
  of 24, sign p 0.064, on an interval that misses it. **That is 3.9 points
  between two binaries with code, roster, order, shapes and shim all pinned**,
  and it is the widest a within-run pairing has moved this pair: Run 11's two
  halves parted by 3.1 points and Run 10's by 1.5. So procedure placement
  is no longer only a candidate that a filtered probe could not rank —
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
  this pair does not contain, so it is not a contradiction — but it is a reason
  not to carry that reading forward as though it described this one.
  And the flag moves procedure starts and the offsets they produce together,
  exactly as [Run 12's second registered prediction](#what-is-open) records,
  so this four-point term prices the package and does not attribute it.

  **Across the nine populations Run 12 runs 0.9013 (`reshape1`) to 1.1644
  (`window`)**, against Run 11's 0.9215 to 1.0209 and Run 10's 0.9148 to 1.0335,
  and the classes swap sides again — `bcastmid` (1.0365) and `window` put
  `build` behind where `reshape1` puts it ahead by 10%. Read the top
  of that span as the two-shape populations it comes from rather than
  as a finding: `window`'s is two cells at sign p 1. What the span says is what
  the entry already said, one run more strongly — whatever the residual is,
  it is not one quantity waiting to be attributed.
- `ANSWERED` **What Run 11 was built to answer, registered before it ran —
  and what it answered.** Three questions, each with what would count
  as an answer, so that a run reporting "nothing moved" reports a result rather
  than a failure. All three are answered; the third only in part.
  1. **The repetition, owed since Run 9: answered, and the bound is a quarter
     of what it was.** With the basis half Run 10's aligned binary byte
     for byte, `list`'s per-shape scatter is **0.958 to 1.043** against a 0.25%
     geomean, where Run 10 widened it to 0.902–1.181 against 0.4%.
     Over the roster, 495 of 762 cells are within 1% and every arm's geomean
     is within 1.5% bar `mut-odo` at 1.0327. So the drift this page has
     been quoting was mostly the layout it could not hold still, and what
     a figure may do between runs for no reason at all is a few percent per
     cell.
  2. **Max-skip across the roster: answered, and the vecdims arms split two
     and two.** `build` and `mut-odo` are unmoved as predicted (0.9896
     and 1.0221, both halves putting their executed copies at 0).
     `mut-odo-vecdims` (1.0074) and `-add-both` (1.0333) keep the whole NOP cost
     Run 10 measured for them (1.0069, 1.0326); `-add-in` (1.0036)
     and `-add-both-down` (1.0029) shed most of theirs (1.0143, 1.0443).
     That is the two-and-two the pair note predicted from the offsets, read
     as arms rather than as a family, and it is what a full-budget run could
     resolve where a filtered pass could not. Across the rest of the roster
     nothing reads below 0.99 but `build`, and `bq-mut` reads 1.0588
     with the maxskip half ahead on 23 shapes of 24: **max-skip is the cheaper
     build nearly everywhere, at a third of the padding.**
  3. **Whether a resident offset costs anything: narrowed, not settled — and one
     of the two arms it was read on was the wrong arm, which the naming has
     since caught.** The two vecdims copies max-skip left at their own offsets,
     24 and 8, are `mut-odo-vecdims`'s and `-add-in`'s, and they run 1.0074
     and 1.0036 against the same code at 0. The 1.0333 this entry quoted beside
     them is `-add-both`'s, whose copy sits at 0 in both halves and so is
     not a resident-offset reading at all; the arm map is [with
     the naming][open], and the split it corrects is at Run 12's second
     prediction below. The direction survives on the two arms that are really
     resident — what the fully padded build charges for aligning them exceeds
     what their offset costs, the same sign on both, as the isolated
     reproducer's ~2% predicted — and the magnitude comes down to
     under a percent. What it does not give is the offset's own price,
     the padding and the offset moving together in every arm here. Separating
     them needs a third build that moves one head without padding before it,
     which is `-fproc-alignment=64`'s territory and wants a probe of its own —
     and what such a probe is now worth is at Run 12's second prediction below,
     which retires it for the split and prices what is left of it
     for this family.

  **And what it must not do was add an arm** — the third `-nosum` one the queue
  then called due — since the repetition needed membership pinned as well
  as layout. It did not; that arm waited past Run 12 as well and is Run 13's,
  and the ordering rule is in the queue entry too.
- `OPEN` **What Run 12 was built to answer, registered before it ran, and how
  it came out.** Four questions, each with what would count as an answer,
  so that a run reporting "nothing moved" reports a result rather
  than a failure. Registered 2026-08-13 before the evening and answered the same
  day; the verdicts belong here rather than in the run's own chapter, which
  the next run replaces. **Two answered, one refuted, one still a gap** —
  and the refuted one is the run's finding.
  1. **What the flag costs across the roster, as a package.** Run 11 priced
     the shim; this prices `-fproc-alignment=64` on top of it, read
     as `run12-maxskippa` against `run12-maxskip` over the main set with each
     class's own table beside it. What counts as an answer is a direction
     and a magnitude clearing the drift band Run 11 measured — at most 3.3% per
     arm, most under 1.5%, 495 of 762 cells within 1% — so an arm inside
     that band is not evidence either way, and "nothing moved past drift"
     is itself the answer if that is what comes back. The decision it feeds
     is which half publishes the table.

     **ANSWERED: the flag costs, and the basis stays without it.** Of the 24
     timed arms, 19 are slower under the flag, and of the five that are not only
     `build` (0.9913) is so by more than a quarter of a percent. Two clear
     the drift band, `bq-mut` at **1.0516** and `offtab` at **1.0502**,
     with `mut-odo` (1.0324) and `bq-gen` (1.0284) just inside it. So pinning
     every procedure start buys nothing this roster can see and charges two arms
     five percent, and the table is published from `run12-maxskip`. Run 13
     inherits the plain max-skip half.
  2. **Whether the two-and-two vecdims split survives the flag.** Run 11 found
     the four arms splitting two and two — `mut-odo-vecdims` (1.0074)
     and `-add-both` (1.0333) keeping the whole NOP cost Run 10 measured
     for them (1.0069, 1.0326), `-add-in` (1.0036) and `-add-both-down` (1.0029)
     shedding most of theirs (1.0143, 1.0443) — and that split was predicted
     from the offsets in the pair note before it was read. The halves' fills
     differ again, `[11, 0, 4, 0]`/`[24, 8, 0, 0]` against
     `[4, 0, 4, 0]`/`[8, 8, 4, 4]`, and Run 11's third question priced the two
     copies max-skip left resident, at 24 and 8. **Which arms those were has
     since been derived and is not what this sentence assumed** (2026-08-13,
     in `run12-pair.txt`): naming the copies off a `-g3` twin and matching
     by byte identity puts `mut-odo-vecdims` at 24 and `-add-in` at 8,
     so the resident pair is 1.0074 and **1.0036**, while `-add-both`'s 1.0333
     sits at 0 beside `-add-out`. One arm of each kind is resident and one
     is at zero, so residency does not sort the split — a second refutation
     of the offsets account, independent of the paired reading below
     and available from these binaries all along. So the prediction is
     that the split persists under the flag rather than closing. The reading
     is the four arms' paired geomeans, `maxskippa` against `maxskip`,
     and it needs no offset mapping. **What kills it** is the four moving
     together, the split closing, which would say the offsets are not what
     it was about. What this does *not* license is tying a named arm to a named
     offset: `loop-offsets.py` labels every `Main` copy with the same mangled
     symbol, and its docstring pins the entry order of the `build`/`mut-odo`
     group alone, so the vecdims group's order is recorded nowhere and would
     have to be derived before any per-arm offset claim is made.

     **REFUTED, on its own kill condition.** The four read **0.9996**,
     **1.0035**, **0.9988** and **1.0003** — a spread of 0.47 points where Run
     11's was 3.0 — so they moved together and the split closed. What that rules
     out is the split being about resident offsets *as such*; what it does
     not establish is any positive account of Run 11's split, this pair moving
     every procedure start rather than the two copies max-skip left resident.
     **So Run 11's split is now an open question rather than an explained one**,
     and the probe this entry once named as what would settle it — one arm
     stepped through several offsets with no straddle anywhere, on the pad-probe
     model — **is not it, for three reasons the naming has since supplied.**
     That probe has been run, on `build`/`mut-odo`, and its graded penalty
     and resident spread are [in the floor section][floor]; what it never
     touched is the vecdims family. It cannot reach the two arms the split turns
     on, `-add-out` and `-add-both` sitting at 0 in both of Run 11's halves,
     so no sweep of offsets can explain a difference their offsets did not make.
     And on the two it could sweep the quantity is bounded small already:
     `mut-odo-vecdims` at 24 and `-add-in` at 8 differ from the same code at 0
     by 0.74% and 0.36% *including* whatever the NOPs cost, which is inside
     the drift band and beside the A/A floor.

     **What is left as the candidate is the NOPs themselves, and it is a static
     question rather than an evening.** An arm pays for a padded head wherever
     one falls on its hot path, its own fill's or a helper's,
     and the unconditional form pads every head where max-skip pads only
     those that need it — so the split should follow which arms carry a skipped
     head. Rebuilding the two assemblies costs seconds, the heads each form
     gives a directive are the shim's own output, and attributing them to arms
     is `addr2line` on a `-g3` twin, which the naming below made ordinary.
     That wants no machine time and no quiet window. A vecdims offset sweep
     is what it falls back to, and would then be answering whether this family's
     loop is offset-insensitive rather than anything about the split.

     **And the naming since says the same without a second run, which is what
     the derivation this entry asked for was worth.** The copies max-skip left
     resident are `mut-odo-vecdims`'s at 24 and `-add-in`'s at 8, which read
     1.0074 and 1.0036 — one on each side of Run 11's split; `-add-out`
     and `-add-both`, the two largest readings the family has at 1.0513
     and 1.0333, sit at 0 in both halves. So the split crosses the resident
     copies rather than following them, and it was never about them. It also
     shows the family is five arms where the split as recorded names four,
     `-add-out` being the one left out and the largest of them. The map is [with
     the naming][open].
  3. **Membership invariance decides the basis and this run does not measure
     it.** Registered as a gap rather than a question, because the queue turns
     Run 13 on it and a later session could read this run as having tested it.
     Run 12 adds no arm — the third `-nosum` one was deferred out
     of it precisely so it would not arrive in the same run as a change of shim
     — so invariance under the flag is an argument from what the flag does,
     pinning every procedure to a 64-byte boundary, and not a reading taken
     here. What would settle it is a membership change on the adopted half
     with the offsets read either side, which is Run 13's first debt
     if the basis lands on max-skip without the flag.

     **The condition was met and the debt is PAID, on 2026-08-13**: the basis
     did land on max-skip without the flag, and the check that made due came
     back clean, recorded once with [the roster's other debts][open] and read
     there rather than restated here.
  4. **The free draw on the wild cell.** A new basis, a new allocation history
     and six A/A worst cells, against the standing question of whether a fresh
     wild cell turns up somewhere else or the same one returns. Three outcomes
     and all three report: `lenet-L1-28-c1-k5/bq-expand` returns, a new cell
     appears elsewhere, or the run is clean. It is a draw and not a test,
     so a clean run refutes nothing.

     **THE RUN IS CLEAN**, which is the third of the three outcomes. The worst
     A/A cell is 4.03% on the basis and 3.23% on the flag half, and 5.19%
     anywhere in the run (`bcastmid-primes`), against the 44%, 41.4% and 35%
     of Runs 8, 9 and 11. The named cell did not return, and the kept per-shape
     record shows it from outside the A/A machinery: `lenet-L1-28-c1-k5`'s
     `bq-expand` fingerprint cell reads **0.130** where Run 11 published 0.175,
     a ratio of 1.35 against the 1.355 that run measured for the wild cell
     itself. Three sightings in four runs is now three in five; the mechanism
     question stays with the wild-cell entry, whose surviving account a clean
     draw refutes nothing about.

  **And what it must not carry** is the resident offset's own price. The pair
  moves padding and offset together, so that stays a probe on the pad-probe
  model rather than anything this run can be read for — a probe worth less
  than it was when this was written, for the reasons two paragraphs up.
- `ANSWERED` **What Run 13 was built to answer, registered before it ran —
  and what it answered.** Its pair was `run13-maxskip`, Run 12's basis recipe
  unchanged, against `run13-lookrts`, carrying two changes at once by request:
  the shim's look-through (`LOOP_LOOKTHROUGH=1`, 422 loop heads given a budget
  where the basis form gives 395) and an RTS default line of `-I0 -T -M8G`
  in place of `micro.cabal`'s `-T -M2G`. **All four are answered, and the first
  is a null the registration named as an answer in advance.** (1) *What
  the package costs across the roster*: **nothing past drift**. Of the 30 arms
  compared, 26 sit within 1% of 1 and the four outside are `mut-odo` 0.9794,
  `bq-gen` 0.9861, `gen-unsafe` 0.9875 and `offtab` 1.0269 — the largest 2.69%
  against a drift band of at most 3.3% per arm — with twelve arms below 1,
  eighteen above and the geomean over the thirty at 1.000. So **Run 14's basis
  may take the look-through and the RTS line as a decision rather than
  as a measurement**, which is the choice this priced and is now [carried
  forward](#what-run-15-compares-against) — where it was taken on 2026-08-14,
  that recipe being Run 14's basis and its `-M8G` the precondition
  for the `-A1G` half beside it. (2) *The gap*, that the pair cannot separate
  the two changes: it stayed a gap and cost nothing, a null result adopting
  or dropping both together and needing no attribution. No follow-up half
  is owed. (3) *The discriminating reading*, registered in advance for the case
  where something moved: **unused, and recorded as unused**. A shim movement
  was to look like placement — scattered, no consistent direction — and an `-I0`
  one broad and one-directional; what came back has neither shape, straddling 1
  and netting to nothing. The registration's own third outcome, *a movement
  with neither shape is the interesting one*, did not arise because there
  was no movement. (4) *The `-nosum` arm's first full-budget row*: delivered.
  `mut-flat-gm-nosum` is in the Results table with its `needs` cell filled —
  as *the same, on a third write pattern*, the column's descriptive convention
  for a control rather than the shippability phrase this entry first proposed,
  every other control row naming what it controls for. Its in-situ term reads
  below 1 like the other two on every population, which is the reading [gate
  3](#what-is-settled-and-where) wanted. **And the standing free draw came up
  clean**: no wild cell, `lenet-L1-28-c1-k5/bq-expand` did not return,
  and the worst A/A cell anywhere was 11.59% at `scaled`'s standing slot — which
  is that slot's own hazard and not a new one.
  1. **What the package costs across the roster.** Read as the two halves'
     paired geomeans over the main set, arm by arm, with each class's table
     beside it. What counts as an answer is a direction and a magnitude clearing
     the drift band Run 11 measured — at most 3.3% per arm, most under 1.5%, 495
     of 762 cells within 1% — so an arm inside that band is not evidence either
     way, and *nothing moved past drift* is itself the answer if that is what
     comes back. The decision it feeds is whether Run 14's basis takes
     the look-through and the RTS line, together, since that is how they
     are being priced.
  2. **It cannot separate the two, and one of the three RTS flags cannot bind.**
     Registered as a gap rather than a question, so that a later session does
     not read this run as having attributed anything: a null result adopts
     or drops both together, and a result that moves needs a follow-up half
     carrying one variable. Of the RTS flags, `-T` is in both halves and `-M8G`
     raises a cap nothing approaches — a main-set process peaked at 218 to 220
     MiB in Run 12 and a one-shape `-L1` pass at 22 MiB, against the 2G
     it replaces — so the live variables are the idle GC and the pad.
  3. **A discriminating reading is available if something does move, and
     it is registered here rather than invented afterwards.** The shim half
     differs by **one pad**: of its 27 extra heads the assembler declines 26,
     and the one that fires moves everything after it by a whole line. Measured
     on the pair itself, 2026-08-14, off `nm` and the two `.text` images:
     the pad lands inside `Main_zdWT_info` at `0x417a40` as five 11-byte NOPs
     and a `90`, every one of the 29342 library symbols downstream sits **64
     bytes** later, the 39 before it do not move, and the shift is absorbed
     before the tail, which is why both `.text` sections are byte-identical
     at 20377797. The 47 is the assembly's own padding count, 3941 bytes against
     3988, and not the displacement. So a movement belonging to the shim should
     look like placement — scattered across arms, no consistent direction,
     the size Run 11's repetition measured — while one belonging to `-I0` should
     be broad and one-directional, the idle GC acting between every bench alike.
     Neither shape proves its cause; a run whose movement has *neither* shape
     is the interesting outcome.
  4. **The `-nosum` arm's first full-budget row**, which is a deliverable rather
     than a question: `mut-flat-gm-nosum` landed after Run 12, so the roster
     is 840 benches against that run's 816, its Results row comes out with `?`
     in `needs` to be filled as *new mutating `Vector` method*, and the `-L1`
     roster pass the membership change made owed **has been run and passed**,
     on 840 benches of the main set and 105 of the `rev` class — what it covered
     is in the pair note, recorded there rather than here for the reason
     the gate's verdict is, that it belongs to the pair and should not be paid
     twice. **And the standing free draw**, unchanged from Run 12: a new basis
     and six A/A worst cells against the question of whether a wild cell returns
     at `lenet-L1-28-c1-k5/bq-expand`, turns up elsewhere, or does not appear.
     It is a draw and not a test, so a clean run refutes nothing.
- `ANSWERED` **Which arm owns a loop copy: answered, and the answer is
  that a binary can carry its own names.** Run 12's second prediction had
  to record that tying a named arm to a named offset was not licensed, every
  `Main` copy printing under one mangled symbol because these arms compile
  to one worker. A `-g3` build carries what is missing — GHC emits a per-block
  symbol with DWARF line info — and `loop-offsets.py` now reads it without help:
  `addr2line` for the source line, the source file for the top-level binding
  that line falls in, so a copy prints as `fbMutOdoVecdims` with the source line
  beside it instead of as one worker's mangled name. A binary with no line info
  prints exactly what it printed before. Read that way on 2026-08-13,
  at `-fspec-constr` with `LOOP_MAXSKIP=1`, the four-copy vecdims group is,
  in address order, `mut-odo-vecdims`, `-add-in`, `-add-out` and `-add-both`,
  and the pair beside it is `mut-odo` then `build`. That is the order [the floor
  section][floor]'s loop table assigns its per-arm offsets in, so that table's
  ordering is now a measurement; and a second route agrees, emission order
  tracking first reference from `roster`, which lists those four in exactly
  that order. What it bought is at Run 12's second prediction above: Run 11's
  split crosses the resident copies rather than following them.
  **The recommended next step is taken and its prediction is refuted**
  (2026-08-14, an unconditional build and a max-skip build from one source read
  with `loop-offsets.py`, against Run 11's two kept main sets).
  The unconditional form puts 100 of 100 Main self-loops at offset 0 where
  max-skip puts 58 of 113, and **neither leaves a straddler**, so what padding
  every head buys is padding that nothing needed. Per arm it buys `build` alone,
  at 0.9896, and costs the tail up to 5.9% — `bq-mut` 1.0588,
  `mut-odo-vecdims-add-out` 1.0513, `bq-gen` 1.0504, `-add-both` 1.0333,
  `gen-unsafe` 1.0327, `gen-quotrem` 1.0275, `offtab` 1.0259, `mut-odo` 1.0221.
  The arms that do carry a head max-skip skipped land on both sides of 1,
  `build` against `mut-odo`, and the three largest losers carry no tracked
  28-byte loop at all, the tracked set being `fbBuild`, `fbMutOdo`,
  `fbMutBaseOffsets` and the four vecdims fills. **What the two forms differ
  in beyond offsets is a census**: the unconditional pads sit inside enclosing
  loops and push thirteen of them past the 64-byte window, 113 self-loops
  falling to 100 and the 28-byte set 36 to 32. That is a cost of padding every
  head which the offsets alone do not show, and it is the better candidate
  the refuted prediction leaves behind. **And the step's own phrasing named
  a difference that is not there**: the two forms emit *the same 395 directives
  at the same heads*, on the same assembly lines, differing only in the max-skip
  budget written as each directive's third operand — a median 33 bytes of slack,
  four heads with none — so there are no per-form head lists to compare,
  and the 27 extra heads on record are look-through's rather
  than the unconditional form's. What the unconditional form spends is 8192
  bytes of `.text`, 20385989 against 20377797. **And the step's other half could
  not have been taken at all**, which is a dependency neither entry declared:
  attributing heads to arms wants `addr2line`, `addr2line` wants DWARF,
  and the naming entry above measures DWARF changing the code — a plain build
  holding two copies of a loop per function where the twin holds one,
  so the offsets-to-arms map is one-to-many in exactly the binary being timed.
  A plan resting on an instrument should say what the instrument is known
  to change. **And the instrument the residue wants now exists**:
  `loop-offsets.py --len 0` widens the grouped, named report from the 28-byte
  run-fill to every loop a cache line can hold, which in Main's own code is 112
  loops over twenty lengths against the nine of one length the tracked set saw —
  so the arms that lose most under the unconditional form, and carry no 28-byte
  loop at all, are visible to whatever asks next.

  **And the map does reach the timed binary, which is the question a twin
  raises.** The two builds are one source, each of the plain build's four
  vecdims copies sits within 192 bytes of exactly one of the `-g3` build's,
  and matching them by the normalised instruction window around each head —
  mnemonics with every displacement and immediate masked, the loop bodies
  themselves being identical — is a bijection that agrees with both: 74 and 75
  of 80 for `-add-out` and `-add-both` against a runner-up of 38, and 73
  for `mut-odo-vecdims` and `-add-in` against 70, those two arms differing
  in almost nothing but the add. `-add-both-down`'s 24-byte loop matches
  the same way at 75 against 3, and sits at offset 0 in the timed half,
  so today's basis recipe has the five at 24, 8, 0, 0 and 0. **The same matching
  says nothing about the `build`/`mut-odo` group**, every score there falling
  to 10 to 13 of 80 because `-g3` restructured that region when it dropped
  the two dead copies; what names those two is `addr2line` on the twin's
  survivors and the entry order already in the docstring. So the window method
  proposed as the fallback works where the code is stable and is silent where
  it is not, which is worth knowing before it is leaned on.

  **Run 13 exported its own and found the twin's fidelity is a per-GROUP
  property, not a per-binary one.** The same method names the vecdims four again
  — offsets 24, 8, 0 and 0 going to `mut-odo-vecdims`, `-add-in`, `-add-out`
  and `-add-both`, in that order, on both halves — and the bijection is cleaner
  than Run 12's, every timed head matching its own named counterpart at exactly
  1.000 on the basis half against a runner-up of 0.921 or less. The other
  tracked group, `[11, 0, 4, 0]`, it cannot name at all: all four copies share
  one byte-identical body, that body is the `fbMutOdo`/`fbBuild` worker the two
  arms compile to, and **the `-g3` twin carries only two copies of it where each
  timed binary carries four** — counted over `.text` in all four binaries.
  With no third or fourth name to give, the window match degenerates
  to near-ties an order below the vecdims group's. So the standing ruling
  that `-g3` is a different program bites group by group: count a body's copies
  in twin and timed binary before trusting the twin's names, which the vecdims
  group passes four against four and this one fails. Run 13's figures are
  in its pair note, which goes with its binaries.
- `ANSWERED` **The shim was blind under `-g`, which is why this wanted a fix
  and not merely a build.** `align-as.py` aligns a head only where the line
  before it is an instruction, that being how it refuses to put padding between
  an info table and the code the table belongs to; under `-g` every head follows
  the previous block's `_end` and `_proc_end` labels instead, so **not one head
  of a `-g3` assembly was given a directive** — 0 against the same day's plain
  assembly at 395, read off the two captures — and the build came out unaligned
  in silence: none of its 101 short self-loops at offset 0, 41 straddling,
  and two of those the timed fills of `-add-in` at 56 and `build` at 52.
  The guard now reads past the lines that emit no bytes, another label
  or a `.loc`, and the same build gets 421 heads a budget, 46 loops at 0 and one
  straddler left — a 44-byte loop in `mkBroadcastMid`, which is view
  construction rather than a fill and one of the heads the info-table guard
  is there to leave alone. **The look-through fires only where the assembly
  carries `.loc`, and that condition is the point rather than a nicety**:
  applied to every build it finds 27 heads more in the plain assembly, 422
  against 395, which would re-base every figure this page has published
  for a reason no strategy changed. So a `-g` assembly gets the corrected guard
  and every other keeps the literal one, byte for byte — which is the control,
  and it is an end-to-end one because a shim change reaches nothing otherwise:
  built from one source into **two fresh builddirs**, `-fforce-recomp` and all,
  the max-skip half comes out md5-identical under the fixed shim and
  under the shim as committed, each printing 395. **Those 27 are one shape
  of loop and not a scattering**: each is a pre-tested loop whose head carries
  a block label as well as its own, two labels at one address, so the literal
  guard read a label where an instruction had been the whole test. **And what
  they do to the binary is one pad**, which is the figure to have before
  spending a run on them: a directive is a budget and not a padding,
  and the assembler declines it wherever the loop already spans the least
  its length allows. Of the 395 the literal guard emits, **156 actually pad** —
  3941 bytes in Main's code, a median of three multi-byte NOP instructions each
  and 60 bytes at the longest — and adding the 27 makes that **157 pads and 3988
  bytes**. Twenty-six of the twenty-seven are declined; one fires,
  and everything after it moves 47 bytes. The short-loop populations agree
  that nothing else happened: 112 loops either way, none straddling in either,
  and the count at offset 0 going 58 to 57. So the question those 27 raise
  is not what NOPs cost. It is whether one more aligned loop is worth re-rolling
  the placement of everything downstream of it, which is the term this page
  prices at a few percent and cannot predict — a paired run's to answer
  if anyone wants it answered.
- `ANSWERED` **`-g3` is a different program, and what differs is register
  allocation.** Measured on the assembly GHC hands the assembler rather
  than inferred from the binary, both sides stripped of every `.loc`, every
  debug label and every `.debug_*` section and their label uniques renamed
  in order of appearance: 60056 instructions against the plain build's 59991,
  of which +63 are `movq`, with register assignments and block order differing
  throughout. What does not differ is what this page times — all three 28-byte
  groups have the same body in both builds — and the two copies the `-g3` build
  lacks are the dead ones, its `build`/`mut-odo` group holding two where
  the plain build's holds four and `addr2line` putting those two in `fbMutOdo`
  and `fbBuild`. That confirms by a second route
  the `[dead, mut-odo, dead, build]` reading `loop-offsets.py`'s docstring had
  asserted, and it is the naming's non-vacuity control: a scheme that names them
  must put those two in that order. `-add-both-down` is in neither group,
  its loop being the count-down form's 24 bytes as [the floor section][floor]'s
  table records, and `--len 24` finds it.
- `ANSWERED` **So building everything with `-g3` is refuted, and a `-g3` build
  is a twin to read rather than a binary to time.** The proposal was that
  if the timed binaries carried their own names there would be no correspondence
  to establish and a per-arm offset claim would become an ordinary reading;
  its own criterion was that the arms agree within the run's floor. They do not.
  A pair differing in `-g3` alone — one source, one regime, and needing no pad,
  the two `.text` coming out the same size with all 29449 shared library symbols
  at a whole-line delta — gates at `build` **0.9391, 0.9488, 0.9363
  and 0.9517**, plain over `-g3`, across the four pairings of two passes each,
  and `mut-odo` at 0.9626 to 0.9743, against each binary's own repeat of 0.9868
  and 0.9970 on `build` and 0.9958 and 1.0079 on `mut-odo`. Five percent
  and three percent, one direction, four to six times the floor, with `list`
  still to under 1.4% and no wider between the halves than inside one. What
  that prices is the package, the halves differing in emitted code
  *and* in where the executed copies land, 0 and 0 against 4 and 28 —
  and the package is what a basis decision wants. The `build`/`mut-odo` ratio
  moves with them, 0.9862 and 0.9952 in the plain passes against 1.0109
  and 1.0219 in the `-g3` ones, but all four are ties by sign test on intervals
  covering 1, so that is a point estimate shifting and not the pair separating;
  [the floor section][floor]'s shared-offset reading is neither confirmed
  nor contradicted at this budget. **The machine was not fully quiet**,
  its owner having said so while the gate ran, which is why the floor here
  is each binary's own repeat rather than Run 11's drift band; the palindrome
  cancels drift across the hour and all four pairings agree in sign and size.
  **Both halves were built with the look-through applied unconditionally**,
  which is the form that predates the `.loc` condition above and the reason
  it can be said the shim is held constant across them rather than treating one
  half differently: what the pair varies is `-g3`. That half is not the basis
  recipe byte for byte, carrying the 27 extra heads, but it places every tracked
  loop where the basis recipe does — the same `[11, 0, 4, 0]`
  and `[24, 8, 0, 0]`, checked on both forms — so what the gate compares is two
  builds whose timed loops sit identically and whose debug information does not.
  Rebuilding the pair from this tree therefore reproduces the `-g3` half exactly
  and the other with those 27 heads unaligned, which is the same experiment
  and not the same bytes. So the naming above is read off a twin and carried
  to the timed binary by the correspondence — the arrangement the recommended
  path meant to remove, and does not. **And the twin is short of copies as well
  as of registers, which is what bounds the naming** (2026-08-14, four binaries
  — the two timed halves, a fresh plain build and a fresh `-g3` twin — matched
  by body bytes rather than by proximity). One body reads four copies in every
  plain binary and **two** in the twin, and the twin's two carry distinct worker
  symbols that `addr2line` puts in `fbMutOdo` and `fbBuild`; the vecdims body
  reads four in all four binaries, which is exactly why that family names
  as a bijection and this group cannot be named at all. A plain build therefore
  holds **two copies of that loop per function** and `-g3` emits one —
  a duplication the debug build suppresses, the same class of divergence
  as the register allocation above, and the reason the recommended path's
  `addr2line` step can reach a function but never a copy — and the reason
  the NOPs entry's own next step was undecidable before it was attempted, which
  is recorded there.

  **And a weaker level is no way round it, which is the move to expect
  from a page that says `-g3` throughout.** `-g1` is the weakest GHC has —
  the users guide gives it as producing stack unwinding records for top-level
  functions, which is data about a program rather than a part of one —
  and it changes the emitted code exactly as `-g3` does: one instruction fewer
  and a different register assignment on an eight-line module, the same on GHC
  9.10.3, 9.12.4, 9.14.1 and HEAD, with `-g2` between them behaving alike.
  The reproducer and that table are horde-ad's
  `docs/ghc-issue-debug-changes-codegen.md`, filed as [GHC work item
  27687](https://gitlab.haskell.org/ghc/ghc/-/work_items/27687), which
  this page's finding produced; what they settle here is that no debug level
  is a cheap way to put names in a binary that will be timed.
- `OPEN` **A recurring transient that lands on the shipped arm's family, worth
  35 to 44%, and which no published column would show.** Not one cell: **three
  sightings in six runs**, moving each time. Run 8 read `bq-expand`'s distant
  twin 44% slow on `vgg-14-c512-k3` and Run 9 41.4% on the same arm and shape;
  Run 10 was clean; Run 11's aligned half reads `lenet-L1-28-c1-k5/bq-expand`
  at **1.355** of what that same binary read in Run 10 — a different shape and,
  this time, the arm's **own** slot rather than a twin's; Runs 12 and 13 came up
  clean. Run 10's roster fix (`sum-only-early` above `list`, so nothing
  is measured on an ungrown pool) removed the Run 8 and Run 9 instance
  and was confirmed at full budget; it did not remove the effect. **Decomposed
  on a kept instance, 2026-08-14, and it is mutator time with the work
  identical.** Run 11's aligned half carries one: `lenet-L1-28-c1-k5/bq-expand`
  reads 56.56 µs net there against 41.4 to 41.9 across the seven other processes
  on disk, with `list` normal in that same process, so it is the arm and
  not the process. Per iteration, wild against normal — time ×1.279, **mutator
  ×1.281**, gcWall ×0.980, GC count ×0.997, allocation **×1.000002**, peak heap
  equal — which is the same instructions on the same bytes running 28% slower,
  and excludes GC, the pool's cost and any extra work *inside the anomalous
  process* rather than in a filtered one that never had the state. It is also
  flat from first sample to last, so the state was entered before the bench
  began. **The cache-miss row is now the only unexcluded candidate rather
  than one of several**, and the published 35 to 44% is the net figure against
  a raw slope ratio of 1.279, the correction amplifying it. **And it is the tail
  of something common, swept over every kept main set the same day**: of 4029
  cells in the eight processes, 121 carry a step past 2% at `t` above 40 — 3% —
  the largest reaching 12 to 15%, and the arms carrying them are the ones
  this page already suspects, `build` at 20% of its cells, `offtab` 19%,
  `mut-odo` 16%, `gen-quotrem` 11%. **The axis is size, and it is not the spread
  instrument's axis**: step size against log `l` reads −0.70, where
  the between-process spread tracks `sInner` and rank instead, so the two
  instruments are measuring different things and neither subsumes the other.
  Incidence tracks `l` too (−0.64 raw), but sample count itself tracks log `l`
  at −0.93, so power is confounded with the effect there and only the size
  figure is clean; within an equal-power band the incidence correlation survives
  at −0.43. The four big shapes carry none at all. What this changes about
  the wild cell is that it is not a lottery among cells but the extreme
  of a distribution, which is why the `scaled` slot can stand in for it.

  **Three things make this a threat to a published claim rather
  than a curiosity.** It is *the expansion family* that is susceptible,
  established rather than guessed: Run 9's filtered probes put
  `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback` each
  35–40% above their published cells on that shape while
  `bq-scan-rem-gm-mulback` and `mut-odo-vecdims` did not move at all.
  That family contains **`bq-expand`, which is what `Data/Array/Internal.hs`
  ships and what this page recommends**. And **the table cannot show it**:
  the winsorized estimator caps the cell, so the row read 0.103 against 0.102
  and nothing looked wrong — the only reason it was seen is that `bq-expand`
  carries two A/A twins, which disagreed with it by 25%. An arm without twins
  would show nothing at all, which is most of the roster.

  The evidence against an intrusion is [in the floor section][floor]: clean
  twins, time-neighbours within 1.2%, CI% 0.06 over 125 samples, `list`
  on that shape unmoved.

  **The samples have since been read, and they say the cell is a shift and
  not a defect** (2026-08-12, arithmetic over the run artifacts, no machine
  time; a refit of `reportMeasured` reproducing criterion's own slope to 2e-16
  first, which is what says the sample layout was read right). Its per-iteration
  residual dispersion is **2.57 µs against its own twins' 2.76 and 0.70**
  in the same process, and against 2.20 to 2.79 for the same three arms
  in the maxskip half — so it is not the noisy one. Every arm there shows
  the same small warm-up in its first third, gone by its last, and the residual
  correlates with allocation and GC count at +0.5 to +0.8 on twins and arm
  alike, so neither is the cell's. Allocation per iteration is the same
  340193–340195 for all six. What is left is a clean 14.4 µs on the slope of one
  arm at one slot, with everything a sample can report looking ordinary — which
  is what Run 8 and Run 9 found at their cell too.

  **Read the rest of what a sample carries and the mechanism narrows sharply**
  (same day, same artifacts). Against its two twins in the same process the cell
  runs 68342 ns an iteration against 53896 and 53364 — and **259697 cycles
  against 204804 and 202781**, the same 1.28 as the time, so the clock
  is not moving: all three read 3.8000 GHz to four digits. Allocation
  is **340197 bytes an iteration against 340196**, one byte apart. GC time
  is **312 ns against 323 and 328**, so the arm collects no more than its twins
  and could not pay for 14.4 µs if it did. The whole excess is mutator cycles:
  the same instructions over the same bytes, stalling 28% more.

  **That refutes, for this instance, the account inherited from Runs 8 and 9.**
  Theirs was a cold block pool at a roster slot — an allocator warmth story,
  which predicts more or dearer collection — and here GC is flat and allocation
  identical to the byte. So either the pool was one trigger of something more
  general, or the two sightings are different effects wearing the same shape.
  What is left, code placement being identical (one binary, the same offsets),
  the data volume identical and the clock fixed, is **where the data sits**:
  the input, the offsets table and the output buffer are allocated per bench
  and their addresses are the one thing that differs between an arm and its own
  twin. This page has spent four runs on code placement and has never measured
  the data side.

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
     Nothing was missing but the reading — which [the
     procedure](#making-a-major-benchmark-run) already demands in as many words,
     a pair inside the floor whose worst cell is an order of magnitude outside
     it being a finding the aggregate is hiding. A sweep of every A/A cell
     of both runs puts the rate at **2 of 804 past 10%**, both of them this one
     incident, and 4 past 5%: rare, not a lottery over every cell,
     and concentrated where the twins are.
  3. **The data-placement hypothesis is refuted, and with it `setarch -R`.**
     A standalone probe allocating the same three buffers a bench does reports
     the same three payload addresses in every one of eight processes —
     `0x0042005fe010`, `0x0042005f6010`, `0x0042005cf010` — because the GHC RTS
     reserves its heap at a fixed base, so ASLR never moves it however
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
  and it predicts exactly what is seen — same binary, same slot, different run,
  one arm of a susceptible family 28% slower in mutator cycles with allocation
  identical to the byte.

  **What follows for reading a table, before any of it is measured further.**
  Four things, and the second is the one this page has been quiet about:
  1. **The A/A worst cell is a gate and not a note.** It is the only thing
     that caught a 35% error, and it caught it while every aggregate stayed
     green. A pair whose worst cell passes about 10% disqualifies that cell
     from the per-shape record and flags its row; listing it for adjudication
     is what let this one be read past.
  2. **Nine of the twenty-four timed strategies carry twins**, so that gate
     covers three eighths of the table: `bq-expand`, `bq-scan-rem-gm-mulback`,
     `mut-odo-vecdims`, and — added 2026-08-14, first read in Run 14 —
     `bq-odo-gm-mulback`, the susceptible family's own pure-tier head, `offtab`
     for [the spread question][open], and then `build`, `mut-odo`, `list`
     and `gen-unsafe` once the same day's readings said what the coverage
     was hiding: both anomalies on record landed on a twinned arm, so their
     apparent distribution is a fact about the controls before it is one about
     the machine. A wild cell on `bq-mut` or any other untwinned arm would still
     be capped by the estimator, would move its row by a thousandth, and nothing
     here would ever say so; that is the honest extent of the defence — now
     with `build` and `mut-odo`, whose 1.13× gap is Run 14's own registered
     control, inside it rather than outside.
  3. **Winsorizing is a defence and not only an estimator choice.** It is what
     held `bq-expand`'s row to 0.103 with a 35% cell inside it. [The `time`
     column](#results) argues for it on estimator grounds — bounded influence
     rather than deleted evidence — and this is the second and larger reason
     to keep it.
  4. **It gives the per-shape caution its mechanism.** [The per-shape
     table][pershape] says to trust the first digit only; a scheduling lottery
     moving one cell by a third is why, where a geomean over 24 shapes cannot
     move like that.

  **And a fourth instrument died on contact, which is worth a sentence because
  it is the obvious one.** If the mechanism is allocation history, pinning
  criterion's iteration count should pin the history and make cells reproduce;
  but `-n/--iters` is *Run benchmarks, don't analyse*, and a run under it writes
  no JSON at all — measured, not read off the help text. There is no other way
  to fix the schedule from the command line, so the mechanism cannot be tested
  by pinning it, and it is recorded here dead rather than left
  to be re-proposed. What `-n` *is* for is the next paragraph.

  **The block-pool issue this project filed is the nearest precedent,
  and its methods are the ones to reach for next** —
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
  shrinking the interval *around the wrong value*, and — the part that matches
  the lottery — an effect that in rare runs does not reproduce and whose
  magnitude differs randomly from run to run.

  **So the instrument that report used is the one this question wants**:
  `perf stat` over runs with a fixed iteration count, read per iteration.
  Its table is the model — task-clock, instructions, dTLB-load-misses,
  cache-misses, page faults, clock — and it identified last-level cache misses
  by finding instructions equal to 0.9994, clock equal, GC and allocation equal,
  and cache-misses 2.86 times. Three of those rows are already known here
  and agree: the clock is fixed, allocation is identical to the byte, GC
  is flat. **The missing row is the cache misses, and only `perf` can supply
  it** — paired with `-n`, whose fixed iteration count and absence of analysis
  is exactly what that method wants, which is what `-n` is for and why
  its retraction above is about JSON alone. `+RTS -H2G` is the control the same
  report validates: a pool taken in one contiguous piece removed the cost there,
  so a wild cell surviving `-H2G` is not pool structure.

  **`perf` needs `kernel.perf_event_paranoid` lowered from this machine's 4
  before it counts anything** — at 4 it reports `cpu-cycles:u <not supported>` —
  and that is a `sudo sysctl -w` in a plain terminal, not something a session
  can do.

  **Run 2026-08-12, and the cell does not reproduce filtered, as expected.**
  Differencing `-n 40000` against `-n 20000` on `run12-maxskip`, which removes
  the process's fixed cost exactly rather than diluting it — at `-n 200` startup
  was 45% of task-clock and the counters said nothing —
  `lenet-L1-28-c1-k5/bq-expand` and its adjacent twin come out at **54.10
  against 53.95 µs an iteration, 866206 against 866252 instructions, 1102.6
  against 1106.4 cache misses, 19.9 against 21.0 dTLB misses**. Everything
  inside a third of a percent but the dTLB, which is 5% on a base of twenty.
  A filtered process has no allocation history and a clean pool, so there
  was nothing for the effect to arise from; the null is consistent
  with the surviving account rather than against it. Three things it does buy:
  the **instructions agree to 5e-5**, which is the first instruction-level proof
  that an A/A pair is the same work and the control row that must stay flat when
  the effect does reproduce; a per-call counter baseline for that bench
  to compare a wild cell against; and **criterion's slope confirmed
  by an instrument sharing no code with it**, 54.10 µs against the 53.46
  that half published, 1.2% apart. Seconds, and no quiet machine: counter ratios
  between two arms do not move because something else is running, where
  a wall-clock figure would.

  **The mechanism itself is tested by logging what it names**, per bench:
  the RTS's allocated-bytes total and the payload addresses. That is a `Main.hs`
  edit and belongs **after the current pair is spent**, since it changes
  the module's code, so its `.text`, so every loop offset, and would invalidate
  the md5s that pair's note records for binaries already built. **What
  it no longer waits on is a wild cell, 2026-08-14.** The `scaled` A/A slot
  shares this signature — one arm, one process, identical work, the difference
  in mutator time and the state kept once entered — and turns up in six runs
  of seven, where a wild cell is a lottery; so the mechanism can be instrumented
  there on demand, and a wild cell only decides whether the large instance
  is caught too. The two differ in where the state is entered, mid-bench there
  and before the bench here, which is why **the logging is per sample
  and not per bench**. And addresses are the right thing to log for a reason
  the decomposition supplies: allocation is identical to the byte in both
  instances, so the cost is per access rather than per allocation.
- `PARKED` **`mut-odo`'s wide interval on `micro-aligned` is, at sample level,
  the `build`/`mut-odo` pair scattering together — a measurement without
  a mechanism.** The interval reproduces and belongs to that binary: CI% 1.06,
  1.09 and 1.15 in three independent processes on it — Run 10's main set
  and both gate passes — against 0.72 and 0.19 on `micro-maxskip` (2026-08-11,
  arithmetic over the run and gate artifacts, no machine time). The CI% column
  reads it as one arm's, `build`'s interval moving only 0.30 to 0.39 —
  an artefact of the interval, which is sampling error about a fitted line
  and not stability: taking each cell's residual about its own line, per
  iteration, as a fraction of that cell's slope and medianing over shapes,
  `mut-odo` scatters **21.9%** on the aligned half and `build` **32.7%**,
  against `mut-odo-vecdims`'s 3.1% and `list`'s 3.2% — an order of magnitude,
  `build` the worse of the two where its *interval* is much the narrower (CI%
  0.44 against 0.82) — and both roughly halve on the max-skip half, 11.1%
  and 22.8%, where `list` and the vecdims arms barely move (2026-08-12,
  arithmetic over Run 11's two main sets). The same pair, behaving together,
  on the same two binaries as [the 3% that survives alignment][open]; kept
  because the two instruments will disagree again, and the scatter is the one
  to believe.

  Three accounts are closed at sample level, the refit reproducing criterion's
  slope to 1e-15 first: the residual correlates with `measNumGcs`
  and `measGcWallSeconds` at ±0.00 in every process, so it is not the block
  pool; with sample index at ±0.03, so it is not drift the slope missed;
  and allocation per iteration is constant. Nor is it shape-localised, two
  passes of one binary sharing no widest shape. What is left is dispersion about
  the line that no recorded covariate explains, on one arm, on one binary —
  and thinner than the three readings suggest, per-cell dispersion swinging
  several-fold between passes and the comparison binary's own median moving 3.7×
  between its two.

  **Run 11 reproduced it a fourth time and turned it into a different
  question.** The same arm at the same slot in the same binary reads CI%
  **0.82**, against 0.31 on `micro-maxskip` — so the split between the binaries
  survives, at three quarters of Run 10's separation. What is new
  is that `mut-odo` is also **the arm that drifts most across the repetition**,
  1.0327 where every other arm bar its own code twin is inside 1.5%, with cells
  at 1.1577 and 1.1467; `build` is second at 1.0095 with a 1.2471 cell. Two arms
  sharing one worker, at offset 0 in both runs, moving together and moving more
  than the roster: the wide interval and the wide drift are one arm's,
  and placement can no longer be either's account. What would separate
  a dispersion belonging to the *worker* from one belonging to the *slot*
  is a run with the two arms' roster positions exchanged — which asks
  for an aligned build, a form this page has moved past ([the tasks' closing
  ruling](#recommended-tasks-after-run-14)).
- `OPEN` **A second instrument says different arms are unstable, and the two
  disagree — which is the finding rather than something to average.** The entry
  above prices instability by the `CI%` column, which is sampling error *within*
  one benchmark. A pair's two halves supply another: each arm's spread
  of per-shape ratios between them, as the standard deviation of their logs,
  which prices disagreement *between* processes. Run 13 raised it and it
  is not that run's alone. **Measured on the three pairs whose two main sets
  are both on disk** — Run 11 aligned against max-skip, Run 12 max-skip against
  `+procalign`, Run 13 max-skip against `lookrts` — `offtab` ranks 3rd, 2nd
  and 1st, `build` 2nd, 3rd and 3rd, and `offtab`, `build`, `gen-unsafe`
  and `bq-gen` sit in the widest six of all three. So it is a stable property
  of the arms and not an accident of one pair. **It is not sampling error**:
  against `CI%` it correlates at r +0.69, and `list` refutes the account
  outright, having the fewest samples of any arm and a *higher* `CI%`
  than `offtab`, `mut-odo` or `build` while its spread is a third of theirs.
  These arms are measured precisely inside a process and disagree wildly between
  them. **And the two instruments name different arms**, which is why this
  is an entry: `offtab`'s interval is an unremarkable 0.74 in both halves,
  so the interval reads it as an arm that does not follow the phenomenon — true
  of the interval, and false of the spread, where it is the worst arm
  in the roster in all three pairs. That account is built
  on the `build`/`mut-odo` code twin; the phenomenon is wider than the twin
  and its most consistent member is not a code twin at all. **Two things would
  settle it, and only the second wants a machine.** Correlating the per-shape
  spread against `sInner`, `l`, `m` and rank, and asking what those four arms
  share — they are not a tier, `offtab` carrying mutable `Int` scratch, `build`
  a class-method fill and the other two pure, so a negative answer
  is informative — is arithmetic over kept artifacts. Separating position
  from code for them wants a *twin* on one of them, which no run has had:
  through Run 13 the A/A gate covered three of the twenty-four timed strategies
  and none of these — the same coverage gap the wild-cell entry above names
  from the other side. **The roster change is made, 2026-08-14**: `offtab`,
  the ranking's most consistent member, carries twins in both positions, so Run
  14 reads its position against its code directly. The three-pair reading
  is possible only while those runs' main sets are kept. **What it is measuring,
  asked over all three pairs and answered in part** (2026-08-14, arithmetic
  over the six kept main sets). Ranking arms by the stdev of their per-shape
  cross-half log ratios reproduces this entry's order at the top — `offtab`
  7.6%, `mut-odo` 6.9%, `build` 6.9%, `gen-unsafe` 6.5% — with `gen-quotrem`
  at 5.8% taking the fifth place recorded for `bq-gen`, which reads 4.7%
  and sixth. **They are not a speed tier**: the wide arms span 2.4 to 17.0 ns
  an element, and the two narrowest arms on the page are its fastest
  and its slowest, `mut-odo-vecdims` at 1.2% and `list` at 2.0%. What three
  of the four share is a shape law the `CI%` instrument has no counterpart for —
  disagreement grows as the runs shorten and the rank rises, the Spearman
  of |log ratio| against `sInner` reading −0.64 on `build`, −0.58 on `offtab`
  and −0.55 on `bq-gen`, against rank +0.51, +0.11 and +0.34 — so what is being
  priced is the placement of the per-run work rather than of the per-element
  work. `gen-unsafe` is flat against every dimension and is therefore wide
  for some other reason, which is the negative answer this entry asked to have
  either way.
- `ANSWERED` **What the eight stride classes are worth as instruments — read
  against each other for the first time on 2026-08-14, over Runs 10 to 13,
  and four things came of it.** Per class: the median A/A deviation runs 0.08%
  (`slice`, `window`) to 0.34% (`scaled`); the worst cell 3.80% (`revsome`)
  to **11.59%** (`scaled`, its standing slot); the median `CI%` 0.05
  to **0.33**, `bcast` alone five times the field and its shapes the ones
  the excess-allocation predictor says cross the nursery; and the correction's
  amplification 1.30× (`reshape1`) to 1.81× (`scaled`), so one class makes
  the same raw wobble read half again worse than another does. **The finding
  is not a class property at all**: in every one of the eight the *distant* twin
  is the slower half, +0.09% to +0.65%, where adjacent twins sit within ±0.2%
  of zero. One-directional across eight classes and four runs is not scatter.
  **And its cause is a confound in the crossed design** — every distant twin sat
  in the group's first dozen slots with its base later, so *distant* has always
  also meant *earlier*, and a residual cold start is exactly what produces
  that sign. Four changes followed, all the same day. `gen-unsafe`'s distant
  twin moved to the group's tail, where it had landed two slots from its base
  and spanned nothing; with `list`'s distant half late by construction, the next
  run reads early-distant against late-distant and can say which of the two
  the bias was. **Every class took a third shape**, two being too few
  for the winsorizing that protects the main set, so a single disturbed cell
  owned a class geomean — and each new shape is that class's own extreme rather
  than another size: `bcastmid-b200k` takes the stretch factor to the size cap,
  `reshape1-rank10` the odometer to rank 11 at one run per element,
  `slice-coprime-r7` the rank to 7 under a slice, `window-64x64-k1x9` the kernel
  to 1 by 9 for an innermost extent of 1, and `scaled-r5` scatters 15015 outputs
  over 42735 source elements. `--block` now prints the largest pair's **raw**
  ratio and its amplification beside the net, which `--aa` always had
  and the eight blocks a run never did; and it prints a **steps** line, `rev`
  and `slice` carrying the most mid-bench steps of any class. What stays open
  is `bcast`'s `CI%`, which Run 14's `-A1G` half now reads directly, every class
  running on both halves. **Each new shape was checked to belong to its class
  and not merely to compile**, which `check` cannot say — it holds an arm
  to the reference on whatever view it is given, so a shape in the wrong list
  would pass it. Read off `check`'s own printed view, strides and offset, all 24
  class shapes satisfy their class's defining property: every stride negative
  under `rev`, mixed signs under `revsome`, a zero stride innermost
  under `bcast` and in the middle under `bcastmid`, an appended size-1 dim
  under `reshape1`, a positive offset under `slice`, the repeated window strides
  under `window`, and superincreasing strides none of them 1 under `scaled` —
  with all 50 checked shapes at regime 3 and none disagreeing. The predicates
  discriminate rather than passing everything, which is what makes that worth
  quoting: the only foreign match is the three `reshape1` shapes satisfying
  `bcast`'s test, and that is the code saying so, `mkReshape1` being
  `mkBroadcast` of the shape with a 1 appended.
- `OPEN` **`scaled`'s A/A slot is real and its size is not: six runs of seven
  find a disturbance at the `mut-odo-vecdims` slot on `scaled-super-r3`,
  its magnitude never repeats, and the ruling is to quote the slot as a hazard
  of the class and never as a figure.** What stays open is the raw disagreement
  under it, which had no account until the sample-level reading at the end
  of this entry. The account below is Run 10's, where the arithmetic half
  was derived; the runs since are at its foot. On Run 10 both `mut-odo-vecdims`
  pairs read below 1, 0.9464 and 0.9574, both worst on `scaled-super-r3`, while
  the other four pairs in that process sat within 0.25% — and it was the base
  arm that was slow, not the twins. **Two thirds of it is arithmetic
  and was mine to divide out before calling it a disturbance.** The raw slopes
  disagree by 2.13%; the forcing term is 59.8% of this bench, the largest share
  in the run; and 1/(1-f) turns the first into a predicted 5.29% against
  the 5.36% read. So the arm's cells are 2% apart, not the 11% the published
  pair suggests. The raw sample lists say nothing further is wrong: R2
  is 0.99995 or better on all four arms and there is no ramp the slope has
  not already handled. What survives is a 2.13% raw disagreement at one slot
  on one shape, against 0.17% raw or less for the four other pairs in the same
  process — smaller than it looked and still this slot's. It also inverts Run
  9's wild cell, where the *twin* was slow and roster warmth was the account:
  the distant twin here is the earliest of the three and is the clean one,
  so that story does not transfer. **Do not reach for a filtered re-run
  of the six controls**: filtering collapses the spans the crossed design needs,
  which [the floor section][floor] records as making a span unmeasurable. What
  can be asked is Run 11 reading this population with layout pinned. **Read
  at sample level on Run 13, and it is neither a ramp nor an outlier
  but a step** (2026-08-14, `run13-maxskip-scaled.json`, the refit reproducing
  criterion's slope to 2e-16 first). The disturbed arm runs at its base's speed
  — 58.106 against 58.06 µs an iteration — for 69 of its 89 post-ramp samples,
  then steps once to 60.700 and stays there, **+4.46%**, 1.69 s into a 4.72 s
  bench. Across that step allocation per iteration is identical to the byte
  at 480561, GC count per iteration is identical at 0.111, and the peak heap
  does not move from 28 MB; what carries the cost is mutator time, 60.4 against
  57.8 µs. The other five A/A pairs in that same process read within 0.25%.
  The signature repeats where the artifacts survive: the twin's last quartile
  jumps on Run 11 (58.27, 58.41, 57.23, **61.44**) and on Run 13 (58.03, 58.17,
  58.11, **62.03**), Run 12 is a mild 1.7%, and **Run 10 carries it on the base
  arm instead** — 57.38 rising to 60.37 with the twin flat — which is why
  the ratio moves in either direction and why the magnitude never repeats.
  A state the process enters once and keeps is the block-pool report's signature
  rather than a scheduling lottery's, so **the mechanism entry's logging wants
  to be per sample and not per bench**: a per-bench figure averages the two
  states it exists to separate.

  **It has, and the answer is that the slot is real and its size is not.** Run
  11 reads this class's floor at **3.27%** — still the run's worst, still
  the `mut-odo-vecdims` slot, still worst on `scaled-super-r3`, so four runs
  of five have found a disturbance at one slot on one shape and a pinned layout
  does not remove it. What did not survive is everything about its magnitude:
  the pair that carries it swapped, the *distant* one reading 1.0327 where
  the adjacent one is clean at 1.0020, and the sign inverted, both having read
  *below* 1 in Run 10. The arithmetic half reproduced exactly — raw 1.25% at `f`
  0.609, so 1/(1-f) predicts 1.0320 against the 1.0327 published — which
  is the account above holding while the quantity it explains moves by two
  points between two runs of one binary. So quote this slot as a hazard
  of the class and never as a figure, and treat a margin under about 3% here
  as unmeasured. **Two more runs have since found it, and the ruling
  is unchanged.** Run 12 read the same distant pair at 1.0151 on a worst cell
  of 3.74%, and Run 13 at **1.0547** on a worst cell of **11.59%** — the largest
  recorded there and the worst A/A cell anywhere in that run. So six runs
  of seven have found a disturbance at this one slot on this one shape, Run 9
  the only exception, and the arithmetic half reproduces a third time: raw
  1.0212 at `f` 0.608, so `1 + raw/(1-f)` predicts 1.0540 against the 1.0547
  read. What goes on moving is the magnitude alone — 5.36%, 3.27%, 1.51%, 5.47%
  across Runs 10 to 13, each the class's floor and not its worst cell — which
  is exactly what this entry already says and is why the ruling needs
  no revision: the slot is real, its size is not, and the amplification
  is arithmetic rather than a second effect.
- `OPEN` **What does the roster owe the next run?** The exact repetition
  is **taken** and is not owed again for its own sake: Run 11 inherited shapes,
  roster, order, regime and binary, and what it bought is [in the floor
  section][floor] — a drift band a quarter of the one this page had
  been quoting, and every claim reproducing on it. What the roster owed
  is the third `-nosum` arm the queue holds, deferred out of Run 11 so
  that its membership stayed pinned and out of Run 12 so that it did not arrive
  in the same run as a change of shim. **It is now written**,
  as `mut-flat-gm-nosum`: a `Force` pair on the flat fill, the third shape
  of fill after the odometer and the expansion, which is what lets gate 3 tell
  a biased read from two biased arms. It sits beside its base, as both other
  `Force` pairs do, so its difference is taken between neighbours. **Both debts
  are now paid, on 2026-08-13.** The membership-invariance check Run 12's basis
  choice made due — max-skip pads only the heads that need it, so an arm's
  arrival is not guaranteed to leave every loop where it was — comes back clean:
  rebuilding the basis recipe with the arm leaves **every tracked loop
  at the same address**, fills `[11, 0, 4, 0]` and `[24, 8, 0, 0]` either side,
  32 self-loops in 25 distinct byte-sequences both times, and the roster grows
  by exactly the 24 cells the arm adds, 816 to 840. **Read that as the weak form
  it is**, though: a `Force` arm reuses a function the roster already
  references, so it emits no new code and emission order has nothing to reorder
  — an addition that brought a *new function* would be the stronger test,
  and is what a later membership change should be read against. **Both fell due
  again for Run 14 and are PAID: the roster gained twelve A/A twins
  on 2026-08-14** — `offtab` and `bq-odo-gm-mulback` first, then `build`,
  `mut-odo`, `list` and `gen-unsafe`, each in both positions, 840 benches
  to 1128 — so that run owes the `-L1` pass and the invariance read, still
  the weak form, a twin reusing a rostered function and emitting no code. **Both
  were taken before the evening and both came back clean**, the `-L1` pass twice
  — the first on a roster that five class shapes and a moved twin then replaced,
  which is the trap that line exists to catch — and the invariance read holding
  every tracked loop at its address across both. What the twelve twins then did
  to the run is not a debt but a finding: they took the A/A population from six
  pairs to eighteen and the floor from a fraction of a percent to 2.19%, because
  the new ones sit on the widest-spread arms. A floor is a property of the arms
  it is measured over, and this is the run that made that visible.
  **The invariance read was taken on the 936-bench tree, 2026-08-14, and came
  back clean**: rebuilt from it, both recipes held every tracked loop where Run
  13's binaries have it — fills `[11, 0, 4, 0]` and `[24, 8, 0, 0]`, at the same
  addresses, on the `lookrts` recipe Run 14 makes its basis and on the max-skip
  one beside it, whose `.text` also came out at 20377797, the size that pair
  note records. **Taken again on the final roster, 2026-08-14, and clean there
  too**: the same build holds those loops at those addresses with `.text`
  to the byte, five class shapes and a moved twin later, which is what a shape
  being data and a twin reusing a rostered function predict. **The `-L1` pass
  was taken twice for the same reason** — the first covered a roster that five
  class shapes and a moved twin then replaced, which is the trap that line
  exists to catch, a pass recorded for a roster that no longer exists.
  The second covers the main set and the `scaled` class, chosen because
  it is one of the five that crossed from two shapes to three, so `--block`'s
  three-shape branch is exercised for the first time; every reader mode exits 0
  on both files, which is what that pass is for. It also settled the one slot
  claim this roster change made on an argument rather than a measurement:
  `list-aa-adjacent`, the single entry inserted above the distant twins,
  allocates 134261336 bytes a call against `list`'s 134261403, agreeing
  to 1.1e-4 over all 24 shapes, where `sum-only-early` — the bench the slot rule
  is about — allocates 204 bytes a call, its allocation being a one-off setup
  vector. So the twin fills as its base does and grows no pool the way
  that bench does. Its readings are with the pair note, and its timings go
  nowhere, `-L1` being a rougher budget than any recorded run's. The arm's own
  reading is [with gate 3](#what-is-open), taken filtered; Run 13 took
  it at full budget, and its Results row's `needs` cell reads *the same,
  on a third write pattern* — the control convention, not the shippability
  phrase this entry first proposed. **A return to -O1 stood behind it
  as the second debt and is retired, its premise being false** (2026-08-14): -O1
  is not the regime this fallback ships in, `-fspec-constr` being set
  in the file the fix is added to, so the basis every run since Run 8 has used
  is already the shipped regime and Run 7's claim set is history rather
  than a debt. The build specification that entry had accumulated goes with it,
  a retired run having no use for one. An -O1 reading of a single ordering stays
  available as a filtered probe, as the 2026-08-08 twin probes were; what
  is retired is the evening. `--check-doc` enforces the yardstick's shape
  in the one direction it safely can: a run named aligned must also be named
  unaligned, so dropping Run 10's unaligned column fails the check. Dropping
  an *aligned* one cannot be checked, an unpaired run being what every column
  before Run 10 is, and stays the reading's job.

  **Run 11 had no unaligned half, and the check was left alone rather
  than widened — the reading is that this was right.** Its two columns
  are `Run 11 (SpecConstr, aligned)` and `Run 11 (SpecConstr, max-skip)`,
  and `--check-doc` passes on them, the rule asking that a paired run publish
  a column per half and not one. Widening it was the alternative and is refused:
  the check would then have to know which half names count as a counterpart,
  which is a list that grows with every pair and is wrong the first time one
  is invented. Keep a basis column named `aligned`; name the other half
  for its shim.
- `OPEN` **At a large nursery an earlier bench in the same process permanently
  slows a later one, and it is not the block-pool issue.** Run 14's probes,
  2026-08-15/16. `vgg-14-c512-k3/list` reads 14.1 ms alone and 22.3 ms once
  certain shapes have run before it, saturating rather than accumulating; six
  of the 23 shapes do it and one of them alone is the whole effect,
  so the reproducer is two benches in one process. At `-A4m` the same ladder
  is flat, so the nursery gates the cost — but not the disturbance: the victim's
  LLC misses per instruction rise by about the same absolute amount at both
  settings (+1.33 and +1.41 per 1000), while IPC falls 21.5% at `-A1G` and 4.4%
  at `-A4m`. The reading, unmeasured, is that the added misses overlap
  into collector stalls at 4 MB, where the process spends 4.9 s in GC and copies
  10.3 GB, and are exposed at 1 GB, where GC is abolished (0.056 s, 2.8 MB)
  and the victim's time is mutator time at a very low baseline miss rate.
  **It is not the pinned-spray pool condition of GHC work item 27601**,
  and that is a controlled result rather than a comparison of write-ups: on one
  machine and one compiler `+RTS -H2G` removes that reproducer's penalty
  and leaves this one at 56%, `max_mem_in_use_bytes` moves 2.7% here against
  a doubling there, and `-A4m` costs nothing here against 6.3% there.
  **The conceptual objection is sharper than those three and needs no control
  at all**: that condition forms only because rare collections let block groups
  accumulate, so at a small nursery it should not form and there should
  be nothing to absorb — where here the disturbance is full size at 4 MB
  and merely goes unpaid. Both accounts turn on the same premise, that a small
  nursery collects often, and one concludes it prevents the condition where
  the other has it hiding the cost; that is what makes them rival rather
  than compatible. Everything reproduces on GHC HEAD 10.1.20260803 — the same
  six shapes in the same order, dTLB flat, IPC −21.5% on both compilers —
  and that issue is itself unfixed in HEAD. **What is not known is which
  property of those six shapes does it**: `conv1d-24` and `cnn-L1-24x24-c1`
  share `l` and `sInner` and land on opposite sides, on both compilers, so
  it is structural and not volume. What would settle it is the allocation size
  classes each shape's setup produces, read against the 3276-byte large-object
  threshold; until then this is not filable, wanting a mechanism
  and a reproducer that is not a `micro` invocation. **It does not touch
  the published tables**, which are the basis half's and so default-nursery,
  where position is free; what it does touch is any absolute quoted
  from the `-A1G` half, and the arm-by-arm comparison, whose position term sits
  on one side only.
- `OPEN` **What Run 15 is built to answer, registered before it runs.** Its pair
  is Run 14's with `-A32m` in place of `-A1G` on the control half and nothing
  else changed, on Run 14's roster ([what it compares
  against](#what-run-15-compares-against)). Two registrations, each with what
  would break it.
  1. *Is the position term visible at 32 MB?* **The registration is
     that it persists**, the entry above having it gated by the nursery at 1 GB
     and flat at 4 MB with the disturbance full size at both. So the reading
     is its size at a nursery eight times the default, and a control half
     showing no ladder at all is the finding rather than the prediction — a null
     that would also make the two halves' absolutes subtractable, which
     the `-A1G` pair's are not. Read it the way Run 14 read it: the same six
     shapes, one of which alone reproduces it, and the victim
     `vgg-14-c512-k3/list` alone against after.
  2. *Does a repetition land inside the drift band?* Both halves run the roster
     Run 14 ran, so every arm on the **basis** half should sit within
     the measured band — at most 3.3% and most under 1.5% — against Run 14's
     basis. An arm outside it is not a strategy finding: the code is identical,
     so it is the machine, the build or the instrument, and it is what
     the repetition is for. This is the reading Run 11 bought once
     and the roster has since spent.

  **And one expectation that is not a measurement**, registered so that
  it is judged rather than remembered: Run 15 is the first run whose claim
  readings are installed rather than transcribed, so the write-up should copy
  no claim figure by hand at all, and `--claims` should leave nothing
  unattributed after the install. A figure that has to be typed is a gap
  in the installer, and belongs in the [non-urgent list](#non-urgent-todo-list)
  as one.


### Recommended tasks after Run 14

**Seven tasks left this heading on 2026-08-14, taken; one is gated and stays.**
The NOPs, the `scaled` slot's raw samples, the `-g3` twin's copy count,
the `bq-expand-b` pooling, the registering, the alignment gain's shape structure
and the between-process spread were all worked down that day over kept artifacts
and two compiles, and each verdict is in the entry above that owns its question
— a taken task leaves this heading rather than being indexed here beside
the entry that is its authority. Nothing left here wants a quiet machine;
the one evening this page still wants is Run 14's.

1. **The wild cell's mechanism — still gated, and the gate has not lifted.**
   Logging the RTS's allocated-bytes total and the payload addresses
   is a `Main.hs` edit and Run 14's pair is the next thing built, so the logging
   would have to ride both halves or neither: it waits for that pair to be spent
   as it waited for this one. Its `perf` half still wants
   `kernel.perf_event_paranoid` lowered by hand. **What it no longer wants
   is the lottery**: the `scaled` slot shares the wild cell's signature
   and turns up six runs of seven, so the mechanism is instrumentable there
   on demand — and the logging goes per sample rather than per bench, a step
   inside one bench being averaged away by a per-bench figure. Both readings
   are with the wild-cell entry.

**One rider rather than a task of its own, since it fires on an event and
not on a session.** The pinning claim — that a shim'd build holds every tracked
loop at one address across a roster change — is measured only in its weak form:
adding `mut-flat-gm-nosum` left every tracked loop where it was, but a `Force`
arm reuses a rostered function and emits no code of its own, so emission order
had nothing to move. **The next roster addition that brings a new function
is the stronger test, and is to be taken as one** — read the fills on one build
either side of it, before anything else changes — which costs nothing
at the moment the arm lands and cannot be taken afterwards. Until then the claim
covers additions that cost nothing to place, and should be quoted that way.

**And one class not to repropose: work that needs an aligned build.**
`mut-odo`'s wide interval is the live case. The dispersion is documented
as belonging to `micro-aligned` — 1.06, 1.09 and 1.15 there against 0.72
and 0.19 on `micro-maxskip`, and 0.82 against 0.31 on Run 11 — and the swap
that would separate a dispersion belonging to the *worker* from one belonging
to the *slot* is enabled by an aligned build making it a membership-free edit.
No run since Run 11 has had one: the basis has been max-skip since Run 12, which
priced `-fproc-alignment=64` and saw the flag lose; the script that built
unaligned/aligned pairs was deleted on 2026-08-14; and Run 13 showed a two-shim
pair can hold every tracked loop at one offset in **both** halves, which
is the property alignment was wanted for. So the swap asks for a build form
this page has moved past, and on a max-skip basis there is little dispersion
left to attribute — the interval it is about is the aligned binary's.


### Non-urgent TODO list

- `STANDING` **A class process's provenance line counts every class view,
  not the population that ran.** The count is fixed before criterion does
  the selecting, so each class process reports the whole class set's size beside
  its own elapsed time and heap peaks, both of which are its own. The page takes
  the population from the reader instead, and that costs nothing at all now:
  `--block` emits the clause and `install-tables.sh` installs the paragraph
  it sits in. The fix in `Main.hs` stays refused — `provenance` would have
  to parse a criterion argument it passes through untouched, a second source
  of truth for criterion's matching rules, wrong the moment a run reaches
  for `-m glob` — and refusing it is what states the rule the installers go by:
  **install from the tool that already knows the value, never from one
  that would have to re-derive another's logic.**
- `ANSWERED` **Runs never overlap in the benchmarked set.** `mkStrided`'s index
  map is a bijection onto `[0, l)`, where im2col patches — the workload
  this page opens by naming — overlap heavily and so reuse cache. The window
  class (`mkWindow`) builds exactly those overlapping patch views, and both
  recorded runs agree: the overlap *lifts* every ratio rather than lowering it,
  so the main set's pessimism about this case was about absolute cost, never
  about the fallback's standing against `list`. The window block in [The stride
  classes, run by run](#the-stride-classes-run-by-run) carries the figures.
- `ANSWERED` **The roster order biases the table, and nothing corrects for it.**
  The warm-up drift above means a strategy's figure depends on its slot, `list`
  being in the coldest one. The fixes are all real changes rather than write-ups
  — a warm-up bench before `list`, interleaving or randomising the order,
  or correcting each row by its slot — and each breaks comparability with every
  run so far, which is why none was taken for eight runs. Run 7 confirmed
  the drift, Run 8 mostly did not, and Run 9 shows why both readings were
  of the wrong quantity ([the floor section][floor]): the effect is
  not a per-slot gradient to fit but a step, worth nothing on most arms
  and 35–40% on one family at one shape. **So a slot correction is now refuted
  rather than merely unmeasured** — a linear fit in slot number cannot express
  a step that depends on the arm, and fitting one would smear a real 40% across
  thirty rows that do not have it. What the drift needed instead was the warm-up
  bench, the only one of the three fixes Run 9 left standing, and **Run 10 takes
  it**: `sum-only-early` above `list`, so the baseline is measured on a grown
  pool like everything else, at the cost of re-basing every published ratio —
  which is what the entry above says none of these fixes could avoid. What
  it does not address is the placement gap the `build`/`mut-odo` pair shows,
  a separate and larger target that no reordering reaches.
- `OPEN` **No build-vs-output time decomposition**, which Run 8 wanted and did
  without. `diag` measures per-builder *allocation* only, so a claim like
  "the table build is a third of the cost" — the natural reading
  of `bq-mut-runs` beating `bq-mut` by 39% — cannot be checked here. Claim 4
  no longer needs it — a Core diff identified what the flag deletes
  from the scan builder and the ~4% it is worth accounts for where the pair
  lands, the two arms sharing their output code exactly — but the residue does:
  how much of each arm's own ~25% absolute gain is build and how much output
  is still unmeasured, and the same question stands for every other arm
  in the table. It needs a timing mode alongside `diag`'s allocation one, using
  the fixed-iteration differencing the horde-ad performance model prescribes
  (`-n 200` minus `-n 100`, fresh processes) rather than criterion, since
  the builders are not benchmarks.
- `OPEN` **Change the method and a family of prose is deleted rather
  than maintained — the lever the two speculative regimes here share,
  and the one no tooling reaches.** The controls, the pairing, the shim
  and the floor exist because wall-clock on this machine is layout-
  and history-dependent, and the write-up pays for that defence every run:
  the floor, the drift band, the pinning caveats, the restatement on the basis
  half, the basis matching owed before any figure is quoted. Numbers needing
  no such defence delete those paragraphs; an installer only makes one cheaper
  to write. Both candidates were written 2026-08-14 from a review
  of the apparatus rather than from any run, and each names the pilot that would
  settle it. **Counted work instead of sampled time, wherever the question
  is an ordering.** Counted work is layout-independent — the wild-cell probe
  read an A/A pair's instructions agreeing to 5e-5 — so a cachegrind
  or fixed-`-n` counter table would want no quiet machine and no floor and would
  reproduce on any box, the clock staying for the boundaries where
  a memory-system effect can invert an ordering. Pilot: counts for every timed
  arm over the shape set, read against a published time column — orderings
  that agree license the switch, and the cells that disagree
  are the memory-bound residue the clock is still for. **Randomised slots
  in per-trial processes instead of pinned ones.** Many short fixed-`-n` trials
  per cell, each in its own process with the order drawn fresh, so that position
  becomes noise that averages rather than bias that persists, and a table stops
  needing comparability carried between runs, being self-contained evidence.
  Not the reordering the roster-order entry above rejected — that varied slots
  inside the one shared process — but a regime that gives the shared process up.
  Pilot: a few arms and shapes read against the published column, with the A/A
  pairs' spread under randomisation as the method's own floor.
- `OPEN` **Render the run-scoped prose from a ledger — speculative likewise.**
  The end state is verdicts, statuses, floors and tallies kept in one small
  machine-readable file beside the roster, `read-run.py` rendering them
  into this page as `--in-place` renders the tables, so that everything rendered
  cannot go stale and the checker fleet stops growing a check per defect class.
  The mechanism is not in doubt; the cost is a rewrite of the write-up
  procedure. **Its pilot was the claims verdicts and it is taken** (2026-08-16),
  which leaves the question the pilot cannot answer: whether one ledger file
  beats an installer per section. Do not design it before the installers say
  what it would hold — three of them now do, and the fourth thing a run still
  writes by hand, the cross-class summary's emphasis, is exactly what a ledger
  would have to carry and no reader can derive.

- **The rename, done rather than checked.** Post-run step 5 is mechanical — four
  run-numbered headings, two taking this run's number and two the next, every
  link's text and anchor repointed, and `Main.hs`'s `README.md#` references
  with them — and `--check-doc` now fails a link whose text and anchor name
  different runs. A mode that performs the bump would leave nothing to catch;
  it writes the page, so it wants `--in-place`'s refusals, which is why
  it is registered rather than written.
- **More checks of the floor-consistency shape: one figure, several sites, must
  agree.** The floor pair, the roster size and every population size quoted
  as `over N shapes` are checked (the last two against Main.hs, 2026-08-16,
  since agreement alone cannot see a count that is stale everywhere). What
  is left of the four subjects Run 14 got wrong is the run window
  and the process count, neither of which has a phrasing crisp enough to match
  yet: the pattern has to distinguish a population's size from a win count,
  which is what `on N shapes` taught.
- **`--claims --compare PREV.json`, if the movement sentence turns out to
  be the last transcription.** The kept JSONs make *held, and moved from 0.9909
  to 0.9940* mechanical — `pair_stats` over both files — and it is the one thing
  a claim's paragraph still copies by hand. Not taken, because it renders
  the reading rather than the arithmetic, and the division the installed
  readings keep is that the author owns whether a movement means anything.


## The goal of these benchmarks

**Nothing in this chapter changes from run to run.** It changes when the harness
changes radically, or when a ruling here is refuted — and a ruling refuted
is a paragraph rewritten, not a figure updated. What it holds is why
these shapes and not others, why these strategies and not others, which designs
were tried and died, and what all of it was for: [the fix
in `Data/Array/Internal.hs`](#the-fix-in-dataarrayinternalhs), which is the goal
the rest of this file exists to have reached. Figures do appear here, inside
rulings that rest on them, and those are re-quoted when a run moves them;
the *rulings* are not re-verified each run.

Those rulings are architecture decision records in all but format — context,
decision, consequence, and an evidence trail that makes them re-openable rather
than merely re-readable. The prose form is kept deliberately, since the evidence
is the point and a template tends to shed it. What the resemblance is worth
is a warning about growth: if the rulings outgrow the chapter, the ADR answer
is one record per file with an explicit *status* — and the thing to carry
over would be that field, since what this page keeps getting wrong
is not stating a ruling but noticing when a later measurement has superseded
one.


### How the strictly positive picture was achieved

Four findings turned the mixed picture into `bq-expand`. **Price the outer
multi-index once per run, not once per element**: an `m`-element base-offsets
table (`m = product (init sh)`) drops the output to one `quotRem` per element,
where the first attempt paid one per *dimension* per element, which
was the whole cost on the small high-rank shapes. **Then the table build is what
remains, and it is a separable grid**, so `concatMap`/`enumFromStepN` builds
it with no division and no lazy cons-list — a `foldl'`-over-a-`build`-list does
not fuse away, and that is `bq-expand`'s edge over `offsets-quot`. **Strictness
bangs on the hot loop are performance-essential**, worth ~2× on their own,
and are carried into `Data/Array/Internal.hs` with the logic.

**While this was achieved, the harness had to be hardened** — criterion `env`
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
which enter only the later dot), so the patch tensor is `[nImgs, nAh, nAw]` ×
`[nCinp, nKh, nKw]`.

In general the source's transposes merge into that view, so its innermost
dimension is strided and normalizing it takes regime 3 — which is the input
`mkStrided` builds (see its comment in `Main.hs` for how). Other operations
reach regime 3 by other routes, and those are the [stride
classes](#the-stride-classes-and-what-they-cover), populations of their own
beside this one.


### The shape set

The conv-derived shapes: the patch tensor, per image, laid out
`[outH, outW, Cin, KH, KW]` — the per-image `[nAh, nAw, nCinp, nKh, nKw]`
of the patch tensor above, renamed to the conventional axes (output spatial,
input channels, kernel) — and its per-position `[Cin, KH, KW]` slices, with dims
from real nets — kernels 3×3 (VGG/ResNet, horde-ad's own CNN), 5×5 (LeNet),
11×11 (AlexNet); channels 1 up to 512; spatial from horde-ad's 6/24 to
AlexNet's 55.

The `stretch-*` shapes are not conv-derived — extreme rank, extreme aspect
ratio, non-power-of-two dims, a cache-hostile innermost stride, a run length
of one element, a base-offset table as long as the result, a page-aliasing
power-of-two stride, and a mid-range innermost extent — to probe the space
beyond convolution. See `convShapes`/`stretchShapes` in `Main.hs` for the full
list.

**The conv set was halved after Run 6, and the shapes that went are not to come
back one at a time.** A strategy sees a shape as its innermost extent `sInner`,
its rank and its `l`, and nothing else — not which paper the dims came from —
and each dropped shape duplicated a kept one on all three while costing
a proportional share of every run. The freed wall clock went to A/A controls,
which calibrate every other figure and were the roster's scarce resource.
The halving moved the published geomean and the ratios between strategies past
the noise floor — a change of population and not of any strategy, which is why
Run 7 was read against Run 6 restricted to the surviving shapes. The ruling,
and the two shapes that must survive any later cut for a reason unrelated
to their workload, sit at `convShapes` in `Main.hs`, beside the list.


### Dropping the minibatch dimension

The minibatch dimension `nImgs` is dropped — every shape is for one image.
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
them reproduces a shape already here — a per-position slice, or a smaller conv —
so `nImgs` is the only dimension genuinely free to drop.


### The stride classes and what they cover

`mkStrided` transposes the two innermost dims of a dense array, so every stride
the main set carries is positive and its offset is zero. The library reaches
regime 3 through other operations too — its two commonest inputs of that kind
among them, a broadcast being stride 0 and `rev` negative — and the **stride
classes** are one population per producing operation, named by the prefix
that selects them: `rev` (every stride negated, offset at the top), `revsome`
(a strict subset reversed, so the signs are mixed), `bcast` (an innermost stride
of 0, every run re-reading one element), `bcastmid` (the stretched axis
in the middle instead), `reshape1` (the `[n] -> [n, 1]` trap, innermost extent
1), `slice` (a view of a larger source, so a non-zero offset with positive
strides), `window` (overlapping im2col patches — the workload this page opens
by naming, carrying the overlap that the main set's bijective index map drops)
and `scaled` (superincreasing strides, none of them 1). Each is a short list
in `Main.hs`, reusing a main-set shape where one fits so that a class figure has
a positive-stride counterpart to stand next to; each generator's comment there
says what it models, and the comment heading them all, above `mkRev`, carries
the coverage argument — a hypothesis about what a valid hand-built view can
recombine, not a theorem — which is not repeated here. *Class* unqualified means
one of these; the other sense on this page always keeps its noun, *method* —
a `class method`, the class-method tier, or in full a `Vector`-class method.

Two rulings govern how they are measured and published, both taken 2026-08-07,
ahead of the implementation:

- **Each class is its own pinned population**, published beside the main geomean
  and never folded into it. The geomean is a ranking statistic over a pinned set
  and a change of population moves it, as the conv-set halving measured; there
  is no combined figure to compute, so a sentence comparing populations compares
  their tables. One process per class follows from the same ruling,
  and `read-run.py` enforces it — it names the population it read, fails a file
  spanning two, and refuses to emit a table for one.
- **No strategy is excluded from any class.** Every one is to be fixed to work
  on all of them, seen failing first wherever the failure can be fired.
  The see-it-fail run found nothing to fix: the Int32 strategies' partial sums
  are each the offset of a real element, in-bounds for any valid view whatever
  the stride signs, so the feared failure cannot fire below a 2^31-element
  source — `int32Fits`'s own unfireable case. What mixed signs did break
  was the packed scan's assert — a corner formula, maximal only for positive
  strides, with no lower bound, its claimed maximum observed sitting below
  a real entry of `revsome-mid-cnn-L2`'s own base-offsets table — fixed
  at the builder, the numbers and the argument recorded at the assert and both
  Int32 comment sites.

**A class population is three shapes**, against the main set's two dozen, which
is deliberate — the classes are there to vary the *mechanism*, and varying size
and rank within one is the main set's job — but it decides how their results
read. A class geomean rests on three cells, so it is a summary of a handful
of numbers rather than a statistic over a spread; the per-shape figures
are nearly the whole population and are worth quoting where the main set's would
be flattened away; winsorizing has almost nothing to cap and `--pair`'s
bootstrap interval almost nothing to resample. What a class run can decide
is whether an *ordering* inverts under its mechanism and whether any strategy's
`worst` crosses 1 there. What it cannot do is be compared with a main-set
number, in either direction.


### The scratch vector flavour

Every table this suite builds — the `m`-element base-offsets of the `bq-*`
family, the `l`-element offset tables, the odometer's dimension vectors — used
to live in a **Storable** `Int` vector, because the payload is Storable
and nothing said the scratch had to follow. The fallback
in `Data/Array/Internal.hs` builds an **unboxed** one, deliberately: index
scratch is independent of the abstract element storage `v`, and the section
above says so in as many words. Nobody had noticed that the arm labelled
*shipped* in the results table therefore measured a vector flavour the shipped
code does not use, and no figure on this page had ever priced the difference.

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
Allocation is unmoved, so this is speed and not volume — the same bytes, held
differently, by a mechanism nothing here measured and the probe does not need.
The one shape it loses is `stretch-square-1341`, which was the worst-measured
shape of both runs and is this page's standing warning about reading a single
cell.

**It was measured twice, with the arms' roles exchanged**, which is why
the figure is quoted flatly rather than hedged. The first run put an unboxed
twin beside a Storable roster, on a machine with other work on it, and read
0.9377 (interval 0.9081..0.9690); the second put a Storable twin beside
an unboxed roster — after the conversion below, so the roster was by
then the other flavour — on a quiet machine, and read 0.9433. They agree
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

Run 7 (Harness) is the first run to measure the converted suite, so the tables
now say what the library actually does. On the shapes the two runs share,
`bq-expand` moved by −6.3% against the probe's −5.7% — the prediction met
at full budget — while the family did not move as one: `bq-scan-packed-mulback`
came out 4% *slower*, spread evenly over the shapes, and `mut-odo-vecdims`,
whose dimension vectors were Storable when its 0.051 was taken, read 0.056
on those same shapes — neither priced by a probe that had measured
the `m`-table's flavour and not theirs.

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
and by a margin matching what the conversion was seen to cost it — the one arm
the conversion hurt, and unexplained. The dimension vectors go the other way:
unboxed is 3.4% *faster*, so the conversion was worth −3.4% to `mut-odo-vecdims`
and removing the suspect deepens its move to about +13%. What is left
is position and code layout, which only a full roster can separate. Allocation
is identical within each pair, as two build-identical arms must be. The probe's
own gates: the `sum-only` halves agreed at 0.9991 and the term scaled 1.03×
across the set, while its one in-situ arm read 0.982; with no A/A pair
in the process its floor is Run 7's, which both margins clear.


### One element type, and what the probe found

Everything timed here is `Storable Double`, horde-ad's element storage, while
the fallback all of it justifies is polymorphic over the `Vector` class
*and* the element type. What the element changes is the copy — its width sets
how many elements a cache line holds, and the instance sets what a write costs —
and what it does not change is the index arithmetic, which is the only thing
the strategies differ in. So the question was never whether the magnitudes move
but whether the **ordering** does, and whether the shipped arm stays
under `list` at every instance the library serves.

The probe, run 2026-08-08 at -O1 on the desktop this page's other figures come
from: three arms — `list`, `bq-expand` and `mut-odo-vecdims`, spanning the list,
the per-element generate and the run copy — over six shapes chosen to span
`sInner` and `l`, one process per type, by `cabal run probe -- f32`
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

**The ordering holds at every type, and the shipped arm is never close
to `list`.** `bq-expand` spans 3.2% across the four, about the floor,
and its `worst` — the column that answers what a geomean cannot — sits between
0.317 and 0.322, so on no shape of any type did it come within three times
of the fallback it replaced. That is the property that had to hold for every
instance, and it holds with room to spare and almost no variation, across
an eightfold range of element width and two `Vector` instances.

**What does not hold is the tidy width story.** `mut-odo-vecdims`
is not monotone in width: `Float` (0.095) is *worse* than `Double` (0.084)
though its elements are half the size, while `Word8` (0.073) is the best
of the four. That is a property of the measurement and not a stray cell —
it reproduced on two independent runs, before and after the probe became
a program of its own — and it is unexplained. It is also nowhere near
an inversion, so it bears on the width intuition rather than on any ruling here.

Three cautions on the table. It is **uncorrected** — a probe carries
no `sum-only` bench — so every column is compressed toward 1 by the forcing
pass; that cannot flip an under-1 verdict, the correction only moving a ratio
further from 1, and it falls on all three arms of a type alike. The `alloc`
column divides by `8*l` whatever the element, so a narrower type reads low
by exactly the result vector's own share: predicted 0.50x below `Double`
at `Float` and 0.875x below at `Word8`, observed 3.23x and 2.85x against 3.73x —
both to the digit, which makes that column a consistency check as much
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

Everything the -O1 table is read for survives. The ranking is the same at every
type, `bq-expand` spans 7% across the four where -O1 gave 3%, and its `worst`
sits between 0.245 and 0.267 — so on no shape of any type does the shipped arm
come within three times of the fallback it replaced, in either regime.
The `alloc` column's consistency check reproduces to the digit: dividing
by `8*l` whatever the element predicts `Float` 0.50x below `Double` and `Word8`
0.875x below, and the observed gaps are 0.50x and 0.88x. So does the width
oddity — `Float` is again *worse* than `Double` for `mut-odo-vecdims` despite
half the width, which is now a two-regime observation and still unexplained.
The one thing that does not carry is the comparison itself: these figures
are the probe's, uncorrected, and belong beside the -O1 table above rather
than beside any run.

**These figures are the probe's own.** `Probe.hs` is a separate program
with its own transcribed arms — all four types, `Double` included, so that none
of them is served by the roster's originals while the others run copies
and a difference could be an artifact of the copying. The price is
that its `bq-expand` is bq-expand-*shaped* rather than the roster's, so a figure
here never belongs beside one from a run. Its six shapes are copies too,
and those *are* held to `Main.hs`'s own dims by `--lint`, which is
not a hypothetical guard: three of the six were transposed when first written
and the check named all three.

**So one element type stays, and generalising the suite stays refused** — now
on evidence rather than on cost alone. The cost argument is unchanged
and is under [what the benchmark does](#what-the-benchmark-does); what has
changed is that the coverage it buys is measured. Boxed elements
are deliberately absent, and not for cost — their elements are thunks, so each
arm would defer a different share of its copy into the forcing sum
and the fill/forcing split every figure on this page rests on would not hold.
Probing boxed needs a design of its own, not another duplicate.


### Lemire multiplicative inverses, at the two division sites

The idea (arXiv 2012.12369): precompute `M = floor(2^64/d) + 1` once per
divisor, then `n div d` is the high word of `M*n` and `n mod d` the high word
of `(M*n)*d` — two 64×64→128 multiplies instead of a division.
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
and sign p 1: a dead tie. The regime is the whole difference — same arms, same
shapes, same machine, one flag — so what the trick buys is however much
of the division GHC has not already dealt with, and the answer
is regime-specific in a way nothing else on this page is. The two extremes
survive the flip. `stretch-inner256` is still the arm's best cell (0.74
of its control) and `stretch-square-1341` still its worst (1.25), the run's
worst-measured shape — read that one as the shape, not the strategy; what
the flag moved is the twenty-odd shapes between them. Two controls back both
readings. Its allocation is identical to `bq-expand`'s on every shape, which
is what a build-identical arm must show; and it runs *before* `bq-expand`
in the group where `bq-gen-lemire` runs *after* `bq-gen`, so a warmer-later-slot
bias would flatter one and penalise the other and cannot produce both.

**At the per-dimension build site it loses in both regimes, by 35% and by 42%.**
`bq-gen-lemire` is `bq-gen` with the per-run, per-rank `quotRem`s replaced,
and it is 1.352× slower at -O1 and 1.421× under `-fspec-constr`, faster
on no shape of the set in either. The shape of the loss says why: it tracks
*rank*, not element count, rising from a few percent on the rank-2 shapes
to over half at ranks 7 through 12. The cost is paid per dimension,
so the division was never what dominated there. Two reasons. (i) The paper's win
assumes you want a quotient *or* a remainder; an odometer decomposition wants
both, so the trick pays twice and collects once — where `quotRemInt#` is one
`idiv` yielding both. (ii) The magic table is a third list to walk in step
with `nts` and `sts`, adding a dereference and a pattern match per dimension
to the very loop whose per-dimension work was the target. Rank 2 costs least
because there is only one dimension to walk, though not nothing.

What separates the two sites is (i) and (ii): at the output the divisor
is a loop invariant, so `M` is computed once for the whole fill with no list
beside it, and the per-element work really is one division against two
multiplies. The win is 6.0% rather than several-fold because the hardware has
moved since the paper — 64-bit `idiv` on this Zen 3 is ~14–19 cycles against
the 40–90 that made the trick famous.

Two things a Core dump settled that source reading had got wrong. Both
are recorded because both were argued the other way first. **`quotRem` on `Int`
is not one instruction**: GHC wraps `quotRemInt#` in two guard branches,
for a zero divisor and for the `minBound quot (-1)` overflow, both
on a loop-invariant divisor — so the `d == 1` guard `fastQR` needs is
not the asymmetry it looked like, the baseline carries two of its own.
And **the first `fastQR` spent three multiplies where the algorithm needs two**,
taking the quotient from `timesWord2# m n` and then recomputing the low half
as a separate `timesWord# m n` when the one `timesWord2#` already yields both.
Fixing that is what turned the output site into the win it now measures,
and it recovered part of the build site's loss too — enough to see, nowhere near
enough to reverse it. Why the low half must not be recomputed is recorded
as a comment on `fastQR`, so the loose form is not written again.

**On shipping it.** `bq-expand-lemire-out` is pure, so the argument that kept
`mut-odo` out (a bar then, a weight since the mutable ceiling's amendment) does
not apply; what it costs is `MagicHash` and `UnboxedTuples`
in `Data/Array/Internal.hs`, about a dozen lines of helper, and a precondition.
The precondition is the substantive part: Lemire's identity holds
for `d, n < 2^32`, and `n` here is the linear output index, so a shipped version
needs an `l < 2^32` test choosing between the two fills — loop-invariant
and chosen once per call, but it must be there, since orthotope does
not otherwise cap array length. **The conditional this paragraph used to end
on has resolved against it**, and against shipping: the 6.0% is an -O1 figure,
the file the fix is added to sets `-fspec-constr`, and under the flag the same
pair is a dead tie — so what there is to weigh against `MagicHash`, the helper
and the precondition is nothing. This page still only prices the arm; at zero,
the pricing is the answer.


### Per shape, where the geomean hides the ordering

The geomean is stable but flattens. Below are the `stretch-*` shapes — chosen
to push past the ranges the rest cover, and named here without their prefix —
against the strategies nearest the decision, each as a multiple of `list`
on the same shape. These are Run 13 (SpecConstr)'s own figures,
from its **basis** half as the fingerprint is, all of them net of the forcing
pass like the rest of the page. A `lemire-out` column stood between
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
is the axis the orderings turn on; the fuller per-shape record is in [What Run
15 compares against](#what-run-15-compares-against).

- **Which strategy wins is decided by the innermost extent (the size
  of the innermost dimension, `sInner` below) — not by the rank, not
  by the element count.** `stretch-inner1` is where the expansion family does
  best against the odometer fills: `bq-expand` (0.076) and `bq-expand-b` (0.069)
  beat `mut-odo` (0.277) and `build` (0.271) three- to fourfold, which they do
  on no other shape here — `stretch-pow2stride` excepted, where the two families
  converge outright (0.068–0.070 across expansion and odometer alike).
  Its innermost extent is 1, so each base offset covers a single element:
  the odometer that `mut-odo`/`build` step has nothing to amortize over, while
  the expansion build has no per-element odometer to begin with. At the other
  end `stretch-tall-Mx2` has an innermost extent of half its length
  and the ordering inverts completely — `mut-odo` 0.018 against `bq-expand`
  0.072, with every mutable fill ahead of every pure arm (the slowest fill
  0.058, the fastest pure arm 0.064). The geomean reports that second case
  and averages the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry:
  that `stretch-inner1` is *the only shape where the pure expansion strategies
  beat every mutable one*, with the four `bq-expand` variants taking the top
  four slots. They no longer do, and this roster says so more plainly than Run
  6's: `mut-flat-gm` and `bq-mut-runs-gm-mulback` take that shape tied at 0.027,
  both ahead of every expansion variant, while `mut-odo-vecdims` sits at 0.097 —
  strategies that did not exist, or were not rostered, when the claim
  was written. The unit innermost extent still explains why `mut-odo`
  and `build` do badly there; it never implied that no mutable fill could.
- **Per-shape figures are far noisier than the geomean: trust the first digit
  only.** Independent runs of these shapes agree within 1–5% on most cells
  but differ by up to 27% on `stretch-inner1/bq-expand-b` — runs whose rosters
  also differed, making the [roster effect][floor] a candidate cause —
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
  0.030 against 0.078 — its best cell of all 24, as it was at -O1. Those four
  figures are quoted rather than looked up because both arms have since left
  the timed roster and their per-shape columns left the fingerprint with them;
  the reading is Run 8's and is what a later run would have to re-establish
  before using it. Read such a cell first and average it away last.

All three bullets are measured on positive-stride views. The [stride
classes](#the-stride-classes-and-what-they-cover) put the same axis under other
mechanisms — `bcast`'s innermost stride of 0 has every run re-read one element
whatever its extent, `reshape1`'s extent is 1 by construction, `scaled-rank1-m1`
is a single run — so each class run is a test of whether `sInner` still decides,
and a class table that contradicts this ruling is a finding to write up rather
than a cell to average away.


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
- Non-vacuity: deliberately dropping the `r * tInner` term fails the suite
  at `transpose_2/4/5/6`, `stride_1` and `rev_1/2` among others — so the pass
  is not vacuous.
- This benchmark: every strategy agrees with `list` on every shape, the [stride
  classes](#the-stride-classes-and-what-they-cover) included, so the agreement
  covers negative, mixed-sign, zero and overlapping strides and not only
  the positive ones the main set carries — and in both regimes, `check` having
  been re-run under `-fspec-constr` as well as at -O1.

End-to-end confirmation in horde-ad's `bench/ConvVjpBench.hs` — wiring
this branch's orthotope in and rebuilding ox-arrays + horde-ad — has been done
and is reported in that repo, not here.


### The mutable ceiling (not taken)

The `bq-*` strategies still fill the result one element at a time. The tightest
possible shape drops to a **mutable result buffer**: allocate it once, walk
the outer odometer, and write each innermost run with a tight additive inner
loop — no `quotRem`, no base-offsets table, no per-element step.
That is `mut-odo` and `mut-odo-vecdims` (0.049), the latter 2.11×
over `bq-expand` on Run 13 (SpecConstr); its family holds the top of the table,
`mut-odo-vecdims-add-in` leading it on a tied sign test with both printing
0.049. All allocate essentially just the result vector. `offtab` (0.125) does
not go that far — its output is an ordinary `vGenerate` and only its `l`-sized
`Int` offset table is filled mutably, so it needs no class method, just
a mutable scratch — and it sits **25% behind `mut-odo`** for it, at two wins
of 24 with sign p 3.6e-05, where Run 10's aligned half read 26%
and its unaligned half tied them: alignment decided this comparison and three
runs since have held it. On these numbers it is no longer the cheap way to most
of the gain, as it was when Failed Run 6 had the two tied, and the gap it must
close to become one again is 2.6× against `mut-odo-vecdims` (0.3901 paired, 24
shapes of 24).

**Plain `mut-odo` has stopped making the case, and it is not the regime's
doing.** Run 8 read the pair 1.08× *against* `mut-odo` and blamed the flag,
which sets that arm back hardest but one; Run 9, same flag, has the geomean back
on `mut-odo`'s side at 0.947, Run 10 at 0.9671 aligned, Run 11 at 0.9842 and Run
12 at **0.9719** — and it is still not a win, at nine shapes of 24 with sign p
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
`build` prices exactly that — `mut-odo` driven through `vBuildVS`, a prototype
of

    vBuild :: Int -> (forall s. (Int -> a -> ST s ()) -> ST s ()) -> v a

— and Run 6 had it matching `mut-odo` on every shape, so **the class method
was free there** (it inlines to the identical loop). Run 7 (Harness) broke
that identity, `build` reading 1.24× behind `mut-odo` paired and slower on 22
shapes of 24, on cells whose own CIs are hundredths of a percent, with neither
arm's source changed between the two binaries.

**The Core says the identity holds and the gap is the measurement — in both
regimes now.** Dumped from Run 6's source and Run 7's against one pinned
dependency set, `$wfbBuild` and `$wfbMutOdo` are the same worker in both
binaries — byte-identical once GHC's numbering is normalised, with `vBuildVS`
surviving as no top-level binding in either — and the two sources differ only
by the `Strides` newtype's zero-cost cast, which falls in both arms alike,
so neither binary is the odd one out. Nor is a dependency: `vector`
and `criterion` have been the same versions across those runs. A probe
then failed to reproduce the gap at all — in a binary relaid out by two inserted
arms the pair reads 1.004 paired (0.976..1.032, 11 shapes of 22), 1.24× falling
outside its whole per-shape range. Dumped again from Run 8's own commit
under `-fspec-constr` (2026-08-08) the two workers are still the same worker,
identical once the numbering is normalised down to the four floated
`init`/`last` error thunks each carries a private copy of, and `vBuildVS`
is still no top-level binding. So **the signature is free**, and no `vBuild`
is to be held back on either run's figure.

**What the pair has become is a second instrument, and it is read where
the other instruments are.** Two top-level names with identical Core are a true
ratio of exactly 1, which is what the A/A controls are built to supply,
and this pair disagrees by far more than they do — so it prices what placement
does to two *separately compiled* arms, where the twins price only what it does
to two calls of one. That reading, its figures in every run and population,
and the per-loop account underneath it are [in the floor section][floor]
and are deliberately not repeated here: what this section needs from the pair
is only that its disagreement is placement rather than the abstraction, which
is what leaves the identity above licensing `vBuild`. A pure-typed alternative
(a strided-gather method taking the shape/stride/source and hiding the mutation
inside each instance, as `vGenerate` already does) would keep the speed without
`ST` in the signature.

This was **deliberately not taken.** Orthotope's `Vector` API was to stay pure
and minimal, and the gain over `bq-expand` (pure-Haskell either way, so [the
C-gap](#the-c-gap-still-a-deeper-ceiling) bounds both) did not justify a new
class method across all four instances. The strategies stay here as the measured
evidence for that ruling — since amended below: the evidence now prices
the option instead of closing it. `mut-odo-vecdims` keeps the stake high rather
than settling it: the fill's real cost was the odometer's cons-list traffic,
not the fill itself, and Run 10 (SpecConstr) prices the class-method tier
at 2.11× over `bq-expand` (0.4745 paired). Against that, the best pure strategy
reaches 0.090, so the gap the class method would buy is **1.85×**, not 2.11× —
which is the figure the ruling turns on. It has now read 1.80× at -O1, 1.68×
on Run 8, 1.87× on Run 9, 1.85× on Run 10 with its aligned half giving 1.84×,
and **1.84×** here — the same cell and the same 23 wins of 24 as Run 10's
aligned half, to four digits. So the spread is a tenth either side of 1.8
and neither the pairing nor a repetition moves it. Read it as *approaching 2×
and volatile at the tenth* between runs that differ, and do not reopen or close
the ruling on a movement of that size — Run 10 showed the volatility is
not the layout's, and Run 11 shows it is not the run's either, which leaves
the roster and the regime as what moved it.

**Amended 2026-08-07: the bar is now a weight.** The tree itself carries
a precedent this section did not weigh: `Data/Array/Internal/FastReshape.hs`,
a `runST` flattener over this same fallback territory — structurally `mut-odo`,
an allocate-once mutable result filled through an outer odometer recursion
with a per-element strided inner copy loop, its outer offsets stepped additively
where `mut-odo` multiplies — which sidesteps the `Vector` class altogether
by `unsafeCast` to `Double`/`Float` on element size. So neither mutability
nor needing a new class method *disqualifies* a strategy any longer. What keeps
both as weights against one is that FastReshape.hs is not in use — absent
from the cabal file, and still declaring its source project's module name
and imports (`CoreCompiler.ArrayReshape`; `Utils.Misc`, `CoreCompiler.Error`),
so it does not even compile in place: precedent for writing such a module,
not for shipping one. A mutable or class-method strategy is now priced against
that weight rather than refused at the door.

**And now weighed in code, 2026-08-08: the four FastReshape arms.** They port
the precedent's loop arithmetic onto `mut-odo-vecdims` one axis at a time, a 2×2
plus one over that shared control: `mut-odo-vecdims-add-in`, the input offset
stepped additively in place of the loop's one multiply;
`mut-odo-vecdims-add-out`, the output position through a precomputed stride
table in place of the threaded return — the axis that can lose;
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
of 24, sign p 0.00028) against 1.0009 at 13 of 24 — three of the four inside
a quarter of a percent, and the fourth the sign-test flip [the Results
findings](#results) read as the instrument rather than the arm. The corner stays
sharply sub-additive — 11.7% where the two solo losses sum to 15.2% —
and the count-down form still recovers most of the corner's loss, 0.9408 against
it on 22 shapes of 24 where Run 10 had 0.9412 on 24 of 24.

**Run 9 had priced them differently, and the pre-run reading was right about
the sign and wrong about the size.** That reading — one shape, Run 8's regime —
put all four behind their control by +4% to +12%, the corner sub-additive
and the count-down form recovering two thirds of its loss. Over 24 shapes Run 9
read `add-in` **1.1552** (0 wins of 24), `add-out` **1.1795** (1 of 24),
`add-both` **1.1645** (1 of 24), each against `mut-odo-vecdims` and each
with sign p at or below 3e-06. So all three solo-or-corner arms sat behind their
control by more than the one-shape probe suggested, and near-unanimously across
shapes — which the write-up first read as the precedent's arithmetic losing
on both axes, and which the Core reading two paragraphs down withdraws:
near-unanimity across shapes is what the identical-code pair shows too,
so it separates nothing. The corner is sharply sub-additive, 16.5% where the two
solo losses sum to 33.5%, so the two axes are largely paying for the same thing.
The count-down form is the one that pays: `add-both-down` reads **0.8745**
against the corner on 23 shapes of 24, recovering nearly the whole loss rather
than two thirds, and it ties the shared control outright (1.0183, 13 of 24, sign
p 0.84). Allocation was not in doubt and is not — all four read 1.00x,
the stride table costing about 1.3 KB against a megabyte-scale result.

**Why the count-down form pays is now in the Core, and why the other three lose
is not what this section took it to be** (2026-08-09, `-fspec-constr`).
`add-both-down`'s innermost run-fill is seven instructions where every sibling's
is eight: it carries the output position in a register and steps it, where
the others rebuild `outPos + j` with a move and an add on every element.
That is a per-element change, and Run 9 agrees it behaves like one —
its advantage grows with `sInner`, r −0.29 against log `sInner`, 1.052 where
`sInner` is 3 or less against 0.972 where it is 8 or more. The other three do
not. `add-in`'s counted loops are identical to its control's instruction
for instruction, its whole code difference sitting in the odometer recursion,
where one multiply becomes an accumulated add threaded as a further argument —
a per-*run* change. `add-out` and `add-both` carry real extra code of the same
kind — a `scanr (*)` over the shape, built into a byte array once per call
and read once per run — which adds nothing to the per-element loop.

**Run 9 could not see those as per-run changes and Run 10 can, which
is the second thing the pairing bought.** On Run 9 the three penalties were flat
in `sInner` (`add-in` r +0.21) and largest on `stretch-tall-Mx2`, shape [2,
900000], where the odometer descends twice per call — 1.3152, 1.2930 and 1.2901
there, which two multiplies and a two-element table cannot cost. That
was the argument for suspending them, and it was right to suspect the figures:
they were layout. Read on Run 10's aligned half, where every copy of the shared
loop sits at offset 0, the same regression comes out the shape a per-run cost
has to have. **`add-out`'s penalty scales as 1/`sInner`**, r **−0.64** against
log `sInner` and **−0.01** against log `m`: 1.423 on `cnn-L1-6x6-c1` and 1.340
on `cnn-slice-c32`, both `sInner` 3, against 1.009 at `sInner` 256 and 0.997
at `sInner` 64. A cost paid once per run and amortized over the run's elements
is exactly a penalty that falls with the run's length and ignores the number
of runs, and `stretch-tall-Mx2` — the shape whose 1.29 was the objection — now
reads level. `add-both` tracks it at r −0.64, and `add-in`, which is free,
is flat at −0.16 over a 0.955–1.078 range. So the code identified
in 2026-08-09's Core reading is the code that pays, the arithmetic is per-run
as that reading said, and what stood between the two was the address of a loop
neither arm's difference lives in.

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
  arms share.
- **`add-out` is convicted, and the corner with it.** It reads 1.1266 resident
  and **1.1612** aligned, `add-both` 1.0906 and 1.1184, on four placements
  between them and no straddle among any of them. So the +18.0%
  is the arithmetic's after all: carrying the output position through
  a precomputed stride table, in place of the threaded return, costs about 16%,
  and the corner's sub-additivity is a property of the two axes and not of where
  they landed.

That is the outcome the registration named as killing the straddle hypothesis
for the arm that shows it, and it kills it for two of three. What survives
is sharper than what it replaces: of the three axes FastReshape's loop
arithmetic ports, one is free, one costs 16%, and the count-down form that ties
its control is the third.

**The pad probe had upheld the suspension**, and this is where the two
instruments part. Stepping a shared loop through all eight offsets prices a deep
straddle at 1.19 against a resident copy, and these three sat at mod 40, 44
and 44 against a control at 24 — a predicted 1.18 against the 1.155 to 1.180
they read, on a family and a binary the probe never touched ([the floor
section][floor]). The agreement was real and was a coincidence for two
of the three arms: the correction the probe supplies is a *screen*, licensed
only where the loop is the same code, and here it is the same code while
the arms differ elsewhere as well. Read that as the screen's stated limit
meeting a case it could not see rather than as the probe being wrong — its own
binaries, which differ in placement and in nothing else, still reproduce
to a median 1.0%.

**What that does to the precedent's weight.** FastReshape's arithmetic, ported
one axis at a time onto this page's fastest arm, buys nothing here and one axis
of it now demonstrably *costs*: the count-down form ties the control,
the additive input offset is free, and the precomputed output stride table
is 16% behind on a layout that cannot be blamed. So the in-tree precedent argues
for the *shape* of a mutable fill and not for its arithmetic, and the ruling
above is unmoved: what a new class method would buy is still `mut-odo-vecdims`,
at [the 1.85×](#results) the ceiling section prices, and none of these four adds
to it.


### The C-gap: still a deeper ceiling

**Everything in this document lives under this ceiling.** Every strategy
in the table, every ruling resting on one, and every margin the ~3% floor
adjudicates are rearrangements *within* pure Haskell — and no pure-Haskell
strategy closes the gap to the stride-aware C kernels. Measured on the analogous
chain (horde-ad's interleaved A/B of 2026-07-31, recorded in that repo):
concrete *scatter*, which routes through them, runs it in ~0.5 ms,
and the gather over this branch's fix takes 2.55× that in its natural
orientation, 1.32× in its fastest — a 1.3–2.6× gap, down from the order
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
  from deltas is a prefix sum — a scan the callback would redo per element.
- **Reordering the expansion so the largest outer dimension expands last**
  (to shrink the `concatMap` intermediates, whose sizes are the prefix products
  of the expansion order) has no freedom to spend: the table must be indexed
  by the row-major run index, so the expansion order is fixed by the output
  order.
- **Fusing the base-offsets build into the output fill** — the output reads
  the table at `q = i div sInner`, which ascends monotonically, so the two
  passes could stream in lockstep; but the callback would then carry odometer
  state, and a stateful fill is exactly what the mutable ceiling's class
  extension exists to provide — so since that ceiling's amendment this idea
  is priced with it, not dead outright. The table exists because `vGenerate`
  is stateless.
- **Caching the table across calls** (horde-ad normalizes the same shapes
  over and over) — `toVectorListT` is a pure per-array function with nowhere
  to keep a cache.
- **Padding the innermost extent to a power of two**, so the output division
  becomes shift-and-mask — padding changes the enumeration the contract fixes,
  and conv's inner extents are 3/5/7/11.
- **A separate `q`-table** (`qtab[i] = i div sInner`, in Int32) — strictly
  dominated by `offtab32`, which stores the finished offset for the same
  traffic.
- **Software-prefetching `v` from inside the callback** (which may legally read
  the offset table ahead of `i`) — GHC's prefetch primops all thread `State#`,
  so a pure callback cannot issue them without an unsafe escape.
- **`constructN` instead of `scanl'` for the prefix-sum build** (its callback
  legally reads the already-built prefix) — the scan fuses, so the fallback
  is moot, and it loses regardless: the recurrence reads `table[q-1]` back
  through a store-to-load forward where the scan carries the sum in a register,
  each step passes a freshly wrapped prefix slice, and the one power `scanl'`
  lacks — deltas depending on earlier *values* — is power a position-only delta
  never uses. Prefix access cannot even cheapen the carries:
  `table[q] = table[q - suffixProduct c] + st_c` still needs the same
  divisibility cascade to find `c`.
- **A branchless delta select in the scan build** (folding the carry correction
  in arithmetically instead of branching) — the branch's outcome is periodic
  with period `sInner`, which a modern predictor learns, so the branch
  is already ~free.
- **Unrolling the scan by `sInner`** so the carry test runs once per run —
  `sInner` is not a compile-time constant, and GHC will not unroll a loop
  by a runtime value.
- **Alternatives to the Granlund–Montgomery form for an unbounded output
  quotient.** For a stateless output loop with a runtime divisor that wants
  quotient and remainder both, the GM round-up magic is the end of the road.
  Barrett reduction's correction step is a *data-dependent* branch —
  a misprediction generator where GM's dispatch is loop-invariant;
  floating-point reciprocals cap the dividend at 2^53 and need an exactness
  proof plus FMA to be safe; a full-width 128-bit Lemire magic spends three
  multiply-highs, worse than the division it replaces. And the general GM form's
  65-bit add-fixup never arises here: `Int` dividends spend only 63 bits,
  so a magic of width `63 + ceil(log2 d)` always fits one `Word` — one
  multiply-high and one shift per element, no bound on `l` (`gmMagic`
  in `Main.hs`).


## About the current harness

**This chapter normally does not change from run to run either**, but
for a different reason: it describes the instrument rather than any result.
Every generic instruction for making, reading and checking a run is here,
and a session told to make one can work from this chapter alone — but
for the two layouts a write-up pastes into, which sit beside the figures they
explain: the [Results](#results) columns and the [per-class
blocks](#the-stride-classes-run-by-run). What is *not* here is anything
a particular future run has to settle — that is [What is open](#what-is-open),
the chapter at the front, which is where everything that goes stale as soon
as a run reports is now collected.


### What the benchmark does

`Main.hs` replicates orthotope's `T` representation and its `toListT` faithfully
(specialised to `Storable Double`, horde-ad's element storage), then compares
the regime-3 strategies in one binary — the real orthotope compiles only one
at a time, so a replica is the only way to A/B them.

**One element type, where the fix serves them all.** Everything here
is `Storable Double`; the fallback is polymorphic over the `Vector` class
and the element type. Element width sets how many elements a cache line holds
and boxed elements change the copy entirely, so the *ranking* and not only
the magnitudes may differ for the instances the shipped code actually serves.
Nothing in the roster probes that; `Probe.hs`, a program of its own, does
at three further types and found the ordering unmoved — [the
probe](#one-element-type-and-what-the-probe-found) is the evidence
this restriction now rests on, boxed excepted.

**Don't generalise the suite to run every arm at every element type.**
The typing is the cheap part — the payload is only ever loaded and stored, all
the arithmetic being `Int`, so `T a` and a `Storable a` context would cost about
sixty lines of signature. What it would really cost is a run per type,
and the roster shared by both is what makes figures commensurable, so the choice
is between interleaving them — doubling the roster and re-collapsing the A/A
spans the crossed controls need — and two processes, whose comparison
then crosses processes and inherits the roster effect. The code cost is worse
than it looks too: `NOINLINE` on a polymorphic function blocks specialisation,
so every arm would time a dictionary rather than a fill unless roughly forty
`SPECIALISE` pragmas are added, **and each of those has to be confirmed
in Core** — an unverified one leaves the dictionary in place and the suite
then measures dispatch while reporting it as a strategy, which is the failure
mode that looks most like a result. Probe instead: a handful of shapes at one
other type, asking only whether the ranking inverts. The property that has
to hold for every instance is not the ranking but `worst` staying under 1 —
never slower than the fallback being replaced — and six shapes will show that.

The strategies are named here and *described* in `Main.hs`, each at its own
definition, where a reader meets the code the description is about. This list
is the index, in that file's definition order — base before variant, which
is also the order to read them in:

- **The originals and the first attempt.** `list` (the fallback being replaced:
  `vFromListN l . toListT`, a lazy cons-list), `gen-quotrem` (a `vGenerate`
  over one `quotRem` per *dimension* per element), `gen-unsafe` (that minus
  the bounds checks, to price them), `unfold-add` and `fused`
  (an `unfoldrExactN` odometer, allocating and then allocation-free).
- **The run base-offsets family**, all with the same output — one `vGenerate`
  doing one `quotRem` per element against a precomputed `m`-element table —
  and differing only in how that table is built: `offsets-quot` (lazy list),
  `bq-mut` and `bq-mut-runs` (mutable odometer), `bq-unfold`, `bq-gen`,
  `bq-gen-lemire` (Lemire at the build site; kept because it *lost*, so the idea
  is not re-proposed), `bq-expand` (**shipped**), `bq-expand-zf`
  and `bq-expand-b`.
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
  the unconditional twin of the one before it — its bound is the builder's,
  which no output substitution reaches.
- **Direct mutable result-buffer fills**, which need a class extension
  or explicit mutation and are the [ceiling](#the-mutable-ceiling-not-taken):
  `mut-odo`, `mut-odo-vecdims`, `mut-offsets`, `build`, `mut-flat`
  and `mut-flat-gm`, the unconditional twin of the last. And `concat-runs`,
  class-methods-only and the first arm to be checked without being timed
  (below).

The order they are *run* in is deliberately a different one, fixed by `roster`
in `Main.hs`, where a majority of them now take no slot at all, being checked
and not timed; the Results table below is sorted by time, a third. Sharing
that roster with the strategies, and not strategies themselves, are twenty-three
controls: eighteen A/A arms — `bq-expand-aa-adjacent`
and `bq-expand-aa-distant`, `bq-scan-rem-gm-mulback-aa-adjacent`
and `bq-scan-rem-gm-mulback-aa-distant`, `mut-odo-vecdims-aa`
and `mut-odo-vecdims-aa-distant`, `offtab-aa-adjacent` and `offtab-aa-distant`,
`bq-odo-gm-mulback-aa-adjacent` and `bq-odo-gm-mulback-aa-distant`, and, added
2026-08-14, `build-aa-adjacent` and `build-aa-distant`, `mut-odo-aa-adjacent`
and `mut-odo-aa-distant`, `list-aa-adjacent` and `list-aa-distant`,
`gen-unsafe-aa-adjacent` and `gen-unsafe-aa-distant`, nine strategies each
duplicated in both positions — the `sum-only-early`/`sum-only-late` pair,
and `bq-expand-nosum`, `mut-odo-vecdims-nosum` and `mut-flat-gm-nosum`, each
its base arm forced with one element instead of the sum. [The noise
floor](#what-moves-a-figure-when-no-strategy-changed)
and [sum-only](#sum-only-and-the-correction-now-applied) say what each is for.

The `check` mode (below) asserts every strategy produces byte-identical vectors
on every shape, that each shape actually takes regime 3, and that the view's
innermost extent is the second-to-last dim as listed — which is the one thing
`read-run.py` has to assume, since no JSON carries the strided shape, and which
`m` and every `alloc` multiple rest on. The [stride
classes](#the-stride-classes-and-what-they-cover) go through the same mode, each
held to its own structural conditions — negative strides, mixed signs,
a stride-0 axis — with a deliberate-breakage proof per conjunct, and each class
list has its own reading of the innermost extent in the reader, which `check`
is again the only place to confirm. It is built from that same `roster`,
so a strategy cannot be timed without being checked; what that leaves to go
stale, `read-run.py --lint` holds — every arm named here, every strategy defined
in `Main.hs` rostered, each A/A control running the arm its name duplicates,
every control named as the reader's own control test reads it, and every shape's
`l` annotation agreeing with what its list's rule computes.

`concat-runs` was the first strategy `check` covers and the benchmark does not,
and is the only one excluded on its own noise rather than by a ruling below.
It was by a clear margin the noisiest bench of the set — Failed Run 6's single
worst cell, and a median cell some 2.5× the shape's typical CI — so excluding
it costs no information the run needs, and it is one of the changes preceding
the current, quieter run, though nothing separates its contribution
from the others'.

The worry was never its own figures but its neighbours': every `time` is a ratio
to `list`, which runs before every strategy, so an aftermath outliving one bench
would tilt the group rather than cancel. The probes found nothing —
its successor timed the same after it as after a benign predecessor, and
of the three A/A pairs the one straddling it agreed best. What stays unprobed
is the [roster effect][floor], worth ~18% in horde-ad's `ConvVjpBench`
and persisting for a whole run rather than one bench: unretired rather
than absent, since that case ran benchmarks of a different scale.

**Two rulings taken 2026-08-08 cut the timed roster from 38 strategies to 15,
and the arms written since bring it back to 23** — the four unconditional forms
the precondition ruling itself called for (below) and the four FastReshape arms
([the mutable ceiling](#the-mutable-ceiling-not-taken)). Both rulings are about
what is worth spending a bench on, not about what is worth keeping: every
dropped strategy stays in `Main.hs` and stays in the roster as `concat-runs`
is — checked against the reference on every shape of every class, and not timed
— so the agreement net does not shrink and nothing has to be rewritten
if a ruling is later reopened. The 23 arms the rulings dropped carry `Only`
in that roster, each naming the bound or the multiple that disqualified it;
with the controls the run is 47 benches.

- **A strategy with a precondition is not measured.** The column allowed `none`,
  an empty cell, and `shape well-formed`, which is a condition on being a valid
  view at all rather than on size; everything else is a size bound the caller
  would have to discharge. What that costs is real — it takes `bq-odo-mulback`
  (0.089), the fastest pure arm of Run 8, and the whole `mulback` output family
  with it — and the ruling is that the speed does not make up
  for the restriction: a fallback that needs `l < 2^32` tested and a second fill
  kept for when it fails is a different proposition from one that does not,
  and this suite exists to find the second kind. **Four runs now say the cost
  was near zero**, which the ruling did not need but is worth recording:
  its unconditional counterpart `bq-odo-gm-mulback` has come in at 0.090 on each
  of Runs 9 to 13, within a thousandth of the arm it replaces, and on Run 13
  it took the head of the pure tier outright again (0.9949 paired against
  `bq-scan-rem-gm-mulback`, 7 of 24, sign p 0.064 — a tie by the sign test
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
  the tier above it, which is the whole of the `new pure Vector method` group —
  `fused`, `all-expand`, `cm-gather`, `backperm`, `unfold-add` — plus
  `offsets-quot`, `bq-unfold` and `mut-offsets`.

`list` is exempt: it is the reference every ratio divides by, not a candidate,
and its 23.5x is the thing being beaten. `gen-quotrem` and `gen-unsafe` survive
both cuts at 1.00x, which the page needs — the first attempt is what the fix
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
  bound no longer exists — which is the ruling doing its work, since that pair's
  whole subject is the bound this rule now refuses;
- claim 4's controlled pair, `bq-scan-mulback` against
  `bq-expand-lemire-mulback`, loses both halves, and the Lemire output
  substitution loses its arm. Those *readings* stand as Run 8's and cannot
  be re-measured under this roster, which is the price of the rule
  and is recorded rather than worked around. Both *questions* survive
  on the counterparts written below, and [the claims
  list](#the-claims-run-15-should-test) has been re-aimed onto them.

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
and `baseOffsetsGenLemire` carry a bound of their own — on `m` rather
than on `l`, which is what their consumers' roster entries mark
as *its builder's*; `baseOffsetsExpand`, `baseOffsetsOdo`, `baseOffsetsScanRem`
and `baseOffsetsMutRuns` carry none. Eleven of the fifteen dropped arms had
a counterpart already timed — the mutable-scratch family through `bq-mut`,
`bq-mut-runs` and `bq-mut-runs-gm-mulback`, the scan family through
`bq-scan-rem-gm-mulback`, whose builder drops the bound the Granlund-Montgomery
output cannot reach, and `bq-gen-lemire` through `bq-gen`, its Lemire being
at the build site. Four had none and were written: `bq-expand-gm-mulback`,
`bq-odo-gm-mulback`, `mut-flat-gm` and `offtab-scan-rem`, the last
not a Granlund-Montgomery twin because its bound is its builder's. All four
clear the allocation bar already, at 1.33x, 1.51x, 2.00x and 2.35x — measured
twice, on a quiet machine and a busy one, to the same digits, which
is the property the bar was chosen for. Three runs have now said whether they
are fast: on Run 11 `mut-flat-gm` reads 0.081, `bq-odo-gm-mulback` 0.090,
`bq-expand-gm-mulback` 0.094 and `offtab-scan-rem` 0.119, so three of the four
land ahead of the shipped arm and the fourth behind it, as in each run before.

Two of the eleven are covered at the level of the idea rather
than line-for-line, and say so here rather than being counted quietly.
`bq-expand-lemire-out`'s counterpart is the mul-back output, Granlund-Montgomery
having no `out` analogue that yields quotient and remainder together.
And **the `Int32` narrowing cannot be rescued at all**: its bound is `int32Fits`
on the source, which is what narrowing *means*, so `offtab32`
and `bq-expand32-lemire-mulback` leave with no unconditional form possible.
That is the ruling's sharpest cost, because the narrowing is the one
hand-packing that survives the flag — 0.877 of its control for `offtab32`
and 0.949 for the expansion pair, where the packed state is dominated.
The ruling stands as taken; what it gives up is measured and recorded rather
than assumed small.

`--lint` and `--markdown` both took the change with the roster: the first
asserts every defined `fb` function is rostered, which the not-timed mechanism
satisfies, and reports the not-timed set as a note rather than a failure;
the second carried `needs` and `precondition` forward from the table above,
so the column left the reader and the table in the same commit — a column
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
    cd micro-regime3 && cabal run probe -- check     # the element-type probe
    cd micro-regime3 && cabal run probe -- f32       # one element type

`probe` is a second executable and not part of the roster: [the element-type
probe](#one-element-type-and-what-the-probe-found), whose own header
in `Probe.hs` says why it is a separate program and what its separateness costs.
Both are executables rather than benchmark stanzas, which is what lets every
mode above take its arguments directly — and what keeps a bare `cabal bench`
from launching a multi-hour run.

The `classes` mode replaces the main set
with the [stride-class](#the-stride-classes-and-what-they-cover) populations,
one selected per process by its name prefix; without a prefix it runs all
of them into one process, which is a probe and never a recorded run, the reader
declining to publish a table over two populations.

`cabal.project.freeze` pins the resolved plan — `vector`, `criterion`, `base`
and the rest, with an index-state — so that a recorded run's source commit
and its dependencies are both known. It postdates the earliest runs recorded
here and so cannot pin theirs; what covers those is a hand check that `vector`
and `criterion` have been the same versions since Failed Run 6 inclusive, which
is what lets a question about generated code be asked across those runs at all.
One pin is load-bearing rather than housekeeping: `vector` is built
`+boundschecks -unsafechecks`, which is what makes
the `gen-quotrem`/`gen-unsafe` pair price a bounds check at all, since one uses
`VS.!` and the other `VS.unsafeIndex`.

`micro.cabal` builds at -O1, which is what a default `cabal build` of orthotope
takes — **and that is not the regime the fix ships in**, a correction made
2026-08-14 after several entries had been written on the other reading.
`-fspec-constr` will be set in the file the final solution is added to,
`Data/Array/Internal.hs`, rather than left to whatever `-O` a caller's build
settles on, so the shipped regime is `-fspec-constr` and every run since Run 8
is already in it. Other regimes are command-line only, the flag landing after
the cabal file's so the later `-O` wins: `-fspec-constr` when testing
the `SpecConstr` optimization effect, `-O2` for the half of the scan-fusion
refutation that inverts there (a `diag` at `-O2` is what measures it). **The RTS
is a second thing the shipped setting fixes and this suite does not share**:
the prevailing use of the library is in programs carrying
`-with-rtsopts=-A1G -I0 -T -M8G`, where `micro.cabal` sets `-T -M2G` and every
figure here is taken at the default 4 MB nursery — a gap [the floor
section][floor] prices on one shape and Run 14's pair is built to price
over the table.

The `-O2` one is a probe. `-fspec-constr` is no longer: Run 8 is a full recorded
run in that regime, and the flag therefore goes before the `--` of every command
of the sequence rather than being reached for once. A run whose numbers
are meant to be kept and written into this file is a different undertaking,
and has a procedure of its own: [Making a major benchmark
run](#making-a-major-benchmark-run).


### Making a major benchmark run

A *major run* is the whole roster over the whole shape set at criterion's
default budget — the main set and, by default, **every stride-class population
with it**: one process for the main set and one per class, or two of each where
the run is paired, in the order of the sequence below. Asking for a major run
asks for all of them; leaving a population out is an explicit exception
to be stated, not a choice this page leaves open. The whole is analysed
and written into this file. What follows is the procedure, and it is written
to outlive any one run.

**What asking for a run asks for, since the request is one sentence and the work
is this chapter.** The whole of it, without coming back for permission between
the steps: the pre-run checks, the sequence, the write-up, and the probes
the results turn out to justify. The procedure is the permission — each step
names what it needs and what it must not do — so a question this chapter answers
is not a reason to stop. **Two parties appear below and this page keeps them
apart.** *A session* is whoever executes the run, here as in the twenty-odd
other places this page says it. *Whoever asked for the run* holds the decisions
a procedure cannot make, and is never called *the author*: that word means
the session writing a block — the one whose prose an independent checker is set
against — and it is the executor, not the requester.

**A probe budget rides with it, and it is spent AFTER the write-up rather
than before.** It is separate from the pre-registered questions, which
are appended after the classes and were designed before the evening. What
this ordering is for: the write-up is where a run's errors are made, it is done
last, and a probe spent first is spent out of its attention — Run 14 probed
heavily and well, and shipped twenty-one prose errors past four green checkers
because the writing came at the end of it. Allow up to about two hours
of measurement the run's own *results* make worthwhile: a discriminating reading
of a cell that came out strange, a derivation over the artifacts while they
still exist. Spend it while they do, most of it being unspendable afterwards,
and propose rather than take anything beyond it.

**Stop for two things.** No further progress — a build that will not build,
a gate that fails, evidence that is not on this machine — and a decision
that belongs to whoever asked for the run rather than to the procedure: whether
the artifacts go, whether anything is pushed, which pair the next run takes,
anything that publishes. Report those and wait; decide the rest.

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
that changes what you do belongs in a list — if you find one that is not,
that is the defect, not your reading. And a rule's evidence goes at the end
of its paragraph, as a date and an outcome — never inside an instruction,
and never as a chronology.

    cd ~/r/orthotope/micro-regime3        # and re-set R and REGIME per call
    #      R=runNN; REGIME=-fspec-constr -- an EMPTY regime is a plain -O1
    #      build and nothing downstream notices. That hazard is 3b's
    #      alone: REGIME reaches the build and nothing else, so on the
    #      CONFIRM path nothing reads it and setting it buys nothing.
    #      Governing docs are this
    #      file and read-run.py's docstring; horde-ad's CLAUDE.md is not
    cat $R-pair.txt                       # 0. the note: six steps quote it,
    #      four here and two in the run list -- the halves' roles, the
    #      md5s, the commit, the gate line.
    #      BASIS/OTHER come from it, never from a half's name, and are set
    #      in one place in each of the four scripts that take a run --
    #      run-major.sh, run-gate.sh, smoke-sweep.sh and install-tables.sh,
    #      the last carrying BASIS alone: make all four match, and override
    #      by environment when reading an older pair whose basis differs.
    #      The basis runs second, and both halves run the classes
    ls $R-*                               # 1. is there a pair? A note-only
    #      listing is the answer NO: step 3b writes the note first, so this
    #      is never empty on a run that has reached here
    md5sum $R-<basis> $R-<other>          # 2. is it the note's pair?
    git log -1 --format=%h -- :/micro-regime3/Main.hs   # 3. has it moved?
    git diff <note's commit> HEAD -- :/micro-regime3/Main.hs  # comment-only?
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
    #  1-3 ARE THE FORK, and the two branches have names this file uses
    #  elsewhere. Missing or moved sends you down the BUILD path: 3b and
    #  the two --survey lines, and nothing else. Matching sends you down
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
    #      Every build wants -fforce-recomp and a fresh --builddir, cabal
    #      answering "Up to date" for a -pgma or an environment change;
    #      --ghc-options="$REGIME" stays quoted, and a value with a space
    #      needs inner quotes besides,
    #      --ghc-options='"-with-rtsopts=-I0 -T -M8G"'. Build the halves
    #      back to back with nothing touched between -- about twenty
    #      seconds each here, the dependencies being in the store and only
    #      the local package recompiled -- keep both executables, delete
    #      each --builddir once its binary is copied out, and read the
    #      pair's variable straight out of each
    #      with the note's own `strings` line before trusting either.
    #      Then transcribe into the note what only the build can say: the
    #      Main.hs commit it was built from, the two md5s, .text and the
    #      fills -- the fill-in block is that transcription, and steps 2,
    #      3, 9b and 10 are all reading it back
    ./$R-<basis> check > /tmp/a.log 2>&1  # 4. every shape agrees
    ./$R-<other> check > /tmp/b.log 2>&1  # 5. and the other half
    cmp /tmp/a.log /tmp/b.log             #    byte-identical, or STOP
    #      scratch names, spelled in full: a $R-*.log here makes
    #      run-major.sh refuse hours later, and $TMPDIR is unset unsandboxed
    ./$R-<basis> --list 2>/dev/null | wc -l    # 6. roster size, then the
    diff <(./$R-<basis> --list 2>/dev/null) <(./$R-<other> --list 2>/dev/null)
    #      two halves' listings: identical is what one source built twice
    #      looks like, and the pair note asks for that half of it
    ./read-run.py --lint                  # 7. roster and shape annotations
    ./read-run.py --check-doc --quiet     # 8. anchors, paths, widths, sweeps
    #      7+8 are the WHOLE document check here; no other repo's checkers,
    #      now or at post-run step 7. Exit code is the verdict: the
    #      note: worklists are write-up material, only FAIL: stops you, and
    #      a wrap FAIL means a HAND-wrapped paragraph, not a long one
    #      --quiet keeps the FAILs and withholds the worklists by count.
    #      Every call but one takes it; the one that does not is post-run
    #      step 7, where the worklists are read and adjudicated
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
    #      near-total same-offset agreement is what a sound pair looks
    #      like -- but only `--library` PRINTS an agreement figure. The
    #      plain form lists each binary's own fills and leaves the
    #      comparison to the eye, which is a reading and not a verdict:
    #      what a sound pair shows there is the same fills at the same
    #      addresses in both sections. A note's nm-based figure is a
    #      different number again, so compare like with like.
    ./loop-offsets.py --survey $R-<basis>       #    on the BUILD path,
    ./loop-offsets.py --survey $R-<other>       #    never the confirm one,
    #      and the answer goes in the note: it is the binary's, not the
    #      reading session's. What it means is below, at the pad
    ./smoke-sweep.sh $R                   # 11. the smoke sweep, and read
    #      its counting: it holds each process to the arm count `--list`
    #      gives for that shape
    ./$R-<basis> -L1 --json smoke-l1-main.json         # 12. the roster
    ./$R-<basis> classes scaled- -L1 --json smoke-l1-scaled.json  # pass,
    #      ONLY if `--list` changed membership AND the pair note records
    #      none -- it belongs to the pair as the gate does, so grep the
    #      note before paying the twenty minutes. Any class serves, every
    #      one being three shapes since 2026-08-14 -- prefer one of the
    #      five that crossed from two, which drives `--block`'s
    #      three-shape branch. Name the artifacts smoke*, never $R-* -- any
    #      $R-*.json/.log makes run-major.sh refuse, only $R-gate-* exempt.
    #      Record it on an `L1 ROSTER PASS:` line. With the previous run's
    #      binary gone, membership is compared against the roster delta
    #      under Provenance
    #  11 and 12 here, and 14 in the run list below, all belong to the
    #      PAIR: on passing, write each into $R-pair.txt, or the next
    #      session repays the hour
    #  that is the preparation, and none of it wants a quiet machine. What
    #      does is the run list below, which starts on an explicit
    #      go-ahead and never on a session's own reading of the box

**Then the run — and this is the list that wants the machine, so it does
not start on a session's judgement.** Steps 13 to 17 sit here rather
than with the preparation above because the evening runs through them: 14 spends
the machine and 16 reads it, while 13, 15 and 17 cost nothing and are here
because they decide whether 14 happens and what it is for. The gate is forty
minutes and the sequence is most of an evening, and both want the desktop
to itself. **The free three are free — run them.** The go-ahead is owed before
14 and 16, not before a grep, and a rule read as covering everything below
the line is a rule read loosely everywhere. **Have an explicit go-ahead before
starting anything below, every time — the request for the run is one — and never
infer one from a quiet machine.** No `uptime` or `ps` is run at this point,
and neither would settle it if it were: what they cannot see is what their owner
is about to want the machine for. The `ps` at step 16 is an alarm and
not a permission — it runs after the go-ahead and before the longest stretch,
so a machine that got busy since stops the run short of the hours rather
than after them. Unsandboxed throughout:

    grep -i gate $R-pair.txt              # 13. has the gate run and passed?
    #      read UP: the newest GATE: line is the script's own "reading still
    #      to do"; the hand-written verdict sits above it. An md5-identical
    #      rebuild inherits the gate; any real one needs its own
    ./run-gate.sh $R                      # 14. only if 13 says it has not
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
    #      predictions -- and READ `What Run N compares against` besides,
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
    #  17. read ahead while the sequence runs, which costs no machine time
    #      and is what the write-up needs first: the last run's chapter,
    #      the open list, and the replace list under Provenance
    ./run-major.sh $R &                   # many processes, several hours
    ps -eo pid,etime,comm | grep $R-      # confirm from an UNSANDBOXED ps:
    #      comm, not args, and comm truncates at 15 characters. A blocked
    #      write leaves a launch that never happened looking like one in
    #      progress, which is how two copies once ran at once
    #      do NOT wait with pgrep -f, which self-matches and never returns;
    #      the sequence ENDS WITHOUT ANNOUNCING ITSELF, so arrange to be
    #      woken by `major run complete` in $R-wallclock.log rather than
    #      deciding to look: six hours of idle machine followed a session
    #      that read this line as where to look and set nothing watching
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

Steps 6 to 10 are read-only and fine sandboxed; 3b, 11, 12 and 14 write
and are not, and so do 4 and 5 — only through their redirect, but
that is enough, the sandbox permitting the session's own directory
and `/tmp/claude`, and `/tmp/a.log` being in neither. Send those two logs
somewhere the sandbox allows, or run them unsandboxed with the rest. Step 16
answers less than it looks: `ps` in a session lists only that session's own
processes, so it catches a launch made from here and not one made from anywhere
else, and `uptime` is the half of it that reaches the machine. The one
that is skipped most often is 8, and the one that is run when it should
not be is 14 — the gate belongs to the pair, so a note recording a pass means
it is done. **And what is true of 14 is true of 11 and 12: write each
into the pair note when it passes.** All three cost machine time, all three
are properties of the pair and its roster rather than of the session that ran
them, and a session that cannot see they were run pays for them again — twenty
minutes for the roster pass, about forty for the gate. The note is the only
thing that outlives a session, so an outcome recorded nowhere is an outcome
nobody after you can use; the gate's own line has said so all along,
and the other two now say it too.

**Steps 7 and 8 are the whole of this page's document check, and no other
repository's checkers belong on it.** Theirs carry a per-repo configuration —
search roots, an owned module namespace, an allowlist — so pointed here they
resolve this directory's names in their own tree and report correct names
as missing, which is the noise-for-signal failure that stops a checker being
read at all. Said here rather than beside the verification pass it governs
because a session starts in another repository and arrives
with that repository's standing checks already resident, so the moment to know
this is the moment the checklist reaches these two steps. If a future document
here does grow `file:line` citations, that is the moment to port one,
and not before.

**Where the effort actually goes, because it is not where it looks.** The run
is several hours and *unattended* — a process sitting far longer
than its neighbours is worth looking at rather than waiting on, and what says
how long each should take is the previous run's `-wallclock.log`, which stamps
every start and finish; it costs patience and a quiet machine, nothing else.
Everything expensive happens after it, in the write-up, and that is where
a session's token budget is spent and where its mistakes are made. **The eight
class blocks are the bulk of the typing**, and mostly mechanical: write each
from the verdicts `--block` emits rather than from the table above them, keep
each to one paragraph, and expect them to take longer than the main set's
write-up did. **The bulk of the *cost* is adjudication rather than typing** —
deciding which run, which basis and which population a figure belongs to —
and it scales with how many comparisons the run invites rather than with how
many tables it fills, so a run that is both a repetition and a pairing
is the dearest to write up for that reason alone. **The shape to expect,
in the units a session actually spends**, which are not hours but tool calls
and how much of this file must be read before the first one. The fixed cost
is the reading — this chapter and the last run's — and it is larger
than executing either checklist, which is what both checklists are for. After
it the work divides three ways and only one part is large. *Batchable*: anything
with one invocation per process or per claim — a `--selftest` and an `--aa`
apiece, the dozen-odd `--pair` lines, a `--block` per class — goes in one call
per kind, so steps 1 and 3 together are a handful. *One per site*: the eleven
`--in-place` installs, three calls. *Unbatchable*: the prose, one edit per
paragraph, and this is the bulk — the eight class blocks alone are some thirty
items, and no tool reduces the count, `--block`'s skeletons only removing
the extraction that used to precede each. Then verification costs about what
the prose cost, because every finding is a fix and every fix is a claim. Budget
the prose and the verification as the work; the readings are noise beside them,
and the run itself is unattended. Two further consequences worth having in mind
before starting. Prefer analysis that localises — per shape, per control —
over re-quoting figures that moved a few percent and changed nothing; the first
is where the surprises have come from and the second is what has gone stale
twice. And **a probe is not a lesser instrument than a major run —
and the write-up is where the instruments get built**, which is the sharper form
of the same point. Run 13's registered question came back a null,
and its durable output was four instruments: two checks in the reader and two
rules in this chapter, every one of them from a mistake made while writing up
rather than from anything the run measured. So the write-up
is an instrument-building phase and not only a reporting one, and the three
things worth watching for are the computation you improvised, the check
that would have caught the error, and the step you skipped — that trio
is the run's other product, and it outlives the figures, which the next run
replaces. On the original point: the measurements that closed the `sum-only`
objection, established that the forcing term scales, and settled the floor's
mechanism cost twenty minutes and, for the latter two, no extra machine time
at all, while the major run they hang off changed no decision. A question
with a discriminating measurement usually deserves a filtered run now rather
than a slot in the next full one.

**What a run must read, so that nothing else is read to find out.**
This chapter, and of the rest only what the write-up replaces: the last run's
chapter, [What Run N compares against](#what-run-15-compares-against), [the
claims](#the-claims-run-15-should-test), [the class
blocks](#the-stride-classes-run-by-run) and [Provenance](#provenance). The open
list is read by its status markers rather than end to end. Everything else
in this file is reference, and reading it is how a write-up's budget goes
without a figure to show for it.

**Where.** A session starts in `~/r/horde-ad`, which leaves *that* repository's
`CLAUDE.md` resident while this repo is not governed by it, even though all
generalizable preferences apply; read this file and `read-run.py`'s docstring
instead, orthotope carrying no `CLAUDE.md` of its own. Then:

    cd ~/r/orthotope/micro-regime3

**The run's two variables come first**, because everything below uses them
and a shell that has not set them will silently do the wrong thing: an empty
`$REGIME` is a -O1 build that every gate here passes. It reaches the *build*
and nothing else — no check mode takes a regime, and
on the confirm-don't-rebuild path nothing consumes it at all.

    R=run10                              # names every artifact; no default
    REGIME=-fspec-constr                 # every run since Run 8; empty for -O1
    #  and the pair's halves are $R-<basis> and $R-<other> throughout, here
    #  as in the checklist: which is which is what the pair note records and
    #  what no half's name tells you, so no command below spells one out

**And in a session they will not survive to the next command.** Each tool call
gets a fresh shell, so a `cd` and an assignment made in one are gone
by the next, and the commands below are spread over a dozen of them — which
is to say the shell this warning is about is the ordinary one here,
not a careless one. Inline the two literals into every command, or re-set them
at the head of each:
`cd ~/r/orthotope/micro-regime3 && R=run10 REGIME=-fspec-constr && …`. The two
do not fail alike, which is the reason to spell this out rather than trust care.
`./run-major.sh $R` with `$R` empty is loud, the driver refusing without a name.
A build with `--ghc-options="$REGIME"` empty is not: it degrades to a plain -O1
build, which is exactly the silent wrong thing the paragraph above describes
and nothing downstream detects.

`$REGIME` is the bare GHC flag and not a `--ghc-options=` spelling of it,
because a recipe composes it with a `-pgma` of its own and each wants
an `--ghc-options=` of its own. Its value begins with a dash, so it goes inside
the quotes — `--ghc-options="$REGIME"` — and never as a bare word after a space,
which the option's parser reads as the next flag.

**Everything below that writes runs unsandboxed**, which is every step
that builds, benchmarks or leaves a file: the two builds, the smoke block,
`run-gate.sh`, `run-major.sh`. The read-only ones — both `check`s, `diag`,
`--lint`, `--check-doc`, `loop-offsets.py`, `--list`, a `grep` of the note —
are fine sandboxed and are worth having cheap, so this is not a blanket
instruction to drop the sandbox for the afternoon. A session starts
in `~/r/horde-ad`, so its sandbox permits writes there and to its own temp
directory and nowhere else; this directory is outside it, and `run-major.sh`
moves here before doing anything. Sandboxed, every `--json` and every
`> $out.log` is refused — and the two refusals do not look alike. A redirection
on a simple command is checked before exec, so the benchmark never starts
at all, while `log`'s `tee` is a pipeline whose `echo` still prints: you get
the sequence's start lines on the console, no wall-clock file, no JSON
and no run. That reads as a run in progress, which is how two copies once ended
up on this machine at the same time. Confirm a launch by an unsandboxed process
list, never by the launching shell.

**So never write `$TMPDIR` in this directory; spell the scratch path in full.**
That variable is set only under the sandbox, so the same idiom that works
in a read-only check writes to `/` the moment you add the flag that makes
a command able to write at all — silently, since the write succeeds. The fact
is in the session-level notes and was resident when this bit: what defeats
it is that the rule is conditional on a property of the *call*, which changes
call to call here, while `$TMPDIR/x` is a habit that does not. A directory where
half the commands must be unsandboxed is one where the conditional should
not exist, which is why this is a rule about the place rather than a caution
about the variable.

**Then build what will actually be timed — but first, is there a pair here
already?** That is the fork, and it comes before the build rather than after it,
because a rebuild replaces both halves: the offsets the predictions
are registered against are the present pair's, and one coming out even slightly
different would retire them in silence. Where the binaries and the note
recording what they were built from are already there, confirm them instead
of rebuilding.

The fork's three questions are answerable in three commands, none of which
the page should make you invent. Is there a pair — `ls $R-*`. Is it the pair
the note describes — `md5sum $R-<basis> $R-<other>` against its two `md5` lines.
Has the source moved under it —
`git log -1 --format=%h -- :/micro-regime3/Main.hs` against the commit the note
records for `Main.hs`, which is the one that command returns; where the note
records two, the other is the tree it was built in and is not what
this compares. **Expect it to differ, and read the diff before believing it**:
step 8 below sends the write-up into `Main.hs`'s comments and forbids rebuilding
for it, so a comment-only move is the normal state after every run,
and `git diff <note's commit> HEAD -- :/micro-regime3/Main.hs` is what tells
it from a real one — the `:/` prefix in both, since a bare `-- Main.hs`
from the repo root prints nothing and exits 0. The regime is the fourth
and is not answerable this way, the JSON recording no compiler flag; the `diag`
step below is what answers it.

Only where there is no pair, or where `Main.hs` or the regime has moved since
the note was written, is a build the thing to do — and there is nothing here
that does it. Every pair since Run 11 is two shims, and each half is one
`cabal build` from the recipe its note carries: the regime, a `-pgma` shim
of its own, whatever variable the pair exists to price, and `-fforce-recomp`
with a fresh `--builddir`, without which cabal answers *Up to date*
for a `-pgma` or an environment change and relinks the previous object — which
is how a shim change comes to be measured against itself. Write the note first,
since it is the only copy of both recipes, and read the pair afterwards:

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
`cabal build micro ${REGIME:+--ghc-options=$REGIME}` is still for is a probe —
a filtered handful of benches answering one question — and those are run
with `cabal run micro ${REGIME:+--ghc-options=$REGIME} --`, never through
the sequence below.

**Before spending the hours**, the cheap checks — the first three against
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

**The exit code is the verdict; the `note:` lines are not.** A clean
`--check-doc` here still prints them, each heading an indented list running
to dozens of entries — every superseded figure, every superlative, every
absolute time the page quotes, and every link into the run chapter from standing
prose, listed for adjudication during the write-up and not before it.
**`--check-doc --quiet` is that sentence made operative**: it prints the `FAIL:`
lines and one line counting what it withheld, and every call takes
it but post-run step 7's, which is where the worklists are read. `--lint`
is the same, noting the rostered arms it knows are deliberately untimed. Both
exit 0 when they pass, and a `FAIL:` line is the only thing that should stop you
at this point. **One of those `ok:` lines is the wrap check, and it reads
differently mid-edit.** It asks its question per paragraph rather than
of the whole file, so a paragraph an edit left on one line is reported
as mid-edit and not failed, and a `FAIL:` there means a paragraph wrapped
by *hand* — neither the formatter's form nor one line. The gate therefore stays
green on a document being worked on, which is what stops it demanding
a `wrap80 -i` between edits: wrapping is owed before committing, not before
checking.

Both halves. On the unaligned/aligned pairs this page used to build, only one
half had its own code rewritten — the other's shim appended dead bytes, where
`align-as.py` moves labels about — but on a pair of two shims, which every pair
since Run 11 has been, both can be mispadded and both need it, so checking both
is the rule and the one-sided case is the exception that no longer arises.
The halves are held to each other besides — a sound pair makes the two logs
byte-identical, agreement on every shape being a property of the strategies
and not of where their loops landed. A difference stops the run, and the rebuild
goes through the recipe in that pair's note. The two lines above cost seconds.

**Then confirm the regime is the one intended**, which nothing later can:

    ./$R-<basis> diag

and read one row of it — the allocated bytes of `baseOffsetsScan` against
`baseOffsetsMut` on `vgg-14-c512`, which is a `diag` label rather than a shape
and so will not be found in the shape set. They are equal to three figures
under SpecConstr and ten times apart at plain -O1, a separation no eye misreads,
and both ends of it are measured (2026-08-08), the flag being the only thing
that moves them. Seconds either way — on the build path, the seconds after
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
of the session confirming it — offsets at 0 are what a fully padded half shows
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
of removing — which is not hypothetical, `list`'s own loop being library code
(prediction 5). Padding the unaligned half to the same size *and phase* closed
it: 95% of the library loops at the same cache-line offset and 98% in the same
straddle state, the rest of the delta being 384 bytes, six whole lines. Matching
the size alone does not do it — that left the delta at 416, which is 32 mod 64
and so the worst shift available — and the two-step that does
is in `align-as.py`'s docstring, beside the `PAD_BYTES` it feeds. **A pair
of two shims has no such step and no such guarantee**, only whatever its two
recipes give it, which is why `./loop-offsets.py --library` exists: it reports
what share of the library self-loops the two halves put at the same offset
in their line, and near-total agreement is what a sound pair looks like. A note
may record the same property the other way round, off `nm` symbol by symbol,
which is the stronger reading and not this tool's output — so compare like
with like, or read the note's own figure as the note's. So the pair now differs
in Main's loop alignment and in nothing else an offset can see,
and `micro-unaligned` keeps every offset the unpadded build had: the same fills
at [3, 53, 59, 45] and [16, 0, 36, 36], the same 115 short loops with 50
straddling.

**Which two halves a pair has is a property of the pair, not of this page.**
The names are recorded in the pair note and set in one place in each of the four
scripts that take a run — `run-major.sh`, `run-gate.sh`, `smoke-sweep.sh`
and `install-tables.sh`, the last carrying `BASIS` alone — as `OTHER`
and `BASIS`, and each is a `${BASIS:-…}` default an environment variable
overrides for an older pair; the basis is the half the expected bench counts
are read from and every table is installed from, and it runs second; both halves
run every class. **The two roles are BASIS and CONTROL**, which is what
this page calls them where it names a role at all; the scripts' variable
is `OTHER` and the prose often says *the other half*, and all three are one
thing. The halves are named for what they vary — Run 10's `unaligned`/`aligned`,
Run 11's `maxskip`/`aligned`, Run 12's `maxskip`/`maxskippa` — and which of them
is the basis is a decision the pair note records, not something a half's name
tells you. Run 12 is where the two would collide if this page still called
the basis *the aligned half*: its control is `maxskippa`, the half that carries
`-fproc-alignment=64` and so is the more aligned build of the two. Where
a sentence below says *aligned* it is about alignment, not about a role; where
it is plainly about one past pair — as the paragraph on the 12 KB of `.text` is,
every figure in it being Run 10's — it keeps that pair's half names.

**Name the artifacts by half, and drive every `--in-place` from the basis
half.** The sequence below builds every filename off `$R`, which a paired run
has to split: one `$R-<half>-main.json` per half, and the class files
`$R-<basis>-$c.json`, there being no others — the infix being the binary's own
name, so an artifact cannot be traced to the wrong half. **One scheme covers
everything a run leaves**, the binaries and the pair note with the JSONs:
`$R-<rest>`, the run first and nothing before it, which is what stops two runs
writing one filename. Binaries from Run 11 and earlier were named for the half
alone (`micro-aligned`, `micro-unaligned`), which is what this page's history
calls them. **All three installing modes come from the basis**: `--markdown`,
`--fingerprint` and `--block` alike, so the page carries one basis and not one
per half, and what the other half contributes is the `--compare` and a yardstick
column. Run 10 is the one run that answered otherwise, its Results table coming
from the unaligned half while its fingerprint and its class blocks came
from the aligned one — a split it needed because its aligned half was the first
here and had no predecessor to succeed. That ended with Run 11: **the basis half
is the table and the other half is the control**, whatever the control is built
to price.

**What the other half is for**, since a run that publishes no table from it will
otherwise be asked why it spends an hour building and timing it. That depends
on which half it is, and the pair is chosen for it. An *unaligned* control
is the layout one, the per-arm term being measured afresh each run rather
than inherited, and it is the yardstick for GHC itself: the native backend
aligns no loop today ([the floor section][floor]), and when that is fixed
the same pairing is what prices how well GHC does it against the assembler shim
here — a comparison no single build can make. Run 11's *max-skip* counterpart
prices the shim's own padding instead, its two halves differing in which loop
heads get a directive and in nothing else, so its arms separate what alignment
buys from what the NOPs cost.

**The pairing doubles the classes too.** Both halves run the main set, since
that is where the per-arm comparison lives, and both now run every class
as well. The rule it replaces ran the eight class populations on the basis
alone, on the argument that a class block is read for the ordering inside
its own population and the basis is where that ordering is legible — true,
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
the *benchmark* while nothing exercises the *reader* until hours later —
at `-L1`, since the smoke tests the reader's code paths, not its statistics:

    ./smoke-sweep.sh $R

It runs three `-L1` processes — one main-set shape from each half and one class
from the basis — then every reader mode over what they wrote, then the three
`--in-place` installers into a copy of this file, and deletes all of it. About
two minutes. It uses binaries already built rather than `cabal run`, which would
build a third in whatever regime the shell happens to carry; it exercises
the reader rather than the regime either way. **It is a driver, for the reason
`run-major.sh` is one:** it counts, holding each process to the arm count
`--list` gives for that shape. The reason it is not *also* still printed here
is the one this page learned the hard way the same day — a pasted copy
of a driver's sequence drifts from the driver and nothing checks it, which
is what the class loop above had done.

**What this proves and what it does not**, since it reads like a verification
of the installs and is not one: it proves each installer found its table
and wrote something, and `cmp` fails loudly if the copy came out identical,
which is the case where one silently found nothing. It does not prove the right
rows went to the right place — that guarantee lives in `install`, which matches
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
**Each install is smoked from the half it will really come from** — all three
from the basis half, `--markdown` and `--fingerprint` off the main-set JSON
and `--block` off the class one — which is why these are three commands
and not a loop. The write-up is hours too late to find a broken installer.

The first runs every timed arm on one shape and puts the whole analysis path —
the correction, the controls, the table generator — through its paces; the third
does the same for the `classes` plumbing, the reader's per-list shape rules
and the six-column class table, on the class whose rule is least trivial.
Those two go through every single-file mode, because they take different paths
through the reader from the population line onwards, and the lines after them
add the modifiers a write-up reaches for — `--brief` on `--aa` and `--block`,
and the filters `--no-controls`, `--exclude` and `--exclude-shape` — because
a mode that passes bare can still die under the flag it is really given.
A reader broken by a roster or shape-list change fails here in minutes instead
of after the run.

The second file exists for `--compare`, which no single file can reach:
it is the reader's only two-run mode and the one a paired run is read with,
so leaving it out of the sweep would leave the pairing's own instrument untested
until the write-up. It is also the only point before the evening at which
the *other* half writes a JSON at all — the basis half writes the first file —
and a pair whose halves turn out not to be comparable has cost the hours twice.

**Run every mode, not the interesting ones.** The loop above is written
as a loop because a partial sweep has already missed a real break: after
the trim came out, `--pair` and `--aa` both died on a name that a removal had
taken with it, while `check`, `--lint`, `--check-doc` and `--selftest` all
passed — the failure lived in the two modes nobody had thought to run. Modes
are cheap to run and expensive to be missing, and the run artifact is the only
thing that can reproduce one, so sweep before deleting it rather than after.

**After a roster change, add a `-L1` pass over the main set and one three-shape
class**, which is about twenty minutes and reaches three things a one-shape
smoke cannot. `--selftest` skips a whole block on one shape and says so —
winsorizing, the six A/A identities and the baseline identity, none of which
is an identity of anything until there are shapes to be one over. Every claim's
`--pair` line goes unrun, and a claim re-aimed at an arm the run does not carry
fails only when someone runs it. And `--block`'s per-shape line is guarded
by `len(shapes) > 2`, so it is dead on a one-shape file — a guard that hid
an edited line of this reader through a whole smoke sweep. Every class
is three-shape since 2026-08-14, so any of them serves; the list above prefers
one of the five that crossed from two, which drives `--block`'s three-shape
branch, and `scaled` is the one it names. The pass is two processes:

    ./$R-<basis> -L1 --json smoke-l1-main.json
    ./$R-<basis> classes scaled- -L1 --json smoke-l1-scaled.json

Its numbers go nowhere: `-L1` is a rougher budget than any recorded run's,
and this pass is a test of the reader, not a measurement. **And like the gate,
it belongs to the pair rather than to the session that ran it**, so
it is recorded in `$R-pair.txt` and read there before it is paid for,
on an `L1 ROSTER PASS:` line. Grep the note first; a second session owes
the twenty minutes only if none is recorded. **Name its artifacts `smoke*`
and not `$R-*`**, which is not tidiness: `run-major.sh` refuses to start where
`$R-*.json` or `$R-*.log` exists, excluding only `$R-gate-`,
so a `$R-l1-main.json` left beside the pair reads as a previous attempt
and refuses the very run this pass was run to clear. `smoke*.json` is outside
that glob and inside `.gitignore` already.

**"Roster change" here means membership, and the test is `--list`**:
the binary's listing differs from what the previous run's did, in its set
of names rather than their order. Criterion emits it sorted, so an arm moving
slot cannot produce a false positive — which is the only thing making the test
sound and is worth knowing, since order *is* a change, of the kind
[Provenance](#provenance) deals with rather than this pass. An edit
to the reader or to a claim is not a roster change either, though the three
reasons above are worded in their terms because a roster change is the only
thing that has ever broken them. What the test cannot usually do is run itself:
the previous run's binary is deleted and its listing recorded nowhere,
so the comparison is against the roster delta under [Provenance](#provenance) —
look before taking that route, since a pair whose artifacts have
not been offered for deletion yet is still on disk and answers directly, which
is kept for exactly this. A run whose basis half *is* the previous run's binary,
as Run 11's is, answers it outright instead, and the pair note records the count
on both sides. Spelled out because two readings of this paragraph have split
on it: with membership unmoved the pass is not owed however much else changed,
and Run 10 is such a run.

**A paired run has one gate more, and the first thing to do about it is read
rather than run it. The gate belongs to the pair, not to the session**, which
is what stops it being paid for twice. A pair's note, `$R-pair.txt`, is written
by hand beside the binaries — every name in this directory carries the run,
so that two runs cannot write one filename however alike their half names are —
and it carries both recipes, what was verified, and a `GATE:` line saying it has
not been run; `run-gate.sh` appends to that file. So read what the note says
about the gate first — `grep -i gate $R-pair.txt`, this pair's note
and not every note in the directory, case-insensitive and not anchored
on the `GATE:` token, because a note written by hand says it in prose
and grepping for the token finds nothing in one, which reads as *no gate*
and costs the hour it was meant to save. **Read the whole output and
not its last line, and the newest `GATE:` line is not the verdict**:
`run-gate.sh` appends its mechanical block last and closes by asking
for a reading, so on every gated pair the newest `GATE:` line is the script's
and says the reading is still to do, while the verdict — written by hand, above
it — is the older one. Read up the output until a `GATE:` line states
an outcome; that is the verdict, whatever sits below it. Following *newest wins*
here costs the forty minutes the step exists to save, which is how it was found.
If a verdict records a pass, this step is already done and the next action
is the run itself. A rebuild that comes out md5-identical inherits the gate,
and one that does not — a changed `Main.hs`, a changed regime — needs its own.
Re-running it on a pair that has already passed costs a quiet forty minutes
and can only reproduce what the note says.

**If that line says the gate has not run**, it is the last thing before
the evening — but it is not part of the preparation, and *get the run ready*
does not license it. The gate spends forty minutes of quiet machine, so it lives
in the run list behind the go-ahead with the sequence itself. `run-gate.sh`
takes five benches over the shape set from each half, twice each,
in a palindrome — control, basis, basis, control — so that drift over the hour
cannot read as a difference between the binaries, which is the part a person
retyping the command would drop:

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
which this page claimed until a run measured it. Its selection carries `build`
and `mut-odo`, which are two of the three widest-spread arms in the roster —
the placement-sensitive pair [the floor section][floor] is written about —
so the term between its two passes runs past the drift band a movement is asked
to clear, and a magnitude read off a gate is not evidence. Whether a five-bench
process is *also* noisier than a full one is not separable from this with one
process per binary, so the reason to distrust the figure is the selection, which
is known. And the two passes disagreeing is not a second opinion about
the binaries: their ratio is algebraically the ratio of the two same-binary
readings, so a palindrome that fails to converge is reporting its own noise.
Read the gate for soundness, and take every magnitude off the run. What
the script writes back into the note is the mechanical half alone — four exit
codes and four bench counts — because that is what it knows; whether the pair
is sound is the reading's verdict and is written there by hand — **above**
the script's block, where reading up from the end meets it first,
and the `GATE: not yet run` line goes in the same edit, since a reader reading
up would otherwise meet that one and stop. What the predictions are is in [the
open list](#what-is-open) with the rest of the run's registrations; what
the gate read is in the note, written by hand above the script's mechanical
block. **The gate also answers one question that is not a reading at all: has
the machine changed?** `run-gate.sh` runs
`./read-run.py $R-gate-<basis>-a.json --machine` after its four processes
and puts the answer in the note. It holds `list`'s net per call, shape by shape,
to the fingerprint this page keeps, so the last run's absolutes are on the page
long after its JSONs are offered for deletion and nothing has to be kept for it;
the gate's own selection carries `*/list` and both `sum-only` halves on every
shape, which is what makes the comparison net against net. It gates the geomean
rather than a cell, at a threshold the mode's own docstring derives from every
kept process this page has. When it fires the gate fails with it, and the thing
to do is not to read the code: **ask whether the box changed** — a kernel,
a microcode update, a BIOS setting, a thermal state, a different machine — none
of which a run can see from inside itself. It re-baselines by itself, each
write-up replacing the fingerprint it reads.

**The run** is one sequence — the main set from each binary the run has,
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
is not optional there. A run made in the wrong regime is not detectably wrong —
the roster, the shapes, the gates and the reader all pass, the JSON records
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
    # An option whose VALUE contains a SPACE wants inner quotes besides --
    # --ghc-options='"-with-rtsopts=-I0 -T -M8G"' -- cabal splitting on
    # whitespace otherwise, which for that flag dies loudly on `-T` and, if
    # repeated once per word instead, builds a binary carrying the LAST
    # -with-rtsopts alone. Measured 2026-08-13, setting up Run 13's pair.
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
an interrupted sequence a hand job — expect that, since the machine gets wanted
back.** The guard is right (relaunching overwrites hours in place), but it has
no resume, so finishing a sequence whose main sets landed and whose classes did
not means running the class loop yourself: the `for c in ...` half
of the sequence above, both halves inside it,
an `[ -e "$out.json" ] && continue` before each so a population that already ran
is skipped rather than redone, and its `benchmarking` count checked against
`classes --list` as the driver does. Stamp each into the same
`$R-wallclock.log`, so the run's own record stays one file, and say
in the write-up that the populations ran in more than one window — one process
per population is what makes that harmless, each carrying its own controls
and gates, but it is a fact about the run and the chapter states it.

What it adds over pasting the sequence is the counting: every process's bench
count is checked against what the roster holds, so a selection that silently
caught the wrong set is loud in the log at once instead of at the write-up —
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
is the literal that remains, so the drift the other way — a class the binary has
that `CLASSES` does not name — is refused before the run rather than reported
during it: it would otherwise run nowhere, print nothing and leave no artifact,
which is measured and not feared. Neither builds anything, and both refuse
to start without the pair. The sequence:

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
to stderr as it finishes — roster size, shape count, wall clock and the two heap
peaks — so a document quoting its scale copies a measured number rather
than counting benches by hand, and so `micro.cabal`'s `-M2G` headroom claim has
a current source; the stderr redirect above is what keeps it. In a class process
every part of that line is its own but the shape count, which is fixed before
criterion selects and so names the whole class set.

**Check what a filtered selection actually selected.** Criterion takes one
`-m MODE` and then its patterns positionally, so `-m glob A -m glob B` matches
*nothing* and the process exits at once — which looks exactly like a fast run
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
list](#what-is-open) with its measurement written — a twin in a named slot,
a filtered A/B — is appended after the classes and answered the same day,
pre-registered rather than improvised. What this does not cover is the run's own
surprises, which need the run read first; those become that list's next entries,
each with the probe that would settle it.

**The time budget is always criterion's default.** Raising `-L` would buy
samples for the slowest shapes — they bottom out around 6 where the fastest get
130 — but at a proportional cost in wall clock, and the runs are already hours.
Every recorded run therefore uses the default, so figures stay comparable
between runs and the sample counts in the tables mean the same thing throughout.
Where that leaves a shape thinly measured, the `smp` and `CI%` columns say
so rather than the budget hiding it.

Expect several hours for the sequence, so run it in the background — and **run
nothing else on this machine while it does**. Unsandboxed, and confirmed
from a process list rather than from the launching shell, which a blocked write
leaves lying:

    ./run-major.sh $R &               # its own wall-clock log is the record
    ps -eo pid,etime,comm | grep $R-  # comm, NOT args: under args the
                                      #   launching shell matches its own
                                      #   command line. comm truncates at 15
                                      #   characters, which a `runNN-` name
                                      #   of nine more exactly fills -- past
                                      #   that a half is cut and missed

`pgrep -f`/`pkill -f` self-match here and an `until ! pgrep -f …` waiter
therefore never returns; watch `$R-wallclock.log` for `major run complete`
instead. Every strategy of a population shares that population's process
precisely so its figures are commensurable, and the [noise floor][floor] section
is the measured evidence that they move with what shares that process. What
the rest of the machine does on top of that is unmeasured, and a recorded run
is the wrong place to find out. The session's own hands stay off the machine
and the tree alike until the sequence ends — the script's git lines
are the binary's provenance, and an edit under a running sequence falsifies them
— while reading ahead costs nothing: the last run's chapter and the open list
are what the write-up is about to need.

The wall-clock file is why the script stamps each process: a criterion log
is timestamped only at the end, so without the window there is no way to say
which shapes an intrusion exposed, and a suspicious cell can then be neither
blamed on it nor cleared of it. The exit codes ride along because a class
process that dies mid-sequence otherwise leaves a truncated JSON behind a green
scroll-back. Run 6 (-O1) had three short greps in its first minutes
and the exposure was settled from the cell data instead — the anomalies
were strategy-intrinsic, not a time window
([R2](#r2-is-the-ramp-detector-not-the-noise-detector)) — but that worked only
because the suspects sat at one roster slot on two shapes, which is luck
and not a method.

**The run's registered predictions** ([the open list][open]) say what this run
was for and what would kill each one, and are read while the sequence is still
ahead of you — checklist step 15, which is where their reading is placed. Record
their verdicts there rather than in the run's own chapter, which the next run
replaces. **An empty registration does not hold the run.** Where a run has none,
note the absence and read the outcome against its queue entry instead. What
is not open is registering afterwards: the point of the list is that it predates
the hours, so the choice here is to register before the evening or to do
without. **And say what a partial outcome is**: a prediction registered
over several arms can come apart, and neither "held" nor "refuted" is then true
— Run 10's first was stated over three arms and one confirmed it while two met
its own kill condition. Report that as a split, name which arms went which way,
and carry the consequence for each separately; the temptation is to round
it to whichever answer the majority of arms gives, which loses the finding.

**After it lands**, in this order:

**The post-run half as a list, for the same reason the pre-run half has one.**
Its twelve steps below are the prose's own numbers, so a reference to step 7.7
still lands; the prose is where the reasons live and is not replaced by this.
What it replaces is reading the twelve paragraphs three times to be sure nothing
was missed, which is what they have cost.

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
    #      logged loudly and is not fatal, so nothing else stops on it
    #   2. match bases before reading any ratio -- same population, same
    #      restriction, the basis the claim was stated on
    ./read-run.py RUN.json --claims                   # 3. every claim's
    #      ordering and registered verdict in one call, in the claims
    #      section's own order -- and, after them, the page's own verdict
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
    #   5. rename the FOUR run-numbered headings: the chapter head and
    #      `Recommended tasks after Run N` take THIS run, while `What Run N
    #      compares against` and `The claims Run N should test` look
    #      forward and take the NEXT. The tasks heading is the one a count
    #      of three left behind, its content coming from the replace list
    #      while its title and anchor come from here. Repoint every
    #      link -- its TEXT as well as its anchor, the check seeing only the
    #      second -- and Main.hs's own README.md# references with them.
    #      Repointing is not re-verifying: walk the standing-prose links
    #      into the chapter, which --check-doc lists, against what the
    #      chapter still says
    ./install-tables.sh $R                            # (7.4) install, never
    #      paste: --markdown, --fingerprint, a --block per class and
    #      --claims, eleven tables and a reading per claim, all from the
    #      BASIS half. Take the movement reading BEFORE this: the claims
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
    #      The independent checker is TWO passes on one agent, tables when
    #      they go in and prose when written, briefed that it works in this
    #      directory, that its evidence is this run's JSONs and read-run.py,
    #      and that no other repo's checkers come near this page.
    #      Once the write-up settles, one comprehension probe: a fresh
    #      session answers a few of the page's own questions from the
    #      document alone, with citations
    ./read-run.py --lint          # 8. again after ANY Main.hs edit, and
    #      never rebuild the pair to satisfy it: say in the write-up that
    #      the comment-only move happened
    #   9. record the run's name and regime, each process's stderr line,
    #      the machine, and THE COMMIT, transcribed from $R-pair.txt; also
    #      which half ran first. A class line's shape count is the whole
    #      class-view set, so the population size comes from the reader
    #  10. walk the open list: grep the settled index before adding an
    #      entry, move answered ones with their measurement, and add each
    #      surprise with what would settle it. Prediction verdicts go THERE,
    #      not in the chapter the next run replaces; report a split as a
    #      split, arm by arm
    #  11. spend the load-independent measurements while the artifacts live
    #      -- allocation, Core, a `size` invocation, minutes each. Owed by
    #      every paired run: rebuild each recipe with -g3 and export the
    #      NAMED fills into the note, matching groups by byte identity of
    #      the loop body, never by proximity
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



1. **Gate every population on the correction, before reading any figure —
   and read the A/A *worst cell*, not only the pair's geomean.** A control
   that passes its gate can still be the run's most informative measurement:
   `bq-expand`'s distant twin passed on Run 8 and again on Run 9 while carrying
   a 41% cell, published both times as a noise floor, and chasing that one cell
   is what produced the roster fix and the nursery account [in the floor
   section][floor]. A pair inside the floor whose worst cell is an order
   of magnitude outside it is not noise; it is a finding the aggregate
   is hiding. The gates themselves: `--selftest` checks that the forcing term
   scales with `l` — one pass over the elements, not something whose size varies
   with the shape — and `--aa` prints both whether the two `sum-only` halves
   agree and how the term compares with the same pass measured in situ, off
   the `-nosum` arms. The three are independent and the correction needs all
   of them: position, size, and the read itself, each blind to what the others
   catch ([sum-only](#sum-only-and-the-correction-now-applied)). Any of them
   failing invalidates the whole time column rather than merely leaving
   it uncorrected, and all have to be re-passed by every run rather
   than inherited — by every *population* too, each process carrying its own
   `sum-only` pair, its own six A/A controls and its own two `-nosum` arms,
   so a class run passes or fails the gates on its own evidence and a failure
   there invalidates that class's column and no other. **Then write this run's
   own floor at the head of the chapter as you draft it, and keep it there.**
   That is where every margin judged against it is written too, so
   it is published with them rather than kept where only this session can see
   it. Every margin below is judged against it, it is re-measured each run,
   and the runs have disagreed several-fold, so the previous run's figure
   is the one you will reach for by habit and it is the wrong one. `--aa` prints
   each pair's raw ratio and `f` beside the net one for a related reason:
   the net figure is the floor between two published rows, the raw one is how
   much an arm disagrees with itself, and quoting the first as the second
   overstates it by 1/(1-f).
2. **Match bases before reading any ratio.** The first act of a comparison
   is making its two sides one basis — the same population, the same
   restriction, the basis a claim was stated on — and only then reading figures.
   Run 7's first claim check ran on its 24 shapes against claims stated on 22,
   and every pair had to be re-run.
3. Analyse with `./read-run.py`, which is where every table in this file comes
   from — read [the reader's own section](#the-reader-read-runpy) first, and do
   not write another reader. **The claims are part of this and are the thing
   these steps are likeliest to leave out**: the run chapter names three things
   a run reads, and the claims section is the third, each of its orderings
   carried in `--claims` with its registered expectation, so that a run
   transcribes printed verdicts rather than re-deriving the table. The class
   properties are the same job three times a population, off the verdicts
   `--block` emits, and the set is restated for the next run on this run's basis
   while the readings are still in front of you. **A paired run's own mode
   is `--compare`, and its direction is a convention worth stating**: the run
   given first is the one the ratios are *of*, the `--compare` argument being
   what they are divided by, so `basis --compare control` puts a figure below 1
   where the basis is faster — for Run 10, whose control was unaligned,
   that was where alignment was faster. Prediction 4's per-arm term
   and the aligned half's published column both read that way round; reversed,
   every one of them inverts and nothing in the output says so.
4. **One JSON at a time, never merged.** The reader takes one file,
   and its geomean is that file's population — the main set's or one class's.
   Every mode names that population in its first line, `--selftest` fails a file
   spanning two and `--markdown` declines to emit a table for one, so a merged
   run is caught rather than published. The class tables stand beside the main
   geomean, per [the ruling](#the-stride-classes-and-what-they-cover), and there
   is no combined figure to compute, so a sentence comparing populations
   compares their tables.
5. **Rename the four run-numbered headings, which do not all take the same
   number** — the chapter head and *Recommended tasks after Run N* go
   from the last run to this one, being about the run just read, while *What Run
   N compares against* and *The claims Run N should test* look forward and go
   from this run to the next, so a write-up of Run 10 leaves the four reading
   10, 10, 11 and 11. Repoint every link to them. All four are named here
   because a heading governed only by the closing index is how a heading comes
   to name a run two chapters old. It is mechanical, it is easy to forget
   because nothing in the numbers asks for it, and `--check-doc` catches
   the fallout as dead anchors rather than as the rename it was: Run 9 left
   eleven. Repointing is not re-verifying: a standing-prose link
   into the chapter promises content the replacement may have moved out, so walk
   the links `--check-doc` lists and check each against what the chapter now
   says — the five that decayed this way kept resolving through two renames.
6. Walk the list under [Provenance](#provenance) of what the new numbers
   replace, and do not trust it to be complete: re-run the two sweeps it names
   and map each hit to the bullet covering it, since running the sweeps
   is not the same as reading them, and the list has been wrong before.
   **Replace; do not annotate.** Walking a list of what to replace makes "now X,
   where it was Y" the natural sentence, and a superseded number has to earn
   its place by the test in the user-scope `CLAUDE.md` — would someone redo
   the work without it — which most do not meet; `--check-doc` lists the ones
   already here for adjudication. And a figure that moved *inside* the floor
   is requoted without comment — only a movement past the floor earns
   a sentence.
7. **Verify the write-up before deleting anything.** These are the checks
   the procedure used to leave to judgement, each of which has caught something.

   **This step is the whole of the document verification a run owes, and nothing
   else is to be reached for. Four passes, in this order:** run
   `./read-run.py --lint` and `--check-doc` — **without `--quiet`, this being
   the one call that reads the worklists rather than the verdict** — whose exit
   codes are the verdict; read the worklists they print and adjudicate each
   entry; read the write-up end to end against the run's own artifacts; and hand
   the diff to an independent checker, which the paragraph after next briefs.
   None of them is optional, the third is the one that keeps finding real
   errors, and the fourth is what catches what the third cannot see in its own
   writing.

   **And where the write-up was made by scripted replacement rather
   than by `Edit`, one mechanical read comes before those four.** Unwrap both
   sides and diff them — `wrap80 --unwrap` over the committed version
   and over the working one — and read that diff for text that left without
   a replacement arriving. A scripted rewrite fails in two shapes and neither
   is a wrong figure. Anchored on a *prefix*, it replaces the whole paragraph
   and drops whatever followed the part its author had read; `--check-doc`
   catches that one, every prose paragraph being required to end a sentence.
   Anchored on two *markers*, it deletes every paragraph between them, however
   many that turns out to be — and nothing catches it: the survivors still end
   sentences, the anchors still resolve, the figures still match, and every
   check here is a predicate over what is **present**, so none can see what
   is gone. Measured on 2026-08-14, when a paragraph recording that the regime
   had been confirmed in the binary was removed from this file and `--lint`,
   `--check-doc` and the truncation check all exited 0. So assert the extent
   in the script, echo what it is about to overwrite, and read the unwrapped
   diff afterwards, which is the only place a lost paragraph shows.

   **A correction is a claim, and is written under exactly the conditions
   that produce bad ones.** Whatever the verification turns up gets fixed
   at the end of a long write-up, at speed, and the fix is a new assertion
   with no derivation behind it unless one is made: Run 13 corrected
   its allocation reading twice and the second correction was wrong, having
   been computed from a rounded print. Derive a fix the way the sentence
   it replaces should have been derived, and re-run the gates after it.

   **Expect every error to be in the prose and none in the numbers, and expect
   the green checkers to be why.** Run 11 shipped six, and not one was a wrong
   figure out of the reader: four superlatives asserted without sorting
   the population they quantify over, one sentence contradicting its own
   paragraph three lines later, and one percentage computed from a published
   table instead of from the cells. `--lint`, `--check-doc`, `--selftest`
   and `--aa` were green throughout and right to be — they check
   the measurements, and the measurements were sound. The hazard is that green
   instruments make the remaining gap feel small when the remaining gap is where
   all of it lives.

   A write-up is a document edit, so the three-pass discipline applies —
   but its passes live here, in this repo's own instruments,
   and the general-purpose form of it does not fit a page whose claims
   are *measurements* rather than statements about code. Pass 1, which resolves
   `file:line` citations and pinned permalinks, has no subject: this page cites
   no line and no permalink, deliberately, and what it does cite — arm names,
   strategy names, shape names, `Main.hs` functions — is what `--lint` checks,
   which a line number could not, a citation surviving the refactor that moves
   it. Pass 2 is `--check-doc`'s path check. Pass 3 is the reading, below.
   The heading-scope and cross-reference passes are `--check-doc`'s anchor
   and replace-list coverage checks. No other repository's checkers belong
   on this page, for the reason given with the pre-run checklist, where
   a session meets these two tools first.

   **What the instruments cannot supply is the reading, and the reading
   is the pass.** What the tools print is its output and not its method:
   `--check-doc`'s three sweeps hand you a worklist of superseded figures,
   superlatives and absolute times, and adjudicating that list is not reading
   the document. Nor is inheriting one — a worklist you did not derive verifies
   somebody else's findings while telling you nothing about what else is wrong,
   which is the completeness question the reading exists to answer. Run 11
   is the case above: every checker green and the worklist adjudicated while six
   errors stood. **So put an independent checker on the diff against
   the artifacts, launched when the tables go in rather than at the end** —
   and it is **two passes on one agent**, since at that moment only the tables
   exist: the tables as they go in, the prose when the prose is written,
   the second continuing the first rather than paying a fresh bootstrap. Run
   13's first pass verified 341 table lines and found the cross-class summary
   untouched; its second found six prose errors, including a previous run's
   figure presented as this one's. One agent, briefed to recompute every added
   figure from the reader and to re-derive every *only*, *largest* and *N
   of the nine* by sorting, and to report discrepancies rather than opinions.
   It is dear per finding — Run 11's cost some thirty times what the same
   session's own targeted re-checks did — and it is worth it anyway, because
   its findings are the ones a session has already proved it cannot see
   in its own prose, and because it returns a completeness the author cannot:
   306 of 306 table rows verified rather than the ones somebody thought
   to check. Launch it early, keep it to one, and leave the placement,
   contradiction and writing-rule reading to yourself. Three things it cannot
   derive go in the brief: that it works in this directory, that its evidence
   is this run's own JSONs and `read-run.py`, and that no other repository's
   checkers come near this page — it starts where your session started,
   so the artifacts are not where it is and the checkers it arrives with
   are not this page's. And once the write-up has settled, aim the same
   instrument at the finished page rather than the diff: a comprehension probe —
   a fresh session answering a handful of the page's own questions
   from the document alone, with citations — reads as a stranger what every
   diff-scoped check reads as a change, and its one run so far (2026-08-14, six
   questions, all answered) surfaced a contradiction between two standing
   passages that nothing above could have seen. (The rule that a check must
   be proven able to fail governs the instruments themselves and is stated
   with them, [in the reader's section](#the-reader-read-runpy).)

   The checks themselves:
   1. **derive every count and ratio in the prose from `--cells`, never by eye,
      and never from a published table** — the second half is the one that looks
      safe: a table prints three significant figures because that is what
      a reader needs, so arithmetic on its cells is arithmetic on the rounding.
      Run 11 computed its eleven anchor movements from the printed anchors
      and put the largest at +4.1% where the cells say +4.3%, which is a tenth
      of the figure and was invisible until an independent reader rebuilt it.
      A percentage, a ratio and a count all come from `--cells`
      or from `--pair`, whatever is printed three lines above — and for a class
      paragraph, from the verdicts `--block` now emits under its per-shape line,
      which state the three properties' outcomes and name the arms that actually
      lead. That block exists because this rule kept losing to the table being
      right there while the paragraph was written: three of Run 9's class
      sentences were wrong that way and no mechanical check saw any of them. "32
      of 33", "30th of its 33 shapes", "the only two past 7%" are all claims
      a glance at a sorted table gets wrong; two of Run 6's were wrong until
      recomputed. Two shapes of claim need naming because counting is not what
      they look like. **Every *only*, *largest*, *fastest* or *never* is a claim
      about the whole table** and is derived by sorting it, not by looking
      at the arms the sentence is about: Run 8's write-up carried four such —
      "the only arm the flag demotes", "the largest gain of any arm" among them
      — each false, and each caught late or by a reader. And **a ratio between
      two published cells comes from `--pair`, never from dividing the printed
      figures**, which are rounded to three digits: the same write-up quoted
      0.9898 for a pair the reader puts at 0.9946. **And `--cells` is a print
      too**, its `alloc_mult` carrying four decimals, so a question finer
      than what it prints wants the mode that answers it rather than a script
      over the dump: allocation agreement is `--compare --alloc`, which exists
      because a script over the printed multiple found every cell agreeing where
      the underlying fit does not. **Before re-deriving a figure a previous run
      published, re-derive that run's own value first and check it reproduces.**
      This is the prove-a-search-non-vacuous rule applied to a derivation rather
      than a grep — run the computation against a case whose answer is known
      before trusting it on one whose answer is not — and it is cheap: one extra
      invocation. Run 13's write-up skipped it, read the wrong column, got
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
      *and* system — never user alone**: the inherited "wall and user time agree
      on it" is a property of the workload it was written for, and where the RTS
      does kernel work they part completely, which is how 0.36 ms per call
      of system time went unseen and a real 10% effect was reported as zero.
      And **difference at two scales**: if the per-call figure moves with `n`,
      part of what is being divided is a fixed cost, which is how a one-time 0.9
      s of page-faulting read as half a millisecond a call;
   3. **when two instruments disagree, that is the finding.** Do not average
      them, pick the one the page prefers, or quietly drop the awkward one.
      Locate the disagreement first: the criterion slope and the `-n`
      differencing above parted by 8 points on one arm, both reproducible
      to a fraction of a percent, and the cause was neither sampling nor sample
      size but which clock was being read. Until it is located, neither number
      is evidence, and a retraction made on the strength of the wrong one
      is worse than the claim it withdrew;
   4. **install the tables with `--in-place` rather than pasting them.**
      `--markdown`, `--fingerprint`, `--block` and `--claims` each take it —
      the last installing a `Readings:` paragraph under each claim's lead rather
      than a table — and each refuses rather than guessing: the match
      is by whole line, the count is asserted, and a class table is narrowed
      by its block's bolded lead. Hand-pasting is what this replaces,
      and the reason is on the record — the cross-class summary's header
      is written out twice, once indented as the spec that fixes the columns,
      and a session locating the table by searching for that text put Run 8's
      rows under the spec and left Run 7's table standing, with every check
      green because the check looked it up the same way. If you paste by hand
      anyway, do not edit the table: it renders the same rows the terminal does,
      and carries `needs` and the emphasis forward from the table already there.
      `--aa` and `--block` both take `--brief`, which drops the standing
      explanation and the table `--in-place` installs anyway, costing
      no computed figure; across a run's processes that is several hundred lines
      you have already read. Its stderr is the whole of what is left by hand:
      a row new to the roster comes out with `?`, a departed row is dropped
      with a warning. Run 9 had ten such rows and filled them from a note
      written here before the run, which is the practice to repeat whenever
      a roster change is known in advance — the cell then gets transcribed
      rather than invented at the end of a long day. Each class JSON emits
      its own table the same way and is pasted the same way, into its block
      in [The stride classes, run by run](#the-stride-classes-run-by-run);
      those come out six columns wide, `needs` being a property of a strategy
      rather than of a population and so stated in the main table alone.
      The per-shape fingerprint is pasted the same way, whole,
      from `--fingerprint`;
   5. **assemble the cross-class summary last, from the tables and not
      from the JSONs.** Every cell of it appears in one of the class tables
      above it, so it is a transcription and is checked as one — cell against
      table, each in turn — where recomputing it from the runs would be a second
      derivation able to disagree with the tables it summarises. **Each class's
      `--block` now checks its own row** and names the cell on stderr,
      so `install-tables.sh` reports a wrong transcription among what it leaves
      you; the table stays hand-assembled because its emphasis is a judgement
      no reader can derive, and the marks have already drifted between runs;
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
      That the checkers here are good is itself the hazard — green instruments
      make the remaining gap feel small, and the gap is exactly where they do
      not look, so read for placement, for *only* and *largest*, and for which
      run and basis each figure belongs to. This is the pass that keeps finding
      real errors;

   Three conventions this page holds to, each of which exists because breaking
   it has cost something here. **A figure in prose names its run, its basis
   and its population, or it belongs in a table with the prose pointing
   at it** — a bare numeral carries no provenance, and that is how one sentence
   came to put a Failed Run 6 figure beside a Run 6 one, and another to compare
   a *published* ratio with a *paired* one. The population is the newest way
   to make that mistake and the easiest, a class figure and a main-set one being
   the same kind of number over different shapes. **An anchor longer than about
   thirty characters goes reference-style**, defined at the foot of the file:
   inline it overflows the width and the rewrapping that follows is pure churn.
   And **a link's text names its subject, never its position** — five links
   reading *the head of the run chapter* kept resolving through two renames
   while the content they promised left the chapter, a decay no anchor check
   sees, which is why `--check-doc` lists standing-prose links into the run
   chapter and the rename step re-verifies them;
8. Re-run `--lint` after editing `Main.hs`, even when only comments changed:
   the reader parses that file for the roster and the shape dims, so a comment
   edit can break a check that passed before it. `--lint` reads the source
   and needs no build, which is the whole of what that reason asks for. **Do
   not rebuild the pair to satisfy this step.** Steps 6 and 7.7 send you
   into `Main.hs`'s comments on purpose, and a rebuild would replace both halves
   and want a fresh note stamped with today's date and commit — which
   is the file the next step transcribes the binary's provenance out of.
   A comment edit after the run leaves the timed binaries correct and the source
   they were built from moved by a comment; say so in the write-up rather
   than rebuilding to hide it;
9. Record beside the numbers the run's name and regime, each process's stderr
   provenance line, which machine, **and the commit the binary was built
   from** — for a paired run, transcribed from `<prefix>-pair.txt`, which
   carries the commit, the regime, the GHC and both md5s because this step asks
   for them and the note outlives the session that built the pair (the JSONs do
   not survive, so the source is the only thing that makes a run reproducible
   even in principle — this page's figures are one desktop's and
   are not portable, see [Provenance](#provenance)). A class process's line
   is measured for its elapsed time and its two heap peaks but not for its shape
   count: that count is fixed before criterion does the selecting, so it reads
   every class view rather than the population that ran, and the population's
   own size comes from the reader's first line;
10. **Walk the open list against what this session actually did**, which nothing
    checks. **Grep [the settled index][settled] before adding an entry**,
    not only before deriving: a question is easy to open against something
    already answered in a section you are not writing in, which is how Run 10's
    write-up proposed a Core dump that had been taken three times and whose
    answer — `vBuildVS` surviving as no top-level binding, so there is no call
    path to dump — was recorded at the ceiling, a thousand lines from where
    the entry was being written. A run answers some of its own questions
    and a write-up raises others, and both go stale in place: Run 8 answered
    the element-type entry with the probe that entry specified and left
    it standing open, and answered the packed-arm entry the same day. Move what
    was answered into the answered block with its measurement, leave what
    a probe narrowed as narrowed, and add the run's surprises
    with the measurement that would settle each.
11. **Spend the load-independent measurements before the artifacts go.**
    Allocation is deterministic per call, Core is a compile, and a binary's size
    is a `size` invocation — none of them wants a quiet machine or a run slot,
    and each is minutes. Run 8 stopped at the write-up and left a Core diff,
    a two-regime `diag` and a code-size figure undone; all three were done
    later, two of them changed rulings, and one answered an open question
    outright. So before step 12, take every question on the open list whose
    measurement is a compile, an allocation or an arithmetic re-derivation,
    and take it now. **One of them is owed by every paired run and is named here
    so it is not rediscovered: export the pair's NAMED fills into its note.**
    `loop-offsets.py` names a copy only in a `-g3` build, so each half's recipe
    is rebuilt with `-g3` added and the twin's groups matched to the timed ones
    by byte identity of the loop body — never by proximity or by which group
    sorts first. Bare offsets are what the note records otherwise, and the map
    is a property of the binary: once the binaries go, no offset this page
    quotes can ever be tied to an arm again. Run 12's were derived this way
    on the last day they existed and refuted two accounts of its own split; Run
    10's and Run 11's are gone unnamed. What is left over is the timing work,
    which is what a quiet machine is for.
12. **Only then, offer the artifacts for deletion — once — and abide
    by the answer.** The JSONs, the logs and the wall-clock file, and
    for a paired run the two binaries and their `$R-pair.txt` with them,
    that note being about a pair and worth little once the pair is gone.
    **Offering is the step; deleting is not**, and the offer is made after
    the verification above is done and presented, not after the writing — Run
    6's artifact went as soon as its write-up was drafted, which cost
    the ability to re-check anything needing the raw samples when that write-up
    was later questioned.

    **They are not required to go, and this page no longer says they are.**
    The rule used to be that the normal state of this directory is no run
    artifact at all; what justified it was that the numbers live in this file
    and the fingerprint exists precisely so a per-shape record outlives its run.
    Both remain true, and neither makes deletion *owed*: what they actually
    argue is that nothing is *lost* by deleting, which is a licence and
    not an obligation. What is lost by deleting early is concrete and has
    been paid twice — every `--pair` a later question wants, every per-shape
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


### The reader: read-run.py

Every figure below comes out of `read-run.py` in this directory, and the table
above is *emitted* by it rather than copied from it. **Use it; do not write
another reader.** The definitions it encodes — which cells the column caps,
that `CI%` is a mean half-width rather than a bound, that `alloc` needs an `l`
the JSON does not carry (it parses `Main.hs` for it), that the `*-aa-*`,
`sum-only*` and `*-nosum` rows are controls, that every ratio is net
of the forcing pass while every other column is raw — each cost a session
to settle, and an ad-hoc script gets them subtly wrong. Its docstring
is the reference for all of them; extend the script rather than starting over.

    ./read-run.py RUN.json                  # roster, then the strategy table
    ./read-run.py RUN.json --markdown       # that table as README markdown
    ./read-run.py RUN.json --shapes         # per shape: CI% max / median / mean
    ./read-run.py RUN.json --aa             # controls, spans, in-situ term
    ./read-run.py RUN.json --pair A B       # two arms, paired, with an interval
    ./read-run.py A.json --compare B.json   # one arm across two runs
    ./read-run.py A.json --compare B.json --alloc  # what each arm allocates
    ./read-run.py A.json --compare B.json --chapter  # the chapter's figures
    ./read-run.py RUN.json --claims         # every claim's verdict, one call
    #      then the page's verdict figures read back: what reproduces these
    #      readings, and what is neither theirs nor attributed to a run
    ./read-run.py RUN.json --cells          # every cell as TSV, for the rest
    ./read-run.py RUN.json --fingerprint    # the kept per-shape record
    ./read-run.py RUN.json --block          # a class block's parts, + verdicts
    ./read-run.py RUN.json --markdown --in-place   # install it, do not paste
    ./read-run.py RUN.json --selftest       # check the reader's own invariants
    ./read-run.py RUN.json --exclude concat-runs --exclude-shape deep-7-c512-k3
    ./read-run.py --lint                    # Main.hs's roster and shape
                                            # annotations, against README
                                            # and against itself
    ./read-run.py --para 'the floor is'     # the paragraphs whose bolded
                                            # lead matches, and their lines

**Anything this reader can emit, a session should not read.** It is why
no write-up has ever read a table row out of this file: `--markdown`,
`--fingerprint` and `--block` emit those rows and `--in-place` installs them,
so three hundred-odd cells are never carried through a context that does
not need them. `--claims --in-place` extended that from rows to prose,
the readings under each claim being the reader's sentence and not the author's.
`--para` is the same trick for prose — the alternative is a `grep -n` paired
with a `sed -n` for every passage wanted, both of which go stale the moment
an edit above moves the lines, which every install and every fix does. The rule
generalises: when a session finds itself reading this page to get at something
the reader could compute or locate, that is a mode missing rather than a page
to read harder.

Every mode's first line names the run's **population** — the main set or one
[stride class](#the-stride-classes-and-what-they-cover) — which the reader works
out from the shape lists in `Main.hs`. It is the one property of a run
that no column shows and every figure depends on, so `--selftest` fails a file
spanning two populations and `--markdown` emits no table for one: a geomean
over two of them is a statistic of neither.

`--pair` compares two arms **shape by shape**, and it is the right way
to compare any two: a strategy's ratio to `list` spans six-fold across the shape
set, so an unpaired comparison of two table columns fights that spread, while
`A_s/B_s` does not — both arms move together with the shape. `list` cancels out
of it too, so a paired figure owes nothing to the baseline. It prints the paired
geomean, a bootstrap interval, the win count and its sign test,
and the published-column ratio beside them, those last two answering different
questions. **Reach for it instead of writing a script.** Every paired figure
this page quotes was once recomputed by hand and thrown away, which is how one
came to be printed beside a figure from a different run.

The interval wants multiplying before it is believed, and `--aa` says by how
much: the A/A pairs are the only comparisons whose true answer is known
to be exactly 1, so they are the only place an interval can be held
to an answer. `--aa` reports whether each covers 1 and how its half-width
compares with the spread the pairs actually show, which turns the floor
from a threshold someone chose into a factor a run measured. Read that factor
as an order of magnitude: it rests on six pairs.

`--markdown` renders the same rows the plain table does, from one shared call,
so the published figures cannot drift from the terminal's. It reads the Results
table already in this file for the one column a run cannot know — `needs` —
and for which rows the prose emphasises, carries those forward, and says
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
finds no match and survives — so one arm silently leaves the run and criterion
reports nothing wrong. That cost a placement probe its whole point once, the arm
dropped being the only one the probe was about. The general guard is to count
what a filtered run selected before reading it ([the
procedure](#making-a-major-benchmark-run)), which catches this
and the repeated-`-m` mistake alike.

The second takes seconds and still exercises the reader; a one-shape run says
so. A filtered run like it carries no `sum-only` bench, so its figures
are uncorrected and not comparable to the tables here — the reader warns
on stderr when that is what it is reading. A run's JSONs go when its questions
are answered and the offer to delete them is accepted, so whether a table here
can be re-derived depends on what is still in the directory; the next run
replaces it either way.

`--lint` needs no run JSON at all, which is this directory's usual state.
It reads `roster` out of `Main.hs` — the one list both the benchmark and `check`
are built from — and asks the four things about it that go stale silently:
is every arm named somewhere in this file; is every strategy defined
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
— which for a class list is after that population's process has finished, hours
past the point where the check is worth anything.

And a sixth about a second file: do `Probe.hs`'s six copied shapes still match
the dims `Main.hs` gives those names. The probe is a separate program
and its shapes are copies (its header says why), so this is the one thing
standing between a transposed dim there and a probe measuring a shape it still
names after — which is not hypothetical, three of the six being wrong when they
were first written and named by this check.

The question it used to ask second — is every benchmarked strategy also held
to the reference by `check`? — is gone, and deliberately. The roster
and the agreement chain were two hand-written lists of the same strategies,
and that check compared them; one list now builds both, so the drift cannot
happen rather than being merely detectable. A check that cannot fail is a silent
search, so it was replaced rather than kept.

That is the standing rule for everything under `--lint`, `--selftest`,
`--check-doc` and the `health` warnings, and it is why each carries a recorded
proof in its docstring: **a new check is not finished until it has been made
to fail on purpose**, with what was broken and what it then said written down
beside it. Several here can only fail on data no real run produces — a forcing
term larger than the cell it is subtracted from, a term that does not scale
with `l` — so provoking them is the only way to know they are wired to anything.
It reaches a pass run *by hand* too, which has the same failure and no exit
status to hint at it: before calling one clean, break something it ought
to catch and confirm it says so. And it reaches a check's every *branch*:
the path check's absent-sibling arm is exercised by pointing its roots
at a directory that does not exist, since a branch no control reaches
is a silent search whatever the checks around it do.

`--selftest` checks invariants of whatever run it is given: that the dims
it parses out of `Main.hs` match that file's own `l` annotations, that every
cell has a positive slope and a sane R², that the forcing term is positive
on every shape and leaves every cell's net positive, that the same term scales
with `l` as one pass over the elements must, that every row's winsorized geomean
covers all shapes and lands inside its own per-shape range, that `list` against
itself is 1, and that an A/A pair with no capped cell has its published ratio
equal to its paired one. The one thing it still cannot reach — that `sInner`
is the second-to-last listed dim — it now names as `check`'s rather
than as nobody's. It names what it could not exercise rather than passing
silently, and exits 2 when the run file is absent. That last invariant
is a finding: the A/A ratios in the noise-floor table are geomeans over every
shape, so a published ratio is the paired one whenever neither arm had a cell
capped. `--aa` prints both and `--selftest` asserts the identity where it holds.


### What moves a figure when no strategy changed

Eighteen A/A controls run an existing strategy twice under a second name — nine
strategies, each duplicated once beside its base and once at a distance,
so position varies within a strategy and strategy within a position.
The `offtab` and `bq-odo-gm-mulback` pairs, added 2026-08-14 for the coverage
gap the wild-cell entry names and for the spread instrument's widest arm,
and the `build`, `mut-odo`, `list` and `gen-unsafe` pairs added the same day —
the placement-sensitive pair that carries Run 14's own control, the denominator
every ratio divides by, and the one wide arm flat against every shape dimension
— are first read in Run 14, so the table below is Run 13's six. They
are the only rows whose true ratio is known to be exactly 1 — or were, until
[the mutable ceiling](#the-mutable-ceiling-not-taken) turned up another
by accident:

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
figure above equals its paired one — the identity the winsorized estimator
bought and `--selftest` asserts — and the published column is the yardstick
for comparing two rows of the Results table, while a margin measured per shape
still belongs against the paired figures `read-run.py --aa` prints. Two spans
moved by one against Run 12's, the roster having gained an arm between
the distant twins and their bases.

**On Run 14 the floor is 2.19% on the basis half and 4.02% on the control,
and the population it is measured over changed underneath it.** Twelve A/A twins
landed after Run 13, taking the pairs from six to eighteen, and the new ones sit
on the roster's widest-spread arms — `build`'s adjacent pair carries the basis
figure and `mut-odo`'s the control one, where every earlier run's floor came off
the tight arms alone. Read on Run 13's six the same run gives 0.29% and 0.16%,
so **the threshold did not move and the instrument widened**: a run quoting
this run's figure against a predecessor's is comparing two populations, not two
machines. The threshold this run supports is therefore two figures — *three
tenths of a percent between any two rows of the table* on the six-pair basis,
which is what carries across runs, and two and a fifth on the control — where
Run 12 supported 0.35% and 0.24%, Run 11 a quarter of a percent on its max-skip
half and 1.21% on the other, Run 10 1.00% unaligned and 0.54% aligned, Run 9
under 0.1% with a wild cell, Run 8 0.5% and Run 7 nearly 4%. Runs disagreeing
several-fold on the floor is itself the caution, and halves of one pair
disagreeing twofold is the same caution one level down: read the floor
as the run's *and the half's*, re-measured every time, not as a constant
of the harness.

**The twins have now taken every side available, which is what a sign this weak
is worth.** Run 10 read all six pairs above 1 on its unaligned half and five
of six above on its aligned one, the twin slower than its base, and called
it worth a sentence and not a mechanism. Run 11 read all six *below* 1
on that same aligned binary and five of six above on the max-skip one. Run 12
split both halves, three of six above on the basis and four on the flag half.
Run 13 splits both halves evenly — three of six above 1 in each — which is again
the arrangement a fair coin gives. Three strategies at two positions each
are not six independent draws, and the direction is evidently not a property
of the code, the layout or the roster order, all of which were held fixed across
the flips.

Those six pairs' bootstrap intervals are half-widths of 0.05-0.61% and their
`CI%` column reads 0.03-0.11%, so the interval still understates run-to-run
variability: it measures sampling error *within* one benchmark, while two
separately placed benchmarks also differ in code layout, cache occupancy
and inherited GC state. The A/A is the only column that sees that, and `--aa`
prints the calibration outright — on Run 14, a median interval half-width
of 0.67% against an observed spread of 2.19% on the basis half, a factor
of **3**, and 0.35% against 4.02% on the control, a factor of **12** —
so multiply any interval this reader prints by about that before believing it,
where Run 12 wanted one either way, Run 11 one on its max-skip half and three
on its aligned one, Run 10 four and one, Run 9 nine, Run 8 two and Run 7 three.
That the two halves now disagree on the factor, where Run 12's agreed, is
not a wild cell this time — neither half has one — but the same
`bq-scan-rem-gm-mulback` distant pair reading twice as far from 1 on the control
as on the basis. It rests on six pairs, and one loose pair moves it.

**The class populations are where the factor still bites**, and the reason
is arithmetic rather than noise: a two- or three-shape bootstrap gives
an interval far narrower than the spread those shapes actually show,
so `reshape1` reads a median half-width of 0.23% against a spread of 2.74% —
a factor of twelve — and three of its six intervals cover 1. The run's largest
is `scaled`, at 0.10% against 5.47%, a factor of fifty-five, with two of six
covering: that population's standing slot is what the spread is, so the factor
is reporting the slot rather than the reader's arithmetic. Read a class interval
that misses 1 as the reader's arithmetic and the pair's own deviation
as the finding; the per-class factors are with each block below.

**And what is left when every other cause is pinned has now been measured:
run-to-run drift is a few percent per cell and a quarter of a percent
on a geomean.** Run 11 re-ran Run 10's aligned binary with shapes, roster, order
and regime unchanged — the repetition this page had wanted since Run 9 —
so its every movement is drift and nothing else. `list`'s per-shape scatter
is **0.958 to 1.043**; of 762 cells, 495 are within 1%, 693 within 5% and 743
within 10%; every arm's geomean is within 1.5% but `mut-odo`'s 1.0327.
That is the figure to hold a *later* margin against, and it is a quarter
of the 0.902-to-1.181 band Run 10 had to quote when the roster order moved
the layout underneath it. Two consequences worth keeping when the run chapter
carrying them is replaced: a margin of a few percent between two runs is still
not evidence, and a margin under about 1.2% between two *arms* of one run
is not either, which is the A/A floor above and a different quantity.
The exceptions are `build` and `mut-odo`, one worker at two slots, whose cells
reach 1.25 and 1.16 with their loops at offset 0 in both runs — the residue
the pairing cannot reach, and [the open list][open]'s.

**And a busy machine has now been measured rather than only avoided, which
is what says the wild cell is not one.** Run 11's sequence was launched twice;
the first attempt's max-skip main set completed before it was stopped,
on a machine that turned out not to be quiet, and its artifact was read against
the recorded one — the same binary, the same roster, an hour apart — before
being deleted with the rest. The disturbance is **diffuse**: the floor rises
from 0.22% to **1.11%**, **50 of 762 cells** run more than 5% slow,
and the worst of them are scattered over four shapes and eight arms (`build`
on `cnn-L2-24x24-c32` 1.161, `bq-odo-gm-mulback` on `stretch-square-1341` 1.147,
`mut-odo-vecdims` on `cifar-L2-16-c64-k3` 1.138), while every arm's geomean
stays inside 2% and the per-shape ranges widen to 0.758..1.161. **The wild cell
is the opposite signature in every respect**: one bench, its interval
a twentieth of a microsecond, its neighbours in run order and its own two twins
clean — and in this disturbed run `lenet-L1-28-c1-k5/bq-expand` reads 1.0070,
so the shape and slot are not what carries it either. An intrusion smears;
this does not, which is why it is a finding and not noise.

**The wild cell went where the fix predicted, and came back somewhere the fix
does not reach.** Run 8 recorded `bq-expand`'s distant twin 44% slow
on `vgg-14-c512-k3`, Run 9 41.4% on the same arm and shape, and five filtered
probes ran it down to a cold block pool at that twin's roster slot. Run 10 moved
`sum-only-early` above `list`, so nothing is measured on an ungrown pool,
and that pair read 1.0043 with its worst cell 1.67% on a different shape —
the three-bench probe that priced the fix at 0.24% reproduced over the whole
roster and shape set at full budget. **Run 11, on that same binary, carries
a 35% cell at `lenet-L1-28-c1-k5/bq-expand`**, with both of that arm's twins
clean, both time-neighbours clean, CI% 0.06 and `list` on the shape unmoved.
So what the roster fix removed was the *slot* — a twin measured on an ungrown
pool — and not whatever makes this family susceptible: the same arm, the third
run in four to carry a cell of this size, and this time at its own slot rather
than a twin's. Nothing here has been probed, the machine having been wanted
elsewhere; [the open list][open] carries what would settle it. The account
of the Run 8 and Run 9 cell, from those probes (2026-08-09, Run 9's own binary
and regime), stays because the mechanism is what the predictor below rests
on and because a recurrence is the reason to keep it:

- It **reproduces deterministically**. The twin reads 4.46 ms in the run
  and 4.50 ms alone; the two adjacent copies read 3.315 and 3.314 ms in the run.
  Same code, same allocation, tight intervals on all of them.
- **The slow figure is the arm's real isolated cost, and the published one
  is the anomaly.** Run `bq-expand` in a two-bench process and it reads 4.52 ms
  — the *distant twin's* figure, not its own published 3.32. So the twin
  at roster slot 3 is measuring the arm correctly and the arm at slot 29
  is being flattered by 26%.
- **It is the whole expansion family, not one arm.** Filtered into a small
  process, `bq-expand-gm-mulback`, `bq-expand-qr-prim` and `bq-odo-gm-mulback`
  each read 35–40% above their published cells on this shape, while
  `bq-scan-rem-gm-mulback` (2.275 ms against 2.279) and `mut-odo-vecdims` (1.566
  against 1.570) do not move at all. Susceptibility is a property of the arm,
  and these are five more arms with it settled.
- **One single predecessor does all of it, and it is `sum-only-early`.** Six
  bisection probes looked for a cumulative cause and found none — `list` first,
  `bq-gen` between, slots 4–16, 17–22 and 24–28 each left the arm slow — because
  every one of them omitted the bench that matters. Put `sum-only-early` between
  the twin and the arm and `bq-expand` reads 3.347 ms; put `mut-odo-vecdims`
  there instead and it reads 4.583. Nothing else is needed and nothing else
  substitutes. `sum-only` times a sum over a *fixed* vector, so its setup
  allocates one `l`-sized buffer and then allocates essentially nothing per call
  — a single large allocation that grows the block pool and leaves it grown,
  which is exactly [the position effect][pos-effect]'s mechanism and not code
  placement, the binary being identical throughout.

  **That made it a roster-order defect rather than a curiosity, and it is now
  fixed.** `sum-only-early` sat at slot 5 with the three distant A/A twins
  at slots 2, 3 and 4 — *before* it — so those three controls were measured
  against a colder heap than every strategy they exist to calibrate,
  and the only reason two of them looked fine is that they twin arms with too
  little excess allocation to care. A "distant" twin was therefore varying heap
  state as well as position, which is not what the crossed design says
  it varies. `sum-only-early` now runs at slot 2, directly after `list`
  and ahead of the twins; the reasoning, and why it stays *after* `list` rather
  than before, is at its roster entry in `Main.hs`.

  **Proven non-vacuous, as a fix to a measurement has to be.** The same
  three-bench probe that isolated the cause, re-run on the moved roster
  at the default nursery, puts the twin at 3.367 ms and its base at 3.375 —
  **0.24% apart**, where the identical selection before the move read 4.53
  and 3.35. The 41% cell is gone, and gone for the stated reason rather
  than by any change to what the arms compute.
- **It is not GC time.** Under `+RTS -s` the cold two-bench process spends
  **5.8%** of its total time collecting (productivity 94.2%, 41 MiB in use)
  and the warm 34-bench one **2.3%** (97.7%, 60 MiB). Even abolishing collection
  outright in the cold process buys 5.8% against a 36% gap, so the cost
  is inside MUT.
- **The allocation area is what it turns on, and `-A32m` removes it outright.**
  `-H512m` does nothing (4.74 and 5.16 ms raw), so it is the nursery
  specifically and not the heap size. An eight-point sweep, all on this shape
  and all **net** of the forcing pass, with `mut-odo-vecdims` carried through
  as a control the predictor says must not move:

  The two left columns are criterion slopes on the **pre-fix** roster, where
  the twin was still cold, and are here to show it converging. The two GC
  columns are exact rather than normalised: taken at a fixed `-n`, every setting
  allocates the identical 41.066 GB, so the counts are directly comparable
  and no per-GB rate is needed.

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

  The gen-0 column is the method checking itself: it falls as `1/nursery`
  at a constant 0.74 of the predicted count, that fraction being the large
  objects that bypass the nursery altogether. `-A1G` under the cap is the one
  row where it collapses to **zero** — a 1 GB nursery the 2 GB cap will not let
  it fill, so the RTS does 31 major collections instead of minor ones.

  **What the sweep settles is the cold arm, not the warm one.** The twin
  converges on its arm from 32m onward — 41% apart at the default, within 2%
  everywhere after — so a large nursery is a second route to the state
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
  the two level. Neither sample size nor GC interleaving explained it —
  at `-L60`, where criterion's samples reach 839 iterations, its ratio
  is unchanged at 0.903. **What explained it is that `/usr/bin/time -f %U`
  reports user CPU only.** Split the clocks and the default's missing cost
  is in *system* time, 0.29 s at `-n 800` and 0.58 s at `-n 1600` — perfectly
  linear, so **0.36 ms of kernel time per call** — where `-A32m` pays 0.03
  and 0.04 s, which is fixed startup and nothing per call. Differenced on wall
  time the two instruments agree: 3.300 ms against 3.075. So the small nursery's
  price is memory-management work in the kernel, an arm allocating 13.2 MB per
  call beyond its result against a 4 MB area, and a user-CPU measurement cannot
  see it. The general lesson is worth more than the figure: **difference wall
  time, or user *and* system** — a page rule inherited from horde-ad says "wall
  and user time agree on it", which was true of the workload it was written
  for and is false here.

  **The predictor called it, on a control shape** — the excess-allocation rule
  stated in full below. `cifar-L2-16-c64-k3` has 1.59 MB of excess per call,
  below the 4 MB area, so it should show neither kernel time nor benefit.
  It shows neither: system time is 0.00-0.01 s at both settings and does
  not scale with `n`, and `-A32m` is if anything 6% *slower* there. Two shapes,
  opposite predictions, both confirmed.

  **`-A1G` is a cliff, and the cliff is the `-M2G` cap and not the nursery.**
  The arm reads worse than the *default* — +20.3% by differencing — and gen-1
  collections go from 2 to 31 at identical work. Re-run at `-M8G` and it rejoins
  the others exactly (gen-1 back to 2). The high-water mark, 2318 MiB,
  is the first in the sweep to cross `micro.cabal`'s 2048 MiB cap, and crossing
  it is the whole of the effect. So a large nursery is not intrinsically bad
  here; a large nursery *under this cabal file's heap cap* is pathological,
  and would also destroy the guard the cap exists for.

  **What a caller should run with is a different question, and it answers
  cleanly.** The suite's question is which setting measures best; a user
  of `Data/Array/Internal.hs` wants the cheapest real cost, which is wall time —
  kernel work is cost to them — with no `-M` cap in the way. Differencing wall
  time at `-n 400`/`-n 800`, `-M8G` throughout, on the shape where the effect
  is largest:

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
  is flat and only the costs grow — memory linearly, and a one-time kernel
  charge of roughly **1.2 s per GB** as the area is faulted in. That fixed
  charge is what makes a small-`n` measurement of a large nursery look
  catastrophic: divided over 100 calls it reads as half a millisecond each,
  and it is not per call at all. The gain also exists only where an arm's
  per-call excess outruns the default 4 MB, so on `cifar-L2-16-c64-k3` (1.59 MB)
  every enlarged nursery is *worse* — 0.465 ms at the default against 0.480
  to 0.500 across the band. And `-A1G` is safe here only because `-M8G` removes
  the cap.

  **But "at this size" is load-bearing, and the advice inverts above the shape
  cap.** Real callers use arrays past `sizeCap`, so the `tooBig` shapes
  were promoted into the shape set behind a temporary edit and measured
  (2026-08-09, `-M20G`, busy machine, min of 5; the edit is reverted).
  Allocation first, which is exact and load-independent, and which confirms
  the one thing that does scale: **excess allocation is linear in `l` to three
  digits** over a 32× range — `bq-expand` 14.6 to 14.7 B/element, `list` 190.2
  to 190.4 — so at `imagenet-224-c64-k3` (`l` = 28.9M) a single call churns
  **425 MB** past its result, and `list` churns **5.50 GB**.

  | `-A`, at `imagenet-224-c64-k3` | `bq-expand` | its kernel time | `list` |
  |---|---:|---:|---:|
  | default | 113.5 ms | 13.5 ms | 1040 ms |
  | 32m | **134.0** | **31.0** | 637 |
  | 64m | 94.5 | ~0 | 603 |
  | 128m | 99.0 | 1.0 | 657 |
  | 256m | 99.0 | 1.0 | -- |
  | 512m | 100.0 | 0.5 | 603 |

  **`-A32m` goes from the best setting to the worst one** — worse
  than the default, by 18%, on 31 ms per call of kernel time, and it reproduced
  in two passes. Whatever the 4 MB default does badly at this scale, 32 MB does
  twice as badly, and 64 MB stops doing it at all. The threshold therefore moves
  with `l` but **nowhere near linearly**: 32m suffices at `l` = 0.9M and fails
  at 28.9M, while 64m covers both — a 2× nursery across a 32× size, not the 425
  MB a "nursery must exceed the excess" rule would demand. That rule is refuted;
  what sets the threshold is not measured here.

  Two more things the big shapes change. The prize **grows** rather
  than shrinking with size — 6% at `l` = 0.9M against 12-17% here, and ~40%
  for `list` — so the guess that DRAM-bound behaviour would swamp the allocator
  at scale is wrong. And the fix's margin over what it replaced narrows
  under a bigger nursery at *every* size measured, 9.2× to 6.4× here against
  10.2× to 6.4× at `l` = 0.9M, which is the same effect at a 32× remove.

  **So, for a caller: `-A64m` to `-A256m`.** It is the only band that is good
  at both ends — the default leaves 6-17% on the table above `l` ≈ 1M, `-A32m`
  is actively harmful at the top of the range, and above 256m nothing improves
  while memory and startup keep growing. Below `l` ≈ 1M, stay on the default.
  These are busy-machine wall figures and the ±5% between neighbouring settings
  should not be read; the kernel-time column is what carries the finding, being
  the mechanism marker and far less disturbed by load. **The prevailing caller
  sits just above that band and lands safely in it**: programs using the library
  carry `-with-rtsopts=-A1G -I0 -T -M8G`, and the sweep puts `-A1G`
  with the rest on per-call time once the cap is raised — its cliff
  was `micro.cabal`'s `-M2G` and not the nursery, and at `-M8G` it rejoins
  the others exactly — so what the setting costs against 64m to 256m is memory
  and a one-time fault-in charge. The consequence for this page is the other way
  round, and is Run 14: the caller's arms run in an allocation regime none
  of the figures here is taken in, which is what that pair is built to price.

**So the mechanism is settled: an arm allocating more per call beyond its result
than the nursery holds pays for it in kernel memory management, and the default
area is 4 MB.** The first consequence is the one already acted on — the roster
move, which warms every timed bench and takes the cell from 41% to 0.24%.

**The second is much larger and is not acted on: `list` is the most
nursery-sensitive arm on this page, so the published ratios are themselves
a statement about the default allocation area.** Its excess is predicted at up
to 353 MB per call, two orders above `bq-expand`'s, because a cons list of `l`
elements is nothing but small-object allocation. Measured on `vgg-14-c512-k3`,
quiet: `list` goes **28.659 ms to 16.019 ms**, a 1.79× speedup, where
`bq-expand` gains 10%. The ratios therefore do not cancel, they move hard —

| on `vgg-14-c512-k3` | default | `-A32m` |
|---|---:|---:|
| `bq-expand` / `list` | 0.098 | **0.157** |
| `mut-odo-vecdims` / `list` | 0.036 | **0.065** |

— so on this shape the shipped fix beats the fallback it replaced by 10.2×
at the default area and 6.4× at 32 MB. **Both are true; they answer different
questions.** The default is what a GHC program gets unless it says otherwise,
so the published column is the right one for "what does a caller see today",
and this page has only ever measured that. What it is *not*
is a nursery-independent property of the two algorithms, and the headline ratios
should not be read as one. Quantifying it over the whole table is a run,
not a probe: one shape is not the geomean, and the small shapes — where every
arm's excess is under 4 MB, as the `cifar` control shows — will move nothing.
**That run is Run 14**, whose control half carries `-A1G` against a basis
identical to it but for the allocation area ([what it compares
against](#what-run-15-compares-against)).

**The predictor, recorded before the run that would test it.** What decides
whether an arm feels the nursery is not its total allocation but its allocation
**in excess of the result buffer**, `(alloc − 1) × 8l`: the result is one large
object and goes straight to the large-object list, bypassing the nursery, while
the excess is the part that churns through it. On the six arms whose
`vgg-14-c512-k3` behaviour is already measured the rule separates them outright,
and the line falls on the nursery itself — affected at 11.2 to 13.2 MB of excess
(`bq-expand` and its two output variants, `bq-odo-gm-mulback`), unaffected
at 2.4 MB (`bq-scan-rem-gm-mulback`) and 0 (`mut-odo-vecdims`). Total allocation
does *not* separate them, putting an unaffected arm at 9.6 MB and an affected
one at 18.5 MB with no line between that means anything. Applied to the kept Run
9 cells the rule predicts **131 of 782** cells move, concentrated on the large
shapes, and names **14 arms that should not move on any shape** — the whole
`mut-odo-vecdims` family, `build`, `mut-odo`, `gen-quotrem`, `gen-unsafe`
and both `sum-only` halves. Two consequences worth having in writing before
the measurement. `list` itself is predicted affected on 17 shapes, by up to 353
MB of excess, so **the baseline is expected to move and every ratio with it** —
which is most of the case against adopting the flag casually. And `build`
and `mut-odo` are both predicted *unaffected*, so their 1.13× gap should survive
`-A32m` untouched; if it collapses instead, this predictor is wrong and what
this page calls placement is really the allocator. **Run 14 is the run
that tests all of this**, over 24 shapes rather than the one it was built on,
and at `-A1G` rather than the `-A32m` named above — the two agree at `l` ≈ 0.9M
and part company at the top of the range, where 32m turns actively harmful
and 1G does not, so the larger area is the stronger test of the same predictions
and not a substitution.

**And the eight class populations, which that count left out** (2026-08-09,
the same arithmetic over the kept JSONs; it reproduces the main set's 131 of 782
exactly, which is what makes the rest worth quoting). `list` crosses the nursery
in **every** population, so no class table divides by an unaffected baseline —
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
in absolute time across the change, against the 35–40% the excess-allocating
arms show. Two things follow. The predictor survives a test it could have
failed, on the side where failure was cheapest to detect. And **the placement
question is now confirmed independent of the allocator**, so the pad probe
was unavoidable rather than possibly-subsumed: this pair's 1.16×
is not filtering either, the full run reading 1.13× over the same shapes with 31
benches between the two arms.

**So position reproduced after all, and much larger than the twins price it.**
Run 7 read the distant twin above the adjacent one within every strategy
and growing with span; Run 8 read that as not reproducing. Run 9 says both
were looking at a summary of the wrong thing. Aggregated over shapes the effect
is nothing — three of Run 9's six pairs sit *below* 1 — while on one shape
and one family it is 35–40%, which no geomean over 24 shapes can show.
The standing advice survives and sharpens: `list` runs in the coldest slot, arms
far down the roster are **flattered** rather than penalised, and now there
is a measured case of by how much.

**What did turn up is a bigger placement effect, from an accident.** `build`
and `mut-odo` compile to the same worker — checked in Core at -O1 and again
under `-fspec-constr`, the dumps being [the mutable ceiling][ceiling]'s, which
is where that identity is kept — so they are a seventh known-true-ratio-1 pair,
and they disagree by 1.24× on Run 7, 0.86× on Run 8, **1.13×** on Run 9 (3 wins
of 24, sign p 0.00028) and 0.95× on Run 10's unaligned half. Four runs, two
of them differing from their predecessor in the roster alone, and the pair spans
0.86 to 1.24: that range is the instrument, and it is 44% wide for code
that is identical. The twins share one worker called from two slots; those two
are separate copies of one worker at two addresses, and the gap between what
the two instruments read is the part of layout the twins cannot see. Do
not price a margin between distant rows at the twins' floor. **Aligning both
copies shrinks the instrument rather than zeroing it**: on Run 10's aligned half
the pair reads 0.9685 with both copies at offset 0, so about 3% survives the one
intervention that removes the whole difference the table above attributes
it to — and the sign test ties there, 16 of 24, where every unaligned reading
of this pair has been lopsided.

**And those two addresses now have a candidate consequence, read out
of the binary** (2026-08-09, `-fspec-constr`). The innermost run-fill is 28
bytes — seven instructions and a backward branch — and the binary carries four
byte-identical copies of it, two per arm, the only alignment directive anywhere
in either procedure being `.align 8`. One copy per arm is the mismatched-length
`fail` join and cannot run on a well-formed shape; the copies that do run
are `mut-odo`'s at byte 29 of its cache line, which fits, and `build`'s at 53,
which straddles two. The dead copies fall the other way round, which is why
the pair looks like a wash until the executed one is identified. That is one bit
against one gap, so it was a candidate and not an account — but one the pad
probe could test, nothing pinning these loops to a line: pad in eight-byte steps
until `build`'s executed copy lands whole and see whether the gap goes with it.
It did — the confirmation is below the loop table. The instrument is steady
meanwhile, the flag's 12 KiB of `.text` reproducing to the byte on a base
the arms written since have grown.

**And a second family reads the same way, which is what takes it past one
point.** The four `mut-odo-vecdims` arms carry one copy each of that same
28-byte fill, the FastReshape three differing from their control nowhere inside
it ([the mutable ceiling](#the-mutable-ceiling-not-taken)), so their copies
stand beside `build`/`mut-odo`'s. **Every ratio is the row's arm against
its family's control** — `mut-odo-vecdims` for the four arms under it, `mut-odo`
for `build` — which is why the two control rows have no ratio of their own
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
and every copy that straddles read 13–18% behind, with no arm of either family
dissenting. Run 10 splits that.** Its offsets come from `loop-offsets.py`
over the two binaries, so the mod-64 column is read and not inferred,
and the aligned column is a build in which all ten copies the table covers sit
at 0. `build`/`mut-odo` behaves as the hypothesis says throughout — both copies
straddle in `micro-unaligned` at 45 and 53, both are resident
in `micro-aligned`, and the pair goes from Run 9's 1.13 to 0.9532 and 0.9685.
`add-in` behaves as it says too, and twice over: its copy is resident in *both*
Run 10 binaries and the ratio is 1.00 in both, where Run 9 had it straddling
at 40 and reading 1.1552. But `add-out` and `add-both` are resident at 36
in the unaligned half and at 0 in the aligned one, and they read 1.1266
and 1.0906, then **1.1612 and 1.1184**. Four placements each, none of them
straddling, and the penalty does not go. So the correlation inside Run 9's
binary was real for one arm of the family and coincidental for two, and what
those two cost is not layout — it is read in [the mutable ceiling][ceiling],
whose suspension of those figures this withdraws. The count-down form sits
in the table for completeness, resident throughout and so with nothing to say
about straddling either way, and is read in its own section.

**A third placement of the pair, taken the same day, says what the residual
is** (2026-08-11, `-fspec-constr`, one filtered pass, `*/build` and `*/mut-odo`
over the shape set, 48 benches in each process, the two arms adjacent so each
ratio is formed inside one process). The `-fproc-alignment=64` build below puts
*both* executed copies at 53 — the same offset, both straddling — where
`micro-unaligned` has them at 45 and 53 and `micro-aligned` at 0 and 0:

| binary | the two copies | `build`/`mut-odo` | 95% CI | sign test |
|---|---|---:|---|---|
| `micro-unaligned` | 45 and 53 | 0.9585 | 0.9347..0.9813 | 18/24, p 0.023 |
| `micro-aligned` | 0 and 0 | 0.9782 | 0.9498..1.0054 | 12/24, **p 1** |
| `micro-procalign` | 53 and 53 | 0.9893 | 0.9703..1.0091 | 16/24, p 0.15 |

**Whenever the two copies share an offset the pair ties, and when they do
not it does not** — and that holds at a resident shared offset and a straddling
one alike, which is what layout-neutral-by-construction predicts and what
no earlier reading could separate. **What this cannot do is rank the two
same-offset builds.** Their intervals overlap heavily and the two tests disagree
about which is nearer level — the shim's build has the flatter sign test
and the flag's the point estimate nearer 1 — so 0.9782 against 0.9893 is
not a difference one filtered pass resolves, the same binary moving by about
as much between a filtered reading and a full-roster one (0.9782 against
0.9685). Procedure placement, which aligning loop *heads* does not control,
therefore stays a candidate for the residual rather than a finding. What
the probe does settle is that no placement of these two copies leaves them more
than about a percent apart once they share an offset.

**A build with both, and an instrument that does not cancel** (2026-08-11,
`-fspec-constr`, `*/build` and `*/mut-odo` over the shape set, 48 benches
a process). `micro-both` carries the shim *and* `-fproc-alignment=64`, so all
eight fills sit at 0 inside procedures pinned to 64 — the build [the open
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

The count is shapes of 24 where the row's build is faster. So a shared
straddling offset costs both arms 8 to 13% while leaving their ratio level —
the flag removes the variance, not the cost — and shim plus flag costs 2 to 4%
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
is a reading of one penalty in its own right: `build` runs **1.169×** slower
where its executed copy straddles and `mut-odo` **1.162×**, every straddling
placement of an arm slower than every resident one. The discriminating pair
inverts as predicted — 0.874 where only `mut-odo` straddles, 1.102 where only
`build` does. And the penalty turns on *where* the split falls, which no reading
inside one binary could have shown: offsets 37, 45 and 53 cost 1.19 where offset
61, three bytes short of the boundary, costs 1.10 — which is why the one control
with both arms straddling reads 1.069 instead of level, `build` at 53 paying
full where `mut-odo` at 61 pays half. Evaluated at Run 9's own offsets
those penalties give 1.144 against the 1.13 it read, on a binary not among
the eight. The binaries differ in placement and in nothing else: fitted
allocation agrees to 1.000008 across the sixteen runs, and the subtracted
forcing term spreads 1.0046 where the arms spread 1.20. So the table above
stands, and the 13–18% it spans is the distance between a deep straddle
and a resident copy rather than a range still to be explained.

**What that span bounds is every margin under about a fifth — in an unaligned
build.** The per-offset figures run 0.9040 at offset 13 to 1.1051 at 37, so one
loop's placement is worth **1.22×** best to worst, and that is the number
a margin has to clear rather than the 1.169. Two rows of the Results table
differing by less can be layout entire, and the A/A twins cannot see it: they
call one worker from two slots, executing one copy at one address, where `build`
and `mut-odo` are two copies at two. **An aligned build removes that variance
rather than bounding it**, every short loop of Main's code sitting at offset 0,
so a margin read there does not have to clear 1.22 — which is what makes
the aligned half the place to adjudicate, and why a margin agreeing across
the two halves is evidence where either alone is not. Two limits on that.
It reaches only the loops the shim reaches, Main's and not the libraries',
so `list`'s own hot loop is outside it. And attribution is per arm and exists
for six of them, so for any other pair this is a statement about the population
of loops rather than about that pair's own. Reading the offsets is minutes
of `objdump` against a quiet-machine window, so it is the cheap first question
about a gap this size. `loop-offsets.py` beside this file finds the copies
structurally — a backward branch whose target is one loop length back, grouped
by raw bytes, so "byte-identical copies" is read rather than assumed —
and it was proved non-vacuous by reproducing three of the probe binaries'
documented offsets before it was pointed at anything new.

**But the table corrects only where the loop is the same code; elsewhere
it screens.** As 0.98 × pen(A's offset) / pen(B's offset) — the intrinsic ratio
being 0.98 and not the 0.9973 the probe's balanced design gave, which Run 10's
gate settled against it (see the open list) — it reproduces the eight binaries
to a median 1.0% and a worst 3.8%, Run 9's pair to 1.144 against the 1.13 read,
and the FastReshape three to 1.18 against 1.155–1.180. Its resolution floor
is the 5.9% by which the two arms disagree at offset 13, so it settles a 17% gap
and cannot touch a 5% one. And it reaches the six arms carrying this fill
and no others: dividing layout out of two *different* algorithms needs each
one's own penalty curve, which only stepping that arm's address supplies.
Everywhere else this is a quantified caveat, not a correction.

**GHC's native backend aligns no loop, and every other compiler to hand does**
(verified 2026-08-10 on this machine). GCC 13.3 at -O2 emits `.p2align 4,,10`
at each loop head, on by default as `-falign-loops=16:11:8`; clang 18 emits
`.p2align 4` above every block LLVM marks an inner loop header, with nothing
asked for. GHC's NCG emits `.align 8` at procedure starts and nothing inside
them — on 9.10.3, 9.12.4, 9.14.1 and HEAD (10.1.20260803) alike,
and `-fproc-alignment=64` adds none of it either — which is what leaves
this loop wherever it falls. The exposure follows: at 8-byte alignment three
or four of the eight reachable offsets straddle, four of eight for this one;
at 16 bytes one of four; at 32 or more none at all, a 28-byte loop starting at 0
or 32 ending inside its line either way.

**An isolated reproducer prices the same effect at 1.58×, and names what
it needs to appear** — horde-ad's `docs/ghc-issue-no-loop-alignment.md`, filed
as [GHC work item 27668](https://gitlab.haskell.org/ghc/ghc/-/work_items/27668),
which is where this belongs written up and which cites this benchmark for what
`-fproc-alignment=64` does in a larger program and what the correction costs
there. A 23-byte loop stepped through all eight 8-byte positions of a line runs
0.256 to 0.261 ns an iteration at the six that keep it whole and 0.410
at the two that divide it, alike on the four compilers. Two things that adds
here. It is outside this harness entirely — no criterion, no shape set,
no forcing term — so the pad probe's verdict no longer rests on one instrument.
And it names the condition: that loop carries four independent accumulators
and is fetch-bound, where the first attempt at the reproducer used one
accumulator with each iteration waiting on the last and measured
**no** difference at any position. So a straddle costs where the processor
is fetching ahead and is free where it is waiting — a sharper statement of scope
than two arms here could reach, and a candidate for why 1.19 here is smaller
than 1.58 there, the run-fill copying memory rather than only adding, though
nothing here measures that.

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
and the offsets read out of the binaries — a claim about layout, so no quiet
machine is involved). Without it the four copies walk 24 bytes a pad:
`[3, 53, 59, 45]`, `[27, 13, 19, 5]`, `[51, 37, 43, 29]`. With it all three
builds read `[3, 53, 3, 53]`, and the `mut-odo-vecdims` family `[8, 8, 4, 4]`.
A membership change no longer rerolls layout, which is the confound that made
Run 9's question unanswerable and this probe necessary. It does more than pin
them: the two procedures holding the copies are then 64-aligned and internally
identical, so the paired arms land on the *same* offset and the pair
is layout-neutral by construction. Two things it does not do. It freezes
this pair at 53, which straddles — the variance goes, the penalty stays,
and the offset frozen at is set by the procedure's own internals rather
than chosen. That the option stops at functions is deliberate and known: GHC
[#14701](https://gitlab.haskell.org/ghc/ghc/-/work_items/14701) has the person
who added it saying loops could be done too and were not looked at closely.
**It is now timed, and it is free on the baseline** (2026-08-11, a filtered
`*/list` pass over the shape set on each of three binaries, 24 benches each,
quiet machine). `.text` grows 0.14% and `list` does not notice: per-shape
geomeans of **0.9993** for the flag's build against `micro-unaligned` and 0.9997
for `micro-aligned` against the same, both scattering ±2 to 3.5% per shape.
So the insusceptible arm stays insusceptible under either intervention, which
is what licenses reading a ratio out of any of these builds — and it reproduces
Run 10's fifth prediction in a second setting, a one-bench process rather
than a full roster. The rebuilt binary's offsets are the `[3, 53, 3, 53]`
and `[8, 8, 4, 4]` recorded above, read out again, and its `check` log
is byte-identical to `micro-unaligned`'s:
`cabal build micro --ghc-options='-fspec-constr -fproc-alignment=64' --builddir=dist-procalign`,
the fresh builddir being what forces the rebuild a value-carrying flag does not.

**The loops can be aligned outright, though, by standing in for the assembler**
(2026-08-10). `-pgma` replaces the program GHC assembles with, so `align-as.py`
beside this file rewrites the `.s` on the way past: every local label
that a later instruction jumps backwards to — which is what a loop head
is in the NCG's output — gets a `.p2align 6`. On this suite that aligns 395
heads and puts **every copy of both fills at offset 0**, grows `.text` by 0.13%,
and leaves `micro check` green, 45 shapes agreeing and none dissenting.
So the straddle can be removed rather than merely frozen, and with
it the penalty — which turns the whole finding into a two-bench question ([the
open list][open]).

**How far it gets is a thing to measure and not to infer**, the shim's own count
of 395 being labels in the assembly it was handed rather than loops
in the binary that came out. `loop-offsets.py --survey` counts the population
that matters — self-loops no longer than a line, in this suite's own compiled
code, since only those can be rescued by an offset and everything longer spans
several lines in any build. It reads 115 such loops in `micro-unaligned`, **50
of them straddling and one at offset 0**, against 101 in `micro-aligned`
with **100 at offset 0 and none straddling at all**.

**Those two populations are not the same size, and the difference
is the disassembler rather than the binary** (2026-08-11, and it corrects how
the two counts above may be read). Lifting the survey's own 64-byte cap, Main's
resolved self-loops go 144 to 125 across *every* span bucket, not just the short
one — which rules out the obvious account, that padding inflated loops past
a line, since the 65-to-128 bucket falls too, 20 to 16. Counting one level
further back says what happened: Main's code carries **1580** backward jumps
in the unaligned binary and **1583** in the aligned one, so the loop structure
is untouched, as it must be for a shim that only inserts alignment directives.
What moves is resolvability — targets not decoded as an instruction start go
**613 to 777** — because `objdump -d` sweeps linearly and tables-next-to-code
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
this page compiles, the alignment is complete rather than partial. What it still
does not reach is the libraries, `vector`'s loops among them, which no `-pgma`
on this build touches.

**Pad only between two instructions, which is what the first attempt did not.**
Aligning every backward-jump target, 928 of them, produced a binary that failed
`check` on the first shape with `index out of bounds (-1378,324)`.
Tables-next-to-code puts an info table immediately before a return point, which
is a local label too, and a `.p2align` inserted there separates the table
from the code it belongs to. Requiring the preceding line to be an instruction
fixes it, at the cost of the loops whose head follows a table — none of which
this page measures. It is also why `check` is the gate to run on such a build
and the offsets are not: the offsets looked right in the broken one.

**And a trap that would have ruined that experiment silently**, on all four
of those compilers. GHC does not count `-fproc-alignment` as a flag change,
so an incremental build that only adds or drops it keeps the old object code
and says nothing: `ghc -O1` then `ghc -O1 -fproc-alignment=64` leaves
a byte-identical binary, where adding `-fforce-recomp` gives a different one.
Cabal is not at fault — it reports `(configuration changed)` and re-invokes GHC
every time, and the same toggle on `-fspec-constr` recompiles
with `[Optimisation flags changed]`.

**And the trap is far wider than the flag that found it**, which is what makes
it a standing rule here rather than a note about one probe. Recompilation
checking hashes boolean `GeneralFlag`s and a fixed list of fields, so every
setting that carries a *value* is outside it — `-pgma` and `-optlo`/`-optlc`,
the inliner's `-funfolding-use-threshold` and `-funfolding-fun-discount`,
`-fmax-worker-args`, `-fdmd-unbox-width`, and **`-fllvm`**, so that switching
the whole code generator reuses the native backend's objects in silence. All
of them confirmed missed on all four compilers, and that list is a floor:
it is what one test module could exercise. So **any A/B on this page
that toggles a flag must force the rebuild** — `-fforce-recomp` or a fresh
`--builddir` — and the regime comparisons already run that way only because they
were built in separate trees. The first round of the alignment experiment had
neither and read its flag as inert. Written up
as `docs/ghc-issue-recompilation-ignores-codegen-flags.md` in horde-ad, beside
the block-pool issue and in the same form, and filed from there as [GHC work
item 27667](https://gitlab.haskell.org/ghc/ghc/-/work_items/27667) — that file
carries the cause in GHC's own source and the list of settings, and is the copy
to read.

**What is comparable across an alignment change, and what is not.** `list`
is the one arm measured insusceptible to placement — 0.9949, 1.0019 and 1.0031
across the rebuild probe's four binaries — so the denominator of every ratio
this page publishes, and the absolute anchor cells beside them, stay comparable
across the change. A susceptible arm's absolute figure does not, which is why
an aligned build wants a column of its own beside the regimes rather
than a splice into one: folding aligned figures into `-fspec-constr`'s column
would reintroduce in silence the term that alignment exists to remove. And once
an aligned build is the standing regime, the per-shape record a later run
compares against is taken from *it*, a fingerprint kept from an unaligned run
passing the layout term forward into every run that reads it.

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
It does not close the pair — 3% survives on the main set — and the one
population that inverts is `reshape1`, where both arms are twenty-seven times
slower than the class's leaders and whatever separates them is not the loop
the shim aligned.

**And a probe has since priced the rebuild itself, which is what neither
the twins nor that pair measure.** Four binaries built from sources differing
only in inert pad arms, the run filtered so the pads never execute, leave `list`
inside 0.5% and move `mut-odo` and `offtab` by up to 18% ([the open
list](#what-is-open) carries the figures). So this page has three uncertainties
of quite different size and only the smallest is on the table above. An arm
against **itself in one binary** is the A/A twins, 1.00% on Run 10's unaligned
half and 0.54% on its aligned one. Two **different arms in one binary** carry
placement, which `build`/`mut-odo` put at 14-24% for a pair whose code
is identical — **until the loops were aligned, which takes it to about 3%**,
and to a tie by the sign test whenever the two copies share an offset. One arm
across **two binaries** carries the rebuild, up to 18% on a susceptible arm
and almost nothing on an insusceptible one. Susceptibility is a property
of the arm and has been measured for three of them, so for the rest
it is unknown; what that protects is orderings and tiers, which several arms
witness at once, and what it does not protect is any single arm's figure read
across a rebuild.

**And the third of those is a bias, not a floor, which is the distinction
to keep.** A floor is a threshold below which a margin might be noise,
and it shrinks as samples accumulate; this does not. Each binary's figure
is *correct for that binary* — the four-binary rebuild probe's cells
are geomeans over 24 shapes with per-cell intervals of a fraction of a percent —
so collecting more samples inside one build cannot reduce it, and only averaging
over several builds would. The per-shape picture says the same: across rebuilds
`list` scatters 2.2-2.5% per shape while its geomean holds to 0.5%, where
the two susceptible arms scatter 5-10% per shape *and* move their geomeans.
So do not read 18% as a new floor for this page's tables. Every comparison
inside the Results table is two rows of one binary and is governed by the A/A
twins as before; what the 18% governs is the sentences that cross a build, which
on this page means the cross-regime absolute figures and nothing else.

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
another slot. Read the two uses apart — a filtered run cannot price the distance
between two slots, and it can price the difference between a warmed process
and a cold one, which is the larger of the two effects here by an order
of magnitude.

The floor grows with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a real
difference. On raw slopes Run 10's unaligned six read 1.0008 and 1.0038, 1.0027
and 1.0033, 1.0066 and 1.0035 — adjacent and distant per strategy —
so the largest deviation is 0.66% before the correction and 1.00% after it,
and every one of the six grows. Correcting the table without correcting
the floor would have been the whole error.

**And it was re-checked at full budget on Run 10, over four populations
at once** (2026-08-11). Predicting each A/A pair's net deviation from its raw
one as `1 + raw/(1-f)`, with `f` the forcing term's share of that arm's own
slope, reproduces all **24** pairs of the main set, `window`, `bcastmid`
and `scaled` to a few hundredths of a percentage point — 5.36% predicted 5.29%,
0.54% predicted 0.67%, and the rest closer. Two things that buys.
The amplification is arithmetic and not a second effect, confirmed on a run
rather than inherited. And it says **why the `mut-odo-vecdims` slot keeps
carrying the worst pair**: `f` is largest for the fastest fill, 0.598 against
0.296 for `bq-expand` in the same `scaled` process, so that arm amplifies
whatever raw disagreement it has by 2.49x where its neighbours amplify by 1.42x.
The raw disagreement is still the larger factor there — 2.13% against 0.17% —
so this explains part of a pattern rather than dissolving it.

That is a mechanism rather than an observation, so it was checked — on Run 6's
three pairs, when the correction landed. Subtracting a shared term scales
a pair's deviation from 1 by `1/(1-f)`, `f` being the term as a share of the arm
— an identity *per shape*, and therefore worth nothing until it has survived
the geomean over shapes. It did, to within 0.01 percentage points on all three:
predicted 1.0010, 0.9943 and 1.0293 against observed 1.0011, 0.9942 and 1.0292,
with the amplification tracking `1/(1-f)` arm by arm too. So the floor's growth
is the correction's own arithmetic, not a second effect riding along with it —
and Run 9's pairs move the same way, every deviation larger net than raw.

**Failed Run 6's two conclusions here are settled.** *1/time* is refuted
as an account of the floor: per-cell *scatter* does track it — the adjacent
pairs in the table rank by their arms' speed — but scatter cancels, and the bias
that survives cancelling ranks by span, not by any arm's speed. *Position*
was confirmed by the crossed design built for it, read as not reproducing on Run
8, and is confirmed again by Run 9 in a form the crossing cannot summarise:
it is per shape and per family, not a trend in span. What the crossed design
settled for good is that the question is answerable at all; what Run 9 adds
is that the answer is not a single number.

Six A/A points are a modest estimate of a noise floor whichever run supplies
them, and the four runs disagree several-fold: Run 9 was the tightest
and the wildest at once, five pairs inside 0.07% and one cell at 41%, where Run
10 is uniform instead — every pair inside 1.00% unaligned and 0.54% aligned,
worst cells 11.2% and 7.7%. Expect either shape rather than a constant.
So the threshold to quote is the running one, and it is the run's own number
and not a tenth of a percent that a margin has to clear.

The floor above is also measured within one roster, and the roster is a variable
of its own: RTS pool state a predecessor leaves in the process moved a horde-ad
benchmark ~18% ([the full account][pos-effect] — which includes this suite's own
floor measured isolated against in-process, on both harness generations). Run 9
is that account reproduced here and larger, its expansion family reading 35-40%
above its published cells once the process is emptied of predecessors. Every
strategy sharing one process is what protects the tables above, ratios
cancelling the shared process draw — and the vgg cell is what that protection
costs when the draw is *not* shared, one family warming and another not.
A comparison that crosses runs should pin the benchmark selection along
with the binary.

**Every kind of comparison this page makes wants an instrument, and only some
have one.** Worth asking outright of any new claim, because the four answers
known so far differ by two orders of magnitude and none was found on purpose:
an arm against itself in one binary is the A/A twins, 0.54% to 1.00% on Run 10
and 0.07% on Run 9; two different arms in one binary carry placement, which
`build`/`mut-odo` put at 13-24% for a pair whose code is identical and put
at about 3% once both copies are aligned; one arm across two binaries carries
the rebuild, up to 18% on a susceptible arm; and one arm across two *process
populations* carries the warming, 35-40% on the expansion family
at `vgg-14-c512-k3`. The last is the largest, and the second is the one
this page has learned to remove rather than only price. So when a sentence
compares something new — two populations, two machines, two GHC versions, an arm
against a prediction — ask which of these bounds it, and if none does, say
so in the sentence rather than borrowing the nearest number.

**Each population measures its own floor.** The same six controls ride every
process, so a stride-class run prices the noise of the process its own figures
came out of — which is the only process they can be judged in — but it prices
it over three cells where the main set has two dozen. Read a class's controls
as this floor confirmed there or not, rather than as a threshold of that class's
own, and never carry the main set's figure into a class comparison or the other
way about. Run 10's class processes are that ruling observed: floors from 0.16%
(`rev`) up to 5.36% (`scaled`), a **thirty-fourfold** spread across populations
of one run, where Run 9 spread fifteenfold and Run 8 differently again.
The `mut-odo-vecdims` slot carries the worst pair in **five** of the eight —
`revsome`, `bcastmid`, `reshape1`, `window` and `scaled` — where Run 9 put
it in four and Run 8 in seven; `bq-expand`'s pairs take the other three
and `bq-scan-rem-gm-mulback`'s take none. Four runs at four counts is
not a pattern settling, but the amplification above says the slot is not neutral
either: `f` is largest for the fastest fill, so that arm converts a given raw
disagreement into a larger published one than any other pair in the same
process. Read the recurrence as partly arithmetic and partly unexplained,
and read a class's floor as the run's own.


### R2 is the ramp detector, not the noise detector

The two columns catch disjoint failures. **CI%** finds sampling noise, which
the capping then bounds. **R2** finds *curvature* — early, low-iteration samples
running slower than late ones, because criterion forces only a minor GC between
samples and a full one just once per benchmark, so promoted data accumulates
as the sample count climbs.

A ramp is systematic, so it yields a *narrow* CI around a *biased* slope:
the capping cannot see it and will not bound it. The bias tilts the fit shallow,
so a ramped strategy reads slightly **faster** than it is — and not uniformly,
since strategies allocating a large scratch ramp harder than in-place fills,
making the flattery differential exactly where the comparison is decided. Read
any row with R2 below 0.99 as possibly a couple of percent optimistic rather
than merely noisy. In Run 10 (SpecConstr) the unaligned half has 1 cell of 816
in the main set — `bq-expand-zf` on `stretch-inner256` at 0.9877, **the same arm
and shape for the third run running**, which makes it a property of that pair
rather than of a run — while the aligned half has 3, worst
`bq-expand-gm-mulback` on `stretch-square-1341` at 0.9800, and two class
processes add one each (`build` on `reshape1-r3` at 0.9886, `gen-quotrem`
on `slice-cnn-L2-24x24-c32` at 0.9751). Run 9 had one and no class cell, Run 8
one plus `build` on `bcast-tall-Mx2`, Run 7 two and six, five of its six
on `bcast-inner900` where the scan family ramped re-reading a 2000-element
backing with 1.8M elements; those are gone, in the regime that takes the same
family's allocation to the table. Alignment therefore does not reduce curvature
and may add a little, which is a different axis from the noise it leaves alone
(its median CI% is 0.138 against the unaligned half's 0.134 over the same 816
cells).

Run 6's two worst cells had a cause worth the space, because it is a method
as much as a finding. `mut-odo` carried that run's highest CI cell on both
of its two smallest `cnn-L1` shapes, while `build` — the identical fill through
`vBuildVS`, from a different roster slot — and `mut-odo-vecdims` — the same fill
with the odometer's cons-lists replaced by unboxed vectors — were clean
on the same two. Same shape, same process, so it was neither the shape
nor a disturbance in that stretch of the run: it is the odometer's list traffic
as a GC ramp where `l` is small enough for it to dominate, which is the cost
`mut-odo-vecdims` exists to remove. The ramp did not recur at Run 7's full
budget, where the same cost surfaced as scatter instead, `mut-odo` carrying
that run's highest `noise` figure by far; it did not recur on Run 8 or Run 9,
that arm reading an ordinary 1.01 on the latter — **and it is back on Run 10,
larger, and largest of all on the half where the arm is fastest**. `mut-odo`
reads 2.40 unaligned and **4.51 aligned**, the noisiest bench of that process,
ahead of `list` (3.59), `gen-unsafe` (3.43) and `gen-quotrem` (3.36);
on the unaligned half the first-attempt arms still lead it, `gen-unsafe` at 5.57
and `gen-quotrem` at 3.48. For scale, `concat-runs` was dropped from the timed
roster at 2.45. So the earlier reading — that whatever the flag does
to this arm, it does not do it by making the bench noisy — no longer holds:
removing 12% of its time by aligning its loop left it noisier than anything else
in the process, and nothing here explains why. **Positional
or strategy-intrinsic is the question to ask first of any suspicious cell**,
and `--cells` answers it cheaply: a disturbance shows as a contiguous window
of roster slots, a property of the code shows as one slot across several shapes.

That second reading needs several shapes to see the slot across, which a [stride
class](#the-stride-classes-and-what-they-cover) does not have: with two
or three, a ramped cell is a large share of its column and only the first
reading is available. Whether it is the shape or the strategy is then a question
for the main set, where the same strategy has two dozen cells.


### sum-only, and the correction now applied

Every strategy is timed as `VS.sum . fb`, so every measurement carries the same
forcing pass; `sum-only` times that pass alone. It is a median 17.7%
of `bq-expand` and 2.7% of `list`, so an uncorrected ratio is compressed toward
1 by about that much and every margin read off one is an *understatement*.

**Run 6 (-O1) licensed subtracting it, and every figure on this page is net
of it**: its two halves agreed to 0.01% paired, flat in shape size as well
as position, and `read-run.py` has since taken the term per shape as the mean
of the halves and divided net of it. Nothing is comparable across that line —
every figure predating Run 6 here and in `Main.hs` was uncorrected — though
the uncorrected column stays one
`--exclude sum-only-early --exclude sum-only-late` away, and `read-run.py` says
on stderr when it is reading one. And the correction can change an ordering,
although `(B+S)/(A+S) < 1` exactly when `B < A`: that identity holds *per
shape*, and the geomean over shapes does not preserve it — Run 6 saw three
adjacent pairs swap, all inside the floor.

**The term passes three gates, re-passed by every run rather than inherited**,
each blind to what the others catch:

1. *Position.* The two halves sit far apart in the roster and must agree;
   failing is the halves parting past the floor. **Run 9 (SpecConstr)**: 1.0000
   paired, 0.10% mean per cell, worst cell 0.53%, the halves 28 benches apart;
   and every class process within 0.3%, the loosest being `scaled` at 1.0026.
2. *Size.* The term is subtracted **per shape**, so it must be the same pass
   on every shape — one sum over `l` elements — and a term that were not could
   be wrong in both halves alike, leaving their agreement to notice nothing.
   It is: 0.592 to 0.607 ns per element across the whole shape set, a 1.02x
   spread over that 6250x range of `l`, with the largest shapes a couple
   of percent dearer per element than the smallest and no trend beyond that.
   `--selftest` checks it on every run and fails the run past a 1.5x spread; all
   nine of Run 9's populations passed, none spreading past 1.02x.
3. *The read itself.* `sum-only` re-reads one **fixed** vector, where a strategy
   sums one its own fill has just written — a different cache state, and the one
   thing neither gate above can see, since a term biased by it would be biased
   alike on every shape and in both halves. This is what `bq-expand-nosum`
   and `mut-odo-vecdims-nosum` are for: each is its base arm run again
   and forced with a single element instead of the sum, so *base minus arm*
   is that sum in situ. Measured against `sum-only` on Run 9 they read
   **0.9854** and **0.9764** as medians — within 3%, on the two arms where
   the term is the smallest and largest share of the bench (a quarter
   of `bq-expand`, a third of `mut-odo-vecdims`), so the test spans the range
   over which a bias would matter. Per-cell scatter is 4.3% and 3.5%, the worst
   cells on `stretch-inner256` and `stretch-square-1341`. Failing is both
   medians leaving 1 on the same side by more than a few percent —
   the biased-read signature; one arm scattering while the other reads clean
   is a local disturbance for that population's write-up, not a failed gate.

   **It has now not bracketed for two runs, which promotes it from a thing
   to watch to a thing to price.** Run 7's two medians sat either side of 1; Run
   8's were both below, and Run 9's are both below again — as is **every**
   in-situ median of both arms in all nine populations, eighteen readings
   between 0.960 and 0.999. Two runs and eighteen readings on one side
   is no longer a coincidence at any reasonable reading. The in-situ sum costs
   *less* than `sum-only`'s re-read, so the term is slightly over-subtracted
   and every ratio slightly flattered — by about 0.5% of `bq-expand`'s own slope
   at a 2% error in a term that is a quarter of it, which is inside this run's
   floor everywhere but `bcastmid`, where the reading is 0.9597 and the flattery
   about 1%. The gate still passes on its own test, which asks for *more
   than a few percent*; what it has stopped doing is passing for the reason
   the test assumes. [The open list](#what-is-open) carries what would settle
   it.

   **The cells under those medians say the same, and add a gradient the medians
   hide** (2026-08-09, off Run 9's artifacts). Taken per shape instead of
   as a median, over both arms and all nine populations, the in-situ readings
   sit below 1 on 73 cells of 86, sign p 2.7e-11 — and not because differencing
   two nearly equal numbers is noisy: calibrated on each arm's own A/A cells
   and amplified by the differencing, the scatter to expect is a fraction
   of a percent to a couple of percent, and three `bq-expand` cells of 24
   and no `mut-odo-vecdims` cell fall inside it. The two arms also order
   the main set's shapes alike — Spearman 0.82, and 0.85 with the three cells
   above 1.03 set aside — and two fills an octave apart in speed, at roster
   slots 13 and 50, agreeing shape by shape is what a property of the read looks
   like rather than one of either arm. The gradient is in `l`: the shortfall
   runs about a tenth of the term at the smallest shapes and vanishes
   at the largest (smallest twelve shapes 0.955 and 0.960 by geomean, largest
   twelve 1.027 and 1.002; r against log `l` 0.60 and 0.58), which is neither
   a per-call constant nor a per-element rate. Where it concentrates
   is the shapes whose result is L1-resident: the three at 32 KiB of result
   or under read 0.898 and 0.925 by geomean against 0.98 to 0.99 for everything
   larger, and between the L2 and L3 buckets it barely moves at all. Whether
   that is a step at the L1 boundary or a smooth trend three shapes cannot
   settle — with the cells above 1.03 kept a line in log `l` fits better
   and with them dropped a three-level step does, decisively for `bq-expand`
   and marginally for `mut-odo-vecdims` — so read it as concentrated
   in the L1-resident shapes rather than as a boundary effect. None
   of this replaced the third `-nosum` arm: a third write pattern was the only
   thing that could separate the read from these two arms, and the above
   is evidence pointing that way rather than a substitute. **The arm has since
   been added, and it agrees.** `mut-flat-gm-nosum` is a flat fill sharing
   neither an odometer step nor an expansion stream, and its in-situ term reads
   below 1 like the other two, which is the reading gate 3's entry carries
   and the answer this paragraph was waiting for.

   **Priced, it is under a point.** Re-pricing each arm's own numerator
   with its in-situ term, the `list` denominator left alone at 2.7% of itself,
   moves Run 9's published main-set geomean to 0.9993 for `bq-expand` and 1.0088
   for `mut-odo-vecdims`, and each class's to between 1.0015 and 1.0288,
   the largest under `bcastmid`, `scaled` and `bcast`. Per shape it reaches +3%
   and −8%, and the cells that move a published figure most are the three
   reading *above* 1 rather than the systematic shortfall. So the flattery
   is real, sits inside the layout span everywhere, and is worth a sentence
   about a particular cell rather than a second correction to the column.

**The three gates are a population's, not a run's.** Every process carries
the `sum-only` pair and the two `-nosum` arms, so a [stride
class](#the-stride-classes-and-what-they-cover) measures its own term
and re-passes all three on its own cells; the main set's term licenses nothing
about a class's, in either direction. What a small population weakens is gate 2
alone: it reads the term's cost per element across the shape set, and a class
spans a fraction of the main set's range of `l` — three shapes of nearly equal
`l` leave it almost nothing to see. Gates 1 and 3 are as strong there as here,
being about position and about the read.

What remains open is narrower than the original objection: the `-nosum` pairs
price two arms, not the whole roster, so a fill whose write pattern leaves
the cache in some quite different state could still be summed at a cost
`sum-only` misses. Two arms an octave apart in speed agreeing to 1% makes
that unlikely rather than impossible, and the arms are in the roster so every
run reprices them.


## About the last run (Run 14)

**Run 14 (SpecConstr), and what the allocation area costs.** Criterion, GHC
9.12.4, **`--ghc-options=-fspec-constr`**; Run 13's regime, its shapes
with a third added to five class views, and its roster plus twelve A/A twins,
which takes the roster to 1128 benches and the timed arms to 47 over 24 shapes.
Both halves are Run 13's `lookrts` recipe — the max-skip shim
with its look-through, adopted on Run 13's evidence rather than re-measured here
— and they differ in their baked RTS line and in nothing else: `-I0 -T -M8G`
on the basis `run14-lookrts`, `-A1G -I0 -T -M8G` on `run14-a1g`. That single
variable is the allocation area, and `-M8G` is what makes the 1 GB half
a legitimate build, its cliff having been `micro.cabal`'s `-M2G` cap and
not the nursery. md5 `369ab669a61ea1ffe35581d42bc60045` for the basis
and `1653886a9b9b77fa13ff393a7152a301` for the control, from `Main.hs` at commit
`c1639ee` — the tree at `b4a561e` and clean when the sequence was launched —
on the same desktop, Zen 3, a Ryzen 7 5800X. The two main processes read
*1h37m14s* and *1h37m58s* elapsed at *139 MiB max residency* apiece, and their
peaks in use are the pair's variable made visible: *365 MiB* on the basis
against *2869 MiB* on the 1 GB half.

**This run's floor is 2.19% on the basis half and 4.02% on the control,
and it is not Run 13's floor restricted.** The roster's twelve new A/A twins
take the A/A population from six pairs to eighteen and put the new ones
on `build`, `mut-odo`, `offtab`, `gen-unsafe`, `bq-odo-gm-mulback` and `list`,
the first four of them the widest-spread in the roster — the widest-spread arms
here, the ones this pair reads at 0.86 to 1.24 across runs for identical code —
where Run 13's six sat on the tight arms alone. So the figure every margin below
is judged against is measured over a wider instrument than any before it,
and **the comparable figure is the six-pair one, 0.29% and 0.16%** against Run
13's 0.33% and 0.62%. On that basis the machine did not get noisier;
the instrument got wider on purpose. Read a class or main-set worst cell
the same way: the worst A/A cell anywhere is 33.51%, on `stretch-wide-2xM`
in the basis main set, and it belongs to one of the new twins rather
than to anything Run 13 could have shown.

**The finding is that a 1 GB nursery costs about a tenth of the roster's time,
and that excess allocation does not say which arms pay.** Arm over arm across
the main set, 41 of the 42 arms compared sit outside 1% of 1 and every one
of them is slower on the 1 GB half, from `gen-quotrem` at 0.7454 to `bq-gen`
at 0.9906. The excess-allocation predictor registered before the run named
the arms that should move on no shape — those allocating exactly their result,
which on this roster is nine timed arms: the five `mut-odo-vecdims` variants,
`build`, `mut-odo`, `gen-quotrem` and `gen-unsafe`, with their eight A/A twins
beside them. (The registration counted 14 on the roster it was written against;
the set is the same rule over a roster that has since gained twins.) **Every one
of the nine moved**, from `build` at 0.9589 to `gen-quotrem` at 0.7454. **What
survives of the rule is its account of allocation and not its account of time**:
the fitted allocation agrees between the halves on 845 of the 1080 cells
that allocate in earnest, so nothing below is a code difference.

**Its control did not decide the question, and the reason is worth recording
rather than reporting as a break.** `build` against `mut-odo` was registered
as the pair whose 1.13× gap must survive; it reads **1.0171** on this run's
*basis* half, which is the same default-nursery configuration every earlier run
used, so the gap had already gone before the variable was applied. This page
prices that pair at 0.86 to 1.24 across runs for code that compiles to one
worker, and 1.02 sits inside that. The control was ill-posed rather
than refuted: a quantity with a 44%-wide instrument cannot carry a 13% test.

**Three instruments, and they agree once the regime is matched.** Criterion's
slopes put the penalty at 0.9% to 25.5% across the main set and 20% to 40%
across the classes. Differencing two fixed-iteration runs of a *single* bench
in a fresh process puts the same arm at under 1% — 290 µs against 292.
Differencing the *shared* 47-bench process removes every fixed cost and leaves
**0.913 on wall and 0.912 on user-plus-system**, so about 9.5%. The middle
reading is not a refutation: it says the cost is absent when an arm runs alone
and present when the process is shared, so it is a property of the process's
memory regime and not of any arm's own work — which is exactly why arms
with no excess allocation pay it. The remaining few points between 9.5%
and criterion's figure are the correction, below.

**The `-A1G` half's kernel time is fixed, and its minor faults prove it.** The 1
GB half carries 0.87 s of system time against the basis's 0.01, which reads like
a per-call cost and is not one: differencing a doubling of iterations moves
it by 0.02 s, and its minor-fault count is 695 916 against 695 730 across
that same doubling — flat, where the basis half's doubles with the work, 500 692
to 994 193. So the fault-in is per-process startup, as registered, and the small
nursery is the half whose kernel work scales.

**And the correction does not sit on the same footing in the two halves, which
is this run's caution against its own figures.** The in-situ forcing term —
an arm minus its `-nosum` twin, against the `sum-only` the correction actually
subtracts — reads 0.9914, 1.0115 and 1.0023 on the basis and **1.0959, 1.0735
and 1.0660** on the 1 GB half, with the scatter roughly tripled. Summing
a vector the fill has just written costs 6.6% to 9.6% more there than summing
a fixed one, which is a locality reading rather than an arithmetic one,
and it means the correction under-subtracts on that half. At `f` around 0.25
that inflates its corrected times by some 3%, so the 1 GB half's absolute
figures are overstated by about that much against the basis's, and a margin here
under a few percent is not this pair's to decide.

**The two halves differ in a baked string and in nothing a layout can see**,
which makes this the cleanest pair this page has run. Both `.text` sections come
out at 20377797 bytes; every tracked loop sits at the same offset in both, fills
`[11, 0, 4, 0]` and `[24, 8, 0, 0]`, at the same addresses;
and `loop-offsets.py --library` reads 953 library self-loops at 100% same offset
and 100% same straddle. A `-with-rtsopts` change relinks a different options
string and nothing else, so no pad is derived, none is needed, and the placement
term earlier pairs had to argue about is absent rather than cancelled.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512`, where
plain -O1 separates the two tenfold. On the confirm-don't-rebuild path this run
took, with no build to carry the flag, that is the only check standing between
a mistyped regime and the hours.

**The `scaled` slot is answered, and the answer is the run's best result.** Six
runs of seven had found a disturbance at the `mut-odo-vecdims` slot
on `scaled-super-r3`, its magnitude never repeating; this run was registered
to read it on both halves, and the prediction named its own outcome in advance —
*if the step is nursery or pool structure, the 1 GB half does not carry it*.
It does not carry it. The adjacent pair reads **1.0000 at a worst cell
of 0.21%** on the control half against **1.0171 and 4.15%** on the basis,
and the distant pair 0.9967 and 1.84% against 0.9850 and 5.26%. **So the step
is nursery or pool structure**, which closes a question open since Run 8
and which no run before this one could have asked, the classes having run
on the basis alone. Read the slot and not the process: `scaled`'s worst A/A cell
on the control half is 10.3% on that same shape, and it belongs to one
of the twelve new twins, so a reader taking the process summary for the slot
would invert the finding.

**The free draw came up clean, and the worst cells belong to arms no earlier run
twinned.** The worst A/A cell in the basis main set is **33.51%**
(`stretch-wide-2xM`) and in the control **26.67%** (`stretch-tab7MB`), and both
sit on twins the roster gained after Run 13 — none of the six pairs the earlier
runs measured reads worse than 7.83% here, which is the whole of why this run's
floor looks several times theirs. `lenet-L1-28-c1-k5/bq-expand`, the cell Run 11
carried, does not return. Against the 44%, 41.4% and 35% of Runs 8, 9 and 11
this run is clean, and every claim below is read on all 24 shapes.
**The `scaled` slot is quieter than it has been**: `mut-odo-vecdims`'s distant
pair there reads 0.9850 on a worst cell of 5.26%, against Run 13's 1.0547
and 11.59%, and its arithmetic account holds as ever — raw 0.9942 at `f` 0.583,
so `1 + raw/(1-f)` predicts 0.9862. Its magnitude goes on being the unstable
half. [The open list][open] carries the ruling that follows and this run does
not change it: quote the slot as a hazard of the class and never as a figure.

**Run 14 records every population twice** — the main set and all eight stride
classes from each half, one process each, which is what makes its class readings
a pair rather than a basis alone — and **all eighteen ran in one window**,
06:58:23 to 13:28:21 on an idle desktop, each exiting 0 at the bench count
its roster holds. Each class process's provenance line sits beside its own table
in [The stride classes, run by run](#the-stride-classes-run-by-run); the regime,
the machine and the commit are the whole run's and stay here. One process per
population is what makes each population's gates its own, and all eighteen
passed them.

**Everything in this chapter is replaced by the next run.** What exactly,
and in which other files, is [Provenance](#provenance). None of it is portable:
a run on another machine is a different measurement rather than a repetition.


### Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](#sum-only-and-the-correction-now-applied) carries that decision
and this run's re-pass of its gates), the scratch vectors are the unboxed ones
the shipped code uses, as they have been since Run 7 ([the scratch vector
flavour](#the-scratch-vector-flavour) says what that severed), and **this
is a `-fspec-constr` table**: it is not the regime `Data/Array/Internal.hs`
compiles under, and a row's distance from Run 11's max-skip column is drift
and not a strategy's, the flag, the roster, the order and the shim being
the same ones.

**And it is the basis half's**, `run13-maxskip`, as every published table here
is from Run 11 on: the flag half's column is one column on the yardstick below
rather than a second copy of these thirty-odd rows.

**Comparing runs?** The table below is Run 14's own; what to hold a new run
against is [What Run 15 compares against](#what-run-15-compares-against),
the claims to test are [the ones after it](#the-claims-run-15-should-test),
the population and the absolute anchor are in [Provenance](#provenance),
and this run's own floor — no A/A pair further than 2.19% from 1 on the basis
half or 4.02% on the control, on worst single cells of 33.51% and 26.67%,
and 0.29% and 0.16% read on the six pairs that carry across runs — is [in
the floor section][floor]. That floor governs an arm against *itself*; two
different rows of the table below are separated by their code, and in a build
whose loop heads the shim has already placed, no longer by where each landed —
which is what Run 10 spent two binaries to establish and every run since has
inherited.

**It is the main set's table**, and every column below is a statistic
of that population: each stride class has a table of its own, on the same rows
and in the same columns but its own basis, in [The stride classes, run
by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*,
  less that shape's forcing term, over `list`'s slope less the same term,
  with the per-shape log-ratios *winsorized* first — capped at the row's own
  median plus or minus three MADs. Nothing is dropped, so all rows cover one
  population and any two columns are comparable; a cell far enough out
  to distort the mean has its influence bounded instead of its evidence deleted.
  The `CI%`, `worst`, `smp` and `alloc` columns stay raw: subtracting a shared
  term moves a point estimate, it does not make a cell better measured.

  **This replaced a trim** — drop each strategy's single highest-CI shape —
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
  runs a median 5,000x the within-shape kind — the heterogeneity is this page's
  finding, not its error — so weighting by precision collapses the effective
  shape count from 33 to about nine and hands a quarter of the weight
  to the smallest shape in the set. Worse for the purpose: a catastrophically
  slow cell buys fewer samples, so it has a wider CI, so IVW discounts precisely
  the cells the trim used to delete — the same failure made continuous,
  not a repair of it.

  The *slope* rather than criterion's mean, because criterion never times one
  call: it times batches — one call, then four, then twenty — and every batch
  also pays for starting the timer and for the first pass through cold code
  and cold data. A mean divides each batch's time by its calls, so that fixed
  cost is smeared across them and weighs most in the small batches. The slope
  is the line through those points: how much more time one *additional* call
  adds, leaving the fixed part behind as the line's height at zero.
  On the microsecond shapes, hundreds of samples and no warm-up worth speaking
  of, the two agree. They part on the slow shapes, where the early batches run
  cold: there the mean reads high, and by different amounts for different
  strategies — which is exactly the part that dividing by `list` cannot cancel.
  It also keeps `CI%` and R² describing the number the table shows, both being
  properties of that same fitted line.
- **CI%** is the median across shapes of the slope's confidence interval
  as a percentage of the slope — "how many digits are real". 0.5% is three; 5%
  is one.
- **smp** is the median sample count. Criterion spends a time budget, so a slow
  call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`),
  the median over shapes of the `allocated` fit the harness now runs on every
  bench of every shape. The multiples were held to be shape-independent —
  refitted on a different shape, every one reproduced to within 0.4% —
  so that the median was a formality rather than a smoothing and the column did
  not move with what it was fitted on. **That is wrong**, and Run 6 (-O1)
  reproduced the refutation at full budget where a rough pass had found it.
  Re-derived on Run 9's cells and roster it is unanimous: **every one of the 32
  benched rows** varies by more than 5% from shape to shape, the median row
  by 2.00× and the worst by 5.10× (`bq-expand-b`, 1.00× to 5.10×), and the four
  shapes of identical `l` = 1800000 give `bq-expand` 2.000×, 2.111×, 1.000×
  and 2.639×. The spread narrowed as the roster was cut — Run 6's worst
  was an arm nothing times any more — and the property it measures did not.
  Every allocated fit sat at R² 1.000 on Run 6, so the spread is the quantity
  and not the measurement, and allocation being deterministic per call
  the budget does not bear on it either way. What does survive is the column:
  a median over a *pinned* shape set reproduces, which claim 7 now carries
  on a live basis, every allocation tier returning on its own level across
  a roster change. So read `alloc` as a statistic of a strategy **and** a shape
  set, and pin the shape set before comparing it across runs, exactly
  as the `time` column already asks. It is the one column the correction does
  not touch.

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *80* | *2.35x* | *its base arm, forced with one element* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.24* | *94* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *92* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *102* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *102* | *0.00x* | *the same, at the other end* |
| mut-odo-vecdims-add-in | 0.048 | 0.100 | 0.14 | 82 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa-distant* | *0.049* | *0.101* | *0.05* | *82* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.049* | *0.101* | *0.10* | *82* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.049** | 0.101 | 0.06 | 82 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both-down | 0.051 | 0.122 | 0.11 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both | 0.053 | 0.126 | 0.12 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-out | 0.054 | 0.131 | 0.15 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.081 | 0.217 | 0.19 | 83 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.087 | 0.214 | 0.37 | 82 | 1.33x | mutable `Int` scratch |
| bq-odo-gm-mulback | 0.090 | 0.181 | 0.16 | 80 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-adjacent* | *0.090* | *0.181* | *0.14* | *80* | *1.51x* | *A/A control* |
| *bq-odo-gm-mulback-aa-distant* | *0.090* | *0.179* | *0.07* | *80* | *1.51x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.090* | *0.162* | *0.05* | *76* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.091* | *0.172* | *0.12* | *76* | *1.33x* | *A/A control* |
| **bq-scan-rem-gm-mulback** | **0.091** | 0.176 | 0.06 | 76 | 1.33x | nothing (pure) |
| bq-expand-gm-mulback | 0.094 | 0.225 | 0.11 | 82 | 2.35x | nothing (pure) |
| bq-mut-runs | 0.096 | 0.230 | 0.40 | 76 | 1.33x | mutable `Int` scratch |
| *mut-odo-aa-adjacent* | *0.097* | *0.308* | *0.18* | *72* | *1.00x* | *A/A control* |
| mut-odo | 0.099 | 0.325 | 0.18 | 71 | 1.00x | new mutating `Vector` method |
| *build-aa-distant* | *0.100* | *0.326* | *0.94* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-distant* | *0.101* | *0.348* | *0.21* | *70* | *1.00x* | *A/A control* |
| *build-aa-adjacent* | *0.101* | *0.293* | *0.99* | *70* | *1.00x* | *A/A control* |
| bq-expand-b | 0.102 | 0.229 | 0.09 | 76 | 2.18x | nothing (pure) |
| bq-expand-qr-prim | 0.102 | 0.227 | 0.12 | 76 | 2.35x | nothing (pure) |
| **bq-expand** | **0.102** | 0.228 | 0.11 | 76 | 2.35x | **nothing -- SHIPPED** |
| *bq-expand-aa-distant* | *0.102* | *0.228* | *0.05* | *76* | *2.35x* | *A/A control* |
| *bq-expand-aa-adjacent* | *0.102* | *0.228* | *0.11* | *76* | *2.35x* | *A/A control* |
| build | 0.103 | 0.342 | 1.02 | 70 | 1.00x | new mutating `Vector` method |
| bq-expand-zf | 0.105 | 0.247 | 0.11 | 75 | 2.35x | nothing (pure) |
| *offtab-aa-adjacent* | *0.121* | *0.296* | *0.89* | *69* | *2.00x* | *A/A control* |
| offtab-scan-rem | 0.121 | 0.244 | 0.24 | 73 | 2.00x | nothing (pure) |
| offtab | 0.121 | 0.293 | 0.67 | 69 | 2.00x | mutable `Int` scratch |
| *offtab-aa-distant* | *0.122* | *0.332* | *0.22* | *68* | *2.00x* | *A/A control* |
| bq-mut | 0.140 | 0.312 | 0.22 | 66 | 1.33x | mutable `Int` scratch |
| bq-gen | 0.334 | 2.179 | 0.65 | 52 | 1.33x | nothing (pure) |
| gen-unsafe | 0.898 | 3.406 | 0.85 | 41 | 1.00x | -- |
| *gen-unsafe-aa-adjacent* | *0.899* | *3.427* | *0.88* | *41* | *1.00x* | *A/A control* |
| *gen-unsafe-aa-distant* | *0.902* | *3.710* | *0.84* | *40* | *1.00x* | *A/A control* |
| gen-quotrem | 0.905 | 3.514 | 0.51 | 41 | 1.00x | 1st attempt |
| *list-aa-distant* | *0.997* | *1.021* | *0.52* | *37* | *23.51x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.63 | 37 | 23.51x | -- |
| *list-aa-adjacent* | *1.001* | *1.050* | *0.55* | *37* | *23.51x* | *A/A control* |

`concat-runs` has no row, and neither do the other 23 arms the roster holds
and checks without timing: the reason is at each entry and the count
is [`--lint`'s](#the-reader-read-runpy). No row here is a first reading,
the roster's membership being Run 9's exactly, so every movement below
is a movement and not a new arm arriving.

**Three things in the table are the run's findings rather than its numbers.**
**The table mostly reproduced across a roster change that added twelve arms,
and where it did not, the movement is the arm's own width.** Four of the eight
yardstick rows are unmoved and four are not: `mut-flat-gm` 0.082 to 0.081
and `bq-expand` 0.103 to 0.102 are inside anyone's floor, while `offtab` 0.125
to 0.121 and `build` 0.099 to 0.103 are past this run's 2.19%. Both movers
are among the arms the new twins show to be the widest-spread in the roster,
which is what the twins were added to make visible: an A/A twin emits no code,
so what moved is how loosely those two measure and not what they compute.
**The ceiling reproduced again** — `mut-odo-vecdims` against the fastest pure
arm, `bq-odo-gm-mulback` at 0.090, on the figure [the
ruling](#the-mutable-ceiling-not-taken) turns on, and with the same denominator
Run 13 had. **And allocation is the column that says none of this is code —
but not by reproducing to the cell, which this pair is the first that cannot**:
845 of the 1080 earnest-allocator cells agree between the halves to 1e-4 and 235
do not, where every earlier pair agreed on all of them. The reader's own caveat
is why, and it was registered before the run: a pair varying the RTS nursery
moves this fit on identical code, by up to 9.4e-4 in the measurement
that established it and by 1.42e-3 here. A second partition of 48 near-zero
cells, of which 44 allocate at most 18 bytes a call, resolves nothing either way
— the mutable fills and `gen-quotrem` at 1.00x, the scan family and `bq-mut`
at 1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x
and `list` 23.51x. **This is the run where that column earns its keep**:
the halves differ by 5 to 25% in time on nearly every arm, and allocation says
none of it is a code difference, so the movement is the nursery and nothing
else. The reader's own caveat is worth carrying with it — a pair varying the RTS
nursery moves the fitted bytes by up to 9.4e-4 on identical code, where two
processes of one configuration agree to 4.9e-8, so agreement here is *to 1e-4*
rather than to the cell.

**The third is about the instrument, and it is the repetition's alone to find:
a sub-percent margin's win count is not stable across runs.**
`mut-odo-vecdims-add-in` against the arm it varies read 1.0009 at 13 wins of 24
in Run 10, **0.9934 at 21 of 24** in Run 13, and **0.9967 at 13 of 24** here,
sign p 0.84 — three runs, one roster order, and a count that has now
been to both ends and back. The geomeans differ by less than any of those runs'
floors and agree about the size of the margin; what moves is which side of zero
twenty-four near-ties fall on. So a sub-percent margin's win count is not more
stable than its geomean, which is worth having said plainly, the sign test being
what this page reaches for whenever the baseline is in doubt. Claim 9 did
the same thing in the same run, which is two independent cases of it.

**And one of Run 10's orderings needs restating rather than replacing.**
That run put both plain mutable fills past `bq-expand` on the aligned half,
`build` at 0.9367 of it and `mut-odo` at 0.9671; this run reads **0.9834**
and **0.9669**, so the point estimates still straddle it rather than settling
it. The win counts are 8 and 9 of 24 here against 8 and 9 there — the fill ahead
on the geomean while behind on most shapes, which is what a few large wins
against many small losses looks like, and what a sign test is for. Read the pair
as *the fills win big where they win*, and not as an ordering: at sign p 0.15
and 0.31 there is nothing here to order.


### What Run 15 compares against

**Run 15's regime, roster and basis are settled, and since 2026-08-16 its pair
is too: it repeats Run 14 with one variable changed.** The regime
is `-fspec-constr`, as every run since Run 8, and it is the regime the fix ships
in rather than a flag priced against the shipped one. The roster is Run 14's
1128 benches, 47 timed arms over 24 shapes, with every stride class at three
shapes. The basis is the `lookrts` recipe, unchanged and now twice used. **Run
14 left two candidates for what the other half varies, and Run 15 takes neither
whole**: its pair is Run 14's with `-A32m` in place of `-A1G`, so the roster
repeats — the second candidate, and what the drift band needs — while
the allocation area stays the variable at a nursery eight times the default
rather than two hundred and fifty-six times it. The repetition carries a second
reason that is not about the benchmark at all: Run 15 is the first run to use
the write-up machinery the [non-urgent list](#non-urgent-todo-list) registers,
and an installer is best tested against a run whose figures are already known,
where a figure landing outside the drift band is a defect in the tool rather
than a finding.

**The candidate not taken is the position term, and it stays the better
question.** Run 14 established that at `-A1G` an earlier bench in the same
process permanently slows a later one, by up to 57% on the arm measured, while
at the default nursery the same ladder is flat; that six of 23 shapes cause
it and one alone reproduces it; that `+RTS -H2G` does not fix it; and
that it survives GHC HEAD. What it did not establish is which property
of those six shapes does it — `conv1d-24` and `cnn-L1-24x24-c1` share `l`
and `sInner` and land on opposite sides. A pair varying nothing but roster
**order** would price how much of this page's per-shape scatter is that term,
which is the oldest open question here and now has a mechanism to hang on. [The
open list][open] carries the entry.

**The repetition is what Run 15's roster does, and Run 14 made it expensive
to skip.** Run 14 changed two things at once by accretion rather than by design
— twelve A/A twins and five class shapes — so its floor is over eighteen pairs
where every predecessor's was over six, and its class figures are over three
shapes where five classes had two. Neither is comparable with what came before,
and the next run is the first that could be. A repetition on this exact roster
would give the drift band a basis that carries, which Run 11 bought once
and the roster has since spent.

**That a pair must not vary the allocation area again was the ruling here,
and it was overruled on 2026-08-16.** What Run 14 established stands: at `-A1G`
the control half's absolutes carry a position term the basis half does not,
so the two halves are not subtractable and the steady-state cost had to come
from differencing outside criterion rather than from the run. `-A32m`
is the same variable at a thirty-second of the size, and what the pair reads
is whether the term is *visible* there. **The registered expectation is
that it persists** — registered as such in [the open list][open], with what
would break it — so a Run 15 control half free of it is the finding and
not the prediction — and would also be a half whose absolutes subtract, which
the `-A1G` one is not. Pricing the area properly still wants a runner that can
give one binary two RTS configurations, which `run-major.sh` does not do today,
and then the pair is one binary and no gate is owed at all — the note for Run
14's pair records that this was available and not taken.

Its columns will be `Run 15 (SpecConstr, max-skip +lookrts)`
and `Run 15 (SpecConstr, max-skip +lookrts +A32m)`. The table below is read
against the two Run 14 columns; the -O1 column stays the yardstick
for a comparison of the two regimes.

**Run 13 contributed two columns, and the second names a shim setting and an RTS
line at once.** `Run 13 (SpecConstr, max-skip)` is the basis, Run 12's basis
recipe unchanged; `Run 13 (SpecConstr, max-skip +lookrts)` is the same source
and compile with the shim's look-through and an RTS default of `-I0 -T -M8G`
in place of `-T -M2G`. The two changes are deliberately not separable — the pair
varies both by request — so read the columns as pricing the package and never
either change alone.

**Run 12 contributed two columns, and both name a shim rather than a build.**
`Run 12 (SpecConstr, max-skip)` is the basis;
`Run 12 (SpecConstr, max-skip +procalign)` is the same source, shim and compile
with `-fproc-alignment=64` added, which pins every procedure start to a 64-byte
boundary. The rule against pruning a column is joined by one against **merging**
two: folding two halves into one column would put back, in the one table built
to outlive every artifact, exactly the term the pairing exists to separate.
`--check-doc` catches one half of that: a run named aligned must also be named
unaligned, so pruning Run 10's unaligned column fails it. Pruning an aligned
column, merging two, and naming a second half accurately are the reading's
to catch — the check cannot demand an unaligned half of every pair without
failing the last two runs, which have none, nor an aligned column of every run
without failing Runs 6 through 9, which had none either.

**Run 11 contributed two columns, and the second names a shim rather
than a build.** `Run 11 (SpecConstr, aligned)` is the basis, and is Run 10's
aligned binary run again; `Run 11 (SpecConstr, max-skip)` is the same source
and compile with the assembler shim padding only the heads that needed it.

**What each pair of columns is for differs, and the table cannot say
so itself.** Run 10's two are one source and one compile apart and price
**layout**: 12 to 14% on the two arms whose loop straddled a cache line,
a percent or two the other way where none did. Run 11's two are one *shim* apart
and price what that padding costs when it rescues nothing: nothing below 0.99
and up to 1.06 against the fully padded half. Run 12's two are one *compiler
flag* apart and price what pinning every procedure start costs on top
of that shim: `offtab` 0.125 against 0.131 is the widest of them, and the flag
is the dearer build. Run 13's two are one shim setting and one RTS line apart,
both at once, and price the package at nothing: `offtab`'s 0.125 against 0.121
is the widest of them and sits inside the drift band, the paired reading putting
it at 1.0269. Reading Run 11's aligned column against Run 10's aligned one
is a further thing again — the same binary twice, which is drift and nothing
else.

**Neither of the older columns is to be pruned**, however much each looks like
a leftover. The -O1 one is the only place Run 7's basis survives, so deleting
it leaves any comparison of the two regimes with no yardstick at all and nothing
to recover one from once the artifacts are gone — and it is now the *only* form
that comparison can take, the -O1 run that would have replaced this column being
retired with its premise; `--check-doc` fails if the column disappears. The Run
8 one is now load-bearing for a second reason: its four bottom rows name arms
**nothing times any more**, so with Run 8's Results table replaced above
and its JSON deleted, this is the only record they have left. The rows nearest
the decisions, in every regime that has measured them, so no comparison needs
another section:

| strategy | Run 14 (SpecConstr, max-skip +lookrts) | Run 14 (SpecConstr, max-skip +lookrts +A1G) | Run 13 (SpecConstr, max-skip) | Run 13 (SpecConstr, max-skip +lookrts) | Run 12 (SpecConstr, max-skip) | Run 12 (SpecConstr, max-skip +procalign) | Run 11 (SpecConstr, aligned) | Run 11 (SpecConstr, max-skip) | Run 10 (SpecConstr) | Run 10 (SpecConstr, aligned) | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | **0.049** | 0.051 | 0.049 | 0.049 | 0.049 | 0.049 | 0.048 | 0.048 | 0.048 | 0.049 | 0.048 | 0.053 | 0.054 |
| `mut-flat-gm` | **0.081** | 0.083 | 0.082 | 0.082 | 0.081 | 0.082 | 0.081 | 0.081 | 0.083 | 0.081 | 0.080 | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.087** | 0.088 | 0.087 | 0.087 | 0.087 | 0.088 | 0.087 | 0.086 | 0.085 | 0.088 | 0.088 | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.090** | 0.095 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.091** | 0.090 | 0.091 | 0.090 | 0.090 | 0.091 | 0.089 | 0.090 | 0.090 | 0.089 | 0.090 | 0.090 | 0.119 |
| `bq-expand` | **0.102** | 0.107 | 0.103 | 0.102 | 0.102 | 0.102 | 0.103 | 0.103 | 0.102 | 0.102 | 0.105 | 0.102 | 0.127 |
| `build` | **0.103** | 0.097 | 0.099 | 0.099 | 0.098 | 0.098 | 0.096 | 0.100 | 0.110 | 0.096 | 0.114 | 0.095 | -- |
| `offtab` | **0.121** | 0.121 | 0.125 | 0.121 | 0.125 | 0.131 | 0.125 | 0.123 | 0.123 | 0.124 | 0.115 | 0.146 | -- |
| `mut-flat` | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.108 | 0.097 |

Every column but the last is a published geomean over the same 24 shapes,
and the SpecConstr ones share a denominator too — `list` moved 0.47% between
the two Run 13 columns, 0.24% between the two Run 12 ones, 0.7% between the two
Run 11 ones, and 0.6% and 0.4% inside Run 10 and against Run 9 — so they may
be subtracted and not merely ordered, which is what the -O1 column cannot do
at an 8% baseline shift. **Across the Run 11/Run 12 boundary it holds more
loosely**, the two runs sharing no binary, Run 11's having been deleted —
but its **JSONs were kept**, so the baseline comparison is measured rather
than guessed: `list` reads **0.9953** of its Run 11 max-skip self over the 24
shapes, scattering 0.9611 to 1.0431 per shape. Half a percent on the geomean
is small enough to subtract across; five percent on a cell is not, so read
a per-shape difference of a point or two there as unresolved rather than
as a movement. Read the two Run 12 columns against each other for the **flag's
term**: `offtab`'s 0.125 against 0.131 is the same arm in the same run, one
compiler flag apart. Read the two Run 11 columns for the **padding term** —
`build`'s 0.096 against 0.100, one shim apart — and the two Run 10 columns
for the **layout term**, `build`'s 0.110 against 0.096, and the -O1 column
for orderings only.

**Each stride class's yardstick is its own table below.** Run 8 re-ran every
class with the populations pinned, and every run since has again, so each
class's paragraph carries what the last change moved and the table above
it is what Run 13 reads against. **The two sides of a class comparison across
the Run 11/Run 12 boundary are not the same build**, and this is the one place
that bites: Run 11's class tables are its *aligned* half's, Run 12's
are its *max-skip* basis half's, and the main set prices that difference
at nothing below 0.99 and up to 1.06. So read a class figure that moved a point
or two across that boundary as the shim rather than as the class, and take
the two Run 12 columns above as what a same-build comparison looks like.
From Run 13 on, both sides are max-skip again.

And because a geomean cannot say *where* it moved, the **fingerprint** below
is kept so a future disagreement can be localised rather than only noticed.
Its membership is a rule, not a habit: the shipped arm, the rows the Results
table bolds, and any arm an open question names — `mut-odo` and `build` sit here
on [the placement question](#what-is-open), which they are now the answer
to rather than the sharpest form of — and an arm leaves when its question
closes, the roster cut having taken two out that way. An arm nothing measures
cannot be the subject of a future disagreement to localise, and what is given up
when one goes is the per-shape half alone, its geomean staying in the yardstick
table above. `list`'s own net per call rides along, guarding the baseline
at every shape where the anchors guard three, and converting any ratio beside
it back to absolute time. Allocation stays medians-only on purpose:
deterministic per call, so a run that raises an allocation question re-derives
it within itself. `./read-run.py RUN.json --fingerprint` emits both tables —
paste them whole, transcribing nothing by hand, since hand-carrying this table
once left two of Run 6's cells standing under Run 7's name, and the first
emitted paste is what caught them. The column heads shorten the arm names
as the stretch table's do: scan-rem-gm is `bq-scan-rem-gm-mulback` and vecdims
`mut-odo-vecdims`. And the [stretch table][pershape] is the same kind of record
for `bq-expand-b`, on the shapes chosen to stress orderings — compare
it the same way. It lost a `lemire-out` column to this same rule on the same
day, and says so.

| shape | `sInner` | `l` | `list`, net | bq-expand |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.32 µs | 0.148 |
| `cnn-L1-6x6-c1` | 3 | 324 | 6.43 µs | 0.205 |
| `stretch-rank12` | 2 | 4096 | 99.3 µs | 0.228 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 101 µs | 0.172 |
| `conv1d-24` | 3 | 5184 | 88.5 µs | 0.105 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 324 µs | 0.129 |
| `gather48-src-50` | 3 | 22500 | 382 µs | 0.099 |
| `stretch-rank10` | 3 | 59049 | 1.23 ms | 0.136 |
| `stretch-coprime-r7` | 13 | 60060 | 1 ms | 0.107 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.17 ms | 0.111 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.58 ms | 0.114 |
| `stretch-primes` | 89 | 250357 | 3.51 ms | 0.102 |
| `stretch-inner1` | 1 | 500000 | 11.6 ms | 0.076 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 26.2 ms | 0.061 |
| `vgg-14-c512-k3` | 3 | 903168 | 30 ms | 0.089 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 16.4 ms | 0.103 |
| `stretch-inner256` | 256 | 1750784 | 48.3 ms | 0.066 |
| `stretch-pow2stride` | 64 | 1769472 | 49.1 ms | 0.069 |
| `stretch-r5-8x432` | 8 | 1769472 | 50.8 ms | 0.053 |
| `stretch-square-1341` | 1341 | 1798281 | 25.3 ms | 0.128 |
| `stretch-bigstride` | 3 | 1800000 | 41.4 ms | 0.070 |
| `stretch-tab7MB` | 2 | 1800000 | 33.7 ms | 0.098 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 35.7 ms | 0.072 |
| `stretch-wide-2xM` | 2 | 1800000 | 33.6 ms | 0.087 |

| shape | scan-rem-gm | vecdims | mut-odo | build |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 0.152 | 0.082 | 0.193 | 0.176 |
| `cnn-L1-6x6-c1` | 0.137 | 0.094 | 0.219 | 0.219 |
| `stretch-rank12` | 0.139 | 0.101 | 0.325 | 0.342 |
| `cnn-L1-24x24-c1` | 0.103 | 0.073 | 0.219 | 0.207 |
| `conv1d-24` | 0.106 | 0.061 | 0.153 | 0.161 |
| `lenet-L1-28-c1-k5` | 0.099 | 0.051 | 0.133 | 0.135 |
| `gather48-src-50` | 0.105 | 0.057 | 0.122 | 0.139 |
| `stretch-rank10` | 0.101 | 0.065 | 0.187 | 0.175 |
| `stretch-coprime-r7` | 0.087 | 0.032 | 0.066 | 0.066 |
| `cifar-L2-16-c64-k3` | 0.090 | 0.053 | 0.153 | 0.163 |
| `cnn-L2-24x24-c32` | 0.090 | 0.055 | 0.138 | 0.146 |
| `stretch-primes` | 0.095 | 0.029 | 0.031 | 0.031 |
| `stretch-inner1` | 0.076 | 0.097 | 0.280 | 0.253 |
| `alexnet-L2-27-c48-k5` | 0.053 | 0.025 | 0.054 | 0.051 |
| `vgg-14-c512-k3` | 0.058 | 0.034 | 0.085 | 0.096 |
| `alexnet-L1-55-c3-k11` | 0.093 | 0.035 | 0.059 | 0.065 |
| `stretch-inner256` | 0.051 | 0.015 | 0.016 | 0.016 |
| `stretch-pow2stride` | 0.078 | 0.071 | 0.071 | 0.071 |
| `stretch-r5-8x432` | 0.050 | 0.019 | 0.036 | 0.038 |
| `stretch-square-1341` | 0.176 | 0.089 | 0.091 | 0.090 |
| `stretch-bigstride` | 0.075 | 0.039 | 0.104 | 0.106 |
| `stretch-tab7MB` | 0.107 | 0.067 | 0.166 | 0.160 |
| `stretch-tall-Mx2` | 0.064 | 0.018 | 0.018 | 0.018 |
| `stretch-wide-2xM` | 0.104 | 0.067 | 0.147 | 0.176 |

Two rows to read first, and the pair is derived rather than remembered:
`stretch-square-1341` and `stretch-pow2stride` are the only two shapes where
**both** arms tying at the head of the pure tier *lose* to `bq-expand`, so treat
a disagreement on either as the shape. They fail differently, which is why both
are named. On `stretch-square-1341` the mutable fills win it back outright
(`mut-odo-vecdims` 0.089 against `bq-expand`'s 0.125) while the pure arms trail;
on `stretch-pow2stride` the two families converge instead, four of the five
fingerprint arms landing inside two thousandths of each other ([the per-shape
section][pershape]). Taking the tier's leaders one at a time gives eight shapes
and three, which is why the sentence says both. `stretch-inner1` has `sInner` 1,
so anything special-casing a unit dimension behaves differently there
by construction.


### The claims Run 15 should test

**Run 14's verdicts on Run 13's nine claims first**, since a run reports breaks
rather than re-deriving the table. **Every claim held — 13 of 13 registered
orderings**, for the fourth run running and again on all 24 shapes. Each claim's
`Readings:` paragraph is installed from the basis (`run14-lookrts`) half
by `--claims --in-place`; the paragraph above it is the reading of those figures
and carries none of them itself.

**What moved is in the sign tests again, and this run has the sharpest case
of it yet.** Claim 9's `bq-expand-b` / `bq-expand` crossed *into* significance
on Run 13 at 19 wins of 24 and has crossed straight back out, reading **8 of 24
at p 0.15** on a geomean that barely moved, 0.9909 to 0.9940. A margin of six
thousandths cannot be worth a verdict either way, and two consecutive runs
disagreeing about its sign test while agreeing about its size is the plainest
evidence on this page that the count is the looser instrument. Claim 4's first
link did the same more mildly, 16 of 24 to 14 of 24. **Read claim 9 by its two
shapes, as it says**, and they are where they have been for seven runs.

**Claim 1 held on all three links.** The middle link, the one Run 10's two
halves parted over, reads the aligned figure for a fifth run and gained a win
rather than losing one.

Readings: `mut-odo-vecdims` / `mut-flat-gm` 0.5993, 22 of 24, sign p 3.6e-05;
`mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9305, 21 of 24, sign p 0.00028;
`bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9701, 19 of 24, sign p 0.0066.
3 of 3 registered orderings held.

**Claim 2 held, and its sign test went soft.** On `offtab` / `bq-expand`
the ordering is unchanged and the margin a fifth as before, but the count moved
from Run 13's 5 to 7 and the p from its 0.0066 to the edge of significance.
The margin is the finding and the p is not, which this claim's own entry has
said since Run 9.

Readings: `bq-expand` / `bq-mut` 0.7292, 20 of 24, sign p 0.0015; `offtab` /
`bq-expand` 1.1860, 7 of 24, sign p 0.064. 2 of 2 registered orderings held.

**Claim 3 held.** A mul-back output is worth 8% on the shipped build
under this flag, as on every run since Run 10.

Readings: `bq-expand-gm-mulback` / `bq-expand` 0.9243, 20 of 24, sign p 0.0015.
1 of 1 registered ordering held.

**Claim 4 is a tie on both its halves, for the fifth run running.** Both
readings are the claim — the scan against its own build control, and the scan
against `bq-expand` — and the second is again a double-digit point estimate
on a tied sign test, the shape that invites quoting the point estimate alone.

Readings: `bq-scan-rem-gm-mulback` / `bq-expand-gm-mulback` 0.9587, 14 of 24,
sign p 0.54; `bq-scan-rem-gm-mulback` / `bq-expand` 0.8861, 16 of 24, sign p
0.15. 2 of 2 registered orderings held.

**Claim 5 held.** Among the builds only the mutable odometer still beats
`bq-expand`.

Readings: `bq-expand` / `bq-gen` 0.3059, 22 of 24, sign p 3.6e-05; `bq-mut-runs`
/ `bq-expand` 0.9351, 23 of 24, sign p 3e-06. 2 of 2 registered orderings held.

**Claim 6 held and its alarm again had nothing to answer for.** The count
and the p are the last two runs', on a margin a point and a half lower.
The anchor the claim tells you to check first is sound, the three absolutes
moving +0.86%, +2.10% and +0.74% against Run 13.

Readings: `gen-quotrem` / `list` 0.9048, 11 of 24, sign p 0.84. 1 of 1
registered ordering held.

**Claim 7 held, and is the claim this run leans on.**

**Claim 8's structural half stands.** Every pure arm still runs its output
through the single in-order `vGenerate` over an `m`-length table, and the arms
that fall behind still lose on their table build; `bq-expand-zf` (0.105)
and `offtab-scan-rem` (0.121) still populate the gap to `bq-gen` (0.334).

**Claim 9's per-shape half survived a seventh run and its sign test crossed
back.** Where Run 13 read 19 of 24 at 0.0066, this run reads a tie on a geomean
six thousandths away, and `bq-expand-zf` / `bq-expand` is behind as before.
**What is stable is the shapes**: `bq-expand-b`'s two best cells are the same
two named in each of the last seven runs, which is why the reading below
verifies that pair rather than the geomean.

Readings: `bq-expand-b` / `bq-expand` 0.9940, 8 of 24, sign p 0.15, best two
cells `stretch-inner1` and `stretch-wide-2xM`; `bq-expand-zf` / `bq-expand`
1.0287, 2 of 24, sign p 3.6e-05. 2 of 2 registered orderings held.

Restated as the predicates the next run checks, and carrying no reading
of its own: the figures each was last measured at are in the `Readings:`
paragraphs above, so an entry here changes when a claim is re-aimed and not when
a run moves a margin. **All of them are `-fspec-constr` claims, which
is the regime the fix ships in** — the file the solution is added to sets
the flag — so they are the set that decides, and a run at -O1 would test Run 7's
instead, the two differing in more than their numbers. **What they are not read
in is the caller's allocation regime**, every figure here being taken
at the default 4 MB nursery against a prevailing
`-with-rtsopts=-A1G -I0 -T -M8G`; that gap is what Run 14's pair is built
to price, and no claim below is qualified by it yet. **And all of them are read
against a measured drift band rather than a layout span**, which is what
the last three runs bought. A roster *order* change alone moved arms 0.966
to 1.142 between Run 9 and Run 10, and that is what a margin used to have
to clear; with the layout pinned, a repetition moves an arm by at most 3.3%
and most of them by under 1.5%, so a margin above a few percent is now evidence
of a strategy. **Run 13 is the first pair here to hold every tracked loop at one
offset in both halves**, which is what lets its arm-by-arm comparison be read
as the package costing nothing rather than as two terms cancelling. A claim
resting on an arm whose own loop the shim skipped — `list`'s, which is library
code — is still decidable nowhere until that loop is read. **And the pinning
claim is measured only in its weak form**: adding `mut-flat-gm-nosum` left every
tracked loop at the same address, but a `Force` arm reuses a rostered function
and emits no code for emission order to move. The strong form wants an arm
that emits its own, and until one is added the claim covers additions that cost
nothing to place.

**The list needed no re-aiming this time either**, the roster it was rewritten
onto before Run 8 being the roster Run 13 ran: every claim below names an arm
this run timed. Five full runs on that roster is the evidence that keeping
the *question* and changing the *arm* was the right repair — the unconditional
counterparts were written so that dropping a precondition would not drop
a question with it, and none of them dropped one.

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` <
   `bq-odo-gm-mulback`, the whole ordering read on unconditional arms.
   The middle link is the one this page has seen a layout term move — 0.9708
   at 15 of 24 on Run 10's unaligned half against 0.9293 at 22 on its aligned
   one — and on a placed layout it has now read the aligned figure four runs
   running. The ceiling's ordering has survived five runs, two changes of basis
   and a repetition.
2. `bq-expand` < `bq-mut` while `offtab` is *behind* `bq-expand`: the `m`-length
   table beats both the mutable scratch that builds it and the `l`-length table
   that replaces it. Run 9 left the second of those at 1.0969, inside the layout
   span and undecidable there; Run 10 decided it at 1.2224, and the four runs
   since have put it between 1.2095 and 1.2224 while the sign test went
   from 0.064 to 0.0066. The margin is the finding and the p is not.
3. `bq-expand-gm-mulback` < `bq-expand`: a mul-back output pays on the shipped
   build under this flag. `bq-expand-lemire-out` — the arm the question used
   to be asked through — is untimed for its `l < 2^32` precondition and has
   no unconditional form, Granlund-Montgomery offering no `out` analogue
   that yields quotient and remainder together.
4. `bq-scan-rem-gm-mulback` ties its own build control `bq-expand-gm-mulback`,
   on an interval covering one, **and ties `bq-expand` too by the sign test**,
   where Run 9 had the second at 18 of 24 and called it outright. The two differ
   in `baseOffsetsScanRem` against `baseOffsetsExpand` and in nothing else,
   their output code being identical, so the first reading is about builders
   and the second about the shipped arm. Both readings are the claim;
   a double-digit point estimate sitting on a tied sign test is exactly
   the shape that invites quoting the point estimate alone.
5. `bq-expand` < `bq-gen`: the build ordering, trimmed to its timed arms —
   `offsets-quot` and `bq-gen-lemire` were its two ends and are both untimed,
   so the run cannot re-read the gap widening or the ending. That refutation
   stands on Run 7 and Run 8, which is enough for an idea kept only so
   that it is not re-proposed. Among the builds only the mutable odometer still
   beats `bq-expand`, the scan build being level rather than ahead (claim 4).
   So `bq-expand` is still the fastest build that needs neither a class
   extension nor explicit mutation.
6. `gen-quotrem` ties `list` — the first attempt's arithmetic stops being dearer
   than the list's allocation once the flag takes its own allocation to 1.00x
   against the list's 23.5x, which is the mixed picture this suite exists
   to have refuted, arriving by a route nobody proposed. The `cm-gather` <
   `list` half is untimed and stands as Run 8's. A break here would mean
   something changed in `list` or in GHC, not in a strategy — check the anchor
   before anything else, as Run 8 had to and the five runs since did not.
7. Allocation, median multiples of the result on this basis: the mutable fills
   1.00x, `gen-quotrem` also 1.00x, `bq-mut` and the scan family 1.33x,
   `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x, `list` 23.5x.
   Every one of the 34 rows Run 12 also carried reproduced its figure,
   `mut-flat-gm-nosum` being this run's addition, and the cells behind them
   agree across the pair's halves on all 792 that allocate in earnest, which
   is what makes this the claim to check first when anything else moves:
   allocation is deterministic per call, so a level that *does* move is a code
   change and never a slot.
8. Every pure arm in the fast tier runs its output through the single in-order
   `vGenerate` over an `m`-length table, and a `bq-*` arm that falls behind
   loses on its table build and not on its output. Read the structure and
   not a threshold: the gap the claim used to be stated across is populated,
   `bq-expand-zf` and `offtab-scan-rem` lying between the leading tier
   and `bq-gen`.
9. **Read this one per shape and not on its geomean.** `bq-expand-b`'s two best
   cells are `stretch-inner1` and `stretch-wide-2xM`, the rank-2 views with one
   huge outer dimension where seeding from `enumFromStepN` replaces the whole
   `concatMap` build — the same two shapes in every run since Run 8, which
   is the stable part of this claim. The geomeans are not, and the series
   is why: across Runs 8 to 13 `bq-expand-b` / `bq-expand` read 0.996, 0.9678,
   0.9943, 0.9819, 0.9923 and 0.9909, its sign test crossing into significance
   only on the last of them, while `bq-expand-zf` / `bq-expand` went 3.6%
   behind, then level at 1.0028, then 1.0325, 1.0197, 1.0256 and 1.0265. Both
   series are closed at Run 13 and not extended per run; what this run read
   is above.

Each ordering is one line of `--claims`, whose manifest now carries
the registered expectation — the direction of the geomean, a tie by sign test,
or claim 9's two best shapes — and prints HELD or BROKE beside the paired
geomean, interval and sign test. `--claims --in-place` then installs
that arithmetic as each claim's `Readings:` paragraph above, so a run no longer
transcribes it at all; what stays the reading's is whether a HELD margin moved
and whether a movement clears the floor, and a BROKE is what obliges
the paragraph above its reading to be rewritten rather than requoted. **A claim
with no named invocation is a gap in this list, not a claim to be checked
by hand**: where a session has to invent the computation it will invent a wrong
one, which is how claim 7 came to be read off the raw fitted bytes, explained
by a mechanism the previous pair refutes, and then "corrected" onto a rounded
print. It has `--compare --alloc` now. Claim 8 is the one still without one,
read off the table by eye. **The general form, and it is a standing instruction
rather than an observation: if a write-up hand-rolls a script to answer
something the reader should answer, that is a defect report against the reader**
— fix it there, before the sentence it was written for, or the next run invents
its own wrong version.

**And for each stride class, the same three properties, now carrying Run 14's
verdicts**, the details beside each class's table:

1. **`bq-expand`'s `worst` stays under 1.** Held in every class — 0.171
   at its highest, under `rev`, and 0.228 on the main set — so the shipped
   fallback was never slower than the `list` it replaced, on any shape of any
   class the library can produce, in any regime, roster or layout this page has
   run. This is the property the classes exist to test, no geomean can state it,
   and a break would have been the one result here to bear
   on `Data/Array/Internal.hs` directly.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-scan-rem-gm-mulback` the fastest pure arm, `bq-expand` behind both.
   The first clause, read as the vecdims family's rather than one arm's —
   the ruling Run 9 left, and no run has yet separated them — holds in eight
   of the nine populations and breaks in `reshape1` alone, where the flat fills
   own the top outright, `bq-mut-runs-gm-mulback` reading 0.2928
   of `mut-odo-vecdims` there. *Which* member of the family leads is
   not a stable fact and moved twice again: `mut-odo-vecdims-add-in` heads
   `window` and the main set, `add-both-down` heads `bcast`, `bcastmid`
   and `scaled`, and the arm itself heads `rev`, `revsome` and `slice` —
   `bcastmid` and `slice` changing hands against Run 12. **The second clause
   recovers, after three runs of falling**: it holds in five of the nine (`rev`,
   `revsome`, `bcastmid`, `slice`, `window`) where Run 12 counted three, Run 11
   four and Run 10 six. Of the four breaks, two are ties the sort had to settle
   — the main set to `bq-odo-gm-mulback` at 0.9949 and `scaled`
   to `bq-expand-gm-mulback` at 0.9971, whose two arms print the same figure
   to three digits — and two are margins, `bcast` at 0.8862 and `reshape1`
   at 0.4998, both to `bq-expand-gm-mulback`. So the pure tier is still tight
   enough that the slot follows the sort, and this run's count moved up rather
   than down without any arm winning something new. The third clause holds
   in all nine if read as *behind whichever arms lead*, and breaks on the arms
   it names in two rather than Run 12's three — `bq-expand` (0.8609) ahead
   of `mut-odo-vecdims` in `reshape1` and (0.9868) ahead
   of `bq-scan-rem-gm-mulback` in `bcast` — `revsome`'s tenth-of-a-percent tip
   having gone back the other way at 1.0513. Each is read in its class's
   paragraph, and [the `sInner`
   ruling](#per-shape-where-the-geomean-hides-the-ordering) is what they bear
   on.
3. **The allocation tiers survive**: the mutable fills at the result vector,
   `bq-expand` at one to four times it, `list` at an order of magnitude more.
   Where a level moves it is the class's own `m` showing through, exactly
   as this property warned — `bq-expand` at 1.07x on `scaled` (`m` of 1
   and 2,000) and 4.22x on `reshape1` (`m = l`) — the ordering of tiers unbroken
   everywhere, and every level the same to the digit as Run 12's, Run 11's
   and Run 10's.

`--pair` works within a class JSON exactly as within the main one, and is still
the way to compare two arms; its bootstrap interval, over three shapes, is worth
less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier
in two. A **new pure `Vector` method** delegates to a pure function the vector
package already ships for every carrier — `unfoldrExactN`, `backpermute`,
the `concatMap`/`enumFromStepN` pipeline — so it fights only *minimal*
in orthotope's pure-and-minimal API rule; the **new mutating `Vector` method**
the direct fills need is the [mutable ceiling](#the-mutable-ceiling-not-taken)'s
ask, which *pure* barred outright until the amendment there turned the bar
into a weight. `offtab` is the `Vector`-class-expressible shape of these gathers
— output by plain `vGenerate` over a concrete offset table — so its own cell
names only its mutable `Int` scratch. And the geomean weights every benchmarked
shape **equally**, so a figure here is a ranking statistic, not a claim about
total work saved: the small shapes count as much as the largest.


### The stride classes, run by run

**Run 14 (SpecConstr, max-skip +lookrts) records every class on BOTH halves**,
one process each, in [the sequence](#making-a-major-benchmark-run) — sixteen
class processes where every run before this had eight. Every table below
is still the **basis half**'s, so the published figures are at the default
nursery as they have always been; what the second half buys is that a pair's
variable can now be read on a class, which is what answered this run's `scaled`
question and what no earlier run could have asked. Read across the halves
and the direction is one-sided without being uniform: of the 336 arm-comparisons
the eight classes carry, **316 put the 1 GB half slower and 20 put it faster**,
on a spread from 0.6078 to 1.2860. Only `rev` has no exception, and `reshape1`
has six. The movement is larger than the main set's and carries the same
position term the chapter head describes, so take its direction and not its size
— and read the exceptions as real rather than noise, several of them clearing
this run's floor many times over. This section fixes the form, so that a class
is written up the way the main set is rather than however the session that ran
it chose. The form is this section's own prose and is not a run's to rewrite,
exactly as the column definitions under [Results](#results) outlive the table
they explain; what a run replaces is everything below the form. What a class
*is*, and the two rulings that keep it a population of its own, are [in the goal
chapter](#the-stride-classes-and-what-they-cover).

First, one table over all of them, so that an inversion is visible without
reading every class's table. Every figure in it is transcribed from a class's
own table below — none is computed here, and none is an average across classes,
there being no such population to average over. Its header, fixed here so a run
fills rows and never reshapes columns:

    | class | shapes | bq-expand | worst | fastest pure | ceiling | floor |

That header line is written out twice in this file, once here as the spec
and once as the table's own, and the two are the same text — so a session
pasting a run's rows must anchor at the line start and check that it landed
on the unindented one. Getting that wrong put Run 8's rows under this paragraph
and left Run 7's standing in the table, both checks passing, because the check
looked the table up the same wrong way the paste did.

`bq-expand` and `worst` are the shipped row's two columns in that class's table;
*fastest pure* and *ceiling* are the leading pure and mutable arms, each
with its name, since which arm leads is half of what the column says; *floor*
is the largest deviation from 1 among that process's six A/A controls. A cell
that breaks one of [the three properties](#the-claims-run-15-should-test)
is bolded, and the class's own paragraph says what broke.

Then one block per class, in `classViews`' order — `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled` — each carrying the same
five things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause,
   and its shapes with their `l` and `sInner`, which is what makes the table
   under it readable without `Main.hs` open;
2. the table `--block --in-place` installs from `$R-<basis>-$c.json`, whole
   and never edited — six columns, with the emphasis carried over from the main
   table so the shipped row is found at a glance, and `needs` left to that table
   as a property of a strategy rather than of a population;
3. its own controls, off `--aa`: the A/A deviations with their spans, the two
   `sum-only` halves, and the in-situ term from the `-nosum` arms —
   this process's own floor and its own three gates, neither inherited nor lent;
4. its provenance and its anchor: elapsed time and the two heap peaks
   from that process's stderr line, its population's size from the reader's
   first line ([why not both from one place](#making-a-major-benchmark-run)),
   and `list`'s absolute per-call time on one of its shapes, raw and net.
   The main set's three anchors guard a baseline that moves for every population
   at once; this one guards a baseline that could move for this mechanism alone,
   which is the case a table of ratios hides completely. A three-shape class
   adds one line here — the bolded rows' per-shape net ratios, in the lead's
   shape order — because its table under-determines its cells, where a two-shape
   table carried them already, `time` and `worst` jointly fixing both; every
   class is three-shape now, so the line always prints;
5. the cross-half reading, one line, from `--compare` against the other half's
   JSON for the same class — how many of the population's arms move, which way,
   and the spread. Both halves have run every class since 2026-08-14 and
   this is where that is read: a pair's variable can act on a class and
   not on the main set, which is how Run 14 answered its `scaled` question.
   A run whose halves differ in nothing a class can see says so in a clause;
6. one paragraph of what the class says, and none where it says nothing:
   an ordering that inverted, a `worst` above 1, an allocation tier that moved,
   a mechanism showing through a single cell. A class that reproduces the main
   ordering gets one sentence saying so, that being a result and reading as one.

`./read-run.py RUN.json --block` assembles items 2 through 4's mechanical parts,
and `install-tables.sh` now writes them in in one call — table, controls,
the provenance and anchor skeleton, and a three-shape population's per-shape
line; the lead and the paragraph stay the author's, a skeleton writing
no findings.

The blocks carry no headings of their own. One per class would crowd
the contents and the replace list alike, where a bolded lead reads the same
and lets one link cover the section — which is what `--check-doc`'s coverage
check counts.

| class | shapes | bq-expand | worst | fastest pure | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.106 | 0.171 | `bq-expand-gm-mulback` 0.101 | `mut-odo-vecdims` 0.049 | 8.83% |
| `revsome` | 3 | 0.106 | 0.133 | `bq-scan-rem-gm-mulback` 0.105 | `mut-odo-vecdims` 0.053 | 7.82% |
| `bcast` | 3 | **0.078** | 0.097 | **`bq-expand-gm-mulback`** 0.071 | `mut-odo-vecdims-add-both-down` 0.026 | 7.25% |
| `bcastmid` | 3 | 0.094 | 0.132 | **`bq-odo-gm-mulback`** 0.085 | `mut-odo-vecdims-add-in` 0.036 | 7.91% |
| `reshape1` | 3 | 0.104 | 0.159 | **`bq-odo-gm-mulback`** 0.055 | **`mut-flat-gm`** 0.034 | 7.19% |
| `slice` | 3 | 0.115 | 0.133 | `bq-scan-rem-gm-mulback` 0.102 | `mut-odo-vecdims-add-in` 0.039 | 4.70% |
| `window` | 3 | 0.118 | 0.130 | **`bq-odo-gm-mulback`** 0.091 | `mut-odo-vecdims-add-in` 0.066 | 8.48% |
| `scaled` | 3 | 0.104 | 0.104 | **`bq-expand-gm-mulback`** 0.093 | `mut-odo-vecdims-add-both-down` 0.029 | 1.94% |

**Every class is three shapes now**, where five of them carried two before,
so a figure here is over a larger population than its Run 13 counterpart
and the two are not subtractable. **The floor column is on eighteen A/A pairs
where Run 13's was on six**, and the twelve added sit on the widest-spread arms:
`build`'s pair carries the floor in five of the eight classes, and `offtab`'s,
`gen-unsafe`'s and `mut-odo`'s in one each. Read the column as this run's own,
not against the predecessor's — the head of the run chapter says the same
of the main set's.

`bq-scan-rem-gm-mulback` holds the pure slot in **two** classes where Run 13 had
it in five, losing `rev`, `bcastmid` and `window`. Only `rev`'s loss is a tie
the sort had to settle — it and `bq-expand-gm-mulback` both print 0.101,
so that cell is unbolded — while `bcastmid` goes by a thousandth and `window`
by nine, both bolded as breaks. What did not move is the shipped arm's `worst`,
under 1 in all eight.

**`rev` — every stride negated, offset at the top: the view `rev` on every axis
builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.03* | *137* | *2.52x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.05* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.01* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.049* | *0.073* | *0.01* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.049** | 0.073 | 0.03 | 138 | 1.00x |
| *mut-odo-vecdims-aa* | *0.050* | *0.073* | *0.07* | *138* | *1.00x* |
| mut-odo-vecdims-add-in | 0.051 | 0.077 | 0.05 | 138 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.052 | 0.079 | 0.04 | 137 | 1.01x |
| mut-odo-vecdims-add-both | 0.053 | 0.083 | 0.06 | 137 | 1.01x |
| mut-odo-vecdims-add-out | 0.055 | 0.086 | 0.06 | 136 | 1.01x |
| build | 0.092 | 0.196 | 0.05 | 126 | 1.00x |
| *build-aa-adjacent* | *0.094* | *0.210* | *0.04* | *127* | *1.00x* |
| mut-flat-gm | 0.098 | 0.142 | 0.05 | 134 | 1.34x |
| *mut-odo-aa-adjacent* | *0.098* | *0.209* | *0.05* | *124* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.101* | *0.105* | *0.03* | *130* | *1.34x* |
| bq-expand-gm-mulback | 0.101 | 0.165 | 0.03 | 132 | 2.52x |
| **bq-scan-rem-gm-mulback** | **0.101** | 0.105 | 0.02 | 130 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.101* | *0.105* | *0.03* | *130* | *1.34x* |
| *bq-odo-gm-mulback-aa-distant* | *0.102* | *0.115* | *0.05* | *132* | *1.41x* |
| bq-odo-gm-mulback | 0.102 | 0.115 | 0.03 | 132 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.102* | *0.116* | *0.02* | *132* | *1.41x* |
| mut-odo | 0.103 | 0.201 | 0.05 | 124 | 1.00x |
| *mut-odo-aa-distant* | *0.103* | *0.202* | *0.05* | *125* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.104 | 0.143 | 0.03 | 133 | 1.34x |
| bq-expand-b | 0.106 | 0.172 | 0.05 | 131 | 2.52x |
| bq-expand-qr-prim | 0.106 | 0.169 | 0.03 | 131 | 2.52x |
| *bq-expand-aa-adjacent* | *0.106* | *0.171* | *0.04* | *131* | *2.52x* |
| **bq-expand** | **0.106** | 0.171 | 0.02 | 131 | 2.52x |
| *bq-expand-aa-distant* | *0.106* | *0.172* | *0.02* | *131* | *2.52x* |
| bq-expand-zf | 0.108 | 0.182 | 0.04 | 130 | 2.52x |
| *build-aa-distant* | *0.108* | *0.213* | *0.09* | *124* | *1.00x* |
| bq-mut-runs | 0.113 | 0.169 | 0.05 | 132 | 1.34x |
| *offtab-aa-adjacent* | *0.118* | *0.213* | *0.55* | *124* | *2.00x* |
| offtab | 0.120 | 0.215 | 0.02 | 124 | 2.00x |
| *offtab-aa-distant* | *0.120* | *0.214* | *0.05* | *124* | *2.00x* |
| offtab-scan-rem | 0.138 | 0.141 | 0.05 | 125 | 2.00x |
| bq-mut | 0.166 | 0.226 | 0.13 | 120 | 1.34x |
| bq-gen | 0.521 | 0.640 | 1.20 | 100 | 1.34x |
| *list-aa-distant* | *0.998* | *1.000* | *0.07* | *89* | *23.45x* |
| list (baseline) | 1.000 | 1.000 | 0.03 | 89 | 23.45x |
| *list-aa-adjacent* | *1.001* | *1.001* | *0.04* | *89* | *23.45x* |
| *gen-unsafe-aa-distant* | *1.410* | *1.631* | *0.61* | *82* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.412* | *1.639* | *0.23* | *81* | *1.00x* |
| gen-quotrem | 1.424 | 1.660 | 0.45 | 81 | 1.00x |
| gen-unsafe | 1.433 | 1.729 | 0.32 | 82 | 1.00x |

Controls: The largest A/A pair is `build-aa-distant` at 1.0883, worst cell
18.40% on `rev-gather48-src-50`, and 11 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0001 on a worst cell of 0.08% on `rev-gather48-src-50`,
its interval covering 1. The in-situ term reads 0.9779, 1.0013, 0.9859
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0720, which the correction amplifies by 1.44x -- quote both
wherever that is past 1.5.

Provenance: elapsed 0h12m6s, peak 63 MiB in use, 21 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 3.64 ms per call raw, 3.49 ms net.

Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes): `mut-odo-vecdims` 0.073/0.057/0.029 `bq-scan-rem-gm-mulback`
0.103/0.105/0.095 `bq-expand` 0.171/0.099/0.102

What the class says: the shipped row is safe at `worst` 0.171, the highest
of the eight, and the pure slot is a tie the sort had to settle —
`bq-expand-gm-mulback` and `bq-scan-rem-gm-mulback` both print 0.101,
with `bq-odo-gm-mulback` a thousandth behind. Five runs have now split this slot
three and two — `bq-expand-gm-mulback` on Runs 11, 12 and 14,
`bq-scan-rem-gm-mulback` on Runs 10 and 13 — which is the reading: the cluster
is the fact and the winner is not.

**`revsome` — a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *91* | *2.52x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.04* | *93* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.06* | *115* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *117* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.053* | *0.063* | *0.05* | *98* | *1.00x* |
| **mut-odo-vecdims** | **0.053** | 0.063 | 0.05 | 98 | 1.00x |
| mut-odo-vecdims-add-in | 0.054 | 0.063 | 0.05 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.054* | *0.063* | *0.04* | *98* | *1.00x* |
| mut-odo-vecdims-add-both | 0.055 | 0.069 | 0.07 | 98 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.056 | 0.067 | 0.05 | 98 | 1.00x |
| mut-odo-vecdims-add-out | 0.060 | 0.072 | 0.04 | 98 | 1.00x |
| *mut-odo-aa-distant* | *0.090* | *0.180* | *0.03* | *97* | *1.00x* |
| mut-flat-gm | 0.092 | 0.110 | 0.05 | 87 | 1.33x |
| build | 0.092 | 0.189 | 0.93 | 97 | 1.00x |
| *mut-odo-aa-adjacent* | *0.099* | *0.164* | *0.04* | *97* | *1.00x* |
| *build-aa-adjacent* | *0.099* | *0.189* | *1.15* | *97* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.100 | 0.115 | 0.21 | 87 | 1.33x |
| bq-mut-runs | 0.103 | 0.119 | 0.04 | 86 | 1.33x |
| **bq-scan-rem-gm-mulback** | **0.105** | 0.107 | 0.03 | 88 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.105* | *0.107* | *0.04* | *88* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.105* | *0.107* | *0.05* | *88* | *1.33x* |
| bq-expand-b | 0.106 | 0.133 | 0.04 | 84 | 2.52x |
| **bq-expand** | **0.106** | 0.133 | 0.06 | 84 | 2.52x |
| bq-expand-qr-prim | 0.107 | 0.132 | 0.05 | 84 | 2.52x |
| bq-expand-gm-mulback | 0.107 | 0.124 | 0.06 | 85 | 2.52x |
| *bq-expand-aa-adjacent* | *0.107* | *0.133* | *0.05* | *84* | *2.52x* |
| *bq-odo-gm-mulback-aa-distant* | *0.107* | *0.118* | *0.04* | *86* | *1.41x* |
| *bq-expand-aa-distant* | *0.107* | *0.133* | *0.02* | *84* | *2.52x* |
| bq-odo-gm-mulback | 0.107 | 0.118 | 0.07 | 86 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.107* | *0.118* | *0.10* | *86* | *1.41x* |
| bq-expand-zf | 0.110 | 0.139 | 0.04 | 84 | 2.52x |
| *build-aa-distant* | *0.114* | *0.152* | *1.54* | *97* | *1.00x* |
| *offtab-aa-adjacent* | *0.116* | *0.198* | *0.07* | *92* | *2.00x* |
| mut-odo | 0.121 | 0.165 | 0.20 | 97 | 1.00x |
| offtab | 0.123 | 0.168 | 0.08 | 92 | 2.00x |
| *offtab-aa-distant* | *0.123* | *0.195* | *0.31* | *92* | *2.00x* |
| offtab-scan-rem | 0.139 | 0.142 | 0.05 | 84 | 2.00x |
| bq-mut | 0.170 | 0.195 | 0.04 | 84 | 1.33x |
| bq-gen | 0.541 | 0.622 | 0.17 | 83 | 1.33x |
| list (baseline) | 1.000 | 1.000 | 0.15 | 49 | 23.45x |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.07* | *49* | *23.45x* |
| *list-aa-distant* | *1.001* | *1.001* | *0.15* | *49* | *23.45x* |
| *gen-unsafe-aa-adjacent* | *1.341* | *1.568* | *0.83* | *44* | *1.00x* |
| gen-unsafe | 1.363 | 1.582 | 0.94 | 44 | 1.00x |
| *gen-unsafe-aa-distant* | *1.375* | *1.583* | *0.38* | *45* | *1.00x* |
| gen-quotrem | 1.393 | 1.620 | 0.26 | 44 | 1.00x |

Controls: The largest A/A pair is `offtab-aa-distant` at 1.0782, worst cell
15.79% on `revsome-mid-cnn-L2`, and 12 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0001 on a worst cell of 0.05% on `revsome-mid-cnn-L2`,
its interval covering 1. The in-situ term reads 0.9906, 0.9912, 0.9851
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0648, which the correction amplifies by 1.36x -- quote both
wherever that is past 1.5.

Provenance: elapsed 0h12m6s, peak 61 MiB in use, 22 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 3.63 ms per call raw, 3.48 ms net.

Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2): `mut-odo-vecdims` 0.031/0.058/0.063
`bq-scan-rem-gm-mulback` 0.104/0.107/0.105 `bq-expand` 0.102/0.099/0.133

What the class says: nothing the main set does not. All three clauses hold —
`mut-odo-vecdims` at the top, `bq-scan-rem-gm-mulback` the fastest pure at 0.105
with `bq-expand-b` a thousandth behind it, and the shipped arm behind both
at 0.106 — and that is a result rather than an absence of one.

**`bcast` — an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.30* | *53* | *1.38x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.26* | *56* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *84* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.026 | 0.071 | 0.25 | 63 | 1.00x |
| mut-odo-vecdims-add-in | 0.028 | 0.066 | 0.24 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.067* | *0.02* | *62* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.067* | *0.03* | *62* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.067 | 0.24 | 62 | 1.00x |
| mut-odo-vecdims-add-both | 0.029 | 0.072 | 0.23 | 62 | 1.00x |
| mut-odo-vecdims-add-out | 0.029 | 0.072 | 0.24 | 62 | 1.00x |
| *build-aa-adjacent* | *0.046* | *0.168* | *2.80* | *62* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.048* | *0.160* | *0.03* | *62* | *1.00x* |
| build | 0.049 | 0.181 | 0.57 | 62 | 1.00x |
| mut-odo | 0.050 | 0.181 | 0.25 | 62 | 1.00x |
| *build-aa-distant* | *0.050* | *0.175* | *1.25* | *62* | *1.00x* |
| *mut-odo-aa-distant* | *0.051* | *0.180* | *0.09* | *62* | *1.00x* |
| mut-flat-gm | 0.063 | 0.081 | 0.33 | 48 | 1.13x |
| bq-mut-runs-gm-mulback | 0.067 | 0.085 | 0.57 | 48 | 1.13x |
| *offtab-aa-adjacent* | *0.068* | *0.167* | *0.95* | *55* | *2.00x* |
| bq-expand-gm-mulback | 0.071 | 0.087 | 0.34 | 48 | 1.38x |
| offtab | 0.071 | 0.183 | 0.59 | 55 | 2.00x |
| *offtab-aa-distant* | *0.073* | *0.195* | *0.49* | *55* | *2.00x* |
| bq-mut-runs | 0.073 | 0.095 | 0.32 | 47 | 1.13x |
| bq-expand-b | 0.073 | 0.097 | 0.34 | 47 | 1.38x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.076* | *0.090* | *0.35* | *48* | *1.14x* |
| bq-odo-gm-mulback | 0.076 | 0.090 | 0.34 | 48 | 1.14x |
| *bq-odo-gm-mulback-aa-distant* | *0.077* | *0.091* | *0.34* | *48* | *1.14x* |
| *bq-expand-aa-adjacent* | *0.077* | *0.097* | *0.34* | *47* | *1.38x* |
| bq-expand-qr-prim | 0.078 | 0.097 | 0.37 | 47 | 1.38x |
| **bq-expand** | **0.078** | 0.097 | 0.33 | 47 | 1.38x |
| bq-expand-zf | 0.078 | 0.098 | 0.32 | 47 | 1.38x |
| *bq-expand-aa-distant* | *0.079* | *0.097* | *0.02* | *47* | *1.38x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.084* | *0.106* | *0.04* | *48* | *1.13x* |
| **bq-scan-rem-gm-mulback** | **0.084** | 0.105 | 0.35 | 48 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.084* | *0.105* | *0.34* | *48* | *1.13x* |
| bq-mut | 0.104 | 0.173 | 0.32 | 47 | 1.13x |
| offtab-scan-rem | 0.117 | 0.135 | 0.73 | 44 | 2.00x |
| bq-gen | 0.178 | 0.286 | 0.33 | 47 | 1.13x |
| gen-unsafe | 0.414 | 1.114 | 1.25 | 25 | 1.00x |
| *gen-unsafe-aa-distant* | *0.447* | *1.192* | *1.13* | *25* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.458* | *1.174* | *2.30* | *25* | *1.00x* |
| gen-quotrem | 0.481 | 1.109 | 0.35 | 25 | 1.00x |
| *list-aa-distant* | *1.000* | *1.000* | *1.16* | *16* | *20.64x* |
| list (baseline) | 1.000 | 1.000 | 1.06 | 16 | 20.64x |
| *list-aa-adjacent* | *1.002* | *1.007* | *0.62* | *16* | *20.64x* |

Controls: The largest A/A pair is `build-aa-adjacent` at 0.9275, worst cell
14.82% on `bcast-inner8`, and 11 of 18 intervals cover 1. The `sum-only` halves
agree at 0.9998 on a worst cell of 0.05% on `bcast-tall-Mx2`, its interval
missing 1. The in-situ term reads 0.9869, 1.0035, 0.9871 of `sum-only`
as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 0.9483, which the correction amplifies by 1.69x -- quote both wherever
that is past 1.5.

Provenance: elapsed 0h12m12s, peak 95 MiB in use, 40 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 52 ms per call raw, 50.9 ms net.

Per shape, in the lead's order (bcast-inner8, bcast-inner900, bcast-tall-Mx2):
`mut-odo-vecdims` 0.035/0.010/0.067 `bq-scan-rem-gm-mulback` 0.095/0.044/0.105
`bq-expand` 0.097/0.049/0.088

What the class says: `bq-expand-gm-mulback` keeps the pure slot at 0.071 against
`bq-expand-b`'s 0.073, so this is still the class where a mul-back output pays
most. The shipped arm reads its best of the eight here, 0.078, on the only
`worst` under a tenth.

**`bcastmid` — the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *88* | *2.11x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.06* | *93* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *103* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *109* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *109* | *0.00x* |
| mut-odo-vecdims-add-in | 0.036 | 0.063 | 0.04 | 95 | 1.00x |
| **mut-odo-vecdims** | **0.036** | 0.063 | 0.04 | 95 | 1.00x |
| *mut-odo-vecdims-aa* | *0.036* | *0.063* | *0.04* | *95* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.036* | *0.063* | *0.03* | *95* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.036 | 0.067 | 0.06 | 94 | 1.00x |
| mut-odo-vecdims-add-both | 0.038 | 0.069 | 0.14 | 94 | 1.00x |
| mut-odo-vecdims-add-out | 0.039 | 0.072 | 0.08 | 93 | 1.00x |
| build | 0.067 | 0.167 | 1.49 | 80 | 1.00x |
| *build-aa-adjacent* | *0.068* | *0.165* | *1.87* | *80* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.069* | *0.155* | *0.04* | *81* | *1.00x* |
| mut-odo | 0.070 | 0.164 | 0.07 | 81 | 1.00x |
| *mut-odo-aa-distant* | *0.071* | *0.170* | *1.02* | *80* | *1.00x* |
| *build-aa-distant* | *0.072* | *0.174* | *0.94* | *79* | *1.00x* |
| mut-flat-gm | 0.078 | 0.107 | 0.05 | 86 | 1.33x |
| bq-mut-runs-gm-mulback | 0.080 | 0.112 | 0.15 | 86 | 1.33x |
| *bq-odo-gm-mulback-aa-distant* | *0.085* | *0.116* | *0.04* | *85* | *1.33x* |
| bq-odo-gm-mulback | 0.085 | 0.117 | 0.04 | 85 | 1.33x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.085* | *0.118* | *0.17* | *85* | *1.33x* |
| bq-expand-gm-mulback | 0.086 | 0.124 | 0.05 | 85 | 2.11x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.086* | *0.105* | *0.05* | *86* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.086** | 0.105 | 0.05 | 86 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.087* | *0.105* | *0.03* | *86* | *1.33x* |
| *offtab-aa-adjacent* | *0.089* | *0.169* | *0.09* | *80* | *2.00x* |
| bq-mut-runs | 0.090 | 0.123 | 0.32 | 84 | 1.33x |
| *offtab-aa-distant* | *0.091* | *0.162* | *0.55* | *81* | *2.00x* |
| offtab | 0.092 | 0.194 | 0.19 | 78 | 2.00x |
| bq-expand-qr-prim | 0.094 | 0.132 | 0.06 | 84 | 2.11x |
| *bq-expand-aa-distant* | *0.094* | *0.133* | *0.08* | *84* | *2.11x* |
| **bq-expand** | **0.094** | 0.132 | 0.05 | 84 | 2.11x |
| *bq-expand-aa-adjacent* | *0.094* | *0.132* | *0.05* | *84* | *2.11x* |
| bq-expand-b | 0.094 | 0.133 | 0.10 | 84 | 2.11x |
| bq-expand-zf | 0.096 | 0.138 | 0.07 | 83 | 2.11x |
| bq-mut | 0.104 | 0.185 | 0.05 | 79 | 1.33x |
| offtab-scan-rem | 0.124 | 0.135 | 0.09 | 80 | 2.00x |
| bq-gen | 0.274 | 0.689 | 1.35 | 56 | 1.33x |
| gen-unsafe | 0.848 | 1.417 | 0.63 | 43 | 1.00x |
| gen-quotrem | 0.851 | 1.494 | 0.47 | 42 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.854* | *1.483* | *0.91* | *42* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.860* | *1.495* | *0.49* | *42* | *1.00x* |
| *list-aa-distant* | *0.996* | *1.006* | *0.28* | *46* | *23.33x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 46 | 23.33x |
| *list-aa-adjacent* | *1.002* | *1.004* | *0.31* | *46* | *23.33x* |

Controls: The largest A/A pair is `build-aa-distant` at 1.0791, worst cell
20.95% on `bcastmid-b200k`, and 15 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9982 on a worst cell of 0.53% on `bcastmid-primes`,
its interval covering 1. The in-situ term reads 0.9803, 0.9779, 0.9949
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0629, which the correction amplifies by 1.52x -- quote both
wherever that is past 1.5.

Provenance: elapsed 0h12m9s, peak 95 MiB in use, 33 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 46.9 ms per call raw, 45.9 ms net.

Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k): `mut-odo-vecdims` 0.063/0.021/0.035 `bq-scan-rem-gm-mulback`
0.105/0.090/0.067 `bq-expand` 0.132/0.101/0.063

What the class says: the pure slot changes hands to `bq-odo-gm-mulback`
at 0.085, one thousandth ahead of `bq-expand-gm-mulback`
and `bq-scan-rem-gm-mulback` alike. A margin that size is
under this population's floor of 7.91%, so read it as a three-way tie the sort
settled and not as an arm winning something.

**`reshape1` — the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *89* | *5.43x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.06* | *100* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| mut-flat-gm | 0.034 | 0.108 | 0.06 | 97 | 2.00x |
| bq-mut-runs-gm-mulback | 0.036 | 0.120 | 0.13 | 96 | 2.00x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.054* | *0.099* | *0.05* | *95* | *2.31x* |
| bq-odo-gm-mulback | 0.055 | 0.099 | 0.07 | 95 | 2.31x |
| *bq-odo-gm-mulback-aa-distant* | *0.055* | *0.099* | *0.03* | *95* | *2.31x* |
| bq-expand-gm-mulback | 0.058 | 0.129 | 0.11 | 93 | 5.43x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.077* | *0.078* | *0.07* | *87* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.077** | 0.078 | 0.05 | 87 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.077* | *0.078* | *0.01* | *87* | *2.00x* |
| offtab-scan-rem | 0.078 | 0.078 | 0.04 | 87 | 2.00x |
| bq-mut-runs | 0.081 | 0.152 | 0.12 | 87 | 2.00x |
| mut-odo-vecdims-add-in | 0.097 | 0.100 | 0.03 | 83 | 1.00x |
| *mut-odo-vecdims-aa* | *0.098* | *0.100* | *0.03* | *83* | *1.00x* |
| **mut-odo-vecdims** | **0.098** | 0.100 | 0.04 | 83 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.098* | *0.100* | *0.01* | *83* | *1.00x* |
| bq-expand-b | 0.102 | 0.159 | 0.08 | 84 | 5.43x |
| bq-expand-qr-prim | 0.104 | 0.158 | 0.10 | 84 | 5.43x |
| *bq-expand-aa-adjacent* | *0.104* | *0.159* | *0.11* | *84* | *5.43x* |
| **bq-expand** | **0.104** | 0.159 | 0.09 | 84 | 5.43x |
| *bq-expand-aa-distant* | *0.105* | *0.159* | *0.07* | *84* | *5.43x* |
| mut-odo-vecdims-add-both-down | 0.106 | 0.108 | 0.04 | 82 | 1.00x |
| mut-odo-vecdims-add-both | 0.107 | 0.109 | 0.05 | 82 | 1.00x |
| bq-expand-zf | 0.108 | 0.170 | 0.08 | 84 | 5.43x |
| mut-odo-vecdims-add-out | 0.108 | 0.109 | 0.05 | 82 | 1.00x |
| bq-mut | 0.260 | 0.297 | 0.63 | 66 | 2.00x |
| offtab | 0.278 | 0.309 | 2.17 | 68 | 2.00x |
| *offtab-aa-distant* | *0.279* | *0.307* | *0.04* | *64* | *2.00x* |
| build | 0.282 | 0.316 | 1.10 | 65 | 1.00x |
| mut-odo | 0.284 | 0.314 | 0.09 | 65 | 1.00x |
| *mut-odo-aa-adjacent* | *0.284* | *0.311* | *0.08* | *65* | *1.00x* |
| *mut-odo-aa-distant* | *0.284* | *0.295* | *0.08* | *65* | *1.00x* |
| *offtab-aa-adjacent* | *0.286* | *0.309* | *0.49* | *67* | *2.00x* |
| *build-aa-distant* | *0.296* | *0.307* | *0.26* | *66* | *1.00x* |
| *build-aa-adjacent* | *0.302* | *0.320* | *0.48* | *64* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.888* | *1.915* | *0.80* | *45* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.905* | *2.038* | *1.50* | *43* | *1.00x* |
| gen-quotrem | 0.905 | 1.964 | 1.26 | 44 | 1.00x |
| gen-unsafe | 0.919 | 1.940 | 0.27 | 44 | 1.00x |
| *list-aa-distant* | *0.994* | *1.000* | *0.32* | *44* | *32.37x* |
| list (baseline) | 1.000 | 1.000 | 0.37 | 43 | 32.37x |
| *list-aa-adjacent* | *1.002* | *1.005* | *0.19* | *44* | *32.37x* |
| bq-gen | 1.005 | 2.532 | 0.23 | 42 | 2.00x |

Controls: The largest A/A pair is `build-aa-adjacent` at 1.0719, worst cell
18.59% on `reshape1-500k`, and 16 of 18 intervals cover 1. The `sum-only` halves
agree at 0.9981 on a worst cell of 0.55% on `reshape1-500k`, its interval
covering 1. The in-situ term reads 0.9800, 0.9824, 0.9868 of `sum-only`
as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 1.0655, which the correction amplifies by 1.08x -- quote both wherever
that is past 1.5.

Provenance: elapsed 0h12m6s, peak 58 MiB in use, 20 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 11.8 ms per call raw, 11.5 ms net.

Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10):
`mut-odo-vecdims` 0.098/0.100/0.095 `bq-scan-rem-gm-mulback` 0.076/0.078/0.077
`bq-expand` 0.076/0.094/0.159

What the class says: this is the one population where the first clause breaks,
and it breaks as it has since -O1 — the flat fills own the top outright,
`mut-flat-gm` at 0.034 and `bq-mut-runs-gm-mulback` at 0.036,
with no `mut-odo-vecdims` arm near them. `bq-odo-gm-mulback` takes the pure slot
at 0.055 against `bq-expand-gm-mulback`'s 0.058 — wider than the thousandth
that settles `bcastmid`, but still 5.5% against this population's 7.19% floor,
so read it as a sort rather than as a win. And `m = l` here, so `bq-expand`
allocates 5.43x its result, the highest of the eight — the class's own `m`
showing through exactly as the third property warns it will.

**`slice` — a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *91* | *1.58x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.10* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *116* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *117* | *0.00x* |
| mut-odo-vecdims-add-in | 0.039 | 0.063 | 0.05 | 98 | 1.00x |
| **mut-odo-vecdims** | **0.040** | 0.063 | 0.03 | 98 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.063* | *0.02* | *98* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.040* | *0.063* | *0.06* | *98* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.041 | 0.067 | 0.04 | 98 | 1.00x |
| mut-odo-vecdims-add-both | 0.042 | 0.069 | 0.03 | 98 | 1.00x |
| mut-odo-vecdims-add-out | 0.043 | 0.072 | 0.04 | 98 | 1.00x |
| build | 0.070 | 0.166 | 0.86 | 97 | 1.00x |
| *mut-odo-aa-adjacent* | *0.070* | *0.155* | *0.03* | *97* | *1.00x* |
| mut-odo | 0.072 | 0.180 | 0.04 | 97 | 1.00x |
| *build-aa-distant* | *0.073* | *0.188* | *0.36* | *97* | *1.00x* |
| *build-aa-adjacent* | *0.073* | *0.186* | *0.77* | *97* | *1.00x* |
| *mut-odo-aa-distant* | *0.074* | *0.179* | *0.08* | *97* | *1.00x* |
| mut-flat-gm | 0.091 | 0.108 | 0.07 | 87 | 1.08x |
| offtab | 0.092 | 0.182 | 0.07 | 92 | 2.00x |
| *offtab-aa-adjacent* | *0.093* | *0.196* | *0.07* | *92* | *2.00x* |
| *offtab-aa-distant* | *0.096* | *0.200* | *0.28* | *92* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.105* | *0.02* | *88* | *1.08x* |
| **bq-scan-rem-gm-mulback** | **0.102** | 0.105 | 0.05 | 88 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.102* | *0.105* | *0.05* | *88* | *1.08x* |
| bq-mut-runs-gm-mulback | 0.102 | 0.111 | 0.05 | 87 | 1.08x |
| bq-mut-runs | 0.108 | 0.119 | 0.04 | 86 | 1.08x |
| bq-expand-gm-mulback | 0.108 | 0.125 | 0.06 | 85 | 1.58x |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.119* | *0.02* | *86* | *1.50x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.110* | *0.119* | *0.05* | *86* | *1.50x* |
| bq-odo-gm-mulback | 0.111 | 0.119 | 0.04 | 86 | 1.50x |
| bq-expand-qr-prim | 0.114 | 0.132 | 0.04 | 84 | 1.58x |
| bq-expand-b | 0.114 | 0.133 | 0.04 | 84 | 1.58x |
| *bq-expand-aa-distant* | *0.115* | *0.133* | *0.02* | *84* | *1.58x* |
| **bq-expand** | **0.115** | 0.133 | 0.05 | 84 | 1.58x |
| *bq-expand-aa-adjacent* | *0.115* | *0.134* | *0.05* | *84* | *1.58x* |
| bq-expand-zf | 0.118 | 0.140 | 0.06 | 84 | 1.58x |
| offtab-scan-rem | 0.136 | 0.143 | 0.05 | 83 | 2.00x |
| bq-mut | 0.136 | 0.194 | 0.34 | 84 | 1.08x |
| bq-gen | 0.288 | 0.637 | 0.10 | 83 | 1.08x |
| *list-aa-distant* | *0.999* | *1.001* | *0.20* | *49* | *20.55x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 49 | 20.55x |
| *list-aa-adjacent* | *1.000* | *1.004* | *0.09* | *49* | *20.55x* |
| *gen-unsafe-aa-adjacent* | *1.547* | *2.586* | *0.50* | *45* | *1.00x* |
| gen-unsafe | 1.568 | 2.553 | 0.55 | 45 | 1.00x |
| *gen-unsafe-aa-distant* | *1.580* | *2.429* | *0.85* | *44* | *1.00x* |
| gen-quotrem | 1.606 | 2.509 | 0.68 | 45 | 1.00x |

Controls: The largest A/A pair is `build-aa-adjacent` at 1.0470, worst cell
11.86% on `slice-cnn-L2-24x24-c32`, and 16 of 18 intervals cover 1.
The `sum-only` halves agree at 0.9989 on a worst cell of 0.59%
on `slice-coprime-r7`, its interval covering 1. The in-situ term reads 0.9837,
1.0030, 0.9926 of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0374, which the correction amplifies
by 1.58x -- quote both wherever that is past 1.5.

Provenance: elapsed 0h12m6s, peak 94 MiB in use, 37 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 3.64 ms per call raw, 3.48 ms net.

Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7): `mut-odo-vecdims` 0.063/0.030/0.034 `bq-scan-rem-gm-mulback`
0.105/0.104/0.090 `bq-expand` 0.133/0.103/0.110

What the class says: nothing new. All three clauses hold,
`bq-scan-rem-gm-mulback` keeping the pure slot at 0.102, and this population has
the tightest floor of the eight but one.

**`window` — overlapping im2col patches: the workload this page opens by naming,
with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5`
(`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.02* | *120* | *2.81x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.11* | *137* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *121* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *151* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *151* | *0.00x* |
| mut-odo-vecdims-add-in | 0.066 | 0.102 | 0.05 | 117 | 1.00x |
| **mut-odo-vecdims** | **0.067** | 0.102 | 0.03 | 117 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.067* | *0.102* | *0.03* | *117* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.068* | *0.102* | *0.03* | *117* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.071 | 0.111 | 0.04 | 116 | 1.01x |
| mut-odo-vecdims-add-both | 0.073 | 0.112 | 0.03 | 115 | 1.01x |
| mut-odo-vecdims-add-out | 0.075 | 0.113 | 0.08 | 115 | 1.01x |
| mut-flat-gm | 0.077 | 0.107 | 0.09 | 128 | 1.33x |
| bq-mut-runs-gm-mulback | 0.086 | 0.106 | 0.02 | 129 | 1.33x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.091* | *0.116* | *0.04* | *125* | *2.56x* |
| bq-odo-gm-mulback | 0.091 | 0.115 | 0.04 | 125 | 2.56x |
| *bq-odo-gm-mulback-aa-distant* | *0.091* | *0.116* | *0.05* | *125* | *2.56x* |
| bq-expand-gm-mulback | 0.095 | 0.122 | 0.03 | 124 | 2.81x |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.104 | 0.01 | 121 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.104* | *0.03* | *121* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.104* | *0.03* | *121* | *1.33x* |
| bq-mut-runs | 0.106 | 0.117 | 0.04 | 118 | 1.33x |
| bq-expand-qr-prim | 0.118 | 0.130 | 0.05 | 116 | 2.81x |
| *bq-expand-aa-adjacent* | *0.118* | *0.130* | *0.03* | *116* | *2.81x* |
| **bq-expand** | **0.118** | 0.130 | 0.02 | 116 | 2.81x |
| *bq-expand-aa-distant* | *0.118* | *0.130* | *0.03* | *116* | *2.81x* |
| bq-expand-b | 0.118 | 0.130 | 0.05 | 116 | 2.81x |
| bq-expand-zf | 0.120 | 0.136 | 0.05 | 115 | 2.81x |
| offtab-scan-rem | 0.132 | 0.132 | 0.06 | 121 | 2.00x |
| *build-aa-adjacent* | *0.168* | *0.269* | *1.73* | *99* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.176* | *0.305* | *0.67* | *98* | *1.00x* |
| *offtab-aa-adjacent* | *0.177* | *0.310* | *1.21* | *98* | *2.00x* |
| offtab | 0.177 | 0.285 | 0.13 | 99 | 2.00x |
| build | 0.182 | 0.299 | 1.12 | 98 | 1.00x |
| *build-aa-distant* | *0.182* | *0.301* | *1.86* | *98* | *1.00x* |
| mut-odo | 0.183 | 0.275 | 0.14 | 100 | 1.00x |
| *offtab-aa-distant* | *0.186* | *0.294* | *0.36* | *98* | *2.00x* |
| *mut-odo-aa-distant* | *0.187* | *0.311* | *0.26* | *97* | *1.00x* |
| bq-mut | 0.192 | 0.334 | 1.24 | 96 | 1.33x |
| bq-gen | 0.631 | 1.159 | 0.34 | 72 | 1.33x |
| *list-aa-distant* | *1.000* | *1.000* | *0.12* | *75* | *24.78x* |
| *list-aa-adjacent* | *1.000* | *1.000* | *0.05* | *75* | *24.78x* |
| list (baseline) | 1.000 | 1.000 | 0.08 | 75 | 24.78x |
| gen-unsafe | 1.067 | 1.583 | 0.68 | 75 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.069* | *1.622* | *1.59* | *75* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.116* | *1.638* | *0.34* | *74* | *1.00x* |
| gen-quotrem | 1.152 | 1.634 | 0.07 | 75 | 1.00x |

Controls: The largest A/A pair is `gen-unsafe-aa-distant` at 1.0848, worst cell
18.12% on `window-224x224-k3`, and 10 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9998 on a worst cell of 0.06% on `window-28x28-k5`,
its interval covering 1. The in-situ term reads 0.9776, 0.9894, 0.9851
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0822, which the correction amplifies by 1.03x -- quote both
wherever that is past 1.5.

Provenance: elapsed 0h12m7s, peak 57 MiB in use, 19 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 8.37 ms per call raw, 8.11 ms net.

Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9): `mut-odo-vecdims` 0.048/0.061/0.102 `bq-scan-rem-gm-mulback`
0.102/0.104/0.078 `bq-expand` 0.115/0.130/0.110

What the class says: `bq-odo-gm-mulback` takes the pure slot at 0.091 against
`bq-scan-rem-gm-mulback`'s 0.100, a break by a margin rather than by a sort —
the second widest of the eight, `reshape1`'s being twice it. The shipped arm's
0.118 is its worst reading of the eight.

**`scaled` — superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 — rank 1, so `m` is 1 and the whole view is one
strided run).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.04* | *120* | *1.14x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.05* | *124* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.06* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *138* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.029 | 0.034 | 0.02 | 128 | 1.00x |
| mut-odo-vecdims-add-in | 0.030 | 0.034 | 0.04 | 128 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.030* | *0.034* | *0.04* | *128* | *1.00x* |
| **mut-odo-vecdims** | **0.030** | 0.034 | 0.06 | 128 | 1.00x |
| mut-odo-vecdims-add-out | 0.031 | 0.037 | 0.02 | 128 | 1.00x |
| *mut-odo-vecdims-aa* | *0.031* | *0.034* | *0.05* | *127* | *1.00x* |
| mut-odo-vecdims-add-both | 0.031 | 0.036 | 0.10 | 127 | 1.00x |
| *mut-odo-aa-distant* | *0.033* | *0.055* | *0.06* | *126* | *1.00x* |
| *build-aa-adjacent* | *0.035* | *0.054* | *0.49* | *126* | *1.00x* |
| mut-odo | 0.036 | 0.055 | 0.05 | 126 | 1.00x |
| *build-aa-distant* | *0.037* | *0.052* | *0.05* | *126* | *1.00x* |
| build | 0.037 | 0.054 | 0.09 | 126 | 1.00x |
| *mut-odo-aa-adjacent* | *0.038* | *0.055* | *0.25* | *126* | *1.00x* |
| *offtab-aa-adjacent* | *0.060* | *0.080* | *0.11* | *120* | *2.00x* |
| offtab | 0.060 | 0.080 | 0.09 | 120 | 2.00x |
| *offtab-aa-distant* | *0.062* | *0.077* | *0.05* | *121* | *2.00x* |
| mut-flat-gm | 0.083 | 0.083 | 0.06 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.091 | 0.093 | 0.07 | 115 | 1.03x |
| bq-expand-gm-mulback | 0.093 | 0.095 | 0.06 | 114 | 1.14x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.094* | *0.096* | *0.02* | *114* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.094** | 0.097 | 0.05 | 114 | 1.04x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.097* | *0.03* | *114* | *1.04x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.098* | *0.099* | *0.04* | *114* | *1.04x* |
| bq-odo-gm-mulback | 0.098 | 0.099 | 0.02 | 114 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.098* | *0.099* | *0.03* | *114* | *1.04x* |
| bq-mut-runs | 0.102 | 0.103 | 0.04 | 113 | 1.03x |
| bq-expand-qr-prim | 0.104 | 0.105 | 0.02 | 113 | 1.14x |
| **bq-expand** | **0.104** | 0.104 | 0.04 | 113 | 1.14x |
| *bq-expand-aa-adjacent* | *0.104* | *0.104* | *0.02* | *113* | *1.14x* |
| bq-expand-b | 0.104 | 0.105 | 0.03 | 113 | 1.14x |
| *bq-expand-aa-distant* | *0.104* | *0.105* | *0.02* | *113* | *1.14x* |
| bq-expand-zf | 0.105 | 0.105 | 0.06 | 113 | 1.14x |
| bq-mut | 0.113 | 0.126 | 0.03 | 112 | 1.03x |
| offtab-scan-rem | 0.136 | 0.138 | 0.07 | 109 | 2.00x |
| bq-gen | 0.157 | 0.267 | 0.18 | 108 | 1.03x |
| list (baseline) | 1.000 | 1.000 | 0.11 | 73 | 19.44x |
| *list-aa-distant* | *1.001* | *1.001* | *0.14* | *73* | *19.44x* |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.08* | *73* | *19.44x* |
| *gen-unsafe-aa-adjacent* | *1.003* | *2.241* | *0.07* | *69* | *1.00x* |
| gen-unsafe | 1.008 | 2.183 | 0.08 | 68 | 1.00x |
| *gen-unsafe-aa-distant* | *1.015* | *2.115* | *0.27* | *68* | *1.00x* |
| gen-quotrem | 1.037 | 2.185 | 0.06 | 68 | 1.00x |

Controls: The largest A/A pair is `mut-odo-aa-adjacent` at 1.0194, worst cell
5.24% on `scaled-super-r3`, and 15 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0001 on a worst cell of 0.02% on `scaled-rank1-m1`,
its interval covering 1. The in-situ term reads 0.9975, 0.9839, 0.9858
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0083, which the correction amplifies by 2.12x -- quote both
wherever that is past 1.5.

Provenance: elapsed 0h12m7s, peak 88 MiB in use, 34 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.28 ms per call raw, 4.1 ms net.

Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1, scaled-r5):
`mut-odo-vecdims` 0.028/0.030/0.034 `bq-scan-rem-gm-mulback` 0.093/0.094/0.097
`bq-expand` 0.102/0.104/0.104

What the class says: the slot this class has carried in six runs of seven
is this run's registered second question, and the answer is at the head
of the chapter — the 1 GB half does not carry it. On the basis half it is still
here, and this population's floor is 1.94% — the tightest of the eight classes,
though not comparable with the figures earlier runs published for it,
those being over six A/A pairs where this is over eighteen. The pure slot
separates for the first time, `bq-expand-gm-mulback` 0.093 against
`bq-scan-rem-gm-mulback` 0.094, where Run 13 printed the two at one figure.


### Provenance

The run's name, regime, scale and source commit are at the head of this chapter;
what follows is what they have to be read against. The commit is recorded there
because a run whose artifact is deleted and whose source is unrecorded cannot
be repeated even in principle.

**Run 14's halves differ in less than any pair here has, and this time
the difference is not code at all.** They share shapes, class lists, roster
membership and order, machine, GHC, `cabal.project.freeze`, source commit
and shim form and setting — differing in one baked RTS string, `-A1G`. What
that buys is measurable rather than asserted: both `.text` sections are 20377797
bytes, every tracked loop sits at the same offset in both halves at the same
address, and `--library` reads 953 library self-loops at 100% same offset
and 100% same straddle. So no pad is derived, none is needed, and the two
columns are separated by a run-time setting rather than by a layout. **What
that does not buy is subtractability of the absolutes**, which every earlier
pair had and this one does not: the `-A1G` half carries a position-in-process
term the basis half does not, so its per-shape figures are inflated by an amount
that varies with a shape's slot. The paired ratios and the orderings are sound;
the magnitudes come from the differencing named at the head of this chapter.

The desktop named at the head of this chapter is the same machine whose `idiv`
cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and should
say which machine here.

**The sequence was launched once and ran to the end in one window**, 06:58:23
to 13:28:21, eighteen processes, every one exiting 0 with the bench count
its roster asked for — 1128 twice and 141 sixteen times — and none of them
reporting a selection it did not ask for. The machine carried no other load
for it, confirmed from an unsandboxed process list before the launch rather
than from the launching shell, and the tree was clean at launch by the driver's
own `git status`. Neither of Run 11's caveats applies, and the wall-clock log
is a single unbroken record.

**The pair's own identity, transcribed before its note went with it.** The two
md5s, the `Main.hs` commit and the tree at launch are at [the head
of this chapter](#about-the-last-run-run-14) and are not repeated here — one
live copy, since both places are replaced by the same run and a second copy
is only somewhere to drift. What this paragraph adds is what that head does
not carry: GHC 9.12.4 with `-fspec-constr`, and `align-as.py` as committed
at `89c7ae8`. **Both halves were built by hand**, this being a pair of two
shims, so both recipes went into the pair note: each is `cabal build micro`
with `-fspec-constr`, a `-pgma` of `align-as.py`, `-fforce-recomp` and a fresh
`--builddir`, both setting `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1`, and differing
only in `--ghc-options='"-with-rtsopts=-I0 -T -M8G"'` against the same
with `-A1G` prepended. Three things there are not optional and each was met
as a failure first: the inner quotes, without which cabal splits on whitespace
and the build dies on `-T`; not repeating the option instead, which builds
and silently keeps only the last; and `-fforce-recomp` with the fresh builddir,
GHC counting neither a `-pgma` nor an environment change as a flag change.
Those two md5s are what a rebuild has to reproduce for this chapter's figures
to be its own.

**The shapes have moved for the first time in seven runs**: five class views
gained a third shape, so every class is three-shape and no class figure here
is over the population its Run 13 counterpart was. The roster order is unchanged
and **membership moved by twelve arms**, the A/A twins of `offtab`,
`bq-odo-gm-mulback`, `build`, `mut-odo`, `list` and `gen-unsafe`, each in both
positions, taking both halves from 840 benches to 1128. That is what made
the `-L1` roster pass owed, and it was run and passed on this pair before
the evening — twice, the first pass covering a roster that five class shapes
and a moved twin then replaced — and recorded in the pair note. The addition
is again the weak-form evidence for the pinning claim, leaving every tracked
loop at the same address, and no more than that: a twin reuses a rostered
function and emits no code of its own.

**The delta, so the population is recoverable.** What follows is the *only* form
in which a shape set or roster is recorded here: its difference from whatever
`Main.hs` holds now. A snapshot would need rewriting at every change and would
be a second copy of a list that already exists; a delta costs what actually
moved and shrinks to nothing when the two agree. A roster delta has two halves
now that membership no longer settles what ran: which arms the roster held,
and which of them it timed. **And a third: the ORDER they ran in.** Order
is not membership, it *can* move code layout, and Run 10 measured layout at 12
to 14% on the two arms whose loop the shim rescues — so a delta stated
in membership alone can read empty while the run is not repeatable. Whether
a given reorder moves anything is a thing to measure rather than assume, both
answers having turned up in one afternoon: `sum-only-early`'s slot-5-to-2 move
left all eight loops this page tracks byte-identical, while lifting it one
further place, above `list`, shifts every worker by ~40 KB and rerolls every
alignment. So record the order, and read the binary before deciding what
the record costs. **A fourth half arrives with the pairing and is not a delta
at all**: which half of the pair a figure came from, which is why the tables
below and the fingerprint say so.

- Run 14 measured today's shapes, class lists, roster membership and order,
  so its delta is empty — it is today. What a reader has to carry is which half
  a figure came from: everything published below is `run14-lookrts`,
  the default-nursery half, and `run14-a1g` contributes the yardstick's second
  column, the arm-by-arm comparison at the head of this chapter, and a class
  comparison on all eight populations.
- Run 13 measured today's class lists and today's roster **order**, on **five
  class views short of a third shape** and on today's roster **minus the twelve
  A/A twins added after it** (`offtab`, `bq-odo-gm-mulback`, `build`, `mut-odo`,
  `list` and `gen-unsafe`, each in both positions) — 840 benches against today's
  1128 — timing 35 of its own and leaving 24 untimed, winsorized per
  the estimator under `time`. What a reader has to carry besides is which half
  a figure came from: everything published below is `run13-maxskip`,
  and `run13-lookrts` contributes the yardstick's second column
  and the arm-by-arm comparison at the head of this chapter.
- Run 12 measured the same shapes, class lists and order, on Run 13's roster
  **minus `mut-flat-gm-nosum`** — 816 benches against Run 13's 840 — timing 34
  of its own, winsorized likewise. Everything it published was `run12-maxskip`,
  `run12-maxskippa` contributing its yardstick column, and its class tables
  are a max-skip half's as this run's are, which is the one thing that makes
  the two runs' class figures a same-kind-of-build comparison.
- Run 11 measured the same shapes, class lists and order, on the roster Run 12
  had, so its delta is Run 12's — what a reader has to carry there is
  that its published tables were the *aligned* half's, where Run 12's and Run
  13's are a max-skip half's.
- Run 10 measured the same shapes, class lists, membership and order,
  so its delta is empty too — what a reader has to carry there is which binary
  each of its figures came from, its Results table being `micro-unaligned`'s
  while its fingerprint and class blocks were `micro-aligned`'s. That mixed
  basis was the transition to this one and lasted the one run.
- Run 9 measured the same shapes, class lists and membership **in a different
  roster ORDER**: `sum-only-early` sat at slot 5, moved to slot 2 ahead
  of the three distant A/A twins after that run, and to slot 1 above `list`
  for Run 10 ([the floor section][floor]). The first move relocated nothing —
  a binary rebuilt from Run 9's own commit `96378d2` puts all eight tracked
  loops at the same offsets as the moved roster does, to the byte —
  and the second relocated everything, which is what Run 10 spent to buy
  the pool fix and its predictions. **Run 11 did not spend it again**, which
  is the second thing alignment bought the schedule: in an aligned build
  a roster change relocates no loop, so the repetition this page had never had
  was available for the first time and is what Run 11 took.
- Run 8 measured today's shapes and today's class lists, on Run 12's roster
  **minus the eight arms written between them** (`bq-expand-gm-mulback`,
  `bq-odo-gm-mulback`, `mut-flat-gm`, `offtab-scan-rem` and the four
  `mut-odo-vecdims-add-*`), **timing all of it but `concat-runs`** where today
  leaves 24 untimed, winsorized likewise. Run 7's delta is Run 8's plus
  the regime, which is what keeps the last two columns in [What Run 15 compares
  against](#what-run-15-compares-against) a controlled pair and the first two
  a different controlled pair.
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

**The anchor, so a moved baseline is visible** — and it is the one column
that could have said the machine had changed under the run. Every published
figure is a ratio to `list`, so a change in `list` itself — a new compiler,
a new machine, a changed `toListT`, or a compiler flag — rescales the whole
table while leaving every ratio intact and undetectable. These three absolute
per-call figures are the guard, and against Run 13's basis half they read
**+0.86%**, **+2.10%** and **+0.74%**, computed from both runs' cells rather
than from either table's three digits — all three up, and all three inside
the drift band. **`cifar-L2-16-c64-k3` is the widest of the three for a fourth
run running**, which is now past the point where a one-in-twenty-seven
coincidence covers it; what has changed is its size, +2.10% against the +4.3%,
+4.31% and −3.91% of the three before, and its sign, back to positive after one
negative. A shape that is always the widest and never the same magnitude
is a shape to keep instrumented rather than a property established,
and the previous write-up's reading — worth recording, not worth a mechanism —
is the one this run leaves in place, with the coincidence explanation weaker
than it was. The control half's figures are given beside them — and unlike every
earlier pair's they are not a second measurement of the same thing: the `-A1G`
column carries the position-in-process term this chapter's head describes,
so a shape's figure there is inflated by an amount that varies with its slot.
Read the column for its direction and read no baseline drift off it:

| shape | `l` | `list`, per call | net | +A1G, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 5.49 µs | 5.32 µs | 7.30 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.26 ms | 3.17 ms | 3.61 ms |
| `stretch-wide-2xM` | 1800000 | 34.7 ms | 33.6 ms | 44.4 ms |

Each stride class carries an anchor of its own, beside its table, and this time
the eight **do** scatter: five moved up and three down, none of them past 1.1%,
where Run 12's eight all moved down and Run 11's eleven ran −1.8% to +4.3%.
Those eight are computed from both runs' cells, Run 12's class JSONs being
on disk though its binaries are not. Scatter is what a rebuild alone should look
like, and it is what Run 12's eight could not show: theirs read a change
of basis half, this run's shares that basis with them and has only the rebuild
left to read. A baseline that had changed for one *mechanism* — under negative
strides, say, or a stride-0 read — would still show as one class out of step
with the other seven rather than as eight small movements either way.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.585–0.602 ns per element across the whole set, so a raw
slope is the published one plus about `0.60e-9 * l`, with `l` from `Main.hs`.
That recovers any uncorrected figure to within the term's own 3% spread — enough
to hold a corrected run against any number measured before the correction
existed. The term is within 1% of every run's since Run 7, so neither the flag,
the roster, the layout, the shim's padding, `-fproc-alignment=64` nor now an RTS
line touches the forcing pass, which is the control saying seven runs'
corrections are one correction — and this pair's two halves agree on
it as closely as any, the control reading 0.586–0.603 against the basis half's
0.585–0.602, so a figure differenced across these halves carries almost none
of its own.

**What the next run replaces.** Run 13's numbers reach past the Results table,
so this is the list to walk when Run 14's land. Run 10 walked it twice
over and not symmetrically, one half per pass; Run 11, Run 12 and Run 13 each
walked it once, one basis publishing everything, which is how it is walked
from here. It names *sections*, not figures: a list of figures is a second copy
of them, and enumerating it was how the previous two versions of this list went
stale — one missing six sections, its predecessor leaking past it. What now
guarantees completeness is mechanical instead. Every section below is reached
by an anchor, and the coverage check is: no section carrying a figure outside
a table may be absent from these links. Run that check, and repeat the two
sweeps it cannot replace — grep this file for figure-shaped numerals outside
the tables, and grep it for the name of the run being superseded, which
is the one the chapter head above still carries — before trusting the list.
The second sweep is written without its numeral on purpose: spelled out, it
is a run number the rename step does not reach, so it would go on naming a run
two runs back. It earns its place every time: this run's pass found eight links
whose *text* still named the superseded run while the anchor beside it had
been renamed, which the anchor check cannot see because every one of them
resolved.

**Inside a section, find the paragraphs rather than reading it.** The list names
sections and a section here runs to hundreds of lines, of which a run rewrites
three or four paragraphs; Run 10's write-up read most of the floor section
to change four of its leads. **Not every paragraph opens with a bolded lead**:
457 of 868 carry a bolded span and 411 carry none, and 37 of those 411 carry
a figure. So `grep -n '^\*\*' README.md` between a section's heading
and the next gives a section's **claims** and not its contents, and a walk
that stops there misses figure-bearing prose — the opening section's continuous
argument, and continuation paragraphs inside list entries. The ones a run
touches are those whose lead or body carries a figure, which is why `--para`
falls back to the body when no lead matches. `./read-run.py --para 'lead'`
then prints any one of them with the line it starts at, which is what keeps
a jump off the `grep -n`/`sed -n` pair that the install above it has already
invalidated. `--check-doc`'s two sweeps print line numbers for the comparative
and superlative candidates already, so between the three the walk is a list
of jumps rather than a read. This is deliberately a recipe and not a stored list
of paragraph names: a stored one would be a second copy of the structure
and would rot the first time a lead was reworded, which is the failure this list
was rewritten to escape.

- [the head of this chapter](#about-the-last-run-run-14), which carries
  the run's name, regime, scale and source commit, the layout span a roster
  order change alone is worth, and which half published what;
- [the recommended tasks after Run 14](#recommended-tasks-after-run-14), which
  is run-scoped by its own title: a task taken or superseded leaves it, what
  survives is renamed to the run that inherits it, and a run's own surprises
  are added to it before its chapter is replaced;
- [the Results table](#results), which `--markdown` emits whole,
  and the findings under it;
- [What Run 15 compares against](#what-run-15-compares-against) — the yardstick
  geomeans in every regime measured and the two-column per-shape fingerprint,
  all of which a run replaces wholesale, and which are the only per-shape record
  kept once the JSON is deleted;
- [The claims Run 15 should test](#the-claims-run-15-should-test), where a run
  reports which held rather than re-deriving them, and whose readings are run
  figures throughout;
- [the noise-floor table][floor] and its prose, from `--aa` — including
  the raw-slope six it compares against, the position verdict the crossed
  controls now disagree about between runs, and the `build`/`mut-odo` pair read
  as a second control;
- [the opening section][opening]'s headline ratios and its regime paragraph;
- [The stride classes, run by run](#the-stride-classes-run-by-run) — the summary
  table, and each class's own table, controls, provenance, anchor and paragraph.
  All of that is a run's, in the way the Results table is; the layout above them
  is not, in the way the column definitions are not. A run that leaves
  a population out says so there, rather than leaving the previous run's table
  standing under a new run's name;
- [The mutable ceiling (not taken)](#the-mutable-ceiling-not-taken)
  and the shipping paragraph closing [the Lemire section][lemire].
  These are *rulings resting on figures*, so a stale number re-opens a decision
  rather than merely misreporting one — and a ruling's number moves for reasons
  its verdict does not. Both now carry two regimes, and the Lemire one turns
  on which regime orthotope compiles under, so a run in a third would have
  to say what it does to that decision rather than only to the figure. Requote
  from the run; do not carry forward;
- [The C-gap](#the-c-gap-still-a-deeper-ceiling), whose figures are horde-ad's,
  not a run's: no run here replaces them, and they move when that repo
  re-measures — so the walk checks their currency instead;
- [The scratch vector flavour](#the-scratch-vector-flavour), whose figures
  are a probe's too, and whose conversion is why no `bq-*` figure predating
  it is comparable with one after it;
- [One element type](#one-element-type-and-what-the-probe-found), whose figures
  are a probe's and which no run replaces either. What would call for re-probing
  is a run that moves the ordering at `Storable Double`, since the claim
  is that the other types follow it — which Run 8 does, in a regime the probe
  was not run in, so the trigger is live and is [on the open
  list](#what-is-open) rather than discharged here;
- [sum-only](#sum-only-and-the-correction-now-applied), where what a run decides
  is no longer *whether* to correct but whether the term still passes its three
  gates, any failure invalidating the column rather than informing it;
- [R2 is the ramp detector][ramp], [the Lemire section][lemire], and [the
  per-shape `stretch-*` table][pershape];
- [what the benchmark does](#what-the-benchmark-does), whose two roster rulings
  quote the run they were cut on — the arms they drop and the allocation tier
  the threshold sits above — and whose membership a later ruling can reopen;
- [the non-urgent TODO list](#non-urgent-todo-list), whose roster-order entry
  cites the position figures a run measures and whose decomposition entry cites
  the question a run leaves open — the one part of the harness chapter a run
  touches at all;
- the `alloc` column's shape-dependence, refuted and confirmed refuted at full
  budget: every multiple quoted anywhere is a property of a strategy
  *and* a shape set, so pin the shape set before comparing across runs,
  as `time` already asks — and now a property of the regime too, three
  of the column's levels having moved with the flag alone;
- [What is open](#what-is-open), whose whole content is questions a run answers
  and figures a run moves;
- this section, which becomes the next run's own provenance;
- `read-run.py`'s docstring, whose `time`, `corr` and `net` definitions and A/A
  paragraph quote the run;
- `micro.cabal`'s `-M2G` note, if the printed heap peaks have moved;
- `Main.hs`, wherever a comment cites a figure — now `fbBQmutRunsGmMulback`'s
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
benchmark run](#making-a-major-benchmark-run) — which is also where the walk
of the list above is one of the steps.



[achieved]: #how-the-strictly-positive-picture-was-achieved
[bench]: #what-the-benchmark-does
[ceiling]: #the-mutable-ceiling-not-taken
[cgap]: #the-c-gap-still-a-deeper-ceiling
[classes]: #the-stride-classes-and-what-they-cover
[correction]: #sum-only-and-the-correction-now-applied
[dead]: #dead-ideas
[fix]: #the-fix-in-dataarrayinternalhs
[floor]: #what-moves-a-figure-when-no-strategy-changed
[lemire]: #lemire-multiplicative-inverses-at-the-two-division-sites
[open]: #what-is-open
[opening]: #regime-3-micro-benchmark-the-fix-bq-expand
[pershape]: #per-shape-where-the-geomean-hides-the-ordering
[pos-effect]: https://github.com/Mikolaj/horde-ad/blob/master/docs/position-effect.md
[probe]: #one-element-type-and-what-the-probe-found
[procedure]: #making-a-major-benchmark-run
[prov]: #provenance
[ramp]: #r2-is-the-ramp-detector-not-the-noise-detector
[reader]: #the-reader-read-runpy
[results]: #results
[settled]: #what-is-settled-and-where
[scratch]: #the-scratch-vector-flavour
[shapeset]: #the-shape-set
[todo]: #non-urgent-todo-list
