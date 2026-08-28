# Run 20 (SpecConstr)

One run's write-up: its head, its Results, what the next run compares against,
the claims that run should test, the eight class blocks, and its own Provenance.
A run replaces this file whole and edits [README.md](../README.md) around it,
in the score of places [the replace list under Provenance there][prov] names ---
the open list among them, which is where a run's registrations, verdicts
and surprises go rather than here. So this file is most of what a run replaces
and by no means all of it. What stands between runs is the harness, [the
procedure][procedure] that makes a file like this one, and the rulings
a measurement does not reach.

**Run 20 (SpecConstr), and what the arms written since Run 19 are worth.**
Criterion, **`--ghc-options=-fspec-constr`**; Run 19's regime, main-set shapes
and roster order, and **what moved is the roster and the class views**: 1272
benches, 53 timed arms over 24 main-set shapes, with `reshape1` and `bcastmid`
at four shapes each and the other six classes at three, where Run 19 ran 47 arms
and 1128 benches over 24 and 24. **The basis is the 9.12 half**, `run20-g912`:
Run 19's basis recipe with only the source moved, so it carries
`-fobject-determinism`, the per-sample instrument and the saturating preamble,
and both halves ran under `WILDLOG=1 SATURATE=1`. **The control
is `run20-ghead`**, the same source and the same shim built by the in-tree
stage1 of the GHC checkout at 10.1.20260803 through `cabal.project.ghead`, whose
freeze resolves the same `vector`, `criterion` and `criterion-measurement`
at the one index-state the other two plans hold --- so the halves differ
in the compiler and its boot libraries and in nothing a freeze can see, and what
they price is a consumer's build on GHC HEAD, library code recompiled included.
The binaries carry `ghc-internal-9.1204.0` against `ghc-internal-10.100.0`,
criterion 1.6.5.0 on both, and `.text` of 20451525 against 20596543 bytes. md5
`3392bdba85bc1931bde4233d7b6d3ffc` for the basis
and `930f910435c53c81a6d74bbd23b66a2d` for the control, from `Main.hs`
at `ba79b3c` and `align-as.py` at `40f7a37`; the tree at launch was `1fb2367`,
with three untracked scratch paths and nothing modified. The same desktop, Zen
3, a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main
processes read *1h49m43s* and *1h50m10s*, at *291 MiB* in use and *127 MiB* max
residency on the basis against *282 MiB* and *122 MiB* on the control.

**The basis half is not a repetition, and this run gave up that instrument
on purpose.** Nine timed arms landed since Run 19 was built and three dropped
to `Only`, so every address moved and neither half can reproduce its Run 19
counterpart byte for byte; the md5 comparison and the three-read hunt a moved
md5 usually triggers were both taken off for this run, decided 2026-08-25,
so a differing md5 here is what the roster change predicts and not a finding.
**What holds the build to something instead is three readings that survive
a relink.** The gate's machine check reads **-0.24%** on `list`'s net against
Run 19's kept fingerprint over 24 of 24 shapes, worst `stretch-pow2stride`
+3.07% and none past 5%. The 44 arms both halves and Run 19 all time read
against Run 19's columns, with the caveat the roster change puts on them:
a layout term nothing here separates, which Run 10 priced at 12 to 14%
on the two arms whose loop the shim rescues. And each half's own eighteen A/A
pairs give it a floor. **The pinning claim was read at the build and KILLED**,
which is registration 2 and belongs there rather than here: not one tracked loop
stayed where `run19-g912` held it, the four-copy group at `[0, 24, 0, 4]` having
become a six-copy group at `[0, 0, 24, 0, 0, 24]` with every address moved
and none by a constant, on two builds one roster change apart whose package ABI
strings are identical as sets.

**Every registered ordering holds on GHC HEAD, and this is the second run to say
so on this pair.** All **eight** of the manifest's orderings --- claims 1, 2
and 6, read off `--claims` rather than off the sentence that registered them ---
hold on 10.1.20260803, and all eight hold on 9.12.4: no BROKE on either half.
That is the first reading of the eight the settlement of 2026-08-24 left,
the thirteen having been held through Run 19 for their last cross-compiler
reading and retired at its write-up. **Allocation is where the pair parts,
as it did on Run 19 and to the same cell**: **1143 of the 1224** main-set cells
that allocate in earnest match to 1e-4, and the worst disagreement is **1.13e-02
on `cnn-slice-c32/bq-expand-qr-prim`**, which is the arm and the shape Run 19
named. Allocation is deterministic per call, so those eighty-odd cells
are a code change and never a slot. What did not move is the tiers --- claim 7's
levels return per compiler, and the class blocks read them unbroken in all eight
populations. **And the two columns of this pair may NOT be differenced,
by a hair**: `list`, the denominator of every ratio here, reads **1.0071** basis
over control across the main set, where the bar that separates a subtractable
pair from one that can only be ordered is 0.7%. Run 19 read 1.0078 and failed
the same bar less narrowly. Two routes agree on this run's figure ---
the reader's paired reading and a geomean taken over the `list` cells directly
--- so what is marginal is the threshold and not the measurement,
and the conservative reading is the one taken: these columns are ordered
and not subtracted.

**What the compiler is worth, arm by arm, is what Run 19 read and it is still
one-sided.** Over the 47 arms compared, 22 sit within 1% of 1 at a geomean
of **0.9844**, 30 below and 17 above --- where Run 19's pair read 0.9836 at 30
below and 12 above over 42 arms. So HEAD is about a point and a half behind 9.12
across this roster, in one direction, and a run that changed nine arms
of the roster did not change that. **Eight arms move past 3% and every one
of them is the same way, the basis faster.** The new leaf arm
`mut-odo-vecdims-add-in-leaf` heads them at **0.8513**, alone and further out
than anything Run 19 saw; then the two fastest pure builds with their A/A twins,
`bq-odo-gm-mulback` at 0.9257, 0.9247 and 0.9254 and `bq-scan-rem-gm-mulback`
at 0.9395, 0.9391 and 0.9410; and `canon-vecdims`, one of the rework's arms,
at 0.9529. Nothing reaches 3% in HEAD's favour, the largest being
`offtab-aa-adjacent` at 1.0237. **A whole family moving with its own A/A twins
is the shape to read**: a twin is that arm's code at another slot, so three
copies moving together is the arm and not where one of them landed --- and both
`-gm-mulback` families read within two thousandths of their twins, as they did
on Run 19. What the counted-work column then does with these is the paragraph
below; it splits them cleanly.

**This run's floor is 1.51% on the basis half and 1.18% on the control**,
against Run 19's 2.32% and 1.71% over the same eighteen A/A pairs, so both ends
tightened while staying well inside Run 17's 3.70% and 3.89%. The pairs carrying
it are `gen-unsafe-aa-distant` on the basis and `offtab-aa-adjacent`
on the control, and the worst A/A cell of either main set is **13.66%**
on `alexnet-L2-27-c48-k5` on the basis against **16.22%** on `stretch-rank12`
on the control, where Run 19 read 18.50% and 17.66%. Restricted to the six pairs
that carry back to Run 10 the two read **0.44%** and **0.28%**, against Run 19's
0.49% and 0.29% --- so the tight six are where they have been and the movement
is in the twelve outside them, the same place Run 19's loosening lived. Fifteen
of the eighteen basis intervals cover 1 and seventeen of the control's. **Which
of the two a margin is judged against depends on what it compares**: an arm
against its own duplicate against these, 1.51% and 1.18%; two different arms
against the six-pair figures above, 0.44% and 0.28%. Neither is judged against
the predecessor's, for the reason [the floor section][floor] holds and this file
does not restate --- what Run 20 adds to it is one more reading, the same recipe
on the same box one roster change later moving from 2.32% to 1.51%.

**The two halves' cells resolve differently again, and this run the lean runs
the other way.** `CI%` --- the median half-width of a cell's own fit --- runs
a geomean of **0.97** on the basis against the control across the roster, 21
arms wider here and 32 narrower, where Run 19 read 1.06 at 26 wider and 21
narrower. So the half whose cells resolved worse on Run 19 resolves better here,
on one box and one pair of compilers, with the roster the only input that moved
between the two runs. **What that breaks is a coincidence, not a rule.**
The basis carries the wider floor in both runs --- 1.51% against the control's
1.18% here, 2.32% against 1.71% there --- so on Run 19 the basis was the looser
half on both columns at once and the two looked like one fact. Here they part:
the basis is the looser half on placements and the tighter half on cells.
Sampling error inside one bench and agreement between two placements of one
strategy are different quantities measured by different columns, which is what
this file has said all along; Run 19 could have been read as evidence they
track, and this run says they do not.

**No wild cell this run, and the standing free draw came up clean a third
time.** The worst A/A cell of any population is **19.19%**, on `reshape1-r3`
in the control half's `reshape1` process, against Run 19's 19.75%, Run 18's
23.03%, Run 17's 74.48% and Run 16's 43.43%; the worst on the basis side
is 13.66% on `alexnet-L2-27-c48-k5` in the main set. So the run's worst cell
is a shade tighter than its predecessor's and nothing in it approaches the class
the two runs before those produced. **The class floors moved and they did
not move together**: on the basis half the widest is `reshape1`'s **8.31%**
and the tightest `scaled`'s **3.01%**, where Run 19 read 8.11% and 2.00%.
The tightest is a different class from Run 19's, and the class that lost
the title is the one worth naming --- `revsome`, which Run 17 found loose
at an 18.05% floor and Run 19 read at 2.00% as its half's tightest, reads
**6.14%** here, third widest of this half's eight. Its Run 17 looseness has
still failed to repeat three runs running, so what that reading retired stays
retired; what this run adds is that its 2.00% did not repeat either, which
is the floor being a property of the run said once more at class scale.

**Two populations were rerun, and this run says plainly why rather than carrying
the exposure.** The sequence ran unattended from 02:56:06 to 10:35:11
and its last four processes met the machine's owner coming back to it: `window`
and `scaled`, on both halves, reported 71, 54, 134 and 131 benches at or above
0.25 foreign CPU, with a worst sample of 1861 ms. The per-sample instrument
is what names that an INTRUSION rather than a wild cell --- a wild cell moves
the mutator clock with the machine quiet beside it, and here the machine
was not --- and the plateau gate saw the same event from the other end, though
not as simply as four high readings: THREE of the four read their preamble
victim at 21.0, 21.4 and 21.5 ms against a 19.8 to 20.6 band for the fourteen
clean ones, while the fourth, `ghead-window`, read **19.74** --- the LOWEST
of all eighteen, because the intrusion began after its preamble had run. The two
ends of the 8.72% spread the gate reported were therefore both exposed
processes, which is why the gate reports the spread and every process's reading,
and leaves the naming to a person. **The other fourteen processes are clean**,
each reporting no bench reaching 0.25 foreign, and both main sets are among
them, so the Results table, the claims, the fingerprint and the yardstick never
sat under it. **Post-run step 1c was paid rather than priced away.** Run 19
declined its rerun on one exposed bench in 1128 that its own A/A twins bounded
at under 0.09%; this is 390 benches across two whole populations and no such
bound exists, so the four processes were rerun on a quiet box, both halves
of each because a pair read across two windows is not a pair. The reruns ran
11:47:46 to 12:42:56, each exiting 0 at 159 benches with its `@@saturate` stamp,
and each reports no bench reaching 0.25 foreign. **The populations therefore ran
in more than one window and this file states it**, which is what one process per
population makes harmless: each carries its own controls, its own floor
and its own gates. The four superseded processes are excluded from the published
set, so nothing downstream reads them as the run's own, and the plateau
over the eighteen processes now stands at **4.26%**, inside the band.

**The counted-work instrument cuts this pair's movements in two,
and it reproduces Run 19's split to four figures.** `run-counts.sh` counts
instructions an iteration from two fixed-`-n` processes a cell and owes
criterion nothing; `--counts` reads a pair of those files beside `--compare`.
**What is codegen**: the fast pure tier's whole loss, again. `bq-odo-gm-mulback`
reads a count ratio of **0.9340** against its time ratio of 0.9257
and `bq-scan-rem-gm-mulback` **0.9423** against 0.9395, leaving time-over-counts
at 0.9912 and 0.9971 --- where Run 19 read 0.9340 and 0.9422 on the counts,
the first reproducing to four figures and the second to three. HEAD simply emits
about 7% and 6% more instructions for these two, on two runs a roster change
apart. **What is not codegen**: the placement-exposed family, at count ratios
of **1.0000** to four figures on every one of `mut-odo`, `build`, `offtab`,
`gen-unsafe`, `gen-quotrem` and `bq-mut`, exactly as Run 18 and Run 19 found
them --- so their time movements, 0.25% on `gen-quotrem` to 1.75% on `mut-odo`,
are layout or the runtime and not code. **And the new arm is both at once.**
`mut-odo-vecdims-add-in-leaf`, this run's largest movement at 0.8513 in time,
reads **0.8971** on the counts, leaving time-over-counts at **0.9490**: about
ten points of its fifteen are HEAD emitting more instructions and the remaining
five are not, which no clock in this README could have separated.
`canon-vecdims` is the mirror image, moving 4.7% in time at a count ratio
of **0.9997** --- a rework arm whose whole cross-half movement is placement
or runtime.

**The counted work covers every population, as it has since 2026-08-25,
and the class picture changed shape.** Sixteen sweeps, both halves over all
eight classes, 159 or 212 cells apiece and no cell perf refused. **Seven
of the eight read as the main set does** --- every arm together at a count
geomean of 0.9860 to 0.9918, HEAD emitting about a percent more --- while
**the eighth sits apart at 0.9995**, near enough to 1 that HEAD and 9.12 emit
the same instructions across that whole class. That eighth is `reshape1`. Run 19
read it at 1.0032 against 0.9892 to 0.9953 elsewhere and called it an inversion;
here it is not inverted, only flat, so what survives of that reading
is that `reshape1` is the class HEAD does not cost, and the sign of the residue
did not repeat. `window` is again the runner-up at 0.9918, as Run 19 found
it splitting inside itself. **The most extreme arm is the same one in all eight
classes and it is new**: `mut-odo-vecdims-add-in-leaf`, from 0.8694 on `bcast`
to 0.9286 on `reshape1`, where on Run 19 that slot belonged
to `bq-odo-gm-mulback` in six of the eight.

**The unit-innermost-extent rule was registered as a mechanism claim
and this run could have killed it; it held, on a shape that did not exist when
it was made.** Wherever `sInner` is 1, `bq-odo-gm-mulback`'s HEAD penalty
is absent: `stretch-inner1` reads **1.0000** on the counts, `reshape1`'s four
shapes 1.0169, 1.0032, 1.0023 and 1.0000, and `window-64x64-k1x9` 1.0099.
Everywhere else it runs **0.9149 to 0.9701**, and the far end of
that is `stretch-rank12` at `sInner` 2, the one shape between absent
and the band, which is what a graded effect looks like rather than a switched
one. **The new shape is the test the registration asked for.**
`reshape1-strided-r3` landed with this roster, is `sInner` 1, and is strided
where the class's others leave a contiguous run --- so it separates the unit
extent from the contiguity that came with it in every earlier instance. It reads
1.0023: no penalty. Run 19's kill condition was any `sInner` of 1 that shows
the penalty, and six shapes now decline to. What this still is not is a reading
of the code, so the claim stays registered rather than settled.

**And the correction sits on nearly the same footing in both halves, as it did
on Runs 17, 18 and 19.** The in-situ forcing term --- an arm minus its `-nosum`
twin, against the `sum-only` the correction actually subtracts --- reads 1.0266,
1.0341 and 1.0701 as medians on the basis and 1.0298, 1.0214 and 1.0655
on the control, on `mut-odo-vecdims`, `mut-flat-gm` and `bq-expand`. So both
halves subtract a term between about 2% and 7% under the in-situ pass, tilting
the same way on all three arms and agreeing with each other to within 0.32, 1.27
and 0.46 of a point, and **a margin between these two halves is therefore
not carrying a correction bias**. The fourth control the rework brought,
`canon-full-nosum`, reads 1.0267 and 1.0239 --- so the endpoint arm, whose write
pattern varies by shape where the three standing controls are element-wise
fills, sits with them rather than apart, which is what it was added to find out.
The two `sum-only` halves agree at 1.0004 on the basis and 1.0002
on the control. Every one of those figures is within a few thousandths of Run
19's on the three arms it shares.

**The add-in split did not repeat, and this run is the first that could have
read it against a floor this tight.** `mut-odo-vecdims-add-in` against the arm
it varies reads **0.9945 at 18 of 24, sign p 0.023** on the 9.12 half
and **0.9913 at 16 of 24, p 0.15** on HEAD --- both below 1, and both margins,
0.55% and 0.87%, CLEARING the six-pair figures of 0.44% and 0.28% that two
different rows of one table must clear. **The eighteen-pair floor is the wrong
quantity here and this file used it at first**: 1.51% and 1.18% govern an arm
against its own duplicate, and against those the same margins read
as no separation at all --- which is the reading a comprehension probe caught,
the rule sitting in Results and its application here. **What the two instruments
then say is not the same thing, and both are reported.** By the margin, the arm
separates from its base on both compilers and in the same direction. By the sign
test it separates on the basis (18 of 24, p 0.023) and does not on HEAD (16
of 24, p 0.15). Run 19 read 0.9755 outside its floor on the basis and 0.9991
at a coin flip on HEAD and called that a split by compiler; this run has
the direction agreeing across the compilers where Run 19 had it absent on one,
and the significance still splitting. The question was **parked on 2026-08-25**
in any case, the margin being too small to move the shipping choice whichever
way it came out, and the three arms it turned on stopped costing benches
the same day. This reading is recorded because the pair was still rostered
to give it, not because the question reopened. **What replaced it as the run's
own placement question is `build` against `mut-odo`**, one worker at two slots:
**0.9899 at 13 of 24, sign p 0.84** on the basis and **0.9668 at 18 of 24, p
0.023** on HEAD. Run 19 read this pair at 0.9633 and 0.9325, both halves well
below 1 and both significant; here the basis's margin has fallen to 1.01%
and HEAD's to 3.32% --- both past the six-pair figures of 0.44% and 0.28%
that two rows of one table must clear, while the basis's sign test is a coin
flip at 13 of 24, p 0.84, and HEAD's is 18 of 24 at p 0.023. So the pair
that agreed across the compilers on Run 19 disagrees now, and it is the 9.12
half that moved. Their per-shape ranges remain the finding rather than their
geomeans, **0.884..1.053** on the basis and **0.841..1.116** on the control,
so on HEAD the two slots still disagree by more than a quarter on a single
shape. The roster change moved every address between these runs and this pair
is the one designed to feel that, which is what stops the movement being read
as anything about the two workers.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512`
on the basis, and 2408978 against 2408530 on the control, where plain -O1
separates the two tenfold. The two compilers put the scan arm's own allocation
48 bytes apart and the mutable arm's at the same byte.
On the confirm-don't-rebuild path this run took, with no build to have carried
the flag, that is the only check standing between a mistyped regime
and the hours.

**Run 20 records every population twice** --- the main set and all eight stride
classes from each half, one process each, which is what makes its class readings
a pair rather than a basis alone --- and **its eighteen published processes come
from two windows rather than one**. Eighteen ran unbroken from 02:56:06
to 10:35:11 --- 1272 twice, 212 four times for the two four-shape classes,
and 159 twelve times --- and the four the intrusion touched were rerun 11:47:46
to 12:42:56, so what stands is fourteen processes from the first window and four
from the second. Every one exited 0 at the bench count its roster holds.
No process reported a selection it did not ask for. The sixteen class processes
span 13m45s to 18m27s, the four-shape classes accounting for the top
of that range. **The control half ran first throughout**, `ghead` before `g912`
on the main set and on each class in turn, which is the driver's order and which
the reruns kept --- so *the 9.12 half* and *the second process of the two* again
name the same nine processes, and this run took no order probe to separate them,
as Run 19 took none. **The alone-leg riders followed the sequence** rather
than sitting inside it, 108 single-bench processes over four invocations of 27
--- the 24 shapes plus a second reading of the three anchors, each half clean
and saturated, which is the pair of columns the decomposition needs. Each rider
invocation recorded the machine it launched on, 0.2% to 0.4% of the CPUs
non-idle, a guard that did not exist when the sequence started.

**The decomposition reproduces on both halves, and the roster's own share came
in smaller than Run 19's on one half and larger on the other.** The riders time
each shape's `list` by itself, one bench per process on that half's own binary,
`SAT=` off and on, and the saturated legs split the deflation into the state
the preamble puts on a clean process --- **+12.27%** on the basis
and **+13.27%** on the control --- and the rest the roster adds on top of it,
**+0.66%** and **+0.29%**, both geomeans inside their halves' floors. Run 19
read +11.73% and +12.57% for the state and +0.31% and +0.72% for the rest,
so the state term has now reproduced across two runs and a roster change while
the roster's own contribution stays under a point on every half either run
measured. **The two tails are the same shape on both halves and it is the shape
Run 19 named**, `stretch-tall-Mx2` at 1.0999 and 1.1301 against its 1.0838
and 1.0998 --- which makes it a roster effect on one shape rather than a term
belonging to either compiler, now on two rosters. Both readings are raw slope
against raw slope, an alone leg carrying no `sum-only` bench to correct with,
so no correction convention enters either.

**Everything in this file is replaced by the next run, which is what makes
it a file.** What a run replaces OUTSIDE it, in README.md and in the sources,
is [README's own Provenance](../README.md#provenance). None of it is portable:
a run on another machine is a different measurement rather than a repetition,
which Run 19 was in a position to be firm about, having repeated one binary
on one box and moved its floor by 1.7x. This run cannot repeat
that demonstration and does not try --- its roster moved, so neither half
reproduces a predecessor byte for byte --- and it makes the weaker half
of the same point instead: the floor fell from 2.32% to 1.51% on one recipe, one
box and one regime, with only the roster between them.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries
that decision and this run's re-pass of its gates), the scratch vectors
are the unboxed ones the shipped code uses, as they have been since Run 7 ([the
scratch vector flavour](../README.md#the-scratch-vector-flavour) says what
that severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under. **A row's distance from Run 19's basis
column is NOT drift alone, and this is the first run since Run 16 that has
to say so.** Nine timed arms landed and three left, so every address moved
between the two builds; the flag, the shapes, the order, the allocation area,
the box and the recipe are all the same ones, but the layout is not, and Run 10
priced a reorder at 12 to 14% on the two arms whose loop the shim rescues.
So read a distance from Run 19's column as drift PLUS a layout term this run
cannot separate, and prefer the within-run comparisons for anything that has
to be decided. This pair's halves differ in the compiler, so they differ
in layout by construction too; there the counted-work instrument does separate
them, and the table's cross-half distances are read as codegen where the counts
moved and as placement or runtime where they did not.

**And it is the basis half's**, `run20-g912`, as every published table here
is from Run 11 on: the control half's column is one column on the yardstick
below rather than a second copy of these forty-odd rows. That the published half
is the 9.12 one is this pair's own decision --- it keeps the lineage, being Run
19's basis recipe with only the source moved --- and the HEAD half
is the yardstick column. **Nine rows here are first readings**, which no run
since Run 16 has had to say: the three leaf arms, the rework's five
and the fourth forcing control. A first reading has no predecessor to be drift
against, so nothing in this file compares one to an earlier column,
and the registrations they answer are [in the open
list](../README.md#what-is-open).

**Comparing runs?** The table below is Run 20's own; what to hold a new run
against is [What the next run compares
against](#what-the-next-run-compares-against), the claims to test are [the ones
after it](#the-claims-the-next-run-should-test), the absolute anchor
is under [Provenance](#provenance) below and the population it was measured
over in [README's delta chain](../README.md#provenance), and this run's own
floor --- no A/A pair further than 1.51% from 1 on the basis half or 1.18%
on the control, on worst single cells of 13.66% and 16.22%, and 0.44% and 0.28%
read on the six pairs that carry across runs --- is [in the floor
section][floor]. The eighteen-pair figure governs an arm against *itself*; what
two different rows of the table below must clear is the SIX-pair one, 0.44%
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
| *bq-expand-nosum* | *--* | *--* | *0.57* | *79* | *2.35x* | *its base arm, forced with one element* |
| *canon-full-nosum* | *--* | *--* | *0.60* | *102* | *1.00x* | *the same, on a write pattern that varies by shape* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.67* | *92* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.49* | *92* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *101* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *101* | *0.00x* | *the same, at the other end* |
| mut-odo-vecdims-add-in-leaf-down | 0.035 | 0.118 | 0.63 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf | 0.036 | 0.118 | 0.57 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf-u2 | 0.038 | 0.125 | 0.56 | 88 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| canon-vecdims | 0.049 | 0.122 | 0.68 | 94 | 1.00x | new mutating `Vector` method |
| canon-memcpy-r2 | 0.052 | 0.122 | 0.66 | 94 | 1.00x | new mutating `Vector` method |
| canon-full | 0.053 | 0.122 | 0.64 | 94 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.054 | 0.122 | 0.64 | 80 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa* | *0.054* | *0.122* | *0.55* | *80* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.054** | 0.122 | 0.57 | 80 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.123* | *0.40* | *80* | *1.00x* | *A/A control* |
| mid-copy | 0.055 | 0.122 | 0.68 | 80 | 1.00x | new mutating `Vector` method |
| bcast-set | 0.057 | 0.122 | 0.63 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.083 | 0.186 | 0.61 | 82 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.090 | 0.191 | 0.64 | 80 | 1.33x | mutable `Int` scratch |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.097* | *0.154* | *0.51* | *74* | *1.33x* | *A/A control* |
| **bq-scan-rem-gm-mulback** | **0.098** | 0.154 | 0.53 | 74 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.155* | *0.29* | *74* | *1.33x* | *A/A control* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.099* | *0.179* | *0.45* | *79* | *1.51x* | *A/A control* |
| bq-odo-gm-mulback | 0.099 | 0.179 | 0.40 | 79 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-distant* | *0.099* | *0.179* | *0.51* | *79* | *1.51x* | *A/A control* |
| bq-mut-runs | 0.100 | 0.189 | 0.73 | 75 | 1.33x | mutable `Int` scratch |
| *build-aa-adjacent* | *0.100* | *0.255* | *1.49* | *71* | *1.00x* | *A/A control* |
| *build-aa-distant* | *0.100* | *0.260* | *1.80* | *70* | *1.00x* | *A/A control* |
| build | 0.101 | 0.257 | 1.61 | 70 | 1.00x | new mutating `Vector` method |
| *mut-odo-aa-distant* | *0.101* | *0.254* | *0.83* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-adjacent* | *0.101* | *0.248* | *0.72* | *71* | *1.00x* | *A/A control* |
| bq-expand-gm-mulback | 0.103 | 0.227 | 0.67 | 79 | 2.35x | nothing (pure) |
| mut-odo | 0.103 | 0.248 | 1.01 | 71 | 1.00x | new mutating `Vector` method |
| bq-expand-b | 0.113 | 0.233 | 0.55 | 74 | 2.18x | nothing (pure) |
| bq-expand-qr-prim | 0.113 | 0.233 | 0.58 | 74 | 2.35x | nothing (pure) |
| *bq-expand-aa-adjacent* | *0.114* | *0.233* | *0.54* | *74* | *2.35x* | *A/A control* |
| bq-expand | 0.114 | 0.233 | 0.59 | 74 | 2.35x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.115* | *0.230* | *0.39* | *74* | *2.35x* | *A/A control* |
| bq-expand-zf | 0.117 | 0.252 | 0.55 | 73 | 2.35x | nothing (pure) |
| offtab-scan-rem | 0.132 | 0.216 | 0.82 | 72 | 2.00x | nothing (pure) |
| offtab | 0.135 | 0.287 | 1.14 | 66 | 2.00x | mutable `Int` scratch |
| *offtab-aa-distant* | *0.136* | *0.305* | *0.92* | *66* | *2.00x* | *A/A control* |
| *offtab-aa-adjacent* | *0.136* | *0.305* | *1.10* | *66* | *2.00x* | *A/A control* |
| bq-mut | 0.148 | 0.273 | 1.04 | 64 | 1.33x | mutable `Int` scratch |
| bq-gen | 0.339 | 1.801 | 1.42 | 51 | 1.33x | nothing (pure) |
| *list-aa-distant* | *0.996* | *1.014* | *0.49* | *35* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.47 | 35 | 23.50x | -- |
| *list-aa-adjacent* | *1.002* | *1.026* | *0.32* | *35* | *23.50x* | *A/A control* |
| *gen-unsafe-aa-distant* | *1.153* | *3.040* | *1.38* | *39* | *1.00x* | *A/A control* |
| *gen-unsafe-aa-adjacent* | *1.157* | *3.264* | *1.47* | *38* | *1.00x* | *A/A control* |
| gen-quotrem | 1.159 | 3.173 | 1.54 | 38 | 1.00x | 1st attempt |
| gen-unsafe | 1.170 | 3.196 | 1.26 | 38 | 1.00x | -- |

`concat-runs` has no row, and neither do the other 28 arms the roster holds
and checks without timing --- 29 of its 82 in all: the reason is at each entry
and the count is [`--lint`'s](../README.md#the-reader-read-runpy). So a movement
below is a movement only on the 44 arms this run shares with Run 19; the nine
first readings are named in the section's own opening.

**Three things in the table are the run's findings rather than its numbers.**
**The head of the table changed hands, and the fix is now eighth on it.**
`mut-odo-vecdims`, the arm decided 2026-08-22, reads 0.054 with six arms clear
of it and a seventh level with it: the three leaf arms at 0.035, 0.036
and 0.038, the rework's `canon-vecdims`, `canon-memcpy-r2` and `canon-full`
at 0.049, 0.052 and 0.053, and `mut-odo-vecdims-add-in` at 0.054, which
is the level one --- it sorts ahead but reads 0.9945 paired, inside this half's
floor, so it is not separated from the fix at all. Every one of the seven needs
exactly what the fix needs --- a mutating `Vector` method and nothing more ---
so what the table shows is not a new tier but a better member of the tier
that already shipped. Four are `mut-odo-vecdims` variants and three
are the rework's canonicalizing arms, which this file counts OUTSIDE the vecdims
family wherever it says *best outside family*; the shared thing is the `needs`
column, not the family. **The ceiling reproduced on the arm the class property
names**: `mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm
needing nothing at all, reads **0.5479 at 23 wins of 24** and sign p 3e-06
on the basis, against Run 19's 0.5572, Run 18's 0.5577, Run 17's 0.5446 and Run
16's 0.5567 --- the figure [the ruling](../README.md#the-mutable-ceiling-taken)
turns on, unmoved by a roster change that moved every address. On HEAD it reads
**0.5159** at the same 23 of 24 and the same p, so the ordering
is the compiler's to keep and the ratio is not. **And the `alloc` column is Run
15's through Run 19's at every level, with nine rows added inside it**: every
new arm reads 1.00x, the mutable fills' own level, so the rework and the leaf
block buy their time without buying allocation --- which is the one column
that would have shown a different bargain.

**The leaf block's internal ordering is this run's sharpest reading,
and it bears on what ships.** `genericFillStrided` in `Data/Array/Internal.hs`
is a bang-for-bang port of `mut-odo-vecdims-add-in-leaf-u2`, and no recorded run
had read that arm until this one. Against the arm it refines it is emphatic
and it repeats across the compilers: `-u2` / `mut-odo-vecdims` reads **0.7034
at 20 of 24, sign p 0.0015** on the basis and **0.7022 at 19 of 24, p 0.0066**
on HEAD, so the shipped code is about thirty percent ahead of the code
it was refined from on both. **But it does not head its own block.**
`mut-odo-vecdims-add-in-leaf-down` reads **0.9489 of it at 17 of 24, p 0.064**
on the basis and **0.9389 at 19 of 24, p 0.0066** on HEAD --- 5.1% and 6.1%,
each outside its half's floor of 1.51% and 1.18%, and in the same direction
on both compilers. **The third member is the one that does not carry**:
`-add-in-leaf` reads 0.9598 of `-u2` on the basis and **1.1267** on HEAD, at 16
of 24 and 3 of 24 --- it is the arm with the run's largest cross-half movement,
0.8513, so it wins on 9.12 and loses by more on HEAD, and nothing here
recommends it. `-down` against `-add-in-leaf` is 0.9886 on the basis, inside
the floor, so on 9.12 alone those two cannot be separated and only
the cross-compiler reading tells them apart. **So the reading is that `-down`
beats the shipped variant on both compilers by a margin both floors clear**,
on one run, and what it would take to act on it is [under the recommended
tasks](../README.md#recommended-tasks-after-run-20), beside the registration
it splits.

**The two standing placement controls both moved toward 1 on the basis half,
and the run cannot tell that from the roster change.** `mut-odo-vecdims-add-in`
against the arm it varies reads 0.9945 on the basis and 0.9913 on HEAD, both
inside their floors, where Run 19 had 0.9755 outside its floor and 0.9991
at a coin flip; `build` against `mut-odo` reads 0.9899 on the basis, inside
the floor and a tie at sign p 0.84, against Run 19's 0.9633 at p 0.023, while
on HEAD it reads 0.9668 and still clears. Both pairs are read for placement
and every address moved between these runs, so a movement here is exactly what
this file says such a boundary carries and is not evidence about either worker.
The head of this file has the full readings and the `add-in` question is parked
in any case; what belongs under the table is that neither control contradicts
it.


## What the next run compares against

**Run 21's regime, roster, basis and PAIR are all settled --- the pair
on 2026-08-28, so nothing in this section is a stop.** The regime
is `-fspec-constr`, as every run since Run 8, and it is the regime the claims
decide in; the shipped file does not set the flag ([the
ceiling](../README.md#the-mutable-ceiling-taken)). **The roster MOVED after
this was written**, on 2026-08-28: 49 timed arms over 24 main-set shapes and 33
class views, 1176 benches and 1617, with the new `runs` class at seven shapes,
`reshape1` and `bcastmid` at four and the other six at three --- six arms in,
ten names out. The basis is `run20-g912`'s recipe --- ghc-9.12.4,
`-fobject-determinism`, the per-sample instrument and the saturating preamble,
run under `WILDLOG=1 SATURATE=1` --- which is now the same recipe four runs
running. The allocation area is fixed at `-A32m` and no pair will vary it again.
**The pair, decided 2026-08-28, is none of the three candidates below**:
it is Run 20's pair again --- the same two recipes, 9.12.4 against the same GHC
HEAD, one source and one shim --- over the extended roster and shapes, which
is what Run 20 itself was to Run 19. The three are kept for what each says
it would have bought, a later run being free to want one. A *repetition* --- one
recipe built twice, or one binary run twice --- is the one thing Run 20 could
not give and the one this file most wants: its roster change put a layout term
into every cross-run figure, so no reading here separates drift from placement,
and a repetition on an unmoved roster would restore the clean drift band Run 19
had. A *third compiler reading* buys least: the manifest's orderings --- eight
when this run read them, seven since claim 2's second link retired --- have now
held on 9.12, 9.14 and HEAD, and Run 19 already advised against another
on that ground. A *purpose-built pair* has no question left to answer
that this run raised --- the leaf-block finding below is a code question
that both halves already answered the same way, so it wants a decision about
what ships rather than another evening. **What is NOT a candidate** is a pair
varying the allocation area, closed 2026-08-21, or one varying the roster
between its halves, refused because it would break `preflight`'s `check`
comparison and both drivers' bench counts.

**This overrides a ruling recorded in this very section, and what moved
is the premise rather than the judgement.** Run 19 advised that Run 20
not be another compiler pair, HEAD and 9.14 both having been read and both
having said the same thing about the orderings. That was weighed on a Run 20
rostering nothing new. Run 20 rosters the five rework arms and the control
the fix actually ships, so a second compiler now buys a first reading
of the shipped code on a compiler its consumers will build with, rather
than a re-reading of settled orderings. Decided 2026-08-26 by whoever asked
for the run. **And the question a purpose-built pair was owed for is gone.**
That question was the `add-in` placement one, which wanted one compiler, one
source and two shims placing the two arms at swapped cache-line offsets --- Run
18 thought a compiler pair gave it for free and Run 19 showed the free route
does not carry, the `-g3` twin naming HEAD's four functions and unable to locate
them --- and it was **parked 2026-08-25** ([its own entry][open]), the margin
being too small to move the shipping choice whichever way it came out.
So the pair above is not owed to it, and the three arms it turned on stopped
costing benches the same day. **Where the roster change does land is across
runs, not across the halves.** Within the pair one thing differs and it
is the compiler; between Run 19 and either half of Run 20 the roster has moved,
so a figure read across that boundary on the 44 arms all three still time brings
a layout term with it --- Run 10 measured a reorder at 12 to 14% on the two arms
whose loop the shim rescues. **What the roster change costs**: nine new
functions move every address, so neither half of Run 20 can reproduce its Run 19
counterpart byte for byte, and **neither owes it** --- the md5 comparison
and the three-read hunt a moved md5 usually triggers are both off for this run,
decided 2026-08-25, and saying so here is what stops a session hunting
a difference the roster explains. What holds the build to something instead
is the gate's machine check, `list`'s net per shape against Run 19's kept
fingerprint; the 44 arms both halves and Run 19 all time, read against
its columns; and each half's own eighteen A/A pairs for its floor. **And one
thing to expect of the write-up**, now that the sibling is in: `reshape1`'s
other three shapes still go degenerate for the canonicalizing arms, whose cells
there measure dispatch rather than filling, so that class's geomean for them
mixes three dispatch cells with one fill cell and its paragraph has to say which
is which. `reshape1-strided-r3` is the only cell in the class that prices
the fill. **And one thing it does NOT owe**: Run 19's main-set rerun, declined
on 2026-08-25 rather than carried forward, so Run 20 inherits no backlog
from it.

**What Run 20 leaves the next run to read against, and the first item is
not a figure.** **The box did not change**, its machine check reading -0.24%
against Run 19's kept fingerprint over 24 of 24 shapes, worst
`stretch-pow2stride` +3.07% and none past 5%; so absolutes cross from Run 19
to Run 20 freely and the boundary that matters is still the BIOS change before
Run 18, which no absolute crosses. **The floor is 1.51% on the basis and 1.18%
on the control**, with the restricted six at 0.44% and 0.28%. A Run 21 margin
is judged on both and they answer different questions: the six-pair figure
is what two rows of one table must clear, the eighteen-pair one is how far
an arm differs from its own duplicate. **And it is not inherited**: Run 19's
basis read 2.32% where the same binary had read 1.36% a day earlier,
and this run reads 1.51% on the same recipe one roster change on, so a floor
is re-drawn per run and a Run 21 margin is judged against Run 21's own, never
against these. **The two columns below may NOT be differenced, though only
just**: `list` moved **0.71%** between the halves against a 0.7% bar, where Run
19 read 0.78%. What they price is a compiler, and the counted-work column says
which movements that reaches: `bq-odo-gm-mulback` and `bq-scan-rem-gm-mulback`
six to seven percent apart ON their instruction counts,
`mut-odo-vecdims-add-in-leaf` ten points of its fifteen,
and the placement-exposed arms (`build`, `offtab`, `mut-odo`, `gen-unsafe`,
`gen-quotrem`, `bq-mut`) apart at count ratios of 1.0000. So a Run 21 movement
on one of those six is layout or runtime until the counts say otherwise.
**And one boundary is new**: the roster moved between Run 19 and Run 20, so any
figure read across it carries a layout term as well as drift, which Run 10
priced at 12 to 14% on the two arms whose loop the shim rescues.

**Registered with the pair.** Run 20's six registrations, their kill conditions
and their verdicts are [in the open list](../README.md#what-is-open),
and the commands that produced them were the pair note's, transcribed
into Provenance below before that note goes with the pair. **What Run 21
inherits is five riders that are now routine and no instrument that is new.**
The alone legs, the counted-work sweeps over every population, the saturating
preamble, the per-sample load fields and `--counts` all ran to form and want
no re-deciding. **What it inherits as a debt** is nothing: the rerun post-run
step 1c asked for was paid inside this run rather than deferred, on the two
populations an intrusion touched. **What it inherits as a warning** is two
things. The floor is re-drawn per run, as above. And **a rider now refuses
a busy machine**: `run-alonelegs.sh` reads `/proc/stat` twice two seconds apart
and will not start above 5% non-idle, added 2026-08-26 after four legs
were launched onto a box whose owner had taken it back, so a rider that refuses
is doing its job and the answer is a quiet window rather than `MAXBUSY`.

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

| strategy | Run 20 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 20 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 19 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 19 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.14.1) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, instrumented) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, plain) | Run 16 (SpecConstr, max-skip +lookrts, -A32m) | Run 16 (SpecConstr, max-skip +lookrts, -A64m) | Run 15 (SpecConstr, max-skip +lookrts) | Run 15 (SpecConstr, max-skip +lookrts +A32m) | Run 14 (SpecConstr, max-skip +lookrts) | Run 14 (SpecConstr, max-skip +lookrts +A1G) | Run 13 (SpecConstr, max-skip) | Run 13 (SpecConstr, max-skip +lookrts) | Run 12 (SpecConstr, max-skip) | Run 12 (SpecConstr, max-skip +procalign) | Run 11 (SpecConstr, aligned) | Run 11 (SpecConstr, max-skip) | Run 10 (SpecConstr) | Run 10 (SpecConstr, aligned) | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | **0.054** | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.054 | 0.047 | 0.048 | 0.054 | 0.049 | 0.051 | 0.049 | 0.049 | 0.049 | 0.049 | 0.048 | 0.048 | 0.048 | 0.049 | 0.048 | 0.053 | 0.054 |
| `mut-flat-gm` | **0.083** | 0.083 | 0.083 | 0.084 | 0.084 | 0.083 | 0.084 | 0.084 | 0.087 | 0.076 | 0.081 | 0.088 | 0.081 | 0.083 | 0.082 | 0.082 | 0.081 | 0.082 | 0.081 | 0.081 | 0.083 | 0.081 | 0.080 | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.090** | 0.093 | 0.090 | 0.094 | 0.089 | 0.091 | 0.093 | 0.092 | 0.093 | 0.080 | 0.086 | 0.094 | 0.087 | 0.088 | 0.087 | 0.087 | 0.087 | 0.088 | 0.087 | 0.086 | 0.085 | 0.088 | 0.088 | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.099** | 0.108 | 0.100 | 0.109 | 0.100 | 0.100 | 0.101 | 0.100 | 0.100 | 0.087 | 0.090 | 0.100 | 0.090 | 0.095 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.098** | 0.105 | 0.098 | 0.106 | 0.096 | 0.098 | 0.099 | 0.099 | 0.096 | 0.082 | 0.091 | 0.096 | 0.091 | 0.090 | 0.091 | 0.090 | 0.090 | 0.091 | 0.089 | 0.090 | 0.090 | 0.089 | 0.090 | 0.090 | 0.119 |
| `bq-expand` | **0.114** | 0.116 | 0.115 | 0.117 | 0.115 | 0.117 | 0.117 | 0.115 | 0.114 | 0.101 | 0.102 | 0.114 | 0.102 | 0.107 | 0.103 | 0.102 | 0.102 | 0.102 | 0.103 | 0.103 | 0.102 | 0.102 | 0.105 | 0.102 | 0.127 |
| `build` | **0.101** | 0.101 | 0.103 | 0.101 | 0.103 | 0.102 | 0.105 | 0.106 | 0.109 | 0.097 | 0.102 | 0.110 | 0.103 | 0.097 | 0.099 | 0.099 | 0.098 | 0.098 | 0.096 | 0.100 | 0.110 | 0.096 | 0.114 | 0.095 | -- |
| `offtab` | **0.135** | 0.135 | 0.134 | 0.136 | 0.134 | 0.143 | 0.135 | 0.141 | 0.136 | 0.124 | 0.126 | 0.138 | 0.121 | 0.121 | 0.125 | 0.121 | 0.125 | 0.131 | 0.125 | 0.123 | 0.123 | 0.124 | 0.115 | 0.146 | -- |
| `mut-flat` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.108 | 0.097 |

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
and `bq-mut-runs-gm-mulback`, in that order of shapes led, `offtab-scan-rem`
on Run 18, and **on Run 20 three of the rework's arms**: `canon-vecdims`, best
outside the family on 17 shapes, `mid-copy` on 17 and `bcast-set` on 3 ---
and **it only ever grows**: an arm that has earned a column keeps it, and no run
drops one; the second table carries the same columns over every stride-class
shape, with its class named. **One representative per family**, besides: where
a qualifying arm is a close variant of a member and measures closely,
the leading one keeps the column, so no strategy costs two. **Run 20 is the run
that had to apply that clause, and it kept two arms out.** `canon-memcpy-r2`
and `canon-full` both qualified --- best outside the family on 4 shapes and 6
--- and both are close variants of `canon-vecdims` measuring within four
thousandths of it on the main set, 0.052 and 0.053 against 0.049.
The installer's own membership note is what settles it rather than the judgement
alone: on nearly every shape either of them leads, the arm it beats
is `canon-vecdims` or `bcast-set` at the same three decimals, which is what
*measuring this closely* means. The judgement is still the author's, which
is why `--fingerprint` names the best member on the shape a newcomer leads.
**Neither way of dropping an arm survives.** Dropping one that leads nothing
this run churns on a thousandth --- `offtab-scan-rem` holds `reshape1-rank10`
at 0.090 against 0.091 --- and gaps the record wherever the column went. Judging
it off the fingerprint this file carries is worse: that table holds the members
alone, so a leaver would be judged against the members alone where a joiner
is judged against every timed arm --- on `reshape1-rank10` the members' own
minimum was `bq-scan-rem-gm-mulback` at 0.091, while the arm that won the shape
read 0.090 and had no column to be seen in. The header therefore grows,
and the run writer narrows it by hand if it gets unwieldy: it is fifteen columns
now and the next run that adds one should ask whether it still reads.

| shape | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | mut-runs | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.94 us | 0.085 | 0.146 | 0.153 | 0.159 | 0.159 | 0.139 | 0.154 | 0.170 | 0.116 | 0.085 | 0.087 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.29 us | 0.093 | 0.182 | 0.141 | 0.189 | 0.186 | 0.174 | 0.191 | 0.161 | 0.101 | 0.103 | 0.095 |
| `stretch-rank12` | 2 | 4096 | 111 us | 0.092 | 0.186 | 0.132 | 0.257 | 0.248 | 0.189 | 0.176 | 0.169 | 0.072 | 0.109 | 0.097 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 114 us | 0.068 | 0.131 | 0.098 | 0.171 | 0.164 | 0.147 | 0.137 | 0.126 | 0.057 | 0.070 | 0.071 |
| `conv1d-24` | 3 | 5184 | 101 us | 0.056 | 0.071 | 0.098 | 0.116 | 0.125 | 0.087 | 0.077 | 0.141 | 0.057 | 0.057 | 0.060 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 369 us | 0.048 | 0.092 | 0.094 | 0.104 | 0.100 | 0.111 | 0.101 | 0.120 | 0.044 | 0.049 | 0.051 |
| `gather48-src-50` | 3 | 22500 | 436 us | 0.053 | 0.066 | 0.098 | 0.110 | 0.115 | 0.083 | 0.075 | 0.133 | 0.053 | 0.053 | 0.056 |
| `stretch-rank10` | 3 | 59049 | 1.27 ms | 0.066 | 0.108 | 0.104 | 0.158 | 0.160 | 0.126 | 0.116 | 0.137 | 0.055 | 0.071 | 0.069 |
| `stretch-coprime-r7` | 13 | 60060 | 1.03 ms | 0.035 | 0.082 | 0.092 | 0.060 | 0.058 | 0.101 | 0.093 | 0.121 | 0.033 | 0.034 | 0.037 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.09 ms | 0.057 | 0.089 | 0.098 | 0.138 | 0.148 | 0.105 | 0.095 | 0.129 | 0.056 | 0.060 | 0.060 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.5 ms | 0.057 | 0.089 | 0.098 | 0.138 | 0.133 | 0.103 | 0.097 | 0.128 | 0.056 | 0.059 | 0.061 |
| `stretch-primes` | 89 | 250357 | 4.01 ms | 0.029 | 0.075 | 0.092 | 0.031 | 0.031 | 0.091 | 0.086 | 0.131 | 0.030 | 0.029 | 0.030 |
| `stretch-inner1` | 1 | 500000 | 13 ms | 0.090 | 0.031 | 0.073 | 0.214 | 0.224 | 0.069 | 0.031 | 0.073 | 0.000 | 0.090 | 0.097 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.1 ms | 0.044 | 0.074 | 0.092 | 0.092 | 0.095 | 0.094 | 0.085 | 0.124 | 0.043 | 0.044 | 0.046 |
| `vgg-14-c512-k3` | 3 | 903168 | 18.9 ms | 0.057 | 0.088 | 0.097 | 0.139 | 0.138 | 0.104 | 0.097 | 0.131 | 0.060 | 0.059 | 0.060 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.5 ms | 0.034 | 0.070 | 0.088 | 0.058 | 0.055 | 0.090 | 0.081 | 0.130 | 0.033 | 0.035 | 0.037 |
| `stretch-inner256` | 256 | 1750784 | 33.2 ms | 0.032 | 0.068 | 0.084 | 0.033 | 0.033 | 0.109 | 0.074 | 0.116 | 0.032 | 0.032 | 0.031 |
| `stretch-pow2stride` | 64 | 1769472 | 29.2 ms | 0.122 | 0.118 | 0.143 | 0.122 | 0.123 | 0.111 | 0.130 | 0.216 | 0.122 | 0.122 | 0.122 |
| `stretch-r5-8x432` | 8 | 1769472 | 34.1 ms | 0.032 | 0.060 | 0.081 | 0.050 | 0.051 | 0.077 | 0.068 | 0.114 | 0.031 | 0.031 | 0.034 |
| `stretch-square-1341` | 1341 | 1798281 | 29.8 ms | 0.089 | 0.132 | 0.154 | 0.088 | 0.088 | 0.108 | 0.140 | 0.202 | 0.091 | 0.088 | 0.087 |
| `stretch-bigstride` | 3 | 1800000 | 49.4 ms | 0.035 | 0.044 | 0.067 | 0.073 | 0.083 | 0.057 | 0.051 | 0.093 | 0.035 | 0.035 | 0.037 |
| `stretch-tab7MB` | 2 | 1800000 | 38.2 ms | 0.063 | 0.063 | 0.100 | 0.136 | 0.149 | 0.078 | 0.068 | 0.144 | 0.062 | 0.062 | 0.067 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39.4 ms | 0.022 | 0.051 | 0.062 | 0.023 | 0.023 | 0.066 | 0.057 | 0.095 | 0.022 | 0.022 | 0.022 |
| `stretch-wide-2xM` | 2 | 1800000 | 38.2 ms | 0.061 | 0.060 | 0.098 | 0.136 | 0.132 | 0.076 | 0.069 | 0.141 | 0.060 | 0.060 | 0.065 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | mut-runs | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 877 us | 0.033 | 0.066 | 0.089 | 0.055 | 0.059 | 0.087 | 0.080 | 0.118 | 0.032 | 0.032 | 0.030 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 26.8 ms | 0.022 | 0.072 | 0.089 | 0.022 | 0.022 | 0.095 | 0.088 | 0.124 | 0.022 | 0.021 | 0.019 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 37.7 ms | 0.062 | 0.061 | 0.097 | 0.136 | 0.152 | 0.077 | 0.070 | 0.141 | 0.061 | 0.061 | 0.061 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.46 ms | 0.058 | 0.090 | 0.099 | 0.147 | 0.142 | 0.107 | 0.106 | 0.129 | 0.058 | 0.012 | 0.061 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.92 ms | 0.021 | 0.069 | 0.087 | 0.022 | 0.023 | 0.091 | 0.085 | 0.122 | 0.022 | 0.013 | 0.024 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.4 ms | 0.036 | 0.045 | 0.069 | 0.075 | 0.083 | 0.058 | 0.055 | 0.094 | 0.035 | 0.032 | 0.038 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.4 ms | 0.022 | 0.052 | 0.065 | 0.023 | 0.023 | 0.063 | 0.060 | 0.088 | 0.023 | 0.018 | 0.022 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.89 ms | 0.109 | 0.129 | 0.092 | 0.309 | 0.284 | 0.150 | 0.125 | 0.092 | 0.000 | 0.121 | 0.107 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.72 ms | 0.091 | 0.032 | 0.073 | 0.217 | 0.252 | 0.072 | 0.032 | 0.073 | 0.000 | 0.092 | 0.092 |
| `reshape1-strided-r3` | `reshape1` | 1 | 180000 | 4.72 ms | 0.095 | 0.033 | 0.075 | 0.254 | 0.240 | 0.071 | 0.033 | 0.075 | 0.016 | 0.094 | 0.094 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 12.9 ms | 0.090 | 0.029 | 0.072 | 0.233 | 0.227 | 0.070 | 0.029 | 0.072 | -- | 0.090 | 0.090 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 114 us | 0.067 | 0.130 | 0.097 | 0.166 | 0.178 | 0.143 | 0.140 | 0.123 | 0.057 | 0.074 | 0.070 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 434 us | 0.052 | 0.065 | 0.097 | 0.118 | 0.117 | 0.082 | 0.075 | 0.132 | 0.052 | 0.052 | 0.056 |
| `rev-primes` | `rev` | 89 | 250357 | 4.04 ms | 0.029 | 0.072 | 0.091 | 0.030 | 0.030 | 0.089 | 0.085 | 0.129 | 0.029 | 0.029 | 0.030 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 441 us | 0.053 | 0.067 | 0.098 | 0.110 | 0.122 | 0.081 | 0.077 | 0.131 | 0.054 | 0.053 | 0.056 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.49 ms | 0.057 | 0.087 | 0.098 | 0.138 | 0.135 | 0.108 | 0.098 | 0.128 | 0.056 | 0.060 | 0.060 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.02 ms | 0.030 | 0.080 | 0.102 | 0.031 | 0.031 | 0.089 | 0.093 | 0.131 | 0.030 | 0.030 | 0.031 |
| `scaled-r5` | `scaled` | 13 | 15015 | 251 us | 0.034 | 0.073 | 0.094 | 0.048 | 0.049 | 0.092 | 0.081 | 0.128 | 0.032 | 0.034 | 0.037 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 961 us | 0.028 | 0.071 | 0.090 | 0.032 | 0.033 | 0.091 | 0.080 | 0.125 | 0.028 | 0.027 | 0.028 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.78 ms | 0.034 | 0.071 | 0.090 | 0.034 | 0.034 | 0.091 | 0.080 | 0.134 | 0.034 | 0.034 | 0.034 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.04 ms | 0.037 | 0.082 | 0.096 | 0.061 | 0.060 | 0.100 | 0.092 | 0.127 | 0.037 | 0.037 | 0.039 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.59 ms | 0.057 | 0.088 | 0.098 | 0.134 | 0.138 | 0.104 | 0.095 | 0.131 | 0.057 | 0.058 | 0.061 |
| `slice-primes` | `slice` | 89 | 250357 | 4.01 ms | 0.030 | 0.080 | 0.103 | 0.032 | 0.032 | 0.090 | 0.093 | 0.132 | 0.030 | 0.030 | 0.031 |
| `window-28x28-k5` | `window` | 5 | 14400 | 263 us | 0.044 | 0.078 | 0.095 | 0.089 | 0.096 | 0.097 | 0.087 | 0.121 | 0.045 | 0.045 | 0.047 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 873 us | 0.095 | 0.049 | 0.074 | 0.243 | 0.261 | 0.088 | 0.047 | 0.075 | 0.020 | 0.101 | 0.103 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.27 ms | 0.057 | 0.087 | 0.096 | 0.136 | 0.142 | 0.102 | 0.097 | 0.126 | 0.058 | 0.057 | 0.060 |

**Two rows to read first, and the set is derived rather than remembered ---
it was three last run and this run it is two**: `stretch-square-1341`
and `stretch-pow2stride` are the shapes where **both** arms tying at the head
of the pure tier *lose* to `bq-expand`, so treat a disagreement on either
as the shape. `cnn-slice-c32` leaves the list, which is its own small finding:
the smallest shape in the set joined on Run 19 and did not repeat,
and the roster moved between the two runs, so nothing here separates a real
change from the layout term that boundary carries. The two that stay fail
differently, which is why each is named. On `stretch-square-1341` the mutable
fills win it back outright (`mut-odo-vecdims` 0.088 against `bq-expand`'s 0.132)
while the pure arms trail at 0.154; on `stretch-pow2stride` the two families
converge instead, the pure pair landing within a thousandth of each other
at 0.143 and 0.142 against `bq-expand`'s 0.126 ([the per-shape
section][pershape]). Taking the tier's leaders one at a time gives six shapes
and three, which is why the sentence says both. `stretch-inner1` has `sInner` 1,
so anything special-casing a unit dimension behaves differently there
by construction --- which this run's counted work makes concrete, the HEAD
penalty on `bq-odo-gm-mulback` being absent on every `sInner` of 1 it measured.


## The claims the next run should test

**Run 20's verdicts first**, since a run reports breaks rather than re-deriving
the table. **All eight registered orderings held, and they held on both
compilers** --- eight as this run read them; claim 2's second link retired
on that reading, 2026-08-26, leaving seven in the manifest --- --- no BROKE
on the 9.12 basis and none on the GHC HEAD control, a third clean sweep running.
This is the first reading of the eight that the settlement of 2026-08-24 left,
the thirteen having been held through Run 19 for a last cross-compiler reading
and retired at its write-up; claims 3, 4, 5 and 9 are gone and their numbers
are not reused, so a verdict recorded against *claim 4* in an earlier run's file
still means what it said. **What this run adds to the sweep is a roster
the manifest had not been read on.** Nine timed arms landed and three left
between Run 19 and Run 20, so every ordering was re-read on a build whose every
address had moved; none of them noticed. The arms the claims name are all still
timed, and `--pair` recovers any retired ordering in one call whenever
it is wanted.

**The four retired claims are not re-read here, and their last readings are Run
19's.** Claims 3, 4, 5 and 9 left the manifest at Run 19's write-up, on a sweep
in which all thirteen held on both of that run's halves; the numbered items
below say what each was in a clause, and Run 19's own file carries the figures
they retired on. Run 20 does not re-derive them and quotes none of them
as its own: every arm they named is still rostered and still timed, so any
of the four orderings is one `--pair` call away whenever it is wanted --- which
is the whole of what retiring them gave up.

**Claim 1 held on all five links, on both halves, and the ladder is now read
against a family that has grown under it.** The five links are what the `needs`
column draws: what a mutating `Vector` method buys (**0.6530** on the basis),
what one more mutable write pattern buys (0.9163), what a mutable `Int` scratch
buys (0.9157 against the best arm needing nothing), and, at the foot, **the two
fastest pure arms tied at 0.9977 on 12 of 24 and sign p 1** --- so
if the mutating method is refused upstream, `bq-scan-rem-gm-mulback`
and `bq-odo-gm-mulback` are indistinguishable and either is what ships. On HEAD
the same five hold at 0.6545, 0.8982, 0.8627, 0.8775 and a tie at p 0.31.
**The first link is the one this run's new arms bear on and the claim does
not see it.** Claim 1 reads `mut-odo-vecdims` against `mut-flat-gm`, and three
arms now sit ahead of `mut-odo-vecdims` inside its own family, at 0.035, 0.036
and 0.038 against its 0.054 --- so the ladder's top rung understates what
a mutating method buys by about a third, while remaining true as stated. Whether
the claim should be re-aimed at the family's leader is a question for the next
run and is [under the recommended
tasks](../README.md#recommended-tasks-after-run-20); it is not re-aimed here,
a claim being re-aimed on a decision and not on one reading.

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6530, 20 of 24, sign p 0.0015;
`mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9163, 23 of 24, sign p 3e-06;
`bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9136, 21 of 24, sign p 0.00028;
`bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9157, 17 of 24, sign p
0.064; `bq-scan-rem-gm-mulback` / `bq-odo-gm-mulback` 0.9977, 12 of 24, sign
p 1. 5 of 5 registered orderings held.

**Claim 2 held on both links and both halves, and the second link retires
on that reading.** `offtab`, which needs only a mutable `Int` scratch,
is **1.3647** behind the best arm needing nothing at all, on 6 of 24 and sign p
0.023, where Run 19 read 1.3458 and Run 18's halves 1.36 and 1.44; on HEAD
it reads 1.2753. `bq-expand`, the last candidate and what
`Data/Array/Internal.hs` carried until 2026-08-24, is **2.1134** behind the arm
that ships, on 1 of 24 and sign p 3e-06, and 2.1218 on HEAD --- the widest
and most significant ordering the manifest ever carried, and the one that priced
the branch's own code against its replacement. **That second link is RETIRED,
2026-08-26, and the reading above is its last.** It was kept only while
`Data/Array/Internal.hs` carried `bq-expand` and was to retire with the three
`TODO: retarget` markers, one decision with it; both halves were spent before
this run was written up and nobody read the condition back. The markers
were three inline `(TODO: retarget ...)` notes in README prose, added 2026-08-24
and gone once that prose was re-aimed --- never in any `.hs`, which is what made
them look like source markers nobody could find. And the file has carried
`vFillStrided` since the same day, its three vector-backed instances overriding
the default with `genericFillStrided`, so `bq-expand` survives there only
as a class default the code calls speed-irrelevant. A link pricing the branch's
code against its replacement has nothing left to price once the replacement
*is* the branch's code. Both arms stay rostered and timed,
so `--pair bq-expand mut-odo-vecdims` recovers the ordering whenever
it is wanted. **Both figures are within a few thousandths of Run 19's across
a roster change that moved every address**, which is the more useful reading
of them than either magnitude.

**Readings:** `offtab` / `bq-scan-rem-gm-mulback` 1.3647, 6 of 24, sign p 0.023.
1 of 1 registered ordering held.

**Claim 6 held, and its alarm is the reason to keep reading it.** `gen-quotrem`
/ `list` reads **1.1588** at 9 of 24 and sign p 0.31, a tie by the sign test
as registered, and on HEAD 9 of 24 at the same p. The claim's alarm is
that a break here means something moved in `list` or in GHC rather than
in a strategy, and both halves of that were under test: the control half
is a compiler two releases on, and the basis half is a build whose whole layout
moved under a roster change. It held through both, with `gen-quotrem` moving
0.25% between the halves at a count ratio of **1.0000** --- so neither GHC HEAD
nor the relink changes what this arm computes or what `list` costs relative
to it.

**Readings:** `gen-quotrem` / `list` 1.1588, 9 of 24, sign p 0.31. 1 of 1
registered ordering held.

**Claim 7 held on the levels, and the cell count says the same thing it said
on Run 19.** Every level is Run 15's through Run 19's to the digit ---
the mutable fills and `gen-quotrem` at 1.00x, `bq-mut` and the scan family
1.33x, `bq-odo-gm-mulback` 1.51x, `offtab` 2.00x, `bq-expand` 2.35x, `list`
23.50x --- and the class blocks read the tiers unbroken in all eight
populations. **Nine rows joined inside those levels and moved none of them**:
every new arm reads 1.00x, the mutable fills' own tier, so the leaf block
and the rework buy their time without buying allocation. **The cross-half
agreement is where the pair parts, as before**: **1143 of the 1224** cells
that allocate in earnest agree to 1e-4, where Run 19 read 1016 of 1080,
and the worst disagreement is **1.13e-02 on `cnn-slice-c32/bq-expand-qr-prim`**
--- the same arm on the same shape Run 19 named, to three figures. Allocation
is deterministic per call, so a cell that moves is a code change and never
a slot: the levels surviving while eighty-odd cells move is HEAD reallocating
within a tier rather than changing what any strategy fundamentally costs,
and the reproduction of the worst cell across a roster change says the effect
belongs to that arm's code.

**Claim 8's structural half stands, and the rework's arms are the first that do
not fit its sentence.** Every pure arm in the fast tier still runs its output
through the single in-order `vGenerate` over an `m`-length table, and the arms
that fall behind lose on their table build: `bq-expand-zf` and `offtab-scan-rem`
lie between the leading tier and `bq-gen`, as the claim says to expect. **What
the claim does not describe is the top of the table any more.** The seven arms
now sorting ahead of `mut-odo-vecdims` are mutable fills, not `bq-*` arms,
so the structure the claim is about governs a tier that no longer leads;
the claim is still true and its subject has shrunk. It remains the one claim
with no named invocation, read off the table by eye --- and this run repeats
what Run 19 said that costs: the counted-work column would tell the same story
from instruction counts, which is a route the claim could be given whenever
someone wants it checked rather than seen.

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

**The list needed no re-aiming, and the roster under it moved for the first time
since Run 14.** Nine timed arms landed and three dropped to `Only` between Run
19 and Run 20, where Runs 15 to 19 each ran the membership Run 14 left,
so the claims were re-read on a roster none of them had been read on ---
and every claim below still names an arm this run timed, which is what
the re-aiming of that era bought: the unconditional counterparts were written
so that dropping a precondition would not drop a question with it, and a roster
that grows underneath them does not either. **What the growth does raise
is a question the manifest cannot see**, and it is claim 1's first link: three
arms now sit ahead of `mut-odo-vecdims` inside its own family, so the ladder's
top rung understates what a mutating method buys. That is left to the next run
rather than re-aimed here.

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
2. **Retired 2026-08-28** with the parking of `offtab`, the arm its surviving
   link turned on --- the other, `bq-scan-rem-gm-mulback`, is timed still. What
   it asked, since the settlement of 2026-08-24 re-aimed it, was where the arms
   needing something other than the fix sit --- `offtab` behind
   `bq-scan-rem-gm-mulback`, a mutable `Int` scratch priced against needing
   nothing --- and its last reading is Run 20's, above. **Its second link,
   `bq-expand` behind `mut-odo-vecdims`, had gone already, 2026-08-26**
   on the reading above, its condition having been spent since 2026-08-24 ---
   what it priced was the branch's own code against its replacement,
   and the replacement is now the branch's own code. It was the widest ordering
   the manifest carried, and `--pair` recovers it, both arms staying rostered
   and timed.
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
6. **Retired 2026-08-28** with the parking of `gen-quotrem`, the arm its only
   link turned on. What it asked: `gen-quotrem` ties `list`, the first attempt's
   arithmetic ceasing to be dearer than the list's allocation once the flag
   takes its own allocation to 1.00x against the list's 23.5x --- the mixed
   picture this suite exists to have refuted, arriving by a route nobody
   proposed. Its last reading is Run 20's, above; the `cm-gather` < `list` half
   was untimed throughout and stands as Run 8's. What goes with it
   is the standing advice to check `list` as an anchor before blaming
   a strategy, which is now nobody's claim and is why the machine check reads
   `list` net per shape every run.
7. Allocation, median multiples of the result on this basis: the mutable fills
   1.00x, the scan family 1.33x, `bq-odo-gm-mulback` 1.51x, `offtab-scan-rem`
   2.00x, `bq-expand` 2.35x, `list` 23.5x --- re-listed 2026-08-28, three
   of the arms that carried these levels having gone with the parking and every
   level having kept one. Every level has reproduced since Run 15, which is what
   makes this the claim to check first when anything else moves: allocation
   is deterministic per call, so a level that *does* move is a code change
   and never a slot. **Read the levels and the cells as two questions**, which
   Run 19 is the run that separated: its levels all returned while
   the cross-half cell agreement fell to 1016 of 1080, where the 9.14 pair had
   1072 --- so a compiler can reallocate within a tier without moving any tier,
   and only the cell count sees it.
8. Every pure arm in the fast tier runs its output through the single in-order
   `vGenerate` over an `m`-length table, and a `bq-*` arm that falls behind
   loses on its table build and not on its output. Read the structure and
   not a threshold: the span is populated, `bq-expand-gm-mulback`
   and `bq-expand` lying between the leading tier and `offtab-scan-rem`,
   the slowest pure arm left. Re-aimed 2026-08-28.
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

**What the parking of 2026-08-28 did to this set**, recorded in prose because
a live item carries a predicate and no reading, and because naming a parked arm
inside one is now a `--lint` failure. Claims 2 and 6 retired with `offtab`
and `gen-quotrem`, the arms their surviving links turned on. Claim 7 lost three
of the arms that carried its levels --- `gen-quotrem` at 1.00x, `bq-mut`
at 1.33x and `offtab` at 2.00x, every figure of theirs ending at Run 20 ---
but no level with them: `offtab-scan-rem` carries the 2.00x tier, the mutable
fills the 1.00x and the scan family the 1.33x, so the list is the same six
levels it was. Claim 8 was re-aimed off `bq-expand-zf` and `bq-gen`, its span
running from the leading tier to `offtab-scan-rem` instead; the readings above
are the last that name the two. Nothing was retired on a reading here,
the parking being a decision about what is worth a bench, and the two claims
that went had no link left that a run could measure.

**Two homes, and which carries what.** Each live claim has a prose paragraph
here and a numbered predicate at the foot, and they divide: the PROSE carries
this run's figures and what moved, the ITEM carries the predicate the next run
checks and no reading at all. A RETIRED claim keeps its numbered item, which
says in a clause what it was, and gets no prose paragraph --- Run 20 wrote two
and they restated their own items clause for clause, because stripping
the figures had removed the only thing that distinguished them. Each ordering
is one line of `--claims`, whose manifest now carries the registered expectation
--- the direction of the geomean, a tie by sign test, or claim 9's two best
shapes --- and prints HELD or BROKE beside the paired geomean, interval and sign
test. `--claims --in-place` then installs that arithmetic as each claim's
`Readings:` paragraph above, so a run no longer transcribes it at all; what
stays the reading's is whether a HELD margin moved and whether a movement clears
the floor, and a BROKE is what obliges the paragraph above its reading
to be rewritten rather than requoted. **A claim with no named invocation
is a gap in this list, not a claim to be checked by hand**: where a session has
to invent the computation it will invent a wrong one, which is how claim 7 came
to be read off the raw fitted bytes, explained by a mechanism the previous pair
refutes, and then "corrected" onto a rounded print. It has `--compare --alloc`
now. Claim 8 is the one still without one, read off the table by eye.
**The general form, and it is a standing instruction rather than an observation:
if a write-up hand-rolls a script to answer something the reader should answer,
that is a defect report against the reader** --- fix it there, before
the sentence it was written for, or the next run invents its own wrong version.
**Two riders, both bought on Run 19.** A new MODE joins the guards its siblings
already have, and is checked against them rather than written beside them:
`--counts` shipped able to be given without the `--compare` it reads, silently
printing the default table and exiting 0 --- the unread-flag family exactly,
added next to four sibling readings of `--compare` that were every one of them
already guarded, and joining none. **And an instrument may be BACKED OUT, which
is not a failure of the write-up but a result of it.** Measure what it flags
before shipping it: the obvious mechanical repair for stale paragraphs was built
and returned 100 for the four that mattered, so it went, and the refutation
with its numbers is under the tasks heading --- worth more than the mode, since
it stops the next session building the same thing. A report that never empties
is one nobody reads, which this file already knows about hints.

**And for each stride class, the same three properties, now carrying Run 20's
verdicts**, the details beside each class's table:

1. **The regime 3 fix's `worst` stays under 1.** Held in every one of the nine
   populations, in every regime, roster and layout the README has run ---
   so the fix was never slower than the `list` it replaced, on any shape of any
   class the library can produce. This is the property the classes exist
   to test, no geomean can state it, and a break would be the one result here
   to bear on `Data/Array/Internal.hs` directly. Re-aimed 2026-08-22
   with the decision to ship `mut-odo-vecdims`, and read for that arm since:
   **on Run 20 its worst is 0.122 on the main set and 0.109 in a class
   (`reshape1`), both read on the basis half, with the control half at 0.121
   and 0.110** --- so the property holds for the arm decided, on both compilers,
   and neither end comes within a factor of eight of 1. Both halves are quoted
   because one is not enough: Run 18's entry here read a floor-level figure
   from whichever half happened to be lower, which is the defect this phrasing
   exists to prevent. **The margin widened this run and it is the roster's
   doing, not the arm's**: the main-set `worst` reads 0.122 where Run 19 read
   0.126, on a build whose every address moved.

2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-expand` behind it. **The first clause breaks in all nine populations
   this run, and in seven of them it breaks to a sibling.** Read as the vecdims
   family's rather than one arm's --- the ruling Run 9 left, and no run has yet
   separated them --- it holds in seven: the main set and `rev`, `revsome`,
   `bcast`, `slice`, `window` and `scaled` are each led by a `mut-odo-vecdims`
   variant from the leaf block, at margins of 6.4% (`scaled`) to 48.6%
   (`window`) against those populations' own floors, every one of them outside.
   **In two it breaks outright, to arms outside the family, and both
   are the rework's.** `bcastmid` is led by `mid-copy` at 0.017 against
   the fix's 0.031 --- **0.5490 paired, ahead on 4 of 4 shapes** ---
   and `reshape1` by `canon-memcpy-r2`, whose cells there are degenerate
   and price dispatch rather than filling, so that one is a break in the sort
   and not in the work. **What changed since Run 19 is which arm leads
   and by how much, not the direction.** Run 19 read its five SIBLING-led class
   margins inside their populations' floors, from 0.9704 on `window` to 0.9856
   on `slice`, and called the sort a naming of rounding; property 2 held
   outright in `revsome` and `scaled`, where the fix itself led,
   and its `reshape1` break was outside the family and far outside that class's
   floor, at 0.5042 against 8.11%. This run prices seven of the eight and every
   one is outside its floor, by factors rather than points --- `reshape1`
   is the eighth and is not priced at all, its leader and the fix having
   no positive net on the same cell --- because the arms that lead are new code
   and not another placement of the same code. So the family clause survives
   where the leader is a sibling, and the honest statement of it now
   is that `mut-odo-vecdims` is not the fastest member of its own family on any
   population this run measured. The third clause reads the last candidate
   `bq-expand` behind `mut-odo-vecdims` and holds in all nine. The summary's
   outside-family slot is `canon-vecdims` in `rev`, `slice` and `window`,
   `mid-copy` in `revsome` and `bcastmid`, `bcast-set` in `bcast`, `canon-full`
   in `scaled` and `canon-memcpy-r2` in `reshape1` --- the rework's arms in all
   eight, where Run 19 had `mut-flat-gm`, `build`, `bq-mut-runs-gm-mulback`
   and `mut-odo`.

3. **The allocation tiers survive, and every level is Run 15's through Run 19's
   to the digit**: the mutable fills at the result vector, `bq-expand` between
   1.14x and 4.91x it, `list` an order of magnitude above. Where a level moves
   it is the class's own `m` showing through, exactly as this property warned
   --- `bq-expand` at 1.14x on `scaled` (`m` of 1 and 2,000) and 4.91x
   on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine
   and `list` running 19.43x to 32.29x across them. **The nine arms that joined
   the roster all read 1.00x**, the mutable fills' own tier, so nothing
   in the leaf block or the rework buys its time with allocation. On a pair
   whose two halves are different compilers this is the property that says
   a difference is codegen and not the program: allocation is deterministic per
   call, none of these levels moved, and the two halves agree on 1143 of 1224
   allocating cells.

**SETTLED 2026-08-24 and APPLIED 2026-08-25, at Run 19's write-up rather
than at the settlement**, so that the retiring orderings got one last
cross-compiler reading and the retirement is recorded with it --- which is how
Run 17 retired claim 4's tie, in prose at its write-up with the manifest taking
it the same day. **They got it**: all thirteen held on both of Run 19's halves,
and the eight that remain hold on both too, so each of the four retires
on a reading rather than on a decision. `CLAIMS` in `read-run.py` carried claims
1, 2 and 6 alone after that settlement, and **claim 1 alone since 2026-08-28**,
`offtab` and `gen-quotrem` having been parked. The test applied: an ordering
stays only if it forecloses something anyone would propose again *and* can still
break. What fails both is a figure, and figures live in the tables above.
**Claims 3, 5 and 9 retire outright.** Claim 3 sets one output form against
another on a build nothing ships, where every leading pure arm
is a `-gm-mulback` already; claim 5's `bq-expand` / `bq-gen` says of itself
that the refutation stands on Runs 7 and 8, and claim 6 keeps that family
guarded through `gen-quotrem`; claim 9's two series are closed at Run 13
by this section's own words, and a closed series in a live manifest
is maintenance without a question. **Claim 4 retires with them, its tie moving
into claim 1** --- and what goes with it is the one place the manifest reads
a *builder* apart from its output, which `--pair` recovers whenever
it is wanted, both arms staying rostered. **Claim 1 becomes the ladder
the `needs` column already draws**, gaining `bq-scan-rem-gm-mulback`, the best
arm needing nothing at all, between `bq-mut-runs-gm-mulback`
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
and to retire with the three `TODO: retarget` markers, which were one decision
with it. **That condition was spent the same day and the link outlived it by two
runs**: the file went to `vFillStrided` on 2026-08-24 and the markers went
with the prose they marked, but nothing read the condition back, so Run 20
registered and read the link like any other and it retired only on 2026-08-26.
Thirteen registered orderings become eight here, and seven when that second link
finally goes; claims 7 and 8 stay unmanifested prose. **The rewriting the ask
paired with this was already done**: the eight *What the class says* paragraphs
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

**Run 20 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) records every class
on BOTH halves**, one process each, in [the
sequence](../README.md#making-a-major-benchmark-run) --- with `window`
and `scaled` rerun in a second window after an intrusion, both halves of each
--- stated here rather than in those two blocks, whose tables and controls
are the reruns' and carry nothing to distinguish them from the other six. Every
table below is the **basis half**'s, which on this run is the 9.12 one, the half
that keeps the lineage. What the second half buys is that a pair's variable can
be read on a class, which is what settled Run 14's `scaled` question and what
no run before it could have asked. **Read across the halves and the direction
Run 19 found holds, at about the same size.** Of the 376 arm-comparisons
the eight classes carry, **259 put the 9.12 half faster and 117 slower**,
and all eight geomeans fall below 1, running **0.9700 on `bcast` to 0.9952
on `window`**, where Run 19's eight ran 0.9830 to 0.9889. So on the classes
as on the main set, GHC HEAD costs this roster a little more, and does
it everywhere. **The extreme at one end is the same arm in all eight classes
and it is new**: `mut-odo-vecdims-add-in-leaf`, from **0.7120** on `bcast`
to 0.8757 on `scaled`, the arm the main set puts at 0.8513 and the counted work
splits ten points codegen to five points not. **The other end wants reading
before it is quoted.** The largest figure any class reports is `reshape1`'s
`canon-vecdims` at **2.7150**, and it is not a movement: that class's
canonicalizing arms return O(1) on three of its four shapes, so the ratio prices
dispatch and not filling. Set those three aside and the high end is **1.1133**,
`reshape1`'s `offtab-aa-distant` --- a clean four-shape reading, 1.0237, 1.2062,
1.0707 and 1.1618, with no cell dropped --- and `rev`'s `offtab-aa-adjacent`
at 1.0970 behind it. Every figure here but that one is read straight off
the eight cross-half lines below; 1.1133 is not, those lines reporting each
class's own maximum, which for `reshape1` is the degenerate 2.7150.

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

**And the aggregate figures in the paragraph above the blocks are the reader's,
emitted rather than assembled.**
`./read-run.py --cross-classes --classes BASIS... --others CONTROL...` prints
every one of them --- the comparison count, the faster/slower split, the range
of the eight geomeans with the class at each end, the arm holding each extreme
and how many populations share it, the degenerate arms it kept out,
and the classes whose `list` is past the 0.7% bar --- from the same per-class
rows the eight cross-half lines below print, so the intro and the blocks cannot
part. The comparison count, the faster/slower split, the range of the eight
geomeans and the extreme arms are each an aggregate over the eight
`--block --compare` lines below, so they are read off those lines and never off
a population assembled for the purpose: Run 20 assembled its own twice
and was wrong both times --- once on the split, once on a low end that excluded
a class the sentence said it covered. Where a figure genuinely cannot come off
those lines, because a class's own maximum is a degenerate cell, the paragraph
says so rather than quoting it as though it could.

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
| `rev` | 3 | 0.047 | 0.067 | `canon-vecdims` 0.046 | `mut-odo-vecdims-add-in-leaf` 0.032 | 4.14% |
| `revsome` | 3 | 0.048 | 0.057 | `mid-copy` 0.046 | `mut-odo-vecdims-add-in-leaf-u2` 0.031 | 6.14% |
| `bcast` | 3 | 0.035 | 0.062 | `bcast-set` 0.032 | `mut-odo-vecdims-add-in-leaf-down` 0.022 | 7.15% |
| `bcastmid` | 4 | 0.031 | 0.058 | **`mid-copy`** 0.017 | **`mid-copy`** 0.017 | 4.83% |
| `reshape1` | 4 | 0.095 | 0.109 | **`canon-memcpy-r2`** 0.000 | **`canon-memcpy-r2`** 0.000 | 8.31% |
| `slice` | 3 | 0.040 | 0.057 | `canon-vecdims` 0.040 | `mut-odo-vecdims-add-in-leaf-down` 0.033 | 5.73% |
| `window` | 3 | 0.062 | 0.095 | `canon-vecdims` 0.037 | `mut-odo-vecdims-add-in-leaf-u2` 0.032 | 5.75% |
| `scaled` | 3 | 0.034 | 0.034 | `canon-full` 0.031 | `mut-odo-vecdims-add-in-leaf-down` 0.029 | 3.01% |

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
| *bq-expand-nosum* | *--* | *--* | *0.09* | *134* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.06* | *145* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.11* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.06* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.051 | 0.09 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.032 | 0.049 | 0.09 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.034 | 0.052 | 0.08 | 145 | 1.00x |
| canon-vecdims | 0.046 | 0.057 | 0.09 | 137 | 1.01x |
| *mut-odo-vecdims-aa-distant* | *0.046* | *0.067* | *0.05* | *137* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.046* | *0.067* | *0.05* | *137* | *1.00x* |
| **mut-odo-vecdims** | **0.047** | 0.067 | 0.06 | 137 | 1.00x |
| mut-odo-vecdims-add-in | 0.047 | 0.068 | 0.20 | 137 | 1.00x |
| mid-copy | 0.048 | 0.074 | 0.08 | 137 | 1.00x |
| bcast-set | 0.049 | 0.070 | 0.10 | 136 | 1.00x |
| canon-memcpy-r2 | 0.050 | 0.060 | 0.08 | 137 | 1.01x |
| canon-full | 0.052 | 0.063 | 0.06 | 136 | 1.01x |
| mut-flat-gm | 0.082 | 0.130 | 0.17 | 134 | 1.34x |
| *build-aa-adjacent* | *0.083* | *0.166* | *1.86* | *126* | *1.00x* |
| build | 0.084 | 0.166 | 2.13 | 126 | 1.00x |
| *build-aa-distant* | *0.086* | *0.182* | *1.81* | *126* | *1.00x* |
| mut-odo | 0.086 | 0.178 | 0.11 | 125 | 1.00x |
| *mut-odo-aa-adjacent* | *0.086* | *0.179* | *0.40* | *126* | *1.00x* |
| *mut-odo-aa-distant* | *0.086* | *0.172* | *0.63* | *125* | *1.00x* |
| bq-expand-gm-mulback | 0.089 | 0.166 | 0.13 | 130 | 2.52x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.095* | *0.115* | *0.10* | *131* | *1.41x* |
| bq-odo-gm-mulback | 0.095 | 0.116 | 0.21 | 131 | 1.41x |
| *bq-odo-gm-mulback-aa-distant* | *0.095* | *0.117* | *0.09* | *131* | *1.41x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.096* | *0.097* | *0.10* | *128* | *1.34x* |
| **bq-scan-rem-gm-mulback** | **0.096** | 0.097 | 0.09 | 128 | 1.34x |
| bq-mut-runs-gm-mulback | 0.096 | 0.140 | 0.22 | 132 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.097* | *0.098* | *0.09* | *128* | *1.34x* |
| bq-mut-runs | 0.098 | 0.143 | 0.20 | 131 | 1.34x |
| *bq-expand-aa-distant* | *0.101* | *0.176* | *0.11* | *129* | *2.52x* |
| bq-expand-qr-prim | 0.103 | 0.174 | 0.12 | 129 | 2.52x |
| bq-expand-b | 0.104 | 0.174 | 0.12 | 128 | 2.52x |
| *bq-expand-aa-adjacent* | *0.104* | *0.174* | *0.10* | *128* | *2.52x* |
| bq-expand | 0.104 | 0.174 | 0.14 | 128 | 2.52x |
| bq-expand-zf | 0.105 | 0.185 | 0.08 | 128 | 2.52x |
| offtab | 0.122 | 0.220 | 0.84 | 122 | 2.00x |
| *offtab-aa-adjacent* | *0.124* | *0.225* | *0.96* | *121* | *2.00x* |
| offtab-scan-rem | 0.128 | 0.132 | 0.07 | 124 | 2.00x |
| *offtab-aa-distant* | *0.131* | *0.208* | *1.24* | *121* | *2.00x* |
| bq-mut | 0.148 | 0.227 | 1.63 | 121 | 1.34x |
| bq-gen | 0.442 | 0.566 | 1.59 | 100 | 1.34x |
| list (baseline) | 1.000 | 1.000 | 0.25 | 86 | 23.43x |
| *list-aa-adjacent* | *1.001* | *1.007* | *0.25* | *86* | *23.43x* |
| *list-aa-distant* | *1.004* | *1.015* | *0.20* | *86* | *23.43x* |
| *gen-unsafe-aa-adjacent* | *1.204* | *1.366* | *1.16* | *82* | *1.00x* |
| gen-unsafe | 1.256 | 1.491 | 1.14 | 81 | 1.00x |
| *gen-unsafe-aa-distant* | *1.266* | *1.412* | *1.18* | *81* | *1.00x* |
| gen-quotrem | 1.267 | 1.491 | 0.97 | 82 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 0.9586, worst
cell 8.40% on `rev-cnn-L1-24x24-c1`, and 15 of 18 intervals cover 1.
The `sum-only` halves agree at 1.0001 on a worst cell of 0.36%
on `rev-gather48-src-50`, its interval covering 1. The in-situ term reads
1.0154, 1.0038, 1.0075, 1.0124 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9594, which
the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m46s, peak 95 MiB in use, 26 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.19 ms per call raw, 4.04 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes):** `mut-odo-vecdims` 0.067/0.052/0.029 `bq-scan-rem-gm-mulback`
0.097/0.097/0.091

**Across the halves:** 31 of the 47 arms are faster on this half and 16 slower,
at a geomean of 0.9856, from `mut-odo-vecdims-add-in-leaf` at 0.8579
to `offtab-aa-adjacent` at 1.0970, with `list` itself at 0.9869. **The baseline
moved 1.31% between the halves, past the 0.7% that lets two columns
be differenced, so this line is NOT read for the pair's variable.** The table
above is one process's and stands; what goes is the comparison.

**What the class says:** all three properties hold and the class reproduces
the main ordering, with the head of its table changed as the main set's is.
The `mut-odo-vecdims` row's `worst` is 0.067, an order of magnitude inside 1;
`bq-expand` sits behind it, behind on all three shapes; and the vecdims family
heads the table, though the member leading is `mut-odo-vecdims-add-in-leaf`
at 0.032 against the arm itself at 0.047 --- **0.7452 paired at 2 of 3 shapes,
a 25.5% margin against this class's 4.14% floor**, so outside it by six times.
The leader being a family member is why property 2's first clause does
not break: it is read as the family's until a run separates them. The best arm
outside the family is `canon-vecdims` at 0.046, where Run 19 had `mut-flat-gm`
at 0.080 --- the rework arm nearly halves that slot. Its floor, 4.14%,
is the second tightest of the eight and looser than Run 19's 2.65%.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *90* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.07* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.16* | *94* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.031 | 0.036 | 0.10 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.031 | 0.036 | 0.10 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.037 | 0.09 | 100 | 1.00x |
| mid-copy | 0.046 | 0.060 | 0.09 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.058* | *0.08* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.048** | 0.057 | 0.09 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.049 | 0.057 | 0.10 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.049* | *0.057* | *0.09* | *96* | *1.00x* |
| canon-vecdims | 0.051 | 0.056 | 0.08 | 96 | 1.00x |
| bcast-set | 0.052 | 0.060 | 0.08 | 96 | 1.00x |
| canon-memcpy-r2 | 0.054 | 0.059 | 0.15 | 96 | 1.00x |
| canon-full | 0.056 | 0.063 | 0.06 | 96 | 1.00x |
| mut-flat-gm | 0.077 | 0.087 | 0.14 | 88 | 1.33x |
| *build-aa-adjacent* | *0.084* | *0.136* | *1.77* | *96* | *1.00x* |
| build | 0.085 | 0.138 | 1.40 | 96 | 1.00x |
| *build-aa-distant* | *0.088* | *0.136* | *2.03* | *96* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.088 | 0.098 | 0.14 | 87 | 1.33x |
| bq-mut-runs | 0.092 | 0.108 | 0.11 | 85 | 1.33x |
| bq-expand-gm-mulback | 0.096 | 0.118 | 0.16 | 83 | 2.52x |
| bq-expand | 0.097 | 0.130 | 0.13 | 83 | 2.52x |
| bq-expand-qr-prim | 0.097 | 0.129 | 0.17 | 83 | 2.52x |
| *mut-odo-aa-distant* | *0.098* | *0.135* | *0.14* | *96* | *1.00x* |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.102 | 0.09 | 86 | 1.33x |
| bq-expand-b | 0.099 | 0.129 | 0.13 | 83 | 2.52x |
| *bq-expand-aa-distant* | *0.100* | *0.129* | *0.16* | *83* | *2.52x* |
| bq-expand-zf | 0.100 | 0.135 | 0.10 | 83 | 2.52x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.103* | *0.08* | *86* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.102* | *0.12* | *86* | *1.33x* |
| *bq-expand-aa-adjacent* | *0.100* | *0.129* | *0.15* | *83* | *2.52x* |
| bq-odo-gm-mulback | 0.102 | 0.123 | 0.11 | 83 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.102* | *0.123* | *0.09* | *83* | *1.41x* |
| *bq-odo-gm-mulback-aa-distant* | *0.103* | *0.123* | *0.09* | *83* | *1.41x* |
| mut-odo | 0.109 | 0.135 | 1.62 | 96 | 1.00x |
| *mut-odo-aa-adjacent* | *0.112* | *0.126* | *0.08* | *96* | *1.00x* |
| *offtab-aa-adjacent* | *0.113* | *0.166* | *1.70* | *90* | *2.00x* |
| offtab | 0.125 | 0.166 | 1.52 | 90 | 2.00x |
| *offtab-aa-distant* | *0.126* | *0.171* | *0.47* | *90* | *2.00x* |
| offtab-scan-rem | 0.131 | 0.131 | 0.14 | 82 | 2.00x |
| bq-mut | 0.147 | 0.177 | 0.49 | 83 | 1.33x |
| bq-gen | 0.417 | 0.573 | 1.61 | 82 | 1.33x |
| *list-aa-distant* | *0.998* | *1.000* | *0.19* | *47* | *23.43x* |
| *list-aa-adjacent* | *0.999* | *1.001* | *0.23* | *47* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 47 | 23.43x |
| *gen-unsafe-aa-adjacent* | *1.252* | *1.396* | *0.55* | *42* | *1.00x* |
| gen-unsafe | 1.272 | 1.519 | 0.66 | 41 | 1.00x |
| gen-quotrem | 1.306 | 1.548 | 0.70 | 42 | 1.00x |
| *gen-unsafe-aa-distant* | *1.319* | *1.323* | *0.91* | *43* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 0.9386, worst
cell 12.93% on `revsome-mid-cnn-L2`, and 13 of 18 intervals cover 1.
The `sum-only` halves agree at 0.9997 on a worst cell of 0.08%
on `revsome-outer-g48`, its interval covering 1. The in-situ term reads 1.0116,
1.0178, 0.9967, 1.0114 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9403, which
the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m47s, peak 132 MiB in use, 26 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 4.18 ms per call raw, 4.02 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.053/0.057
`bq-scan-rem-gm-mulback` 0.102/0.098/0.098

**Across the halves:** 36 of the 47 arms are faster on this half and 11 slower,
at a geomean of 0.9805, from `mut-odo-vecdims-add-in-leaf` at 0.8394
to `gen-quotrem` at 1.0436, with `list` itself at 0.9925. **The baseline moved
0.75% between the halves, past the 0.7% that lets two columns be differenced,
so this line is NOT read for the pair's variable.** The table above is one
process's and stands; what goes is the comparison.

**What the class says:** all three properties hold and nothing inverts.
`mut-odo-vecdims`'s `worst` is 0.057 and `bq-expand` trails it on every shape.
The table's head is `mut-odo-vecdims-add-in-leaf-u2` at 0.031 against the fix's
0.048 --- **0.7004 paired at 2 of 3 shapes, 30.0% against a 6.14% floor** ---
a family member again, so the first clause stands. **This is one of the two
classes where the shipped variant leads its own block** --- `window`
is the other --- which it does not on the main set; with three shapes
and a floor of 6.14% that is an ordering and not a separation, and the main set
is where the block's internal ordering is decided. The best outside the family
is `mid-copy` at 0.046, against Run 19's `mut-flat-gm` at 0.078. The floor
loosened from Run 19's 2.00%, which was that half's tightest, to 6.14%, third
widest here --- so the class that looked tightest a run ago is not,
and the floor is a property of the run.

**`bcast` --- an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *52* | *1.38x* |
| *canon-full-nosum* | *--* | *--* | *0.48* | *84* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.58* | *58* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.35* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.022 | 0.023 | 0.49 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.022 | 0.023 | 0.48 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.028 | 0.48 | 59 | 1.00x |
| bcast-set | 0.032 | 0.061 | 0.49 | 61 | 1.00x |
| canon-full | 0.033 | 0.061 | 0.50 | 61 | 1.00x |
| mid-copy | 0.035 | 0.061 | 0.53 | 60 | 1.00x |
| mut-odo-vecdims-add-in | 0.035 | 0.062 | 0.52 | 60 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.035* | *0.062* | *0.38* | *60* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.035* | *0.062* | *0.50* | *60* | *1.00x* |
| **mut-odo-vecdims** | **0.035** | 0.062 | 0.41 | 60 | 1.00x |
| canon-vecdims | 0.035 | 0.061 | 0.53 | 60 | 1.00x |
| canon-memcpy-r2 | 0.037 | 0.066 | 0.54 | 60 | 1.00x |
| *build-aa-distant* | *0.054* | *0.134* | *1.28* | *60* | *1.00x* |
| *build-aa-adjacent* | *0.054* | *0.133* | *2.31* | *60* | *1.00x* |
| build | 0.055 | 0.136 | 1.69 | 60 | 1.00x |
| *mut-odo-aa-distant* | *0.057* | *0.144* | *0.65* | *60* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.057* | *0.144* | *0.94* | *60* | *1.00x* |
| mut-odo | 0.058 | 0.152 | 1.32 | 60 | 1.00x |
| mut-flat-gm | 0.066 | 0.072 | 0.66 | 49 | 1.13x |
| bq-mut-runs-gm-mulback | 0.079 | 0.088 | 0.60 | 47 | 1.13x |
| bq-expand-gm-mulback | 0.079 | 0.083 | 0.62 | 48 | 1.38x |
| bq-odo-gm-mulback | 0.082 | 0.088 | 0.70 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.082* | *0.089* | *0.85* | *47* | *1.14x* |
| *bq-odo-gm-mulback-aa-distant* | *0.083* | *0.089* | *0.52* | *47* | *1.14x* |
| bq-mut-runs | 0.086 | 0.095 | 0.67 | 46 | 1.13x |
| bq-expand-b | 0.088 | 0.097 | 0.65 | 46 | 1.38x |
| *offtab-aa-distant* | *0.089* | *0.170* | *1.16* | *53* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.090* | *0.099* | *0.06* | *47* | *1.13x* |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.097 | 0.68 | 47 | 1.13x |
| *offtab-aa-adjacent* | *0.090* | *0.176* | *1.00* | *53* | *2.00x* |
| offtab | 0.090 | 0.176 | 0.86 | 53 | 2.00x |
| bq-expand-qr-prim | 0.091 | 0.096 | 0.67 | 46 | 1.38x |
| bq-expand-zf | 0.091 | 0.097 | 0.67 | 46 | 1.38x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.091* | *0.098* | *0.65* | *47* | *1.13x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.097* | *0.65* | *46* | *1.38x* |
| bq-expand | 0.091 | 0.097 | 0.64 | 46 | 1.38x |
| *bq-expand-aa-distant* | *0.092* | *0.098* | *0.40* | *46* | *1.38x* |
| bq-mut | 0.121 | 0.161 | 0.66 | 46 | 1.13x |
| offtab-scan-rem | 0.128 | 0.141 | 1.00 | 43 | 2.00x |
| bq-gen | 0.173 | 0.270 | 0.79 | 46 | 1.13x |
| *gen-unsafe-aa-adjacent* | *0.953* | *1.054* | *1.10* | *21* | *1.00x* |
| gen-unsafe | 0.992 | 1.051 | 1.80 | 21 | 1.00x |
| *list-aa-distant* | *0.998* | *1.000* | *1.19* | *18* | *20.62x* |
| list (baseline) | 1.000 | 1.000 | 0.94 | 18 | 20.62x |
| *list-aa-adjacent* | *1.003* | *1.009* | *0.73* | *18* | *20.62x* |
| gen-quotrem | 1.027 | 1.028 | 1.58 | 20 | 1.00x |
| *gen-unsafe-aa-distant* | *1.100* | *1.107* | *1.39* | *20* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0715, worst
cell 8.24% on `bcast-tall-Mx2`, and 14 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0014 on a worst cell of 0.72% on `bcast-inner8`, its interval
covering 1. The in-situ term reads 1.0187, 1.0152, 1.0115, 1.0119 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0684, which the correction amplifies by 1.04x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h13m47s, peak 151 MiB in use, 45 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 27.9 ms per call raw, 26.8 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900,
bcast-tall-Mx2):** `mut-odo-vecdims` 0.033/0.022/0.062 `bq-scan-rem-gm-mulback`
0.089/0.089/0.097

**Across the halves:** 36 of the 47 arms are faster on this half and 11 slower,
at a geomean of 0.9700, from `mut-odo-vecdims-add-in-leaf` at 0.7120
to `gen-unsafe-aa-distant` at 1.0629, with `list` itself at 1.0045.

**What the class says:** all three properties hold, and this is one of the three
classes the rework was registered to act on, `bcastmid` and `window` being
the others. `bcast-set`, the zero-stride condition taken solo, is **the best arm
outside the vecdims family at 0.032**, against `build`'s 0.057 in Run 19 ---
the registration asked only for it to be ahead of its control on `bcast`
and it is, by a factor rather than a margin. The table's head
is `mut-odo-vecdims-add-in-leaf-down` at 0.022 against the fix's 0.035, **0.6195
paired at 2 of 3 shapes, 38.1% against this class's 7.15% floor**; the leader
is a family member, so the first clause holds. `worst` is 0.062 and `bq-expand`
is behind throughout. The floor, 7.15%, is the second widest of the eight
and well above Run 19's 4.79%.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000,
`sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed
2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k`
is its worst, its block taken to 150000 elements where the class's others run 3
to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *70* | *1.57x* |
| *canon-full-nosum* | *--* | *--* | *0.44* | *104* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.45* | *75* | *1.17x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.28* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| mid-copy | 0.017 | 0.032 | 0.37 | 80 | 1.00x |
| canon-full | 0.018 | 0.033 | 0.56 | 80 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.023 | 0.037 | 0.35 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.023 | 0.037 | 0.33 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.037 | 0.34 | 78 | 1.00x |
| mut-odo-vecdims-add-in | 0.031 | 0.058 | 0.32 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.031* | *0.058* | *0.30* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.031** | 0.058 | 0.30 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.058* | *0.21* | *76* | *1.00x* |
| canon-vecdims | 0.032 | 0.058 | 0.36 | 75 | 1.00x |
| bcast-set | 0.033 | 0.061 | 0.34 | 75 | 1.00x |
| canon-memcpy-r2 | 0.033 | 0.061 | 0.38 | 74 | 1.00x |
| *mut-odo-aa-distant* | *0.047* | *0.127* | *0.33* | *69* | *1.00x* |
| *build-aa-adjacent* | *0.048* | *0.138* | *1.16* | *68* | *1.00x* |
| build | 0.049 | 0.147 | 1.21 | 68 | 1.00x |
| *mut-odo-aa-adjacent* | *0.049* | *0.150* | *1.35* | *68* | *1.00x* |
| *build-aa-distant* | *0.049* | *0.144* | *1.01* | *68* | *1.00x* |
| mut-odo | 0.050 | 0.142 | 1.46 | 68 | 1.00x |
| mut-flat-gm | 0.062 | 0.090 | 0.58 | 68 | 1.17x |
| bq-mut-runs-gm-mulback | 0.074 | 0.106 | 0.48 | 66 | 1.17x |
| bq-expand-gm-mulback | 0.076 | 0.121 | 0.47 | 64 | 1.57x |
| bq-mut-runs | 0.077 | 0.107 | 0.46 | 65 | 1.17x |
| offtab | 0.078 | 0.172 | 0.65 | 64 | 2.00x |
| *offtab-aa-adjacent* | *0.078* | *0.177* | *1.05* | *64* | *2.00x* |
| *offtab-aa-distant* | *0.079* | *0.177* | *1.06* | *64* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.079* | *0.099* | *0.39* | *64* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.079** | 0.099 | 0.42 | 64 | 1.17x |
| bq-odo-gm-mulback | 0.079 | 0.123 | 0.43 | 64 | 1.17x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.079* | *0.123* | *0.41* | *64* | *1.17x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.079* | *0.099* | *0.25* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-distant* | *0.079* | *0.124* | *0.36* | *64* | *1.17x* |
| bq-expand-qr-prim | 0.084 | 0.129 | 0.41 | 64 | 1.57x |
| bq-expand-b | 0.084 | 0.129 | 0.41 | 64 | 1.57x |
| bq-expand | 0.084 | 0.129 | 0.42 | 64 | 1.57x |
| *bq-expand-aa-distant* | *0.084* | *0.129* | *0.33* | *64* | *1.57x* |
| *bq-expand-aa-adjacent* | *0.085* | *0.129* | *0.41* | *64* | *1.57x* |
| bq-expand-zf | 0.085 | 0.134 | 0.40 | 64 | 1.57x |
| bq-mut | 0.102 | 0.180 | 0.66 | 61 | 1.17x |
| offtab-scan-rem | 0.107 | 0.129 | 0.64 | 60 | 2.00x |
| bq-gen | 0.176 | 0.569 | 1.30 | 50 | 1.17x |
| *gen-unsafe-aa-adjacent* | *0.958* | *1.575* | *1.29* | *28* | *1.00x* |
| gen-unsafe | 0.974 | 1.543 | 1.59 | 28 | 1.00x |
| *gen-unsafe-aa-distant* | *0.981* | *1.522* | *1.71* | *28* | *1.00x* |
| gen-quotrem | 0.992 | 1.484 | 1.48 | 28 | 1.00x |
| *list-aa-adjacent* | *0.998* | *0.999* | *1.14* | *29* | *21.22x* |
| *list-aa-distant* | *0.999* | *1.002* | *1.09* | *30* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 1.16 | 29 | 21.22x |

**Controls:** The largest A/A pair is `mut-odo-aa-distant` at 0.9517, worst cell
10.54% on `bcastmid-c32-cnn`, and 11 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9987 on a worst cell of 0.57% on `bcastmid-c32-cnn`,
its interval covering 1. The in-situ term reads 1.0179, 1.0449, 1.0138, 1.0202
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 0.9615, which the correction amplifies
by 1.65x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m21s, peak 138 MiB in use, 38 MiB max residency;
the reader reads 53 benchmarks over 4 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 48.5 ms per call raw, 47.4 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.058/0.021/0.036/0.022
`bq-scan-rem-gm-mulback` 0.099/0.087/0.069/0.065

**Across the halves:** 28 of the 47 arms are faster on this half and 19 slower,
at a geomean of 0.9849, from `mut-odo-vecdims-add-in-leaf` at 0.8089
to `offtab-aa-adjacent` at 1.0335, with `list` itself at 1.0082. **The baseline
moved 0.82% between the halves, past the 0.7% that lets two columns
be differenced, so this line is NOT read for the pair's variable.** The table
above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1 and 3 hold and **property 2 BREAKS
outright, which is the result this class was extended to get.** `mid-copy` ---
the zero-stride-on-an-outer-axis condition taken solo, the second
of the rework's two conditions --- is the fastest timed arm at **0.017** against
`mut-odo-vecdims`'s 0.031, **0.5490 paired and ahead on 4 of 4 shapes, a 45.1%
margin against this class's 4.83% floor**. It is not a vecdims variant,
so unlike the six classes where a sibling leads, the first clause of property 2
breaks here rather than being read as the family's. Its registration asked
for `mid-copy` ahead of its control on `bcastmid` and it is, on every shape
including the new one: `bcastmid-block150k`, the block-copy arm's best case,
was added for exactly this reading. `worst` is 0.058 and `bq-expand` trails
throughout, so the fix is never slower than the `list` it replaces here whatever
leads the table. The floor is 4.83%, against Run 19's 4.16% over three shapes.

**`reshape1` --- the `[n] -> [n, 1]` trap: innermost extent 1 on a stride-0
axis.** Shapes: `reshape1-500k` (`l` 500000, `sInner` 1), `reshape1-r3` (`l`
180000, `sInner` 1), `reshape1-rank10` (`l` 59049, `sInner` 1),
`reshape1-strided-r3` (`l` 180000, `sInner` 1). The fourth landed 2026-08-25
and is the one cell of this class that prices a fill: it is `reshape1-r3`'s
dense shape viewed with its innermost two dimensions transposed before
the size-1 dim is appended, so dropping that dim leaves a strided view where
the other three leave a contiguous run.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.27* | *84* | *4.91x* |
| *canon-full-nosum* | *--* | *--* | *0.28* | *256* | *0.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.47* | *104* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| canon-memcpy-r2 | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| canon-full | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| canon-vecdims | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.062 | 0.08 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.030 | 0.066 | 0.08 | 98 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.030 | 0.065 | 0.12 | 98 | 1.00x |
| mut-flat-gm | 0.034 | 0.129 | 0.23 | 96 | 2.00x |
| bq-mut-runs-gm-mulback | 0.034 | 0.125 | 0.22 | 96 | 2.00x |
| *bq-odo-gm-mulback-aa-distant* | *0.049* | *0.140* | *0.14* | *92* | *2.26x* |
| bq-odo-gm-mulback | 0.050 | 0.139 | 0.15 | 92 | 2.26x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.050* | *0.139* | *0.14* | *92* | *2.26x* |
| bq-mut-runs | 0.072 | 0.150 | 0.30 | 86 | 2.00x |
| bq-expand-gm-mulback | 0.074 | 0.169 | 0.28 | 87 | 4.91x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.075* | *0.092* | *0.10* | *86* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.075** | 0.092 | 0.14 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.075* | *0.092* | *0.12* | *86* | *2.00x* |
| offtab-scan-rem | 0.075 | 0.092 | 0.11 | 86 | 2.00x |
| mut-odo-vecdims-add-in | 0.094 | 0.109 | 0.07 | 82 | 1.00x |
| **mut-odo-vecdims** | **0.095** | 0.109 | 0.12 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.095* | *0.109* | *0.17* | *82* | *1.00x* |
| mid-copy | 0.095 | 0.121 | 0.24 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.095* | *0.109* | *0.13* | *82* | *1.00x* |
| bcast-set | 0.095 | 0.107 | 0.20 | 82 | 1.00x |
| bq-expand-b | 0.110 | 0.201 | 0.24 | 80 | 4.91x |
| bq-expand-qr-prim | 0.114 | 0.201 | 0.28 | 80 | 4.91x |
| *bq-expand-aa-adjacent* | *0.114* | *0.201* | *0.28* | *80* | *4.91x* |
| bq-expand | 0.115 | 0.201 | 0.23 | 80 | 4.91x |
| *bq-expand-aa-distant* | *0.115* | *0.200* | *0.22* | *80* | *4.91x* |
| bq-expand-zf | 0.117 | 0.217 | 0.30 | 80 | 4.91x |
| *build-aa-distant* | *0.228* | *0.294* | *2.56* | *68* | *1.00x* |
| *build-aa-adjacent* | *0.229* | *0.323* | *2.33* | *67* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.246* | *0.284* | *0.68* | *66* | *1.00x* |
| mut-odo | 0.250 | 0.284 | 1.65 | 66 | 1.00x |
| build | 0.251 | 0.309 | 3.50 | 66 | 1.00x |
| bq-mut | 0.260 | 0.308 | 1.33 | 66 | 2.00x |
| *mut-odo-aa-distant* | *0.261* | *0.321* | *1.67* | *66* | *1.00x* |
| offtab | 0.275 | 0.315 | 1.66 | 64 | 2.00x |
| *offtab-aa-adjacent* | *0.282* | *0.334* | *1.66* | *64* | *2.00x* |
| *offtab-aa-distant* | *0.298* | *0.342* | *0.87* | *62* | *2.00x* |
| gen-unsafe | 0.947 | 1.955 | 1.16 | 42 | 1.00x |
| *gen-unsafe-aa-distant* | *0.950* | *2.214* | *2.55* | *43* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.986* | *2.115* | *0.47* | *42* | *1.00x* |
| bq-gen | 0.989 | 2.611 | 1.73 | 41 | 2.00x |
| gen-quotrem | 0.995 | 2.104 | 0.93 | 42 | 1.00x |
| *list-aa-distant* | *0.999* | *1.004* | *0.32* | *41* | *32.29x* |
| list (baseline) | 1.000 | 1.000 | 0.31 | 41 | 32.29x |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.27* | *41* | *32.29x* |

**Controls:** The largest A/A pair is `offtab-aa-distant` at 1.0831, worst cell
11.86% on `reshape1-strided-r3`, and 14 of 18 intervals cover 1. The `sum-only`
halves agree at 1.0007 on a worst cell of 0.46% on `reshape1-500k`, its interval
covering 1. The in-situ term reads 1.0120, 1.0002, 1.0241, 1.0996 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0769, which the correction amplifies by 1.08x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h18m19s, peak 159 MiB in use, 39 MiB max residency;
the reader reads 53 benchmarks over 4 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 13.2 ms per call raw, 12.9 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10,
reshape1-strided-r3):** `mut-odo-vecdims` 0.090/0.091/0.109/0.095
`bq-scan-rem-gm-mulback` 0.072/0.073/0.092/0.075

**Across the halves:** 33 of the 47 arms are faster on this half and 14 slower,
at a geomean of 0.9927, from `mut-odo-vecdims-add-in-leaf` at 0.7409
to `canon-vecdims` at 2.7150, with `list` itself at 0.9897. **The baseline moved
1.03% between the halves, past the 0.7% that lets two columns be differenced,
so this line is NOT read for the pair's variable.** The table above is one
process's and stands; what goes is the comparison.

**What the class says:** properties 1 and 3 hold, **property 2 breaks,
and this class's cells need reading before its table does.** Three of its four
shapes go degenerate for the canonicalizing arms: canonicalization drops
the unit dimension, the fill becomes a regime-1 return, and there is nothing
per-element left for the correction to subtract --- so `canon-vecdims`,
`canon-memcpy-r2` and `canon-full` each read `--` on those cells and their rows
are geomeans over 3 of 4 shapes, which the reader now reports as work removed
rather than failing the file. **`reshape1-strided-r3` is the one cell
of this class that prices a fill**, and it landed with this roster
for that reason. So the table's head, `canon-memcpy-r2` at 0.000, is the class
measuring dispatch and not filling, and the honest statement of property 2 here
is that the arms that lead have nothing to do; `mut-odo-vecdims` reads 0.095
with `worst` 0.109, an order of magnitude inside 1, and `bq-expand` trails it.
This class carries the run's widest floor at **8.31%** and its worst A/A cell
on the control half, 19.19% on `reshape1-r3`. It is also the class the counted
work singles out: every arm together reads 0.9995 HEAD against 9.12, where
the other seven read 0.9860 to 0.9918.

**`slice` --- a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *90* | *1.58x* |
| *canon-full-nosum* | *--* | *--* | *0.09* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.14* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.033 | 0.037 | 0.09 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.037 | 0.07 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.035 | 0.038 | 0.07 | 99 | 1.00x |
| mut-odo-vecdims-add-in | 0.040 | 0.057 | 0.08 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.040** | 0.057 | 0.08 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.040* | *0.057* | *0.07* | *96* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.058* | *0.07* | *96* | *1.00x* |
| canon-vecdims | 0.040 | 0.057 | 0.10 | 96 | 1.00x |
| mid-copy | 0.040 | 0.058 | 0.06 | 96 | 1.00x |
| canon-memcpy-r2 | 0.041 | 0.060 | 0.08 | 96 | 1.00x |
| bcast-set | 0.042 | 0.061 | 0.10 | 96 | 1.00x |
| canon-full | 0.042 | 0.064 | 0.09 | 96 | 1.00x |
| *mut-odo-aa-adjacent* | *0.062* | *0.130* | *0.09* | *96* | *1.00x* |
| build | 0.064 | 0.134 | 1.17 | 96 | 1.00x |
| mut-odo | 0.064 | 0.138 | 0.53 | 96 | 1.00x |
| *build-aa-adjacent* | *0.064* | *0.139* | *0.87* | *96* | *1.00x* |
| *mut-odo-aa-distant* | *0.065* | *0.133* | *0.18* | *96* | *1.00x* |
| *build-aa-distant* | *0.066* | *0.147* | *1.01* | *96* | *1.00x* |
| mut-flat-gm | 0.083 | 0.088 | 0.10 | 88 | 1.08x |
| *offtab-aa-distant* | *0.091* | *0.160* | *0.56* | *90* | *2.00x* |
| bq-mut-runs-gm-mulback | 0.093 | 0.095 | 0.16 | 86 | 1.08x |
| *offtab-aa-adjacent* | *0.096* | *0.179* | *1.55* | *90* | *2.00x* |
| offtab | 0.097 | 0.180 | 1.27 | 90 | 2.00x |
| bq-mut-runs | 0.098 | 0.104 | 0.17 | 85 | 1.08x |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.103 | 0.08 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.099* | *0.103* | *0.10* | *86* | *1.08x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.099* | *0.103* | *0.07* | *86* | *1.08x* |
| bq-expand-gm-mulback | 0.103 | 0.119 | 0.09 | 83 | 1.58x |
| bq-expand-qr-prim | 0.109 | 0.127 | 0.14 | 83 | 1.58x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.109* | *0.120* | *0.09* | *83* | *1.50x* |
| bq-expand-b | 0.110 | 0.128 | 0.10 | 83 | 1.58x |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.121* | *0.11* | *83* | *1.50x* |
| bq-odo-gm-mulback | 0.110 | 0.121 | 0.08 | 83 | 1.50x |
| bq-expand | 0.110 | 0.128 | 0.16 | 83 | 1.58x |
| *bq-expand-aa-adjacent* | *0.110* | *0.128* | *0.09* | *83* | *1.58x* |
| *bq-expand-aa-distant* | *0.110* | *0.128* | *0.08* | *83* | *1.58x* |
| bq-expand-zf | 0.112 | 0.134 | 0.10 | 83 | 1.58x |
| bq-mut | 0.125 | 0.175 | 0.52 | 83 | 1.08x |
| offtab-scan-rem | 0.130 | 0.132 | 0.12 | 81 | 2.00x |
| bq-gen | 0.256 | 0.565 | 0.94 | 82 | 1.08x |
| list (baseline) | 1.000 | 1.000 | 0.21 | 46 | 20.54x |
| *list-aa-adjacent* | *1.000* | *1.003* | *0.19* | *46* | *20.54x* |
| *list-aa-distant* | *1.000* | *1.003* | *0.14* | *46* | *20.54x* |
| *gen-unsafe-aa-distant* | *1.487* | *2.429* | *1.07* | *42* | *1.00x* |
| gen-unsafe | 1.533 | 2.450 | 1.63 | 42 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.588* | *2.428* | *1.14* | *42* | *1.00x* |
| gen-quotrem | 1.622 | 2.405 | 0.82 | 42 | 1.00x |

**Controls:** The largest A/A pair is `offtab-aa-distant` at 0.9427, worst cell
10.80% on `slice-cnn-L2-24x24-c32`, and 14 of 18 intervals cover 1.
The `sum-only` halves agree at 0.9992 on a worst cell of 0.31%
on `slice-coprime-r7`, its interval covering 1. The in-situ term reads 1.0161,
1.0100, 1.0157, 1.0499 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9551, which
the correction amplifies by 1.39x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m48s, peak 117 MiB in use, 37 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.17 ms per call raw, 4.01 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7):** `mut-odo-vecdims` 0.057/0.030/0.037
`bq-scan-rem-gm-mulback` 0.098/0.103/0.096

**Across the halves:** 33 of the 47 arms are faster on this half and 14 slower,
at a geomean of 0.9885, from `mut-odo-vecdims-add-in-leaf` at 0.8672 to `offtab`
at 1.0674, with `list` itself at 0.9806. **The baseline moved 1.94% between
the halves, past the 0.7% that lets two columns be differenced, so this line
is NOT read for the pair's variable.** The table above is one process's
and stands; what goes is the comparison.

**What the class says:** all three properties hold and the class reproduces
the main ordering. `mut-odo-vecdims` reads 0.040 with `worst` 0.057,
and `bq-expand` is behind on every shape. The head
is `mut-odo-vecdims-add-in-leaf-down` at 0.033, **0.8338 paired at 2 of 3
shapes, 16.6% against this class's 5.73% floor** --- a family member,
so the first clause holds. The best outside the family is `canon-vecdims`
at 0.040, level with the fix itself and against `build`'s 0.065 in Run 19.
This class has the widest gap on the column of the eight,
its `best outside family` sitting exactly on `mut-odo-vecdims`, so a sentence
about the narrowest or widest gap has to say whether it means the column
or the paired reading. The floor loosened from Run 19's 2.43% to 5.73%.

**`window` --- overlapping im2col patches: the workload the README opens
by naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *116* | *2.81x* |
| *canon-full-nosum* | *--* | *--* | *0.35* | *153* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.85* | *134* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *150* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *150* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.032 | 0.035 | 0.09 | 132 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.037 | 0.10 | 130 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.037 | 0.16 | 130 | 1.00x |
| canon-vecdims | 0.037 | 0.058 | 0.08 | 137 | 1.01x |
| canon-full | 0.039 | 0.063 | 0.16 | 137 | 1.01x |
| canon-memcpy-r2 | 0.040 | 0.063 | 0.30 | 137 | 1.01x |
| mut-odo-vecdims-add-in | 0.061 | 0.095 | 0.09 | 116 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.095* | *0.09* | *116* | *1.00x* |
| **mut-odo-vecdims** | **0.062** | 0.095 | 0.06 | 116 | 1.00x |
| *mut-odo-vecdims-aa* | *0.062* | *0.095* | *0.05* | *116* | *1.00x* |
| mid-copy | 0.064 | 0.101 | 0.28 | 115 | 1.00x |
| bcast-set | 0.066 | 0.103 | 0.06 | 115 | 1.00x |
| mut-flat-gm | 0.069 | 0.087 | 0.44 | 126 | 1.33x |
| bq-mut-runs-gm-mulback | 0.076 | 0.097 | 0.22 | 127 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.097* | *0.08* | *120* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.093* | *0.097* | *0.07* | *120* | *1.33x* |
| bq-odo-gm-mulback | 0.093 | 0.118 | 0.25 | 121 | 2.55x |
| **bq-scan-rem-gm-mulback** | **0.094** | 0.096 | 0.06 | 120 | 1.33x |
| *bq-odo-gm-mulback-aa-distant* | *0.094* | *0.119* | *0.26* | *121* | *2.55x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.119* | *0.21* | *121* | *2.55x* |
| bq-mut-runs | 0.095 | 0.102 | 0.24 | 117 | 1.33x |
| bq-expand-gm-mulback | 0.099 | 0.118 | 0.08 | 119 | 2.81x |
| offtab-scan-rem | 0.115 | 0.126 | 0.05 | 120 | 2.00x |
| bq-expand-qr-prim | 0.120 | 0.128 | 0.14 | 112 | 2.81x |
| bq-expand-b | 0.120 | 0.128 | 0.16 | 112 | 2.81x |
| bq-expand | 0.120 | 0.128 | 0.23 | 112 | 2.81x |
| *bq-expand-aa-distant* | *0.120* | *0.128* | *0.13* | *112* | *2.81x* |
| *bq-expand-aa-adjacent* | *0.121* | *0.129* | *0.12* | *112* | *2.81x* |
| bq-expand-zf | 0.124 | 0.134 | 0.15 | 112 | 2.81x |
| build | 0.144 | 0.243 | 2.26 | 99 | 1.00x |
| *build-aa-adjacent* | *0.147* | *0.247* | *2.45* | *99* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.151* | *0.264* | *1.30* | *98* | *1.00x* |
| *build-aa-distant* | *0.152* | *0.272* | *1.94* | *98* | *1.00x* |
| mut-odo | 0.153 | 0.261 | 1.90 | 98 | 1.00x |
| *mut-odo-aa-distant* | *0.155* | *0.266* | *0.83* | *98* | *1.00x* |
| *offtab-aa-distant* | *0.183* | *0.294* | *1.84* | *95* | *2.00x* |
| *offtab-aa-adjacent* | *0.185* | *0.304* | *1.67* | *96* | *2.00x* |
| offtab | 0.186 | 0.300 | 2.35 | 96 | 2.00x |
| bq-mut | 0.191 | 0.269 | 1.13 | 98 | 1.33x |
| bq-gen | 0.539 | 0.978 | 1.26 | 73 | 1.33x |
| list (baseline) | 1.000 | 1.000 | 0.30 | 73 | 24.76x |
| *list-aa-adjacent* | *1.002* | *1.004* | *0.26* | *73* | *24.76x* |
| *list-aa-distant* | *1.007* | *1.007* | *0.33* | *73* | *24.76x* |
| *gen-unsafe-aa-adjacent* | *1.097* | *1.423* | *1.51* | *76* | *1.00x* |
| gen-unsafe | 1.098 | 1.426 | 1.24 | 75 | 1.00x |
| *gen-unsafe-aa-distant* | *1.101* | *1.319* | *1.95* | *74* | *1.00x* |
| gen-quotrem | 1.113 | 1.419 | 0.63 | 74 | 1.00x |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0575, worst cell
11.77% on `window-64x64-k1x9`, and 12 of 18 intervals cover 1. The `sum-only`
halves agree at 0.9996 on a worst cell of 0.11% on `window-28x28-k5`,
its interval missing 1. The in-situ term reads 1.0061, 1.0064, 0.9960, 1.0427
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0486, which the correction amplifies
by 1.21x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m46s, peak 110 MiB in use, 24 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.54 ms per call raw, 9.27 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9):** `mut-odo-vecdims` 0.044/0.057/0.095
`bq-scan-rem-gm-mulback` 0.095/0.096/0.074

**Across the halves:** 25 of the 47 arms are faster on this half and 22 slower,
at a geomean of 0.9952, from `mut-odo-vecdims-add-in-leaf` at 0.8495
to `build-aa-distant` at 1.0777, with `list` itself at 1.0053.

**What the class says:** all three properties hold. `mut-odo-vecdims` reads
0.062, its highest of the eight classes bar `reshape1`, with `worst` 0.095
and `bq-expand` behind throughout. The head is `mut-odo-vecdims-add-in-leaf-u2`
at 0.032, **0.5144 paired and ahead on 3 of 3 shapes, a 48.6% margin against
this class's 5.75% floor** --- the widest family margin of the eight,
and a family member, so the first clause holds. **The rework arm registered
for this class did not take the outside-family slot**: `canon-memcpy-r2`, whose
contiguous-run copy fires here, is behind `canon-vecdims`, which leads outside
the family at 0.037 against Run 19's `mut-flat-gm` at 0.070. The registration
asked for `canon-memcpy-r2` ahead of its control on `window` and read
by population that is what its 0.052 on the main table is measured against; what
this class shows is that a sibling of it does better here, which
the registration did not ask about and which the next run's entry carries.
The floor is 5.75%, against Run 19's 7.57%.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one
strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *119* | *1.14x* |
| *canon-full-nosum* | *--* | *--* | *0.14* | *144* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.12* | *125* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.029 | 0.034 | 0.14 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.030 | 0.034 | 0.10 | 126 | 1.00x |
| canon-full | 0.031 | 0.034 | 0.11 | 126 | 1.00x |
| canon-vecdims | 0.031 | 0.034 | 0.09 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.031 | 0.034 | 0.13 | 125 | 1.00x |
| canon-memcpy-r2 | 0.032 | 0.034 | 0.08 | 126 | 1.00x |
| bcast-set | 0.033 | 0.037 | 0.15 | 126 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.034* | *0.035* | *0.09* | *126* | *1.00x* |
| **mut-odo-vecdims** | **0.034** | 0.034 | 0.10 | 126 | 1.00x |
| mut-odo-vecdims-add-in | 0.034 | 0.034 | 0.09 | 126 | 1.00x |
| mid-copy | 0.034 | 0.034 | 0.06 | 126 | 1.00x |
| *mut-odo-vecdims-aa* | *0.034* | *0.034* | *0.09* | *126* | *1.00x* |
| *mut-odo-aa-distant* | *0.036* | *0.048* | *0.11* | *124* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.036* | *0.048* | *0.15* | *124* | *1.00x* |
| mut-odo | 0.036 | 0.049 | 0.13 | 124 | 1.00x |
| *build-aa-distant* | *0.036* | *0.052* | *0.16* | *124* | *1.00x* |
| build | 0.037 | 0.048 | 0.30 | 125 | 1.00x |
| *build-aa-adjacent* | *0.037* | *0.052* | *0.15* | *125* | *1.00x* |
| *offtab-aa-adjacent* | *0.066* | *0.074* | *0.47* | *118* | *2.00x* |
| offtab | 0.067 | 0.077 | 0.77 | 118 | 2.00x |
| *offtab-aa-distant* | *0.067* | *0.077* | *0.61* | *118* | *2.00x* |
| mut-flat-gm | 0.072 | 0.073 | 0.12 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.081 | 0.081 | 0.06 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.083 | 0.087 | 0.08 | 114 | 1.14x |
| bq-odo-gm-mulback | 0.090 | 0.092 | 0.06 | 113 | 1.04x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.090* | *0.092* | *0.05* | *113* | *1.04x* |
| *bq-odo-gm-mulback-aa-distant* | *0.090* | *0.093* | *0.06* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.090* | *0.094* | *0.05* | *112* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.094 | 0.05 | 112 | 1.04x |
| bq-mut-runs | 0.091 | 0.092 | 0.07 | 112 | 1.03x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.095* | *0.06* | *112* | *1.04x* |
| bq-expand-qr-prim | 0.095 | 0.097 | 0.07 | 112 | 1.14x |
| bq-expand-zf | 0.095 | 0.098 | 0.06 | 112 | 1.14x |
| bq-expand-b | 0.095 | 0.098 | 0.08 | 112 | 1.14x |
| *bq-expand-aa-adjacent* | *0.095* | *0.098* | *0.05* | *112* | *1.14x* |
| bq-expand | 0.096 | 0.098 | 0.07 | 112 | 1.14x |
| *bq-expand-aa-distant* | *0.096* | *0.099* | *0.08* | *111* | *1.14x* |
| bq-mut | 0.100 | 0.112 | 0.17 | 111 | 1.03x |
| offtab-scan-rem | 0.129 | 0.134 | 0.08 | 107 | 2.00x |
| bq-gen | 0.138 | 0.231 | 0.42 | 108 | 1.03x |
| *gen-unsafe-aa-adjacent* | *0.925* | *1.767* | *1.92* | *68* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.950* | *1.948* | *1.09* | *69* | *1.00x* |
| gen-unsafe | 0.952 | 1.846 | 1.46 | 68 | 1.00x |
| gen-quotrem | 0.977 | 1.970 | 0.58 | 68 | 1.00x |
| *list-aa-distant* | *0.998* | *1.001* | *0.28* | *70* | *19.43x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 71 | 19.43x |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.14* | *70* | *19.43x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0301, worst cell
8.13% on `scaled-r5`, and 12 of 18 intervals cover 1. The `sum-only` halves
agree at 0.9990 on a worst cell of 0.30% on `scaled-r5`, its interval
covering 1. The in-situ term reads 1.0103, 1.0148, 1.0057, 1.0177 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0169, which the correction amplifies by 1.99x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h13m45s, peak 125 MiB in use, 54 MiB max residency;
the reader reads 53 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.96 ms per call raw, 4.78 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1,
scaled-r5):** `mut-odo-vecdims` 0.028/0.034/0.034 `bq-scan-rem-gm-mulback`
0.090/0.090/0.094

**Across the halves:** 37 of the 47 arms are faster on this half and 10 slower,
at a geomean of 0.9798, from `mut-odo-vecdims-add-in-leaf` at 0.8757
to `gen-unsafe` at 1.0665, with `list` itself at 0.9931.

**What the class says:** all three properties hold, and this is the class where
the family's margin is smallest. `mut-odo-vecdims` reads 0.034 with `worst`
0.034 --- the two are the same figure, this class's cells being that uniform ---
and `bq-expand` trails it. The head is `mut-odo-vecdims-add-in-leaf-down`
at 0.029, **0.9358 paired and ahead on 3 of 3 shapes, 6.4% against this class's
3.01% floor**, so it clears by a margin rather than by the factor it clears
by elsewhere; a family member again, so the first clause holds. The best outside
the family is `canon-full` at 0.031, against `mut-odo` at 0.037 in Run 19.
**This class carries the run's tightest floor, 3.01%**, where Run 19's tightest
was `revsome` at 2.00% and this class read 3.80%.



## Provenance

What this run's figures have to be read against, and it is a section
of this file because a run replaces every word of it. What does NOT move
with a run --- the delta chain that says which shape set and roster each run
measured, and the list of what a run replaces outside this file --- is [README's
own Provenance][prov].

**Run 20's halves differ in the compiler, as Run 19's did, and the pair
is that pair over a changed roster.** They share source, shim, shim setting,
roster, shapes, class lists, bench order, machine and the one baked RTS line ---
but not their position in the sequence, the control half having run first
in every pair, which aliases *9.12* with *second of the two* again; no order
probe was taken. `cabal.project.ghead`'s freeze resolves the same `vector`,
`criterion` and `criterion-measurement` at the one index-state the other two
plans hold, so what differs is ghc-9.12.4 against GHC HEAD 10.1.20260803
and their boot libraries, `ghc-internal-9.1204.0` against
`ghc-internal-10.100.0`. `.text` is 20451525 against 20596543 bytes, each 45056
B above its Run 19 counterpart, and every address after the first difference
moves: `--library` puts **11.1%** of library self-loops at the same offset
in their cache line and **77.1%** in the same straddle state --- Run 19's two
figures to the digit, one compiler pair over one set of libraries. **The tracked
`Main` fill groups do not keep their shapes**, as Run 19's did not: a six-copy
group at `[0, 0, 24, 0, 0, 24]` and a two-copy group at `[0, 0]` on the basis
against a six-copy group at `[10, 31, 0, 1, 2, 0]`, a three-copy group
at `[0, 0, 13]` and a two-copy at `[0, 0]` on the control. Which arm owns which
copy on HEAD is a `-g3` twin's to say and Run 19 established the twin cannot say
it there, so none was built and the note records bare offsets. **What does
NOT transfer between these halves is a difference of absolutes**: `list` moved
**0.71%**, past the 0.7% bar by a hair, where Run 19 read 0.78%.
**The correction sits evenly on both**, the in-situ forcing term reading
1.0266/1.0341/1.0701 against 1.0298/1.0214/1.0655 as medians, so a ratio read
within either half carries almost none of its own.

**The sequence was launched once, ran to the end, and two of its populations
were then rerun in a second window.** Eighteen processes ran 02:56:06
to 10:35:11, every one exiting 0 with the bench count its roster asked for ---
1272 twice, 212 four times and 159 twelve times --- and the wall-clock log
closes with `major run complete`. Four of the eighteen were superseded
by the reruns, so fourteen of that window's processes are the ones this file
publishes. **The machine's owner came back to it during the last four**,
and `window` and `scaled` on both halves reported 71, 54, 134 and 131 benches
at or above 0.25 foreign CPU, worst sample 1861 ms; the plateau gate saw
the same event as an 8.72% spread against a 5% band. Those four were rerun
11:47:46 to 12:42:56 on a quiet box, each exiting 0 at 159 benches
with its `@@saturate` stamp and each reporting no bench reaching 0.25 foreign;
the four they supersede are excluded from the published set. **The other
fourteen processes are clean** and both main sets are among them. The plateau
over the fourteen kept processes and the four reruns now reads 19.8303
to 20.6757 ms, a **4.26%** spread. **The control half ran first throughout**,
`ghead` before `g912` on the main set and on each class, which the reruns kept,
so every class's cross-half direction is aliased with its slot. **The tree
was NOT clean at launch**: the driver's own `git status` recorded three
untracked paths, `micro-regime3/check-x.log`, `probe-counts-table.txt`
and `probe-run20arms.sh`, none in the run's namespace and none modified source.
**The alone-leg riders followed**, four invocations of 27 single-bench
processes, 108 in all, clean and saturated on each half, each invocation
recording a box 0.2% to 0.4% non-idle. **The counted-work sweeps followed
them**, both halves over every population, 5300 cells and no cell perf refused.

**The pair's own identity, transcribed before its note goes with it.** The two
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
`d415f38a75`, reporting 10.1.20260803 and unmoved since Run 19 was built. A HEAD
that moves is a different compiler and a different pair. **No input moved
that a freeze does not record**: the box is where Run 19 left it, its machine
check reading -0.24%, so absolutes cross freely from Run 19 and the boundary
that stops them is still the BIOS change before Run 18.

**The roster moved and nothing else in the inputs did**, which is this run's one
departure from what a compiler pair wants: 1272 benches, 53 timed arms
over the same 24 shapes, six classes at three shapes and two at four,
and the same roster order, with both halves' `--list` listings identical to each
other and NOT to `run19-g912`'s 1128. Nine timed arms landed --- the leaf
block's three and the rework's five with its forcing control --- and three
dropped to `Only`, and two class shapes joined. **So the `-L1` roster pass
was owed and was taken**, on this roster, before the gate: 1272 benches
over the main set and a three-shape class beside it, every reader mode exercised
over both. **What the change costs is stated wherever a figure crosses the Run
19 boundary**: new functions move every address, so no cross-run figure here
is drift alone, and the pinning claim was read at the build and killed
on exactly that.

**The anchor, so a moved baseline is visible** --- and two of this run's three
move by well under its floor while the third does not, on a build whose every
address moved. Every published figure is a ratio to `list`, so a change
in `list` alone would move every cell without any strategy moving. The three
anchors read **5.94 us** on `cnn-slice-c32`, **3.09 ms** on `cifar-L2-16-c64-k3`
and **38.2 ms** on `stretch-wide-2xM`, net per call on the basis half, against
Run 19's 6.08 us, 3.10 ms and 38.3 ms --- **-2.18%, -0.12% and -0.40%**, derived
from the cells rather than from the printed three figures. The first is past
this run's 1.51% floor and the other two are well inside it; it is also
the smallest shape in the set, and the gate's machine check over all 24 shapes
read -0.24% with a worst of +3.07%, so the box is flat and the movement
is the roster change's layout term showing on the shape least able to absorb it.
**The control half's three are 5.91 us, 3.07 ms and 36.8 ms**, 0.52%, 0.70%
and 3.59% under the basis's --- the compiler IS in this movement, which
is the same fact as `list` moving 0.71% between the halves and is why these two
columns are ordered rather than differenced.

| shape | `l` | `list`, per call | net | HEAD, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.12 us | 5.94 us | 5.91 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.18 ms | 3.09 ms | 3.07 ms |
| `stretch-wide-2xM` | 1800000 | 39.3 ms | 38.2 ms | 36.8 ms |

**Each stride class carries an anchor of its own, beside its table, and all
eight are inside their own class's floor against Run 19 --- seven of them inside
a point and a half.** They run **-1.39% to -0.05%** on seven,
`window-224x224-k3` at the far end and `slice-primes` at the near one, every one
inside its class's floor and six of the seven inside a point. **`bcastmid-b200k`
is the exception at +3.93%**, against that class's 4.83% floor --- inside it,
but the only class anchor past a point in either direction, and the class whose
population went from three shapes to four between the runs. So a class anchor
is comparable across this boundary, with the caveat every cross-run figure here
carries: the roster moved, so a movement is drift plus a layout term
and not drift alone. What they cannot be compared across is still the Run 17
boundary, where the BIOS sits.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is **0.596--0.613 ns per element** on the basis half
and 0.595--0.614 on the control, over all 24 shapes, so a raw slope
is the published one plus about `0.61e-9 * l`, with `l` from `Main.hs`.
That recovers any uncorrected figure to within the term's own spread --- enough
to hold a corrected run against any number measured before the correction
existed. The term is within about 2% of every run's since Run 7, so neither
the flag, the roster, the layout, the shim's padding, `-fproc-alignment=64`,
an RTS line, a source patch that moves every loop offset, **nor a change
of compiler** touches the forcing pass, which is the control saying every run's
correction is one correction --- and this pair's two halves agree on
it to within a thousandth of a nanosecond, so a figure differenced across
these halves carries almost none of its own. **This run adds a fourth arm
to the control that reads it**, `canon-full-nosum`, whose write pattern varies
by shape where the three standing ones are element-wise fills: it reads 1.0267
and 1.0239 of `sum-only` against the others' 1.0266 to 1.0701 and 1.0214
to 1.0655, so the hole the sum-only section names --- a fill whose write pattern
leaves the cache in a quite different state being summed at a cost `sum-only`
misses --- is not open on the one arm built to look for it.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance
