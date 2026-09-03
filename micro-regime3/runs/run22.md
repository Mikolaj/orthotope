# Run 22 (SpecConstr)

One run's write-up: its head, its Results, what the next run compares against,
the claims that run should test, the nine class blocks, and its own Provenance.
A run replaces this file whole and edits [README.md](../README.md) around it,
in the score of places [the replace list under Provenance there][prov] names ---
the open list among them, which is where a run's surprises go and where
its registrations keep a verdict and a pointer --- the registrations themselves
being in this file since 2026-08-29, in the section at its foot. So this file
is most of what a run replaces and by no means all of it. What stands between
runs is the harness, [the procedure][procedure] that makes a file like this one,
and the rulings a measurement does not reach.

**Run 22 (SpecConstr), and what the unboxing and the doubled cursor are worth
at full budget: the branch's fourfold regime-3 regression is gone.** Criterion,
**`--ghc-options=-fspec-constr`**; Run 21's regime, recipes and basis,
and **what moved is the source, the roster and the shape set**: 1320 benches, 55
timed arms over 24 main-set shapes, and 2035 more over 37 class views
in **nine** classes, where Run 21 ran 49 arms, 1176 and 1617 over 33. Six timed
arms landed and none left --- the run-length dispatch `lib-stage2-disp`,
the three fill candidates `lib-stage2-u4`, `lib-stage2-short`
and `lib-stage2-lean`, and the unordered entry point's `libunord-stage1`
and `libunord-stage2` --- and the `runs` class took `runs-4`, `runs-5`,
`runs-256` and `runs-512`, going from seven views to eleven. **The basis
is the 9.12 half**, `run22-g912`: Run 21's basis recipe with only the source
and the shim moved, carrying `-fobject-determinism`, the per-sample instrument
and the saturating preamble, both halves under `WILDLOG=1 SATURATE=1`.
**The control is `run22-ghead`**, the same source and the same shim built
by the in-tree stage1 of the GHC checkout at 10.1.20260803 through
`cabal.project.ghead` --- so the halves differ in the compiler and its boot
libraries and in nothing a freeze can see, and what they price is a consumer's
build on GHC HEAD, library code recompiled included. The binaries carry
`ghc-internal-9.1204.0` against `ghc-internal-10.100.0`, criterion 1.6.5.0
on both, and `.text` of 20512965 against 20657983 bytes. md5
`9bac6d77a913f139171430874f99b985` for the basis
and `7a86094800e76ddd6e0ee31b4825761e` for the control, from `Main.hs`
at `0add4f4` and `align-as.py` at `c57e5c4`; the tree at launch was `bd8493c`,
with four untracked scratch paths and nothing modified. The same desktop, Zen 3,
a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main
processes read *1h53m50s* and *1h54m15s*, at *340 MiB* in use and *126 MiB* max
residency on the basis against *384 MiB* and *120 MiB* on the control.

**The basis half is not a repetition, and this run gave up that instrument
on purpose for the third time running.** Six timed arms landed since Run 21
was built and none left, so every address moved and neither half can reproduce
its Run 21 counterpart byte for byte; the md5 comparison and the three-read hunt
a moved md5 usually triggers were both taken off for this run, decided
2026-08-30, so a differing md5 here is what the roster change predicts and
not a finding. **And this run it is stronger than a roster change alone**,
because seven of Run 21's columns are different CODE: `fillStage2` unboxed
its source vector and now steps its cursor twice, which reaches `lib-stage2`
and `lib-stage2-concat` through the call; `lib-stage2-concat`, `liblist-stage2`,
`-add-in-leaf-u2` and `-u2-down` changed in their own bodies; and `lib-stage1`
and `liblist-stage1`, byte-identical in their own texts, fall back
to `-add-in-leaf-u2` on every regime-3 view. So no distance from Run 21's column
on any of those seven is drift or layout at all. The build-time reading
of the fills says how far the addresses went: `run21-g912` held its six-copy
group at `[0, 0, 24, 0, 0, 8]` and `run22-g912` holds one
at `[0, 0, 24, 0, 0, 24]`, no tracked address surviving and none moved
by a constant, five of the six mod-64 offsets those Run 21 held and the sixth
--- `fbCanonVecdims`, named at post-run step 0 --- moved from 8 to 24.

**What holds the build to something instead is four readings that survive
a relink.** The gate's machine check reads **-0.87%** on `list`'s net against
the fingerprint Run 21 kept, over 24 of 24 shapes, worst `stretch-primes` -1.66%
and none past 5%; the run's own main-set process reads the same comparison ---
`--machine` with `--run-doc` pointed at the fingerprint Run 21 kept, a plain
`--machine` reading this run's own instead and giving -0.03% --- at **+0.08%**,
worst `stretch-r5-8x432` +1.85% --- two readings against the SAME kept
fingerprint rather than two instruments, both inside 3%, so the box measures
as it did and no absolute is re-baselined. The 43 arms both halves and Run 21
all give a corrected time read against Run 21's columns, with the caveat above:
seven of them are changed code and the rest carry a layout term nothing here
separates. Each half's own sixteen A/A pairs give it a floor. **And the counted
work is the fourth and strongest**: `bq-odo-gm-mulback` reads a count ratio
of **0.9340** where Runs 19, 20 and 21 all read 0.9340,
and `bq-scan-rem-gm-mulback` **0.9422** against 0.9422, 0.9423 and 0.9422 ---
four figures across three roster changes, on an instrument that owes criterion
nothing.

**The manifest's one surviving claim held on the basis, and the ladder
is unmoved.** Claim 1's four registered links all hold: `mut-odo-vecdims` /
`mut-flat-gm` **0.6448** at 21 of 24 and sign p 0.00028, `mut-flat-gm` /
`bq-mut-runs-gm-mulback` 0.9210 at 23 of 24, `bq-mut-runs-gm-mulback` /
`bq-odo-gm-mulback` 0.9158 at 20 of 24, and `bq-mut-runs-gm-mulback` /
`bq-scan-rem-gm-mulback` 0.9175 at 17 of 24 --- 4 of 4, a fifth clean sweep
running, on a roster the manifest had not been read on and a build whose every
address moved. Every figure is within a few thousandths of Run 21's on the links
they share.

**What the compiler is worth changed sign, and most of the change
is those degenerate arms rather than the roster.** Over the 49 arms compared
the basis half reads a geomean of **1.0168** against the control, 17 below 1
and 32 above --- where Run 21 read 0.9920 at 22 below and 21 above over 43. Drop
the two `libunord` arms, whose two halves cover 23 and 20 shapes and which read
1.3441 and 1.2508, and the same comparison gives **1.0064 over 47 arms**, 17
below and 30 above. So HEAD is now a little ahead of 9.12 on this roster where
it was a little behind, and the honest size of that is under a point,
not the 1.7% the unrestricted geomean shows. **What did not change is which arms
HEAD runs faster on, and by how much.** `mut-odo-vecdims-add-in-leaf` heads
those again at **0.8465**, where Run 21 read 0.8481 and Run 20 0.8513,
and the two fastest pure builds follow with their A/A twins, `bq-odo-gm-mulback`
at 0.9275, 0.9273 and 0.9270 and `bq-scan-rem-gm-mulback` at 0.9411, 0.9400
and 0.9402 --- three copies moving together being the arm and not where one
of them landed, for a fourth run. **It does NOT head the movers outright,
and this run is the first where that distinction bites**: measured by distance
from 1 the three widest are `libunord-stage2` at 1.3441, `libunord-stage1`
at 1.2508 and `mut-odo-vecdims-add-in-leaf-down` at 1.2109, the first two being
the degenerate arms above and the third the variant registration 5 unseated. Run
21's sentence could say *heads the movers* because nothing then moved further up
than the leaf arm moved down; six new arms have made that false while leaving
the reading under it intact.

**Every one of the twenty processes gated clean**, `--selftest` and both `--aa`
gates, so no time column here is uncorrected. **This run's floor is 2.12%
on the basis half and 1.08% on the control**, against Run 21's 2.92% and 2.16%
--- so both ends tightened, on the same two recipes and the same box,
with the source and the roster the inputs that moved. The pair carrying
it is `build-aa-distant` on **both** halves this run, where Run 21 had
`mut-odo-aa-distant` and `gen-unsafe-aa-distant`, and the worst A/A cell
of either main set is **19.44%** on `stretch-r5-8x432` on the basis against
**14.40%** on `stretch-inner1` on the control, where Run 21 read 22.86%
and 14.47%. Restricted to the six pairs that carry back to Run 10 the two read
**0.37%** and **0.51%**, against Run 21's 0.46% and 0.60%. **Which of the two
a margin is judged against depends on what it compares**: an arm against its own
duplicate against 2.12% and 1.08%; two different arms against the six-pair
figures. Neither is judged against the predecessor's, which is the rule
this README has restated at every run since Run 19 and which this run neither
strengthens nor weakens --- it is the third consecutive run of one recipe on one
box whose floor moved for no isolated reason, 1.51%, 2.92%, 2.12%.

**The two halves' cells resolve differently again, and this run they very nearly
do not.** `CI%` --- the median half-width of a cell's own fit --- runs a geomean
of **1.01** on the basis against the control across the roster, **28 arms wider
here and 27 narrower**, where Run 21 read 1.02 at 34 and 15, Run 20 0.97 at 21
and 32 and Run 19 1.06 at 26 and 21. So the direction has now gone one way,
the other, back, and this run to an even split, which is what a quantity
with no stable sign looks like when it is finally read at a roster big enough
to say so. It remains a different quantity from the floor: sampling error inside
one bench against agreement between two placements of one strategy.

**This run's sequence ran in TWO WINDOWS and that is a fact about the evening
rather than about the measurement.** Eighteen of the twenty processes ran
unbroken from 01:57:43 to 09:53:49; the machine was then wanted by its owner,
so the sequence was stopped BY HAND at the `scaled`/`runs` boundary --- three
seconds into `run22-ghead-runs`, which had written a zero-byte log and no JSON
at all --- and the two `runs` processes were re-driven at 16:41:21 to 18:26:27
on a box measured 0.6% non-idle at launch. **The plateau gate is what says
the split cost nothing**: all twenty processes assert their preamble victim
inside **19.8075 to 20.3228 ms/iter, a 2.60% spread** against a 5% band, the two
late processes among them, so every process measured in the same in-process
state whatever the clock said. Both `runs` legs exited 0 at the 605 benches
their roster holds, each carrying its one `@@saturate` line and its `@@wild`
stamps. No population was rerun for an intrusion and post-run step 3 is owed
nothing.

**What this run was built to price is `fillStage2` after the unboxing
of 2026-08-29 and the doubled cursor of 2026-08-30, and the answer is that Run
21's headline regression has gone.** `lib-stage2` against `lib-stage1` ---
the branch against what ships --- reads **0.7400** on the main set, 0.8902
on `rev`, 1.0262 on `revsome`, 1.0344 on `slice`, 0.9849 on `scaled` and 0.8110
on `window`, where Run 21 read **2.4323, 4.0152, 4.5377, 4.0984, 4.0765
and 3.7237** on the same six populations. So a ratio that ran between
two-and-a-half and four-and-a-half is now between 0.74 and 1.03, and no regime-3
population reads the branch behind stage one by so much as four percent.
Registration 1 predicted the six inside **0.78 to 1.08** and named its kill
condition as any regime-3 population reading the branch behind by more
than a tenth; nothing came near it, and five of the six land inside
the predicted band with the main set below it, the branch being faster there
than the registration dared. The reading is one both of whose sides are changed
code --- stage one's regime-3 fallback is the re-stepped `-add-in-leaf-u2` ---
so it prices the two routes as they now are and not the fill against its old
self, which is what the registration said it would do.

**The crossover moved with it, and that is the sharper form of the same
result.** On the `runs` class `lib-stage2` / `lib-stage1` reads 0.0227, 0.0274,
0.0397, 0.0437, 0.0834, 0.5202, 0.7679, 0.8170, 0.9254, 1.1485 and 1.0364 across
`runs-2`, `-3`, `-4`, `-5`, `-9`, `-96`, `-256`, `-512`, `-1024`, `-65536`
and `-r3-48x30` on the basis, and 0.0230 to 1.1513 on the control.
**So the branch is now the better route at every length through `runs-1024`**
and behind only at `runs-65536` and `runs-r3-48x30`, where Run 21 had it behind
from `runs-96` up by factors of 2.9, 5.2 and 6.5. The crossover has therefore
moved from between `runs-9` and `runs-96` to between `runs-1024`
and `runs-65536` --- the bracket's lower edge moving 114-fold and its upper
683-fold, so the crossing itself went out by something near two hundred ---
and it moved by the same step on both compilers, the control reading 0.9601
at `runs-1024` against the basis's 0.9254.

**And that is what kills registration 3.** `lib-stage2-disp` cuts the slice
route in at a canonical run of `dispRun` or more with `dispRun` at 256, a number
chosen when the crossover sat between 9 and 96. It reproduces the filtered sweep
closely at the seven lengths that sweep read --- 0.0227, 0.0273, 0.0834, 0.5193,
0.9870, 1.0083 and 1.0102 against stage one, where 0.0283, 0.0312, 0.0951,
0.6190, 1.0029, 1.0096 and 1.0075 were registered --- but the registration's
kill condition is being behind the better route past the floor at any length
the sweep read, and at `runs-1024` the better route is now stage two
and the dispatch is **6.65%** behind it against a 3.26% class floor. **KILLED,
on the basis half, and killed on the control too** at 4.22% against 3.33%.
The threshold is not wrong in kind; it is a bracket's representative
and the bracket moved under it, the fill having become the better route three
lengths further out than when 256 was chosen. Two further readings say the same
thing from the other side: at `runs-256` and `runs-512`, the two lengths nothing
had read, the dispatch is 33.2% and 20.9% behind stage two on the basis, which
by the registration's own words re-cuts `dispRun` inside its bracket rather
than killing the dispatch --- but `runs-1024` is a read length and it kills.
**The half of registration 3 that held is the one nobody expected to**:
it predicted the control BEHIND `lib-stage2` at `runs-1024` by *about four
points*, and the control reads 4.22%. What is refuted is its reason ---
it expected the basis to be ahead there because 9.12's crossover sat earlier
than HEAD's, and both halves now put the crossover in the same place,
so the threshold's failure is not a compiler difference but the fill getting
faster on both.

**The three fill candidates were registered off counted work and filtered
probes, and time refuses all three.** `lib-stage2-short` --- a canonical run
of 2 to 5 elements written by a body of exactly that length --- was predicted
about 0.50 of `lib-stage2` at `runs-2` and 0.59 at `runs-3`, with `runs-4`
and `runs-5` bracketing them at 0.5528 and 0.6099 in counts. In time it reads
**0.8066, 0.9678, 0.8311 and 0.9407** at those four lengths: the win is real
and its direction is right, and it is a third to a sixth of the size the counts
predicted. Its kill condition was being behind past a population's floor
anywhere the counts put it at or below 1, and **it fires**. Its four cells above
1 on `runs` are inside that class's 3.26% floor --- `runs-9` 1.0010, `runs-256`
1.0135, `runs-512` 1.0112 and `runs-r3-48x30` 1.0230 --- but the MAIN SET
carries six more, and one of them is `stretch-inner1` at **1.0308**, 3.08%
behind against a 2.12% floor where this run's own counted work reads the arm
at 0.999997, at or below 1. **KILLED**, and the magnitudes refuted with it.
`lib-stage2-u4`, the stepping run unrolled by four, was predicted 0.83 to 0.85
at the long runs; it reads **0.9759 at `runs-65536`, 0.9916 at `runs-1024`
and 0.9821 at `runs-512`** --- ahead, but by 2.4%, 0.8% and 1.8% against
that class's 3.26% floor, so not ahead past it at any long length, which
is its own kill condition. **KILLED.** `lib-stage2-lean`, whose leaner dispatch
skips the strides comparison, was predicted at or below `lib-stage2` everywhere
and past a floor only on `cnn-L1-6x6-c1`, `cnn-slice-c32` and `stretch-inner1`.
Two of those three hold and are the run's cleanest confirmation of a counted
reading: **0.8771 and 0.8565**, both far past the 2.12% main-set floor.
The third inverts. On `stretch-inner1`, where canonicalization collapses
the call to a slice and the counted sweep put the lean dispatch 21 points ahead,
it reads **1.0617** --- behind by 6.2%, past the floor, which is the kill
condition in the letter and in the direction nobody registered. **KILLED** ---
and the sign disagreement is the REGISTERING sweep's against this run's clock,
not this run's own: the shim-free sweep of 2026-08-30 put the arm 21 points
ahead there, while this run's counted work reads it at 1.0000, agreeing
with the clock that it is not.

**The unordered entry point is the registration that was evaluated rather
than predicted, and it came back exactly as evaluated.** `probe-oneblock.py` had
said stage two's one-block test fires on ten of the 37 rostered class views ---
every view of `rev`, `revsome` and `reshape1` --- and stage one's on none.
In time `libunord-stage2` against `liblist-stage2` reads **0.0197 on `rev`,
0.0081 on `revsome` and 0.0064 on `reshape1`**: degenerate on precisely
those three whole classes and nowhere else. On the six classes where neither
test fires it reads 0.9867, 1.0013, 1.0239, 1.0256, 1.0185 and 0.9999
on `bcast`, `bcastmid`, `slice`, `window`, `scaled` and `runs`, every one inside
that class's own floor, and `libunord-stage1` tracks `liblist-stage1` the same
way. Killed by a margin past the floor on any of the six, or by stage two
not collapsing on `rev`: neither happened. **HELD**, and it is the only one
of the five registrations that neither moved nor surprised.

**The vecdims ordering reverses Run 21's and splits on one cell.** Run 21 read
`-add-in-leaf-down` ahead of the shipped `-add-in-leaf-u2` by 5.6% and 6.7%
on its two halves, and this run predicted `-u2` ahead everywhere past each
population's floor. On the basis it is, in all ten populations, from **0.6686**
on `reshape1` to 0.8522 on `scaled`, with the main set at **0.7938 at 23 of 24
shapes, sign p 3e-06**. On the control it is ahead in nine of the ten.
**The tenth is `bcast`, where `-down` is ahead at 1.1306 on 0 of 3 shapes**, 13%
past that class's own control floor of 2.79% --- which is the registration's
kill condition, fired on exactly one population of twenty. So the verdict
is a SPLIT: the in-process re-take of 2026-08-30 was reading the change
and not a displacement, on nineteen of twenty populations, and the twentieth
says the reversal is not yet unconditional. `-u2` against `-u2-down`
was predicted a tie inside the floor and is one, 1.0004 on the basis at 12 of 24
and 1.0091 on the control, both inside.

**The roster pass warned that some cells would sink below the shared forcing
pass, and at full budget they do --- far fewer on the basis than it predicted
and far more on the control, which nothing had looked at.** An arm whose
one-block test or whose canonicalization collapses the view to a single
`VS.slice` can cost less than the correction's own pass, and such a cell cannot
be corrected: it reads `--` and its row becomes a geomean over fewer shapes.
The `-L1` pass of 2026-08-30 saw eight such cells on the basis and predicted
three short rows. **The basis at full budget has two**, `libunord-stage1`
and `libunord-stage2`, each over 23 of 24 shapes. **The control has seventeen,
across eleven rows** --- `canon-full`, `canon-memcpy-r2`, `canon-vecdims`
and all six `lib-stage2*` arms over 23 of 24, and the two `libunord` arms
over 20 of 24 --- because on HEAD `stretch-inner1` sinks for every
canonicalizing arm. That is a structural fact about this run's Results table
and not a defect in it: **the `time` column no longer rests on every row
covering one population**, and each affected row says what it covers. It also
bites the reader: `lib-stage2` against `lib-stage1` is **not readable at all**
on the control main set, one cell having no positive net, which is why
registration 1's main-set figure above is the basis's and its cross-compiler
check is taken on the classes instead.

**The counted work cuts those movements in two and reproduces the previous three
runs to four figures.** `bq-odo-gm-mulback` reads a count ratio of **0.9340**
where Runs 19, 20 and 21 all read 0.9340, and `bq-scan-rem-gm-mulback`
**0.9422** against 0.9422, 0.9423 and 0.9422 --- four runs and three roster
changes on an instrument that owes criterion nothing --- so the fast pure tier's
whole loss is codegen, with time-over-counts at 0.9931 and 0.9988. **What
is not codegen** is the placement-exposed family, at count ratios of **1.0000**
to four figures on `build`, `mut-odo` and `gen-unsafe`, exactly as Runs 18
through 21 found them, so their time movements of 7.32%, 3.91% and 6.83%
are layout or the runtime and not code. `mut-odo-vecdims-add-in-leaf` reads
0.8971 on the counts against 0.8465 in time, as Run 21 read 0.8971 against
0.8481, and `canon-full` 0.9712 against 1.0004, where Run 21 read 0.9712 against
1.1241 --- the same count, a time that moved twelve points, which
is the rework's arms settling rather than the compiler changing its mind.

**The counted work covers every population, and the class picture is the one
Runs 20 and 21 drew.** Twenty sweeps, both halves over all ten populations, 165,
220, 605 or 1320 cells apiece and no cell perf refused anywhere in the twenty
files. **Eight of the nine classes read as the main set does** --- every arm
together at a count geomean of 0.9815 to 0.9972, HEAD emitting about a percent
more --- while **the ninth sits apart at 1.0026**, above 1, so on that class
9.12 emits slightly more than HEAD. That ninth is `reshape1`, as it was Run 21's
ninth at 0.9990 and Run 20's eighth at 0.9995: the class HEAD does not cost,
on three runs, and the first run in which it crosses. `window` is the runner-up
at 0.9972, as it was at 0.9934 and 0.9918. These nine are taken as Runs 20
and 21 took theirs, the geomean over every arm the sweep carries, controls
included, which is 55 here and was 49 and 53 there. **The lowest count ratio
in all nine classes belongs to the same arm and it is the one Runs 20 and 21
named**, `mut-odo-vecdims-add-in-leaf`, from 0.8649 on `runs` to 0.9286
on `reshape1`, where Run 21 read 0.8653 to 0.9286 --- the same arm and the same
far end to four figures over a roster change. It is not the widest DEVIATION
in every class, `-add-in-leaf-down` sitting further from 1 in two of the nine,
`reshape1` and `window`, which is a distinction Run 21's phrasing did not have
to make.

**The unit-innermost-extent rule was registered as a mechanism claim,
and a third run has now declined to kill it.** Wherever `sInner` is 1,
`bq-odo-gm-mulback`'s HEAD penalty is absent: `stretch-inner1` reads **1.0000**
on the counts, to four figures, as it did on Runs 20 and 21. Everywhere else
it runs **0.9149 to 0.9701** --- the identical range both those runs published
--- and the far end of it is again `stretch-rank12` at `sInner` 2, the one shape
between absent and the band, which is what a graded effect looks like rather
than a switched one. Run 19's kill condition was any `sInner` of 1 that shows
the penalty, and none does. What this still is not is a reading of the code,
so the claim stays registered rather than settled. **And it is hand-rolled,
which is a defect report against the reader**: `--counts` aggregates per arm
and prints no per-shape column, so this run computed the ratios from the two
counts files directly. By this README's own rule that is the reader's gap
to close, not a licence to keep computing it here.

**And the correction sits on nearly the same footing in both halves, as it has
on every run since Run 17.** The in-situ forcing term --- an arm minus
its `-nosum` twin, against the `sum-only` the correction actually subtracts,
read off `--aa`'s `ratio` column --- reads 1.0256, 1.0225, 1.0371 and 1.0754
on the basis and 1.0266, 1.0225, 1.0278 and 1.0722 on the control,
on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm` and `bq-expand`. So both
halves subtract a term between two and eight points under the in-situ pass,
every one of the eight figures tilting the same way, and the two halves agree
with each other to within **0.10, 0.00 and 0.32** of a point
on `mut-odo-vecdims`, `canon-full` and `bq-expand` --- `canon-full` reading
identically on both to four figures. `mut-flat-gm` is again the one where they
part in size rather than direction, 1.0371 against 1.0278. **A margin between
these two halves is therefore not carrying a correction bias**, which rests
on the term the correction actually subtracts rather than on the in-situ check:
the two `sum-only` halves agree at **1.0003** on the basis and **1.0000**
on the control, both intervals covering 1.

**The run's standing placement pair moved again, and this run it changes sign
on BOTH halves against Run 21.** `build` against `mut-odo`, one worker at two
slots, reads **1.0125 at 10 of 24, sign p 0.54** on the basis --- a tie ---
and **0.9803 at 17 of 24, p 0.064** on HEAD, where Run 21 read 0.9870 and 1.0764
and Run 20 read 0.9899 and 0.9668. So `build` is the slower slot on 9.12
and the faster on HEAD, which is Run 21's arrangement inverted on both sides,
and the gate had already said so before the sequence ran: its two passes read
1.0086 and 1.0226 on the basis and 0.9763 and 0.9635 on the control, five
benches apiece and the same signs. Their per-shape ranges remain the finding
rather than their geomeans, **0.919..1.129** on the basis and **0.865..1.126**
on the control. **`mut-odo`'s own A/A twins moved with it and in opposite
directions on the two halves** --- 1.0059 and 1.0034 on the basis and 0.9993
and 0.9895 on the control, PAIRED figures, which for this pair carry
the opposite SIGN to the published column the table prints, 0.9940 and 0.9861
against the base's own row. The pair is capped, which is the one case the two
statistics part; read the table for the column and these for the pair, and never
the two as one picture --- so `mut-odo`'s base slot is the fast one on 9.12
and the slow one on HEAD, and the pair above is reading that rather
than anything about the two workers. Post-run step 0 named the two-copy group
off a `-g3` twin again --- `fbBuild` at `0x423e00` and `fbMutOdo` at `0x42ed40`,
both at offset 0 on both halves and at addresses identical in twin and timed
binary --- so what separates these two slots is not where the tracked loop
landed. The counted work agrees it is not code: both arms read a count ratio
of 1.0000 to four figures.

**The ceiling reproduced for a sixth run, on the arm the class property names.**
`mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm needing
nothing at all, reads **0.5449 at 23 wins of 24** and sign p 3e-06 on the basis,
against Run 21's 0.5424, Run 20's 0.5479, Run 19's 0.5572, Run 18's 0.5577, Run
17's 0.5446 and Run 16's 0.5567 --- the figure [the
ruling](../README.md#the-mutable-ceiling-taken) turns on, unmoved by a third
consecutive roster change that moved every address. On HEAD it reads **0.5184**,
against Run 21's 0.5164, at the same 23 of 24 and the same p. Seven runs, three
compilers and four rosters have now put the basis reading between 0.5424
and 0.5577 and the HEAD one between 0.5159 and 0.5184.

**And this run's two columns MAY NOT be differenced, which reverses Run 21
and is the first refusal in three runs.** `list` moves **0.81%** between
the halves on the main set against the 0.7% bar --- past it, where Run 21 read
0.64% and called that a hair inside while preferring the within-run comparisons
anyway. So the cross-half figures here are read as an ordering and not
as a subtraction, and the counted work is what carries any claim about *why*
an arm moved. **The bar bites five of the nine classes too, overlapping Run 21's
three in two of them**: `bcastmid` at 1.0106, `reshape1` at 0.9900, `window`
at 1.0082, `scaled` at 0.9911 and `runs` at 1.0114 are past it, so those five
class blocks say in their cross-half lines that they are not read for the pair's
variable --- while `rev`, which Run 21 disqualified at 1.0126, is inside
it this run at 1.0069, as are `revsome`, `bcast` and `slice`.

**And the one straddling loop this run can name lies in the branch's own fill.**
The build-time reading found four self-loops straddling a cache line
in the basis half's `Main`-compiled code where Run 21 found none, and post-run
step 0's `-g3` twin can name exactly one of them: the 6-byte loop at `0x42207c`,
offset 60, which is byte-identical in the twin **at the same address** and which
the twin's DWARF puts inside `fillStage2`, in the `copies` loop that doubles
a canonical run by `unsafeCopy`. The other three are 63-byte bodies of which
the twin holds no byte-identical copy --- it carries 152 self-loops and one
straddler against the timed binary's 158 and four --- so they are not named
from it, and the source lines it offers at those addresses are discarded as read
off code that is not the same code. [What moves a figure when no strategy
changed](../README.md#what-moves-a-figure-when-no-strategy-changed) prices
a straddling loop as a per-element term; that it lands in `fillStage2`,
the function this run exists to price and the one whose code moved, is a thing
to hold against the next reading of that arm rather than a correction
to this one.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512`
on the basis, and 2408978 against 2408530 on the control, where plain -O1
separates the two tenfold. Those are Run 21's three figures to the byte, both
runs' preflight having asked the basis alone while both notes record the pair.
With no rebuild between the gate and the sequence, that is the only check
standing between a mistyped regime and the hours.

**Run 22 records every population twice** --- the main set and all nine stride
classes from each half, one process each, which is what makes its class readings
a pair rather than a basis alone --- **and it is the first run here whose twenty
processes did NOT come out of one window.** Eighteen ran unbroken from 01:57:43
to 09:53:49; the machine was then wanted by its owner, so the sequence
was stopped by hand at the `scaled`/`runs` boundary rather than dying,
and the two `runs` processes ran at 16:41:21 to 18:26:27 on a box measured 0.6%
non-idle. Every one of the twenty exited 0 at the bench count its roster holds
--- 1320 twice, 605 twice, 220 four times and 165 twelve times ---
and no process reported a selection it did not ask for. The eighteen class
processes span **14m14s to 52m35s**, the two `runs` processes accounting
for the whole top of that range at 52m30s and 52m35s, some thirty-three minutes
clear of the next; at eleven shapes and 605 benches they were predicted
to be the longest and they are. **The control half ran first throughout**,
`ghead` before `g912` on the main set and on each class in turn, which
is the driver's order. **The alone-leg riders followed the sequence**, 108
single-bench processes over four invocations of 27, each half clean
and saturated, each invocation launching on a box between 0.0% and 0.3%
non-idle.

**The decomposition reproduces on both halves for a fourth run.** The riders
time each shape's `list` by itself, one bench per process on that half's own
binary, `SAT=` off and on: the saturated legs split the deflation into the state
the preamble puts on a clean process --- **+12.12%** on the basis
and **+12.37%** on the control --- and the rest the roster adds on top of it,
**+0.15%** and **+0.22%**. Run 21 read +11.84% and +12.02% for the state
and +0.12% and +0.50% for the rest, Run 20 +12.27% and +13.27% and +0.66%
and +0.29%. So the state term has now reproduced across four runs and three
roster changes inside a point and a half, while the roster's own contribution
has stayed under a point on every half of every run that measured it. **The tail
is the same shape on both halves and it is the shape Runs 19, 20 and 21 all
named**, `stretch-tall-Mx2` at 1.0858 and 1.0960 against Run 21's 1.0944
and 1.0956 --- a roster effect on one shape rather than a term belonging
to either compiler, now on four rosters. All 108 rider legs ran on a box
the script measured at 0.0% to 0.3% non-idle before each of the four
invocations.

**Everything in this file is replaced by the next run, which is what makes
it a file.** What a run replaces OUTSIDE it, in README.md and in the sources,
is [README's own Provenance](../README.md#provenance). None of it is portable:
a run on another machine is a different measurement rather than a repetition,
which Run 19 was in a position to be firm about, having repeated one binary
on one box and moved its floor by 1.7x. This run cannot repeat
that demonstration and does not try --- its roster moved again, so neither half
reproduces a predecessor byte for byte --- and it adds the weaker half
of the same point a third time, with the sign reversed once more: the floor went
2.32%, 1.51%, 2.92%, 2.12% over three roster changes on one recipe, one box
and one regime. A quantity that moves by a factor of two in each direction
over three roster changes is not a property any run inherits from the one before
it.
## Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries
that decision and this run's re-pass of its gates), the scratch vectors
are the unboxed ones the shipped code uses, as they have been since Run 7 ([the
scratch vector flavour](../README.md#the-scratch-vector-flavour) says what
that severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under. **A row's distance from Run 21's basis
column is NOT drift alone, and this run has a second reason as well as the usual
one.** Six timed arms landed and none left, so every address moved between
the two builds --- the build-time fill reading found no tracked address
surviving and none moved by a constant --- while the flag, the shapes,
the order, the allocation area, the box and the recipe are all the same ones;
Run 10 priced a reorder at 12 to 14% on the two arms whose loop the shim
rescues. **And seven rows are different CODE**, which layout does not cover
at all: `fillStage2` unboxed its source vector and steps its cursor twice,
reaching `lib-stage2` and `lib-stage2-concat` through the call;
`lib-stage2-concat`, `liblist-stage2`, `-add-in-leaf-u2` and `-u2-down` changed
in their own bodies; and `lib-stage1` and `liblist-stage1` fall back
to `-add-in-leaf-u2` on every regime-3 view. So read a distance from Run 21's
column as drift plus a layout term on the other rows, and as a code change
on those seven, and prefer the within-run comparisons for anything that has
to be decided. This pair's halves differ in the compiler, so they differ
in layout by construction too; there the counted-work instrument does separate
them, and the table's cross-half distances are read as codegen where the counts
moved and as placement or runtime where they did not.

**And it is the basis half's**, `run22-g912`, as every published table here
is from Run 11 on: the control half's column sits beside the basis one
in this file rather than as a second copy of these forty-odd rows.
That the published half is the 9.12 one is this pair's own decision --- it keeps
the lineage, being Run 21's basis recipe with only the source and the shim moved
--- and the HEAD half is the second column below. **Six rows here are first
readings**: `lib-stage2-disp`, `lib-stage2-lean`, `lib-stage2-short`,
`lib-stage2-u4`, `libunord-stage1` and `libunord-stage2`. A first reading has
no predecessor to be drift against, so nothing in this file compares one
to an earlier column, and the registrations they answer are [in this file's own
last section](#what-this-run-was-built-to-answer-and-what-it-answered).

**Comparing runs?** The table below is Run 22's own; what to hold a new run
against is [What the next run compares
against](#what-the-next-run-compares-against), the claims to test are [the ones
after it](#the-claims-the-next-run-should-test), the absolute anchor
is under [Provenance](#provenance) below and the population it was measured
over in [README's delta chain](../README.md#provenance), and this run's own
floor --- no A/A pair further than 2.12% from 1 on the basis half or 1.08%
on the control, and 0.37% and 0.51% read on the six pairs that carry across
runs, beside which the worst SINGLE cells of 19.44% and 14.40% are not floors
at all and are not to be quoted as any --- is [in the floor section][floor].
The sixteen-pair figure governs an arm against *itself*; what two different rows
of the table below must clear is the SIX-pair one, 0.37% here, that being
the pair that carries across runs --- and in a build whose loop heads the shim
has already placed, two rows are separated by their code and no longer by where
each landed --- which is what Run 10 spent two binaries to establish and every
run since has inherited.

**It is the main set's table**, and every column below is a statistic
of that population: each stride class has a table of its own, on the same rows
and in the same columns but its own basis, in [The stride classes, run
by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns:

- **time** is the geomean over **every** shape of the per-shape OLS *slope*,
  less that shape's forcing term, over `list`'s slope less the same term,
  with the per-shape log-ratios *winsorized* first --- capped at the row's own
  median plus or minus three MADs, the MAD scaled by 1.4826 so the cap
  is in standard deviations. Nothing is dropped by the estimator, so winsorizing
  costs no row its population and a cell far enough out to distort the mean has
  its influence bounded instead of its evidence deleted. **What DOES cost a row
  its population on this run is the correction, not the estimator**: two rows
  on the basis and eleven on the control carry cells the shared forcing pass
  is not smaller than, and such a cell cannot be corrected at all ---
  so on those rows the geomean is over 23 or 20 shapes of 24, they are named
  in the head, and two columns are comparable everywhere else. The `CI%`, `smp`
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
  on which that strategy does least well against the baseline. It is what claim
  1 is about, and it is raw rather than winsorized.
- **CI%** is the median across shapes of the slope's confidence half-width
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
| *bq-expand-nosum* | *--* | *--* | *0.56* | *78* | *2.35x* | *its base arm, forced with one element* |
| *canon-full-nosum* | *--* | *--* | *0.58* | *102* | *1.00x* | *the same, on a write pattern that varies by shape* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.70* | *90* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.46* | *91* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *101* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *101* | *0.00x* | *the same, at the other end* |
| libunord-stage2 | 0.000 | 0.053 | 0.02 | 101 | 0.00x | new mutating `Vector` method -- the branch's driver behind the unordered one-block test |
| libunord-stage1 | 0.000 | 0.049 | 0.01 | 101 | 0.00x | new mutating `Vector` method -- stage one behind the unordered one-block test |
| lib-stage2-short | 0.028 | 0.128 | 0.59 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, a short canonical run written by a body of its length |
| lib-stage2-lean | 0.031 | 0.128 | 0.59 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-concat | 0.031 | 0.128 | 0.61 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, runs sent back to a concat |
| lib-stage2 | 0.031 | 0.128 | 0.60 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver |
| lib-stage2-disp | 0.032 | 0.128 | 0.60 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, slice route above a run-length threshold |
| mut-odo-vecdims-add-in-leaf-u2 | 0.032 | 0.128 | 0.60 | 89 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| lib-stage2-u4 | 0.033 | 0.129 | 0.60 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, stepping run unrolled by four |
| lib-stage1 | 0.033 | 0.128 | 0.57 | 89 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.033 | 0.128 | 0.59 | 90 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf | 0.036 | 0.123 | 0.65 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf-down | 0.042 | 0.125 | 0.70 | 86 | 1.00x | new mutating `Vector` method |
| canon-vecdims | 0.049 | 0.126 | 0.70 | 94 | 1.00x | new mutating `Vector` method |
| liblist-stage2 | 0.049 | 0.160 | 0.92 | 90 | 2.00x | new mutating `Vector` method -- the branch at the list entry point |
| liblist-stage1 | 0.051 | 0.159 | 0.93 | 84 | 2.00x | new mutating `Vector` method -- stage one at the list entry point |
| canon-memcpy-r2 | 0.052 | 0.126 | 0.68 | 94 | 1.00x | new mutating `Vector` method |
| canon-full | 0.053 | 0.126 | 0.66 | 94 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.054 | 0.127 | 0.59 | 80 | 1.00x | new mutating `Vector` method |
| **mut-odo-vecdims** | **0.054** | 0.127 | 0.51 | 80 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa* | *0.054* | *0.127* | *0.51* | *80* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.126* | *0.40* | *80* | *1.00x* | *A/A control* |
| mid-copy | 0.055 | 0.126 | 0.69 | 80 | 1.00x | new mutating `Vector` method |
| bcast-set | 0.057 | 0.126 | 0.60 | 79 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.084 | 0.185 | 0.76 | 81 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.091 | 0.191 | 0.70 | 80 | 1.33x | mutable `Int` scratch |
| **bq-scan-rem-gm-mulback** | **0.098** | 0.158 | 0.56 | 74 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.098* | *0.157* | *0.61* | *74* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.156* | *0.32* | *74* | *1.33x* | *A/A control* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.100* | *0.181* | *0.46* | *79* | *1.51x* | *A/A control* |
| bq-odo-gm-mulback | 0.100 | 0.181 | 0.41 | 79 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-distant* | *0.100* | *0.181* | *0.53* | *79* | *1.51x* | *A/A control* |
| bq-expand-gm-mulback | 0.104 | 0.227 | 0.66 | 79 | 2.35x | nothing (pure) |
| *mut-odo-aa-distant* | *0.105* | *0.265* | *1.24* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-adjacent* | *0.106* | *0.268* | *0.91* | *70* | *1.00x* | *A/A control* |
| mut-odo | 0.107 | 0.273 | 1.38 | 70 | 1.00x | new mutating `Vector` method |
| build | 0.107 | 0.273 | 0.92 | 70 | 1.00x | new mutating `Vector` method |
| *build-aa-adjacent* | *0.108* | *0.287* | *1.44* | *70* | *1.00x* | *A/A control* |
| *build-aa-distant* | *0.109* | *0.290* | *1.14* | *70* | *1.00x* | *A/A control* |
| *bq-expand-aa-adjacent* | *0.115* | *0.232* | *0.46* | *74* | *2.35x* | *A/A control* |
| bq-expand | 0.115 | 0.233 | 0.53 | 74 | 2.35x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.115* | *0.232* | *0.38* | *74* | *2.35x* | *A/A control* |
| offtab-scan-rem | 0.132 | 0.225 | 0.88 | 72 | 2.00x | nothing (pure) |
| *list-aa-distant* | *1.000* | *1.017* | *0.38* | *35* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.45 | 35 | 23.50x | -- |
| *list-aa-adjacent* | *1.003* | *1.013* | *0.37* | *35* | *23.50x* | *A/A control* |
| *gen-unsafe-aa-adjacent* | *1.168* | *3.279* | *2.38* | *39* | *1.00x* | *A/A control* |
| gen-unsafe | 1.173 | 3.056 | 2.07 | 38 | 1.00x | -- |
| *gen-unsafe-aa-distant* | *1.181* | *3.107* | *2.00* | *38* | *1.00x* | *A/A control* |

`concat-runs` has no row, and neither do the other 36 arms the roster holds
and checks without timing --- 37 of its 92 in all: the reason is at each entry
and the count is [`--lint`'s](../README.md#the-reader-read-runpy). So a movement
below is a movement only on the 43 arms this run and Run 21 both give
a corrected time --- 49 names are shared, but six of them are `sum-only`
and `-nosum` controls with no corrected time to move --- and on seven
of those 43 it is a code change rather than a movement, as the section's opening
says. The six first readings are named in the paragraph above.

**Three things in the table are the run's findings rather than its numbers.**
**The head of the table has moved a long way from the family's plain arm,
and the count is no longer one a sentence can carry loosely.** `mut-odo-vecdims`
reads 0.054 with **eighteen** timed arms below it and one level --- where Run 21
had seven below and two level. The eighteen are the two `libunord` arms
at 0.000, six `lib-stage2*` arms and `lib-stage1` between 0.028 and 0.033, four
leaf arms between 0.032 and 0.042, `canon-vecdims` and the two `liblist` arms
between 0.049 and 0.051, and `canon-memcpy-r2` and `canon-full` at 0.052
and 0.053; `mut-odo-vecdims-add-in` is the one level with it. Every one of them
needs exactly what the fix needs --- a mutating `Vector` method and nothing more
--- so what the table shows is still not a new tier but a much better populated
one, with the shipped library route and six candidates now inside it.
**The ceiling reproduced on the arm the class property names**:
`mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm needing
nothing at all, reads **0.5449 at 23 wins of 24** and sign p 3e-06 on the basis,
against Run 21's 0.5424 and Run 20's 0.5479, and **0.5184** on HEAD against Run
21's 0.5164. **And the `alloc` column gains a tier below the fills, which no run
before this had.** Four of the six new arms read 1.00x, the mutable fills' own
level, and the two `libunord` arms read **0.00x** --- an unordered consumer
whose one-block test fires returns a single `VS.slice` and allocates nothing
at all, so the ladder claim 7 carries now has a floor under its floor.

**The leaf block's internal ordering reverses Run 21's, and it bears on what
ships.** `genericFillStrided` in `Data/Array/Internal.hs` is a bang-for-bang
port of `mut-odo-vecdims-add-in-leaf-u2`, and that arm's own body changed
this run. Against `mut-odo-vecdims` it is emphatic and it repeats across
the compilers: `-u2` / `mut-odo-vecdims` reads **0.6353 at 22 of 24, sign p
3.6e-05** on the basis and **0.6319 at 22 of 24** on HEAD, against Run 21's
0.7098 and 0.7043 --- so the shipped code is now some 37% ahead of the code
it was refined from, where it was 30% ahead a run ago. **And it now heads
its own block, which it did not.** `mut-odo-vecdims-add-in-leaf-down` reads
**1.2598 of it at 1 of 24, p 3e-06** on the basis and **1.0346 at 8 of 24, p
0.15** on HEAD, where Run 21 read 0.9440 and 0.9327 the other way ---
so the variant that was 5.6% and 6.7% ahead on two halves a run ago is 26%
and 3.5% behind on them now, and the re-stepped cursor is what moved between
the two readings. **The third member does not carry, again, and this run
it loses on both**: `-add-in-leaf` reads 1.0677 of `-u2` on the basis
and **1.2544** on HEAD, at 4 of 24 and 1 of 24, against Run 21's 0.9513
and 1.1236 --- so where it won on 9.12 and lost on HEAD, it now loses on both.
**What the dispatch around the fill costs is unchanged**: `lib-stage1`,
that same fill reached through the library's own regime test, reads **1.0374**
of the bare arm on the basis and 1.0414 on HEAD, against Run 21's 1.0333
and 1.0402, so a user's `toVectorT` still pays about three to four percent
over the kernel on the main set.

**The two standing placement controls part this run, and both moved.**
`mut-odo-vecdims-add-in` against the arm it varies reads **0.9944 at 15 of 24,
sign p 0.31** on the basis and **0.9886 at 16 of 24, p 0.15** on HEAD, where Run
21 read 0.9949 and 0.9957. Both sit inside their halves' sixteen-pair floors
of 2.12% and 1.08%; against the six-pair figures the basis margin of 0.56%
clears its 0.37% and the control's 1.14% clears its 0.51%, so where Run 21 had
one clearing and one not, this run has both clearing at sign tests
that are still coin flips --- a separation the margins assert and the signs
decline to. `build` against `mut-odo` is the one that inverted, on **both**
halves: 1.0125 on the basis at 10 of 24 by sign and p 0.54, against **0.9803**
on HEAD at 17 of 24 and p 0.064, where Run 21 read 0.9870 and 1.0764. Both pairs
are read for placement and every address moved between these runs; what this run
adds is that the tracked loops of `build` and `mut-odo` were named off a `-g3`
twin again and both sit at offset 0 on both halves, at addresses identical
in twin and timed binary, so the cache-line reading is not what separates them
--- and the counted work puts both at 1.0000, so neither is code.


## What the next run compares against

**Run 23's regime, roster and basis are settled, and so, since 2026-09-01,
is its PAIR: `run23-g912` against `run23-spot`, the basis recipe built twice
from one source, the `spot` half with `LOOP_DEADSPOT=1` in front of the shim
and nothing else varied** --- the layout pair that [task 6][open] priced
on the main set, now over the classes and under a run's own controls,
and the pair a basis move would rest on; the repetition and the threshold pair
argued for below stay argued for. The regime is `-fspec-constr`, as every run
since Run 8, and it is the regime the claims decide in; the shipped file does
not set the flag ([the ceiling](../README.md#the-mutable-ceiling-taken)).
The roster is Run 22's --- 55 timed arms over 24 main-set shapes and 37 class
views over nine classes, 1320 benches and 2035 --- unless the tasks below add
to it, and the basis is `run22-g912`'s recipe, ghc-9.12.4
with `-fobject-determinism`, the per-sample instrument and the saturating
preamble, run under `WILDLOG=1 SATURATE=1`, which is now the same recipe six
runs running. The allocation area is fixed at `-A32m` and no pair will vary
it again. **What Run 22's results argue for, stated so the decision has
something to weigh and not as a choice this file makes.** A *repetition* --- one
recipe built twice, or one binary run twice --- is what this file has wanted
for four runs and has now been refused four times, each roster change putting
a layout term into every cross-run figure; and it is the pair that would answer
[task 3][open], which wants one binary over the roster several times
and no second recipe at all. **A purpose-built pair has the strongest candidate
it has had**: `dispRun` is now demonstrably mis-cut, the crossover having moved
from between `runs-9` and `runs-96` to between `runs-1024` and `runs-65536`
on both compilers, so a pair varying nothing but that threshold would settle
in one evening what registration 3 could only kill. A *fifth compiler reading*
buys least of all: the surviving manifest claim has now held on 9.12, 9.14
and HEAD five times, and this run's cross-half geomean is carried by two
degenerate arms. **What is NOT a candidate** is a pair varying the allocation
area, closed 2026-08-21, or one varying the roster between its halves, refused
because it would break `preflight`'s `check` comparison and both drivers' bench
counts.

**The ruling this section carried about compiler pairs is now spent twice over,
and this run is the one that spends it.** Run 19 advised against another
compiler pair, HEAD and 9.14 both having been read; Run 20 overrode that because
it rostered the rework's arms, and Runs 21 and 22 spent the reading again. Run
22's answer is the plainest of the three: the manifest's surviving claim holds
on both halves, every allocation tier holds on both, the counted work reproduces
on both to four figures, and **four of the five registrations were decided
the same way on both compilers** --- the exceptions being registration 5's
`bcast` cell and registration 3's threshold, and the second of those turns out
not to be a compiler difference at all, both halves having moved their crossover
to the same place. **So the compiler variable has stopped paying**, which
is what Run 19 said three runs ago and what three runs of evidence now support.
What has taken its place is not a variable but two things this run made
concrete: a repetition, which no pair since Run 19 has been able to give,
and a threshold whose right value is now a measurable question rather
than a guess.

**What Run 22 leaves the next run to read against, and the first item is
not a figure.** **The box did not change**, its gate machine check reading
-0.87% against the fingerprint Run 21 kept and the run's own main-set process
reading +0.08% against that same fingerprint, over 24 of 24 shapes both times,
worst -1.66% and +1.85% and none past 5%; so absolutes cross from Run 21 to Run
22 freely and the boundary that matters is still the BIOS change before Run 18,
which no absolute crosses. **The floor is 2.12% on the basis and 1.08%
on the control**, with the restricted six at 0.37% and 0.51%. A Run 23 margin
is judged on both and they answer different questions: the six-pair figure
is what two rows of one table must clear, the sixteen-pair one is how far an arm
differs from its own duplicate. **And it is not inherited**: Run 21 read 2.92%
and 2.16% on these same two recipes and this run reads 2.12% and 1.08%, one
roster change on, having risen from 1.51% over the previous such step ---
so a floor moves by a factor of two in either direction for reasons no run has
isolated, and a Run 23 margin is judged against Run 23's own, never against
these. **The two columns below MAY NOT be differenced, which reverses Run 21**:
`list` moved **0.81%** between the halves against the 0.7% bar, where Run 21
read 0.64% and passed marginally and Runs 20 and 19 read 0.71% and 0.78%
and were refused. So read them as an ordering; and note that five of the nine
classes are past the bar too --- `bcastmid` 1.0106, `reshape1` 0.9900, `window`
1.0082, `scaled` 0.9911 and `runs` 1.0114 --- while `rev`, which Run 21
disqualified, is inside it here. What the columns price is a compiler,
and the counted-work column says which movements that reaches:
`bq-odo-gm-mulback` and `bq-scan-rem-gm-mulback` six to seven percent apart
ON their instruction counts, `mut-odo-vecdims-add-in-leaf` ten points
of its fifteen, and the placement-exposed arms `build`, `mut-odo`
and `gen-unsafe` apart at count ratios of 1.0000. So a movement on one
of those three is layout or runtime until the counts say otherwise.

**Registered with the pair.** Run 22's five registrations, their kill conditions
and their verdicts are [in this file's last
section](#what-this-run-was-built-to-answer-and-what-it-answered),
and the commands that produced them were the pair note's, transcribed
into Provenance below before that note goes with the pair. **What Run 23
inherits is five riders that are now routine and no instrument that is new.**
The alone legs, the counted-work sweeps over every population, the saturating
preamble, the per-sample load fields and `--counts` all ran to form and want
no re-deciding; the counted work was again taken outside the quiet window,
on a working desktop, which is what its own scope note licenses. **What
it inherits as a debt** is one thing and it is procedural rather than measured:
this run's sequence ran in two windows, the machine having been wanted back part
way, so a session comparing process elapsed times against this run's wall-clock
log must read the two `runs` processes as a separate window. No population
was rerun for an intrusion, no gate failed, and post-run step 3 was owed
nothing. **What it inherits as a warning** is that a registration written off
counted work can be right in sign and wrong by a factor: `lib-stage2-short`
was predicted at 0.50 and 0.59 where it reads 0.81 and 0.97,
and `lib-stage2-lean` was predicted 21 points ahead on `stretch-inner1` where
it reads 6.2% behind. Price a candidate in time before predicting a magnitude
for it.

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

**Where a run changes basis, the new basis is checked against the half
at its OWN allocation area and against no other**, which is the rule the Run 15
to Run 16 change settled and the one place *against the previous run* can still
be ambiguous. **The six figures that follow are Run 16's, are no longer
checkable, and are stamped so that no later run reads them as its own**,
`run15-*` and `run16-*` having been deleted; they are kept as the evidence
the ruling was taken on. Against `run15-a32m` Run 16's three anchors read
**-0.66%, -1.01% and -0.06%**, every one well inside the 2.32% floor
it measured; against `run15-lookrts` the same three would have read **+8.81%,
-9.57% and +7.74%**, which is the allocation area and not the shapes, and would
have put all three outside that floor for a reason that is not theirs. Distance
from a half at another area is that area plus whatever else moved; only distance
from the half at this run's own area is drift.

**A pair's two halves are never folded into one.** Merging them puts back,
in the record built to outlive every artifact, exactly the term the pairing
exists to separate --- and what a given pair's two columns price is that run's
own file's to say, not this section's. `--check-doc` catches one half of it:
a run named aligned must also be named unaligned. Pruning an aligned column,
merging two, and naming a second half accurately are the reading's to catch ---
the check cannot demand an unaligned half of every pair without failing the last
two runs, which have none, nor an aligned column of every run without failing
Runs 6 through 9, which had none either.

**The next run compares against Run 22 and against nothing before it.** Each
run's figures and the names of its halves are in its own file, `runs/run<N>.md`,
back-filled to Run 7 on 2026-08-29; a comparison reaching further back
is a chain of one-step comparisons, each recorded by the run that made it,
and walking that chain here is what this section stopped doing. So an older run
is read by opening its file, not by reading a column across. This run's own two
halves, on the rows nearest the decisions:

| strategy | Run 22 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 22 (SpecConstr, max-skip +lookrts, -A32m, GHC HEAD) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.054** | 0.055 |
| `mut-flat-gm` | **0.084** | 0.083 |
| `bq-mut-runs-gm-mulback` | **0.091** | 0.095 |
| `bq-odo-gm-mulback` | **0.100** | 0.109 |
| `bq-scan-rem-gm-mulback` | **0.098** | 0.106 |
| `bq-expand` | **0.115** | 0.116 |
| `build` | **0.107** | 0.101 |

**A published geomean is over the same 24 shapes, and two halves of one
SpecConstr run usually share a denominator too**, `list` moving under 0.7%
between them --- so such a pair may be subtracted and not merely ordered, which
is what an -O1 reading cannot do at an 8% baseline shift. **THE TABLE ABOVE
IS NOT SUCH A PAIR**, `list` having moved 0.81% on this run's main set, which
is why the paragraph before it refuses the subtraction; *usually* is doing
the work in this sentence and this run is the exception it allows for. **A pair
that varies the allocation area is the exception, and its two halves may never
be subtracted from each other.** `list` moved **9.20%** between Run 14's halves,
**5.13%** between Run 15's and **16.51%** between Run 16's. **Run 16's
is the largest of the three and was registered to be the smallest**,
on the reasoning that its two halves both sit at enlarged areas where
the earlier two each crossed the default --- a prediction refuted by its own
run, and the refutation is the finding: what moves the baseline is
not the distance from the default but the in-process deflation, which at roster
scale is worse at 64 MB than at 32 MB by more than the whole default-to-32 MB
step was worth. So the exception widens rather than narrowing, and it covers
every pair that varies the area at all. Every cell of such a pair's second
column is scaled by a denominator the pairing moved: read it for the pairing's
direction, take no strategy quality off it, and read the arm-by-arm comparison
at the head of this file instead, which divides absolutes rather than ratios.

**Each stride class has its own table below.** Run 8 re-ran every class
with the populations pinned, and every run since has again, so each class's
paragraph carries what the last change moved and the table above it is what Run
13 reads against. **The two sides of a class comparison across the Run 11/Run 12
boundary are not the same build**, and this is the one place that bites: Run
11's class tables are its *aligned* half's, Run 12's are its *max-skip* basis
half's, and the main set prices that difference at nothing below 0.99 and up
to 1.06. So read a class figure that moved a point or two across that boundary
as the shim rather than as the class, and take the two Run 12 columns above
as what a same-build comparison looks like. From Run 13 on, both sides
are max-skip again.

**Two tables in this file are NOT installed and are edited by hand:
the two-column one above and the cross-class summary below.** Every other table
a run publishes comes from `install-tables.sh` and is replaced whole. The one
above is replaced whole too, being this run's own halves and no earlier run's;
the summary gains a row per run instead. A hand-edited table is edited
with the whole line named, never with a prefix anchor. On Run 17 an insertion
anchored on ``| `arm` | `` matched an earlier table and put two cells
into the element-type probe's header and a loop-offsets row; `--check-doc`'s
width pass caught it in the same call, which is the only reason it cost minutes.
Name the whole row, assert it occurs exactly once, and read the width check's
verdict afterwards.

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
| `cnn-slice-c32` | 3 | 288 | 5.98 us | 0.084 | 0.143 | 0.158 | 0.164 | 0.173 | 0.148 | 0.169 | 0.116 | 0.085 | 0.086 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.28 us | 0.094 | 0.184 | 0.143 | 0.200 | 0.199 | 0.184 | 0.160 | 0.104 | 0.103 | 0.096 |
| `stretch-rank12` | 2 | 4096 | 111 us | 0.092 | 0.185 | 0.131 | 0.273 | 0.273 | 0.191 | 0.170 | 0.073 | 0.104 | 0.097 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 115 us | 0.067 | 0.124 | 0.098 | 0.177 | 0.166 | 0.135 | 0.124 | 0.057 | 0.071 | 0.070 |
| `conv1d-24` | 3 | 5184 | 99.3 us | 0.058 | 0.072 | 0.101 | 0.134 | 0.131 | 0.078 | 0.140 | 0.058 | 0.058 | 0.061 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 368 us | 0.048 | 0.093 | 0.093 | 0.113 | 0.107 | 0.100 | 0.120 | 0.043 | 0.049 | 0.051 |
| `gather48-src-50` | 3 | 22500 | 437 us | 0.053 | 0.066 | 0.098 | 0.133 | 0.130 | 0.075 | 0.131 | 0.052 | 0.053 | 0.056 |
| `stretch-rank10` | 3 | 59049 | 1.28 ms | 0.065 | 0.112 | 0.103 | 0.157 | 0.159 | 0.119 | 0.138 | 0.055 | 0.068 | 0.069 |
| `stretch-coprime-r7` | 13 | 60060 | 1.02 ms | 0.034 | 0.082 | 0.093 | 0.061 | 0.060 | 0.095 | 0.123 | 0.033 | 0.034 | 0.037 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.07 ms | 0.057 | 0.090 | 0.098 | 0.148 | 0.148 | 0.097 | 0.129 | 0.056 | 0.059 | 0.061 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.46 ms | 0.058 | 0.090 | 0.099 | 0.150 | 0.138 | 0.100 | 0.130 | 0.057 | 0.059 | 0.061 |
| `stretch-primes` | 89 | 250357 | 4.01 ms | 0.029 | 0.075 | 0.092 | 0.030 | 0.030 | 0.086 | 0.130 | 0.029 | 0.029 | 0.030 |
| `stretch-inner1` | 1 | 500000 | 12.8 ms | 0.090 | 0.035 | 0.074 | 0.240 | 0.226 | 0.031 | 0.074 | 0.000 | 0.090 | 0.098 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16 ms | 0.044 | 0.077 | 0.094 | 0.096 | 0.098 | 0.087 | 0.126 | 0.044 | 0.045 | 0.047 |
| `vgg-14-c512-k3` | 3 | 903168 | 18.8 ms | 0.057 | 0.092 | 0.098 | 0.148 | 0.147 | 0.097 | 0.131 | 0.058 | 0.059 | 0.061 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.4 ms | 0.035 | 0.071 | 0.090 | 0.053 | 0.057 | 0.083 | 0.130 | 0.034 | 0.035 | 0.038 |
| `stretch-inner256` | 256 | 1750784 | 32.9 ms | 0.032 | 0.068 | 0.086 | 0.032 | 0.033 | 0.074 | 0.117 | 0.032 | 0.032 | 0.031 |
| `stretch-pow2stride` | 64 | 1769472 | 28.1 ms | 0.127 | 0.124 | 0.148 | 0.127 | 0.127 | 0.135 | 0.225 | 0.126 | 0.126 | 0.126 |
| `stretch-r5-8x432` | 8 | 1769472 | 34 ms | 0.032 | 0.060 | 0.081 | 0.052 | 0.056 | 0.067 | 0.114 | 0.032 | 0.032 | 0.035 |
| `stretch-square-1341` | 1341 | 1798281 | 29.3 ms | 0.087 | 0.134 | 0.156 | 0.088 | 0.088 | 0.142 | 0.204 | 0.082 | 0.087 | 0.087 |
| `stretch-bigstride` | 3 | 1800000 | 49.1 ms | 0.035 | 0.045 | 0.067 | 0.085 | 0.080 | 0.052 | 0.094 | 0.035 | 0.035 | 0.037 |
| `stretch-tab7MB` | 2 | 1800000 | 38.2 ms | 0.063 | 0.063 | 0.100 | 0.148 | 0.140 | 0.068 | 0.144 | 0.062 | 0.062 | 0.067 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39 ms | 0.023 | 0.052 | 0.064 | 0.023 | 0.023 | 0.058 | 0.097 | 0.022 | 0.023 | 0.023 |
| `stretch-wide-2xM` | 2 | 1800000 | 37.9 ms | 0.062 | 0.061 | 0.098 | 0.159 | 0.141 | 0.070 | 0.143 | 0.061 | 0.061 | 0.066 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 870 us | 0.032 | 0.066 | 0.091 | 0.058 | 0.057 | 0.081 | 0.117 | 0.032 | 0.032 | 0.030 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 27.1 ms | 0.022 | 0.071 | 0.089 | 0.022 | 0.022 | 0.089 | 0.124 | 0.022 | 0.021 | 0.019 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 37.4 ms | 0.062 | 0.061 | 0.099 | 0.157 | 0.162 | 0.070 | 0.142 | 0.062 | 0.062 | 0.062 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.38 ms | 0.058 | 0.089 | 0.101 | 0.151 | 0.152 | 0.104 | 0.132 | 0.059 | 0.012 | 0.062 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.91 ms | 0.021 | 0.069 | 0.088 | 0.023 | 0.023 | 0.085 | 0.122 | 0.022 | 0.013 | 0.023 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.4 ms | 0.036 | 0.045 | 0.069 | 0.083 | 0.077 | 0.054 | 0.093 | 0.036 | 0.033 | 0.038 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 41.9 ms | 0.023 | 0.053 | 0.066 | 0.023 | 0.023 | 0.060 | 0.089 | 0.023 | 0.018 | 0.022 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.88 ms | 0.109 | 0.132 | 0.093 | 0.344 | 0.321 | 0.129 | 0.093 | 0.000 | 0.120 | 0.107 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.71 ms | 0.092 | 0.035 | 0.073 | 0.267 | 0.267 | 0.032 | 0.073 | 0.000 | 0.092 | 0.092 |
| `reshape1-strided-r3` | `reshape1` | 1 | 180000 | 4.72 ms | 0.094 | 0.033 | 0.075 | 0.243 | 0.252 | 0.034 | 0.075 | 0.016 | 0.094 | 0.095 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 12.8 ms | 0.091 | 0.032 | 0.074 | 0.238 | 0.223 | 0.032 | 0.073 | 0.000 | 0.091 | 0.092 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 114 us | 0.067 | 0.130 | 0.097 | 0.168 | 0.177 | 0.134 | 0.124 | 0.056 | 0.072 | 0.070 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 433 us | 0.052 | 0.066 | 0.098 | 0.133 | 0.118 | 0.076 | 0.129 | 0.052 | 0.053 | 0.056 |
| `rev-primes` | `rev` | 89 | 250357 | 4.05 ms | 0.028 | 0.071 | 0.091 | 0.030 | 0.030 | 0.085 | 0.128 | 0.029 | 0.028 | 0.029 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 433 us | 0.053 | 0.068 | 0.101 | 0.130 | 0.116 | 0.077 | 0.132 | 0.054 | 0.053 | 0.057 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.45 ms | 0.058 | 0.089 | 0.099 | 0.149 | 0.149 | 0.100 | 0.130 | 0.057 | 0.059 | 0.062 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.04 ms | 0.030 | 0.079 | 0.101 | 0.031 | 0.031 | 0.092 | 0.130 | 0.030 | 0.030 | 0.031 |
| `runs-65536` | `runs` | 65536 | 1769472 | 25.9 ms | 0.027 | 0.075 | 0.093 | 0.027 | 0.028 | 0.089 | 0.135 | 0.028 | 0.028 | 0.028 |
| `runs-1024` | `runs` | 1024 | 1799168 | 26.2 ms | 0.028 | 0.075 | 0.093 | 0.028 | 0.029 | 0.088 | 0.136 | 0.029 | 0.028 | 0.030 |
| `runs-512` | `runs` | 512 | 1799680 | 26.5 ms | 0.028 | 0.074 | 0.092 | 0.028 | 0.028 | 0.087 | 0.135 | 0.029 | 0.028 | 0.030 |
| `runs-256` | `runs` | 256 | 1799936 | 26.7 ms | 0.028 | 0.074 | 0.092 | 0.029 | 0.029 | 0.088 | 0.135 | 0.029 | 0.028 | 0.030 |
| `runs-2` | `runs` | 2 | 1800000 | 38 ms | 0.063 | 0.062 | 0.100 | 0.161 | 0.163 | 0.068 | 0.148 | 0.062 | 0.062 | 0.067 |
| `runs-3` | `runs` | 3 | 1800000 | 34 ms | 0.052 | 0.066 | 0.099 | 0.120 | 0.122 | 0.075 | 0.141 | 0.052 | 0.051 | 0.056 |
| `runs-4` | `runs` | 4 | 1800000 | 32.3 ms | 0.046 | 0.068 | 0.098 | 0.088 | 0.097 | 0.077 | 0.135 | 0.045 | 0.045 | 0.050 |
| `runs-5` | `runs` | 5 | 1800000 | 31.3 ms | 0.043 | 0.069 | 0.096 | 0.084 | 0.086 | 0.078 | 0.135 | 0.043 | 0.043 | 0.046 |
| `runs-9` | `runs` | 9 | 1800000 | 29.6 ms | 0.034 | 0.070 | 0.093 | 0.057 | 0.056 | 0.081 | 0.134 | 0.034 | 0.034 | 0.037 |
| `runs-96` | `runs` | 96 | 1800000 | 26.6 ms | 0.029 | 0.075 | 0.093 | 0.030 | 0.030 | 0.088 | 0.141 | 0.029 | 0.029 | 0.030 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 27 ms | 0.030 | 0.075 | 0.094 | 0.034 | 0.034 | 0.088 | 0.136 | 0.028 | 0.030 | 0.031 |
| `scaled-r5` | `scaled` | 13 | 15015 | 247 us | 0.033 | 0.074 | 0.096 | 0.052 | 0.048 | 0.083 | 0.130 | 0.032 | 0.034 | 0.037 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 962 us | 0.028 | 0.071 | 0.091 | 0.033 | 0.033 | 0.082 | 0.124 | 0.028 | 0.027 | 0.028 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.73 ms | 0.033 | 0.073 | 0.092 | 0.035 | 0.033 | 0.082 | 0.136 | 0.035 | 0.035 | 0.035 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.02 ms | 0.037 | 0.084 | 0.096 | 0.063 | 0.065 | 0.092 | 0.128 | 0.038 | 0.037 | 0.039 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.58 ms | 0.057 | 0.088 | 0.098 | 0.148 | 0.147 | 0.093 | 0.130 | 0.058 | 0.059 | 0.061 |
| `slice-primes` | `slice` | 89 | 250357 | 3.98 ms | 0.030 | 0.081 | 0.103 | 0.032 | 0.032 | 0.094 | 0.133 | 0.030 | 0.030 | 0.031 |
| `window-28x28-k5` | `window` | 5 | 14400 | 263 us | 0.044 | 0.077 | 0.095 | 0.107 | 0.091 | 0.086 | 0.120 | 0.045 | 0.045 | 0.047 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 878 us | 0.095 | 0.048 | 0.073 | 0.290 | 0.265 | 0.047 | 0.073 | 0.020 | 0.096 | 0.102 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.25 ms | 0.057 | 0.087 | 0.097 | 0.149 | 0.149 | 0.099 | 0.127 | 0.058 | 0.057 | 0.060 |

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

**Run 22's verdicts first**, since a run reports breaks rather than re-deriving
the table. **The one manifest claim left held on both compilers**, all four
of claim 1's links on the 9.12 basis and all four on GHC HEAD --- no BROKE
on either half, a fifth clean sweep running. That is the second reading
of the set the parking of 2026-08-28 left: claims 2 and 6 retired with `offtab`
and `gen-quotrem`, so what was thirteen registered orderings through Run 19
and eight at Run 20 is four links of one claim here, the foot rung having
retired on 2026-08-29 with Run 21's reading as its last. Claims 3, 4, 5 and 9
went at Run 19's write-up; none of their numbers is reused, so a verdict
recorded against *claim 4* in an earlier run's file still means what it said.
**What this run adds to the sweep is a roster the manifest had not been read
on**, for the third run running: six timed arms landed between Run 21 and Run
22, so every ordering was re-read on a build whose every address had moved,
and none of them noticed. Every arm claim 1 names is still timed, and `--pair`
recovers any retired ordering in one call whenever it is wanted.

**The six retired claims are not re-read here.** Claims 3, 4, 5 and 9 left
the manifest at Run 19's write-up, on a sweep in which all thirteen held on both
of that run's halves; claims 2 and 6 left on 2026-08-28 with the parking
of the arms their surviving links turned on, and their last readings are Run
20's, in that run's own file. The numbered items below say what each was
in a clause. Run 22 does not re-derive any of them and quotes none as its own:
of the arms they named, those still rostered and timed put any
of those orderings one `--pair` call away, and the parked ones would want a run
that re-times them --- which is the whole of what retiring them gave up.

**Claim 1 held on all four links, on both halves, and the family below its top
rung has grown enormously.** The four links are what the `needs` column draws:
what a mutating `Vector` method buys (**0.6448** on the basis), what one more
mutable write pattern buys (0.9210), and what a mutable `Int` scratch buys
against the two fastest arms needing nothing (0.9158 and 0.9175). On HEAD
the same four hold at **0.6631, 0.8809, 0.8731 and 0.8875** --- every link wider
there than on the basis, which is the compiler costing the pure tier more
than it costs the fills. Every figure is within a few thousandths of Run 21's
on the basis links they share, across a roster change that moved every address.

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6448, 21 of 24, sign p
0.00028; `mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9210, 23 of 24, sign p
3e-06; `bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9158, 20 of 24, sign p
0.0015; `bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9175, 17 of 24,
sign p 0.064. 4 of 4 registered orderings held.

**The first link is the one this run's new arms bear on, and the claim now sees
it a great deal less well than it did.** Claim 1 reads `mut-odo-vecdims` against
`mut-flat-gm`, and **eighteen** arms now read below `mut-odo-vecdims` with one
more level with it, at 0.000 to 0.053 against its 0.054 --- where Run 21 had
seven below and two level, and Run 20 six and one. So the ladder's top rung
understates what a mutating method buys by a factor rather than by a third,
while remaining true as stated. **Two of the eighteen are not fills at all**,
`libunord-stage1` and `libunord-stage2` at 0.000, which return a single
`VS.slice` where their one-block test fires and so measure dispatch; the other
sixteen do the work. **And the shipped library route sits well inside
the group**, `lib-stage1` at 0.033, as does every one of the six candidates.
Whether the claim should be re-aimed at the family's leader is a question
for the next run and is [under the recommended
tasks](../README.md#recommended-tasks-after-run-22); it is not re-aimed here,
a claim being re-aimed on a decision and not on one reading.

**Claim 7 held on every level it carried and gained one below them all.** Every
level is Run 15's through Run 21's to the digit --- the mutable fills at 1.00x,
the scan family 1.33x, `bq-odo-gm-mulback` 1.51x, `offtab-scan-rem` 2.00x,
`bq-expand` 2.35x, `list` 23.50x --- and the class blocks read the tiers
unbroken in all nine classes, `bq-expand` running 1.14x on `scaled` to 4.91x
on `reshape1` where that class's own `m` shows through. **What is new is a floor
under the floor**: `libunord-stage1` and `libunord-stage2` read **0.00x**,
an unordered consumer whose one-block test fires returning a view of its source
and allocating nothing at all, which is the first level below the result vector
any run here has recorded. The other four new arms read 1.00x, the fills' own
tier, so the candidates buy their time without buying allocation.
**The cross-half agreement is where the pair parts, as on the three runs
before**: **1123 of the 1272** main-set cells that allocate in earnest agree
to 1e-4, where Run 21 read 1026 of 1128 and Run 20 1143 of 1224, and the worst
disagreement is **6.24e-03 on `cnn-slice-c32/mut-flat-gm-nosum`** --- the same
shape Runs 19, 20 and 21 all named, on a different arm this run and the same one
on Runs 19 and 20. Allocation is deterministic per call, so a cell that moves
is a code change and never a slot: the levels surviving while a hundred-odd
cells move is HEAD reallocating within a tier rather than changing what any
strategy fundamentally costs.

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

**The list did NOT need re-aiming this run, and that is the first run in three
of which it is true.** Six timed arms landed and none left, so no claim lost
an arm and nothing retired on a parking; claim 1's four links all name arms
that are still timed. **What the roster does raise is the same question
the manifest cannot see, and it has grown by a factor**: eighteen arms now read
below `mut-odo-vecdims` where seven did a run ago, six of them the candidates
this run added and one of them the shipped library route. That is left
to the next run rather than re-aimed here, and it is the sharpest of [the
recommended tasks](../README.md#recommended-tasks-after-run-22).

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
is the `mut-odo-vecdims` family. The arms all stay rostered and timed, so any
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

**And for each stride class, the same three properties, now carrying Run 22's
verdicts** over nine classes, the details beside each class's table:

1. **`mut-odo-vecdims`'s `worst` stays under 1.** Held in every one of the ten
   populations, in every regime, roster and layout the README has run ---
   so it was never slower than the `list` it replaced, on any shape of any class
   the library can produce. This is the property the classes exist to test,
   no geomean can state it, and a break would be the one result here to bear
   on `Data/Array/Internal.hs` directly. Re-aimed 2026-08-22 with the decision
   to ship the `mut-odo-vecdims` family, and read for its plain arm since:
   **on Run 22 its worst is 0.127 on the main set and 0.109 in a class
   (`reshape1`), both read on the basis half, with the control half at 0.126
   and 0.108** --- so the property holds for the arm decided, on both compilers,
   and neither end is within a tenth of 1: the main-set end is a factor of 7.87
   inside it and the class end 9.17. Both halves are quoted because one
   is not enough: Run 18's entry here read a floor-level figure from whichever
   half happened to be lower, which is the defect this phrasing exists
   to prevent. **What breaks it is again not a fill the library would ship.**
   `gen-unsafe` carries a `worst` above 1 in all ten populations, from 1.089
   on `bcast` to 3.056 on the main set, and at least one `list` twin does
   in each --- but they are a baseline variant and the baseline's own controls.
   **The library-shaped arms break it on `runs` alone and all at `runs-2`**,
   and this run they are SIX where Run 21 had four, the two unordered arms
   having joined them: `liblist-stage1` at **1.3485**, `libunord-stage1`
   at 1.3467, `lib-stage2-concat` at 1.3311, `lib-stage1` --- the shipped route
   --- at **1.3149**, `liblist-stage2` at 1.1399 and `libunord-stage2`
   at 1.1368. So on 900000 runs of two elements SIX of the eleven library-shaped
   arms are slower than the `list` baseline they replace --- every route
   that takes a slice per run at that length, which is `lib-stage1`,
   `lib-stage2-concat` and the two `liblist` arms, and both unordered entry
   points --- while `lib-stage2`, the three fill candidates and the dispatch
   built on it fill every run whatever its length and are the five that are not.
   **The property is stated of `mut-odo-vecdims` and holds of it; it does
   NOT hold of what the library actually calls.** `lib-stage1` is the shipped
   route and is among the six, at 1.3149 --- so a reader taking property 1
   as clearance for the code that ships is reading it wider than it is stated,
   and the class that catches the difference is `runs`.

2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-expand` behind it. **The first clause breaks in all nine CLASS
   populations --- the main set is the tenth and is counted separately
   throughout this section --- and this run it breaks OUTRIGHT in all nine,
   to an arm outside the vecdims family every time.** That is a change from Run
   21, which broke to a sibling in seven of the nine and outright in two,
   and from Run 20, which broke to the rework's arms in all eight. The nine
   heads divide three ways. **Three are degenerate**: `libunord-stage2` leads
   `rev`, `revsome` and `reshape1` at 0.0174, 0.0076 and 0.0008
   of `mut-odo-vecdims`, which is its one-block test firing on every view
   of those classes and collapsing them to a single slice, so it prices dispatch
   and not filling. **Three are the unrolled fill**: `lib-stage2-u4` leads
   `bcast`, `bcastmid` and `scaled` at 0.5968, 0.5258 and 0.8815, margins
   of 40.3%, 47.4% and 11.9% against those populations' floors, every one
   outside. **Three are the short-body fill**: `lib-stage2-short` leads `slice`,
   `window` and `runs` at 0.7522, 0.3291 and 0.7647, margins of 24.8%, 67.1%
   and 23.5%, likewise all outside. **So six of the nine classes are now led
   by a candidate this run added**, and the fact sits oddly beside
   those candidates' own registrations, which killed `-u4` for not clearing
   the `runs` floor at long lengths and refuted `-short`'s predicted magnitudes:
   a registration scoped to one population and a class set say different things,
   and both are readings of the same arms. The third clause reads the last
   candidate `bq-expand` behind `mut-odo-vecdims` and holds in all nine.

3. **The allocation tiers survive, and every level is Run 15's through Run 21's
   to the digit**: the mutable fills at the result vector, `bq-expand` between
   1.14x and 4.91x it, `list` an order of magnitude above. Where a level moves
   it is the class's own `m` showing through, exactly as this property warned
   --- `bq-expand` at 1.14x on `scaled` (`m` of 1 and 2,000) and 4.91x
   on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine
   and `list` running 19.43x to 32.29x across them. **Four of the six arms
   that joined the roster read 1.00x**, the mutable fills' own tier, so neither
   the unrolled nor the short-body fill buys its time with allocation; the two
   unordered arms are the exception and they are the first arms here to sit
   BELOW the result vector, at 0.00x, returning a slice rather than filling
   anything. On a pair whose two halves are different compilers this
   is the property that says a difference is codegen and not the program:
   allocation is deterministic per call, none of these levels moved, and the two
   halves agree on 1123 of 1272 allocating cells.

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

**Run 22 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) records every class
on BOTH halves**, one process each, in [the
sequence](../README.md#making-a-major-benchmark-run) --- but NOT all in one
window, which is this run's own departure and is said here because a class block
cannot say it: sixteen of the eighteen class processes ran in the overnight
window with the two main sets, and the two `runs` processes ran after the box
came back, eight hours later. The plateau gate is what makes them one run, all
twenty processes asserting their preamble victim inside a 2.60% spread against
a 5% band. Every table below is the **basis half**'s, which on this run
is the 9.12 one, the half that keeps the lineage. What the second half buys
is that a pair's variable can be read on a class, which is what settled Run 14's
`scaled` question. **Read across the halves and the direction Runs 19, 20 and 21
all found has broken.** Of the 441 arm-comparisons the nine classes carry, three
(`reshape1`'s canonicalizing arms) sit out the vote and the geomeans
as degenerate; **215 put the 9.12 half faster and 223 slower**, and the nine
geomeans no longer all fall below 1: they run **0.9595 on `bcast` to 1.0928
on `reshape1`**, where Run 21's nine ran 0.9749 to 0.9945 and Run 20's eight
0.9700 to 0.9952. So on the classes, unlike on the three runs before, GHC HEAD
does not cost this roster everywhere. **The extreme at one end is the arm Runs
20 and 21 both named and it now holds eight of the nine**:
`mut-odo-vecdims-add-in-leaf` is the low extreme in eight of the nine, `bcast`
being the exception --- there the class's low extreme is `lib-stage2-disp`
at **0.6753** and the leaf arm reads 0.7100. **The other end wants reading
before it is quoted**, as it has every run: the largest figure any class reports
is `lib-stage2` at **2.6120** on `reshape1`, and that class's canonicalizing
arms return O(1) on three of its four shapes, so a ratio there prices dispatch
and not filling --- `lib-stage2-lean`, `lib-stage2-short` and `lib-stage2-u4`
are degenerate there and kept out of the extremes entirely. **And five classes
disqualify their own cross-half line**, where Run 21 had three, two of them
the same classes: `bcastmid` at 1.0106, `reshape1` at 0.9900, `window`
at 1.0082, `scaled` at 0.9911 and `runs` at 1.0114 move `list` past the 0.7%
bar, so their lines say so and are not read for the compiler --- and the main
set, at 0.81%, is past it too for the first time in three runs.

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
the leading arm OF the family, each with its name, since which arm leads is half
of what the column says --- so where property 2 breaks the two name different
arms and the gap between them is what the break is worth, and Run 21's table,
which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong
to; *floor* is the largest deviation from 1 among that process's sixteen A/A
controls. A cell that breaks one of [the three
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
   and `runs` at eleven --- so the line always prints;
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
| `rev` | 3 | 0.046 | 0.067 | **`libunord-stage2`** 0.001 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 | 2.35% |
| `revsome` | 3 | 0.048 | 0.058 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.027 | 3.31% |
| `bcast` | 3 | 0.035 | 0.062 | **`lib-stage2-u4`** 0.019 | `mut-odo-vecdims-add-in-leaf` 0.022 | 4.57% |
| `bcastmid` | 4 | 0.032 | 0.058 | **`lib-stage2-u4`** 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 5.39% |
| `reshape1` | 4 | 0.094 | 0.109 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.024 | 4.96% |
| `slice` | 3 | 0.040 | 0.057 | **`lib-stage2-short`** 0.030 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.030 | 3.44% |
| `window` | 3 | 0.062 | 0.095 | **`lib-stage2-short`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.029 | 4.77% |
| `scaled` | 3 | 0.032 | 0.033 | **`lib-stage2-u4`** 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 4.14% |
| `runs` | 11 | 0.034 | 0.063 | **`lib-stage2-short`** 0.027 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.028 | 3.26% |

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
| *bq-expand-nosum* | *--* | *--* | *0.10* | *134* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.09* | *144* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.26* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.04* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| libunord-stage2 | 0.001 | 0.003 | 0.06 | 157 | 0.01x |
| lib-stage2-short | 0.024 | 0.029 | 0.10 | 148 | 1.01x |
| lib-stage2-lean | 0.027 | 0.034 | 0.09 | 146 | 1.01x |
| lib-stage2 | 0.027 | 0.035 | 0.07 | 146 | 1.01x |
| lib-stage2-disp | 0.027 | 0.035 | 0.07 | 146 | 1.01x |
| lib-stage2-concat | 0.027 | 0.035 | 0.09 | 146 | 1.01x |
| lib-stage2-u4 | 0.028 | 0.039 | 0.09 | 145 | 1.01x |
| lib-stage1 | 0.029 | 0.047 | 0.09 | 146 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.029 | 0.045 | 0.10 | 146 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.029 | 0.045 | 0.09 | 146 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.050 | 0.10 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.057 | 0.19 | 142 | 1.00x |
| liblist-stage2 | 0.041 | 0.046 | 0.27 | 142 | 2.01x |
| liblist-stage1 | 0.044 | 0.058 | 0.32 | 142 | 2.01x |
| libunord-stage1 | 0.045 | 0.061 | 0.35 | 142 | 2.03x |
| *mut-odo-vecdims-aa* | *0.046* | *0.067* | *0.07* | *137* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.046* | *0.067* | *0.07* | *137* | *1.00x* |
| mut-odo-vecdims-add-in | 0.046 | 0.067 | 0.06 | 137 | 1.00x |
| **mut-odo-vecdims** | **0.046** | 0.067 | 0.07 | 137 | 1.00x |
| mid-copy | 0.048 | 0.072 | 0.10 | 137 | 1.00x |
| canon-vecdims | 0.048 | 0.056 | 0.09 | 137 | 1.01x |
| bcast-set | 0.049 | 0.070 | 0.06 | 136 | 1.00x |
| canon-memcpy-r2 | 0.052 | 0.059 | 0.05 | 136 | 1.01x |
| canon-full | 0.055 | 0.063 | 0.06 | 136 | 1.01x |
| mut-flat-gm | 0.079 | 0.130 | 0.21 | 134 | 1.34x |
| mut-odo | 0.085 | 0.177 | 0.27 | 126 | 1.00x |
| *mut-odo-aa-distant* | *0.086* | *0.178* | *0.37* | *125* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.087* | *0.188* | *0.81* | *125* | *1.00x* |
| bq-expand-gm-mulback | 0.091 | 0.167 | 0.14 | 130 | 2.52x |
| *build-aa-adjacent* | *0.093* | *0.181* | *0.12* | *124* | *1.00x* |
| bq-mut-runs-gm-mulback | 0.095 | 0.134 | 0.16 | 132 | 1.34x |
| bq-odo-gm-mulback | 0.096 | 0.117 | 0.14 | 131 | 1.41x |
| *bq-odo-gm-mulback-aa-distant* | *0.096* | *0.117* | *0.12* | *131* | *1.41x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.096* | *0.117* | *0.12* | *131* | *1.41x* |
| **bq-scan-rem-gm-mulback** | **0.096** | 0.098 | 0.06 | 128 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.098* | *0.098* | *0.08* | *128* | *1.34x* |
| *build-aa-distant* | *0.098* | *0.176* | *1.27* | *124* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.098* | *0.09* | *128* | *1.34x* |
| build | 0.101 | 0.168 | 0.80 | 124 | 1.00x |
| bq-expand | 0.102 | 0.176 | 0.10 | 129 | 2.52x |
| *bq-expand-aa-distant* | *0.102* | *0.175* | *0.12* | *129* | *2.52x* |
| *bq-expand-aa-adjacent* | *0.103* | *0.175* | *0.11* | *128* | *2.52x* |
| offtab-scan-rem | 0.127 | 0.129 | 0.06 | 124 | 2.00x |
| *list-aa-adjacent* | *0.996* | *0.998* | *0.18* | *86* | *23.43x* |
| *list-aa-distant* | *0.998* | *1.010* | *0.28* | *86* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.27 | 86 | 23.43x |
| *gen-unsafe-aa-distant* | *1.243* | *1.423* | *0.92* | *82* | *1.00x* |
| gen-unsafe | 1.257 | 1.479 | 2.06 | 81 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.372* | *1.404* | *1.50* | *80* | *1.00x* |

**Controls:** The largest A/A pair is `mut-odo-aa-adjacent` at 1.0235, worst
cell 5.88% on `rev-cnn-L1-24x24-c1`, and 14 of 16 intervals cover 1.
The `sum-only` halves agree at 0.9989 on a worst cell of 0.28%
on `rev-cnn-L1-24x24-c1`, its interval missing 1. The in-situ term reads 0.9969,
1.0109, 1.0004, 1.0069 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0201, which
the correction amplifies by 1.43x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m14s, peak 96 MiB in use, 26 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.21 ms per call raw, 4.05 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes):** `mut-odo-vecdims` 0.067/0.052/0.028 `bq-scan-rem-gm-mulback`
0.097/0.098/0.091

**Across the halves:** 20 of the 49 arms are faster on this half and 29 slower,
at a geomean of 1.0100, from `mut-odo-vecdims-add-in-leaf` at 0.8435
to `libunord-stage2` at 1.4348, with `list` itself at 1.0069.

**What the class says:** properties 1 and 3 hold for `mut-odo-vecdims` --
`worst` 0.067 against a `list` it never loses to, and the tiers at 1.00x, 2.52x
and 23.43x -- and property 2 breaks outright, as it does in all nine classes
this run. The arm at the top is `libunord-stage2` at 0.001, **0.0174
of `mut-odo-vecdims` on 3 of 3 shapes**, and the margin is 98% against a 2.35%
floor: this is the unordered one-block test firing on every view of the class,
exactly where `probe-oneblock.py` said it would, collapsing the view to a single
`VS.slice`. So the break prices dispatch and not filling, and the honest leader
among arms that do the work is `lib-stage1`. Nineteen cells changed level
mid-bench here, the largest `-12.76%`
on `rev-gather48-src-50/mut-odo-vecdims-nosum`; read each as a question rather
than a verdict.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.19* | *90* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.09* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.16* | *94* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| libunord-stage2 | 0.000 | 0.001 | 0.01 | 116 | 0.00x |
| lib-stage2-short | 0.024 | 0.029 | 0.15 | 102 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.033 | 0.09 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.033 | 0.12 | 101 | 1.00x |
| lib-stage1 | 0.027 | 0.033 | 0.08 | 101 | 1.00x |
| lib-stage2-lean | 0.028 | 0.035 | 0.09 | 101 | 1.00x |
| lib-stage2 | 0.028 | 0.034 | 0.10 | 101 | 1.00x |
| lib-stage2-concat | 0.028 | 0.034 | 0.09 | 101 | 1.00x |
| lib-stage2-disp | 0.028 | 0.035 | 0.09 | 100 | 1.00x |
| lib-stage2-u4 | 0.029 | 0.038 | 0.15 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.037 | 0.09 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.035 | 0.043 | 0.11 | 98 | 1.00x |
| liblist-stage1 | 0.041 | 0.045 | 0.39 | 97 | 2.00x |
| libunord-stage1 | 0.042 | 0.045 | 0.18 | 97 | 2.00x |
| liblist-stage2 | 0.042 | 0.046 | 0.25 | 97 | 2.00x |
| mid-copy | 0.047 | 0.059 | 0.08 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.048 | 0.058 | 0.08 | 96 | 1.00x |
| **mut-odo-vecdims** | **0.048** | 0.058 | 0.07 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.048* | *0.058* | *0.08* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.048* | *0.058* | *0.07* | *96* | *1.00x* |
| canon-vecdims | 0.051 | 0.057 | 0.07 | 96 | 1.00x |
| bcast-set | 0.051 | 0.062 | 0.10 | 96 | 1.00x |
| canon-memcpy-r2 | 0.054 | 0.060 | 0.09 | 96 | 1.00x |
| canon-full | 0.056 | 0.064 | 0.10 | 96 | 1.00x |
| mut-flat-gm | 0.078 | 0.089 | 0.20 | 88 | 1.33x |
| mut-odo | 0.087 | 0.149 | 0.94 | 96 | 1.00x |
| bq-mut-runs-gm-mulback | 0.089 | 0.100 | 0.17 | 86 | 1.33x |
| bq-expand-gm-mulback | 0.091 | 0.121 | 0.18 | 83 | 2.52x |
| *build-aa-adjacent* | *0.099* | *0.149* | *0.13* | *96* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.100* | *0.101* | *0.09* | *86* | *1.33x* |
| *mut-odo-aa-adjacent* | *0.101* | *0.150* | *0.27* | *96* | *1.00x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.101* | *0.101* | *0.13* | *86* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.101** | 0.101 | 0.11 | 86 | 1.33x |
| *mut-odo-aa-distant* | *0.103* | *0.151* | *0.84* | *96* | *1.00x* |
| *bq-odo-gm-mulback-aa-distant* | *0.103* | *0.125* | *0.10* | *83* | *1.41x* |
| bq-odo-gm-mulback | 0.104 | 0.125 | 0.13 | 83 | 1.41x |
| *bq-expand-aa-distant* | *0.104* | *0.130* | *0.13* | *83* | *2.52x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.104* | *0.124* | *0.14* | *83* | *1.41x* |
| *build-aa-distant* | *0.104* | *0.152* | *1.74* | *96* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.105* | *0.131* | *0.18* | *83* | *2.52x* |
| bq-expand | 0.105 | 0.131 | 0.12 | 83 | 2.52x |
| build | 0.112 | 0.149 | 0.65 | 96 | 1.00x |
| offtab-scan-rem | 0.131 | 0.132 | 0.14 | 82 | 2.00x |
| *list-aa-adjacent* | *0.997* | *0.998* | *0.18* | *47* | *23.43x* |
| *list-aa-distant* | *0.997* | *1.001* | *0.17* | *47* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.22 | 47 | 23.43x |
| *gen-unsafe-aa-distant* | *1.317* | *1.485* | *0.97* | *42* | *1.00x* |
| gen-unsafe | 1.317 | 1.474 | 0.95 | 42 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.329* | *1.600* | *2.98* | *42* | *1.00x* |

**Controls:** The largest A/A pair is `mut-odo-aa-distant` at 1.0331, worst cell
9.03% on `revsome-outer-g48`, and 10 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0011 on a worst cell of 0.34% on `revsome-outer-g48`,
its interval covering 1. The in-situ term reads 1.0157, 1.0126, 1.0299, 1.0092
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0264, which the correction amplifies
by 1.44x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m17s, peak 117 MiB in use, 26 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 4.19 ms per call raw, 4.04 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.053/0.058
`bq-scan-rem-gm-mulback` 0.101/0.101/0.099

**Across the halves:** 24 of the 49 arms are faster on this half and 25 slower,
at a geomean of 1.0129, from `mut-odo-vecdims-add-in-leaf` at 0.8321
to `libunord-stage2` at 1.3139, with `list` itself at 1.0069.

**What the class says:** the same shape as `rev` and for the same reason --
`libunord-stage2` at 0.000, **0.0076 of `mut-odo-vecdims` on 3 of 3**, 99%
against a 3.31% floor, the one-block test firing on every view -- so property 2
breaks to a degenerate cell and properties 1 and 3 hold. The class's own
contribution is that it separates the two stages' tests: stage one's does
not fire here, and `libunord-stage1` tracks `liblist-stage1` at 1.0090, inside
the floor.

**`bcast` --- an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.96* | *52* | *1.38x* |
| *canon-full-nosum* | *--* | *--* | *0.44* | *83* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.70* | *58* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.30* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-u4 | 0.019 | 0.027 | 0.55 | 61 | 1.00x |
| lib-stage2-lean | 0.019 | 0.026 | 0.52 | 61 | 1.00x |
| lib-stage2-disp | 0.019 | 0.026 | 0.51 | 61 | 1.00x |
| lib-stage2-short | 0.019 | 0.027 | 0.51 | 61 | 1.00x |
| lib-stage2 | 0.019 | 0.026 | 0.51 | 61 | 1.00x |
| lib-stage2-concat | 0.019 | 0.026 | 0.50 | 61 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.022 | 0.023 | 0.53 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.024 | 0.027 | 0.52 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.027 | 0.49 | 60 | 1.00x |
| lib-stage1 | 0.025 | 0.027 | 0.50 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.031 | 0.032 | 0.54 | 58 | 1.00x |
| bcast-set | 0.033 | 0.062 | 0.54 | 61 | 1.00x |
| canon-full | 0.033 | 0.061 | 0.72 | 61 | 1.00x |
| mid-copy | 0.035 | 0.062 | 0.54 | 60 | 1.00x |
| *mut-odo-vecdims-aa* | *0.035* | *0.062* | *0.50* | *60* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.035* | *0.062* | *0.39* | *60* | *1.00x* |
| **mut-odo-vecdims** | **0.035** | 0.062 | 0.44 | 60 | 1.00x |
| canon-vecdims | 0.035 | 0.062 | 0.55 | 60 | 1.00x |
| mut-odo-vecdims-add-in | 0.035 | 0.062 | 0.51 | 60 | 1.00x |
| canon-memcpy-r2 | 0.037 | 0.067 | 0.54 | 60 | 1.00x |
| libunord-stage2 | 0.041 | 0.045 | 0.95 | 54 | 2.00x |
| liblist-stage1 | 0.045 | 0.051 | 0.92 | 53 | 2.00x |
| liblist-stage2 | 0.045 | 0.046 | 1.03 | 54 | 2.00x |
| libunord-stage1 | 0.045 | 0.051 | 0.83 | 53 | 2.00x |
| *build-aa-adjacent* | *0.058* | *0.146* | *1.68* | *60* | *1.00x* |
| build | 0.058 | 0.157 | 1.88 | 60 | 1.00x |
| mut-odo | 0.059 | 0.162 | 0.57 | 60 | 1.00x |
| *mut-odo-aa-distant* | *0.059* | *0.160* | *1.81* | *60* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.060* | *0.164* | *0.97* | *60* | *1.00x* |
| *build-aa-distant* | *0.061* | *0.163* | *0.41* | *60* | *1.00x* |
| mut-flat-gm | 0.066 | 0.071 | 0.75 | 49 | 1.13x |
| bq-expand-gm-mulback | 0.078 | 0.082 | 0.65 | 48 | 1.38x |
| bq-mut-runs-gm-mulback | 0.080 | 0.089 | 0.63 | 47 | 1.13x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.083* | *0.088* | *0.66* | *47* | *1.14x* |
| bq-odo-gm-mulback | 0.083 | 0.088 | 0.65 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-distant* | *0.083* | *0.088* | *0.43* | *47* | *1.14x* |
| bq-expand | 0.091 | 0.097 | 0.65 | 46 | 1.38x |
| *bq-expand-aa-adjacent* | *0.091* | *0.097* | *0.70* | *46* | *1.38x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.091* | *0.100* | *0.06* | *47* | *1.13x* |
| *bq-expand-aa-distant* | *0.093* | *0.097* | *0.43* | *46* | *1.38x* |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.099 | 0.66 | 47 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.099* | *0.67* | *47* | *1.13x* |
| offtab-scan-rem | 0.127 | 0.142 | 1.02 | 43 | 2.00x |
| gen-unsafe | 0.915 | 1.089 | 2.50 | 21 | 1.00x |
| *gen-unsafe-aa-adjacent* | *0.948* | *1.156* | *1.42* | *20* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.12 | 18 | 20.62x |
| *list-aa-distant* | *1.002* | *1.008* | *1.18* | *18* | *20.62x* |
| *list-aa-adjacent* | *1.003* | *1.007* | *0.73* | *18* | *20.62x* |
| *gen-unsafe-aa-distant* | *1.049* | *1.081* | *2.53* | *21* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0457, worst
cell 6.18% on `bcast-inner8`, and 10 of 16 intervals cover 1. The `sum-only`
halves agree at 0.9999 on a worst cell of 0.05% on `bcast-inner8`, its interval
covering 1. The in-situ term reads 1.0207, 1.0090, 0.9936, 1.0089 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0440, which the correction amplifies by 1.04x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h14m21s, peak 151 MiB in use, 45 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 28.2 ms per call raw, 27.1 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900,
bcast-tall-Mx2):** `mut-odo-vecdims` 0.032/0.022/0.062 `bq-scan-rem-gm-mulback`
0.091/0.089/0.099

**Across the halves:** 30 of the 49 arms are faster on this half and 19 slower,
at a geomean of 0.9595, from `lib-stage2-disp` at 0.6753
to `mut-odo-vecdims-add-in-leaf-down` at 1.3980, with `list` itself at 1.0038.

**What the class says:** property 2 breaks to a fill that is doing the work,
which is new. `lib-stage2-u4` leads at 0.019, **0.5968 of `mut-odo-vecdims` on 3
of 3 shapes**, a 40.3% margin against a 4.57% floor -- so on a broadcast
the stepping run unrolled by four is worth a factor of one and two thirds
over the shipped fill, on a class where the registration expected the unrolling
to buy nothing. Properties 1 and 3 hold, `bq-expand` at 1.38x. **And this
is the one population where registration 5 fails**: `-u2` against `-down` reads
1.1306 on the control at 0 of 3 shapes, `-down` ahead by 13% past this class's
own control floor of 2.79%, where the basis reads 0.8042 the other way.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000,
`sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed
2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k`
is its worst, its block taken to 150000 elements where the class's others run 3
to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.37* | *69* | *1.57x* |
| *canon-full-nosum* | *--* | *--* | *0.54* | *104* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.47* | *75* | *1.17x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| lib-stage2-u4 | 0.017 | 0.032 | 0.39 | 80 | 1.00x |
| lib-stage2-concat | 0.017 | 0.032 | 0.31 | 80 | 1.00x |
| lib-stage2 | 0.017 | 0.032 | 0.33 | 80 | 1.00x |
| lib-stage2-disp | 0.017 | 0.032 | 0.34 | 80 | 1.00x |
| lib-stage2-lean | 0.017 | 0.032 | 0.34 | 80 | 1.00x |
| lib-stage2-short | 0.017 | 0.035 | 0.33 | 80 | 1.00x |
| mid-copy | 0.017 | 0.033 | 0.37 | 80 | 1.00x |
| canon-full | 0.019 | 0.033 | 0.41 | 80 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.033 | 0.32 | 79 | 1.00x |
| lib-stage1 | 0.022 | 0.033 | 0.32 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.022 | 0.033 | 0.33 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.023 | 0.038 | 0.32 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.028 | 0.044 | 0.48 | 76 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.058 | 0.38 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.059* | *0.41* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.058 | 0.27 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.058* | *0.28* | *76* | *1.00x* |
| canon-vecdims | 0.032 | 0.059 | 0.38 | 75 | 1.00x |
| liblist-stage2 | 0.033 | 0.048 | 0.57 | 74 | 2.00x |
| libunord-stage2 | 0.033 | 0.047 | 0.55 | 74 | 2.00x |
| bcast-set | 0.033 | 0.062 | 0.31 | 76 | 1.00x |
| canon-memcpy-r2 | 0.034 | 0.062 | 0.38 | 75 | 1.00x |
| libunord-stage1 | 0.037 | 0.044 | 0.56 | 74 | 2.00x |
| liblist-stage1 | 0.038 | 0.044 | 0.58 | 74 | 2.00x |
| *mut-odo-aa-distant* | *0.049* | *0.137* | *1.40* | *68* | *1.00x* |
| mut-odo | 0.050 | 0.152 | 0.29 | 68 | 1.00x |
| *build-aa-adjacent* | *0.051* | *0.148* | *1.24* | *68* | *1.00x* |
| build | 0.051 | 0.151 | 0.37 | 68 | 1.00x |
| *mut-odo-aa-adjacent* | *0.051* | *0.152* | *0.30* | *68* | *1.00x* |
| *build-aa-distant* | *0.052* | *0.154* | *1.24* | *68* | *1.00x* |
| mut-flat-gm | 0.062 | 0.089 | 0.71 | 68 | 1.17x |
| bq-mut-runs-gm-mulback | 0.073 | 0.104 | 0.64 | 66 | 1.17x |
| bq-expand-gm-mulback | 0.077 | 0.123 | 0.45 | 64 | 1.57x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.080* | *0.101* | *0.28* | *64* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.080** | 0.101 | 0.43 | 64 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.080* | *0.101* | *0.39* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-distant* | *0.080* | *0.126* | *0.35* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.080* | *0.127* | *0.47* | *64* | *1.17x* |
| bq-odo-gm-mulback | 0.080 | 0.127 | 0.42 | 64 | 1.17x |
| *bq-expand-aa-adjacent* | *0.086* | *0.133* | *0.40* | *64* | *1.57x* |
| *bq-expand-aa-distant* | *0.086* | *0.132* | *0.35* | *64* | *1.57x* |
| bq-expand | 0.086 | 0.133 | 0.43 | 64 | 1.57x |
| offtab-scan-rem | 0.108 | 0.132 | 0.69 | 60 | 2.00x |
| gen-unsafe | 0.955 | 1.431 | 2.51 | 28 | 1.00x |
| *gen-unsafe-aa-distant* | *0.980* | *1.430* | *2.22* | *28* | *1.00x* |
| *list-aa-distant* | *0.989* | *1.005* | *1.16* | *30* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 1.00 | 29 | 21.22x |
| *list-aa-adjacent* | *1.002* | *1.006* | *1.06* | *29* | *21.22x* |
| *gen-unsafe-aa-adjacent* | *1.007* | *1.486* | *3.41* | *28* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0539, worst
cell 12.23% on `bcastmid-block150k`, and 14 of 16 intervals cover 1.
The `sum-only` halves agree at 1.0011 on a worst cell of 0.45%
on `bcastmid-c32-cnn`, its interval covering 1. The in-situ term reads 1.0180,
1.0392, 1.0194, 1.0512 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0522, which
the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h19m3s, peak 149 MiB in use, 38 MiB max residency;
the reader reads 55 benchmarks over 4 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 48.5 ms per call raw, 47.4 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.058/0.021/0.036/0.023
`bq-scan-rem-gm-mulback` 0.101/0.088/0.069/0.066

**Across the halves:** 26 of the 49 arms are faster on this half and 23 slower,
at a geomean of 0.9964, from `mut-odo-vecdims-add-in-leaf` at 0.8069
to `mut-odo-vecdims-add-in-leaf-down` at 1.2157, with `list` itself at 1.0106.
**The baseline moved 1.06% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** `lib-stage2-u4` leads again at 0.017, **0.5258
of `mut-odo-vecdims` on 4 of 4 shapes**, 47.4% against a 5.39% floor --
the widest of the three `-u4` classes and the clearest statement
that the unrolling pays where the runs are long and regular. Properties 1 and 3
hold. `mid-copy`, which led this class on Runs 20 and 21, is no longer its head.

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
| *bq-expand-nosum* | *--* | *--* | *0.35* | *84* | *4.91x* |
| *canon-full-nosum* | *--* | *--* | *0.35* | *253* | *0.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.55* | *102* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.21* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| libunord-stage2 | 0.000 | 0.000 | 0.01 | 114 | 0.00x |
| canon-vecdims | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| canon-full | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| lib-stage2-concat | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| canon-memcpy-r2 | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| lib-stage2-disp | 0.000 | 0.015 | 0.05 | 110 | 0.00x |
| lib-stage2 | 0.000 | 0.015 | 0.01 | 110 | 0.00x |
| lib-stage2-short | 0.001 | 0.016 | 0.01 | 110 | 0.00x |
| lib-stage2-u4 | 0.001 | 0.014 | 0.03 | 110 | 0.00x |
| lib-stage2-lean | 0.002 | 0.015 | 0.02 | 110 | 0.00x |
| liblist-stage2 | 0.011 | 0.025 | 0.16 | 104 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.024 | 0.057 | 0.10 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.057 | 0.08 | 100 | 1.00x |
| lib-stage1 | 0.025 | 0.057 | 0.10 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.030 | 0.066 | 0.13 | 98 | 1.00x |
| bq-mut-runs-gm-mulback | 0.034 | 0.129 | 0.40 | 96 | 2.00x |
| liblist-stage1 | 0.034 | 0.063 | 0.17 | 96 | 2.00x |
| libunord-stage1 | 0.035 | 0.063 | 0.18 | 96 | 2.00x |
| mut-flat-gm | 0.035 | 0.132 | 0.23 | 96 | 2.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.038 | 0.069 | 0.08 | 96 | 1.00x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.049* | *0.142* | *0.16* | *92* | *2.26x* |
| bq-odo-gm-mulback | 0.049 | 0.142 | 0.15 | 92 | 2.26x |
| *bq-odo-gm-mulback-aa-distant* | *0.050* | *0.140* | *0.15* | *92* | *2.26x* |
| bq-expand-gm-mulback | 0.074 | 0.169 | 0.31 | 87 | 4.91x |
| offtab-scan-rem | 0.075 | 0.093 | 0.15 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.075* | *0.093* | *0.12* | *86* | *2.00x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.075* | *0.093* | *0.12* | *86* | *2.00x* |
| **bq-scan-rem-gm-mulback** | **0.075** | 0.093 | 0.14 | 86 | 2.00x |
| **mut-odo-vecdims** | **0.094** | 0.109 | 0.08 | 82 | 1.00x |
| mut-odo-vecdims-add-in | 0.094 | 0.109 | 0.10 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.095* | *0.109* | *0.13* | *82* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.095* | *0.109* | *0.18* | *82* | *1.00x* |
| bcast-set | 0.095 | 0.107 | 0.13 | 82 | 1.00x |
| mid-copy | 0.095 | 0.120 | 0.20 | 82 | 1.00x |
| bq-expand | 0.116 | 0.202 | 0.32 | 80 | 4.91x |
| *bq-expand-aa-adjacent* | *0.116* | *0.202* | *0.30* | *80* | *4.91x* |
| *bq-expand-aa-distant* | *0.116* | *0.200* | *0.24* | *80* | *4.91x* |
| *mut-odo-aa-adjacent* | *0.259* | *0.319* | *2.10* | *66* | *1.00x* |
| mut-odo | 0.263 | 0.321 | 2.86 | 66 | 1.00x |
| *mut-odo-aa-distant* | *0.264* | *0.326* | *1.35* | *66* | *1.00x* |
| build | 0.267 | 0.344 | 1.53 | 65 | 1.00x |
| *build-aa-adjacent* | *0.272* | *0.339* | *1.20* | *64* | *1.00x* |
| *build-aa-distant* | *0.284* | *0.319* | *1.58* | *64* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.968* | *2.166* | *2.14* | *42* | *1.00x* |
| gen-unsafe | 0.968 | 2.353 | 1.62 | 42 | 1.00x |
| *gen-unsafe-aa-distant* | *0.972* | *2.241* | *3.05* | *42* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 0.28 | 41 | 32.29x |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.27* | *42* | *32.29x* |
| *list-aa-distant* | *1.001* | *1.005* | *0.35* | *41* | *32.29x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 1.0496, worst cell
18.15% on `reshape1-strided-r3`, and 15 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0006 on a worst cell of 0.35% on `reshape1-r3`, its interval
covering 1. The in-situ term reads 0.9826, 1.0044, 1.0437, 1.1293 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0449, which the correction amplifies by 1.08x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h19m0s, peak 158 MiB in use, 37 MiB max residency;
the reader reads 55 benchmarks over 4 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 13.1 ms per call raw, 12.8 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10,
reshape1-strided-r3):** `mut-odo-vecdims` 0.091/0.092/0.109/0.094
`bq-scan-rem-gm-mulback` 0.074/0.073/0.093/0.075

**Across the halves:** 18 of the 46 voting arms are faster on this half and 28
slower, at a geomean of 1.0928, from `mut-odo-vecdims-add-in-leaf` at 0.8057
to `lib-stage2` at 2.6120, `lib-stage2-lean`, `lib-stage2-short`,
`lib-stage2-u4` sitting out as degenerate, a basis cell of theirs not left
positive by the correction, with `list` itself at 0.9900. **The baseline moved
1.00% between the halves, past the 0.7% that lets two columns be differenced,
so this line is NOT read for the pair's variable.** The table above is one
process's and stands; what goes is the comparison.

**What the class says:** the class remains the one whose cells price dispatch
rather than filling -- the canonicalizing arms return O(1) on three of its four
shapes -- and property 2 breaks to `libunord-stage2` at 0.000, 0.0008
of `mut-odo-vecdims`, which is that degeneracy compounded by the one-block test
firing on every view. Properties 1 and 3 hold, and property 3's `bq-expand`
reads **4.91x**, the top of the range across all nine classes, which
is this class's own `m` showing through exactly as the property warns. Four
cells sink below the forcing pass here on the basis, so `lib-stage2-lean` covers
2 of 4 shapes and `-short` and `-u4` 3 of 4.

**`slice` --- a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *90* | *1.58x* |
| *canon-full-nosum* | *--* | *--* | *0.08* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.29* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| lib-stage2-short | 0.030 | 0.033 | 0.07 | 101 | 1.00x |
| lib-stage2-u4 | 0.030 | 0.040 | 0.08 | 98 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.030 | 0.033 | 0.09 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.030 | 0.034 | 0.09 | 100 | 1.00x |
| lib-stage1 | 0.030 | 0.034 | 0.13 | 100 | 1.00x |
| lib-stage2-lean | 0.031 | 0.036 | 0.13 | 100 | 1.00x |
| lib-stage2 | 0.032 | 0.036 | 0.07 | 100 | 1.00x |
| lib-stage2-disp | 0.032 | 0.036 | 0.08 | 100 | 1.00x |
| lib-stage2-concat | 0.032 | 0.036 | 0.07 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.038 | 0.10 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.039 | 0.043 | 0.10 | 97 | 1.00x |
| mut-odo-vecdims-add-in | 0.039 | 0.057 | 0.12 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.057* | *0.08* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.040* | *0.057* | *0.09* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.040** | 0.057 | 0.08 | 96 | 1.00x |
| canon-vecdims | 0.040 | 0.058 | 0.08 | 96 | 1.00x |
| mid-copy | 0.040 | 0.059 | 0.09 | 96 | 1.00x |
| canon-memcpy-r2 | 0.041 | 0.061 | 0.09 | 96 | 1.00x |
| bcast-set | 0.042 | 0.061 | 0.09 | 96 | 1.00x |
| canon-full | 0.042 | 0.065 | 0.08 | 96 | 1.00x |
| liblist-stage2 | 0.045 | 0.049 | 0.16 | 96 | 2.00x |
| liblist-stage1 | 0.045 | 0.048 | 0.27 | 96 | 2.00x |
| libunord-stage1 | 0.045 | 0.048 | 0.24 | 96 | 2.00x |
| libunord-stage2 | 0.046 | 0.051 | 0.22 | 95 | 2.01x |
| *mut-odo-aa-distant* | *0.065* | *0.140* | *0.09* | *96* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.066* | *0.146* | *0.18* | *96* | *1.00x* |
| build | 0.067 | 0.148 | 0.48 | 96 | 1.00x |
| mut-odo | 0.067 | 0.147 | 1.55 | 96 | 1.00x |
| *build-aa-distant* | *0.067* | *0.153* | *0.56* | *96* | *1.00x* |
| *build-aa-adjacent* | *0.068* | *0.157* | *0.37* | *96* | *1.00x* |
| mut-flat-gm | 0.084 | 0.088 | 0.12 | 88 | 1.08x |
| bq-mut-runs-gm-mulback | 0.093 | 0.094 | 0.28 | 87 | 1.08x |
| **bq-scan-rem-gm-mulback** | **0.099** | 0.103 | 0.10 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.099* | *0.103* | *0.11* | *86* | *1.08x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.099* | *0.103* | *0.07* | *86* | *1.08x* |
| bq-expand-gm-mulback | 0.104 | 0.119 | 0.11 | 83 | 1.58x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.110* | *0.121* | *0.13* | *83* | *1.50x* |
| bq-odo-gm-mulback | 0.110 | 0.121 | 0.15 | 83 | 1.50x |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.122* | *0.11* | *83* | *1.50x* |
| bq-expand | 0.110 | 0.128 | 0.10 | 83 | 1.58x |
| *bq-expand-aa-adjacent* | *0.110* | *0.128* | *0.10* | *83* | *1.58x* |
| *bq-expand-aa-distant* | *0.111* | *0.129* | *0.09* | *83* | *1.58x* |
| offtab-scan-rem | 0.130 | 0.133 | 0.12 | 82 | 2.00x |
| *list-aa-distant* | *0.998* | *1.008* | *0.29* | *46* | *20.54x* |
| list (baseline) | 1.000 | 1.000 | 0.22 | 46 | 20.54x |
| *list-aa-adjacent* | *1.004* | *1.011* | *0.23* | *46* | *20.54x* |
| *gen-unsafe-aa-adjacent* | *1.585* | *2.609* | *1.71* | *42* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.608* | *2.646* | *1.48* | *42* | *1.00x* |
| gen-unsafe | 1.642 | 2.709 | 1.47 | 42 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 0.9656, worst
cell 5.80% on `slice-cnn-L2-24x24-c32`, and 10 of 16 intervals cover 1.
The `sum-only` halves agree at 0.9983 on a worst cell of 0.48%
on `slice-cnn-L2-24x24-c32`, its interval missing 1. The in-situ term reads
1.0154, 1.0192, 1.0154, 1.0388 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9663, which
the correction amplifies by 1.02x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m15s, peak 121 MiB in use, 38 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.14 ms per call raw, 3.98 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7):** `mut-odo-vecdims` 0.057/0.030/0.037
`bq-scan-rem-gm-mulback` 0.098/0.103/0.096

**Across the halves:** 26 of the 49 arms are faster on this half and 23 slower,
at a geomean of 1.0055, from `mut-odo-vecdims-add-in-leaf` at 0.8535
to `mut-odo-vecdims-add-in-leaf-down` at 1.1831, with `list` itself at 0.9964.

**What the class says:** `lib-stage2-short` leads at 0.030, **0.7522
of `mut-odo-vecdims` on 3 of 3 shapes**, 24.8% against a 3.44% floor. Properties
1 and 3 hold. This is one of the two classes where registration 1's ratio sits
above 1 -- `lib-stage2` / `lib-stage1` reads 1.0344 -- and it is the population
the registration singled out as still behind past its floor on Run 21
and predicted inside 1.05; it lands there, so the eight points that cost
it then are gone and the three the shim accounts for remain.

**`window` --- overlapping im2col patches: the workload the README opens
by naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.21* | *116* | *2.81x* |
| *canon-full-nosum* | *--* | *--* | *0.44* | *153* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.40* | *134* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.09* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *150* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *150* | *0.00x* |
| lib-stage2-short | 0.020 | 0.028 | 0.12 | 140 | 1.01x |
| lib-stage2-u4 | 0.022 | 0.038 | 0.16 | 141 | 1.01x |
| lib-stage2-lean | 0.024 | 0.034 | 0.06 | 140 | 1.00x |
| lib-stage2-disp | 0.025 | 0.034 | 0.06 | 140 | 1.01x |
| lib-stage2 | 0.025 | 0.034 | 0.08 | 140 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.029 | 0.031 | 0.15 | 133 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.029 | 0.031 | 0.12 | 132 | 1.00x |
| lib-stage1 | 0.030 | 0.031 | 0.07 | 132 | 1.01x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.037 | 0.15 | 130 | 1.00x |
| canon-vecdims | 0.037 | 0.058 | 0.07 | 137 | 1.01x |
| canon-memcpy-r2 | 0.038 | 0.061 | 0.95 | 137 | 1.01x |
| canon-full | 0.038 | 0.064 | 0.34 | 137 | 1.01x |
| liblist-stage1 | 0.039 | 0.044 | 0.46 | 129 | 2.01x |
| lib-stage2-concat | 0.040 | 0.147 | 0.18 | 109 | 1.02x |
| libunord-stage1 | 0.041 | 0.044 | 0.69 | 129 | 2.02x |
| mut-odo-vecdims-add-in-leaf-down | 0.041 | 0.041 | 0.07 | 128 | 1.00x |
| libunord-stage2 | 0.052 | 0.095 | 0.66 | 116 | 2.05x |
| liblist-stage2 | 0.054 | 0.093 | 0.48 | 116 | 2.02x |
| mut-odo-vecdims-add-in | 0.061 | 0.095 | 0.17 | 116 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.094* | *0.08* | *116* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.062* | *0.095* | *0.07* | *116* | *1.00x* |
| **mut-odo-vecdims** | **0.062** | 0.095 | 0.18 | 116 | 1.00x |
| mid-copy | 0.063 | 0.096 | 0.30 | 116 | 1.00x |
| bcast-set | 0.066 | 0.102 | 0.16 | 115 | 1.00x |
| mut-flat-gm | 0.069 | 0.087 | 0.31 | 126 | 1.33x |
| bq-mut-runs-gm-mulback | 0.074 | 0.099 | 0.46 | 127 | 1.33x |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.097 | 0.08 | 120 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.093* | *0.097* | *0.18* | *120* | *1.33x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.097* | *0.06* | *120* | *1.33x* |
| *bq-odo-gm-mulback-aa-distant* | *0.094* | *0.122* | *0.19* | *121* | *2.55x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.122* | *0.11* | *121* | *2.55x* |
| bq-odo-gm-mulback | 0.094 | 0.122 | 0.15 | 121 | 2.55x |
| bq-expand-gm-mulback | 0.098 | 0.118 | 0.22 | 119 | 2.81x |
| offtab-scan-rem | 0.112 | 0.127 | 0.07 | 120 | 2.00x |
| *bq-expand-aa-distant* | *0.120* | *0.128* | *0.11* | *112* | *2.81x* |
| bq-expand | 0.120 | 0.128 | 0.13 | 112 | 2.81x |
| *bq-expand-aa-adjacent* | *0.120* | *0.129* | *0.16* | *112* | *2.81x* |
| mut-odo | 0.153 | 0.265 | 1.83 | 98 | 1.00x |
| *mut-odo-aa-adjacent* | *0.155* | *0.260* | *1.55* | *98* | *1.00x* |
| *mut-odo-aa-distant* | *0.157* | *0.268* | *0.61* | *98* | *1.00x* |
| *build-aa-distant* | *0.165* | *0.276* | *2.67* | *97* | *1.00x* |
| build | 0.167 | 0.290 | 1.43 | 97 | 1.00x |
| *build-aa-adjacent* | *0.168* | *0.314* | *1.00* | *96* | *1.00x* |
| *list-aa-distant* | *0.999* | *1.002* | *0.36* | *73* | *24.76x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 73 | 24.76x |
| *list-aa-adjacent* | *1.002* | *1.003* | *0.23* | *73* | *24.76x* |
| *gen-unsafe-aa-distant* | *1.097* | *1.314* | *2.27* | *76* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.132* | *1.403* | *1.78* | *74* | *1.00x* |
| gen-unsafe | 1.152 | 1.363 | 2.07 | 74 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 0.9523, worst
cell 11.27% on `window-64x64-k1x9`, and 13 of 16 intervals cover 1.
The `sum-only` halves agree at 0.9983 on a worst cell of 0.47%
on `window-64x64-k1x9`, its interval covering 1. The in-situ term reads 1.0088,
1.0026, 1.0035, 1.0276 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9535, which
the correction amplifies by 1.02x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m17s, peak 107 MiB in use, 24 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.52 ms per call raw, 9.25 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9):** `mut-odo-vecdims` 0.044/0.057/0.095
`bq-scan-rem-gm-mulback` 0.095/0.097/0.073

**Across the halves:** 21 of the 49 arms are faster on this half and 28 slower,
at a geomean of 1.0158, from `mut-odo-vecdims-add-in-leaf` at 0.8237
to `mut-odo-vecdims-add-in-leaf-down` at 1.2260, with `list` itself at 1.0082.
**The baseline moved 0.82% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** `lib-stage2-short` leads at 0.020, **0.3291
of `mut-odo-vecdims` on 3 of 3 shapes**, a 67.1% margin against a 4.77% floor --
the widest property-2 break of any non-degenerate class this run, and by some
distance. Properties 1 and 3 hold. A window's runs are short and numerous, which
is the condition the short-body fill was written for, so the class
is the candidate's best case and reads like it.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one
strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *118* | *1.14x* |
| *canon-full-nosum* | *--* | *--* | *0.14* | *144* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.13* | *125* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| lib-stage2-u4 | 0.026 | 0.036 | 0.12 | 127 | 1.00x |
| lib-stage2-concat | 0.026 | 0.035 | 0.09 | 126 | 1.00x |
| lib-stage2-lean | 0.027 | 0.035 | 0.07 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.035 | 0.07 | 126 | 1.00x |
| lib-stage2-disp | 0.027 | 0.035 | 0.12 | 126 | 1.00x |
| lib-stage2 | 0.027 | 0.035 | 0.09 | 126 | 1.00x |
| lib-stage2-short | 0.027 | 0.035 | 0.10 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.035 | 0.11 | 126 | 1.00x |
| lib-stage1 | 0.029 | 0.035 | 0.07 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.030 | 0.033 | 0.09 | 126 | 1.00x |
| canon-vecdims | 0.032 | 0.035 | 0.09 | 126 | 1.00x |
| canon-memcpy-r2 | 0.032 | 0.035 | 0.09 | 126 | 1.00x |
| canon-full | 0.032 | 0.035 | 0.08 | 126 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.034* | *0.17* | *126* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.033 | 0.10 | 126 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.033* | *0.10* | *126* | *1.00x* |
| mut-odo-vecdims-add-in | 0.033 | 0.033 | 0.13 | 126 | 1.00x |
| mut-odo | 0.033 | 0.048 | 0.13 | 124 | 1.00x |
| *mut-odo-aa-adjacent* | *0.033* | *0.051* | *0.11* | *124* | *1.00x* |
| *mut-odo-aa-distant* | *0.033* | *0.049* | *0.14* | *124* | *1.00x* |
| bcast-set | 0.033 | 0.037 | 0.07 | 126 | 1.00x |
| mid-copy | 0.033 | 0.035 | 0.07 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.035 | 0.08 | 124 | 1.00x |
| *build-aa-distant* | *0.035* | *0.052* | *0.35* | *124* | *1.00x* |
| *build-aa-adjacent* | *0.037* | *0.050* | *0.32* | *124* | *1.00x* |
| build | 0.037 | 0.052 | 0.40 | 124 | 1.00x |
| libunord-stage1 | 0.043 | 0.063 | 0.17 | 122 | 2.01x |
| liblist-stage1 | 0.045 | 0.063 | 0.18 | 122 | 2.00x |
| libunord-stage2 | 0.047 | 0.064 | 0.21 | 122 | 2.01x |
| liblist-stage2 | 0.047 | 0.064 | 0.17 | 122 | 2.00x |
| mut-flat-gm | 0.073 | 0.074 | 0.12 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.082 | 0.083 | 0.12 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.085 | 0.088 | 0.07 | 114 | 1.14x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.091* | *0.093* | *0.06* | *113* | *1.04x* |
| bq-odo-gm-mulback | 0.091 | 0.093 | 0.06 | 113 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.091* | *0.093* | *0.06* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.092* | *0.096* | *0.06* | *112* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.095* | *0.06* | *112* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.096 | 0.08 | 112 | 1.04x |
| *bq-expand-aa-distant* | *0.095* | *0.100* | *0.06* | *112* | *1.14x* |
| *bq-expand-aa-adjacent* | *0.097* | *0.100* | *0.06* | *111* | *1.14x* |
| bq-expand | 0.097 | 0.100 | 0.08 | 111 | 1.14x |
| offtab-scan-rem | 0.130 | 0.136 | 0.08 | 108 | 2.00x |
| *gen-unsafe-aa-distant* | *0.952* | *1.920* | *2.22* | *68* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *0.970* | *1.918* | *0.58* | *68* | *1.00x* |
| gen-unsafe | 0.993 | 2.077 | 1.00 | 68 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 0.27 | 71 | 19.43x |
| *list-aa-adjacent* | *1.002* | *1.002* | *0.22* | *70* | *19.43x* |
| *list-aa-distant* | *1.002* | *1.010* | *0.23* | *71* | *19.43x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 0.9586, worst
cell 7.59% on `scaled-r5`, and 12 of 16 intervals cover 1. The `sum-only` halves
agree at 1.0019 on a worst cell of 0.35% on `scaled-rank1-m1`, its interval
covering 1. The in-situ term reads 1.0312, 1.0233, 1.0193, 1.0118 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 0.9596, which the correction amplifies by 1.05x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h14m17s, peak 121 MiB in use, 52 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.91 ms per call raw, 4.73 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1,
scaled-r5):** `mut-odo-vecdims` 0.028/0.033/0.033 `bq-scan-rem-gm-mulback`
0.091/0.092/0.096

**Across the halves:** 35 of the 49 arms are faster on this half and 14 slower,
at a geomean of 0.9882, from `mut-odo-vecdims-add-in-leaf` at 0.8564
to `mut-odo-vecdims-add-in-leaf-down` at 1.1273, with `list` itself at 0.9911.
**The baseline moved 0.89% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** the tightest break of the nine. `lib-stage2-u4` leads
at 0.026, **0.8815 of `mut-odo-vecdims` on 2 of 3 shapes at sign p 1**, an 11.9%
margin against a 4.14% floor -- outside it, but on a split sign test,
so the class ranks the candidate first without separating it. Properties 1 and 3
hold, `bq-expand` at 1.14x, the bottom of the range across the nine
and this class's own `m` of 1 and 2,000 showing through.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1
throughout: regime 2, which the library reaches by a route of its own,
and the population the rework's question needed --- extended this run from seven
views to eleven.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l`
1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 ---
NEW, and the first view in the suite with a canonical innermost extent of 4,
the branch the short-body fills take and which nothing, `check` included, had
exercised), `runs-5` (`l` 1800000, `sInner` 5 --- NEW, beside it), `runs-9` (`l`
1800000, `sInner` 9 --- the window probe's run), `runs-96` (`l` 1800000,
`sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- NEW,
and the dispatch threshold's own cell, `>= dispRun` firing exactly here),
`runs-512` (`l` 1799680, `sInner` 512 --- NEW, bracketing `dispRun` within
a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-65536` (`l`
1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000,
`sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l`
of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.51* | *51* | *1.15x* |
| *canon-full-nosum* | *--* | *--* | *0.62* | *76* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.45* | *57* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-short | 0.027 | 0.029 | 0.32 | 58 | 1.00x |
| lib-stage2-u4 | 0.028 | 0.030 | 0.33 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.028 | 0.030 | 0.32 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.030 | 0.30 | 58 | 1.00x |
| lib-stage2 | 0.028 | 0.031 | 0.31 | 58 | 1.00x |
| lib-stage2-lean | 0.028 | 0.031 | 0.32 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.029 | 0.031 | 0.15 | 58 | 1.00x |
| lib-stage2-disp | 0.029 | 0.038 | 0.32 | 58 | 1.00x |
| canon-vecdims | 0.031 | 0.062 | 0.47 | 58 | 1.00x |
| mid-copy | 0.033 | 0.062 | 0.33 | 58 | 1.00x |
| mut-odo-vecdims-add-in | 0.033 | 0.063 | 0.13 | 58 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.034* | *0.063* | *0.08* | *58* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.035 | 0.06 | 57 | 1.00x |
| canon-full | 0.034 | 0.086 | 0.51 | 58 | 1.00x |
| canon-memcpy-r2 | 0.034 | 0.088 | 0.46 | 58 | 1.00x |
| **mut-odo-vecdims** | **0.034** | 0.063 | 0.08 | 58 | 1.00x |
| *mut-odo-vecdims-aa* | *0.035* | *0.063* | *0.10* | *58* | *1.00x* |
| bcast-set | 0.037 | 0.067 | 0.33 | 58 | 1.00x |
| *mut-odo-aa-adjacent* | *0.047* | *0.158* | *0.36* | *57* | *1.00x* |
| build | 0.047 | 0.161 | 0.51 | 57 | 1.00x |
| *build-aa-adjacent* | *0.047* | *0.158* | *0.93* | *57* | *1.00x* |
| mut-odo | 0.047 | 0.163 | 0.26 | 57 | 1.00x |
| *build-aa-distant* | *0.048* | *0.148* | *0.83* | *57* | *1.00x* |
| *mut-odo-aa-distant* | *0.048* | *0.152* | *0.32* | *57* | *1.00x* |
| mut-flat-gm | 0.073 | 0.075 | 0.38 | 49 | 1.03x |
| bq-expand-gm-mulback | 0.083 | 0.088 | 0.53 | 47 | 1.15x |
| bq-mut-runs-gm-mulback | 0.084 | 0.089 | 0.51 | 47 | 1.03x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.088* | *0.093* | *0.56* | *47* | *1.04x* |
| bq-odo-gm-mulback | 0.088 | 0.093 | 0.56 | 47 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.089* | *0.093* | *0.04* | *47* | *1.04x* |
| liblist-stage2 | 0.094 | 1.140 | 0.57 | 55 | 1.21x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.094* | *0.100* | *0.54* | *46* | *1.03x* |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.100 | 0.53 | 46 | 1.03x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.095* | *0.101* | *0.04* | *46* | *1.03x* |
| libunord-stage2 | 0.095 | 1.137 | 0.54 | 55 | 1.21x |
| *bq-expand-aa-adjacent* | *0.096* | *0.101* | *0.57* | *45* | *1.15x* |
| bq-expand | 0.096 | 0.101 | 0.57 | 45 | 1.15x |
| *bq-expand-aa-distant* | *0.097* | *0.102* | *0.03* | *45* | *1.15x* |
| lib-stage1 | 0.136 | 1.315 | 0.80 | 53 | 1.28x |
| offtab-scan-rem | 0.136 | 0.148 | 0.72 | 41 | 2.00x |
| liblist-stage1 | 0.137 | 1.349 | 0.55 | 53 | 1.28x |
| lib-stage2-concat | 0.137 | 1.331 | 0.47 | 52 | 1.31x |
| libunord-stage1 | 0.138 | 1.347 | 0.56 | 53 | 1.28x |
| *gen-unsafe-aa-adjacent* | *0.696* | *1.081* | *3.40* | *21* | *1.00x* |
| gen-unsafe | 0.710 | 1.090 | 2.87 | 21 | 1.00x |
| *gen-unsafe-aa-distant* | *0.715* | *1.071* | *2.27* | *20* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 2.52 | 17 | 19.43x |
| *list-aa-distant* | *1.016* | *1.032* | *1.91* | *17* | *19.43x* |
| *list-aa-adjacent* | *1.033* | *1.050* | *0.28* | *17* | *19.43x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0326, worst cell
4.96% on `runs-r3-48x30`, and 10 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9999 on a worst cell of 0.47% on `runs-2`, its interval covering 1.
The in-situ term reads 1.0328, 1.0253, 1.0291, 1.0232 of `sum-only` as medians,
on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 1.0314, which the correction amplifies by 1.04x --- quote both wherever
that is past 1.5.

**Provenance:** elapsed 0h52m30s, peak 494 MiB in use, 208 MiB max residency;
the reader reads 55 benchmarks over 11 shapes of the runs class. Anchor:
`runs-2`, `list` at 39.1 ms per call raw, 38 ms net.

**Per shape, in the lead's order (runs-2, runs-3, runs-4, runs-5, runs-9,
runs-96, runs-256, runs-512, runs-1024, runs-65536, runs-r3-48x30):**
`mut-odo-vecdims`
0.063/0.052/0.046/0.043/0.034/0.029/0.028/0.028/0.028/0.027/0.030
`bq-scan-rem-gm-mulback`
0.100/0.099/0.098/0.096/0.093/0.093/0.092/0.092/0.093/0.093/0.094

**Across the halves:** 15 of the 49 arms are faster on this half and 34 slower,
at a geomean of 0.9986, from `mut-odo-vecdims-add-in-leaf` at 0.8393
to `mut-odo-vecdims-add-in-leaf-down` at 1.1544, with `list` itself at 1.0114.
**The baseline moved 1.14% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** this is the class the run was extended for
and it answers three registrations at once. `lib-stage2-short` leads at 0.027,
**0.7647 of `mut-odo-vecdims` on 7 of 11 shapes**, 23.5% against a 3.26% floor.
Properties 1 and 3 hold. **The crossover moved**: `lib-stage2` / `lib-stage1`
runs 0.0227, 0.0274, 0.0397, 0.0437, 0.0834, 0.5202, 0.7679, 0.8170, 0.9254,
1.1485 and 1.0364 across the eleven lengths, so the branch is the better route
through `runs-1024` where Run 21 had it behind from `runs-96` up by factors
of 2.9 to 6.5. **And that kills the dispatch**: `lib-stage2-disp` is 6.65%
behind stage two at `runs-1024`, past this floor, because `dispRun` is cut
to 256 and the bracket moved out from under it; at `runs-256` and `runs-512`,
the two lengths nothing had read, it is 33.2% and 20.9% behind. The four new
views earn their place -- `runs-4` and `runs-5` exercise the short bodies' one
branch that nothing, `check` included, had reached.



## Provenance

What this run's figures have to be read against, and it is a section
of this file because a run replaces every word of it. What does NOT move
with a run --- the delta chain that says which shape set and roster each run
measured, and the list of what a run replaces outside this file --- is [README's
own Provenance][prov].

**Run 22's halves differ in the compiler, as Run 19's, Run 20's and Run 21's
did, and in nothing else a freeze can see.** One source, `Main.hs` at `0add4f4`,
and one shim, `align-as.py` at `c57e5c4`, built twice: the basis by ghc-9.12.4,
the default on PATH here, and the control by the in-tree stage1 of the GHC
checkout at `d415f38a75`, GHC 10.1.20260803, through `cabal.project.ghead`. Both
carry `-fspec-constr -fobject-determinism`, the max-skip shim
with its look-through and `LOOP_NOOVERLAP` unset, and both ran
under `WILDLOG=1 SATURATE=1`. `cabal.project.ghead`'s freeze resolves the same
criterion 1.6.5.0, criterion-measurement 0.2.5.0 and vector 0.13.2.0 at the one
index-state the released freezes hold, 2026-07-25T13:22:10Z, so the plans differ
in the boot libraries and in nothing else. What the pair prices is a consumer's
build on GHC HEAD, library code recompiled included.

**The sequence was launched once and did NOT run to the end in one window, which
no run here has had to say before.** Eighteen of the twenty processes ran
unbroken from 2026-08-31T01:57:43 to 09:53:49 --- both main sets and both halves
of `rev`, `revsome`, `bcast`, `bcastmid`, `reshape1`, `slice`, `window`
and `scaled`. The machine was then wanted by its owner, so the sequence
was stopped BY HAND at the `scaled`/`runs` boundary, three seconds
into `run22-ghead-runs`, which had written a zero-byte log and no JSON; nothing
was truncated and nothing was salvaged. The two `runs` processes were re-driven
at 16:41:21 to 18:26:27, on a box the driver measured at 0.6% non-idle before
it started, under the same launch line and with the same four per-process
assertions the sequence applies --- exit status, bench count read
from the binary, one `@@saturate` line, `@@wild` stamps present. **What makes
the twenty one run rather than two is TWO things and the chapter names only
the first.** The procedure's own warrant is that one process per population
is what makes more than one window harmless, each carrying its own controls
and its own three gates, neither inherited nor lent --- which this run
satisfies, and which is why post-run step 3's *a pair read across two windows
is not a pair* is met too, BOTH `runs` halves having been re-driven together
rather than a clean one left beside an exposed twin. The evidence on top
of it is the plateau gate: every process asserts its preamble victim inside
**19.8075 to 20.3228 ms/iter, a 2.60% spread** against a 5% band, the two late
ones among them, so the second window measured in the state the first did.
No population was rerun for an intrusion, no gate failed, and post-run step 3
is owed nothing. A session comparing elapsed times against this run's wall-clock
log must read the two `runs` processes as their own window.

**The pair's own identity, transcribed before its note goes with it.** The two
binaries are `run22-g912`, md5 `9bac6d77a913f139171430874f99b985`,
and `run22-ghead`, md5 `7a86094800e76ddd6e0ee31b4825761e`, with `.text`
of 20512965 and 20657983 bytes --- 24576 and 20480 bytes above their Run 21
counterparts. Both bake `-with-rtsopts=-A32m -I0 -T -M8G`, read back
by `+RTS --info` rather than by `strings`, and both carry the per-sample
instrument and the saturating preamble, one `@@wild` and one `@@saturate` marker
apiece. The tree at launch was `bd8493c` with four untracked scratch paths
and nothing modified. The regime was confirmed in both binaries by `diag` before
the hours were spent: `baseOffsetsScan` at 2408930 bytes against
`baseOffsetsMut`'s 2408530 on `vgg-14-c512` on the basis, and 2408978 against
2408530 on the control, where plain -O1 separates the two tenfold.

**The roster and the source both moved, which is this run's one departure
from Run 21's inputs**, and the fills say how far. `Main.hs` went from `70ef2de`
to `0add4f4` over eight commits, 456 lines added and 28 removed, and the shim
from `40f7a37` to `c57e5c4` by one commit that adds `LOOP_NOOVERLAP` off
by default, which neither half sets. Six timed arms landed and none left --- 49
arms to 55, all 49 in common --- and the `runs` class went from seven views
to eleven, so `--list` reads 1320 against Run 21's 1176 and `classes --list`
2035 over 37 views against 1617 over 33. No tracked address survives between
the two runs' basis binaries and none moved by a constant: `run21-g912` held
its six-copy group at `[0, 0, 24, 0, 0, 8]` and `run22-g912` holds one
at `[0, 0, 24, 0, 0, 24]`, five of the six mod-64 offsets unchanged
and the sixth --- `fbCanonVecdims`, named off a `-g3` twin at post-run step 0
--- moved from 8 to 24. **The basis half also gained four straddling self-loops
where Run 21 had none**, 158 loops against 135 and 80 at offset 0 against 71;
three are 63-byte bodies the twin cannot name, and the fourth, 6 bytes at offset
60, is byte-identical in the twin at the same address and lies in `fillStage2`.
No md5 comparison against Run 21 is owed and none was taken: the roster moved
and seven arms' code with it.

anchors read **5.98 us** on `cnn-slice-c32`, **3.07 ms** on `cifar-L2-16-c64-k3`
and **37.94 ms** on `stretch-wide-2xM`, all three net of the forcing term
and all three the basis half's; raw they read 6.15 us, 3.16 ms and 39.04 ms.
**The control half's three are 5.94 us, 3.05 ms and 37.18 ms net**, so the two
halves' baselines sit within 0.7%, 0.7% and 2.0% of each other --- which
is the same measurement the 0.7% bar above reads as a geomean, and the reason
that bar refuses this pair: `list` moves 0.81% between the halves over the whole
shape set.

| shape | `l` | `list`, per call | net | HEAD, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.15 us | 5.98 us | 5.94 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.16 ms | 3.07 ms | 3.05 ms |
| `stretch-wide-2xM` | 1800000 | 39.0 ms | 37.9 ms | 37.2 ms |

**Each stride class carries an anchor of its own, beside its table, and all nine
are `list` on one of that class's shapes, raw and net.** The main set's three
guard a baseline that moves for every population at once; a class anchor guards
one that could move for that mechanism alone, which is the case a table
of ratios hides completely. The `runs` anchor is `runs-2` at 39.1 ms raw and 38
ms net, the class having eleven shapes this run where it had seven. Read a class
anchor against the same class's anchor in an earlier run and against nothing
else, and against that class's own floor rather than the main set's.

**The correction is invertible, so pre-correction figures stay comparable.**
The `sum-only` term subtracted from every cell is published per shape,
and the two `sum-only` halves agree at **1.0003** on the basis and **1.0000**
on the control, both intervals covering 1 --- so a reader wanting a raw figure
can recover it, and a reader comparing against a run that corrected differently
can say by how much. The in-situ check, which is a different instrument
and not the correction, reads 1.0256, 1.0225, 1.0371 and 1.0754 on the basis
and 1.0266, 1.0225, 1.0278 and 1.0722 on the control.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

The pair was Run 21's again, `run22-g912` against `run22-ghead`, one source
and one shim, both under `WILDLOG=1 SATURATE=1`, over an extended roster: 55
timed arms, 1320 main-set benches and 2035 class benches over 37 views in nine
classes. Five questions were registered on 2026-08-30 and amended at `ce8f5f7`
with a prediction and a kill condition each; **two held, one split and two
killed**, and unlike Run 21's one-sided set, whose five failed for one shared
mistake, these failed for one shared FACT: `fillStage2` got fast enough between
the two runs to move everything registered around it. (1) *The fill in time,
over every population.* **HELD, and by a wider margin than it dared.**
`lib-stage2` against `lib-stage1` was predicted inside **0.78 to 1.08**
on the six populations carrying Run 21's 2.43-to-4.54 regression, killed by any
regime-3 population reading the branch behind by more than a tenth. It reads
**0.7400** on the main set, 0.8902 on `rev`, 1.0262 on `revsome`, 1.0344
on `slice`, 0.9849 on `scaled` and 0.8110 on `window`; five land inside
the band, the main set below it, and nothing is within six points of the kill
condition. `slice`, singled out as the one still behind past its floor
and predicted inside 1.05, reads 1.0344. The broadcast exception held as stated,
`bcast` and `bcastmid` being bandwidth-bound and unreached by an unboxing. (2)
*The three fill candidates in time.* **KILLED, all three of them, and it
is the registration that shows what a counted reading is worth.**
`lib-stage2-short` was predicted about 0.50 of `lib-stage2` at `runs-2`, 0.59
at `runs-3`, with `runs-4` and `runs-5` counted at 0.5528 and 0.6099; in time
it reads **0.8066, 0.9678, 0.8311 and 0.9407** --- right in sign, a third
to a sixth of the size --- and it is **KILLED** besides: on `stretch-inner1`
it reads 1.0308, 3.08% behind against the main set's 2.12% floor, where
the counted work puts it at 0.999997. Its four `runs` cells above 1 are inside
that class's floor, which is what a scan stopping at `runs` sees.
`lib-stage2-u4` was predicted 0.83 to 0.85 at the long runs and reads 0.9759,
0.9916 and 0.9821 at `runs-65536`, `-1024` and `-512`: ahead, but never past
the 3.26% floor, which is its own kill condition. **KILLED.** `lib-stage2-lean`
was predicted at or below `lib-stage2` everywhere and past a floor on exactly
three main-set shapes; two are its cleanest confirmation, `cnn-L1-6x6-c1`
at **0.8771** and `cnn-slice-c32` at **0.8565**, and the third inverts ---
`stretch-inner1` reads **1.0617**, behind by 6.2% past the floor, where
the sweep it was registered off put it 21 points ahead. **KILLED** ---
and the disagreement is that sweep's against the clock, not this run's:
this run's own counted work reads the arm at 1.0000 on that shape and agrees
with the clock. (3) *The dispatch.* **KILLED, on both halves, and the reason
is registration 1.** `lib-stage2-disp` reproduces the filtered sweep
at the seven lengths that sweep read --- 0.0227, 0.0273, 0.0834, 0.5193, 0.9870,
1.0083 and 1.0102 against stage one, where 0.0283, 0.0312, 0.0951, 0.6190,
1.0029, 1.0096 and 1.0075 were registered --- but its kill condition is being
behind the better route past the floor at any of those lengths,
and at `runs-1024` the better route is now stage two and the dispatch
is **6.65%** behind it against a 3.26% floor, **4.22%** against 3.33%
on the control. `dispRun` was cut to 256 when the crossover sat between `runs-9`
and `runs-96`; the crossover now sits between `runs-1024` and `runs-65536`,
so the threshold fires the slice route three lengths too early.
**Its control-half prediction is the one thing here that landed exactly** ---
behind `lib-stage2` at `runs-1024` by *about four points*, read 4.22% --- while
its reason is refuted: it expected the basis ahead there because 9.12's
crossover sat earlier than HEAD's, and both halves put the crossover in the same
place, so the failure is not a compiler difference but the fill improving
on both. (4) *The unordered entry point.* **HELD, and it is the one registration
that neither moved nor surprised**, because it was evaluated rather
than predicted. `probe-oneblock.py` had said stage two's one-block test fires
on ten of the 37 rostered class views --- every view of `rev`, `revsome`
and `reshape1` --- and stage one's on none. `libunord-stage2` against
`liblist-stage2` reads **0.0197, 0.0081 and 0.0064** on those three classes
and 0.9867, 1.0013, 1.0239, 1.0256, 1.0185 and 0.9999 on the six where neither
fires, every one inside that class's floor; `libunord-stage1` tracks
`liblist-stage1` the same way. Neither kill condition fired. **What the run adds
is the main set, which the registration left unpredicted and the roster pass
answered**: both tests fire there, and at full budget two cells sink below
the shared forcing pass on the basis and seventeen on the control. (5)
*The vecdims family's ordering.* **SPLIT on one population of twenty.** `-u2`
was predicted ahead of `-down` on the main set and every class past each floor;
on the basis it is, in all ten, from **0.6686** on `reshape1` to 0.8522
on `scaled`, the main set at **0.7938 at 23 of 24, sign p 3e-06** --- so Run
21's 5.6% and 6.7% the other way are reversed and the in-process re-take
of 2026-08-30 was reading the change and not a displacement. On the control
it is ahead in nine of ten. The tenth is `bcast`, where `-down` leads
at **1.1306 on 0 of 3 shapes**, 13% past that class's own control floor
of 2.79%, which is the kill condition fired on one cell of twenty. `-u2` against
`-u2-down` was predicted a tie inside the floor and is one, 1.0004 and 1.0091.
**What the set is worth**: all five were decidable, none came back a null,
and the two that died plus the one that split all moved for the same reason ---
`fillStage2` is now fast enough that a threshold, an unrolling and a family
ordering chosen around its old cost are each mis-cut. The registration
a horde-ad consumer should take from this is not any one of the five: it
is that the branch's driver has stopped being the regression this benchmark
was built to catch.
