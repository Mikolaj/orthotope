# Run 35 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span, stage thirteen)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 35 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span, stage thirteen): the two compilers come back where Run 34 left them, an arm geomean of 1.0044 against its 1.0048 --- and what moved is `list` itself, by 0.77 of a point, which pushes the MAIN SET past the 0.7% bar and so COSTS it the subtraction of its two columns, for the first time since Run 31.** The pair is Run 34's recipe to the commit --- `LOOP_EXITSPAN=1` on both halves, the shim at `f31bd1c`, one shim environment, one regime, one roster and one bench order, every process launched from the `hugebin/` mount, the 9.12.4 half `run35-exit` publishing and the in-tree stage1 `10.1.20260803` half `run35-gheadexit` the candidate --- rebuilt at `Main.hs` `0eda736`, three commits past Run 34's build, two of which touch comments alone. So `the basis` below is the 9.12.4 half and every `cross` figure reads basis over control, ABOVE 1 meaning the control is the faster. Over the sixteen main-set arms that carry a cross-half figure, TEN sit within 1% of 1 and the six outside reach 2.70 points, where Run 34's same reading put twelve inside and four outside: `lib-stage1` at **1.0270**, `lib-stage2-lean` at **1.0246**, the shipped leaf at **1.0199** with its two A/A copies at 1.0230 and 1.0175, all five faster under HEAD, and `lib-stage2-lean-u1` at **0.9864**, the only one of the six outside 1% that is faster on the basis. **The bar an arm has to clear to be the compiler's rather than the run's is 0.35 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, `list-aa-distant` at 0.9958 against `list` at 0.9923, which `--compare` prints under every table and which is NOT this population's floor, that being 0.64% and measured WITHIN one half --- and SIX of the eight strategies clear it. No arm moves past 3%, and the geomean over the arms is **1.0044**, against Run 34's 1.0048 and Run 32's 0.9985.

**Stage thirteen reads under stage twelve where a call is short and level where it is long, on both compilers, and registration (1) HOLDS on every one of its twenty-two readings.** It is stage twelve's route found with fewer passes over the axes, landed at `0eda736` with its untimed fill beside it. Basis then control: the main set reads **0.9679** and **0.9722** against 0.97 within 2%, `small` **0.8410** and **0.8518** against 0.86 within 3%, `rev` 0.9823 and 0.9852 against 0.98 within 2%, `scaled` 0.9956 and 0.9967 against 0.985 within 1.5%, `block` 1.0000 and 0.9999 against 0.99 within 1.5%, and the six populations the item puts at level --- `bcast`, `bcastmid`, `compose`, `flip`, `runs` and `window` --- come in between 0.9942 and 1.0004 against 1.0 within 1%. Its deepest cells across the halves are on `runs-3`, where it is one of nine consumers reading 0.7563 to 0.7581 --- a compiler reading and not a stage one, which the `runs` block takes.

**(2) is KILLED on `scaled` alone, by sixty-two instructions.** The item said stage thirteen retires more than two hundred instructions a call fewer than stage twelve on every view of every population. Over ten of the eleven it does, the thinnest view of each running from **-283** on the main set to **-885** on `bcastmid`, on both halves alike; on `scaled` the thinnest view is `scaled-rank1-m1` at **-138** on the basis and **-136** on the control, inside the two hundred. So the saving is real everywhere and small in one place, which is the item's own kill condition and not a reversal: no view of any population retires MORE than stage twelve. **And (3) is killed too, though how it is killed is worth more than the kill: its spans ask a question its prose does not.** The item says the shared code --- the merge step `mergeInto` and the route tail `routeOf`, lifted to top level where `canonViewOfPairs`, `routeList4` and `dispatchLean` now call them --- left the two ported library arms' instruction counts where Run 34 read them. Read as the prose states it, that HOLDS to six hundred-thousandths: this run's counts against Run 34's, same half, give `liblist-stage4-sum` and `lib-stage2-lean` geomeans of **0.99999** and **0.99998** on the basis and 0.99997 and 1.00006 on the control, no shape further than 0.07 of a point, and the cross-run counts geomean over all 34 arms the sweep carries is **1.0000**. What is killed is the spans as WRITTEN: a `counts` span under `--compare` reads this half over the OTHER, so it asks whether the two COMPILERS emit the same count, which the item never claimed --- and it reads 1.0062 and 1.0073 on the main set, 1.0074 and 1.0086 on `rev`, 1.0156 and 1.0186 on `window`, and 0.9986 on `small`'s `lib-stage2-lean`, each past the 0.1% the item allowed. **The two earlier runs of this pair read 1.0062 and 1.0063 there, Run 33's and Run 34's**, so no run of this pair could have held that span, and the band was set against a quantity nobody measured. Its `pair ARM list` spans miss twice besides, both under four tenths of a point: `lib-stage2-lean` against `list` on `rev`'s control half at 0.0226 against 0.0234 within 0.07, and on `small`'s basis half at 0.0581 against 0.0545 within 0.16.

**One registration held and two were killed, over 132 span readings in scope of the 704 read.** (1) HOLDS on both halves of all eleven populations; (2) holds on ten and dies on `scaled`; (3) dies on four of its spans, two `counts` and two `pair`, and its own sentence holds. **Against Run 34, each half on its own moved past 3% in eight arm-population cells, and seven of the eight carry their counts level at 1.0000, the eighth within four ten-thousandths of it**: `lib-stage1` on `compose`'s control at 1.0773, `mut-odo-vecdims-add-in-leaf-u1` on `compose`'s basis at 1.0494 and on `scaled`'s at 0.9510, `lib-stage2-lean-u1` on `scaled`'s basis at 1.0588 and on `rev`'s at 0.9381, `lib-stage2-lean` on `small`'s basis at 1.0515 and on `rev`'s control at 0.9672, and the shipped leaf on `flip`'s basis at 1.0308. None is the code, and none is registered; the copy test that would tell a file instance from a binary was not taken this run. **The largest single cell across the halves is `flip-whole-square/lib-stage2-lean-u1` at 1.6225 in time on 0.9412 in counts**, a time-over-counts of 1.72 and the run's widest, the count side being the latch of GHC [#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799) on a rank-1 view, which `--cell-movers` names under its table and which also carries `scaled-rank1-m1` and `compose-scalar`.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition. **What this run leaves the next one is a compiler pair that has stopped moving and a baseline that has not**: the arm geomean sits within four ten-thousandths of Run 34's on a source three commits along, every cross-run count reads 1.0000 to four decimals, and the one thing that shifted enough to matter is `list`, whose 0.77 of a point on the main set costs that population its subtraction and leaves SEVEN of the eleven differenceable where Run 34 had nine.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span**, as Runs 32 to 34's were, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **What is new in it is the SOURCE alone**: `Main.hs` at `0eda736`, three commits past Run 34's build, of which two touch comments only; the switch, the shim, the four shim variables, the launch from `hugebin/` and both compilers are Run 34's to the commit and to the day. **Read against Run 34, which this run's note rules is its reference, the distance is small and the reference does not move**: over the 16 arms that carry a corrected time and stand in both rosters, this run over Run 34's basis half runs from **0.9849** on `lib-stage2-lean-u1` to **1.0113** on `mut-odo-vecdims-add-in-leaf-u2-aa` --- below 1 meaning this run is the faster, and no row further than 1.51 points from level --- with `list` itself at **0.9996**; read as a ratio to `list` within each run, which cancels a box term exactly, the other fifteen give a `--bridge` geomean of **1.0005**, none outside the 3.3% drift band Run 11 measured. That span carries three `Main.hs` commits and the box, and nothing else. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run35-exit`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-five rows. That the published half is the ghc-9.12.4 one is the re-declaration of 2026-09-15 inherited rather than this run's to make --- 9.12.4 is what a default build takes on this machine and what a cross-run absolute is read against, and HEAD is the candidate reading. **Thirty-four of the thirty-five rows are not first readings**: every one of them has a twin in Run 34's file, and all but `libunord-stage11-sum` and `libunord-stage12-sum` in Run 32's. The thirty-fifth, `libunord-stage13-sum`, landed at `0eda736` --- stage twelve's route found with fewer passes over the axes --- and is read here for the first time.

**Comparing runs?** The table below is Run 35's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.64%** from 1 on the basis half or **0.40%** on the control, read over the eight pairs this roster carries, and over the four pairs that carry back to Run 10 at **0.49%** and **0.36%** --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **Both halves name the SAME pair this run**, `mut-odo-vecdims-add-in-leaf-u2-aa-distant`, where the carry-back figure names `bq-expand-aa-distant` on each, so the whole-set figure and the carry-back one part on both halves --- by fifteen hundredths of a point on the basis and four on the control. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **5.55%** on `gather48-src-50` on the basis and **3.97%** on `stretch-square-1341` on the control --- are not floors at all and are not to be quoted as any. **And its two columns may be differenced on SEVEN of the eleven populations**, `list` having moved **0.77 points** on this run's main set, which is past the bar, so a cross-half figure here is an ORDERING on the main set and on three classes and a measurement on the other seven.

**It is the main set's table**, and every column below is a statistic of that population: each stride class has a table of its own, on the same rows and in the same columns but its own basis, in [The stride classes, run by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.61* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.58 | 69 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage2-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over the port's base-offset table |
| liblist-stage3-sum | -- | -- | 0.61 | 70 | 1.00x | the same, over the lazy odometer under the natural-strides dispatch |
| liblist-stage4-list-sum | -- | -- | 0.57 | 70 | 1.00x | the same, base's `sum` over stage four's list -- the fold a library user brings, over the lazy odometer under the lean dispatch |
| liblist-stage4-sum | -- | -- | 0.60 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| libunord-stage1-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage10-list-sum | -- | -- | 0.02 | 83 | 0.00x | the same, base's `sum` over stage ten's list -- the fold a library user brings, over the two reorderings composed |
| libunord-stage10-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's tie-break with stage nine's zero-stride axes moved outermost -- the two reorderings composed |
| libunord-stage11-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage eleven's list --- stage ten with its zero-stride move guarded, so the move fires only where a zero stride is there to move |
| libunord-stage12-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage twelve's list --- stage eleven with the run chosen among tied unit-stride axes by its length |
| libunord-stage13-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.43* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage2-lean | 0.025 | 0.113 | 0.59 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-lean-u1 | 0.026 | 0.110 | 0.57 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.112* | *0.58* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.113 | 0.46 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.113* | *0.46* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.110 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- the shipped fill's leaf with the bound merged in and the body not unrolled |
| lib-stage1 | 0.029 | 0.113 | 0.45 | 69 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.39* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.51* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.112 | 0.39 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.127 | 0.251 | 0.63 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.127* | *0.251* | *0.62* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.128* | *0.251* | *0.36* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.69 | 21 | 25.20x | -- |
| *list-aa-adjacent* | *1.002* | *1.009* | *0.47* | *21* | *25.20x* | *A/A control* |
| *list-aa-distant* | *1.002* | *1.013* | *0.72* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run THREE of the 105 pairs among the fifteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 34's basis parted on six. All three are `lib-stage2-lean-u1` against the shipped leaf and its two A/A copies: the column reads **0.9788**, 0.9656 and 0.9812, putting the lean twin ahead, where the paired figures read **1.0193**, 1.0178 and 1.0259, putting it behind. **The widest disagreement is on the rows the cap touched most**: `bq-expand` over `lib-stage2-lean` divides to 5.1517 on the column where the paired figure is 4.4224, the column 16.5% off it, and `lib-stage2-lean` is the widest-capped row of the table, four of its nineteen cells capped and its published 0.02468 sitting 14.2 points under its plain per-shape geomean of 0.02875. Those column ratios are `--pair`'s own `published-column ratio` and not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads fourteen of the sixteen rows moved against Run 34's table and two at the same three decimals, where `--compare` against Run 34's own JSON puts every one of the sixteen within 1.51 points of level and `list` at 0.9996.

**This run's two columns MAY be differenced on SEVEN of the eleven populations, two fewer than Run 34 could say, and the MAIN SET is one of the two it newly loses.** It rests on `list` having moved **0.77 points** on this run's main set, past the 0.7% bar, and on `read-all.sh --brief-facts` putting `bcast` (1.0025), `bcastmid` (0.9963), `block` (1.0062), `compose` (0.9965), `flip` (0.9983), `runs` (1.0025) and `window` (1.0059) inside it. FOUR are past: the main set at **0.9923**, `rev` at 0.9826, `scaled` at 1.0080 and `small` at 1.0162. On those four every arm-by-arm figure across the halves in this file is an ORDERING and not a subtraction, and each says so in its own cross-half line --- which is why this run's head reads its main-set arm geomean as an ordering of the two compilers and not as a measurement of the gap between them.

`concat-runs` has no row, and neither do the other 87 arms the roster holds and checks without timing --- **88 of its 123** in all, where Run 34 checked 87 of 121: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **Two arms were added to the roster this run, ONE of them timed, and NONE was parked**, as on Runs 32 to 34. `libunord-stage13-sum`, stage twelve's route found with fewer passes over the axes, landed at `0eda736` with the untimed `libunord-stage13` beside it; the six parked on 2026-09-13 stay parked, and the thirteen Fill arms over a list that went to `check` on 2026-09-09 stay where they are. So a movement against Run 34's basis column is a movement on the **16 shared arms that carry a corrected time**, with a source term between the two runs and no switch, shim, launch or compiler term at all.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage2-lean` at 0.025**, with `lib-stage2-lean-u1` at 0.026, the shipped leaf and its two A/A copies at 0.027, `mut-odo-vecdims-add-in-leaf-u1` 0.027 and `lib-stage1` 0.029 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, the same five Runs 31 to 34 had. **The column and the pair DISAGREE about the order behind the leader**, as they did on Run 34: paired on the basis, `lib-stage2-lean` over `lib-stage1` is **0.9387** at 17 of 19 and p 0.00073, over its own unrolling twin **0.9676** at 12 of 19 and p 0.36, and over the shipped leaf **0.9863** at 11 of 19 and p 0.65, while the twin over the leaf reads **1.0193** at 5 of 19 --- the pairs putting the leaf second and the twin behind it, where the column prints the twin a thousandth behind the leader and ahead of the leaf. The disagreement is the winsorizing and not an arm: `lib-stage2-lean-u1`'s published 0.02606 sits 12.3 points under its plain per-shape geomean of 0.02971, four of its nineteen cells capped. **The third is that the leaf fusion is unmoved by the compiler and by the source**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6492** on the basis and **0.6382** on the control, both within half a point of Run 34's 0.6443 and 0.6360, and inside the 0.6358 to 0.6525 that Run 34's file records ten readings across Runs 29 to 33 spanning --- a span carried from that file and not re-derived here.

**The two standing placement controls are still gone with the prune, the straddlers stand at EIGHT on each half, and this pair moves tracked fill copies as Runs 33's and 34's did.** Within the pair `./loop-offsets.py run35-gheadexit run35-exit` puts the tracked six-copy group at **[0, 0, 0, 8, 4, 0]** on the basis and **[18, 0, 0, 0, 9, 2]** on the control, while the two-copy group reads **[0, 0]** on both; the basis carries 33 self-loops of 28 B in 26 distinct byte-sequences and the control 34 in 27 --- Run 34's four offset lists and two counts to the byte. So a compiler displaces fill copies as an optimisation level does, which is what `--library` says over the whole library too: 136 self-loops in common at **11.0%** the same offset in line. Against the previous build of the basis's own recipe, Run 34's basis binary, `--delta` reads EVERY mod-64 offset preserved on both groups with no address surviving to the byte and one displacement of 0x1b40 on each, so the source that moved under this run moved every copy and no head's offset. **And the exit spans astride are ZERO on both halves**, where this run's own preparation read one on the basis: that one was the phantom the owner refused at `e4f0624`, and this is the first reading of this pair with the fix in.


## What the next run compares against

**Run 36's pair was ruled on 2026-09-18, by the owner, and it is this run's HEAD half against itself with the two `-O2` passes added: both halves are `run35-gheadexit`'s recipe to the commit --- GHC HEAD through `cabal.project.ghead`, `Main.hs` at `0eda736`, which the tree still carries unchanged, the shim at `f31bd1c` under the four switches with the exit span, every process launched from `hugebin/` --- and the second half's command line carries `-fspec-constr` and `-fliberate-case` besides, nothing else differing. What this run leaves the next one as its reference is `run35-exit`, the basis half whose column stands below, and against the ruled pair that reference is a cross-compiler one: Run 36's basis is this run's CONTROL, so the fingerprint under Provenance, being the 9.12.4 half's, carries a compiler term against a HEAD basis --- 0.77 of a point on `list` here --- and which fingerprint the next machine check reads is the preparation's to say.** **AND THE COMPILER MOVED UNDER THAT RECIPE BEFORE RUN 36 WAS PREPARED, which is recorded here because the recipe above no longer names what a rebuild gets**: the in-tree stage1 under `~/r/horde-ad/ghc` is 10.1.20260918 from 2026-09-18, where this run's HEAD half read 10.1.20260803, which survives beside it under `~/r/horde-ad/ghc.old`; the owner ruled the same day that both of Run 36's halves take the CURRENT checkout, so that pair shares no compiler with this run and `run35-gheadexit` is its recipe but not its build. The whole dependency stack rebuilt with it, and `cabal.project.ghead` needed one stanza to build at all. What it costs -- the repetition reading that was there to be had, the like-for-like cross-run comparison this section was written expecting, and a machine check whose compiler term is now two steps of which one is measured -- is in Run 36's own pair note. The pair is the one declared 2026-09-15 morning and deferred by Runs 33, 34 and 35, moved from ghc-9.12.4 to HEAD by the ruling: the two `-O2` passes against neither, one variable and nothing else. The basis half is the dead-spot form at plain `-O1`, `nospec` naming what that half is, and the other is that same recipe with `-fspec-constr` and `-fliberate-case` added by hand, `twopass`, so that `--compare` reads nospec over twopass and every `cross` is what the two passes together do to one arm. One source, one shim, one shim environment, one roster, one shape set, one class list and one bench order, with the two command lines differing in two flags on one of them. The shim-environment question the deferred declaration left open is settled by the ruling, both halves carrying `LOOP_EXITSPAN=1` as this run's HEAD half did. What the pair answers, and what a `cross` reading of it costs, is the registration's to state before it runs, [registered 2026-09-18][open] as `What Run 36 is built to answer`. The recipes, spelled out as a pair note wants them, the half names being the preparation's to hold to the tag grammar:

    run36-gheadnospec   cd here, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --project-file=cabal.project.ghead --builddir=db-r36a \
                          --ghc-options="-fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --project-file=cabal.project.ghead --builddir=db-r36a) run36-gheadnospec
                        rm -rf db-r36a
    run36-gheadtwopass  the same source, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --project-file=cabal.project.ghead --builddir=db-r36b \
                          --ghc-options="-fspec-constr -fliberate-case -fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --project-file=cabal.project.ghead --builddir=db-r36b) run36-gheadtwopass
                        rm -rf db-r36b

`LOOP_MAXSKIP` and `LOOP_LOOKTHROUGH` are inert under the dead-spot form and stay on both lines so that the lines differ in the regime flags alone; `LOOP_ENTRIES`, `LOOP_BLOCKRULES`, `LOOP_PIN` and `LOOP_TRACE` are unset on both. Every build wants `-fforce-recomp` and a fresh `--builddir`, the switches being an environment change cabal does not see, and every driver takes its half from `hugebin/` through `half-bin.sh`, as this run's did. Under the exit span `loop-offsets.py --survey` reads 0 exit spans astride off a timed binary, as it did on both of this run's halves, so the preparation's legs 10a and 10b stop on anything else. **It is the pair Run 31's arithmetic wanted and no run since could supply.** Run 31 read `-O2` worth **1.2974** on `list` where `-fspec-constr` and `-fliberate-case`, measured one at a time on Runs 29 and 30, multiply to 1.3325 --- a 2.7-point overshoot that is either the level's other passes handing `list` back or an artefact of composing two runs' readings, and a pair with both passes on one half and neither on the other is the only thing here that tells them apart. Ruled onto HEAD, the pair reads that arithmetic across compilers, Runs 29 to 31 having been ghc-9.12.4 builds, so a HEAD reading near 1.30 confirms the composition only where HEAD's two passes are worth what 9.12.4's were, which no run has measured --- a limit for the registration to state, not a reason against the ruling. **And what this run changes about the case for it is that the compiler question at plain -O1 has stopped moving IN THE AGGREGATE and has not stopped moving arm by arm.** Run 33 read HEAD against 9.12.4 at an arm geomean of 1.0068 with the lean fill parting by 3.54 points, which the owner then ruled skewed by filesystem issues; Run 34, asked again from `hugebin/`, read **1.0048** with the lean fill level at 1.0047 and four of sixteen arms outside 1%; this run, on a source three commits along and nothing else moved, reads **1.0044** --- four ten-thousandths away --- with SIX arms outside 1%, the lean fill now at **1.0246** and its unrolling twin at **0.9864**, the only arm OUTSIDE 1% on either run to sit below it --- seven of this run's sixteen sit below 1 against five of Run 34's, all of those inside the percent. So the aggregate repeats and its composition does not, which is the reason a cross-half arm figure at this level is read against its A/A bar and not against its distance from 1, and the `-O2` pair is what is left waiting.

**The COMPILER variable has now been asked TEN times, and this run is the fourth to ask it at the level the library ships and the third under the exit span.** Runs 19 and 24 to 28 all varied it with `-fspec-constr` on BOTH halves: Run 24 read the two 5.7% and 6.8% apart on the instructions of two pure arms; Run 25 read `list` 1.10% apart in time and 0.33% in counts; Run 26 found twenty-four of twenty-six arms inside a percent in counts and the two `Ptr` arms outside at 0.6219 and 0.9295, which was GHC [#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778); Run 27 worked it around and read every arm inside a percent; Run 28 confirmed it at a counted geomean of 1.0027. **Run 32 asked it at plain -O1 and got the cleanest null of them all, Run 33 asked it under the exit span and read a gap, Run 34 asked Run 33's question from `hugebin/` and read close to Run 32's null again, and this run repeats Run 34 on a moved source.** Run 32's arm geomean was 0.9985 with no arm past 3% and three of eight strategies clearing its A/A bar; Run 33's was 1.0068, one arm past 3% and eight of eight past a 0.16-point bar; Run 34's was 1.0048, no arm past 3% and six of eight past a 0.23-point bar, the widest `lib-stage1` at 1.0258; this run's is **1.0044**, no arm past 3% and six of eight past a bar of **0.35** points, the widest `lib-stage1` again at **1.0270**. All four share both compilers to the day; Runs 34 and 35 share the recipe and differ in three `Main.hs` commits, two of them comments, so this pair of runs is the one place in the series where the source is the ONLY term --- and it moves the widest arm by 0.12 of a point and the lean fill by two. **The REGIME variable, meanwhile, has been asked three times and the arithmetic it left is still open.** Put in one orientation --- the unflagged half over the flagged --- Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**; on `bq-expand` the two passes MULTIPLY to 1.2967 against a measured 1.2943, 0.19% apart, while on `list` they multiply to 1.3325 against 1.2974, 2.7% apart. That arithmetic is an observation and not a subtraction, and the `-O2` pair above is what settles it.

**What Run 35 leaves the next run to read against, and the first item is a check that did NOT fire. The box is where Runs 28 to 34 left it**, and this run's gate says so: read against the fingerprint Run 34 installed, which this run's note rules is its own comparison, the machine check puts `list`'s net at **+0.11%**, worst `stretch-tall-Mx2` at +1.75%, 0 of 19 shapes past 5% and the geomean inside the 3% bar. **And this reading IS like-for-like**, which no machine check since Run 32 has been: Run 34's published half is this basis on the same shim, the same switch, the same launch and the same compiler, three `Main.hs` commits back and two of those comments, so the check reads the box and a source term and nothing else. Against `run34-exit` itself the sixteen shared timed arms span **0.9849 to 1.0113** with `list` at **0.9996**, and the fifteen that are not `list` give a `--bridge` geomean of **1.0005**, none outside the 3.3% drift band Run 11 measured and none outside Run 23's narrower 2.1% either. So this run publishes INSIDE the third machine era rather than opening a fourth, and the fingerprint below is this run's own, which the next run's machine check reads. **What a Run 36 reading may take from those sixteen arms that no run since Run 32 could is a reading with ONE term beside the box**: one thing separates the two builds and it is the source, so their spread is the box's and three commits' and nothing further.

**Registered with the pair.** Run 35's three registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. ONE held and TWO were killed. **What a next registration should take from this one is that a `predict:` span asks the question its VOCABULARY asks and not the one its prose does**: item (3)'s prose claims this run's counts read Run 34's, which holds at a cross-run geomean of 1.0000 over all 34 arms the sweep carries, while its `counts` spans under `--compare` read this half over the OTHER --- a compiler comparison the item never made, on which the two earlier runs of this pair read 1.0062 and 1.0063 where the item allowed 0.1%, so the span was unholdable the day it was written. A registration quoting a figure derived one way and spanning it another wants the reader mode named beside the figure, which the pair note's own rule already asks for.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are edited by hand, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 35**, whose halves were launched from `hugebin/` and whose basis carries `LOOP_EXITSPAN=1`; a run keeping that recipe reads against this basis within the switch, as this run read Run 34 within it. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it, and walking that chain here is what this section stopped doing. So an older run is read by opening its file, and the one step this run records is Run 34 to Run 35 --- **and its two published bases differ in the SOURCE alone**, both halves carrying the switch, the shim, the launch and the compiler, so it is a subtraction and not a bridge and carries a source term alone. Over the **16 arms both rosters time and both give a corrected time**, this run over Run 34's basis runs from **0.9849** on `lib-stage2-lean-u1` to **1.0113** on `mut-odo-vecdims-add-in-leaf-u2-aa` --- below 1 meaning this run is the faster --- FOURTEEN of the sixteen inside 1% of 1, with `list` itself at **0.9996**. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one, and the two differing in ONE COMPILER and in nothing else. Its two columns may NOT be differenced, `list` having moved 0.77 points between them, so the table is two orderings read side by side.
| strategy | Run 35 (plain -O1, dead-spot, exit span, -A32m, 9.12.4) | Run 35 (plain -O1, dead-spot, exit span, -A32m, GHC HEAD) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.044 |
| `mut-odo-vecdims-add-in-leaf-u1` | **0.027** | 0.027 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.027** | 0.026 |
| `lib-stage1` | **0.029** | 0.026 |
| `lib-stage2-lean` | **0.025** | 0.023 |
| `lib-stage2-lean-u1` | **0.026** | 0.025 |
| `bq-expand` | **0.127** | 0.127 |

**READ THE SECOND COLUMN AS A RATIO AND NOT AS A SPEED, and this run it is not even an ordering of speeds.** Every entry is that arm's net over `list`'s net in ITS OWN half, and `list` moved **0.77 points** between the halves --- past the 0.7% bar, so a control entry reading lower is the arm AND the denominator together and this table does not say which. **And it is not an identity either**: each entry is winsorized per row within its own half, so dividing an arm's two entries does not reproduce its `--compare` figure and is not meant to --- on `lib-stage2-lean` the two unrounded entries, 0.02468 and 0.02285, divide to about 1.080 where the cross reads 1.0246, which is the capping and not a disagreement, the basis capping four of that row's nineteen cells and the control five. The arm-by-arm reading of what the compiler is worth is in the head, off `--compare`, where the reference is not divided out.

**A published geomean is over the same 19 shapes, and two halves of one run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered. **THE TABLE ABOVE IS NOT SUCH A PAIR, which this section has not had to say of its own main set since Run 31**: `list` moved **0.77 points** between these halves, so the two columns are read side by side as orderings and never differenced. **They still print within three thousandths of each other on every row** --- `lib-stage2-lean` 0.025 against 0.023, `lib-stage1` 0.029 against 0.026, the shipped leaf 0.027 against 0.026, `lib-stage2-lean-u1` 0.026 against 0.025 and `mut-odo-vecdims` 0.045 against 0.044, with `mut-odo-vecdims-add-in-leaf-u1` at 0.027 and `bq-expand` at 0.127 on both --- and read down a column the head and the foot are the same on both, `lib-stage2-lean` leading each and `bq-expand` at the foot of each. **Those gaps are the winsorizing as much as the arms**: `lib-stage2-lean`'s plain per-shape geomeans are 0.02875 and 0.02784, 3.2 points apart where the published figures part by eight, the cap touching four of its cells on the basis and five on the control.

**The control half's own standings on the arms this run's roster carries, which no table here holds, every published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `-u1` **0.9544** (0.9730) and against `mut-odo-vecdims` **0.6382** (0.6492); `lib-stage1` against `-u2` **1.0434** (1.0508); `lib-stage2-lean` against `-u2` **0.9817** (0.9863) and against `lib-stage1` **0.9409** (0.9387). **All five hold their direction across the halves**, as they did on Run 34: the lean fill is ahead of the shipped leaf under both compilers, by 1.4 points on the basis and 1.8 on the control, and ahead of `lib-stage1` by six on each. **The one ordering that changes sides is the one Run 34 named too**: `mut-odo-vecdims-add-in-leaf-u1` against `lib-stage1` reads **0.9781** on the basis and **1.0042** on the control, and the control reading sits 0.42 of a point from level against that half's 0.40% floor, which is just outside it --- so the sides it changes are two readings two hundredths of a point apart in significance and not a compiler telling the two arms apart. What does NOT repeat from Run 34 is `bcastmid`'s leader outside the family, which parted between the halves there and is `lib-stage1` on both here.

**Each stride class has its own table below.** Run 8 re-ran every class with the populations pinned, and every run since has again, so each class's paragraph carries what the last change moved and the table above it is what the next run reads against. **A class figure compared across the Run 11/Run 12 boundary is not compared on one build**: Run 11's class tables are its *aligned* half's and Run 12's its *max-skip* basis half's, and the main set prices that difference at nothing below 0.99 and up to 1.06, so a point or two of movement across that boundary is the shim rather than the class. From Run 13 on, every run's class tables are its own basis half's, Run 34's included.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.35 us | 0.080 | `lib-stage2-lean-u1` 0.078 | `mut-odo-vecdims-add-in-leaf-u1` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.69 us | 0.088 | `lib-stage2-lean-u1` 0.071 | `mut-odo-vecdims-add-in-leaf-u2` 0.069 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 120 us | 0.063 | `lib-stage2-lean` 0.032 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 390 us | 0.043 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `gather48-src-50` | 3 | 22500 | 454 us | 0.049 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.11 ms | 0.030 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.7 ms | 0.052 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `stretch-primes` | 89 | 250357 | 4.38 ms | 0.025 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17 ms | 0.040 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.9 ms | 0.052 | `lib-stage1` 0.031 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.9 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `stretch-inner256` | 256 | 1750784 | 44.4 ms | 0.023 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `stretch-pow2stride` | 64 | 1769472 | 31.3 ms | 0.112 | `lib-stage2-lean-u1` 0.110 | `mut-odo-vecdims-add-in-leaf-u1` 0.110 |
| `stretch-r5-8x432` | 8 | 1769472 | 48.2 ms | 0.021 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.8 ms | 0.087 | `lib-stage2-lean` 0.078 | `mut-odo-vecdims-add-in-leaf-u2` 0.078 |
| `stretch-bigstride` | 3 | 1800000 | 51 ms | 0.033 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.8 ms | 0.058 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 41 ms | 0.021 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.4 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 942 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.2 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.4 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.3 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.7 ms | 0.015 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.3 ms | 0.057 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.67 ms | 0.052 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.26 ms | 0.019 | `lib-stage1` 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.017 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.5 ms | 0.034 | `lib-stage1` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.1 ms | 0.022 | `lib-stage1` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.23 ms | 0.019 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.26 ms | 0.025 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.3 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.35 ms | 0.028 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.47 ms | 0.020 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 945 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 944 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.5 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.9 ms | 0.022 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.31 ms | 0.026 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.052 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.4 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30.1 ms | 0.024 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.4 ms | 0.048 | `lib-stage2-lean` 0.040 | `mut-odo-vecdims-add-in-leaf-u2` 0.045 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 119 us | 0.065 | `lib-stage2-lean` 0.032 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 457 us | 0.048 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.37 ms | 0.025 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.3 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.5 ms | 0.025 | `lib-stage1` 0.024 | `mut-odo-vecdims` 0.025 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.5 ms | 0.024 | `lib-stage2-lean` 0.026 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 28.7 ms | 0.024 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.024 |
| `runs-256` | `runs` | 256 | 1799936 | 28.8 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 33.3 ms | 0.032 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 39.9 ms | 0.057 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 35.6 ms | 0.047 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 29.9 ms | 0.025 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34 ms | 0.041 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.4 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.2 ms | 0.038 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.3 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 31.9 ms | 0.030 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 29.5 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.5 ms | 0.026 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 270 us | 0.029 | `lib-stage2-lean-u1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.05 ms | 0.023 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.13 ms | 0.028 | `lib-stage2-lean` 0.031 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.077 | `lib-stage1` 0.100 | `mut-odo-vecdims-add-in-leaf-u2` 0.058 |
| `small-bcast32` | `small` | 32 | 256 | 4.51 us | 0.051 | `lib-stage1` 0.062 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `small-flat64` | `small` | 64 | 256 | 4.44 us | 0.060 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-patch-r5` | `small` | 4 | 256 | 5.31 us | 0.088 | `lib-stage2-lean` 0.098 | `mut-odo-vecdims-add-in-leaf-u1` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.57 us | 0.041 | `lib-stage2-lean` 0.056 | `mut-odo-vecdims-add-in-leaf-u2` 0.040 |
| `window-28x28-k5` | `window` | 5 | 14400 | 278 us | 0.040 | `lib-stage1` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 962 us | 0.084 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.43 ms | 0.052 | `lib-stage2-lean` 0.031 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 10.1 ms | 0.048 | `lib-stage1` 0.028 | `mut-odo-vecdims-add-in-leaf-u1` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.85 ms | 0.051 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.029 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.6 ms | 0.052 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage1` 0.032 | `mut-odo-vecdims-add-in-leaf-u1` 0.031 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage1` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-five rows is a geomean over fewer shapes than the rest, as on Runs 32, 33 and 34 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the FIFTEEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, `libunord-stage13-sum` being the fifteenth and landing this run --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names `lib-stage2-lean` on SIX, `lib-stage1` on three --- `rev`, `bcastmid` and `scaled` --- and `lib-stage2-lean-u1` on one, `small`, where Run 34 named the lean fill on seven and the unrolling twin on `bcastmid`. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 35's verdicts** over ten classes, the details beside each class's table:

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **The first held in every one of the eleven populations on both halves; the second held in all ten classes on both halves and BROKE on the main set's CONTROL half, as it broke on one half of Run 34.** On the MAIN SET `mut-odo-vecdims` is ahead of `bq-expand` on `stretch-pow2stride` at **0.9950** on the basis and BEHIND at **1.0030** on the control, each margin inside its half's floor, and `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints every earlier run's reading beside its own; whether a run reads the fill behind by more than its half's floor there is [the open list][open]'s question, and neither this run nor Run 34 does --- 0.30 of a point against a 0.40% floor here and 0.16 against 0.49% there. Run 34's two readings were 0.9989 and 1.0016, so this run parts the same way and by three times as much. The `worst` clause holds in every regime, roster, compiler and layout the README has run, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population. The `bq-expand` clause folded in on 2026-09-06 from the ordering that was property 2 until then, strengthened from a geomean to every shape, and is read that way here for the eighth time.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` carries a `worst` of **1.085** on `runs` on the basis and **1.069** on the control, and one cell does it on each, `runs-2`, at those same two figures, the halves parting by 1.6 points where Run 34's parted by 1.4. Over every timed arm outside the controls and the reducing consumers, on all eleven populations and both halves --- twenty-two tables scanned for it --- no other cell reads above 1. It has narrowed since Run 34, whose two readings were 1.105 and 1.091.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the fifth run running that this property is the one left entirely alone.** The `list` clause is closest at `small-patch-k5`, **0.05918**, and every closest shape outside `small` sits under 0.048. The `bq-expand` clause is closest at `scaled-rank1-m1`, **1.00003**, then `stretch-tall-Mx2` on the main set at 1.00000 --- the same two shapes at the same two figures as Run 34, and inside the margin the strict form would have failed on, which is why the margin is there and why it is not widened further.

3. **The allocation tiers survive, their ORDER is unbroken in all ten classes and on the main set, and their LEVELS are identical on the two halves in every one of the eleven populations, cell for cell; what `small` is outside is the LEVEL clause and not the order one**, by the ruling of 2026-09-07, it being the class built to break it and read here for what it shows: the mutable fills at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 20.99x to 27.66x. On the main set the fills read 1.00x, `bq-expand` **2.78x** and `list` **25.20x**, a plain -O1 half's levels as Runs 30 to 34's were --- **and the control half reads the same 2.78x and 25.20x, and the same triple in every one of the ten classes**, `small`'s 1.27x family included. No registration of this run names allocation; the reading is taken anyway because it is free and because it is what would show a compiler changing what an arm allocates rather than how fast it runs. It shows none: `--alloc` puts 470 of the 627 allocating cells inside 1e-4 between the halves, worst **2.26e-02** on `stretch-inner256/libunord-stage13-sum` --- this run's new arm, and a reducing consumer whose published multiple is 0.00x --- with the 38 cells under 100 bytes a call set aside as a property of fitting a near-zero allocation.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 35 (GHC HEAD against ghc-9.12.4, both at plain -O1, dead-spot, exit span, -A32m, launched from `hugebin/`, stage thirteen) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 0.17 of a point on `flip` at narrowest and 1.74 on `rev` at widest, so SEVEN of the ten classes sit INSIDE the 0.7% that lets two columns be differenced and their cross-half readings are readings of the pair's variable rather than orderings; the three past the bar are `rev` at 0.9826, `scaled` at 1.0080 and `small` at 1.0162 --- and this run the MAIN SET is past it too, at 0.9923, which no run since Run 31 has had to say --- Runs 32, 33 and 34 read `list` there at 1.0043, 0.9955 and 1.0006, all inside. Over the ten classes the reader counts **160 arm-comparisons, 72 putting the basis faster and 88 slower**, with no degenerate arm excluded, at geomeans from **0.9947** on `bcastmid` to **1.0132** on `window` and extremes of `lib-stage1` at **0.9348** on `compose` and `lib-stage2-lean-u1` at **1.1232** on `flip`, their counts at 1.0002 and 0.9901, so neither extreme is code. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **All three items read every class** --- (1) sets a span per population, (2) a `countdiff` on all eleven and (3) a `pair` and a `counts` span on each --- so each block below carries what applies to it, and the classes where an item DIES are `scaled` for (2) and `rev`, `window` and `small` for (3).

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table; *best outside family* is the leading arm outside the vecdims family, what the dropped stride-conditioned redirect would have taken, and *ceiling* the leading arm OF the family, each with its name --- and both are read over the POPULATION, so the arm named here may lead on no single shape and the per-shape fingerprint below may name another, which is [the README's per-shape section][pershape]'s own point and not a disagreement --- since which arm leads is half of what the column says --- so where an arm outside the family leads, the two name different arms and the gap between them is what the lead is worth, and Run 21's table, which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong to; *floor* is the largest deviation from 1 among that process's A/A controls. A cell that breaks property 1, or that leads `mut-odo-vecdims` --- what broke the ordering that was property 2 until 2026-09-06 ([the properties](#the-properties-the-next-run-should-test)) --- is bolded. **In practice that marks the FASTER of the two named arms, one cell a row**: the arm outside the family on FOUR of the ten --- `rev` and `bcastmid`, where `lib-stage1` leads, and `window` and `flip`, where `lib-stage2-lean` does --- and the family's own ceiling on the other SIX, `bcast`, `scaled`, `runs`, `block`, `small` and `compose`, where the ceiling is faster. **The two pointer leaves held five of Run 30's six bolded ceilings and are parked**, so every bolded ceiling here is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` itself, which is the form the family would ship. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.043 | 0.065 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.36% |
| `bcast` | 6 | 0.021 | 0.057 | `lib-stage2-lean` 0.016 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.016 | 0.62% |
| `bcastmid` | 4 | 0.029 | 0.052 | **`lib-stage1`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 | 2.60% |
| `window` | 8 | 0.050 | 0.084 | **`lib-stage2-lean`** 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.88% |
| `scaled` | 3 | 0.028 | 0.029 | `lib-stage1` 0.023 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.022 | 0.72% |
| `runs` | 17 | 0.026 | 0.057 | `lib-stage2-lean` 0.024 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.024 | 3.48% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage2-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 0.72% |
| `block` | 5 | 0.023 | 0.028 | `lib-stage2-lean` 0.021 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.021 | 1.18% |
| `small` | 5 | 0.061 | 0.088 | `lib-stage2-lean-u1` 0.057 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.052 | 1.94% |
| `compose` | 4 | 0.024 | 0.028 | `lib-stage2-lean` 0.015 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.015 | 0.29% |

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` in every one of the ten --- the lead that broke the ordering property 2 carried until 2026-09-06. **On SIX rows --- `bcast`, `scaled`, `runs`, `block`, `small` and `compose` --- the bold sits in the CEILING column instead**, and it names ONE arm on all six, the shipped leaf `mut-odo-vecdims-add-in-leaf-u2`; against Run 34 the one row that changed sides is `bcast`, which moved into that set, and `bcastmid` now names `lib-stage1` outside the family where Run 34's named the lean fill's unrolling twin. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **FIVE rows tie at three decimals** --- `bcast` at 0.016, `window` at 0.027, `runs` at 0.024, `block` at 0.021 and `compose` at 0.015 --- and the bold on each is `--block`'s own, computed on the unrounded values where the printed ones cannot separate: outside the family against the ceiling, 0.015672 against 0.015582, 0.026907 against 0.026943, 0.024483 against 0.024374, 0.021225 against 0.021108 and 0.014716 against 0.014530, so `window` falls to the arm outside the family and the other four to the ceiling.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.14 | 147 | 1.01x |
| liblist-stage2-sum | -- | -- | 0.11 | 147 | 1.01x |
| liblist-stage3-sum | -- | -- | 0.10 | 147 | 1.01x |
| liblist-stage4-list-sum | -- | -- | 0.09 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.11 | 147 | 1.01x |
| libunord-stage1-sum | -- | -- | 0.08 | 146 | 1.03x |
| libunord-stage10-list-sum | -- | -- | 0.05 | 157 | 0.01x |
| libunord-stage10-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage11-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage12-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage13-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.05 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.04 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage1 | 0.021 | 0.048 | 0.09 | 147 | 1.01x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.043* | *0.10* | *147* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.043* | *0.07* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.043 | 0.10 | 147 | 1.00x |
| lib-stage2-lean | 0.023 | 0.032 | 0.06 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.025 | 0.033 | 0.11 | 147 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.044 | 0.11 | 146 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.043* | *0.064* | *0.12* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.043** | 0.065 | 0.10 | 138 | 1.00x |
| *mut-odo-vecdims-aa* | *0.043* | *0.064* | *0.16* | *138* | *1.00x* |
| *bq-expand-aa-distant* | *0.138* | *0.235* | *0.09* | *122* | *3.22x* |
| bq-expand | 0.139 | 0.234 | 0.12 | 122 | 3.22x |
| *bq-expand-aa-adjacent* | *0.139* | *0.234* | *0.21* | *122* | *3.22x* |
| *list-aa-distant* | *0.999* | *1.001* | *0.22* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.19 | 85 | 26.11x |
| *list-aa-adjacent* | *1.002* | *1.005* | *0.20* | *85* | *26.11x* |

**Controls:** The largest A/A pair is `bq-expand-aa-adjacent` at 1.0036, worst cell 0.78% on `rev-gather48-src-50`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0016 on a worst cell of 0.51% on `rev-primes`, its interval covering 1. The in-situ term reads 0.9892, 1.0165 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0029, which the correction amplifies by 1.23x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h9m8s, peak 95 MiB in use, 24 MiB max residency; the reader reads 35 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.52 ms per call raw, 4.37 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.065/0.048/0.025

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0043, from `lib-stage2-lean-u1` at 0.9358 to `lib-stage1` at 1.0544, with `list` itself at 0.9826. **The baseline moved 1.74% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.065, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.6498 over 3 of 3 shapes at sign p 0.25, a margin of 35.02% against this class's 0.36% floor (`bq-expand-aa-adjacent`). **What is this class's own is the extra pass over the axes, visible here for the eighth run running.** `rev` negates every stride and carries no zero stride and no pair of axes tied on stride, so `zerosOutermost` hands its list back unchanged and only the walk over the axes separates the dispatches. It is also the class whose `list` moved furthest between the halves of the ten, 1.74 points. Its two columns may NOT be differenced, `list` having moved 1.74 of a point, at a class geomean of 1.0043 over the 16 arms, with 6 of 8 strategies past an A/A bar of 1.15 points. The counted work reads a counts geomean of 1.0066 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9823** and **0.9852** against 0.98 within 2%, holding on both halves, and (2) at -557 and -550 instructions on its thinnest view. **(3) dies here twice**: its `counts` span at 1.0074 and 1.0086 against 0.1%, which reads the compiler and not the source, and its `lib-stage2-lean` against `list` span on the CONTROL half at 0.0226 against a 0.0234 within 0.07. Against Run 34 the class carries two half-local movers, `lib-stage2-lean-u1` at 0.9381 on the basis and `lib-stage2-lean` at 0.9672 on the control, both with counts at 1.0000.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it; this run reads the class for stage twelve's tie with stage eleven, at registration (2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.51 | 62 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.52 | 62 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 74 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.49 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.52 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.31* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *69* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.52* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.42 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.41* | *62* | *1.00x* |
| lib-stage2-lean | 0.016 | 0.020 | 0.50 | 62 | 1.00x |
| lib-stage1 | 0.016 | 0.020 | 0.44 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.024 | 0.50 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.020 | 0.44 | 61 | 1.00x |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.32* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.08 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.35* | *61* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.144* | *0.69* | *46* | *1.00x* |
| bq-expand | 0.091 | 0.142 | 0.73 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.092* | *0.143* | *0.39* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.14 | 17 | 20.99x |
| *list-aa-distant* | *1.006* | *1.011* | *0.89* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.006* | *1.013* | *0.79* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0062, worst cell 1.26% on `bcast-src8`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.05% on `bcast-src8`, its interval missing 1. The in-situ term reads 1.0190, 1.0126 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0060, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m13s, peak 169 MiB in use, 42 MiB max residency; the reader reads 35 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.5 ms per call raw, 29.4 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.028/0.019/0.057/0.015/0.019/0.019

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0025, from `mut-odo-vecdims` at 0.9947 to `mut-odo-vecdims-add-in-leaf-u1` at 1.0218, with `list` itself at 1.0025.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage2-lean` leads outside the family at 0.016, priced against `mut-odo-vecdims` at 0.6700 over 6 of 6 shapes at sign p 0.031, a margin of 33.00% against this class's 0.62% floor (`list-aa-adjacent`). **What is this class's own is that both routes fill**, an innermost stride of 0 sending the lean dispatch and stage one down the same path, which is why `bq-expand` sits at the fills' own 1.00x tier here and nowhere else. Its two columns MAY be differenced, `list` having moved 0.25 of a point, at a class geomean of 1.0025 over the 16 arms, with 4 of 8 strategies past an A/A bar of 0.48 points. The counted work reads a counts geomean of 1.0024 over the same arms, 16 of them counted. Every span in scope holds: registration (1) reads stage thirteen over stage twelve at **0.9964** and **0.9994** against 1.0 within 1%, (2) at -574 and -578 on its thinnest view, and (3)'s four spans all hold, its `counts` clause at 1.0001 and 0.9999. No arm moved past 3% against Run 34 on either half.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.38 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.37 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.40 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.50 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.42 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.39 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.03 | 96 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.33 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.32 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.32 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 96 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.33* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *89* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *89* | *0.00x* |
| lib-stage1 | 0.012 | 0.017 | 0.33 | 82 | 1.00x |
| lib-stage2-lean | 0.012 | 0.018 | 0.39 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.012 | 0.018 | 0.35 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.019 | 0.030 | 0.46 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.38* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.31* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.031 | 0.46 | 78 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.052* | *0.28* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.052 | 0.31 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.48* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.099* | *0.180* | *0.42* | *61* | *1.92x* |
| bq-expand | 0.099 | 0.180 | 0.45 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.180* | *0.31* | *61* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 1.11 | 28 | 23.56x |
| *list-aa-adjacent* | *1.001* | *1.006* | *0.94* | *28* | *23.56x* |
| *list-aa-distant* | *1.003* | *1.015* | *0.89* | *28* | *23.56x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0260, worst cell 11.18% on `bcastmid-primes`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.05% on `bcastmid-b200k`, its interval missing 1. The in-situ term reads 1.0133, 1.0817 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0088, which the correction amplifies by 2.38x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m11s, peak 125 MiB in use, 35 MiB max residency; the reader reads 35 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.5 ms per call raw, 47.5 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.052/0.019/0.034/0.022

**Across the halves:** 13 of the 16 arms are faster on this half and 3 slower, at a geomean of 0.9947, from `lib-stage2-lean-u1` at 0.9694 to `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0058, with `list` itself at 0.9963.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage1` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4141 over 4 of 4 shapes at sign p 0.12, a margin of 58.59% against this class's 2.60% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). **What is this class's own this run is that BOTH its halves were measured twice.** A root cron job took about a core for a minute inside the first `bcastmid` process, which `--wild` read as three benches on `bcastmid-primes` at 0.28, 0.99 and 1.10 of a core, so BOTH halves were re-run on a quiet box and the first pair of JSONs is parked as `probe-intruded-*`; the figures here are the second pair's, and `--wild` reads no bench at 0.25 on either of them. What survives the rerun is the A/A worst cell: **11.18%** on `bcastmid-primes` in the basis process, four times this class's 2.60% floor and the widest A/A cell of the run. Its two columns MAY be differenced, `list` having moved 0.37 of a point, at a class geomean of 0.9947 over the 16 arms, with 1 of 8 strategies past an A/A bar of 2.96 points. The counted work reads a counts geomean of 1.0037 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9980** and **0.9990** against 1.0 within 1%, and (2) at **-884** and **-885** instructions on its thinnest view, the deepest saving of the eleven populations; (3)'s four spans all hold.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.35* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.19 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.18 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.18 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.18 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.18 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.05 | 102 | 0.03x |
| libunord-stage10-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage11-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage12-sum | -- | -- | 0.09 | 104 | 0.03x |
| libunord-stage13-sum | -- | -- | 0.08 | 104 | 0.03x |
| libunord-stage6-loop-sum | -- | -- | 1.39 | 89 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage7-sum | -- | -- | 0.04 | 102 | 0.03x |
| libunord-stage9-sum | -- | -- | 0.10 | 101 | 0.03x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.21* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage2-lean | 0.027 | 0.032 | 0.17 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.031* | *0.18* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.031 | 0.16 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.031* | *0.16* | *82* | *1.00x* |
| lib-stage2-lean-u1 | 0.028 | 0.033 | 0.23 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.031 | 0.16 | 82 | 1.00x |
| lib-stage1 | 0.028 | 0.032 | 0.16 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.050* | *0.084* | *0.14* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.050* | *0.086* | *0.18* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.050** | 0.084 | 0.18 | 76 | 1.00x |
| bq-expand | 0.172 | 0.219 | 0.33 | 57 | 3.86x |
| *bq-expand-aa-adjacent* | *0.172* | *0.220* | *0.32* | *57* | *3.86x* |
| *bq-expand-aa-distant* | *0.173* | *0.219* | *0.31* | *57* | *3.86x* |
| list (baseline) | 1.000 | 1.000 | 0.45 | 30 | 27.66x |
| *list-aa-adjacent* | *1.001* | *1.004* | *0.42* | *30* | *27.66x* |
| *list-aa-distant* | *1.002* | *1.110* | *0.48* | *30* | *27.66x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0088, worst cell 10.98% on `window-128x128-k7`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.04% on `window-224x224-k3-s2`, its interval missing 1. The in-situ term reads 1.0026, 1.1408 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0085, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h24m13s, peak 130 MiB in use, 52 MiB max residency; the reader reads 35 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.084/0.031/0.052/0.048/0.053/0.052

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0132, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9805 to `lib-stage1` at 1.0536, with `list` itself at 1.0059.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.084, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage2-lean` leads outside the family at 0.027, priced against `mut-odo-vecdims` at 0.4822 over 8 of 8 shapes at sign p 0.0078, a margin of 51.78% against this class's 0.88% floor (`list-aa-distant`). **What is this class's own is the run's widest count disagreement between the compilers, and one view on which the whole stage family parts between them.** On `window-224x224-k3` the new arm reads **0.7745** basis over control and stage twelve 0.7840 on the same view --- the two arms moving together and not apart, so this pair prices the COMPILER on that view and not the stage; they are this class's two deepest cells and the eleventh and twelfth of the run's 2800. and the class's counted work reads 1.0098 over the sixteen arms, the widest of the eleven. Its basis process also carries an A/A worst cell of **10.98%** on `window-128x128-k7`, twelve times this class's 0.88% floor. Its two columns MAY be differenced, `list` having moved 0.59 of a point, at a class geomean of 1.0132 over the 16 arms, with 5 of 8 strategies past an A/A bar of 1.06 points. The counted work reads a counts geomean of 1.0098 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9942** and **0.9979** against 1.0 within 1%, and (2) at -664 and -645 on its thinnest view; **(3)'s `counts` spans die here widest**, 1.0156 and 1.0186 against 0.1%, which is this class's compiler gap and not the shared code, whose cross-run counts read 1.0000.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.06* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.13 | 128 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.12 | 128 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.17 | 127 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.12 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.11 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.11 | 127 | 1.01x |
| libunord-stage10-list-sum | -- | -- | 0.18 | 127 | 1.00x |
| libunord-stage10-sum | -- | -- | 0.11 | 127 | 1.00x |
| libunord-stage11-sum | -- | -- | 0.11 | 127 | 1.00x |
| libunord-stage12-sum | -- | -- | 0.14 | 127 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.11 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.13 | 127 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.15 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.12 | 127 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *137* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.030* | *0.13* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.031 | 0.18 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.031* | *0.14* | *128* | *1.00x* |
| lib-stage1 | 0.023 | 0.031 | 0.13 | 127 | 1.00x |
| lib-stage2-lean | 0.023 | 0.031 | 0.15 | 127 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.024 | 0.030 | 0.23 | 127 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.036 | 0.19 | 127 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.028* | *0.10* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.029 | 0.07 | 127 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.028* | *0.11* | *127* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.091* | *0.100* | *0.07* | *111* | *1.21x* |
| bq-expand | 0.091 | 0.100 | 0.08 | 111 | 1.21x |
| *bq-expand-aa-distant* | *0.091* | *0.100* | *0.07* | *111* | *1.21x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 69 | 21.49x |
| *list-aa-distant* | *1.000* | *1.002* | *0.19* | *69* | *21.49x* |
| *list-aa-adjacent* | *1.001* | *1.004* | *0.18* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9928, worst cell 0.82% on `scaled-r5`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0006 on a worst cell of 0.53% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0142, 1.0071 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9970, which the correction amplifies by 2.42x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h9m9s, peak 110 MiB in use, 29 MiB max residency; the reader reads 35 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.31 ms per call raw, 5.13 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0080, from `bq-expand-aa-distant` at 0.9968 to `lib-stage2-lean-u1` at 1.0577, with `list` itself at 1.0080. **The baseline moved 0.80% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.9454 over 2 of 3 shapes at sign p 1, a margin of 5.46% against this class's 0.72% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). **What is this class's own is registration (2), which dies here and nowhere else.** On `scaled-rank1-m1` stage thirteen retires **138** instructions a call fewer than stage twelve on the basis and **136** on the control, where the item asked for more than two hundred on every view of every population; the other ten populations give it between -283 and -885. So the saving is smallest on the class of rank-1 and scaled views, which is where the sort it removes had least to do. Its two columns may NOT be differenced, `list` having moved 0.80 of a point, at a class geomean of 1.0080 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.71 points. The counted work reads a counts geomean of 1.0007 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9956** and **0.9967** against 0.985 within 1.5%, holding on both halves; (3)'s four spans hold. This class is one of the four whose columns may NOT be differenced, `list` having moved 0.80 of a point, and against Run 34 it carries two half-local movers on the basis, `lib-stage2-lean-u1` at 1.0588 and `mut-odo-vecdims-add-in-leaf-u1` at 0.9510, both with counts at 1.0000. Its A/A slot on `scaled-super-r3` is the hazard [the open list][open]'s own entry describes and is not read as a figure here.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.53* | *52* | *1.08x* |
| liblist-stage1-sum | -- | -- | 0.11 | 61 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.09 | 69 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.02 | 77 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 74 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.03 | 77 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 61 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.03 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.03 | 77 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 77 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.02 | 77 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 77 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 69 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 77 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 77 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.03 | 77 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.50* | *59* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.12* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.026 | 0.13 | 59 | 1.00x |
| lib-stage2-lean | 0.024 | 0.026 | 0.11 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.025 | 0.028 | 0.12 | 59 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.026 | 0.14 | 59 | 1.00x |
| *mut-odo-vecdims-aa* | *0.026* | *0.057* | *0.09* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.026** | 0.057 | 0.10 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.026* | *0.057* | *0.11* | *59* | *1.00x* |
| bq-expand | 0.094 | 0.142 | 0.45 | 46 | 1.08x |
| *bq-expand-aa-adjacent* | *0.094* | *0.142* | *0.59* | *46* | *1.08x* |
| *bq-expand-aa-distant* | *0.095* | *0.142* | *0.05* | *46* | *1.08x* |
| lib-stage1 | 0.098 | 1.085 | 0.18 | 51 | 1.42x |
| list (baseline) | 1.000 | 1.000 | 2.60 | 17 | 21.30x |
| *list-aa-distant* | *1.032* | *1.049* | *0.25* | *17* | *21.30x* |
| *list-aa-adjacent* | *1.035* | *1.049* | *0.26* | *17* | *21.30x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0348, worst cell 4.94% on `runs-r3-48x30`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0002 on a worst cell of 0.51% on `runs-5`, its interval covering 1. The in-situ term reads 1.0293, 1.0277 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0336, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h51m24s, peak 657 MiB in use, 289 MiB max residency; the reader reads 35 benchmarks over 17 shapes of the runs class. Anchor: `runs-2`, `list` at 41 ms per call raw, 39.9 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.047/0.041/0.038/0.032/0.030/0.025/0.025/0.025/0.025/0.025/0.024/0.024/0.025/0.024/0.024/0.026

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0027, from `lib-stage1` at 0.9967 to `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0080, with `list` itself at 1.0025.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.08x, 21.30x --- and `lib-stage2-lean` leads outside the family at 0.024, priced against `mut-odo-vecdims` at 0.8362 over 9 of 17 shapes at sign p 1, a margin of 16.38% against this class's 3.48% floor (`list-aa-adjacent`). **What is this class's own this run is one shape on which the whole roster parts between the halves.** On `runs-3` NINE consumers read between **0.7563** and **0.7581** across the halves with their counts at 1.0000 --- the basis a quarter faster on every one of them, on identical instruction counts --- which fills the top of `--cell-movers`. It is also the class with the widest floor of the ten, **3.48%** on the basis and 3.70% on the control, so margins here are read with more room than anywhere else. Its two columns MAY be differenced, `list` having moved 0.25 of a point, at a class geomean of 1.0027 over the 16 arms, with 5 of 8 strategies past an A/A bar of 0.26 points. The counted work reads a counts geomean of 1.0023 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9984** and **1.0004** against 1.0 within 1%, and (2) at -287 and -289 on its thinnest view; (3)'s four spans all hold, its `counts` clause exactly at 1.0000 on both halves.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.42* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.10 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.09 | 88 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.08 | 92 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.13 | 92 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.07 | 92 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.11 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *93* | *0.00x* |
| lib-stage2-lean | 0.023 | 0.040 | 0.50 | 84 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.044* | *0.36* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.045 | 0.18 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.045* | *0.17* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.046 | 0.23 | 80 | 1.00x |
| lib-stage2-lean-u1 | 0.027 | 0.046 | 0.40 | 82 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.052* | *0.10* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.10* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.10 | 77 | 1.00x |
| lib-stage1 | 0.034 | 0.048 | 0.24 | 80 | 1.00x |
| bq-expand | 0.090 | 0.179 | 0.43 | 61 | 1.05x |
| *bq-expand-aa-adjacent* | *0.090* | *0.179* | *0.45* | *61* | *1.05x* |
| *bq-expand-aa-distant* | *0.091* | *0.180* | *0.15* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.71 | 32 | 21.18x |
| *list-aa-distant* | *1.004* | *1.018* | *0.45* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.004* | *1.024* | *0.25* | *32* | *21.18x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0072, worst cell 2.43% on `flip-last-rows`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9992 on a worst cell of 0.49% on `flip-fwd-rows96`, its interval covering 1. The in-situ term reads 1.0186, 1.0223 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0069, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m11s, peak 209 MiB in use, 76 MiB max residency; the reader reads 35 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31.2 ms per call raw, 30.1 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.048/0.026/0.026

**Across the halves:** 11 of the 16 arms are faster on this half and 5 slower, at a geomean of 1.0058, from `bq-expand-aa-distant` at 0.9888 to `lib-stage2-lean-u1` at 1.1232, with `list` itself at 0.9983.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7605 over 5 of 6 shapes at sign p 0.22, a margin of 23.95% against this class's 0.72% floor (`list-aa-adjacent`). **What is this class's own is the run's largest single cell, and the disappearance of Run 34's.** `lib-stage2-lean-u1` on `flip-whole-square` reads **1.6225** in time across the halves on **0.9412** in counts, a time-over-counts of 1.72 and the widest row of `--cell-movers`; the count side is the latch of GHC [#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799) on a rank-1 view, which that mode names under its table, and the time side is four times what the counts explain. Meanwhile Run 34's 22.29% A/A cell on `flip-last-rows`, which set that run's basis floor and has [an open-list entry][open] of its own, reads **2.43%** here. Its two columns MAY be differenced, `list` having moved 0.17 of a point, at a class geomean of 1.0058 over the 16 arms, with 3 of 8 strategies past an A/A bar of 0.58 points. The counted work reads a counts geomean of 1.0023 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9995** and **0.9997** against 1.0 within 1%, and (2) at -313 and -316 on its thinnest view; (3)'s four spans all hold. The class's own A/A worst cell moved to the control half this run, 6.18% on `flip-last-rows` against the basis's 2.43%.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.13* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.18 | 113 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.12 | 122 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.03 | 129 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.03 | 129 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.15 | 113 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 129 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.18* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.04* | *122* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.024* | *0.09* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.024 | 0.10 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.13* | *111* | *1.00x* |
| lib-stage2-lean | 0.021 | 0.024 | 0.09 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.026 | 0.11 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.026 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.028* | *0.09* | *111* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.028* | *0.13* | *110* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.028 | 0.10 | 111 | 1.00x |
| lib-stage1 | 0.049 | 0.058 | 0.12 | 103 | 1.42x |
| bq-expand | 0.086 | 0.087 | 0.11 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.09* | *96* | *1.06x* |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.15* | *96* | *1.06x* |
| *list-aa-adjacent* | *1.000* | *1.004* | *0.17* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.26 | 54 | 21.22x |
| *list-aa-distant* | *1.003* | *1.008* | *0.37* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa` at 0.9882, worst cell 3.16% on `block-run64-off7`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.58% on `block-run64-page`, its interval covering 1. The in-situ term reads 1.0266, 1.0195 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9951, which the correction amplifies by 2.50x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m7s, peak 133 MiB in use, 37 MiB max residency; the reader reads 35 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.63 ms per call raw, 4.47 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.025/0.028/0.024/0.020

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 0.9993, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9849 to `list-aa-distant` at 1.0085, with `list` itself at 1.0062.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.028, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.9188 over 5 of 5 shapes at sign p 0.062, a margin of 8.12% against this class's 1.18% floor (`mut-odo-vecdims-aa`). **What is this class's own is that it is the cleanest null of the ten**: NOT ONE of the eight strategies clears its A/A bar of 1.23 points, the only class of which that is true this run, at a cross-half geomean of **0.9993** over the sixteen arms with the counted work at 1.0019. Its two columns MAY be differenced, `list` having moved 0.62 of a point, at a class geomean of 0.9993 over the 16 arms, with 0 of 8 strategies past an A/A bar of 1.23 points. The counted work reads a counts geomean of 1.0019 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **1.0000** and **0.9999** against 0.99 within 1.5%, which is the item's own centre missed by a point and inside its band on both halves, and (2) at -318 and -314 on its thinnest view; (3)'s four spans all hold.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.25 | 228 | 1.64x |
| liblist-stage2-sum | -- | -- | 0.15 | 230 | 1.55x |
| liblist-stage3-sum | -- | -- | 0.18 | 226 | 1.69x |
| liblist-stage4-list-sum | -- | -- | 0.26 | 230 | 1.51x |
| liblist-stage4-sum | -- | -- | 0.30 | 230 | 1.51x |
| libunord-stage1-sum | -- | -- | 0.29 | 223 | 2.07x |
| libunord-stage10-list-sum | -- | -- | 0.26 | 233 | 0.57x |
| libunord-stage10-sum | -- | -- | 0.32 | 233 | 0.55x |
| libunord-stage11-sum | -- | -- | 0.24 | 235 | 0.55x |
| libunord-stage12-sum | -- | -- | 0.28 | 235 | 0.55x |
| libunord-stage13-sum | -- | -- | 0.19 | 238 | 0.49x |
| libunord-stage6-loop-sum | -- | -- | 0.24 | 235 | 0.81x |
| libunord-stage6-sum | -- | -- | 0.20 | 234 | 0.83x |
| libunord-stage7-sum | -- | -- | 0.27 | 233 | 0.83x |
| libunord-stage9-sum | -- | -- | 0.29 | 233 | 0.55x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.23* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.04* | *249* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.07* | *250* | *0.01x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.052* | *0.068* | *0.26* | *229* | *1.27x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.052 | 0.069 | 0.27 | 229 | 1.27x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.052* | *0.068* | *0.20* | *229* | *1.27x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.055 | 0.068 | 0.29 | 229 | 1.27x |
| lib-stage2-lean-u1 | 0.057 | 0.101 | 0.21 | 227 | 1.46x |
| lib-stage2-lean | 0.058 | 0.103 | 0.29 | 228 | 1.46x |
| *mut-odo-vecdims-aa-distant* | *0.060* | *0.087* | *0.30* | *229* | *1.27x* |
| *mut-odo-vecdims-aa* | *0.060* | *0.088* | *0.20* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.061** | 0.088 | 0.23 | 229 | 1.27x |
| lib-stage1 | 0.091 | 0.108 | 0.21 | 221 | 2.32x |
| *bq-expand-aa-distant* | *0.134* | *0.193* | *0.17* | *218* | *1.44x* |
| *bq-expand-aa-adjacent* | *0.135* | *0.194* | *0.24* | *218* | *1.44x* |
| bq-expand | 0.135 | 0.193 | 0.15 | 217 | 1.44x |
| *list-aa-distant* | *0.994* | *1.001* | *0.16* | *179* | *21.57x* |
| *list-aa-adjacent* | *0.994* | *0.999* | *0.15* | *179* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.23 | 179 | 21.57x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9806, worst cell 4.57% on `small-flat64`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.65% on `small-patch-k5`, its interval covering 1. The in-situ term reads 0.9914, 0.9964 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9876, which the correction amplifies by 1.54x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m13s, peak 135 MiB in use, 54 MiB max residency; the reader reads 35 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.8 us per call raw, 6.57 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.077/0.051/0.060/0.088

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0078, from `lib-stage1` at 0.9860 to `lib-stage2-lean` at 1.0725, with `list` itself at 1.0162. **The baseline moved 1.62% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage2-lean-u1` leads outside the family at 0.057, priced against `mut-odo-vecdims` at 0.9277 over 1 of 5 shapes at sign p 0.38, a margin of 7.23% against this class's 1.94% floor (`mut-odo-vecdims-aa-distant`). **What is this class's own is where stage thirteen buys most, and the one class whose level clause is read off a family at 1.27x rather than at the result vector** --- the per-call constants showing through a call under a microsecond, which is the reservation this class has carried since 2026-09-07. Registration (1) reads **0.8410** on the basis and **0.8518** on the control, the deepest of the eleven populations, 12.7 points under the main set's reading, which is the next deepest. Its two columns may NOT be differenced, `list` having moved 1.62 of a point, at a class geomean of 1.0078 over the 16 arms, with 3 of 8 strategies past an A/A bar of 1.75 points. The counted work reads a counts geomean of 0.9987 over the same arms, 16 of them counted. **(3) dies here on the basis half**, its `lib-stage2-lean` against `list` span reading 0.0581 against a 0.0545 within 0.16 --- the widest miss of the item's twenty-two `pair` spans --- while the same span holds on the control at 0.0550, and its `counts` clause dies on both at 0.9986 and 1.0014. (2) holds at -289 on the thinnest view of each half. This class is one of the four whose columns may NOT be differenced, `list` having moved 1.62 points, and it is the one population where the basis executes FEWER instructions than the control, 0.9987 over the sixteen arms.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.34* | *86* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.37 | 98 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.34 | 98 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.39 | 98 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.32 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.35 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.32 | 98 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.03 | 110 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.32 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.34 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.35 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.20* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.014* | *0.016* | *0.32* | *98* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.015* | *0.016* | *0.33* | *98* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.28 | 98 | 1.00x |
| lib-stage2-lean | 0.015 | 0.017 | 0.32 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.36 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.017 | 0.32 | 97 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.018 | 0.39 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.024* | *0.028* | *0.24* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.024* | *0.028* | *0.26* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.028 | 0.19 | 94 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.102* | *0.38* | *79* | *1.35x* |
| bq-expand | 0.094 | 0.102 | 0.38 | 79 | 1.35x |
| *bq-expand-aa-distant* | *0.094* | *0.102* | *0.23* | *79* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 0.67 | 44 | 22.01x |
| *list-aa-distant* | *1.000* | *1.001* | *0.74* | *44* | *22.01x* |
| *list-aa-adjacent* | *1.002* | *1.008* | *0.73* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0029, worst cell 0.60% on `compose-scalar`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `compose-rev-bcast`, its interval covering 1. The in-situ term reads 1.0114, 1.0243 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0020, which the correction amplifies by 1.37x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m14s, peak 126 MiB in use, 33 MiB max residency; the reader reads 35 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 31 ms per call raw, 29.9 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.028/0.028/0.022/0.019

**Across the halves:** 11 of the 16 arms are faster on this half and 5 slower, at a geomean of 0.9957, from `lib-stage1` at 0.9348 to `mut-odo-vecdims-add-in-leaf-u1` at 1.0367, with `list` itself at 0.9965.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.028, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage2-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6164 over 4 of 4 shapes at sign p 0.12, a margin of 38.36% against this class's 0.29% floor (`bq-expand-aa-distant`). **What is this class's own is that TWO of the run's eight half-local movers against Run 34 land here**, and on opposite halves: `lib-stage1` at **1.0773** on the control and `mut-odo-vecdims-add-in-leaf-u1` at **1.0494** on the basis, each with its counts at 1.0000, so neither is the code and neither is registered. The class also carries one of the three latch cells, `compose-scalar` on `lib-stage2-lean-u1`, at 1.0714 in counts. Its two columns MAY be differenced, `list` having moved 0.35 of a point, at a class geomean of 0.9957 over the 16 arms, with 5 of 8 strategies past an A/A bar of 1.11 points. The counted work reads a counts geomean of 1.0033 over the same arms, 16 of them counted. Registration (1) reads stage thirteen over stage twelve at **0.9986** and **0.9998** against 1.0 within 1%, and (2) at -349 and -383 on its thinnest view; (3)'s four spans all hold.


## Provenance

**Run 35's halves differ in ONE COMPILER and in nothing else.** One source, `Main.hs` at `0eda736`, one shim at `f31bd1c` and one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1` in front of the assembler, one roster, one shape set, one class list and one bench order, both run under `WILDLOG=1 SATURATE=1`, both launched from the `hugebin/` mount and both with `-A32m -I0 -T -M8G` baked and read back by `+RTS --info`. What differs is the compiler and everything a compiler brings with it: the basis takes ghc-9.12.4 through `cabal.project` and its freeze, the control the in-tree stage1 of the GHC checkout, `10.1.20260803`, through `cabal.project.ghead` and its own freeze --- two stores, two plans and two sets of boot libraries, which the binaries carry back as `ghc-internal-9.1204.0` and `ghc-internal-10.100.0`. **Neither half adds a regime flag**: `-O1` is micro.cabal's own `ghc-options`, so both halves are plain -O1 and `diag` reads the ten-times-apart row on each. **So this pair is Run 34's recipe rebuilt from the moved source**, and against Run 34, which this run's note makes its cross-run reference, ONE term moved: three `Main.hs` commits, two of them comments alone.

**The roster is 35 timed arms over 19 main-set shapes and 665 benches, with 61 class views over ten classes for 2135 more, and it is NOT Run 34's.** `./roster-delta.py run34-exit run35-exit` reads 34 arms to 35 over 19 shapes to 19: ONE in and NONE out, the 34 survivors in the same order, no main-set shape moved and no class view moved either, every one of the ten classes holding the view count it held. In, landing at `0eda736`, is `libunord-stage13-sum`, stage twelve's route found with fewer passes over the axes, with the untimed `libunord-stage13` beside it. The L1 roster pass was therefore OWED and its MAIN leg was taken, 665 benches at rc=0; the ten class legs were started and stopped by the owner, who ruled them not owed for this pair, and the note's `L1 ROSTER PASS:` row says what a later run would pay to take the rest. **The shim did not move under this pair**, `align-as.py` standing at Run 33's and Run 34's `f31bd1c`, so what separates this run from Run 34 is the source and nothing else.

**The sequence was launched twice and one population was measured twice, so this run spans THREE windows rather than one.** The gate's four processes ran 01:21:07 to 01:54:30 and the main set's two 01:54:33 to 03:49:22; at 03:52 the session's harness killed the driver for a reported low-memory condition on a box with 43 GB free --- its memory-pressure reaper, fed by the kernel's stall counter, which a burst of faults on pages evicted earlier, swapped or page-cache, trips with the memory free, and not a shortage of this machine's memory; what was read out of the harness and the counters, and the switch that disables the reaper since, are in [the README's recommended tasks after this run](../README.md#recommended-tasks-after-run-35) --- and the class loop was re-launched detached at 03:55:00 and ran to 10:05:35, the four rider stages following to 10:18:40 and the counted work, on a box already handed back, from 10:20:36 to 11:06:52. `rev`'s first control-half process was two minutes in when the kill landed and its JSON is truncated; it is parked as `probe-killed-*` and the population was run again from the start. **And `bcastmid` was run twice on BOTH halves**, at 04:49:46 to 05:14:09 and again at 11:24:11 to 11:48:34, because `--wild` named an intrusion in the first control-half process --- three benches on `bcastmid-primes` at 0.28, 0.99 and 1.10 of a core, which the journal attributes to a root `CRON` session closing at 04:55:01. The first pair is parked as `probe-intruded-*` and the figures in this file are the second pair's. Every one of the twenty-two processes this file reads --- the main set on each half and 20 class processes, one per class per half --- exited 0 at the count its population asks for, with no complaint and no `!!` line in the wall-clock record, and the gheadexit half ran first throughout, each process's `start` line naming its instance under `hugebin/`. **The control half's evening instance is no longer under that name**: the instance gate's first real run, 2026-09-18 on a box at a load near two, read `hugebin/run35-gheadexit` at 1.135 of a fresh copy on `scaled-rank1-m1/mut-odo-vecdims-add-in-leaf-u1`, four readings a side, and swapped the copy in, parking the evening's instance as `hugebin/run35-gheadexit.slow`; the basis's read 0.959 and stands. So a re-timing of this run's control half from the mount reads the copy, and the evening's own instance is the `.slow` file until the deletion offer; whether it was a slow draw or the load is one quiet re-run of the gate away, and its movers above were read before either. The main-set two: `run35-gheadexit-main` took 0h57m28s at a peak of 229 MiB in use and 74 MiB max residency and `run35-exit-main` 0h57m20s at 195 MiB and 62 MiB. **ONE PROCESS WAS INTRUDED ON AND IT IS A GATE PROCESS**: `--wild` over the hundred and nineteen logs this run wrote reads 2 of 95 benches at or above 0.25 of a core in `run35-gate-gheadexit-a`, peak 0.81, and none in any of the twenty-two sequence logs, the other three gate logs or the 88 alone-leg rider logs; the five that leave are the wall-clock record and the riders' four drivers, which carry no samples. Those two benches are the third and fourth of that process, and the intruder was this session's own `./run-status.sh run35`, which the run list places on the line AFTER the launch.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes agree to **0.09**, **0.12** and **0.18** points on `list`, `bq-expand` and `mut-odo-vecdims`, and no arm crosses 1 between them: all five sit below it on both passes, the basis the faster, where Run 34's `list` and `mut-odo-vecdims` each crossed. **The machine check**, read against Run 34's fingerprint, which this run's note rules is its own comparison, puts `list`'s net at a geomean of **+0.11%**, inside the 3% bar, worst `stretch-tall-Mx2` at +1.75% and 0 of 19 shapes past 5%. It IS like-for-like, which no machine check since Run 32 has been --- Run 34's published half is this basis on the same shim, switch, launch and compiler, three `Main.hs` commits back --- and read arm by arm with `--compare run34-exit-main.json` the sixteen shared timed arms span **0.9849** to **1.0113** with `list` at **0.9996**. So the box has not moved and this run publishes inside the third machine era.

**Every one of the twenty-two processes gated clean, the plateau did not fire, and FIVE A/A worst cells sit above 5%, three of them on the basis half.** The preamble's victim spans 21.084 to 21.905 ms/iter across the run, a **3.89%** spread against a 5% band, all twenty-two processes asserting ONE `keep` and ONE `inuse`; within the halves the control's eleven span 3.52% and the basis's 1.40%, so most of the run's spread is the control's own. The five cells above 5% are `exit-bcastmid` at **11.18%** on `bcastmid-primes`, `exit-window` at **10.98%** on `window-128x128-k7`, `gheadexit-runs` at **6.94%** on `runs-4096`, `gheadexit-flip` at **6.18%** on `flip-last-rows` and `exit-main` at **5.55%** on `gather48-src-50`, and `--wild` clears every log they sit in --- the `bcastmid` one in the RERUN, the process taken after the cron that spoilt its first attempt was gone. Two of them are many times their population's floor: `exit-window`'s 10.98% against 0.88%, twelve times it, and `exit-main`'s 5.55% against 0.64%, nearly nine.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run35-exit`, md5 `9cc099284296dace3486995c868e7714`, and `run35-gheadexit`, md5 `84de3e4e445fbbaf0781be9a2b474450`, with `.text` at **20820165** bytes on the basis and **20973375** on the control --- the HEAD half larger by **153210**, the gap Runs 32, 33 and 34 read to the byte --- and load addresses of 4218880 and 4214784, Runs 32's and 34's two unchanged. Each half sits **12288** bytes, three pages, above its Run 34 counterpart; this file offers no mechanism for that. **NEITHER md5 is two-sided**: `Main.hs` moved from `2496c98` to `0eda736` since Run 34's build of this recipe, so no md5 here can reproduce an earlier binary's, and what the two say is that they differ from each other. The commit the pair was built at is `0eda736`, transcribed from the pair note while that note is still here; the tree the sequence ran on was `fc9c4a3`, three commits further on and none of them touching `Main.hs` or the shim.

**The source moved and a timed function landed while the shim stood still, and the pinning claim's strong form HOLDS for the tracked offsets across that change.** The tracked 28-byte loops were read at the build with `--delta`, and re-read here off the same binaries. Against `run34-exit`, which is both the previous build of this recipe and the run this one is compared with, EVERY mod-64 offset is preserved on both groups, `[0, 0, 0, 8, 4, 0]` and `[0, 0]`, with NO address surviving to the byte and ONE displacement on each, `0x1b40` --- three `Main.hs` commits and one timed arm moving every copy and no head's offset. **No second `--delta` is owed this run**, the previous build of the recipe and the comparison run being the same binary, where Runs 33 and 34 each had to read two. **Within the pair** `./loop-offsets.py run35-gheadexit run35-exit` puts the six-copy group at `[0, 0, 0, 8, 4, 0]` on the basis and `[18, 0, 0, 0, 9, 2]` on the control and the two-copy group at `[0, 0]` on both, Run 34's offsets unchanged, and post-run step 0's twins name those six as `fbMidCopy`, `fbCanonVecdims`, `fbMutOdoVecdimsAddIn`, `fbMutOdoVecdims`, `fbMutOdoVecdimsAddOut` and `fbMutOdoVecdimsAddBoth` on each half, with `fbBuild` and `fbMutOdo` the two. **Neither twin's count check refuses**: 33 self-loops of 28 B in 26 sequences on the basis and on its twin alike, 34 in 27 on the control and on its twin alike.

**The straddling loops stand at EIGHT on each half, as on Runs 32 to 34, and no exit span sits astride on either.** `loop-offsets.py --survey` reads **322** self-loops of at most 64 B in the basis's own compiled code, 193 of them at offset 0, and **339** on the control, 203 at offset 0 --- about three fifths at offset 0 on both halves, as on Runs 33 and 34. **Each half reads one self-loop and one straddler fewer than this run's own preparation recorded**, 323 with 9 straddling on the basis and 340 with 9 on the control, and the basis has lost an exit span astride besides, which the control never had: the astride reading was a phantom the owner refused at `e4f0624`, a stray-REX body the survey had been counting, and this is the first reading of this pair with the fix in. Within the pair `--library` reads **136** self-loops in common in the LINKED libraries, **11.0%** of them at the same offset in line and **65.4%** in the same straddle state --- Runs 32's and 34's three figures to the digit for the fourth run, under a moved source, and this file offers no account of that. **Post-run step 0's naming was taken off the binaries that were timed**, with two `-g3` twins built from the same two recipes: six of the basis's eight straddlers are named by byte identity --- `fillStage2Short`, `fbMutOdoVecdimsAddInLeafU2` twice, and its `Down`, `Last` and `Ptr` forms --- and three of the control's, one of those three off the OTHER half's twin, with two more of the control's readable off single-member `--loose` signatures, `-U2Down` and `-U2Last`. The basis twin holds 319 self-loops against either timed binary's 322 and 339, so the tool refuses ITS population comparison and every name off it rests on its own byte match.

**The regime was confirmed in this run's own binaries before the hours were spent, and both halves read the same side of it.** `diag` reads `baseOffsetsScan` against `baseOffsetsMut` on `vgg-14-c512` at **24066407** against **2408530** on the basis and 24066455 against 2408530 on the control --- **9.992** times apart on each, the ten times this README has attributed to plain -O1 since Run 8, and Run 34's four figures unchanged. The version comes out of the binaries rather than off a project file: `ghc-internal-9.1204.0` on the basis and `ghc-internal-10.100.0` on the control, the HEAD Runs 32 to 34 ran.

**The three main-set anchors** read **6.35 us** on `cnn-slice-c32`, **3.70 ms** on `cnn-L2-24x24-c32` and **39.4 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm:
| shape | `l` | `list`, per call | net | `gheadexit`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.52 us | 6.35 us | 6.40 us |
| `cnn-L2-24x24-c32` | 165888 | 3.80 ms | 3.70 ms | 3.72 ms |
| `stretch-wide-2xM` | 1800000 | 40.5 ms | 39.4 ms | 40.3 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's shapes, raw and net.** The main set's three guard a baseline that moves for every population at once; a class anchor guards one that could move for that mechanism alone, which is the case a table of ratios hides completely. The `runs` anchor is `runs-2` at **40.98 ms** raw and **39.90 ms** net on the basis, against Run 34's 40.86 ms and 39.79 ms on that run's basis --- **0.28%** and **0.29%** above it, computed from the cells and not from the rounded milliseconds, and carrying the source term and the box and nothing else. **The control half reads 42.33 ms and 41.25 ms on the same shape**, 3.4% above the basis. **NO class population moved this run**: `roster-delta.py` reads 61 class views to 61 and every one of the ten classes holding its own count, so a class figure against Run 34 is read over the same shapes on both sides.

**The correction sits on the same footing in both halves, and one cell of the whole run is one the reader flags.** The two `sum-only` arms agree to within **0.24%** on every population and on both halves of the pair --- 0.9976 to 1.0017 across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. `CI%` reads a geomean of **0.97** over the 35 arms, 20 wider on the basis and 15 narrower. **ONE cell sits below R2 0.99**, on the looping stage-six consumer as both of Run 34's were: `runs-3/libunord-stage6-loop-sum` at 0.9872 on the control, and the basis carries none; no cell of any population sits under ten samples.

**The counted work covers every population, no cell was refused anywhere, and the two compilers emit very nearly the same work.** The counts geomean over the sixteen timed arms runs **0.9987** on `small` to **1.0098** on `window`, the main set at **1.0053**. On the main set `time/counts` puts `lib-stage1` at **1.0194**, `lib-stage2-lean` at 1.0183 and the shipped leaf at 1.0132, while `list` sits at **0.9823** --- the basis executing about one percent MORE instructions on the reference and running it 0.77 of a point FASTER, which is the whole of why this run's main set lost its subtraction. Among the seven populations whose columns may be differenced, the one where the counts carry much of a figure is `window`, `lib-stage1` and `lib-stage2-lean` executing 1.76 and 1.56 points more on the basis and taking 5.36 and 4.81 more time. So the compiler term this pair measures is small, and mostly outside the instruction stream where it is not. **Read per cell rather than per arm, the geomeans hide the run's largest cells, and post-run step 4b takes that reading.** The largest count differences of the run are `lib-stage2-lean-u1` on `compose-scalar` at **1.0714** and on `flip-whole-square` and `scaled-rank1-m1` at **0.9412**, GHC [#27799](https://gitlab.haskell.org/ghc/ghc/-/work_items/27799)'s latch on a rank-1 view --- and on `flip-whole-square` that arm's TIME reads **1.6225**, four times what its counts explain and the widest row of `--cell-movers`. With their counts at 1.0000, NINE consumers read 0.7563 to 0.7581 on `runs-3`, the basis a quarter faster on every one of them on identical instruction counts; the two `-list-sum` arms of that shape sit apart together, `liblist-stage4-list-sum` at 0.8740 and `libunord-stage10-list-sum` at 0.8741, on counts of 0.9787, and are not among them --- which is the pair the answer to [the open list][open]'s entry turns on, both bringing base's `sum` as their fold and holding no route.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0000** on the basis and **1.0000** on the control on the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0327** and **1.1059** on the basis and **1.0313** and **1.1104** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and ten or eleven on `bq-expand`, by nearly the same on both halves, which is where it has run since Run 17. So the compiler does not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns do not part.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, and the state the preamble puts on a process comes back at a geomean of **1.1140** on the basis and **1.1147** on the control, **0.07** of a point apart, the closest the two halves have read it. What the roster adds on top of that state is **1.0217** on the basis, 8 of 19 shapes above 1, and **1.0293** on the control, 14 of 19; the basis's rest runs 0.9795 on `stretch-bigstride` to 1.2218 on `stretch-r5-8x432`, the control's 0.9798 on `stretch-pow2stride` to 1.2228 on that same worst shape.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 34's: the same two compilers at plain -O1 under the exit span, ghc-9.12.4 the basis and GHC HEAD the control, both halves rebuilt by Run 34's recipe from the moved source, on the same machine and with no reboot between, so what varies from Run 34 is the source alone: `libunord-stage13-sum`, stage twelve's route found with fewer passes over the axes (reasons at `routeUnord13`; its fill is rostered checked and never timed), and the two pieces it shares with older arms, the merge step `mergeInto` that `canonViewOfPairs` now folds and the route tail `routeOf` that `routeList4` and `dispatchLean` now end in. Each prediction is its own kill condition, a `predict:` span that fails kills its item, and every span is read on both halves.

(1) *Stage thirteen reads under stage twelve where a call is short and level where it is long.* A probe of the two arms on a plain -O1 build of the committed source, `0eda736`, launched from the build directory rather than `hugebin/` with nothing else running, `probe-stage13-main.json` and one `probe-stage13-<class>.json` per class, read the pair at 0.9726 on the main set, from 0.681 on `cnn-L1-6x6-c1` to 1.017 on `stretch-coprime-r7`; at 0.8561 on `small`, from 0.765 on `small-flat64` to 0.926 on `small-row96`; at 0.9841 on `rev` and 0.9849 on `scaled`; and within a percent of level on the other seven classes, `block` at 0.9910 the furthest: `predict: pair libunord-stage13-sum libunord-stage12-sum 0.97 within 2% on main both`, `predict: pair libunord-stage13-sum libunord-stage12-sum 0.86 within 3% on small both`, `predict: pair libunord-stage13-sum libunord-stage12-sum 0.98 within 2% on rev both`, `predict: pair libunord-stage13-sum libunord-stage12-sum 0.985 within 1.5% on scaled both`, `predict: pair libunord-stage13-sum libunord-stage12-sum 0.99 within 1.5% on block both`, `predict: pair libunord-stage13-sum libunord-stage12-sum 1.0 within 1% on bcast,bcastmid,compose,flip,runs,window both`. The route is stage twelve's on every view, which `check` holds it to and no span reads.

**Read by --predictions, item (1):** `pair libunord-stage13-sum libunord-stage12-sum 0.97 within 2% on main both`: HELD on main basis, read 0.9679 over 19 shape(s), 0.21 point(s) off, within 2.00%; HELD on main control, read 0.9722 over 19 shape(s), 0.22 point(s) off, within 2.00% --- `pair libunord-stage13-sum libunord-stage12-sum 0.86 within 3% on small both`: HELD on small basis, read 0.8410 over 5 shape(s), 1.90 point(s) off, within 3.00%; HELD on small control, read 0.8518 over 5 shape(s), 0.82 point(s) off, within 3.00% --- `pair libunord-stage13-sum libunord-stage12-sum 0.98 within 2% on rev both`: HELD on rev basis, read 0.9823 over 3 shape(s), 0.23 point(s) off, within 2.00%; HELD on rev control, read 0.9852 over 3 shape(s), 0.52 point(s) off, within 2.00% --- `pair libunord-stage13-sum libunord-stage12-sum 0.985 within 1.5% on scaled both`: HELD on scaled basis, read 0.9956 over 3 shape(s), 1.06 point(s) off, within 1.50%; HELD on scaled control, read 0.9967 over 3 shape(s), 1.17 point(s) off, within 1.50% --- `pair libunord-stage13-sum libunord-stage12-sum 0.99 within 1.5% on block both`: HELD on block basis, read 1.0000 over 5 shape(s), 1.00 point(s) off, within 1.50%; HELD on block control, read 0.9999 over 5 shape(s), 0.99 point(s) off, within 1.50% --- `pair libunord-stage13-sum libunord-stage12-sum 1.0 within 1% on bcast,bcastmid,compose,flip,runs,window both`: HELD on bcast basis, read 0.9964 over 6 shape(s), 0.36 point(s) off, within 1.00%; HELD on bcast control, read 0.9994 over 6 shape(s), 0.06 point(s) off, within 1.00%; HELD on bcastmid basis, read 0.9980 over 4 shape(s), 0.20 point(s) off, within 1.00%; HELD on bcastmid control, read 0.9990 over 4 shape(s), 0.10 point(s) off, within 1.00%; HELD on compose basis, read 0.9986 over 4 shape(s), 0.14 point(s) off, within 1.00%; HELD on compose control, read 0.9998 over 4 shape(s), 0.02 point(s) off, within 1.00%; HELD on flip basis, read 0.9995 over 6 shape(s), 0.05 point(s) off, within 1.00%; HELD on flip control, read 0.9997 over 6 shape(s), 0.03 point(s) off, within 1.00%; HELD on runs basis, read 0.9984 over 17 shape(s), 0.16 point(s) off, within 1.00%; HELD on runs control, read 1.0004 over 17 shape(s), 0.04 point(s) off, within 1.00%; HELD on window basis, read 0.9942 over 8 shape(s), 0.58 point(s) off, within 1.00%; HELD on window control, read 0.9979 over 8 shape(s), 0.21 point(s) off, within 1.00%.

(2) *And it retires fewer instructions than stage twelve on every view, by more than two hundred a call.* Counted on the plain build as run-counts.sh counts, the gap runs from 295 on `small-row96` to 2001 on `rev-cnn-L1-24x24-c1`, the four views with an extent-1 axis, which the sort no longer sees, all above 1860: `predict: countdiff libunord-stage13-sum libunord-stage12-sum under -200 on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,small,window both`, read with `--counts` over each population's own sweep.

**Read by --predictions, item (2):** `countdiff libunord-stage13-sum libunord-stage12-sum under -200 on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,small,window both`: HELD on bcast basis, A - B up to -574 over 6 view(s), under -200; HELD on bcast control, A - B up to -578 over 6 view(s), under -200; HELD on bcastmid basis, A - B up to -884 over 4 view(s), under -200; HELD on bcastmid control, A - B up to -885 over 4 view(s), under -200; HELD on block basis, A - B up to -318 over 5 view(s), under -200; HELD on block control, A - B up to -314 over 5 view(s), under -200; HELD on compose basis, A - B up to -349 over 4 view(s), under -200; HELD on compose control, A - B up to -383 over 4 view(s), under -200; HELD on flip basis, A - B up to -313 over 6 view(s), under -200; HELD on flip control, A - B up to -316 over 6 view(s), under -200; HELD on main basis, A - B up to -283 over 19 view(s), under -200; HELD on main control, A - B up to -283 over 19 view(s), under -200; HELD on rev basis, A - B up to -557 over 3 view(s), under -200; HELD on rev control, A - B up to -550 over 3 view(s), under -200; HELD on runs basis, A - B up to -287 over 17 view(s), under -200; HELD on runs control, A - B up to -289 over 17 view(s), under -200; KILLED on scaled basis, A - B up to -138 over 3 view(s), under -200; KILLED on scaled control, A - B up to -136 over 3 view(s), under -200; HELD on small basis, A - B up to -289 over 5 view(s), under -200; HELD on small control, A - B up to -289 over 5 view(s), under -200; HELD on window basis, A - B up to -664 over 8 view(s), under -200; HELD on window control, A - B up to -645 over 8 view(s), under -200.

(3) *The shared code left the two ported library arms where Run 34 read them.* `lib-stage2-lean` compiles through `mergeInto` now and `liblist-stage4-sum` through `mergeInto` and `routeOf`, and a plain build of the committed source counted every control cell read within five instructions of a plain build of Run 34's source, `2496c98`, whose only later changes are to comments, but `liblist-stage4-sum` on `small-row96`, 27 under. So their counts read Run 34's, exact but for that cell: `predict: counts lib-stage2-lean 1.0 within 0.1% on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,small,window both`, `predict: counts liblist-stage4-sum 1.0 within 0.1% on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,window both`, `predict: counts liblist-stage4-sum 1.0 within 0.3% on small both`; and their times against `list` read Run 34's, the machine and the recipe being the same: per population the target is the geometric mean of Run 34's two halves' `--pair ARM list` figures and the tolerance three percent of it, five on the three where Run 34's own halves part by more than a point and a half, written in points of the ratio since that is what a span's `within` reads: `predict: pair lib-stage2-lean list 0.0286 within 0.086% on main both`, `predict: pair lib-stage2-lean list 0.0156 within 0.047% on bcast both`, `predict: pair lib-stage2-lean list 0.0121 within 0.036% on bcastmid both`, `predict: pair lib-stage2-lean list 0.0213 within 0.064% on block both`, `predict: pair lib-stage2-lean list 0.0147 within 0.044% on compose both`, `predict: pair lib-stage2-lean list 0.0241 within 0.072% on flip both`, `predict: pair lib-stage2-lean list 0.0234 within 0.07% on rev both`, `predict: pair lib-stage2-lean list 0.0243 within 0.073% on runs both`, `predict: pair lib-stage2-lean list 0.0237 within 0.071% on scaled both`, `predict: pair lib-stage2-lean list 0.0545 within 0.16% on small both`, `predict: pair lib-stage2-lean list 0.0233 within 0.12% on window both`, `predict: pair liblist-stage4-sum list 0.0569 within 0.17% on main both`, `predict: pair liblist-stage4-sum list 0.0471 within 0.14% on bcast both`, `predict: pair liblist-stage4-sum list 0.0385 within 0.12% on bcastmid both`, `predict: pair liblist-stage4-sum list 0.0226 within 0.068% on block both`, `predict: pair liblist-stage4-sum list 0.0475 within 0.14% on compose both`, `predict: pair liblist-stage4-sum list 0.0414 within 0.12% on flip both`, `predict: pair liblist-stage4-sum list 0.0515 within 0.15% on rev both`, `predict: pair liblist-stage4-sum list 0.0257 within 0.13% on runs both`, `predict: pair liblist-stage4-sum list 0.0560 within 0.17% on scaled both`, `predict: pair liblist-stage4-sum list 0.0788 within 0.39% on small both`, `predict: pair liblist-stage4-sum list 0.0430 within 0.13% on window both`.

**Read by --predictions, item (3):** `counts lib-stage2-lean 1.0 within 0.1% on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,small,window both`: HELD on bcast basis, read 1.0001 over 6 shape(s), 0.01 point(s) off, within 0.10%; HELD on bcast control, read 0.9999 over 6 shape(s), 0.01 point(s) off, within 0.10%; HELD on bcastmid basis, read 1.0004 over 4 shape(s), 0.04 point(s) off, within 0.10%; HELD on bcastmid control, read 0.9996 over 4 shape(s), 0.04 point(s) off, within 0.10%; HELD on block basis, read 1.0004 over 5 shape(s), 0.04 point(s) off, within 0.10%; HELD on block control, read 0.9996 over 5 shape(s), 0.04 point(s) off, within 0.10%; HELD on compose basis, read 1.0000 over 4 shape(s), 0.00 point(s) off, within 0.10%; HELD on compose control, read 1.0000 over 4 shape(s), 0.00 point(s) off, within 0.10%; HELD on flip basis, read 1.0002 over 6 shape(s), 0.02 point(s) off, within 0.10%; HELD on flip control, read 0.9998 over 6 shape(s), 0.02 point(s) off, within 0.10%; KILLED on main basis, read 1.0062 over 19 shape(s), 0.62 point(s) off, within 0.10%; KILLED on main control, read 0.9938 over 19 shape(s), 0.62 point(s) off, within 0.10%; KILLED on rev basis, read 1.0074 over 3 shape(s), 0.74 point(s) off, within 0.10%; KILLED on rev control, read 0.9926 over 3 shape(s), 0.74 point(s) off, within 0.10%; HELD on runs basis, read 1.0000 over 17 shape(s), 0.00 point(s) off, within 0.10%; HELD on runs control, read 1.0000 over 17 shape(s), 0.00 point(s) off, within 0.10%; HELD on scaled basis, read 1.0000 over 3 shape(s), 0.00 point(s) off, within 0.10%; HELD on scaled control, read 1.0000 over 3 shape(s), 0.00 point(s) off, within 0.10%; KILLED on small basis, read 0.9986 over 5 shape(s), 0.14 point(s) off, within 0.10%; KILLED on small control, read 1.0014 over 5 shape(s), 0.14 point(s) off, within 0.10%; KILLED on window basis, read 1.0156 over 8 shape(s), 1.56 point(s) off, within 0.10%; KILLED on window control, read 0.9846 over 8 shape(s), 1.54 point(s) off, within 0.10% --- `counts liblist-stage4-sum 1.0 within 0.1% on main,bcast,bcastmid,block,compose,flip,rev,runs,scaled,window both`: HELD on bcast basis, read 1.0001 over 6 shape(s), 0.01 point(s) off, within 0.10%; HELD on bcast control, read 0.9999 over 6 shape(s), 0.01 point(s) off, within 0.10%; HELD on bcastmid basis, read 1.0007 over 4 shape(s), 0.07 point(s) off, within 0.10%; HELD on bcastmid control, read 0.9993 over 4 shape(s), 0.07 point(s) off, within 0.10%; HELD on block basis, read 1.0000 over 5 shape(s), 0.00 point(s) off, within 0.10%; HELD on block control, read 1.0000 over 5 shape(s), 0.00 point(s) off, within 0.10%; HELD on compose basis, read 1.0000 over 4 shape(s), 0.00 point(s) off, within 0.10%; HELD on compose control, read 1.0000 over 4 shape(s), 0.00 point(s) off, within 0.10%; HELD on flip basis, read 1.0001 over 6 shape(s), 0.01 point(s) off, within 0.10%; HELD on flip control, read 0.9999 over 6 shape(s), 0.01 point(s) off, within 0.10%; KILLED on main basis, read 1.0073 over 19 shape(s), 0.73 point(s) off, within 0.10%; KILLED on main control, read 0.9928 over 19 shape(s), 0.72 point(s) off, within 0.10%; KILLED on rev basis, read 1.0086 over 3 shape(s), 0.86 point(s) off, within 0.10%; KILLED on rev control, read 0.9914 over 3 shape(s), 0.86 point(s) off, within 0.10%; HELD on runs basis, read 1.0000 over 17 shape(s), 0.00 point(s) off, within 0.10%; HELD on runs control, read 1.0000 over 17 shape(s), 0.00 point(s) off, within 0.10%; HELD on scaled basis, read 1.0001 over 3 shape(s), 0.01 point(s) off, within 0.10%; HELD on scaled control, read 0.9999 over 3 shape(s), 0.01 point(s) off, within 0.10%; KILLED on window basis, read 1.0186 over 8 shape(s), 1.86 point(s) off, within 0.10%; KILLED on window control, read 0.9818 over 8 shape(s), 1.82 point(s) off, within 0.10% --- `counts liblist-stage4-sum 1.0 within 0.3% on small both`: HELD on small basis, read 0.9977 over 5 shape(s), 0.23 point(s) off, within 0.30%; HELD on small control, read 1.0023 over 5 shape(s), 0.23 point(s) off, within 0.30% --- `pair lib-stage2-lean list 0.0286 within 0.086% on main both`: HELD on main basis, read 0.0287 over 19 shape(s), 0.01 point(s) off, within 0.09%; HELD on main control, read 0.0278 over 19 shape(s), 0.08 point(s) off, within 0.09% --- `pair lib-stage2-lean list 0.0156 within 0.047% on bcast both`: HELD on bcast basis, read 0.0157 over 6 shape(s), 0.01 point(s) off, within 0.05%; HELD on bcast control, read 0.0155 over 6 shape(s), 0.01 point(s) off, within 0.05% --- `pair lib-stage2-lean list 0.0121 within 0.036% on bcastmid both`: HELD on bcastmid basis, read 0.0123 over 4 shape(s), 0.02 point(s) off, within 0.04%; HELD on bcastmid control, read 0.0123 over 4 shape(s), 0.02 point(s) off, within 0.04% --- `pair lib-stage2-lean list 0.0213 within 0.064% on block both`: HELD on block basis, read 0.0212 over 5 shape(s), 0.01 point(s) off, within 0.06%; HELD on block control, read 0.0214 over 5 shape(s), 0.01 point(s) off, within 0.06% --- `pair lib-stage2-lean list 0.0147 within 0.044% on compose both`: HELD on compose basis, read 0.0147 over 4 shape(s), 0.00 point(s) off, within 0.04%; HELD on compose control, read 0.0149 over 4 shape(s), 0.02 point(s) off, within 0.04% --- `pair lib-stage2-lean list 0.0241 within 0.072% on flip both`: HELD on flip basis, read 0.0238 over 6 shape(s), 0.03 point(s) off, within 0.07%; HELD on flip control, read 0.0239 over 6 shape(s), 0.02 point(s) off, within 0.07% --- `pair lib-stage2-lean list 0.0234 within 0.07% on rev both`: HELD on rev basis, read 0.0237 over 3 shape(s), 0.03 point(s) off, within 0.07%; KILLED on rev control, read 0.0226 over 3 shape(s), 0.08 point(s) off, within 0.07% --- `pair lib-stage2-lean list 0.0243 within 0.073% on runs both`: HELD on runs basis, read 0.0245 over 17 shape(s), 0.02 point(s) off, within 0.07%; HELD on runs control, read 0.0244 over 17 shape(s), 0.01 point(s) off, within 0.07% --- `pair lib-stage2-lean list 0.0237 within 0.071% on scaled both`: HELD on scaled basis, read 0.0242 over 3 shape(s), 0.05 point(s) off, within 0.07%; HELD on scaled control, read 0.0242 over 3 shape(s), 0.05 point(s) off, within 0.07% --- `pair lib-stage2-lean list 0.0545 within 0.16% on small both`: KILLED on small basis, read 0.0581 over 5 shape(s), 0.36 point(s) off, within 0.16%; HELD on small control, read 0.0550 over 5 shape(s), 0.05 point(s) off, within 0.16% --- `pair lib-stage2-lean list 0.0233 within 0.12% on window both`: HELD on window basis, read 0.0240 over 8 shape(s), 0.07 point(s) off, within 0.12%; HELD on window control, read 0.0230 over 8 shape(s), 0.03 point(s) off, within 0.12% --- `pair liblist-stage4-sum list 0.0569 within 0.17% on main both`: HELD on main basis, read 0.0570 over 19 shape(s), 0.01 point(s) off, within 0.17%; HELD on main control, read 0.0559 over 19 shape(s), 0.10 point(s) off, within 0.17% --- `pair liblist-stage4-sum list 0.0471 within 0.14% on bcast both`: HELD on bcast basis, read 0.0473 over 6 shape(s), 0.02 point(s) off, within 0.14%; HELD on bcast control, read 0.0473 over 6 shape(s), 0.02 point(s) off, within 0.14% --- `pair liblist-stage4-sum list 0.0385 within 0.12% on bcastmid both`: HELD on bcastmid basis, read 0.0386 over 4 shape(s), 0.01 point(s) off, within 0.12%; HELD on bcastmid control, read 0.0389 over 4 shape(s), 0.04 point(s) off, within 0.12% --- `pair liblist-stage4-sum list 0.0226 within 0.068% on block both`: HELD on block basis, read 0.0226 over 5 shape(s), 0.00 point(s) off, within 0.07%; HELD on block control, read 0.0229 over 5 shape(s), 0.03 point(s) off, within 0.07% --- `pair liblist-stage4-sum list 0.0475 within 0.14% on compose both`: HELD on compose basis, read 0.0473 over 4 shape(s), 0.02 point(s) off, within 0.14%; HELD on compose control, read 0.0471 over 4 shape(s), 0.04 point(s) off, within 0.14% --- `pair liblist-stage4-sum list 0.0414 within 0.12% on flip both`: HELD on flip basis, read 0.0411 over 6 shape(s), 0.03 point(s) off, within 0.12%; HELD on flip control, read 0.0414 over 6 shape(s), 0.00 point(s) off, within 0.12% --- `pair liblist-stage4-sum list 0.0515 within 0.15% on rev both`: HELD on rev basis, read 0.0526 over 3 shape(s), 0.11 point(s) off, within 0.15%; HELD on rev control, read 0.0507 over 3 shape(s), 0.08 point(s) off, within 0.15% --- `pair liblist-stage4-sum list 0.0257 within 0.13% on runs both`: HELD on runs basis, read 0.0253 over 17 shape(s), 0.04 point(s) off, within 0.13%; HELD on runs control, read 0.0262 over 17 shape(s), 0.05 point(s) off, within 0.13% --- `pair liblist-stage4-sum list 0.0560 within 0.17% on scaled both`: HELD on scaled basis, read 0.0564 over 3 shape(s), 0.04 point(s) off, within 0.17%; HELD on scaled control, read 0.0567 over 3 shape(s), 0.07 point(s) off, within 0.17% --- `pair liblist-stage4-sum list 0.0788 within 0.39% on small both`: HELD on small basis, read 0.0797 over 5 shape(s), 0.09 point(s) off, within 0.39%; HELD on small control, read 0.0799 over 5 shape(s), 0.11 point(s) off, within 0.39% --- `pair liblist-stage4-sum list 0.0430 within 0.13% on window both`: HELD on window basis, read 0.0436 over 8 shape(s), 0.06 point(s) off, within 0.13%; HELD on window control, read 0.0430 over 8 shape(s), 0.00 point(s) off, within 0.13%.

**One of the three held and two were killed --- and BOTH kills fall on a clause the run's own instrument reads differently from the way the item's prose states it.** Every verdict below is its item's KILL CONDITION applied across the populations and halves the item names, an item that names no half being read on both, since every span of this registration carries `both`; every figure is re-derived from this run's own JSONs, by `--predictions` over each population on each half, by `--cells` where a clause names a shape, and by `--counts` where it names instructions. **One thing governs how the list reads**: stage thirteen does on the clock exactly what it was built to do, on every population and both compilers, and what fails is a count clause on one class and a pair of spans whose vocabulary asks a question their own sentences do not.

(1) *Stage thirteen reads under stage twelve where a call is short and level where it is long.* **HELD, on all twenty-two readings.** Basis then control: the main set reads **0.9679** and **0.9722** against 0.97 within 2%, `small` **0.8410** and **0.8518** against 0.86 within 3%, `rev` 0.9823 and 0.9852 against 0.98 within 2%, `scaled` 0.9956 and 0.9967 against 0.985 within 1.5%, `block` 1.0000 and 0.9999 against 0.99 within 1.5%, and the six populations the item puts at level --- `bcast`, `bcastmid`, `compose`, `flip`, `runs` and `window` --- come in at 0.9964 and 0.9994, 0.9980 and 0.9990, 0.9986 and 0.9998, 0.9995 and 0.9997, 0.9984 and 1.0004, and 0.9942 and 0.9979, each against 1.0 within 1%. The item's shape is the reading's too: the gain is deepest where the call is shortest, 12.7 points deeper on `small` than on the main set, which is the next deepest, and level on the six long-call classes.

(2) *And it retires fewer instructions than stage twelve on every view, by more than two hundred a call.* **KILLED on `scaled`, on both halves, and held on the other ten populations.** The thinnest view of each population runs from **-283** on the main set to **-885** on `bcastmid`; on `scaled` it is `scaled-rank1-m1` at **-138** on the basis and **-136** on the control, inside the two hundred the item asked for. **The direction never reverses**: no view of any population retires more under stage thirteen than under stage twelve, so what the kill prices is the size of the saving on the class of rank-1 and scaled views and not its sign. A next registration setting a floor on a count difference wants the floor taken from the population where the reordering has least to remove, which is what `scaled` is.

(3) *The shared code left the two ported library arms where Run 34 read them.* **KILLED on four of its spans --- two `counts` and two `pair` --- while the sentence itself HOLDS.** Read as the prose states it --- this run's counts against Run 34's, same half --- `liblist-stage4-sum` and `lib-stage2-lean` give geomeans of **0.99999** and **0.99998** on the basis and **0.99997** and **1.00006** on the control, no shape further than 0.07 of a point, and the cross-run counts geomean over all 34 arms the sweep carries is **1.0000**. What the spans read is something else: a `counts` span under `--compare` reads this half over the OTHER, a comparison of the two COMPILERS, and it misses on the main set (1.0062 and 1.0073 against 0.1%), on `rev` (1.0074 and 1.0086), on `window` (1.0156 and 1.0186) and on `small`'s `lib-stage2-lean` (0.9986 and 1.0014), while holding on the other seven populations. **The two earlier runs of this pair read 1.0062 and 1.0063 on the main set, Run 33's and Run 34's**, so that span was unholdable the day it was written and its band was set against a quantity nobody had measured. Its twenty-two `pair ARM list` spans miss twice besides, both under four tenths of a point: `lib-stage2-lean` against `list` on `rev`'s control half at **0.0226** against a 0.0234 within 0.07, and on `small`'s basis half at **0.0581** against a 0.0545 within 0.16 --- the second being `small`'s own 1.62-point `list` move showing through a span whose target was taken from Run 34's two halves averaged.
