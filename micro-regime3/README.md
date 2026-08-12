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
with its dimension lists replaced by unboxed vectors — is on Run 11
(SpecConstr) **2.13×** over `bq-expand` and the fastest strategy measured
here. Both need a new `Vector`-class method, which was
measured and deliberately **not** taken, to keep orthotope's `Vector` API
pure and minimal — a bar an in-tree precedent has since softened to a weight
([below](#the-mutable-ceiling-not-taken), amended). Plain `mut-odo` no longer
argues for it at all: it and the shipped arm are a tie, winning nine shapes
of 24 with sign p 0.31 and an interval covering 1, where Run 7 (Harness), at
-O1, had it 1.51× ahead.

Several strategies measured since are faster than what shipped and need no
class method. The fastest pure ones on Run 11 are
**`bq-scan-rem-gm-mulback`** (0.089) and **`bq-odo-gm-mulback`** (0.090)
against `bq-expand`'s 0.103 — a margin of **1.15** paired on each, where Run
10 read 1.14 on both halves of its pair. So it is no longer a margin sitting
inside the 1.22 that placement alone is worth in an unaligned build, to be
read as a candidate rather than a verdict: alignment removed that term, and a
run repeating Run 10 exactly — same binary, same roster, same order —
reproduces the margin to a hundredth ([the head of the run
chapter](#about-the-last-run-run-11)). They also carry **no size precondition
at all**, which is the point of them, a ruling since having stopped this
suite timing any arm that needs one ([what the benchmark
does](#what-the-benchmark-does)). Neither is what
`Data/Array/Internal.hs` does today. Of the trade-offs, allocation and a
noise floor this run measures at 0.22% across the six control pairs of its
max-skip half, and 0.33% across four of the six on the half the table comes
from, are in [Results](#results), each
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

And **one regime's**, **one roster's** and now **one layout's** as well. Runs
8 through 11 all
compiled the suite with `-fspec-constr`, where every run before them took the
plain -O1 a default `cabal build` of orthotope takes, and the flag reorders
the table rather than nudging it — it speeds `list` itself by 8%, `bq-expand`
by 27% and the plain scan family by 31%. The 19% it was also said to *cost*
`mut-odo` is not the flag's: `build` compiles to the same worker and moved
17% the other way, which identical code cannot do, and the pad probe has
since priced that disagreement as placement ([the floor section][floor]).
Every figure in this sentence crosses a rebuild and so carries some of the
same term; the three that survive it do so by being larger than it. Run 9
then changed the roster and nothing else, and moved arms from 9% faster to
19% slower with the baseline standing still; Run 10 changed only the roster's
*order* and moved them 3% faster to 14% slower, and then measured the layout
term directly by running the same source from two binaries that differ in
where its loops sit — 12 to 14% on the two arms whose loop straddled a cache
line, and a percent or two the other way on everything else. **Run 11 then
changed nothing at all**, re-running Run 10's aligned binary, and moved every
arm but one by under 1.5% and `list`'s worst cell by 4.3% ([the head of the
run chapter](#about-the-last-run-run-11)) — which is what the three figures
above have to be read against, and is a quarter of the band that was
available before the layout could be held still. So a figure here belongs to
a flag, to a membership, to an order *and* to a layout, and the last is the
one this page can now remove rather than only price. **Whether orthotope
should carry the flag is not this page's question** and is deliberately not
on its open list: this is a replica
of one function, where that decision is a library-wide one about compile time
and code size, and the measurement that would settle it is horde-ad's
`convVjpBench` over a real build. The 27% is what this page contributes to
it.

## Contents

Thirty-odd sections, so the map is here rather than left to a grep. It is
anchors and not line numbers on purpose: `--check-doc` verifies that every
anchor in this file resolves, so this list cannot rot silently, where line
numbers would be wrong by the next edit and say nothing.

- [What is settled, and where](#what-is-settled-and-where)
- [What is open](#what-is-open)
  - [Non-urgent TODO list](#non-urgent-todo-list)
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
  - [What moves a figure when no strategy changed](#what-moves-a-figure-when-no-strategy-changed)
  - [R2 is the ramp detector, not the noise detector](#r2-is-the-ramp-detector-not-the-noise-detector)
  - [sum-only, and the correction now applied](#sum-only-and-the-correction-now-applied)
- [About the last run (Run 11)](#about-the-last-run-run-11)
  - [Results](#results)
  - [What Run 12 compares against](#what-run-12-compares-against)
  - [The claims Run 12 should test](#the-claims-run-12-should-test)
  - [The stride classes, run by run](#the-stride-classes-run-by-run)
  - [Provenance](#provenance)

## What is settled, and where

**One line per thing this page has established, and the section that holds
it.** It exists because the file is long enough to re-derive itself: the
`build`/`mut-odo` Core identity was dumped, diffed and drafted as a new
finding, and found afterwards to have been recorded at [the mutable
ceiling][ceiling] since Run 8, a thousand lines from where the session was
working. Read this before deriving anything and grep it before writing
anything up.

**It carries no figures, and that is the design.** A figure here would be a
second copy of one kept elsewhere, which is how two versions of
[Provenance][prov]'s replace list went stale before it was rewritten to name
sections rather than numbers. Each entry names a subject and a home and stops;
the numbers live at the home and move with the run. An entry earns its place
by being a thing a later session might otherwise redo.

- **The fix that shipped** and why the base-offsets table is built by
  expansion rather than by division: [the fix][fix], with the four findings
  behind it in [how the picture was achieved][achieved].
- **The mutable ceiling**, why a direct mutable fill was not taken, and the
  amendment that turned that bar into a weight: [the ceiling][ceiling].
- **The class-method signature is free** — `build` and `mut-odo` compile to
  the same worker, dumped in both regimes — so no `vBuild` is held back on a
  figure: [the ceiling][ceiling].
- **Code placement moves figures**, and by more than the A/A controls can
  see: the identical-code pair, the rebuild bias, the per-loop reading and
  the cache-line table are all [in the floor section][floor]. **Straddling a
  cache line is a cost and not a correlation** — the pad probe stepped two
  arms through every offset — **and the penalty is graded** by where the
  split falls: same section. **But it is not the account of every gap it once
  seemed to explain**: Run 10 read three arms at four placements each and
  two of them kept their 16% with no copy straddling anywhere, which is what
  withdrew a suspension [the ceiling][ceiling] had placed on its own figures.
  The probe's own design, including the two kinds
  of pad that relocate nothing, is [on the open list][open] with what is
  still open about placement.
- **GHC's native backend aligns no loop**, where GCC, clang and GHC's own
  LLVM backend all do; `-fproc-alignment=64` pins the offsets rather than
  choosing them, and an assembler shim on `-pgma` aligns the loops outright,
  which is the instrument fix. What it costs and buys in time is [on the open
  list][open]; the rest is [in the floor section][floor], including why the
  shim must pad only between instructions. Two tools beside this file:
  `loop-offsets.py` reads a binary's copies, which makes the question a
  minute's work rather than a run's, and `align-as.py` is the shim; a paired
  run's two binaries come from `make-pair.py`, which derives the padding its
  unaligned half needs and refuses a pair that does not verify. Both this
  and the recompilation trap beside it are written up and filed as GHC issues
  from horde-ad's `docs/`, which is where a reader outside this page should
  go; what stays here is what they cost this benchmark.
- **The allocation area moves figures too** — the default nursery against an
  arm's allocation in excess of its result — with the predictor and the
  populations it reaches [in the floor section][floor].
- **The A/A controls are the noise floor**, not the printed CI, and what they
  do and do not bound is [in the floor section][floor]; R² is the ramp
  detector rather than the noise detector, [here][ramp].
- **Run-to-run drift, with shapes, roster, order, regime and layout all
  pinned**, measured for the first time by re-running one binary: a few
  percent per cell, a quarter of a percent on a geomean, and two arms that
  exceed it, [in the floor section][floor].
- **The forcing pass is subtracted from every figure**, on three gates that
  every run and every population re-passes, and gate 3's standing bias:
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
- **The roster is cut by two rulings** — a size precondition disqualifies an
  arm, and so does allocating past a bar — and a majority of the roster is
  checked without being timed: [what the benchmark does][bench].
- **The shape set was halved and is not to grow back one shape at a time**:
  [the shape set][shapeset], the ruling itself beside `convShapes` in
  `Main.hs`.
- **The stride classes are separate populations**, tabled beside the main set
  and never merged into it: [the classes][classes].
- **Ideas that died on paper** are recorded so they are not re-proposed:
  [dead ideas][dead].
- **Pure Haskell cannot close the gap to the C kernels**, which bounds every
  strategy here: [the C-gap][cgap].
- **How a run is made and analysed**, including what a run does *not* touch:
  [the procedure][procedure], [the reader][reader] and [Provenance][prov].
- **What is open** is the chapter directly below, this index's complement,
  each question carrying the measurement that would settle it and what needs
  a quiet machine: [the open list][open], with the harness's own backlog
  folded in under [the TODO list][todo]. Nothing open is recorded anywhere
  else.

## What is open

**The complement of the index above, and read with it.** That one says what
is settled and where; this says what is not, each question with the
measurement that would settle it and the run that can supply it. Between
them a session knows what it must not re-derive and what is worth deriving,
which is the pair the file opens with rather than the two lists it used to
end its chapters with.

**This is the only home for an open question.** They are collected here
because otherwise they sit one per section and get reconstructed every time
— and worse, get missed: the question of why the count-down FastReshape form
pays was raised inside [the mutable ceiling][ceiling]'s own write-up and
never migrated, so a session that mined this list and its queue walked past
it. A question recorded anywhere else is a bug to be moved here, not a note
to be left where it was written. The harness's own backlog is folded in
below, for the same reason: two backlogs a thousand lines apart is how one
belongs to neither.

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
and was then the only route left to this question. **It has since been run**
and prices layout alone at 1.16 to 1.19 on a shared loop ([the floor
section][floor]), which is more than the 13% asked about here, so layout
remains a sufficient account of it; what the probe does not supply is this
arm's own offsets across the two runs, and Run 10's first prediction is where
its family is read. Its fourth prediction closes the question for every arm
at once, the two halves' difference being each arm's own layout term, so this
entry ends there or nowhere.

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
section][floor], and it carried **a roster fix, since applied twice**:
`sum-only-early` moved first from slot 5 to slot 2, ahead of the three
distant A/A twins, which were being calibrated against a colder heap than
everything they calibrate — on that roster the 41% cell reads 0.24% — and
then, for Run 10, above `list` as well, which is the warm-up bench [the TODO
list][todo] had been asking for and leaves nothing measured on an ungrown
pool.

  **It was answered the same day, and the decision it forced is kept
  with the account**: keep the default area, and carry the caveat that
  the headline ratios are partly a statement about it ([the floor
  section][floor], which also holds the predictor for which cells the
  setting reaches, and the nine populations it has been applied to).
  What stays open is the size of it — how much of a published geomean
  moves is a run and not a probe, and it heads the queue below.

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

**What Run 10 leaves open**, each with what would settle it:

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

  **Answered, 2026-08-10: for a loop this size, placement costs 1.16 to
  1.19.** The first attempt at this left the question narrower than it found
  it — it should have timed `build` across the four layouts and did not, a
  shell glob having eaten the arm ([the reader's
  section](#the-reader-read-runpy)) — and what settled it instead was the pad
  probe done properly, eight binaries stepping each arm through all eight
  8-byte offsets with membership fixed ([the floor section][floor] carries the
  figures, the graded penalty and the tables). So the *how* is now measured
  and not merely read off a
  binary: a straddled copy of the 28-byte fill costs 1.19, or 1.10 where only
  three bytes precede the boundary, and that is what the pair's 0.86-to-1.24
  span across runs was made of.

  What the probe does **not** reach is the rest of this entry. The 18% a
  rebuild is worth stands as measured, since a rebuild moves more than one
  loop's offset; `offtab`'s and `bq-gen`'s regressions have no shared-loop
  counterpart to be read this way, which is the entry below on crediting a
  margin to a strategy; and susceptibility remains a property of the arm, now
  with a mechanism for the two arms that share a loop and none for the
  others.

  **Run 9 had made this the page's central question rather than a caveat on
  it**, and that is the framing the answer inherits. A membership change alone
  moved five fingerprint arms from 0.910 to 1.192 in absolute time against a
  baseline that held to 0.998, and moved `build`/`mut-odo` — one worker, two
  slots — to 1.13 where Run 8 read 0.86 and Run 7 1.24. Every route through
  the roster was blocked, the roster being one of the things that sets the
  layout, which is why the answer had to come from a probe that holds
  membership still.
- **The queue of experiments that want a quiet machine**, ranked, so that the
  next quiet window is not spent deciding what to spend it on. Written down
  2026-08-09 with Run 9's artifacts still alive, and the ranking turns on one
  thing worth stating: *the binary must not be rebuilt between the arms of a
  comparison*, since a rebuild is worth up to 18% on a susceptible arm and
  swamps most of what is being asked.

  **Ordered against Run 10 rather than by value, 2026-08-10, now that its
  regime and roster are fixed.** One entry goes before it and the rest after,
  and the reasons are the schedule rather than the ranking: an experiment
  whose answer changes how Run 10 is *read* is worth its window first, while
  one Run 10 supplies half of for nothing is worth waiting for. Durations
  below are quiet-machine costs, derived from the elapsed time and bench
  count a run's own provenance line reports — about five seconds a
  bench-shape cell, criterion spending its budget whether the call is fast or
  slow — and nothing here measures what contention does to them. **The gate
  entry below has since been folded into Run 10 rather than queued behind
  it**, alignment having turned out to be the thing that decides whether the
  rest of the queue is measuring anything; what stays there is the cheap gate
  that runs before the run does. Entries are referred to by name and not by
  number, one having been removed from under a reference already.
  1. **The pad probe done properly — run 2026-08-10, and the hypothesis
     survives.** Eight binaries differing only in inert pad arms, two
     interleaved passes over all eight, 2h12m, with `build` and `mut-odo`
     both timed this time (the first attempt lost them to a shell glob) and
     each stepped through all eight 8-byte offsets — the step being all GHC
     aligns the loop to — with membership fixed throughout. A straddled copy
     costs 1.19, or 1.10 where only three bytes precede the boundary, and the
     two discriminating binaries invert as predicted: [the floor
     section][floor] carries the verdict, the graded penalty and the
     controls. Placement and the allocator are separate effects, which is why
     this wanted a window of its own rather than being shrunk by 1: the
     `build`/`mut-odo` gap was measured across the nursery change and did not
     move.

     **Two pad designs relocate nothing, so they are not retried** — measured
     on 2026-08-10 rather than reasoned about, and recorded here because the
     directory that first held them is to be deleted. Module-level inert pads
     that nothing rosters left both arms exactly where they were, across six
     variants. So did permuting two untimed roster entries deep in the list,
     which relocates only each other. What works is a pad rostered *before*
     the arm it must displace, emission order tracking first reference from
     `roster`; a pad kept inert by rostering it `Only` is checked on every
     shape and timed on none, so the selection stays what it was. Nothing else
     in that file was load-bearing, which was checked before deleting it: its
     shell-glob trap, its rule about counting what a filtered run selected and
     its correction caveat were already in [the reader][reader] and [the
     procedure](#making-a-major-benchmark-run), and what went with it was a
     per-binary offset map for binaries that are themselves gone.

     **It went before Run 10, which makes Run 10 a replication rather than
     the evidence** — the point of that ordering, two of Run 10's registered
     predictions being the straddle hypothesis, and Run 10 testing
     it while moving roster order, heap warmth and code layout together where
     these binaries moved one thing and held the rest. It did more than
     replicate, in the end: answering the hypothesis is what turned Run 10
     from one binary into two, since an effect this size is worth removing
     once it is no longer in doubt. The asymmetric risk it
     was run against did not materialise: [the floor section][floor]'s loop
     table and [the suspension of two FastReshape axis figures][ceiling] both
     rested on a correlation inside one binary, and both stand, the
     suspension now with an out-of-sample check of its own. The binaries and
     the sixteen run files were untracked in `pad-probe/`, ~280 MB, and are
     deleted: this page carries what they showed, and the effect has a
     self-contained public reproducer in the filed issue.
  2. **A third `-nosum` arm, on a flat fill** — a `Main.hs` addition and then
     a filtered run over the shape set. The two existing `-nosum` arms are an
     odometer and an expansion, so a flat fill is the one probe that
     separates *the read is biased* from *those two arms are*, which is what
     gate 3's entry below now needs. Cheaper than it reads — four benches
     over the shape set is minutes, and most of what used to hold it back is
     gone: it wanted a full run rather than a filtered one so that its
     reading is comparable with those already taken, and adding an arm is a
     membership change which, in an aligned build, relocates no loop — the
     first thing alignment buys the queue rather than the tables.
     **But it must not go into a run that is taking the exact repetition**,
     and Run 11 was that run. The repetition needed membership pinned as well
     as layout, so this entry and the roster entry below could not both be
     satisfied at once; the resolution is ordering, not a judgement about
     which matters more. Recorded here rather than left to be rediscovered,
     because the two entries read as independent and are not.

     **It is now postponed again, to Run 13, and for the same kind of reason
     twice over.** Run 11 took the repetition; Run 12 takes the basis
     question that Run 11's second answer opened, and adding an arm in the
     same run as a change of shim would confound the arm's own cost with what
     its arrival does to a layout the new shim no longer pins. So the order
     is: Run 12 settles which build publishes the table, Run 13 adds this arm
     to whatever that turns out to be — and if Run 12 lands on a basis
     without membership invariance, Run 13 owes a check that the addition
     relocated nothing before it owes anything else. Twice postponed is worth
     noticing rather than defending: this arm has been due since Run 11 and
     is cheap, so if it slips a third time the reason should be written here
     or the entry should be promoted over whatever displaced it.

     **Run 11 answered the cost half and left the decision harder, not
     easier.** Max-skip won on cost: the cheaper build nearly everywhere at
     a third of the padding, nothing below 0.99 but `build`, up to 1.06 the
     other way ([the head of the run chapter](#about-the-last-run-run-11)).
     But cost was never the whole of it, and **the two virtues now point
     opposite ways for this particular run**: the unconditional shim's
     unconditionality is what makes a loop's offset invariant to membership,
     max-skip gives that up by padding only the heads that need it, and Run
     12 is precisely the run that **adds an arm**. So taking max-skip as the
     basis and adding the third `-nosum` arm in the same run reintroduces
     the thing alignment was adopted to remove, and the run would not be
     able to tell an arm's own cost from what its arrival did to the layout.
     **The way out is the one this page's pairings already use, and stating
     it saves the next run rediscovering it: the second half is where the
     run's question goes.** Run 10 paired against an unaligned build and
     priced layout; Run 11 against max-skip and priced the padding.
     **Run 12's pair is `micro-maxskip` and `micro-maxskippa`**, both
     carrying the shim in its max-skip form and differing in
     `-fproc-alignment=64` alone — built and gated 2026-08-12, the recipe,
     the derived padding and the checks in `micro-pair-run12.txt`. **The
     basis is `micro-maxskip`**: it publishes the table, which is a change of
     basis and the second this page has made.

     Two things about that pair are worth having here rather than only in
     its note. `micro-both` was the obvious candidate and is the wrong one:
     it carries the *unconditional* shim with the flag, not because anything
     preferred that combination but because it was built on 2026-08-11 at
     12:51, hours before the max-skip form existed at all — a composition
     that is chronology and not design, and a name that invites being read
     as design. And the pair does not separate the flag from the offsets it
     produces, since pinning procedures is *how* it works: the halves' fills
     are `[11, 0, 4, 0]`/`[24, 8, 0, 0]` against `[4, 0, 4, 0]`/`[8, 8, 4,
     4]`, none straddling either side. That is the right quantity for a
     basis decision, adopting the flag being adopting its offsets, and the
     wrong one for asking what a resident offset costs alone — which is a
     probe on the pad-probe model and not a paired run, and should not be
     loaded onto Run 12.

     So the three runs decompose the two variables one at a time: Run 11
     priced the shim, Run 12 prices the flag, and **Run 13 adopts whichever
     combination the two price best and adds the arm under the flag's
     invariance**, which is what makes an addition safe to attribute.
  3. **The five-bench gate before Run 10's aligned half — run 2026-08-10 and
     it passes**, its verdicts and two corrections being with the predictions
     above. Kept because a later paired run wants the same gate before its own
     evening:

         ./run-gate.sh        # the two-process form this entry used to spell
                              # out is superseded: the script runs four, in a
                              # palindrome, and names its files
                              # gate-<half>-<pass>.json, which is what the
                              # procedure's read commands expect

     run against `micro-unaligned` too, and expect 120 `benchmarking` lines
     each, then `--compare` one against the other, which is the reader's mode
     for an arm across two runs of one population and what prediction 4 is
     read with. `*/list` is in it for two reasons: it gives prediction 5 an
     early reading, and without a baseline `--selftest` has no ratios to
     check. With both executed copies resident at 0, `build`/`mut-odo` must
     read **1.00** and both arms must run at the resident level, which against
     Run 9's placement is 10 to 19% faster rather than merely equal. A pair
     that reads 1.00 while neither arm moves would refute the penalty while
     confirming the symmetry, and that is a distinction no run so far can
     draw. Minutes, and it is the cheapest place to find out that the aligned
     binary is wrong before an hour of main set is spent on it. The dear half
     of this entry — a main set aligned against one unaligned — is no longer a
     queue item at all: it *is* Run 10, whose fourth prediction is that
     comparison read arm by arm.

  And three things **not** worth a quiet window, recorded so they are not
  reached for. The *how many preceding benches warm it* sweep, which the
  nursery finding supersedes — the bench count is the symptom and the
  allocation area is the cause. The element-type re-probe, whose trigger
  is a run that moves the ordering at `Storable Double`, which Run 9 does
  only through layout and membership rather than anything an element type
  would feel. And **an A/B of the pre-swap binary against the post-swap one,
  to price the roster swap on its own** — proposed and refuted the same day:
  that swap moved heap warmth *and* relocated every worker by ~40 KB, so
  binary against binary conflates exactly the two things Run 10's unaligned
  half conflates, and buys a number Run 10 supplies anyway at the price of a
  quiet hour and a false sense that one variable had been pinned. **Half of
  that refutation has since expired and the other half has not.** In an
  aligned build a roster swap relocates no loop, so such a pairing would no
  longer conflate the two — but it would still buy a number Run 10's third
  prediction supplies for nothing, which was always the stronger of the two
  reasons. Recorded because the expiry of a premise is exactly what makes a
  dead idea look alive again.
- **Is the term still unbiased?** Gate 3 passes and still does not bracket 1:
  every in-situ median of both arms in all ten of Run 10's processes sits
  below it, **0.9641 to 0.9903**, for the **third** run running
  ([sum-only](#sum-only-and-the-correction-now-applied)) — and the two halves
  of the pair agree about it, so it is not a layout term either. Three runs
  on one side is no longer the coin-flip the failure test
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
- **Run 10's predictions, and how they came out.** The run is made; the
  verdicts are here, with the registrations they are read against left
  standing underneath so that what was predicted before the hours were spent
  stays legible. **Two held, one held only in direction, one split and one is
  refuted.**
  1. **Split, and the split is the finding.** `mut-odo-vecdims-add-in`
     collapsed as predicted — 0.9937 on the unaligned half, where all four
     copies are now line-resident, and **1.0009** on the aligned half, where
     the prediction was 1.00 outright — so its Run 9 reading of 1.1552 was
     layout and is gone. `add-out` and `add-both` did not: they read 1.1266
     and 1.0906 unaligned and **1.1612** and **1.1184** *aligned*, with every
     copy of the loop at offset 0. The registration says a reading near 1.16
     surviving alignment kills the hypothesis for the arm that carries it,
     and `add-out`'s does. So the straddle account holds for one of the three
     and is refuted for the other two, and [the suspension of those axis
     figures][ceiling] resolves the same way — withdrawn for `add-in`,
     converted into a measured cost for `add-out` and the corner.
  2. **Held in direction, missed its point value.** `build`/`mut-odo` reads
     0.9532 paired unaligned and **0.9685** aligned, against a registered
     0.998 and Run 9's 1.13. So the pair closed past 1.0 rather than onto it,
     and on the aligned half — where both copies sit at offset 0 and the
     prediction is 1.00 by construction — identical code still differs 3.2%
     by geomean while tying by the sign test (16 of 24, p 0.15). The gate had
     already read 0.961 to 1.008 aligned, so this is the gate reproduced at
     full budget rather than a new disagreement.
  3. **Refuted.** The anchors did not fall. `list`'s net per call, aligned,
     against Run 9: `cnn-slice-c32` −0.6% (the control, predicted to hold,
     and it did), `cifar-L2-16-c64-k3` −2.5%, `stretch-wide-2xM` +0.2%, and
     across the eight class anchors −1.1% (`rev-primes`) to **+7.9%**
     (`bcast-inner900`), four of them rising by more than a percent. Ten of
     the eleven cells were
     predicted to move down and did not, which is the prediction's own second
     disjunct: **warming does not reach the baseline.** What the swap did buy
     is prediction 1's sibling finding below — the wild cell — so the roster
     move is vindicated by the controls and not by the anchors, and a
     predecessor's one large allocation is evidently not the same lever on
     `list` as the nursery size is ([the floor section][floor] measures the
     latter at 1.79× on one shape).
  4. **Held, and it is the run's main result.** `mut-odo` reads **0.8632** of
     its unaligned self and `build` **0.8771**, each on 22 shapes of 24,
     against a registered ~0.85 and the gate's 0.8836 and 0.8778; the two
     agree to 1.6% where the gate had them at 0.7%, against a per-shape floor
     the gate put at 6.3%. The four already-resident `mut-odo-vecdims` arms
     moved a few percent at most, as registered, and all four the *slower*
     way — 1.0069, 1.0143, 1.0326 and 1.0378, the last on 0 shapes of 24 —
     which the registration allows for as the shim's own NOP cost and which
     is worth carrying as a measured price rather than a possibility. For the
     rest of the roster the moves do fall in two groups: two arms at 0.86 to
     0.88 and every other at 0.97 to 1.07.
     An independent route agrees: differencing whole-process wall time at a
     fixed `-n`, five interleaved pairs on `stretch-wide-2xM/build`, gives
     0.887 where the reader's per-shape cell reads 0.8688 — two instruments
     sharing no code, 2% apart, on a cell whose own spread across passes is
     8%. System time was 0.02 s throughout, so wall and user+system agree
     here and the two-clock caution finds nothing.
  5. **Held.** `list` reads **1.0058** aligned over unaligned, 8 shapes of 24
     — 0.6% where the gate read 0.3%, and inside the unaligned half's own
     1.00% A/A floor. The baseline is still, so the denominator holds, the
     three things resting on this one stand, and the mixed-basis page is
     readable.

  **And the roster fix is confirmed at full budget, which no prediction
  claimed.** Run 9's `bq-expand` distant twin read 1.0152 with **41.4% on one
  cell** of `vgg-14-c512-k3`; the same pair now reads 1.0043 with its worst
  cell 1.67%, and the six A/A pairs span 1.0011 to 1.0100 unaligned and
  0.9987 to 1.0054 aligned. The three-bench probe that priced the fix at
  0.24% is thereby reproduced over the whole roster and the whole shape set.
  What the aligned half does *not* do is tighten the floor everywhere: it
  halves the main set's (1.00% to 0.54%) and leaves `scaled` with a 5.36%
  pair on one cell of `scaled-super-r3`, the run's one bad control.

- **The registrations those verdicts are read against.** Its order was
  chosen for heap state — `sum-only-early` above `list`, so nothing is
  measured on an ungrown pool — and the layout it happens to give was then
  read off the binary rather than shopped for, which is the distinction that
  keeps the run from being confirmatory. **Run 10 is now two binaries rather
  than one**, differing only in the assembler shim, so each prediction below
  says which half it is read on and the last two exist only because there are
  two ([the run's plan](#making-a-major-benchmark-run) has why, and the build
  and check sequence). Against Run 9's offsets, both of the straddle
  hypothesis's arms move, in opposite directions:
  1. **The FastReshape three go straddling to resident** (mod 40, 44, 44 to
     mod 0, 36, 36) while their control stays resident (24 to 16). The
     hypothesis predicts 1.1552, 1.1795 and 1.1645 collapse toward 1.00. If
     they hold near 1.16, the hypothesis is dead and [the suspension of
     those axis figures](#the-mutable-ceiling-not-taken) is withdrawn —
     which is the outcome this page has the most reason to want detectable,
     the suspension being its own. **Sharpened by the pad probe**, which
     prices each offset instead of each side of the boundary: their present
     values are what a deep straddle over a resident control predicts, 1.18,
     and after the move all four copies sit resident, where the probe's own
     resident offsets span 0.904 to 0.956. So the collapse should be to
     between 1.00 and 1.05, and anything near 1.16 still kills it. Do not
     interpolate the 36 across the boundary — the penalty steps between 36
     and 37 rather than ramping. **Read on the unaligned half**, which is the
     half these offsets belong to; on the aligned half all four copies sit at
     0, so the same three ratios must read 1.00 outright, and that is the
     stronger form of the same test — a 1.16 surviving alignment would kill
     the hypothesis where a 1.05 could still be argued.
  2. **`mut-odo` goes resident to straddling** (29 to 53) while `build` stays
     straddling (53 to 45). The hypothesis predicts their 1.13 closes toward
     1.0, and **the pad probe makes that a point prediction, 0.998**: two deep
     straddles, whose penalties cancel, so the pair should land on 1.0 rather
     than merely approach it. The same penalties reproduce Run 9's own 1.13,
     at 1.144. If it holds or widens, the hypothesis is dead by the other
     route. **Read on both halves, and it is the weaker of the two arms
     precisely because they agree**: the unaligned half predicts 1.00 because
     45 and 53 happen to carry near-equal penalties, and the aligned half
     predicts 1.00 by construction, so the two halves cannot disagree here and
     the pair's own value is not what makes this run worth two binaries.
     Prediction 1 and prediction 4 are.
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
     any class paragraph. **Read on the aligned half alone.** Warming is heap
     state and not layout, `list` carries no layout term worth the name, so
     the anchors read the same on both halves and reading them twice would
     enter one effect as two findings. That last step is prediction 5's to
     establish, not this one's to assume: read 5 first, and if `list` does
     move between the halves then this prediction has no fixed anchor to be
     read against and waits. The nine populations' anchors are commensurable
     as printed, the fingerprint this run publishes being the aligned one and
     the eight class blocks aligned with it, so the reading-together above can
     be done off the page. That is a ruling and not a coincidence: had the
     unaligned fingerprint been the published one, exactly one of the nine
     would have crossed a basis, and the run's plan says why it is not.
  4. **The two halves differ, and for six arms by how much is registered
     here.** This is what the second binary is for. It was to have been a
     per-arm prediction over the whole roster, and **that is not available**:
     attributing a loop to an arm needs source information, every build that
     carries it relocates the code, and no bridge survives. `-g3` moves the
     fills from `[3, 53, 59, 45]` to `[8, 56, 4, 4]`; `-finfo-table-map`
     dissolves the groups altogether; matching the two builds by loop order
     fails at the first loop, and only 30 of 957 release loops have a body
     unique enough in both to match by bytes. The release binary keeps four
     `zdwgo7` symbols where the debug build has 47 and carries 98 `Main`
     symbols in all, none named for an arm, so its own symbol table cannot do
     it either — and `NOINLINE`, the obvious fix, is already on these arms:
     adding it a second time is a compile error and the symbols are absent
     regardless, GHC emitting the module's code under a handful of workers.
     Measured 2026-08-10, and recorded so the routes are not retried.

     What *did* work is the case-by-case form, and it is why six arms can be
     registered at all: take a loop's bytes from a `-g3` build, where
     `addr2line` names the `Main.hs` line and so the arm, then find the same
     bytes in the release binary. It succeeds when a loop is distinctive and
     fails when it is not — the 30-of-957 figure is the wholesale version of
     this, and a loop shared by two arms is ambiguous by construction, which
     for `build` and `mut-odo` is the very fact being measured. So attribution
     is available one arm at a time, at the price of a second build and a
     hand check, and is not available as a sweep.

     What is registrable is the six arms whose loops this page has already
     identified, read off `micro-unaligned` with `loop-offsets.py`: the fills
     sit at `[3, 53, 59, 45]` and `[16, 0, 36, 36]`, and all eight copies go
     to offset 0 in `micro-aligned`. So **`build` and `mut-odo` should each
     run about 0.85 of their unaligned selves** — from 45 and 53, both deep
     straddles at about 1.10, to the resident level near 0.93 — while their
     *ratio* stays at 1.00, which is what makes this a different measurement
     from prediction 2 rather than a restatement of it. The four
     `mut-odo-vecdims` arms are resident already, at 16, 0, 36 and 36, so they
     should move by a few percent at most, and the three ratios by less. An
     arm here that moves the wrong way, or the pair moving apart, is a
     finding.

     For the rest of the roster the prediction is aggregate and weaker, and
     says so: the moves falling in two groups rather than smeared, and the
     count that can move bounded by the short loops the shim rescues — 50
     of `micro-unaligned`'s 115 straddle where none of `micro-aligned`'s do,
     so 50
     loop heads' worth of penalty is removed and how many arms that touches
     is exactly what the run finds out. An arm reading *slower* aligned is
     not by itself a
     refutation: the padding is NOPs, and an arm that falls through into an
     aligned head executes them every time it does, so a small loss where no
     loop was straddling is the shim's own cost and not evidence against the
     penalty.
  5. **`list` does not move between the halves**, which is the pairing's
     control and the one result that would invalidate the rest. It is the
     insusceptible arm, 0.5% across four rebuilds, so alignment should leave
     it alone; if it moves, the baseline may have been carrying layout too,
     every published ratio on this page divided by a moving denominator, and
     that is a larger finding than anything the run was built to get. *May*,
     because `list`'s hot loop is **library code and not Main's**: `fbList` is
     one line over `VS.fromListN` and `toListT`, and no loop in a `-g3` build
     resolves to its source lines, so the shim cannot align it and only the
     phase-matching keeps it still. Its expected stillness therefore rests on
     measurement and not on mechanism — 0.5% across four rebuilds, which
     rerolled the libraries too — which is weaker ground than the six arms
     stand on and worth saying before the number is read.

     **Three things rest on this one, and no other prediction here carries
     more than itself** — which is why it is read first and why a failure is
     not one prediction lost but the run's arrangement to reconsider.
     Prediction 3 has no fixed anchor without it and says so. Run 10's mixed
     basis, its main table unaligned and its eight class blocks aligned, is
     tolerable only while the two halves' baselines agree. And the transition
     to Run 11 turns on Run 11's second column succeeding Run 10's unaligned
     table, which a moving denominator would put in doubt as well.
     The gate below already reads it on every shape and at the ordinary
     budget, so what the run adds is not coverage but company: `list` there
     shares a process with 33 other arms instead of four, and heap state and
     code position are exactly what this page has measured moving a figure
     when no strategy changed. That is the reading all three wait on.

  **The gate has been run and the three testable predictions hold**
  (2026-08-10, five benches over the 24 shapes, two passes per half in the
  order unaligned, aligned, aligned, unaligned, so both binaries carry the
  same mean position). Prediction 4: `build` reads **0.8836** of its
  unaligned self and `mut-odo` **0.8778**, so alignment is worth **12%** to
  each and the two agree to 0.7%, which is what one worker in two places
  should do. Prediction 5: `list` moves **0.3%**, so the baseline is still,
  the denominator holds, and the library reroll does not reach the one arm
  whose loop is library code — the phase-matching earning its keep.
  Prediction 2: the pair reads 0.9754 and 0.9805 unaligned, 0.9610 and 1.0082
  aligned, nowhere near the 1.13 or 0.86 earlier runs saw. Run 10 is worth
  its evening on this; what a gate of five benches and two passes cannot say
  is anything about the rest of the roster.

  **Two corrections come with it.** The registered 1.00 for prediction 2 was
  too strong: the pair sits at ~0.98 on both halves, where the pad probe's own
  both-resident binaries sat, so the arms' intrinsic ratio is **0.98 rather
  than the 0.9973** [the floor section][floor] carries — an estimate that
  assumed the two arms share one penalty curve, which their 5.9% disagreement
  at offset 13 already contradicted. It costs the arms nothing, since they
  share a worker but not a call path, `build` being `mut-odo` driven through
  `vBuildVS`. And **offset 0 is measured for the first time**: the probe's
  eight offsets were all congruent to 5 mod 8, so the 0.85 predicted here was
  an extrapolation from the resident mean, and the gain at 0 is 12% rather
  than the 15.6% that implied.

  **The gain is not a constant, which prediction 4's aggregate form should
  say.** Read shape by shape it runs 0.719 to 1.031 for `build` and 0.763 to
  1.033 for `mut-odo` — 28% at the best shape and a slight loss at the worst —
  against a per-shape noise floor this gate puts at 6.3%, that being the
  median disagreement between the two arms' own gains where identical code
  says they should agree. So the extremes are real and the middle is not
  resolvable on two passes: the 12% is a geomean over a structured
  distribution and not a factor every arm pays. What the structure is remains
  open, no shape ordering being obvious from five benches.

  **The correction term moves too, by 0.6%.** Both `sum-only` halves read
  0.9939 and 0.9938 aligned over unaligned, agreeing to a digit over a range
  of 0.990 to 0.998, so the forcing pass is itself slightly faster in the
  aligned build — its own loop presumably being among the fifty the shim
  rescues. It is subtracted from every figure, so it is not a term that
  cancels between the halves; at 0.6% of a fraction of each cell it cannot
  reach the 12%, but a later reading that needs the halves to share a
  correction should know they do not quite. Allocation, by contrast, is
  identical to 2.5e-6.

  **The gate read the aligned half as the noisier one and the full budget
  says it is not.** Over the gate's five benches its median CI% was 0.532
  against the unaligned half's 0.218, and its two passes disagreed more
  (`mut-odo` at 1.0224 against 0.9859), which left open whether alignment
  widens the per-cell interval structurally. Over Run 10's 816 cells a side
  the two halves are indistinguishable: median CI% **0.138 against 0.134**,
  median R² 0.99997 on both, and the aligned cell is the wider one 389 times
  of 816. So the widening was the gate's own sample size, and alignment
  removes a systematic term at no cost in precision. That closes the
  question the gate raised, which is what the full budget was wanted for.

  The first two were arms of one prediction, either of which could kill it,
  on arms already rostered and at no extra machine time; the third priced
  what the order change was for and carried its own control; the fourth is
  why the run was two binaries and the fifth is what made the fourth
  readable. The pad probe having answered the hypothesis first, the first two
  were replications carrying point predictions rather than the evidence —
  which is what that probe's window was spent to buy, and why the run's own
  weight sat on 4.
- **What costs `mut-odo-vecdims-add-out` its 16%, now that layout cannot?
  Asked and answered the same day: it is a per-run cost, and the Core reading
  had it right all along.** Run 10 read the arm 1.1266 with its loop resident
  and 1.1612 with every copy at offset 0, so the suspension [the
  ceiling][ceiling] carried is withdrawn and the cost is the arithmetic's.
  Regressing the per-shape penalty on the aligned half — arithmetic over the
  run's own cells, no machine time — puts it at r **−0.64** against log
  `sInner` and **−0.01** against log `m`, 1.423 where `sInner` is 3 and 0.997
  where it is 64. That is the signature of work done once per run and
  amortized over the run's elements, which is what the `scanr (*)` stride
  table is; the account is [in the ceiling section][ceiling]. What made this
  unanswerable before is that Run 9's copy of the shared loop straddled a
  cache line, adding a *per-element* term that flattened the very correlation
  the question turns on — so the pairing bought a mechanism here and not only
  a number. `add-both` tracks it at the same r and the corner's
  sub-additivity says the two axes largely pay for one thing.
- **What is the 3% that survives alignment on `build`/`mut-odo`?** With both
  copies of one worker at offset 0 the pair still reads 0.9685 on the main
  set, tying by the sign test (16 of 24) while the interval misses 1, and it
  runs 0.9148 to 1.0335 across the nine populations. The gate's correction
  already put these arms' intrinsic ratio at 0.98 rather than 1, on the pad
  probe's both-resident binaries, so Run 10 reproduces that at full budget
  rather than contradicting it.

  **Run 11 says the residual is not stable within itself, which is new.**
  Re-running that binary puts the pair at **0.9467** on the main set at 21
  wins of 24, sign p 0.00028, where Run 10 read 0.9685 at 16 of 24 and
  called it a tie — the point estimate moving two points and the sign test
  from tie to decisive with nothing changed. Across the nine populations it
  runs 0.9215 (`revsome`) to 1.0209 (`slice`), reproducing Run 10's 0.9148
  to 1.0335 as a span while the individual classes swap sides: `bcastmid`
  and `slice` put `build` behind, `reshape1` puts it ahead by 5% where Run
  10 had it behind by 3%. And these two arms are the ones the repetition
  finds least stable anywhere — `mut-odo` the only arm whose geomean leaves
  1.5%, `build` holding the two widest cells after the wild one ([the floor
  section][floor]). So the 3% is not one quantity waiting to be attributed:
  whatever it is fluctuates run to run on arms whose code, layout and slot
  are all pinned, and an experiment that prices it once has priced one draw.

  **The Core route is closed and is not to be re-proposed.** The obvious
  candidate is the call path — `build` being `mut-odo` driven through
  `vBuildVS` — and it has been dumped three times, from Run 6's source, Run
  7's, and Run 8's commit under this regime: there is no call path to find,
  `vBuildVS` surviving as no top-level binding in any of them, the two
  workers byte-identical once numbering is normalised, and the sources
  differing only by the `Strides` newtype's zero-cost cast ([the mutable
  ceiling][ceiling] keeps the dumps' verdict). A fourth dump would reproduce
  that and nothing else.

  **Narrowed the same day, to about a percent, and not attributed.** The next
  candidate after the call path is that the shim aligns loop heads and not
  procedures, so putting both inner loops at offset 0 leaves everything about
  where the two procedures sit — their cache sets, their neighbours, the
  outer odometer recursion's own alignment — different. [The floor
  section][floor] had the build that tests it, a `-fproc-alignment=64` one in
  which the two procedures are 64-aligned and internally identical so both
  copies land on the *same* offset, built and read and left untimed; timing
  it is a filtered A/B and it now reads 0.9893 against 0.9782 for the shim's
  build and 0.9585 for neither. **Sharing an offset is what makes the pair
  tie** — both same-offset builds do, the different-offset one does not — but
  the two ties cannot be ranked against each other on one pass, their
  intervals overlapping and their sign tests disagreeing about which is
  flatter. So procedure placement is still a candidate and not the answer,
  and the honest bound is that these two names differ by about a percent once
  their copies share an offset, part of which is roster context rather than
  either arm. The shim *and* the flag together would have ranked them; that
  build was made and timed on 2026-08-11 and **does not**, landing about a
  percent nearer level inside a 1.8 to 2.3% repeat spread, so procedure
  placement stays a candidate. A small filtered test beside it prices a
  shared straddling offset at 8 to 13% on both arms and the flag at 2 to 4%
  over the shim alone — indicative only, and a reason to pad any pair that
  adopts the flag ([the floor section][floor]).
- **What Run 11 was built to answer, registered before it ran — and what it
  answered.** Three questions, each with what would count as an answer, so
  that a run reporting "nothing moved" reports a result rather than a failure.
  All three are answered; the third only in part.
  1. **The repetition, owed since Run 9: answered, and the bound is a quarter
     of what it was.** With the basis half Run 10's aligned binary byte for
     byte, `list`'s per-shape scatter is **0.958 to 1.043** against a 0.25%
     geomean, where Run 10 widened it to 0.902–1.181 against 0.4%. Over the
     roster, 495 of 762 cells are within 1% and every arm's geomean is within
     1.5% bar `mut-odo` at 1.0327. So the drift this page has been quoting
     was mostly the layout it could not hold still, and what a figure may do
     between runs for no reason at all is a few percent per cell.
  2. **Max-skip across the roster: answered, and the vecdims arms split two
     and two.** `build` and `mut-odo` are unmoved as predicted (0.9896 and
     1.0221, both halves putting their executed copies at 0).
     `mut-odo-vecdims` (1.0074) and `-add-both` (1.0333) keep the whole NOP
     cost Run 10 measured for them (1.0069, 1.0326); `-add-in` (1.0036) and
     `-add-both-down` (1.0029) shed most of theirs (1.0143, 1.0443). That is
     the two-and-two the pair note predicted from the offsets, read as arms
     rather than as a family, and it is what a full-budget run could resolve
     where a filtered pass could not. Across the rest of the roster nothing
     reads below 0.99 but `build`, and `bq-mut` reads 1.0588 with the maxskip
     half ahead on 23 shapes of 24: **max-skip is the cheaper build nearly
     everywhere, at a third of the padding.**
  3. **Whether a resident offset costs anything: narrowed, not settled.** The
     two vecdims copies max-skip left at their own offsets (24 and 8) run
     1.0074 and 1.0333 against the same code at 0, so what the fully padded
     build charges for aligning them exceeds what their offset costs — the
     direction the isolated reproducer's ~2% predicted, and the same sign on
     both. What it does not give is the offset's own price, the padding and
     the offset moving together in every arm here. Separating them needs a
     third build that moves one head without padding before it, which is
     `-fproc-alignment=64`'s territory and is [the queue][open]'s.

  **And what it must not do was add an arm** — the third `-nosum` one the
  queue calls due — since the repetition needed membership pinned as well as
  layout. It did not; that arm is Run 12's, and the ordering is in the queue
  entry too.
- **The wild cell is back, on the same family and at the other end of the
  roster.** Run 11's aligned half reads `lenet-L1-28-c1-k5/bq-expand` at
  1.355 of what the same binary read in Run 10, with both of that arm's A/A
  twins clean in the same process, both time-neighbours within 1.2%, CI%
  0.06 over 125 samples, and `list` on the shape unmoved — the evidence
  against an intrusion is at [the head of the run
  chapter](#about-the-last-run-run-11). Run 8 and Run 9 saw 44% and 41.4% of
  this on the same arm at its **distant twin's** slot, and Run 10's roster fix
  — `sum-only-early` above `list`, so nothing is measured on an ungrown pool
  — removed it there and was confirmed at full budget. Here the arm's **own**
  slot carries it, which the fix does not reach and does not claim to. So
  susceptibility is a standing property of the expansion family and the pool
  account explains one of its two sightings.

  **The samples have since been read, and they say the cell is a shift and
  not a defect** (2026-08-12, arithmetic over the run artifacts, no machine
  time; a refit of `reportMeasured` reproducing criterion's own slope to
  2e-16 first, which is what says the sample layout was read right). Its
  per-iteration residual dispersion is **2.57 µs against its own twins'
  2.76 and 0.70** in the same process, and against 2.20 to 2.79 for the same
  three arms in the maxskip half — so it is not the noisy one. Every arm
  there shows the same small warm-up in its first third, gone by its last,
  and the residual correlates with allocation and GC count at +0.5 to +0.8
  on twins and arm alike, so neither is the cell's. Allocation per iteration
  is the same 340193–340195 for all six. What is left is a clean 14.4 µs on
  the slope of one arm at one slot, with everything a sample can report
  looking ordinary — which is what Run 8 and Run 9 found at their cell too.

  So the one instrument left is **a repeat of the aligned main set**: a
  filtered run cannot answer it, putting every arm at the cold end by
  construction ([the floor section][floor]), so it is another 70-minute
  process on a quiet machine — and it is the only thing that says whether
  the cell belongs to the *run* or to the *shape and slot*.
- **Why is `mut-odo`'s interval wide on `micro-aligned`?** Its CI% reads 1.06
  there against 0.34 unaligned, and the raw samples have since been read
  (2026-08-11, arithmetic over the run and gate artifacts, no machine time).
  **It reproduces and it belongs to that binary**: 1.06, 1.09 and 1.15 in
  three independent processes on it — Run 10's main set and both gate passes
  — against 0.72 and 0.19 on `micro-maxskip`. **And it is one arm, not the
  four this entry used to name.** `offtab`'s interval is 0.74 in both halves
  and `list`'s *narrows*, 0.67 to 0.59, while their `noise` reads 1.78 to
  3.03 and 2.24 to 3.59: `noise` is a row's CI against the median CI on its
  shape, so the aligned half being quieter overall — median CI% over rows
  0.180 to 0.160, the same direction as its halved A/A floor — lifts every
  row's figure without touching its cell. `build` moves 0.30 to 0.39, a
  tenth of what its `noise` suggests. So the code-twin does not follow and
  `list` never joined, which was the whole of what made this puzzling.

  Three accounts are closed at sample level, the refit reproducing
  criterion's slope to 1e-15 first: the residual correlates with `measNumGcs`
  and `measGcWallSeconds` at ±0.00 in every process, so it is not the block
  pool; with sample index at ±0.03, so it is not drift the slope missed; and
  allocation per iteration is constant. Nor is it shape-localised, two passes
  of one binary sharing no widest shape. What is left is dispersion about the
  line that no recorded covariate explains, on one arm, on one binary — and
  thinner than the three readings suggest, per-cell dispersion swinging
  several-fold between passes and the comparison binary's own median moving
  3.7× between its two.

  **Run 11 reproduced it a fourth time and turned it into a different
  question.** The same arm at the same slot in the same binary reads CI%
  **0.82**, against 0.31 on `micro-maxskip` — so the split between the
  binaries survives, at three quarters of Run 10's separation. What is new is
  that `mut-odo` is also **the arm that drifts most across the repetition**,
  1.0327 where every other arm bar its own code twin is inside 1.5%, with
  cells at 1.1577 and 1.1467; `build` is second at 1.0095 with a 1.2471 cell.
  Two arms sharing one worker, at offset 0 in both runs, moving together and
  moving more than the roster: the wide interval and the wide drift are one
  arm's, and placement can no longer be either's account. What would separate
  a dispersion belonging to the *worker* from one belonging to the *slot* is
  a run with the two arms' roster positions exchanged, which an aligned build
  now makes a membership-free edit.

  **And at sample level the pair is one thing again, which the CI% column
  hides** (2026-08-12, arithmetic over Run 11's two main sets, no machine
  time). Taking each cell's residual about its own fitted line, per
  iteration, as a fraction of that cell's slope, and medianing over shapes:
  `mut-odo` scatters **21.9%** on the aligned half and `build` **32.7%**,
  against `mut-odo-vecdims`'s 3.1% and `list`'s 3.2% — an order of magnitude,
  and `build` the worse of the two where its *interval* is much the narrower
  (CI% 0.44 against 0.82). So the entry's earlier reading, that this is one
  arm and its code twin does not follow, was an artefact of reading CI%: the
  twin does follow, and by more. Both roughly halve on the max-skip half,
  11.1% and 22.8%, where `list` and the vecdims arms barely move. That is
  the same pair, behaving together, on the same two binaries as [the 3% that
  survives alignment][open] — recorded as a measurement, not a mechanism,
  since nothing here says what the scatter is.
- **Why did `list` move 18% on `stretch-tall-Mx2` between two runs that did
  not touch it? Answered: because those two runs did not hold the layout
  still.** Run 11 inherited shapes, roster, regime and layout and reads that
  cell at **1.0063**, inside the 0.958–1.043 band its 23 neighbours occupy,
  so the 18% belonged to the roster-order change between Runs 9 and 10 and
  not to run-to-run drift. The cheap half of the diagnosis had already shown
  the cell was stable inside its own run — 16 samples and CI% 0.822
  unaligned, 15 and 1.612 aligned, R² above 0.9994 on both, the two halves
  agreeing to 0.25% — which is what left drift as the only reading available
  then. What the repetition adds is that drift will not carry 18%, so the
  bound this page quotes for it comes down accordingly.
- **`scaled`'s A/A floor is back at 5.36%, at the slot that carried it in Run
  7 and Run 8 and not in Run 9 — and it is the base arm that is slow, not the
  twins.** Both `mut-odo-vecdims` pairs read below 1, 0.9464 and 0.9574, both
  worst on `scaled-super-r3`, while the other four pairs in that process sit
  within 0.25%. **Two thirds of it is arithmetic and was mine to divide out
  before calling it a disturbance.** The raw slopes disagree by 2.13%; the
  forcing term is 59.8% of this bench, the largest share in the run; and
  1/(1-f) turns the first into a predicted 5.29% against the 5.36% read. So
  the arm's cells are 2% apart, not the 11% the published pair suggests. The
  raw sample lists say nothing further is wrong: R2 is 0.99995 or better on
  all four arms and there is no ramp the slope has not already handled.
  What survives is a 2.13% raw disagreement at one slot on one shape, against
  0.17% raw or less for the four other pairs in the same process — smaller
  than it looked and still this slot's. It also inverts Run 9's wild cell,
  where the *twin* was slow and roster warmth was the account: the distant
  twin here is the earliest of the three and is the clean one, so that story
  does not transfer. **Do not reach for a filtered
  re-run of the six controls**: filtering collapses the spans the crossed
  design needs, which [the floor section][floor] records as making a span
  unmeasurable. What can be asked is Run 11 reading this population with
  layout pinned.

  **It has, and the answer is that the slot is real and its size is not.**
  Run 11 reads this class's floor at **3.27%** — still the run's worst, still
  the `mut-odo-vecdims` slot, still worst on `scaled-super-r3`, so four runs
  of five have found a disturbance at one slot on one shape and a pinned
  layout does not remove it. What did not survive is everything about its
  magnitude: the pair that carries it swapped, the *distant* one reading
  1.0327 where the adjacent one is clean at 1.0020, and the sign inverted,
  both having read *below* 1 in Run 10. The arithmetic half reproduced
  exactly — raw 1.25% at `f` 0.609, so 1/(1-f) predicts 1.0320 against the
  1.0327 published — which is the account above holding while the quantity
  it explains moves by two points between two runs of one binary. So quote
  this slot as a hazard of the class and never as a figure, and treat a
  margin under about 3% here as unmeasured.
- **What does the roster owe the next run?** The exact repetition is **taken**
  and is not owed again for its own sake: Run 11 inherited shapes, roster,
  order, regime and binary, and what it bought is at [the head of the run
  chapter](#about-the-last-run-run-11) — a drift band a quarter of the one
  this page had been quoting, and every claim reproducing on it. What the
  roster owes is still the third `-nosum` arm the queue holds, deferred out
  of Run 11 so that its membership stayed pinned and now out of Run 12 so
  that it does not arrive in the same run as a change of shim: **it is Run
  13's**, and cheap on any build that pins a loop's offset against
  membership, which is the property Run 12's basis choice decides. A return
  to -O1 — the regime `Data/Array/Internal.hs` actually compiles under,
  unvisited since Run 7 — stays open behind it, and is the more expensive of
  the two, an aligned -O1 build being a fourth kind of column.
  `--check-doc` enforces the yardstick's shape in the one direction it safely
  can: a run named aligned must also be named unaligned, so dropping Run 10's
  unaligned column fails the check. Dropping an *aligned* one cannot be
  checked, an unpaired run being what every column before Run 10 is, and
  stays the reading's job.

  **Run 11 had no unaligned half, and the check was left alone rather than
  widened — the reading is that this was right.** Its two columns are `Run 11
  (SpecConstr, aligned)` and `Run 11 (SpecConstr, max-skip)`, and
  `--check-doc` passes on them, the rule asking that a paired run publish a
  column per half and not one. Widening it was the alternative and is
  refused: the check would then have to know which half names count as a
  counterpart, which is a list that grows with every pair and is wrong the
  first time one is invented. Keep a basis column named `aligned`; name the
  other half for its shim.

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
  with every run so far, which is why none was taken for eight runs. Run 7
  confirmed the
  drift, Run 8 mostly did not, and Run 9 shows why both readings were of the
  wrong quantity ([the floor section][floor]): the effect is not a per-slot
  gradient to fit but a step, worth nothing on most arms and 35–40% on one
  family at one shape. **So a slot correction is now refuted rather than
  merely unmeasured** — a linear fit in slot number cannot express a step
  that depends on the arm, and fitting one would smear a real 40% across
  thirty rows that do not have it. What the drift needed instead was the
  warm-up bench, the only one of the three fixes Run 9 left standing, and
  **Run 10 takes it**: `sum-only-early` above `list`, so the baseline is
  measured on a grown pool like everything else, at the cost of re-basing
  every published ratio — which is what the entry above says none of these
  fixes could avoid. What it does not address is the placement gap the
  `build`/`mut-odo` pair shows, a separate and larger target that no
  reordering reaches.
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
the same shape. These are Run 11 (SpecConstr)'s own figures, from its
**aligned** half as the fingerprint is, all of them net
of the forcing pass like the rest of the page. A `lemire-out` column stood
between `bq-expand-b` and `mut-odo` until the precondition ruling took
`bq-expand-lemire-out` out of the timed roster, a column a later run could
only have left standing under its own name. What that arm's per-shape
behaviour showed is in
[the Lemire section][lemire], which is where its decision lives anyway:

| shape      | bq-expand | bq-expand-b | mut-odo | vecdims |
|------------|----------:|------------:|--------:|--------:|
| inner1     |     0.077 |       0.071 |   0.284 |   0.099 |
| rank12     |     0.227 |       0.228 |   0.345 |   0.102 |
| wide-2xM   |     0.087 |       0.081 |   0.176 |   0.066 |
| coprime-r7 |     0.105 |       0.105 |   0.061 |   0.033 |
| pow2stride |     0.066 |       0.066 |   0.068 |   0.068 |
| primes     |     0.101 |       0.101 |   0.030 |   0.029 |
| inner256   |     0.069 |       0.069 |   0.016 |   0.015 |
| tall-Mx2   |     0.071 |       0.071 |   0.018 |   0.018 |

Ordered by `sInner`, 1 at the top and half the length at the bottom, which is
the axis the orderings turn on; the fuller per-shape record is in
[What Run 12 compares against](#what-run-12-compares-against).

- **Which strategy wins is decided by the innermost extent (the size of the
  innermost dimension, `sInner` below) — not by the rank, not by the element
  count.** `stretch-inner1` is where the expansion family does best against
  the odometer fills: `bq-expand` (0.077) and `bq-expand-b` (0.071) beat
  `mut-odo` (0.284) and `build` (0.250) three- to fourfold, which they do on
  no other shape here
  — `stretch-pow2stride` excepted, where the two families converge outright
  (0.066–0.068 across expansion and odometer alike).
  Its innermost extent is 1, so each
  base offset covers a single element: the odometer that `mut-odo`/`build`
  step has nothing to amortize over, while the expansion build has no
  per-element odometer to begin with. At the other end `stretch-tall-Mx2` has
  an innermost extent of half its length and the ordering inverts completely —
  `mut-odo` 0.018 against `bq-expand` 0.071, with every mutable strategy
  ahead of every pure one. The geomean reports that second case and averages
  the first away, which is why this table is here.

  **What Run 6 refutes** is the stronger form this bullet used to carry: that
  `stretch-inner1` is *the only shape where the pure expansion strategies beat
  every mutable one*, with the four `bq-expand` variants taking the top four
  slots. They no longer do, and this roster says so more plainly than
  Run 6's: `mut-flat-gm` and
  `bq-mut-runs-gm-mulback` take that shape tied at 0.028, both ahead of every
  expansion variant, while `mut-odo-vecdims` sits at 0.099 —
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
  the worst-measured shape of the set by median and mean CI% (0.938 and
  0.958 on Run 11, both the highest here, as they were on Runs 9 and 10). It
  stays in the column, its influence capped.
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
That is `mut-odo` and `mut-odo-vecdims` (0.048), the latter 2.13× over
`bq-expand` on Run 11 (SpecConstr) and the fastest strategy
in the table. All allocate essentially just the result
vector. `offtab` (0.125) does not go that far — its output is an ordinary
`vGenerate` and only its `l`-sized `Int` offset table is filled mutably, so it
needs no class method, just a mutable scratch — and it sits **24% behind
`mut-odo`** for it, at three wins of 24 with sign p 0.00028, where Run 10's
aligned half read 26% and its unaligned half tied them: alignment decided
this comparison and the repetition holds it. On these numbers it is
no longer the cheap way to most of the gain, as it was when Failed Run 6 had
the two tied, and the gap it must close to become one again is 2.6× against
`mut-odo-vecdims` (0.3864 paired, 24 shapes of 24).

**Plain `mut-odo` has stopped making the case, and it is not the regime's
doing.** Run 8 read the pair 1.08× *against* `mut-odo` and blamed the flag,
which sets that arm back hardest but one; Run 9, same flag, has the geomean
back on `mut-odo`'s side at 0.947, Run 10 at 0.9671 aligned and Run 11 at
**0.9842** — and it is still not a win, at nine
shapes of 24 with sign p 0.31 and an interval covering 1. The geomean and the
win count
point opposite ways because the pair's per-shape range is enormous, 0.234 on
`stretch-inner256` to 3.687 on `stretch-inner1`, so a handful of large shapes
carry the geomean while most shapes go the other way; read the sign test, and
the answer is a tie in all four runs. What removed `mut-odo` from the
argument
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

**What the pair has become is a second instrument, and it is read where the
other instruments are.** Two top-level names with identical Core are a true
ratio of exactly 1, which is what the A/A controls are built to supply, and
this pair disagrees by far more than they do — so it prices what placement
does to two *separately compiled* arms, where the twins price only what it
does to two calls of one. That reading, its figures in every run and
population, and the per-loop account underneath it are [in the floor
section][floor] and are deliberately not repeated here: what this section
needs from the pair is only that its disagreement is placement rather than
the abstraction, which is what leaves the identity above licensing `vBuild`.
A pure-typed alternative (a
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
10 (SpecConstr) prices the class-method tier at 2.11× over `bq-expand`
(0.4745 paired). Against that, the best pure strategy reaches 0.090, so the
gap the class method would buy is **1.85×**, not 2.11× — which is the figure
the ruling
turns on. It has now read 1.80× at -O1, 1.68× on Run 8, 1.87× on Run 9,
1.85× on Run 10 with its aligned half giving 1.84×, and **1.84×** here — the
same cell and the same 23 wins of 24 as Run 10's aligned half, to four
digits. So the spread is a tenth either side of 1.8 and neither the pairing
nor a repetition moves it. Read it as *approaching 2× and volatile at the
tenth* between runs that differ, and do not reopen or close the ruling on a
movement of that size — Run 10 showed the volatility is not the layout's, and
Run 11 shows it is not the run's either, which leaves the roster and the
regime as what moved it.

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

**Run 10 priced them on a build where the loop's placement cannot be the
answer** (the paragraph after next is what makes that true) **and Run 11
reproduced every one of them**: against `mut-odo-vecdims`, `add-out`
**1.1588** where Run 10 read 1.1612, `add-both` **1.1173** against 1.1184,
`add-both-down` **1.0512** against 1.0527 at the same 7 wins of 24, and
`add-in` **0.9934** (21 of 24, sign p 0.00028) against 1.0009 at 13 of 24 —
three of the four inside a quarter of a percent, and the fourth the sign-test
flip [the Results findings](#results) read as the instrument rather than the
arm. The corner stays sharply sub-additive — 11.7% where the two solo losses
sum to 15.2% — and the count-down form still recovers most of the corner's
loss, 0.9408 against it on 22 shapes of 24 where Run 10 had 0.9412 on 24 of
24.

**Run 9 had priced them differently, and the pre-run reading was right about
the sign and wrong about the size.** That reading — one shape, Run 8's
regime — put all
four behind their control by +4% to +12%, the corner sub-additive and the
count-down form recovering two thirds of its loss. Over 24 shapes Run 9 read
`add-in` **1.1552** (0 wins of 24), `add-out` **1.1795** (1 of 24),
`add-both` **1.1645** (1 of 24), each against `mut-odo-vecdims` and each with
sign p at or below 3e-06. So all three solo-or-corner arms sat behind their
control by more than the one-shape probe suggested, and near-unanimously
across shapes — which the write-up first read as the precedent's arithmetic
losing on both axes, and which the Core reading two paragraphs down
withdraws: near-unanimity across shapes is what the identical-code pair shows
too, so it separates nothing. The corner
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
as a further argument — a per-*run* change. `add-out` and `add-both` carry
real extra code of the same kind — a `scanr (*)` over
the shape, built into a byte array once per call and read once per run —
which adds nothing to the per-element loop.

**Run 9 could not see those as per-run changes and Run 10 can, which is the
second thing the pairing bought.** On Run 9 the three penalties were flat in
`sInner` (`add-in` r +0.21) and largest on `stretch-tall-Mx2`, shape [2,
900000], where the odometer descends twice per call — 1.3152, 1.2930 and
1.2901 there, which two multiplies and a two-element table cannot cost. That
was the argument for suspending them, and it was right to suspect the
figures: they were layout. Read on Run 10's aligned half, where every copy of
the shared loop sits at offset 0, the same regression comes out the shape a
per-run cost has to have. **`add-out`'s penalty scales as 1/`sInner`**, r
**−0.64** against log `sInner` and **−0.01** against log `m`: 1.423 on
`cnn-L1-6x6-c1` and 1.340 on `cnn-slice-c32`, both `sInner` 3, against 1.009
at `sInner` 256 and 0.997 at `sInner` 64. A cost paid once per run and
amortized over the run's elements is exactly a penalty that falls with the
run's length and ignores the number of runs, and `stretch-tall-Mx2` — the
shape whose 1.29 was the objection — now reads level. `add-both` tracks it at
r −0.64, and `add-in`, which is free, is flat at −0.16 over a 0.955–1.078
range. So the code identified in 2026-08-09's Core reading is the code that
pays, the arithmetic is per-run as that reading said, and what stood between
the two was the address of a loop neither arm's difference lives in.

**The two solo axis figures were suspended on that reading, and Run 10
resolves the suspension in opposite directions.** The suspension said: what
costs 16% on them is not the arithmetic they port, the loop doing the
per-element work being the same code in all four arms, but the layout span,
their executed copy of that loop straddling a cache line where their
control's does not ([the floor section][floor]). Run 10 put every copy of
that loop inside a line in one binary and at offset 0 in another, and read
the three arms in both:

- **`add-in` is acquitted and the suspension becomes a withdrawal.** It reads
  0.9937 and 1.0009 against its control, where Run 9 read 1.1552. Stepping
  the input offset additively in place of the loop's one multiply costs
  **nothing**, and the +15.5% recorded for it was the address of a loop the
  two arms share.
- **`add-out` is convicted, and the corner with it.** It reads 1.1266
  resident and **1.1612** aligned, `add-both` 1.0906 and 1.1184, on four
  placements between them and no straddle among any of them. So the +18.0%
  is the arithmetic's after all: carrying the output position through a
  precomputed stride table, in place of the threaded return, costs about 16%,
  and the corner's sub-additivity is a property of the two axes and not of
  where they landed.

That is the outcome the registration named as killing the straddle
hypothesis for the arm that shows it, and it kills it for two of three. What
survives is sharper than what it replaces: of the three axes FastReshape's
loop arithmetic ports, one is free, one costs 16%, and the count-down form
that ties its control is the third.

**The pad probe had upheld the suspension**, and this is where the two
instruments part. Stepping a shared loop through all eight offsets prices a
deep straddle at 1.19 against a resident copy, and these three sat at mod 40,
44 and 44 against a control at 24 — a predicted 1.18 against the 1.155 to
1.180 they read, on a family and a binary the probe never touched ([the floor
section][floor]). The agreement was real and was a coincidence for two of the
three arms: the correction the probe supplies is a *screen*, licensed only
where the loop is the same code, and here it is the same code while the arms
differ elsewhere as well. Read that as the screen's stated limit meeting a
case it could not see rather than as the probe being wrong — its own
binaries, which differ in placement and in nothing else, still reproduce to a
median 1.0%.

**What that does to the precedent's weight.** FastReshape's arithmetic,
ported one axis at a time onto this page's fastest arm, buys nothing here and
one axis of it now demonstrably *costs*: the count-down form ties the
control, the additive input offset is free, and the precomputed output stride
table is 16% behind on a layout that cannot be blamed. So the in-tree
precedent argues for the *shape* of a mutable fill and
not for its arithmetic, and the ruling above is unmoved: what a new class
method would buy is still `mut-odo-vecdims`, at [the 1.85×](#results) the
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
[What is open](#what-is-open), the chapter at the front, which is where
everything that goes stale as soon as a run reports is now collected.

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
[The noise floor](#what-moves-a-figure-when-no-strategy-changed) and
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
and the arms written since bring it back to 23** — the four unconditional
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
  **Three runs now say the cost was near zero**, which the ruling did not
  need but is worth recording: its unconditional counterpart
  `bq-odo-gm-mulback` has come in at 0.090 on each of Runs 9, 10 and 11,
  within a thousandth of the arm it replaces, and ties
  `bq-scan-rem-gm-mulback` at the head of the pure tier (0.9987 paired, 17 of
  24). Dropping the bound bought back the restriction and cost about a point.
  The column went with them, having nothing left to say once every surviving
  row's cell was empty; each dropped arm's bound is now at its roster entry,
  spelled as that arm's own assert spells it.
- **A strategy allocating 2.4x the result or more is not measured**, at
  `-fspec-constr`, which is the regime the cut was taken in and Run 10's.
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
  list](#the-claims-run-12-should-test) has been re-aimed onto them.

**The crossed A/A design survives the cut, at half to two thirds the span.**
Its three distant twins are placed early and their bases late, and 23 of the
benches between them have gone: the spans fell to 25, 22 and 4 intervening
benches, from 38, 31 and 8, and Run 10's roster order takes one more off each
(24, 21 and 3). That is still nothing like the
twelve-arm probe where [spans of 28 and 0 read alike][floor], so the design
keeps doing what it was built for; what it does not keep is comparability
with an older span column, a pair being a different distance apart under
the same name in each of the last three runs.

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
same digits, which is the property the bar was chosen for. Three runs have
now said whether they are fast: on Run 11 `mut-flat-gm` reads 0.081,
`bq-odo-gm-mulback` 0.090, `bq-expand-gm-mulback` 0.094 and
`offtab-scan-rem` 0.119, so three of the four land ahead of the shipped arm
and the fourth behind it, as in each run before.

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
default budget — the main set and, by default, **every stride-class population
with it**: one process for the main set, or two where the run is paired, and
one per class, in the order of the sequence below. Asking for a major run asks
for all of them; leaving a population out is an explicit exception to be
stated, not a choice this page leaves open. The whole is analysed and written
into this file. What follows is the procedure, and it is written to outlive
any one run.

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

**The run's two variables come first**, because everything below uses them
and a shell that has not set them will silently do the wrong thing: an empty
`$REGIME` is a -O1 build that every gate here passes.

    R=run10                              # names every artifact; no default
    REGIME=-fspec-constr                 # every run since Run 8; empty for -O1

**And in a session they will not survive to the next command.** Each tool
call gets a fresh shell, so a `cd` and an assignment made in one are gone by
the next, and the commands below are spread over a dozen of them — which is
to say the shell this warning is about is the ordinary one here, not a
careless one. Inline the two literals into every command, or re-set them at
the head of each: `cd ~/r/orthotope/micro-regime3 && R=run10
REGIME=-fspec-constr && …`. The two do not fail alike, which is the reason to
spell this out rather than trust care. `./run-major.sh $R` with `$R` empty is
loud, the driver refusing without a name. `./make-pair.py --regime="$REGIME"`
with `$REGIME` empty is not: it degrades to a plain -O1 build, which is
exactly the silent wrong thing the paragraph above describes and nothing
downstream detects.

`$REGIME` is the bare GHC flag and not a `--ghc-options=` spelling of it,
because `make-pair.py` composes it with a `-pgma` of its own and would wrap
it twice. The one site that hands it to `cabal` wraps it there instead. Its
value begins with a dash, so every option taking it wants `--opt="$REGIME"`
and not `--opt "$REGIME"`: argparse reads a dash-leading word as the next
option and exits 2 saying the argument expected one, which is loud but reads
as a broken script rather than as a quoting rule.

**Everything below that writes runs unsandboxed**, which is every step that
builds, benchmarks or leaves a file: `make-pair.py` either way round, the
smoke block, `run-gate.sh`, `run-major.sh`. The read-only ones — both
`check`s, `diag`, `--lint`, `--check-doc`, `loop-offsets.py`, `--list`, a
`grep` of the note — are fine sandboxed and are worth having cheap, so this
is not a blanket instruction to drop the sandbox for the afternoon. A session
starts in `~/r/horde-ad`, so its sandbox permits writes
there and to its own temp directory and nowhere else; this directory is
outside it, and `run-major.sh` moves here before doing anything. Sandboxed,
every `--json` and every `> $out.log` is refused — and the two refusals do
not look alike. A redirection on a simple command is checked before exec, so
the benchmark never starts at all, while `log`'s `tee` is a pipeline whose
`echo` still prints: you get the sequence's start lines on the console, no
wall-clock file, no JSON and no run. That reads as a run in progress, which
is how two copies once ended up on this machine at the same time. Confirm a
launch by an unsandboxed process list, never by the launching shell.

**So never write `$TMPDIR` in this directory; spell the scratch path in
full.** That variable is set only under the sandbox, so the same idiom that
works in a read-only check writes to `/` the moment you add the flag that
makes a command able to write at all — silently, since the write succeeds.
The fact is in the session-level notes and was resident when this bit: what
defeats it is that the rule is conditional on a property of the *call*, which
changes call to call here, while `$TMPDIR/x` is a habit that does not. A
directory where half the commands must be unsandboxed is one where the
conditional should not exist, which is why this is a rule about the place
rather than a caution about the variable.

**Then build what will actually be timed — but first, is there a pair here
already?** That is the fork, and it comes before the build command rather
than after it, because `make-pair.py` overwrites both halves in place: the
offsets the predictions are registered against are the present pair's, and a
rebuild coming out even slightly different would retire them in silence.
Where the binaries and the note recording what they were built from are
already there, confirm them instead of rebuilding:

    ./make-pair.py --verify-only         # every gate again; builds nothing,
                                         # but DOES append to the pair note

which re-runs `check` on both halves, compares the two listings and reads the
fills off the binaries, and appends what it found to the note rather than
overwriting it. Two gates it cannot run, both needing the plain build that a
rebuild would have made: PAD_BYTES is not re-derived and the moved-fill
comparison has nothing to compare against. It says so, in the note and in the
verdict, so a re-verification does not read as a fresh build's clean sheet.

The fork's three questions are answerable in three commands, none of which
the page should make you invent, and each names the pair's own two halves —
`micro-maxskip` and `micro-aligned` today. Is there a pair — `ls
micro-maxskip micro-aligned micro-pair.txt`. Is it the pair the note
describes — `md5sum micro-maxskip micro-aligned` against the note's two
`md5` lines. Has the source moved under it — `git log -1 --format=%h --
Main.hs` against the commit the note records — the *tree* commit where it
records two, the binaries' own being the other. **Expect it to differ, and
read the diff before believing it**: step 8 below sends the
write-up into `Main.hs`'s comments and forbids rebuilding for it, so a
comment-only move is the normal state after every run, and `git diff <note's
commit> HEAD -- Main.hs` is what tells it from a real one. The regime is
the fourth and is not answerable this
way, the JSON recording no compiler flag; the `diag` step below is what
answers it.

Only where there is no pair, or where `Main.hs` or the regime has moved since
the note was written, is the build the thing to run — and the regime goes to
it rather than being assumed, since it has a default of its own:

    ./make-pair.py --regime="$REGIME"    # four builds, ~5 min, and it verifies
    ./loop-offsets.py micro-unaligned micro-aligned

**But only for an unaligned/aligned pair, which is the only kind it builds.**
A pair of two shims — Run 11's — is built by the recipe its own note
carries, which is why that note is written by hand and says so, and records
the offsets both halves came out with. The confirm path above wants
the same care: `--verify-only` looks at `<prefix>-unaligned` and
`<prefix>-aligned` unless `--basis`/`--other` tell it otherwise, so beside a
hand-built pair it gates two binaries that are not the ones you mean. It
refuses rather than overwrite a note recording a gate, but the refusal is the
backstop, not the instruction:

    ./make-pair.py --verify-only --basis aligned --other maxskip

There is no single-binary form of a major run any more, the pairing being
permanent: `run-major.sh` and `run-gate.sh` both refuse to start without both
halves, so a lone binary has no driver. What `cabal build micro
${REGIME:+--ghc-options=$REGIME}` is still for is a probe — a filtered handful
of benches answering one question — and those are run with `cabal run micro
${REGIME:+--ghc-options=$REGIME} --`, never through the sequence below.

**Before spending the hours**, the cheap checks — the first two against the
binaries that will be timed, not a third built beside them, and the last two
against `Main.hs` and this file, which open no binary at all:

    ./micro-maxskip check        # every strategy agrees, every shape regime 3
    ./micro-aligned check        # and the other half: both were shim-rewritten
    ./micro-aligned --list 2>/dev/null | wc -l   # 2>/dev/null is not optional:
                                 #   the provenance line goes to stderr and
                                 #   interleaves inside a bench name without it
    ./read-run.py --lint         # the roster and the shape annotations
    ./read-run.py --check-doc    # anchors, coverage, widths, stale figures

**The exit code is the verdict; the `note:` lines are not.** A clean
`--check-doc` here still prints three of them, each heading an indented list
running to dozens of entries — every superseded figure, every superlative
and every absolute time the page quotes, listed for adjudication during the
write-up and not before it. `--lint` is the same, noting the rostered arms it
knows are deliberately untimed. Both exit 0 when they pass, and a `FAIL:`
line is the only thing that should stop you at this point.

Both halves, and on an unaligned/aligned pair the aligned one is the half
that needs it, being the only one whose own code the shim rewrote —
`pad-as.py` only appends dead bytes after the other half's, where
`align-as.py` moves labels about. On a pair whose halves are two shims, as
Run 11's is, both can be mispadded and both need it. `make-pair.py` now
runs both itself and refuses on either, and
holds them to each other besides — a sound pair makes the two
logs byte-identical, agreement on every shape being a property of the
strategies and not of where their loops landed. It checked the unaligned half
alone until 2026-08-10, which is to say its gate was pointed at the binary
that could not fail; the two lines above are then a re-check rather than the
only check, and cost seconds.

**Then confirm the regime is the one intended**, which nothing later can:

    ./micro-aligned diag

and read one row of it — `baseOffsetsScan` against `baseOffsetsMut` on
`vgg-14-c512`, which is a `diag` label rather than a shape and so will not be
found in the shape set. They are equal under SpecConstr and ten times apart
at plain -O1, a separation no eye misreads, and both ends of it are measured
(2026-08-08), the flag being the only thing that moves them. Seconds either
way — on the build path, the seconds after a rebuild the flag forces anyway;
on the confirm path, its own, and the only ones spent there that matter,
since with no build to carry the regime this is the only
check
standing between a mistyped regime and a run that refutes the design it was
built to test.

**A paired run adds a second binary, and both are built and checked before
either is timed.** Alignment is not a regime flag: it arrives on `-pgma`,
GHC notices neither that nor `-fproc-alignment`, and a rebuild between the
two halves would put back the very effect the pairing measures. That is why
`make-pair.py` is the build step above rather than a `cabal build`, and why
both executables are kept.

`make-pair.py` derives the padding rather than taking it on trust — the size
the aligning shim adds, then the residual phase, which is two measurements and
a rebuild — and it runs `check` and refuses on a bad pair, so the command
above is the whole of it. `check` is the gate and the offsets are not, a
wrongly padded binary having correct-looking offsets and wrong answers. Read
both listings anyway and keep them with the run: the fills at 0 in the aligned
binary and no short loop of its own code straddling, and the unaligned
binary's offsets recorded as they stand, since the six-arm prediction is made
from them and no later binary has them; `--survey` is the length-agnostic
form and takes one binary at a time
(`./loop-offsets.py --survey micro-aligned`), and what "every timed arm's
loop" means is bounded by what can be
attributed at all. The sequence below runs each half in turn, and
`run-major.sh` does it for you; what neither can do is interleave two
processes of this size within a population, so the order they ran in is
written down and is one of the two things left uncontrolled.

**The other was that the halves differed by more than Main's alignment, and
that one is fixed.** Aligning grows `.text` by 12 KB, so everything linked
after it moves: in the first pair built here, of 867 library symbols carrying
a short loop, 856 sat at a different address and `vector`'s straddling short
loops went from 36 to 40. The shim reaches only what GHC compiles here, so
those loops were rerolled rather than aligned, and an arm whose innermost work
is in library code would have carried a term the pairing scrambled instead of
removing — which is not hypothetical, `list`'s own loop being library code
(prediction 5). `pad-as.py` closes it: padding the unaligned half to the same
size *and phase* leaves 95% of the library loops at the same cache-line offset
and 98% in the same straddle state, the rest of the delta being 384 bytes,
six whole lines. Matching the size alone does not do it — that left the delta
at 416, which is 32 mod 64 and so the worst shift available — and the two-step
that does is in that file. So the pair now differs in Main's loop alignment
and in nothing else an offset can see, and `micro-unaligned` keeps every
offset the unpadded build had: the same fills at [3, 53, 59, 45] and
[16, 0, 36, 36], the same 115 short loops with 50 straddling.

**Which two halves a pair has is a property of the pair, not of this page.**
The names are recorded in `<prefix>-pair.txt` and set in one place in each of
`run-major.sh` and `run-gate.sh`, as `OTHER` and `BASIS`; the basis is the
half the classes run on, the expected bench counts are read from and every
table is installed from, and it runs second. Run 10's two were `unaligned`
and `aligned`; **Run 11's were `maxskip` and `aligned`**, its basis being Run
10's aligned binary reused byte for byte, which is what made its first
question an exact repetition. So read every *aligned half* below as the basis
and every *unaligned half* as the other one, except where a sentence is
plainly about Run 10 — as the paragraph below on `pad-as.py` and the
12 KB of `.text` is, every figure in it being that pair's.

**Name the artifacts by half, and drive every `--in-place` from the basis
half.** The sequence below builds every filename off `$R`, which a paired run
has to split: one `$R-<half>-main.json` per half, and the class files
`$R-<basis>-$c.json`, there being no others — the infix being the binary's own
name, so an artifact cannot be traced to the wrong half. **All three
installing modes come from the basis**: `--markdown`, `--fingerprint` and
`--block` alike, so the page carries one basis and not one per half, and what
the other half contributes is the `--compare` and a yardstick column. Run 10
is the one run that answered otherwise, its Results table coming from the
unaligned half while its fingerprint and its class blocks came from the
aligned one — a split it needed because its aligned half was the first here
and had no predecessor to succeed. That ended with Run 11: **the aligned half
is the table and the second half is the control**, whatever the second half
is built to price.

**What the other half is for**, since a run that publishes no table from it
will otherwise be asked why it spends an hour building and timing it. That
depends on which half it is, and the pair is chosen for it. An *unaligned*
counterpart is the layout control, the per-arm term being measured afresh
each run rather than inherited, and it is the yardstick for GHC itself: the
native backend aligns no loop today ([the floor section][floor]), and when
that is fixed the same pairing is what prices how well GHC does it against
the assembler shim here — a comparison no single build can make. Run 11's
*max-skip* counterpart prices the shim's own padding instead, its two halves
differing in which loop heads get a directive and in nothing else, so its
arms separate what alignment buys from what the NOPs cost.

**The pairing doubles the main set and not the classes.** Both halves run the
main set, since that is where the per-arm comparison lives; the eight class
populations run on the aligned half alone, class blocks existing for
orderings within a population and those being exactly what alignment makes
readable. It is an explicit exception to the rule above that a major run
covers every population — stated here rather than left to the runner, which
is what that rule asks for — and a **standing** one rather than a concession
made once, now that every run is paired. The hour it saves is not the reason
and would not survive as one, an hour being cheap against a population's
worth of figures; the reason is the sentence before it, that a class block is
read for the ordering inside its own population and the aligned half is where
that ordering is legible.

**And one more, nearly free**, because everything above exercises the
*benchmark* while nothing exercises the *reader* until
hours later — at `-L1`, since the smoke tests the reader's code paths, not
its statistics:

    ./micro-aligned -L1 cnn-slice-c32 --json smoke.json
    ./micro-maxskip -L1 cnn-slice-c32 --json smoke-other.json
    ./micro-aligned classes window-28x28-k5 -L1 --json smoke-class.json
    for f in smoke.json smoke-class.json; do
      for m in --selftest --aa --shapes --markdown --cells --fingerprint \
               "--pair bq-expand list" ""; do
        ./read-run.py $f $m >/dev/null || echo "BROKEN: $f $m"
      done
    done
    ./read-run.py smoke-class.json --block >/dev/null || echo "BROKEN: --block"
    ./read-run.py smoke.json --compare smoke-other.json >/dev/null \
      || echo "BROKEN: --compare"
    cp README.md README.smoke.md            # --in-place WRITES; never at README
    ./read-run.py smoke.json --markdown --in-place --readme README.smoke.md \
      >/dev/null || echo "BROKEN: --markdown --in-place"
    ./read-run.py smoke.json --fingerprint --in-place \
      --readme README.smoke.md >/dev/null || echo "BROKEN: --fingerprint --in-place"
    ./read-run.py smoke-class.json --block --in-place --readme README.smoke.md \
      >/dev/null || echo "BROKEN: --block --in-place"
    ! cmp -s README.smoke.md README.md \
      || echo "BROKEN: --in-place wrote nothing"
    rm smoke.json smoke-other.json smoke-class.json README.smoke.md

These use a binary already built rather than `cabal run`, which would build a
third one in whatever regime the shell happens to carry; they exercise the
reader rather than the regime either way.

`--in-place` earns its own block because it is the one mode that writes:
pointed at `README.md` it would install a one-shape smoke table over the
published one, so the copy is the point, and `cmp` afterwards is what keeps
the check from passing on an installer that found nothing and said nothing.
Run the copy's own diff by eye if a table looks wrong; the copy is deleted
with the rest. **Each install is smoked from the half it will really come
from** — all three from the basis half, `--markdown` and `--fingerprint`
off the main-set JSON and `--block` off the class one — which is why these
are three commands and not a loop. The write-up is hours too late to find a
broken installer.

The first runs every timed arm on one shape and puts the whole analysis
path — the correction, the controls, the table generator — through its
paces; the third does the same for the `classes` plumbing, the reader's
per-list shape rules and the six-column class table, on the class whose
rule is least trivial. Those two go through every single-file mode, because
they take different paths through the reader from the population line
onwards. A reader broken by a roster or shape-list change fails here in
minutes instead of after the run.

The second file exists for `--compare`, which no single file can reach: it
is the reader's only two-run mode and the one a paired run is read with, so
leaving it out of the sweep would leave the pairing's own instrument
untested until the write-up. It is also the only point before the evening at
which the *other* half writes a JSON at all — the basis half writes the
first file — and a pair whose halves turn out not to be comparable has cost
the hours twice.

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

**"Roster change" here means membership, and the test is `--list`**: the
binary's listing differs from what the previous run's did, in its set of
names rather than their order. Criterion emits it sorted, so an arm moving
slot cannot produce a false positive — which is the only thing making the
test sound and is worth knowing, since order *is* a change, of the kind
[Provenance](#provenance) deals with rather than this pass. An edit to the
reader or to a claim is not a roster change either, though the three reasons
above are worded in their terms because a roster change is the only thing
that has ever broken them. What the test cannot usually do is run itself: the
previous run's binary is deleted and its listing recorded nowhere, so the
comparison is against the roster delta under [Provenance](#provenance), which
is kept for exactly this. A run whose basis half *is* the previous run's
binary, as Run 11's is, answers it outright instead, and the pair note records
the count on both sides. Spelled out because two readings of this paragraph
have split on it: with membership unmoved the pass is not owed however much
else changed, and Run 10 is such a run.

**A paired run has one gate more, and the first thing to do about it is read
rather than run it. The gate belongs to the pair, not to the session**, which
is what stops it being paid for twice. `make-pair.py` writes a
`<prefix>-pair.txt` beside the binaries — `micro-pair.txt`, the prefix being
the one everything here is named for — with what it verified and a `GATE:`
line saying it has not been run; `run-gate.sh` appends to that file. So read
what the note says about the gate first — `grep -i gate micro-pair.txt`,
case-insensitive and not anchored on the `GATE:` token, because a note
written by hand says it in prose and grepping for the token finds nothing in
one, which reads as *no gate* and costs the hour it was meant to save. **Read
the whole output and not its last line**: `run-gate.sh` closes its own block
by asking for a reading, so a note whose verdict was written above that block
— which is where a hand-written one goes — greps up as *the reading is
still to do* however long ago it was done. The verdict is a `GATE:` line, and
the newest one wins. If it
records a pass, this step is already done and the next action is the run
itself. A `--verify-only` run earlier in this procedure does not disturb
that: it appends its measurements alone, the `GATE:` line going in only when
a note is written fresh, so re-verifying a pair cannot restate *not yet run*
over a verdict saying otherwise. `make-pair.py` being deterministic, a
rebuild that comes out md5-identical inherits the gate too, and one that
does not — a
changed `Main.hs`, a changed regime — needs its own. Re-running it on a pair
that has already passed costs a quiet hour and can only reproduce what the
note says.

**If that line says the gate has not run**, it is the last thing before the
evening. `run-gate.sh` takes five benches over the shape set from each half,
twice each, in a palindrome — unaligned, aligned, aligned, unaligned — so that
drift over the hour cannot read as a difference between the binaries, which is
the part a person retyping the command would drop:

    ./run-gate.sh
    ./read-run.py gate-aligned-a.json --compare gate-maxskip-a.json

It wants the same quiet the run does and costs the better part of an hour, so
it is not one of the cheap checks above; what it buys is finding out that the
aligned binary is wrong before an hour of main set is spent on it, and a first
reading of the arms the pairing is predicted on. What the script writes back
into the note is the mechanical half alone — four exit codes and four bench
counts — because that is what it knows; whether the pair is sound is the
reading's verdict and is written there by hand. What the predictions are, and
what the gate read when it was last run, are in [the open
list](#what-is-open) with the rest of the run's registrations.

**The run** is one sequence — the main set from each binary the run has,
then each stride-class population in its own process, in `classViews`'
order. Each `$c-` argument
selects a class by name prefix, the prefixes being disjoint by
construction (`bcast-` does not match `bcastmid-*`); one process per
population is the recorded protocol at `classBenches`, so no population's
figures owe anything to another's leftover heap state and each JSON is
single-population by construction. **The regime is a variable of the procedure,
not a flag to remember**: it is set once at the top beside the run's name and
goes to `make-pair.py`, so that leaving it empty is a deliberate act rather
than an omission. It reaches the *build* and nothing else — no check mode
takes a regime, and on the confirm-don't-rebuild path nothing consumes it at
all, `--verify-only` building nothing to apply it to. There the whole guard
is the `diag` reading above, which is why that step is not optional on a path
that skipped the build. A run made in
the wrong regime is not detectably wrong — the roster, the shapes, the gates
and the reader all pass, the JSON records no compiler flag, and the only
symptom is the regime's own effect failing to appear, which reads as a
refutation of the design rather than as a missing flag:

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

**`run-major.sh` is that sequence as a driver**, and `$R` is its argument
rather than a variable it inherits:

    ./run-major.sh $R          # ten processes, unattended, several hours

It refuses without one, the prefix being the run's identity: artifacts called
`run-*` would not say which run made them and the next run would overwrite
them. **It also refuses to start where that name already has artifacts,
which makes an interrupted sequence a hand job — expect that, since the
machine gets wanted back.** The guard is right (relaunching overwrites hours
in place), but it has no resume, so finishing a sequence whose main sets
landed and whose classes did not means running the class loop yourself: the
`for c in ...` half of the sequence above, with the basis half's name, an
`[ -e "$out.json" ] && continue` before each so a population that already
ran is skipped rather than redone, and its `benchmarking` count checked
against `classes --list` as the driver does. Stamp each into the same
`$R-wallclock.log`, so the run's own record stays one file, and say in the
write-up that the populations ran in more than one window — one process per
population is what makes that harmless, each carrying its own controls and
gates, but it is a fact about the run and the chapter states it.

What it adds over pasting the sequence is the counting: every
process's bench count is checked against what the roster holds, so a selection
that silently caught the wrong set is loud in the log at once instead of at
the write-up — loud rather than fatal: the sequence carries on to the next
process, there being no reading in which eight sound populations are worth
discarding for one that is not, so the wall-clock log is what has to be read
before any figure is.
The expected count is read from the binary's own `--list` rather than written
down, because a literal would be wrong for the next roster and would turn a
correct run into an alarm on every process; `run-gate.sh` derives its own the
same way, and a class process's is its prefix's share of `classes --list`,
a prefix matching nothing being reported rather than run as a process of no
benches. Neither builds anything, and both refuse to start without the pair.
The sequence:

    {
      date -Is
      # A paired run: both halves take the main set, the classes go to the
      # basis half alone, and each half is its own binary -- never rebuild
      # between them. $OTHER and $BASIS are the pair's, set in run-major.sh.
      for h in $OTHER $BASIS; do
        ./micro-$h --json $R-$h-main.json > $R-$h-main.log 2>&1
        echo "$h main exit=$? $(date -Is)"
      done
      for c in rev revsome bcast bcastmid reshape1 slice window scaled; do
        ./micro-$BASIS classes $c- --json $R-$BASIS-$c.json \
          > $R-$BASIS-$c.log 2>&1
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
silently caught more arms than intended. The sequence's own processes have
this done for them by `run-major.sh`, class ones included; what is left to
the runner is every filtered probe made by hand, which is where the rule was
learned and where nothing counts on its behalf.

**Probes whose designs predate the run ride the same script.** The machine
is quiet for the whole sequence either way, so a question already on [the
open list](#what-is-open) with its measurement written
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
**run nothing else on this machine while it does**. Unsandboxed, and confirmed
from a process list rather than from the launching shell, which a blocked
write leaves lying:

    ./run-major.sh run11 &            # its own wall-clock log is the record
    ps -eo pid,etime,comm | grep micro-   # comm, NOT args: any shell that has
                                      #   cd'd here carries micro-regime3 in
                                      #   its own command line and matches

`pgrep -f`/`pkill -f` self-match here and an `until ! pgrep -f …` waiter
therefore never returns; watch `$R-wallclock.log` for `major run complete`
instead. Every strategy of a
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

**Before any of it, read the run's registered predictions** ([the open
list][open]), which say what this run was for and what would kill each one.
Record their verdicts there rather than in the run's own chapter, which the
next run replaces. **And say what a partial outcome is**: a prediction
registered over several arms can come apart, and neither "held" nor
"refuted" is then true -- Run 10's first was stated over three arms and one
confirmed it while two met its own kill condition. Report that as a split,
name which arms went which way, and carry the consequence for each
separately; the temptation is to round it to whichever answer the majority
of arms gives, which loses the finding.

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
   **Then write this run's own floor at the head of your notes and keep it
   there.** Every margin below is judged against it, it is re-measured each
   run, and the runs have disagreed several-fold, so the previous run's
   figure is the one you will reach for by habit and it is the wrong one.
   `--aa` prints each pair's raw ratio and `f` beside the net one for a
   related reason: the net figure is the floor between two published rows,
   the raw one is how much an arm disagrees with itself, and quoting the
   first as the second overstates it by 1/(1-f).
2. **Match bases before reading any ratio.** The first act of a comparison
   is making its two sides one basis — the same population, the same
   restriction, the basis a claim was stated on — and only then reading
   figures. Run 7's first claim check ran on its 24 shapes against claims
   stated on 22, and every pair had to be re-run.
3. Analyse with `./read-run.py`, which is where every table in this file
   comes
   from — read [the reader's own section](#the-reader-read-runpy) first, and
   do not write another reader. **The claims are part of this and are the
   thing these steps are likeliest to leave out**: the run chapter names three
   things a run reads, and the claims section is the third, each of its
   orderings one `./read-run.py RUN.json --pair A B` so that a run reports its
   breaks rather than re-deriving the table. The class properties are the same
   job three times a population, off the verdicts `--block` emits, and the set
   is restated for the next run on this run's basis while the readings are
   still in front of you. **A paired run's own mode is `--compare`, and
   its direction is a convention worth stating**: the run given first is the
   one the ratios are *of*, the `--compare` argument being what they are
   divided by, so `aligned --compare unaligned` puts a figure below 1 where
   alignment is faster. Prediction 4's per-arm term and the aligned half's
   published column both read that way round; reversed, every one of them
   inverts and nothing in the output says so.
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
5. **Rename the three run-numbered headings, which do not all take the same
   number** -- the chapter head goes from the last run to this one, while
   *What Run N compares against* and *The claims Run N should test* look
   forward and go from this run to the next, so a write-up of Run 10 leaves
   the three reading 10, 11 and 11. Repoint every
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
   procedure used to leave to judgement, each of which has caught something.

   **This step is the whole of the document verification a run owes, and
   nothing else is to be reached for.** A write-up is a document edit, so
   the three-pass discipline applies — but its passes live here, in this
   repo's own instruments, and the general-purpose form of it does not fit
   a page whose claims are *measurements* rather than statements about
   code. Pass 1, which resolves `file:line` citations and pinned
   permalinks, has no subject: this page cites no line and no permalink,
   deliberately, and what it does cite — arm names, strategy names, shape
   names, `Main.hs` functions — is what `--lint` checks, which a line
   number could not, a citation surviving the refactor that moves it. Pass
   2 is `--check-doc`'s path check. Pass 3 is the reading, below. The
   heading-scope and cross-reference passes are `--check-doc`'s anchor and
   replace-list coverage checks. **Do not run another repository's
   checkers against this page**: theirs carry a per-repo configuration —
   search roots, an owned module namespace, an allowlist — so pointed here
   they resolve this directory's names in their own tree and report correct
   names as missing, which is the noise-for-signal failure that stops a
   checker being read at all. If a future document here does grow
   `file:line` citations, that is the moment to port one, and not before.

   **What the instruments cannot supply is the reading, and the reading is
   the pass.** What the tools print is its output and not its method:
   `--check-doc`'s three sweeps hand you a worklist of superseded figures,
   superlatives and absolute times, and adjudicating that list is not
   reading the document. Nor is inheriting one — a worklist you did not
   derive verifies somebody else's findings while telling you nothing about
   what else is wrong, which is the completeness question the reading
   exists to answer. Run 11 is the case: every checker green and the
   worklist adjudicated while six errors stood, four of them superlatives
   asserted without sorting the population they quantify over and one
   contradicting its own paragraph three lines later. **So put an
   independent checker on the diff against the artifacts, launched when the
   tables go in rather than at the end**: one, briefed to recompute every
   added figure from the reader and to re-derive every *only*, *largest* and
   *N of the nine* by sorting, and to report discrepancies rather than
   opinions. It is dear per finding — Run 11's cost some thirty times what
   the same session's own targeted re-checks did — and it is worth it
   anyway, because its findings are the ones a session has already proved it
   cannot see in its own prose, and because it returns a completeness the
   author cannot: 306 of 306 table rows verified rather than the ones
   somebody thought to check. Launch it early, keep it to one, and leave the
   placement, contradiction and writing-rule reading to yourself.
   (The rule that a check must be proven able to fail governs the
   instruments themselves and is stated with them, [in the reader's
   section](#the-reader-read-runpy).)

   The checks themselves:
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
      `--aa` and `--block` both take `--brief`, which drops the standing
      explanation and the table `--in-place` installs anyway, costing no
      computed figure; over ten populations that is several hundred lines you
      have already read.
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
8. Re-run `--lint` after editing `Main.hs`, even when only comments changed:
   the reader parses that file for the roster and the shape dims, so a comment
   edit can break a check that passed before it. `--lint` reads the source and
   needs no build, which is the whole of what that reason asks for. **Do not
   rebuild the pair to satisfy this step.** Steps 6 and 7.7 send you into
   `Main.hs`'s comments on purpose, and `make-pair.py` would overwrite both
   halves and append a block to `<prefix>-pair.txt` stamped with today's date
   and commit — which is the file the next step transcribes the binary's
   provenance out of. A comment edit after the run leaves the timed binaries
   correct and the source they were built from moved by a comment; say so in
   the write-up rather than rebuilding to hide it;
9. Record beside the numbers the run's name and regime, each process's stderr
   provenance line, which machine, **and the commit the binary was built
   from** — for a paired run, transcribed from `<prefix>-pair.txt`, which
   carries the commit, the regime, the GHC and both md5s because this step
   asks for them and the note outlives the session that built the pair (the
   JSONs do not survive, so the source is the only thing that
   makes a run reproducible even in principle — this page's figures are one
   desktop's and are not portable, see [Provenance](#provenance)). A class
   process's line is measured for its elapsed time and its two heap peaks but
   not for its shape count: that count is fixed before criterion does the
   selecting, so it reads every class view rather than the population that
   ran, and the population's own size comes from the reader's first line;
10. **Walk the open list against what this session actually did**, which
   nothing checks. **Grep [the settled index][settled] before adding an
   entry**, not only before deriving: a question is easy to open against
   something already answered in a section you are not writing in, which is
   how Run 10's write-up proposed a Core dump that had been taken three times
   and whose answer -- `vBuildVS` surviving as no top-level binding, so there
   is no call path to dump -- was recorded at the ceiling, a thousand lines
   from where the entry was being written. A run answers some of its own
   questions and a write-up
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
   the JSONs, the logs and the wall-clock file alike, and for a paired run
   the two binaries and their `<prefix>-pair.txt` with them, that note being
   about a pair and worthless once the pair is gone. **A change of basis at
   the next run buys no exception here**, which was proposed and refused.
   The argument for keeping Run 10's JSONs was that Run 11 reads against an
   aligned fingerprint Run 10 would never have published; the answer is to
   publish it, which the plan above now does. Keeping a JSON to regenerate a
   record this page already has a mechanism for would trade a durable
   artifact for a fragile one, and would make the no-artifacts rule
   conditional in a way that does not stay temporary — the fingerprint exists
   precisely so that a per-shape record outlives its run, and Run 6's deleted
   artifact is the precedent it was built on.
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
    ./read-run.py A.json --compare B.json   # one arm across two runs
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

That is the standing rule for everything under `--lint`, `--selftest`,
`--check-doc` and the
`health` warnings, and it is why each carries a recorded proof in its
docstring: **a new check is not finished until it has been made to fail on
purpose**, with what was broken and what it then said written down beside it.
Several here can only fail on data no real run produces — a forcing term
larger than the cell it is subtracted from, a term that does not scale with
`l` — so provoking them is the only way to know they are wired to anything.
It reaches a pass run *by hand* too, which has the same failure and no exit
status to hint at it: before calling one clean, break something it ought to
catch and confirm it says so. And it reaches a check's every *branch*: the
path check's absent-sibling arm is exercised by pointing its roots at a
directory that does not exist, since a branch no control reaches is a silent
search whatever the checks around it do.

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


### What moves a figure when no strategy changed

Six A/A controls run an existing strategy twice under a second name — three
strategies, each duplicated once beside its base and once at a distance, so
position varies within a strategy and strategy within a position. They
are the only rows whose true ratio is known to be exactly 1 — or were, until
[the mutable ceiling](#the-mutable-ceiling-not-taken) turned up another by
accident:

| pair | span | max-skip | aligned | mean per cell |
|---|---:|---:|---:|---:|
| `mut-odo-vecdims` vs adjacent twin | 1 | 1.0000 | 0.9967 | 0.19 / 0.41% |
| `bq-expand` vs adjacent twin | 1 | 1.0001 | **0.9879** | 0.31 / 1.24% |
| `bq-scan-rem-gm-mulback` vs adjacent twin | 0 | 1.0003 | 0.9996 | 0.24 / 0.12% |
| `bq-scan-rem-gm-mulback` vs distant twin | 21 | 1.0014 | 0.9997 | 0.47 / 0.55% |
| `mut-odo-vecdims` vs distant twin | 3 | 1.0021 | 0.9967 | 0.27 / 0.67% |
| `bq-expand` vs distant twin | 24 | **1.0022** | 0.9883 | 0.49 / 1.66% |

Run 11 is paired, so each pair reads twice; the two columns are the two
binaries and nothing else. No pair had a cell capped in either half, so every
published figure above equals its paired one — the identity the winsorized
estimator bought and `--selftest` asserts — and the published column is the
yardstick for comparing two rows of the Results table, while a margin
measured per shape still belongs against the paired figures `read-run.py
--aa` prints. The spans are Run 10's, the roster order being Run 10's.

**On Run 11 the floor is 0.22% on the max-skip half — the tightest this page
has measured — and 0.33% on four of the aligned half's six pairs against
1.21% on all six.** The whole of that difference is one cell, the 35% at
`lenet-L1-28-c1-k5/bq-expand` that both `bq-expand` pairs inherit through
their shared base ([the head of the run chapter](#about-the-last-run-run-11)):
their worst cells are 25.51% and 26.44% where the other four pairs' are
inside 3.7%. So the threshold this run supports is *a quarter of a percent
between any two rows of the table, and a fifth of that between two rows
neither of which is `bq-expand`* — where Run 10 supported 1.00% unaligned and
0.54% aligned, Run 9 under 0.1% with a wild cell, Run 8 0.5% and Run 7 nearly
4%. Runs disagreeing several-fold on the floor is itself the caution: read
the floor as the run's, re-measured every time, not as a constant of the
harness.

**The twins changed sides between two runs of one binary, which is what a
sign this weak is worth.** Run 10 read all six pairs above 1 on its unaligned
half and five of six above on its aligned one, the twin slower than its base,
and called it worth a sentence and not a mechanism. Run 11 reads all six
*below* 1 on that same aligned binary and five of six above on the max-skip
one. Three strategies at two positions each are not six independent draws,
and the direction is evidently not a property of the code, the layout or the
roster order, all three of which were held fixed across the flip.

The CI% for those six rows reads 0.02-0.15%, so the interval still
understates run-to-run variability: it
measures sampling error *within* one benchmark, while two separately placed
benchmarks also differ in code layout, cache occupancy and inherited GC
state. The A/A is the only column that sees that, and `--aa` prints the
calibration outright — on Run 11, a median interval half-width of 0.18%
against an observed spread of 0.22% on the max-skip half, a factor of **1**,
and 0.36% against 1.21% aligned, a factor of **3** that the wild cell alone
buys — so multiply any interval this reader prints by about that before
believing it, where Run 10 wanted four and one, Run 9 nine, Run 8 two and Run
7 three. Two builds one shim apart differing this much in the factor is the
warning the calibration is meant to carry: it rests on six pairs, and one bad
cell moves it.

**And what is left when every other cause is pinned has now been measured:
run-to-run drift is a few percent per cell and a quarter of a percent on a
geomean.** Run 11 re-ran Run 10's aligned binary with shapes, roster, order
and regime unchanged — the repetition this page had wanted since Run 9 — so
its every movement is drift and nothing else. `list`'s per-shape scatter is
**0.958 to 1.043**; of 762 cells, 495 are within 1%, 693 within 5% and 743
within 10%; every arm's geomean is within 1.5% but `mut-odo`'s 1.0327. That
is the figure to hold a *later* margin against, and it is a quarter of the
0.902-to-1.181 band Run 10 had to quote when the roster order moved the
layout underneath it. Two consequences worth keeping when the run chapter
carrying them is replaced: a margin of a few percent between two runs is
still not evidence, and a margin under about 1.2% between two *arms* of one
run is not either, which is the A/A floor above and a different quantity.
The exceptions are `build` and `mut-odo`, one worker at two slots, whose
cells reach 1.25 and 1.16 with their loops at offset 0 in both runs — the
residue the pairing cannot reach, and [the open list][open]'s.

**And a busy machine has now been measured rather than only avoided, which
is what says the wild cell is not one.** Run 11's sequence was launched
twice; the first attempt's max-skip main set completed before it was stopped,
on a machine that turned out not to be quiet, and its artifact was read
against the recorded one — the same binary, the same roster, an hour apart —
before being deleted with the rest. The disturbance is **diffuse**: the floor
rises from 0.22% to **1.11%**, **50 of 762 cells** run more than 5% slow,
and the worst of them are scattered over four shapes and eight arms
(`build` on `cnn-L2-24x24-c32` 1.161, `bq-odo-gm-mulback` on
`stretch-square-1341` 1.147, `mut-odo-vecdims` on `cifar-L2-16-c64-k3`
1.138), while every arm's geomean stays inside 2% and the per-shape ranges
widen to 0.758..1.161. **The wild cell is the opposite signature in every
respect**: one bench, its interval a twentieth of a microsecond, its
neighbours in run order and its own two twins clean — and in this disturbed
run `lenet-L1-28-c1-k5/bq-expand` reads 1.0070, so the shape and slot are not
what carries it either. An intrusion smears; this does not, which is why it
is a finding and not noise.

**The wild cell went where the fix predicted, and came back somewhere the fix
does not reach.** Run 8 recorded `bq-expand`'s distant twin 44% slow on
`vgg-14-c512-k3`, Run 9 41.4% on the same arm and shape, and five filtered
probes ran it down to a cold block pool at that twin's roster slot. Run 10
moved `sum-only-early` above `list`, so nothing is measured on an ungrown
pool, and that pair read 1.0043 with its worst cell 1.67% on a different
shape — the three-bench probe that priced the fix at 0.24% reproduced over
the whole roster and shape set at full budget. **Run 11, on that same binary,
carries a 35% cell at `lenet-L1-28-c1-k5/bq-expand`**, with both of that
arm's twins clean, both time-neighbours clean, CI% 0.06 and `list` on the
shape unmoved. So what the roster fix removed was the *slot* — a twin
measured on an ungrown pool — and not whatever makes this family
susceptible: the same arm, the third run in four to carry a cell of this
size, and this time at its own slot rather than a twin's. Nothing here has
been probed, the machine having been wanted elsewhere; [the open
list][open] carries what would settle it. The account of the Run 8 and Run 9
cell, from those probes (2026-08-09, Run 9's own binary and regime), stays
because the mechanism is what the predictor below rests on and because a
recurrence is the reason to keep it:

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

  **The predictor called it, on a control shape** — the excess-allocation
  rule stated in full below. `cifar-L2-16-c64-k3` has
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
unevenly and are where a nursery A/B would move a table.

**That second half was tested the same day and the prediction holds.** Both
arms plus a `sum-only` half, filtered over all 24 shapes, run twice from
one binary with the nursery as the only difference (2026-08-09): the pair
reads **1.1604** at the default and **1.1433** at `-A32m`, each at three
wins of 24 and sign p 0.00028. The gap does not move. Nor do the arms
themselves, 1.028 and 1.043 in absolute time across the change, against the
35–40% the excess-allocating arms show. Two things follow. The predictor
survives a test it could have failed, on the side where failure was
cheapest to detect. And **the placement question is now confirmed
independent of the allocator**, so the pad probe was unavoidable rather than
possibly-subsumed: this pair's 1.16× is not filtering either, the full run
reading 1.13× over the same shapes with 31 benches between the two arms.

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
under `-fspec-constr`, the dumps being [the mutable ceiling][ceiling]'s,
which is where that identity is kept — so they are a seventh
known-true-ratio-1 pair, and
they disagree by 1.24× on Run 7, 0.86× on Run 8, **1.13×** on Run 9 (3
wins of 24, sign p 0.00028) and 0.95× on Run 10's unaligned half. Four runs,
two of them differing from their predecessor in the roster alone, and the
pair spans 0.86 to 1.24: that range
is the instrument, and it is 44% wide for code that is identical. The twins
share one worker called from two slots; those two are separate
copies of one worker at two addresses, and the gap between what the two
instruments read is the part of layout the twins cannot see. Do not price a
margin between distant rows at the twins' floor. **Aligning both copies
shrinks the instrument rather than zeroing it**: on Run 10's aligned half the
pair reads 0.9685 with both copies at offset 0, so about 3% survives the one
intervention that removes the whole difference the table above attributes it
to — and the sign test ties there, 16 of 24, where every unaligned reading of
this pair has been lopsided.

**And those two addresses now have a candidate consequence, read out of the
binary** (2026-08-09, `-fspec-constr`). The innermost run-fill is 28 bytes —
seven instructions and a backward branch — and the binary carries four
byte-identical copies of it, two per arm, the only alignment directive
anywhere in either procedure being `.align 8`. One copy per arm is the
mismatched-length `fail` join and cannot run on a well-formed shape; the
copies that do run are `mut-odo`'s at byte 29 of its cache line, which fits,
and `build`'s at 53, which straddles two. The dead copies fall the other way
round, which is why the pair looks like a wash until the executed one is
identified. That is one bit against one gap, so it was a candidate and not an
account — but one the pad probe could test, nothing pinning these loops to a
line: pad in eight-byte steps until `build`'s executed copy lands whole and
see whether the gap goes with it. It did — the confirmation is below the loop
table. The instrument is steady meanwhile, the flag's 12 KiB of `.text`
reproducing to the byte on a base the arms written since have grown.

**And a second family reads the same way, which is what takes it past one
point.** The four `mut-odo-vecdims` arms carry one copy each of that same
28-byte fill, the FastReshape three differing from their control nowhere
inside it ([the mutable ceiling](#the-mutable-ceiling-not-taken)), so their
copies stand beside `build`/`mut-odo`'s. **Every ratio is the row's arm
against its family's control** — `mut-odo-vecdims` for the four arms under
it, `mut-odo` for `build` — which is why the two control rows have no ratio
of their own and read `--` in all three: a control against itself is 1 by
construction and says nothing. The offsets are the executed copy's, read with
`loop-offsets.py`:

| arm | loop | mod 64, Run 9 | Run 9 ratio | mod 64, Run 10 | Run 10 ratio | aligned ratio |
|---|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | 28 B | 24 | -- | 16 | -- | -- |
| `mut-odo-vecdims-add-in` | 28 B | 40 | 1.1552 | 0 | 0.9937 | 1.0009 |
| `mut-odo-vecdims-add-out` | 28 B | 44 | 1.1795 | 36 | 1.1266 | **1.1612** |
| `mut-odo-vecdims-add-both` | 28 B | 44 | 1.1645 | 36 | 1.0906 | **1.1184** |
| `mut-odo-vecdims-add-both-down` | 24 B | 33 | 1.0183 | 29, 5 | 1.0149 | 1.0527 |
| `mut-odo` | 28 B | 29 | -- | 53 | -- | -- |
| `build` | 28 B | 53 | 1.13 | 45 | 0.9532 | 0.9685 |

The count-down row is the one whose loop is not the 28-byte fill, so
`loop-offsets.py --len 24` is what finds it, and its group has two copies
with neither attributed to a call path: 29 and 5 in `micro-unaligned`, both
at 0 in `micro-aligned`. Which of the two executes does not matter to the
question this table asks, since a 24-byte loop fits inside a line at both 29
and 5, so that row is resident in every binary here.

**On Run 9's binary every copy that fits inside one line read level or ahead
and every copy that straddles read 13–18% behind, with no arm of either
family dissenting. Run 10 splits that.** Its offsets come from
`loop-offsets.py` over the two binaries, so the mod-64 column is read and not
inferred, and the aligned column is a build in which all ten copies the table
covers sit at
0. `build`/`mut-odo` behaves as the hypothesis says throughout — both copies
straddle in `micro-unaligned` at 45 and 53, both are resident in
`micro-aligned`, and the pair goes from Run 9's 1.13 to 0.9532 and 0.9685.
`add-in` behaves as it says too, and twice over: its copy is resident in
*both* Run 10 binaries and the ratio is 1.00 in both, where Run 9 had it
straddling at 40 and reading 1.1552. But `add-out` and `add-both` are
resident at 36 in the unaligned half and at 0 in the aligned one, and they
read 1.1266 and 1.0906, then **1.1612 and 1.1184**. Four placements each,
none of them straddling, and the penalty does not go. So the correlation
inside Run 9's binary was real for one arm of the family and coincidental for
two, and what those two cost is not layout — it is read in [the mutable
ceiling][ceiling], whose suspension of those figures this withdraws. The
count-down form sits in the table for completeness, resident throughout and
so with nothing to say about straddling either way, and is read in its own
section.

**A third placement of the pair, taken the same day, says what the residual
is** (2026-08-11, `-fspec-constr`, one filtered pass, `*/build` and
`*/mut-odo` over the shape set, 48 benches in each process, the two arms
adjacent so each ratio is formed inside one process). The
`-fproc-alignment=64` build below puts *both* executed copies at 53 — the
same offset, both straddling — where `micro-unaligned` has them at 45 and 53
and `micro-aligned` at 0 and 0:

| binary | the two copies | `build`/`mut-odo` | 95% CI | sign test |
|---|---|---:|---|---|
| `micro-unaligned` | 45 and 53 | 0.9585 | 0.9347..0.9813 | 18/24, p 0.023 |
| `micro-aligned` | 0 and 0 | 0.9782 | 0.9498..1.0054 | 12/24, **p 1** |
| `micro-procalign` | 53 and 53 | 0.9893 | 0.9703..1.0091 | 16/24, p 0.15 |

**Whenever the two copies share an offset the pair ties, and when they do not
it does not** — and that holds at a resident shared offset and a straddling
one alike, which is what layout-neutral-by-construction predicts and what no
earlier reading could separate. **What this cannot do is rank the two
same-offset builds.** Their intervals overlap heavily and the two tests
disagree about which is nearer level — the shim's build has the flatter sign
test and the flag's the point estimate nearer 1 — so 0.9782 against 0.9893 is
not a difference one filtered pass resolves, the same binary moving by about
as much between a filtered reading and a full-roster one (0.9782 against
0.9685). Procedure placement, which aligning loop *heads* does not control,
therefore stays a candidate for the residual rather than a finding. What the
probe does settle is that no placement of these two copies leaves them more
than about a percent apart once they share an offset.

**A build with both, and an instrument that does not cancel** (2026-08-11,
`-fspec-constr`, `*/build` and `*/mut-odo` over the shape set, 48 benches a
process). `micro-both` carries the shim *and* `-fproc-alignment=64`, so all
eight fills sit at 0 inside procedures pinned to 64 — the build [the open
list][open] asked for. Its pair ratio ranks nothing: 1.0001 and 0.9820 over
two passes
against the shim alone's 0.9921 and 0.9695, where each build's own passes
differ by 1.8 to 2.3%. That is the pair ratio's nature, dividing two arms
that share a penalty. The absolute per-arm reading does not cancel:

| against `micro-aligned` | its two copies | `mut-odo` | `build` |
|---|---|---:|---:|
| `micro-procalign`, the flag alone | 53 and 53 | 1.1167 (1/24) | 1.1294 (2/24) |
| `micro-unaligned`, phase-matched | 45 and 53 | 1.1061 (2/24) | 1.0839 (3/24) |
| `micro-both`, the shim and the flag | 0 and 0 | 1.0163, 1.0319 (6, 4/24) | 1.0246, 1.0451 (9, 7/24) |
| `micro-aligned`, its own second pass | 0 and 0 | 1.0025 (13/24) | 0.9797 (14/24) |

The count is shapes of 24 where the row's build is faster. So a shared
straddling offset costs both arms 8 to 13% while leaving their ratio level
— the flag removes the variance, not the cost — and shim plus flag costs 2
to 4% over the shim alone. **Indicative only**: one pass a row against that
same repeat spread, times uncorrected, and only `micro-unaligned` phase-
matched to the basis. That row is what says the instrument works, reading
1.11 and 1.08 where Run 10's full budget read 1.16 and 1.14. Keep these out
of the table above, which is one pass per binary of a different quantity.

**The probe has since confirmed it, and found the penalty graded**
(2026-08-10, `-fspec-constr`, eight binaries differing only in inert pad arms,
two interleaved passes over the shape set, no rebuild anywhere in it;
the tables are here, the scratch directory being gone). Each arm
was stepped through all eight 8-byte offsets with code, membership and bench
order fixed, so each is a reading of one penalty in its own right: `build`
runs **1.169×** slower where its executed copy straddles and `mut-odo`
**1.162×**, every straddling placement of an arm slower than every resident
one. The discriminating pair inverts as predicted — 0.874 where only
`mut-odo` straddles, 1.102 where only `build` does. And the penalty turns on
*where* the split falls, which no reading inside one binary could have shown:
offsets 37, 45 and 53 cost 1.19 where offset 61, three bytes short of the
boundary, costs 1.10 — which is why the one control with both arms straddling
reads 1.069 instead of level, `build` at 53 paying full where `mut-odo` at 61
pays half. Evaluated at Run 9's own offsets those penalties give 1.144
against the 1.13 it read, on a binary not among the eight. The binaries
differ in placement and in nothing else: fitted allocation agrees to
1.000008 across the sixteen runs, and the subtracted forcing term spreads
1.0046 where the arms spread 1.20. So the table above stands, and the 13–18%
it spans is the distance between a deep straddle and a resident copy rather
than a range still to be explained.

**What that span bounds is every margin under about a fifth — in an
unaligned build.** The per-offset
figures run 0.9040 at offset 13 to 1.1051 at 37, so one loop's placement is
worth **1.22×** best to worst, and that is the number a margin has to clear
rather than the 1.169. Two rows of the Results table differing by less can be
layout entire, and the A/A twins cannot see it: they call one worker from two
slots, executing one copy at one address, where `build` and `mut-odo` are two
copies at two. **An aligned build removes that variance rather than bounding
it**, every short loop of Main's code sitting at offset 0, so a margin read
there does not have to clear 1.22 — which is what makes the aligned half the
place to adjudicate, and why a margin agreeing across the two halves is
evidence where either alone is not. Two limits on that. It reaches only the
loops the shim reaches, Main's and not the libraries', so `list`'s own hot
loop is outside it. And attribution is per arm and exists for six of them, so
for any other pair this is a statement about the population of loops rather
than about that pair's own. Reading the offsets is minutes of `objdump`
against a quiet-machine window, so it is the cheap first question about a gap
this size.
`loop-offsets.py` beside this file finds the copies structurally — a backward
branch whose target is one loop length back, grouped by raw bytes, so
"byte-identical copies" is read rather than assumed — and it was proved
non-vacuous by reproducing three of the probe binaries' documented offsets
before it was pointed at anything new.

**But the table corrects only where the loop is the same code; elsewhere it
screens.** As 0.98 × pen(A's offset) / pen(B's offset) -- the intrinsic
ratio being 0.98 and not the 0.9973 the probe's balanced design gave, which
Run 10's gate settled against it (see the open list) -- it reproduces the
eight binaries to a median 1.0% and a worst 3.8%, Run 9's pair to 1.144
against the 1.13 read, and the FastReshape three to 1.18 against 1.155–1.180.
Its resolution floor is the 5.9% by which the two arms disagree at offset 13,
so it settles a 17% gap and cannot touch a 5% one. And it reaches the six arms
carrying this fill and no others: dividing layout out of two *different*
algorithms needs each one's own penalty curve, which only stepping that arm's
address supplies. Everywhere else this is a quantified caveat, not a
correction.

**GHC's native backend aligns no loop, and every other compiler to hand
does** (verified 2026-08-10 on this machine). GCC 13.3 at -O2 emits
`.p2align 4,,10` at each loop head, on by default as `-falign-loops=16:11:8`;
clang 18 emits `.p2align 4` above every block LLVM marks an inner loop header,
with nothing asked for. GHC's NCG emits `.align 8` at procedure starts and
nothing inside them — on 9.10.3, 9.12.4, 9.14.1 and HEAD (10.1.20260803)
alike, and `-fproc-alignment=64` adds none of it either — which is what leaves
this loop wherever it falls. The
exposure follows: at 8-byte alignment three or four of the eight reachable
offsets straddle, four of eight for this one; at 16 bytes one of four; at 32
or more none at all, a 28-byte loop starting at 0 or 32 ending inside its line
either way.

**An isolated reproducer prices the same effect at 1.58×, and names what it
needs to appear** — horde-ad's `docs/ghc-issue-no-loop-alignment.md`, filed as
[GHC work item
27668](https://gitlab.haskell.org/ghc/ghc/-/work_items/27668), which is where
this belongs written up and which cites this
benchmark for what `-fproc-alignment=64` does in a larger program and what the
correction costs there. A 23-byte loop stepped through all eight 8-byte
positions of a line runs 0.256 to 0.261 ns an iteration at the six that keep
it whole and 0.410 at the two that divide it, alike on the four compilers.
Two things that adds here. It is outside this harness entirely — no criterion,
no shape set, no forcing term — so the pad probe's verdict no longer rests on
one instrument. And it names the condition: that loop carries four independent
accumulators and is fetch-bound, where the first attempt at the reproducer
used one accumulator with each iteration waiting on the last and measured
**no** difference at any position. So a straddle costs where the processor is
fetching ahead and is free where it is waiting — a sharper statement of scope
than two arms here could reach, and a candidate for why 1.19 here is smaller
than 1.58 there, the run-fill copying memory rather than only adding, though
nothing here measures that.

**Its LLVM backend does align them, which makes this a backend choice rather
than a property of the compiler.** `-fllvm` emits that same `.p2align 4` above
the inner loop header, on all four of those compilers, and `-optlc
-align-loops=64` (bytes) or `-optlc
-x86-experimental-pref-innermost-loop-alignment=6` (log2) raises it to 64,
each checked by reading the directive that came out. Read it rather than
trusting it: these feed a heuristic, and
`-x86-experimental-pref-loop-alignment` at 5 and at 6 gave 64 and 4 bytes.
What it would cost is a whole regime, `-fllvm` being a different code
generator that no figure here would survive; what it would buy is the first
regime in which layout is controlled rather than measured around, and in which
the identical-code pair must read 1.00.

**`-fproc-alignment=64` pins the offsets, which is the instrument fix**
(2026-08-10; the pad0, pad1 and pad2 sources rebuilt with and without it and
the offsets read out of the binaries — a claim about layout, so no quiet
machine is involved). Without it the four copies walk 24 bytes a pad: `[3, 53,
59, 45]`, `[27, 13, 19, 5]`, `[51, 37, 43, 29]`. With it all three builds read
`[3, 53, 3, 53]`, and the `mut-odo-vecdims` family `[8, 8, 4, 4]`. A
membership change no longer rerolls layout, which is the confound that made
Run 9's question unanswerable and this probe necessary. It does more than pin
them: the two procedures holding the copies are then 64-aligned and internally
identical, so the paired arms land on the *same* offset and the pair is
layout-neutral by construction. Two things it does not do. It freezes this
pair at 53, which straddles — the variance goes, the penalty stays, and the
offset frozen at is set by the procedure's own internals rather than chosen.
That the option stops at functions is deliberate and known: GHC
[#14701](https://gitlab.haskell.org/ghc/ghc/-/work_items/14701) has the person
who added it saying loops could be done too and were not looked at closely.
**It is now timed, and it is free on the baseline** (2026-08-11, a filtered
`*/list` pass over the shape set on each of three binaries, 24 benches each,
quiet machine). `.text` grows 0.14% and `list` does not notice: per-shape
geomeans of **0.9993** for the flag's build against `micro-unaligned` and
0.9997 for `micro-aligned` against the same, both scattering ±2 to 3.5% per
shape. So the insusceptible arm stays insusceptible under either
intervention, which is what licenses reading a ratio out of any of these
builds — and it reproduces Run 10's fifth prediction in a second setting, a
one-bench process rather than a full roster. The rebuilt binary's offsets are
the `[3, 53, 3, 53]` and `[8, 8, 4, 4]` recorded above, read out again, and
its `check` log is byte-identical to `micro-unaligned`'s: `cabal build micro
--ghc-options='-fspec-constr -fproc-alignment=64' --builddir=dist-procalign`,
the fresh builddir being what forces the rebuild a value-carrying flag does
not.

**The loops can be aligned outright, though, by standing in for the
assembler** (2026-08-10). `-pgma` replaces the program GHC assembles with, so
`align-as.py` beside this file rewrites the `.s` on the way past: every local
label that a later instruction jumps backwards to — which is what a loop head
is in the NCG's output — gets a `.p2align 6`. On this suite that aligns 395
heads and puts **every copy of both fills at offset 0**, grows `.text` by
0.13%, and leaves `micro check` green, 45 shapes agreeing and none dissenting.
So the straddle can be removed rather than merely frozen, and with it the
penalty — which turns the whole finding into a two-bench question ([the open
list][open]).

**How far it gets is a thing to measure and not to infer**, the shim's own
count of 395 being labels in the assembly it was handed rather than loops in
the binary that came out. `loop-offsets.py --survey` counts the population
that matters — self-loops no longer than a line, in this suite's own compiled
code, since only those can be rescued by an offset and everything longer
spans several lines in any build. It reads 115 such loops in `micro-unaligned`,
**50 of them straddling and one at offset 0**, against 101 in `micro-aligned`
with **100 at offset 0 and none straddling at all**.

**Those two populations are not the same size, and the difference is the
disassembler rather than the binary** (2026-08-11, and it corrects how the
two counts above may be read). Lifting the survey's own 64-byte cap, Main's
resolved self-loops go 144 to 125 across *every* span bucket, not just the
short one — which rules out the obvious account, that padding inflated loops
past a line, since the 65-to-128 bucket falls too, 20 to 16. Counting one
level further back says what happened: Main's code carries **1580** backward
jumps in the unaligned binary and **1583** in the aligned one, so the loop
structure is untouched, as it must be for a shim that only inserts alignment
directives. What moves is resolvability — targets not decoded as an
instruction start go **613 to 777** — because `objdump -d` sweeps linearly and
tables-next-to-code interleaves info tables with instructions, so shifting
code by arbitrary NOP runs changes where the sweep mis-decodes and re-syncs.
So the fourteen missing short loops did not grow and did not vanish; they
stopped being visible to the instrument. Read *none straddling* as a
statement about a sample that alignment makes smaller, not about the binary,
and take the completeness question to the assembly instead, where the shim
works and there is no decoding ambiguity: it knows which 395 heads it
aligned, and the heads it skipped are exactly those whose preceding line was
not an instruction. That is the form in which the claim below is sound, and
the survey is corroboration rather than the evidence.

The heads the padding
rule skips, the ones a table sits in front of, are not loop heads that would
have straddled here: for short loops in the code this page compiles, the
alignment is complete rather than partial. What it still does not reach is
the libraries, `vector`'s loops among them, which no `-pgma` on this build
touches.

**Pad only between two instructions, which is what the first attempt did
not.** Aligning every backward-jump target, 928 of them, produced a binary
that failed `check` on the first shape with `index out of bounds
(-1378,324)`. Tables-next-to-code puts an info table immediately before a
return point, which is a local label too, and a `.p2align` inserted there
separates the table from the code it belongs to. Requiring the preceding line
to be an instruction fixes it, at the cost of the loops whose head follows a
table — none of which this page measures. It is also why `check` is the gate
to run on such a build and the offsets are not: the offsets looked right in
the broken one.

**And a trap that would have ruined that experiment silently**, on all four
of those compilers. GHC does not
count `-fproc-alignment` as a flag change, so an incremental build that only
adds or drops it keeps the old object code and says nothing: `ghc -O1` then
`ghc -O1 -fproc-alignment=64` leaves a byte-identical binary, where adding
`-fforce-recomp` gives a different one. Cabal is not at fault — it reports
`(configuration changed)` and re-invokes GHC every time, and the same toggle
on `-fspec-constr` recompiles with `[Optimisation flags changed]`.

**And the trap is far wider than the flag that found it**, which is what makes
it a standing rule here rather than a note about one probe. Recompilation
checking hashes boolean `GeneralFlag`s and a fixed list of fields, so every
setting that carries a *value* is outside it — `-pgma` and `-optlo`/`-optlc`,
the inliner's `-funfolding-use-threshold` and `-funfolding-fun-discount`,
`-fmax-worker-args`, `-fdmd-unbox-width`, and **`-fllvm`**, so that switching
the whole code generator reuses the native backend's objects in silence. All
of them confirmed missed on all four compilers, and that list is a floor: it
is what one test module could exercise. So **any A/B on this page that toggles
a flag must force the rebuild** — `-fforce-recomp` or a fresh `--builddir` —
and the regime comparisons already run that way only because they were built
in separate trees. The first round of the alignment experiment had neither and
read its flag as inert. Written up as
`docs/ghc-issue-recompilation-ignores-codegen-flags.md` in horde-ad, beside
the block-pool issue and in the same form, and filed from there as [GHC work
item 27667](https://gitlab.haskell.org/ghc/ghc/-/work_items/27667) — that file
carries the cause in GHC's own source and the list of settings, and is the
copy to read.

**What is comparable across an alignment change, and what is not.** `list` is
the one arm measured insusceptible to placement — 0.9949, 1.0019 and 1.0031
across the rebuild probe's four binaries — so the denominator of every ratio
this page publishes, and the absolute anchor cells beside them, stay
comparable across the change. A susceptible arm's absolute figure does not,
which is why an aligned build wants a column of its own beside the regimes
rather than a splice into one: folding aligned figures into `-fspec-constr`'s
column would reintroduce in silence the term that alignment exists to remove.
And once an aligned build is the standing regime, the per-shape record a later
run compares against is taken from *it*, a fingerprint kept from an unaligned
run passing the layout term forward into every run that reads it.

**An aligned figure read against an unaligned one is a diagnosis, not a
continuation.** An arm that moves between the two has had its old figure's
layout term subtracted, which is neither a regression to explain nor the
roster doing something, and it wants writing up in those words. Such a pairing
also carries its own control, and the control is `list`: it is predicted not
to move, and if it does then the baseline was carrying layout too, every
published ratio has been divided by a moving denominator, and that is a larger
finding than whatever the pairing was run for.

**And the identical-code pair collapsed across all nine populations at once
when the loops were aligned**, which is the strongest single result the
pairing gave. On Run 9, one unaligned binary throughout, `build`/`mut-odo`
ran 1.078 (`window`) to 1.375 (`bcastmid`), above 1 in every population, with
`build` slower on 39 of the 43 shapes between them. On Run 10's aligned half
it runs **0.9148 (`revsome`) to 1.0335 (`reshape1`)**, below 1 in eight of
the nine. So a 30-point spread that was above 1 everywhere became a
12-point band around it, in nine populations measured in nine separate
processes, and the only thing changed was where the loop sits in its cache
line. Two things it does not do. It does not close the pair — 3% survives on
the main set — and the one population that inverts is `reshape1`, where both
arms are twenty-seven times slower than the class's leaders and whatever
separates them is not the loop the shim aligned.

**And a probe has since priced the rebuild itself, which is what neither the
twins nor that pair measure.** Four binaries built from sources differing
only in inert pad arms, the run filtered so the pads never execute, leave
`list` inside 0.5% and move `mut-odo` and `offtab` by up to 18% ([the open
list](#what-is-open) carries the figures). So this page
has three uncertainties of quite different size and only the smallest is on
the table above. An arm against **itself in one binary** is the A/A twins,
1.00% on Run 10's unaligned half and 0.54% on its aligned one. Two
**different arms in one binary** carry placement, which `build`/`mut-odo` put
at 14-24% for a pair whose code is identical — **until the loops were
aligned, which takes it to about 3%**, and to a tie by the sign test whenever
the two copies share an offset. One arm
across **two binaries** carries the rebuild, up to 18% on a susceptible arm
and almost nothing on an insusceptible one. Susceptibility is a property of
the arm and has been measured for three of them, so for the rest it is
unknown; what that protects is orderings and tiers, which several arms
witness at once, and what it does not protect is any single arm's figure read
across a rebuild.

**And the third of those is a bias, not a floor, which is the distinction to
keep.** A floor is a threshold below which a margin might be noise, and it
shrinks as samples accumulate; this does not. Each binary's figure is
*correct for that binary* — the four-binary rebuild probe's cells are
geomeans over 24 shapes with per-cell intervals of a fraction of a percent —
so collecting more samples inside one build cannot reduce it, and only
averaging over several builds would. The per-shape picture says the same:
across rebuilds `list` scatters 2.2-2.5% per shape while its geomean holds to
0.5%, where the two susceptible arms scatter 5-10% per shape *and* move their
geomeans. So do not
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

The floor grows with the margins, and for the same reason: subtracting a term
common to both arms magnifies their disagreement exactly as it magnifies a
real difference. On raw slopes Run 10's unaligned six read 1.0008 and 1.0038,
1.0027 and 1.0033, 1.0066 and 1.0035 — adjacent and distant per strategy —
so the largest deviation is 0.66% before the correction and 1.00%
after it, and every one of the six grows. Correcting the table without
correcting the floor would have been the whole error.

**And it was re-checked at full budget on Run 10, over four populations at
once** (2026-08-11). Predicting each A/A pair's net deviation from its raw
one as `1 + raw/(1-f)`, with `f` the forcing term's share of that arm's own
slope, reproduces all **24** pairs of the main set, `window`, `bcastmid` and
`scaled` to a few hundredths of a percentage point — 5.36% predicted 5.29%,
0.54% predicted 0.67%, and the rest closer. Two things that buys. The
amplification is arithmetic and not a second effect, confirmed on a run
rather than inherited. And it says **why the `mut-odo-vecdims` slot keeps
carrying the worst pair**: `f` is largest for the fastest fill, 0.598 against
0.296 for `bq-expand` in the same `scaled` process, so that arm amplifies
whatever raw disagreement it has by 2.49x where its neighbours amplify by
1.42x. The raw disagreement is still the larger factor there — 2.13% against
0.17% — so this explains part of a pattern rather than dissolving it.

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
them, and the four runs disagree several-fold: Run 9 was the tightest and the
wildest at once, five pairs inside 0.07% and one cell at 41%, where Run 10 is
uniform instead — every pair inside 1.00% unaligned and 0.54% aligned, worst
cells 11.2% and 7.7%. Expect either shape rather than a constant. So the
threshold to quote is the running one, and it is the run's own number and not
a tenth of a percent that a margin has to clear.

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
purpose: an arm against itself in one binary is the A/A twins, 0.54% to 1.00%
on Run 10 and 0.07% on Run 9; two
different arms in one binary carry placement, which `build`/`mut-odo` put at
13-24% for a pair whose code is identical and put at about 3% once both
copies are aligned; one arm across two binaries
carries the rebuild, up to 18% on a susceptible arm; and one arm across two
*process populations* carries the warming, 35-40% on the expansion family at
`vgg-14-c512-k3`. The last is the largest, and the second is the one this
page has learned to remove rather than only price. So when a sentence
compares something new — two populations, two machines, two GHC versions, an
arm against a prediction — ask which of these bounds it, and if none does,
say so in the sentence rather than borrowing the nearest number.

**Each population measures its own floor.** The same six controls ride every
process, so a stride-class run prices the noise of the process its own
figures came out of — which is the only process they can be judged in — but
it prices it over two or three cells where the main set has two dozen. Read a
class's controls as this floor confirmed there or not, rather than as a
threshold of that class's own, and never carry the main set's figure into a
class comparison or the other way about. Run 10's class processes are that
ruling observed: floors from 0.16% (`rev`) up to 5.36% (`scaled`), a
**thirty-fourfold** spread across populations of one run, where Run 9 spread
fifteenfold and Run 8 differently again. The `mut-odo-vecdims` slot
carries the worst pair in **five** of the eight — `revsome`, `bcastmid`,
`reshape1`, `window` and `scaled` — where Run 9 put it in four and Run 8 in
seven; `bq-expand`'s pairs take the other three and
`bq-scan-rem-gm-mulback`'s take none. Four runs at four counts is not a
pattern settling, but the amplification above says the slot is not neutral
either: `f` is largest for the fastest fill, so that arm converts a given raw
disagreement into a larger published one than any other pair in the same
process. Read the recurrence as partly arithmetic and partly unexplained,
and read a class's floor as the run's own.


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
rather than merely noisy. In Run 10 (SpecConstr) the unaligned half has 1
cell of 816 in the main set — `bq-expand-zf` on `stretch-inner256` at
0.9877, **the same arm and shape for the third run running**, which makes it
a property of that pair rather than of a run — while the aligned half has 3,
worst `bq-expand-gm-mulback` on `stretch-square-1341` at 0.9800, and two
class processes add one each (`build` on `reshape1-r3` at 0.9886,
`gen-quotrem` on `slice-cnn-L2-24x24-c32` at 0.9751). Run 9 had one and no
class cell, Run 8 one plus `build` on `bcast-tall-Mx2`, Run 7 two
and six, five of its six on `bcast-inner900` where the scan family ramped
re-reading a 2000-element backing with 1.8M elements; those are gone, in the
regime that takes the same family's allocation to the table. Alignment
therefore does not reduce curvature and may add a little, which is a
different axis from the noise it leaves alone (its median CI% is 0.138
against the unaligned half's 0.134 over the same 816 cells).

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
`noise` figure by far; it did not recur on Run 8 or Run 9, that arm reading
an ordinary 1.01 on the latter — **and it is back on Run 10, larger, and
largest of all on the half where the arm is fastest**. `mut-odo` reads 2.40
unaligned and **4.51 aligned**, the noisiest bench of that process, ahead of
`list` (3.59), `gen-unsafe` (3.43) and `gen-quotrem` (3.36); on the unaligned
half the first-attempt arms still lead it, `gen-unsafe` at 5.57 and
`gen-quotrem` at 3.48. For scale, `concat-runs` was dropped from the timed
roster at 2.45. So the earlier reading — that whatever the flag does to this
arm, it does not do it by making the bench noisy — no longer holds: removing
12% of its time by aligning its loop left it noisier than anything else in
the process, and nothing here explains why. **Positional or
strategy-intrinsic is the question to ask
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
   list](#what-is-open) carries what would settle it.

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


## About the last run (Run 11)

**Run 11 (SpecConstr), and the exact repetition this page has been owed since
Run 9.** Criterion, GHC 9.12.4, **`--ghc-options=-fspec-constr`**; Run 10's
regime, Run 10's roster in Run 10's order, Run 10's shapes — and Run 10's
aligned binary itself, byte for byte, md5
`a28b3e5b1c409cec6cca64de9f46bb4d` against the note that run left behind. So
shapes, roster, regime *and layout* are all pinned, which no previous run
here could say, and anything that moves between the two is run-to-run drift
and nothing else. The pairing continues, with a different second half:
`micro-maxskip` emits a directive at the same 395 loop heads and lets the
assembler act on one only where the loop would otherwise cross a cache line
it need not, so it carries a third of the padding for the same zero misplaced
heads ([the floor section][floor]). What separates the two is how many NOPs
they contain and nothing else an offset can see, and two load-independent
checks say so after the fact as well as before: `size` puts both text
segments at 20791127 bytes, the maxskip half having been padded to the
aligned one's size and phase, and the fitted allocation agrees on **768 of
768** cells to a worst 1.7e-05 and a median of exactly zero, between the
halves and against Run 10 alike. From
`Main.hs` at commit `2b41e53` — the tree at `c37abfe` for the maxskip half, a
comment apart — on the same desktop, Zen 3, a Ryzen 7 5800X. Both main
processes' stderr provenance lines read *roster 34 benchmarks over 24 shapes;
elapsed 1h10m16s; peak 220 MiB in use, 74 MiB max residency*, the aligned
half two mebibytes under it, comfortably inside `micro.cabal`'s `-M2G`.

**The flag was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts
`baseOffsetsScan` at 2408938 bytes against `baseOffsetsMut`'s 2408530 on
`vgg-14-c512`, where plain -O1 separates the two tenfold. A run made in the
wrong regime passes every gate this page has and reads as a refutation of the
design it was built to test, so [the
procedure](#making-a-major-benchmark-run) puts that check before the run and
this line records that it was made. Both figures are Run 10's, Run 9's and
Run 8's to the byte, which is the instrument saying it did not move — and on
a run whose basis half is Run 10's own binary that is a tautology worth
keeping anyway, since it is the check that would have caught the binary not
being the one the note names.

**The baseline did not move, in either direction it could have.** `list` per
call reads **1.0025** against Run 10 over the 24 shapes, on the binary that
run used, so the two runs share a denominator and a ratio may be held against
its predecessor directly; and it reads **1.0066** aligned over maxskip, so
the two halves share one too. The second is the pairing's own control, and
what it says here is narrower than what alignment's control said: the shim's
padding reaches the baseline for two thirds of a percent, `list`'s own hot
loop being library code the shim never rewrote ([the floor section][floor]).
Every arm-over-maxskip figure below is an absolute time and owes that nothing;
a published *ratio* has it in both numerator and denominator.

**Drift, with everything else pinned, is a quarter of what the page has been
bounding it at.** `list`'s per-shape scatter against Run 10 runs **0.958 to
1.043** where Run 10 against Run 9 ran 0.902 to 1.181 — the same arm, the
same shapes, and this time the same binary, where that run had moved
`sum-only-early` above `list` and rerolled every alignment with it. Over the
whole roster the picture is the same: of 762 cells compared, 495 are within
1%, 693 within 5% and 743 within 10%, and every arm's geomean is within 1.5%
of its Run 10 self bar `mut-odo` at **1.0327**. So the span this page has
quoted for eight runs as *what a figure may do between runs for no reason at
all* was mostly the reason it could not see, and the residue is smaller.

**Two arms drift where placement can no longer be the account, and they are
one worker.** `mut-odo` is the only arm whose geomean leaves 1.5%, at
**1.0327**, and its code twin `build` holds the two widest cells of the
repetition after the wild one, 1.2471 and 1.1701, with `mut-odo`'s own at
1.1577 and 1.1467 — and their loops are at offset 0 in both runs, this being
the same binary. Run 10 read the pair's ends as a placement span and
[the floor section][floor] priced it; here there is no placement to price, and
the two arms that share `vBuildVS` are still the ones that move. What that
leaves is a per-run term neither alignment nor the roster order reaches.

**What the pairing measures now is the shim's own cost, and max-skip is the
cheaper build nearly everywhere.** Against the fully padded half, arm over
arm, nothing reads below 0.99 but `build` (0.9896), while `bq-mut` reads
**1.0588** with the maxskip half ahead on 23 shapes of 24,
`mut-odo-vecdims-add-out` 1.0513, `bq-gen` 1.0504 and
`mut-odo-vecdims-add-both` 1.0333 — the aligned build slower each time, by
the NOPs an arm executes when it falls through into a head that did not need
aligning. `build` and `mut-odo` are unmoved, at 0.9896 and 1.0221, which is
what both halves putting their executed copies at 0 predicts: the 12 to 14%
Run 10 measured on those two is bought by both builds here and separates
neither. **The four vecdims copies split two and two, as the pair note said to
read them**: `mut-odo-vecdims` (1.0074) and `-add-both` (1.0333) keep the
whole of the NOP cost Run 10 measured for them (1.0069, 1.0326), their copies
having been left where they fell, while `-add-in` (1.0036) and
`-add-both-down` (1.0029) shed most of theirs (1.0143, 1.0443), max-skip
having moved the two copies that straddled. So a third of the padding buys
every misplaced head the unconditional shim buys, and gives back most of what
it charges for the ones that were already resident.

**One cell of the run is 35% wrong, and finding out which is the repetition's
own doing.** `lenet-L1-28-c1-k5/bq-expand` reads 1.355 of what the same
binary read in Run 10 and of what the maxskip half read in the hour before,
while that arm's two A/A twins — its own code under two other names, in the
same process — read within 1% of both. **Criterion's own printed `time`
lines say it without the reader**: 68.32 µs (68.28..68.37) for the arm
against 53.89 µs (53.88..53.90) for its adjacent twin, in one process, on
intervals of a twentieth of a microsecond, where the maxskip half puts the
two at 53.46 and 53.49. It is not the machine: the benches either side of it
in run order are within 1.2%, the cell is measured to CI% **0.06** over 125
samples on one of the run's tightest shapes, and `list` on that shape moves
0.1%. An intrusion widens an interval and does not stop at one bench of five
seconds — which this run can say from measurement rather than from argument,
a disturbed process of its own having been read before it was discarded
([the floor section][floor]). This is the third sighting of the effect Run 8 and
Run 9 recorded at 44% and 41.4% and ran down to a cold block pool at a roster
slot ([the floor section][floor]), and the first with the sides swapped: the
base arm's own slot carries it and both twins are clean, where Run 9's twin
carried it and its base was clean. So the fix that removed it — lifting
`sum-only-early` above `list`, which Run 10 confirmed at full budget — did
not remove what causes it. **Every figure this page states for `bq-expand`
therefore carries a cell that a repetition says is 35% out**, which the
winsorized estimator caps and the claims below quote around: with the shape
set aside, each of them lands within about a point of Run 10's.

**Run 11 records every population**: the main set from both halves and the
eight stride classes from the aligned one, one process each,
so its provenance lines are one per process: the main set's at this head, each
class's beside its own table in [The stride classes, run by
run](#the-stride-classes-run-by-run). The regime, the machine and the commit
are the whole run's and stay here, stated once. **The classes ran in a later
window than the main sets**, the machine having been wanted in between — a
separate hour on the same idle desktop, `rev` alone excepted, which ran in
the main sequence. One process per population is what makes that harmless:
each carries its own six A/A controls, its own `sum-only` pair and its own
two `-nosum` arms, so it passes or fails the three gates on its own evidence
and owes nothing to what shared the machine with it. It is recorded because
the run's own arrangement is what a repetition is read against.

**The page it leaves is one basis throughout**, which Run 10's was not: the
Results table, the per-shape fingerprint and every class block below are the
aligned half's, and what the other half contributes is the yardstick's second
column and the arm-by-arm comparison above. The mixed-basis apparatus Run 10
needed is spent, and the sentence that survives it is that *the aligned half
is the table and the second half is the control*, whatever the second half is
built to price — layout for Run 10, the shim's own padding here.

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
`Data/Array/Internal.hs` compiles under, and a row's distance from Run 10's is
drift and not a strategy's, the flag, the roster, the order and the binary
being the same ones.

**And it is the aligned half's**, as every published table here is from this
run on: the maxskip half's column is one column on the yardstick below rather
than a second copy of these thirty-odd rows.

**Comparing runs?** The table below is Run 11's own; what to hold a new run
against is [What Run 12 compares against](#what-run-12-compares-against), the
claims to test are [the ones after it](#the-claims-run-12-should-test), the
population and the absolute anchor are in [Provenance](#provenance), and this
run's own floor — 0.22% on the maxskip half, and 0.33% on four of the aligned
half's six A/A pairs against 1.21% on all six — is [in the floor
section][floor]. That floor governs an arm against *itself*; two different
rows of the table below are separated by their code, and in an aligned build
no longer by where each landed — which is what the previous run spent two
binaries to establish and this one inherits.

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
  reproduced the refutation at full budget where a rough pass had found it.
  Re-derived on Run 9's cells and roster it is unanimous: **every one of the
  32 benched rows** varies by more than 5% from shape to shape, the median
  row by 2.00× and the worst by 5.10× (`bq-expand-b`, 1.00× to 5.10×), and
  the four shapes of identical `l` = 1800000 give `bq-expand` 2.000×,
  2.111×, 1.000× and 2.639×. The spread narrowed as the roster was cut —
  Run 6's worst was an arm nothing times any more — and the property it
  measures did not. Every allocated fit sat at R² 1.000 on Run 6, so the
  spread is the quantity and not the measurement, and allocation being
  deterministic per call the budget does not bear on it either way.
  What does survive is the column: a median over a *pinned* shape set
  reproduces, which claim 7 now carries on a live basis, every allocation
  tier returning on its own level across a roster change. So read `alloc` as a
  statistic of a strategy **and** a shape set, and pin the shape set before
  comparing it across runs, exactly as the `time` column already asks. It is
  the one column the correction does not touch.

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.18* | *80* | *2.35x* | *its base arm, forced with one element* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *92* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *102* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *102* | *0.00x* | *the same, at the other end* |
| mut-odo-vecdims-add-in | 0.048 | 0.112 | 0.11 | 82 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.102* | *0.05* | *82* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.048* | *0.101* | *0.10* | *82* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.048** | 0.102 | 0.05 | 82 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both-down | 0.051 | 0.121 | 0.14 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both | 0.054 | 0.127 | 0.11 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-out | 0.056 | 0.133 | 0.12 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.081 | 0.224 | 0.18 | 83 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.087 | 0.232 | 0.20 | 82 | 1.33x | mutable `Int` scratch |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.089* | *0.160* | *0.08* | *76* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.089* | *0.159* | *0.04* | *76* | *1.33x* | *A/A control* |
| **bq-scan-rem-gm-mulback** | **0.089** | 0.162 | 0.07 | 76 | 1.33x | nothing (pure) |
| bq-odo-gm-mulback | 0.090 | 0.180 | 0.17 | 80 | 1.51x | nothing (pure) |
| bq-expand-gm-mulback | 0.094 | 0.226 | 0.16 | 82 | 2.35x | nothing (pure) |
| bq-mut-runs | 0.095 | 0.233 | 0.22 | 76 | 1.33x | mutable `Int` scratch |
| build | 0.096 | 0.292 | 0.44 | 72 | 1.00x | new mutating `Vector` method |
| bq-expand-b | 0.101 | 0.228 | 0.09 | 76 | 2.18x | nothing (pure) |
| *bq-expand-aa-adjacent* | *0.102* | *0.227* | *0.10* | *76* | *2.35x* | *A/A control* |
| bq-expand-qr-prim | 0.102 | 0.228 | 0.15 | 76 | 2.35x | nothing (pure) |
| *bq-expand-aa-distant* | *0.102* | *0.227* | *0.04* | *76* | *2.35x* | *A/A control* |
| mut-odo | 0.103 | 0.345 | 0.82 | 70 | 1.00x | new mutating `Vector` method |
| **bq-expand** | **0.103** | 0.227 | 0.12 | 76 | 2.35x | **nothing -- SHIPPED** |
| bq-expand-zf | 0.105 | 0.248 | 0.17 | 75 | 2.35x | nothing (pure) |
| offtab-scan-rem | 0.119 | 0.241 | 0.19 | 73 | 2.00x | nothing (pure) |
| offtab | 0.125 | 0.350 | 0.70 | 68 | 2.00x | mutable `Int` scratch |
| bq-mut | 0.148 | 0.369 | 0.36 | 64 | 1.33x | mutable `Int` scratch |
| bq-gen | 0.336 | 2.176 | 0.49 | 51 | 1.33x | nothing (pure) |
| gen-quotrem | 0.905 | 3.417 | 0.65 | 41 | 1.00x | 1st attempt |
| gen-unsafe | 0.910 | 3.450 | 0.48 | 42 | 1.00x | -- |
| list (baseline) | 1.000 | 1.000 | 0.60 | 37 | 23.51x | -- |

`concat-runs` has no row, and neither do the other 23 arms the roster holds
and checks without timing: the reason is at each entry and the count is
[`--lint`'s](#the-reader-read-runpy). No row here is a first reading, the
roster's membership being Run 9's exactly, so every movement below is a
movement and not a new arm arriving.

**Three things in the table are the run's findings rather than its numbers.**
**The table reproduced**: every row the yardstick below carries is within a
thousandth of the aligned column Run 10 published, and **the ceiling
reproduced to four digits** — `mut-odo-vecdims` against the fastest pure arm
reads 0.5428 paired at 23 wins of 24, sign p 3e-06, which is Run 10's cell
and win count exactly, where Run 9 read 1.87×, Run 8 1.68× and -O1 1.80× on
the figure [the ruling](#the-mutable-ceiling-not-taken) turns on. **And
allocation reproduced to the cell, for the third run running**: 768 of 768
agree to a worst 1.7e-05 and a median of exactly zero, between the halves and
against Run 10 — the mutable fills and `gen-quotrem` at 1.00x, the scan
family and `bq-mut` at 1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x,
`bq-expand` 2.35x and `list` 23.51x. Neither alignment nor the shim's padding
was expected to touch it and neither did, which is what makes the column the
first thing to read when anything else moves.

**The third is about the instrument, and it is the repetition's alone to
find: three quarters of a percent moved a sign test from a tie to p
0.00028.** `mut-odo-vecdims-add-in` against the arm it varies read 1.0009 at
13 wins of 24 in Run 10 and reads **0.9934 at 21 of 24** here, on one
binary, one roster and one order. The geomeans differ by less than this run's
own floor and agree about the size of the margin; what moved is which side of
zero the per-shape differences fell on, twenty-four near-ties being able to
break either way. So a sub-percent margin's **win count is not more stable
than its geomean**, which is worth having said plainly, the sign test being
what this page reaches for whenever the baseline is in doubt.

**And one of Run 10's orderings needs restating rather than replacing.** That
run put both plain mutable fills past `bq-expand` on the aligned half,
`build` at 0.9367 of it and `mut-odo` at 0.9671; this run reads 0.9318 and
0.9842, so the point estimates reproduce. But the win counts are 8 and 9 of
24 there and 10 and 9 here — the fill ahead on the geomean while behind on
most shapes, which is what a few large wins against many small losses looks
like, and what a sign test is for. Read the pair as *the fills win big where
they win*, and not as an ordering: at p 0.54 and 0.31 there is nothing here
to order.


### What Run 12 compares against

**Run 12's regime and roster are open** — what Run 11 settles is what it costs
to inherit them: with shapes, roster, order and binary all pinned, a row moves
by a thousandth and a cell by a few percent, so a run that inherits them
inherits a basis it can subtract from rather than merely order. The table
below is read against the two Run 11 columns; the -O1 column stays the
yardstick for any future return to that regime, and the two sets of claims
differ in more than their numbers.

**Run 11 contributed two columns, and the second names a shim rather than a
build.** `Run 11 (SpecConstr, aligned)` is the basis, and is Run 10's aligned
binary run again; `Run 11 (SpecConstr, max-skip)` is the same source and
compile with the assembler shim padding only the heads that needed it. The
rule against pruning a column is joined by one against **merging** two:
folding two halves into one column would put back, in the one table built to
outlive every artifact, exactly the term the pairing exists to separate.
`--check-doc` catches one half of that: a run named aligned must also be named
unaligned, so pruning Run 10's unaligned column fails it. Pruning an aligned
column, merging two, and naming a second half accurately are the reading's to
catch — the check cannot demand an unaligned half of every pair without
failing this run, which has none, nor an aligned column of every run without
failing Runs 6 through 9, which had none either.

**What each pair of columns is for differs, and the table cannot say so
itself.** Run 10's two are one source and one compile apart and price
**layout**: 12 to 14% on the two arms whose loop straddled a cache line, a
percent or two the other way where none did. Run 11's two are one *shim* apart
and price what that padding costs when it rescues nothing: nothing below 0.99
and up to 1.06 against the fully padded half. Reading Run 11's aligned column
against Run 10's aligned one is the third thing again — the same binary twice,
which is drift and nothing else.

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

| strategy | Run 11 (SpecConstr, aligned) | Run 11 (SpecConstr, max-skip) | Run 10 (SpecConstr) | Run 10 (SpecConstr, aligned) | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | **0.048** | **0.048** | 0.048 | 0.049 | 0.048 | 0.053 | 0.054 |
| `mut-flat-gm` | **0.081** | **0.081** | 0.083 | 0.081 | 0.080 | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.087** | **0.086** | 0.085 | 0.088 | 0.088 | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.090** | **0.090** | 0.090 | 0.090 | 0.090 | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.089** | **0.090** | 0.090 | 0.089 | 0.090 | 0.090 | 0.119 |
| `bq-expand` | **0.103** | **0.103** | 0.102 | 0.102 | 0.105 | 0.102 | 0.127 |
| `build` | **0.096** | **0.100** | 0.110 | 0.096 | 0.114 | 0.095 | -- |
| `offtab` | **0.125** | **0.123** | 0.123 | 0.124 | 0.115 | 0.146 | -- |
| `mut-flat` | -- | -- | -- | -- | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | -- | -- | -- | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | -- | -- | -- | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | -- | -- | -- | -- | 0.108 | 0.097 |

All seven columns are published geomeans over the same 24 shapes. The first
five share a denominator as well — `list` moved 0.7% between the two Run 11
columns, 0.25% between the first and Run 10's aligned one, and 0.6% and 0.4%
inside Run 10 and against Run 9 — so they may be subtracted and not merely
ordered, which is what the -O1 column cannot do at an 8% baseline shift. Read
the two Run 11 columns against each other for the **padding term**: `build`'s
0.096 against 0.100 is the same arm in the same run, one shim apart. Read the
first column against Run 10's aligned one for **drift**, everything else
being pinned: eight rows within a thousandth, which is the tightest thing
this table has ever been able to say. Read the two Run 10 columns against
each other for the **layout term** — `build`'s 0.110 against 0.096 — and the
-O1 column for orderings only.

**Each stride class's yardstick is its own table below.** Run 8 re-ran every
class with the populations pinned, and every run since has again, so each
class's paragraph carries what the last change moved and the table above it
is what Run 12 reads against. **Both sides of every class comparison are
aligned from here**, Run 10's tables having been the first aligned ones and
read against unaligned predecessors, which was diagnosis rather than
continuation ([the floor section][floor]).

And because a geomean cannot say *where* it moved, the **fingerprint**
below is kept so a future disagreement can be localised rather than only
noticed. Its membership is a rule, not a habit: the shipped arm, the rows
the Results table bolds, and any arm an open question names — `mut-odo`
and `build` sit here on [the placement
question](#what-is-open), which they are now the answer to
rather than the sharpest form of — and an arm leaves when its question closes,
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
| `cnn-slice-c32` | 3 | 288 | 5.34 µs | 0.149 |
| `cnn-L1-6x6-c1` | 3 | 324 | 6.56 µs | 0.198 |
| `stretch-rank12` | 2 | 4096 | 98.3 µs | 0.227 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 102 µs | 0.171 |
| `conv1d-24` | 3 | 5184 | 88.7 µs | 0.106 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 323 µs | 0.175 |
| `gather48-src-50` | 3 | 22500 | 385 µs | 0.098 |
| `stretch-rank10` | 3 | 59049 | 1.26 ms | 0.133 |
| `stretch-coprime-r7` | 13 | 60060 | 1.01 ms | 0.105 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.29 ms | 0.107 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.63 ms | 0.113 |
| `stretch-primes` | 89 | 250357 | 3.54 ms | 0.101 |
| `stretch-inner1` | 1 | 500000 | 11.5 ms | 0.077 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 26.4 ms | 0.060 |
| `vgg-14-c512-k3` | 3 | 903168 | 29.6 ms | 0.090 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 16.3 ms | 0.104 |
| `stretch-inner256` | 256 | 1750784 | 47.7 ms | 0.069 |
| `stretch-pow2stride` | 64 | 1769472 | 51.3 ms | 0.066 |
| `stretch-r5-8x432` | 8 | 1769472 | 49.3 ms | 0.055 |
| `stretch-square-1341` | 1341 | 1798281 | 25.7 ms | 0.127 |
| `stretch-bigstride` | 3 | 1800000 | 41.5 ms | 0.071 |
| `stretch-tab7MB` | 2 | 1800000 | 33.7 ms | 0.097 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 35.7 ms | 0.071 |
| `stretch-wide-2xM` | 2 | 1800000 | 33.9 ms | 0.087 |

| shape | scan-rem-gm | vecdims | mut-odo | build |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 0.142 | 0.084 | 0.192 | 0.175 |
| `cnn-L1-6x6-c1` | 0.132 | 0.096 | 0.215 | 0.229 |
| `stretch-rank12` | 0.137 | 0.102 | 0.345 | 0.292 |
| `cnn-L1-24x24-c1` | 0.102 | 0.072 | 0.217 | 0.212 |
| `conv1d-24` | 0.106 | 0.062 | 0.165 | 0.134 |
| `lenet-L1-28-c1-k5` | 0.099 | 0.051 | 0.121 | 0.122 |
| `gather48-src-50` | 0.104 | 0.057 | 0.145 | 0.130 |
| `stretch-rank10` | 0.097 | 0.064 | 0.174 | 0.190 |
| `stretch-coprime-r7` | 0.086 | 0.033 | 0.061 | 0.055 |
| `cifar-L2-16-c64-k3` | 0.086 | 0.051 | 0.145 | 0.138 |
| `cnn-L2-24x24-c32` | 0.089 | 0.053 | 0.149 | 0.132 |
| `stretch-primes` | 0.094 | 0.029 | 0.030 | 0.030 |
| `stretch-inner1` | 0.077 | 0.099 | 0.284 | 0.250 |
| `alexnet-L2-27-c48-k5` | 0.053 | 0.025 | 0.059 | 0.054 |
| `vgg-14-c512-k3` | 0.058 | 0.034 | 0.099 | 0.090 |
| `alexnet-L1-55-c3-k11` | 0.094 | 0.035 | 0.059 | 0.058 |
| `stretch-inner256` | 0.052 | 0.015 | 0.016 | 0.016 |
| `stretch-pow2stride` | 0.075 | 0.068 | 0.068 | 0.068 |
| `stretch-r5-8x432` | 0.052 | 0.019 | 0.040 | 0.038 |
| `stretch-square-1341` | 0.162 | 0.089 | 0.091 | 0.088 |
| `stretch-bigstride` | 0.075 | 0.039 | 0.103 | 0.101 |
| `stretch-tab7MB` | 0.106 | 0.067 | 0.179 | 0.173 |
| `stretch-tall-Mx2` | 0.063 | 0.018 | 0.018 | 0.017 |
| `stretch-wide-2xM` | 0.104 | 0.066 | 0.176 | 0.160 |

Two rows to read first, and the pair is derived rather than remembered:
`stretch-square-1341` and `stretch-pow2stride` are the only two shapes where
**both** arms tying at the head of the pure tier *lose* to `bq-expand`, so
treat a disagreement on either as the shape. They fail differently, which is
why both are named. On `stretch-square-1341` the mutable fills win it back
outright (`mut-odo-vecdims` 0.089 against `bq-expand`'s 0.127) while the pure
arms trail; on `stretch-pow2stride` the two families converge instead, four
of the five fingerprint arms landing inside two thousandths of each other
([the per-shape section][pershape]). Taking the tier's leaders one at a time
gives seven shapes and three, which is why the sentence says both.
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.


### The claims Run 12 should test

**Run 11's verdicts on Run 10's nine claims first**, since a run reports
breaks rather than re-deriving the table. **Every claim held**, and on a run
this is the first time that sentence means what it appears to: shapes,
roster, order, regime and binary were all pinned, so a claim that moved would
have had nothing to move for. Figures below are the basis (aligned) half's.

**The nine reproduce to about a point, which is the repetition speaking
through them.** Every margin below is within 1.5% of Run 10's reading of the
same claim once `lenet-L1-28-c1-k5` is set aside, and the two shown side by
side are `bq-expand-b` / `bq-expand` at **0.9939** against 0.9943 and
`bq-expand-zf` / `bq-expand` at **1.0322** against 1.0325. That shape is set
aside because one of its cells is 35% out and the arm it belongs to is
`bq-expand`, which is the denominator of five of the nine ([the head of this
chapter](#about-the-last-run-run-11)); each claim it touches is given both
ways below, on 24 shapes and on 23.

**Claim 9's per-shape half survived a fourth run, and its geomean went on not
mattering.** `bq-expand-b` / `bq-expand` reads 0.9819 on 24 shapes at 11 wins
and 0.9939 on 23 at 10 — a tie either way, as in Run 10, where Run 9 read
0.9678 at 22 of 24 and Run 8 a tie at 0.996. `bq-expand-zf` / `bq-expand`
reads 1.0197 at 2 of 24 and 1.0322 at 1 of 23, behind as Run 10 had it.
**What is stable is the shapes**: after the wild cell, `bq-expand-b`'s two
best are `stretch-inner1` (0.920) and `stretch-wide-2xM` (0.931), the same
two named in each of the last four runs — the rank-2 views with one huge
outer dimension where seeding from `enumFromStepN` replaces the whole
`concatMap` build.

**Claim 1's middle link, which the halves parted over in Run 10, holds
without qualification.** `mut-flat-gm` / `bq-mut-runs-gm-mulback` reads
**0.9335** at 23 wins of 24, sign p 3e-06, where Run 10's aligned half read
0.9293 at 22 and its unaligned half 0.9708 at 15. The layout term that
separated those two is not in either of this run's halves, and the link reads
the aligned figure. The other two links hold at 0.5949 and 0.9762.

**Claim 2's second half kept its direction and its size, and lost its sign
test to the margin's own edge.** `offtab` / `bq-expand` reads **1.2166** at 7
wins of 24, sign p 0.064 — 1.2365 at 6 of 23 without the wild shape — against
Run 10's 1.2224 at 6 of 24, p 0.023. The point estimate reproduces to half a
point and the test moved from just inside to just outside 0.05 on one shape
changing sides, which is what a 24-shape sign test does at this margin. Read
the ordering as established, the 22% as reproduced, and neither p as the
finding.

**Claim 3 held.** `bq-expand-gm-mulback` / `bq-expand` reads **0.9105** at 20
of 24, sign p 0.0015, and 0.9214 at 19 of 23: a mul-back output is worth 8 to
9% on the shipped build under this flag, where Run 10 read 7.2%.

**Claim 4 is a tie on both its halves, as Run 10 left it.** Against its own
build control the scan reads **0.9511** at 15 wins of 24, sign p 0.31, on an
interval covering 1; against `bq-expand` **0.8659** at 17 of 24, p 0.064, and
0.8820 at 16 of 23. Both readings are the claim, and the second is again a
double-digit point estimate on a tied sign test — the shape of it that
invites quoting the point estimate alone.

**Claim 5 held.** `bq-expand` / `bq-gen` reads **0.3070** at 21 of 24, and
`bq-mut-runs` / `bq-expand` **0.9231** at 23 of 24, sign p 3e-06 — 0.9344 at
22 of 23 — where Run 10 had the second unanimous. Among the builds only the
mutable odometer still beats `bq-expand`.

**Claim 6 held and its alarm again had nothing to answer for.**
`gen-quotrem` / `list` reads **0.9050** at 12 wins of 24, sign p 1 — a tie by
the only test immune to the baseline — and the anchor the claim tells you to
check first is still: `list` moved 0.25% against Run 10.

**Claim 7 held to the cell, which is stronger than to the digit.** All 34
rows' multiples are Run 10's exactly and the cells behind them agree to a
worst 1.7e-05, in both halves. Allocation is deterministic per call, so this
is the column that says the two runs differ in nothing that changes what an
arm computes — which, the binary being the same one, is what it should say.

**Claim 8's structural half stands.** Every pure arm still runs its output
through the single in-order `vGenerate` over an `m`-length table, and the
arms that fall behind still lose on their table build; `bq-expand-zf` (0.105)
and `offtab-scan-rem` (0.119) still populate the gap to `bq-gen` (0.336).

Restated **on the aligned half**, for Run 12 to check; margins are paired
geomeans, past the floor unless marked, each claim carrying the reading it
rests on. **All of them are `-fspec-constr` claims**: a Run 12 at -O1 tests
Run 7's set instead, and the two sets differ in more than their numbers.
**And all of them are now read against a measured drift band rather than a
layout span**, which is the change this run makes to how the list is used. A
roster *order* change alone moved arms 0.966 to 1.142 between Run 9 and Run
10, and that is what a margin used to have to clear; with the layout pinned,
a repetition moves an arm by at most 3.3% and most of them by under 1.5%, so
a margin above a few percent is now evidence of a strategy. **In an aligned
build the layout stays pinned across a roster change**, no short loop of
Main's code straddling a cache line in `micro-aligned` where 50 of them do in
`micro-unaligned`. (Read those two as counts of straddlers within each
binary, which is sound, and not as a population one can subtract from the
other, which the floor section shows it is not.) A claim resting on an arm
whose own loop the shim skipped — `list`'s, which is library code — is still
decidable nowhere until that loop is read.

**The list needed no re-aiming this time either**, the roster it was
rewritten onto before Run 8 being the roster Run 11 ran: every claim below
names an arm this run timed, and each carries its own reading rather than the
previous one's. Three full runs on that roster is the evidence that keeping
the *question* and changing the *arm* was the right repair — the
unconditional counterparts were written so that dropping a precondition would
not drop a question with it, and none of them dropped one.

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` <
   `bq-odo-gm-mulback`, the whole ordering read on unconditional arms:
   0.5949 (22 of 24), 0.9335 (23 of 24, sign p 3e-06) and 0.9762 (19 of
   24, sign p 0.0066). The middle link is the one this page has seen a layout
   term move — 0.9708 at 15 of 24 on Run 10's unaligned half against 0.9293
   at 22 on its aligned one — and on a pinned layout it reads the aligned
   figure twice running. The ceiling's ordering has now survived three runs, a
   change of basis and a repetition.
2. `bq-expand` < `bq-mut` (0.6946, 20 of 24) while `offtab` is **1.2166**
   *behind* `bq-expand` (7 of 24, sign p 0.064): the `m`-length table beats
   both the mutable scratch that builds it and the `l`-length table that
   replaces it. Run 9 left the second of those at 1.0969, inside the layout
   span and undecidable there; Run 10 decided it at 1.2224 and this run
   reproduces the margin to half a point, its sign test sitting either side
   of 0.05 on one shape.
3. `bq-expand-gm-mulback` < `bq-expand` (0.9105, 20 of 24, sign p 0.0015): a
   mul-back output pays 8 to 9% on the shipped build under this flag.
   `bq-expand-lemire-out` — the arm the question used to be asked
   through — is untimed for its `l < 2^32` precondition and has no
   unconditional form, Granlund-Montgomery offering no `out` analogue that
   yields quotient and remainder together.
4. `bq-scan-rem-gm-mulback` ties its own build control
   `bq-expand-gm-mulback` (0.9511, 15 of 24, sign p 0.31, interval covering
   1) **and ties `bq-expand` too by the sign test** (0.8659, 17 of 24,
   sign p 0.064), where Run 9 had the second at 18 of 24 and called it
   outright. The two differ in `baseOffsetsScanRem` against
   `baseOffsetsExpand` and in nothing else, their output code being
   identical, so the first reading is about builders and the second about the
   shipped arm. Both readings are the claim; a 13% point estimate sitting on
   a tied sign test is exactly the shape that invites quoting the point
   estimate alone.
5. `bq-expand` < `bq-gen` (0.3070, 21 of 24): the build ordering, trimmed to
   its timed arms — `offsets-quot` and `bq-gen-lemire` were its two ends and
   are both untimed, so the run cannot re-read the gap widening or the
   ending. That refutation stands on Run 7 and Run 8, which is enough for an
   idea kept only so that it is not re-proposed. Among the builds only the
   mutable odometer still beats `bq-expand`, `bq-mut-runs` at 0.9231 on 23
   shapes of 24, the scan build being level rather than ahead (claim 4). So
   `bq-expand` is still the fastest build that needs neither a class
   extension nor explicit mutation.
6. `gen-quotrem` ties `list` (0.9050 on the geomean, 12 of 24, sign p 1)
   — the first attempt's arithmetic stops being dearer than the
   list's allocation once the flag takes its own allocation to 1.00x against
   the list's 23.5x, which is the mixed picture this suite exists to have
   refuted, arriving by a route nobody proposed. The `cm-gather` < `list`
   half is untimed and stands as Run 8's. A break here would mean something
   changed in `list` or in GHC, not in a strategy — check the anchor before
   anything else, as Run 8 had to and the three runs since did not.
7. Allocation, median multiples of the result on this basis: the mutable
   fills 1.00x, `gen-quotrem` also 1.00x, `bq-mut` and the scan family
   1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x,
   `list` 23.5x. Every one of the 34 rows reproduced Run 10's cell, and the
   cells behind them agree to a worst 1.7e-05, which is what makes this the
   claim to check first when anything else moves: allocation is deterministic
   per call, so a level that *does* move is a code change and never a slot.
8. Every pure arm in the fast tier runs its output through the single
   in-order `vGenerate` over an `m`-length table, and a `bq-*` arm that falls
   behind loses on its table build and not on its output. Read the structure
   and not a threshold: the gap the claim used to be stated across is
   populated, `bq-expand-zf` (0.105) and `offtab-scan-rem` (0.119) lying
   between the leading tier and `bq-gen` (0.336).
9. **Read this one per shape and not on its geomean.** `bq-expand-b`'s two
   best cells are `stretch-inner1` (0.920) and `stretch-wide-2xM` (0.931),
   the rank-2 views with one huge outer dimension where seeding from
   `enumFromStepN` replaces the whole `concatMap` build — the same two shapes
   in each of the last four runs, which is the stable part of this claim.
   The geomeans are not: `bq-expand-b` / `bq-expand` has read 0.996, 0.9678,
   0.9943 and now **0.9939** (10 of 23, sign p 0.68) across Runs 8 to 11,
   while `bq-expand-zf` / `bq-expand` went 3.6% behind, then level at 1.0028,
   then 1.0325 and now **1.0322** (1 of 23, sign p 5.7e-06). What Run 10 read
   as a layout term the aligned half could not settle, this run reads as
   settled by repetition instead: the last two runs agree to four digits on
   both arms, so the earlier disagreement was between builds and not within
   one. Both figures here are on 23 shapes, `lenet-L1-28-c1-k5` being set
   aside for the wild cell in the denominator.

Each ordering is one `./read-run.py RUN.json --pair A B` line — paired
geomean, an interval and a sign test — so a run reports which claims held
rather than re-deriving them from the table.

**And for each stride class, the same three properties, now carrying Run 11's
verdicts**, the details beside each class's table:

1. **`bq-expand`'s `worst` stays under 1.** Held in every class — 0.173 at
   its highest, under `rev` — so the shipped fallback
   was never slower than the `list` it replaced, on any shape of any class the
   library can produce, in any regime, roster or layout this page has run.
   This is the property the classes
   exist to test, no geomean can state it, and a break would have been the one
   result here to bear on `Data/Array/Internal.hs` directly.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-scan-rem-gm-mulback` the fastest pure arm, `bq-expand` behind both.
   The first clause, read as the vecdims family's rather than one arm's — the
   ruling Run 9 left, and no run has yet separated them — holds in eight of
   the nine populations and breaks in `reshape1` alone, where the flat fills
   own the top outright and have since -O1. *Which* member of the family
   leads is not a stable fact: `mut-odo-vecdims-add-in` heads `slice`,
   `window`, `scaled` and the main set, `add-both-down` heads `bcast` and
   `bcastmid`, the arm itself heads `rev` and `revsome` — and four of those
   eight are ties at the thousandth, `scaled` being the one that changed
   hands against Run 10 on the same binary. **The second clause is the one
   this run moves**: it holds in four of the nine (the main set, `bcastmid`,
   `slice`, `window`), goes to `bq-expand-gm-mulback` in `bcast`, `reshape1`,
   `scaled` and now `rev`, and is a four-way tie at 0.104 in `revsome`. Run
   10 counted six of nine. Nothing changed between the two runs, so what the
   count measures is how many populations have a pure tier tight enough for
   a thousandth to decide it — which is most of them. The third clause holds
   in all nine if read as *behind whichever arms lead*, and breaks in the
   same two as Run 10 if read on the arms it names — `bq-expand` (0.085)
   ahead of `mut-odo-vecdims` in `reshape1` and (0.076) ahead of
   `bq-scan-rem-gm-mulback` in `bcast`. Each break is read in its class's
   paragraph, and [the `sInner`
   ruling](#per-shape-where-the-geomean-hides-the-ordering) is what they bear
   on.
3. **The allocation tiers survive**: the mutable fills at the result vector,
   `bq-expand` at one to four times it, `list` at an order of magnitude more.
   Where a level moves it is the class's own `m` showing through, exactly as
   this property warned — `bq-expand` at 1.07x on `scaled` (`m` of 1 and
   2,000) and 4.22x on `reshape1` (`m = l`) — the ordering of tiers unbroken
   everywhere, and every level the same to the digit as Run 10's, Run 9's and
   Run 8's.

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

**Run 11 (SpecConstr, aligned) records every class**, one process per
class, in [the sequence](#making-a-major-benchmark-run); every table below
is that run's **aligned half**, the classes running there alone, and every
paragraph reads it against Run 10's measurement of the same population on the
same binary at the same regime, roster and order — so what lies between them
is nothing at all, and a class's movement here is drift. That is what makes
this section's readings unusually strong and unusually humbling at once:
where a class figure moved, nothing caused it. This section
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
properties](#the-claims-run-12-should-test) is bolded, and the class's own
paragraph says what broke.

Then one block per class, in `classViews`' order — `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled` — each carrying the same
five things and nothing else:

1. a bolded lead naming the class, the mechanism it models in a clause, and
   its shapes with their `l` and `sInner`, which is what makes the table under
   it readable without `Main.hs` open;
2. the table `--block --in-place` installs from `$R-aligned-$c.json`, whole and
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
| `rev` | 3 | 0.102 | 0.173 | **`bq-expand-gm-mulback`** 0.098 | `mut-odo-vecdims` 0.050 | 2.29% |
| `revsome` | 3 | 0.104 | 0.131 | `bq-expand-b` 0.104 | `mut-odo-vecdims` 0.052 | 1.40% |
| `bcast` | 3 | **0.076** | 0.097 | **`bq-expand-gm-mulback`** 0.069 | `mut-odo-vecdims-add-both-down` 0.026 | 1.58% |
| `bcastmid` | 2 | 0.116 | 0.133 | `bq-scan-rem-gm-mulback` 0.097 | `mut-odo-vecdims-add-both-down` 0.036 | 0.40% |
| `reshape1` | 2 | **0.085** | 0.095 | **`bq-expand-gm-mulback`** 0.038 | **`mut-flat-gm`** 0.029 | 0.67% |
| `slice` | 2 | 0.115 | 0.132 | `bq-scan-rem-gm-mulback` 0.103 | `mut-odo-vecdims-add-in` 0.043 | 0.36% |
| `window` | 2 | 0.121 | 0.129 | `bq-scan-rem-gm-mulback` 0.101 | `mut-odo-vecdims-add-in` 0.053 | 1.61% |
| `scaled` | 2 | 0.102 | 0.103 | **`bq-expand-gm-mulback`** 0.091 | `mut-odo-vecdims-add-in` 0.027 | 3.27% |

`revsome`'s pure cell is the only one here that names an arm the sort put
first rather than an arm that leads: `bq-expand-b`, `bq-scan-rem-gm-mulback`,
`bq-expand-qr-prim` and `bq-expand` all read 0.104 there, so it is unbolded
as a tie rather than a break.

**`rev` — every stride negated, offset at the top: the view `rev` on every
axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *137* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *158* | *0.00x* |
| **mut-odo-vecdims** | **0.050** | 0.077 | 0.05 | 138 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.050* | *0.077* | *0.03* | *138* | *1.00x* |
| mut-odo-vecdims-add-in | 0.050 | 0.077 | 0.04 | 138 | 1.00x |
| *mut-odo-vecdims-aa* | *0.051* | *0.077* | *0.05* | *138* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.052 | 0.079 | 0.06 | 137 | 1.01x |
| mut-odo-vecdims-add-both | 0.055 | 0.086 | 0.24 | 136 | 1.01x |
| mut-odo-vecdims-add-out | 0.057 | 0.090 | 0.05 | 136 | 1.01x |
| build | 0.094 | 0.213 | 0.05 | 127 | 1.00x |
| mut-flat-gm | 0.096 | 0.140 | 0.06 | 134 | 1.34x |
| mut-odo | 0.098 | 0.218 | 0.07 | 125 | 1.00x |
| bq-expand-gm-mulback | 0.098 | 0.168 | 0.03 | 132 | 2.52x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.105* | *0.01* | *130* | *1.34x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.105* | *0.03* | *130* | *1.34x* |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.105 | 0.01 | 130 | 1.34x |
| *bq-expand-aa-distant* | *0.101* | *0.173* | *0.02* | *131* | *2.52x* |
| bq-expand-qr-prim | 0.101 | 0.172 | 0.02 | 131 | 2.52x |
| bq-odo-gm-mulback | 0.101 | 0.115 | 0.06 | 132 | 1.41x |
| **bq-expand** | **0.102** | 0.173 | 0.05 | 131 | 2.52x |
| bq-expand-b | 0.102 | 0.173 | 0.02 | 131 | 2.52x |
| *bq-expand-aa-adjacent* | *0.104* | *0.173* | *0.04* | *131* | *2.52x* |
| bq-expand-zf | 0.104 | 0.184 | 0.03 | 130 | 2.52x |
| bq-mut-runs-gm-mulback | 0.105 | 0.158 | 0.04 | 133 | 1.34x |
| bq-mut-runs | 0.108 | 0.156 | 0.03 | 132 | 1.34x |
| offtab | 0.123 | 0.253 | 0.34 | 125 | 2.00x |
| offtab-scan-rem | 0.138 | 0.140 | 0.03 | 125 | 2.00x |
| bq-mut | 0.174 | 0.248 | 0.04 | 119 | 1.34x |
| bq-gen | 0.517 | 0.665 | 0.07 | 99 | 1.34x |
| list (baseline) | 1.000 | 1.000 | 0.13 | 89 | 23.45x |
| gen-quotrem | 1.308 | 1.589 | 0.21 | 83 | 1.00x |
| gen-unsafe | 1.339 | 1.606 | 0.49 | 82 | 1.00x |


Controls: **the disturbance at this class's `mut-odo-vecdims` slot is back**,
and carries the floor at **2.29%** — the adjacent pair at 1.0229, worst cell
6.93% on `rev-primes` — where Run 10 read 0.16% here and called the slot
quiet, and Run 9 read 1.96% at that same slot with its worst cells on that
same shape. Three runs of four have found it and an aligned build did not
remove it. The other five pairs sit within 0.28% and all six intervals cover
1. Published parts from paired on both `bq-expand` pairs here — 0.9884
against 0.9985 distant and 1.0178 against 1.0026 adjacent, a capped cell on
each — so the paired figures are the ones to read; `revsome`'s distant pair
parts furthest in the run, at 0.9845 against 1.0040. The `sum-only` halves
agree at 1.0018; the in-situ term reads 0.9815 and 0.9861 of `sum-only` as
medians (`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h8m46s, peak 60 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 3.72 ms per call raw, 3.57 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.077/0.057/0.028,
`bq-scan-rem-gm-mulback` 0.102/0.105/0.093, `bq-expand` 0.173/0.099/0.100

What the class says: the shipped row is safe (`worst` 0.173) and the
fastest-pure slot has **changed hands again**, to `bq-expand-gm-mulback` at
0.098, where Run 10 handed it back to `bq-scan-rem-gm-mulback` (now 0.100)
and Run 9 gave it to the arm holding it now. Four pure arms lie inside four
thousandths — 0.098, 0.100, `bq-odo-gm-mulback`'s 0.101 and `bq-expand`'s own
0.102 — so the cluster is the reading and the slot goes to whichever of them
a run happens to put first. Two runs of *one binary* disagreeing about it
settles what Run 10 could only suspect: this is neither a layout term nor a
regime, it is a margin below every floor this page has measured. The other
reading is the ceiling's: the vecdims family sits at 0.050, `build` at 0.094
beats every pure arm and `mut-odo` at 0.098 ties the leader. What survives
every regime, roster and layout is the collapse of the first attempt:
`gen-quotrem` and `gen-unsafe` run 1.31x and 1.34x *slower than `list`*,
worst cells above 1.58. Reversal is this class's stress and the
per-dimension-arithmetic arms bear it worst whatever the flag.

**`revsome` — a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89),
`revsome-outer-g48` (`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l`
165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *91* | *2.52x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.07* | *117* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.08* | *117* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.052* | *0.063* | *0.13* | *98* | *1.00x* |
| **mut-odo-vecdims** | **0.052** | 0.063 | 0.10 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.053* | *0.063* | *0.10* | *97* | *1.00x* |
| mut-odo-vecdims-add-in | 0.053 | 0.063 | 0.18 | 98 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.054 | 0.067 | 0.40 | 98 | 1.00x |
| mut-odo-vecdims-add-both | 0.059 | 0.072 | 0.15 | 98 | 1.00x |
| mut-odo-vecdims-add-out | 0.063 | 0.076 | 0.14 | 98 | 1.00x |
| mut-flat-gm | 0.090 | 0.105 | 0.25 | 87 | 1.33x |
| build | 0.091 | 0.150 | 0.47 | 97 | 1.00x |
| bq-mut-runs-gm-mulback | 0.098 | 0.110 | 0.28 | 87 | 1.33x |
| bq-mut-runs | 0.102 | 0.119 | 0.11 | 86 | 1.33x |
| *bq-expand-aa-distant* | *0.103* | *0.132* | *0.13* | *84* | *2.52x* |
| bq-expand-b | 0.104 | 0.131 | 0.06 | 84 | 2.52x |
| **bq-scan-rem-gm-mulback** | **0.104** | 0.106 | 0.04 | 88 | 1.33x |
| *bq-expand-aa-adjacent* | *0.104* | *0.131* | *0.07* | *84* | *2.52x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.104* | *0.106* | *0.28* | *88* | *1.33x* |
| bq-expand-qr-prim | 0.104 | 0.131 | 0.33 | 84 | 2.52x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.104* | *0.106* | *0.11* | *88* | *1.33x* |
| **bq-expand** | **0.104** | 0.131 | 0.45 | 84 | 2.52x |
| bq-expand-gm-mulback | 0.106 | 0.124 | 0.08 | 85 | 2.52x |
| bq-odo-gm-mulback | 0.106 | 0.117 | 0.11 | 86 | 1.41x |
| bq-expand-zf | 0.107 | 0.138 | 0.21 | 84 | 2.52x |
| offtab | 0.109 | 0.179 | 0.63 | 92 | 2.00x |
| mut-odo | 0.126 | 0.161 | 0.87 | 97 | 1.00x |
| offtab-scan-rem | 0.138 | 0.141 | 0.09 | 84 | 2.00x |
| bq-mut | 0.184 | 0.223 | 0.09 | 84 | 1.33x |
| bq-gen | 0.415 | 0.665 | 0.21 | 83 | 1.33x |
| list (baseline) | 1.000 | 1.000 | 0.61 | 48 | 23.45x |
| gen-quotrem | 1.242 | 1.420 | 0.81 | 45 | 1.00x |
| gen-unsafe | 1.311 | 1.368 | 0.68 | 46 | 1.00x |


Controls: the largest A/A deviation is **1.40%** on the `mut-odo-vecdims`
adjacent pair (1.0140 paired, worst cell 3.80% on `revsome-inner-primes`),
its distant pair reading 1.0016; the other four sit within 0.73%. Three of
the six pairs had a cell capped, so three published figures part from their
paired ones here and `--selftest` asserts the identity for the rest. The
`sum-only` halves agree at 1.0000; the in-situ term reads 0.9835 and 0.9969
as medians (`mut-odo-vecdims` and `bq-expand` arms).

Provenance: elapsed 0h8m46s, peak 60 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 3.69 ms per call raw, 3.54 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.031/0.058/0.063,
`bq-scan-rem-gm-mulback` 0.102/0.106/0.103, `bq-expand` 0.101/0.098/0.131

What the class says: mixed signs keep the top of the table in the main set's
order, and the pure tier is a **four-way tie at 0.104** — `bq-expand-b`,
`bq-scan-rem-gm-mulback`, `bq-expand-qr-prim` and `bq-expand` itself, with
`bq-odo-gm-mulback` and `bq-expand-gm-mulback` a step behind at 0.106. The
verdict `--block` prints hands the fastest-pure slot to `bq-expand-b`, which
is a tie broken past the third digit and is reported here as the tie it is:
the second property's second clause is neither held nor broken in this
population. What did move is `mut-odo`, to **0.126** from Run 10's 0.109 on
this same binary, while its code twin `build` sat still at 0.091 against
0.090 — the largest single movement the repetition found in any population,
on the arm the main set already names as the one that drifts. The first
attempt runs 1.24x and 1.31x behind `list`, as it did in both previous
regimes.

**`bcast` — an innermost stride of 0, every run re-reading one element: a
broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.32* | *53* | *1.38x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *84* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *69* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.026 | 0.070 | 0.26 | 63 | 1.00x |
| mut-odo-vecdims-add-in | 0.028 | 0.066 | 0.25 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.066* | *0.29* | *62* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.066 | 0.02 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.066* | *0.02* | *62* | *1.00x* |
| mut-odo-vecdims-add-both | 0.030 | 0.076 | 0.26 | 62 | 1.00x |
| mut-odo-vecdims-add-out | 0.031 | 0.081 | 0.26 | 62 | 1.00x |
| mut-odo | 0.047 | 0.157 | 0.31 | 62 | 1.00x |
| build | 0.048 | 0.162 | 0.24 | 62 | 1.00x |
| bq-mut-runs-gm-mulback | 0.065 | 0.084 | 0.33 | 48 | 1.13x |
| mut-flat-gm | 0.065 | 0.079 | 0.36 | 48 | 1.13x |
| offtab | 0.067 | 0.162 | 0.60 | 55 | 2.00x |
| bq-expand-gm-mulback | 0.069 | 0.087 | 0.34 | 48 | 1.38x |
| bq-expand-b | 0.073 | 0.097 | 0.33 | 47 | 1.38x |
| bq-mut-runs | 0.073 | 0.095 | 0.35 | 47 | 1.13x |
| bq-odo-gm-mulback | 0.074 | 0.092 | 0.34 | 48 | 1.14x |
| **bq-expand** | **0.076** | 0.097 | 0.35 | 47 | 1.38x |
| bq-expand-qr-prim | 0.076 | 0.097 | 0.34 | 47 | 1.38x |
| *bq-expand-aa-adjacent* | *0.076* | *0.097* | *0.35* | *47* | *1.38x* |
| bq-expand-zf | 0.076 | 0.098 | 0.36 | 47 | 1.38x |
| *bq-expand-aa-distant* | *0.077* | *0.097* | *0.07* | *47* | *1.38x* |
| **bq-scan-rem-gm-mulback** | **0.084** | 0.104 | 0.35 | 48 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.085* | *0.104* | *0.35* | *48* | *1.13x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.085* | *0.104* | *0.02* | *48* | *1.13x* |
| bq-mut | 0.106 | 0.179 | 0.35 | 47 | 1.13x |
| offtab-scan-rem | 0.114 | 0.138 | 0.81 | 44 | 2.00x |
| bq-gen | 0.186 | 0.283 | 0.72 | 47 | 1.13x |
| gen-unsafe | 0.452 | 1.093 | 1.03 | 25 | 1.00x |
| gen-quotrem | 0.494 | 1.159 | 0.54 | 25 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 1.06 | 16 | 20.64x |


Controls: the floor is **1.58%** on the `mut-odo-vecdims` distant pair
(1.0158, worst cell 4.48% on `bcast-inner8`); the other five sit within
0.50%, and its two adjacent pairs are among the run's tightest cells at 0.03%
and 0.04%. Only two of the six intervals cover 1, which on a class whose
printed intervals understate the spread elevenfold is what that factor
means rather than a second finding. The `sum-only` halves agree at 0.9976;
the in-situ term reads 0.9856 and 0.9849 as medians.

Provenance: elapsed 0h8m49s, peak 93 MiB in use, 40 MiB max residency; the
reader reads 34 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 52.3 ms per call raw, 51.2 ms net.

Per shape, in the lead's order: `mut-odo-vecdims` 0.034/0.010/0.066,
`bq-scan-rem-gm-mulback` 0.094/0.043/0.104, `bq-expand` 0.097/0.049/0.086

What the class says: every ratio sits far below the main set's, `list` paying
its cons-list walk on data the strategies read from cache, and the shipped
row is safe (`worst` 0.097). The fastest-pure slot goes to
`bq-expand-gm-mulback` (0.069) and `bq-scan-rem-gm-mulback` falls to 0.084,
so `bq-expand` itself (0.076) is again ahead of the arm claimed to lead the
pure tier — the third run to record that inversion here, so it is this
class's property and not a break to chase. A stride-0 innermost run re-reads
one element, so the table build is nearly the whole cost here and the scan's
cheaper output buys nothing. `bq-expand`'s allocation tier sits at 1.38x on
the class's small `m` (2,000-6,400 against `l` in the hundreds of
thousands), the `m`-tier effect the third property predicts and the same
figure as in the two previous runs; and both first-attempt arms *beat*
`list` (`gen-unsafe` 0.452, `gen-quotrem` 0.494), the stride-0 read being
the one place their arithmetic is cheaper than the list's allocation —
though both carry a worst cell above 1 (1.093 and 1.159), so the win is the
geomean's and not every shape's. `list` itself is measured on 16 samples
here, the thinnest in the run, so read this class's absolute anchor before
its ratios: it moved 1.6% *down* against Run 10, where that run moved 7.9%
up against Run 9 and called it the largest of the eleven.

**`bcastmid` — the stretched axis in the middle instead: stride 0 on an
outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.05* | *90* | *2.10x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *113* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *113* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.036 | 0.067 | 0.08 | 98 | 1.00x |
| mut-odo-vecdims-add-in | 0.036 | 0.062 | 0.14 | 98 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.036* | *0.063* | *0.08* | *98* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.036* | *0.062* | *0.04* | *98* | *1.00x* |
| **mut-odo-vecdims** | **0.036** | 0.062 | 0.04 | 98 | 1.00x |
| mut-odo-vecdims-add-both | 0.039 | 0.072 | 0.08 | 97 | 1.00x |
| mut-odo-vecdims-add-out | 0.040 | 0.075 | 0.06 | 97 | 1.00x |
| mut-odo | 0.060 | 0.159 | 0.83 | 91 | 1.00x |
| build | 0.061 | 0.165 | 0.19 | 90 | 1.00x |
| offtab | 0.088 | 0.168 | 0.59 | 86 | 2.00x |
| mut-flat-gm | 0.097 | 0.107 | 0.29 | 86 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.097* | *0.104* | *0.04* | *87* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.097** | 0.104 | 0.05 | 87 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.105* | *0.02* | *87* | *1.17x* |
| bq-mut-runs-gm-mulback | 0.099 | 0.108 | 0.19 | 86 | 1.17x |
| bq-odo-gm-mulback | 0.105 | 0.117 | 0.05 | 86 | 1.78x |
| bq-expand-gm-mulback | 0.106 | 0.125 | 0.05 | 86 | 2.10x |
| bq-mut-runs | 0.112 | 0.123 | 0.04 | 84 | 1.17x |
| bq-expand-qr-prim | 0.116 | 0.132 | 0.07 | 84 | 2.10x |
| *bq-expand-aa-adjacent* | *0.116* | *0.133* | *0.05* | *84* | *2.10x* |
| bq-expand-b | 0.116 | 0.133 | 0.04 | 84 | 2.10x |
| **bq-expand** | **0.116** | 0.133 | 0.07 | 84 | 2.10x |
| *bq-expand-aa-distant* | *0.117* | *0.134* | *0.02* | *84* | *2.10x* |
| bq-expand-zf | 0.119 | 0.138 | 0.05 | 84 | 2.10x |
| offtab-scan-rem | 0.132 | 0.132 | 0.06 | 82 | 2.00x |
| bq-mut | 0.155 | 0.231 | 0.49 | 80 | 1.17x |
| bq-gen | 0.269 | 0.643 | 0.77 | 70 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.14 | 48 | 21.99x |
| gen-unsafe | 1.177 | 1.337 | 0.89 | 45 | 1.00x |
| gen-quotrem | 1.282 | 1.420 | 0.83 | 44 | 1.00x |


Controls: **the disturbance that had held this class's `mut-odo-vecdims`
adjacent slot for four runs is gone**, that pair reading 0.9993 where -O1,
Run 8, Run 9 and Run 10 all put it near 0.5%. The floor moves to the two
distant pairs instead, at **0.40%** (`bq-expand` 1.0040,
`bq-scan-rem-gm-mulback` 1.0037), and the other four sit within 0.10%. Since
nothing about the binary or the roster changed, a four-run streak ending is
what this page's floor is for: a slot's disturbance is a run's property here
and not a fixture. The `sum-only` halves agree at 0.9965; the in-situ term
reads 0.9852 and 0.9871 as medians.

Provenance: elapsed 0h5m51s, peak 35 MiB in use, 11 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the bcastmid class. Anchor:
`bcastmid-primes`, `list` at 3.62 ms per call raw, 3.47 ms net.

What the class says: the main ordering holds at the top and in the pure tier
both — the vecdims family leads with three of its arms on one thousandth
(`add-both-down`, `add-in` and `mut-odo-vecdims` all 0.036),
`bq-scan-rem-gm-mulback` (0.097) is the fastest pure arm, `bq-expand` (0.116)
sits behind both — which is all three clauses of the second property in one
population, as in `slice` and `window`. Behind the vecdims family come
`mut-odo` (0.060), `build` (0.061) and `offtab` (0.088), the two
placement-susceptible arms adjacent and both ahead of every pure arm — and
adjacent in the *other* order from Run 10, which had `build` 0.060 against
`mut-odo` 0.062. A thousandth either way on the same binary is the pair
being a tie in this class rather than an ordering, which is how the main
set's reading of them now runs too.

**`reshape1` — the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.16* | *81* | *4.22x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.05* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.10* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| mut-flat-gm | 0.029 | 0.031 | 0.11 | 90 | 2.00x |
| bq-mut-runs-gm-mulback | 0.029 | 0.031 | 0.08 | 90 | 2.00x |
| bq-expand-gm-mulback | 0.038 | 0.048 | 0.10 | 86 | 4.22x |
| bq-odo-gm-mulback | 0.041 | 0.045 | 0.08 | 86 | 2.15x |
| bq-mut-runs | 0.076 | 0.077 | 0.11 | 78 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.077* | *0.078* | *0.10* | *77* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.077** | 0.077 | 0.12 | 77 | 2.00x |
| offtab-scan-rem | 0.077 | 0.077 | 0.10 | 77 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.077* | *0.078* | *0.05* | *77* | *2.00x* |
| bq-expand-b | 0.081 | 0.094 | 0.09 | 76 | 3.72x |
| **bq-expand** | **0.085** | 0.095 | 0.18 | 76 | 4.22x |
| *bq-expand-aa-adjacent* | *0.085* | *0.095* | *0.13* | *76* | *4.22x* |
| bq-expand-qr-prim | 0.086 | 0.095 | 0.15 | 76 | 4.22x |
| *bq-expand-aa-distant* | *0.086* | *0.095* | *0.10* | *76* | *4.22x* |
| bq-expand-zf | 0.086 | 0.097 | 0.12 | 76 | 4.22x |
| *mut-odo-vecdims-aa* | *0.099* | *0.100* | *0.05* | *74* | *1.00x* |
| mut-odo-vecdims-add-in | 0.099 | 0.100 | 0.07 | 74 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.099* | *0.100* | *0.02* | *74* | *1.00x* |
| **mut-odo-vecdims** | **0.099** | 0.100 | 0.07 | 74 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.107 | 0.108 | 0.08 | 72 | 1.00x |
| mut-odo-vecdims-add-both | 0.116 | 0.117 | 0.12 | 71 | 1.00x |
| mut-odo-vecdims-add-out | 0.117 | 0.117 | 0.08 | 71 | 1.00x |
| build | 0.255 | 0.262 | 0.19 | 58 | 1.00x |
| mut-odo | 0.268 | 0.290 | 1.20 | 58 | 1.00x |
| bq-mut | 0.272 | 0.320 | 0.36 | 57 | 2.00x |
| offtab | 0.288 | 0.331 | 1.60 | 56 | 2.00x |
| gen-unsafe | 0.608 | 0.878 | 0.56 | 44 | 1.00x |
| gen-quotrem | 0.611 | 0.871 | 0.68 | 43 | 1.00x |
| bq-gen | 0.681 | 1.137 | 0.89 | 41 | 2.00x |
| list (baseline) | 1.000 | 1.000 | 0.33 | 36 | 32.18x |


Controls: every A/A pair within **0.67%**, the largest being `bq-expand`'s
distant pair at 1.0067 with its worst cell 0.77% on `reshape1-500k`, and four
of the six inside 0.15%. The `sum-only` halves agree at 0.9993; the in-situ
term reads 0.9815 and 0.9854 as medians. Run 7's disturbance at this class's
`mut-odo-vecdims` slot, which cost it a 3.5% floor and a 33% in-situ scatter,
is absent for the fourth run running.

Provenance: elapsed 0h5m53s, peak 51 MiB in use, 17 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 11.7 ms per call raw, 11.4 ms net.

What the class says: the top still inverts completely and still by
construction — with `sInner` 1 every run is one element, so the flat fills
win outright (`mut-flat-gm` and `bq-mut-runs-gm-mulback` tied at 0.029) while
the odometer fills pay a full odometer step per element (`build` 0.255,
`mut-odo` 0.268) and `mut-odo-vecdims` lands mid-table (0.099). This is [the
`sInner` ruling][pershape]'s extreme case, mechanism rather than scatter, and
neither the regime, the roster nor the layout touches it. The `build`/`mut-odo`
pair, which Run 10 read here as its one population with `build` *behind*
(1.0335), has swapped back to `build` ahead by 5% — the two being 27 times
slower than the class's leaders, so whatever separates them here is not the
loop the shim aligned, and two runs of one binary disagreeing about the sign
says it is not a fixed property of the class either. It remains the one class
breaking two clauses of the second property at once: the fastest pure arm is
`bq-expand-gm-mulback` (0.038) rather than the scan (0.077), with
`bq-odo-gm-mulback` (0.041) between them, and `bq-expand` (0.085) is *ahead*
of `mut-odo-vecdims` (0.099) — the only population anywhere where the shipped
arm beats the ceiling's own arm. `m = l` here, which is what puts
`bq-expand`'s allocation at 4.22x, its highest in any class and the level the
third property names. That level carries a nursery consequence with it:
`bq-expand` holds 6–8 MB of excess allocation on both shapes and
`mut-odo-vecdims` none at all, against `list`'s 43 and 118 MB, so the default
4 MB area penalises the baseline hardest and the ceiling's arm not at all. A
larger nursery would raise `mut-odo-vecdims`'s ratio more than `bq-expand`'s,
so the inversion above is a floor rather than an artifact — it would widen
([the predictor][floor]).

**`slice` — a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes`
(`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *90* | *2.16x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.04* | *110* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.11* | *113* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *113* | *0.00x* |
| mut-odo-vecdims-add-in | 0.043 | 0.063 | 0.03 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.043** | 0.063 | 0.03 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.043* | *0.063* | *0.03* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.043* | *0.063* | *0.03* | *96* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.044 | 0.067 | 0.04 | 96 | 1.00x |
| mut-odo-vecdims-add-both | 0.047 | 0.072 | 0.06 | 96 | 1.00x |
| mut-odo-vecdims-add-out | 0.048 | 0.076 | 0.04 | 96 | 1.00x |
| mut-odo | 0.069 | 0.150 | 1.82 | 90 | 1.00x |
| build | 0.071 | 0.158 | 0.09 | 89 | 1.00x |
| mut-flat-gm | 0.097 | 0.105 | 0.17 | 87 | 1.17x |
| offtab | 0.100 | 0.188 | 0.64 | 85 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.103* | *0.104* | *0.07* | *86* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.103** | 0.104 | 0.08 | 86 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.103* | *0.105* | *0.02* | *86* | *1.17x* |
| bq-mut-runs-gm-mulback | 0.105 | 0.110 | 0.05 | 86 | 1.17x |
| bq-mut-runs | 0.110 | 0.122 | 0.05 | 84 | 1.17x |
| bq-odo-gm-mulback | 0.114 | 0.119 | 0.08 | 84 | 1.79x |
| bq-expand-gm-mulback | 0.114 | 0.126 | 0.12 | 84 | 2.16x |
| *bq-expand-aa-adjacent* | *0.115* | *0.132* | *0.10* | *84* | *2.16x* |
| **bq-expand** | **0.115** | 0.132 | 0.05 | 84 | 2.16x |
| bq-expand-b | 0.116 | 0.132 | 0.05 | 84 | 2.16x |
| *bq-expand-aa-distant* | *0.116* | *0.132* | *0.05* | *84* | *2.16x* |
| bq-expand-qr-prim | 0.116 | 0.132 | 0.06 | 84 | 2.16x |
| bq-expand-zf | 0.120 | 0.139 | 0.09 | 84 | 2.16x |
| offtab-scan-rem | 0.139 | 0.142 | 0.08 | 82 | 2.00x |
| bq-mut | 0.145 | 0.202 | 0.72 | 80 | 1.17x |
| bq-gen | 0.276 | 0.677 | 0.68 | 70 | 1.17x |
| list (baseline) | 1.000 | 1.000 | 0.32 | 48 | 21.99x |
| gen-unsafe | 1.214 | 1.357 | 1.03 | 44 | 1.00x |
| gen-quotrem | 1.286 | 1.480 | 0.58 | 43 | 1.00x |


Controls: **the quietest of the eight class processes** — every A/A pair
within **0.36%**, the largest being `mut-odo-vecdims`'s distant pair at
1.0036, and four of the six inside 0.10%; only the main set's max-skip half,
at 0.22%, is tighter anywhere in the run. The `sum-only` halves agree at
1.0020; the in-situ term reads 0.9840 and 0.9886 as medians
(`mut-odo-vecdims` and `bq-expand` arms). This class has now been the
quietest or near it in four successive runs, which is the closest thing here
to a population being intrinsically well-behaved.

Provenance: elapsed 0h5m51s, peak 48 MiB in use, 17 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the slice class. Anchor:
`slice-primes`, `list` at 3.69 ms per call raw, 3.54 ms net.

What the class says: a non-zero offset changes nothing, in any regime,
roster or layout — all three clauses of the second property hold, the main
ordering reproduces whole, and that is the result.
`mut-odo-vecdims-add-in` (0.043) ties the arm it varies at the head, as it
does in `window` and `scaled`. `mut-odo` (0.069) and `build` (0.071) sit
adjacent as the identical-worker pair the floor section prices, two
thousandths apart and in the opposite order to Run 10's 0.066 and 0.067 —
a tie read twice, not an ordering that moved.

**`window` — overlapping im2col patches: the workload this page opens by
naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.03* | *107* | *2.48x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.07* | *123* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.09* | *132* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *132* | *0.00x* |
| mut-odo-vecdims-add-in | 0.053 | 0.061 | 0.07 | 114 | 1.00x |
| *mut-odo-vecdims-aa* | *0.054* | *0.061* | *0.04* | *113* | *1.00x* |
| **mut-odo-vecdims** | **0.054** | 0.061 | 0.05 | 113 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.055* | *0.063* | *0.09* | *112* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.056 | 0.066 | 0.06 | 112 | 1.01x |
| mut-odo-vecdims-add-both | 0.061 | 0.071 | 0.08 | 112 | 1.01x |
| mut-odo-vecdims-add-out | 0.064 | 0.074 | 0.06 | 110 | 1.01x |
| mut-flat-gm | 0.097 | 0.107 | 0.31 | 105 | 1.27x |
| **bq-scan-rem-gm-mulback** | **0.101** | 0.103 | 0.06 | 104 | 1.27x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.101* | *0.103* | *0.03* | *104* | *1.27x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.101* | *0.103* | *0.06* | *104* | *1.27x* |
| bq-mut-runs-gm-mulback | 0.102 | 0.107 | 0.08 | 104 | 1.27x |
| bq-odo-gm-mulback | 0.109 | 0.115 | 0.12 | 104 | 2.10x |
| bq-mut-runs | 0.110 | 0.115 | 0.04 | 103 | 1.27x |
| bq-expand-gm-mulback | 0.113 | 0.122 | 0.12 | 102 | 2.48x |
| *bq-expand-aa-adjacent* | *0.121* | *0.129* | *0.05* | *102* | *2.48x* |
| **bq-expand** | **0.121** | 0.129 | 0.04 | 102 | 2.48x |
| *bq-expand-aa-distant* | *0.121* | *0.129* | *0.03* | *102* | *2.48x* |
| bq-expand-qr-prim | 0.121 | 0.129 | 0.03 | 102 | 2.48x |
| bq-expand-b | 0.121 | 0.130 | 0.04 | 102 | 2.48x |
| bq-expand-zf | 0.126 | 0.137 | 0.04 | 101 | 2.48x |
| build | 0.127 | 0.160 | 0.33 | 102 | 1.00x |
| offtab-scan-rem | 0.131 | 0.131 | 0.06 | 100 | 2.00x |
| mut-odo | 0.136 | 0.158 | 1.55 | 100 | 1.00x |
| offtab | 0.152 | 0.183 | 0.63 | 98 | 2.00x |
| bq-mut | 0.188 | 0.203 | 0.69 | 94 | 1.27x |
| bq-gen | 0.458 | 0.512 | 0.43 | 80 | 1.27x |
| list (baseline) | 1.000 | 1.000 | 0.16 | 66 | 23.46x |
| gen-quotrem | 1.164 | 1.310 | 0.43 | 63 | 1.00x |
| gen-unsafe | 1.170 | 1.374 | 0.42 | 62 | 1.00x |


Controls: the floor is **1.61%**, on `mut-odo-vecdims`'s distant pair
(1.0161) — the fifth successive run to put this class's floor at that arm's
slot, and the fourth to put its worst cell on the small shape
`window-28x28-k5`. The other five pairs sit within 0.07%, the tightest set in
the run, so this is one pair and not a noisy process; against that spread the
printed intervals understate by 39x, the run's largest such factor and a
direct consequence of five tight pairs beside one loose one. The `sum-only`
halves agree at 0.9957; the in-situ term reads 0.9783 and 0.9838 as medians.

Provenance: elapsed 0h5m50s, peak 41 MiB in use, 15 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 8.42 ms per call raw, 8.15 ms net.

What the class says: the ordering holds whole — all three clauses — and the
figure this class exists for is the shipped row against the main set's, 0.121
here against 0.103 there. The overlap the main set drops still *lifts* every
ratio rather than lowering it, by about the same margin as in the four
previous runs, so the main set flatters the fallback's standing against
`list` in every regime, roster and layout tried, and the pessimism this page
once recorded was about absolute cost only. Claim 2's second half, which Run
9 found at its narrowest here, reads **1.2583** paired with both shapes
agreeing, against Run 10's 1.3207 — a witness that stays clear while its
size moves by six points between two runs of one binary, which is what a
two-shape population's margin is worth.

**`scaled` — superincreasing strides, none of them 1: a hand-built
dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30),
`scaled-rank1-m1` (`l` 300000, `sInner` 300000 — rank 1, so `m` is 1 and
the whole view is one strided run).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *104* | *1.07x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.03* | *130* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.04* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.09* | *122* | *0.00x* |
| mut-odo-vecdims-add-in | 0.027 | 0.029 | 0.05 | 111 | 1.00x |
| **mut-odo-vecdims** | **0.028** | 0.030 | 0.08 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.030* | *0.09* | *111* | *1.00x* |
| mut-odo-vecdims-add-both | 0.028 | 0.030 | 0.06 | 111 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.028 | 0.030 | 0.61 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.030* | *0.45* | *111* | *1.00x* |
| mut-odo-vecdims-add-out | 0.029 | 0.029 | 0.09 | 110 | 1.00x |
| build | 0.031 | 0.032 | 0.61 | 110 | 1.00x |
| mut-odo | 0.031 | 0.032 | 0.21 | 110 | 1.00x |
| offtab | 0.059 | 0.060 | 0.38 | 104 | 2.00x |
| mut-flat-gm | 0.082 | 0.082 | 0.36 | 100 | 1.02x |
| bq-mut-runs-gm-mulback | 0.090 | 0.091 | 0.05 | 98 | 1.02x |
| bq-expand-gm-mulback | 0.091 | 0.092 | 0.07 | 98 | 1.07x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.092* | *0.07* | *98* | *1.02x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.092* | *0.02* | *98* | *1.02x* |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.093 | 0.20 | 98 | 1.02x |
| bq-odo-gm-mulback | 0.097 | 0.099 | 0.27 | 98 | 1.02x |
| bq-mut-runs | 0.101 | 0.102 | 0.04 | 97 | 1.02x |
| **bq-expand** | **0.102** | 0.103 | 0.10 | 96 | 1.07x |
| bq-expand-qr-prim | 0.102 | 0.104 | 0.06 | 96 | 1.07x |
| bq-expand-b | 0.102 | 0.102 | 0.04 | 97 | 1.07x |
| *bq-expand-aa-adjacent* | *0.102* | *0.104* | *0.27* | *96* | *1.07x* |
| *bq-expand-aa-distant* | *0.103* | *0.103* | *0.04* | *96* | *1.07x* |
| bq-expand-zf | 0.103 | 0.103 | 0.12 | 96 | 1.07x |
| bq-mut | 0.107 | 0.111 | 0.06 | 96 | 1.02x |
| bq-gen | 0.118 | 0.137 | 0.06 | 94 | 1.02x |
| offtab-scan-rem | 0.134 | 0.137 | 0.07 | 92 | 2.00x |
| gen-unsafe | 0.651 | 1.206 | 0.28 | 65 | 1.00x |
| gen-quotrem | 0.673 | 1.219 | 0.95 | 64 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.23 | 58 | 19.22x |


Controls: **this class carries the run's worst floor for the second run
running, at 3.27%**, and the `mut-odo-vecdims` slot carries it again — the
distant pair at 1.0327, worst cell 6.92% on `scaled-super-r3`, which is the
same slot and the same shape as Run 10's. What changed is the sign and the
company: Run 10 had *both* vecdims pairs below 1 at 0.9464 and 0.9574, where
here the adjacent pair is clean at 1.0020 and the distant one is above 1. So
the disturbance is one pair's, not the family's, and its direction is not
stable across two runs of one binary. **Most of it is the correction, not the
arm**, exactly as Run 10 found: on raw slopes the pair disagrees by **1.25%**
and the forcing term is **60.9%** of this bench — the largest share anywhere
in the run — so the 1/(1-f) amplification the [floor section][floor] derives
turns that into the 3.27% published, predicting 1.0320 against the 1.0327
read. Quote the raw deviation for how much a name disagrees with itself and
the net one for the table's floor. The `sum-only` halves agree at 0.9988; the
in-situ term reads 0.9907 and 0.9784 as medians, so the correction itself is
sound here.

Provenance: elapsed 0h5m49s, peak 65 MiB in use, 23 MiB max residency; the
reader reads 34 benchmarks over 2 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.32 ms per call raw, 4.14 ms net.

What the class says: Run 8's break here stays repaired — `build` (0.031) led
this class outright then and sits behind the vecdims family (0.027) and level
with `mut-odo` (0.031), so the second property's first clause holds. Its
second does not: the fastest pure arm is `bq-expand-gm-mulback` (0.091)
rather than the scan (0.092), a thousandth apart and the same way round as
Run 10 read it. The allocation tiers collapse toward 1 (`bq-expand` 1.07x),
the `m`-tier effect at its floor — `m` of 1 and 2,000 makes every table free
— which is why the spread from the fastest arm to `bq-gen` is the narrowest
of any population, 0.027 to 0.118. `gen-quotrem` and `gen-unsafe` beat
`list` at 0.673 and 0.651 while their `worst` cells still cross 1 (1.219 and
1.206), the only class besides `bcast` where the first attempt wins at all.

### Provenance

The run's name, regime, scale and source commit are at the head of this
chapter; what follows is what they have to be read against. The commit is
recorded there because a run whose artifact is deleted and whose source is
unrecorded cannot be repeated even in principle.

Run 11 against Run 10's aligned half is the cleanest comparison this page can
draw, and there is nothing left to pin: the same shapes, the same class
lists, the same roster membership in the same order, the same machine, the
same GHC, the same `cabal.project.freeze`, the same compiler flag — and the
same binary, md5 `a28b3e5b1c409cec6cca64de9f46bb4d`, so not even the compiler
ran twice. Every previous entry on this list left the layout free, and this
one does not. `list` moved 0.25% between the two runs and 0.7% between this
run's halves, so all five SpecConstr columns may be subtracted directly
rather than merely ordered. That is what makes this run's every movement
either drift or the shim's padding, and it is why the drift band at the head
of this chapter is the chapter's main result.

The desktop named at the head of this chapter is the same machine whose
`idiv` cycle counts the [Lemire
section](#lemire-multiplicative-inverses-at-the-two-division-sites) rests on.
A run elsewhere is a different measurement rather than a repetition, and
should say which machine here.

**The sequence was launched twice and the first attempt is not this run.** It
began at 05:16 and was stopped in its second process on being told the
machine had not been quiet for it; neither of its main-set processes
contributes a figure here, since one process from a busy window and nine from
a quiet one is not the arrangement the procedure's figures are read against.
Its completed max-skip half was read once before deletion, as the disturbed
control [the floor section][floor] now rests on, which is the only use a
discarded process has. The recorded run began at 07:36 on a confirmed empty
process list. What that costs is an hour; what it buys is that every
figure above comes from processes whose conditions are known, which is the
one property no gate here can check afterwards.

**The pair's own identity, transcribed before its note went with it.** Run 11
was measured on `micro-aligned` md5 `a28b3e5b1c409cec6cca64de9f46bb4d`, which
is Run 10's aligned binary unrebuilt, and `micro-maxskip` md5
`98534e7d74d2027561ce9b963ab01fe3`, from `Main.hs` at `2b41e53` — the tree at
`c37abfe` for the second, which is `2b41e53` plus two lines inside one
comment — under GHC 9.12.4 with `-fspec-constr`, with 8192 bytes of padding
on the maxskip half. The aligned half is reproduced by `./make-pair.py
--regime=-fspec-constr`, which is deterministic here; the max-skip half is
not built by that script at all and its recipe was written by hand into the
pair note, `LOOP_MAXSKIP=1 PAD_BYTES=8192` with `-pgma align-as.py` and
`-fforce-recomp`. Those two sums are what a rebuild has to reproduce for this
chapter's figures to be its own — the only thing that makes a paired run
repeatable in principle once the binaries are deleted.

**The shapes have not moved**, for the fifth run running, and neither has
roster membership or roster order: Run 11 measured exactly the shapes and the
arms `Main.hs` holds today, in every population, in the order it holds them.
Its delta is empty in all three halves, and unlike Run 10's that is not an
accident of timing — the run was arranged to make it so.

**The delta, so the population is recoverable.** What follows is the *only*
form in which a shape set or roster is recorded here: its difference from
whatever `Main.hs` holds now. A snapshot would need rewriting at every change
and would be a second copy of a list that already exists; a delta costs what
actually moved and shrinks to nothing when the two agree. A roster delta has
two halves now that membership no longer settles what ran: which arms the
roster held, and which of them it timed. **And a third: the ORDER they ran
in.** Order is not membership, it *can* move code layout, and Run 10 measured
layout at 12 to 14% on the two arms whose loop the shim rescues -- so a delta
stated in membership alone can
read empty while the run is not repeatable. Whether a given reorder moves
anything is a thing to measure rather than assume, both answers having
turned up in one afternoon: `sum-only-early`'s slot-5-to-2 move left all
eight loops this page tracks byte-identical, while lifting it one further
place, above `list`, shifts every worker by ~40 KB and rerolls every
alignment. So record the order, and read the binary before deciding what the
record costs. **A fourth half arrives with the pairing and is not a delta at
all**: which half of the pair a figure came from, which is why the tables
below and the fingerprint say so.

- Run 11 measured today's shapes, today's class lists, today's roster
  membership and today's roster **order**, timing today's 24 of it,
  winsorized per the estimator under `time`. Its delta is empty, the whole of
  it, and the only thing a reader has to carry is which half a figure came
  from: everything published below is `micro-aligned`, and `micro-maxskip`
  contributes the yardstick's second column and the arm-by-arm comparison at
  the head of this chapter.
- Run 10 measured the same shapes, class lists, membership and order, so its
  delta is empty too — what a reader has to carry there is which binary each
  of its figures came from, its Results table being `micro-unaligned`'s while
  its fingerprint and class blocks were `micro-aligned`'s. That mixed basis
  was the transition to this one and lasted the one run.
- Run 9 measured the same shapes, class lists and membership **in a different
  roster ORDER**: `sum-only-early` sat at slot 5, moved to slot 2 ahead of
  the three distant A/A twins after that run, and to slot 1 above `list` for
  Run 10 ([the floor section][floor]). The first move relocated nothing — a
  binary rebuilt from Run 9's own commit `96378d2` puts all eight tracked
  loops at the same offsets as the moved roster does, to the byte — and the
  second relocated everything, which is what Run 10 spent to buy the pool fix
  and its predictions. **Run 11 did not spend it again**, which is the second
  thing alignment bought the schedule: in an aligned build a roster change
  relocates no loop, so the repetition this page had never had was available
  for the first time and is what Run 11 took.
- Run 8 measured today's shapes and today's class lists, on today's roster
  **minus the eight arms written since** (`bq-expand-gm-mulback`,
  `bq-odo-gm-mulback`, `mut-flat-gm`, `offtab-scan-rem` and the four
  `mut-odo-vecdims-add-*`), **timing all of it but `concat-runs`** where today
  leaves 24 untimed, winsorized likewise. Run 7's delta is Run 8's plus the
  regime, which is what keeps the last two columns in [What Run 12 compares
  against](#what-run-12-compares-against) a controlled pair and the first two
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

**The anchor, so a moved baseline is visible** — and on a repetition it is
the one column that could have said the machine had changed under the run.
Every published figure is a ratio to `list`, so a change in `list` itself — a
new compiler, a new machine, a changed `toListT`, or a compiler flag —
rescales the whole table while leaving every ratio intact and undetectable.
These three absolute per-call figures are the guard, and against Run 10's
aligned half they read +0.3%, **+4.3%** and +0.9%. The middle one is the
largest of the three by a factor of five and is worth naming rather than
averaging: it is `list`'s own widest cell in the repetition, the top of the
0.958–1.043 band the head of this chapter reads as drift. (Those three, and
the eleven below, are computed from the cells rather than from the rounded
figures in the table, which do not carry the digits a percentage needs.) The
max-skip half's are given beside them:

| shape | `l` | `list`, per call | net | max-skip, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 5.51 µs | 5.34 µs | 5.24 µs |
| `cifar-L2-16-c64-k3` | 147456 | 3.38 ms | 3.29 ms | 3.10 ms |
| `stretch-wide-2xM` | 1800000 | 34.9 ms | 33.9 ms | 33.8 ms |

Each stride class carries an anchor of its own, beside its table, and across
the repetition the eleven scatter without direction: −1.8% (`bcastmid`) to
+4.3% (`cifar-L2-16-c64-k3`), four down and seven up, where Run 10 read −1.1%
to +7.9% against a run that had moved the baseline's own slot. A baseline
that changed for one mechanism only — under negative strides, say, or a
stride-0 read — is exactly the change a population of ratios cannot show, and
scatter of this size across eleven independent baselines, with nothing
whatever between the two runs, is the best measurement this page has of what
an anchor does on its own.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is 0.587–0.605 ns per element across the whole set, so a raw
slope is the published one plus about `0.60e-9 * l`, with `l`
from `Main.hs`. That recovers any uncorrected figure to within the term's own
3% spread — enough to hold a corrected run against any number
measured before the correction existed. The term itself is within 1% of Run
10's, Run 9's, Run 8's and Run 7's, so neither the flag, the roster, the
layout nor the shim's padding touches the forcing pass, which is the control
saying five runs' corrections are one correction — though the two halves'
terms are not quite identical, the max-skip half reading 0.585–0.604, so a
figure differenced across the halves carries a little of its own.

**What the next run replaces.** Run 11's numbers reach past the Results
table, so this is the list to walk when Run 12's land. Run 10 walked it twice
over and not symmetrically, one half per pass; **Run 11 walked it once**,
alignment being the standing basis and both sides of every comparison
aligned, which is how it is walked from here. It names
*sections*, not
figures: a list of figures is a second copy of them, and enumerating it was
how the previous two versions of this list went stale — one missing six
sections, its predecessor leaking past it. What now guarantees completeness is
mechanical instead. Every section below is reached by an anchor, and the
coverage check is: no section carrying a figure outside a table may be absent
from these links. Run that check, and repeat the two sweeps it cannot replace
— grep this file for figure-shaped numerals outside the tables, and grep it
for the name of the run being superseded, which is the one the chapter head
above still carries — before trusting the list. The second sweep is written
without its numeral on purpose: spelled out, it is a run number the rename
step does not reach, so it would go on naming a run two runs back.

**Inside a section, find the paragraphs rather than reading it.** The list
names sections and a section here runs to hundreds of lines, of which a run
rewrites three or four paragraphs; Run 10's write-up read most of the floor
section to change four of its leads. Every paragraph in this file opens with
a bolded lead, so `grep -n '^\*\*' README.md` between a section's heading
and the next is the section's own contents, and the ones a run touches are
those whose lead or body carries a figure. `--check-doc`'s two sweeps print
line numbers for the comparative and superlative candidates already, so
between the three the walk is a list of jumps rather than a read. This is
deliberately a recipe and not a stored list of paragraph names: a stored one
would be a second copy of the structure and would rot the first time a lead
was reworded, which is the failure this list was rewritten to escape.

- [the head of this chapter](#about-the-last-run-run-11), which carries the
  run's name, regime, scale and source commit, the layout span a roster
  order change alone is worth, and which half published what;
- [the Results table](#results), which `--markdown` emits whole, and the
  findings under it;
- [What Run 12 compares against](#what-run-12-compares-against) — the yardstick
  geomeans in every regime measured and the two-column per-shape fingerprint,
  all of which a run replaces wholesale, and which are the only per-shape record
  kept once the JSON is deleted;
- [The claims Run 12 should test](#the-claims-run-12-should-test), where a run
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
  list](#what-is-open) rather than discharged here;
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
- [What is open](#what-is-open), whose whole content is questions a run
  answers and figures a run moves;
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
