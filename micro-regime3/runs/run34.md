# Run 34 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span, from the moved source)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 34 (GHC HEAD against ghc-9.12.4, both at plain -O1 under the exit span, from the moved source): asked again from `hugebin/`, the two compilers come back within 2.6 points on every main-set arm, and the lean fill that parted by 3.54 on Run 33 is level at 1.0047.** The pair is Run 33's recipe unchanged --- `LOOP_EXITSPAN=1` on both halves, the shim switch that charges a loop head's fall-through exit with its body, which [the placement section][floor] prices --- rebuilt at `Main.hs` `2496c98` with the shim at `f31bd1c`, one shim environment, one regime, one roster and one bench order, every process launched from the `hugebin/` mount, the 9.12.4 half `run34-exit` publishing and the in-tree stage1 `10.1.20260803` half `run34-gheadexit` the candidate. So `the basis` below is the 9.12.4 half and every `cross` figure reads basis over control, ABOVE 1 meaning the control is the faster --- `lib-stage1` on `cnn-L1-24x24-c1` taking 5.755 us net on the basis and 5.128 us on the control. Over the sixteen main-set arms that carry a cross-half figure, TWELVE sit within 1% of 1 and the four outside reach 2.58 points: `lib-stage1` at **1.0258** and the shipped leaf with its two A/A copies at **1.0127**, 1.0114 and 1.0111, all four faster under HEAD. **The bar an arm has to clear to be the compiler's rather than the run's is 0.23 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, `bq-expand-aa-adjacent` against `bq-expand`, which `--compare` prints under every table and which is NOT this population's floor, that being 0.51% and measured WITHIN one half --- and SIX of the eight strategies clear it, FOUR clearing the wider of the two halves' floors, the bar the ruling of 2026-09-02 holds a cross-half margin to; Run 33's bar was 0.16 points and all eight cleared it. No arm moves past 3%, and the geomean over the arms is **1.0048**, against Run 33's 1.0068 and Run 32's 0.9985. **Every cross-run reading this file takes --- the machine check, the bridge, the half-local movers, the anchors, the movement --- is against Run 32**, by the owner's ruling of 2026-09-16 that Run 33's timings are skewed by filesystem issues, the file-page frame term `hugebin/` now removes; where Run 33's figures are quoted, it is to say which did not reproduce.

**Stage twelve does on `window` what it was registered to do, and elsewhere moves nothing a span can see.** It is stage eleven with the run chosen among tied unit-stride axes by its length, landed at `0d637b7`. On `window` the basis reads it over stage six at **0.8943** and over stage eleven at **0.9188**, inside the 0.90 and 0.92 within 3% that registration (1) set, and each of the three views it moves within a point of stage six --- 0.9926, 0.9996 and 0.9906 --- so (1) HOLDS, the item naming no half and so being read on the basis; within the control half both spans would miss, 0.8529 and 0.9542. (3) HOLDS: stage twelve across the halves on `window` reads **0.9304** against 0.94 within 2.5%, the basis faster, with stage six at 0.8873 and stage eleven at 0.9664 beside it. (2) HOLDS on every span: stage twelve over stage eleven sits within 0.61 of a point of level on the main set and on the nine classes other than `window`, on both halves; its count clause, read by hand off the counts files, holds as a bound --- stage twelve within 73 instructions a call of stage eleven on every tie view on both compilers, and within half a percent of stage six's count on the three views it moves --- and misses as a direction, stage twelve retiring MORE than stage eleven on 20 of the 154 tie-view readings, and that direction KILLS (2), resting on the five of those readings that part by more than the identical-code `sum-only` pair does on their population.

**Two registrations held and three were killed, and every `predict:` span of the five held on the basis half.** (1) and (3) HOLD. **(2) is KILLED by its count clause**: stage twelve retires more instructions than stage eleven on 20 of the 154 tie-view readings, five of them by more than the identical-code `sum-only` pair differs by on that population, which is what makes the direction a reading and not the instrument's resolution, where the item said fewer. **(4) is KILLED**: `runs-48` reads 4.0 to 5.4% under `runs-96` an element on every consumer whose loop is a unit-stride run, on both halves, against the item's 3%, and `runs-32` against `runs-9` splits by half, 3.4 to 5.0% over it on the basis and 2.3 to 3.4% under it on the control, some consumers inside the band there and some not. **(5) is KILLED within the control half, on one shape**: `small-flat64` under stage eleven reads 5.06% over stage seven against a 4% band, where the basis reads 3.94%; its class span holds at 0.9363 and 0.9300, `small-bcast32` holds on both halves, and stage eleven over stage ten sits where Run 32's cells put it on every other population. Both kills set a band on a per-shape reading from one probe process of 2026-09-16 and missed on the sequence by one to two and a half points.

**Against Run 32, each half on its own moved past 3% on four arms over the eleven populations, and none of them is registered or explained.** `--half-movers run34 run32` names `mut-odo-vecdims-add-in-leaf-u1` on `scaled` on the basis, **1.0636** against 1.0063 on the control; both of the shipped leaf's A/A copies on `small` on the control, **0.9662** each against 1.0200 and 1.0226 on the basis; and `lib-stage2-lean` on `rev` on the control, **1.0322** against 1.0029. All four carry their counts level against Run 32, 1.0000 on the first and last and within 0.20 of a point on the leaf's copies, so none is the code, and the tool calls each a term of that half's binary or its file instance. The procedure's COPY TEST, which times each flagged cell on the binary and on a byte-identical copy to tell a file instance from the code, wanted the box quiet again and so was asked for rather than taken, and it was taken after the run on the owner's go: the `scaled` mover is the evening's FILE INSTANCE, that mounted copy of `run34-exit` running its worst cell at a median 1.075 of a second mounted copy's cycles an iteration, all eight readings above all eight, on 2 MiB pages whose frames alone differ; the other three read level with their copies inside what the probe resolves and stay unattributed ([the open list][open]). What is gone is Run 33's largest term: `lib-stage2-lean-u1` on `runs`, **1.2954** across the halves on Run 33 and read then as the basis file's page frame, reads **1.0027** here.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition. **What this run leaves the next one is Run 33's compiler gap gone**: from `hugebin/` and a moved source the same two compilers read an arm geomean of 1.0048, no arm past 3%, the lean fill level and the `runs` arm that read 1.2954 at 1.0027 --- which agrees with the owner's ruling on Run 33 without by itself separating the launch from the source, and leaves the `-O2` pair to Run 35. **What two of the kills teach is about a probe's per-shape reading**: (4) and (5) each set a band on one probe process's reading of a shape, and the consumers that probe timed missed it on the sequence by one to two and a half points, while every `predict:` span of the registration held on the basis half --- so a per-shape band taken off one probe wants that probe's spread beside it.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span**, as Run 33's was, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **What is new in it is the source and the launch**: `Main.hs` at `2496c98`, three commits past Run 33's build, and every process launched from the `hugebin/` mount. **Read against Run 32, which the owner's ruling makes this run's reference, the distance is small and the reference does not move**: over the 16 arms that carry a corrected time and stand in both rosters, this run over Run 32's basis half runs from **0.9952** on `lib-stage2-lean` to **1.0128** on `lib-stage2-lean-u1` --- below 1 meaning this run is the faster --- with `list` itself at **1.0002**; read as a ratio to `list` within each run, which cancels a box term exactly, the other fifteen give a `--bridge` geomean of **1.0030**, none outside the 3.3% drift band Run 11 measured and the widest, `lib-stage2-lean-u1` at 1.0126, inside Run 23's narrower 2.1% as well. That span carries the switch, the shim, five `Main.hs` commits and the launch besides the box. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run34-exit`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-four rows. That the published half is the ghc-9.12.4 one is the re-declaration of 2026-09-15 inherited rather than this run's to make --- 9.12.4 is what a default build takes on this machine and what a cross-run absolute is read against, and HEAD is the candidate reading. **Thirty-three of the thirty-four rows are not first readings**: every one of them has a twin in Run 33's file, and all but `libunord-stage11-sum` in Run 32's. The thirty-fourth, `libunord-stage12-sum`, landed at `0d637b7` --- stage eleven with the run chosen among tied unit-stride axes by its length --- and is read here for the first time.

**Comparing runs?** The table below is Run 34's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **0.51%** from 1 on the basis half or **0.49%** on the control, read over the eight pairs this roster carries, and over the four pairs that carry back to Run 10 at **0.49%** and **0.49%** --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The two halves name DIFFERENT pairs this run**, `mut-odo-vecdims-add-in-leaf-u2-aa-distant` on the basis and `bq-expand-aa-distant` on the control, where Run 33's two named `bq-expand-aa-distant` alike, so on the basis the whole-set figure and the carry-back one part by two hundredths of a point. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **3.77%** on `stretch-bigstride` on the basis and **4.94%** on `vgg-14-c512-k3` on the control --- are not floors at all and are not to be quoted as any. **And its two columns may be differenced on nine of the eleven populations**, `list` having moved 0.06 points on the main set, so a cross-half figure here is a measurement on those nine and an ordering on the two past the bar.

**It is the main set's table**, and every column below is a statistic of that population: each stride class has a table of its own, on the same rows and in the same columns but its own basis, in [The stride classes, run by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.58* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.58 | 69 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage2-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over the port's base-offset table |
| liblist-stage3-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the lazy odometer under the natural-strides dispatch |
| liblist-stage4-list-sum | -- | -- | 0.55 | 70 | 1.00x | the same, base's `sum` over stage four's list -- the fold a library user brings, over the lazy odometer under the lean dispatch |
| liblist-stage4-sum | -- | -- | 0.58 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| libunord-stage1-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage10-list-sum | -- | -- | 0.01 | 83 | 0.00x | the same, base's `sum` over stage ten's list -- the fold a library user brings, over the two reorderings composed |
| libunord-stage10-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's tie-break with stage nine's zero-stride axes moved outermost -- the two reorderings composed |
| libunord-stage11-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage eleven's list --- stage ten with its zero-stride move guarded, so the move fires only where a zero stride is there to move |
| libunord-stage12-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage twelve's list --- stage eleven with the run chosen among tied unit-stride axes by its length |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.40* | *78* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.01* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.02* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage2-lean | 0.025 | 0.113 | 0.59 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| lib-stage2-lean-u1 | 0.025 | 0.110 | 0.62 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.113 | 0.50 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.112* | *0.57* | *69* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.112* | *0.49* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.110 | 0.50 | 69 | 1.00x | new mutating `Vector` method -- the shipped fill's leaf with the bound merged in and the body not unrolled |
| lib-stage1 | 0.029 | 0.113 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| *mut-odo-vecdims-aa* | *0.045* | *0.112* | *0.42* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa-distant* | *0.045* | *0.112* | *0.42* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.045** | 0.112 | 0.43 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| *bq-expand-aa-adjacent* | *0.127* | *0.249* | *0.65* | *50* | *2.78x* | *A/A control* |
| bq-expand | 0.127 | 0.251 | 0.71 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-distant* | *0.128* | *0.249* | *0.41* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.75 | 21 | 25.20x | -- |
| *list-aa-distant* | *1.001* | *1.015* | *0.67* | *21* | *25.20x* | *A/A control* |
| *list-aa-adjacent* | *1.003* | *1.018* | *0.47* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run SIX of the 105 pairs among the fifteen timed arms other than `list` part in SIGN between the two statistics on the basis, seven on the control. Two are the shipped leaf's A/A copies: `mut-odo-vecdims-add-in-leaf-u2-aa` against its base divides to **1.0084** on the published column, saying the adjacent copy is the slower, where the paired figure is **0.9970**, the copy ahead on 15 of 19 shapes; the distant copy does the same, **1.0026** against **0.9949** on 16 of 19, and that paired figure is the basis half's floor. The other four are `lib-stage2-lean-u1` against the leaf, its two copies and `-u1`, the column putting the lean twin ahead of each and the pair behind it --- against the leaf **0.9413** against **1.0420**. **The widest disagreements are on the rows the cap touched most**: `lib-stage2-lean-u1`, five of its cells capped, divides against `mut-odo-vecdims` to 0.5637 on the column where the paired figure is 0.6713, seventeen points apart; at the head of the table, against `lib-stage1` **0.8692** against **0.9888**, twelve, and `lib-stage2-lean` against `lib-stage1` **0.8470** against **0.9395**, nine. Those column ratios are `--pair`'s own `published-column ratio` and not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `lib-stage1` publishes 0.02913 here and 0.02830 on Run 32's basis half, 2.9 points up, where the cross-run paired reading is **1.0035**, a third of a point, and `--compare` flags that row itself. A margin between two arms is `--pair`'s paired figure, which is also the statistic the floor is defined in; the column is for reading the table, not for differencing it, and not for tracking a row across runs either.

**This run's two columns MAY be differenced on nine of the eleven populations**, one more than Run 33 could say. It rests on `list` having moved **0.06 points** on this run's main set, and on `read-all.sh --brief-facts` putting `bcast` (0.9952), `bcastmid` (1.0008), `block` (1.0039), `compose` (1.0037), `flip` (1.0056), `runs` (1.0020), `scaled` (1.0064) and `window` (1.0020) inside the 0.7% bar beside it. TWO are past it: `rev` at 0.9890 and `small` at 1.0098. On those two every arm-by-arm figure across the halves in this file is an ORDERING and not a subtraction, and each says so in its own cross-half line.

`concat-runs` has no row, and neither do the other 86 arms the roster holds and checks without timing --- **87 of its 121** in all, where Run 33 checked 86 of 119: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **One arm was added to the timed roster this run and NONE was parked**, as on Runs 32 and 33. `libunord-stage12-sum`, stage eleven with the run chosen among tied unit-stride axes by its length, landed at `0d637b7` with the untimed `libunord-stage12` beside it; the six parked on 2026-09-13 stay parked, and the thirteen Fill arms over a list that went to `check` on 2026-09-09 stay where they are. So a movement against Run 32's basis column is a movement on the **16 shared arms that carry a corrected time**, with a switch, a shim, a source and a launch term between the two runs and no roster term on those sixteen.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage2-lean` at 0.025**, with `lib-stage2-lean-u1` printing the same 0.025, the shipped leaf and its two A/A copies 0.027, `mut-odo-vecdims-add-in-leaf-u1` 0.028 and `lib-stage1` 0.029 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.045**, every one of them a fill that writes the result, the same five Runs 31 to 33 had. **The column and the pair DISAGREE about the order behind the leader**: paired on the basis, `lib-stage2-lean` over `lib-stage1` is **0.9395** at 14 of 19 and p 0.064, over its own unrolling twin **0.9501** at 15 of 19 and p 0.019, and over the shipped leaf **0.9900** at 11 of 19 and p 0.65, while the twin over the leaf reads **1.0420** --- the pairs putting the leaf second and the twin behind it, where the column prints the twin level with the leader and ahead of the leaf. The disagreement is the winsorizing and not an arm: `lib-stage2-lean-u1`'s published figure is 0.02532 where its plain per-shape geomean is 0.03015, five of its nineteen cells capped. **The third is that the leaf fusion is unmoved by the compiler**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6443** on the basis and **0.6360** on the control, inside the 0.6358 to 0.6525 that ten readings across Runs 29 to 33 spanned.

**The two standing placement controls are still gone with the prune, the straddlers stand at eight on each half, and this pair moves tracked fill copies as Run 33's did.** Within the pair `./loop-offsets.py run34-gheadexit run34-exit` puts the tracked six-copy group at **[0, 0, 0, 8, 4, 0]** on the basis and **[18, 0, 0, 0, 9, 2]** on the control, while the two-copy group reads **[0, 0]** on both; the basis carries 33 self-loops of 28 B in 26 distinct byte-sequences and the control 34 in 27. So a compiler displaces fill copies as an optimisation level does, which is what `--library` says over the whole library too: 136 self-loops in common at **11.0%** the same offset in line. Against the previous build of the basis's own recipe, Run 33's basis binary, `--delta` reads EVERY offset preserved on both groups with no address surviving to the byte, so the source that moved under this run moved every copy and no head's offset; against Run 32's basis binary the six-copy group's offsets move as Run 33 read them move.


## What the next run compares against

**Run 35 is the pair below, declared 2026-09-15 morning and deferred whole by Runs 33 and 34, neither of which withdrew it: the two `-O2` passes against neither, on ghc-9.12.4, one variable and nothing else, and `Run 35` in it names the run that takes it.** The basis half is the dead-spot form at plain `-O1`, `nospec` naming what that half is, and the other is that same recipe with `-fspec-constr` and `-fliberate-case` added by hand, `twopass`, so that `--compare` reads nospec over twopass and every `cross` is what the two passes together do to one arm. One source, one shim, one shim environment, one roster, one shape set, one class list and one bench order, with the two command lines differing in two flags on one of them. **The one thing the executing session has to settle first is still the shim environment**: the declaration predates `LOOP_EXITSPAN=1`, which the published basis has carried since Run 33, both halves must carry the same answer, and which answer is taken decides only which basis Run 35's absolutes are read against. What the pair answers, and what a `cross` reading of it costs, is the registration's to state before it runs. The recipes, spelled out as a pair note wants them, with the exit span shown on both lines and to be dropped from both if the owner so decides:

    run35-nospec      cd here, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --builddir=db-r35a \
                          --ghc-options="-fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --builddir=db-r35a) run35-nospec
                        rm -rf db-r35a
    run35-twopass     the same source, then
                        LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1 \
                        cabal build micro --builddir=db-r35b \
                          --ghc-options="-fspec-constr -fliberate-case -fobject-determinism" \
                          --ghc-options="-pgma $PWD/align-as.py -fforce-recomp"
                      then
                        cp $(cabal list-bin micro --builddir=db-r35b) run35-twopass
                        rm -rf db-r35b

`LOOP_MAXSKIP` and `LOOP_LOOKTHROUGH` are inert under the dead-spot form and stay on both lines so that the lines differ in the regime flags alone; `LOOP_ENTRIES`, `LOOP_BLOCKRULES`, `LOOP_PIN` and `LOOP_TRACE` are unset on both. Every build wants `-fforce-recomp` and a fresh `--builddir`, the switches being an environment change cabal does not see, and every driver takes its half from `hugebin/` through `half-bin.sh`, as this run's did. Under the exit span `loop-offsets.py --survey` reads 0 exit spans astride off a timed binary, as it did on both of this run's halves, so the preparation's legs 10a and 10b stop on anything else. **It is the pair Run 31's arithmetic wanted and no run since could supply.** Run 31 read `-O2` worth **1.2974** on `list` where `-fspec-constr` and `-fliberate-case`, measured one at a time on Runs 29 and 30, multiply to 1.3325 --- a 2.7-point overshoot that is either the level's other passes handing `list` back or an artefact of composing two runs' readings, and a pair with both passes on one half and neither on the other is the only thing here that tells them apart. **And what this run changes about the case for it is that the compiler question at plain -O1 is close to spent again.** Run 33 read HEAD against 9.12.4 at an arm geomean of 1.0068 with the lean fill parting by 3.54 points, which the owner then ruled skewed by filesystem issues; asked again from `hugebin/`, the same two compilers on a moved source read **1.0048**, the lean fill at **1.0047** and no arm past 3%, the widest `lib-stage1` at 1.0258 with its counts 0.75 of a point apart. So the gap Run 33 read on its fill arms did not survive the move to `hugebin/` and three `Main.hs` commits, which agrees with the owner's ruling and does not by itself separate the launch from the source, and the `-O2` pair is what is left waiting.

**The COMPILER variable has now been asked NINE times, and this run is the third to ask it at the level the library ships and the second under the exit span.** Runs 19 and 24 to 28 all varied it with `-fspec-constr` on BOTH halves: Run 24 read the two 5.7% and 6.8% apart on the instructions of two pure arms; Run 25 read `list` 1.10% apart in time and 0.33% in counts; Run 26 found twenty-four of twenty-six arms inside a percent in counts and the two `Ptr` arms outside at 0.6219 and 0.9295, which was GHC [#27778](https://gitlab.haskell.org/ghc/ghc/-/work_items/27778); Run 27 worked it around and read every arm inside a percent; Run 28 confirmed it at a counted geomean of 1.0027. **Run 32 asked it at plain -O1 and got the cleanest null of them all, Run 33 asked it under the exit span and read a gap, and this run asks Run 33's question from `hugebin/` and reads close to Run 32's null again.** Run 32's arm geomean was 0.9985 with no arm past 3% and three of eight strategies clearing its A/A bar; Run 33's was 1.0068, one arm past 3% and eight of eight past a 0.16-point bar; this run's is **1.0048**, no arm past 3% and six of eight strategies past a bar of **0.23** points, the widest `lib-stage1` at 1.0258. The three runs share both compilers to the day; Runs 33 and 34 share the recipe and differ in three `Main.hs` commits and the launch, so what parts them is the source or the file instance, and nothing in either pair separates the two. **The REGIME variable, meanwhile, has been asked three times and the arithmetic it left is still open.** Put in one orientation --- the unflagged half over the flagged --- Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**; on `bq-expand` the two passes MULTIPLY to 1.2967 against a measured 1.2943, 0.19% apart, while on `list` they multiply to 1.3325 against 1.2974, 2.7% apart. That arithmetic is an observation and not a subtraction, and Run 35's pair is what settles it.

**What Run 34 leaves the next run to read against, and the first item is a check that did NOT fire. The box is where Runs 28 to 33 left it**, and this run's gate says so: read against the fingerprint Run 32 installed, by the owner's ruling, the machine check puts `list`'s net at **+0.18%**, worst `stretch-primes` at +1.94%, 0 of 19 shapes past 5% and the geomean inside the 3% bar. **That reading is NOT like-for-like**, Run 32's published half being this basis less `LOOP_EXITSPAN=1`, on the older shim, five `Main.hs` commits back and launched from disk. Against `run32-nospec` itself the sixteen shared timed arms span **0.9952 to 1.0128** with `list` at **1.0002**, and the fifteen that are not `list` give a `--bridge` geomean of **1.0030**, none outside the 3.3% drift band Run 11 measured and none outside Run 23's narrower 2.1% either. So this run publishes INSIDE the third machine era rather than opening a fourth, and the fingerprint below is this run's own, which the next run's machine check reads. **What a Run 35 reading must not take from those sixteen arms is a box figure**: the switch, the shim, the source and the launch all moved between the two builds, so their spread is theirs and the box's together and nothing here separates them. Only a pair whose halves share a source, a shim and a launch does that, which is what every pair here is for.

**Registered with the pair.** Run 34's five registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. TWO held and THREE were killed. **What a next registration should take from this one is that a band set on one probe's per-shape reading wants that probe's spread beside it**: (4) and (5) both centred a per-shape clause on one probe process of 2026-09-16, and the consumers that probe timed missed on the sequence by one to two and a half points, while every `predict:` span of the five held on the basis half. And a clause resting on the direction of a count difference under a hundred instructions wants beside it what the identical-code `sum-only` pair differs by on that population --- fourteen instructions on `window` and 2925 on `runs` on this run's basis.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are edited by hand, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 34**, whose halves were launched from `hugebin/` and whose basis carries `LOOP_EXITSPAN=1`, so a Run 35 basis built without it reads against Run 34 across that switch, as this run read Run 32; the owner's ruling of 2026-09-16 set Run 33's timings aside and not this run's. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it, and walking that chain here is what this section stopped doing. So an older run is read by opening its file, and the one step this run records is Run 32 to Run 34, by that ruling --- **and it is a step between PUBLISHED bases that are NOT the same recipe**, this run carrying `LOOP_EXITSPAN=1` where Run 32's basis did not, so it is a bridge and not a subtraction and carries a switch, a shim, a source and a launch term with it. Over the **16 arms both rosters time and both give a corrected time**, this run over Run 32's basis runs from **0.9952** on `lib-stage2-lean` to **1.0128** on `lib-stage2-lean-u1` --- below 1 meaning this run is the faster --- FIFTEEN of the sixteen inside 1% of 1, with `list` itself at **1.0002**. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one, and the two differing in ONE COMPILER and in nothing else. Its two columns MAY be differenced, `list` having moved 0.06 points between them.
| strategy | Run 34 (plain -O1, dead-spot, exit span, -A32m, 9.12.4) | Run 34 (plain -O1, dead-spot, exit span, -A32m, GHC HEAD) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.045** | 0.045 |
| `mut-odo-vecdims-add-in-leaf-u1` | **0.028** | 0.027 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.027** | 0.026 |
| `lib-stage1` | **0.029** | 0.027 |
| `lib-stage2-lean` | **0.025** | 0.023 |
| `lib-stage2-lean-u1` | **0.025** | 0.025 |
| `bq-expand` | **0.127** | 0.128 |

**READ THE SECOND COLUMN AS A RATIO AND NOT AS A SPEED.** Every entry is that arm's net over `list`'s net in ITS OWN half, and `list` moved 0.06 points between the halves --- so a control entry reading lower is very nearly the arm and not the denominator, which is what an unmoved reference buys. **That is still not an identity**: each entry is winsorized per row within its own half, so dividing an arm's two entries does not reproduce its `--compare` figure and is not meant to --- on `lib-stage2-lean` the two unrounded entries, 0.02468 and 0.02321, divide to about 1.063 where the cross reads 1.0047, which is the capping and not a disagreement, each half capping four of that row's nineteen cells. The arm-by-arm reading of what the compiler is worth is in the head, off `--compare`, where the reference is not divided out.

**A published geomean is over the same 19 shapes, and two halves of one run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered. **THE TABLE ABOVE IS SUCH A PAIR**, `list` having moved **0.06 points** on this run's main set. **Its two columns print within two thousandths of each other on every row** --- `lib-stage2-lean` 0.025 against 0.023, `lib-stage1` 0.029 against 0.027, `mut-odo-vecdims-add-in-leaf-u1` 0.028 against 0.027, the shipped leaf 0.027 against 0.026 and `bq-expand` 0.127 against 0.128, with `mut-odo-vecdims` at 0.045 and `lib-stage2-lean-u1` at 0.025 on both --- and read down a column the head and the foot are the same on both, `lib-stage2-lean` leading each and `bq-expand` at the foot of each. **Those gaps are the winsorizing more than the arms**: `lib-stage2-lean`'s plain per-shape geomeans are 0.02865 and 0.02854, 0.39 of a point apart where the published figures part by six.

**The control half's own standings on the arms this run's roster carries, which no table here holds, every published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `-u1` **0.9580** (0.9619) and against `mut-odo-vecdims` **0.6360** (0.6443); `lib-stage1` against `-u2` **1.0404** (1.0538); `lib-stage2-lean` against `-u2` **0.9980** at 16 of 19 (0.9900 at 11 of 19) and against `lib-stage1` **0.9592** at 15 of 19 (0.9395 at 14 of 19). **All five hold their direction across the halves**, where Run 33's lean fill changed sides against the leaf: the lean fill is ahead of the shipped leaf under both compilers, by a point on the basis and a fifth of one on the control, the second inside that half's floor, eleven and sixteen shapes of nineteen favouring it. Not every ordering holds across the halves: `mut-odo-vecdims-add-in-leaf-u1` against `lib-stage1` reads 0.9865 on the basis and 1.0032 on the control, the second inside that half's floor, `bcastmid` names a different leader outside the family on each half, and property 1's `stretch-pow2stride` cell changes sides.

**Each stride class has its own table below.** Run 8 re-ran every class with the populations pinned, and every run since has again, so each class's paragraph carries what the last change moved and the table above it is what the next run reads against. **A class figure compared across the Run 11/Run 12 boundary is not compared on one build**: Run 11's class tables are its *aligned* half's and Run 12's its *max-skip* basis half's, and the main set prices that difference at nothing below 0.99 and up to 1.06, so a point or two of movement across that boundary is the shim rather than the class. From Run 13 on, every run's class tables are its own basis half's, Run 34's included.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.4 us | 0.077 | `lib-stage2-lean` 0.075 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.72 us | 0.087 | `lib-stage2-lean` 0.070 | `mut-odo-vecdims-add-in-leaf-u2` 0.068 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 120 us | 0.063 | `lib-stage2-lean` 0.032 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 389 us | 0.043 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `gather48-src-50` | 3 | 22500 | 458 us | 0.048 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.11 ms | 0.030 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.74 ms | 0.052 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `stretch-primes` | 89 | 250357 | 4.35 ms | 0.026 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17.1 ms | 0.039 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u1` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.9 ms | 0.052 | `lib-stage1` 0.031 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.9 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44 ms | 0.023 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.4 ms | 0.112 | `lib-stage2-lean-u1` 0.110 | `mut-odo-vecdims-add-in-leaf-u1` 0.110 |
| `stretch-r5-8x432` | 8 | 1769472 | 48.4 ms | 0.021 | `lib-stage1` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 30.9 ms | 0.088 | `lib-stage2-lean` 0.077 | `mut-odo-vecdims-add-in-leaf-u2` 0.078 |
| `stretch-bigstride` | 3 | 1800000 | 50.6 ms | 0.033 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 39.8 ms | 0.058 | `lib-stage2-lean-u1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 40.7 ms | 0.021 | `lib-stage1` 0.021 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.5 ms | 0.057 | `lib-stage1` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 944 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.2 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.5 ms | 0.020 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.2 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35.6 ms | 0.016 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.4 ms | 0.057 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.66 ms | 0.053 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.25 ms | 0.019 | `lib-stage1` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 48.1 ms | 0.034 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.1 ms | 0.022 | `lib-stage1` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.25 ms | 0.019 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.26 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.26 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-page` | `block` | 64 | 131072 | 2.36 ms | 0.028 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.49 ms | 0.020 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 946 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 945 us | 0.028 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.013 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.3 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 29.8 ms | 0.022 | `lib-stage2-lean-u1` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.35 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.71 ms | 0.052 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.7 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 30 ms | 0.025 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.7 ms | 0.048 | `lib-stage1` 0.043 | `mut-odo-vecdims-add-in-leaf-u2` 0.036 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 121 us | 0.065 | `lib-stage2-lean` 0.032 | `mut-odo-vecdims-add-in-leaf-u2` 0.043 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 460 us | 0.048 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.38 ms | 0.025 | `lib-stage1` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `runs-65536` | `runs` | 65536 | 1769472 | 28.1 ms | 0.024 | `lib-stage1` 0.022 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.4 ms | 0.030 | `lib-stage1` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.6 ms | 0.025 | `lib-stage1` 0.024 | `mut-odo-vecdims` 0.025 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.6 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-512` | `runs` | 512 | 1799680 | 28.8 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-256` | `runs` | 256 | 1799936 | 29 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 33 ms | 0.032 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-2` | `runs` | 2 | 1800000 | 39.8 ms | 0.057 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 36 ms | 0.047 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-32` | `runs` | 32 | 1800000 | 30 ms | 0.025 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 34.3 ms | 0.040 | `lib-stage2-lean-u1` 0.023 | `mut-odo-vecdims-add-in-leaf-u1` 0.023 |
| `runs-48` | `runs` | 48 | 1800000 | 29.5 ms | 0.026 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 33.2 ms | 0.038 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.5 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 32 ms | 0.030 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `runs-96` | `runs` | 96 | 1800000 | 29.2 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29.7 ms | 0.026 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `scaled-r5` | `scaled` | 13 | 15015 | 271 us | 0.029 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.05 ms | 0.023 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.19 ms | 0.028 | `lib-stage2-lean-u1` 0.030 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.97 us | 0.076 | `lib-stage2-lean` 0.097 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-bcast32` | `small` | 32 | 256 | 4.5 us | 0.050 | `lib-stage1` 0.064 | `mut-odo-vecdims-add-in-leaf-u2` 0.044 |
| `small-flat64` | `small` | 64 | 256 | 4.48 us | 0.059 | `lib-stage2-lean-u1` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.057 |
| `small-patch-r5` | `small` | 4 | 256 | 5.37 us | 0.087 | `lib-stage2-lean-u1` 0.097 | `mut-odo-vecdims-add-in-leaf-u1` 0.068 |
| `small-row96` | `small` | 96 | 384 | 6.62 us | 0.041 | `lib-stage2-lean` 0.054 | `mut-odo-vecdims-add-in-leaf-u2` 0.040 |
| `window-28x28-k5` | `window` | 5 | 14400 | 283 us | 0.041 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 967 us | 0.084 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.46 ms | 0.051 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 10.2 ms | 0.048 | `lib-stage2-lean` 0.028 | `mut-odo-vecdims-add-in-leaf-u1` 0.027 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.91 ms | 0.050 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.029 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.8 ms | 0.051 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u1` 0.029 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.6 ms | 0.052 | `lib-stage2-lean` 0.032 | `mut-odo-vecdims-add-in-leaf-u1` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.9 ms | 0.031 | `lib-stage1` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-four rows is a geomean over fewer shapes than the rest, as on Runs 32 and 33 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the FOURTEEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers, `libunord-stage12-sum` being the fourteenth and landing this run --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names `lib-stage2-lean` on SEVEN, `lib-stage1` on two --- `rev` and `scaled` --- and `lib-stage2-lean-u1` on one, `bcastmid`, where Run 33 named the lean fill on eight. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 34's verdicts** over ten classes, the details beside each class's table:

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **The first held in every one of the eleven populations on both halves; the second held in all ten classes on both halves and PARTED BETWEEN THE HALVES on the main set again, with the halves exchanged.** On the MAIN SET `mut-odo-vecdims` is ahead of `bq-expand` on `stretch-pow2stride` at **0.9989** on the basis and BEHIND at **1.0016** on the control, each margin inside its half's floor, and `./read-run.py --series mut-odo-vecdims bq-expand stretch-pow2stride` prints every earlier run's reading beside its own; whether a run reads the fill behind by more than its half's floor there is [the open list][open]'s question. The `worst` clause holds in every regime, roster, compiler and layout the README has run, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population. The `bq-expand` clause folded in on 2026-09-06 from the ordering that was property 2 until then, strengthened from a geomean to every shape, and is read that way here for the seventh time.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm now breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` carries a `worst` of **1.105** on `runs` on the basis and **1.091** on the control, and one cell does it on each: `runs-2`, at those same two figures, the halves parting by a point and a half where Run 33's parted by five. Over every timed arm outside the controls and the reducing consumers, on all eleven populations and both halves, no other cell reads above 1. `gen-unsafe` and its twins carried a `worst` above 1 in seven of ten populations and were the baseline's own controls rather than the property failing; every one of them is parked. Of the five library-shaped arms Run 27 found breaking it at `runs-2` --- `libunord-stage1` 1.237, `liblist-stage1` 1.214, `lib-stage1` 1.198, `liblist-stage2` 1.078 and `libunord-stage2` 1.076 --- four are retired to `check` and are not timed here. Those five figures are RECOMPUTED from Run 27's own cells, that run's prose and its own installed table having printed different ones, and the five are FIVE of NINE library-shaped arms over `list` there rather than the largest five.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the fourth run running that this property is the one left entirely alone.** The `list` clause is closest at `small-patch-k5`, 0.05918, and every closest shape outside `small` sits under 0.048. The `bq-expand` clause is closest at `scaled-rank1-m1`, 1.00003, then `stretch-tall-Mx2` on the main set at 1.00000, `bcast-src8` at 0.99999 and `runs-65536` at 0.99994 --- inside the margin the strict form would have failed on, which is why the margin is there and why it is not widened further.

3. **The allocation tiers survive, their ORDER is unbroken in all ten classes and on the main set, and their LEVELS are again identical on the two halves cell for cell; what `small` is outside is the LEVEL clause and not the order one**, by the ruling of 2026-09-07, it being the class built to break it and read here for what it shows: the mutable fills at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 20.99x to 27.66x. On the main set the fills read 1.00x, `bq-expand` **2.78x** and `list` **25.20x**, a plain -O1 half's levels as Runs 30 to 33's were --- **and the control half reads the same 2.78x and 25.20x, and the same triple in every one of the ten classes**, `small`'s 1.27x family included. No registration of this run names allocation; the reading is taken anyway because it is free and because it is what would show a compiler changing what an arm allocates rather than how fast it runs. It shows none: `--alloc` puts 462 of the 608 allocating cells inside 1e-4 between the halves, worst 2.18e-02 on `stretch-tall-Mx2/libunord-stage11-sum`, with the 38 cells under 100 bytes a call set aside as a property of fitting a near-zero allocation.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 34 (GHC HEAD against ghc-9.12.4, both at plain -O1, dead-spot, exit span, -A32m, launched from `hugebin/`) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 0.08 of a point on `bcastmid` at narrowest and 1.10 on `rev` at widest, so EIGHT of the ten classes sit INSIDE the 0.7% that lets two columns be differenced and their cross-half readings are readings of the pair's variable rather than orderings; the two past the bar are `rev` at 0.9890 and `small` at 1.0098. Over the ten classes the reader counts **160 arm-comparisons, 63 putting the basis faster and 97 slower**, with no degenerate arm excluded, at geomeans from **0.9921** on `bcast` to **1.0116** on `scaled` and extremes of `lib-stage2-lean-u1` at 0.9821 on `rev` and `mut-odo-vecdims-add-in-leaf-u1` at 1.0884 on `scaled`, their counts at 1.0071 and 1.0007, so neither extreme is code; the low extreme is that lean arm in 3 of the 10. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **Two items read nearly every class** --- (2)'s span every class but `window`, its count clause every population, and the last clause of (5) every class but `small`, whose own clauses (5) reads instead --- so each block below carries what applies to it; (1) and (3) name `window` alone and (4) `runs`.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table; *best outside family* is the leading arm outside the vecdims family, what the dropped stride-conditioned redirect would have taken, and *ceiling* the leading arm OF the family, each with its name --- and both are read over the POPULATION, so the arm named here may lead on no single shape and the per-shape fingerprint below may name another, which is [the README's per-shape section][pershape]'s own point and not a disagreement --- since which arm leads is half of what the column says --- so where an arm outside the family leads, the two name different arms and the gap between them is what the lead is worth, and Run 21's table, which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong to; *floor* is the largest deviation from 1 among that process's A/A controls. A cell that breaks property 1, or that leads `mut-odo-vecdims` --- what broke the ordering that was property 2 until 2026-09-06 ([the properties](#the-properties-the-next-run-should-test)) --- is bolded. **In practice that marks the FASTER of the two named arms, one cell a row**: the arm outside the family on FIVE of the ten --- `rev`, where `lib-stage1` leads, `bcast`, `window` and `flip`, where `lib-stage2-lean` does, and `bcastmid`, where its unrolling twin does --- and the family's own ceiling on the other FIVE, `scaled`, `runs`, `block`, `small` and `compose`, where the ceiling is faster. **The two pointer leaves held five of Run 30's six bolded ceilings and are parked**, so every bolded ceiling here is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` itself, which is the form the family would ship. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.043 | 0.065 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 | 0.47% |
| `bcast` | 6 | 0.022 | 0.057 | **`lib-stage2-lean`** 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 0.85% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage2-lean-u1`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 0.55% |
| `window` | 8 | 0.050 | 0.084 | **`lib-stage2-lean`** 0.027 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 1.04% |
| `scaled` | 3 | 0.028 | 0.029 | `lib-stage1` 0.023 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.022 | 0.89% |
| `runs` | 17 | 0.027 | 0.057 | `lib-stage2-lean` 0.024 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.024 | 3.48% |
| `flip` | 6 | 0.028 | 0.052 | **`lib-stage2-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.026 | 3.35% |
| `block` | 5 | 0.023 | 0.028 | `lib-stage2-lean` 0.021 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.021 | 0.23% |
| `small` | 5 | 0.060 | 0.087 | `lib-stage2-lean` 0.055 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.052 | 0.73% |
| `compose` | 4 | 0.024 | 0.028 | `lib-stage2-lean` 0.015 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.015 | 0.44% |

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` in every one of the ten --- the lead that broke the ordering property 2 carried until 2026-09-06. **On FIVE rows --- `scaled`, `runs`, `block`, `small` and `compose` --- the bold sits in the CEILING column instead**, and it names ONE arm on all five, the shipped leaf `mut-odo-vecdims-add-in-leaf-u2`; against Run 33, `scaled` moved into that set and `window` out of it, and `bcastmid` names the lean fill's unrolling twin outside the family. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **FOUR rows tie at three decimals** --- `window` at 0.027, `runs` at 0.024, `block` at 0.021 and `compose` at 0.015 --- and the bold on each is `--block`'s own, computed on the unrounded values where the printed ones cannot separate: outside the family against the ceiling, 0.027028 against 0.027079, 0.024381 against 0.024323, 0.021420 against 0.021167 and 0.014749 against 0.014555, so `window` falls to the arm outside the family and the other three to the ceiling.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.14* | *126* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.11 | 147 | 1.01x |
| liblist-stage2-sum | -- | -- | 0.07 | 147 | 1.01x |
| liblist-stage3-sum | -- | -- | 0.07 | 147 | 1.01x |
| liblist-stage4-list-sum | -- | -- | 0.09 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.10 | 147 | 1.01x |
| libunord-stage1-sum | -- | -- | 0.07 | 146 | 1.03x |
| libunord-stage10-list-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage10-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage11-sum | -- | -- | 0.05 | 157 | 0.01x |
| libunord-stage12-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.04 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage1 | 0.021 | 0.047 | 0.08 | 146 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.043 | 0.06 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.042* | *0.08* | *147* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.042* | *0.08* | *147* | *1.00x* |
| lib-stage2-lean | 0.023 | 0.032 | 0.11 | 147 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.044 | 0.10 | 146 | 1.00x |
| lib-stage2-lean-u1 | 0.027 | 0.039 | 0.14 | 146 | 1.01x |
| *mut-odo-vecdims-aa-distant* | *0.043* | *0.065* | *0.09* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.043* | *0.065* | *0.08* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.043** | 0.065 | 0.14 | 138 | 1.00x |
| *bq-expand-aa-distant* | *0.138* | *0.232* | *0.12* | *122* | *3.22x* |
| *bq-expand-aa-adjacent* | *0.138* | *0.232* | *0.10* | *122* | *3.22x* |
| bq-expand | 0.138 | 0.233 | 0.14 | 122 | 3.22x |
| *list-aa-distant* | *0.998* | *1.001* | *0.21* | *85* | *26.11x* |
| *list-aa-adjacent* | *0.999* | *1.000* | *0.26* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.32 | 85 | 26.11x |

**Controls:** The largest A/A pair is `mut-odo-vecdims-aa-distant` at 0.9953, worst cell 0.73% on `rev-gather48-src-50`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9998 on a worst cell of 0.05% on `rev-cnn-L1-24x24-c1`, its interval covering 1. The in-situ term reads 1.0050, 1.0217 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9973, which the correction amplifies by 1.70x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m51s, peak 95 MiB in use, 25 MiB max residency; the reader reads 34 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.53 ms per call raw, 4.38 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.065/0.048/0.025

**Across the halves:** 8 of the 16 arms are faster on this half and 8 slower, at a geomean of 1.0019, from `lib-stage2-lean-u1` at 0.9821 to `lib-stage1` at 1.0462, with `list` itself at 0.9890. **The baseline moved 1.10% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.065, tiers at 1.00x, 3.22x and 26.11x, identical on the control --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.6413 over 3 of 3 shapes at sign p 0.25, a margin of 35.87% against this class's 0.47% floor (`mut-odo-vecdims-aa-distant`), a floor the third tightest of the ten. **What is this class's own is the extra pass over the axes, visible here for the seventh run running.** `rev` negates every stride and carries no zero stride and no pair of axes tied on stride, so `zerosOutermost` hands its list back unchanged, `routeUnord10` is `routeUnord7` to the byte, and only the walk over the axes separates the dispatches. **This class is one of the two whose columns may NOT be differenced**, `list` having moved **1.10 points** between the halves, the widest of the ten, so its cross-half line is an ordering. Its counted work reads 1.0066 over the sixteen timed arms, and its widest cross-half figure is `lib-stage1` at 1.0462 against an A/A bar of 0.58 points, five of the eight strategies past that bar. Registration (2) reads stage twelve over stage eleven at 1.0007 and 0.9989, and (5)'s last clause stage eleven over stage ten at 0.9906 and 0.9914 against 0.9891 and 0.9904 off Run 32's cells, read by hand off `--cells` --- both holding on both halves.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it; this run reads the class for stage twelve's tie with stage eleven, at registration (2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.59* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.51 | 62 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.52 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.52 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.52 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.33* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.03* | *69* | *0.00x* |
| lib-stage2-lean | 0.015 | 0.020 | 0.49 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.54* | *62* | *1.00x* |
| lib-stage1 | 0.016 | 0.020 | 0.44 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.39 | 62 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.024 | 0.52 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.020 | 0.42 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.022* | *0.057* | *0.32* | *61* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.022* | *0.057* | *0.32* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.022** | 0.057 | 0.08 | 61 | 1.00x |
| bq-expand | 0.092 | 0.141 | 0.68 | 46 | 1.00x |
| *bq-expand-aa-adjacent* | *0.092* | *0.141* | *0.70* | *46* | *1.00x* |
| *bq-expand-aa-distant* | *0.092* | *0.143* | *0.08* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.11 | 17 | 20.99x |
| *list-aa-distant* | *1.008* | *1.014* | *0.85* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.009* | *1.016* | *0.76* | *17* | *20.99x* |

**Controls:** The largest A/A pair is `list-aa-adjacent` at 1.0085, worst cell 1.59% on `bcast-src8`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.02% on `bcast-src8`, its interval covering 1. The in-situ term reads 1.0241, 1.0110 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0082, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m42s, peak 169 MiB in use, 42 MiB max residency; the reader reads 34 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.6 ms per call raw, 29.5 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.028/0.020/0.057/0.016/0.019/0.019

**Across the halves:** 16 of the 16 arms are faster on this half and 0 slower, at a geomean of 0.9921, from `lib-stage2-lean` at 0.9836 to `bq-expand-aa-distant` at 0.9971, with `list` itself at 0.9952.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.057, tiers at 1.00x, 1.00x and 20.99x, identical on the control --- and `lib-stage2-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6463 over 6 of 6 shapes at sign p 0.031, a margin of 35.37% against this class's 0.85% floor (`list-aa-adjacent`). **What is this class's own is that both routes fill**, an innermost stride of 0 sending the lean dispatch and stage one down the same path, which is why `bq-expand` sits at the fills' own 1.00x tier here and nowhere else. **Its two columns MAY be differenced**, `list` having moved 0.48 of a point, and this is the one class where the basis is faster on every arm: all sixteen, at a class geomean of **0.9921**, the lowest of the ten, with seven of the eight strategies past an A/A bar of 0.54 points. **None of it is instructions**: the counted work is level at 1.0024 over the sixteen and at 1.0000 or 1.0001 on every fill arm, so `time/counts` runs 0.984 to 0.995 on the fills. Registration (2) reads stage twelve over stage eleven at 1.0005 and 1.0001, and (5)'s last clause stage eleven over stage ten at 0.9993 and 1.0001 against the 1.0000 Run 32's cells give, read by hand off `--cells` --- both holding on both halves.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.43* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.37 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.35 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.39 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.42 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.35 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.36 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.34 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.30 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 96 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.40* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *88* | *0.00x* |
| lib-stage2-lean-u1 | 0.012 | 0.018 | 0.38 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.35 | 82 | 1.00x |
| lib-stage2-lean | 0.012 | 0.018 | 0.31 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.30 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.43* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.031* | *0.27* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.023 | 0.030 | 0.41 | 78 | 1.00x |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.28 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.27* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.29* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.099* | *0.181* | *0.44* | *61* | *1.92x* |
| bq-expand | 0.099 | 0.181 | 0.42 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.181* | *0.41* | *61* | *1.92x* |
| *list-aa-adjacent* | *0.997* | *0.999* | *0.86* | *28* | *23.56x* |
| *list-aa-distant* | *0.997* | *1.005* | *0.84* | *28* | *23.56x* |
| list (baseline) | 1.000 | 1.000 | 0.83 | 28 | 23.56x |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0055, worst cell 1.98% on `bcastmid-b200k`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.04% on `bcastmid-b200k`, its interval covering 1. The in-situ term reads 1.0170, 1.0791 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0045, which the correction amplifies by 1.29x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h11m51s, peak 129 MiB in use, 35 MiB max residency; the reader reads 34 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 49.2 ms per call raw, 48.1 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0018, from `lib-stage2-lean-u1` at 0.9905 to `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0113, with `list` itself at 1.0008.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.053, tiers at 1.00x, 1.92x and 23.56x, identical on the control --- and `lib-stage2-lean-u1` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4211 over 4 of 4 shapes at sign p 0.12, a margin of 57.89% against this class's 0.55% floor (`bq-expand-aa-distant`), the widest margin of the ten. **THE HALVES NAME DIFFERENT LEADERS OUTSIDE THE FAMILY HERE**, the unrolling twin on the basis and `lib-stage2-lean` itself on the control, both printing 0.012 --- the one class where the two named arms differ. **Its two columns MAY be differenced**, `list` having moved 0.08 of a point, the narrowest of the ten, and the class sits close to level at a cross-half geomean of **1.0018**, four of the eight strategies past a 0.72-point A/A bar and the widest arm, the shipped leaf's distant copy at 1.0113, carrying 0.44 of a point in counts. The counted work over the sixteen reads 1.0037. Registration (2) reads stage twelve over stage eleven at 1.0005 and 1.0003, and (5)'s last clause stage eleven over stage ten at 0.9998 and 1.0007 against the 1.0000 Run 32's cells give, read by hand off `--cells` --- both holding on both halves.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.38* | *62* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.17 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.19 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.18 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.17 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.05 | 102 | 0.03x |
| libunord-stage10-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage11-sum | -- | -- | 0.05 | 102 | 0.03x |
| libunord-stage12-sum | -- | -- | 0.08 | 103 | 0.03x |
| libunord-stage6-loop-sum | -- | -- | 1.73 | 90 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.10 | 101 | 0.03x |
| libunord-stage7-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage9-sum | -- | -- | 0.12 | 101 | 0.03x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *97* | *0.00x* |
| lib-stage2-lean | 0.027 | 0.032 | 0.19 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.031* | *0.18* | *82* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.031* | *0.20* | *82* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.031 | 0.17 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.031 | 0.17 | 82 | 1.00x |
| lib-stage2-lean-u1 | 0.028 | 0.032 | 0.18 | 82 | 1.00x |
| lib-stage1 | 0.028 | 0.032 | 0.17 | 82 | 1.00x |
| **mut-odo-vecdims** | **0.050** | 0.084 | 0.15 | 76 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.050* | *0.084* | *0.15* | *76* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.050* | *0.084* | *0.15* | *76* | *1.00x* |
| *bq-expand-aa-distant* | *0.170* | *0.214* | *0.28* | *57* | *3.86x* |
| bq-expand | 0.171 | 0.211 | 0.33 | 57 | 3.86x |
| *bq-expand-aa-adjacent* | *0.172* | *0.212* | *0.37* | *57* | *3.86x* |
| *list-aa-distant* | *0.993* | *1.006* | *0.44* | *30* | *27.66x* |
| *list-aa-adjacent* | *1.000* | *1.006* | *0.42* | *30* | *27.66x* |
| list (baseline) | 1.000 | 1.000 | 0.55 | 30 | 27.66x |

**Controls:** The largest A/A pair is `list-aa-distant` at 0.9896, worst cell 5.24% on `window-224x224-k3-d2`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 0.9995 on a worst cell of 0.51% on `window-32x32-c64-k3`, its interval covering 1. The in-situ term reads 1.0030, 1.1604 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9898, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h23m32s, peak 126 MiB in use, 51 MiB max residency; the reader reads 34 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.3 ms per call raw, 13.9 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.041/0.050/0.084/0.031/0.051/0.048/0.052/0.051

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0105, from `mut-odo-vecdims` at 0.9934 to `lib-stage1` at 1.0593, with `list` itself at 1.0020.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.084, the second highest of the ten behind `small`'s, and tiers at 1.00x, 3.86x and 27.66x, identical on the control --- and the best arm outside the family and the family's ceiling TIE at 0.027, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the lean fill on the unrounded figures. The lean fill is priced against `mut-odo-vecdims` at 0.4832 over 8 of 8 shapes at sign p 0.0078, a margin of 51.68% against this class's 1.04% floor (`list-aa-distant`). **What is this class's own is stage twelve, and three registrations are read on it.** (1) holds on the basis --- stage twelve over stage six at **0.8943** and over stage eleven at **0.9188**, the three moved views within a point of stage six --- the control half, which the item does not name, reading 0.8529 and 0.9542; (3) holds, stage twelve across the halves at **0.9304** against its 0.94 within 2.5%, with stage six at 0.8873 and stage eleven at 0.9664 beside it; and (5)'s last clause holds, stage eleven over stage ten at 0.9978 and 0.9969 against 0.9979 and 0.9974 off Run 32's cells. (2)'s span does not read this class; its count clause does, the five views stage twelve leaves alone and the three it moves. **Its two columns MAY be differenced**, `list` having moved 0.20 of a point, and the cross-half geomean is **1.0105**, from `mut-odo-vecdims` at 0.9934 to `lib-stage1` at 1.0593, four of the eight strategies past a 0.77-point A/A bar, with the counted work at 1.0098, the widest of the eleven populations --- `lib-stage1` and `lib-stage2-lean` executing 1.76 and 1.56 points more on the basis, about a third of their 5.93 and 4.98 in time.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.09* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.14 | 128 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.15 | 127 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.12 | 127 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.15 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.21 | 127 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 127 | 1.01x |
| libunord-stage10-list-sum | -- | -- | 0.14 | 127 | 1.00x |
| libunord-stage10-sum | -- | -- | 0.15 | 127 | 1.00x |
| libunord-stage11-sum | -- | -- | 0.19 | 127 | 1.00x |
| libunord-stage12-sum | -- | -- | 0.13 | 127 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.11 | 127 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.13 | 127 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.11 | 127 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.15 | 127 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.12* | *146* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.030* | *0.14* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.030 | 0.11 | 128 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.022* | *0.030* | *0.11* | *128* | *1.00x* |
| lib-stage1 | 0.023 | 0.030 | 0.17 | 127 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.023 | 0.036 | 0.12 | 127 | 1.00x |
| lib-stage2-lean | 0.023 | 0.030 | 0.14 | 127 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.030 | 0.15 | 127 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.029* | *0.07* | *127* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.029 | 0.17 | 127 | 1.00x |
| *mut-odo-vecdims-aa* | *0.028* | *0.028* | *0.11* | *127* | *1.00x* |
| *bq-expand-aa-distant* | *0.090* | *0.100* | *0.05* | *111* | *1.21x* |
| *bq-expand-aa-adjacent* | *0.090* | *0.100* | *0.09* | *111* | *1.21x* |
| bq-expand | 0.091 | 0.100 | 0.05 | 111 | 1.21x |
| *list-aa-distant* | *0.999* | *0.999* | *0.21* | *69* | *21.49x* |
| list (baseline) | 1.000 | 1.000 | 0.20 | 69 | 21.49x |
| *list-aa-adjacent* | *1.001* | *1.011* | *0.19* | *69* | *21.49x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9911, worst cell 1.65% on `scaled-super-r3`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0001 on a worst cell of 0.02% on `scaled-super-r3`, its interval covering 1. The in-situ term reads 1.0264, 1.0119 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9965, which the correction amplifies by 2.42x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h8m52s, peak 111 MiB in use, 28 MiB max residency; the reader reads 34 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.37 ms per call raw, 5.19 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.0116, from `bq-expand-aa-adjacent` at 0.9984 to `mut-odo-vecdims-add-in-leaf-u1` at 1.0884, with `list` itself at 1.0064.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.029, and tiers at 1.00x, 1.21x and 21.49x, identical on the control --- and the family's ceiling leads the class at 0.022, `lib-stage1` being the best arm outside it at 0.023 and priced against `mut-odo-vecdims` at 0.9299 over 2 of 3 shapes at sign p 1, a margin of 7.01% against this class's 0.89% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). **What is this class's own is the run's widest cross-half figure**: `mut-odo-vecdims-add-in-leaf-u1` at **1.0884**, the basis slower on all three shapes, from 1.014 to 1.239, carrying the class geomean to **1.0116**, the highest of the ten; six of the eight strategies clear a 0.63-point A/A bar. **None of it is instructions**: that arm's counts read 1.0007, as do the class's over the sixteen, and against Run 32 it is the basis half alone that moved on it, 1.0636 to the control's 1.0063 with counts level on both --- a term the copy test, taken after the run, gives to the evening's mounted copy of the binary, 7.5% raw on `scaled-rank1-m1` against a byte-identical copy on the same mount. **Its two columns MAY be differenced**, `list` having moved 0.64 of a point, where Run 33's could not be. Registration (2) reads stage twelve over stage eleven at 1.0002 and 1.0031, and (5)'s last clause stage eleven over stage ten at 0.9986 and 0.9987 against 1.0003 and 0.9993 off Run 32's cells, read by hand off `--cells` --- both holding on both halves. Its A/A slot on `scaled-super-r3` is the hazard the README's own entry describes and is not read as a figure here.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.48* | *52* | *1.08x* |
| liblist-stage1-sum | -- | -- | 0.10 | 61 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.14 | 69 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.02 | 76 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 74 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 76 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.09 | 61 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.04 | 76 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 76 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.04 | 76 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.07 | 69 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 76 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 76 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.03 | 76 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.13* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.48* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.024 | 0.026 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.024* | *0.026* | *0.13* | *59* | *1.00x* |
| lib-stage2-lean | 0.024 | 0.026 | 0.12 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.025 | 0.027 | 0.12 | 59 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.027 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.057* | *0.10* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.027* | *0.057* | *0.09* | *59* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.057 | 0.10 | 59 | 1.00x |
| bq-expand | 0.093 | 0.141 | 0.45 | 46 | 1.08x |
| *bq-expand-aa-adjacent* | *0.093* | *0.142* | *0.43* | *46* | *1.08x* |
| *bq-expand-aa-distant* | *0.095* | *0.143* | *0.04* | *46* | *1.08x* |
| lib-stage1 | 0.099 | 1.105 | 0.21 | 51 | 1.42x |
| list (baseline) | 1.000 | 1.000 | 2.67 | 17 | 21.30x |
| *list-aa-adjacent* | *1.034* | *1.047* | *0.22* | *17* | *21.30x* |
| *list-aa-distant* | *1.035* | *1.049* | *0.25* | *17* | *21.30x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 1.0348, worst cell 4.94% on `runs-65536`, and 3 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.06% on `runs-96`, its interval covering 1. The in-situ term reads 1.0293, 1.0266 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0336, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h50m1s, peak 644 MiB in use, 289 MiB max residency; the reader reads 34 benchmarks over 17 shapes of the runs class. Anchor: `runs-2`, `list` at 40.9 ms per call raw, 39.8 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.047/0.040/0.038/0.032/0.030/0.025/0.026/0.025/0.025/0.025/0.025/0.025/0.025/0.030/0.024/0.026

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0038, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9983 to `mut-odo-vecdims` at 1.0135, with `list` itself at 1.0020.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.057, tiers at 1.00x, 1.08x and 21.30x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.024, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.8177 over 13 of 17 shapes at sign p 0.049, a margin of 18.23% against this class's **3.48%** floor (`list-aa-distant`), the widest floor of the ten and the reason margins here are read with more room than anywhere else. **What is this class's own this run is the three new views and the registration built on them, which DIES here**: (4) predicted `runs-48` within 3% of `runs-96` an element, and every consumer whose loop is a unit-stride run reads it 4.0 to 5.4% under on both halves (the item's verdict carries the rest). **`lib-stage2-lean-u1`, which carried Run 33's 1.2954 on this class, reads 1.0027**, its counted work at 1.0000. **Its two columns MAY be differenced**, `list` having moved 0.20 of a point, and the class sits close to level: a cross-half geomean of **1.0038**, three of the eight strategies past a 0.28-point A/A bar, the counted work at 1.0023. Registration (2) reads stage twelve over stage eleven at 1.0001 and 0.9998, and (5)'s last clause stage eleven over stage ten at 0.9998 and 1.0007 against 1.0000 and 1.0001 off Run 32's cells over the fourteen views both runs carry --- both holding on both halves.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.40* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.12 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.13 | 88 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.12 | 92 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.07 | 92 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.10 | 92 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.03 | 98 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.05 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *90* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.023 | 0.043 | 0.28 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.046 | 0.31 | 83 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.026 | 0.036 | 0.14 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.026* | *0.043* | *0.10* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.043* | *0.32* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.046 | 0.22 | 80 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.028* | *0.052* | *0.11* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.028* | *0.052* | *0.13* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.028** | 0.052 | 0.10 | 77 | 1.00x |
| lib-stage1 | 0.034 | 0.048 | 0.24 | 80 | 1.00x |
| bq-expand | 0.091 | 0.179 | 0.44 | 61 | 1.05x |
| *bq-expand-aa-adjacent* | *0.091* | *0.179* | *0.44* | *61* | *1.05x* |
| *bq-expand-aa-distant* | *0.091* | *0.180* | *0.11* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.72 | 31 | 21.18x |
| *list-aa-distant* | *1.006* | *1.019* | *0.53* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.009* | *1.021* | *0.27* | *31* | *21.18x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 1.0335, worst cell 22.29% on `flip-last-rows`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.52% on `flip-fwd-rows96`, its interval covering 1. The in-situ term reads 1.0233, 1.0232 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0180, which the correction amplifies by 2.24x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h17m41s, peak 209 MiB in use, 76 MiB max residency; the reader reads 34 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31 ms per call raw, 30 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.025/0.024/0.052/0.048/0.026/0.026

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0036, from `bq-expand` at 0.9906 to `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 1.0265, with `list` itself at 1.0056.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.052, and tiers at 1.00x, 1.05x and 21.18x, identical on the control --- and `lib-stage2-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7616 over 6 of 6 shapes at sign p 0.031, a margin of 23.84% against this class's 3.35% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). **What is this class's own is the widest single A/A cell of the run, and it sets this process's floor**: 22.29% on `flip-last-rows` in the basis half's process, where BOTH of the shipped leaf's A/A copies read slower than the leaf itself, by 22.29% and 21.42% --- the two copies agreeing and the original's own cell the one that parts, with `--wild` clearing the log of any foreign CPU, so it is no intrusion. That one shape carries the two pairs to 1.0335 and 1.0280, so the basis's floor here is one cell's. The control half's own eight pairs span 0.86%. **Its two columns MAY be differenced**, `list` having moved 0.56 of a point, and the class geomean is 1.0036, NONE of the eight strategies clearing the class's 3.23-point A/A bar --- that bar being the same cell's. The counted work reads 1.0023 over the sixteen. Registration (2) reads stage twelve over stage eleven at 0.9998 and 0.9995, and (5)'s last clause stage eleven over stage ten at 0.9989 and 0.9995 against 0.9994 and 0.9997 off Run 32's cells, read by hand off `--cells` --- both holding on both halves.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.12* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.11 | 113 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.16 | 122 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.03 | 129 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.04 | 129 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 113 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.06 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.16* | *130* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.024* | *0.12* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.024 | 0.11 | 111 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.024* | *0.12* | *111* | *1.00x* |
| lib-stage2-lean | 0.021 | 0.024 | 0.10 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.026 | 0.10 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.026 | 0.12 | 111 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.028* | *0.09* | *111* | *1.00x* |
| **mut-odo-vecdims** | **0.023** | 0.028 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.028* | *0.09* | *111* | *1.00x* |
| lib-stage1 | 0.051 | 0.057 | 0.17 | 103 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.10* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.086 | 0.11 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.086* | *0.087* | *0.12* | *96* | *1.06x* |
| *list-aa-distant* | *0.999* | *1.000* | *0.25* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.29 | 54 | 21.22x |
| *list-aa-adjacent* | *1.002* | *1.005* | *0.25* | *54* | *21.22x* |

**Controls:** The largest A/A pair is `list-aa-distant` at 0.9977, worst cell 1.03% on `block-run64-gap1`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9990 on a worst cell of 0.48% on `block-run64-gap1`, its interval covering 1. The in-situ term reads 1.0232, 1.0175 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9978, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m41s, peak 135 MiB in use, 36 MiB max residency; the reader reads 34 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.64 ms per call raw, 4.49 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.028/0.024/0.020

**Across the halves:** 9 of the 16 arms are faster on this half and 7 slower, at a geomean of 0.9989, from `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9869 to `list-aa-adjacent` at 1.0075, with `list` itself at 1.0039.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.028, joint lowest of the ten with `compose`, and tiers at 1.00x, 1.06x and 21.22x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.021, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.9377 over 5 of 5 shapes at sign p 0.062, a margin of 6.23% against this class's **0.23%** floor (`list-aa-distant`), a floor the tightest of the ten --- so a margin of six points is read here with more confidence than a margin of eighteen is on `runs`. **Its two columns MAY be differenced**, `list` having moved 0.39 of a point, and they say nothing about the compiler: the cross-half geomean is **0.9989** and NONE of the eight strategies clears the class's 1.07-point A/A bar, the counted work level at 1.0019. `lib-stage2-lean-u1`, which carried Run 33's 1.1370 here, reads 0.9975. Registration (2) reads stage twelve over stage eleven at 0.9979 and 1.0000, and (5)'s last clause stage eleven over stage ten at 1.0013 and 0.9987 against 0.9993 and 0.9988 off Run 32's cells, read by hand off `--cells` --- both holding on both halves, the basis's 0.21 of a point inside its 0.23% floor.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.24* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.17 | 228 | 1.64x |
| liblist-stage2-sum | -- | -- | 0.21 | 230 | 1.55x |
| liblist-stage3-sum | -- | -- | 0.18 | 227 | 1.69x |
| liblist-stage4-list-sum | -- | -- | 0.20 | 230 | 1.51x |
| liblist-stage4-sum | -- | -- | 0.17 | 230 | 1.51x |
| libunord-stage1-sum | -- | -- | 0.23 | 223 | 2.07x |
| libunord-stage10-list-sum | -- | -- | 0.29 | 233 | 0.57x |
| libunord-stage10-sum | -- | -- | 0.23 | 233 | 0.55x |
| libunord-stage11-sum | -- | -- | 0.19 | 235 | 0.55x |
| libunord-stage12-sum | -- | -- | 0.24 | 235 | 0.55x |
| libunord-stage6-loop-sum | -- | -- | 0.15 | 234 | 0.81x |
| libunord-stage6-sum | -- | -- | 0.21 | 233 | 0.83x |
| libunord-stage7-sum | -- | -- | 0.20 | 234 | 0.83x |
| libunord-stage9-sum | -- | -- | 0.26 | 233 | 0.55x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.37* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.02* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.03* | *250* | *0.01x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.052* | *0.069* | *0.25* | *229* | *1.27x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.052 | 0.068 | 0.21 | 229 | 1.27x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.052* | *0.069* | *0.28* | *229* | *1.27x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.055 | 0.068 | 0.21 | 228 | 1.27x |
| lib-stage2-lean | 0.055 | 0.098 | 0.20 | 228 | 1.46x |
| lib-stage2-lean-u1 | 0.056 | 0.100 | 0.19 | 227 | 1.46x |
| *mut-odo-vecdims-aa-distant* | *0.060* | *0.087* | *0.41* | *229* | *1.27x* |
| *mut-odo-vecdims-aa* | *0.060* | *0.087* | *0.30* | *229* | *1.27x* |
| **mut-odo-vecdims** | **0.060** | 0.087 | 0.31 | 229 | 1.27x |
| lib-stage1 | 0.089 | 0.106 | 0.18 | 221 | 2.32x |
| bq-expand | 0.134 | 0.193 | 0.14 | 217 | 1.44x |
| *bq-expand-aa-adjacent* | *0.134* | *0.193* | *0.16* | *218* | *1.44x* |
| *bq-expand-aa-distant* | *0.135* | *0.193* | *0.23* | *217* | *1.44x* |
| *list-aa-adjacent* | *0.999* | *1.000* | *0.13* | *179* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.15 | 179 | 21.57x |
| *list-aa-distant* | *1.001* | *1.004* | *0.15* | *179* | *21.57x* |

**Controls:** The largest A/A pair is `bq-expand-aa-distant` at 1.0073, worst cell 2.43% on `small-patch-k5`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 0.9997 on a worst cell of 0.24% on `small-row96`, its interval covering 1. The in-situ term reads 0.9891, 0.9849 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0058, which the correction amplifies by 1.24x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h14m45s, peak 131 MiB in use, 52 MiB max residency; the reader reads 34 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.85 us per call raw, 6.62 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.076/0.050/0.059/0.087

**Across the halves:** 2 of the 16 arms are faster on this half and 14 slower, at a geomean of 1.0097, from `lib-stage2-lean-u1` at 0.9912 to `mut-odo-vecdims` at 1.0227, with `list` itself at 1.0098. **The baseline moved 0.98% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** properties 1, 2 and 3 hold on both halves, and this is the one class where property 3's level clause is read off a `mut-odo-vecdims` family at 1.27x rather than at the result vector --- the per-call constants showing through a call under a microsecond, which is the reservation this class has carried since 2026-09-07; the order clause is unbroken, the tiers reading 1.27x, 1.44x and 21.57x and identical on the control. `worst` is 0.087, the highest of the ten. **The family's ceiling leads the class outright at 0.052**, `lib-stage2-lean` being the best arm outside it at 0.055 and priced against `mut-odo-vecdims` at 0.9074 over 1 of 5 shapes at sign p 0.38, a margin of 9.26% against this class's 0.73% floor (`bq-expand-aa-distant`). **What is this class's own is registration (5), which dies here on one shape of one half**: the class span holds at 0.9363 and 0.9300 and `small-bcast32` holds on both, but `small-flat64` under stage eleven reads 1.0506 over stage seven on the control against the item's 4%, where the basis reads 1.0394. (2)'s span holds, stage twelve over stage eleven at 0.9990 and 0.9939. **This class is one of the two whose columns may NOT be differenced**, `list` having moved **0.98 of a point**, so its cross-half line is an ordering: a geomean of 1.0097, fourteen of the sixteen arms slower on the basis, with the counted work at 0.9989, the one population where the basis executes fewer instructions than the control.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.37* | *85* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.33 | 98 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.31 | 98 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.33 | 98 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.33 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.49 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.40 | 97 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.42 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.31 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.33 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.25* | *112* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.014* | *0.016* | *0.31* | *98* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.30 | 98 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.016* | *0.30* | *98* | *1.00x* |
| lib-stage2-lean | 0.015 | 0.017 | 0.31 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.40 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.017 | 0.29 | 97 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.017 | 0.018 | 0.32 | 97 | 1.00x |
| *mut-odo-vecdims-aa* | *0.024* | *0.028* | *0.25* | *94* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.024* | *0.028* | *0.25* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.028 | 0.20 | 94 | 1.00x |
| bq-expand | 0.094 | 0.102 | 0.36 | 79 | 1.35x |
| *bq-expand-aa-adjacent* | *0.094* | *0.102* | *0.37* | *79* | *1.35x* |
| *bq-expand-aa-distant* | *0.094* | *0.102* | *0.22* | *79* | *1.35x* |
| list (baseline) | 1.000 | 1.000 | 0.67 | 44 | 22.01x |
| *list-aa-distant* | *1.002* | *1.007* | *0.74* | *44* | *22.01x* |
| *list-aa-adjacent* | *1.003* | *1.010* | *0.69* | *44* | *22.01x* |

**Controls:** The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9956, worst cell 0.69% on `compose-zero-mid`, and 7 of 8 intervals cover 1. The `sum-only` halves agree at 1.0011 on a worst cell of 0.50% on `compose-scalar`, its interval covering 1. The in-situ term reads 1.0112, 1.0175 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9987, which the correction amplifies by 3.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h11m53s, peak 126 MiB in use, 33 MiB max residency; the reader reads 34 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 30.9 ms per call raw, 29.8 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.028/0.028/0.022/0.019

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0051, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9906 to `mut-odo-vecdims-aa` at 1.0226, with `list` itself at 1.0037.

**What the class says:** properties 1, 2 and 3 hold on both halves --- `worst` 0.028, joint lowest of the ten with `block`, and tiers at 1.00x, 1.35x and 22.01x, identical on the control --- and the family's ceiling and the best arm outside it TIE at 0.015, `lib-stage2-lean` against `mut-odo-vecdims-add-in-leaf-u2`, the bolding going to the ceiling. The lean fill is priced against `mut-odo-vecdims` at 0.6120 over 4 of 4 shapes at sign p 0.12, a margin of 38.80% against this class's 0.44% floor (`mut-odo-vecdims-add-in-leaf-u2-aa`). **Its two columns MAY be differenced**, `list` having moved 0.37 of a point, where Run 33's could not be, and the cross-half geomean is **1.0051**. **ONE strategy clears the 0.78-point A/A bar, and it is the plain arm**: `mut-odo-vecdims` at **1.0209**, its two A/A copies beside it at 1.0180 and 1.0226, with its counts level at 1.0000 --- so the compiler's one reading on this class is not instructions. `mut-odo-vecdims-add-in-leaf-u1`, Run 33's low extreme here at 0.9361, reads 0.9998. The counted work over the sixteen reads 1.0033. Registration (2) reads stage twelve over stage eleven at 1.0000 and 0.9998, and (5)'s last clause stage eleven over stage ten at 1.0001 on both halves against the 1.0000 Run 32's cells give, read by hand off `--cells` --- both holding on both halves.


## Provenance

**Run 34's halves differ in ONE COMPILER and in nothing else.** One source, `Main.hs` at `2496c98`, one shim at `f31bd1c` and one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1` in front of the assembler, one roster, one shape set, one class list and one bench order, both run under `WILDLOG=1 SATURATE=1`, both launched from the `hugebin/` mount and both with `-A32m -I0 -T -M8G` baked and read back by `+RTS --info`. What differs is the compiler and everything a compiler brings with it: the basis takes ghc-9.12.4 through `cabal.project` and its freeze, the control the in-tree stage1 of the GHC checkout, `10.1.20260803`, through `cabal.project.ghead` and its own freeze --- two stores, two plans and two sets of boot libraries, which the binaries carry back as `ghc-internal-9.1204.0` and `ghc-internal-10.100.0`. **Neither half adds a regime flag**: `-O1` is micro.cabal's own `ghc-options`, so both halves are plain -O1 and `diag` reads the ten-times-apart row on each. **So this pair is Run 33's recipe rebuilt from the moved source and launched from `hugebin/`**, and against Run 32, which the owner's ruling of 2026-09-16 makes this run's cross-run reference, the switch, the shim, five `Main.hs` commits and the launch moved as well.

**The roster is 34 timed arms over 19 main-set shapes and 646 benches, with 61 class views over ten classes for 2074 more, and it is NOT Run 33's.** `./roster-delta.py run33-exit run34-exit` reads 33 arms to 34 over 19 shapes to 19: ONE in and NONE out, the 33 survivors in the same order and no main-set shape moved, and three class views in, `runs-32`, `runs-48` and `runs-64`, taking `runs` from fourteen views to seventeen and leaving the other nine classes unmoved. In, landing at `0d637b7`, is `libunord-stage12-sum`; against `run32-nospec` the same tool reads two arms in, stage eleven's and stage twelve's, and the same three views. The L1 roster pass was therefore OWED and taken whole --- eleven legs over all ten classes and the main set, every one `pass clean`. **The shim did not move under this pair**, `align-as.py` standing at Run 33's `f31bd1c`, so what separates this run from Run 33 is three `Main.hs` commits and the launch.

**The sequence was launched once and ran to the end in ONE window, and nothing was rerun.** The window is 2026-09-17T02:20:29 to 10:12:17, twenty-two processes --- the main set on each half and 20 class processes, one per class per half --- with no hole between one finishing and the next starting. The gate's four ran before them from 01:47:05 to 02:20:27, the four rider stages after them to 10:25:21, and the counted work followed on a box already handed back, from 10:25:32 to 11:11:12. Every process exited 0 at the count its population asks for, with no complaint and no `!!` line in the wall-clock record, and the gheadexit half ran first throughout, each process's `start` line naming its instance under `hugebin/`. The class blocks above carry the basis half's stderr lines, so the main-set processes and the control's ten class processes are the ones no block carries; the main-set two: `run34-gheadexit-main` took 0h55m51s at a peak of 209 MiB in use and 60 MiB max residency and `run34-exit-main` 0h55m43s at 188 MiB and 62 MiB. **NO PROCESS WAS INTRUDED ON**: `--wild` over the hundred and nineteen logs this run wrote reads NO bench at 0.25 of a core in any of the twenty-two sequence logs, the four gate logs or the 88 alone-leg rider logs, the other five carrying no samples. This is the first run to take every reading at run list step 13a, before the launch, and the session read nothing between the launch and the riders' last line.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes agree to **0.36**, **0.20** and **0.68** points on `list`, `bq-expand` and `mut-odo-vecdims`, `list` and `mut-odo-vecdims` crossing 1 between the passes inside those spans, where Run 33's crossed nowhere. **The machine check**, read against Run 32's fingerprint by the owner's ruling, puts `list`'s net at a geomean of **+0.18%**, inside the 3% bar, worst `stretch-primes` at +1.94% and 0 of 19 shapes past 5%. It is NOT like-for-like --- Run 32's published half is this basis less `LOOP_EXITSPAN=1`, on the older shim and five `Main.hs` commits back --- and read arm by arm with `--compare run32-nospec` the sixteen shared timed arms span **0.9952** to **1.0128** with `list` at **1.0002**. So the box has not moved and this run publishes inside the third machine era.

**Every one of the twenty-two processes gated clean, the plateau did not fire, and three A/A worst cells sit above 5%, two of them on the basis half.** The preamble's victim spans 21.035 to 21.443 ms/iter across the run, a **1.94%** spread against a 5% band, all twenty-two processes asserting ONE `keep` and ONE `inuse`; within the halves the control's eleven span 1.71% and the basis's 1.93%. The three cells above 5% are `exit-flip` at **22.29%** on `flip-last-rows`, `exit-window` at **5.24%** on `window-224x224-k3-d2` and `gheadexit-runs` at **5.15%** on `runs-r3-48x30`, and `--wild` clears every log they sit in. The first is both of the shipped leaf's A/A copies reading 22% slower than the leaf on one shape, and through those two pairs' geomeans over six shapes it sets the basis's `flip` floor at 3.35%; its class block has the rest.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run34-exit`, md5 `b7ef1c2aa13d78d83b5c2fe6507d137a`, and `run34-gheadexit`, md5 `68438412a48307432bfa19a9b6f4c0b6`, with `.text` at **20807877** bytes on the basis and **20961087** on the control --- the HEAD half larger by **153210**, the gap Runs 32 and 33 read to the byte --- and load addresses of 4218880 and 4214784, Run 32's two unchanged. Each half sits 20480 bytes above its Run 33 counterpart and 40960 above its Run 32 one; this file offers no mechanism for either. **NEITHER md5 is two-sided**: `Main.hs` moved from `f31bd1c` to `2496c98` since Run 33's build of this recipe, so no md5 here can reproduce an earlier binary's, and what the two say is that they differ from each other. The commit the pair was built at is `2496c98`, transcribed from the pair note while that note is still here; the tree the sequence ran on was `780e0c0`. `Main.hs` has since moved by one comment at this write-up, the `runs-32` note gaining this run's reading, which no binary here carries and no rebuild follows.

**The source moved and a timed function landed while the shim stood still, and the pinning claim's strong form HOLDS for the tracked offsets across that change.** The tracked 28-byte loops were read at the build with `--delta`, and re-read here off the same binaries, against two builds. Against `run33-exit`, the previous build of this recipe, EVERY mod-64 offset is preserved on both groups, `[0, 0, 0, 8, 4, 0]` and `[0, 0]`, with NO address surviving to the byte and two displacements on each, `0x1dc0` and `0x3540` --- three `Main.hs` commits, one timed arm and three class views moving every copy and no head's offset. Against `run32-nospec`, the half this run is compared with and this recipe less `LOOP_EXITSPAN=1` on the older shim, the two-copy group keeps `[0, 0]` and the six-copy group does NOT, `[0, 0, 8, 0, 4, 0]` becoming `[0, 0, 0, 8, 4, 0]` over five displacements of which `0x6978` and `0x6988` are not whole lines --- the offsets Run 33's own `--delta` from that binary read, so the move is the switch's or the shim's and not this run's source. What that means for the ruling is [that section][floor]'s to write. **Within the pair** `./loop-offsets.py run34-gheadexit run34-exit` puts the six-copy group at `[0, 0, 0, 8, 4, 0]` on the basis and `[18, 0, 0, 0, 9, 2]` on the control and the two-copy group at `[0, 0]` on both, Run 33's offsets unchanged, and post-run step 0's twins name those six as `fbMidCopy`, `fbCanonVecdims`, `fbMutOdoVecdimsAddIn`, `fbMutOdoVecdims`, `fbMutOdoVecdimsAddOut` and `fbMutOdoVecdimsAddBoth` on each half, with `fbBuild` and `fbMutOdo` the two.

**The straddling loops stand at EIGHT on each half, as on Runs 32 and 33, and no exit span sits astride on either.** `loop-offsets.py --survey` reads **319** self-loops of at most 64 B in the basis's own compiled code, 190 of them at offset 0, and **338** on the control, 202 at offset 0, against Run 32's 292 with 134 and 310 with 130, read off that run's binaries --- about three fifths at offset 0 on both halves, as on Run 33, where Run 32's plain form had under a half. Within the pair `--library` reads **136** self-loops in common in the LINKED libraries, **11.0%** of them at the same offset in line and **65.4%** in the same straddle state --- Run 32's three figures to the digit for the third run, under a moved shim and a moved source, and this file offers no account of that. **Post-run step 0's naming was taken off the binaries that were timed**, with two `-g3` twins built from the same two recipes: six of the basis's eight straddlers are named by byte identity --- `fillStage2Short`, `fbMutOdoVecdimsAddInLeafU2` twice, and its `Down`, `Last` and `Ptr` forms --- and three of the control's, one of those three off the OTHER half's twin. The fill groups name the same six and two arms on each half, at Run 33's offsets.

**The regime was confirmed in this run's own binaries before the hours were spent, and both halves read the same side of it.** `diag` reads `baseOffsetsScan` against `baseOffsetsMut` on `vgg-14-c512` at **24066407** against **2408530** on the basis and 24066455 against 2408530 on the control --- **9.992** times apart on each, the ten times this README has attributed to plain -O1 since Run 8, and Run 33's four figures unchanged. The version comes out of the binaries rather than off a project file: `ghc-internal-9.1204.0` on the basis and `ghc-internal-10.100.0` on the control, the HEAD Runs 32 and 33 ran.

**The three main-set anchors** read **6.40 us** on `cnn-slice-c32`, **3.74 ms** on `cnn-L2-24x24-c32` and **39.5 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm:
| shape | `l` | `list`, per call | net | `gheadexit`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.57 us | 6.40 us | 6.35 us |
| `cnn-L2-24x24-c32` | 165888 | 3.84 ms | 3.74 ms | 3.73 ms |
| `stretch-wide-2xM` | 1800000 | 40.6 ms | 39.5 ms | 40.2 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's shapes, raw and net.** The main set's three guard a baseline that moves for every population at once; a class anchor guards one that could move for that mechanism alone, which is the case a table of ratios hides completely. The `runs` anchor is `runs-2` at **40.86 ms** raw and **39.79 ms** net on the basis, against Run 32's 40.71 ms and 39.63 ms on that run's basis --- 0.37% and 0.39% above it, computed from the cells, carrying the switch, the shim, five commits and the launch as well as the box. **The control half reads 41.27 ms and 40.19 ms on the same shape**, one percent above the basis. **ONE class population moved this run**: `roster-delta.py` reads 58 class views to 61, `runs` taking `runs-32`, `runs-48` and `runs-64` and the other nine classes unmoved, so a `runs` figure against an earlier run is read over the fourteen shapes both carry.

**The correction sits on the same footing in both halves, and two cells of the whole run are ones the reader flags.** The two `sum-only` halves agree to within **0.18%** on every population and both halves --- 0.9982 to 1.0011 across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. `CI%` reads a geomean of **0.97** over the 34 arms, 15 wider on the basis and 19 narrower. **Two cells sit below R2 0.99**, one a half and both on the looping stage-six consumer: `runs-2/libunord-stage6-loop-sum` at 0.9898 on the basis and `window-64x64-c16-k3/libunord-stage6-loop-sum` at 0.9878 on the control; no cell of any population sits under ten samples.

**The counted work covers every population, no cell was refused anywhere, and the two compilers emit very nearly the same work.** The counts geomean over the sixteen timed arms runs **0.9989** on `small` to **1.0098** on `window`, the main set at 1.0053, with the ten fill-family arms running 0.9996 to 1.0081 on that main set. On the main set `time/counts` puts `lib-stage1` at **1.0181** and the shipped leaf at 1.0061, while `list` and its two A/A copies sit at 0.9907 to 0.9912 --- the basis executing about one percent MORE instructions on the reference and running it level. Among the nine populations whose columns may be differenced, the one where the counts carry much of a figure is `window`, `lib-stage1` and `lib-stage2-lean` executing 1.76 and 1.56 points more on the basis and taking 5.93 and 4.98 more time. So the compiler term this pair measures is small, and mostly outside the instruction stream where it is not. **Read per cell rather than per arm, after the write-up, those geomeans hid the run's largest cells.** The largest count differences of the run are `lib-stage2-lean-u1` on `compose-scalar` at **1.0714** and on `flip-whole-square` and `scaled-rank1-m1` at **0.9412**, GHC #27799's latch on a rank-1 view with the time level on all three; and with their counts at 1.0000 the `mut-odo-vecdims` family reads **1.23** on `runs-16384` on the basis, a term of that process which a fresh process does not reproduce, **1.11** on `compose-zero-mid`, one branch mispredict a run on the basis where HEAD's layout predicts the carry, and the leaf `u1` **1.24** on `scaled-rank1-m1`, the file instance above. Post-run step 4b takes that reading now.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0000** on the basis and **1.0000** on the control on the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0309** and **1.1113** on the basis and **1.0310** and **1.1006** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and ten or eleven on `bq-expand`, by nearly the same on both halves, which is where it has run since Run 17. So the compiler does not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns do not part.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, and the state the preamble puts on a process comes back at a geomean of **1.1192** on the basis and **1.1165** on the control, 0.27 of a point apart. What the roster adds on top of that state is **1.0134** on the basis, 4 of 19 shapes above 1, and **1.0141** on the control, 4 of 19; the basis's rest runs 0.9382 on `cnn-L1-6x6-c1` to 1.2318 on `stretch-r5-8x432`, the control's 0.9667 on `stretch-bigstride` to 1.1967 on that same worst shape.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is Run 32's two compilers at plain -O1 with the exit span added on both halves, ghc-9.12.4 the basis and GHC HEAD the control, both halves built from the moved source and launched from `hugebin/`, and the earlier run it is read against is Run 32, by the owner's ruling of 2026-09-16 that Run 33's timings are skewed by filesystem issues --- the file-page frames [the placement section][floor] prices. So what varies from Run 32 is the switch, the shim, from `b3a1aca` to `f31bd1c`, the launch and the source: `libunord-stage11-sum`, stage ten with its zero-stride move guarded; `libunord-stage12-sum`, stage eleven with the run chosen among tied unit-stride axes by its length (reasons at `routeUnord12`; its fill is rostered checked and never timed); and `runs-32`, `runs-48` and `runs-64` in the `runs` class. Stage eleven's guard fires on a zero stride of extent above 1 and not on any zero, corrected 2026-09-16 for `small-flat64`, `[4, 1, 64]` on strides `[64, 0, 1]`, where canonicalization makes the route one block on every stage and stage ten's move runs anyway, 17 and 20 percent a call over stage seven on Run 32's two halves; stage twelve's guard mirrors the correction. Each prediction is its own kill condition, and a `predict:` span that fails kills its item.

(1) *Stage twelve takes stage six's run on three of the four unstrided `window` views without channels and stage seven's everywhere else.* On `window`, Run 32's per-shape figures on the basis give the pair with stage six 0.90, level on the three moved views and stage seven's advantage on the two with channels and `window-28x28-k5`: `predict: pair libunord-stage12-sum libunord-stage6-sum 0.90 within 3%`; and against its control, from Run 32's stage six over stage seven, which is stage eleven's route on a class with no zero stride, 0.72, 0.80 and 0.84 on `window-128x128-k7`, `window-64x64-k1x9` and `window-224x224-k3`, the three moved views, and 1 on the other five, `predict: pair libunord-stage12-sum libunord-stage11-sum 0.92 within 3%`. Each of the three moved views within a point of stage six, whose run it takes under stage seven's outer order and not stage six's, read off `--pair --per-shape` by hand, four probes having put them between 0.990 and 1.024. The probe of 2026-09-16 on the basis recipe and a quiet machine, `probe-stage12h-window.json`, read the two pairs at 0.901 and 0.912 on the class.

(2) *And moves nothing else.* The same probe's `small`, `bcast` and `rev` files and its main-set twin, `probe-stage12h-small.json`, `-bcast.json`, `-rev.json` and `-main.json`, read stage twelve within 1.1 percent of stage eleven on every view it leaves at stage seven's run, the five `window` views, `small-patch-r5`, `small-patch-k5`, `cnn-L1-6x6-c1`, `cnn-L1-24x24-c1` and `cnn-slice-c32`, and on `bcast-inner8` and `rev-cnn-L1-24x24-c1`, where the guard and the other tie-break rule; the list form this arm first took read 4 to 6 percent behind on the tiny views and the `<>` form 2.5 and 4, the case form retiring fewer instructions a call than stage eleven. So on the main set and on every class but `window`: `predict: pair libunord-stage12-sum libunord-stage11-sum 1.0 within 1%`; and the count sweep, read by hand with `--counts --pair`, puts stage twelve under stage eleven by fewer than a hundred instructions a call on every tie view it leaves alone, on both compilers, and within a percent of stage six's count on the three it moves.

(3) *It inherits stage six's placement term on the views it moves.* Run 32 read stage six 1.084, 1.019 and 1.215 slower on HEAD on the three, in that order, and stage seven, stage eleven's route there, within a point, and stage seven's cross on the class was 0.973; replacing its three cells by stage six's gives 0.938: on `window`, `predict: cross libunord-stage12-sum 0.94 within 2.5%`, a span stage eleven's own figure sits outside of, so reading it kills the item as surely as reading 0.90 does.

(4) *The three `runs` shapes sit where the probe of 2026-09-16 put them.* On `runs`, both halves, `runs-32` within 3 percent of `runs-9` per element on every `-sum` arm, the probe having timed `libunord-stage6-sum` and `libunord-stage11-sum`, and `runs-48` and `runs-64` within 3 percent of `runs-96`, read off `--cells` by hand; no span, the quantity being a cell and not a pair.

(5) *Stage eleven's corrected guard takes `small-flat64` back and moves nothing else.* The guard is two tests, the old one-list `any` first and one loop over strides and extents behind a zero, so a view with no zero stride retires the count it retired, `small-patch-k5` to the instruction on the basis probe of 2026-09-16, `probe-s11guard4-small.json`, and a view with one pays the second test, `small-bcast32` 133 instructions a call over stage ten, 78 of them the extent test's. On `small`, both halves: `small-flat64` under stage eleven within 4 percent of stage seven, from 1.17 and 1.20, stage ten's on Run 32's two halves, the probe reading 1.030 at 185 instructions a call over stage seven, and `small-bcast32` under stage eleven within 6 percent of stage ten, the probe reading 1.028, both read off `--pair --per-shape`; on the class `predict: pair libunord-stage11-sum libunord-stage7-sum 0.94 within 2%`, the probe reading 0.941 where Run 32's cells, stage ten's on the two views with a zero stride and stage seven's on the other three, give the uncorrected guard 0.94 and 0.95 on its two halves and the corrected one 0.91 and 0.92 before the guard's own cost; and on every other population stage eleven's pair with stage ten where Run 32's cells put it, stage seven's over stage ten on the views without a zero stride and level on the rest, within the floor, no view there carrying a zero stride on an axis of extent 1.

**Two of the five held and three were killed --- every `predict:` span of the five holding on the basis half, and all three kills falling on clauses read by hand.** Every verdict below is its item's KILL CONDITION applied across the populations and halves the item names, an item that names no half being read on the basis, where `--predictions` reads a `pair` span, and the items that want both halves saying so, as (4) and (5) do; every figure is re-derived from this run's own JSONs, by `--predictions` over each population on each half, by `--cells` where a clause names a shape, and by `--counts` where it names instructions. **One thing governs how the list reads**: stage twelve does what it was built to do on `window` and nothing elsewhere, and what failed is per-shape and per-count readings the probes of 2026-09-16 had put a point or two inside their bands.

(1) *Stage twelve takes stage six's run on three of the four unstrided `window` views without channels and stage seven's everywhere else.* **HELD** on the basis, the half an item naming none is read on. On `window` the basis reads `pair libunord-stage12-sum libunord-stage6-sum 0.90 within 3%` at **0.8943** and `pair libunord-stage12-sum libunord-stage11-sum 0.92 within 3%` at **0.9188**, and the three moved views sit within a point of stage six --- **0.9926** on `window-128x128-k7`, **0.9996** on `window-64x64-k1x9` and **0.9906** on `window-224x224-k3`. Read within the control half, which the item does not name, both spans would miss, **0.8529** and **0.9542**, and `window-64x64-k1x9` sits 2.14 points from stage six at 1.0214 --- the control's stage twelve being the slower of the two halves by the seven points item (3) reads.

(2) *And moves nothing else.* **KILLED by its count clause, every span holding**: `pair libunord-stage12-sum libunord-stage11-sum 1.0 within 1%` reads **1.0008** and **0.9978** on the main set on the two halves, and on the nine classes other than `window` between **0.9939**, on `small`'s control half, and **1.0031**, on `scaled`'s --- no reading further than 0.61 of a point from level. **Its count clause, read by hand off the counts files, holds as a bound and misses as a direction**: stage twelve sits within 73 instructions a call of stage eleven on every tie view on both compilers, and within half a percent of stage six's count on the three views it moves --- 0.9981, 0.9960 and 1.0004 on the basis and 0.9980, 0.9959 and 1.0004 on the control --- but it retires MORE than stage eleven on 20 of the 154 tie-view readings, by 1 to 43 instructions, and on five of them --- two on `block`'s control, one on `small`'s basis and one on each half of `window` --- by more than the identical-code `sum-only` pair differs on that population. **So (2) is KILLED by that direction**, its spans and its bound holding.

(3) *It inherits stage six's placement term on the views it moves.* **HELD**: `cross libunord-stage12-sum 0.94 within 2.5%` on `window` reads **0.9304**, the basis the faster and 0.96 of a point from the centre, where stage eleven's own cross on the class reads 0.9664 and stage six's 0.8873 --- stage eleven outside the band by 0.29 of a point, as the item said it would be.

(4) *The three `runs` shapes sit where the probe of 2026-09-16 put them.* **KILLED on both halves**, read off `--cells` as raw slope per element. `runs-48` sits **4.0 to 5.4%** under `runs-96` on every one of the ten consumers whose loop is a unit-stride run, on both halves, where the item allowed three; `runs-64` holds at 1.7 to 2.6% under; and `runs-32` against `runs-9` splits by half, **3.4 to 5.0%** over it on the basis and 2.3 to 3.4% under it on the control, some consumers inside the band there and some not. So the step the probe put by 48 is not finished there: stage eleven's cost an element on the basis climbs 0.290, 0.300, 0.362, 0.371 and 0.380 ns at 9, 32, 48, 64 and 96, and the control's 0.312, 0.302, 0.362, 0.373 and 0.383. The four consumers whose cost is a per-run overhead --- `liblist-stage1-sum`, `liblist-stage2-sum`, `libunord-stage1-sum` and `libunord-stage6-loop-sum` --- read `runs-32` at 0.41 to 0.59 of `runs-9` an element, their cost per element falling with run length; on the two longer clauses `libunord-stage6-loop-sum` holds within 1.4% on both halves, `liblist-stage2-sum` reads `runs-64` 3.4% over `runs-96`, just outside the band, and `runs-48` 15 to 16% over, and the other two read both 13 to 30% over. The item's *every `-sum` arm* covered them and its probe did not time them.

(5) *Stage eleven's corrected guard takes `small-flat64` back and moves nothing else.* **KILLED within the control half, on `small-flat64`.** On `small` the class span `pair libunord-stage11-sum libunord-stage7-sum 0.94 within 2%` HOLDS on both halves, **0.9363** and **0.9300**, where the preparation had put Run 32's cells under the corrected guard at 0.9125 and 0.9166 before the guard's own cost; `small-bcast32` under stage eleven sits within 6% of stage ten on both, at 1.0202 and 1.0367; and `small-flat64` under stage eleven reads **1.0394** over stage seven on the basis, inside its 4%, and **1.0506** on the control, outside it. The last clause holds everywhere it is read: stage eleven over stage ten, against the figure Run 32's stage seven over stage ten gives on the views without a zero stride and 1 on the rest, sits within its population's floor on the main set and every class but `small` on both halves, the widest being `block`'s basis at 0.21 of a point against 0.23% --- read by hand off `--cells`, each view classed by which of stages seven and ten this run's own basis cell lies nearer.
