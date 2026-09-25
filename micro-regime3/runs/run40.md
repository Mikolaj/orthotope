# Run 40 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 40 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source, launched from disk): the two passes are worth some thirty points on both `list` and `bq-expand`, ALL FOUR registered spans hold, and on the main set the ten source commits moved the fills they rewrote and nothing else.** The pair is Runs 36's to 39's IN ITS VARIABLE --- one source, `Main.hs` at `bb6b12e`, one shim at `fe6d133` under five switches with the exit span and the settled cost, ONE compiler, `10.1.20260918`, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the seventeen main-set arms that carry a cross-half figure, SIX move with the families and ELEVEN do not: the six are the `list` and `bq-expand` families entire, at **1.2983** to **1.3091**, and the eleven others span **1.0016** to **1.0138**, every one of them a fill. **The bar an arm has to clear to be the passes' rather than the run's is 0.85 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.64% on each half and measured WITHIN one half --- and six of the nine arms that are not A/A copies clear it: the two families, `mut-odo-vecdims` at 1.0125, `lib-stage3-lean` at 1.0138, `lib-stage1` at 1.0118 and `lib-stage2-lean-u1` at 1.0098.

**What this run was built to settle is whether the rewritten fills' instruction savings reach the clock, and all three registration items hold, on all four spans.** `lib-stage3-lean` over `lib-stage2-lean` reads **0.9656** on the basis and **0.9564** on the control, where Run 39 read 0.9790 and 0.9783, and `lib-stage2-lean-u1` over `lib-stage3-lean` **1.0575** and **1.0617**, where Run 39 read 1.1203 and 1.1249 --- the instruction ratios the priors took off this run's own basis binary coming out to the third decimal, 0.9751 against 0.975 and 1.0206 against 1.021 --- and the regime's worth on the arms no commit touched reads `list` at 1.2983 and `bq-expand` at 1.3058 against 1.294 and 1.302 within 1%. Against Run 39's basis, the same recipe on the source before the ten commits, three rewritten fills are 1.1 to 7.0 points faster and the other fourteen timed arms within 0.65 of a point.

**One arm no item predicted moved further than any the items did, and the run itself was quiet.** `3c02e36`'s rewrite of the one-level fill sped `lib-stage3-lean-onelevel` as plain -O1 compiles it by 7 to 18% on `runs`, `flip`, `block` and `scaled` against Run 39's, on 2 to 7% fewer instructions, and left its counts as the two passes compile it where they were to the fourth decimal --- so on those four classes the pair's cross figure on that arm now reads 0.83 to 0.94, the basis the faster, and [the open list][open] asks why. A reboot sits between this run and Run 39, and the machine check read `list` at +1.05% across it, inside the bars; no bench met foreign CPU, the evening running in one window in the order the run list gives.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE and the BOOT**: the compiler is Runs 36's to 39's in-tree stage1 `10.1.20260918` unmoved, and the shim `align-as.py` at `fe6d133` with its five switches, the project file `cabal.project.ghead`, the regime and the launch from disk are Run 39's. What moved is `Main.hs`, from `c870e1e` to `bb6b12e` in ten of the owner's commits, which moved no arm in or out, and the box, rebooted between the runs. **Read against the half Run 39 built by this same recipe, three rewritten fills moved and nothing else did**: over the 17 arms that carry a corrected time, this run over that one reads `lib-stage2-lean-u1` at **0.9300**, `lib-stage3-lean` at **0.9853** and `lib-stage3-lean-onelevel` at **0.9892** --- below 1 meaning this run is the faster --- and the other fourteen within 0.65 of a point; read as a ratio to `list` within each run, which cancels a box term exactly, the sixteen others give a `--bridge` geomean of **0.9904** with `lib-stage2-lean-u1` alone outside both the 3.3% drift band Run 11 measured and the 2.1% Run 23 read on one binary. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run40-gheadnospec`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **NONE of the thirty-one rows is a first reading**: the roster is Run 39's unmoved, the same thirty-one arms in the same order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every row has a twin in Run 39's file.

**Comparing runs?** The table below is Run 40's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.64%** from 1 on the basis half or **0.64%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one COINCIDE on the basis and part on the control this run**: over the four pairs that carry back to Run 10 the two halves read **0.64%** and **0.37%**, `mut-odo-vecdims-aa` carrying both of the basis's figures and `bq-expand-aa-distant` the control's, whose whole-set figure `list-aa-distant` carries. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **3.23%** on `cnn-L1-24x24-c1` on the basis and **5.78%** on `stretch-r5-8x432` on the control --- are not floors at all and are not to be quoted as any. Its two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.52* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.58 | 69 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.57 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.62 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.67* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.024 | 0.114 | 0.57 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.114 | 0.48 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage1 | 0.024 | 0.114 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| lib-stage3-lean-onelevel | 0.024 | 0.113 | 0.65 | 70 | 1.00x | new mutating `Vector` method -- `lib-stage3-lean` over the fill that skips its level tables at one level, against `lib-stage3-lean` |
| lib-stage2-lean-u1 | 0.025 | 0.112 | 0.59 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.114* | *0.49* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.113* | *0.56* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.114 | 0.45 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.47* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.43* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.112 | 0.40 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.128 | 0.260 | 0.67 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.128* | *0.260* | *0.64* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.129* | *0.260* | *0.34* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.70 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.007* | *0.73* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.002* | *1.009* | *0.63* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run FIVE of the 120 pairs among the sixteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 39's basis parted on eleven of its 120, Run 38's on one, Run 37's on five of 105 and Run 36's on two. **The cap is what moved**: eight rows have three or four of their nineteen cells capped, the five `lib-` fills and the shipped leaf with its two copies, and the published figures sit 6.4 to 14.6 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms. `lib-stage1` over `lib-stage3-lean-onelevel`, for one, reads **0.9955** on the column against a paired **1.0918**. **The widest disagreement of any kind sits on the row the cap moved furthest**: `lib-stage1` over `list-aa-distant` divides to **0.0243** on the column where the paired figure is **0.0285**, the column 14.6% under it, `lib-stage1`'s published figure sitting 14.6 points under its plain geomean. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads fourteen of the seventeen rows moved against Run 39's table, `lib-stage1` by 2.5 points, where `--compare` against the JSON of the half Run 39 built puts that arm at 0.9993 and `list` at 1.0055.

**This run's two columns may be differenced on NONE of the eleven populations, as Runs 36's to 39's could not, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **29.83 points** on the main set and by 24.82 on `bcastmid` to 33.13 on `bcast` over the ten classes, every one of the eleven figures past the bar by a factor of thirty-five or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's. **That is the bar working rather than failing**: it exists to stop a margin being read off two columns with different denominators, and a pair built to move the denominator is the case it was written to refuse.

`concat-runs` has no row, and neither do the other 81 arms the roster holds and checks without timing --- **82 of its 113** in all, as on Run 39: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **No arm joined or left the timed roster**, the ten commits rewriting fills behind timed arms and none of the roster's membership: `roster-delta.py`, read off the two binaries, reads 31 arms to 31 over 19 shapes to 19, in the same order, and the sixty-one class views unmoved over the same ten classes. A movement against Run 39's own basis column is therefore a movement on the **17 shared arms that carry a corrected time**, with a source term and a boot term between the two runs and no compiler, shim, project-file or launch term --- and a movement across THIS run's two halves is the two passes, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is a FOUR-WAY TIE**: `lib-stage3-lean`, `lib-stage2-lean`, `lib-stage1` and `lib-stage3-lean-onelevel` all read 0.024 and are separated only on the unrounded values, 0.02373, 0.02385, 0.02436 and 0.02447, with `lib-stage2-lean-u1` at 0.025 and the shipped leaf at 0.026 --- **six timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, as on Run 39. **Paired on the basis the head is not a tie**: `lib-stage3-lean` over `lib-stage2-lean` is **0.9656** at 14 of 19 and p 0.064, and `lib-stage2-lean` over the shipped leaf **0.9307** at 14 of 19 and over `lib-stage1` **0.9315** at 12 of 19 --- so the pairs put the inward fill first by three and a half points, which is registration item (1) holding. **The third is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6333** on the basis and **0.6376** on the control, 0.43 of a point apart on a pair that moves `list` by thirty points, the control's figure inside the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 and the basis's 0.25 of a point under it --- a span carried from that file and not re-derived here.

**The ten commits reached the clock where the registration said, and in one place no item predicted.** Against Run 39's basis, the same recipe on `c870e1e`, `lib-stage2-lean-u1` reads **0.9300**, the one arm outside the 3.3% drift band, its gain on `cnn-slice-c32` at 0.632 and `cnn-L1-6x6-c1` at 0.684, and `lib-stage3-lean` **0.9853** --- which is registration items (1) and (2) holding, read across runs rather than within one. **The place no item predicted is `lib-stage3-lean-onelevel` on the BASIS half.** `3c02e36` routed the one-level fill through the odometer, and against Run 39's same half the basis runs the arm at **0.8235** on `runs`, **0.8585** on `block`, **0.8695** on `flip` and **0.9279** on `scaled`, retiring 7.2%, 5.1%, 5.8% and 2.4% fewer instructions, while the control half's counts on those four classes are Run 39's to the fourth decimal and its clock moves under a point and a tenth. So the rewrite reached what plain -O1 emits and not what the two passes emit, and the cross-half figure on the arm turns over on those classes, to 0.8255, 0.8762, 0.8649 and 0.9402 --- the basis now clearly the faster, where Run 39 read the four at 0.9964 to 1.0095. On the main set, where the arm's shapes are mostly many-level, it moves 1.1 points against Run 39 and its cross-half figure reads 1.0052.

**The fifteen half-local movers against Run 39 are two kinds, and the copy test, taken 2026-09-25 after the write-up on a quiet box, splits the second.** `--half-movers run40 run39` flags fifteen arm-populations past 3% on ONE half each. **Six are count-led, the source's**: the four `lib-stage3-lean-onelevel` basis cells above, `lib-stage1` on `rev`, 3.4% faster on the basis with its counts down 2.3% on both halves, and `lib-stage1` on `small`, 6.3% faster on the control with its counts down 5.4% there and 5.0% on the basis, whose clock stays level. **Nine have their counts level**: `lib-stage3-lean-onelevel` on the basis 3.3% and 4.2% slower on `bcast` and `bcastmid`; `mut-odo-vecdims` and both its A/A copies 3.2 to 3.4% faster on the basis on `flip`, the three together, so not a slot; on the control, `list-aa-distant` 3.4% slower on both `block` and `flip`, `lib-stage3-lean` 4.1% faster on `block` and `mut-odo-vecdims-add-in-leaf-u2-aa-distant` 3.3% faster on `scaled`. A mover with its counts level is that half's binary, its file instance or its process and not the pair's variable. `probe-r40-instance.sh` timed the widest cell of eight of the nine --- the `flip` trio by the arm and one copy --- in cycles an iteration, the difference of an `-n 2N` and an `-n N` process over three interleaved passes, on the timed file, a fresh copy of it and Run 39's same half. **The copy reads with the timed file on every cell outside `flip-last-rows`, 0.993 to 1.006 of it, so no mover is the file instance.** **ONE is this run's BUILD**: on `bcast-tall-Mx2` Run 39's basis runs `lib-stage3-lean-onelevel` at 0.918 of this run's in fresh processes, the evening's 1.238 moving the same way further. **FOUR are the evening's PROCESS**, Run 39's binary reading 0.998 to 1.004 of this run's in fresh processes: `lib-stage3-lean-onelevel` on `bcastmid-block150k`, `list-aa-distant` on `flip-last-rows`, `lib-stage3-lean` on `block-run64-off7` and the leaf's distant copy on `scaled-super-r3`. **The `flip` trio's cell is `flip-last-rows`, which re-rolls per process**: its passes spread 11.1 to 13.9 million cycles on both binaries, and in fresh processes Run 39's reads 0.89 of this run's where the evening read this run 0.86 of Run 39's, so the three copies' move is that cell's re-roll and no binary's. `list-aa-distant` on `block-run64-gap1` stays open, Run 39's reading 0.968 of this run's inside passes that spread 15%. **Step 4b's cells read the same way**: the time-led cells with counts level are two unordered consumers on `runs-3`, `libunord-stage6-sum` at 1.3992 and `-stage7-sum` at 1.3693 across the halves, on the cell where the control half's R2 warnings fell, and the count-led cells are led by the `bq-expand` family's, whose counts the two passes move by up to 132%.


## What the next run compares against

**Run 40's pair is Run 39's rebuilt on the changed source, [registered 2026-09-24](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of that day, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; `Recommended tasks after Run 40` is NOT that site and holds post-mortems, which is [an open entry](../README.md#what-is-open) of its own. What this run leaves as the reference is `run40-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `bb6b12e`, the shim at `fe6d133` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **It is the fifth published basis on that compiler, and the step from the fourth is the source and a reboot and nothing else**: against `run39-gheadnospec`, the same recipe on `c870e1e`, fourteen of the seventeen timed arms read within 0.65 of a point of 1, and three fills the ten commits rewrote do not --- `lib-stage2-lean-u1` at **0.9300**, `lib-stage3-lean` at **0.9853** and `lib-stage3-lean-onelevel` at **0.9892**, below 1 meaning this run is the faster, `--bridge` putting the first alone outside the 3.3% drift band. `lib-stage2-lean-u1`'s gain sits on the two smallest main-set shapes, `cnn-slice-c32` at 0.632 and `cnn-L1-6x6-c1` at 0.684, with three shapes past a point slower, `stretch-inner256` at 1.167, `stretch-primes` at 1.048 and `stretch-pow2stride` at 1.012. **The pair itself is Runs 36's to 39's, built a fifth time**, and its draws are `./read-run.py --record regime`'s, a row per build: this one lands among the four before it on both families, and Run 36's stays the outlier. Against Run 31's whole-level **1.2974** the four later `list` draws straddle the level, so **the level's other passes still do not measurably hand `list` back**. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918`, as Runs 36's to 39's were --- and the step this run reads is not a compiler step at all.** The tally of pairs BUILT to ask the compiler stands where Run 35 left it, at TEN. **What this run adds is the pair's fifth build, on a source ten commits on under Run 39's shim and cost**: Runs 36 to 40 are the same two recipes on the same compiler, Run 39's and this one's with the settled cost on both, and their cross-half readings agree to 1.21 points on `bq-expand` and, Run 36's wild cell set aside, to 0.80 on `list` over the four later draws. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim cost and now the source together. **The REGIME variable has now been asked EIGHT times.** Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s five rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and the four later HEAD draws straddle the level on the eighteen shapes where Run 36 read above it.

**What Run 40 leaves the next run to read against, and the first item is a check that did NOT fire across a reboot.** A reboot sits between Run 39 and this run, and the gate says the box still measures as it did: read against the fingerprint Run 39 installed, the machine check that `run-gate.sh` runs on the gate's basis-half `a` JSON puts `list`'s net at **+1.05%**, worst `cnn-L2-24x24-c32` at **+2.44%**, 0 of 19 shapes past 5% and the geomean inside the 3% bar; the main-set JSON reads the same check at +0.56% with `vgg-14-c512-k3` worst at +1.34%. **This reading carries a source term and a boot term**: Run 39's basis is this basis's recipe on `c870e1e`, and `list` runs no code the ten commits changed, so `list` holding level is the reboot's reading and says nothing of the fills, which moved and which the check does not read. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 40's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **All four spans held, on every population and half their scope names**, and the priors behind items (1) and (2) were instruction counts off this run's own basis binary, taken after the build --- the form the preparation adopted when a registration's first priors, off a twin build since deleted, stopped resolving. **What a next registration should take from this one is that a prior taken off the binary the run times survives the run**: both items drawn on it held on both halves, where Run 39's one span priced on the previous run's source died to a commit made after it.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 40**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918`, on `Main.hs` at `bb6b12e`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 39 published a HEAD half on this basis's recipe, so the two published columns carry no compiler and no shim term, only the source and the reboot. Over the **17 arms both rosters time and both give a corrected time** it runs from **0.9300** on `lib-stage2-lean-u1` to **1.0065** on `list-aa-adjacent`, below 1 meaning this run is the faster, the three rewritten fills 1.1 to 7.0 points faster and the other fourteen within 0.65 of a point. **The table below is this run's own two halves and no earlier run's**, eight strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 40 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918) | Run 40 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.032 |
| `lib-stage1` | **0.024** | 0.032 |
| `lib-stage2-lean` | **0.024** | 0.030 |
| `lib-stage2-lean-u1` | **0.025** | 0.031 |
| `lib-stage3-lean` | **0.024** | 0.030 |
| `lib-stage3-lean-onelevel` | **0.024** | 0.031 |
| `bq-expand` | **0.128** | 0.127 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on seven of the eight rows, the control higher on each of those seven, while `bq-expand` prints 0.128 and 0.127, the one arm whose own move keeps pace with the denominator's; in absolute terms the flagged half is the faster on every one of the seventeen timed arms, `--compare` putting all seventeen above 1. **Read DOWN a column and the head is a four-way tie at 0.024 on the basis** --- `lib-stage3-lean`, `lib-stage2-lean`, `lib-stage1` and `lib-stage3-lean-onelevel` --- and a two-way one at 0.030 on the control, `lib-stage2-lean` and `lib-stage3-lean`; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, the two-column table above carrying eight of its rows and every other published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6376** (0.6333); `lib-stage1` against `-u2` **0.9932** (0.9992); `lib-stage2-lean` against `-u2` **0.9322** (0.9307) and against `lib-stage1` **0.9385** (0.9315); `lib-stage3-lean` against `lib-stage2-lean` **0.9564** (0.9656); `lib-stage3-lean-onelevel` against `lib-stage3-lean` **1.0271** (1.0183); and the headline pair README's opening leads with, `bq-expand` against `mut-odo-vecdims`, **2.2015** (2.8391), 0 of 19 shapes to `bq-expand` on either half. **All seven hold their direction across the halves**, the six besides the headline pair each moving under a point; the headline pair moves by 63.8 points, which is the pair's own variable rather than an ordering that shifted. **The one-level fill now reads BEHIND `lib-stage3-lean` on both halves**, by 1.8 points on the basis and 2.7 on the control, at sign p 1 and 0.65, so the lead the nest took is not one the win counts separate.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.33 us | 0.079 | `lib-stage3-lean` 0.046 | `mut-odo-vecdims-add-in-leaf-u2` 0.054 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.64 us | 0.091 | `lib-stage3-lean` 0.044 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 119 us | 0.064 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 390 us | 0.044 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 463 us | 0.048 | `lib-stage3-lean-onelevel` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.030 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.71 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.33 ms | 0.025 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17.1 ms | 0.040 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 20 ms | 0.053 | `lib-stage1` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.9 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.6 ms | 0.023 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.1 ms | 0.112 | `lib-stage2-lean-u1` 0.112 | `mut-odo-vecdims` 0.112 |
| `stretch-r5-8x432` | 8 | 1769472 | 48.3 ms | 0.021 | `lib-stage2-lean-u1` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.9 ms | 0.088 | `lib-stage3-lean-onelevel` 0.073 | `mut-odo-vecdims-add-in-leaf-u2` 0.078 |
| `stretch-bigstride` | 3 | 1800000 | 51.1 ms | 0.032 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.9 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41.2 ms | 0.021 | `lib-stage3-lean-onelevel` 0.020 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.8 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 936 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.2 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.5 ms | 0.019 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.2 ms | 0.019 | `lib-stage3-lean-onelevel` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.7 ms | 0.015 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.7 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.65 ms | 0.053 | `lib-stage2-lean-u1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.25 ms | 0.019 | `lib-stage3-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 48.1 ms | 0.034 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.3 ms | 0.021 | `lib-stage1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.22 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage3-lean-onelevel` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.34 ms | 0.029 | `lib-stage3-lean-onelevel` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.46 ms | 0.020 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 942 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 944 us | 0.029 | `lib-stage3-lean-onelevel` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.4 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 30 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.33 ms | 0.026 | `lib-stage3-lean-onelevel` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.3 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.052 | `lib-stage3-lean-onelevel` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.3 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30.2 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.2 ms | 0.042 | `lib-stage2-lean` 0.041 | `mut-odo-vecdims` 0.042 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 119 us | 0.064 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 460 us | 0.048 | `lib-stage3-lean-onelevel` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.34 ms | 0.025 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.3 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.4 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.7 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 29 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 29.1 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-256` | `runs` | 256 | 1799936 | 29.1 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-7` | `runs` | 7 | 1799994 | 32.8 ms | 0.032 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 40.1 ms | 0.057 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 36.2 ms | 0.046 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-32` | `runs` | 32 | 1800000 | 30.2 ms | 0.025 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.4 ms | 0.040 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.9 ms | 0.025 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.5 ms | 0.038 | `lib-stage3-lean-onelevel` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.4 ms | 0.025 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 32 ms | 0.030 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-96` | `runs` | 96 | 1800000 | 29.5 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.6 ms | 0.025 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 269 us | 0.029 | `lib-stage3-lean-onelevel` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.16 ms | 0.028 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.96 us | 0.078 | `lib-stage3-lean` 0.046 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-bcast32` | `small` | 32 | 256 | 4.4 us | 0.051 | `lib-stage3-lean-onelevel` 0.038 | `mut-odo-vecdims-add-in-leaf-u2` 0.045 |
| `small-flat64` | `small` | 64 | 256 | 4.41 us | 0.060 | `lib-stage2-lean` 0.008 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.32 us | 0.088 | `lib-stage2-lean-u1` 0.056 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.46 us | 0.041 | `lib-stage2-lean-u1` 0.036 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 281 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 956 us | 0.088 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.45 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.6 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.8 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.7 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.5 ms | 0.053 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 39 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the TEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FOURTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names three different `lib-` arms --- `lib-stage3-lean` on FIVE rows, `lib-stage3-lean-onelevel` on four and `lib-stage1` on one --- where Run 39 named `lib-stage3-lean` on six, `lib-stage3-lean-onelevel` on two, `lib-stage2-lean` on one and `lib-stage1` on one. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 40's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in the same eleven populations Runs 36 to 39 broke it in, at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9954**, where the control reads **0.9818**. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw, inside half a point. Every other shape of every population reads the clause with room, the classes' closest cells at 0.28 to 0.49 on the basis. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` is slower than `list` on `runs-2` on both halves, at **1.1061** on the basis and **1.3557** on the control, and on `runs-3` on the CONTROL half alone at **1.1312**; `--over-list` reads every other one of the 1280 timed non-control cells this run carries, over all eleven populations on both halves, at or under 1. **They are the same three cells Runs 36 to 39 read**, `--over-list` on each run giving its own, **and it is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0347 between the halves while `list` moves 1.2682, and on `runs-3` the fill moves 1.0271 against `list`'s 1.2812.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the tenth run running that this property is the one left entirely alone.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits under 0.053. The `bq-expand` clause is closest at `small-row96` on the CONTROL half, **1.00441**, then `scaled-rank1-m1` at 1.00003 on both halves, and `stretch-tall-Mx2` at 1.00000 on both halves of the main set with `bcast-src8` at 1.00000 on the control. **Those five figures are Runs 36's to 39's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, the ten commits having rewritten no code behind `mut-odo-vecdims`, `bq-expand` or `list`. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in all ten classes and on the main set, on both halves --- and their LEVEL clause BREAKS in every one of the eleven populations, as it did on Runs 36 to 39, and on Run 31 before them, where registration (10) died on it.** The order clause is untouched: the mutable fills sit at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 19.00x to 27.66x, on both halves and in every population, `small` outside the LEVEL clause by the ruling of 2026-09-07 as before. What breaks is the level: **the two passes change what `list` and `bq-expand` ALLOCATE, and this run reads that change at Run 31's own figures.** On the main set the fills read 1.00x on both halves while `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the nineteen shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 39's to the fourth decimal.

**AND SIX ARMS OUTSIDE THE TWO FAMILIES MOVE, all of them unordered consumers, as on Run 39 and on Run 38 with a seventh since parked.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.8053** of the basis on `libunord-stage6-sum`, 0.8064 on `-stage6-loop-sum`, 0.8067 on `-stage7-sum`, 0.8413 on `-stage9-sum`, 0.8447 on `-stage13-sum` and 0.8448 on `-stage14-sum`, where `libunord-stage1-sum` reads 0.9992 and every ordered consumer and every fill reads 0.9988 to 1.0005. Beside Run 39's figures the first moves by 0.16 of a point and the third by 0.01 --- `runSlices`'s odometer, behind every one of them, being among what the ten commits rewrote --- and the other four not at all. **In absolute terms it is 408 to 2935 bytes a call on the basis main set** and the whole family sits at the 0.01x tier, so no tier moves and no property verdict changes with it. `--alloc` puts 252 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 40 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 24.82 points on `bcastmid` at narrowest and 33.13 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 39, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **170 arm-comparisons, 26 putting the basis faster and 144 slower**, with no degenerate arm excluded, at geomeans from **1.0519** on `block` to **1.1318** on `window` and extremes of `lib-stage3-lean-onelevel` at **0.8255** on `runs` and `bq-expand-aa-distant` at **1.5281** on `window`; the low extreme is `lib-stage3-lean-onelevel` in four of the ten, the four on which the ten commits sped the arm on the basis by 7 to 18% while it stood still on the control. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **No registration of this run names a class**: every span is `on main`, so each block below carries its properties, its floor and its own cross-half reading.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **In practice the bold marks the FASTER of the two named arms, one cell a row**, and on this run it is the arm outside the family on ALL TEN --- `lib-stage3-lean` on `rev`, `bcast`, `bcastmid`, `window` and `compose`, `lib-stage3-lean-onelevel` on `runs`, `flip`, `block` and `small`, and `lib-stage1` on `scaled`. **The family's ceiling is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Run 39. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.043 | 0.064 | **`lib-stage3-lean`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.30% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.81% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage3-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 | 1.19% |
| `window` | 8 | 0.051 | 0.088 | **`lib-stage3-lean`** 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.56% |
| `scaled` | 3 | 0.026 | 0.029 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.36% |
| `runs` | 17 | 0.025 | 0.057 | **`lib-stage3-lean-onelevel`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.26% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage3-lean-onelevel`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.87% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage3-lean-onelevel`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.76% |
| `small` | 5 | 0.061 | 0.088 | **`lib-stage3-lean-onelevel`** 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 | 0.30% |
| `compose` | 4 | 0.023 | 0.029 | **`lib-stage3-lean`** 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 | 0.62% |

The best arm outside the family is ahead of `mut-odo-vecdims` in every one of the ten classes. **No row's bold sits in the CEILING column this run**, as on Run 39. FIVE rows change the arm they name: `bcastmid` names `lib-stage3-lean` where Run 39 named `lib-stage2-lean`, `window` names `lib-stage3-lean` where it named `lib-stage3-lean-onelevel`, and `runs`, `flip` and `block` name `lib-stage3-lean-onelevel` where it named `lib-stage3-lean` --- so the nest takes `window` from the one-level fill and `bcastmid` from `lib-stage2-lean`, and the one-level fill takes three rows from the nest, on margins the class paragraphs below price. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **No row ties at three decimals this run**, the closest being six rows a thousandth apart --- `rev`, `bcast`, `scaled`, `runs`, `block` and `compose`, so every bold is a lead a reader of the table can see.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.09 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.11 | 148 | 1.01x |
| liblist-stage5-sum | -- | -- | 0.15 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.08 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.04 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *158* | *0.00x* |
| lib-stage3-lean | 0.021 | 0.026 | 0.10 | 148 | 1.00x |
| lib-stage2-lean | 0.022 | 0.027 | 0.09 | 148 | 1.01x |
| lib-stage3-lean-onelevel | 0.022 | 0.028 | 0.07 | 148 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.041* | *0.06* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.041 | 0.06 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.041* | *0.08* | *147* | *1.00x* |
| lib-stage1 | 0.023 | 0.037 | 0.10 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.024 | 0.028 | 0.10 | 147 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.05* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.064* | *0.05* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.043** | 0.064 | 0.05 | 138 | 1.00x |
| bq-expand | 0.140 | 0.239 | 0.10 | 122 | 3.22x |
| *bq-expand-aa-adjacent* | *0.140* | *0.239* | *0.13* | *123* | *3.22x* |
| *bq-expand-aa-distant* | *0.140* | *0.240* | *0.07* | *122* | *3.22x* |
| list (baseline) | 1.000 | 1.000 | 0.17 | 85 | 26.11x |
| *list-aa-adjacent* | *1.001* | *1.003* | *0.14* | *85* | *26.11x* |
| *list-aa-distant* | *1.002* | *1.004* | *0.18* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0030, worst cell 0.76% on `rev-cnn-L1-24x24-c1`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.03% on `rev-gather48-src-50`, its interval covering 1. The in-situ term reads 1.0022, 1.0154 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0026, which the correction amplifies by 1.23x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m7s, peak 96 MiB in use, 25 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.49 ms per call raw, 4.34 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.048/0.025

**Across the halves:** 4 of the 17 arms are faster on this half and 13 slower, at a geomean of 1.0982, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9986 to `bq-expand-aa-distant` at 1.3139, with `list` itself at 1.2720. **The baseline moved 27.20% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.064, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage3-lean` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.5034 over 3 of 3 shapes at sign p 0.25, a margin of 49.66% against this class's 0.30% floor (`bq-expand-aa-distant`). `lib-stage3-lean` leads outside the family here as on Run 39, and the class's one half-local mover against that run is `lib-stage1`, 3.4% faster on the basis with its counted work down 2.3% on both halves. Its two columns may NOT be differenced, `list` having moved 27.20 of a point, at a class geomean of 1.0982 over the 17 arms, with 4 of 9 strategies past an A/A bar of 0.70 points. The counted work reads a counts geomean of 1.1591 over the same arms, 17 of them counted. Its counted work parts by 15.91 points where its clock parts by 9.82, so about 0.62 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.25* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.015 | 0.020 | 0.49 | 62 | 1.00x |
| lib-stage3-lean-onelevel | 0.015 | 0.020 | 0.47 | 62 | 1.00x |
| lib-stage2-lean | 0.015 | 0.020 | 0.39 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.40* | *62* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.56* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.41 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.41 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.48 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.021* | *0.056* | *0.33* | *61* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.056* | *0.34* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.07 | 61 | 1.00x |
| bq-expand | 0.092 | 0.141 | 0.66 | 46 | 1.00x |
| *bq-expand-aa-adjacent* | *0.092* | *0.141* | *0.69* | *46* | *1.00x* |
| *bq-expand-aa-distant* | *0.092* | *0.142* | *0.05* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.07 | 17 | 20.99x |
| *list-aa-distant* | *1.005* | *1.010* | *0.87* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.008* | *1.013* | *0.79* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0081, worst cell 1.10% on `bcast-tall-Mx2`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.03% on `bcast-tall-Mx2`, its interval covering 1. The in-situ term reads 1.0204, 1.0090 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0059, which the correction amplifies by 1.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m11s, peak 169 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.6 ms per call raw, 29.5 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.015/0.019/0.019

**Across the halves:** 1 of the 17 arms are faster on this half and 16 slower, at a geomean of 1.0819, from `lib-stage2-lean-u1` at 0.9998 to `list-aa-distant` at 1.3699, with `list` itself at 1.3313. **The baseline moved 33.13% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6550 over 6 of 6 shapes at sign p 0.031, a margin of 34.50% against this class's 0.81% floor (`bq-expand-aa-distant`). `lib-stage3-lean` leads here as on Run 39, and `lib-stage3-lean-onelevel`, that run's low cross-half extreme on this class, reads 3.3% slower on the basis than Run 39's with its counts level, a half-local mover. Its two columns may NOT be differenced, `list` having moved 33.13 of a point, at a class geomean of 1.0819 over the 17 arms, with 2 of 9 strategies past an A/A bar of 2.89 points. The counted work reads a counts geomean of 1.1638 over the same arms, 17 of them counted. Its counted work parts by 16.38 points where its clock parts by 8.19, so about 0.50 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.54* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.29 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.38 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.28 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 97 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.25* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *89* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *89* | *0.00x* |
| lib-stage3-lean | 0.012 | 0.018 | 0.31 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.020 | 0.30 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.31 | 82 | 1.00x |
| lib-stage2-lean | 0.012 | 0.018 | 0.31 | 82 | 1.00x |
| lib-stage3-lean-onelevel | 0.014 | 0.021 | 0.29 | 81 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.019* | *0.029* | *0.31* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.019 | 0.030 | 0.26 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.029* | *0.40* | *80* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.39* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.27* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.45 | 76 | 1.00x |
| *bq-expand-aa-adjacent* | *0.099* | *0.183* | *0.39* | *61* | *1.92x* |
| bq-expand | 0.099 | 0.183 | 0.44 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.184* | *0.30* | *61* | *1.92x* |
| *list-aa-distant* | *0.999* | *1.002* | *0.79* | *28* | *23.56x* |
| list (baseline) | 1.000 | 1.000 | 0.77 | 28 | 23.56x |
| *list-aa-adjacent* | *1.003* | *1.005* | *0.85* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0119, worst cell 3.57% on `bcastmid-b200k`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `bcastmid-c32-cnn`, its interval covering 1. The in-situ term reads 1.0167, 1.0834 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0094, which the correction amplifies by 1.29x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m51s, peak 125 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 49.2 ms per call raw, 48.1 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.021

**Across the halves:** 3 of the 17 arms are faster on this half and 14 slower, at a geomean of 1.0875, from `lib-stage1` at 0.9737 to `bq-expand-aa-distant` at 1.2616, with `list` itself at 1.2482. **The baseline moved 24.82% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage3-lean` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4125 over 4 of 4 shapes at sign p 0.12, a margin of 58.75% against this class's 1.19% floor (`bq-expand-aa-distant`). `lib-stage3-lean` leads outside the family here, where Run 39 named `lib-stage2-lean`, and the class carries the basis half's widest floor outside `runs`, 1.19%. Its two columns may NOT be differenced, `list` having moved 24.82 of a point, at a class geomean of 1.0875 over the 17 arms, with 6 of 9 strategies past an A/A bar of 1.25 points. The counted work reads a counts geomean of 1.1669 over the same arms, 17 of them counted. Its counted work parts by 16.69 points where its clock parts by 8.75, so about 0.52 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.37* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.17 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.20 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.16 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.15 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 106 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.05 | 106 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 94 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.05 | 102 | 0.02x |
| libunord-stage7-sum | -- | -- | 0.04 | 104 | 0.02x |
| libunord-stage9-sum | -- | -- | 0.05 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *97* | *0.00x* |
| lib-stage3-lean | 0.024 | 0.026 | 0.17 | 84 | 1.00x |
| lib-stage3-lean-onelevel | 0.024 | 0.027 | 0.15 | 84 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage2-lean | 0.024 | 0.027 | 0.16 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.028 | 0.17 | 83 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.17 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.18* | *83* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.029* | *0.19* | *83* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.050* | *0.084* | *0.15* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.088 | 0.13 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.088* | *0.16* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.176* | *0.215* | *0.31* | *57* | *3.86x* |
| bq-expand | 0.176 | 0.214 | 0.36 | 57 | 3.86x |
| *bq-expand-aa-distant* | *0.177* | *0.215* | *0.25* | *57* | *3.86x* |
| *list-aa-distant* | *0.999* | *1.005* | *0.48* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.49 | 30 | 27.66x |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.38* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 1.0056, worst cell 9.61% on `window-32x32-c64-k3`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `window-224x224-k3-d2`, its interval covering 1. The in-situ term reads 1.0086, 1.1438 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0031, which the correction amplifies by 1.55x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m29s, peak 119 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.088/0.031/0.051/0.051/0.053/0.052

**Across the halves:** 1 of the 17 arms are faster on this half and 16 slower, at a geomean of 1.1318, from `lib-stage2-lean-u1` at 0.9986 to `bq-expand-aa-distant` at 1.5281, with `list` itself at 1.3047. **The baseline moved 30.47% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the family at 0.024, priced against `mut-odo-vecdims` at 0.4109 over 8 of 8 shapes at sign p 0.0078, a margin of 58.91% against this class's 0.56% floor (`mut-odo-vecdims-aa`). `lib-stage3-lean` leads outside the family here, where Run 39 named `lib-stage3-lean-onelevel`, and this class carries the run's high cross-half extreme, `bq-expand-aa-distant` at 1.5281. Its two columns may NOT be differenced, `list` having moved 30.47 of a point, at a class geomean of 1.1318 over the 17 arms, with 2 of 9 strategies past an A/A bar of 0.82 points. The counted work reads a counts geomean of 1.1695 over the same arms, 17 of them counted. Its counted work parts by 16.95 points where its clock parts by 13.18, so about 0.78 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.14 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.16 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.15 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.12 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.18 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.18 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.21 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.23 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *138* | *0.00x* |
| lib-stage1 | 0.021 | 0.030 | 0.15 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.030* | *0.18* | *128* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.030* | *0.10* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.030 | 0.13 | 128 | 1.00x |
| lib-stage3-lean | 0.023 | 0.030 | 0.19 | 128 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.030 | 0.15 | 128 | 1.00x |
| lib-stage3-lean-onelevel | 0.023 | 0.030 | 0.13 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.030 | 0.12 | 128 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.029* | *0.08* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.029 | 0.06 | 127 | 1.00x |
| *mut-odo-vecdims-aa* | *0.026* | *0.029* | *0.12* | *127* | *1.00x* |
| bq-expand | 0.091 | 0.101 | 0.07 | 111 | 1.21x |
| *bq-expand-aa-adjacent* | *0.091* | *0.101* | *0.08* | *111* | *1.21x* |
| *bq-expand-aa-distant* | *0.091* | *0.101* | *0.07* | *111* | *1.21x* |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.14* | *69* | *21.49x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 69 | 21.49x |
| *list-aa-distant* | *1.001* | *1.001* | *0.24* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9964, worst cell 0.43% on `scaled-super-r3`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.03% on `scaled-r5`, its interval missing 1. The in-situ term reads 1.0187, 1.0086 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9985, which the correction amplifies by 2.42x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m8s, peak 111 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.34 ms per call raw, 5.16 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 1 of the 17 arms are faster on this half and 16 slower, at a geomean of 1.0662, from `lib-stage3-lean-onelevel` at 0.9402 to `list` at 1.3268, with `list` itself at 1.3268. **The baseline moved 32.68% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.9045 over 2 of 3 shapes at sign p 1, a margin of 9.55% against this class's 0.36% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). `lib-stage1` leads outside the family here, as on Runs 38 and 39, over two of the three shapes, a margin no sign test separates. Its two columns may NOT be differenced, `list` having moved 32.68 of a point, at a class geomean of 1.0662 over the 17 arms, with 8 of 9 strategies past an A/A bar of 0.83 points. The counted work reads a counts geomean of 1.1456 over the same arms, 17 of them counted. Its counted work parts by 14.56 points where its clock parts by 6.62, so about 0.45 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.38* | *52* | *1.08x* |
| liblist-stage1-sum | -- | -- | 0.11 | 61 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 72 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 61 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 70 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 72 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean-onelevel | 0.023 | 0.025 | 0.11 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.024 | 0.11 | 60 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.026 | 0.10 | 60 | 1.00x |
| lib-stage3-lean | 0.023 | 0.024 | 0.10 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.50* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.025 | 0.08 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.10* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.025** | 0.057 | 0.07 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.057* | *0.07* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.09* | *59* | *1.00x* |
| *bq-expand-aa-distant* | *0.093* | *0.142* | *0.03* | *46* | *1.08x* |
| bq-expand | 0.093 | 0.140 | 0.43 | 46 | 1.08x |
| *bq-expand-aa-adjacent* | *0.094* | *0.140* | *0.43* | *46* | *1.08x* |
| lib-stage1 | 0.099 | 1.106 | 0.24 | 51 | 1.42x |
| list (baseline) | 1.000 | 1.000 | 2.55 | 17 | 21.30x |
| *list-aa-distant* | *1.032* | *1.051* | *0.23* | *17* | *21.30x* |
| *list-aa-adjacent* | *1.033* | *1.051* | *0.20* | *17* | *21.30x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0326, worst cell 5.12% on `runs-4096`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.14% on `runs-4`, its interval covering 1. The in-situ term reads 1.0308, 1.0348 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0315, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h45m45s, peak 647 MiB in use, 289 MiB max residency; the reader reads 31 benchmarks over 17 shapes of the runs class. Anchor: `runs-2`, `list` at 41.1 ms per call raw, 40.1 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.046/0.040/0.038/0.032/0.030/0.025/0.025/0.025/0.024/0.024/0.024/0.024/0.024/0.024/0.024/0.025

**Across the halves:** 2 of the 17 arms are faster on this half and 15 slower, at a geomean of 1.0695, from `lib-stage3-lean-onelevel` at 0.8255 to `list-aa-distant` at 1.3144, with `list` itself at 1.3118. **The baseline moved 31.18% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.08x, 21.30x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7834 over 17 of 17 shapes at sign p 1.5e-05, a margin of 21.66% against this class's 3.26% floor (`list-aa-adjacent`). `lib-stage3-lean-onelevel` leads outside the family here, where Run 39 named `lib-stage3-lean`, and carries the run's low cross-half extreme at 0.8255: against Run 39 the basis runs it at 0.8235 on 7.2% fewer instructions while the control half is level on both clocks. This class also holds the three cells where `lib-stage1` is slower than `list`, on `runs-2` and `runs-3` (the properties). Its two columns may NOT be differenced, `list` having moved 31.18 of a point, at a class geomean of 1.0695 over the 17 arms, with 5 of 9 strategies past an A/A bar of 0.77 points. The counted work reads a counts geomean of 1.1507 over the same arms, 17 of them counted. Its counted work parts by 15.07 points where its clock parts by 6.95, so about 0.46 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.43* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.10 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.12 | 93 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.12 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.15 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *91* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *93* | *0.00x* |
| lib-stage3-lean-onelevel | 0.022 | 0.042 | 0.28 | 84 | 1.00x |
| lib-stage2-lean | 0.022 | 0.041 | 0.27 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.045 | 0.25 | 83 | 1.00x |
| lib-stage3-lean | 0.022 | 0.041 | 0.28 | 84 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.32* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.043 | 0.07 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.043* | *0.15* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.052* | *0.09* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.09 | 77 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.08* | *77* | *1.00x* |
| lib-stage1 | 0.033 | 0.049 | 0.23 | 81 | 1.00x |
| bq-expand | 0.090 | 0.183 | 0.43 | 60 | 1.05x |
| *bq-expand-aa-adjacent* | *0.090* | *0.182* | *0.41* | *60* | *1.05x* |
| *bq-expand-aa-distant* | *0.091* | *0.183* | *0.08* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.62 | 32 | 21.18x |
| *list-aa-distant* | *1.007* | *1.017* | *0.45* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.009* | *1.024* | *0.23* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0087, worst cell 2.44% on `flip-last-rows`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.06% on `flip-fwd-rows96`, its interval covering 1. The in-situ term reads 1.0216, 1.0219 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0085, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31.2 ms per call raw, 30.2 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.042/0.026/0.026

**Across the halves:** 8 of the 17 arms are faster on this half and 9 slower, at a geomean of 1.0523, from `lib-stage3-lean-onelevel` at 0.8649 to `list-aa-adjacent` at 1.3032, with `list` itself at 1.3023. **The baseline moved 30.23% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.7481 over 6 of 6 shapes at sign p 0.031, a margin of 25.19% against this class's 0.87% floor (`list-aa-adjacent`). `lib-stage3-lean-onelevel` leads outside the family here, where Run 39 named `lib-stage3-lean`, its basis cell at 0.8695 of Run 39's on 5.8% fewer instructions, and `mut-odo-vecdims` with both its A/A copies reads 3.2 to 3.4% faster on the basis against Run 39 with its counts level. Its two columns may NOT be differenced, `list` having moved 30.23 of a point, at a class geomean of 1.0523 over the 17 arms, with 7 of 9 strategies past an A/A bar of 0.49 points. The counted work reads a counts geomean of 1.1428 over the same arms, 17 of them counted. Its counted work parts by 14.28 points where its clock parts by 5.23, so about 0.37 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.10 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 130 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.01 | 130 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.07 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.02 | 130 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 130 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 130 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 130 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 130 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *130* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *122* | *0.00x* |
| lib-stage3-lean-onelevel | 0.020 | 0.023 | 0.10 | 112 | 1.00x |
| lib-stage2-lean | 0.020 | 0.023 | 0.12 | 112 | 1.00x |
| lib-stage2-lean-u1 | 0.020 | 0.025 | 0.09 | 111 | 1.00x |
| lib-stage3-lean | 0.020 | 0.024 | 0.09 | 112 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.024 | 0.07 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.024* | *0.10* | *111* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.024* | *0.12* | *111* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.10 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| lib-stage1 | 0.050 | 0.058 | 0.20 | 103 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.06* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.087 | 0.11 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.12* | *96* | *1.06x* |
| list (baseline) | 1.000 | 1.000 | 0.16 | 54 | 21.22x |
| *list-aa-adjacent* | *1.000* | *1.003* | *0.20* | *54* | *21.22x* |
| *list-aa-distant* | *1.001* | *1.004* | *0.16* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0076, worst cell 1.73% on `block-run64-off7`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.02% on `block-run64-gap64`, its interval missing 1. The in-situ term reads 1.0205, 1.0190 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0029, which the correction amplifies by 2.63x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m29s, peak 135 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.61 ms per call raw, 4.46 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.029/0.024/0.020

**Across the halves:** 6 of the 17 arms are faster on this half and 11 slower, at a geomean of 1.0519, from `lib-stage3-lean-onelevel` at 0.8762 to `list-aa-adjacent` at 1.3166, with `list` itself at 1.2962. **The baseline moved 29.62% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.020, priced against `mut-odo-vecdims` at 0.8655 over 5 of 5 shapes at sign p 0.062, a margin of 13.45% against this class's 0.76% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). `lib-stage3-lean-onelevel` leads outside the family here, where Run 39 named `lib-stage3-lean`, its basis cell at 0.8585 of Run 39's on 5.1% fewer instructions. Its two columns may NOT be differenced, `list` having moved 29.62 of a point, at a class geomean of 1.0519 over the 17 arms, with 5 of 9 strategies past an A/A bar of 1.57 points. The counted work reads a counts geomean of 1.1405 over the same arms, 17 of them counted. Its counted work parts by 14.05 points where its clock parts by 5.19, so about 0.37 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.22 | 227 | 1.67x |
| liblist-stage4-sum | -- | -- | 0.17 | 235 | 1.37x |
| liblist-stage5-sum | -- | -- | 0.08 | 241 | 1.20x |
| libunord-stage1-sum | -- | -- | 0.28 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.11 | 243 | 0.23x |
| libunord-stage14-sum | -- | -- | 0.10 | 243 | 0.23x |
| libunord-stage6-loop-sum | -- | -- | 0.14 | 239 | 0.69x |
| libunord-stage6-sum | -- | -- | 0.15 | 239 | 0.69x |
| libunord-stage7-sum | -- | -- | 0.15 | 239 | 0.69x |
| libunord-stage9-sum | -- | -- | 0.27 | 237 | 0.46x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.19* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.03* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.02* | *250* | *0.01x* |
| lib-stage3-lean-onelevel | 0.034 | 0.067 | 0.20 | 234 | 1.16x |
| lib-stage3-lean | 0.036 | 0.057 | 0.13 | 234 | 1.16x |
| lib-stage2-lean-u1 | 0.037 | 0.056 | 0.12 | 234 | 1.16x |
| lib-stage2-lean | 0.045 | 0.080 | 0.21 | 230 | 1.32x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.068* | *0.14* | *229* | *1.28x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.053 | 0.068 | 0.22 | 229 | 1.28x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.053* | *0.068* | *0.30* | *229* | *1.28x* |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.089* | *0.25* | *229* | *1.27x* |
| *mut-odo-vecdims-aa* | *0.061* | *0.089* | *0.26* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.061** | 0.088 | 0.27 | 229 | 1.27x |
| lib-stage1 | 0.084 | 0.111 | 0.18 | 221 | 2.35x |
| *bq-expand-aa-adjacent* | *0.137* | *0.200* | *0.10* | *217* | *1.44x* |
| bq-expand | 0.137 | 0.200 | 0.10 | 217 | 1.44x |
| *bq-expand-aa-distant* | *0.137* | *0.200* | *0.11* | *217* | *1.44x* |
| list (baseline) | 1.000 | 1.000 | 0.11 | 180 | 21.57x |
| *list-aa-distant* | *1.001* | *1.002* | *0.10* | *180* | *21.57x* |
| *list-aa-adjacent* | *1.002* | *1.002* | *0.18* | *180* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0030, worst cell 0.61% on `small-bcast32`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.03% on `small-row96`, its interval missing 1. The in-situ term reads 0.9741, 0.9896 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0019, which the correction amplifies by 1.60x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 141 MiB in use, 56 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.68 us per call raw, 6.46 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.078/0.051/0.060/0.088

**Across the halves:** 0 of the 17 arms are faster on this half and 17 slower, at a geomean of 1.1138, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0129 to `list-aa-distant` at 1.2948, with `list` itself at 1.2870. **The baseline moved 28.70% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean-onelevel` leads outside the family at 0.034, priced against `mut-odo-vecdims` at 0.5494 over 5 of 5 shapes at sign p 0.062, a margin of 45.06% against this class's 0.30% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). `lib-stage3-lean-onelevel` leads outside the family here as on Run 39, and with `compose` this is one of two classes where the flagged half runs every one of the seventeen arms faster; `lib-stage1` reads 0.9375 of its Run 39 cell on the control, its counts down 5.4%. Its two columns may NOT be differenced, `list` having moved 28.70 of a point, at a class geomean of 1.1138 over the 17 arms, with 9 of 9 strategies past an A/A bar of 1.02 points. The counted work reads a counts geomean of 1.1477 over the same arms, 17 of them counted. Its counted work parts by 14.77 points where its clock parts by 11.38, so about 0.77 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.33* | *86* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.30 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.29 | 98 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.29 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.29 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.28 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.22* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.016* | *0.24* | *98* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.014* | *0.016* | *0.31* | *98* | *1.00x* |
| lib-stage3-lean | 0.014 | 0.016 | 0.31 | 98 | 1.00x |
| lib-stage2-lean | 0.015 | 0.017 | 0.28 | 98 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.28 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.33 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.017 | 0.28 | 98 | 1.00x |
| lib-stage3-lean-onelevel | 0.016 | 0.024 | 0.30 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.24* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.23* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.18 | 94 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.102* | *0.38* | *79* | *1.35x* |
| bq-expand | 0.094 | 0.102 | 0.35 | 79 | 1.35x |
| *bq-expand-aa-distant* | *0.094* | *0.102* | *0.24* | *79* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 0.63 | 44 | 22.01x |
| *list-aa-distant* | *1.001* | *1.005* | *0.69* | *44* | *22.01x* |
| *list-aa-adjacent* | *1.002* | *1.007* | *0.58* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9938, worst cell 0.93% on `compose-zero-mid`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.03% on `compose-slice-bcast`, its interval covering 1. The in-situ term reads 1.0092, 1.0204 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9981, which the correction amplifies by 3.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m53s, peak 126 MiB in use, 33 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 31 ms per call raw, 30 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019

**Across the halves:** 0 of the 17 arms are faster on this half and 17 slower, at a geomean of 1.0825, from `lib-stage2-lean` at 1.0027 to `list-aa-adjacent` at 1.3359, with `list` itself at 1.3126. **The baseline moved 31.26% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage3-lean` leads outside the family at 0.014, priced against `mut-odo-vecdims` at 0.6217 over 4 of 4 shapes at sign p 0.12, a margin of 37.83% against this class's 0.62% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). `lib-stage3-lean` leads outside the family here by a thousandth, where Run 39's lead was a tie with the ceiling, and with `small` this is one of two classes where the flagged half runs every one of the seventeen arms faster. Its two columns may NOT be differenced, `list` having moved 31.26 of a point, at a class geomean of 1.0825 over the 17 arms, with 3 of 9 strategies past an A/A bar of 1.77 points. The counted work reads a counts geomean of 1.1590 over the same arms, 17 of them counted. Its counted work parts by 15.90 points where its clock parts by 8.25, so about 0.52 of the instruction saving reaches the clock.


## Provenance

**Run 40's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `bb6b12e`; one shim, `align-as.py` at `fe6d133`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`, which is Runs 36's to 39's compiler unmoved; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run40-gheadnospec` and is what every table here publishes; `run40-gheadtwopass` is the candidate. **What is new against Run 39 is not the pair but two things under both halves**: the source moved ten of the owner's commits, `c870e1e` to `bb6b12e`, and the box was rebooted, `uptime -s` putting it up since 2026-09-24 00:00:28, after Run 39's evening. The recipes, the shim, the project file, the compiler and the launch are Run 39's to the character.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 61 class views over ten classes for 1891 more, and it is Run 39's UNMOVED.** `./roster-delta.py run39-gheadnospec run40-gheadnospec`, read off the two binaries, puts no arm in or out: the 31 arms in the same order, the nineteen main-set shapes and the sixty-one class views over the same ten classes, although ten commits of `Main.hs` sit between the two builds. So pre-run step 12's condition did not fire and no -L1 roster pass was owed, and every cross-run figure in this file is read over the whole roster.

**The evening ran in ONE window and in the order the run list gives, and no process met foreign CPU.** `run-evening.sh` took the gate from 00:56:06 to 01:29:27, the alarm at 01:29:30 reading 0.0% busy, the sequence from 2026-09-25T01:29:30 to 2026-09-25T08:40:06 and the riders from 08:40:06 to 08:52:32, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back, the largest hole between one finishing and the next starting 0m, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones --- and each launched from `./run40-<half>`. The counted work, which wants no quiet machine, ran from 08:52, with the `-g3` twins building beside it. **The intrusion verdict is clean**: `--wild` finds no bench at or above 0.25 foreign in any of the twenty-two logs, so post-run step 3's rerun was not owed.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes agree: `list` reads 1.3063 and 1.3061, `bq-expand` 1.3097 and 1.3108, and `mut-odo-vecdims` 0.9999 and 1.0115 --- 0.02, 0.11 and 1.16 points apart --- with the two `sum-only` controls, on raw `slope`, within 0.08% of 1 on both passes. **What the passes part by is each half's own leg-to-leg movement and not a disagreement about the pair**: the control's `a` leg over its `b` reads `mut-odo-vecdims` at 1.0105 where the basis's two legs read 0.9988, so the control moved between its legs and the pair did not, the passes' ratio being the two halves' legs divided by construction (`./read-run.py --gate-draft run40` prints all four). The machine check, read against the fingerprint Run 39 installed --- this run's basis recipe on the source before the ten commits and the boot before the reboot --- puts `list`'s net at **+1.05%**, worst `cnn-L2-24x24-c32` at **+2.44%**, 0 of 19 shapes past 5% and the geomean inside the 3% bar; the main-set JSON reads the same check at +0.56% with `vgg-14-c512-k3` worst at +1.34%, which is the instrument and not a disagreement. So the reboot and the source together moved the box's `list` by under the bars.

**Every one of the twenty-two processes gated clean, the plateau refused by declaration, and SIX A/A worst cells sit past 5%.** `read-all.sh` gates each process on its own correction and passes all twenty-two. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.7295 to 21.3896 ms/iter across the run, a 27.86% spread against a 5% band, and it splits exactly by half, the basis's eleven processes flat within 1.42% at 21.0903 to 21.3896 and the control's within 1.14% at 16.7295 to 16.9209 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-runs` at **12.54%** on `runs-1024`, `gheadnospec-window` at **9.61%** on `window-32x32-c64-k3`, `gheadtwopass-bcast` at **7.62%** on `bcast-src64`, `gheadtwopass-window` at **6.22%**, `gheadtwopass-main` at **5.78%** on `stretch-r5-8x432` and `gheadnospec-runs` at **5.12%**; the main set's floor is 0.64% on both halves, so the main-set cell is one cell an order of magnitude outside a floor the population otherwise keeps. **One cell passes the about 10% [the floor section][floor] gates on**, `list-aa-adjacent` against `list` on `runs-1024` on the control, so that cell leaves the per-shape record and its row is flagged; no span reads the `runs` class.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run40-gheadnospec`, md5 `1d57f1411d4e31d331c3fe64d7272a28`, and `run40-gheadtwopass`, md5 `bed712c6eab6b6166d4e7d30451a33f2`, built back to back on 2026-09-24 against a clean tree. Their `.text` sections are **20174655** and **20248383** bytes, the first column of `size -A`; against Run 39's two the basis is SMALLER by 53248 bytes, thirteen pages exactly, and the flagged half by 57344, fourteen --- the ten commits, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 73728 bytes --- eighteen pages exactly, an eighth exact page multiple in that series --- and this time carries FEWER self-loops, 319 against 326, where Runs 38 and 39 carried more, so [the open list's entry on it](../README.md#what-is-open) gains a run on the side of its first four.

**The ten commits moved no tracked 28-byte copy off offset 0.** `./loop-offsets.py --delta run39-gheadnospec run40-gheadnospec`, the same basis recipe on the two sources, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0] and of the two-copy group at [0, 0], with no address surviving to the byte and every displacement a whole number of lines, four on the first group and two on the second. **Within the pair the two passes move them no more than on Run 39**: the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves and the two-copy group [0, 0] on both, and a group of three copies exists on the control half alone, at [0, 0, 0]. `--library` puts **4.3%** of the 806 library self-loops the two halves share at the same offset in line, which is Runs 36's to 39's 4.3% to the tenth: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 24 on each half, where Run 39 read 27 on the basis and 24 on the control, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 326 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 319 on the control, 231 and 131 of them at offset 0 where Run 39 read 237 and 143 of 338 and 344, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 0's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity nine bodies on the basis and eleven on the control** --- on both, `sumNoSpec`, `fillStage2Short` twice, `fillStage2`, the four leaf bodies of `fbMutOdoVecdimsAddInLeafU2`, `-Down` and `-Last` among them, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the control half `fillStage2OneLevel` and `fbFused` besides. Of the refusals, nine on the basis and seven on the control carry a `--loose` family of `fillStage2Short`, `fillStage2VSdims` and `fillStage2OneLevel` bodies, which the bytes cannot choose between, and six on each half are 60- to 63-byte bodies at offset 40 or 48 for which no twin holds a copy or a signature. **Three of the four twin readings hold FEWER loops than the binary they name for** --- against the basis's 326, its own twin holds 319 and the control's 311; against the control's 319, its own twin holds 311 and the basis's exactly 319 --- so `--match` refuses the population comparison there and each name rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run40-gheadnospec`, 9.992 times apart, which is plain -O1; on `run40-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. The scan builder's figures are Run 39's to the byte and the mutable one eight bytes under Run 39's 2408538, the source having moved. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.33 us** on `cnn-slice-c32`, **3.71 ms** on `cnn-L2-24x24-c32` and **39.8 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 20.7 to 21.6 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.5 us | 6.33 us | 5 us |
| `cnn-L2-24x24-c32` | 165888 | 3.81 ms | 3.71 ms | 2.91 ms |
| `stretch-wide-2xM` | 1800000 | 40.9 ms | 39.8 ms | 31.6 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.49 ms raw and 4.34 ms net; `bcast-inner900` 30.6 ms and 29.5 ms; `bcastmid-b200k` 49.2 ms and 48.1 ms; `window-128x128-k7` 14.2 ms and 13.8 ms; `scaled-rank1-m1` 5.34 ms and 5.16 ms; `runs-2` 41.1 ms and 40.1 ms; `flip-fwd-rows96` 31.2 ms and 30.2 ms; `block-r3-vol64` 4.61 ms and 4.46 ms; `small-row96` 6.68 us and 6.46 us; `compose-zero-mid` 31 ms and 30 ms. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and only three cells of the whole run are ones the reader flags, none of them a cell with a corrected time.** The two `sum-only` arms agree to within **0.02%** on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9998 on `small`'s control to 1.0002 on `runs`'s and `scaled`'s basis across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. **Three cells sit below R2 0.99 ([what that column detects][ramp]), all on `runs-3` and all unordered reducing consumers** --- `libunord-stage14-sum` at 0.9834 on the basis, `-stage9-sum` at 0.9714 and `-stage6-sum` at 0.9850 on the control --- of the run's 4960 cells, 2480 on each half, and none is under ten samples. The consumers carry no corrected time, so nothing in this run's time columns is set aside for how it resolved.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, 0 cells refused, at a cost of 1317s on the basis and 1075s on the control --- beside Run 39's 1373s and 1124s, on the same roster and with this run's `-g3` twins building and its first readings running alongside, which an instruction count does not see. The counts geomean over the seventeen arms that carry a corrected time runs **1.1405** on `block` to **1.1695** on `window`, the main set at **1.1603** --- the basis retiring 14.1 to 17.0 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families cleanly**: the `bq-expand` trio sits at 0.8669 to 0.8691, retiring 50.62 to 50.63% more instructions on the basis for 30.58 to 30.91% more time; the `list` trio at 1.0040 to 1.0114, cashing all of what it saves; and the eleven others between 0.9512 and 0.9752, retiring 3.83 to 5.70 percent more on the basis while their clocks run from 0.16 to 1.38 points above level. **Read per class the same way, the rate runs 0.37 to 0.78**: the instruction saving reaching the clock is lowest on `flip` and `block`, where the counted work parts by 14.28 and 14.05 points and the clock by 5.23 and 5.19, and highest on `window`, 16.95 against 13.18 --- Run 39's 0.43 to 0.76 and Run 38's 0.38 to 0.73, so [the open question][open] on that rate reads a similar range a third time.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0000** on both halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0388** and **1.1048** on the basis and **1.0277** and **1.0733** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three to four percent over the term it stands for on `mut-odo-vecdims` and about ten and seven on `bq-expand`. So the two passes do not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1128** on the basis and **1.1601** on the control, **4.7** points apart, where Run 39's two parted by 4.2, Run 38's by 4.3 and Run 37's by 5.2 --- so the two passes change what the spray costs a process as well as what the roster costs it, by within a point of what they changed it by on each of the three runs before. What the roster adds on top of that state is **1.0213** on the basis, 9 of 19 shapes above 1, and **1.0058** on the control, 8 of 19; the basis's rest runs 0.9747 on `stretch-bigstride` to 1.2245 on `stretch-r5-8x432`, the control's 0.9729 on `alexnet-L1-55-c3-k11` to 1.1059 on `stretch-inner256`. The whole in-process deflation is **1.1365** on the basis, 19 of 19 shapes above 1, and **1.1668** on the control, 17 of 19.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 39's, both recipes unchanged to the character and rebuilt on `Main.hs` at `bb6b12e` where Run 39 built from `c870e1e`, on the owner's word of 2026-09-24 that this run uses the previous run's recipes and benchmarks the changed source: both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, `align-as.py` at `fe6d133` under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run40-gheadnospec` and `run40-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 39's with the builddir names moved. So the pair's own `cross` figure is the two passes read a fifth time, in `--compare`'s orientation of the unflagged basis over the control, and the source is read as each half against Run 39's same half, `--half-movers run40 run39`. The ten commits move no arm in or out --- `./roster-delta.py run39-gheadnospec run40-gheadnospec` reads the 31 arms in the same order --- and touch no code behind `list`, `bq-expand`, any `mut-odo-vecdims` arm or `fillStage2Axes`, which is `lib-stage2-lean`'s fill; what they rewrite behind a timed arm is `fillStage2`, behind `lib-stage3-lean` and the fill branches of `lib-stage1` and of the reducing consumers, laid out as the library's `genericFillStrided` and then a nest folded over its outer levels (`c89fbe4`, `1514c1b`, `bb6b12e`), `fillStage2U1`, behind `lib-stage2-lean-u1`, now that nest's unrolled twin and dispatched as `lib-stage3-lean` is (`bb6b12e`), `fillStage2OneLevel`, behind `lib-stage3-lean-onelevel` (`3c02e36`), and `runSlices`'s odometer behind the reducing consumers (`e2f68a7`, `943fecd`); the rest is the list stages' wrappers, the check and diag plumbing and the class views' input builders, none of them in a timed arm's own code, with the views `roster-delta.py` reads unmoved. **Items (1) and (2)'s priors are instruction counts off this run's own basis binary**, `run40-gheadnospec`, taken with `probe-stalls.sh` at `N=50` over all nineteen main-set shapes for the three arms items (1) and (2) read, twice, into `probe-r40-prior1.txt` and `probe-r40-prior2.txt`, whose instruction counts agree to four decimals; `N=50` is the N of Run 39's own counts, `run39-counts-gheadnospec.txt`, so the two files are read against each other cell for cell. Against those, this binary retires `lib-stage2-lean`'s instructions within 0.04% on every one of the nineteen shapes, which is what makes that arm the denominator. The same files carry cycles, and at `N=50` those are not a prior: on the nine shapes outside the stretch set the two sweeps' ratios part by up to 104 points, `cnn-slice-c32`'s u1 over lean3 at 0.153 and 1.196, so they are quoted below only on the ten stretch shapes. No probe was taken on the control's recipe, so the priors are the basis's, carried to the control on Run 39's two halves agreeing to half a point on each pair below. **The limit this run cannot remove**: a rebuild moves every loop, and the chapter has put eight clauses that a reordering cannot reach a population to the test in time and seen all eight fail, so no item predicts an untouched arm's TIME across runs; the untouched arms stand in the items as within-half denominators instead.

(1) *The nest's instruction saving reaches the clock, and `lib-stage3-lean` moves further ahead of `lib-stage2-lean`.* In `probe-r40-prior1.txt`, lean3 over lean2 in instructions runs from 0.855 on `cnn-slice-c32` to 1.000 on the stretch shapes, a geomean of 0.975 over the nineteen, where `run39-counts-gheadnospec.txt` reads 0.940 to 1.000, a geomean of 0.993; lean3's own instructions fall to 0.910 to 1.000 of Run 39's, a geomean of 0.982. Run 39 read the pair in time at 0.9790 on the basis and 0.9783 on the control, `./read-run.py run39-gheadnospec-main.json --pair lib-stage3-lean lib-stage2-lean` and its control twin, so the band runs from none of the saving reaching the clock, that figure, to all of it, some 0.961. On the ten stretch shapes, where lean3 and lean2 retire equal instructions, the two sweeps read lean3 over lean2 in cycles at 0.899 to 1.096, parting by up to 11 points on one cell, `stretch-wide-2xM` at 1.009 and 0.899, which is placement and counter noise the nineteen-shape geomean averages down. `predict: pair lib-stage3-lean lib-stage2-lean 0.97 within 2% on main both`. A reading at or above 0.99 says the saving did not reach the clock or a placement term took it back; one below 0.95 says the nest bought more than its instructions, which the run's counts sweep then has to show.

**Read by --predictions, item (1):** `pair lib-stage3-lean lib-stage2-lean 0.97 within 2% on main both`: HELD on main basis, read 0.9656 over 19 shape(s), 0.44 point(s) off, within 2.00%; HELD on main control, read 0.9564 over 19 shape(s), 1.36 point(s) off, within 2.00%.

(2) *Rewritten as the nest's unrolled twin, `lib-stage2-lean-u1` gives back most of its gap to `lib-stage3-lean`.* In `probe-r40-prior1.txt`, u1 over lean3 in instructions runs from 0.956 on `stretch-tab7MB` and `stretch-wide-2xM` to 1.035 on `stretch-bigstride`, a geomean of 1.021 over the nineteen, where `run39-counts-gheadnospec.txt` reads 1.000 to 1.189, a geomean of 1.084. Run 39 read the pair in time at 1.1203 on the basis and 1.1249 on the control, `--pair lib-stage2-lean-u1 lib-stage3-lean` on the two main JSONs, a time excess 1.41 times the instruction excess in logarithms on the basis, which carried to this binary's 1.021 gives about 1.03. The two sweeps' cycles on the stretch shapes do not all follow the counts: u1 over lean3 reads 1.092 and 1.071 on `stretch-bigstride` and 1.117 and 1.088 on `stretch-primes`, each at about 1.03 in instructions, so the target sits above the carried figure. `predict: pair lib-stage2-lean-u1 lib-stage3-lean 1.05 within 4% on main both`. A reading at or above 1.09 says the twin keeps most of Run 39's gap, which was then not the instructions the rewrite removed; one below 1.01 says the unrolling is now free on the main set.

**Read by --predictions, item (2):** `pair lib-stage2-lean-u1 lib-stage3-lean 1.05 within 4% on main both`: HELD on main basis, read 1.0575 over 19 shape(s), 0.75 point(s) off, within 4.00%; HELD on main control, read 1.0617 over 19 shape(s), 1.17 point(s) off, within 4.00%.

(3) *The regime's worth on the two families no commit touched holds at the level of the earlier draws.* `list` and `bq-expand` run no code any of the ten commits changed, and their cross figures are the pair's variable on a fifth build: `--compare` of each run's basis main JSON over its control's reads `list` at 1.3360, 1.2960, 1.2889 and 1.2966 on Runs 36 to 39, the three later draws inside 0.77 points, and `bq-expand` at 1.2980, 1.3101, 1.3032 and 1.2985, all four inside 1.21. `predict: cross list 1.294 within 1% on main basis`, the three later draws' mean, and `predict: cross bq-expand 1.302 within 1% on main basis`, the four draws' mean. The reboot between Run 39 and this run is shared by the halves and so outside a cross figure; a reading outside either band on unchanged code says the regime's worth moved with the build and not with the source, which is the instance's term and makes items (1) and (2) harder to read.

**Read by --predictions, item (3):** `cross list 1.294 within 1% on main basis`: HELD on main basis, read 1.2983 over 19 shape(s), 0.43 point(s) off, within 1.00% --- `cross bq-expand 1.302 within 1% on main basis`: HELD on main basis, read 1.3058 over 19 shape(s), 0.38 point(s) off, within 1.00%.


**ALL THREE items hold their sentences whole, on every span on every half each names.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set on each half and by `--pair` with `--counts` for the instructions.

(1) *The nest's instruction saving reaches the clock, and `lib-stage3-lean` moves further ahead of `lib-stage2-lean`.* **HELD on both halves.** The pair reads **0.9656** on the basis and **0.9564** on the control, against the band the item drew from none of the saving reaching the clock, Run 39's 0.9790 on the basis and 0.9783 on the control, to all of it at about 0.961: the basis inside it and the control just past its far end; neither reading reaches the 0.99 that would say the saving did not reach the clock, nor crosses the 0.95 that would say the nest bought more than its instructions. The saving the prior predicted is the one that happened: this run's own sweep puts the pair at **0.9751** of the instructions raw on the basis, the prior's 0.975, and 0.9601 net of the forcing pass, so about 86% of the corrected instruction saving reaches the clock on the basis and all of it, 108%, on the control.

(2) *Rewritten as the nest's unrolled twin, `lib-stage2-lean-u1` gives back most of its gap to `lib-stage3-lean`.* **HELD on both halves.** The pair reads **1.0575** on the basis and **1.0617** on the control, inside 4% of the 1.05 target and clear of both ends the item named --- under the 1.09 that would say the twin kept Run 39's gap, 1.1203 and 1.1249, and over the 1.01 that would say the unrolling is free. The instructions again came out as predicted, **1.0206** raw on the basis against the prior's 1.021; net of the forcing pass the excess is 4.73%, and the time excess runs past it on both halves, at 1.22 and 1.30 of it, which is the stretch shapes' cycles the item named as sitting above the carried figure. Against Run 39's own basis the arm reads **0.9300**, the one fill outside the 3.3% drift band, its gain on the two smallest shapes.

(3) *The regime's worth on the two families no commit touched holds at the level of the earlier draws.* **HELD.** `list` reads **1.2983**, 0.43 of a point off 1.294, and `bq-expand` **1.3058**, 0.38 off 1.302, both inside 1%; the fifth draw of the pair lands among the four before it on both families, so the regime's worth did not move with the build, and nothing here complicates the reading of items (1) and (2).