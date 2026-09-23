# Run 39 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 39 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, launched from disk): the two passes are worth 29.66 points on `list` and 29.85 on `bq-expand`, the fill cell Run 38 read slow is back on both halves, and one registered span of three was KILLED by a source commit the registration predates.** The pair is Runs 36's to 38's IN ITS VARIABLE --- one source, `Main.hs` at `c870e1e`, one shim at `fe6d133` under five switches with the exit span and the settled cost, ONE compiler, `10.1.20260918`, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the seventeen main-set arms that carry a cross-half figure, SIX move with the families and ELEVEN do not: the six are the `list` and `bq-expand` families entire, at **1.2966** to **1.3008**, and the eleven others span **0.9980** to **1.0199**, every one of them a fill. **The bar an arm has to clear to be the passes' rather than the run's is 0.26 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.57% on the basis and 0.43% on the control and measured WITHIN one half --- and five of the nine arms, over all seventeen, that are not A/A copies clear it, the new `lib-stage3-lean-onelevel` at 1.0199 the widest outside the families.

**What this pair was built to settle is whether the settled cost brings back the fill cell Run 38 read slow, and it does, on both halves.** On `stretch-wide-2xM` `lib-stage2-lean` and `lib-stage3-lean` read **1.0259** and **1.0305** of the `-u1` loop on the basis and **1.0301** and **1.0393** on the control, where Run 38 read 1.54 and 1.81 on the basis --- the registration's two cell spans holding on all four readings --- and the switch put every tracked fill copy at offset 0 on both halves. **Against Run 38's basis, this recipe less the switch, the four fills are 3.4 to 7.5 points faster and the other twelve timed arms within 0.8 of a point**, three of the four gains sitting on that cell and on the two smallest main-set shapes. **What it costs is straddlers**, 27 on the basis and 24 on the control against Run 38's twelve on each, and the registration's second item, which bet the switch's back-edge rules on loops they were not read on, finds no arm slower past 3% on both halves in any population. **The pair itself reads as it did**: over the eighteen shapes without Run 36's wild cell the four draws read `list` at 1.3129, 1.2950, 1.2907 and **1.2959**, the three later ones inside 0.52 of a point, and `bq-expand` at 1.2980, 1.3101, 1.3032 and **1.2985** over all nineteen.

**The counted work parts on exactly the two families, and on `bq-expand` it parts far wider than the clock.** `list` retires **1.2930** and `bq-expand` **1.5063** times as many instructions on the unflagged half, against 1.0383 on `mut-odo-vecdims` and 1.0557 on `lib-stage2-lean` --- so the basis retires 50.6 points more instructions than the flagged half on `bq-expand` and takes 29.9 points more time over it, a `time/counts` of **0.8621**, where `list` cashes all of what it saves at **1.0028**. `bq-expand`'s and `mut-odo-vecdims`'s figures are Run 38's to the fourth decimal and `list`'s is 0.02 of a point off it, across a moved source and a moved shim. **They move allocation too, as every earlier flag pair did, and by exactly what Runs 37 and 38 read**: the flagged half allocates **0.8119** of the basis on `bq-expand` and every one of its three twins and **0.9342** on `list` and both of its, on the main set. That breaks property 3's LEVEL clause in every one of the eleven populations, as on Runs 36 to 38 and as Run 31's whole `-O2` level did, while its ORDER clause holds everywhere; and six unordered consumers move with them, on allocations of hundreds of bytes a call. **Property 1 breaks on ONE cell**, the main set's basis `stretch-pow2stride`, `mut-odo-vecdims` over `bq-expand` at 1.0026, which [the open list][open] carries.

**Of two registration items, (2) holds whole and (1) holds its sentence with one of its three spans KILLED.** (1)'s two cell spans hold on both halves, and its pair span, `lib-stage3-lean` against `lib-stage2-lean` at 1.0 within 2% on the basis, reads **0.9790** --- 2.10 points off, and 0.9783 on the control beside it. **The kill is a commit and not the switch**: `c0a8aaa`, landing after the registration, rebuilt the inward fill behind `lib-stage3-lean` as one table of (stride, extent) pairs where `lib-stage2-lean`'s fill keeps two, so the pair the span was drawn for as one variable is two on this run, and the reducing consumers the same commit names read the same way, the list pair at 0.9889 where Run 38 read 1.0027. (2) is adjudicated by `probe-r39-rules.py`, which names no candidate. **Two things are worth saying about the run rather than the pair**: its sequence ran AFTER its riders, the driver having refused the sequence over a stray file named for the run --- `run-evening.sh` now refuses that before its gate --- and THREE control-half benches met foreign CPU, two in `block` and one in `compose`, none named by a span and none rerun, at the owner's word; [Provenance](#provenance) sizes them.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition. **What this run leaves the next one is a basis under the settled cost, a pair whose `list` figure is now known to three agreeing draws, and one new question**: `run39-gheadnospec` is the first published basis carrying `LOOP_SETTLED=1`, so a run keeping that recipe reads against it with no shim term. The new question is the table form `c0a8aaa` gave the inward fill, worth about two points on the fill and one on the list consumer, which no span has yet priced on its own. The SPLIT --- which of the two passes carries the regime's points --- is still read on no compiler this series builds with.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SHIM COST and the SOURCE**: the compiler is Runs 36's to 38's in-tree stage1 `10.1.20260918` unmoved, and the project file `cabal.project.ghead`, the regime, the launch from disk and the boot are Run 38's. What moved is `align-as.py`, from `f31bd1c` to `fe6d133` with `LOOP_SETTLED=1` added to the environment, and `Main.hs`, from `bb6f0fc` to `c870e1e` in seven of the owner's commits, which took the roster from 646 benches and 34 timed arms to 589 and 31. **Read against the half Run 38 built by this basis's recipe less the switch, the fills moved and nothing else did**: over the 16 arms that carry a corrected time and ran in both, this run over that one reads `lib-stage3-lean` at **0.9249**, `lib-stage1` at **0.9491**, `lib-stage2-lean` at **0.9505** and `lib-stage2-lean-u1` at **0.9660** --- below 1 meaning this run is the faster --- and the other twelve within 0.8 of a point; read as a ratio to `list` within each run, which cancels a box term exactly, the fifteen others give a `--bridge` geomean of **0.9885** with those same first three fills outside the 3.3% drift band Run 11 measured. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run39-gheadnospec`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **ONE of the thirty-one rows IS a first reading**: the roster is Run 38's with `lib-stage3-lean-onelevel` in and four arms parked --- `mut-odo-vecdims-add-in-leaf-u1`, `liblist-stage2-sum`, `liblist-stage3-sum` and `libunord-stage12-sum` --- thirty survivors in the same order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every other row has a twin in Run 38's file.

**Comparing runs?** The table below is Run 39's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.57%** from 1 on the basis half or **0.43%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one COINCIDE on both halves this run**, as they did on Run 38: **0.57%** and **0.43%** are the same over the four pairs that carry back to Run 10 as over the eight the roster carries, `bq-expand-aa-distant` carrying both on each half, so the restriction costs nothing here. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **2.09%** on `stretch-wide-2xM` on the basis and **6.20%** on `vgg-14-c512-k3` on the control --- are not floors at all and are not to be quoted as any. **And its two columns may be differenced on NONE of the eleven populations**, `list` having moved **29.66 points** on this run's main set and between 25.82 and 36.65 on the ten classes, all of it past the bar, so every cross-half figure in this file is an ORDERING and not a subtraction.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.56* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.57 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.72* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.024 | 0.113 | 0.57 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.113 | 0.59 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage3-lean-onelevel | 0.024 | 0.113 | 0.63 | 70 | 1.00x | new mutating `Vector` method -- `lib-stage3-lean` over the fill that skips its level tables at one level, against `lib-stage3-lean` |
| lib-stage2-lean-u1 | 0.025 | 0.111 | 0.58 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| lib-stage1 | 0.025 | 0.113 | 0.47 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.114 | 0.40 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.113* | *0.62* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.113* | *0.48* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.49* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.46* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.113 | 0.35 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.128 | 0.258 | 0.56 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.128* | *0.258* | *0.67* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.129* | *0.259* | *0.39* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.69 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.008* | *0.65* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.44* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run ELEVEN of the 120 pairs among the sixteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 38's basis parted on one of its 120, Run 37's on five of 105 and Run 36's on two. **The cap is what moved**: eight rows have four of their nineteen cells capped, every fill and the shipped leaf with its two copies, and the published figures sit 7.6 to 14.5 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms. `lib-stage1` over `lib-stage2-lean-u1`, for one, reads **1.0138** on the column against a paired **0.9785**. **The widest disagreement of any kind sits on the row the cap moved furthest**: `bq-expand-aa-adjacent` over `lib-stage2-lean-u1` divides to **5.1158** on the column where the paired figure is **4.3715**, the column 17.0% above it, `lib-stage2-lean-u1`'s published figure sitting 14.5 points under its plain geomean. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads fourteen of the sixteen rows moved against Run 38's table, `lib-stage1` by 12.4 points, where `--compare` against the JSON of the half Run 38 built puts that arm at 0.9491 and `list` at 0.9929.

**This run's two columns may be differenced on NONE of the eleven populations, as Runs 36's to 38's could not, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **29.66 points** on the main set and by 25.82 on `bcastmid` to 36.65 on `bcast` over the ten classes, every one of the eleven figures past the bar by a factor of thirty-six or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's. **That is the bar working rather than failing**: it exists to stop a margin being read off two columns with different denominators, and a pair built to move the denominator is the case it was written to refuse.

`concat-runs` has no row, and neither do the other 81 arms the roster holds and checks without timing --- **82 of its 113** in all, against Run 38's 97 of 131: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **ONE untimed arm joined the timed roster and FOUR timed arms left it**, in the owner's own commits and not this run's preparation: `lib-stage3-lean-onelevel`, the lean route over a fill that skips its tables at one level, landed with `fe430cf`, and `c870e1e` parked `mut-odo-vecdims-add-in-leaf-u1`, `liblist-stage2-sum`, `liblist-stage3-sum` and `libunord-stage12-sum`; `3efcad8` removed the list entry points' untimed vector arms. So `roster-delta.py`, read off the two binaries, reads 34 arms to 31 over 19 shapes to 19, the thirty survivors in the same order and the sixty-one class views unmoved over the same ten classes. A movement against Run 38's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a switch term and a source term between the two runs and no compiler, project-file, launch or boot term --- and a movement across THIS run's two halves is the two passes, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is a THREE-WAY TIE**: `lib-stage3-lean`, `lib-stage2-lean` and `lib-stage3-lean-onelevel` all read 0.024 and are separated only on the unrounded values, 0.02421, 0.02427 and 0.02438, with `lib-stage2-lean-u1` and `lib-stage1` at 0.025 and the shipped leaf at 0.026 --- **six timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, as on Run 38, the new arm taking the parked `-u1` leaf's place. **Paired on the basis the head is not a tie**: `lib-stage3-lean` over `lib-stage2-lean` is **0.9790** at 14 of 19 and p 0.064, and `lib-stage2-lean` over the shipped leaf **0.9331** at 14 of 19 and over `lib-stage1` **0.9318** at 12 of 19 --- so the pairs put the inward fill first by two points, which is the span item (1) lost. **The third is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6353** on the basis and **0.6370** on the control, 0.17 of a point apart on a pair that moves `list` by thirty points, the control's figure inside the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 and the basis's 0.05 of a point under it --- a span carried from that file and not re-derived here.

**The fill cell Run 38 read slow is back, and the switch placed every tracked fill copy at offset 0 on both halves.** On `stretch-wide-2xM` Run 38's basis read `lib-stage2-lean` and `lib-stage3-lean` at a net 1.237 and 1.452 ms against `lib-stage2-lean-u1`'s 0.801, and this run reads them at **0.820** and **0.823** against 0.799 --- 1.026 and 1.031 of the loop the run left alone, where Run 38's were 1.54 and 1.81 --- and the control half reads 1.030 and 1.039, which is registration item (1)'s two cell spans holding on both halves. `lib-stage1`, whose cell on that shape Run 38 recorded rising 80.2% against Run 37 with its counted work falling, comes back with them, at 0.570 of Run 38's. `./loop-offsets.py --delta` reads the tracked six-copy group at [0, 0, 0, 0, 0, 0] on both halves and the two-copy group at [0, 0] on both, where Run 38's basis read [18, 15, 0, 0, 9, 2] and its control [18, 0, 7, 7, 9, 26]. **What the switch costs is straddlers**: 27 on the basis and 24 on the control against Run 38's twelve on each, with 0 exit spans astride on either, and post-run step 0 names eight of the basis's and nine of the control's by byte identity, `fillStage2Short`, `fillStage2OneLevel` and the leaf bodies among them. Every straddler's arm, and every other arm, is read against Run 38 by `probe-r39-rules.py`, which names none slower past 3% on both halves in any of the eleven populations.

**The eleven half-local movers against Run 38 are two kinds, and the copy test, taken 2026-09-23 after the write-up on a quiet box, tells them apart.** `--half-movers run39 run38` flags eleven arm-populations past 3% on ONE half each, every one FASTER on this run and every one with its counted work level. `probe-r39-instance.sh` timed each one's widest cell --- cycles an iteration, the difference of an `-n 2N` and an `-n N` process, three interleaved passes --- on the timed file, a fresh copy of it and Run 38's same half. **The five `lib-stage2-lean-u1` movers are this run's BUILD**: the copy reads with the timed file, 0.988 to 1.007 of it, and Run 38's same half is slower by 8 to 19% in fresh processes --- 1.0796 on `window-64x64-k1x9` to 1.1920 on `runs-16384` --- with the same instructions, so the `-u1` loop was placed better by this build, the settled cost being the one placement term that moved. **The six `list`-family movers, all on the control half, are the evening's PROCESS**: in fresh processes Run 38's binary reads 0.997 to 1.011 of this run's on the four cells timed, and the copy level with the original on three of them, `runs-512` at 23 iterations scattering too widely a pass to read, so their 3 to 5% moved with the process and not with any binary or file. Neither kind is the pair's variable.

**The one span this run lost is a source change the registration did not see, and it names the table form as worth two points.** Item (1)'s within-run pair, `lib-stage3-lean` against `lib-stage2-lean` at 1.0 within 2% on the basis, read **0.9790**, 2.10 points off, where Run 38 read 1.0061 --- and the control half reads 0.9783. Between the registration and the build, `c0a8aaa` rewrote `fillStage2`, the inward fill behind `lib-stage3-lean`, to build one unboxed table of (stride, extent) pairs in a single pass, while `fillStage2Axes`, behind `lib-stage2-lean`, keeps the library's two tables; so the pair the span was drawn for, one variable read as a numbering, is two variables on this run. **One of the two reducing-consumer pairs the commit names says the same thing**: `liblist-stage5-sum` against `liblist-stage4-sum` reads **0.9889** on raw `slope` where Run 38 read 1.0027, and `libunord-stage14-sum` against `-stage13-sum` **0.9998** where it read 0.9996, the unordered route reading its tables off the hot path. The preparation's note recorded the commit as rewriting `lib-stage2-lean`'s fill; the commit's own message names `fillStage2` and says `fillStage2Axes` keeps its tables.


## What the next run compares against

**Run 39's pair is Run 38's with `LOOP_SETTLED=1` on both halves, [registered 2026-09-22](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's declaration of that day, and both halves were built anew from those two recipes. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; `Recommended tasks after Run 39` is NOT that site and holds post-mortems, which is [an open entry](../README.md#what-is-open) of its own. What this run leaves as the reference is `run39-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `c870e1e`, the shim at `fe6d133` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **It is the fourth published basis on that compiler, and the step from the third is NOT a null**: against `run38-gheadnospec`, which is this recipe less the switch, twelve of the sixteen timed arms that ran in both read within 0.8 points of 1, and the four fills do not --- `lib-stage3-lean` at **0.9249**, `lib-stage1` at **0.9491**, `lib-stage2-lean` at **0.9505** and `lib-stage2-lean-u1` at **0.9660**, below 1 meaning this run is the faster, `--bridge` putting the first three outside the 3.3% drift band. The cells that carry three of them are `stretch-wide-2xM`, where the three fills Run 38 read slow come back by 34 to 43 points, and the two smallest main-set shapes, `cnn-L1-6x6-c1` and `cnn-slice-c32`, by 10 to 29; `lib-stage2-lean-u1`'s gain sits instead on `alexnet-L1-55-c3-k11` at 0.768 and `stretch-tall-Mx2` at 0.795 --- which is the switch and the source together, the two having moved between the runs. **The pair itself is Runs 36's to 38's, built a fourth time**: over the eighteen shapes without Run 36's wild cell the four draws read `list` at **1.3129**, **1.2950**, **1.2907** and **1.2959**, the three later ones inside 0.52 of a point, so Run 36's stays the outlier; and `bq-expand` over all nineteen at **1.2980**, **1.3101**, **1.3032** and **1.2985**, inside 1.21 points. Against Run 31's whole-level **1.2974** the three later draws sit 0.15 to 0.67 of a point under it, so **the level's other passes still do not measurably hand `list` back**. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918`, as Runs 36's to 38's were --- and the step this run reads is not a compiler step at all.** The tally of pairs BUILT to ask the compiler stands where Run 35 left it, at TEN. **What this run adds is the pair's fourth build and the first under a new shim cost**: Runs 36 to 39 are the same two recipes on the same compiler, this one with the settled cost added to both, and their cross-half readings agree to 1.21 points on `bq-expand` and, Run 36's wild cell set aside, to 0.52 on `list` over the three later draws. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box and now the shim cost together. **The REGIME variable has now been asked SEVEN times.** Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together read **1.3360**, **1.2960**, **1.2889** and **1.2966** on `list` over the nineteen shapes and **1.2980**, **1.3101**, **1.3032** and **1.2985** on `bq-expand`. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and the four HEAD draws sit 0.13 to 1.34 points above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and the three later HEAD draws read under the level on the eighteen shapes where Run 36 read above it.

**What Run 39 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 38 and this run, and the gate says the box still measures as it did: read against the fingerprint Run 38 installed, the machine check that `run-gate.sh` runs on the gate's basis-half `a` JSON puts `list`'s net at **-0.17%**, worst `cnn-L2-24x24-c32` at **-1.55%**, 0 of 19 shapes past 5% and the geomean inside the 3% bar; the main-set JSON reads the same check at -0.72% with the same worst shape at -2.58%. **This reading carries a switch term and a source term**: Run 38's basis is this basis's recipe less `LOOP_SETTLED=1`, and seven commits of `Main.hs` separate them, so `list` holding level through both is what the check says and not that nothing moved --- the fills moved, and the check does not read them. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe, the switch included: a run that drops the switch reads against `run38-gheadnospec` instead, the last basis without it.

**Registered with the pair.** Run 39's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. Of three spans, two held and one was KILLED, and item (2)'s script named no candidate. **What a next registration should take from this one is that a span priced on the previous run's source is not a span on this one's**: the killed span is item (1)'s `lib-stage3-lean` against `lib-stage2-lean`, a within-run pair Run 38 read at 1.0061, and `c0a8aaa` --- committed after the registration --- rewrote the fill behind `lib-stage3-lean`, so the two arms now differ in their level table's form as well as in the numbering the span was drawn for, and read **0.9790** on the basis and 0.9783 on the control. The note recorded the commit as moving `lib-stage2-lean`'s fill; its own message says `fillStage2`, the inward one, and that `fillStage2Axes`, behind `lib-stage2-lean`, keeps the library's two tables.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are edited by hand, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 39**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 38 published a HEAD half on this basis's recipe less the switch, so the two published columns carry no compiler term. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9249** on `lib-stage3-lean` to **0.9976** on `mut-odo-vecdims-aa`, below 1 meaning this run is the faster, the four fills 3.4 to 7.5 points faster and the other twelve within 0.8 of a point. **The table below is this run's own two halves and no earlier run's**, eight strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, `list` having moved 29.66 points between them, so the table is two orderings read side by side.
| strategy | Run 39 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918) | Run 39 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.033 |
| `lib-stage1` | **0.025** | 0.033 |
| `lib-stage2-lean` | **0.024** | 0.032 |
| `lib-stage2-lean-u1` | **0.025** | 0.032 |
| `lib-stage3-lean` | **0.024** | 0.031 |
| `lib-stage3-lean-onelevel` | **0.024** | 0.031 |
| `bq-expand` | **0.128** | 0.128 |

**READ THE SECOND COLUMN AS A RATIO AND NOT AS A SPEED.** Every entry is that arm's net over `list`'s net in ITS OWN half, and `list` moved **29.66 points** between the halves --- forty-two times the 0.7% bar --- so the control column reading HIGHER on seven of the eight rows is the denominator having shrunk under it and not one arm of it having slowed. In absolute terms the flagged half is the faster on sixteen of the seventeen timed arms, `lib-stage2-lean-u1` at 0.9980 the one exception; the column cannot say so, and is not asked to. **And it is not an identity either**: each entry is winsorized per row within its own half, so dividing an arm's two entries does not reproduce its `--compare` figure over `list`'s. The arm-by-arm reading of what the two passes are worth is in the head, off `--compare`, where the reference is not divided out.

**A published geomean is over the same 19 shapes, and two halves of one run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered. **THE TABLE ABOVE IS NOT SUCH A PAIR**: `list` moved **29.66 points** between these halves, so the two columns are read side by side as orderings and never differenced. **They print far apart on seven of the eight rows, the control higher on each of those seven**, while `bq-expand` prints 0.128 on both, which is the one arm whose own move keeps pace with the denominator's. **Read DOWN a column and the head is a three-way tie at 0.024 on the basis** --- `lib-stage3-lean`, `lib-stage2-lean` and `lib-stage3-lean-onelevel` --- and a two-way one at 0.031 on the control, `lib-stage3-lean` and `lib-stage3-lean-onelevel`; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, the two-column table above carrying eight of its rows and every other published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6370** (0.6353); `lib-stage1` against `-u2` **1.0060** (1.0014); `lib-stage2-lean` against `-u2` **0.9364** (0.9331) and against `lib-stage1` **0.9308** (0.9318); `lib-stage3-lean` against `lib-stage2-lean` **0.9783** (0.9790); `lib-stage3-lean-onelevel` against `lib-stage3-lean` **0.9966** (1.0143); and the headline pair README's opening leads with, `bq-expand` against `mut-odo-vecdims`, **2.2022** (2.8380), 0 of 19 shapes either way on the control and 1 of 19 on the basis. **Six of the seven hold their direction across the halves**, five of them moving under a point; the headline pair moves by 63.6 points, which is the pair's own variable rather than an ordering that shifted. **The seventh is the new arm**: the one-level fill is 1.4 points behind `lib-stage3-lean` on the basis and 0.3 ahead on the control, both inside a two-point band, so the arm is level with the fill it varies on both halves and the side it lands on is not a reading.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.31 us | 0.079 | `lib-stage3-lean-onelevel` 0.053 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.59 us | 0.088 | `lib-stage3-lean-onelevel` 0.049 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 118 us | 0.063 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 387 us | 0.043 | `lib-stage3-lean-onelevel` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 458 us | 0.048 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.030 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.67 ms | 0.052 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.34 ms | 0.026 | `lib-stage3-lean-onelevel` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.9 ms | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.7 ms | 0.052 | `lib-stage3-lean-onelevel` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.8 ms | 0.031 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.6 ms | 0.023 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.2 ms | 0.113 | `lib-stage2-lean-u1` 0.111 | `mut-odo-vecdims` 0.113 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.9 ms | 0.022 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.8 ms | 0.091 | `lib-stage2-lean` 0.074 | `mut-odo-vecdims-add-in-leaf-u2` 0.077 |
| `stretch-bigstride` | 3 | 1800000 | 50.8 ms | 0.033 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.7 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41.2 ms | 0.021 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.5 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 940 us | 0.029 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29 ms | 0.020 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.6 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29 ms | 0.019 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.6 ms | 0.016 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.2 ms | 0.057 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.64 ms | 0.053 | `lib-stage3-lean-onelevel` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.25 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.9 ms | 0.034 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42 ms | 0.022 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.23 ms | 0.020 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.26 ms | 0.025 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.24 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.33 ms | 0.029 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.45 ms | 0.020 | `lib-stage3-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 940 us | 0.029 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 937 us | 0.029 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.3 ms | 0.019 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.8 ms | 0.020 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.33 ms | 0.026 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.29 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.052 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.3 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 29.8 ms | 0.024 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.3 ms | 0.048 | `lib-stage3-lean` 0.042 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 120 us | 0.063 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 464 us | 0.047 | `lib-stage3-lean-onelevel` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.38 ms | 0.025 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.3 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.3 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.8 ms | 0.025 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.6 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-512` | `runs` | 512 | 1799680 | 28.7 ms | 0.026 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 28.8 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 32.7 ms | 0.032 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 39.7 ms | 0.057 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 36.4 ms | 0.046 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-32` | `runs` | 32 | 1800000 | 30.1 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.2 ms | 0.040 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.7 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.2 ms | 0.038 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.5 ms | 0.025 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 31.8 ms | 0.030 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 29 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.3 ms | 0.026 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 271 us | 0.029 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage3-lean-onelevel` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.17 ms | 0.029 | `lib-stage2-lean-u1` 0.029 | `mut-odo-vecdims` 0.029 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.078 | `lib-stage3-lean-onelevel` 0.055 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.43 us | 0.051 | `lib-stage3-lean-onelevel` 0.036 | `mut-odo-vecdims-add-in-leaf-u2` 0.045 |
| `small-flat64` | `small` | 64 | 256 | 4.44 us | 0.059 | `lib-stage3-lean-onelevel` 0.008 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.31 us | 0.089 | `lib-stage3-lean-onelevel` 0.066 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.46 us | 0.041 | `lib-stage3-lean-onelevel` 0.040 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 279 us | 0.040 | `lib-stage3-lean-onelevel` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 955 us | 0.085 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.46 ms | 0.052 | `lib-stage3-lean-onelevel` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.61 ms | 0.051 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.83 ms | 0.051 | `lib-stage3-lean-onelevel` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.7 ms | 0.052 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.5 ms | 0.053 | `lib-stage3-lean` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 38 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the TEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FOURTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names four different `lib-` arms --- `lib-stage3-lean` on SIX rows, `lib-stage3-lean-onelevel` on two, `lib-stage2-lean` on one and `lib-stage1` on one --- where Run 38 named `lib-stage3-lean` on four, `lib-stage2-lean` on three, `lib-stage1` on two and `lib-stage2-lean-u1` on one. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 39's verdicts** over ten classes, the details beside each class's table. **Property 1 BREAKS ONE CLAUSE ON ONE CELL, the main set's basis `stretch-pow2stride`, where Run 35 broke it last; property 2 held everywhere; and property 3 broke its LEVEL clause in the same eleven populations Runs 36 to 38 broke it in, at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **The `worst` clause held in every one of the eleven populations on both halves; the `bq-expand` clause held in all of them but ONE, and broke on ONE CELL**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **1.0026**, where the control keeps its margin at **0.9835**. That is the shape and the arm pair Run 38 read at 0.9997 and 0.9756, Run 37 at 0.9945 and 0.9810, Run 36 at 0.9970 and 0.9826 and Run 35 broke at 1.0030 --- so the cell [the open list carries][open] has broken on two of the five basis draws since Run 35, by a quarter of a point this time, while the control half keeps a margin of 1.6 to 2.4 points on all four of this pair's draws. Every other shape of every population reads the clause with room, the classes' closest cells at 0.28 to 0.49 on the basis. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` is slower than `list` on `runs-2` on both halves, at **1.1131** on the basis and **1.3723** on the control, and on `runs-3` on the CONTROL half alone at **1.1237**; `--over-list` reads every other one of the 1280 timed non-control cells this run carries, over all eleven populations on both halves, at or under 1. **They are the same three cells Runs 36 to 38 read, and the four runs sit inside 1.9 points on the basis's `runs-2` cell and 1.1 on `runs-3`, and 3.6 on the control's `runs-2`**, Run 38's being 1.1053 on the basis's `runs-2`, 1.3589 on the control's and 1.1295 on `runs-3`, **and it is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0237 between the halves while `list` moves 1.2620, and on `runs-3` the fill moves 1.0301 against `list`'s 1.2889.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the ninth run running that this property is the one left entirely alone.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits under 0.053. The `bq-expand` clause is closest at `small-row96` on the CONTROL half, **1.00441**, then `scaled-rank1-m1` at 1.00003 on both halves, and `stretch-tall-Mx2` at 1.00000 on both halves of the main set with `bcast-src8` at 1.00000 on the control. **Those four figures are Runs 36's to 38's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in all ten classes and on the main set, on both halves --- and their LEVEL clause BREAKS in every one of the eleven populations, as it did on Runs 36 to 38, and on Run 31 before them, where registration (10) died on it.** The order clause is untouched: the mutable fills sit at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 19.00x to 27.66x, on both halves and in every population, `small` outside the LEVEL clause by the ruling of 2026-09-07 as before. What breaks is the level: **the two passes change what `list` and `bq-expand` ALLOCATE, and this run reads that change at Run 31's own figures.** On the main set the fills read 1.00x on both halves while `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the nineteen shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's and 38's to the fourth decimal.

**AND SIX ARMS OUTSIDE THE TWO FAMILIES MOVE, all of them unordered consumers, as on Run 38.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.8037** of the basis on `libunord-stage6-sum`, 0.8064 on `-stage6-loop-sum`, 0.8066 on `-stage7-sum`, 0.8413 on `-stage9-sum`, 0.8447 on `-stage13-sum` and 0.8448 on `-stage14-sum`, where `libunord-stage1-sum` reads 0.9987 and every ordered consumer and every fill reads 1.0000 to 1.0005. Run 38's seventh, `libunord-stage12-sum`, is parked. **In absolute terms it is hundreds of bytes a call** and the whole family sits at the 0.01x tier, so no tier moves and no property verdict changes with it. `--alloc` puts 275 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 39 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 25.82 points on `bcastmid` at narrowest and 36.65 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 38, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **170 arm-comparisons, 39 putting the basis faster and 131 slower**, with no degenerate arm excluded, at geomeans from **1.0625** on `block` to **1.1289** on `window` and extremes of `lib-stage3-lean-onelevel` at **0.9631** on `bcast` and `bq-expand-aa-adjacent` at **1.5228** on `window`; the low extreme is `lib-stage3-lean` in three of the ten. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **No registration of this run names a class**: every span is `on main`, and item (2)'s script reads every class against Run 38 and names no arm, so each block below carries its properties, its floor and its own cross-half reading.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **In practice the bold marks the FASTER of the two named arms, one cell a row**, and on this run it is the arm outside the family on ALL TEN --- `lib-stage3-lean` on `rev`, `bcast`, `runs`, `flip`, `block` and `compose`, `lib-stage3-lean-onelevel` on `window` and `small`, `lib-stage2-lean` on `bcastmid` and `lib-stage1` on `scaled`. **The family's ceiling is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` on every row**, the `-u1` leaf that held `scaled`'s ceiling on Run 38 being parked. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.063 | **`lib-stage3-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 0.54% |
| `bcast` | 6 | 0.022 | 0.057 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.77% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.28% |
| `window` | 8 | 0.051 | 0.085 | **`lib-stage3-lean-onelevel`** 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.10% |
| `scaled` | 3 | 0.029 | 0.029 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 1.51% |
| `runs` | 17 | 0.027 | 0.057 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.22% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage3-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.88% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage3-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 1.02% |
| `small` | 5 | 0.061 | 0.089 | **`lib-stage3-lean-onelevel`** 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 | 0.12% |
| `compose` | 4 | 0.024 | 0.029 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 | 1.00% |

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` in every one of the ten --- the lead that broke the ordering property 2 carried until 2026-09-06. **No row's bold sits in the CEILING column this run**: `compose`, the one row Run 38 bolded there, falls to the arm outside the family, on a tie. SIX rows change the arm they name --- `compose` among them, naming `lib-stage3-lean` where Run 38 named `lib-stage2-lean`, beside the bold's move: `window` and `small` name the new `lib-stage3-lean-onelevel`, where Run 38 named `lib-stage3-lean` and `lib-stage2-lean-u1`; `runs` and `flip` name `lib-stage3-lean` where it named `lib-stage2-lean`; and `bcastmid` names `lib-stage2-lean` where it named `lib-stage1`. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **ONE row ties at three decimals** --- `compose` at 0.015 --- and the bold on it is `--block`'s own, computed on the unrounded values where the printed ones cannot separate: outside the family against the ceiling, 0.014646 against 0.014686, a parting of 4.0e-5, inside the three decimals the table prints, so the bold marks a tie-break and not a lead a reader of the table could see.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.15* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.11 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.09 | 148 | 1.01x |
| liblist-stage5-sum | -- | -- | 0.10 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.13 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.01 | 157 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.04 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage3-lean | 0.022 | 0.026 | 0.10 | 148 | 1.00x |
| lib-stage3-lean-onelevel | 0.022 | 0.026 | 0.08 | 148 | 1.00x |
| lib-stage2-lean | 0.022 | 0.027 | 0.10 | 148 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.041 | 0.10 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.023* | *0.041* | *0.10* | *147* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.041* | *0.07* | *147* | *1.00x* |
| lib-stage1 | 0.024 | 0.039 | 0.11 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.025 | 0.032 | 0.11 | 147 | 1.01x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.062* | *0.11* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.063* | *0.18* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.063 | 0.11 | 138 | 1.00x |
| bq-expand | 0.138 | 0.234 | 0.16 | 122 | 3.22x |
| *bq-expand-aa-adjacent* | *0.138* | *0.235* | *0.15* | *122* | *3.22x* |
| *bq-expand-aa-distant* | *0.139* | *0.235* | *0.09* | *122* | *3.22x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 85 | 26.11x |
| *list-aa-distant* | *1.001* | *1.006* | *0.27* | *85* | *26.11x* |
| *list-aa-adjacent* | *1.002* | *1.008* | *0.23* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9946, worst cell 1.47% on `rev-cnn-L1-24x24-c1`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0004 on a worst cell of 0.15% on `rev-primes`, its interval covering 1. The in-situ term reads 1.0030, 1.0163 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9963, which the correction amplifies by 1.71x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m7s, peak 95 MiB in use, 25 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.53 ms per call raw, 4.38 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.063/0.047/0.025

**Across the halves:** 1 of the 17 arms are faster on this half and 16 slower, at a geomean of 1.1075, from `mut-odo-vecdims-aa-distant` at 0.9976 to `bq-expand-aa-distant` at 1.3082, with `list` itself at 1.2841. **The baseline moved 28.41% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.063, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage3-lean` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.5070 over 3 of 3 shapes at sign p 0.25, a margin of 49.30% against this class's 0.54% floor (`mut-odo-vecdims-aa-distant`). `lib-stage3-lean` leads outside the family here as it did on Run 38, and the class is one of the six the arm leads. Its two columns may NOT be differenced, `list` having moved 28.41 of a point, at a class geomean of 1.1075 over the 17 arms, with 8 of 9 strategies past an A/A bar of 0.73 points. The counted work reads a counts geomean of 1.1586 over the same arms, 17 of them counted. Its counted work parts by 15.86 points where its clock parts by 10.75, so about 0.68 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.58* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.33* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.015 | 0.020 | 0.47 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.49* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.43 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| lib-stage2-lean | 0.016 | 0.020 | 0.42 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.40 | 62 | 1.00x |
| lib-stage3-lean-onelevel | 0.016 | 0.016 | 0.49 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.024 | 0.48 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.022* | *0.057* | *0.33* | *61* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.022* | *0.057* | *0.38* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.022** | 0.057 | 0.18 | 61 | 1.00x |
| bq-expand | 0.092 | 0.143 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-adjacent* | *0.092* | *0.144* | *0.68* | *46* | *1.00x* |
| *bq-expand-aa-distant* | *0.092* | *0.142* | *0.21* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.11 | 17 | 20.99x |
| *list-aa-distant* | *1.004* | *1.008* | *0.81* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.006* | *1.012* | *0.79* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9923, worst cell 2.35% on `bcast-src8`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.10% on `bcast-src64`, its interval covering 1. The in-situ term reads 1.0215, 1.0084 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9975, which the correction amplifies by 3.11x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m14s, peak 169 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.7 ms per call raw, 29.6 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.016/0.019/0.020

**Across the halves:** 1 of the 17 arms are faster on this half and 16 slower, at a geomean of 1.0856, from `lib-stage3-lean-onelevel` at 0.9631 to `list` at 1.3665, with `list` itself at 1.3665. **The baseline moved 36.65% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6452 over 6 of 6 shapes at sign p 0.031, a margin of 35.48% against this class's 0.77% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). `lib-stage3-lean` leads here as on Run 38, and this class carries the run's low cross-half extreme, the new `lib-stage3-lean-onelevel` at 0.9631, the one arm of the seventeen the basis runs faster there. Its two columns may NOT be differenced, `list` having moved 36.65 of a point, at a class geomean of 1.0856 over the 17 arms, with 6 of 9 strategies past an A/A bar of 0.54 points. The counted work reads a counts geomean of 1.1638 over the same arms, 17 of them counted. Its counted work parts by 16.38 points where its clock parts by 8.56, so about 0.52 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.35 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.40 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.33 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.39 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.32 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 96 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.24* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *88* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.017 | 0.32 | 82 | 1.00x |
| lib-stage3-lean | 0.012 | 0.017 | 0.31 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.31 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.018 | 0.37 | 82 | 1.00x |
| lib-stage3-lean-onelevel | 0.013 | 0.019 | 0.32 | 81 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.28 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.26* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.37* | *80* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.27* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.24* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.21 | 76 | 1.00x |
| *bq-expand-aa-adjacent* | *0.099* | *0.183* | *0.45* | *61* | *1.92x* |
| bq-expand | 0.099 | 0.183 | 0.44 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.099* | *0.183* | *0.27* | *61* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 0.79 | 28 | 23.56x |
| *list-aa-distant* | *1.001* | *1.003* | *0.85* | *28* | *23.56x* |
| *list-aa-adjacent* | *1.001* | *1.003* | *0.76* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 0.9972, worst cell 0.69% on `bcastmid-block150k`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.06% on `bcastmid-b200k`, its interval covering 1. The in-situ term reads 1.0176, 1.0631 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9987, which the correction amplifies by 1.93x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m50s, peak 128 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 49 ms per call raw, 47.9 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 6 of the 17 arms are faster on this half and 11 slower, at a geomean of 1.0804, from `lib-stage3-lean` at 0.9747 to `list-aa-distant` at 1.2643, with `list` itself at 1.2582. **The baseline moved 25.82% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4126 over 4 of 4 shapes at sign p 0.12, a margin of 58.74% against this class's 0.28% floor (`mut-odo-vecdims-aa`). `lib-stage2-lean` leads outside the family here, where Run 38 named `lib-stage1`. Its two columns may NOT be differenced, `list` having moved 25.82 of a point, at a class geomean of 1.0804 over the 17 arms, with 7 of 9 strategies past an A/A bar of 0.77 points. The counted work reads a counts geomean of 1.1669 over the same arms, 17 of them counted. Its counted work parts by 16.69 points where its clock parts by 8.04, so about 0.48 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.34* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.21 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.17 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.16 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.17 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage14-sum | -- | -- | 0.08 | 102 | 0.03x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 94 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.10 | 100 | 0.03x |
| libunord-stage7-sum | -- | -- | 0.04 | 102 | 0.03x |
| libunord-stage9-sum | -- | -- | 0.08 | 100 | 0.03x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.22* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage3-lean-onelevel | 0.024 | 0.027 | 0.22 | 84 | 1.00x |
| lib-stage3-lean | 0.024 | 0.027 | 0.18 | 84 | 1.00x |
| lib-stage2-lean | 0.024 | 0.028 | 0.21 | 84 | 1.00x |
| lib-stage1 | 0.025 | 0.027 | 0.15 | 84 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.15* | *83* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.17 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.17* | *82* | *1.00x* |
| lib-stage2-lean-u1 | 0.029 | 0.032 | 0.50 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.051* | *0.085* | *0.16* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.086* | *0.17* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.085 | 0.16 | 76 | 1.00x |
| *bq-expand-aa-distant* | *0.176* | *0.215* | *0.26* | *57* | *3.86x* |
| *bq-expand-aa-adjacent* | *0.176* | *0.214* | *0.30* | *57* | *3.86x* |
| bq-expand | 0.176 | 0.213 | 0.37 | 57 | 3.86x |
| *list-aa-distant* | *0.999* | *1.012* | *0.46* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.48 | 30 | 27.66x |
| *list-aa-adjacent* | *1.000* | *1.007* | *0.36* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 1.0010, worst cell 1.02% on `window-64x64-k1x9`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.24% on `window-224x224-k3-s2`, its interval covering 1. The in-situ term reads 1.0058, 1.1706 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0009, which the correction amplifies by 1.55x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m28s, peak 125 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.085/0.031/0.052/0.051/0.053/0.052

**Across the halves:** 5 of the 17 arms are faster on this half and 12 slower, at a geomean of 1.1289, from `mut-odo-vecdims` at 0.9944 to `bq-expand-aa-adjacent` at 1.5228, with `list` itself at 1.2913. **The baseline moved 29.13% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.085, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.024, priced against `mut-odo-vecdims` at 0.4214 over 8 of 8 shapes at sign p 0.0078, a margin of 57.86% against this class's 0.10% floor (`mut-odo-vecdims-aa-distant`). The new `lib-stage3-lean-onelevel` leads outside the family here, where Run 38 named `lib-stage3-lean`, and this class carries the run's tightest floor, 0.10% on the basis, and its high cross-half extreme, `bq-expand-aa-adjacent` at 1.5228. Its two columns may NOT be differenced, `list` having moved 29.13 of a point, at a class geomean of 1.1289 over the 17 arms, with 3 of 9 strategies past an A/A bar of 0.64 points. The counted work reads a counts geomean of 1.1691 over the same arms, 17 of them counted. Its counted work parts by 16.91 points where its clock parts by 12.89, so about 0.76 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.23 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.16 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.22 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.20 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.20 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.15 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.19 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.16 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.12 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *138* | *0.00x* |
| lib-stage1 | 0.021 | 0.030 | 0.13 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.030* | *0.12* | *128* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.023* | *0.030* | *0.13* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.030 | 0.28 | 127 | 1.00x |
| lib-stage3-lean | 0.023 | 0.030 | 0.15 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.030 | 0.22 | 128 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.18 | 127 | 1.00x |
| lib-stage3-lean-onelevel | 0.025 | 0.030 | 0.17 | 128 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.029* | *0.08* | *127* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.029* | *0.21* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.029 | 0.11 | 127 | 1.00x |
| bq-expand | 0.091 | 0.100 | 0.10 | 111 | 1.21x |
| *bq-expand-aa-adjacent* | *0.091* | *0.100* | *0.08* | *111* | *1.21x* |
| *bq-expand-aa-distant* | *0.091* | *0.101* | *0.10* | *111* | *1.21x* |
| *list-aa-distant* | *0.997* | *1.003* | *0.22* | *69* | *21.49x* |
| list (baseline) | 1.000 | 1.000 | 0.33 | 69 | 21.49x |
| *list-aa-adjacent* | *1.000* | *1.004* | *0.19* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9849, worst cell 2.97% on `scaled-r5`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0005 on a worst cell of 0.15% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0025, 1.0028 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9942, which the correction amplifies by 2.42x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m8s, peak 109 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.35 ms per call raw, 5.17 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.029/0.029

**Across the halves:** 2 of the 17 arms are faster on this half and 15 slower, at a geomean of 1.0697, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9762 to `list-aa-adjacent` at 1.3295, with `list` itself at 1.3254. **The baseline moved 32.54% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.8961 over 2 of 3 shapes at sign p 1, a margin of 10.39% against this class's 1.51% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). `lib-stage1` leads outside the family here, as on Run 38. Its two columns may NOT be differenced, `list` having moved 32.54 of a point, at a class geomean of 1.0697 over the 17 arms, with 2 of 9 strategies past an A/A bar of 3.38 points. The counted work reads a counts geomean of 1.1469 over the same arms, 17 of them counted. Its counted work parts by 14.69 points where its clock parts by 6.97, so about 0.47 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.47* | *52* | *1.08x* |
| liblist-stage1-sum | -- | -- | 0.13 | 61 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 73 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.03 | 73 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.11 | 61 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.03 | 73 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 73 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 70 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 73 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.03 | 73 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 73 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.025 | 0.12 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.025 | 0.15 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.026* | *0.44* | *59* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.11* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.026 | 0.10 | 59 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.026 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.08* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.057 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.057* | *0.09* | *59* | *1.00x* |
| lib-stage3-lean-onelevel | 0.028 | 0.028 | 0.12 | 58 | 1.00x |
| *bq-expand-aa-adjacent* | *0.093* | *0.141* | *0.42* | *46* | *1.08x* |
| bq-expand | 0.094 | 0.141 | 0.42 | 46 | 1.08x |
| *bq-expand-aa-distant* | *0.094* | *0.143* | *0.03* | *46* | *1.08x* |
| lib-stage1 | 0.099 | 1.113 | 0.16 | 51 | 1.42x |
| list (baseline) | 1.000 | 1.000 | 2.57 | 17 | 21.30x |
| *list-aa-distant* | *1.031* | *1.051* | *0.36* | *17* | *21.30x* |
| *list-aa-adjacent* | *1.032* | *1.052* | *0.17* | *17* | *21.30x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0322, worst cell 5.16% on `runs-16384`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.32% on `runs-2`, its interval covering 1. The in-situ term reads 1.0280, 1.0338 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0311, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h45m45s, peak 647 MiB in use, 289 MiB max residency; the reader reads 31 benchmarks over 17 shapes of the runs class. Anchor: `runs-2`, `list` at 40.7 ms per call raw, 39.7 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.046/0.040/0.038/0.032/0.030/0.026/0.025/0.025/0.025/0.025/0.026/0.025/0.025/0.024/0.024/0.026

**Across the halves:** 6 of the 17 arms are faster on this half and 11 slower, at a geomean of 1.0811, from `lib-stage2-lean-u1` at 0.9923 to `list` at 1.3326, with `list` itself at 1.3326. **The baseline moved 33.26% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.08x, 21.30x --- and `lib-stage3-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7750 over 17 of 17 shapes at sign p 1.5e-05, a margin of 22.50% against this class's 3.22% floor (`list-aa-adjacent`). `lib-stage3-lean` leads outside the family here, where Run 38 named `lib-stage2-lean`; this class also holds the three cells where `lib-stage1` is slower than `list`, on `runs-2` and `runs-3` (the properties). Its two columns may NOT be differenced, `list` having moved 33.26 of a point, at a class geomean of 1.0811 over the 17 arms, with 4 of 9 strategies past an A/A bar of 0.82 points. The counted work reads a counts geomean of 1.1556 over the same arms, 17 of them counted. Its counted work parts by 15.56 points where its clock parts by 8.11, so about 0.52 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.16 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.08 | 93 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.15 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *93* | *0.00x* |
| lib-stage3-lean | 0.022 | 0.042 | 0.27 | 84 | 1.00x |
| lib-stage2-lean | 0.022 | 0.042 | 0.24 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.047 | 0.30 | 83 | 1.00x |
| lib-stage3-lean-onelevel | 0.025 | 0.047 | 0.33 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.041* | *0.31* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.042 | 0.13 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.042* | *0.27* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.052* | *0.07* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.08 | 77 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.12* | *77* | *1.00x* |
| lib-stage1 | 0.033 | 0.049 | 0.25 | 82 | 1.00x |
| bq-expand | 0.090 | 0.180 | 0.42 | 61 | 1.05x |
| *bq-expand-aa-adjacent* | *0.091* | *0.180* | *0.42* | *61* | *1.05x* |
| *bq-expand-aa-distant* | *0.092* | *0.181* | *0.08* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.82 | 32 | 21.18x |
| *list-aa-distant* | *1.005* | *1.016* | *0.44* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.007* | *1.023* | *0.22* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9912, worst cell 3.40% on `flip-last-rows`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `flip-fwd-rows96`, its interval covering 1. The in-situ term reads 1.0162, 1.0200 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9956, which the correction amplifies by 2.25x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m13s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.048/0.026/0.026

**Across the halves:** 5 of the 17 arms are faster on this half and 12 slower, at a geomean of 1.0700, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9903 to `list-aa-distant` at 1.3344, with `list` itself at 1.3280. **The baseline moved 32.80% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage3-lean` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.7234 over 6 of 6 shapes at sign p 0.031, a margin of 27.66% against this class's 0.88% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). `lib-stage3-lean` leads outside the family here, where Run 38 named `lib-stage2-lean`. Its two columns may NOT be differenced, `list` having moved 32.80 of a point, at a class geomean of 1.0700 over the 17 arms, with 5 of 9 strategies past an A/A bar of 0.48 points. The counted work reads a counts geomean of 1.1467 over the same arms, 17 of them counted. Its counted work parts by 14.67 points where its clock parts by 7.00, so about 0.48 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.17 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 128 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.06 | 128 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.04 | 129 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.08 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.05 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.12 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.07 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.12 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| lib-stage3-lean | 0.020 | 0.023 | 0.13 | 112 | 1.00x |
| lib-stage2-lean | 0.020 | 0.023 | 0.15 | 112 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.13* | *112* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.13* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.12 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.026 | 0.09 | 111 | 1.00x |
| lib-stage3-lean-onelevel | 0.023 | 0.026 | 0.25 | 110 | 1.00x |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.08 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.14* | *111* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.030* | *0.35* | *111* | *1.00x* |
| lib-stage1 | 0.050 | 0.058 | 0.14 | 103 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.11* | *96* | *1.06x* |
| bq-expand | 0.087 | 0.087 | 0.13 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.087* | *0.087* | *0.13* | *96* | *1.06x* |
| list (baseline) | 1.000 | 1.000 | 0.18 | 54 | 21.22x |
| *list-aa-adjacent* | *1.001* | *1.003* | *0.26* | *54* | *21.22x* |
| *list-aa-distant* | *1.005* | *1.015* | *0.23* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 1.0102, worst cell 4.13% on `block-run64-page`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9997 on a worst cell of 0.16% on `block-run64-gap64`, its interval covering 1. The in-situ term reads 1.0254, 1.0195 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0047, which the correction amplifies by 2.49x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m30s, peak 134 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.61 ms per call raw, 4.45 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.020/0.025/0.029/0.024/0.020

**Across the halves:** 5 of the 17 arms are faster on this half and 12 slower, at a geomean of 1.0625, from `lib-stage3-lean` at 0.9818 to `list-aa-distant` at 1.3478, with `list` itself at 1.3326. **The baseline moved 33.26% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage3-lean` leads outside the family at 0.020, priced against `mut-odo-vecdims` at 0.8660 over 5 of 5 shapes at sign p 0.062, a margin of 13.40% against this class's 1.02% floor (`mut-odo-vecdims-aa-distant`). `lib-stage3-lean` leads outside the family here as on Run 38, and this class holds the run's largest intrusion: two control-half cells on `block-run64-off7`, `lib-stage3-lean` and `lib-stage2-lean`, read 5.8% and 3.0% slower than the same cells on the basis on the mutator clock, 16.3% and 7.5% on the corrected net the tables use, under 1.29 and 0.92 of a core of foreign CPU, so the class's cross-half line reads those two arms through them. Its two columns may NOT be differenced, `list` having moved 33.26 of a point, at a class geomean of 1.0625 over the 17 arms, with 4 of 9 strategies past an A/A bar of 1.62 points. The counted work reads a counts geomean of 1.1438 over the same arms, 17 of them counted. Its counted work parts by 14.38 points where its clock parts by 6.25, so about 0.43 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.20 | 228 | 1.73x |
| liblist-stage4-sum | -- | -- | 0.13 | 235 | 1.37x |
| liblist-stage5-sum | -- | -- | 0.13 | 239 | 1.26x |
| libunord-stage1-sum | -- | -- | 0.17 | 222 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.10 | 243 | 0.22x |
| libunord-stage14-sum | -- | -- | 0.12 | 243 | 0.22x |
| libunord-stage6-loop-sum | -- | -- | 0.19 | 239 | 0.69x |
| libunord-stage6-sum | -- | -- | 0.20 | 239 | 0.69x |
| libunord-stage7-sum | -- | -- | 0.17 | 239 | 0.69x |
| libunord-stage9-sum | -- | -- | 0.19 | 238 | 0.46x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.24* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.05* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.02* | *250* | *0.01x* |
| lib-stage3-lean-onelevel | 0.035 | 0.066 | 0.26 | 235 | 1.12x |
| lib-stage3-lean | 0.042 | 0.067 | 0.23 | 232 | 1.22x |
| lib-stage2-lean | 0.045 | 0.080 | 0.17 | 230 | 1.32x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.053 | 0.068 | 0.37 | 229 | 1.28x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.069* | *0.28* | *229* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.053* | *0.068* | *0.32* | *229* | *1.28x* |
| lib-stage2-lean-u1 | 0.054 | 0.097 | 0.20 | 228 | 1.45x |
| **mut-odo-vecdims** | **0.061** | 0.089 | 0.20 | 229 | 1.27x |
| *mut-odo-vecdims-aa* | *0.061* | *0.088* | *0.35* | *229* | *1.27x* |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.088* | *0.30* | *229* | *1.27x* |
| lib-stage1 | 0.084 | 0.105 | 0.19 | 221 | 2.36x |
| *bq-expand-aa-distant* | *0.136* | *0.198* | *0.14* | *217* | *1.44x* |
| *bq-expand-aa-adjacent* | *0.136* | *0.198* | *0.14* | *218* | *1.44x* |
| bq-expand | 0.137 | 0.198 | 0.13 | 218 | 1.44x |
| list (baseline) | 1.000 | 1.000 | 0.14 | 180 | 21.57x |
| *list-aa-adjacent* | *1.000* | *1.001* | *0.13* | *180* | *21.57x* |
| *list-aa-distant* | *1.001* | *1.001* | *0.15* | *180* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 1.0012, worst cell 0.55% on `small-flat64`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9997 on a worst cell of 0.14% on `small-patch-k5`, its interval covering 1. The in-situ term reads 0.9882, 0.9800 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0008, which the correction amplifies by 1.53x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m33s, peak 142 MiB in use, 56 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.69 us per call raw, 6.46 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.078/0.051/0.059/0.089

**Across the halves:** 2 of the 17 arms are faster on this half and 15 slower, at a geomean of 1.0940, from `lib-stage1` at 0.9842 to `list-aa-adjacent` at 1.3003, with `list` itself at 1.2765. **The baseline moved 27.65% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.089, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.035, priced against `mut-odo-vecdims` at 0.5505 over 5 of 5 shapes at sign p 0.062, a margin of 44.95% against this class's 0.12% floor (`mut-odo-vecdims-aa-distant`). The new `lib-stage3-lean-onelevel` leads outside the family here, where Run 38 named `lib-stage2-lean-u1`. Its two columns may NOT be differenced, `list` having moved 27.65 of a point, at a class geomean of 1.0940 over the 17 arms, with 7 of 9 strategies past an A/A bar of 1.87 points. The counted work reads a counts geomean of 1.1453 over the same arms, 17 of them counted. Its counted work parts by 14.53 points where its clock parts by 9.40, so about 0.65 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.33* | *86* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.29 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 98 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.28 | 98 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.30 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.016* | *0.29* | *98* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.015* | *0.016* | *0.27* | *98* | *1.00x* |
| lib-stage3-lean | 0.015 | 0.017 | 0.32 | 98 | 1.00x |
| lib-stage2-lean | 0.015 | 0.017 | 0.30 | 98 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.36 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.33 | 98 | 1.00x |
| lib-stage3-lean-onelevel | 0.016 | 0.023 | 0.33 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.017 | 0.34 | 97 | 1.00x |
| *mut-odo-vecdims-aa* | *0.024* | *0.029* | *0.24* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.024* | *0.029* | *0.29* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.029 | 0.20 | 94 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.102* | *0.35* | *79* | *1.35x* |
| bq-expand | 0.094 | 0.102 | 0.39 | 79 | 1.35x |
| *bq-expand-aa-distant* | *0.095* | *0.102* | *0.22* | *79* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 0.67 | 44 | 22.01x |
| *list-aa-distant* | *1.002* | *1.007* | *0.78* | *44* | *22.01x* |
| *list-aa-adjacent* | *1.002* | *1.010* | *0.66* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9900, worst cell 1.54% on `compose-scalar`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `compose-rev-bcast`, its interval covering 1. The in-situ term reads 1.0075, 1.0212 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9970, which the correction amplifies by 3.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m52s, peak 126 MiB in use, 33 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.029/0.029/0.020/0.019

**Across the halves:** 6 of the 17 arms are faster on this half and 11 slower, at a geomean of 1.0762, from `lib-stage3-lean` at 0.9871 to `list-aa-distant` at 1.3370, with `list` itself at 1.3366. **The baseline moved 33.66% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage3-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6210 over 4 of 4 shapes at sign p 0.12, a margin of 37.90% against this class's 1.00% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). `lib-stage3-lean` leads outside the family here on a tie with the family's ceiling, 0.014646 against 0.014686 unrounded, where Run 38 bolded the ceiling; one control-half cell, `compose-zero-mid/liblist-stage1-sum`, met 0.27 of a core of foreign CPU and reads 1.3% slower than the basis's. Its two columns may NOT be differenced, `list` having moved 33.66 of a point, at a class geomean of 1.0762 over the 17 arms, with 7 of 9 strategies past an A/A bar of 0.32 points. The counted work reads a counts geomean of 1.1590 over the same arms, 17 of them counted. Its counted work parts by 15.90 points where its clock parts by 7.62, so about 0.48 of the instruction saving reaches the clock.


## Provenance

**Run 39's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `c870e1e`; one shim, `align-as.py` at `fe6d133`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`, which is Runs 36's to 38's compiler unmoved; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run39-gheadnospec` and is what every table here publishes; `run39-gheadtwopass` is the candidate. **What is new against Run 38 is not the pair but two of its inputs**: the shim moved two commits, `6798792` counting the planned straddles as heads under every cost and `fe6d133` adding the `LOOP_SETTLED` switch, which is on both lines; and the source moved seven of the owner's commits. The project file, the compiler, the launch and the boot are Run 38's, `/proc/uptime` putting the box up since 2026-09-21 11:09, so no reboot sits between the two runs.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 61 class views over ten classes for 1891 more, and it is Run 38's with ONE ARM IN and FOUR OUT.** `./roster-delta.py run38-gheadnospec run39-gheadnospec`, read off the two binaries, puts `lib-stage3-lean-onelevel` in and `mut-odo-vecdims-add-in-leaf-u1`, `liblist-stage2-sum`, `liblist-stage3-sum` and `libunord-stage12-sum` out, parked by `c870e1e`, with 30 survivors in the same order, the nineteen main-set shapes unmoved and the sixty-one class views unmoved over the same ten classes. Pre-run step 12's condition fired, the membership having moved and the timed roster having gained an arm, and **its -L1 pass was NOT taken**, the owner having ruled it out for this run; what stood in for it is the smoke sweep, one shape a process. Every cross-run figure in this file is read over the 30 survivors.

**The sequence ran in ONE window, but not in the order the run list gives, and two of its processes met foreign CPU.** The driver's sequence stage refused at once, over a stray log named for the run, which the executing session had redirected the driver's own output to and which `run-major.sh`'s relaunch guard counts as an earlier attempt's artifact; the driver went on to the riders, which ran 02:57 to 03:09 on the quiet box, and the session relaunched the sequence alone under the same launch environment. The wall-clock log puts the twenty-two processes between 2026-09-23T03:10:30 and 2026-09-23T10:21:18, the largest hole between one process finishing and the next starting 0m, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones. The gate's four processes ran 02:23 to 02:57, and the counted work, which wants no quiet machine, from 10:21. **The intrusion verdict is NOT clean, and every exposed bench is the control half's**: `--wild` finds TWO benches at or above 0.25 foreign in `run39-gheadtwopass-block`, `block-run64-off7/lib-stage3-lean` at 1.29 and `block-run64-off7/lib-stage2-lean` at 0.92, between 09:05 and 09:19, when this session ran nothing; and ONE in `run39-gheadtwopass-compose`, `compose-zero-mid/liblist-stage1-sum` at 0.27, inside the window where this session answered a status question with two small reads. The other twenty processes are clean. **Post-run step 3's rerun was NOT taken, on the owner's word**, and the size stands in its place: against the same cells on the basis half, the two `block` cells read 5.8% and 3.0% slower on the control's mutator clock, `lib-stage3-lean`'s first, where the same two arms on the other four `block` shapes part by at most 2.0%, and 16.3% and 7.5% on the corrected net the tables use, where those others part by up to 5.6%; the `compose` cell reads 1.3% on the mutator clock. No registered span reads `block` or `compose`.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes agree: `mut-odo-vecdims` reads 1.0092 and 0.9999, `bq-expand` 1.3044 and 1.2983, and `list` 1.3082 and 1.3024 --- 0.93, 0.61 and 0.58 points apart --- with the two `sum-only` controls, on raw `slope`, within 0.04% of 1 on both passes. **What the passes part by is each half's own leg-to-leg movement and not a disagreement about the pair**: the control's `a` leg over its `b` reads `list` at 1.0022 where the basis's two legs read 1.0066, which predicts the second pass at 0.9956 times the first against an observed 0.9956, and the same arithmetic lands at 0.9953 against 0.9953 on `bq-expand` and 0.9908 against 0.9908 on `mut-odo-vecdims`. The machine check, read against the fingerprint Run 38 installed --- this run's basis recipe less the switch and the moved source --- puts `list`'s net at **-0.17%**, worst `cnn-L2-24x24-c32` at **-1.55%**, 0 of 19 shapes past 5% and the geomean inside the 3% bar; the main-set JSON reads the same check at -0.72% with the same worst shape at -2.58%, which is the instrument and not a disagreement.

**Every one of the twenty-two processes gated clean, the plateau refused by declaration, and FOUR A/A worst cells sit past 5%.** `read-all.sh` gates each process on its own correction and passes all twenty-two. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.8492 to 21.4157 ms/iter across the run, a 27.10% spread against a 5% band, and it splits exactly by half, the basis's eleven processes flat within 1.63% at 21.0730 to 21.4157 and the control's within 2.32% at 16.8492 to 17.2408 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-main` at **6.20%** on `vgg-14-c512-k3`, `gheadtwopass-runs` at **6.24%**, `gheadtwopass-window` at **5.40%** and `gheadnospec-runs` at **5.16%**; the main set's floors are 0.57% on the basis and 0.43% on the control, so the main-set cell is one cell an order of magnitude outside a floor the population otherwise keeps.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run39-gheadnospec`, md5 `dddda660047e6bd7100329e095c407b5`, and `run39-gheadtwopass`, md5 `47086b16c69e222291cd4a2bc5934843`, built back to back in one call on 2026-09-23 against a clean tree. Their `.text` sections are **20227903** and **20305727** bytes, the first column of `size -A`; against Run 38's two the basis is larger by 24576 bytes, six pages exactly, and the flagged half by 36864, nine --- the switch and the source together, recorded and not apportioned. **NEITHER md5 reproduces anything**, the shim and the source having both moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 77824 bytes --- nineteen pages exactly, a seventh exact page multiple in that series --- and carries MORE self-loops, 344 against 338, as on Run 38, so [the open list's entry on it](../README.md#what-is-open) reads on this pair as it did on that one.

**The switch moved every tracked fill copy to offset 0, which is what it is for.** `./loop-offsets.py --delta run38-gheadnospec run39-gheadnospec`, Run 38's basis recipe against this one's, which parts from it in the switch, the shim commit and the source, reads the six-copy group's offsets MOVED, [18, 15, 0, 0, 9, 2] to [0, 0, 0, 0, 0, 0], with no address surviving to the byte and six displacements, four of them not a whole line; the two-copy group keeps every mod-64 offset at [0, 0]. **Within the pair the two passes no longer move them at all**: the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves and the two-copy group [0, 0] on both, where Run 38's control half read [18, 0, 7, 7, 9, 26] and [4, 4] against its basis; a group of three copies exists on the control half alone, at [0, 0, 0]. `--library` puts the two halves at **4.3%** the same offset in line over 808 common library self-loops, which is Runs 36's to 38's 4.3% to the tenth: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 27 on the basis and 24 on the control, where Run 38 read twelve on each, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 338 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 344 on the control, 237 and 143 of them at offset 0 where Run 38 read 193 and 190, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 0's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity the same eight bodies on each half** --- `fillStage2Short` twice, `fillStage2OneLevel`, the four leaf bodies of `fbMutOdoVecdimsAddInLeafU2`, `-Down` and `-Last` among them, and `fbMutOdoVecdimsAddInLeafU2Ptr` --- and on the control half a ninth, `fbFused`. Of the refusals, eight on each half carry a `--loose` family of five `fillStage2` variants, which the bytes cannot choose between, and eleven on the basis and seven on the control are 60- to 63-byte bodies at offset 40 or 48 for which no twin holds a copy or a signature. So the straddle count doubled against Run 38 on both halves alike, the switch and the source having moved together, and the new straddlers sit in `fillStage2`'s variants and in bodies no twin names. **The basis half's own twin holds FEWER loops than the binary it names for**, 330 against 338, so `--match` refuses the population comparison there and each name rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408538 on `run39-gheadnospec`, 9.992 times apart, which is plain -O1; on `run39-gheadtwopass` the same two read 2408978 against 2408538, EQUAL TO THREE FIGURES, which is SpecConstr having fired. All four figures are Run 38's to the byte. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.31 us** on `cnn-slice-c32`, **3.67 ms** on `cnn-L2-24x24-c32` and **39.5 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 20 to 21 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.48 us | 6.31 us | 4.99 us |
| `cnn-L2-24x24-c32` | 165888 | 3.77 ms | 3.67 ms | 2.90 ms |
| `stretch-wide-2xM` | 1800000 | 40.5 ms | 39.5 ms | 31.6 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.53 ms raw and 4.38 ms net; `bcast-inner900` 30.7 ms and 29.6 ms; `bcastmid-b200k` 49 ms and 47.9 ms; `window-128x128-k7` 14.2 ms and 13.8 ms; `scaled-rank1-m1` 5.35 ms and 5.17 ms; `runs-2` 40.7 ms and 39.7 ms; `flip-fwd-rows96` 30.9 ms and 29.8 ms; `block-r3-vol64` 4.61 ms and 4.45 ms; `small-row96` 6.69 us and 6.46 us; `compose-zero-mid` 30.9 ms and 29.8 ms. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and NOT ONE cell of the whole run is one the reader flags.** The two `sum-only` arms agree to within **0.05%** on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9997 on `block`'s basis to 1.0005 on `scaled`'s across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. **NO cell of any population on either half sits below R2 0.99 ([what that column detects][ramp]), and none is under ten samples** --- 0 of the run's 4960 cells on each count, which is 2480 on each half, as on Run 38. So nothing in this run's time columns is set aside for how it resolved.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, 0 cells refused, at a cost of 1373s on the basis and 1124s on the control --- beside Run 38's 1386s and 1149s, on a roster three arms smaller and with this run's `-g3` twins building alongside, which an instruction count does not see. The counts geomean over the seventeen arms that carry a corrected time runs **1.1438** on `block` to **1.1691** on `window`, the main set at **1.1607** --- the basis retiring 14.4 to 16.9 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families cleanly**: the `bq-expand` trio sits at 0.8621 to 0.8636, retiring 50.63% more instructions on the basis for 29.85 to 30.08% more time; the `list` trio at 1.0028 to 1.0054, cashing all of what it saves; and the eleven others between 0.9486 and 0.9704, retiring 3.83 to 6.21 percent more on the basis while their clocks run from 0.20 points BELOW level to 1.99 above. **Read per class the same way, the rate runs 0.43 to 0.76**: the instruction saving reaching the clock is lowest on `block`, where the counted work parts by 14.38 points and the clock by 6.25, and highest on `window`, 16.91 against 12.89 --- Run 38's 0.38 to 0.73 on the same two classes, so [the open question][open] on that rate reads the same range a second time.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0000** on both halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0296** and **1.0945** on the basis and **1.0250** and **1.0708** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` on both halves, and about nine and seven on `bq-expand`. So the two passes do not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated --- on this run BEFORE the sequence rather than after it, on the same quiet box, for the reason the window paragraph gives --- and the state the preamble puts on a process comes back at a geomean of **1.1211** on the basis and **1.1635** on the control, **4.2** points apart, where Run 38's two parted by 4.3 and Run 37's by 5.2 --- so the two passes change what the spray costs a process as well as what the roster costs it, and by within a point of what they changed it by on each of the two runs before. What the roster adds on top of that state is **1.0174** on the basis, 4 of 19 shapes above 1, and **1.0098** on the control, 9 of 19; the basis's rest runs 0.9737 on `stretch-bigstride` to 1.2278 on `stretch-r5-8x432`, the control's 0.9807 on the same first shape to 1.1348 on `stretch-tall-Mx2`. The whole in-process deflation is **1.1406** on the basis, 17 of 19 shapes above 1, and **1.1749** on the control, 18 of 19.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 38's with `LOOP_SETTLED=1` on both halves, the owner's declaration of 2026-09-22, and THIS ENTRY IS ITS ONE DECLARATION SITE by the ruling of 2026-09-19. Both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, one source, one shim, `align-as.py` at fe6d133 or later, under Run 38's four switches with `LOOP_SETTLED=1` added to both lines --- `LOOP_EXITSPAN=1` staying and inert under the settled cost, as `LOOP_MAXSKIP` and `LOOP_LOOKTHROUGH` are under the dead-spot form, the basis built with it on the line checksumming identical to one built without --- the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run39-gheadnospec` and `run39-gheadtwopass`. So the pair's own `cross` figure is the two passes read a fourth time, under the new basis, and the switch itself is read as each half against Run 38's same half, `--half-movers run39 run38`, post-run step 4a's instrument and here the run's first reading. The switch is in [the shim's docstring](../align-as.py), its four controls in `defects.py`: the block rules plus three rules for the back edge's own bytes, the spot fewest jumps cross, and the plan settled against the assembler, which the shim reads back through one to three more probe assemblies, a half building in some three minutes and a quarter where the exit span's took one. On 2026-09-22's builds from Run 38's recipes it placed 776 heads on the basis and 836 on the control at residues the block rules would not. **What the run predicts.**

(1) *The fill cell on `stretch-wide-2xM` comes back to Run 37's level on both halves.* Under the switch the three fill heads read land at residue 0 on both halves, and those builds read `lib-stage2-lean` and `lib-stage3-lean` there at 9.6 to 10.0 million cycles an iteration on both, level with `lib-stage2-lean-u1`, where Run 38 read 11.5 to 12.9. `predict: cell stretch-wide-2xM/lib-stage2-lean over stretch-wide-2xM/lib-stage2-lean-u1 1.0 within 5% on main both` and `predict: cell stretch-wide-2xM/lib-stage3-lean over stretch-wide-2xM/lib-stage2-lean-u1 1.0 within 5% on main both`, the cell against the loop the run left at 9.5 on both halves, with `predict: pair lib-stage3-lean lib-stage2-lean 1.0 within 2% on main basis`, Run 38's item (6) under the new basis.

**Read by --predictions, item (1):** `cell stretch-wide-2xM/lib-stage2-lean over stretch-wide-2xM/lib-stage2-lean-u1 1.0 within 5% on main both`: HELD on main basis, read 1.0259 over 1 shape(s), 2.59 point(s) off, within 5.00%; HELD on main control, read 1.0301 over 1 shape(s), 3.01 point(s) off, within 5.00% --- `cell stretch-wide-2xM/lib-stage3-lean over stretch-wide-2xM/lib-stage2-lean-u1 1.0 within 5% on main both`: HELD on main basis, read 1.0305 over 1 shape(s), 3.05 point(s) off, within 5.00%; HELD on main control, read 1.0393 over 1 shape(s), 3.93 point(s) off, within 5.00% --- `pair lib-stage3-lean lib-stage2-lean 1.0 within 2% on main basis`: KILLED on main basis, read 0.9790 over 19 shape(s), 2.10 point(s) off, within 2.00%.

(2) *The back edge's rules hold beyond the loop that fixed them, which is the bet the switch takes.* The first rule was read on a `jl` and the other two on a `jmp`, and the switch charges all three to any back edge: on `.LQeN1`, a 63-byte loop whose `jne` sits in its head line's last bytes, that makes residues 0 and 1 costly where every earlier cost called them free, and no reading has priced a `jne` there. The reading is each half against Run 38's same half over the eleven populations, a switch that moves heads on both halves alike leaving a one-half mover to the instance, which `--half-movers` names, and a two-half mover to the rules: `script: probe-r39-rules.py`, run as `./probe-r39-rules.py run39 run38`, lists every arm slower past the chapter's 3% mover bar on BOTH halves, and each is then read by `LOOP_TRACE` on its hot loop's head. The prediction is that none of them was moved for the first-eight or last-four rule alone; one that was is the kill, and it names the rule to retire. The bar is 3% and not the floor because the same reading of Run 38 against Run 37, the same recipes with the source moved, names nine arms at the floor and three at 3%, `flip` and `small` cells of loops no rule touched.

**Read by `probe-r39-rules.py`, item (2):** `./probe-r39-rules.py run39 run38` reads each half against Run 38's same half over all eleven populations and names **0 candidates** slower past the 3% bar on both halves; on Run 38 against Run 37 the same script names three, so the silence is a reading. No arm is left for `LOOP_TRACE` to sort.

**ONE of two items holds its sentence whole, and the other holds it with one of its three spans KILLED, by a source change the registration did not see.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs, by `--predictions` over the main set on each half and by the item's own script.

(1) *The fill cell on `stretch-wide-2xM` comes back to Run 37's level on both halves.* **HELD on both cell spans on both halves, and the pair span KILLED.** The two cells read **1.0259** and **1.0305** of `lib-stage2-lean-u1` on the basis and **1.0301** and **1.0393** on the control, inside 5% on all four readings, where Run 38 read 1.54 and 1.81 on the basis and 1.81 and 1.48 on the control, and Run 37 read `lib-stage2-lean` at 1.0060 and 0.9954 --- so the cell is back within four points of the `-u1` loop on every reading, where Run 37 read `lib-stage2-lean` within a point of it, and the loop the run left alone, `lib-stage2-lean-u1`, reads 0.799 and 0.796 ms against Run 38's 0.801 and 0.806. The switch placed every tracked fill copy at offset 0 on both halves, which is the mechanism the item named. **The pair span `lib-stage3-lean` against `lib-stage2-lean` read 0.9790, 2.10 points off a 2% band**, the control half reading 0.9783 beside it, and the kill is not the switch's: `c0a8aaa`, committed after the registration, rebuilt the inward fill behind `lib-stage3-lean` as one table of pairs while `lib-stage2-lean`'s fill keeps two, so the span priced one variable where this run carries two. The item's sentence is about the cell and the cell holds; the killed span records that the table form is worth about two points to the fill.

(2) *The back edge's rules hold beyond the loop that fixed them, which is the bet the switch takes.* **HELD**, and vacuously for its kill: the script names no arm slower past 3% on both halves in any population, so no arm was moved by the first-eight or last-four rule alone and no rule is named for retirement. What the item cannot say is that a rule was TESTED on a `jne`: the one loop it named, `.LQeN1`, belongs to no candidate, so the bet stands unrefuted rather than confirmed.
