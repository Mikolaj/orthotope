# Run 23 (SpecConstr)

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

**Run 23 (SpecConstr), and what moving the shim's pads off the execution path
is worth at full budget over every population: four percent of the instructions
and five percent of the time on the branch's fill and every arm that shares
its loop, nothing on the arms whose fill carried no pad, and no verdict of Run
22's re-decided by the switch --- one by the repetition.** Criterion,
**`--ghc-options=-fspec-constr`**; Run 22's regime, roster, shape set and basis
recipe, and **what moved is the shim's environment on one half and nothing
else**: 1320 benches, 55 timed arms over 24 main-set shapes, and 2035 more
over 37 class views in **nine** classes, Run 22's roster exactly, nothing landed
and nothing left. **The basis is `run23-g912`**, Run 22's basis recipe built
again --- ghc-9.12.4 with `-fobject-determinism`, the max-skip shim
with its look-through, the per-sample instrument and the saturating preamble ---
from a source moved by one comment line and a shim moved by one commit that adds
a switch this half does not set, **and it is Run 22's basis binary byte
for byte**, md5 `9bac6d77a913f139171430874f99b985`. **The other half
is `run23-spot`**, the same recipe with `LOOP_DEADSPOT=1` in front
of `align-as.py`, so that every pad the shim emits sits after an unconditional
`jmp` where no path executes it and the containment test orders the heads
of a group instead of skipping one; md5 `7d0ba79ed030bdcf40479b7efd4d5fa0`,
`.text` 20525253 against 20512965 bytes. One compiler on both halves, the first
pair since Run 17 whose halves share one, so nothing here is a compiler reading
and no boot library differs; both under `WILDLOG=1 SATURATE=1`; `Main.hs`
at `125534d`, `align-as.py` at `38bb3bb`, the tree at launch `c9bf086`
with seven untracked scratch paths and nothing modified. The same desktop, Zen
3, a Ryzen 7 5800X, and the same BIOS Run 18 re-baselined onto. The two main
processes read *1h53m48s* and *1h53m47s*, at *340 MiB* in use and *126 MiB* max
residency on the basis against *341 MiB* and *126 MiB* on the dead-spot half.

**The basis half IS a repetition, the exact one this file has asked for since
Run 19: one binary, Run 22's, timed again two evenings later over every
population.** Over the 23 main-set shapes that exclude `stretch-inner1`, **44
of the 49 arms read within 1% of their Run 22 geomean**, and the five outside
are the two `libunord` arms --- degenerate, a cell that is its own forcing term
moving a hundredfold between evenings --- and three arms
of the placement-exposed families, `gen-unsafe-aa-adjacent` at 1.0208,
`build-aa-adjacent` at 1.0159 and `mut-odo` at 1.0101; `list` itself reads
0.9962 over 24 with a per-shape scatter of 0.983 to 1.019, and the counted work
reproduces on all 49 arms to four figures, 1.0000 apiece. With `stretch-inner1`
in, the canonicalizing arms read 0.81 to 0.92 of Run 22 --- a ratio of nothing,
that cell sitting a few nanoseconds above the forcing pass on both evenings
and on neither side of it reliably. Per class the same binary reads geomeans
over its arms of 0.9989 on `rev`, 1.0076 on `revsome`, 0.9997 on `bcast`, 1.0032
on `bcastmid`, 1.0015 on `slice`, 0.9948 on `window`, 0.9874 on `scaled`
and 1.0006 on `runs` against Run 22's processes, with `list` inside 0.6%
on every one, and 0.9084 on `reshape1`, where the same degeneracy sits on nine
arms. **So this box's day-to-day drift, for one binary, is under a point on most
arms and about 2% at the worst non-degenerate one**, which is the band every
cross-run main-set geomean below is read against and a third narrower than Run
11's 3.3%; a single class cell moves further, as the `runs` block's long-run
cells show. Both halves reproduce task 6's probe as well, being its two
binaries: the basis against `probe-ds-off-main.json` reads 43 of 49 arms within
1% and `list` 0.9913 over those 23 shapes, the dead-spot half against
`probe-ds-on-main.json` 40 of 49 and `list` 0.9890.

**What holds the build to something is the repetition and two readings
that survive a relink.** The gate's machine check reads **-0.44%** on `list`'s
net against the fingerprint Run 22 kept, over 24 of 24 shapes, worst
`stretch-r5-8x432` -1.58% and none past 5%; the run's own main-set process reads
the same comparison at **-0.40%**, worst `conv1d-24` +1.86% --- two readings
against the SAME kept fingerprint, both inside 3%, so the box measures as it did
and no absolute is re-baselined. Each half's own sixteen A/A pairs give
it a floor, and the counted work, taken over every population on both halves,
is what separates a pad the loop executed from a slot the loop landed
in throughout what follows.

**The manifest's one surviving claim held on both halves, and the ladder
is unmoved on a repetition.** Claim 1's four registered links all hold
on the basis: `mut-odo-vecdims` / `mut-flat-gm` **0.6521** at 20 of 24 and sign
p 0.0015, `mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9180 at 23 of 24,
`bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9133 at 20 of 24,
and `bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9130 at 18 of 24 --- 4
of 4, a sixth clean sweep running, each within 0.0073 of Run 22's reading
on this same binary --- and on the dead-spot half at 0.6559, 0.9161, 0.9192
and 0.9199, no link a point from the basis's, six arms none of whose fills
carried a pad.

**What the dead-spot form is worth, and the counted work says it is the pads.**
Read as `--compare` prints it, basis over dead-spot, the nine arms task 6 named
faster under the form read **1.0566** on `lib-stage2`, 1.0560
on `lib-stage2-concat`, 1.0546 on `lib-stage2-disp`, 1.0524
on `lib-stage2-lean`, 1.0533 on `-add-in-leaf-u2`, 1.0514
on `-add-in-leaf-u2-down`, 1.0497 on `lib-stage1`, 1.0243 on `lib-stage2-short`
and **1.1956** on `-add-in-leaf-down`, over the 23 shapes that exclude
`stretch-inner1`, the basis faster on 2 to 10 of them --- and their reciprocals
sit within a point of the nine figures task 6 published off the same two
binaries, 0.9464 against 0.9452 on `lib-stage2` down to 0.8364 against 0.8328
on `-add-in-leaf-down`. **Registration 1 HELD.** The instrument that names
the cause is the counted work: those nine arms execute **4.0% fewer
instructions** on the dead-spot half over the same 23 shapes --- count ratios,
basis over dead-spot, of 1.0417 to 1.0418 on `lib-stage2`, `-concat`, `-disp`
and `-lean`, 1.0407 on `lib-stage1`, 1.0410 and 1.0413 on the two `-u2` arms ---
2.1% fewer on `lib-stage2-short` and **8.1%** fewer on `-add-in-leaf-down`,
so most of each arm's win is the pad instructions themselves and the rest, 0.3
to 1.4% of time over counts on the fills and 9.9% on `-add-in-leaf-down`,
is what removing them does to the loop's placement. Per shape the pad's share
is the run's: 5.2% of `lib-stage2`'s instructions on `alexnet-L1-55-c3-k11`,
4.3% on `stretch-tab7MB`, 1.7% on `cnn-slice-c32` and none on `stretch-inner1`,
where the view canonicalizes to a slice and the fill never runs. **The flatness
control is flat**: `lib-stage2-u4`, the one `lib-stage2` sibling whose fill
carried no pad, reads 1.0043 in time at a count ratio of 1.0000 exactly,
and `bq-expand` 0.9990, `mut-odo-vecdims` 0.9940 and `list` 1.0040, every one
inside either floor, at count ratios of 1.0021, 1.0000 and 1.0000 ---
`bq-expand`'s two thousandths of instructions being a pad of its own the form
also removed, worth nothing in time. **Registration 2 HELD.**

**The placement-exposed workers move as far as the fills and their counts do
not move at all --- which is what registration 5 was written to read, and what
it read is a split.** Over the same 23 shapes `build` reads 1.0610 at 1 of 23,
`gen-unsafe` 1.0660 at 4 of 23 and `mut-odo` 0.9999 at 12 of 23 across
the halves, at count ratios of **1.0000** on all three, so nothing in them
executed a pad and every point they moved is where their bytes landed ---
the dead-spot form having moved every address in the binary, as `--library`'s
4.1% same-offset figure says. Their twins moved in their bases' directions
and not to their figures: `build-aa-distant` 1.0835 and `-aa-adjacent` 1.0884
beside `build`'s 1.0610, `gen-unsafe-aa-distant` 1.0874 and `-aa-adjacent`
1.1123 beside 1.0660, `mut-odo-aa-distant` 0.9939 and `-aa-adjacent` 0.9962
beside 0.9999 --- spreads of up to five points within a family, which
is the term a slot owns and its arm does not. The kill condition, a count
that moved, did not fire; what did not reproduce is the size: task 6 read
`gen-unsafe` at 0.8892 and `mut-odo` at 0.9775 across these same two binaries
where this run reads 0.9381 and 1.0001, 4.9 and 2.3 points apart --- the first
past both floors, the second past the basis's 2.03% --- while `build` reproduced
at 0.9425 against 0.9389. **HELD on its kill condition and not
on its prediction, two of three figures having failed to reproduce**,
and the lesson is the twins' own: a placement term belongs to an evening's slot,
and a repetition on one binary moves these three arms by a point or two
with the layout held still.

**`build` against `mut-odo` answers differently on the two halves, exactly
as registered, and the residue that has stood since Run 10 is now bracketed.**
The pair reads **0.9998 at 11 of 24, sign p 0.84** on the basis --- a tie, where
task 6 read 0.9986 on the same binary and Run 22 1.0125 --- and **0.9449 at 20
of 24, p 0.0015** on the dead-spot half, task 6's 0.9558, both sign counts
on their own sides of 12 and the gate having read the same two signs on five
benches before the sequence ran, 1.0329 and 1.0206 against 0.9626 and 0.9549.
**Registration 4 HELD.** Both tracked loops sit at offset 0 on both halves,
in twin and timed binary alike, and both arms' instruction counts are equal
between the halves to four figures, so what opens a five-and-a-half-point gap
between two copies of one worker is neither their code nor their heads'
cache-line offset but what the pads around them did to the rest of the binary
--- the 3% [the open list][open] has asked about is not on today's basis,
and the form that removes every executed pad puts a larger gap in its place.

**The classes split registration 3 and kill its sharper half.** The nine arms
lead --- the dead-spot half faster --- on `rev`, `revsome`, `slice`, `window`
and `scaled`, by 1.4% to 22%; on `bcast` five of the nine sit inside either
floor, `lib-stage2` at 0.9918 to `lib-stage2-concat` at 1.0016, at count ratios
of 1.0000 --- a broadcast re-reads one element per run, its fill's pad is never
executed and there is nothing for the form to remove --- while `lib-stage1`
and the leaf arms move 17% to 40%; on `bcastmid` the fills sit within a point
and the leaf arms move; on `runs` `lib-stage1` ties at 0.9995 and the rest move
0.7% to 15%; and on `reshape1` the `lib-stage2` family is degenerate on one
or two of its four shapes and the two `-u2` leaf arms are SLOWER
on the dead-spot half, 0.9784 and 0.9637 on 4 of 4 shapes, at count ratios
of 1.0000 --- past the basis half's 3.09% floor and inside the dead-spot half's
own 10.75%. **Its second half is dead outright**: the margin on `runs`
was predicted to shrink monotonically with the run length, and `lib-stage2`
reads 0.9077, 0.9863, 0.8819, 0.9650, 0.9335, 0.9871, 0.9800, 0.9637, 0.9841
and 0.8954 dead-spot over basis from `runs-2` to `runs-65536`, widest
at `runs-4` and second widest at the longest run. **KILLED** in its second half;
in its first, led outright on five classes, tied inside a floor on three,
and reversed on one class's two arms against the narrower of that class's two
floors --- which, judged against the wider of the two as [README's floor
section][floor] rules since 2026-09-02, is a tie and not a kill: the first half
is a SPLIT.

**`mut-odo` is the one arm the dead-spot form costs, and it costs it
in the classes.** On the main set the arm reads 1.0020 across the halves
over all 24 shapes; in the classes the basis is faster on it by 2.3% on `rev`,
3.5% on `revsome`, 6.5% on `window` and 3.6% on `scaled`, on 3 of 3 shapes each,
and by 1.0% on `reshape1` --- past the basis's floor on `window` and `scaled`,
past the dead-spot half's own on `revsome` and `scaled`, its adjacent twin
moving with it on `rev`, `window` and `scaled`. Its loop sits at offset 0
on both halves and its count ratio is 1.0000 in every population, so this
is a placement term the main set reads as 1.0020 and the classes as a cost,
which is the one thing a class comparison exists to see. The cross-class
aggregate, off the nine `--block --compare` lines: 441 arm-comparisons, nine
degenerate and not voted, **116 with the basis faster and 316 the dead-spot
half**, the nine geomeans 0.9985 on `reshape1` to 1.0351 on `bcast`, the high
extreme `-add-in-leaf-down` in eight of the nine and the low extreme `mut-odo`
in three.

**Run 22's five verdicts under the dead-spot form, which registration 6 owed
by name --- one does not hold, and it is the repetition and not the switch
that unseats it.** (1) `lib-stage2` against `lib-stage1` stands: `slice`,
the population Run 22 read the branch behind past its floor, reads 1.0409
on the basis and 1.0120 on the dead-spot half against a kill at 1.10,
and the main set 0.9547 and 0.9484 over the 23 readable shapes --- Run 22's
0.7400 over 24 having carried a ratio of nothing on `stretch-inner1`, which
this run's same binary reads at 0.6193 over 24 and 0.9547 over 23. (2) The three
candidates' kills are single cells and do not survive the repetition:
`lib-stage2-u4` was killed for not clearing the `runs` floor at any long length
and on the same binary now reads **0.9530 at `runs-65536` and 0.9581
at `runs-512`**, past the 3.45% floor at both, so its kill does NOT hold
on the basis, while on the dead-spot half it reads 0.9848, 0.9925 and 0.9941
and the kill stands; `lib-stage2-short`'s killing cell, `stretch-inner1`
at 1.0308, is unreadable this run, its base being its own forcing term there,
and over the other 23 shapes the arm is behind past the floor
on `stretch-coprime-r7` at 1.039 on the basis and nowhere on the dead-spot half,
so that kill holds on one half by a different cell and not on the other;
`lib-stage2-lean`'s killing cell was the same one and is likewise unreadable,
its 23 others putting it behind nowhere past the floor on the basis and behind
past it on `cifar-L2-16-c64-k3` at 1.036 on the dead-spot half --- the reverse
split. So of the three kills, `-u4`'s falls on the basis, and `-short`'s
and `-lean`'s each stand on one half by a cell Run 22 did not name and fall
on the other; none of the three stands on both halves as Run 22 read it. (3)
The dispatch stays killed on both halves, 5.75% and 6.24% behind stage two
at `runs-1024` against floors of 3.45% and 3.46%. (4) The unordered entry point
stands: degenerate on `rev`, `revsome` and `reshape1` on both halves ---
`libunord-stage2` against `liblist-stage2` reading 0.0157 and 0.0200, 0.0097
and 0.0071, and 0.0025 on the basis with the dead-spot half's `reshape1`
unreadable --- and inside every class's floor on the six where neither test
fires. (5) The vecdims ordering stands and is now unconditional: `-u2` leads
`-down` in all ten populations on BOTH halves, 0.6564 to 0.8484 on the basis
and 0.8365 to 0.9463 on the dead-spot half, `scaled`, which the registration
predicted would go, reading 0.9295 at seven points past its 2.46%, and `bcast`,
where Run 22's HEAD half split, 0.9463 at an eighth of a point past its 5.25%
--- the form takes eight to nineteen points off `-down`'s deficit everywhere,
8.1 on `scaled` to 19.2 on `reshape1`, and reverses it nowhere.
**So registration 6 is KILLED by its own terms**, (2) having come out
differently, and what the write-up owed is named: under the dead-spot form
no verdict of Run 22's flips; under a repetition of Run 22's own binary,
`lib-stage2-u4`'s kill does.

**Every one of the twenty processes gated clean**, `--selftest` and both `--aa`
gates, so no time column here is uncorrected. **This run's floor is 2.03%
on the basis half and 2.80% on the control, the dead-spot half**, against Run
22's 2.12% and 1.08% --- the basis figure read twice on one binary two evenings
apart, moving a twentieth, where Run 19's repetition of Run 18's moved a factor
of 1.7. The pair carrying it is `build-aa-distant` on the basis for the second
run running and `gen-unsafe-aa-adjacent` on the dead-spot half, and the worst
A/A cell of either main set is **15.51%** on `cifar-L2-16-c64-k3` on the basis
against **15.18%** on `alexnet-L1-55-c3-k11` on the other, where Run 22 read
19.44% and 14.40%. Restricted to the six pairs that carry back to Run 10 the two
read **0.39%** and **0.40%**, against Run 22's 0.37% and 0.51%. **Which
of the two a margin is judged against depends on what it compares**: an arm
against its own duplicate against 2.03% and 2.80%; two different arms against
the six-pair figures. Neither is judged against the predecessor's --- the fourth
consecutive run of one recipe on one box whose floor moved for no isolated
reason, 1.51%, 2.92%, 2.12%, 2.03%, and the first whose movement a repetition
can bound.

**The two halves' cells resolve alike.** `CI%` --- the median half-width
of a cell's own fit --- runs a geomean of **1.01** on the basis against
the dead-spot half across the roster, **31 arms wider here and 24 narrower**,
where Run 22 read 1.01 at 28 and 27: an even split for the second run running,
on two halves that differ in layout alone as Run 22's differed in compiler.
It remains a different quantity from the floor: sampling error inside one bench
against agreement between two placements of one strategy.

**The sequence ran in ONE window, and one thing happened on the machine during
it, disclosed rather than rerun.** Twenty processes from 23:55:28 to 09:35:21,
every one exiting 0 at its roster's count, the dead-spot half first throughout;
the plateau gate asserts every preamble victim inside **19.7302 to 20.6446
ms/iter, a 4.63% spread** against the 5% band, where Run 22 read 2.60%.
At 00:42:01, forty-seven minutes into `run23-spot-main`, a Claude Code update
installed itself. The per-sample instrument's foreign-CPU column
over that process's 1320 benches puts 2 at or above 0.25 ---
`cnn-L1-6x6-c1/gen-unsafe` at 0.74 and its adjacent twin at 0.71, the process's
first shape at 23:55, ninety seconds after the gate's last process ended, when
this session's own reading of the gate and its launch checks were the only other
thing running, and nothing to do with the update --- and nothing past 0.25 near
00:42; the basis main set peaks at 0.18. Post-run step 3 would have rerun both
main sets and was declined by the person who asked for the run, so
that the machine could be handed back; the two cells it touches are in a row
the registration already reads as not reproducing for reasons of its own.

**The cells that sink below the shared forcing pass are one compiler's this run,
and the dead-spot half sinks five times as many.** On the basis three cells sink
--- `lib-stage2-short` on `stretch-inner1`, and both `libunord` arms
on `stretch-inner256` --- so three rows are geomeans over 23 of 24.
On the dead-spot half fifteen sink across eleven rows: the three `canon-*` arms
and all six `lib-stage2*` arms on `stretch-inner1`, and the two `libunord` arms
there and on `stretch-pow2stride` and `alexnet-L1-55-c3-k11`, so nine rows cover
23 shapes and two cover 21. Run 22 attributed its control's seventeen to HEAD;
this pair says a cheaper layout does it alone, the canonicalizing arms'
one-slice cell coming in under the forcing pass by a few nanoseconds once their
pads are gone. It is a structural fact about the table and not a defect in it,
and it is why every registration figure here is taken over the 23 shapes
that exclude `stretch-inner1`.

**The counted work covers every population, and this run it reads two things
at once: the pads, and the instrument's own reproducibility.** Twenty sweeps,
both halves over all ten populations, 165, 220, 605 or 1320 cells apiece
and no cell perf refused anywhere in the twenty files. **Across the halves every
class reads as the main set does**: the padded fills' count ratios, basis
over dead-spot, run 1.0417 to 1.0471 on `rev`, `revsome`, `slice` and `scaled`,
1.0577 on `runs`, 1.0221 to 1.0398 on `window`, 1.0159 on `reshape1` and 1.0061
on `bcastmid`, where only `lib-stage1` and the `-u2` arms read 1.0483,
and on `bcast` 1.0000 for the `lib-stage2` family --- `lib-stage2`, `-short`
and `-u4`, their times inside the floor, a broadcast's fill never executing
the pad the form removed --- though `lib-stage1` and the two `-u2` arms read
1.0570 there; while `build`, `mut-odo`, `gen-unsafe` and their twins read 1.0000
in all ten populations, so every point those move anywhere is placement.
The nine class geomeans over the arms with a corrected time run 1.0043
on `reshape1` to 1.0133 on `slice`, basis over dead-spot. **Against Run 22's
twenty sweeps every arm reads 1.0000 to four figures on the main set
and on `revsome`, `bcast`, `reshape1`, `slice` and `scaled`, and within 0.0004
on the other four**, the two sweeps being one binary's --- which is what
the instrument's own agreement is, stated for the first time, and the yardstick
against which Runs 19 to 22's cross-compiler count ratios of 0.9340 and 0.9422
were always codegen.

**The correction sits on the same footing in both halves, as it has on every run
since Run 17.** The in-situ forcing term --- an arm minus its `-nosum` twin,
against the `sum-only` the correction actually subtracts, read off `--aa`'s
`ratio` column --- reads 1.0301, 1.0237, 1.0077 and 1.0755 on the basis
and 1.0274, 1.0198, 1.0173 and 1.0715 on the dead-spot half,
on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm` and `bq-expand`, every one
of the eight tilting the same way and the two halves within a point on each;
the two `sum-only` halves agree at 0.9999 on the basis and 1.0002 on the other.
A margin between these two halves is therefore not carrying a correction bias.

**The ceiling reproduced for a seventh run, on the arm the class property
names.** `mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm
needing nothing at all, reads **0.5466 at 23 wins of 24** and sign p 3e-06
on the basis, against Run 22's 0.5449 on this same binary, Run 21's 0.5424, Run
20's 0.5479, Run 19's 0.5572, Run 18's 0.5577, Run 17's 0.5446 and Run 16's
0.5567 --- the figure [the ruling](../README.md#the-mutable-ceiling-taken) turns
on, moved seventeen ten-thousandths by a repetition. On the dead-spot half
it reads **0.5527**, at the same 23 of 24. Eight runs, three compilers, four
rosters and two layouts have now put the basis reading between 0.5424
and 0.5577.

**This run's two columns MAY be differenced, which reverses Run 22.** `list`
moves **0.33%** between the halves on the main set against the 0.7% bar ---
over all 24 shapes; 0.40% over the 23 the registrations use --- where Run 22
read 0.81% and refused; so the cross-half figures here may be read
as subtractions, and the counted work carries the claim about *why*. Three
classes are past the bar --- `revsome` at 1.0092, `bcastmid` at 1.0093
and `runs` at 0.9894 --- where Run 22 had five, and their blocks say in their
cross-half lines that they are ordered and not subtracted.

**The straddling loops the dead-spot form leaves are in the fills it speeds up,
which prices a straddle below a pad.** The dead-spot half carries four
self-loops straddling a cache line in `Main`-compiled code, and post-run step
0's `-g3` twin names all four by byte identity: `fillStage2Short` at `0x4205aa`,
`fillStage2` at `0x422b2a` and `fbMutOdoVecdimsAddInLeafU2` at `0x42922a`,
55-byte bodies at offset 42, and `fbMutOdoVecdimsAddInLeafU2Down` at `0x4281ef`,
53 bytes at offset 47 --- the branch's own fill, its short-body variant
and the two leaf fills the library ports, four of the nine arms the form makes
four to five percent faster. [What moves a figure when no strategy
changed](../README.md#what-moves-a-figure-when-no-strategy-changed) prices
a straddling loop as a per-element term; here that term is outweighed by the pad
the same form removed from the loop's path, on every one of the four.
The basis's four straddlers are Run 22's to the address, one named
in `fillStage2` and three the twin holds no copy of; these counts
are the survey's, over what `objdump` can sync on in the timed binary, and do
not compare with `align-as.py`'s own section, which counts over the assembly,
nor with Run 21's recipe, whose survey read none. The tracked 28-byte groups sit
where Run 22's did on the basis, `fbMutOdoVecdims` alone at offset 24,
and on the dead-spot half at `[0, 0, 24, 0, 4, 24]`, `fbMutOdoVecdimsAddBoth`
having moved from 0 to 4 and `fbBuild` and `fbMutOdo` staying at 0.

**The regime was confirmed in the binary before the hours were spent**, which
nothing afterwards can: a `diag` in the run's own regime puts `baseOffsetsScan`
at 2408930 bytes against `baseOffsetsMut`'s 2408530 on `vgg-14-c512` on both
halves, Run 22's basis figures to the byte, where plain -O1 separates the two
tenfold. With no rebuild between the gate and the sequence, that is the only
check standing between a mistyped regime and the hours.

**Run 23 records every population twice** --- the main set and all nine stride
classes from each half, one process each --- **in one window**, which Run 22
could not say. Every one of the twenty exited 0 at the bench count its roster
holds --- 1320 twice, 605 twice, 220 four times and 165 twelve times ---
and no process reported a selection it did not ask for. The eighteen class
processes span **14m13s to 52m26s**, the two `runs` processes accounting
for the whole top of that range at 52m25s and 52m26s. **The dead-spot half ran
first throughout**, `spot` before `g912` on the main set and on each class
in turn, which is the driver's order. **The alone-leg riders followed
the sequence**, 108 single-bench processes over four invocations of 27, each
half clean and saturated, each invocation launching on a box between 0.0%
and 0.8% non-idle.

**The decomposition reproduces on both halves for a fifth run.** The riders time
each shape's `list` by itself, one bench per process on that half's own binary,
`SAT=` off and on: the saturated legs split the deflation into the state
the preamble puts on a clean process --- **+11.70%** on the basis
and **+12.37%** on the dead-spot half --- and the rest the roster adds on top
of it, **+0.39%** and **-0.28%**. Run 22 read +12.12% and +12.37% for the state
and +0.15% and +0.22% for the rest, Run 21 +11.84% and +12.02% and +0.12%
and +0.50%. So the state term has now reproduced across five runs inside a point
and a half, while the roster's own contribution has stayed under a point
on every half of every run that measured it, and this run reads it below zero
on one. **The tail is the same shape on both halves and it is the shape Runs 19
to 22 all named**, `stretch-tall-Mx2` at 1.0897 and 1.0928 --- a roster effect
on one shape, now on four rosters and two layouts.

**Everything in this file is replaced by the next run, which is what makes
it a file.** What a run replaces OUTSIDE it, in README.md and in the sources,
is [README's own Provenance](../README.md#provenance). None of it is portable:
a run on another machine is a different measurement rather than a repetition,
which Run 19 was in a position to be firm about, having repeated one binary
on one box and moved its floor by 1.7x. This run repeats that demonstration
for the third time, after Runs 11 and 19, and softens it: the same binary,
the same box, two evenings apart, and the floor went 2.12% to 2.03%, the arms
under a point on 44 of 49 --- so the series 2.32%, 1.51%, 2.92%, 2.12%, 2.03%
over three roster changes and one repetition is a quantity that moves
by a factor of two when the roster moves and by a twentieth when nothing does.
A property of the evening, still, and not one any run inherits from the one
before it.
## Results

The shared forcing pass is subtracted here, as every run since Run 6 must
([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries
that decision and this run's re-pass of its gates), the scratch vectors
are the unboxed ones the shipped code uses, as they have been since Run 7 ([the
scratch vector flavour](../README.md#the-scratch-vector-flavour) says what
that severed), and **this is a `-fspec-constr` table**: it is not the regime
`Data/Array/Internal.hs` compiles under. **A row's distance from Run 22's basis
column is drift and nothing else, for the first time since Run 19, whose basis
was Run 18's binary.** `run23-g912` is Run 22's basis binary byte for byte,
and the flag, the shapes, the order, the allocation area, the box and the recipe
are the same ones, so the distance is what two evenings on one binary disagree
by, measured: over the 23 shapes that exclude `stretch-inner1`, 44 of the 49
arms read within 1% of their Run 22 figure, and the five outside are the two
`libunord` arms, degenerate on more cells this run than last, and three arms
of the placement-exposed families at 1.01% to 2.08%. **This pair's halves differ
in where the shim puts its pads and in nothing else** --- one compiler, one
source, one store --- so a cross-half distance is layout by construction,
and the counted work is what separates a pad the loop executed from a slot
the loop landed in: where an arm's instruction count moved between the halves
it was a pad, and where it did not it was placement or the runtime.

**And it is the basis half's**, `run23-g912`, as every published table here
is from Run 11 on: the dead-spot half's column sits beside the basis one
in [What the next run compares against](#what-the-next-run-compares-against)
rather than as a second copy of these forty-odd rows. That the published half
is the max-skip one is this pair's own decision --- it keeps the lineage, being
the recipe every figure in README was measured through, seven runs running ---
and the dead-spot half is the candidate, whose table can then be read against
something before the run that argues for a move. **No row here is a first
reading**: every arm has Run 22's figure on this same binary, so every row has
a predecessor and every distance from it is drift.

**Comparing runs?** The table below is Run 23's own; what to hold a new run
against is [What the next run compares
against](#what-the-next-run-compares-against), the claims to test are [the ones
after it](#the-claims-the-next-run-should-test), the absolute anchor
is under [Provenance](#provenance) below and the population it was measured
over in [README's delta chain](../README.md#provenance), and this run's own
floor --- no A/A pair further than 2.03% from 1 on the basis half or 2.80%
on the control, the dead-spot half, and 0.39% and 0.40% read on the six pairs
that carry across runs, beside which the worst SINGLE cells of 15.51% and 15.18%
are not floors at all and are not to be quoted as any --- is [in the floor
section][floor]. The sixteen-pair figure governs an arm against *itself*; what
two different rows of the table below must clear is the SIX-pair one, 0.39%
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
  median plus or minus three MADs, the MAD scaled by 1.4826 so the cap
  is in standard deviations. Nothing is dropped by the estimator, so winsorizing
  costs no row its population and a cell far enough out to distort the mean has
  its influence bounded instead of its evidence deleted. **What DOES cost a row
  its population on this run is the correction, not the estimator**: three rows
  on the basis and eleven on the dead-spot half carry cells the shared forcing
  pass is not smaller than, and such a cell cannot be corrected at all ---
  so on those rows the geomean is over 23 or 21 shapes of 24, they are named
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
| *bq-expand-nosum* | *--* | *--* | *0.53* | *79* | *2.35x* | *its base arm, forced with one element* |
| *canon-full-nosum* | *--* | *--* | *0.52* | *102* | *1.00x* | *the same, on a write pattern that varies by shape* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.73* | *91* | *1.33x* | *the same, on a third write pattern* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.48* | *91* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *101* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *101* | *0.00x* | *the same, at the other end* |
| libunord-stage1 | 0.000 | 0.049 | 0.01 | 101 | 0.00x | new mutating `Vector` method -- stage one behind the unordered one-block test |
| libunord-stage2 | 0.000 | 0.052 | 0.02 | 101 | 0.00x | new mutating `Vector` method -- the branch's driver behind the unordered one-block test |
| lib-stage2-short | 0.030 | 0.128 | 0.57 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, a short canonical run written by a body of its length |
| lib-stage2-lean | 0.031 | 0.128 | 0.58 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-disp | 0.031 | 0.128 | 0.59 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, slice route above a run-length threshold |
| lib-stage2-concat | 0.031 | 0.128 | 0.60 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, runs sent back to a concat |
| lib-stage2 | 0.031 | 0.128 | 0.60 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver |
| lib-stage1 | 0.033 | 0.128 | 0.60 | 89 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| lib-stage2-u4 | 0.033 | 0.129 | 0.58 | 96 | 1.00x | new mutating `Vector` method -- the branch's driver, stepping run unrolled by four |
| mut-odo-vecdims-add-in-leaf-u2 | 0.033 | 0.127 | 0.63 | 89 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.033 | 0.127 | 0.60 | 90 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf | 0.036 | 0.122 | 0.57 | 88 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in-leaf-down | 0.042 | 0.124 | 0.68 | 85 | 1.00x | new mutating `Vector` method |
| canon-vecdims | 0.049 | 0.126 | 0.61 | 94 | 1.00x | new mutating `Vector` method |
| liblist-stage2 | 0.049 | 0.160 | 0.93 | 90 | 2.00x | new mutating `Vector` method -- the branch at the list entry point |
| liblist-stage1 | 0.051 | 0.160 | 0.97 | 85 | 2.00x | new mutating `Vector` method -- stage one at the list entry point |
| canon-memcpy-r2 | 0.051 | 0.127 | 0.68 | 94 | 1.00x | new mutating `Vector` method |
| canon-full | 0.053 | 0.126 | 0.63 | 94 | 1.00x | new mutating `Vector` method |
| mut-odo-vecdims-add-in | 0.054 | 0.126 | 0.56 | 80 | 1.00x | new mutating `Vector` method |
| *mut-odo-vecdims-aa-distant* | *0.054* | *0.127* | *0.41* | *80* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.055** | 0.126 | 0.59 | 80 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa* | *0.055* | *0.126* | *0.59* | *80* | *1.00x* | *A/A control* |
| mid-copy | 0.055 | 0.127 | 0.67 | 80 | 1.00x | new mutating `Vector` method |
| bcast-set | 0.057 | 0.127 | 0.70 | 80 | 1.00x | new mutating `Vector` method |
| mut-flat-gm | 0.084 | 0.185 | 0.61 | 82 | 1.33x | new mutating `Vector` method |
| bq-mut-runs-gm-mulback | 0.091 | 0.191 | 0.66 | 80 | 1.33x | mutable `Int` scratch |
| **bq-scan-rem-gm-mulback** | **0.098** | 0.159 | 0.53 | 74 | 1.33x | nothing (pure) |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.098* | *0.159* | *0.64* | *74* | *1.33x* | *A/A control* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.098* | *0.159* | *0.30* | *74* | *1.33x* | *A/A control* |
| bq-odo-gm-mulback | 0.100 | 0.178 | 0.44 | 79 | 1.51x | nothing (pure) |
| *bq-odo-gm-mulback-aa-adjacent* | *0.100* | *0.180* | *0.54* | *79* | *1.51x* | *A/A control* |
| *bq-odo-gm-mulback-aa-distant* | *0.100* | *0.178* | *0.46* | *79* | *1.51x* | *A/A control* |
| bq-expand-gm-mulback | 0.104 | 0.227 | 0.62 | 79 | 2.35x | nothing (pure) |
| *mut-odo-aa-distant* | *0.105* | *0.275* | *0.76* | *70* | *1.00x* | *A/A control* |
| *mut-odo-aa-adjacent* | *0.107* | *0.284* | *0.65* | *70* | *1.00x* | *A/A control* |
| mut-odo | 0.107 | 0.275 | 0.82 | 70 | 1.00x | new mutating `Vector` method |
| build | 0.107 | 0.283 | 1.12 | 70 | 1.00x | new mutating `Vector` method |
| *build-aa-adjacent* | *0.108* | *0.289* | *0.84* | *70* | *1.00x* | *A/A control* |
| *build-aa-distant* | *0.109* | *0.280* | *1.07* | *70* | *1.00x* | *A/A control* |
| *bq-expand-aa-adjacent* | *0.115* | *0.233* | *0.52* | *74* | *2.35x* | *A/A control* |
| bq-expand | 0.115 | 0.234 | 0.65 | 74 | 2.35x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.116* | *0.233* | *0.42* | *74* | *2.35x* | *A/A control* |
| offtab-scan-rem | 0.132 | 0.225 | 0.83 | 72 | 2.00x | nothing (pure) |
| *list-aa-distant* | *0.999* | *1.010* | *0.38* | *35* | *23.50x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.39 | 35 | 23.50x | -- |
| *list-aa-adjacent* | *1.002* | *1.031* | *0.39* | *35* | *23.50x* | *A/A control* |
| *gen-unsafe-aa-distant* | *1.181* | *3.264* | *2.06* | *38* | *1.00x* | *A/A control* |
| gen-unsafe | 1.182 | 3.429 | 2.19 | 38 | 1.00x | -- |
| *gen-unsafe-aa-adjacent* | *1.195* | *3.262* | *2.19* | *38* | *1.00x* | *A/A control* |

`concat-runs` has no row, and neither do the other 36 arms the roster holds
and checks without timing --- 37 of its 92 in all: the reason is at each entry
and the count is [`--lint`'s](../README.md#the-reader-read-runpy). So a movement
below is a movement on all 49 arms this run and Run 22 both give a corrected
time, on one binary, and none of it is a code change or a layout change:
it is the band the head quotes as this box's repetition drift.

**Three things in the table are the run's findings rather than its numbers.**
**The head of the table is where Run 22 left it, within a thousandth,
on the binary Run 22 timed.** `mut-odo-vecdims` reads 0.055 with **nineteen**
timed arms below it and one level --- where Run 22 printed eighteen below
and one level from this same binary, the arm that crossed being
`mut-odo-vecdims-add-in`, at 0.9901 of the arm it varies against Run 22's
0.9944, which is a repetition's drift and not a finding. The nineteen
are the two `libunord` arms at 0.000, six `lib-stage2*` arms and `lib-stage1`
between 0.030 and 0.033, four leaf arms between 0.033 and 0.042, `canon-vecdims`
and the two `liblist` arms between 0.049 and 0.051, `canon-memcpy-r2`
and `canon-full` at 0.051 and 0.053, and `mut-odo-vecdims-add-in` at 0.054;
`mid-copy` is the one level with it, 1.0153 paired at 9 of 24. **The ceiling
reproduced on the arm the class property names, for a seventh run**:
`mut-odo-vecdims` against `bq-scan-rem-gm-mulback`, the fastest arm needing
nothing at all, reads **0.5466 at 23 wins of 24** and sign p 3e-06 on the basis,
against Run 22's 0.5449 on this same binary, Run 21's 0.5424 and Run 20's
0.5479, and **0.5527** on the dead-spot half at the same 23 of 24.
**And the `alloc` column is Run 22's to the digit on both halves**: the fills
at 1.00x, the two `libunord` arms at 0.00x, `list` at 23.50x --- allocation
being deterministic per call, a layout change cannot move it, and on 1245
of the 1272 main-set cells that allocate in earnest the two halves agree
to 1e-4.

**The leaf block's ordering is Run 22's on the basis, and the dead-spot half
narrows its widest gap by more than half.** `genericFillStrided`
in `Data/Array/Internal.hs` is a bang-for-bang port
of `mut-odo-vecdims-add-in-leaf-u2`. Against the fix that arm reads **0.6342
at 22 of 24, sign p 3.6e-05** on the basis and **0.5999 at 23 of 24**
on the dead-spot half, against Run 22's 0.6353 on this same binary ---
so the shipped code is 37% ahead of the code it was refined from on the basis
and 40% ahead where its pad is gone. `mut-odo-vecdims-add-in-leaf-down` reads
**1.2619 of it at 1 of 24, p 3e-06** on the basis, Run 22's 1.2598 within drift,
and **1.0985 at 1 of 24** on the dead-spot half: the count-down variant
is the arm the pads cost most, 20.72% across the halves, and losing them takes
sixteen points off its deficit without changing the ordering. `-add-in-leaf`
reads 1.0673 of `-u2` on the basis at 5 of 24 and **1.1152** on the dead-spot
half at 2 of 24, so it loses on both and by more where `-u2`'s pad is gone.
**What the dispatch around the fill costs is unchanged on both**: `lib-stage1`,
that same fill reached through the library's own regime test, reads **1.0389**
of the bare arm on the basis and 1.0430 on the dead-spot half, against Run 22's
1.0374, so a user's `toVectorT` still pays about four percent over the kernel
on the main set.

**The two standing placement controls read alike on the basis and part
on the dead-spot half.** `mut-odo-vecdims-add-in` against the arm it varies
reads **0.9901 at 19 of 24, sign p 0.0066** on the basis and **0.9896 at 21
of 24, p 0.00028** on the dead-spot half, where Run 22 read 0.9944 at 15 of 24
on this binary; both clear their halves' six-pair figures of 0.39% and 0.40%,
both sit inside the sixteen-pair floors of 2.03% and 2.80%, and both halves put
the two loops at the offsets Run 22 named, 0 and 24. `build` against `mut-odo`
is the pair the dead-spot form was registered to move, and it moved it: **0.9998
on the basis at 11 of 24 by sign and p 0.84** --- a tie, where Run 22 read
1.0125 on this binary --- against **0.9449 on the dead-spot half at 20 of 24
and p 0.0015**, with the tracked loops of `build` and `mut-odo` at offset 0
on both halves, in twin and timed binary alike, so the cache-line reading
is not what separates them there either. What does is under [What this run
was built to answer](#what-this-run-was-built-to-answer-and-what-it-answered),
where the counted work says which of the two executed a pad.


## What the next run compares against

**Run 24's regime and pair are settled, and its roster and shape set are not:
decided 2026-09-02 by whoever asked for this run, Run 24's binaries are Run 23's
dead-spot recipe built TWICE --- one source, one compiler, `LOOP_DEADSPOT=1`
in front of `align-as.py` on both halves --- so the basis MOVES to the dead-spot
form and its first run is the repetition this section says such a move owes.**
The regime is `-fspec-constr`, as every run since Run 8, and it is the regime
the claims decide in; the shipped file does not set the flag ([the
ceiling](../README.md#the-mutable-ceiling-taken)). The roster and the shape set
were undecided when this was written; whatever they become, [the recommended
tasks after Run 23](../README.md#recommended-tasks-after-run-23) is where
an addition is registered, and a roster that moves puts a layout term back
into the cross-run column that a repetition alone would not carry. **What
the decision weighed, kept as the record of it.** What this run said
for the move: every arm whose fill carried a pad is five to six percent faster
under it on the main set, on five of nine classes outright and inside the floor
on the other four, and the flatness controls and the claims do not move. What
it says against, or at least aside: `mut-odo` is slower under it in three
classes past a floor (`scaled` 3.6%, `window` 6.5%, `revsome` 3.5%), the two
`-u2` leaf arms are slower on `reshape1` by 2.2% and 3.6% against one
of that class's two floors, the four straddling loops the form leaves are
in the branch's own fills, and every figure in this README's lineage
was measured through the max-skip recipe, so a move puts a layout term
into the next cross-run column exactly as a roster change does. **What Run 24's
pair buys**: the first published table on the dead-spot recipe read against
a second build of the same recipe, which is the instrument this run has just
shown to be worth having --- one binary, two evenings, 44 of 49 arms within
a point --- taken this time within one evening and on the new basis before
anything else is varied. **What waits behind it**: the `dispRun` threshold pair
the open list names is still the cheapest decisive pair this file has been able
to name in four runs --- one binary, one arm per candidate threshold,
over the `runs` class alone, wanting no evening and no second recipe --- and Run
23 re-read the dispatch killed at `runs-1024` on both halves, so the question
stays live. **What is NOT a candidate** is unchanged: a pair varying
the allocation area, closed 2026-08-21, and one varying the roster between
its halves, refused because it would break `preflight`'s `check` comparison
and both drivers' bench counts.

**The compiler variable has stopped paying, and Run 23 confirms it
from the other side.** Runs 19 to 22 each varied the compiler and the last three
read the same answer; this run varied nothing but the shim's pad placement
on one compiler and read a five-percent term on the fills that no compiler pair
could have separated from codegen, both moving at once on those pairs.
So the variable to vary next is a layout one or a threshold one,
and the compiler stays where it is.

**What Run 23 leaves the next run to read against, and the first item is
not a figure.** **The box did not change**, its gate machine check reading
-0.44% against the fingerprint Run 22 kept and the run's own main-set process
reading -0.40% against that same fingerprint, over 24 of 24 shapes both times,
worst -1.58% and +1.86% and none past 5%; so absolutes cross from Run 22 to Run
23 freely and the boundary that matters is still the BIOS change before Run 18,
which no absolute crosses. **The floor is 2.03% on the basis and 2.80%
on the control**, with the restricted six at 0.39% and 0.40%. A Run 24 margin
is judged on both and they answer different questions: the six-pair figure
is what two rows of one table must clear, the sixteen-pair one is how far an arm
differs from its own duplicate. **And it is not inherited**: Run 22 read 2.12%
on this very binary two evenings earlier and this run reads 2.03%, so a floor
moves by a twentieth when nothing moves and by a factor of two when the roster
does, and a Run 24 margin is judged against Run 24's own, never against these.
**The two columns below MAY be differenced, which reverses Run 22**: `list`
moved **0.33%** between the halves against the 0.7% bar, where Run 22 read 0.81%
and was refused and Run 21 0.64%. So read them as a subtraction where one
is wanted; and note that three of the nine classes are past the bar ---
`revsome` 1.0092, `bcastmid` 1.0093 and `runs` 0.9894 --- while the other six
are inside it. What the columns price is the shim's pad placement,
and the counted-work column says which movements that reaches: the padded fills
four percent apart ON their instruction counts and five in time,
`-add-in-leaf-down` nine points of its twenty, and the placement-exposed arms
`build`, `mut-odo` and `gen-unsafe` apart at count ratios of 1.0000.
So a movement on one of those three is layout or runtime --- and this run's
cross-run column against Run 22 carries no layout term at all, its basis being
Run 22's binary.

**Registered with the pair.** Run 23's six registrations, their kill conditions
and their verdicts are [in this file's last
section](#what-this-run-was-built-to-answer-and-what-it-answered),
and the commands that produced them were the pair note's, transcribed
into Provenance below before that note goes with the pair. **What Run 24
inherits is the same five riders, routine, and one instrument that is new only
in having been used**: the alone legs, the counted-work sweeps over every
population, the saturating preamble, the per-sample load fields and `--counts`
all ran to form; the counted work was again taken outside the quiet window;
and the exact repetition --- a basis binary identical to the previous run's ---
was taken for the first time since Run 19 and priced this box's day-to-day drift
at under a point on 44 of 49 arms. **What it inherits as a warning** is about
the placement-exposed arms: a registration that predicts `gen-unsafe`
or `mut-odo` to a figure off one evening will miss, this run's cross-half
readings of the two landing 4.9 and 2.3 points from task 6's on the same two
binaries, where the fills landed within one. Predict those arms' direction
and their twins' agreement, not their size.

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

**The next run compares against Run 23 and against nothing before it.** Each
run's figures and the names of its halves are in its own file, `runs/run<N>.md`,
back-filled to Run 7 on 2026-08-29; a comparison reaching further back
is a chain of one-step comparisons, each recorded by the run that made it,
and walking that chain here is what this section stopped doing. So an older run
is read by opening its file, not by reading a column across. This run's own two
halves, on the rows nearest the decisions --- `+lookrts` in the column heads
being the tag the lineage's recipe has carried since Run 15 and not a variable
of this pair:

| strategy | Run 23 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) | Run 23 (SpecConstr, dead-spot +lookrts, -A32m, 9.12.4) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.055** | 0.055 |
| `mut-flat-gm` | **0.084** | 0.084 |
| `bq-mut-runs-gm-mulback` | **0.091** | 0.092 |
| `bq-odo-gm-mulback` | **0.100** | 0.100 |
| `bq-scan-rem-gm-mulback` | **0.098** | 0.098 |
| `bq-expand` | **0.115** | 0.116 |
| `build` | **0.107** | 0.101 |

**A published geomean is over the same 24 shapes, and two halves of one
SpecConstr run usually share a denominator too**, `list` moving under 0.7%
between them --- so such a pair may be subtracted and not merely ordered, which
is what an -O1 reading cannot do at an 8% baseline shift. **THE TABLE ABOVE
IS SUCH A PAIR**, `list` having moved 0.33% on this run's main set, so the two
columns may be differenced --- and what the difference reads is nothing
on the six pure and mutable arms and six thousandths on `build`,
the placement-exposed worker, which is the pair's whole story in one row; Run
22's 0.81% was the exception this sentence allows for. **A pair that varies
the allocation area is the exception, and its two halves may never be subtracted
from each other.** `list` moved **9.20%** between Run 14's halves, **5.13%**
between Run 15's and **16.51%** between Run 16's. **Run 16's is the largest
of the three and was registered to be the smallest**, on the reasoning
that its two halves both sit at enlarged areas where the earlier two each
crossed the default --- a prediction refuted by its own run, and the refutation
is the finding: what moves the baseline is not the distance from the default
but the in-process deflation, which at roster scale is worse at 64 MB than at 32
MB by more than the whole default-to-32 MB step was worth. So the exception
widens rather than narrowing, and it covers every pair that varies the area
at all. Every cell of such a pair's second column is scaled by a denominator
the pairing moved: read it for the pairing's direction, take no strategy quality
off it, and read the arm-by-arm comparison at the head of this file instead,
which divides absolutes rather than ratios.

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
published, and the next run that adds one should ask whether it still reads. Run
23 adds none: the installer's membership note names `libunord-stage2`
and `libunord-stage1` as best outside the family on 17 and 13 shapes, which
is their one-block test returning a slice and not a fill leading anything,
and `lib-stage2-u4` and `lib-stage2-short` on 13 and 7, candidates whose column
is the basis decision's to grant, so the fourteen stand.

| shape | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cnn-slice-c32` | 3 | 288 | 5.92 us | 0.084 | 0.145 | 0.159 | 0.173 | 0.170 | 0.149 | 0.169 | 0.115 | 0.087 | 0.086 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.24 us | 0.094 | 0.178 | 0.144 | 0.203 | 0.202 | 0.185 | 0.162 | 0.103 | 0.104 | 0.097 |
| `stretch-rank12` | 2 | 4096 | 109 us | 0.094 | 0.185 | 0.130 | 0.283 | 0.275 | 0.191 | 0.170 | 0.073 | 0.106 | 0.098 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 114 us | 0.066 | 0.128 | 0.097 | 0.178 | 0.178 | 0.135 | 0.124 | 0.056 | 0.071 | 0.071 |
| `conv1d-24` | 3 | 5184 | 101 us | 0.056 | 0.070 | 0.099 | 0.134 | 0.126 | 0.077 | 0.136 | 0.058 | 0.057 | 0.060 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 364 us | 0.048 | 0.093 | 0.094 | 0.109 | 0.108 | 0.100 | 0.120 | 0.044 | 0.049 | 0.051 |
| `gather48-src-50` | 3 | 22500 | 433 us | 0.054 | 0.067 | 0.099 | 0.134 | 0.122 | 0.075 | 0.132 | 0.053 | 0.054 | 0.057 |
| `stretch-rank10` | 3 | 59049 | 1.27 ms | 0.065 | 0.109 | 0.102 | 0.183 | 0.172 | 0.117 | 0.139 | 0.055 | 0.068 | 0.069 |
| `stretch-coprime-r7` | 13 | 60060 | 1.02 ms | 0.034 | 0.083 | 0.093 | 0.063 | 0.060 | 0.094 | 0.124 | 0.033 | 0.035 | 0.037 |
| `cifar-L2-16-c64-k3` | 3 | 147456 | 3.03 ms | 0.058 | 0.091 | 0.100 | 0.142 | 0.149 | 0.100 | 0.132 | 0.057 | 0.059 | 0.062 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.46 ms | 0.059 | 0.090 | 0.099 | 0.147 | 0.153 | 0.095 | 0.129 | 0.056 | 0.058 | 0.061 |
| `stretch-primes` | 89 | 250357 | 3.95 ms | 0.029 | 0.076 | 0.093 | 0.031 | 0.030 | 0.087 | 0.132 | 0.029 | 0.029 | 0.030 |
| `stretch-inner1` | 1 | 500000 | 12.8 ms | 0.091 | 0.031 | 0.073 | 0.229 | 0.245 | 0.031 | 0.073 | 0.000 | 0.090 | 0.098 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.1 ms | 0.044 | 0.075 | 0.092 | 0.095 | 0.096 | 0.085 | 0.124 | 0.043 | 0.045 | 0.046 |
| `vgg-14-c512-k3` | 3 | 903168 | 18.7 ms | 0.060 | 0.089 | 0.098 | 0.144 | 0.151 | 0.096 | 0.131 | 0.058 | 0.058 | 0.060 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 18.2 ms | 0.035 | 0.072 | 0.091 | 0.058 | 0.057 | 0.084 | 0.131 | 0.034 | 0.036 | 0.038 |
| `stretch-inner256` | 256 | 1750784 | 32.9 ms | 0.032 | 0.068 | 0.085 | 0.032 | 0.033 | 0.074 | 0.117 | 0.031 | 0.031 | 0.031 |
| `stretch-pow2stride` | 64 | 1769472 | 28 ms | 0.126 | 0.123 | 0.148 | 0.127 | 0.127 | 0.136 | 0.225 | 0.126 | 0.127 | 0.127 |
| `stretch-r5-8x432` | 8 | 1769472 | 33.8 ms | 0.032 | 0.061 | 0.082 | 0.055 | 0.054 | 0.068 | 0.116 | 0.032 | 0.032 | 0.035 |
| `stretch-square-1341` | 1341 | 1798281 | 29.5 ms | 0.088 | 0.133 | 0.156 | 0.089 | 0.090 | 0.141 | 0.204 | 0.085 | 0.087 | 0.087 |
| `stretch-bigstride` | 3 | 1800000 | 49.3 ms | 0.035 | 0.045 | 0.067 | 0.079 | 0.086 | 0.051 | 0.093 | 0.035 | 0.035 | 0.038 |
| `stretch-tab7MB` | 2 | 1800000 | 37.6 ms | 0.063 | 0.063 | 0.101 | 0.148 | 0.151 | 0.068 | 0.145 | 0.062 | 0.063 | 0.068 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 39.2 ms | 0.023 | 0.052 | 0.064 | 0.023 | 0.023 | 0.058 | 0.096 | 0.023 | 0.023 | 0.023 |
| `stretch-wide-2xM` | 2 | 1800000 | 38 ms | 0.061 | 0.061 | 0.098 | 0.144 | 0.146 | 0.069 | 0.143 | 0.061 | 0.061 | 0.065 |

| shape | class | `sInner` | `l` | `list`, net | vecdims | flat-gm | scan-rem-gm | build | mut-odo | runs-gm | offtab-rem | canon-vd | mid-copy | bcast-set |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `bcast-inner8` | `bcast` | 8 | 51200 | 872 us | 0.032 | 0.066 | 0.090 | 0.064 | 0.059 | 0.080 | 0.117 | 0.032 | 0.032 | 0.030 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 27.2 ms | 0.022 | 0.071 | 0.088 | 0.022 | 0.022 | 0.089 | 0.123 | 0.022 | 0.022 | 0.019 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 36.9 ms | 0.063 | 0.062 | 0.100 | 0.149 | 0.156 | 0.071 | 0.143 | 0.062 | 0.062 | 0.062 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.46 ms | 0.057 | 0.090 | 0.100 | 0.153 | 0.155 | 0.101 | 0.127 | 0.057 | 0.012 | 0.061 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 3.89 ms | 0.021 | 0.069 | 0.087 | 0.023 | 0.023 | 0.085 | 0.122 | 0.022 | 0.013 | 0.023 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 46.5 ms | 0.036 | 0.046 | 0.069 | 0.087 | 0.086 | 0.055 | 0.095 | 0.036 | 0.033 | 0.039 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 41.7 ms | 0.023 | 0.053 | 0.067 | 0.023 | 0.023 | 0.061 | 0.090 | 0.023 | 0.018 | 0.023 |
| `reshape1-rank10` | `reshape1` | 1 | 59049 | 1.89 ms | 0.108 | 0.127 | 0.091 | 0.315 | 0.314 | 0.127 | 0.091 | -- | 0.116 | 0.106 |
| `reshape1-r3` | `reshape1` | 1 | 180000 | 4.7 ms | 0.091 | 0.033 | 0.073 | 0.276 | 0.241 | 0.032 | 0.073 | -- | 0.091 | 0.092 |
| `reshape1-strided-r3` | `reshape1` | 1 | 180000 | 4.72 ms | 0.094 | 0.033 | 0.075 | 0.279 | 0.244 | 0.033 | 0.075 | 0.016 | 0.095 | 0.095 |
| `reshape1-500k` | `reshape1` | 1 | 500000 | 12.9 ms | 0.091 | 0.031 | 0.073 | 0.228 | 0.230 | 0.031 | 0.072 | -- | 0.090 | 0.091 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 114 us | 0.067 | 0.126 | 0.098 | 0.179 | 0.179 | 0.137 | 0.124 | 0.057 | 0.073 | 0.070 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 436 us | 0.053 | 0.066 | 0.098 | 0.130 | 0.120 | 0.073 | 0.130 | 0.052 | 0.053 | 0.056 |
| `rev-primes` | `rev` | 89 | 250357 | 4 ms | 0.029 | 0.072 | 0.091 | 0.030 | 0.030 | 0.085 | 0.130 | 0.029 | 0.029 | 0.030 |
| `revsome-outer-g48` | `revsome` | 3 | 22500 | 437 us | 0.053 | 0.069 | 0.101 | 0.133 | 0.119 | 0.076 | 0.132 | 0.054 | 0.054 | 0.057 |
| `revsome-mid-cnn-L2` | `revsome` | 3 | 165888 | 3.46 ms | 0.057 | 0.091 | 0.099 | 0.150 | 0.135 | 0.098 | 0.129 | 0.057 | 0.059 | 0.061 |
| `revsome-inner-primes` | `revsome` | 89 | 250357 | 4.02 ms | 0.030 | 0.081 | 0.103 | 0.031 | 0.031 | 0.093 | 0.131 | 0.030 | 0.030 | 0.031 |
| `runs-65536` | `runs` | 65536 | 1769472 | 25.9 ms | 0.028 | 0.079 | 0.098 | 0.030 | 0.027 | 0.092 | 0.138 | 0.029 | 0.028 | 0.028 |
| `runs-1024` | `runs` | 1024 | 1799168 | 26.4 ms | 0.028 | 0.075 | 0.093 | 0.029 | 0.028 | 0.088 | 0.136 | 0.029 | 0.028 | 0.030 |
| `runs-512` | `runs` | 512 | 1799680 | 26.1 ms | 0.028 | 0.076 | 0.093 | 0.029 | 0.029 | 0.090 | 0.137 | 0.029 | 0.029 | 0.031 |
| `runs-256` | `runs` | 256 | 1799936 | 26.6 ms | 0.028 | 0.075 | 0.091 | 0.029 | 0.029 | 0.088 | 0.136 | 0.029 | 0.028 | 0.030 |
| `runs-2` | `runs` | 2 | 1800000 | 37.1 ms | 0.064 | 0.064 | 0.103 | 0.147 | 0.163 | 0.070 | 0.152 | 0.063 | 0.063 | 0.068 |
| `runs-3` | `runs` | 3 | 1800000 | 34 ms | 0.052 | 0.066 | 0.098 | 0.113 | 0.128 | 0.073 | 0.140 | 0.052 | 0.051 | 0.055 |
| `runs-4` | `runs` | 4 | 1800000 | 32 ms | 0.045 | 0.068 | 0.098 | 0.098 | 0.100 | 0.077 | 0.137 | 0.045 | 0.045 | 0.050 |
| `runs-5` | `runs` | 5 | 1800000 | 31.3 ms | 0.043 | 0.069 | 0.096 | 0.081 | 0.084 | 0.079 | 0.135 | 0.042 | 0.042 | 0.045 |
| `runs-9` | `runs` | 9 | 1800000 | 29.4 ms | 0.034 | 0.070 | 0.093 | 0.056 | 0.060 | 0.081 | 0.133 | 0.035 | 0.034 | 0.037 |
| `runs-96` | `runs` | 96 | 1800000 | 26.8 ms | 0.028 | 0.074 | 0.092 | 0.029 | 0.029 | 0.087 | 0.138 | 0.028 | 0.029 | 0.029 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 26.7 ms | 0.030 | 0.075 | 0.094 | 0.034 | 0.035 | 0.087 | 0.137 | 0.028 | 0.030 | 0.031 |
| `scaled-r5` | `scaled` | 13 | 15015 | 250 us | 0.033 | 0.072 | 0.094 | 0.052 | 0.049 | 0.081 | 0.127 | 0.031 | 0.033 | 0.036 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 946 us | 0.028 | 0.072 | 0.092 | 0.033 | 0.033 | 0.082 | 0.126 | 0.029 | 0.028 | 0.029 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 4.71 ms | 0.033 | 0.072 | 0.091 | 0.033 | 0.033 | 0.082 | 0.135 | 0.033 | 0.033 | 0.033 |
| `slice-coprime-r7` | `slice` | 13 | 60060 | 1.04 ms | 0.036 | 0.083 | 0.095 | 0.064 | 0.061 | 0.093 | 0.126 | 0.037 | 0.036 | 0.039 |
| `slice-cnn-L2-24x24-c32` | `slice` | 3 | 165888 | 3.53 ms | 0.058 | 0.089 | 0.100 | 0.160 | 0.149 | 0.097 | 0.132 | 0.058 | 0.059 | 0.061 |
| `slice-primes` | `slice` | 89 | 250357 | 3.98 ms | 0.030 | 0.081 | 0.104 | 0.032 | 0.032 | 0.093 | 0.133 | 0.030 | 0.030 | 0.031 |
| `window-28x28-k5` | `window` | 5 | 14400 | 265 us | 0.044 | 0.077 | 0.094 | 0.101 | 0.096 | 0.087 | 0.120 | 0.045 | 0.044 | 0.047 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 860 us | 0.098 | 0.050 | 0.075 | 0.294 | 0.260 | 0.049 | 0.075 | 0.020 | 0.103 | 0.104 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.29 ms | 0.056 | 0.087 | 0.095 | 0.145 | 0.140 | 0.096 | 0.125 | 0.058 | 0.056 | 0.059 |

**One row to read first, and it is a property of the shape and not of any arm**:
`stretch-inner1` has `sInner` 1, so anything special-casing a unit dimension
behaves differently there by construction --- and on this run it is the cell
where the correction gives out. Every canonicalizing arm returns a slice there,
and on the dead-spot half all eleven of them --- the three `canon-*` arms,
the six `lib-stage2*` arms and the two `libunord` arms --- cost less
than the shared forcing pass on that shape, so their cells read `--` and their
rows are geomeans over 23 or 21 shapes; on the basis the same cell sinks
for `lib-stage2-short` alone and sits a few nanoseconds above zero for the rest,
which is why every registration figure in the last section is taken over the 23
shapes that exclude it, and why a `--pair` against `lib-stage2` over 24 shapes
reads a ratio of nothing there. The two rows this paragraph used to name
are retired with the arms that derived them.


## The claims the next run should test

**Run 23's verdicts first**, since a run reports breaks rather than re-deriving
the table. **The one manifest claim left held on both halves**, all four
of claim 1's links on the max-skip basis and all four on the dead-spot half ---
no BROKE on either, a sixth clean sweep running, and the first read on two
halves of one compiler. What this run adds to the sweep is a repetition:
the basis is Run 22's binary timed again, so each link's distance from Run 22's
reading is drift --- 0.0073, 0.0030, 0.0025 and 0.0045 on the four ---
and a layout pair, across which every link moves under a point as well. Every
arm claim 1 names is still timed, and `--pair` recovers any retired ordering
in one call whenever it is wanted.

**The six retired claims are not re-read here.** Claims 3, 4, 5 and 9 left
the manifest at Run 19's write-up, on a sweep in which all thirteen held on both
of that run's halves; claims 2 and 6 left on 2026-08-28 with the parking
of the arms their surviving links turned on, and their last readings are Run
20's, in that run's own file. The numbered items below say what each was
in a clause. Run 23 does not re-derive any of them and quotes none as its own:
of the arms they named, those still rostered and timed put any
of those orderings one `--pair` call away, and the parked ones would want a run
that re-times them --- which is the whole of what retiring them gave up.

**Claim 1 held on all four links, on both halves, and the two halves read
it within a point of each other.** The four links are what the `needs` column
draws: what a mutating `Vector` method buys (**0.6521** on the basis), what one
more mutable write pattern buys (0.9180), and what a mutable `Int` scratch buys
against the two fastest arms needing nothing (0.9133 and 0.9130).
On the dead-spot half the same four hold at **0.6559, 0.9161, 0.9192
and 0.9199** --- no link wider than a point from the basis's, which is what
a pair whose pads sit on none of these six arms should read. Against Run 22's
0.6448, 0.9210, 0.9158 and 0.9175, taken on this same basis binary, the four
moved by 0.0073, 0.0030, 0.0025 and 0.0045.

**Readings:** `mut-odo-vecdims` / `mut-flat-gm` 0.6521, 20 of 24, sign p 0.0015;
`mut-flat-gm` / `bq-mut-runs-gm-mulback` 0.9180, 23 of 24, sign p 3e-06;
`bq-mut-runs-gm-mulback` / `bq-odo-gm-mulback` 0.9133, 20 of 24, sign p 0.0015;
`bq-mut-runs-gm-mulback` / `bq-scan-rem-gm-mulback` 0.9130, 18 of 24, sign p
0.023. 4 of 4 registered orderings held.

**The first link's top rung still understates what a mutating method buys
by a factor.** Claim 1 reads `mut-odo-vecdims` against `mut-flat-gm`,
and **nineteen** arms read below `mut-odo-vecdims` with one more level with it,
at 0.000 to 0.054 against its 0.055 --- Run 22's eighteen and one on the same
binary, `mut-odo-vecdims-add-in` having crossed by a thousandth. **Two
of the nineteen are not fills at all**, `libunord-stage1` and `libunord-stage2`
at 0.000, which return a single `VS.slice` where their one-block test fires
and so measure dispatch; the other seventeen do the work. **And the shipped
library route sits well inside the group**, `lib-stage1` at 0.033, as does every
one of the six candidates. Whether the claim should be re-aimed at the family's
leader is a question for the next run and is [under the recommended
tasks](../README.md#recommended-tasks-after-run-23); it is not re-aimed here,
a claim being re-aimed on a decision and not on one reading.

**Claim 7 held on every level, on both halves, to the digit.** Every level
is Run 15's through Run 22's --- the mutable fills at 1.00x, the scan family
1.33x, `bq-odo-gm-mulback` 1.51x, `offtab-scan-rem` 2.00x, `bq-expand` 2.35x,
`list` 23.50x, and the floor under the floor, `libunord-stage1`
and `libunord-stage2` at **0.00x** --- and the class blocks read the tiers
unbroken in all nine classes, `bq-expand` running 1.14x on `scaled` to 4.91x
on `reshape1` where that class's own `m` shows through, and `list` 19.43x
to 32.29x. **The cross-half agreement is the instrument's own this run, the two
halves being one compiler's code**: **1245 of the 1272** main-set cells
that allocate in earnest agree to 1e-4, where Run 22's two compilers agreed
on 1123, and the worst disagreement is **1.92e-03
on `stretch-tall-Mx2/libunord-stage1`**, an arm at 0.00x whose fit resolves near
nothing. Allocation is deterministic per call and a layout change cannot reach
it, so the 27 cells apart are what fitting one allocation twice disagrees by,
and a later pair reading a disagreement past that on identical code is reading
a code change.

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
by at most 3.3% on Run 11's reading and 2.1% on Run 23's, most of them
by under a point, so a margin above a few percent is now evidence of a strategy.
**Run 13 is the first pair here to hold every tracked loop at one offset in both
halves**, which is what lets its arm-by-arm comparison be read as the package
costing nothing rather than as two terms cancelling. A claim resting on an arm
whose own loop the shim skipped --- `list`'s, which is library code --- is still
decidable nowhere until that loop is read. **And the pinning claim is measured
only in its weak form**: adding `mut-flat-gm-nosum` left every tracked loop
at the same address, but a `Force` arm reuses a rostered function and emits
no code for emission order to move. The strong form wants an arm that emits
its own, and until one is added the claim covers additions that cost nothing
to place.

**The list did NOT need re-aiming this run, and nothing in it changed**:
the roster is Run 22's exactly, no arm landed or left, and claim 1's four links
all name arms that are still timed. **What the roster raises is the question Run
22 raised**, unchanged in size: nineteen arms read below `mut-odo-vecdims`, six
of them the candidates Run 22 added and one of them the shipped library route.
That is left to the next run rather than re-aimed here, and it is [under
the recommended tasks](../README.md#recommended-tasks-after-run-23).

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
   figure five runs running. The ordering has survived nine runs, two changes
   of basis, two repetitions and three compilers.
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

**And for each stride class, the same three properties, now carrying Run 23's
verdicts** over nine classes, the details beside each class's table:

1. **The regime 3 fix's `worst` stays under 1.** Held in every one of the ten
   populations, on both halves, in every regime, roster and layout the README
   has run --- so the fix was never slower than the `list` it replaced, on any
   shape of any class the library can produce. This is the property the classes
   exist to test, no geomean can state it, and a break would be the one result
   here to bear on `Data/Array/Internal.hs` directly. Re-aimed 2026-08-22
   with the decision to ship `mut-odo-vecdims`, and read for that arm since:
   **on Run 23 its worst is 0.126 on the main set and 0.108 in a class
   (`reshape1`), both read on the basis half, with the dead-spot half at 0.124
   and 0.112** --- so the property holds for the arm decided, on both layouts,
   and neither end is within a tenth of 1: the main-set end is a factor of 7.9
   inside it and the class end 9.3. Both halves are quoted because one
   is not enough: Run 18's entry here read a floor-level figure from whichever
   half happened to be lower, which is the defect this phrasing exists
   to prevent. **What breaks it is again not a fill the library would ship.**
   `gen-unsafe` carries a `worst` above 1 in all ten populations on the basis,
   from 1.035 on `bcast` to 3.429 on the main set, and in nine of ten
   on the dead-spot half, `runs` reading 0.901 there --- but it is a baseline
   variant, and its twins and the `list` twins that cross 1 are the baseline's
   own controls. **The library-shaped arms break it on `runs` alone and all
   at `runs-2`**, six of eleven on both halves, as Run 22 found on this same
   basis binary: `libunord-stage1` at **1.362**, `liblist-stage1` at 1.354,
   `lib-stage2-concat` at 1.350, `lib-stage1` --- the shipped route ---
   at **1.333**, `liblist-stage2` at 1.167 and `libunord-stage2` at 1.161
   on the basis, and 1.375, 1.352, 1.341, 1.325, 1.154 and 1.153
   on the dead-spot half. So on 900000 runs of two elements SIX of the eleven
   library-shaped arms are slower than the `list` baseline they replace ---
   every route that takes a slice per run at that length --- while `lib-stage2`,
   the three fill candidates and the dispatch built on it fill every run
   whatever its length and are the five that are not. **The property is stated
   of `mut-odo-vecdims` and holds of it; it does NOT hold of what the library
   actually calls.** `lib-stage1` is the shipped route and is among the six,
   at 1.333 and 1.325 --- so a reader taking property 1 as clearance
   for the code that ships is reading it wider than it is stated, and the class
   that catches the difference is `runs`.

2. **The top of the table keeps its order**: `mut-odo-vecdims` fastest,
   `bq-expand` behind it. **The first clause breaks outright in seven
   of the nine CLASS populations on both halves --- the main set is the tenth
   and is counted separately throughout this section --- and in the other two
   the fastest arm is a `mut-odo-vecdims` sibling, which is read as the family's
   and not as a break**, where Run 22 read it outright in all nine on this same
   basis binary: `slice` and `scaled` are led by `-add-in-leaf-u2-down`
   at 0.7526 and 0.9060 of the fix, with `lib-stage2-short` and `lib-stage1`
   level with it at the third decimal, and a sibling's lead is read
   as the family's until a run separates them. The seven divide three ways.
   **Three are degenerate**: `libunord-stage2` leads `rev`, `revsome`
   and `reshape1` at 0.0136, 0.0091 and 0.0003 of the fix, its one-block test
   firing on every view of those classes and collapsing them to a single slice,
   so it prices dispatch and not filling. **Two are the unrolled fill**:
   `lib-stage2-u4` leads `bcast` and `bcastmid` at 0.5993 and 0.5266, margins
   of 40.1% and 47.3% against those populations' floors of 5.87% and 2.77% ---
   on the dead-spot half `bcast`'s head is `lib-stage2-lean` at 0.021, the four
   fills there sitting within two thousandths. **Two are the short-body fill**:
   `lib-stage2-short` leads `window` and `runs` at 0.3282 and 0.7654, margins
   of 67.2% and 23.5% against 4.50% and 3.45%, the second on 6 of 11 shapes
   at sign p 1, a lead the short lengths carry alone. **So five of the six
   classes Run 22 found led by a candidate still are**, four outright
   and `slice` by a candidate level with a sibling, and `scaled`'s head is three
   arms at 0.027 --- the sibling, `lib-stage1` and `lib-stage2-u4`, which led
   it a run ago by a thousandth. The third clause reads the last candidate
   `bq-expand` behind `mut-odo-vecdims` and holds in all nine on both halves.

3. **The allocation tiers survive, and every level is Run 15's through Run 22's
   to the digit**: the mutable fills at the result vector, `bq-expand` between
   1.14x and 4.91x it, `list` an order of magnitude above. Where a level moves
   it is the class's own `m` showing through, exactly as this property warned
   --- `bq-expand` at 1.14x on `scaled` (`m` of 1 and 2,000) and 4.91x
   on `reshape1` (`m = l`) --- with the ordering of tiers unbroken in all nine
   and `list` running 19.43x to 32.29x across them, on both halves and
   to the digit. The two `libunord` arms sit BELOW the result vector at 0.00x
   in every class, returning a slice rather than filling anything, and the four
   other arms Run 22 added read 1.00x, the fills' own tier. On a pair whose two
   halves are one compiler's code this is the property that says nothing changed
   but the bytes' addresses: the two halves agree on 1245 of 1272 allocating
   main-set cells, and every tier is identical on both.

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

**Run 23 (SpecConstr, max-skip +lookrts, -A32m, 9.12.4) records every class
on BOTH halves**, one process each, in [the
sequence](../README.md#making-a-major-benchmark-run), all twenty processes
in one window this run where Run 22's ran in two. Every table below
is the **basis half**'s, the max-skip one, the half that keeps the lineage
and is Run 22's binary; what the second half buys is that the pair's variable
--- where the shim puts its pads --- can be read on a class, which is what
settled Run 14's `scaled` question. **Read across the halves and the dead-spot
form is faster nearly everywhere.** Of the 441 arm-comparisons the nine classes
carry, nine (`reshape1`'s canonicalizing arms, a basis cell of each not left
positive by the correction) sit out the vote and the geomeans as degenerate;
**116 put the basis half faster and 316 the dead-spot half**, and the nine
geomeans run **0.9985 on `reshape1` to 1.0351 on `bcast`**, eight of them
above 1. **The high extreme is one arm in eight of the nine classes**,
`mut-odo-vecdims-add-in-leaf-down`, from 1.1343 on `scaled` to 1.3991 on `bcast`
--- the count-down leaf fill, the arm whose pads cost most on the main set too
--- `revsome`'s being `libunord-stage2` at 1.4101. **The low extreme
is `mut-odo` in three of the nine**, `revsome` 0.9655, `window` 0.9351
and `scaled` 0.9636, the basis faster: the one worker the dead-spot form costs,
and it costs it in the classes and not on the main set, where the arm reads
1.0020 over all 24 shapes. **Three classes disqualify their own cross-half
line**, where Run 22 had five: `revsome` at 1.0092, `bcastmid` at 1.0093
and `runs` at 0.9894 move `list` past the 0.7% bar, so their lines say
so and are not read for the pads --- and the main set, at 1.0033, is inside
it this run, where Run 22's 0.81% was not.

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
   this process's own floor and its own three gates, neither inherited nor lent
   --- and where the paragraph quotes the OTHER half's figure, it says so
   in the form `the other half's own sixteen pairs span N%` and never
   with the word *floor* beside the number, which `--check-doc` holds
   to this table's column (Run 23 was refused four times before it learned
   the shape);
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
   --- how many of the population's arms move, which way, and the spread;
   a margin on this line is judged against the WIDER of the two halves' floors
   ([README, the floor section][floor]). Both halves have run every class since
   2026-08-14 and this is where that is read: a pair's variable can act
   on a class and not on the main set, which is how Run 14 answered its `scaled`
   question. A run whose halves differ in nothing a class can see says so
   in a clause;
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
| `rev` | 3 | 0.047 | 0.067 | **`libunord-stage2`** 0.001 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 | 7.21% |
| `revsome` | 3 | 0.049 | 0.057 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 4.25% |
| `bcast` | 3 | 0.035 | 0.063 | **`lib-stage2-u4`** 0.019 | `mut-odo-vecdims-add-in-leaf` 0.022 | 5.87% |
| `bcastmid` | 4 | 0.032 | 0.057 | **`lib-stage2-u4`** 0.017 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.022 | 2.77% |
| `reshape1` | 4 | 0.094 | 0.108 | **`libunord-stage2`** 0.000 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.024 | 3.09% |
| `slice` | 3 | 0.040 | 0.058 | `lib-stage2-short` 0.030 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.030 | 3.11% |
| `window` | 3 | 0.062 | 0.098 | **`lib-stage2-short`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.029 | 4.50% |
| `scaled` | 3 | 0.032 | 0.033 | `lib-stage1` 0.027 | `mut-odo-vecdims-add-in-leaf-u2-down` 0.027 | 1.99% |
| `runs` | 11 | 0.033 | 0.064 | **`lib-stage2-short`** 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 | 3.45% |

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
| *canon-full-nosum* | *--* | *--* | *0.07* | *144* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.28* | *142* | *1.34x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.00* | *157* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *157* | *0.00x* |
| libunord-stage2 | 0.001 | 0.003 | 0.06 | 157 | 0.01x |
| lib-stage2-short | 0.024 | 0.030 | 0.12 | 148 | 1.01x |
| lib-stage2-lean | 0.027 | 0.034 | 0.08 | 146 | 1.01x |
| lib-stage2 | 0.027 | 0.035 | 0.08 | 146 | 1.01x |
| lib-stage2-concat | 0.027 | 0.035 | 0.09 | 146 | 1.01x |
| lib-stage2-disp | 0.027 | 0.035 | 0.09 | 146 | 1.01x |
| lib-stage2-u4 | 0.028 | 0.039 | 0.08 | 145 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.029 | 0.045 | 0.07 | 146 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.029 | 0.045 | 0.10 | 146 | 1.00x |
| lib-stage1 | 0.030 | 0.047 | 0.08 | 146 | 1.01x |
| mut-odo-vecdims-add-in-leaf | 0.033 | 0.051 | 0.07 | 144 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.055 | 0.12 | 142 | 1.00x |
| liblist-stage2 | 0.040 | 0.046 | 0.19 | 142 | 2.01x |
| liblist-stage1 | 0.044 | 0.058 | 0.23 | 142 | 2.01x |
| libunord-stage1 | 0.045 | 0.061 | 0.22 | 142 | 2.03x |
| *mut-odo-vecdims-aa* | *0.046* | *0.067* | *0.05* | *137* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.047* | *0.067* | *0.05* | *137* | *1.00x* |
| mut-odo-vecdims-add-in | 0.047 | 0.067 | 0.12 | 137 | 1.00x |
| **mut-odo-vecdims** | **0.047** | 0.067 | 0.08 | 137 | 1.00x |
| canon-vecdims | 0.048 | 0.057 | 0.11 | 137 | 1.01x |
| mid-copy | 0.048 | 0.073 | 0.09 | 137 | 1.00x |
| bcast-set | 0.049 | 0.070 | 0.10 | 136 | 1.00x |
| canon-memcpy-r2 | 0.053 | 0.060 | 0.09 | 136 | 1.01x |
| canon-full | 0.055 | 0.064 | 0.06 | 135 | 1.01x |
| mut-flat-gm | 0.079 | 0.126 | 0.21 | 134 | 1.34x |
| *mut-odo-aa-adjacent* | *0.086* | *0.174* | *0.61* | *125* | *1.00x* |
| mut-odo | 0.087 | 0.179 | 0.09 | 125 | 1.00x |
| *mut-odo-aa-distant* | *0.087* | *0.178* | *0.10* | *125* | *1.00x* |
| *build-aa-adjacent* | *0.090* | *0.181* | *1.41* | *124* | *1.00x* |
| build | 0.091 | 0.179 | 0.27 | 124 | 1.00x |
| bq-expand-gm-mulback | 0.092 | 0.168 | 0.09 | 130 | 2.52x |
| bq-mut-runs-gm-mulback | 0.095 | 0.137 | 0.13 | 133 | 1.34x |
| *build-aa-distant* | *0.096* | *0.179* | *0.08* | *123* | *1.00x* |
| *bq-odo-gm-mulback-aa-distant* | *0.096* | *0.117* | *0.11* | *131* | *1.41x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.096* | *0.117* | *0.11* | *131* | *1.41x* |
| bq-odo-gm-mulback | 0.096 | 0.116 | 0.14 | 131 | 1.41x |
| **bq-scan-rem-gm-mulback** | **0.097** | 0.098 | 0.07 | 128 | 1.34x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.097* | *0.099* | *0.07* | *128* | *1.34x* |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.097* | *0.098* | *0.09* | *128* | *1.34x* |
| bq-expand | 0.101 | 0.176 | 0.12 | 128 | 2.52x |
| *bq-expand-aa-distant* | *0.101* | *0.176* | *0.09* | *128* | *2.52x* |
| *bq-expand-aa-adjacent* | *0.102* | *0.176* | *0.11* | *128* | *2.52x* |
| offtab-scan-rem | 0.129 | 0.130 | 0.06 | 124 | 2.00x |
| *list-aa-distant* | *1.000* | *1.002* | *0.19* | *86* | *23.43x* |
| *list-aa-adjacent* | *1.000* | *1.001* | *0.23* | *86* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 86 | 23.43x |
| gen-unsafe | 1.271 | 1.462 | 1.38 | 81 | 1.00x |
| *gen-unsafe-aa-distant* | *1.281* | *1.421* | *1.73* | *82* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.363* | *1.539* | *1.10* | *80* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0721, worst
cell 14.06% on `rev-primes`, and 13 of 16 intervals cover 1. The `sum-only`
halves agree at 0.9987 on a worst cell of 0.41% on `rev-gather48-src-50`,
its interval covering 1. The in-situ term reads 1.0059, 1.0190, 1.0023, 1.0155
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0701, which the correction amplifies
by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m14s, peak 96 MiB in use, 26 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the rev class. Anchor:
`rev-primes`, `list` at 4.15 ms per call raw, 4 ms net.

**Per shape, in the lead's order (rev-cnn-L1-24x24-c1, rev-gather48-src-50,
rev-primes):** `mut-odo-vecdims` 0.067/0.053/0.029 `bq-scan-rem-gm-mulback`
0.098/0.098/0.091

**Across the halves:** 21 of the 49 arms are faster on this half and 28 slower,
at a geomean of 1.0094, from `libunord-stage2` at 0.7887
to `mut-odo-vecdims-add-in-leaf-down` at 1.1695, with `list` itself at 0.9999.

**What the class says:** properties 1 and 3 hold for the fix --- `worst` 0.067
against a `list` it never loses to, and the tiers at 1.00x, 2.52x and 23.43x ---
and property 2 breaks outright to `libunord-stage2` at 0.001, **0.0136
of the fix on 3 of 3 shapes**, 98.6% against a 7.21% floor: the unordered
one-block test firing on every view of the class and collapsing it to a single
`VS.slice`, so the break prices dispatch and not filling, as on Run 22. What
the class adds is across the halves: every padded fill is faster
on the dead-spot half, by 1.4% (`lib-stage2-short`) to 2.9% (`-add-in-leaf-u2`)
and `-add-in-leaf-down` by 17%, while `mut-odo` is the arm the basis wins,
0.9770 at 3 of 3 with its adjacent twin at 0.9476 --- all of it inside the 7.21%
this class's basis floor carries, the widest of the nine and one pair's,
`gen-unsafe-aa-adjacent`, where the dead-spot half's own floor here is 2.50%.

**`revsome` --- a strict subset of axes reversed, so the signs are mixed.**
Shapes: `revsome-inner-primes` (`l` 250357, `sInner` 89), `revsome-outer-g48`
(`l` 22500, `sInner` 3), `revsome-mid-cnn-L2` (`l` 165888, `sInner` 3).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.19* | *90* | *2.52x* |
| *canon-full-nosum* | *--* | *--* | *0.07* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.30* | *93* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| libunord-stage2 | 0.000 | 0.001 | 0.01 | 116 | 0.00x |
| lib-stage2-short | 0.025 | 0.028 | 0.10 | 103 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.033 | 0.09 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.033 | 0.29 | 101 | 1.00x |
| lib-stage1 | 0.027 | 0.033 | 0.11 | 101 | 1.00x |
| lib-stage2-lean | 0.028 | 0.034 | 0.13 | 101 | 1.00x |
| lib-stage2-disp | 0.028 | 0.034 | 0.12 | 101 | 1.00x |
| lib-stage2-concat | 0.028 | 0.034 | 0.10 | 101 | 1.00x |
| lib-stage2 | 0.028 | 0.034 | 0.10 | 101 | 1.00x |
| lib-stage2-u4 | 0.029 | 0.038 | 0.11 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.032 | 0.037 | 0.11 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.036 | 0.043 | 0.10 | 98 | 1.00x |
| liblist-stage2 | 0.042 | 0.046 | 0.20 | 97 | 2.00x |
| liblist-stage1 | 0.042 | 0.045 | 0.21 | 98 | 2.00x |
| libunord-stage1 | 0.043 | 0.045 | 0.46 | 97 | 2.00x |
| mid-copy | 0.048 | 0.059 | 0.11 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.049* | *0.058* | *0.07* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.049* | *0.057* | *0.10* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.049** | 0.057 | 0.08 | 96 | 1.00x |
| mut-odo-vecdims-add-in | 0.050 | 0.057 | 0.12 | 96 | 1.00x |
| canon-vecdims | 0.052 | 0.057 | 0.11 | 96 | 1.00x |
| bcast-set | 0.053 | 0.061 | 0.06 | 96 | 1.00x |
| canon-memcpy-r2 | 0.055 | 0.060 | 0.11 | 96 | 1.00x |
| canon-full | 0.057 | 0.064 | 0.09 | 96 | 1.00x |
| mut-flat-gm | 0.080 | 0.091 | 0.11 | 88 | 1.33x |
| bq-mut-runs-gm-mulback | 0.089 | 0.098 | 0.18 | 87 | 1.33x |
| bq-expand-gm-mulback | 0.093 | 0.119 | 0.12 | 83 | 2.52x |
| *mut-odo-aa-distant* | *0.097* | *0.143* | *1.09* | *96* | *1.00x* |
| bq-expand | 0.100 | 0.129 | 0.14 | 83 | 2.52x |
| *bq-expand-aa-distant* | *0.101* | *0.130* | *0.13* | *83* | *2.52x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.101* | *0.103* | *0.14* | *86* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.101** | 0.103 | 0.11 | 86 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.101* | *0.102* | *0.12* | *86* | *1.33x* |
| mut-odo | 0.102 | 0.135 | 1.98 | 96 | 1.00x |
| *bq-expand-aa-adjacent* | *0.103* | *0.129* | *0.21* | *83* | *2.52x* |
| bq-odo-gm-mulback | 0.103 | 0.122 | 0.09 | 83 | 1.41x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.103* | *0.122* | *0.11* | *83* | *1.41x* |
| *bq-odo-gm-mulback-aa-distant* | *0.104* | *0.124* | *0.12* | *83* | *1.41x* |
| *mut-odo-aa-adjacent* | *0.105* | *0.146* | *1.88* | *96* | *1.00x* |
| *build-aa-distant* | *0.113* | *0.153* | *0.30* | *96* | *1.00x* |
| *build-aa-adjacent* | *0.115* | *0.151* | *0.43* | *96* | *1.00x* |
| build | 0.116 | 0.150 | 0.68 | 96 | 1.00x |
| offtab-scan-rem | 0.131 | 0.132 | 0.14 | 82 | 2.00x |
| *list-aa-adjacent* | *0.998* | *1.003* | *0.25* | *47* | *23.43x* |
| list (baseline) | 1.000 | 1.000 | 0.28 | 47 | 23.43x |
| *list-aa-distant* | *1.002* | *1.004* | *0.29* | *47* | *23.43x* |
| *gen-unsafe-aa-distant* | *1.278* | *1.558* | *0.84* | *43* | *1.00x* |
| *gen-unsafe-aa-adjacent* | *1.327* | *1.494* | *1.82* | *42* | *1.00x* |
| gen-unsafe | 1.335 | 1.505 | 1.44 | 42 | 1.00x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 0.9575, worst
cell 9.13% on `revsome-inner-primes`, and 10 of 16 intervals cover 1.
The `sum-only` halves agree at 0.9979 on a worst cell of 0.43%
on `revsome-outer-g48`, its interval covering 1. The in-situ term reads 1.0135,
1.0150, 1.0157, 1.0146 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9588, which
the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m16s, peak 115 MiB in use, 26 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the revsome class. Anchor:
`revsome-inner-primes`, `list` at 4.17 ms per call raw, 4.02 ms net.

**Per shape, in the lead's order (revsome-inner-primes, revsome-outer-g48,
revsome-mid-cnn-L2):** `mut-odo-vecdims` 0.030/0.053/0.057
`bq-scan-rem-gm-mulback` 0.103/0.101/0.099

**Across the halves:** 8 of the 49 arms are faster on this half and 41 slower,
at a geomean of 1.0339, from `mut-odo` at 0.9655 to `libunord-stage2` at 1.4101,
with `list` itself at 1.0092. **The baseline moved 0.92% between the halves,
past the 0.7% that lets two columns be differenced, so this line is NOT read
for the pair's variable.** The table above is one process's and stands; what
goes is the comparison.

**What the class says:** the same shape as `rev` and for the same reason ---
`libunord-stage2` at 0.000, **0.0091 of the fix on 3 of 3**, 99.1% against
a 4.25% floor, the one-block test firing on every view --- so property 2 breaks
to a degenerate cell and properties 1 and 3 hold, and stage one's test does
not fire, `libunord-stage1` tracking `liblist-stage1` inside the floor. Across
the halves the class reads as the main set does, only more so: 41 of 49 arms
are faster on the dead-spot half at a geomean of 1.0339, the padded fills
by 4.0% to 4.5%, `-add-in-leaf-down` by 19% and `build` and `gen-unsafe` by 11%
--- and `mut-odo` is again the arm the basis wins, 0.9655 at 3 of 3, past
the 1.96% the dead-spot half's own sixteen pairs span and inside the basis's
4.25% floor. `list` moved 0.92% between the halves, so the line above says
the pair is ordered here and not subtracted.

**`bcast` --- an innermost stride of 0, every run re-reading one element:
a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8),
`bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000,
`sInner` 2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.63* | *52* | *1.38x* |
| *canon-full-nosum* | *--* | *--* | *0.49* | *84* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.58* | *58* | *1.13x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.41* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-u4 | 0.019 | 0.027 | 0.56 | 61 | 1.00x |
| lib-stage2-lean | 0.019 | 0.027 | 0.50 | 61 | 1.00x |
| lib-stage2-disp | 0.019 | 0.027 | 0.51 | 61 | 1.00x |
| lib-stage2-short | 0.019 | 0.027 | 0.49 | 61 | 1.00x |
| lib-stage2-concat | 0.019 | 0.027 | 0.55 | 61 | 1.00x |
| lib-stage2 | 0.019 | 0.027 | 0.55 | 61 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.022 | 0.023 | 0.53 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.024 | 0.027 | 0.52 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.027 | 0.50 | 60 | 1.00x |
| lib-stage1 | 0.025 | 0.027 | 0.52 | 60 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.031 | 0.032 | 0.55 | 58 | 1.00x |
| bcast-set | 0.033 | 0.062 | 0.50 | 61 | 1.00x |
| canon-full | 0.033 | 0.062 | 0.55 | 61 | 1.00x |
| *mut-odo-vecdims-aa* | *0.035* | *0.063* | *0.51* | *60* | *1.00x* |
| **mut-odo-vecdims** | **0.035** | 0.063 | 0.45 | 60 | 1.00x |
| mut-odo-vecdims-add-in | 0.035 | 0.063 | 0.54 | 60 | 1.00x |
| mid-copy | 0.035 | 0.062 | 0.53 | 60 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.035* | *0.063* | *0.34* | *60* | *1.00x* |
| canon-vecdims | 0.036 | 0.062 | 0.55 | 60 | 1.00x |
| canon-memcpy-r2 | 0.037 | 0.067 | 0.59 | 60 | 1.00x |
| liblist-stage2 | 0.041 | 0.049 | 0.89 | 54 | 2.00x |
| libunord-stage2 | 0.041 | 0.049 | 0.84 | 54 | 2.00x |
| liblist-stage1 | 0.043 | 0.049 | 0.92 | 53 | 2.00x |
| libunord-stage1 | 0.044 | 0.050 | 0.92 | 53 | 2.00x |
| *mut-odo-aa-distant* | *0.059* | *0.155* | *1.15* | *60* | *1.00x* |
| mut-odo | 0.059 | 0.156 | 1.05 | 60 | 1.00x |
| *build-aa-adjacent* | *0.059* | *0.149* | *0.62* | *60* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.059* | *0.160* | *1.42* | *60* | *1.00x* |
| build | 0.059 | 0.149 | 1.57 | 60 | 1.00x |
| *build-aa-distant* | *0.062* | *0.171* | *0.96* | *60* | *1.00x* |
| mut-flat-gm | 0.066 | 0.071 | 0.68 | 49 | 1.13x |
| bq-mut-runs-gm-mulback | 0.079 | 0.089 | 0.69 | 47 | 1.13x |
| bq-expand-gm-mulback | 0.080 | 0.082 | 0.67 | 48 | 1.38x |
| bq-odo-gm-mulback | 0.083 | 0.088 | 0.69 | 47 | 1.14x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.083* | *0.088* | *0.79* | *47* | *1.14x* |
| *bq-odo-gm-mulback-aa-distant* | *0.083* | *0.088* | *0.40* | *47* | *1.14x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.091* | *0.100* | *1.00* | *47* | *1.13x* |
| bq-expand | 0.091 | 0.096 | 0.71 | 46 | 1.38x |
| *bq-expand-aa-distant* | *0.091* | *0.097* | *0.44* | *46* | *1.38x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.096* | *0.68* | *46* | *1.38x* |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.100 | 0.67 | 47 | 1.13x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.093* | *0.101* | *0.07* | *47* | *1.13x* |
| offtab-scan-rem | 0.127 | 0.143 | 1.02 | 43 | 2.00x |
| *gen-unsafe-aa-distant* | *0.981* | *1.074* | *4.29* | *21* | *1.00x* |
| *list-aa-distant* | *0.999* | *1.006* | *1.26* | *18* | *20.62x* |
| list (baseline) | 1.000 | 1.000 | 1.08 | 18 | 20.62x |
| *list-aa-adjacent* | *1.001* | *1.012* | *0.73* | *18* | *20.62x* |
| gen-unsafe | 1.026 | 1.035 | 3.26 | 21 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.101* | *1.132* | *1.32* | *21* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0587, worst
cell 9.31% on `bcast-inner8`, and 10 of 16 intervals cover 1. The `sum-only`
halves agree at 0.9991 on a worst cell of 0.38% on `bcast-inner900`,
its interval covering 1. The in-situ term reads 1.0140, 1.0120, 1.0209, 1.0220
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0567, which the correction amplifies
by 1.04x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m21s, peak 151 MiB in use, 45 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the bcast class. Anchor:
`bcast-inner900`, `list` at 28.3 ms per call raw, 27.2 ms net.

**Per shape, in the lead's order (bcast-inner8, bcast-inner900,
bcast-tall-Mx2):** `mut-odo-vecdims` 0.032/0.022/0.063 `bq-scan-rem-gm-mulback`
0.090/0.088/0.100

**Across the halves:** 10 of the 49 arms are faster on this half and 39 slower,
at a geomean of 1.0351, from `lib-stage2` at 0.9918
to `mut-odo-vecdims-add-in-leaf-down` at 1.3991, with `list` itself at 1.0041.

**What the class says:** property 2 breaks to a fill that is doing the work,
`lib-stage2-u4` at 0.019, **0.5993 of the fix on 3 of 3 shapes**, 40.1% against
a 5.87% floor --- Run 22's 0.5968 on this same binary --- and properties 1 and 3
hold, `bq-expand` at 1.38x. **And it is the one class where the dead-spot form
buys the padded fills nothing**: `lib-stage2` 0.9918, `-disp` 0.9937, `-short`
0.9949, `-lean` 0.9983 and `-concat` 1.0016 across the halves, every one inside
either floor, where the same arms move five percent on the main set ---
a broadcast re-reads one element per run and is bandwidth-bound, so a pad
in its dispatch is not on the path that costs. The arms that do move
are the ones whose pads sit in the per-run work: `lib-stage1` 1.1735, the two
`-u2` leaf arms at 1.1849 and 1.1888 and `-add-in-leaf-down` at 1.3991,
the dead-spot half faster on all of them. **This is also the population where
Run 22's registration 5 split**, `-down` leading `-u2` on the HEAD half;
on this pair `-u2` leads on both halves, 0.8041 on the basis and 0.9463
on the dead-spot half, the second past the 5.25% that half's own sixteen pairs
span, by an eighth of a point.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer
dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3),
`bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000,
`sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed
2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k`
is its worst, its block taken to 150000 elements where the class's others run 3
to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.40* | *70* | *1.57x* |
| *canon-full-nosum* | *--* | *--* | *0.60* | *104* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.78* | *75* | *1.17x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.28* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| lib-stage2-u4 | 0.017 | 0.033 | 0.48 | 80 | 1.00x |
| lib-stage2-lean | 0.017 | 0.033 | 0.32 | 80 | 1.00x |
| lib-stage2-disp | 0.017 | 0.033 | 0.35 | 80 | 1.00x |
| lib-stage2-concat | 0.017 | 0.033 | 0.33 | 80 | 1.00x |
| lib-stage2 | 0.017 | 0.033 | 0.43 | 80 | 1.00x |
| lib-stage2-short | 0.017 | 0.035 | 0.35 | 80 | 1.00x |
| mid-copy | 0.017 | 0.033 | 0.38 | 80 | 1.00x |
| canon-full | 0.018 | 0.033 | 0.36 | 80 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.022 | 0.032 | 0.33 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.032 | 0.32 | 79 | 1.00x |
| lib-stage1 | 0.022 | 0.032 | 0.31 | 79 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.023 | 0.037 | 0.33 | 78 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.028 | 0.042 | 0.58 | 76 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.057 | 0.33 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.057* | *0.32* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.057 | 0.29 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.058* | *0.30* | *76* | *1.00x* |
| canon-vecdims | 0.032 | 0.057 | 0.38 | 75 | 1.00x |
| liblist-stage2 | 0.032 | 0.048 | 0.55 | 74 | 2.00x |
| libunord-stage2 | 0.033 | 0.048 | 0.52 | 74 | 2.00x |
| bcast-set | 0.033 | 0.061 | 0.30 | 76 | 1.00x |
| canon-memcpy-r2 | 0.034 | 0.061 | 0.50 | 75 | 1.00x |
| liblist-stage1 | 0.038 | 0.043 | 0.60 | 74 | 2.00x |
| libunord-stage1 | 0.038 | 0.044 | 0.54 | 74 | 2.00x |
| *mut-odo-aa-adjacent* | *0.050* | *0.151* | *0.87* | *68* | *1.00x* |
| *mut-odo-aa-distant* | *0.051* | *0.150* | *1.03* | *68* | *1.00x* |
| *build-aa-distant* | *0.051* | *0.154* | *0.63* | *68* | *1.00x* |
| build | 0.052 | 0.153 | 0.99 | 68 | 1.00x |
| mut-odo | 0.052 | 0.155 | 0.64 | 68 | 1.00x |
| *build-aa-adjacent* | *0.053* | *0.168* | *1.53* | *68* | *1.00x* |
| mut-flat-gm | 0.063 | 0.090 | 0.65 | 68 | 1.17x |
| bq-mut-runs-gm-mulback | 0.073 | 0.101 | 0.62 | 66 | 1.17x |
| bq-expand-gm-mulback | 0.077 | 0.120 | 0.45 | 64 | 1.57x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.079* | *0.098* | *0.41* | *64* | *1.17x* |
| **bq-scan-rem-gm-mulback** | **0.080** | 0.100 | 0.63 | 64 | 1.17x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.080* | *0.099* | *0.26* | *64* | *1.17x* |
| bq-odo-gm-mulback | 0.080 | 0.123 | 0.58 | 64 | 1.17x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.080* | *0.124* | *0.42* | *64* | *1.17x* |
| *bq-odo-gm-mulback-aa-distant* | *0.080* | *0.124* | *0.35* | *64* | *1.17x* |
| bq-expand | 0.086 | 0.129 | 0.42 | 64 | 1.57x |
| *bq-expand-aa-adjacent* | *0.086* | *0.129* | *0.40* | *64* | *1.57x* |
| *bq-expand-aa-distant* | *0.086* | *0.131* | *0.36* | *64* | *1.57x* |
| offtab-scan-rem | 0.107 | 0.127 | 0.64 | 60 | 2.00x |
| *list-aa-distant* | *0.996* | *1.010* | *1.05* | *30* | *21.22x* |
| *list-aa-adjacent* | *0.999* | *1.006* | *1.12* | *30* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 1.33 | 29 | 21.22x |
| *gen-unsafe-aa-adjacent* | *1.001* | *1.485* | *2.01* | *28* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.010* | *1.518* | *2.53* | *28* | *1.00x* |
| gen-unsafe | 1.011 | 1.419 | 3.26 | 28 | 1.00x |

**Controls:** The largest A/A pair is `mut-odo-aa-adjacent` at 0.9723, worst
cell 8.38% on `bcastmid-b200k`, and 14 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0008 on a worst cell of 0.32% on `bcastmid-b200k`,
its interval covering 1. The in-situ term reads 1.0202, 1.0415, 1.0214, 1.0543
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 0.9782, which the correction amplifies
by 1.63x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h19m2s, peak 137 MiB in use, 38 MiB max residency;
the reader reads 55 benchmarks over 4 shapes of the bcastmid class. Anchor:
`bcastmid-b200k`, `list` at 47.6 ms per call raw, 46.5 ms net.

**Per shape, in the lead's order (bcastmid-c32-cnn, bcastmid-primes,
bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.057/0.021/0.036/0.023
`bq-scan-rem-gm-mulback` 0.100/0.087/0.069/0.067

**Across the halves:** 8 of the 49 arms are faster on this half and 41 slower,
at a geomean of 1.0201, from `canon-full` at 0.9712
to `mut-odo-vecdims-add-in-leaf-down` at 1.2272, with `list` itself at 1.0093.
**The baseline moved 0.93% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** `lib-stage2-u4` leads again at 0.017, **0.5266
of the fix on 4 of 4 shapes**, 47.3% against a 2.77% floor, Run 22's 0.5258
on this binary, and properties 1 and 3 hold. Across the halves the fills sit
within a point of each other --- `-short` 0.9992 to `lib-stage2` 1.0071 ---
with `lib-stage1` at 1.0124, the `-u2` arms at 1.0135 and 1.0190
and `-add-in-leaf-down` at 1.2272 the ones that move, as on `bcast` and
for the same reason. `list` moved 0.93% between the halves, so the line above
is ordered and not subtracted.

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
| *bq-expand-nosum* | *--* | *--* | *0.36* | *84* | *4.91x* |
| *canon-full-nosum* | *--* | *--* | *0.33* | *253* | *0.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.33* | *104* | *2.00x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *115* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *115* | *0.00x* |
| libunord-stage2 | 0.000 | 0.000 | 0.01 | 115 | 0.00x |
| lib-stage2-short | 0.000 | 0.015 | 0.05 | 110 | 0.00x |
| canon-full | 0.000 | 0.016 | 0.01 | 110 | 0.00x |
| lib-stage2-disp | 0.000 | 0.015 | 0.02 | 110 | 0.00x |
| lib-stage2-lean | 0.001 | 0.015 | 0.01 | 110 | 0.00x |
| lib-stage2-concat | 0.001 | 0.015 | 0.01 | 110 | 0.00x |
| lib-stage2-u4 | 0.001 | 0.014 | 0.01 | 110 | 0.00x |
| lib-stage2 | 0.001 | 0.016 | 0.01 | 110 | 0.00x |
| liblist-stage2 | 0.012 | 0.025 | 0.23 | 104 | 1.00x |
| canon-vecdims | 0.016 | 0.016 | 0.02 | 110 | 0.00x |
| canon-memcpy-r2 | 0.016 | 0.016 | 0.02 | 110 | 0.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.024 | 0.056 | 0.07 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.056 | 0.11 | 100 | 1.00x |
| lib-stage1 | 0.025 | 0.057 | 0.08 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.030 | 0.065 | 0.10 | 98 | 1.00x |
| bq-mut-runs-gm-mulback | 0.034 | 0.127 | 0.21 | 96 | 2.00x |
| mut-flat-gm | 0.034 | 0.127 | 0.36 | 96 | 2.00x |
| liblist-stage1 | 0.034 | 0.062 | 0.14 | 96 | 2.00x |
| libunord-stage1 | 0.035 | 0.063 | 0.24 | 96 | 2.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.039 | 0.068 | 0.34 | 96 | 1.00x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.049* | *0.137* | *0.16* | *92* | *2.26x* |
| bq-odo-gm-mulback | 0.050 | 0.139 | 0.16 | 92 | 2.26x |
| *bq-odo-gm-mulback-aa-distant* | *0.050* | *0.141* | *0.16* | *92* | *2.26x* |
| bq-expand-gm-mulback | 0.074 | 0.166 | 0.28 | 87 | 4.91x |
| **bq-scan-rem-gm-mulback** | **0.075** | 0.091 | 0.14 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.075* | *0.091* | *0.13* | *86* | *2.00x* |
| offtab-scan-rem | 0.075 | 0.091 | 0.14 | 86 | 2.00x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.075* | *0.092* | *0.10* | *86* | *2.00x* |
| *mut-odo-vecdims-aa-distant* | *0.093* | *0.108* | *0.13* | *82* | *1.00x* |
| mut-odo-vecdims-add-in | 0.094 | 0.109 | 0.07 | 82 | 1.00x |
| **mut-odo-vecdims** | **0.094** | 0.108 | 0.14 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.094* | *0.108* | *0.10* | *82* | *1.00x* |
| mid-copy | 0.095 | 0.116 | 0.24 | 82 | 1.00x |
| bcast-set | 0.095 | 0.106 | 0.13 | 82 | 1.00x |
| bq-expand | 0.115 | 0.199 | 0.32 | 80 | 4.91x |
| *bq-expand-aa-adjacent* | *0.116* | *0.201* | *0.30* | *80* | *4.91x* |
| *bq-expand-aa-distant* | *0.116* | *0.201* | *0.25* | *80* | *4.91x* |
| mut-odo | 0.247 | 0.314 | 0.62 | 66 | 1.00x |
| *mut-odo-aa-distant* | *0.250* | *0.319* | *1.64* | *66* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.260* | *0.317* | *1.58* | *66* | *1.00x* |
| *build-aa-distant* | *0.267* | *0.339* | *1.46* | *65* | *1.00x* |
| *build-aa-adjacent* | *0.268* | *0.318* | *1.79* | *65* | *1.00x* |
| build | 0.273 | 0.315 | 1.13 | 64 | 1.00x |
| gen-unsafe | 0.969 | 2.332 | 1.68 | 43 | 1.00x |
| *gen-unsafe-aa-distant* | *0.981* | *2.397* | *1.65* | *42* | *1.00x* |
| *list-aa-distant* | *0.997* | *1.000* | *0.29* | *41* | *32.29x* |
| *gen-unsafe-aa-adjacent* | *0.999* | *2.296* | *0.91* | *42* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 0.27 | 41 | 32.29x |
| *list-aa-adjacent* | *1.003* | *1.013* | *0.37* | *41* | *32.29x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-adjacent` at 1.0309, worst
cell 7.72% on `reshape1-500k`, and 15 of 16 intervals cover 1. The `sum-only`
halves agree at 1.0000 on a worst cell of 0.05% on `reshape1-rank10`,
its interval covering 1. The in-situ term reads 1.0128, 0.9995, 1.0478, 1.0977
of `sum-only` as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`,
`bq-expand`. Raw, that pair reads 1.0296, which the correction amplifies
by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h19m0s, peak 156 MiB in use, 37 MiB max residency;
the reader reads 55 benchmarks over 4 shapes of the reshape1 class. Anchor:
`reshape1-500k`, `list` at 13.2 ms per call raw, 12.9 ms net.

**Per shape, in the lead's order (reshape1-500k, reshape1-r3, reshape1-rank10,
reshape1-strided-r3):** `mut-odo-vecdims` 0.091/0.091/0.108/0.094
`bq-scan-rem-gm-mulback` 0.073/0.073/0.091/0.075

**Across the halves:** 17 of the 40 voting arms are faster on this half and 23
slower, at a geomean of 0.9985, from `libunord-stage2` at 0.3872
to `mut-odo-vecdims-add-in-leaf-down` at 1.2641, `canon-full`,
`canon-memcpy-r2`, `canon-vecdims`, `lib-stage2`, `lib-stage2-concat`,
`lib-stage2-disp`, `lib-stage2-lean`, `lib-stage2-short`, `lib-stage2-u4`
sitting out as degenerate, a basis cell of theirs not left positive
by the correction, with `list` itself at 1.0032.

**What the class says:** the class remains the one whose cells price dispatch
rather than filling --- the canonicalizing arms return O(1) on three of its four
shapes --- and property 2 breaks to `libunord-stage2` at 0.000, 0.0003
of the fix, that degeneracy compounded by the one-block test firing on every
view. Properties 1 and 3 hold, and property 3's `bq-expand` reads **4.91x**,
the top of the range across all nine classes. Eighteen cells sink below
the forcing pass on the basis, so nine rows are geomeans over 1 to 3 shapes of 4
and the whole `lib-stage2` family sits out the cross-half vote as degenerate.
**What the class does say about the pair is the run's one reversal**: the two
`-u2` leaf arms are SLOWER on the dead-spot half, `-u2` 0.9784 and `-u2-down`
0.9637, the basis faster on 4 of 4 shapes for both, with `mut-odo-aa-distant`
at 0.9560 beside them --- 3.6% at the widest, past the basis half's 3.09% floor
and inside the dead-spot half's 10.75%, which is the widest floor any
of the run's twenty processes carries and is one pair's, `build-aa-distant`
at 1.1075. Judged against the wider of the two floors, as [README's floor
section][floor] rules, it is a tie, and registration 3's first half a split
rather than a kill. Either way, this is the class where the form that removed
the fills' pads placed the two leaf loops the library ports on a cache-line
boundary --- `fbMutOdoVecdimsAddInLeafU2` and `-U2Down` are two of its four
straddlers --- and where that shows.

**`slice` --- a view of a larger source: non-zero offset, positive strides.**
Shapes: `slice-cnn-L2-24x24-c32` (`l` 165888, `sInner` 3), `slice-primes` (`l`
250357, `sInner` 89), `slice-coprime-r7` (`l` 60060, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *90* | *1.58x* |
| *canon-full-nosum* | *--* | *--* | *0.08* | *113* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.11* | *93* | *1.08x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *114* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *116* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *116* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.030 | 0.033 | 0.09 | 101 | 1.00x |
| lib-stage2-short | 0.030 | 0.032 | 0.09 | 101 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.030 | 0.033 | 0.09 | 101 | 1.00x |
| lib-stage2-u4 | 0.030 | 0.041 | 0.09 | 98 | 1.00x |
| lib-stage1 | 0.030 | 0.033 | 0.08 | 101 | 1.00x |
| lib-stage2-lean | 0.032 | 0.037 | 0.07 | 100 | 1.00x |
| lib-stage2 | 0.032 | 0.037 | 0.12 | 100 | 1.00x |
| lib-stage2-disp | 0.032 | 0.037 | 0.06 | 100 | 1.00x |
| lib-stage2-concat | 0.032 | 0.037 | 0.12 | 100 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.034 | 0.038 | 0.07 | 99 | 1.00x |
| mut-odo-vecdims-add-in-leaf-down | 0.039 | 0.044 | 0.10 | 97 | 1.00x |
| mut-odo-vecdims-add-in | 0.040 | 0.058 | 0.07 | 96 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.040* | *0.057* | *0.06* | *96* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.040* | *0.059* | *0.08* | *96* | *1.00x* |
| **mut-odo-vecdims** | **0.040** | 0.058 | 0.08 | 96 | 1.00x |
| mid-copy | 0.040 | 0.059 | 0.12 | 96 | 1.00x |
| canon-vecdims | 0.040 | 0.058 | 0.11 | 96 | 1.00x |
| canon-memcpy-r2 | 0.041 | 0.061 | 0.07 | 96 | 1.00x |
| bcast-set | 0.042 | 0.061 | 0.07 | 96 | 1.00x |
| canon-full | 0.042 | 0.065 | 0.08 | 96 | 1.00x |
| libunord-stage2 | 0.045 | 0.051 | 0.18 | 96 | 2.01x |
| liblist-stage1 | 0.045 | 0.049 | 0.17 | 96 | 2.00x |
| libunord-stage1 | 0.045 | 0.048 | 0.15 | 96 | 2.00x |
| liblist-stage2 | 0.045 | 0.050 | 0.19 | 96 | 2.00x |
| *mut-odo-aa-adjacent* | *0.065* | *0.143* | *1.34* | *96* | *1.00x* |
| mut-odo | 0.066 | 0.149 | 0.31 | 96 | 1.00x |
| *mut-odo-aa-distant* | *0.066* | *0.149* | *0.88* | *96* | *1.00x* |
| *build-aa-distant* | *0.067* | *0.151* | *1.26* | *96* | *1.00x* |
| *build-aa-adjacent* | *0.068* | *0.157* | *0.99* | *96* | *1.00x* |
| build | 0.069 | 0.160 | 0.78 | 96 | 1.00x |
| mut-flat-gm | 0.084 | 0.089 | 0.13 | 88 | 1.08x |
| bq-mut-runs-gm-mulback | 0.094 | 0.097 | 0.11 | 86 | 1.08x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.099* | *0.104* | *0.07* | *86* | *1.08x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.100* | *0.104* | *0.12* | *86* | *1.08x* |
| **bq-scan-rem-gm-mulback** | **0.100** | 0.104 | 0.11 | 86 | 1.08x |
| bq-expand-gm-mulback | 0.104 | 0.121 | 0.09 | 83 | 1.58x |
| *bq-odo-gm-mulback-aa-distant* | *0.110* | *0.123* | *0.15* | *83* | *1.50x* |
| *bq-odo-gm-mulback-aa-adjacent* | *0.110* | *0.123* | *0.10* | *83* | *1.50x* |
| bq-odo-gm-mulback | 0.111 | 0.123 | 0.10 | 83 | 1.50x |
| *bq-expand-aa-distant* | *0.111* | *0.129* | *0.10* | *83* | *1.58x* |
| *bq-expand-aa-adjacent* | *0.111* | *0.130* | *0.15* | *83* | *1.58x* |
| bq-expand | 0.111 | 0.130 | 0.10 | 83 | 1.58x |
| offtab-scan-rem | 0.132 | 0.133 | 0.12 | 82 | 2.00x |
| list (baseline) | 1.000 | 1.000 | 0.19 | 46 | 20.54x |
| *list-aa-adjacent* | *1.000* | *1.009* | *0.21* | *46* | *20.54x* |
| *list-aa-distant* | *1.000* | *1.005* | *0.26* | *46* | *20.54x* |
| *gen-unsafe-aa-adjacent* | *1.594* | *2.662* | *2.04* | *43* | *1.00x* |
| gen-unsafe | 1.604 | 2.600 | 1.57 | 43 | 1.00x |
| *gen-unsafe-aa-distant* | *1.631* | *2.516* | *2.29* | *41* | *1.00x* |

**Controls:** The largest A/A pair is `build-aa-distant` at 0.9689, worst cell
5.54% on `slice-cnn-L2-24x24-c32`, and 14 of 16 intervals cover 1.
The `sum-only` halves agree at 0.9993 on a worst cell of 0.31%
on `slice-coprime-r7`, its interval covering 1. The in-situ term reads 1.0176,
1.0174, 1.0192, 1.0404 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 0.9762, which
the correction amplifies by 1.55x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m16s, peak 123 MiB in use, 38 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the slice class. Anchor:
`slice-primes`, `list` at 4.14 ms per call raw, 3.98 ms net.

**Per shape, in the lead's order (slice-cnn-L2-24x24-c32, slice-primes,
slice-coprime-r7):** `mut-odo-vecdims` 0.058/0.030/0.036
`bq-scan-rem-gm-mulback` 0.100/0.104/0.095

**Across the halves:** 5 of the 49 arms are faster on this half and 44 slower,
at a geomean of 1.0258, from `bcast-set` at 0.9876
to `mut-odo-vecdims-add-in-leaf-down` at 1.1729, with `list` itself at 1.0038.

**What the class says:** the table's head is a `mut-odo-vecdims` sibling,
`-add-in-leaf-u2-down` at 0.030, **0.7526 of the fix on 3 of 3 shapes**, 24.7%
against a 3.11% floor, so by the claims' own reading property 2's first clause
does not break here --- the best arm OUTSIDE the family is `lib-stage2-short`,
level with it at 0.030, where Run 22 read the candidate ahead by a thousandth
on this same binary. Properties 1 and 3 hold. Across the halves this
is the class the pads cost most evenly: 44 of 49 arms are faster
on the dead-spot half at a geomean of 1.0258, the `lib-stage2` family by 5.6%
to 6.6%, `lib-stage1` by 3.3% and the two `-u2` arms by 3.2% and 3.9%, all past
the basis half's 3.11% floor; the dead-spot half's own is 6.47%, which only
`-lean` at 6.6%, `gen-unsafe` at 12% with its distant twin at 7.8%,
and `-add-in-leaf-down` at 17% clear. Registration 1's ratio, `lib-stage2` /
`lib-stage1`, reads 1.0409 on the basis and 1.0120 on the dead-spot half ---
the one population Run 22 read the branch behind past its floor, inside its 1.10
kill on both.

**`window` --- overlapping im2col patches: the workload the README opens
by naming, with the overlap the main set's bijective map drops.** Shapes:
`window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556,
`sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *116* | *2.81x* |
| *canon-full-nosum* | *--* | *--* | *0.15* | *153* | *1.01x* |
| *mut-flat-gm-nosum* | *--* | *--* | *1.07* | *134* | *1.33x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *120* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *150* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *150* | *0.00x* |
| lib-stage2-short | 0.020 | 0.027 | 0.15 | 140 | 1.01x |
| lib-stage2-u4 | 0.022 | 0.037 | 0.14 | 141 | 1.01x |
| lib-stage2-lean | 0.024 | 0.033 | 0.11 | 140 | 1.00x |
| lib-stage2-disp | 0.024 | 0.033 | 0.12 | 140 | 1.01x |
| lib-stage2 | 0.024 | 0.033 | 0.11 | 140 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.029 | 0.031 | 0.09 | 133 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.029 | 0.031 | 0.11 | 133 | 1.00x |
| lib-stage1 | 0.030 | 0.031 | 0.15 | 133 | 1.01x |
| mut-odo-vecdims-add-in-leaf | 0.033 | 0.037 | 0.08 | 130 | 1.00x |
| canon-vecdims | 0.038 | 0.058 | 0.08 | 137 | 1.01x |
| canon-memcpy-r2 | 0.038 | 0.060 | 1.04 | 137 | 1.01x |
| lib-stage2-concat | 0.038 | 0.150 | 0.16 | 109 | 1.02x |
| canon-full | 0.039 | 0.063 | 0.20 | 137 | 1.01x |
| liblist-stage1 | 0.039 | 0.043 | 0.33 | 129 | 2.01x |
| mut-odo-vecdims-add-in-leaf-down | 0.039 | 0.042 | 0.07 | 129 | 1.00x |
| libunord-stage1 | 0.040 | 0.043 | 0.28 | 129 | 2.02x |
| libunord-stage2 | 0.048 | 0.096 | 0.23 | 116 | 2.05x |
| liblist-stage2 | 0.051 | 0.096 | 0.20 | 116 | 2.02x |
| mut-odo-vecdims-add-in | 0.061 | 0.097 | 0.11 | 116 | 1.00x |
| *mut-odo-vecdims-aa* | *0.062* | *0.097* | *0.08* | *116* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.097* | *0.05* | *116* | *1.00x* |
| **mut-odo-vecdims** | **0.062** | 0.098 | 0.09 | 116 | 1.00x |
| mid-copy | 0.064 | 0.103 | 0.20 | 115 | 1.00x |
| bcast-set | 0.066 | 0.104 | 0.07 | 115 | 1.00x |
| mut-flat-gm | 0.069 | 0.087 | 0.48 | 126 | 1.33x |
| bq-mut-runs-gm-mulback | 0.078 | 0.096 | 0.36 | 127 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.091* | *0.097* | *0.08* | *120* | *1.33x* |
| **bq-scan-rem-gm-mulback** | **0.093** | 0.095 | 0.07 | 120 | 1.33x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.093* | *0.095* | *0.07* | *120* | *1.33x* |
| *bq-odo-gm-mulback-aa-distant* | *0.093* | *0.119* | *0.16* | *121* | *2.55x* |
| bq-odo-gm-mulback | 0.094 | 0.120 | 0.20 | 121 | 2.55x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.094* | *0.120* | *0.13* | *121* | *2.55x* |
| bq-expand-gm-mulback | 0.099 | 0.117 | 0.14 | 119 | 2.81x |
| offtab-scan-rem | 0.115 | 0.125 | 0.11 | 120 | 2.00x |
| bq-expand | 0.120 | 0.127 | 0.12 | 112 | 2.81x |
| *bq-expand-aa-distant* | *0.120* | *0.128* | *0.21* | *112* | *2.81x* |
| *bq-expand-aa-adjacent* | *0.120* | *0.127* | *0.12* | *112* | *2.81x* |
| *mut-odo-aa-adjacent* | *0.151* | *0.250* | *1.70* | *99* | *1.00x* |
| mut-odo | 0.152 | 0.260 | 1.08 | 99 | 1.00x |
| *mut-odo-aa-distant* | *0.155* | *0.258* | *1.75* | *99* | *1.00x* |
| *build-aa-adjacent* | *0.162* | *0.295* | *1.17* | *96* | *1.00x* |
| build | 0.163 | 0.294 | 0.78 | 96 | 1.00x |
| *build-aa-distant* | *0.166* | *0.291* | *2.28* | *97* | *1.00x* |
| *list-aa-distant* | *0.990* | *1.010* | *0.30* | *73* | *24.76x* |
| list (baseline) | 1.000 | 1.000 | 0.55 | 73 | 24.76x |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.59* | *73* | *24.76x* |
| gen-unsafe | 1.102 | 1.286 | 2.05 | 75 | 1.00x |
| *gen-unsafe-aa-adjacent* | *1.115* | *1.278* | *2.08* | *74* | *1.00x* |
| *gen-unsafe-aa-distant* | *1.151* | *1.280* | *1.52* | *73* | *1.00x* |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0450, worst
cell 7.37% on `window-64x64-k1x9`, and 14 of 16 intervals cover 1.
The `sum-only` halves agree at 1.0014 on a worst cell of 0.38%
on `window-64x64-k1x9`, its interval covering 1. The in-situ term reads 1.0226,
1.0080, 1.0088, 1.0399 of `sum-only` as medians, on `mut-odo-vecdims`,
`canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair reads 1.0439, which
the correction amplifies by 1.02x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m16s, peak 105 MiB in use, 24 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the window class. Anchor:
`window-224x224-k3`, `list` at 9.57 ms per call raw, 9.29 ms net.

**Per shape, in the lead's order (window-28x28-k5, window-224x224-k3,
window-64x64-k1x9):** `mut-odo-vecdims` 0.044/0.056/0.098
`bq-scan-rem-gm-mulback` 0.094/0.095/0.075

**Across the halves:** 13 of the 49 arms are faster on this half and 36 slower,
at a geomean of 1.0270, from `mut-odo` at 0.9351
to `mut-odo-vecdims-add-in-leaf-down` at 1.2207, with `list` itself at 1.0061.

**What the class says:** `lib-stage2-short` leads at 0.020, **0.3282 of the fix
on 3 of 3 shapes**, 67.2% against a 4.50% floor, Run 22's 0.3291 on this binary
and again the widest property-2 break of any non-degenerate class. Properties 1
and 3 hold. **Across the halves it is `mut-odo` that moves most, and the wrong
way for the pair's story**: 0.9351 at 3 of 3, the basis faster by 6.5%, past
the basis's 4.50% floor and inside the dead-spot half's 7.43%, its adjacent twin
at 0.9609 with it, while the `lib-stage2` family and `lib-stage1` go 3.4% to 10%
the other way, the `-u2` arms 2.7% and 3.7%, and `-add-in-leaf-down` 22%.
The arm's own loop sits at offset 0 on both halves, named off the twins, so what
moved it is not its head.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated
view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1`
(`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one
strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *119* | *1.14x* |
| *canon-full-nosum* | *--* | *--* | *0.13* | *144* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.10* | *125* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *144* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.027 | 0.034 | 0.07 | 127 | 1.00x |
| lib-stage1 | 0.027 | 0.035 | 0.08 | 126 | 1.00x |
| lib-stage2-u4 | 0.027 | 0.035 | 0.16 | 127 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.034 | 0.08 | 126 | 1.00x |
| lib-stage2-lean | 0.028 | 0.035 | 0.09 | 126 | 1.00x |
| lib-stage2-short | 0.028 | 0.035 | 0.10 | 126 | 1.00x |
| lib-stage2-disp | 0.028 | 0.035 | 0.11 | 126 | 1.00x |
| lib-stage2-concat | 0.028 | 0.035 | 0.09 | 126 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.028 | 0.033 | 0.08 | 126 | 1.00x |
| lib-stage2 | 0.028 | 0.035 | 0.13 | 126 | 1.00x |
| canon-vecdims | 0.031 | 0.033 | 0.06 | 126 | 1.00x |
| canon-full | 0.031 | 0.033 | 0.10 | 126 | 1.00x |
| canon-memcpy-r2 | 0.031 | 0.033 | 0.09 | 126 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.032* | *0.033* | *0.08* | *126* | *1.00x* |
| **mut-odo-vecdims** | **0.032** | 0.033 | 0.10 | 126 | 1.00x |
| mut-odo-vecdims-add-in | 0.032 | 0.033 | 0.06 | 126 | 1.00x |
| *mut-odo-vecdims-aa* | *0.032* | *0.033* | *0.08* | *126* | *1.00x* |
| mid-copy | 0.032 | 0.033 | 0.07 | 126 | 1.00x |
| bcast-set | 0.033 | 0.036 | 0.08 | 126 | 1.00x |
| mut-odo | 0.033 | 0.049 | 0.14 | 125 | 1.00x |
| *mut-odo-aa-adjacent* | *0.033* | *0.050* | *0.17* | *125* | *1.00x* |
| *mut-odo-aa-distant* | *0.033* | *0.050* | *0.10* | *125* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.034 | 0.08 | 124 | 1.00x |
| build | 0.034 | 0.052 | 0.18 | 124 | 1.00x |
| *build-aa-distant* | *0.034* | *0.050* | *0.26* | *124* | *1.00x* |
| *build-aa-adjacent* | *0.035* | *0.051* | *0.42* | *124* | *1.00x* |
| libunord-stage1 | 0.047 | 0.062 | 0.14 | 122 | 2.01x |
| liblist-stage2 | 0.047 | 0.063 | 0.22 | 122 | 2.00x |
| libunord-stage2 | 0.047 | 0.063 | 0.19 | 122 | 2.01x |
| liblist-stage1 | 0.048 | 0.063 | 0.17 | 122 | 2.00x |
| mut-flat-gm | 0.072 | 0.072 | 0.10 | 116 | 1.03x |
| bq-mut-runs-gm-mulback | 0.082 | 0.082 | 0.08 | 114 | 1.03x |
| bq-expand-gm-mulback | 0.085 | 0.087 | 0.07 | 114 | 1.14x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.091* | *0.092* | *0.05* | *113* | *1.04x* |
| bq-odo-gm-mulback | 0.091 | 0.092 | 0.05 | 113 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.091* | *0.092* | *0.09* | *113* | *1.04x* |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.092* | *0.094* | *0.05* | *112* | *1.04x* |
| **bq-scan-rem-gm-mulback** | **0.092** | 0.094 | 0.05 | 112 | 1.04x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.093* | *0.095* | *0.06* | *112* | *1.04x* |
| *bq-expand-aa-distant* | *0.097* | *0.099* | *0.06* | *112* | *1.14x* |
| bq-expand | 0.097 | 0.099 | 0.08 | 112 | 1.14x |
| *bq-expand-aa-adjacent* | *0.097* | *0.098* | *0.08* | *112* | *1.14x* |
| offtab-scan-rem | 0.127 | 0.135 | 0.09 | 108 | 2.00x |
| *gen-unsafe-aa-adjacent* | *0.945* | *1.898* | *0.96* | *69* | *1.00x* |
| gen-unsafe | 0.949 | 1.924 | 3.44 | 68 | 1.00x |
| *gen-unsafe-aa-distant* | *0.968* | *1.984* | *1.08* | *68* | *1.00x* |
| *list-aa-distant* | *0.992* | *1.001* | *0.27* | *71* | *19.43x* |
| *list-aa-adjacent* | *1.000* | *1.007* | *0.15* | *71* | *19.43x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 71 | 19.43x |

**Controls:** The largest A/A pair is `gen-unsafe-aa-distant` at 1.0199, worst
cell 3.15% on `scaled-r5`, and 15 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9999 on a worst cell of 0.40% on `scaled-r5`, its interval
covering 1. The in-situ term reads 1.0272, 1.0230, 1.0012, 1.0140 of `sum-only`
as medians, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw,
that pair reads 1.0189, which the correction amplifies by 1.05x --- quote both
wherever that is past 1.5.

**Provenance:** elapsed 0h14m17s, peak 121 MiB in use, 52 MiB max residency;
the reader reads 55 benchmarks over 3 shapes of the scaled class. Anchor:
`scaled-rank1-m1`, `list` at 4.89 ms per call raw, 4.71 ms net.

**Per shape, in the lead's order (scaled-super-r3, scaled-rank1-m1,
scaled-r5):** `mut-odo-vecdims` 0.028/0.033/0.033 `bq-scan-rem-gm-mulback`
0.092/0.091/0.094

**Across the halves:** 23 of the 49 arms are faster on this half and 26 slower,
at a geomean of 1.0151, from `mut-odo` at 0.9636
to `mut-odo-vecdims-add-in-leaf-down` at 1.1343, with `list` itself at 0.9974.

**What the class says:** the tightest break of the nine, and to a sibling:
`-add-in-leaf-u2-down` leads at 0.027, **0.9060 of the fix on 2 of 3 shapes
at sign p 1**, 9.4% against a 1.99% floor, with `lib-stage1` the best arm
outside the family level with it at 0.027 --- where Run 22 read `lib-stage2-u4`
ahead of the sibling by a thousandth and of `lib-stage1` by three on this same
binary --- so property 2's first clause holds by the claims' own reading
and the fix's `worst` here, 0.033, is the tightest of the ten populations.
Properties 1 and 3 hold, `bq-expand` at 1.14x, the bottom of the range. Across
the halves `mut-odo` is slower on the dead-spot half by 3.6% at 3 of 3, past
the basis's 1.99% floor and the dead-spot half's own 2.46%,
and `mut-odo-vecdims`, its twins, `-add-in` and `-add-in-leaf` with it by 0.6%
to 2.0%, while the `lib-stage2` family gains 1.9% to 3.4%, `lib-stage1` 3.7%
and the three other leaf arms 2.5% to 13%; the population where the registration
expected `-down` to catch `-u2` reads `-u2` ahead on both halves, 0.8484
and 0.9295, the second past the 2.46% the dead-spot half's own pairs span,
threefold.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1
throughout: regime 2, which the library reaches by a route of its own,
and the population the rework's question needed --- extended on Run 22
from seven views to eleven.** Shapes: `runs-2` (`l` 1800000, `sInner` 2),
`runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000,
`sInner` 4 --- landed on Run 22, and the first view in the suite
with a canonical innermost extent of 4, the branch the short-body fills take
and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000,
`sInner` 5 --- landed on Run 22, beside it), `runs-9` (`l` 1800000, `sInner` 9
--- the window probe's run), `runs-96` (`l` 1800000, `sInner` 96 --- an image
row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22,
and the dispatch threshold's own cell, `>= dispRun` firing exactly here),
`runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun`
within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-65536`
(`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000,
`sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l`
of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.50* | *52* | *1.15x* |
| *canon-full-nosum* | *--* | *--* | *0.54* | *76* | *1.00x* |
| *mut-flat-gm-nosum* | *--* | *--* | *0.32* | *57* | *1.03x* |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *76* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage2-short | 0.027 | 0.029 | 0.29 | 58 | 1.00x |
| lib-stage2-u4 | 0.028 | 0.031 | 0.32 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.030 | 0.13 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2-down | 0.028 | 0.030 | 0.33 | 58 | 1.00x |
| mut-odo-vecdims-add-in-leaf | 0.029 | 0.031 | 0.11 | 58 | 1.00x |
| lib-stage2 | 0.029 | 0.031 | 0.31 | 58 | 1.00x |
| lib-stage2-lean | 0.029 | 0.032 | 0.35 | 58 | 1.00x |
| lib-stage2-disp | 0.029 | 0.038 | 0.32 | 58 | 1.00x |
| canon-vecdims | 0.031 | 0.063 | 0.46 | 58 | 1.00x |
| mid-copy | 0.033 | 0.063 | 0.44 | 58 | 1.00x |
| mut-odo-vecdims-add-in | 0.033 | 0.064 | 0.11 | 58 | 1.00x |
| **mut-odo-vecdims** | **0.033** | 0.064 | 0.07 | 58 | 1.00x |
| *mut-odo-vecdims-aa* | *0.033* | *0.064* | *0.08* | *58* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.033* | *0.065* | *0.06* | *58* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-down | 0.034 | 0.035 | 0.05 | 57 | 1.00x |
| canon-full | 0.035 | 0.102 | 0.58 | 58 | 1.00x |
| canon-memcpy-r2 | 0.035 | 0.092 | 0.44 | 58 | 1.00x |
| bcast-set | 0.037 | 0.068 | 0.45 | 58 | 1.00x |
| build | 0.044 | 0.147 | 0.48 | 57 | 1.00x |
| *build-aa-adjacent* | *0.044* | *0.154* | *0.83* | *57* | *1.00x* |
| *build-aa-distant* | *0.046* | *0.158* | *0.37* | *57* | *1.00x* |
| *mut-odo-aa-adjacent* | *0.048* | *0.150* | *0.18* | *57* | *1.00x* |
| *mut-odo-aa-distant* | *0.048* | *0.155* | *0.10* | *57* | *1.00x* |
| mut-odo | 0.049 | 0.163 | 0.30 | 57 | 1.00x |
| mut-flat-gm | 0.072 | 0.079 | 0.39 | 49 | 1.03x |
| bq-mut-runs-gm-mulback | 0.083 | 0.092 | 0.55 | 47 | 1.03x |
| bq-expand-gm-mulback | 0.084 | 0.090 | 0.54 | 47 | 1.15x |
| *bq-odo-gm-mulback-aa-adjacent* | *0.088* | *0.096* | *0.56* | *47* | *1.04x* |
| bq-odo-gm-mulback | 0.088 | 0.097 | 0.55 | 46 | 1.04x |
| *bq-odo-gm-mulback-aa-distant* | *0.088* | *0.093* | *0.04* | *47* | *1.04x* |
| liblist-stage2 | 0.091 | 1.167 | 0.52 | 55 | 1.21x |
| libunord-stage2 | 0.092 | 1.161 | 0.53 | 55 | 1.21x |
| *bq-scan-rem-gm-mulback-aa-adjacent* | *0.095* | *0.103* | *0.53* | *46* | *1.03x* |
| **bq-scan-rem-gm-mulback** | **0.095** | 0.103 | 0.54 | 46 | 1.03x |
| *bq-scan-rem-gm-mulback-aa-distant* | *0.096* | *0.104* | *0.04* | *46* | *1.03x* |
| bq-expand | 0.096 | 0.102 | 0.56 | 45 | 1.15x |
| *bq-expand-aa-adjacent* | *0.096* | *0.102* | *0.58* | *45* | *1.15x* |
| *bq-expand-aa-distant* | *0.097* | *0.103* | *0.02* | *45* | *1.15x* |
| lib-stage1 | 0.136 | 1.333 | 0.54 | 53 | 1.28x |
| offtab-scan-rem | 0.137 | 0.152 | 0.68 | 41 | 2.00x |
| lib-stage2-concat | 0.137 | 1.350 | 0.64 | 52 | 1.31x |
| liblist-stage1 | 0.137 | 1.354 | 0.56 | 53 | 1.28x |
| libunord-stage1 | 0.138 | 1.362 | 0.48 | 53 | 1.28x |
| *gen-unsafe-aa-adjacent* | *0.718* | *1.053* | *2.30* | *21* | *1.00x* |
| *gen-unsafe-aa-distant* | *0.719* | *1.127* | *3.36* | *21* | *1.00x* |
| gen-unsafe | 0.734 | 1.110 | 1.99 | 21 | 1.00x |
| list (baseline) | 1.000 | 1.000 | 2.71 | 17 | 19.43x |
| *list-aa-distant* | *1.019* | *1.041* | *2.00* | *17* | *19.43x* |
| *list-aa-adjacent* | *1.035* | *1.048* | *0.26* | *18* | *19.43x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0345, worst cell
4.85% on `runs-r3-48x30`, and 9 of 16 intervals cover 1. The `sum-only` halves
agree at 0.9998 on a worst cell of 0.39% on `runs-9`, its interval covering 1.
The in-situ term reads 1.0305, 1.0288, 1.0275, 1.0311 of `sum-only` as medians,
on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm`, `bq-expand`. Raw, that pair
reads 1.0332, which the correction amplifies by 1.04x --- quote both wherever
that is past 1.5.

**Provenance:** elapsed 0h52m26s, peak 494 MiB in use, 208 MiB max residency;
the reader reads 55 benchmarks over 11 shapes of the runs class. Anchor:
`runs-2`, `list` at 38.2 ms per call raw, 37.1 ms net.

**Per shape, in the lead's order (runs-2, runs-3, runs-4, runs-5, runs-9,
runs-96, runs-256, runs-512, runs-1024, runs-65536, runs-r3-48x30):**
`mut-odo-vecdims`
0.064/0.052/0.045/0.043/0.034/0.028/0.028/0.028/0.028/0.028/0.030
`bq-scan-rem-gm-mulback`
0.103/0.098/0.098/0.096/0.093/0.092/0.091/0.093/0.093/0.098/0.094

**Across the halves:** 11 of the 49 arms are faster on this half and 38 slower,
at a geomean of 1.0217, from `bq-odo-gm-mulback-aa-adjacent` at 0.9758
to `mut-odo-vecdims-add-in-leaf-down` at 1.1474, with `list` itself at 0.9894.
**The baseline moved 1.06% between the halves, past the 0.7% that lets two
columns be differenced, so this line is NOT read for the pair's variable.**
The table above is one process's and stands; what goes is the comparison.

**What the class says:** `lib-stage2-short` leads at 0.027, **0.7654 of the fix
on 6 of 11 shapes, sign p 1**, 23.5% against a 3.45% floor by the geomean
and a coin flip by the sign test, the win being the short lengths' alone.
Properties 1 and 3 hold for the fix; property 1 does NOT hold for six
of the eleven library-shaped arms, all at `runs-2` on both halves, the claims
section naming them. **The crossover stands where Run 22 put it, on this same
binary**: `lib-stage2` / `lib-stage1` runs 0.0229, 0.0275, 0.0395, 0.0442,
0.0839, 0.5241, 0.7530, 0.8411, 0.9478, 1.2607 and 1.0323 across `runs-2`, `-3`,
`-4`, `-5`, `-9`, `-96`, `-256`, `-512`, `-1024`, `-65536` and `-r3-48x30`
on the basis, so the branch is the better route through `runs-1024` and behind
at the two longest --- Run 22's 0.9254 at `runs-1024` and 1.1485 at `runs-65536`
having drifted to 0.9478 and 1.2607 on one binary, which is how far a long-run
cell moves between two evenings --- and 0.0209 to 1.1408 on the dead-spot half.
**And the dispatch is still killed on both halves**: `lib-stage2-disp` is 5.75%
behind stage two at `runs-1024` on the basis and 6.24% on the dead-spot half,
past the basis's 3.45% floor and the dead-spot half's own 3.46%, and 33.6%
and 18.4% behind at `runs-256` and `runs-512`. **Registration 3's second half
dies here**: the dead-spot margin on `lib-stage2`, dead-spot over basis
as the registration reads it, runs 0.9077, 0.9863, 0.8819, 0.9650, 0.9335,
0.9871, 0.9800, 0.9637, 0.9841 and 0.8954 from `runs-2` to `runs-65536`, widest
at `runs-4` and second widest at the longest run, ordering with nothing. `list`
moved 1.06% between the halves, so the cross-half line is ordered
and not subtracted; and the process's worst A/A cell, 39.51%
on `runs-65536/bq-odo-gm-mulback-aa-adjacent` on the dead-spot half, is a level
and not a step, `--steps` finding none past 2%.



## Provenance

What this run's figures have to be read against, and it is a section
of this file because a run replaces every word of it. What does NOT move
with a run --- the delta chain that says which shape set and roster each run
measured, and the list of what a run replaces outside this file --- is [README's
own Provenance][prov].

**Run 23's halves differ in where the shim places its pads, and in nothing else
at all.** One source, `Main.hs` at `125534d`, one shim, `align-as.py`
at `38bb3bb`, one compiler, ghc-9.12.4, the default on PATH here, and one store,
through the default project file and freeze, built twice: the basis
under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1`, which is Run 22's basis recipe,
and the other half under the same two with `LOOP_DEADSPOT=1` added, under which
`rewrite()` returns through `plan_dead()` before either of the other two is read
--- so the two command lines differ in one added variable and the binaries
in one shim behaviour: every pad goes after an unconditional `jmp` where no path
executes it, and the containment test orders the heads of a group instead
of skipping one. Both carry `-fspec-constr -fobject-determinism`,
`LOOP_NOOVERLAP` unset, and both ran under `WILDLOG=1 SATURATE=1`. What the pair
prices is a layout change over the whole roster: the first pair since Run 17
whose halves share a compiler, and the first here whose halves are one
compiler's code differing only in where the bytes landed.

**The sequence was launched once and ran to the end in one window**,
2026-09-01T23:55:28 to 2026-09-02T09:35:21, twenty processes, every one exiting
0 at the count its roster holds --- 1320 twice, 605 twice, 220 four times
and 165 twelve times --- each carrying its one `@@saturate` line
and its `@@wild` stamps, and the driver recording no complaint. The dead-spot
half ran first throughout, `spot` before `g912` on the main set and on each
class in turn, which is the driver's order. The plateau gate reads every
process's preamble victim inside **19.7302 to 20.6446 ms/iter, a 4.63% spread**
against the 5% band, where Run 22 read 2.60%. **One thing happened
on the machine during the window and it is disclosed rather than rerun**:
a Claude Code update installed itself at 00:42:01, forty-seven minutes
into `run23-spot-main`. The per-sample instrument's foreign-CPU column, read
over all 1320 benches of that process, puts 2 benches at or above 0.25 ---
`cnn-L1-6x6-c1/gen-unsafe` at 0.74 and its adjacent twin at 0.71, the first
shape of the process at 23:55, ninety seconds after the gate's last process
ended and while this session read the gate and checked the launch, and nothing
to do with the update --- and nothing past 0.25 anywhere near 00:42; the basis
main set peaks at 0.18. No population was rerun, at the request of whoever asked
for the run, so that the machine could be handed back; what the two intruded
cells touch is the dead-spot half's `gen-unsafe` row, which the last section
already reads as not reproducing task 6's figure for reasons of its own.
Post-run step 3 would have owed both main sets a rerun by the letter,
and was declined.

**The pair's own identity, transcribed before its note goes with it.** The two
binaries are `run23-g912`, md5 `9bac6d77a913f139171430874f99b985`,
and `run23-spot`, md5 `7d0ba79ed030bdcf40479b7efd4d5fa0`, with `.text`
of 20512965 and 20525253 bytes --- the dead-spot half 12288 bytes larger.
**The first is `run22-g912` and task 6's `probe-ds-off-g912` byte for byte,
and the second is task 6's `probe-ds-on-g912`**, so the basis is a repetition
of the previous run's and this run's main set is that probe run again
on the same two binaries; the comment-only source move and the shim commit
are emission-neutral with the switch unset. Both bake
`-with-rtsopts=-A32m -I0 -T -M8G`, read back by `+RTS --info` rather
than by `strings`, and both carry the per-sample instrument and the saturating
preamble, one `@@wild` and one `@@saturate` marker apiece. The tree at launch
was `c9bf086` with seven untracked scratch paths and nothing modified.
The regime was confirmed in both binaries by `diag` before the hours were spent:
`baseOffsetsScan` at 2408930 bytes against `baseOffsetsMut`'s 2408530
on `vgg-14-c512` on each, Run 22's basis figures to the byte, where plain -O1
separates the two tenfold. The gate ran 23:12 to 23:54 the same evening, four
processes at 120 benches each, its machine check reading **-0.44%** on `list`'s
net against the fingerprint Run 22 kept, worst `stretch-r5-8x432` -1.58%,
and the run's own main-set process reads the same comparison at **-0.40%**,
worst `conv1d-24` +1.86%, both over 24 of 24 shapes and inside 3%, so the box
measures as it did.

**Neither the roster nor the source moved, which is what makes the basis
a repetition**, and the fills say so. `Main.hs` went from `0add4f4` to `125534d`
by one line of one comment, the shim from `c57e5c4` to `38bb3bb` by one commit
that adds `LOOP_DEADSPOT` off by default, and `--list` reads 1320 on both halves
and `classes --list` 2035 over 37 views, identical to each other
and to `run22-g912`'s --- 55 timed arms, sixteen A/A twin pairs, nine classes,
nothing in and nothing out. **Every tracked address of the basis is Run 22's**,
which the md5 predicts: its six-copy group at `[0, 0, 24, 0, 0, 24]`
and `0x424800`, `0x42cf00`, `0x42ddd8`, `0x453a00`, `0x454d00`, `0x457218`,
named off a `-g3` twin at post-run step 0 as `fbMidCopy`,
`fbMutOdoVecdimsAddIn`, `fbMutOdoVecdims` --- the fix, and the only tracked copy
not at offset 0 --- `fbMutOdoVecdimsAddOut`, `fbMutOdoVecdimsAddBoth`
and `fbCanonVecdims`, and its two-copy group `fbBuild` at `0x423e00`
and `fbMutOdo` at `0x42ed40`, both at offset 0; the twin locates three
of the six to the byte and the other three `0x40` below, as on Runs 21 and 22.
**The dead-spot half holds the same eight names at other addresses**:
the six-copy group at `[0, 0, 24, 0, 4, 24]` and `0x425540`, `0x42e040`,
`0x42ef58`, `0x455840`, `0x456b84`, `0x459198`, in the same order, five
of the six mod-64 offsets the basis's and `fbMutOdoVecdimsAddBoth` moved from 0
to 4; and `fbBuild` at `0x424b00` and `fbMutOdo` at `0x42ff40`, both at offset 0
still. Its twin sits `0x180` to `0x1c0` below the timed binary throughout, every
mod-64 offset preserved, so the naming rests on byte identity and the location
on a constant shift. **The four straddling self-loops the dead-spot half carries
are named**, each byte-identical in its twin: `fillStage2Short` at `0x4205aa`,
`fillStage2` at `0x422b2a` and `fbMutOdoVecdimsAddInLeafU2` at `0x42922a`, all
55-byte bodies at offset 42, and `fbMutOdoVecdimsAddInLeafU2Down` at `0x4281ef`,
53 bytes at offset 47 --- the branch's own fill, its short-body variant
and the two leaf fills the library ports, four of the nine arms the form makes
FASTER. The basis's four straddlers are Run 22's, its twin naming the 6-byte one
at `0x42207c` in `fillStage2` and refusing the three 63-byte bodies it holds
no copy of. Within the pair `--library` reads 4.1% same offset in line and 60.6%
same straddle state, the lowest same-offset figure on record, which is what
a whole-binary layout change reads.

**The three main-set anchors** read **5.92 us** on `cnn-slice-c32`, **3.03 ms**
on `cifar-L2-16-c64-k3` and **38.0 ms** on `stretch-wide-2xM`, all three net
of the forcing term and all three the basis half's; raw they read 6.10 us, 3.12
ms and 39.1 ms. **The dead-spot half's three are 5.96 us, 3.02 ms and 37.3 ms
net**, so the two halves' baselines sit within 0.5%, 0.3% and 1.7% of each other
--- the same measurement the 0.7% bar above reads as a geomean, 0.33%
over the whole shape set, which is why that bar admits this pair. Against Run
22's basis anchors of 5.98 us, 3.07 ms and 37.9 ms on this same binary,
the three moved -0.9%, -1.2% and +0.1%.

| shape | `l` | `list`, per call | net | dead-spot, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.10 us | 5.92 us | 5.96 us |
| `cifar-L2-16-c64-k3` | 147456 | 3.12 ms | 3.03 ms | 3.02 ms |
| `stretch-wide-2xM` | 1800000 | 39.1 ms | 38.0 ms | 37.3 ms |

**Each stride class carries an anchor of its own, beside its table, and all nine
are `list` on one of that class's shapes, raw and net.** The main set's three
guard a baseline that moves for every population at once; a class anchor guards
one that could move for that mechanism alone, which is the case a table
of ratios hides completely. The `runs` anchor is `runs-2` at 38.2 ms raw
and 37.1 ms net, against Run 22's 39.1 ms and 38 ms on this same binary. Read
a class anchor against the same class's anchor in an earlier run and against
nothing else, and against that class's own floor rather than the main set's.

**The correction is invertible, so pre-correction figures stay comparable.**
The `sum-only` term subtracted from every cell is published per shape,
and the two `sum-only` halves agree at **0.9999** on the basis and **1.0002**
on the dead-spot half, both within a fifth of a point of 1 --- so a reader
wanting a raw figure can recover it, and a reader comparing against a run
that corrected differently can say by how much. The in-situ check, which
is a different instrument and not the correction, reads 1.0301, 1.0237, 1.0077
and 1.0755 on the basis and 1.0274, 1.0198, 1.0173 and 1.0715 on the dead-spot
half, on `mut-odo-vecdims`, `canon-full`, `mut-flat-gm` and `bq-expand`.

[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

The pair was task 6's, `run23-g912` against `run23-spot`: one source, one
compiler, one shim commit and one roster, the second half built
with `LOOP_DEADSPOT=1` in front of `align-as.py` and nothing else varied, both
under `WILDLOG=1 SATURATE=1`, over Run 22's roster --- 55 timed arms, 1320
main-set benches and 2035 class benches over 37 views in nine classes. Six
questions were registered on 2026-09-01 --- in README's open list, where
a registration is written before its run, and moved here with their verdicts
as every run's have been since 2026-08-29 --- with a prediction and a kill
condition each, every figure in them re-derived from `probe-ds-off-main.json`
and `probe-ds-on-main.json`, the two files this run's own main set repeats
on the same two binaries; **three held, one held on its kill condition
and not on its prediction, one split, and one was killed --- by the repetition
and not by the switch**. Every cross-half figure below is read over the 23
main-set shapes that exclude `stretch-inner1`, where the branch's cell
is its own forcing term on both halves, and quoted as the registration
was written, dead-spot over basis, which is the reciprocal of what `--compare`
prints; (4)'s pair is a within-half `--pair` and is over all 24.

(1) *The padded arms' win, reproduced.* Nine arms were predicted to come back
inside this run's main-set floor of task 6's figure: `-add-in-leaf-down` 0.8328,
`lib-stage2-concat` 0.9433, `lib-stage2-disp` 0.9440, `lib-stage2-lean` 0.9441,
`lib-stage2` 0.9452, `-add-in-leaf-u2` 0.9507, `lib-stage1` 0.9537, `-u2-down`
0.9545 and `lib-stage2-short` 0.9762. They read **0.8364, 0.9470, 0.9482,
0.9502, 0.9464, 0.9494, 0.9527, 0.9511 and 0.9763** --- every one within 0.7
of a point of its prediction against a 2.03% floor. **HELD.** The counted work,
which the registration did not have, says why: the nine execute 4.0% fewer
instructions on the dead-spot half (`-short` 2.1%, `-add-in-leaf-down` 8.1%),
and on `alexnet-L1-55-c3-k11` the pad is 5.2% of `lib-stage2`'s instructions,
where the shim-free sweep the registration cited put it at 5.51%.

(2) *The flatness control: no pad, no movement.* `lib-stage2-u4`, `bq-expand`,
`mut-odo-vecdims` and `list` were predicted inside the floor of 1 with their
instruction counts equal between the halves, killed by one of the four past
the floor. They read **0.9957, 1.0010, 1.0060 and 0.9960** at count ratios
of 1.0000, 1.0021, 1.0000 and 1.0000 --- `bq-expand`'s two thousandths being
a pad of its own the form removed, worth nothing in time. **HELD.**

(3) *The classes.* The nine arms were predicted to lead on all nine classes,
each within its class floor of the main-set margin, and on `runs` the margin
to shrink monotonically with the run length; killed by a class where one
of the nine reads at or above 1 outside that class's floor, or by a `runs`
margin that does not order with the length. They lead outright on `rev`,
`revsome`, `slice`, `window` and `scaled`; on `bcast`, `bcastmid` and `runs`
several sit inside the floor either way --- on `bcast` at count ratios
of 1.0000, the fill's pad never executing on a broadcast --- and on `reshape1`
the two `-u2` leaf arms are slower on the dead-spot half, 1.0221 and 1.0377 at 4
of 4 shapes, past the basis's 3.09% and inside the dead-spot half's 10.75%,
the wider floor being the one a cross-half class margin is judged against.
The `runs` margin on `lib-stage2` reads 0.9077, 0.9863, 0.8819, 0.9650, 0.9335,
0.9871, 0.9800, 0.9637, 0.9841 and 0.8954 from `runs-2` to `runs-65536`,
ordering with nothing. **SPLIT in its first half and KILLED in its second.**

(4) *The `build`/`mut-odo` pair.* Predicted to reproduce 0.9986 on the basis
and 0.9558 on the dead-spot half inside the floors, with the sign counts staying
on their own sides of 12; killed if the halves read within a floor of each
other. It reads **0.9998 at 11 of 24** and **0.9449 at 20 of 24**, the halves
five and a half points apart, both arms' counts at 1.0000. **HELD.**

(5) *The placement-exposed workers and their twins.* `gen-unsafe` 0.8892,
`build` 0.9389 and `mut-odo` 0.9775 were predicted to reproduce inside the floor
with their instruction counts equal, killed by a count that moved. The counts
are equal, 1.0000 on all three and on all six twins; the figures read **0.9381,
0.9425 and 1.0001** --- `build` reproduced, `gen-unsafe` 4.9 points off
and `mut-odo` 2.3, both past the basis's floor --- and the twins moved in their
bases' direction at spreads of up to five points within a family, as registered.
**HELD on the kill condition, not on the prediction**: the movement
is placement, as the counts say, and its size is an evening's.

(6) *No verdict of Run 22's is re-decided by the switch --- and the write-up
names any that is.* Four were predicted to stand and (5), the vecdims ordering,
to lose `scaled`; killed by any of the other four coming out differently.
Under the dead-spot form all five stand, (5) on every population of twenty,
`scaled` included at 0.9295. Under the repetition of Run 22's own binary,
verdict (2)'s kill of `lib-stage2-u4` does not hold --- 0.9530 at `runs-65536`,
past the `runs` floor --- and its kills of `-short` and `-lean` rest on a cell
this run cannot read. **KILLED by its own terms, and by the repetition**;
the debt it put on the write-up is paid in the head of this file, verdict
by verdict.

**What the set is worth**: all six were decidable, none came back a null,
and the split and the kill were both instructive in the direction nobody
registered --- what a single evening's placement figure for a wide arm is worth,
a point or two, and what a repetition of one binary does to a verdict decided
on one cell. The registration a horde-ad consumer should take from
this is registration 1's: on this roster the shim's pads cost the shipped fill's
arms four percent of their instructions and five of their time, and a form
of the shim that places them off the path recovers it on every population
but the two broadcast classes, where the fill's pad never executes, and
at the cost of the two `-u2` leaf arms on `reshape1`.
