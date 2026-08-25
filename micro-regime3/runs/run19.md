# Run 19 (SpecConstr)

One run's write-up: its head, its Results, what the next run compares against,
the claims that run should test, the eight class blocks, and its own Provenance.
A run replaces this file whole and edits [README.md](../README.md) around it,
in the score of places [the replace list under Provenance there][prov] names ---
the open list among them, which is where a run's registrations, verdicts
and surprises go rather than here. So this file is most of what a run replaces
and by no means all of it. What stands between runs is the harness, [the
procedure][procedure] that makes a file like this one, and the rulings
a measurement does not reach.

**Run 19 (SpecConstr), and what GHC HEAD is worth to this fallback.** Criterion,
**`--ghc-options=-fspec-constr`**; Run 16's regime, shapes, class views
and roster order all unchanged, and the roster is Run 16's: 1128 benches, 47
timed arms over 24 shapes with every stride class at three. **The basis
is the 9.12 half**, `run19-g912`: Run 18's basis recipe with nothing changed
at all, so it carries `-fobject-determinism`, the per-sample instrument
and the saturating preamble, and both halves ran under `WILDLOG=1 SATURATE=1`.
**The control is `run19-ghead`**, the same source and the same shim built
by the in-tree stage1 of the GHC checkout at 10.1.20260803 through
`cabal.project.ghead`, whose freeze resolves the same `vector`, `criterion`
and `criterion-measurement` at the one index-state the other two plans hold ---
so the halves differ in the compiler and its boot libraries and in nothing
a freeze can see, and what they price is a consumer's build on GHC HEAD, library
code recompiled included. The binaries carry `base-4.21.2.0`
with `ghc-internal-9.1204.0` against `base-4.23.0.0`
with `ghc-internal-10.100.0`, criterion 1.6.5.0 on both, and `.text` of 20406469
against 20551487 bytes. md5 `9768189b5c6947beca4ba89cad5800c8` for the basis
and `0ef1fa2cb7686e549d50b414f11086f1` for the control, from `Main.hs`
at `e9fab1e` and `align-as.py` at `40f7a37`; the tree at launch was `0cda6a4`,
with two untracked scratch files and nothing modified. The same desktop, Zen 3,
a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main
processes read *1h37m23s* and *1h37m50s*, at *298 MiB* in use and *131 MiB* max
residency on the basis against *285 MiB* and *125 MiB* on the control.

**The basis half is a repetition, and it is the first here whose rebuild
reproduced its predecessor byte for byte.** `Main.hs` and the shim had not moved
since Run 18 was built, so `run19-g912` IS `run18-g912` --- same md5, same
`.text`, the same tracked fills and the same one 38 B straddler ---
and the md5's one-sided instrument therefore answers positively, every input
proved unmoved with the dependency store among them and no three-read hunt owed.
What that buys is registration 1, read arm for arm on one binary two runs a day
apart: **every one of the 42 arms lands between 0.9836 and 1.0133**, inside
this run's own 2.32% floor, and the movement is uniform rather than per-arm ---
`list` itself reads 0.9918, and the machine check reads **-0.84%** against
the kept fingerprint over 24 of 24 shapes, worst -1.98% and none past 5%.
So the box is where Run 18 left it, the harness reproduces itself to
under a percent on the baseline, and no arm here moved. **What did not reproduce
is the floor**, which the floor paragraph below takes up: the same binary read
1.36% on Run 18 and 2.32% here.

**Every registered ordering holds on GHC HEAD, which is what this pair was built
to answer.** All **thirteen** of the manifest's orderings --- claims 1 to 6
and 9, read off `--claims` rather than off the sentence that registered them ---
hold on 10.1.20260803, and all thirteen hold on 9.12.4: no BROKE on either half.
That is also the reading the retiring claims retire on, the manifest having
been held at thirteen through the run for exactly that, and the eight
the settlement leaves hold on both halves too. **Allocation is where this pair
parts from Run 18's**: **1016 of the 1080** main-set cells that allocate
in earnest match to 1e-4, where the 9.14 pair matched on 1072, and the worst
disagreement is 1.13e-02 on `cnn-slice-c32/bq-expand-qr-prim`. Allocation
is deterministic per call, so those sixty-odd cells are a code change and never
a slot: HEAD allocates differently where 9.14 allocated exactly what 9.12 did.
What did not move is the tiers --- claim 7's levels return per compiler,
and the class blocks read them unbroken in all eight populations. **And the two
columns of this pair may NOT be differenced**: `list`, the denominator of every
ratio here, reads **1.0078** basis over control across the main set, past
the 0.7% that separates a subtractable pair from one that can only be ordered,
where Run 18's read 0.52%. The gate said so before the evening was paid
and the run confirmed it.

**What the compiler is worth, arm by arm, is larger than 9.14 was and
it is one-sided.** Over the 42 arms compared, 18 sit within 1% of 1 at a geomean
of **0.9836**, 30 below and 12 above --- where the 9.14 pair read 0.9913 at 25
below and 17 above. So HEAD is about a point and a half behind 9.12 across
this roster, in one direction. **Eleven arms move past 3%, in five groups.**
Against HEAD are the two fastest pure builds with their A/A twins ---
`bq-odo-gm-mulback` at 0.9270, 0.9282 and 0.9306, and `bq-scan-rem-gm-mulback`
at 0.9397, 0.9400 and 0.9425 --- with `bq-mut-runs-gm-mulback` at 0.9559 behind
them, and the placement-exposed `gen-unsafe` and its twins at 0.9601, 0.9457
and 0.9585. To HEAD's credit is `bq-gen` at **1.0753**, the arm with by far
the dearest table build and the same arm 9.14 led on, there at 1.0926. **A whole
family moving with its own A/A twins is the shape to read**: a twin
is that arm's code at another slot, so three copies moving together is the arm
and not where one of them landed --- which the counted-work paragraph below
confirms outright. The arms the claims rest on stay put: `mut-odo-vecdims`
at 1.0054, `mut-flat-gm` at 0.9975, `bq-expand` at 0.9914.

**This run's floor is 2.32% on the basis half and 1.71% on the control**,
against Run 18's 1.36% and 1.42% over the same eighteen A/A pairs on the same
roster, so both ends loosened while staying well inside Run 17's 3.70%
and 3.89%. The pairs carrying it are `offtab-aa-distant` on the basis
and `build-aa-distant` on the control, and the worst A/A cell of either main set
is **18.50%** on `alexnet-L2-27-c48-k5` on the basis against **17.66%**
on `vgg-14-c512-k3` on the control. Restricted to the six pairs that carry back
to Run 10 the two read **0.49%** and **0.29%**, against Run 18's 0.54% and 0.31%
--- so **the tight six did not move at all and the loosening is entirely
in the twelve outside them**. Sixteen of the eighteen basis intervals cover 1
and seventeen of the control's. Every margin below is judged against 2.32%
and 1.71%, not against the predecessor's. **And this is the sharpest thing
the repetition says**: the basis half is the same binary that read 1.36% a day
earlier, on one box, one roster, one layout and one regime, so a floor
is a property of the RUN and not of the pair or the build --- which is what Run
18 could only guess at when both of its halves tightened together and it had
nothing to hold them against. A margin between 1.36% and 2.32% is one two
consecutive runs of one binary disagree about.

**The two halves' cells resolve differently, and it is the basis half
that is noisier.** `CI%` --- the median half-width of a cell's own fit --- runs
wider on 9.12 than on HEAD across the roster at a geomean of **1.06**,
and the split is 26 arms wider against 21 narrower, so this is a lean and
not a rule. **What carries it is the loose end**: the widest-resolving arms
are the ones that part, `gen-quotrem` 2.85 against 1.62, `build` 1.64 against
1.06 and `bq-gen` 1.43 against 1.02 --- ratios up to **1.76** --- while the arms
that resolve well move either way, `mut-odo-vecdims` 0.65 against 0.54
but `add-in` 0.55 against 0.72 and `offtab` 1.15 against 1.46. Against Run 18
the basis half is where it was --- `mut-odo-vecdims` 0.65 against 0.55,
`bq-expand` 0.61 against 0.60, `build` 1.64 against 1.66 --- so what this pair
shows is the HEAD half resolving BETTER than either, not the 9.12 half
degrading. **That lines up with the floors and is the same fact twice**:
the basis carries the wider floor, 2.32% against 1.71%, and the wider cells,
and it is also the half that carried this run's one exposed bench. Sampling
error inside one bench and agreement between two placements of one strategy
are still different quantities measured by different columns; what is new
is that on this pair they move together, where Run 18 moved them in opposite
directions.

**No wild cell this run either, and the standing free draw came up clean
a second time.** The worst A/A cell of any population is **19.75%**,
on `reshape1-500k` in the basis half's `reshape1` process, against Run 18's
23.03%, Run 17's 74.48% and Run 16's 43.43%; the worst on the control side
is 19.58% on `bcastmid-c32-cnn`. So the whole run's worst cell is tighter
than its predecessor's and nothing in it approaches the class the two runs
before that produced. `revsome`, the population Run 17 found loose at an 18.05%
floor, reads **2.00%** on the basis half, the tightest of that half's eight ---
though 5.96% on the control's, which is a reminder that a class floor is one
process's. Its looseness has now failed to repeat twice running against Run 17's
18.05%, which retires the reading that it was a property of that mechanism.

**One exposed bench in eighteen processes, and this run can name what did it.**
Seventeen of the eighteen report no bench reaching 0.25 foreign CPU. The basis
main process reports exactly one of its 1128 --- `cnn-L1-6x6-c1/bq-expand`,
at **0.35** foreign with a worst sample of 201 ms --- and what was running
is known rather than inferred: a Claude Code update installing itself, named
by the machine's owner, as Run 18's intruder was. **Its own A/A twins price it,
which is what turns the exposure into a measurement rather than a caveat.**
The exposed copy reads 1.5537e-06 where its two twins --- the same code at two
other slots in the same process, on the same shape --- read 1.5227e-06
and 1.5199e-06 and agree with each other to **0.19%**, so the cell sits 2.0
to 2.2% above where its own code reads beside it, and its own fit is 2.3 and 5.8
times their width; on the control half the same three agree to 0.53%. One shape
of 24 at 2.1% moves that arm's geomean by under **0.09%**, an order of magnitude
inside the floor, and winsorization bounds it further. **The rerun step 1c asks
for was NOT taken, and on 2026-08-25 it was DECLINED rather than deferred** ---
the decision being whoever asked for the run's, as every decision about what
the machine is spent on is. What it would have cost: both main halves in one
quiet window, a pair read across two windows not being a pair,
and `run-major.sh` has no population filter, so three and a quarter hours
hand-driven or six and a half through the driver. What it would have bought
is priced above and is under 0.09% on one arm of one half. **So this run
publishes a main set carrying one exposed bench, and says so here rather
than anywhere it could be missed.** Nothing else in the run is touched:
the eight class populations and the whole control half are clean. **The rule
is not weakened by the decision** --- 1c still says rerun, a later run meeting
a real intrusion still owes one, and what made this exposure declinable
is that the A/A twins priced it, which is a thing a run has to do BEFORE it can
decide anything of the sort.

**The counted-work instrument is in the reader now, and it cuts this pair's
movements in two.** `run-counts.sh` counts instructions an iteration from two
fixed-`-n` processes a cell and owes criterion nothing; for two runs the reading
off it was hand-rolled at the write-up, which this file's own standing
instruction calls a defect report against the reader, so `--counts` was built
here with two cases behind it and the hand-rolling retired. **What is codegen**:
the fast pure tier's whole loss. `bq-odo-gm-mulback` reads a count ratio
of **0.9340** against its time ratio of 0.9270, and `bq-scan-rem-gm-mulback`
**0.9422** against 0.9397, leaving time-over-counts at 0.9925 and 0.9973, within
a percent of 1 --- and each arm's two A/A twins carry the SAME count ratio
to four figures, which is the second reason it is the arm and not a slot. HEAD
simply emits 7.1% and 6.1% more instructions for these two. **What
is not codegen**: `gen-unsafe` and its twins move 4.0 to 5.4% in time at count
ratios of **1.0000**, `mut-odo` 2.5% at 1.0000 and `offtab` 1.2% at 1.0000 ---
the placement-exposed family, exactly as Run 18 found it --- and **`bq-gen`,
the largest movement to HEAD's credit at +7.5%, sits at 1.0019**. HEAD hands
it the same instructions and runs them in seven percent fewer cycles, which
no clock in the README could have told from a code change. So Run 14's standing
caution --- read per-arm magnitudes as criterion's --- survives,
with a non-clock instrument now saying which movements are code.

**And the counted work now covers every population, which it had never done:
it swept the main set alone until 2026-08-25.** Sixteen further sweeps, both
halves over all eight classes, 141 cells apiece and no cell perf refused.
**Seven of the eight classes read as the main set does** --- every arm together
at a count geomean of 0.9892 to 0.9953, HEAD emitting about a percent more,
with `bq-odo-gm-mulback` the most extreme arm in six of them at 0.9167
to 0.9290. **`reshape1` inverts, and its whole class does**: 1.0032 over every
arm, `bq-odo-gm-mulback` at 1.0066 rather than 0.93, and the extreme arm
is `mut-odo-vecdims-add-both-down` at **1.0603** --- HEAD emitting 5.7% FEWER
instructions where everywhere else it emits more. `window` splits the same way
inside itself.

**What sorts them is the unit innermost extent, and the rule is clean over five
shapes in three populations.** Wherever `sInner` is 1, `bq-odo-gm-mulback`'s
HEAD penalty is absent: `stretch-inner1` 1.0000 --- 16,005,915 instructions
against 16,005,919, four apart in sixteen million --- `reshape1`'s three shapes
1.0000, 1.0032 and 1.0169, and `window-64x64-k1x9` 1.0099. Everywhere else
it runs **0.9149 to 0.9702**, and the far end of that is `stretch-rank12`
at `sInner` 2 --- the one shape between absent and the band, which is what
a graded effect would look like rather than a switched one, which is HEAD +5.4%
to +9.3%. And the same shapes are where `mut-odo-vecdims-add-both-down` gains
most, -4.5% to -6.3%. So whatever HEAD does differently to this odometer is
on a path a unit innermost dimension does not take, and one arm's regression
and another's improvement are the same event seen twice. **That is a mechanism
claim and it is registered rather than settled**: nothing here reads the code,
and the next run can kill it with any `sInner` of 1 that shows the penalty.

**And the correction sits on nearly the same footing in both halves, as it did
on Run 17's and Run 18's.** The in-situ forcing term --- an arm minus
its `-nosum` twin, against the `sum-only` the correction actually subtracts ---
reads 1.0282, 1.0295 and 1.0552 as medians on the basis and 1.0267, 1.0347
and 1.0492 on the control, on `mut-odo-vecdims`, `mut-flat-gm` and `bq-expand`.
So both halves subtract a term between about 3% and 6% under the in-situ pass,
tilting the same way on all three arms and agreeing with each other to within
0.15, 0.52 and 0.60 of a point, and **a margin between these two halves
is therefore not carrying a correction bias**. The two `sum-only` halves agree
at 0.9996 on the basis and 1.0001 on the control, worst cells 0.71% and 0.58%.
Every one of those figures is within a few thousandths of Run 18's, on a pair
one of whose halves is a compiler that did not exist when the correction
was designed. What both halves still carry is scatter, worst cells past 100%
on `stretch-inner256` as before --- so the term is even on the median and wild
per cell, which is a reason to read medians rather than a reason to distrust
them.

**The add-in split repeats on a third compiler, and the slot account fails
the first test that could have refuted it.** `mut-odo-vecdims-add-in` against
the arm it varies reads **0.9755 at 19 of 24, sign p 0.0066** on the 9.12 half
and **0.9991 at 14 of 24, p 0.54** on HEAD --- the same shape Run 18 read across
9.12 and 9.14, and on the HEAD side the same win count and the same p to two
figures. So the margin is a property of the compiler and not of the arm, now
three times over. **What is new is that the offsets no longer follow it.** Run
18 read the swap off a `-g3` twin per compiler, each reproducing its timed
binary's tracked offsets a flat `0x40` below; on HEAD the twin does not locate
anything, reading `[0, 31, 31, 21]` where the timed binary reads
`[23, 0, 1, 2]`, at address deltas of `0x45A9`, `0x49DF`, `0xF65E` and `0xFC13`
rather than one constant, and byte identity cannot stand in, the four copies
being one 28 B sequence by construction. Under the ascending-address
correspondence --- which the 9.12 half satisfies, which nothing on the HEAD half
checks, and which is stated here as the assumption it is --- HEAD puts
`mut-odo-vecdims` at 0 and `add-in` at 23, the SAME arrangement as 9.12, where
9.14 had the two swapped. A slot account predicts 9.12's margin there, and
it is absent. **So either the correspondence fails on HEAD or the margin does
not follow the slot, and this pair cannot separate those two** --- what
it removes is the reading that made the slot the answer. The control pair says
as much on its own: `build` against `mut-odo` reads 0.9633 on the basis
and **0.9325** on HEAD, both well below 1, where Run 18 had it split 0.9751
against 1.0006 --- so between compilers the control moved three points,
in the direction the add-in pair did not. [The add-in entry][open] carries all
of it; the twins were built and read before the run and then deleted,
and `run19-pair.txt` keeps the named offsets.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512`
on the basis, and 2408978 against 2408530 on the control, where plain -O1
separates the two tenfold. The two compilers put the scan arm's own allocation
48 bytes apart and the mutable arm's at the same byte.
On the confirm-don't-rebuild path this run took, with no build to have carried
the flag, that is the only check standing between a mistyped regime
and the hours.

**Run 19 records every population twice** --- the main set and all eight stride
classes from each half, one process each, which is what makes its class readings
a pair rather than a basis alone --- and **the eighteen processes come from one
unbroken window**, 00:21:14 to 06:52:34, each exiting 0 at the bench count
its roster holds, 1128 twice and 141 sixteen times, with no process reporting
a selection it did not ask for and none rerun. The sixteen class processes span
12m11s to 12m19s, an eight-second spread over six and a half hours.
**The control half ran first throughout**, `ghead` before `g912` on the main set
and on each class in turn, which is the driver's order --- so *the 9.12 half*
and *the second process of the two* again name the same nine processes,
and this run took no order probe to separate them, where Run 18 broke that tie
on one class. **The alone-leg riders followed the sequence** rather than sitting
inside it, 108 single-bench processes over four invocations of 27 --- the 24
shapes plus a second reading of the three anchors, each half clean
and saturated, which is the pair of columns registration 3's decomposition
needs.

**The decomposition reproduces on both halves, and the roster's own share came
in smaller than Run 18's.** The riders time each shape's `list` by itself, one
bench per process on that half's own binary, `SAT=` off and on,
and the saturated legs split the deflation into the state the preamble puts
on a clean process --- **+11.73%** on the basis and **+12.57%** on the control
--- and the rest the roster adds on top of it, **+0.31%** and **+0.72%**, both
geomeans inside their halves' floors. Run 18 read +11.43% and +1.20%
on its basis, so the state term reproduces across a compiler while the roster's
own contribution fell to under a point on both halves. **The two tails
are the same shape on both halves**, `stretch-tall-Mx2` at 1.0838 and 1.0998,
which makes it a roster effect on one shape rather than a term belonging
to either compiler. Both readings are raw slope against raw slope, an alone leg
carrying no `sum-only` bench to correct with, so no correction convention enters
either. What this run could NOT read off the riders is the two halves' level
against each other outside a roster, Run 18's 1.0031: no reader mode produces
it, and it is left to the next run rather than hand-rolled here.

**Everything in this file is replaced by the next run, which is what makes
it a file.** That sentence was the one paragraph here Run 19 did not rewrite,
and it read *everything in this chapter*; the split of 2026-08-25 rewrote
it to say *file*, so what it can no longer claim of itself is the identity
that was its whole point --- and it stands on the run before it now, as every
other paragraph here does. What a run replaces OUTSIDE it, in README.md
and in the sources, is [README's own Provenance](../README.md#provenance). None
of it is portable: a run on another machine is a different measurement rather
than a repetition, which this run is in a position to be firm about, having
repeated one binary on one box and moved its floor by 1.7x.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries
that decision and this run's re-pass of its gates), the scratch vectors
are the unboxed ones the shipped code uses, as they have been since Run 7 ([the
scratch vector flavour](../README.md#the-scratch-vector-flavour) says what
that severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under. **A row's distance from Run 18's basis
column IS drift alone, and this is the first run that can say so flatly**:
the flag, the roster, the order, the allocation area, the box and the binary
are all the same ones, the basis half being Run 18's basis rebuilt to the same
md5, so nothing but the evening separates the two columns. Every arm bore
that out, landing between 0.9836 and 1.0133 with `list` itself at 0.9918.
This pair's halves differ in the compiler, so they differ in layout
by construction; but on this run the arms that moved between them are mostly
not the placement-exposed six, and the counted-work instrument says which
are which rather than leaving it to be assumed --- `bq-odo-gm-mulback`
and `bq-scan-rem-gm-mulback` moved six to seven percent on their instruction
counts, while `gen-unsafe`, `mut-odo` and `offtab` moved four, two and one
at count ratios of 1.0000. Read a cross-half distance here as codegen where
the counts moved and as placement or runtime where they did not, and read
a distance from Run 18's column as drift.

**And it is the basis half's**, `run19-g912`, as every published table here
is from Run 11 on: the control half's column is one column on the yardstick
below rather than a second copy of these thirty-odd rows. That the published
half is the 9.12 one is this pair's own decision --- it keeps the lineage, being
Run 18's basis recipe with nothing changed at all --- and the HEAD half
is the yardstick column.

**Comparing runs?** The table below is Run 19's own; what to hold a new run
against is [What the next run compares
against](#what-the-next-run-compares-against), the claims to test are [the ones
after it](#the-claims-the-next-run-should-test), the absolute anchor
is under [Provenance](#provenance) below and the population it was measured
over in [README's delta chain](../README.md#provenance), and this run's own
floor --- no A/A pair further than 2.32% from 1 on the basis half or 1.71%
on the control, on worst single cells of 18.50% and 17.66%, and 0.49% and 0.29%
read on the six pairs that carry across runs --- is [in the floor
section][floor]. The eighteen-pair figure governs an arm against *itself*; what
two different rows of the table below must clear is the SIX-pair one, 0.49%
here, that being the pair that carries across runs --- and in a build whose loop
heads the shim has already placed, two rows are separated by their code
and no longer by where each landed --- which is what Run 10 spent two binaries
to establish and every run since has inherited.

**It is the main set's table**, and every column below is a statistic
of that population: each stride class has a table of its own, on the same rows
and in the same columns but its own basis, in [The stride classes, run
by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*,
  less that shape's forcing term, over `list`'s slope less the same term,
  with the per-shape log-ratios *winsorized* first --- capped at the row's own
  median plus or minus three MADs. Nothing is dropped, so all rows cover one
  population and any two columns are comparable; a cell far enough out
  to distort the mean has its influence bounded instead of its evidence deleted.
  The `CI%`, `worst`, `smp` and `alloc` columns stay raw: subtracting a shared
  term moves a point estimate, it does not make a cell better measured.

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
  on which that strategy does least well against the baseline. It is what claim
  1 is about, and it is raw rather than winsorized.
- **CI%** is the median across shapes of the slope's confidence interval
  as a percentage of the slope --- "how many digits are real". 0.5% is three; 5%
  is one.
- **smp** is the median sample count. Criterion spends a time budget, so a slow
  call buys fewer samples; this is where that shows.
- **alloc** is bytes per call as a multiple of the result vector (`8*l`),
  the median over shapes of the `allocated` fit the harness now runs on every
  bench of every shape. The multiples were held to be shape-independent ---
  refitted on a different shape, every one reproduced to within 0.4% ---
  so that the median was a formality rather than a smoothing and the column did
  not move with what it was fitted on. **That is wrong**, and Run 6 (-O1)
  reproduced the refutation at full budget where a rough pass had found it.
  Re-derived on Run 9's cells and roster it is unanimous: **every one of the 32
  benched rows** varies by more than 5% from shape to shape, the median row
  by 2.00x and the worst by 5.10x (`bq-expand-b`, 1.00x to 5.10x), and the four
  shapes of identical `l` = 1800000 give `bq-expand` 2.000x, 2.111x, 1.000x
  and 2.639x. The spread narrowed as the roster was cut --- Run 6's worst
  was an arm nothing times any more --- and the property it measures did not.
  Every allocated fit sat at R^2 1.000 on Run 6, so the spread is the quantity
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
| *bq-expand-nosum* | *--* | *--* | *0.53* | *78* | *2.35x* | *its base arm, forced with one element* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.68* | *92* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.54* | *90* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *101* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *101* | *0.00x* | *the same, at the other end* |
| mut-odo-vecdims-add-in | 0.054 | 0.126 | 0.55 | 80 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa* | *0.055* | *0.126* | *0.60* | *80* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.055** | 0.126 | 0.65 | 80 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa-distant* | *0.055* | *0.126* | *0.54* | *80* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-both-down | 0.058 | 0.126 | 0.60 | 80 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-both | 0.059 | 0.126 | 0.61 | 79 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-out | 0.060 | 0.126 | 0.62 | 78 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.083 | 0.184 | 0.71 | 82 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.090 | 0.181 | 0.72 | 80 | 1.33x | mutable `Int` scratch |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.097* | *0.155* | *0.59* | *74* | *1.33x* | *A/A control* |
| **bq-scan-rem-gm-mulback** | **0.098** | 0.155 | 0.52 | 74 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.155* | *0.37* | *74* | *1.33x* | *A/A control* |
| bq-mut-runs | 0.100 | 0.198 | 0.75 | 75 | 1.33x | mutable `Int` scratch |
| bq-odo-gm-mulback | 0.100 | 0.178 | 0.50 | 78 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-adjacent* | *0.100* | *0.177* | *0.55* | *78* | *1.51x* | *A/A control* |
| *bq-odo-gm-mulback-aa-distant* | *0.100* | *0.180* | *0.54* | *78* | *1.51x* | *A/A control* |
| *build-aa-distant* | *0.102* | *0.269* | *1.93* | *71* | *1.00x* | *A/A control* |
| *build-aa-adjacent* | *0.102* | *0.249* | *1.59* | *72* | *1.00x* | *A/A control* |
| build | 0.103 | 0.263 | 1.64 | 71 | 1.00x | new mutating `Vector` method |
| bq-expand-gm-mulback | 0.103 | 0.226 | 0.70 | 78 | 2.35x | nothing (pure) |
| *mut-odo-aa-adjacent* | *0.104* | *0.273* | *1.61* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-distant* | *0.105* | *0.286* | *1.79* | *70* | *1.00x* | *A/A control* |
| mut-odo | 0.106 | 0.268 | 1.41 | 70 | 1.00x | new mutating `Vector` method |
| bq-expand-b | 0.113 | 0.230 | 0.55 | 74 | 2.18x | nothing (pure) |
| bq-expand-qr-prim | 0.114 | 0.232 | 0.61 | 74 | 2.35x | nothing (pure) |
| bq-expand | 0.115 | 0.231 | 0.61 | 74 | 2.35x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.115* | *0.232* | *0.55* | *74* | *2.35x* | *A/A control* |
| *bq-expand-aa-distant* | *0.115* | *0.233* | *0.41* | *74* | *2.35x* | *A/A control* |
| bq-expand-zf | 0.117 | 0.251 | 0.53 | 73 | 2.35x | nothing (pure) |
| offtab-scan-rem | 0.130 | 0.223 | 0.89 | 72 | 2.00x | nothing (pure) |
| offtab | 0.134 | 0.298 | 1.15 | 66 | 2.00x | mutable `Int` scratch |
| *offtab-aa-adjacent* | *0.135* | *0.290* | *1.32* | *66* | *2.00x* | *A/A control* |
| *offtab-aa-distant* | *0.137* | *0.290* | *1.24* | *66* | *2.00x* | *A/A control* |
| bq-mut | 0.148 | 0.297 | 0.97 | 64 | 1.33x | mutable `Int` scratch |
| bq-gen | 0.370 | 2.104 | 1.43 | 50 | 1.33x | nothing (pure) |
| *list-aa-distant* | *0.999* | *1.011* | *0.44* | *35* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.49 | 35 | 23.50x | -- |
| *list-aa-adjacent* | *1.001* | *1.009* | *0.45* | *35* | *23.50x* | *A/A control* |
| *gen-unsafe-aa-adjacent* | *1.053* | *2.847* | *1.90* | *40* | *1.00x* | *A/A control* |
| gen-unsafe | 1.059 | 2.850 | 1.69 | 40 | 1.00x | -- |
| *gen-unsafe-aa-distant* | *1.061* | *2.792* | *1.52* | *40* | *1.00x* | *A/A control* |
| gen-quotrem | 1.097 | 2.946 | 2.85 | 40 | 1.00x | 1st attempt |

`concat-runs` has no row, and neither do the other 23 arms the roster holds
and checks without timing: the reason is at each entry and the count
is [`--lint`'s](../README.md#the-reader-read-runpy). No row here is a first
reading, the roster's membership being Run 16's exactly, so every movement below
is a movement and not a new arm arriving.

**Three things in the table are the run's findings rather than its numbers.**
**The whole table reproduced against Run 18's basis column**, and this time
on absolutes as well as ratios, the box having held still and the binary being
the same one: of the eight yardstick rows, **five are identical** ---
`mut-odo-vecdims`, `bq-odo-gm-mulback`, `bq-expand`, `build` and `offtab`
at 0.055, 0.100, 0.115, 0.103 and 0.134, `bq-expand` reading 0.9927 paired
besides --- and **three move**: `mut-flat-gm` 0.083 against 0.084
and `bq-mut-runs-gm-mulback` 0.090 against 0.089 by a thousandth,
`bq-scan-rem-gm-mulback` 0.098 against 0.096 by two. That is what one binary run
twice ought to look like, and it is close to the only other same-binary
repetition here: Run 11's aligned column against Run 10's reads four identical
and four moving, none by more than a thousandth. This run has more rows
identical and fewer moving, and one row moving further, so neither is flatly
tighter than the other. **The ceiling reproduced on the arm the class property
names**: `mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm
outside the family's own tier, reads **0.5572 at 23 wins of 24** and sign p
3e-06, against Run 18's 0.5577 at the same 23 of 24, Run 17's 0.5446 and Run
16's 0.5567 --- the figure [the ruling](../README.md#the-mutable-ceiling-taken)
turns on. **What is unmoved by the compiler is the ORDERING and
not the figure**: 23 of 24 and p 3e-06 hold on both halves, while the ratio
itself reads **0.5208** on HEAD, 6.5% from the basis's and three times
its floor, which turns 1.79x into 1.92x. **And the `alloc` column is Run 15's
through Run 18's at every level, while the CELLS behind it are not**: the two
halves agree on **1016 of 1080** allocating cells where the 9.14 pair agreed
on 1072, so on this pair of compilers the column says the tiers did not change
and the cell count says HEAD's code did.

**The series Run 14 opened on sub-percent margins has a tenth and an eleventh
reading, and they split as the last pair's did.** `mut-odo-vecdims-add-in`
against the arm it varies read 1.0009 at 13 of 24 in Run 10, 0.9934 at 21 in Run
13, 0.9967 at 13 in Run 14, 1.0023 at 14 in Run 15, 1.0043 at 12 in Run 16,
0.9889 at 19 and 0.9709 at 21 on Run 17's two halves and 0.9813 at 19 and 1.0016
at 14 on Run 18's --- and here it reads **0.9755 at 19 of 24, sign p 0.0066**
on the 9.12 half and **0.9991 at 14 of 24, p 0.54** on the HEAD half. So the two
halves of this pair do not agree in direction, the difference between them
is the compiler, and the HEAD half repeats Run 18's 9.14 win count and p
exactly. **What Run 18 read off the `-g3` twins, this run cannot**: on HEAD
the twin does not reproduce the timed binary's offsets, so the swap that made
9.12 against 9.14 look like a slot effect has no counterpart here ---
and under the correspondence that is left, HEAD arranges the two arms as 9.12
does while the margin is absent. [Its own entry][open] carries the whole of it,
the control beside it, and what is still missing, which is now the mechanism
as well as the magnitude.

**And the other standing control moved further this run, and in ONE direction
--- which is what stops the add-in split being read as placement.** `build`
against `mut-odo` --- one worker at two slots, and the pair the README prices
at 0.86 to 1.24 across its history --- reads **0.9633 at 18 of 24, sign p
0.023** on the 9.12 half and **0.9325 at 20 of 24, p 0.0015** on the HEAD half.
That is NOT the shape of the add-in split: both halves sit well below 1 where
the add-in pair has one half below and one at it, and the two copies sit
at cache-line offset **0 in both compilers** on 9.12's twin, the only twin
that can still be read. Run 18 had this pair split 0.9751 against 1.0006,
so between compilers it has now moved three points in the direction the add-in
pair did not. **A slot account of the add-in margin has to explain a control
that moves as much or more with no slot change, and it still cannot.** Their
per-shape ranges remain the finding rather than their geomeans, **0.867..1.073**
on the basis and **0.774..1.015** on the control, so on HEAD the two slots
disagree by more than two tenths on a single shape --- and this run is the first
where the pair does NOT agree to within a floor over the set either, 3.67%
against a 2.32% floor on the basis and 6.75% against 1.71% on HEAD.


## What the next run compares against

**Run 20's regime, roster and basis are settled; its pair is not, and
that is the one decision it owes before anything is built.** The regime
is `-fspec-constr`, as every run since Run 8, and it is the regime the claims
decide in; the shipped file does not set the flag ([the
ceiling](../README.md#the-mutable-ceiling-taken)). **The roster is no longer Run
16's, and Run 20 is the run that changes it**: the rework's arms landed
2026-08-25 --- `canon-vecdims` and its memcpy-run form `canon-memcpy-r2`,
the zero-stride conditions `bcast-set` and `mid-copy`, and the endpoint
`canon-full` --- and three placement-family arms dropped to `Only` beside them,
so the timed roster is 53 arms over the same 24 shapes and 1272 benches, where
Run 19 ran 47 and 1128. The sixth of the block is `canon-full-nosum`, a fourth
in-situ forcing control, the three standing ones all being element-wise fills
where the endpoint's write pattern varies by shape. **And two classes go to four
shapes on 2026-08-25**: `reshape1-strided-r3` joins `reshape1` --- the same
dense shape as `reshape1-r3` viewed with its innermost two dimensions transposed
before the size-1 dim is appended, so dropping that dim leaves a strided view
where the class's other three leave a contiguous run, without which
the canonicalizing arms measure dispatch in this class and not filling ---
and `bcastmid-block150k` joins `bcastmid`, its block taken to 150000 elements
where the class's blocks ran 3 to 216, the block-copy arm's best case where
`bcastmid-b200k` is its worst. The other six classes stay at three, so the class
view set is 26 shapes and 1378 benches, and those two processes run four shapes
where the rest run three. The allocation area is fixed at `-A32m` and no pair
will vary it again: Runs 14, 15 and 16 priced it, the decision of 2026-08-21
closed it, and the 24m/48m probe that could have reopened it was taken ahead
of Run 17 and killed. The basis is `run19-g912`'s recipe --- ghc-9.12.4,
`-fobject-determinism`, the per-sample instrument and the saturating preamble,
run under `WILDLOG=1 SATURATE=1` --- which is now the same recipe three runs
running and reproduces byte for byte, so a Run 20 basis that does not is itself
a finding. **Run 20 is a pair, and the roster change is its variable** ---
decided 2026-08-25. `run20-g912` carries the 53 timed arms and `run20-r19roster`
Run 19's 47, one compiler, one shim, one shim setting and one machine apart
from the roster itself --- and the control's name deliberately does not begin
with the basis's, `install-tables.sh` refusing a half caught by its own
`$R-$BASIS-*.json` glob. The two do NOT share source, which every pair before
this one did: the roster is in `Main.hs`, so the halves are two source states
and the pair note records both. so what the pair prices is what five new
functions did to the layout of the arms that were already there. Run 10 measured
a reorder at 12 to 14% on the two arms whose loop the shim rescues, and each
half's own eighteen A/A pairs bound only what is inside it, so nothing else here
can read that. It costs the second half of the machine: about thirteen hours
of processes rather than six and a half. **And the question a purpose-built pair
was owed for is gone.** That question was the `add-in` placement one, which
wanted one compiler, one source and two shims placing the two arms at swapped
cache-line offsets --- Run 18 thought a compiler pair gave it for free and Run
19 showed the free route does not carry, the `-g3` twin naming HEAD's four
functions and unable to locate them --- and it was **parked 2026-08-25** ([its
own entry][open]), the margin being too small to move the shipping choice
whichever way it came out. So the pair above is not owed to it, and the three
arms it turned on stopped costing benches the same day. **What that rules out
is a second variable, not the roster change itself.** A roster change confounds
whatever a pair varies, so a Run 20 that both extends the roster and varies
something else can attribute neither; and another compiler pair is ruled out
on its own evidence, HEAD and 9.14 both having been read and both having said
the same thing about the orderings. **What the roster change costs, and
it is not a caveat but the run's own subject**: five new functions move every
address, so Run 20 cannot reproduce Run 19 byte for byte and **does not owe
it** --- the md5 comparison and the three-read hunt a moved md5 usually triggers
are both off for this run, decided 2026-08-25, and saying so here is what stops
a session hunting a difference the roster explains. What holds the build
to something instead is the gate's machine check, `list`'s net per shape against
Run 19's kept fingerprint; the 47 arms both halves and Run 19 all carry, read
against its columns; and each half's own eighteen A/A pairs for its floor.
**And one thing to expect of the write-up**, now that the sibling is in:
`reshape1`'s other three shapes still go degenerate for the canonicalizing arms,
whose cells there measure dispatch rather than filling, so that class's geomean
for them mixes three dispatch cells with one fill cell and its paragraph has
to say which is which. `reshape1-strided-r3` is the only cell in the class
that prices the fill. **And one thing it does NOT owe**: Run 19's main-set
rerun, declined on 2026-08-25 rather than carried forward, so Run 20 inherits
no backlog from it.

**What Run 19 leaves it to read against, and the first item is not a figure.**
**The box did not change**, its machine check reading -0.84% against the kept
fingerprint over 24 of 24 shapes, worst -1.98%; so absolutes cross from Run 18
to Run 19 freely and the boundary that matters is still the BIOS change before
Run 18, which no absolute crosses. **The floor is 2.32% on the basis and 1.71%
on the control**, with the restricted six at 0.49% and 0.29%. A Run 20 margin
is judged on both and they answer different questions: the six-pair figure
is what two rows of one table must clear, the eighteen-pair one is how far
an arm differs from its own duplicate. **And it is not inherited from the pair
or the build**: Run 19's basis is Run 18's basis binary byte for byte and read
2.32% where that binary read 1.36%, so the floor is re-drawn per run and a Run
20 margin is judged against Run 20's own, never against these. **The two columns
below may NOT be differenced**: `list` moved **0.78%** between the halves, past
the 0.7% that separates a subtractable pair from one that can only be ordered,
where Run 18 read 0.52%. What they price is a compiler, and this run stopped
guessing which movements that reaches: the counted-work column puts
`bq-odo-gm-mulback` and `bq-scan-rem-gm-mulback` six to seven percent apart
ON their instruction counts, and the placement-exposed arms (`build`, `offtab`,
`mut-odo`, `gen-unsafe`, `gen-quotrem`, `bq-mut`) apart at count ratios
of 1.0000. So a Run 20 movement on one of those six is layout or runtime until
the counts say otherwise --- and the counts are one `--counts` call away now,
which is the reading Run 19 built rather than hand-rolled.

**Registered with the pair.** Run 19's six registrations, their kill conditions
and their verdicts are [in the open list](../README.md#what-is-open);
the commands are `run19-pair.txt`'s. **What Run 20 inherits is four riders
that are now routine and one instrument that is new.** The alone legs,
the counted-work sweeps, the saturating preamble and the per-sample load fields
all ran to form and want no re-deciding; `--counts` is the new one,
and it retires the hand-rolled reading two write-ups had been doing ---
so registration 4's shape for Run 20 is a call and not a computation. **What
it inherits as a debt** is nothing, Run 19's un-taken main-set rerun having
been declined rather than deferred, and **what it inherits as a warning**
is that the floor is re-drawn per run: Run 19's basis read 2.32% where the same
binary read 1.36% a day earlier, so a Run 20 margin is judged against Run 20's
own floor and against no predecessor's.

**The position term was the candidate Run 15 promoted, and the probes have since
spent it.** What Run 14 first saw and Run 15 confirmed is resolved
as small-pinned churn --- selector found, ladder re-sized, no poison set ---
in [the position-term entry][open]
and `small-pinned-churn-investigation/nursery-position-findings2.txt`,
so the roster-order pair this paragraph used to ask for is not owed:
the corrected scans priced the term per shape in filtered processes, without
a pair and without a layout term to argue about.

**The allocation area has now been priced twice and does not want a third pair**
--- a ruling superseded in scope, 2026-08-19, and kept because what it refused
stays refused. Run 14 took the area at `-A1G` and could not subtract its halves'
absolutes; Run 15 took it at `-A32m` and found the cost at about 6%
of the roster's time --- so re-PRICING default-against-enlarged is spent,
and Run 16's pair does not do that: it changes the published basis to `-A32m`
and reads `-A64m` against it, the one comparison neither earlier pair made
and the one the churn findings' recommendation turns on, in the saturated
in-process state both halves share. On 2026-08-21 the area was fixed at `-A32m`
outright, here and in every horde-ad suite, so the one-binary runner
this section used to ask for is not owed, and no further `-A` question
is the README's.

**Run 16 contributed two columns.** They
are `Run 16 (SpecConstr, max-skip +lookrts, -A32m)` --- that run's basis,
and the first `-A32m` column published as one ---
and `Run 16 (SpecConstr, max-skip +lookrts, -A64m)`. The basis column was read
against Run 15's `-A32m` column arm for arm and reproduced it, seven of eight
rows within a thousandth, which is what licensed the change of basis; the -O1
column stays the yardstick for a comparison of the two regimes.

**Which Run 15 half a comparison uses is settled here rather than per
paragraph**, the basis change having made *against Run 15* ambiguous
for the first time. Absolutes and anchors go against `run15-a32m`, the half
at that run's own area, and Run 16 bore that decision out. **The six figures
that follow are Run 16's and are no longer checkable here**, `run15-*`
and `run16-*` having been deleted; they are kept because the RULING is what
this paragraph is for and the numbers are the evidence it was taken on, and they
are stamped so that no later run reads them as its own. Against `run15-a32m` Run
16's three anchors read **-0.66%, -1.01% and -0.06%**, every one well inside
the 2.32% floor it measured; against `run15-lookrts` the same three would have
read **+8.81%, -9.57% and +7.74%**, which is the allocation area and
not the shapes, and would have put all three outside that floor for a reason
that is not theirs. The published lineage and the yardstick column go against
`run15-lookrts`, which is what Runs 8 to 15 are read through and what a rebasing
would cost this table. **The two rules answer different questions and neither
overrides the other**: `run15-a32m` is what the basis change is CHECKED against,
arm for arm, because it is the half at this run's own area; `run15-lookrts`
is what the lineage is READ through, because it is the column every run from 8
to 15 published. A row's distance from the lookrts column is therefore the area
plus whatever else moved, and only its distance from the a32m column is drift.

**Run 13 contributed two columns, and the second names a shim setting and an RTS
line at once.** `Run 13 (SpecConstr, max-skip)` is the basis, Run 12's basis
recipe unchanged; `Run 13 (SpecConstr, max-skip +lookrts)` is the same source
and compile with the shim's look-through and an RTS default of `-I0 -T -M8G`
in place of `-T -M2G`. The two changes are deliberately not separable ---
the pair varies both by request --- so read the columns as pricing the package
and never either change alone.

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
to catch --- the check cannot demand an unaligned half of every pair without
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
is a further thing again --- the same binary twice, which is drift and nothing
else.

**Neither of the older columns is to be pruned**, however much each looks like
a leftover. The -O1 one is the only place Run 7's basis survives, so deleting
it leaves any comparison of the two regimes with no yardstick at all and nothing
to recover one from once the artifacts are gone --- and it is now the *only*
form that comparison can take, the -O1 run that would have replaced this column
being retired with its premise; `--check-doc` fails if the column disappears.
The Run 8 one is now load-bearing for a second reason: its four bottom rows name
arms **nothing times any more**, so with Run 8's Results table replaced above
and its JSON deleted, this is the only record they have left. The rows nearest
the decisions, in every regime that has measured them, so no comparison needs
another section:

| strategy | Run 19 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 19 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.14.1) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, instrumented) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, plain) | Run 16 (SpecConstr, max-skip +lookrts, -A32m) | Run 16 (SpecConstr, max-skip +lookrts, -A64m) | Run 15 (SpecConstr, max-skip +lookrts) | Run 15 (SpecConstr, max-skip +lookrts +A32m) | Run 14 (SpecConstr, max-skip +lookrts) | Run 14 (SpecConstr, max-skip +lookrts +A1G) | Run 13 (SpecConstr, max-skip) | Run 13 (SpecConstr, max-skip +lookrts) | Run 12 (SpecConstr, max-skip) | Run 12 (SpecConstr, max-skip +procalign) | Run 11 (SpecConstr, aligned) | Run 11 (SpecConstr, max-skip) | Run 10 (SpecConstr) | Run 10 (SpecConstr, aligned) | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | **0.055** | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.054 | 0.047 | 0.048 | 0.054 | 0.049 | 0.051 | 0.049 | 0.049 | 0.049 | 0.049 | 0.048 | 0.048 | 0.048 | 0.049 | 0.048 | 0.053 | 0.054 |
| `mut-flat-gm` | **0.083** | 0.084 | 0.084 | 0.083 | 0.084 | 0.084 | 0.087 | 0.076 | 0.081 | 0.088 | 0.081 | 0.083 | 0.082 | 0.082 | 0.081 | 0.082 | 0.081 | 0.081 | 0.083 | 0.081 | 0.080 | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.090** | 0.094 | 0.089 | 0.091 | 0.093 | 0.092 | 0.093 | 0.080 | 0.086 | 0.094 | 0.087 | 0.088 | 0.087 | 0.087 | 0.087 | 0.088 | 0.087 | 0.086 | 0.085 | 0.088 | 0.088 | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.100** | 0.109 | 0.100 | 0.100 | 0.101 | 0.100 | 0.100 | 0.087 | 0.090 | 0.100 | 0.090 | 0.095 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.098** | 0.106 | 0.096 | 0.098 | 0.099 | 0.099 | 0.096 | 0.082 | 0.091 | 0.096 | 0.091 | 0.090 | 0.091 | 0.090 | 0.090 | 0.091 | 0.089 | 0.090 | 0.090 | 0.089 | 0.090 | 0.090 | 0.119 |
| `bq-expand` | **0.115** | 0.117 | 0.115 | 0.117 | 0.117 | 0.115 | 0.114 | 0.101 | 0.102 | 0.114 | 0.102 | 0.107 | 0.103 | 0.102 | 0.102 | 0.102 | 0.103 | 0.103 | 0.102 | 0.102 | 0.105 | 0.102 | 0.127 |
| `build` | **0.103** | 0.101 | 0.103 | 0.102 | 0.105 | 0.106 | 0.109 | 0.097 | 0.102 | 0.110 | 0.103 | 0.097 | 0.099 | 0.099 | 0.098 | 0.098 | 0.096 | 0.100 | 0.110 | 0.096 | 0.114 | 0.095 | -- |
| `offtab` | **0.134** | 0.136 | 0.134 | 0.143 | 0.135 | 0.141 | 0.136 | 0.124 | 0.126 | 0.138 | 0.121 | 0.121 | 0.125 | 0.121 | 0.125 | 0.131 | 0.125 | 0.123 | 0.123 | 0.124 | 0.115 | 0.146 | -- |
| `mut-flat` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.108 | 0.097 |

**Every column but the last is a published geomean over the same 24 shapes,
and most of the SpecConstr ones share a denominator too** --- `list` moved 0.47%
between the two Run 13 columns, 0.24% between the two Run 12 ones, 0.7% between
the two Run 11 ones, and 0.6% and 0.4% inside Run 10 and against Run 9 ---
so those may be subtracted and not merely ordered, which is what the -O1 column
cannot do at an 8% baseline shift. **The three nursery pairs are the exception,
and no such pair's columns may be subtracted from each other.** `list` moved
**9.20%** between Run 14's two halves, **5.13%** between Run 15's and **16.51%**
between Run 16's, where no other within-run pair here moves it past 0.7%. **Run
16's is the largest of the three and was registered to be the smallest**,
on the reasoning that its two halves both sit at enlarged areas where
the earlier two each crossed the default --- a prediction refuted by its own
run, and the refutation is the finding: what moves the baseline is
not the distance from the default but the in-process deflation, which at roster
scale is worse at 64 MB than at 32 MB by more than the whole default-to-32 MB
step was worth. So the exception widens rather than narrowing, and it now covers
every pair that varies the allocation area at all. Every cell of a nursery
pair's second column is scaled by a denominator the pairing moved: read such
a column for the pairing's direction and take no strategy quality off it,
and read the arm-by-arm comparison at the head of this file instead, which
divides absolutes rather than ratios. **Across the Run 11/Run 12 boundary
the sharing holds more loosely**, the two runs sharing no binary, Run 11's
having been deleted --- but its **JSONs were kept**, so the baseline comparison
is measured rather than guessed: `list` reads **0.9953** of its Run 11 max-skip
self over the 24 shapes, scattering 0.9611 to 1.0431 per shape. Half a percent
on the geomean is small enough to subtract across; five percent on a cell
is not, so read a per-shape difference of a point or two there as unresolved
rather than as a movement. Read the two Run 12 columns against each other
for the **flag's term**: `offtab`'s 0.125 against 0.131 is the same arm
in the same run, one compiler flag apart. Read the two Run 11 columns
for the **padding term** --- `build`'s 0.096 against 0.100, one shim apart ---
and the two Run 10 columns for the **layout term**, `build`'s 0.110 against
0.096, and the -O1 column for orderings only.

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

**Two tables in this file are NOT installed and are edited by hand:
the yardstick above and the cross-class summary below.** Every other table a run
publishes comes from `install-tables.sh` and is replaced whole. These two gain
a column or a row per run instead, which is why they outlive the artifacts ---
and it is why a run edits them with the whole line named, never with a prefix
anchor. On Run 17 an insertion anchored on ``| `arm` | `` matched an earlier
table and put two cells into the element-type probe's header and a loop-offsets
row; `--check-doc`'s width pass caught it in the same call, which is the only
reason it cost minutes. Name the whole row, assert it occurs exactly once,
and read the width check's verdict afterwards.

And because a geomean cannot say *where* it moved, the **fingerprint** below
is kept so a future disagreement can be localised rather than only noticed.
Its membership is a rule, not a habit, re-aimed 2026-08-22 and settled
2026-08-24: `mut-odo-vecdims` and every arm that is the best outside the vecdims
family on at least one shape of the main set or a stride class --- on Run 16
`mut-flat-gm`, `bq-scan-rem-gm-mulback`, `build`, `mut-odo`, `bq-mut-runs`
and `bq-mut-runs-gm-mulback`, in that order of shapes led, and `offtab-scan-rem`
on Run 18 --- and **it only ever grows**: an arm that has earned a column keeps
it, and no run drops one; the second table carries the same columns over every
stride-class shape, with its class named. **One representative per family**,
besides: where a qualifying arm is a close variant of a member and measures
closely, the leading one keeps the column, so no strategy costs two.
The judgement is the author's, which is why `--fingerprint` names the best
member on the shape a newcomer leads. **Neither way of dropping an arm
survives.** Dropping one that leads nothing this run churns on a thousandth ---
`offtab-scan-rem` holds `reshape1-rank10` at 0.090 against 0.091 --- and gaps
the record wherever the column went. Judging it off the fingerprint this file
carries is worse: that table holds the members alone, so a leaver would
be judged against the members alone where a joiner is judged against every timed
arm --- on `reshape1-rank10` the members' own minimum
was `bq-scan-rem-gm-mulback` at 0.091, while the arm that won the shape read
0.090 and had no column to be seen in. The header therefore grows, and the run
writer narrows it by hand if it gets unwieldy. An arm nothing measures cannot
be the subject of a future disagreement to localise, and what is given up when
one goes is the per-shape half alone, its geomean staying in the yardstick table
above. `list`'s own net per call rides along, guarding the baseline at every
shape where the anchors guard three, and converting any ratio beside it back
to absolute time. Allocation stays medians-only on purpose: deterministic per
call, so a run that raises an allocation question re-derives it within itself.
`./read-run.py RUN.json --fingerprint --classes CLASS.json...` emits both tables
--- paste them whole, transcribing nothing by hand, since hand-carrying
this table once left two of Run 6's cells standing under Run 7's name,
and the first emitted paste is what caught them. The column heads shorten
the arm names as the stretch table's do: vecdims is `mut-odo-vecdims`, flat-gm
`mut-flat-gm`, scan-rem-gm `bq-scan-rem-gm-mulback`, mut-runs `bq-mut-runs`,
runs-gm `bq-mut-runs-gm-mulback` and offtab-rem `offtab-scan-rem`.
And the [stretch table][pershape] is the same kind of record for `bq-expand-b`,
on the shapes chosen to stress orderings --- compare it the same way. It lost
a `lemire-out` column to this same rule on the same day, and says so.

| shape | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | mut-runs | runs-gm | offtab-rem |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 6.08 us | 0.085 | 0.143 | 0.155 | 0.162 | 0.158 | 0.135 | 0.145 | 0.168 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.35 us | 0.099 | 0.184 | 0.147 | 0.187 | 0.193 | 0.178 | 0.181 | 0.161 |
| `stretch-rank12` | 2 | 4096 | 110 us | 0.103 | 0.184 | 0.132 | 0.263 | 0.268 | 0.198 | 0.178 | 0.171 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 115 us | 0.070 | 0.134 | 0.097 | 0.160 | 0.166 | 0.140 | 0.124 | 0.122 |
| `conv1d-24` | 3 | 5184 | 103 us | 0.056 | 0.070 | 0.098 | 0.124 | 0.126 | 0.085 | 0.075 | 0.132 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 369 us | 0.048 | 0.093 | 0.094 | 0.100 | 0.104 | 0.109 | 0.099 | 0.120 |
| `gather48-src-50` | 3 | 22500 | 436 us | 0.053 | 0.066 | 0.098 | 0.117 | 0.122 | 0.083 | 0.074 | 0.129 |
| `stretch-rank10` | 3 | 59049 | 1.29 ms | 0.067 | 0.108 | 0.102 | 0.154 | 0.172 | 0.125 | 0.111 | 0.135 |
| `stretch-coprime-r7` | 13 | 60060 | 1.02 ms | 0.036 | 0.083 | 0.093 | 0.059 | 0.058 | 0.102 | 0.092 | 0.124 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.1 ms | 0.059 | 0.089 | 0.098 | 0.143 | 0.134 | 0.105 | 0.094 | 0.126 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.52 ms | 0.058 | 0.087 | 0.098 | 0.131 | 0.152 | 0.107 | 0.095 | 0.126 |
| `stretch-primes` | 89 | 250357 | 4 ms | 0.030 | 0.075 | 0.092 | 0.031 | 0.031 | 0.090 | 0.086 | 0.131 |
| `stretch-inner1` | 1 | 500000 | 12.9 ms | 0.090 | 0.032 | 0.073 | 0.215 | 0.228 | 0.070 | 0.032 | 0.073 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.2 ms | 0.045 | 0.074 | 0.093 | 0.093 | 0.100 | 0.094 | 0.085 | 0.125 |
| `vgg-14-c512-k3` | 3 | 903168 | 19 ms | 0.058 | 0.086 | 0.097 | 0.142 | 0.151 | 0.104 | 0.095 | 0.128 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.4 ms | 0.037 | 0.071 | 0.090 | 0.055 | 0.053 | 0.091 | 0.082 | 0.130 |
| `stretch-inner256` | 256 | 1750784 | 32.9 ms | 0.033 | 0.070 | 0.087 | 0.034 | 0.034 | 0.111 | 0.076 | 0.118 |
| `stretch-pow2stride` | 64 | 1769472 | 28.3 ms | 0.126 | 0.122 | 0.147 | 0.126 | 0.127 | 0.115 | 0.134 | 0.223 |
| `stretch-r5-8x432` | 8 | 1769472 | 33.9 ms | 0.033 | 0.061 | 0.082 | 0.052 | 0.059 | 0.078 | 0.068 | 0.115 |
| `stretch-square-1341` | 1341 | 1798281 | 30.2 ms | 0.088 | 0.131 | 0.154 | 0.088 | 0.089 | 0.107 | 0.137 | 0.203 |
| `stretch-bigstride` | 3 | 1800000 | 49.6 ms | 0.035 | 0.044 | 0.066 | 0.078 | 0.086 | 0.057 | 0.051 | 0.091 |
| `stretch-tab7MB` | 2 | 1800000 | 38.1 ms | 0.063 | 0.063 | 0.100 | 0.137 | 0.150 | 0.078 | 0.068 | 0.142 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39.5 ms | 0.023 | 0.052 | 0.063 | 0.024 | 0.024 | 0.067 | 0.058 | 0.095 |
| `stretch-wide-2xM` | 2 | 1800000 | 38.3 ms | 0.061 | 0.060 | 0.098 | 0.139 | 0.152 | 0.076 | 0.069 | 0.136 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | mut-runs | runs-gm | offtab-rem |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 871 us | 0.033 | 0.067 | 0.090 | 0.061 | 0.061 | 0.087 | 0.079 | 0.118 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 27.1 ms | 0.022 | 0.071 | 0.089 | 0.023 | 0.023 | 0.095 | 0.089 | 0.123 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 37.6 ms | 0.062 | 0.062 | 0.098 | 0.131 | 0.152 | 0.077 | 0.070 | 0.136 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.42 ms | 0.059 | 0.090 | 0.100 | 0.138 | 0.157 | 0.107 | 0.100 | 0.128 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.91 ms | 0.022 | 0.069 | 0.087 | 0.023 | 0.023 | 0.091 | 0.085 | 0.122 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 45.6 ms | 0.037 | 0.047 | 0.071 | 0.079 | 0.090 | 0.061 | 0.056 | 0.094 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.88 ms | 0.110 | 0.135 | 0.091 | 0.311 | 0.337 | 0.162 | 0.113 | 0.092 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.7 ms | 0.092 | 0.032 | 0.073 | 0.230 | 0.245 | 0.072 | 0.032 | 0.073 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 13 ms | 0.089 | 0.032 | 0.074 | 0.228 | 0.217 | 0.069 | 0.032 | 0.073 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 115 us | 0.070 | 0.126 | 0.096 | 0.168 | 0.180 | 0.146 | 0.128 | 0.121 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 438 us | 0.052 | 0.065 | 0.097 | 0.118 | 0.121 | 0.082 | 0.074 | 0.126 |
| `rev-primes` | `rev` | 89 | 250357 | 4.07 ms | 0.029 | 0.071 | 0.090 | 0.031 | 0.031 | 0.089 | 0.084 | 0.129 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 441 us | 0.053 | 0.067 | 0.099 | 0.117 | 0.122 | 0.082 | 0.076 | 0.127 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.47 ms | 0.059 | 0.089 | 0.097 | 0.140 | 0.136 | 0.107 | 0.096 | 0.126 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.06 ms | 0.030 | 0.079 | 0.101 | 0.032 | 0.032 | 0.088 | 0.092 | 0.131 |
| `scaled-r5` | `scaled` | 13 | 15015 | 247 us | 0.033 | 0.073 | 0.094 | 0.047 | 0.048 | 0.093 | 0.082 | 0.128 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 951 us | 0.029 | 0.073 | 0.092 | 0.034 | 0.033 | 0.093 | 0.081 | 0.127 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.79 ms | 0.033 | 0.073 | 0.090 | 0.035 | 0.035 | 0.091 | 0.081 | 0.134 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.03 ms | 0.037 | 0.082 | 0.095 | 0.060 | 0.063 | 0.101 | 0.091 | 0.126 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.54 ms | 0.059 | 0.091 | 0.098 | 0.140 | 0.135 | 0.102 | 0.092 | 0.129 |
| `slice-primes` | `slice` | 89 | 250357 | 4.02 ms | 0.030 | 0.081 | 0.102 | 0.032 | 0.032 | 0.091 | 0.092 | 0.132 |
| `window-28x28-k5` | `window` | 5 | 14400 | 265 us | 0.044 | 0.078 | 0.094 | 0.089 | 0.088 | 0.094 | 0.085 | 0.120 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 876 us | 0.097 | 0.046 | 0.074 | 0.250 | 0.263 | 0.086 | 0.045 | 0.074 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.4 ms | 0.055 | 0.086 | 0.094 | 0.131 | 0.145 | 0.103 | 0.095 | 0.121 |

**Three rows to read first, and the set is derived rather than remembered ---
it was two until this run**: `stretch-square-1341`, `stretch-pow2stride` and now
`cnn-slice-c32` are the shapes where **both** arms tying at the head of the pure
tier *lose* to `bq-expand`, so treat a disagreement on any of them as the shape.
They fail differently, which is why each is named. On `stretch-square-1341`
the mutable fills win it back outright (`mut-odo-vecdims` 0.088 against
`bq-expand`'s 0.134) while the pure arms trail; on `stretch-pow2stride` the two
families converge instead, three of the eight fingerprint arms landing inside
two thousandths of each other and the whole row spanning 0.115 to 0.223,
or 0.115 to 0.147 with `offtab-scan-rem` set aside ([the per-shape
section][pershape]); `cnn-slice-c32` is the smallest shape in the set and is new
to this list, which is itself the reason to watch it. Taking the tier's leaders
one at a time gives seven shapes and three, which is why the sentence says both.
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction.


## The claims the next run should test

**Run 19's verdicts first**, since a run reports breaks rather than re-deriving
the table. **All thirteen registered orderings held, and they held on both
compilers** --- no BROKE on the 9.12 basis and none on the GHC HEAD control,
a second clean sweep running, and the second half of it is registration 2's
whole subject: every ordering the README rests on survives a compiler two
releases ahead of the one they were measured on. **And that sweep is what
the four retiring claims retire on.** The settlement of 2026-08-24 held
the manifest at thirteen through this run so that claims 3, 4, 5 and 9 got one
last cross-compiler reading before going, and they got it: all four held on both
halves. The manifest took the retirement at this write-up, thirteen orderings
becoming eight, and the eight hold on both halves too. What follows keeps
the surviving claims' numbers --- 1, 2, 6, 7 and 8 --- and does not renumber,
so that a verdict recorded against a number in an earlier run's file still means
what it said.

**Nothing crossed, on either half, so the four retirements are clean ones.**
Claim 3 read 0.8992 on the basis and 0.9072 on HEAD; claim 4's tie held at sign
p 0.84 and 0.54 and its ordering at 0.8653 and 0.9129; claim 5's two links
at 0.3134 and 0.8702 on the basis, 0.3400 and 0.8614 on HEAD; and claim 9's
stable pair came back `stretch-inner1` and `stretch-wide-2xM` on both, its `zf`
link at 1.0188 and 1.0211. **Each retires a live and holding ordering rather
than a broken one**, which is what the settlement's test asks for ---
an ordering goes when it forecloses nothing anyone would propose again, not when
it fails --- and each is recorded here so that the last reading survives
the manifest entry. What the four leave rostered is every arm they named:
`--pair` recovers any of them in one call.

**Claim 1 held on all five links, and it is five links from this run on.**
The settlement gave it the two the retiring claim 4 was carrying, so it is now
the whole ladder the `needs` column draws: what a mutating `Vector` method buys
(0.6650), what one more mutable write pattern buys (0.9299), what a mutable
`Int` scratch buys (0.9011 against the best arm needing nothing), and,
at the foot, **the two fastest pure arms tied at 0.9943 on 13 of 24 and sign p
0.84** --- so if the mutating method is refused upstream,
`bq-scan-rem-gm-mulback` and `bq-odo-gm-mulback` are indistinguishable
and either is what ships. The two new links read 0.9060 and 0.9902 on Run 18's
basis and 0.9011 and 0.9943 here, which is the agreement that let them
be registered at all. The ceiling's ordering has now survived eight runs, two
changes of basis, a repetition, a layout pair and three compilers.

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6650, 21 of 24, sign p
0.00028; `mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9299, 20 of 24, sign p
0.0015; `bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.8960, 20 of 24, sign p
0.0015; `bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9011, 19 of 24,
sign p 0.0066; `bq-scan-rem-gm-mulback` / `bq-odo-gm-mulback` 0.9943, 13 of 24,
sign p 0.84. 5 of 5 registered orderings held.

**Claim 2 kept its number and changed its question**, from where `bq-expand` sat
among its neighbours to where the arms needing something other than the fix sit
behind it. Both links held. `offtab`, which needs only a mutable `Int` scratch,
is **1.3458** behind the best arm needing nothing at all, on 6 of 24 and sign p
0.023, where Run 18's halves read 1.36 and 1.44. `bq-expand`, the last candidate
and what `Data/Array/Internal.hs` still carries, is **2.0741** behind the arm
that ships, on 1 of 24 and sign p 3e-06 --- the widest and most significant
ordering in the manifest, and the one that prices the branch's own code against
its replacement. That second link is kept only while the branch carries
`bq-expand`, and retires with the three `TODO: retarget` markers, which are one
decision with it.

**Readings:** `offtab` / `bq-scan-rem-gm-mulback` 1.3458, 6 of 24, sign p 0.023;
`bq-expand` / `mut-odo-vecdims` 2.0741, 1 of 24, sign p 3e-06. 2 of 2 registered
orderings held.

**Claims 3, 4 and 5 retired at this write-up**, on the readings in the sweep
paragraph above and for the reasons the settlement paragraph at the foot
of this section gives. In one line each, so the last thing they said is not only
in a manifest diff: claim 3 read `bq-expand-gm-mulback` / `bq-expand` at 0.8992
on 20 of 24, a mul-back output worth about a tenth on a build nothing ships;
claim 4's tie held at 0.9623 on 11 of 24 and p 0.84 and its ordering
over `bq-expand` at 0.8653 on 17 of 24, the third and last run of a reading Run
17 promoted from a tie; claim 5's two links read 0.3134 at 21 of 24
and `bq-mut-runs` / `bq-expand` at **0.8702 on 24 of 24, sign p 1.2e-07**,
the only unanimous ordering the manifest had. Every arm the three named stays
rostered and timed, so any of these is one `--pair` call away whenever
it is wanted again.

**Claim 6 held, and this run is the one that could test its alarm properly.**
`gen-quotrem` / `list` reads **1.0971** at 9 of 24 and sign p 0.31, a tie
by the sign test as registered. The claim's alarm is that a break here means
something moved in `list` or in GHC rather than in a strategy, and half
of that was under test all evening: the control half is a compiler two releases
on. It held there too, at the same 9 of 24 and the same p, with `gen-quotrem`
moving 1.2% between the halves at a count ratio of 1.0000 --- so GHC HEAD
changes neither what this arm computes nor what `list` costs relative to it.

**Readings:** `gen-quotrem` / `list` 1.0971, 9 of 24, sign p 0.31. 1 of 1
registered ordering held.

**Claim 7 held on the levels and is the one claim this pair moved.** Every level
is Run 15's, Run 16's, Run 17's and Run 18's to the digit --- the mutable fills
and `gen-quotrem` at 1.00x, `bq-mut` and the scan family 1.33x,
`bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x, `list` 23.50x ---
and the class blocks read the tiers unbroken in all eight populations.
**But the cross-half agreement fell**: **1016 of the 1080** cells that allocate
in earnest agree to 1e-4, where the 9.14 pair had 1072, and the worst
disagreement is 1.13e-02 on `cnn-slice-c32/bq-expand-qr-prim`. Allocation
is deterministic per call, so a cell that moves is a code change and never
a slot: 9.14 allocated exactly what 9.12 allocated, and **HEAD does not**.
The levels surviving while sixty-odd cells move is the shape to read --- HEAD
reallocates within a tier rather than changing what any strategy fundamentally
costs --- and it is the first thing this claim has ever caught, which is why
it is checked first when anything else moves.

**Claim 8's structural half stands.** Every pure arm in the fast tier still runs
its output through the single in-order `vGenerate` over an `m`-length table,
and the arms that fall behind lose on their table build: `bq-expand-zf` at 0.117
and `offtab-scan-rem` at 0.130 lie between the leading tier and `bq-gen`'s
0.370, as the claim says to expect. It is read off the table by eye, being
the one claim with no named invocation --- **and this run says what
that costs**: the counted-work column would have told the same story
from instruction counts, which is a route the claim could be given whenever
someone wants it checked rather than seen.

**Claim 9 retired at this write-up**, having held on both halves first: the two
best cells are `stretch-inner1` and `stretch-wide-2xM` again, on 9.12
and on HEAD alike, so the pair Run 17 disturbed has now returned twice running
and the follow-up that kept it live is spent. Its second ordering,
`bq-expand-zf` behind `bq-expand`, read 1.0188 and 1.0211 on the two halves,
inside the 1.0028-to-1.0325 band that series has held since Run 8. Both series
were closed at Run 13 by this section's own words, and a closed series in a live
manifest is maintenance without a question, which is what retired it.

Restated as the predicates the next run checks, and carrying no reading
of its own: the figures each was last measured at are in the `Readings:`
paragraphs above, so an entry here changes when a claim is re-aimed and not when
a run moves a margin. **All of them are `-fspec-constr` claims, the regime they
are read in** --- the shipped file does not set the flag, measured irrelevant
to the shipped family --- so they are the set that decides, and a run at -O1
would test Run 7's instead, the two differing in more than their numbers. **They
are read in the caller's allocation regime now**, every figure here being taken
at the `-A32m` Run 16 promoted to the basis and every horde-ad test
and benchmark bakes since 2026-08-21; the gap Runs 14, 15 and 16 priced against
a prevailing `-A1G` is closed, and no claim below needs qualifying by it.
**And all of them are read against a measured drift band rather than a layout
span**, which is what the last three runs bought. A roster *order* change alone
moved arms 0.966 to 1.142 between Run 9 and Run 10, and that is what a margin
used to have to clear; with the layout pinned, a repetition moves an arm
by at most 3.3% and most of them by under 1.5%, so a margin above a few percent
is now evidence of a strategy. **Run 13 is the first pair here to hold every
tracked loop at one offset in both halves**, which is what lets its arm-by-arm
comparison be read as the package costing nothing rather than as two terms
cancelling. A claim resting on an arm whose own loop the shim skipped ---
`list`'s, which is library code --- is still decidable nowhere until that loop
is read. **And the pinning claim is measured only in its weak form**: adding
`mut-flat-gm-nosum` left every tracked loop at the same address, but a `Force`
arm reuses a rostered function and emits no code for emission order to move.
The strong form wants an arm that emits its own, and until one is added
the claim covers additions that cost nothing to place.

**The list needed no re-aiming this time either**, the roster it was rewritten
onto before Run 8 being the roster Run 18 ran: every claim below names an arm
this run timed. Seven full runs on that roster is the evidence that keeping
the *question* and changing the *arm* was the right repair --- the unconditional
counterparts were written so that dropping a precondition would not drop
a question with it, and none of them dropped one. The claims that read against
`bq-expand` read against it because the branch carried it; since 2026-08-24
the branch carries the stage-one fix instead, and their retirement is settled
below, applied at Run 19's write-up.

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` <
   `bq-scan-rem-gm-mulback` ~ `bq-odo-gm-mulback`, the whole ordering read
   on unconditional arms --- **the ladder the `needs` column draws**, each link
   pricing one thing the implementation is allowed to ask for. The last link
   is a tie and is registered as one: the two fastest arms needing nothing
   at all are indistinguishable, so either is what ships if the mutating
   `Vector` method is refused. The middle link is the one the README has seen
   a layout term move --- 0.9708 at 15 of 24 on Run 10's unaligned half against
   0.9293 at 22 on its aligned one --- and on a placed layout it has now read
   the aligned figure five runs running. The ordering has survived eight runs,
   two changes of basis, a repetition and three compilers.
2. `offtab` sits behind `bq-scan-rem-gm-mulback` and `bq-expand` behind
   `mut-odo-vecdims`: **the arms needing something other than the fix sit behind
   it**, which is what this claim asks since the settlement of 2026-08-24
   re-aimed it. The first prices a mutable `Int` scratch against needing
   nothing, the second prices the branch's own code against its replacement
   and is the widest ordering in the manifest. The second link is kept only
   while `Data/Array/Internal.hs` carries `bq-expand`, and retires
   with the three `TODO: retarget` markers, which are one decision with it.
3, 4, 5. **Retired at Run 19's write-up**, on a last reading in which all three
held on both compilers, and for the reasons in the settlement paragraph
at the foot of this section. Their numbers are left standing here rather
than reused: a verdict recorded against *claim 4* in an earlier run's file still
means what it said. What they were, in a clause each, so that nothing
is recoverable only from a manifest diff --- claim 3, that a mul-back output
pays on the `bq-expand` build; claim 4, that the scan build ties its own build
control while beating `bq-expand`, a tie Run 17 promoted to an ordering
and three runs then read as one; claim 5, that `bq-expand` beats `bq-gen`, whose
refutation of the generate-per-element build stands on Runs 7 and 8. **What none
of the three could still foreclose is the point**: every one asks where
`bq-expand` sits among arms nothing ships, on a branch whose fix
is `mut-odo-vecdims`. The arms all stay rostered and timed, so any
of these orderings is one `--pair` call away.
6. `gen-quotrem` ties `list` --- the first attempt's arithmetic stops being
   dearer than the list's allocation once the flag takes its own allocation
   to 1.00x against the list's 23.5x, which is the mixed picture this suite
   exists to have refuted, arriving by a route nobody proposed. The `cm-gather`
   < `list` half is untimed and stands as Run 8's. A break here would mean
   something changed in `list` or in GHC, not in a strategy --- check the anchor
   before anything else, as Run 8 had to and the five runs since did not.
7. Allocation, median multiples of the result on this basis: the mutable fills
   1.00x, `gen-quotrem` also 1.00x, `bq-mut` and the scan family 1.33x,
   `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x, `list` 23.5x.
   Every level has reproduced since Run 15, which is what makes this the claim
   to check first when anything else moves: allocation is deterministic per
   call, so a level that *does* move is a code change and never a slot. **Read
   the levels and the cells as two questions**, which Run 19 is the run
   that separated: its levels all returned while the cross-half cell agreement
   fell to 1016 of 1080, where the 9.14 pair had 1072 --- so a compiler can
   reallocate within a tier without moving any tier, and only the cell count
   sees it.
8. Every pure arm in the fast tier runs its output through the single in-order
   `vGenerate` over an `m`-length table, and a `bq-*` arm that falls behind
   loses on its table build and not on its output. Read the structure and
   not a threshold: the gap the claim used to be stated across is populated,
   `bq-expand-zf` and `offtab-scan-rem` lying between the leading tier
   and `bq-gen`.
9. **Retired at Run 19's write-up with 3, 4 and 5**, and for a reason of its own
   worth keeping: its per-shape half was answered rather than abandoned.
   `bq-expand-b`'s two best cells were `stretch-inner1` and `stretch-wide-2xM`
   in every run from Run 8 to Run 16 --- the rank-2 views with one huge outer
   dimension where seeding from `enumFromStepN` replaces the whole `concatMap`
   build --- until **Run 17 read `stretch-inner1` and `stretch-square-1341`
   instead**, which registered the follow-up. Runs 18 and 19 both read
   the original pair back, on four compilers between them, so the excursion
   was one run's and the mechanism is cleared of picking the wrong shapes.
   The geomeans were never the stable part, and the series is why: across Runs 8
   to 13 `bq-expand-b` / `bq-expand` read 0.996, 0.9678, 0.9943, 0.9819, 0.9923
   and 0.9909, its sign test crossing into significance only on the last
   of them, while `bq-expand-zf` / `bq-expand` went 3.6% behind, then level
   at 1.0028, then 1.0325, 1.0197, 1.0256 and 1.0265. Both series were closed
   at Run 13 and not extended per run, and a closed series in a live manifest
   is maintenance without a question --- which, with the follow-up spent,
   is the whole case for retiring it.

Each ordering is one line of `--claims`, whose manifest now carries
the registered expectation --- the direction of the geomean, a tie by sign test,
or claim 9's two best shapes --- and prints HELD or BROKE beside the paired
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
--- fix it there, before the sentence it was written for, or the next run
invents its own wrong version. **Two riders, both bought on Run 19.** A new MODE
joins the guards its siblings already have, and is checked against them rather
than written beside them: `--counts` shipped able to be given without
the `--compare` it reads, silently printing the default table and exiting 0 ---
the unread-flag family exactly, added next to four sibling readings
of `--compare` that were every one of them already guarded, and joining none.
**And an instrument may be BACKED OUT, which is not a failure of the write-up
but a result of it.** Measure what it flags before shipping it: the obvious
mechanical repair for stale paragraphs was built and returned 100 for the four
that mattered, so it went, and the refutation with its numbers is
under the tasks heading --- worth more than the mode, since it stops the next
session building the same thing. A report that never empties is one nobody
reads, which this file already knows about hints.

**And for each stride class, the same three properties, now carrying Run 19's
verdicts**, the details beside each class's table:

1. **The regime 3 fix's `worst` stays under 1.** Held in every one of the nine
   populations, in every regime, roster and layout the README has run ---
   so the fix was never slower than the `list` it replaced, on any shape of any
   class the library can produce. This is the property the classes exist
   to test, no geomean can state it, and a break would be the one result here
   to bear on `Data/Array/Internal.hs` directly. Re-aimed 2026-08-22
   with the decision to ship `mut-odo-vecdims` instead, and read for that arm
   since: **on Run 19 its worst is 0.126 on the main set and 0.110 in a class
   (`reshape1`), both read on the basis half, with the control half at 0.121
   and 0.109** --- so the property holds for the arm decided, on both compilers,
   and neither end comes within a factor of eight of 1. **Both halves are quoted
   because one is not enough**: Run 18's entry here read 0.125 from its basis
   and 0.107 from its *control*'s `reshape1` without saying so, which
   is a floor-level figure taken from whichever half happened to be lower.
2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-expand` behind it. The first clause, read as the vecdims family's rather
   than one arm's --- the ruling Run 9 left, and no run has yet separated them
   --- holds in eight of the nine populations and breaks in `reshape1` alone,
   where two arms outside the family own the top outright --- `mut-flat-gm`,
   a flat mutable fill, and `bq-mut-runs-gm-mulback`, which needs only an `Int`
   scratch --- tied at 0.033 against `mut-odo-vecdims`'s 0.094. **Which member
   leads has moved again**: `mut-odo-vecdims-add-in` heads five of the nine
   by the sort --- the main set, `rev`, `bcastmid`, `slice` and `window` ---
   with `mut-odo-vecdims` itself taking `revsome` and `scaled`
   and `add-both-down` taking `bcast`, where Run 18 had `add-in` heading six
   and Run 16 two. **Read that by margin and not by sort, as this list has had
   to since Run 16**: every one of the eight CLASS margins is inside
   its population's floor, from 0.9704 on `window` to 1.0013 on `scaled`,
   and **`revsome` inverts outright**: its column puts `mut-odo-vecdims` first
   while the paired reading puts `add-in` 0.96% ahead, the two printing 0.047
   and 0.048. `scaled` is the other class whose column puts `mut-odo-vecdims`
   first, and there the paired reading agrees with it, at 1.0013 --- a tenth
   of a percent. The other six classes sort `add-in` first and their paired
   readings agree, so it is `revsome` alone that inverts. So no run has
   separated the family in a class yet, and in one of the eight the sort
   is naming rounding. **The main set is the one population that clears a floor,
   and it splits by compiler for the second run running**: `add-in` leads
   at **0.9755 on 19 of 24 shapes, sign p 0.0066** on the 9.12 half --- 2.45%,
   outside that half's 2.32% and five times its restricted six --- and reads
   **0.9991 at 14 of 24, p 0.54** on the HEAD half, a coin flip. Only the main
   set could show this at all, a three-shape class bottoming out at p 0.25,
   so the eight classes say nothing about significance either way. [Its own
   entry][open] carries the whole of it, including what Run 19 took away:
   the `-g3` twin does not carry to HEAD, so the swapped-offset reading
   that made this placement is gone and the mechanism is unidentified. What
   belongs here is that the arm leading most populations
   is not `mut-odo-vecdims`, and that its lead is not a property of the arm.
   The third clause reads the last candidate `bq-expand` behind
   `mut-odo-vecdims` and holds in all nine, from 0.3272 on `scaled` to 0.7978
   on `reshape1`, the main set at 0.4821. The summary's outside-family slot ---
   what the dropped redirect would have taken --- is `mut-flat-gm` in `rev`,
   `revsome` and `window`, `build` in `bcast`, `bcastmid` and `slice`,
   `bq-mut-runs-gm-mulback` in `reshape1` and `mut-odo` in `scaled`, only
   `reshape1`'s ahead of `mut-odo-vecdims`.
3. **The allocation tiers survive, and every level is Run 15's, Run 16's and Run
   17's to the digit**: the mutable fills at the result vector, `bq-expand`
   between 1.14x and 5.43x it, `list` an order of magnitude above. Where a level
   moves it is the class's own `m` showing through, exactly as this property
   warned --- `bq-expand` at 1.14x on `scaled` (`m` of 1 and 2,000) and 5.43x
   on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine
   and `list` running 19.43x to 32.34x across them. On a pair whose two halves
   are different compilers this is the property that says the difference
   is codegen and not the program: allocation is deterministic per call, none
   of these levels moved, and the two halves agree on 1016 of 1080 allocating
   cells.

**SETTLED 2026-08-24 and APPLIED 2026-08-25, at Run 19's write-up rather
than at the settlement**, so that the retiring orderings got one last
cross-compiler reading and the retirement is recorded with it --- which is how
Run 17 retired claim 4's tie, in prose at its write-up with the manifest taking
it the same day. **They got it**: all thirteen held on both of Run 19's halves,
and the eight that remain hold on both too, so each of the four retires
on a reading rather than on a decision. `CLAIMS` in `read-run.py` now carries
claims 1, 2 and 6 alone. The test applied: an ordering stays only
if it forecloses something anyone would propose again *and* can still break.
What fails both is a figure, and figures live in the tables above. **Claims 3, 5
and 9 retire outright.** Claim 3 sets one output form against another on a build
nothing ships, where every leading pure arm is a `-gm-mulback` already; claim
5's `bq-expand` / `bq-gen` says of itself that the refutation stands on Runs 7
and 8, and claim 6 keeps that family guarded through `gen-quotrem`; claim 9's
two series are closed at Run 13 by this section's own words, and a closed series
in a live manifest is maintenance without a question. **Claim 4 retires
with them, its tie moving into claim 1** --- and what goes with it is the one
place the manifest reads a *builder* apart from its output, which `--pair`
recovers whenever it is wanted, both arms staying rostered. **Claim 1 becomes
the ladder the `needs` column already draws**, gaining `bq-scan-rem-gm-mulback`,
the best arm needing nothing at all, between `bq-mut-runs-gm-mulback`
and `bq-odo-gm-mulback`: the first ahead of it at **0.9060** and **0.9171**
on Run 18's two halves, 19 and 17 of 24, which is what a mutable `Int` scratch
buys; and the second **tied** with it at **0.9902** and **0.9936**, 13 and 12
of 24 at p 0.84 and 1, so the two fastest pure arms are indistinguishable
and either is what ships if the mutating method is refused. Its three existing
links stay, the middle one redundant with the two new ones and carrying seven
runs of history they do not. **Claim 2 keeps its number and changes
its question** to where the arms needing something other than the fix sit:
`offtab`, which needs only that `Int` scratch, behind `bq-scan-rem-gm-mulback`
at **1.36** and **1.44**; and `bq-expand` behind `mut-odo-vecdims` at **2.09**
and **2.13**, kept only while `Data/Array/Internal.hs` carried `bq-expand`,
which ended 2026-08-24, and retired with the three `TODO: retarget` markers,
which were one decision with it. Thirteen registered orderings become eight,
claims 7 and 8 staying unmanifested prose. **The rewriting the ask paired
with this was already done**: the eight *What the class says* paragraphs
were written to the re-aimed properties at Run 18's write-up, and only
the sentence asking for it survived.

`--pair` works within a class JSON exactly as within the main one, and is still
the way to compare two arms; its bootstrap interval, over three shapes, is worth
less there than its win count.

Two notes on the columns. The `needs` column splits the class-method tier
in two. A **new pure `Vector` method** delegates to a pure function the vector
package already ships for every carrier --- `unfoldrExactN`, `backpermute`,
the `concatMap`/`enumFromStepN` pipeline --- so it fights only *minimal*
in orthotope's pure-and-minimal API rule; the **new mutating `Vector` method**
the direct fills need is the [mutable
ceiling](../README.md#the-mutable-ceiling-taken)'s ask, which *pure* barred
outright until the amendment there turned the bar into a weight, and which
the decision of 2026-08-22 takes. `offtab` is the `Vector`-class-expressible
shape of these gathers --- output by plain `vGenerate` over a concrete offset
table --- so its own cell names only its mutable `Int` scratch. And the geomean
weights every benchmarked shape **equally**, so a figure here is a ranking
statistic, not a claim about total work saved: the small shapes count as much
as the largest.


## The stride classes, run by run

**Run 19 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) records every class
on BOTH halves**, one process each, in [the
sequence](../README.md#making-a-major-benchmark-run). Every table below
is the **basis half**'s, which on this run is the 9.12 one, the half that keeps
the lineage. What the second half buys is that a pair's variable can be read
on a class, which is what settled Run 14's `scaled` question and what no run
before it could have asked. **Read across the halves and the direction Run 18
found is not only there, it is stronger.** Of the 336 arm-comparisons the eight
classes carry, **206 put the 9.12 half faster and 130 slower**, and all eight
geomeans fall below 1, running **0.9830 to 0.9889** --- one to one and seven
tenths of a percent, in the same direction every time, where Run 18's eight ran
0.9866 to 0.9949 against 9.14. So on the classes as on the main set, GHC HEAD
costs this roster a little more than 9.14 did, and does it everywhere.
The extremes are `bcast`'s `bq-odo-gm-mulback-aa-distant` at 0.8883 at one end
and `window`'s `bq-gen` at 1.1176 at the other --- the arm the counted-work
column puts six percent of its movement on, and the dearest build in the roster,
which is the one arm HEAD is reliably better at, leading seven of the eight
classes' upper extremes --- `bcast`'s is `mut-odo-vecdims-add-both-down`
at 1.0381. **What this run cannot say from its own sequence is
that the direction is the compiler's**, the control half having run first
in every pair, so that *the 9.12 half* and *the second process of the two* name
the same nine processes. **And unlike Run 18 it took no order probe**, whose
`slice` reversal separated the two there; so the alias is unbroken this run,
and a Run 20 that wants the class direction attributed owes a reversed class
of its own. **Three of the eight cross-half lines are not read for a level
at all**: `list` runs **0.9973 to 1.0186** across the eight, and on `revsome`,
`bcastmid` and `window` it sits past the 0.7% that lets two columns
be differenced, by 1.86%, 1.60% and 1.43%. They are not the three Run 18
disqualified --- that was `reshape1`, `window` and `scaled` --- so which classes
fail the threshold is not a property of the class, and `window` alone failed
it twice. Their tables, controls and floors are each one process's and stand;
it is the comparison between halves that goes, and each block says so.
This section fixes the form, so that a class is written up the way the main set
is rather than however the session that ran it chose. The form is this section's
own prose and is not a run's to rewrite, exactly as the column definitions
under [Results](#results) outlive the table they explain; what a run replaces
is everything below the form. What a class *is*, and the two rulings that keep
it a population of its own, are [in the goal
chapter](../README.md#the-stride-classes-and-what-they-cover).

First, one table over all of them, so that an inversion is visible without
reading every class's table. Every figure in it is transcribed from a class's
own table below --- none is computed here, and none is an average across
classes, there being no such population to average over. Its header, fixed here
so a run fills rows and never reshapes columns:

    | class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |

That header line is written out twice in this file, once here as the spec
and once as the table's own, and the two are the same text --- so a session
pasting a run's rows must anchor at the line start and check that it landed
on the unindented one. Getting that wrong put Run 8's rows under this paragraph
and left Run 7's standing in the table, both checks passing, because the check
looked the table up the same wrong way the paste did.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table;
*best outside family* is the leading arm outside the vecdims family, what
the dropped stride-conditioned redirect would have taken, and *ceiling*
the leading arm of the family, each with its name, since which arm leads is half
of what the column says; *floor* is the largest deviation from 1 among
that process's eighteen A/A controls. A cell that breaks one of [the three
properties](#the-claims-the-next-run-should-test) is bolded, and the class's own
paragraph says what broke.

Then one block per class, in `classViews`' order --- `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled` --- each carrying the same
six things and nothing else:

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
   this process's own floor and its own three gates, neither inherited nor lent;
4. its provenance and its anchor: elapsed time and the two heap peaks
   from that process's stderr line, its population's size from the reader's
   first line ([why not both from one
   place](../README.md#making-a-major-benchmark-run)), and `list`'s absolute
   per-call time on one of its shapes, raw and net. The main set's three anchors
   guard a baseline that moves for every population at once; this one guards
   a baseline that could move for this mechanism alone, which is the case
   a table of ratios hides completely. A three-shape class adds one line here
   --- the bolded rows' per-shape net ratios, in the lead's shape order ---
   because its table under-determines its cells, where a two-shape table carried
   them already, `time` and `worst` jointly fixing both; every class
   is three-shape now, so the line always prints;
5. the cross-half reading, one line, which `--block --compare` against the other
   half's JSON now emits and `install-tables.sh` writes in with the other three
   --- how many of the population's arms move, which way, and the spread. Both
   halves have run every class since 2026-08-14 and this is where that is read:
   a pair's variable can act on a class and not on the main set, which is how
   Run 14 answered its `scaled` question. A run whose halves differ in nothing
   a class can see says so in a clause;
6. one paragraph of what the class says, and none where it says nothing:
   an ordering that inverted, a `worst` above 1, an allocation tier that moved,
   a mechanism showing through a single cell. A class that reproduces the main
   ordering gets one sentence saying so, that being a result and reading as one.

`./read-run.py RUN.json --block --compare OTHER.json` assembles items 2 through
5's mechanical parts, and `install-tables.sh` writes them in in one call ---
table, controls, the provenance and anchor skeleton, a three-shape population's
per-shape line, and the cross-half line; the lead and the paragraph stay
the author's, a skeleton writing no findings. **The cross-half line carries
its own disqualification**: where `list` moves more than 0.7% between the halves
the line says so and says it is not read for the pair's variable --- a reading
Run 18 needed, and which no other output showed.

The blocks carry no headings of their own. One per class would crowd
the contents and the replace list alike, where a bolded lead reads the same
and lets one link cover the section --- which is what `--check-doc`'s coverage
check counts.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.047 | 0.070 | `mut-flat-gm` 0.080 | `mut-odo-vecdims-add-in` 0.046 | 2.65% |
| `revsome` | 3 | 0.047 | 0.059 | `mut-flat-gm` 0.078 | `mut-odo-vecdims` 0.047 | 2.00% |
| `bcast` | 3 | 0.036 | 0.062 | `build` 0.057 | `mut-odo-vecdims-add-both-down` 0.035 | 4.79% |
| `bcastmid` | 3 | 0.037 | 0.059 | `build` 0.063 | `mut-odo-vecdims-add-in` 0.036 | 4.16% |
| `reshape1` | 3 | 0.094 | 0.110 | **`bq-mut-runs-gm-mulback`** 0.033 | **`bq-mut-runs-gm-mulback`** 0.033 | 8.11% |
| `slice` | 3 | 0.040 | 0.059 | `build` 0.065 | `mut-odo-vecdims-add-in` 0.040 | 2.43% |
| `window` | 3 | 0.062 | 0.097 | `mut-flat-gm` 0.070 | `mut-odo-vecdims-add-in` 0.060 | 7.57% |
| `scaled` | 3 | 0.032 | 0.033 | `mut-odo` 0.037 | `mut-odo-vecdims` 0.032 | 3.80% |

The floor-movement paragraph that stood here was cut on 2026-08-22, having read
Run 16's column against Run 15's while Run 17 installed this one over it ---
the defect `--check-doc` now holds every such movement to. What moves
these floors is [an open question](../README.md#what-is-open) and not a sentence
under a table.

The pure slot this table carried until 2026-08-22, and the paragraph that read
it, retired with the pure/impure distinction when the decision shipped
the mutable family's arm; the column now carries the best arm outside
the family, which the table above gives per class and which is ahead
of `mut-odo-vecdims` on `reshape1` alone.

**`rev` --- every stride negated, offset at the top: the view `rev` on every
axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3),
`rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357,
`sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *134* | *2.52x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.16* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| mut-odo-vecdims-add-in | 0.046 | 0.066 | 0.06 | 137 | 1.00x |
| *mut-odo-vecdims-aa* | *0.047* | *0.068* | *0.11* | *137* | *1.00x* |
| **mut-odo-vecdims** | **0.047** | 0.070 | 0.10 | 137 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.071* | *0.13* | *137* | *1.00x* |
| mut-odo-vecdims-add-both-down | 0.049 | 0.073 | 0.05 | 136 | 1.01x |
| mut-odo-vecdims-add-both | 0.050 | 0.076 | 0.07 | 136 | 1.01x |
| mut-odo-vecdims-add-out | 0.052 | 0.079 | 0.07 | 135 | 1.01x |
| mut-flat-gm | 0.080 | 0.126 | 0.19 | 134 | 1.34x |
| build | 0.085 | 0.168 | 1.77 | 125 | 1.00x |
| *build-aa-adjacent* | *0.086* | *0.166* | *1.75* | *125* | *1.00x* |
| *build-aa-distant* | *0.087* | *0.177* | *0.30* | *126* | *1.00x* |
| *mut-odo-aa-distant* | *0.087* | *0.181* | *0.89* | *125* | *1.00x* |
| mut-odo | 0.088 | 0.180 | 1.91 | 125 | 1.00x |
| bq-expand-gm-mulback | 0.090 | 0.167 | 0.09 | 130 | 2.52x |
| *mut-odo-aa-adjacent* | *0.091* | *0.172* | *2.44* | *125* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.093 | 0.128 | 0.13 | 132 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.095* | *0.097* | *0.07* | *128* | *1.34x* |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.097 | 0.09 | 128 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.097* | *0.06* | *128* | *1.34x* |
| bq-odo-gm-mulback | 0.095 | 0.116 | 0.11 | 131 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.095* | *0.116* | *0.10* | *131* | *1.41x* |
| *bq-odo-gm-mulback-aa-distant* | *0.095* | *0.116* | *0.11* | *131* | *1.41x* |
| bq-mut-runs | 0.097 | 0.146 | 0.10 | 131 | 1.34x |
| *bq-expand-aa-distant* | *0.101* | *0.175* | *0.11* | *128* | *2.52x* |
| bq-expand-qr-prim | 0.103 | 0.175 | 0.10 | 128 | 2.52x |
| bq-expand-b | 0.103 | 0.175 | 0.11 | 128 | 2.52x |
| bq-expand | 0.103 | 0.175 | 0.14 | 128 | 2.52x |
| bq-expand-zf | 0.103 | 0.186 | 0.13 | 128 | 2.52x |
| *bq-expand-aa-adjacent* | *0.104* | *0.175* | *0.11* | *128* | *2.52x* |
| offtab | 0.118 | 0.203 | 1.24 | 122 | 2.00x |
| *offtab-aa-distant* | *0.120* | *0.207* | *1.20* | *122* | *2.00x* |
| *offtab-aa-adjacent* | *0.120* | *0.208* | *1.67* | *122* | *2.00x* |
| offtab-scan-rem | 0.125 | 0.129 | 0.07 | 124 | 2.00x |
| bq-mut | 0.145 | 0.210 | 1.37 | 120 | 1.34x |
| bq-gen | 0.439 | 0.643 | 1.76 | 98 | 1.34x |
| *list-aa-adjacent* | *0.998* | *1.003* | *0.22* | *86* | *23.43x* |
| *list-aa-distant* | *0.999* | *1.002* | *0.30* | *86* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 86 | 23.43x |
| *gen-unsafe-aa-adjacent* | *1.116* | *1.258* | *1.37* | *84* | *1.00x* |
| gen-unsafe | 1.131 | 1.278 | 0.87 | 84 | 1.00x |
| *gen-unsafe-aa-distant* | *1.161* | *1.267* | *1.60* | *83* | *1.00x* |
| gen-quotrem | 1.204 | 1.330 | 2.59 | 83 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0265, worst
cell 4.99% on `rev-gather48-src-50`, and 15 of 18 intervals cover 1.
The `sum-only` halves agree at 1.0005 on a worst cell of 0.38%
on `rev-gather48-src-50`, its interval covering 1. The in-situ term reads
0.9986, 0.9969, 1.0095 of `sum-only` as medians, on `mut-odo-vecdims`,
`mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0257, which the correction
amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m11s, peak 88 MiB in use, 19 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.22 ms per call raw, 4.07 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes):** `mut-odo-vecdims` 0.070/0.052/0.029 `bq-scan-rem-gm-mulback`
0.096/0.097/0.090

**Across the halves:** 28 of the 42 arms are faster on this half and 14 slower,
at a geomean of 0.9845, from `bq-odo-gm-mulback-aa-distant` at 0.9039
to `bq-gen` at 1.0889, with `list` itself at 1.0068.

**What the class says:** all three properties hold, and the class reproduces
the main ordering. The `mut-odo-vecdims` row's `worst` is 0.070; `bq-expand`
sits behind it at 2.4497 paired, behind on all three shapes; and the vecdims
family heads the table, though the member leading is `mut-odo-vecdims-add-in`
rather than the arm itself, by **0.9808** paired at 2 of 3 shapes --- a 1.92%
margin inside this class's 2.65% floor, so a sort order and not a separation.
Its floor, 2.65%, is the third tightest of the eight.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *90* | *2.52x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.11* | *94* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *mut-odo-vecdims-aa-distant* | *0.047* | *0.059* | *0.09* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.047* | *0.059* | *0.10* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.047** | 0.059 | 0.10 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.048 | 0.057 | 0.11 | 96 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.049 | 0.061 | 0.13 | 96 | 1.00x |
| mut-odo-vecdims-add-both | 0.050 | 0.063 | 0.15 | 96 | 1.00x |
| mut-odo-vecdims-add-out | 0.054 | 0.065 | 0.11 | 96 | 1.00x |
| mut-flat-gm | 0.078 | 0.089 | 0.13 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.087 | 0.096 | 0.09 | 87 | 1.33x |
| bq-mut-runs | 0.092 | 0.107 | 0.11 | 85 | 1.33x |
| bq-expand-gm-mulback | 0.093 | 0.120 | 0.19 | 83 | 2.52x |
| build | 0.096 | 0.140 | 1.96 | 96 | 1.00x |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.101 | 0.09 | 87 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.099* | *0.101* | *0.12* | *87* | *1.33x* |
| *build-aa-distant* | *0.099* | *0.134* | *0.33* | *96* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.102* | *0.11* | *87* | *1.33x* |
| bq-expand-b | 0.100 | 0.130 | 0.11 | 83 | 2.52x |
| bq-expand-qr-prim | 0.100 | 0.129 | 0.13 | 83 | 2.52x |
| *mut-odo-aa-adjacent* | *0.100* | *0.138* | *1.83* | *96* | *1.00x* |
| *bq-expand-aa-distant* | *0.101* | *0.130* | *0.15* | *83* | *2.52x* |
| bq-expand-zf | 0.101 | 0.136 | 0.14 | 83 | 2.52x |
| bq-expand | 0.101 | 0.130 | 0.10 | 83 | 2.52x |
| *bq-expand-aa-adjacent* | *0.101* | *0.130* | *0.16* | *83* | *2.52x* |
| bq-odo-gm-mulback | 0.102 | 0.123 | 0.12 | 83 | 1.41x |
| *build-aa-adjacent* | *0.102* | *0.137* | *2.36* | *96* | *1.00x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.102* | *0.123* | *0.11* | *83* | *1.41x* |
| *bq-odo-gm-mulback-aa-distant* | *0.102* | *0.123* | *0.11* | *83* | *1.41x* |
| *mut-odo-aa-distant* | *0.104* | *0.141* | *2.03* | *96* | *1.00x* |
| mut-odo | 0.107 | 0.136 | 1.80 | 96 | 1.00x |
| *offtab-aa-adjacent* | *0.110* | *0.171* | *0.26* | *90* | *2.00x* |
| offtab | 0.111 | 0.174 | 1.95 | 90 | 2.00x |
| *offtab-aa-distant* | *0.113* | *0.171* | *0.21* | *89* | *2.00x* |
| offtab-scan-rem | 0.128 | 0.131 | 0.13 | 83 | 2.00x |
| bq-mut | 0.138 | 0.166 | 1.23 | 83 | 1.33x |
| bq-gen | 0.442 | 0.634 | 1.44 | 82 | 1.33x |
| *list-aa-distant* | *0.998* | *1.001* | *0.25* | *47* | *23.43x* |
| *list-aa-adjacent* | *0.999* | *0.999* | *0.22* | *47* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 47 | 23.43x |
| *gen-unsafe-aa-adjacent* | *1.133* | *1.318* | *0.80* | *44* | *1.00x* |
| gen-unsafe | 1.150 | 1.327 | 1.20 | 43 | 1.00x |
| *gen-unsafe-aa-distant* | *1.173* | *1.360* | *1.67* | *44* | *1.00x* |
| gen-quotrem | 1.174 | 1.368 | 1.57 | 43 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0200, worst
cell 9.97% on `revsome-outer-g48`, and 13 of 18 intervals cover 1.
The `sum-only` halves agree at 0.9976 on a worst cell of 0.40%
on `revsome-outer-g48`, its interval covering 1. The in-situ term reads 1.0200,
1.0206, 1.0136 of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0197, which the correction amplifies
by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m15s, peak 117 MiB in use, 19 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 4.21 ms per call raw, 4.06 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.053/0.059
`bq-scan-rem-gm-mulback` 0.101/0.099/0.097

**Across the halves:** 26 of the 42 arms are faster on this half and 16 slower,
at a geomean of 0.9889, from `bq-odo-gm-mulback` at 0.9334 to `bq-gen`
at 1.0638, with `list` itself at 1.0186. **The baseline moved 1.86% between
the halves, past the 0.7% that lets two columns be differenced, so this line
is NOT read for the pair's variable.** The table above is one process's
and stands; what goes is the comparison.

**What the class says:** all three properties hold, and **this is one of the two
populations where `mut-odo-vecdims` heads the table outright**, at 0.047,
as it did on Run 18. The `mut-odo-vecdims` row's `worst` is 0.059
and `bq-expand` sits behind it at 2.2952 paired, behind on all three shapes.
What is worth more than the ordering is the floor, for the second run running:
**2.00% here, the tightest of the eight**, against Run 18's 4.20% and Run 17's
18.05%, which was the largest of that run's eight and carried its 74.48% cell.
Neither the cell nor the looseness has returned in two runs, so the population
Run 17 called stably loose was not, and that reading can now be retired rather
than merely doubted.

**`bcast` --- an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.65* | *52* | *1.38x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.70* | *58* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.36* | *81* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| mut-odo-vecdims-add-both-down | 0.035 | 0.066 | 0.48 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.036* | *0.062* | *0.46* | *60* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.036* | *0.062* | *0.54* | *60* | *1.00x* |
| mut-odo-vecdims-add-in | 0.036 | 0.061 | 0.53 | 60 | 1.00x |
| **mut-odo-vecdims** | **0.036** | 0.062 | 0.68 | 60 | 1.00x |
| mut-odo-vecdims-add-both | 0.037 | 0.067 | 0.51 | 60 | 1.00x |
| mut-odo-vecdims-add-out | 0.037 | 0.066 | 0.50 | 60 | 1.00x |
| build | 0.057 | 0.131 | 1.18 | 60 | 1.00x |
| *build-aa-adjacent* | *0.057* | *0.146* | *1.36* | *60* | *1.00x* |
| *build-aa-distant* | *0.057* | *0.139* | *2.13* | *60* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.058* | *0.152* | *1.37* | *60* | *1.00x* |
| *mut-odo-aa-distant* | *0.058* | *0.150* | *1.56* | *60* | *1.00x* |
| mut-odo | 0.059 | 0.152 | 1.13 | 60 | 1.00x |
| mut-flat-gm | 0.067 | 0.071 | 0.62 | 49 | 1.13x |
| bq-mut-runs-gm-mulback | 0.079 | 0.089 | 0.67 | 47 | 1.13x |
| bq-expand-gm-mulback | 0.079 | 0.082 | 0.63 | 48 | 1.38x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.082* | *0.088* | *0.66* | *47* | *1.14x* |
| bq-odo-gm-mulback | 0.083 | 0.088 | 0.68 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-distant* | *0.083* | *0.088* | *0.57* | *47* | *1.14x* |
| bq-mut-runs | 0.086 | 0.095 | 0.68 | 46 | 1.13x |
| bq-expand-b | 0.088 | 0.096 | 0.69 | 46 | 1.38x |
| *offtab-aa-distant* | *0.089* | *0.172* | *0.66* | *52* | *2.00x* |
| *offtab-aa-adjacent* | *0.089* | *0.173* | *0.89* | *52* | *2.00x* |
| offtab | 0.090 | 0.179 | 0.89 | 52 | 2.00x |
| bq-expand-qr-prim | 0.091 | 0.096 | 0.66 | 46 | 1.38x |
| *bq-expand-aa-adjacent* | *0.091* | *0.096* | *0.70* | *46* | *1.38x* |
| **bq-scan-rem-gm-mulback** | **0.091** | 0.098 | 0.68 | 47 | 1.13x |
| bq-expand-zf | 0.091 | 0.097 | 0.82 | 46 | 1.38x |
| bq-expand | 0.091 | 0.097 | 0.66 | 46 | 1.38x |
| *bq-expand-aa-distant* | *0.091* | *0.097* | *0.36* | *46* | *1.38x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.100* | *0.37* | *47* | *1.13x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.098* | *0.66* | *47* | *1.13x* |
| bq-mut | 0.120 | 0.158 | 0.65 | 46 | 1.13x |
| offtab-scan-rem | 0.126 | 0.136 | 1.06 | 43 | 2.00x |
| bq-gen | 0.184 | 0.299 | 0.73 | 46 | 1.13x |
| gen-unsafe | 0.902 | 0.986 | 2.63 | 22 | 1.00x |
| gen-quotrem | 0.922 | 0.962 | 3.35 | 21 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.935* | *0.978* | *2.84* | *22* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.981* | *0.985* | *1.80* | *21* | *1.00x* |
| *list-aa-distant* | *0.997* | *1.003* | *1.21* | *18* | *20.62x* |
| list (baseline) | 1.000 | 1.000 | 1.09 | 18 | 20.62x |
| *list-aa-adjacent* | *1.003* | *1.011* | *0.69* | *18* | *20.62x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0479, worst
cell 10.82% on `bcast-tall-Mx2`, and 16 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0003 on a worst cell of 0.07% on `bcast-inner900`,
its interval covering 1. The in-situ term reads 1.0331, 1.0126, 1.0212
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0453, which the correction amplifies by 1.05x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m16s, peak 137 MiB in use, 40 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 28.2 ms per call raw, 27.1 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900,
bcast-tall-Mx2):** `mut-odo-vecdims` 0.033/0.022/0.062 `bq-scan-rem-gm-mulback`
0.090/0.089/0.098

**Across the halves:** 21 of the 42 arms are faster on this half and 21 slower,
at a geomean of 0.9836, from `bq-odo-gm-mulback-aa-distant` at 0.8883
to `mut-odo-vecdims-add-both-down` at 1.0381, with `list` itself at 1.0018.

**What the class says:** all three properties hold. The `mut-odo-vecdims` row's
`worst` is 0.062, `bq-expand` sits behind it at 2.5499 paired and behind on all
three shapes, and the family member leading is `mut-odo-vecdims-add-both-down`
by **0.9813** paired at 2 of 3 --- a 1.87% margin inside this class's 4.79%
floor, so a sort order and not a separation, and the same member led here on
Run 18. The one figure of this class that is not a fill's
is `mut-flat-gm / mut-odo-vecdims` at 1.8606, whose interval reaches **0.9990**
--- so the best arm outside the family is level with the fix at the bottom
of its range here, where in five of the eight classes that interval stays clear
of 1 entirely. Two go further than `bcast` does: `window` and `reshape1`, both
of them putting that arm ahead on a unit-innermost shape.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000,
`sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.23* | *87* | *2.11x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.80* | *94* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.50* | *102* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *108* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *108* | *0.00x* |
| mut-odo-vecdims-add-in | 0.036 | 0.058 | 0.14 | 94 | 1.00x |
| *mut-odo-vecdims-aa* | *0.036* | *0.058* | *0.49* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.037* | *0.058* | *0.47* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.037** | 0.059 | 0.52 | 94 | 1.00x |
| mut-odo-vecdims-add-both | 0.038 | 0.064 | 0.10 | 93 | 1.00x |
| mut-odo-vecdims-add-out | 0.039 | 0.066 | 0.12 | 93 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.042 | 0.062 | 0.26 | 93 | 1.00x |
| build | 0.063 | 0.138 | 1.52 | 81 | 1.00x |
| *build-aa-adjacent* | *0.065* | *0.148* | *2.36* | *81* | *1.00x* |
| *build-aa-distant* | *0.066* | *0.148* | *2.00* | *80* | *1.00x* |
| mut-flat-gm | 0.066 | 0.090 | 0.43 | 87 | 1.33x |
| *mut-odo-aa-adjacent* | *0.067* | *0.147* | *2.21* | *81* | *1.00x* |
| *mut-odo-aa-distant* | *0.068* | *0.158* | *1.37* | *80* | *1.00x* |
| mut-odo | 0.069 | 0.157 | 1.06 | 80 | 1.00x |
| bq-mut-runs-gm-mulback | 0.078 | 0.100 | 0.23 | 85 | 1.33x |
| bq-mut-runs | 0.084 | 0.107 | 0.13 | 84 | 1.33x |
| bq-expand-gm-mulback | 0.084 | 0.122 | 0.18 | 83 | 2.11x |
| **bq-scan-rem-gm-mulback** | **0.085** | 0.100 | 0.16 | 84 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.085* | *0.100* | *0.13* | *84* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.086* | *0.099* | *0.12* | *84* | *1.33x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.086* | *0.125* | *0.14* | *83* | *1.33x* |
| bq-odo-gm-mulback | 0.086 | 0.125 | 0.13 | 83 | 1.33x |
| *bq-odo-gm-mulback-aa-distant* | *0.086* | *0.124* | *0.19* | *83* | *1.33x* |
| bq-expand-qr-prim | 0.094 | 0.132 | 0.18 | 82 | 2.11x |
| bq-expand | 0.095 | 0.131 | 0.13 | 82 | 2.11x |
| bq-expand-b | 0.095 | 0.133 | 0.13 | 82 | 2.11x |
| *bq-expand-aa-adjacent* | *0.095* | *0.132* | *0.16* | *82* | *2.11x* |
| *bq-expand-aa-distant* | *0.095* | *0.132* | *0.18* | *82* | *2.11x* |
| bq-expand-zf | 0.097 | 0.139 | 0.17 | 81 | 2.11x |
| offtab | 0.097 | 0.169 | 1.64 | 78 | 2.00x |
| *offtab-aa-distant* | *0.098* | *0.161* | *2.40* | *79* | *2.00x* |
| *offtab-aa-adjacent* | *0.099* | *0.175* | *1.52* | *78* | *2.00x* |
| offtab-scan-rem | 0.116 | 0.128 | 0.19 | 79 | 2.00x |
| bq-mut | 0.120 | 0.170 | 0.92 | 78 | 1.33x |
| bq-gen | 0.270 | 0.654 | 2.09 | 54 | 1.33x |
| *gen-unsafe-aa-distant* | *0.918* | *1.347* | *1.48* | *42* | *1.00x* |
| gen-unsafe | 0.922 | 1.359 | 1.67 | 42 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.949* | *1.336* | *3.48* | *42* | *1.00x* |
| gen-quotrem | 0.968 | 1.405 | 2.30 | 41 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.30 | 44 | 23.31x |
| *list-aa-adjacent* | *1.000* | *1.006* | *0.61* | *44* | *23.31x* |
| *list-aa-distant* | *1.009* | *1.016* | *0.31* | *44* | *23.31x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0416, worst cell
7.36% on `bcastmid-c32-cnn`, and 10 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9988 on a worst cell of 0.35% on `bcastmid-b200k`,
its interval covering 1. The in-situ term reads 1.0251, 1.0173, 1.0094
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0316, which the correction amplifies by 1.52x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m15s, peak 125 MiB in use, 33 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 46.7 ms per call raw, 45.6 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k):** `mut-odo-vecdims` 0.059/0.022/0.037 `bq-scan-rem-gm-mulback`
0.100/0.087/0.071

**Across the halves:** 20 of the 42 arms are faster on this half and 22 slower,
at a geomean of 0.9887, from `bq-odo-gm-mulback` at 0.9035 to `bq-gen`
at 1.0769, with `list` itself at 1.0160. **The baseline moved 1.60% between
the halves, past the 0.7% that lets two columns be differenced, so this line
is NOT read for the pair's variable.** The table above is one process's
and stands; what goes is the comparison.

**What the class says:** all three properties hold and nothing inverted.
The `mut-odo-vecdims` row's `worst` is 0.059, `bq-expand / mut-odo-vecdims`
reads 2.5840 paired and is behind on all three shapes,
and `mut-odo-vecdims-add-in / mut-odo-vecdims` is **0.9795** paired at 3 of 3
--- a 2.05% margin against a 4.16% floor, so ahead on every shape and still
inside the floor, which is what a three-shape population can say and no more.
**This class's cross-half line is not read for the pair's variable**: `list`
moved 1.60% between the halves, past the 0.7% that lets two columns
be differenced. The table above is one process's and stands.

**`reshape1` --- the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1), `reshape1-rank10` (`l` 59049, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *84* | *5.43x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.31* | *97* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.31* | *87* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| bq-mut-runs-gm-mulback | 0.033 | 0.113 | 0.26 | 97 | 2.00x |
| mut-flat-gm | 0.033 | 0.135 | 0.27 | 95 | 2.00x |
| bq-odo-gm-mulback | 0.058 | 0.143 | 0.16 | 92 | 2.31x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.058* | *0.142* | *0.15* | *92* | *2.31x* |
| *bq-odo-gm-mulback-aa-distant* | *0.058* | *0.144* | *0.13* | *92* | *2.31x* |
| offtab-scan-rem | 0.073 | 0.092 | 0.15 | 86 | 2.00x |
| bq-mut-runs | 0.074 | 0.162 | 0.28 | 86 | 2.00x |
| **bq-scan-rem-gm-mulback** | **0.074** | 0.091 | 0.14 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.074* | *0.091* | *0.13* | *86* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.076* | *0.091* | *0.12* | *86* | *2.00x* |
| bq-expand-gm-mulback | 0.079 | 0.171 | 0.43 | 86 | 5.43x |
| mut-odo-vecdims-add-in | 0.093 | 0.107 | 0.08 | 83 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.093* | *0.109* | *0.19* | *83* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.094* | *0.113* | *0.29* | *83* | *1.00x* |
| **mut-odo-vecdims** | **0.094** | 0.110 | 0.22 | 83 | 1.00x |
| mut-odo-vecdims-add-both | 0.102 | 0.123 | 0.08 | 81 | 1.00x |
| mut-odo-vecdims-add-out | 0.102 | 0.123 | 0.20 | 81 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.105 | 0.118 | 0.19 | 81 | 1.00x |
| bq-expand-b | 0.115 | 0.201 | 0.31 | 79 | 5.43x |
| bq-expand-qr-prim | 0.121 | 0.202 | 0.33 | 79 | 5.43x |
| bq-expand | 0.121 | 0.202 | 0.43 | 79 | 5.43x |
| *bq-expand-aa-distant* | *0.121* | *0.204* | *0.27* | *79* | *5.43x* |
| *bq-expand-aa-adjacent* | *0.121* | *0.202* | *0.37* | *79* | *5.43x* |
| bq-expand-zf | 0.125 | 0.219 | 0.32 | 79 | 5.43x |
| build | 0.231 | 0.311 | 3.84 | 67 | 1.00x |
| bq-mut | 0.247 | 0.298 | 2.32 | 66 | 2.00x |
| *build-aa-distant* | *0.250* | *0.297* | *3.20* | *67* | *1.00x* |
| *build-aa-adjacent* | *0.251* | *0.303* | *2.94* | *66* | *1.00x* |
| mut-odo | 0.262 | 0.337 | 2.33 | 66 | 1.00x |
| *mut-odo-aa-distant* | *0.263* | *0.331* | *2.47* | *65* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.283* | *0.332* | *2.44* | *65* | *1.00x* |
| offtab | 0.285 | 0.351 | 2.52 | 64 | 2.00x |
| *offtab-aa-distant* | *0.288* | *0.353* | *1.43* | *64* | *2.00x* |
| *offtab-aa-adjacent* | *0.293* | *0.366* | *0.61* | *64* | *2.00x* |
| *gen-unsafe-aa-adjacent* | *0.877* | *2.044* | *0.85* | *45* | *1.00x* |
| gen-unsafe | 0.895 | 2.061 | 2.02 | 45 | 1.00x |
| *gen-unsafe-aa-distant* | *0.913* | *1.969* | *1.50* | *43* | *1.00x* |
| gen-quotrem | 0.929 | 2.079 | 1.90 | 43 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.34 | 42 | 32.34x |
| *list-aa-distant* | *1.000* | *1.009* | *0.41* | *41* | *32.34x* |
| *list-aa-adjacent* | *1.001* | *1.004* | *0.22* | *42* | *32.34x* |
| bq-gen | 1.110 | 2.835 | 2.08 | 39 | 2.00x |

**Controls:** The largest A/A pair is `mut-odo-aa-adjacent` at 1.0811, worst
cell 15.54% on `reshape1-500k`, and 17 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9999 on a worst cell of 0.10% on `reshape1-rank10`,
its interval covering 1. The in-situ term reads 0.9951, 1.0298, 1.1566
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0735, which the correction amplifies by 1.08x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m15s, peak 122 MiB in use, 25 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 13.3 ms per call raw, 13 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3,
reshape1-rank10):** `mut-odo-vecdims` 0.089/0.092/0.110 `bq-scan-rem-gm-mulback`
0.074/0.073/0.091

**Across the halves:** 27 of the 42 arms are faster on this half and 15 slower,
at a geomean of 0.9873, from `mut-odo` at 0.9018 to `bq-gen` at 1.0982,
with `list` itself at 1.0005.

**What the class says:** **property 2 breaks here and only here**, as it did
on Runs 16, 17 and 18 and for the same reason: the fills own the top outright,
`bq-mut-runs-gm-mulback` at **0.033** and `mut-flat-gm` beside it against
`mut-odo-vecdims`'s **0.094** --- 0.5042 and 0.5355 paired, a margin near 50%
that this class's 8.11% floor, the widest of the eight, comes nowhere near.
It is the one break of the eight that is a break and not a sort. Properties 1
and 3 hold --- `worst` 0.110 on the `mut-odo-vecdims` row, the highest
of the eight, and `bq-expand` at 5.43x the result vector where `scaled` puts
it at 1.14x, which is `m = l` showing through exactly as that property warns.
`bq-expand / mut-odo-vecdims` is **1.2534 on an interval reaching 0.8801, ahead
on one shape of three**, so in this class the last candidate is not measurably
behind the arm that ships --- the only population of the nine where
that is true. This population was the standing case for a stride-conditioned
redirect from Run 16 on; the drop of 2026-08-24 sends it to [the two-stage
plan](../README.md#the-two-stage-plan-and-the-rework-proposal) instead, whose
canonicalization pass reclassifies every shape of it to regime 1.

**`slice` --- a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.15* | *90* | *1.58x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.27* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in | 0.040 | 0.057 | 0.11 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.058* | *0.13* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.040* | *0.058* | *0.12* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.040** | 0.059 | 0.09 | 96 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.041 | 0.061 | 0.09 | 96 | 1.00x |
| mut-odo-vecdims-add-both | 0.042 | 0.063 | 0.09 | 96 | 1.00x |
| mut-odo-vecdims-add-out | 0.043 | 0.065 | 0.07 | 96 | 1.00x |
| *build-aa-distant* | *0.064* | *0.140* | *1.23* | *96* | *1.00x* |
| *mut-odo-aa-distant* | *0.065* | *0.140* | *1.00* | *96* | *1.00x* |
| build | 0.065 | 0.140 | 1.10 | 95 | 1.00x |
| mut-odo | 0.065 | 0.135 | 1.32 | 96 | 1.00x |
| *build-aa-adjacent* | *0.065* | *0.146* | *0.19* | *95* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.066* | *0.148* | *1.19* | *96* | *1.00x* |
| mut-flat-gm | 0.083 | 0.091 | 0.25 | 88 | 1.08x |
| bq-mut-runs-gm-mulback | 0.091 | 0.092 | 0.26 | 87 | 1.08x |
| offtab | 0.094 | 0.170 | 0.56 | 90 | 2.00x |
| *offtab-aa-distant* | *0.094* | *0.171* | *0.35* | *90* | *2.00x* |
| *offtab-aa-adjacent* | *0.096* | *0.170* | *0.81* | *90* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.098** | 0.102 | 0.08 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.102* | *0.09* | *86* | *1.08x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.098* | *0.102* | *0.14* | *86* | *1.08x* |
| bq-mut-runs | 0.100 | 0.102 | 0.34 | 85 | 1.08x |
| bq-expand-gm-mulback | 0.104 | 0.121 | 0.13 | 83 | 1.58x |
| bq-expand-qr-prim | 0.109 | 0.129 | 0.10 | 83 | 1.58x |
| bq-odo-gm-mulback | 0.109 | 0.122 | 0.10 | 83 | 1.50x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.110* | *0.123* | *0.09* | *83* | *1.50x* |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.123* | *0.08* | *83* | *1.50x* |
| bq-expand-b | 0.110 | 0.129 | 0.13 | 83 | 1.58x |
| *bq-expand-aa-adjacent* | *0.110* | *0.129* | *0.10* | *83* | *1.58x* |
| *bq-expand-aa-distant* | *0.110* | *0.129* | *0.08* | *83* | *1.58x* |
| bq-expand | 0.110 | 0.130 | 0.10 | 83 | 1.58x |
| bq-expand-zf | 0.112 | 0.136 | 0.13 | 83 | 1.58x |
| bq-mut | 0.127 | 0.180 | 0.16 | 83 | 1.08x |
| offtab-scan-rem | 0.129 | 0.132 | 0.18 | 82 | 2.00x |
| bq-gen | 0.275 | 0.618 | 1.60 | 82 | 1.08x |
| *list-aa-distant* | *0.996* | *0.999* | *0.22* | *46* | *20.54x* |
| *list-aa-adjacent* | *0.999* | *1.002* | *0.22* | *46* | *20.54x* |
| list (baseline) | 1.000 | 1.000 | 0.25 | 46 | 20.54x |
| gen-unsafe | 1.422 | 2.248 | 0.72 | 44 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.439* | *2.300* | *1.18* | *44* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.451* | *2.261* | *1.24* | *43* | *1.00x* |
| gen-quotrem | 1.459 | 2.300 | 1.11 | 43 | 1.00x |

**Controls:** The largest A/A pair is `offtab-aa-adjacent` at 1.0243, worst cell
6.96% on `slice-coprime-r7`, and 15 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9995 on a worst cell of 0.37% on `slice-primes`, its interval
covering 1. The in-situ term reads 1.0177, 1.0212, 1.0497 of `sum-only`
as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 1.0175, which the correction amplifies by 1.38x --- quote both wherever
that is past 1.5.

**Provenance:** elapsed 0h12m13s, peak 118 MiB in use, 30 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.17 ms per call raw, 4.02 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7):** `mut-odo-vecdims` 0.059/0.030/0.037
`bq-scan-rem-gm-mulback` 0.098/0.102/0.095

**Across the halves:** 32 of the 42 arms are faster on this half and 10 slower,
at a geomean of 0.9830, from `bq-scan-rem-gm-mulback` at 0.9355 to `bq-gen`
at 1.0581, with `list` itself at 1.0010.

**What the class says:** all three properties hold and the class reproduces
the main ordering. The `mut-odo-vecdims` row's `worst` is 0.059,
`bq-expand / mut-odo-vecdims` is 2.7337 and is behind on all three shapes,
and `mut-odo-vecdims-add-in / mut-odo-vecdims` is **0.9856** paired at 2 of 3
--- a 1.44% margin inside this class's 2.43% floor, which is a tie in all
but the sort. This is the class Run 18 reversed the halves' order on, to tell
*the 9.12 half* from *the second process of the two*; no such probe was taken
this run, so the cross-half direction here is aliased with the order again.

**`window` --- overlapping im2col patches: the workload the README opens
by naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *116* | *2.81x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.96* | *135* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.89* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *150* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *150* | *0.00x* |
| mut-odo-vecdims-add-in | 0.060 | 0.095 | 0.08 | 116 | 1.00x |
| *mut-odo-vecdims-aa* | *0.062* | *0.096* | *0.28* | *116* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.095* | *0.21* | *116* | *1.00x* |
| **mut-odo-vecdims** | **0.062** | 0.097 | 0.27 | 116 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.065 | 0.103 | 0.06 | 115 | 1.01x |
| mut-odo-vecdims-add-both | 0.067 | 0.105 | 0.06 | 114 | 1.01x |
| mut-odo-vecdims-add-out | 0.068 | 0.105 | 0.05 | 114 | 1.01x |
| mut-flat-gm | 0.070 | 0.086 | 0.86 | 127 | 1.33x |
| bq-mut-runs-gm-mulback | 0.075 | 0.095 | 0.53 | 127 | 1.33x |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.094 | 0.07 | 120 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.094* | *0.08* | *120* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.093* | *0.095* | *0.16* | *120* | *1.33x* |
| bq-odo-gm-mulback | 0.094 | 0.117 | 0.25 | 121 | 2.55x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.118* | *0.20* | *121* | *2.55x* |
| bq-mut-runs | 0.094 | 0.103 | 0.66 | 118 | 1.33x |
| *bq-odo-gm-mulback-aa-distant* | *0.094* | *0.119* | *0.19* | *121* | *2.55x* |
| bq-expand-gm-mulback | 0.098 | 0.115 | 0.13 | 119 | 2.81x |
| bq-expand-qr-prim | 0.119 | 0.125 | 0.11 | 112 | 2.81x |
| offtab-scan-rem | 0.119 | 0.121 | 0.10 | 120 | 2.00x |
| bq-expand | 0.119 | 0.127 | 0.19 | 112 | 2.81x |
| bq-expand-b | 0.119 | 0.127 | 0.13 | 112 | 2.81x |
| *bq-expand-aa-distant* | *0.120* | *0.127* | *0.13* | *112* | *2.81x* |
| *bq-expand-aa-adjacent* | *0.120* | *0.127* | *0.11* | *112* | *2.81x* |
| bq-expand-zf | 0.123 | 0.132 | 0.11 | 112 | 2.81x |
| build | 0.143 | 0.250 | 3.07 | 99 | 1.00x |
| *build-aa-distant* | *0.147* | *0.266* | *1.99* | *98* | *1.00x* |
| *mut-odo-aa-distant* | *0.149* | *0.254* | *2.49* | *99* | *1.00x* |
| mut-odo | 0.149 | 0.263 | 2.76 | 99 | 1.00x |
| *mut-odo-aa-adjacent* | *0.152* | *0.261* | *2.16* | *99* | *1.00x* |
| *build-aa-adjacent* | *0.154* | *0.278* | *2.65* | *98* | *1.00x* |
| offtab | 0.178 | 0.295 | 2.48 | 96 | 2.00x |
| *offtab-aa-distant* | *0.180* | *0.299* | *2.54* | *96* | *2.00x* |
| *offtab-aa-adjacent* | *0.180* | *0.278* | *1.89* | *97* | *2.00x* |
| bq-mut | 0.182 | 0.256 | 1.62 | 99 | 1.33x |
| bq-gen | 0.595 | 1.065 | 2.27 | 72 | 1.33x |
| *gen-unsafe-aa-adjacent* | *0.977* | *1.164* | *1.32* | *77* | *1.00x* |
| gen-unsafe | 0.982 | 1.178 | 1.07 | 77 | 1.00x |
| *list-aa-distant* | *0.996* | *1.000* | *0.32* | *73* | *24.76x* |
| list (baseline) | 1.000 | 1.000 | 0.41 | 73 | 24.76x |
| *list-aa-adjacent* | *1.003* | *1.007* | *0.45* | *72* | *24.76x* |
| *gen-unsafe-aa-distant* | *1.025* | *1.289* | *1.31* | *75* | *1.00x* |
| gen-quotrem | 1.051 | 1.273 | 0.95 | 76 | 1.00x |

**Controls:** The largest A/A pair is `build-aa-adjacent` at 1.0757, worst cell
11.34% on `window-64x64-k1x9`, and 13 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0005 on a worst cell of 0.08% on `window-224x224-k3`,
its interval missing 1. The in-situ term reads 1.0022, 0.9958, 1.0396
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0647, which the correction amplifies by 1.21x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m14s, peak 103 MiB in use, 30 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.67 ms per call raw, 9.4 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9):** `mut-odo-vecdims` 0.044/0.055/0.097
`bq-scan-rem-gm-mulback` 0.094/0.094/0.074

**Across the halves:** 28 of the 42 arms are faster on this half and 14 slower,
at a geomean of 0.9889, from `mut-odo-aa-distant` at 0.8925 to `bq-gen`
at 1.1176, with `list` itself at 1.0143. **The baseline moved 1.43% between
the halves, past the 0.7% that lets two columns be differenced, so this line
is NOT read for the pair's variable.** The table above is one process's
and stands; what goes is the comparison.

**What the class says:** all three properties hold. The `mut-odo-vecdims` row's
`worst` is 0.097, and the shape carrying it is `window-64x64-k1x9`,
the unit-innermost view where the best arm outside the family beats the fix ---
the same one-dimensional trap `reshape1` is built of, arriving here on one shape
of three rather than on all of them, which is why
`mut-flat-gm / mut-odo-vecdims` over the three reads **1.0877 on an interval
from 0.4683 to 1.7647**, level on the point estimate and resolving nothing.
`bq-expand / mut-odo-vecdims` reads 1.9282 paired, behind on all three shapes,
and `mut-odo-vecdims-add-in / mut-odo-vecdims` is **0.9704** paired at 3 of 3,
a whole-population sign at a 2.96% margin inside this class's 7.57% floor,
the second widest of the eight. **This class's cross-half line is not read
for the pair's variable**, `list` having moved 1.43% between the halves.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one
strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *119* | *1.14x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.12* | *124* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.19* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *mut-odo-vecdims-aa* | *0.032* | *0.033* | *0.09* | *126* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.033* | *0.07* | *126* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.033 | 0.10 | 126 | 1.00x |
| mut-odo-vecdims-add-both-down | 0.032 | 0.035 | 0.09 | 126 | 1.00x |
| mut-odo-vecdims-add-out | 0.033 | 0.036 | 0.10 | 125 | 1.00x |
| mut-odo-vecdims-add-in | 0.033 | 0.033 | 0.10 | 126 | 1.00x |
| *mut-odo-aa-distant* | *0.033* | *0.047* | *0.09* | *125* | *1.00x* |
| *build-aa-distant* | *0.034* | *0.048* | *0.13* | *124* | *1.00x* |
| mut-odo-vecdims-add-both | 0.035 | 0.035 | 0.20 | 125 | 1.00x |
| *mut-odo-aa-adjacent* | *0.036* | *0.048* | *0.34* | *124* | *1.00x* |
| mut-odo | 0.037 | 0.048 | 0.16 | 124 | 1.00x |
| build | 0.037 | 0.047 | 0.19 | 124 | 1.00x |
| *build-aa-adjacent* | *0.038* | *0.047* | *0.14* | *124* | *1.00x* |
| *offtab-aa-adjacent* | *0.066* | *0.072* | *0.27* | *118* | *2.00x* |
| *offtab-aa-distant* | *0.066* | *0.075* | *0.17* | *118* | *2.00x* |
| offtab | 0.066 | 0.074 | 0.33 | 118 | 2.00x |
| mut-flat-gm | 0.073 | 0.073 | 0.12 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.081 | 0.082 | 0.14 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.085 | 0.087 | 0.09 | 113 | 1.14x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.090* | *0.092* | *0.06* | *113* | *1.04x* |
| *bq-odo-gm-mulback-aa-distant* | *0.090* | *0.092* | *0.08* | *113* | *1.04x* |
| bq-odo-gm-mulback | 0.090 | 0.092 | 0.06 | 113 | 1.04x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.094* | *0.06* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.094* | *0.06* | *112* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.094 | 0.11 | 112 | 1.04x |
| bq-mut-runs | 0.092 | 0.093 | 0.07 | 112 | 1.03x |
| bq-expand-qr-prim | 0.095 | 0.098 | 0.07 | 112 | 1.14x |
| bq-expand-b | 0.096 | 0.099 | 0.06 | 112 | 1.14x |
| bq-expand-zf | 0.096 | 0.099 | 0.09 | 112 | 1.14x |
| bq-expand | 0.096 | 0.099 | 0.06 | 112 | 1.14x |
| *bq-expand-aa-adjacent* | *0.096* | *0.099* | *0.06* | *112* | *1.14x* |
| *bq-expand-aa-distant* | *0.096* | *0.099* | *0.06* | *112* | *1.14x* |
| bq-mut | 0.101 | 0.112 | 0.15 | 111 | 1.03x |
| offtab-scan-rem | 0.129 | 0.134 | 0.09 | 107 | 2.00x |
| bq-gen | 0.145 | 0.258 | 0.22 | 107 | 1.03x |
| *gen-unsafe-aa-adjacent* | *0.832* | *1.692* | *0.48* | *70* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.834* | *1.653* | *1.35* | *70* | *1.00x* |
| gen-unsafe | 0.862 | 1.734 | 0.90 | 70 | 1.00x |
| gen-quotrem | 0.929 | 1.747 | 1.48 | 68 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.29 | 71 | 19.43x |
| *list-aa-adjacent* | *1.003* | *1.006* | *0.19* | *71* | *19.43x* |
| *list-aa-distant* | *1.005* | *1.012* | *0.19* | *70* | *19.43x* |

**Controls:** The largest A/A pair is `mut-odo-aa-distant` at 0.9620, worst cell
7.15% on `scaled-rank1-m1`, and 13 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0002 on a worst cell of 0.06% on `scaled-rank1-m1`,
its interval covering 1. The in-situ term reads 1.0325, 0.9898, 1.0160
of `sum-only` as medians, on `mut-odo-vecdims`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 0.9812, which the correction amplifies by 2.00x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m15s, peak 110 MiB in use, 40 MiB max residency;
the reader reads 47 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.98 ms per call raw, 4.79 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1,
scaled-r5):** `mut-odo-vecdims` 0.029/0.033/0.033 `bq-scan-rem-gm-mulback`
0.092/0.090/0.094

**Across the halves:** 24 of the 42 arms are faster on this half and 18 slower,
at a geomean of 0.9857, from `bq-odo-gm-mulback-aa-adjacent` at 0.9141
to `bq-gen` at 1.0429, with `list` itself at 0.9973.

**What the class says:** all three properties hold, and this population is again
the tightest here on every count of that kind: `worst` 0.033
on the `mut-odo-vecdims` row, the lowest of the eight;
`bq-expand / mut-odo-vecdims` at **3.0563**, the widest of the eight and
on the tightest interval any class gives it, 2.8449 to 3.3650; and `bq-expand`
at 1.14x the result vector, the lowest allocation multiple of the eight, which
is the class's own small `m` showing through. **And this is the second
of the two populations where `mut-odo-vecdims` heads the table outright**,
at 0.032, where Run 18 had `mut-odo-vecdims-add-in` on top by 1.39% --- inside
the floor then and inside it now, so the two runs disagree about the sign
of a margin neither can resolve, which is the family's internal order still
being unsettled rather than a movement. Its floor is 3.80%, against 6.15% on Run
18, carried by `gen-unsafe`'s distant twin rather than `mut-odo-vecdims`'s,
so the standing A/A slot did not fire this run either. The best arm outside
the family is `mut-odo` at 0.037.



## Provenance

What this run's figures have to be read against, and it is a section
of this file because a run replaces every word of it. What does NOT move
with a run --- the delta chain that says which shape set and roster each run
measured, and the list of what a run replaces outside this file --- is [README's
own Provenance][prov].

**Run 19's halves differ in the compiler, as Run 18's did, and this one reaches
further than a released compiler can.** They share source, shim, shim setting,
roster, shapes, class lists, bench order, machine and the one baked RTS line ---
but not their position in the sequence, the control half having run first
in every pair, which aliases *9.12* with *second of the two* again; Run 18 broke
that tie on one class with an order probe and this run took none.
`cabal.project.ghead`'s freeze resolves the same `vector`, `criterion`
and `criterion-measurement` at the one index-state the other two plans hold,
so what differs is ghc-9.12.4 against GHC HEAD 10.1.20260803 and their boot
libraries, `base-4.21.2.0` with `ghc-internal-9.1204.0` against `base-4.23.0.0`
with `ghc-internal-10.100.0`. `.text` is 20406469 against 20551487 bytes,
and every address after the first difference moves: `--library` puts **11.1%**
of library self-loops at the same offset in their cache line and 77.1%
in the same straddle state, where two halves built from one source by one
compiler read 100% and Run 18's cross-compiler figure was 20.1%. **The tracked
`Main` fill groups do not even keep their shapes**, which Run 18's did:
`[0, 24, 0, 4]` and `[0, 0]` on the basis against `[23, 0, 1, 2]`, `[0, 0, 13]`
and `[0, 0]` on the control, the three-copy group being
`bq-mut-runs-gm-mulback`, `bq-mut-lemire-mulback` and `bq-mut-runs-mulback`
compiled to one seven-instruction body that 9.12 does not share between them.
Which arm owns which copy on HEAD is a `-g3` twin's to say and **the twin cannot
say it**, its addresses sitting at four different deltas from the timed binary's
rather than one, which is [the add-in entry][open]'s finding and not a detail.
**What does NOT transfer between these halves is a difference of absolutes**:
`list` moved **0.78%**, past the 0.7% that separates a subtractable pair
from one that can only be ordered, where Run 18 read 0.52%. **The correction
sits evenly on both**, the in-situ forcing term reading 1.0282/1.0295/1.0552
against 1.0267/1.0347/1.0492 as medians, so a ratio read within either half
carries almost none of its own.

**The sequence was launched once and ran to the end**, 00:21:14 to 06:52:34,
eighteen processes, every one exiting 0 with the bench count its roster asked
for --- 1128 twice and 141 sixteen times --- none of them reporting a selection
it did not ask for, and **none rerun**, which Run 18 could not say.
The wall-clock log is an unbroken record and closes with `major run complete`.
**The control half ran first throughout**, `ghead` before `g912` on the main set
and on each class in turn, which is the driver's order and the one the basis's
second position is read in; **the order was NOT varied**, so every class's
cross-half direction is aliased with its slot, where Run 18 had broken that tie
on `slice`. **The machine carried one exposed bench, and the run can name what
did it.** Seventeen of the eighteen processes report no bench reaching 0.25
foreign CPU. The basis main process reports one of its 1128 ---
`cnn-L1-6x6-c1/bq-expand` at 0.35 foreign, worst sample 201 ms --- and the cause
is a Claude Code update installing itself, named by the machine's owner. Its own
A/A twins bound it: the exposed copy sits 2.0 to 2.2% above two twins that agree
with each other to 0.19%, so one shape of 24 moves that arm's geomean
by under 0.09%, an order of magnitude inside the floor. **The rerun post-run
step 1c asks for was not taken, and was declined on 2026-08-25** by whoever
asked for the run, the exposure having been priced at under 0.09% on one arm;
so this main set is published with it, and the decision is recorded rather
than the debt. **The tree was NOT clean at launch**, and this is the run's
second small caveat: the driver's own `git status` recorded two untracked paths,
`micro-regime3/check-x.log` and `micro-regime3/probe-run20arms.sh`, neither
of them in the run's namespace and neither modified source. **The alone-leg
riders followed the sequence**, 06:53:30 onward, four invocations of 27
single-bench processes, 108 in all --- clean and saturated on each half, which
is what registration 3's decomposition needs. **The counted-work sweeps preceded
it**, taken 2026-08-24 on a machine doing ordinary work as that rider allows,
1128 data lines a half and no cell perf refused.

**The pair's own identity, transcribed before its note went with it.** The two
md5s, the `Main.hs` commit and the tree at launch are at this file's own head
and are not repeated here --- one live copy, since both places are replaced
by the same run. What this paragraph adds is what that head does not carry:
`-fspec-constr` and `-fobject-determinism` on both halves, `align-as.py`
as committed at `40f7a37`, and `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1` on both
builds, the two differing only in `--project-file=cabal.project.ghead` and
so in the compiler. **Both halves were built by hand**, this being a pair of two
shims, so both recipes went into the pair note. **And the control half's
compiler is not a released one**, which is this pair's own provenance hazard
and is why the version is read back out of each binary rather than off a recipe
line: the in-tree stage1 of the GHC checkout under `~/r/horde-ad/ghc` at commit
`d415f38a75`, reporting 10.1.20260803. A HEAD that moves is a different compiler
and a different pair. **No input moved that a freeze does not record**: the box
is where Run 18 left it, its machine check reading -0.84%, so absolutes cross
freely from Run 18 and the boundary that stops them is still the BIOS change
before it.

**Nothing moved in the shapes or the roster**, which is what a compiler pair
needs and what its own registration required: 1128 benches, the same 47 timed
arms over the same 24 shapes, every class at three shapes, and the same roster
order, with both halves' `--list` listings identical to each other
and to `run18-g912`'s, compared directly off the previous basis binary while
it was still on disk. So no `-L1` roster pass was owed and none was run.
**The one input that moved by design is the compiler**, which adds no bench
and so leaves membership untouched while moving every address.

**The anchor, so a moved baseline is visible** --- and this is the run where
it stayed still. Every published figure is a ratio to `list`, so a change
in `list` alone would move every cell without any strategy moving. The three
anchors read **6.08 us** on `cnn-slice-c32`, **3.10 ms** on `cifar-L2-16-c64-k3`
and **38.3 ms** on `stretch-wide-2xM`, net per call on the basis half, against
Run 18's 6.10 us, 3.13 ms and 38.4 ms --- **-0.31%, -0.93% and -0.22%**, every
one of them well inside this run's floor and inside the drift band besides.
That is the same binary reading the same box a day later, and the gate's machine
check said so before the evening was spent, at -0.42% over all 24 shapes.
**The control half's three are 5.93 us, 3.06 ms and 37.5 ms**, 2.39%, 1.26%
and 2.15% under the basis's --- so unlike Run 18's pair the compiler IS
in this movement, which is the same fact as `list` moving 0.78% between
the halves and is why these two columns are ordered rather than differenced.

| shape | `l` | `list`, per call | net | HEAD, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.25 us | 6.08 us | 5.93 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.19 ms | 3.10 ms | 3.06 ms |
| `stretch-wide-2xM` | 1800000 | 39.4 ms | 38.3 ms | 37.5 ms |

**Each stride class carries an anchor of its own, beside its table,
and this time every one of the eight is inside its floor** --- which is what
a box holding still looks like from the class end, and is the reading Run 18
could not get because a busy window sat in the middle of it. Against Run 18's
basis they run **-2.48% to +0.95%**, six down and two up, the extremes being
`bcast` at -2.48% and `reshape1` at +0.95% and the other six inside a point
and a third. Every one of those is inside its own class's floor, the tightest
of which is `revsome`'s 2.00%. **So a class anchor is comparable across
this boundary in both directions**, which no run since the BIOS change has
been able to say, and the eight of them agree with the main set's three about
the box rather than adding anything to them. What they cannot be compared across
is still the Run 17 boundary, where the BIOS sits.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is **0.601--0.615 ns per element** on the basis half
and 0.597--0.615 on the control, across the whole set, so a raw slope
is the published one plus about `0.61e-9 * l`, with `l` from `Main.hs`.
That recovers any uncorrected figure to within the term's own spread --- enough
to hold a corrected run against any number measured before the correction
existed. The term is within about 2% of every run's since Run 7, so neither
the flag, the roster, the layout, the shim's padding, `-fproc-alignment=64`,
an RTS line, a source patch that moves every loop offset, **nor a change
of compiler** touches the forcing pass, which is the control saying every run's
correction is one correction --- and this pair's two halves agree on
it to within a thousandth of a nanosecond, so a figure differenced across
these halves carries almost none of its own.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance
