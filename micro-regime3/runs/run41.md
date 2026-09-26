# Run 41 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source and shim, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 41 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source and shim, launched from disk): the two passes are worth some thirty points on `list` and thirty-six on `bq-expand`, FOUR of the five registered spans hold, and on the main set the fifteen source commits moved the fills they rewrote.** The pair is Runs 36's to 40's IN ITS VARIABLE --- one source, `Main.hs` at `688e952`, one shim at `1a359bd` under five switches with the exit span and the settled cost, ONE compiler, `10.1.20260918`, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the sixteen main-set arms that carry a cross-half figure, SIX move with the families and TEN do not: the six are the `list` and `bq-expand` families entire, at **1.2926** to **1.3629**, and the ten others span **0.9953** to **1.0053**, every one of them a fill. **The bar an arm has to clear to be the passes' rather than the run's is 0.71 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.33% on the basis and 0.63% on the control and measured WITHIN one half --- and two of the eight arms that are not A/A copies clear it, the two families; no fill does, where on Run 40 four of them cleared it by up to half a point.

**What this run was built to settle is whether the fill frozen as a copy of the nest carries the nest's time with it, and three of the four items hold whole while the fourth splits.** `lib-stage3-lean` over `lib-stage2-lean` reads **0.9904** on the basis and **0.9948** on the control, where Run 40 read 0.9656 and 0.9564, so one fill algorithm under both closed the lead; `lib-stage2-lean-u1` over `lib-stage2-lean` reads **1.0601** and **1.0638**, what the unroll cost against the nest on Run 40; and `lib-stage2-lean` over the shipped leaf **0.8911** and **0.8938**, where Run 40 read 0.9307 and 0.9322 --- the raw instruction ratios the priors took off this run's own basis binary coming out to the third decimal on all three. The regime's worth on the arms no commit touched reads `list` at 1.2926 against 1.295 within 1%, and `bq-expand` at **1.3620** against 1.303, killed ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)).

**The kill is ONE half's `bq-expand`, and the run itself was quiet but for two benches.** Against Run 40's basis the basis half runs the whole `bq-expand` family 3.9 to 4.3% slower on the main set and up to 10.2% on `window`, on instructions level to the fourth decimal and on code no commit changed, while the control's family reads within a quarter of a point of Run 40's control on the main set and past 3% on no population --- so what moved is where this build put `bq-expand` or the file it ran from, and the copy test taken after the evening says the build ([Results](#results)). The same move takes the opening's headline, `bq-expand` over `mut-odo-vecdims`, from 2.84x to 2.97x on the basis. No reboot sits between this run and Run 40, and the machine check read `list` inside the bars; two benches of the control's main set met foreign CPU, both reducing consumers no published figure reads, and on the owner's word they were not rerun.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE and the SHIM**: the compiler is Runs 36's to 40's in-tree stage1 `10.1.20260918` unmoved, and the project file `cabal.project.ghead`, the shim's five switches, the regime and the launch from disk are Run 40's. What moved is `Main.hs`, from `bb6b12e` to `688e952` in fifteen of the owner's commits, which retired one timed arm and one class view and moved none in, and `align-as.py`, from `fe6d133` to `1a359bd`, whose settled cost now plans again a group the pad had moved. **Read against the half Run 40 built by this same recipe, two rewritten fills moved and one untouched family did**, which [What the next run compares against](#what-the-next-run-compares-against) gives arm by arm. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run41-gheadnospec`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **NONE of the thirty rows is a first reading**: the roster is Run 40's less one retired arm, the other thirty in Run 40's order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every row has a twin in Run 40's file.

**Comparing runs?** The table below is Run 41's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.33%** from 1 on the basis half or **0.63%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one part on the basis and COINCIDE on the control this run**: over the four pairs that carry back to Run 10 the two halves read **0.25%** and **0.63%**, `mut-odo-vecdims-aa-distant` carrying the basis's carry-back figure where `mut-odo-vecdims-add-in-leaf-u2-aa-distant` carries its whole-set one, and `bq-expand-aa-distant` carrying both of the control's. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **2.30%** on `stretch-square-1341` on the basis and **6.82%** on `stretch-wide-2xM` on the control --- are not floors at all and are not to be quoted as any. Its two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.63* | *53* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.62 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.01 | 82 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.40* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.023 | 0.114 | 0.58 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.114 | 0.52 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-lean-u1 | 0.025 | 0.112 | 0.57 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| lib-stage1 | 0.025 | 0.114 | 0.47 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.113* | *0.58* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.114 | 0.42 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.113* | *0.50* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.41* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.40* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.113 | 0.39 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.134 | 0.279 | 0.57 | 49 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.134* | *0.278* | *0.54* | *49* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.134* | *0.278* | *0.34* | *49* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.73 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.007* | *0.65* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.002* | *1.009* | *0.46* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run NONE of the 105 pairs among the fifteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 40's basis parted on five of its 120. **The cap still moves the fills' rows**: seven rows have two to four of their nineteen cells capped, the four `lib-` fills and the shipped leaf with its two copies, and the published figures sit 7.3 to 11.9 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms. **The widest disagreement of any kind sits on the row the cap moved furthest**: `lib-stage1` over `list-aa-adjacent` divides to **0.0249** on the column where the paired figure is **0.0283**, the column 11.9% under it, `lib-stage1`'s published figure sitting 11.9 points under its plain geomean. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads thirteen of the sixteen rows moved against Run 40's table, `lib-stage1` by 4.0 points slower, where `--compare` against the JSON of the half Run 40 built puts that arm at 0.9894, faster, and `list` at 0.9965.

**This run's two columns may be differenced on NONE of the eleven populations, as Runs 36's to 40's could not, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **29.26 points** on the main set and by 27.52 on `bcastmid` to 39.12 on `bcast` over the ten classes, every one of the eleven figures past the bar by a factor of thirty-nine or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's. **That is the bar working rather than failing**: it exists to stop a margin being read off two columns with different denominators, and a pair built to move the denominator is the case it was written to refuse.

`concat-runs` has no row, and neither do the other 82 arms the roster holds and checks without timing --- **83 of its 113** in all, one more than on Run 40: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **One arm left the timed roster and none joined it**, `0cd790c` retiring `lib-stage3-lean-onelevel` to `check`: `roster-delta.py`, read off the two binaries, reads 31 arms to 30 over 19 shapes to 19, the other thirty in the same order, and the class views 61 to 60, `runs-3` out. A movement against Run 40's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a source term and a shim term between the two runs and no compiler, boot, project-file or launch term --- and a movement across THIS run's two halves is the two passes, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage3-lean` alone at 0.023**, with `lib-stage2-lean` at 0.024, `lib-stage1` and `lib-stage2-lean-u1` at 0.025 and the shipped leaf at 0.026 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, Run 40's sixth, the one-level fill, being retired. **Paired on the basis the head is a tie between the two lean fills and a lead over the rest**: `lib-stage3-lean` over `lib-stage2-lean` is **0.9904** at 13 of 19 and p 0.17, which is registration item (1) holding, and `lib-stage2-lean` over the shipped leaf **0.8911** at 15 of 19 and over `lib-stage1` **0.9004** at 14 of 19 --- so the two lean fills lead `lib-stage1` and the shipped leaf by ten and eleven points, where Run 40's inward fill led its outward twin by three and a half. **The third is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6354** on the basis and **0.6369** on the control, 0.15 of a point apart on a pair that moves `list` by twenty-nine points, the control's figure inside the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 and the basis's 0.04 of a point under it --- a span carried from that file and not re-derived here.

**The fifteen commits reached the clock where the registration said, and one family no commit reached moved on one half.** Against Run 40's basis, the same recipe on `bb6b12e`, `lib-stage2-lean` reads **0.9563** on counts of 0.9737 and `lib-stage3-lean` **0.9809** on 0.9976 --- the two fills items (1) and (3) are about, read across runs rather than within one --- while `lib-stage1` reads 0.9894 on counts level to the fourth decimal and `lib-stage2-lean-u1` 0.9929 on 0.9985. **The strict merge's reading of 2026-09-25 reproduces in the run**: on `small-flat64` the basis runs the three lean fills at 0.74 to 0.78 of Run 40's net time and the control at 1.00 to 1.01, where that reading, taken on one build, put the basis at 0.71 to 0.77 and the control at 1.00 to 1.11. **The family no commit reached is `bq-expand`, on the BASIS half alone**, slower than Run 40's basis on level instructions in four populations and past 3% on none on the control, which is registration item (4)'s kill; [What the next run compares against](#what-the-next-run-compares-against) gives the main set's cells and [the registration](#what-this-run-was-built-to-answer-and-what-it-answered) its verdict.

**The half-local movers against Run 40 are two kinds past the fills, and the second has its counts level.** `--half-movers run41 run40` flags nineteen arm-populations past 3% on ONE half each, three more arms having moved on both halves, which is the runs parting and not a half. **Two are count-led**: `lib-stage3-lean` and `lib-stage2-lean-u1` on the basis's `small`, 11.7% and 8.8% faster on counts down 2.6% and 1.5%. **Seventeen have their counts level**: the basis's `bq-expand` trio on `main`, `bcastmid` and `window`, with two of it on `rev`, 3.0 to 10.2% slower; and the control's `list` or its distant copy on `bcast`, `block`, `compose` and `flip`, 3.3 to 4.3% faster --- on four class processes and not on the main set, where the control's `list` reads 1.0009 of Run 40's. A mover with its counts level is that half's binary, its file instance or its process and not the pair's variable. **The copy test, taken 2026-09-26 on a quiet box after the evening, splits the seventeen by kind**: `probe-r41-instance.sh` timed the widest cell of each of the eight arm-populations in cycles an iteration, the difference of an `-n 2N` and an `-n N` process over three interleaved passes, on the timed file, a fresh copy of it and Run 40's same half. **The copy reads with the timed file on every cell**, 0.996 to 1.013 of it, so no mover is the file instance. **The `bq-expand` movers are this run's BUILD**: Run 40's basis runs those four cells at 0.883 to 0.906 of this run's in fresh processes, where the evening read this run's at 1.089 to 1.143 of Run 40's. **The `list` movers are the evening's PROCESS**: Run 40's control reads 0.976 to 1.007 of this run's in fresh processes, where the evening read this run's at 0.925 to 0.956 of Run 40's, the passes spreading up to 12% on those cells. **Step 4b's cells read the same way**: ranked by time over counts, the twenty widest cells of the 2370 are all `bq-expand-nosum`, whose counts the two passes move by 37 to 40% on cells where its clock moves by under 6%, and the count-led cells are led by the `bq-expand` family's, whose counts the passes move by up to 132%; Run 40's two time-led cells with counts level sat on `runs-3`, which this roster no longer times.


## What the next run compares against

**Run 41's pair is Run 40's rebuilt on the changed source, [registered 2026-09-25](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of that day, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; `Recommended tasks after Run 41` is NOT that site and holds post-mortems, which is [an open entry](../README.md#what-is-open) of its own. What this run leaves as the reference is `run41-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `688e952`, the shim at `1a359bd` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **It is the sixth published basis on that compiler, and the step from the fifth is the source and the shim and nothing else**: against `run40-gheadnospec`, the same recipe on `bb6b12e` and `fe6d133`, eleven of the sixteen timed arms both runs carry read within 1.1 points of 1, and five do not --- `lib-stage2-lean` at **0.9563** and `lib-stage3-lean` at **0.9809**, below 1 meaning this run is the faster, and the `bq-expand` trio at **1.0385** to **1.0428**, `--bridge` putting `lib-stage2-lean` and the trio outside the 3.3% drift band. `lib-stage2-lean`'s gain sits on the two smallest main-set shapes, `cnn-slice-c32` at 0.721 and `cnn-L1-6x6-c1` at 0.740, where its instructions fell with it; `bq-expand`'s loss sits on eight of the nineteen shapes, 5.8 to 13.6% slower with `cnn-L2-24x24-c32` the widest, and its instructions a call are Run 40's to the fourth decimal on the main set. **The pair itself is Runs 36's to 40's, built a sixth time**, and its draws are `./read-run.py --record regime`'s, a row per build: on `list` this one lands among the five before it, and on `bq-expand` it lands 5.2 points above the highest of them --- the basis half's family moving and not the control's, which reads it within a quarter of a point of Run 40's same half on the main set. Against Run 31's whole-level **1.2974** the five later `list` draws straddle the level, so **the level's other passes still do not measurably hand `list` back**. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918`, as Runs 36's to 40's were --- and the step this run reads is not a compiler step at all.** The tally of pairs BUILT to ask the compiler stands where Run 35 left it, at TEN. **What this run adds is the pair's sixth build, on a source fifteen commits on and a shim two on**: Runs 36 to 41 are the same two recipes on the same compiler, Runs 39's to 41's with the settled cost on both, and their cross-half readings agree to 0.94 points on `list` over the five later draws, Run 36's wild cell set aside, while `bq-expand` leaves the 1.2980 to 1.3101 its five earlier draws kept for 1.3620. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim and the source together --- and on `bq-expand` this is the first draw to break the bound. **The REGIME variable has now been asked NINE times.** Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s six build rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them, this one furthest. On `list` they multiply to 1.3325 against Run 31's 1.2974, and the five later HEAD draws straddle the level on the eighteen shapes where Run 36 read above it.

**What Run 41 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 40 and this run, and the gate says the box still measures as it did, the machine check reading `list`'s net inside the bars against the fingerprint Run 40 installed ([Provenance](#provenance) gives the figures). **This reading carries a source term and a shim term**: Run 40's basis is this basis's recipe on `bb6b12e` and `fe6d133`, and `list` runs no code the fifteen commits changed, so `list` holding level says the shim's replanning left `list` where it was, and says nothing of `bq-expand`, which moved and which the check does not read. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 41's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **Four of the five spans held, on every population and half their scope names, and the fifth, `bq-expand`'s cross figure, was killed**, and the priors behind items (1) to (3) were instruction counts off this run's own basis binary, taken after the build, as Run 40's were. **What a next registration should take from this one is that an untouched arm's cross figure is not a quantity a rebuild leaves alone**: item (4) argued from no commit reaching `bq-expand` and the shim being shared by the halves, and the family moved 4.3% on ONE half with its instructions level --- a placement term that argument does not reach, the chapter's eight reordering clauses having failed the same way on times.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 41**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918`, on `Main.hs` at `688e952` with the shim at `1a359bd`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 40 published a HEAD half on this basis's recipe, so the two published columns carry no compiler term, only the source and the shim. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9563** on `lib-stage2-lean` to **1.0428** on `bq-expand`, below 1 meaning this run is the faster, as the first paragraph of this section breaks down. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 41 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918) | Run 41 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.032 |
| `lib-stage1` | **0.025** | 0.032 |
| `lib-stage2-lean` | **0.024** | 0.031 |
| `lib-stage2-lean-u1` | **0.025** | 0.033 |
| `lib-stage3-lean` | **0.023** | 0.030 |
| `bq-expand` | **0.134** | 0.127 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on six of the seven rows, the control higher on each of those six, while `bq-expand` prints 0.134 and 0.127, the one arm whose own move outpaces the denominator's; in absolute terms the flagged half is the faster on thirteen of the sixteen timed arms, `--compare` putting the other three, `lib-stage3-lean`, `lib-stage2-lean-u1` and `lib-stage2-lean`, at 0.9953 to 0.9997, inside the 0.71-point bar that comparison prints. **Read DOWN a column and the head is `lib-stage3-lean` alone**, at 0.023 on the basis and 0.030 on the control, with `lib-stage2-lean` next on both; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, the two-column table above carrying seven of its rows and every other published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6369** (0.6354); `lib-stage1` against `-u2` **0.9909** (0.9897); `lib-stage2-lean` against `-u2` **0.8938** (0.8911) and against `lib-stage1` **0.9020** (0.9004); `lib-stage3-lean` against `lib-stage2-lean` **0.9948** (0.9904); `lib-stage2-lean-u1` against `lib-stage2-lean` **1.0638** (1.0601); and the headline pair README's opening leads with, `bq-expand` against `mut-odo-vecdims`, **2.1946** (2.9735), 0 of 19 shapes to `bq-expand` on either half. **All seven hold their direction across the halves**, the six besides the headline pair each moving under half a point; the headline pair moves by 77.9 points, the pair's own variable and, this run, the basis half's `bq-expand` besides. **`lib-stage2-lean` now leads the shipped leaf by eleven points on both halves**, where Run 40 read seven, and `lib-stage3-lean` sits within half a point to a point of it, at sign p 0.17 on both.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.34 us | 0.078 | `lib-stage3-lean` 0.043 | `mut-odo-vecdims-add-in-leaf-u2` 0.054 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.58 us | 0.090 | `lib-stage3-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.069 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 119 us | 0.065 | `lib-stage2-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 388 us | 0.043 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 462 us | 0.048 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.030 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.72 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.37 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.9 ms | 0.041 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.8 ms | 0.052 | `lib-stage3-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.6 ms | 0.031 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.7 ms | 0.023 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.2 ms | 0.113 | `lib-stage2-lean-u1` 0.112 | `mut-odo-vecdims` 0.113 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.7 ms | 0.022 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 31 ms | 0.087 | `lib-stage1` 0.073 | `mut-odo-vecdims-add-in-leaf-u2` 0.076 |
| `stretch-bigstride` | 3 | 1800000 | 50.9 ms | 0.033 | `lib-stage1` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.7 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 40.9 ms | 0.021 | `lib-stage1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.7 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 933 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.3 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.5 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.2 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.7 ms | 0.016 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.5 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.66 ms | 0.052 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.28 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.7 ms | 0.034 | `lib-stage2-lean-u1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.1 ms | 0.022 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.23 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.28 ms | 0.024 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.27 ms | 0.024 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-page` | `block` | 64 | 131072 | 2.38 ms | 0.029 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.51 ms | 0.020 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 942 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 942 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.7 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 30.3 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.3 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.052 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.3 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 29.9 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.6 ms | 0.046 | `lib-stage2-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.040 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 119 us | 0.063 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 461 us | 0.047 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.39 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.4 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.4 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.7 ms | 0.024 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.8 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 28.9 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 29.1 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 32.4 ms | 0.033 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-2` | `runs` | 2 | 1800000 | 40 ms | 0.057 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 30 ms | 0.025 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.4 ms | 0.040 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.7 ms | 0.025 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-5` | `runs` | 5 | 1800000 | 33.3 ms | 0.038 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.5 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 31.9 ms | 0.030 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-96` | `runs` | 96 | 1800000 | 29.3 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.6 ms | 0.026 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 268 us | 0.029 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.15 ms | 0.028 | `lib-stage2-lean-u1` 0.029 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.077 | `lib-stage3-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.42 us | 0.050 | `lib-stage3-lean` 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.045 |
| `small-flat64` | `small` | 64 | 256 | 4.44 us | 0.058 | `lib-stage2-lean-u1` 0.006 | `mut-odo-vecdims` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.29 us | 0.090 | `lib-stage3-lean` 0.050 | `mut-odo-vecdims-add-in-leaf-u2` 0.069 |
| `small-row96` | `small` | 96 | 384 | 6.46 us | 0.042 | `lib-stage3-lean` 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 282 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 960 us | 0.087 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.47 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.66 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.87 ms | 0.051 | `lib-stage3-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.7 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage3-lean` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.7 ms | 0.031 | `lib-stage1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty rows is a geomean over fewer shapes than the rest, as on Runs 32 to 40 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the TEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FOURTEEN of the thirty rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names three different `lib-` arms --- `lib-stage3-lean` on FIVE rows, `lib-stage2-lean` on four and `lib-stage1` on one --- where Run 40 named `lib-stage3-lean` on five, `lib-stage3-lean-onelevel` on four and `lib-stage1` on one. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 41's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in the same eleven populations Runs 36 to 40 broke it in, at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9991**, where the control reads **0.9819**. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw, inside its 0.33% floor. Every other shape of every population reads the clause with room, the classes' closest cells at 0.28 to 0.48 on the basis. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, and the case has simplified three times --- the prune of 2026-09-04 parked the arm that used to be half of it, the retirement of 2026-09-09 took four of the five arms that broke the rest, and the retirement of `runs-3` on 2026-09-25 took one of its cells: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` is slower than `list` on `runs-2` on both halves, at **1.1177** on the basis and **1.3678** on the control; `--over-list` reads every other one of the 1106 timed non-control cells this run carries, over all eleven populations on both halves, at or under 1. **It is the cell Runs 36 to 40 read**, the third they read being on the retired view, **and it is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0464 between the halves while `list` moves 1.2806.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the eleventh run running that this property is the one left entirely alone.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits under 0.053. The `bq-expand` clause is closest at `small-row96` on the CONTROL half, **1.00441**, then `scaled-rank1-m1` at 1.00003 on both halves, and `stretch-tall-Mx2` at 1.00000 on both halves of the main set with `bcast-src8` at 1.00000 on the control. **Those five figures are Runs 36's to 40's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, no commit having rewritten code behind `mut-odo-vecdims`, `bq-expand` or `list`. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in all ten classes and on the main set, on both halves --- and their LEVEL clause BREAKS in every one of the eleven populations, as it did on Runs 36 to 40, and on Run 31 before them, where registration (10) died on it.** The order clause is untouched: the mutable fills sit at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 19.00x to 27.66x, on both halves and in every population, `small` outside the LEVEL clause by the ruling of 2026-09-07 as before. What breaks is the level: **the two passes change what `list` and `bq-expand` ALLOCATE, and this run reads that change at Run 31's own figures.** On the main set the fills read 1.00x on both halves while `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the nineteen shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 40's to the fourth decimal.

**AND FOUR ARMS OUTSIDE THE TWO FAMILIES MOVE, all of them unordered consumers, by 1.5 to 2.1 points, where Run 40 read six moving by 15.5 to 19.5.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.9795** of the basis on `libunord-stage6-sum`, 0.9810 on `-stage6-loop-sum`, 0.9811 on `-stage7-sum` and 0.9852 on `-stage9-sum`, where Run 40 read 0.8053, 0.8064, 0.8067 and 0.8413; `-stage13-sum` and `-stage14-sum`, which Run 40 read at 0.8447 and 0.8448, now read 1.0001 and 0.9999, and `libunord-stage1-sum` 0.9994. The fills and ordered consumers read 0.9981 to 1.0000 --- `lib-stage2-lean` and its `-u1` at 0.9981 the lowest, now that they share the strict merge. **Every one of the six is reached by the fifteen commits** --- `815ffa2`'s strict merge record and `f7cbccf`'s typed pair lists reach the first five, the `Axis` path the sixth, `registration-drift.py` naming each --- and a reading of 2026-09-25 put most of the move on the merge fold's boxing, which `815ffa2` made a strict record ([the open list][open]); on `small` the six read 0.969 to 1.000 per cell, flagged over basis, which is what the preparation read off the two binaries before the run and [the open list][open] carried. **In absolute terms it is 432 to 2447 bytes a call on the basis main set** and the family sits at the 0.01x tier, so no tier moves and no property verdict changes with it. `--alloc` puts 283 of the main set's 532 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-aa-distant`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 41 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 27.52 points on `bcastmid` at narrowest and 39.12 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 40, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **160 arm-comparisons, 24 putting the basis faster and 136 slower**, with no degenerate arm excluded, at geomeans from **1.0677** on `scaled` to **1.1555** on `window` and extremes of `lib-stage2-lean-u1` at **0.9874** on `flip` and `bq-expand-aa-distant` at **1.6696** on `window`. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **No registration of this run names a class**: every span is `on main`, so each block below carries its properties, its floor and its own cross-half reading.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **In practice the bold marks the FASTER of the two named arms, one cell a row**, and on this run it is the arm outside the family on ALL TEN --- `lib-stage3-lean` on `bcast`, `window`, `runs`, `small` and `compose`, `lib-stage2-lean` on `rev`, `bcastmid`, `flip` and `block`, and `lib-stage1` on `scaled`. **The family's ceiling is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Runs 39 and 40. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.063 | **`lib-stage2-lean`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.42% |
| `bcast` | 6 | 0.022 | 0.057 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.90% |
| `bcastmid` | 4 | 0.029 | 0.052 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.32% |
| `window` | 8 | 0.051 | 0.087 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.55% |
| `scaled` | 3 | 0.027 | 0.029 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 1.01% |
| `runs` | 16 | 0.026 | 0.057 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.24% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage2-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.76% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage2-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.47% |
| `small` | 5 | 0.061 | 0.090 | **`lib-stage3-lean`** 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 | 0.35% |
| `compose` | 4 | 0.024 | 0.029 | **`lib-stage3-lean`** 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 | 0.46% |

The best arm outside the family is ahead of `mut-odo-vecdims` in every one of the ten classes. **No row's bold sits in the CEILING column this run**, as on Runs 39 and 40. SIX rows change the arm they name: `runs` and `small` name `lib-stage3-lean` and `flip` and `block` name `lib-stage2-lean` where Run 40 named `lib-stage3-lean-onelevel`, which this roster no longer times, and `rev` and `bcastmid` name `lib-stage2-lean` where Run 40 named `lib-stage3-lean` --- so the retired one-level fill's four rows split between the two lean fills, on margins the class paragraphs below price. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **No row ties at three decimals this run**, the closest being six rows a thousandth apart --- `rev`, `bcast`, `scaled`, `runs`, `block` and `compose`, so every bold is a lead a reader of the table can see.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.09 | 148 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.11 | 148 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.08 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.01 | 157 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.01 | 157 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.01 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.01 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage2-lean | 0.021 | 0.025 | 0.09 | 148 | 1.00x |
| lib-stage3-lean | 0.021 | 0.025 | 0.10 | 148 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.041* | *0.06* | *147* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.041* | *0.08* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.041 | 0.06 | 147 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.028 | 0.09 | 147 | 1.00x |
| lib-stage1 | 0.024 | 0.037 | 0.13 | 148 | 1.01x |
| **mut-odo-vecdims** | **0.042** | 0.063 | 0.12 | 138 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.04* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.064* | *0.07* | *138* | *1.00x* |
| bq-expand | 0.143 | 0.260 | 0.11 | 122 | 3.22x |
| *bq-expand-aa-adjacent* | *0.143* | *0.260* | *0.10* | *122* | *3.22x* |
| *bq-expand-aa-distant* | *0.143* | *0.260* | *0.08* | *122* | *3.22x* |
| *list-aa-distant* | *1.000* | *1.001* | *0.14* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.15 | 85 | 26.11x |
| *list-aa-adjacent* | *1.000* | *1.001* | *0.12* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9958, worst cell 0.72% on `rev-primes`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `rev-cnn-L1-24x24-c1`, its interval covering 1. The in-situ term reads 0.9983, 1.0142 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9984, which the correction amplifies by 2.16x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h7m52s, peak 96 MiB in use, 24 MiB max residency; the reader reads 30 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.54 ms per call raw, 4.39 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.063/0.047/0.025

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.1124, from `mut-odo-vecdims` at 0.9977 to `bq-expand-aa-adjacent` at 1.3552, with `list` itself at 1.2961. **The baseline moved 29.61% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.063, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage2-lean` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.4928 over 3 of 3 shapes at sign p 0.25, a margin of 50.72% against this class's 0.42% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 29.61 of a point, at a class geomean of 1.1124 over the 16 arms, with 2 of 8 strategies past an A/A bar of 0.78 points. The counted work reads a counts geomean of 1.1656 over the same arms, 16 of them counted. Its counted work parts by 16.56 points where its clock parts by 11.24, so about 0.68 of the instruction saving reaches the clock. Its one half-local mover against Run 40 is the basis's `bq-expand`, with its adjacent copy, 3.0% slower on level counts --- the main set's `bq-expand` move again.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.59* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.47 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.33* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.015 | 0.020 | 0.49 | 62 | 1.00x |
| lib-stage2-lean | 0.015 | 0.020 | 0.40 | 62 | 1.00x |
| lib-stage1 | 0.015 | 0.020 | 0.40 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.50* | *62* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.38* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.40 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.49 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.34* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.022** | 0.057 | 0.07 | 61 | 1.00x |
| *mut-odo-vecdims-aa* | *0.022* | *0.057* | *0.36* | *61* | *1.00x* |
| bq-expand | 0.092 | 0.140 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.092* | *0.143* | *0.06* | *46* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.093* | *0.140* | *0.76* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.23 | 17 | 20.99x |
| *list-aa-distant* | *1.005* | *1.011* | *0.95* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.006* | *1.014* | *0.77* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0090, worst cell 2.10% on `bcast-tall-Mx2`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `bcast-src512`, its interval covering 1. The in-situ term reads 1.0206, 1.0145 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0068, which the correction amplifies by 1.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m41s, peak 180 MiB in use, 42 MiB max residency; the reader reads 30 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.6 ms per call raw, 29.5 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.016/0.019/0.019

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0960, from `lib-stage2-lean` at 0.9947 to `list-aa-distant` at 1.3961, with `list` itself at 1.3912. **The baseline moved 39.12% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6437 over 6 of 6 shapes at sign p 0.031, a margin of 35.63% against this class's 0.90% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 39.12 of a point, at a class geomean of 1.0960 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.81 points. The counted work reads a counts geomean of 1.1697 over the same arms, 16 of them counted. Its counted work parts by 16.97 points where its clock parts by 9.60, so about 0.57 of the instruction saving reaches the clock. Its one half-local mover against Run 40 is the control's `list`, 4.3% faster on level counts.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.47* | *64* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.35 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.30 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.37 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.40 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.30 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 97 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.41* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *89* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.017 | 0.34 | 82 | 1.00x |
| lib-stage3-lean | 0.012 | 0.019 | 0.36 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.019 | 0.30 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.018 | 0.34 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.029* | *0.41* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.029* | *0.32* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.029 | 0.25 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.052* | *0.32* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.052 | 0.27 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.48* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.104* | *0.208* | *0.40* | *60* | *1.92x* |
| bq-expand | 0.104 | 0.208 | 0.43 | 60 | 1.92x |
| *bq-expand-aa-distant* | *0.104* | *0.208* | *0.37* | *60* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 0.78 | 28 | 23.56x |
| *list-aa-distant* | *1.001* | *1.003* | *0.79* | *28* | *23.56x* |
| *list-aa-adjacent* | *1.001* | *1.004* | *0.61* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9968, worst cell 1.22% on `bcastmid-primes`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.07% on `bcastmid-primes`, its interval covering 1. The in-situ term reads 1.0186, 1.0933 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9988, which the correction amplifies by 2.39x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m30s, peak 129 MiB in use, 35 MiB max residency; the reader reads 30 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.8 ms per call raw, 47.7 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.052/0.019/0.034/0.022

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.1057, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0013 to `bq-expand` at 1.3114, with `list` itself at 1.2752. **The baseline moved 27.52% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4119 over 4 of 4 shapes at sign p 0.12, a margin of 58.81% against this class's 0.32% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). Its two columns may NOT be differenced, `list` having moved 27.52 of a point, at a class geomean of 1.1057 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.49 points. The counted work reads a counts geomean of 1.1710 over the same arms, 16 of them counted. Its counted work parts by 17.10 points where its clock parts by 10.57, so about 0.62 of the instruction saving reaches the clock. Its half-local movers against Run 40 are the basis's `bq-expand` trio, 3.7 to 4.9% slower on level counts --- the main set's `bq-expand` move again.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.33* | *60* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.20 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.17 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.16 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.19 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.04 | 106 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.05 | 105 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.05 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.06 | 102 | 0.02x |
| libunord-stage7-sum | -- | -- | 0.05 | 104 | 0.02x |
| libunord-stage9-sum | -- | -- | 0.05 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *97* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage2-lean | 0.023 | 0.027 | 0.20 | 84 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.24 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.028 | 0.18 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.17* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.15 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.17* | *82* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.051* | *0.087* | *0.17* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.087 | 0.17 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.087* | *0.16* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.201* | *0.215* | *0.33* | *56* | *3.86x* |
| bq-expand | 0.201 | 0.215 | 0.36 | 56 | 3.86x |
| *bq-expand-aa-distant* | *0.201* | *0.218* | *0.25* | *56* | *3.86x* |
| list (baseline) | 1.000 | 1.000 | 0.50 | 30 | 27.66x |
| *list-aa-adjacent* | *1.000* | *1.005* | *0.41* | *30* | *27.66x* |
| *list-aa-distant* | *1.001* | *1.006* | *0.44* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0055, worst cell 1.39% on `window-64x64-k1x9`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `window-64x64-c16-k3`, its interval covering 1. The in-situ term reads 1.0105, 1.1484 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0048, which the correction amplifies by 1.15x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h20m49s, peak 120 MiB in use, 46 MiB max residency; the reader reads 30 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.7 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.087/0.031/0.051/0.051/0.053/0.052

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.1555, from `lib-stage2-lean-u1` at 0.9925 to `bq-expand-aa-distant` at 1.6696, with `list` itself at 1.3070. **The baseline moved 30.70% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.087, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.4091 over 8 of 8 shapes at sign p 0.0078, a margin of 59.09% against this class's 0.55% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 30.70 of a point, at a class geomean of 1.1555 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.39 points. The counted work reads a counts geomean of 1.1776 over the same arms, 16 of them counted. Its counted work parts by 17.76 points where its clock parts by 15.55, so about 0.88 of the instruction saving reaches the clock. Its half-local movers against Run 40 are the basis's `bq-expand` trio, 9.8 to 10.2% slower on level counts, the widest that move reaches in the run.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.13* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.14 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.15 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.12 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.16 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.19 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *138* | *0.00x* |
| lib-stage1 | 0.022 | 0.030 | 0.13 | 128 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.030 | 0.13 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.030 | 0.15 | 128 | 1.00x |
| lib-stage3-lean | 0.023 | 0.030 | 0.15 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.023* | *0.030* | *0.14* | *127* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.023* | *0.030* | *0.13* | *128* | *1.00x* |
| lib-stage2-lean-u1 | 0.023 | 0.029 | 0.27 | 127 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.029* | *0.09* | *127* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.026* | *0.029* | *0.06* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.029 | 0.08 | 127 | 1.00x |
| *bq-expand-aa-distant* | *0.091* | *0.101* | *0.06* | *111* | *1.21x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.102* | *0.06* | *111* | *1.21x* |
| bq-expand | 0.091 | 0.101 | 0.09 | 111 | 1.21x |
| list (baseline) | 1.000 | 1.000 | 0.15 | 69 | 21.49x |
| *list-aa-adjacent* | *1.002* | *1.003* | *0.13* | *69* | *21.49x* |
| *list-aa-distant* | *1.003* | *1.003* | *0.20* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9899, worst cell 2.32% on `scaled-r5`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.02% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0208, 1.0155 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9960, which the correction amplifies by 2.43x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h7m52s, peak 109 MiB in use, 35 MiB max residency; the reader reads 30 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.33 ms per call raw, 5.15 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.0677, from `mut-odo-vecdims-aa` at 0.9881 to `list-aa-distant` at 1.3262, with `list` itself at 1.3197. **The baseline moved 31.97% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.8980 over 2 of 3 shapes at sign p 1, a margin of 10.20% against this class's 1.01% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.97 of a point, at a class geomean of 1.0677 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.74 points. The counted work reads a counts geomean of 1.1524 over the same arms, 16 of them counted. Its counted work parts by 15.24 points where its clock parts by 6.77, so about 0.44 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen, and cut to sixteen for Run 41, `runs-3` (`sInner` 3, a k3 conv row) leaving timing in `94aeee7` and staying in `check`.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.35* | *52* | *1.07x* |
| liblist-stage1-sum | -- | -- | 0.13 | 62 | 0.35x |
| liblist-stage4-sum | -- | -- | 0.02 | 75 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.10 | 62 | 0.35x |
| libunord-stage13-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 70 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 75 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.11* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.024 | 0.09 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.024 | 0.12 | 60 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.024 | 0.14 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.38* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.025 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.025* | *0.11* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.08* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.057 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.057* | *0.08* | *59* | *1.00x* |
| lib-stage1 | 0.086 | 1.118 | 0.22 | 52 | 1.35x |
| *bq-expand-aa-adjacent* | *0.091* | *0.141* | *0.52* | *46* | *1.07x* |
| bq-expand | 0.092 | 0.141 | 0.41 | 46 | 1.07x |
| *bq-expand-aa-distant* | *0.093* | *0.143* | *0.04* | *46* | *1.07x* |
| list (baseline) | 1.000 | 1.000 | 2.39 | 17 | 21.26x |
| *list-aa-distant* | *1.031* | *1.050* | *0.30* | *17* | *21.26x* |
| *list-aa-adjacent* | *1.032* | *1.044* | *0.22* | *17* | *21.26x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0324, worst cell 4.44% on `runs-16384`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.05% on `runs-7`, its interval covering 1. The in-situ term reads 1.0285, 1.0295 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0313, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h41m40s, peak 597 MiB in use, 270 MiB max residency; the reader reads 30 benchmarks over 16 shapes of the runs class. Anchor: `runs-2`, `list` at 41 ms per call raw, 40 ms net.

**Per shape, in the run's shape order (runs-2, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.040/0.038/0.033/0.030/0.025/0.025/0.025/0.025/0.025/0.025/0.024/0.024/0.024/0.024/0.026

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0861, from `lib-stage3-lean` at 0.9989 to `list` at 1.3490, with `list` itself at 1.3490. **The baseline moved 34.90% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.07x, 21.26x --- and `lib-stage3-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7994 over 16 of 16 shapes at sign p 3.1e-05, a margin of 20.06% against this class's 3.24% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 34.90 of a point, at a class geomean of 1.0861 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.49 points. The counted work reads a counts geomean of 1.1600 over the same arms, 16 of them counted. Its counted work parts by 16.00 points where its clock parts by 8.61, so about 0.54 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *64* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.10 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.09 | 93 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.10 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.13 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.08* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.022 | 0.041 | 0.23 | 84 | 1.00x |
| lib-stage3-lean | 0.022 | 0.041 | 0.30 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.045 | 0.25 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.040* | *0.31* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.040* | *0.11* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.040 | 0.09 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.052* | *0.10* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.08 | 77 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.12* | *77* | *1.00x* |
| lib-stage1 | 0.032 | 0.048 | 0.21 | 82 | 1.00x |
| *bq-expand-aa-adjacent* | *0.090* | *0.206* | *0.42* | *60* | *1.05x* |
| bq-expand | 0.090 | 0.206 | 0.43 | 60 | 1.05x |
| *bq-expand-aa-distant* | *0.092* | *0.207* | *0.08* | *60* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.74 | 32 | 21.18x |
| *list-aa-distant* | *1.006* | *1.017* | *0.46* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.008* | *1.021* | *0.25* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0076, worst cell 2.12% on `flip-last-rows`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.04% on `flip-outer-gap64`, its interval covering 1. The in-situ term reads 1.0179, 1.0234 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0073, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m41s, peak 209 MiB in use, 76 MiB max residency; the reader reads 30 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31 ms per call raw, 29.9 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.046/0.026/0.026

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.0784, from `lib-stage2-lean-u1` at 0.9874 to `list-aa-distant` at 1.3407, with `list` itself at 1.3345. **The baseline moved 33.45% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.7292 over 6 of 6 shapes at sign p 0.031, a margin of 27.08% against this class's 0.76% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 33.45 of a point, at a class geomean of 1.0784 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.54 points. The counted work reads a counts geomean of 1.1523 over the same arms, 16 of them counted. Its counted work parts by 15.23 points where its clock parts by 7.84, so about 0.51 of the instruction saving reaches the clock. Its one half-local mover against Run 40 is the control's `list-aa-distant`, 3.3% faster on level counts.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.11 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 129 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 128 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.03 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *122* | *0.00x* |
| lib-stage2-lean | 0.020 | 0.023 | 0.11 | 111 | 1.00x |
| lib-stage3-lean | 0.020 | 0.023 | 0.10 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.020 | 0.026 | 0.13 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.10* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.10 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.08* | *111* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.08* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.08 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| lib-stage1 | 0.051 | 0.059 | 0.15 | 103 | 1.42x |
| bq-expand | 0.086 | 0.086 | 0.16 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.086* | *0.086* | *0.10* | *96* | *1.06x* |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.08* | *96* | *1.06x* |
| *list-aa-distant* | *1.000* | *1.002* | *0.19* | *54* | *21.22x* |
| *list-aa-adjacent* | *1.000* | *1.003* | *0.18* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.18 | 54 | 21.22x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 1.0047, worst cell 2.16% on `block-run64-off7`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.02% on `block-run64-off7`, its interval missing 1. The in-situ term reads 1.0188, 1.0157 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0019, which the correction amplifies by 2.49x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m2s, peak 133 MiB in use, 46 MiB max residency; the reader reads 30 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.67 ms per call raw, 4.51 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.029/0.024/0.020

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.0839, from `lib-stage2-lean-u1` at 1.0110 to `list` at 1.3650, with `list` itself at 1.3650. **The baseline moved 36.50% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the family at 0.020, priced against `mut-odo-vecdims` at 0.8638 over 5 of 5 shapes at sign p 0.062, a margin of 13.62% against this class's 0.47% floor (`mut-odo-vecdims-aa`). Its two columns may NOT be differenced, `list` having moved 36.50 of a point, at a class geomean of 1.0839 over the 16 arms, with 8 of 8 strategies past an A/A bar of 0.78 points. The counted work reads a counts geomean of 1.1491 over the same arms, 16 of them counted. Its counted work parts by 14.91 points where its clock parts by 8.39, so about 0.56 of the instruction saving reaches the clock. Its half-local movers against Run 40 are the control's `list` and its distant copy, 4.1% and 3.6% faster on level counts.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.17 | 228 | 1.67x |
| liblist-stage4-sum | -- | -- | 0.07 | 242 | 1.20x |
| liblist-stage5-sum | -- | -- | 0.06 | 243 | 1.17x |
| libunord-stage1-sum | -- | -- | 0.23 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.10 | 243 | 0.28x |
| libunord-stage14-sum | -- | -- | 0.10 | 244 | 0.23x |
| libunord-stage6-loop-sum | -- | -- | 0.14 | 239 | 0.55x |
| libunord-stage6-sum | -- | -- | 0.15 | 239 | 0.55x |
| libunord-stage7-sum | -- | -- | 0.14 | 239 | 0.55x |
| libunord-stage9-sum | -- | -- | 0.25 | 238 | 0.42x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.23* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.03* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.03* | *250* | *0.01x* |
| lib-stage3-lean | 0.034 | 0.050 | 0.16 | 235 | 1.13x |
| lib-stage2-lean-u1 | 0.036 | 0.052 | 0.21 | 234 | 1.16x |
| lib-stage2-lean | 0.037 | 0.055 | 0.14 | 234 | 1.16x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.069* | *0.27* | *229* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.053* | *0.069* | *0.20* | *229* | *1.28x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.053 | 0.069 | 0.24 | 229 | 1.28x |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.089* | *0.29* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.061** | 0.090 | 0.20 | 229 | 1.27x |
| *mut-odo-vecdims-aa* | *0.061* | *0.090* | *0.26* | *229* | *1.27x* |
| lib-stage1 | 0.083 | 0.109 | 0.21 | 221 | 2.35x |
| *bq-expand-aa-adjacent* | *0.139* | *0.212* | *0.11* | *217* | *1.44x* |
| bq-expand | 0.139 | 0.212 | 0.15 | 217 | 1.44x |
| *bq-expand-aa-distant* | *0.139* | *0.212* | *0.13* | *217* | *1.44x* |
| *list-aa-distant* | *1.000* | *1.006* | *0.13* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.14 | 180 | 21.57x |
| *list-aa-adjacent* | *1.000* | *1.006* | *0.14* | *180* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9965, worst cell 0.71% on `small-patch-r5`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.08% on `small-bcast32`, its interval covering 1. The in-situ term reads 0.9623, 1.0020 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9978, which the correction amplifies by 1.60x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m5s, peak 135 MiB in use, 54 MiB max residency; the reader reads 30 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.68 us per call raw, 6.46 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.042/0.077/0.050/0.058/0.090

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.1030, from `lib-stage3-lean` at 1.0176 to `list-aa-distant` at 1.3041, with `list` itself at 1.2971. **The baseline moved 29.71% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.090, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean` leads outside the family at 0.034, priced against `mut-odo-vecdims` at 0.4555 over 5 of 5 shapes at sign p 0.062, a margin of 54.45% against this class's 0.35% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 29.71 of a point, at a class geomean of 1.1030 over the 16 arms, with 8 of 8 strategies past an A/A bar of 1.05 points. The counted work reads a counts geomean of 1.1460 over the same arms, 16 of them counted. Its counted work parts by 14.60 points where its clock parts by 10.30, so about 0.71 of the instruction saving reaches the clock. Its half-local movers against Run 40 are the basis's `lib-stage3-lean`, 11.7% faster, and `lib-stage2-lean-u1`, 8.8% faster, their counts down 2.6% and 1.5% --- the run's only half-local movers whose counts moved with them.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.34* | *85* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.30 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.34 | 98 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.33 | 98 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.30 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.37 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.30 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| lib-stage3-lean | 0.014 | 0.016 | 0.33 | 98 | 1.00x |
| lib-stage2-lean | 0.015 | 0.017 | 0.51 | 98 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.016* | *0.29* | *98* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.015* | *0.016* | *0.27* | *98* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.26 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.31 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.016 | 0.31 | 98 | 1.00x |
| *mut-odo-vecdims-aa* | *0.024* | *0.029* | *0.24* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.024* | *0.029* | *0.24* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.029 | 0.18 | 94 | 1.00x |
| bq-expand | 0.094 | 0.103 | 0.37 | 79 | 1.35x |
| *bq-expand-aa-adjacent* | *0.094* | *0.103* | *0.38* | *79* | *1.35x* |
| *bq-expand-aa-distant* | *0.094* | *0.103* | *0.24* | *79* | *1.35x* |
| *list-aa-distant* | *0.999* | *1.003* | *0.71* | *44* | *22.01x* |
| list (baseline) | 1.000 | 1.000 | 0.62 | 44 | 22.01x |
| *list-aa-adjacent* | *1.002* | *1.008* | *0.66* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0046, worst cell 1.22% on `compose-scalar`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.03% on `compose-zero-mid`, its interval covering 1. The in-situ term reads 1.0117, 1.0255 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0033, which the correction amplifies by 1.37x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m33s, peak 126 MiB in use, 33 MiB max residency; the reader reads 30 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 31.3 ms per call raw, 30.3 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0915, from `lib-stage1` at 0.9963 to `list-aa-adjacent` at 1.3711, with `list` itself at 1.3692. **The baseline moved 36.92% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage3-lean` leads outside the family at 0.014, priced against `mut-odo-vecdims` at 0.6136 over 4 of 4 shapes at sign p 0.12, a margin of 38.64% against this class's 0.46% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 36.92 of a point, at a class geomean of 1.0915 over the 16 arms, with 6 of 8 strategies past an A/A bar of 0.52 points. The counted work reads a counts geomean of 1.1641 over the same arms, 16 of them counted. Its counted work parts by 16.41 points where its clock parts by 9.15, so about 0.56 of the instruction saving reaches the clock. Its half-local movers against Run 40 are the control's `list` and its distant copy, 3.7% and 3.6% faster on level counts.


## Provenance

**Run 41's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `688e952`; one shim, `align-as.py` at `1a359bd`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`, which is Runs 36's to 40's compiler unmoved; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run41-gheadnospec` and is what every table here publishes; `run41-gheadtwopass` is the candidate. **What is new against Run 40 is not the pair but two things under both halves**: the source moved fifteen of the owner's commits, `bb6b12e` to `688e952`, and the shim two, `fe6d133` to `1a359bd`, the second changing which groups the settled cost plans again under `LOOP_SETTLED=1`. The recipes, the project file, the compiler and the launch are Run 40's to the character, and no reboot sits between the two runs, `uptime` putting the box up since 2026-09-24 00:00 at both.

**The roster is 30 timed arms over 19 main-set shapes and 570 benches, with 60 class views over ten classes for 1800 more, and it is Run 40's LESS TWO RETIREMENTS.** `./roster-delta.py run40-gheadnospec run41-gheadnospec`, read off the two binaries, puts one arm out, `lib-stage3-lean-onelevel` (`0cd790c`), and one class view out, `runs-3` (`94aeee7`), both kept in `check`, and nothing in: the other 30 arms run in Run 40's order over the same nineteen main-set shapes, and the other nine classes' views are unmoved. So pre-run step 12's condition fired, and the -L1 roster pass it owes was stopped on the owner's word of 2026-09-26 and not taken; every cross-run figure in this file is read over the 30 arms both runs time and, on `runs`, over the sixteen views both ran.

**The evening ran in ONE window and in the order the run list gives, and one process met foreign CPU, on two benches.** `run-evening.sh` took the gate from 01:36:46 to 02:10:04, the alarm at 02:10:07 reading 0.1% busy, the sequence from 2026-09-26T02:10:07 to 2026-09-26T09:01:49 and the riders from 09:01:49 to 09:14:14, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back, the largest hole between one finishing and the next starting 0m, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones --- and each launched from `./run41-<half>`. The counted work, which wants no quiet machine, ran from 09:14, with the `-g3` twins building beside it. **`--wild` names ONE intrusion**, in the control's main-set process: 2 of its 570 benches at or above 0.25 of a core foreign, both on `stretch-tall-Mx2` and both unordered reducing consumers, `libunord-stage7-sum` at a peak of 1.95 and `-stage6-loop-sum` at 1.20, the other twenty-one logs reaching 0.25 on no bench. Across the halves, basis over control, the two cells read 0.9739 and 0.9742 on raw `slope` and 0.9770 and 0.9619 on the mutator clock, the intruded half the slower. **Post-run step 3's rerun was not taken, on the owner's word of 2026-09-26**, the note's `RERUN:` line having read `ask`, so the sensitivity reading stands in its place. `--compare --exclude-shape stretch-tall-Mx2`, taken both ways, moves the two consumers' cross figures from 0.9994 and 0.9997 to 1.0009 and 1.0012, no registration reading a reducing consumer, and it leaves registration item (4)'s two verdicts where they are, `list` reading 1.2962 and `bq-expand` 1.3850 without the shape.

**The gate read SOUND and the machine check did not fire --- and the gate already carried the run's one surprise.** The two palindrome passes agree: `list` reads 1.3122 and 1.3121, `bq-expand` 1.3630 and 1.3605, and `mut-odo-vecdims` 1.0024 and 1.0013 --- 0.01, 0.18 and 0.11 points apart --- with the two `sum-only` controls, on raw `slope`, within 0.07% of 1 on both passes. **What the passes part by is each half's own leg-to-leg movement and not a disagreement about the pair**: the control's `a` leg over its `b` reads `bq-expand` at 0.9966 where the basis's two legs read 0.9984, the passes' ratio being the two halves' legs divided by construction (`./read-run.py --gate-draft run41` prints all four). The machine check, read against the fingerprint Run 40 installed --- this run's basis recipe on the source before the fifteen commits and the shim before `1a359bd` --- puts `list`'s net at **+0.22%**, worst `cnn-slice-c32` at **+1.30%**, 0 of 19 shapes past 5% and the geomean inside the 3% bar; the main-set JSON reads the same check at -0.34% with `alexnet-L1-55-c3-k11` worst at -1.30%. So the source and the shim together moved the box's `list` by under the bars. **The surprise is `bq-expand` at 1.36 in both passes**, where Run 40's gate read 1.31: registration item (4)'s `bq-expand` span was already outside its band before the sequence began, which a gate verdict does not read and this file does at [the registration](#what-this-run-was-built-to-answer-and-what-it-answered).

**Every one of the twenty-two processes gated clean, the plateau refused by declaration, and FIVE A/A worst cells sit past 5%.** `read-all.sh` gates each process on its own correction and passes all twenty-two. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.6848 to 21.3490 ms/iter across the run, a 27.95% spread against a 5% band, and it splits exactly by half, the basis's eleven processes flat within 1.09% at 21.1178 to 21.3490 and the control's within 2.27% at 16.6848 to 17.0633 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-runs` at **8.60%** on `runs-2`, `gheadtwopass-main` at **6.82%** on `stretch-wide-2xM`, `gheadtwopass-window` at **5.18%** on `window-32x32-c64-k3`, `gheadnospec-bcast` at **5.10%** on `bcast-src64` and `gheadnospec-runs` at **5.05%** on `runs-1024`; the main set's floor is 0.33% on the basis and 0.63% on the control, so the main-set cell is one cell an order of magnitude outside the floor its population otherwise keeps. **No cell reaches the about 10% [the floor section][floor] gates on**, so no cell leaves the per-shape record this run.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run41-gheadnospec`, md5 `d1963ecd131378676e042e08cde87b34`, and `run41-gheadtwopass`, md5 `aba522851bd99368ba3ddb31eda7cad1`, built on 2026-09-26 against a tree clean at `688e952`. Their `.text` sections are **20174655** and **20240191** bytes, the first column of `size -A`; against Run 40's two the basis is the SAME SIZE to the byte and the flagged half smaller by 8192, two pages exactly --- the fifteen commits and the shim together, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source and the shim having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 65536 bytes --- sixteen pages exactly, as every row of `./read-run.py --record selfloops` that varies a pass is an exact page multiple --- and it carries MORE self-loops, 348 against 336, as on Runs 38 and 39 and not on Run 40, so [the open list's entry on it](../README.md#what-is-open) gains a run on that side.

**The source and the shim moved no tracked 28-byte copy off its offset.** `./loop-offsets.py --delta run40-gheadnospec run41-gheadnospec`, the same basis recipe on the two sources and shims, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0] and of the two-copy group at [0, 0], with no address surviving to the byte and every displacement a whole number of lines, four on the first group and two on the second; two bodies that had one copy each now have three, at [0, 0, 0] and [11, 11, 11]. **Within the pair** the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves and the two-copy group [0, 0] on both; the two three-copy groups read [0, 3, 3] and [11, 14, 14] on the control, and a third three-copy group, at [0, 0, 0], exists on the control half alone. `--library` puts **4.3%** of the 807 library self-loops the two halves share at the same offset in line, Run 40's 4.3% to the tenth: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 29 on the basis and 33 on the control, where Run 40 read 24 on each, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 336 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 348 on the control, 230 and 148 of them at offset 0 where Run 40 read 231 and 131 of 326 and 319, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes; the survey's x87 tell, new with `b173873`, is what keeps the basis's count at 336 and its astride count at 0, one body having read out of step before it. **Post-run step 0's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity twelve straddlers on the basis and fourteen on the control** --- on both, `sumNoSpec` twice, `fillStage2Short` twice, the leaf bodies of `fbMutOdoVecdimsAddInLeafU2`, `-Down` and `-Last` among them, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the basis the one body `fillStage3`, `fillStage2Axes` and `fillStage2` share, byte-identical in all three and straddling at offset 30 in each; on the control that body in `fillStage2Axes` and `fillStage2` alone, with `fillStage3`'s own copy, `fillStage2OneLevel` and `fbFused` besides. Of the refusals, nine on the basis and seven on the control carry a `--loose` family of `fillStage3`, `fillStage2Short`, `fillStage2VSdims` and `fillStage2OneLevel` bodies, which the bytes cannot choose between, and eight on the basis and twelve on the control are 60- to 63-byte bodies at offset 32, 40 or 48 for which no twin holds a copy. **Every twin holds FEWER loops than the binary it names for** --- 327 and 335 against 336 and 348 --- so `--match` refuses the population comparison throughout and each name rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run41-gheadnospec`, 9.992 times apart, which is plain -O1; on `run41-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. Both builders' figures are Run 40's to the byte on both halves. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.34 us** on `cnn-slice-c32`, **3.72 ms** on `cnn-L2-24x24-c32` and **39.7 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 19.4 to 21.9 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.51 us | 6.34 us | 5.01 us |
| `cnn-L2-24x24-c32` | 165888 | 3.82 ms | 3.72 ms | 2.91 ms |
| `stretch-wide-2xM` | 1800000 | 40.7 ms | 39.7 ms | 32 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.54 ms raw and 4.39 ms net; `bcast-inner900` 30.6 ms and 29.5 ms; `bcastmid-b200k` 48.8 ms and 47.7 ms; `window-128x128-k7` 14.2 ms and 13.7 ms; `scaled-rank1-m1` 5.33 ms and 5.15 ms; `runs-2` 41 ms and 40 ms; `flip-fwd-rows96` 31 ms and 29.9 ms; `block-r3-vol64` 4.67 ms and 4.51 ms; `small-row96` 6.68 us and 6.46 us; `compose-zero-mid` 31.3 ms and 30.3 ms. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and no cell of the whole run is one the reader flags.** The two `sum-only` arms agree on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9999 to 1.0001 across the twenty-two processes, at a mean absolute difference of at most 0.05% --- so the term subtracted from one half is the term subtracted from the other. **No cell sits below R2 0.99 ([what that column detects][ramp]) and none is under ten samples**, of the run's 4740 cells, 2370 on each half; the reader's warnings print for none of the twenty-two JSONs, where the same call on Run 40's `runs` JSON prints its `runs-3` cell. The three cells Run 40 flagged were all on `runs-3`, which this roster no longer times.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, 4740 cells and none refused, at a cost of 1266s on the basis and 1035s on the control --- beside Run 40's 1317s and 1075s, on a roster one arm smaller and with this run's `-g3` twins building and its first readings running alongside, which an instruction count does not see. The counts geomean over the sixteen arms that carry a corrected time runs **1.1460** on `small` to **1.1776** on `window`, the main set at **1.1674** --- the basis retiring 14.6 to 17.8 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families**: the `bq-expand` trio sits at 0.9003 to 0.9048, retiring 50.63% more instructions on the basis for 35.62 to 36.29% more time, where Run 40's trio sat at 0.8669 to 0.8691 on the same instruction ratio --- which is the basis half's `bq-expand` move again; the `list` trio at 0.9992 to 1.0068, cashing all of what it saves; and the ten others between 0.9438 and 0.9682, retiring 3.83 to 5.49 percent more on the basis while their clocks run from 0.47 of a point below level to 0.53 above. **Read per class the same way, the rate runs 0.44 to 0.88**: the instruction saving reaching the clock is lowest on `scaled`, where the counted work parts by 15.24 points and the clock by 6.77, and highest on `window`, 17.76 against 15.55 --- where Run 40 read 0.37 to 0.78, Run 39 0.43 to 0.76 and Run 38 0.38 to 0.73, so [the open question][open] on that rate reads a wider range than any of the three before it, `window`'s top end carrying the basis half's `bq-expand` move, 10% on that class.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0001** and **1.0000** on the two halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0327** and **1.0964** on the basis and **1.0208** and **1.0775** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs two to three percent over the term it stands for on `mut-odo-vecdims` and about ten and eight on `bq-expand`. So the two passes do not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1172** on the basis and **1.1601** on the control, **4.3** points apart, where Run 40's two parted by 4.7, Run 39's by 4.2 and Run 38's by 4.3 --- so the two passes change what the spray costs a process as well as what the roster costs it, by within a point of what they changed it by on each of the three runs before. What the roster adds on top of that state is **1.0183** on the basis, 5 of 19 shapes above 1, and **1.0205** on the control, 14 of 19; the basis's rest runs 0.9823 on `stretch-bigstride` to 1.2157 on `stretch-r5-8x432`, the control's 0.9838 on `stretch-bigstride` to 1.1053 on `stretch-inner256`. The whole in-process deflation is **1.1377** on the basis, 17 of 19 shapes above 1, and **1.1838** on the control, 19 of 19.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 40's, both recipes unchanged to the character and rebuilt on `Main.hs` at `688e952` where Run 40 built from `bb6b12e`, on the owner's word of 2026-09-25 that this run uses the previous run's recipes and benchmarks the changed source: both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, `align-as.py` at `1a359bd` where Run 40's took `fe6d133`, under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run41-gheadnospec` and `run41-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 40's with the builddir names moved. So the pair's own `cross` figure is the two passes read a sixth time, in `--compare`'s orientation of the unflagged basis over the control, and the source and the shim are read as each half against Run 40's same half, `--half-movers run41 run40`. The shim moved under both halves alike: `1a359bd` has the settled cost's off-plan test decide on the first tier differing past its tolerance where the whole padded tuple decided, so a group the pad had moved is planned again, which reaches placement and not what any arm executes. The fifteen commits move one arm out, the one-level fill's, and one class view, `runs-3`, and none in --- `./roster-delta.py run40-gheadnospec run41-gheadnospec` reads the other 30 arms in the same order --- and `./registration-drift.py run41 --since run40` reaches no code behind `list`, `bq-expand` or any `mut-odo-vecdims` arm. What retiring `runs-3` owes this run's write-up, the class counts dropping a retired view, is in the open entry on what the roster owes the next run. What they change behind the four lean arms, read off the diffs: `lib-stage2-lean`'s fill, `fillStage2Axes`, is now a copy of `fillStage2`'s nest in place of the outermost-first odometer (`fd34ce1`), and its merge a strict record (`815ffa2`); `lib-stage3-lean` runs that same nest algorithm as `fillStage3`, its nest built in a loop, behind a dispatch and merge of its own over `Axis` that drop extent-1 axes before merging (`c7e5ba2` to `688e952`); `lib-stage2-lean-u1` changes in that strict merge alone, `fillStage2U1` being unmoved but for a rename; and `lib-stage1` executes the code it did. **The items' priors are instruction counts off this run's own basis binary**, `run41-gheadnospec`, taken with `probe-stalls.sh` at `N=25`, half the N of Run 40's counts on the owner's word of 2026-09-26, over all nineteen main-set shapes for the four arms the items read, twice, into `probe-r41-prior1.txt` and `probe-r41-prior2.txt`, whose instruction ratios agree to three decimals and whose every nonlinear cell is a cycles cell. They are read RAW, the sweeps carrying no `sum-only` arm for `--counts` to correct with, as Run 40's priors were quoted. Against `run40-counts-gheadnospec.txt`, `mut-odo-vecdims-add-in-leaf-u2`'s instructions a call read within 0.1% of Run 40's on sixteen shapes and 0.57 to 1.27 points above on three, `cnn-L2-24x24-c32`, `stretch-primes` and `stretch-coprime-r7`, where `lib-stage3-lean` and `lib-stage2-lean-u1` carry the same excess to within 0.03 of a point, a term the three arms share and no commit explains; that is what makes `-u2` the denominator. The cycles the files carry are no prior: at `N=25` three cells on `cnn-slice-c32` read negative, so no cycle figure is quoted below. No probe was taken on the control's recipe, so the priors are the basis's, carried to the control on Run 40's two halves agreeing to within a point on each pair below. **The limit this run cannot remove**: a rebuild moves every loop, and the chapter has put eight clauses that a reordering cannot reach a population to the test in time and seen all eight fail, so no item predicts an untouched arm's TIME across runs; the untouched arms stand in the items as within-half denominators instead.

(1) *With one fill algorithm under both, `lib-stage3-lean`'s lead over `lib-stage2-lean` closes.* In `probe-r41-prior1.txt`, lean3 over lean2 in instructions runs from 0.991 on `cnn-slice-c32` to 1.000, a geomean of 0.9990 over the nineteen, where `run40-counts-gheadnospec.txt` reads 0.9751; lean2's own instructions a call fall to 0.845 to 1.006 of Run 40's, a geomean of 0.9748, while lean3's read a geomean of 0.9988, the commits taking 2.5 and 2.0 points off `cnn-L1-6x6-c1` and `cnn-slice-c32`. Run 40 read the pair in time at 0.9656 on the basis and 0.9564 on the control, `./read-run.py run40-gheadnospec-main.json --pair lib-stage3-lean lib-stage2-lean` and its control twin, its two fills then differing in algorithm; what is left between them is the `Axis` dispatch and merge and the loop-built nest, a tenth of a point of instructions. `predict: pair lib-stage3-lean lib-stage2-lean 1.00 within 2% on main both`. A reading below 0.98 says the `Axis` path buys time its instructions do not show, or that the copy is not the fill it copied; one above 1.02 says the path costs time its instructions do not show.

**Read by --predictions, item (1):** `pair lib-stage3-lean lib-stage2-lean 1.00 within 2% on main both`: HELD on main basis, read 0.9904 over 19 shape(s), 0.96 point(s) off, within 2.00%; HELD on main control, read 0.9948 over 19 shape(s), 0.52 point(s) off, within 2.00%.

(2) *The unroll alone costs `lib-stage2-lean-u1` against `lib-stage2-lean` what it cost against the nest on Run 40.* The two arms now share the route and the strict merge and differ in the fill, the nest against its unrolled twin, which is the difference Run 40's u1 over lean3 read. In `probe-r41-prior1.txt`, u1 over lean2 in instructions runs from 0.956 on `stretch-wide-2xM` to 1.035 on `stretch-bigstride`, a geomean of 1.0206, where `run40-counts-gheadnospec.txt` reads u1 over lean3 at 1.0206 raw, `--counts --pair lib-stage2-lean-u1 lib-stage3-lean` on Run 40's main JSON. Run 40 read that pair in time at 1.0575 on the basis and 1.0617 on the control, `--pair lib-stage2-lean-u1 lib-stage3-lean` on the two main JSONs. `predict: pair lib-stage2-lean-u1 lib-stage2-lean 1.06 within 3% on main both`. A reading above 1.09 says the copy runs faster than the nest it copied, or the strict merge favours the nest's side; one below 1.03 says the unroll's cost moved with the rebuild, which the counts sweep then has to show is not in the instructions.

**Read by --predictions, item (2):** `pair lib-stage2-lean-u1 lib-stage2-lean 1.06 within 3% on main both`: HELD on main basis, read 1.0601 over 19 shape(s), 0.01 point(s) off, within 3.00%; HELD on main control, read 1.0638 over 19 shape(s), 0.38 point(s) off, within 3.00%.

(3) *With the nest frozen into its fill, `lib-stage2-lean` takes over the lead `lib-stage3-lean` held on the untouched `-u2`.* In `probe-r41-prior1.txt`, lean2 over `mut-odo-vecdims-add-in-leaf-u2` in instructions runs from 0.704 on `cnn-L1-6x6-c1` to 0.978 on `stretch-wide-2xM`, a geomean of 0.9251, where `run40-counts-gheadnospec.txt` reads 0.9501 for lean2 and 0.9264 for lean3, `--counts --pair` raw on Run 40's main JSON. Run 40 read lean2 over `-u2` in time at 0.9307 on the basis and 0.9322 on the control and lean3 over `-u2` at 0.8987 and 0.8916, `--pair` on the two main JSONs, lean3's time ratio 1.40 times its instruction ratio in logarithms on the basis, which carried to 0.9251 gives about 0.897. `predict: pair lib-stage2-lean mut-odo-vecdims-add-in-leaf-u2 0.90 within 3% on main both`. A reading above 0.93 says the copy did not bring the nest's time with it, Run 40's lean2 figure; one below 0.87 says the strict merge bought more than its instructions.

**Read by --predictions, item (3):** `pair lib-stage2-lean mut-odo-vecdims-add-in-leaf-u2 0.90 within 3% on main both`: HELD on main basis, read 0.8911 over 19 shape(s), 0.89 point(s) off, within 3.00%; HELD on main control, read 0.8938 over 19 shape(s), 0.62 point(s) off, within 3.00%.

(4) *The regime's worth on the two families no commit touched holds at the level of the earlier draws, the shim's change being shared.* `list` and `bq-expand` run no code any of the fifteen commits changed, and `1a359bd` is under both halves, so their cross figures are the pair's variable on a sixth build: `--record regime` reads `list` over the nineteen shapes at 1.2960, 1.2889, 1.2966 and 1.2983 on Runs 37 to 40's builds, inside 0.94 points, with Run 36's 1.3360 above them, and `bq-expand` at 1.2980, 1.3101, 1.3032, 1.2985 and 1.3058 on Runs 36 to 40's, inside 1.21. `predict: cross list 1.295 within 1% on main basis`, the four later draws' mean, and `predict: cross bq-expand 1.303 within 1% on main basis`, the five draws' mean. A reading outside either band on unchanged code says the regime's worth moved with the build or the shim and not with the source, which makes items (1) to (3) harder to read.

**Read by --predictions, item (4):** `cross list 1.295 within 1% on main basis`: HELD on main basis, read 1.2926 over 19 shape(s), 0.24 point(s) off, within 1.00% --- `cross bq-expand 1.303 within 1% on main basis`: KILLED on main basis, read 1.3620 over 19 shape(s), 5.90 point(s) off, within 1.00%.

**Items (1) to (3) hold their sentences whole, on every span on every half each names, and item (4) SPLITS: `list` holds and `bq-expand` is killed.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set on each half and by `--pair` with `--counts` for the instructions.

(1) *With one fill algorithm under both, `lib-stage3-lean`'s lead over `lib-stage2-lean` closes.* **HELD on both halves.** The pair reads **0.9904** on the basis and **0.9948** on the control, inside 2% of 1.00 and clear of both ends the item named --- above the 0.98 that would say the `Axis` path buys time its instructions do not show, and under the 1.02 that would say it costs time. The instructions came out as the prior said, **0.9990** raw on the basis against the prior's 0.9990, 0.9984 net of the forcing pass, so the lead Run 40 read at 3.4 and 4.4 points has closed to under one; what is left, 0.96 of a point on the basis and 0.52 on the control, is more than the 0.16 and 0.10 of a point of net instructions the path saves, and inside half the item's band.

(2) *The unroll alone costs `lib-stage2-lean-u1` against `lib-stage2-lean` what it cost against the nest on Run 40.* **HELD on both halves.** The pair reads **1.0601** on the basis and **1.0638** on the control, inside 3% of 1.06 and clear of both ends --- under the 1.09 that would say the copy runs faster than the nest it copied, and over the 1.03 that would say the unroll's cost moved with the rebuild --- beside Run 40's 1.0575 and 1.0617 for u1 over the nest. The instructions came out as predicted, **1.0205** raw on the basis against the prior's 1.0206; net of the forcing pass the excess is 4.72% on the basis and 4.74% on the control, and the time excess runs past it on both halves, at 1.27 and 1.35 of it, where Run 40 read 1.22 and 1.30.

(3) *With the nest frozen into its fill, `lib-stage2-lean` takes over the lead `lib-stage3-lean` held on the untouched `-u2`.* **HELD on both halves.** The pair reads **0.8911** on the basis and **0.8938** on the control, inside 3% of 0.90 and clear of both ends --- under the 0.93 that would say the copy did not bring the nest's time with it, and over the 0.87 that would say the strict merge bought more than its instructions --- where Run 40 read lean2 over `-u2` at 0.9307 and 0.9322 and lean3 over it at 0.8987 and 0.8916. The instructions came out as predicted, **0.9251** raw on the basis against the prior's 0.9251, 0.8694 and 0.8703 net on the two halves, of which the clock takes 83% and 82%. The term the prior found under all three arms on three shapes, `-u2`'s instructions a call 0.57 to 1.27 points above Run 40's at `N=25`, is absent from the run's own sweep at `N=50`, which reads `-u2` at Run 40's count to the fourth decimal on all three.

(4) *The regime's worth on the two families no commit touched holds at the level of the earlier draws, the shim's change being shared.* **SPLIT: `list` HELD and `bq-expand` KILLED.** `list` reads **1.2926**, 0.24 of a point off 1.295, a sixth draw inside the 0.94 points the four before it kept. `bq-expand` reads **1.3620**, 5.90 points off 1.303, where its five earlier draws kept 1.2980 to 1.3101 --- a reading outside its band on code no commit changed, which the item said would be the build or the shim and not the source. **It is the BASIS half's `bq-expand` and not the pair**: against Run 40's same half the basis runs the family 3.9 to 4.3% slower on the main set, 1.0385 to 1.0428, with its instructions a call level to the fourth decimal, while the control reads it within a quarter of a point of Run 40's control; the same family moves on the basis by 3.0 to 10.2% on `rev`, `bcastmid` and `window` too, its widest cell in each population a shape of `sInner` 3, and past 3% on no population on the control. Items (1) to (3) read pairs of fills within one half, none of them a `bq-expand` arm, so the kill does not reach them. **The copy test, taken 2026-09-26 on a quiet box after the evening, says the move is this BUILD**: on the four widest cells a fresh copy of `run41-gheadnospec` reads 0.996 to 1.013 of the timed file, and Run 40's basis runs them at 0.883 to 0.906 of it in fresh processes.
