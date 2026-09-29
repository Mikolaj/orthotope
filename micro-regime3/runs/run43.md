# Run 43 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach. The words it uses and the bars it reads against --- a point, the sign of a ratio, a strategy, a family, the plateau, and which bar answers what --- are defined once in [README's *Reading a run file*](../README.md#reading-a-run-file).

**Run 43 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source, launched from disk): the two passes are worth some twenty-nine and a half points on `list` and thirty-two on `bq-expand`, ALL ELEVEN registered spans hold, and the six source commits moved no timed arm's instructions and no arm's clock by more than a point on the main set.** The pair is Runs 36's to 42's IN ITS VARIABLE --- one source, `Main.hs` at `e29cdf2`, one shim at `1a359bd` under five switches with the exit span and the settled cost, ONE compiler, `10.1.20260918`, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the sixteen main-set arms that carry a cross-half figure, SIX move with the families and TEN do not: the six are the `list` and `bq-expand` families entire, at **1.2939** to **1.3249**, and the ten others span **0.9961** to **1.0058**. **The bar an arm has to clear to be the passes' rather than the run's is 0.28 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.79% on the basis and 0.60% on the control and measured WITHIN one half --- and five of the eight arms that are not A/A copies clear it: the two families, `lib-stage1` at 0.9961, the basis the faster, and `lib-stage2-lean-u1` and the shipped leaf at 1.0058 and 1.0053, the control the faster, all three by under 0.6 of a point.

**What this run was built to settle is whether the six commits left each fill where Run 42 read it, and all eleven spans hold on every half they name, the instructions of every timed arm unmoved.** `lib-stage2-lean-u1` over `lib-stage3-lean` reads **1.0662** on the basis and **1.0628** on the control, where Run 42 read 1.0690 and 1.0654; `lib-stage3-lean` over `lib-stage2-lean` **1.0066** and **1.0044**, level; `lib-stage1` over the shipped leaf **0.9928** and **1.0021**; and the shipped leaf over `mut-odo-vecdims` **0.6416** and **0.6380**, the fusion untouched by the bangs of `0a20749`. Grown to 1.8 million elements, `libunord-stage15-sum` over stage fourteen reads **0.67** on `compose-bcast-wide` and **1.04** on `compose-bcast-nest` on the basis and 0.66 and 1.06 on the control, where at 4992 elements Run 42 read 0.37 and 2.02, the wide view's time now following its cycles and not its instructions; and the regime's worth reads `list` at **1.2950** against 1.294 within 1% and `bq-expand` at **1.3212** against 1.305 within 2% ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)).

**One process met foreign CPU and its population was rerun, and the rerun showed a process term on `bq-expand` the size of a build term.** One bench of the basis's first main-set process read 0.77 of a core foreign, and on the owner's word both halves of `main` were rerun on a quiet box the same day, every main-set figure here being the rerun's; the rerun of the same two binaries reads the basis half's `bq-expand` family 1.5 to 1.7 points slower than the first process and every other arm within 0.72 of a point, which is what puts the family 1.1 to 1.6 points over Run 42's basis while its instructions read level ([Provenance](#provenance)). The machine check read `list` inside the bars and no reboot sits between this run and Run 42. The control's four `flip` movers against Run 42 are Run 42's own fast file instance gone, reading level with Run 41's control; its `lib-stage1` on `small` reads slower a second run running with its counts level, and the copy test that would place it was not taken ([Results](#results)).


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE alone**: the compiler is Runs 36's to 42's in-tree stage1 `10.1.20260918` unmoved, and the project file `cabal.project.ghead`, the shim `align-as.py` at `1a359bd` with its five switches, the regime and the launch from disk are Run 42's. What moved is `Main.hs`, from `eb76398` to `e29cdf2` in six of the owner's commits, which brought no arm in and took none out and grew two `compose` views to `sizeCap`, with `micro.cabal` taking orthotope's warning flags beside them. **Read against the half Run 42 built by this same recipe, the six commits moved no arm by more than a point on either half, and the one family that moved further is the one no commit reached**, the basis's `bq-expand` family, whose 1.1 to 1.6 points are this run's second main-set process and not its build, which [What the next run compares against](#what-the-next-run-compares-against) gives arm by arm. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run43-gheadnospec`, as every published table here is from Run 13 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **NONE of the thirty-one rows is a first reading**: every one is Run 42's, in Run 42's order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every row has a twin in Run 42's file.

**Comparing runs?** The table below is Run 43's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.79%** from 1 on the basis half or **0.60%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one part on BOTH halves this run**: over the four pairs that carry back to Run 10 the two halves read **0.64%** and **0.35%**, `bq-expand-aa-distant` carrying both, where `mut-odo-vecdims-add-in-leaf-u2-aa-distant` carries the whole-set figure on both. The main-set figures are the rerun's, taken on a quiet box after the evening, the first basis process having met foreign CPU ([Provenance](#provenance)). Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **3.89%** on `alexnet-L1-55-c3-k11` on the basis and **2.35%** on `stretch-bigstride` on the control --- are not floors at all and are not to be quoted as any. Its two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *54* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.66 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage15-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage fourteen's route with the zero-stride axis consed just outside the run |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.43* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.03* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.024 | 0.113 | 0.60 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.113 | 0.48 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage1 | 0.025 | 0.113 | 0.49 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| lib-stage2-lean-u1 | 0.025 | 0.111 | 0.75 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.112* | *0.56* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.113* | *0.51* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.113 | 0.51 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` was a port of until 2026-09-11 |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.40* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.39* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.112 | 0.32 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.130 | 0.261 | 0.67 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.130* | *0.261* | *0.69* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.131* | *0.261* | *0.31* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.76 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.010* | *0.67* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.002* | *1.010* | *0.45* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run THREE of the 105 pairs among the timed arms other than `list` part in SIGN between the two statistics on the basis and SEVEN on the control, `--winsor` printing each. **The cap moves seven rows on the basis**, `lib-stage1` with 4 of 19 cells capped, `lib-stage2-lean` with 2 of 19 cells capped, `lib-stage2-lean-u1` with 3 of 19 cells capped, `lib-stage3-lean` with 2 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2` with 4 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2-aa` with 4 of 19 cells capped, `mut-odo-vecdims-add-in-leaf-u2-aa-distant` with 4 of 19 cells capped, their published figures sitting 6.0 to 12.8 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms. **The widest disagreement of any kind on the basis** is `bq-expand` over `lib-stage1`, which divides to **5.2000** on the column where the paired figure is **4.5357**, the column +14.6% off it. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads 13 of the 16 rows moved against Run 42's table, where what says how far an ARM moved is `--compare` against the JSON of the half Run 42 built.

**This run's two columns may be differenced on NONE of the eleven populations, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **29.50 points** on the main set and by 25.04 on `bcastmid` to 35.90 on `bcast` over the ten classes, every one of the figures past the bar by a factor of 35 or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's.

`concat-runs` has no row, and neither do the other 82 arms the roster holds and checks without timing --- **83 of its 114** in all: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). `roster-delta.py`, read off the two binaries, reads 31 arms to 31 over 19 shapes to 19 and the class views 62 to 62; every arm, main-set shape and class view in Run 42's order, the six commits having moved no name on or off the roster and grown two `compose` views under their names instead (`aa18c24`). A movement against Run 42's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a source term between the two runs and no shim, compiler, boot or launch term, nor a project-file term that reaches the code, `micro.cabal`'s move being warning flags alone --- and a movement across THIS run's two halves is the pair's own variable, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table prints the two lean fills level at 0.024**, `lib-stage3-lean` ahead of `lib-stage2-lean` by two in the fifth decimal, with `lib-stage1` and `lib-stage2-lean-u1` at 0.025 and the shipped leaf at 0.027 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result. **Paired on the basis the head is a tie between the two lean fills and a lead over the rest**: `lib-stage3-lean` over `lib-stage2-lean` is **1.0066** at 9 of 19 and p 1, which is registration item (1) holding and which the printed column orders the other way, the cap moving the two rows apart; and `lib-stage2-lean` over the shipped leaf **0.8809** at 16 of 19 and over `lib-stage1` **0.8873** at 15 of 19 --- so the two lean fills lead `lib-stage1` and the shipped leaf by eleven to twelve points, as on Run 42. **The third, read across the halves, is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6416** on the basis and **0.6380** on the control, 0.36 of a point apart on a pair that moves `list` by twenty-nine points, both inside the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 --- a span carried from that file and not re-derived here.

**The six commits moved no timed arm's instructions on the main set, and no arm's clock by more than a point on either half.** Against Run 42's basis, the same recipe on `eb76398`, every timed arm's instructions an iteration read 1.0000 of Run 42's to the fourth decimal on the basis and on the control, `lib-stage1` at 1.0001 the widest, which is registration item (1)'s premise read on the run; and the clock moves under a point on every arm outside the `bq-expand` family, from **0.9974** on `list-aa-adjacent` to **1.0093** on `lib-stage3-lean` on the basis and from **0.9942** on `list` to **1.0039** on the shipped leaf on the control. **The `bq-expand` family reads 1.1 to 1.6 points slower on the BASIS half alone, and that is this run's own second process**: the basis's first main-set process, the one [Provenance](#provenance) finds foreign CPU in on another shape, read the family at 0.9964 to 0.9984 of Run 42's, and the rerun of the same binary reads it at 1.0147 to 1.0173 of that first process, every other arm within 0.72 of a point of it --- so a process term on this family is the size of the build term Run 41 drew on it, and a cross-run figure on `bq-expand` under two points reads the process as much as the build.

**The half-local movers against Run 42 are five, all on the control and all with their counts level, and four of them are Run 42's own file instance gone.** `--half-movers run43 run42` flags five arm-populations past 3%, each on ONE half and none on both, none on the main set. **Four are on `flip`**: the control's `lib-stage2-lean`, `mut-odo-vecdims`, `mut-odo-vecdims-aa` and `mut-odo-vecdims-aa-distant` 3.3 to 3.8% SLOWER than Run 42's control, widest on `flip-last-rows` at 1.17 to 1.19, their counts at 1.0000 --- the arms Run 42 read FASTER than Run 41 on the same cell, which its copy test gave to that run's control FILE INSTANCE; against Run 41's control the four read 0.9877 to 1.0034, so the term went with Run 42's file and this run's control reads where Run 41's did. **The fifth is the control's `lib-stage1` on `small`**, 3.3% slower on counts of 0.9989 and widest on `small-bcast32` at 1.08, where Run 42 flagged the same arm on the same half 4.4% slower on counts up 2.5%, so the arm has read slower two runs running, 7.8% over Run 41's control now, the second time with its instructions level. A mover with its counts level is that half's binary, its file instance or its process and not the pair's variable, and **the copy test that tells those apart was not taken**: the note's `QUIET-AFTER:` line reads `ask`, the owner granted the quiet box for the main-set rerun alone, and the test is recorded as owed in [the open list][open]. **Step 4b's cells read as Run 42's did**: ranked by time over counts, the twenty widest cells of the 2511 are all `bq-expand-nosum`, whose counts the two passes move by 37 to 40% on cells where its clock moves by at most three and a half points, and the count-led cells are led by the `bq-expand` family's, whose counts the passes move by up to 132%.


## What the next run compares against

**Run 43's pair is Run 42's rebuilt on the changed source, [registered 2026-09-29](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of 2026-09-29, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; [the standing rulings from past runs](../README.md#standing-rulings-from-past-runs) are NOT that site either. What this run leaves as the reference is `run43-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `e29cdf2`, the shim at `1a359bd` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under, and its main-set column is the quiet rerun's. **It is another published basis on that compiler, and the step from Run 42's is the source and nothing else**: against `run42-gheadnospec`, the same recipe on `eb76398`, thirteen of the sixteen timed arms both runs carry read within 1.1 points of 1 by `--compare`, paired per shape, and three do not --- the `bq-expand` trio at **1.0113** to **1.0157**, below 1 meaning this run is the faster, `--bridge` putting no arm outside the 3.3% drift band it prints, Run 11's. **The trio's step is this run's second process and not its build**: the first basis process read it at 0.9964 to 0.9984 of Run 42's, and the rerun of the same binary moved the family alone ([Results](#results)). **The pair itself is Runs 36's to 42's, built again**, and its draws are `./read-run.py --record regime`'s, a row per build: on `list` this one lands among the seven before it, and on `bq-expand` it lands above the six draws that are not Run 41's. Against Run 31's whole-level **1.2974** the seven later `list` draws straddle the level, so **the level's other passes still do not measurably hand `list` back**. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918`, as Runs 36's to 42's were --- and the step this run reads is not a compiler step at all.** **What this run adds is another build of the pair, on a source six commits on**: Runs 36 to 43 are the same two recipes on the same compiler, Runs 39's to 43's with the settled cost on both, and their cross-half readings agree to 0.94 points on `list` over the seven draws after Run 36's, this run's 1.2950 inside them, while `bq-expand` reads 1.3212, 1.11 points over the 1.2980 to 1.3101 its six draws before and after Run 41's kept and under Run 41's 1.3620 --- and this run's own first main-set process read it at 1.3105, inside that spread, the rerun of the same two binaries moving the basis half's family by 1.5 to 1.7 points ([Results](#results)). That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim and the source together --- and on `bq-expand` one draw has broken the bound, and what this run adds is that a second process of one build moves the family further than the builds after Run 41's did. Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s eight build rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and on the eighteen shapes left without Run 36's wild cell, where Run 36 read above the level, the seven later HEAD draws straddle it, this run's 1.2943 under it.

**What Run 43 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 42 and this run, and the gate says the box still measures as it did, the machine check reading `list`'s net inside the bars against the fingerprint Run 42 installed ([Provenance](#provenance) gives the figures). **This reading carries a source term and nothing else**: Run 42's basis is this basis's recipe on `eb76398`, and `list` runs no code the six commits changed, so `list` holding level says the rebuild left `list` where it was. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 43's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **All eleven spans held, on every population and half their scope names**, on the main set's quiet rerun as on its first processes, and the priors behind items (1) to (3) were instruction counts, cycles and bytes off this run's own basis binary, taken before preflight on a quiet box. **What a next registration should take from this one is that a cross figure on `bq-expand` carries a process term the size of a build term**: item (4)'s `bq-expand` span read 1.3105 on the first basis process and 1.3212 on the rerun of the same binary, both inside its 2% band, and a band set from the spread of builds alone is set too narrow by about that much.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 43**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918`, on `Main.hs` at `e29cdf2` with the shim at `1a359bd`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 42 published a HEAD half on this basis's recipe, so the two published columns carry no compiler or shim term, only the source. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9974** on `list-aa-adjacent` to **1.0157** on `bq-expand-aa-distant`, below 1 meaning this run is the faster, as the first paragraph of this section breaks down. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 43 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918) | Run 43 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.027** | 0.032 |
| `lib-stage1` | **0.025** | 0.032 |
| `lib-stage2-lean` | **0.024** | 0.030 |
| `lib-stage2-lean-u1` | **0.025** | 0.033 |
| `lib-stage3-lean` | **0.024** | 0.030 |
| `bq-expand` | **0.130** | 0.127 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on six of the seven rows, the control higher on each of those six, while `bq-expand` prints 0.130 and 0.127, the one arm whose own move outpaces the denominator's; in absolute terms the flagged half is the faster on twelve of the sixteen timed arms, `--compare` putting the other four, `lib-stage1` and the `mut-odo-vecdims` trio, at 0.9961 to 0.9996, and five of the eight arms that are not A/A copies clear the 0.28-point bar that comparison prints: `list` and `bq-expand`, the two families the passes reach, `lib-stage1` on the basis's side, and `lib-stage2-lean-u1` and the shipped leaf on the control's, the last three by under 0.6 of a point, where on Run 42 three fills cleared a 0.38-point bar. **Read DOWN a column and the head is the two lean fills**, `lib-stage3-lean` and `lib-stage2-lean` level at 0.024 on the basis, and `lib-stage2-lean` at 0.030 on the control with `lib-stage3-lean` level with it to three decimals; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, every published table but the two-column one being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over the main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6380** (0.6416); `lib-stage1` against `mut-odo-vecdims-add-in-leaf-u2` **1.0021** (0.9928); `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2` **0.8852** (0.8809); `lib-stage2-lean` against `lib-stage1` **0.8834** (0.8873); `lib-stage3-lean` against `lib-stage2-lean` **1.0044** (1.0066); `lib-stage2-lean-u1` against `lib-stage3-lean` **1.0628** (1.0662); `bq-expand` against `mut-odo-vecdims` **2.1860** (2.8893). **Six of the seven hold their direction across the halves** by the paired figure, each of the six besides the headline pair moving under a point; the seventh is `lib-stage1` against the shipped leaf, which sits either side of 1, 0.93 of a point apart, both inside item (1)'s band, and the headline pair moves by 70.3 points, the pair's own variable. **`lib-stage2-lean` leads the shipped leaf by about twelve points on both halves**, as on Runs 41 and 42, and `lib-stage3-lean` is level with it, at sign p 1 on both halves.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.3 us | 0.079 | `lib-stage2-lean` 0.044 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.55 us | 0.089 | `lib-stage2-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 118 us | 0.064 | `lib-stage2-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 388 us | 0.043 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `gather48-src-50` | 3 | 22500 | 458 us | 0.049 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.1 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.69 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `stretch-primes` | 89 | 250357 | 4.37 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 16.9 ms | 0.040 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.7 ms | 0.053 | `lib-stage1` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.8 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `stretch-inner256` | 256 | 1750784 | 44.5 ms | 0.023 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.3 ms | 0.112 | `lib-stage2-lean-u1` 0.111 | `mut-odo-vecdims` 0.112 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.7 ms | 0.022 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 31.1 ms | 0.086 | `lib-stage3-lean` 0.073 | `mut-odo-vecdims-add-in-leaf-u2` 0.077 |
| `stretch-bigstride` | 3 | 1800000 | 50.7 ms | 0.033 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.8 ms | 0.058 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41.2 ms | 0.020 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims` 0.020 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.6 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 933 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.4 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35 ms | 0.016 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.2 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.63 ms | 0.053 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.25 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.7 ms | 0.034 | `lib-stage2-lean-u1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42 ms | 0.022 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.22 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.28 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-page` | `block` | 64 | 131072 | 2.36 ms | 0.030 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.5 ms | 0.020 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 936 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 933 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-bcast-nest` | `compose` | 6 | 1800000 | 33.3 ms | 0.036 | `lib-stage3-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-bcast-wide` | `compose` | 120 | 1800000 | 48.2 ms | 0.012 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.010 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.3 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.8 ms | 0.019 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.3 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.66 ms | 0.053 | `lib-stage3-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.2 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 29.8 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.5 ms | 0.047 | `lib-stage2-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 118 us | 0.064 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 459 us | 0.048 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.44 ms | 0.025 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.3 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.5 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.6 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 28.8 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 29.1 ms | 0.024 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-7` | `runs` | 7 | 1799994 | 32.6 ms | 0.033 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-2` | `runs` | 2 | 1800000 | 39.6 ms | 0.058 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-32` | `runs` | 32 | 1800000 | 30 ms | 0.025 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.4 ms | 0.040 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.7 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.3 ms | 0.038 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.6 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 32 ms | 0.030 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 29.4 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.3 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 267 us | 0.029 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.03 ms | 0.023 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.12 ms | 0.029 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.029 |
| `small-patch-k5` | `small` | 5 | 150 | 2.92 us | 0.077 | `lib-stage3-lean` 0.040 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.39 us | 0.050 | `lib-stage3-lean` 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.044 |
| `small-flat64` | `small` | 64 | 256 | 4.39 us | 0.059 | `lib-stage3-lean` 0.006 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.29 us | 0.089 | `lib-stage2-lean-u1` 0.050 | `mut-odo-vecdims-add-in-leaf-u2` 0.069 |
| `small-row96` | `small` | 96 | 384 | 6.43 us | 0.041 | `lib-stage3-lean` 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 280 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 957 us | 0.086 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.45 ms | 0.052 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.58 ms | 0.051 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.88 ms | 0.051 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.6 ms | 0.052 | `lib-stage1` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage2-lean` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.032 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 42 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the ELEVEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FIFTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside vecdims` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names three different `lib-` arms --- `lib-stage2-lean` on FIVE rows, `lib-stage3-lean` on four and `lib-stage1` on one, where Run 42 gave the lean fills the other way about, three of its rows now naming another arm. The cross-class summary's `best outside vecdims` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 43's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in every population it reads, as on Runs 36 to 42 and at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9901**, where the control reads **0.9827** on `stretch-pow2stride`. Every other shape of every population reads the clause with room, the classes' closest cells at 0.30 to 0.48 on the basis. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw, and further under it than its 0.79% floor, the lowest basis draw of Runs 36 to 43. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, the WIDER statement this class set is read for --- that no arm the library would ship is slower than `list` on any shape: **two timed non-control cells of 1134 are slower than their own shape's `list`**, both `lib-stage1` on `runs-2`, the stage-one route as it shipped, whose fill since `c7549d2` is `fillStage3` behind a `walkAx` conversion and so no longer the library's own --- the two cells Runs 41 and 42 read: `lib-stage1` on `runs-2` on the control at **1.3431**; `lib-stage1` on `runs-2` on the basis at **1.0874**. **It is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0101 between the halves while `list` moves 1.2476.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits at or under 0.05268. The `bq-expand` clause is closest at `small-row96` at 1.00441 on the control, then `scaled-rank1-m1` at 1.00003 on the basis, then `scaled-rank1-m1` at 1.00003 on the control, then `stretch-tall-Mx2` at 1.00000 on both halves of the main set. **Those figures are Runs 36's to 42's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, no commit having rewritten code behind `bq-expand` or `list`. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in the ten classes, on both halves --- and their LEVEL clause BREAKS in ten of the ten classes.** `bq-expand` sits between 1.00x and 3.86x the result vector and `list` at 19.00x to 27.66x, on both halves and in every class. On the main set `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the main-set shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 42's to the fourth decimal.

**AND ONE ARM OUTSIDE THE TWO FAMILIES MOVES, `libunord-stage13-sum`, by 3.1 points, as on Run 42.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.9686** of the basis on `libunord-stage13-sum`, where Run 42 read 0.9687; `-stage6-sum`, `-stage6-loop-sum`, `-stage7-sum` and `-stage9-sum` read 1.0000 to 1.0003, and `-stage14-sum`, `-stage15-sum` and `libunord-stage1-sum` 1.0000 to 1.0006. The fills and ordered consumers read 1.0000 to 1.0016 --- `lib-stage2-lean` at 1.0016 the highest, as on Run 42. **In absolute terms it allocates 320 to 1536 bytes a call on the basis main set**, Run 42's range, and the consumers sit under the 0.01x tier, so no tier moves and no property verdict changes with it. `--alloc` puts 366 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 43 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 25.04 points on `bcastmid` at narrowest and 35.90 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 42, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **160 arm-comparisons, 45 putting the basis faster and 115 slower**, with no degenerate arm excluded, at geomeans from **1.0689** on `compose` to **1.1398** on `window` and extremes of `lib-stage1` at **0.9702** on `compose` and `bq-expand` at **1.5438** on `window`. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **One registration names a class**: item (3)'s three cell spans are `on compose` and are read in that block, every other span being `on main`.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **The bold is the arm outside the vecdims arms on TEN of the TEN rows this run** --- `lib-stage2-lean` on `bcastmid`, `block`, `flip`, `rev`, `runs`, `lib-stage3-lean` on `bcast`, `compose`, `small`, `window`, `lib-stage1` on `scaled`. **The vecdims arms' ceiling is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Runs 39 to 42, and no row's bold sits in the CEILING column. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside vecdims | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.064 | **`lib-stage2-lean`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.25% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage3-lean`** 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.94% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.34% |
| `window` | 8 | 0.051 | 0.086 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.44% |
| `scaled` | 3 | 0.029 | 0.029 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 | 1.34% |
| `runs` | 16 | 0.026 | 0.058 | **`lib-stage2-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.30% |
| `flip` | 6 | 0.028 | 0.053 | **`lib-stage2-lean`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.87% |
| `block` | 5 | 0.023 | 0.030 | **`lib-stage2-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.48% |
| `small` | 5 | 0.061 | 0.089 | **`lib-stage3-lean`** 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 | 0.70% |
| `compose` | 6 | 0.023 | 0.036 | **`lib-stage3-lean`** 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 | 0.44% |

The best arm outside the vecdims arms is ahead of `mut-odo-vecdims` in ten of the ten classes. Three row(s) change the arm they name against Run 42, `block` to `lib-stage2-lean`, `compose` to `lib-stage3-lean`, `runs` to `lib-stage2-lean`. **THREE rows tie at three decimals this run**, `bcast`, `compose`, `rev`, and `block`, `runs`, `scaled` sit a thousandth apart; the `bold` column decides each on the unrounded values.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *126* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.08 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.12 | 148 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.12 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.01 | 157 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 157 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.05 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.01 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage2-lean | 0.021 | 0.025 | 0.09 | 148 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.041* | *0.11* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.041 | 0.09 | 147 | 1.00x |
| lib-stage3-lean | 0.021 | 0.026 | 0.08 | 148 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.041* | *0.08* | *147* | *1.00x* |
| lib-stage1 | 0.022 | 0.040 | 0.07 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-aa* | *0.042* | *0.064* | *0.08* | *138* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.09* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.064 | 0.11 | 138 | 1.00x |
| bq-expand | 0.138 | 0.236 | 0.12 | 122 | 3.22x |
| *bq-expand-aa-distant* | *0.138* | *0.236* | *0.09* | *122* | *3.22x* |
| *bq-expand-aa-adjacent* | *0.139* | *0.236* | *0.14* | *122* | *3.22x* |
| *list-aa-adjacent* | *0.999* | *1.002* | *0.20* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 85 | 26.11x |
| *list-aa-distant* | *1.003* | *1.005* | *0.22* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0025, worst cell 0.53% on `rev-gather48-src-50`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.07% on `rev-primes`, its interval covering 1. The in-situ term reads 1.0052, 1.0137 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0025, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m6s, peak 96 MiB in use, 24 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.59 ms per call raw, 4.44 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.048/0.025

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0991, from `lib-stage3-lean` at 0.9846 to `bq-expand-aa-adjacent` at 1.3067, with `list` itself at 1.2772. **The baseline moved 27.72% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.064, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.021, priced against `mut-odo-vecdims` at 0.4898 over 3 of 3 shapes at sign p 0.25, a margin of 51.02% against this class's 0.25% floor (`list-aa-distant`). Its two columns may NOT be differenced, `list` having moved 27.72 of a point, at a class geomean of 1.0991 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.64 points. The counted work reads a counts geomean of 1.1656 over the same arms, 16 of them counted. Its counted work parts by 16.56 points where its clock parts by 9.91, so about 0.60 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.61* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.47 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.016 | 0.020 | 0.51 | 62 | 1.00x |
| lib-stage2-lean | 0.016 | 0.020 | 0.43 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.48* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.46 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.43 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.50 | 62 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.29* | *61* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.37* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.09 | 61 | 1.00x |
| *bq-expand-aa-adjacent* | *0.092* | *0.143* | *0.69* | *46* | *1.00x* |
| bq-expand | 0.092 | 0.143 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.093* | *0.144* | *0.24* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.15 | 17 | 20.99x |
| *list-aa-distant* | *1.008* | *1.025* | *0.91* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.010* | *1.015* | *0.80* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0094, worst cell 1.51% on `bcast-tall-Mx2`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.06% on `bcast-inner8`, its interval covering 1. The in-situ term reads 1.0206, 1.0126 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0091, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 169 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.4 ms per call raw, 29.4 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.016/0.019/0.019

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0893, from `lib-stage2-lean` at 0.9995 to `list-aa-distant` at 1.3755, with `list` itself at 1.3590. **The baseline moved 35.90% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.016, priced against `mut-odo-vecdims` at 0.6542 over 6 of 6 shapes at sign p 0.031, a margin of 34.58% against this class's 0.94% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 35.90 of a point, at a class geomean of 1.0893 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.21 points. The counted work reads a counts geomean of 1.1697 over the same arms, 16 of them counted. Its counted work parts by 16.97 points where its clock parts by 8.93, so about 0.53 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.33 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.35 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.30 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 97 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *88* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.020 | 0.34 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.021 | 0.31 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.35 | 82 | 1.00x |
| lib-stage3-lean | 0.012 | 0.017 | 0.36 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.28* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.37 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.33* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.28* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.27 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.27* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.100* | *0.183* | *0.44* | *61* | *1.92x* |
| bq-expand | 0.100 | 0.183 | 0.41 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.183* | *0.38* | *61* | *1.92x* |
| *list-aa-adjacent* | *0.997* | *0.998* | *0.66* | *28* | *23.56x* |
| *list-aa-distant* | *0.999* | *1.000* | *0.76* | *28* | *23.56x* |
| list (baseline) | 1.000 | 1.000 | 0.84 | 28 | 23.56x |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 0.9966, worst cell 0.57% on `bcastmid-b200k`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `bcastmid-block150k`, its interval covering 1. The in-situ term reads 1.0165, 1.1182 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9967, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m51s, peak 129 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.8 ms per call raw, 47.7 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0892, from `lib-stage1` at 0.9945 to `list-aa-distant` at 1.2592, with `list` itself at 1.2504. **The baseline moved 25.04% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.012, priced against `mut-odo-vecdims` at 0.4231 over 4 of 4 shapes at sign p 0.12, a margin of 57.69% against this class's 0.34% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 25.04 of a point, at a class geomean of 1.0892 over the 16 arms, with 2 of 8 strategies past an A/A bar of 5.11 points. The counted work reads a counts geomean of 1.1710 over the same arms, 16 of them counted. Its counted work parts by 17.10 points where its clock parts by 8.92, so about 0.52 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.37* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.28 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.17 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.21 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.20 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.04 | 105 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.06 | 105 | 0.02x |
| libunord-stage15-sum | -- | -- | 0.05 | 105 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.10 | 100 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.06 | 102 | 0.02x |
| libunord-stage7-sum | -- | -- | 0.05 | 104 | 0.02x |
| libunord-stage9-sum | -- | -- | 0.06 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.04* | *97* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.027 | 0.23 | 84 | 1.00x |
| lib-stage2-lean | 0.023 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.16 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.029 | 0.20 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.16* | *82* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.18* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.20 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.084* | *0.15* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.051* | *0.084* | *0.14* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.086 | 0.15 | 76 | 1.00x |
| *bq-expand-aa-distant* | *0.178* | *0.218* | *0.29* | *57* | *3.86x* |
| *bq-expand-aa-adjacent* | *0.179* | *0.218* | *0.37* | *57* | *3.86x* |
| bq-expand | 0.180 | 0.218 | 0.36 | 57 | 3.86x |
| *list-aa-distant* | *0.999* | *1.004* | *0.44* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.47 | 30 | 27.66x |
| *list-aa-adjacent* | *1.000* | *1.003* | *0.42* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9956, worst cell 1.23% on `window-224x224-k3-s2`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.13% on `window-224x224-k3`, its interval covering 1. The in-situ term reads 1.0098, 1.2885 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9977, which the correction amplifies by 2.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m30s, peak 128 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.086/0.032/0.052/0.051/0.053/0.052

**Across the halves:** 1 of the 16 arms are faster on this half and 15 slower, at a geomean of 1.1398, from `mut-odo-vecdims-aa` at 0.9936 to `bq-expand` at 1.5438, with `list` itself at 1.2947. **The baseline moved 29.47% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.086, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.4132 over 8 of 8 shapes at sign p 0.0078, a margin of 58.68% against this class's 0.44% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 29.47 of a point, at a class geomean of 1.1398 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.05 points. The counted work reads a counts geomean of 1.1776 over the same arms, 16 of them counted. Its counted work parts by 17.76 points where its clock parts by 13.98, so about 0.79 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.19 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.13 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.19 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.18 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage15-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.17 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.15 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *138* | *0.00x* |
| lib-stage1 | 0.022 | 0.031 | 0.16 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.031* | *0.11* | *128* | *1.00x* |
| lib-stage2-lean-u1 | 0.023 | 0.030 | 0.15 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.023* | *0.030* | *0.14* | *128* | *1.00x* |
| lib-stage3-lean | 0.023 | 0.031 | 0.17 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.031 | 0.12 | 128 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.023 | 0.031 | 0.17 | 128 | 1.00x |
| *mut-odo-vecdims-aa* | *0.027* | *0.029* | *0.10* | *127* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.029* | *0.10* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.029 | 0.23 | 127 | 1.00x |
| *bq-expand-aa-distant* | *0.092* | *0.101* | *0.06* | *111* | *1.21x* |
| bq-expand | 0.092 | 0.101 | 0.07 | 111 | 1.21x |
| *bq-expand-aa-adjacent* | *0.092* | *0.101* | *0.08* | *111* | *1.21x* |
| list (baseline) | 1.000 | 1.000 | 0.16 | 69 | 21.49x |
| *list-aa-distant* | *1.002* | *1.005* | *0.19* | *69* | *21.49x* |
| *list-aa-adjacent* | *1.004* | *1.004* | *0.21* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9866, worst cell 3.65% on `scaled-rank1-m1`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.06% on `scaled-rank1-m1`, its interval covering 1. The in-situ term reads 1.0199, 1.0143 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9940, which the correction amplifies by 2.29x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m8s, peak 111 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.3 ms per call raw, 5.12 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.029/0.029

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0697, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9928 to `list-aa-distant` at 1.3179, with `list` itself at 1.3170. **The baseline moved 31.70% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.8898 over 2 of 3 shapes at sign p 1, a margin of 11.02% against this class's 1.34% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 31.70 of a point, at a class geomean of 1.0697 over the 16 arms, with 3 of 8 strategies past an A/A bar of 1.36 points. The counted work reads a counts geomean of 1.1524 over the same arms, 16 of them counted. Its counted work parts by 15.24 points where its clock parts by 6.97, so about 0.46 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen, and cut to sixteen for Run 41, `runs-3` (`sInner` 3, a k3 conv row) leaving timing in `94aeee7` and staying in `check`.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.53* | *52* | *1.07x* |
| liblist-stage1-sum | -- | -- | 0.10 | 62 | 0.35x |
| liblist-stage4-sum | -- | -- | 0.02 | 75 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.08 | 62 | 0.35x |
| libunord-stage13-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 74 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 75 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *69* | *0.00x* |
| lib-stage2-lean | 0.023 | 0.025 | 0.10 | 60 | 1.00x |
| lib-stage3-lean | 0.023 | 0.025 | 0.11 | 60 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.024 | 0.14 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.50* | *59* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.09* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.025 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.058* | *0.09* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.058 | 0.10 | 59 | 1.00x |
| *mut-odo-vecdims-aa* | *0.026* | *0.058* | *0.08* | *59* | *1.00x* |
| lib-stage1 | 0.085 | 1.087 | 0.18 | 52 | 1.35x |
| *bq-expand-aa-adjacent* | *0.092* | *0.143* | *0.50* | *46* | *1.07x* |
| bq-expand | 0.092 | 0.143 | 0.42 | 46 | 1.07x |
| *bq-expand-aa-distant* | *0.093* | *0.144* | *0.05* | *46* | *1.07x* |
| list (baseline) | 1.000 | 1.000 | 2.48 | 17 | 21.26x |
| *list-aa-distant* | *1.031* | *1.047* | *0.27* | *17* | *21.26x* |
| *list-aa-adjacent* | *1.033* | *1.046* | *0.18* | *17* | *21.26x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0330, worst cell 4.57% on `runs-65536`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.24% on `runs-256`, its interval covering 1. The in-situ term reads 1.0303, 1.0297 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0318, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h43m4s, peak 610 MiB in use, 270 MiB max residency; the reader reads 31 benchmarks over 16 shapes of the runs class. Anchor: `runs-2`, `list` at 40.6 ms per call raw, 39.6 ms net.

**Per shape, in the run's shape order (runs-2, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.058/0.040/0.038/0.033/0.030/0.025/0.025/0.025/0.024/0.024/0.025/0.024/0.024/0.024/0.024/0.025

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0773, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9973 to `list` at 1.3114, with `list` itself at 1.3114. **The baseline moved 31.14% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.058, tiers at 1.00x, 1.07x, 21.26x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.8102 over 16 of 16 shapes at sign p 3.1e-05, a margin of 18.98% against this class's 3.30% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 31.14 of a point, at a class geomean of 1.0773 over the 16 arms, with 3 of 8 strategies past an A/A bar of 0.48 points. The counted work reads a counts geomean of 1.1597 over the same arms, 16 of them counted. Its counted work parts by 15.97 points where its clock parts by 7.73, so about 0.48 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.12 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.12 | 93 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.15 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.10 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.03 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *91* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.022 | 0.041 | 0.20 | 84 | 1.00x |
| lib-stage3-lean | 0.022 | 0.041 | 0.29 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.044 | 0.26 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.37* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.043* | *0.10* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.043 | 0.09 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.053* | *0.09* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.053* | *0.08* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.053 | 0.08 | 77 | 1.00x |
| lib-stage1 | 0.032 | 0.048 | 0.21 | 82 | 1.00x |
| *bq-expand-aa-adjacent* | *0.091* | *0.182* | *0.43* | *61* | *1.05x* |
| bq-expand | 0.091 | 0.182 | 0.46 | 61 | 1.05x |
| *bq-expand-aa-distant* | *0.092* | *0.182* | *0.11* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.66 | 32 | 21.18x |
| *list-aa-distant* | *1.007* | *1.016* | *0.53* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.009* | *1.023* | *0.20* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0087, worst cell 2.34% on `flip-last-rows`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.27% on `flip-last-rows`, its interval covering 1. The in-situ term reads 1.0213, 1.0259 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0084, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.053/0.047/0.026/0.026

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0739, from `lib-stage2-lean-u1` at 0.9950 to `list-aa-distant` at 1.3297, with `list` itself at 1.3075. **The baseline moved 30.75% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.7280 over 6 of 6 shapes at sign p 0.031, a margin of 27.20% against this class's 0.87% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 30.75 of a point, at a class geomean of 1.0739 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.70 points. The counted work reads a counts geomean of 1.1522 over the same arms, 16 of them counted. Its counted work parts by 15.22 points where its clock parts by 7.39, so about 0.49 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.10* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.10 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 129 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.04 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| lib-stage2-lean | 0.020 | 0.023 | 0.11 | 111 | 1.00x |
| lib-stage3-lean | 0.020 | 0.023 | 0.12 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.020 | 0.025 | 0.08 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.11* | *111* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.11* | *111* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.023* | *0.030* | *0.09* | *111* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.030* | *0.10* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.030 | 0.14 | 111 | 1.00x |
| lib-stage1 | 0.049 | 0.057 | 0.13 | 104 | 1.42x |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.10* | *96* | *1.06x* |
| *bq-expand-aa-adjacent* | *0.087* | *0.087* | *0.11* | *96* | *1.06x* |
| bq-expand | 0.087 | 0.087 | 0.14 | 96 | 1.06x |
| *list-aa-adjacent* | *1.000* | *1.001* | *0.19* | *54* | *21.22x* |
| *list-aa-distant* | *1.000* | *1.002* | *0.20* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.27 | 54 | 21.22x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0048, worst cell 1.89% on `block-run64-gap64`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0009 on a worst cell of 0.38% on `block-run64-gap64`, its interval missing 1. The in-situ term reads 1.0259, 1.0235 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0018, which the correction amplifies by 2.61x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m29s, peak 134 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.65 ms per call raw, 4.5 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.030/0.024/0.020

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0707, from `lib-stage2-lean` at 0.9982 to `list-aa-distant` at 1.3388, with `list` itself at 1.3273. **The baseline moved 32.73% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.030, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.020, priced against `mut-odo-vecdims` at 0.8567 over 5 of 5 shapes at sign p 0.062, a margin of 14.33% against this class's 0.48% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 32.73 of a point, at a class geomean of 1.0707 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.87 points. The counted work reads a counts geomean of 1.1488 over the same arms, 16 of them counted. Its counted work parts by 14.88 points where its clock parts by 7.07, so about 0.47 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.20 | 228 | 1.69x |
| liblist-stage4-sum | -- | -- | 0.10 | 242 | 1.17x |
| liblist-stage5-sum | -- | -- | 0.12 | 243 | 1.17x |
| libunord-stage1-sum | -- | -- | 0.21 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.11 | 244 | 0.20x |
| libunord-stage14-sum | -- | -- | 0.08 | 244 | 0.20x |
| libunord-stage15-sum | -- | -- | 0.09 | 244 | 0.20x |
| libunord-stage6-loop-sum | -- | -- | 0.25 | 240 | 0.55x |
| libunord-stage6-sum | -- | -- | 0.26 | 239 | 0.55x |
| libunord-stage7-sum | -- | -- | 0.18 | 239 | 0.55x |
| libunord-stage9-sum | -- | -- | 0.32 | 238 | 0.43x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.45* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.05* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.10* | *250* | *0.01x* |
| lib-stage3-lean | 0.034 | 0.052 | 0.23 | 235 | 1.13x |
| lib-stage2-lean | 0.036 | 0.052 | 0.17 | 235 | 1.13x |
| lib-stage2-lean-u1 | 0.036 | 0.050 | 0.24 | 234 | 1.13x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.053 | 0.069 | 0.26 | 229 | 1.28x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.053* | *0.069* | *0.25* | *229* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.069* | *0.22* | *229* | *1.28x* |
| **mut-odo-vecdims** | **0.061** | 0.089 | 0.16 | 229 | 1.27x |
| *mut-odo-vecdims-aa* | *0.061* | *0.089* | *0.22* | *229* | *1.27x* |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.090* | *0.20* | *229* | *1.27x* |
| lib-stage1 | 0.083 | 0.107 | 0.19 | 221 | 2.36x |
| bq-expand | 0.138 | 0.200 | 0.11 | 217 | 1.44x |
| *bq-expand-aa-adjacent* | *0.138* | *0.200* | *0.12* | *217* | *1.44x* |
| *bq-expand-aa-distant* | *0.138* | *0.200* | *0.22* | *217* | *1.44x* |
| *list-aa-adjacent* | *1.000* | *1.001* | *0.11* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.15 | 180 | 21.57x |
| *list-aa-distant* | *1.000* | *1.002* | *0.16* | *180* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0070, worst cell 1.86% on `small-flat64`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0016 on a worst cell of 0.46% on `small-flat64`, its interval missing 1. The in-situ term reads 0.9498, 0.9637 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0043, which the correction amplifies by 1.61x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 132 MiB in use, 52 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.65 us per call raw, 6.43 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.077/0.050/0.059/0.089

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0781, from `lib-stage1` at 0.9776 to `list-aa-adjacent` at 1.2803, with `list` itself at 1.2712. **The baseline moved 27.12% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.089, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.034, priced against `mut-odo-vecdims` at 0.4467 over 5 of 5 shapes at sign p 0.062, a margin of 55.33% against this class's 0.70% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 27.12 of a point, at a class geomean of 1.0781 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.72 points. The counted work reads a counts geomean of 1.1449 over the same arms, 16 of them counted. Its counted work parts by 14.49 points where its clock parts by 7.81, so about 0.54 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500), and the two views that landed 2026-09-26, for Run 42, and grew from 4992 elements to `sizeCap` on 2026-09-27 (`aa18c24`), for this run --- `compose-bcast-nest` (`l` 1800000, `sInner` 6) and `compose-bcast-wide` (`l` 1800000, `sInner` 120). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero; the two grown ones put a broadcast beside short runs under a reversed nest --- of extent 6 beside runs of 10 under three strided axes nothing merges on `compose-bcast-nest`, of extent 120 beside runs of 6 under five strided axes of extent 4 or 5 on `compose-bcast-wide` --- so that where the unordered stages place the zero-stride axis decides which extent the odometer turns over on.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.63* | *52* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.04 | 80 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.03 | 80 | 0.01x |
| libunord-stage15-sum | -- | -- | 0.03 | 82 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.04 | 80 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.23* | *82* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.014 | 0.018 | 0.50 | 62 | 1.00x |
| lib-stage2-lean | 0.014 | 0.018 | 0.41 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.014 | 0.019 | 0.41 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.014* | *0.019* | *0.47* | *62* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.019* | *0.40* | *62* | *1.00x* |
| lib-stage1 | 0.014 | 0.018 | 0.42 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.46 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.036* | *0.31* | *61* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.036* | *0.32* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.036 | 0.18 | 61 | 1.00x |
| *bq-expand-aa-adjacent* | *0.093* | *0.121* | *0.68* | *46* | *1.35x* |
| bq-expand | 0.093 | 0.123 | 0.65 | 46 | 1.35x |
| *bq-expand-aa-distant* | *0.093* | *0.123* | *0.28* | *46* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 1.15 | 17 | 22.01x |
| *list-aa-distant* | *1.001* | *1.013* | *1.01* | *17* | *22.01x* |
| *list-aa-adjacent* | *1.004* | *1.010* | *0.94* | *17* | *22.01x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0044, worst cell 0.98% on `compose-bcast-nest`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.45% on `compose-bcast-nest`, its interval covering 1. The in-situ term reads 1.0182, 1.0271 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0043, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m15s, peak 142 MiB in use, 41 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar, compose-bcast-nest, compose-bcast-wide):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019/0.036/0.012

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 1.0689, from `lib-stage1` at 0.9702 to `list` at 1.2942, with `list` itself at 1.2942. **The baseline moved 29.42% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.036, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.014, priced against `mut-odo-vecdims` at 0.6257 over 6 of 6 shapes at sign p 0.031, a margin of 37.43% against this class's 0.44% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 29.42 of a point, at a class geomean of 1.0689 over the 16 arms, with 3 of 8 strategies past an A/A bar of 0.87 points. The counted work reads a counts geomean of 1.1606 over the same arms, 16 of them counted. Its counted work parts by 16.06 points where its clock parts by 6.89, so about 0.43 of the instruction saving reaches the clock.


## Provenance

**Run 43's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `e29cdf2`; one shim, `align-as.py` at `1a359bd`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`, which is Runs 36's to 42's compiler unmoved; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run43-gheadnospec` and is what every table here publishes; `run43-gheadtwopass` is the candidate. **What is new against Run 42 is not the pair but the source under both halves**: `Main.hs` moved six of the owner's commits, `eb76398` to `e29cdf2`, and `micro.cabal` took orthotope's warning flags beside them (`6b9e206`), `-O1`, the asserts and the baked RTS options unchanged, while the shim, the recipes, `cabal.project.ghead`, the compiler and the launch are Run 42's to the character, and no reboot sits between the two runs, `uptime -s` putting the box up since 2026-09-24 00:00:29 at both.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 62 class views over ten classes for 1922 more, and it is Run 42's to the name: nothing in and nothing out.** `./roster-delta.py run42-gheadnospec run43-gheadnospec`, read off the two binaries, reads every arm, main-set shape and class view in Run 42's order and every class at its count, so pre-run step 12's condition did not fire and no -L1 roster pass was owed or taken. **What moved is under two unmoved names**, which `roster-delta.py` compares by name and so cannot see: `compose-bcast-nest` and `compose-bcast-wide` grew from 4992 elements to `sizeCap`, 1800000 (`aa18c24`), so every arm's two cells there time a different view than Run 42's did, and a cross-run figure on `compose` is read over its other four views.

**The evening ran in ONE window and in the order the run list gives, one process met foreign CPU on one bench, and the population it touched was rerun on a quiet box the same day.** `run-evening.sh` took the gate from 01:45:40 to 02:19:01, the alarm at 02:19:04 reading 0.2% busy, the sequence from 2026-09-29T02:19:04 to 2026-09-29T09:35:18 and the riders from 09:35:18 to 09:47:50, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones --- and each launched from `./run43-<half>`. The counted work, which wants no quiet machine, ran from 09:48 to 10:28, with the `-g3` twins building beside it. **`--wild` named ONE intrusion**, in the basis's main-set process: 1 of its 589 benches at or above 0.25 of a core foreign, `cnn-L1-6x6-c1/list-aa-adjacent` at a peak of 0.77, early in the process, `cnn-L1-6x6-c1` being its first shape. **Post-run step 3's rerun was taken on the owner's word of 2026-09-29**, the note's `RERUN:` line reading `ask`: both halves of `main`, through `./run-major.sh run43 main` under the same launch environment, control first, from 11:03:06 to 12:45:06, each process reporting rc=0 and its 589 benches, and neither log reaching 0.25 foreign on any bench. So the main set ran in a SECOND window, `read-all.sh` putting 87 minutes between the sequence's last process and the rerun's first, and every main-set figure in this file is the rerun's; the two first processes are parked as `probe-intruded-run43-<half>-main.json` and `.log`. **The rerun is also a reading of its own**: the same two binaries a second time, the basis half's `bq-expand` family 1.5 to 1.7 points slower than its first process and every other arm on either half within 0.72 of a point, `--compare` of each rerun JSON against its parked first process, in `log-read-run43/main-<half>-rerun-vs-first.txt`.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes read `list` 1.2928 and 1.3003, `mut-odo-vecdims` 0.9990 and 1.0006, `bq-expand` 1.3050 and 1.3063 --- 0.75, 0.16 and 0.13 points apart. Between its own two legs `gheadnospec` moved by at most 0.17 points, on `list`, and `gheadtwopass` by at most 0.76 points, on `list`, so what the passes part by is the control's legs and not a disagreement about the pair; `mut-odo-vecdims`, the arm the two passes leave alone, sits either side of 1 inside that drift (`./read-run.py --gate-draft run43` prints all four readings). The machine check, read against the fingerprint Run 42 installed --- this run's basis recipe on the source before the six commits --- puts `list`'s net at **+0.07%**, worst `stretch-coprime-r7` at **-1.07%**, none of 19 shapes past 5% and the geomean inside the 3% bar, so the six commits moved the box's `list` by under the bars.

**Every one of the twenty-two processes gated clean and the plateau refused by declaration, and two A/A worst cells pass 5%, both on the control and both past 10%.** `read-all.sh` gates each process on its own correction and passes 22 of 22, the two main-set ones being the rerun's. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.9094 to 21.2147 ms/iter across the run, a 25.46% spread against a 5% band, and it splits exactly by half, `gheadnospec`'s 11 processes flat within 1.02% at 21.0001 to 21.2147 and `gheadtwopass`'s within 2.35% at 16.9094 to 17.3061, the rerun's process the highest on each half --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-bcastmid` at **26.00%** on `bcastmid-c32-cnn`, `bq-expand-aa-distant` against `bq-expand`, and `gheadtwopass-runs` at **10.25%** on `runs-1024`, `list-aa-adjacent` against `list`, and `--wild` finds no foreign CPU on either. **Both pass the about 10% [the floor section][floor] gates on**, so those two cells leave the per-shape record and their rows are flagged: `bq-expand-aa-distant` on `bcastmid` puts that class's control floor at **5.73%**, where its basis reads 0.34%, and `list-aa-adjacent` on `runs` the control's at 3.80% beside the basis's 3.30%; no span reads either class. **The first of them is the recurring `bq-expand` transient's signature**: on the mutator clock `bq-expand-aa-distant` runs 1.21 times `bq-expand` there, 655486 against 541460 an iteration, on allocation equal to within 1e-4, which is the shape [the open list's entry][open] records. The main set's floor is 0.79% on the basis and 0.60% on the control.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run43-gheadnospec`, md5 `053919ac8c419a0a739101f910cfc96a`, and `run43-gheadtwopass`, md5 `37bcbe57520b6bbe7cf724de9b952dd0`, built on 2026-09-29 from `Main.hs` at `e29cdf2`, clean against it, and run from a tree at `9ee2ad3`, the main-set rerun from `ab96e1b`, two commits of this write-up later and neither touching `Main.hs`. Their `.text` sections are **20145983** and **20191039** bytes, the first column of `size -A`; against Run 42's two the basis is smaller by 8192 bytes and the flagged half by 12288, two and three pages exactly --- the six commits, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 45056 bytes, eleven pages exactly, and it carries MORE self-loops, 303 against 296, so [the open list's entry on it](../README.md#what-is-open) gains a run on that side.

**The six commits moved no 28-byte copy off its offset, in any of the three groups the basis carries.** `./loop-offsets.py --delta run42-gheadnospec run43-gheadnospec`, the same basis recipe on the two sources, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0] and of the two two-copy groups at [0, 3] and [11, 14], with no address surviving to the byte and every displacement a whole number of lines, four displacements on the first group and one on each of the others. **Within the pair** the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves and the two-copy groups [0, 3] and [11, 14] on both, and a three-copy group at [0, 0, 0] exists on the control half alone, as on Runs 41 and 42. `--library` puts **4.3%** of the 806 library self-loops the two halves share at the same offset in line, Run 42's 4.3% to the tenth: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 32 on the basis and 24 on the control, where Run 42 read 27 and 26, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 296 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 303 on the control, 197 and 128 of them at offset 0, where Run 42 read 293 and 296 self-loops, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 3a's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity eleven straddlers on the basis and thirteen on the control** --- on both, `sumNoSpec` twice, `fillStage3`'s body at offset 30, `fillStage2Short` twice, `fillStage2Axes`, the leaf bodies of `fbMutOdoVecdimsAddInLeafU2` twice, `-Down` and `-Last`, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the control `fillStage2OneLevel` and `fbFused` besides, the same names as Run 42's. Of the refusals, eight on the basis and six on the control carry a `--loose` family of `fillStage3`, `fillStage2Short`, `fillStage2VSdims`, `fillStage2OneLevel` and `fillStage2Axes` bodies, which the bytes cannot choose between, and thirteen on the basis and five on the control are 60- to 63-byte bodies at offset 32, 40 or 48 for which no twin holds a copy. **Neither half's own `-g3` twin holds as many loops as the binary it names for**, 287 against the basis's 296 and 290 against the control's 303, where Run 42's basis twin held as many as its binary, so every name above rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run43-gheadnospec`, 9.992 times apart, which is plain -O1; on `run43-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. Both builders' figures are Run 42's to the byte on both halves. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.3 us** on `cnn-slice-c32`, **3.69 ms** on `cnn-L2-24x24-c32`, **39.6 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 19.3 to 21.2 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.47 us | 6.3 us | 5.02 us |
| `cnn-L2-24x24-c32` | 165888 | 3.79 ms | 3.69 ms | 2.91 ms |
| `stretch-wide-2xM` | 1800000 | 40.6 ms | 39.6 ms | 31.9 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.59 ms raw and 4.44 ms net; `bcast-inner900` 30.4 ms raw and 29.4 ms net; `bcastmid-b200k` 48.8 ms raw and 47.7 ms net; `window-128x128-k7` 14.2 ms raw and 13.8 ms net; `scaled-rank1-m1` 5.3 ms raw and 5.12 ms net; `runs-2` 40.6 ms raw and 39.6 ms net; `flip-fwd-rows96` 30.9 ms raw and 29.8 ms net; `block-r3-vol64` 4.65 ms raw and 4.5 ms net; `small-row96` 6.65 us raw and 6.43 us net; `compose-zero-mid` 30.9 ms raw and 29.8 ms net. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and no cell of the whole run is one the reader flags.** The two `sum-only` arms agree on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9998 to 1.0016 across the twenty-two processes, at a mean absolute difference of at most 0.16% --- so the term subtracted from one half is the term subtracted from the other. **No cell sits below R2 0.99 ([what that column detects][ramp]) and none is under ten samples**, of the run's 5022 cells, 2511 on each half; the reader's warnings print for none of the twenty-two JSONs. The first basis main-set process carried one, `stretch-inner256/bq-expand-nosum` at R2 0.9873, and the rerun does not.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, none refused, at a cost of 1339s on the basis and 1113s on the control by `--counts-totals` --- beside Run 42's 1278s and 1049s, on the same roster with two `compose` views grown to 1.8 million elements, and with this run's `-g3` twins building and its first readings running alongside, which an instruction count does not see. The counts are read against the main set's rerun and carry no process term, instructions an iteration being the binary's. The counts geomean over the sixteen arms that carry a corrected time runs **1.1449** on `small` to **1.1776** on `window`, the main set at **1.1673** --- the basis retiring 14.5 to 17.8 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families**: the `bq-expand` trio sits at 0.8768 to 0.8796, retiring 50.63% more instructions on the basis for 32.07 to 32.49% more time, where Run 42's trio sat at 0.8670 to 0.8695 on the same instruction ratio; the `list` trio at 1.0006 to 1.0016, cashing all of what it saves; and the ten others between 0.9464 and 0.9628, retiring 3.83 to 5.47 percent more on the basis while their clocks run from 0.39 of a point below level to 0.58 above. **Read per class the same way, the rate runs 0.43 to 0.79**: the instruction saving reaching the clock is lowest on `compose`, where the counted work parts by 16.06 points and the clock by 6.89, and highest on `window`, 17.76 against 13.98 --- where Run 42 read 0.43 to 0.78, lowest then on `block`.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0001** and **1.0000** on the two halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0284** and **1.0967** on the basis and **1.0265** and **1.0692** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and about ten and seven on `bq-expand`, the term that is subtracted being the `sum-only` one and not this proxy.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1191** on the basis and **1.1558** on the control, **3.7** points apart, where Run 42's two parted by 4.4 and Run 41's by 4.3 --- so the two passes change what the spray costs a process as well as what the roster costs it, by within a point of what they changed it by on the runs before. What the roster adds on top of that state is **1.0191** on the basis, 6 of 19 shapes above 1, and **1.0124** on the control, 13 of 19; the basis's rest runs 0.9710 on `stretch-bigstride` to 1.2147 on `stretch-r5-8x432`, the control's 0.9861 on `stretch-bigstride` to 1.1175 on `stretch-tall-Mx2`. The whole in-process deflation is **1.1404** on the basis, 18 of 19 shapes above 1, and **1.1702** on the control, 19 of 19. **The roster cells are the rerun's and the legs the evening's**, taken 75 minutes before the rerun began, so the decomposition spans the two windows; the box is the one quiet box on both sides of it.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 42's, both recipes unchanged to the character and rebuilt on `Main.hs` at `e29cdf2` where Run 42 built from `eb76398`, on the owner's word of 2026-09-29 that this run keeps the previous run's recipes and focuses on the code and shape changes: both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, `align-as.py` at `1a359bd` as for Run 42, under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run43-gheadnospec` and `run43-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 42's with the builddir names moved. So the pair's own `cross` figure is the two passes read an eighth time, in `--compare`'s orientation of the unflagged basis over the control, and the source is read as each half against Run 42's same half, `--half-movers run43 run42`; the shim, the compiler and `cabal.project.ghead` did not move, and `micro.cabal` moved by warning flags alone (`6b9e206`). The six commits bring no arm in and take none out --- `./roster-delta.py run42-gheadnospec run43-gheadnospec` reads every arm, main-set shape and class view in the same order --- and `./registration-drift.py run43 --since run42` reaches 22 timed arms and no code behind `list`, `bq-expand`, their `-aa` twins, `bq-expand-nosum` or the two `sum-only` halves. What they change behind the arms the items read, off the diffs: bangs moved where the -O1 Core read better, `!l` on `product sh` in the `mut-odo-vecdims` family's fills and `!t` and `!n` in `fbLibStage1`'s stage loops among them (`0a20749`), and dropped where it stayed the same, `absAxes`'s and `absPairs`'s last equation improving it (`6b9e206`); the `Axis` port's bangs and local names matched to the library's, the Core unchanged but for source positions and binder names (`e29cdf2`); `lib-stage1`'s lone slice returned without `VS.concat`, on a path no view of Run 42's sets takes (`2479905`); and `compose-bcast-nest` and `compose-bcast-wide` grown from 4992 elements to `sizeCap`, 1800000, the one shape change (`aa18c24`). **The items' priors are instruction counts, cycles and bytes off this run's own basis binary**, `run43-gheadnospec`, taken with `probe-stalls.sh` at `N=50`, Run 42's counts N, twice, on a quiet box before preflight: into `probe-r43-prior1.txt` and `probe-r43-prior2.txt` over the timed arms and the nineteen main-set shapes, and into `probe-r43-prior1-compose.txt` and `probe-r43-prior2-compose.txt` over `compose`, the two sweeps' instructions agreeing to 0.04% on every cell and their cycles by a median of 1.2% on the main set and 1.4% on `compose`; and allocation a call over `compose` in `probe-r43-alloc-compose.txt`. A cycle figure is quoted only where the two sweeps agree on it. No probe was taken on the control's recipe, so the priors are the basis's, carried to the control on Run 42's two halves agreeing within a point on each of items (1) and (2)'s `lib-` and leaf pairs. **The limit this run cannot remove**: a rebuild moves every loop --- `./loop-offsets.py --delta run42-gheadnospec run43-gheadnospec` finds no matched loop at its old address --- and Run 41's `bq-expand` moved on one half with its instructions level, so a figure on unmoved instructions is predicted only within the spread earlier builds drew.

(1) *The six commits move no timed arm's instructions on the main set, so the lean fills and `lib-stage1` keep the distances Run 42 read.* `./read-run.py --counts-over probe-r43-prior1.txt run42-counts-gheadnospec.txt` reads every timed arm at 0.9998 to 1.0001 of Run 42's counts; `--counts probe-r43-prior1.txt --pair` raw on `run42-gheadnospec-main.json` reads `lib-stage2-lean-u1` over `lib-stage3-lean` at 1.0206, `lib-stage3-lean` over `lib-stage2-lean` at 0.9994 and `lib-stage1` over `mut-odo-vecdims-add-in-leaf-u2` at 0.9737, each within 0.0001 of what `run42-counts-gheadnospec.txt` reads the same way. Run 42 read the three in time at 1.0690, 1.0005 and 1.0009 on the basis and 1.0654, 0.9961 and 1.0058 on the control, `--pair` on `run42-gheadnospec-main.json` and `run42-gheadtwopass-main.json`. `predict: pair lib-stage2-lean-u1 lib-stage3-lean 1.067 within 2.5% on main both`, `predict: pair lib-stage3-lean lib-stage2-lean 0.998 within 2% on main both`, and `predict: pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 1.003 within 2% on main both`. A reading outside a band, the instructions level, is the rebuild's placement and not the source, and `--half-movers run43 run42` names which arm of the pair moved.

**Read by --predictions, item (1):** `pair lib-stage2-lean-u1 lib-stage3-lean 1.067 within 2.5% on main both`: HELD on main basis, read 1.0662 over 19 shape(s), 0.08 point(s) off, within 2.50%; HELD on main control, read 1.0628 over 19 shape(s), 0.42 point(s) off, within 2.50% --- `pair lib-stage3-lean lib-stage2-lean 0.998 within 2% on main both`: HELD on main basis, read 1.0066 over 19 shape(s), 0.86 point(s) off, within 2.00%; HELD on main control, read 1.0044 over 19 shape(s), 0.64 point(s) off, within 2.00% --- `pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 1.003 within 2% on main both`: HELD on main basis, read 0.9928 over 19 shape(s), 1.02 point(s) off, within 2.00%; HELD on main control, read 1.0021 over 19 shape(s), 0.09 point(s) off, within 2.00%.

(2) *The shipped leaf keeps its lead over `mut-odo-vecdims`, and `bq-expand` its distance behind it on each half.* `--counts probe-r43-prior1.txt --pair` raw on `run42-gheadnospec-main.json` reads `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` at 0.7199 and `bq-expand` over `mut-odo-vecdims` at 1.8778, both equal to what `run42-counts-gheadnospec.txt` reads to the fourth place, so the bangs `0a20749` gave the family's fills leave its instructions where they were. Run 42 read the two in time at 0.6368 and 2.8615 on the basis and 0.6375 and 2.1874 on the control, `--pair` on the two main JSONs. `predict: pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.637 within 2% on main both`, `predict: pair bq-expand mut-odo-vecdims 2.86 within 12% on main basis` and `predict: pair bq-expand mut-odo-vecdims 2.19 within 9% on main control`, the last two about four percent of the ratio either way, which is what `bq-expand` moved between Runs 41's and 42's builds with its instructions level, `run42-gheadnospec-main.json --compare run41-gheadnospec-main.json` reading it at 0.9594. A `bq-expand` reading outside its band says the build term exceeds what that pair of builds drew; the leaf's says a bang reached its time without reaching its instructions.

**Read by --predictions, item (2):** `pair mut-odo-vecdims-add-in-leaf-u2 mut-odo-vecdims 0.637 within 2% on main both`: HELD on main basis, read 0.6416 over 19 shape(s), 0.46 point(s) off, within 2.00%; HELD on main control, read 0.6380 over 19 shape(s), 0.10 point(s) off, within 2.00% --- `pair bq-expand mut-odo-vecdims 2.86 within 12% on main basis`: HELD on main basis, read 2.8893 over 19 shape(s), 2.93 point(s) off, within 12.00% --- `pair bq-expand mut-odo-vecdims 2.19 within 9% on main control`: HELD on main control, read 2.1860 over 19 shape(s), 0.40 point(s) off, within 9.00%.

(3) *Grown to `sizeCap`, `compose-bcast-wide` still pays for `libunord-stage15-sum`'s placement of the zero-stride axis, `compose-bcast-nest` costs it little beyond its bytes, and the move stays level where it passes no axis.* At 4992 elements Run 42 read stage fifteen over fourteen at 2.0242 on `compose-bcast-nest` and 0.3706 on `compose-bcast-wide` on the basis, and 2.0127 and 0.3772 on the control, `--pair libunord-stage15-sum libunord-stage14-sum --per-shape` on `run42-gheadnospec-compose.json` and `run42-gheadtwopass-compose.json`. At 1800000, `probe-r43-prior1-compose.txt` reads the pair's instructions at 1.1129 on the first and 0.8030 on the second, where `run42-counts-gheadnospec-compose.txt` read 1.5794 and 0.4570, and 257610 against 257637 on `compose-rev-bcast`; its cycles and `probe-r43-prior2-compose.txt`'s read 0.6970 and 0.7013 on `compose-bcast-wide`, and part on `compose-bcast-nest`, 0.9855 and 1.0565, so that view has no cycle prior; `probe-r43-alloc-compose.txt` puts stage fifteen's allocation a call at 1225929 bytes against 157316 on the first and 126198 against 2998978 on the second. `predict: cell compose-bcast-wide/libunord-stage15-sum over compose-bcast-wide/libunord-stage14-sum 0.70 within 8% on compose both`, `predict: cell compose-bcast-nest/libunord-stage15-sum over compose-bcast-nest/libunord-stage14-sum 1.10 within 12% on compose both`, and `predict: cell compose-rev-bcast/libunord-stage15-sum over compose-rev-bcast/libunord-stage14-sum 1.00 within 3% on compose both`. A `compose-bcast-wide` reading over 0.78 says the agreeing cycles did not carry into time; a `compose-bcast-nest` one over 1.22 says the bytes cost more than their share at this size, as Run 42's time outran its instructions at 4992; a level cell outside 3% is placement.

**Read by --predictions, item (3):** `cell compose-bcast-wide/libunord-stage15-sum over compose-bcast-wide/libunord-stage14-sum 0.70 within 8% on compose both`: HELD on compose basis, read 0.6677 over 1 shape(s), 3.23 point(s) off, within 8.00%; HELD on compose control, read 0.6608 over 1 shape(s), 3.92 point(s) off, within 8.00% --- `cell compose-bcast-nest/libunord-stage15-sum over compose-bcast-nest/libunord-stage14-sum 1.10 within 12% on compose both`: HELD on compose basis, read 1.0432 over 1 shape(s), 5.68 point(s) off, within 12.00%; HELD on compose control, read 1.0588 over 1 shape(s), 4.12 point(s) off, within 12.00% --- `cell compose-rev-bcast/libunord-stage15-sum over compose-rev-bcast/libunord-stage14-sum 1.00 within 3% on compose both`: HELD on compose basis, read 0.9999 over 1 shape(s), 0.01 point(s) off, within 3.00%; HELD on compose control, read 0.9999 over 1 shape(s), 0.01 point(s) off, within 3.00%.

(4) *The regime's worth on `list` stays at its level, and on `bq-expand` inside the spread its builds drew but Run 41's.* `./read-run.py --record regime` reads `list` over the nineteen shapes at 1.2960, 1.2889, 1.2966, 1.2983, 1.2926 and 1.2905 on Runs 37 to 42's builds, inside 0.94 points, and `bq-expand` at 1.2980 to 1.3101 on Runs 36 to 40's and 42's and 1.3620 on Run 41's; no commit reaches either arm, and `--counts-over probe-r43-prior1.txt run42-counts-gheadnospec.txt` reads both at 1.0000. `predict: cross list 1.294 within 1% on main basis`, and `predict: cross bq-expand 1.305 within 2% on main basis`, the band reaching every draw but Run 41's. A `list` reading outside its band says the regime's worth moved with this build; a `bq-expand` one above 1.325 says Run 41's draw was not alone.

**Read by --predictions, item (4):** `cross list 1.294 within 1% on main basis`: HELD on main basis, read 1.2950 over 19 shape(s), 0.10 point(s) off, within 1.00% --- `cross bq-expand 1.305 within 2% on main basis`: HELD on main basis, read 1.3212 over 19 shape(s), 1.62 point(s) off, within 2.00%.

**All four items hold by their kill conditions, on every span on every half each names: eleven spans, eighteen readings, none killed --- item (4)'s `bq-expand` span landing 1.62 points off its centre on the main set's rerun, where the first basis process read it 0.55 off.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set and `compose` on each half and by `--pair` with `--counts` for the instructions; the main-set readings are the quiet rerun's ([Provenance](#provenance)).

(1) *The six commits move no timed arm's instructions on the main set, so the lean fills and `lib-stage1` keep the distances Run 42 read.* **HELD on both halves, on all three spans.** The premise held first: `--counts-over` puts every timed arm's instructions an iteration at 1.0000 of Run 42's to the fourth decimal on both halves, `lib-stage1` at 1.0001 on the basis the widest. `lib-stage2-lean-u1` over `lib-stage3-lean` reads **1.0662** on the basis and **1.0628** on the control, inside 2.5% of 1.067, on instructions of 1.0206 and 1.0219 raw; `lib-stage3-lean` over `lib-stage2-lean` **1.0066** and **1.0044**, inside 2% of 0.998, on 0.9994 and 0.9995; and `lib-stage1` over the shipped leaf **0.9928** and **1.0021**, inside 2% of 1.003, on 0.9737 and 0.9734 --- each instruction ratio the prior's to the fourth decimal, so no reading here carries the placement term the item named, and the last pair sits either side of 1 across the halves inside its band.

(2) *The shipped leaf keeps its lead over `mut-odo-vecdims`, and `bq-expand` its distance behind it on each half.* **HELD on both halves, on all three spans.** The leaf over `mut-odo-vecdims` reads **0.6416** on the basis and **0.6380** on the control, inside 2% of 0.637, on instructions of 0.7199 and 0.7104 raw, so the bangs of `0a20749` reached neither the leaf's instructions nor its time; `bq-expand` over `mut-odo-vecdims` reads **2.8893** on the basis, inside 12% of 2.86, and **2.1860** on the control, inside 9% of 2.19, on 1.8778 and 1.2944. The basis's figure is the rerun's, 1.5% over its first process's 2.8453, the family's process term reaching this pair as it reached the cross figure.

(3) *Grown to `sizeCap`, `compose-bcast-wide` still pays for `libunord-stage15-sum`'s placement of the zero-stride axis, `compose-bcast-nest` costs it little beyond its bytes, and the move stays level where it passes no axis.* **HELD on both halves, on all three spans.** Stage fifteen over fourteen, on raw `slope` since a reducing consumer carries no corrected time, reads **0.6677** on the basis and **0.6608** on the control on `compose-bcast-wide`, inside 8% of 0.70 and under the 0.78 that would say the agreeing cycles did not carry into time; **1.0432** and **1.0588** on `compose-bcast-nest`, inside 12% of 1.10 and under the 1.22 that would say the bytes cost more than their share; and **0.9999** on both halves on `compose-rev-bcast`. The instructions came out as the prior said, 0.8030 and 0.8025 on `compose-bcast-wide`, 1.1129 and 1.1139 on `compose-bcast-nest` and 0.9999 on `compose-rev-bcast`, so at 1.8 million elements the wide view's time follows its cycles, 0.6970 and 0.7013 in the two prior sweeps, rather than its instructions, and the nest view's lands between the two cycle readings the sweeps parted on.

(4) *The regime's worth on `list` stays at its level, and on `bq-expand` inside the spread its builds drew but Run 41's.* **HELD on both spans.** `list` reads **1.2950**, 0.10 of a point off 1.294, back inside the 0.94 points the draws after Run 36's keep. `bq-expand` reads **1.3212**, 1.62 points off 1.305 and inside its 2% band, but 1.11 points over the 1.3101 the six draws that are not Run 41's reached and under the 1.325 the item named as Run 41's draw not being alone --- and the first basis process read it at 1.3105, inside that spread, so what this run adds to the series is a process term on the family and not a second Run 41.
