# Run 42 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span and the settled cost, on the changed source, launched from disk)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach. The words it uses and the bars it reads against --- a point, the sign of a ratio, a strategy, a family, the plateau, and which bar answers what --- are defined once in [README's *Reading a run file*](../README.md#reading-a-run-file).

**Run 42 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span and the settled cost, on the changed source, launched from disk): the two passes are worth some twenty-nine points on `list` and thirty-one on `bq-expand`, ALL NINE registered spans hold, and on the main set the six source commits moved one fill, `lib-stage1`, by about a point.** The pair is Runs 36's to 41's IN ITS VARIABLE --- one source, `Main.hs` at `eb76398`, one shim at `1a359bd` under five switches with the exit span and the settled cost, ONE compiler, `10.1.20260918`, one roster, one shape set, every process launched from disk --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the sixteen main-set arms that carry a cross-half figure, SIX move with the families and TEN do not: the six are the `list` and `bq-expand` families entire, at **1.2905** to **1.3097**, and the ten others span **0.9915** to **1.0026**. **The bar an arm has to clear to be the passes' rather than the run's is 0.38 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 0.26% on the basis and 0.49% on the control and measured WITHIN one half --- and five of the eight arms that are not A/A copies clear it: the two families, and three fills the passes make SLOWER, `lib-stage2-lean` at 0.9915, `lib-stage1` at 0.9953 and `lib-stage3-lean` at 0.9959, where on Run 41 no fill cleared it.

**What this run was built to settle is whether the six commits' ports left each fill where its instructions put it, and all nine spans hold, `lib-stage1` moving further than its instructions and inside its band.** `lib-stage2-lean-u1` over `lib-stage3-lean`, now on one path, reads **1.0690** on the basis and **1.0654** on the control, where Run 41 read 1.0703 and 1.0693 with the path between them as well, so the distance lives in the run bodies; `lib-stage3-lean` over `lib-stage2-lean` reads **1.0005** and **0.9961**, level; and `lib-stage1` over the shipped leaf **1.0009** and **1.0058**, where Run 41 read 0.9897 and 0.9909, the conversion a call costing about a point. `libunord-stage15-sum` over stage fourteen reads **2.02** on `compose-bcast-nest` and **0.37** on `compose-bcast-wide` on the basis and 2.01 and 0.38 on the control, where its instructions read 1.58 and 0.46, and level where the move passes no axis; and the regime's worth reads `list` at 1.2905 against 1.295 within 1% and `bq-expand` at **1.3097** against 1.33 within 3.5% ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)).

**The one move no commit made is Run 41's `bq-expand` move undone, and the run itself was quiet.** Against Run 41's basis the basis half runs the whole `bq-expand` family 3.4 to 9.5% faster on the four populations where Run 41 read it slower, on level instructions and on code no commit changed, reading 1.0004 of Run 40's basis on the main set, while the control's family moves past 3% on no population --- so what Run 41 read was its own build, as its copy test said ([What the next run compares against](#what-the-next-run-compares-against)). The same return takes the opening's headline, `bq-expand` over `mut-odo-vecdims`, from 2.97x to 2.86x on the basis. No reboot sits between this run and Run 41, the machine check read `list` inside the bars and no bench met foreign CPU; the copy test, taken the next afternoon, puts the control's three `flip` movers on its file instance and the basis's `lib-stage1` on `rev` on this build ([Results](#results)).


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span and the settled cost**, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is the SOURCE alone**: the compiler is Runs 36's to 41's in-tree stage1 `10.1.20260918` unmoved, and the project file `cabal.project.ghead`, the shim `align-as.py` at `1a359bd` with its five switches, the regime and the launch from disk are Run 41's. What moved is `Main.hs`, from `688e952` to `eb76398` in six of the owner's commits, which brought one timed arm and two class views in and took none out. **Read against the half Run 41 built by this same recipe, the untouched `bq-expand` family moved back and one rewritten fill moved**, which [What the next run compares against](#what-the-next-run-compares-against) gives arm by arm. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run42-gheadnospec`, as every published table here is from Run 13 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-one rows. What decides which half publishes is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **ONE of the thirty-one rows is a first reading**, `libunord-stage15-sum`, the arm `eb76398` added; the other thirty are Run 41's in Run 41's order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries, so every other row has a twin in Run 41's file.

**Comparing runs?** The table below is Run 42's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.26%** from 1 on the basis half or **0.49%** on the control, read over the eight pairs this roster carries --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The whole-set figure and the carry-back one part on the basis and COINCIDE on the control this run**: over the four pairs that carry back to Run 10 the two halves read **0.21%** and **0.49%**, `bq-expand-aa-distant` carrying the basis's carry-back figure where `list-aa-adjacent` carries its whole-set one, and `bq-expand-aa-distant` carrying both of the control's. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **2.20%** on `stretch-primes` on the basis and **3.74%** on `stretch-coprime-r7` on the control --- are not floors at all and are not to be quoted as any. Its two columns may be differenced on none of the eleven populations, for the reason [below the table](#results) gives.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.60* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.54 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage4-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| liblist-stage5-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over stage four's route with the fill numbered innermost first |
| libunord-stage1-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage14-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's route with the fill numbered innermost first |
| libunord-stage15-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage fourteen's route with the zero-stride axis consed just outside the run |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.35* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage3-lean | 0.023 | 0.112 | 0.52 | 70 | 1.00x | new mutating `Vector` method -- the lean dispatch over the fill numbered innermost first, against `lib-stage2-lean`, which keeps the outermost-first numbering |
| lib-stage2-lean | 0.024 | 0.112 | 0.53 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage1 | 0.025 | 0.112 | 0.50 | 70 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| lib-stage2-lean-u1 | 0.025 | 0.110 | 0.59 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.112 | 0.51 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` was a port of until 2026-09-11 |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.112* | *0.55* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.111* | *0.62* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.111* | *0.42* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.111 | 0.32 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *mut-odo-vecdims-aa* | *0.045* | *0.111* | *0.40* | *66* | *1.00x* | *A/A control* |
| *bq-expand-aa-adjacent* | *0.128* | *0.261* | *0.66* | *50* | *2.78x* | *A/A control* |
| bq-expand | 0.128 | 0.261 | 0.67 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.129* | *0.261* | *0.31* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.67 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.000* | *1.014* | *0.73* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.003* | *1.013* | *0.52* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run SEVEN of the 105 pairs among the fifteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 41's basis parted on none, four of the seven with `lib-stage1` on one side, and ELEVEN part on the control. **The cap still moves the fills' rows**: seven rows have two to four of their nineteen cells capped, the four `lib-` fills and the shipped leaf with its two copies, and the published figures sit 6.9 to 12.8 points under their plain per-shape geomeans, so rows 0.001 apart in print are ordered by the cap and not by the arms. **The widest disagreement of any kind on the basis sits on the row the cap moved furthest**: `lib-stage1` over `mut-odo-vecdims` divides to **0.5557** on the column where the paired figure is **0.6374**, the column 12.8% under it, `lib-stage1`'s published figure sitting 12.8 points under its plain geomean. Those column ratios are `--pair`'s own `published-column ratio` and `--winsor`'s census, not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads thirteen of the sixteen rows moved against Run 41's table, `lib-stage1` by 0.3 points faster, where `--compare` against the JSON of the half Run 41 built puts that arm at 1.0106, slower, and `list` at 1.0017.

**This run's two columns may be differenced on NONE of the eleven populations, as Runs 36's to 41's could not, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **29.05 points** on the main set and by 26.97 on `bcastmid` to 39.78 on `bcast` over the ten classes, every one of the eleven figures past the bar by a factor of thirty-eight or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. What stays readable is `--compare`'s paired ratio per arm, which the head quotes against the cross-half A/A bar `--compare` prints: it says which half runs that arm faster and by how much, and never licenses subtracting one half's published column from the other's. **That is the bar working rather than failing**: it exists to stop a margin being read off two columns with different denominators, and a pair built to move the denominator is the case it was written to refuse.

`concat-runs` has no row, and neither do the other 82 arms the roster holds and checks without timing --- **83 of its 114** in all, as many as on Run 41: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **One arm joined the timed roster and none left it**, `eb76398` adding `libunord-stage15-sum`: `roster-delta.py`, read off the two binaries, reads 30 arms to 31 over 19 shapes to 19, the other thirty in the same order, and the class views 60 to 62, `compose-bcast-nest` and `compose-bcast-wide` in. A movement against Run 41's own basis column is therefore a movement on the **16 shared arms that carry a corrected time**, with a source term between the two runs and no shim, compiler, boot, project-file or launch term --- and a movement across THIS run's two halves is the two passes, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table prints `lib-stage3-lean` alone at 0.023**, with `lib-stage2-lean` at 0.024, `lib-stage1` and `lib-stage2-lean-u1` at 0.025 and the shipped leaf at 0.026 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result. **Paired on the basis the head is a tie between the two lean fills and a lead over the rest**: `lib-stage3-lean` over `lib-stage2-lean` is **1.0005** at 7 of 19 and p 0.36, which is registration item (2) holding, and `lib-stage2-lean` over the shipped leaf **0.8860** at 16 of 19 and over `lib-stage1` **0.8853** at 16 of 19 --- so the two lean fills lead `lib-stage1` and the shipped leaf by eleven points each, where on Run 41 they led `lib-stage1` by ten. **The third, read across the halves, is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6368** on the basis and **0.6375** on the control, 0.07 of a point apart on a pair that moves `list` by twenty-nine points, both inside the 0.6358 to 0.6525 that Run 34's file records across Runs 29 to 33 --- a span carried from that file and not re-derived here.

**The six commits reached the clock where the registration said, and the one family no commit reached moved back on one half.** Against Run 41's basis, the same recipe on `688e952`, `lib-stage1` reads **1.0106** on counts of 1.0033, and the control's **1.0169** on 1.0038 --- the `walkAx` conversion item (3) is about, costing the clock three to four and a half times what it costs the instructions across runs, while within each half its pair with the shipped leaf stays under the 1.013 item (3) set as the sign of such a cost --- while the other three rewritten fills read 0.9936 to 1.0037 on counts of 0.9982 to 0.9992, `lib-stage2-lean` at 0.9936, `lib-stage2-lean-u1` at 1.0025 and `lib-stage3-lean` at 1.0037. **The family no commit reached is `bq-expand`, on the BASIS half alone**, at 0.9585 to 0.9594 of Run 41's on counts level to the fourth decimal and at 1.0004 of Run 40's, while the control's family reads 0.9963 to 0.9986 of Run 41's; [What the next run compares against](#what-the-next-run-compares-against) gives the main set's cells.

**The half-local movers against Run 41 are three kinds, and the largest is Run 41's own move undone.** `--half-movers run42 run41` flags twenty arm-populations past 3%, each on ONE half and none on both. **Twelve are the basis's `bq-expand` trio on `main`, `bcastmid`, `rev` and `window`**, 3.4 to 9.5% faster on counts level --- the family and the four populations Run 41 flagged slower on the basis, so the term that run read went with its build. **Four are count-led, on `small`**: the basis's `lib-stage2-lean`, `lib-stage2-lean-u1` and `lib-stage3-lean` 5.9, 3.6 and 3.2% faster on counts down 1.3, 2.2 and 1.1%, and the control's `lib-stage1` 4.4% slower on counts up 2.5%, the conversion again. **Four more have their counts level**: the control's `lib-stage2-lean`, `mut-odo-vecdims` and `mut-odo-vecdims-aa` on `flip`, 4.9, 3.9 and 3.2% faster, widest on `flip-last-rows`, and the basis's `lib-stage1` on `rev`, 3.4% slower on counts up 0.24%. A mover with its counts level is that half's binary, its file instance or its process and not the pair's variable. **The copy test, taken 2026-09-27 on a quiet box the owner granted after the write-up, tells the four apart**: `./copy-test.sh run42` timed the widest cell of the widest mover in each population and half, one cell standing for the movers beside it, and `rev-cnn-L1-24x24-c1/lib-stage1` the same way by hand, in cycles an iteration, the difference of an `-n 2N` and an `-n N` process over three interleaved passes, on the timed file, a fresh copy of it and Run 41's same half, read by `--copy-test`. **The `flip` movers are the control's FILE INSTANCE**: on `flip-last-rows/lib-stage2-lean` the fresh copy reads 1.168 of the timed file and Run 41's control 1.162, so the same bytes loaded afresh run with the previous build and only the file the evening ran from is faster. **`lib-stage1` on `rev` is this run's BUILD**: the copy reads 0.997 of the timed file and Run 41's basis 0.962. **The `bq-expand` movers are BUILD too**, the cells `--copy-cells` took on the basis reading the copy at 0.996 to 1.007 of the timed file and Run 41's basis at 1.100 to 1.130, which is Run 41's own copy test seen from this side. The page-frame reading the chapter takes next on an INSTANCE verdict, `probe-pageflags.py` as root, was not taken. **Step 4b's cells read the same way**: ranked by time over counts, the twenty widest cells of the 2511 are all `bq-expand-nosum`, whose counts the two passes move by 37 to 40% on cells where its clock moves by at most ten, and the count-led cells are led by the `bq-expand` family's, whose counts the passes move by up to 132%.


## What the next run compares against

**Run 42's pair is Run 41's rebuilt on the changed source, [registered 2026-09-26](#what-this-run-was-built-to-answer-and-what-it-answered)**, on the owner's word of 2026-09-26, both recipes unchanged to the character. **That entry is the ONE declaration site by the ruling of 2026-09-19 and it spells both recipes out, so they are not restated here; [the standing rulings from past runs](../README.md#standing-rulings-from-past-runs) are NOT that site either. What this run leaves as the reference is `run42-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `eb76398`, the shim at `1a359bd` under five switches with the exit span and the settled cost, every process launched FROM DISK, `hugebin/` unmounted, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **It is another published basis on that compiler, and the step from Run 41's is the source and nothing else**: against `run41-gheadnospec`, the same recipe on `688e952`, thirteen of the sixteen timed arms both runs carry read within 1.1 points of 1 by `--compare`, paired per shape, and three do not --- the `bq-expand` trio at **0.9585** to **0.9594**, below 1 meaning this run is the faster, `--bridge` putting the trio and no other arm outside the 3.3% drift band it prints, Run 11's. The trio's gain sits on eight of the nineteen shapes, 6.1 to 12.8% faster with `cnn-L2-24x24-c32` and `vgg-14-c512-k3` the widest, the shapes Run 41's loss sat on; **against Run 40's basis `bq-expand` reads 1.0004**, so this build put the family back where Run 40's had it, and what Run 41 read was that build's. **The pair itself is Runs 36's to 41's, built again**, and its draws are `./read-run.py --record regime`'s, a row per build: on `list` this one lands among the six before it, and on `bq-expand` it lands back inside the five draws before Run 41's. Against Run 31's whole-level **1.2974** the six later `list` draws straddle the level, so **the level's other passes still do not measurably hand `list` back**. **What it leaves unasked is the split**: this pair prices `-fspec-constr` and `-fliberate-case` TOGETHER, and no reading of either pass alone exists on this compiler; it is [an open question][open].

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918`, as Runs 36's to 41's were --- and the step this run reads is not a compiler step at all.** **What this run adds is another build of the pair, on a source six commits on**: Runs 36 to 42 are the same two recipes on the same compiler, Runs 39's to 42's with the settled cost on both, and their cross-half readings agree to 0.94 points on `list` over the six draws after Run 36's, while `bq-expand` returns to 1.3097, inside the 1.2980 to 1.3101 its five draws before Run 41 kept, Run 41's 1.3620 standing alone above them. That is a repetition of the READING and not of a binary, so what it bounds is the harness, the box, the shim and the source together --- and on `bq-expand` one draw has broken the bound, and the build after it did not. Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; on GHC HEAD the two passes together are `--record regime`'s seven build rows. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, and every HEAD draw sits above the higher of them. On `list` they multiply to 1.3325 against Run 31's 1.2974, and on the eighteen shapes left without Run 36's wild cell, where Run 36 read above the level, the six later HEAD draws straddle it.

**What Run 42 leaves the next run to read against, and the first item is a check that did NOT fire.** No reboot sits between Run 41 and this run, and the gate says the box still measures as it did, the machine check reading `list`'s net inside the bars against the fingerprint Run 41 installed ([Provenance](#provenance) gives the figures). **This reading carries a source term and nothing else**: Run 41's basis is this basis's recipe on `688e952`, and `list` runs no code the six commits changed, so `list` holding level says the rebuild left `list` where it was, and says nothing of `bq-expand`, which moved back and which the check does not read. The fingerprint below is this run's own. **What a next run may take from it is a like-for-like check** if it keeps this recipe.

**Registered with the pair.** Run 42's registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. **All nine spans held, on every population and half their scope names**, and the priors behind items (1) to (4) were instruction counts and bytes off this run's own basis binary, taken after the build, as Run 41's were. **What a next registration should take from this one is that an instruction ratio bounds a direction and not a size**: item (4)'s two moving cells landed at 2.02 and 0.37 where their instructions read 1.58 and 0.46, inside bands widened for what the bytes might add, and `lib-stage1`'s conversion cost the clock three to four and a half times its instructions.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are installed and how, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 42**, whose halves were launched FROM DISK and whose basis carries `LOOP_EXITSPAN=1 LOOP_SETTLED=1` at plain -O1 on the in-tree stage1 `10.1.20260918`, on `Main.hs` at `eb76398` with the shim at `1a359bd`; a run keeping that recipe reads against this basis with no shim term. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it. **The step this run records IS basis to basis**: Run 41 published a HEAD half on this basis's recipe, so the two published columns carry no compiler or shim term, only the source. Over the **16 arms both rosters time and both give a corrected time** it runs from **0.9585** on `bq-expand-aa-adjacent` to **1.0106** on `lib-stage1`, below 1 meaning this run is the faster, as the first paragraph of this section breaks down. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one. Its two columns may NOT be differenced, for the reason Results gives, so the table is two orderings read side by side.
| strategy | Run 42 (plain -O1, dead-spot, exit span, settled cost, -A32m, HEAD 10.1.20260918) | Run 42 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.026** | 0.032 |
| `lib-stage1` | **0.025** | 0.032 |
| `lib-stage2-lean` | **0.024** | 0.030 |
| `lib-stage2-lean-u1` | **0.025** | 0.033 |
| `lib-stage3-lean` | **0.023** | 0.030 |
| `bq-expand` | **0.128** | 0.126 |

**Read the two columns as orderings, as [README's *Reading a run file*](../README.md#reading-a-run-file) says, `list` having moved past the bar between these halves.** They print far apart on six of the seven rows, the control higher on each of those six, while `bq-expand` prints 0.128 and 0.126, the one arm whose own move outpaces the denominator's; in absolute terms the flagged half is the faster on twelve of the sixteen timed arms, `--compare` putting the other four, `lib-stage2-lean`, `lib-stage1`, `lib-stage3-lean` and `lib-stage2-lean-u1`, at 0.9915 to 0.9992, the first three outside the 0.38-point bar that comparison prints. **Read DOWN a column and the head is the two lean fills**, `lib-stage3-lean` at 0.023 on the basis with `lib-stage2-lean` next, and `lib-stage2-lean` at 0.030 on the control with `lib-stage3-lean` level with it to three decimals; `bq-expand` is at the foot of each.

**The control half's own standings on the arms this run's roster carries, which no FULL table here holds, the two-column table above carrying seven of its rows and every other published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `mut-odo-vecdims` **0.6375** (0.6368); `lib-stage1` against `-u2` **1.0058** (1.0009); `lib-stage2-lean` against `-u2` **0.8937** (0.8860) and against `lib-stage1` **0.8886** (0.8853); `lib-stage3-lean` against `lib-stage2-lean` **0.9961** (1.0005); `lib-stage2-lean-u1` against `lib-stage3-lean` **1.0654** (1.0690); and the headline pair README's opening leads with, `bq-expand` against `mut-odo-vecdims`, **2.1874** (2.8615), 0 of 19 shapes to `bq-expand` on either half. **Six of the seven hold their direction across the halves** by the paired figure, the five besides the headline pair each moving under a point; `lib-stage3-lean` against `lib-stage2-lean` sits either side of 1, 0.44 of a point apart, and the headline pair moves by 67.4 points, the pair's own variable. **`lib-stage2-lean` leads the shipped leaf by about eleven points on both halves**, as on Run 41, and `lib-stage3-lean` is level with it, at sign p 0.36 on the basis and 1 on the control.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.29 us | 0.079 | `lib-stage2-lean` 0.044 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.52 us | 0.089 | `lib-stage3-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.067 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 118 us | 0.063 | `lib-stage2-lean` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 387 us | 0.044 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `gather48-src-50` | 3 | 22500 | 457 us | 0.048 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.12 ms | 0.030 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.71 ms | 0.052 | `lib-stage3-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `stretch-primes` | 89 | 250357 | 4.42 ms | 0.024 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17.1 ms | 0.039 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.7 ms | 0.052 | `lib-stage1` 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 20 ms | 0.030 | `lib-stage2-lean` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.8 ms | 0.023 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.6 ms | 0.111 | `lib-stage2-lean-u1` 0.110 | `mut-odo-vecdims` 0.111 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.7 ms | 0.022 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 31.1 ms | 0.086 | `lib-stage3-lean` 0.073 | `mut-odo-vecdims-add-in-leaf-u2` 0.076 |
| `stretch-bigstride` | 3 | 1800000 | 51.1 ms | 0.033 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 40 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 40.8 ms | 0.021 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.5 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside vecdims | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 945 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.6 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.9 ms | 0.019 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.7 ms | 0.019 | `lib-stage3-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 36 ms | 0.015 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.2 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.64 ms | 0.053 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.3 ms | 0.019 | `lib-stage2-lean` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.6 ms | 0.034 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.3 ms | 0.022 | `lib-stage3-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.25 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.26 ms | 0.024 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.28 ms | 0.024 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.34 ms | 0.029 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.51 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-bcast-nest` | `compose` | 2 | 4992 | 121 us | 0.072 | `lib-stage3-lean` 0.036 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `compose-bcast-wide` | `compose` | 52 | 4992 | 85.1 us | 0.026 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 943 us | 0.029 | `lib-stage3-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 937 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.4 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.8 ms | 0.019 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.36 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.3 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.66 ms | 0.053 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.4 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30 ms | 0.024 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.4 ms | 0.047 | `lib-stage3-lean` 0.042 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 120 us | 0.064 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 456 us | 0.048 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.41 ms | 0.025 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.2 ms | 0.025 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.025 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.5 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.7 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.8 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 29 ms | 0.024 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-256` | `runs` | 256 | 1799936 | 29.3 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-7` | `runs` | 7 | 1799994 | 32.4 ms | 0.033 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-2` | `runs` | 2 | 1800000 | 39.9 ms | 0.058 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 30.4 ms | 0.025 | `lib-stage3-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.3 ms | 0.040 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.9 ms | 0.025 | `lib-stage3-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-5` | `runs` | 5 | 1800000 | 33.3 ms | 0.038 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.5 ms | 0.025 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 32.3 ms | 0.030 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-96` | `runs` | 96 | 1800000 | 29.4 ms | 0.024 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.6 ms | 0.025 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 267 us | 0.029 | `lib-stage3-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage3-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.19 ms | 0.029 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.029 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.077 | `lib-stage2-lean` 0.041 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-bcast32` | `small` | 32 | 256 | 4.41 us | 0.050 | `lib-stage3-lean` 0.034 | `mut-odo-vecdims-add-in-leaf-u2` 0.044 |
| `small-flat64` | `small` | 64 | 256 | 4.42 us | 0.058 | `lib-stage3-lean` 0.006 | `mut-odo-vecdims-add-in-leaf-u2` 0.056 |
| `small-patch-r5` | `small` | 4 | 256 | 5.26 us | 0.088 | `lib-stage3-lean` 0.050 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.44 us | 0.042 | `lib-stage3-lean` 0.035 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `window-28x28-k5` | `window` | 5 | 14400 | 279 us | 0.040 | `lib-stage3-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 947 us | 0.085 | `lib-stage3-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.44 ms | 0.052 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.59 ms | 0.052 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.83 ms | 0.051 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.9 ms | 0.051 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.3 ms | 0.053 | `lib-stage3-lean` 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.7 ms | 0.031 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-one rows is a geomean over fewer shapes than the rest, as on Runs 32 to 41 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the ELEVEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, and with the two `-nosum` controls and the two `sum-only` halves beside them FIFTEEN of the thirty-one rows carry no corrected time --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside vecdims` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names three different `lib-` arms --- `lib-stage3-lean` on FIVE rows, `lib-stage2-lean` on four and `lib-stage1` on one, Run 41's split, with two of its rows now naming the other lean fill. The cross-class summary's `best outside vecdims` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 42's verdicts** over ten classes, the details beside each class's table. **Properties 1 and 2 held everywhere, property 1's one main-set cell included, and property 3 broke its LEVEL clause in every population it reads, as on Runs 36 to 41 and at the same multiples**, the pair's variable being the same one: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**: the main set's basis puts `mut-odo-vecdims` over `bq-expand` on `stretch-pow2stride` at **0.9957**, where the control reads **0.9856**. That is the cell [the open list carries][open], every draw of which `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints beside its half's floor: under 1 on this basis draw, and further under it than its 0.26% floor. Every other shape of every population reads the clause with room, the classes' closest cells at 0.33 to 0.48 on the basis. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population.

Beside property 1, and the case has simplified three times --- the prune of 2026-09-04 parked the arm that used to be half of it, the retirement of 2026-09-09 took four of the five arms that broke the rest, and the retirement of `runs-3` on 2026-09-25 took one of its cells: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the stage-one route as it shipped.** `lib-stage1`, whose fill since `c7549d2` is `fillStage3` behind a `walkAx` conversion and so no longer the library's own, is slower than `list` on `runs-2` on both halves, at **1.1005** on the basis and **1.3463** on the control; `--over-list` reads every other one of the 1134 timed non-control cells this run carries, over all eleven populations on both halves, at or under 1. **They are the two cells Run 41 read, and it is still `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0124 between the halves while `list` moves 1.2386.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits under 0.053. The `bq-expand` clause is closest at `small-row96` on the CONTROL half, **1.00441**, then `scaled-rank1-m1` at 1.00003 on both halves, and `stretch-tall-Mx2` at 1.00000 on both halves of the main set with `bcast-src8` at 1.00000 on the control. **Those five figures are Runs 36's to 41's to the digit printed, on the same shape and the same half**, which is what allocation being deterministic per call predicts, no commit having rewritten code behind `mut-odo-vecdims`, `bq-expand` or `list`. **The two passes are still what put the closest one where it is**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control.

3. **The allocation tiers survive and their ORDER is unbroken in all ten classes and on the main set, on both halves --- and their LEVEL clause BREAKS in every population it reads, as it did on Runs 36 to 41, and on Run 31 before them, where registration (10) died on it.** The order clause is untouched: `mut-odo-vecdims` sits at the result vector --- the tier the three columns read, `lib-stage1` sitting above it at 1.01x to 1.42x on `rev`, `runs` and `block` and every fill above it on `small` --- `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 19.00x to 27.66x, on both halves and in every population, `small` outside the LEVEL clause by the ruling of 2026-09-07 as before. What breaks is the level: **the two passes change what `list` and `bq-expand` ALLOCATE, and this run reads that change at Run 31's own figures.** On the main set the fills read 1.00x on both halves while `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the nineteen shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, both figures Runs 37's to 41's to the fourth decimal.

**AND ONE ARM OUTSIDE THE TWO FAMILIES MOVES, `libunord-stage13-sum`, by 3.1 points, where Run 41 read four unordered consumers moving by 1.5 to 2.1.** On the main set, read per cell over the nineteen shapes, the flagged half allocates **0.9687** of the basis on `libunord-stage13-sum`, where Run 41 read it at 1.0001; `-stage6-sum`, `-stage6-loop-sum`, `-stage7-sum` and `-stage9-sum`, which Run 41 read at 0.9795 to 0.9852, now read 0.9989 to 1.0001, and `-stage14-sum`, the new `-stage15-sum` and `libunord-stage1-sum` 0.9988 to 1.0000. The fills and ordered consumers read 1.0000 to 1.0016 --- `lib-stage2-lean` at 1.0016 the highest, where Run 41 read it and its `-u1` at 0.9981. **Every one of Run 41's four is reached by the six commits** --- `ea7d222` moved them onto the `Axis` path, whose merge `7ca5d40` made a loop, `registration-drift.py` naming each --- **and `-stage13-sum` by one commit alone**, `08b4f19`, which ported that loop to the pair arms and to `routeUnord13`; which part of the port the two passes reach, no reading here separates. **In absolute terms it allocates 320 to 1536 bytes a call on the basis main set** and the consumers sit under the 0.01x tier, so no tier moves and no property verdict changes with it. `--alloc` puts 363 of the main set's 551 cells above 100 bytes a call inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-aa-distant`, with the 38 cells under that size set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 42 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, settled cost, -A32m, launched from disk) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 26.97 points on `bcastmid` at narrowest and 39.78 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Runs 36 to 41, which read this same pair, and on Run 31, whose variable was the whole level. Over the ten classes the reader counts **160 arm-comparisons, 47 putting the basis faster and 113 slower**, with no degenerate arm excluded, at geomeans from **1.0636** on `block` to **1.1384** on `window` and extremes of `mut-odo-vecdims-add-in-leaf-u2-aa` at **0.9795** on `block` and `bq-expand-aa-distant` at **1.5236** on `window`. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **One registration names a class**: item (4)'s three cell spans are `on compose` and are read in that block, every other span being `on main`.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

The cross-class summary's columns and its bold are [README's *Reading a run file*](../README.md#reading-a-run-file). **The bold is the arm outside the vecdims arms on ALL TEN rows this run** --- `lib-stage3-lean` on `bcast`, `window`, `runs`, `block` and `small`, `lib-stage2-lean` on `rev`, `bcastmid`, `flip` and `compose`, and `lib-stage1` on `scaled`. **The vecdims arms' ceiling is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` on every row**, as on Runs 39 to 41. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside vecdims | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.064 | **`lib-stage2-lean`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.49% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage3-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 | 0.70% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage2-lean`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.51% |
| `window` | 8 | 0.051 | 0.085 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.21% |
| `scaled` | 3 | 0.029 | 0.029 | **`lib-stage1`** 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.59% |
| `runs` | 16 | 0.026 | 0.058 | **`lib-stage3-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 | 3.17% |
| `flip` | 6 | 0.028 | 0.053 | **`lib-stage2-lean`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.82% |
| `block` | 5 | 0.023 | 0.029 | **`lib-stage3-lean`** 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.47% |
| `small` | 5 | 0.061 | 0.088 | **`lib-stage3-lean`** 0.033 | `mut-odo-vecdims-add-in-leaf-u2` 0.053 | 0.76% |
| `compose` | 6 | 0.029 | 0.072 | **`lib-stage2-lean`** 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.017 | 0.58% |

The best arm outside the vecdims arms is ahead of `mut-odo-vecdims` in every one of the ten classes. **No row's bold sits in the CEILING column this run**, as on Runs 39 to 41. TWO rows change the arm they name, `block` to `lib-stage3-lean` and `compose` to `lib-stage2-lean`, each the other lean fill where Run 41 named one. **FOUR rows tie at three decimals this run**, `rev`, `bcast`, `scaled` and `compose`, the bold arm and the ceiling printing the same figure, and `runs` and `block` sit a thousandth apart; the `bold` column decides each on the unrounded values, so on those four the bold is a lead the printed table cannot show.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.15 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.11 | 148 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 148 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 147 | 1.03x |
| libunord-stage13-sum | -- | -- | 0.01 | 157 | 0.01x |
| libunord-stage14-sum | -- | -- | 0.01 | 157 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 157 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.01 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.02 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.10* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage2-lean | 0.021 | 0.025 | 0.09 | 148 | 1.00x |
| lib-stage3-lean | 0.021 | 0.026 | 0.11 | 148 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.041* | *0.07* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.041 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.041* | *0.14* | *147* | *1.00x* |
| lib-stage1 | 0.022 | 0.040 | 0.08 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.024 | 0.029 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.10* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.064* | *0.08* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.064 | 0.13 | 138 | 1.00x |
| *bq-expand-aa-adjacent* | *0.138* | *0.234* | *0.10* | *122* | *3.22x* |
| bq-expand | 0.138 | 0.235 | 0.13 | 123 | 3.22x |
| *bq-expand-aa-distant* | *0.139* | *0.236* | *0.16* | *122* | *3.22x* |
| list (baseline) | 1.000 | 1.000 | 0.24 | 85 | 26.11x |
| *list-aa-distant* | *1.005* | *1.006* | *0.17* | *85* | *26.11x* |
| *list-aa-adjacent* | *1.006* | *1.006* | *0.21* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9951, worst cell 0.94% on `rev-gather48-src-50`, and 2 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.01% on `rev-primes`, its interval covering 1. The in-situ term reads 1.0090, 1.0171 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9972, which the correction amplifies by 1.71x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m6s, peak 96 MiB in use, 25 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.56 ms per call raw, 4.41 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.048/0.025

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.1021, from `lib-stage2-lean` at 0.9919 to `bq-expand-aa-distant` at 1.3117, with `list` itself at 1.2758. **The baseline moved 27.58% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.064, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.021, priced against `mut-odo-vecdims` at 0.4861 over 3 of 3 shapes at sign p 0.25, a margin of 51.39% against this class's 0.49% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 27.58 of a point, at a class geomean of 1.1021 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.45 points. The counted work reads a counts geomean of 1.1656 over the same arms, 16 of them counted. Its counted work parts by 16.56 points where its clock parts by 10.21, so about 0.62 of the instruction saving reaches the clock.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.57* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.52 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.33* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.015 | 0.020 | 0.50 | 62 | 1.00x |
| lib-stage2-lean | 0.015 | 0.020 | 0.43 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.020* | *0.51* | *62* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.015* | *0.020* | *0.40* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.020 | 0.41 | 62 | 1.00x |
| lib-stage1 | 0.015 | 0.020 | 0.43 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.020 | 0.47 | 62 | 1.00x |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.32* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.08 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.29* | *61* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.142* | *0.69* | *46* | *1.00x* |
| bq-expand | 0.091 | 0.142 | 0.67 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.091* | *0.143* | *0.12* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 0.98 | 17 | 20.99x |
| *list-aa-distant* | *1.006* | *1.012* | *0.95* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.007* | *1.010* | *0.80* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0070, worst cell 1.18% on `bcast-src512`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.01% on `bcast-tall-Mx2`, its interval covering 1. The in-situ term reads 1.0179, 1.0108 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0050, which the correction amplifies by 1.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m12s, peak 180 MiB in use, 42 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 31 ms per call raw, 29.9 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.015/0.019/0.019

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 1.0905, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9940 to `list` at 1.3978, with `list` itself at 1.3978. **The baseline moved 39.78% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.015, priced against `mut-odo-vecdims` at 0.6531 over 6 of 6 shapes at sign p 0.031, a margin of 34.69% against this class's 0.70% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 39.78 of a point, at a class geomean of 1.0905 over the 16 arms, with 2 of 8 strategies past an A/A bar of 0.63 points. The counted work reads a counts geomean of 1.1697 over the same arms, 16 of them counted. Its counted work parts by 16.97 points where its clock parts by 9.05, so about 0.53 of the instruction saving reaches the clock.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.45* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.37 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.31 | 82 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.34 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.29 | 82 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.01 | 97 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 97 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.30 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 97 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.28* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *89* | *0.00x* |
| lib-stage2-lean | 0.012 | 0.018 | 0.31 | 82 | 1.00x |
| lib-stage3-lean | 0.012 | 0.017 | 0.37 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.020 | 0.32 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.39 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.29* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.32* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.29 | 80 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.31* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.27 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.24* | *76* | *1.00x* |
| bq-expand | 0.099 | 0.182 | 0.41 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.099* | *0.183* | *0.31* | *61* | *1.92x* |
| *bq-expand-aa-adjacent* | *0.100* | *0.183* | *0.40* | *61* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 0.82 | 28 | 23.56x |
| *list-aa-adjacent* | *1.002* | *1.006* | *0.79* | *28* | *23.56x* |
| *list-aa-distant* | *1.005* | *1.012* | *0.88* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0051, worst cell 1.16% on `bcastmid-b200k`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.03% on `bcastmid-block150k`, its interval covering 1. The in-situ term reads 1.0196, 1.1217 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0050, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h10m50s, peak 122 MiB in use, 35 MiB max residency; the reader reads 31 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.7 ms per call raw, 47.6 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 1 of the 16 arms are faster on this half and 15 slower, at a geomean of 1.0990, from `lib-stage2-lean` at 0.9976 to `list-aa-distant` at 1.2780, with `list` itself at 1.2697. **The baseline moved 26.97% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.012, priced against `mut-odo-vecdims` at 0.4133 over 4 of 4 shapes at sign p 0.12, a margin of 58.67% against this class's 0.51% floor (`list-aa-distant`). Its two columns may NOT be differenced, `list` having moved 26.97 of a point, at a class geomean of 1.0990 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.66 points. The counted work reads a counts geomean of 1.1711 over the same arms, 16 of them counted. Its counted work parts by 17.11 points where its clock parts by 9.90, so about 0.58 of the instruction saving reaches the clock.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.33* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.17 | 84 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.18 | 84 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.18 | 84 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.19 | 84 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.06 | 105 | 0.02x |
| libunord-stage14-sum | -- | -- | 0.05 | 106 | 0.02x |
| libunord-stage15-sum | -- | -- | 0.05 | 106 | 0.02x |
| libunord-stage6-loop-sum | -- | -- | 0.15 | 100 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.07 | 102 | 0.02x |
| libunord-stage7-sum | -- | -- | 0.05 | 104 | 0.02x |
| libunord-stage9-sum | -- | -- | 0.06 | 102 | 0.02x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.31* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage2-lean | 0.023 | 0.027 | 0.20 | 84 | 1.00x |
| lib-stage1 | 0.024 | 0.027 | 0.17 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.029 | 0.18 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.19* | *82* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.17* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.15 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.085* | *0.17* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.051* | *0.085* | *0.19* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.085 | 0.15 | 76 | 1.00x |
| *bq-expand-aa-adjacent* | *0.175* | *0.216* | *0.31* | *57* | *3.86x* |
| bq-expand | 0.175 | 0.216 | 0.33 | 57 | 3.86x |
| *bq-expand-aa-distant* | *0.176* | *0.216* | *0.31* | *57* | *3.86x* |
| *list-aa-distant* | *0.999* | *1.011* | *0.49* | *30* | *27.66x* |
| *list-aa-adjacent* | *1.000* | *1.005* | *0.41* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.49 | 30 | 27.66x |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0021, worst cell 1.15% on `window-224x224-k3`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.06% on `window-128x128-k7`, its interval covering 1. The in-situ term reads 1.0056, 1.1618 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0018, which the correction amplifies by 1.17x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h21m29s, peak 121 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.7 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.085/0.031/0.052/0.052/0.053/0.051

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.1384, from `lib-stage1` at 0.9973 to `bq-expand-aa-distant` at 1.5236, with `list` itself at 1.2990. **The baseline moved 29.90% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.085, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.4157 over 8 of 8 shapes at sign p 0.0078, a margin of 58.43% against this class's 0.21% floor (`bq-expand-aa-distant`). Its two columns may NOT be differenced, `list` having moved 29.90 of a point, at a class geomean of 1.1384 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.42 points. The counted work reads a counts geomean of 1.1776 over the same arms, 16 of them counted. Its counted work parts by 17.76 points where its clock parts by 13.84, so about 0.78 of the instruction saving reaches the clock.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.07* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.14 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.18 | 128 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 128 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.27 | 128 | 1.00x |
| libunord-stage14-sum | -- | -- | 0.17 | 128 | 1.00x |
| libunord-stage15-sum | -- | -- | 0.22 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.19 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.18 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.22 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.14 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *138* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.031* | *0.18* | *128* | *1.00x* |
| lib-stage1 | 0.022 | 0.031 | 0.13 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.031* | *0.14* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.030 | 0.13 | 128 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.030 | 0.16 | 128 | 1.00x |
| lib-stage3-lean | 0.023 | 0.030 | 0.10 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.030 | 0.12 | 128 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.029* | *0.09* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.029 | 0.09 | 127 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.029* | *0.09* | *127* | *1.00x* |
| *bq-expand-aa-distant* | *0.091* | *0.101* | *0.08* | *111* | *1.21x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.102* | *0.06* | *111* | *1.21x* |
| bq-expand | 0.091 | 0.102 | 0.07 | 111 | 1.21x |
| list (baseline) | 1.000 | 1.000 | 0.27 | 69 | 21.49x |
| *list-aa-adjacent* | *1.005* | *1.006* | *0.20* | *69* | *21.49x* |
| *list-aa-distant* | *1.006* | *1.012* | *0.14* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0059, worst cell 1.24% on `scaled-r5`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.09% on `scaled-rank1-m1`, its interval covering 1. The in-situ term reads 1.0095, 1.0224 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0057, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m9s, peak 111 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.37 ms per call raw, 5.19 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.029/0.029

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.0701, from `lib-stage3-lean` at 0.9905 to `list-aa-distant` at 1.3388, with `list` itself at 1.3266. **The baseline moved 32.66% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the vecdims arms at 0.022, priced against `mut-odo-vecdims` at 0.8931 over 2 of 3 shapes at sign p 1, a margin of 10.69% against this class's 0.59% floor (`list-aa-distant`). Its two columns may NOT be differenced, `list` having moved 32.66 of a point, at a class geomean of 1.0701 over the 16 arms, with 3 of 8 strategies past an A/A bar of 0.92 points. The counted work reads a counts geomean of 1.1524 over the same arms, 16 of them counted. Its counted work parts by 15.24 points where its clock parts by 7.01, so about 0.46 of the instruction saving reaches the clock.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen, and cut to sixteen for Run 41, `runs-3` (`sInner` 3, a k3 conv row) leaving timing in `94aeee7` and staying in `check`.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.49* | *52* | *1.07x* |
| liblist-stage1-sum | -- | -- | 0.11 | 62 | 0.35x |
| liblist-stage4-sum | -- | -- | 0.02 | 75 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.10 | 62 | 0.35x |
| libunord-stage13-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.03 | 75 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 74 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 75 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 75 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 75 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *78* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage3-lean | 0.023 | 0.025 | 0.10 | 60 | 1.00x |
| lib-stage2-lean | 0.023 | 0.025 | 0.14 | 60 | 1.00x |
| lib-stage2-lean-u1 | 0.023 | 0.024 | 0.13 | 60 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.45* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.026 | 0.12 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.13* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.10* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.058 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.057* | *0.12* | *59* | *1.00x* |
| lib-stage1 | 0.086 | 1.100 | 0.16 | 52 | 1.35x |
| *bq-expand-aa-adjacent* | *0.091* | *0.141* | *0.42* | *46* | *1.07x* |
| bq-expand | 0.091 | 0.141 | 0.41 | 46 | 1.07x |
| *bq-expand-aa-distant* | *0.092* | *0.144* | *0.05* | *46* | *1.07x* |
| list (baseline) | 1.000 | 1.000 | 2.47 | 17 | 21.26x |
| *list-aa-distant* | *1.031* | *1.060* | *0.41* | *17* | *21.26x* |
| *list-aa-adjacent* | *1.032* | *1.044* | *0.22* | *17* | *21.26x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0317, worst cell 4.37% on `runs-r3-48x30`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.22% on `runs-2`, its interval covering 1. The in-situ term reads 1.0303, 1.0304 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0306, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h43m3s, peak 624 MiB in use, 270 MiB max residency; the reader reads 31 benchmarks over 16 shapes of the runs class. Anchor: `runs-2`, `list` at 40.9 ms per call raw, 39.9 ms net.

**Per shape, in the run's shape order (runs-2, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.058/0.040/0.038/0.033/0.030/0.025/0.025/0.025/0.024/0.024/0.024/0.024/0.024/0.024/0.025/0.025

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 1.0774, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9911 to `list` at 1.3267, with `list` itself at 1.3267. **The baseline moved 32.67% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.058, tiers at 1.00x, 1.07x, 21.26x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.023, priced against `mut-odo-vecdims` at 0.8047 over 16 of 16 shapes at sign p 3.1e-05, a margin of 19.53% against this class's 3.17% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 32.67 of a point, at a class geomean of 1.0774 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.35 points. The counted work reads a counts geomean of 1.1601 over the same arms, 16 of them counted. Its counted work parts by 16.01 points where its clock parts by 7.74, so about 0.48 of the instruction saving reaches the clock.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.40* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.17 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.11 | 93 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.11 | 93 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 83 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.24* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.021 | 0.042 | 0.23 | 84 | 1.00x |
| lib-stage3-lean | 0.022 | 0.042 | 0.32 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.046 | 0.28 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.34* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.043 | 0.16 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.043* | *0.09* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.053* | *0.09* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.053* | *0.11* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.053 | 0.13 | 77 | 1.00x |
| lib-stage1 | 0.033 | 0.048 | 0.32 | 82 | 1.00x |
| bq-expand | 0.090 | 0.182 | 0.43 | 61 | 1.05x |
| *bq-expand-aa-adjacent* | *0.091* | *0.182* | *0.44* | *61* | *1.05x* |
| *bq-expand-aa-distant* | *0.092* | *0.182* | *0.12* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.64 | 32 | 21.18x |
| *list-aa-distant* | *1.007* | *1.018* | *0.55* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.008* | *1.025* | *0.26* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0082, worst cell 2.52% on `flip-last-rows`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.22% on `flip-last-rows`, its interval covering 1. The in-situ term reads 1.0210, 1.0223 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0080, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m13s, peak 209 MiB in use, 76 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31.1 ms per call raw, 30 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.053/0.047/0.026/0.026

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0853, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9932 to `list-aa-adjacent` at 1.3326, with `list` itself at 1.3305. **The baseline moved 33.05% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.021, priced against `mut-odo-vecdims` at 0.7251 over 6 of 6 shapes at sign p 0.031, a margin of 27.49% against this class's 0.82% floor (`list-aa-adjacent`). Its two columns may NOT be differenced, `list` having moved 33.05 of a point, at a class geomean of 1.0853 over the 16 arms, with 7 of 8 strategies past an A/A bar of 0.45 points. The counted work reads a counts geomean of 1.1523 over the same arms, 16 of them counted. Its counted work parts by 15.23 points where its clock parts by 8.53, so about 0.56 of the instruction saving reaches the clock.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.15 | 113 | 0.42x |
| liblist-stage4-sum | -- | -- | 0.02 | 130 | 0.00x |
| liblist-stage5-sum | -- | -- | 0.03 | 130 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 113 | 0.42x |
| libunord-stage13-sum | -- | -- | 0.03 | 130 | 0.00x |
| libunord-stage14-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage15-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.04 | 130 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 130 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 130 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *130* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *122* | *0.00x* |
| lib-stage3-lean | 0.020 | 0.023 | 0.12 | 112 | 1.00x |
| lib-stage2-lean | 0.020 | 0.023 | 0.11 | 112 | 1.00x |
| lib-stage2-lean-u1 | 0.020 | 0.025 | 0.10 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.11* | *112* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.08 | 112 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.024* | *0.10* | *111* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.11* | *111* | *1.00x* |
| lib-stage1 | 0.050 | 0.057 | 0.14 | 103 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.086* | *0.12* | *96* | *1.06x* |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.08* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.086 | 0.11 | 96 | 1.06x |
| *list-aa-distant* | *0.997* | *1.003* | *0.20* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.30 | 54 | 21.22x |
| *list-aa-adjacent* | *1.000* | *1.008* | *0.20* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 1.0047, worst cell 1.34% on `block-r3-vol64`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9994 on a worst cell of 0.35% on `block-r3-vol64`, its interval covering 1. The in-situ term reads 1.0205, 1.0191 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0016, which the correction amplifies by 2.51x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m29s, peak 134 MiB in use, 47 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.67 ms per call raw, 4.51 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.029/0.024/0.019

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 1.0636, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9795 to `list` at 1.3536, with `list` itself at 1.3536. **The baseline moved 35.36% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.020, priced against `mut-odo-vecdims` at 0.8609 over 5 of 5 shapes at sign p 0.062, a margin of 13.91% against this class's 0.47% floor (`mut-odo-vecdims-aa-distant`). Its two columns may NOT be differenced, `list` having moved 35.36 of a point, at a class geomean of 1.0636 over the 16 arms, with 5 of 8 strategies past an A/A bar of 1.00 points. The counted work reads a counts geomean of 1.1492 over the same arms, 16 of them counted. Its counted work parts by 14.92 points where its clock parts by 6.36, so about 0.43 of the instruction saving reaches the clock.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.15 | 228 | 1.69x |
| liblist-stage4-sum | -- | -- | 0.15 | 243 | 1.17x |
| liblist-stage5-sum | -- | -- | 0.10 | 243 | 1.17x |
| libunord-stage1-sum | -- | -- | 0.21 | 223 | 2.08x |
| libunord-stage13-sum | -- | -- | 0.10 | 244 | 0.20x |
| libunord-stage14-sum | -- | -- | 0.14 | 244 | 0.20x |
| libunord-stage15-sum | -- | -- | 0.10 | 244 | 0.20x |
| libunord-stage6-loop-sum | -- | -- | 0.23 | 239 | 0.55x |
| libunord-stage6-sum | -- | -- | 0.27 | 239 | 0.55x |
| libunord-stage7-sum | -- | -- | 0.20 | 239 | 0.55x |
| libunord-stage9-sum | -- | -- | 0.24 | 238 | 0.43x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.27* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.05* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.02* | *250* | *0.01x* |
| lib-stage3-lean | 0.033 | 0.050 | 0.17 | 235 | 1.13x |
| lib-stage2-lean | 0.034 | 0.050 | 0.10 | 235 | 1.13x |
| lib-stage2-lean-u1 | 0.035 | 0.050 | 0.19 | 234 | 1.13x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.053* | *0.068* | *0.28* | *230* | *1.28x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.053 | 0.068 | 0.25 | 230 | 1.28x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.053* | *0.068* | *0.25* | *229* | *1.28x* |
| *mut-odo-vecdims-aa* | *0.061* | *0.088* | *0.17* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.061** | 0.088 | 0.19 | 229 | 1.27x |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.088* | *0.21* | *229* | *1.27x* |
| lib-stage1 | 0.083 | 0.108 | 0.19 | 221 | 2.36x |
| bq-expand | 0.137 | 0.199 | 0.10 | 217 | 1.44x |
| *bq-expand-aa-adjacent* | *0.137* | *0.199* | *0.12* | *217* | *1.44x* |
| *bq-expand-aa-distant* | *0.137* | *0.199* | *0.15* | *217* | *1.44x* |
| *list-aa-adjacent* | *1.000* | *1.002* | *0.14* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 180 | 21.57x |
| *list-aa-distant* | *1.000* | *1.003* | *0.20* | *180* | *21.57x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0076, worst cell 1.83% on `small-flat64`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.10% on `small-patch-k5`, its interval covering 1. The in-situ term reads 0.9880, 0.9816 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0049, which the correction amplifies by 1.61x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h13m31s, peak 132 MiB in use, 52 MiB max residency; the reader reads 31 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.67 us per call raw, 6.44 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.042/0.077/0.050/0.058/0.088

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0797, from `lib-stage2-lean` at 0.9798 to `list-aa-adjacent` at 1.2900, with `list` itself at 1.2784. **The baseline moved 27.84% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage3-lean` leads outside the vecdims arms at 0.033, priced against `mut-odo-vecdims` at 0.4441 over 5 of 5 shapes at sign p 0.062, a margin of 55.59% against this class's 0.76% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). Its two columns may NOT be differenced, `list` having moved 27.84 of a point, at a class geomean of 1.0797 over the 16 arms, with 6 of 8 strategies past an A/A bar of 0.91 points. The counted work reads a counts geomean of 1.1450 over the same arms, 16 of them counted. Its counted work parts by 14.50 points where its clock parts by 7.97, so about 0.55 of the instruction saving reaches the clock.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500), and the two views that landed 2026-09-26, for Run 42 --- `compose-bcast-nest` (`l` 4992, `sInner` 2) and `compose-bcast-wide` (`l` 4992, `sInner` 52). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero; the two new ones put a broadcast beside runs of 3 under a reversed nest --- of extent 2 under a nest of three levels nothing merges on `compose-bcast-nest`, of extent 52 under a nest of five twos on `compose-bcast-wide` --- so that where the unordered stages place the zero-stride axis decides which extent the odometer turns over on.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.13* | *118* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.37 | 134 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.36 | 134 | 1.00x |
| liblist-stage5-sum | -- | -- | 0.34 | 134 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.36 | 134 | 1.01x |
| libunord-stage13-sum | -- | -- | 0.09 | 141 | 0.09x |
| libunord-stage14-sum | -- | -- | 0.04 | 141 | 0.09x |
| libunord-stage15-sum | -- | -- | 0.05 | 141 | 0.05x |
| libunord-stage6-loop-sum | -- | -- | 0.36 | 134 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.32 | 134 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.33 | 134 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.09 | 141 | 0.10x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.23* | *143* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *141* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *141* | *0.00x* |
| lib-stage2-lean | 0.017 | 0.038 | 0.34 | 134 | 1.00x |
| lib-stage3-lean | 0.017 | 0.036 | 0.34 | 134 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.017* | *0.043* | *0.36* | *134* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.017 | 0.043 | 0.27 | 134 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.017* | *0.043* | *0.30* | *134* | *1.00x* |
| lib-stage2-lean-u1 | 0.018 | 0.039 | 0.29 | 133 | 1.00x |
| lib-stage1 | 0.019 | 0.039 | 0.33 | 134 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.072* | *0.24* | *128* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.072 | 0.24 | 128 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.072* | *0.19* | *128* | *1.00x* |
| bq-expand | 0.102 | 0.220 | 0.07 | 112 | 1.44x |
| *bq-expand-aa-adjacent* | *0.102* | *0.220* | *0.08* | *112* | *1.44x* |
| *bq-expand-aa-distant* | *0.102* | *0.220* | *0.14* | *112* | *1.44x* |
| *list-aa-distant* | *1.000* | *1.004* | *0.22* | *71* | *22.17x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 71 | 22.17x |
| *list-aa-adjacent* | *1.002* | *1.007* | *0.19* | *71* | *22.17x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0058, worst cell 1.57% on `compose-bcast-nest`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.04% on `compose-rev-bcast`, its interval covering 1. The in-situ term reads 1.0007, 1.0143 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0026, which the correction amplifies by 2.75x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h16m13s, peak 126 MiB in use, 36 MiB max residency; the reader reads 31 benchmarks over 6 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar, compose-bcast-nest, compose-bcast-wide):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019/0.072/0.026

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0896, from `lib-stage2-lean` at 0.9914 to `list-aa-distant` at 1.3289, with `list` itself at 1.3262. **The baseline moved 32.62% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.072, tiers at 1.00x, 1.44x, 22.17x --- and `lib-stage2-lean` leads outside the vecdims arms at 0.017, priced against `mut-odo-vecdims` at 0.6080 over 6 of 6 shapes at sign p 0.031, a margin of 39.20% against this class's 0.58% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). Its two columns may NOT be differenced, `list` having moved 32.62 of a point, at a class geomean of 1.0896 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.49 points. The counted work reads a counts geomean of 1.1632 over the same arms, 16 of them counted. Its counted work parts by 16.32 points where its clock parts by 8.96, so about 0.55 of the instruction saving reaches the clock. **Registration item (4)'s three cells are this class's, and all three held**: stage fifteen over stage fourteen reads 2.0242 on `compose-bcast-nest` and 0.3706 on `compose-bcast-wide` on the basis, 2.0127 and 0.3772 on the control, and 1.0000 on `compose-rev-bcast` on both ([the registration](#what-this-run-was-built-to-answer-and-what-it-answered)).


## Provenance

**Run 42's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `eb76398`; one shim, `align-as.py` at `1a359bd`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`, which is Runs 36's to 41's compiler unmoved; one roster, one shape set, one class list and one bench order; one allocation area, `-A32m`, baked into the cabal file since 2026-08-21 and fixed for every process here; both halves built with `-fobject-determinism`, both launched FROM DISK, `hugebin/` being unmounted, and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run42-gheadnospec` and is what every table here publishes; `run42-gheadtwopass` is the candidate. **What is new against Run 41 is not the pair but the source under both halves**: `Main.hs` moved six of the owner's commits, `688e952` to `eb76398`, while the shim, the recipes, the project file, the compiler and the launch are Run 41's to the character, and no reboot sits between the two runs, `uptime` putting the box up since 2026-09-24 00:00 at both.

**The roster is 31 timed arms over 19 main-set shapes and 589 benches, with 62 class views over ten classes for 1922 more, and it is Run 41's PLUS ONE ARM AND TWO VIEWS.** `./roster-delta.py run41-gheadnospec run42-gheadnospec`, read off the two binaries, puts one arm in, `libunord-stage15-sum` (`eb76398`), and two `compose` views in, `compose-bcast-nest` and `compose-bcast-wide` (`e1ab85c`), and nothing out: the other 30 arms run in Run 41's order over the same nineteen main-set shapes, and the other nine classes' views are unmoved. So pre-run step 12's condition fired, and the -L1 roster pass it owes was taken on 2026-09-26 over every class and read clean; every cross-run figure in this file is read over the 30 arms both runs time and, on `compose`, over the four views both ran.

**The evening ran in ONE window and in the order the run list gives, and nothing foreign reached it.** `run-evening.sh` took the gate from 01:11:15 to 01:44:36, the alarm at 01:44:40 reading 0.2% busy, the sequence from 2026-09-27T01:44:40 to 2026-09-27T09:00:47 and the riders from 09:00:47 to 09:13:15, every stage exiting 0; the wall-clock log puts the twenty-two sequence processes back to back, the largest hole between one finishing and the next starting 0m, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones --- and each launched from `./run42-<half>`. The counted work, which wants no quiet machine, ran from 09:13, with the `-g3` twins building beside it. **`--wild` finds no bench at or above 0.25 of a core foreign in any of the twenty-two sequence logs**, so post-run step 3 owed no rerun.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes read `list` 1.3005 and 1.3048, `mut-odo-vecdims` 0.9995 and 1.0040, `bq-expand` 1.3130 and 1.3124 --- 0.43, 0.45, 0.06 points apart. Between its own two legs `gheadnospec` moved by at most 0.31 points, on `bq-expand`, and `gheadtwopass` by at most 0.57 points, on `mut-odo-vecdims`, so what the passes part by is the control's legs and not a disagreement about the pair; `mut-odo-vecdims`, the arm the two passes leave alone, sits either side of 1 inside that drift (`./read-run.py --gate-draft run42` prints all four readings). The machine check, read against the fingerprint Run 41 installed --- this run's basis recipe on the source before the six commits --- puts `list`'s net at **+0.81%**, worst `stretch-pow2stride` at **+1.98%**, none of 19 shapes past 5% and the geomean inside the 3% bar, so the six commits moved the box's `list` by under the bars. `bq-expand` read 1.31 in both passes, where Run 41's gate read 1.36, the first sign of the basis half's family coming back, which [What the next run compares against](#what-the-next-run-compares-against) reads on the run.

**Every one of the twenty-two processes gated clean, the plateau refused by declaration, and the two A/A worst cells past 5% are both on `runs`.** `read-all.sh` gates each process on its own correction and passes 22 of 22. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.9147 to 21.3646 ms/iter across the run, a 26.31% spread against a 5% band, and it splits exactly by half, `gheadnospec`'s 11 processes flat within 1.14% at 21.1238 to 21.3646 and `gheadtwopass`'s within 1.96% at 16.9147 to 17.2466 --- so both halves are flat within a few points, which is what the declaration covers, and the refusal is the pair's variable. The A/A worst cells past 5% are `gheadtwopass-runs` at **6.49%** on `runs-65536` and `gheadnospec-runs` at **6.04%** on `runs-1024`, in the population whose floor is the widest of the eleven on both halves, 3.17% on the basis and 3.49% on the control; the main set's floor is 0.26% on the basis and 0.49% on the control. **No cell reaches the about 10% [the procedure][procedure] gates on**, so no cell leaves the per-shape record this run.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run42-gheadnospec`, md5 `a16d88128431822e807fc1b77c29a7f1`, and `run42-gheadtwopass`, md5 `0279d029139b8b526bd0027a867531ac`, built on 2026-09-26 from `Main.hs` at `eb76398`, clean against it, and run from a tree at `e8b549a`. Their `.text` sections are **20154175** and **20203327** bytes, the first column of `size -A`; against Run 41's two the basis is smaller by 20480 bytes and the flagged half by 36864, five and nine pages exactly --- the six commits, recorded and not apportioned. **NEITHER md5 reproduces anything**, the source having moved; what the two md5s do instead is DIFFER, which is the two passes having reached the emission. The flagged half is again the LARGER binary, by 49152 bytes, twelve pages exactly, and it carries MORE self-loops, 296 against 293, so [the open list's entry on it](../README.md#what-is-open) gains a run on that side.

**The six commits moved no 28-byte copy off its offset in the two groups that kept their copies, and took one copy from each of the other two.** `./loop-offsets.py --delta run41-gheadnospec run42-gheadnospec`, the same basis recipe on the two sources, keeps every mod-64 offset of the six-copy group at [0, 0, 0, 0, 0, 0] and of the two-copy group at [0, 0], with no address surviving to the byte and every displacement a whole number of lines, four on the first group and two on the second; the two three-copy groups Run 41's basis carried at [0, 0, 0] and [11, 11, 11] have two copies each, at [0, 3] and [11, 14]. **Within the pair** the six-copy group reads [0, 0, 0, 0, 0, 0] on both halves, the two-copy group [0, 0] on both and the two groups just named [0, 3] and [11, 14] on both, and a three-copy group at [0, 0, 0] exists on the control half alone, as on Run 41. `--library` puts **4.3%** of the 805 library self-loops the two halves share at the same offset in line, Run 41's 4.3% to the tenth: the switch places `_Main_`-compiled heads, and the library's loops read as they did.

**The straddling loops stand at 27 on the basis and 26 on the control, where Run 41 read 29 and 33, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 293 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 296 on the control, 194 and 131 of them at offset 0, where Run 41 read 336 and 348 self-loops, and 0 exit spans astride on each, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 3a's naming, taken off the binaries that were timed with both halves' `-g3` twins and `--loose`, names by byte identity eleven straddlers on the basis and thirteen on the control** --- on both, `sumNoSpec` twice, `fillStage3`'s body at offset 30, `fillStage2Short` twice, `fillStage2Axes`, the leaf bodies of `fbMutOdoVecdimsAddInLeafU2` twice, `-Down` and `-Last`, and `fbMutOdoVecdimsAddInLeafU2Ptr`; on the control `fillStage2OneLevel` and `fbFused` besides. Of the refusals, eight on the basis and six on the control carry a `--loose` family of `fillStage3`, `fillStage2Short`, `fillStage2VSdims`, `fillStage2OneLevel` and `fillStage2Axes` bodies, which the bytes cannot choose between, and eight on the basis and seven on the control are 60- to 63-byte bodies at offset 32, 40 or 48 for which no twin holds a copy. **The basis's own `-g3` twin holds as many loops as the basis binary, 293, and the control's own twin more than the control binary, 298 against 296**; only the basis's twin, read across to name the control's loops, holds fewer than the binary it names for, so a name it gives there rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run42-gheadnospec`, 9.992 times apart, which is plain -O1; on `run42-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. Both builders' figures are Run 41's to the byte on both halves. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.29 us** on `cnn-slice-c32`, **3.71 ms** on `cnn-L2-24x24-c32` and **39.5 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and sits 19.2 to 20.6 points below the basis on the three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.46 us | 6.29 us | 5.08 us |
| `cnn-L2-24x24-c32` | 165888 | 3.81 ms | 3.71 ms | 2.95 ms |
| `stretch-wide-2xM` | 1800000 | 40.5 ms | 39.5 ms | 31.9 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.56 ms raw and 4.41 ms net; `bcast-inner900` 31 ms raw and 29.9 ms net; `bcastmid-b200k` 48.7 ms raw and 47.6 ms net; `window-128x128-k7` 14.2 ms raw and 13.7 ms net; `scaled-rank1-m1` 5.37 ms raw and 5.19 ms net; `runs-2` 40.9 ms raw and 39.9 ms net; `flip-fwd-rows96` 31.1 ms raw and 30 ms net; `block-r3-vol64` 4.67 ms raw and 4.51 ms net; `small-row96` 6.67 us raw and 6.44 us net; `compose-zero-mid` 30.9 ms raw and 29.8 ms net. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and no cell of the whole run is one the reader flags.** The two `sum-only` arms agree on every population and on both halves of the pair --- as `--aa` prints it, late over early, 0.9994 to 1.0002 across the twenty-two processes, at a mean absolute difference of at most 0.19% --- so the term subtracted from one half is the term subtracted from the other. **No cell sits below R2 0.99 ([what that column detects][ramp]) and none is under ten samples**, of the run's 5022 cells, 2511 on each half; the reader's warnings print for none of the twenty-two JSONs.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, none refused, at a cost of 1278s on the basis and 1049s on the control --- beside Run 41's 1266s and 1035s, on a roster one arm and two views larger and with this run's `-g3` twins building and its first readings running alongside, which an instruction count does not see. The counts geomean over the sixteen arms that carry a corrected time runs **1.1450** on `small` to **1.1776** on `window`, the main set at **1.1673** --- the basis retiring 14.5 to 17.8 percent more instructions than the flagged half, and more in every population. **On the main set `time/counts` separates the families**: the `bq-expand` trio sits at 0.8670 to 0.8695, retiring 50.63% more instructions on the basis for 30.60 to 30.97% more time, where Run 41's trio sat at 0.9003 to 0.9048 and Run 40's at 0.8669 to 0.8691 on the same instruction ratio --- which is the basis half's `bq-expand` back where Run 40's build had it; the `list` trio at 0.9980 to 1.0018, cashing all of what it saves; and the ten others between 0.9401 and 0.9650, retiring 3.83 to 5.47 percent more on the basis while their clocks run from 0.85 of a point below level to 0.26 above. **Read per class the same way, the rate runs 0.43 to 0.78**: the instruction saving reaching the clock is lowest on `block`, where the counted work parts by 14.92 points and the clock by 6.36, and highest on `window`, 17.76 against 13.84 --- where Run 41 read 0.44 to 0.88, `window`'s top end then carrying the basis half's `bq-expand` move, and Run 40 read 0.37 to 0.78.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0000** and **1.0000** on the two halves of the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0303** and **1.1059** on the basis and **1.0323** and **1.0605** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and about eleven and six on `bq-expand`, the term that is subtracted being the `sum-only` one and not this proxy.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, after the sequence on the same quiet box, and the state the preamble puts on a process comes back at a geomean of **1.1172** on the basis and **1.1611** on the control, **4.4** points apart, where Run 41's two parted by 4.3 and Run 40's by 4.7 --- so the two passes change what the spray costs a process as well as what the roster costs it, by within a point of what they changed it by on the two runs before. What the roster adds on top of that state is **1.0203** on the basis, 7 of 19 shapes above 1, and **1.0111** on the control, 8 of 19; the basis's rest runs 0.9818 on `stretch-bigstride` to 1.2065 on `stretch-r5-8x432`, the control's 0.9740 on `stretch-bigstride` to 1.1272 on `stretch-tall-Mx2`. The whole in-process deflation is **1.1399** on the basis, 17 of 19 shapes above 1, and **1.1740** on the control, 19 of 19.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 41's, both recipes unchanged to the character and rebuilt on `Main.hs` at `eb76398` where Run 41 built from `688e952`, on the owner's word of 2026-09-26 that this run builds the previous run's recipes and focuses on the new code, shapes and roster: both halves GHC HEAD `10.1.20260918` through `cabal.project.ghead` at plain `-O1`, `align-as.py` at `1a359bd` as for Run 41, under `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 LOOP_SETTLED=1`, `-fobject-determinism` on both, the control's line carrying `-fspec-constr -fliberate-case` besides, every process launched from disk, the half names `run42-gheadnospec` and `run42-gheadtwopass`. THIS ENTRY IS THE ONE DECLARATION SITE by the ruling of 2026-09-19, the command lines being Run 41's with the builddir names moved. So the pair's own `cross` figure is the two passes read a seventh time, in `--compare`'s orientation of the unflagged basis over the control, and the source is read as each half against Run 41's same half, `--half-movers run42 run41`; the shim, the compiler and the project file did not move. The six commits bring one arm in, `libunord-stage15-sum`, and two views into `compose`, `compose-bcast-nest` and `compose-bcast-wide`, and take nothing out --- `./roster-delta.py run41-gheadnospec run42-gheadnospec` reads the other 30 arms in the same order --- and `./registration-drift.py run42 --since run41` reaches every timed arm whose name begins `lib` and no code behind `list`, `bq-expand` or any `mut-odo-vecdims` arm. What they change behind the arms the items read, off the diffs: `lib-stage2-lean-u1` moves onto the `Axis` path as `fillStage3U1` behind `routeList5`, so that it differs from `lib-stage3-lean` in its run bodies alone (`08b4f19`); `lib-stage2-lean`'s merge and nest become loops of the `Axis` path's form over pairs, so that the two lean arms differ in what rests on `Axis` alone (`7ca5d40`, `08b4f19`); `lib-stage1` fills through `fillStage3`, converting its walk with `walkAx` on every call, and so no longer fills as the library does (`c7549d2`); and `libunord-stage15-sum` is `libunord-stage14-sum` with the zero-stride axis consed just outside the run where stage fourteen appends it outermost (`eb76398`). **The items' priors are instruction counts off this run's own basis binary**, `run42-gheadnospec`, taken with `probe-stalls.sh` at `N=50`, Run 41's counts N, twice: into `probe-r42-prior1.txt` and `probe-r42-prior2.txt` over the nineteen main-set shapes, and into `probe-r42-prior1-compose.txt` and `probe-r42-prior2-compose.txt` over `compose`, the two sweeps' instructions agreeing to 0.1% on every cell; and allocation a call on three `compose` views, in `probe-r42-alloc-compose.txt`. They are read RAW, as Run 41's priors were. The cycles the sweeps carry are no prior: they were taken under the roster pass, and they read stage fifteen over fourteen on `compose-bcast-nest` at 0.49 in one sweep and 1.93 in the other, so no cycle figure is quoted below. No probe was taken on the control's recipe, so the priors are the basis's, carried to the control on Run 41's two halves agreeing within a point on each of items (1) to (3)'s pairs. **The limit this run cannot remove**: a rebuild moves every loop, and Run 41's `bq-expand` moved on one half with its instructions level, so an untouched arm's cross figure is predicted only within the spread its earlier builds drew.

(1) *On one path, `lib-stage2-lean-u1` keeps the distance it held from `lib-stage3-lean` when the two differed in path as well.* In `probe-r42-prior1.txt`, u1 over lean3 in instructions runs from 0.956 on `stretch-wide-2xM` to 1.035 on `stretch-bigstride`, a geomean of 1.0206, where `run41-counts-gheadnospec.txt` reads 1.0216, `--counts --pair lib-stage2-lean-u1 lib-stage3-lean` raw on Run 41's main JSON. Run 41 read the pair in time at 1.0703 on the basis and 1.0693 on the control, `--pair lib-stage2-lean-u1 lib-stage3-lean` on the two main JSONs. `predict: pair lib-stage2-lean-u1 lib-stage3-lean 1.07 within 3% on main both`. A reading below 1.04 says part of Run 41's distance was the path and not the run bodies; one above 1.10 says the `Axis` path costs the unrolled bodies time their instructions do not show.

**Read by --predictions, item (1):** `pair lib-stage2-lean-u1 lib-stage3-lean 1.07 within 3% on main both`: HELD on main basis, read 1.0690 over 19 shape(s), 0.10 point(s) off, within 3.00%; HELD on main control, read 1.0654 over 19 shape(s), 0.46 point(s) off, within 3.00%.

(2) *With both lean fills merging and nesting in loops, `lib-stage3-lean` stays level with `lib-stage2-lean`.* In `probe-r42-prior1.txt`, lean3 over lean2 in instructions runs from 0.994 on `cnn-slice-c32` to 1.000, a geomean of 0.9994, where `run41-counts-gheadnospec.txt` reads 0.9990, `--counts --pair` raw on Run 41's main JSON. Run 41 read the pair in time at 0.9904 on the basis and 0.9948 on the control, `--pair lib-stage3-lean lib-stage2-lean` on the two main JSONs. `predict: pair lib-stage3-lean lib-stage2-lean 0.99 within 2% on main both`. A reading below 0.97 says the `Axis` side buys time its instructions do not show; one above 1.01 says the loops over pairs bought `lib-stage2-lean` time they did not buy its `Axis` twin.

**Read by --predictions, item (2):** `pair lib-stage3-lean lib-stage2-lean 0.99 within 2% on main both`: HELD on main basis, read 1.0005 over 19 shape(s), 1.05 point(s) off, within 2.00%; HELD on main control, read 0.9961 over 19 shape(s), 0.61 point(s) off, within 2.00%.

(3) *`lib-stage1`'s `walkAx` conversion a call leaves it where Run 41 read it against the untouched `-u2`.* In `probe-r42-prior1.txt`, `lib-stage1`'s instructions a call read 1.0303 of `run41-counts-gheadnospec.txt`'s on `cnn-L1-6x6-c1` and 1.0220 on `cnn-slice-c32`, 420 and 214 more a call, and within 0.7% of them on the other seventeen shapes, a geomean of 1.0033, while `mut-odo-vecdims-add-in-leaf-u2`'s read 1.0000; `lib-stage1` over `-u2` reads 0.9736 in instructions, where Run 41's counts read 0.9704. Run 41 read the pair in time at 0.9897 on the basis and 0.9909 on the control, `--pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2` on the two main JSONs. `predict: pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 0.993 within 2% on main both`. A reading above 1.013 says the conversion costs time beyond its instructions; one below 0.973 says the `Axis` fill runs `lib-stage1` faster than the fill it replaced, which its instructions do not show.

**Read by --predictions, item (3):** `pair lib-stage1 mut-odo-vecdims-add-in-leaf-u2 0.993 within 2% on main both`: HELD on main basis, read 1.0009 over 19 shape(s), 0.79 point(s) off, within 2.00%; HELD on main control, read 1.0058 over 19 shape(s), 1.28 point(s) off, within 2.00%.

(4) *`libunord-stage15-sum`'s placement of the zero-stride axis pays on `compose-bcast-wide`, costs on `compose-bcast-nest`, and is level where the move passes no axis.* In `probe-r42-prior1-compose.txt`, stage fifteen over fourteen in instructions reads 1.5794 on `compose-bcast-nest` and 0.4570 on `compose-bcast-wide`, or 0.4288 over stage fourteen's `-n 3N` increment, that cell being `NONLINEAR` in instructions in both sweeps, at 147469 then 157177 a call in this one, and 27 instructions fewer of about 257600 on `compose-rev-bcast`; `probe-r42-alloc-compose.txt` puts its allocation a call at 37208 bytes against 7089 on the first, 3805 against 66041 on the second, and 561 on both on the third. Over the main set, `probe-r42-prior1.txt` reads the pair at 1.0000 in instructions, 0.999 to 1.001 by shape. No timing of the pair exists, so the two moving cells' bands are the instruction ratios widened for what the bytes may add: `predict: cell compose-bcast-nest/libunord-stage15-sum over compose-bcast-nest/libunord-stage14-sum 1.7 within 50% on compose both`, `predict: cell compose-bcast-wide/libunord-stage15-sum over compose-bcast-wide/libunord-stage14-sum 0.45 within 25% on compose both`, `predict: cell compose-rev-bcast/libunord-stage15-sum over compose-rev-bcast/libunord-stage14-sum 1.00 within 3% on compose both`, and `predict: pair libunord-stage15-sum libunord-stage14-sum 1.00 within 3% on main both`, the 3% set against the 2.3 points Run 29's item (7) read between two routes identical where no zero stride exists, on `rev`. A `compose-bcast-nest` reading under 1.2 or a `compose-bcast-wide` one over 0.70 says the time follows neither the instructions nor the bytes; a level cell or the main set reading outside 3% is placement, as Run 29's was.

**Read by --predictions, item (4):** `cell compose-bcast-nest/libunord-stage15-sum over compose-bcast-nest/libunord-stage14-sum 1.7 within 50% on compose both`: HELD on compose basis, read 2.0242 over 1 shape(s), 32.42 point(s) off, within 50.00%; HELD on compose control, read 2.0127 over 1 shape(s), 31.27 point(s) off, within 50.00% --- `cell compose-bcast-wide/libunord-stage15-sum over compose-bcast-wide/libunord-stage14-sum 0.45 within 25% on compose both`: HELD on compose basis, read 0.3706 over 1 shape(s), 7.94 point(s) off, within 25.00%; HELD on compose control, read 0.3772 over 1 shape(s), 7.28 point(s) off, within 25.00% --- `cell compose-rev-bcast/libunord-stage15-sum over compose-rev-bcast/libunord-stage14-sum 1.00 within 3% on compose both`: HELD on compose basis, read 1.0000 over 1 shape(s), 0.00 point(s) off, within 3.00%; HELD on compose control, read 1.0000 over 1 shape(s), 0.00 point(s) off, within 3.00% --- `pair libunord-stage15-sum libunord-stage14-sum 1.00 within 3% on main both`: HELD on main basis, read 1.0008 over 19 shape(s), 0.08 point(s) off, within 3.00%; HELD on main control, read 0.9999 over 19 shape(s), 0.01 point(s) off, within 3.00%.

(5) *The regime's worth on `list` holds at its level, and on `bq-expand` stays inside the spread its builds have drawn.* `--record regime` reads `list` over the nineteen shapes at 1.2960, 1.2889, 1.2966, 1.2983 and 1.2926 on Runs 37 to 41's builds, inside 0.94 points, with Run 36's 1.3360 above them, and `bq-expand` at 1.2980 to 1.3101 on Runs 36 to 40's and 1.3620 on Run 41's, the basis half's family having moved with that build. `predict: cross list 1.295 within 1% on main basis`, and `predict: cross bq-expand 1.33 within 3.5% on main basis`, the band reaching every draw. A `list` reading outside its band says the regime's worth moved with this build; a `bq-expand` one outside says the build term exceeds anything the six builds before it drew.

**Read by --predictions, item (5):** `cross list 1.295 within 1% on main basis`: HELD on main basis, read 1.2905 over 19 shape(s), 0.45 point(s) off, within 1.00% --- `cross bq-expand 1.33 within 3.5% on main basis`: HELD on main basis, read 1.3097 over 19 shape(s), 2.03 point(s) off, within 3.50%.

**All five items hold by their kill conditions, on every span on every half each names: nine spans, sixteen readings, none killed --- item (3)'s pair moving a point off Run 41's reading, inside its band.** Every verdict below is its item's KILL CONDITION applied across the populations and halves it names, every figure re-derived from this run's own JSONs and count sweeps, by `--predictions` over the main set and `compose` on each half and by `--pair` with `--counts` for the instructions.

(1) *On one path, `lib-stage2-lean-u1` keeps the distance it held from `lib-stage3-lean` when the two differed in path as well.* **HELD on both halves.** The pair reads **1.0690** on the basis and **1.0654** on the control, inside 3% of 1.07 and clear of both ends the item named --- above the 1.04 that would say part of Run 41's distance was the path, and under the 1.10 that would say the `Axis` path costs the unrolled bodies time --- beside Run 41's 1.0703 and 1.0693. The instructions came out as the prior said, **1.0206** raw on the basis against the prior's 1.0206 and 1.0219 on the control; net of the forcing pass the excess is 4.74% on the basis and 4.75% on the control, and the time excess runs past it on both halves, at 1.46 and 1.38 of it.

(2) *With both lean fills merging and nesting in loops, `lib-stage3-lean` stays level with `lib-stage2-lean`.* **HELD on both halves.** The pair reads **1.0005** on the basis and **0.9961** on the control, inside 2% of 0.99 and clear of both ends --- over the 0.97 that would say the `Axis` side buys time its instructions do not show, and under the 1.01 that would say the loops over pairs bought `lib-stage2-lean` time --- where Run 41 read 0.9904 and 0.9948. The instructions came out as predicted, **0.9994** raw on the basis against the prior's 0.9994, 0.9990 net of the forcing pass on the basis and 0.9992 on the control, so the two fills now differ by a tenth of a point of instructions and by under half a point of time on either half, the basis's reading on the other side of 1 from the control's.

(3) *`lib-stage1`'s `walkAx` conversion a call leaves it where Run 41 read it against the untouched `-u2`.* **HELD on both halves.** The pair reads **1.0009** on the basis and **1.0058** on the control, inside 2% of 0.993 and clear of both ends --- under the 1.013 that would say the conversion costs time beyond its instructions, and over the 0.973 that would say the `Axis` fill runs `lib-stage1` faster --- where Run 41 read 0.9897 and 0.9909. The instructions came out as predicted, **0.9736** raw on the basis against the prior's 0.9736, 0.9410 net of the forcing pass; across runs `lib-stage1`'s own instructions a call read 1.0033 and 1.0038 of Run 41's on the two halves, and its time 1.0106 and 1.0169, so the pair moved 1.1 and 1.5 points off Run 41's reading where its instructions moved a third of one --- inside the item's band on both halves, whose top was set at 1.013, and further than the sentence's *where Run 41 read it* suggests.

(4) *`libunord-stage15-sum`'s placement of the zero-stride axis pays on `compose-bcast-wide`, costs on `compose-bcast-nest`, and is level where the move passes no axis.* **HELD on both halves, on all four spans.** Stage fifteen over fourteen, on raw `slope` since a reducing consumer carries no corrected time, reads **2.0242** on the basis and **2.0127** on the control on `compose-bcast-nest`, inside 50% of 1.7 and over the 1.2 that would say the time follows neither the instructions nor the bytes; **0.3706** and **0.3772** on `compose-bcast-wide`, inside 25% of 0.45 and under the 0.70 that would say the same; **1.0000** on both halves on `compose-rev-bcast`; and **1.0008** and **0.9999** over the main set. The instructions came out as the prior said, 1.5794 on `compose-bcast-nest`, 0.4570 on `compose-bcast-wide` and 27 fewer of about 257600 on `compose-rev-bcast` in this run's own `compose` sweep on the basis, the control's within a thousandth of each, so the two moving cells' times run past their instruction ratios in the direction the bytes point, nest 2.02 against 1.58 and wide 0.37 against 0.46.

(5) *The regime's worth on `list` holds at its level, and on `bq-expand` stays inside the spread its builds have drawn.* **HELD on both spans.** `list` reads **1.2905**, 0.45 of a point off 1.295, a draw inside the 0.94 points the draws after Run 36's keep. `bq-expand` reads **1.3097**, 2.03 points off 1.33 and back inside the 1.2980 to 1.3101 the five draws before Run 41's kept, so the build term Run 41 drew is not in this build.
