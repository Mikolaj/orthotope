# Run 21 (SpecConstr)

One run's write-up: its head, its Results, what the next run compares against,
the claims that run should test, the nine class blocks, and its own Provenance.
A run replaces this file whole and edits [README.md](../README.md) around it,
in the score of places [the replace list under Provenance there][prov] names ---
the open list among them, which is where a run's registrations, verdicts
and surprises go rather than here. So this file is most of what a run replaces
and by no means all of it. What stands between runs is the harness, [the
procedure][procedure] that makes a file like this one, and the rulings
a measurement does not reach.

**Run 21 (SpecConstr), and what the branch's two-stage rework costs where
it cannot canonicalize.** Criterion, **`--ghc-options=-fspec-constr`**; Run 20's
regime, recipes and basis, and **what moved is the roster and the shape set**:
1176 benches, 49 timed arms over 24 main-set shapes, and 1617 more over 33 class
views in **nine** classes, where Run 20 ran 53 arms, 1272 and 1378 over eight.
Six timed arms landed --- `mut-odo-vecdims-add-in-leaf-u2-down`,
the library-shaped `lib-stage1`, `lib-stage2` and `lib-stage2-concat`,
and the list-consumer `liblist-stage1` and `liblist-stage2` --- and ten names
left, eight arms parked permanently together with `offtab`'s two A/A twins,
so the floor reads over **sixteen** pairs from this run on. The new `runs` class
is seven regime-2 views sweeping run length from 2 to 65536 at `l` of about 1.8M
throughout, and it is the population the rework's own question needed.
**The basis is the 9.12 half**, `run21-g912`: Run 20's basis recipe with only
the source moved, so it carries `-fobject-determinism`, the per-sample
instrument and the saturating preamble, and both halves ran
under `WILDLOG=1 SATURATE=1`. **The control is `run21-ghead`**, the same source
and the same shim built by the in-tree stage1 of the GHC checkout
at 10.1.20260803 through `cabal.project.ghead`, whose freeze resolves the same
`vector`, `criterion` and `criterion-measurement` at the one index-state
the other two plans hold --- so the halves differ in the compiler and its boot
libraries and in nothing a freeze can see, and what they price is a consumer's
build on GHC HEAD, library code recompiled included. The binaries carry
`ghc-internal-9.1204.0` against `ghc-internal-10.100.0`, criterion 1.6.5.0
on both, and `.text` of 20488389 against 20637503 bytes. md5
`80f1dae4493b44cffd38ea30f78095ab` for the basis
and `248f599a0579f8e06913b7ca6895192e` for the control, from `Main.hs`
at `70ef2de` and `align-as.py` at `40f7a37`; the tree at launch was `ec45334`,
with eight untracked scratch paths and nothing modified. The same desktop, Zen
3, a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main
processes read *1h41m24s* and *1h41m49s*, at *296 MiB* in use and *130 MiB* max
residency on the basis against *286 MiB* and *125 MiB* on the control.

**The basis half is not a repetition, and this run gave up that instrument
on purpose for the second time running.** Six timed arms landed since Run 20
was built and ten names left, so every address moved and neither half can
reproduce its Run 20 counterpart byte for byte; the md5 comparison
and the three-read hunt a moved md5 usually triggers were both taken off
for this run, decided 2026-08-28, so a differing md5 here is what the roster
change predicts and not a finding. The build-time reading of the fills says how
far the addresses went: `run20-g912` held its six-copy group
at `[0, 0, 24, 0, 0, 24]` and `run21-g912` holds one at `[0, 0, 24, 0, 0, 8]`,
no tracked address surviving and none moved by a constant --- which is Run 20's
killing of the pinning claim in its strong form, repeated over a roster change
that both adds and removes.

**What holds the build to something instead is three readings that survive
a relink.** The gate's machine check reads **-0.33%** on `list`'s net against
the fingerprint Run 20 kept, over 24 of 24 shapes, worst `stretch-pow2stride`
-3.52% and none past 5% --- inside 3%, so the box measures as it did
and no absolute is re-baselined. The 37 arms both halves and Run 20 all give
a corrected time read against Run 20's columns, with the caveat the roster
change puts on them: a layout term nothing here separates, which Run 10 priced
at 12 to 14% on the two arms whose loop the shim rescues. And each half's own
sixteen A/A pairs give it a floor. **The counted work is the fourth and
it is the strongest of them**: `bq-odo-gm-mulback` reads a count ratio
of **0.9340** where Run 20 read 0.9340 and Run 19 read 0.9340,
and `bq-scan-rem-gm-mulback` **0.9422** against 0.9423 --- four figures
and three figures across two roster changes, on an instrument that owes
criterion nothing.

**The manifest's one surviving claim held on both compilers, and the set is now
a single ladder.** Claim 1's five links all hold on the 9.12 basis --- 0.6463,
0.9154, 0.9168, 0.9169 and a tie at sign p 0.84 --- and all five hold on GHC
HEAD at 0.6466, 0.9066, 0.8670, 0.8810 and a tie at p 0.31: no BROKE on either
half, a fourth clean sweep running. Claims 2 and 6 retired on 2026-08-28
with the parking of `offtab` and `gen-quotrem`, the arms their only surviving
links turned on, so what was thirteen orderings through Run 19 and eight at Run
20 is five links of one claim here. Claim 7 stays unmanifested prose and is read
below; claim 8, prose too, retired on 2026-08-29. **What the ladder does not see
is the same thing Run 20 said it does not see, and this run widens it**: claim
1's top rung reads `mut-odo-vecdims` against `mut-flat-gm`, and seven arms now
read below `mut-odo-vecdims`, four of them inside its own family, so the rung
understates what a mutating method buys. Re-aiming it is a decision and
not a reading, and it is [under the recommended
tasks](../README.md#recommended-tasks-after-run-21).

**What the compiler is worth, arm by arm, stopped being one-sided, and
that is this run's plainest movement.** Over the 43 arms compared, 19 sit within
1% of 1 at a geomean of **0.9920**, **22 below and 21 above** --- where Run 20's
pair read 0.9844 at 30 below and 17 above over 47 arms, and Run 19's 0.9836
at 30 and 12. So HEAD is now under a point behind this roster and no longer
behind it everywhere; the split is even. What did not change is which arms move
and by how much. **`mut-odo-vecdims-add-in-leaf` heads the movers again
at 0.8481**, where Run 20 read 0.8513, and the two fastest pure builds follow
with their A/A twins, `bq-odo-gm-mulback` at 0.9314, 0.9302 and 0.9322
and `bq-scan-rem-gm-mulback` at 0.9463, 0.9449 and 0.9468. **What is new
at the other end is the rework's arms, and they lean the other way**:
`canon-full` reads **1.1241**, `lib-stage2-concat` 1.0799 and `lib-stage2`
1.0715, so HEAD is materially *faster* on the branch's own driver than 9.12 is.
**A whole family moving with its own A/A twins is the shape to read** --- a twin
is that arm's code at another slot, so three copies moving together is the arm
and not where one of them landed --- and both `-gm-mulback` families again read
within two thousandths of their twins, as they did on Runs 19 and 20.

**This run's floor is 2.92% on the basis half and 2.16% on the control**,
against Run 20's 1.51% and 1.18% --- so both ends roughly doubled, on the same
two recipes and the same box, with the roster the only input that moved between
the runs. The pairs carrying it are `mut-odo-aa-distant` on the basis
and `gen-unsafe-aa-distant` on the control, and the worst A/A cell of either
main set is **22.86%** on `vgg-14-c512-k3` on the basis against **14.47%**
on `stretch-inner1` on the control, where Run 20 read 13.66% and 16.22%.
Restricted to the six pairs that carry back to Run 10 the two read **0.46%**
and **0.60%**, against Run 20's 0.44% and 0.28% --- so the tight six are where
they have been on the basis and have loosened on the control, and most
of the movement is again in the ten outside them. **Which of the two a margin
is judged against depends on what it compares**: an arm against its own
duplicate against 2.92% and 2.16%; two different arms against the six-pair
figures. Neither is judged against the predecessor's, and this run is a plain
demonstration of why --- a floor that doubles between two runs of one recipe
is not a property anything inherits.

**The two halves' cells resolve differently again, and this run the lean is back
the way Run 19 had it.** `CI%` --- the median half-width of a cell's own fit ---
runs a geomean of **1.02** on the basis against the control across the roster,
34 arms wider here and 15 narrower, where Run 20 read 0.97 at 21 wider and 32
narrower and Run 19 read 1.06 at 26 and 21. So the direction has now gone one
way, the other, and back, over three runs of the same pair of compilers, which
is what a quantity with no stable sign looks like. It remains a different
quantity from the floor: sampling error inside one bench against agreement
between two placements of one strategy, and this run has the basis carrying both
the wider floor and the wider cells, where Run 20 had them split.

**No wild cell, no intrusion, and one unbroken window --- which is what Run 20
could not say.** The sequence ran from 23:31 to 07:35 on a box its owner had
handed over, every one of the twenty processes exiting 0 at the bench count
its roster holds, and none reporting a bench at or above 0.25 foreign CPU.
The plateau gate reads the same event from the other end: all twenty processes
assert their preamble victim inside **19.70 to 20.55 ms/iter, a 4.30% spread**
against a 5% band, so every process measured in the same in-process state.
So no population was rerun and post-run step 1c is owed nothing, where Run 20
had to rerun `window` and `scaled` on both halves. **The class floors moved
and they did not move together**: on the basis half the widest is `rev`'s
**8.95%** and the tightest `scaled`'s **3.30%**, where Run 20 read `reshape1`
at 8.31% and `scaled` at 3.01%. So the tight end did NOT change hands ---
`scaled` holds it for a second run, three tenths of a point looser --- while
the wide end did, `rev` going from 4.14% to 8.95% and `reshape1` from 8.31%
to 6.31%. The new class lands second tightest at 3.50%, between `scaled`
and `slice`'s 3.55%, which is the floor being a property of the run said once
more at class scale.

**The rework is what this run was built to price, and the answer is a boundary
in run length rather than a verdict on the branch.** `lib-stage1` is stage one
as it shipped --- regime 1 the vector or a slice, regime 2 one slice per maximal
normal suffix and a concatenation, regime 3 the `genericFillStrided` fill ---
and `lib-stage2` is the branch, which canonicalizes and then fills everything
left, contiguous runs included. The two therefore differ on exactly two
populations' worth of work, and they differ in opposite directions. **On regime
3 the branch is a plain regression against what ships**: `lib-stage2` against
`lib-stage1` reads **4.0152** on `rev`, 4.5377 on `revsome`, 4.0984 on `slice`,
4.0765 on `scaled`, 3.7237 on `window` and **2.4323** on the main set at 1 of 24
shapes and sign p 3e-06, 2.2588 on HEAD, these being factors where their
populations' floors are 3.3 to 9.0 percent, so nothing here is near the floor
and no arithmetic against it is worth doing; and each within 8% of its HEAD
counterpart. That is the condition registration 4 named as the regression
this benchmark now exists to catch, and it fired: on a view that will
not canonicalize, stage one falls through to the shipped fill and the branch's
`fillStage2` is two-and-a-half to four-and-a-half times slower than it, the main
set at the near end and `revsome` at the far one. **On regime 2 the branch
is a large win and a large loss at once**, and the `runs` class was built
to find where they cross. `lib-stage2` / `lib-stage1` reads 0.0854, 0.1529,
0.4626, 2.8823, 5.2058, 6.4790 and 5.6810 across `runs-2`, `-3`, `-9`, `-96`,
`-1024`, `-65536` and `-r3-48x30` on the basis, and 0.0821 to 6.2086 on HEAD ---
**so the crossover falls between `runs-9` and `runs-96`, exactly where
it was registered**, and the kill condition for that registration was that stage
two not be behind past the floor at 96, 1024 and 65536, which it is by factors
of 2.9, 5.2 and 6.5. **The two broadcast classes are where the branch's
conditions earn something, and only one of them earns enough**: `bcastmid` reads
0.8648, stage two ahead by 13.5%, while `bcast` reads 1.2496 --- still behind,
though by a quarter rather than by the fourfold the regime-3 classes report.

**What the run-length sweep exposes is not the branch's fault, and this
is the finding under the finding: the SHIPPED route is the pathological one
at short runs.** Read as ratios to the `list` baseline each arm exists to beat,
`lib-stage2` is flat --- 0.1140, 0.1479, 0.1527, 0.1550, 0.1564, 0.1580, 0.1528
--- and cares nothing for run length, while `lib-stage1` runs **1.3346, 0.9672,
0.3301, 0.0538, 0.0300, 0.0244 and 0.0269**. So at `runs-2`, which is 900000
runs of two elements, stage one's slice-per-run concatenation is **a third
slower than doing nothing at all**, and at `runs-3` it barely breaks even; only
from `runs-96` up does it become the right route --- at `runs-9` stage two
is still ahead, 0.4626 of it, and by `runs-65536` it is six times better
than the branch's fill. **That reverses the reading of the repair candidate.**
`lib-stage2-concat` --- stage two with canonical contiguous runs sent back
to one slice per run --- restores stage one's figure at every length, 1.0027,
0.9893, 1.0584, 1.0185, 1.0046, 0.9961 and 1.0044 against it, which is what
registration 1 predicted and what makes it a faithful repair of the long-run
loss. But restoring stage one's figure at `runs-2` means restoring **1.3382**,
so the candidate buys back the long runs by giving up a twelvefold win
at the short ones. Neither arm is the answer on its own, and what the class puts
on the table instead is the run-length condition registration 1 already named
when it asked the same question of `canon-memcpy-r2` against `canon-vecdims`:
fill the short runs, copy the long ones, and the crossover this class measures
is between 9 and 96.

**The counted-work instrument cuts this pair's movements in two,
and it reproduces the previous two runs to four figures.** `run-counts.sh`
counts instructions an iteration from two fixed-`-n` processes a cell and owes
criterion nothing; `--counts` reads a pair of those files beside `--compare`.
**What is codegen**: the fast pure tier's whole loss, a third time.
`bq-odo-gm-mulback` reads a count ratio of **0.9340** against its time ratio
of 0.9314 and `bq-scan-rem-gm-mulback` **0.9422** against 0.9463, leaving
time-over-counts at 0.9972 and 1.0043 --- where Run 20 read 0.9340 and 0.9423
on the counts and Run 19 read 0.9340 and 0.9422. HEAD emits about 7% and 6% more
instructions for these two, on three runs and two roster changes. **What
is not codegen**: the placement-exposed family, at count ratios of **1.0000**
to four figures on `build`, `mut-odo` and `gen-unsafe` --- the three of the six
that survive the parking --- exactly as Runs 18, 19 and 20 found them, so their
time movements, 0.53% on `gen-unsafe` through 3.44% on `mut-odo` to 5.15%
on `build`, are layout or the runtime and not code. **And the rework's arms
are a third thing again.** `canon-full` moves 12.41% in time at a count ratio
of **0.9712**, leaving time-over-counts at 1.1574 --- the run's largest residue
by a wide margin and the opposite sign to `mut-odo-vecdims-add-in-leaf`, which
reads 0.8971 on the counts against 0.8481 in time, about ten points
of its fifteen being HEAD emitting more instructions and the remaining five not.

**The counted work covers every population, and the class picture is the one Run
20 drew.** Eighteen sweeps, both halves over all nine classes, 147, 196 or 343
cells apiece and no cell perf refused anywhere in the twenty files. **Eight
of the nine read as the main set does** --- every arm together at a count
geomean of 0.9852 to 0.9934, HEAD emitting about a percent more --- while
**the ninth sits apart at 0.9990**, near enough to 1 that HEAD and 9.12 emit
almost the same instructions across that whole class. That ninth is `reshape1`,
as it was Run 20's eighth at 0.9995 against its seven at 0.9860 to 0.9918,
so what Run 19 read as an inversion and Run 20 read as flat is flat again:
`reshape1` is the class HEAD does not cost, on three runs. `window`
is the runner-up at 0.9934, as it was at 0.9918. **These nine are taken the way
Run 20 took its eight** --- the geomean over every arm the counts sweep carries,
controls included, which is 49 here and was 53 there --- so the two runs'
figures are commensurable and Run 20's reproduce from its own artifacts
to the digit. A geomean over the 43 arms `--counts` PRINTS is a different
number, `reshape1` reading 0.9996 that way, and the two must not be mixed.
**The most extreme arm is the same one in all nine classes and it is the same
one Run 20 named**: `mut-odo-vecdims-add-in-leaf`, from 0.8653 on `runs`
to 0.9286 on `reshape1`, where Run 20 read 0.8694 on `bcast` to 0.9286
on `reshape1` --- the same arm, the same top of the range to four figures,
over a roster change.

**The unit-innermost-extent rule was registered as a mechanism claim,
and a second run has now declined to kill it.** Wherever `sInner` is 1,
`bq-odo-gm-mulback`'s HEAD penalty is absent: `stretch-inner1` reads **1.0000**
on the counts, to four figures, as it did on Run 20. Everywhere else it runs
**0.9149 to 0.9701** --- the identical range Run 20 published --- and the far
end of it is again `stretch-rank12` at `sInner` 2, the one shape between absent
and the band, which is what a graded effect looks like rather than a switched
one. Run 19's kill condition was any `sInner` of 1 that shows the penalty,
and none does. What this still is not is a reading of the code, so the claim
stays registered rather than settled.

**And the correction sits on nearly the same footing in both halves, as it has
on every run since Run 17.** The in-situ forcing term --- an arm minus
its `-nosum` twin, against the `sum-only` the correction actually subtracts,
and read here off `--aa`'s `ratio` column where each class block below prints
its `median` one, so the two are not the same statistic under the same phrase
--- reads 1.0243, 1.0204, 1.0043 and 1.0768 on the basis and 1.0256, 1.0198,
1.0325 and 1.0677 on the control --- the reader's `ratio` column, which
is the figure Run 20 published and called a median, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm` and `bq-expand`. So both halves subtract a term
between about half a point and eight points under the in-situ pass, every one
of the eight figures tilting the same way, and the two halves agree with each
other to within 0.13, 0.06 and 0.91 of a point on `mut-odo-vecdims`,
`canon-full` and `bq-expand`. `mut-flat-gm` is the one where they part in SIZE
rather than direction, 1.0043 against 1.0325, and it is the arm whose in-situ
term is noisiest on both halves --- its `mean|d|` reads 4.88% and 6.72% against
3.03% and 3.04% on the fix. **A margin between these two halves is therefore
not carrying a correction bias**, which rests on the term the correction
actually subtracts rather than on the in-situ check: the two `sum-only` halves
agree at 0.9996 on the basis and 0.9999 on the control, both intervals
covering 1.

**The run's standing placement pair moved, and this time the fills say what
it is not.** `build` against `mut-odo`, one worker at two slots, reads **0.9870
at 14 of 24, sign p 0.54** on the basis --- a tie --- and **1.0764 at 7 of 24, p
0.064** on HEAD, where Run 20 read 0.9899 and 0.9668 and Run 19 read 0.9633
and 0.9325. So the sign on HEAD has reversed: `build` was the faster slot there
on both previous runs and is 7.6% the slower one here. Their per-shape ranges
remain the finding rather than their geomeans, **0.866..1.076** on the basis
and **0.934..1.212** on the control. **What makes this run's reading sharper
than its predecessors' is that `mut-odo`'s own A/A twins moved with it,
and in opposite directions on the two halves**: both twins read below the base
on the basis, 0.9642 and 0.9620, and both read above it on the control, 1.0129
and 1.0081 --- so `mut-odo`'s base slot is the slow one on 9.12 and the fast one
on HEAD, and the pair above is reading that rather than anything about the two
workers. **And the tracked fills rule out the obvious explanation.** Post-run
step 11 named the two-copy group off a `-g3` twin: it is `fbBuild`
and `fbMutOdo`, and on both halves both copies sit at offset 0 in their cache
line. So whatever separates these two slots on this run, it is not where
the tracked loop landed --- which is a narrowing of [the standing open
question][open] and not an answer to it. The counted work agrees it is not code:
both arms read a count ratio of 1.0000 to four figures.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512`
on the basis, and 2408978 against 2408530 on the control, where plain -O1
separates the two tenfold. Those are Run 20's three figures to the byte.
On the confirm-don't-rebuild path this run took, with no build to have carried
the flag, that is the only check standing between a mistyped regime
and the hours.

**Run 21 records every population twice** --- the main set and all nine stride
classes from each half, one process each, which is what makes its class readings
a pair rather than a basis alone --- **and all twenty came out of one window**,
which Run 20 could not say. They ran unbroken from 23:31:03 to 07:35:03, 8h04m:
1176 benches twice, 343 twice for the new `runs` class, 196 four times
for the two four-shape classes and 147 twelve times. Every one exited 0
at the bench count its roster holds and no process reported a selection it did
not ask for. The eighteen class processes span 12m41s to 29m53s, the two `runs`
processes accounting for the whole top of that range at some 30 minutes each ---
the note predicted they would be the longest of the run, and they are, by twelve
minutes over the next. **The control half ran first throughout**, `ghead` before
`g912` on the main set and on each class in turn, which is the driver's order
--- so *the 9.12 half* and *the second process of the two* again name the same
ten processes, and this run took no order probe to separate them, as Runs 19
and 20 took none. **The alone-leg riders followed the sequence** rather
than sitting inside it, 108 single-bench processes over four invocations of 27
--- the 24 shapes plus a second reading of the three anchors, each half clean
and saturated, which is the pair of columns the decomposition needs. Each rider
invocation recorded the machine it launched on, 0.1% to 0.5% of the CPUs
non-idle.

**The decomposition reproduces on both halves for a third run, and the roster's
own share came in under half a point on each.** The riders time each shape's
`list` by itself, one bench per process on that half's own binary, `SAT=` off
and on, and the saturated legs split the deflation into the state the preamble
puts on a clean process --- **+11.84%** on the basis and **+12.02%**
on the control --- and the rest the roster adds on top of it, **+0.12%**
and **+0.50%**. Run 20 read +12.27% and +13.27% for the state and +0.66%
and +0.29% for the rest, and Run 19 read +11.73% and +12.57% and +0.31%
and +0.72%, so the state term has now reproduced across three runs and two
roster changes inside a point and a half, while the roster's own contribution
has stayed under a point on every half of every run that measured it. **The two
tails are the same shape on both halves and it is the shape Runs 19 and 20 both
named**, `stretch-tall-Mx2` at 1.0944 and 1.0956 against Run 20's 1.0999
and 1.1301 --- a roster effect on one shape rather than a term belonging
to either compiler, now on three rosters. Both readings are raw slope against
raw slope, an alone leg carrying no `sum-only` bench to correct with,
so no correction convention enters either.

**Everything in this file is replaced by the next run, which is what makes
it a file.** What a run replaces OUTSIDE it, in README.md and in the sources,
is [README's own Provenance](../README.md#provenance). None of it is portable:
a run on another machine is a different measurement rather than a repetition,
which Run 19 was in a position to be firm about, having repeated one binary
on one box and moved its floor by 1.7x. This run cannot repeat
that demonstration and does not try --- its roster moved again, so neither half
reproduces a predecessor byte for byte --- and it makes the weaker half
of the same point a second time: the floor rose from 1.51% to 2.92% on one
recipe, one box and one regime, with only the roster between them, having fallen
from 2.32% to 1.51% over the previous such step. A quantity that moves
by a factor of two in each direction over two roster changes is not a property
any run inherits from the one before it.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries
that decision and this run's re-pass of its gates), the scratch vectors
are the unboxed ones the shipped code uses, as they have been since Run 7 ([the
scratch vector flavour](../README.md#the-scratch-vector-flavour) says what
that severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under. **A row's distance from Run 20's basis
column is NOT drift alone, and this is the second run running that has to say
so.** Six timed arms landed and ten left, so every address moved between the two
builds --- the build-time fill reading found no tracked address surviving
and none moved by a constant --- while the flag, the shapes, the order,
the allocation area, the box and the recipe are all the same ones. Run 10 priced
a reorder at 12 to 14% on the two arms whose loop the shim rescues. So read
a distance from Run 20's column as drift PLUS a layout term this run cannot
separate, and prefer the within-run comparisons for anything that has
to be decided. This pair's halves differ in the compiler, so they differ
in layout by construction too; there the counted-work instrument does separate
them, and the table's cross-half distances are read as codegen where the counts
moved and as placement or runtime where they did not.

**And it is the basis half's**, `run21-g912`, as every published table here
is from Run 11 on: the control half's column is one column on the yardstick
below rather than a second copy of these forty-odd rows. That the published half
is the 9.12 one is this pair's own decision --- it keeps the lineage, being Run
20's basis recipe with only the source moved --- and the HEAD half
is the yardstick column. **Six rows here are first readings**: `lib-stage1`,
`lib-stage2`, `lib-stage2-concat`, `liblist-stage1`, `liblist-stage2`
and `mut-odo-vecdims-add-in-leaf-u2-down`. A first reading has no predecessor
to be drift against, so nothing in this file compares one to an earlier column,
and the registrations they answer are [in the open
list](../README.md#what-is-open).

**Comparing runs?** The table below is Run 21's own; what to hold a new run
against is [What the next run compares
against](#what-the-next-run-compares-against), the claims to test are [the ones
after it](#the-claims-the-next-run-should-test), the absolute anchor
is under [Provenance](#provenance) below and the population it was measured
over in [README's delta chain](../README.md#provenance), and this run's own
floor --- no A/A pair further than 2.92% from 1 on the basis half or 2.16%
on the control, on worst single cells of 22.86% and 14.47%, and 0.46% and 0.60%
read on the six pairs that carry across runs --- is [in the floor
section][floor]. The sixteen-pair figure governs an arm against *itself*; what
two different rows of the table below must clear is the SIX-pair one, 0.46%
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
| *bq-expand-nosum* | *--* | *--* | *0.54* | *79* | *2.35x* | *its base arm, forced with one element* |
| *canon-full-nosum* | *--* | *--* | *0.56* | *102* | *1.00x* | *the same, on a write pattern that varies by shape* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.76* | *91* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.50* | *92* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *101* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *101* | *0.00x* | *the same, at the other end* |
| mut-odo-vecdims-add-in-leaf-down | 0.036 | 0.121 | 0.60 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf | 0.036 | 0.121 | 0.57 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf-u2 | 0.038 | 0.128 | 0.60 | 88 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| lib-stage1 | 0.039 | 0.129 | 0.59 | 88 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.039 | 0.133 | 0.62 | 88 | 1.00x | new mutating `Vector` method |
| canon-vecdims | 0.049 | 0.125 | 0.67 | 94 | 1.00x | new mutating `Vector` method |
| canon-full | 0.053 | 0.125 | 0.61 | 94 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.054 | 0.125 | 0.57 | 80 | 1.00x | new mutating `Vector` method |
| canon-memcpy-r2 | 0.054 | 0.125 | 0.69 | 94 | 1.00x | new mutating `Vector` method |
| **mut-odo-vecdims** | **0.054** | 0.125 | 0.54 | 80 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa* | *0.054* | *0.126* | *0.57* | *80* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.126* | *0.42* | *80* | *1.00x* | *A/A control* |
| liblist-stage1 | 0.055 | 0.156 | 0.94 | 84 | 2.00x | new mutating `Vector` method -- stage one at the list entry point |
| mid-copy | 0.055 | 0.125 | 0.73 | 80 | 1.00x | new mutating `Vector` method |
| bcast-set | 0.057 | 0.125 | 0.68 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.084 | 0.189 | 0.75 | 82 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.092 | 0.195 | 0.75 | 80 | 1.33x | mutable `Int` scratch |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.154 | 0.63 | 74 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.099* | *0.157* | *0.66* | *74* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.157* | *0.35* | *74* | *1.33x* | *A/A control* |
| bq-odo-gm-mulback | 0.100 | 0.178 | 0.44 | 79 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-adjacent* | *0.100* | *0.177* | *0.47* | *79* | *1.51x* | *A/A control* |
| *bq-odo-gm-mulback-aa-distant* | *0.100* | *0.178* | *0.50* | *79* | *1.51x* | *A/A control* |
| *mut-odo-aa-adjacent* | *0.103* | *0.264* | *1.97* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-distant* | *0.104* | *0.261* | *1.90* | *70* | *1.00x* | *A/A control* |
| bq-expand-gm-mulback | 0.104 | 0.225 | 0.68 | 79 | 2.35x | nothing (pure) |
| build | 0.104 | 0.273 | 1.32 | 71 | 1.00x | new mutating `Vector` method |
| *build-aa-adjacent* | *0.105* | *0.271* | *1.69* | *71* | *1.00x* | *A/A control* |
| *build-aa-distant* | *0.107* | *0.291* | *1.41* | *71* | *1.00x* | *A/A control* |
| mut-odo | 0.107 | 0.270 | 1.63 | 70 | 1.00x | new mutating `Vector` method |
| *bq-expand-aa-adjacent* | *0.115* | *0.230* | *0.56* | *74* | *2.35x* | *A/A control* |
| bq-expand | 0.115 | 0.230 | 0.61 | 74 | 2.35x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.115* | *0.231* | *0.42* | *74* | *2.35x* | *A/A control* |
| offtab-scan-rem | 0.132 | 0.222 | 0.68 | 72 | 2.00x | nothing (pure) |
| lib-stage2 | 0.140 | 0.203 | 0.51 | 78 | 1.00x | new mutating `Vector` method -- the branch's driver |
| lib-stage2-concat | 0.141 | 0.206 | 0.66 | 78 | 1.00x | new mutating `Vector` method -- the branch's driver, runs sent back to a concat |
| liblist-stage2 | 0.154 | 0.257 | 0.72 | 76 | 2.00x | new mutating `Vector` method -- the branch at the list entry point |
| *list-aa-distant* | *0.999* | *1.010* | *0.31* | *35* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.36 | 35 | 23.50x | -- |
| *list-aa-adjacent* | *1.002* | *1.025* | *0.33* | *35* | *23.50x* | *A/A control* |
| *gen-unsafe-aa-distant* | *1.152* | *3.255* | *2.52* | *39* | *1.00x* | *A/A control* |
| gen-unsafe | 1.160 | 3.324 | 2.43 | 38 | 1.00x | -- |
| *gen-unsafe-aa-adjacent* | *1.163* | *3.271* | *2.36* | *38* | *1.00x* | *A/A control* |

`concat-runs` has no row, and neither do the other 36 arms the roster holds
and checks without timing --- 37 of its 86 in all, the parking of 2026-08-28
having moved eight of them from timed to checked: the reason is at each entry
and the count is [`--lint`'s](../README.md#the-reader-read-runpy). So a movement
below is a movement only on the 37 arms this run and Run 20 both give
a corrected time --- 43 names are shared, but six of them are `sum-only`
and `-nosum` controls with no corrected time to move; the six first readings
are named in the section's own opening.

**Three things in the table are the run's findings rather than its numbers.**
**The head of the table moved further from the fix, and seven arms now read
below it.** `mut-odo-vecdims`, the arm decided 2026-08-22, reads 0.054
with seven arms below it --- the three leaf arms at 0.036, 0.036 and 0.038,
`lib-stage1` at 0.039 and `mut-odo-vecdims-add-in-leaf-u2-down` at 0.039,
and the rework's `canon-vecdims` and `canon-full` at 0.049 and 0.053 --- and two
more level with it at 0.054, `canon-memcpy-r2` and `mut-odo-vecdims-add-in`,
which the printed column cannot separate from it. Run 20 had six clear of
it and a seventh level. Every one of the nine needs exactly what the fix needs
--- a mutating `Vector` method and nothing more --- so what the table shows
is still not a new tier but a better member of the tier that already shipped,
now with the shipped library route itself inside it. **The ceiling reproduced
on the arm the class property names**: `mut-odo-vecdims` against
`bq-scan-rem-gm-mulback`, the fastest arm needing nothing at all, reads **0.5424
at 23 wins of 24** and sign p 3e-06 on the basis, against Run 20's 0.5479, Run
19's 0.5572, Run 18's 0.5577, Run 17's 0.5446 and Run 16's 0.5567 --- the figure
[the ruling](../README.md#the-mutable-ceiling-taken) turns on, unmoved
by a second consecutive roster change that moved every address. On HEAD it reads
**0.5164**, against Run 20's 0.5159, at the same 23 of 24 and the same p.
**And the `alloc` column is Run 15's through Run 20's at every level**: five
of the six new arms read 1.00x, the mutable fills' own level, and only the two
list-entry arms sit above it, `liblist-stage1` and `liblist-stage2` at 2.00x.

**The leaf block's internal ordering is this run's sharpest repetition,
and it bears on what ships.** `genericFillStrided` in `Data/Array/Internal.hs`
is a bang-for-bang port of `mut-odo-vecdims-add-in-leaf-u2`, and this run reads
that arm a second time. Against the arm it refines it is emphatic and it repeats
across the compilers: `-u2` / `mut-odo-vecdims` reads **0.7098 at 20 of 24, sign
p 0.0015** on the basis and **0.7043 at 20 of 24** on HEAD, against Run 20's
0.7034 and 0.7022 --- so the shipped code is about thirty percent ahead
of the code it was refined from on both, twice measured. **And it still does
not head its own block.** `mut-odo-vecdims-add-in-leaf-down` reads **0.9440
of it at 19 of 24, p 0.0066** on the basis and **0.9327 at 20 of 24, p 0.0015**
on HEAD --- 5.6% and 6.7%, each outside its half's floor of 2.92% and 2.16%,
and in the same direction on both compilers, where Run 20 read 0.9489
and 0.9389. That is now two runs agreeing, on two rosters, that the variant
which is not shipped is the faster one. **The third member is the one that does
not carry, again**: `-add-in-leaf` reads 0.9513 of `-u2` on the basis
and **1.1236** on HEAD, at 20 of 24 and 3 of 24, against Run 20's 0.9598
and 1.1267 --- so it wins on 9.12 and loses by more on HEAD, twice, and nothing
here recommends it. **What is new is the cost of the dispatch around the fill**:
`lib-stage1`, which is that same fill reached through the library's own regime
test, reads **1.0333** of the bare arm on the basis and 1.0402 on HEAD,
so a user's `toVectorT` pays about three to four percent over the kernel
on the main set.

**The two standing placement controls part this run, and one of them changes
sign between the halves.** `mut-odo-vecdims-add-in` against the arm it varies
reads **0.9949 at 13 of 24, sign p 0.84** on the basis and **0.9957 at 16 of 24,
p 0.15** on HEAD --- both inside their halves' floors of 2.92% and 2.16%
and both a coin flip or near it by the sign test. Against the six-pair figures
the two answer differently and neither answers loudly: the basis margin of 0.51%
just clears its 0.46%, the control's 0.43% does not clear its 0.60%,
and a margin that clears a threshold by five hundredths of a point at 13 wins
of 24 is not a separation. So that pair separates nothing on either compiler ---
as Run 20 also found, and the question is parked in any case. `build` against
`mut-odo` is the one that moved: 0.9870 on the basis, a tie at 14 of 24 and p
0.54, against **1.0764** on HEAD at 7 of 24 and p 0.064, where Run 20 read
0.9899 and 0.9668 and Run 19 read 0.9633 and 0.9325. So the arm that
was the faster slot on HEAD in both previous runs is the slower one here
by 7.6%. Both pairs are read for placement and every address moved between
these runs, so a movement here is exactly what this file says such a boundary
carries; what the head of this file adds, and what neither previous run could
say, is that the tracked loops of `build` and `mut-odo` were NAMED off a `-g3`
twin this run and both sit at offset 0 on both halves, so the cache-line reading
is not what separates them.


## What the next run compares against

**Run 22's regime, roster and basis are settled; its PAIR is the one decision
this section leaves open, and it belongs to whoever asks for the run.**
The regime is `-fspec-constr`, as every run since Run 8, and it is the regime
the claims decide in; the shipped file does not set the flag ([the
ceiling](../README.md#the-mutable-ceiling-taken)). The roster is Run 21's --- 49
timed arms over 24 main-set shapes and 33 class views over nine classes, 1176
benches and 1617 --- unless the tasks below add to it, and the basis
is `run21-g912`'s recipe, ghc-9.12.4 with `-fobject-determinism`, the per-sample
instrument and the saturating preamble, run under `WILDLOG=1 SATURATE=1`, which
is now the same recipe five runs running. The allocation area is fixed
at `-A32m` and no pair will vary it again. **What Run 21's results argue for,
stated so the decision has something to weigh and not as a choice this file
makes.** A *repetition* --- one recipe built twice, or one binary run twice ---
is what this file has wanted for three runs and has now been refused three
times, each roster change putting a layout term into every cross-run figure;
and Run 21 makes the case sharper than argument, its floor having gone 2.32%,
1.51%, 2.92% over two roster changes with box, recipe and regime held still.
It is also the pair that would answer [task 3][open], the cheapest unspent
measurement here, which wants one binary over the roster several times
and no second recipe at all. A *fourth compiler reading* buys least,
the surviving manifest claim having now held on 9.12, 9.14 and HEAD four times.
A *purpose-built pair* has a candidate for the first time in three runs:
the `fillStage2` gap of task 1 is a code question about two fills in one binary,
so it wants a `-g3` dump and an instruction count rather than an evening,
and the run-length condition of task 2 wants one new arm on an existing class
rather than a pair. **So what the results ask for is a repetition and a handful
of arms, not a new variable** --- but the pair is not this file's to fix. **What
is NOT a candidate** is a pair varying the allocation area, closed 2026-08-21,
or one varying the roster between its halves, refused because it would break
`preflight`'s `check` comparison and both drivers' bench counts.

**The ruling this section carried about compiler pairs is now spent, and what
replaces it is a preference rather than an argument.** Run 19 advised against
another compiler pair, HEAD and 9.14 both having been read; Run 20 overrode
that because it rostered the rework's arms and the control the fix ships,
so a second compiler bought a first reading of shipped code on the compiler
its consumers will build with. Run 21 spent that reading a second time
and it came back the same: the manifest's surviving claim holds on both,
the allocation tiers hold on both, and every one of the five registrations
was decided the same way on both halves. **So the compiler variable has stopped
paying**, which is what Run 19 said two runs ago and what two runs of evidence
now support rather than contradict. What has taken its place as the thing worth
an evening is not a variable at all --- it is a repetition, which no pair since
Run 19 has been able to give.

**What Run 21 leaves the next run to read against, and the first item is
not a figure.** **The box did not change**, its machine check reading -0.33%
against the fingerprint Run 20 kept, over 24 of 24 shapes, worst
`stretch-pow2stride` -3.52% and none past 5%; so absolutes cross from Run 20
to Run 21 freely and the boundary that matters is still the BIOS change before
Run 18, which no absolute crosses. **The floor is 2.92% on the basis and 2.16%
on the control**, with the restricted six at 0.46% and 0.60%. A Run 22 margin
is judged on both and they answer different questions: the six-pair figure
is what two rows of one table must clear, the sixteen-pair one is how far an arm
differs from its own duplicate. **And it is not inherited**, which this run
demonstrates more plainly than any before it: Run 20 read 1.51% and 1.18%
on these same two recipes and this run reads 2.92% and 2.16%, one roster change
on, having itself fallen from 2.32% over the previous such step --- so a floor
moves by a factor of two in either direction for reasons no run has isolated,
and a Run 22 margin is judged against Run 22's own, never against these.
**The two columns below MAY be differenced, which is new**: `list` moved
**0.64%** between the halves against the 0.7% bar, where Run 20 read 0.71%
and Run 19 0.78% and both were refused. That is a hair INSIDE the bar rather
than past it, which is the passing side; treat it as marginal all the same
and prefer the within-run comparisons; and note that it is the MAIN SET's figure
alone --- `rev` at 1.0126, `bcastmid` at 1.0137 and `window` at 1.0097 are past
the bar, so those three class blocks say in their cross-half lines that they
are not read for the pair's variable. What the columns price is a compiler,
and the counted-work column says which movements that reaches:
`bq-odo-gm-mulback` and `bq-scan-rem-gm-mulback` six to seven percent apart
ON their instruction counts, `mut-odo-vecdims-add-in-leaf` ten points
of its fifteen, `canon-full` moving 12.4% in time at a count ratio of 0.9712,
and the placement-exposed arms `build`, `mut-odo` and `gen-unsafe` apart
at count ratios of 1.0000. So a movement on one of those three is layout
or runtime until the counts say otherwise.

**Registered with the pair.** Run 21's five registrations, their kill conditions
and their verdicts are [in the open list](../README.md#what-is-open),
and the commands that produced them were the pair note's, transcribed
into Provenance below before that note goes with the pair. **What Run 22
inherits is five riders that are now routine and no instrument that is new.**
The alone legs, the counted-work sweeps over every population, the saturating
preamble, the per-sample load fields and `--counts` all ran to form and want
no re-deciding; the counted work was taken before the evening this run,
on a working desktop, which is what its own scope note licenses and what left
the quiet window entirely to criterion. **What it inherits as a debt**
is nothing: no population was rerun, no gate failed, and post-run step 1c
was owed nothing. **What it inherits as a warning** is two things. The floor
is re-drawn per run and has now moved by a factor of two in each direction
across two roster changes, so no margin is judged against a predecessor's.
And **four of five registrations were refuted**, all of them in the same
direction and for the same reason --- they were written expecting the branch's
fill to cost about what the shipped fill costs --- so a Run 22 registration
about the rework should price `fillStage2` before it predicts anything
that composes with it.

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

| strategy | Run 21 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 21 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 20 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 20 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 19 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 19 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 18 (SpecConstr, max-skip +lookrts, -A32m, 9.14.1) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, instrumented) | Run 17 (SpecConstr, max-skip +lookrts, -A32m, plain) | Run 16 (SpecConstr, max-skip +lookrts, -A32m) | Run 16 (SpecConstr, max-skip +lookrts, -A64m) | Run 15 (SpecConstr, max-skip +lookrts) | Run 15 (SpecConstr, max-skip +lookrts +A32m) | Run 14 (SpecConstr, max-skip +lookrts) | Run 14 (SpecConstr, max-skip +lookrts +A1G) | Run 13 (SpecConstr, max-skip) | Run 13 (SpecConstr, max-skip +lookrts) | Run 12 (SpecConstr, max-skip) | Run 12 (SpecConstr, max-skip +procalign) | Run 11 (SpecConstr, aligned) | Run 11 (SpecConstr, max-skip) | Run 10 (SpecConstr) | Run 10 (SpecConstr, aligned) | Run 9 (SpecConstr) | Run 8 (SpecConstr) | Run 7 (Harness, -O1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mut-odo-vecdims` | **0.054** | 0.055 | 0.054 | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.055 | 0.054 | 0.047 | 0.048 | 0.054 | 0.049 | 0.051 | 0.049 | 0.049 | 0.049 | 0.049 | 0.048 | 0.048 | 0.048 | 0.049 | 0.048 | 0.053 | 0.054 |
| `mut-flat-gm` | **0.084** | 0.085 | 0.083 | 0.083 | 0.083 | 0.084 | 0.084 | 0.083 | 0.084 | 0.084 | 0.087 | 0.076 | 0.081 | 0.088 | 0.081 | 0.083 | 0.082 | 0.082 | 0.081 | 0.082 | 0.081 | 0.081 | 0.083 | 0.081 | 0.080 | -- | -- |
| `bq-mut-runs-gm-mulback` | **0.092** | 0.094 | 0.090 | 0.093 | 0.090 | 0.094 | 0.089 | 0.091 | 0.093 | 0.092 | 0.093 | 0.080 | 0.086 | 0.094 | 0.087 | 0.088 | 0.087 | 0.087 | 0.087 | 0.088 | 0.087 | 0.086 | 0.085 | 0.088 | 0.088 | 0.086 | -- |
| `bq-odo-gm-mulback` | **0.100** | 0.108 | 0.099 | 0.108 | 0.100 | 0.109 | 0.100 | 0.100 | 0.101 | 0.100 | 0.100 | 0.087 | 0.090 | 0.100 | 0.090 | 0.095 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | 0.090 | -- | -- |
| `bq-scan-rem-gm-mulback` | **0.099** | 0.106 | 0.098 | 0.105 | 0.098 | 0.106 | 0.096 | 0.098 | 0.099 | 0.099 | 0.096 | 0.082 | 0.091 | 0.096 | 0.091 | 0.090 | 0.091 | 0.090 | 0.090 | 0.091 | 0.089 | 0.090 | 0.090 | 0.089 | 0.090 | 0.090 | 0.119 |
| `bq-expand` | **0.115** | 0.116 | 0.114 | 0.116 | 0.115 | 0.117 | 0.115 | 0.117 | 0.117 | 0.115 | 0.114 | 0.101 | 0.102 | 0.114 | 0.102 | 0.107 | 0.103 | 0.102 | 0.102 | 0.102 | 0.103 | 0.103 | 0.102 | 0.102 | 0.105 | 0.102 | 0.127 |
| `build` | **0.104** | 0.111 | 0.101 | 0.101 | 0.103 | 0.101 | 0.103 | 0.102 | 0.105 | 0.106 | 0.109 | 0.097 | 0.102 | 0.110 | 0.103 | 0.097 | 0.099 | 0.099 | 0.098 | 0.098 | 0.096 | 0.100 | 0.110 | 0.096 | 0.114 | 0.095 | -- |
| `offtab` | -- | -- | 0.135 | 0.135 | 0.134 | 0.136 | 0.134 | 0.143 | 0.135 | 0.141 | 0.136 | 0.124 | 0.126 | 0.138 | 0.121 | 0.121 | 0.125 | 0.121 | 0.125 | 0.131 | 0.125 | 0.123 | 0.123 | 0.124 | 0.115 | 0.146 | -- |
| `mut-flat` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.074 | 0.063 |
| `bq-mut-runs-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.078 | 0.072 |
| `bq-odo-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.089 | 0.101 |
| `bq-scan-packed-mulback` | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | 0.108 | 0.097 |

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
(dropped 2026-08-28 with its parking) and `bq-mut-runs-gm-mulback`,
in that order of shapes led, `offtab-scan-rem` on Run 18, and **on Run 20 three
of the rework's arms**: `canon-vecdims`, best outside the family on 17 shapes,
`mid-copy` on 17 and `bcast-set` on 3 --- and **it only ever grows**: an arm
that has earned a column keeps it, and no run drops one --- **which
is a preference, not a law, and is superseded here. ARMS GET DROPPED, AND HAVE
BEEN MANY TIMES; ruled 2026-08-28.** A trim took fifteen at once; Run 20 demoted
`mut-odo-vecdims-add-out`, `-add-both` and `-add-both-down` to `Only`
on 2026-08-25; Run 21 parked eight permanently and removed `offtab`'s two A/A
twins on 2026-08-28; and this table lost `bq-mut-runs` with them, the first
column to go. What the preference buys is that a column is not churned
on a thousandth, which is worth having and is not a proof that none can go.
**What governs a drop is two questions**, and the paragraph below prices
the cost of taking one rather than forbidding it: is the arm still TIMED,
an untimed one being unable to fill a cell at all --- keeping `bq-mut-runs`
asked the installer for a cell nothing can compute, which `--check-doc` fails
as an install `?`, and the only other answer was a rebuild of both halves;
and is the column the only copy of what it holds, which it never is, a run's own
figures living in its Results and class tables whatever the fingerprint carries.
Its figures end at Run 20 and went from the two tables below with the column,
narrowed by hand in the same edit --- `install` matches a table by its whole
header line, so a narrowed emitter and a wide table refuse each other, measured
that day when `smoke-sweep.sh` failed on exactly that. `--lint` now holds
this list to the TIMED roster, the older check having asked only whether
its arms were rostered, which a parked arm still is. The second table carries
the same columns over every stride-class shape, with its class named. **One
representative per family**, besides: where a qualifying arm is a close variant
of a member and measures closely, the leading one keeps the column,
so no strategy costs two. **Run 20 is the run that had to apply that clause,
and it kept two arms out.** `canon-memcpy-r2` and `canon-full` both qualified
--- best outside the family on 4 shapes and 6 --- and both are close variants
of `canon-vecdims` measuring within four thousandths of it on the main set,
0.052 and 0.053 against 0.049. The installer's own membership note is what
settles it rather than the judgement alone: on nearly every shape either of them
leads, the arm it beats is `canon-vecdims` or `bcast-set` at the same three
decimals, which is what *measuring this closely* means. The judgement is still
the author's, which is why `--fingerprint` names the best member on the shape
a newcomer leads. **Neither way of dropping an arm THAT STOPPED EARNING
ITS COLUMN survives**, which is what this paragraph is about; an arm PARKED out
of the timed roster is the other case and is ruled on above. Dropping one
that leads nothing this run churns on a thousandth --- `offtab-scan-rem` holds
`reshape1-rank10` at 0.090 against 0.091 --- and gaps the record wherever
the column went. Judging it off the fingerprint this file carries is worse:
that table holds the members alone, so a leaver would be judged against
the members alone where a joiner is judged against every timed arm ---
on `reshape1-rank10` the members' own minimum was `bq-scan-rem-gm-mulback`
at 0.091, while the arm that won the shape read 0.090 and had no column
to be seen in. The header therefore grows, and the run writer narrows it by hand
if it gets unwieldy: it is fourteen columns now, one fewer than Run 20
published, and the next run that adds one should ask whether it still reads.

| shape | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.92 us | 0.084 | 0.145 | 0.154 | 0.171 | 0.173 | 0.149 | 0.169 | 0.119 | 0.086 | 0.088 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.21 us | 0.094 | 0.179 | 0.148 | 0.204 | 0.204 | 0.190 | 0.161 | 0.105 | 0.105 | 0.098 |
| `stretch-rank12` | 2 | 4096 | 110 us | 0.092 | 0.189 | 0.131 | 0.273 | 0.270 | 0.195 | 0.169 | 0.072 | 0.105 | 0.098 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 114 us | 0.067 | 0.135 | 0.098 | 0.188 | 0.180 | 0.136 | 0.125 | 0.058 | 0.072 | 0.071 |
| `conv1d-24` | 3 | 5184 | 101 us | 0.057 | 0.071 | 0.100 | 0.139 | 0.134 | 0.077 | 0.137 | 0.057 | 0.057 | 0.060 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 364 us | 0.048 | 0.094 | 0.095 | 0.108 | 0.107 | 0.103 | 0.121 | 0.044 | 0.050 | 0.051 |
| `gather48-src-50` | 3 | 22500 | 436 us | 0.053 | 0.066 | 0.099 | 0.131 | 0.132 | 0.075 | 0.132 | 0.053 | 0.053 | 0.057 |
| `stretch-rank10` | 3 | 59049 | 1.28 ms | 0.065 | 0.116 | 0.103 | 0.158 | 0.167 | 0.119 | 0.138 | 0.055 | 0.068 | 0.069 |
| `stretch-coprime-r7` | 13 | 60060 | 1.02 ms | 0.035 | 0.085 | 0.094 | 0.060 | 0.059 | 0.093 | 0.123 | 0.033 | 0.035 | 0.038 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.05 ms | 0.057 | 0.090 | 0.101 | 0.148 | 0.153 | 0.098 | 0.130 | 0.057 | 0.060 | 0.061 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.44 ms | 0.057 | 0.091 | 0.100 | 0.146 | 0.148 | 0.102 | 0.131 | 0.057 | 0.060 | 0.061 |
| `stretch-primes` | 89 | 250357 | 4.01 ms | 0.029 | 0.073 | 0.091 | 0.030 | 0.030 | 0.084 | 0.129 | 0.029 | 0.029 | 0.030 |
| `stretch-inner1` | 1 | 500000 | 12.9 ms | 0.090 | 0.031 | 0.073 | 0.220 | 0.253 | 0.032 | 0.073 | 0.000 | 0.090 | 0.098 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.1 ms | 0.043 | 0.077 | 0.094 | 0.089 | 0.096 | 0.087 | 0.126 | 0.044 | 0.045 | 0.047 |
| `vgg-14-c512-k3` | 3 | 903168 | 18.6 ms | 0.058 | 0.090 | 0.100 | 0.130 | 0.143 | 0.101 | 0.133 | 0.057 | 0.060 | 0.064 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.4 ms | 0.035 | 0.071 | 0.090 | 0.053 | 0.056 | 0.082 | 0.129 | 0.034 | 0.035 | 0.037 |
| `stretch-inner256` | 256 | 1750784 | 32.8 ms | 0.032 | 0.069 | 0.086 | 0.033 | 0.033 | 0.075 | 0.117 | 0.032 | 0.032 | 0.032 |
| `stretch-pow2stride` | 64 | 1769472 | 28.3 ms | 0.125 | 0.122 | 0.147 | 0.125 | 0.126 | 0.134 | 0.222 | 0.125 | 0.125 | 0.125 |
| `stretch-r5-8x432` | 8 | 1769472 | 33.4 ms | 0.033 | 0.062 | 0.083 | 0.058 | 0.055 | 0.069 | 0.116 | 0.032 | 0.032 | 0.035 |
| `stretch-square-1341` | 1341 | 1798281 | 29.7 ms | 0.086 | 0.130 | 0.153 | 0.086 | 0.087 | 0.139 | 0.201 | 0.080 | 0.085 | 0.086 |
| `stretch-bigstride` | 3 | 1800000 | 49.6 ms | 0.035 | 0.044 | 0.067 | 0.084 | 0.089 | 0.051 | 0.093 | 0.035 | 0.035 | 0.037 |
| `stretch-tab7MB` | 2 | 1800000 | 38 ms | 0.063 | 0.063 | 0.101 | 0.153 | 0.142 | 0.068 | 0.145 | 0.062 | 0.062 | 0.068 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39.5 ms | 0.023 | 0.051 | 0.063 | 0.023 | 0.023 | 0.057 | 0.095 | 0.022 | 0.023 | 0.026 |
| `stretch-wide-2xM` | 2 | 1800000 | 37.9 ms | 0.062 | 0.061 | 0.098 | 0.148 | 0.152 | 0.069 | 0.143 | 0.062 | 0.062 | 0.066 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 867 us | 0.033 | 0.066 | 0.091 | 0.063 | 0.054 | 0.080 | 0.118 | 0.032 | 0.032 | 0.030 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 27.1 ms | 0.022 | 0.074 | 0.092 | 0.022 | 0.022 | 0.092 | 0.124 | 0.022 | 0.021 | 0.019 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 37.5 ms | 0.061 | 0.060 | 0.098 | 0.136 | 0.145 | 0.070 | 0.140 | 0.061 | 0.061 | 0.061 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.43 ms | 0.058 | 0.091 | 0.100 | 0.153 | 0.144 | 0.102 | 0.128 | 0.058 | 0.012 | 0.062 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.87 ms | 0.022 | 0.070 | 0.088 | 0.023 | 0.023 | 0.086 | 0.124 | 0.022 | 0.013 | 0.023 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.2 ms | 0.036 | 0.046 | 0.069 | 0.076 | 0.090 | 0.054 | 0.094 | 0.036 | 0.033 | 0.038 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.1 ms | 0.023 | 0.053 | 0.066 | 0.023 | 0.023 | 0.060 | 0.089 | 0.023 | 0.019 | 0.023 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.89 ms | 0.108 | 0.133 | 0.092 | 0.338 | 0.328 | 0.129 | 0.092 | 0.000 | 0.116 | 0.106 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.7 ms | 0.091 | 0.032 | 0.073 | 0.269 | 0.247 | 0.032 | 0.073 | 0.000 | 0.093 | 0.092 |
| `reshape1-strided-r3` | `reshape1` | 1 | 180000 | 4.75 ms | 0.094 | 0.033 | 0.074 | 0.248 | 0.237 | 0.033 | 0.074 | 0.016 | 0.094 | 0.094 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 13.1 ms | 0.089 | 0.031 | 0.071 | 0.230 | 0.229 | 0.031 | 0.071 | 0.000 | 0.088 | 0.098 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 115 us | 0.067 | 0.133 | 0.097 | 0.182 | 0.169 | 0.137 | 0.125 | 0.057 | 0.070 | 0.070 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 439 us | 0.052 | 0.065 | 0.097 | 0.124 | 0.111 | 0.074 | 0.129 | 0.052 | 0.052 | 0.055 |
| `rev-primes` | `rev` | 89 | 250357 | 4.05 ms | 0.029 | 0.072 | 0.091 | 0.030 | 0.030 | 0.084 | 0.129 | 0.029 | 0.029 | 0.029 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 435 us | 0.054 | 0.068 | 0.101 | 0.127 | 0.128 | 0.077 | 0.131 | 0.054 | 0.053 | 0.057 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.48 ms | 0.058 | 0.089 | 0.099 | 0.157 | 0.149 | 0.099 | 0.128 | 0.057 | 0.059 | 0.060 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.01 ms | 0.030 | 0.079 | 0.102 | 0.031 | 0.031 | 0.092 | 0.131 | 0.030 | 0.030 | 0.031 |
| `runs-65536` | `runs` | 65536 | 1769472 | 25.8 ms | 0.027 | 0.075 | 0.093 | 0.027 | 0.027 | 0.088 | 0.134 | 0.028 | 0.027 | 0.032 |
| `runs-1024` | `runs` | 1024 | 1799168 | 26.7 ms | 0.028 | 0.074 | 0.090 | 0.028 | 0.028 | 0.086 | 0.132 | 0.028 | 0.028 | 0.030 |
| `runs-2` | `runs` | 2 | 1800000 | 37.3 ms | 0.063 | 0.063 | 0.101 | 0.133 | 0.158 | 0.069 | 0.149 | 0.063 | 0.063 | 0.068 |
| `runs-3` | `runs` | 3 | 1800000 | 33.9 ms | 0.052 | 0.066 | 0.098 | 0.113 | 0.104 | 0.074 | 0.140 | 0.051 | 0.051 | 0.055 |
| `runs-9` | `runs` | 9 | 1800000 | 29.3 ms | 0.034 | 0.071 | 0.094 | 0.054 | 0.053 | 0.082 | 0.134 | 0.034 | 0.034 | 0.037 |
| `runs-96` | `runs` | 96 | 1800000 | 26.9 ms | 0.028 | 0.074 | 0.091 | 0.030 | 0.030 | 0.086 | 0.137 | 0.028 | 0.028 | 0.030 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 27.3 ms | 0.030 | 0.074 | 0.092 | 0.033 | 0.033 | 0.085 | 0.134 | 0.028 | 0.029 | 0.031 |
| `scaled-r5` | `scaled` | 13 | 15015 | 249 us | 0.033 | 0.073 | 0.094 | 0.049 | 0.051 | 0.083 | 0.128 | 0.031 | 0.033 | 0.036 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 941 us | 0.028 | 0.072 | 0.092 | 0.032 | 0.033 | 0.081 | 0.127 | 0.029 | 0.028 | 0.029 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.77 ms | 0.034 | 0.072 | 0.090 | 0.034 | 0.034 | 0.080 | 0.134 | 0.032 | 0.032 | 0.032 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.03 ms | 0.037 | 0.082 | 0.096 | 0.062 | 0.061 | 0.093 | 0.126 | 0.037 | 0.037 | 0.039 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.5 ms | 0.059 | 0.091 | 0.101 | 0.139 | 0.154 | 0.098 | 0.133 | 0.059 | 0.061 | 0.062 |
| `slice-primes` | `slice` | 89 | 250357 | 3.99 ms | 0.030 | 0.081 | 0.104 | 0.032 | 0.032 | 0.093 | 0.132 | 0.030 | 0.030 | 0.031 |
| `window-28x28-k5` | `window` | 5 | 14400 | 266 us | 0.044 | 0.079 | 0.094 | 0.103 | 0.094 | 0.087 | 0.119 | 0.045 | 0.044 | 0.047 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 871 us | 0.095 | 0.048 | 0.074 | 0.283 | 0.264 | 0.048 | 0.074 | 0.020 | 0.101 | 0.103 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.21 ms | 0.058 | 0.089 | 0.098 | 0.141 | 0.154 | 0.099 | 0.127 | 0.057 | 0.058 | 0.060 |

**One row to read first, and it is a property of the shape and not of any arm**:
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction --- which this run's counted work
makes concrete for the second time, the HEAD penalty on `bq-odo-gm-mulback`
reading exactly 1.0000 there and 0.9149 to 0.9701 everywhere else. **The two
rows this paragraph used to name are retired with the arms that derived them**:
`stretch-square-1341` and `stretch-pow2stride` were the shapes where both arms
tying at the head of the pure tier lost to `bq-expand`, a set re-derived every
run since Run 19; `vFillStrided` ships the mutable fill, so that ordering flags
nothing and the set is not derived again.


## The claims the next run should test

**Run 21's verdicts first**, since a run reports breaks rather than re-deriving
the table. **The one manifest claim left held on both compilers**, all five
of claim 1's links on the 9.12 basis and all five on GHC HEAD --- no BROKE
on either half, a fourth clean sweep running. That is the first reading
of the set the parking of 2026-08-28 left: claims 2 and 6 retired with `offtab`
and `gen-quotrem`, the arms their only surviving links turned on, so what
was thirteen registered orderings through Run 19 and eight at Run 20 is five
links of one claim here. Claims 3, 4, 5 and 9 went at Run 19's write-up and 2
and 6 at Run 21's preparation; none of their numbers is reused, so a verdict
recorded against *claim 4* in an earlier run's file still means what it said.
**What this run adds to the sweep is a roster the manifest had not been read
on**, for the second run running: six timed arms landed and ten left between Run
20 and Run 21, so every ordering was re-read on a build whose every address had
moved, and none of them noticed. Every arm claim 1 names is still timed,
and `--pair` recovers any retired ordering in one call whenever it is wanted.

**The six retired claims are not re-read here.** Claims 3, 4, 5 and 9 left
the manifest at Run 19's write-up, on a sweep in which all thirteen held on both
of that run's halves; claims 2 and 6 left on 2026-08-28 with the parking
of the arms their surviving links turned on, and their last readings are Run
20's, in that run's own file. The numbered items below say what each was
in a clause. Run 21 does not re-derive any of them and quotes none as its own:
of the arms they named, those still rostered and timed put any
of those orderings one `--pair` call away, and the parked ones would want a run
that re-times them --- which is the whole of what retiring them gave up.

**Claim 1 held on all five links, on both halves, and the family above its top
rung has grown again.** The five links are what the `needs` column drew: what
a mutating `Vector` method buys (**0.6463** on the basis), what one more mutable
write pattern buys (0.9154), what a mutable `Int` scratch buys (0.9168
and 0.9169 against the two fastest arms needing nothing), and, at the foot
and **retired on 2026-08-29 with this as its last reading**, the two fastest
pure arms tied at 0.9999 on 11 of 24 and sign p 0.84 --- so while the mutating
method's upstream answer stayed open, `bq-scan-rem-gm-mulback`
and `bq-odo-gm-mulback` were indistinguishable and either was what would ship.
On HEAD the same five hold at 0.6466, 0.9066, 0.8670, 0.8810 and a tie at p
0.31. Every figure is within a few thousandths of Run 20's on the links they
share, across a roster change that moved every address. **The manifest below
therefore carries four links where this paragraph reads five.**

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6463, 20 of 24, sign p 0.0015;
`mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9154, 24 of 24, sign p 1.2e-07;
`bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9168, 20 of 24, sign p 0.0015;
`bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9169, 17 of 24, sign p
0.064. 4 of 4 registered orderings held.

**The first link is the one this run's new arms bear on, and the claim sees
it less well than it did.** Claim 1 reads `mut-odo-vecdims` against
`mut-flat-gm`, and **seven** arms now read below `mut-odo-vecdims`, four of them
inside its own family, at 0.036 to 0.053 against its 0.054, with two more level
with it --- where Run 20 had three inside the family and six arms ahead in all.
So the ladder's top rung understates what a mutating method buys by about
a third, while remaining true as stated. **And one of the seven is the shipped
library route itself**, `lib-stage1` at 0.039, which is the first run in which
an arm shaped like `Data/Array/Internal.hs` sorts above the arm that file's fix
is named for. Whether the claim should be re-aimed at the family's leader
is a question for the next run and is [under the recommended
tasks](../README.md#recommended-tasks-after-run-21); it is not re-aimed here,
a claim being re-aimed on a decision and not on one reading.

**Claim 7 held on the levels, and the cell count moved with the roster rather
than with the compiler.** Every level is Run 15's through Run 20's to the digit
--- the mutable fills at 1.00x, the scan family 1.33x, `bq-odo-gm-mulback`
1.51x, `offtab-scan-rem` 2.00x, `bq-expand` 2.35x, `list` 23.50x ---
and the class blocks read the tiers unbroken in all nine classes, `bq-expand`
running 1.14x on `scaled` to 4.91x on `reshape1` where that class's own `m`
shows through. **Six rows joined and moved no level**: five of the new arms read
1.00x, the mutable fills' own tier, and only the two list-entry arms sit above
it at 2.00x, so the rework and the library-shaped arms buy their time without
buying allocation. **The cross-half agreement is where the pair parts, as
on the two runs before**: **1026 of the 1128** main-set cells that allocate
in earnest agree to 1e-4, where Run 20 read 1143 of 1224 and Run 19 1016
of 1080, and the worst disagreement is **6.24e-03
on `cnn-slice-c32/bq-mut-runs-gm-mulback`** --- the same shape Run 19 and Run 20
both named, on a different arm, the one they named having been parked.
Allocation is deterministic per call, so a cell that moves is a code change
and never a slot: the levels surviving while a hundred-odd cells move is HEAD
reallocating within a tier rather than changing what any strategy fundamentally
costs.

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

**The list DID need re-aiming this run, and the roster moved under it
for the second time running.** Six timed arms landed and ten names left between
Run 20 and Run 21, and the ten include the two arms claims 2 and 6 turned on,
so those two retired on 2026-08-28 rather than on a reading --- which is the one
thing the re-aiming of the 2026-08-24 era did not insure against: it wrote
unconditional counterparts so that dropping a PRECONDITION would not drop
a question, and what dropped here was the arm itself. Claim 1 needed nothing:
every arm its links name is still timed. **What the roster does raise
is a question the manifest cannot see**, and it is claim 1's first link: seven
arms now read below `mut-odo-vecdims`, four of them inside its own family,
so the ladder's top rung understates what a mutating method buys. That is left
to the next run rather than re-aimed here.

1. `mut-odo-vecdims` < `mut-flat-gm` < `bq-mut-runs-gm-mulback` < each
   of `bq-scan-rem-gm-mulback` and `bq-odo-gm-mulback`, the whole ordering read
   on unconditional arms --- **the ladder the `needs` column draws**, each link
   pricing one thing the implementation is allowed to ask for. **The foot rung
   retired 2026-08-29**, on a decision rather than on a reading: it registered
   the two arms needing nothing at all as a tie, so that either was what would
   ship if the mutating `Vector` method were refused upstream, and it had read
   as a tie on every run that carried it. Both arms stay rostered and stay
   in the rung above, `--pair bq-scan-rem-gm-mulback bq-odo-gm-mulback` recovers
   the reading whenever the upstream answer wants it, and its last is Run 21's,
   above. The middle link is the one the README has seen a layout term move ---
   0.9708 at 15 of 24 on Run 10's unaligned half against 0.9293 at 22
   on its aligned one --- and on a placed layout it has now read the aligned
   figure five runs running. The ordering has survived eight runs, two changes
   of basis, a repetition and three compilers.
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
8. **Retired 2026-08-29**, on a decision and one day after its last re-aiming.
   What it asked: that every pure arm in the fast tier run its output through
   the single in-order `vGenerate` over an `m`-length table, so a `bq-*` arm
   falling behind loses on its table build and not on its output. Its last
   reading is Run 21's, which found it true and its subject smaller again ---
   nine arms at or below `mut-odo-vecdims` and not one of them a `bq-*`,
   so the structure it described governed a tier starting a third of the way
   down. What retires it is that subject: the pure tier is no longer what ships,
   and a claim quantified over it was being re-aimed and re-read every run
   to say so. It was also the one claim with no named invocation, read off
   the table by eye throughout, so nothing mechanical goes with it.
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
now, and no live claim is without one since claim 8 retired. **The general form,
and it is a standing instruction rather than an observation: if a write-up
hand-rolls a script to answer something the reader should answer, that
is a defect report against the reader** --- fix it there, before the sentence
it was written for, or the next run invents its own wrong version. **Two riders,
both bought on Run 19.** A new MODE joins the guards its siblings already have,
and is checked against them rather than written beside them: `--counts` shipped
able to be given without the `--compare` it reads, silently printing the default
table and exiting 0 --- the unread-flag family exactly, added next to four
sibling readings of `--compare` that were every one of them already guarded,
and joining none. **And an instrument may be BACKED OUT, which is not a failure
of the write-up but a result of it.** Measure what it flags before shipping it:
the obvious mechanical repair for stale paragraphs was built and returned 100
for the four that mattered, so it went, and the refutation with its numbers
is under the tasks heading --- worth more than the mode, since it stops the next
session building the same thing. A report that never empties is one nobody
reads, which this file already knows about hints.

**And for each stride class, the same three properties, now carrying Run 21's
verdicts** over nine classes rather than eight, the details beside each class's
table:

1. **The regime 3 fix's `worst` stays under 1.** Held in every one of the ten
   populations, in every regime, roster and layout the README has run ---
   so the fix was never slower than the `list` it replaced, on any shape of any
   class the library can produce. This is the property the classes exist
   to test, no geomean can state it, and a break would be the one result here
   to bear on `Data/Array/Internal.hs` directly. Re-aimed 2026-08-22
   with the decision to ship `mut-odo-vecdims`, and read for that arm since:
   **on Run 21 its worst is 0.125 on the main set and 0.108 in a class
   (`reshape1`), both read on the basis half, with the control half at 0.126
   and 0.109** --- so the property holds for the arm decided, on both compilers,
   and neither end is within a tenth of 1 --- the main-set end is a factor
   of 7.98 inside it, on `stretch-pow2stride`, and the class end 9.25. Both
   halves are quoted because one is not enough: Run 18's entry here read
   a floor-level figure from whichever half happened to be lower, which
   is the defect this phrasing exists to prevent. **What the new class adds
   is the first FILL to break it.** `gen-unsafe` carries a `worst` above 1
   in all ten populations, from 1.039 on `runs` to 3.324 on the main set,
   and at least one `list` twin does in each --- but they are a baseline variant
   and the baseline's own controls rather than candidate fills;
   the library-shaped arms are not, and FOUR of them break it on `runs`, all
   at `runs-2`: `liblist-stage1` at **1.371**, `lib-stage2-concat` at 1.338,
   `lib-stage1` --- the shipped route --- at **1.335**, and `liblist-stage2`
   at 1.135. So on that shape every route the library offers is slower
   than the baseline it replaces, and the branch's fill is the only arm
   of the four that is not. The property is stated of the fix and the fix holds;
   that a library-shaped arm does not is this run's finding and is read
   at the class's own block.

2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-expand` behind it. **The first clause breaks in all nine CLASS
   populations this run --- the main set is the tenth and is counted separately
   throughout this section --- and in seven of the nine it breaks
   to a sibling.** Read as the vecdims family's rather than one arm's ---
   the ruling Run 9 left, and no run has yet separated them --- it holds
   in seven: `rev`, `revsome`, `bcast`, `slice`, `window`, `scaled` and the new
   `runs` are each led by a `mut-odo-vecdims` variant from the leaf block,
   at margins of 7.5% (`scaled`) to 47.2% (`window`) against those populations'
   own floors, every one of them outside. **In two it breaks outright, to arms
   outside the family.** `bcastmid` is led by `mid-copy` at 0.017 against
   the fix's 0.032 --- **0.5429 paired, ahead on 4 of 4 shapes**, and within six
   thousandths of Run 20's 0.5490 on the same pair --- and `reshape1`
   by `lib-stage2-concat`, whose cells there are degenerate and price dispatch
   rather than filling, so that one is a break in the sort and not in the work.
   **What changed since Run 20 is which arm holds the outside-family slot,
   and it is the same arm in five of the nine**: `lib-stage1` leads outside
   the family on `rev`, `revsome`, `bcast`, `slice` and `window`,
   `canon-vecdims` on `scaled` and `runs`, and the two outright breaks hold
   their own slot --- where Run 20 had the rework's arms in all eight. The third
   clause reads the last candidate `bq-expand` behind `mut-odo-vecdims`
   and holds in all nine.

3. **The allocation tiers survive, and every level is Run 15's through Run 20's
   to the digit**: the mutable fills at the result vector, `bq-expand` between
   1.14x and 4.91x it, `list` an order of magnitude above. Where a level moves
   it is the class's own `m` showing through, exactly as this property warned
   --- `bq-expand` at 1.14x on `scaled` (`m` of 1 and 2,000) and 4.91x
   on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine
   and `list` running 19.43x to 32.29x across them, the new `runs` class sitting
   at the bottom of that range with `scaled`. **Five of the six arms that joined
   the roster read 1.00x**, the mutable fills' own tier, so neither the leaf
   variant nor the library-shaped fills buy their time with allocation; the two
   list-entry arms are the exception at 2.00x, which is the table the list form
   carries. On a pair whose two halves are different compilers this
   is the property that says a difference is codegen and not the program:
   allocation is deterministic per call, none of these levels moved, and the two
   halves agree on 1026 of 1128 allocating cells.

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
of 24 at p 0.84 and 1, so the two fastest pure arms were indistinguishable
and either was what would ship if the mutating method were refused --- the rung
this installed, and retired again on 2026-08-29. Its three existing links stay,
the middle one redundant with the two new ones and carrying seven runs
of history they do not. **Claim 2 keeps its number and changes its question**
to where the arms needing something other than the fix sit: `offtab`, which
needs only that `Int` scratch, behind `bq-scan-rem-gm-mulback` at **1.36**
and **1.44**; and `bq-expand` behind `mut-odo-vecdims` at **2.09** and **2.13**,
kept only while `Data/Array/Internal.hs` carried `bq-expand`, and to retire
with the three `TODO: retarget` markers, which were one decision with it.
**That condition was spent the same day and the link outlived it by two runs**:
the file went to `vFillStrided` on 2026-08-24 and the markers went
with the prose they marked, but nothing read the condition back, so Run 20
registered and read the link like any other and it retired only on 2026-08-26.
Thirteen registered orderings become eight here, and seven when that second link
finally goes; claims 7 and 8 stayed unmanifested prose. **The rewriting the ask
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

**Run 21 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) records every class
on BOTH halves**, one process each, in [the
sequence](../README.md#making-a-major-benchmark-run), and all eighteen came out
of the same unbroken window as the two main sets --- no intrusion, no rerun,
nothing to distinguish one block from another on that count, which is what Run
20's two rerun populations obliged it to state here. Every table below
is the **basis half**'s, which on this run is the 9.12 one, the half that keeps
the lineage. What the second half buys is that a pair's variable can be read
on a class, which is what settled Run 14's `scaled` question and what no run
before it could have asked. **Read across the halves and the direction Runs 19
and 20 found holds, at about the same size.** Of the 387 arm-comparisons
the nine classes carry, **224 put the 9.12 half faster and 163 slower**, and all
nine geomeans fall below 1, running **0.9749 on `reshape1` to 0.9945
on `bcastmid`**, where Run 20's eight ran 0.9700 to 0.9952. So on the classes
as on the main set, GHC HEAD costs this roster a little more, and does
it everywhere. **The extreme at one end is the same arm Run 20 named and it now
holds eight of the nine**: `mut-odo-vecdims-add-in-leaf`, reaching **0.7140**
on `bcast`, against Run 20's 0.7120 on the same class. **The other end wants
reading before it is quoted**, as it did last run: the largest figure any class
reports is `reshape1`'s `canon-vecdims` at **1.2134**, and that class's
canonicalizing arms return O(1) on three of its four shapes, so a ratio there
prices dispatch and not filling. **And three classes disqualify their own
cross-half line**: `rev` at 1.0126, `bcastmid` at 1.0137 and `window` at 1.0097
move `list` past the 0.7% bar, so their lines say so and are not read
for the compiler --- where the main set, at 0.64%, is inside it for the first
time in three runs.

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
that process's sixteen A/A controls. A cell that breaks one of [the three
properties](#the-claims-the-next-run-should-test) is bolded, and the class's own
paragraph says what broke.

**And the aggregate figures in the paragraph above the blocks are the reader's,
emitted rather than assembled.**
`./read-run.py --cross-classes --classes BASIS... --others CONTROL...` prints
every one of them --- the comparison count, the faster/slower split, the range
of the nine geomeans with the class at each end, the arm holding each extreme
and how many populations share it, the degenerate arms it kept out,
and the classes whose `list` is past the 0.7% bar --- from the same per-class
rows the nine cross-half lines below print, so the intro and the blocks cannot
part. The comparison count, the faster/slower split, the range of the nine
geomeans and the extreme arms are each an aggregate over the nine
`--block --compare` lines below, so they are read off those lines and never off
a population assembled for the purpose: Run 20 assembled its own twice
and was wrong both times --- once on the split, once on a low end that excluded
a class the sentence said it covered. Where a figure genuinely cannot come off
those lines, because a class's own maximum is a degenerate cell, the paragraph
says so rather than quoting it as though it could.

Then one block per class, in `classViews`' order --- `rev`, `revsome`, `bcast`,
`bcastmid`, `reshape1`, `slice`, `window`, `scaled`, `runs` --- each carrying
the same six things and nothing else:

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
   them already, `time` and `worst` jointly fixing both; every class is three
   shapes or more now --- six at three, `bcastmid` and `reshape1` at four
   and `runs` at seven --- so the line always prints;
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
| `rev` | 3 | 0.046 | 0.067 | `lib-stage1` 0.035 | `mut-odo-vecdims-add-in-leaf-down` 0.032 | 8.95% |
| `revsome` | 3 | 0.049 | 0.058 | `lib-stage1` 0.032 | `mut-odo-vecdims-add-in-leaf-down` 0.032 | 6.97% |
| `bcast` | 3 | 0.035 | 0.061 | `lib-stage1` 0.027 | `mut-odo-vecdims-add-in-leaf-down` 0.022 | 6.56% |
| `bcastmid` | 4 | 0.032 | 0.058 | **`mid-copy`** 0.017 | **`mid-copy`** 0.017 | 4.69% |
| `reshape1` | 4 | 0.094 | 0.108 | **`lib-stage2-concat`** 0.000 | **`lib-stage2-concat`** 0.000 | 6.31% |
| `slice` | 3 | 0.040 | 0.059 | `lib-stage1` 0.036 | `mut-odo-vecdims-add-in-leaf-down` 0.033 | 3.55% |
| `window` | 3 | 0.062 | 0.095 | `lib-stage1` 0.033 | `mut-odo-vecdims-add-in-leaf-u2` 0.033 | 5.72% |
| `scaled` | 3 | 0.032 | 0.034 | `canon-vecdims` 0.030 | `mut-odo-vecdims-add-in-leaf` 0.028 | 3.30% |
| `runs` | 7 | 0.032 | 0.063 | `canon-vecdims` 0.029 | `mut-odo-vecdims-add-in-leaf` 0.029 | 3.50% |

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
| *bq-expand-nosum* | *--* | *--* | *0.17* | *134* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.07* | *144* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.24* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.032 | 0.049 | 0.08 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.033 | 0.050 | 0.13 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.035 | 0.051 | 0.08 | 145 | 1.00x |
| lib-stage1 | 0.035 | 0.053 | 0.07 | 145 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.036 | 0.052 | 0.07 | 145 | 1.00x |
| *mut-odo-vecdims-aa* | *0.046* | *0.067* | *0.05* | *137* | *1.00x* |
| **mut-odo-vecdims** | **0.046** | 0.067 | 0.09 | 137 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.046* | *0.067* | *0.08* | *137* | *1.00x* |
| mut-odo-vecdims-add-in | 0.046 | 0.067 | 0.10 | 137 | 1.00x |
| canon-vecdims | 0.047 | 0.057 | 0.06 | 137 | 1.01x |
| mid-copy | 0.047 | 0.070 | 0.10 | 137 | 1.00x |
| bcast-set | 0.049 | 0.070 | 0.05 | 136 | 1.00x |
| liblist-stage1 | 0.049 | 0.064 | 0.22 | 141 | 2.01x |
| canon-memcpy-r2 | 0.050 | 0.060 | 0.12 | 136 | 1.01x |
| canon-full | 0.054 | 0.062 | 0.06 | 136 | 1.01x |
| mut-flat-gm | 0.081 | 0.133 | 0.17 | 134 | 1.34x |
| mut-odo | 0.083 | 0.169 | 1.76 | 126 | 1.00x |
| build | 0.088 | 0.182 | 1.47 | 124 | 1.00x |
| *mut-odo-aa-distant* | *0.088* | *0.190* | *1.91* | *125* | *1.00x* |
| *build-aa-distant* | *0.089* | *0.164* | *1.18* | *125* | *1.00x* |
| *build-aa-adjacent* | *0.089* | *0.193* | *1.44* | *125* | *1.00x* |
| bq-expand-gm-mulback | 0.089 | 0.167 | 0.12 | 130 | 2.52x |
| *mut-odo-aa-adjacent* | *0.091* | *0.184* | *2.15* | *124* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.095 | 0.137 | 0.11 | 132 | 1.34x |
| bq-odo-gm-mulback | 0.095 | 0.116 | 0.13 | 131 | 1.41x |
| *bq-odo-gm-mulback-aa-distant* | *0.096* | *0.116* | *0.09* | *130* | *1.41x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.096* | *0.116* | *0.11* | *130* | *1.41x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.096* | *0.097* | *0.08* | *128* | *1.34x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.097* | *0.097* | *0.08* | *128* | *1.34x* |
| **bq-scan-rem-gm-mulback** | **0.097** | 0.097 | 0.07 | 128 | 1.34x |
| *bq-expand-aa-distant* | *0.100* | *0.175* | *0.11* | *128* | *2.52x* |
| bq-expand | 0.100 | 0.175 | 0.13 | 128 | 2.52x |
| *bq-expand-aa-adjacent* | *0.101* | *0.175* | *0.12* | *128* | *2.52x* |
| offtab-scan-rem | 0.129 | 0.129 | 0.09 | 124 | 2.00x |
| lib-stage2 | 0.142 | 0.146 | 0.04 | 122 | 1.01x |
| lib-stage2-concat | 0.142 | 0.146 | 0.06 | 122 | 1.01x |
| liblist-stage2 | 0.155 | 0.162 | 0.20 | 121 | 2.01x |
| list (baseline) | 1.000 | 1.000 | 0.29 | 86 | 23.43x |
| *list-aa-adjacent* | *1.001* | *1.002* | *0.19* | *86* | *23.43x* |
| *list-aa-distant* | *1.001* | *1.005* | *0.26* | *86* | *23.43x* |
| *gen-unsafe-aa-adjacent* | *1.222* | *1.341* | *1.30* | *81* | *1.00x* |
| gen-unsafe | 1.247 | 1.432 | 0.84 | 81 | 1.00x |
| *gen-unsafe-aa-distant* | *1.279* | *1.437* | *2.11* | *81* | *1.00x* |

**Controls:** The largest A/A pair is `mut-odo-aa-adjacent` at 1.0895, worst
cell 18.89% on `rev-gather48-src-50`, and 11 of 16 intervals cover 1.
The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `rev-primes`,
its interval covering 1. The in-situ term reads 1.0037, 1.0120, 1.0022, 1.0013
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0725, which the correction amplifies
by 1.43x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m41s, peak 95 MiB in use, 26 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.2 ms per call raw, 4.05 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes):** `mut-odo-vecdims` 0.067/0.052/0.029 `bq-scan-rem-gm-mulback`
0.097/0.097/0.091

**Across the halves:** 28 of the 43 arms are faster on this half and 15 slower,
at a geomean of 0.9805, from `mut-odo-vecdims-add-in-leaf` at 0.8464
to `mut-odo-aa-adjacent` at 1.1023, with `list` itself at 1.0126. **The baseline
moved 1.26% between the halves, past the 0.7% that lets two columns
be differenced, so this line is NOT read for the pair's variable.** The table
above is one process's and stands; what goes is the comparison.

**What the class says:** all three properties hold and the class reproduces
the main ordering. `mut-odo-vecdims` reads 0.046 with `worst` 0.067, an order
of magnitude inside 1, and `bq-expand` sits behind it on all three shapes.
The head is `mut-odo-vecdims-add-in-leaf-down` at 0.032 --- **0.7300 paired at 2
of 3 shapes, a 27.0% margin against this class's 8.95% floor**, so outside
it threefold --- and it is a family member, so property 2's first clause does
not break. **What is new is the slot below the family**: the best arm outside
it is `lib-stage1` at 0.035, the shipped library route itself, where Run 20 had
`canon-vecdims` at 0.046. **This class carries the run's widest floor, 8.95%**,
against Run 20's 4.14% and Run 19's 2.65%, and the pair carrying
it is `mut-odo-aa-adjacent` --- the same arm whose twins move the main set's
floor, so the two readings are one.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *90* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.10* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.27* | *93* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.032 | 0.037 | 0.07 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.037 | 0.08 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.032 | 0.038 | 0.09 | 99 | 1.00x |
| lib-stage1 | 0.032 | 0.038 | 0.07 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.033 | 0.038 | 0.07 | 99 | 1.00x |
| mid-copy | 0.048 | 0.059 | 0.09 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.049 | 0.057 | 0.07 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.049* | *0.057* | *0.09* | *96* | *1.00x* |
| liblist-stage1 | 0.049 | 0.050 | 0.61 | 96 | 2.00x |
| **mut-odo-vecdims** | **0.049** | 0.058 | 0.08 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.049* | *0.057* | *0.07* | *96* | *1.00x* |
| canon-vecdims | 0.052 | 0.057 | 0.07 | 96 | 1.00x |
| bcast-set | 0.053 | 0.060 | 0.07 | 96 | 1.00x |
| canon-memcpy-r2 | 0.054 | 0.060 | 0.13 | 96 | 1.00x |
| canon-full | 0.057 | 0.063 | 0.09 | 96 | 1.00x |
| mut-flat-gm | 0.078 | 0.089 | 0.19 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.089 | 0.099 | 0.14 | 86 | 1.33x |
| bq-expand-gm-mulback | 0.094 | 0.118 | 0.17 | 83 | 2.52x |
| *mut-odo-aa-distant* | *0.097* | *0.134* | *1.39* | *96* | *1.00x* |
| *bq-expand-aa-distant* | *0.099* | *0.129* | *0.16* | *83* | *2.52x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.102* | *0.09* | *86* | *1.33x* |
| build | 0.100 | 0.157 | 1.65 | 96 | 1.00x |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.102 | 0.09 | 86 | 1.33x |
| bq-expand | 0.101 | 0.128 | 0.21 | 83 | 2.52x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.101* | *0.102* | *0.17* | *86* | *1.33x* |
| *bq-expand-aa-adjacent* | *0.102* | *0.128* | *0.19* | *83* | *2.52x* |
| bq-odo-gm-mulback | 0.102 | 0.121 | 0.10 | 83 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.103* | *0.121* | *0.11* | *83* | *1.41x* |
| *bq-odo-gm-mulback-aa-distant* | *0.103* | *0.122* | *0.17* | *83* | *1.41x* |
| *mut-odo-aa-adjacent* | *0.107* | *0.156* | *1.50* | *96* | *1.00x* |
| mut-odo | 0.107 | 0.149 | 1.38 | 96 | 1.00x |
| *build-aa-adjacent* | *0.114* | *0.143* | *1.40* | *96* | *1.00x* |
| *build-aa-distant* | *0.117* | *0.145* | *1.51* | *96* | *1.00x* |
| offtab-scan-rem | 0.130 | 0.131 | 0.15 | 82 | 2.00x |
| lib-stage2 | 0.144 | 0.147 | 0.07 | 81 | 1.00x |
| lib-stage2-concat | 0.144 | 0.147 | 0.09 | 81 | 1.00x |
| liblist-stage2 | 0.158 | 0.163 | 0.19 | 79 | 2.00x |
| *list-aa-adjacent* | *0.999* | *1.000* | *0.18* | *47* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 47 | 23.43x |
| *list-aa-distant* | *1.001* | *1.010* | *0.28* | *47* | *23.43x* |
| *gen-unsafe-aa-adjacent* | *1.235* | *1.382* | *3.24* | *42* | *1.00x* |
| gen-unsafe | 1.235 | 1.367 | 1.29 | 42 | 1.00x |
| *gen-unsafe-aa-distant* | *1.261* | *1.415* | *1.67* | *42* | *1.00x* |

**Controls:** The largest A/A pair is `mut-odo-aa-distant` at 0.9303, worst cell
10.37% on `revsome-mid-cnn-L2`, and 11 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0003 on a worst cell of 0.33% on `revsome-outer-g48`,
its interval covering 1. The in-situ term reads 1.0164, 1.0168, 0.9991, 1.0145
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 0.9432, which the correction amplifies
by 1.45x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m43s, peak 119 MiB in use, 25 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 4.16 ms per call raw, 4.01 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.054/0.058
`bq-scan-rem-gm-mulback` 0.102/0.101/0.099

**Across the halves:** 25 of the 43 arms are faster on this half and 18 slower,
at a geomean of 0.9851, from `mut-odo-vecdims-add-in-leaf` at 0.8392
to `mut-odo-aa-adjacent` at 1.0714, with `list` itself at 1.0063.

**What the class says:** all three properties hold and nothing inverts.
`mut-odo-vecdims`'s `worst` is 0.058 and `bq-expand` trails it on every shape.
The head is `mut-odo-vecdims-add-in-leaf-down` at 0.032 against the fix's 0.049
--- **0.6989 paired at 2 of 3 shapes, a 30.1% margin against this class's 6.97%
floor** --- a family member, so the first clause holds. The best arm outside
the family is `lib-stage1` at 0.032, level with the family's own head, where Run
20 had `mid-copy` at 0.046. The floor is `mut-odo-aa-distant`'s 6.97%, against
Run 20's 6.14%.

**`bcast` --- an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *52* | *1.38x* |
| *canon-full-nosum* | *--* | *--* | *0.43* | *83* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.65* | *57* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.36* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.022 | 0.023 | 0.51 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.022 | 0.023 | 0.51 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.029 | 0.54 | 58 | 1.00x |
| lib-stage1 | 0.027 | 0.029 | 0.52 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.032 | 0.034 | 0.53 | 57 | 1.00x |
| bcast-set | 0.032 | 0.061 | 0.51 | 61 | 1.00x |
| canon-full | 0.033 | 0.061 | 0.55 | 61 | 1.00x |
| lib-stage2-concat | 0.034 | 0.073 | 0.48 | 61 | 1.00x |
| lib-stage2 | 0.034 | 0.073 | 0.51 | 61 | 1.00x |
| mid-copy | 0.035 | 0.061 | 0.52 | 60 | 1.00x |
| canon-vecdims | 0.035 | 0.061 | 0.55 | 60 | 1.00x |
| *mut-odo-vecdims-aa* | *0.035* | *0.061* | *0.54* | *60* | *1.00x* |
| **mut-odo-vecdims** | **0.035** | 0.061 | 0.44 | 60 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.035* | *0.062* | *0.39* | *60* | *1.00x* |
| mut-odo-vecdims-add-in | 0.035 | 0.061 | 0.51 | 60 | 1.00x |
| canon-memcpy-r2 | 0.036 | 0.066 | 0.56 | 60 | 1.00x |
| liblist-stage1 | 0.046 | 0.057 | 0.84 | 52 | 2.00x |
| liblist-stage2 | 0.047 | 0.089 | 1.01 | 54 | 2.00x |
| mut-odo | 0.056 | 0.145 | 1.35 | 60 | 1.00x |
| *build-aa-adjacent* | *0.056* | *0.139* | *1.60* | *60* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.057* | *0.153* | *1.08* | *60* | *1.00x* |
| build | 0.057 | 0.136 | 0.54 | 60 | 1.00x |
| *build-aa-distant* | *0.058* | *0.150* | *2.17* | *60* | *1.00x* |
| *mut-odo-aa-distant* | *0.059* | *0.157* | *1.83* | *60* | *1.00x* |
| mut-flat-gm | 0.067 | 0.074 | 0.65 | 49 | 1.13x |
| bq-mut-runs-gm-mulback | 0.080 | 0.092 | 0.59 | 46 | 1.13x |
| bq-expand-gm-mulback | 0.081 | 0.087 | 0.69 | 47 | 1.38x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.083* | *0.090* | *0.73* | *47* | *1.14x* |
| bq-odo-gm-mulback | 0.083 | 0.090 | 0.64 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-distant* | *0.083* | *0.090* | *0.42* | *46* | *1.14x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.098* | *0.69* | *46* | *1.38x* |
| bq-expand | 0.092 | 0.098 | 0.67 | 46 | 1.38x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.098* | *0.76* | *46* | *1.13x* |
| *bq-expand-aa-distant* | *0.093* | *0.098* | *0.37* | *46* | *1.38x* |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.098 | 0.69 | 46 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.094* | *0.100* | *0.09* | *46* | *1.13x* |
| offtab-scan-rem | 0.127 | 0.140 | 1.09 | 43 | 2.00x |
| gen-unsafe | 0.968 | 1.071 | 2.01 | 21 | 1.00x |
| *list-aa-distant* | *0.997* | *1.001* | *1.17* | *18* | *20.62x* |
| list (baseline) | 1.000 | 1.000 | 0.98 | 18 | 20.62x |
| *list-aa-adjacent* | *1.002* | *1.009* | *0.67* | *18* | *20.62x* |
| *gen-unsafe-aa-distant* | *1.044* | *1.044* | *1.67* | *21* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.067* | *1.072* | *2.27* | *21* | *1.00x* |

**Controls:** The largest A/A pair is `mut-odo-aa-distant` at 1.0656, worst cell
11.88% on `bcast-inner8`, and 12 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9994 on a worst cell of 0.24% on `bcast-tall-Mx2`, its interval
covering 1. The in-situ term reads 1.0156, 1.0095, 1.0074, 1.0149 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0453, which the correction amplifies by 1.67x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m47s, peak 151 MiB in use, 45 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 28.2 ms per call raw, 27.1 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900,
bcast-tall-Mx2):** `mut-odo-vecdims` 0.033/0.022/0.061 `bq-scan-rem-gm-mulback`
0.091/0.092/0.098

**Across the halves:** 25 of the 43 arms are faster on this half and 18 slower,
at a geomean of 0.9760, from `mut-odo-vecdims-add-in-leaf` at 0.7140
to `gen-unsafe-aa-adjacent` at 1.0800, with `list` itself at 1.0067.

**What the class says:** all three properties hold, and the slot below
the family changed hands. `mut-odo-vecdims` reads 0.035 with `worst` 0.061
and `bq-expand` behind on every shape. The head
is `mut-odo-vecdims-add-in-leaf-down` at 0.022 --- **0.6189 paired at 2 of 3
shapes, a 38.1% margin against this class's 6.56% floor**, the second widest
family margin of the nine behind `window`'s 47.2% --- and a family member,
so the first clause holds. **`bcast-set`, the zero-stride condition taken solo,
no longer leads outside the family**: `lib-stage1` does, at 0.027, where Run 20
read `bcast-set` at 0.032. The floor is `mut-odo-aa-distant`'s 6.56%, against
Run 20's 7.15%.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000,
`sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed
2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k`
is its worst, its block taken to 150000 elements where the class's others run 3
to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.38* | *70* | *1.57x* |
| *canon-full-nosum* | *--* | *--* | *0.62* | *103* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.63* | *75* | *1.17x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.26* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| mid-copy | 0.017 | 0.033 | 0.35 | 80 | 1.00x |
| canon-full | 0.018 | 0.033 | 0.44 | 80 | 1.00x |
| lib-stage2 | 0.022 | 0.038 | 0.36 | 77 | 1.00x |
| lib-stage2-concat | 0.022 | 0.038 | 0.38 | 77 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.023 | 0.037 | 0.34 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.023 | 0.037 | 0.32 | 78 | 1.00x |
| lib-stage1 | 0.026 | 0.038 | 0.32 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.038 | 0.35 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.028 | 0.038 | 0.33 | 77 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.058 | 0.31 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.058* | *0.29* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.032* | *0.059* | *0.50* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.058 | 0.49 | 76 | 1.00x |
| canon-vecdims | 0.032 | 0.058 | 0.36 | 75 | 1.00x |
| bcast-set | 0.033 | 0.062 | 0.32 | 75 | 1.00x |
| canon-memcpy-r2 | 0.034 | 0.061 | 0.35 | 75 | 1.00x |
| liblist-stage2 | 0.038 | 0.060 | 0.62 | 72 | 2.00x |
| liblist-stage1 | 0.042 | 0.049 | 0.81 | 72 | 2.00x |
| build | 0.050 | 0.153 | 1.15 | 68 | 1.00x |
| *build-aa-adjacent* | *0.051* | *0.165* | *1.91* | *68* | *1.00x* |
| mut-odo | 0.051 | 0.144 | 1.18 | 68 | 1.00x |
| *mut-odo-aa-distant* | *0.052* | *0.154* | *1.07* | *68* | *1.00x* |
| *build-aa-distant* | *0.052* | *0.152* | *1.85* | *68* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.053* | *0.166* | *1.05* | *68* | *1.00x* |
| mut-flat-gm | 0.063 | 0.091 | 0.63 | 68 | 1.17x |
| bq-mut-runs-gm-mulback | 0.073 | 0.102 | 0.54 | 66 | 1.17x |
| bq-expand-gm-mulback | 0.077 | 0.120 | 0.44 | 65 | 1.57x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.079* | *0.100* | *0.46* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.080* | *0.122* | *0.50* | *64* | *1.17x* |
| bq-odo-gm-mulback | 0.080 | 0.122 | 0.44 | 64 | 1.17x |
| **bq-scan-rem-gm-mulback** | **0.080** | 0.100 | 0.46 | 64 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.080* | *0.100* | *0.28* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-distant* | *0.080* | *0.123* | *0.34* | *64* | *1.17x* |
| *bq-expand-aa-distant* | *0.085* | *0.131* | *0.32* | *64* | *1.57x* |
| bq-expand | 0.085 | 0.131 | 0.46 | 64 | 1.57x |
| *bq-expand-aa-adjacent* | *0.086* | *0.131* | *0.40* | *64* | *1.57x* |
| offtab-scan-rem | 0.107 | 0.128 | 0.61 | 60 | 2.00x |
| *gen-unsafe-aa-adjacent* | *0.984* | *1.577* | *2.44* | *28* | *1.00x* |
| gen-unsafe | 0.997 | 1.522 | 2.07 | 28 | 1.00x |
| *gen-unsafe-aa-distant* | *0.998* | *1.466* | *2.72* | *28* | *1.00x* |
| *list-aa-adjacent* | *0.998* | *1.004* | *1.02* | *30* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 1.10 | 30 | 21.22x |
| *list-aa-distant* | *1.000* | *1.009* | *0.95* | *29* | *21.22x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0469, worst cell
21.73% on `bcastmid-b200k`, and 12 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0011 on a worst cell of 0.48% on `bcastmid-primes`,
its interval covering 1. The in-situ term reads 1.0208, 1.0446, 1.0185, 1.0320
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0373, which the correction amplifies
by 1.63x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m0s, peak 137 MiB in use, 38 MiB max residency;
the reader reads 49 benchmarks over 4 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 48.3 ms per call raw, 47.2 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.058/0.022/0.036/0.023
`bq-scan-rem-gm-mulback` 0.100/0.088/0.069/0.066

**Across the halves:** 14 of the 43 arms are faster on this half and 29 slower,
at a geomean of 0.9945, from `mut-odo-vecdims-add-in-leaf` at 0.8146
to `gen-unsafe` at 1.0654, with `list` itself at 1.0137. **The baseline moved
1.37% between the halves, past the 0.7% that lets two columns be differenced,
so this line is NOT read for the pair's variable.** The table above is one
process's and stands; what goes is the comparison.

**What the class says:** properties 1 and 3 hold and **property 2 BREAKS
outright, as it did on Run 20 and to the same arm.** `mid-copy` ---
the zero-stride-on-an-outer-axis condition taken solo, the second
of the rework's two conditions --- is the fastest timed arm at **0.017** against
`mut-odo-vecdims`'s 0.032, **0.5429 paired and ahead on 4 of 4 shapes, a 45.7%
margin against this class's 4.69% floor**. It is outside the vecdims family,
so this is a break in the first clause and not a naming of rounding, and
it is the one population where a rework condition beats the fix outright
on its own ground. Run 20 read 0.5490 on the same pair, so the margin has
reproduced to two figures over a roster change, 0.54 both times.
`mut-odo-vecdims`'s `worst` is 0.058 and `bq-expand` is behind throughout.
The floor is `build-aa-distant`'s 4.69%, against Run 20's 4.83%.

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
| *canon-full-nosum* | *--* | *--* | *0.18* | *254* | *0.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.61* | *103* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| lib-stage2-concat | 0.000 | 0.089 | 0.02 | 104 | 0.00x |
| canon-full | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| lib-stage2 | 0.000 | 0.089 | 0.01 | 104 | 0.00x |
| canon-memcpy-r2 | 0.000 | 0.016 | 0.03 | 110 | 0.00x |
| canon-vecdims | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| liblist-stage2 | 0.011 | 0.099 | 0.23 | 97 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.024 | 0.060 | 0.13 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.064 | 0.11 | 100 | 1.00x |
| lib-stage1 | 0.026 | 0.064 | 0.07 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.031 | 0.065 | 0.08 | 98 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.031 | 0.066 | 0.12 | 98 | 1.00x |
| mut-flat-gm | 0.034 | 0.133 | 0.36 | 96 | 2.00x |
| bq-mut-runs-gm-mulback | 0.034 | 0.129 | 0.42 | 96 | 2.00x |
| liblist-stage1 | 0.034 | 0.070 | 0.16 | 96 | 2.00x |
| *bq-odo-gm-mulback-aa-distant* | *0.050* | *0.141* | *0.14* | *93* | *2.26x* |
| bq-odo-gm-mulback | 0.050 | 0.140 | 0.17 | 92 | 2.26x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.050* | *0.138* | *0.21* | *92* | *2.26x* |
| bq-expand-gm-mulback | 0.073 | 0.168 | 0.40 | 87 | 4.91x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.075* | *0.092* | *0.14* | *86* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.075* | *0.092* | *0.12* | *86* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.075** | 0.092 | 0.17 | 86 | 2.00x |
| offtab-scan-rem | 0.075 | 0.092 | 0.13 | 86 | 2.00x |
| **mut-odo-vecdims** | **0.094** | 0.108 | 0.09 | 82 | 1.00x |
| mut-odo-vecdims-add-in | 0.094 | 0.108 | 0.08 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.094* | *0.108* | *0.13* | *82* | *1.00x* |
| mid-copy | 0.095 | 0.116 | 0.17 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.096* | *0.108* | *0.12* | *82* | *1.00x* |
| bcast-set | 0.097 | 0.106 | 0.08 | 82 | 1.00x |
| *bq-expand-aa-adjacent* | *0.114* | *0.200* | *0.29* | *80* | *4.91x* |
| bq-expand | 0.114 | 0.200 | 0.25 | 80 | 4.91x |
| *bq-expand-aa-distant* | *0.115* | *0.200* | *0.25* | *80* | *4.91x* |
| *mut-odo-aa-distant* | *0.248* | *0.344* | *4.38* | *67* | *1.00x* |
| mut-odo | 0.249 | 0.328 | 2.88 | 66 | 1.00x |
| build | 0.268 | 0.338 | 2.11 | 66 | 1.00x |
| *mut-odo-aa-adjacent* | *0.270* | *0.365* | *3.25* | *66* | *1.00x* |
| *build-aa-adjacent* | *0.274* | *0.324* | *2.52* | *64* | *1.00x* |
| *build-aa-distant* | *0.279* | *0.338* | *2.97* | *64* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.953* | *2.279* | *2.13* | *42* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.961* | *2.157* | *2.44* | *42* | *1.00x* |
| gen-unsafe | 0.992 | 2.308 | 1.63 | 42 | 1.00x |
| *list-aa-distant* | *0.994* | *0.999* | *0.27* | *42* | *32.29x* |
| *list-aa-adjacent* | *0.999* | *1.003* | *0.35* | *42* | *32.29x* |
| list (baseline) | 1.000 | 1.000 | 0.35 | 42 | 32.29x |

**Controls:** The largest A/A pair is `mut-odo-aa-adjacent` at 1.0631, worst
cell 11.19% on `reshape1-rank10`, and 7 of 16 intervals cover 1. The `sum-only`
halves agree at 0.9998 on a worst cell of 0.21% on `reshape1-500k`, its interval
covering 1. The in-situ term reads 1.0091, 1.0038, 1.0371, 1.1163 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0585, which the correction amplifies by 1.09x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h16m58s, peak 148 MiB in use, 40 MiB max residency;
the reader reads 49 benchmarks over 4 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 13.4 ms per call raw, 13.1 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10,
reshape1-strided-r3):** `mut-odo-vecdims` 0.089/0.091/0.108/0.094
`bq-scan-rem-gm-mulback` 0.071/0.073/0.092/0.074

**Across the halves:** 30 of the 43 arms are faster on this half and 13 slower,
at a geomean of 0.9749, from `mut-odo-vecdims-add-in-leaf-u2-down` at 0.8304
to `canon-vecdims` at 1.2134, with `list` itself at 1.0000.

**What the class says:** properties 1 and 3 hold, **property 2 breaks,
and this class's cells need reading before its table does.** Three of its four
shapes go degenerate for the canonicalizing arms: canonicalization drops
the unit dimension, the fill becomes a regime-1 return, and there is nothing
per-element left for a ratio to price --- so `lib-stage2-concat` heads the table
at 0.000 and its 0.0055 against the fix is a break in the sort and not
in the work. **`reshape1-strided-r3` is the one cell in the class that prices
the fill**, being strided where the others leave a contiguous run, and there
the branch's stage two reads 0.4215 ms against stage one's 0.1153 ms --- 3.66
times behind, which is the same regression the six genuine regime-3 classes
report and the one figure in this block that means what it appears to mean.
`mut-odo-vecdims` reads 0.094 with `worst` 0.108, its highest of the nine
classes, and `bq-expand` is behind throughout. The floor
is `mut-odo-aa-adjacent`'s 6.31%, against Run 20's 8.31%.

**`slice` --- a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *90* | *1.58x* |
| *canon-full-nosum* | *--* | *--* | *0.08* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.28* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.033 | 0.039 | 0.09 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.038 | 0.08 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.036 | 0.039 | 0.08 | 99 | 1.00x |
| lib-stage1 | 0.036 | 0.040 | 0.08 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.040 | 0.040 | 0.06 | 99 | 1.00x |
| mut-odo-vecdims-add-in | 0.040 | 0.059 | 0.08 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.040** | 0.059 | 0.07 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.059* | *0.09* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.040* | *0.059* | *0.08* | *96* | *1.00x* |
| mid-copy | 0.040 | 0.061 | 0.11 | 96 | 1.00x |
| canon-vecdims | 0.041 | 0.059 | 0.09 | 96 | 1.00x |
| canon-memcpy-r2 | 0.041 | 0.062 | 0.08 | 96 | 1.00x |
| bcast-set | 0.042 | 0.062 | 0.09 | 96 | 1.00x |
| canon-full | 0.042 | 0.066 | 0.09 | 96 | 1.00x |
| liblist-stage1 | 0.051 | 0.053 | 0.14 | 95 | 2.00x |
| *build-aa-distant* | *0.063* | *0.130* | *0.93* | *96* | *1.00x* |
| *build-aa-adjacent* | *0.064* | *0.136* | *0.92* | *96* | *1.00x* |
| build | 0.065 | 0.139 | 1.12 | 96 | 1.00x |
| *mut-odo-aa-adjacent* | *0.066* | *0.153* | *0.63* | *96* | *1.00x* |
| mut-odo | 0.067 | 0.154 | 1.35 | 96 | 1.00x |
| *mut-odo-aa-distant* | *0.067* | *0.156* | *1.02* | *96* | *1.00x* |
| mut-flat-gm | 0.084 | 0.091 | 0.17 | 87 | 1.08x |
| bq-mut-runs-gm-mulback | 0.093 | 0.098 | 0.18 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.103* | *0.08* | *86* | *1.08x* |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.104 | 0.08 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.104* | *0.09* | *86* | *1.08x* |
| bq-expand-gm-mulback | 0.104 | 0.121 | 0.15 | 83 | 1.58x |
| bq-odo-gm-mulback | 0.110 | 0.124 | 0.11 | 83 | 1.50x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.111* | *0.124* | *0.11* | *83* | *1.50x* |
| *bq-odo-gm-mulback-aa-distant* | *0.111* | *0.124* | *0.09* | *83* | *1.50x* |
| bq-expand | 0.111 | 0.131 | 0.11 | 83 | 1.58x |
| *bq-expand-aa-distant* | *0.111* | *0.131* | *0.08* | *83* | *1.58x* |
| *bq-expand-aa-adjacent* | *0.111* | *0.131* | *0.10* | *83* | *1.58x* |
| offtab-scan-rem | 0.131 | 0.133 | 0.13 | 82 | 2.00x |
| lib-stage2-concat | 0.147 | 0.150 | 0.08 | 80 | 1.00x |
| lib-stage2 | 0.147 | 0.150 | 0.08 | 80 | 1.00x |
| liblist-stage2 | 0.161 | 0.164 | 0.13 | 79 | 2.00x |
| list (baseline) | 1.000 | 1.000 | 0.18 | 47 | 20.54x |
| *list-aa-adjacent* | *1.005* | *1.010* | *0.24* | *46* | *20.54x* |
| *list-aa-distant* | *1.006* | *1.008* | *0.22* | *46* | *20.54x* |
| gen-unsafe | 1.562 | 2.520 | 3.30 | 43 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.616* | *2.458* | *1.51* | *42* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.617* | *2.660* | *2.03* | *42* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0355, worst
cell 5.52% on `slice-coprime-r7`, and 6 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0020 on a worst cell of 0.37% on `slice-cnn-L2-24x24-c32`,
its interval missing 1. The in-situ term reads 1.0152, 1.0140, 1.0158, 1.0392
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0348, which the correction amplifies
by 1.02x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m45s, peak 125 MiB in use, 36 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.14 ms per call raw, 3.99 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7):** `mut-odo-vecdims` 0.059/0.030/0.037
`bq-scan-rem-gm-mulback` 0.101/0.104/0.096

**Across the halves:** 24 of the 43 arms are faster on this half and 19 slower,
at a geomean of 0.9868, from `mut-odo-vecdims-add-in-leaf` at 0.8545
to `gen-unsafe-aa-distant` at 1.0494, with `list` itself at 0.9967.

**What the class says:** all three properties hold and the class reproduces
the main ordering. `mut-odo-vecdims` reads 0.040 with `worst` 0.059,
and `bq-expand` is behind on every shape. The head
is `mut-odo-vecdims-add-in-leaf-down` at 0.033 --- **0.8339 paired at 2 of 3
shapes, a 16.6% margin against this class's 3.55% floor** --- a family member,
so the first clause holds. The best arm outside the family is `lib-stage1`
at 0.036, where Run 20 had `canon-vecdims` at 0.040. **Its floor is 3.55%**,
on `gen-unsafe-aa-distant`, third tightest of the nine behind `scaled`'s 3.30%
and `runs`'s 3.50%, where this class read 5.73% on Run 20 --- so it tightened
by a third while the run's floors as a whole roughly doubled.

**`window` --- overlapping im2col patches: the workload the README opens
by naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *116* | *2.81x* |
| *canon-full-nosum* | *--* | *--* | *0.15* | *153* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.84* | *134* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *150* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *150* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.033 | 0.037 | 0.09 | 132 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.033 | 0.037 | 0.09 | 132 | 1.00x |
| lib-stage1 | 0.033 | 0.037 | 0.07 | 132 | 1.01x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.037 | 0.07 | 130 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.035 | 0.037 | 0.11 | 130 | 1.00x |
| canon-vecdims | 0.037 | 0.057 | 0.04 | 137 | 1.01x |
| canon-full | 0.038 | 0.064 | 0.18 | 138 | 1.01x |
| canon-memcpy-r2 | 0.039 | 0.061 | 1.00 | 137 | 1.01x |
| liblist-stage1 | 0.043 | 0.048 | 0.26 | 129 | 2.01x |
| mut-odo-vecdims-add-in | 0.061 | 0.095 | 0.06 | 116 | 1.00x |
| *mut-odo-vecdims-aa* | *0.062* | *0.095* | *0.08* | *116* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.095* | *0.05* | *116* | *1.00x* |
| **mut-odo-vecdims** | **0.062** | 0.095 | 0.06 | 116 | 1.00x |
| mid-copy | 0.064 | 0.101 | 0.25 | 115 | 1.00x |
| bcast-set | 0.066 | 0.103 | 0.07 | 115 | 1.00x |
| mut-flat-gm | 0.069 | 0.089 | 0.50 | 126 | 1.33x |
| bq-mut-runs-gm-mulback | 0.075 | 0.099 | 0.52 | 126 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.090* | *0.097* | *0.10* | *120* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.090** | 0.098 | 0.06 | 120 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.090* | *0.097* | *0.08* | *120* | *1.33x* |
| bq-odo-gm-mulback | 0.093 | 0.120 | 0.17 | 121 | 2.55x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.120* | *0.19* | *121* | *2.55x* |
| *bq-odo-gm-mulback-aa-distant* | *0.094* | *0.120* | *0.11* | *121* | *2.55x* |
| bq-expand-gm-mulback | 0.098 | 0.119 | 0.10 | 119 | 2.81x |
| offtab-scan-rem | 0.111 | 0.127 | 0.07 | 120 | 2.00x |
| *bq-expand-aa-distant* | *0.120* | *0.128* | *0.09* | *112* | *2.81x* |
| bq-expand | 0.120 | 0.129 | 0.10 | 112 | 2.81x |
| *bq-expand-aa-adjacent* | *0.120* | *0.130* | *0.10* | *112* | *2.81x* |
| lib-stage2 | 0.139 | 0.145 | 0.04 | 117 | 1.01x |
| lib-stage2-concat | 0.145 | 0.147 | 0.19 | 109 | 1.02x |
| *mut-odo-aa-distant* | *0.149* | *0.245* | *2.52* | *99* | *1.00x* |
| liblist-stage2 | 0.151 | 0.157 | 0.25 | 116 | 2.02x |
| *mut-odo-aa-adjacent* | *0.151* | *0.252* | *1.60* | *99* | *1.00x* |
| mut-odo | 0.156 | 0.264 | 2.66 | 98 | 1.00x |
| *build-aa-distant* | *0.159* | *0.288* | *1.00* | *97* | *1.00x* |
| build | 0.160 | 0.283 | 1.23 | 97 | 1.00x |
| *build-aa-adjacent* | *0.169* | *0.293* | *2.95* | *97* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 0.36 | 73 | 24.76x |
| *list-aa-adjacent* | *1.002* | *1.014* | *0.28* | *73* | *24.76x* |
| *list-aa-distant* | *1.002* | *1.008* | *0.27* | *73* | *24.76x* |
| gen-unsafe | 1.078 | 1.323 | 2.85 | 75 | 1.00x |
| *gen-unsafe-aa-distant* | *1.092* | *1.348* | *1.40* | *74* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.094* | *1.279* | *2.54* | *75* | *1.00x* |

**Controls:** The largest A/A pair is `build-aa-adjacent` at 1.0572, worst cell
15.85% on `window-224x224-k3`, and 12 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0001 on a worst cell of 0.02% on `window-224x224-k3`,
its interval covering 1. The in-situ term reads 1.0044, 1.0039, 0.9847, 1.0394
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0493, which the correction amplifies
by 1.19x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m44s, peak 107 MiB in use, 24 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.48 ms per call raw, 9.21 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9):** `mut-odo-vecdims` 0.044/0.058/0.095
`bq-scan-rem-gm-mulback` 0.094/0.098/0.074

**Across the halves:** 27 of the 43 arms are faster on this half and 16 slower,
at a geomean of 0.9820, from `mut-odo-vecdims-add-in-leaf` at 0.8378
to `bcast-set` at 1.0449, with `list` itself at 1.0097. **The baseline moved
0.97% between the halves, past the 0.7% that lets two columns be differenced,
so this line is NOT read for the pair's variable.** The table above is one
process's and stands; what goes is the comparison.

**What the class says:** all three properties hold. `mut-odo-vecdims` reads
0.062, its highest of the nine classes bar `reshape1`, with `worst` 0.095
and `bq-expand` behind throughout. The head is `mut-odo-vecdims-add-in-leaf-u2`
at 0.033 --- **0.5278 paired and ahead on 3 of 3 shapes, a 47.2% margin against
this class's 5.72% floor** --- a family member, so the first clause holds.
The best arm outside the family is `lib-stage1` at 0.033, level
with the family's head, where Run 20 had `canon-vecdims` at 0.037. The floor
is `build-aa-adjacent`'s 5.72%, within three hundredths of Run 20's 5.75%.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one
strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *119* | *1.14x* |
| *canon-full-nosum* | *--* | *--* | *0.14* | *144* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.07* | *125* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| mut-odo-vecdims-add-in-leaf | 0.028 | 0.032 | 0.08 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.029 | 0.032 | 0.11 | 126 | 1.00x |
| canon-vecdims | 0.030 | 0.032 | 0.08 | 126 | 1.00x |
| mid-copy | 0.031 | 0.033 | 0.08 | 126 | 1.00x |
| canon-full | 0.031 | 0.032 | 0.08 | 126 | 1.00x |
| canon-memcpy-r2 | 0.031 | 0.032 | 0.08 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.032 | 0.034 | 0.12 | 125 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.034 | 0.09 | 126 | 1.00x |
| lib-stage1 | 0.032 | 0.034 | 0.15 | 125 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.034* | *0.08* | *126* | *1.00x* |
| bcast-set | 0.032 | 0.036 | 0.07 | 126 | 1.00x |
| **mut-odo-vecdims** | **0.032** | 0.034 | 0.07 | 126 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.033* | *0.034* | *0.08* | *126* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.034 | 0.035 | 0.08 | 124 | 1.00x |
| *mut-odo-aa-distant* | *0.035* | *0.052* | *0.44* | *125* | *1.00x* |
| *build-aa-distant* | *0.035* | *0.050* | *0.49* | *125* | *1.00x* |
| build | 0.036 | 0.049 | 0.14 | 125 | 1.00x |
| *mut-odo-aa-adjacent* | *0.036* | *0.051* | *0.15* | *125* | *1.00x* |
| *build-aa-adjacent* | *0.036* | *0.049* | *0.23* | *125* | *1.00x* |
| mut-odo | 0.036 | 0.051 | 0.33 | 125 | 1.00x |
| liblist-stage1 | 0.046 | 0.062 | 0.22 | 121 | 2.00x |
| mut-flat-gm | 0.072 | 0.073 | 0.06 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.081 | 0.083 | 0.11 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.085 | 0.087 | 0.08 | 114 | 1.14x |
| bq-odo-gm-mulback | 0.090 | 0.092 | 0.08 | 113 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.091* | *0.092* | *0.04* | *113* | *1.04x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.091* | *0.093* | *0.05* | *113* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.094 | 0.05 | 112 | 1.04x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.094* | *0.04* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.094* | *0.07* | *112* | *1.04x* |
| bq-expand | 0.096 | 0.099 | 0.06 | 112 | 1.14x |
| *bq-expand-aa-adjacent* | *0.097* | *0.099* | *0.05* | *112* | *1.14x* |
| *bq-expand-aa-distant* | *0.097* | *0.099* | *0.06* | *112* | *1.14x* |
| offtab-scan-rem | 0.129 | 0.134 | 0.07 | 108 | 2.00x |
| lib-stage2-concat | 0.149 | 0.150 | 0.05 | 105 | 1.00x |
| lib-stage2 | 0.149 | 0.150 | 0.04 | 105 | 1.00x |
| liblist-stage2 | 0.162 | 0.162 | 0.16 | 104 | 2.00x |
| gen-unsafe | 0.929 | 1.793 | 2.10 | 68 | 1.00x |
| *gen-unsafe-aa-distant* | *0.944* | *1.790* | *2.35* | *68* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.960* | *1.874* | *1.22* | *68* | *1.00x* |
| *list-aa-distant* | *1.000* | *1.013* | *0.19* | *71* | *19.43x* |
| list (baseline) | 1.000 | 1.000 | 0.28 | 71 | 19.43x |
| *list-aa-adjacent* | *1.003* | *1.012* | *0.22* | *71* | *19.43x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0330, worst
cell 4.51% on `scaled-r5`, and 7 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9993 on a worst cell of 0.24% on `scaled-super-r3`, its interval
covering 1. The in-situ term reads 1.0145, 1.0213, 1.0076, 1.0101 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0315, which the correction amplifies by 1.05x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h12m44s, peak 116 MiB in use, 37 MiB max residency;
the reader reads 49 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.96 ms per call raw, 4.77 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1,
scaled-r5):** `mut-odo-vecdims` 0.028/0.034/0.033 `bq-scan-rem-gm-mulback`
0.092/0.090/0.094

**Across the halves:** 28 of the 43 arms are faster on this half and 15 slower,
at a geomean of 0.9815, from `mut-odo-vecdims-add-in-leaf` at 0.8562
to `gen-unsafe-aa-distant` at 1.0413, with `list` itself at 0.9941.

**What the class says:** all three properties hold, and this is again the class
where the family's margin is smallest. `mut-odo-vecdims` reads 0.032
with `worst` 0.034 --- nearly the same figure, this class's cells being
that uniform --- and `bq-expand` trails it. The head
is `mut-odo-vecdims-add-in-leaf` at 0.028, **0.9252 paired and ahead on 2 of 3
shapes, 7.5% against this class's 3.30% floor**, so it clears by a margin rather
than by the factor it clears by elsewhere; a family member again, so the first
clause holds. The best outside the family is `canon-vecdims` at 0.030, against
`canon-full` at 0.031 in Run 20. The floor is `gen-unsafe-aa-adjacent`'s 3.30%,
against Run 20's 3.01%, so this class holds the run's tightest floor
for a second run and moved three tenths of a point doing it, while the run's
floors as a whole roughly doubled.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1
throughout: regime 2, which the library reaches by a route of its own,
and the population the rework's question needed.** Shapes: `runs-2` (`l`
1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row),
`runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-96` (`l`
1800000, `sInner` 96 --- an image row), `runs-1024` (`l` 1799168, `sInner`
1024), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs),
`runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs
of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class
is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *52* | *1.15x* |
| *canon-full-nosum* | *--* | *--* | *0.51* | *77* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.42* | *57* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| mut-odo-vecdims-add-in-leaf | 0.029 | 0.030 | 0.32 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.029 | 0.031 | 0.31 | 58 | 1.00x |
| canon-vecdims | 0.029 | 0.063 | 0.68 | 58 | 1.00x |
| canon-full | 0.031 | 0.102 | 0.76 | 59 | 1.00x |
| canon-memcpy-r2 | 0.031 | 0.097 | 0.65 | 59 | 1.00x |
| mid-copy | 0.032 | 0.063 | 0.47 | 58 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.064* | *0.05* | *58* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.032* | *0.063* | *0.07* | *58* | *1.00x* |
| mut-odo-vecdims-add-in | 0.032 | 0.063 | 0.08 | 58 | 1.00x |
| **mut-odo-vecdims** | **0.032** | 0.063 | 0.09 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.033 | 0.034 | 0.46 | 57 | 1.00x |
| bcast-set | 0.035 | 0.068 | 0.63 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.036 | 0.038 | 0.47 | 56 | 1.00x |
| *build-aa-adjacent* | *0.042* | *0.135* | *0.78* | *57* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.043* | *0.149* | *0.63* | *57* | *1.00x* |
| mut-odo | 0.043 | 0.158 | 0.73 | 57 | 1.00x |
| build | 0.043 | 0.133 | 0.60 | 57 | 1.00x |
| *mut-odo-aa-distant* | *0.044* | *0.144* | *0.54* | *57* | *1.00x* |
| *build-aa-distant* | *0.047* | *0.152* | *0.66* | *57* | *1.00x* |
| mut-flat-gm | 0.072 | 0.075 | 0.50 | 49 | 1.03x |
| liblist-stage2 | 0.081 | 1.135 | 0.63 | 55 | 1.21x |
| bq-mut-runs-gm-mulback | 0.082 | 0.088 | 0.53 | 47 | 1.03x |
| bq-expand-gm-mulback | 0.083 | 0.086 | 0.57 | 47 | 1.15x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.087* | *0.091* | *0.68* | *47* | *1.04x* |
| bq-odo-gm-mulback | 0.087 | 0.091 | 0.58 | 47 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.089* | *0.092* | *0.03* | *47* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.094* | *0.101* | *0.60* | *46* | *1.03x* |
| **bq-scan-rem-gm-mulback** | **0.094** | 0.101 | 0.59 | 46 | 1.03x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.102* | *0.04* | *46* | *1.03x* |
| *bq-expand-aa-adjacent* | *0.096* | *0.100* | *0.70* | *45* | *1.15x* |
| bq-expand | 0.096 | 0.100 | 0.68 | 45 | 1.15x |
| *bq-expand-aa-distant* | *0.097* | *0.101* | *0.03* | *45* | *1.15x* |
| lib-stage1 | 0.124 | 1.335 | 0.54 | 53 | 1.28x |
| liblist-stage1 | 0.125 | 1.371 | 0.49 | 53 | 1.28x |
| lib-stage2-concat | 0.125 | 1.338 | 0.53 | 52 | 1.31x |
| offtab-scan-rem | 0.136 | 0.149 | 0.82 | 41 | 2.00x |
| lib-stage2 | 0.151 | 0.158 | 0.61 | 40 | 1.00x |
| *gen-unsafe-aa-distant* | *0.701* | *1.022* | *2.75* | *21* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.709* | *1.076* | *2.82* | *21* | *1.00x* |
| gen-unsafe | 0.727 | 1.039 | 2.39 | 21 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 1.64 | 17 | 19.43x |
| *list-aa-distant* | *1.010* | *1.021* | *1.77* | *17* | *19.43x* |
| *list-aa-adjacent* | *1.029* | *1.048* | *0.24* | *17* | *19.43x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 0.9650, worst
cell 10.26% on `runs-3`, and 9 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9997 on a worst cell of 0.35% on `runs-9`, its interval covering 1.
The in-situ term reads 1.0310, 1.0148, 1.0344, 1.0219 of `sum-only` as medians,
on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 0.9668, which the correction amplifies by 1.05x --- quote both wherever
that is past 1.5.

**Provenance:** elapsed 0h29m50s, peak 361 MiB in use, 147 MiB max residency;
the reader reads 49 benchmarks over 7 shapes of the runs class. Anchor:
`runs-2`, `list` at 38.4 ms per call raw, 37.3 ms net.

**Per shape, in the lead's order (runs-2, runs-3, runs-9, runs-96, runs-1024,
runs-65536, runs-r3-48x30):** `mut-odo-vecdims`
0.063/0.052/0.034/0.028/0.028/0.027/0.030 `bq-scan-rem-gm-mulback`
0.101/0.098/0.094/0.091/0.090/0.093/0.092

**Across the halves:** 23 of the 43 arms are faster on this half and 20 slower,
at a geomean of 0.9820, from `mut-odo-vecdims-add-in-leaf` at 0.8349
to `gen-unsafe-aa-adjacent` at 1.0676, with `list` itself at 0.9993.

**What the class says:** properties 1 and 3 hold for the fix, and the class
exists to price the library rather than the fix --- which it does, twice over.
`mut-odo-vecdims` reads 0.032 with `worst` 0.063, that worst being `runs-2`,
and it leads every library-shaped arm from `runs-2` to `runs-1024` ---
but not at the top of the sweep: at `runs-65536` `lib-stage1` reads 0.0244
of `list` against the fix's 0.0274, and at `runs-r3-48x30` 0.0269 against
0.0296, so a long enough run is one a memcpy wins and an odometer fill does not.
The table's own head is `mut-odo-vecdims-add-in-leaf` at 0.029, **0.8027 paired
and ahead on 4 of 7 shapes, a 19.7% margin against this class's 3.50% floor**,
a family member, so property 2's first clause does not break. **What the class
was built for is the two rows near the foot.** `lib-stage2` reads 0.151
with `worst` 0.158 --- flat, because the branch fills every run whatever
its length --- while `lib-stage1` reads 0.124 with **`worst` 1.335**,
and that `worst` is the class's finding: at `runs-2`, which is 900000 runs
of two elements, the shipped slice-per-run concatenation is a third SLOWER
than the `list` baseline it exists to beat, and `lib-stage2-concat` (1.338)
and `liblist-stage1` (1.371) carry the same cell for the same reason. So the two
routes cross between `runs-9` and `runs-96`, and neither is right on both sides
of that crossing. The floor is `gen-unsafe-aa-distant`'s 3.50%.



## Provenance

What this run's figures have to be read against, and it is a section
of this file because a run replaces every word of it. What does NOT move
with a run --- the delta chain that says which shape set and roster each run
measured, and the list of what a run replaces outside this file --- is [README's
own Provenance][prov].

**Run 21's halves differ in the compiler, as Run 19's and Run 20's did,
and the pair is the third reading of that variable.** `run21-g912`
is ghc-9.12.4, the default on PATH here; `run21-ghead` is the in-tree stage1
of the GHC checkout under `~/r/horde-ad/ghc` at `d415f38a75`, reporting
10.1.20260803 and unmoved since Run 19 was built. Both took
`-fspec-constr -fobject-determinism`, the max-skip shim with its look-through
at `align-as.py` `40f7a37`, and `-fforce-recomp` into a fresh `--builddir`;
the HEAD half went through `cabal.project.ghead`, whose freeze pins
`criterion ==1.6.5.0`, `vector ==0.13.2.0` with `+boundschecks -unsafechecks`
and `hashable ==1.5.0.0` at the same index-state `cabal.project.freeze` holds,
`2026-07-25T13:22:10Z`. So the two plans differ in the boot libraries
and in nothing else a freeze can see, and what the pair prices is a consumer's
build on GHC HEAD, library code recompiled included. **`list` moved 0.64%
between the halves, INSIDE the 0.7% bar**, where Run 20 read 0.71% and Run 19
0.78% and both were refused --- so this is the first of the three whose two
columns may be differenced rather than only ordered, by a hair, and two routes
agree on the figure to four decimals. On the classes it is not so: `rev`
at 1.0126, `bcastmid` at 1.0137 and `window` at 1.0097 are past the bar,
and those three blocks say so in their cross-half lines.

**The sequence was launched once and ran to the end, and no population
was rerun.** `run-major.sh run21` started 2026-08-28T23:31:03 and its last
process finished 2026-08-29T07:35:03, 8h04m, twenty processes
with `WILDLOG=1 SATURATE=1` on the launch line and both switches read back off
the driver's own record rather than off the command typed. Every process exited
0 at the count its roster holds --- 1176 twice, 343 twice, 196 four times
and 147 twelve times --- and no process reported a selection it did not ask for.
The eighteen class processes span 12m41s to 29m53s. **The per-sample instrument
found no intrusion**: no bench in any of the twenty reached 0.25 foreign CPU,
and the plateau gate reads all twenty preamble victims inside 19.70 to 20.55
ms/iter, a 4.30% spread against a 5% band. So post-run step 1c is owed nothing,
where Run 20 had to rerun two populations on both halves after its last four
processes met the machine's owner. **The control half ran first throughout**,
`ghead` before `g912` on the main set and on each class in turn, which
is the driver's order.

**The pair's own identity, transcribed before its note goes with it.** The two
binaries are `run21-g912`, md5 `80f1dae4493b44cffd38ea30f78095ab`, `.text`
20488389 bytes, and `run21-ghead`, md5 `248f599a0579f8e06913b7ca6895192e`,
`.text` 20637503 bytes --- 36864 and 40960 bytes above their Run 20
counterparts. Both were built from `Main.hs` at `70ef2de`, the tip,
with `align-as.py` at `40f7a37` under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1`;
the tree at launch was `ec45334` with eight untracked scratch paths and nothing
modified. They carry `ghc-internal-9.1204.0` and `ghc-internal-10.100.0`,
criterion 1.6.5.0 on both, and the baked `-with-rtsopts=-A32m -I0 -T -M8G` read
back by `+RTS --info` on each. **The gate passed on 2026-08-28**, four processes
at 120 benches each in the palindrome, its two readings agreeing in direction
on all three timed arms and to within two thirds of a point; its machine check
read -0.33% on `list`'s net over 24 of 24 shapes against the fingerprint Run 20
kept, so the box did not move. **And the fills were NAMED**, which no run before
Run 17 could do and which this one owes to post-run step 11: two `-g3` twins
rebuilt from these same recipes put the basis's six-copy group at `fbMidCopy`,
`fbMutOdoVecdimsAddIn`, `fbMutOdoVecdims`, `fbMutOdoVecdimsAddOut`,
`fbMutOdoVecdimsAddBoth` and `fbCanonVecdims`, and its two-copy group
at `fbBuild` and `fbMutOdo`. On the basis the twin locates as well as names ---
three of the six addresses are the timed binary's to the byte and the rest sit
0x40 below at the same offsets --- while on HEAD it names without locating,
as Run 19 recorded of that compiler, so on that half the membership is read
and no offset is assigned to an arm.

**The roster moved and nothing else in the inputs did**, which is this run's one
departure from what a compiler pair wants, and the second run running that has
to say it: 1176 benches, 49 timed arms over the same 24 main-set shapes, six
classes at three shapes, two at four and one at seven, with both halves'
`--list` listings identical to each other and NOT to `run20-g912`'s 1272. Six
timed arms landed --- the `-u2-down` leaf variant, the three library-shaped arms
and the two list-consumer ones --- and TEN names left, eight arms parked
permanently on 2026-08-28 together with `offtab`'s two A/A twins, so the floor
reads over sixteen pairs rather than eighteen. The `runs` class is new
and brings seven shapes and 343 benches a process. **So the `-L1` roster pass
was owed and was taken**, on this roster, before the gate: 1176 benches
over the main set, a three-shape class beside it and a `runs` leg added because
no reader mode had ever seen that class, every reader mode exercised over all
three. **What the change costs is stated wherever a figure crosses the Run 20
boundary**: new functions move every address, so no cross-run figure here
is drift alone, and the build-time fill reading found no tracked address
surviving between the two builds.

anchors read **5.92 us** on `cnn-slice-c32`, **3.05 ms** on `cifar-L2-16-c64-k3`
and **37.9 ms** on `stretch-wide-2xM`, net per call on the basis half, against
Run 20's 5.94 us, 3.09 ms and 38.2 ms --- **-0.37%, -1.53% and -0.73%**, derived
from both runs' cells rather than from either printed table, Run 20's JSONs
still being on disk to derive from. Its own published figures reproduce
from them first, 5.94 us and 3.09 ms to the digit and 38.15 ms where it printed
38.2, so the method agreed with Run 20's before it was used on Run 21. All three
are well inside this run's 2.92% floor, and the gate's machine check over all 24
shapes read -0.33% with a worst of -3.52%, so the box is flat and what movement
there is sits under the roster change's layout term. **The control half's three
are 5.92 us, 3.04 ms and 37.3 ms**, 0.09%, 0.09% and 1.55% under the basis's.

| shape | `l` | `list`, per call | net | HEAD, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.09 us | 5.92 us | 5.92 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.14 ms | 3.05 ms | 3.04 ms |
| `stretch-wide-2xM` | 1800000 | 39.0 ms | 37.9 ms | 37.3 ms |

**Each stride class carries an anchor of its own, beside its table, and all
eight that Run 20 also measured are inside their own class's floor against
it --- six of them inside a point.** They run **-0.67% to +1.70%**,
`reshape1-500k` at the far end and `scaled-rank1-m1` at the near one, every one
inside its class's floor: the widest movement, `reshape1`'s +1.70%, sits against
that class's 6.31% floor, and `bcast-inner900`'s +1.07% against 6.56%.
**The ninth anchor is new and has nothing to move against**: `runs-2`, `list`
at 37.3 ms net per call, the first reading of that class. So a class anchor
is comparable across this boundary, with the caveat every cross-run figure here
carries: the roster moved, so a movement is drift plus a layout term
and not drift alone --- and unlike Run 20, no anchor here is past two points
in either direction, its `bcastmid-b200k` exception at +3.93% having come back
to -0.58%. What they cannot be compared across is still the Run 17 boundary,
where the BIOS sits.

**The correction is invertible, so pre-correction figures stay comparable.**
The forcing term is **0.596--0.613 ns per element** on the basis half
and 0.599--0.614 on the control, over all 24 shapes, so a raw slope
is the published one plus about `0.61e-9 * l`, with `l` from `Main.hs`.
That recovers any uncorrected figure to within the term's own spread --- enough
to hold a corrected run against any number measured before the correction
existed. The term is within about 2% of every run's since Run 7, so neither
the flag, the roster, the layout, the shim's padding, `-fproc-alignment=64`,
an RTS line, a source patch that moves every loop offset, **nor a change
of compiler** touches the forcing pass, which is the control saying every run's
correction is one correction --- and this pair's two halves agree on
it to within a thousandth of a nanosecond, so a figure differenced across
these halves carries almost none of its own. **The fourth arm of the control,
added at Run 20, reads it again**: `canon-full-nosum`, whose write pattern
varies by shape where the three standing ones are element-wise fills, reads
1.0204 and 1.0198 of `sum-only` against the others' 1.0043 to 1.0768
on the basis and 1.0256 to 1.0677 on the control --- so on the basis it sits
inside their span, as it did on both of Run 20's halves, while on the control
it sits just BELOW all three rather than apart from them the other way. The hole
the sum-only section names --- a fill whose write pattern leaves the cache
in a quite different state being summed at a cost `sum-only` misses ---
is therefore not open on the one arm built to look for it, on two runs.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance
