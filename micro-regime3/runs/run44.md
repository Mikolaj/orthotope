# Run 44 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source and a patched compiler, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach. The words it uses and the bars it reads against --- a point, the sign of a ratio, a strategy, a family, the plateau, and which bar answers what --- are defined once in [README's *Reading a run file*](../README.md#reading-a-run-file).

**Run 44 (GHC HEAD's in-tree stage1 against itself, patched under its unchanged version `10.1.20260918`, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source, launched from disk): the two passes are worth some thirty points on `list` and on `bq-expand`, and the branch's conversion code made `lib-stage2-lean` SLOWER by two and a half to three points on fewer instructions.** The pair is Runs 36's to 43's IN ITS VARIABLE --- one source, `Main.hs` at `c100112`, one shim at `1a359bd` under five switches with the exit span and the settled cost, ONE compiler, the patched stage1, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the sixteen main-set arms that carry a cross-half figure, SIX move with the families and TEN do not: the six are the `list` and `bq-expand` families entire, at **1.3040** to **1.3080**, and the ten others span **0.9903** to **1.0081**. **The bar an arm has to clear to be the passes' rather than the run's is 0.40 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.48% on the basis and 0.41% on the control and measured WITHIN one half --- and four of the eight arms that are not A/A copies clear it: the two families, `lib-stage3-lean` at 0.9903, the basis the faster, and `lib-stage2-lean-u1` at 1.0048, the control the faster.

**What this run was built to settle is what the three commits and the patched compiler did to each fill, and twelve of its fourteen spans hold while item (1) is KILLED on both halves: the instructions `b7d0ee1` saves bought no time.** `lib-stage3-lean` over `lib-stage2-lean` reads **0.9709** on the basis and **0.9840** on the control against the 1.017 the saved instructions predicted, `liblist-stage4-sum` over its sister **1.0118** and **1.0003** against 0.990, and a cycles reading of the two runs' basis binaries puts the cost in the loop the branch's code compiles to, 6.7% more cycles on 2.2% fewer instructions on `stretch-wide-2xM`, with the fill no commit reached level. The rest hold: `libunord-stage13-sum` reads with stage fifteen on the two grown `compose` views, **0.9985** and **1.0005** on the basis, the route `b7d0ee1` gave it placing the zero-stride axis where stage fifteen does; `lib-stage2-lean-u1` over `lib-stage3-lean` reads **1.0767** and **1.0611**, and the shipped leaf over `mut-odo-vecdims` **0.6366** and **0.6358**; and the patch left the control's counted work on `list` and `bq-expand` at Run 43's to the fourth decimal, the regime's worth reading `list` at **1.3040**, at the edge of its 1% band and over every draw since Run 37's build, and `bq-expand` at **1.3070** ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)).

**No process met foreign CPU, and the copy test the owner granted after the counts places every half-local mover.** Five arm-populations move past 3% on one half against Run 43's same half: the copy test reads three as PROCESS, among them the control's `bq-expand-aa-distant` on `bcastmid`, Run 43's 26% transient cell gone, and two as BUILD, the basis's `mut-odo-vecdims` on `small`, Run 43's binary 4.7% faster in fresh processes, and the control's `lib-stage1` on `rev`, where Run 43's binary reads 1.8% SLOWER, the other way from the evening's 3.6% ([Results](#results)). The same sitting took Run 43's owed copy test, and the control's `lib-stage1` on `small` that Run 43 left unexplained reads PROCESS. The machine check read `list` inside the bars and no reboot sits between this run and Run 43; one A/A cell, `runs-65536` on the control at 12.71%, carries the `bq-expand` transient's signature ([Provenance](#provenance)).


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE and the COMPILER together**: `Main.hs` moved from `e29cdf2` to `c100112` in three of the owner's commits, which brought no arm in and took none out and gave three arms the conversion code of the `pr-mikolaj-toVectorListT` branch, and the in-tree stage1 was patched under its unchanged version, `10.1.20260918` ([Provenance](#provenance)); the project file `cabal.project.ghead`, the shim `align-as.py` at `1a359bd` with its five switches, the regime and the launch from disk are Run 43's. **Read against the half Run 43 built by this same recipe, the two timed arms the branch's code reached moved the WRONG way on both halves**: `lib-stage2-lean` reads 2.81 points slower on the basis and 2.49 on the control, and the reducing consumer `liblist-stage4-sum` 1.28 and 1.03, on fewer instructions; every other arm with a corrected time moved by at most 1.08 points on the basis and 0.45 on the control, which [What the next run compares against](#what-the-next-run-compares-against) gives arm by arm. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run44-gheadnospec`, as every published table here is from Run 13 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **NONE of the thirty-one rows is a first reading**: every one is Run 43's, in Run 43's order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every row has a twin in Run 43's file.

**Comparing runs?** The table below is Run 44's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.48%** from 1 on the basis half or **0.41%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one agree on the basis and part by a hundredth of a point on the control**: over the four pairs that carry back to Run 10 the two halves read **0.48%** and **0.40%**, `bq-expand-aa-distant` carrying both, where the basis's whole-set figure is the same pair's and the control's is `mut-odo-vecdims-add-in-leaf-u2-aa-distant`'s. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **2.88%** on `alexnet-L1-55-c3-k11` on the basis and **3.53%** on `stretch-wide-2xM` on the control --- are not floors at all and are not to be quoted as any. This run's two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.61* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.63 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage15-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage fourteen's route with the zero-stride axis consed just outside the run |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.41* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.023 | 0.111 | 0.60 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.111 | 0.55 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage1 | 0.024 | 0.111 | 0.51 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| lib-stage2-lean-u1 | 0.025 | 0.109 | 0.60 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.111* | *0.52* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.111 | 0.46 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` was a port of until 2026-09-11 |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.110* | *0.58* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.110* | *0.47* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.045* | *0.110* | *0.41* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.110 | 0.37 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.128 | 0.256 | 0.67 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.128* | *0.255* | *0.70* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.128* | *0.257* | *0.38* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.64 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.010* | *0.60* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.003* | *1.009* | *0.46* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run SEVEN of the 105 pairs among the timed arms other than `list` part in SIGN between the two statistics on the basis and SEVEN on the control, `--winsor` printing each. **The cap moves seven rows on the basis**, `lib-stage1` with 5 of 19 cells capped, `lib-stage2-lean` with 2 of 19, `lib-stage2-lean-u1` with 3 of 19, `lib-stage3-lean` with 4 of 19, and `mut-odo-vecdims-add-in-leaf-u2` and its two A/A copies with 4 of 19 each, their published figures sitting 5.9 to 14.1 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms; it touches one cell of `list-aa-distant` besides, to no effect at three decimals. **The widest disagreement of any kind on the basis** is `bq-expand-aa-adjacent` over `lib-stage1`, which divides to **5.2125** on the column where the paired figure is **4.4751**, the column +16.5% off it. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads 14 of the 16 rows moved against Run 43's table, where what says how far an ARM moved is `--compare` against the JSON of the half Run 43 built.

**This run's two columns may be differenced on NONE of the eleven populations, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **30.40 points** on the main set and by 25.61 on `bcastmid` to 36.18 on `bcast` over the ten classes, every one of the figures past the bar by a factor of 36 or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's.

`concat-runs` has no row, and neither do the other 82 arms the roster holds and checks without timing --- **83 of its 114** in all: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). `roster-delta.py`, read off the two binaries, reads 31 arms to 31 over 19 shapes to 19 and the class views 62 to 62, every arm, main-set shape and class view in Run 43's order and every geometry unmoved. A movement against Run 43's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a source term and a compiler term between the two runs and no shim, boot or launch term, nor a project-file term --- and a movement across THIS run's two halves is the pair's own variable and the two processes', with no build, source or box term.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage3-lean` alone at 0.023**, with `lib-stage2-lean` and `lib-stage1` at 0.024, `lib-stage2-lean-u1` at 0.025 and the shipped leaf at 0.026 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result. **Paired on the basis, `lib-stage3-lean` leads `lib-stage2-lean` by three points where Run 43 read the two level**: `lib-stage3-lean` over `lib-stage2-lean` is **0.9709** at 16 of 19 and sign p 0.0044, widest on `stretch-wide-2xM` at 0.845, which is registration item (1) KILLED, the branch's conversion code having made `lib-stage2-lean` slower and not faster; and `lib-stage3-lean` leads the shipped leaf at **0.8844**, 15 of 19, and `lib-stage1` at **0.8819**, 18 of 19, where `lib-stage2-lean` reads 0.9110 and 0.9083 against the same two --- so both lean fills still lead `lib-stage1` and the shipped leaf, `lib-stage3-lean` by some twelve points and `lib-stage2-lean` by about nine, where Run 43 had both at eleven to twelve. **The third, read across the halves, is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6366** on the basis and **0.6358** on the control, 0.08 of a point apart on a pair that moves `list` by thirty points, both within the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33, the control's at its foot --- a span carried from that file and not re-derived here.

**The three commits moved instructions only in the three arms `b7d0ee1` gave the branch's code, and the patch moved none; the clock moved the wrong way on two of the three.** Against Run 43's basis, the same recipe on `e29cdf2` and the unpatched compiler, every timed arm but those three reads 1.0000 of Run 43's instructions an iteration on both halves, and `lib-stage2-lean`, `liblist-stage4-sum` and `libunord-stage13-sum` read 0.9928, 0.9908 and 0.9969 on the basis and 0.9925, 0.9904 and 0.9976 on the control. The clock moves by at most 1.08 points on every arm with a corrected time but `lib-stage2-lean`, from **0.9892** on `bq-expand-aa-distant` to **1.0108** on `list-aa-adjacent` on the basis and from **0.9955** on the shipped leaf to **1.0041** on `lib-stage3-lean` on the control; `lib-stage2-lean` reads **1.0281** and **1.0249**, and the consumer `liblist-stage4-sum` **1.0128** and **1.0103**, both slower on fewer instructions, which is registration item (1) KILLED. **The `bq-expand` family reads a point faster on the basis than Run 43's published column, and that column was Run 43's second process**: its first process read the family 1.5 to 1.7 points faster than its rerun, so this run's basis lands between Run 43's two processes of one binary, and a cross-run figure on the family under two points still reads the process as much as the build.

**The half-local movers against Run 43 are five, each on one half, and the copy test places all five.** `--half-movers run44 run43` flags five arm-populations past 3% on ONE half, none on the main set: the control's `bq-expand-aa-distant` on `bcastmid` 5.4% FASTER, widest on `bcastmid-c32-cnn` at 0.80, which is Run 43's 26% transient cell gone; the basis's `lib-stage2-lean-u1` on `block` 3.1% slower, widest on `block-run64-off7` at 1.07; the control's `lib-stage2-lean` on `flip` 3.1% slower on counts of 0.9963, widest on `flip-last-rows` at 1.14; the control's `lib-stage1` on `rev` 3.6% slower, widest on `rev-gather48-src-50` at 1.07; and the basis's `mut-odo-vecdims` on `small` 3.6% slower, widest on `small-patch-k5` at 1.06 --- every one but the `flip` cell on counts level to 1e-4. **The copy test, taken on the owner's quiet box after the counts** (`probe-copy-test-run44.log`), reads the first three PROCESS, a fresh copy and Run 43's binary reading with the timed file in fresh processes, and the last two BUILD: on `small-patch-k5/mut-odo-vecdims` Run 43's basis reads 0.953 of the timed file, the same direction as the evening's move, so that is this build's term; on `rev-gather48-src-50/lib-stage1` Run 43's control reads 1.018, the OTHER direction, so the build accounts for none of the evening's 3.6%. **The same sitting took Run 43's owed copy test** (`probe-copy-test-run43.log`): the control's `lib-stage1` on `small-bcast32`, which Run 43 left unexplained, reads PROCESS, and the other cell it carried, `flip-last-rows/mut-odo-vecdims-aa-distant`, reads INSTANCE, Run 43's control file itself some 9% faster than a fresh copy of it. **Step 4b's cells read as Run 43's did**: ranked by time over counts, nineteen of the twenty widest cells of the 2511 are `bq-expand-nosum`, whose counts the two passes move by 37 to 40% on cells where its clock moves by at most 6.2 points, and the twentieth is the transient cell on `runs-65536`; the count-led cells are led by `bq-expand-nosum`'s and the `bq-expand` family's, whose counts the passes move by up to 132% and 108%.


## What the next run compares against

**Run 44's pair is Run 43's rebuilt on the changed source and a patched compiler, [registered before it ran](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of 2026-10-03, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; [the standing rulings from past runs](../README.md#standing-rulings-from-past-runs) are NOT that site either.** What this run leaves as the reference is `run44-gheadnospec`, the unflagged half whose column stands below: the in-tree stage1 reporting `10.1.20260918` as patched on 2026-10-03, through `cabal.project.ghead`, `Main.hs` at `c100112`, the shim at `1a359bd` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **Its step from `run43-gheadnospec`**: 15 of the 16 timed arms both runs carry read within 1.1 points of 1 by `--compare`, paired per shape, and one does not --- `lib-stage2-lean` at **1.0281**, 0.992..1.158, widest on `stretch-wide-2xM` at 1.158, below 1 meaning this run is the faster; `--bridge` puts no arm outside the 3.3% drift band it prints. **The step is the source and the compiler together, and the counts part them where they can**: every arm `b7d0ee1` did not reach retires Run 43's instructions on both halves, so the patch moved none of theirs, and the three it reached moved by under a point in instructions and, on `lib-stage2-lean`, the wrong way in time ([Results](#results)). **The pair itself is Runs 36's to 43's, built again**, and its draws are `./read-run.py --record regime`'s, a row per build. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER was not this pair's variable --- both halves are one in-tree stage1 --- but it moved under both since Run 43, patched under its unchanged version, so the step from Run 43 carries a compiler term beside the source.** **What this run adds is another build of the pair, the first on the patched compiler**: Runs 36 to 44 are the same two recipes, Runs 39's to 44's with the settled cost on both, and their cross-half readings on `list` agreed to 0.94 points over the seven builds after Run 36's, 1.2889 to 1.2983, where this run reads **1.3040**, 0.57 of a point over the highest of them; `bq-expand` reads **1.3070**, inside the 1.2980 to 1.3212 every build but Run 41's 1.3620 kept. The control's counted work on both families is Run 43's to the fourth decimal, so the patch did not reach what the two passes compile, and `list`'s draw is this build's placement or process. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim, the source and now the compiler together. Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s build rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and on the eighteen shapes left without Run 36's wild cell, where Run 36 read above the level, the seven HEAD draws from Run 37's to Run 43's straddle it, and this run's `list` reads 1.3049 over those eighteen shapes, above it.

**What Run 44 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 43 and this run, and the gate says the box still measures as it did, the machine check reading `list`'s net inside the bars against the fingerprint Run 43 installed ([Provenance](#provenance) gives the figures). **This reading carries a source term and a compiler term**: Run 43's basis is this basis's recipe on `e29cdf2` and the unpatched compiler, and `list` runs no code the three commits changed and retires the instructions it did on Run 43, so `list` holding inside the bars says the rebuild left it there. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 44's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **Twelve of the fourteen spans held on every population and half their scope names, and item (1)'s two were KILLED**, the priors behind items (1) to (3) being instruction counts, cycles and bytes off this run's own basis binary, taken before preflight on a quiet box. **What a next registration should take from this one is that on code a commit rewrote, the prior's cycles outrank its instructions**: item (1) read the instructions the branch's code saves as time, while the two prior sweeps' own cycles put `lib-stage3-lean` at 0.932 and 0.935 of `lib-stage2-lean` on `stretch-wide-2xM`, agreeing, which is the direction the run then read.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 44**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918` as patched on 2026-10-03, on `Main.hs` at `c100112` with the shim at `1a359bd`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 43 published a HEAD half on this basis's recipe, so the two published columns carry no shim term, only the source and the compiler's patch. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9892** on `bq-expand-aa-distant` to **1.0281** on `lib-stage2-lean`, below 1 meaning this run is the faster, as the first paragraph of this section breaks down. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 44 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918 patched) | Run 44 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.032 |
| `lib-stage1` | **0.024** | 0.032 |
| `lib-stage2-lean` | **0.024** | 0.032 |
| `lib-stage2-lean-u1` | **0.025** | 0.033 |
| `lib-stage3-lean` | **0.023** | 0.031 |
| `bq-expand` | **0.128** | 0.127 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on six of the seven rows, the control higher on each of those six, while `bq-expand` prints 0.128 and 0.127, the one arm whose own move outpaces the denominator's; in absolute terms the flagged half is the faster on fourteen of the sixteen timed arms, `--compare` putting the other two, `lib-stage3-lean` and `lib-stage1`, at 0.9903 and 0.9995, and four of the eight arms that are not A/A copies clear the 0.40-point bar that comparison prints: `list` and `bq-expand`, the two families the passes reach, `lib-stage3-lean` on the basis's side by 0.97 of a point, and `lib-stage2-lean-u1` on the control's by 0.48, where on Run 43 five arms cleared a 0.28-point bar. **Read DOWN a column and the head is `lib-stage3-lean`**, at 0.023 on the basis and 0.031 on the control, with `lib-stage2-lean` and `lib-stage1` level at 0.024 on the basis and level with the shipped leaf at 0.032 on the control; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, every published table but the two-column one being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over the main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6358** (0.6366); `lib-stage1` against `mut-odo-vecdims-add-in-leaf-u2` **1.0074** (1.0029); `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2` **0.9113** (0.9110); `lib-stage2-lean` against `lib-stage1` **0.9046** (0.9083); `lib-stage3-lean` against `lib-stage2-lean` **0.9840** (0.9709); `lib-stage2-lean-u1` against `lib-stage3-lean` **1.0611** (1.0767); `bq-expand` against `mut-odo-vecdims` **2.1917** (2.8567). **All seven hold their direction across the halves** by the paired figure: four move under half a point, the two that read `lib-stage3-lean` move by 1.31 and 1.56 points, and the headline pair, `bq-expand` against `mut-odo-vecdims`, by 66.5 points, the pair's own variable. **`lib-stage2-lean` leads the shipped leaf by about nine points on both halves**, where Runs 41 to 43 read about twelve, and `lib-stage3-lean` leads `lib-stage2-lean` on both, at sign p 0.0044 on the basis and 0.36 on the control.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.35 us | 0.079 | `lib-stage3-lean` 0.043 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.7 us | 0.090 | `lib-stage3-lean` 0.040 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 119 us | 0.063 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 390 us | 0.043 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 461 us | 0.048 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.11 ms | 0.030 | `lib-stage3-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.73 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.49 ms | 0.024 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17.1 ms | 0.040 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 20 ms | 0.052 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 20.1 ms | 0.031 | `lib-stage2-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.9 ms | 0.023 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.9 ms | 0.110 | `lib-stage2-lean-u1` 0.109 | `mut-odo-vecdims` 0.110 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.9 ms | 0.022 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 31.6 ms | 0.084 | `lib-stage2-lean` 0.071 | `mut-odo-vecdims-add-in-leaf-u2` 0.075 |
| `stretch-bigstride` | 3 | 1800000 | 51.2 ms | 0.032 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.9 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41.1 ms | 0.021 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.8 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 945 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.1 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.7 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.1 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.5 ms | 0.016 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.4 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.64 ms | 0.053 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.27 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.8 ms | 0.034 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42 ms | 0.022 | `lib-stage2-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.25 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.28 ms | 0.024 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.28 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-page` | `block` | 64 | 131072 | 2.36 ms | 0.029 | `lib-stage3-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.5 ms | 0.020 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 946 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 946 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-bcast-nest` | `compose` | 6 | 1800000 | 33.4 ms | 0.036 | `lib-stage1` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |
| `compose-bcast-wide` | `compose` | 120 | 1800000 | 48.6 ms | 0.012 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.010 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.4 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.9 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.37 ms | 0.026 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.053 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.4 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 33.2 ms | 0.046 | `lib-stage1` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.037 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 120 us | 0.064 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 460 us | 0.048 | `lib-stage3-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.53 ms | 0.024 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.4 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.7 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 29 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 29.1 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 29.2 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-256` | `runs` | 256 | 1799936 | 29.3 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-7` | `runs` | 7 | 1799994 | 32.9 ms | 0.033 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 40.2 ms | 0.057 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 30 ms | 0.025 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.6 ms | 0.040 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.9 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.6 ms | 0.038 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.8 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 32.4 ms | 0.030 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-96` | `runs` | 96 | 1800000 | 29.6 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.8 ms | 0.025 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 268 us | 0.029 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.14 ms | 0.028 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.96 us | 0.080 | `lib-stage3-lean` 0.040 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.45 us | 0.051 | `lib-stage3-lean` 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `small-flat64` | `small` | 64 | 256 | 4.45 us | 0.060 | `lib-stage2-lean` 0.006 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.35 us | 0.089 | `lib-stage2-lean-u1` 0.049 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.55 us | 0.042 | `lib-stage2-lean` 0.033 | `mut-odo-vecdims-add-in-leaf-u2` 0.040 |
| `window-28x28-k5` | `window` | 5 | 14400 | 279 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 951 us | 0.085 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.44 ms | 0.053 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.72 ms | 0.051 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.84 ms | 0.051 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.7 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage3-lean` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 43 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the ELEVEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FIFTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside vecdims` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names four different `lib-` arms --- `lib-stage2-lean` and `lib-stage3-lean` on FOUR rows each, `lib-stage2-lean-u1` and `lib-stage1` on one each, where Run 43 gave `lib-stage2-lean` five rows and `lib-stage3-lean` four, five of its rows now naming another arm. The cross-class summary's `best outside vecdims` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 44's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in every population it reads, as on Runs 36 to 43 and at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9898**, where the control reads **0.9798** on the same shape. Every other shape of every population reads the clause with room, the classes' closest cells at 0.30 to 0.51 on the basis. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw by more than its 0.48% floor, and the lowest basis draw of Runs 36 to 44, 0.03 of a point under Run 43's. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half and the patched compiler included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, the WIDER statement this class set is read for --- that no arm the library would ship is slower than `list` on any shape: **two timed non-control cells of 1134 are slower than their own shape's `list`**, both `lib-stage1` on `runs-2`, the stage-one route as it shipped, whose fill since `c7549d2` is `fillStage3` behind a `walkAx` conversion and so no longer the library's own --- the two cells Runs 41 to 43 read: `lib-stage1` on `runs-2` on the control at **1.3367**; `lib-stage1` on `runs-2` on the basis at **1.0738**. **It is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0079 between the halves while `list` moves 1.2547.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits at or under 0.05268. The `bq-expand` clause is closest at `small-row96` at 1.00441 on the control, then `scaled-rank1-m1` at 1.00003 on both halves, then `stretch-tall-Mx2` at 1.00000 on both halves of the main set and `bcast-src8` at 1.00000 on the control. **Those figures are Runs 36's to 43's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, no commit having rewritten code behind `bq-expand` or `list`, and the compiler's patch moving none of it. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in the ten classes, on both halves --- and their LEVEL clause BREAKS in every one of the eleven populations, the ten classes and the main set.** `bq-expand` sits between 1.00x and 3.86x the result vector and `list` at 19.00x to 27.66x, on both halves and in every class. On the main set `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the main-set shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 43's to the fourth decimal.

**AND THE ONE ARM OUTSIDE THE TWO FAMILIES THAT MOVED ON RUNS 42 AND 43 NO LONGER DOES: `libunord-stage13-sum`, which `b7d0ee1` put on the branch's `unorderedRouteT`.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.9991** of the basis on `libunord-stage13-sum`, where Runs 42 and 43 read 0.9687 and 0.9686; every arm outside the `bq-expand` and `list` families reads 0.9991 to 1.0009, `libunord-stage14-sum` the highest, and the fills and ordered consumers 1.0000 to 1.0002. `--alloc` puts 382 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 44 (GHC HEAD's in-tree stage1 against itself, patched under its unchanged version `10.1.20260918`, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 25.61 points on `bcastmid` at narrowest and 36.18 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 43, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **160 arm-comparisons, 36 putting the basis faster and 124 slower**, with no degenerate arm excluded, at geomeans from **1.0709** on `flip` to **1.1353** on `window` and extremes of `lib-stage1` at **0.9761** on `small` and `bq-expand-aa-adjacent` at **1.5282** on `window`. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **One registration names a class**: item (2)'s three cell spans are `on compose` and are read in [this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), every other span being `on main`.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **The bold is the arm outside the vecdims arms on NINE of the TEN rows this run** --- `lib-stage2-lean` on `block`, `compose`, `flip`, `small`, `lib-stage3-lean` on `bcast`, `bcastmid`, `window`, `lib-stage2-lean-u1` on `runs`, `lib-stage1` on `scaled`; the ceiling on `rev`. **The vecdims arms' ceiling is `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Runs 39 to 43, and the one row whose bold sits in the CEILING column is `rev`, where the leaf and `lib-stage3-lean` both print 0.021 and the unrounded values put the leaf ahead. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside vecdims | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.064 | `lib-stage3-lean` 0.021 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.021 | 0.22% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.62% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage3-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.51% |
| `window` | 8 | 0.051 | 0.085 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 1.31% |
| `scaled` | 3 | 0.027 | 0.029 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 0.28% |
| `runs` | 16 | 0.026 | 0.057 | **`lib-stage2-lean-u1`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.20% |
| `flip` | 6 | 0.028 | 0.053 | **`lib-stage2-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 1.03% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage2-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.18% |
| `small` | 5 | 0.062 | 0.089 | **`lib-stage2-lean`** 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.052 | 0.77% |
| `compose` | 6 | 0.023 | 0.036 | **`lib-stage2-lean`** 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 | 0.60% |

The best arm outside the vecdims arms is ahead of `mut-odo-vecdims` in ten of the ten classes. Five row(s) change the arm they name against Run 43, `bcastmid` to `lib-stage3-lean`, `compose` to `lib-stage2-lean`, `rev` to `lib-stage3-lean`, `runs` to `lib-stage2-lean-u1`, `small` to `lib-stage2-lean`. **TWO rows tie at three decimals this run**, `compose`, `rev`, and `bcast`, `block`, `runs`, `scaled` sit a thousandth apart; the `bold` column decides each on the unrounded values.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *126* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.10 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.11 | 148 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.02 | 157 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.03 | 157 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 157 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.05 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.06 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *158* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.041* | *0.06* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.041 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.041* | *0.07* | *147* | *1.00x* |
| lib-stage3-lean | 0.021 | 0.026 | 0.09 | 148 | 1.00x |
| lib-stage2-lean | 0.021 | 0.026 | 0.10 | 148 | 1.00x |
| lib-stage1 | 0.022 | 0.041 | 0.14 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.10 | 147 | 1.00x |
| *mut-odo-vecdims-aa* | *0.042* | *0.063* | *0.09* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.064 | 0.09 | 138 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.14* | *138* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.138* | *0.236* | *0.12* | *122* | *3.22x* |
| *bq-expand-aa-distant* | *0.138* | *0.236* | *0.09* | *122* | *3.22x* |
| bq-expand | 0.138 | 0.236 | 0.12 | 122 | 3.22x |
| *list-aa-distant* | *0.999* | *1.000* | *0.30* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 85 | 26.11x |
| *list-aa-adjacent* | *1.002* | *1.003* | *0.22* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 1.0022, worst cell 0.71% on `rev-gather48-src-50`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0003 on a worst cell of 0.05% on `rev-cnn-L1-24x24-c1`, its interval missing 1. The in-situ term reads 1.0002, 1.0172 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0015, which the correction amplifies by 1.71x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m7s, peak 96 MiB in use, 25 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.68 ms per call raw, 4.53 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.048/0.024

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.1011, from `lib-stage3-lean` at 0.9809 to `bq-expand` at 1.3142, with `list` itself at 1.2830. **The baseline moved 28.30% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.064, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.021, priced against `mut-odo-vecdims` at 0.4994 over 3 of 3 shapes at sign p 0.25, a margin of 50.06% against this class's 0.22% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 28.30 of a point, at a class geomean of 1.1011 over the 16 arms, with 4 of 8 strategies past an A/A bar of 1.05 points. The counted work reads a counts geomean of 1.1656 over the same arms, 16 of them counted. Its counted work parts by 16.56 points where its clock parts by 10.11, so about 0.61 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.59* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.28* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.015 | 0.020 | 0.50 | 62 | 1.00x |
| lib-stage2-lean | 0.015 | 0.020 | 0.44 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.49* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.47 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.40 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.44* | *62* | *1.00x* |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.51 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.36* | *61* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.33* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.20 | 61 | 1.00x |
| *bq-expand-aa-adjacent* | *0.092* | *0.142* | *0.70* | *46* | *1.00x* |
| bq-expand | 0.092 | 0.142 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.093* | *0.144* | *0.07* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.14 | 17 | 20.99x |
| *list-aa-distant* | *1.003* | *1.012* | *0.99* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.006* | *1.015* | *0.88* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 0.9938, worst cell 1.71% on `bcast-src512`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.11% on `bcast-inner900`, its interval covering 1. The in-situ term reads 1.0210, 1.0115 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9977, which the correction amplifies by 2.40x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m13s, peak 180 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.8 ms per call raw, 29.7 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.016/0.019/0.019

**Across the halves:** 10 of the 16 arms are faster on this half and 6 slower, at a geomean of 1.0816, from `lib-stage2-lean` at 0.9847 to `list` at 1.3618, with `list` itself at 1.3618. **The baseline moved 36.18% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.015, priced against `mut-odo-vecdims` at 0.6503 over 6 of 6 shapes at sign p 0.031, a margin of 34.97% against this class's 0.62% floor (`mut-odo-vecdims-aa`). Its two columns may NOT be differenced, `list` having moved 36.18 of a point, at a class geomean of 1.0816 over the 16 arms, with 6 of 8 strategies past an A/A bar of 0.76 points. The counted work reads a counts geomean of 1.1697 over the same arms, 16 of them counted. Its counted work parts by 16.97 points where its clock parts by 8.16, so about 0.48 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.31 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.34 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.34 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.30 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 97 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.27* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *88* | *0.00x* |
| lib-stage3-lean | 0.012 | 0.019 | 0.32 | 82 | 1.00x |
| lib-stage2-lean | 0.012 | 0.018 | 0.35 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.021 | 0.34 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.019 | 0.33 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.35* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.27* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.29 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.31* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.31 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.29* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.100* | *0.183* | *0.43* | *61* | *1.92x* |
| bq-expand | 0.100 | 0.184 | 0.41 | 60 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.183* | *0.28* | *61* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 0.72 | 28 | 23.56x |
| *list-aa-adjacent* | *1.000* | *1.005* | *0.74* | *28* | *23.56x* |
| *list-aa-distant* | *1.001* | *1.005* | *0.92* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9949, worst cell 0.72% on `bcastmid-primes`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.03% on `bcastmid-primes`, its interval covering 1. The in-situ term reads 1.0177, 1.1313 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9978, which the correction amplifies by 2.38x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m50s, peak 135 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.9 ms per call raw, 47.8 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0917, from `mut-odo-vecdims` at 0.9944 to `bq-expand-aa-distant` at 1.2598, with `list` itself at 1.2561. **The baseline moved 25.61% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.012, priced against `mut-odo-vecdims` at 0.4183 over 4 of 4 shapes at sign p 0.12, a margin of 58.17% against this class's 0.51% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 25.61 of a point, at a class geomean of 1.0917 over the 16 arms, with 6 of 8 strategies past an A/A bar of 0.81 points. The counted work reads a counts geomean of 1.1711 over the same arms, 16 of them counted. Its counted work parts by 17.11 points where its clock parts by 9.17, so about 0.54 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.36* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.29 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.16 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.18 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.26 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.06 | 105 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.07 | 105 | 0.02x |
| libunord-stage15-sum | -- | -- | 0.05 | 105 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.24 | 100 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.09 | 102 | 0.02x |
| libunord-stage7-sum | -- | -- | 0.06 | 104 | 0.02x |
| libunord-stage9-sum | -- | -- | 0.09 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.027 | 0.20 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.16 | 83 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage2-lean | 0.024 | 0.028 | 0.17 | 84 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.19 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.18* | *82* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.17* | *82* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.085* | *0.18* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.051* | *0.086* | *0.19* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.085 | 0.19 | 76 | 1.00x |
| bq-expand | 0.176 | 0.216 | 0.34 | 57 | 3.86x |
| *bq-expand-aa-distant* | *0.177* | *0.216* | *0.28* | *57* | *3.86x* |
| *bq-expand-aa-adjacent* | *0.177* | *0.217* | *0.33* | *57* | *3.86x* |
| list (baseline) | 1.000 | 1.000 | 0.56 | 30 | 27.66x |
| *list-aa-adjacent* | *1.001* | *1.003* | *0.43* | *30* | *27.66x* |
| *list-aa-distant* | *1.003* | *1.054* | *0.53* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0131, worst cell 5.45% on `window-128x128-k7`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.05% on `window-32x32-c64-k3`, its interval covering 1. The in-situ term reads 1.0059, 1.1612 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0128, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m31s, peak 127 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.085/0.031/0.053/0.051/0.053/0.052

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.1353, from `mut-odo-vecdims-aa-distant` at 0.9910 to `bq-expand-aa-adjacent` at 1.5282, with `list` itself at 1.2870. **The baseline moved 28.70% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.085, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.4146 over 8 of 8 shapes at sign p 0.0078, a margin of 58.54% against this class's 1.31% floor (`list-aa-distant`). Its two columns may NOT be differenced, `list` having moved 28.70 of a point, at a class geomean of 1.1353 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.28 points. The counted work reads a counts geomean of 1.1776 over the same arms, 16 of them counted. Its counted work parts by 17.76 points where its clock parts by 13.53, so about 0.76 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.12 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.21 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.20 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.15 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.17 | 128 | 1.00x |
| libunord-stage15-sum | -- | -- | 0.16 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.21 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.16 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.12 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.16 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *138* | *0.00x* |
| lib-stage1 | 0.022 | 0.031 | 0.11 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.031* | *0.19* | *128* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.031* | *0.16* | *127* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.031 | 0.15 | 127 | 1.00x |
| lib-stage3-lean | 0.023 | 0.031 | 0.12 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.031 | 0.18 | 128 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.030 | 0.21 | 128 | 1.00x |
| *mut-odo-vecdims-aa* | *0.027* | *0.029* | *0.11* | *127* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.029* | *0.08* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.029 | 0.09 | 127 | 1.00x |
| bq-expand | 0.092 | 0.102 | 0.06 | 111 | 1.21x |
| *bq-expand-aa-distant* | *0.092* | *0.102* | *0.07* | *111* | *1.21x* |
| *bq-expand-aa-adjacent* | *0.092* | *0.102* | *0.10* | *111* | *1.21x* |
| list (baseline) | 1.000 | 1.000 | 0.18 | 69 | 21.49x |
| *list-aa-distant* | *1.003* | *1.004* | *0.27* | *69* | *21.49x* |
| *list-aa-adjacent* | *1.003* | *1.005* | *0.18* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9972, worst cell 1.13% on `scaled-super-r3`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.03% on `scaled-r5`, its interval covering 1. The in-situ term reads 1.0160, 1.0176 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9990, which the correction amplifies by 2.43x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m10s, peak 110 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.32 ms per call raw, 5.14 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 1 of the 16 arms are faster on this half and 15 slower, at a geomean of 1.0721, from `lib-stage1` at 0.9992 to `list` at 1.3191, with `list` itself at 1.3191. **The baseline moved 31.91% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.8995 over 2 of 3 shapes at sign p 1, a margin of 10.05% against this class's 0.28% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.91 of a point, at a class geomean of 1.0721 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.36 points. The counted work reads a counts geomean of 1.1524 over the same arms, 16 of them counted. Its counted work parts by 15.24 points where its clock parts by 7.21, so about 0.47 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen, and cut to sixteen for Run 41, `runs-3` (`sInner` 3, a k3 conv row) leaving timing in `94aeee7` and staying in `check`.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.44* | *52* | *1.07x* |
| liblist-stage1-sum | -- | -- | 0.12 | 62 | 0.35x |
| liblist-stage4-sum | -- | -- | 0.02 | 75 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.11 | 62 | 0.35x |
| libunord-stage13-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.03 | 75 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 74 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 75 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.03 | 75 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 75 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage2-lean-u1 | 0.023 | 0.024 | 0.14 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.026 | 0.14 | 60 | 1.00x |
| lib-stage3-lean | 0.023 | 0.025 | 0.14 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.52* | *59* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.025* | *0.12* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.025 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.025* | *0.057* | *0.11* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.025* | *0.057* | *0.11* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.057 | 0.11 | 59 | 1.00x |
| lib-stage1 | 0.084 | 1.074 | 0.22 | 52 | 1.35x |
| *bq-expand-aa-adjacent* | *0.092* | *0.140* | *0.47* | *46* | *1.07x* |
| bq-expand | 0.092 | 0.140 | 0.42 | 46 | 1.07x |
| *bq-expand-aa-distant* | *0.093* | *0.143* | *0.04* | *46* | *1.07x* |
| list (baseline) | 1.000 | 1.000 | 2.44 | 17 | 21.26x |
| *list-aa-distant* | *1.030* | *1.047* | *0.32* | *17* | *21.26x* |
| *list-aa-adjacent* | *1.032* | *1.047* | *0.27* | *17* | *21.26x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0320, worst cell 4.71% on `runs-65536`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.20% on `runs-9`, its interval covering 1. The in-situ term reads 1.0308, 1.0259 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0309, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h43m7s, peak 596 MiB in use, 270 MiB max residency; the reader reads 31 benchmarks over 16 shapes of the runs class. Anchor: `runs-2`, `list` at 41.3 ms per call raw, 40.2 ms net.

**Per shape, in the run's shape order (runs-2, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.040/0.038/0.033/0.030/0.025/0.025/0.025/0.024/0.024/0.024/0.024/0.024/0.024/0.024/0.025

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.0803, from `mut-odo-vecdims-aa-distant` at 1.0003 to `list-aa-adjacent` at 1.3246, with `list` itself at 1.3205. **The baseline moved 32.05% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.07x, 21.26x --- and `lib-stage2-lean-u1` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.8061 over 16 of 16 shapes at sign p 3.1e-05, a margin of 19.39% against this class's 3.20% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 32.05 of a point, at a class geomean of 1.0803 over the 16 arms, with 2 of 8 strategies past an A/A bar of 0.73 points. The counted work reads a counts geomean of 1.1598 over the same arms, 16 of them counted. Its counted work parts by 15.98 points where its clock parts by 8.03, so about 0.50 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.17 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.12 | 92 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.13 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.50 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.03 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.022 | 0.041 | 0.23 | 84 | 1.00x |
| lib-stage3-lean | 0.022 | 0.041 | 0.33 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.045 | 0.28 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.037* | *0.36* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.037* | *0.12* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.037 | 0.14 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.053* | *0.10* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.053* | *0.09* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.053 | 0.10 | 77 | 1.00x |
| lib-stage1 | 0.032 | 0.047 | 0.37 | 82 | 1.00x |
| *bq-expand-aa-adjacent* | *0.091* | *0.184* | *0.44* | *60* | *1.05x* |
| bq-expand | 0.091 | 0.184 | 0.43 | 60 | 1.05x |
| *bq-expand-aa-distant* | *0.093* | *0.183* | *0.13* | *60* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.69 | 32 | 21.18x |
| *list-aa-distant* | *1.006* | *1.022* | *0.61* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.009* | *1.028* | *0.42* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0103, worst cell 3.92% on `flip-last-rows`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.20% on `flip-outer-gap64`, its interval covering 1. The in-situ term reads 1.0212, 1.0252 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0075, which the correction amplifies by 1.34x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31 ms per call raw, 30 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.053/0.046/0.026/0.026

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0709, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9783 to `list-aa-adjacent` at 1.3311, with `list` itself at 1.3152. **The baseline moved 31.52% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.7300 over 6 of 6 shapes at sign p 0.031, a margin of 27.00% against this class's 1.03% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.52 of a point, at a class geomean of 1.0709 over the 16 arms, with 3 of 8 strategies past an A/A bar of 1.21 points. The counted work reads a counts geomean of 1.1522 over the same arms, 16 of them counted. Its counted work parts by 15.22 points where its clock parts by 7.09, so about 0.47 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.13 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.03 | 129 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| lib-stage2-lean | 0.020 | 0.024 | 0.15 | 111 | 1.00x |
| lib-stage3-lean | 0.020 | 0.024 | 0.11 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.021 | 0.026 | 0.15 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.16* | *111* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.11* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.11 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.030* | *0.08* | *110* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.10 | 110 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.030* | *0.11* | *111* | *1.00x* |
| lib-stage1 | 0.048 | 0.057 | 0.17 | 104 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.13* | *96* | *1.06x* |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.08* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.087 | 0.13 | 96 | 1.06x |
| *list-aa-adjacent* | *0.999* | *1.002* | *0.19* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.32 | 54 | 21.22x |
| *list-aa-distant* | *1.000* | *1.002* | *0.29* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `bq-expand-aa-adjacent` at 0.9982, worst cell 0.33% on `block-run64-gap1`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0004 on a worst cell of 0.11% on `block-run64-page`, its interval covering 1. The in-situ term reads 1.0213, 1.0229 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9987, which the correction amplifies by 1.40x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m26s, peak 136 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.66 ms per call raw, 4.5 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.029/0.024/0.020

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.0764, from `lib-stage1` at 1.0017 to `list-aa-distant` at 1.3418, with `list` itself at 1.3330. **The baseline moved 33.30% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.020, priced against `mut-odo-vecdims` at 0.8629 over 5 of 5 shapes at sign p 0.062, a margin of 13.71% against this class's 0.18% floor (`bq-expand-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 33.30 of a point, at a class geomean of 1.0764 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.66 points. The counted work reads a counts geomean of 1.1489 over the same arms, 16 of them counted. Its counted work parts by 14.89 points where its clock parts by 7.64, so about 0.51 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.18 | 228 | 1.69x |
| liblist-stage4-sum | -- | -- | 0.07 | 243 | 1.16x |
| liblist-stage5-sum | -- | -- | 0.08 | 243 | 1.17x |
| libunord-stage1-sum | -- | -- | 0.23 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.11 | 244 | 0.19x |
| libunord-stage14-sum | -- | -- | 0.15 | 244 | 0.20x |
| libunord-stage15-sum | -- | -- | 0.10 | 244 | 0.20x |
| libunord-stage6-loop-sum | -- | -- | 0.18 | 239 | 0.55x |
| libunord-stage6-sum | -- | -- | 0.22 | 239 | 0.55x |
| libunord-stage7-sum | -- | -- | 0.22 | 239 | 0.55x |
| libunord-stage9-sum | -- | -- | 0.25 | 238 | 0.43x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.46* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.07* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.03* | *250* | *0.01x* |
| lib-stage2-lean | 0.034 | 0.051 | 0.20 | 235 | 1.13x |
| lib-stage3-lean | 0.034 | 0.050 | 0.35 | 235 | 1.13x |
| lib-stage2-lean-u1 | 0.035 | 0.049 | 0.19 | 234 | 1.13x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.052 | 0.068 | 0.23 | 229 | 1.28x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.052* | *0.068* | *0.26* | *229* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.068* | *0.22* | *229* | *1.28x* |
| *mut-odo-vecdims-aa* | *0.062* | *0.089* | *0.21* | *229* | *1.27x* |
| *mut-odo-vecdims-aa-distant* | *0.062* | *0.088* | *0.18* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.062** | 0.089 | 0.17 | 229 | 1.27x |
| lib-stage1 | 0.083 | 0.105 | 0.22 | 221 | 2.36x |
| *bq-expand-aa-adjacent* | *0.136* | *0.197* | *0.18* | *217* | *1.44x* |
| bq-expand | 0.136 | 0.198 | 0.12 | 217 | 1.44x |
| *bq-expand-aa-distant* | *0.137* | *0.198* | *0.16* | *217* | *1.44x* |
| *list-aa-adjacent* | *0.999* | *1.001* | *0.12* | *179* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.18 | 180 | 21.57x |
| *list-aa-distant* | *1.000* | *1.002* | *0.15* | *179* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0077, worst cell 3.82% on `small-bcast32`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0008 on a worst cell of 0.43% on `small-bcast32`, its interval covering 1. The in-situ term reads 0.9945, 1.0022 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0043, which the correction amplifies by 1.61x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m32s, peak 132 MiB in use, 52 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.77 us per call raw, 6.55 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.042/0.080/0.051/0.060/0.089

**Across the halves:** 1 of the 16 arms are faster on this half and 15 slower, at a geomean of 1.0905, from `lib-stage1` at 0.9761 to `list-aa-distant` at 1.2828, with `list` itself at 1.2734. **The baseline moved 27.34% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.089, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.034, priced against `mut-odo-vecdims` at 0.4370 over 5 of 5 shapes at sign p 0.062, a margin of 56.30% against this class's 0.77% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 27.34 of a point, at a class geomean of 1.0905 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.91 points. The counted work reads a counts geomean of 1.1448 over the same arms, 16 of them counted. Its counted work parts by 14.48 points where its clock parts by 9.05, so about 0.63 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500), and the two views that landed 2026-09-26, for Run 42, and grew from 4992 elements to `sizeCap` on 2026-09-27 (`aa18c24`), for this run --- `compose-bcast-nest` (`l` 1800000, `sInner` 6) and `compose-bcast-wide` (`l` 1800000, `sInner` 120). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero; the two grown ones put a broadcast beside short runs under a reversed nest --- of extent 6 beside runs of 10 under three strided axes nothing merges on `compose-bcast-nest`, of extent 120 beside runs of 6 under five strided axes of extent 4 or 5 on `compose-bcast-wide` --- so that where the unordered stages place the zero-stride axis decides which extent the odometer turns over on.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.61* | *52* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.46 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 82 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.05 | 80 | 0.01x |
| libunord-stage15-sum | -- | -- | 0.05 | 82 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.05 | 80 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage2-lean | 0.014 | 0.018 | 0.43 | 62 | 1.00x |
| lib-stage3-lean | 0.014 | 0.018 | 0.52 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.018* | *0.42* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.014 | 0.018 | 0.41 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.014* | *0.019* | *0.49* | *62* | *1.00x* |
| lib-stage1 | 0.014 | 0.018 | 0.42 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.48 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.036* | *0.35* | *61* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.023* | *0.036* | *0.30* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.036 | 0.17 | 61 | 1.00x |
| *bq-expand-aa-adjacent* | *0.093* | *0.121* | *0.71* | *46* | *1.35x* |
| bq-expand | 0.093 | 0.122 | 0.65 | 46 | 1.35x |
| *bq-expand-aa-distant* | *0.093* | *0.123* | *0.24* | *46* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 1.18 | 17 | 22.01x |
| *list-aa-distant* | *1.000* | *1.007* | *1.02* | *17* | *22.01x* |
| *list-aa-adjacent* | *1.002* | *1.008* | *0.89* | *17* | *22.01x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9940, worst cell 2.10% on `compose-bcast-wide`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.30% on `compose-bcast-nest`, its interval covering 1. The in-situ term reads 1.0200, 1.0243 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9982, which the correction amplifies by 3.23x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m15s, peak 142 MiB in use, 41 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 31 ms per call raw, 29.9 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar, compose-bcast-nest, compose-bcast-wide):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019/0.036/0.012

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0793, from `lib-stage2-lean-u1` at 0.9993 to `list` at 1.3138, with `list` itself at 1.3138. **The baseline moved 31.38% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.036, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.014, priced against `mut-odo-vecdims` at 0.6240 over 6 of 6 shapes at sign p 0.031, a margin of 37.60% against this class's 0.60% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.38 of a point, at a class geomean of 1.0793 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.31 points. The counted work reads a counts geomean of 1.1606 over the same arms, 16 of them counted. Its counted work parts by 16.06 points where its clock parts by 7.93, so about 0.49 of the instruction saving reaches the clock.


## Provenance

**Run 44's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `c100112`; one shim, `align-as.py` at `1a359bd`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 reporting `10.1.20260918` and reached through `cabal.project.ghead`; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run44-gheadnospec` and is what every table here publishes; `run44-gheadtwopass` is the candidate. **What is new against Run 43 is not the pair but two inputs under both halves.** `Main.hs` moved three of the owner's commits, `e29cdf2` to `c100112`; and the compiler was patched under its unchanged version, its `--version` and the strings the binaries carry reading as Run 43's: the stage1 at the recipe's path was written 2026-10-03 19:11, md5 `39db416de5ed25e1b272d801bfa405d7`, over the GHC checkout at `6913545fd3` with `GHC.Core.Opt.Simplify.Iteration`, `GHC.Core.Opt.Specialise`, `GHC.Core.Utils` and `GHC.Core.Map.Expr` modified in its working tree and its libraries rebuilt the same day, while the dependency store was not rebuilt, every ABI hash `run44-gheadnospec` carries being `run43-gheadnospec`'s. The shim, the recipes, `cabal.project.ghead`, `micro.cabal` and the launch are Run 43's to the character, and no reboot sits between the two runs, `uptime -s` reading 2026-09-24 00:00:31, before Run 43's build.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 62 class views over ten classes for 1922 more, and it is Run 43's to the name and to the geometry: nothing in, nothing out and nothing grown.** `./roster-delta.py run43-gheadnospec run44-gheadnospec`, read off the two binaries, reads every arm, main-set shape and class view in Run 43's order, every class at its count and the geometry of every shape and view the two carry unmoved, so pre-run step 12's condition did not fire and no -L1 roster pass was owed or taken.

**The evening ran in ONE window and in the order the run list gives, and no bench met foreign CPU, so no population was rerun.** `run-evening.sh` took the gate from 02:16:27 to 02:49:48, the alarm at 02:49:51 reading 0.2% busy, the sequence from 2026-10-04T02:49:51 to 2026-10-04T10:06:18 and the riders from 10:06:18 to 10:18:46, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones --- and each launched from `./run44-<half>`. The counted work, which wants no quiet machine, ran from 10:19 to 11:00, with the `-g3` twins building and this write-up's first readings running beside it. `--wild` finds no bench at or above 0.25 of a core foreign in any of the 22 sequence logs, so post-run step 3 owed no rerun and every figure in this file is the evening's. **The owner then granted the quiet box once, from 11:02:51 to 11:09:06**, for three readings the results called for and no table here reads: the cycles sweeps behind [the registration](#what-this-run-was-built-to-answer-and-what-it-answered)'s item (1), and the copy tests of this run's half-local movers and of Run 43's owed one ([Results](#results)).

**The gate read SOUND and the machine check did not fire.** The two palindrome passes read `list` 1.3036 and 1.2978, `mut-odo-vecdims` 1.0037 and 1.0016, `bq-expand` 1.3057 and 1.3077 --- 0.58, 0.21 and 0.20 points apart. Between its own two legs `gheadnospec` moved by at most 0.38 points, on `list`, and `gheadtwopass` by at most 0.10 points, on `mut-odo-vecdims`, so what the passes part by is the basis's legs and not a disagreement about the pair; `mut-odo-vecdims`, the arm the two passes leave alone, sits above 1 on both passes, by 0.37 and 0.16 of a point (`./read-run.py --gate-draft run44` prints all four readings). The machine check, which reads the gate's first basis process and so neither main-set process, against the fingerprint Run 43 installed --- this run's basis recipe on the source before the three commits and on the compiler before its patch --- puts `list`'s net at **+1.26%**, worst `stretch-primes` at **+2.21%**, none of 19 shapes past 5% and the geomean inside the 3% bar, so the source's and the compiler's terms together moved the box's `list` by under the bars.

**Every one of the twenty-two processes gated clean and the plateau refused by declaration, and four A/A worst cells pass the 5% `read-all.sh` reports at, one of them past 10%.** `read-all.sh` gates each process on its own correction and passes 22 of 22. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.9595 to 21.4302 ms/iter across the run, a 26.36% spread against a 5% band, and it splits exactly by half, `gheadnospec`'s 11 processes flat within 1.47% at 21.1190 to 21.4302 and `gheadtwopass`'s within 1.87% at 16.9595 to 17.2760 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-runs` at **12.71%** on `runs-65536`, `bq-expand-aa-adjacent` against `bq-expand`; `gheadtwopass-window` at **7.25%** on `window-128x128-k7`, `mut-odo-vecdims-aa-distant` against `mut-odo-vecdims`; `gheadtwopass-compose` at **5.61%** on `compose-zero-mid` and `gheadnospec-window` at **5.45%** on `window-128x128-k7`, both `list-aa-distant` against `list`; and `--wild` finds no foreign CPU on any of them. **Only the first passes the about 10% [the floor section][floor] gates on**, so that cell leaves the per-shape record and its row is flagged; `runs`'s control floor is set by another pair, `list-aa-distant` at **3.01%** beside the basis's 3.20%, and no span reads that class. **It is the recurring `bq-expand` transient's signature**: on the mutator clock `bq-expand-aa-adjacent` runs 1.080 times `bq-expand` there, 3871401 against 3585110 an iteration, on allocation equal to within 1e-4, which is the shape [the open list's entry][open] records. The main set's floor is 0.48% on the basis and 0.41% on the control.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run44-gheadnospec`, md5 `26a54dfb373a01b2f247933d78f88064`, and `run44-gheadtwopass`, md5 `d64815a893db85a0d89d0d5074efcbc2`, built on 2026-10-03 from `Main.hs` at `c100112`, clean against it, and run from a tree at `13461c4`, the commit that registered this run, which touches no `Main.hs`. Their `.text` sections are **20133695** and **20170559** bytes, the first column of `size -A`; against Run 43's two the basis is smaller by 12288 bytes and the flagged half by 20480, three and five pages exactly --- the three commits and the compiler's patch together, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source and the compiler having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 36864 bytes, nine pages exactly, and it carries MORE self-loops, 328 against 304, so [the open list's entry on it](../README.md#what-is-open) gains a run on that side.

**The three commits and the patch kept the basis's six-copy group at offset 0 and moved both its two-copy groups.** `./loop-offsets.py --delta run43-gheadnospec run44-gheadnospec`, the same basis recipe on the two sources and the two compilers, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0], with no address surviving to the byte and its four displacements whole lines; moves the first two-copy group from [0, 3] to [0, 0], one of its two displacements not a whole line; and leaves one copy of the second, at 11 of [11, 14]. **Within the pair** the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves and the remaining two-copy group [0, 0] on both, and a three-copy group at [0, 0, 0] exists on the control half alone, as on Runs 41 to 43. `--library` puts **4.4%** of the 804 library self-loops the two halves share at the same offset in line, where Run 43 read 4.3% of 806: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 29 on each half, where Run 43 read 32 and 24, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 304 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 328 on the control, 209 and 144 of them at offset 0, where Run 43 read 296 and 303 self-loops, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. These are the survey as repaired before pre-run step 11: its first reading counted a phantom loop on the control, 329 self-loops and one exit span astride, decoding a continuation's bytes after an info table as a loop. **Post-run step 3a's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity twelve straddlers on the basis and fourteen on the control** --- on both, `sumNoSpec` three times, `fillStage3`'s body at offset 30, `fillStage2Short` twice, `fillStage2Axes`, two leaf bodies of `fbMutOdoVecdimsAddInLeafU2`, one each of `fbMutOdoVecdimsAddInLeafU2Down` and `-Last`, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the control `fillStage2OneLevel` and `fbFused` besides, Run 43's names with a third copy of `sumNoSpec`. Of the refusals, nine on the basis and seven on the control carry a `--loose` family of `fillStage3`, `fillStage2Short`, `fillStage2VSdims`, `fillStage2OneLevel` and `fillStage2Axes` bodies, which the bytes cannot choose between, and eight on each half are 60- to 63-byte bodies at offset 32, 40 or 48 for which no twin holds a copy. **Neither half's own `-g3` twin holds as many loops as the binary it names for**, 296 against the basis's 304 and 298 against the control's 328, as on Run 43, so every name above rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run44-gheadnospec`, 9.992 times apart, which is plain -O1; on `run44-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. Both builders' figures are Run 43's to the byte on both halves, the patched compiler included. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.35 us** on `cnn-slice-c32`, **3.73 ms** on `cnn-L2-24x24-c32`, **39.8 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 19.5 to 21.7 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.52 us | 6.35 us | 5.04 us |
| `cnn-L2-24x24-c32` | 165888 | 3.83 ms | 3.73 ms | 2.92 ms |
| `stretch-wide-2xM` | 1800000 | 40.9 ms | 39.8 ms | 32 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.68 ms raw and 4.53 ms net; `bcast-inner900` 30.8 ms raw and 29.7 ms net; `bcastmid-b200k` 48.9 ms raw and 47.8 ms net; `window-128x128-k7` 14.2 ms raw and 13.8 ms net; `scaled-rank1-m1` 5.32 ms raw and 5.14 ms net; `runs-2` 41.3 ms raw and 40.2 ms net; `flip-fwd-rows96` 31 ms raw and 30 ms net; `block-r3-vol64` 4.66 ms raw and 4.5 ms net; `small-row96` 6.77 us raw and 6.55 us net; `compose-zero-mid` 31 ms raw and 29.9 ms net. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and one cell of the whole run is one the reader flags.** The two `sum-only` arms agree on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9992 to 1.0014 across the twenty-two processes, at a mean absolute difference of at most 0.26% --- so the term subtracted from one half is the term subtracted from the other. **One cell sits below R2 0.99 ([what that column detects][ramp]) and none is under ten samples**, of the run's 5022 cells, 2511 on each half: `runs-65536/bq-expand-aa-adjacent` on the control, at R2 0.9798, the transient's cell above.

**The counted work covers every population, no cell was refused anywhere, and the two halves part in work as Run 43's did.** `run-counts-all.sh` wrote 22 sweep files over eleven populations, none refused, at a cost of 1365s on the basis and 1108s on the control by `--counts-totals` --- beside Run 43's 1339s and 1113s on the same roster, with this run's `-g3` twins building and its first readings running alongside, which an instruction count does not see. The counts geomean over the sixteen arms that carry a corrected time runs **1.1448** on `small` to **1.1776** on `window`, the main set at **1.1673**, Run 43's to the third decimal --- the basis retiring 14.5 to 17.8 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families**: the `bq-expand` trio sits at 0.8677 to 0.8684, retiring 50.63% more instructions on the basis for 30.70 to 30.80% more time; the `list` trio at 1.0086 to 1.0088, cashing a little more than all of what it saves; and the ten others between 0.9390 and 0.9676, retiring 3.83 to 5.49 percent more on the basis while their clocks run from 0.97 of a point below level to 0.81 above. **Read per class the same way, the rate runs 0.47 to 0.76**: the instruction saving reaching the clock is lowest on `flip`, where the counted work parts by 15.22 points and the clock by 7.09, and highest on `window`, 17.76 against 13.53 --- where Run 43 read 0.43 to 0.79, lowest then on `compose`.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **0.9998** on each half of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0296** and **1.1042** on the basis and **1.0269** and **1.0729** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and about ten and seven on `bq-expand`, the term that is subtracted being the `sum-only` one and not this proxy.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1153** on the basis and **1.1630** on the control, **4.8** points apart, where Run 43's two parted by 3.7 and Run 42's by 4.4 --- so the two passes change what the spray costs a process as well as what the roster costs it. What the roster adds on top of that state is **1.0240** on the basis, 10 of 19 shapes above 1, and **1.0031** on the control, 9 of 19; the basis's rest runs 0.9881 on `stretch-bigstride` to 1.2180 on `stretch-r5-8x432`, the control's 0.9700 on `stretch-bigstride` to 1.0888 on `stretch-tall-Mx2`. The whole in-process deflation is **1.1421** on the basis, 18 of 19 shapes above 1, and **1.1665** on the control, 19 of 19. **The roster cells and the legs are one evening's**, the legs taken straight after the sequence, so the decomposition spans no second window.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 43's, both recipes unchanged to the character and rebuilt on `Main.hs` at `c100112` where Run 43 built from `e29cdf2`, on the owner's word of 2026-10-03 that this run builds the previous run's recipes on the source at the tip: both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, `align-as.py` at `1a359bd` as for Run 43, under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run44-gheadnospec` and `run44-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 43's with the builddir names moved. **The compiler moved under the recipe**: on the owner's word of the same day it was patched without changing its version, its name or the way it operates, and the stage1 at the recipe's path was written 2026-10-03 19:11 over a GHC checkout carrying `GHC.Core.Opt.Simplify.Iteration`, `GHC.Core.Opt.Specialise`, `GHC.Core.Utils` and `GHC.Core.Map.Expr` modified, its `--version` and the strings the binaries carry unchanged; the dependency store was not rebuilt, every ABI hash `run44-gheadnospec` carries being `run43-gheadnospec`'s. So the pair's own `cross` figure is the two passes on a ninth build, now under the patched compiler, and each half against Run 43's same half, `--half-movers run44 run43`, carries the source and the compiler together; the shim, `cabal.project.ghead` and `micro.cabal` did not move. The three commits bring no arm in and take none out --- `./roster-delta.py run43-gheadnospec run44-gheadnospec` reads every arm, main-set shape and class view in the same order and every geometry unmoved --- and `./registration-drift.py run44 --since run43` reaches every `lib-`, `liblist-` and `libunord-` arm and no code behind the `list`, `mut-odo-vecdims` and `bq-expand` families or the two `sum-only` halves. What they change behind the arms the items read, off the commit messages: `fillStage2Axes`, `fillStage3` and `fillStage3U1` read a broadcast run's element as the branch's `genericFillStrided` does (`fdcd7a8`); `lib-stage2-lean`, `liblist-stage4-sum` and `libunord-stage13-sum` run the conversion code of `pr-mikolaj-toVectorListT` in place of the pair form, `routeList4` its `routeT`, `routeUnord13` its `unorderedRouteT` with the zero-stride axis now just outside the run, and `fillStage2Axes` its `genericFillStrided` (`b7d0ee1`); and `c100112` reaches no timed arm. **The items' priors are instruction counts, cycles and bytes off this run's own basis binary**, `run44-gheadnospec`, taken with `probe-stalls.sh` at `N=50`, Run 43's counts N, twice, on a quiet box before preflight: into `probe-r44-prior1.txt` and `probe-r44-prior2.txt` over every timed arm and the nineteen main-set shapes, and into their `-compose`, `-bcast` and `-bcastmid` siblings over the nine `lib-`, `liblist-` and `libunord-` arms the items read, the two sweeps' instructions agreeing arm by arm to 1.0000 on the main set by `--counts-over probe-r44-prior2.txt probe-r44-prior1.txt` and their cycles by a median of 1.6% a cell on the main set and 1.2% on `compose`, over the cells both sweeps count positive; and bytes a call over the nine arms in `probe-r44-alloc.txt` and `probe-r44-alloc-compose.txt`. A cycle figure is quoted only where the two sweeps agree on it. No probe was taken on the control's recipe, so the priors are the basis's. **The compiler moved no instruction the basis counts**: `./read-run.py --counts-over probe-r44-prior1.txt run43-counts-gheadnospec.txt` reads every timed arm at 1.0000 of Run 43's but the three `b7d0ee1` gave the branch's code, `lib-stage2-lean` at 0.9927, `liblist-stage4-sum` at 0.9914 and `libunord-stage13-sum` at 0.9969. **The limit this run cannot remove**: a rebuild moves every loop --- `./loop-offsets.py --delta run43-gheadnospec run44-gheadnospec` finds none of the loops it compares at its old address --- so a figure on unmoved instructions is predicted only within the spread earlier builds drew.

(1) *The branch's conversion code makes `lib-stage2-lean` and `liblist-stage4-sum` cheaper by the instructions it saves, and they gain on the Axis path's fastest by about that.* `--counts-over probe-r44-prior1.txt run43-counts-gheadnospec.txt` reads `lib-stage2-lean` at 0.9927 of Run 43's instructions, 0.9778 on `stretch-wide-2xM`, and `liblist-stage4-sum` at 0.9914; `--counts probe-r44-prior1.txt --pair` on `run43-gheadnospec-main.json` reads `lib-stage3-lean` over `lib-stage2-lean` at 1.0131 corrected and 1.0067 raw, where `--counts run43-counts-gheadnospec.txt --pair` reads 0.9990 and 0.9994, and `liblist-stage4-sum` over `liblist-stage5-sum` at 0.9923 raw over the seventeen shapes it reads there, where Run 43's counts read 1.0009 over all nineteen; `probe-r44-alloc.txt` puts `lib-stage2-lean` and `lib-stage3-lean` at the same bytes a call on every main-set shape. Run 43 read the two pairs in time at 1.0066 and 0.9978 on the basis and 1.0044 and 0.9984 on the control, `--pair` on `run43-gheadnospec-main.json` and `run43-gheadtwopass-main.json`, the `-sum` pair raw. `predict: pair lib-stage3-lean lib-stage2-lean 1.017 within 1.5% on main both` and `predict: pair liblist-stage4-sum liblist-stage5-sum 0.990 within 1.2% on main both`. A reading under 1.002 on the first or over 1.002 on the second says the instructions the branch's code saves bought no time; one past the band's far edge, that the time moved by more than the instructions.

**Read by --predictions, item (1):** `pair lib-stage3-lean lib-stage2-lean 1.017 within 1.5% on main both`: KILLED on main basis, read 0.9709 over 19 shape(s), 4.61 point(s) off, within 1.50%; KILLED on main control, read 0.9840 over 19 shape(s), 3.30 point(s) off, within 1.50% --- `pair liblist-stage4-sum liblist-stage5-sum 0.990 within 1.2% on main both`: KILLED on main basis, read 1.0118 over 19 shape(s), 2.18 point(s) off, within 1.20%; HELD on main control, read 1.0003 over 19 shape(s), 1.03 point(s) off, within 1.20%.

(2) *`libunord-stage13-sum` now takes `libunord-stage15-sum`'s placement of the zero-stride axis on the two compose views grown to `sizeCap`, so it reads with stage fifteen there and not with stage fourteen.* `--counts-over probe-r44-prior1-compose.txt run43-counts-gheadnospec-compose.txt` reads `libunord-stage13-sum` at 0.8030 of Run 43's instructions on `compose-bcast-wide` and 1.1129 on `compose-bcast-nest`, the ratios `probe-r43-prior1-compose.txt` read for stage fifteen over fourteen there, and level on the other four views; `probe-r44-prior1-compose.txt` puts stage thirteen at 15781014 instructions a call against stage fifteen's 15781178 on the first view and 14666451 against 14666476 on the second, and the two sweeps' cycles at 2816247 and 2803500 against 2814119 and 2803648 on the first and 2865378 and 2877959 against 2852852 and 2847558 on the second, so stage thirteen over fourteen reads 0.6884 and 0.6852 in cycles on `compose-bcast-wide`. Run 43 read stage fifteen over fourteen there at 0.6677 on the basis and 0.6608 on the control, `--pair libunord-stage15-sum libunord-stage14-sum --per-shape` on `run43-gheadnospec-compose.json` and `run43-gheadtwopass-compose.json`, raw. `predict: cell compose-bcast-wide/libunord-stage13-sum over compose-bcast-wide/libunord-stage15-sum 1.00 within 3% on compose both`, `predict: cell compose-bcast-nest/libunord-stage13-sum over compose-bcast-nest/libunord-stage15-sum 1.00 within 3% on compose both`, and `predict: cell compose-bcast-wide/libunord-stage13-sum over compose-bcast-wide/libunord-stage14-sum 0.67 within 6% on compose both`. A reading of either of the first two outside 3%, the instructions level, is placement; a third over 0.73 says the route's saving did not carry into time.

**Read by --predictions, item (2):** `cell compose-bcast-wide/libunord-stage13-sum over compose-bcast-wide/libunord-stage15-sum 1.00 within 3% on compose both`: HELD on compose basis, read 0.9985 over 1 shape(s), 0.15 point(s) off, within 3.00%; HELD on compose control, read 0.9999 over 1 shape(s), 0.01 point(s) off, within 3.00% --- `cell compose-bcast-nest/libunord-stage13-sum over compose-bcast-nest/libunord-stage15-sum 1.00 within 3% on compose both`: HELD on compose basis, read 1.0005 over 1 shape(s), 0.05 point(s) off, within 3.00%; HELD on compose control, read 0.9991 over 1 shape(s), 0.09 point(s) off, within 3.00% --- `cell compose-bcast-wide/libunord-stage13-sum over compose-bcast-wide/libunord-stage14-sum 0.67 within 6% on compose both`: HELD on compose basis, read 0.6533 over 1 shape(s), 1.67 point(s) off, within 6.00%; HELD on compose control, read 0.6723 over 1 shape(s), 0.23 point(s) off, within 6.00%.

(3) *The fills `fdcd7a8` rewrote and the arms no commit reaches keep Run 43's distances: the patch moves none of their instructions on the basis, and they hold on the control too.* `--counts-over probe-r44-prior1.txt run43-counts-gheadnospec.txt` reads every such arm at 1.0000 of Run 43's, `lib-stage3-lean`, `lib-stage2-lean-u1` and `lib-stage1` among them; `--counts probe-r44-prior1.txt --pair` on `run43-gheadnospec-main.json` reads `lib-stage2-lean-u1` over `lib-stage3-lean` at 1.0206 raw, `lib-stage1` over `mut-odo-vecdims-add-in-leaf-u2` at 0.9737, the leaf over `mut-odo-vecdims` at 0.7198 and `bq-expand` over `mut-odo-vecdims` at 1.8778, each within 0.0001 of what `run43-counts-gheadnospec.txt` reads the same way. Run 43 read the four in time at 1.0662, 0.9928, 0.6416 and 2.8893 on the basis and 1.0628, 1.0021, 0.6380 and 2.1860 on the control, `--pair` on the two main JSONs, its basis `bq-expand` figure the rerun's, 1.5% over its first process's 2.8453 by `runs/run43.md`'s Results. `predict: pair lib-stage2-lean-u1 lib-stage3-lean 1.065 within 2.5% on main both`, `predict: pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 0.998 within 2% on main both`, `predict: pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.640 within 2% on main both`, `predict: pair bq-expand mut-odo-vecdims 2.87 within 12% on main basis` and `predict: pair bq-expand mut-odo-vecdims 2.19 within 9% on main control`. A reading outside its band with the basis's instructions level is the rebuild's placement, or on the control the patch reaching what the two passes do, which item (4)'s count spans tell apart; `--half-movers run44 run43` names which arm of the pair moved.

**Read by --predictions, item (3):** `pair lib-stage2-lean-u1 lib-stage3-lean 1.065 within 2.5% on main both`: HELD on main basis, read 1.0767 over 19 shape(s), 1.17 point(s) off, within 2.50%; HELD on main control, read 1.0611 over 19 shape(s), 0.39 point(s) off, within 2.50% --- `pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 0.998 within 2% on main both`: HELD on main basis, read 1.0029 over 19 shape(s), 0.49 point(s) off, within 2.00%; HELD on main control, read 1.0074 over 19 shape(s), 0.94 point(s) off, within 2.00% --- `pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.640 within 2% on main both`: HELD on main basis, read 0.6366 over 19 shape(s), 0.34 point(s) off, within 2.00%; HELD on main control, read 0.6358 over 19 shape(s), 0.42 point(s) off, within 2.00% --- `pair bq-expand mut-odo-vecdims 2.87 within 12% on main basis`: HELD on main basis, read 2.8567 over 19 shape(s), 1.33 point(s) off, within 12.00% --- `pair bq-expand mut-odo-vecdims 2.19 within 9% on main control`: HELD on main control, read 2.1917 over 19 shape(s), 0.17 point(s) off, within 9.00%.

(4) *The regime's worth holds under the patched compiler: the two passes leave `list` and `bq-expand` the instructions Run 43's control counted, `list` at its level and `bq-expand` inside the spread its builds and processes drew but Run 41's.* `--counts-over probe-r44-prior1.txt run43-counts-gheadnospec.txt` reads both families at 1.0000 on the basis, and `./read-run.py run43-gheadnospec-main.json --compare run43-gheadtwopass-main.json --counts run43-counts-gheadnospec.txt run43-counts-gheadtwopass.txt` reads Run 43's counted work across the halves at 1.2929 on `list` and 1.5063 on `bq-expand`; no probe was taken on the control, so the two count spans are this item's test of whether the patch reached the control's code. `./read-run.py --record regime` reads `list` over the nineteen shapes at 1.2889 to 1.2986 on every reading from Run 37's build to Run 43's, Run 43's at 1.2950, and `bq-expand` at 1.2980 to 1.3212 on every one from Run 36's but Run 41's 1.3620, Run 43's first basis process having read 1.3105 against its rerun's 1.3212 by `runs/run43.md`'s Results. `predict: counts list 1.2929 within 0.1% on main basis`, `predict: counts bq-expand 1.5063 within 0.1% on main basis`, `predict: cross list 1.294 within 1% on main basis`, and `predict: cross bq-expand 1.31 within 2.5% on main basis`, the last band half a point wider than Run 43's for the process term Run 43 measured. A count span outside its band says the patch moved the control's code on that family; a `list` cross outside its band with the counts held says the regime's worth moved with this build; a `bq-expand` one above 1.335 says Run 41's draw was not alone.

**Read by --predictions, item (4):** `counts list 1.2929 within 0.1% on main basis`: HELD on main basis, read 1.2929 over 19 shape(s), 0.00 point(s) off, within 0.10% --- `counts bq-expand 1.5063 within 0.1% on main basis`: HELD on main basis, read 1.5063 over 19 shape(s), 0.00 point(s) off, within 0.10% --- `cross list 1.294 within 1% on main basis`: HELD on main basis, read 1.3040 over 19 shape(s), 1.00 point(s) off, within 1.00% --- `cross bq-expand 1.31 within 2.5% on main basis`: HELD on main basis, read 1.3070 over 19 shape(s), 0.30 point(s) off, within 2.50%.

**Three of the four items hold by their kill conditions and item (1) is KILLED: fourteen spans and twenty-two readings, three killed and all three item (1)'s --- the branch's conversion code saves the instructions it was registered on and buys no time with them, `lib-stage2-lean` reading SLOWER than `lib-stage3-lean` on both halves.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set and `compose` on each half and by `--pair` with `--counts` for the instructions.

(1) *The branch's conversion code makes `lib-stage2-lean` and `liblist-stage4-sum` cheaper by the instructions it saves, and they gain on the Axis path's fastest by about that.* **KILLED on both halves on its first span, and on the basis on its second.** The premise held: against Run 43's counts `lib-stage2-lean` retires 0.9928 of the instructions on the basis and 0.9925 on the control, 0.9778 and 0.9768 on `stretch-wide-2xM`, and `liblist-stage4-sum` 0.9908 and 0.9904, and the pairs' own counts read as the prior said, `lib-stage3-lean` over `lib-stage2-lean` at 1.0131 corrected on both halves and `liblist-stage4-sum` over `liblist-stage5-sum` at 0.9775. The time did not follow. `lib-stage3-lean` over `lib-stage2-lean` reads **0.9709** on the basis and **0.9840** on the control, under the 1.002 the kill condition names, so the instructions saved bought no time and `lib-stage2-lean` is now the slower of the two lean fills, widest on `stretch-wide-2xM` at 0.845 and 0.864; and `liblist-stage4-sum` over `liblist-stage5-sum` reads **1.0118** on the basis, over the 1.002 the condition names, and **1.0003** on the control, inside its band and under that line. Against Run 43's same half `lib-stage2-lean` is 2.81 points slower on the basis and 2.49 on the control. A cycles reading taken on the quiet box after the counts says where the time went: on the two runs' basis binaries `lib-stage2-lean` reads 1.0094 of Run 43's cycles over the seventeen shapes large enough to resolve, and 1.0669 on `stretch-wide-2xM`, on 0.9930 and 0.9778 of the instructions, while `lib-stage3-lean`, which no commit reached, reads 0.9914 of the cycles on level instructions --- so the rebuild did not slow the fill it left alone, and the loop the branch's code compiles to runs at a lower rate ([the open list][open]).

(2) *`libunord-stage13-sum` now takes `libunord-stage15-sum`'s placement of the zero-stride axis on the two compose views grown to `sizeCap`, so it reads with stage fifteen there and not with stage fourteen.* **HELD on both halves, on all three spans.** Stage thirteen over stage fifteen, on raw `slope` since a reducing consumer carries no corrected time, reads **0.9985** on the basis and **0.9999** on the control on `compose-bcast-wide` and **1.0005** and **0.9991** on `compose-bcast-nest`, inside 3% of 1.00; and stage thirteen over fourteen on `compose-bcast-wide` reads **0.6533** and **0.6723**, inside 6% of 0.67 and under the 0.73 that would say the route's saving did not carry into time. The instructions came out as the prior said: stage thirteen retires within 185 instructions a call of stage fifteen on both views on both halves, and 3.87 million fewer than stage fourteen on `compose-bcast-wide`, so `b7d0ee1`'s `unorderedRouteT` places the zero-stride axis where stage fifteen does.

(3) *The fills `fdcd7a8` rewrote and the arms no commit reaches keep Run 43's distances: the patch moves none of their instructions on the basis, and they hold on the control too.* **HELD on both halves, on all five spans.** The premise held on both halves: `--counts-over` puts every timed arm but the three `b7d0ee1` reached at 1.0000 of Run 43's instructions on the basis and on the control. `lib-stage2-lean-u1` over `lib-stage3-lean` reads **1.0767** on the basis and **1.0611** on the control, inside 2.5% of 1.065; `lib-stage1` over the shipped leaf **1.0029** and **1.0074**, inside 2% of 0.998; the leaf over `mut-odo-vecdims` **0.6366** and **0.6358**, inside 2% of 0.640; and `bq-expand` over `mut-odo-vecdims` **2.8567** on the basis, inside 12% of 2.87, and **2.1917** on the control, inside 9% of 2.19. The widest is `lib-stage2-lean-u1` over `lib-stage3-lean` on the basis, 1.17 points off its centre, and it is `lib-stage3-lean` that moved there, 0.83 of a point faster than Run 43's basis on level instructions.

(4) *The regime's worth holds under the patched compiler: the two passes leave `list` and `bq-expand` the instructions Run 43's control counted, `list` at its level and `bq-expand` inside the spread its builds and processes drew but Run 41's.* **HELD on all four spans.** The two count spans read **1.2929** on `list` and **1.5063** on `bq-expand`, Run 43's counted work across the halves to the fourth decimal, so the patch reached neither family's code on the control. `list`'s cross reads **1.3040**, 1.00 point off 1.294 and at the edge of its 1% band, and 0.57 of a point over the 1.2889 to 1.2983 the seven builds from Run 37's to Run 43's drew --- on level counts, so it is this build's placement or process and not the code; `bq-expand` reads **1.3070**, 0.30 of a point off 1.31, inside its band and inside the 1.2980 to 1.3212 every draw but Run 41's kept.
