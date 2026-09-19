# Run 36 (GHC HEAD against itself, plain -O1 against -O1 with -fspec-constr -fliberate-case, under the exit span)

One run's write-up: its head, its Results, what the next run compares against, the properties that run should test, the ten class blocks, and its own Provenance. A run replaces this file whole and edits [README.md](../README.md) around it, in the score of places [the replace list under Provenance there][prov] names --- the open list among them, which is where a run's surprises go and where its registrations keep a verdict and a pointer --- the registrations themselves being in this file since 2026-08-29, in the section at its foot. So this file is most of what a run replaces and by no means all of it. What stands between runs is the harness, [the procedure][procedure] that makes a file like this one, and the rulings a measurement does not reach.

**Run 36 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, under the exit span): the two passes are worth 33.60 points on `list` and 29.80 on `bq-expand`, and NOTHING else that carries a corrected time moves past 1.2%.** The pair is `run35-gheadexit`'s recipe on both halves --- one source, `Main.hs` at `0eda736` unmoved since that build, one shim at `f31bd1c` under the four switches with the exit span, ONE compiler, one roster, one shape set, every process launched from `hugebin/` --- with two `-O2` passes added to the control half's command line and nothing else differing. So `the basis` below is the UNFLAGGED half and every `cross` figure reads basis over control, ABOVE 1 meaning the FLAGGED half is the faster. Over the sixteen main-set arms that carry a cross-half figure, SIX move and TEN do not: the six are the `list` and `bq-expand` families entire, at **1.2980** to **1.3360**, and the ten others span **0.9920** to **1.0119**, every one of them a fill. **The bar an arm has to clear to be the passes' rather than the run's is 1.90 points** --- the widest an arm and its own A/A duplicate part in this same cross-half reading, which `--compare` prints under its table and which is NOT this population's floor, that being 1.63% and measured WITHIN one half --- and exactly two of the eight strategies clear it, `list` and `bq-expand`.

**What the pair was built to settle is an arithmetic Run 31 left open, and it settles it against Run 31's own figure.** Run 31 measured the whole `-O2` level at **1.2974** on `list`; `-fspec-constr` and `-fliberate-case` measured one at a time on Runs 29 and 30 multiply to **1.3325**, a 3.51-point overshoot that is either the level's other passes handing `list` back or an artefact of composing two runs' readings. This pair puts both passes on one half and neither on the other and reads **1.3360** --- past the level by 3.86 points and past the composition by 0.35 --- so the composition is not an artefact and the level's other passes do hand `list` back. **`bq-expand` is the control on that reading and it confirms both accounts**: where the level and the composition agree to a quarter of a point, 1.2943 and 1.2967, the pair reads **1.2980**. That is what licenses reading item (1)'s miss as the composition question rather than as the compiler having moved under the pair --- and the compiler is separately bounded, `run36-gheadnospec` against `run35-gheadexit` reading every one of the sixteen arms within 1.02 points of 1, 0.9898 to 1.0099.

**The counted work parts far wider than the clock, and it parts on exactly the two families.** `list` retires **1.2926** and `bq-expand` **1.5063** times as many instructions on the unflagged half, against 1.0383 on `mut-odo-vecdims` and 1.0522 on `lib-stage2-lean` --- so the basis retires 50.6 points more instructions than the flagged half on `bq-expand` and takes only 29.8 points more time over it, a `time/counts` of **0.8617**, where `list` cashes more than it saves at **1.0336**. **They move allocation too, as every earlier flag pair did, and by exactly what the whole level moved**: the flagged half allocates **0.8119** of the basis on `bq-expand` and every one of its three twins and **0.9342** on `list` and both of its, on the main set and in the same shape on all ten classes, while every other timed arm reads 1.0000 to within two tenths of a point on the main set and only one moves at all across the classes. That breaks property 3's LEVEL clause in every one of the eleven populations, as Run 31's whole `-O2` level did --- to the published decimal, 2.11x and 23.45x on the main set on each --- while its ORDER clause holds everywhere.

**One registration item is killed and three hold their sentences, over 20 spans of which 15 held and 5 were killed --- and two of those five kills are the first one counted again.** (1) is killed on `list` and is the run's finding; (2) holds on `bq-expand`; (3)'s sentence holds, no arm outside the two families joining them, while its two `list`-family spans die with item (1)'s and for its reason; (4)'s sentence holds, the counted work parting on all four arms it spans, while its two family spans die on size. **The run's one anomaly is a single cell and it is worth 2.31 points of the headline**: `stretch-coprime-r7/list` on the basis reads a CI of 10.07% and an R2 of 0.9395 where its own two A/A copies, in the same process, agree to 0.22 of a point and stand 28.4% below it. Excluding that shape puts `list` at **1.3129**, which is still outside item (1)'s band but BETWEEN the two accounts rather than past both --- so the pair kills the level's figure for these two passes and leaves the size of the other passes' contribution open to a point and a half. Nothing else is wrong with the run: 22 of 22 processes gated clean, no bench of the 119 logs reaches 0.25 foreign, and the plateau's refusal splits exactly by half with each half flat inside 1.9%.

**Everything in this file is replaced by the next run, which is what makes it a file.** What a run replaces OUTSIDE it, in README.md and in the sources, is [README's own Provenance](../README.md#provenance). None of it is portable: a run on another machine is a different measurement rather than a repetition. **What this run leaves the next one is the first published basis on this compiler and one question split off the one it closed**: `run36-gheadnospec` is a plain -O1 GHC HEAD build whose recipe a next run can repeat for a like-for-like reading this one could not have, and the arithmetic that wanted this pair is now closed against Run 31's level figure while the SPLIT --- which of the two passes carries the 33.60 points --- has been read on no compiler this series still builds with.


## Results

The shared forcing pass is subtracted here, as every run since Run 6 must ([sum-only](../README.md#sum-only-and-the-correction-now-applied) carries that decision and this run's re-pass of its gates), the scratch vectors are the unboxed ones the shipped code uses, as they have been since Run 7 ([the scratch vector flavour](../README.md#the-scratch-vector-flavour) says what that severed), and **this is a PLAIN -O1 table under the exit span**, as Runs 32 to 35's were, plain -O1 being the regime `Data/Array/Internal.hs` actually compiles under. **On this run that sentence describes the BASIS half and not the pair**: the control half is that same -O1 with `-fspec-constr -fliberate-case` on its command line, two of `-O2`'s passes and nothing else, so the table below is the unflagged half's. **What is new in it is neither the source nor the switch**: `Main.hs` stands at `0eda736`, unmoved since Run 35's build, and the shim at `f31bd1c`, the four shim variables, the regime and the launch from `hugebin/` are Run 35's to the commit. What moved is the compiler, to an in-tree stage1 of `10.1.20260918` where Run 35's HEAD half was `10.1.20260803`. **Read against the half Run 35 built by this basis's own recipe, the distance is under 1.02 points on every arm**: over the 16 arms that carry a corrected time, this run over that one runs from **0.9898** on `lib-stage2-lean-u1` to **1.0099** on `list` --- below 1 meaning this run is the faster --- and read as a ratio to `list` within each run, which cancels a box term exactly, the other fifteen give a `--bridge` geomean of **0.9890**, none outside the 3.3% drift band Run 11 measured. That span carries six weeks of GHC HEAD with its rebuilt dependency stack, and nothing else. **The `alloc` column is a median over this run's own nineteen shapes**, `bq-expand` at 2.78x and `list` at 25.20x, so it is a statistic of a strategy and a shape set together and does not cross to a run that timed a different set.

**And it is the basis half's**, `run36-gheadnospec`, as every published table here is from Run 11 on: the control half's column sits beside the basis one in [What the next run compares against](#what-the-next-run-compares-against) rather than as a second copy of these thirty-five rows. Which half publishes is not the re-declaration of 2026-09-15 this run inherits --- that one names ghc-9.12.4, and this pair has ONE compiler on both halves, so it cannot decide anything here. What decides it is the pair's own variable: the UNFLAGGED half is what `Data/Array/Internal.hs` compiles under, the flagged one is the candidate reading, and `--compare` takes the basis first, so every `cross` figure below reads unflagged over flagged and ABOVE 1 means the FLAGGED half is the faster. **None of the thirty-five rows is a first reading**: the roster is Run 35's unchanged --- none in, none out, thirty-five survivors in the same order over the same nineteen shapes, which `roster-delta.py` read off the two runs' binaries before this one ran --- so every row here has a twin in Run 35's file and all but `libunord-stage12-sum` and `libunord-stage13-sum` in Run 33's, those two having landed on Runs 34 and 35.

**Comparing runs?** The table below is Run 36's own; what to hold a new run against is [What the next run compares against](#what-the-next-run-compares-against), the properties to test are [the ones after it](#the-properties-the-next-run-should-test), the absolute anchor is under [Provenance](#provenance) below and the population it was measured over in [README's delta chain](../README.md#provenance), and this run's own floor --- no A/A pair further than **1.63%** from 1 on the basis half or **0.53%** on the control, read over the eight pairs this roster carries, and over the four pairs that carry back to Run 10 at **0.75%** and **0.42%** --- is [in the floor section][floor], which is where the figures are DEFINED and which of them answers what: this file quotes them and does not re-derive the rule. **The two halves name DIFFERENT pairs this run**, `list-aa-adjacent` on the basis and `mut-odo-vecdims-add-in-leaf-u2-aa-distant` on the control, where the carry-back figure names `bq-expand-aa-distant` on each; so the whole-set figure and the carry-back one part on both halves, by eighty-eight hundredths of a point on the basis and eleven on the control. Beside those, the worst SINGLE A/A cells of the two MAIN-SET processes --- **28.36%** on `stretch-coprime-r7` on the basis and **2.72%** on `stretch-r5-8x432` on the control --- are not floors at all and are not to be quoted as any; the first of them is this run's one anomaly and has a paragraph of its own below. **And its two columns may be differenced on NONE of the eleven populations**, `list` having moved **33.60 points** on this run's main set and between 24.97 and 37.98 on the ten classes, all of it past the bar, so every cross-half figure in this file is an ORDERING and not a subtraction.

**It is the main set's table**, and every column below is a statistic of that population: each stride class has a table of its own, on the same rows and in the same columns but its own basis, in [The stride classes, run by run](#the-stride-classes-run-by-run). No figure crosses between them.

How to read the columns, and why `time` is a winsorized geomean of slopes rather than criterion's mean, is [README's *Reading a run file*](../README.md#reading-a-run-file).

| strategy | time | worst | CI% | smp | alloc | needs |
|---|---:|---:|---:|---:|---:|---|
| *bq-expand-nosum* | *--* | *--* | *0.61* | *55* | *2.78x* | *its base arm, forced with one element* |
| liblist-stage1-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over the ordered list of master's slice recursion |
| liblist-stage2-sum | -- | -- | 0.59 | 70 | 1.00x | the same, over the port's base-offset table |
| liblist-stage3-sum | -- | -- | 0.66 | 70 | 1.00x | the same, over the lazy odometer under the natural-strides dispatch |
| liblist-stage4-list-sum | -- | -- | 0.57 | 70 | 1.00x | the same, base's `sum` over stage four's list -- the fold a library user brings, over the lazy odometer under the lean dispatch |
| liblist-stage4-sum | -- | -- | 0.61 | 70 | 1.00x | the same, over the lazy odometer under the lean dispatch |
| libunord-stage1-sum | -- | -- | 0.03 | 83 | 0.00x | the same, over stage one's list, which is master's consumer |
| libunord-stage10-list-sum | -- | -- | 0.01 | 83 | 0.00x | the same, base's `sum` over stage ten's list -- the fold a library user brings, over the two reorderings composed |
| libunord-stage10-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's tie-break with stage nine's zero-stride axes moved outermost -- the two reorderings composed |
| libunord-stage11-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage eleven's list --- stage ten with its zero-stride move guarded, so the move fires only where a zero stride is there to move |
| libunord-stage12-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage twelve's list --- stage eleven with the run chosen among tied unit-stride axes by its length |
| libunord-stage13-sum | -- | -- | 0.02 | 83 | 0.00x | the same, over stage thirteen's list --- stage twelve's route found with fewer passes over the axes |
| libunord-stage6-loop-sum | -- | -- | 0.01 | 83 | 0.00x | the same, the fold taken into the walk -- a strict loop over the levels and no list |
| libunord-stage6-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage six's list -- stage five with the first canonicalization dropped |
| libunord-stage7-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage seven's list -- the tie-break, the longer extent innermost |
| libunord-stage9-sum | -- | -- | 0.01 | 83 | 0.00x | the same, over stage nine's list -- every zero-stride axis moved outermost |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.36* | *79* | *1.00x* | *the same, on the fastest arm* |
| *sum-only-early* | *--* | *--* | *0.02* | *83* | *0.00x* | *the term every row has subtracted* |
| *sum-only-late* | *--* | *--* | *0.01* | *83* | *0.00x* | *the same, at the other end* |
| lib-stage2-lean | 0.027 | 0.112 | 0.49 | 70 | 1.00x | new mutating `Vector` method -- the branch's driver, dispatch without the strides comparison |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.028* | *0.112* | *0.51* | *69* | *1.00x* | *A/A control* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.028 | 0.113 | 0.49 | 69 | 1.00x | new mutating `Vector` method -- what `genericFillStrided` is a port of |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.028* | *0.112* | *0.66* | *69* | *1.00x* | *A/A control* |
| lib-stage2-lean-u1 | 0.028 | 0.110 | 0.60 | 69 | 1.00x | new mutating `Vector` method -- the lean dispatch with the stepping run not unrolled, the unrolling's control |
| lib-stage1 | 0.028 | 0.112 | 0.55 | 69 | 1.00x | new mutating `Vector` method -- stage one as it shipped, dispatch included |
| mut-odo-vecdims-add-in-leaf-u1 | 0.029 | 0.110 | 0.61 | 69 | 1.00x | new mutating `Vector` method -- the shipped fill's leaf with the bound merged in and the body not unrolled |
| *mut-odo-vecdims-aa-distant* | *0.044* | *0.111* | *0.44* | *66* | *1.00x* | *A/A control* |
| *mut-odo-vecdims-aa* | *0.044* | *0.111* | *0.43* | *66* | *1.00x* | *A/A control* |
| **mut-odo-vecdims** | **0.044** | 0.111 | 0.42 | 66 | 1.00x | **new mutating `Vector` method -- THE FIX, decided 2026-08-22** |
| bq-expand | 0.125 | 0.256 | 0.68 | 50 | 2.78x | nothing (pure) -- the last candidate |
| *bq-expand-aa-adjacent* | *0.125* | *0.256* | *0.66* | *50* | *2.78x* | *A/A control* |
| *bq-expand-aa-distant* | *0.126* | *0.256* | *0.41* | *50* | *2.78x* | *A/A control* |
| list (baseline) | 1.000 | 1.000 | 0.78 | 21 | 25.20x | -- |
| *list-aa-adjacent* | *1.000* | *1.012* | *0.50* | *21* | *25.20x* | *A/A control* |
| *list-aa-distant* | *1.000* | *1.028* | *0.73* | *21* | *25.20x* | *A/A control* |

**DO NOT DIVIDE TWO ROWS OF THIS TABLE FOR A MARGIN.** The `time` column is a geomean over shapes of net over `list`'s net, WINSORIZED per row, so a ratio of two of its entries equals the per-shape paired ratio only where neither row had a cell capped --- and on this run TWO of the 105 pairs among the fifteen timed arms other than `list` part in SIGN between the two statistics on the basis, where Run 35's basis parted on three and Run 34's on six. They are `lib-stage1` over `lib-stage2-lean-u1`, column **1.0104** against a paired **0.9965**, and the shipped leaf over its distant A/A copy, column 0.9979 against a paired 1.0014. **The widest disagreement is on the rows the cap touched most**: `lib-stage2-lean-u1` over `list-aa-adjacent` divides to 0.0281 on the column where the paired figure is 0.0298, the column 5.6% under it, and `lib-stage2-lean-u1` is the widest-capped row of the table, four of its nineteen cells capped and its published 0.02811 sitting 4.0 points under its plain per-shape geomean of 0.02929. Those column ratios are `--pair`'s own `published-column ratio` and not the printed table divided. **And a SINGLE row's movement between runs is not the arm's either**: `--movement` reads fifteen of the sixteen rows moved against Run 35's table and one at the same three decimals, where `--compare` against the JSON of the half Run 35 built by this basis's recipe puts every one of the sixteen within a point of level and `list` at 1.0099.

**This run's two columns may be differenced on NONE of the eleven populations, as Run 31's could not, and the reason is the pair itself.** The 0.7% bar asks whether `list` --- the denominator every other row is divided by --- sits still between the halves, and here the two passes move `list` by **33.60 points** on the main set and by 24.97 on `bcastmid` to 37.98 on `bcast` over the ten classes, every one of the eleven figures past the bar by a factor of thirty or more. So on every population in this file an arm-by-arm figure across the halves is an ORDERING and not a subtraction, and each says so in its own cross-half line. Run 35 could difference seven of the eleven and Run 34 nine; Run 31, the only earlier pair whose variable was a level, marked all eleven past the bar as this one does. **That is the bar working rather than failing**: it exists to stop a margin being read off two columns with different denominators, and a pair built to move the denominator is the case it was written to refuse.

`concat-runs` has no row, and neither do the other 87 arms the roster holds and checks without timing --- **88 of its 123** in all, as on Run 35: the reason is at each entry and the count is [`--lint`'s](../README.md#the-reader-read-runpy). **NO arm was added, retimed or parked this run**, `Main.hs` not having moved since Run 35's build, so the roster is that run's entire --- none in, none out, thirty-five survivors in the same order over the same nineteen main-set shapes and the same sixty-one class views, which `roster-delta.py` read off the two binaries before the run. The six parked on 2026-09-13 stay parked and the thirteen Fill arms over a list that went to `check` on 2026-09-09 stay where they are. So a movement against Run 35's own HEAD column is a movement on the **16 shared arms that carry a corrected time**, with a compiler term between the two runs and no source, switch, shim or launch term at all --- and a movement across THIS run's two halves is the two passes, with no term of any other kind.

**Three things in the table are the run's findings rather than its numbers.** **The head of the table is `lib-stage2-lean` at 0.027**, with the shipped leaf and its two A/A copies at 0.028, `lib-stage2-lean-u1` at 0.028, `lib-stage1` at 0.028 and `mut-odo-vecdims-add-in-leaf-u1` at 0.029 --- **five timed non-control arms below `mut-odo-vecdims`'s 0.044**, every one of them a fill that writes the result, the same five Runs 31 to 35 had. **The column and the pair now AGREE about the order behind the leader on every pair but one**, where Run 35's basis parted on three and Run 34's on six: paired on the basis, `lib-stage2-lean` over `lib-stage1` is **0.9392** at 15 of 19 and p 0.019, over its own unrolling twin **0.9359** at 15 of 19 and p 0.019, and over the shipped leaf **0.9737** at 16 of 19 and p 0.0044, so pairs and column alike put the leaf second and the twin behind it. The one pair that parts in sign among the leading arms is `lib-stage1` over `lib-stage2-lean-u1`, column **1.0104** against a paired **0.9965** at 12 of 19 and p 0.36, which separates them neither way; the other is the shipped leaf over its own distant A/A copy. That the disagreement shrank is the winsorizing and not an arm: `lib-stage2-lean-u1` is the widest-capped row here, and its published 0.02811 sits 4.0 points under its plain per-shape geomean where Run 35's sat 12.3 under. **The third is that the leaf fusion is untouched by the two passes**: `mut-odo-vecdims-add-in-leaf-u2` over `mut-odo-vecdims` reads **0.6381** on the basis and **0.6382** on the control, a hundredth of a point apart on a pair that moves `list` by thirty-three points, and both inside the 0.6358 to 0.6525 that Run 34's file records ten readings across Runs 29 to 33 spanning --- a span carried from that file and not re-derived here.

**The two standing placement controls are still gone with the prune, the straddlers stand at EIGHT on each half, and this pair moves tracked fill copies as a whole compiler does.** Within the pair `./loop-offsets.py run36-gheadnospec run36-gheadtwopass` puts the tracked six-copy group at **[18, 0, 0, 0, 9, 2]** on the basis and **[18, 0, 7, 7, 9, 26]** on the control, and where the basis carries that group beside a two-copy one at [0, 0], the control carries a three-copy group at [0, 0, 0] and a two-copy one at [4, 4]; the basis holds 28 self-loops of 28 B in 21 distinct byte-sequences and the control 31 in 22. So two of `-O2`'s passes displace fill copies as a compiler change and an optimisation level do, which is what `--library` says over the whole library too: 809 self-loops in both, **4.3%** at the same offset in line and 46.5% in the same straddle state. **Against the previous build of the basis's own recipe, Run 35's HEAD half, `--delta` reads EVERY mod-64 offset preserved on both groups** --- [18, 0, 0, 0, 9, 2] and [0, 0] --- with no address surviving to the byte and three displacements on the six-copy group and two on the other, so six weeks of GHC HEAD moved every copy and no head's offset. **And the exit spans astride are ZERO on both halves**, as `LOOP_EXITSPAN=1` owes; post-run step 0's naming, taken off the binaries that were timed, puts the same eight bodies at the same eight mod-64 offsets on each half --- 42, 42, 19, 49, 45, 42, 19 and 29 in address order --- so the two passes moved no straddling loop across a cache line either.

**The run's one anomaly is a SINGLE CELL, and it is worth 2.31 points of `list`'s headline.** On the basis half `list` on `stretch-coprime-r7` reads a net slope of 1.5371e-03 s at a criterion CI of 10.07% and an R2 of **0.9395** --- the main set's only cell under 0.99, four more sitting on `flip`'s basis --- while its two A/A copies, on that shape and in that same process, read 1.1012e-03 and 1.1036e-03 at CIs of 0.38% and 0.26% and R2 0.9999 apiece. So the ORIGINAL is the wild one: its own duplicates agree with each other to 0.22 of a point and it stands 39% above them, which is the **28.36%** the floor paragraph above refuses to call a floor. The control half's three cells are clean and agree, at 8.4099e-04, 8.4006e-04 and 8.4429e-04. **It is a wild cell and not an intrusion**, by the distinction [the floor section][floor] draws: `--wild` over all 119 logs this run wrote finds no bench at 0.25 foreign, so nothing else was on the machine while it was timed. **Nor is it a ramp**, which is the other thing a low R2 means here: [README's ramp section][ramp] reads a row under 0.99 as a couple of percent OPTIMISTIC, and this cell reads 39% SLOW against its own copies, so the rule that usually explains an R2 this low points the other way and by an order of magnitude. **What it costs is one figure and not the run**: `--exclude-shape stretch-coprime-r7` puts `list` at **1.3129** over the remaining eighteen shapes where all nineteen give 1.3360, and on those eighteen the whole `list` family agrees --- 1.3129 with its copies at 1.3106 and 1.3114 --- where over nineteen the original stands 2.5 points clear of copies that share its code. Every other arm of the table moves by under a point between the two readings, `bq-expand-aa-adjacent` furthest at 0.57. The registration's own spans are read over the nineteen, as they were registered; where that changes what an item says, [the item says so](#what-this-run-was-built-to-answer-and-what-it-answered).


## What the next run compares against

**No pair is ruled for Run 37 yet, and what this run leaves as the reference is `run36-gheadnospec`**, the unflagged half whose column stands below: GHC HEAD `10.1.20260918` through `cabal.project.ghead`, `Main.hs` at `0eda736`, the shim at `f31bd1c` under the four switches with the exit span, every process launched from `hugebin/`, at plain `-O1`, which is the regime `Data/Array/Internal.hs` compiles under. **It is the first published basis on that compiler**, so a next run keeping the recipe gets the like-for-like cross-run reading this one could not have --- and the step behind it is already priced here: against `run35-gheadexit`, the same recipe on the HEAD of 2026-08-03, every one of the sixteen timed arms reads within 1.02 points of 1, 0.9898 to 1.0099, at a `--bridge` geomean of 0.9890 with none outside the 3.3% drift band. **The pair declared on 2026-09-15 and deferred by Runs 33, 34 and 35 is the one that ran here and does not want repeating**: the two `-O2` passes together against neither, on one compiler, one source, one shim, one roster and one bench order. **What it leaves unasked is the split**, which its own outcome makes the candidate for the next pair: this run priced `-fspec-constr` and `-fliberate-case` TOGETHER and read them at 1.3360 on `list` where the whole `-O2` level was worth 1.2974, so the two passes overshoot the level they belong to; the single-pass readings that would say which of them carries it are Runs 29's and 30's, taken on ghc-9.12.4 and on a roster three sources back, and no reading of either pass alone exists on this compiler. Either half of this pair against the unflagged one, on the recipe above, would supply it at one variable and one term. That is a candidate and not a ruling: the pair, the level and the switch are the owner's to settle before a preparation writes a note. The two recipes this run built, spelled out as a pair note wants them:

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

`LOOP_MAXSKIP` and `LOOP_LOOKTHROUGH` are inert under the dead-spot form and stay on both lines so that the lines differ in the regime flags alone; `LOOP_ENTRIES`, `LOOP_BLOCKRULES`, `LOOP_PIN` and `LOOP_TRACE` are unset on both. Every build wants `-fforce-recomp` and a fresh `--builddir`, the switches being an environment change cabal does not see, and every driver takes its half from `hugebin/` through `half-bin.sh`, as this run's did. Under the exit span `loop-offsets.py --survey` reads 0 exit spans astride off a timed binary, as it did on both of this run's halves, so the preparation's legs 10a and 10b stop on anything else. **It was the pair Run 31's arithmetic wanted and no run since could supply, and it has now been supplied.** Run 31 read `-O2` worth **1.2974** on `list` where `-fspec-constr` and `-fliberate-case`, measured one at a time on Runs 29 and 30, multiply to **1.3325** --- a 3.51-point overshoot that is either the level's other passes handing `list` back or an artefact of composing two runs' readings. This pair reads the two together at **1.3360** over the nineteen main-set shapes, which is 0.35 of a point ABOVE the composition and 3.86 above the level, and at **1.3129** with the one wild shape of the anomaly paragraph excluded, which sits BETWEEN the two accounts --- 1.55 points above the level and 1.96 under the composition. **On `bq-expand`, where the two accounts agree to a quarter of a point, the pair confirms both**: 1.2980 read against 1.2943 from the level and 1.2967 from the composition. So the composition is not an artefact, the level's other passes do hand `list` back, and how much of it they hand back is the figure the wild cell blurs: somewhere between one and a half and four points, which one clean rerun of the main set on these same two binaries would settle.

**The COMPILER variable was not this run's to vary --- both halves are one in-tree stage1, `10.1.20260918` --- and the run reads a step of it anyway, one nobody had taken.** The tally of pairs BUILT to ask it stands where Run 35 left it, at TEN. What the series has of it is Runs 19 and 24 to 28, all with `-fspec-constr` on BOTH halves, then Run 32 at plain -O1 with the cleanest null of them (arm geomean 0.9985), Run 33 under the exit span with a gap (1.0068), Run 34 asked from `hugebin/` and back near the null (1.0048), and Run 35 on a moved source at 1.0044. **What this run adds to it is one step nobody had measured, and it is a null**: `run36-gheadnospec` against `run35-gheadexit`, the same recipe six weeks apart on the same compiler line, reads every one of the sixteen timed arms within 1.02 points of 1 --- 0.9898 to 1.0099, `--bridge` geomean 0.9890, none outside the drift band --- and `--delta` finds every mod-64 offset of both tracked fill groups preserved across the rebuild. **The REGIME variable has now been asked FOUR times, and this run is the one that closes its arithmetic.** Put in one orientation, the unflagged half over the flagged, Runs 29, 30 and 31 read `list` at **1.1379**, **1.1710** and **1.2974** and `bq-expand` at **1.2804**, **1.0127** and **1.2943**, all three on ghc-9.12.4; this run reads the two passes together on GHC HEAD at **1.3360** on `list` and **1.2980** on `bq-expand`. On `bq-expand` the single-pass pair multiplies to 1.2967 against Run 31's measured 1.2943, 0.19% apart, and this run lands between them --- three accounts inside four tenths of a point, across two compilers. On `list` they multiply to 1.3325 against Run 31's 1.2974, 3.51 points apart, and this run lands on the composition's side of that gap. The cross-compiler term the reading carries is bounded rather than assumed: the -O1 baseline moved 0.77 of a point from ghc-9.12.4 to the HEAD of 2026-08-03, by `run35-exit` against `run35-gheadexit`, and under a point from that HEAD to this one.

**What Run 36 leaves the next run to read against, and the first item is a check that did NOT fire. The box is where Runs 28 to 35 left it**, and this run's gate says so: read against the fingerprint Run 35 installed, which this run's note rules is its own comparison, the machine check puts `list`'s net at **-0.23%**, worst `stretch-square-1341` at +1.63%, 0 of 19 shapes past 5% and the geomean inside the 3% bar. **And this reading is NOT like-for-like**, which the pair note ruled before the run rather than leaving to be discovered: Run 35's published half is `run35-exit`, a ghc-9.12.4 build, where this basis is a GHC HEAD of 2026-09-18, so the check carries a COMPILER term of two steps beside the box. What a net inside the bars therefore says is that the box and both steps TOGETHER sum to less than the bar, and not that the box has not moved. **Both steps are now bounded**, which is what this run adds: `run35-exit` against `run35-gheadexit` reads `list` at 0.9923, so 9.12.4 to the HEAD of 2026-08-03 is 0.77 of a point, and `run35-gheadexit` against this basis puts every one of the sixteen timed arms within 1.02 points of 1, `list` at 1.0099. So this run publishes INSIDE the third machine era rather than opening a fourth, and the fingerprint below is this run's own, which the next run's machine check reads. **What a Run 37 reading may take from those sixteen arms that this one could not take from Run 35's basis is a like-for-like check**: this basis is the FIRST published one on this compiler, so a next run keeping the recipe compares against it with the box as the only term.

**Registered with the pair.** Run 36's four registrations, their kill conditions and their verdicts are [in this file's last section](#what-this-run-was-built-to-answer-and-what-it-answered), and the commands that produced them were the pair note's, which goes with the binaries and is offered for deletion with them. ONE item is killed and THREE hold their sentences, over 20 spans of which 15 held and 5 were killed. **What a next registration should take from this one is that bands drawn from ONE prior figure die together and say one thing between them**: item (1) set its band on Run 31's `-O2` level reading of `list` and asked whether the two passes reach it, which they do not --- that is the item doing its work --- and then items (3) and (4) set four more bands on that same reading and its per-arm siblings, so when the first missed, `list-aa-adjacent` and `list-aa-distant` missed with it, in the same direction and by the same order of magnitude. Item (4)'s two are NOT an echo of it: its bands come off Run 31's counts SWEEPS rather than its times, and they miss in opposite directions from each other, `list` 1.94 points under and `bq-expand` 6.40 over. So two of the five kills are item (1) counted again and the other two price the counted work's size. Either derive a family's bands from the item that carries the family and read them as one span, or say in the registration which spans are downstream of which, so a tally does not read four echoes as four results.

What this section stands on --- the rulings on the position term, the allocation area, a change of basis and a pair's two halves, which of its tables are edited by hand, and why the fingerprint is kept --- is [README's *Reading a run file*](../README.md#reading-a-run-file).

**The next run compares against Run 36**, whose halves were launched from `hugebin/` and whose basis carries `LOOP_EXITSPAN=1` at plain -O1 on the in-tree stage1 `10.1.20260918`; a run keeping that recipe reads against this basis within the switch, as this run read `run35-gheadexit` within it. Each run's figures and the names of its halves are in its own file, `runs/run<N>.md`, back-filled to Run 7 on 2026-08-29; a comparison reaching further back is a chain of one-step comparisons, each recorded by the run that made it, and walking that chain here is what this section stopped doing. **The step this run records is NOT basis to basis**: Run 35 published its ghc-9.12.4 half and this run publishes a HEAD one, so those two columns carry a compiler term and are not a subtraction. What this run records instead is against the half Run 35 built by this basis's own recipe, `run35-gheadexit` --- **one term, six weeks of GHC HEAD with its rebuilt dependency stack** --- and over the **16 arms both rosters time and both give a corrected time** it runs from **0.9898** on `lib-stage2-lean-u1` to **1.0099** on `list`, below 1 meaning this run is the faster, ALL SIXTEEN within 1.02 points of 1. **The table below is this run's own two halves and no earlier run's**, seven strategies over the nineteen main-set shapes, the emphasised column being the basis and so this run's published one, and the two differing in TWO GHC FLAGS and in nothing else. Its two columns may NOT be differenced, `list` having moved 33.60 points between them, so the table is two orderings read side by side.
| strategy | Run 36 (plain -O1, dead-spot, exit span, -A32m, HEAD 10.1.20260918) | Run 36 (that recipe plus `-fspec-constr -fliberate-case`) |
|---|---:|---:|
| `mut-odo-vecdims` | **0.044** | 0.058 |
| `mut-odo-vecdims-add-in-leaf-u1` | **0.029** | 0.035 |
| `mut-odo-vecdims-add-in-leaf-u2` | **0.028** | 0.032 |
| `lib-stage1` | **0.028** | 0.032 |
| `lib-stage2-lean` | **0.027** | 0.031 |
| `lib-stage2-lean-u1` | **0.028** | 0.032 |
| `bq-expand` | **0.125** | 0.129 |

**READ THE SECOND COLUMN AS A RATIO AND NOT AS A SPEED, and this run it is not even an ordering of speeds.** Every entry is that arm's net over `list`'s net in ITS OWN half, and `list` moved **33.60 points** between the halves --- forty-eight times the 0.7% bar --- so the control column reading HIGHER on every row is the denominator having shrunk under it and not one arm of it having slowed. In absolute terms the flagged half is the faster on fifteen of the sixteen timed arms, `lib-stage2-lean-u1` at 0.9920 the one exception; the column cannot say so, and is not asked to. **And it is not an identity either**: each entry is winsorized per row within its own half, so dividing an arm's two entries does not reproduce its `--compare` figure over `list`'s. On `lib-stage2-lean` the two unrounded published entries, **0.02672** and **0.03088**, divide to 0.865, where the two PLAIN per-shape geomeans, 0.02741 and 0.03659, divide to **0.7491** --- which is exactly the arm's cross-half figure over `list`'s, 1.0008 over 1.3360. The capping is the whole of the difference: three of that row's nineteen cells capped on the basis and four on the control, whose published figure sits 15.6 points under its plain one. The arm-by-arm reading of what the two passes are worth is in the head, off `--compare`, where the reference is not divided out.

**A published geomean is over the same 19 shapes, and two halves of one run usually share a denominator too**, `list` moving under 0.7% between them --- so such a pair may be subtracted and not merely ordered. **THE TABLE ABOVE IS NOT SUCH A PAIR, and it misses by more than Run 31's did**: `list` moved **33.60 points** between these halves where Run 31's whole `-O2` level moved it 29.74, so the two columns are read side by side as orderings and never differenced. **They print far apart on every row, the control higher on all seven** --- `mut-odo-vecdims` 0.044 against 0.058, `mut-odo-vecdims-add-in-leaf-u1` 0.029 against 0.035, the shipped leaf 0.028 against 0.032, `lib-stage1` 0.028 against 0.032, `lib-stage2-lean` 0.027 against 0.031, `lib-stage2-lean-u1` 0.028 against 0.032 and `bq-expand` 0.125 against 0.129 --- and read DOWN a column the head and the foot are the same on both, `lib-stage2-lean` leading each and `bq-expand` at the foot of each. **Those gaps are the moved denominator and the winsorizing together, in that order**: `lib-stage2-lean`'s plain per-shape geomeans are 0.02741 and 0.03659, 33.5 points apart where the published figures part by 15.6, the cap touching three of its cells on the basis and four on the control.

**The control half's own standings on the arms this run's roster carries, which no table here holds, every published table being the basis half's.** Read off the control half's main-set process with `--pair`, paired geomeans over all 19 main-set shapes, with the basis half's reading in brackets: `mut-odo-vecdims-add-in-leaf-u2` against `-u1` **0.9465** (0.9509) and against `mut-odo-vecdims` **0.6382** (0.6381); `lib-stage1` against `-u2` **1.0410** (1.0367); `lib-stage2-lean` against `-u2` **0.9806** (0.9737) and against `lib-stage1` **0.9419** (0.9392); and the headline pair README's opening leads with, `bq-expand` against `mut-odo-vecdims`, **2.1990** (2.8311), 0 of 19 shapes either way. **All five hold their direction across the halves and none moves by a point**, the widest 0.69 of one: the lean fill is ahead of the shipped leaf on both, by 2.6 points on the basis and 1.9 on the control, and ahead of `lib-stage1` by 6.1 and 5.8. **The ordering Run 35 saw change sides does not change here**: `mut-odo-vecdims-add-in-leaf-u1` against `lib-stage1` reads **1.0144** on the basis and **1.0148** on the control, four ten-thousandths apart and on one side of 1, where Run 35 read 0.9781 and 1.0042. **What the two passes do move is which arm a class bolds**: four of the ten name a different one on the two halves --- `rev`, `lib-stage1` on the basis against `lib-stage2-lean` on the control, and `bcastmid`, `lib-stage2-lean-u1` against `lib-stage2-lean`, both within the outside-the-family column; and `scaled` and `small`, which change COLUMN, the family's ceiling leading `scaled` on the basis and the arm outside it on the control, and the reverse on `small`.

**Each stride class has its own table below.** Run 8 re-ran every class with the populations pinned, and every run since has again, so each class's paragraph carries what the last change moved and the table above it is what the next run reads against. **A class figure compared across the Run 11/Run 12 boundary is not compared on one build**: Run 11's class tables are its *aligned* half's and Run 12's its *max-skip* basis half's, and the main set prices that difference at nothing below 0.99 and up to 1.06, so a point or two of movement across that boundary is the shim rather than the class. From Run 13 on, every run's class tables are its own basis half's, Run 34's included.

| shape | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---:|---:|---:|---:|---|---|
| `cnn-slice-c32` | 3 | 288 | 6.32 us | 0.078 | `lib-stage2-lean` 0.075 | `mut-odo-vecdims-add-in-leaf-u2` 0.056 |
| `cnn-L1-6x6-c1` | 3 | 324 | 7.59 us | 0.090 | `lib-stage2-lean` 0.067 | `mut-odo-vecdims-add-in-leaf-u1` 0.070 |
| `cnn-L1-24x24-c1` | 3 | 5184 | 119 us | 0.065 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u2` 0.042 |
| `lenet-L1-28-c1-k5` | 5 | 19600 | 386 us | 0.044 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `gather48-src-50` | 3 | 22500 | 463 us | 0.047 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-coprime-r7` | 13 | 60060 | 1.54 ms | 0.021 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `cnn-L2-24x24-c32` | 3 | 165888 | 3.71 ms | 0.052 | `lib-stage2-lean` 0.028 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `stretch-primes` | 89 | 250357 | 4.41 ms | 0.025 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `alexnet-L2-27-c48-k5` | 5 | 874800 | 17 ms | 0.039 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `vgg-14-c512-k3` | 3 | 903168 | 19.7 ms | 0.053 | `lib-stage1` 0.029 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `alexnet-L1-55-c3-k11` | 11 | 1098075 | 19.7 ms | 0.031 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `stretch-inner256` | 256 | 1750784 | 44.7 ms | 0.023 | `lib-stage2-lean-u1` 0.019 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `stretch-pow2stride` | 64 | 1769472 | 31.4 ms | 0.111 | `lib-stage2-lean-u1` 0.110 | `mut-odo-vecdims-add-in-leaf-u1` 0.110 |
| `stretch-r5-8x432` | 8 | 1769472 | 47.5 ms | 0.022 | `lib-stage1` 0.015 | `mut-odo-vecdims-add-in-leaf-u2` 0.015 |
| `stretch-square-1341` | 1341 | 1798281 | 31.4 ms | 0.088 | `lib-stage2-lean` 0.077 | `mut-odo-vecdims-add-in-leaf-u2` 0.076 |
| `stretch-bigstride` | 3 | 1800000 | 51 ms | 0.032 | `lib-stage1` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `stretch-tab7MB` | 2 | 1800000 | 41 ms | 0.057 | `lib-stage2-lean-u1` 0.021 | `mut-odo-vecdims-add-in-leaf-u1` 0.022 |
| `stretch-tall-Mx2` | 900000 | 1800000 | 40.9 ms | 0.021 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims` 0.021 |
| `stretch-wide-2xM` | 2 | 1800000 | 39.6 ms | 0.057 | `lib-stage2-lean-u1` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |

| shape | class | `sInner` | `l` | `list`, net | mut-odo-vecdims | best outside family | ceiling |
|---|---|---:|---:|---:|---:|---|---|
| `bcast-inner8` | `bcast` | 8 | 51200 | 932 us | 0.029 | `lib-stage2-lean` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcast-src512` | `bcast` | 3515 | 1799680 | 29.1 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-inner900` | `bcast` | 900 | 1800000 | 29.7 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src64` | `bcast` | 28125 | 1800000 | 29.1 ms | 0.019 | `lib-stage1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `bcast-src8` | `bcast` | 225000 | 1800000 | 35 ms | 0.016 | `lib-stage1` 0.013 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcast-tall-Mx2` | `bcast` | 2 | 1800000 | 39.3 ms | 0.057 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u1` 0.020 |
| `bcastmid-c32-cnn` | `bcastmid` | 3 | 165888 | 3.62 ms | 0.053 | `lib-stage2-lean` 0.011 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `bcastmid-primes` | `bcastmid` | 97 | 250357 | 4.22 ms | 0.019 | `lib-stage2-lean-u1` 0.012 | `mut-odo-vecdims` 0.019 |
| `bcastmid-b200k` | `bcastmid` | 3 | 1800000 | 47.3 ms | 0.034 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `bcastmid-block150k` | `bcastmid` | 300 | 1800000 | 42.2 ms | 0.022 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u1` 0.019 |
| `block-run64-gap1` | `block` | 64 | 131072 | 2.21 ms | 0.019 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `block-run64-gap64` | `block` | 64 | 131072 | 2.25 ms | 0.024 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `block-run64-off7` | `block` | 64 | 131072 | 2.24 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `block-run64-page` | `block` | 64 | 131072 | 2.32 ms | 0.029 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `block-r3-vol64` | `block` | 64 | 262144 | 4.44 ms | 0.020 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.019 |
| `compose-rev-bcast` | `compose` | 8 | 51200 | 942 us | 0.029 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-slice-bcast` | `compose` | 8 | 51200 | 942 us | 0.029 | `lib-stage2-lean` 0.014 | `mut-odo-vecdims-add-in-leaf-u2` 0.014 |
| `compose-scalar` | `compose` | 1500 | 1800000 | 29.6 ms | 0.019 | `lib-stage2-lean` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `compose-zero-mid` | `compose` | 100 | 1800000 | 30.2 ms | 0.019 | `lib-stage2-lean-u1` 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 |
| `flip-inner-gap64` | `flip` | 64 | 131072 | 2.35 ms | 0.026 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-outer-gap64` | `flip` | 64 | 131072 | 2.34 ms | 0.025 | `lib-stage2-lean` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `flip-last-c32` | `flip` | 3 | 165888 | 3.68 ms | 0.052 | `lib-stage2-lean` 0.017 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `flip-whole-square` | `flip` | 1341 | 1798281 | 29.1 ms | 0.024 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims` 0.024 |
| `flip-fwd-rows96` | `flip` | 96 | 1800000 | 29.9 ms | 0.024 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims` 0.024 |
| `flip-last-rows` | `flip` | 96 | 1800000 | 32.5 ms | 0.040 | `lib-stage1` 0.043 | `mut-odo-vecdims` 0.040 |
| `rev-cnn-L1-24x24-c1` | `rev` | 3 | 5184 | 119 us | 0.064 | `lib-stage2-lean` 0.030 | `mut-odo-vecdims-add-in-leaf-u2` 0.041 |
| `rev-gather48-src-50` | `rev` | 3 | 22500 | 465 us | 0.047 | `lib-stage2-lean` 0.019 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `rev-primes` | `rev` | 89 | 250357 | 4.48 ms | 0.024 | `lib-stage2-lean` 0.020 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 |
| `runs-65536` | `runs` | 65536 | 1769472 | 27.9 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-16384` | `runs` | 16384 | 1785856 | 28.2 ms | 0.024 | `lib-stage1` 0.023 | `mut-odo-vecdims` 0.024 |
| `runs-4096` | `runs` | 4096 | 1798144 | 28.4 ms | 0.024 | `lib-stage1` 0.024 | `mut-odo-vecdims` 0.024 |
| `runs-1024` | `runs` | 1024 | 1799168 | 28.5 ms | 0.024 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.024 |
| `runs-512` | `runs` | 512 | 1799680 | 28.7 ms | 0.024 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.024 |
| `runs-256` | `runs` | 256 | 1799936 | 28.7 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-7` | `runs` | 7 | 1799994 | 32.3 ms | 0.033 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-2` | `runs` | 2 | 1800000 | 40 ms | 0.057 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.024 |
| `runs-3` | `runs` | 3 | 1800000 | 36.1 ms | 0.047 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-32` | `runs` | 32 | 1800000 | 29.7 ms | 0.025 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.024 |
| `runs-4` | `runs` | 4 | 1800000 | 33.8 ms | 0.041 | `lib-stage2-lean-u1` 0.024 | `mut-odo-vecdims-add-in-leaf-u1` 0.024 |
| `runs-48` | `runs` | 48 | 1800000 | 29.1 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `runs-5` | `runs` | 5 | 1800000 | 32.9 ms | 0.039 | `lib-stage2-lean` 0.024 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-64` | `runs` | 64 | 1800000 | 29.3 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-9` | `runs` | 9 | 1800000 | 31.4 ms | 0.030 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.023 |
| `runs-96` | `runs` | 96 | 1800000 | 29 ms | 0.025 | `lib-stage2-lean` 0.025 | `mut-odo-vecdims` 0.025 |
| `runs-r3-48x30` | `runs` | 1440 | 1800000 | 29 ms | 0.028 | `lib-stage1` 0.025 | `mut-odo-vecdims-add-in-leaf-u2` 0.025 |
| `scaled-r5` | `scaled` | 13 | 15015 | 265 us | 0.029 | `lib-stage2-lean` 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-super-r3` | `scaled` | 30 | 60000 | 1.04 ms | 0.023 | `lib-stage1` 0.022 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 |
| `scaled-rank1-m1` | `scaled` | 300000 | 300000 | 5.11 ms | 0.028 | `lib-stage2-lean` 0.031 | `mut-odo-vecdims` 0.028 |
| `small-patch-k5` | `small` | 5 | 150 | 2.94 us | 0.077 | `lib-stage2-lean` 0.097 | `mut-odo-vecdims-add-in-leaf-u1` 0.061 |
| `small-bcast32` | `small` | 32 | 256 | 4.4 us | 0.050 | `lib-stage2-lean` 0.065 | `mut-odo-vecdims-add-in-leaf-u2` 0.045 |
| `small-flat64` | `small` | 64 | 256 | 4.37 us | 0.058 | `lib-stage2-lean` 0.015 | `mut-odo-vecdims` 0.058 |
| `small-patch-r5` | `small` | 4 | 256 | 5.27 us | 0.088 | `lib-stage2-lean-u1` 0.094 | `mut-odo-vecdims-add-in-leaf-u1` 0.069 |
| `small-row96` | `small` | 96 | 384 | 6.43 us | 0.041 | `lib-stage2-lean` 0.055 | `mut-odo-vecdims` 0.041 |
| `window-28x28-k5` | `window` | 5 | 14400 | 277 us | 0.040 | `lib-stage2-lean` 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.022 |
| `window-64x64-k1x9` | `window` | 1 | 32256 | 942 us | 0.086 | `lib-stage2-lean` 0.010 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 |
| `window-224x224-k3-s2` | `window` | 3 | 110889 | 2.42 ms | 0.052 | `lib-stage1` 0.029 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-224x224-k3-d2` | `window` | 3 | 435600 | 9.63 ms | 0.051 | `lib-stage1` 0.028 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-224x224-k3` | `window` | 3 | 443556 | 9.73 ms | 0.051 | `lib-stage2-lean` 0.028 | `mut-odo-vecdims-add-in-leaf-u2` 0.028 |
| `window-32x32-c64-k3` | `window` | 3 | 518400 | 11.6 ms | 0.052 | `lib-stage2-lean` 0.029 | `mut-odo-vecdims-add-in-leaf-u2` 0.029 |
| `window-64x64-c16-k3` | `window` | 3 | 553536 | 12.4 ms | 0.053 | `lib-stage1` 0.030 | `mut-odo-vecdims-add-in-leaf-u2` 0.030 |
| `window-128x128-k7` | `window` | 7 | 729316 | 13.8 ms | 0.031 | `lib-stage1` 0.018 | `mut-odo-vecdims-add-in-leaf-u2` 0.018 |

**No row of the table is read over fewer shapes than the rest, which is a property of the shape set and not of any arm**: NONE of the thirty-five rows is a geomean over fewer shapes than the rest, as on Runs 32 to 35 and where nine of Run 27's thirty-five were. Not one cell on either half sinks below the shared forcing term, so every row of both columns that carries a corrected time covers all nineteen shapes and no span in this file is recorded NOT READ for want of a population. Two changes did it, and neither is a measurement: the ruling of 2026-09-10 that a reducing consumer has no corrected time --- it hands back a scalar and never runs the pass being subtracted, so the FIFTEEN `-sum` rows read `--` in `time` and `worst` rather than a ratio of two near-zero numbers --- and the retirement of every Fill arm over a list, which took the rest. **What it costs is one column's comparability**: `best outside family` can no longer name a `-sum` arm, so where Run 27's cross-class summary named a `-sum` consumer on seven of its ten rows, this one names `lib-stage2-lean` on SEVEN, `lib-stage1` on two --- `rev` and `scaled` --- and `lib-stage2-lean-u1` on one, `bcastmid`, where Run 35 named the lean fill on six, `lib-stage1` on three and the unrolling twin on `small`. The cross-class summary's `best outside family` column --- the one far below, not the fingerprint's just above --- is not to be read across the two runs.


## The properties the next run should test

**Each stride class carries the same three properties, now with Run 36's verdicts** over ten classes, the details beside each class's table. **Two held everywhere and the third broke a clause for the first time**, and what broke it is the pair's own variable rather than anything about an arm: the two `-O2` passes change what `list` and `bq-expand` allocate.

1. **`mut-odo-vecdims`'s `worst` stays under 1, and `mut-odo-vecdims` is ahead of `bq-expand` on every shape.** **Both clauses held in every one of the eleven populations on both halves**, where Run 35's second clause broke on the main set's CONTROL half and Run 34's on one half too: here `mut-odo-vecdims` is ahead of `bq-expand` over 19 of 19 main-set shapes on each, closest at `stretch-pow2stride` at **0.9970** on the basis and **0.9826** on the control, which is the shape and the arm pair Run 35 read at 1.0030. So the margin Run 35 lost by three tenths of a point this run keeps by three tenths on the basis and by 1.7 points on the control, the two passes having been worth more to the fill than to `bq-expand` on that one shape where over the population they are worth far more to `bq-expand`. The `worst` clause holds in every regime, roster, compiler and layout the README has run, this pair's flagged half included, so `mut-odo-vecdims` --- and this is a statement about THAT arm and not about the route the library ships, which the paragraph below reads separately --- was never slower than the `list` it replaced, on any shape of any population. The `bq-expand` clause folded in on 2026-09-06 from the ordering that was property 2 until then, strengthened from a geomean to every shape, and is read that way here for the ninth time.

Beside property 1, and the case has simplified twice --- the prune of 2026-09-04 parked the arm that used to be half of it, and the retirement of 2026-09-09 took four of the five arms that broke the rest: **exactly ONE arm still breaks the WIDER statement this class set is really read for --- that no arm the library would ship is slower than `list` on any shape --- and it is the route the library ships.** `lib-stage1` is slower than `list` on `runs-2` on both halves, at **1.0978** on the basis and **1.3495** on the control, and on `runs-3` on the CONTROL half alone at **1.1348**; `--over-list` reads every other one of the 1120 timed non-control cells this run carries, over all eleven populations on both halves, at or under 1. **What is new is that the two passes make its excess over `list` three and a half times what it is without them, and give it a second cell --- and it is `list` moving and not `lib-stage1`**: on `runs-2` the fill's own net moves 1.0341 between the halves on counts of 1.0274, while `list` moves 1.2712, so the ratio parts by 25 points where Run 35's two readings of the same cell parted by 1.6; and `runs-3`, which Run 35 put at or under 1 on both of its halves, sits at 1.1348 once the passes are on, `lib-stage1` there moving 1.0283 against `list`'s 1.2805. So the one standing break of the wider statement is not merely still there, it is wider under the passes than without them, and it sits on the two shortest runs of the class that exists to price short runs.

2. **`mut-odo-vecdims` allocates at most 1% over `list` and over `bq-expand` on every shape** --- property 1's two inequalities in allocation with a 1% margin, on the `alloc` multiple each cell carries, registered strict on 2026-09-06 and given the margin on 2026-09-07 at its first reading: by `--block` per class and by the default mode on the main set, each clause printed with its closest shape. **Both clauses hold in every one of the eleven populations on both halves, the sixth run running that this property is the one left entirely alone.** The `list` clause is closest at `small-flat64` on the control, **0.06524**, and every closest shape outside `small` sits under 0.053. The `bq-expand` clause is closest at `small-row96` on the CONTROL half, **1.00441**, then `scaled-rank1-m1` at 1.00003 on the basis and `bcast-src8` at 1.00000 on the control --- and that first figure sits four tenths of a point inside a margin of one, where Run 35's closest sat three thousandths of a point inside it. **The two passes are what moved it**: `small-row96` reads 0.98216 on the basis and 1.00441 on the control, so the clause survives on the flagged half by less than half the margin, and it is the allocation change property 3 records that put it there.

3. **The allocation tiers survive and their ORDER is unbroken in all ten classes and on the main set, on both halves --- and their LEVEL clause BREAKS in every one of the eleven populations, as it did on Run 31, whose registration (10) died on it.** The order clause is untouched: the mutable fills sit at the result vector, `bq-expand` between 1.00x and 3.86x it, `list` an order of magnitude above at 19.00x to 27.66x, on both halves and in every population, `small` outside the LEVEL clause by the ruling of 2026-09-07 as before. What breaks is the clause Run 35 read as holding cell for cell: **the two passes change what `list` and `bq-expand` ALLOCATE, and they change it by exactly what the whole `-O2` level changed it by.** Run 31's flagged half read `bq-expand` at 2.11x and `list` at 23.45x on the main set and 1.00x to 2.75x and 19.00x to 26.55x across the classes; this run's flagged half reads the same five figures, on a different compiler, from two of that level's passes. On the main set the fills read 1.00x on both halves while `bq-expand` reads **2.78x** on the basis and **2.11x** on the control and `list` **25.20x** and **23.45x** --- medians over the nineteen shapes, so they are not to be divided. **Read per cell, which is the reading that may be**: over those nineteen shapes the flagged half allocates **0.9342** of the basis on `list` and identically on both its A/A twins, and **0.8119** on `bq-expand` and identically on all three of its, while every other timed arm of the main set reads 1.0000 to within two tenths of a point. Over all eleven populations `list` runs from 0.9073 on `block` to 0.9342 on the main set and `bq-expand` from **0.7263** on `window` to 0.9705 on `block`. **ONE arm outside the two families moves, the same way and less far**: `liblist-stage2-sum`, a reducing consumer, allocates **0.9096** of the basis on `block`, 0.9100 on `runs`, 0.9688 on `flip`, 0.9884 on `window` and 0.9901 on `small`, and 1.0000 on the other six, the main set among them --- a geomean deviation of 2.18% over the eleven populations against `list`'s 7.89% and `bq-expand`'s 12.52%, so between a sixth and a third of what the families get, though the same size as theirs on the two populations where it moves most. `--alloc` puts 468 of the main set's 627 allocating cells inside 1e-4 between the halves, worst **3.33e-01** on `stretch-wide-2xM/bq-expand-nosum`, with the 32 cells under 100 bytes a call set aside as a property of fitting a near-zero allocation. Allocation is deterministic per call, so a level that moves is a code change and never a slot --- and here the code change is named before the reading: two of `-O2`'s passes, on the two families whose time they move and, by between a sixth and a third of what those get, on one reducing consumer besides.

`--pair` within a class JSON, the `needs` column's two class-method tiers and the equal weighting of shapes are [README's *Reading a run file*](../README.md#reading-a-run-file).


## The stride classes, run by run

**Run 36 (GHC HEAD `10.1.20260918` against itself, plain -O1 against -O1 with `-fspec-constr -fliberate-case`, dead-spot, exit span, -A32m, launched from `hugebin/`) records every class twice**, one process per class per half, so each block below has a control-half twin and the cross-half line under it is derived from both. `list` moved between the halves by 24.97 points on `bcastmid` at narrowest and 37.98 on `bcast` at widest, so NONE of the ten classes sits inside the 0.7% that lets two columns be differenced and every cross-half reading below is an ordering of the pair's variable rather than a measurement of it --- as on Run 31, the only other pair whose variable was a level, and where Run 35 could difference seven of the ten and Run 34 eight. Over the ten classes the reader counts **160 arm-comparisons, 47 putting the basis faster and 113 slower**, with no degenerate arm excluded, at geomeans from **1.0598** on `block` to **1.1368** on `window` and extremes of `lib-stage2-lean-u1` at **0.9418** on `rev` and `bq-expand-aa-distant` at **1.5306** on `window` --- the low extreme being that same arm in three of the ten populations, and neither extreme the code: the flagged half's counts move with it on one and not on the other, which each block reads. Every `Across the halves` line below reads the basis over the control, ABOVE 1 meaning the control --- the FLAGGED half --- is the faster, as every cross figure in this file does. What each class still decides, and decides on both halves separately, is the three properties, its own floor, and whichever registrations name it. **No registration of this run names a class**: all twenty of its spans are `on main basis`, so each block below carries its properties, its floor and its own cross-half reading, and the registration verdicts are the main set's alone.

First, one table over all of them, transcribed from each class's own table below, in the columns [README's *Reading a run file*](../README.md#reading-a-run-file) fixes, which also says what the blocks under it carry and what installs them.

`mut-odo-vecdims` and `worst` are that arm's two columns in that class's table; *best outside family* is the leading arm outside the vecdims family, what the dropped stride-conditioned redirect would have taken, and *ceiling* the leading arm OF the family, each with its name --- and both are read over the POPULATION, so the arm named here may lead on no single shape and the per-shape fingerprint below may name another, which is [the README's per-shape section][pershape]'s own point and not a disagreement --- since which arm leads is half of what the column says --- so where an arm outside the family leads, the two name different arms and the gap between them is what the lead is worth, and Run 21's table, which repeated one arm in both columns on `bcastmid` and `reshape1`, was wrong to; *floor* is the largest deviation from 1 among that process's A/A controls. A cell that breaks property 1, or that leads `mut-odo-vecdims` --- what broke the ordering that was property 2 until 2026-09-06 ([the properties](#the-properties-the-next-run-should-test)) --- is bolded. **In practice that marks the FASTER of the two named arms, one cell a row**: the arm outside the family on SIX of the ten --- `rev`, where `lib-stage1` leads, `bcastmid`, where `lib-stage2-lean-u1` does, and `bcast`, `window`, `flip` and `small`, where `lib-stage2-lean` does --- and the family's own ceiling on the other FOUR, `scaled`, `runs`, `block` and `compose`, where the ceiling is faster. **The two pointer leaves held five of Run 30's six bolded ceilings and are parked**, so every bolded ceiling here is the shipped leaf `mut-odo-vecdims-add-in-leaf-u2` itself, which is the form the family would ship. The class's own paragraph says what the bold marks; properties 2 and 3 are allocation and have no cell here.

| class | shapes | mut-odo-vecdims | worst | best outside family | ceiling | floor |
|---|---:|---:|---:|---|---|---:|
| `rev` | 3 | 0.042 | 0.064 | **`lib-stage1`** 0.021 | `mut-odo-vecdims-add-in-leaf-u2` 0.021 | 0.51% |
| `bcast` | 6 | 0.021 | 0.057 | **`lib-stage2-lean`** 0.016 | `mut-odo-vecdims-add-in-leaf-u2` 0.016 | 1.06% |
| `bcastmid` | 4 | 0.029 | 0.053 | **`lib-stage2-lean-u1`** 0.012 | `mut-odo-vecdims-add-in-leaf-u2` 0.020 | 1.36% |
| `window` | 8 | 0.051 | 0.086 | **`lib-stage2-lean`** 0.026 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 0.43% |
| `scaled` | 3 | 0.027 | 0.029 | `lib-stage1` 0.023 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.022 | 0.64% |
| `runs` | 17 | 0.027 | 0.057 | `lib-stage2-lean` 0.025 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.025 | 3.57% |
| `flip` | 6 | 0.027 | 0.052 | **`lib-stage2-lean`** 0.023 | `mut-odo-vecdims-add-in-leaf-u2` 0.027 | 1.21% |
| `block` | 5 | 0.023 | 0.029 | `lib-stage2-lean` 0.022 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.021 | 0.13% |
| `small` | 5 | 0.061 | 0.088 | **`lib-stage2-lean`** 0.055 | `mut-odo-vecdims-add-in-leaf-u2` 0.055 | 0.63% |
| `compose` | 4 | 0.024 | 0.029 | `lib-stage2-lean` 0.015 | **`mut-odo-vecdims-add-in-leaf-u2`** 0.015 | 1.11% |

The pure slot this table carried until 2026-08-22, and the paragraph that read it, retired with the pure/impure distinction when the decision shipped the mutable family's arm; the column now carries the best arm outside the family, which the table above gives per class and which is ahead of `mut-odo-vecdims` in every one of the ten --- the lead that broke the ordering property 2 carried until 2026-09-06. **On FOUR rows --- `scaled`, `runs`, `block` and `compose` --- the bold sits in the CEILING column instead**, and it names ONE arm on all four, the shipped leaf `mut-odo-vecdims-add-in-leaf-u2`; against Run 35 the rows that changed sides are `bcast` and `small`, both leaving that set for the arm outside the family, and `bcastmid` now names `lib-stage2-lean-u1` outside the family where Run 35's named `lib-stage1`. The reader's convention counts a `mut-odo-vecdims` sibling as the family's and so as no break; this file overrides it for the two pointer fills, which the dead-ideas ruling refuses as a design rather than as a form the family could ship --- an override no row here exercises, both of them having been parked on 2026-09-13. **FIVE rows tie at three decimals** --- `rev` at 0.021, `bcast` at 0.016, `runs` at 0.025, `small` at 0.055 and `compose` at 0.015 --- and the bold on each is `--block`'s own, computed on the unrounded values where the printed ones cannot separate: outside the family against the ceiling, 0.020817 against 0.021142, 0.015551 against 0.015762, 0.024617 against 0.024506, 0.055205 against 0.055401 and 0.014799 against 0.014749, so `rev`, `bcast` and `small` fall to the arm outside the family and `runs` and `compose` to the ceiling.

**`rev` --- every stride negated, offset at the top: the view `rev` on every axis builds.** Shapes: `rev-cnn-L1-24x24-c1` (`l` 5184, `sInner` 3), `rev-gather48-src-50` (`l` 22500, `sInner` 3), `rev-primes` (`l` 250357, `sInner` 89).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.11* | *127* | *3.22x* |
| liblist-stage1-sum | -- | -- | 0.09 | 147 | 1.01x |
| liblist-stage2-sum | -- | -- | 0.11 | 147 | 1.01x |
| liblist-stage3-sum | -- | -- | 0.15 | 147 | 1.01x |
| liblist-stage4-list-sum | -- | -- | 0.07 | 147 | 1.01x |
| liblist-stage4-sum | -- | -- | 0.13 | 147 | 1.01x |
| libunord-stage1-sum | -- | -- | 0.11 | 147 | 1.03x |
| libunord-stage10-list-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage10-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage11-sum | -- | -- | 0.02 | 157 | 0.01x |
| libunord-stage12-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage13-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage6-loop-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage6-sum | -- | -- | 0.04 | 157 | 0.01x |
| libunord-stage7-sum | -- | -- | 0.03 | 157 | 0.01x |
| libunord-stage9-sum | -- | -- | 0.05 | 157 | 0.01x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.19* | *148* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *158* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *158* | *0.00x* |
| lib-stage1 | 0.021 | 0.043 | 0.10 | 147 | 1.01x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.041* | *0.09* | *147* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.041 | 0.09 | 147 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.041* | *0.08* | *147* | *1.00x* |
| lib-stage2-lean | 0.022 | 0.030 | 0.07 | 147 | 1.01x |
| lib-stage2-lean-u1 | 0.025 | 0.034 | 0.10 | 147 | 1.01x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.027 | 0.044 | 0.11 | 146 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.042* | *0.064* | *0.08* | *138* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.042* | *0.064* | *0.10* | *138* | *1.00x* |
| **mut-odo-vecdims** | **0.042** | 0.064 | 0.05 | 138 | 1.00x |
| bq-expand | 0.137 | 0.235 | 0.11 | 122 | 3.22x |
| *bq-expand-aa-distant* | *0.137* | *0.235* | *0.13* | *122* | *3.22x* |
| *bq-expand-aa-adjacent* | *0.137* | *0.235* | *0.15* | *122* | *3.22x* |
| *list-aa-distant* | *0.995* | *1.001* | *0.30* | *85* | *26.11x* |
| *list-aa-adjacent* | *1.000* | *1.005* | *0.18* | *85* | *26.11x* |
| list (baseline) | 1.000 | 1.000 | 0.28 | 85 | 26.11x |

**Controls:** SOUND. The largest A/A pair is `list-aa-distant` at 0.9949, worst cell 1.00% on `rev-gather48-src-50`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9987 on a worst cell of 0.35% on `rev-gather48-src-50`, its interval missing 1. The in-situ term reads 1.0072, 1.0136 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9951, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h9m9s, peak 96 MiB in use, 24 MiB max residency; the reader reads 35 benchmarks over 3 shapes of the rev class. Anchor: `rev-primes`, `list` at 4.63 ms per call raw, 4.48 ms net.

**Per shape, in the run's shape order (rev-cnn-L1-24x24-c1, rev-gather48-src-50, rev-primes):** `mut-odo-vecdims` 0.064/0.047/0.024

**Across the halves:** 3 of the 16 arms are faster on this half and 13 slower, at a geomean of 1.1025, from `lib-stage2-lean-u1` at 0.9418 to `bq-expand` at 1.3050, with `list` itself at 1.2983. **The baseline moved 29.83% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.064, tiers at 1.00x, 3.22x, 26.11x --- and `lib-stage1` leads outside the family at 0.021, priced against `mut-odo-vecdims` at 0.6170 over 3 of 3 shapes at sign p 0.25, a margin of 38.30% against this class's 0.51% floor (`list-aa-distant`). **What this class shows of the pair is its widest arm swing the basis's way**: `lib-stage2-lean-u1` at 0.9418, the low extreme of the whole cross-half reading over the ten classes, in the same table as `bq-expand` at 1.3050. Its two columns may NOT be differenced, `list` having moved 29.83 of a point, at a class geomean of 1.1025 over the 16 arms, with 4 of 8 strategies past an A/A bar of 1.04 points. The counted work reads a counts geomean of 1.1645 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 16.45 points in instructions against 10.25 in time.

**`bcast` --- an innermost stride of 0, every run re-reading one element: a broadcast's view.** Shapes: `bcast-inner8` (`l` 51200, `sInner` 8), `bcast-inner900` (`l` 1800000, `sInner` 900), `bcast-tall-Mx2` (`l` 1800000, `sInner` 2), and the repeat ladder that landed 2026-09-09, for Run 28 --- `bcast-src8` (`l` 1800000, `sInner` 225000), `bcast-src64` (`l` 1800000, `sInner` 28125) and `bcast-src512` (`l` 1799680, `sInner` 3515). The ladder is one source length per rung broadcast to the same 1.8 million elements, so what varies is how long a slice stage nine repeats and how many times; the two older views sit ABOVE every rung of it, at 2000 and 900000 source elements against the ladder's 8, 64 and 512, so the ladder extends the sweep downward rather than filling a gap inside it. It was added to find where the repeated slice meets the fill, and Run 28's registration (7) read no crossover on it; this run reads the class for stage twelve's tie with stage eleven, at registration (2).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.62* | *53* | *1.00x* |
| liblist-stage1-sum | -- | -- | 0.49 | 62 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.50 | 62 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.52 | 62 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.48 | 62 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 74 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.50 | 62 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.48 | 62 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.01 | 74 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.26* | *83* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *69* | *0.00x* |
| lib-stage2-lean | 0.016 | 0.020 | 0.50 | 62 | 1.00x |
| lib-stage1 | 0.016 | 0.020 | 0.43 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.016* | *0.020* | *0.42* | *62* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.016 | 0.020 | 0.45 | 62 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.016* | *0.020* | *0.53* | *62* | *1.00x* |
| lib-stage2-lean-u1 | 0.016 | 0.024 | 0.51 | 62 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.018 | 0.020 | 0.43 | 61 | 1.00x |
| *mut-odo-vecdims-aa* | *0.021* | *0.057* | *0.34* | *61* | *1.00x* |
| **mut-odo-vecdims** | **0.021** | 0.057 | 0.12 | 61 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.021* | *0.057* | *0.36* | *61* | *1.00x* |
| bq-expand | 0.092 | 0.140 | 0.69 | 46 | 1.00x |
| *bq-expand-aa-distant* | *0.093* | *0.144* | *0.22* | *46* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.093* | *0.140* | *0.72* | *46* | *1.00x* |
| list (baseline) | 1.000 | 1.000 | 1.17 | 17 | 20.99x |
| *list-aa-distant* | *1.005* | *1.031* | *0.91* | *17* | *20.99x* |
| *list-aa-adjacent* | *1.007* | *1.014* | *0.85* | *17* | *20.99x* |

**Controls:** SOUND. The largest A/A pair is `bq-expand-aa-distant` at 1.0106, worst cell 2.61% on `bcast-tall-Mx2`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0008 on a worst cell of 0.47% on `bcast-src512`, its interval covering 1. The in-situ term reads 1.0177, 1.0089 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0080, which the correction amplifies by 1.36x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m16s, peak 169 MiB in use, 42 MiB max residency; the reader reads 35 benchmarks over 6 shapes of the bcast class. Anchor: `bcast-inner900`, `list` at 30.8 ms per call raw, 29.7 ms net.

**Per shape, in the run's shape order (bcast-inner8, bcast-inner900, bcast-tall-Mx2, bcast-src8, bcast-src64, bcast-src512):** `mut-odo-vecdims` 0.029/0.019/0.057/0.016/0.019/0.019

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0881, from `lib-stage2-lean-u1` at 0.9892 to `list` at 1.3798, with `list` itself at 1.3798. **The baseline moved 37.98% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.00x, 20.99x --- and `lib-stage2-lean` leads outside the family at 0.016, priced against `mut-odo-vecdims` at 0.6628 over 6 of 6 shapes at sign p 0.031, a margin of 33.72% against this class's 1.06% floor (`bq-expand-aa-distant`). **What this class shows of the pair is the widest `list` move of the ten**, 37.98 points, on the class whose views broadcast a small source over a large extent --- and `bq-expand` allocating at level with the fills here, 1.00x on both halves, where the passes cut its allocation on every other population. Its two columns may NOT be differenced, `list` having moved 37.98 of a point, at a class geomean of 1.0881 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.21 points. The counted work reads a counts geomean of 1.1686 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 16.86 points in instructions against 8.81 in time.

**`bcastmid` --- the stretched axis in the middle instead: stride 0 on an outer dimension.** Shapes: `bcastmid-c32-cnn` (`l` 165888, `sInner` 3), `bcastmid-primes` (`l` 250357, `sInner` 97), `bcastmid-b200k` (`l` 1800000, `sInner` 3), `bcastmid-block150k` (`l` 1800000, `sInner` 300). The fourth landed 2026-08-25 and is the block-copy arm's best case where `bcastmid-b200k` is its worst, its block taken to 150000 elements where the class's others run 3 to 216.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.39* | *66* | *1.92x* |
| liblist-stage1-sum | -- | -- | 0.34 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.38 | 82 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.30 | 82 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.35 | 82 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.37 | 82 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.33 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 96 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.31 | 82 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.33 | 82 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.34 | 82 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 96 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.30* | *88* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *88* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *88* | *0.00x* |
| lib-stage2-lean-u1 | 0.012 | 0.018 | 0.39 | 82 | 1.00x |
| lib-stage2-lean | 0.012 | 0.017 | 0.40 | 82 | 1.00x |
| lib-stage1 | 0.012 | 0.017 | 0.38 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.020 | 0.030 | 0.48 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.020* | *0.030* | *0.34* | *80* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.020* | *0.030* | *0.37* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.031 | 0.51 | 78 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.029* | *0.053* | *0.31* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.029** | 0.053 | 0.29 | 76 | 1.00x |
| *mut-odo-vecdims-aa* | *0.029* | *0.053* | *0.33* | *76* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.099* | *0.183* | *0.40* | *61* | *1.92x* |
| bq-expand | 0.099 | 0.184 | 0.50 | 61 | 1.92x |
| *bq-expand-aa-distant* | *0.100* | *0.186* | *0.49* | *60* | *1.92x* |
| list (baseline) | 1.000 | 1.000 | 0.77 | 28 | 23.56x |
| *list-aa-adjacent* | *1.001* | *1.012* | *0.75* | *28* | *23.56x* |
| *list-aa-distant* | *1.001* | *1.010* | *0.87* | *28* | *23.56x* |

**Controls:** SOUND. The largest A/A pair is `bq-expand-aa-distant` at 1.0136, worst cell 4.41% on `bcastmid-b200k`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 0.9999 on a worst cell of 0.08% on `bcastmid-block150k`, its interval covering 1. The in-situ term reads 1.0142, 1.0524 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0111, which the correction amplifies by 1.29x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m13s, peak 135 MiB in use, 35 MiB max residency; the reader reads 35 benchmarks over 4 shapes of the bcastmid class. Anchor: `bcastmid-b200k`, `list` at 48.4 ms per call raw, 47.3 ms net.

**Per shape, in the run's shape order (bcastmid-c32-cnn, bcastmid-primes, bcastmid-b200k, bcastmid-block150k):** `mut-odo-vecdims` 0.053/0.019/0.034/0.022

**Across the halves:** 7 of the 16 arms are faster on this half and 9 slower, at a geomean of 1.0829, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9722 to `list-aa-adjacent` at 1.2663, with `list` itself at 1.2497. **The baseline moved 24.97% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.053, tiers at 1.00x, 1.92x, 23.56x --- and `lib-stage2-lean-u1` leads outside the family at 0.012, priced against `mut-odo-vecdims` at 0.4242 over 4 of 4 shapes at sign p 0.12, a margin of 57.58% against this class's 1.36% floor (`bq-expand-aa-distant`). **What this class shows of the pair is the narrowest `list` move of the ten**, 24.97 points, and the widest lead an arm outside the family takes anywhere in this run: `lib-stage2-lean-u1` at 0.012 against the family's ceiling at 0.020. Its two columns may NOT be differenced, `list` having moved 24.97 of a point, at a class geomean of 1.0829 over the 16 arms, with 4 of 8 strategies past an A/A bar of 1.33 points. The counted work reads a counts geomean of 1.1678 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 16.78 points in instructions against 8.29 in time.

**`window` --- overlapping im2col patches: the workload the README opens by naming, with the overlap the main set's bijective map drops.** Shapes: `window-28x28-k5` (`l` 14400, `sInner` 5), `window-224x224-k3` (`l` 443556, `sInner` 3), `window-64x64-k1x9` (`l` 32256, `sInner` 1), `window-128x128-k7` (`l` 729316, `sInner` 7), `window-224x224-k3-s2` (`l` 110889, `sInner` 3) and `window-224x224-k3-d2` (`l` 435600, `sInner` 3). The last two landed 2026-09-03, a strided and a dilated k3 window, and they are the class's first views whose patches step by more than one; the arm they were registered for was parked the day after, so this run times them for the other arms' sanity alone. Two more landed 2026-09-09, for Run 28, `window-64x64-c16-k3` (`l` 553536, `sInner` 3) and `window-32x32-c64-k3` (`l` 518400, `sInner` 3): patch views with a channel axis, listed as image, channels and kernel rather than as the view shape, at one image size in elements, so the channel stride and the run length vary together while the view's size does not. They are the shape stage seven's tie-break exists for, the channel axis standing untied between the tied pairs.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.34* | *61* | *3.86x* |
| liblist-stage1-sum | -- | -- | 0.16 | 83 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.19 | 83 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.17 | 83 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.16 | 83 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.15 | 83 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.16 | 83 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage10-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage11-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage12-sum | -- | -- | 0.06 | 102 | 0.03x |
| libunord-stage13-sum | -- | -- | 0.09 | 102 | 0.03x |
| libunord-stage6-loop-sum | -- | -- | 1.23 | 90 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.10 | 100 | 0.03x |
| libunord-stage7-sum | -- | -- | 0.07 | 102 | 0.03x |
| libunord-stage9-sum | -- | -- | 0.06 | 100 | 0.03x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *86* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *97* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *97* | *0.00x* |
| lib-stage2-lean | 0.026 | 0.030 | 0.20 | 83 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.027* | *0.030* | *0.18* | *83* | *1.00x* |
| lib-stage1 | 0.027 | 0.030 | 0.18 | 83 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.030 | 0.15 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.030* | *0.16* | *83* | *1.00x* |
| lib-stage2-lean-u1 | 0.029 | 0.032 | 0.26 | 82 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.030 | 0.031 | 0.20 | 82 | 1.00x |
| *mut-odo-vecdims-aa* | *0.051* | *0.088* | *0.16* | *76* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.051* | *0.088* | *0.15* | *76* | *1.00x* |
| **mut-odo-vecdims** | **0.051** | 0.086 | 0.18 | 76 | 1.00x |
| *bq-expand-aa-adjacent* | *0.177* | *0.220* | *0.31* | *57* | *3.86x* |
| bq-expand | 0.179 | 0.219 | 0.31 | 57 | 3.86x |
| *bq-expand-aa-distant* | *0.179* | *0.220* | *0.27* | *57* | *3.86x* |
| list (baseline) | 1.000 | 1.000 | 0.43 | 30 | 27.66x |
| *list-aa-adjacent* | *1.001* | *1.004* | *0.43* | *30* | *27.66x* |
| *list-aa-distant* | *1.002* | *1.046* | *0.50* | *30* | *27.66x* |

**Controls:** SOUND. The largest A/A pair is `list-aa-distant` at 1.0043, worst cell 4.57% on `window-64x64-c16-k3`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.47% on `window-32x32-c64-k3`, its interval covering 1. The in-situ term reads 1.0087, 1.1729 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0042, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h24m15s, peak 122 MiB in use, 48 MiB max residency; the reader reads 35 benchmarks over 8 shapes of the window class. Anchor: `window-128x128-k7`, `list` at 14.2 ms per call raw, 13.8 ms net.

**Per shape, in the run's shape order (window-28x28-k5, window-224x224-k3, window-64x64-k1x9, window-128x128-k7, window-224x224-k3-s2, window-224x224-k3-d2, window-64x64-c16-k3, window-32x32-c64-k3):** `mut-odo-vecdims` 0.040/0.051/0.086/0.031/0.052/0.051/0.053/0.052

**Across the halves:** 5 of the 16 arms are faster on this half and 11 slower, at a geomean of 1.1368, from `mut-odo-vecdims` at 0.9941 to `bq-expand-aa-distant` at 1.5306, with `list` itself at 1.2938. **The baseline moved 29.38% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.086, tiers at 1.00x, 3.86x, 27.66x --- and `lib-stage2-lean` leads outside the family at 0.026, priced against `mut-odo-vecdims` at 0.4585 over 8 of 8 shapes at sign p 0.0078, a margin of 54.15% against this class's 0.43% floor (`list-aa-distant`). **What this class shows of the pair is the widest class geomean of the ten**, 1.1368, and the high extreme of the whole cross-half reading, `bq-expand-aa-distant` at 1.5306 --- on the class where the passes also cut `bq-expand`'s allocation furthest, to 0.7263 of the basis. Its two columns may NOT be differenced, `list` having moved 29.38 of a point, at a class geomean of 1.1368 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.04 points. The counted work reads a counts geomean of 1.1765 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 17.65 points in instructions against 13.68 in time.

**`scaled` --- superincreasing strides, none of them 1: a hand-built dilated view.** Shapes: `scaled-super-r3` (`l` 60000, `sInner` 30), `scaled-rank1-m1` (`l` 300000, `sInner` 300000 --- rank 1, so `m` is 1 and the whole view is one strided run), `scaled-r5` (`l` 15015, `sInner` 13).

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *118* | *1.21x* |
| liblist-stage1-sum | -- | -- | 0.12 | 128 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.16 | 128 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.10 | 128 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.17 | 128 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.11 | 128 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.13 | 127 | 1.01x |
| libunord-stage10-list-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage10-sum | -- | -- | 0.14 | 128 | 1.00x |
| libunord-stage11-sum | -- | -- | 0.17 | 128 | 1.00x |
| libunord-stage12-sum | -- | -- | 0.24 | 127 | 1.00x |
| libunord-stage13-sum | -- | -- | 0.13 | 128 | 1.00x |
| libunord-stage6-loop-sum | -- | -- | 0.19 | 128 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.20 | 127 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.21 | 128 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.12 | 128 | 1.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.17* | *147* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *138* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.031* | *0.19* | *128* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.022* | *0.031* | *0.18* | *128* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.022 | 0.031 | 0.21 | 128 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.023 | 0.031 | 0.15 | 127 | 1.00x |
| lib-stage1 | 0.023 | 0.031 | 0.15 | 128 | 1.00x |
| lib-stage2-lean | 0.023 | 0.031 | 0.11 | 128 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.031 | 0.19 | 127 | 1.00x |
| **mut-odo-vecdims** | **0.027** | 0.029 | 0.11 | 127 | 1.00x |
| *mut-odo-vecdims-aa* | *0.027* | *0.029* | *0.11* | *127* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.029* | *0.09* | *127* | *1.00x* |
| bq-expand | 0.091 | 0.102 | 0.07 | 111 | 1.21x |
| *bq-expand-aa-adjacent* | *0.091* | *0.102* | *0.08* | *111* | *1.21x* |
| *bq-expand-aa-distant* | *0.091* | *0.102* | *0.07* | *111* | *1.21x* |
| *list-aa-distant* | *0.996* | *1.001* | *0.24* | *69* | *21.49x* |
| list (baseline) | 1.000 | 1.000 | 0.31 | 69 | 21.49x |
| *list-aa-adjacent* | *1.001* | *1.005* | *0.24* | *69* | *21.49x* |

**Controls:** SOUND, and the correction amplifies by 2.44x here, so both the corrected net and the raw slope are quoted where this class is read. The largest A/A pair is `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at 0.9936, worst cell 0.91% on `scaled-super-r3`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 0.9986 on a worst cell of 0.41% on `scaled-super-r3`, its interval missing 1. The in-situ term reads 1.0172, 1.0123 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9974, which the correction amplifies by 2.44x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h9m11s, peak 111 MiB in use, 38 MiB max residency; the reader reads 35 benchmarks over 3 shapes of the scaled class. Anchor: `scaled-rank1-m1`, `list` at 5.29 ms per call raw, 5.11 ms net.

**Per shape, in the run's shape order (scaled-super-r3, scaled-rank1-m1, scaled-r5):** `mut-odo-vecdims` 0.023/0.028/0.029

**Across the halves:** 8 of the 16 arms are faster on this half and 8 slower, at a geomean of 1.0616, from `mut-odo-vecdims-add-in-leaf-u2-aa` at 0.9900 to `list` at 1.3051, with `list` itself at 1.3051. **The baseline moved 30.51% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.21x, 21.49x --- and `lib-stage1` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.9251 over 2 of 3 shapes at sign p 1, a margin of 7.49% against this class's 0.64% floor (`mut-odo-vecdims-add-in-leaf-u2-aa-distant`). **What this class shows of the pair is a bolded column that changes between the halves**: the family's ceiling leads on the basis and `lib-stage1` on the control, one of two classes where that happens and the only one where the family loses the lead under the passes. Its two columns may NOT be differenced, `list` having moved 30.51 of a point, at a class geomean of 1.0616 over the 16 arms, with 2 of 8 strategies past an A/A bar of 1.87 points. The counted work reads a counts geomean of 1.1515 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 15.15 points in instructions against 6.16 in time.

**`runs` --- run length swept from 2 to 65536 with innermost stride 1 throughout: regime 2, which the library reaches by a route of its own, and the population the rework's question needed --- extended on Run 22 from seven views to eleven, on Run 24 to fourteen and on Run 34 to seventeen.** Shapes: `runs-2` (`l` 1800000, `sInner` 2), `runs-3` (`l` 1800000, `sInner` 3 --- a k3 conv row), `runs-4` (`l` 1800000, `sInner` 4 --- landed on Run 22, and the first view in the suite with a canonical innermost extent of 4, the branch the short-body fills take and which nothing, `check` included, had exercised), `runs-5` (`l` 1800000, `sInner` 5 --- landed on Run 22, beside it), `runs-7` (`l` 1799994, `sInner` 7 --- landed on Run 24, one past the short bodies of `fillStage2Short`, which write runs of 2 to 5: the first length where the stepping loop with its odd tail takes over from them, and a k7 conv row), `runs-9` (`l` 1800000, `sInner` 9 --- the window probe's run), `runs-32` (`l` 1800000, `sInner` 32), `runs-48` (`l` 1800000, `sInner` 48) and `runs-64` (`l` 1800000, `sInner` 64) --- the three landed on Run 34, inside the gap from 9 to 96 where a fit to Run 33's stage-eleven curve had put a minimum --- `runs-96` (`l` 1800000, `sInner` 96 --- an image row), `runs-256` (`l` 1799936, `sInner` 256 --- landed on Run 22, and the dispatch threshold's own cell, `>= dispRun` firing exactly here), `runs-512` (`l` 1799680, `sInner` 512 --- landed on Run 22, bracketing `dispRun` within a factor of two), `runs-1024` (`l` 1799168, `sInner` 1024), `runs-4096` (`l` 1798144, `sInner` 4096 --- landed on Run 24), `runs-16384` (`l` 1785856, `sInner` 16384 --- landed on Run 24, the two of them inside the 64x gap the crossover moved into), `runs-65536` (`l` 1769472, `sInner` 65536 --- a few long runs), `runs-r3-48x30` (`l` 1800000, `sInner` 1440 --- rank 3, merging to runs of 1440). Every shape sits at `l` of about 1.8M, so what varies across the class is the run length alone.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.52* | *52* | *1.08x* |
| liblist-stage1-sum | -- | -- | 0.12 | 61 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.06 | 69 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.02 | 72 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 72 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 61 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.06 | 69 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.03 | 72 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 72 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 72 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.14* | *77* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.02* | *69* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *69* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.024* | *0.025* | *0.47* | *59* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.025 | 0.025 | 0.11 | 59 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.025* | *0.025* | *0.11* | *59* | *1.00x* |
| lib-stage2-lean | 0.025 | 0.026 | 0.11 | 59 | 1.00x |
| lib-stage2-lean-u1 | 0.025 | 0.027 | 0.11 | 59 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.025 | 0.027 | 0.13 | 59 | 1.00x |
| **mut-odo-vecdims** | **0.027** | 0.057 | 0.09 | 59 | 1.00x |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.057* | *0.08* | *59* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.027* | *0.057* | *0.09* | *59* | *1.00x* |
| *bq-expand-aa-adjacent* | *0.095* | *0.140* | *0.52* | *46* | *1.08x* |
| bq-expand | 0.095 | 0.140 | 0.44 | 46 | 1.08x |
| *bq-expand-aa-distant* | *0.096* | *0.142* | *0.05* | *46* | *1.08x* |
| lib-stage1 | 0.099 | 1.098 | 0.19 | 51 | 1.42x |
| list (baseline) | 1.000 | 1.000 | 2.67 | 17 | 21.30x |
| *list-aa-distant* | *1.034* | *1.061* | *0.22* | *17* | *21.30x* |
| *list-aa-adjacent* | *1.036* | *1.049* | *0.23* | *17* | *21.30x* |

**Controls:** SOUND. The largest A/A pair is `list-aa-adjacent` at 1.0357, worst cell 4.93% on `runs-r3-48x30`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9997 on a worst cell of 0.48% on `runs-64`, its interval covering 1. The in-situ term reads 1.0287, 1.0292 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0345, which the correction amplifies by 1.03x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h51m33s, peak 657 MiB in use, 289 MiB max residency; the reader reads 35 benchmarks over 17 shapes of the runs class. Anchor: `runs-2`, `list` at 41 ms per call raw, 40 ms net.

**Per shape, in the run's shape order (runs-2, runs-3, runs-4, runs-5, runs-7, runs-9, runs-32, runs-48, runs-64, runs-96, runs-256, runs-512, runs-1024, runs-4096, runs-16384, runs-65536, runs-r3-48x30):** `mut-odo-vecdims` 0.057/0.047/0.041/0.039/0.033/0.030/0.025/0.025/0.025/0.025/0.025/0.024/0.024/0.024/0.024/0.024/0.028

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0818, from `mut-odo-vecdims-add-in-leaf-u1` at 0.9955 to `list-aa-distant` at 1.3201, with `list` itself at 1.3079. **The baseline moved 30.79% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.057, tiers at 1.00x, 1.08x, 21.30x --- and `lib-stage2-lean` leads outside the family at 0.025, priced against `mut-odo-vecdims` at 0.8356 over 8 of 17 shapes at sign p 1, a margin of 16.44% against this class's 3.57% floor (`list-aa-adjacent`). **What this class shows of the pair is the one standing break of the wider statement, widened by the passes speeding up the thing it is measured against**: `lib-stage1` is slower than `list` on `runs-2` at 1.0978 on the basis and 1.3495 on the control, and on `runs-3` at 1.1348 on the control alone --- the only three cells of the run's 1120 to read above 1, and on both shapes the fill's own net moves under 3.5% between the halves where `list` moves 27 to 28. Its two columns may NOT be differenced, `list` having moved 30.79 of a point, at a class geomean of 1.0818 over the 16 arms, with 3 of 8 strategies past an A/A bar of 0.93 points. The counted work reads a counts geomean of 1.1613 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 16.13 points in instructions against 8.18 in time.



**`flip` --- a dense array reversed, whole or along its last axis, so the innermost stride is -1: regime 2 mirrored, and one run at stride -1 once canonicalized.** Shapes: in the order they run, `flip-fwd-rows96` (`l` 1800000, `sInner` 96), which landed 2026-09-09 and is `runs-96`'s construction under a `flip` name --- the forward control for `flip-last-rows`, so the class's own reversal finding is read inside ONE process over one baseline where it used to be read across two; `flip-whole-square` (`l` 1798281, `sInner` 1341); `flip-last-c32` (`l` 165888, `sInner` 3); `flip-last-rows` (`l` 1800000, `sInner` 96); and the two that landed 2026-09-05 and are the `block` class's gap-64 rows reversed, `flip-inner-gap64` (`l` 131072, `sInner` 64), each row reversed, and `flip-outer-gap64` (`l` 131072, `sInner` 64), the rows in reverse order. The control sits in this class by its name alone --- `classOf` reads the class off the name --- and not in `flipShapes`, every member of which is asserted to have an innermost stride of -1.

| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.43* | *66* | *1.05x* |
| liblist-stage1-sum | -- | -- | 0.10 | 82 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.11 | 88 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.08 | 92 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.07 | 92 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.26 | 92 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.12 | 82 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 98 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.03 | 98 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.02 | 96 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 98 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 98 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.09* | *91* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *93* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.02* | *93* | *0.00x* |
| lib-stage2-lean | 0.023 | 0.043 | 0.25 | 84 | 1.00x |
| lib-stage2-lean-u1 | 0.024 | 0.046 | 0.34 | 82 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.026* | *0.041* | *0.38* | *80* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.027 | 0.042 | 0.09 | 80 | 1.00x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.027* | *0.042* | *0.16* | *80* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.027* | *0.052* | *0.12* | *77* | *1.00x* |
| *mut-odo-vecdims-aa* | *0.027* | *0.052* | *0.15* | *77* | *1.00x* |
| **mut-odo-vecdims** | **0.027** | 0.052 | 0.10 | 77 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.028 | 0.046 | 0.23 | 80 | 1.00x |
| lib-stage1 | 0.034 | 0.047 | 0.26 | 80 | 1.00x |
| *bq-expand-aa-adjacent* | *0.091* | *0.181* | *0.43* | *61* | *1.05x* |
| bq-expand | 0.091 | 0.181 | 0.43 | 61 | 1.05x |
| *bq-expand-aa-distant* | *0.092* | *0.182* | *0.12* | *61* | *1.05x* |
| list (baseline) | 1.000 | 1.000 | 0.72 | 32 | 21.18x |
| *list-aa-distant* | *1.004* | *1.022* | *0.58* | *32* | *21.18x* |
| *list-aa-adjacent* | *1.008* | *1.024* | *0.28* | *32* | *21.18x* |

**Controls:** SOUND, and the correction amplifies by 2.09x here, so both the corrected net and the raw slope are quoted where this class is read. The largest A/A pair is `mut-odo-vecdims-aa` at 1.0121, worst cell 6.49% on `flip-last-rows`, and 6 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.50% on `flip-inner-gap64`, its interval covering 1. The in-situ term reads 1.0197, 1.0222 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0064, which the correction amplifies by 2.09x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h18m15s, peak 209 MiB in use, 76 MiB max residency; the reader reads 35 benchmarks over 6 shapes of the flip class. Anchor: `flip-fwd-rows96`, `list` at 31 ms per call raw, 29.9 ms net.

**Per shape, in the run's shape order (flip-fwd-rows96, flip-whole-square, flip-last-c32, flip-last-rows, flip-inner-gap64, flip-outer-gap64):** `mut-odo-vecdims` 0.024/0.024/0.052/0.040/0.026/0.025

**Across the halves:** 6 of the 16 arms are faster on this half and 10 slower, at a geomean of 1.0657, from `mut-odo-vecdims` at 0.9603 to `list-aa-adjacent` at 1.3241, with `list` itself at 1.3098. **The baseline moved 30.98% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.052, tiers at 1.00x, 1.05x, 21.18x --- and `lib-stage2-lean` leads outside the family at 0.023, priced against `mut-odo-vecdims` at 0.7907 over 4 of 6 shapes at sign p 0.69, a margin of 20.93% against this class's 1.21% floor (`mut-odo-vecdims-aa`). **What this class shows of the pair is the plain arm left behind**: `mut-odo-vecdims` reads 0.9603, the basis the faster, which no other class puts below 0.96 --- and this is the class whose A/A worst cell is above 5% on BOTH halves, 6.49% and 5.40%, both on `flip-last-rows`. Its two columns may NOT be differenced, `list` having moved 30.98 of a point, at a class geomean of 1.0657 over the 16 arms, with 3 of 8 strategies past an A/A bar of 2.05 points. The counted work reads a counts geomean of 1.1513 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 15.13 points in instructions against 6.57 in time.

**`block` --- regime 2 as a sub-block of a wider array, the gap between one run and the next being the variable.** Shapes: `block-run64-gap1` (`l` 131072, `sInner` 64), `block-run64-gap64` (`l` 131072, `sInner` 64), `block-run64-page` (`l` 131072, `sInner` 64), `block-run64-off7` (`l` 131072, `sInner` 64), `block-r3-vol64` (`l` 262144, `sInner` 64). The first three sweep the gap from one element to a page at one run length, the fourth is `block-run64-gap64` moved off an eight-element boundary, and the fifth is a rank-3 block whose two outer dimensions do not merge.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.08* | *103* | *1.06x* |
| liblist-stage1-sum | -- | -- | 0.14 | 113 | 0.42x |
| liblist-stage2-sum | -- | -- | 0.17 | 122 | 0.34x |
| liblist-stage3-sum | -- | -- | 0.04 | 129 | 0.00x |
| liblist-stage4-list-sum | -- | -- | 0.02 | 129 | 0.00x |
| liblist-stage4-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage1-sum | -- | -- | 0.14 | 113 | 0.42x |
| libunord-stage10-list-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 129 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.03 | 129 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.06 | 127 | 0.00x |
| libunord-stage6-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage7-sum | -- | -- | 0.02 | 129 | 0.00x |
| libunord-stage9-sum | -- | -- | 0.03 | 129 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.15* | *129* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.03* | *122* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *122* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.021* | *0.025* | *0.09* | *111* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.021* | *0.025* | *0.12* | *111* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.021 | 0.025 | 0.13 | 111 | 1.00x |
| lib-stage2-lean | 0.022 | 0.025 | 0.20 | 111 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.022 | 0.026 | 0.12 | 111 | 1.00x |
| lib-stage2-lean-u1 | 0.022 | 0.026 | 0.11 | 111 | 1.00x |
| **mut-odo-vecdims** | **0.023** | 0.029 | 0.09 | 111 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.08* | *111* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.09* | *111* | *1.00x* |
| lib-stage1 | 0.049 | 0.058 | 0.11 | 104 | 1.42x |
| *bq-expand-aa-adjacent* | *0.086* | *0.087* | *0.13* | *96* | *1.06x* |
| bq-expand | 0.086 | 0.087 | 0.13 | 96 | 1.06x |
| *bq-expand-aa-distant* | *0.087* | *0.088* | *0.11* | *96* | *1.06x* |
| *list-aa-adjacent* | *0.999* | *1.002* | *0.20* | *54* | *21.22x* |
| list (baseline) | 1.000 | 1.000 | 0.24 | 54 | 21.22x |
| *list-aa-distant* | *1.001* | *1.006* | *0.28* | *54* | *21.22x* |

**Controls:** SOUND. The largest A/A pair is `bq-expand-aa-adjacent` at 0.9987, worst cell 0.32% on `block-run64-gap1`, and 8 of 8 intervals cover 1. The `sum-only` halves agree at 0.9989 on a worst cell of 0.48% on `block-run64-gap1`, its interval missing 1. The in-situ term reads 1.0205, 1.0219 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9991, which the correction amplifies by 1.40x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m12s, peak 134 MiB in use, 52 MiB max residency; the reader reads 35 benchmarks over 5 shapes of the block class. Anchor: `block-r3-vol64`, `list` at 4.6 ms per call raw, 4.44 ms net.

**Per shape, in the run's shape order (block-run64-gap1, block-run64-gap64, block-run64-page, block-run64-off7, block-r3-vol64):** `mut-odo-vecdims` 0.019/0.024/0.029/0.024/0.020

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0598, from `lib-stage2-lean-u1` at 0.9730 to `list-aa-distant` at 1.3344, with `list` itself at 1.3050. **The baseline moved 30.50% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.06x, 21.22x --- and `lib-stage2-lean` leads outside the family at 0.022, priced against `mut-odo-vecdims` at 0.9343 over 5 of 5 shapes at sign p 0.062, a margin of 6.57% against this class's 0.13% floor (`bq-expand-aa-adjacent`). **What this class shows of the pair is the narrowest class geomean of the ten**, 1.0598, on the tightest basis-half floor of the eleven populations, 0.13% --- so the smallest movement this pair makes anywhere is read against its finest ruler. Its two columns may NOT be differenced, `list` having moved 30.50 of a point, at a class geomean of 1.0598 over the 16 arms, with 3 of 8 strategies past an A/A bar of 2.26 points. The counted work reads a counts geomean of 1.1484 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 14.84 points in instructions against 5.98 in time.

**`small` --- one view per canonical regime at a few hundred elements, where a per-call cost is a share of the call: the one class defined by a size and not by an operation.** Shapes: `small-row96` (`l` 384, `sInner` 96), `small-patch-k5` (`l` 150, `sInner` 5), `small-bcast32` (`l` 256, `sInner` 32), `small-flat64` (`l` 256, `sInner` 64), and `small-patch-r5` (`l` 256, `sInner` 4), a rank-5 im2col patch canonicalizing to rank 4, which landed 2026-09-05.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.20* | *222* | *1.44x* |
| liblist-stage1-sum | -- | -- | 0.17 | 228 | 1.65x |
| liblist-stage2-sum | -- | -- | 0.20 | 230 | 1.55x |
| liblist-stage3-sum | -- | -- | 0.20 | 227 | 1.69x |
| liblist-stage4-list-sum | -- | -- | 0.17 | 231 | 1.51x |
| liblist-stage4-sum | -- | -- | 0.20 | 231 | 1.51x |
| libunord-stage1-sum | -- | -- | 0.22 | 223 | 2.08x |
| libunord-stage10-list-sum | -- | -- | 0.29 | 233 | 0.57x |
| libunord-stage10-sum | -- | -- | 0.29 | 233 | 0.55x |
| libunord-stage11-sum | -- | -- | 0.25 | 234 | 0.55x |
| libunord-stage12-sum | -- | -- | 0.17 | 235 | 0.55x |
| libunord-stage13-sum | -- | -- | 0.22 | 238 | 0.49x |
| libunord-stage6-loop-sum | -- | -- | 0.19 | 235 | 0.81x |
| libunord-stage6-sum | -- | -- | 0.25 | 234 | 0.83x |
| libunord-stage7-sum | -- | -- | 0.18 | 234 | 0.83x |
| libunord-stage9-sum | -- | -- | 0.23 | 233 | 0.55x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.29* | *238* | *1.27x* |
| *sum-only-early* | *--* | *--* | *0.03* | *250* | *0.01x* |
| *sum-only-late* | *--* | *--* | *0.03* | *250* | *0.01x* |
| lib-stage2-lean | 0.055 | 0.097 | 0.23 | 228 | 1.46x |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.055* | *0.071* | *0.28* | *229* | *1.28x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.055* | *0.071* | *0.32* | *229* | *1.28x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.055 | 0.072 | 0.29 | 229 | 1.28x |
| lib-stage2-lean-u1 | 0.056 | 0.101 | 0.23 | 228 | 1.46x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.056 | 0.069 | 0.36 | 229 | 1.28x |
| **mut-odo-vecdims** | **0.061** | 0.088 | 0.28 | 229 | 1.27x |
| *mut-odo-vecdims-aa-distant* | *0.061* | *0.088* | *0.19* | *229* | *1.27x* |
| *mut-odo-vecdims-aa* | *0.061* | *0.088* | *0.26* | *229* | *1.27x* |
| lib-stage1 | 0.097 | 0.106 | 0.20 | 221 | 2.33x |
| bq-expand | 0.138 | 0.200 | 0.15 | 217 | 1.44x |
| *bq-expand-aa-adjacent* | *0.138* | *0.200* | *0.13* | *217* | *1.44x* |
| *bq-expand-aa-distant* | *0.139* | *0.208* | *0.10* | *217* | *1.44x* |
| *list-aa-adjacent* | *0.998* | *1.001* | *0.16* | *180* | *21.57x* |
| *list-aa-distant* | *0.998* | *1.001* | *0.13* | *180* | *21.57x* |
| list (baseline) | 1.000 | 1.000 | 0.12 | 180 | 21.57x |

**Controls:** SOUND. The largest A/A pair is `bq-expand-aa-distant` at 1.0063, worst cell 4.30% on `small-patch-r5`, and 5 of 8 intervals cover 1. The `sum-only` halves agree at 1.0000 on a worst cell of 0.01% on `small-row96`, its interval covering 1. The in-situ term reads 0.9917, 1.0026 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 1.0057, which the correction amplifies by 1.24x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h15m17s, peak 134 MiB in use, 53 MiB max residency; the reader reads 35 benchmarks over 5 shapes of the small class. Anchor: `small-row96`, `list` at 6.65 us per call raw, 6.43 us net.

**Per shape, in the run's shape order (small-row96, small-patch-k5, small-bcast32, small-flat64, small-patch-r5):** `mut-odo-vecdims` 0.041/0.077/0.050/0.058/0.088

**Across the halves:** 0 of the 16 arms are faster on this half and 16 slower, at a geomean of 1.0995, from `mut-odo-vecdims` at 1.0134 to `list` at 1.2916, with `list` itself at 1.2916. **The baseline moved 29.16% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.088, tiers at 1.27x, 1.44x, 21.57x --- and `lib-stage2-lean` leads outside the family at 0.055, priced against `mut-odo-vecdims` at 0.9111 over 1 of 5 shapes at sign p 0.38, a margin of 8.89% against this class's 0.63% floor (`bq-expand-aa-distant`). **What this class shows of the pair is unanimity**: 0 of the 16 arms is faster on the basis and 16 on the control, the only class of the ten with no arm on the basis's side --- and the class that brings property 2's `bq-expand` clause closest to its margin, `small-row96` at 1.00441 on the control. Its two columns may NOT be differenced, `list` having moved 29.16 of a point, at a class geomean of 1.0995 over the 16 arms, with 8 of 8 strategies past an A/A bar of 1.00 points. The counted work reads a counts geomean of 1.1424 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 14.24 points in instructions against 9.95 in time.

**`compose` --- a zero stride combined with a second mechanism, as the library composes its operations and no one operation's class builds.** Shapes: `compose-rev-bcast` (`l` 51200, `sInner` 8), `compose-slice-bcast` (`l` 51200, `sInner` 8), `compose-zero-mid` (`l` 1800000, `sInner` 100), `compose-scalar` (`l` 1800000, `sInner` 1500). The first is a broadcast reversed, the second the same broadcast at an offset, the third a second zero stride the first cannot merge with, and the fourth every stride zero.
| strategy | time | worst | CI% | smp | alloc |
|---|---:|---:|---:|---:|---:|
| *bq-expand-nosum* | *--* | *--* | *0.37* | *85* | *1.35x* |
| liblist-stage1-sum | -- | -- | 0.33 | 98 | 1.00x |
| liblist-stage2-sum | -- | -- | 0.30 | 98 | 1.00x |
| liblist-stage3-sum | -- | -- | 0.33 | 98 | 1.00x |
| liblist-stage4-list-sum | -- | -- | 0.41 | 98 | 1.00x |
| liblist-stage4-sum | -- | -- | 0.32 | 98 | 1.00x |
| libunord-stage1-sum | -- | -- | 0.33 | 98 | 1.00x |
| libunord-stage10-list-sum | -- | -- | 0.02 | 110 | 0.00x |
| libunord-stage10-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage11-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage12-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage13-sum | -- | -- | 0.01 | 110 | 0.00x |
| libunord-stage6-loop-sum | -- | -- | 0.34 | 98 | 1.00x |
| libunord-stage6-sum | -- | -- | 0.37 | 98 | 1.00x |
| libunord-stage7-sum | -- | -- | 0.34 | 98 | 1.00x |
| libunord-stage9-sum | -- | -- | 0.02 | 110 | 0.00x |
| *mut-odo-vecdims-nosum* | *--* | *--* | *0.21* | *113* | *1.00x* |
| *sum-only-early* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *sum-only-late* | *--* | *--* | *0.01* | *105* | *0.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa-distant* | *0.015* | *0.016* | *0.29* | *98* | *1.00x* |
| *mut-odo-vecdims-add-in-leaf-u2-aa* | *0.015* | *0.016* | *0.31* | *98* | *1.00x* |
| mut-odo-vecdims-add-in-leaf-u2 | 0.015 | 0.016 | 0.29 | 98 | 1.00x |
| lib-stage2-lean | 0.015 | 0.016 | 0.32 | 98 | 1.00x |
| lib-stage1 | 0.015 | 0.017 | 0.33 | 98 | 1.00x |
| lib-stage2-lean-u1 | 0.016 | 0.016 | 0.30 | 97 | 1.00x |
| mut-odo-vecdims-add-in-leaf-u1 | 0.017 | 0.018 | 0.29 | 96 | 1.00x |
| *mut-odo-vecdims-aa* | *0.023* | *0.029* | *0.23* | *92* | *1.00x* |
| *mut-odo-vecdims-aa-distant* | *0.023* | *0.029* | *0.23* | *94* | *1.00x* |
| **mut-odo-vecdims** | **0.024** | 0.029 | 0.18 | 94 | 1.00x |
| *bq-expand-aa-adjacent* | *0.094* | *0.103* | *0.38* | *79* | *1.35x* |
| bq-expand | 0.094 | 0.103 | 0.34 | 79 | 1.35x |
| *bq-expand-aa-distant* | *0.095* | *0.103* | *0.23* | *79* | *1.35x* |
| *list-aa-adjacent* | *0.999* | *1.001* | *0.77* | *44* | *22.01x* |
| *list-aa-distant* | *1.000* | *1.006* | *0.74* | *44* | *22.01x* |
| list (baseline) | 1.000 | 1.000 | 0.67 | 44 | 22.01x |

**Controls:** SOUND, and the correction amplifies by 2.46x here, the furthest of the ten, so both the corrected net and the raw slope are quoted where this class is read. The largest A/A pair is `mut-odo-vecdims-aa` at 0.9889, worst cell 3.24% on `compose-scalar`, and 4 of 8 intervals cover 1. The `sum-only` halves agree at 0.9975 on a worst cell of 0.54% on `compose-scalar`, its interval covering 1. The in-situ term reads 1.0120, 1.0243 of `sum-only` as medians, on `mut-odo-vecdims`, `bq-expand`. Raw, that pair reads 0.9961, which the correction amplifies by 2.46x --- quote both wherever that is past 1.5.

**Provenance:** elapsed 0h12m17s, peak 126 MiB in use, 33 MiB max residency; the reader reads 35 benchmarks over 4 shapes of the compose class. Anchor: `compose-zero-mid`, `list` at 31.3 ms per call raw, 30.2 ms net.

**Per shape, in the run's shape order (compose-rev-bcast, compose-slice-bcast, compose-zero-mid, compose-scalar):** `mut-odo-vecdims` 0.029/0.029/0.019/0.019

**Across the halves:** 4 of the 16 arms are faster on this half and 12 slower, at a geomean of 1.0806, from `mut-odo-vecdims-aa` at 0.9922 to `list` at 1.3410, with `list` itself at 1.3410. **The baseline moved 34.10% between the halves, past the 0.7% that lets two columns be differenced, so this line is NOT read for the pair's variable.** The table above is one process's and stands; what goes is the comparison.

**What the class says:** property 1 HOLDS and property 2 HOLDS --- `worst` 0.029, tiers at 1.00x, 1.35x, 22.01x --- and `lib-stage2-lean` leads outside the family at 0.015, priced against `mut-odo-vecdims` at 0.6289 over 4 of 4 shapes at sign p 0.12, a margin of 37.11% against this class's 1.11% floor (`mut-odo-vecdims-aa`). **What this class shows of the pair is the correction's widest amplification of the ten**, 2.46x, on a class whose bolded column does not move: the family's ceiling leads on both halves here, where `scaled` and `small` are the two classes whose column changes. Its two columns may NOT be differenced, `list` having moved 34.10 of a point, at a class geomean of 1.0806 over the 16 arms, with 4 of 8 strategies past an A/A bar of 1.05 points. The counted work reads a counts geomean of 1.1626 over the same arms, 16 of them counted. The counted work moves further than the clock, as it does in all ten: 16.26 points in instructions against 8.06 in time.


## Provenance

**Run 36's halves differ in TWO GHC FLAGS and in nothing else.** One source, `Main.hs` at `0eda736`, unmoved since Run 35's build; one shim, `align-as.py` at `f31bd1c`; one shim environment, `LOOP_MAXSKIP=1 LOOP_LOOKTHROUGH=1 LOOP_DEADSPOT=1 LOOP_EXITSPAN=1` in front of the assembler shim; ONE compiler, the in-tree stage1 `10.1.20260918` reached through `cabal.project.ghead`; one roster, one shape set, one class list and one bench order; both halves built with `-fobject-determinism`, both launched from the `hugebin/` mount and both run under `WILDLOG=1 SATURATE=1`. The two command lines differ in `-fspec-constr -fliberate-case` on one of them, which micro.cabal's own `-O1` makes two of `-O2`'s passes on top of plain -O1 rather than a level. The basis is `run36-gheadnospec` and is what every table here publishes; `run36-gheadtwopass` is the candidate.

**The roster is 35 timed arms over 19 main-set shapes and 665 benches, with 61 class views over ten classes for 2135 more, and it IS Run 35's.** `./roster-delta.py run35-exit run36-gheadnospec`, read off the two binaries before the run, puts NONE in and NONE out with 35 survivors in the same order, the nineteen main-set shapes unmoved and the sixty-one class views unmoved over the same ten classes. So pre-run step 12's condition --- a membership change --- does not fire, and no figure in this file carries a roster term against Run 35. Of the roster's 123 arms, 88 are checked without being timed, as on Run 35.

**The sequence ran in ONE window and nothing else was on the machine.** The wall-clock log puts the twenty-two processes between 2026-09-19T02:06:14 and 2026-09-19T10:11:57, the largest hole between one process finishing and the next starting 0m, every process reporting rc=0 and the bench count asked of it --- 20 class processes, one per class per half, and two main-set ones. The gate's four processes ran 01:28 to 02:01 before it and the four alone-leg riders 10:12 to 10:24 after it, and the counted work, which wants no quiet machine, 10:24 to 11:06. **The intrusion verdict is clean over the whole of that**: `--wild` over the 119 logs this run wrote finds no bench at 0.25 foreign in the 114 that carry samples, the other five being the four rider drivers and the wall-clock log, which carry none.

**The gate read SOUND and the machine check did not fire.** The two palindrome passes agree: `mut-odo-vecdims` reads 1.0043 on both, `bq-expand` 1.3052 and 1.3046, and `list` 1.2963 and 1.3123 --- 0.00, 0.06 and 1.60 points apart --- with the two `sum-only` controls, on raw `slope`, at 0.9999 against 1.0003 and 1.0000 against 1.0003. **`list`'s 1.60 points are one half's own leg-to-leg movement and not a disagreement about the pair**: the control's `a` leg over its `b` reads `list` at 1.0128 where the basis's two legs read 1.0004, which predicts the second pass at 1.0124 times the first against an observed 1.0123. The machine check, read against the fingerprint Run 35 installed, puts `list`'s net at -0.23%, worst `stretch-square-1341` at +1.63%, 0 of 19 shapes past 5% and the geomean inside the 3% bar --- **which is not a box reading on this run**, the kept fingerprint being Run 35's ghc-9.12.4 basis, so what it says is that the box and the two compiler steps together sum to less than the bar.

**Every one of the twenty-two processes gated clean, the plateau refused by declaration, and SEVEN A/A worst cells sit past 5%.** `read-all.sh` gates each process on its own correction and passes all twenty-two. The plateau band refuses, as the pair note declared before the run that it would: the victim runs 16.6997 to 21.5794 ms/iter across the run, a 29.22% spread against a 5% band --- but it splits exactly by half, the basis's eleven processes flat within 1.77% at 21.2040 to 21.5794 and the control's eleven within 1.82% at 16.6997 to 17.0044, which is the variable working and not the box moving. The seven A/A worst cells past 5% are `gheadnospec-main` at 28.36%, `gheadtwopass-runs` at 9.21%, `gheadtwopass-block` at 7.29%, `gheadnospec-flip` at 6.49%, `gheadnospec-runs` at 6.07%, `gheadtwopass-window` at 5.50% and `gheadtwopass-flip` at 5.40%; the first has a paragraph of its own under Results and the rest sit on populations whose floors this file publishes.

**The pair's own identity, transcribed before its note goes with it.** The two binaries are `run36-gheadnospec`, md5 `b85f2f04ac065eb78e499fd4fc0a164c`, and `run36-gheadtwopass`, md5 `40ad21b4e1de28c617c91d1a3d35b1ee`, built back to back in one call on 2026-09-18 against a clean tree. Their `.text` sections are **20379455** and **20383551** bytes, the first column of `size -A`, and both load at 4214784, which is `run35-gheadexit`'s load address unchanged. **NEITHER md5 reproduces anything**: the basis carries `run35-gheadexit`'s recipe on an unmoved source, so a repetition was there to be read and the compiler moved instead --- `10.1.20260918` against `10.1.20260803`, on a rebuilt dependency stack, criterion included. What the two md5s do instead is DIFFER, which is the two passes having reached the emission.

**The source stood still and the compiler moved, which is the reverse of Run 35's provenance and leaves the pinning claim's strong form untested again.** `Main.hs` is at `0eda736` on both builds, so no figure here carries a source term; what is new under the recipe is six weeks of GHC HEAD. `./loop-offsets.py --delta run35-gheadexit run36-gheadnospec` reads EVERY mod-64 offset preserved on both tracked groups, [18, 0, 0, 0, 9, 2] and [0, 0], with no address surviving to the byte and three displacements on the six-copy group and two on the other --- so a six-week compiler move displaced every copy and no head's offset. Within the pair the two passes do move them: the six-copy group reads [18, 0, 0, 0, 9, 2] on the basis and [18, 0, 7, 7, 9, 26] on the control, and `--library` puts the two halves at 4.3% the same offset in line over 809 common library self-loops.

**The straddling loops stand at EIGHT on each half, as on Runs 32 to 35, and no exit span sits astride on either.** `loop-offsets.py --survey` reads 387 self-loops of at most 64 B in `_Main_`-compiled code on the basis and 310 on the control, 8 straddling on each and 0 exit spans astride, which is what `LOOP_EXITSPAN=1` owes. **Post-run step 0's naming, taken off the binaries that were timed, puts the SAME eight bodies at the SAME eight mod-64 offsets on each half** --- 42, 42, 19, 49, 45, 42, 19 and 29 in address order --- five named by byte identity against this run's own `-g3` twins and three by `--loose` signature, each of those three having either one family member or the rest already anchored. So the two passes moved no straddling loop across a cache line, and the straddle map is one map for the pair.

**The regime was confirmed in this run's own binaries before the hours were spent, and the two halves read DIFFERENTLY, which is the point of the pair.** `diag` on `vgg-14-c512` puts `baseOffsetsScan` against `baseOffsetsMut` at 24066455 against 2408530 on `run36-gheadnospec`, 9.992 times apart, which is plain -O1 and is `run35-gheadexit`'s pair of figures to the byte; on `run36-gheadtwopass` the same two read 2408978 against 2408530, EQUAL TO THREE FIGURES, which is SpecConstr having fired. So pre-run steps 9 and 9b are one reading on this pair, and the variable is legible in the binary before any bench runs.

**The three main-set anchors** read **6.32 us** on `cnn-slice-c32`, **3.71 ms** on `cnn-L2-24x24-c32` and **39.6 ms** on `stretch-wide-2xM`, net of the forcing pass on the basis half, with the control half's beside them --- the absolutes every ratio in this file divides away, kept so a later run can tell a moved box from a moved arm. The control column is the flagged half and is 20 to 22 points below the basis on all three, which is the pair's own variable and not the box:
| shape | `l` | `list`, per call | net | `gheadtwopass`, net |
|---|---:|---:|---:|---:|
| `cnn-slice-c32` | 288 | 6.49 us | 6.32 us | 4.98 us |
| `cnn-L2-24x24-c32` | 165888 | 3.81 ms | 3.71 ms | 2.91 ms |
| `stretch-wide-2xM` | 1800000 | 40.7 ms | 39.6 ms | 31.6 ms |

**Each stride class carries an anchor of its own, beside its table, and all ten are `list` on one of that class's own shapes, raw and net, off the basis half.** `rev-primes` 4.63 ms raw and 4.48 ms net; `bcast-inner900` 30.8 ms and 29.7 ms; `bcastmid-b200k` 48.4 ms and 47.3 ms; `window-128x128-k7` 14.2 ms and 13.8 ms; `scaled-rank1-m1` 5.29 ms and 5.11 ms; `runs-2` 41 ms and 40 ms; `flip-fwd-rows96` 31 ms and 29.9 ms; `block-r3-vol64` 4.6 ms and 4.44 ms; `small-row96` 6.65 us and 6.43 us; `compose-zero-mid` 31.3 ms and 30.2 ms. Each is one process's reading of one shape and crosses to no other population.

**The correction sits on the same footing in both halves, and five cells of the whole run are ones the reader flags.** The two `sum-only` arms agree to within **0.25%** on every population and on both halves of the pair --- 0.9992 on `bcast`'s basis to 1.0025 on `compose`'s across the twenty-two --- so the term subtracted from one half is the term subtracted from the other. `CI%` reads a geomean of **1.02** over the 35 arms, 22 wider on the basis and 13 narrower. **FIVE cells sit below R2 0.99, all of them on the BASIS half**: `stretch-coprime-r7/list` at 0.9395 on the main set, which Results reads as this run's one anomaly, and four on `flip`, worst `flip-last-rows/mut-odo-vecdims-nosum` at 0.9736; the control half carries none, and no cell of any population sits under ten samples.

**The counted work covers every population, no cell was refused anywhere, and the two halves emit very different work.** `run-counts-all.sh` wrote 22 sweep files over eleven populations on each half, 0 cells refused, at a cost of 1381s on the basis and 1142s on the control. The counts geomean over the sixteen timed arms runs **1.1424** on `small` to **1.1765** on `window`, the main set at **1.1663** --- the basis retiring some sixteen percent more instructions than the flagged half across every population. **On the main set `time/counts` separates the families cleanly**: the `bq-expand` trio sits at 0.8617 to 0.8645, retiring 50.6% more instructions on the basis for 30% more time; the `list` trio at 1.0139 to 1.0336, its time moving further than its counts; and the ten others between 0.9448 and 0.9713, retiring four to five percent more on the basis at a clock within 1.2 points of level. So the two passes buy `bq-expand` far more in instructions than they cash on the clock, and buy `list` rather less.

**The correction is invertible, so pre-correction figures stay comparable.** The `sum-only` term subtracted from every cell is published per shape, and the two `sum-only` halves agree at **1.0001** on the basis and **1.0001** on the control on the main set, so the quantity taken out of the two columns is the same quantity. The in-situ term, an arm minus its `-nosum` twin against the `sum-only` the correction actually subtracts, reads **1.0332** and **1.0882** on the basis and **1.0289** and **1.0703** on the control for the `mut-odo-vecdims` and `bq-expand` pairs: the proxy runs about three percent over the term it stands for on `mut-odo-vecdims` and seven to nine on `bq-expand`, by nearly the same on both halves. So the two passes do not move the correction, and no ratio in this file is an artefact of a forcing pass that parted between the halves.

**The decomposition reproduces on both halves and its two columns part by the pair's own variable.** The riders time each shape's `list` alone, one bench to a process, clean and then saturated, and the state the preamble puts on a process comes back at a geomean of **1.1174** on the basis and **1.1666** on the control, **4.9** points apart, where Run 35's two halves parted by 0.07 --- so the two passes change what the spray costs a process as well as what the roster costs it. What the roster adds on top of that state is **1.0406** on the basis, 10 of 19 shapes above 1, and **0.9924** on the control, 4 of 19; the basis's rest runs 0.9756 on `stretch-bigstride` to 1.3788 on `stretch-coprime-r7`, the control's 0.9182 on `stretch-pow2stride` to 1.0786 on `stretch-tall-Mx2`.

[dead]: ../README.md#dead-ideas
[floor]: ../README.md#what-moves-a-figure-when-no-strategy-changed
[open]: ../README.md#what-is-open
[pershape]: ../README.md#per-shape-where-the-geomean-hides-the-ordering
[procedure]: ../README.md#making-a-major-benchmark-run
[ramp]: ../README.md#r2-is-the-ramp-detector-not-the-noise-detector
[prov]: ../README.md#provenance


## What this run was built to answer, and what it answered

Registered in README's open list on the date the entry carries, before the run, and moved here whole at post-run step 5; the verdicts are the write-up's to add beside each prediction, and the summary sentence its to write.

The pair is the REGIME: both halves are GHC HEAD at the `-O1` level in the dead-spot form under the exit span, one source (`Main.hs` at `0eda736`), one shim (`align-as.py` at `f31bd1c`), one shim environment, one roster, one shape set and one launch from `hugebin/`, and the control half's command line carries `-fspec-constr -fliberate-case` besides, nothing else differing --- so every span below reads the two `-O2` passes TOGETHER, in `--compare`'s orientation of the unflagged basis over the flagged control, which is the half `on main basis` names, the population being the rest of it. It is the pair Run 31's arithmetic wanted and no run since could supply. Off `run31-nospec-main.json` against `run31-o2-main.json`, re-derived here rather than quoted, the whole `-O2` level read **1.2974** on `list` and **1.2943** on `bq-expand`, where the two passes measured ONE AT A TIME on Runs 29 and 30 --- 1.1379 and 1.1710 on `list`, 1.2804 and 1.0127 on `bq-expand`, off those runs' own files, `runs/run29.md` and `runs/run30.md`, their artifacts being gone --- and Run 29's two are the RECIPROCALS of what its file publishes, that run's basis having been the FLAGGED half: it reads `list` at **0.8788** and `bq-expand` at **0.7810**, and says `list` is 13.79% slower without the flag --- multiply to **1.3325** and **1.2967**. So the composition overshoots the level by 3.51 points on `list` and sits 0.24 of a point from it on `bq-expand`: this pair separates the two accounts on `list` and CANNOT on `bq-expand`, which is what makes the second arm the first one's control rather than a second reading of the same question. TWO LIMITS, both named before it runs and neither removable by it: the compiler moved under the ruled recipe on 2026-09-18, to a HEAD of that date where Runs 29 to 31 were ghc-9.12.4 builds, so every distance from their figures carries the two passes AND two compiler steps, across neither of which has any run here measured what these two passes are worth; and the dependency stack rebuilt with it, criterion included.

(1) *The two passes together are worth on `list` what the whole level was worth, not what composing the two single-pass runs gives.* `predict: cross list 1.2974 within 1.3% on main basis`. The band is 1.3 points against the 3.51-point gap it has to resolve, so a reading above 1.3104 falls on the composition's side and says `-O2`'s other passes hand `list` back, while one below 1.2844 is neither account; which of those to read as the compiler is what item (2) says.

**Read by --predictions, item (1):** `cross list 1.2974 within 1.3% on main basis`: KILLED on main basis, read 1.3360 over 19 shape(s), 3.86 point(s) off, within 1.30%.

(2) *And `bq-expand`, where the two accounts agree to a quarter of a point, reads where both put it.* `predict: cross bq-expand 1.2943 within 1.5% on main basis`. This span cannot tell the two accounts apart and is not asked to: inside it, these passes are worth on this HEAD what they were worth on 9.12.4 for that arm and item (1) is the composition question; outside it, the compiler has moved the regime's worth and item (1) prices these two passes on this HEAD while settling nothing about Run 31's arithmetic.

**Read by --predictions, item (2):** `cross bq-expand 1.2943 within 1.5% on main basis`: HELD on main basis, read 1.2980 over 19 shape(s), 0.37 point(s) off, within 1.50%.

(3) *The gain is confined to the `list` and `bq-expand` families, and no arm Run 31 timed outside them joins them.* Run 31's sixteen arms with a corrected time rank into exactly two groups with nothing between them: the six of those two families at 1.2887 to 1.2974, and the other ten at 0.9745 to 1.0097, the widest being `mut-odo-vecdims-add-in-leaf-u1` at 2.55 points the basis's way. The ten bands below are set AT that widest reading rather than under it, so each tolerates its own arm's Run 31 movement repeating and refuses only an arm joining the families --- `predict: cross mut-odo-vecdims 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-aa 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-aa-distant 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-add-in-leaf-u1 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-add-in-leaf-u2 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-add-in-leaf-u2-aa 1.0 within 3% on main basis`, `predict: cross mut-odo-vecdims-add-in-leaf-u2-aa-distant 1.0 within 3% on main basis`, `predict: cross lib-stage1 1.0 within 3% on main basis`, `predict: cross lib-stage2-lean 1.0 within 3% on main basis`, `predict: cross lib-stage2-lean-u1 1.0 within 3% on main basis`, and the two families' own members at the level's figures for them: `predict: cross list-aa-adjacent 1.2921 within 1.5% on main basis`, `predict: cross list-aa-distant 1.2887 within 1.5% on main basis`, `predict: cross bq-expand-aa-adjacent 1.2937 within 1.5% on main basis`, `predict: cross bq-expand-aa-distant 1.2967 within 1.5% on main basis`. The arms this roster times that Run 31's did not carry no prior here and no span.

**Read by --predictions, item (3):** `cross mut-odo-vecdims 1.0 within 3% on main basis`: HELD on main basis, read 1.0082 over 19 shape(s), 0.82 point(s) off, within 3.00% --- `cross mut-odo-vecdims-aa 1.0 within 3% on main basis`: HELD on main basis, read 1.0085 over 19 shape(s), 0.85 point(s) off, within 3.00% --- `cross mut-odo-vecdims-aa-distant 1.0 within 3% on main basis`: HELD on main basis, read 1.0047 over 19 shape(s), 0.47 point(s) off, within 3.00% --- `cross mut-odo-vecdims-add-in-leaf-u1 1.0 within 3% on main basis`: HELD on main basis, read 1.0033 over 19 shape(s), 0.33 point(s) off, within 3.00% --- `cross mut-odo-vecdims-add-in-leaf-u2 1.0 within 3% on main basis`: HELD on main basis, read 1.0079 over 19 shape(s), 0.79 point(s) off, within 3.00% --- `cross mut-odo-vecdims-add-in-leaf-u2-aa 1.0 within 3% on main basis`: HELD on main basis, read 1.0076 over 19 shape(s), 0.76 point(s) off, within 3.00% --- `cross mut-odo-vecdims-add-in-leaf-u2-aa-distant 1.0 within 3% on main basis`: HELD on main basis, read 1.0119 over 19 shape(s), 1.19 point(s) off, within 3.00% --- `cross lib-stage1 1.0 within 3% on main basis`: HELD on main basis, read 1.0037 over 19 shape(s), 0.37 point(s) off, within 3.00% --- `cross lib-stage2-lean 1.0 within 3% on main basis`: HELD on main basis, read 1.0008 over 19 shape(s), 0.08 point(s) off, within 3.00% --- `cross lib-stage2-lean-u1 1.0 within 3% on main basis`: HELD on main basis, read 0.9920 over 19 shape(s), 0.80 point(s) off, within 3.00% --- `cross list-aa-adjacent 1.2921 within 1.5% on main basis`: KILLED on main basis, read 1.3106 over 19 shape(s), 1.85 point(s) off, within 1.50% --- `cross list-aa-distant 1.2887 within 1.5% on main basis`: KILLED on main basis, read 1.3111 over 19 shape(s), 2.24 point(s) off, within 1.50% --- `cross bq-expand-aa-adjacent 1.2937 within 1.5% on main basis`: HELD on main basis, read 1.3011 over 19 shape(s), 0.74 point(s) off, within 1.50% --- `cross bq-expand-aa-distant 1.2967 within 1.5% on main basis`: HELD on main basis, read 1.3023 over 19 shape(s), 0.56 point(s) off, within 1.50%.

(4) *And the counted work parts on all four arms this item spans, the two families far further than the two outside them.* Off Run 31's own sweeps, `run31-counts-nospec.txt` against `run31-counts-o2.txt`, the level's counts read **1.3120** on `list` and **1.4423** on `bq-expand` against 1.0380 to 1.0530 on the ten arms outside those families --- not one of its arms read 1.0000, which is why this item's lead says every arm and its timed twin at (3) says none: `predict: counts list 1.3120 within 1.5% on main basis`, `predict: counts bq-expand 1.4423 within 2% on main basis`, `predict: counts mut-odo-vecdims 1.0380 within 1% on main basis`, `predict: counts lib-stage2-lean 1.0516 within 1% on main basis`, read with `--counts` over the main set's own sweep, which run list step 20 takes. A `counts` span here reads the two HALVES and so asks the passes' question in the same vocabulary its prose uses, which is what [Run 35's own item (3)](run35.md#what-this-run-was-built-to-answer-and-what-it-answered) wanted and did not have.

**Read by --predictions, item (4):** `counts list 1.3120 within 1.5% on main basis`: KILLED on main basis, read 1.2926 over 19 shape(s), 1.94 point(s) off, within 1.50% --- `counts bq-expand 1.4423 within 2% on main basis`: KILLED on main basis, read 1.5063 over 19 shape(s), 6.40 point(s) off, within 2.00% --- `counts mut-odo-vecdims 1.0380 within 1% on main basis`: HELD on main basis, read 1.0383 over 19 shape(s), 0.03 point(s) off, within 1.00% --- `counts lib-stage2-lean 1.0516 within 1% on main basis`: HELD on main basis, read 1.0522 over 19 shape(s), 0.06 point(s) off, within 1.00%.

**ONE item is killed and THREE hold their sentences, over 20 spans of which 15 held and 5 were killed --- and four of the five kills are the first one counted again.** Every verdict below is its item's KILL CONDITION applied across the population and half it names, which on this registration is `main basis` for all twenty spans; every figure is re-derived from this run's own JSONs, by `--predictions` over the main set on the basis half and by `--counts` where a clause names instructions. **One thing governs how the list reads**: the two passes do to `bq-expand` what both accounts of them predicted and do to `list` more than the level account allows, so the item built to separate the two accounts is the one that dies, and it dies on the side that says `-O2`'s other passes hand `list` back.

(1) *The two passes together are worth on `list` what the whole level was worth, not what composing the two single-pass runs gives.* **KILLED, and killed informatively.** The span asked for 1.2974 within 1.3 points and the run reads **1.3360**, 3.86 points out and above the 1.3104 the item itself named as the composition's side --- so the answer is the one the item's own text assigned to that outcome: `-O2`'s other passes hand `list` back, and Runs 29 and 30 composed, at 1.3325, is the better account of these two passes than Run 31's level figure. **The margin is smaller than it reads, and the registration could not have known it**: the run's one wild cell, `stretch-coprime-r7/list` on the basis, is worth 2.31 of those 3.86 points, and with that shape excluded `list` reads **1.3129** --- still outside the band and still above 1.3104, but BETWEEN the two accounts rather than past both. So what the pair settles is that Run 31's level figure is the wrong account of these two passes; what it does not settle, to better than a point and a half, is how much of the 3.51-point gap the level's other passes own.

(2) *And `bq-expand`, where the two accounts agree to a quarter of a point, reads where both put it.* **HELD**, at **1.2980** against 1.2943 within 1.5 points, 0.37 of a point out, inside a band the level account and the composition account both name. By the item's own reading that settles the compiler question it was registered to settle: these two passes are worth on this HEAD what they were worth on ghc-9.12.4 for that arm, so item (1)'s miss is the composition question and not the compiler having moved under the pair.

(3) *The gain is confined to the `list` and `bq-expand` families, and no arm Run 31 timed outside them joins them.* **The sentence HOLDS and two of its fourteen spans are killed.** All ten arms outside the two families come in within 3% of 1, the widest `mut-odo-vecdims-add-in-leaf-u2-aa-distant` at **1.0119** and the narrowest `lib-stage2-lean` at 1.0008, so not one of them joins the families and the confinement is exact. The two `bq-expand` twins hold, at 1.3011 and 1.3023 against 1.2937 and 1.2967 within 1.5. The two `list` twins are killed, at **1.3106** and **1.3111** against 1.2921 and 1.2887 --- 1.85 and 2.24 points out, in the same direction as item (1)'s miss and from the same source, their targets having come off the same Run 31 level reading.

(4) *And the counted work parts on all four arms this item spans, the two families far further than the two outside them.* **The sentence HOLDS and two of its four spans are killed.** The parting is as the item described it and wider: `list` reads **1.2926** and `bq-expand` **1.5063** where `mut-odo-vecdims` reads 1.0383 and `lib-stage2-lean` 1.0522, so the two families part from the two arms outside them by between 24 and 47 points. What is killed is the SIZE on the families: `list` at 1.2926 against 1.3120 within 1.5 is 1.94 points under, and `bq-expand` at 1.5063 against 1.4423 within 2 is 6.40 points over --- the counted work moving LESS than Run 31's level did on `list` and MORE on `bq-expand`. The two arms outside the families hold to three and six ten-thousandths.
