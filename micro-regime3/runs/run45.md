# Run 45 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach. The words it uses and the bars it reads against --- a point, the sign of a ratio, a strategy, a family, the plateau, and which bar answers what --- are defined once in [README's *Reading a run file*](../README.md#reading-a-run-file).

**Run 45 (GHC HEAD's in-tree stage1 against itself, as patched on 2026-10-03 under its unchanged version `10.1.20260918`, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source, launched from disk): the two passes are worth some thirty points on `list` and on `bq-expand`, and the count-down level loop took back the three points the bounded one cost `lib-stage2-lean`.** The pair is Runs 36's to 44's IN ITS VARIABLE --- one source, `Main.hs` at `f5bf411`, one shim at `1a359bd` under five switches with the exit span and the settled cost, ONE compiler, the patched stage1, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the eighteen main-set arms that carry a cross-half figure, SEVEN move with the families and ELEVEN do not: the seven are the `list` and `bq-expand` families entire and `lib-stage0`, which builds regime 3 as `list` does, at **1.2928** to **1.3092**, and the eleven others span **0.9938** to **1.0020**. **The bar an arm has to clear to be the passes' rather than the run's is 0.69 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.85% on the basis and 0.72% on the control and measured WITHIN one half --- and three of the ten arms that are not A/A copies clear it, the three that move with the families. That bar is the control's wild cell on `vgg-14-c512-k3`: without that shape it is 0.37 points, and four fills clear it on the basis's side as well, at 0.9948 to 0.9958.

**What this run was built to settle is what the source's two commits did to the fills they reached and whether the regime's worth held, and eight of its ten spans hold while item (2)'s is KILLED and item (3)'s is KILLED on one reading of four: master's `lib-stage0` runs 35 times `lib-stage1` where the four prior cycle sweeps put it 26.4 to 29.2.** `lib-stage3-lean` over `lib-stage2-lean` reads **1.0053** on `stretch-wide-2xM` and **1.0013** over the main set on the basis, the count-down loop having taken back Run 44's loss on 0.81% more instructions; `lib-stage2-disp` reads with `lib-stage2-lean` at **1.0021** and **1.0017** on the main set and **0.9992** on `small`'s control, and at **0.9873** on `small`'s basis on level instructions, a placement; `libunord-stage13-sum` retires at least 115 instructions a call fewer than stage fifteen on every view the countdiff reads and runs at **0.9879** of its time on the main set; and the control's counted work on `list` and `bq-expand` is Run 44's to the fourth decimal, the regime's worth reading `list` at **1.2929** and `bq-expand` at **1.3048**, `list` inside the spread its builds from Run 37's on drew and `bq-expand` inside every draw from Run 36's but Run 41's ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)). Item (2)'s time reads **35.0472** against cycles of 26.4 to 29.2 in four sweeps whose files record no launch environment; the one sweep taken under the preamble read nothing, and [the open list][open] carries what would settle it.

**Foreign CPU met two A/A benches of one shape on the basis's main set and the owner declined the rerun, and the quiet box the owner granted after the run placed both half-local movers the copy test took.** On `cnn-slice-c32` `bq-expand-aa-distant` and `list-aa-adjacent` met 1.79 and 0.42 of a core foreign, which sets the basis's main-set floor at 0.85%, 0.53% without the shape, and moves no verdict; the control's floor, 0.72%, is a wild cell, `mut-odo-vecdims` itself running 4.3 to 4.5% over its copies on `vgg-14-c512-k3`, at 13.81% the one A/A cell past 10% ([Provenance](#provenance)). Four arm-populations move past 3% on the basis against Run 44's same half: the copy test reads `lib-stage2-lean-u1` on `bcastmid` INSTANCE and the `mut-odo-vecdims` family on `small` BUILD, Run 44's build reverting ([Results](#results)). And under the two passes `libunord-stage13-sum`, newly on a top-level merge loop, allocates 18% MORE than on the basis, where Run 44 read its halves level ([the properties](#the-properties-the-next-run-should-test)). The machine check read `list` inside the bars, and no reboot sits between this run and Run 44.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE alone**: `Main.hs` moved from `c100112` to `f5bf411` in two of the owner's commits, which took two unordered consumers out, brought `lib-stage0` in and `lib-stage2-disp` back, counted `fillStage2Axes`'s level loop down and sorted `routeUnord13`'s axes by insertion ([Provenance](#provenance)); the compiler, the project file `cabal.project.ghead`, the shim `align-as.py` at `1a359bd` with its five switches, the regime and the launch from disk are Run 44's. **Read against the half Run 44 built by this same recipe, the three arms whose instructions the two commits moved all moved FASTER on both halves**: `lib-stage2-lean` reads 3.11 points faster on the basis and 2.31 on the control, which gives back the 2.81 and 2.49 Run 44 read it lose, and the reducing consumers `liblist-stage4-sum` 1.35 and 1.03 and `libunord-stage13-sum` 1.22 and 1.23, raw --- the first two on 0.81 and 1.00% MORE instructions than Run 44's on the basis and the third on 1.40% fewer, every other arm's counts level to 1e-4. Every other arm with a corrected time moved by at most 0.86 points on the basis and 0.73 on the control, the range [What the next run compares against](#what-the-next-run-compares-against) quotes. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run45-gheadnospec`, as every published table here is from Run 13 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **TWO of the thirty-one rows have no twin in Run 44's file**: `lib-stage0`, master's `toVectorT`, is a first reading, and `lib-stage2-disp`, last timed on Run 26, returns as different code under its old name, rebuilt over `lib-stage2-lean` with its cut at 32768; the other twenty-nine are Run 44's, in Run 44's order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries.

**Comparing runs?** The table below is Run 45's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.85%** from 1 on the basis half or **0.72%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **Each half's floor is one disturbed cell's**: the basis's pair, `bq-expand-aa-distant`, is one of the two benches foreign CPU met on `cnn-slice-c32`, and read without that shape the basis's floor is **0.53%**, the same pair carrying it; the control's, `mut-odo-vecdims-aa-distant` against `mut-odo-vecdims`, carries that half's wild cell on `vgg-14-c512-k3` ([Provenance](#provenance) reads both). **The whole-set figure and the carry-back one agree on both halves**: over the four pairs that carry back to Run 10 the two halves read **0.85%** and **0.72%**, each carried by its half's whole-set pair. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **6.61%** on `cnn-slice-c32` on the basis and **13.81%** on `vgg-14-c512-k3` on the control, those two cells --- are not floors at all and are not to be quoted as any. This run's two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.51 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.53 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage15-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage fourteen's route with the zero-stride axis consed just outside the run |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.37* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.023 | 0.114 | 0.46 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.023 | 0.114 | 0.51 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-disp | 0.024 | 0.114 | 0.45 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch with a canonical run of 32768 or more routed to slices, against `lib-stage2-lean` |
| lib-stage2-lean-u1 | 0.025 | 0.113 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| lib-stage1 | 0.025 | 0.114 | 0.36 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.114 | 0.46 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` was a port of until 2026-09-11 |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.114* | *0.63* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.113* | *0.58* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.45* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.38* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.113 | 0.35 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *bq-expand-aa-adjacent* | *0.128* | *0.259* | *0.67* | *50* | *2.78x* | *A/A control* |
| bq-expand | 0.128 | 0.258 | 0.63 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.130* | *0.258* | *0.37* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.88 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.010* | *0.72* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.004* | *1.051* | *0.61* | *21* | *25.20x* | *A/A control* |
| lib-stage0 | 1.004 | 1.032 | 0.78 | 21 | 25.21x | nothing (pure) -- stage zero, master's `toVectorT`, building regime 3 from the element list: what the two stages replace |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run SEVEN of the 136 pairs among the timed arms other than `list` part in SIGN between the two statistics on the basis and SEVEN on the control, `--winsor` printing each. **The cap moves nine rows on the basis**, `lib-stage1` with 4 of 19 cells capped, `lib-stage2-disp` with 2 of 19 cells capped, `lib-stage2-lean` with 2 of 19 cells capped, `lib-stage2-lean-u1` with 4 of 19 cells capped, `lib-stage3-lean` with 2 of 19 cells capped, `list-aa-adjacent` with 1 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2` with 4 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2-aa` with 4 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2-aa-distant` with 3 of 19 cells capped, their published figures sitting 0.2 to 13.0 points under their plain per-shape geomeans, while `lib-stage0` and `list-aa-distant`, with 2 and 1 of 19 cells capped, sit 0.05 and 0.001 of a point over theirs, so rows 0.001 apart in print are ordered by the cap and not by the arms. **The widest disagreement of any kind on the basis** is `lib-stage0` over `lib-stage1`, which divides to **40.2862** on the column where the paired figure is **35.0472**, the column +14.9% off it. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads 14 of the 16 rows moved against Run 44's table, where what says how far an ARM moved is `--compare` against the JSON of the half Run 44 built.

**This run's two columns may be differenced on NONE of the eleven populations, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here `list` moves by **29.29 points** on the main set and by 24.40 on `bcastmid` to 36.92 on `bcast` over the ten classes, every one of the figures past the bar by a factor of 34 or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's.

`concat-runs` has no row, and neither do the other 83 arms the roster holds and checks without timing --- **84 of its 115** in all: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). `roster-delta.py`, read off the two binaries, reads 31 arms to 31 over 19 shapes to 19 and the class views 62 to 62, in: lib-stage0, lib-stage2-disp, out: libunord-stage7-sum, libunord-stage9-sum; `b5cd52e` moved all four, the twenty-nine survivors keeping Run 44's order and every geometry unmoved. A movement against Run 44's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a source term between the two runs and no compiler, shim, boot or launch term, nor a project-file term --- and a movement across THIS run's two halves is the pair's own variable, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is the two lean fills, `lib-stage3-lean` and `lib-stage2-lean`, level at 0.023**, with `lib-stage2-disp` at 0.024, `lib-stage2-lean-u1` and `lib-stage1` at 0.025 and the shipped leaf at 0.026 --- **six timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result. **Paired on the basis, the two lean fills are level again where Run 44 had `lib-stage3-lean` three points ahead**: `lib-stage3-lean` over `lib-stage2-lean` is **1.0013** at 9 of 19 and sign p 1, and **1.0053** on `stretch-wide-2xM`, where Run 44 read 0.845, which is registration item (1) HELD, the count-down level loop having given `lib-stage2-lean` back what Run 44's bounded loop cost it; and both lead the shipped leaf and `lib-stage1` by eleven to twelve points, `lib-stage3-lean` at **0.8859** and **0.8844**, `lib-stage2-lean` at 0.8847 and 0.8833, as on Run 43. **The second is master's route, `lib-stage0`, in the table for the first time: it reads with `list` and not with the fills**, at **1.0035** of `list` on the basis and 0.9915 on the control, paired, and at **35.0472** times `lib-stage1` on the basis --- registration item (2) KILLED, the band having been drawn from four cycle sweeps that put `lib-stage0` at 26.4 to 29.2 times `lib-stage1`. Its regime 3 builds a vector from the element list as `list` does, so the passes move it with `list`, at **1.3085** across the halves against `list`'s 1.2929. **The third, read across the halves, is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6362** on the basis and **0.6336** on the control, 0.26 of a point apart on a pair that moves `list` by twenty-nine points, the control's 0.22 of a point under the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 --- a span carried from that file and not re-derived here.

**The two commits moved instructions in three of the ten arms both runs time whose code they reached, and the clock moved the RIGHT way on all three, two of them on MORE instructions.** Against Run 44's basis, the same recipe on `c100112`, every timed arm both runs carry but those three reads 0.9999 to 1.0001 of Run 44's instructions an iteration on both halves, and `lib-stage2-lean`, `liblist-stage4-sum` and `libunord-stage13-sum` read **1.0081**, **1.0100** and **0.9860** on the basis and 1.0085, 1.0107 and 0.9838 on the control --- the first two most on `stretch-wide-2xM`, 2.27 and 2.78% over Run 44's on the basis. The clock moves by at most 0.86 points on every other arm with a corrected time, from **0.9914** on `lib-stage2-lean-u1` to **1.0030** on `bq-expand-aa-distant` on the basis and from **0.9928** on `lib-stage3-lean` to **1.0073** on `mut-odo-vecdims` on the control; `lib-stage2-lean` reads **0.9689** and **0.9769**, and the consumers `liblist-stage4-sum` **0.9865** and **0.9897** and `libunord-stage13-sum` **0.9878** and **0.9877**, raw. **So the count-down level loop runs faster on more instructions, the reverse of Run 44's bounded loop**, which ran slower on fewer: the loop's form is what moved the clock, as [the open list][open]'s entry on Run 44's loss answered, and this run is the other half of that reading.

**The half-local movers against Run 44 are four arm-populations, all on the basis, and the copy test places both of the cells it took.** `--half-movers run45 run44` flags `lib-stage2-lean-u1` on `bcastmid` 3.6% FASTER, widest on `bcastmid-block150k` at 0.879, and the `mut-odo-vecdims` family on `small` 3.0 to 3.3% faster, the arm and both its A/A copies, widest on `small-row96` at 0.953 --- every one on counts level to 1e-4, and none on the main set. **The copy test, taken on the owner's quiet box before the counts had landed** (`probe-copy-test-run45.log`), reads the `bcastmid` cell INSTANCE, a fresh copy of the basis at 0.911 of the timed file and Run 44's basis at 0.983, the copy's passes spread by 1.067; and the `small` cell, `small-row96/mut-odo-vecdims-aa-distant`, BUILD, the copy reading with the timed file at 0.996 and Run 44's basis apart from both at 1.032 --- so the family's move on `small` is Run 44's build reverting, the term Run 44's own copy test placed as that build's when it read `mut-odo-vecdims` 3.6% slower there, its copies 2.7 and 2.9%. **Step 4b's cells read as Run 44's did**: ranked by time over counts, all twenty of the widest cells of the 2511 are `bq-expand-nosum`, whose counts the two passes move by 37 to 44% on cells where its clock moves by at most 6.5 points; the count-led cells are led by `bq-expand-nosum`'s and the `bq-expand` family's, whose counts the passes move by up to 132% and 108%.


## What the next run compares against

**Run 45's pair is Run 44's rebuilt on the changed source, [registered before it ran](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of 2026-10-04, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; [the standing rulings from past runs](../README.md#standing-rulings-from-past-runs) are NOT that site either.** What this run leaves as the reference is `run45-gheadnospec`, the unflagged half whose column stands below: the in-tree stage1 reporting `10.1.20260918` as patched on 2026-10-03, through `cabal.project.ghead`, `Main.hs` at `f5bf411`, the shim at `1a359bd` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **Its step from `run44-gheadnospec`**: 15 of the 16 arms both runs carry with a corrected time read within 0.86 points of 1 by `--compare`, paired per shape, and one does not --- `lib-stage2-lean` at **0.9689**, 0.854..1.008, widest on `stretch-wide-2xM` at 0.854, below 1 meaning this run is the faster; `--bridge` puts no arm outside the 3.3% drift band it prints. **The step is the source alone**, the compiler, the shim and the recipes being Run 44's, and the counts say where it reached ([Results](#results)). **The pair itself is Runs 36's to 44's, built again**, and its draws are `./read-run.py --record regime`'s, a row per reading. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER was not this pair's variable --- both halves are one in-tree stage1 --- and it has not moved since Run 44, so the step from Run 44 carries the source alone.** **What this run adds is another build of the pair, the second on the stage1 patched on 2026-10-03**: Runs 36 to 45 are the same two recipes, Runs 39's to 45's with the settled cost on both, and their cross-half readings on `list` ran 1.2889 to 1.3040 over the eight builds after Run 36's, where this run reads **1.2929**, inside them and 1.11 points under Run 44's draw on the same compiler; `bq-expand` reads **1.3048**, inside the 1.2980 to 1.3212 every build but Run 41's 1.3620 kept. The control's counted work on both families is Run 44's to the fourth decimal, so the source did not reach what the two passes compile, and `list`'s move from Run 44's draw is this build's or this process's. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim, the source and the compiler together. Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s build rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and on the eighteen shapes left without Run 36's wild cell, where Run 36 read above the level, the eight HEAD builds' draws from Run 37's to Run 44's straddle Run 31's 1.2974, and this run's `list` reads 1.2926 over those eighteen shapes, below it.

**What Run 45 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 44 and this run, and the gate says the box still measures as it did, the machine check reading `list`'s net inside the bars against the fingerprint Run 44 installed ([Provenance](#provenance) gives the figures). **This reading carries a source term alone**: Run 44's basis is this basis's recipe on `c100112`, and `list` runs no code the two commits changed and retires the instructions it did on Run 44, so `list` holding inside the bars says the rebuild left it there. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 45's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **Eight of the ten spans held on every population and half their scope names, item (2)'s was KILLED and item (3)'s KILLED on one of its four readings**, the priors behind the items being instruction counts, cycles and bytes off this run's own basis binary, taken before preflight on a quiet box. **What a next registration should take from this one is that a cycle prior taken outside the preamble does not bound a `list`-shaped arm's time**: item (2) drew its band from four sweeps that put `lib-stage0` 26.4 to 29.2 times `lib-stage1` in cycles and whose files record no launch environment, and time read 35.05 under the preamble every timed process carries, the one sweep taken under it reading nothing.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 45**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918` as patched on 2026-10-03, on `Main.hs` at `f5bf411` with the shim at `1a359bd`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 44 published a HEAD half on this basis's recipe, so the two published columns carry no shim or compiler term, only the source. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9689** on `lib-stage2-lean` to **1.0030** on `bq-expand-aa-distant`, below 1 meaning this run is the faster, as the first paragraph of this section breaks down. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 45 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918 patched) | Run 45 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.033 |
| `lib-stage1` | **0.025** | 0.032 |
| `lib-stage2-lean` | **0.023** | 0.030 |
| `lib-stage2-lean-u1` | **0.025** | 0.033 |
| `lib-stage3-lean` | **0.023** | 0.030 |
| `bq-expand` | **0.128** | 0.127 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on six of the seven rows, the control higher on each of those six, while `bq-expand` prints 0.128 and 0.127, the one arm whose own move outpaces the denominator's. In absolute terms the flagged half is the faster on the `list` and `bq-expand` families, on `lib-stage0` and on three A/A copies of the fills by at most 0.20 of a point, ten of the eighteen arms with a corrected time, and the basis on the other eight, `--compare` putting them at 0.9938 on `mut-odo-vecdims` to 0.9994 on its copy `mut-odo-vecdims-aa` --- where on Run 44 the flagged half was the faster on fourteen of sixteen. **Three of the ten arms that are not A/A copies clear the 0.69-point bar that comparison prints**: `list` and `bq-expand`, the two families the passes reach, and `lib-stage0` at **1.3085**, whose regime 3 builds from the element list as `list` does; on Run 44 four of eight cleared a 0.40-point bar. This run's bar is `mut-odo-vecdims` against its copy `mut-odo-vecdims-aa-distant`, and the control's wild cell on `vgg-14-c512-k3` sets it ([Provenance](#provenance)): read without that shape the bar is 0.37 points, `list-aa-adjacent` against `list`, and seven arms clear it, the three above and four fills on the basis's side, `lib-stage2-lean-u1`, `lib-stage1`, `lib-stage2-disp` and `lib-stage2-lean` at 0.9948 to 0.9958. **Read DOWN a column and the head is `lib-stage3-lean` and `lib-stage2-lean`**, level at 0.023 on the basis and 0.030 on the control, `lib-stage3-lean` first on the basis's unrounded column and `lib-stage2-lean` on the control's; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, every published table but the two-column one being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over the main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6336** (0.6362); `lib-stage1` against `mut-odo-vecdims-add-in-leaf-u2` **1.0041** (1.0017); `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2` **0.8870** (0.8847); `lib-stage2-lean` against `lib-stage1` **0.8834** (0.8833); `lib-stage3-lean` against `lib-stage2-lean` **1.0000** (1.0013); `lib-stage2-lean-u1` against `lib-stage3-lean` **1.0702** (1.0683); `bq-expand` against `mut-odo-vecdims` **2.1783** (2.8599). **Six of the seven hold their direction across the halves** by the paired figure, and the seventh is a tie: `lib-stage3-lean` against `lib-stage2-lean` reads 1.0000 on the control and 1.0013 on the basis at 9 of 19 and sign p 1, the two lean fills level on both halves where Run 44 put `lib-stage3-lean` three points ahead on the basis. The headline pair, `bq-expand` against `mut-odo-vecdims`, moves by 68.2 points between the halves, the pair's own variable, and the other six by at most 0.26 of a point. **`lib-stage2-lean` leads the shipped leaf by about eleven and a half points and `lib-stage1` by about twelve, on both halves**, where Run 44 read about nine against each. Three readings of the fourteen part in sign from the published columns, which the cap orders: `lib-stage1` against the leaf on both halves, its columns dividing to 0.9482 and 0.9759, and `lib-stage3-lean` against `lib-stage2-lean` on the basis, to 0.9959; a margin is judged on the paired figure.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.39 us | 0.077 | `lib-stage2-disp` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.55 us | 0.090 | `lib-stage3-lean` 0.039 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 118 us | 0.064 | `lib-stage2-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 386 us | 0.044 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 460 us | 0.048 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.09 ms | 0.031 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.69 ms | 0.052 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.51 ms | 0.024 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.9 ms | 0.040 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.9 ms | 0.053 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.6 ms | 0.031 | `lib-stage2-disp` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.4 ms | 0.023 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.1 ms | 0.113 | `lib-stage2-lean-u1` 0.113 | `mut-odo-vecdims` 0.113 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.5 ms | 0.022 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.7 ms | 0.088 | `lib-stage2-lean` 0.073 | `mut-odo-vecdims-add-in-leaf-u2` 0.077 |
| `stretch-bigstride` | 3 | 1800000 | 51.5 ms | 0.032 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 40.5 ms | 0.057 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 40.6 ms | 0.021 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 40.3 ms | 0.056 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 920 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 28.7 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 28.7 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 34.8 ms | 0.016 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 40.5 ms | 0.056 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.64 ms | 0.053 | `lib-stage2-disp` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.2 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 48.1 ms | 0.034 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 41.3 ms | 0.022 | `lib-stage1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.19 ms | 0.020 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.23 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.23 ms | 0.024 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-page` | `block` | 64 | 131072 | 2.3 ms | 0.029 | `lib-stage2-disp` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.41 ms | 0.020 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 925 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 925 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-bcast-nest` | `compose` | 6 | 1800000 | 33.3 ms | 0.036 | `lib-stage3-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-bcast-wide` | `compose` | 120 | 1800000 | 47.5 ms | 0.012 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.010 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.5 ms | 0.019 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.3 ms | 0.026 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.27 ms | 0.026 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.053 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.2 ms | 0.024 | `lib-stage2-disp` 0.023 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 29.8 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 31.9 ms | 0.049 | `lib-stage2-lean` 0.042 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 118 us | 0.065 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 463 us | 0.047 | `lib-stage2-disp` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.46 ms | 0.025 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `runs-65536` | `runs` | 65536 | 1769472 | 27.7 ms | 0.024 | `lib-stage2-disp` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 27.9 ms | 0.024 | `lib-stage0` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.2 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.6 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 28.5 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 28.5 ms | 0.025 | `lib-stage2-disp` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 32.5 ms | 0.033 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-2` | `runs` | 2 | 1800000 | 40.6 ms | 0.057 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 29.8 ms | 0.026 | `lib-stage2-disp` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.6 ms | 0.040 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.2 ms | 0.025 | `lib-stage2-disp` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.4 ms | 0.038 | `lib-stage2-disp` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29 ms | 0.025 | `lib-stage2-disp` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 31.8 ms | 0.030 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 28.8 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.2 ms | 0.026 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 264 us | 0.030 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.02 ms | 0.023 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.13 ms | 0.029 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.029 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.077 | `lib-stage3-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.36 us | 0.050 | `lib-stage3-lean` 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `small-flat64` | `small` | 64 | 256 | 4.4 us | 0.058 | `lib-stage2-disp` 0.006 | `mut-odo-vecdims-add-in-leaf-u2` 0.056 |
| `small-patch-r5` | `small` | 4 | 256 | 5.33 us | 0.088 | `lib-stage2-lean-u1` 0.048 | `mut-odo-vecdims-add-in-leaf-u2` 0.066 |
| `small-row96` | `small` | 96 | 384 | 6.37 us | 0.042 | `lib-stage3-lean` 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 280 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 960 us | 0.084 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.44 ms | 0.052 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.64 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.9 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.7 ms | 0.053 | `lib-stage2-disp` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage1` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.6 ms | 0.032 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 44 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the NINE `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them THIRTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside vecdims` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names four different `lib-` arms --- `lib-stage3-lean` on FIVE rows, `lib-stage2-lean` and `lib-stage2-disp` on two each and `lib-stage1` on one, where Run 44 gave `lib-stage2-lean` and `lib-stage3-lean` four rows each, six of its rows now naming another arm. The cross-class summary's `best outside vecdims` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 45's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in every population it reads, as on Runs 36 to 44 and at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9950**, where the control reads **0.9805** on `stretch-pow2stride`. Every other shape of every population reads the clause with room, the classes' closest cells at 0.30 to 0.48 on the basis. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw by 0.50 of a point, INSIDE its 0.85% floor and inside the 0.53% that floor reads without the intruded shape, where the six draws on disk, Runs 40 to 45, run 0.9898 to 0.9991 on the basis and 0.9798 to 0.9856 on the control. The `worst` clause holds in every regime, roster, compiler and layout the README has run, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, the WIDER statement this class set is read for --- that no arm the library would ship is slower than `list` on any shape: **58 timed non-control cells of 1458 are slower than their own shape's `list`, and 56 of them are `lib-stage0`**, master's `toVectorT`, which the fix replaces rather than ships: its regime 3 builds the vector from the element list as `list` does, so it reads with `list` on every population whose views are regime 3, 1.004 on the main set and 0.989 to 1.023 on eight classes, and far below it only on `runs` and `block`, at 0.085 and 0.050, where its regime 2 serves slices. It reads above `list` on those 56 cells by at most 6.82% outside `runs-2` (`small-bcast32` on the control) and at **1.3486** and **1.0577** on `runs-2` on the control and the basis. **The other two are the cells Runs 41 to 44 read**, `lib-stage1` on `runs-2`, the stage-one route as it shipped, whose fill since `c7549d2` is `fillStage3` behind a `walkAx` conversion and so no longer the library's own: on the control at **1.4625** and on the basis at **1.0726**. **It is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 0.9445 between the halves while `list` moves 1.2879, so the control's cell reads 1.4625 against the basis's 1.0726 because `list` moved by twenty-nine points and the fill, if anything, the other way.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits at or under 0.05268. The `bq-expand` clause is closest at `small-row96` at 1.00441 on the control, then `scaled-rank1-m1` at 1.00003 on both halves, then `stretch-tall-Mx2` at 1.00000 on the basis. **Those figures are Runs 36's to 44's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, no commit having rewritten code behind `bq-expand` or `list`. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in the ten classes, on both halves --- and their LEVEL clause BREAKS in ten of the ten classes.** `bq-expand` sits between 1.00x and 3.86x the result vector and `list` at 19.00x to 27.66x, on both halves and in every class. On the main set `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the main-set shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, `lib-stage0` reading 0.9343 beside them, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 44's to the fourth decimal.

**AND ONE OTHER ARM MOVES AGAIN, THE OTHER WAY AND FURTHER: `libunord-stage13-sum`, which `f5bf411` put on a top-level merge loop.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **1.1845** of the basis on `libunord-stage13-sum`, from 1.111 on `stretch-wide-2xM` to 1.254 on `stretch-coprime-r7`, where Run 44 read 0.9991 and Runs 42 and 43 0.9687 and 0.9686 --- so the two passes now make the sorted route allocate MORE, and [the open list][open] carries it. Every other arm outside the `bq-expand` and `list` families and `lib-stage0`, which allocates as `list` does, reads 0.9992 to 1.0009, `libunord-stage14-sum` the highest, and the fills and ordered consumers 1.0000 to 1.0002. `--alloc` puts 358 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 45 (GHC HEAD's in-tree stage1 against itself, as patched on 2026-10-03 under its unchanged version `10.1.20260918`, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 24.40 points on `bcastmid` at narrowest and 36.92 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 44, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **180 arm-comparisons, 67 putting the basis faster and 113 slower**, with no degenerate arm excluded, at geomeans from **1.0567** on `block` to **1.1355** on `window` and extremes of `lib-stage1` at **0.9786** on `small` and `bq-expand-aa-distant` at **1.5332** on `window`. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **Two registrations name a class**: item (3)'s pair span is `on main,small` and item (4)'s countdiff span `on main,compose,bcast,bcastmid`, both read in [this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), every other span being `on main`.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **The bold is the arm outside the vecdims arms on TEN of the TEN rows this run** --- `lib-stage3-lean` on `bcast`, `compose`, `flip`, `small`, `window`, `lib-stage2-lean` on `bcastmid`, `block`, `lib-stage2-disp` on `rev`, `runs`, `lib-stage1` on `scaled`. **The vecdims arms' ceiling is `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Runs 39 to 44, and no row's bold sits in the CEILING column, where Run 44's `rev` had it: `lib-stage2-disp`, timed again, takes `rev` and `runs`, the two rows Run 44 gave the ceiling and `lib-stage2-lean-u1`.

| class | shapes | mut-odo-vecdims | worst | best outside vecdims | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.065 | **`lib-stage2-disp`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.33% |
| `bcast` | 6 | 0.022 | 0.056 | **`lib-stage3-lean`** 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.99% |
| `bcastmid` | 4 | 0.030 | 0.053 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.28% |
| `window` | 8 | 0.051 | 0.084 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.24% |
| `scaled` | 3 | 0.029 | 0.030 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 1.04% |
| `runs` | 16 | 0.026 | 0.057 | **`lib-stage2-disp`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 | 3.30% |
| `flip` | 6 | 0.029 | 0.053 | **`lib-stage3-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 1.58% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage2-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.28% |
| `small` | 5 | 0.061 | 0.088 | **`lib-stage3-lean`** 0.033 | `mut-odo-vecdims-add-in-leaf-u2` 0.052 | 0.36% |
| `compose` | 6 | 0.023 | 0.036 | **`lib-stage3-lean`** 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 | 0.43% |

The best arm outside the vecdims arms is ahead of `mut-odo-vecdims` in ten of the ten classes. Six row(s) change the arm they name against Run 44, `bcastmid` to `lib-stage2-lean`, `compose` to `lib-stage3-lean`, `flip` to `lib-stage3-lean`, `rev` to `lib-stage2-disp`, `runs` to `lib-stage2-disp`, `small` to `lib-stage3-lean`. **THREE rows tie at three decimals this run**, `bcast`, `compose`, `rev`, and `scaled` sit a thousandth apart; the `bold` column decides each on the unrounded values.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.16 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.13 | 148 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.13 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.01 | 158 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 157 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 157 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.01 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.05* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage2-disp | 0.021 | 0.025 | 0.12 | 148 | 1.00x |
| lib-stage3-lean | 0.021 | 0.026 | 0.15 | 148 | 1.00x |
| lib-stage2-lean | 0.021 | 0.025 | 0.12 | 148 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.042 | 0.06 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.041* | *0.07* | *147* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.041* | *0.13* | *147* | *1.00x* |
| lib-stage1 | 0.023 | 0.039 | 0.11 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.12 | 147 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.065* | *0.07* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.065* | *0.09* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.065 | 0.09 | 138 | 1.00x |
| bq-expand | 0.138 | 0.238 | 0.11 | 122 | 3.22x |
| *bq-expand-aa-adjacent* | *0.138* | *0.238* | *0.10* | *122* | *3.22x* |
| *bq-expand-aa-distant* | *0.138* | *0.238* | *0.13* | *122* | *3.22x* |
| lib-stage0 | 0.989 | 0.999 | 0.26 | 85 | 26.12x |
| list (baseline) | 1.000 | 1.000 | 0.24 | 85 | 26.11x |
| *list-aa-distant* | *1.003* | *1.003* | *0.26* | *85* | *26.11x* |
| *list-aa-adjacent* | *1.005* | *1.005* | *0.18* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9967, worst cell 0.64% on `rev-cnn-L1-24x24-c1`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.03% on `rev-gather48-src-50`, its interval covering 1. The in-situ term reads 0.9962, 1.0260 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9982, which the correction amplifies by 2.16x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m8s, peak 96 MiB in use, 24 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.61 ms per call raw, 4.46 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.065/0.047/0.025

**Across the halves:** 7 of the 18 arms are faster on this half and 11 slower, at a geomean of 1.1032, from `lib-stage1` at 0.9792 to `bq-expand-aa-distant` at 1.3074, with `list` itself at 1.2889. **The baseline moved 28.89% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.065, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage2-disp` leads outside the vecdims arms at 0.021, priced against `mut-odo-vecdims` at 0.4894 over 3 of 3 shapes at sign p 0.25, a margin of 51.06% against this class's 0.33% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 28.89 of a point, at a class geomean of 1.1032 over the 18 arms, with 7 of 10 strategies past an A/A bar of 0.48 points. The counted work reads a counts geomean of 1.1659 over the same arms, 18 of them counted. Its counted work parts by 16.59 points where its clock parts by 10.32, so about 0.62 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.41 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.41 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.51 | 62 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.26* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| lib-stage3-lean | 0.016 | 0.019 | 0.39 | 62 | 1.00x |
| lib-stage2-disp | 0.016 | 0.020 | 0.29 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.019* | *0.50* | *62* | *1.00x* |
| lib-stage2-lean | 0.016 | 0.020 | 0.33 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.40 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.17 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.019 | 0.41 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.056* | *0.36* | *61* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.021* | *0.056* | *0.30* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.022** | 0.056 | 0.06 | 61 | 1.00x |
| bq-expand | 0.094 | 0.139 | 0.68 | 46 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.139* | *0.70* | *46* | *1.00x* |
| *bq-expand-aa-distant* | *0.095* | *0.142* | *0.04* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.15 | 17 | 20.99x |
| lib-stage0 | 1.001 | 1.007 | 1.41 | 17 | 20.99x |
| *list-aa-distant* | *1.004* | *1.009* | *0.89* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.009* | *1.012* | *0.84* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0099, worst cell 2.57% on `bcast-tall-Mx2`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.05% on `bcast-inner8`, its interval missing 1. The in-situ term reads 1.0212, 1.0141 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0075, which the correction amplifies by 1.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 180 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.1 ms per call raw, 29 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.056/0.016/0.019/0.019

**Across the halves:** 10 of the 18 arms are faster on this half and 8 slower, at a geomean of 1.0947, from `lib-stage3-lean` at 0.9947 to `lib-stage0` at 1.3715, with `list` itself at 1.3692. **The baseline moved 36.92% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.056, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.016, priced against `mut-odo-vecdims` at 0.6531 over 6 of 6 shapes at sign p 0.031, a margin of 34.69% against this class's 0.99% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 36.92 of a point, at a class geomean of 1.0947 over the 18 arms, with 3 of 10 strategies past an A/A bar of 0.88 points. The counted work reads a counts geomean of 1.1722 over the same arms, 18 of them counted. Its counted work parts by 17.22 points where its clock parts by 9.47, so about 0.55 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.38* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.34 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.38 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.42 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.29 | 82 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.27* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.020 | 0.33 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.019 | 0.32 | 82 | 1.00x |
| lib-stage3-lean | 0.012 | 0.018 | 0.31 | 82 | 1.00x |
| lib-stage2-disp | 0.012 | 0.018 | 0.27 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.40 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.36* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.35* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.28 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.030* | *0.053* | *0.29* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.030* | *0.053* | *0.38* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.030** | 0.053 | 0.42 | 76 | 1.00x |
| *bq-expand-aa-distant* | *0.101* | *0.184* | *0.44* | *60* | *1.92x* |
| *bq-expand-aa-adjacent* | *0.101* | *0.185* | *0.50* | *60* | *1.92x* |
| bq-expand | 0.101 | 0.186 | 0.41 | 60 | 1.92x |
| list (baseline) | 1.000 | 1.000 | 0.89 | 28 | 23.56x |
| lib-stage0 | 1.001 | 1.015 | 0.87 | 28 | 23.56x |
| *list-aa-distant* | *1.002* | *1.007* | *0.78* | *28* | *23.56x* |
| *list-aa-adjacent* | *1.003* | *1.005* | *0.82* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9972, worst cell 0.76% on `bcastmid-c32-cnn`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `bcastmid-c32-cnn`, its interval covering 1. The in-situ term reads 1.0203, 1.1033 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9982, which the correction amplifies by 1.93x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m49s, peak 129 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 49.2 ms per call raw, 48.1 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 6 of the 18 arms are faster on this half and 12 slower, at a geomean of 1.0925, from `mut-odo-vecdims-aa-distant` at 0.9953 to `bq-expand` at 1.2655, with `list` itself at 1.2440. **The baseline moved 24.40% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.012, priced against `mut-odo-vecdims` at 0.4170 over 4 of 4 shapes at sign p 0.12, a margin of 58.30% against this class's 0.28% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 24.40 of a point, at a class geomean of 1.0925 over the 18 arms, with 4 of 10 strategies past an A/A bar of 1.35 points. The counted work reads a counts geomean of 1.1720 over the same arms, 18 of them counted. Its counted work parts by 17.20 points where its clock parts by 9.25, so about 0.54 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.30* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.23 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.20 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.17 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.22 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.04 | 105 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.05 | 105 | 0.02x |
| libunord-stage15-sum | -- | -- | 0.05 | 105 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.16 | 100 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.04 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.027 | 0.18 | 84 | 1.00x |
| lib-stage2-disp | 0.023 | 0.027 | 0.18 | 84 | 1.00x |
| lib-stage2-lean | 0.023 | 0.027 | 0.19 | 84 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.16 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.029 | 0.17 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.18* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.18 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.18* | *82* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.051* | *0.084* | *0.15* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.084 | 0.14 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.084* | *0.17* | *76* | *1.00x* |
| bq-expand | 0.179 | 0.212 | 0.36 | 57 | 3.86x |
| *bq-expand-aa-adjacent* | *0.179* | *0.213* | *0.34* | *57* | *3.86x* |
| *bq-expand-aa-distant* | *0.180* | *0.213* | *0.23* | *57* | *3.86x* |
| lib-stage0 | 0.995 | 1.002 | 0.52 | 30 | 27.66x |
| list (baseline) | 1.000 | 1.000 | 0.49 | 30 | 27.66x |
| *list-aa-distant* | *1.001* | *1.010* | *0.47* | *30* | *27.66x* |
| *list-aa-adjacent* | *1.002* | *1.011* | *0.42* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0024, worst cell 1.06% on `window-32x32-c64-k3`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.19% on `window-64x64-c16-k3`, its interval covering 1. The in-situ term reads 1.0073, 1.1931 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0024, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m30s, peak 120 MiB in use, 48 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14 ms per call raw, 13.6 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.084/0.032/0.052/0.051/0.053/0.053

**Across the halves:** 7 of the 18 arms are faster on this half and 11 slower, at a geomean of 1.1355, from `lib-stage1` at 0.9791 to `bq-expand-aa-distant` at 1.5332, with `list` itself at 1.2924. **The baseline moved 29.24% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.084, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.4142 over 8 of 8 shapes at sign p 0.0078, a margin of 58.58% against this class's 0.24% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 29.24 of a point, at a class geomean of 1.1355 over the 18 arms, with 4 of 10 strategies past an A/A bar of 0.74 points. The counted work reads a counts geomean of 1.1762 over the same arms, 18 of them counted. Its counted work parts by 17.62 points where its clock parts by 13.55, so about 0.77 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.20 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.13 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.15 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.12 | 128 | 1.00x |
| libunord-stage15-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.21 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.09* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *137* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *137* | *0.00x* |
| lib-stage1 | 0.022 | 0.031 | 0.10 | 128 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.031 | 0.16 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.031* | *0.11* | *127* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.023* | *0.031* | *0.11* | *127* | *1.00x* |
| lib-stage2-lean-u1 | 0.023 | 0.030 | 0.10 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.031 | 0.12 | 128 | 1.00x |
| lib-stage3-lean | 0.023 | 0.031 | 0.18 | 128 | 1.00x |
| lib-stage2-disp | 0.023 | 0.031 | 0.18 | 128 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.030* | *0.06* | *127* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.030* | *0.08* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.030 | 0.06 | 127 | 1.00x |
| bq-expand | 0.093 | 0.103 | 0.07 | 111 | 1.21x |
| *bq-expand-aa-adjacent* | *0.093* | *0.103* | *0.08* | *111* | *1.21x* |
| *bq-expand-aa-distant* | *0.093* | *0.104* | *0.07* | *111* | *1.21x* |
| *list-aa-adjacent* | *1.000* | *1.003* | *0.15* | *69* | *21.49x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 69 | 21.49x |
| *list-aa-distant* | *1.002* | *1.006* | *0.27* | *69* | *21.49x* |
| lib-stage0 | 1.004 | 1.011 | 0.26 | 69 | 21.50x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9896, worst cell 1.53% on `scaled-super-r3`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.26% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0103, 1.0168 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9955, which the correction amplifies by 2.28x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m8s, peak 111 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.31 ms per call raw, 5.13 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.029/0.030

**Across the halves:** 4 of the 18 arms are faster on this half and 14 slower, at a geomean of 1.0786, from `lib-stage2-lean-u1` at 0.9957 to `list-aa-adjacent` at 1.3124, with `list` itself at 1.3024. **The baseline moved 30.24% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.030, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.8874 over 2 of 3 shapes at sign p 1, a margin of 11.26% against this class's 1.04% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 30.24 of a point, at a class geomean of 1.0786 over the 18 arms, with 5 of 10 strategies past an A/A bar of 0.77 points. The counted work reads a counts geomean of 1.1556 over the same arms, 18 of them counted. Its counted work parts by 15.56 points where its clock parts by 7.86, so about 0.50 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen, and cut to sixteen for Run 41, `runs-3` (`sInner` 3, a k3 conv row) leaving timing in `94aeee7` and staying in `check`.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *52* | *1.07x* |
| liblist-stage1-sum | -- | -- | 0.07 | 62 | 0.35x |
| liblist-stage4-sum | -- | -- | 0.02 | 75 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.07 | 62 | 0.35x |
| libunord-stage13-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 73 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 75 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage2-disp | 0.023 | 0.024 | 0.11 | 60 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.024 | 0.13 | 60 | 1.00x |
| lib-stage3-lean | 0.023 | 0.024 | 0.10 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.024 | 0.11 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.026* | *0.40* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.026 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.025* | *0.026* | *0.13* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.057 | 0.08 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.057* | *0.09* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.08* | *59* | *1.00x* |
| lib-stage0 | 0.085 | 1.058 | 0.16 | 52 | 1.35x |
| lib-stage1 | 0.086 | 1.073 | 0.21 | 52 | 1.35x |
| *bq-expand-aa-adjacent* | *0.093* | *0.139* | *0.47* | *46* | *1.07x* |
| bq-expand | 0.094 | 0.139 | 0.45 | 46 | 1.07x |
| *bq-expand-aa-distant* | *0.095* | *0.142* | *0.05* | *46* | *1.07x* |
| list (baseline) | 1.000 | 1.000 | 2.60 | 17 | 21.26x |
| *list-aa-distant* | *1.032* | *1.050* | *0.25* | *17* | *21.26x* |
| *list-aa-adjacent* | *1.033* | *1.050* | *0.21* | *17* | *21.26x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0330, worst cell 4.95% on `runs-16384`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.42% on `runs-9`, its interval covering 1. The in-situ term reads 1.0299, 1.0370 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0319, which the correction amplifies by 1.04x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h43m4s, peak 610 MiB in use, 270 MiB max residency; the reader reads 31 benchmarks over 16 shapes of the runs class. Anchor: `runs-2`, `list` at 41.7 ms per call raw, 40.6 ms net.

**Per shape, in the run's shape order (runs-2, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.040/0.038/0.033/0.030/0.026/0.025/0.025/0.025/0.025/0.025/0.024/0.025/0.024/0.024/0.026

**Across the halves:** 9 of the 18 arms are faster on this half and 9 slower, at a geomean of 1.0685, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9931 to `list` at 1.3256, with `list` itself at 1.3256. **The baseline moved 32.56% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.07x, 21.26x --- and `lib-stage2-disp` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.8051 over 16 of 16 shapes at sign p 3.1e-05, a margin of 19.49% against this class's 3.30% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 32.56 of a point, at a class geomean of 1.0685 over the 18 arms, with 2 of 10 strategies past an A/A bar of 0.49 points. The counted work reads a counts geomean of 1.1492 over the same arms, 18 of them counted. Its counted work parts by 14.92 points where its clock parts by 6.85, so about 0.46 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.16 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.10 | 92 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.12 | 92 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *93* | *0.00x* |
| lib-stage3-lean | 0.022 | 0.042 | 0.12 | 84 | 1.00x |
| lib-stage2-lean | 0.022 | 0.042 | 0.10 | 84 | 1.00x |
| lib-stage2-disp | 0.022 | 0.042 | 0.11 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.046 | 0.13 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.34* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.043 | 0.07 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.043* | *0.13* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.10* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.12* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.11 | 77 | 1.00x |
| lib-stage1 | 0.033 | 0.048 | 0.13 | 82 | 1.00x |
| bq-expand | 0.091 | 0.181 | 0.43 | 60 | 1.05x |
| *bq-expand-aa-adjacent* | *0.091* | *0.184* | *0.43* | *60* | *1.05x* |
| *bq-expand-aa-distant* | *0.093* | *0.184* | *0.09* | *60* | *1.05x* |
| lib-stage0 | 0.991 | 1.010 | 0.41 | 50 | 21.07x |
| list (baseline) | 1.000 | 1.000 | 0.69 | 32 | 21.18x |
| *list-aa-distant* | *1.003* | *1.016* | *0.48* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.009* | *1.024* | *0.29* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0158, worst cell 5.91% on `flip-last-rows`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9993 on a worst cell of 0.37% on `flip-whole-square`, its interval missing 1. The in-situ term reads 1.0189, 1.0174 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0120, which the correction amplifies by 1.34x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.053/0.049/0.026/0.026

**Across the halves:** 7 of the 18 arms are faster on this half and 11 slower, at a geomean of 1.0735, from `lib-stage1` at 0.9925 to `list` at 1.3105, with `list` itself at 1.3105. **The baseline moved 31.05% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.7284 over 6 of 6 shapes at sign p 0.031, a margin of 27.16% against this class's 1.58% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.05 of a point, at a class geomean of 1.0735 over the 18 arms, with 3 of 10 strategies past an A/A bar of 1.25 points. The counted work reads a counts geomean of 1.1509 over the same arms, 18 of them counted. Its counted work parts by 15.09 points where its clock parts by 7.35, so about 0.49 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.11 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.03 | 130 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.03 | 130 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.03 | 130 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.03 | 130 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 130 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 130 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.22* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *122* | *0.00x* |
| lib-stage2-lean | 0.020 | 0.023 | 0.16 | 112 | 1.00x |
| lib-stage3-lean | 0.020 | 0.023 | 0.13 | 112 | 1.00x |
| lib-stage2-disp | 0.020 | 0.023 | 0.11 | 112 | 1.00x |
| lib-stage2-lean-u1 | 0.021 | 0.025 | 0.11 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.025* | *0.09* | *111* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.025* | *0.10* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.025 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.07* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.08 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.10* | *111* | *1.00x* |
| lib-stage1 | 0.049 | 0.058 | 0.15 | 104 | 1.42x |
| lib-stage0 | 0.050 | 0.058 | 0.14 | 104 | 1.42x |
| *bq-expand-aa-distant* | *0.088* | *0.089* | *0.09* | *96* | *1.06x* |
| *bq-expand-aa-adjacent* | *0.088* | *0.089* | *0.12* | *96* | *1.06x* |
| bq-expand | 0.088 | 0.089 | 0.14 | 96 | 1.06x |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.16* | *55* | *21.22x* |
| *list-aa-distant* | *1.000* | *1.002* | *0.21* | *55* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.27 | 55 | 21.22x |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 0.9972, worst cell 0.70% on `block-run64-page`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.06% on `block-r3-vol64`, its interval missing 1. The in-situ term reads 1.0187, 1.0254 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9980, which the correction amplifies by 1.40x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 134 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.56 ms per call raw, 4.41 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.020/0.025/0.029/0.024/0.020

**Across the halves:** 5 of the 18 arms are faster on this half and 13 slower, at a geomean of 1.0567, from `mut-odo-vecdims-aa-distant` at 0.9958 to `list` at 1.3237, with `list` itself at 1.3237. **The baseline moved 32.37% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.020, priced against `mut-odo-vecdims` at 0.8596 over 5 of 5 shapes at sign p 0.062, a margin of 14.04% against this class's 0.28% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 32.37 of a point, at a class geomean of 1.0567 over the 18 arms, with 8 of 10 strategies past an A/A bar of 0.21 points. The counted work reads a counts geomean of 1.1392 over the same arms, 18 of them counted. Its counted work parts by 13.92 points where its clock parts by 5.67, so about 0.41 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.22 | 228 | 1.69x |
| liblist-stage4-sum | -- | -- | 0.11 | 243 | 1.16x |
| liblist-stage5-sum | -- | -- | 0.14 | 243 | 1.17x |
| libunord-stage1-sum | -- | -- | 0.33 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.09 | 245 | 0.16x |
| libunord-stage14-sum | -- | -- | 0.11 | 244 | 0.20x |
| libunord-stage15-sum | -- | -- | 0.10 | 244 | 0.20x |
| libunord-stage6-loop-sum | -- | -- | 0.19 | 239 | 0.55x |
| libunord-stage6-sum | -- | -- | 0.17 | 239 | 0.55x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.34* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.02* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.02* | *250* | *0.01x* |
| lib-stage3-lean | 0.033 | 0.049 | 0.15 | 235 | 1.13x |
| lib-stage2-disp | 0.033 | 0.049 | 0.14 | 235 | 1.13x |
| lib-stage2-lean | 0.034 | 0.050 | 0.18 | 235 | 1.13x |
| lib-stage2-lean-u1 | 0.034 | 0.048 | 0.24 | 234 | 1.13x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.052* | *0.066* | *0.17* | *230* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.052* | *0.066* | *0.20* | *230* | *1.28x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.052 | 0.066 | 0.21 | 230 | 1.28x |
| *mut-odo-vecdims-aa* | *0.061* | *0.088* | *0.19* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.061** | 0.088 | 0.15 | 229 | 1.27x |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.088* | *0.20* | *229* | *1.27x* |
| lib-stage1 | 0.082 | 0.105 | 0.24 | 221 | 2.36x |
| bq-expand | 0.138 | 0.198 | 0.12 | 217 | 1.44x |
| *bq-expand-aa-distant* | *0.138* | *0.199* | *0.15* | *217* | *1.44x* |
| *bq-expand-aa-adjacent* | *0.138* | *0.198* | *0.17* | *217* | *1.44x* |
| *list-aa-adjacent* | *0.999* | *1.001* | *0.12* | *180* | *21.57x* |
| *list-aa-distant* | *1.000* | *1.003* | *0.15* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.13 | 180 | 21.57x |
| lib-stage0 | 1.023 | 1.041 | 0.15 | 187 | 21.95x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 0.9964, worst cell 0.85% on `small-bcast32`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.26% on `small-bcast32`, its interval covering 1. The in-situ term reads 0.9784, 0.9924 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9978, which the correction amplifies by 1.54x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m30s, peak 132 MiB in use, 52 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.6 us per call raw, 6.37 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.042/0.077/0.050/0.058/0.088

**Across the halves:** 5 of the 18 arms are faster on this half and 13 slower, at a geomean of 1.0748, from `lib-stage1` at 0.9786 to `list-aa-distant` at 1.2922, with `list` itself at 1.2918. **The baseline moved 29.18% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.033, priced against `mut-odo-vecdims` at 0.4412 over 5 of 5 shapes at sign p 0.062, a margin of 55.88% against this class's 0.36% floor (`mut-odo-vecdims-aa`). Its two columns may NOT be differenced, `list` having moved 29.18 of a point, at a class geomean of 1.0748 over the 18 arms, with 8 of 10 strategies past an A/A bar of 0.78 points. The counted work reads a counts geomean of 1.1421 over the same arms, 18 of them counted. Its counted work parts by 14.21 points where its clock parts by 7.48, so about 0.53 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500), and the two views that landed 2026-09-26, for Run 42, and grew from 4992 elements to `sizeCap` on 2026-09-27 (`aa18c24`), for Run 43 --- `compose-bcast-nest` (`l` 1800000, `sInner` 6) and `compose-bcast-wide` (`l` 1800000, `sInner` 120). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero; the two grown ones put a broadcast beside short runs under a reversed nest --- of extent 6 beside runs of 10 under three strided axes nothing merges on `compose-bcast-nest`, of extent 120 beside runs of 6 under five strided axes of extent 4 or 5 on `compose-bcast-wide` --- so that where the unordered stages place the zero-stride axis decides which extent the odometer turns over on.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.58* | *52* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.42 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.43 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.46 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 82 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.22 | 80 | 0.01x |
| libunord-stage15-sum | -- | -- | 0.02 | 82 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.47 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.46 | 62 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.25* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.014 | 0.018 | 0.40 | 62 | 1.00x |
| lib-stage2-disp | 0.014 | 0.018 | 0.35 | 62 | 1.00x |
| lib-stage2-lean | 0.014 | 0.018 | 0.37 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.019* | *0.38* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.014 | 0.019 | 0.39 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.014* | *0.019* | *0.47* | *62* | *1.00x* |
| lib-stage1 | 0.015 | 0.018 | 0.24 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.44 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.036* | *0.31* | *61* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.036* | *0.31* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.036 | 0.20 | 61 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.121* | *0.66* | *46* | *1.35x* |
| bq-expand | 0.094 | 0.121 | 0.64 | 46 | 1.35x |
| *bq-expand-aa-distant* | *0.094* | *0.122* | *0.23* | *46* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 1.12 | 17 | 22.01x |
| *list-aa-adjacent* | *1.001* | *1.008* | *0.91* | *17* | *22.01x* |
| *list-aa-distant* | *1.001* | *1.004* | *1.04* | *17* | *22.01x* |
| lib-stage0 | 1.002 | 1.005 | 1.22 | 17 | 22.01x |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0043, worst cell 0.76% on `compose-bcast-nest`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.02% on `compose-bcast-nest`, its interval covering 1. The in-situ term reads 1.0188, 1.0268 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0031, which the correction amplifies by 1.35x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m16s, peak 142 MiB in use, 41 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.6 ms per call raw, 29.5 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar, compose-bcast-nest, compose-bcast-wide):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019/0.036/0.012

**Across the halves:** 7 of the 18 arms are faster on this half and 11 slower, at a geomean of 1.0825, from `mut-odo-vecdims-aa-distant` at 0.9961 to `list-aa-adjacent` at 1.3010, with `list` itself at 1.2998. **The baseline moved 29.98% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.036, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.014, priced against `mut-odo-vecdims` at 0.6223 over 6 of 6 shapes at sign p 0.031, a margin of 37.77% against this class's 0.43% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 29.98 of a point, at a class geomean of 1.0825 over the 18 arms, with 5 of 10 strategies past an A/A bar of 0.28 points. The counted work reads a counts geomean of 1.1625 over the same arms, 18 of them counted. Its counted work parts by 16.25 points where its clock parts by 8.25, so about 0.51 of the instruction saving reaches the clock.


## Provenance

**Run 45's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `f5bf411`; one shim, `align-as.py` at `1a359bd`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 reporting `10.1.20260918` as patched on 2026-10-03 and reached through `cabal.project.ghead`; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run45-gheadnospec` and is what every table here publishes; `run45-gheadtwopass` is the candidate. **What is new against Run 44 is not the pair but the SOURCE under both halves, and nothing else.** `Main.hs` moved by two of the owner's commits, `c100112` to `f5bf411`: `b5cd52e` retires `libunord-stage7-sum` and `-stage9-sum`, adds `lib-stage0`, times `lib-stage2-disp` again rebuilt over `lib-stage2-lean` with `dispRun` re-cut from 2048 to 32768, and has `fillStage2Axes` count its level loop down as `pr-mikolaj-toVectorListT`'s fill does; `f5bf411` sorts `routeUnord13`'s axes by insertion, its merge loop top-level. The compiler is the one Run 44 built with, the stage1 at the recipe's path md5 `39db416de5ed25e1b272d801bfa405d7`, patched to the Core optimizer and not GHC [#27742](https://gitlab.haskell.org/ghc/ghc/-/work_items/27742)'s spill fix, and every ABI hash `run45-gheadnospec` carries is `run44-gheadnospec`'s. The shim, the recipes, `cabal.project.ghead`, `micro.cabal` and the launch are Run 44's to the character, and no reboot sits between the two runs, `uptime -s` reading 2026-09-24 00:00:31, before Run 43's build.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 62 class views over ten classes for 1922 more, and it is Run 44's but for two arms out and two in, every shape and view unmoved.** `./roster-delta.py run44-gheadnospec run45-gheadnospec`, read off the two binaries, reads `libunord-stage7-sum` and `libunord-stage9-sum` out and `lib-stage0` and `lib-stage2-disp` in, the twenty-nine survivors in Run 44's order, every class at its count and the geometry of every shape and view the two carry unmoved. So pre-run step 12's condition fired on the membership, and its -L1 roster pass was taken on the basis on 2026-10-04 from 19:31, every leg exiting 0 and finding nothing structural.

**The evening ran in ONE window and in the order the run list gives, and foreign CPU met two A/A benches of one shape on the basis's main set, whose rerun the owner declined.** `run-evening.sh` took the gate from 02:08:41 to 02:42:02, the alarm at 02:42:06 reading 0.1% busy, the sequence from 02:42:06 to 09:58:35 and the riders from 09:58:35 to 10:11:04, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back --- 20 class processes, one per class per half, and two main-set ones --- every process reporting rc=0 and the bench count asked of it and each launched from `./run45-<half>`. The counted work, which wants no quiet machine, ran from 10:11 to 11:33 in three calls, with the `-g3` twins building and this write-up's first readings running beside it. **The owner took the quiet box back from 10:36 to 11:12**, the counts stopped by hand for it twice, for three readings the results called for and no table here reads: the copy test of this run's half-local movers ([Results](#results)) and two cycle sweeps behind item (2)'s kill, clean and under `SATURATE=1` ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)). `--wild` finds benches at or above 0.25 of a core foreign in 1 of the 22 sequence logs, `run45-gheadnospec-main`, 2 of its 589 benches, peak 1.79: `cnn-slice-c32/bq-expand-aa-distant` at 1.79 of a core and `cnn-slice-c32/list-aa-adjacent` at 0.42, on the mutator clock 1.057 and 1.056 of their own twins, `bq-expand` and `list`, on the same shape. **Post-run step 3's rerun of the main set on both halves was DECLINED**: the note's `RERUN:` line says `ask`, and the owner, asked on their return, chose the sensitivity reading in its place: `--compare --exclude-shape cnn-slice-c32` moves `list`'s cross from 1.2929 to 1.2941 and `bq-expand`'s from 1.3048 to 1.2997, no span the registration reads on either arm changing its verdict, and takes the basis's main-set floor from 0.85% to 0.53%, the intruded `bq-expand-aa-distant` carrying it either way.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes read `list` 1.2991 and 1.2975, `mut-odo-vecdims` 1.0011 and 1.0007, `bq-expand` 1.3079 and 1.3102 --- 0.16, 0.04 and 0.23 points apart. Between its own two legs `gheadnospec` moved by at most 0.34 points and `gheadtwopass` by at most 0.16, both on `bq-expand`, so what the passes part by is the two halves' legs and not a disagreement about the pair; `mut-odo-vecdims`, the arm the two passes leave alone, sits above 1 on both passes, by 0.11 and 0.07 of a point (`./read-run.py --gate-draft run45` prints the four readings, the two passes and each half's own two legs). The machine check, which reads the gate's first basis process and so neither main-set process, against the fingerprint Run 44 installed --- this run's basis recipe on the source before its two commits --- puts `list`'s net at **-0.60%**, worst `stretch-square-1341` at **-2.59%**, none of 19 shapes past 5% and the geomean inside the 3% bar, so the source's term moved the box's `list` by under the bars.

**Every one of the twenty-two processes gated clean and the plateau refused by declaration, and five A/A worst cells pass the 5% `read-all.sh` reports at, one of them past 10%.** `read-all.sh` gates each process on its own correction and passes 22 of 22. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.9735 to 21.3974 ms/iter across the run, a 26.06% spread against a 5% band, and it splits exactly by half, `gheadnospec`'s 11 processes flat within 0.90% at 21.2076 to 21.3974 and `gheadtwopass`'s within 1.82% at 16.9735 to 17.2818 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-main` at **13.81%** on `vgg-14-c512-k3`, `mut-odo-vecdims-aa-distant` against `mut-odo-vecdims`; `gheadtwopass-window` at **9.32%** on `window-224x224-k3-d2`, the same pair; `gheadnospec-main` at **6.61%** on `cnn-slice-c32`, `bq-expand-aa-distant` against `bq-expand`, the intrusion above; `gheadnospec-flip` at **5.91%** on `flip-last-rows`, `bq-expand-aa-distant` against `bq-expand` again; and `gheadtwopass-runs` at **5.64%** on `runs-r3-48x30`, `list-aa-distant` against `list`. `--wild` finds no foreign CPU on any but the intrusion's, and on the mutator clock the slow member is the arm itself on the first, `mut-odo-vecdims` at 1.043 and 1.045 of its two copies, the copy on the second at 1.046 and the fourth at 1.040, and `list` itself on the fifth at 1.019, each on allocation equal to within 1e-4. **Only the first passes the about 10% past which [the open list][open] takes a worst cell out of the per-shape record**, so that cell leaves it and its row is flagged. The main set's floor is 0.85% on the basis and 0.72% on the control.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run45-gheadnospec`, md5 `4d7a37864d30c1ece286573237f95429`, and `run45-gheadtwopass`, md5 `3f152181e17531a770752cfb19b37f93`, built on 2026-10-04 from `Main.hs` at `f5bf411`, clean against it, and run from a tree at `3513ffb`, whose `Main.hs` differs from `f5bf411` in comment lines alone. Their `.text` sections are **20141887** and **20174655** bytes, the first column of `size -A`; against Run 44's two the basis is larger by 8192 bytes and the flagged half by 4096, two pages and one exactly --- the two commits' term, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 32768 bytes, eight pages exactly, and it carries MORE self-loops, 311 against 305, so [the open list's entry on it](../README.md#what-is-open) gains a run on that side.

**The two commits kept the basis's six-copy group at offset 0 and moved the copy counts of its two seven-instruction groups.** `./loop-offsets.py --delta run44-gheadnospec run45-gheadnospec`, the same basis recipe on the two sources, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0], with no address surviving to the byte and its two displacements, 0x140 and 0x1580, whole lines; takes the two-copy group at [0, 0] to one copy at [0]; and takes the one-copy group at 11 to two copies at [11, 11]. **Within the pair** the six-copy group reads [0, 0, 0, 0, 0, 0] and the group at 11 reads [11, 11] on both halves, the control carries a three-copy group at [0, 0, 0] as on Runs 41 to 44, and a six-instruction two-copy group sits at [62, 23] on the basis and [30, 55] on the control. `--library` puts **4.4%** of the 804 library self-loops the two halves share at the same offset in line, Run 44's figure over the same count: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 30 on the basis and 27 on the control, where Run 44 read 29 on each, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 305 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 311 on the control, 208 and 137 of them at offset 0, where Run 44 read 304 and 328 self-loops, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 3a's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity twelve straddlers on the basis and fourteen on the control, Run 44's names on both** --- on both, `sumNoSpec` three times, `fillStage3`'s body at offset 30, `fillStage2Short` twice, `fillStage2Axes`, two leaf bodies of `fbMutOdoVecdimsAddInLeafU2`, one each of `fbMutOdoVecdimsAddInLeafU2Down` and `-Last`, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the control `fillStage2OneLevel` and `fbFused` besides. Of the refusals, nine on the basis and seven on the control carry a `--loose` family of `fillStage3`, `fillStage2Short`, `fillStage2VSdims`, `fillStage2OneLevel` and `fillStage2Axes` bodies, which the bytes cannot choose between, and nine on the basis and six on the control are 60- to 63-byte bodies at offset 32, 40 or 48 for which no twin holds a copy. **Neither half's own `-g3` twin holds as many loops as the binary it names for**, 297 against the basis's 305 and 301 against the control's 311, as on Runs 43 and 44, so every name above rests on its own byte match. The twins were built over `Main.hs` at `3513ffb`, `G3_TREE=1` taking the comment-only move since `f5bf411`.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run45-gheadnospec`, 9.992 times apart, which is plain -O1; on `run45-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. Both builders' figures are Run 44's to the byte on both halves, the two commits reaching neither. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.39 us** on `cnn-slice-c32`, **3.69 ms** on `cnn-L2-24x24-c32`, **40.3 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 20.2 to 21.3 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.55 us | 6.39 us | 5.02 us |
| `cnn-L2-24x24-c32` | 165888 | 3.79 ms | 3.69 ms | 2.95 ms |
| `stretch-wide-2xM` | 1800000 | 41.4 ms | 40.3 ms | 31.9 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.61 ms raw and 4.46 ms net; `bcast-inner900` 30.1 ms raw and 29 ms net; `bcastmid-b200k` 49.2 ms raw and 48.1 ms net; `window-128x128-k7` 14 ms raw and 13.6 ms net; `scaled-rank1-m1` 5.31 ms raw and 5.13 ms net; `runs-2` 41.7 ms raw and 40.6 ms net; `flip-fwd-rows96` 30.9 ms raw and 29.8 ms net; `block-r3-vol64` 4.56 ms raw and 4.41 ms net; `small-row96` 6.6 us raw and 6.37 us net; `compose-zero-mid` 30.6 ms raw and 29.5 ms net. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and one cell of the whole run is one the reader flags.** The two `sum-only` arms agree on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9992 to 1.0008 across the twenty-two processes, at a mean absolute difference of at most 0.16% --- so the term subtracted from one half is the term subtracted from the other. **One cell sits below R2 0.99 ([what that column detects][ramp]) and none is under ten samples**, of the run's 5022 cells, 2511 on each half: `cnn-slice-c32/bq-expand-aa-distant` on the basis, at R2 0.9837, the intrusion's cell above.

**The counted work covers every population, no cell was refused anywhere, and the two halves part in work as Run 44's did.** `run-counts-all.sh` wrote 22 sweep files over eleven populations, none refused, at a cost of 1504s on the basis and 1228s on the control by `--counts-totals`, beside Run 44's 1365s and 1108s, the last two calls keeping what the stopped ones had written. The counts geomean over the eighteen arms that carry a corrected time runs **1.1392** on `block` to **1.1762** on `window`, the main set at **1.1675** --- the basis retiring 13.9 to 17.6 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families**: the `bq-expand` trio sits at 0.8649 to 0.8692, retiring 50.63% more instructions on the basis for 30.29 to 30.92% more time; the `list` trio at 0.9998 to 1.0038 and `lib-stage0` beside it at 1.0088, cashing all of what they save; and the eleven others between 0.9440 and 0.9638, retiring 3.83 to 5.45 percent more on the basis while their clocks run from 0.62 of a point below level to 0.20 above. **Read per class the same way, the rate runs 0.41 to 0.77**: the instruction saving reaching the clock is lowest on `block`, where the counted work parts by 13.92 points and the clock by 5.67, and highest on `window`, 17.62 against 13.55 --- where Run 44 read 0.47 to 0.76, lowest then on `flip`.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0001** and **1.0002** on the two halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0244** and **1.1066** on the basis and **1.0415** and **1.0743** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs two and four percent over the term it stands for on `mut-odo-vecdims` and eleven and seven on `bq-expand`, the term that is subtracted being the `sum-only` one and not this proxy.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1183** on the basis and **1.1655** on the control, **4.7** points apart, where Run 44's two parted by 4.8 and Run 43's by 3.7 --- so the two passes change what the spray costs a process as well as what the roster costs it. What the roster adds on top of that state is **1.0145** on the basis, 5 of 19 shapes above 1, and **1.0061** on the control, 11 of 19; the basis's rest runs 0.9663 on `cnn-L1-24x24-c1` to 1.2144 on `stretch-r5-8x432`, the control's 0.9701 on `stretch-bigstride` to 1.0948 on `stretch-tall-Mx2`. The whole in-process deflation is **1.1346** on the basis, 18 of 19 shapes above 1, and **1.1726** on the control, 18 of 19. **The roster cells and the legs are one evening's**, the legs taken straight after the sequence, so the decomposition spans no second window.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 44's, both recipes unchanged to the character, on the owner's word of 2026-10-04 that Run 45 has the same recipe, rebuilt on the source at the tip at build time: both halves the in-tree stage1 reporting `10.1.20260918` as patched on 2026-10-03, through `cabal.project.ghead` at `5221ef0` with `micro.cabal` at `6b9e206`, at plain `-O1`, `align-as.py` at `1a359bd` under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run45-gheadnospec` and `run45-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 44's with the builddir names moved. What the source moves under the recipe is the roster of 2026-10-04, the branch's fill and stage thirteen's route: two unordered stages' consumers retired, `lib-stage0` landing beside `lib-stage1`, `lib-stage2-disp` timed again and rebuilt over `lib-stage2-lean` with `dispRun` re-cut to 32768, `fillStage2Axes` following pr-mikolaj-toVectorListT's fill as its commit "Port the Axis path" has it since 2026-10-04, and `routeUnord13`, the route `libunord-stage13-sum` sums over, sorting by insertion into a merge loop out of line since the same day, as that branch has it since 2026-10-05, reasons at the roster entries, the fill and `sortAxes`. **So the pair's own `cross` figure is the two passes on a tenth build**, and each half against Run 44's same half, `--half-movers run45 run44`, carries the source alone: the stage1 at the recipe's path is the one Run 44 built with, md5 `39db416de5ed25e1b272d801bfa405d7`, every ABI hash `run45-gheadnospec` carries is `run44-gheadnospec`'s, and the shim, `cabal.project.ghead` and `micro.cabal` did not move. `./roster-delta.py run44-gheadnospec run45-gheadnospec` reads `lib-stage0` and `lib-stage2-disp` in and the two retired consumers out, the survivors in their order and every shape, view and geometry unmoved, and `./registration-drift.py run45 --since run44` reaches `liblist-stage4-sum`, `-stage5-sum`, five `libunord-` consumers and every `lib-` arm but `lib-stage1`, and no code behind the `list`, `mut-odo-vecdims` and `bq-expand` families, `lib-stage1`, `liblist-stage1-sum`, `libunord-stage1-sum` or the two `sum-only` halves. **The items' priors are instruction counts, cycles and bytes off this run's own basis binary**, `run45-gheadnospec`, taken with `probe-stalls.sh` at `N=50`, Run 44's counts N, twice, on a quiet box before preflight, from 18:44 to 19:24 on 2026-10-04: into `probe-r45-prior1.txt` and `probe-r45-prior2.txt` over every timed arm and the nineteen main-set shapes, and into their `-compose`, `-bcast` and `-bcastmid` siblings over eleven `lib-`, `liblist-` and `libunord-` arms, those the items read among them, and the shipped leaf, the two sweeps' instructions agreeing arm by arm at 1.0000 by `--counts-over probe-r45-prior2.txt probe-r45-prior1.txt`; bytes a call over the same twelve arms in `probe-r45-alloc.txt` and `probe-r45-alloc-compose.txt`; and instructions alone for `lib-stage2-disp` and `lib-stage2-lean` on `small` and `runs`, taken under step 12's roster pass, in `probe-r45-disp-small.txt` and `probe-r45-disp-runs.txt`. A cycle figure is net of the mean of the two `sum-only` arms, as `--counts --pair` corrects, and raw on a `-sum` arm, read per shape by `probe-r45-cyc.py` beside the sweeps, which keeps a cell marked nonlinear and drops a shape whose net is not positive, naming it. Two more sweeps of the arms whose cycles the items quote were taken on the idle box from 20:32, `probe-r45-quiet1.txt` and `probe-r45-quiet2.txt`, and they part as widely as the first two, a main-set net-cycle geomean near 1 between two fill arms by up to eleven points on either pair, so the spread is the reader's net of the forcing pass at `N=50`, which a quiet box does not remove; a cycle figure is a prior only where the four agree, and the items quote the others to say they part. No probe was taken on the control's recipe, so the priors are the basis's. **The source moved no instruction outside the arms it reaches**: `./read-run.py --counts-over probe-r45-prior1.txt run44-counts-gheadnospec.txt` reads every arm both runs time at 0.9999 to 1.0001 of Run 44's but three, `lib-stage2-lean` at 1.0081, `liblist-stage4-sum` at 1.0100 and `libunord-stage13-sum` at 0.9860. **The limit this run cannot remove**: a rebuild moves every loop --- `./loop-offsets.py --delta run44-gheadnospec run45-gheadnospec` finds no address of the loops it compares surviving to the byte --- so a figure on unmoved instructions is predicted only within the spread earlier builds drew.

(1) *The count-down level loop gives `lib-stage2-lean` back what Run 44's bounded loop cost it: level with `lib-stage3-lean` or ahead of it on the cell where that cost was found, and on the main set back toward Run 43's reading.* On `stretch-wide-2xM`, `SHAPE=stretch-wide-2xM probe-r45-cyc.py` puts `lib-stage3-lean` at 1.0007 and 0.9910 of `lib-stage2-lean` in net cycles on `probe-r45-prior1.txt` and `probe-r45-prior2.txt` and at 1.1000 and 1.0552 on `probe-r45-quiet1.txt` and `probe-r45-quiet2.txt`, the first of those two on a `lib-stage3-lean` cell marked nonlinear, all four on instructions level at 1.0000; the same reader puts Run 44's sweeps at 0.8508 and 0.8613 on 1.0417, `probe-r44-prior1.txt` and `probe-r44-prior2.txt`, and Run 44 read the cell at 0.845 in time, the low end of `--pair lib-stage3-lean lib-stage2-lean`'s range on `run44-gheadnospec-main.json`, so its cycles priced it. Over the main set the four sweeps' net cycles run from 0.9227 to 1.0149, as Run 44's two parted, 1.0234 and 0.9879, so the main-set band is drawn from the counts and the time readings either side: `--counts probe-r45-prior1.txt --pair lib-stage3-lean lib-stage2-lean` on `run44-gheadnospec-main.json` reads 0.9974 corrected where `--counts probe-r44-prior1.txt` reads 1.0131, and `--pair lib-stage3-lean lib-stage2-lean` reads 0.9709 on `run44-gheadnospec-main.json` and 1.0066 on `run43-gheadnospec-main.json`, the bounded loop's build and the last counted one's, the band holding the second and not the first. `predict: cell stretch-wide-2xM/lib-stage3-lean over stretch-wide-2xM/lib-stage2-lean 1.02 within 4% on main basis`, holding the three readings on linear cells, and `predict: pair lib-stage3-lean lib-stage2-lean 1.00 within 1.5% on main basis`. A cell under 0.98 says the count-down did not take the loop's cost back in this build, and one over 1.06 that it bought more than the cost; a pair under 0.985 with the cell held, that the cost Run 44 read lay on other shapes as well, and one over 1.015, that stage three lost ground the loop does not explain.

**Read by --predictions, item (1):** `cell stretch-wide-2xM/lib-stage3-lean over stretch-wide-2xM/lib-stage2-lean 1.02 within 4% on main basis`: HELD on main basis, read 1.0053 over 1 shape(s), 1.47 point(s) off, within 4.00% --- `pair lib-stage3-lean lib-stage2-lean 1.00 within 1.5% on main basis`: HELD on main basis, read 1.0013 over 19 shape(s), 0.13 point(s) off, within 1.50%.

(2) *`lib-stage0`, master's `toVectorT`, runs regime 3 at about twenty-eight times `lib-stage1`'s fill, every main-set shape being regime 3 and the two arms parting in regime 3 alone.* `--counts probe-r45-prior1.txt --pair lib-stage0 lib-stage1` on `run44-gheadnospec-main.json` reads 31.0070 corrected over the eighteen shapes it keeps, `cnn-L1-6x6-c1` dropped for a nonlinear cell, and 15.2125 raw; `probe-r45-cyc.py` puts the four sweeps' net cycles at 27.0065, 29.2027, 26.4249 and 28.1165, the last over eighteen shapes, and `probe-r45-alloc.txt` its bytes a call at 22.93 of stage one's. `predict: pair lib-stage0 lib-stage1 27.8 within 250% on main basis`, the band holding the four cycle readings with a point to spare each side, since time follows cycles, and not the counted 31.0070, the list route retiring more instructions a cycle than the fill. A reading outside it says the list route's time does not follow its cycles as the fill's does; the control has no prior.

**Read by --predictions, item (2):** `pair lib-stage0 lib-stage1 27.8 within 250% on main basis`: KILLED on main basis, read 35.0472 over 19 shape(s), 724.72 point(s) off, within 250.00%.

(3) *`lib-stage2-disp` is `lib-stage2-lean`'s code below a canonical run of 32768, which no main-set shape and no `small` view reaches, so the two read as an A/A there on both halves.* `--counts probe-r45-prior1.txt --pair lib-stage2-disp lib-stage2-lean` on `run44-gheadnospec-main.json` reads 1.0001 corrected and raw over the nineteen shapes, and `probe-r45-disp-small.txt` puts the dispatch at 1.0000 to 1.0041 of lean's corrected instructions on the five `small` views; `probe-r45-disp-runs.txt` reads them level on every `runs` view but `runs-65536`, where the slice route executes 0.1379 of the fill's, which is why `runs` is not in the span. The four sweeps' net cycles run from 0.9834 to 1.0552 on that one code, which is the reader's spread and not a prior. `predict: pair lib-stage2-disp lib-stage2-lean 1.0 on main,small both`. A reading past the floor says the dispatch's own test costs time or a run reaches the cut.

**Read by --predictions, item (3):** `pair lib-stage2-disp lib-stage2-lean 1.0 on main,small both`: HELD on main basis, read 1.0021 over 19 shape(s), 0.21 point(s) off, within 0.85%; HELD on main control, read 1.0017 over 19 shape(s), 0.17 point(s) off, within 0.72%; KILLED on small basis, read 0.9873 over 5 shape(s), 1.27 point(s) off, within 0.36%; HELD on small control, read 0.9992 over 5 shape(s), 0.08 point(s) off, within 0.52%.

(4) *`sortAxes` saves `libunord-stage13-sum` instructions against `libunord-stage15-sum` on every view the sweeps read, and some of that saving reaches the clock on the main set.* `probe-r45-prior1.txt` and its `-compose`, `-bcast` and `-bcastmid` siblings put stage thirteen below stage fifteen by 113 to 1280 instructions a call on the main set, 172 to 645 on `compose`, 124 to 287 on `bcast` and 272 to 941 on `bcastmid`, where `probe-r44-prior1.txt` read 2 to 22 on the main set; `probe-r45-alloc.txt` puts its bytes at 0.5326 of stage fifteen's over the main set, where `probe-r44-alloc.txt` read 0.9748. In raw instructions stage thirteen reads 0.9855 of stage fifteen over the main set, `probe-r45-cyc.py` on `probe-r45-prior1.txt`, where the same reader reads 0.9996 on `probe-r44-prior1.txt`, and `--pair libunord-stage13-sum libunord-stage15-sum` reads 0.9980 raw on `run44-gheadnospec-main.json`; the four sweeps' raw cycles run from 0.9738 to 1.0525, no prior, so the time band runs from none of the saving reaching the clock to all of it. `predict: countdiff libunord-stage13-sum libunord-stage15-sum under -100 on main,compose,bcast,bcastmid basis`, read with `--counts` over each population's own sweep, which run-list step 20 takes, and `predict: pair libunord-stage13-sum libunord-stage15-sum 0.991 within 0.8% on main basis`. A difference at or over -100 on any shape or view says the sort did not save there; a pair over 0.999, that the instructions saved bought no time, and one under 0.983, that the time moved by more than the instructions.

**Read by --predictions, item (4):** `countdiff libunord-stage13-sum libunord-stage15-sum under -100 on main,compose,bcast,bcastmid basis`: HELD on bcast basis, A - B up to -126 over 6 view(s), under -100; HELD on bcastmid basis, A - B up to -272 over 4 view(s), under -100; HELD on compose basis, A - B up to -173 over 6 view(s), under -100; HELD on main basis, A - B up to -115 over 19 view(s), under -100 --- `pair libunord-stage13-sum libunord-stage15-sum 0.991 within 0.8% on main basis`: HELD on main basis, read 0.9879 over 19 shape(s), 0.31 point(s) off, within 0.80%.

(5) *The arms no commit reaches keep the regime's worth: `list` and `bq-expand` read inside the spread this pair's builds drew, on the instructions Run 44's halves counted.* `--counts-over probe-r45-prior1.txt run44-counts-gheadnospec.txt` reads both families at 1.0000 on the basis, and `./read-run.py run44-gheadnospec-main.json --compare run44-gheadtwopass-main.json --counts run44-counts-gheadnospec.txt run44-counts-gheadtwopass.txt` reads Run 44's counted work across the halves at 1.2929 on `list` and 1.5063 on `bq-expand`; no probe was taken on the control, so the two count spans are this item's test that the source reached nothing the passes compile on those families. `./read-run.py --record regime` reads `list` over the nineteen shapes at 1.2889 to 1.3040 on every reading from Run 37's build to Run 44's, and `bq-expand` at 1.2980 to 1.3212 on every one from Run 36's but Run 41's 1.3620. `predict: counts list 1.2929 within 0.1% on main basis`, `predict: counts bq-expand 1.5063 within 0.1% on main basis`, `predict: cross list 1.2965 within 1% on main basis` and `predict: cross bq-expand 1.3096 within 1.3% on main basis`. A count span outside its band says the source reached the control's code on that family; a cross outside its band with the counts held, that this build's placement or the box moved the regime's worth.

**Read by --predictions, item (5):** `counts list 1.2929 within 0.1% on main basis`: HELD on main basis, read 1.2929 over 19 shape(s), 0.00 point(s) off, within 0.10% --- `counts bq-expand 1.5063 within 0.1% on main basis`: HELD on main basis, read 1.5063 over 19 shape(s), 0.00 point(s) off, within 0.10% --- `cross list 1.2965 within 1% on main basis`: HELD on main basis, read 1.2929 over 19 shape(s), 0.36 point(s) off, within 1.00% --- `cross bq-expand 1.3096 within 1.3% on main basis`: HELD on main basis, read 1.3048 over 19 shape(s), 0.48 point(s) off, within 1.30%.

**Three of the five items hold by their kill conditions, item (2) is KILLED and item (3) is KILLED on one of its four readings: ten spans and sixteen readings, two killed --- the count-down level loop took back what Run 44's bounded loop cost `lib-stage2-lean`, `sortAxes`'s saving reached the clock, the passes' worth held on the instructions Run 44 counted, and master's `lib-stage0` runs further behind `lib-stage1` in time than any cycle sweep put it.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set, `small`, `compose`, `bcast` and `bcastmid` on the halves each span names and by `--pair` with `--counts` for the instructions.

(1) *The count-down level loop gives `lib-stage2-lean` back what Run 44's bounded loop cost it: level with `lib-stage3-lean` or ahead of it on the cell where that cost was found, and on the main set back toward Run 43's reading.* **HELD on both spans.** The premise held as the prior read it: against Run 44's counts `lib-stage2-lean` retires 1.0081 of the instructions on the basis, 1.0227 on `stretch-wide-2xM`, while `lib-stage3-lean` reads 0.9999, so the count-down costs instructions and was registered for time alone. `lib-stage3-lean` over `lib-stage2-lean` reads **1.0053** on `stretch-wide-2xM`, inside 4% of 1.02 and between the 0.98 and 1.06 the condition names, and **1.0013** over the main set, inside 1.5% of 1.00 and between 0.985 and 1.015, at 9 of 19 shapes and sign p 1 --- half a point from Run 43's 1.0066, where Run 44 read 0.9709. On the control the pair reads 1.0000. Against Run 44's same half `lib-stage2-lean` is 3.11 points faster on the basis and 2.31 on the control.

(2) *`lib-stage0`, master's `toVectorT`, runs regime 3 at about twenty-eight times `lib-stage1`'s fill, every main-set shape being regime 3 and the two arms parting in regime 3 alone.* **KILLED.** `lib-stage0` over `lib-stage1` reads **35.0472** over the nineteen shapes, corrected, `lib-stage1` the faster on all nineteen, 7.25 over 27.8 against a band of 2.5 --- so by the condition's own reading the list route's time does not follow its cycles as the fill's does. The instructions read 29.2547 times `lib-stage1`'s, corrected, on the basis, so in time the route runs about a fifth past its counted work as well. Two sweeps the owner granted on the quiet box after the run say where the time did not go and where the instrument stops: clean, at `N=50`, user cycles read 28.79 by `probe-r45-cyc.py` and user and kernel cycles 19.64 by a scratch computation, no reader taking `cycles:k`, kernel time running the OTHER way, `lib-stage1` carrying the larger share; under `SATURATE=1`, the state every timed process here benchmarks in, 69 of the 76 cells read NONLINEAR and `sum-only`'s own cycles, summed over both arms, 1.19 times the clean sweep's, three of the nineteen shapes negative, so that sweep reads nothing (`probe-r45-item2k.txt`, `probe-r45-item2sat.txt`). The candidate is the preamble's state, which slows `list`-shaped allocation and leaves a fill that allocates only its result where it was; [the open list][open] carries what would settle it. Published, `lib-stage0` reads with `list`, at 1.0035 and 0.9915 of it paired on the two halves, and moves with it across them, 1.3085 against 1.2929.

(3) *`lib-stage2-disp` is `lib-stage2-lean`'s code below a canonical run of 32768, which no main-set shape and no `small` view reaches, so the two read as an A/A there on both halves.* **HELD on the main set on both halves and on `small`'s control, KILLED on `small`'s basis.** `lib-stage2-disp` over `lib-stage2-lean` reads **1.0021** on the basis and **1.0017** on the control over the main set, inside the 0.85% and 0.72% floors, and **0.9992** on `small`'s control, inside 0.52%, and **0.9873** on `small`'s basis, 5 of 5 shapes, past its 0.36% floor. The condition names two causes for a reading past the floor, the dispatch's own test costing time or a run reaching the cut, and the reading refutes both: the dispatch arm is the FASTER, and it retires 1.0004 of the lean fill's corrected instructions on `small` on the basis and 1.0006 on the control, so no extra work runs and no view reaches the slice route. What is left is the basis binary's placement of two copies of one loop, a term no instruction count sees, on one half of one population.

(4) *`sortAxes` saves `libunord-stage13-sum` instructions against `libunord-stage15-sum` on every view the sweeps read, and some of that saving reaches the clock on the main set.* **HELD on both spans.** Read off this run's own sweeps, stage thirteen retires at least 115 instructions a call fewer than stage fifteen on every main-set shape and at least 126, 173 and 272 on every view of `bcast`, `compose` and `bcastmid`, all under the -100 the countdiff names, and 0.9855 of stage fifteen's raw instructions over the main set, as the prior read; in time it reads **0.9879** of stage fifteen over the main set, raw, inside 0.8% of 0.991 and between the 0.999 that would say the saving bought no time and the 0.983 that would say it bought more than the instructions --- some 83% of the saving reaching the clock. Against Run 44's same half the arm reads 1.22 points faster on the basis and 1.23 on the control, raw. On the control the two passes make it allocate 1.1845 of the basis's bytes, which [the open list][open] carries.

(5) *The arms no commit reaches keep the regime's worth: `list` and `bq-expand` read inside the spread this pair's builds drew, on the instructions Run 44's halves counted.* **HELD on all four spans.** The two count spans read **1.2929** on `list` and **1.5063** on `bq-expand`, Run 44's counted work across the halves to the fourth decimal, so the source reached nothing the passes compile on either family. `list`'s cross reads **1.2929**, 0.36 of a point off 1.2965, inside its 1% band and inside the 1.2889 to 1.3040 the builds from Run 37's to Run 44's drew, and `bq-expand` reads **1.3048**, 0.48 of a point off 1.3096, inside its 1.3% band and the 1.2980 to 1.3212 every draw but Run 41's kept. Without the intruded `cnn-slice-c32` the two read 1.2941 and 1.2997, inside their bands too.
